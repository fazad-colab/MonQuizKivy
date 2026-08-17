import random
import math
import json
import os
import sys
os.environ['KIVY_ORIENTATION'] = 'portrait'
from kivy.app import App
os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.core.window import Window 
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from moteur_quiz import MoteurMathematique
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.network.urlrequest import UrlRequest 
from kivy.core.text import LabelBase
import webbrowser

# Ajout pour les requêtes asynchrones
class FixedDynamicQuizApp(App):
    def build(self):
        Window.rotation = 0  # Force rotation 0 degré
        Window.clearcolor = (0.1, 0.2, 0.4, 1) # ta couleur de fond
        return TonEcranPrincipal()
        
        # --- VARIABLES GLOBALES DE SESSION ---
        self.score = 0
        self.combo = 0  
        self.bonne_reponse = ""
        self.explication_erreur = ""
        self.niveau_actuel = ""
        self.classe_actuelle = ""
        self.question_generée_ia = "Aucune question pour l'instant"
        self.mode_jeu = "" 
        
        # --- DONNÉES UTILISATEUR & DEVELOPPEUR ---
        self.nom_utilisateur = ""
        self.niveau_utilisateur =""
        self.classe_utilisateur=""
        self.sexe_utilisateur =""
        self.age_utilisateur =""
        self.nom_developpeur = "Fazad Nassur"
        self.temps_debut_question = 0.0
        
        # --- SYSTÈME DE PROGRESSION (XP & RANGS EXTENDUS TYPE COMPÉTITIF) ---
        self.xp = 0
        self.niveau_profil = 1
        self.points_de_rang = 0 
        
        # --- FILE D'ATTENTE DES AVIS (HORS-LIGNE) ---
        self.file_attente_avis = []

        # Liste ordonnée mise à jour avec toutes les sous-catégories 
        self.LISTE_RANGS = [
            "Bronze I ", "Bronze II ", "Bronze III ", "Bronze IV ", "Bronze V ",
            "Argent I ", "Argent II ", "Argent III ", "Argent IV ", "Argent V ",
            "Or I ", "Or II ", "Or III ", "Or IV ", "Or V ",
            "Platine I ", "Platine II ", "Platine III ", "Platine IV ", "Platine V ",
            "Diamant I ", "Diamant II ", "Diamant III ", "Diamant IV ", "Diamant V ",
            "Héroïque I ", "Héroïque II ", "Héroïque III ", "Héroïque IV ", "Héroïque V ",
            "Maître I ", "Maître II ", "Maître III ", "Maître IV ", "Maître V ",
            "Grand Maître I ", "Grand Maître II ", "Grand Maître III ", "Grand Maître IV ", "Grand Maître V ",
            "Master I ", "Master II ", "Master III ", "Master IV ", "Master V ",
            "Grand Master I ", "Grand Master II ", "Grand Master III ", "Grand Master IV ", "Grand Master V ",
            "Leadership "
        ]
        
        # --- SYSTÈME D'EXAMEN BLANC ---
        self.examen_questions = []
        self.examen_index_actuel = 0
        self.examen_reponses_eleve = [] 
        self.temps_examen_restant = 300 
        
        self.pile_chapitres_courants = []
        self.ordre_classes = ["6ème", "5ème", "4ème", "3ème", "2nde", "1ere", "Terminale", "L1 MPC"]
        
        # --- STATISTIQUES AVANCÉES ---
        self.stats_chapitres = {}
        self.historique_scores = []  # Pour analyser la vitesse d'évolution (stable, progresse, régresse)
        self.nom_fichier_sauvegarde = "mathquiz.json"
        
        # --- PROGRAMME OFFICIEL COMPLET ---
        self.progression_officielle = {
            "6ème": ["Arithmétiques", "Droites et Segments", "Nombres décimaux", "Les angles", "Fraction", "Triangles", "Organisation des calculs", "Cercle et parallélogramme", "Entier relatifs et nombres décimaux relatifs", "Symétrie centrale et axiale", "Initiation aux calculs littéraux", "Proportionnalité", "Cube – Pavé droit – Cylindre", "Pourcentage et échelle"],
            "5ème": ["Nombres décimaux relatifs", "Puissance", "Arithmétique", "Distance entre deux points", "Angles", "Fraction", "Calcul littérale", "Notion d’équation", "Symétrie centrale et orthogonale", "Médiatrice d’un segment", "Repérage sur un quadrillage", "Proportionnalité", "Pourcentage et échelle", "Polygone", "Prisme droit", "Pyramide"],
            "4ème": ["PGDC et PPCM", "Nombres rationnels", "Distance d’un point à une droite", "Secteurs angulaires", "Symétrie centrale et orthogonale", "Projection", "Les triangles", "Cercle", "Outil vectoriel", "Puissance", "Calcul sur les expressions algébriques", "Equation, Intervalle et Inéquation", "Proportionnalité", "Statistique", "Repérage", "Sphère et boule", "Polygone régulier", "Pyramide et cône de révolution"],
            "3ème": ["Renforcement de capacité", "Racine carrée et Valeur absolue", "Triangle rectangle", "Monôme et polynôme", "Thales", "Equation et Inéquation", "Vecteur et Homothétie", "Repère", "Equation d’une droite", "Application affine", "Système dans IR²", "Statistique", "Angles et Rotation", "Symétrie centrale et Axiale", "Pyramide et cône", "Sujet types"],
            "2nde": ["Vecteurs et repérage", "Valeur absolue et intervalles"],
            "1ere": ["Dérivation fonctionnelle", "Polynômes du second degré"],
            "Terminale": ["Nombres complexes", "Calcul intégral"],
            "L1 MPC": ["Cinématique absolue", "Accélération de Coriolis", "Frenet", "Régime RLC", "Optique de Descartes", "Théorème du rang", "Développements limités"]
        }
        
        # --- DICTIONNAIRE DU FORMULAIRE DE COURS ---
        self.formulaire_cours = {
            "6ème": "• Priorités : Multiplications et divisions d'abord.\n• Périmètre Cercle = 2 × π × R\n• Angles : Aigu (<90°), Droit (=90°), Obtus (>90°).\n• Symétrie axiale : Pliage le long d'une droite.",
            "5ème": "• Formule des puissances : a^n × a^m = a^(n+m)\n• Triangle : La somme des angles vaut toujours 180°.\n• Symétrie centrale : Demi-tour autour d'un centre (O est le milieu).",
            "4ème": "• Rationnels : Nombre s'écrivant a/b avec b non nul.\n• Cosinus = Côté adjacent / Hypoténuse.\n• Relation de Chasles : vec(AB) + vec(BC) = vec(AC).",
            "3ème": "• Identités Remarquables :\n  1) (a+b)² = a² + 2ab + b²\n  2) (a-b)² = a² - 2ab + b²\n  3) (a-b)(a+b) = a² - b²\n• Thalès : OA/OC = OB/OD = AB/CD\n• Équation droite : y = ax + b (a = coefficient directeur).",
            "2nde": "• Valeur absolue : |x| est la distance à zéro. Toujours ≥ 0.\n• Vecteurs colinéaires si xy' - yx' = 0.",
            "1ere": "• Dérivées usuelles : (x²)' = 2x, (x^n)' = n·x^(n-1)\n• Second degré : Δ = b² - 4ac. Si Δ>0 (2 racines), Si Δ=0 (1 racine double), Si Δ<0 (0 racine réelle).",
            "Terminale": "• Nombre complexe : z = a + ib avec i² = -1.\n• Intégrale : Valeur de [F(b) - F(a)] où F est la primitive.",
            "L1 MPC": "• Accélération Coriolis : Ac = 2·vec(Ω) × vec(Vr)\n• Base de Frenet : An = v² / R\n• Théorème du rang : dim(Ker(f)) + dim(Im(f)) = dim(E)\n• Développements limités (en 0) :\n  cos(x) = 1 - x²/2 + o(x²)\n  sin(x) = x - x³/6 + o(x³)\n  e^x = 1 + x + o(x)"
        }
        
        for classe, chapitres in self.progression_officielle.items():
            for chap in chapitres:
                self.stats_chapitres[chap] = [0, 0]
                
        self.evenement_chrono = None
        self.chapitre_en_cours = ""
        
        # --- CONSTRUCTION DE L'INTERFACE ENTIÈREMENT OPTIMISÉE POUR LE BAS DU POUCE ---
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(15))
        with self.main_layout.canvas.before:
            Color(0.12, 0.28, 0.48, 1)
            self.rect = RoundedRectangle(size=self.main_layout.size, pos=self.main_layout.pos, radius=[10])
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # 1. Zone d'en-tête (Informations de profil et Chronomètre) - RESTE EN HAUT MAIS COMPACT
        self.info_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(90), spacing=dp(2))
        self.info_label = Label(text="Initialisation en cours...", font_size='18sp', bold=True, color=(1, 0.84, 0, 1), halign='left', valign='middle')
        self.info_label.bind(size=self._update_text_size)
        self.chrono_label = Label(text="", font_size='22sp', bold=True, color=(1, 0.35, 0.35, 1), halign='right', valign='middle')
       # Bouton Paramètres dans le coin supérieur droit
        self.btn_parametres = Button(
            text="Paramètres",
            font_size='22sp',
            size_hint=(None, 1),
            width=dp(200),
            background_color=(0.12, 0.28, 0.48, 0.1)
        )
        self.btn_parametres.bind(on_press=self.ouvrir_menu_parametres)

        self.chrono_label.bind(size=self._update_text_size)
        self.info_layout.add_widget(self.info_label)
        self.info_layout.add_widget(self.chrono_label)
        self.main_layout.add_widget(self.info_layout)
        self.info_layout.add_widget(self.btn_parametres)

        
        # 2. Zone d'affichage des énoncés de questions ou des cours - MILIEU SUPÉRIEUR
        self.scroll_texte = ScrollView(size_hint_y=0.32, do_scroll_x=False, do_scroll=True)
        self.question_label = Label(text="", font_size='20sp', halign='center', valign='middle', size_hint=(1, None), color=(1, 1, 1, 1))
        self.question_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - 10, None)))
        self.question_label.bind(texture_size=lambda instance, size: setattr(instance, 'height', max(size[1] + 10, 150)))
        self.scroll_texte.add_widget(self.question_label)
        self.main_layout.add_widget(self.scroll_texte)
        
        # 3. Zone d'interaction dynamique principale (Boutons de réponses, Saisie, Menus) - BAS DU POUCE
        self.scroll_interaction = ScrollView(size_hint_y=0.68, do_scroll_x=False, do_scroll_y=True)
        self.interaction_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(600), spacing=dp(15))
        self.scroll_interaction.add_widget(self.interaction_layout)
        self.main_layout.add_widget(self.scroll_interaction)
        
        # Bouton persistant dédié pour le retour menu (Placé stratégiquement sous les boutons ou réajusté)
        self.btn_menu_persistant = Button(text="Revenir au Menu Principal", font_size='20sp', bold=True, size_hint_y=None, height=dp(90), background_color=(0.12, 0.53, 0.9, 1))
        self.btn_menu_persistant.bind(on_press=self.action_retour_menu_persistant)
        
        # Bouton unique de retour pour les vues isolées (S'affichera tout en bas du main_layout)
        self.btn_retour_isole = Button(text="← Retour Évolution", size_hint=(1, None), height=dp(90), font_size='22sp', bold=True, background_color=(0.15, 0.45, 0.75, 1))
        self.charger_donnees_locales()
        
        # Lancement de la tâche récurrente de synchronisation en arrière-plan (toutes les 15 secondes)
        Clock.schedule_interval(self.tenter_synchronisation_file_attente, 15.0)
        self.afficher_ecran_demarrage()
            
        return self.main_layout
        
    def afficher_question_math(self, enonce):
        # Chemin vers ton fichier index.html dans le dossier de l'app
        chemin_fichier = "index.html"

        # Structure HTML qui intègre ton énoncé et charge KaTeX
        contenu_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="file:///storage/emulated/0/Algorithmes/katex/katex.min.css">
            <script src="file:///storage/emulated/0/Algorithmes/katex/katex.min.js"></script>
            <script src="file:///storage/emulated/0/Algorithmes/katex/contrib/auto-render.min.js"></script>
        </head>
        <body>
            <div id="math-content" style="font-size:20px; padding:20px;">
                {enonce_latex}
            </div>
            <script>
                renderMathInElement(document.getElementById("math-content"), {{
                    delimiters: [
                        {{left: "$$", right: "$$", display: true}},
                        {{left: "$", right: "$", display: false}}
                    ]
                }});
            </script>
        </body>
        </html>
        """
         
         # Sauvegarde de la nouvelle question dans le fichier
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            f.write(contenu_html)

        chemin_complet = os.path.abspath(chemin_fichier)
        try:
            webbrowser.open(f"file://{chemin_complet}")
            print("Succès : Commande d'ouverture du navigateur envoyée.")
        except Exception as e:
            print(f"Erreur : Le navigateur n'a pas pu s'ouvrir. Détails : {e}")

        print(f"Question générée et sauvegardée dans {chemin_fichier}")
    
    def afficher_ecran_demarrage(self):
        self.nettoyer_boutons_bas()
        self.info_layout.opacity = 0
        self.scroll_texte.opacity = 0 
        self.scroll_interaction.opacity = 0

        chemin_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'badges', 'logo.png')
        print(f"CHEMIN LOGO: {chemin_logo}")

        ecran_intro = FloatLayout()
        
        with ecran_intro.canvas.before:
             Color(0.12, 0.28, 0.48, 1)
             self.rect_splash = Rectangle(size=ecran_intro.size, pos=ecran_intro.pos)
        ecran_intro.bind(size=lambda inst, val: setattr(self.rect_splash, 'size', val))
        ecran_intro.bind(pos=lambda inst, val: setattr(self.rect_splash, 'pos', val))
    
        if os.path.exists(chemin_logo):
            logo_splash = Image(
                source=chemin_logo, 
                nocache=True,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(0.9, 0.9), 
                pos_hint={'center_x': 0.5, 'center_y': 1},
                opacity=0 
            )
            ecran_intro.add_widget(logo_splash)
        
            # FONDU IN + OUT
            anim = Animation(opacity=1, duration=0.5) + Animation(opacity=1, duration=2) + Animation(opacity=1, duration=0.5)
            anim.start(logo_splash)
        
        else:
            test = Label(text="LOGO TEST", font_size=dp(50), color=(1,0,0,1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
            ecran_intro.add_widget(test)
            print(f"ALERTE: Le fichier image est introuvable -> {chemin_logo}")

        self.main_layout.add_widget(ecran_intro) 
        Clock.schedule_once(lambda dt: self.    aller_au_menu_principal(ecran_intro), 5)

    def initialiser_lecteur_musique(self):
        if hasattr(self, 'lecteur_actif') and self.lecteur_actif:
            return

        self.dossier_musique = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'musiques')
        
        if not os.path.exists(self.dossier_musique):
            os.makedirs(self.dossier_musique)
            print(f"Dossier 'musiques' créé ici : {self.dossier_musique}")
            self.playlist = []
            return

        # Récupère uniquement les .ogg situés directement à la racine du dossier 'musiques' (pour le menu)
        self.playlist = [os.path.join(self.dossier_musique, f) for f in os.listdir(self.dossier_musique) if f.endswith('.ogg') and os.path.isfile(os.path.join(self.dossier_musique, f))]
        
        if not self.playlist:
            print("Aucun fichier .ogg trouvé à la racine du dossier 'musiques'.")
            return

        self.sound = None
        self.lecteur_actif = True
        self.jouer_musique_suivante()
        
        # Vérifier si la musique est finie
        Clock.schedule_interval(self.verifier_fin_musique, 1)

    def jouer_musique_suivante(self):
        if not self.playlist:
            return

        # Vérifier si l'index dépasse la taille de la playlist pour recommencer au début
        if not hasattr(self, 'current_index') or self.current_index >= len(self.playlist):
            self.current_index = 0

        morceau_choisi = self.playlist[self.current_index]
        self.current_index += 1

        if self.sound:
            self.sound.stop()
            self.sound.unload()

        self.sound = SoundLoader.load(morceau_choisi)
        if self.sound:
            self.sound.play()
            print(f"Lecture en cours (Menu) : {os.path.basename(morceau_choisi)}")

    def verifier_fin_musique(self, dt):
        # Relance la musique suivante uniquement si on est dans le menu principal (playlist active)
        if self.sound and self.sound.state == 'stop':
            if hasattr(self, 'playlist') and self.playlist:
                self.jouer_musique_suivante()

    def aller_au_menu_principal(self, ecran_intro):
        # 1. On retire le splash
        self.main_layout.remove_widget(ecran_intro)
        self.initialiser_lecteur_musique()
        # 2. On remet tout visible avec un petit fondu
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.info_layout)
        anim.start(self.scroll_texte)
        anim.start(self.scroll_interaction)
        
         # Réaffiche le bouton paramètres s'il n'y est plus
        if self.btn_parametres not in self.info_layout.children:
            self.info_layout.add_widget(self.btn_parametres)

        if not self.nom_utilisateur:
            self.demander_nom_utilisateur()
        else:
            self.afficher_menu_principal_modes()
            
         # ___MENU PARAMÈTRES ___
    def ouvrir_menu_parametres(self, instance):
        if hasattr(self, 'layout_parametres') and self.layout_parametres in self.root.children:
            self.root.remove_widget(self.layout_parametres)
        self.layout_parametres = FloatLayout()
        
        # Fond noir semi-transparent ou opaque
        with self.layout_parametres.canvas.before:
            Color(0, 0, 0, 0.95) 
            self.rect_fond = Rectangle(size=(Window.width, Window.height), pos=(0, 0))
            
        # Titre des paramètres
        lbl_titre = Label(
            text="PARAMÈTRES DE L'APPLICATION",
            font_size='22sp',
            bold=True,
            size_hint=(1, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        self.layout_parametres.add_widget(lbl_titre)

        # Bouton : Modifier les informations (Nom, niveau, classe, âge, sexe)
        btn_modifier_infos = Button(
            text="Modifier mes informations personnelles",
            font_size='18sp',
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.75},
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_modifier_infos.bind(on_press=self.afficher_formulaire_modification_infos)
        self.layout_parametres.add_widget(btn_modifier_infos)

        # Bouton : Voir toutes les informations enregistrées
        btn_voir_infos = Button(
            text="Consulter mes données enregistrées",
            font_size='18sp',
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.62},
            background_color=(0.2, 0.7, 0.4, 1)
        )
        btn_voir_infos.bind(on_press=self.afficher_donnees_utilisateur)
        self.layout_parametres.add_widget(btn_voir_infos)

        # Bouton supplémentaire Pro : À propos / Version
        btn_pro = Button(
            text="À propos & Version Pro",
            font_size='18sp',
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.49},
            background_color=(0.6, 0.3, 0.8, 1)
        )
        btn_pro.bind(on_press=self.afficher_a_propos)

        self.layout_parametres.add_widget(btn_pro)

        # Bouton Fermer les paramètres pour revenir en arrière
        btn_fermer = Button(
            text="Fermer les Paramètres",
            font_size='18sp',
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.3},
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_fermer.bind(on_press=self.fermer_menu_parametres)
        self.layout_parametres.add_widget(btn_fermer)

        # Affichage par-dessus l'application
        self.root.add_widget(self.layout_parametres)

    def fermer_menu_parametres(self, instance):
        if hasattr(self, 'layout_parametres'):
            self.root.remove_widget(self.layout_parametres)
            del self.layout_parametres

    def afficher_donnees_utilisateur(self, instance):
        self.layout_parametres.clear_widgets()

        # Fond noir
        with self.layout_parametres.canvas.before:
            Color(0, 0, 0, 0.95)
            Rectangle(size=(Window.width, Window.height), pos=(0, 0))

        lbl_titre = Label(
            text="DONNÉES ENREGISTRÉES",
            font_size='22sp',
            bold=True,
            size_hint=(1, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        self.layout_parametres.add_widget(lbl_titre)

        recap_texte = (
            f"Nom : {self.nom_utilisateur}\n"
            f"Niveau : {self.niveau_utilisateur}\n"
            f"Classe : {self.classe_utilisateur}\n"
            f"Âge : {self.age_utilisateur}\n"
            f"Sexe : {self.sexe_utilisateur}"
        )
        
        lbl_data = Label(
            text=recap_texte,
            font_size='18sp',
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout_parametres.add_widget(lbl_data)

        # Bouton pour revenir au menu des paramètres
        btn_retour_param = Button(
            text="← Retour",
            font_size='18sp',
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.2},
            background_color=(0.75, 0.2, 0.2, 1)
        )
        # On rappelle l'ouverture du menu paramètres initial
        btn_retour_param.bind(on_press=self.ouvrir_menu_parametres)
        self.layout_parametres.add_widget(btn_retour_param)
        
        # ___SOUS-MENUS À-PROPOS ET VERSION ___      
    def afficher_a_propos(self, instance):
        # 1. On nettoie les boutons actuels des paramètres pour faire de la place (optionnel)
        self.layout_parametres.clear_widgets()
        
        # 2. On ajoute un Label pour afficher les infos
        lbl_info = Label(
            text="Math Quiz Comores\nVersion 1.0.0\nDéveloppé par Fazad Nassur\nTous droits réservés.",
            font_size='20sp',
            halign='center',
            valign='middle',
            size_hint=(0.8, None),
            height=dp(150),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        lbl_info.bind(texture_size=lambda instance, value: setattr(instance, 'text_size', value))
        self.layout_parametres.add_widget(lbl_info)
        
        # 3. Un bouton Retour pour revenir aux options des paramètres
        btn_retour_param = Button(
            text="Retour",
            font_size='18sp',
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.3},
            background_color=(0.75, 0.2, 0.2, 1)
        )
        btn_retour_param.bind(on_press=self.ouvrir_menu_parametres)
        self.layout_parametres.add_widget(btn_retour_param)

# ___INDICATEUR DE SAISIE ___
    def afficher_formulaire_modification_infos(self, instance):
        self.fermer_menu_parametres(None)
        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = 0.15
        self.scroll_interaction.size_hint_y = 0.85
        
        self.info_label.text = "Modifier vos informations"
        self.question_label.text = "Saisissez vos nouvelles informations ci-dessous :"

        # ___DICTIONNAIRE DE SAISIE ___     
        self.liste_niveaux_valides = [ "1ère année", "2ème année", "3ème année", "6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Terminale" ]
        self.liste_classes_valides = ["MPC", "PC", "SVT", "Collège", "Lycée"]

        # Champs de saisie (TextInput)
        self.input_nom = TextInput(text=str(getattr(self, 'nom_utilisateur', '')), hint_text="Nom d'utilisateur", size_hint_y=None, height=dp(50), background_color=(0.6, 0, 0.9, 0.8), multiline=False)
        
        self.input_niveau = TextInput(text=str(getattr(self, 'niveau_utilisateur', '')), hint_text="Classe(ex: 1ère année)", size_hint_y=None, height=dp(50), background_color=(0.6, 0, 0.9, 0.8), multiline=False)
        self.suggestions_niveau_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        
        self.input_classe = TextInput(text=str(getattr(self, 'classe_utilisateur', '')), hint_text="Niveau(ex: MPC)", size_hint_y=None, background_color=(0.6, 0, 0.9, 0.8), height=dp(50), multiline=False)
        self.suggestions_classe_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        
        self.input_age = TextInput(text=str(getattr(self, 'age_utilisateur', '')), hint_text="Âge", size_hint_y=None,background_color=(0.6, 0, 0.9, 0.8),  height=dp(50), multiline=False)
        self.input_sexe = TextInput(text=str(getattr(self, 'sexe_utilisateur', '')), hint_text="Sexe", size_hint_y=None,background_color=(0.6, 0, 0.9, 0.8),  height=dp(50), multiline=False)

        # Bouton Enregistrer
        btn_sauvegarder = Button(text="Enregistrer les modifications", font_size='18sp', bold=True, size_hint_y=None, height=dp(60), background_color=(0.2, 0.7, 0.4, 1))
        btn_sauvegarder.bind(on_press=self.sauvegarder_nouvelles_infos)

        btn_retour_menu = Button(text="← Retour au menu principal", font_size='18sp', bold=True, size_hint_y=None, height=dp(60), background_color=(0.75, 0.2, 0.2, 1))
        btn_retour_menu.bind(on_press=lambda x: self.afficher_menu_principal_modes())

        # Ajout des widgets dans l'ordre (avec les suggestions juste au-dessus des champs)
        self.interaction_layout.add_widget(self.input_nom)
        
        self.interaction_layout.add_widget(self.suggestions_niveau_layout)
        self.interaction_layout.add_widget(self.input_niveau)
        
        self.interaction_layout.add_widget(self.suggestions_classe_layout)
        self.interaction_layout.add_widget(self.input_classe)
        
        self.interaction_layout.add_widget(self.input_age)
        self.interaction_layout.add_widget(self.input_sexe)
        self.interaction_layout.add_widget(btn_sauvegarder)
        self.interaction_layout.add_widget(btn_retour_menu)

        # Bind pour écouter la saisie
        self.input_niveau.bind(text=self.mettre_a_jour_suggestions_niveau)
        self.input_classe.bind(text=self.mettre_a_jour_suggestions_classe)
        
    # ___MISE A JOUR DES SUGGESTIONS ___    
    def mettre_a_jour_suggestions_niveau(self, instance, valeur):
        self.suggestions_niveau_layout.clear_widgets()
        saisie = valeur.strip().lower()
        if not saisie:
            return
        for item in self.liste_niveaux_valides:
            if saisie in item.lower():
                btn = Button(text=f"Dire : {item}", size_hint_x=None, width=dp(150), background_color=(0.3, 0.5, 0.7, 1))
                btn.bind(on_release=lambda b, choix=item: self.selectionner_niveau(choix))
                self.suggestions_niveau_layout.add_widget(btn)

    def selectionner_niveau(self, choix):
        self.input_niveau.text = choix
        self.suggestions_niveau_layout.clear_widgets()

    def mettre_a_jour_suggestions_classe(self, instance, valeur):
        self.suggestions_classe_layout.clear_widgets()
        saisie = valeur.strip().lower()
        if not saisie:
            return
        for item in self.liste_classes_valides:
            if saisie in item.lower():
                btn = Button(text=f"Dire : {item}", size_hint_x=None, width=dp(150), background_color=(0.3, 0.5, 0.7, 1))
                btn.bind(on_release=lambda b, choix=item: self.selectionner_classe(choix))
                self.suggestions_classe_layout.add_widget(btn)

    def selectionner_classe(self, choix):
        self.input_classe.text = choix
        self.suggestions_classe_layout.clear_widgets()
        
     # ___SAUVEGARDE LOCALE NOUVELLE INFO ___
    def sauvegarder_nouvelles_infos(self, instance):
        niveau_saisi = self.input_niveau.text.strip()
        classe_saisie = self.input_classe.text.strip()

        if niveau_saisi not in self.liste_niveaux_valides:
            self.question_label.text = "Erreur : Veuillez sélectionner un niveau valide parmi les propositions."
            return

        if classe_saisie not in self.liste_classes_valides:
            self.question_label.text = "Erreur : Veuillez sélectionner une classe valide parmi les propositions."
            return
            
        self.nom_utilisateur = self.input_nom.text
        self.niveau_utilisateur = niveau_saisi
        self.classe_utilisateur = classe_saisie
        self.age_utilisateur = self.input_age.text
        self.sexe_utilisateur = self.input_sexe.text
        
        self.question_label.text = "Modifications enregistrées avec succès !"     
        self.sauvegarder_donnees_locales()
      
    def jouer_musique_fade_in(self, chemin_fichier):
        # 1. On arrête TOUT ce qui
        if self.sound:
            self.sound.stop()
            self.sound.unload()
        
        # 2. On charge la nouvelle musique dans le canal unique self.sound
        self.sound = SoundLoader.load(chemin_fichier)
        
        if self.sound:
            self.sound.volume = 0
            self.sound.play()
            Clock.schedule_interval(self.augmenter_volume, 0.2)
            print(f"Lecture en cours (Spéciale) : {os.path.basename(chemin_fichier)}")

    def augmenter_volume(self, dt):
        if self.sound and self.sound.volume < 1:
            self.sound.volume += 0.1
        else:
            return False
            
    def initialiser_playlist_question(self):
        # 1. Définir le chemin du dossier question
        dossier_q = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'musiques', 'question')
        
        if not os.path.exists(dossier_q):
            self.playlist_question = []
            return

        # 2. Récupérer tous les .ogg du dossier question et les trier par ordre alphabétique/numérique
        self.playlist_question = sorted([
            os.path.join(dossier_q, f) for f in os.listdir(dossier_q) 
            if f.endswith('.ogg') and os.path.isfile(os.path.join(dossier_q, f))
        ])
        
        self.index_playlist_q = 0
        
        if self.playlist_question:
            self.jouer_prochaine_musique_question()

    def jouer_prochaine_musique_question(self):
        if not self.playlist_question:
            return
            
        # Récupérer le morceau actuel dans l'ordre
        morceau = self.playlist_question[self.index_playlist_q]
        
        # Arrêter le son précédent
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            
        # Charger et jouer
        self.sound = SoundLoader.load(morceau)
        if self.sound:
            self.sound.volume = 0
            self.sound.play()
            Clock.schedule_interval(self.augmenter_volume, 0.2)
            print(f"Lecture en cours (Question) : {os.path.basename(morceau)}")
            
        # Passer au suivant pour la prochaine fois, et boucler si on arrive à la fin
        self.index_playlist_q = (self.index_playlist_q + 1) % len(self.playlist_question)

    def verifier_fin_musique_question(self, dt):
        # Vérifie si la musique est finie pour enchaîner la suivante dans le dossier question
        if self.sound and self.sound.state == 'stop':
            if hasattr(self, 'playlist_question') and self.playlist_question:
                self.jouer_prochaine_musique_question()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_text_size(self, instance, value):
        instance.text_size = value

    def nettoyer_boutons_bas(self):
        if self.btn_menu_persistant in self.main_layout.children:
            self.main_layout.remove_widget(self.btn_menu_persistant)
        if self.btn_retour_isole in self.main_layout.children:
            self.main_layout.remove_widget(self.btn_retour_isole)

    def action_retour_menu_persistant(self, instance):
        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.scroll_texte.clear_widgets()
        self.scroll_texte.add_widget(self.question_label)
        self.afficher_menu_principal_modes()

    # --- OBTENTION DU RANG ACTUEL ET CALCUL DES SEUILS PARTICULIERS (FORMULE +5% PAR COLORIS MAJORITAIRE) ---
    def determiner_rang_et_details(self):
        rp_restant = self.points_de_rang
        index_rang = 0
        seuil_actuel = 10.0
        
        for i in range(len(self.LISTE_RANGS)):
            index_rang = i
            palier_majeur = i // 5  
            seuil_actuel = 10.0 * (1.0 + (palier_majeur * 0.05))
            seuil_arrondi = max(1, int(round(seuil_actuel)))
            
            if rp_restant < seuil_arrondi:
                break
            else:
                rp_restant -= seuil_arrondi
                if i == len(self.LISTE_RANGS) - 1:
                    rp_restant = seuil_arrondi
                    break
                    
        palier_majeur_actuel = index_rang // 5
        seuil_suivant = max(1, int(round(10.0 * (1.0 + (palier_majeur_actuel * 0.05)))))
        
        return self.LISTE_RANGS[index_rang], int(rp_restant), seuil_suivant, index_rang

    def obtenir_rang_actuel(self):
        rang, _, _, _ = self.determiner_rang_et_details()
        return rang

    # --- SAUVEGARDE & PERSISTANCE ---
    def sauvegarder_donnees_locales(self):
        data = {
            "nom_utilisateur": self.nom_utilisateur,
            "classe_utilisateur": self.classe_utilisateur,
            "niveau_utilisateur": self.niveau_utilisateur,
            "age_utilisateur": self.age_utilisateur,
            "sexe_utilisateur": self.sexe_utilisateur,
            "score": self.score,
            "combo": self.combo,
            "niveau_actuel": self.niveau_actuel,
            "classe_actuelle": self.classe_actuelle,
            "mode_jeu": self.mode_jeu,
            "pile_chapitres_courants": self.pile_chapitres_courants,
            "examen_questions": self.examen_questions,
            "examen_index_actuel": self.examen_index_actuel,
            "temps_examen_restant": self.temps_examen_restant,
            "stats_chapitres": self.stats_chapitres,
            "xp": self.xp,
            "niveau_profil": self.niveau_profil,
            "points_de_rang": self.points_de_rang,
            "historique_scores": self.historique_scores,
            "file_attente_avis": self.file_attente_avis
        }
        try:
            with open(self.nom_fichier_sauvegarde, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception: pass

    def charger_donnees_locales(self):
        if os.path.exists(self.nom_fichier_sauvegarde):
            try:
                with open(self.nom_fichier_sauvegarde, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.nom_utilisateur = data.get("nom_utilisateur", "")
                self.niveau_utilisateur=data.get("niveau_utilisateur", "")
                self.classe_utilisateur=data.get("classe_utilisateur", "")
                self.sexe_utilisateur=data.get("sexe_utilisateur", "")
                self.age_utilisateur=data.get("age_utilisateur", "")
                self.score = data.get("score", 0)
                self.combo = data.get("combo", 0)
                self.niveau_actuel = data.get("niveau_actuel", "")
                self.classe_actuelle = data.get("classe_actuelle", "")
                self.mode_jeu = data.get("mode_jeu", "")
                self.pile_chapitres_courants = data.get("pile_chapitres_courants", [])
                self.examen_questions = data.get("examen_questions", [])
                self.examen_index_actuel = data.get("examen_index_actuel", 0)
                self.temps_examen_restant = data.get("temps_examen_restant", 300)
                self.xp = data.get("xp", 0)
                self.niveau_profil = data.get("niveau_profil", 1)
                self.points_de_rang = data.get("points_de_rang", 0)
                self.historique_scores = data.get("historique_scores", [])
                self.file_attente_avis = data.get("file_attente_avis", [])
                
                saved_stats = data.get("stats_chapitres", {})
                for k, v in saved_stats.items():
                    if k in self.stats_chapitres: self.stats_chapitres[k] = v
            except Exception: pass

    # --- ÉCRANS ET NAVIGATION ---
    def demander_nom_utilisateur(self):
        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.info_label.text = f"Créateur : {self.nom_developpeur}"
        self.question_label.text = f" Bienvenue sur Math Quiz Comores \n\nDéveloppé par : {self.nom_developpeur}\n\nEntre ton prénom pour t'enregistrer :"
        
        self.input_nom = TextInput(hint_text="Ton prénom ici...", multiline=False, size_hint_y=None, height=90, font_size='22sp')
        btn_valider_nom = Button(text="S'enregistrer et Continuer", size_hint_y=None, height=130, background_color=(0.12, 0.53, 0.9, 1), font_size='22sp', bold=True)
        btn_valider_nom.bind(on_press=self.sauvegarder_nouveau_nom)
        
        self.interaction_layout.add_widget(self.input_nom)
        self.interaction_layout.add_widget(btn_valider_nom)

    def sauvegarder_nouveau_nom(self, instance):
        nom_saisi = self.input_nom.text.strip()
        if nom_saisi:
            self.nom_utilisateur = nom_saisi
            self.sauvegarder_donnees_locales()
            self.afficher_menu_principal_modes()

    def afficher_menu_principal_modes(self):
           # Réaffiche le bouton paramètres s'il n'y est plus
        if self.btn_parametres not in self.info_layout.children:
            self.info_layout.add_widget(self.btn_parametres)

        self.arreter_chrono()
        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.chrono_label.text = ""
        self.interaction_layout.clear_widgets()
        
        rang_actuel = self.obtenir_rang_actuel()
        self.info_label.text = f"{self.nom_utilisateur}    LV:{self.niveau_profil}\n{rang_actuel}  XP:{self.xp}  RP:{self.points_de_rang}"
        self.question_label.text = f" Bienvenue sur Math Quiz, cher\n{self.nom_utilisateur} \n\nDéveloppeur officiel : {self.nom_developpeur}\n\nSélectionne une activité pour commencer :"
        
        layout_l1 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(90), spacing=dp(15))
        
        btn_entrainement = Button(text=" Entraînement Rythmé ", font_size='22sp', bold=True, background_color=(0.12, 0.28, 0.48, 1), size_hint=(1,None), height=dp(90))
        btn_entrainement.bind(on_press=lambda x: self.selectionner_mode("Entraînement"))
        layout_l1.add_widget(btn_entrainement)
        
        btn_examen = Button(text="Examen Blanc ", font_size='22sp', bold=True, background_color=(0.12, 0.28, 0.48, 1), size_hint_y=None, height=dp(90))
        btn_examen.bind(on_press=lambda x: self.selectionner_mode("Examen"))
        layout_l1.add_widget(btn_examen)
        
        self.interaction_layout.add_widget(layout_l1)
        
        layout_l2 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(90), spacing=dp(15))
        btn_jouer_4 = Button(text="Joue jusqu'à 4", font_size='22sp', bold=True, background_color=(0.12, 0.28, 0.48, 1))
        btn_jouer_4.bind(on_press=self.afficher_sous_menu_joueurs)
        layout_l2.add_widget(btn_jouer_4)

        
        btn_stats = Button(text=" Salle des Rangs\n & Statistiques", font_size='22sp', bold=True, background_color=(0.12, 0.28, 0.48, 1), size_hint_y=None, height=dp(90))
        btn_stats.bind(on_press=self.afficher_sous_menu_evolution)
        layout_l2.add_widget(btn_stats)    
        self.interaction_layout.add_widget(layout_l2)

        btn_avis_general = Button(text="Laisser un avis au Développeur", font_size='22sp', bold=True, background_color=(0.85, 0.65, 0.13, 1), size_hint=(1, None), height=dp(90))
        btn_avis_general.bind(on_press=self.afficher_interface_avis_general)
        self.interaction_layout.add_widget(btn_avis_general)
        
        layout_l3 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(90), spacing=dp(15))
        btn_niveaux_activites = Button(text="Niveaux d'Activités", font_size='22sp', bold=True, background_color=(0.12, 0.28, 0.48, 1))
        btn_niveaux_activites.bind(on_press=self.afficher_sous_menu_niveaux_activites)
        layout_l3.add_widget(btn_niveaux_activites)
   
        btn_sujets = Button(text="Sujets Casse-Tête", font_size='22sp', bold=True, background_color=(0.12, 0.28, 0.48, 1))
        btn_sujets.bind(on_press=self.afficher_sous_menu_sujets_casse_tete)
        layout_l3.add_widget(btn_sujets)
        self.interaction_layout.add_widget(layout_l3)
        
        layout_l4 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(90), spacing=dp(15))
        layout_l4.add_widget(Button(text='bientôt disponible', font_size='22sp', bold=True, background_color=(0.25, 0.25, 0.25, 1)))
        layout_l4.add_widget(Button(text='bientôt disponible', font_size='22sp', bold=True, background_color=(0.25, 0.25, 0.25, 1)))
        self.interaction_layout.add_widget(layout_l4)
        
        btn_autres = Button(text='Autres bientot disponible', font_size='22sp', bold=True, size_hint=(1, None), height=dp(90), background_color=(0.25, 0.25, 0.25, 1))
        self.interaction_layout.add_widget(btn_autres)
        
        #___SOUS-MENUS DES NIVEAUX___      
    def obtenir_index_palier_requis(self, nom_activite):
                # Retire le bouton paramètres
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        # Dictionnaire mis à jour pour les 16 activités
        seuils_rangs = {
            "Calcul Mental Éclair": "Bronze I ",
            "Arithmétique de Base": "Bronze III ",
            "Fractions & Proportions": "Argent I ",
            "Équations du 1er Degré": "Argent III ",
            "Puissances & Racines": "Or I ",
            "Identités Remarquables": "Or III ",
            "Systèmes Linéaires": "Platine I ",
            "Dérivation & Limites": "Platine III ",
            "Nombres Complexes": "Diamant I ",
            "Calcul Intégral": "Diamant III ",
            "Mécanique du Point": "Héroïque I ",
            "Thermodynamique Appliquée": "Maître I ",
            "Optique Géométrique": "Grand Maître I ",
            "Électrostatique Avancée": "Master I ",
            "Théorèmes Vectoriels Complexes": "Grand Master I ",
            "Physique Quantique 101": "Leadership "
        }
        nom_rang_requis = seuils_rangs.get(nom_activite, "Bronze I ")
        try:
            return self.LISTE_RANGS.index(nom_rang_requis)
        except ValueError:
            return 0

    def afficher_sous_menu_niveaux_activites(self, instance):
        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.16
        self.scroll_interaction.size_hint_y = 0.84
        self.interaction_layout.clear_widgets()

        self.info_label.text = "Niveaux d'Activités"
        self.question_label.text = f"Progresse pour débloquer tes 16 activités, {self.nom_utilisateur} :"

        _, _, _, index_grade_actuel = self.determiner_rang_et_details()

        liste_16_activites = [
            "Calcul Mental Éclair", "Arithmétique de Base", "Fractions & Proportions",
            "Équations du 1er Degré", "Puissances & Racines", "Identités Remarquables",
            "Systèmes Linéaires", "Dérivation & Limites", "Nombres Complexes",
            "Calcul Intégral", "Mécanique du Point", "Thermodynamique Appliquée",
            "Optique Géométrique", "Électrostatique Avancée", "Théorèmes Vectoriels Complexes",
            "Physique Quantique 101"
        ]

        # On calcule dynamiquement la hauteur nécessaire pour loger les 16 blocs 
        hauteur_totale = (len(liste_16_activites) // 2) * dp(90)
        
        grille_activites = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=hauteur_totale)

        for activite in liste_16_activites:
            index_requis = self.obtenir_index_palier_requis(activite)
            est_debloque = index_grade_actuel >= index_requis

            if est_debloque:
                btn = Button(text=f"✔ {activite}", font_size='14sp', bold=True, background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(80))
                btn.bind(on_press=lambda x, act=activite: self.lancer_activite_niveau(act))
            else:
                nom_rang_nom = self.LISTE_RANGS[index_requis].strip()
                btn = Button(text=f"🔒 {activite}\n[Requis: {nom_rang_nom}]", font_size='12sp', bold=True, background_color=(0.3, 0.3, 0.3, 1), size_hint_y=None, height=dp(80))
                btn.bind(on_press=lambda x, r=nom_rang_nom: self.alerte_activite_verrouillee(r))

            grille_activites.add_widget(btn)

        # On ajuste la hauteur du layout d'interaction pour que le ScrollView permette de tout faire défiler
        self.interaction_layout.height = hauteur_totale + dp(120)
        self.interaction_layout.add_widget(grille_activites)

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())
        self.interaction_layout.add_widget(btn_retour)
        
    def lancer_activite_niveau(self, nom_activite):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Activité : {nom_activite}"
        self.question_label.text = f"Session de l'activité '{nom_activite}' lancée avec succès.\nBonne concentration !"
        
        btn_retour = Button(text="← Retour aux niveaux", font_size='22sp', bold=True, background_color=(0.12, 0.53, 0.9, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=self.afficher_sous_menu_niveaux_activites)
        self.interaction_layout.add_widget(btn_retour)
    
    def alerte_activite_verrouillee(self, rang_requis):
        self.question_label.text = f"ACTIVITÉ VERROUILLÉE !\n\nTu dois atteindre au minimum le grade '{rang_requis}' pour débloquer cette option. Améliore ton rang !"
        
     #___SOUS-MENUS DES SUJETS CASSE-TÊTE ___   
    def afficher_sous_menu_sujets_casse_tete(self, instance):
                # Retire le bouton paramètres
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.interaction_layout.clear_widgets()
        self.info_label.text = "Sujets Casse-Tête"
        self.question_label.text = f"Prépare tes neurones, {self.nom_utilisateur}. Sélectionne un défi logique :"

        btn_paradoxes = Button(text="Paradoxes Mathématiques", font_size='22sp', bold=True, background_color=(0.55, 0.3, 0.75, 1), size_hint_y=None, height=dp(90))
        btn_paradoxes.bind(on_press=lambda x: self.lancer_sujet_casse_tete("Paradoxes"))

        btn_enigmes = Button(text="Énigmes Algébriques", font_size='22sp', bold=True, background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(90))
        btn_enigmes.bind(on_press=lambda x: self.lancer_sujet_casse_tete("Énigmes"))

        btn_geometrie = Button(text="Défis Géométriques Poussés", font_size='22sp', bold=True, background_color=(0.85, 0.65, 0.13, 1), size_hint_y=None, height=dp(90))
        btn_geometrie.bind(on_press=lambda x: self.lancer_sujet_casse_tete("Géométrie"))

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())

        self.interaction_layout.add_widget(btn_paradoxes)
        self.interaction_layout.add_widget(btn_enigmes)
        self.interaction_layout.add_widget(btn_geometrie)
        self.interaction_layout.add_widget(btn_retour)

    def lancer_sujet_casse_tete(self, type_defi):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Défi : {type_defi}"
        self.question_label.text = f"Le module spécial '{type_defi}' est en cours de déploiement pour propulser ton niveau vers les sommets."
        
        btn_retour = Button(text="← Retour aux sujets", font_size='22sp', bold=True, background_color=(0.12, 0.53, 0.9, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=self.afficher_sous_menu_sujets_casse_tete)
        self.interaction_layout.add_widget(btn_retour)
        
     #___SOUS-MENUS MODE MULTIJOUEURS___
    def afficher_sous_menu_joueurs(self, instance):
                # Retire le bouton paramètres 
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.interaction_layout.clear_widgets()
        self.info_label.text = "Mode Multijoueur"
        self.question_label.text = f"Choisis le nombre de participants pour cette session, {self.nom_utilisateur} :"

        btn_2p = Button(text="2 Joueurs", font_size='22sp', bold=True, background_color=(0.2, 0.5, 0.8, 1), size_hint_y=None, height=dp(90))
        btn_2p.bind(on_press=lambda x: self.lancer_mode_multijoueur(2))

        btn_3p = Button(text="3 Joueurs", font_size='22sp', bold=True, background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(90))
        btn_3p.bind(on_press=lambda x: self.lancer_mode_multijoueur(3))

        btn_4p = Button(text="4 Joueurs", font_size='22sp', bold=True, background_color=(0.85, 0.65, 0.13, 1), size_hint_y=None, height=dp(90))
        btn_4p.bind(on_press=lambda x: self.lancer_mode_multijoueur(4))

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())

        self.interaction_layout.add_widget(btn_2p)
        self.interaction_layout.add_widget(btn_3p)
        self.interaction_layout.add_widget(btn_4p)
        self.interaction_layout.add_widget(btn_retour)
        
    def lancer_mode_multijoueur(self, nombre_joueurs):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Mode {nombre_joueurs} Joueurs"
        self.question_label.text = f"Le mode multijoueur local pour {nombre_joueurs} joueurs est en cours de configuration.\nPrépare-toi à en découdre !"
        
        btn_retour = Button(text="← Retour au menu", font_size='22sp', bold=True, background_color=(0.12, 0.53, 0.9, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=self.afficher_sous_menu_joueurs)
        self.interaction_layout.add_widget(btn_retour)


    # --- SOUS-MENUS DU PANNEAU D'ÉVOLUTION ---
    def afficher_sous_menu_evolution(self, instance):
                # Retire le bouton paramètres
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.interaction_layout.clear_widgets()
        self.info_label.text = " Menu Évolution"
        self.question_label.text = f"Mon cher {self.nom_utilisateur}, bienvenue dans ton espace de suivi.\nSélectionne la section à consulter :"

        btn_profil_rangs = Button(text=" Mon Grade, XP & Rythme Actuel", font_size='22sp', bold=True, background_color=(0.2, 0.5, 0.8, 1), size_hint_y=None, height=dp(90))
        btn_profil_rangs.bind(on_press=self.afficher_tableau_de_bord_stats)

        btn_liste_grades = Button(text=" Liste Officielle des Rangs", font_size='22sp', bold=True, background_color=(0.55, 0.3, 0.75, 1), size_hint_y=None, height=dp(90))
        btn_liste_grades.bind(on_press=self.afficher_liste_complete_des_rangs)

        btn_modules_maitrise = Button(text=" Maîtrise des Chapitres", font_size='22sp', bold=True, background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(90))
        btn_modules_maitrise.bind(on_press=self.afficher_maitrise_des_modules)

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())

        self.interaction_layout.add_widget(btn_profil_rangs)
        self.interaction_layout.add_widget(btn_liste_grades)
        self.interaction_layout.add_widget(btn_modules_maitrise)
        self.interaction_layout.add_widget(btn_retour)

    def afficher_liste_complete_des_rangs(self, instance):
        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.scroll_texte.clear_widgets()
        
        # Maximiser la zone supérieure de texte et réduire l'interaction
        self.scroll_texte.size_hint_y = 1.0
        self.scroll_interaction.size_hint_y = None
        self.scroll_interaction.height = 0
        
        self.info_label.text = " Hiérarchie des Grades"
        
        layout_liste_scroll = BoxLayout(orientation='vertical', size_hint=(1,None), spacing=dp(8), padding=dp(15))
        layout_liste_scroll.bind(minimum_height=layout_liste_scroll.setter('height'))

        lbl_intro = Label(text="Hiérarchie dynamique indexée sur les bonus de paliers (+5% RP requis par couleur) :", font_size='18sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1,None), height=dp(80))
        lbl_intro.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
        layout_liste_scroll.add_widget(lbl_intro)

        for rg in self.LISTE_RANGS:
            lbl_rg = Label(text=f"• {rg}", font_size='20sp', halign='left', size_hint=(1,None), height=dp(55))
            lbl_rg.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 20, None)))
            layout_liste_scroll.add_widget(lbl_rg)

        self.scroll_texte.add_widget(layout_liste_scroll)

        # Bouton placé directement tout en bas de l'écran principal
        self.btn_retour_isole.text = "← Retour Évolution"
        self.btn_retour_isole.bind(on_press=self.restaurer_ecran_initial_apres_stats)
        self.main_layout.add_widget(self.btn_retour_isole)

    def afficher_maitrise_des_modules(self, instance):
        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.scroll_texte.clear_widgets()
        
        # Maximiser la zone supérieure de texte et réduire l'interaction
        self.scroll_texte.size_hint_y = 1.0
        self.scroll_interaction.size_hint_y = None
        self.scroll_interaction.height = 0
        
        self.info_label.text = "Maîtrise des Chapitres"

        layout_modules_scroll = BoxLayout(orientation='vertical', size_hint=(1,None), spacing=dp(8), padding=dp(15))
        layout_modules_scroll.bind(minimum_height=layout_modules_scroll.setter('height'))

        lbl_titre = Label(text="Suivi complet par module officiel :", font_size='20sp', bold=True, size_hint=(1,None), height=dp(55), color=(0.9, 0.9, 0.9, 1))
        layout_modules_scroll.add_widget(lbl_titre)

        aucun_suivi = True
        for chap, valeurs in self.stats_chapitres.items():
            reussites, total = valeurs[0], valeurs[1]
            if total > 0:
                aucun_suivi = False
                taux = (reussites / total) * 100
                box_item = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), spacing=dp(5))
                lbl_item = Label(text=f"• {chap} : {reussites}/{total} Corrects", font_size='18sp', halign='left')
                lbl_item.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
                pb = ProgressBar(max=100, value=taux, size_hint=(1,None), height=dp(25))
                box_item.add_widget(lbl_item)
                box_item.add_widget(pb)
                layout_modules_scroll.add_widget(box_item)

        if aucun_suivi:
            lbl_vide = Label(text="Aucune statistique enregistrée pour le moment.\nCommence une partie !", font_size='20sp', halign='center', size_hint=(1,None), height=dp(150), color=(0.6, 0.6, 0.6, 1))
            layout_modules_scroll.add_widget(lbl_vide)

        self.scroll_texte.add_widget(layout_modules_scroll)

        # Bouton placé directement tout en bas de l'écran principal
        self.btn_retour_isole.text = "← Retour Évolution"
        self.btn_retour_isole.bind(on_press=self.restaurer_ecran_initial_apres_stats)
        self.main_layout.add_widget(self.btn_retour_isole)
        
     # ___SOUS-MENUS DES AVIS GÉNÉRAL ___
    def afficher_interface_avis_general(self, instance):
                # Retire le bouton paramètres
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = 0.22
        self.scroll_interaction.size_hint_y = 0.78
        self.info_label.text = "Retour Développeur"
        self.question_label.text = f"Mon cher ami {self.nom_utilisateur}, dis-moi ce que je devrais modifier ou ajouter dans mon application, et laisse ton numéro WhatsApp pour plus de communication, merci :"
        
        self.input_avis_global = TextInput(hint_text="Écris tes remarques ici...", background_color=(0.6, 0, 0.9, 0.8), multiline=True, size_hint_y=None, height=dp(300), font_size='18sp')
        self.input_whatsapp_global = TextInput(hint_text="Ton numéro WhatsApp (Optionnel)...", multiline=False, background_color=(0.6, 0, 0.9, 0.8),  size_hint_y=None, height=dp(100), font_size='18sp')
        
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(90), spacing=dp(15))
        btn_annuler = Button(text="Annuler", background_color=(0.75, 0.2, 0.2, 1), font_size='22sp', bold=True)
        btn_annuler.bind(on_press=lambda x: self.afficher_menu_principal_modes())
        
        btn_envoyer = Button(text="Envoyer l'avis", background_color=(0.2, 0.65, 0.4, 1), font_size='22sp', bold=True)
        btn_envoyer.bind(on_press=self.preparer_avis_general_local)
        
        btn_box.add_widget(btn_annuler)
        btn_box.add_widget(btn_envoyer)
        
        self.interaction_layout.add_widget(self.input_avis_global)
        self.interaction_layout.add_widget(self.input_whatsapp_global)
        self.interaction_layout.add_widget(btn_box)

    def preparer_avis_general_local(self, instance):
        texte_saisi = self.input_avis_global.text.strip()
        num_wa = self.input_whatsapp_global.text.strip()
        if texte_saisi:
            message_formate = f"[AVIS GÉNÉRAL ACCUEIL] [WhatsApp: {num_wa}] -> {texte_saisi}"
            
            # Ajout dans le dictionnaire interne unique, prêt pour la mise en queue
            avis_dict = {
                "user": self.nom_utilisateur,
                "msg": message_formate
            }
            self.file_attente_avis.append(avis_dict)
            self.sauvegarder_donnees_locales()
            
            # Essai d'envoi immédiat
            self.tenter_synchronisation_file_attente(0)
            
        self.afficher_menu_principal_modes()

    def selectionner_mode(self, mode):
        self.mode_jeu = mode
        self.sauvegarder_donnees_locales()
        self.afficher_menu_niveaux()
        
    # ___MENU POUR LE CHOIX DES NIVEAUX ___
    def afficher_menu_niveaux(self):
                # Retire le bouton paramètres
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.info_label.text = f"Mode : {self.mode_jeu}\nChoix du Cycle"
        self.question_label.text = "Sélectionne ta catégorie d'étude :"
        
        niveaux = {
            "Cycle Collège (6ème à 3ème)": ["6ème", "5ème", "4ème", "3ème"], 
            "Cycle Lycée (2nde à Terminale)": ["2nde", "1ere", "Terminale"],
            " Université (Comores MPC)": ["L1 MPC"]
        }
        
        for nv in niveaux.keys():
            btn = Button(text=nv, font_size='22sp', background_color=(0.15, 0.45, 0.75, 1), size_hint_y=None, height=dp(90))
            btn.bind(on_press=lambda inst, n=nv, list_cl=niveaux[nv]: self.afficher_menu_classes(n, list_cl))
            self.interaction_layout.add_widget(btn)

        btn_retour = Button(text="← Revenir à l'Accueil", size_hint_y=None, height=dp(90), font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())
        self.interaction_layout.add_widget(btn_retour)
        
     # ___SOUS-MENUS DE CHOIX DES CLASSES ___
    def afficher_menu_classes(self, niveau, list_cl):
                # Retire le bouton paramètres 
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.question_label.text = f"Sélectionne la classe pour charger le programme associé :"
        
        for cl in list_cl:
            btn = Button(text=cl, font_size='22sp', background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(90))
            btn.bind(on_press=self.initialiser_session_classe)
            self.interaction_layout.add_widget(btn)

        btn_retour = Button(text="← Étape Précédente", size_hint_y=None, height=dp(90), font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_niveaux())
        self.interaction_layout.add_widget(btn_retour)

    def initialiser_session_classe(self, instance):
        self.classe_actuelle = instance.text
        self.combo = 0
        self.score = 0  
        self.pile_chapitres_courants = []
        self.sauvegarder_donnees_locales()
        
        # --- PRÉPARATION DE L'ARCHITECTURE SERVEUR ---
        #  effectuer l'envoi vers l'API d'historique centralisée locale ou distante
        url_sauvegarde_serveur = "https://FazadNassur.pythonanywhere.com/api/sauvegarde"
        data_json = json.dumps({"user": self.nom_utilisateur, "classe": self.classe_actuelle, "points": self.points_de_rang})
        headers_api = {'Content-type': 'application/json', 'Accept': 'application/json'}
        
        # Envoi asynchrone transparent (l'application ne freeze pas si le serveur est indisponible)
        UrlRequest(url_sauvegarde_serveur, req_body=data_json, req_headers=headers_api, timeout=4, 
                   on_success=lambda req, res: print("Données synchronisées sur le serveur."),
                   on_failure=lambda req, res: print("Serveur inaccessible, sauvegarde locale conservée."),
                   on_error=lambda req, res: print("Erreur réseau."))
                   
        self.initialiser_playlist_question()
        Clock.unschedule(self.verifier_fin_musique_question) 
        Clock.schedule_interval(self.verifier_fin_musique_question, 1)
              
        if self.mode_jeu == "Examen":
            liste_chapitres = list(self.progression_officielle[self.classe_actuelle])
            while len(liste_chapitres) < 10:
                liste_chapitres += list(self.progression_officielle[self.classe_actuelle])
            random.shuffle(liste_chapitres)
            self.examen_questions = liste_chapitres[:10]
            self.examen_index_actuel = 0
            self.examen_reponses_eleve = []
            self.temps_examen_restant = 300 
            self.sauvegarder_donnees_locales()
            self.lancer_chrono_examen_global()
            self.generer_question_examen()
        else:
            self.generer_question_dynamique()

    # --- ÉCRAN DU FORMULAIRE DE COURS ---
    def afficher_formulaire_cours(self, instance):
        self.arreter_chrono()
        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.scroll_texte.clear_widgets()
        
        # Maximisation de la zone supérieure de texte et réduire l'interaction
        self.scroll_texte.size_hint_y = 1.0
        self.scroll_interaction.size_hint_y = None
        self.scroll_interaction.height = 0
        
        self.info_label.text = f" Formulaire de Cours\nClasse : {self.classe_actuelle}"
        self.chrono_label.text = ""
        
        contenu_cours = self.formulaire_cours.get(self.classe_actuelle, "Aucun résumé disponible pour cette classe.")
        
        lbl_cours = Label(text=contenu_cours, font_size='20sp', size_hint_y=None, halign='left', valign='top', color=(0.9, 0.9, 0.9, 1))
        lbl_cours.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 20, None)))
        lbl_cours.bind(texture_size=lambda inst, size: setattr(inst, 'height', max(size[1] + 60, 500)))
        
        self.scroll_texte.add_widget(lbl_cours)
        
        # Bouton placé directement tout en bas de l'écran principal
        self.btn_retour_isole.text = "← Retour au Quiz"
        self.btn_retour_isole.bind(on_press=self.retourner_au_quiz_apres_cours)
        self.main_layout.add_widget(self.btn_retour_isole)

    def retourner_au_quiz_apres_cours(self, instance):
        self.scroll_texte.clear_widgets()
        self.scroll_texte.add_widget(self.question_label)
        
        # Restaurer les proportions pour le jeu
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        
        if self.mode_jeu == "Examen":
            self.lancer_chrono_examen_global()
            self.generer_question_examen()
        else:
            self.generer_question_dynamique()

    # --- GESTION DU TEMPS RÈGLEMENTAIRE ---
    def lancer_chrono_entrainement(self):
        self.arreter_chrono()
        self.temps_restant = 60
        self.temps_debut_question = Clock.get_time()
        self.chrono_label.text = f"{self.temps_restant}s"
        self.evenement_chrono = Clock.schedule_interval(self.mettre_a_jour_chrono_entrainement, 1.0)

    def mettre_a_jour_chrono_entrainement(self, dt):
        self.temps_restant -= 1
        self.chrono_label.text = f"{self.temps_restant}s"
        if self.temps_restant <= 0:
            self.arreter_chrono()
            self.interaction_layout.clear_widgets()
            self.combo = max(0, self.combo - 2)
            self.points_de_rang = max(0, self.points_de_rang - 3)
            self.enregistrer_statistique_reponse(self.chapitre_en_cours, False)
            self.question_label.text = f" TEMPS ÉCOULÉ !\n\nLa bonne réponse attendue était : {self.bonne_reponse}."
            self.creer_interface_suivante()

    def lancer_chrono_examen_global(self):
        self.arreter_chrono()
        self.chrono_label.text = f" {self.temps_examen_restant // 60:02d}:{self.temps_examen_restant % 60:02d}"
        self.evenement_chrono = Clock.schedule_interval(self.mettre_a_jour_chrono_examen, 1.0)

    def mettre_a_jour_chrono_examen(self, dt):
        self.temps_examen_restant -= 1
        if self.temps_examen_restant % 5 == 0: self.sauvegarder_donnees_locales()
            
        mins = self.temps_examen_restant // 60
        secs = self.temps_examen_restant % 60
        self.chrono_label.text = f" {mins:02d}:{secs:02d}"
        if self.temps_examen_restant <= 0:
            self.arreter_chrono()
            self.terminer_et_afficher_bilan_examen()

    def arreter_chrono(self):
        if self.evenement_chrono:
            Clock.unschedule(self.evenement_chrono)
            self.evenement_chrono = None

    def enregistrer_statistique_reponse(self, chapitre, est_correct):
        if chapitre in self.stats_chapitres:
            self.stats_chapitres[chapitre][1] += 1
            if est_correct:
                self.stats_chapitres[chapitre][0] += 1
                self.xp += 10
                xp_requis = self.niveau_profil * 50
                while self.xp >= xp_requis:
                    self.xp -= xp_requis
                    self.niveau_profil += 1
                        
        self.sauvegarder_donnees_locales()

    # --- AFFICHAGE DU MODULE INDIVIDUEL : NOTATION, COMPÉTITION & RYTHME ---
    def afficher_tableau_de_bord_stats(self, instance):
        self.arreter_chrono()
        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.scroll_texte.clear_widgets()
        
        # Maximiser la zone supérieure de texte et réduire l'interaction
        self.scroll_texte.size_hint_y = 1.0
        self.scroll_interaction.size_hint_y = None
        self.scroll_interaction.height = 0
        
        self.info_label.text = f" Profil de Compétition"
        self.chrono_label.text = ""
        
        layout_stats_scroll = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(20), padding=dp(15))
        layout_stats_scroll.bind(minimum_height=layout_stats_scroll.setter('height'))
        
        rang_actuel, rp_courant, seuil_requis, _ = self.determiner_rang_et_details()
        lbl_rang_titre = Label(text=f"GRADE DE SAISON : {rang_actuel}\n SCORE DE RANG : {self.points_de_rang} PR", 
                               font_size='22sp', bold=True, size_hint=(1,None), height=dp(100), halign='center', color=(1, 0.84, 0, 1))
        lbl_rang_titre.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
        layout_stats_scroll.add_widget(lbl_rang_titre)
        
        jauge_interactive = BoxLayout(size_hint=(1, None), height=dp(60))
        with jauge_interactive.canvas.before:
            Color(0.2, 0.2, 0.25, 1)
            self.bg_bar = Rectangle(pos=(jauge_interactive.pos[0] + 20, jauge_interactive.pos[1] + 10), size=(jauge_interactive.size[0] - 40, 40))
            Color(1, 0.45, 0, 1)
            ratio_f = min(1.0, float(rp_courant) / float(seuil_requis))
            largeur_remplissage = (jauge_interactive.size[0] - 40) * ratio_f
            self.fill_bar = Rectangle(pos=(jauge_interactive.pos[0] + 20, jauge_interactive.pos[1] + 10), size=(largeur_remplissage, 40))
            
        def rafraichir_jauge(inst, val):
            _, r_c, s_r, _ = self.determiner_rang_et_details()
            self.bg_bar.pos = (inst.pos[0] + 20, inst.pos[1] + 10)
            self.bg_bar.size = (inst.size[0] - 40, 40)
            self.fill_bar.pos = (inst.pos[0] + 20, inst.pos[1] + 10)
            rat = min(1.0, float(r_c) / float(s_r))
            self.fill_bar.size = ((inst.size[0] - 40) * rat, 40)
            
        jauge_interactive.bind(pos=rafraichir_jauge, size=rafraichir_jauge)
        
        lbl_points_restants = Label(text=f" {seuil_requis - rp_courant} PR avant le prochain Échelon !", font_size='18sp', color=(0.2, 0.8, 1, 1), size_hint=(1,None), height=dp(45))
        layout_stats_scroll.add_widget(jauge_interactive)
        layout_stats_scroll.add_widget(lbl_points_restants)
        
        xp_requis = self.niveau_profil * 50
        box_xp = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(100), spacing=dp(8))
        lbl_xp = Label(text=f"Niveau du Profil : Lvl {self.niveau_profil} ({self.xp} / {xp_requis} XP)", font_size='18sp', bold=True)
        pb_xp = ProgressBar(max=xp_requis, value=self.xp, size_hint_y=None, height=25)
        box_xp.add_widget(lbl_xp)
        box_xp.add_widget(pb_xp)
        layout_stats_scroll.add_widget(box_xp)
        
        lbl_analyse_vitesse = Label(size_hint_y=None, font_size='18sp', bold=True, halign='center')
        lbl_analyse_vitesse.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
        lbl_analyse_vitesse.bind(texture_size=lambda inst, size: setattr(inst, 'height', max(size[1] + 30, 100)))
        
        if len(self.historique_scores) < 2:
            lbl_analyse_vitesse.text = "ANALYSE : En attente d'enseignements.\nEnchaîne des sessions de quiz pour tracer ta courbe !"
            lbl_analyse_vitesse.color = (0.7, 0.7, 0.7, 1)
        else:
            derniers = self.historique_scores[-5:]
            if all(derniers[i] < derniers[i+1] for i in range(len(derniers)-1)):
                lbl_analyse_vitesse.text = " RYTHME : ÉVOLUTION GÉOMÉTRIQUE !\nTu massacres le classement. Tes performances augmentent de façon fulgurante."
                lbl_analyse_vitesse.color = (0.3, 0.9, 0.5, 1)
            elif all(derniers[i] > derniers[i+1] for i in range(len(derniers)-1)):
                lbl_analyse_vitesse.text = "SÉRIE DE DÉFAITES : CHUTE DE SÉCURITÉ !\nAttention , tu perds des points de rang. Révise tes fiches."
                lbl_analyse_vitesse.color = (1, 0.3, 0.3, 1)
            else:
                lbl_analyse_vitesse.text = "TRAJECTOIRE : CONSTANTE ET STABLE.\nTon niveau actuel est parfaitement ancré."
                lbl_analyse_vitesse.color = (0.2, 0.6, 1, 1)
        layout_stats_scroll.add_widget(lbl_analyse_vitesse)
        
        btn_regles_rang = Button(text="ℹ Comment fonctionne le système de Rang ?", size_hint=(1, None), height=dp(50), background_color=(0.2, 0.2, 0.25, 1), font_size='18sp')
        btn_regles_rang.bind(on_press=self.afficher_explication_rangs_pop)
        layout_stats_scroll.add_widget(btn_regles_rang)
                
        self.scroll_texte.add_widget(layout_stats_scroll)
        
        # Bouton placé directement tout en bas de l'écran principal
        self.btn_retour_isole.text = "← Retour Évolution"
        self.btn_retour_isole.bind(on_press=self.restaurer_ecran_initial_apres_stats)
        self.main_layout.add_widget(self.btn_retour_isole)

    def afficher_explication_rangs_pop(self, instance):
        self.nettoyer_boutons_bas()
        self.scroll_texte.clear_widgets()
        
        # S'assurer de garder l'affichage maximisé
        self.scroll_texte.size_hint_y = 1.0
        self.scroll_interaction.size_hint_y = None
        self.scroll_interaction.height = 0
        
        texte_explicatif = (
            "SYSTÈME DE RANGS MATH QUIZ COMORES\n\n"
            "Chaque tranche de points de Compétition (PR) requis augmente de +5% à chaque changement global de couleur de grade.\n\n"
            "COMMENT GAGNER DES POINTS ?\n"
            "1. Répondre correctement et rapidement en Entraînement (+2 PR).\n"
            "2. Enchaîner les victoires (Combo) augmente tes gains.\n"
            "3. Décrocher une excellente moyenne en Examen Blanc (+6 PR).\n\n"
            "ATTENTION : Une mauvaise réponse ou un chrono expiré te fait perdre des points (-3 PR) !"
        )
        lbl_info = Label(text=texte_explicatif, font_size='18sp', size_hint_y=None, halign='left', valign='top')
        lbl_info.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 20, None)))
        lbl_info.bind(texture_size=lambda inst, size: setattr(inst, 'height', max(size[1] + 60, 500)))
        self.scroll_texte.add_widget(lbl_info)
        
        # Le bouton retour unique reste ancré tout en bas
        self.btn_retour_isole.text = "← Retour Évolution"
        self.btn_retour_isole.bind(on_press=self.restaurer_ecran_initial_apres_stats)
        self.main_layout.add_widget(self.btn_retour_isole)

    def restaurer_ecran_initial_apres_stats(self, instance):
        self.scroll_texte.clear_widgets()
        self.scroll_texte.add_widget(self.question_label)
        
        # Réinitialisation des proportions normales avant d'ouvrir le sous-menu
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        
        self.afficher_sous_menu_evolution(None)

    # --- PROCESSUS ENTRAÎNEMENT RYTHMÉ ---
    def generer_question_dynamique(self):
                # Retire le bouton paramètres
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.interaction_layout.clear_widgets()
        
        # Sécurité proportions
        self.scroll_texte.size_hint_y = 0.22
        self.scroll_interaction.size_hint_y = 0.78
        
        try: idx_actuel = self.ordre_classes.index(self.classe_actuelle)
        except ValueError: idx_actuel = 0
            
        if idx_actuel > 0 and random.random() < 0.30:
            classes_inferieures = self.ordre_classes[:idx_actuel]
            poids = [2**i for i in range(len(classes_inferieures))]
            classe_cible = random.choices(classes_inferieures, weights=poids, k=1)[0]
            chapitre_cible = random.choice(self.progression_officielle[classe_cible])
        else:
            classe_cible = self.classe_actuelle
            if not self.pile_chapitres_courants:
                self.pile_chapitres_courants = list(self.progression_officielle[classe_cible])
                random.shuffle(self.pile_chapitres_courants)
            chapitre_cible = self.pile_chapitres_courants.pop(0)

        self.chapitre_en_cours = chapitre_cible
        self.sauvegarder_donnees_locales()
        
        rang_actuel = self.obtenir_rang_actuel()
        self.info_label.text = f" {rang_actuel}\n Combo : x{self.combo}"
        
        enonce, correct, opts, exp = self.moteur_generateur_mathematique(classe_cible, chapitre_cible)
        self.question_label.text = enonce
        self.bonne_reponse = str(correct)
        self.explication_erreur = exp
        self.question_generée_ia = enonce  
        
        liste_options = list(set([str(o) for o in opts]))
        if str(correct) not in liste_options: liste_options.append(str(correct))
        random.shuffle(liste_options)
                # --- BOUTONS ENTRAÎNEMENT AJUSTÉS ---
        for opt in liste_options:
            btn_opt = Button(
                text=opt, 
                font_size='22sp', 
                bold=True, 
                size_hint_y=None, 
                height=dp(90),
                text_size=(None, None),
                background_color=(0.6, 0, 0.9, 0.8),
                halign='center',        
                valign='middle'         
            )
            
            btn_opt.padding = [10,10]
            btn_opt.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0] - 20, None)))
            
            btn_opt.bind(on_press=self.verifier_choix_entrainement)
            self.interaction_layout.add_widget(btn_opt)

        layout_actions = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(90), spacing=dp(10))
        btn_quitter = Button(text="← Quitter", background_color=(0.8, 0.25, 0.25, 1), font_size='18sp', bold=True)
        btn_quitter.bind(on_press=self.quitter_action)
        btn_aide = Button(text="Fiches Cours", background_color=(0.12, 0.55, 0.85, 1), font_size='18sp', bold=True)
        btn_aide.bind(on_press=self.afficher_formulaire_cours)
        layout_actions.add_widget(btn_quitter)
        layout_actions.add_widget(btn_aide)
        self.interaction_layout.add_widget(layout_actions)

        self.lancer_chrono_entrainement()

    def quitter_action(self, instance):
        if self.sound:
            self.sound.stop()
        self.jouer_musique_suivante()
        self.afficher_menu_principal_modes()

    def verifier_choix_entrainement(self, instance):
        self.arreter_chrono() 
        temps_mis = Clock.get_time() - self.temps_debut_question
        choix = instance.text
        self.interaction_layout.clear_widgets()
        
        est_correct = (choix == self.bonne_reponse)
        if est_correct:
            self.score += 1
            self.combo += 1
            bonus_vitesse = 2 if temps_mis < 7.0 else 0
            gain = 2 + bonus_vitesse
            self.points_de_rang += gain
            texte = f" Correct {self.nom_utilisateur} !\n\n+{gain} Points de Rang (Temps : {temps_mis:.1f}s)\nCombo : x{self.combo}"
        else:
            self.combo = max(0, self.combo - 2)
            self.points_de_rang = max(0, self.points_de_rang - 3)
            texte = f" ERREUR SUR CETTE NOTION.\nLa réponse attendue était : {self.bonne_reponse}.\n\n"
            if self.explication_erreur: 
                texte += f"DÉVELOPPEMENT ALGÉBRIQUE RIGOUREUX :\n{self.explication_erreur}"
        
        self.historique_scores.append(self.points_de_rang)
        self.enregistrer_statistique_reponse(self.chapitre_en_cours, est_correct)
        self.question_label.text = texte
        self.creer_interface_suivante()

    def creer_interface_suivante(self):
        self.label_flou = Label(text="C'est encore flou ? Écris-nous ci-dessous :", font_size='18sp', size_hint=(1, None), height=dp(55), color=(0.8, 0.8, 0.8, 1))
        self.interaction_layout.add_widget(self.label_flou)
        
        self.input_avis_texte = TextInput(hint_text="Précise ta difficulté ici...", multiline=True, size_hint=(1, None), background_color=(0.6, 0, 0.9, 0.8), height=dp(270), font_size='18sp')
        self.input_whatsapp_tek = TextInput(hint_text="Ton numéro WhatsApp...", multiline=False, size_hint=(1, None), background_color=(0.6, 0, 0.9, 0.8), height=dp(80), font_size='18sp')
        
        self.interaction_layout.add_widget(self.input_avis_texte)
        self.interaction_layout.add_widget(self.input_whatsapp_tek)
        
        self.feedback_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(60), spacing=dp(10))
        for diff in ["Simple", "Abordable", "Moyen", "Complexe"]:
            btn_diff = Button(text=diff, font_size='16sp', bold=True, background_color=(0.35, 0.35, 0.98, 1))
            btn_diff.bind(on_press=lambda inst, df=diff: self.preparer_retours_developpeur_local(df))
            self.feedback_layout.add_widget(btn_diff)
        self.interaction_layout.add_widget(self.feedback_layout)
        
        btn_suivant = Button(text="Continuer →", font_size='22sp', bold=True, size_hint=(1,None), height=dp(90), background_color=(0.12, 0.55, 0.85, 1))
        btn_suivant.bind(on_press=lambda x: self.generer_question_dynamique())
        self.interaction_layout.add_widget(btn_suivant)

    def preparer_retours_developpeur_local(self, evaluation):
        texte_saisi = ""
        whatsapp_saisi = ""
        if hasattr(self, 'input_avis_texte') and self.input_avis_texte.text.strip():
            texte_saisi = self.input_avis_texte.text.strip()
        if hasattr(self, 'input_whatsapp_tek') and self.input_whatsapp_tek.text.strip():
            whatsapp_saisi = self.input_whatsapp_tek.text.strip()
            
        texte_avis_complet = f"[Eval: {evaluation}] [WhatsApp: {whatsapp_saisi}] [Difficulté: {texte_saisi}] [Question: {self.question_generée_ia}]"
        
        # Centralisation unique dans la file d'attente du dictionnaire JSON
        avis_dict = {
            "user": self.nom_utilisateur,
            "msg": texte_avis_complet
        }
        self.file_attente_avis.append(avis_dict)
        self.sauvegarder_donnees_locales()

        # Essai d'envoi immédiat
        self.tenter_synchronisation_file_attente(0)

        self.feedback_layout.disabled = True
        if hasattr(self, 'input_avis_texte'): self.input_avis_texte.disabled = True
        if hasattr(self, 'input_whatsapp_tek'): self.input_whatsapp_tek.disabled = True

         # --- ENVOI EN ARRIÈRE-PLAN VERS PYTHONANYWHERE ---
    def tenter_synchronisation_file_attente(self, dt):
        if not self.file_attente_avis:
            return
        
        # Vérifier que la file n'est pas vide avant de tenter l'envoi
        avis_a_envoyer = self.file_attente_avis[0]
        url_officiel = "https://FazadNassur.pythonanywhere.com/api/avis"

        try:
            data_json = json.dumps({
                "user": avis_a_envoyer['user'],
                "msg": avis_a_envoyer['msg']
            })
            headers = {'Content-type': 'application/json'}

            UrlRequest(
                url_officiel,
                req_body=data_json,
                req_headers=headers,
                method='POST',
                on_success=self.envoi_reussi,
                on_error=self.envoi_echoue, # Vérifie que cette méthode existe !
                on_failure=self.envoi_echoue # Important aussi pour les erreurs 400/500
            )
        except Exception as e:
            print(f"Erreur lors de la préparation de l'envoi : {e}")

    def envoi_reussi(self, req, resultat):
        if self.file_attente_avis:
            self.file_attente_avis.pop(0)
            self.sauvegarder_donnees_locales()
            print("Envoi réussi et liste mise à jour.")

    def envoi_echoue(self, req, erreur):
        #  log l'erreur pour savoir pourquoi ça plante
        print(f"Échec de l'envoi : {erreur}")
        
        # --- PROCESSUS EXAMEN BLANC --- 
    def generer_question_examen(self):
                # Retire le bouton paramètres 
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)

        self.interaction_layout.clear_widgets()
        
        # --- CONFIGURATION DES PROPORTIONS (Espace pour le haut / bas) ---
        # On donne plus d'espace en haut pour les énoncés et explications
        self.scroll_texte.size_hint_y = 0.22
        self.scroll_interaction.size_hint_y = 0.78
        
        chapitre_cible = self.examen_questions[self.examen_index_actuel]
        self.chapitre_en_cours = chapitre_cible
        
        self.info_label.text = f"MODE EXAMEN\n Question {self.examen_index_actuel + 1}/10"
        enonce, correct, opts, exp = self.moteur_generateur_mathematique(self.classe_actuelle, chapitre_cible)

        self.question_label.text = enonce
        self.bonne_reponse = str(correct)
        self.explication_erreur = exp
        
        liste_options = list(set([str(o) for o in opts]))
        if str(correct) not in liste_options: 
            liste_options.append(str(correct))
        random.shuffle(liste_options)
        
        # --- 1. AJOUT DES BOUTONS DE NAVIGATION (Quitter / Fiches) TOUT EN BAS ---
        layout_actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(90), spacing=dp(10))
        btn_quitter = Button(text="← Quitter", background_color=(0.8, 0.25, 0.25, 1), font_size='18sp', bold=True)
        btn_quitter.bind(on_press=self.quitter_action)
        btn_aide = Button(text="Fiches Cours", background_color=(0.12, 0.55, 0.85, 1), font_size='18sp', bold=True)
        btn_aide.bind(on_press=self.afficher_formulaire_cours)
        layout_actions.add_widget(btn_quitter)
        layout_actions.add_widget(btn_aide)

        # BOUTONS DE RÉPONSES AU-DESSUS DES ACTIONS 
        for opt in liste_options:
            btn_opt = Button(
                text=opt, 
                font_size='22sp', 
                bold=True, 
                size_hint_y=None, 
                height=dp(90),
                text_size=(None, None), 
                background_color=(0.6, 0, 0.9, 0.8),
                halign='center', 
                valign='middle' 
            )
            btn_opt.padding = [10, 10]
            btn_opt.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0] - 20, None)))
            btn_opt.bind(on_press=self.valider_choix_examen)
            self.interaction_layout.add_widget(btn_opt)
        self.interaction_layout.add_widget(layout_actions)

    def valider_choix_examen(self, instance):
        choix = instance.text
        # Enregistre la réponse de l'élève pour le bilan final sans interrompre l'examen
        self.examen_reponses_eleve.append((self.question_label.text, choix, self.bonne_reponse, self.explication_erreur))
        
        est_correct = (choix == self.bonne_reponse)
        if est_correct: 
            self.score += 1
            
        self.enregistrer_statistique_reponse(self.chapitre_en_cours, est_correct)
        self.examen_index_actuel += 1
        
        # Passe directement à la question suivante jusqu'à 10
        if self.examen_index_actuel < 10:
            self.generer_question_examen()
        else:
            self.arreter_chrono()
            self.terminer_et_afficher_bilan_examen()

    def terminer_et_afficher_bilan_examen(self):
        self.interaction_layout.clear_widgets()
        self.chrono_label.text = "FIN"
        
        note_sur_20 = (self.score / 10) * 20
        self.info_label.text = f"Bilan Examen\nNote : {note_sur_20:.1f}/20"
        
        if note_sur_20 >= 16:
            self.points_de_rang += 6
            mention = "EXCELLENT TRAVAIL"
        elif note_sur_20 >= 10:
            self.points_de_rang += 2
            mention = "MOYENNE VALIDÉE"
        else:
            self.points_de_rang = max(0, self.points_de_rang - 4)
            mention = "RÉTROGRADATION"
            
        self.historique_scores.append(self.points_de_rang)
        self.sauvegarder_donnees_locales()
        
        rang_actuel = self.obtenir_rang_actuel()
        
        # AJUSTEMENT DES PROPORTIONS : Plus d'espace pour le texte de correction (0.80 au lieu de 0.52)
        self.scroll_texte.size_hint_y = 0.90
        self.scroll_interaction.size_hint_y = 0.10
        
        graph_widget = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(20), padding=dp(15))
        with graph_widget.canvas.before:
            Color(0.14, 0.14, 0.18, 1)
            Rectangle(pos=graph_widget.pos, size=graph_widget.size)
        
        lbl_rank_visuel = Label(text=f" RÉSUMÉ DE FIN DE SAISSION - {mention}\nGRADE ACTUEL : {rang_actuel}\n TOTAL SCORE : {self.points_de_rang} PR", 
                                font_size='16sp', bold=True, color=(1, 1, 1, 1), halign='center')
        graph_widget.add_widget(lbl_rank_visuel)
        
        jauge_box = BoxLayout(size_hint=(1, None), height=dp(40),  padding=[20, 0, 20, 0])
        _, rp_c, s_r, _ = self.determiner_rang_et_details()
        valeur_jauge = min(100, int((float(rp_c) / float(s_r)) * 100))
        pb_ff_style = ProgressBar(max=100, value=valeur_jauge, size_hint=(1,None), height=dp(30))
        jauge_box.add_widget(pb_ff_style)
        graph_widget.add_widget(jauge_box)
        
        self.interaction_layout.add_widget(graph_widget)
        
        #  CONSTRUCTION DU BILAN PÉDAGOGIQUE DÉTAILLÉ
        bilan_texte = f"RÉSULTAT EXAMEN DE {self.nom_utilisateur}\nNote globale : {note_sur_20:.1f}/20\n\n"
        bilan_texte += "========================================\n"
        bilan_texte += "--- CORRECTIONS DÉTAILLÉES ---\n"
        bilan_texte += "========================================\n"
        
        for i, (q, recu, bon, exp) in enumerate(self.examen_reponses_eleve):
            bilan_texte += f"\n[ Question {i+1} ]\n"
            bilan_texte += f"Énoncé : {q}\n"
            
            if recu == bon:
                bilan_texte += f"Statut : [ CORRECT ] (Votre réponse : {recu})\n"
            else:
                bilan_texte += f"Statut : [ À REVOIR ]\n"
                bilan_texte += f"• Votre réponse : {recu}\n"
                bilan_texte += f"• Réponse attendue : {bon}\n"
                bilan_texte += f"\n--- DÉMONSTRATION ALGÉBRIQUE ---\n{exp}\n"
            
            bilan_texte += "----------------------------------------\n"
                
        self.question_label.text = bilan_texte
        
        if self.btn_menu_persistant not in self.main_layout.children:
            self.main_layout.add_widget(self.btn_menu_persistant)

            # --- MOTEUR DE GÉNÉRATION DES ÉNONCÉS MULTI-VARIANTES ---
    def moteur_generateur_mathematique(self, classe_cible, chapitre_cible):
        _, _, _, index_grade = self.determiner_rang_et_details()
        return MoteurMathematique.moteur_generateur_mathematique(
            classe_cible,
            chapitre_cible,
            index_grade,
            self.niveau_profil
        )   
if __name__ == '__main__':
    FixedDynamicQuizApp().run()
