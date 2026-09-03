import random
import math
import json
import time
import os
import sys
os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.uix.popup import Popup
from kivy.core.window import Window 
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from moteur_quiz import MoteurMathematique
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.network.urlrequest import UrlRequest 
from kivy.core.text import LabelBase
import webbrowser

# ___CLASS DU MASCOTTE ___
class DraggableMascot(FloatLayout):
    def __init__(self, **kwargs):
        super(DraggableMascot, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(200), dp(120))
        self.pos = (dp(60), dp(800))
        
        with self.canvas.before:
            Color(0.08, 0.18, 0.32, 0.05)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[8])
        
        self.bind(pos=self._update_graphics, size=self._update_graphics)

        self.layout_interne = BoxLayout( 
            orientation='horizontal', 
            size_hint=(1, 1), 
            pos_hint={'x': 0, 'y': 0},
            padding=dp(0), 
            spacing=dp(0)
        )
        
        self.avatar_img = Image(
            source='badges/locky.png', 
            size_hint=(None, None),
            size=(dp(150), dp(150))
        )
        
        self.bulle_label = Label(
            text="Prêt pour le défi ?",
            font_size='12sp',
            color=(0.3, 0.8, 0.6, 1),
            halign='center',
            valign='middle',
            bold=True  
        )
        self.bulle_label.bind(size=lambda s, w: setattr(s, 'text_size', w))

        self.layout_interne.add_widget(self.avatar_img)
        self.layout_interne.add_widget(self.bulle_label)  
        self.add_widget(self.layout_interne)            
        
        Clock.schedule_interval(self.changer_message_aleatoire, 10)
        Clock.schedule_interval(self.declencher_acrobatie, 15)

    def _update_graphics(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_offset_x = touch.pos[0] - self.x
            self.touch_offset_y = touch.pos[1] - self.y
            self.is_dragging = False
            # On mémorise la position de départ du toucher pour calculer si on a bougé ou juste tapé
            self.start_touch_pos = touch.pos
            return True
        return super(DraggableMascot, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) or getattr(self, 'is_dragging', False):
            # Si le doigt a bougé de plus de quelques pixels, c'est un glissement (drag)
            if hasattr(self, 'start_touch_pos'):
                distance = ((touch.pos[0] - self.start_touch_pos[0])**2 + (touch.pos[1] - self.start_touch_pos[1])**2)**0.5
                if distance > dp(10):
                    self.is_dragging = True
            
            if getattr(self, 'is_dragging', False):
                self.x = touch.pos[0] - self.touch_offset_x
                self.y = touch.pos[1] - self.touch_offset_y
            return True
        return super(DraggableMascot, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) or getattr(self, 'is_dragging', False):
            # Si on n'a PAS glissé, c'est un simple tap -> On déclenche l'excitation et les flammes !
            if not getattr(self, 'is_dragging', False):
                self.declencher_excitation()
            
            self.is_dragging = False
            return True
        return super(DraggableMascot, self).on_touch_up(touch)


    def creer_paillette(self, dt):
        
        pos_globale_x, pos_globale_y = self.to_window(self.center_x, self.center_y)
        
        particule = FloatLayout(
            size_hint=(None, None), 
            size=(dp(14), dp(14)), 
            pos=(self.x + self.width / 2 + random.randint(int(dp(-15)), int(dp(15))), 
                 self.y + self.height / 2 + random.randint(int(dp(-15)), int(dp(15))))
        )
        with particule.canvas:
            Color(0.4, 0.8, 1, 0.9)
            Ellipse(size=(dp(14), dp(14)), pos=(0, 0))
            
        Window.add_widget(particule)
        
        anim_flamme = Animation(
            size=(dp(4), dp(4)),  
            y=particule.y + random.randint(int(dp(10)), int(dp(35))), 
            x=particule.x + random.randint(int(dp(-10)), int(dp(10))), 
            opacity=0, 
            duration=0.35,
            t='out_quad'
        )
        anim_flamme.bind(on_complete=lambda *args: self.parent.remove_widget(particule) if particule.parent else None)
        anim_flamme.start(particule)

    def declencher_excitation(self):
        self.size_hint = (None, None)
        
        anim = Animation(duration=0)
        for _ in range(4):
            rand_x = random.randint(int(dp(10)), int(Window.width - self.width - dp(10)))
            rand_y = random.randint(int(Window.height * 0.05), int(Window.height - self.height - dp(50)))
            anim += Animation(x=rand_x, y=rand_y, duration=0.12, t='out_quad')
        
        for i in range(8):
            Clock.schedule_once(self.creer_paillette, i * 0.08)
            
        messages_excites = [
            "Waaah ! ", 
            "Magie ! ", 
            "Bougeotte ! ", 
            "Génie ! "
        ]
        self.bulle_label.text = random.choice(messages_excites)
        
        anim.start(self)

    def changer_message_aleatoire(self, dt):
        messages = [
            "Prêt pour le défi ?",
            "Force à toi ! ",
            "La mathématique est un jeu !",
            "Montre ton génie !",
            "Encore un effort !",
            "Attention aux pièges !"
        ]
        self.bulle_label.text = random.choice(messages)

    def declencher_acrobatie(self, dt):
        anim = Animation(y=self.y + dp(30), duration=0.25) + Animation(y=self.y, duration=0.25)
        anim.start(self)

# ___CLASS PRINCIPAL ___
class FixedDynamicQuizApp(App):
    def build(self):
        
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
        
        # --- ROOT LAYOUT GLOBAL (FloatLayout pour superposer Locky) ---
        self.root_layout = FloatLayout()
        
        # --- CONSTRUCTION DE L'INTERFACE ENTIÈREMENT OPTIMISÉE POUR LE BAS DU POUCE ---
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(5), spacing=dp(2))
        with self.main_layout.canvas.before:
            Color(0.12, 0.28, 0.48, 1)
            self.rect = RoundedRectangle(size=self.main_layout.size, pos=self.main_layout.pos, radius=[10])
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # 1. Zone d'en-tête (Informations de profil et Chronomètre) 
        self.info_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(90), spacing=dp(2))
        self.info_label = Label(text="Initialisation en cours...", font_size='18sp', bold=True, color=(1, 0.84, 0, 1), halign='left', valign='middle')
        self.info_label.bind(size=self._update_text_size)
        self.chrono_label = Label(text="", font_size='22sp', bold=True, color=(1, 0.35, 0.35, 1), halign='right', valign='middle')
       # Bouton Paramètres dans le coin supérieur droit
        self.btn_parametres = Button(
        background_normal='icône_appli/parametre.png',
        background_down='icône_appli/parametre.png',
        size_hint=(None, None),
        size=(dp(40), dp(40)),
        pos_hint={'top': 0.86, 'right': 0.96}
    )
        self.btn_parametres.bind(on_press=self.ouvrir_menu_parametres)

        self.chrono_label.bind(size=self._update_text_size)
        self.info_layout.add_widget(self.info_label)
        self.info_layout.add_widget(self.chrono_label)
        self.main_layout.add_widget(self.info_layout)
        self.info_layout.add_widget(self.btn_parametres)

        
        # 2. Zone d'affichage des énoncés de questions ou des cours - MILIEU SUPÉRIEUR
        self.scroll_texte = ScrollView(size_hint_y=0.10, do_scroll_x=False, do_scroll=True)
        self.question_label = Label(text="", font_size='20sp', halign='center', valign='middle', size_hint=(1, None), color=(1, 1, 1, 1))
        self.question_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - 10, None)))
        self.question_label.bind(texture_size=lambda instance, size: setattr(instance, 'height', max(size[1] + 10, 40)))
        self.scroll_texte.add_widget(self.question_label)
        self.main_layout.add_widget(self.scroll_texte)
        
        # 3. Zone d'interaction dynamique principale (Boutons de réponses, Saisie, Menus) - BAS DU POUCE
        self.scroll_interaction = ScrollView(size_hint_y=0.90, do_scroll_x=False, do_scroll_y=True)
        self.interaction_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(510), spacing=dp(2))
        self.scroll_interaction.add_widget(self.interaction_layout)
        self.main_layout.add_widget(self.scroll_interaction)
        
        # Bouton persistant dédié pour le retour menu (Placé stratégiquement sous les boutons ou réajusté)
        self.btn_menu_persistant = Button(text="Revenir au Menu Principal", font_size='20sp', bold=True, size_hint_y=None, height=dp(80), background_color=(0.12, 0.53, 0.9, 1))
        self.btn_menu_persistant.bind(on_press=self.action_retour_menu_persistant)
        
        # Bouton unique de retour pour les vues isolées (S'affichera tout en bas du main_layout)
        self.btn_retour_isole = Button(text="← Retour Évolution", size_hint=(1, None), height=dp(80), font_size='22sp', bold=True, background_color=(0.15, 0.45, 0.75, 1))
        self.charger_donnees_locales()
        
        # Ajout du layout principal dans le root_layout
        self.root_layout.add_widget(self.main_layout)

        # --- INSTANCIATION ET AJOUT DE LA MASCOTTE LOCKY ---
        self.mascotte = DraggableMascot()
        self.root_layout.add_widget(self.mascotte)

        self.charger_donnees_locales()
        
        # Lancement de la tâche récurrente de synchronisation en arrière-plan (toutes les 15 secondes)
        Clock.schedule_interval(self.tenter_synchronisation_file_attente, 15.0)
        self.afficher_ecran_demarrage()
            
        return self.root_layout
              
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
        
    #___ECRAN DE DÉMARRAGE ___ 
    def afficher_ecran_demarrage(self):
        self.nettoyer_boutons_bas()
        self.info_layout.opacity = 0
        self.scroll_texte.opacity = 0 
        self.scroll_interaction.opacity = 0

        chemin_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'badges', 'logo.png')
        print(f"CHEMIN LOGO: {chemin_logo}")

        ecran_intro = FloatLayout()
        
        # 1. Utiliser l'unique instance globale de la mascotte
        if not hasattr(self, 'mascotte') or self.mascotte is None:
            self.mascotte = DraggableMascot(size=(dp(160), dp(90)), pos=(dp(20), dp(150)))
        
        if self.mascotte.parent:
            self.mascotte.parent.remove_widget(self.mascotte)
            
        with ecran_intro.canvas.before:
             Color(0.12, 0.28, 0.48, 1)
             self.rect_splash = Rectangle(size=ecran_intro.size, pos=ecran_intro.pos)
        ecran_intro.bind(size=lambda inst, val: setattr(self.rect_splash, 'size', val))
        ecran_intro.bind(pos=lambda inst, val: setattr(self.rect_splash, 'pos', val))
    
        # 2. Ajouter d'abord le logo de fond
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

        # 3. Ajouter la mascotte EN DERNIER 
        ecran_intro.add_widget(self.mascotte)
        self.sequence_intro_locky(self.mascotte)

        self.main_layout.add_widget(ecran_intro) 
        Clock.schedule_once(lambda dt: self.aller_au_menu_principal(ecran_intro), 11)

        
    def sequence_intro_locky(self, mascot):
        # Positions aléatoires ou définies pour l'écran      
        points = [
            (Window.width * 0.4, Window.height * 0.7), 
            (Window.width * 0.5, Window.height * 0.1),
            (Window.width * 0.3, Window.height * 0.8)
        ]
        messages = [
            "Salut, je m'appelle Locky !",
            "Chargement... veuillez patienter.",
            f"Cher {self.nom_utilisateur}, c'est presque prêt !"
        ]
              
        for i in range(3):
            # 1. Déplacement
            anim_move = Animation(pos=points[i], duration=0.4, t='out_quad')
            
            # 2. Changement de message
            def set_msg(inst, val, m=messages[i]):
                mascot.bulle_label.text = m
            
            # 3. Pause
            anim_wait = Animation(duration=2.90)
            
            # Assemblage : Mouvement -> Changement de message
            sequence = anim_move + Animation(duration=0.5)
            sequence.bind(on_start=set_msg)
            
            Clock.schedule_once(lambda dt, s=sequence: s.start(mascot), i * 4.45)


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
        # 1. Retirer l'écran d'intro du layout principal
        if ecran_intro in self.main_layout.children:
            self.main_layout.remove_widget(ecran_intro)
            
        # 2. Détacher la mascotte de l'écran d'intro pour qu'elle ne soit pas supprimée
        if self.mascotte.parent:
            self.mascotte.parent.remove_widget(self.mascotte)
            
        # 3. L'ajouter au conteneur principal permanent pour qu'elle reste visible sur le menu
        if self.mascotte not in self.root.children:
            self.root.add_widget(self.mascotte)
            
        # 1. On retire le splash
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
            height=dp(30),
            pos_hint={'center_x': 0.5, 'top': 0.88}
        )
        self.layout_parametres.add_widget(lbl_titre)

        # Hauteur fixe des boutons et espacement
        h_btn = dp(60)
        espacement = dp(0)

        # Bouton 1 : Modifier les informations
        btn_modifier_infos = Button(
            text="Modifier mes informations personnelles",
            text_size=(0.8 * Window.width - dp(20), None),
            font_size='18sp',
            size_hint=(0.8, None),
            halign='center',        
            valign='middle',        
            height=h_btn,
            pos_hint={'center_x': 0.5, 'top': 0.57},
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_modifier_infos.bind(on_press=self.afficher_formulaire_modification_infos)
        self.layout_parametres.add_widget(btn_modifier_infos)

        # Bouton 2 : Consulter mes données enregistrées
        btn_voir_infos = Button(
            text="Consulter mes données enregistrées",
             font_size='18sp',
             text_size=(0.8 * Window.width - dp(20), None),
            size_hint=(0.8, None),
            halign='center',        
            valign='middle' ,       
            height=h_btn,
            pos_hint={'center_x': 0.5, 'top': 0.58 - (h_btn + espacement) / Window.height},
            background_color=(0.2, 0.7, 0.4, 1)
        )
        btn_voir_infos.bind(on_press=self.afficher_donnees_utilisateur)
        self.layout_parametres.add_widget(btn_voir_infos)

        # Bouton 3 : À propos & Version Pro
        btn_pro = Button(
            text="À propos & Version Pro",
            font_size='18sp',
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.8, None),
            height=h_btn,
            pos_hint={'center_x': 0.5, 'top': 0.61 - (4 * (h_btn + espacement)) / Window.height},
            background_color=(0.6, 0.3, 0.8, 1)
        )
        btn_pro.bind(on_press=self.afficher_a_propos)
        self.layout_parametres.add_widget(btn_pro)
        
        # 4. Bouton pour rejoindre la communauté 
        btn_whatsapp = Button(
            text="Rester connecté au Développeur ",
            font_size='18sp',
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.58 - (2 * (h_btn + espacement)) / Window.height},
            background_color=(0.4, 0.4, 0.7, 1) 
        )
        # ouvrir le lien de la communauté
        btn_whatsapp.bind(on_release=lambda x:                   webbrowser.open("https://chat.whatsapp.com/FlcaUC6BTroDBzZ3ZujlVx"))
        self.layout_parametres.add_widget(btn_whatsapp) 


# 5. le guide d'utilisation de l'appli
        btn_aide = Button(
            text="Comment fonctionne l'appli",
            font_size='18sp',
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.59 - (3 * (h_btn + espacement)) / Window.height},
            background_color=(0.2, 0.5, 0.8, 1) 
        )
        btn_aide.bind(on_release=lambda x: self.afficher_popup_aide())
        self.layout_parametres.add_widget(btn_aide)

        # Bouton 6 : Fermer les Paramètres
        btn_fermer = Button(
            text="Fermer les Paramètres",
            font_size='18sp',
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.8, None),
            height=h_btn,
            pos_hint={'center_x': 0.5, 'top': 0.61 - (5 * (h_btn + espacement)) / Window.height},
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
            
    def afficher_popup_aide(self):
        # Contenu détaillé expliquant comment utiliser l'application et à quoi servent les boutons
        texte_explicatif = (
            "●[b]Guide d'utilisation de l'application :[/b]\n\n"
            "○ [b]Le Quiz de Mathématiques :[/b] Conçu spécialement pour vous accompagner dans vos révisions universitaires (Algèbre, Analyse, etc.) ou générales.\n\n"
            "  - [i]Mode Quiz :[/i] Lance les séries de questions aléatoires pour tester vos compétences.\n"
            "  - [i]Paramètres :[/i] Permet de configurer l'application, de rejoindre la communauté du développeur et de consulter ce guide.\n\n"
            
            "[b]Guide d'utilisation des Paramètres :[/b]\n\n"
            "- [i]Modifier mes informations personnelles :[/i] Permet de mettre à jour votre nom, votre niveau universitaire ou de classe, votre âge ainsi que votre sexe. Des suggestions intelligentes s'affichent automatiquement lors de la saisie.\n\n"         
            "- [i]Consulter mes données enregistrées :[/i] Affiche un récapitulatif complet de toutes vos informations personnelles actuellement sauvegardées dans l'application.\n\n"           
            "- [i]À propos & Version Pro :[/b] Fournit les informations sur l'application (Version , développeur Fazad Nassur) et l'accès aux fonctionnalités avancées.\n\n"         
            "- [i]Rester connecté au Développeur :[/i] Ouvre directement le groupe WhatsApp officiel pour rejoindre la communauté, suivre les mises à jour et échanger.\n\n"          
            "- [i]Comment fonctionne l'appli :[/i] Ouvre ce guide d'aide interactif pour vous orienter à tout moment dans l'utilisation de l'application.\n\n"
            
            "• [b]Astuce :[/b] Restez connectés au Développeur via le bouton WhatsApp pour suivre les mises à jour et évolutions du Développeur !\n\n"
            "● [b]Navigation et option:[/b]\n\n"
            
            " - [i]Entraînement :[/i] Idéal pour s'exercer à son rythme sur des séries de questions dynamiques adaptées à votre classe. Un chronomètre rythmé et un système de combo pimentent vos sessions !\n\n"           
            " - [i]Examen Blanc :[/i] Un mode sérieux composé d'une série de 10 questions chronométrées pour tester vos connaissances en conditions réelles et obtenir un bilan noté sur 20.\n\n"
            " - [i]Joue jusqu'à 4 :[/i] Un mode multijoueur local (de 2 à 4 participants) pour affronter vos amis et voir qui a les meilleures compétences mathématiques.\n\n"
            " - [i]Niveaux d'Activités :[/i] Un parcours progressif de 16 activités spécialisées (allant du calcul mental à la physique quantique et l'analyse) qui se débloquent selon votre rang.\n\n"
            " - [i]Sujets Casse-Tête :[/i] Des défis de logique, des paradoxes mathématiques et des énigmes algébriques pour stimuler vos neurones.\n\n"
            "[b]Guide de l'Espace Évolution :[/b]\n\n"
            " - [i]Mon Grade, XP & Rythme :[/i] Visualisez votre score de rang (PR), votre niveau d'expérience (XP) et votre jauge de progression avec une analyse intelligente de votre rythme.\n\n"
            " - [i]Liste Officielle des Rangs :[/i] Consultez la hiérarchie complète des grades disponibles, du niveau Bronze jusqu'aux sommets.\n\n"
            " - [i]Maîtrise des Chapitres :[/i] Un suivi personnalisé sous forme de barres de progression récapitulant vos réussites notion par notion.\n\n"
            "[b]Aide et Fiches de Cours :[/b]\n\n"
            " - [i]Fiches Cours :[/i] Accessible pendant les quiz pour afficher un résumé théorique et des rappels adaptés à votre classe.\n\n"
            " - [i]Démonstrations Algébriques :[/i] En cas d'erreur, une correction détaillée et rigoureuse vous est fournie pour comprendre immédiatement le raisonnement.\n\n"
            "[b]Astuce :[/b] Utilisez le bouton d'avis au développeur pour laisser vos remarques et votre numéro WhatsApp afin d'échanger directement !"    
   
     )
    
        contenu = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
    
        scroll = ScrollView(size_hint=(1, 0.8))
        label = Label(
            text=texte_explicatif,
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
    # Ajustement automatique de la taille du texte dans le ScrollView
        label.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(20), None)))
        label.bind(texture_size=lambda s, t: setattr(s, 'height', t[1]))
    
        scroll.add_widget(label)
    
        btn_fermer = Button(
            text="J'ai compris",
            text_size=(1 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.2, 0.2, 1)
        )
    
        contenu.add_widget(scroll)
        contenu.add_widget(btn_fermer)
    
        popup_aide = Popup(
            title="Comment fonctionne l'appli",
            content=contenu,
            text_size=(0.9* Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.9, 0.8),
            auto_dismiss=True
        )
    
        btn_fermer.bind(on_release=popup_aide.dismiss)
        popup_aide.open()

        
    def afficher_donnees_utilisateur(self, instance):
        self.layout_parametres.clear_widgets()

        # Fond noir
        with self.layout_parametres.canvas.before:
            Color(0, 0, 0, 0.95)
            Rectangle(size=(Window.width, Window.height), pos=(0, 0))

        lbl_titre = Label(
            text="DONNÉES ENREGISTRÉES",
            font_size='22sp',
            text_size=(1 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            bold=True,
            size_hint=(1, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.7}
        )
        self.layout_parametres.add_widget(lbl_titre)

        # Récupération sécurisée des variables pour éviter le crase
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
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        self.layout_parametres.add_widget(lbl_data)

        # Bouton pour revenir au menu des paramètres
        btn_retour_param = Button(
            text="← Retour",
            font_size='18sp',
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.3},
            background_color=(0.75, 0.2, 0.2, 1)
        )
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
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',
            valign='middle',
            size_hint=(0.8, None),
            height=dp(150),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        lbl_info.bind(texture_size=lambda instance, value: setattr(instance, 'text_size', value))
        self.layout_parametres.add_widget(lbl_info)
        
        # 3. Un bouton Retour pour revenir aux options des paramètres
        btn_retour_param = Button(
            text="Retour",
            font_size='18sp',
            text_size=(0.8 * Window.width - dp(20), None),
            halign='center',        
            valign='middle',
            size_hint=(0.8, None),
            height=dp(50),
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
        self.suggestions_niveau_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        self.input_classe = TextInput(text=str(getattr(self, 'classe_utilisateur', '')), hint_text="Niveau(ex: MPC)", size_hint_y=None, background_color=(0.6, 0, 0.9, 0.8), height=dp(50), multiline=False)
        self.suggestions_classe_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        self.input_age = TextInput(text=str(getattr(self, 'age_utilisateur', '')), hint_text="Âge", size_hint_y=None,background_color=(0.6, 0, 0.9, 0.8),  height=dp(50), multiline=False)
        self.input_sexe = TextInput(text=str(getattr(self, 'sexe_utilisateur', '')), hint_text="Sexe", size_hint_y=None,background_color=(0.6, 0, 0.9, 0.8),  height=dp(50), multiline=False)

        # Bouton Enregistrer
        btn_sauvegarder = Button(text="Enregistrer les modifications", font_size='18sp', text_size=(1 * Window.width - dp(20), None),halign='center',        valign='middle',bold=True, size_hint_y=None, height=dp(50), background_color=(0.2, 0.7, 0.4, 1))
        btn_sauvegarder.bind(on_press=self.sauvegarder_nouvelles_infos)

        btn_retour_menu = Button(text="← Retour au menu principal", font_size='18sp',text_size=(1 * Window.width - dp(20), None),halign='center',        valign='middle', bold=True, size_hint_y=None, height=dp(50), background_color=(0.75, 0.2, 0.2, 1))
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
            self.question_label.text = "Erreur : Veuillez sélectionner une classe valide parmi les propositions et assurez vous que les cases classe et niveau son  saisie."
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
        
        self.input_nom = TextInput(hint_text="Ton prénom ici...", multiline=False, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle',size_hint_y=None, height=dp(80), font_size='22sp')
        btn_valider_nom = Button(text="S'enregistrer et Continuer", size_hint_y=None, text_size=(1* Window.width - dp(20), None), halign='center', valign='middle',height=dp(130), background_color=(0.12, 0.53, 0.9, 1), font_size='22sp', bold=True)
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
           # Supprimer le bouton menu de l'IA s'il existe à l'écran
        if hasattr(self, 'btn_menu_ia') and self.btn_menu_ia in self.root.children:
            self.root.remove_widget(self.btn_menu_ia)
            
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
        
        layout_l1 = BoxLayout(orientation='horizontal', size_hint=(1, None) ,height=dp(80), spacing=dp(15))
        
        btn_entrainement = Button(text=" Entraînement ", font_size='22sp', text_size=(1 * Window.width - dp(20), None), halign='center',        valign='middle', bold=True, background_color=(0.12, 0.28, 0.48, 1), size_hint=(1,None), height=dp(80))
        btn_entrainement.bind(on_press=lambda x: self.selectionner_mode("Entraînement"))
        layout_l1.add_widget(btn_entrainement)
        
        btn_examen = Button(text="Examen Blanc ", font_size='22sp', text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', bold=True, background_color=(0.12, 0.28, 0.48, 1), size_hint_y=None, height=dp(80))
        btn_examen.bind(on_press=lambda x: self.selectionner_mode("Examen"))
        layout_l1.add_widget(btn_examen)
        
        self.interaction_layout.add_widget(layout_l1)
        
        layout_l2 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(80), spacing=dp(15))
        
        btn_jouer_4 = Button(text="Joue jusqu'à 4", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.28, 0.48, 1))
        btn_jouer_4.bind(on_press=self.afficher_sous_menu_joueurs)
        layout_l2.add_widget(btn_jouer_4)

        
        btn_stats = Button(text=" Salle des Rangs\n & Statistiques", font_size='22sp', text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', bold=True, background_color=(0.12, 0.28, 0.48, 1), size_hint_y=None, height=dp(80))
        btn_stats.bind(on_press=self.afficher_sous_menu_evolution)
        layout_l2.add_widget(btn_stats)    
        self.interaction_layout.add_widget(layout_l2)

        btn_avis_general = Button(text="Laisser un avis au Développeur", font_size='22sp', text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', bold=True, background_color=(0.85, 0.65, 0.13, 1), size_hint=(1, None), height=dp(80))
        btn_avis_general.bind(on_press=self.afficher_interface_avis_general)
        self.interaction_layout.add_widget(btn_avis_general)
        
        layout_l3 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(80), spacing=dp(15))
        
        btn_niveaux_activites = Button(text="Niveaux d'Activités", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.28, 0.48, 1))
        btn_niveaux_activites.bind(on_press=self.afficher_sous_menu_niveaux_activites)
        layout_l3.add_widget(btn_niveaux_activites)
   
        btn_sujets = Button(text="Sujets Casse-Tête", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.28, 0.48, 1))
        btn_sujets.bind(on_press=self.afficher_sous_menu_sujets_casse_tete)
        layout_l3.add_widget(btn_sujets)
        self.interaction_layout.add_widget(layout_l3)
        
        layout_l4 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(80), spacing=dp(15))
        
        btn_ia = Button(text='Lancer l\'IA (En ligne)', font_size='22sp', height =dp(80), bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', size_hint =(1, None), background_color=(0.3, 0.2, 0.6, 1))
        layout_l4.add_widget(btn_ia)
        btn_ia.bind(on_press=self.afficher_menu_ia_parametres)
        
        layout_l4.add_widget(Button(text='bientôt disponible', font_size='22sp', text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', bold=True, background_color=(0.25, 0.25, 0.25, 1)))
        self.interaction_layout.add_widget(layout_l4)
        
        btn_autres = Button(text='Autres bientot disponible', font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle',  size_hint=(1, None), height=dp(80), background_color=(0.25, 0.25, 0.25, 1))
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
                btn = Button(text=f"✔ {activite}", font_size='14sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(80))
                btn.bind(on_press=lambda x, act=activite: self.lancer_activite_niveau(act))
            else:
                nom_rang_nom = self.LISTE_RANGS[index_requis].strip()
                btn = Button(text=f"🔒 {activite}\n[Requis: {nom_rang_nom}]", font_size='12sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.3, 0.3, 0.3, 1), size_hint_y=None, height=dp(80))
                btn.bind(on_press=lambda x, r=nom_rang_nom: self.alerte_activite_verrouillee(r))

            grille_activites.add_widget(btn)

        # On ajuste la hauteur du layout d'interaction pour que le ScrollView permette de tout faire défiler
        self.interaction_layout.height = hauteur_totale + dp(120)
        self.interaction_layout.add_widget(grille_activites)

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(80))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())
        self.interaction_layout.add_widget(btn_retour)
        
    def lancer_activite_niveau(self, nom_activite):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Activité : {nom_activite}"
        self.question_label.text = f"Session de l'activité '{nom_activite}' lancée avec succès.\nBonne concentration !"
        
        btn_retour = Button(text="← Retour aux niveaux", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.53, 0.9, 1), size_hint_y=None, height=dp(80))
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

        btn_paradoxes = Button(text="Paradoxes Mathématiques", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.55, 0.3, 0.75, 1), size_hint_y=None, height=dp(80))
        btn_paradoxes.bind(on_press=lambda x: self.lancer_sujet_casse_tete("Paradoxes"))

        btn_enigmes = Button(text="Énigmes Algébriques", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(80))
        btn_enigmes.bind(on_press=lambda x: self.lancer_sujet_casse_tete("Énigmes"))

        btn_geometrie = Button(text="Défis Géométriques Poussés", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None), halign='center', valign='middle', background_color=(0.85, 0.65, 0.13, 1), size_hint_y=None, height=dp(80))
        btn_geometrie.bind(on_press=lambda x: self.lancer_sujet_casse_tete("Géométrie"))

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(80))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())

        self.interaction_layout.add_widget(btn_paradoxes)
        self.interaction_layout.add_widget(btn_enigmes)
        self.interaction_layout.add_widget(btn_geometrie)
        self.interaction_layout.add_widget(btn_retour)

    def lancer_sujet_casse_tete(self, type_defi):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Défi : {type_defi}"
        self.question_label.text = f"Le module spécial '{type_defi}' est en cours de déploiement pour propulser ton niveau vers les sommets."
        
        btn_retour = Button(text="← Retour aux sujets", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.53, 0.9, 1), size_hint_y=None, height=dp(80))
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

        btn_2p = Button(text="2 Joueurs", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.2, 0.5, 0.8, 1), size_hint_y=None, height=dp(80))
        btn_2p.bind(on_press=lambda x: self.lancer_mode_multijoueur(2))

        btn_3p = Button(text="3 Joueurs", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=dp(80))
        btn_3p.bind(on_press=lambda x: self.lancer_mode_multijoueur(3))

        btn_4p = Button(text="4 Joueurs", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.85, 0.65, 0.13, 1), size_hint_y=None, height=dp(80))
        btn_4p.bind(on_press=lambda x: self.lancer_mode_multijoueur(4))

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(80))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())

        self.interaction_layout.add_widget(btn_2p)
        self.interaction_layout.add_widget(btn_3p)
        self.interaction_layout.add_widget(btn_4p)
        self.interaction_layout.add_widget(btn_retour)
        
    def lancer_mode_multijoueur(self, nombre_joueurs):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Mode {nombre_joueurs} Joueurs"
        self.question_label.text = f"Le mode multijoueur local pour {nombre_joueurs} joueurs est en cours de configuration.\nPrépare-toi à en découdre !"
        
        btn_retour = Button(text="← Retour au menu", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.53, 0.9, 1), size_hint_y=None, height=dp(90))
        btn_retour.bind(on_press=self.afficher_sous_menu_joueurs)
        self.interaction_layout.add_widget(btn_retour)

# --- SOUS-MENUS DU PANNEAU D'ÉVOLUTION --
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

        btn_profil_rangs = Button(text=" Mon Grade, XP & Rythme Actuel", font_size='22sp', bold=True, background_color=(0.2, 0.5, 0.8, 1), text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', size_hint_y=None, height=dp(90))
        btn_profil_rangs.bind(on_press=self.afficher_tableau_de_bord_stats)

        btn_liste_grades = Button(text=" Liste Officielle des Rangs", font_size='22sp', bold=True, background_color=(0.55, 0.3, 0.75, 1), text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', size_hint_y=None, height=dp(90))
        btn_liste_grades.bind(on_press=self.afficher_liste_complete_des_rangs)

        btn_modules_maitrise = Button(text=" Maîtrise des Chapitres", font_size='22sp', bold=True, background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', height=dp(80))
        btn_modules_maitrise.bind(on_press=self.afficher_maitrise_des_modules)

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=dp(80))
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
        
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), spacing=dp(15))
        btn_annuler = Button(text="Annuler", text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.75, 0.2, 0.2, 1), font_size='22sp', bold=True)
        btn_annuler.bind(on_press=lambda x: self.afficher_menu_principal_modes())
        
        btn_envoyer = Button(text="Envoyer l'avis", text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.2, 0.65, 0.4, 1), font_size='22sp', bold=True)
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
            btn = Button(text=nv, font_size='22sp', background_color=(0.15, 0.45, 0.75, 1), size_hint_y=None, height=dp(80))
            btn.bind(on_press=lambda inst, n=nv, list_cl=niveaux[nv]: self.afficher_menu_classes(n, list_cl))
            self.interaction_layout.add_widget(btn)

        btn_retour = Button(text="← Revenir à l'Accueil", size_hint_y=None, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', height=dp(80), font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1))
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
            btn = Button(text=cl, font_size='22sp', background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', height=dp(80))
            btn.bind(on_press=self.initialiser_session_classe)
            self.interaction_layout.add_widget(btn)

        btn_retour = Button(text="← Étape Précédente", size_hint_y=None, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', height=dp(80), font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1))
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
                height=dp(80),
                text_size=(None, None),
                background_color=(0.6, 0, 0.9, 0.8),
                halign='center',        
                valign='middle'         
            )
            
            btn_opt.padding = [10,10]
            btn_opt.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0] - 20, None)))
            
            btn_opt.bind(on_press=self.verifier_choix_entrainement)
            self.interaction_layout.add_widget(btn_opt)

        layout_actions = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(80), spacing=dp(10))
        
        btn_quitter = Button(text="← Quitter", text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.8, 0.25, 0.25, 1), font_size='18sp', bold=True)
        btn_quitter.bind(on_press=self.quitter_action)
        
        btn_aide = Button(text="Fiches Cours", text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.55, 0.85, 1), font_size='18sp', bold=True)
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
        
        # --- ANIMATION AVANCÉE 
        taille_initiale = self.question_label.font_size
        couleur_origine = self.question_label.color[:] # Sauvegarde de la couleur de base du texte
        
        # Définition de la couleur du flash selon la réussite
        couleur_flash = [0.1, 0.9, 0.3, 1] if est_correct else [0.9, 0.2, 0.2, 1]
        
        # Préparation de l'état initial pour l'animation
        self.question_label.opacity = 0.3
        self.question_label.color = couleur_flash
        
        # Séquence fluide : fondu + grossissement, puis retour à la normale avec un effet rebond
        anim = (
            Animation(opacity=1.0, font_size=taille_initiale * 1.25, duration=0.12, t='out_quad') +
            Animation(font_size=taille_initiale, color=couleur_origine, duration=0.25, t='out_bounce')
        )
        anim.start(self.question_label)     
        self.creer_interface_suivante()

    def creer_interface_suivante(self):
        self.label_flou = Label(text="C'est encore flou ? Écris-nous ci-dessous :", font_size='18sp', size_hint=(1, None), height=dp(45), color=(0.8, 0.8, 0.8, 1))
        self.interaction_layout.add_widget(self.label_flou)
        
        self.input_avis_texte = TextInput(hint_text="Précise ta difficulté ici...", multiline=True, size_hint=(1, None), background_color=(0.6, 0, 0.9, 0.8),height=dp(100), font_size='18sp')
        self.input_whatsapp_tek = TextInput(hint_text="Ton numéro WhatsApp...", multiline=False, size_hint=(1, None), background_color=(0.6, 0, 0.9, 0.8), height=dp(40), font_size='18sp')
        
        self.interaction_layout.add_widget(self.input_avis_texte)
        self.interaction_layout.add_widget(self.input_whatsapp_tek)
        
        self.feedback_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(40), spacing=dp(10))
        for diff in ["Simple", "Abordable", "Moyen", "Complexe"]:
            btn_diff = Button(text=diff, font_size='16sp', bold=True, background_color=(0.35, 0.35, 0.98, 1))
            btn_diff.bind(on_press=lambda inst, df=diff: self.preparer_retours_developpeur_local(df))
            self.feedback_layout.add_widget(btn_diff)
        self.interaction_layout.add_widget(self.feedback_layout)
        
        btn_suivant = Button(text="Continuer →", font_size='22sp', bold=True, size_hint=(1,None), height=dp(80), background_color=(0.12, 0.55, 0.85, 1))
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
        layout_actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), spacing=dp(10))
        btn_quitter = Button(text="← Quitter", text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.8, 0.25, 0.25, 1), font_size='18sp', bold=True)
        btn_quitter.bind(on_press=self.quitter_action)
        btn_aide = Button(text="Fiches Cours", text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.12, 0.55, 0.85, 1), font_size='18sp', bold=True)
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
                height=dp(80),
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
                 
 # ===ASSISTANT IA : ÉTAPE 1 (CLASSE) ====
    def afficher_menu_ia_parametres(self, instance):
        # Retire le bouton paramètres
        if self.btn_parametres in self.info_layout.children:
            self.info_layout.remove_widget(self.btn_parametres)
            
        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.3
        self.scroll_interaction.size_hint_y = 0.7
        self.interaction_layout.clear_widgets()
        
        self.info_label.text = "Assistant IA - Étape 1"
        self.question_label.text = f"Salut {self.nom_utilisateur}, sélectionne d'abord ta classe :"
        
        classes_disponibles = ["6ème", "5ème", "4ème", "3ème", "2nde", "1ere", "Terminale", "L1 MPC"]
        for c in classes_disponibles:
            btn = Button(
                text=f"Classe : {c}",
                font_size='18sp',
                bold=True,
                text_size=(1 * Window.width - dp(20), None),
                halign='center', 
                valign='middle',
                background_color=(0.2, 0.5, 0.8, 1),
                size_hint_y=None,
                height=dp(40)
            )
            btn.bind(on_press=lambda x, classe_choisie=c: self.etape_selection_mode(classe_choisie))
            self.interaction_layout.add_widget(btn)

        btn_retour = Button(
            text="⬅ Retour au menu",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())
        self.interaction_layout.add_widget(btn_retour)
        
    # --- AJOUT DU BOUTON MENU AVEC ICÔNE ---
        self.btn_menu_ia = Button(
            background_normal='icône_appli/menu.png',
            background_down='icône_appli/menu.png',
            size_hint=(None, None),
            size=(dp(45), dp(45)),
            pos_hint={'top': 0.98, 'right': 0.98}
        )
        self.btn_menu_ia.bind(on_press=self.ouvrir_panneau_menu_ia)
        self.root.add_widget(self.btn_menu_ia)  
        
#==== MENU LATÉRAL DE L'ASSISTANT IA ====
    def ouvrir_panneau_menu_ia(self, instance):
        # Évite de superposer plusieurs panneaux s'il est déjà ouvert
        if hasattr(self, 'layout_panneau_menu') and self.layout_panneau_menu in self.root.children:
            return
            
        self.layout_panneau_menu = FloatLayout()
        
        # Canvas noir vertical occupant la moitié gauche de l'écran (coupe l'écran en deux)
        with self.layout_panneau_menu.canvas.before:
            Color(0, 0, 0, 0.98) 
            self.rect_panneau = Rectangle(size=(Window.width * 0.5, Window.height), pos=(0, 0))
            
        # Titre du menu latéral
        lbl_titre_menu = Label(
            text="MENU RAPIDE",
            font_size='18sp',
            text_size=(0.5 * Window.width - dp(20), None),
            halign='center',
            valign='middle',
            bold=True,
            size_hint=(0.5, None),
            height=dp(50),
            pos_hint={'top': 0.9, 'x': 0}
        )
        self.layout_panneau_menu.add_widget(lbl_titre_menu)
        
        # ==== REQUÊTE ====        
        btn_requete_libre = Button(
            text="✍️ Requête & Idée personnelle",
            font_size='18sp',
            bold=True,
            text_size=(0.4 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            size_hint=(0.4, None),
            height=dp(45),
            pos_hint={'center_x': 0.25, 'top': 0.63},
            background_color=(0.2, 0.7, 0.5, 1)
        )
        btn_requete_libre.bind(on_press=lambda x: [self.fermer_panneau_menu_ia(None), self.afficher_formulaire_requete_libre(None)])
        self.layout_panneau_menu.add_widget(btn_requete_libre)


        # Bouton Accueil / Retour au menu principal dans le panneau
        btn_accueil = Button(
            text=" Accueil",
            font_size='18sp',
            text_size=(0.4 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            bold=True,
            size_hint=(0.4, None),
            height=dp(45),
            pos_hint={'center_x': 0.25, 'top': 0.75},
            background_color=(0.2, 0.5, 0.8, 1)
        )
        btn_accueil.bind(on_press=lambda x: [self.fermer_panneau_menu_ia(None), self.afficher_menu_principal_modes()])
        self.layout_panneau_menu.add_widget(btn_accueil)

        # Bouton de fermeture du panneau menu
        btn_fermer_menu = Button(
            text=" Fermer",
            font_size='16sp',
            text_size=(0.4 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            bold=True,
            size_hint=(0.4, None),
            height=dp(45),
            pos_hint={'center_x': 0.25, 'top': 0.2},
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_fermer_menu.bind(on_press=self.fermer_panneau_menu_ia)
        self.layout_panneau_menu.add_widget(btn_fermer_menu)

        # Ajout du panneau par-dessus l'écran actuel
        self.root.add_widget(self.layout_panneau_menu)

    def fermer_panneau_menu_ia(self, instance):
        if hasattr(self, 'layout_panneau_menu') and self.layout_panneau_menu in self.root.children:
            self.root.remove_widget(self.layout_panneau_menu)
            del self.layout_panneau_menu
            
       # ==== CHOIX REQUÊTE =====         
    def afficher_formulaire_requete_libre(self, instance):
        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.info_label.text = "Requêtes & Suggestions Libres"
        self.question_label.text = "Tape ton sujet, chapitre ou question, puis choisis la catégorie :"

        # Champ de texte pour la saisie libre (chapitre, matière ou question)
        self.saisie_requete_libre = TextInput(
            text='',
            hint_text="Ex: Intégrales, thermodynamique, ou question précise...",
            font_size='16sp',
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        self.interaction_layout.add_widget(self.saisie_requete_libre)

                # Catégorie sélectionnée 
        self.categorie_selectionnee = ""
        categories = ["Résumé du chapitre", "Question", "Infos sur la matière", "Infos du chapitre", "Autre"]
        self.boutons_categories = []

        for cat in categories:
            est_coche = (cat == self.categorie_selectionnee)
            # Utilisation de tes images personnalisées pour l'arrière-plan de l'icône/bouton
            img_fond = 'icône_appli/box_cocher.png' if est_coche else 'icône_appli/box_non_cocher.png'
            
            btn_cat = Button(
                text=f"    {cat}",  
                font_size='12sp',
                bold=True,
                text_size=(1 * Window.width - dp(20), None),
                halign='left',
                valign='middle',
                size_hint_y=None,
                height=dp(42),
                background_normal=img_fond,
                background_down=img_fond
            )
            btn_cat.bind(texture_size=lambda s, t: setattr(s, 'text_size', (s.width - dp(40), s.height)))
            btn_cat.categorie_nom = cat
            btn_cat.bind(on_press=self.selectionner_categorie_libre)
            self.boutons_categories.append(btn_cat)
            self.interaction_layout.add_widget(btn_cat)

        # Bouton d'envoi des données
        btn_envoyer = Button(
            text="Envoyer ma demande",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.15, 0.6, 0.3, 1)
        )
        btn_envoyer.bind(on_press=self.envoyer_requete_utilisateur_api)
        self.interaction_layout.add_widget(btn_envoyer)

        # Bouton Retour
        btn_retour = Button(
            text="⬅ Retour",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        btn_retour.bind(on_press=lambda x: self.etape_selection_mode(getattr(self, 'niveau_actuelle', '1ere')))
        self.interaction_layout.add_widget(btn_retour)

    def selectionner_categorie_libre(self, instance):
        self.categorie_selectionnee = instance.categorie_nom
        # Met à jour l'image de chaque bouton selon s'il est coché ou non
        for b in self.boutons_categories:
            if b.categorie_nom == self.categorie_selectionnee:
                b.background_normal = 'icône_appli/box_cocher.png'
                b.background_down = 'icône_appli/box_cocher.png'
            else:
                b.background_normal = 'icône_appli/box_non_cocher.png'
                b.background_down = 'icône_appli/box_non_cocher.png'

    def envoyer_requete_utilisateur_api(self, instance):
        texte_utilisateur = self.saisie_requete_libre.text.strip()
        if not texte_utilisateur:
            self.question_label.text = "⚠️ Veuillez saisir un texte avant d'envoyer !"
            return
            
        # --- GESTION DE LA LIMITE (3 requêtes par minute max) ---
        if not hasattr(self, 'historique_requetes_temps'):
            self.historique_requetes_temps = []
        
        temps_actuel = time.time()
        # Filtrer pour ne garder que les requêtes de la dernière minute (60 secondes)
        self.historique_requetes_temps = [t for t in self.historique_requetes_temps if temps_actuel - t < 60]

        if len(self.historique_requetes_temps) >= 3:
            self.question_label.text = " Doucement ! Tu as atteint la limite de 3 requêtes par minute. Attends un peu."
            return

        # Enregistrer le timestamp de cette nouvelle requête
        self.historique_requetes_temps.append(temps_actuel)

        # URL de ton API Flask sur PythonAnywhere pour collecter les avis / requêtes
        url = "https://fazadnassur.pythonanywhere.com/api/avis"
        donnees = {
            "utilisateur": getattr(self, 'nom_utilisateur', 'Anonyme'),
            "classe": getattr(self, 'classe_actuelle', 'Non spécifiée'),
            "categorie": self.categorie_selectionnee,
            "requete": texte_utilisateur
        }
        
        headers = {'Content-Type': 'application/json'}
        
        UrlRequest(
            url,
            req_body=json.dumps(donnees),
            req_headers=headers,
            method='POST',
            on_success=lambda req, res: setattr(self.question_label, 'text', "✅ Demande bien transmise au développeur ! Merci pour ton aide."),
            on_error=lambda req, err: setattr(self.question_label, 'text', f"❌ Erreur d'envoi : {err}")
        )
        
                # 2. Génération immédiate par l'IA en fonction de la catégorie choisie
        self.question_label.text = f"L'IA traite ta demande ({self.categorie_selectionnee})...\nSujet : {texte_utilisateur}"
        
        # Appel de ta fonction de génération habituelle de l'IA avec le texte et la catégorie
        self.generer_reponse_ia_libre(texte_utilisateur, self.categorie_selectionnee)

    def generer_reponse_ia_libre(self, requete, categorie):
        # On configure le comportement selon la catégorie d'exercice / de contenu demandée
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Requête Libre - {categorie}"
        self.question_label.text = f"Génération de '{requete}' ({categorie}) en cours..."
        
        # On appelle l'API Flask de génération de questions/exercices en lui passant le sujet libre
        url = "https://fazadnassur.pythonanywhere.com/api/generer_question"
        donnees_requete = {
            "niveau": getattr(self, 'niveau_actuelle', '1ere'),
            "classe": getattr(self, 'classe_actuelle', '1ere'),
            "chapitre": requete,  # On injecte le texte libre de l'utilisateur comme sujet/chapitre
            "mode": categorie     # La catégorie sert de mode de traitement pour l'IA
        }
        headers = {'Content-Type': 'application/json'}
        
        UrlRequest(
            url,
            req_body=json.dumps(donnees_requete),
            req_headers=headers,
            method='POST',
            on_success=self.recevoir_et_afficher_ia,
            on_error=lambda req, err: setattr(self.question_label, 'text', f'❌ Erreur génération IA : {err}')
        )
        
        # Bouton Retour pour revenir en arrière
        btn_retour = Button(
            text="⬅ Retour",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_retour.bind(on_press=lambda x: self.afficher_menu_ia_parametres(None))
        self.interaction_layout.add_widget(btn_retour)

# ===== ASSISTANT IA : CHOIX DU MODE======
    def etape_selection_mode(self, niveau_choisi):
        self.nettoyer_boutons_bas()
        self.niveau_actuelle = niveau_choisi
        self.interaction_layout.clear_widgets()
        
        self.info_label.text = "Assistant IA - Choix du Mode"
        self.question_label.text = f"Choisis le mode de travail pour la classe de {self.classe_actuelle} :"

        btn_ent = Button(
            text="Mode Entraînement (Question par question + Note /20)",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.1, 0.5, 0.8, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_ent.bind(on_press=lambda x: self.lancer_mode_entrainement())
        self.interaction_layout.add_widget(btn_ent)

        btn_exam = Button(
            text=" Mode Examen (Séries ou Sujets complets)",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.8, 0.4, 0.1, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_exam.bind(on_press=lambda x: self.etape_sous_menu_examen())
        self.interaction_layout.add_widget(btn_exam)

        btn_retour = Button(
            text="⬅ Retour",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_retour.bind(on_press=lambda x: self.afficher_menu_ia_parametres(None))
        self.interaction_layout.add_widget(btn_retour)

# ======= SOUS-MENU EXAMEN ===========
    def etape_sous_menu_examen(self):
        self.interaction_layout.clear_widgets()
        self.info_label.text = "Mode Examen - Type d'épreuve"
        self.question_label.text = "Choisis le format de l'examen :"

        btn_simple = Button(
            text="Examen Simple (Série de 10 ou 20 questions)",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.2, 0.6, 0.4, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_simple.bind(on_press=lambda x: self.etape_choix_nombre_questions())
        self.interaction_layout.add_widget(btn_simple)

        btn_sujet = Button(
            text="Sujet Type / Contrôle Officiel (Signé Math Quiz Comores)",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.6, 0.2, 0.6, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_sujet.bind(on_press=lambda x: self.lancer_generation_sujet_entier())
        self.interaction_layout.add_widget(btn_sujet)

        btn_retour = Button(
            text="⬅ Retour",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center',
             valign='middle',
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_retour.bind(on_press=lambda x: self.etape_selection_mode(self.niveau_actuelle))
        self.interaction_layout.add_widget(btn_retour)

    def etape_choix_nombre_questions(self):
        self.interaction_layout.clear_widgets()
        self.info_label.text = "Examen Simple - Longueur"
        self.question_label.text = "Combien de questions souhaites-tu pour cet examen ?"

        for nb in [10, 20]:
            btn_nb = Button(
                text=f" {nb} Questions",
                font_size='18sp',
                bold=True,
                text_size=(1 * Window.width - dp(20), None),
                halign='center',
                 valign='middle',
                background_color=(0.3, 0.4, 0.7, 1),
                size_hint_y=None,
                height=dp(45)
            )
            btn_nb.bind(on_press=lambda x, n=nb: self.lancer_examen_simple(n))
            self.interaction_layout.add_widget(btn_nb)

        btn_retour = Button(
            text="⬅ Retour",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_retour.bind(on_press=lambda x: self.etape_sous_menu_examen())
        self.interaction_layout.add_widget(btn_retour)

 # ====== LANCEMENT DES MODES ========
    def lancer_mode_entrainement(self):
        self.score_session = 0
        self.total_questions_session = 0
        self.requeter_ia_generer("Entraînement")

    def lancer_examen_simple(self, nb_questions):
        self.max_questions_examen = nb_questions
        self.index_examen_actuel = 0
        self.score_examen = 0
        self.historique_examen = [] # Pour stocker le récapitulatif détaillé
        self.requeter_ia_generer("Examen Simple")

    def lancer_generation_sujet_entier(self):
        self.interaction_layout.clear_widgets()
        self.info_label.text = "Sujet Officiel - Math Quiz Comores"
        self.question_label.text = f"Génération d'un sujet complet signé *Math Quiz Comores* pour la classe de {self.classe_actuelle}, cher {self.nom_utilisateur}..."
        self.appeler_api_flask(mode="Sujet Complet")

    def requeter_ia_generer(self, mode_str):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Génération IA - {mode_str}"
        
        if mode_str == "Examen Simple":
            self.index_examen_actuel += 1
            self.question_label.text = f"Question {self.index_examen_actuel}/{self.max_questions_examen} en cours de génération..."
        else:
            self.question_label.text = f"Génération par l'IA d'une question d'entraînement..."
        
        self.appeler_api_flask(mode=mode_str)

    def appeler_api_flask(self, mode):
        url = "https://fazadnassur.pythonanywhere.com/api/generer_question"
        donnees_requete = {
            "niveau": self.niveau_actuelle,
            "classe": self.classe_actuelle,
            "chapitre": getattr(self, 'chapitre_en_cours', ''),
            "mode": mode
        }
        headers = {'Content-Type': 'application/json'}
        
        UrlRequest(
            url,
            req_body=json.dumps(donnees_requete),
            req_headers=headers,
            method='POST',
            on_success=self.recevoir_et_afficher_ia,
            on_error=lambda req, err: setattr(self.question_label, 'text', f'Erreur réseau : {err}')
        )
        
        btn_retour = Button(
            text="⬅ Retour",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(45)
        )
        btn_retour.bind(on_press=lambda x: self.afficher_menu_ia_parametres(None))
        self.interaction_layout.add_widget(btn_retour)
        
# === AFFICHAGE DES QUESTIONS REÇUES ====
    def recevoir_et_afficher_ia(self, req, resultat):
        if isinstance(resultat, str):
            import json
            resultat = json.loads(resultat)
            
        self.enonce_actuel = resultat.get("enonce", "Erreur : aucune donnée reçue")
        self.bonne_reponse_ia = resultat.get("bonne_reponse", "")
        self.options_ia = resultat.get("options", [])
        self.explication_ia = resultat.get("explication", "Aucune explication fournie.")
        
        # Si c'est un sujet complet affiché d'un bloc
        if "Sujet Complet" in self.info_label.text:
            self.question_label.text = self.enonce_actuel
            self.interaction_layout.clear_widgets()
            
            btn_retour = Button(
                text="🏠 Retour Assistant IA",
                font_size='18sp',
                bold=True,
                text_size=(1 * Window.width - dp(20), None),
                halign='center', 
                valign='middle',
                background_color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(40)
            )
            btn_retour.bind(on_press=lambda x: self.afficher_menu_ia_parametres(None))
            self.interaction_layout.add_widget(btn_retour)
            return

        # Mode Question par Question (Entraînement ou Examen Simple)
        self.question_label.text = f"Question :\n{self.enonce_actuel}"
        self.interaction_layout.clear_widgets()
        
        for opt in self.options_ia:
            btn_opt = Button(
                text=opt,
                font_size='18sp',
                bold=True,
                text_size=(1 * Window.width - dp(20), None),
                halign='center', 
                valign='middle',
                background_color=(0.2, 0.4, 0.6, 1),
                size_hint_y=None,
                height=dp(40)
            )
            btn_opt.bind(on_press=lambda instance, choix=opt: self.verifier_reponse_interactive(choix))
            self.interaction_layout.add_widget(btn_opt)

# ==== VÉRIFICATION & GESTION DES NOTES ==
    def verifier_reponse_interactive(self, choix_utilisateur):
        est_correct = (choix_utilisateur.strip() == self.bonne_reponse_ia.strip())
        mode_actuel = "Examen Simple" if hasattr(self, 'max_questions_examen') and self.index_examen_actuel <= self.max_questions_examen else "Entraînement"

        if mode_actuel == "Entraînement":
            self.total_questions_session = getattr(self, 'total_questions_session', 0) + 1
            if est_correct:
                self.score_session = getattr(self, 'score_session', 0) + 1
            
            note_sur_20 = (self.score_session / self.total_questions_session) * 20
            self.interaction_layout.clear_widgets()
            
            if est_correct:
                self.question_label.text = (
                    f"EXCELLENT TRAVAIL, {self.nom_utilisateur} ! \n\n"
                    f"Question posée : {self.enonce_actuel}\n\n"
                    f"Bonne réponse \n"
                    f"Note actuelle : {note_sur_20:.2f} / 20"
                )
                btn_suite = Button(text="Question Suivante", font_size='18sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.15, 0.6, 0.3, 1), size_hint_y=None, height=dp(45))
                btn_suite.bind(on_press=lambda x: self.requeter_ia_generer("Entraînement"))
            else:
                self.question_label.text = (
                    f"Dommage {self.nom_utilisateur}, c'est une erreur \n\n"
                    f"Question posée : {self.enonce_actuel}\n"
                    f"Bonne réponse : {self.bonne_reponse_ia}\n\n"
                    f"Explication :\n{self.explication_ia}\n\n"
                    f"Note actuelle : {note_sur_20:.2f} / 20"
                )
                btn_suite = Button(text="Continuer l'entraînement", font_size='18sp', bold=True, text_size=(1 * Window.width - dp(20), None),halign='center', valign='middle', background_color=(0.8, 0.3, 0.2, 1), size_hint_y=None, height=dp(45))
                btn_suite.bind(on_press=lambda x: self.requeter_ia_generer("Entraînement"))
            
            self.interaction_layout.add_widget(btn_suite)

        else:
            # Mode Examen Simple : Stockage pour le récapitulatif final
            if est_correct:
                self.score_examen += 1
            
            self.historique_examen.append({
                "question": self.enonce_actuel,
                "choix": choix_utilisateur,
                "bonne_reponse": self.bonne_reponse_ia,
                "correct": est_correct,
                "explication": self.explication_ia
            })

            # Vérifier si l'examen est terminé
            if self.index_examen_actuel < self.max_questions_examen:
                self.requeter_ia_generer("Examen Simple")
                return
            else:
                # Affichage du récapitulatif complet de l'examen
                note_examen_20 = (self.score_examen / self.max_questions_examen) * 20
                mention = "Échec"
                if note_examen_20 >= 16: mention = "Très Bien "
                elif note_examen_20 >= 14: mention = "Bien "
                elif note_examen_20 >= 12: mention = "Assez Bien "
                elif note_examen_20 >= 10: mention = "Passable "

                recap_texte = f"RÉCAPITULATIF DE L'EXAMEN\nNote Finale : {note_examen_20:.2f} / 20\nMention : {mention}\n\n"
                for i, res in enumerate(self.historique_examen, 1):
                    statut = "" if res["correct"] else ""
                    recap_texte += f"Q{i}: {res['question']}\nVotre réponse: {res['choix']} {statut}\n"
                    if not res["correct"]:
                        recap_texte += f"Attendu: {res['bonne_reponse']} | Expl: {res['explication']}\n\n"
                        
            self.question_label.size_hint_y = None
            self.question_label.bind(
                texture_size=lambda instance, size: setattr(instance, 'height', size[1])
                     )
            self.question_label.text_size = (self.scroll_texte.width - 20, None)
            self.question_label.text = recap_texte
        self.interaction_layout.clear_widgets()

        # Bouton de retour commun
        btn_retour = Button(
            text="Retour Assistant IA",
            font_size='18sp',
            bold=True,
            text_size=(1 * Window.width - dp(20), None),
            halign='center', 
            valign='middle',
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(40)
        )
        btn_retour.bind(on_press=lambda x: self.afficher_menu_ia_parametres)
        self.interaction_layout.add_widget(btn_retour)

        
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
