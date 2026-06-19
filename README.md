import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class FixedDynamicQuizApp(App):
    def build(self):
        self.score = 0
        self.combo = 0  
        self.bonne_reponse = ""
        self.explication_erreur = ""
        self.niveau_actuel = ""
        self.classe_actuelle = ""
        self.historique_questions = []
        self.question_generée_ia = ""
        
        # Variables pour le chronomètre
        self.temps_restant = 60
        self.evenement_chrono = None
        
        # Layout Principal
        self.main_layout = BoxLayout(orientation='vertical', padding=12, spacing=10)
        
        # Zone d'information supérieure (Score & Chrono)
        self.info_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        self.info_label = Label(text="Sélectionnez votre niveau", font_size='15sp', halign='left')
        self.chrono_label = Label(text="", font_size='16sp', bold=True, color=(1, 0.3, 0.3, 1), halign='right')
        self.info_layout.add_widget(self.info_label)
        self.info_layout.add_widget(self.chrono_label)
        self.main_layout.add_widget(self.info_layout)
        
        # ZONE QUESTIONS : Défilement vertical
        self.scroll_texte = ScrollView(size_hint=(1, 0.46), do_scroll_x=False, do_scroll_y=True)
        self.question_label = Label(
            text="", 
            font_size='16sp', 
            halign='center', 
            valign='middle',
            size_hint_y=None
        )
        self.question_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - 20, None)))
        self.question_label.bind(texture_size=lambda instance, size: setattr(instance, 'height', max(size[1] + 40, 300)))
        
        self.scroll_texte.add_widget(self.question_label)
        self.main_layout.add_widget(self.scroll_texte)
        
        # Zone principale pour les boutons
        self.interaction_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.46), spacing=6)
        self.main_layout.add_widget(self.interaction_layout)
        
        self.afficher_menu_niveaux()
        return self.main_layout

    def afficher_menu_niveaux(self):
        self.arreter_chrono()
        self.chrono_label.text = ""
        self.interaction_layout.clear_widgets()
        self.info_label.text = "Menu Principal"
        self.question_label.text = "Bienvenue sur Math Quiz\nVersion Haute Technologie Rapide ⚡\n\nSélectionnez un niveau :"
        
        niveaux = {
            "Collège": ["6ème", "5ème", "4ème", "3ème"], 
            "Lycée": ["2nde", "1ère", "Terminale"],
            "Université": ["L1 MPC"]
        }
        
        for nv in niveaux.keys():
            btn = Button(text=nv, font_size='18sp', background_color=(0.2, 0.5, 0.8, 1))
            btn.bind(on_press=lambda inst, n=nv, list_cl=niveaux[nv]: self.afficher_menu_classes(n, list_cl))
            self.interaction_layout.add_widget(btn)

    def afficher_menu_classes(self, niveau, list_cl):
        self.arreter_chrono()
        self.chrono_label.text = ""
        self.niveau_actuel = niveau
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"Niveau : {niveau}"
        self.question_label.text = "Choisissez votre classe :"
        
        btn_retour = Button(text="← Retour au Menu Principal", size_hint_y=0.18, background_color=(0.7, 0.2, 0.2, 1))
        btn_retour.bind(on_press=lambda x: self.afficher_menu_niveaux())
        self.interaction_layout.add_widget(btn_retour)
        
        for cl in list_cl:
            btn = Button(text=cl, font_size='16sp', background_color=(0.2, 0.6, 0.4, 1))
            btn.bind(on_press=self.clic_classe)
            self.interaction_layout.add_widget(btn)

    def clic_classe(self, instance):
        self.classe_actuelle = instance.text
        self.score = 0
        self.combo = 0
        self.historique_questions = []
        self.generer_question_dynamique()

    def lancer_chrono(self):
        self.arreter_chrono()
        self.temps_restant = 60
        self.chrono_label.text = f"⏱️ {self.temps_restant}s"
        self.evenement_chrono = Clock.schedule_interval(self.mettre_a_jour_chrono, 1.0)

    def arreter_chrono(self):
        if self.evenement_chrono:
            Clock.unschedule(self.evenement_chrono)
            self.evenement_chrono = None

    def mettre_a_jour_chrono(self, dt):
        self.temps_restant -= 1
        self.chrono_label.text = f"⏱️ {self.temps_restant}s"
        
        if self.temps_restant <= 0:
            self.arreter_chrono()
            self.gerer_temps_ecoule()

    def gerer_temps_ecoule(self):
        self.interaction_layout.clear_widgets()
        self.combo = max(0, self.combo - 2)
        texte = f"⏰ TEMPS ÉCOULÉ ! (Limite de 1 min dépassée)\n\nLa bonne réponse était : {self.bonne_reponse}.\n\n"
        if self.explication_erreur:
            texte += f"Explication :\n{self.explication_erreur}"
            
        self.question_label.text = texte
        self.creer_interface_suivante()

    def generer_question_dynamique(self):
        self.interaction_layout.clear_widgets()
        self.info_label.text = f"{self.classe_actuelle} | Score : {self.score} | Combo : x{self.combo}"
        
        ordre_classes = ["6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Terminale", "L1 MPC"]
        try:
            idx_actuel = ordre_classes.index(self.classe_actuelle)
        except ValueError:
            idx_actuel = 0
            
        pool_classes = ordre_classes[:idx_actuel + 1]
        
        if len(pool_classes) == 1 or random.random() < 0.70:
            classe_cible = self.classe_actuelle
        else:
            classes_inferieures = pool_classes[:-1]
            poids = [2**i for i in range(len(classes_inferieures))]
            classe_cible = random.choices(classes_inferieures, weights=poids, k=1)[0]
        
        # Nombre maximum de types (Chaque classe possède maintenant son lot de variations algorithmiques)
        max_types = 9 if classe_cible == "6ème" else (12 if classe_cible in ["5ème", "4ème", "3ème"] else 8)
        if classe_cible == "L1 MPC": max_types = 10
        
        id_type = random.randint(1, max_types)
        enonce, correct, opts, exp = "", "", [], ""

        # ================= PROGRAMME 6ème =================
        if classe_cible == "6ème":
            if id_type == 1:
                n = random.randint(-25, 25)
                if n == 0: n = 7
                enonce = f"[Entiers relatifs] Le nombre {n} est-il un nombre positif ou négatif ?"
                correct = "Positif" if n > 0 else "Négatif"
                opts = ["Positif", "Négatif"]
                exp = f"Un nombre précédé du signe (-) est inférieur à 0 donc négatif."
            elif id_type in [2, 3]:
                a, b = random.randint(-30, 30), random.randint(-30, 30)
                while a == b: b = random.randint(-30, 30)
                quel = "grand" if id_type == 2 else "petit"
                enonce = f"[Comparaison] Quel nombre est le plus {quel} entre {a} et {b} ?"
                correct = str(max(a, b)) if id_type == 2 else str(min(a, b))
                opts = [str(a), str(b)]
                exp = "Visualisez les nombres sur un axe gradué de gauche à droite."
            elif id_type == 4:
                n = random.randint(11, 199)
                enonce = f"Le nombre {n} est-il pair ou impair ?"
                correct = "Pair" if n % 2 == 0 else "Impair"
                opts = ["Pair", "Impair"]
                exp = f"Il se termine par {n%10}, donc il est {correct.lower()}."
            elif id_type == 5:
                a, b, c = random.randint(5, 20), random.randint(2, 10), random.randint(1, 9)
                enonce = f"[Priorités] Calculez le résultat exact : {a} + ({b} - {c})"
                correct = str(a + (b - c))
                opts = [str(a + (b - c)), str((a + b) - c), str(a + b + c)]
                exp = "Les parenthèses s'effectuent en toute priorité."
            elif id_type == 6:
                a, b = random.randint(10, 50), random.randint(10, 50)
                enonce = f"[Calcul mental] Résolvez de tête l'opération : {a} + {b}"
                correct = str(a + b)
                opts = [str(a + b), str(a + b - 2), str(a + b + 5)]
                exp = f"Addition simple des unités et des dizaines."
            else:
                n = random.randint(2, 150)
                enonce = f"[Ensembles] Le nombre {n} appartient-il à l'ensemble N (Entiers naturels) ?"
                correct = "Oui"
                opts = ["Oui", "Non"]
                exp = "L'ensemble N regroupe tous les nombres entiers qui sont positifs ou nuls."

        # ================= PROGRAMME 5ème (ABONDANCE DE PUISSANCES DYNAMIQUES) =================
        elif classe_cible == "5ème":
            if id_type in [1, 2, 3, 4]: # Les puissances dynamiques règnent en maître
                base = random.choice([2, 3, 4, 5, 10])
                expo = random.randint(2, 4) if base != 10 else random.randint(2, 6)
                enonce = f"[Puissances] Calculez la valeur numérique exacte de la puissance : {base}^{expo}"
                res = base ** expo
                correct = str(res)
                opts = [str(res), str(base * expo), str(res + base), str(res - base)]
                exp = f"{base}^{expo} signifie que l'on multiplie le nombre {base} par lui-même {expo} fois."
            elif id_type in [5, 6]:
                base = random.randint(2, 9)
                enonce = f"[Puissances Spéciales] Quelle est la valeur de n'importe quel nombre non nul élevé à l'exposant 0 ? Exemple : {base}^0"
                correct = "1"
                opts = ["1", "0", str(base), "-1"]
                exp = "Par convention algébrique incontournable, tout nombre non nul à la puissance 0 vaut 1."
            elif id_type == 7:
                a, b, c = random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)
                enonce = f"[Priorités opératoires] Calculez l'expression : {a} + {b} × {c}"
                correct = str(a + (b * c))
                opts = [str(a + (b * c)), str((a + b) * c), str(a * b * c)]
                exp = "La multiplication passe impérativement avant l'addition."
            elif id_type == 8:
                coeff = random.randint(2, 7)
                cible = coeff * random.randint(2, 6)
                enonce = f"[Équations] Trouvez la valeur de x dans l'équation linéaire : {coeff}x = {cible}"
                correct = str(cible // coeff)
                opts = [str(cible // coeff), str(cible - coeff), str(cible + coeff)]
                exp = f"On isole x en divisant le membre de droite par le coefficient : x = {cible} / {coeff}."
            else:
                a, b = random.randint(-20, -2), random.randint(-20, -2)
                enonce = f"[Relatifs] Calculez la somme de deux nombres négatifs : ({a}) + ({b})"
                correct = str(a + b)
                opts = [str(a + b), str(abs(a + b)), str(a - b)]
                exp = "On fait la somme de leurs valeurs absolues et on garde le signe commun (-)."

        # ================= PROGRAMME 4ème (ABONDANCE DE FRACTIONS DYNAMIQUES) =================
        elif classe_cible == "4ème":
            if id_type in [1, 2, 3, 4, 5]: # Multiplication, addition et réduction de fractions aléatoires
                num1, den1 = random.randint(1, 5), random.randint(2, 4)
                num2, den2 = random.randint(1, 5), random.randint(2, 5)
                while den1 == den2: den2 = random.randint(2, 5)
                
                type_frac = random.choice(["mult", "add"])
                if type_frac == "mult":
                    enonce = f"[Fractions] Multipliez ces deux fractions : ({num1}/{den1}) × ({num2}/{den2}). Quelle est la valeur brute ?"
                    final_num = num1 * num2
                    final_den = den1 * den2
                    correct = f"{final_num}/{final_den}"
                    opts = [correct, f"{num1+num2}/{den1+den2}", f"{num1*den2}/{num2*den1}"]
                    exp = "Pour multiplier deux fractions, on multiplie les numérateurs entre eux et les dénominateurs entre eux."
                else:
                    # Addition simple même dénominateur pour rester gérable sur mobile sans papier
                    den_commun = random.randint(2, 7)
                    num_a, num_b = random.randint(1, 6), random.randint(1, 6)
                    enonce = f"[Fractions] Additionnez ces fractions à dénominateur identique : ({num_a}/{den_commun}) + ({num_b}/{den_commun})"
                    correct = f"{num_a + num_b}/{den_commun}"
                    opts = [correct, f"{num_a + num_b}/{den_commun * 2}", f"{num_a * num_b}/{den_commun}"]
                    exp = "On additionne les numérateurs et on conserve précieusement le dénominateur commun."
            elif id_type in [6, 7]:
                val = random.randint(3, 12)
                enonce = f"[Racines] Simplifiez radicalement la racine carrée parfaite suivante : √({val * val})"
                correct = str(val)
                opts = [str(val), str(val * 2), str(val + 1)]
                exp = f"La racine carrée est l'opération inverse du carré : {val} × {val} = {val*val}."
            elif id_type == 8:
                enonce = "Quelle est l'identité remarquable exacte pour développer (a - b)(a + b) ?"
                correct = "a² - b²"
                opts = ["a² - b²", "a² + b²", "a² - 2ab + b²"]
                exp = "C'est la troisième identité remarquable : différence de deux carrés."
            else:
                a = random.randint(2, 5)
                enonce = f"[Polynômes] Développez l'expression suivante : (x - {a})(x + {a})"
                correct = f"x² - {a*a}"
                opts = [f"x² - {a*a}", f"x² + {a*a}", f"x² - {2*a}x"]
                exp = f"Application directe de (a-b)(a+b) = a² - b². Ici b = {a}."

        # ================= PROGRAMME 3ème =================
        elif classe_cible == "3ème":
            if id_type == 1:
                enonce = "[Système] Résolvez le système linéaire :\n2x + y = 7\nx - y = 2"
                correct = "(3, 1)"
                opts = ["(3, 1)", "(2, 3)", "(4, -1)"]
                exp = "Par addition des deux lignes : 3x = 9 => x = 3, d'où y = 1."
            elif id_type == 2:
                a = random.choice([2, 3, 4])
                enonce = f"[Fonction Affine] Soit f(x) = -{a}x + 7. Quel est son coefficient directeur ?"
                correct = f"-{a}"
                opts = [f"-{a}", "7", f"{a}"]
                exp = "Dans f(x) = ax + b, le coefficient directeur est le nombre multiplicateur de x."
            elif id_type == 3:
                val = random.choice([6, 8, 10])
                enonce = f"[Pythagore] Si un triangle rectangle possède des côtés de longueurs 6 et 8. Combien vaut son hypoténuse ?"
                correct = "10"
                opts = ["10", "14", "12"]
                exp = "H² = 6² + 8² = 36 + 64 = 100 => H = √100 = 10."
            else:
                a = random.randint(2, 5)
                enonce = f"[Algèbre] Trouvez les solutions de l'équation produit : (x - {a})(x + 3) = 0"
                correct = f"x = {a} ou x = -3"
                opts = [f"x = {a} ou x = -3", f"x = -{a} ou x = 3", "x = 0"]
                exp = "Un produit de facteurs est nul si au moins un des facteurs est nul."

        # ================= PROGRAMME 2nde =================
        elif classe_cible == "2nde":
            if id_type == 1:
                k = random.randint(2, 6)
                enonce = f"[Vecteurs] Si U(2; 3) et V(4; m) sont colinéaires, alors m vaut :"
                correct = str(6)
                opts = ["6", "5", "8"]
                exp = "Condition de colinéarité : 2*m - 3*4 = 0 => 2m = 12 => m = 6."
            else:
                enonce = "[Valeur absolue] Simplifiez l'expression absolue suivante : |3 - π|"
                correct = "π - 3"
                opts = ["π - 3", "3 - π", "0"]
                exp = "Puisque π > 3, la quantité 3 - π est négative. Son absolue est donc son opposé."

        # ================= PROGRAMME 1ère =================
        elif classe_cible == "1ère":
            if id_type == 1:
                enonce = "Quelle est la fonction dérivée de la fonction f(x) = ln(x) sur ]0; +∞[ ?"
                correct = "1/x"
                opts = ["1/x", "e^x", "1/x²"]
                exp = "C'est une formule de dérivation fondamentale du cours."
            else:
                enonce = "[Second degré] Si le discriminant Delta d'une équation est strictement négatif (< 0), combien y a-t-il de racines réelles ?"
                correct = "0"
                opts = ["0", "1", "2"]
                exp = "Un discriminant négatif indique l'absence totale d'intersections réelles avec l'axe des abscisses."

        # ================= PROGRAMME TERMINALE =================
        elif classe_cible == "Terminale":
            if id_type == 1:
                enonce = "[Complexes] Quelle est la forme exponentielle de z = 1 - i ?"
                correct = "√2 e^(-iπ/4)"
                opts = ["√2 e^(-iπ/4)", "√2 e^(iπ/4)", "2 e^(-iπ/4)"]
                exp = "Le module vaut √2 et l'argument principal vaut -π/4."
            else:
                enonce = "[Intégrales] Quelle est la valeur de l'intégrale de 0 à 1 de e^x dx ?"
                correct = "e - 1"
                opts = ["e - 1", "e", "1"]
                exp = "La primitive de e^x est e^x. On calcule donc e¹ - e⁰ = e - 1."

        # ================= PROGRAMME UNIVERSITÉ (L1 MPC) =================
        else:
            if id_type == 1:
                enonce = "[Algèbre linéaire] Si le déterminant d'une matrice carrée M est égal à 0, alors :"
                correct = "M n'est pas inversible"
                opts = ["M n'est pas inversible", "M est inversible", "M est l'identité"]
                exp = "det(M) = 0 signifie que la matrice est singulière (colonnes liées)."
            elif id_type == 2:
                enonce = "[Optique] Quelle est la formule exacte de la loi de Snell-Descartes pour la réfraction ?"
                correct = "n1 × sin(i1) = n2 × sin(i2)"
                opts = ["n1 × sin(i1) = n2 × sin(i2)", "n1 × cos(i1) = n2 × cos(i2)", "n1 × i1 = n2 × i2"]
                exp = "C'est le produit de l'indice de réfraction par le sinus de l'angle d'incidence."
            else:
                enonce = "[Analyse] Quel est le développement limité à l'ordre 2 en 0 de ln(1 + x) ?"
                correct = "x - (x²/2) + o(x²)"
                opts = ["x - (x²/2) + o(x²)", "x + (x²/2) + o(x²)", "x - x²"]
                exp = "Formule de Taylor-Maclaurin classique à l'ordre 2."

        self.question_label.text = enonce
        self.bonne_reponse = str(correct)
        self.explication_erreur = exp
        self.question_generée_ia = enonce
        
        # Filtrage strict et mélange des choix
        liste_options = list(set([str(o) for o in opts]))
        if str(correct) not in liste_options:
            liste_options.append(str(correct))
        random.shuffle(liste_options)
        
        # Bouton Quitter
        btn_quitter = Button(text="← Quitter", size_hint_y=0.12, background_color=(0.8, 0.3, 0.3, 1))
        btn_quitter.bind(on_press=lambda x: self.afficher_menu_classes(self.niveau_actuel, ["6ème", "5ème", "4ème", "3ème"] if self.niveau_actuel == "Collège" else (["2nde", "1ère", "Terminale"] if self.niveau_actuel == "Lycée" else ["L1 MPC"])))
        self.interaction_layout.add_widget(btn_quitter)

        # Affichage des choix sous forme de boutons
        for opt in liste_options:
            btn_opt = Button(text=opt, font_size='14sp', size_hint_y=0.15)
            btn_opt.bind(on_press=self.verifier_choix)
            self.interaction_layout.add_widget(btn_opt)

        # Lancement immédiat du chronomètre de 1 minute
        self.lancer_chrono()

    def verifier_choix(self, instance):
        self.arreter_chrono() # On stoppe le chrono dès qu'il clique
        choix = instance.text
        self.interaction_layout.clear_widgets()
        
        if choix == self.bonne_reponse:
            self.score += 1
            self.combo += 1
            texte = f"🔥 Correct ! Tu assures !\n\nScore : {self.score} | Combo : x{self.combo}"
        else:
            self.combo = max(0, self.combo - 2)
            texte = f"📉 Faux...\nLa bonne réponse était : {self.bonne_reponse}.\n\n"
            if self.explication_erreur:
                texte += f"Explication :\n{self.explication_erreur}"
        
        self.question_label.text = texte
        self.creer_interface_suivante()

    def creer_interface_suivante(self):
        lbl_feedback = Label(text="Avis développeur :", size_hint_y=0.10, font_size='12sp')
        self.interaction_layout.add_widget(lbl_feedback)
        
        self.feedback_layout = BoxLayout(orientation='horizontal', size_hint_y=0.18, spacing=5)
        for diff in ["Très Facile", "Facile", "Moyen", "Compliqué", "Très Compliqué"]:
            btn_diff = Button(text=diff, font_size='10sp', background_color=(0.4, 0.4, 0.4, 1))
            btn_diff.bind(on_press=lambda inst, df=diff: self.enregistrer_retours_developpeur(df))
            self.feedback_layout.add_widget(btn_diff)
        self.interaction_layout.add_widget(self.feedback_layout)
        
        btn_suivant = Button(text="Défi Suivant →", font_size='18sp', size_hint_y=0.34, background_color=(0.1, 0.6, 0.9, 1))
        btn_suivant.bind(on_press=lambda x: self.generer_question_dynamique())
        self.interaction_layout.add_widget(btn_suivant)

    def enregistrer_retours_developpeur(self, evaluation):
        import os
        try:
            with open("notes_fazad.txt", "a", encoding="utf-8") as f:
                f.write(f"Question: {self.question_generée_ia} -> Avis: {evaluation}\n")
        except Exception:
            pass
        self.feedback_layout.disabled = True

if __name__ == '__main__':
    FixedDynamicQuizApp().run()
