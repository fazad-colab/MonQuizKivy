# -*- coding: utf-8 -*-
"""
parametres_ui.py — Paramètres par catégories (page HTML « dark web » de la surcouche de Locky) + actions.

 * Mon compte : connexion / déconnexion, consulter mes données, informations personnelles
   (nom, classe, âge, sexe, île, e-mail, mot de passe), suppression des données
 * Réglages audio : musique, volumes, sons d'interaction, piste suivante, mode silencieux
 * Rester connecté au Développeur : liens directs (WhatsApp, YouTube, GitHub, Facebook, site, Google)
 * À propos & Version : confidentialité, conditions, développeur, licence (texte dans param_page.py)
 * Icônes ⚙ et menu IA : plaque néon bien visible, placées dans l'en-tête
"""
import webbrowser

from kivy.clock import Clock
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from en_ligne import AMBRE, CYAN, PANEL2, ROUGE, VERT, SoundManager, bouton, champ, etiquette

VERSION_APP = "Version Bêta (testeurs)"      # ← à modifier à chaque publication

# Seules ces adresses peuvent être ouvertes depuis la page (la page envoie une clé, jamais une URL).
LIENS = {
    "communaute": "https://chat.whatsapp.com/FlcaUC6BTroDBzZ3ZujlVx",
    "google": "https://www.google.com/search?q=Omnimath",
    "youtube": "https://www.youtube.com/@Omnimath.14",
    "github": "https://github.com/fazad-colab/MonQuizKivy",
    "facebook": "https://www.facebook.com/profile.php?id=61595888940618",
    "site": "https://fazad-colab.github.io/Omnimath.dev/",
}


class FonctionsParametres:
    VERSION_APP = VERSION_APP

    # ================================================================= audio
    def audio_etat(self):
        return {"musique": bool(getattr(self, "musique_active", True)),
                "vol": int(round(getattr(self, "volume_musique", 0.5) * 100)),
                "sons": bool(SoundManager.actif),
                "vol_fx": int(round(getattr(SoundManager, "volume_fx", 1.0) * 100)),
                "muet": bool(getattr(self, "audio_muet", False))}

    def audio_cfg_vers_dict(self):
        if not getattr(self, "_audio_applique", False) and getattr(self, "_audio_cfg", None):
            return dict(self._audio_cfg)                    # lecteur pas encore démarré : on garde ce qui a été chargé
        return {"musique": bool(getattr(self, "musique_active", True)),
                "vol": float(getattr(self, "volume_musique", 0.5)),
                "vol_fx": float(getattr(SoundManager, "volume_fx", 1.0))}

    def audio_cfg_depuis_dict(self, d):
        self._audio_cfg = d if isinstance(d, dict) else {}
        SoundManager.volume_fx = float(self._audio_cfg.get("vol_fx", 1.0))

    def audio_appliquer_sauvegarde(self):
        """À appeler quand le lecteur de musique est démarré : réapplique les réglages enregistrés."""
        c = getattr(self, "_audio_cfg", None) or {}
        self._audio_applique = True
        if "vol" in c:
            self.changer_volume(None, float(c["vol"]))
        if c.get("musique") is False:
            self._audio_musique(False)

    def _audio_musique(self, actif):
        self.musique_active = bool(actif)
        snd = getattr(self, "sound", None)
        if actif:
            if snd:
                snd.play()
            else:
                self.jouer_musique_suivante()
        elif snd:
            snd.stop()

    def param_audio(self, k, v):
        if k == "musique":
            self._audio_musique(bool(v))
            if v:
                self.audio_muet = False
        elif k == "vol":
            self.changer_volume(None, max(0.0, min(1.0, float(v) / 100.0)))
        elif k == "sons":
            SoundManager.actif = bool(v)
            self._sauver_prefs_reseau()
            if v:
                self.audio_muet = False
                SoundManager.play("clic", 0.5)
        elif k == "vol_fx":
            SoundManager.volume_fx = max(0.0, min(1.0, float(v) / 100.0))
        elif k == "suivante":
            self.musique_active = True
            self.audio_muet = False
            self.jouer_musique_suivante()
        elif k == "muet":
            if v:
                self._avant_muet = (bool(getattr(self, "musique_active", True)), bool(SoundManager.actif))
                self._audio_musique(False)
                SoundManager.actif = False
            else:
                m, s = getattr(self, "_avant_muet", (True, True))
                self._audio_musique(m)
                SoundManager.actif = s
            self.audio_muet = bool(v)
            self._sauver_prefs_reseau()
        self.sauvegarder_donnees_locales()

    # ================================================================= ouverture des paramètres
    def ouvrir_menu_parametres(self, instance=None):
        """Nouvelle page de paramètres (surcouche) ; l'ancien menu Kivy sert de secours (PC / surcouche indisponible)."""
        ov = getattr(self, "locky_overlay", None)
        if ov is not None and ov.pret:
            self.fermer_menu_parametres(None)              # purge d'un ancien écran Kivy resté ouvert
            self.locky_signal("parametres")
            ov.pousser(self.locky_donnees())
            ov.regler_mode("param")
        else:
            self.ouvrir_menu_parametres_legacy(instance)

    # ================================================================= événements venant de la page
    def param_evenement(self, e):
        a = e.get("a")
        if a == "audio":
            self.param_audio(e.get("k"), e.get("v"))
            self.locky_overlay.pousser(self.locky_donnees())
        elif a == "lien":
            url = LIENS.get(e.get("k"))
            if url:
                try:
                    webbrowser.open(url)
                except Exception:
                    self.toast("Impossible d'ouvrir le lien")
        elif a == "p":
            self.param_action(e.get("k"))

    def param_action(self, k):
        ov = self.locky_overlay
        if k == "locky":
            ov.pousser(self.locky_donnees())
            ov.regler_mode("menu")
            return
        ov.regler_mode("avatar")                          # on ferme la page, puis on ouvre l'écran demandé
        actions = {
            "compte": lambda: self.afficher_mon_compte(),
            "donnees": lambda: (self.ouvrir_menu_parametres_legacy(None), self.afficher_donnees_utilisateur(None)),
            "infos": lambda: self.afficher_infos_perso(),
            "copier_id": lambda: self.copier_identifiant(),
            "suppr_ligne": lambda: self.supprimer_mes_donnees_en_ligne(),
            "suppr_local": lambda: self.confirmer_effacement_local(),
            "serveur": lambda: self.afficher_reglage_serveur(),
            "internet": lambda: self.ouvrir_reglages_internet(),
            "aide": lambda: self.afficher_popup_aide(),
        }
        f = actions.get(k)
        if f:
            Clock.schedule_once(lambda dt: f(), 0.05)

    def _retour_parametres(self):
        self.afficher_menu_principal_modes()
        Clock.schedule_once(lambda dt: self.ouvrir_menu_parametres(), 0.25)

    # ================================================================= informations personnelles
    def afficher_infos_perso(self):
        self._ecran("Informations personnelles", "Choisis ce que tu veux modifier.", 0.14)
        L = self.interaction_layout
        L.add_widget(bouton("Nom, classe, âge, sexe", PANEL2, lambda: self.afficher_formulaire_modification_infos(None), neon=AMBRE))
        L.add_widget(bouton("Île de résidence", PANEL2, lambda: self._si_compte(self.afficher_modifier_ile), neon=CYAN))
        L.add_widget(bouton("Adresse e-mail", PANEL2, lambda: self._si_compte(self.afficher_modifier_email), neon=CYAN))
        L.add_widget(bouton("Mot de passe", PANEL2, lambda: self._si_compte(self.afficher_modifier_mdp), neon=CYAN))
        L.add_widget(bouton("« Retour aux paramètres", ROUGE, self._retour_parametres, h=48, neon=ROUGE))
        self._fixer_hauteur()

    def _si_compte(self, f):
        if not getattr(self, "jeton_compte", ""):
            self.toast("Connecte-toi à un compte pour modifier cette information")
            return
        f()

    def _ecran_formulaire(self, titre, texte):
        self._ecran(titre, texte, 0.2)
        return self.interaction_layout, etiquette("", taille="14sp")

    def afficher_modifier_mdp(self):
        L, msg = self._ecran_formulaire("Changer le mot de passe", "Saisis ton mot de passe actuel puis le nouveau.")
        f_old = self._champ_mdp("Mot de passe actuel")
        f_new = self._champ_mdp("Nouveau mot de passe (6 caractères minimum)")
        f_new2 = self._champ_mdp("Confirmer le nouveau mot de passe")
        for w in (f_old, f_new, f_new2):
            L.add_widget(w)
        L.add_widget(self._bouton_voir_mdp(f_old, f_new, f_new2))
        L.add_widget(msg)

        def valider():
            if not f_old.text:
                return self._message(msg, "Saisis ton mot de passe actuel.")
            if len(f_new.text) < 6:
                return self._message(msg, "Le nouveau mot de passe doit contenir au moins 6 caractères.")
            if f_new.text != f_new2.text:
                return self._message(msg, "Les deux nouveaux mots de passe sont différents.")
            if f_new.text == f_old.text:
                return self._message(msg, "Le nouveau mot de passe doit être différent de l'ancien.")

            def succes(res):
                self.toast("Mot de passe modifié")
                self.afficher_infos_perso()
            self._envoyer_compte("/api/compte/mot_de_passe", {"ancien": f_old.text, "nouveau": f_new.text}, msg, succes)
        L.add_widget(bouton("Enregistrer le mot de passe", VERT, valider, h=54, font="18sp", neon=VERT))
        L.add_widget(bouton("« Retour", ROUGE, self.afficher_infos_perso, h=48, neon=ROUGE))
        self._fixer_hauteur()

    def afficher_modifier_email(self):
        L, msg = self._ecran_formulaire("Changer l'e-mail", f"E-mail actuel : {self.email_utilisateur or '—'}\n"
                                        "Un code de vérification sera envoyé à la nouvelle adresse.")
        f_mail = champ("Nouvelle adresse e-mail")
        f_mail.input_type = "mail"
        f_mdp = self._champ_mdp("Mot de passe actuel")
        L.add_widget(f_mail)
        L.add_widget(f_mdp)
        L.add_widget(self._bouton_voir_mdp(f_mdp))
        L.add_widget(msg)

        def valider():
            from comptes_ui import RE_EMAIL
            mail = f_mail.text.strip().lower()
            if not RE_EMAIL.match(mail):
                return self._message(msg, "Adresse e-mail invalide.")
            if not f_mdp.text:
                return self._message(msg, "Saisis ton mot de passe actuel.")

            def succes(res):
                self.email_utilisateur = mail
                self.sauvegarder_donnees_locales()
                self._jeton_attente = self.jeton_compte
                if not res.get("email_envoye"):
                    self.toast("Envoi d'e-mails indisponible pour l'instant : redemande le code plus tard")
                self.afficher_verification_email(obligatoire=False, nouveau=False)
            self._envoyer_compte("/api/compte/email", {"email": mail, "mot_de_passe": f_mdp.text}, msg, succes)
        L.add_widget(bouton("Changer l'e-mail", VERT, valider, h=54, font="18sp", neon=VERT))
        L.add_widget(bouton("« Retour", ROUGE, self.afficher_infos_perso, h=48, neon=ROUGE))
        self._fixer_hauteur()

    def afficher_modifier_ile(self):
        L, msg = self._ecran_formulaire("Changer l'île", f"Île actuelle : {self.ile_utilisateur or '—'}")
        etat = {"ile": self.ile_utilisateur}
        L.add_widget(self._selecteur_ile(etat))
        L.add_widget(msg)

        def valider():
            if not etat.get("ile"):
                return self._message(msg, "Choisis une île.")

            def succes(res):
                self.ile_utilisateur = etat["ile"]
                self.sauvegarder_donnees_locales()
                self.toast("Île modifiée")
                self.afficher_infos_perso()
            self._envoyer_compte("/api/compte/ile", {"ile": etat["ile"]}, msg, succes)
        L.add_widget(bouton("Enregistrer l'île", VERT, valider, h=54, font="18sp", neon=VERT))
        L.add_widget(bouton("« Retour", ROUGE, self.afficher_infos_perso, h=48, neon=ROUGE))
        self._fixer_hauteur()

    # ================================================================= effacer la progression locale
    def confirmer_effacement_local(self):
        c = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        c.add_widget(etiquette("Remettre à zéro tes points de rang, ton XP, tes statistiques, ton historique et tes records ?\n"
                               "Si tu es connecté, la remise à zéro est aussi envoyée à ton compte lors de la prochaine "
                               "synchronisation. Cette action est irréversible.", taille="14sp"))
        p = self._popup("Effacer ma progression", c, (0.9, 0.62))

        def go():
            p.dismiss()
            self.points_de_rang = 0
            self.xp = 0
            self.niveau_profil = 1
            self.historique_scores = []
            for k in list(self.stats_chapitres):
                self.stats_chapitres[k] = [0, 0]
            self.meilleur_rp = 0
            self.meilleure_note_examen = None
            self.notes_examen = []
            self.rangs_resync()
            self.sauvegarder_donnees_locales()
            self.toast("Progression effacée")
        c.add_widget(bouton("Oui, tout effacer", ROUGE, go, neon=ROUGE))
        c.add_widget(bouton("Annuler", PANEL2, p.dismiss))
        p.open()

    # ================================================================= icônes ⚙ et IA bien visibles
    def habiller_icone_neon(self, btn, couleur=(0.0, 0.94, 1.0, 1.0), taille=46):
        """Plaque sombre-cyan + contour néon derrière l'icône (visible sur fond sombre comme clair)."""
        btn.size_hint = (None, None)
        btn.size = (dp(taille), dp(taille))
        btn.background_color = (1, 1, 1, 1)
        fond_c = Color(0.04, 0.32, 0.42, 0.96)
        fond = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(12)])
        btn.canvas.before.insert(0, fond)
        btn.canvas.before.insert(0, fond_c)
        with btn.canvas.after:
            Color(*couleur)
            ligne = Line(rounded_rectangle=(btn.x, btn.y, btn.width, btn.height, dp(12)), width=dp(1.5))

        def maj(i, *_):
            fond.pos, fond.size = i.pos, i.size
            ligne.rounded_rectangle = (i.x, i.y, i.width, i.height, dp(12))
        btn.bind(pos=maj, size=maj)

    def creer_icone_ia(self, callback):
        btn = Button(background_normal="icone_appli/menu.png", background_down="icone_appli/menu.png")
        self.habiller_icone_neon(btn, couleur=(1.0, 0.17, 0.84, 1.0))
        btn.bind(on_press=callback)
        return btn
