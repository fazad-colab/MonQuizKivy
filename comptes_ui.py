# -*- coding: utf-8 -*-
"""
comptes_ui.py — création / récupération de compte (mixin pour FixedDynamicQuizApp)

Première ouverture de l'application :
    * « Créer mon compte »     : nom, île de résidence, e-mail de vérification, mot de passe
    * « J'ai déjà un compte »  : nom, identifiant, mot de passe, e-mail de vérification, île
    * « Continuer hors-ligne » : ancien fonctionnement (prénom seul, aucune fonction en ligne)

Tout est contrôlé par le serveur Flask (flask_app.py) : le mot de passe n'est jamais stocké en clair,
l'application ne garde qu'un jeton de session, et chaque appel suivant est authentifié par ce jeton.
"""
import re

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from en_ligne import (AMBRE, CYAN, PANEL2, ROUGE, VERT, bouton, champ, etiquette)

RE_EMAIL = re.compile(r"^[A-Za-z0-9._%+\-]{1,64}@[A-Za-z0-9.\-]{1,190}\.[A-Za-z]{2,24}$")

# (valeur envoyée au serveur, libellé affiché) — doit rester identique à ILES dans flask_app.py
ILES = (
    ("Ngazidja", "Grande Comore (Ngazidja)"),
    ("Ndzuani", "Anjouan (Ndzuani)"),
    ("Mwali", "Mohéli (Mwali)"),
    ("Maore", "Mayotte (Maore)"),
    ("Autre", "Autre (hors des Comores)"),
)


class FonctionsComptes:

    # ------------------------------------------------------------------ état
    def init_comptes(self):
        self.jeton_compte = getattr(self, "jeton_compte", "")
        self.ile_utilisateur = getattr(self, "ile_utilisateur", "")
        self.email_utilisateur = getattr(self, "email_utilisateur", "")
        self.compte_hors_ligne = getattr(self, "compte_hors_ligne", False)
        self._jeton_attente = ""
        self._requete_compte = False

    def compte_requis(self):
        """True si l'écran de compte doit s'afficher : aucun nom enregistré, ou profil jamais relié à un compte."""
        if not getattr(self, "nom_utilisateur", ""):
            return True
        return not self.jeton_compte and not self.compte_hors_ligne

    # --------------------------------------------------------------- accueil
    def demander_nom_utilisateur(self):
        """Remplace l'ancienne saisie du prénom : choix créer / récupérer un compte."""
        self.afficher_accueil_compte()

    def afficher_accueil_compte(self, instance=None):
        migration = bool(getattr(self, "nom_utilisateur", ""))
        self._ecran(
            "Math Quiz Comores",
            ("Ton profil n'est pas encore relié à un compte sécurisé.\nCrée-en un pour sauvegarder ta progression "
             "et jouer en ligne, ou retrouve ton compte existant.") if migration else
            ("Bienvenue sur Math Quiz Comores !\n\nCrée ton compte pour sauvegarder ta progression et jouer en ligne, "
             "ou retrouve ton compte existant."),
            0.30)
        L = self.interaction_layout
        L.add_widget(bouton("Créer mon compte", VERT, self.afficher_formulaire_inscription, h=56, font="19sp", neon=VERT))
        L.add_widget(bouton("J'ai déjà un compte", PANEL2, self.afficher_formulaire_connexion, h=56, font="19sp"))
        L.add_widget(bouton("Continuer hors-ligne (sans compte)", PANEL2, self._continuer_hors_ligne, h=50, font="15sp", neon=AMBRE))
        self._fixer_hauteur()

    def _continuer_hors_ligne(self):
        self.compte_hors_ligne = True
        self.sauvegarder_donnees_locales()
        if getattr(self, "nom_utilisateur", ""):
            self.afficher_menu_principal_modes()
        else:
            self.demander_nom_utilisateur_hors_ligne()

    # ------------------------------------------------------- éléments communs
    def _champ_mdp(self, hint):
        c = champ(hint)
        c.password = True
        return c

    def _bouton_voir_mdp(self, *champs):
        def basculer():
            voir = not champs[0].password
            for c in champs:
                c.password = voir
        return bouton("Afficher / masquer le mot de passe", PANEL2, basculer, h=40, font="13sp")

    def _selecteur_ile(self, etat):
        """Cinq boutons-îles ; la sélection est mémorisée dans etat['ile']."""
        boite = GridLayout(cols=2, size_hint=(1, None), spacing=dp(6))
        boite.height = dp(46 + 6) * 3

        def dessiner():
            boite.clear_widgets()
            for valeur, libelle in ILES:
                choisi = etat.get("ile") == valeur
                boite.add_widget(bouton(libelle, VERT if choisi else PANEL2, lambda v=valeur: choisir(v), h=46, font="13sp",
                                        neon=VERT if choisi else CYAN))

        def choisir(valeur):
            etat["ile"] = valeur
            dessiner()
        dessiner()
        return boite

    def _message(self, lbl, texte, erreur=True):
        lbl.color = (1, 0.45, 0.5, 1) if erreur else (0.4, 1, 0.6, 1)
        lbl.text = texte

    def _envoyer_compte(self, chemin, corps, lbl, succes, timeout=15):
        """Appel serveur protégé contre le double clic."""
        if self._requete_compte:
            return
        if not getattr(self, "en_ligne", False):
            self._message(lbl, "Pas de connexion Internet : active-la pour créer ou récupérer ton compte.")
            return
        self._requete_compte = True
        self._message(lbl, "Connexion au serveur…", erreur=False)

        def fini():
            self._requete_compte = False

        def ok(res):
            fini()
            succes(res)

        def err(msg):
            fini()
            self._message(lbl, str(msg))
        self.api(chemin, corps, ok=ok, err=err, timeout=timeout)

    # ----------------------------------------------------------- inscription
    def afficher_formulaire_inscription(self):
        self._ecran("Créer mon compte", "Tous les champs sont obligatoires.", 0.10)
        L = self.interaction_layout
        etat = {"ile": ""}
        f_nom = champ("Ton nom")
        f_mail = champ("E-mail de vérification")
        f_mail.input_type = "mail"
        f_mdp = self._champ_mdp("Mot de passe (6 caractères minimum)")
        f_mdp2 = self._champ_mdp("Confirme le mot de passe")
        msg = etiquette("", taille="14sp")
        L.add_widget(f_nom)
        L.add_widget(etiquette("Île de résidence :", taille="14sp", align="left"))
        L.add_widget(self._selecteur_ile(etat))
        L.add_widget(f_mail)
        L.add_widget(f_mdp)
        L.add_widget(f_mdp2)
        L.add_widget(self._bouton_voir_mdp(f_mdp, f_mdp2))
        L.add_widget(etiquette("En créant un compte, tu acceptes que ton profil (nom, île, e-mail, progression) soit "
                               "enregistré sur le serveur Math Quiz Comores.", taille="12sp", couleur=(0.65, 0.68, 0.85, 1)))
        L.add_widget(msg)

        def valider():
            nom = " ".join(f_nom.text.split())
            mail = f_mail.text.strip().lower()
            if len(nom) < 2:
                return self._message(msg, "Entre ton nom (2 caractères minimum).")
            if not etat["ile"]:
                return self._message(msg, "Choisis ton île de résidence.")
            if not RE_EMAIL.match(mail):
                return self._message(msg, "Adresse e-mail invalide.")
            if len(f_mdp.text) < 6:
                return self._message(msg, "Le mot de passe doit contenir au moins 6 caractères.")
            if f_mdp.text != f_mdp2.text:
                return self._message(msg, "Les deux mots de passe sont différents.")

            def succes(res):
                self.consentement = True                  # l'information est donnée juste au-dessus
                self._sauver_prefs_reseau()
                self._jeton_attente = res["jeton"]
                self.identifiant_joueur = res["identifiant"]
                self.nom_utilisateur, self.ile_utilisateur, self.email_utilisateur = nom, etat["ile"], mail
                if res.get("verification_requise") or res.get("email_envoye"):
                    self.afficher_verification_email(obligatoire=bool(res.get("verification_requise")), nouveau=True)
                else:
                    self._adopter_jeton({"identifiant": res["identifiant"], "nom": nom, "ile": etat["ile"], "email": mail},
                                        nouveau=True)
                    self.toast("Compte créé (la vérification e-mail n'est pas disponible pour l'instant)", 3.0)
            self._envoyer_compte("/api/inscription", {"nom": nom, "ile": etat["ile"], "email": mail,
                                                      "mot_de_passe": f_mdp.text}, msg, succes)

        L.add_widget(bouton("Créer mon compte", VERT, valider, h=54, font="18sp", neon=VERT))
        L.add_widget(bouton("« Retour", ROUGE, self.afficher_accueil_compte, h=48, neon=ROUGE))
        self._fixer_hauteur()

    # ------------------------------------------------------------- connexion
    def afficher_formulaire_connexion(self):
        self._ecran("Retrouver mon compte",
                    "Saisis exactement les informations de ton inscription.", 0.10)
        L = self.interaction_layout
        etat = {"ile": ""}
        f_nom = champ("Ton nom")
        f_id = champ("Ton identifiant (ex. id123456)")
        f_mdp = self._champ_mdp("Ton mot de passe")
        f_mail = champ("E-mail de vérification")
        f_mail.input_type = "mail"
        msg = etiquette("", taille="14sp")
        L.add_widget(f_nom)
        L.add_widget(f_id)
        L.add_widget(f_mdp)
        L.add_widget(self._bouton_voir_mdp(f_mdp))
        L.add_widget(f_mail)
        L.add_widget(etiquette("Île de résidence :", taille="14sp", align="left"))
        L.add_widget(self._selecteur_ile(etat))
        L.add_widget(msg)

        def valider():
            nom = " ".join(f_nom.text.split())
            ident = f_id.text.strip().lower()
            mail = f_mail.text.strip().lower()
            if len(nom) < 2 or not ident or not f_mdp.text:
                return self._message(msg, "Remplis le nom, l'identifiant et le mot de passe.")
            if not RE_EMAIL.match(mail):
                return self._message(msg, "Adresse e-mail invalide.")
            if not etat["ile"]:
                return self._message(msg, "Choisis ton île de résidence.")

            def succes(res):
                if res.get("connecte"):
                    self._jeton_attente = res["jeton"]
                    self._adopter_jeton(res["compte"], nouveau=False)
                else:                                       # e-mail pas encore vérifié
                    self._jeton_attente = res["jeton"]
                    self.afficher_verification_email(obligatoire=True, nouveau=False)
            self._envoyer_compte("/api/connexion", {"nom": nom, "identifiant": ident, "mot_de_passe": f_mdp.text,
                                                    "email": mail, "ile": etat["ile"]}, msg, succes)

        L.add_widget(bouton("Me connecter", VERT, valider, h=54, font="18sp", neon=VERT))
        L.add_widget(bouton("« Retour", ROUGE, self.afficher_accueil_compte, h=48, neon=ROUGE))
        self._fixer_hauteur()

    # ------------------------------------------------------ vérification e-mail
    def afficher_verification_email(self, obligatoire=True, nouveau=True):
        self._ecran("Vérification de l'e-mail",
                    "Un code à 6 chiffres vient d'être envoyé à ton adresse e-mail.\nSaisis-le ci-dessous "
                    "(pense à regarder dans les courriers indésirables).", 0.22)
        L = self.interaction_layout
        f_code = champ("Code à 6 chiffres")
        f_code.input_filter = "int"
        f_code.input_type = "number"
        msg = etiquette("", taille="14sp")
        L.add_widget(f_code)
        L.add_widget(msg)

        def valider():
            code = f_code.text.strip()
            if len(code) != 6:
                return self._message(msg, "Le code contient 6 chiffres.")
            if self._requete_compte:
                return
            self._requete_compte = True
            self._message(msg, "Vérification…", erreur=False)

            def ok(res):
                self._requete_compte = False
                self._adopter_jeton(res["compte"], nouveau=nouveau)

            def err(m):
                self._requete_compte = False
                self._message(msg, str(m))
            self.api("/api/verifier_email", {"code": code}, ok=ok, err=err, timeout=12, jeton=self._jeton_attente)

        def renvoyer():
            self.api("/api/renvoyer_code", {}, jeton=self._jeton_attente, timeout=12,
                     ok=lambda r: self._message(msg, "Nouveau code envoyé." if r.get("email_envoye")
                                                else "L'envoi d'e-mails est indisponible pour l'instant.", erreur=not r.get("email_envoye")),
                     err=lambda m: self._message(msg, str(m)))

        L.add_widget(bouton("Valider le code", VERT, valider, h=54, font="18sp", neon=VERT))
        L.add_widget(bouton("Renvoyer le code", PANEL2, renvoyer, h=46, font="15sp"))
        if not obligatoire:
            L.add_widget(bouton("Plus tard", PANEL2, lambda: self._adopter_jeton(
                {"identifiant": self.identifiant_joueur, "nom": self.nom_utilisateur, "ile": self.ile_utilisateur,
                 "email": self.email_utilisateur}, nouveau=nouveau), h=46, font="15sp", neon=AMBRE))
        L.add_widget(bouton("« Retour", ROUGE, self.afficher_accueil_compte, h=48, neon=ROUGE))
        self._fixer_hauteur()

    # ----------------------------------------- compte accepté : profil local mis à jour
    def _adopter_jeton(self, compte, nouveau):
        """Le serveur a validé le compte : on garde le jeton et on récupère le profil (connexion sur un autre téléphone)."""
        self.jeton_compte = self._jeton_attente
        self._jeton_attente = ""
        self.compte_hors_ligne = False
        self.identifiant_joueur = compte.get("identifiant", self.identifiant_joueur)
        self.nom_utilisateur = compte.get("nom") or self.nom_utilisateur
        self.ile_utilisateur = compte.get("ile") or self.ile_utilisateur
        self.email_utilisateur = compte.get("email") or self.email_utilisateur
        if not nouveau:                                    # on ne perd jamais de progression : on garde le meilleur des deux
            self.points_de_rang = max(int(self.points_de_rang or 0), int(compte.get("points_de_rang") or 0))
            self.xp = max(int(self.xp or 0), int(compte.get("xp") or 0))
            self.niveau_profil = max(int(self.niveau_profil or 1), int(compte.get("niveau_profil") or 1))
            self.niveau_mascotte = max(int(self.niveau_mascotte or 1), int(compte.get("niveau_mascotte") or 1))
            self.xp_mascotte = max(int(self.xp_mascotte or 0), int(compte.get("xp_mascotte") or 0))
            self.classe_utilisateur = self.classe_utilisateur or compte.get("classe") or ""
            self.niveau_utilisateur = self.niveau_utilisateur or compte.get("niveau") or ""
            self.sexe_utilisateur = self.sexe_utilisateur or compte.get("sexe") or ""
            self.age_utilisateur = self.age_utilisateur or compte.get("age") or ""
            for chap, v in (compte.get("stats_chapitres") or {}).items():
                loc = self.stats_chapitres.get(chap)
                if isinstance(v, (list, tuple)) and len(v) == 2 and (not loc or v[1] > loc[1]):
                    self.stats_chapitres[chap] = [v[0], v[1]]
        self.sauvegarder_donnees_locales()
        self.synchroniser_profil(force=True)
        if nouveau:
            self.afficher_popup_succes_identifiant(self.identifiant_joueur)
        else:
            self.toast(f"Bon retour {self.nom_utilisateur} !", 2.5)
            self.afficher_menu_principal_modes()

    # ------------------------------------------------------------- Mon compte
    def afficher_mon_compte(self, confirmer=False):
        self._ecran("Mon compte", "", 0.08)
        L = self.interaction_layout
        if self.jeton_compte:
            L.add_widget(etiquette(f"Nom : {self.nom_utilisateur}\nIdentifiant : {self.identifiant_joueur}\n"
                                   f"Île : {self.ile_utilisateur or '—'}\nE-mail : {self.email_utilisateur or '—'}",
                                   taille="16sp", align="left"))
            L.add_widget(bouton("Copier mon identifiant", PANEL2, self.copier_identifiant, h=48, font="15sp"))
            if confirmer:
                L.add_widget(etiquette("Ce téléphone sera vidé de ta progression (elle reste sur ton compte, "
                                       "sauf ce qui n'a pas encore été synchronisé).", taille="13sp", couleur=(1, 0.6, 0.4, 1)))
                L.add_widget(bouton("Confirmer la déconnexion", ROUGE, self._deconnecter, h=52, neon=ROUGE))
            else:
                L.add_widget(bouton("Se déconnecter", ROUGE, lambda: self.afficher_mon_compte(True), h=52, neon=ROUGE))
        else:
            L.add_widget(etiquette("Aucun compte relié : les fonctions en ligne (classement, salles, sauvegarde) sont désactivées.",
                                   taille="15sp"))
            L.add_widget(bouton("Créer / retrouver mon compte", VERT, self.afficher_accueil_compte, h=56, font="18sp", neon=VERT))
        L.add_widget(bouton("« Retour au menu", ROUGE, self.afficher_menu_principal_modes, h=48, neon=ROUGE))
        self._fixer_hauteur()

    def _deconnecter(self):
        self.api("/api/deconnexion", {}, timeout=6)            # le jeton est lu avant d'être effacé
        self.jeton_compte = ""
        self.compte_hors_ligne = False
        self.nom_utilisateur = self.identifiant_joueur = self.ile_utilisateur = self.email_utilisateur = ""
        self.classe_utilisateur = self.niveau_utilisateur = ""
        self.points_de_rang = self.xp = self.xp_mascotte = 0
        self.niveau_profil = self.niveau_mascotte = 1
        self.historique_scores = []
        for k in list(self.stats_chapitres):
            self.stats_chapitres[k] = [0, 0]
        self.sauvegarder_donnees_locales()
        self.afficher_accueil_compte()
