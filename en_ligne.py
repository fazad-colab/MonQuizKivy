# -*- coding: utf-8 -*-
"""
en_ligne.py — fonctions ajoutées à l'application Math Quiz Comores (mixin pour FixedDynamicQuizApp)

  * SonButton / SoundManager ........ sons d'interaction sur TOUS les boutons (dossier ./sons)
  * vérification permanente d'Internet + bandeau « Activer Internet » + popup au démarrage
  * copie de l'identifiant (en-tête, popup de création, paramètres)
  * consentement RGPD + synchronisation du profil (collecte des données utilisateurs)
  * module « Joueurs » : recherche par identifiant/nom, joueurs en ligne, classement, fiche détaillée
  * salles multijoueurs EN LIGNE (téléphones séparés, sans limite de joueurs)
  * MODE CLASSE : le professeur est l'hôte, personnalise la session, partage un code ;
    chaque élève voit la question + les propositions et répond ; seul le professeur voit les réponses ;
    à la fin le tableau des scores s'affiche chez tout le monde
  * réglage du serveur (internet ou Wi-Fi local de la classe)
"""
import json
import os
import time

from urllib.parse import quote

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as _KButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from android_math_webview import AndroidMathWebView
from latex_utils import latex_vers_texte
from moteur_quiz import PROGRESSION_OFFICIELLE, CLASSES

try:
    import certifi
    CA_FILE = certifi.where()
except Exception:  # pragma: no cover
    CA_FILE = None

DOSSIER = os.path.dirname(os.path.abspath(__file__))
URL_PAR_DEFAUT = "https://fazadnassur.pythonanywhere.com/"
LETTRES = "ABCDEFGH"

# ---------------------------------------------------------------- palette « dark web »
BG = (0.02, 0.02, 0.05, 1)
PANEL = (0.08, 0.06, 0.17, 1)
PANEL2 = (0.12, 0.08, 0.26, 1)
CYAN = (0.0, 0.94, 1.0, 1)
MAG = (1.0, 0.17, 0.84, 1)
VERT = (0.13, 0.80, 0.42, 1)
ROUGE = (0.80, 0.14, 0.24, 1)
AMBRE = (0.95, 0.65, 0.05, 1)


# =======================================
# Sons
# =======================================
class SoundManager:
    actif = True
    _cache = {}

    @staticmethod
    def play(nom, volume=0.7):
        if not SoundManager.actif:
            return
        try:
            s = SoundManager._cache.get(nom)
            if s is None:
                for ext in (".ogg", ".wav", ".mp3"):
                    chemin = os.path.join(DOSSIER, "sons", nom + ext)
                    if os.path.exists(chemin):
                        s = SoundLoader.load(chemin)
                        break
                SoundManager._cache[nom] = s or False
            if s:
                s.volume = volume
                s.stop()
                s.play()
        except Exception:
            pass


class Button(_KButton):
    """Remplace kivy.uix.button.Button dans main.py :
       - son de clic automatique sur chaque bouton
       - fin contour néon (thème « dark web ») sauf pour les boutons-icônes (image)"""

    def __init__(self, **kwargs):
        icone = bool(kwargs.get("background_normal"))
        super().__init__(**kwargs)
        if not icone:
            with self.canvas.after:
                Color(0.0, 0.94, 1.0, 0.45)
                self._neon = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(18)), width=dp(1))
            self.bind(pos=self._maj_neon, size=self._maj_neon)

    def _maj_neon(self, *args):
        self._neon.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(18))

    def on_press(self):
        SoundManager.play("clic", 0.5)


# =======================================
# Widgets utilitaires
# =======================================
def bouton(texte, couleur=PANEL2, cb=None, h=50, font="17sp", neon=CYAN):
    b = Button(text=texte, font_size=font, bold=True, size_hint=(1, None), height=dp(h), halign="center",
               valign="middle", background_normal="", background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
    b.bind(size=lambda i, v: setattr(i, "text_size", (v[0] - dp(14), v[1])))
    b.canvas.after.clear()
    with b.canvas.before:
        Color(0, 0, 0, 0.5)
        b._ombre = RoundedRectangle(pos=(b.x + dp(3), b.y - dp(3)), size=b.size, radius=[dp(16)])
        Color(*couleur)
        b._fond = RoundedRectangle(pos=b.pos, size=b.size, radius=[dp(16)])
        Color(neon[0], neon[1], neon[2], 0.85)
        b._ligne = Line(rounded_rectangle=(b.x, b.y, b.width, b.height, dp(16)), width=dp(1.1))

    def maj(i, *_):
        i._ombre.pos = (i.x + dp(3), i.y - dp(3))
        i._ombre.size = i.size
        i._fond.pos = i.pos
        i._fond.size = i.size
        i._ligne.rounded_rectangle = (i.x, i.y, i.width, i.height, dp(16))
    b.bind(pos=maj, size=maj)
    if cb:
        b.bind(on_release=lambda *_: cb())
    return b


def etiquette(texte, h=None, couleur=(0.9, 0.93, 1, 1), taille="15sp", gras=False, align="center", markup=False):
    lb = Label(text=texte, font_size=taille, bold=gras, color=couleur, halign=align, valign="middle",
               size_hint=(1, None), markup=markup)
    lb.bind(width=lambda i, w: setattr(i, "text_size", (w - dp(10), None)))
    if h:
        lb.height = dp(h)
    else:
        def _maj(i, t):
            i.height = t[1] + dp(8)
            Clock.schedule_once(lambda dt: _refit(i), 0)
        lb.bind(texture_size=_maj)
    return lb


def _refit(label):
    """Recalcule la hauteur de l'écran courant quand un label (sans hauteur fixe) change de taille."""
    app = App.get_running_app()
    if app is not None and hasattr(app, "_fixer_hauteur") and label in list(app.interaction_layout.walk()):
        app._fixer_hauteur(0)


def champ(hint, h=46, texte=""):
    return TextInput(hint_text=hint, text=texte, multiline=False, size_hint=(1, None), height=dp(h), font_size="18sp",
                     background_color=(0.1, 0.08, 0.2, 1), foreground_color=(1, 1, 1, 1),
                     hint_text_color=(0.55, 0.55, 0.75, 1), cursor_color=CYAN, padding=[dp(12), dp(12)])


# =======================================
# Mixin principal
# =======================================
class FonctionsEnLigne:

    # init
    def init_en_ligne(self):
        self.url_serveur = URL_PAR_DEFAUT
        self.consentement = None 
        self.en_ligne = None 
        self.salon = None
        self._poll_salon = None
        self._fichier_reseau = os.path.join(self.user_data_dir, "reseau.json")
        self._charger_prefs_reseau()
        SoundManager.actif = getattr(self, "_son_actif", True)

        # bandeau réseau (en haut)
        self.banner_reseau = BoxLayout(orientation="horizontal", size_hint=(1, None), height=0, opacity=0,
                                       spacing=dp(6), padding=[dp(6), 0])
        with self.banner_reseau.canvas.before:
            Color(0.55, 0.05, 0.12, 1)
            self._banner_fond = RoundedRectangle(pos=self.banner_reseau.pos, size=self.banner_reseau.size, radius=[dp(10)])
        self.banner_reseau.bind(pos=lambda i, v: setattr(self._banner_fond, "pos", v),
                                size=lambda i, v: setattr(self._banner_fond, "size", v))
        self.lbl_banner = Label(text="Pas de connexion Internet", font_size="14sp", bold=True, halign="left", valign="middle")
        self.lbl_banner.bind(size=lambda i, v: setattr(i, "text_size", v))
        self.btn_banner = Button(text="Activer Internet", font_size="13sp", bold=True, size_hint=(None, 1), width=dp(140),
                                 background_normal="", background_color=(0.0, 0.7, 0.8, 1))
        self.btn_banner.bind(on_release=lambda *_: self.ouvrir_reglages_internet())
        self.banner_reseau.add_widget(self.lbl_banner)
        self.banner_reseau.add_widget(self.btn_banner)
        self.main_layout.add_widget(self.banner_reseau, index=len(self.main_layout.children))

        # bouton « copier mon identifiant » dans l'en-tête --------------------
        self.btn_copy_id = Button(text="ID\ncopier", font_size="11sp", bold=True, size_hint=(None, None),
                                  size=(dp(52), dp(50)), background_normal="", background_color=(0.1, 0.5, 0.6, 1),
                                  halign="center")
        self.btn_copy_id.bind(on_release=lambda *_: self.copier_identifiant())
        self.info_layout.add_widget(self.btn_copy_id)

        Clock.schedule_once(lambda dt: self._ping_reseau(0), 0.5)
        Clock.schedule_interval(self._ping_reseau, 6.0)
        Clock.schedule_interval(lambda dt: self.synchroniser_profil(), 120.0)
        Clock.schedule_once(self._verifier_consentement, 3.0)

    # ------------------------------------------------------------ préférences
    def _charger_prefs_reseau(self):
        try:
            with open(self._fichier_reseau, "r", encoding="utf-8") as f:
                d = json.load(f)
            self.url_serveur = d.get("url_serveur", URL_PAR_DEFAUT) or URL_PAR_DEFAUT
            self.consentement = d.get("consentement", None)
            self._son_actif = d.get("son_actif", True)
        except Exception:
            pass

    def _sauver_prefs_reseau(self):
        try:
            with open(self._fichier_reseau, "w", encoding="utf-8") as f:
                json.dump({"url_serveur": self.url_serveur, "consentement": self.consentement,
                           "son_actif": SoundManager.actif}, f)
        except Exception:
            pass

    def basculer_sons(self):
        SoundManager.actif = not SoundManager.actif
        self._sauver_prefs_reseau()
        self.toast("Sons d'interaction " + ("activés" if SoundManager.actif else "coupés"))

    # --------------------------------------------------------------- réseau
    def url_api(self, chemin):
        return self.url_serveur.rstrip("/") + chemin

    def api(self, chemin, corps=None, ok=None, err=None, timeout=5):
        def _ok(req, res):
            if isinstance(res, (str, bytes)):
                try:
                    res = json.loads(res)
                except Exception:
                    res = {"status": "error", "message": "réponse illisible"}
            if isinstance(res, dict) and res.get("status") == "error":
                if err:
                    err(res.get("message", "erreur"))
                return
            if ok:
                ok(res)

        def _ko(req, e):
            msg = e.get("message", "erreur serveur") if isinstance(e, dict) else str(e)
            if err:
                err(msg)
        kw = dict(timeout=timeout, on_success=_ok, on_error=_ko, on_failure=_ko)
        if CA_FILE:
            kw["ca_file"] = CA_FILE
        if corps is not None:
            kw["req_body"] = json.dumps(corps)
            kw["req_headers"] = {"Content-Type": "application/json", "Accept": "application/json"}
        UrlRequest(self.url_api(chemin), **kw)

    def _ping_reseau(self, dt):
        ident = getattr(self, "identifiant_joueur", "") or ""
        self.api("/api/ping" + (f"?id={ident}" if ident else ""), ok=lambda r: self._maj_reseau(True),
                 err=lambda m: self._maj_reseau(False), timeout=4)

    def _maj_reseau(self, connecte):
        avant = self.en_ligne
        self.en_ligne = connecte
        if avant == connecte:
            return
        if connecte:
            self._montrer_banner(False)
            if avant is False:
                SoundManager.play("connexion")
                self.toast("Connexion rétablie")
            self.synchroniser_profil(force=True)
        else:
            self._montrer_banner(True)
            SoundManager.play("deconnexion")
            if avant is None:
                Clock.schedule_once(lambda dt: self._popup_hors_ligne(), 1.5)

    def _montrer_banner(self, afficher):
        cible_h = dp(44) if afficher else 0
        Animation(height=cible_h, opacity=1 if afficher else 0, duration=0.25).start(self.banner_reseau)

    def ouvrir_reglages_internet(self):
        if platform != "android":
            self.toast("Active ta connexion Internet puis réessaie")
            return
        try:
            from jnius import autoclass
            Intent = autoclass("android.content.Intent")
            Settings = autoclass("android.provider.Settings")
            act = autoclass("org.kivy.android.PythonActivity").mActivity
            try:
                act.startActivity(Intent("android.settings.panel.action.INTERNET_CONNECTIVITY"))   # Android 10+
            except Exception:
                act.startActivity(Intent(Settings.ACTION_WIRELESS_SETTINGS))
        except Exception as e:
            print("Réglages internet :", e)
            self.toast("Ouvre les paramètres du téléphone → Réseau")

    def _popup_hors_ligne(self):
        if self.en_ligne:
            return
        c = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        c.add_widget(etiquette("Tu n'as pas de connexion Internet.\n\nTu peux jouer hors-ligne (entraînement, examen, "
                               "multijoueur sur le même téléphone). Pour le classement, les salles en ligne et le "
                               "mode classe, active tes données mobiles ou le Wi-Fi.", taille="15sp"))
        p = self._popup("Connexion Internet", c, (0.9, 0.55))
        c.add_widget(bouton("Activer Internet", VERT, lambda: (p.dismiss(), self.ouvrir_reglages_internet()), neon=VERT))
        c.add_widget(bouton("Continuer hors-ligne", PANEL2, p.dismiss))
        p.open()

    def exiger_en_ligne(self):
        """True si on peut utiliser les fonctions en ligne ; sinon explique pourquoi."""
        if not self.en_ligne:
            self._popup_hors_ligne()
            return False
        if self.consentement is not True:
            self.demander_consentement(forcer=True)
            return False
        if not getattr(self, "identifiant_joueur", ""):
            self.toast("Crée d'abord ton profil")
            return False
        return True

    # ------------------------------------------------------------ popups/toast
    def _popup(self, titre, contenu, taille=(0.9, 0.6), fermable=True):
        p = Popup(title=titre, content=contenu, size_hint=taille, auto_dismiss=fermable, title_color=CYAN,
                  separator_color=CYAN, background="", background_color=(0.04, 0.03, 0.1, 0.98), title_size="17sp")
        AndroidMathWebView.masquer_tous()
        p.bind(on_dismiss=lambda *a: AndroidMathWebView.afficher_tous())
        return p

    def toast(self, msg, duree=2.0):
        lb = Label(text=msg, font_size="14sp", bold=True, size_hint=(None, None), color=(1, 1, 1, 1))
        lb.texture_update()
        lb.size = (lb.texture_size[0] + dp(30), lb.texture_size[1] + dp(18))
        lb.pos = ((Window.width - lb.width) / 2, dp(90))
        with lb.canvas.before:
            Color(0.05, 0.4, 0.5, 0.95)
            fond = RoundedRectangle(pos=lb.pos, size=lb.size, radius=[dp(14)])
        lb.bind(pos=lambda i, v: setattr(fond, "pos", v), size=lambda i, v: setattr(fond, "size", v))
        self.root_layout.add_widget(lb)
        a = Animation(opacity=1, duration=0.01) + Animation(opacity=0, duration=0.5, t="in_quad")
        Clock.schedule_once(lambda dt: (a.start(lb), Clock.schedule_once(lambda d: self.root_layout.remove_widget(lb), 0.6)), duree)

    # ------------------------------------------------------- copier identifiant
    def copier_identifiant(self, *args):
        ident = getattr(self, "identifiant_joueur", "")
        if not ident:
            self.toast("Pas encore d'identifiant")
            return
        try:
            Clipboard.copy(ident)
        except Exception as e:
            print("presse-papiers :", e)
        SoundManager.play("notif")
        self.toast(f"Identifiant {ident} copié ✔")

    def bouton_copier_id(self, h=50):
        return bouton(f"Copier mon identifiant : {getattr(self, 'identifiant_joueur', '')}", PANEL2, self.copier_identifiant,
                      h=h, font="15sp")

    # ----------------------------------------------------------- consentement
    def _verifier_consentement(self, dt):
        if self.consentement is not None:
            return
        if not getattr(self, "nom_utilisateur", ""):
            Clock.schedule_once(self._verifier_consentement, 4.0)
            return
        self.demander_consentement()

    def demander_consentement(self, forcer=False):
        c = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        c.add_widget(etiquette(
            "Pour le classement, la recherche de joueurs, les salles en ligne et le mode classe, l'application "
            "enregistre sur le serveur : ton identifiant, ton prénom/pseudo, ta classe, ton niveau, ton âge et ton sexe "
            "(si renseignés), tes points, ta progression par chapitre et ta dernière connexion.\n\n"
            "Ces données servent au jeu et à améliorer l'application. Seuls ton prénom, ta classe, ton grade et tes "
            "statistiques sont visibles par les autres joueurs. Tu peux effacer tes données en ligne à tout moment "
            "dans Paramètres.", taille="13sp", align="left"))
        p = self._popup("Tes données", c, (0.94, 0.8), fermable=False)

        def choisir(ok_):
            self.consentement = ok_
            self._sauver_prefs_reseau()
            p.dismiss()
            if ok_:
                self.synchroniser_profil(force=True)
                self.toast("Merci ! Fonctions en ligne activées")
            else:
                self.toast("Mode hors-ligne uniquement")
        c.add_widget(bouton("J'accepte", VERT, lambda: choisir(True), neon=VERT))
        c.add_widget(bouton("Je refuse (hors-ligne seulement)", PANEL2, lambda: choisir(False)))
        p.open()

    def synchroniser_profil(self, force=False):
        """Envoie le profil au serveur (uniquement si connecté ET consentement donné)."""
        if not getattr(self, "en_ligne", False) or getattr(self, "consentement", None) is not True \
                or not getattr(self, "identifiant_joueur", ""):
            return
        if not force and time.time() - getattr(self, "_derniere_sync", 0) < 12:
            return
        self._derniere_sync = time.time()
        st = getattr(self, "stats_chapitres", {}) or {}
        bonnes = sum(v[0] for v in st.values() if isinstance(v, (list, tuple)) and len(v) == 2)
        total = sum(v[1] for v in st.values() if isinstance(v, (list, tuple)) and len(v) == 2)
        corps = {
            "identifiant": self.identifiant_joueur, "nom_utilisateur": self.nom_utilisateur,
            "classe_utilisateur": self.classe_utilisateur, "niveau_utilisateur": self.niveau_utilisateur,
            "sexe": getattr(self, "sexe_utilisateur", ""), "age": str(getattr(self, "age_utilisateur", "")),
            "points_de_rang": self.points_de_rang, "niveau_profil": self.niveau_profil, "xp": self.xp,
            "niveau_mascotte": self.niveau_mascotte, "xp_mascotte": self.xp_mascotte,
            "stats_chapitres": {k: v for k, v in st.items() if v and v[1] > 0},
            "bonnes": bonnes, "total": total, "consentement": True,
        }
        self.api("/api/sauvegarde", corps, timeout=6)

    def supprimer_mes_donnees_en_ligne(self):
        if not self.en_ligne:
            self._popup_hors_ligne()
            return
        c = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        c.add_widget(etiquette("Effacer définitivement ton profil du serveur (classement, statistiques en ligne) ?\n"
                               "Tes données restent sur ce téléphone.", taille="15sp"))
        p = self._popup("Supprimer mes données en ligne", c, (0.88, 0.5))

        def go():
            p.dismiss()
            self.api("/api/joueur/supprimer", {"identifiant": self.identifiant_joueur},
                     ok=lambda r: (setattr(self, "consentement", False), self._sauver_prefs_reseau(),
                                   self.toast("Données en ligne supprimées")),
                     err=lambda m: self.toast("Échec : " + str(m)))
        c.add_widget(bouton("Oui, supprimer", ROUGE, go, neon=ROUGE))
        c.add_widget(bouton("Annuler", PANEL2, p.dismiss))
        p.open()

    # ================================================================ écrans
    def _ecran(self, titre, texte="", ratio_texte=0.2, garder_poll=False):
        """Prépare l'écran standard de l'application (réutilise info_label / question_label)."""
        if not garder_poll:
            self._arreter_poll_salon()
            self.salon = None
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)
        self.nettoyer_boutons_bas()
        self.arreter_chrono()
        self.chrono_label.text = ""
        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = ratio_texte
        self.scroll_interaction.size_hint_y = 1 - ratio_texte
        self.info_label.text = titre
        self.question_label.text = texte

    def _fixer_hauteur(self, minimum=500):
        lay = self.interaction_layout
        total = sum(c.height for c in lay.children) + lay.spacing * max(0, len(lay.children) - 1) + dp(16)
        lay.height = max(total, dp(minimum) if minimum else 0)

    def _retour_accueil_btn(self, texte="← Revenir à l'Accueil", cb=None):
        return bouton(texte, ROUGE, cb or (lambda: self.afficher_menu_principal_modes()), neon=ROUGE)

    # ------------------------------------------------------------ hub multijoueur
    def afficher_hub_multijoueur(self, instance=None):
        self._ecran("Multijoueur & Classe", "Choisis comment jouer :\n• sur le même téléphone (limité)\n"
                    "• en ligne, chacun sur son téléphone (sans limite)\n• en classe avec le professeur")
        L = self.interaction_layout
        L.add_widget(bouton("Même téléphone (2 à 4 joueurs)", PANEL2, lambda: self.afficher_sous_menu_joueurs(None)))
        L.add_widget(bouton("Salle en ligne : créer", PANEL2, lambda: self.afficher_config_salon("duel"), neon=MAG))
        L.add_widget(bouton("Salle en ligne : rejoindre avec un code", PANEL2, lambda: self.afficher_rejoindre_salon("duel"), neon=MAG))
        L.add_widget(bouton("MODE CLASSE — Professeur (hôte)", PANEL2, lambda: self.afficher_config_salon("classe"), neon=VERT))
        L.add_widget(bouton("MODE CLASSE — Élève (code du prof)", PANEL2, lambda: self.afficher_rejoindre_salon("classe"), neon=VERT))
        L.add_widget(bouton("Joueurs : recherche, en ligne, classement", PANEL2, lambda: self.afficher_module_joueurs(), neon=AMBRE))
        L.add_widget(self._retour_accueil_btn())
        self._fixer_hauteur()

    # ------------------------------------------------------------ module Joueurs
    def afficher_module_joueurs(self, instance=None, onglet="recherche", requete=""):
        self._ecran("Joueurs & Statistiques", "", 0.12)
        L = self.interaction_layout
        ligne = BoxLayout(size_hint=(1, None), height=dp(46), spacing=dp(6))
        for nom, cle, col in (("Recherche", "recherche", CYAN), ("En ligne", "en_ligne", VERT), ("Classement", "classement", AMBRE)):
            ligne.add_widget(bouton(nom, PANEL2 if onglet != cle else PANEL, lambda c=cle: self.afficher_module_joueurs(None, c), h=46,
                                    font="14sp", neon=col))
        L.add_widget(ligne)
        L.add_widget(bouton("Mes statistiques (ce téléphone)", PANEL2, lambda: self.afficher_tableau_de_bord_stats(None), h=44, font="14sp"))
        L.add_widget(self.bouton_copier_id(44))

        if not self.exiger_en_ligne():
            L.add_widget(etiquette("Connecte-toi à Internet et accepte le partage de données pour voir les autres joueurs.", taille="14sp"))
            L.add_widget(self._retour_accueil_btn())
            self._fixer_hauteur()
            return

        zone = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=dp(6))
        if onglet == "recherche":
            inp = champ("Identifiant (ex : id123456) ou prénom", texte=requete)
            L.add_widget(inp)
            L.add_widget(bouton("Rechercher", VERT, lambda: self._chercher_joueurs(inp.text.strip(), zone), h=46, neon=VERT))
            if requete:
                self._chercher_joueurs(requete, zone)
        elif onglet == "en_ligne":
            self.api("/api/joueurs/en_ligne", ok=lambda r: self._remplir_joueurs(zone, r.get("joueurs", []),
                     f"{r.get('nombre', 0)} joueur(s) en ligne"), err=lambda m: self._msg_zone(zone, "Erreur : " + str(m)))
        else:
            self.api("/api/classement", ok=lambda r: self._remplir_joueurs(zone, r.get("classement", []), "Top 20"),
                     err=lambda m: self._msg_zone(zone, "Erreur : " + str(m)))
        L.add_widget(zone)
        L.add_widget(self._retour_accueil_btn())
        self._msg_zone(zone, "Chargement…" if onglet != "recherche" else "")

    def _msg_zone(self, zone, msg):
        zone.clear_widgets()
        zone.height = dp(40) if msg else 0
        if msg:
            zone.add_widget(etiquette(msg, h=36, taille="14sp"))
        self._fixer_hauteur(0)

    def _chercher_joueurs(self, q, zone):
        if len(q) < 2:
            self._msg_zone(zone, "Tape au moins 2 caractères")
            return
        self._msg_zone(zone, "Recherche…")
        self.api("/api/joueurs/recherche?q=" + quote(q),
                 ok=lambda r: self._remplir_joueurs(zone, r.get("joueurs", []), "Aucun joueur trouvé" if not r.get("joueurs") else ""),
                 err=lambda m: self._msg_zone(zone, "Erreur : " + str(m)))

    def _remplir_joueurs(self, zone, joueurs, titre):
        zone.clear_widgets()
        h = 0
        if titre:
            zone.add_widget(etiquette(titre, h=30, taille="14sp", couleur=CYAN))
            h += dp(36)
        for j in joueurs:
            point = "[color=22ff88]●[/color]" if j.get("en_ligne") else "[color=777799]●[/color]"
            b = bouton("", PANEL, None, h=58, font="14sp", neon=VERT if j.get("en_ligne") else (0.4, 0.4, 0.6, 1))
            b.markup = True
            b.text = f"{point} [b]{j.get('nom', '?')}[/b]  ({j.get('identifiant')})\n{j.get('grade', '')} — {j.get('points_rang', 0)} PR — {j.get('classe', '')}"
            b.bind(on_release=lambda *_, i=j.get("identifiant"): self.afficher_profil_joueur(i))
            zone.add_widget(b)
            h += dp(64)
        zone.height = h
        self._fixer_hauteur(0)

    def afficher_profil_joueur(self, ident):
        self._ecran("Fiche joueur", "Chargement…", 0.12)
        L = self.interaction_layout

        def affiche(p):
            self.question_label.text = ""
            st = p.get("stats_chapitres", {})
            classes = sorted(((v[0] / v[1], k, v) for k, v in st.items() if v and v[1] >= 3), reverse=True)
            forts = ", ".join(k for _, k, _ in classes[:3]) or "—"
            faibles = ", ".join(k for _, k, _ in classes[-3:][::-1]) if len(classes) > 3 else "—"
            etat = "[color=22ff88]● en ligne[/color]" if p.get("en_ligne") else "[color=8888aa]● hors-ligne[/color]"
            L.clear_widgets()
            L.add_widget(etiquette(
                f"[size=22sp][b]{p.get('nom', '?')}[/b][/size]   {etat}\n[color=00f0ff]{p.get('identifiant')}[/color]\n\n"
                f"Grade : [b]{p.get('grade', '')}[/b]   ({p.get('points_rang', 0)} PR)\n"
                f"Classe : {p.get('classe', '—')}    Niveau profil : {p.get('niveau_profil', 1)}\n"
                f"Parties : {p.get('parties', 0)}    Questions : {p.get('total', 0)}\n"
                f"Précision : [b]{p.get('precision', 0)} %[/b]    Série : {p.get('serie_jours', 0)} jour(s)\n"
                f"Points forts : {forts}\nÀ travailler : {faibles}\n"
                f"Dernière connexion : {p.get('derniere_connexion', '—')}", taille="15sp", markup=True, align="left"))
            L.add_widget(bouton("Copier cet identifiant", PANEL2, lambda: (Clipboard.copy(p.get("identifiant", "")), self.toast("Copié ✔")), h=46))
            L.add_widget(bouton("← Retour aux joueurs", ROUGE, lambda: self.afficher_module_joueurs(None), neon=ROUGE))
            self._fixer_hauteur()
        self.api("/api/joueur/" + str(ident), ok=affiche,
                 err=lambda m: setattr(self.question_label, "text", "Joueur introuvable"))
        L.add_widget(bouton("← Retour", ROUGE, lambda: self.afficher_module_joueurs(None), neon=ROUGE))
        self._fixer_hauteur()

    # ------------------------------------------------------------ réglage serveur
    def afficher_reglage_serveur(self, instance=None):
        self._ecran("Serveur", "Adresse du serveur.\nInternet : adresse par défaut.\nClasse sans Internet : le professeur lance "
                    "le serveur sur un PC/téléphone relié au même Wi-Fi, ex : http://192.168.1.20:5000", 0.3)
        L = self.interaction_layout
        inp = champ("https://...", texte=self.url_serveur)
        L.add_widget(inp)

        def tester():
            self.url_serveur = inp.text.strip().rstrip("/") or URL_PAR_DEFAUT
            self.api("/api/ping", ok=lambda r: self.toast("Serveur joignable ✔"), err=lambda m: self.toast("Injoignable : " + str(m)))

        def enregistrer():
            self.url_serveur = inp.text.strip().rstrip("/") or URL_PAR_DEFAUT
            self._sauver_prefs_reseau()
            self.toast("Serveur enregistré")
            self._ping_reseau(0)
        L.add_widget(bouton("Tester", PANEL2, tester))
        L.add_widget(bouton("Enregistrer", VERT, enregistrer, neon=VERT))
        L.add_widget(bouton("Adresse par défaut", PANEL2, lambda: setattr(inp, "text", URL_PAR_DEFAUT)))
        L.add_widget(self._retour_accueil_btn())
        self._fixer_hauteur()

    # ================================================================ salles
    def afficher_config_salon(self, type_):
        if not self.exiger_en_ligne():
            return
        prof = type_ == "classe"
        self._ecran("Mode Classe — Professeur" if prof else "Créer une salle en ligne",
                    "Personnalise la session puis lance la salle.\nLes élèves rejoignent avec le code." if prof
                    else "Choisis les réglages. Tes amis rejoignent avec le code (tu joues aussi).", 0.16)
        cfg = {"classe": self.classe_utilisateur if self.classe_utilisateur in CLASSES else "3ème", "chapitres": [],
               "nb_questions": 10, "temps_par_question": 30, "avance": "manuel", "bonus_vitesse": True,
               "points_bonne": 100}
        L = self.interaction_layout

        zone_chap = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=dp(4))

        def rebuild_chapitres():
            zone_chap.clear_widgets()
            chaps = PROGRESSION_OFFICIELLE.get(cfg["classe"], [])
            zone_chap.add_widget(etiquette(f"Chapitres ({len(cfg['chapitres']) or 'tous'} sélectionné(s))", h=26, taille="13sp", couleur=CYAN))
            for ch in chaps:
                actif = ch in cfg["chapitres"]
                zone_chap.add_widget(bouton(("✔ " if actif else "") + ch, PANEL if actif else PANEL2,
                                            lambda c=ch: (cfg["chapitres"].remove(c) if c in cfg["chapitres"] else cfg["chapitres"].append(c),
                                                          rebuild_chapitres()), h=38, font="13sp", neon=VERT if actif else CYAN))
            zone_chap.height = dp(32) + dp(42) * len(chaps)
            self._fixer_hauteur()

        def choisir_classe(c):
            cfg["classe"], cfg["chapitres"] = c, []
            maj_classes()
            rebuild_chapitres()

        zone_classes = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=dp(4))

        def maj_classes():
            zone_classes.clear_widgets()
            zone_classes.add_widget(etiquette("Classe", h=26, taille="13sp", couleur=CYAN))
            ligne1, ligne2 = BoxLayout(spacing=dp(4), size_hint=(1, None), height=dp(38)), BoxLayout(spacing=dp(4), size_hint=(1, None), height=dp(38))
            for i, c in enumerate(CLASSES):
                (ligne1 if i < 4 else ligne2).add_widget(bouton(c, PANEL if c == cfg["classe"] else PANEL2, lambda c=c: choisir_classe(c),
                                                                h=38, font="12sp", neon=MAG if c == cfg["classe"] else CYAN))
            zone_classes.add_widget(ligne1)
            zone_classes.add_widget(ligne2)
            zone_classes.height = dp(26 + 38 * 2 + 12)
            self._fixer_hauteur()

        L.add_widget(zone_classes)
        L.add_widget(zone_chap)

        def cycle(libelle, cle, valeurs, fmt):
            b = bouton("", PANEL2, None, h=44, font="14sp")

            def maj():
                b.text = f"{libelle} : {fmt(cfg[cle])}"

            def clic():
                i = valeurs.index(cfg[cle]) if cfg[cle] in valeurs else -1
                cfg[cle] = valeurs[(i + 1) % len(valeurs)]
                maj()
            b.bind(on_release=lambda *_: clic())
            maj()
            return b
        L.add_widget(cycle("Nombre de questions", "nb_questions", [5, 10, 15, 20, 30], str))
        L.add_widget(cycle("Temps par question", "temps_par_question", [0, 15, 20, 30, 45, 60, 90], lambda v: "illimité" if v == 0 else f"{v} s"))
        L.add_widget(cycle("Passage à la suivante", "avance", ["manuel", "auto"], lambda v: "par le professeur" if v == "manuel" and prof else ("manuel" if v == "manuel" else "automatique")))
        L.add_widget(cycle("Bonus de rapidité", "bonus_vitesse", [True, False], lambda v: "oui" if v else "non"))
        L.add_widget(cycle("Points par bonne réponse", "points_bonne", [50, 100, 200], str))

        def creer():
            corps = {"type": type_, "hote_id": self.identifiant_joueur, "hote_nom": self.nom_utilisateur,
                     "config": {**cfg, "difficulte": self.determiner_rang_et_details()[3], "hote_joue": not prof,
                                "titre": f"Classe de {self.nom_utilisateur}" if prof else ""}}
            self.api("/api/salon/creer", corps, timeout=10,
                     ok=lambda r: self._salon_demarrer(r["code_pin"], "hote", type_, r.get("config", cfg)),
                     err=lambda m: self.toast("Création impossible : " + str(m)))
        L.add_widget(bouton("Créer la salle", VERT, creer, h=54, neon=VERT))
        L.add_widget(self._retour_accueil_btn("← Retour", lambda: self.afficher_hub_multijoueur()))
        maj_classes()
        rebuild_chapitres()

    def afficher_rejoindre_salon(self, type_):
        if not self.exiger_en_ligne():
            return
        self._ecran("Rejoindre " + ("la classe" if type_ == "classe" else "une salle"), "Entre le code à 6 chiffres donné par l'hôte :", 0.2)
        L = self.interaction_layout
        inp = champ("Code à 6 chiffres", h=60)
        inp.input_filter = "int"
        inp.halign = "center"
        L.add_widget(inp)

        def go():
            code = inp.text.strip()
            if len(code) != 6:
                self.toast("Le code contient 6 chiffres")
                return
            self.api("/api/salon/rejoindre", {"code_pin": code, "identifiant": self.identifiant_joueur, "nom": self.nom_utilisateur},
                     ok=lambda r: self._salon_demarrer(code, "joueur", r.get("type", type_), r.get("config", {}), r.get("hote", "")),
                     err=lambda m: self.toast("Impossible : " + str(m)))
        L.add_widget(bouton("Rejoindre", VERT, go, h=54, neon=VERT))
        L.add_widget(self._retour_accueil_btn("← Retour", lambda: self.afficher_hub_multijoueur()))
        self._fixer_hauteur()

    # ------------------------------------------------------------- cycle d'une salle
    def _salon_demarrer(self, code, role, type_, cfg, hote_nom=""):
        self._ecran("Salle " + code, "Connexion à la salle…", 0.2)
        self.salon = {"code": code, "role": role, "type": type_, "cfg": cfg, "vue": None, "index_affiche": -1,
                      "hote_nom": hote_nom, "stats_envoyees": False, "a_repondu": False, "widgets": {}}
        self._poll_salon = Clock.schedule_interval(self._salon_poll, 1.2)
        self._salon_poll(0)

    def _arreter_poll_salon(self):
        if getattr(self, "_poll_salon", None):
            self._poll_salon.cancel()
            self._poll_salon = None

    def quitter_salon(self):
        self._arreter_poll_salon()
        self.salon = None
        self.afficher_hub_multijoueur()

    def _salon_poll(self, dt):
        s = self.salon
        if not s:
            return False
        self.api(f"/api/salon/{s['code']}/etat?id={quote(self.identifiant_joueur)}", ok=self._salon_maj,
                 err=lambda m: None, timeout=4)

    def _salon_maj(self, res):
        s = self.salon
        if not s:
            return
        etat = res.get("etat")
        s["derniere"] = res
        if etat == "attente":
            if s["vue"] != "attente":
                self._vue_attente(res)
            self._maj_attente(res)
        elif etat == "question":
            if s["index_affiche"] != res["index_q"] or s["vue"] != "question":
                self._vue_question(res)
            self._maj_question(res)
        elif etat == "termine":
            if s["vue"] != "fin":
                self._arreter_poll_salon()
                self._vue_fin(res)

    # -- salle d'attente ------------------------------------------------------
    def _vue_attente(self, res):
        s = self.salon
        s["vue"] = "attente"
        hote = s["role"] == "hote"
        self._ecran("Salle " + s["code"], "", 0.12, garder_poll=True)
        L = self.interaction_layout
        L.add_widget(etiquette(f"[size=16sp]Code de la salle[/size]\n[size=44sp][b][color=00f0ff]{s['code']}[/color][/b][/size]", h=110, markup=True))
        L.add_widget(bouton("Copier le code", PANEL2, lambda: (Clipboard.copy(s["code"]), self.toast("Code copié ✔")), h=44))
        s["widgets"]["parts"] = etiquette("", taille="15sp")
        L.add_widget(s["widgets"]["parts"])
        if hote:
            L.add_widget(bouton("Lancer la session", VERT, lambda: self._salon_action("lancer"), h=56, neon=VERT))
        else:
            L.add_widget(etiquette("En attente du lancement par l'hôte…", h=40, couleur=CYAN))
        L.add_widget(self._retour_accueil_btn("Quitter la salle", self.quitter_salon))
        self._fixer_hauteur()

    def _maj_attente(self, res):
        w = self.salon["widgets"].get("parts")
        if not w:
            return
        noms = [p["nom"] or p["identifiant"] for p in res.get("participants", [])]
        if self.salon["role"] == "hote":
            w.text = f"{res.get('nombre_eleves', 0)} participant(s) connecté(s)\n" + ("\n".join(noms[:30]) if noms else "—")
        else:
            w.text = f"{res.get('nombre_eleves', 0)} participant(s) dans la salle\nHôte : {self.salon.get('hote_nom', '')}"

    def _salon_action(self, action):
        s = self.salon
        self.api(f"/api/salon/{s['code']}/{action}", {"hote_id": self.identifiant_joueur},
                 ok=lambda r: self._salon_poll(0), err=lambda m: self.toast("Erreur : " + str(m)))

    # -- question ---------------------------------------------------------------
    def _vue_question(self, res):
        s = self.salon
        s["vue"] = "question"
        s["index_affiche"] = res["index_q"]
        s["a_repondu"] = bool(res.get("a_repondu"))
        hote = s["role"] == "hote"
        joue = (not hote) or s["cfg"].get("hote_joue") or res.get("config", {}).get("hote_joue")
        q = res["question"]
        self._ecran(f"Question {res['index_q'] + 1}/{res['nb_questions']}", "", 0.0, garder_poll=True)
        self.scroll_texte.size_hint_y = None
        self.scroll_texte.height = 0
        self.scroll_interaction.size_hint_y = 1
        L = self.interaction_layout
        s["widgets"] = {}
        web = AndroidMathWebView(size_hint=(1, None), height=dp(300 if not joue else 240))
        web.set_question({"enonce": q["enonce"], "options": q["options"], "explication": ""},
                         titre_tete=f"Salle {s['code']} · Q{res['index_q'] + 1}/{res['nb_questions']}", avec_explication=False)
        L.add_widget(web)
        s["widgets"]["web"] = web
        s["widgets"]["statut"] = etiquette("", h=34, taille="14sp", couleur=CYAN)
        L.add_widget(s["widgets"]["statut"])
        s["widgets"]["boutons"] = []
        if joue:
            for i, o in enumerate(q["options"]):
                b = bouton(f"{LETTRES[i]}   {latex_vers_texte(o)}", PANEL2, lambda i=i: self._salon_repondre(i), h=50, font="16sp")
                s["widgets"]["boutons"].append(b)
                L.add_widget(b)
            if s["a_repondu"]:
                self._verrouiller_boutons()
        if hote:
            s["widgets"]["liste"] = etiquette("", taille="13sp", align="left")
            L.add_widget(s["widgets"]["liste"])
            ligne = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(6))
            ligne.add_widget(bouton("Question suivante ➜", VERT, lambda: self._salon_action("suivante"), h=50, font="14sp", neon=VERT))
            ligne.add_widget(bouton("Voir les réponses", PANEL2, self.afficher_details_reponses, h=50, font="14sp", neon=AMBRE))
            L.add_widget(ligne)
            L.add_widget(bouton("Terminer la session", ROUGE, lambda: self._salon_action("terminer"), h=46, neon=ROUGE))
        else:
            L.add_widget(self._retour_accueil_btn("Quitter la salle", self.quitter_salon))
        self._fixer_hauteur()
        SoundManager.play("notif")

    def _verrouiller_boutons(self, choisi=None):
        for i, b in enumerate(self.salon["widgets"].get("boutons", [])):
            b.disabled = True
            if choisi is not None and i == choisi:
                b.opacity = 1
            else:
                b.opacity = 0.45

    def _salon_repondre(self, i):
        s = self.salon
        if not s or s["a_repondu"]:
            return
        s["a_repondu"] = True
        self._verrouiller_boutons(i)
        web = s["widgets"].get("web")
        if web:
            web.marquer(i)
        self.api(f"/api/salon/{s['code']}/repondre",
                 {"identifiant": self.identifiant_joueur, "index_q": s["index_affiche"], "choix": i},
                 ok=lambda r: self.toast("Réponse envoyée ✔"), err=lambda m: self.toast("Non envoyée : " + str(m)))

    def _maj_question(self, res):
        s = self.salon
        w = s["widgets"]
        if not w:
            return
        t = res.get("temps_restant")
        self.chrono_label.text = f"{t}s" if t is not None else ""
        if "statut" in w:
            etat = "Réponse envoyée — en attente des autres" if s["a_repondu"] else "À toi de répondre"
            if s["role"] == "hote" and not s["cfg"].get("hote_joue"):
                etat = f"{res.get('eleves_ont_repondu', 0)}/{res.get('nombre_eleves', 0)} ont répondu"
            w["statut"].text = etat
        if "liste" in w:
            lignes = [("[color=22ff88]✔[/color] " if p.get("a_repondu") else "[color=888899]…[/color] ") + (p.get("nom") or p["identifiant"])
                      for p in res.get("participants", [])]
            w["liste"].markup = True
            w["liste"].text = "\n".join(lignes[:40])
            self._fixer_hauteur()

    # -- fin : tableau des scores pour tout le monde ------------------------------
    def _vue_fin(self, res):
        s = self.salon
        s["vue"] = "fin"
        self.chrono_label.text = ""
        classement = res.get("classement", [])
        mon = next((c for c in classement if c["identifiant"] == self.identifiant_joueur), None)
        podium = mon and mon["rang"] <= 3
        SoundManager.play("victoire" if podium else "notif")
        self._ecran("Tableau des scores", "", 0.12, garder_poll=True)
        L = self.interaction_layout
        L.add_widget(etiquette("[size=20sp][b]CLASSEMENT FINAL[/b][/size]", h=40, markup=True, couleur=AMBRE))
        medailles = {1: "🥇", 2: "🥈", 3: "🥉"}
        for c in classement[:50]:
            moi = c["identifiant"] == self.identifiant_joueur
            col = "00f0ff" if moi else "e9eaff"
            L.add_widget(etiquette(f"[color={col}]{medailles.get(c['rang'], str(c['rang']) + '.')}  [b]{c['nom'] or c['identifiant']}[/b]"
                                   f"{'  (toi)' if moi else ''} — {c['score']} pts[/color]", h=34, markup=True, taille="16sp", align="left"))
        if s["role"] == "hote":
            L.add_widget(bouton("Détails des réponses (professeur)", PANEL2, self.afficher_details_reponses, neon=AMBRE))
            if not s["stats_envoyees"]:
                s["stats_envoyees"] = True
                self.api(f"/api/salon/{s['code']}/cloturer_stats", {"hote_id": self.identifiant_joueur})
        L.add_widget(self._retour_accueil_btn("Retour au multijoueur", self.quitter_salon))
        self._fixer_hauteur()
        self.points_de_rang += 2 if mon else 0
        self.sauvegarder_donnees_locales()
        self.synchroniser_profil()

    def afficher_details_reponses(self):
        """Réservé à l'hôte : qui a répondu quoi, temps, taux de réussite par question."""
        s = self.salon
        if not s or s["role"] != "hote":
            return

        def affiche(res):
            sv = ScrollView(do_scroll_x=False)
            col = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8), padding=dp(6))
            col.bind(minimum_height=col.setter("height"))
            for q in res["questions"]:
                taux = q["taux_reussite"]
                lignes = [f"[b]Q{q['index'] + 1}.[/b] {latex_vers_texte(q['enonce'])}",
                          f"[color=22ff88]Bonne réponse : {latex_vers_texte(q['bonne_reponse'])}[/color]   "
                          f"(réussite : {'—' if taux is None else str(taux) + ' %'})"]
                for r in q["reponses"]:
                    ok_ = r["correct"]
                    lignes.append(("[color=22ff88]✔[/color] " if ok_ else "[color=ff3b5c]✘[/color] ") +
                                  f"{r['nom']} : {latex_vers_texte(r['choix_texte'] or '—')}  ({r['temps_ms'] / 1000:.1f}s)")
                col.add_widget(etiquette("\n".join(lignes), taille="13sp", markup=True, align="left"))
            sv.add_widget(col)
            p = self._popup("Réponses des élèves", sv, (0.96, 0.85))
            p.open()
        self.api(f"/api/salon/{s['code']}/resultats?id={self.identifiant_joueur}", ok=affiche,
                 err=lambda m: self.toast("Erreur : " + str(m)), timeout=8)
