# -*- coding: utf-8 -*-
"""
locky_ui.py — Locky au premier plan, menu « dark web », calculatrice intégrée.

Pourquoi Locky était caché : sur Android la WebView des questions est une vue NATIVE posée au-dessus de la
surface Kivy ; aucun widget Kivy ne peut passer devant. Solution : sur Android, Locky (avatar, bulle, menu,
calculatrice) est affiché dans une SECONDE WebView transparente, ajoutée après et avec une élévation plus
haute, donc toujours devant. Sur PC (ou si la vue native échoue), le Locky Kivy classique reste utilisé.
"""
import json
import random
import time

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import platform

import locky_core as core
from locky_page import page_complete

try:
    from android_math_webview import run_on_ui_thread, _resoudre_activite, _diag, DOSSIER_APP
except Exception:                                    # PC sans le module Android
    run_on_ui_thread = lambda f: f
    _resoudre_activite = None
    DOSSIER_APP = "."

    def _diag(msg):
        print("[Locky]", msg)


# ======================================================================================================
#  Surcouche Android
# ======================================================================================================
class LockyOverlay:
    """WebView native transparente, toujours devant, qui affiche Locky (avatar / menu / calculatrice)."""

    def __init__(self, app, mascotte, sur_evenement):
        self.app, self.mascotte, self.sur_evenement = app, mascotte, sur_evenement
        self.webview = None
        self.pret = False                 # la page HTML a envoyé « pret »
        self.mode = "avatar"              # avatar | menu | calc
        self._dernier_layout = None
        self._dernier_etat = None
        self._cb = None
        self._ev = None
        self._n = 0
        self.calc_pos = None
        self._d0 = None
        self._r0 = None
        self._dw = None

    @property
    def disponible(self):
        return platform == "android"

    def demarrer(self):
        if not self.disponible or self._ev is not None:
            return
        self._creer()
        self._ev = Clock.schedule_interval(self._tick, 1 / 20.0)

    # ---------------------------------------------------------------- création de la vue native
    def _creer(self):
        @run_on_ui_thread
        def creer():
            try:
                from jnius import autoclass
                WebView = autoclass("android.webkit.WebView")
                WebViewClient = autoclass("android.webkit.WebViewClient")
                FLP = autoclass("android.widget.FrameLayout$LayoutParams")
                Gravity = autoclass("android.view.Gravity")
                activite, _ = _resoudre_activite()
                try:
                    # doit être identique à celui de la WebView des questions (Pydroid3 : 1 seul répertoire de données)
                    WebView.setDataDirectorySuffix("nexusmath")
                except Exception as e:
                    _diag(f"Locky: setDataDirectorySuffix: {e}")
                wv = WebView(activite)
                wv.setWebViewClient(WebViewClient())
                wv.setBackgroundColor(0)                      # transparent
                wv.setLayerType(1, None)                      # rendu logiciel : fond transparent fiable
                wv.setVerticalScrollBarEnabled(False)
                wv.setHorizontalScrollBarEnabled(False)
                wv.setOverScrollMode(2)
                try:
                    wv.setElevation(80.0)                     # au-dessus de la WebView des questions, quel que soit l'ordre de création
                except Exception:
                    pass
                st = wv.getSettings()
                st.setJavaScriptEnabled(True)
                st.setDomStorageEnabled(True)
                st.setAllowFileAccess(True)
                st.setAllowFileAccessFromFileURLs(True)
                st.setAllowUniversalAccessFromFileURLs(True)
                st.setSupportZoom(False)
                st.setBuiltInZoomControls(False)
                p = FLP(1, 1)
                p.gravity = Gravity.TOP | Gravity.LEFT
                wv.setVisibility(4)
                activite.addContentView(wv, p)
                wv.loadDataWithBaseURL("file://" + DOSSIER_APP + "/", page_complete(), "text/html", "UTF-8", None)
                self.webview = wv
                _diag("Locky: surcouche créée")
            except Exception as e:
                _diag(f"Locky: création impossible : {e}")
        try:
            creer()
        except Exception as e:
            _diag(f"Locky: thread UI inaccessible : {e}")

    # ---------------------------------------------------------------- Python -> page
    def js(self, code):
        wv = self.webview
        if wv is None or not self.disponible:
            return

        @run_on_ui_thread
        def exe():
            try:
                wv.evaluateJavascript(code, None)
            except Exception as e:
                _diag(f"Locky JS: {e}")
        exe()

    def dire(self, texte):
        if self.pret:
            self.js("LK.dire(%s)" % json.dumps(texte or ""))

    def pousser(self, etat):
        brut = json.dumps(etat, ensure_ascii=False, sort_keys=True)
        if brut != self._dernier_etat and self.pret:
            self._dernier_etat = brut
            self.js("LK.maj(%s)" % brut)

    def regler_mode(self, mode):
        self.mode = mode
        if mode == "avatar":
            self.app._page_courante_active = False            # plus de page en cours : on est sur l'écran de jeu
        self._dernier_layout = None
        if self.pret:
            self.js("LK.mode(%s)" % json.dumps(mode))

    # ---------------------------------------------------------------- page -> Python (lecture des événements)
    def _callback(self):
        from jnius import PythonJavaClass, java_method

        class _Rappel(PythonJavaClass):
            __javainterfaces__ = ["android/webkit/ValueCallback"]
            __javacontext__ = "app"

            def __init__(self, fn):
                super().__init__()
                self._fn = fn

            @java_method("(Ljava/lang/Object;)V")
            def onReceiveValue(self, valeur):
                try:
                    self._fn(valeur.toString() if hasattr(valeur, "toString") else str(valeur))
                except Exception as e:
                    _diag(f"Locky rappel: {e}")
        return _Rappel(self._recu)

    def _recu(self, brut):
        try:
            interne = json.loads(brut)                    # evaluateJavascript renvoie une chaîne JSON
            evts = json.loads(interne) if isinstance(interne, str) else interne
        except Exception:
            return
        for e in evts or []:
            Clock.schedule_once(lambda dt, e=e: self._traiter(e), 0)

    def _traiter(self, e):
        if e.get("a") == "pret":
            self.pret = True
            self._dernier_etat = None
            self.js("LK.mode(%s)" % json.dumps(self.mode))
        self.sur_evenement(e)

    def _lire(self):
        wv = self.webview
        if wv is None:
            return
        if self._cb is None:
            self._cb = self._callback()
        cb = self._cb

        @run_on_ui_thread
        def lire():
            try:
                wv.evaluateJavascript("(function(){var q=window.__lk_q||[];window.__lk_q=[];return JSON.stringify(q);})()", cb)
            except Exception as e:
                _diag(f"Locky lecture: {e}")
        lire()

    # ---------------------------------------------------------------- glisser (Locky ou calculatrice)
    def drag(self, e):
        """La page envoie la position DOIGT en pixels écran (donc indépendante du déplacement de la vue)."""
        ph, w = e.get("ph"), e.get("w")
        if ph == "s":
            if self.mode != ("calc" if w == "calc" else "avatar"):
                return
            r = self._rect()
            if r is None:
                return
            self._d0 = (float(e.get("x", 0)), float(e.get("y", 0)))
            self._r0 = (r[0], r[1])
            self._dw = w
        elif ph == "m" and self._d0 is not None:
            r = self._rect()
            if r is None:
                return
            W, H = Window.width, Window.height
            nx = self._r0[0] + (float(e.get("x", 0)) - self._d0[0])
            ny = self._r0[1] - (float(e.get("y", 0)) - self._d0[1])          # l'écran descend, Kivy monte
            nx, ny = max(0, min(W - r[2], nx)), max(0, min(H - r[3], ny))
            if self._dw == "calc":
                self.calc_pos = (nx, ny)
            else:
                self.mascotte.pos = (nx, ny)
        elif ph == "e":
            if self._d0 is not None and self._dw != "calc":
                self.app.locky_cfg["coin"] = ""                                # position libre : on oublie le coin
                self.app.sauvegarder_donnees_locales()
            self._d0 = None

    # ---------------------------------------------------------------- géométrie
    def _rect(self):
        """(x, y_bas, w, h) en pixels Kivy, ou None si la surcouche doit être cachée."""
        m = self.mascotte
        if m.get_root_window() is None or m.parent is not getattr(self.app, "root_layout", None):
            return None                                    # intro / écran où Locky n'est pas sur le plateau principal
        W, H = Window.width, Window.height
        if self.mode in ("menu", "param", "evo", "pg"):
            return 0, 0, W, H                                  # pages principales : tout l'écran
        if self.mode == "rang":
            return 0, 0, W, H                                  # popup de promotion plein écran
        if self.mode == "rangm":
            return dp(6), H - dp(138), W - dp(12), dp(128)     # bandeau compact en haut (entraînement)
        if self.mode == "calc":
            w, h = W - dp(20), dp(340)                        # compacte : la question reste visible
            x, y = self.calc_pos or (dp(10), dp(64))          # déplaçable : on la saisit par son en-tête
            return max(0, min(W - w, x)), max(0, min(H - h, y)), w, h
        x, y = m.to_window(m.x, m.y)
        return x, y, m.width, m.height

    def _tick(self, dt):
        self._n += 1
        if self.webview is None:
            return
        if self.mode != "avatar" or self._d0 is not None or self._n % 2 == 0:
            self._lire()
        r = self._rect() if self.pret else None
        cle = None if r is None else tuple(int(v) for v in r) + (self.mode,)
        # le Locky Kivy n'est masqué que lorsque la surcouche est réellement affichée
        self.mascotte.opacity = 0 if cle is not None else 1
        if cle == self._dernier_layout:
            return
        self._dernier_layout = cle
        wv, H, mode_layout = self.webview, Window.height, self.mode

        @run_on_ui_thread
        def appliquer():
            try:
                from jnius import autoclass
                FLP = autoclass("android.widget.FrameLayout$LayoutParams")
                Gravity = autoclass("android.view.Gravity")
                if cle is not None:
                    x, y, w, h = r
                    p = FLP(max(1, int(w)), max(1, int(h)))
                    p.gravity = Gravity.TOP | Gravity.LEFT
                    p.setMargins(int(x), int(max(0, H - (y + h))), 0, 0)
                    wv.setLayoutParams(p)
                    wv.requestLayout()
                wv.setLayerType(1 if mode_layout == "avatar" else 2, None)   # matériel = défilement fluide ; logiciel = fond transparent fiable
                wv.setVisibility(0 if cle is not None else 4)
                if cle is not None:
                    from jnius import cast
                    par = wv.getParent()
                    par = cast("android.view.ViewGroup", par) if par is not None else None
                    if par is not None and par.getChildAt(par.getChildCount() - 1) != wv:
                        wv.bringToFront()                 # filet de sécurité en plus de l'élévation
            except Exception as e:
                _diag(f"Locky layout: {e}")
        appliquer()


# ======================================================================================================
#  Mixin de l'application
# ======================================================================================================
class FonctionsLocky:
    # ------------------------------------------------------------ données persistantes
    def locky_defauts(self):
        self.jours_connectes = 0
        self.dernier_jour_connexion = ""
        self.points_connexion = 0
        self.meilleur_rp = 0
        self.meilleure_note_examen = None
        self.locky_cfg = {"messages": True, "freq": "normal", "coin": ""}
        self._defi_actif = False
        self._multi_actif = False
        self.calc_groupe_autorisee = True
        self.rangs_defauts()
        self.pages_defauts()

    def locky_vers_dict(self):
        return {"jours_connectes": self.jours_connectes, "dernier_jour_connexion": self.dernier_jour_connexion,
                "points_connexion": self.points_connexion, "meilleur_rp": self.meilleur_rp,
                "meilleure_note_examen": self.meilleure_note_examen, "locky_cfg": self.locky_cfg,
                "audio_cfg": self.audio_cfg_vers_dict(), **self.rangs_vers_dict()}

    def locky_depuis_dict(self, data):
        self.jours_connectes = int(data.get("jours_connectes", 0) or 0)
        self.dernier_jour_connexion = data.get("dernier_jour_connexion", "") or ""
        self.points_connexion = int(data.get("points_connexion", 0) or 0)
        self.meilleur_rp = int(data.get("meilleur_rp", 0) or 0)
        self.meilleure_note_examen = data.get("meilleure_note_examen", None)
        cfg = data.get("locky_cfg") or {}
        self.locky_cfg = {"messages": cfg.get("messages", True), "freq": cfg.get("freq", "normal"), "coin": cfg.get("coin", "")}
        self.audio_cfg_depuis_dict(data.get("audio_cfg"))
        self.rangs_depuis_dict(data)

    # ------------------------------------------------------------ démarrage
    def locky_init(self):
        self.locky_msgs = core.MessagesLocky()
        self._locky_ctx = "menu"
        self._locky_t_activite = time.time()
        self._locky_t_idle = 0.0
        self._locky_popup = None
        self.locky_overlay = LockyOverlay(self, self.mascotte, self.locky_evenement)
        self.habiller_icone_neon(self.btn_parametres)          # icône ⚙ bien visible
        self._ev_bulle = None

        def bulle_changee(inst, v):
            self.locky_overlay.dire(v)
            if self._ev_bulle is not None:
                self._ev_bulle.cancel()
                self._ev_bulle = None
            if v:                                             # le message disparaît tout seul après 5 à 7 secondes
                self._ev_bulle = Clock.schedule_once(lambda dt, t=v: setattr(inst, "text", "") if inst.text == t else None, random.uniform(5, 7))
        self.mascotte.bulle_label.bind(text=bulle_changee)
        Window.bind(on_touch_down=lambda *a: setattr(self, "_locky_t_activite", time.time()))
        self.locky_overlay.demarrer()
        Clock.schedule_interval(self._locky_tick, 1.0)
        if self.locky_cfg.get("coin"):
            Clock.schedule_once(lambda dt: self.locky_placer(self.locky_cfg["coin"], anime=False), 0.2)

    def locky_enregistrer_connexion(self):
        j, d, p, n, evt = core.maj_connexion(self.jours_connectes, self.dernier_jour_connexion,
                                             self.points_connexion, self.niveau_mascotte)
        self.jours_connectes, self.dernier_jour_connexion, self.points_connexion, self.niveau_mascotte = j, d, p, n
        if evt:
            self.sauvegarder_donnees_locales()
            Clock.schedule_once(lambda dt: self.locky_signal("niveau" if evt == "niveau" else "jour"), 1.0)

    def locky_noter_examen(self, note_sur_20):
        note = round(float(note_sur_20), 1)
        self.notes_examen.append(note)
        if self.meilleure_note_examen is None or note > self.meilleure_note_examen:
            self.meilleure_note_examen = note

    # ------------------------------------------------------------ permission de la calculatrice
    def _locky_web_attache(self):
        web = getattr(self, "web_quiz", None)
        try:
            return web is not None and web.get_root_window() is not None
        except Exception:
            return False

    def calculatrice_permise(self):
        d = getattr(self, "_defi", None) or {}
        salon = getattr(self, "salon", None)
        return core.calculatrice_permise(
            defi_actif=bool(getattr(self, "_defi_actif", False) and self._locky_web_attache()),
            defi_genre=d.get("genre", ""), defi_cle=d.get("cle", ""), defi_titre=d.get("titre", ""),
            multi_actif=bool(getattr(self, "_multi_actif", False)),
            multi_autorisee=bool(getattr(self, "calc_groupe_autorisee", True)),
            salle_active=salon is not None,
            salle_autorisee=bool(((salon or {}).get("cfg") or {}).get("calculatrice", True)))

    # ------------------------------------------------------------ messages
    def locky_signal(self, evt, **kw):
        """Point d'entrée UNIQUE : l'appli dit ce qui se passe, Locky décide s'il réagit."""
        ctx_evt = {"menu", "choix_mode", "choix_classe", "entrainement", "examen", "defi", "defi_calcul_mental", "casse_tete",
                   "activites", "multi", "hub_multi", "salle_attente", "salle_question", "salle_fin", "cours", "stats",
                   "evolution", "ia", "parametres"}
        if evt in ctx_evt:
            self._locky_ctx = evt
        self._locky_t_activite = time.time()
        kw.setdefault("nom", getattr(self, "nom_utilisateur", "") or "")
        if evt in ("niveau", "jour"):
            kw.setdefault("niveau", self.niveau_mascotte)
            kw.setdefault("jours", self.jours_connectes)
            kw.setdefault("pts", self.points_connexion)
        texte = self.locky_msgs.choisir(evt, freq=self.locky_cfg.get("freq", "normal"), **kw)
        if texte and self.locky_cfg.get("messages", True):
            self.mascotte.bulle_label.text = texte
            if evt in ("bonne_serie5", "bonne_serie10", "niveau") or (evt == "bonne" and kw.get("combo", 0) in (5, 10)):
                self.mascotte.declencher_acrobatie(0)

    def _locky_tick(self, dt):
        """Une fois par seconde : état de la surcouche + réaction à l'INACTIVITÉ (jamais de message au hasard)."""
        if self.locky_overlay.mode == "calc" and not self.calculatrice_permise()[0]:
            self.locky_overlay.regler_mode("avatar")
            self.locky_signal("calc_interdite")
        self.locky_overlay.pousser(self.locky_donnees())
        self._rangs_tick()                                  # promotion ? (en attente pendant un examen)
        inactif = time.time() - self._locky_t_activite
        seuil = 25 if self.locky_cfg.get("freq") == "bavard" else 45
        if inactif > seuil and time.time() - self._locky_t_idle > 60:
            self._locky_t_idle = time.time()
            if self._locky_ctx in core.CTX_QUESTION:
                self.locky_signal("idle_question")
            elif self._locky_ctx == "menu":
                self.locky_signal("idle_menu")

    # ------------------------------------------------------------ données pour le menu
    def locky_donnees(self):
        a = core.analyser(getattr(self, "stats_chapitres", {}))
        ok, raison = self.calculatrice_permise()
        meilleur = max([self.meilleur_rp, self.points_de_rang] + [int(x) for x in (self.historique_scores or [0])])
        if meilleur != self.meilleur_rp:
            self.meilleur_rp = meilleur
        return {"nom": self.nom_mascotte, "niveau": self.niveau_mascotte, "pts": self.points_connexion,
                "jours": self.jours_connectes, "rp": self.points_de_rang, "rp_best": meilleur,
                "note_best": self.meilleure_note_examen, "total": a["total"], "reussite": a["reussite"],
                "echec": a["echec"], "forts": a["forts"], "faibles": a["faibles"],
                "cfg": self.locky_cfg, "calc": {"ok": ok, "raison": raison}, "audio": self.audio_etat(), "version": self.VERSION_APP, "rangs": self.rangs_payload(),
                "compte": {"connecte": bool(getattr(self, "jeton_compte", "")), "nom": getattr(self, "nom_utilisateur", ""),
                           "email": getattr(self, "email_utilisateur", ""), "ile": getattr(self, "ile_utilisateur", ""),
                           "ident": getattr(self, "identifiant_joueur", ""), "hors_ligne": bool(getattr(self, "compte_hors_ligne", False))}}

    # ------------------------------------------------------------ actions (appelées par le Locky Kivy ou la surcouche)
    def locky_tap(self):
        self.locky_ouvrir_menu()

    def locky_ouvrir_menu(self):
        if self.locky_overlay.pret:
            self.locky_overlay.pousser(self.locky_donnees())
            self.locky_overlay.regler_mode("menu")
        else:
            self._locky_menu_kivy()

    def locky_ouvrir_calculatrice(self):
        ok, raison = self.calculatrice_permise()
        if not ok:
            self.locky_signal("calc_interdite")
            if self.locky_overlay.pret:
                self.locky_overlay.regler_mode("avatar")
            self.toast(raison) if hasattr(self, "toast") else None
            return
        if self.locky_overlay.pret:
            self.locky_overlay.regler_mode("calc")
        else:
            self._locky_calc_kivy()

    def locky_placer(self, coin, anime=True):
        """coin : 'hg' 'hd' 'bg' 'bd' (haut/bas + gauche/droite)."""
        m = self.mascotte
        mg = dp(8)
        x = mg if coin[1] == "g" else Window.width - m.width - mg
        y = (Window.height - m.height - dp(70)) if coin[0] == "h" else dp(70)
        if anime:
            Animation(x=x, y=y, duration=0.25, t="out_quad").start(m)
        else:
            m.pos = (x, y)

    def locky_evenement(self, e):
        a = e.get("a")
        if a == "pret":
            self.locky_overlay.dire(self.mascotte.bulle_label.text)
        elif a in ("p", "lien", "audio"):
            self.param_evenement(e)
        elif a in ("rang_fin", "evo", "evo_cfg"):
            self.rangs_evenement(e)
        elif a == "drag":
            self.locky_overlay.drag(e)
        elif a == "tap":
            self.locky_tap()
        elif a == "dbl":
            self.mascotte.declencher_excitation()
        elif a == "fermer":
            if not self.pages_reprendre():
                self.locky_overlay.regler_mode("avatar")
        elif a == "pg":
            self.pages_evenement(e)
        elif a == "calc":
            self.locky_ouvrir_calculatrice()
        elif a == "coin":
            m = self.mascotte
            dx, dy = float(e.get("dx", 0)), float(e.get("dy", 0))
            gauche = dx < -36 or (abs(dx) <= 36 and m.center_x < Window.width / 2)
            haut = dy < -36 or (abs(dy) <= 36 and m.center_y > Window.height / 2)       # dy < 0 : glissé vers le haut
            coin = ("h" if haut else "b") + ("g" if gauche else "d")
            self.locky_cfg["coin"] = coin
            self.locky_placer(coin)
            self.sauvegarder_donnees_locales()
        elif a == "cfg":
            k, v = e.get("k"), e.get("v")
            if k in ("messages", "freq", "coin"):
                self.locky_cfg[k] = v
                if k == "coin" and v:
                    self.locky_placer(v)
                if k == "messages" and not v:
                    self.mascotte.bulle_label.text = ""
                self.sauvegarder_donnees_locales()
            self.locky_overlay.pousser(self.locky_donnees())

    # ------------------------------------------------------------ secours PC : menu et calculatrice Kivy
    def _locky_menu_kivy(self):
        d = self.locky_donnees()
        L = [f"[b][color=ffb000]LOCKY  ·  NIVEAU {d['niveau']}[/color][/b]",
             f"Connexions : {d['pts']}/7 point(s) avant le niveau suivant",
             f"Jours connectés : {d['jours']}", ""]
        if d["total"]:
            L += [f"[b]Analyse[/b]  réussite [color=39ff88]{d['reussite']}%[/color]  ·  échec [color=ff3b5c]{d['echec']}%[/color]  ({d['total']} réponses)"]
        else:
            L += ["[b]Analyse[/b]  pas encore de réponses"]
        L += ["Points forts : " + (", ".join(f"{c} ({p}%)" for c, p in d["forts"]) or "—"),
              "Points faibles : " + (", ".join(f"{c} ({p}%)" for c, p in d["faibles"]) or "—"), "",
              f"Meilleur score RP : {d['rp_best']}",
              "Meilleure note examen : " + ("—" if d["note_best"] is None else f"{d['note_best']}/20")]
        boite = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(10))
        lab = Label(text="\n".join(L), markup=True, halign="left", valign="top", color=(0.9, 0.95, 1, 1))
        lab.bind(size=lambda i, s: setattr(i, "text_size", (s[0], None)))
        boite.add_widget(lab)
        b_calc = Button(text="Calculatrice" if d["calc"]["ok"] else "Calculatrice (interdite)", size_hint_y=None, height=dp(48),
                        background_color=(0.1, 0.6, 0.9, 1) if d["calc"]["ok"] else (0.3, 0.3, 0.3, 1))
        b_fermer = Button(text="Fermer", size_hint_y=None, height=dp(44), background_color=(0.75, 0.2, 0.2, 1))
        boite.add_widget(b_calc)
        boite.add_widget(b_fermer)
        pop = Popup(title="Locky — profil", content=boite, size_hint=(0.92, 0.85), separator_color=(1, 0.69, 0, 1))
        b_fermer.bind(on_release=lambda *_: pop.dismiss())
        b_calc.bind(on_release=lambda *_: (pop.dismiss(), self.locky_ouvrir_calculatrice()))
        pop.open()

    def _locky_calc_kivy(self):
        etat = {"ans": 0.0, "mode": "DEG"}
        boite = BoxLayout(orientation="vertical", spacing=dp(4), padding=dp(6))
        champ = TextInput(multiline=False, size_hint_y=None, height=dp(46), font_size="20sp", halign="right")
        res = Label(text="0", size_hint_y=None, height=dp(40), font_size="24sp", bold=True, color=(0.2, 1, 0.5, 1))
        boite.add_widget(champ)
        boite.add_widget(res)

        def calculer(*_):
            try:
                v = core.calcul_python(champ.text, etat["mode"], etat["ans"])
                etat["ans"] = v
                res.color = (0.2, 1, 0.5, 1)
                res.text = core.formater(v)
            except ValueError as e:
                res.color = (1, 0.3, 0.4, 1)
                res.text = str(e)

        def ajouter(t):
            champ.text += t

        grille = GridLayout(cols=6, spacing=dp(4))
        touches = [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("ln", "ln("), ("log", "log("), ("√", "sqrt("),
                   ("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), ("(", "("), (")", ")"),
                   ("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"), ("^", "^"), ("π", "pi"),
                   ("1", "1"), ("2", "2"), ("3", "3"), ("-", "-"), ("x²", "^2"), ("ans", "ans"),
                   ("0", "0"), (".", "."), ("e", "e"), ("+", "+"), ("C", None), ("=", "=")]
        for lib, ins in touches:
            b = Button(text=lib, font_size="16sp")
            if lib == "C":
                b.bind(on_release=lambda *_: (setattr(champ, "text", ""), setattr(res, "text", "0")))
            elif lib == "=":
                b.bind(on_release=calculer)
            else:
                b.bind(on_release=lambda _i, t=ins: ajouter(t))
            grille.add_widget(b)
        boite.add_widget(grille)
        b_mode = Button(text="DEG", size_hint_y=None, height=dp(40))

        def basculer(*_):
            etat["mode"] = {"DEG": "RAD", "RAD": "GRAD", "GRAD": "DEG"}[etat["mode"]]
            b_mode.text = etat["mode"]
        b_mode.bind(on_release=basculer)
        b_f = Button(text="Fermer (la session continue)", size_hint_y=None, height=dp(44), background_color=(0.75, 0.2, 0.2, 1))
        boite.add_widget(b_mode)
        boite.add_widget(b_f)
        pop = Popup(title="Calculatrice", content=boite, size_hint=(0.95, 0.9))
        b_f.bind(on_release=lambda *_: pop.dismiss())
        pop.open()
