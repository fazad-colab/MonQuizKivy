# -*- coding: utf-8 -*-
"""
rangs_ui.py — badges de rang, popup de promotion, menu Évolution, classement.

 * Promotion détectée quand l'index de rang dépasse le meilleur rang déjà célébré (rang_max_idx, sauvegardé) :
     - examen, défi, session de groupe, question de salle → le popup ATTEND que l'on quitte la session
     - entraînement → bandeau compact en haut (rien n'est interrompu, le chrono continue)
     - partout ailleurs → grand popup plein écran avec flammes
 * Évolution : page HTML (surcouche de Locky) ; l'ancien menu Kivy reste le secours si la surcouche est indisponible
"""
import json
import os
import time

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import rangs_core as rc

try:
    from android_math_webview import DOSSIER_APP
except Exception:
    DOSSIER_APP = "."

CTX_ATTENTE = ("examen", "defi", "defi_calcul_mental", "multi", "salle_question")   # on n'interrompt pas ces sessions
CLES_CFG = {"m": str, "type": str, "pal": str, "plage": int, "top": int, "tri": str,
            "grille": bool, "points": bool, "valeurs": bool, "lisse": bool, "multi": bool}


class FonctionsRangs:

    # ------------------------------------------------------------------ données persistantes
    def rangs_defauts(self):
        self.rang_max_idx = -1               # meilleur rang déjà célébré (-1 : pas encore initialisé)
        self.notes_examen = []
        self.evo_cfg = {}
        self._promo_file = []
        self._promo_actif = None
        self._promo_retour = None
        self._classement = {}
        self._clas_t = 0.0
        self._liste_cache = (None, None)

    def rangs_vers_dict(self):
        return {"rang_max_idx": self.rang_max_idx, "notes_examen": self.notes_examen[-60:], "evo_cfg": self.evo_cfg}

    def rangs_depuis_dict(self, data):
        self.rang_max_idx = int(data.get("rang_max_idx", -1))
        self.notes_examen = [float(x) for x in (data.get("notes_examen") or []) if isinstance(x, (int, float))][-60:]
        cfg = data.get("evo_cfg") or {}
        self.evo_cfg = {k: cfg[k] for k, t in CLES_CFG.items() if k in cfg and isinstance(cfg[k], t)}

    def rangs_resync(self):
        """La progression a changé hors jeu (connexion, effacement…) : on aligne, SANS popup."""
        try:
            self.rang_max_idx = self.determiner_rang_et_details()[3]
        except Exception:
            pass
        self._promo_file = []

    # ------------------------------------------------------------------ badges / données pour la page
    def _rangs_liste(self):
        dossier = os.path.join(DOSSIER_APP, "badges")
        index = rc.indexer_badges(dossier)
        sig = tuple(sorted(index.items()))
        if self._liste_cache[0] != sig:                    # nouveaux badges ajoutés dans le dossier : on reconstruit
            self._liste_cache = (sig, rc.construire_liste(self.LISTE_RANGS, index))
        return self._liste_cache[1]

    def rangs_payload(self):
        rang, rp_in, seuil, idx = self.determiner_rang_et_details()
        hist = list(getattr(self, "historique_scores", []) or [])
        return {"liste": self._rangs_liste(), "idx": idx, "rp_in": rp_in, "seuil": seuil,
                "total_rp": int(self.points_de_rang), "best_rp": max([self.meilleur_rp, int(self.points_de_rang)] + [int(x) for x in hist[-500:] or [0]]),
                "jours": self.jours_connectes, "niveau_profil": getattr(self, "niveau_profil", 1),
                "hist": rc.echantillonner(hist, 150), "notes": self.notes_examen[-60:],
                "chap": rc.chapitres_pour_page(getattr(self, "stats_chapitres", {})),
                "cfg": self.evo_cfg, "rythme": list(rc.rythme(hist)), "clas": self._classement}

    # ------------------------------------------------------------------ promotions
    def _rangs_tick(self):
        try:
            idx = self.determiner_rang_et_details()[3]
        except Exception:
            return
        if self.rang_max_idx < 0:                          # première fois : pas de popup pour l'existant
            self.rang_max_idx = idx
            return
        if idx > self.rang_max_idx:
            self._promo_file.append((self.rang_max_idx, idx))
            self.rang_max_idx = idx
            self.sauvegarder_donnees_locales()
        if self._promo_file and self._promo_actif is None:
            self._promo_essayer()

    def _promo_essayer(self):
        ctx = getattr(self, "_locky_ctx", "menu")
        if ctx in CTX_ATTENTE:
            return                                         # on attend la fin de l'examen / du défi / de la session
        ov = self.locky_overlay
        if ov.pret and ov.mode not in ("avatar", "pg"):
            return                                         # profil, calculatrice, paramètres… ouverts : on patiente
        de, vers = self._promo_file[0][0], self._promo_file[-1][1]
        self._promo_file = []
        liste = self._rangs_liste()
        r, avant = liste[vers], liste[de]
        _, rp_in, seuil, _ = self.determiner_rang_et_details()
        mini = ctx == "entrainement"                       # bandeau compact : l'entraînement n'est pas coupé
        info = {"nom": r["n"], "tier": r["t"], "niv": r["v"], "col": r["col"], "b": r["b"], "idx": vers, "total": len(liste),
                "nb": vers - de, "division": r["t"] != avant["t"], "rp_in": rp_in, "seuil": seuil,
                "total_rp": int(self.points_de_rang), "titre": r["ti"], "mini": mini}
        self._promo_actif = time.time()
        self._promo_retour = "pg" if ov.mode == "pg" else None
        self.locky_signal("promotion", rang=r["n"])
        if ov.pret:
            ov.regler_mode("rangm" if mini else "rang")
            ov.js("R.promo(%s)" % json.dumps(info, ensure_ascii=False))
        else:
            self._promo_kivy(info)

    def _promo_fin(self):
        """Appelé uniquement quand l'utilisateur TOUCHE le popup."""
        self._promo_actif = None
        retour, self._promo_retour = self._promo_retour, None
        ov = self.locky_overlay
        if ov.mode in ("rang", "rangm"):
            ov.regler_mode(retour or "avatar")                # un replay lancé depuis Évolution y revient

    def rangs_revoir(self, i):
        """Rejoue l'animation d'un rang déjà débloqué (jamais d'un rang verrouillé)."""
        try:
            idx_actuel = self.determiner_rang_et_details()[3]
        except Exception:
            return
        liste = self._rangs_liste()
        i = int(i)
        if not (0 <= i <= idx_actuel) or self._promo_actif is not None:
            return
        r = liste[i]
        avant = liste[i - 1] if i > 0 else r
        info = {"nom": r["n"], "tier": r["t"], "niv": r["v"], "col": r["col"], "b": r["b"], "idx": i, "total": len(liste),
                "nb": 1, "division": i == 0 or r["t"] != avant["t"], "rp_in": r["s"], "seuil": r["s"], "cumul": r["c"],
                "total_rp": int(self.points_de_rang), "titre": r["ti"], "mini": False, "replay": True}
        ov = self.locky_overlay
        self._promo_actif = time.time()
        self._promo_retour = "evo" if ov.mode == "evo" else None
        ov.regler_mode("rang")
        ov.js("R.promo(%s)" % json.dumps(info, ensure_ascii=False))

    def _promo_kivy(self, info):
        """Secours sans surcouche (PC) : popup simple avec le badge."""
        boite = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(6))
        if info["b"] and os.path.exists(os.path.join(DOSSIER_APP, info["b"])):
            boite.add_widget(Image(source=os.path.join(DOSSIER_APP, info["b"])))
        boite.add_widget(Label(text=f"[b]{info['nom'].upper()}[/b]\n{info['total_rp']} RP", markup=True, font_size="22sp",
                               size_hint_y=None, height=dp(80)))
        p = Popup(title="PROMOTION !", content=boite, size_hint=(0.85, 0.6))
        p.bind(on_dismiss=lambda *a: setattr(self, "_promo_actif", None))
        p.open()
        Clock.schedule_once(lambda dt: p.dismiss(), 5)

    # ------------------------------------------------------------------ Évolution
    def afficher_sous_menu_evolution(self, instance=None):
        ov = getattr(self, "locky_overlay", None)
        if ov is not None and ov.pret:
            self.locky_signal("evolution")
            ov.pousser(self.locky_donnees())
            ov.regler_mode("evo")
        else:
            self.afficher_sous_menu_evolution_legacy(instance)

    def rangs_evenement(self, e):
        a = e.get("a")
        if a == "rang_fin":
            self._promo_fin()
        elif a == "evo" and e.get("k") == "open" and e.get("v") in ("clas", "home"):
            self.rangs_charger_classement()
        elif a == "evo" and e.get("k") == "revoir":
            self.rangs_revoir(e.get("i", -1))
        elif a == "evo_cfg":
            cfg = e.get("cfg") or {}
            self.evo_cfg = {k: cfg[k] for k, t in CLES_CFG.items() if k in cfg and isinstance(cfg[k], t)}
            self.sauvegarder_donnees_locales()

    # ------------------------------------------------------------------ classement / rivalité
    def rangs_charger_classement(self, force=False):
        if time.time() - self._clas_t < 20 and not force:
            return
        if not getattr(self, "jeton_compte", "") or not getattr(self, "en_ligne", False):
            self._classement = {"hors_ligne": True}
            return
        self._clas_t = time.time()
        self.api("/api/classement", ok=self._clas_ok, err=lambda m: setattr(self, "_classement", {"hors_ligne": True}), timeout=8)

    def _clas_ok(self, r):
        index = rc.indexer_badges(os.path.join(DOSSIER_APP, "badges"))
        lignes = rc.lignes_classement(r.get("classement", []), getattr(self, "identifiant_joueur", ""), self.LISTE_RANGS, index)
        mon_rp = int(self.points_de_rang)
        pos = next((l["pos"] for l in lignes if l["moi"]), None)
        rival = None
        autres = [l for l in lignes if not l["moi"]]
        if autres:
            devant = [l for l in autres if l["rp"] >= mon_rp]
            if devant:                                     # le joueur juste au-dessus de moi
                v = min(devant, key=lambda l: l["rp"])
                rival = {"nom": v["nom"], "rang": v["rang"], "devant": True, "ecart": max(0, v["rp"] - mon_rp)}
            else:                                          # je suis devant : le plus proche poursuivant
                v = max(autres, key=lambda l: l["rp"])
                rival = {"nom": v["nom"], "rang": v["rang"], "devant": False, "ecart": max(0, mon_rp - v["rp"])}
        self._classement = {"charge": True, "lignes": lignes, "pos": pos, "rival": rival}
