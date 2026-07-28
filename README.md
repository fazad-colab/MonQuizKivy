import random
import math
import json
import os
from kivy.app import App
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
        self.main_layout = BoxLayout(orientation='vertical', padding=15, spacing=12)
        with self.main_layout.canvas.before:
            Color(0.11, 0.11, 0.14, 1) 
            self.rect = RoundedRectangle(size=self.main_layout.size, pos=self.main_layout.pos, radius=[10])
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # 1. Zone d'en-tête (Informations de profil et Chronomètre) - RESTE EN HAUT MAIS COMPACT
        self.info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=90, spacing=10)
        self.info_label = Label(text="Initialisation en cours...", font_size='18sp', bold=True, color=(1, 0.84, 0, 1), halign='left', valign='middle')
        self.info_label.bind(size=self._update_text_size)
        self.chrono_label = Label(text="", font_size='22sp', bold=True, color=(1, 0.35, 0.35, 1), halign='right', valign='middle')
        self.chrono_label.bind(size=self._update_text_size)
        self.info_layout.add_widget(self.info_label)
        self.info_layout.add_widget(self.chrono_label)
        self.main_layout.add_widget(self.info_layout)
        
        # 2. Zone d'affichage des énoncés de questions ou des cours - MILIEU SUPÉRIEUR
        self.scroll_texte = ScrollView(size_hint_y=0.32, do_scroll_x=False, do_scroll_y=True)
        self.question_label = Label(text="", font_size='20sp', halign='center', valign='middle', size_hint_y=None, color=(1, 1, 1, 1))
        self.question_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - 20, None)))
        self.question_label.bind(texture_size=lambda instance, size: setattr(instance, 'height', max(size[1] + 30, 220)))
        self.scroll_texte.add_widget(self.question_label)
        self.main_layout.add_widget(self.scroll_texte)
        
        # 3. Zone d'interaction dynamique principale (Boutons de réponses, Saisie, Menus) - BAS DU POUCE
        self.scroll_interaction = ScrollView(size_hint_y=0.68, do_scroll_x=False, do_scroll_y=True)
        self.interaction_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        self.interaction_layout.bind(minimum_height=self.interaction_layout.setter('height'))
        self.scroll_interaction.add_widget(self.interaction_layout)
        self.main_layout.add_widget(self.scroll_interaction)
        
        # Bouton persistant dédié pour le retour menu (Placé stratégiquement sous les boutons ou réajusté)
        self.btn_menu_persistant = Button(text="Revenir au Menu Principal", font_size='20sp', bold=True, size_hint_y=None, height=110, background_color=(0.12, 0.53, 0.9, 1))
        self.btn_menu_persistant.bind(on_press=self.action_retour_menu_persistant)
        
        # Bouton unique de retour pour les vues isolées (S'affichera tout en bas du main_layout)
        self.btn_retour_isole = Button(text="← Retour Évolution", size_hint_y=None, height=110, font_size='22sp', bold=True, background_color=(0.15, 0.45, 0.75, 1))
        
        # Charger l'historique et vérifier l'identité locale
        self.charger_donnees_locales()
        
        # Lancement de la tâche récurrente de synchronisation en arrière-plan (toutes les 15 secondes)
        Clock.schedule_interval(self.tenter_synchronisation_file_attente, 15.0)
        
        if not self.nom_utilisateur:
            self.demander_nom_utilisateur()
        else:
            self.afficher_menu_principal_modes()
            
        return self.main_layout
    def afficher_question_math(self, enonce_latex):
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

    # Action du bouton tout en bas de l'écran pour nettoyer proprement l'état
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
        self.arreter_chrono()
        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.chrono_label.text = ""
        self.interaction_layout.clear_widgets()
        
        rang_actuel = self.obtenir_rang_actuel()
        self.info_label.text = f"{self.nom_utilisateur}\n{rang_actuel}"
        self.question_label.text = f" Bienvenue sur Math Quiz,cher\n{self.nom_utilisateur} \n\nDévelopeur officiel : {self.nom_developpeur}\n\nSélectionne une activité :"
        btn_entrainement = Button(text=" Entraînement Rythmé ", font_size='22sp', bold=True, background_color=(0.2, 0.65, 0.4, 1), size_hint_y=None, height=140)
        btn_entrainement.bind(on_press=lambda x: self.selectionner_mode("Entraînement"))
        
        btn_examen = Button(text="Examen Blanc ", font_size='22sp', bold=True, background_color=(0.9, 0.5, 0.15, 1), size_hint_y=None, height=140)
        btn_examen.bind(on_press=lambda x: self.selectionner_mode("Examen"))
        
        btn_stats = Button(text=" Salle des Rangs & Statistiques", font_size='22sp', bold=True, background_color=(0.55, 0.3, 0.75, 1), size_hint_y=None, height=140)
        btn_stats.bind(on_press=self.afficher_sous_menu_evolution)

        btn_avis_general = Button(text="Laisser un avis au Développeur", font_size='22sp', bold=True, background_color=(0.12, 0.53, 0.9, 1), size_hint_y=None, height=140)
        btn_avis_general.bind(on_press=self.afficher_interface_avis_general)
        
        self.interaction_layout.add_widget(btn_entrainement)
        self.interaction_layout.add_widget(btn_examen)
        self.interaction_layout.add_widget(btn_stats)
        self.interaction_layout.add_widget(btn_avis_general)

    # --- SOUS-MENUS DU PANNEAU D'ÉVOLUTION ---
    def afficher_sous_menu_evolution(self, instance):
        self.nettoyer_boutons_bas()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.interaction_layout.clear_widgets()
        self.info_label.text = " Menu Évolution"
        self.question_label.text = f"Mon cher {self.nom_utilisateur}, bienvenue dans ton espace de suivi.\nSélectionne la section à consulter :"

        btn_profil_rangs = Button(text=" Mon Grade, XP & Rythme Actuel", font_size='22sp', bold=True, background_color=(0.2, 0.5, 0.8, 1), size_hint_y=None, height=140)
        btn_profil_rangs.bind(on_press=self.afficher_tableau_de_bord_stats)

        btn_liste_grades = Button(text=" Liste Officielle des Rangs", font_size='22sp', bold=True, background_color=(0.55, 0.3, 0.75, 1), size_hint_y=None, height=140)
        btn_liste_grades.bind(on_press=self.afficher_liste_complete_des_rangs)

        btn_modules_maitrise = Button(text=" Maîtrise des Chapitres", font_size='22sp', bold=True, background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=140)
        btn_modules_maitrise.bind(on_press=self.afficher_maitrise_des_modules)

        btn_retour = Button(text="← Revenir à l'Accueil", font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1), size_hint_y=None, height=140)
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
        
        layout_liste_scroll = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=15)
        layout_liste_scroll.bind(minimum_height=layout_liste_scroll.setter('height'))

        lbl_intro = Label(text="Hiérarchie dynamique indexée sur les bonus de paliers (+5% RP requis par couleur) :", font_size='18sp', color=(0.8, 0.8, 0.8, 1), size_hint_y=None, height=80)
        lbl_intro.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
        layout_liste_scroll.add_widget(lbl_intro)

        for rg in self.LISTE_RANGS:
            lbl_rg = Label(text=f"• {rg}", font_size='20sp', halign='left', size_hint_y=None, height=55)
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

        layout_modules_scroll = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=15)
        layout_modules_scroll.bind(minimum_height=layout_modules_scroll.setter('height'))

        lbl_titre = Label(text="Suivi complet par module officiel :", font_size='20sp', bold=True, size_hint_y=None, height=55, color=(0.9, 0.9, 0.9, 1))
        layout_modules_scroll.add_widget(lbl_titre)

        aucun_suivi = True
        for chap, valeurs in self.stats_chapitres.items():
            reussites, total = valeurs[0], valeurs[1]
            if total > 0:
                aucun_suivi = False
                taux = (reussites / total) * 100
                box_item = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=8)
                lbl_item = Label(text=f"• {chap} : {reussites}/{total} Corrects", font_size='18sp', halign='left')
                lbl_item.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
                pb = ProgressBar(max=100, value=taux, size_hint_y=None, height=25)
                box_item.add_widget(lbl_item)
                box_item.add_widget(pb)
                layout_modules_scroll.add_widget(box_item)

        if aucun_suivi:
            lbl_vide = Label(text="Aucune statistique enregistrée pour le moment.\nCommence une partie !", font_size='20sp', halign='center', size_hint_y=None, height=150, color=(0.6, 0.6, 0.6, 1))
            layout_modules_scroll.add_widget(lbl_vide)

        self.scroll_texte.add_widget(layout_modules_scroll)

        # Bouton placé directement tout en bas de l'écran principal
        self.btn_retour_isole.text = "← Retour Évolution"
        self.btn_retour_isole.bind(on_press=self.restaurer_ecran_initial_apres_stats)
        self.main_layout.add_widget(self.btn_retour_isole)

    def afficher_interface_avis_general(self, instance):
        self.nettoyer_boutons_bas()
        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.info_label.text = "Retour Développeur"
        self.question_label.text = f"Mon cher ami {self.nom_utilisateur}, dis-moi ce que je devrais modifier ou ajouter dans mon application, et laisse ton numéro WhatsApp pour plus de communication, merci :"
        
        self.input_avis_global = TextInput(hint_text="Écris tes remarques ici...", multiline=True, size_hint_y=None, height=180, font_size='18sp')
        self.input_whatsapp_global = TextInput(hint_text="Ton numéro WhatsApp (Optionnel)...", multiline=False, size_hint_y=None, height=80, font_size='18sp')
        
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=130, spacing=15)
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

    def afficher_menu_niveaux(self):
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
            btn = Button(text=nv, font_size='22sp', background_color=(0.15, 0.45, 0.75, 1), size_hint_y=None, height=130)
            btn.bind(on_press=lambda inst, n=nv, list_cl=niveaux[nv]: self.afficher_menu_classes(n, list_cl))
            self.interaction_layout.add_widget(btn)

        btn_retour = Button(text="← Revenir à l'Accueil", size_hint_y=None, height=130, font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_principal_modes())
        self.interaction_layout.add_widget(btn_retour)

    def afficher_menu_classes(self, niveau, list_cl):
        self.interaction_layout.clear_widgets()
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        self.question_label.text = f"Sélectionne la classe pour charger le programme associé :"
        
        for cl in list_cl:
            btn = Button(text=cl, font_size='22sp', background_color=(0.18, 0.58, 0.4, 1), size_hint_y=None, height=130)
            btn.bind(on_press=self.initialiser_session_classe)
            self.interaction_layout.add_widget(btn)

        btn_retour = Button(text="← Étape Précédente", size_hint_y=None, height=130, font_size='22sp', bold=True, background_color=(0.75, 0.2, 0.2, 1))
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
        self.chrono_label.text = f"⏱{self.temps_restant}s"
        self.evenement_chrono = Clock.schedule_interval(self.mettre_a_jour_chrono_entrainement, 1.0)

    def mettre_a_jour_chrono_entrainement(self, dt):
        self.temps_restant -= 1
        self.chrono_label.text = f"⏱{self.temps_restant}s"
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
        
        layout_stats_scroll = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=15)
        layout_stats_scroll.bind(minimum_height=layout_stats_scroll.setter('height'))
        
        rang_actuel, rp_courant, seuil_requis, _ = self.determiner_rang_et_details()
        lbl_rang_titre = Label(text=f"GRADE DE SAISON : {rang_actuel}\n SCORE DE RANG : {self.points_de_rang} PR", 
                               font_size='22sp', bold=True, size_hint_y=None, height=100, halign='center', color=(1, 0.84, 0, 1))
        lbl_rang_titre.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
        layout_stats_scroll.add_widget(lbl_rang_titre)
        
        jauge_interactive = BoxLayout(size_hint_y=None, height=60)
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
        
        lbl_points_restants = Label(text=f" {seuil_requis - rp_courant} PR avant le prochain Échelon !", font_size='18sp', color=(0.2, 0.8, 1, 1), size_hint_y=None, height=45)
        layout_stats_scroll.add_widget(jauge_interactive)
        layout_stats_scroll.add_widget(lbl_points_restants)
        
        xp_requis = self.niveau_profil * 50
        box_xp = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=8)
        lbl_xp = Label(text=f"Niveau du Profil : Lvl {self.niveau_profil} ({self.xp} / {xp_requis} XP)", font_size='18sp', bold=True)
        pb_xp = ProgressBar(max=xp_requis, value=self.xp, size_hint_y=None, height=25)
        box_xp.add_widget(lbl_xp)
        box_xp.add_widget(pb_xp)
        layout_stats_scroll.add_widget(box_xp)
        
        lbl_analyse_vitesse = Label(size_hint_y=None, font_size='18sp', bold=True, halign='center')
        lbl_analyse_vitesse.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 10, None)))
        lbl_analyse_vitesse.bind(texture_size=lambda inst, size: setattr(inst, 'height', max(size[1] + 30, 100)))
        
        if len(self.historique_scores) < 2:
            lbl_analyse_vitesse.text = "ANALYSE : En attente de matches.\nEnchaîne des sessions de quiz pour tracer ta courbe !"
            lbl_analyse_vitesse.color = (0.7, 0.7, 0.7, 1)
        else:
            derniers = self.historique_scores[-5:]
            if all(derniers[i] < derniers[i+1] for i in range(len(derniers)-1)):
                lbl_analyse_vitesse.text = " RYTHME : ÉVOLUTION GÉOMÉTRIQUE !\nTu massacres le classement. Tes performances augmentent de façon fulgurante."
                lbl_analyse_vitesse.color = (0.3, 0.9, 0.5, 1)
            elif all(derniers[i] > derniers[i+1] for i in range(len(derniers)-1)):
                lbl_analyse_vitesse.text = "⚠SÉRIE DE DÉFAITES : CHUTE DE SÉCURITÉ !\nAttention , tu perds des points de rang. Révise tes fiches."
                lbl_analyse_vitesse.color = (1, 0.3, 0.3, 1)
            else:
                lbl_analyse_vitesse.text = "⚖ TRAJECTOIRE : CONSTANTE ET STABLE.\nTon niveau actuel est parfaitement ancré."
                lbl_analyse_vitesse.color = (0.2, 0.6, 1, 1)
        layout_stats_scroll.add_widget(lbl_analyse_vitesse)
        
        btn_regles_rang = Button(text="ℹ Comment fonctionne le système de Rang ?", size_hint_y=None, height=90, background_color=(0.2, 0.2, 0.25, 1), font_size='18sp')
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
            "⚙ SYSTÈME DE RANGS MATH QUIZ COMORES\n\n"
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
        self.interaction_layout.clear_widgets()
        
        # Sécurité proportions
        self.scroll_texte.size_hint_y = 0.32
        self.scroll_interaction.size_hint_y = 0.68
        
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
                height=130,
                text_size=(None, None), 
                halign='center',        
                valign='middle'         
            )
            
            btn_opt.padding = [10,10]
            btn_opt.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0] - 20, None)))
            
            btn_opt.bind(on_press=self.verifier_choix_entrainement)
            self.interaction_layout.add_widget(btn_opt)

        layout_actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=110, spacing=10)
        btn_quitter = Button(text="← Quitter", background_color=(0.8, 0.25, 0.25, 1), font_size='18sp', bold=True)
        btn_quitter.bind(on_press=self.quitter_action)
        btn_aide = Button(text="Fiches Cours", background_color=(0.12, 0.55, 0.85, 1), font_size='18sp', bold=True)
        btn_aide.bind(on_press=self.afficher_formulaire_cours)
        layout_actions.add_widget(btn_quitter)
        layout_actions.add_widget(btn_aide)
        self.interaction_layout.add_widget(layout_actions)

        self.lancer_chrono_entrainement()

    def quitter_action(self, instance):
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
        self.label_flou = Label(text="C'est encore flou ? Écris-nous ci-dessous :", font_size='18sp', size_hint_y=None, height=55, color=(0.8, 0.8, 0.8, 1))
        self.interaction_layout.add_widget(self.label_flou)
        
        self.input_avis_texte = TextInput(hint_text="Précise ta difficulté ici...", multiline=True, size_hint_y=None, height=130, font_size='18sp')
        self.input_whatsapp_tek = TextInput(hint_text="Ton numéro WhatsApp...", multiline=False, size_hint_y=None, height=75, font_size='18sp')
        
        self.interaction_layout.add_widget(self.input_avis_texte)
        self.interaction_layout.add_widget(self.input_whatsapp_tek)
        
        self.feedback_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)
        for diff in ["Simple", "Abordable", "Moyen", "Complexe"]:
            btn_diff = Button(text=diff, font_size='16sp', bold=True, background_color=(0.35, 0.35, 0.38, 1))
            btn_diff.bind(on_press=lambda inst, df=diff: self.preparer_retours_developpeur_local(df))
            self.feedback_layout.add_widget(btn_diff)
        self.interaction_layout.add_widget(self.feedback_layout)
        
        btn_suivant = Button(text="Continuer →", font_size='22sp', bold=True, size_hint_y=None, height=140, background_color=(0.12, 0.55, 0.85, 1))
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
        self.interaction_layout.clear_widgets()
        
        # --- CONFIGURATION DES PROPORTIONS (Espace pour le haut / bas) ---
        # On donne plus d'espace en haut pour les énoncés et explications
        self.scroll_texte.size_hint_y = 0.45
        self.scroll_interaction.size_hint_y = 0.55
        
        chapitre_cible = self.examen_questions[self.examen_index_actuel]
        self.chapitre_en_cours = chapitre_cible
        
        self.info_label.text = f"⚡ MODE EXAMEN\n Question {self.examen_index_actuel + 1}/10"
        enonce, correct, opts, exp = self.moteur_generateur_mathematique(self.classe_actuelle, chapitre_cible)
        
        self.question_label.text = enonce
        self.bonne_reponse = str(correct)
        self.explication_erreur = exp
        
        liste_options = list(set([str(o) for o in opts]))
        if str(correct) not in liste_options: 
            liste_options.append(str(correct))
        random.shuffle(liste_options)
        
        # --- 1. AJOUT DES BOUTONS DE NAVIGATION (Quitter / Fiches) TOUT EN BAS ---
        layout_actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)
        btn_quitter = Button(text="← Quitter", background_color=(0.8, 0.25, 0.25, 1), font_size='18sp', bold=True)
        btn_quitter.bind(on_press=self.quitter_action)
        btn_aide = Button(text="Fiches Cours", background_color=(0.12, 0.55, 0.85, 1), font_size='18sp', bold=True)
        btn_aide.bind(on_press=self.afficher_formulaire_cours)
        layout_actions.add_widget(btn_quitter)
        layout_actions.add_widget(btn_aide)

        # --- 2. BOUTONS DE RÉPONSES AU-DESSUS DES ACTIONS ---
        for opt in liste_options:
            btn_opt = Button(
                text=opt, 
                font_size='22sp', 
                bold=True, 
                size_hint_y=None, 
                height=110,
                text_size=(None, None), 
                halign='center', 
                valign='middle' 
            )
            btn_opt.padding = [10, 10]
            btn_opt.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0] - 20, None)))
            btn_opt.bind(on_press=self.valider_choix_examen)
            self.interaction_layout.add_widget(btn_opt)

        # On ajoute les boutons de bas de page à la toute fin du conteneur
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
        
        # Ajustement des proportions pour le bilan
        self.scroll_texte.size_hint_y = 0.52
        self.scroll_interaction.size_hint_y = 0.48
        
        graph_widget = BoxLayout(orientation='vertical', size_hint_y=None, height=220, padding=15)
        with graph_widget.canvas.before:
            Color(0.14, 0.14, 0.18, 1)
            Rectangle(pos=graph_widget.pos, size=graph_widget.size)
        
        lbl_rank_visuel = Label(text=f" RÉSUMÉ DE FIN DE SAISON - {mention}\nGRADE ACTUEL : {rang_actuel}\n TOTAL SCORE : {self.points_de_rang} PR", 
                                font_size='18sp', bold=True, color=(1, 1, 1, 1), halign='center')
        graph_widget.add_widget(lbl_rank_visuel)
        
        jauge_box = BoxLayout(size_hint_y=None, height=50, padding=[20, 0, 20, 0])
        _, rp_c, s_r, _ = self.determiner_rang_et_details()
        valeur_jauge = min(100, int((float(rp_c) / float(s_r)) * 100))
        pb_ff_style = ProgressBar(max=100, value=valeur_jauge, size_hint_y=None, height=35)
        jauge_box.add_widget(pb_ff_style)
        graph_widget.add_widget(jauge_box)
        
        self.interaction_layout.add_widget(graph_widget)
        
        bilan_texte = f"RÉSULTAT EXAMEN DE {self.nom_utilisateur}\nNote globale : {note_sur_20:.1f}/20\n\n--- CORRECTIONS ALGEBRIQUES INDIVIDUELLES ---\n"
        
        for i, (q, recu, bon, exp) in enumerate(self.examen_reponses_eleve):
            if recu == bon:
                bilan_texte += f"\n Question {i+1} : CORRECT\n"
            else:
                bilan_texte += f"\n Question {i+1} : REVOIR\nSaisie : {recu} | Attendu : {bon}\n\nDÉMONSTRATION ALGÉBRIQUE :\n{exp}\n"
                
        self.question_label.text = bilan_texte
        
        if self.btn_menu_persistant not in self.main_layout.children:
            self.main_layout.add_widget(self.btn_menu_persistant)

    # --- MOTEUR DE GÉNÉRATION DES ENONCÉS MULTI-VARIANTES ---
    def moteur_generateur_mathematique(self, classe_cible, chapitre_cible):
        enonce, correct, opts, exp = "", "", [], ""
        variante = random.choice(["V1", "V2", "V3"])
        
        _, _, _, index_grade = self.determiner_rang_et_details()
        facteur_diff = 1 + (index_grade // 5) + (self.niveau_profil // 3)
        
        if chapitre_cible in ["Arithmétiques"]:
            if variante == "V1":
                div = random.choice([2,4,8,1,7,6, 3, 5, 9])
                depart = random.randint(100 * facteur_diff, 999 * facteur_diff)
                vrai = depart - (depart % div)
                f1, f2 = vrai + random.randint(1, div-1), vrai - random.randint(1, 4)
                if f2 == vrai: f2 -= 1
                enonce = f"Lequel de ces nombres est divisible par {div} ?"
                correct = str(vrai)
                opts = [correct, str(f1), str(f2)]
                exp = f"n ≡ 0 [mod {div}]\n{vrai} = {div} × {vrai // div} + 0\nReste = 0"
            elif variante == "V2":
                n = random.randint(11 * facteur_diff, 49 * facteur_diff)
                enonce = f"Le nombre {n} est-il un nombre premier ?"
                est_premier = all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))
                correct = "Oui" if est_premier else "Non"
                opts = ["Oui", "Non"]
                if est_premier:
                    exp = f"∀ p ≤ √{n} ({int(math.sqrt(n))}), p ∤ {n}\nDiviseurs = {{1, {n}}}"
                else:
                    facteur = next(i for i in range(2, n) if n % i == 0)
                    exp = f"{n} = {facteur} × {n//facteur}\nDiviseurs ⊃ {{1, {facteur}, {n}}}"
            elif variente == "V3":
                a, b = random.randint(4, 99) * facteur_diff, random.randint(3, 7) * facteur_diff
                enonce = f"Quel est le reste de la division euclidienne de {a*b + 2} par {a} ?"
                correct = "2"
                opts = ["2", "0", str(b)]
                exp = f"D = d × q + r, 0 ≤ r < d\n{a*b + 2} = {a} × {b} + 2\n0 ≤ 2 < {a} ⇒ r = 2"

        elif chapitre_cible == "Droites et Segments":
            if variante == "V1":
                enonce = f"Si deux droites (D1) et (D2) sont toutes deux perpendiculaires à une même troisième droite (D3), alors (D1) et (D2) sont :"
                correct = "Parallèles"
                opts = [correct, "Perpendiculaires", "Sécantes"]
                exp = "(D1) ⊥ (D3) ⇒ vec(u1) · vec(u3) = 0\n(D2) ⊥ (D3) ⇒ vec(u2) · vec(u3) = 0\n⇒ vec(u1) // vec(u2) ⇒ (D1) // (D2)"
            elif variante == "V2":
                longueur = 12 * facteur_diff
                enonce = f"Si le segment [AB] mesure {longueur} cm et que le point M est défini comme son milieu géométrique, quelle est la longueur du segment [AM] ?"
                correct = f"{longueur // 2} cm"
                opts = [f"{longueur // 2} cm", f"{longueur * 2} cm", f"{longueur // 3} cm"]
                exp = "M ∈ [AB] et AM = MB\nAB = AM + MB = 2AM\nAM = AB / 2"
            elif variante == "V3":
                enonce = f"Combien de points d'intersection possèdent deux droites de l'espace plane qui sont strictly parallèles ?"
                correct = "0"
                opts = ["0", "1", "Une infinité"]
                exp = "(D1) // (D2) ⇔ (D1) ∩ (D2) = ∅\nCard(∅) = 0"

        elif chapitre_cible == "Nombres décimaux":
            if variante == "V1":
                c, d, m = random.randint(1, 99) * facteur_diff, random.randint(1, 99), random.randint(1, 99)
                enonce = f"Déterminez l'écriture décimale standard du nombre : {c} × 10 + {d}/10 + {m}/1000"
                val = (c * 10) + (d / 10) + (m / 1000)
                correct = f"{val}".replace('.', ',')
                opts = [correct, f"{c}{d},{m}", f"{c}0,{d}{m}"]
                exp = f"{c} × 10¹ = {c*10}\n{d} × 10⁻¹ = {d/10}\n{m} × 10⁻³ = {m/1000}\nSomme = {val}"    
            elif variante == "V2":
                n = (random.randint(10, 99) * facteur_diff) / 10
                enonce = f"Quelle est la partie entière du nombre décimal {n} ?"
                correct = str(int(n))
                opts = [correct, str(int(n*10) % 10), f"{n}"]
                exp = f"x = E(x) + r, r ∈ [0, 1[\n{int(n)} ≤ {n} < {int(n)+1}\nE({n}) = {int(n)}"
            elif variante =="V3":
                enonce = f"Multiplier un nombre réel fini par le coefficient décimal 0,1 revient mathématiquement à le :"
                correct = "Diviser par 10"
                opts = ["Diviser par 10", "Multiplier par 10", "Diviser par 100"]
                exp = f"0,1 = 1/10\nx × 0,1 = x × (1/10) = x / 10"

        elif chapitre_cible in ["Les angles", "Angles"]:
            if variante == "V1":
                ang = random.randint(15, 99)
                enonce = f"Un angle géométrique mesurant exactement {ang}° est qualifié de :"
                correct = "Aigu"
                opts = ["Aigu", "Obtus", "Droit"]
                exp = f"0° < θ < 90°\n0° < {ang}° < 90° ⇒ Angle Aigu"
            elif variante == "V2":
                ang = random.randint(91, 175)
                enonce = f"Un angle géométrique mesurant exactement {ang}° est qualifié de :"
                correct = "Obtus"
                opts = ["Aigu", "Obtus", "Droit"]
                exp = f"90° < θ < 180°\n90° < {ang}° < 180° ⇒ Angle Obtus"
            elif variante =="V3":
                prem_ang = random.choice([30, 45, 60])
                enonce = f"Si deux angles sont dits complémentaires et que le premier vaut {prem_ang}°, quelle est la mesure du second ?"
                correct = f"{90 - prem_ang}°"
                opts = [f"{90 - prem_ang}°", f"{180 - prem_ang}°", "90°"]
                exp = "α + β = 90°"

        elif chapitre_cible == "Fraction":
            num = random.randint(1, 99) * facteur_diff
            den = random.randint(1, 99)
            if variante == "V1":
                enonce = f"Déterminez la value décimale exacte associée au quotient rationnel {num}/{den} :"
                correct = f"{num/den}".replace('.', ',')
                opts = [correct, f"{num},{den}", f"{den/num}".replace('.', ',')]
                exp = f"x = {num} ÷ {den} = {num/den}"
            elif variante == "V2":
                enonce = f"Simplifiez au maximum la fraction rationnelle suivante : {num*3}/{den*3}"
                correct = f"{num}/{den}"
                opts = [correct, f"{num*2}/{den*2}", "1/2"]
                exp = f"Simplification par 3 ⇒ F = {num}/{den}"
            elif variante == "V3":
                enonce = f"Effectuez le calcul de la somme rationnelle suivante : {num}/{den} + 1/{den}"
                correct = f"{num+1}/{den}"
                opts = [correct, f"{num+1}/{den*2}", f"{num+2}/{den}"]
                exp = f"a/c + b/c = (a+b)/c"

        elif chapitre_cible in ["Triangles", "Les triangles"]:
            if variante == "V1":
                enonce = "Si dans un triangle, la somme des carrés des longueurs des deux plus petits côtés est strictement égale au carré de la longueur du plus grand côté, que peut-on affirmer ?"
                correct = "Rectangle"
                opts = ["Rectangle", "Isocèle", "Équilatéral"]
                exp = "Réciproque de Pythagore :\nAB² + AC² = BC² ⇒ ̂A = 90°"
            elif variante == "V2":
                enonce = "Un triangle plane possédant trois côtés de longueurs rigoureusement identiques est défini comme un triangle :"
                correct = "Équilatéral"
                opts = ["Équilatéral", "Isocèle", "Scalène"]
                exp = "AB = BC = CA"
            elif variante == "V3":
                enonce = "En géométrie euclidienne plane, la somme des mesures des angles intérieurs de tout triangle est invariante et vaut :"
                correct = "180°"
                opts = ["180°", "360°", "90°"]
                exp = "̂A + ̂B + ̂C = π rad = 180°"

        elif chapitre_cible == "Organisation des calculs":
            a, b, c = random.randint(1, 99) * facteur_diff, random.randint(1, 99), random.randint(1, 99)
            if variante == "V1":
                enonce = f"Calculez la valeur numérique de l'expression suivante en respectant les priorités opératoires : {a} + {b} × {c}"
                correct = str(a + (b * c))
                opts = [correct, str((a + b) * c), str(a * b + c)]
                exp = f"Priorité opératoire (×) :\n{a} + {b} × {c} = {a} + {b*c}"
            elif variante == "V2":
                enonce = f"Calculez la valeur numérique de l'expression : ({a} + {b}) × {c}"
                correct = str((a + b) * c)
                opts = [correct, str(a + b * c), str(a * b + c)]
                exp = f"Priorité des parenthèses"
            elif variante == "V3":
                enonce = f"Calculez la valeur de l'expression suivante : {a*b} ÷ {b} + {c}"
                correct = str(a + c)
                opts = [correct, str(a*b // (b+c)), str(a)]
                exp = f"De gauche à droite"

        elif chapitre_cible in ["Cercle et parallélogramme", "Cercle"]:
            r = random.randint(5, 40) * facteur_diff
            if variante == "V1":
                enonce = f"Si un cercle (C) possède un rayon de mesure R = {r} cm, quelle est la mesure exacte de son diamètre ?"
                correct = f"{r * 2} cm"
                opts = [correct, f"{r} cm", f"{r // 2} cm"]
                exp = f"D = 2 × R"
            elif variante == "V2":
                enonce = f"Si un quadrilatère non croisé possède ses côtés opposés deux à deux parallèles, il s'agit par définition d'un :"
                correct = "Parallélogramme"
                opts = ["Parallélogramme", "Trapèze", "Cerf-volant"]
                exp = "(AB) // (CD) et (AD) // (BC) ⇒ Parallélogramme"
            elif variante == "V3":
                enonce = f"La droite plane qui intersecte un cercle en exactement deux points géométriques distincts est qualifiée de :"
                correct = "Sécante"
                opts = ["Sécante", "Tangente", "Corde"]
                exp = "Card(D ∩ C) = 2 ⇒ Droite Sécante"

        elif chapitre_cible in ["Entier relatifs et nombres décimaux relatifs", "Nombres décimaux relatifs"]:
            n1, n2 = random.randint(-100, -5) * facteur_diff, random.randint(2, 95)
            if variante == "V1":
                enonce = f"Calculez la somme algébrique dans Z des deux éléments suivants : ({n1}) + ({n2})"
                correct = str(n1 + n2)
                opts = [correct, str(n1 - n2), str(abs(n1) + n2)]
                exp = f"Addition de nombres relatifs signés"
            elif variante == "V2":
                enonce = f"Calculez le produit relatif suivant : (-2) × ({n2})"
                correct = str(-2 * n2)
                opts = [correct, str(2 * n2), str(-2 + n2)]
                exp = f"(-) × (+) = (-)"
            elif variante =="V3":
                enonce = f"Déterminez l'élément symétrique pour la loi d'addition (l'opposé) du nombre négatif {n1} :"
                correct = str(-n1)
                opts = [correct, str(n1), "0"]
                exp = f"x + y = 0 ⇒ y = -x"

        elif chapitre_cible in ["Symétrie centrale et axiale", "Symétrie centrale et orthogonale", "Symétrie centrale et Axiale"]:
            if variante == "V1":
                enonce = "Quelle transformation géométrique plane correspond formellement à une rotation d'angle π (180°) autour d'un point fixe ?"
                correct = "Symétrie centrale"
                opts = ["Symétrie centrale", "Symétrie axiale", "Translation"]
                exp = "R(O, π) : vec(OM') = -vec(OM) ⇔ Symétrie Centrale"
            elif variante == "V2":
                enonce = "Si un point A' est défini comme le symétrique d'un point A par rapport à un centre de symétrie O, quelle est la proposition exacte ?"
                correct = "Le milieu de [AA']"
                opts = ["Le milieu de [AA']", "L'extrémité de [AA']", "Perpendiculaire"]
                exp = "O est le milieu de [AA']"
            elif variante =="V3":
                enonce = "Sous l'action d'une symétrie axiale (orthogonale), quelles grandeurs topologiques des figures sont invariantes ?"
                correct = "Les longueurs et les aires"
                opts = ["Les longueurs et les aires", "Uniquement l'orientation", "Rien"]
                exp = "Isométrie indirecte ⇒ Conservation métrique"

        elif chapitre_cible in ["Initiation aux calculs littéraux", "Calcul littérale", "Calcul sur les expressions algébriques"]:
            a,b,c = random.randint(2, 99) * facteur_diff, random.randint(1,99), random.randint(1,99)
            if variante == "V1":
                enonce = f"Réduisez l'expression littérale suivante en factorisant par la variable x : {a}x + {b}x - {c}x"
                correct = f"{a + b - c}x"
                opts = [correct, f"{a + b - c}x", f"{a + 2}x²",f"{a - b + c}x"]
                exp = f"({a} + {b} - {c}) × x =( {a}+{b - c} )x ={a + b - c}"
            elif variante == "V2":
                enonce = f"Développez l'expression algébrique suivante en appliquant la distributivité simple : {a} × (x + 2)"
                correct = f"{a}x + {a*2}"
                opts = [correct, f"{a}x + 2", f"{a+2}x"]
                exp = f"{a}x + {a*2}"
            elif varuante == "V3":
                enonce = f"Calculez la valeur numérique prise par l'expression polynomiale (2x + 5) sous l'évaluation x = {3 * facteur_diff}"
                correct = str(2 * (3 * facteur_diff) + 5)
                opts = [correct, str(2 * (3 * facteur_diff)), "11"]
                exp = f"Substitution directe de la variable x"

        elif chapitre_cible == "Proportionnalité":
            val = random.randint(3, 99) * facteur_diff
            if variante == "V1":
                enonce = f"Si un lot homogène de 2 objets possède un prix de {2*val} KMF, déterminez par l'intensité géométrique le prix de 5 objets."
                correct = f"{5 * val} KMF"
                opts = [correct, f"{4 * val} KMF", f"{6 * val} KMF"]
                exp = f"k = {2*val} / 2 = {val}\nf(5) = 5 × {val}"
            elif variante == "V2":
                enonce = "Dans un tableau de proportionnalité reliant deux variables x et y, le coefficient linéaire k s'obtient par la relation :"
                correct = "Divisant une value du bas par celle du haut"
                opts = ["Divisant une valeur du bas par celle du haut", "Multipliant les deux", "Soustrayant"]
                exp = "y = k × x ⇒ k = y / x"
            elif variante == "V3":
                enonce = "Dans le cadre d'un mouvement rectiligne uniforme (vitesse constante), doubler le temps de parcours Δt implique de :"
                correct = "Doubler la distance"
                opts = ["Doubler la distance", "Diviser la distance par 2", "Laisser la distance identique"]
                exp = "d = v × t"

        elif chapitre_cible in ["Cube – Pavé droit – Cylindre", "Prisme droit", "Pyramide", "Pyramide et cône de révolution", "Pyramide et cône"]:
            c = random.randint(2, 99) * facteur_diff
            if variante == "V1":
                enonce = f"Calculez le volume tridimensionnel exact d'un cube dont l'arête mesure {c} cm."
                correct = f"{c**3} cm³"
                opts = [correct, f"{c*3} cm³", f"{c**2} cm³"]
                exp = f"V = c³ = {c}³"
            elif variante == "V2":
                enonce = "Combien de faces bidimensionnelles planes possède un pavé droit (parallélépipède rectangle) ?"
                correct = "6"
                opts = ["6", "8", "12"]
                exp = "Faces rectangulaires opposées 2 à 2"
            elif variante == "V3":
                enonce = "L'expression générale permettant de calculer le volume d'une pyramide est donné par :"
                correct = "(1/3) × Aire base × Hauteur"
                opts = ["(1/3) × Aire base × Hauteur", "Aire base × Hauteur", "Côté × Hauteur"]
                exp = "V = (1/3) × A_base × h"

        elif chapitre_cible == "Pourcentage et échelle":
            if variante == "V1":
                enonce = "Appliquer un taux de pourcentage de 50% sur une grandeur scalaire revient strictement à la :"
                correct = "Diviser par 2"
                opts = ["Diviser par 2", "Multiplier par 2", "Diviser par 4"]
                exp = "50% = 50/100 = 1/2"
            elif variante == "V2":
                base_p = 250 * facteur_diff
                enonce = f"Calculez la valeur numérique exacte correspondant à 10% de {base_p}."
                correct = f"{base_p // 10}"
                opts = [f"{base_p // 10}", f"{base_p // 100}", f"{base_p}"]
                exp = f"{base_p} × 0,1"
            else:
                enonce = "Sur une carte de géographie construite à l'échelle linéaire 1/100, une longueur mesurée de 1 cm correspond sur le terrain à :"
                correct = "100 cm (1 m)"
                opts = ["100 cm (1 m)", "10 cm", "1000 cm"]
                exp = "E = d / D ⇒ D = 100 cm"

        elif chapitre_cible == "Puissance":
            b = random.randint([2, 99])
            e = random.randint(2, 20) + (facteur_diff // 3)
            enonce = f"Calculez la value exacte de l'élévation à la puissance suivante : {b}^{e}"
            correct = str(b ** e)
            opts = [correct, str(b * e), str(b ** (e-1))]
            exp = f"x^n = x × x ... × x"

        elif chapitre_cible == "Distance entre deux points":
            x1 = random.randint(-99, -1) * facteur_diff
            x2 = random.randint(1, 99) * facteur_diff
            enonce = f"Sur une droite réelle graduée, déterminez la distance euclidienne reliant les points A({x1}) et B({x2})."
            correct = str(x2 - x1)
            opts = [correct, str(abs(x2 + x1)), str(x1 - x2)]
            exp = f"d = |x_B - x_A|"

        elif chapitre_cible == "Médiatrice d’un segment":
            p_ext = random.choice([("E","F"), ("P","Q"), ("X","Y")])
            enonce = f"Si un point M appartient à la médiatrice d'un segment [{p_ext[0]}{p_ext[1]}], quelle relation métrique est rigoureusement vérifiée ?"
            correct = f"M{p_ext[0]} = M{p_ext[1]}"
            opts = [f"M{p_ext[0]} = M{p_ext[1]}", f"M{p_ext[0]} + M{p_ext[1]} = 0", f"O, M, {p_ext[0]} sont alignés"]
            exp = f"M ∈ Δ ⇒ d(M, {p_ext[0]}) = d(M, {p_ext[1]})"

        elif chapitre_cible == "PGDC et PPCM":
            f = random.choice([2, 3, 5])
            a, b = f * random.randint(2, 4) * facteur_diff, f * random.randint(5, 7) * facteur_diff
            enonce = f"Déterminez le Plus Grand Commun Diviseur (PGCD) de {a} et {b}."
            correct = str(math.gcd(a, b))
            opts = [correct, str(f), str(a * b)]
            exp = f"Algorithme d'Euclide"

        elif chapitre_cible == "Nombres rationnels":
            n_rat = random.randint(2, 5) * facteur_diff
            d_rat = random.choice([7, 9, 11])
            enonce = f"Le nombre {n_rat}/{d_rat} appartient à l'ensemble Q des rationnels. Quelle est sa définition formelle ?"
            correct = "Le quotient d'un entier par un entier non nul"
            opts = ["Le quotient d'un entier par un entier non nul", "Un nombre décimal possédant un noble fini de chiffres après la virgule", "Une racine carrée parfaite"]
            exp = "Q = {a/b ; a ∈ Z, b ∈ Z*}"

        elif chapitre_cible == "Distance d’un point à une droite":
            pt_nom = random.choice(["M", "P", "K"])
            enonce = f"Le plus court chemin reliant un point externe {pt_nom} à une droite plane (D) correspond par définition à la distance entre {pt_nom} et :"
            correct = f"Son projeté orthogonal sur (D)"
            opts = [f"Son projeté orthogonal sur (D)", "Le milieu de la droite (D)", "L'origine du repère lié à (D)"]
            exp = "Minimisation géométrique via la perpendiculaire"

        elif chapitre_cible == "Secteurs angulaires":
            portion = random.choice([(2, 180), (3, 120), (4, 90)])
            enonce = f"Si un secteur angulaire occupe exactement un {portion[0]}ième de la surface d'un disque complet, quelle est la mesure de son angle au centre ?"
            correct = f"{portion[1]}°"
            opts = ["90°", "180°", "120°", "60°"]
            exp = f"θ = 360° / {portion[0]}"

        elif chapitre_cible == "Projection":
            prop_proj = random.choice(["alignement", "milieu"])
            if prop_proj == "alignement":
                enonce = "Lors d'une projection affine ou orthogonale sur une droite du plan, quelle propriété est invariante ?"
                correct = "L'alignement des points"
                opts = ["L'alignement des points", "La longueur des segments", "La mesure des angles"]
                exp = "Conservation des applications affines"
            else:
                enonce = "Si un point I est le milieu du segment [AB], son projeté orthogonal I' sur une droite quelconque sera obligatoirement :"
                correct = "Le milieu du segment projeté [A'B']"
                opts = ["Le milieu du segment projeté [A'B']", "Perpendiculaire à A' et B'", "Confondue avec l'origine"]
                exp = "Conservation du barycentre"

        elif chapitre_cible == "Outil vectoriel":
            v1 = random.choice(["A", "B", "C"])
            enonce = f"En utilisant la relation de Chasles dans l'espace vectoriel plan, simplifiez la somme vectorielle : vec({v1}B) + vec(BX)"
            correct = f"vec({v1}X)"
            opts = [f"vec({v1}X)", f"vec(BX)", f"vec({v1}B)"]
            exp = f"vec(IJ) + vec(JK) = vec(IK)"

        elif chapitre_cible == "Statistique":
            s1, s2, s3 = random.randint(10, 15) * facteur_diff, random.randint(8, 12) * facteur_diff, random.randint(14, 19) * facteur_diff
            enonce = f"Calculez la moyenne arithmétique simple x̄ de la série statistique de données suivantes : {s1}, {s2}, et {s3}."
            m_calc = round((s1 + s2 + s3) / 3, 2)
            correct = f"{m_calc}".replace('.', ',')
            opts = [correct, f"{(s1+s2)/2}".replace('.', ','), f"{s1+s2+s3}"]
            exp = f"x̄ = (∑ x_i) / n"

        elif chapitre_cible == "Sphère et boule":
            r_sph = random.choice([2, 3, 5, 10]) * facteur_diff
            enonce = f"Calculez l'aire superficielle externe d'une sphère de rayon R = {r_sph} cm (en fonction de π)."
            a_sph = 4 * (r_sph ** 2)
            correct = f"{a_sph}π cm²"
            opts = [correct, f"{2 * r_sph}π cm²", f"{a_sph // 4}π cm²"]
            exp = f"A = 4πR²"

        elif chapitre_cible in ["Renforcement de capacité", "Renforcement de capacity"]:
            a = random.randint(2, 5)
            b = random.randint(2, 9)
            res = a * (random.randint(2, 6) * facteur_diff) + b
            enonce = f"Résolvez l'équation du premier degré dans R suivante : {a}x + {b} = {res}"
            correct = str((res - b) // a)
            opts = [correct, str(res - b), str(res + a)]
            exp = f"{a}x + {b} = {res} ⇔ {a}x = {res} - {b}"

        elif chapitre_cible == "Racine carrée et Valeur absolue":
            val_abs = random.randint(-15, -3) * facteur_diff
            enonce = f"Simplifiez l'expression analytique suivante : √(({val_abs})²)"
            correct = str(abs(val_abs))
            opts = [correct, str(val_abs), str(val_abs ** 2)]
            exp = f"√(x²) = |x|"

        elif chapitre_cible == "Triangle rectangle":
            adj = random.randint(3, 8) * facteur_diff
            hyp = adj + random.randint(2, 5)
            enonce = f"Dans un triangle rectangle, si le côté adjacent à un angle α mesure {adj} cm et l'hypoténuse vaut {hyp} cm, déterminez Cos(α)."
            correct = f"{adj}/{hyp}"
            opts = [f"{adj}/{hyp}", f"{hyp}/{adj}", f"{adj * hyp}"]
            exp = f"Cos(α) = Adjacent / Hypoténuse"

        elif chapitre_cible == "Monôme et polynôme":
            val_id = random.choice([2, 3, 4, 6, 7, 9]) * facteur_diff
            enonce = f"Donnez la factorisation sous forme de polynômes irréductibles de l'expression : x² - {val_id**2}"
            correct = f"(x - {val_id})(x + {val_id})"
            opts = [f"(x - {val_id})(x + {val_id})", f"(x - {val_id})²", f"x(x - {val_id**2})"]
            exp = f"a² - b² = (a-b)(a+b)"

        elif chapitre_cible in ["Thales", "Tháles"]:
            div_t = random.choice([2, 3, 4])
            tot_t = div_t * random.randint(3, 5) * facteur_diff
            enonce = f"Dans une configuration de Thalès avec (AB) // (CD), si OA = {div_t} cm, OB = 5 cm et OC = {tot_t} cm, calculez la longueur du segment OD."
            correct = str((tot_t * 5) // div_t)
            opts = [correct, str(tot_t + 5), str(tot_t - div_t)]
            exp = f"OA/OC = OB/OD"

        elif chapitre_cible == "Equation d’une droite":
            a_dir = random.randint(-6, 6) * facteur_diff
            while a_dir == 0: a_dir = 2
            b_ord = random.randint(1, 9)
            enonce = f"Quel est le coefficient directeur (la pente affine) de la droite (D) d'équation réduite : y = {a_dir}x + {b_ord} ?"
            correct = str(a_dir)
            opts = [correct, str(b_ord), str(-a_dir)]
            exp = f"y = mx + p ⇒ m = {a_dir}"

        elif chapitre_cible == "Application affine":
            coef_a = random.randint(2, 7) * facteur_diff
            x_val = random.randint(2, 5)
            enonce = f"Soit la fonction linéaire f définie sur R par f(x) = {coef_a}x. Calculez l'image de la valeur {x_val}."
            correct = str(coef_a * x_val)
            opts = [correct, str(coef_a + x_val), str(coef_a)]
            exp = f"f({x_val}) = {coef_a} × {x_val}"

        elif chapitre_cible == "Système dans IR²":
            choix_sys = random.choice(["sec", "para"])
            if choix_sys == "sec":
                enonce = "Si deux droites représentant un système d'équations linéaires dans IR² possèdent des coefficients directeurs distincts, le système admet :"
                correct = "Une solution unique"
                opts = ["Une solution unique", "Aucune solution", "Une infinité de solutions"]
                exp = "m1 ≠ m2 ⇒ Unique point d'intersection D1 ∩ D2"
            else:
                enonce = "Si deux droites représentant un système linéaire sont strictement parallèles, l'ensemble des solutions est :"
                correct = "Vide (aucune solution)"
                opts = ["Vide (aucune solution)", "Un point unique", "Une infinité de points"]
                exp = "D1 // D2 et D1 ∩ D2 = ∅"

        elif chapitre_cible == "Angles et Rotation":
            enonce = "Une rotation plane d'angle 180° modifie-t-elle la distance euclidienne entre deux points transformés ?"
            correct = "Non, car c'est une isométrie"
            opts = ["Non, car c'est une isométrie", "Oui, elle les multiplie", "Uniquement si le centre est l'origine"]
            exp = "Conservation de la distance"

        elif chapitre_cible == "Sujet types":
            k = random.choice([2, 3, 4]) * facteur_diff
            enonce = f"Dans un triangle ABC rectangle en A, si AB = {k*3} cm et AC = {k*4} cm, déterminez la longueur de la diagonale BC."
            correct = f"{k*5} cm"
            opts = [f"{k*5} cm", f"{k*7} cm", f"{(k*5)**2} cm"]
            exp = f"BC² = AB² + AC²"
            
        # --- AJOUTS DE SÉCURITÉ : LYCÉE (2nde à Terminale) 
        elif chapitre_cible == "Vecteurs et repérage":
            x, y = random.randint(1, 40) * facteur_diff, random.randint(1, 5)
            enonce = f"Soit un vecteur u({x}, {y}). Déterminez les coordonnées du vecteur 2u."
            correct = f"({x*2}, {y*2})"
            opts = [correct, f"({x}, {y})", f"({x+2}, {y+2})"]
            exp = f"k · vec(u)(x, y) = vec(v)(k·x, k·y)"

        elif chapitre_cible == "Valeur absolue et intervalles":
            val = random.randint(2, 80) * facteur_diff
            enonce = f"Résolvez l'équation d'intervalle simple : |x| = {val}"
            correct = f"x = {val} ou x = -{val}"
            opts = [correct, f"x = {val}", "Aucune solution"]
            exp = f"|x| = a (avec a ≥ 0) ⇒ x = a ou x = -a"

        elif chapitre_cible == "Dérivation fonctionnelle":
            coef = random.randint(2, 6) * facteur_diff
            enonce = f"Quelle est la dérivée de la fonction f(x) = {coef}x² ?"
            correct = f"{coef*2}x"
            opts = [correct, f"{coef}x", f"2x"]
            exp = f"(x²)' = 2x ⇒ ({coef}x²)' = {coef} × 2x = {coef*2}x"

        elif chapitre_cible == "Polynômes du second degré":
            enonce = "Si le discriminant Δ d'un polynôme du second degré ax² + bx + c est strictly négatif (Δ < 0), combien de racines réelles possède-t-il ?"
            correct = "0"
            opts = ["0", "1 racine double", "2 racines distinctes"]
            exp = "Δ < 0 implies aucune intersection réelle avec l'axe des abscisses."

        elif chapitre_cible == "Nombres complexes":
            enonce = "Quelle est la valeur mathématique rigoureuse de la puissance imaginaire i² ?"
            correct = "-1"
            opts = ["-1", "1", "0"]
            exp = "Par définition de l'ensemble C, le nombre imaginaire pur i vérifie i² = -1."

        elif chapitre_cible == "Calcul intégral":
            enonce = "La valeur numérique calculée d'une intégrale définie d'une fonction continue et positive sur un intervalle [a, b] représente :"
            correct = "L'aire sous la courbe"
            opts = ["L'aire sous la courbe", "La pente de la tangente", "La valeur limite à l'infini"]
            exp = "L'intégrale de a à b de f(x)dx est la mesure de la surface délimitée par la courbe."
            
        # AJOUTS DE SÉCURITÉ : UNIVERSITÉ (L1 MPC) 
        elif chapitre_cible == "Cinématique absolue":
            enonce = "En cinématique du point, la loi de composition des vitesses exprime la vitesse absolue comme la somme de :"
            correct = "Vitesse relative + Vitesse d'entraînement"
            opts = ["Vitesse relative + Vitesse d'entraînement", "Vitesse de Coriolis + Vitesse relative", "Vitesse angulaire + Vitesse de Frenet"]
            exp = "vec(Va) = vec(Vr) + vec(Ve)"

        elif chapitre_cible == "Accélération de Coriolis":
            enonce = "Donnez l'expression vectorielle exacte de l'accélération de Coriolis (Ac) :"
            correct = "2 · vec(Ω) × vec(Vr)"
            opts = ["2 · vec(Ω) × vec(Vr)", "vec(Ω) × vec(OM)", "v² / R"]
            exp = "Ac = 2 · vec(Ω) × vec(Vr) (produit vectoriel entre la rotation du repère et la vitesse relative)"

        elif chapitre_cible == "Frenet":
            enonce = "Dans la base mobile de Frenet, l'accélération normale (An) d'un point en mouvement curviligne sur une trajectoire de rayon R vaut :"
            correct = "v² / R"
            opts = ["v² / R", "dv / dt", "2·v·R"]
            exp = "vec(a) = (dv/dt)·vec(τ) + (v²/R)·vec(n)"

        elif chapitre_cible == "Régime RLC":
            enonce = "Quelle est la condition sur la résistance globale R pour obtenir un régime pseudo-périodique (oscillations amorties) ?"
            correct = "R < 2 · √(L/C)"
            opts = ["R < 2 · √(L/C)", "R > 2 · √(L/C)", "R = 0"]
            exp = "Le régime pseudo-périodique apparaît lorsque le discriminant de l'équation caractéristique est négatif."

        elif chapitre_cible == "Optique de Descartes":
            enonce = "Selon la seconde loi de Snell-Descartes for la réfraction, la relation liant les angles d'incidence (i1) et de réfraction (i2) is :"
            correct = "n1 · sin(i1) = n2 · sin(i2)"
            opts = ["n1 · sin(i1) = n2 · sin(i2)", "n1 · cos(i1) = n2 · cos(i2)", "n1 · i1 = n2 · i2"]
            exp = "Loi fondamentale de la réfraction : n1 · sin(i1) = n2 · sin(i2)."

        elif chapitre_cible == "Théorème du rang":
            enonce = "Soit f une application linéaire d'un espace vectoriel E de dimension finie vers F. Le théorème du rang affirme que :"
            correct = "dim(Ker(f)) + dim(Im(f)) = dim(E)"
            opts = ["dim(Ker(f)) + dim(Im(f)) = dim(E)", "dim(Ker(f)) = dim(Im(f))", "dim(Im(f)) = dim(F)"]
            exp = "Théorème central de l'algèbre linéaire : la somme de la dimension du noyau et du rang est égale à la dimension de l'espace de départ."

        elif chapitre_cible == "Développements limités":
            enonce = "Quel est le développement limité à l'ordre 2 en 0 de la fonction cos(x) ?"
            correct = "1 - x²/2 + o(x²)"
            opts = ["1 - x²/2 + o(x²)", "x - x³/6 + o(x³)", "1 + x + x² + o(x²)"]
            exp = "Formule de Taylor-Young en 0 : cos(x) = 1 - x²/2! + o(x²)."

        # SÉCURITÉ ABSOLUE : SÉLECTION PAR DÉFAUT 
        else:
            val_a = random.randint(1, 99) * facteur_diff
            val_b = random.randint(1, 99)
            enonce = f" [Défi Session] Calculez rapidement la somme : {val_a} + {val_b}"
            correct = str(val_a + val_b)
            opts = [correct, str(val_a * val_b), str(val_a - val_b)]
            exp = f"Opération de secours pour le chapitre : {chapitre_cible}\nCalcul : {val_a} + {val_b} = {val_a + val_b}"

        return enonce, correct, opts, exp

if __name__ == '__main__':
    FixedDynamicQuizApp().run()
