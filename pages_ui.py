# -*- coding: utf-8 -*-
"""
pages_ui.py — tous les menus et sous-menus sont des PAGES plein écran (surcouche de Locky).

Principe : chaque ancien menu Kivy commence par `if self.page_xxx(): return`.
 * surcouche prête  -> la page est affichée, les anciens boutons Kivy ne sont pas construits
 * surcouche absente (PC, chargement) -> l'ancien menu Kivy sert de secours, rien ne change

Un appui sur une carte exécute son action. Si l'action ouvre une autre page, la page est simplement remplacée ;
si elle lance une session (questions…), la page se referme pour laisser place à l'écran de jeu.
"""
import json
from types import SimpleNamespace

CYAN, MAG, VERT, AMBRE, VIOLET, ROUGE, BLEU = "#00f0ff", "#ff2bd6", "#39ff88", "#ffb000", "#9d6bff", "#ff3b5c", "#3d8bff"

ACTIVITES = [
    ("Calcul Mental Éclair", "⚡", "Calcule vite, sans calculatrice : chaque seconde compte."),
    ("Arithmétique de Base", "➕", "Les opérations fondamentales, sans faute."),
    ("Fractions & Proportions", "🍰", "Fractions, pourcentages, proportionnalité."),
    ("Équations du 1er Degré", "⚖️", "Isoler l'inconnue et résoudre."),
    ("Puissances & Racines", "√", "Exposants, racines carrées et règles de calcul."),
    ("Identités Remarquables", "✳️", "Développer, factoriser, simplifier."),
    ("Systèmes Linéaires", "🔗", "Plusieurs équations, plusieurs inconnues."),
    ("Dérivation & Limites", "📈", "Pentes, variations et comportements limites."),
    ("Nombres Complexes", "🌀", "Le plan complexe et ses calculs."),
    ("Calcul Intégral", "∫", "Primitives, aires et intégrales."),
    ("Mécanique du Point", "🎯", "Forces, mouvements et énergie."),
    ("Thermodynamique Appliquée", "🔥", "Chaleur, travail et rendement."),
    ("Optique Géométrique", "🔭", "Lentilles, miroirs et rayons."),
    ("Électrostatique Avancée", "⚡", "Charges, champs et potentiels."),
    ("Théorèmes Vectoriels Complexes", "🧭", "Circulation, flux, divergence."),
    ("Physique Quantique 101", "⚛️", "Les bases du monde quantique."),
]
GROUPES_ACTIVITES = [("Fondations", 0, 4), ("Algèbre & analyse", 4, 10), ("Physique avancée", 10, 16)]
CYCLES = [
    ("Cycle Collège (6ème à 3ème)", "🏫", "Collège", "De la 6ème à la 3ème", CYAN),
    ("Cycle Lycée (2nde à Terminale)", "📚", "Lycée", "De la 2nde à la Terminale", MAG),
    (" Université (Comores MPC)", "🎓", "Université", "Comores · filière MPC", AMBRE),
]
CLASSES_IA = ["6ème", "5ème", "4ème", "3ème", "2nde", "1ére", "Terminale", "1ére année", "2éme année"]


class FonctionsPages:

    def pages_defauts(self):
        self._page_cb = []
        self._page_retour = None
        self._page_ouverte = False
        self._page_courante_active = False        # une page est « en cours » (même masquée par Paramètres, Évolution…)

    # ------------------------------------------------------------------ moteur
    def pages_pretes(self):
        ov = getattr(self, "locky_overlay", None)
        return ov is not None and ov.pret

    def page_menu(self, titre, sous="", sections=None, retour=None, hero=None, cols=1, accueil=False, blocs=None):
        """sections : liste de (titre_de_section, [items]) ; item : dict(t, d, i, col, etat, tag, msg, bar, rang, cb)."""
        if not self.pages_pretes():
            return False
        flat, secs = [], []
        for titre_sec, items in (sections or []):
            sortie = []
            for it in items:
                d = {k: v for k, v in it.items() if k != "cb"}
                d["n"] = len(flat)
                flat.append(it.get("cb"))
                sortie.append(d)
            secs.append({"t": titre_sec, "items": sortie})
        self._page_cb = flat
        self._page_retour = retour
        self._page_ouverte = True
        self._page_courante_active = True
        btns = [{"k": "param", "i": "⚙"}, {"k": "locky", "i": "🦊"}] if accueil else [{"k": "accueil", "i": "🏠"}]
        p = {"titre": titre, "sous": sous, "retour": bool(retour), "cols": cols, "hero": hero, "secs": secs, "btns": btns, "blocs": blocs}
        ov = self.locky_overlay
        ov.regler_mode("pg")
        ov.js("PG.ouvrir(%s)" % json.dumps(p, ensure_ascii=False))
        return True

    def _page_executer(self, f):
        """Lance une action puis referme la page SEULEMENT si l'action n'en a pas ouvert une autre."""
        ov = self.locky_overlay
        self._page_ouverte = False
        if self.btn_parametres in self.info_layout.children:          # comme les anciens menus : pas d'icône ⚙ pendant une session
            self.info_layout.remove_widget(self.btn_parametres)
        if f:
            f()
        if not self._page_ouverte and ov.mode == "pg":
            self._page_courante_active = False
            ov.regler_mode("avatar")

    def pages_evenement(self, e):
        k = e.get("k")
        if k == "item":
            i = int(e.get("i", -1))
            if 0 <= i < len(self._page_cb):
                self._page_executer(self._page_cb[i])
        elif k == "retour":
            self._page_executer(self._page_retour)
        elif k == "btn":
            v = e.get("v")
            if v == "accueil":
                self._page_executer(lambda: self.afficher_menu_principal_modes())
            elif v == "param":
                self._page_executer(lambda: self.ouvrir_menu_parametres())
            elif v == "locky":
                self._page_executer(lambda: self.locky_ouvrir_menu())

    def pages_reprendre(self):
        """Fermeture de Paramètres / Évolution / profil de Locky : on revient à la page d'où l'on venait."""
        ov = self.locky_overlay
        if self._page_courante_active and ov.mode in ("param", "evo", "menu", "calc"):
            ov.regler_mode("pg")
            return True
        return False

    # ------------------------------------------------------------------ accueil
    def _hero_joueur(self):
        _, rp_in, seuil, idx = self.determiner_rang_et_details()
        liste = self._rangs_liste()
        r = liste[idx]
        suiv = liste[idx + 1]["n"] if idx + 1 < len(liste) else None
        stat = f"LV {self.niveau_profil} · {int(self.points_de_rang)} RP · {self.xp} XP"
        stat += f"\n{seuil - rp_in} RP avant {suiv}" if suiv else "\nRang maximal"
        return {"nom": self.nom_utilisateur, "rang": r["n"], "col": r["col"], "b": r["b"], "v": r["v"] and ["", "I", "II", "III", "IV", "V"][r["v"]] or "★",
                "pct": round(100 * rp_in / max(1, seuil)), "stat": stat.replace("\n", " · ")}

    def _nb_activites_debloquees(self):
        idx = self.determiner_rang_et_details()[3]
        return sum(1 for nom, _, _ in ACTIVITES if idx >= self.obtenir_index_palier_requis(nom))

    def page_accueil(self):
        n = self._nb_activites_debloquees()
        sections = [
            ("S'entraîner", [
                {"t": "Entraînement", "d": "Séries de questions à ton rythme, avec chrono et combo.", "i": "🏋️", "col": CYAN,
                 "cb": lambda: self.selectionner_mode("Entraînement")},
                {"t": "Examen blanc", "d": "10 questions chronométrées, bilan noté sur 20.", "i": "📝", "col": MAG,
                 "cb": lambda: self.selectionner_mode("Examen")},
                {"t": "Assistant IA", "d": "Des questions plus avancées selon ta classe (en ligne).", "i": "🤖", "col": VIOLET, "tag": "EN LIGNE",
                 "cb": lambda: self.afficher_menu_ia_parametres(None)},
            ]),
            ("Défis", [
                {"t": "Niveaux d'activités", "d": "16 activités à débloquer selon ton rang.", "i": "🎯", "col": AMBRE, "tag": f"{n}/16",
                 "cb": lambda: self.afficher_sous_menu_niveaux_activites(None)},
                {"t": "Sujets casse-tête", "d": "Paradoxes, énigmes et défis de géométrie.", "i": "🧩", "col": VERT,
                 "cb": lambda: self.afficher_sous_menu_sujets_casse_tete(None)},
            ]),
            ("Jouer à plusieurs", [
                {"t": "Multijoueur & mode classe", "d": "Même téléphone, salle en ligne ou classe avec le professeur.", "i": "⚔️", "col": ROUGE,
                 "cb": lambda: self.afficher_hub_multijoueur()},
                {"t": "Joueurs & stats en ligne", "d": "Recherche, joueurs en ligne, classement.", "i": "🌍", "col": BLEU, "tag": "EN LIGNE",
                 "cb": lambda: self.afficher_module_joueurs()},
            ]),
            ("Mon espace", [
                {"t": "Salle des rangs & statistiques", "d": "Ton grade, tes badges, tes graphiques et ton rival.", "i": "🏆", "col": AMBRE,
                 "cb": lambda: self.afficher_sous_menu_evolution(None)},
                {"t": "Avis au développeur", "d": "Dis-nous ce que tu en penses.", "i": "💬", "col": CYAN,
                 "cb": lambda: self.afficher_interface_avis_general(None)},
            ]),
        ]
        return self.page_menu("Math Quiz", f"Bienvenue, [b]{self.nom_utilisateur}[/b] : choisis une activité pour commencer.",
                              sections, hero=self._hero_joueur(), accueil=True)

    # ------------------------------------------------------------------ entraînement / examen : cycle puis classe
    def page_niveaux(self):
        niveaux = {
            "Cycle Collège (6ème à 3ème)": ["6ème", "5ème", "4ème", "3ème"],
            "Cycle Lycée (2nde à Terminale)": ["2nde", "1ére", "Terminale"],
            " Université (Comores MPC)": ["1ére année", "2éme année"],
        }
        items = []
        for cle, ic, nom, desc, col in CYCLES:
            classes = niveaux[cle]
            items.append({"t": nom, "d": f"{desc} · {len(classes)} classes", "i": ic, "col": col,
                          "cb": lambda c=cle, l=classes: self.afficher_menu_classes(c, l)})
        mode = "Examen blanc" if self.mode_jeu == "Examen" else "Entraînement"
        return self.page_menu("Choix du cycle", f"Mode : [b]{mode}[/b]. Sélectionne ta catégorie d'étude.", [("Cycles", items)],
                              retour=lambda: self.afficher_menu_principal_modes())

    def page_classes(self, niveau, liste_classes):
        items = []
        for cl in liste_classes:
            chap = self.progression_officielle.get(cl) or []
            if chap:
                items.append({"t": cl, "d": f"{len(chap)} chapitres au programme", "i": "📖", "col": CYAN, "tag": "PROGRAMME",
                              "cb": lambda c=cl: self.initialiser_session_classe(SimpleNamespace(text=c))})
            else:
                items.append({"t": cl, "d": "Programme bientôt disponible", "i": "📖", "col": CYAN, "etat": "lock",
                              "msg": "Cette classe n'a pas encore de chapitres : choisis-en une autre."})
        mode = "Examen blanc" if self.mode_jeu == "Examen" else "Entraînement"
        return self.page_menu("Choix de la classe", f"Mode : [b]{mode}[/b]. Sélectionne ta classe pour charger le programme associé.",
                              [(niveau.strip(), items)], retour=lambda: self.afficher_menu_niveaux())

    # ------------------------------------------------------------------ niveaux d'activités
    def page_activites(self):
        idx_actuel = self.determiner_rang_et_details()[3]
        liste = self._rangs_liste()
        rang_actuel = liste[idx_actuel]["n"]
        n = self._nb_activites_debloquees()
        sections = []
        for titre, a, b in GROUPES_ACTIVITES:
            items = []
            for nom, ic, desc in ACTIVITES[a:b]:
                requis = self.obtenir_index_palier_requis(nom)
                r = liste[requis]
                if idx_actuel >= requis:
                    items.append({"t": nom, "d": desc, "i": ic, "col": r["col"], "tag": "JOUER", "rang": {"b": r["b"], "col": r["col"], "v": ["", "I", "II", "III", "IV", "V"][r["v"]] or "★"},
                                  "cb": lambda x=nom: self.lancer_activite_niveau(x)})
                else:
                    items.append({"t": nom, "d": f"Débloquée au rang {r['n']}", "i": ic, "col": r["col"], "etat": "lock",
                                  "rang": {"b": r["b"], "col": r["col"], "v": ["", "I", "II", "III", "IV", "V"][r["v"]] or "★"},
                                  "msg": f"Atteins le rang {r['n']} pour débloquer « {nom} » (tu es {rang_actuel})."})
            sections.append((titre, items))
        return self.page_menu("Niveaux d'activités", f"[b]{n}/16[/b] activités débloquées. Monte en rang pour accéder aux suivantes.",
                              sections, retour=lambda: self.afficher_menu_principal_modes())

    def page_casse_tete(self):
        items = [
            {"t": "Paradoxes mathématiques", "d": "Des affirmations qui semblent fausses… et pourtant.", "i": "🌀", "col": MAG,
             "cb": lambda: self.lancer_sujet_casse_tete("Paradoxes")},
            {"t": "Énigmes algébriques", "d": "Trouve l'inconnue cachée derrière l'énigme.", "i": "🔮", "col": CYAN,
             "cb": lambda: self.lancer_sujet_casse_tete("Énigmes")},
            {"t": "Défis géométriques poussés", "d": "Figures, angles et raisonnements avancés.", "i": "📐", "col": VERT,
             "cb": lambda: self.lancer_sujet_casse_tete("Géométrie")},
        ]
        return self.page_menu("Sujets casse-tête", f"Prépare tes neurones, [b]{self.nom_utilisateur}[/b]. Choisis un défi logique.",
                              [("Défis logiques", items)], retour=lambda: self.afficher_menu_principal_modes())

    # ------------------------------------------------------------------ multijoueur
    def page_hub(self):
        sections = [
            ("Sur le même téléphone", [
                {"t": "Même téléphone", "d": "2 à 4 joueurs qui se passent l'appareil.", "i": "📱", "col": CYAN,
                 "cb": lambda: self.afficher_sous_menu_joueurs(None)}]),
            ("Salles en ligne", [
                {"t": "Créer une salle", "d": "Chacun sur son téléphone, sans limite de joueurs.", "i": "➕", "col": MAG, "tag": "EN LIGNE",
                 "cb": lambda: self.afficher_config_salon("duel")},
                {"t": "Rejoindre avec un code", "d": "Entre le code PIN donné par l'hôte.", "i": "🔑", "col": MAG, "tag": "EN LIGNE",
                 "cb": lambda: self.afficher_rejoindre_salon("duel")}]),
            ("Mode classe", [
                {"t": "Professeur (hôte)", "d": "Lance une séance pour toute ta classe.", "i": "🧑‍🏫", "col": VERT, "tag": "EN LIGNE",
                 "cb": lambda: self.afficher_config_salon("classe")},
                {"t": "Élève (code du prof)", "d": "Rejoins la séance de ton professeur.", "i": "🎒", "col": VERT, "tag": "EN LIGNE",
                 "cb": lambda: self.afficher_rejoindre_salon("classe")}]),
            ("Communauté", [
                {"t": "Joueurs", "d": "Recherche, joueurs en ligne et classement.", "i": "🌍", "col": AMBRE, "tag": "EN LIGNE",
                 "cb": lambda: self.afficher_module_joueurs()}]),
        ]
        return self.page_menu("Multijoueur & classe", "Choisis comment jouer : sur le même téléphone, en ligne ou en classe avec le professeur.",
                              sections, retour=lambda: self.afficher_menu_principal_modes())

    def page_nombre_joueurs(self):
        items = [
            {"t": "2 joueurs", "d": "Le duel : face à face.", "i": "✌️", "col": VERT, "cb": lambda: self.afficher_sous_menu_config_noms(2)},
            {"t": "3 joueurs", "d": "Un trio qui se dispute la première place.", "i": "🔥", "col": AMBRE, "cb": lambda: self.afficher_sous_menu_config_noms(3)},
            {"t": "4 joueurs", "d": "Le grand format : tout le monde joue.", "i": "🏟️", "col": ROUGE, "cb": lambda: self.afficher_sous_menu_config_noms(4)},
        ]
        return self.page_menu("Multijoueur local", "Affrontez-vous sur le même appareil. [b]Combien de participants ?[/b]",
                              [("Participants", items)], retour=lambda: self.afficher_hub_multijoueur())

    # ------------------------------------------------------------------ assistant IA
    def page_ia_classes(self):
        items = [{"t": c, "d": "Questions adaptées à cette classe", "i": "🎓", "col": VIOLET, "cb": lambda x=c: self.enregistrer_et_continuer(x)}
                 for c in CLASSES_IA]
        return self.page_menu("Assistant IA", f"Salut [b]{getattr(self, 'nom_utilisateur', 'Élève')}[/b], sélectionne d'abord ta classe.",
                              [("Étape 1 · Ta classe", items)], retour=lambda: self.afficher_menu_principal_modes())

    def page_ia_modes(self, classe):
        items = [
            {"t": "Mode entraînement", "d": "Des questions générées pour t'exercer.", "i": "🏋️", "col": CYAN, "cb": lambda: self.lancer_mode_entrainement()},
            {"t": "Mode examen", "d": "Examen simple ou sujet type contrôle officiel.", "i": "📝", "col": MAG, "cb": lambda: self.etape_sous_menu_examen()},
        ]
        return self.page_menu("Assistant IA", f"Classe : [b]{classe}[/b]. Choisis le mode de travail.", [("Étape 2 · Le mode", items)],
                              retour=lambda: self.afficher_menu_ia_parametres(None))

    def page_ia_examen(self):
        items = [
            {"t": "Examen simple", "d": "Une série de questions chronométrées.", "i": "📄", "col": CYAN, "cb": lambda: self.etape_choix_nombre_questions()},
            {"t": "Sujet type contrôle officiel", "d": "Un sujet complet signé Math Quiz Comores.", "i": "🏛️", "col": AMBRE, "cb": lambda: self.lancer_generation_sujet_entier()},
        ]
        return self.page_menu("Mode examen", "Choisis le format de l'examen.", [("Type d'épreuve", items)],
                              retour=lambda: self.etape_selection_mode(self.classe_choisie))

    def page_ia_nombre(self):
        items = [{"t": f"{n} questions", "d": "Examen simple", "i": "🔢", "col": CYAN, "cb": lambda x=n: self.lancer_examen_simple(x)} for n in (10, 20)]
        return self.page_menu("Nombre de questions", "Combien de questions pour cet examen ?", [("Longueur", items)],
                              retour=lambda: self.etape_sous_menu_examen())

    def page_menu_ia(self):
        items = [
            {"t": "Requête & idée personnelle", "d": "Pose ta propre question à l'assistant.", "i": "💡", "col": VIOLET,
             "cb": lambda: self.afficher_formulaire_requete_libre(None)},
            {"t": "Accueil", "d": "Retour au menu principal.", "i": "🏠", "col": CYAN, "cb": lambda: self.afficher_menu_principal_modes()},
        ]
        return self.page_menu("Menu rapide", "Que veux-tu faire avec l'assistant ?", [("Actions", items)])

    # ------------------------------------------------------------------ aide
    def page_aide(self, texte):
        """Le guide d'aide : chaque titre [b]…[/b] devient un bloc déroulant."""
        blocs, titre, lignes = [], "Guide d'utilisation", []
        for brut in texte.split("\n"):
            ligne = brut.strip()
            if ligne.startswith("[b]") and ligne.endswith("[/b]") and ligne.count("[b]") == 1:
                if lignes:
                    blocs.append({"t": titre.replace(":", "").strip(), "h": "\n".join(lignes)})
                titre, lignes = ligne[3:-4], []
            elif ligne.startswith("● [b]") and ligne.endswith("[/b]"):
                if lignes:
                    blocs.append({"t": titre.replace(":", "").strip(), "h": "\n".join(lignes)})
                titre, lignes = ligne[5:-4], []
            elif ligne:
                lignes.append(ligne)
        if lignes:
            blocs.append({"t": titre.replace(":", "").strip(), "h": "\n".join(lignes)})
        return self.page_menu("Comment fonctionne l'appli", "", blocs=blocs, retour=lambda: self.afficher_menu_principal_modes())
