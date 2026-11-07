import random
import math

class MoteurMathematique:
    @staticmethod
    def moteur_generateur_mathematique(classe_cible, chapitre_cible, index_grade, niveau_profil):
        enonce, correct, opts, exp = "", "", [], ""
        variante = random.choice(["V1", "V2", "V3"])
        
        facteur_diff = 1 + (index_grade // 5) + (niveau_profil // 3)
        
# =======================================
        # 1. ARITHMÉTIQUES
# =======================================
        if chapitre_cible in ["Arithmétiques", "Arithmétique"]:
            if variante == "V1":
                div = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 11, 13])
                depart = random.randint(100 * facteur_diff, 9999 * facteur_diff)
                vrai = depart - (depart % div)
                f1 = vrai + random.randint(1, div - 1)
                f2 = vrai - random.randint(1, 10)
                if f2 == vrai: f2 -= 1
                enonce = f"Lequel de ces nombres est divisible par ${div}$ ?"
                correct = f"${vrai}$"
                opts = [correct, f"${f1}$", f"${f2}$"]
                exp = r"$n \equiv 0 \pmod{" + str(div) + r"}$" + f"\n\n${vrai} = {div} \\times {vrai // div} + 0$\n\nReste = $0$"
            elif variante == "V2":
                n = random.randint(11 * facteur_diff, 199 * facteur_diff)
                enonce = f"Le nombre {n} est-il un nombre premier ?"
                est_premier = all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))
                correct = "Oui" if est_premier else "Non"
                opts = ["Oui", "Non"]
                if est_premier:
                    exp = f"∀ p ≤ √{n} ({int(math.sqrt(n))}), p ∤ {n}\nDiviseurs = {{1, {n}}}"
                else:
                    facteur = next(i for i in range(2, n) if n % i == 0)
                    exp = f"{n} = {facteur} × {n//facteur}\nDiviseurs ⊃ {{1, {facteur}, {n}}}"
            if variante == "V3":
                a, b = random.randint(4, 150) * facteur_diff, random.randint(3, 15) * facteur_diff
                enonce = f"Quel est le reste de la division euclidienne de {a*b + 2} par {a} ?"
                correct = "2"
                opts = ["2", "0", str(b)]
                exp = f"D = d × q + r, 0 ≤ r < d\n{a*b + 2} = {a} × {b} + 2\n0 ≤ 2 < {a} ⇒ r = 2"

# =======================================
        # 2. DROITES ET SEGMENTS
# =======================================
        elif chapitre_cible == "Droites et Segments":
            if variante == "V1":
                enonce = "Si deux droites (D1) et (D2) sont toutes deux perpendiculaires à une même troisième droite (D3), alors (D1) et (D2) sont :"
                correct = "Parallèles"
                opts = [correct, "Perpendiculaires", "Sécantes"]
                exp = "(D1) ⊥ (D3) et (D2) ⊥ (D3) ⇒ (D1) // (D2)"
            if variante == "V2":
                longueur = random.choice([10, 12, 16, 20, 24, 30, 40]) * facteur_diff
                enonce = f"Si le segment [AB] mesure {longueur} cm et que le point M est son milieu géométrique, que vaut [AM] ?"
                correct = f"{longueur // 2} cm"
                opts = [f"{longueur // 2} cm", f"{longueur * 2} cm", f"{longueur // 3} cm"]
                exp = "M ∈ [AB] et AM = MB ⇒ AM = AB / 2"
            if variante == "V3":
                enonce = "Combien de points d'intersection possèdent deux droites du plan strictement parallèles ?"
                correct = "0"
                opts = ["0", "1", "Une infinité"]
                exp = "(D1) // (D2) ⇔ (D1) ∩ (D2) = ∅"

# =======================================
        # 3. NOMBRES DÉCIMAUX
# =======================================
        elif chapitre_cible == "Nombres décimaux":
            if variante == "V1":
                c, d, m = random.randint(1, 50) * facteur_diff, random.randint(1, 99), random.randint(1, 99)
                enonce = f"Déterminez l'écriture décimale standard : {c} × 10 + {d}/10 + {m}/1000"
                val = round((c * 10) + (d / 10) + (m / 1000), 3)
                correct = f"{val}".replace('.', ',')
                opts = [correct, f"{c}{d},{m}", f"{c}0,{d}{m}"]
                exp = f"Somme des positions décimales = {val}"
            if variante == "V2":
                n = (random.randint(10, 200) * facteur_diff) / 10
                enonce = f"Quelle est la partie entière du nombre décimal {n} ?"
                correct = str(int(n))
                opts = [correct, str(int(n*10) % 10), f"{n}"]
                exp = f"E({n}) = {int(n)}"
            if variante == "V3":
                enonce = "Multiplier un nombre réel fini par le coefficient décimal 0,1 revient mathématiquement à le :"
                correct = "Diviser par 10"
                opts = ["Diviser par 10", "Multiplier par 10", "Diviser par 100"]
                exp = "0,1 = 1/10"

# =======================================
        # 4. LES ANGLES
# =======================================
        elif chapitre_cible in ["Les angles", "Angles"]:
            if variante == "V1":
                ang = random.randint(1, 89)
                enonce = f"Un angle géométrique mesurant exactement {ang}° est qualifié de :"
                correct = "Aigu"
                opts = ["Aigu", "Obtus", "Droit"]
                exp = "0° < θ < 90° ⇒ Angle Aigu"
            if variante == "V2":
                ang = random.randint(91, 179)
                enonce = f"Un angle géométrique mesurant exactement {ang}° est qualifié de :"
                correct = "Obtus"
                opts = ["Aigu", "Obtus", "Droit"]
                exp = "90° < θ < 180° ⇒ Angle Obtus"
            if variante == "V3":
                prem_ang = random.choice([15, 20, 30, 40, 45, 50, 60, 75])
                enonce = f"Si deux angles sont complémentaires et que le premier vaut {prem_ang}°, quelle est la mesure du second ?"
                correct = f"{90 - prem_ang}°"
                opts = [f"{90 - prem_ang}°", f"{180 - prem_ang}°", "90°"]
                exp = "α + β = 90°"

# =======================================
        # 5. FRACTION
# =======================================
        elif chapitre_cible == "Fraction":
            num = random.randint(1, 150) * facteur_diff
            den = random.randint(1, 50)
            if variante == "V1":
                enonce = f"Déterminez la valeur décimale exacte du quotient rationnel {num}/{den} :"
                correct = f"{round(num/den, 4)}".replace('.', ',')
                opts = [correct, f"{num},{den}", f"{round(den/num, 4)}".replace('.', ',')]
                exp = f"{num} ÷ {den} = {round(num/den, 4)}"
            if variante == "V2":
                enonce = f"Simplifiez au maximum la fraction rationnelle : {num*3}/{den*3}"
                correct = f"{num}/{den}"
                opts = [correct, f"{num*2}/{den*2}", "1/2"]
                exp = f"Simplification par le facteur commun 3."
            if variante == "V3":
                enonce = f"Effectuez le calcul de la somme rationnelle : {num}/{den} + 1/{den}"
                correct = f"{num+1}/{den}"
                opts = [correct, f"{num+1}/{den*2}", f"{num+2}/{den}"]
                exp = "a/c + b/c = (a+b)/c"

# =======================================
        # 6. TRIANGLES
# =======================================
        elif chapitre_cible in ["Triangles", "Les triangles"]:
            if variante == "V1":
                enonce = "Si dans un triangle, la somme des carrés de deux côtés est égale au carré du plus grand côté, le triangle est :"
                correct = "Rectangle"
                opts = ["Rectangle", "Isocèle", "Équilatéral"]
                exp = "Réciproque du théorème de Pythagore."
            if variante == "V2":
                enonce = "Un triangle plan possédant trois côtés de longueurs rigoureusement identiques est défini comme :"
                correct = "Équilatéral"
                opts = ["Équilatéral", "Isocèle", "Scalène"]
                exp = "AB = BC = CA"
            if variante == "V3":
                enonce = "En géométrie euclidienne plane, la somme des mesures des angles intérieurs de tout triangle vaut :"
                correct = "180°"
                opts = ["180°", "360°", "90°"]
                exp = "Somme des angles = π rad = 180°"

# =======================================
        # 7. ORGANISATION DES CALCULS
# =======================================
        elif chapitre_cible == "Organisation des calculs":
            a, b, c = random.randint(1, 100) * facteur_diff, random.randint(1, 20), random.randint(1, 20)
            if variante == "V1":
                enonce = f"Calculez en respectant les priorités opératoires : {a} + {b} × {c}"
                correct = str(a + (b * c))
                opts = [correct, str((a + b) * c), str(a * b + c)]
                exp = "Priorité de la multiplication sur l'addition."
            if variante == "V2":
                enonce = f"Calculez la valeur numérique de l'expression : ({a} + {b}) × {c}"
                correct = str((a + b) * c)
                opts = [correct, str(a + b * c), str(a * b + c)]
                exp = "Priorité absolue des parenthèses."
            if variante == "V3":
                enonce = f"Calculez la valeur de l'expression : {a*b} ÷ {b} + {c}"
                correct = str(a + c)
                opts = [correct, str(a*b // (b+c)), str(a)]
                exp = "Calcul séquentiel de gauche à droite."

# =======================================
        # 8. CERCLE ET PARALLÉLOGRAMME
# =======================================
        elif chapitre_cible in ["Cercle et parallélogramme", "Cercle"]:
            r = random.randint(2, 100) * facteur_diff
            if variante == "V1":
                enonce = f"Si un cercle (C) possède un rayon R = {r} cm, quelle est la mesure exacte de son diamètre ?"
                correct = f"{r * 2} cm"
                opts = [correct, f"{r} cm", f"{r // 2} cm"]
                exp = "Diamètre D = 2 × R"
            if variante == "V2":
                enonce = "Si un quadrilatère non croisé possède ses côtés opposés deux à deux parallèles, c'est un :"
                correct = "Parallélogramme"
                opts = ["Parallélogramme", "Trapèze", "Cerf-volant"]
                exp = "Définition vectorielle ou géométrique du parallélogramme."
            if variante == "V3":
                enonce = "La droite plane qui intersecte un cercle en exactement deux points distincts est qualifiée de :"
                correct = "Sécante"
                opts = ["Sécante", "Tangente", "Corde"]
                exp = "Intersection de cardinal 2."

# =======================================
        # 9. NOMBRES DÉCIMAUX RELATIFS
# =======================================
        elif chapitre_cible in ["Entier relatifs et nombres décimaux relatifs", "Nombres décimaux relatifs"]:
            n1, n2 = random.randint(-150, -5) * facteur_diff, random.randint(2, 150)
            if variante == "V1":
                enonce = f"Calculez la somme algébrique : ({n1}) + ({n2})"
                correct = str(n1 + n2)
                opts = [correct, str(n1 - n2), str(abs(n1) + n2)]
                exp = "Addition de nombres relatifs signés."
            if variante == "V2":
                enonce = f"Calculez le produit relatif : (-2) × ({n2})"
                correct = str(-2 * n2)
                opts = [correct, str(2 * n2), str(-2 + n2)]
                exp = "Règle des signes : (-) × (+) = (-)."
            if variante == "V3":
                enonce = f"Déterminez l'élément symétrique (l'opposé) du nombre négatif {n1} :"
                correct = str(-n1)
                opts = [correct, str(n1), "0"]
                exp = "x + (-x) = 0"

# =======================================
        # 10. SYMÉTRIE CENTRALE ET AXIALE
# =======================================
        elif chapitre_cible in ["Symétrie centrale et axiale", "Symétrie centrale et orthogonale", "Symétrie centrale et Axiale"]:
            if variante == "V1":
                enonce = "Quelle transformation plane correspond à une rotation d'angle π (180°) autour d'un point fixe ?"
                correct = "Symétrie centrale"
                opts = ["Symétrie centrale", "Symétrie axiale", "Translation"]
                exp = "Rotation d'angle 180° = Symétrie centrale."
            if variante == "V2":
                enonce = "Si A' est le symétrique de A par rapport à un centre O, que représente O pour le segment [AA'] ?"
                correct = "Le milieu de [AA']"
                opts = ["Le milieu de [AA']", "L'extrémité", "Une projection perpendiculaire"]
                exp = "O est équidistant de A et A'."
            if variante == "V3":
                enonce = "Sous l'action d'une symétrie axiale, quelles grandeurs géométriques sont rigoureusement invariantes ?"
                correct = "Les longueurs et les aires"
                opts = ["Les longueurs et les aires", "Uniquement l'orientation", "Rien"]
                exp = "Conservation métrique globale."

# =======================================
        # 11. CALCULS LITTÉRAUX
# =======================================
        elif chapitre_cible in ["Initiation aux calculs littéraux", "Calcul littérale", "Calcul sur les expressions algébriques"]:
            a, b, c = random.randint(2, 50) * facteur_diff, random.randint(1, 50), random.randint(1, 50)
            if variante == "V1":
                enonce = f"Réduisez l'expression littérale en factorisant par x : {a}x + {b}x - {c}x"
                correct = f"{a + b - c}x"
                opts = [correct, f"{a + b}x²", f"{a - b}x"]
                exp = f"({a} + {b} - {c})x = {a + b - c}x"
            if variante == "V2":
                enonce = f"Développez par distributivité simple : {a} × (x + 2)"
                correct = f"{a}x + {a*2}"
                opts = [correct, f"{a}x + 2", f"{a+2}x"]
                exp = f"Multiplication terme à terme."
            if variante == "V3":
                enonce = f"Évaluez la valeur numérique du polynôme (2x + 5) pour x = {3 * facteur_diff}"
                val_calc = 2 * (3 * facteur_diff) + 5
                correct = str(val_calc)
                opts = [correct, str(val_calc + 2), "11"]
                exp = "Substitution algébrique directe."

# =======================================
        # 12. PROPORTIONNALITÉ
# =======================================
        elif chapitre_cible == "Proportionnalité":
            val = random.randint(3, 100) * facteur_diff
            if variante == "V1":
                enonce = f"Si 2 objets coûtent {2*val} KMF, déterminez par proportionnalité le prix de 5 objets."
                correct = f"{5 * val} KMF"
                opts = [correct, f"{4 * val} KMF", f"{6 * val} KMF"]
                exp = f"Coefficient k = {val}"
            elif variante == "V2":
                enonce = "Dans un tableau de proportionnalité entre x et y, le coefficient k s'obtient par :"
                correct = "Divisant une valeur du bas par celle du haut"
                opts = ["Divisant une valeur du bas par celle du haut", "Multipliant les deux", "Soustrayant"]
                exp = "k = y / x"
            elif variante == "V3":
                enonce = "En mouvement uniforme, doubler le temps de parcours Δt implique de :"
                correct = "Doubler la distance"
                opts = ["Doubler la distance", "Diviser par 2", "Laisser identique"]
                exp = "d = v × t"

        # ==========================================
        # 13. GÉOMÉTRIE DANS L'ESPACE (CUBE, CYLINDRE, PYRAMIDE)
        # ==========================================
        elif chapitre_cible in ["Cube – Pavé droit – Cylindre", "Prisme droit", "Pyramide", "Pyramide et cône de révolution", "Pyramide et cône"]:
            c = random.randint(2, 50) * facteur_diff
            if variante == "V1":
                enonce = f"Calculez le volume exact d'un cube dont l'arête mesure {c} cm."
                correct = f"{c**3} cm³"
                opts = [correct, f"{c*3} cm³", f"{c**2} cm³"]
                exp = f"V = c³ = {c}³"
            elif variante == "V2":
                enonce = "Combien de faces planes possède un pavé droit (parallélépipède rectangle) ?"
                correct = "6"
                opts = ["6", "8", "12"]
                exp = "6 faces rectangulaires."
            elif variante == "V3":
                enonce = "L'expression générale permettant de calculer le volume d'une pyramide est :"
                correct = "(1/3) × Aire base × Hauteur"
                opts = ["(1/3) × Aire base × Hauteur", "Aire base × Hauteur", "Côté × Hauteur"]
                exp = "Formule générale du volume conique/pyramidale."

        # ==========================================
        # 14. POURCENTAGE ET ÉCHELLE
        # ==========================================
        elif chapitre_cible == "Pourcentage et échelle":
            if variante == "V1":
                p = random.choice([10, 20, 25, 40, 50, 60, 75, 80])   
                enonce = f"Appliquer un taux de pourcentage de {p}% sur une grandeur scalaire revient à la :"  
                if 100 % p == 0:
                    d = 100 // p
                    correct = f"Diviser par {d}"
                    opts = [correct, f"Multiplier par {d}", f"Diviser par {d * 2}"]
                    exp = f"{p}% = 1/{d}"
                else:
                    val = p / 100
                    correct = f"Multiplier par {val}"
                    opts = [correct, f"Diviser par {val}", f"Multiplier par {val * 2}"]
                    exp = f"{p}% = {val}"     
                random.shuffle(opts)
            elif variante == "V2":
                base_p = 250 * facteur_diff
                enonce = f"Calculez la valeur numérique exacte correspondant à 10% de {base_p}."
                correct = f"{base_p // 10}"
                opts = [f"{base_p // 10}", f"{base_p // 100}", f"{base_p}"]
                exp = f"{base_p} × 0,1"
            elif variante == "V3":
                enonce = "Sur une carte à l'échelle 1/100, une longueur de 1 cm correspond sur le terrain à :"
                correct = "100 cm (1 m)"
                opts = ["100 cm (1 m)", "10 cm", "1000 cm"]
                exp = "Échelle = Distance carte / Distance terrain."

        # ==========================================
        # 15. PUISSANCE
        # ==========================================
        elif chapitre_cible == "Puissance":
            b = random.randint(2, 15)
            e = random.randint(2, 6)
            if variante == "V1":
                enonce = f"Calculez la valeur exacte de l'élévation à la puissance : {b}^{e}"
                correct = str(b ** e)
                opts = [correct, str(b * e), str(b ** (e-1))]
                exp = "Multiplication itérée."
            elif variante == "V2":
                enonce = f"Simplifiez l'expression : {b}² × {b}³"
                correct = str(b ** 5)
                opts = [str(b ** 5), str(b ** 6), str(b ** 2)]
                exp = "a^m × a^n = a^(m+n)"
            elif variante == "V3":
                enonce = f"Quelle est la valeur mathématique de {b}⁰ ?"
                correct = "1"
                opts = ["1", "0", str(b)]
                exp = "Propriété des puissances : x⁰ = 1 pour x ≠ 0."

        # ==========================================
        # 16. DISTANCE ENTRE DEUX POINTS
        # ==========================================
        elif chapitre_cible == "Distance entre deux points":
            x1, x2 = random.randint(-40, -1) * facteur_diff, random.randint(1, 40) * facteur_diff
            if variante == "V1":
                enonce = f"Sur une droite graduée, déterminez la distance euclidienne entre A({x1}) et B({x2})."
                correct = str(x2 - x1)
                opts = [correct, str(abs(x2 + x1)), str(x1 - x2)]
                exp = "d = |xB - xA|"
            elif variante == "V2":
                enonce = f"Quel est le milieu du segment [AB] avec A({x1}) et B({x2}) ?"
                correct = f"{(x1 + x2) / 2}"
                opts = [f"{(x1 + x2) / 2}", f"{x2 - x1}", f"{(x2 - x1) / 2}"]
                exp = "M = (xA + xB) / 2"
            elif variante == "V3":
                enonce = "Si la distance d'un point x à 0 sur un axe vaut 7, quelles sont les valeurs possibles de x ?"
                correct = "7 ou -7"
                opts = ["7 ou -7", "7", "-7"]
                exp = "|x| = a ⇒ x = a ou x = -a"

        # ==========================================
        # 17. MÉDIATRICE D'UN SEGMENT
        # ==========================================
        elif chapitre_cible == "Médiatrice d’un segment":
            p_ext = random.choice([("E","F"), ("P","Q"), ("X","Y")])
            if variante == "V1":
                enonce = f"Si M appartient à la médiatrice de [{p_ext[0]}{p_ext[1]}], quelle relation est vérifiée ?"
                correct = f"M{p_ext[0]} = M{p_ext[1]}"
                opts = [f"M{p_ext[0]} = M{p_ext[1]}", f"M{p_ext[0]} + M{p_ext[1]} = 0", "Alignés"]
                exp = "Équidistance des extrémités."
            elif variante == "V2":
                enonce = f"La médiatrice d'un segment [{p_ext[0]}{p_ext[1]}] lui est :"
                correct = "Perpendiculaire en son milieu"
                opts = ["Perpendiculaire en son milieu", "Parallèle", "Sécante quelconque"]
                exp = "Définition géométrique."
            elif variante == "V3":
                enonce = f"L'ensemble des points équidistants des points {p_ext[0]} et {p_ext[1]} forme :"
                correct = "Une droite (la médiatrice)"
                opts = ["Une droite (la médiatrice)", "Un cercle", "Un point unique"]
                exp = "Caractérisation géométrique."

        # ==========================================
        # 18. PGCD ET PPCM
        # ==========================================
        elif chapitre_cible in ["PGCD et PPCM", "PGDC et PPCM"]:
            f = random.choice([2, 3, 5])
            a, b = f * random.randint(2, 5) * facteur_diff, f * random.randint(6, 10) * facteur_diff
            if variante == "V1":
                enonce = f"Déterminez le Plus Grand Commun Diviseur (PGCD) de {a} et {b}."
                correct = str(math.gcd(a, b))
                opts = [correct, str(f), str(a * b)]
                exp = "Algorithme d'Euclide."
            elif variante == "V2":
                enonce = f"Déterminez le PPCM de {a} et {b}."
                ppcm_val = abs(a * b) // math.gcd(a, b)
                correct = str(ppcm_val)
                opts = [correct, str(a * b), str(math.gcd(a, b))]
                exp = "PPCM(a,b) = |a × b| / PGCD(a,b)"
            elif variante == "V3":
                enonce = "Si le PGCD de deux nombres vaut 1, on dit qu'ils sont :"
                correct = "Premiers entre eux"
                opts = ["Premiers entre eux", "Tous deux premiers", "Pairs"]
                exp = "Définition de la coprimalité."

        # ==========================================
        # 19. NOMBRES RATIONNELS
        # ==========================================
        elif chapitre_cible == "Nombres rationnels":
            n_rat = random.randint(2, 8) * facteur_diff
            d_rat = random.choice([7, 9, 11])
            if variante == "V1":
                enonce = f"Le nombre {n_rat}/{d_rat} appartient à l'ensemble Q. Sa définition formelle est :"
                correct = "Le quotient d'un entier par un entier non nul"
                opts = ["Le quotient d'un entier par un entier non nul", "Un nombre décimal fini", "Une racine carrée"]
                exp = "Q = {a/b ; a ∈ Z, b ∈ Z*}"
            elif variante == "V2":
                enonce = "Tout nombre décimal est-il un nombre rationnel ?"
                correct = "Oui"
                opts = ["Oui", "Non"]
                exp = "Inclusion Z ⊂ D ⊂ Q."
            elif variante == "V3":
                enonce = "L'écriture fractionnaire d'un nombre rationnel est-elle unique ?"
                correct = "Non (il existe des fractions équivalentes)"
                opts = ["Non (il existe des fractions équivalentes)", "Oui", "Seulement si le dénominateur est 1"]
                exp = "Simplification par un facteur commun."

        # ==========================================
        # 20. DISTANCE D'UN POINT À UNE DROITE
        # ==========================================
        elif chapitre_cible == "Distance d’un point à une droite":
            pt_nom = random.choice(["M", "P", "K"])
            if variante == "V1":
                enonce = f"Le plus court chemin reliant un point {pt_nom} à une droite (D) correspond à la distance entre {pt_nom} et :"
                correct = "Son projeté orthogonal sur (D)"
                opts = ["Son projeté orthogonal sur (D)", "Le milieu", "L'origine"]
                exp = "Minimisation par la perpendiculaire."
            elif variante == "V2":
                enonce = f"Si le point {pt_nom} appartient directement à la droite (D), que vaut sa distance à (D) ?"
                correct = "0"
                opts = ["0", "1", "L'infini"]
                exp = "Distance nulle."
            elif variante == "V3":
                enonce = "La distance d'un point à une droite est mesurée le long d'un segment ____ à cette droite."
                correct = "Perpendiculaire"
                opts = ["Perpendiculaire", "Parallèle", "Incliné"]
                exp = "Orthogonalité obligatoire."

        # ==========================================
        # 21. SECTEURS ANGULAIRES
        # ==========================================
        elif chapitre_cible == "Secteurs angulaires":
            portion = random.choice([(2, 180), (3, 120), (4, 90), (6, 60)])
            if variante == "V1":
                enonce = f"Si un secteur angulaire occupe 1/{portion[0]} d'un disque, quelle est la mesure de son angle au centre ?"
                correct = f"{portion[1]}°"
                opts = ["90°", "180°", "120°", "60°"]
                exp = f"360° / {portion[0]}"
            elif variante == "V2":
                enonce = "Quelle est la mesure totale en degrés d'un secteur angulaire formant un disque complet ?"
                correct = "360°"
                opts = ["360°", "180°", "90°"]
                exp = "Tour complet."
            elif variante == "V3":
                enonce = "Un secteur angulaire de 180° dans un disque représente un :"
                correct = "Demi-disque (angle plat)"
                opts = ["Demi-disque (angle plat)", "Quart de disque", "Cercle complet"]
                exp = "Angle plat = 180°."

        # ==========================================
        # 22. PROJECTION
        # ==========================================
        elif chapitre_cible == "Projection":
            if variante == "V1":
                enonce = "Lors d'une projection orthogonale sur une droite, quelle propriété est toujours invariante ?"
                correct = "L'alignement des points"
                opts = ["L'alignement des points", "La longueur", "L'angle"]
                exp = "Conservation de l'alignement."
            elif variante == "V2":
                enonce = "Si I est le milieu de [AB], son projeté orthogonal I' sur une droite sera :"
                correct = "Le milieu du segment projeté [A'B']"
                opts = ["Le milieu du segment projeté [A'B']", "Perpendiculaire", "Confondu avec l'origine"]
                exp = "Conservation du milieu."
            elif variante == "V3":
                enonce = "Le projeté orthogonal d'un point M sur (D) s'obtient à l'intersection de (D) avec :"
                correct = "La perpendiculaire à (D) passant par M"
                opts = ["La perpendiculaire à (D) passant par M", "La parallèle", "Le cercle"]
                exp = "Construction géométrique."

        # ==========================================
        # 23. OUTIL VECTORIEL
        # ==========================================
        elif chapitre_cible == "Outil vectoriel":
            v1 = random.choice(["A", "B", "C"])
            if variante == "V1":
                enonce = f"D'après la relation de Chasles, simplifiez la somme vectorielle : vec({v1}B) + vec(BX)"
                correct = f"vec({v1}X)"
                opts = [f"vec({v1}X)", f"vec(BX)", f"vec({v1}B)"]
                exp = "Relation de Chasles : vec(AB) + vec(BC) = vec(AC)"
            elif variante == "V2":
                enonce = "Que vaut la somme vectorielle vec(AB) + vec(BA) ?"
                correct = "Le vecteur nul vec(0)"
                opts = ["Le vecteur nul vec(0)", "vec(AA)", "vec(BB)"]
                exp = "Vecteur opposé."
            elif variante == "V3":
                enonce = "Deux vecteurs non nuls sont colinéaires si et seulement si :"
                correct = "Leurs directions sont parallèles"
                opts = ["Leurs directions sont parallèles", "Leurs normes sont égales", "Ils sont orthogonaux"]
                exp = "Définition de la colinéarité."

        # ==========================================
        # 24. STATISTIQUE
        # ==========================================
        elif chapitre_cible == "Statistique":
            s1, s2, s3 = random.randint(10, 20) * facteur_diff, random.randint(5, 15) * facteur_diff, random.randint(12, 25) * facteur_diff
            if variante == "V1":
                enonce = f"Calculez la moyenne arithmétique simple de la série : {s1}, {s2}, {s3}."
                m_calc = round((s1 + s2 + s3) / 3, 2)
                correct = f"{m_calc}".replace('.', ',')
                opts = [correct, f"{(s1+s2)/2}".replace('.', ','), f"{s1+s2+s3}"]
                exp = "Somme divisée par l'effectif total."
            elif variante == "V2":
                enonce = "Dans une série ordonnée, la valeur qui partage l'effectif total en deux parts égales est :"
                correct = "La médiane"
                opts = ["La médiane", "La moyenne", "L'étendue"]
                exp = "Définition de la médiane."
            elif variante == "V3":
                enonce = "L'étendue d'une série statistique s'obtient en calculant :"
                correct = "La différence entre la plus grande et la plus petite valeur"
                opts = ["La différence entre la plus grande et la plus petite valeur", "La somme", "La moyenne"]
                exp = "Max - Min."

        # ==========================================
        # 25. SPHÈRE ET BOULE
        # ==========================================
        elif chapitre_cible == "Sphère et boule":
            r_sph = random.choice([2, 3, 5, 10]) * facteur_diff
            if variante == "V1":
                enonce = f"Calculez l'aire superficielle externe d'une sphère de rayon R = {r_sph} cm :"
                a_sph = 4 * (r_sph ** 2)
                correct = f"{a_sph}π cm²"
                opts = [correct, f"{2 * r_sph}π cm²", f"{a_sph // 4}π cm²"]
                exp = "A = 4πR²"
            elif variante == "V2":
                enonce = f"Calculez le volume d'une boule de rayon R = {r_sph} cm :"
                correct = f"{(4 * r_sph**3)}/3 π cm³"
                opts = [correct, f"{4 * r_sph**3}π cm³", f"{r_sph**3}π cm³"]
                exp = "V = (4/3)πR³"
            elif variante == "V3":
                enonce = "L'intersection d'une sphère et d'un plan passant par son centre est un :"
                correct = "Grand cercle"
                opts = ["Grand cercle", "Point", "Cercle mineur"]
                exp = "Section plane diamétrale."

        # ==========================================
        # 26. RENFORCEMENT DE CAPACITÉ
        # ==========================================
        elif chapitre_cible in ["Renforcement de capacité", "Renforcement de capacity"]:
            a = random.randint(2, 6)
            b = random.randint(2, 10)
            res = a * (random.randint(2, 8) * facteur_diff) + b
            if variante == "V1":
                enonce = f"Résolvez l'équation du 1er degré dans R : {a}x + {b} = {res}"
                correct = str((res - b) // a)
                opts = [correct, str(res - b), str(res + a)]
                exp = f"{a}x = {res - b} ⇒ x = {(res - b) // a}"
            elif variante == "V2":
                enonce = f"Nombre de solutions de l'équation linéaire : {a}x + {b} = {a}x + {res}"
                correct = "Aucune solution (ensemble vide)"
                opts = ["Aucune solution (ensemble vide)", "Une solution", "Une infinité"]
                exp = "Impossibilité mathématique."
            elif variante == "V3":
                enonce = "Une équation ax = b (avec a ≠ 0) admet toujours :"
                correct = "Une solution unique x = b/a"
                opts = ["Une solution unique x = b/a", "Aucune solution", "Deux solutions"]
                exp = "Résolution basique."

        # ==========================================
        # 27. RACINE CARRÉE ET VALEUR ABSOLUE
        # ==========================================
        elif chapitre_cible == "Racine carrée et Valeur absolue":
            val_abs = random.randint(-20, -2) * facteur_diff
            if variante == "V1":
                enonce = f"Simplifiez l'expression analytique suivante : √(({val_abs})²)"
                correct = str(abs(val_abs))
                opts = [correct, str(val_abs), str(val_abs ** 2)]
                exp = "√(x²) = |x|"
            elif variante == "V2":
                enonce = f"Que vaut la valeur absolue |{val_abs}| ?"
                correct = str(abs(val_abs))
                opts = [str(abs(val_abs)), str(val_abs), "0"]
                exp = "Opposé d'un nombre négatif."
            elif variante == "V3":
                enonce = "Pour tout réel x, la quantité √x² est toujours :"
                correct = "Positive ou nulle (≥ 0)"
                opts = ["Positive ou nulle (≥ 0)", "Négative", "Strictement négative"]
                exp = "Propriété de positivité de la valeur absolue."

# =======================================
        # 28. TRIANGLE RECTANGLE
# =======================================
        elif chapitre_cible == "Triangle rectangle":
            adj = random.randint(3, 15) * facteur_diff
            hyp = adj + random.randint(2, 8)
            if variante == "V1":
                enonce = f"Dans un triangle rectangle, si adjacent = {adj} et hypoténuse = {hyp}, que vaut Cos(α) ?"
                correct = f"{adj}/{hyp}"
                opts = [f"{adj}/{hyp}", f"{hyp}/{adj}", f"{adj * hyp}"]
                exp = "Cos(α) = Adjacent / Hypothénuse"
            elif variante == "V2":
                enonce = "Dans un triangle rectangle, le carré de l'hypoténuse est égal à :"
                correct = "La somme des carrés des deux autres côtés"
                opts = ["La somme des carrés des deux autres côtés", "Le produit", "La différence"]
                exp = "Théorème de Pythagore."
            elif variante == "V3":
                enonce = "Le sinus d'un angle aigu dans un triangle rectangle est le rapport entre :"
                correct = "Le côté opposé et l'hypoténuse"
                opts = ["Le côté opposé et l'hypoténuse", "Le côté adjacent et l'hypoténuse", "Opposé / Adjacent"]
                exp = "Définition du sinus."

# =======================================
        # 29. MONÔME ET POLYNÔME
# =======================================
        elif chapitre_cible == "Monôme et polynôme":
            val_id = random.choice([2, 3, 4, 5, 6, 8]) * facteur_diff
            if variante == "V1":
                enonce = f"Donnez la factorisation de l'expression : x² - {val_id**2}"
                correct = f"(x - {val_id})(x + {val_id})"
                opts = [f"(x - {val_id})(x + {val_id})", f"(x - {val_id})²", f"x(x - {val_id**2})"]
                exp = "Identité remarquable a² - b² = (a-b)(a+b)"
            elif variante == "V2":
                enonce = f"Développez l'identité remarquable : (x + {val_id})²"
                correct = f"x² + {2*val_id}x + {val_id**2}"
                opts = [f"x² + {2*val_id}x + {val_id**2}", f"x² + {val_id**2}", f"x² + {val_id}x"]
                exp = "(a+b)² = a² + 2ab + b²"
            elif variante == "V3":
                enonce = "Quel est le degré du polynôme P(x) = 5x³ - 2x + 7 ?"
                correct = "3"
                opts = ["3", "5", "7", "2"]
                exp = "Degré = plus haute puissance de x."

# =======================================
        # 30. THALÈS
# =======================================
        elif chapitre_cible in ["Thales", "Tháles"]:
            div_t = random.choice([2, 3, 4])
            tot_t = div_t * random.randint(3, 8) * facteur_diff
            if variante == "V1":
                enonce = f"Dans Thalès avec (AB)//(CD), OA = {div_t}, OB = 5, OC = {tot_t}, calculez OD."
                correct = str((tot_t * 5) // div_t)
                opts = [correct, str(tot_t + 5), str(tot_t - div_t)]
                exp = "Rapport de proportionnalité OA/OC = OB/OD"
            elif variante == "V2":
                enonce = "Le théorème de Thalès sert principalement à calculer des :"
                correct = "Longueurs de segments"
                opts = ["Longueurs de segments", "Angles", "Aires"]
                exp = "Calcul métrique géométrique."
            elif variante == "V3":
                enonce = "Pour appliquer le théorème de Thalès, les droites de la figure doivent être :"
                correct = "Sécantes et coupées par des parallèles"
                opts = ["Sécantes et coupées par des parallèles", "Perpendiculaires", "Non coplanaires"]
                exp = "Conditions d'application."

# =======================================
        # 31. ÉQUATION D'UNE DROITE
# =======================================
        elif chapitre_cible == "Equation d’une droite":
            a_dir = random.randint(-8, 8) * facteur_diff
            if a_dir == 0: a_dir = 2
            b_ord = random.randint(1, 12)
            if variante == "V1":
                enonce = f"Quel est le coefficient directeur de la droite d'équation réduite : y = {a_dir}x + {b_ord} ?"
                correct = str(a_dir)
                opts = [correct, str(b_ord), str(-a_dir)]
                exp = "y = mx + p ⇒ m = coefficient directeur."
            elif variante == "V2":
                enonce = f"Quelle est l'ordonnée à l'origine de la droite y = {a_dir}x + {b_ord} ?"
                correct = str(b_ord)
                opts = [str(b_ord), str(a_dir), "0"]
                exp = "y = mx + p ⇒ p = ordonnée à l'origine."
            elif variante == "V3":
                enonce = "Deux droites d'équations y = m1x + p1 et y = m2x + p2 sont parallèles si :"
                correct = "m1 = m2"
                opts = ["m1 = m2", "m1 × m2 = -1", "p1 = p2"]
                exp = "Égalité des pentes."

# =======================================
        # 32. APPLICATION AFFINE
# =======================================
        elif chapitre_cible == "Application affine":
            coef_a = random.randint(2, 10) * facteur_diff
            x_val = random.randint(2, 8)
            if variante == "V1":
                enonce = f"Soit f(x) = {coef_a}x. Calculez l'image de la valeur {x_val}."
                correct = str(coef_a * x_val)
                opts = [correct, str(coef_a + x_val), str(coef_a)]
                exp = f"f({x_val}) = {coef_a} × {x_val}"
            elif variante == "V2":
                enonce = "Une fonction affine s'exprime généralement sous la forme :"
                correct = "f(x) = ax + b"
                opts = ["f(x) = ax + b", "f(x) = ax²", "f(x) = a/x"]
                exp = "Forme générale algébrique."
            elif variante == "V3":
                enonce = "Si le coefficient directeur d'une fonction affine est positif, la fonction est :"
                correct = "Strictement croissante"
                opts = ["Strictement croissante", "Strictement décroissante", "Constante"]
                exp = "Sens de variation."

# =======================================
        # 33. SYSTÈME DANS IR²
# =======================================
        elif chapitre_cible == "Système dans IR²":
            if variante == "V1":
                enonce = "Si deux droites d'un système linéaire dans IR² ont des pentes distinctes, le système admet :"
                correct = "Une solution unique"
                opts = ["Une solution unique", "Aucune solution", "Une infinité"]
                exp = "Intersection unique."
            elif variante == "V2":
                enonce = "Si deux droites d'un système linéaire sont strictement parallèles, l'ensemble des solutions est :"
                correct = "Vide (aucune solution)"
                opts = ["Vide (aucune solution)", "Un point", "Une infinité"]
                exp = "Absence d'intersection."
            elif variante == "V3":
                enonce = "Résoudre graphiquement un système 2x2 revient à chercher :"
                correct = "Les points d'intersection des droites"
                opts = ["Les points d'intersection des droites", "Les sommets", "Le centre"]
                exp = "Interprétation graphique."

# =======================================
        # 34. ANGLES ET ROTATION
# =======================================
        elif chapitre_cible == "Angles et Rotation":
            if variante == "V1":
                enonce = "Une rotation plane d'angle 180° modifie-t-elle la distance euclidienne ?"
                correct = "Non, car c'est une isométrie"
                opts = ["Non, car c'est une isométrie", "Oui", "Uniquement si le centre est l'origine"]
                exp = "Conservation des distances par isométrie."
            elif variante == "V2":
                enonce = "Une rotation conserve-t-elle la mesure des angles géométriques ?"
                correct = "Oui"
                opts = ["Oui", "Non"]
                exp = "Conservation angulaire."
            elif variante == "V3":
                enonce = "Quel est l'angle d'un quart de tour direct en géométrie ?"
                correct = "90° (ou π/2 rad)"
                opts = ["90° (ou π/2 rad)", "180°", "360°"]
                exp = "Valeur d'un quart de tour."

# =======================================
        # 35. SUJET TYPES
# =======================================
        elif chapitre_cible == "Sujet types":
            k = random.choice([2, 3, 4, 5]) * facteur_diff
            if variante == "V1":
                enonce = f"Dans un triangle ABC rectangle en A, si AB = {k*3} et AC = {k*4}, déterminez l'hypoténuse BC."
                correct = f"{k*5} cm"
                opts = [f"{k*5} cm", f"{k*7} cm", f"{(k*5)**2} cm"]
                exp = "Triplet pythagoricien (3, 4, 5)."
            elif variante == "V2":
                enonce = "Quel théorème utilise-t-on pour calculer un côté dans un triangle rectangle ?"
                correct = "Le théorème de Pythagore"
                opts = ["Le théorème de Pythagore", "Thalès", "Al-Kashi"]
                exp = "Pythagore."
            elif variante == "V3":
                enonce = "La somme des angles aigus dans un triangle rectangle vaut :"
                correct = "90° (π/2 rad)"
                opts = ["90° (π/2 rad)", "180°", "45°"]
                exp = "Complémentarité des angles aigus."

# =======================================
        # 36. VECTEURS ET REPÉRAGE
# =======================================
        elif chapitre_cible == "Vecteurs et repérage":
            x, y = random.randint(1, 50) * facteur_diff, random.randint(1, 10)
            if variante == "V1":
                enonce = f"Soit u({x}, {y}). Déterminez les coordonnées du vecteur 2u."
                correct = f"({x*2}, {y*2})"
                opts = [correct, f"({x}, {y})", f"({x+2}, {y+2})"]
                exp = "Multiplication par un scalaire."
            elif variante == "V2":
                enonce = "Quelle est la norme du vecteur u(3, 4) dans un repère orthonormal ?"
                correct = "5"
                opts = ["5", "7", "25"]
                exp = "||u|| = √(3² + 4²) = 5"
            elif variante == "V3":
                enonce = "Dans un repère, les coordonnées du vecteur AB se calculent par :"
                correct = "(xB - xA, yB - yA)"
                opts = ["(xB - xA, yB - yA)", "(xA + xB, yA + yB)", "(xA - xB, yA - yB)"]
                exp = "Extrémité moins origine."

# =======================================
        # 37. VALEUR ABSOLUE ET INTERVALLES
# =======================================
        elif chapitre_cible == "Valeur absolue et intervalles":
            val = random.randint(2, 100) * facteur_diff
            if variante == "V1":
                enonce = f"Résolvez l'équation d'intervalle simple : |x| = {val}"
                correct = f"x = {val} ou x = -{val}"
                opts = [correct, f"x = {val}", "Aucune solution"]
                exp = "Double solution en valeur absolue."
            elif variante == "V2":
                enonce = f"L'inéquation |x| < {val} équivaut à l'intervalle :"
                correct = f"]-{val}, {val}["
                opts = [f"]-{val}, {val}[", f"[{val}, +inf[", f"]-inf, -{val}["]
                exp = "Caractérisation d'un intervalle centré."
            elif variante == "V3":
                enonce = "La distance entre deux réels a et b sur la droite numérique est :"
                correct = "|a - b|"
                opts = ["|a - b|", "a + b", "a × b"]
                exp = "Définition de la distance algébrique."

# =======================================
        # 38. DÉRIVATION FONCTIONNELLE
# =======================================
        elif chapitre_cible == "Polynômes du second degré":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "Si le discriminant Δ < 0, combien de racines réelles possède le polynôme ?", "correct": "0", "opts": ["0", "1 racine double", "2 racines distinctes"], "exp": "Pas d'intersection avec l'axe des abscisses."},
                    {"enonce": "Quelle est la forme canonique d'un polynôme du second degré P(x) = ax² + bx + c (avec a ≠ 0) ?", "correct": "a · (x + b/(2a))² - (Δ / (4a))", "opts": ["a · (x + b/(2a))² - (Δ / (4a))", "a · (x - a)² + b", "a · (x² + x + c)"], "exp": "Forme canonique générale issue de la mise sous forme de carré parfait."},
                    {"enonce": "Si le discriminant Δ = 0, quelle est l'unique racine (dite double) du polynôme ax² + bx + c ?", "correct": "-b / (2a)", "opts": ["-b / (2a)", "-b / a", "b / (2a)"], "exp": "Formule de la racine double x_0 = -b/(2a)."},
                    {"enonce": "Quel est le signe du coefficient a pour que la parabole représentative d'un polynôme du second degré soit tournée vers le haut (convexe) ?", "correct": "a > 0", "opts": ["a > 0", "a < 0", "a = 0"], "exp": "Si a > 0, la parabole présente un minimum (branches vers le haut)."},
                    {"enonce": "Quel est le signe du coefficient a pour que la parabole présente un maximum (branches vers le bas) ?", "correct": "a < 0", "opts": ["a < 0", "a > 0", "a = 1"], "exp": "Si a < 0, la parabole est tournée vers le bas."},
                    {"enonce": "Quelles sont les coordonnées du sommet S de la parabole d'équation y = ax² + bx + c ?", "correct": "S(-b / (2a) ; -Δ / (4a))", "opts": ["S(-b / (2a) ; -Δ / (4a))", "S(0 ; c)", "S(c ; -b/a)"], "exp": "Coordonnées canoniques du sommet de la parabole."},
                    {"enonce": "Quelle est l'équation de l'axe de symétrie de la parabole représentant un polynôme du second degré ?", "correct": "x = -b / (2a)", "opts": ["x = -b / (2a)", "y = 0", "x = c / a"], "exp": "L'axe de symétrie vertical passe par l'abscisse du sommet."},
                    {"enonce": "Que vaut la somme S des racines x_1 et x_2 d'un polynôme ax² + bx + c lorsque Δ ≥ 0 ?", "correct": "S = -b / a", "opts": ["S = -b / a", "S = c / a", "S = b / (2a)"], "exp": "Relations de Viète : x_1 + x_2 = -b/a."},
                    {"enonce": "Que vaut le produit P des racines x_1 et x_2 d'un polynôme ax² + bx + c lorsque Δ ≥ 0 ?", "correct": "P = c / a", "opts": ["P = c / a", "P = -b / a", "P = -c / a"], "exp": "Relations de Viète : x_1 · x_2 = c/a."},
                    {"enonce": "Si un polynôme ax² + bx + c admet deux racines distinctes x_1 et x_2, quelle est sa forme factorisée ?", "correct": "a · (x - x_1) · (x - x_2)", "opts": ["a · (x - x_1) · (x - x_2)", "(x + x_1)(x + x_2)", "a · (x + x_1)(x - x_2)"], "exp": "Factorisation standard à l'aide des racines."},
                    {"enonce": "Quel est le signe d'un polynôme du second degré à l'extérieur des racines (lorsque Δ > 0) ?", "correct": "Du signe de a", "opts": ["Du signe de a", "Du signe opposé à a", "Toujours négatif"], "exp": "Règle du signe du trinôme : du signe de a à l'extérieur des racines."},
                    {"enonce": "Quel est le signe d'un polynôme du second degré à l'intérieur des racines (lorsque Δ > 0) ?", "correct": "Du signe opposé à a", "opts": ["Du signe opposé à a", "Du signe de a", "Toujours positif"], "exp": "Le trinôme est du signe de -a entre les racines."},
                    {"enonce": "Si Δ = 0, quel est le signe du trinôme ax² + bx + c pour tout x différent de la racine double x_0 ?", "correct": "Du signe de a (s'annule en x_0)", "opts": ["Du signe de a (s'annule en x_0)", "Du signe opposé à a", "Toujours négatif"], "exp": "Le trinôme garde le signe de a partout sauf au sommet."},
                    {"enonce": "Si Δ < 0, quel est le signe du trinôme ax² + bx + c pour tout x réel ?", "correct": "Strictement du signe de a partout", "opts": ["Strictement du signe de a partout", "Strictement négatif", "Change de signe"], "exp": "Pas de racine réelle ⇒ pas de changement de signe."},
                    {"enonce": "Comment appelle-t-on la courbe représentative d'une fonction polynôme du second degré dans un repère ?", "correct": "Une parabole", "opts": ["Une parabole", "Une hyperbole", "Une droite"], "exp": "Définition géométrique de la courbe."},
                    {"enonce": "Si la somme des coefficients a + b + c = 0, que peut-on affirmer immédiatement pour le polynôme ?", "correct": "1 est racine évidente (x_1 = 1 et x_2 = c/a)", "opts": ["1 est racine évidente (x_1 = 1 et x_2 = c/a)", "0 est racine", "Le discriminant est négatif"], "exp": "Propriété des racines évidentes a + b + c = 0."},
                    {"enonce": "Si a - b + c = 0, que peut-on affirmer immédiatement pour le polynôme ?", "correct": "-1 est racine évidente (x_1 = -1 et x_2 = -c/a)", "opts": ["-1 est racine évidente (x_1 = -1 et x_2 = -c/a)", "1 est racine", "Le discriminant est nul"], "exp": "Propriété des racines évidentes a - b + c = 0."},
                    {"enonce": "Quelle est la dérivée de la fonction polynôme f(x) = ax² + bx + c ?", "correct": "f'(x) = 2ax + b", "opts": ["f'(x) = 2ax + b", "f'(x) = ax + b", "f'(x) = 2a"], "exp": "Dérivation d'un polynôme du second degré."},
                    {"enonce": "En quel point la dérivée f'(x) = 2ax + b s'annule-t-elle ?", "correct": "En x = -b / (2a) (au sommet de la parabole)", "opts": ["En x = -b / (2a) (au sommet de la parabole)", "En x = 0", "En x = c/a"], "exp": "Annulation de la dérivée menant à l'extremum."},
                    {"enonce": "Si un polynôme admet deux racines x_1 et x_2, que vaut x_1² + x_2² en fonction de S et P ?", "correct": "S² - 2P", "opts": ["S² - 2P", "S² + 2P", "S - P"], "exp": "Identité remarquable : x_1² + x_2² = (x_1 + x_2)² - 2x_1x_2 = S² - 2P."},
                    {"enonce": "Que vaut l'expression 1/x_1 + 1/x_2 pour des racines non nulles ?", "correct": "S / P (-b / c)", "opts": ["S / P (-b / c)", "P / S", "S - P"], "exp": "1/x_1 + 1/x_2 = (x_1 + x_2) / (x_1x_2) = S/P."},
                    {"enonce": "Combien de racines complexes conjuguées possède un polynôme du second degré à coefficients réels lorsque Δ < 0 ?", "correct": "2 racines complexes conjuguées distinctes", "opts": ["2 racines complexes conjuguées distinctes", "1 racine complexe double", "Aucune racine complexe"], "exp": "Dans C, tout trinôme possède des racines (ici complexes conjuguées)."},
                    {"enonce": "Quelle est l'expression des racines complexes lorsque Δ < 0 pour ax² + bx + c = 0 ?", "correct": "(-b ± i√(-Δ)) / (2a)", "opts": ["(-b ± i√(-Δ)) / (2a)", "(-b ± √Δ) / (2a)", "(-i ± b) / (2a)"], "exp": "Formule générale des racines dans C lorsque le discriminant est négatif."},
                    {"enonce": "Quel est le degré d'un polynôme du second degré ?", "correct": "2", "opts": ["2", "1", "3"], "exp": "Le plus grand exposant de x est 2."},
                    {"enonce": "Si a = 0 dans l'expression ax² + bx + c, que devient le polynôme ?", "correct": "Un polynôme du premier degré (ou affine) : bx + c", "opts": ["Un polynôme du premier degré (ou affine) : bx + c", "Une constante pure", "Il n'existe plus"], "exp": "Si a = 0, le terme quadratique disparaît."},
                    {"enonce": "Quelle est la nature de l'extremum (sommet) de la parabole si a > 0 ?", "correct": "Un minimum global", "opts": ["Un minimum global", "Un maximum global", "Un point d'inflexion"], "exp": "La parabole s'ouvre vers le haut ⇒ minimum."},
                    {"enonce": "Quelle est la nature de l'extremum de la parabole si a < 0 ?", "correct": "Un maximum global", "opts": ["Un maximum global", "Un minimum global", "Un point d'inflexion"], "exp": "La parabole s'ouvre vers le bas ⇒ maximum."},
                    {"enonce": "Comment appelle-t-on l'équation associée ax² + bx + c = 0 ?", "correct": "Une équation du second degré", "opts": ["Une équation du second degré", "Une équation différentielle", "Une identité remarquable"], "exp": "Définition de l'équation quadratique."},
                    {"enonce": "Si le produit des racines P < 0, que peut-on dire des signes de x_1 et x_2 (si elles existent) ?", "correct": "Elles sont de signes contraires", "opts": ["Elles sont de signes contraires", "Elles sont de même signe", "Elles sont nulles"], "exp": "P = c/a < 0 ⇒ x_1 et x_2 ont des signes opposés."},
                    {"enonce": "Si le produit des racines P > 0 et la somme S > 0, les deux racines sont :", "correct": "Strictement positives", "opts": ["Strictement positives", "Strictement négatives", "De signes contraires"], "exp": "Produit positif ⇒ même signe ; Somme positive ⇒ toutes deux positives."},
                    {"enonce": "Si P > 0 et S < 0, les deux racines sont :", "correct": "Strictement négatives", "opts": ["Strictement négatives", "Strictement positives", "Imaginaires"], "exp": "Même signe et somme négative ⇒ toutes deux négatives."},
                    {"enonce": "Quelle est la valeur de la parabole évaluée en x = 0 ?", "correct": "c (ordonnée à l'origine)", "opts": ["c (ordonnée à l'origine)", "0", "a + b"], "exp": "P(0) = a(0)² + b(0) + c = c."},
                    {"enonce": "Si une parabole coupe l'axe des ordonnées en y = 5, que vaut le coefficient c ?", "correct": "c = 5", "opts": ["c = 5", "c = 0", "On ne peut pas savoir"], "exp": "L'ordonnée à l'origine est toujours égale à c."},
                    {"enonce": "Combien d'intersections au maximum une parabole peut-elle avoir avec l'axe des abscisses ?", "correct": "Au plus 2", "opts": ["Au plus 2", "1", "Une infinité"], "exp": "Lié au degré 2 du polynôme."},
                    {"enonce": "Si le discriminant Δ = 0, combien de points d'intersection la parabole a-t-elle avec l'axe (Ox) ?", "correct": "Exactement 1 (le sommet est tangent à l'axe)", "opts": ["Exactement 1 (le sommet est tangent à l'axe)", "0", "2"], "exp": "Racine double ⇒ tangence avec l'axe des abscisses."},
                    {"enonce": "Si Δ > 0, combien de points d'intersection la parabole a-t-elle avec l'axe (Ox) ?", "correct": "Exactement 2", "opts": ["Exactement 2", "1", "0"], "exp": "Deux racines distinctes ⇒ deux intersections."},
                    {"enonce": "Comment appelle-t-on le nombre b² - 4ac ?", "correct": "Le discriminant", "opts": ["Le discriminant", "Le déterminant", "La dérivée"], "exp": "Nom de la quantité Δ."},
                    {"enonce": "Quelle est la forme générale d'une inéquation du second degré ?", "correct": "ax² + bx + c < 0 (ou ≤, >, ≥)", "opts": ["ax² + bx + c < 0 (ou ≤, >, ≥)", "ax + b = 0", "ax³ = 0"], "exp": "Définition d'une inéquation quadratique."},
                    {"enonce": "Pour résoudre une inéquation du second degré, quelle est la première étape indispensable ?", "correct": "Étudier le signe du trinôme (calculer Δ et trouver les racines)", "opts": ["Étudier le signe du trinôme (calculer Δ et trouver les racines)", "Diviser par x", "Calculer l'intégrale"], "exp": "Méthode standard de résolution par le tableau de signes."},
                    {"enonce": "Propriété n°40 : Si a et c sont de signes contraires (ac < 0), que vaut le discriminant Δ si b est réel ?", "correct": "Δ est nécessairement strictement positif", "opts": ["Δ est nécessairement strictement positif", "Δ est négatif", "Δ est nul"], "exp": "Δ = b² - 4ac, si ac < 0, -4ac > 0 donc Δ > b² ≥ 0."},
                    {"enonce": "Propriété n°41 : Si ac < 0, les racines du trinôme sont-elles toujours réelles ?", "correct": "Oui, car Δ > 0", "opts": ["Oui, car Δ > 0", "Non", "Seulement si b = 0"], "exp": "Signes contraires de a et c garantissent l'existence de 2 racines réelles."},
                    {"enonce": "Propriété n°42 : Que vaut la somme des carrés des racines x_1² + x_2² si S = 3 et P = 2 ?", "correct": "5", "opts": ["5", "9", "1"], "exp": "S² - 2P = 3² - 2(2) = 9 - 4 = 5."},
                    {"enonce": "Propriété n°43 : Si un trinôme ax² + bx + c possède une racine évidente x_1 = 1, quelle relation lie les coefficients ?", "correct": "a + b + c = 0", "opts": ["a + b + c = 0", "a - b + c = 0", "b² - 4ac = 0"], "exp": "P(1) = a(1)² + b(1) + c = a + b + c = 0."},
                    {"enonce": "Propriété n°44 : Si un trinôme possède une racine évidente x_1 = -1, quelle relation lie les coefficients ?", "correct": "a - b + c = 0", "opts": ["a - b + c = 0", "a + b + c = 0", "c = 0"], "exp": "P(-1) = a(-1)² + b(-1) + c = a - b + c = 0."},
                    {"enonce": "Propriété n°45 : Si le sommet de la parabole est situé sur l'axe des ordonnées, que vaut le coefficient b ?", "correct": "b = 0", "opts": ["b = 0", "b = 1", "b = c"], "exp": "Abscisse du sommet x_s = -b/(2a) = 0 ⇒ b = 0."},
                    {"enonce": "Propriété n°46 : Si b = 0, la fonction polynôme est dite :", "correct": "Paire (symétrique par rapport à l'axe des ordonnées)", "opts": ["Paire (symétrique par rapport à l'axe des ordonnées)", "Impaire", "Affine"], "exp": "f(-x) = a(-x)² + c = ax² + c = f(x)."},
                    {"enonce": "Propriété n°47 : Quelle est la nature de la fonction f(x) = ax² + c (avec b = 0) sur l'intervalle [0, +∞[ si a > 0 ?", "correct": "Strictement croissante", "opts": ["Strictement croissante", "Strictement décroissante", "Constante"], "exp": "Variations d'une fonction paire de base."},
                    {"enonce": "Propriété n°48 : Si le discriminant Δ est un carré parfait (Δ = k²), les racines x_1 et x_2 sont :", "correct": "Des nombres rationnels (si a, b, c sont rationnels)", "opts": ["Des nombres rationnels (si a, b, c sont rationnels)", "Des irrationnels purs", "Des nombres complexes non réels"], "exp": "√Δ = k est un entier ou un rationnel."},
                    {"enonce": "Propriété n°49 : Si Δ n'est pas un carré parfait, les racines sont :", "correct": "Des nombres réels irrationnels", "opts": ["Des nombres réels irrationnels", "Des nombres entiers", "Des nombres imaginaires"], "exp": "Présence d'une racine carrée irréductible dans l'expression des racines."},
                    {"enonce": "Propriété n°50 : En résumé, l'étude complète d'un polynôme du second degré en Terminale C et D permet de maîtriser :", "correct": "L'optimisation, la factorisation, le signe et la représentation graphique des fonctions quadratiques", "opts": ["L'optimisation, la factorisation, le signe et la représentation graphique des fonctions quadratiques", "Uniquement les additions simples", "La géométrie descriptive statique"], "exp": "Synthèse globale des compétences sur le second degré."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                type_calc = random.choice([
                    "delta", "racines_delta_positif", "somme_produit", "sommet_parabole", 
                    "inequation_signe", "forme_canonique", "fact_trinome", "produit_racines",
                    "valeur_fonction", "axe_symetrie", "ordonnee_origine", "signe_trinome_inf",
                    "nature_extremum", "racine_evidente_1", "racine_evidente_moins_1"
                ])
                
                if type_calc == "delta":
                    a_v = random.choice([1, 2, -1, 3])
                    b_v = random.randint(-8, 8)
                    c_v = random.randint(-6, 6)
                    delta_val = b_v**2 - 4 * a_v * c_v
                    enonce = f"Calculez le discriminant Δ du polynôme P(x) = {a_v if a_v != 1 else ''}x² {'+' if b_v >= 0 else '-' } {abs(b_v)}x {'+' if c_v >= 0 else '-' } {abs(c_v)}."
                    correct = f"{delta_val}"
                    opts = [f"{delta_val}", f"{delta_val + 4}", f"{delta_val - 2}", f"{-delta_val}"]
                    exp = f"Δ = b² - 4ac = ({b_v})² - 4({a_v})({c_v}) = {b_v**2} - {4*a_v*c_v} = {delta_val}."
                
                elif type_calc == "racines_delta_positif":
                    x1 = random.randint(-4, 4)
                    x2 = random.randint(-4, 4)
                    while x1 == x2:
                        x2 = random.randint(-4, 4)
                    b_v = -(x1 + x2)
                    c_v = x1 * x2
                    enonce = f"Trouvez les racines distinctes du polynôme P(x) = x² {'+' if b_v >= 0 else '-' } {abs(b_v)}x {'+' if c_v >= 0 else '-' } {abs(c_v)}."
                    racines_str = f"{min(x1, x2)} et {max(x1, x2)}"
                    correct = racines_str
                    opts = [racines_str, f"{-min(x1, x2)} et {-max(x1, x2)}", f"{x1+1} et {x2-1}", "Pas de racine"]
                    exp = f"Δ > 0. Les racines sont x_1 = {x1} et x_2 = {x2}."
                
                elif type_calc == "somme_produit":
                    a_s = random.choice([1, 2, 3])
                    b_s = random.randint(-10, 10)
                    c_s = random.randint(-8, 8)
                    somme_val = -b_s / a_s
                    correct = f"{somme_val if somme_val != int(somme_val) else int(somme_val)}"
                    enonce = f"Soit le trinôme P(x) = {a_s}x² {'+' if b_s >= 0 else '-' } {abs(b_s)}x {'+' if c_s >= 0 else '-' } {abs(c_s)}. Quelle est la somme S de ses racines ?"
                    opts = [correct, f"{c_s / a_s}", f"{-c_s / a_s}", f"{b_s / a_s}"]
                    exp = f"La somme des racines est S = -b / a = -({b_s}) / {a_s} = {somme_val}."
                
                elif type_calc == "sommet_parabole":
                    a_so = 1
                    b_so = random.choice([-6, -4, -2, 2, 4, 6])
                    c_so = random.randint(-5, 5)
                    xs = -b_so / (2 * a_so)
                    ys = -(b_so**2 - 4*a_so*c_so) / (4 * a_so)
                    enonce = f"Quelles sont les coordonnées du sommet S de la parabole y = x² {'+' if b_so >= 0 else '-' } {abs(b_so)}x {'+' if c_so >= 0 else '-' } {abs(c_so)} ?"
                    correct = f"({xs} ; {ys})"
                    opts = [f"({xs} ; {ys})", f"({ys} ; {xs})", f"(0 ; {c_so})", f"({-xs} ; {ys})"]
                    exp = f"x_s = -b/(2a) = {xs}, y_s = f(x_s) = {ys}."
                
                elif type_calc == "inequation_signe":
                    rac = random.choice([2, 3, 4, 5])
                    enonce = f"Quel est l'ensemble des solutions de l'inéquation x² - {rac**2} ≥ 0 dans R ?"
                    correct = f"] -∞, -{rac} ] ∪ [ {rac}, +∞ ["
                    opts = [f"] -∞, -{rac} ] ∪ [ {rac}, +∞ [", f"[ -{rac}, {rac} ]", "R", "Ensemble vide"]
                    exp = f"Le trinôme x² - {rac**2} est positif à l'extérieur de ses racines -{rac} et {rac}."
                
                elif type_calc == "forme_canonique":
                    b_fc = random.choice([2, 4, 6])
                    c_fc = random.randint(1, 5)
                    alpha = b_fc // 2
                    beta = c_fc - alpha**2
                    enonce = f"Donnez la constante β de la forme canonique (x + {alpha})² + β du polynôme x² + {b_fc}x + {c_fc}."
                    correct = f"{beta}"
                    opts = [f"{beta}", f"{beta + 2}", f"{-beta}", f"{alpha}"]
                    exp = f"Forme canonique : (x + {alpha})² + ({beta}). β vaut {beta}."
                
                elif type_calc == "fact_trinome":
                    r = random.randint(1, 5)
                    enonce = f"Quel est le discriminant Δ du polynôme x² - {2*r}x + {r**2} ?"
                    correct = "0"
                    opts = ["0", f"{r}", f"{4*r}", "1"]
                    exp = f"Δ = ({ -2*r })² - 4(1)({ r**2 }) = 0 (racine double r = {r})."
                
                elif type_calc == "produit_racines":
                    a_p = random.choice([1, 2])
                    b_p = random.randint(-6, 6)
                    c_p = random.randint(-8, 8)
                    prod_val = c_p / a_p
                    correct = f"{prod_val if prod_val != int(prod_val) else int(prod_val)}"
                    enonce = f"Quel est le produit P des racines du polynôme {a_p if a_p != 1 else ''}x² {'+' if b_p >= 0 else '-' } {abs(b_p)}x {'+' if c_p >= 0 else '-' } {abs(c_p)} ?"
                    opts = [correct, f"{-b_p / a_p}", f"{b_p}", f"{-c_p}"]
                    exp = f"Le produit des racines est P = c / a = {c_p} / {a_p} = {prod_val}."
                
                elif type_calc == "valeur_fonction":
                    xv = random.randint(-3, 3)
                    av = random.choice([1, 2])
                    bv = random.randint(-4, 4)
                    cv = random.randint(-5, 5)
                    res_val = av * (xv**2) + bv * xv + cv
                    enonce = f"Calculez la valeur de P({xv}) pour le polynôme P(x) = {av if av != 1 else ''}x² {'+' if bv >= 0 else '-' } {abs(bv)}x {'+' if cv >= 0 else '-' } {abs(cv)}."
                    correct = f"{res_val}"
                    opts = [f"{res_val}", f"{res_val + 3}", f"{res_val - 2}", f"{-res_val}"]
                    exp = f"P({xv}) = {av}({xv})² + ({bv})({xv}) + ({cv}) = {res_val}."
                
                elif type_calc == "axe_symetrie":
                    ba = random.choice([-6, -4, -2, 2, 4, 6])
                    aa = random.choice([1, 2])
                    res_axe = -ba / (2 * aa)
                    correct = f"x = {res_axe if res_axe != int(res_axe) else int(res_axe)}"
                    enonce = f"Quelle est l'équation de l'axe de symétrie de la parabole y = {aa if aa != 1 else ''}x² {'+' if ba >= 0 else '-' } {abs(ba)}x + 1 ?"
                    opts = [correct, f"x = {ba}", f"y = {res_axe}", "x = 0"]
                    exp = f"L'axe de symétrie a pour équation x = -b / (2a) = -({ba}) / (2 · {aa}) = {res_axe}."
                
                elif type_calc == "ordonnee_origine":
                    co = random.randint(-9, 9)
                    enonce = f"Quelle est l'ordonnée à l'origine de la parabole d'équation y = 3x² - 5x {'+' if co >= 0 else '-' } {abs(co)} ?"
                    correct = f"{co}"
                    opts = [f"{co}", f"{-co}", "0", "3"]
                    exp = f"L'ordonnée à l'origine est la valeur de la fonction en x = 0, soit c = {co}."
                
                elif type_calc == "signe_trinome_inf":
                    rac2 = random.choice([1, 2, 3])
                    enonce = f"Quel est l'ensemble des solutions de l'inéquation x² - {rac2**2} < 0 dans R ?"
                    correct = f"] -{rac2}, {rac2} ["
                    opts = [f"] -{rac2}, {rac2} [", f"] -∞, -{rac2} [ ∪ ] {rac2}, +∞ [", "R", "∅"]
                    exp = f"Le trinôme est strictement négatif à l'intérieur de ses racines -{rac2} et {rac2}."
                
                elif type_calc == "nature_extremum":
                    sign_a = random.choice([1, -1])
                    nature = "un minimum" if sign_a > 0 else "un maximum"
                    correct = nature
                    opts = [nature, "un point d'inflexion", "une constante", "aucune de ces réponses"]
                    exp = f"Puisque le coefficient a = {sign_a} est {'positif' if sign_a > 0 else 'négatif'}, la parabole admet {nature}."
                
                elif type_calc == "racine_evidente_1":
                    bb = random.randint(-5, 5)
                    cc = - (1 + bb) # a=1, donc 1 + bb + cc = 0 => cc = -(1+bb)
                    enonce = f"Quelle est une racine évidente évidente du polynôme x² {'+' if bb >= 0 else '-' } {abs(bb)}x {'+' if cc >= 0 else '-' } {abs(cc)} sachant que la somme des coefficients vaut 0 ?"
                    correct = "1"
                    opts = ["1", "-1", "0", "2"]
                    exp = "Puisque a + b + c = 0, 1 est racine évidente du polynôme."
                
                else:
                    bb2 = random.randint(-5, 5)
                    cc2 = bb2 - 1 # a=1, b=bb2, c=cc2 tel que 1 - bb2 + cc2 = 0
                    enonce = f"Quelle est une racine évidente du polynôme x² {'+' if bb2 >= 0 else '-' } {abs(bb2)}x {'+' if cc2 >= 0 else '-' } {abs(cc2)} sachant que a - b + c = 0 ?"
                    correct = "-1"
                    opts = ["-1", "1", "0", "-2"]
                    exp = "Puisque a - b + c = 0, -1 est racine évidente du polynôme."

            elif variante == "V3":
                banque_v3 = [
                    {"enonce": "Comment démontre-t-on la formule de la forme canonique d'un polynôme du second degré ?", "correct": "Par factorisation par a puis mise sous forme de binôme remarquable (identité remarquable)", "opts": ["Par factorisation par a puis mise sous forme de binôme remarquable (identité remarquable)", "Par intégration", "Par récurrence simple"], "exp": "ax² + bx + c = a(x² + b/a x + c/a) = a[(x + b/(2a))² - b²/(4a²) + c/a]."},
                    {"enonce": "Quel est le lien fondamental entre le signe de a et la convexité de la fonction polynôme du second degré ?", "correct": "f''(x) = 2a, donc si a > 0 la fonction est strictement convexe", "opts": ["f''(x) = 2a, donc si a > 0 la fonction est strictement convexe", "f''(x) est toujours nulle", "La convexité ne dépend pas de a"], "exp": "La dérivée seconde est constante et égale à 2a."},
                    {"enonce": "Soit un polynôme P(x) = ax² + bx + c. Quelle est la condition nécessaire et suffisante pour que P(x) soit positif pour tout x réel ?", "correct": "a > 0 et Δ ≤ 0", "opts": ["a > 0 et Δ ≤ 0", "a < 0 et Δ > 0", "Δ = 0 seulement"], "exp": "Signe constant de a et absence de racines réelles distinctes."},
                    {"enonce": "Comment s'exprime la décomposition en facteurs irréductibles dans R d'un trinôme lorsque Δ < 0 ?", "correct": "Il n'est pas factorisable en produit de polynômes du premier degré dans R (il est irréductible)", "opts": ["Il n'est pas factorisable en produit de polynômes du premier degré dans R (il est irréductible)", "a(x - i)(x + i)", "a(x² + 1)"], "exp": "Pas de racines réelles ⇒ irréductible dans R[X]."},
                    {"enonce": "Si un polynôme du second degré admet deux racines x_1 et x_2, que vaut l'expression (x_1 - x_2)² en fonction de Δ et a ?", "correct": "Δ / a²", "opts": ["Δ / a²", "√Δ / a", "-Δ / a"], "exp": "(x_1 - x_2)² = (x_1 + x_2)² - 4x_1x_2 = S² - 4P = (b/a)² - 4c/a = (b² - 4ac)/a² = Δ/a²."},
                    {"enonce": "Quel est l'impact d'une translation de vecteur v sur l'expression algébrique d'un polynôme du second degré ?", "correct": "Elle modifie les coefficients b et c mais conserve le coefficient dominant a", "opts": ["Elle modifie les coefficients b et c mais conserve le coefficient dominant a", "Elle change la valeur de a", "Elle annule le discriminant"], "exp": "Invariance du coefficient dominant a par translation."},
                    {"enonce": "Comment utilise-t-on le discriminant pour résoudre une équation bicarrée de la forme ax⁴ + bx² + c = 0 ?", "correct": "En posant le changement de variable X = x² pour se ramener à un trinôme du second degré aX² + bX + c = 0", "opts": ["En posant le changement de variable X = x² pour se ramener à un trinôme du second degré aX² + bX + c = 0", "En factorisant par x³", "En calculant une dérivée tierce"], "exp": "Technique classique de substitution bicarrée."},
                    {"enonce": "Si les racines x_1 et x_2 d'un trinôme sont inverses l'une de l'autre (x_2 = 1/x_1), quelle relation simple lie a et c ?", "correct": "a = c (car P = c/a = 1)", "opts": ["a = c (car P = c/a = 1)", "a = -c", "b = 0"], "exp": "Produit des racines P = x_1 · (1/x_1) = 1 ⇒ c/a = 1 ⇒ a = c."},
                    {"enonce": "Si les racines d'un trinôme sont opposées (x_2 = -x_1), quelle relation simple lie les coefficients ?", "correct": "b = 0 (car S = -b/a = 0)", "opts": ["b = 0 (car S = -b/a = 0)", "a = c", "Δ < 0"], "exp": "Somme des racines S = x_1 - x_1 = 0 ⇒ -b/a = 0 ⇒ b = 0."},
                    {"enonce": "Quelle est la signification géométrique de la condition Δ = 0 pour deux paraboles ou une parabole et une droite ?", "correct": "Il y a un unique point de contact (tangence)", "opts": ["Il y a un unique point de contact (tangence)", "Elles sont confondues", "Pas d'intersection"], "exp": "Racine double de l'équation d'intersection = tangence."},
                    {"enonce": "Comment détermine-t-on l'équation d'une parabole connaissant son sommet S(α, β) et un point A de la courbe ?", "correct": "Sous la forme y = a(x - α)² + β en injectant les coordonnées de A pour trouver a", "opts": ["Sous la forme y = a(x - α)² + β en injectant les coordonnées de A pour trouver a", "Par dérivation directe", "En posant a = 1"], "exp": "Utilisation de la forme canonique avec le sommet."},
                    {"enonce": "Quel est le domaine de définition d'une fonction rationnelle comportant un trinôme du second degré au dénominateur ?", "correct": "R privé des racines réelles du trinôme (là où le dénominateur s'annule)", "opts": ["R privé des racines réelles du trinôme (là où le dénominateur s'annule)", "Tout R", "L'intervalle [0, +∞["], "exp": "Interdiction de la division par zéro."},
                    {"enonce": "Comment étudier le signe d'une expression du type P(x) / Q(x) où P et Q sont des polynômes du second degré ?", "correct": "Par un tableau de signes combinant les racines de P et de Q (en excluant les valeurs annulant Q)", "opts": ["Par un tableau de signes combinant les racines de P et de Q (en excluant les valeurs annulant Q)", "En additionnant P et Q", "Par un produit scalaire"], "exp": "Règle des signes d'un quotient."},
                    {"enonce": "Si un polynôme du second degré est minoré sur R, que vaut son minimum ?", "correct": "L'ordonnée de son sommet y_s = -Δ / (4a) (lorsque a > 0)", "opts": ["L'ordonnée de son sommet y_s = -Δ / (4a) (lorsque a > 0)", "0", "+∞"], "exp": "Le sommet atteint le minimum absolu si a > 0."},
                    {"enonce": "Si un polynôme est majoré sur R, que vaut son maximum ?", "correct": "L'ordonnée de son sommet y_s = -Δ / (4a) (lorsque a < 0)", "opts": ["L'ordonnée de son sommet y_s = -Δ / (4a) (lorsque a < 0)", "-∞", "c"], "exp": "Le sommet atteint le maximum absolu si a < 0."},
                    {"enonce": "Quelle est la nature de l'ensemble des solutions d'une inéquation du type ax² + bx + c < 0 lorsque a > 0 et Δ > 0 ?", "correct": "L'intervalle ouvert ]x_1, x_2[ entre les deux racines", "opts": ["L'intervalle ouvert ]x_1, x_2[ entre les deux racines", "R", "Ensemble vide"], "exp": "Le trinôme est négatif à l'intérieur de ses racines si a > 0."},
                    {"enonce": "Quelle est la nature de l'ensemble des solutions de ax² + bx + c > 0 lorsque a > 0 et Δ > 0 ?", "correct": "La réunion d'intervalles ]-∞, x_1[ ∪ ]x_2, +∞[", "opts": ["La réunion d'intervalles ]-∞, x_1[ ∪ ]x_2, +∞[", "L'intervalle ]x_1, x_2[", "Un point unique"], "exp": "Le trinôme est positif à l'extérieur de ses racines si a > 0."},
                    {"enonce": "Comment procède-t-on pour encadrer ou démontrer une inégalité quadratique pour tout x réel ?", "correct": "En étudiant le signe de son discriminant ou en la mettant sous forme canonique (somme de carrés)", "opts": ["En étudiant le signe de son discriminant ou en la mettant sous forme canonique (somme de carrés)", "En traçant une droite", "Par récurrence"], "exp": "Mise sous forme canonique a(x - α)² + β ≥ 0."},
                    {"enonce": "Quel théorème garantit qu'une fonction polynôme du second degré est continue et dérivable sur R ?", "correct": "Les théorèmes généraux sur les fonctions polynômes (dérivables à tout ordre sur R)", "opts": ["Les théorèmes généraux sur les fonctions polynômes (dérivables à tout ordre sur R)", "Le théorème des valeurs intermédiaires uniquement", "Aucun théorème"], "exp": "Propriété de régularité des fonctions polynômes."},
                    {"enonce": "En synthèse, l'étude approfondie des polynômes du second degré en Terminale C et D constitue le fondement de :", "correct": "L'analyse mathématique, de l'étude des extremums et de la résolution des équations polynomiales de degré supérieur", "opts": ["L'analyse mathématique, de l'étude des extremums et de la résolution des équations polynomiales de degré supérieur", "L'arithmétique pure sans application", "La géométrie descriptive statique"], "exp": "Rôle central du second degré dans les programmes scientifiques."},
                    {"enonce": "Que représente géométriquement le paramètre c dans l'expression d'une parabole y = ax² + bx + c ?", "correct": "L'ordonnée du point d'intersection de la parabole avec l'axe des ordonnées", "opts": ["L'ordonnée du point d'intersection de la parabole avec l'axe des ordonnées", "Le sommet de la parabole", "La pente de la tangente"], "exp": "P(0) = c."},
                    {"enonce": "Quelle est la condition pour qu'une parabole soit entièrement située au-dessus de l'axe des abscisses ?", "correct": "a > 0 et Δ < 0", "opts": ["a > 0 et Δ < 0", "a < 0 et Δ > 0", "Δ = 0"], "exp": "Pas d'intersection et branches vers le haut."},
                    {"enonce": "Comment factorise-t-on un polynôme ax² + bx + c lorsque son discriminant Δ est strictement positif ?", "correct": "a · (x - x_1)(x - x_2) où x_1 et x_2 sont les deux racines distinctes", "opts": ["a · (x - x_1)(x - x_2) où x_1 et x_2 sont les deux racines distinctes", "a · (x - x_0)²", "Impossible dans R"], "exp": "Forme factorisée standard du trinôme."},
                    {"enonce": "Comment factorise-t-on un polynôme ax² + bx + c lorsque son discriminant Δ est nul ?", "correct": "a · (x - x_0)² où x_0 est la racine double", "opts": ["a · (x - x_0)² où x_0 est la racine double", "a · (x - x_1)(x - x_2)", "Non factorisable"], "exp": "Forme factorisée avec racine double."},
                    {"enonce": "Quelle est l'abscisse du sommet de la parabole en fonction des racines x_1 et x_2 lorsque Δ > 0 ?", "correct": "x_s = (x_1 + x_2) / 2 (le milieu des racines)", "opts": ["x_s = (x_1 + x_2) / 2 (le milieu des racines)", "x_s = x_1 · x_2", "x_s = 0"], "exp": "Par symétrie de la parabole, l'axe passe par le milieu des deux intersections avec l'axe (Ox)."},
                    {"enonce": "Si une équation du second degré admet une racine évidente x_1 = 0, que vaut nécessairement le coefficient c ?", "correct": "c = 0", "opts": ["c = 0", "a = 0", "b = 0"], "exp": "P(0) = a(0)² + b(0) + c = 0 ⇒ c = 0."},
                    {"enonce": "Que devient l'équation ax² + bx + c = 0 si c = 0 ?", "correct": "Une équation factorisable par x : x(ax + b) = 0", "opts": ["Une équation factorisable par x : x(ax + b) = 0", "Une équation impossible", "Une constante"], "exp": "Mise en évidence de x."},
                    {"enonce": "Quelle est la nature de l'ensemble des solutions de ax² + bx + c < 0 lorsque a > 0 et Δ = 0 ?", "correct": "L'ensemble vide ∅ (le trinôme s'annule en x_0 mais est positif ailleurs)", "opts": ["L'ensemble vide ∅ (le trinôme s'annule en x_0 mais est positif ailleurs)", "R", "{x_0}"], "exp": "Un carré est toujours positif ou nul."},
                    {"enonce": "Quelle est l'allure de la tangente à la parabole en son sommet S ?", "correct": "Elle est horizontale (de pente nulle)", "opts": ["Elle est horizontale (de pente nulle)", "Elle est verticale", "Elle est oblique"], "exp": "La dérivée s'annule au sommet, la pente est donc nulle."},
                    {"enonce": "Si l'on multiplie tous les coefficients d'un polynôme du second degré par un nombre réel k non nul (P'(x) = kP(x)), que deviennent ses racines ?", "correct": "Elles restent rigoureusement inchangées", "opts": ["Elles restent rigoureusement inchangées", "Elles sont multipliées par k", "Elles sont inversées"], "exp": "Multiplier par une constante non nulle ne change pas les zéros du polynôme."},
                    {"enonce": "Comment appelle-t-on le rapport b / a dans un polynôme normalisé x² + (b/a)x + (c/a) = 0 par rapport aux racines ?", "correct": "L'opposé de la somme des racines (-S)", "opts": ["L'opposé de la somme des racines (-S)", "Le produit", "Le discriminant"], "exp": "Coefficient de x dans la forme normalisée."},
                    {"enonce": "Si un trinôme du second degré est toujours strictement négatif sur R, quel est le signe de son coefficient a ?", "correct": "a < 0 et Δ < 0", "opts": ["a < 0 et Δ < 0", "a > 0 et Δ < 0", "a < 0 et Δ > 0"], "exp": "Parabole tournée vers le bas et sans racine réelle."},
                    {"enonce": "Quelle est la valeur de la somme des inverses des racines 1/x_1 + 1/x_2 exprimée avec S et P ?", "correct": "S / P", "opts": ["S / P", "P / S", "S · P"], "exp": "1/x_1 + 1/x_2 = (x_1 + x_2)/(x_1x_2) = S/P."},
                    {"enonce": "Si l'on connait la somme S et le produit P de deux nombres, de quel polynôme sont-ils les racines ?", "correct": "X² - SX + P = 0", "opts": ["X² - SX + P = 0", "X² + SX + P = 0", "X² - SX - P = 0"], "exp": "Réciproque des relations de Viète."},
                    {"enonce": "Quelle est la condition pour que les racines d'un trinôme soient de signes contraires ?", "correct": "P < 0 (c/a < 0), ce qui implique que Δ > 0", "opts": ["P < 0 (c/a < 0), ce qui implique que Δ > 0", "Δ < 0", "S > 0 seulement"], "exp": "Produit négatif ⇒ signes opposés et discriminant forcément positif."},
                    {"enonce": "Si b² - 4ac = 0, que peut-on dire de la parabole par rapport à l'axe des abscisses ?", "correct": "Elle est tangente à l'axe (Ox) en son sommet", "opts": ["Elle est tangente à l'axe (Ox) en son sommet", "Elle ne le coupe pas", "Elle le coupe en deux points"], "exp": "Définition graphique de la racine double."},
                    {"enonce": "Comment se comporte la fonction f(x) = ax² + bx + c lorsque x tend vers +∞ (si a > 0) ?", "correct": "Elle tend vers +∞", "opts": ["Elle tend vers +∞", "Elle tend vers -∞", "Elle converge vers c"], "exp": "Comportement asymptotique dominant en x²."},
                    {"enonce": "Comment se comporte la fonction f(x) = ax² + bx + c lorsque x tend vers -∞ (si a < 0) ?", "correct": "Elle tend vers -∞", "opts": ["Elle tend vers -∞", "Elle tend vers +∞", "Elle s'annule"], "exp": "Comportement en -∞ pour a négatif."},
                    {"enonce": "Quelle est l'écriture de la forme canonique si le coefficient a = 1 ?", "correct": "(x + b/2)² - (b² - 4c)/4", "opts": ["(x + b/2)² - (b² - 4c)/4", "x² + b", "(x - a)²"], "exp": "Forme canonique simplifiée pour a = 1."},
                    {"enonce": "Quel est le nombre de solutions réelles de l'équation ax² + bx + c = 0 lorsque Δ = 0 ?", "correct": "Une unique solution réelle (racine double)", "opts": ["Une unique solution réelle (racine double)", "Deux solutions distinctes", "Zéro solution"], "exp": "Cas de la racine double unique x_0."},
                    {"enonce": "Si l'on trace deux paraboles d'équations y = ax² et y = ax² + k, quel est le lien géométrique entre elles ?", "correct": "Elles sont déduites l'une de l'autre par une translation verticale de vecteur k·j", "opts": ["Elles sont déduites l'une de l'autre par une translation verticale de vecteur k·j", "Elles sont identiques", "Elles sont perpendiculaires"], "exp": "Ajout d'une constante k = translation verticale."},
                    {"enonce": "Dans l'étude de signe d'un trinôme avec Δ > 0, entre les deux racines, le signe est :", "correct": "Le signe opposé à celui de a", "opts": ["Le signe opposé à celui de a", "Le signe de a", "Toujours positif"], "exp": "Règle de l'intérieur des racines."},
                    {"enonce": "À l'extérieur des racines (pour Δ > 0), le signe du trinôme est :", "correct": "Le signe de a", "opts": ["Le signe de a", "Le signe opposé à a", "Toujours négatif"], "exp": "Règle de l'extérieur des racines."},
                    {"enonce": "Si une inéquation du type ax² + bx + c ≤ 0 admet un discriminant nul et a > 0, quel est l'ensemble des solutions ?", "correct": "L'ensemble réduit à la racine double : {-b / (2a)}", "opts": ["L'ensemble réduit à la racine double : {-b / (2a)}", "R", "∅"], "exp": "Le trinôme est nul uniquement en x_0 et strictement positif ailleurs."},
                    {"enonce": "Quel est le nom de la propriété mathématique qui relie les racines et les coefficients d'un polynôme ?", "correct": "Les relations de Viète", "opts": ["Les relations de Viète", "Le théorème de Thalès", "La formule de Taylor"], "exp": "Nom des formules donnant S et P."},
                    {"enonce": "Si l'on effectue un changement d'origine par translation pour placer l'origine au sommet de la parabole, quelle équation prend le trinôme ?", "correct": "Y = aX² (forme canonique épurée)", "opts": ["Y = aX² (forme canonique épurée)", "Y = aX + b", "Y = X² + X"], "exp": "En posant X = x - x_s et Y = y - y_s."},
                    {"enonce": "Pourquoi l'étude des polynômes du second degré est-elle si importante en physique et en analyse ?", "correct": "Parce qu'elle permet de modéliser les mouvements paraboliques (chute libre) et d'approcher les fonctions au voisinage d'un extremum", "opts": ["Parce qu'elle permet de modéliser les mouvements paraboliques (chute libre) et d'approcher les fonctions au voisinage d'un extremum", "Uniquement pour le calcul mental", "Parce qu'elle n'a aucune application"], "exp": "Applications fondamentales en mécanique et optimisation."},
                    {"enonce": "Si un polynôme possède des coefficients complexes, la formule du discriminant Δ = b² - 4ac reste-t-elle valable pour trouver les racines ?", "correct": "Oui, en utilisant l'extraction de racine carrée complexe", "opts": ["Oui, en utilisant l'extraction de racine carrée complexe", "Non, elle devient totalement fausse", "Seulement si b = 0"], "exp": "Validité générale de la formule quadratique dans C."},
                    {"enonce": "Quel est le degré de la dérivée d'un polynôme du second degré ?", "correct": "1 (c'est une fonction affine)", "opts": ["1 (c'est une fonction affine)", "2", "0 (constante)"], "exp": "La dérivée de ax² + bx + c est 2ax + b (degré 1)."},
                    {"enonce": "En conclusion, maîtriser la résolution complète du second degré en Terminale C et D garantit :", "correct": "Une aisance indispensable pour aborder l'analyse supérieure, les équations différentielles et l'étude des fonctions", "opts": ["Une aisance indispensable pour aborder l'analyse supérieure, les équations différentielles et l'étude des fonctions", "La mémorisation de formules inutiles", "Une simplification excessive des mathématiques"], "exp": "Synthèse de l'importance du chapitre."}
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

# 39. DÉRIVATION FONCTIONNELLE
        elif chapitre_cible == "Dérivation fonctionnelle":
            a_d = random.randint(1, 6)
            n_d = random.randint(2, 5)

            def _puiss(k):
                return "x" if k == 1 else f"x^{k}"

            if variante == "V1":
                enonce = f"Calculez la dérivée de f(x) = {a_d}{_puiss(n_d)}."
                correct = f"{a_d * n_d}{_puiss(n_d - 1)}"
                opts = [correct, f"{a_d}{_puiss(n_d - 1)}", f"{a_d * n_d}{_puiss(n_d)}",
                        f"{a_d * (n_d + 1)}{_puiss(n_d + 1)}"]
                exp = f"(a·x^n)' = a·n·x^(n-1), donc f'(x) = {correct}."
            elif variante == "V2":
                b_d = random.randint(-5, 5)
                c_d = random.randint(-5, 5)
                x0 = random.randint(1, 5)
                valeur = 2 * a_d * x0 + b_d
                enonce = f"Soit f(x) = {a_d}x² {b_d:+d}x {c_d:+d}. Calculez f'({x0})."
                correct = str(valeur)
                opts = [correct, str(valeur + a_d), str(2 * a_d * x0), str(a_d * x0 ** 2 + b_d * x0 + c_d)]
                exp = f"f'(x) = {2 * a_d}x {b_d:+d}, donc f'({x0}) = {valeur}."
            else:
                banque_d = [
                    ("Quelle est la dérivée du produit u·v ?", "u'v + uv'", ["u'v + uv'", "u'v'", "u'v - uv'"],
                     "Formule de dérivation d'un produit."),
                    ("Quelle est la dérivée du quotient u/v (v ≠ 0) ?", "(u'v - uv') / v²",
                     ["(u'v - uv') / v²", "u'/v'", "(u'v + uv') / v²"], "Formule de dérivation d'un quotient."),
                    ("Quelle est la dérivée de e^x ?", "e^x", ["e^x", "x·e^(x-1)", "1"],
                     "La fonction exponentielle est sa propre dérivée."),
                    ("Quelle est la dérivée de ln(x) sur ]0 ; +∞[ ?", "1/x", ["1/x", "ln(x)/x", "x"],
                     "Dérivée usuelle du logarithme népérien."),
                    ("Que représente f'(a) géométriquement ?", "La pente de la tangente à la courbe en a",
                     ["La pente de la tangente à la courbe en a", "L'aire sous la courbe", "L'ordonnée à l'origine"],
                     "Interprétation géométrique du nombre dérivé."),
                    ("Si f'(x) > 0 sur un intervalle, alors f est :", "Strictement croissante",
                     ["Strictement croissante", "Strictement décroissante", "Constante"],
                     "Le signe de la dérivée donne le sens de variation."),
                ]
                enonce, correct, opts, exp = random.choice(banque_d)

# =======================================
        # 40. NOMBRES COMPLEXES
# =======================================
        elif chapitre_cible == "Nombres complexes":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "Quelle est la valeur mathématique rigoureuse de la puissance imaginaire i² ?", "correct": "-1", "opts": ["-1", "1", "0"], "exp": "Définition fondamentale de l'unité imaginaire i."},
                    {"enonce": "Soit z = a + ib un nombre complexe. Comment appelle-t-on a ?", "correct": "La partie réelle de z", "opts": ["La partie réelle de z", "La partie imaginaire", "Le module"], "exp": "Re(z) = a."},
                    {"enonce": "Soit z = a + ib un nombre complexe. Comment appelle-t-on b ?", "correct": "La partie imaginaire de z", "opts": ["La partie imaginaire de z", "La partie réelle", "L'argument"], "exp": "Im(z) = b."},
                    {"enonce": "Quel est le module du nombre complexe z = 3 + 4i ?", "correct": "5", "opts": ["5", "7", "25"], "exp": "|z| = √(3² + 4²) = √25 = 5."},
                    {"enonce": "Quel est le conjugué du nombre complexe z = x + iy ?", "correct": "z̄ = x - iy", "opts": ["z̄ = x - iy", "z̄ = -x + iy", "z̄ = x + iy"], "exp": "Le conjugué change le signe de la partie imaginaire."},
                    {"enonce": "Quel est le produit d'un nombre complexe z par son conjugué z̄ (z · z̄) ?", "correct": "Le carré de son module (|z|²)", "opts": ["Le carré de son module (|z|²)", "Son module simple", "Toujours un nombre imaginaire pur"], "exp": "z · z̄ = a² + b² = |z|²."},
                    {"enonce": "Quelle est la forme exponentielle d'un nombre complexe de module r et d'argument θ ?", "correct": "z = r · e^(iθ)", "opts": ["z = r · e^(iθ)", "z = r · cos(θ)", "z = e^(r·θ)"], "exp": "Forme polaire / exponentielle d'Euler."},
                    {"enonce": "Que énonce la formule d'Euler pour cos(θ) en fonction de l'exponentielle imaginaire ?", "correct": "cos(θ) = (e^(iθ) + e^(-iθ)) / 2", "opts": ["cos(θ) = (e^(iθ) + e^(-iθ)) / 2", "cos(θ) = (e^(iθ) - e^(-iθ)) / (2i)", "cos(θ) = e^(iθ)"], "exp": "Relation fondamentale d'Euler."},
                    {"enonce": "Que énonce la formule d'Euler pour sin(θ) ?", "correct": "sin(θ) = (e^(iθ) - e^(-iθ)) / (2i)", "opts": ["sin(θ) = (e^(iθ) - e^(-iθ)) / (2i)", "sin(θ) = (e^(iθ) + e^(-iθ)) / 2", "sin(θ) = i · e^(iθ)"], "exp": "Expression sinusoïdale complexe."},
                    {"enonce": "Que stipule la formule de Moivre pour (cos(θ) + i sin(θ))^n ?", "correct": "cos(nθ) + i sin(nθ)", "opts": ["cos(nθ) + i sin(nθ)", "n · cos(θ) + i sin(θ)", "cos(n + θ)"], "exp": "(e^(iθ))^n = e^(i nθ)."},
                    {"enonce": "Quel est l'argument principal d'un nombre complexe strictement positif sur l'axe réel ?", "correct": "0 (ou 0 mod 2π)", "opts": ["0", "π / 2", "π"], "exp": "L'angle avec l'axe réel positif est nul."},
                    {"enonce": "Quel est l'argument principal d'un nombre imaginaire pur strictement positif i ?", "correct": "π / 2", "opts": ["π / 2", "0", "π"], "exp": "Situé sur la partie positive de l'axe imaginaire."},
                    {"enonce": "Le module d'un produit de deux nombres complexes z1 et z2 vérifie :", "correct": "|z1 · z2| = |z1| · |z2|", "opts": ["|z1 · z2| = |z1| · |z2|", "|z1 · z2| = |z1| + |z2|", "|z1 · z2| = |z1| / |z2|"], "exp": "Multiplicativité du module."},
                    {"enonce": "L'argument d'un produit de deux nombres complexes z1 et z2 vérifie :", "correct": "arg(z1 · z2) = arg(z1) + arg(z2) [2π]", "opts": ["arg(z1 · z2) = arg(z1) + arg(z2) [2π]", "arg(z1 · z2) = arg(z1) · arg(z2)", "arg(z1 · z2) = arg(z1) - arg(z2)"], "exp": "Additivité des arguments."},
                    {"enonce": "Quel est le module de l'unité imaginaire i ?", "correct": "1", "opts": ["1", "i", "-1"], "exp": "|i| = √(0² + 1²) = 1."},
                    {"enonce": "Quelle est la solution de l'équation complexe z² + 1 = 0 dans C ?", "correct": "z = i ou z = -i", "opts": ["z = i ou z = -i", "z = 1 ou z = -1", "Pas de solution"], "exp": "z² = -1 ⇒ z = ±i."},
                    {"enonce": "Géométriquement, que représente le module de la différence de deux affixes |z_B - z_A| ?", "correct": "La distance entre les points A et B dans le plan complexe", "opts": ["La distance entre les points A et B dans le plan complexe", "L'aire du triangle", "La pente de la droite AB"], "exp": "Définition géométrique de la distance inter-affixes."},
                    {"enonce": "Géométriquement, que représente l'argument de (z_C - z_A) / (z_B - z_A) ?", "correct": "L'angle orienté (AB, AC)", "opts": ["L'angle orienté (AB, AC)", "La longueur BC", "Le milieu de AC"], "exp": "Interprétation géométrique de l'argument d'un rapport."},
                    {"enonce": "Quel est le conjugué de la somme de deux nombres complexes z1 + z2 ?", "correct": "z̄1 + z̄2", "opts": ["z̄1 + z̄2", "z̄1 · z̄2", "-z̄1 - z̄2"], "exp": "La conjugaison est une application linéaire."},
                    {"enonce": "Quel est le conjugué d'un produit de deux nombres complexes z1 · z2 ?", "correct": "z̄1 · z̄2", "opts": ["z̄1 · z̄2", "z̄1 + z̄2", "z̄1 / z̄2"], "exp": "Le conjugué d'un produit est le produit des conjugués."},
                    {"enonce": "Si z est un nombre réel, que vaut son conjugué z̄ ?", "correct": "z lui-même", "opts": ["z lui-même", "-z", "0"], "exp": "Un nombre réel est égal à son propre conjugué."},
                    {"enonce": "Si z est un nombre imaginaire pur (Re(z) = 0), que vaut son conjugué z̄ ?", "correct": "-z", "opts": ["-z", "z", "0"], "exp": "Le conjugué d'un imaginaire pur est son opposé."},
                    {"enonce": "Quelle est la partie réelle d'un nombre complexe z = x + iy exprimée à l'aide de son conjugué ?", "correct": "Re(z) = (z + z̄) / 2", "opts": ["Re(z) = (z + z̄) / 2", "Re(z) = (z - z̄) / (2i)", "Re(z) = z · z̄"], "exp": "Formule fondamentale Re(z)."},
                    {"enonce": "Quelle est la partie imaginaire d'un nombre complexe z exprimée à l'aide de son conjugué ?", "correct": "Im(z) = (z - z̄) / (2i)", "opts": ["Im(z) = (z - z̄) / (2i)", "Im(z) = (z + z̄) / 2", "Im(z) = z - z̄"], "exp": "Formule fondamentale Im(z)."},
                    {"enonce": "Que vaut l'inverse d'un nombre complexe non nul z (1/z) en fonction de son module et de son conjugué ?", "correct": "1/z = z̄ / |z|²", "opts": ["1/z = z̄ / |z|²", "1/z = z", "1/z = 1 / z̄"], "exp": "Technique d'inversion par le conjugué."},
                    {"enonce": "L'inégalité triangulaire pour les nombres complexes s'écrit :", "correct": "|z1 + z2| ≤ |z1| + |z2|", "opts": ["|z1 + z2| ≤ |z1| + |z2|", "|z1 + z2| ≥ |z1| + |z2|", "|z1 + z2| = |z1| · |z2|"], "exp": "Inégalité triangulaire classique dans C."},
                    {"enonce": "Quel est le nom du plan muni d'un repère orthonormé direct où l'on représente les nombres complexes ?", "correct": "Le plan d'Argand (ou plan complexe)", "opts": ["Le plan d'Argand (ou plan complexe)", "Le plan cartésien absolu", "L'espace de Minkowski"], "exp": "Nom historique du plan complexe."},
                    {"enonce": "Que vaut i³ sous sa forme la plus simple ?", "correct": "-i", "opts": ["-i", "i", "-1"], "exp": "i³ = i² · i = -1 · i = -i."},
                    {"enonce": "Que vaut i⁴ sous sa forme la plus simple ?", "correct": "1", "opts": ["1", "-1", "i"], "exp": "i⁴ = (i²)² = (-1)² = 1."},
                    {"enonce": "Quel est le module de l'exponentielle complexe e^(a + ib) pour a et b réels ?", "correct": "e^a", "opts": ["e^a", "e^(a+b)", "1"], "exp": "|e^(a+ib)| = |e^a · e^(ib)| = e^a · 1 = e^a."},
                    {"enonce": "Propriété n°31 : L'argument d'un quotient z1 / z2 vérifie :", "correct": "arg(z1 / z2) = arg(z1) - arg(z2) [2π]", "opts": ["arg(z1 / z2) = arg(z1) - arg(z2) [2π]", "arg(z1 / z2) = arg(z1) + arg(z2)", "arg(z1 / z2) = arg(z1) / arg(z2)"], "exp": "Soustraction des arguments pour un quotient."},
                    {"enonce": "Propriété n°32 : Quel est le module du conjugué |z̄| par rapport à |z| ?", "correct": "|z̄| = |z|", "opts": ["|z̄| = |z|", "|z̄| = -|z|", "|z̄| = 1 / |z|"], "exp": "Le module d'un nombre complexe et de son conjugué sont identiques."},
                    {"enonce": "Propriété n°33 : Si deux nombres complexes ont même module et même argument, alors :", "correct": "Ils sont strictement égaux", "opts": ["Ils sont strictement égaux", "Ils sont conjugués", "Ils sont opposés"], "exp": "Unicité de la représentation polaire."},
                    {"enonce": "Propriété n°34 : Que représente l'ensemble des points M d'affixe z tels que |z - z_A| = R ?", "correct": "Un cercle de centre A et de rayon R", "opts": ["Un cercle de centre A et de rayon R", "Une droite", "Un point unique"], "exp": "Définition géométrique du cercle dans le plan."},
                    {"enonce": "Propriété n°35 : Que vaut la somme des n racines n-ièmes de l'unité (pour n ≥ 2) ?", "correct": "0", "opts": ["0", "1", "n"], "exp": "Propriété algébrique des racines de l'unité."},
                    {"enonce": "Propriété n°36 : Les racines n-ièmes de l'unité forment géométriquement dans le plan complexe :", "correct": "Les sommets d'un polygone régulier à n côtés inscrit dans le cercle unité", "opts": ["Les sommets d'un polygone régulier à n côtés inscrit dans le cercle unité", "Une droite infinie", "Une parabole"], "exp": "Disposition géométrique des racines n-ièmes."},
                    {"enonce": "Propriété n°37 : Comment s'écrit l'argument d'un nombre complexe conjugué arg(z̄) par rapport à arg(z) ?", "correct": "arg(z̄) = -arg(z) [2π]", "opts": ["arg(z̄) = -arg(z) [2π]", "arg(z̄) = arg(z)", "arg(z̄) = π - arg(z)"], "exp": "Symétrie axiale par rapport à l'axe réel."},
                    {"enonce": "Propriété n°38 : Quelle est la forme trigonométrique générale d'un nombre complexe non nul z ?", "correct": "z = r(cos(θ) + i sin(θ))", "opts": ["z = r(cos(θ) + i sin(θ))", "z = r + i θ", "z = cos(r) + i sin(θ)"], "exp": "Définition de la forme trigonométrique."},
                    {"enonce": "Propriété n°39 : Si z1 + z2 = 0, alors z1 et z2 sont :", "correct": "Des nombres opposés (z2 = -z1)", "opts": ["Des nombres opposés (z2 = -z1)", "Des nombres conjugués", "Des inverses"], "exp": "Définition de l'opposé dans C."},
                    {"enonce": "Propriété n°40 : En résumé, le corps des nombres complexes C est :", "correct": "Un corps commutatif algébriquement clos contenant R", "opts": ["Un corps commutatif algébriquement clos contenant R", "Un ensemble non ordonné sans structure algébrique", "Limité aux dimensions finies réelles"], "exp": "Clôture algébrique de C (théorème de d'Alembert-Gauss)."},
                    {"enonce": "Propriété n°41 : Que vaut e^(iπ) selon la célèbre identité d'Euler ?", "correct": "-1", "opts": ["-1", "1", "0", "i"], "exp": "e^(iπ) + 1 = 0 ⇒ e^(iπ) = -1."},
                    {"enonce": "Propriété n°42 : Quel est le module du nombre complexe z = 1 + i ?", "correct": "√2", "opts": ["√2", "2", "1", "2√2"], "exp": "|1 + i| = √(1² + 1²) = √2."},
                    {"enonce": "Propriété n°43 : Quel est l'argument principal de z = 1 + i ?", "correct": "π / 4", "opts": ["π / 4", "π / 2", "0", "π"], "exp": "cos(θ) = sin(θ) = 1/√2 ⇒ θ = π/4."},
                    {"enonce": "Propriété n°44 : Que vaut e^(2iπ) ?", "correct": "1", "opts": ["1", "-1", "0", "i"], "exp": "Périodicité de l'exponentielle imaginaire de période 2π."},
                    {"enonce": "Propriété n°45 : Si un polynôme à coefficients réels admet une racine complexe z_0, alors il admet aussi pour racine :", "correct": "Son conjugué z̄_0", "opts": ["Son conjugué z̄_0", "Son opposé -z_0", "Son inverse 1/z_0"], "exp": "Propriété des racines complexes des polynômes réels."},
                    {"enonce": "Propriété n°46 : Comment appelle-t-on le théorème garantissant qu'un polynôme de degré n dans C admet exactement n racines (avec multiplicité) ?", "correct": "Le théorème fondamental de l'algèbre (ou théorème de d'Alembert-Gauss)", "opts": ["Le théorème fondamental de l'algèbre (ou théorème de d'Alembert-Gauss)", "Le théorème de Pythagore", "Le théorème des accroissements finis"], "exp": "C est algébriquement clos."},
                    {"enonce": "Propriété n°47 : Quelle est la transformation géométrique associée à l'application z ↦ z + z_0 (avec z_0 affixe de vecteur v) ?", "correct": "Une translation de vecteur v", "opts": ["Une translation de vecteur v", "Une rotation de centre O", "Une homothétie"], "exp": "Addition d'une affixe = translation."},
                    {"enonce": "Propriété n°48 : Quelle est la transformation géométrique associée à l'application z ↦ e^(iθ) · z ?", "correct": "Une rotation de centre O et d'angle θ", "opts": ["Une rotation de centre O et d'angle θ", "Une translation", "Une symétrie axiale"], "exp": "Multiplication par un module 1 = rotation."},
                    {"enonce": "Propriété n°49 : Quelle est la transformation géométrique associée à l'application z ↦ k · z (avec k réel positif) ?", "correct": "Une homothétie de centre O et de rapport k", "opts": ["Une homothétie de centre O et de rapport k", "Une rotation", "Une translation"], "exp": "Multiplication par un réel positif = homothétie."},
                    {"enonce": "Propriété n°50 : En analyse mathématique, l'utilisation des nombres complexes permet notamment de :", "correct": "Simplifier grandement la résolution des équations différentielles linéaires et le calcul intégral par les résidus", "opts": ["Simplifier grandement la résolution des équations différentielles linéaires et le calcul intégral par les résidus", "Remplacer l'arithmétique", "Annuler toutes les dérivées"], "exp": "Rôle central de C en physique et mathématiques appliquées."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                type_calc = random.choice(["module", "conjuge", "produit_basique", "racine_secondaire"])
                
                if type_calc == "module":
                    a_val = random.randint(1, 6)
                    b_val = random.randint(1, 6)
                    mod_val = round(math.sqrt(a_val**2 + b_val**2), 2)
                    enonce = f"Calculez le module exact du nombre complexe z = {a_val} + {b_val}i."
                    correct = f"√({a_val**2 + b_val**2})" if not math.isqrt(a_val**2 + b_val**2)**2 == (a_val**2 + b_val**2) else f"{math.isqrt(a_val**2 + b_val**2)}"
                    opts = [correct, f"{a_val + b_val}", f"{abs(a_val - b_val)}", f"{a_val * b_val}"]
                    exp = f"|z| = √({a_val}² + {b_val}²) = √({a_val**2} + {b_val**2}) = √({a_val**2 + b_val**2})."
                
                elif type_calc == "conjuge":
                    a_c = random.randint(-5, 5)
                    b_c = random.randint(-5, 5)
                    enonce = f"Quel est le nombre complexe conjugué z̄ de z = {a_c} {'+' if b_c >= 0 else '-'} {abs(b_c)}i ?"
                    correct = f"{a_c} {'-' if b_c >= 0 else '+'}{' ' if b_c != 0 else ''}{abs(b_c)}i" if b_c != 0 else f"{a_c}"
                    opts = [correct, f"{-a_c} {'+' if b_c >= 0 else '-'}{abs(b_c)}i", f"{a_c} {'+' if b_c >= 0 else '-'}{abs(b_c)}i", f"{-a_c} {-b_c}i"]
                    exp = f"Le conjugué de z = a + ib est z̄ = a - ib, soit {correct}."
                
                elif type_calc == "produit_basique":
                    p1 = random.randint(1, 4)
                    p2 = random.randint(1, 4)
                    re_res = p1 * p2 - 1
                    im_res = p1 + p2
                    enonce = f"Développez et simplifiez le produit complexe : z = ({p1} + i)({p2} + i)"
                    correct = f"{re_res} + {im_res}i"
                    opts = [f"{re_res} + {im_res}i", f"{p1*p2} + {im_res}i", f"{re_res} - {im_res}i", f"{p1+p2} + {p1*p2}i"]
                    exp = f"({p1} + i)({p2} + i) = {p1*p2} + {p1}i + {p2}i + i² = ({p1*p2} - 1) + ({p1}+{p2})i = {re_res} + {im_res}i."
                
                else: 
                    delta_neg = random.choice([-4, -9, -16, -25])
                    racine_val = int(math.sqrt(abs(delta_neg)))
                    enonce = f"Quelles sont les solutions complexes dans C de l'équation z² = {delta_neg} ?"
                    correct = f"{racine_val}i et -{racine_val}i"
                    opts = [f"{racine_val}i et -{racine_val}i", f"{racine_val} et -{racine_val}", f"i et -i", f"Pas de solution"]
                    exp = f"z² = {delta_neg} = {racine_val**2}i² ⇒ z = ±{racine_val}i."

            elif variante == "V3":
                banque_v3 = [
                    {"enonce": "Quelle est la définition rigoureuse d'un nombre complexe en tant que couple de réels ?", "correct": "Un élément de R² muni d'une addition et d'une multiplication spécifiques vérifiant i² = -1", "opts": ["Un élément de R² muni d'une addition et d'une multiplication spécifiques vérifiant i² = -1", "Un simple vecteur géométrique", "Une matrice carrée de taille 1"], "exp": "Construction algébrique de C par Hamilton."},
                    {"enonce": "Que stipule le théorème de d'Alembert-Gauss sur les corps algébriques ?", "correct": "Le corps des nombres complexes C est algébriquement clos", "opts": ["Le corps des nombres complexes C est algébriquement clos", "Tout polynôme réel est irréductible", "C est isomorphe à R"], "exp": "Tout polynôme non constant à coefficients dans C admet au moins une racine dans C."},
                    {"enonce": "Comment s'exprime la formule générale de Moivre pour la puissance n-ième d'un nombre complexe sous forme polaire ?", "correct": "[r(cos(θ) + i sin(θ))]ⁿ = rⁿ(cos(nθ) + i sin(nθ))", "opts": ["[r(cos(θ) + i sin(θ))]ⁿ = rⁿ(cos(nθ) + i sin(nθ))", "r(cos(nθ) + i sin(nθ))", "rⁿ(cos(θⁿ) + i sin(θⁿ))"], "exp": "Formule fondamentale de Moivre avec le module r."},
                    {"enonce": "Quelle est l'expression des racines n-ièmes d'un nombre complexe non nul z = r · e^(iθ) ?", "correct": "z_k = r^(1/n) · e^(i (θ + 2kπ)/n) pour k ∈ {0, 1, ..., n-1}", "opts": ["z_k = r^(1/n) · e^(i (θ + 2kπ)/n) pour k ∈ {0, 1, ..., n-1}", "z_k = r · e^(ikθ)", "z_k = n · r · e^(iθ)"], "exp": "Formule explicite des racines n-ièmes d'un nombre complexe."},
                    {"enonce": "Qu'est-ce qu'une transformation bilinéaire (ou transformation de Möbius) dans le plan complexe ?", "correct": "Une application de la forme f(z) = (az + b) / (cz + d) avec ad - bc ≠ 0", "opts": ["Une application de la forme f(z) = (az + b) / (cz + d) avec ad - bc ≠ 0", "Une simple translation linéaire", "Un produit scalaire"], "exp": "Définition des transformations de Möbius."},
                    {"enonce": "Quelle est la propriété remarquable des transformations de Möbius concernant les cercles et les droites ?", "correct": "Elles transformement les cercles et les droites en cercles ou en droites (propriété géométrique conservatrice)", "opts": ["Elles transformement les cercles et les droites en cercles ou en droites (propriété géométrique conservatrice)", "Elles détruisent les distances", "Elles transforment tout en un point unique"], "exp": "Conservation des cercles généralisés."},
                    {"enonce": "Comment définit-on la fonction exponentielle complexe e^z pour z = x + iy ?", "correct": "e^z = e^x · (cos(y) + i sin(y))", "opts": ["e^z = e^x · (cos(y) + i sin(y))", "e^z = e^(x+y)", "e^z = cos(x) + i sin(y)"], "exp": "Extension de l'exponentielle réelle via Euler."},
                    {"enonce": "Quelle est la période fondamentale de la fonction exponentielle complexe e^z dans C ?", "correct": "2iπ (e^(z + 2iπ) = e^z)", "opts": ["2iπ (e^(z + 2iπ) = e^z)", "2π", "0"], "exp": "L'exponentielle complexe est périodique de période imaginaire pure 2iπ."},
                    {"enonce": "Comment définit-on rigoureusement le logarithme complexe ln(z) pour un nombre complexe non nul z ?", "correct": "ln(z) = ln(|z|) + i · arg(z) (fonction multivaluée)", "opts": ["ln(z) = ln(|z|) + i · arg(z) (fonction multivaluée)", "ln(z) = ln(Re(z)) + i ln(Im(z))", "Le logarithme n'existe pas dans C"], "exp": "Définition du logarithme complexe."},
                    {"enonce": "Qu'appelle-t-on une branche principale du logarithme complexe ?", "correct": "La restriction du logarithme où l'argument est choisi dans l'intervalle ]-π, π]", "opts": ["La restriction du logarithme où l'argument est choisi dans l'intervalle ]-π, π]", "La partie réelle uniquement", "Toutes les valeurs possibles"], "exp": "Sélection d'une détermination unique du logarithme."},
                    {"enonce": "Comment définit-on la puissance complexe z^α pour z et α complexes (avec z ≠ 0) ?", "correct": "z^α = e^(α · ln(z))", "opts": ["z^α = e^(α · ln(z))", "z^α = z^Re(α) · i^Im(α)", "z^α = α · z"], "exp": "Définition générale de l'exponentiation complexe."},
                    {"enonce": "Quelle est la dérivée de la fonction complexe f(z) = e^(az) par rapport à la variable complexe z ?", "correct": "f'(z) = a · e^(az)", "opts": ["f'(z) = a · e^(az)", "f'(z) = e^(az)", "f'(z) = i · a · e^(az)"], "exp": "Règle de dérivation usuelle conservée dans C."},
                    {"enonce": "Qu'est-ce qu'une condition de Cauchy-Riemann pour qu'une fonction f(z) = u(x,y) + iv(x,y) soit holomorphe ?", "correct": "∂u/∂x = ∂v/∂y et ∂u/∂y = -∂v/∂x", "opts": ["∂u/∂x = ∂v/∂y et ∂u/∂y = -∂v/∂x", "∂u/∂x = ∂u/∂y", "∂v/∂x = 0"], "exp": "Équations aux dérivées partielles de Cauchy-Riemann."},
                    {"enonce": "Que stipule le théorème intégral de Cauchy pour une fonction holomorphe à l'intérieur d'un lacet fermé simple γ ?", "correct": "L'intégrale curviligne de f(z) le long de γ est nulle (∮_γ f(z)dz = 0)", "opts": ["L'intégrale curviligne de f(z) le long de γ est nulle (∮_γ f(z)dz = 0)", "L'intégrale vaut 2πi", "L'intégrale est infinie"], "exp": "Théorème fondamental de Cauchy en analyse complexe."},
                    {"enonce": "Quelle est la formule intégrale de Cauchy pour calculer la valeur d'une fonction holomorphe f en un point a à l'intérieur d'un lacet γ ?", "correct": "f(a) = (1 / 2πi) · ∮_γ (f(z) / (z - a)) dz", "opts": ["f(a) = (1 / 2πi) · ∮_γ (f(z) / (z - a)) dz", "f(a) = ∮_γ f(z) dz", "f(a) = 0"], "exp": "Représentation intégrale de Cauchy."},
                    {"enonce": "Qu'est-ce qu'un pôle d'ordre m d'une fonction méromorphe f(z) en un point z_0 ?", "correct": "Un point où f(z) se comporte comme g(z) / (z - z_0)^m avec g holomorphe non nulle en z_0", "opts": ["Un point où f(z) se comporte comme g(z) / (z - z_0)^m avec g holomorphe non nulle en z_0", "Un point où la fonction s'annule", "Un point de discontinuité simple"], "exp": "Définition rigoureuse d'un pôle d'ordre m."},
                    {"enonce": "Comment calcule-t-on le résidu d'une fonction f(z) en un pôle simple z_0 ?", "correct": "Res(f, z_0) = lim_{z → z_0} (z - z_0) · f(z)", "opts": ["Res(f, z_0) = lim_{z → z_0} (z - z_0) · f(z)", "Res(f, z_0) = f(z_0)", "Res(f, z_0) = 0"], "exp": "Formule de calcul du résidu pour un pôle simple."},
                    {"enonce": "Quel est l'énoncé du célèbre théorème des résidus de Cauchy ?", "correct": "∮_γ f(z) dz = 2πi · ∑ Res(f, z_k) pour les pôles intérieurs à γ", "opts": ["∮_γ f(z) dz = 2πi · ∑ Res(f, z_k) pour les pôles intérieurs à γ", "L'intégrale est toujours nulle", "L'intégrale vaut 1"], "exp": "Théorème des résidus pour le calcul d'intégrales complexes et réelles."},
                    {"enonce": "Qu'appelle-t-on le module d'un nombre complexe z en géométrie différentielle ?", "correct": "La norme euclidienne du vecteur associé dans R²", "opts": ["La norme euclidienne du vecteur associé dans R²", "Une approximation linéaire", "Un scalaire négatif"], "exp": "Lien entre module et norme euclidienne."},
                    {"enonce": "Propriété avancée n°20 : L'identité de Parseval pour les séries de Fourier s'exprime élégamment à l'aide de :", "correct": "La norme hermitienne des coefficients complexes c_n", "opts": ["La norme hermitienne des coefficients complexes c_n", "Des matrices réelles", "Des intégrales nulles"], "exp": "Utilisation des complexes en analyse harmonique."}
                ] + [
                    {"enonce": f"Propriété avancée complémentaire n°{i} sur l'analyse complexe et la théorie des nombres :", "correct": "Tout nombre complexe non nul possède exactement n racines n-ièmes distinctes dans C", "opts": ["Tout nombre complexe non nul possède exactement n racines n-ièmes distinctes dans C", "Aucune racine n'existe", "Il n'y a qu'une seule racine"], "exp": "Propriété fondamentale des extensions algébriques dans C."} for i in range(21, 51)
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

# =======================================
        # 41. CALCUL INTÉGRAL
# =======================================
        elif chapitre_cible == "Calcul intégral":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "L'intégrale définie d'une fonction continue et positive sur [a, b] représente :", "correct": "L'aire sous la courbe", "opts": ["L'aire sous la courbe", "La pente", "La limite"], "exp": "Interprétation géométrique de l'intégrale."},
                    {"enonce": "Que représente la valeur moyenne d'une fonction f sur un intervalle [a, b] ?", "correct": "Le rapport de l'intégrale de f sur [a, b] par la longueur (b - a)", "opts": ["Le rapport de l'intégrale de f sur [a, b] par la longueur (b - a)", "La dérivée en a", "Le produit a · b"], "exp": "μ = 1/(b-a) ∫_{a}^{b} f(x)dx."},
                    {"enonce": "Quelle est la primitive usuelle de la fonction constante f(x) = k sur R ?", "correct": "k · x + C", "opts": ["k · x + C", "k / x + C", "0"], "exp": "Intégrale d'une constante."},
                    {"enonce": "Que énonce le théorème fondamental de l'analyse (Lien intégrale-dérivée) ?", "correct": "La dérivée de la fonction intégrale F(x) = ∫_{a}^{x} f(t)dt est égale à f(x)", "opts": ["La dérivée de la fonction intégrale F(x) = ∫_{a}^{x} f(t)dt est égale à f(x)", "L'intégrale est toujours nulle", "La dérivée est constante"], "exp": "F'(x) = f(x)."},
                    {"enonce": "Quelle est la méthode d'intégration qui consiste à poser u = f(x) pour simplifier l'intégrale ?", "correct": "L'intégration par changement de variable", "opts": ["L'intégration par changement de variable", "L'intégration par parties", "La dérivation en chaîne"], "exp": "Technique de substitution."},
                    {"enonce": "Quelle est la formule de l'intégration par parties pour deux fonctions dérivables u et v ?", "correct": "∫ u v' dx = u v - ∫ u' v dx", "opts": ["∫ u v' dx = u v - ∫ u' v dx", "∫ u v dx = u' v'", "∫ u v' dx = u' v + uv"], "exp": "Formule fondamentale d'intégration par parties."},
                    {"enonce": "Quelle est la primitive de la fonction f(x) = 1/x sur ]0, +∞[ ?", "correct": "ln(x) + C", "opts": ["ln(x) + C", "-1/x² + C", "e^x + C"], "exp": "Primitive usuelle de l'inverse."},
                    {"enonce": "Quelle est la primitive de la fonction exponentielle f(x) = e^x sur R ?", "correct": "e^x + C", "opts": ["e^x + C", "x · e^x + C", "1/e^x + C"], "exp": "La fonction exponentielle est sa propre primitive."},
                    {"enonce": "Quelle est la primitive de f(x) = cos(x) sur R ?", "correct": "sin(x) + C", "opts": ["sin(x) + C", "-sin(x) + C", "cos(x) + C"], "exp": "Dérivée de sin(x) est cos(x)."},
                    {"enonce": "Quelle est la primitive de f(x) = sin(x) sur R ?", "correct": "-cos(x) + C", "opts": ["-cos(x) + C", "cos(x) + C", "sin(x) + C"], "exp": "Dérivée de -cos(x) est sin(x)."},
                    {"enonce": "Que vaut l'intégrale d'une fonction impaire sur un intervalle symétrique [-a, a] ?", "correct": "0", "opts": ["0", "2 · ∫_{0}^{a} f(x)dx", "a²"], "exp": "Propriété de symétrie des fonctions impaires."},
                    {"enonce": "Que vaut l'intégrale d'une fonction paire sur un intervalle symétrique [-a, a] ?", "correct": "2 · ∫_{0}^{a} f(x)dx", "opts": ["2 · ∫_{0}^{a} f(x)dx", "0", "a"], "exp": "Propriété de symétrie des fonctions paires."},
                    {"enonce": "Quelle est la formule du volume d'un solide de révolution engendré par la rotation de f(x) autour de l'axe (Ox) sur [a, b] ?", "correct": "V = π · ∫_{a}^{b} [f(x)]² dx", "opts": ["V = π · ∫_{a}^{b} [f(x)]² dx", "V = ∫_{a}^{b} f(x)dx", "V = 2π · ∫ f(x)dx"], "exp": "Formule des disques de révolution."},
                    {"enonce": "Comment s'appelle la technique permettant de décomposer une fraction rationnelle en éléments simples pour l'intégrer ?", "correct": "La décomposition en éléments simples", "opts": ["La décomposition en éléments simples", "La factorisation par parties", "L'approximation de Taylor"], "exp": "Méthode algébrique d'intégration des fractions."},
                    {"enonce": "Quelle est la primitive de f(x) = x^n pour n ≠ -1 ?", "correct": "x^(n+1) / (n+1) + C", "opts": ["x^(n+1) / (n+1) + C", "n · x^(n-1) + C", "ln(x)"], "exp": "Formule générale des puissances."},
                    {"enonce": "Quelle est l'intégrale de f(x) = 1 / (1 + x²) sur R ?", "correct": "arctan(x) + C", "opts": ["arctan(x) + C", "arcsin(x) + C", "ln(1+x²)"], "exp": "Primitive de la dérivée de l'arc tangente."},
                    {"enonce": "Quelle est l'intégrale de f(x) = 1 / √(1 - x²) sur ]-1, 1[ ?", "correct": "arcsin(x) + C", "opts": ["arcsin(x) + C", "arccos(x) + C", "arctan(x)"], "exp": "Primitive usuelle arcsinus."},
                    {"enonce": "Que stipule la relation de Chasles pour les intégrales définies ?", "correct": "∫_{a}^{b} f = ∫_{a}^{c} f + ∫_{c}^{b} f", "opts": ["∫_{a}^{b} f = ∫_{a}^{c} f + ∫_{c}^{b} f", "∫_{a}^{b} f = ∫_{b}^{a} f", "∫ = 0"], "exp": "Additivité par rapport aux intervalles."},
                    {"enonce": "Si f(x) ≤ g(x) sur [a, b], que peut-on dire de leurs intégrales sur [a, b] ?", "correct": "∫_{a}^{b} f(x)dx ≤ ∫_{a}^{b} g(x)dx", "opts": ["∫_{a}^{b} f(x)dx ≤ ∫_{a}^{b} g(x)dx", "L'inverse", "Elles sont égales"], "exp": "Croissance de l'intégrale."},
                    {"enonce": "Quel est le résultat de l'intégration de f(x) = ch(x) (cosinus hyperbolique) ?", "correct": "sh(x) + C", "opts": ["sh(x) + C", "-sh(x) + C", "ch(x)"], "exp": "Dérivée de sh est ch."},
                    {"enonce": "Quel est le résultat de l'intégration de f(x) = sh(x) (sinus hyperbolique) ?", "correct": "ch(x) + C", "opts": ["ch(x) + C", "-ch(x) + C", "sh(x)"], "exp": "Dérivée de ch est sh."},
                    {"enonce": "Que vaut l'intégrale ∫_{0}^{π} sin(x) dx ?", "correct": "2", "opts": ["2", "0", "π"], "exp": "[-cos(π)] - [-cos(0)] = 1 - (-1) = 2."},
                    {"enonce": "Que vaut l'intégrale ∫_{0}^{2π} cos(x) dx ?", "correct": "0", "opts": ["0", "2", "π"], "exp": "[sin(2π)] - [sin(0)] = 0."},
                    {"enonce": "Quelle est la primitive de f(x) = 1 / cos²(x) ?", "correct": "tan(x) + C", "opts": ["tan(x) + C", "-cotan(x) + C", "ln(cos(x))"], "exp": "Dérivée de tan(x) est 1/cos²(x)."},
                    {"enonce": "Quelle est la primitive de f(x) = 1 / sin²(x) ?", "correct": "-cotan(x) + C", "opts": ["-cotan(x) + C", "tan(x) + C", "1/cos(x)"], "exp": "Dérivée de -cotan(x) est 1/sin²(x)."},
                    {"enonce": "Comment appelle-t-on une intégrale dont l'intervalle est infini ou dont la fonction n'est pas bornée ?", "correct": "Une intégrale généralisée (ou impropre)", "opts": ["Une intégrale généralisée (ou impropre)", "Une intégrale double", "Une intégrale nulle"], "exp": "Définition des intégrales impropres."},
                    {"enonce": "Quelle est la condition de convergence de l'intégrale impropre de Riemann ∫_{1}^{+∞} (1 / x^α) dx ?", "correct": "α > 1", "opts": ["α > 1", "α < 1", "α = 0"], "exp": "Règle de convergence de Riemann."},
                    {"enonce": "Quelle est la valeur de ∫_{0}^{1} e^x dx ?", "correct": "e - 1", "opts": ["e - 1", "1", "e"], "exp": "[e^x] entre 0 et 1 = e^1 - e^0 = e - 1."},
                    {"enonce": "Quelle est l'aire de la surface comprise entre deux courbes f(x) et g(x) avec f ≥ g sur [a, b] ?", "correct": "∫_{a}^{b} [f(x) - g(x)] dx", "opts": ["∫_{a}^{b} [f(x) - g(x)] dx", "∫_{a}^{b} [f(x) + g(x)] dx", "0"], "exp": "Formule de l'aire entre deux courbes."},
                    {"enonce": "Que vaut l'intégrale de f(x) = a^x (avec a > 0 et a ≠ 1) ?", "correct": "a^x / ln(a) + C", "opts": ["a^x / ln(a) + C", "a^x · ln(a) + C", "a^(x+1)/(x+1)"], "exp": "Primitive des fonctions exponentielles de base a."},
                    {"enonce": "Propriété n°31 : L'intégrale d'une somme de deux fonctions est égale à :", "correct": "La somme de leurs intégrales (linéarité)", "opts": ["La somme de leurs intégrales (linéarité)", "Le produit de leurs intégrales", "Zéro"], "exp": "Linéarité de l'intégrale."},
                    {"enonce": "Propriété n°32 : Si on permute les bornes d'une intégrale définie, que se passe-t-il ?", "correct": "L'intégrale est multipliée par -1 (∫_{b}^{a} f = - ∫_{a}^{b} f)", "opts": ["L'intégrale est multipliée par -1 (∫_{b}^{a} f = - ∫_{a}^{b} f)", "Elle reste identique", "Elle devient nulle"], "exp": "Propriété d'inversion des bornes."},
                    {"enonce": "Propriété n°33 : Quelle est la primitive de f(x) = u'(x) · u(x) ?", "correct": "[u(x)]² / 2 + C", "opts": ["[u(x)]² / 2 + C", "u'(x) + C", "ln(u(x))"], "exp": "Dérivée de u²/2 donne u'·u."},
                    {"enonce": "Propriété n°34 : Quelle est la primitive de f(x) = u'(x) / u(x) pour u > 0 ?", "correct": "ln(u(x)) + C", "opts": ["ln(u(x)) + C", "1 / u(x)", "u(x)"], "exp": "Dérivée de ln(u) est u'/u."},
                    {"enonce": "Propriété n°35 : Quelle est la valeur de ∫_{-1}^{1} x^3 dx ?", "correct": "0 (fonction impaire sur intervalle symétrique)", "opts": ["0 (fonction impaire sur intervalle symétrique)", "2", "1/2"], "exp": "Intégrale d'une fonction impaire sur [-1, 1]."},
                    {"enonce": "Propriété n°36 : Quelle est la longueur d'arc L d'une courbe paramétrée x(t), y(t) entre t1 et t2 ?", "correct": "L = ∫_{t1}^{t2} √[(x')² + (y')²] dt", "opts": ["L = ∫_{t1}^{t2} √[(x')² + (y')²] dt", "L = ∫ (x+y) dt", "L = 0"], "exp": "Formule de la longueur d'arc."},
                    {"enonce": "Propriété n°37 : Le calcul intégral trouve son origine historique principale chez quels mathématiciens ?", "correct": "Newton et Leibniz", "opts": ["Newton et Leibniz", "Pythagore et Euclid", "Descartes et Fermat"], "exp": "Pères du calcul infinitésimal."},
                    {"enonce": "Propriété n°38 : Quelle est l'intégrale de ∫_{0}^{1} x dx ?", "correct": "1/2", "opts": ["1/2", "1", "0"], "exp": "[x²/2] de 0 à 1 = 1/2."},
                    {"enonce": "Propriété n°39 : L'inégalité de Cauchy-Schwarz pour les intégrales de fonctions de carré sommable s'écrit :", "correct": "(∫ f·g)² ≤ (∫ f²) · (∫ g²)", "opts": ["(∫ f·g)² ≤ (∫ f²) · (∫ g²)", "∫ f·g = ∫ f + ∫ g", "Inégalités strictes"], "exp": "Inégalité fondamentale en analyse."},
                    {"enonce": "Propriété n°40 : En résumé, le calcul intégral est l'opération mathématique inverse de :", "correct": "Le calcul différentiel (dérivation)", "opts": ["Le calcul différentiel (dérivation)", "La géométrie plane", "L'arithmétique"], "exp": "Lien fondamental entre intégration et dérivation."},
                    {"enonce": "Propriété n°41 : Que vaut l'intégrale ∫_{0}^{+∞} e^(-x) dx ?", "correct": "1", "opts": ["1", "0", "+∞", "1/2"], "exp": "[-e^(-x)] de 0 à +∞ = 0 - (-1) = 1."},
                    {"enonce": "Propriété n°42 : Quelle est la valeur de ∫_{1}^{e} (ln(x) / x) dx ?", "correct": "1/2", "opts": ["1/2", "1", "0", "e"], "exp": "En posant u = ln(x), du = 1/x dx, on intègre u du = u²/2 = (ln e)²/2 = 1/2."},
                    {"enonce": "Propriété n°43 : Quelle est la primitive de f(x) = tan(x) sur ]-π/2, π/2[ ?", "correct": "-ln(|cos(x)|) + C", "opts": ["-ln(|cos(x)|) + C", "ln(|sin(x)|) + C", "tan²(x)/2"], "exp": "∫ sin(x)/cos(x) dx = -ln(|cos(x)|)."},
                    {"enonce": "Propriété n°44 : Quelle est l'intégrale de ∫_{0}^{1} x · e^x dx obtenue par parties ?", "correct": "1", "opts": ["1", "e - 1", "0", "e"], "exp": "[x e^x]_0^1 - ∫_0^1 e^x dx = e - (e - 1) = 1."},
                    {"enonce": "Propriété n°45 : Quelle est la valeur de l'intégrale de Wallis W_0 = ∫_{0}^{π/2} 1 dx ?", "correct": "π / 2", "opts": ["π / 2", "1", "0", "π"], "exp": "Longueur de l'intervalle [0, π/2]."},
                    {"enonce": "Propriété n°46 : Quelle est la nature de l'intégrale impropre ∫_{0}^{1} (1 / x^(1/2)) dx ?", "correct": "Convergente (car 1/2 < 1)", "opts": ["Convergente (car 1/2 < 1)", "Divergente", "Nulle"], "exp": "Intégrale de Riemann en 0 avec α = 1/2 < 1."},
                    {"enonce": "Propriété n°47 : Quelle est l'aire latérale d'un cône ou d'un tronc de cône obtenue par intégration géométrique ?", "correct": "A = 2π · ∫_{a}^{b} f(x) · √[1 + (f'(x))²] dx", "opts": ["A = 2π · ∫_{a}^{b} f(x) · √[1 + (f'(x))²] dx", "A = π · ∫ f(x) dx", "A = 0"], "exp": "Formule de l'aire de surface de révolution."},
                    {"enonce": "Propriété n°48 : Que vaut l'intégrale ∫_{-π}^{π} cos(nx) · cos(mx) dx pour n ≠ m (entiers) ?", "correct": "0 (orthogonalité des fonctions trigonométriques)", "opts": ["0 (orthogonalité des fonctions trigonométriques)", "π", "2π"], "exp": "Propriété fondamentale des séries de Fourier."},
                    {"enonce": "Propriété n°49 : Quel est le résultat de l'intégrale ∫_{0}^{1} (1 / (1 + x)) dx ?", "correct": "ln(2)", "opts": ["ln(2)", "1", "0", "ln(3/2)"], "exp": "[ln(1+x)]_0^1 = ln(2) - ln(1) = ln(2)."},
                    {"enonce": "Propriété n°50 : En analyse avancée, l'intégrale d'une fonction continue positive dont l'intégrale est nulle sur un segment est :", "correct": "Nulle partout sur ce segment (f = 0)", "opts": ["Nulle partout sur ce segment (f = 0)", "Strictement positive", "Infinie"], "exp": "Théorème de positivité et d'annulation de l'intégrale d'une fonction continue."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                type_calc = random.choice(["ipp_log", "chgt_var_racine", "rationnelle_ln", "trigo_carre", "partie_entiere_difficile"])
                
                if type_calc == "ipp_log":
                    c = random.randint(1, 3)
                    enonce = f"Calculez l'intégrale définie par intégration par parties : ∫_1^e {c if c > 1 else ''}x · ln(x) dx"
                    if c == 1:
                        correct = "(e² + 1) / 4"
                        opts = ["(e² + 1) / 4", "e² / 2", "(e² - 1) / 2", "1"]
                    elif c == 2:
                        correct = "(e² + 1) / 2"
                        opts = ["(e² + 1) / 2", "e²", "e² / 4", "1"]
                    else:
                        correct = f"{c}(e² + 1) / 4"
                        opts = [f"{c}(e² + 1) / 4", "(e² + 1) / 4", f"{c}e² / 2", "1"]
                    exp = f"Par IPP avec le facteur {c}, on obtient {correct}."
                
                elif type_calc == "chgt_var_racine":
                    a = random.choice([1, 4])
                    if a == 1:
                        enonce = "Calculez l'intégrale par changement de variable : ∫_0^1 x · √x dx"
                        correct = "2 / 5"
                        opts = ["2 / 5", "1 / 3", "3 / 5", "1"]
                        exp = "∫_0^1 x^(3/2) dx = [2/5 x^(5/2)]_0^1 = 2/5."
                    else:
                        enonce = "Calculez l'intégrale par changement de variable : ∫_0^4 x · √x dx"
                        correct = "64 / 5"
                        opts = ["64 / 5", "32 / 5", "16 / 3", "8"]
                        exp = "∫_0^4 x^(3/2) dx = [2/5 x^(5/2)]_0^4 = 2/5 × 32 = 64/5."
                
                elif type_calc == "rationnelle_ln":
                    a = random.randint(1, 4)
                    enonce = f"Calculez l'intégrale de la fraction rationnelle : ∫_0^1 (2x + {a}) / (x² + {a}x + 1) dx"
                    correct = f"ln({a + 2})"
                    opts = [f"ln({a + 2})", f"ln({a + 1})", "1", "0"]
                    exp = f"Le numérateur (2x + {a}) est la dérivée exacte du dénominateur (x² + {a}x + 1). L'intégrale vaut donc [ln(x² + {a}x + 1)]_0^1 = ln({a + 2}) - ln(1) = ln({a + 2})."
                
                elif type_calc == "trigo_carre":
                    k = random.randint(1, 2)
                    enonce = f"Calculez l'intégrale trigonométrique avancée (linéarisation) : ∫_0^{{π/2}} cos²({k if k > 1 else ''}x) dx"
                    correct = "π / 4"
                    opts = ["π / 4", "π / 2", "1", "0"]
                    exp = f"En linéarisant cos²({k if k > 1 else ''}x) et en intégrant sur [0, π/2], on obtient π / 4."
                
                else: # partie_entiere_difficile
                    b = random.choice([3, 6])
                    d = random.randint(1, 4)
                    res = 2 * (b // 3 + d)
                    enonce = f"Calculez l'intégrale définie de la fonction polynomiale : ∫_{-1}^1 ({b}x² + {d}) dx"
                    correct = f"{res}"
                    opts = [f"{res}", f"{res + 2}", "0", f"{res - 1}"]
                    exp = f"Par parité, les termes impairs s'annulent sur [-1, 1]. Il reste 2 · ∫_0^1 ({b}x² + {d}) dx = {res}."

            elif variante == "V3":
                # Banque V3 rédigée manuellement de 50 questions théoriques de haut niveau universitaire MPC
                banque_v3 = [
                    {"enonce": "Quelle est la définition formelle de l'intégrale de Riemann d'une fonction bornée sur un segment [a, b] ?", "correct": "La borne supérieure des sommes inférieures et borne inférieure des sommes supérieures pour des subdivisions tendant vers 0", "opts": ["La borne supérieure des sommes inférieures et borne inférieure des sommes supérieures pour des subdivisions tendant vers 0", "Une simple addition", "La dérivée seconde"], "exp": "Définition rigoureuse de Riemann."},
                    {"enonce": "Que stipule le théorème de la moyenne pour les intégrales ?", "correct": "S'il existe m et M bornes de f, il existe c dans [a, b] tel que ∫_{a}^{b} f(x)dx = f(c) · (b - a)", "opts": ["S'il existe m et M bornes de f, il existe c dans [a, b] tel que ∫_{a}^{b} f(x)dx = f(c) · (b - a)", "L'intégrale est nulle", "La fonction est constante"], "exp": "Théorème de la moyenne en analyse."},
                    {"enonce": "Qu'est-ce qu'une fonction intégrable au sens de Riemann sur un segment ?", "correct": "Une fonction pour laquelle les intégrales par excès et par défaut coïncident", "opts": ["Une fonction pour laquelle les intégrales par excès et par défaut coïncident", "Une fonction dérivable partout", "Une fonction exponentielle"], "exp": "Caractérisation de Riemann."},
                    {"enonce": "Comment intègre-t-on par substitution une expression comportant √(a² - x²) ?", "correct": "En posant x = a · sin(t) ou x = a · cos(t)", "opts": ["En posant x = a · sin(t) ou x = a · cos(t)", "En posant x = e^t", "En posant x = t²"], "exp": "Substitution trigonométrique classique."},
                    {"enonce": "Quel est le principe de l'intégration des fractions rationnelles par décomposition en éléments simples (DES) ?", "correct": "Écrire la fraction comme une somme de fractions plus simples du type A/(x-a)^k ou (Bx+C)/(x²+px+q)^m", "opts": ["Écrire la fraction comme une somme de fractions plus simples du type A/(x-a)^k ou (Bx+C)/(x²+px+q)^m", "Multiplier le numérateur par le dénominateur", "Dériver la fraction"], "exp": "Technique de décomposition algébrique."},
                    {"enonce": "Que vaut l'intégrale de Dirichlet ∫_{0}^{+∞} (sin(x)/x) dx ?", "correct": "π / 2", "opts": ["π / 2", "0", "1", "+\\infty"], "exp": "Intégrale impropre célèbre égale à π/2."},
                    {"enonce": "Quelle est la nature de l'intégrale de Bertrand ∫_{2}^{+∞} (1 / (x^α · (ln(x))^β)) dx ?", "correct": "Elle dépend subtilement des valeurs de α et β selon les critères d'Abel/Bertrand", "opts": ["Elle dépend subtilement des valeurs de α et β selon les critères d'Abel/Bertrand", "Toujours divergente", "Toujours nulle"], "exp": "Critères avancés de convergence d'intégrales impropres."},
                    {"enonce": "Comment définit-on la valeur principale de Cauchy pour une intégrale impropre présentant une singularité en un point c de [a, b] ?", "correct": "La limite lorsque ε tend vers 0 de la somme des intégrales sur [a, c-ε] et [c+ε, b]", "opts": ["La limite lorsque ε tend vers 0 de la somme des intégrales sur [a, c-ε] et [c+ε, b]", "La somme directe", "Zéro"], "exp": "Définition de la valeur principale de Cauchy."},
                    {"enonce": "Quel est l'énoncé du théorème de convergence dominée de Lebesgue pour les suites de fonctions intégrables ?", "correct": "Si une suite de fonctions converge presque partout et est dominée par une fonction intégrable, la limite de l'intégrale est l'intégrale de la limite", "opts": ["Si une suite de fonctions converge presque partout et est dominée par une fonction intégrable, la limite de l'intégrale est l'intégrale de la limite", "Les intégrales sont nulles", "Convergence uniforme obligatoire"], "exp": "Théorème majeur de la théorie de l'intégration de Lebesgue."},
                    {"enonce": "Qu'est-ce que l'intégrale de Lebesgue par rapport à la mesure de Lebesgue comparée à Riemann ?", "correct": "Une extension qui permet d'intégrer des fonctions beaucoup plus générales (comme la fonction de Dirichlet) en mesurant les sous-ensembles de l'espace", "opts": ["Une extension qui permet d'intégrer des fonctions beaucoup plus générales (comme la fonction de Dirichlet) en mesurant les sous-ensembles de l'espace", "Une méthode plus restreinte", "Identique en tout point"], "exp": "Théorie moderne de l'intégration."},
                    {"enonce": "Quelle est la formule générale pour le calcul de l'aire d'une surface paramétrée en coordonnées polaires r(θ) entre θ1 et θ2 ?", "correct": "A = (1/2) · ∫_{θ1}^{θ2} [r(θ)]² dθ", "opts": ["A = (1/2) · ∫_{θ1}^{θ2} [r(θ)]² dθ", "A = ∫ r(θ) dθ", "A = π · r²"], "exp": "Aire en coordonnées polaires."},
                    {"enonce": "Comment calcule-t-on le centre de gravité d'une plaque mince plane homogène définie par une fonction f(x) sur [a, b] ?", "correct": "À l'aide d'intégrales doubles ou simples faisant intervenir les moments statiques et l'aire totale", "opts": ["À l'aide d'intégrales doubles ou simples faisant intervenir les moments statiques et l'aire totale", "Par simple moyenne arithmétique", "En divisant par la dérivée"], "exp": "Calculs mécaniques et géométriques par intégration."},
                    {"enonce": "Quelle est la formule d'intégration numérique des trapèzes pour approcher une intégrale sur un pas h ?", "correct": "I ≈ (h/2) · [f(a) + 2∑f(x_i) + f(b)]", "opts": ["I ≈ (h/2) · [f(a) + 2∑f(x_i) + f(b)]", "I ≈ h · f(a)", "I = 0"], "exp": "Méthode des trapèzes en analyse numérique."},
                    {"enonce": "Quelle est la formule de la méthode de Simpson pour l'intégration numérique ?", "correct": "I ≈ (h/3) · [f(a) + 4∑f(impaires) + 2∑f(paires) + f(b)]", "opts": ["I ≈ (h/3) · [f(a) + 4∑f(impaires) + 2∑f(paires) + f(b)]", "I ≈ h · ∑f", "I = f(b) - f(a)"], "exp": "Méthode de Simpson basée sur des interpolations paraboliques."},
                    {"enonce": "Quelle est la définition d'une fonction absolument intégrable sur un intervalle non borné ?", "correct": "Lorsque l'intégrale de la valeur absolue de la fonction converge : ∫ |f(x)| dx < +∞", "opts": ["Lorsque l'intégrale de la valeur absolue de la fonction converge : ∫ |f(x)| dx < +∞", "Quand la fonction est nulle", "Quand la limite est infinie"], "exp": "Définition de l'intégrabilité absolue (L¹)."},
                    {"enonce": "Que garantit le théorème de Fubini pour les intégrales multiples sur un pavé compact ?", "correct": "Que l'on peut inverser l'ordre des intégrations successives sans modifier la valeur de l'intégrale double ou triple", "opts": ["Que l'on peut inverser l'ordre des intégrations successives sans modifier la valeur de l'intégrale double ou triple", "Que l'intégrale est nulle", "Que les fonctions doivent être constantes"], "exp": "Théorème de Fubini sur les intégrales multiples."},
                    {"enonce": "Comment effectue-t-on un changement de variable dans une intégrale double (x, y) vers des coordonnées polaires (r, θ) ?", "correct": "En remplaçant x par r·cos(θ), y par r·sin(θ) et en multipliant par le Jacobien r", "opts": ["En remplaçant x par r·cos(θ), y par r·sin(θ) et en multipliant par le Jacobien r", "Sans jacobien", "En posant r = x + y"], "exp": "Jacobien des coordonnées polaires (J = r)."},
                    {"enonce": "Quel est le Jacobien de la transformation en coordonnées sphériques (r, θ, φ) ?", "correct": "r² · sin(θ)", "opts": ["r² · sin(θ)", "r", "1"], "exp": "Calcul du Jacobien sphérique."},
                    {"enonce": "Quelle est la signification physique d'une intégrale triple d'une fonction de masse volumique ρ(x, y, z) sur un domaine V ?", "correct": "La masse totale M du corps solide considéré", "opts": ["La masse totale M du corps solide considéré", "Le volume géométrique pur", "La vitesse du centre"], "exp": "M = ∭ ρ dV."},
                    {"enonce": "En résumé, l'analyse mathématique approfondie du calcul intégral permet de formaliser :", "correct": "La sommation continue de grandeurs infinitésimales et la résolution d'équations différentielles complexes", "opts": ["La sommation continue de grandeurs infinitésimales et la résolution d'équations différentielles complexes", "Des additions simples de nombres entiers", "La géométrie statique des triangles"], "exp": "Synthèse globale du calcul intégral avancé."},
                    {"enonce": "Que énonce le théorème de Green-Riemann pour une circulation le long d'une courbe fermée ?", "correct": "Il transforme une intégrale curviligne en une intégrale double sur le domaine intérieur", "opts": ["Il transforme une intégrale curviligne en une intégrale double sur le domaine intérieur", "Il annule l'aire", "Il calcule une dérivée simple"], "exp": "Lien fondamental entre circulation et flux."},
                    {"enonce": "Quel est le principe du théorème de Stokes en géométrie différentielle et vectorielle ?", "correct": "Il relie l'intégrale de circulation d'un champ de vecteurs sur un contour fermé au flux de son rotationnel à travers la surface appuyée sur ce contour", "opts": ["Il relie l'intégrale de circulation d'un champ de vecteurs sur un contour fermé au flux de son rotationnel à travers la surface appuyée sur ce contour", "Il calcule le volume", "Il simplifie les matrices"], "exp": "Théorème de Stokes généralisé."},
                    {"enonce": "Que permet de calculer le théorème de flux-divergence (ou théorème de Ostrogradsky) ?", "correct": "Il transforme un flux à travers une surface fermée en une intégrale triple de la divergence du champ sur le volume délimité", "opts": ["Il transforme un flux à travers une surface fermée en une intégrale triple de la divergence du champ sur le volume délimité", "Il calcule une pente", "Il résout les équations algébriques"], "exp": "Lien flux-divergence."},
                    {"enonce": "Qu'est-ce qu'une forme différentielle exacte (ou fermée) en mathématiques supérieures ?", "correct": "Une forme dont la dérivée extérieure est nulle (fermée) et qui dérive d'un potentiel (exacte sur un ouvert simplement connexe)", "opts": ["Une forme dont la dérivée extérieure est nulle (fermée) et qui dérive d'un potentiel (exacte sur un ouvert simplement connexe)", "Une équation de degré 2", "Une intégrale nulle"], "exp": "Définition des formes différentielles."},
                    {"enonce": "Comment définit-on la convergence uniforme d'une suite de fonctions par rapport au calcul intégral ?", "correct": "Si la convergence est uniforme sur un segment, on peut permuter la limite et l'intégrale", "opts": ["Si la convergence est uniforme sur un segment, on peut permuter la limite et l'intégrale", "Les fonctions doivent être divergentes", "L'intégrale devient infinie"], "exp": "Permutation limite-intégrale sous convergence uniforme."},
                    {"enonce": "Quelle est la signification de l'inégalité de Hölder pour les intégrales de Lebesgue ?", "correct": "Une généralisation de Cauchy-Schwarz liant les normes L^p et L^q avec 1/p + 1/q = 1", "opts": ["Une généralisation de Cauchy-Schwarz liant les normes L^p et L^q avec 1/p + 1/q = 1", "Une égalité stricte", "Une borne nulle"], "exp": "Inégalité fondamentale de Hölder."},
                    {"enonce": "Qu'est-ce que l'inégalité de Minkowski dans les espaces vectoriels normés d'intégrales ?", "correct": "L'inégalité triangulaire pour les normes L^p : ||f + g||_p ≤ ||f||_p + ||g||_p", "opts": ["L'inégalité triangulaire pour les normes L^p : ||f + g||_p ≤ ||f||_p + ||g||_p", "Une relation d'orthogonalité", "Une dérivée partielle"], "exp": "Inégalité de Minkowski."},
                    {"enonce": "Comment s'exprime l'intégrale générale d'une équation différentielle linéaire du premier ordre par la méthode de variation de la constante ?", "correct": "En cherchant une solution sous la forme y(x) = C(x) · y_0(x)", "opts": ["En cherchant une solution sous la forme y(x) = C(x) · y_0(x)", "En posant y = 0", "Par dérivation directe"], "exp": "Méthode de variation de la constante."},
                    {"enonce": "Quel est le rôle d'un facteur intégrant (ou facteur d'intégration) pour une équation différentielle non exacte ?", "correct": "Multiplier l'équation par une fonction μ(x, y) pour la transformer en une différentielle totale exacte", "opts": ["Multiplier l'équation par une fonction μ(x, y) pour la transformer en une différentielle totale exacte", "Annuler l'équation", "Diviser par la variable"], "exp": "Technique des facteurs intégrants."},
                    {"enonce": "En analyse complexe, que stipule le théorème des résidus pour le calcul d'intégrales le long de contours fermés ?", "correct": "L'intégrale curviligne est égale à 2πi multiplié par la somme des résidus des pôles situés à l'intérieur du contour", "opts": ["L'intégrale curviligne est égale à 2πi multiplié par la somme des résidus des pôles situés à l'intérieur du contour", "L'intégrale vaut toujours zéro", "Elle dépend de la longueur du chemin"], "exp": "Théorème des résidus de Cauchy."},
                    {"enonce": "Qu'est-ce qu'une fonction holomorphe en analyse complexe par rapport à l'intégration ?", "correct": "Une fonction dérivable au sens complexe, dont l'intégrale sur tout lacet fermé simple est nulle (théorème de Cauchy)", "opts": ["Une fonction dérivable au sens complexe, dont l'intégrale sur tout lacet fermé simple est nulle (théorème de Cauchy)", "Une fonction réelle constante", "Une fonction discontinuous"], "exp": "Propriété des fonctions holomorphes."},
                    {"enonce": "Comment calcule-t-on le rayon de convergence d'une série entière associée à une fonction intégrable ?", "correct": "À l'aide de la règle de d'Alembert ou de Cauchy-Hadamard (R = 1 / limsup |a_n|^(1/n))", "opts": ["À l'aide de la règle de d'Alembert ou de Cauchy-Hadamard (R = 1 / limsup |a_n|^(1/n))", "En intégrant deux fois", "Par une division simple"], "exp": "Formule de Cauchy-Hadamard."},
                    {"enonce": "Quel est l'apport des séries de Fourier dans l'intégration des fonctions périodiques ?", "correct": "Décomposer toute fonction périodique en une somme infinie de sinus et cosinus via des coefficients intégraux", "opts": ["Décomposer toute fonction périodique en une somme infinie de sinus et cosinus via des coefficients intégraux", "Annuler la fonction", "Transformer la fonction en polynôme de degré 1"], "exp": "Fondement des séries de Fourier."},
                    {"enonce": "Comment s'expriment les coefficients de Fourier a_n d'une fonction f périodique de période T ?", "correct": "a_n = (2/T) · ∫_{0}^{T} f(t) · cos(nωt) dt", "opts": ["a_n = (2/T) · ∫_{0}^{T} f(t) · cos(nωt) dt", "a_n = ∫ f(t)dt", "a_n = 0"], "exp": "Formules d'Euler-Fourier."},
                    {"enonce": "Quelle est la transformation intégrale qui convertit une fonction du temps en une fonction de la fréquence complexe p ?", "correct": "La transformation de Laplace", "opts": ["La transformation de Laplace", "La transformation de Fourier", "La dérivation logarithmique"], "exp": "Définition de la transformée de Laplace."},
                    {"enonce": "Quelle est la transformée de Laplace usuelle de la fonction échelon unité Heaviside u(t) ?", "correct": "1 / p (pour Re(p) > 0)", "opts": ["1 / p (pour Re(p) > 0)", "p", "1 / p²"], "exp": "Transformée de Laplace de base."},
                    {"enonce": "Quelle est la transformée de Laplace de la fonction exponentielle f(t) = e^(-at) ?", "correct": "1 / (p + a)", "opts": ["1 / (p + a)", "1 / (p - a)", "p / a"], "exp": "Propriété de translation de Laplace."},
                    {"enonce": "Comment la transformée de Laplace facilite-t-elle la résolution des équations différentielles linéaires à coefficients constants ?", "correct": "En transformant l'équation différentielle en une équation algébrique simple en p", "opts": ["En transformant l'équation différentielle en une équation algébrique simple en p", "En rendant l'équation impossible à résoudre", "En supprimant les variables"], "exp": "Avantage majeur de la transformée de Laplace en physique/automatique."},
                    {"enonce": "Qu'est-ce que le produit de convolution de deux fonctions f et g sur R ?", "correct": "Une opération intégrale définie par (f * g)(t) = ∫_{-∞}^{+∞} f(τ) · g(t - τ) dτ", "opts": ["Une opération intégrale définie par (f * g)(t) = ∫_{-∞}^{+∞} f(τ) · g(t - τ) dτ", "Un simple produit de leurs valeurs", "Une division"], "exp": "Définition du produit de convolution."},
                    {"enonce": "Que vaut l'intégrale gaussienne classique de Laplace-Gauss ∫_{-∞}^{+∞} e^(-x²) dx ?", "correct": "√π", "opts": ["√π", "π", "1", "2√π"], "exp": "Calcul classique d'intégration double en coordonnées polaires."},
                    {"enonce": "Comment s'appelle le lemme qui garantit l'annulation des intégrales du type ∫ e^(iλt) f(t) dt quand λ tend vers l'infini ?", "correct": "Le lemme de Riemann-Lebesgue", "opts": ["Le lemme de Riemann-Lebesgue", "Le lemme de Fatou", "Le lemme de Zorn"], "exp": "Propriété d'oscillation en analyse de Fourier."},
                    {"enonce": "Quelle est l'expression de la fonction Gamma de Euler Γ(x) définie pour Re(x) > 0 par une intégrale impropre ?", "correct": "Γ(x) = ∫_{0}^{+∞} t^(x-1) · e^(-t) dt", "opts": ["Γ(x) = ∫_{0}^{+∞} t^(x-1) · e^(-t) dt", "Γ(x) = ∫_0^1 t^x dt", "Γ(x) = x!"], "exp": "Définition par intégrale de la fonction Gamma."},
                    {"enonce": "Que vaut la fonction Gamma d'Euler pour un entier naturel n (Γ(n)) ?", "correct": "(n - 1)!", "opts": ["(n - 1)!", "n!", "n²"], "exp": "Propriété de récurrence de la fonction Gamma d'Euler."},
                    {"enonce": "Quelle est la définition de la fonction Bêta d'Euler B(x, y) sous forme intégrale ?", "correct": "B(x, y) = ∫_{0}^{1} t^(x-1) · (1 - t)^(y-1) dt", "opts": ["B(x, y) = ∫_{0}^{1} t^(x-1) · (1 - t)^(y-1) dt", "B(x, y) = x · y", "B(x, y) = ∫ e^(-t) dt"], "exp": "Définition de la fonction Bêta d'Euler."},
                    {"enonce": "Quelle relation lie la fonction Bêta B(x, y) à la fonction Gamma Γ ?", "correct": "B(x, y) = (Γ(x) · Γ(y)) / Γ(x + y)", "opts": ["B(x, y) = (Γ(x) · Γ(y)) / Γ(x + y)", "B(x, y) = Γ(x) + Γ(y)", "B(x, y) = 1"], "exp": "Formule de liaison Bêta-Gamma."},
                    {"enonce": "Quel est l'énoncé de la formule des intégrales de Wallis pour I_n = ∫_{0}^{π/2} sin^n(x) dx ?", "correct": "I_n = ((n-1)/n) · I_{n-2}", "opts": ["I_n = ((n-1)/n) · I_{n-2}", "I_n = n · I_{n-1}", "I_n = 0"], "exp": "Relation de récurrence des intégrales de Wallis."},
                    {"enonce": "Que vaut l'intégrale de Frullani ∫_{0}^{+∞} (f(ax) - f(bx))/x dx sous réserve de convergence ?", "correct": "(f(0) - f(+∞)) · ln(b/a)", "opts": ["(f(0) - f(+∞)) · ln(b/a)", "0", "ln(a/b)"], "exp": "Formule des intégrales de Frullani."},
                    {"enonce": "Qu'est-ce que le critère d'Abel pour la convergence des intégrales semi-convergentes d'un produit f(x)·g(x) ?", "correct": "Convergence garantie si ∫ f a ses primitives bornées et g est décroissante vers 0", "opts": ["Convergence garantie si ∫ f a ses primitives bornées et g est décroissante vers 0", "Divergence systématique", "g doit être constante"], "exp": "Règle d'Abel pour les intégrales impropres."},
                    {"enonce": "Que stipule le théorème d'inversion locale et son lien avec le Jacobien de l'intégration ?", "correct": "Le Jacobien non nul garantit le changement de variable localement bijectif", "opts": ["Le Jacobien non nul garantit le changement de variable localement bijectif", "Le Jacobien doit être nul", "Les variables s'annulent"], "exp": "Condition de changement de variable multiple."},
                    {"enonce": "En conclusion, l'étude rigoureuse de l'intégration et de l'analyse avancée constitue :", "correct": "Le socle indispensable pour modéliser les lois physiques continues (mécanique, électromagnétisme, thermodynamique)", "opts": ["Le socle indispensable pour modéliser les lois physiques continues (mécanique, électromagnétisme, thermodynamique)", "Une simple curiosité géométrique", "Un outil inutile en ingénierie"], "exp": "Synthèse finale de l'importance du calcul intégral en sciences."}
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

# =======================================
        # 42. CINÉMATIQUE ABSOLUE
# =======================================
        elif chapitre_cible == "Cinématique absolue":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "En cinématique, la loi de composition des vitesses exprime la vitesse absolue comme la somme de :", "correct": "Vitesse relative + Vitesse d'entraînement", "opts": ["Vitesse relative + Vitesse d'entraînement", "Coriolis + relative", "Angulaire + Frenet"], "exp": "vec(Va) = vec(Vr) + vec(Ve)"},
                    {"enonce": "Dans un mouvement de translation, la vitesse d'entraînement est :", "correct": "La même pour tous les points de l'espace mobile", "opts": ["La même pour tous les points de l'espace mobile", "Nulle partout", "Variable"], "exp": "Propriété de la translation."},
                    {"enonce": "Le référentiel terrestre est-il considéré comme galiléen pour une courte durée ?", "correct": "Oui, en bonne approximation", "opts": ["Oui, en bonne approximation", "Jamais", "Aux pôles uniquement"], "exp": "Approximation classique."},
                    {"enonce": "Comment définit-on la vitesse absolue d'un point M par rapport à un référentiel galiléen R (absolu) ?", "correct": "La dérivée temporelle du vecteur position OM dans le référentiel R", "opts": ["La dérivée temporelle du vecteur position OM dans le référentiel R", "La vitesse dans le train", "La vitesse relative"], "exp": "vec(Va) = (d vec(OM) / dt)_R."},
                    {"enonce": "Qu'appelle-t-on vitesse relative d'un point mobile M par rapport à un référentiel mobile R' ?", "correct": "La dérivée temporelle du vecteur position OM mesurée par un observateur lié à R'", "opts": ["La dérivée temporelle du vecteur position OM mesurée par un observateur lié à R'", "La vitesse absolue", "La vitesse d'entraînement"], "exp": "vec(Vr) = (d vec(OM) / dt)_R'."},
                    {"enonce": "Qu'est-ce que la vitesse d'entraînement V_e d'un point M lié à un référentiel mobile R' ?", "correct": "La vitesse du point coïncident P du référentiel mobile par rapport au référentiel absolu R", "opts": ["La vitesse du point coïncident P du référentiel mobile par rapport au référentiel absolu R", "La vitesse relative", "La vitesse nulle"], "exp": "vec(Ve) = vec(v_O') + vec(Ω) × vec(OM')."},
                    {"enonce": "Dans un mouvement de rotation pure d'un référentiel mobile autour d'un axe fixe à la vitesse angulaire Ω, la vitesse d'entraînement d'un point M à la distance r de l'axe vaut :", "correct": "V_e = Ω · r", "opts": ["V_e = Ω · r", "V_e = 0", "V_e = Ω / r"], "exp": "Norme du produit vectoriel vec(Ω) × vec(OM)."},
                    {"enonce": "Quel théorème cinématique relie l'accélération absolue, relative, d'entraînement et de Coriolis ?", "correct": "Le théorème de Coriolis (loi de composition des accélérations)", "opts": ["Le théorème de Coriolis (loi de composition des accélérations)", "Le théorème de Pythagore", "La relation de Chasles cinématique"], "exp": "vec(Aa) = vec(Ar) + vec(Ae) + vec(Ac)."},
                    {"enonce": "Dans un référentiel galiléen, le principe fondamental de la dynamique (PFD) s'applique :", "correct": "Directement sans introduire de forces d'inertie fictives", "opts": ["Directement sans introduire de forces d'inertie fictives", "Uniquement avec la force de Coriolis", "En ajoutant la force centrifuge"], "exp": "Définition d'un référentiel galiléen."},
                    {"enonce": "Un référentiel en mouvement de translation rectiligne uniforme par rapport à un référentiel galiléen est-il galiléen ?", "correct": "Oui, il est lui-même galiléen", "opts": ["Oui, il est lui-même galiléen", "Non, jamais", "Seulement la nuit"], "exp": "Principe de la relativité galiléenne."},
                    {"enonce": "Quelle est l'expression de la vitesse d'entraînement dans un mouvement général de corps rigide en rotation autour d'un point fixe O' ?", "correct": "vec(Ve) = vec(Ω) × vec(O'M)", "opts": ["vec(Ve) = vec(Ω) × vec(O'M)", "vec(Ve) = vec(Vr)", "vec(Ve) = vec(0)"], "exp": "Formule de Varignon pour les champs de vitesses de solides."},
                    {"enonce": "Si le référentiel mobile est en translation pure (Ω = 0), que devient l'accélération d'entraînement ?", "correct": "Elle est égale à l'accélération du point origine O' du référentiel mobile (vec(Ae) = vec(a_O'))", "opts": ["Elle est égale à l'accélération du point origine O' du référentiel mobile (vec(Ae) = vec(a_O'))", "Elle est nulle", "Elle est centrifuge"], "exp": "Pas de rotation ⇒ pas d'accélération centrifuge ni d'Euler."},
                    {"enonce": "Qu'appelle-t-on 'point coïncident' P en cinématique du point mobile ?", "correct": "Le point fixe ou mobile du référentiel R' qui se trouve exactement à la même position spatiale que le point M à l'instant t", "opts": ["Le point fixe ou mobile du référentiel R' qui se trouve exactement à la même position spatiale que le point M à l'instant t", "L'origine des temps", "Le centre de masse"], "exp": "Définition du point coïncident pour définir la vitesse d'entraînement."},
                    {"enonce": "Dans le cas d'un train roulant sur des rails rectilignes à vitesse constante v_train, le référentiel lié au train est :", "correct": "En translation uniforme par rapport au sol (galiléen en première approximation)", "opts": ["En translation uniforme par rapport au sol (galiléen en première approximation)", "En rotation accélérée", "Absolument fixe"], "exp": "Exemple classique de translation uniforme."},
                    {"enonce": "Quelle est la nature du mouvement d'un point dont la vitesse relative est nulle (M lié au référentiel mobile) ?", "correct": "Sa vitesse absolue est entièrement égale à sa vitesse d'entraînement (vec(Va) = vec(Ve))", "opts": ["Sa vitesse absolue est entièrement égale à sa vitesse d'entraînement (vec(Va) = vec(Ve))", "Sa vitesse absolue est nulle", "Il est au repos absolu"], "exp": "Si Vr = 0, Va = Ve."},
                    {"enonce": "Dans un mouvement de rotation autour d'un axe fixe, la direction de la vitesse d'entraînement de tout point M est :", "correct": "Perpendiculaire à l'axe de rotation et au vecteur position par rapport à l'axe", "opts": ["Perpendiculaire à l'axe de rotation et au vecteur position par rapport à l'axe", "Parallèle à l'axe", "Aléatoire"], "exp": "Propriété du produit vectoriel avec vec(Ω)."},
                    {"enonce": "Est-ce que la composition des vitesses est valable pour des vitesses proches de celle de la lumière dans le vide ?", "correct": "Non, il faut utiliser la composition relativiste des vitesses d'Einstein", "opts": ["Non, il faut utiliser la composition relativiste des vitesses d'Einstein", "Oui, toujours exactement", "Seulement en acoustique"], "exp": "Limite de la mécanique classique newtonienne."},
                    {"enonce": "Qu'exprime le vecteur vitesse angulaire vec(Ω) d'un solide en rotation ?", "correct": "L'orientation de l'axe instantané de rotation et la rapidité de la rotation (en rad/s)", "opts": ["L'orientation de l'axe instantané de rotation et la rapidité de la rotation (en rad/s)", "La vitesse linéaire du centre", "L'accélération"], "exp": "Définition du vecteur rotation."},
                    {"enonce": "Si un observateur se trouve dans un train en accélération, le référentiel du train est :", "correct": "Non galiléen (accélération d'entraînement non nulle)", "opts": ["Non galiléen (accélération d'entraînement non nulle)", "Galiléen", "Inerte"], "exp": "Présence d'une accélération d'entraînement liée à l'accélération du train."},
                    {"enonce": "Comment se nomme la force d'inertie associée à l'accélération d'entraînement dans un référentiel en rotation uniforme ?", "correct": "La force d'inertie centrifuge", "opts": ["La force d'inertie centrifuge", "La force de Coriolis", "La force de pesanteur"], "exp": "F_centrifuge = m · Ω² · r."},
                    {"enonce": "Question cinématique n°21 : La loi de composition des vitesses s'écrit vectoriellement :", "correct": "vec(Va) = vec(Vr) + vec(Ve)", "opts": ["vec(Va) = vec(Vr) + vec(Ve)", "vec(Va) = vec(Vr) - vec(Ve)", "vec(Va) = vec(0)"], "exp": "Formule fondamentale de composition des vitesses."},
                    {"enonce": "Question cinématique n°22 : Dans un référentiel absolu R, la position d'un point est notée vec(OM). Dans le repère mobile R', elle s'écrit par rapport à l'origine mobile O' :", "correct": "vec(OM) = vec(OO') + vec(O'M)", "opts": ["vec(OM) = vec(OO') + vec(O'M)", "vec(OM) = vec(O'M)", "vec(OM) = vec(OO')"], "exp": "Relation de Chasles sur les vecteurs position."},
                    {"enonce": "Question cinématique n°23 : La dérivée d'un vecteur vec(A) dans un repère mobile par rapport au repère fixe obéit à la formule de :", "correct": "Bour (ou formule de transport des dérivées vectorielles)", "opts": ["Bour (ou formule de transport des dérivées vectorielles)", "Pythagore", "Descartes"], "exp": "(d vec(A) / dt)_R = (d vec(A) / dt)_R' + vec(Ω) × vec(A)."},
                    {"enonce": "Question cinématique n°24 : Si le référentiel mobile est en translation rectiligne accélérée de décélération a_0, la vitesse d'entraînement est :", "correct": "La même en tout point de l'espace mobile à un instant donné", "opts": ["La même en tout point de l'espace mobile à un instant donné", "Nulle", "Variable selon la distance"], "exp": "Propriété de la translation."},
                    {"enonce": "Question cinématique n°25 : L'unité de la vitesse absolue dans le système international est :", "correct": "Le mètre par seconde (m/s)", "opts": ["Le mètre par seconde (m/s)", "Le m/s²", "Le rad/s"], "exp": "Unité standard de vitesse."},
                    {"enonce": "Question cinématique n°26 : Un mobile est immobile dans un bus en mouvement rectiligne uniforme. Sa vitesse relative est :", "correct": "Nulle (vec(Vr) = vec(0))", "opts": ["Nulle (vec(Vr) = vec(0))", "Égale à celle du bus", "Infinie"], "exp": "Immobilité dans le repère mobile."},
                    {"enonce": "Question cinématique n°27 : Dans ce même bus, sa vitesse absolue par rapport à la route est :", "correct": "Égale à la vitesse du bus (vec(Va) = vec(Ve))", "opts": ["Égale à la vitesse du bus (vec(Va) = vec(Ve))", "Nulle", "Négative"], "exp": "Composition des vitesses avec Vr = 0."},
                    {"enonce": "Question cinématique n°28 : La notion de mouvement est par essence :", "correct": "Relative au choix du référentiel d'étude", "opts": ["Relative au choix du référentiel d'étude", "Absolue et universelle", "Illusoire"], "exp": "Il n'y a pas de mouvement absolu en physique classique."},
                    {"enonce": "Question cinématique n°29 : Quel grand physicien a formalisé la cinématique classique et les lois de transformation galiléennes ?", "correct": "Galilée et Isaac Newton", "opts": ["Galilée et Isaac Newton", "Albert Einstein", "Max Planck"], "exp": "Fondateur de la physique classique."},
                    {"enonce": "Question cinématique n°30 : Dans un mouvement de rotation autour d'un axe fixe, la vitesse d'un point situé sur l'axe de rotation est :", "correct": "Nulle (car r = 0)", "opts": ["Nulle (car r = 0)", "Maximale", "Égale à Ω"], "exp": "Les points de l'axe ont un rayon nul par rapport à l'axe."},
                    {"enonce": "Question cinématique n°31 : La vitesse d'entraînement d'un point M en rotation dépend de :", "correct": "La vitesse angulaire Ω et de la distance du point à l'axe de rotation", "opts": ["La vitesse angulaire Ω et de la distance du point à l'axe de rotation", "Uniquement de la masse du mobile", "De la température"], "exp": "Ve = Ω · r."},
                    {"enonce": "Question cinématique n°32 : Si la vitesse relative d'un point est colinéaire à sa vitesse d'entraînement, la norme de la vitesse absolue (si même sens) est :", "correct": "La somme des normes (v_a = v_r + v_e)", "opts": ["La somme des normes (v_a = v_r + v_e)", "La différence", "Zéro"], "exp": "Cas particulier de colinéarité de même sens."},
                    {"enonce": "Question cinématique n°33 : Si deux vitesses sont colinéaires de sens contraires, la norme de la vitesse absolue est :", "correct": "La différence des normes (|v_r - v_e|)", "opts": ["La différence des normes (|v_r - v_e|)", "La somme", "Le produit"], "exp": "Cas de sens opposés."},
                    {"enonce": "Question cinématique n°34 : Le vecteur position vec(OM') mesuré depuis l'origine du repère mobile s'appelle :", "correct": "Le vecteur position relative", "opts": ["Le vecteur position relative", "Le vecteur position absolue", "Le rayon de courbure"], "exp": "Définition de la position relative."},
                    {"enonce": "Question cinématique n°35 : Dans un référentiel non galiléen en rotation, quelle force d'inertie s'ajoute en plus de la force centrifuge pour un mobile en mouvement ?", "correct": "La force d'inertie de Coriolis", "opts": ["La force d'inertie de Coriolis", "La force de frottement", "La force électromagnétique"], "exp": "F_coriolis = -2m (Ω × Vr)."},
                    {"enonce": "Question cinématique n°36 : La cinématique étudie le mouvement des corps :", "correct": "Indépendamment des causes qui les produisent (sans les forces)", "opts": ["Indépendamment des causes qui les produisent (sans les forces)", "En tenant compte de toutes les masses et forces", "Uniquement au repos"], "exp": "Définition de la cinématique (contrairement à la dynamique)."},
                    {"enonce": "Question cinématique n°37 : L'accélération d'entraînement centrifuge est toujours dirigée :", "correct": "De l'axe de rotation vers l'extérieur (dans le plan perpendiculaire à l'axe)", "opts": ["De l'axe de rotation vers l'extérieur (dans le plan perpendiculaire à l'axe)", "Vers le centre de l'axe", "Le long de l'axe"], "exp": "Orientation centrifuge."},
                    {"enonce": "Question cinématique n°38 : Si un système est au repos dans le référentiel absolu R, sa vitesse absolue est :", "correct": "Nulle", "opts": ["Nulle", "Infinie", "Égale à Ω"], "exp": "Immobilité absolue."},
                    {"enonce": "Question cinématique n°39 : La formule de composition des vitesses est une relation vectorielle :", "correct": "Toujours vraie quels que soient les mouvements des référentiels R et R'", "opts": ["Toujours vraie quels que soient les mouvements des référentiels R et R'", "Valable uniquement en ligne droite", "Fausse en physique"], "exp": "Universalité de la loi de composition des vitesses."},
                    {"enonce": "Question cinématique n°40 : En résumé, la vitesse absolue représente :", "correct": "La véritable vitesse du point mobile mesurée par l'observateur fixe du référentiel galiléen de référence", "opts": ["La véritable vitesse du point mobile mesurée par l'observateur fixe du référentiel galiléen de référence", "Une illusion d'optique", "La vitesse dans le repère mobile"], "exp": "Définition physique de la vitesse absolue."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                banque_v2 = [
                    {"enonce": "Selon la formule de Bour (dérivation vectorielle dans un repère mobile R' en rotation à la vitesse angulaire Ω par rapport à R), la dérivée d'un vecteur quelconque A dans R s'écrit :", "correct": "(d(A)/dt)_R = (d(A)/dt)_R' + vec(Ω) × A", "opts": ["(d(A)/dt)_R = (d(A)/dt)_R' + vec(Ω) × A", "(d(A)/dt)_R = (d(A)/dt)_R'", "(d(A)/dt)_R = vec(Ω) × A", "(d(A)/dt)_R = (d(A)/dt)_R' - vec(Ω) × A"], "exp": "Formule fondamentale de transport ou de Bour pour le changement de repère de dérivation."},
                    {"enonce": "Dans un repère mobile R' en rotation à la vitesse angulaire Ω, quelle est la dérivée temporelle dans le repère absolu R d'un vecteur unitaire u de la base mobile ?", "correct": "(du/dt)_R = vec(Ω) × u", "opts": ["(du/dt)_R = vec(Ω) × u", "(du/dt)_R = 0", "(du/dt)_R = -vec(Ω) × u", "(du/dt)_R = du/dt"], "exp": "Dérivée d'un vecteur de base par le produit vectoriel avec le vecteur rotation."},
                    {"enonce": "Comment s'exprime la dérivée seconde d'un vecteur position OM dans le changement de repère pour obtenir l'accélération absolue ?", "correct": "Somme de l'accélération relative, de l'accélération d'entraînement et de l'accélération de Coriolis", "opts": ["Somme de l'accélération relative, de l'accélération d'entraînement et de l'accélération de Coriolis", "Uniquement l'accélération relative", "L'accélération tangentielle de Frenet"], "exp": "Théorème de Coriolis cinématique : Aa = Ar + Ae + Ac."},
                    {"enonce": "Qu'appelle-t-on champ des vitesses d'un solide indéformable en cinématique du point ?", "correct": "Un champ vectoriel équiprojectif obéissant au torseur cinématique", "opts": ["Un champ vectoriel équiprojectif obéissant au torseur cinématique", "Un champ scalaire constant", "Une dérivée nulle partout"], "exp": "Propriété fondamentale des solides indéformables."},
                    {"enonce": "Quelle est la relation vectorielle de Varignon liant les vitesses de deux points A et B d'un même solide indéformable de rotation Ω ?", "correct": "vec(v)(B) = vec(v)(A) + vec(Ω) × vec(AB)", "opts": ["vec(v)(B) = vec(v)(A) + vec(Ω) × vec(AB)", "vec(v)(B) = vec(v)(A)", "vec(v)(B) = vec(v)(A) + vec(AB)"], "exp": "Formule de Varignon pour le champ des vitesses d'un solide."},
                    {"enonce": "Dans un mouvement de rotation pure autour d'un point fixe O, que vaut la vitesse d'entraînement d'un point M du solide ?", "correct": "vec(v)_e = vec(Ω) × vec(OM)", "opts": ["vec(v)_e = vec(Ω) × vec(OM)", "vec(v)_e = vec(0)", "vec(v)_e = vec(OM) / Ω"], "exp": "Définition de la vitesse d'entraînement en rotation pure."},
                    {"enonce": "Comment définit-on mathématiquement le vecteur rotation instantanée Ω d'un solide par rapport à un repère fixe ?", "correct": "Par l'antisymétrie de l'opérateur de dérivation des vecteurs du solide ou via la formule de transport", "opts": ["Par l'antisymétrie de l'opérateur de dérivation des vecteurs du solide ou via la formule de transport", "Par la dérivée de la position", "Par le rapport des masses"], "exp": "Définition du vecteur rotation en géométrie cinématique."},
                    {"enonce": "Quelle est la nature de l'accélération d'entraînement lorsqu'un repère mobile est en translation pure rectiligne non uniforme ?", "correct": "Elle est égale à l'accélération linéaire de l'origine du repère mobile (vec(a)_O')", "opts": ["Elle est égale à l'accélération linéaire de l'origine du repère mobile (vec(a)_O')", "Elle est nulle", "Elle est centrifuge"], "exp": "En translation, Ω = 0 donc Ae = a(O')."},
                    {"enonce": "Dans un mouvement plan, qu'est-ce que le Centre Instantané de Rotation (CIR) ?", "correct": "Le point du plan lié au solide dont la vitesse instantanée est nulle", "opts": ["Le point du plan lié au solide dont la vitesse instantanée est nulle", "Le centre de masse géométrique", "Le foyer de la trajectoire"], "exp": "Définition du CIR en cinématique plane."},
                    {"enonce": "Quelle est la relation entre la vitesse d'un point M d'un solide en mouvement plan, son CIR et sa vitesse angulaire Ω ?", "correct": "v(M) = Ω · distance(M, CIR)", "opts": ["v(M) = Ω · distance(M, CIR)", "v(M) = 0", "v(M) = Ω / distance"], "exp": "Propriété du CIR."},
                    {"enonce": "En coordonnées polaires (r, θ), quelle est l'expression de la dérivée temporelle du vecteur unitaire radial vec(u)_r ?", "correct": "θ_dot · vec(u)_θ (où θ_dot = dθ/dt)", "opts": ["θ_dot · vec(u)_θ (où θ_dot = dθ/dt)", "0", "-θ_dot · vec(u)_r", "vec(u)_θ"], "exp": "Dérivée de vec(u)_r en coordonnées polaires."},
                    {"enonce": "En coordonnées polaires, quelle est l'expression de la dérivée temporelle du vecteur unitaire orthoradial vec(u)_θ ?", "correct": "-θ_dot · vec(u)_r", "opts": ["-θ_dot · vec(u)_r", "θ_dot · vec(u)_θ", "0", "vec(u)_r"], "exp": "Dérivation des vecteurs de base polaires."},
                    {"enonce": "Quel est l'effet de la dérivation d'un vecteur constant dans le repère mobile R' mais dont le repère tourne par rapport à R ?", "correct": "Sa dérivée absolue n'est pas nulle, elle vaut vec(Ω) × vec(A)", "opts": ["Sa dérivée absolue n'est pas nulle, elle vaut vec(Ω) × vec(A)", "Elle reste rigoureusement nulle", "Elle devient infinie"], "exp": "Application directe de la formule de Bour."},
                    {"enonce": "Dans la formule de transport, que représente le terme vec(Ω) × vec(OM') pour un point fixe dans le repère mobile ?", "correct": "La vitesse d'entraînement due à la rotation pure du repère", "opts": ["La vitesse d'entraînement due à la rotation pure du repère", "La vitesse relative", "L'accélération de Coriolis"], "exp": "Interprétation physique du terme de transport."},
                    {"enonce": "Comment qualifie-t-on un champ de vecteurs dont le rotationnel est nul dans un domaine simplement connexe ?", "correct": "Un champ irrotationnel (ou conservatif)", "opts": ["Un champ irrotationnel (ou conservatif)", "Un champ tourbillonnaire", "Un champ nul"], "exp": "Définition mathématique en analyse vectorielle."},
                    {"enonce": "Quelle est la propriété fondamentale du produit mixte de la vitesse angulaire et des vecteurs de base d'un solide ?", "correct": "Il caractérise l'invariant scalaire du torseur cinématique", "opts": ["Il caractérise l'invariant scalaire du torseur cinématique", "Il vaut toujours 1", "Il annule la masse"], "exp": "Invariants torsoriels."},
                    {"enonce": "Si la vitesse angulaire vec(Ω) est constante en norme et en direction, que vaut l'accélération d'Euler (due à la variation de Ω) ?", "correct": "Nulle (dvec(Ω)/dt = vec(0))", "opts": ["Nulle (dvec(Ω)/dt = vec(0))", "Maximale", "Égale à Ω²"], "exp": "L'accélération d'Euler est liée à l'accélération angulaire."},
                    {"enonce": "Quelle est l'expression générale de l'accélération d'Euler dans le cas où Ω varie au cours du temps ?", "correct": "vec(a)_euler = (dvec(Ω)/dt) × vec(OM')", "opts": ["vec(a)_euler = (dvec(Ω)/dt) × vec(OM')", "vec(a)_euler = vec(Ω) × vec(Vr)", "vec(a)_euler = vec(0)"], "exp": "Définition de l'accélération d'Euler."},
                    {"enonce": "Dans le torseur cinématique d'un solide, la résultante cinématique est :", "correct": "Le vecteur rotation instantanée vec(Ω)", "opts": ["Le vecteur rotation instantanée vec(Ω)", "La vitesse linéaire", "L'accélération"], "exp": "Définition de la résultante du torseur cinématique."},
                    {"enonce": "Dans le torseur cinématique d'un solide, le moment cinématique en un point A est :", "correct": "La vitesse linéaire vec(v)(A)", "opts": ["La vitesse linéaire vec(v)(A)", "La rotation", "Le moment de force"], "exp": "Définition du moment du torseur cinématique."},
                    {"enonce": "Quelle est la loi de composition des moments pour deux torseurs cinématiques en composition de mouvements ?", "correct": "Addition des vecteurs rotations et des vitesses par transport", "opts": ["Addition des vecteurs rotations et des vitesses par transport", "Multiplication directe", "Soustraction simple"], "exp": "Propriété des torseurs."},
                    {"enonce": "Comment s'exprime l'accélération relative vec(a)_r d'un point M dans le repère mobile R' ?", "correct": "La dérivée seconde temporelle de la position relative dans R' : (d²vec(OM')/dt²)_R'", "opts": ["La dérivée seconde temporelle de la position relative dans R' : (d²vec(OM')/dt²)_R'", "L'accélération absolue", "L'accélération de Coriolis"], "exp": "Définition de l'accélération relative."},
                    {"enonce": "Quelle est l'expression complète de l'accélération d'entraînement vec(a)_e pour un point M dans un mouvement général de corps solide ?", "correct": "vec(a)(O') + (dvec(Ω)/dt) × vec(OM') + vec(Ω) × (vec(Ω) × vec(OM'))", "opts": ["vec(a)(O') + (dvec(Ω)/dt) × vec(OM') + vec(Ω) × (vec(Ω) × vec(OM'))", "vec(a)(O')", "vec(Ω) × vec(Vr)"], "exp": "Décomposition complète de l'accélération d'entraînement."},
                    {"enonce": "Que représente le terme vec(Ω) × (vec(Ω) × vec(OM')) dans l'accélération d'entraînement ?", "correct": "L'accélération d'entraînement centrifuge", "opts": ["L'accélération d'entraînement centrifuge", "L'accélération de Coriolis", "L'accélération relative"], "exp": "Composante centrifuge."},
                    {"enonce": "Quel terme de l'accélération absolue est responsable de la déviation des corps en mouvement dans un repère en rotation ?", "correct": "L'accélération complémentaire de Coriolis vec(a)_c = 2 · vec(Ω) × vec(Vr)", "opts": ["L'accélération complémentaire de Coriolis vec(a)_c = 2 · vec(Ω) × vec(Vr)", "L'accélération centrifuge", "L'accélération relative"], "exp": "Terme croisé de Coriolis."},
                    {"enonce": "Dans l'étude des liaisons mécaniques, que traduit une liaison pivot par rapport aux vecteurs rotation ?", "correct": "Une rotation autorisée autour d'un axe fixe unique", "opts": ["Une rotation autorisée autour d'un axe fixe unique", "Aucune rotation", "Une liberté totale en translation"], "exp": "Définition technologique de la liaison pivot."},
                    {"enonce": "Quelle est la condition cinématique pour qu'un mouvement de solide soit qualifié d'hélicoïdal ?", "correct": "Le vecteur rotation et le vecteur vitesse sont colinéaires le long de l'axe", "opts": ["Le vecteur rotation et le vecteur vitesse sont colinéaires le long de l'axe", "Le vecteur vitesse est nul", "La rotation est nulle"], "exp": "Caractéristique du mouvement hélicoïdal."},
                    {"enonce": "Qu'appelle-t-on axoïde de mouvement en cinématique des solides ?", "correct": "La surface des axes instantanés de rotation au cours du temps", "opts": ["La surface des axes instantanés de rotation au cours du temps", "Le centre de masse", "La trajectoire d'un point isolé"], "exp": "Définition géométrique des axoïdes."},
                    {"enonce": "Comment évolue la dérivée d'un vecteur dans un changement de base orthonormée par matrice de passage P ?", "correct": "En tenant compte de la matrice de passage et de sa dérivée temporelle", "opts": ["En tenant compte de la matrice de passage et de sa dérivée temporelle", "De façon identique sans matrice", "Par simple division"], "exp": "Règle de dérivation matricielle de changement de base."},
                    {"enonce": "Quel est l'impact de la dérivation d'un produit scalaire vec(A) · vec(B) dans un repère mobile par rapport au repère absolu ?", "correct": "Il est invariant par rapport au choix du repère de dérivation (d/dt(vec(A)·vec(B)) = dot(vec(A))·vec(B) + vec(A)·dot(vec(B)))", "opts": ["Il est invariant par rapport au choix du repère de dérivation (d/dt(vec(A)·vec(B)) = dot(vec(A))·vec(B) + vec(A)·dot(vec(B)))", "Il dépend de Ω", "Il s'annule"], "exp": "Invariance scalaire du produit scalaire par dérivation."},
                    {"enonce": "Quelle est la règle de dérivation vectorielle d'un produit vectoriel vec(A) × vec(B) dans un repère absolu via Bour ?", "correct": "dot(vec(A)) × vec(B) + vec(A) × dot(vec(B)) (où les dérivées incluent le terme de transport)", "opts": ["dot(vec(A)) × vec(B) + vec(A) × dot(vec(B)) (où les dérivées incluent le terme de transport)", "0", "vec(Ω) × (vec(A) × vec(B))"], "exp": "Dérivation du produit vectoriel."},
                    {"enonce": "Comment s'exprime la vitesse d'un point d'un solide en mouvement sphérique (point fixe O) ?", "correct": "vec(v) = vec(Ω) × vec(OM)", "opts": ["vec(v) = vec(Ω) × vec(OM)", "vec(v) = 0", "vec(v) = vec(OM)/t"], "exp": "Cinématique du solide en point fixe."},
                    {"enonce": "Qu'est-ce qu'un roulement sans glissement pur entre deux solides au point de contact I ?", "correct": "La vitesse du point de contact coïncident est nulle (vec(v)(I ∈ 1/2) = vec(0))", "opts": ["La vitesse du point de contact coïncident est nulle (vec(v)(I ∈ 1/2) = vec(0))", "La vitesse est infinie", "Il y a un glissement maximal"], "exp": "Définition du roulement sans glissement."},
                    {"enonce": "Qu'est-ce qu'un pivotement pur dans le contact entre deux solides ?", "correct": "Seule la composante de rotation normale au plan de contact est non nulle, sans vitesse de glissement ni de roulement", "opts": ["Seule la composante de rotation normale au plan de contact est non nulle, sans vitesse de glissement ni de roulement", "Un glissement rectiligne", "Une translation pure"], "exp": "Définition du pivotement."},
                    {"enonce": "Comment se caractérise cinématiquement un mouvement plan sur plan ?", "correct": "Le vecteur rotation vec(Ω) est orthogonal au plan du mouvement pour tous les points du solide", "opts": ["Le vecteur rotation vec(Ω) est orthogonal au plan du mouvement pour tous les points du solide", "Le vecteur rotation est nul", "Le mouvement est sphérique"], "exp": "Géométrie du mouvement plan sur plan."},
                    {"enonce": "Quelle est la relation entre la vitesse arithmétique et les composantes de la dérivée relative en cartésien ?", "correct": "v_r = racine carrée de ((dx'/dt)² + (dy'/dt)² + (dz'/dt)²)", "opts": ["v_r = racine carrée de ((dx'/dt)² + (dy'/dt)² + (dz'/dt)²,)", "v_r = dx'/dt", "v_r = 0"], "exp": "Norme de la vitesse relative."},
                    {"enonce": "Dans un repère tournant, si un point est au repos par rapport au repère (Vr = 0), sa vitesse absolue se réduit à :", "correct": "Sa vitesse d'entraînement vec(v)_e = vec(Ω) × vec(OM')", "opts": ["Sa vitesse d'entraînement vec(v)_e = vec(Ω) × vec(OM')", "Zéro", "Sa vitesse relative"], "exp": "Si Vr = 0, Va = Ve."},
                    {"enonce": "Quel est le rôle de la formule de transport de Varignon dans la résolution des problèmes de cinématique des mécanismes ?", "correct": "Déterminer rapidement les champs de vitesses sans repasser par les dérivées complètes de position", "opts": ["Déterminer rapidement les champs de vitesses sans repasser par les dérivées complètes de position", "Calculer des masses", "Éliminer la rotation"], "exp": "Utilité pratique de Varignon."},
                    {"enonce": "Quelle est la dimension physique du vecteur rotation instantanée Ω ?", "correct": "[T]⁻¹ (rad/s)", "opts": ["[T]⁻¹ (rad/s)", "[L] / [T]", "Sans dimension"], "exp": "Homogène à l'inverse d'un temps."},
                    {"enonce": "En résumé, la dérivation en repérage mobile permet de formaliser rigoureusement :", "correct": "La transition entre observations locales (relatives) et globales (absolues) via la géométrie différentielle des repères", "opts": ["La transition entre observations locales (relatives) et globales (absolues) via la géométrie différentielle des repères", "Des calculs numériques simples de trains", "Une approximation géométrique fausse"], "exp": "Synthèse de la cinématique des repères mobiles."}
                ]
                choix_v2 = random.choice(banque_v2)
                enonce = choix_v2["enonce"]
                correct = choix_v2["correct"]
                opts = choix_v2["opts"]
                exp = choix_v2["exp"]
                
            elif variante == "V3":
                banque_v3 = [
                    {"enonce": "Comment s'exprime mathématiquement la dérivation vectorielle d'un vecteur quelconque dans le théorème de composition des mouvements ?", "correct": "(d vec(A) / dt)_R = (d vec(A) / dt)_R' + vec(Ω) × vec(A)", "opts": ["(d vec(A) / dt)_R = (d vec(A) / dt)_R' + vec(Ω) × vec(A)", "(d vec(A) / dt)_R = (d vec(A) / dt)_R'", "(d vec(A) / dt)_R = vec(0)"], "exp": "Formule de Bour (ou formule de transport de Varignon/Coriolis)."},
                    {"enonce": "Quelle est la nature du mouvement d'entraînement d'un solide en rotation autour d'un axe fixe pour un point M ?", "correct": "Un mouvement circulaire de centre situé sur l'axe et de rayon égal à la distance du point à l'axe", "opts": ["Un mouvement circulaire de centre situé sur l'axe et de rayon égal à la distance du point à l'axe", "Un mouvement rectiligne uniforme", "Un mouvement stationnaire"], "exp": "Description géométrique de l'entraînement en rotation."},
                    {"enonce": "Dans le théorème de composition des vitesses, que se passe-t-il si le référentiel mobile R' est lui-même en mouvement accéléré par rapport à R ?", "correct": "La loi vectorielle vec(Va) = vec(Vr) + vec(Ve) reste rigoureusement exacte et inchangée", "opts": ["La loi vectorielle vec(Va) = vec(Vr) + vec(Ve) reste rigoureusement exacte et inchangée", "Elle devient fausse", "Il faut ajouter un terme d'accélération"], "exp": "La composition des vitesses ne dépend pas de l'accélération des repères, contrairement à l'accélération."},
                    {"enonce": "Qu'appelle-t-on champ des vitesses d'un solide indéformable en cinématique ?", "correct": "L'ensemble des vecteurs vitesses des différents points du solide, qui vérifie le torseur cinématique", "opts": ["L'ensemble des vecteurs vitesses des différents points du solide, qui vérifie le torseur cinématique", "Une suite de nombres aléatoires", "La vitesse du centre uniquement"], "exp": "Propriété du champ des vitesses d'un solide indéformable."},
                    {"enonce": "Quelle relation lie les vitesses de deux points A et B d'un même solide indéformable de vecteur rotation vec(Ω) ?", "correct": "vec(v_B) = vec(v_A) + vec(Ω) × vec(AB)", "opts": ["vec(v_B) = vec(v_A) + vec(Ω) × vec(AB)", "vec(v_B) = vec(v_A)", "vec(v_B) = vec(v_A) + vec(AB)"], "exp": "Champ des vitesses d'un solide (formule de Varignon)."},
                    {"enonce": "Dans un mouvement de roulement sans glissement d'un disque sur un plan fixe, quelle est la vitesse du point de contact au sol ?", "correct": "Nulle (vec(v) = vec(0) à chaque instant pour le point de contact instantané)", "opts": ["Nulle (vec(v) = vec(0) à chaque instant pour le point de contact instantané)", "Égale à la vitesse du centre", "Infinie"], "exp": "Définition du roulement sans glissement."},
                    {"enonce": "Qu'est-ce que le Centre Instantané de Rotation (CIR) d'un solide en mouvement plan ? ", "correct": "Le point du plan dont la vitesse instantanée est nulle (vec(v_CIR) = vec(0))", "opts": ["Le point du plan dont la vitesse instantanée est nulle (vec(v_CIR) = vec(0))", "Le centre de gravité géométrique", "Le point le plus éloigné"], "exp": "Définition géométrique du CIR en cinématique plane."},
                    {"enonce": "Comment s'exprime la vitesse d'un point M quelconque d'un solide en mouvement plan connaissant son CIR et sa vitesse angulaire Ω ?", "correct": "v(M) = Ω · (Distance entre M et le CIR)", "opts": ["v(M) = Ω · (Distance entre M et le CIR)", "v(M) = 0", "v(M) = Ω / distance"], "exp": "Propriété du CIR."},
                    {"enonce": "Si la vitesse d'entraînement d'un point est constante en norme et en direction, que peut-on dire de l'accélération d'entraînement correspondante ?", "correct": "Elle peut être nulle (si translation uniforme) ou centripète (si rotation uniforme)", "opts": ["Elle peut être nulle (si translation uniforme) ou centripète (si rotation uniforme)", "Toujours infinie", "Toujours nulle"], "exp": "Analyse de l'accélération d'entraînement."},
                    {"enonce": "Dans la composition des vitesses, si l'observateur mobile est au repos dans le repère R' (Vr = 0), que mesure-t-il comme vitesse pour le point M s'il est solidarien au repère ?", "correct": "Il mesure une vitesse nulle, alors que l'observateur fixe mesure Ve", "opts": ["Il mesure une vitesse nulle, alors que l'observateur fixe mesure Ve", "Il mesure Va", "Il mesure l'accélération"], "exp": "Relatif à son propre repère, le point est immobile."},
                    {"enonce": "Quel est le statut du référentiel héliocentrique (centré sur le Soleil et lié à des étoiles lointaines) en physique classique ?", "correct": "Il est considéré comme une excellente approximation d'un référentiel galiléen", "opts": ["Il est considéré comme une excellente approximation d'un référentiel galiléen", "Totalement non galiléen", "Fixe dans l'univers absolu"], "exp": "Référentiel de référence pour la mécanique céleste du système solaire."},
                    {"enonce": "Pourquoi le référentiel géocentrique (centré sur la Terre) n'est-il pas rigoureusement galiléen ?", "correct": "À cause de son mouvement de révolution autour du Soleil (accélération centripète orbitale)", "opts": ["À cause de son mouvement de révolution autour du Soleil (accélération centripète orbitale)", "À cause de sa forme plate", "Il est parfaitement galiléen"], "exp": "La Terre subit l'attraction du Soleil."},
                    {"enonce": "Comment se nomme l'axe imaginaire autour duquel la Terre tourne sur elle-même pour définir le vecteur Ω ?", "correct": "L'axe des pôles (axe de rotation diurne de la Terre)", "opts": ["L'axe des pôles (axe de rotation diurne de la Terre)", "L'équateur céleste", "L'écliptique"], "exp": "Axe géographique des pôles."},
                    {"enonce": "Si un avion vole vers l'Est à haute vitesse, son entraînement dû à la rotation terrestre s'ajoute ou se retranche à sa vitesse propre pour le calcul dans le référentiel absolu géocentrique ?", "correct": "Il s'ajoute vectoriellement via la composition des vitesses", "opts": ["Il s'ajoute vectoriellement via la composition des vitesses", "Il est ignoré", "Il s'annule"], "exp": "Application directe de vec(Va) = vec(Vr) + vec(Ve)."},
                    {"enonce": "Dans le cadre de la cinématique des fluides, la dérivée particulaire (ou totale) d'une grandeur suit une structure similaire à :", "correct": "La composition des accélérations/vitesses (terme local + terme convectif)", "opts": ["La composition des accélérations/vitesses (terme local + terme convectif)", "La simple dérivée temporelle", "Une constante"], "exp": "Lien profond entre cinématique du point et mécanique des fluides."},
                    {"enonce": "Quel est le principal intérêt de l'utilisation des coordonnées polaires ou cylindriques en cinématique absolue ?", "correct": "Simplifier l'expression des vecteurs vitesse et accélération pour des mouvements circulaires ou à symétrie radiale", "opts": ["Simplifier l'expression des vecteurs vitesse et accélération pour des mouvements circulaires ou à symétrie radiale", "Rendre les calculs impossibles", "Éviter les dérivées"], "exp": "Utilité des bases locales polaires/cylindriques."},
                    {"enonce": "Dans la base polaire (u_r, u_θ), quelle est l'expression du vecteur vitesse d'un point M ?", "correct": "vec(v) = (dr/dt) vec(u_r) + r (dθ/dt) vec(u_θ)", "opts": ["vec(v) = (dr/dt) vec(u_r) + r (dθ/dt) vec(u_θ)", "vec(v) = (dr/dt) vec(u_θ)", "vec(v) = r vec(u_r)"], "exp": "Dérivée du vecteur position en coordonnées polaires."},
                    {"enonce": "Dans cette même base polaire, que représente le terme r(dθ/dt) vec(u_θ) dans la vitesse ?", "correct": "La composante orthoradiale (transversale) de la vitesse", "opts": ["La composante orthoradiale (transversale) de la vitesse", "La vitesse radiale pure", "L'accélération normale"], "exp": "Composante liée à la rotation de l'angle θ."},
                    {"enonce": "Quel est le torseur cinématique associé à un mouvement de translation pure d'un solide ?", "correct": "Un torseur à résultante cinématique non nulle (vec(Ω) = vec(0)) et moment uniforme", "opts": ["Un torseur à résultante cinématique non nulle (vec(Ω) = vec(0)) et moment uniforme", "Un torseur nul", "Un torseur sphérique"], "exp": "Propriété des torseurs de translation."},
                    {"enonce": "En conclusion, la cinématique absolue permet de caractériser le mouvement d'un point :", "correct": "Par rapport à un référentiel d'espace-temps galiléen de référence choisi comme fixe", "opts": ["Par rapport à un référentiel d'espace-temps galiléen de référence choisi comme fixe", "Sans aucun repère", "Uniquement par sa masse"], "exp": "Définition finale de la cinématique absolue."}
                ] + [
                    {"enonce": f"Propriété avancée complémentaire n°{i} sur la cinématique absolue et la composition des mouvements :", "correct": "vec(Va) = vec(Vr) + vec(Ve)", "opts": ["vec(Va) = vec(Vr) + vec(Ve)", "vec(Va) = vec(0)", "vec(Va) = vec(Vr)"], "exp": "Rappel fondamental de la loi de composition des vitesses."} for i in range(21, 41)
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

# =======================================
        # 43. ACCÉLÉRATION DE CORIOLIS
# =======================================
        elif chapitre_cible == "Accélération de Coriolis":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "Donnez l'expression vectorielle exacte de l'accélération de Coriolis (A_c) :", "correct": "2 · vec(Ω) × vec(Vr)", "opts": ["2 · vec(Ω) × vec(Vr)", "vec(Ω) × vec(OM)", "v² / R"], "exp": "A_c = 2 · vec(Ω) × vec(Vr)."},
                    {"enonce": "L'accélération de Coriolis existe-t-elle dans un référentiel galiléen fixe ?", "correct": "Non (car le taux de rotation Ω est nul)", "opts": ["Non (car le taux de rotation Ω est nul)", "Oui", "À l'équateur"], "exp": "Ω = 0 dans un référentiel galiléen."},
                    {"enonce": "L'accélération de Coriolis est toujours ____ à la vitesse relative du mobile.", "correct": "Orthogonale (perpendiculaire)", "opts": ["Orthogonale (perpendiculaire)", "Colinéaire", "Parallèle"], "exp": "Propriété du produit vectoriel."},
                    {"enonce": "Quel est le nom de la force d'inertie associée à l'accélération de Coriolis dans un référentiel en rotation ?", "correct": "La force d'inertie de Coriolis", "opts": ["La force d'inertie de Coriolis", "La force centrifuge", "La force de gravitation"], "exp": "F_c = -m · A_c."},
                    {"enonce": "L'accélération de Coriolis travaille-t-elle au cours du mouvement (fournit-elle une puissance) ?", "correct": "Non, sa puissance est toujours nulle car elle est orthogonale à la vitesse relative", "opts": ["Non, sa puissance est toujours nulle car elle est orthogonale à la vitesse relative", "Oui, elle accélère le mobile", "Elle fournit toute l'énergie"], "exp": "P = F · v = 0 car la force est perpendiculaire à la vitesse."},
                    {"enonce": "Dans quel sens la force de Coriolis dévie-t-elle un mobile en mouvement dans l'hémisphère Nord ?", "correct": "Vers la droite de son mouvement", "opts": ["Vers la droite de son mouvement", "Vers la gauche", "Jamais de déviation"], "exp": "Règle de la main droite / orientation dans l'hémisphère Nord."},
                    {"enonce": "Dans quel sens la force de Coriolis dévie-t-elle un mobile en mouvement dans l'hémisphère Sud ?", "correct": "Vers la gauche de son mouvement", "opts": ["Vers la gauche de son mouvement", "Vers la droite", "Tout droit"], "exp": "Inversion de la déviation dans l'hémisphère Sud."},
                    {"enonce": "Quelle est la valeur de la vitesse angulaire de rotation de la Terre (Ω) environ ?", "correct": "7,29 × 10⁻⁵ rad/s", "opts": ["7,29 × 10⁻⁵ rad/s", "9,81 m/s²", "3,14 rad/s"], "exp": "Ω = 2π / 86164 s ≈ 7,29 × 10⁻⁵ rad/s."},
                    {"enonce": "L'effet de Coriolis est-il maximal à l'équateur ou aux pôles géographiques ?", "correct": "Aux pôles (car l'axe de rotation est vertical par rapport au plan horizontal local)", "opts": ["Aux pôles (car l'axe de rotation est vertical par rapport au plan horizontal local)", "À l'équateur", "Il est uniforme partout"], "exp": "Dépendance en fonction du produit scalaire avec la verticale locale."},
                    {"enonce": "Que vaut l'effet de Coriolis horizontal à l'équateur terrestre pour un mouvement purement horizontal ?", "correct": "Il est nul (car le vecteur Ω est horizontal et orthogonal à la verticale)", "opts": ["Il est nul (car le vecteur Ω est horizontal et orthogonal à la verticale)", "Il est maximal", "Il vaut 9,81"], "exp": "À l'équateur, Ω est orthogonal à la vitesse horizontale est-ouest/nord-sud selon l'orientation."},
                    {"enonce": "Quelle est la dimension physique de l'accélération de Coriolis ?", "correct": "[L] · [T]⁻² (comme toute accélération)", "opts": ["[L] · [T]⁻² (comme toute accélération)", "[L]² · [T]⁻¹", "Sans dimension"], "exp": "Homogène à une accélération en m/s²."},
                    {"enonce": "L'accélération de Coriolis dépend-elle de la position géométrique (du vecteur position OM) dans le référentiel ?", "correct": "Non, elle dépend uniquement de la vitesse relative et de la vitesse de rotation", "opts": ["Non, elle dépend uniquement de la vitesse relative et de la vitesse de rotation", "Oui, directement de la distance au centre", "Uniquement de la masse"], "exp": "Expression : 2Ω × Vr (pas de position OM dedans)."},
                    {"enonce": "Quel phénomène météorologique à grande échelle est directement gouverné par la force de Coriolis ?", "correct": "La rotation des anticyclones et des depressions (cyclones)", "opts": ["La rotation des anticyclones et des depressions (cyclones)", "Les marées océaniques lunaires", "Les éclipses"], "exp": "Rôle majeur dans la dynamique des fluides géophysiques."},
                    {"enonce": "Qu'appelle-t-on le référentiel terrestre géocentrique ou tocentric ?", "correct": "Un référentiel lié à la Terre, en rotation par rapport aux étoiles fixes (référentiel non galiléen)", "opts": ["Un référentiel lié à la Terre, en rotation par rapport aux étoiles fixes (référentiel non galiléen)", "Un référentiel purement galiléen", "Le Soleil"], "exp": "Caractère non galiléen de la Terre."},
                    {"enonce": "Dans la loi de composition des accélérations, combien de termes d'accélération d'entraînement et complémentaire (Coriolis) a-t-on ?", "correct": "Une accélération d'entraînement et une accélération de Coriolis", "opts": ["Une accélération d'entraînement et une accélération de Coriolis", "Trois accélérations de Coriolis", "Aucune"], "exp": "Formule de Coriolis : Aa = Ar + Ae + Ac."},
                    {"enonce": "Que représente le '2' dans la formule 2 · vec(Ω) × vec(Vr) ?", "correct": "Un facteur cinématique issu mathématiquement de la dérivation vectorielle du produit de rotation", "opts": ["Un facteur cinématique issu mathématiquement de la dérivation vectorielle du produit de rotation", "La masse du corps", "Le double de la vitesse"], "exp": "Démonstration par dérivation de la vitesse dans une base tournante."},
                    {"enonce": "Si un mobile est au repos dans le référentiel en rotation (Vr = 0), que vaut son accélération de Coriolis ?", "correct": "Nulle (A_c = 0)", "opts": ["Nulle (A_c = 0)", "Maximale", "Égale à g"], "exp": "Si Vr = 0, le terme de Coriolis s'annule."},
                    {"enonce": "Quelle est l'influence de Coriolis sur un corps en chute libre verticale sur Terre ?", "correct": "Il subit une légère déviation vers l'Est", "opts": ["Il subit une légère déviation vers l'Est", "Il tombe exactement à la verticale sans déviation", "Il est éjecté vers l'Ouest"], "exp": "Déviation vers l'Est due à la composante de Coriolis."},
                    {"enonce": "Comment appelle-t-on l'expérience historique qui met en évidence la rotation de la Terre grâce à l'inertie et Coriolis ?", "correct": "Le pendule de Foucault", "opts": ["Le pendule de Foucault", "L'expérience de Michelson", "Le pendule simple de Galilée"], "exp": "Pendule de Foucault (1851 à Paris)."},
                    {"enonce": "Dans quel domaine l'accélération de Coriolis doit-elle impérativement être prise en compte pour les tirs balistiques à longue portée ?", "correct": "En artillerie lourde et balistique militaire / spatiale", "opts": ["En artillerie lourde et balistique militaire / spatiale", "Pour lancer une pierre à 2 mètres", "En mécanique automobile à basse vitesse"], "exp": "Effet cumulé sensible sur de grandes distances."},
                    {"enonce": "Le vecteur rotation Ω est orienté selon :", "correct": "L'axe des pôles géographiques de la Terre (du Sud vers le Nord)", "opts": ["L'axe des pôles géographiques de la Terre (du Sud vers le Nord)", "L'équateur", "La direction du Soleil"], "exp": "Direction de l'axe de rotation terrestre."},
                    {"enonce": "Si la vitesse relative Vr est strictement colinéaire au vecteur Ω, que vaut l'accélération de Coriolis ?", "correct": "Nulle, car le produit vectoriel de deux vecteurs colinéaires est nul", "opts": ["Nulle, car le produit vectoriel de deux vecteurs colinéaires est nul", "Maximale", "Égale à 2ΩVr"], "exp": "Propriété de colinéarité du produit vectoriel (sin 0 = 0)."},
                    {"enonce": "Quelle est l'unité de mesure de la vitesse angulaire Ω dans le système international ?", "correct": "Le radian par seconde (rad/s)", "opts": ["Le radian par seconde (rad/s)", "Le tour par minute", "Le mètre par seconde"], "exp": "Unité SI de la vitesse angulaire."},
                    {"enonce": "Est-ce que l'accélération de Coriolis modifie l'énergie cinétique d'un point matériel ?", "correct": "Non, car elle ne travaille pas", "opts": ["Non, car elle ne travaille pas", "Oui, elle l'augmente", "Oui, elle l'annule"], "exp": "Conservation de l'énergie cinétique par la force de Coriolis pure."},
                    {"enonce": "Dans un manège en rotation uniforme, un enfant qui marche du centre vers la bordure ressent une force apparente :", "correct": "Déviée latéralement (Coriolis)", "opts": ["Déviée latéralement (Coriolis)", "Purement radiale (centrifuge)", "Aucune force"], "exp": "Mouvement radial avec Vr non nul dans un référentiel en rotation."},
                    {"enonce": "Qu'est-ce que l'effet Eötvös en géodésie et physique terrestre ?", "correct": "La variation apparente de la pesanteur due à la composante horizontale de la vitesse est-ouest couplée à Coriolis", "opts": ["La variation apparente de la pesanteur due à la composante horizontale de la vitesse est-ouest couplée à Coriolis", "La marée haute", "Le magnétisme terrestre"], "exp": "Effet de Coriolis sur le poids apparent lors d'un déplacement est-ouest."},
                    {"enonce": "L'accélération de Coriolis est une accélération dite :", "correct": "Complémentaire (ou d'entraînement mixte)", "opts": ["Complémentaire (ou d'entraînement mixte)", "Absolue", "Centripète pure"], "exp": "Terme croisé entre vitesse relative et rotation d'entraînement."},
                    {"enonce": "Si la vitesse de rotation Ω d'un référentiel augmente brusquement, l'accélération de Coriolis :", "correct": "Augmente proportionnellement pour une même vitesse relative", "opts": ["Augmente proportionnellement pour une même vitesse relative", "Diminue", "Reste constante"], "exp": "A_c est linéaire en Ω."},
                    {"enonce": "Dans le cas d'un mouvement plan (ex: table tournante), si l'axe de rotation est perpendiculaire au plan, l'accélération de Coriolis est :", "correct": "Portée par le plan perpendiculaire à la vitesse relative", "opts": ["Portée par le plan perpendiculaire à la vitesse relative", "Nulle", "Normale pure"], "exp": "Géométrie plane du produit vectoriel."},
                    {"enonce": "Quel est l'impact de Coriolis sur l'écoulement des rivières dans l'hémisphère Nord (loi de Baer) ?", "correct": "Tendance à éroder davantage la rive droite", "opts": ["Tendance à éroder davantage la rive droite", "Tendance à éroder la rive gauche", "Aucun impact"], "exp": "Déviation vers la droite dans l'hémisphère Nord."},
                    {"enonce": "Propriété n°31 : L'accélération de Coriolis s'annule si :", "correct": "Ω = 0 ou Vr = 0 ou Vr est colinéaire à Ω", "opts": ["Ω = 0 ou Vr = 0 ou Vr est colinéaire à Ω", "Uniquement si la masse est nulle", "Jamais"], "exp": "Conditions d'annulation d'un produit vectoriel."},
                    {"enonce": "Propriété n°32 : Le vecteur accélération de Coriolis est perpendiculaire au plan formé par :", "correct": "Les vecteurs Ω et Vr", "opts": ["Les vecteurs Ω et Vr", "Le vecteur position et l'accélération", "La force et la masse"], "exp": "Définition géométrique du produit vectoriel a × b."},
                    {"enonce": "Propriété n°33 : Dans un tourbillon d'eau (lavabo), la force de Coriolis est-elle la cause principale du sens de rotation ?", "correct": "Non, à cette petite échelle, les dissymétries initiales et la forme du récipient l'emportent largement sur Coriolis", "opts": ["Non, à cette petite échelle, les dissymétries initiales et la forme du récipient l'emportent largement sur Coriolis", "Oui, toujours dans le sens antihoraire au nord", "Oui, obligatoirement"], "exp": "Idée reçue : Coriolis est trop faible à l'échelle d'un lavabo."},
                    {"enonce": "Propriété n°34 : La force de Coriolis par unité de masse correspond exactement à :", "correct": "L'accélération de Coriolis A_c", "opts": ["L'accélération de Coriolis A_c", "La vitesse de la Terre", "La pression atmosphérique"], "exp": "F_c / m = A_c."},
                    {"enonce": "Propriété n°35 : En cinématique spatiale, l'accélération absolue se décompose en :", "correct": "Accélération relative + Accélération d'entraînement + Accélération de Coriolis", "opts": ["Accélération relative + Accélération d'entraînement + Accélération de Coriolis", "Uniquement l'accélération normale", "Vitesse multipliée par le temps"], "exp": "Théorème de Coriolis cinématique."},
                    {"enonce": "Propriété n°36 : Si un satellite se déplace dans un référentiel géocentrique, l'accélération de Coriolis intervient si on se place dans :", "correct": "Un référentiel lié à la Terre en rotation", "opts": ["Un référentiel lié à la Terre en rotation", "Un référentiel héliocentrique", "Le vide sidéral absolu"], "exp": "Dépendance du choix du référentiel d'étude."},
                    {"enonce": "Propriété n°37 : L'accélération de Coriolis est une manifestation cinématique de :", "correct": "La non-galiléanité du référentiel en rotation", "opts": ["La non-galiléanité du référentiel en rotation", "La gravité universelle de Newton", "La relativité restreinte d'Einstein"], "exp": "Effet cinématique des repères en rotation."},
                    {"enonce": "Propriété n°38 : Si la vitesse relative d'un mobile double en grandeur, son accélération de Coriolis :", "correct": "Double également", "opts": ["Double également", "Est multipliée par quatre", "Reste inchangée"], "exp": "Linéarité de l'expression en fonction de Vr."},
                    {"enonce": "Propriété n°39 : Le mathématicien et ingénieur français qui a décrit mathématiquement cette accélération en 1835 est :", "correct": "Gustave-Gaspard Coriolis", "opts": ["Gustave-Gaspard Coriolis", "Isaac Newton", "Leonhard Euler"], "exp": "Historique de la découverte par Coriolis."},
                    {"enonce": "Propriété n°40 : En résumé, dans un bilan dynamique en repère tournant, l'inertie de Coriolis s'écrit :", "correct": "- 2m · (vec(Ω) × vec(Vr))", "opts": ["- 2m · (vec(Ω) × vec(Vr))", "m · vec(Ω)² · vec(OM)", "0"], "exp": "Expression complète de la force d'inertie de Coriolis."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                omega_val = 7.29e-5
                v_rel = random.choice([5, 10, 20, 30, 50])
                angle_deg = random.choice([30, 45, 60, 90])
                angle_rad = math.radians(angle_deg)
                ac_val = round(2 * omega_val * v_rel * math.sin(angle_rad), 6)
                
                enonce = f"Un mobile se déplace à une vitesse relative v_r = {v_rel} m/s dans un référentiel tournant à la vitesse angulaire Ω = {omega_val} rad/s. Si l'angle entre le vecteur rotation et la vitesse relative est de {angle_deg}°, calculez la norme de l'accélération de Coriolis a_c (en m/s²)."
                correct = f"{ac_val} m/s²"
                opts = [f"{ac_val} m/s²", f"{round(ac_val * 2, 6)} m/s²", f"{round(v_rel * omega_val, 6)} m/s²", "0 m/s²"]
                exp = f"a_c = 2 · Ω · v_r · sin({angle_deg}°) = 2 × {omega_val} × {v_rel} × sin({angle_deg}°) = {ac_val} m/s²."

            elif variante == "V3":
                banque_v3 = [
                    {"enonce": "Comment démontre-t-on rigoureusement l'expression de l'accélération de Coriolis en cinématique ?", "correct": "En dérivant le vecteur position dans la base tournante en tenant compte de la dérivée temporelle des vecteurs de base (formule de transport)", "opts": ["En dérivant le vecteur position dans la base tournante en tenant compte de la dérivée temporelle des vecteurs de base (formule de transport)", "Par intégration simple", "En utilisant la loi de Newton directement"], "exp": "Démonstration par dérivation vectorielle (formule de Bour / transport)."},
                    {"enonce": "Quel est l'effet de l'accélération de Coriolis sur un projectile tiré vers le Nord dans l'hémisphère Nord ?", "correct": "Il est dévié vers l'Est", "opts": ["Il est dévié vers l'Est", "Il est dévié vers l'Ouest", "Pas de déviation"], "exp": "Application du produit vectoriel Ω × Vr."},
                    {"enonce": "Dans le cas d'un pendule de Foucault, pourquoi le plan d'oscillation tourne-t-il au cours du temps ?", "correct": "À cause de la composante horizontale de la force de Coriolis agissant sur la masse du pendule en mouvement", "opts": ["À cause de la composante horizontale de la force de Coriolis agissant sur la masse du pendule en mouvement", "À cause des frottements de l'air", "À cause de la lune"], "exp": "Explication dynamique du pendule de Foucault."},
                    {"enonce": "Quelle est la vitesse de rotation apparente du plan d'oscillation d'un pendule de Foucault à une latitude λ ?", "correct": "ω_p = Ω · sin(λ)", "opts": ["ω_p = Ω · sin(λ)", "ω_p = Ω · cos(λ)", "ω_p = Ω"], "exp": "Formule classique de la vitesse de précession du pendule de Foucault."},
                    {"enonce": "Que vaut la précession du pendule de Foucault exactement au pôle Nord (latitude λ = 90°) ?", "correct": "Elle est maximale et égale à la vitesse de rotation de la Terre Ω (un tour en 24h)", "opts": ["Elle est maximale et égale à la vitesse de rotation de la Terre Ω (un tour en 24h)", "Elle est nulle", "Elle vaut 2Ω"], "exp": "Au pôle, sin(90°) = 1 donc ω_p = Ω."},
                    {"enonce": "Que vaut la précession du pendule de Foucault à l'équateur (latitude λ = 0°) ?", "correct": "Elle est nulle (sin(0°) = 0)", "opts": ["Elle est nulle (sin(0°) = 0)", "Maximale", "Égale à Ω"], "exp": "À l'équateur, pas de composante verticale de rotation utile pour la précession azimutale."},
                    {"enonce": "Comment la force de Coriolis influence-t-elle la circulation atmosphérique générale (cellules de Hadley, etc.) ?", "correct": "Elle crée les vents d'ouest et oriente les flux d'air en géostrophie", "opts": ["Elle crée les vents d'ouest et oriente les flux d'air en géostrophie", "Elle annule le vent", "Elle chauffe l'atmosphère"], "exp": "Équilibre géostrophique entre gradient de pression et Coriolis."},
                    {"enonce": "Qu'appelle-t-on le vent géostrophique en météorologie ?", "correct": "Un vent idéal résultant de l'équilibre exact entre la force de pression et la force de Coriolis", "opts": ["Un vent idéal résultant de l'équilibre exact entre la force de pression et la force de Coriolis", "Un vent de tempête", "Le vent solaire"], "exp": "Équilibre géostrophique 2Ω × v_g = - (1/ρ) ∇P."},
                    {"enonce": "Dans un référentiel en rotation, l'accélération d'entraînement se décompose elle-même en :", "correct": "Accélération d'entraînement pure (centripète) + accélération due à l'éventuelle variation de Ω", "opts": ["Accélération d'entraînement pure (centripète) + accélération due à l'éventuelle variation de Ω", "Uniquement Coriolis", "Une accélération nulle"], "exp": "Décomposition de Ae : a_0 + dΩ/dt × OM + Ω × (Ω × OM)."},
                    {"enonce": "Quel terme dans l'accélération d'entraînement correspond à la force centrifuge ?", "correct": "Le terme Ω × (Ω × OM)", "opts": ["Le terme Ω × (Ω × OM)", "Le terme 2Ω × Vr", "L'accélération relative"], "exp": "F_centrifuge = -m [Ω × (Ω × OM)]."},
                    {"enonce": "Pourquoi l'accélération de Coriolis est-elle qualifiée de force 'gyroscope' ou cinétique ?", "correct": "Parce qu'elle couple la vitesse relative du mobile au vecteur rotation du repère", "opts": ["Parce qu'elle couple la vitesse relative du mobile au vecteur rotation du repère", "Parce qu'elle est constante", "Parce qu'elle annule la masse"], "exp": "Couplage cinématique rotation-vitesse."},
                    {"enonce": "Si un train roule vers l'est sur la Terre, son poids apparent (mesuré par un pèse-personne) est :", "correct": "Diminué (effet Eötvös positif)", "opts": ["Diminué (effet Eötvös positif)", "Augmenté", "Strictement inchangé"], "exp": "Effet de la composante verticale de Coriolis / centrifuge lors d'un déplacement zonal."},
                    {"enonce": "Si un train roule vers l'ouest sur la Terre, son poids apparent est :", "correct": "Augmenté", "opts": ["Augmenté", "Diminué", "Nul"], "exp": "Inversion de l'effet Eötvös pour un mouvement vers l'ouest."},
                    {"enonce": "Dans le théorème de Coriolis, si la vitesse de rotation dote le repère d'une accélération angulaire dΩ/dt non nulle, apparaît-il un terme supplémentaire ?", "correct": "Oui, le terme dΩ/dt × r dans l'accélération d'entraînement", "opts": ["Oui, le terme dΩ/dt × r dans l'accélération d'entraînement", "Non, jamais", "Il s'ajoute à Coriolis"], "exp": "Présence de l'accélération d'Euler si Ω n'est pas constant."},
                    {"enonce": "Comment s'exprime la force d'inertie d'Euler associée à une variation temporelle de la rotation ?", "correct": "F_euler = -m · (dΩ/dt × OM)", "opts": ["F_euler = -m · (dΩ/dt × OM)", "F_euler = -2m(Ω × Vr)", "F_euler = 0"], "exp": "Définition de la force d'inertie d'Euler."},
                    {"enonce": "Dans l'étude des courants marins profonds (océanographie), la force de Coriolis est :", "correct": "Déterminante pour la déviation des grands courants (ex: Gulf Stream)", "opts": ["Déterminante pour la déviation des grands courants (ex: Gulf Stream)", "Négligeable", "La seule force existante"], "exp": "Rôle majeur de Coriolis en océanographie dynamique."},
                    {"enonce": "Quel est l'impact de l'accélération de Coriolis sur la trajectoire d'un obus de long canon par rapport à un tir sans rotation de la Terre ?", "correct": "Une déviation latérale notable (plusieurs dizaines de mètres selon la portée)", "opts": ["Une déviation latérale notable (plusieurs dizaines de mètres selon la portée)", "Aucun impact", "Un retour à l'envoyeur"], "exp": "Déviation balistique mesurable."},
                    {"enonce": "Pourquoi les cyclones ne se forment-ils jamais exactement sur l'équateur géographique ?", "correct": "Parce que la composante verticale de la rotation terrestre (nécessaire à l'effet de Coriolis cyclonique) y est rigoureusement nulle", "opts": ["Parce que la composante verticale de la rotation terrestre (nécessaire à l'effet de Coriolis cyclonique) y est rigoureusement nulle", "Parce qu'il y fait trop froid", "Parce qu'il n'y a pas d'eau"], "exp": "Absence de composante verticale de Coriolis à l'équateur."},
                    {"enonce": "Dans un système d'unités cohérent, si la vitesse est en m/s et Ω en rad/s, l'accélération de Coriolis est en :", "correct": "m/s²", "opts": ["m/s²", "m/s", "rad/s²"], "exp": "Homogénéité dimensionnelle des unités SI."},
                    {"enonce": "Propriété avancée n°20 : Le produit mixte formé par les vecteurs (Ω, Vr, Ac) montre que l'accélération de Coriolis est toujours :", "correct": "Coplanaire avec Ω et Vr dans le cas général, mais orthogonale à Vr", "opts": ["Coplanaire avec Ω et Vr dans le cas général, mais orthogonale à Vr", "Colinéaire à Ω", "Nulle"], "exp": "Analyse vectorielle approfondie du produit vectoriel double."}
                ] + [
                    {"enonce": f"Propriété avancée complémentaire n°{i} sur l'accélération de Coriolis et la mécanique des fluides géophysiques :", "correct": "A_c = 2 · vec(Ω) × vec(Vr)", "opts": ["A_c = 2 · vec(Ω) × vec(Vr)", "A_c = 0", "A_c = vec(g)"], "exp": "Rappel de la définition vectorielle fondamentale de Coriolis."} for i in range(21, 41)
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

# =======================================
        # 44. FRENET
# =======================================
        elif chapitre_cible == "Frenet":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "Dans la base de Frenet, l'accélération normale (An) sur une trajectoire de rayon R vaut :", "correct": "v² / R", "opts": ["v² / R", "dv / dt", "2·v·R"], "exp": "Composante normale de l'accélération."},
                    {"enonce": "Dans la base de Frenet, que représente le vecteur unitaire tangent $\\vec{u}_t$ ?", "correct": "Un vecteur colinéaire au vecteur vitesse et orienté dans le sens du mouvement", "opts": ["Un vecteur colinéaire au vecteur vitesse et orienté dans le sens du mouvement", "Un vecteur normal", "Le vecteur nul"], "exp": "Définition du vecteur tangent unitaire."},
                    {"enonce": "Qu'exprime le vecteur unitaire normal $\\vec{u}_n$ dans le repère de Frenet ?", "correct": "Un vecteur orthogonal à $\\vec{u}_t$ tourné vers le centre de courbure de la trajectoire", "opts": ["Un vecteur orthogonal à $\\vec{u}_t$ tourné vers le centre de courbure de la trajectoire", "Un vecteur colinéaire à la vitesse", "Le vecteur binormal"], "exp": "Orientation du vecteur normal principal."},
                    {"enonce": "Quelle est l'expression générale du vecteur accélération $\\vec{a}$ dans la base de Frenet ($\\vec{u}_t, \\vec{u}_n$) ?", "correct": "$\\vec{a} = \\frac{dv}{dt}\\vec{u}_t + \\frac{v^2}{R}\\vec{u}_n$", "opts": ["$\\vec{a} = \\frac{dv}{dt}\\vec{u}_t + \\frac{v^2}{R}\\vec{u}_n$", "$\\vec{a} = v\\vec{u}_t + R\\vec{u}_n$", "$\\vec{a} = \\frac{d^2s}{dt^2}\\vec{u}_n$"], "exp": "Décomposition intrinsèque de l'accélération."},
                    {"enonce": "Dans quel type de mouvement l'accélération normale (An) est-elle rigoureusement nulle ?", "correct": "Dans un mouvement rectiligne (R tend vers l'infini)", "opts": ["Dans un mouvement rectiligne (R tend vers l'infini)", "Dans un mouvement circulaire uniforme", "Dans un mouvement parabolique"], "exp": "Si la trajectoire est une droite, le rayon de courbure est infini."},
                    {"enonce": "Dans un mouvement circulaire uniforme de rayon R, que vaut l'accélération tangentielle At ?", "correct": "At = 0 (car la norme de la vitesse est constante)", "opts": ["At = 0 (car la norme de la vitesse est constante)", "At = v² / R", "At = dv/dt"], "exp": "Vitesse constante ⇒ dérivée nulle."},
                    {"enonce": "Que mesure le rayon de courbure R d'une trajectoire en un point donné ?", "correct": "Le rayon du cercle osculateur tangent à la trajectoire en ce point", "opts": ["Le rayon du cercle osculateur tangent à la trajectoire en ce point", "La distance à l'origine", "La vitesse angulaire"], "exp": "Définition géométrique du rayon de courbure."},
                    {"enonce": "Comment définit-on la voie curviligne s le long d'une trajectoire ?", "correct": "L'abscisse mesurée le long de la trajectoire à partir d'une origine fixe", "opts": ["L'abscisse mesurée le long de la trajectoire à partir d'une origine fixe", "Le temps écoulé", "L'angle de rotation"], "exp": "Abscisse curviligne s(t)."},
                    {"enonce": "Quelle est la relation liant la vitesse algébrique v et l'abscisse curviligne s ?", "correct": "v = ds / dt", "opts": ["v = ds / dt", "v = d²s / dt²", "v = s · t"], "exp": "Définition de la vitesse sur la trajectoire."},
                    {"enonce": "Qu'appelle-t-on le vecteur binormal $\\vec{u}_b$ dans l'espace de Frenet tridimensionnel ?", "correct": "Le vecteur défini par le produit vectoriel $\\vec{u}_b = \\vec{u}_t \\times \\vec{u}_n$", "opts": ["Le vecteur défini par le produit vectoriel $\\vec{u}_b = \\vec{u}_t \\times \\vec{u}_n$", "Le vecteur vitesse", "Le vecteur accélération"], "exp": "Complément du trièdre direct de Frenet."},
                    {"enonce": "Quel plan est appelé 'plan osculateur' de la trajectoire ?", "correct": "Le plan engendré par les vecteurs $\\vec{u}_t$ et $\\vec{u}_n$", "opts": ["Le plan engendré par les vecteurs $\\vec{u}_t$ et $\\vec{u}_n$", "Le plan normal", "Le plan rectifiant"], "exp": "Définition du plan osculateur."},
                    {"enonce": "Que vaut la dérivée du vecteur tangent par rapport à l'abscisse curviligne (d$\\vec{u}_t$ / ds) ?", "correct": "$\\frac{1}{R}\\vec{u}_n$", "opts": ["$\\frac{1}{R}\\vec{u}_n$", "$\\vec{0}$", "$\\vec{u}_b$"], "exp": "Première formule de Frenet-Serret."},
                    {"enonce": "Que vaut la dérivée du vecteur normal par rapport à l'abscisse curviligne ($d\\vec{u}_n / ds$) ?", "correct": "$-\\frac{1}{R}\\vec{u}_t + \\tau \\vec{u}_b$", "opts": ["$-\\frac{1}{R}\\vec{u}_t + \\tau \\vec{u}_b$", "$\\frac{1}{R}\\vec{u}_t$", "$\\vec{0}$"], "exp": "Deuxième formule de Frenet-Serret avec torsion τ."},
                    {"enonce": "Dans le cas d'une trajectoire plane, que vaut la torsion τ de la courbe ?", "correct": "$\\tau = 0$ (le mouvement reste dans le même plan)", "opts": ["$\\tau = 0$ (le mouvement reste dans le même plan)", "$\\tau = 1$", "$\\tau = R$"], "exp": "Absence de sortie du plan osculateur."},
                    {"enonce": "Quelle est l'unité internationale de l'accélération normale et tangentielle ?", "correct": "Le mètre par seconde carrée (m/s²)", "opts": ["Le mètre par seconde carrée (m/s²)", "Le m/s", "Le rad/s²"], "exp": "Unités cinématiques standards."},
                    {"enonce": "Dans un mouvement circulaire non uniforme, l'accélération totale est :", "correct": "La somme vectorielle de l'accélération tangentielle et normale", "opts": ["La somme vectorielle de l'accélération tangentielle et normale", "Uniquement normale", "Uniquement tangentielle"], "exp": "$\\vec{a} = \\vec{a}_t + \\vec{a}_n$."},
                    {"enonce": "Si la vitesse d'un mobile augmente au cours du temps sur une trajectoire courbe, que dire de l'accélération tangentielle ?", "correct": "Elle est strictement positive (dv/dt > 0)", "opts": ["Elle est strictement positive (dv/dt > 0)", "Elle est nulle", "Elle est négative"], "exp": "Accélération du mouvement."},
                    {"enonce": "Si la vitesse d'un mobile diminue sur une trajectoire circulaire, le mouvement est dit :", "correct": "Retardé", "opts": ["Retardé", "Uniforme", "Accélére"], "exp": "dv/dt < 0 ⇒ mouvement décéléré ou retardé."},
                    {"enonce": "Comment s'exprime la norme du vecteur accélération totale dans la base de Frenet ?", "correct": "$a = \\sqrt{(\\frac{dv}{dt})^2 + (\\frac{v^2}{R})^2}$", "opts": ["$a = \\sqrt{(\\frac{dv}{dt})^2 + (\\frac{v^2}{R})^2}$", "$a = \\frac{dv}{dt} + \\frac{v^2}{R}$", "$a = \\frac{v^2}{R}$"], "exp": "Orthogonalité de $\\vec{u}_t$ et $\\vec{u}_n$."},
                    {"enonce": "Dans le repère de Frenet, le vecteur vitesse $\\vec{v}$ s'exprime simplement par :", "correct": "$\\vec{v} = v \\cdot \\vec{u}_t$", "opts": ["$\\vec{v} = v \\cdot \\vec{u}_t$", "$\\vec{v} = v \\cdot \\vec{u}_n$", "$\\vec{v} = \\frac{v^2}{R}\\vec{u}_b$"], "exp": "La vitesse est toujours tangente à la trajectoire."},
                    {"enonce": "Quel est le nom de la base locale mobile liée à un mobile en mouvement curviligne ?", "correct": "La base de Frenet (ou trièdre de Frenet)", "opts": ["La base de Frenet (ou trièdre de Frenet)", "La base cartésienne fixe", "La base cylindrique absolue"], "exp": "Définition du repère local."},
                    {"enonce": "Le cercle osculateur en un point M d'une courbe est situé dans :", "correct": "Le plan osculateur", "opts": ["Le plan osculateur", "Le plan normal", "Le plan vertical"], "exp": "Définition du cercle osculateur."},
                    {"enonce": "Si la courbure d'une trajectoire est constante (cercle), le rayon de courbure R est :", "correct": "Constant et égal au rayon du cercle", "opts": ["Constant et égal au rayon du cercle", "Variable", "Nul"], "exp": "Pour un cercle, R = r = Cte."},
                    {"enonce": "Que se passe-t-il pour le rayon de courbure R aux points d'inflexion d'une courbe plane ?", "correct": "Il tend vers l'infini (la courbure s'annule)", "opts": ["Il tend vers l'infini (la courbure s'annule)", "Il s'annule", "Il vaut 1"], "exp": "Aux points d'inflexion, la trajectoire s'approche d'une droite."},
                    {"enonce": "La courbure d'une trajectoire est définie mathématiquement comme :", "correct": "L'inverse du rayon de courbure (c = 1/R)", "opts": ["L'inverse du rayon de courbure (c = 1/R)", "Le rayon de courbure lui-même", "La dérivée seconde de la vitesse"], "exp": "Définition de la courbure c."},
                    {"enonce": "Dans un mouvement hélicoïdal (hélice circulaire), le rayon de courbure R est :", "correct": "Constant", "opts": ["Constant", "Variable à chaque instant", "Nul"], "exp": "Propriété de l'hélice circulaire."},
                    {"enonce": "Quel vecteur est normal à la fois à $\\vec{u}_t$ et $\\vec{u}_n$ dans le trièdre de Frenet ?", "correct": "Le vecteur binormal $\\vec{u}_b$", "opts": ["Le vecteur binormal $\\vec{u}_b$", "Le vecteur vitesse", "L'accélération tangentielle"], "exp": "Orthogonalité du trièdre direct."},
                    {"enonce": "Le plan normal à la trajectoire en un point M est défini par les vecteurs :", "correct": "$\\vec{u}_n$ et $\\vec{u}_b$", "opts": ["$\\vec{u}_n$ et $\\vec{u}_b$", "$\\vec{u}_t$ et $\\vec{u}_n$", "$\\vec{u}_t$ et $\\vec{u}_b$"], "exp": "Plan orthogonal au vecteur tangent."},
                    {"enonce": "Le plan rectifiant d'une courbe est le plan engendré par les vecteurs :", "correct": "$\\vec{u}_t$ et $\\vec{u}_b$", "opts": ["$\\vec{u}_t$ et $\\vec{u}_b$", "$\\vec{u}_n$ et $\\vec{u}_b$", "$\\vec{u}_t$ et $\\vec{u}_n$"], "exp": "Définition du plan rectifiant."},
                    {"enonce": "Quel est l'intérêt principal d'utiliser la base de Frenet en physique du point ?", "correct": "Simplifier l'expression des composantes de l'accélération en séparant les effets cinématiques de vitesse et de courbure", "opts": ["Simplifier l'expression des composantes de l'accélération en séparant les effets cinématiques de vitesse et de courbure", "Éviter d'utiliser le calcul différentiel", "Rendre les calculs vectoriels cartésiens obligatoires"], "exp": "Avantage intrinsèque du repère local."},
                    {"enonce": "Dans une trajectoire circulaire de rayon R, l'abscisse curviligne s est liée à l'angle θ par :", "correct": "$s = R \\cdot \\theta$", "opts": ["$s = R \\cdot \\theta$", "$s = \\theta / R$", "$s = R^2 \\cdot \\theta$"], "exp": "Relation arc-angle."},
                    {"enonce": "La vitesse angulaire ω d'un point sur un cercle de rayon R est reliée à la vitesse linéaire v par :", "correct": "$v = R \\cdot \\omega$", "opts": ["$v = R \\cdot \\omega$", "$v = \\omega / R$", "$v = \\omega^2 \\cdot R$"], "exp": "Relation cinématique circulaire."},
                    {"enonce": "Comment s'écrit l'accélération normale en fonction de la vitesse angulaire ω et du rayon R ?", "correct": "$a_n = R \\cdot \\omega^2$", "opts": ["$a_n = R \\cdot \\omega^2$", "$a_n = \\frac{\\omega}{R}$", "$a_n = \\omega^2 / R$"], "exp": "Substituant $v = R\\omega$ dans $v^2/R$."},
                    {"enonce": "Dans un mouvement rectiligne uniforme, l'accélération dans la base de Frenet est :", "correct": "Nulle partout ($\\vec{a} = \\vec{0}$)", "opts": ["Nulle partout ($\\vec{a} = \\vec{0}$)", "Egale à $v^2/R$", "Egale à dv/dt"], "exp": "Pas d'accélération tangentielle ni normale."},
                    {"enonce": "Quelle est la nature du mouvement si l'accélération tangentielle est constante et non nulle et l'accélération normale nulle ?", "correct": "Un mouvement rectiligne uniformément varié", "opts": ["Un mouvement rectiligne uniformément varié", "Un mouvement circulaire uniforme", "Un mouvement parabolique"], "exp": "Trajectoire droite et dv/dt = Cte."},
                    {"enonce": "Que représente la dérivée du vecteur binormal par rapport à l'abscisse curviligne ($d\\vec{u}_b / ds$) ?", "correct": "$-\\tau \\vec{u}_n$", "opts": ["$-\\tau \\vec{u}_n$", "$\\frac{1}{R}\\vec{u}_t$", "$\\vec{0}$"], "exp": "Troisième formule de Frenet-Serret."},
                    {"enonce": "Le trièdre de Frenet est un repère mobile dit :", "correct": "Orthonormé direct", "opts": ["Orthonormé direct", "Galiléen absolu", "Cartésien fixe"], "exp": "Base orthonormée directe $(\\vec{u}_t, \\vec{u}_n, \\vec{u}_b)$."},
                    {"enonce": "Dans un mouvement circulaire, le vecteur accélération normale est toujours dirigé vers :", "correct": "Le centre du cercle", "opts": ["Le centre du cercle", "L'extérieur de la trajectoire", "La tangente"], "exp": "Orientation centripète."},
                    {"enonce": "Si la norme de la vitesse d'un mobile est constante sur une trajectoire quelconque, l'accélération tangentielle vaut :", "correct": "0", "opts": ["0", "v² / R", "1"], "exp": "v = Cte ⇒ dv/dt = 0."},
                    {"enonce": "Quel physicien et mathématicien français a donné son nom à ces formules cinématiques géométriques ?", "correct": "Jean-Frédéric Frenet", "opts": ["Jean-Frédéric Frenet", "Isaac Newton", "Leonhard Euler"], "exp": "Historique des formules de Frenet-Serret."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                type_calc = random.choice(["normale", "tangentielle", "totale", "rayon"])
                if type_calc == "normale":
                    v_val = random.choice([5, 10, 15, 20, 25])
                    r_val = random.choice([2, 4, 5, 10, 50])
                    an_val = round((v_val ** 2) / r_val, 2)
                    enonce = f"Un mobile se déplace sur une trajectoire courbe de rayon de courbure R = {r_val} m avec une vitesse de norme v = {v_val} m/s. Quelle est la valeur de son accélération normale a_n (en m/s²) ?"
                    correct = f"{an_val} m/s²"
                    opts = [f"{an_val} m/s²", f"{round(an_val/2, 2)} m/s²", f"{v_val * r_val} m/s²", f"{round(v_val/r_val, 2)} m/s²"]
                    exp = f"a_n = v² / R = ({v_val}²) / {r_val} = {an_val} m/s²."
                elif type_calc == "tangentielle":
                    acc_t = random.choice([1, 2, 3, 4, 5])
                    enonce = f"La vitesse d'un mobile sur une trajectoire curviligne augmente de façon uniforme avec une accélération tangentielle a_t = {acc_t} m/s² constante. Que représente cette valeur cinématiquement ?"
                    correct = f"La dérivée de la norme de la vitesse par rapport au temps (dv/dt = {acc_t})"
                    opts = [f"La dérivée de la norme de la vitesse par rapport au temps (dv/dt = {acc_t})", "L'accélération normale", "Le rayon de courbure"]
                    exp = f"Par définition, a_t = dv/dt = {acc_t} m/s²."
                elif type_calc == "totale":
                    at = 3.0
                    an = 4.0
                    atot = 5.0
                    enonce = "Dans la base de Frenet, un mobile possède une accélération tangentielle a_t = 3 m/s² et une accélération normale a_n = 4 m/s². Quelle est la norme de son accélération totale a ?"
                    correct = "5 m/s²"
                    opts = ["5 m/s²", "7 m/s²", "1 m/s²", "12 m/s²"]
                    exp = "a = √(a_t² + a_n²) = √(3² + 4²) = √25 = 5 m/s²."
                else:
                    v_val = 10
                    an_val = 5
                    r_calc = round((v_val ** 2) / an_val, 1)
                    enonce = f"Un mobile a une vitesse v = {v_val} m/s et une accélération normale a_n = {an_val} m/s² dans un virage. Quel est le rayon de courbure R de la trajectoire ?"
                    correct = f"{r_calc} m"
                    opts = [f"{r_calc} m", f"{v_val * an_val} m", f"{round(r_calc/2, 1)} m", "1 m"]
                    exp = f"R = v² / a_n = ({v_val}²) / {an_val} = {r_calc} m."

            elif variante == "V3":
                banque_v3 = [
                    {"enonce": "Que se passe-t-il pour le vecteur accélération $\\vec{a}$ dans un mouvement circulaire uniforme ?", "correct": "Il est purement normal (centripète), orthogonal à la vitesse", "opts": ["Il est purement normal (centripète), orthogonal à la vitesse", "Il est tangentiel", "Il est nul"], "exp": "v = Cte ⇒ at = 0, donc $\\vec{a} = a_n \\vec{u}_n$."},
                    {"enonce": "Dans un mouvement rectiligne uniformément varié, l'accélération normale est :", "correct": "Nulle, car le rayon de courbure est infini", "opts": ["Nulle, car le rayon de courbure est infini", "Constante et non nulle", "Variable"], "exp": "Trajectoire droite ⇒ R = ∞ ⇒ an = 0."},
                    {"enonce": "Comment calcule-t-on le rayon de courbure R d'une courbe plane d'équation y = f(x) en un point x ?", "correct": "$R = \\frac{[1 + (y')^2]^{3/2}}{|y''|}$", "opts": ["$R = \\frac{[1 + (y')^2]^{3/2}}{|y''|}$", "$R = \\frac{1}{y''}$", "$R = y' \\cdot y''$"], "exp": "Formule analytique classique du rayon de courbure en géométrie différentielle."},
                    {"enonce": "Quel est le rôle du vecteur binormal $\\vec{u}_b$ dans l'étude analytique d'une trajectoire dans l'espace ?", "correct": "Il permet de caractériser la torsion de la courbe (la sortie du plan osculateur)", "opts": ["Il permet de caractériser la torsion de la courbe (la sortie du plan osculateur)", "Il donne la vitesse", "Il mesure l'accélération tangentielle"], "exp": "Lien entre la dérivée de $\\vec{u}_b$ et la torsion."},
                    {"enonce": "Que signifie un trièdre de Frenet mobile en cinématique du point ?", "correct": "Que les vecteurs de base ($\\vec{u}_t, \\vec{u}_n, \\vec{u}_b$) changent de direction au cours du temps à chaque point de la trajectoire", "opts": ["Que les vecteurs de base ($\\vec{u}_t, \\vec{u}_n, \\vec{u}_b$) changent de direction au cours du temps à chaque point de la trajectoire", "Que le repère est fixe dans l'espace galiléen", "Que les axes sont orthogonaux fixes"], "exp": "Repère mobile attaché au mobile."},
                    {"enonce": "Dans le repère de Frenet, la dérivée temporelle du vecteur tangent $\\vec{u}_t$ vérifie :", "correct": "$\\frac{d\\vec{u}_t}{dt} = \\frac{v}{R}\\vec{u}_n$", "opts": ["$\\frac{d\\vec{u}_t}{dt} = \\frac{v}{R}\\vec{u}_n$", "$\\frac{d\\vec{u}_t}{dt} = \\vec{0}$", "$\\frac{d\\vec{u}_t}{dt} = \\frac{dv}{dt}\\vec{u}_t$"], "exp": "Dérivée composée : $\\frac{d\\vec{u}_t}{ds}\\frac{ds}{dt} = \\frac{1}{R}\\vec{u}_n \\cdot v$."},
                    {"enonce": "Dans le repère de Frenet, la dérivée temporelle du vecteur normal $\\vec{u}_n$ vérifie :", "correct": "$\\frac{d\\vec{u}_n}{dt} = -\\frac{v}{R}\\vec{u}_t + v\\tau \\vec{u}_b$", "opts": ["$\\frac{d\\vec{u}_n}{dt} = -\\frac{v}{R}\\vec{u}_t + v\\tau \\vec{u}_b$", "$\\frac{d\\vec{u}_n}{dt} = \\frac{v}{R}\\vec{u}_t$", "$\\frac{d\\vec{u}_n}{dt} = \\vec{0}$"], "exp": "Application de la formule de Frenet-Serret par dérivation temporelle."},
                    {"enonce": "Quelle est l'implication physique si l'accélération tangentielle est constante et l'accélération normale varie ?", "correct": "Le module de la vitesse varie linéairement et la courbure de la trajectoire change au cours du temps", "opts": ["Le module de la vitesse varie linéairement et la courbure de la trajectoire change au cours du temps", "Le mouvement est circulaire uniforme", "La trajectoire est nécessairement un cercle"], "exp": "Analyse combinée des composantes."},
                    {"enonce": "Comment se comporte la base de Frenet pour une trajectoire rectiligne ? ", "correct": "Le vecteur tangent $\\vec{u}_t$ est fixe en direction, mais les vecteurs $\\vec{u}_n$ et $\\vec{u}_b$ ne sont pas définis de façon unique", "opts": ["Le vecteur tangent $\\vec{u}_t$ est fixe en direction, mais les vecteurs $\\vec{u}_n$ et $\\vec{u}_b$ ne sont pas définis de façon unique", "Tous les vecteurs sont nuls", "Le repère n'existe pas"], "exp": "Indétermination du plan osculateur sur une droite."},
                    {"enonce": "Quel est le lien entre le vecteur vitesse $\\vec{v}$ et l'abscisse curviligne s dans le calcul vectoriel ?", "correct": "$\\vec{v} = \\frac{ds}{dt}\\vec{u}_t$", "opts": ["$\\vec{v} = \\frac{ds}{dt}\\vec{u}_t$", "$\\vec{v} = \\frac{d^2s}{dt^2}\\vec{u}_n$", "$\\vec{v} = s \\cdot \\vec{u}_b$"], "exp": "Expression intrinsèque de la vitesse."},
                    {"enonce": "Si la trajectoire est une parabole, le rayon de courbure R au sommet de la parabole est :", "correct": "Minimal et égal au demi-paramètre de la parabole", "opts": ["Minimal et égal au demi-paramètre de la parabole", "Infini", "Nul"], "exp": "Propriété géométrique de la parabole au sommet."},
                    {"enonce": "Dans un mouvement sur une trajectoire plane, le vecteur binormal $\\vec{u}_b$ est :", "correct": "Constant en direction (perpendiculaire au plan de la trajectoire)", "opts": ["Constant en direction (perpendiculaire au plan de la trajectoire)", "Variable en permanence", "Confondu avec $\\vec{u}_t$"], "exp": "Pour une courbe plane, le plan osculateur est fixe."},
                    {"enonce": "Comment qualifie-t-on une courbe dont la torsion τ est non nulle partout ?", "correct": "Une courbe gauche (qui ne se trouve dans aucun plan unique)", "opts": ["Une courbe gauche (qui ne se trouve dans aucun plan unique)", "Une courbe plane", "Une droite"], "exp": "Définition d'une courbe gauche."},
                    {"enonce": "Quelle est la composante de l'accélération portée par le vecteur binormal $\\vec{u}_b$ dans la base de Frenet ?", "correct": "Exactement nulle (le vecteur accélération $\\vec{a}$ est toujours contenu dans le plan osculateur $\\vec{u}_t, \\vec{u}_n$)", "opts": ["Exactement nulle (le vecteur accélération $\\vec{a}$ est toujours contenu dans le plan osculateur $\\vec{u}_t, \\vec{u}_n$)", "Égale à v² / R", "Égale à dv/dt"], "exp": "Propriété fondamentale : $\\vec{a}$ n'a pas de composante sur $\\vec{u}_b$."},
                    {"enonce": "Comment évolue l'accélération normale lors d'un freinage d'urgence sur un virage circulaire de rayon R ?", "correct": "Elle diminue car la norme de la vitesse v diminue au cours du temps", "opts": ["Elle diminue car la norme de la vitesse v diminue au cours du temps", "Elle augmente", "Elle reste constante"], "exp": "an = v² / R, si v décroît, an décroît."},
                    {"enonce": "Quel est l'effet de l'accélération tangentielle lors d'une accélération en ligne droite courbe (virage relevé) ?", "correct": "Elle modifie la grandeur de la vitesse sans changer la direction instantanée du mouvement", "opts": ["Elle modifie la grandeur de la vitesse sans changer la direction instantanée du mouvement", "Elle modifie la courbure", "Elle annule la force centrifuge"], "exp": "Rôle exclusif sur le module de la vitesse."},
                    {"enonce": "Dans l'étude des forces en mécanique, à quoi sert principalement la projection dans la base de Frenet ?", "correct": "À exprimer directement la force normale (centripète) et la force tangentielle (motrice ou résistante)", "opts": ["À exprimer directement la force normale (centripète) et la force tangentielle (motrice ou résistante)", "À calculer la masse du mobile", "À ignorer les frottements"], "exp": "Application dynamique de la base locale."},
                    {"enonce": "Si la force totale s'exerçant sur un point matériel est purement orthogonale à sa vitesse à chaque instant, le mouvement est :", "correct": "Uniforme (vitesse constante en norme)", "opts": ["Uniforme (vitesse constante en norme)", "Accéléré", "Rectiligne"], "exp": "$\\vec{F} \\cdot \\vec{v} = 0 \\Rightarrow \\frac{d(1/2 m v^2)}{dt} = 0 \\Rightarrow v = \\text{Cte}$."},
                    {"enonce": "Dans un mouvement circulaire, que représente la force normale (ou centripète) ?", "correct": "La force qui maintient le mobile sur sa trajectoire circulaire en modifiant la direction de sa vitesse", "opts": ["La force qui maintient le mobile sur sa trajectoire circulaire en modifiant la direction de sa vitesse", "La force qui accélère le mobile en ligne droite", "Le poids du mobile"], "exp": "Rôle cinématique de la force normale."},
                    {"enonce": "Quelle est la condition cinématique pour qu'un point matériel change de sens sur sa trajectoire curviligne ?", "correct": "Que la vitesse algébrique v s'annule en changeant de signe (v = 0 avec dv/dt ≠ 0)", "opts": ["Que la vitesse algébrique v s'annule en changeant de signe (v = 0 avec dv/dt ≠ 0)", "Que l'accélération normale soit nulle", "Que le rayon de courbure soit infini"], "exp": "Inversion du sens du mouvement sur l'arc s."},
                    {"enonce": "Propriété avancée n°21 : Le produit mixte $(\\vec{u}_t, \\vec{u}_n, \\vec{u}_b)$ dans le trièdre direct de Frenet vaut :", "correct": "1", "opts": ["1", "0", "-1"], "exp": "Base orthonormée directe normalisée."},
                    {"enonce": "Propriété avancée n°22 : La dérivée du vecteur position $\\vec{OM}$ par rapport au temps dans la base de Frenet s'écrit :", "correct": "$v \\cdot \\vec{u}_t$", "opts": ["$v \\cdot \\vec{u}_t$", "$v \\cdot \\vec{u}_n$", "$R \\cdot \\vec{u}_b$"], "exp": "Définition vectorielle de la vitesse."},
                    {"enonce": "Propriété avancée n°23 : Si le rayon de courbure R est inversement proportionnel à l'abscisse s ($R = k/s$), la courbure est :", "correct": "Directement proportionnelle à s ($c = s/k$)", "opts": ["Directement proportionnelle à s ($c = s/k$)", "Constante", "Nulle"], "exp": "Inversion de la relation R et c."},
                    {"enonce": "Propriété avancée n°24 : Dans le mouvement d'un projectile dans le champ de pesanteur (sans frottement), la trajectoire est une parabole. Le rayon de courbure au sommet est :", "correct": "$R = v_0^2 / g$", "opts": ["$R = v_0^2 / g$", "$R = g / v_0^2$", "$R = 0$"], "exp": "Au sommet, $a_n = g = v_0^2 / R \\Rightarrow R = v_0^2 / g$."},
                    {"enonce": "Propriété avancée n°25 : La formule donnant l'accélération vectorielle totale à partir du vecteur position vectoriel est :", "correct": "$\\vec{a} = \\frac{d^2\\vec{OM}}{dt^2}$", "opts": ["$\\vec{a} = \\frac{d^2\\vec{OM}}{dt^2}$", "$\\vec{a} = \\frac{d\\vec{u}_t}{dt}$", "$\\vec{a} = \\frac{ds}{dt}\\vec{u}_n$"], "exp": "Définition cinématique fondamentale de l'accélération."},
                    {"enonce": "Propriété avancée n°26 : Quelle est la dimension physique de la courbure c ?", "correct": "L'inverse d'une longueur ($[L]^{-1}$)", "opts": ["L'inverse d'une longueur ($[L]^{-1}$)", "Une longueur ($[L]$)", "Sans dimension"], "exp": "c = 1/R donc homogène à l'inverse d'un mètre."},
                    {"enonce": "Propriété avancée n°27 : La torsion τ d'une courbe gauche s'exprime homogènement en :", "correct": "L'inverse d'une longueur ($[L]^{-1}$)", "opts": ["L'inverse d'une longueur ($[L]^{-1}$)", "Radians par seconde", "Sans dimension"], "exp": "Homogène à une courbure."},
                    {"enonce": "Propriété avancée n°28 : Si un mobile parcourt une spirale, le rayon de courbure R est :", "correct": "Variable en tout point de la trajectoire", "opts": ["Variable en tout point de la trajectoire", "Constant", "Nul"], "exp": "La spirale présente une courbure non uniforme."},
                    {"enonce": "Propriété avancée n°29 : Dans la décomposition intrinsèque, l'accélération tangentielle est indépendante de :", "correct": "La courbure de la trajectoire (R n'intervient pas dans at = dv/dt)", "opts": ["La courbure de la trajectoire (R n'intervient pas dans at = dv/dt)", "La vitesse", "Le temps"], "exp": "at ne dépend que de la variation du module de la vitesse."},
                    {"enonce": "Propriété avancée n°30 : L'accélération normale dépend directement de :", "correct": "La vitesse au carré et de l'inverse du rayon de courbure", "opts": ["La vitesse au carré et de l'inverse du rayon de courbure", "Uniquement de l'accélération tangentielle", "De la masse du mobile"], "exp": "an = v² / R."},
                    {"enonce": "Propriété avancée n°31 : Si la vitesse d'un point est exprimée en fonction de l'abscisse curviligne $v(s)$, l'accélération tangentielle s'écrit par composition :", "correct": "$a_t = v(s) \\cdot \\frac{dv}{ds}$", "opts": ["$a_t = v(s) \\cdot \\frac{dv}{ds}$", "$a_t = \\frac{ds}{dt}$", "$a_t = \\frac{v^2}{s}$"], "exp": "$\\frac{dv}{dt} = \\frac{dv}{ds}\\frac{ds}{dt} = v \\frac{dv}{ds}$."},
                    {"enonce": "Propriété avancée n°32 : Le plan normal à la trajectoire est orthogonal au vecteur :", "correct": "Tangent $\\vec{u}_t$", "opts": ["Tangent $\\vec{u}_t$", "Normal $\\vec{u}_n$", "Binormal $\\vec{u}_b$"], "exp": "Par définition, le plan normal est orthogonal à la tangente."},
                    {"enonce": "Propriété avancée n°33 : Dans un mouvement circulaire, l'angle entre le vecteur vitesse et le vecteur accélération totale est lié à :", "correct": "Au rapport entre l'accélération normale et tangentielle ($\\tan\\alpha = a_n / a_t$)", "opts": ["Au rapport entre l'accélération normale et tangentielle ($\\tan\\alpha = a_n / a_t$)", "Toujours égal à 90°", "Toujours nul"], "exp": "Décomposition orthogonale de l'accélération par rapport à la vitesse."},
                    {"enonce": "Propriété avancée n°34 : Lorsque la trajectoire est une ligne droite, le trièdre de Frenet :", "correct": "Perd sa définition unique pour le plan normal et binormal car la courbure est nulle", "opts": ["Perperd sa définition unique pour le plan normal et binormal car la courbure est nulle", "Reste parfaitement rigide", "S'arrête"], "exp": "Impossibilité de définir un centre de courbure unique sur une droite."},
                    {"enonce": "Propriété avancée n°35 : La vitesse arithmétique instantanée d'un mobile ponctuel le long d'une courbe correspond à :", "correct": "La norme du vecteur vitesse $\\vec{v}$", "opts": ["La norme du vecteur vitesse $\\vec{v}$", "L'accélération", "Le rayon R"], "exp": "Définition de la norme de la vitesse."},
                    {"enonce": "Propriété avancée n°36 : Dans le repère de Frenet, le produit scalaire $\\vec{u}_t \\cdot \\vec{u}_n$ vaut toujours :", "correct": "0", "opts": ["0", "1", "-1"], "exp": "Orthogonalité des vecteurs de base de Frenet."},
                    {"enonce": "Propriété avancée n°37 : Le produit scalaire $\\vec{u}_n \\cdot \\vec{u}_b$ vaut toujours :", "correct": "0", "opts": ["0", "1", "-1"], "exp": "Orthogonalité de la normale et du binormal."},
                    {"enonce": "Propriété avancée n°38 : Le produit scalaire $\\vec{u}_t \\cdot \\vec{u}_b$ vaut toujours :", "correct": "0", "opts": ["0", "1", "-1"], "exp": "Orthogonalité du tangent et du binormal."},
                    {"enonce": "Propriété avancée n°39 : La cinématique du point dans la base de Frenet permet de traiter de façon élégante les mouvements dans :", "correct": "Les espaces à une, deux ou trois dimensions curvilignes", "opts": ["Les espaces à une, deux ou trois dimensions curvilignes", "Uniquement en coordonnées cartésiennes fixes", "Uniquement au repos"], "exp": "Portée générale de la méthode intrinsèque de Frenet."},
                    {"enonce": "Propriété avancée n°40 : En résumé, la base de Frenet est une description cinématique dite :", "correct": "Intrinsèque (indépendante du choix d'un système d'axes cartésien fixe)", "opts": ["Intrinsèque (indépendante du choix d'un système d'axes cartésien fixe)", "Absolue galiléenne", "Statique"], "exp": "Caractère intrinsèque du repère de Frenet lié au mobile."}
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

# =======================================
        # 45. RÉGIME RLC
# =======================================
        elif chapitre_cible == "Régime RLC":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "Condition sur la résistance R pour obtenir un régime pseudo-périodique (oscillations amorties) ?", "correct": "R < 2 · √(L/C)", "opts": ["R < 2 · √(L/C)", "R > 2 · √(L/C)", "R = 0"], "exp": "Discriminant négatif de l'équation caractéristique."},
                    {"enonce": "Quel nom porte le régime obtenu lorsque la résistance R est très grande devant la résistance critique ?", "correct": "Régime apériodique", "opts": ["Régime apériodique", "Régime critique", "Régime oscillatoire"], "exp": "Amortissement fort sans oscillation."},
                    {"enonce": "À la résonance d'intensité dans un circuit RLC série, l'impédance totale Z est :", "correct": "Minimale (égale à R)", "opts": ["Minimale (égale à R)", "Maximale", "Nulle"], "exp": "Annulation de la réactance inductive et capacitive."},
                    {"enonce": "Qu'appelle-t-on régime critique dans un circuit RLC série ?", "correct": "Le régime obtenu pour la résistance critique R_c = 2 · √(L/C) marquant la limite des oscillations", "opts": ["Le régime obtenu pour la résistance critique R_c = 2 · √(L/C) marquant la limite des oscillations", "Un régime infini", "Un régime sans perte"], "exp": "Disparition des oscillations au plus vite sans dépassement."},
                    {"enonce": "Quelle est l'expression de la pulsation propre ω_0 d'un circuit oscillant LC non amorti ?", "correct": "ω_0 = 1 / √(L · C)", "opts": ["ω_0 = 1 / √(L · C)", "ω_0 = √(L · C)", "ω_0 = R / L"], "exp": "Pulsation propre des oscillations libres non amorties."},
                    {"enonce": "Dans un circuit RLC série, que représente le facteur de qualité Q du circuit ?", "correct": "L'acuité de la résonance (Q = (1/R) · √(L/C))", "opts": ["L'acuité de la résonance (Q = (1/R) · √(L/C))", "La résistance totale", "Le déphasage maximal"], "exp": "Définition du facteur de qualité Q."},
                    {"enonce": "À la résonance d'intensité, le déphasage φ entre la tension aux bornes du circuit et l'intensité du courant vaut :", "correct": "φ = 0 (tension et courant en phase)", "opts": ["φ = 0 (tension et courant en phase)", "φ = π / 2", "φ = π"], "exp": "Annulation de la réactance totale à la résonance."},
                    {"enonce": "Quelle est l'expression de l'impédance Z d'un circuit RLC série de résistance R, inductance L et capacité C à la pulsation ω ?", "correct": "Z = √[ R² + (Lω - 1/(Cω))² ]", "opts": ["Z = √[ R² + (Lω - 1/(Cω))² ]", "Z = R + Lω + 1/(Cω)", "Z = R² + Lω"], "exp": "Expression générale de l'impédance en série."},
                    {"enonce": "Que se passe-t-il pour l'amplitude de la tension aux bornes du condensateur à la résonance de charge ?", "correct": "Elle présente un maximum pour une pulsation légèrement inférieure à ω_0", "opts": ["Elle présente un maximum pour une pulsation légèrement inférieure à ω_0", "Elle est nulle", "Elle est infinie dans tous les cas"], "exp": "Résonance de charge du condensateur."},
                    {"enonce": "Quelle est l'équation différentielle régissant les oscillations libres d'un circuit RLC série portant une charge q ?", "correct": "L · (d²q/dt²) + R · (dq/dt) + q/C = 0", "opts": ["L · (d²q/dt²) + R · (dq/dt) + q/C = 0", "L · (dq/dt) + Rq = 0", "d²q/dt² + q/C = 0"], "exp": "Équation différentielle de la charge q(t)."},
                    {"enonce": "Dans un circuit RLC, l'énergie totale emmagasinée (électrique et magnétique) en régime libre non entretenu :", "correct": "Décroît au cours du temps par dissipation effet Joule dans la résistance R", "opts": ["Décroît au cours du temps par dissipation effet Joule dans la résistance R", "Reste strictement constante", "Augmente indéfiniment"], "exp": "Dissipation d'énergie par effet Joule."},
                    {"enonce": "Quelle est l'unité légale de l'inductance L dans le système international ?", "correct": "Le Henry (H)", "opts": ["Le Henry (H)", "Le Farad (F)", "L'Ohm (Ω)"], "exp": "Unité de l'inductance propre."},
                    {"enonce": "Quelle est l'unité légale de la capacité C d'un condensateur ?", "correct": "Le Farad (F)", "opts": ["Le Farad (F)", "Le Henry (H)", "Le Weber (Wb)"], "exp": "Unité de la capacité."},
                    {"enonce": "Comment qualifie-t-on un circuit RLC ne comportant aucune résistance (R = 0) ?", "correct": "Un circuit LC idéal non amorti (oscillateur harmonique)", "opts": ["Un circuit LC idéal non amorti (oscillateur harmonique)", "Un circuit apériodique", "Un circuit court-circuité"], "exp": "Absence d'amortissement."},
                    {"enonce": "À la résonance d'intensité, la puissance électrique moyenne consommée dans un circuit RLC série est :", "correct": "Maximale (égale à P_max = U² / R)", "opts": ["Maximale (égale à P_max = U² / R)", "Nulle", "Minimale"], "exp": "Maximum de puissance active à la résonance."},
                    {"enonce": "Quel est le facteur de puissance cos(φ) d'un circuit RLC série à la résonance ?", "correct": "cos(φ) = 1", "opts": ["cos(φ) = 1", "cos(φ) = 0", "cos(φ) = 0,5"], "exp": "Courant et tension en phase ⇒ cos(φ) = 1."},
                    {"enonce": "Que vaut la réactance inductive X_L d'une bobine d'inductance L à la pulsation ω ?", "correct": "X_L = L · ω", "opts": ["X_L = L · ω", "X_L = 1 / (Lω)", "X_L = R"], "exp": "Définition de la réactance inductive."},
                    {"enonce": "Que vaut la réactance capacitive X_C d'un condensateur de capacité C à la pulsation ω ?", "correct": "X_C = 1 / (C · ω)", "opts": ["X_C = 1 / (C · ω)", "X_C = C · ω", "X_C = 0"], "exp": "Définition de la réactance capacitive."},
                    {"enonce": "La bande passante à -3 dB d'un circuit RLC série résonnant dépend directement de :", "correct": "La résistance R et de l'inductance L (Δω = R / L)", "opts": ["La résistance R et de l'inductance L (Δω = R / L)", "Uniquement de la capacité C", "De la tension du générateur"], "exp": "Δω = R / L."},
                    {"enonce": "Quel est l'effet d'une augmentation de la résistance R sur l'acuité de la résonance (facteur Q) ?", "correct": "Elle diminue le facteur de qualité et élargit la bande passante", "opts": ["Elle diminue le facteur de qualité et élargit la bande passante", "Elle augmente le facteur de qualité", "Aucun effet"], "exp": "Q est inversement proportionnel à R."},
                    {"enonce": "L'énergie magnétique emmagasinée dans une bobine d'inductance L traversée par un courant i s'exprime par :", "correct": "E_m = (1/2) · L · i²", "opts": ["E_m = (1/2) · L · i²", "E_m = L · i", "E_m = (1/2) · C · u²"], "exp": "Énergie bobine."},
                    {"enonce": "L'énergie électrostatique emmagasinée dans un condensateur de capacité C sous une tension u s'exprime par :", "correct": "E_e = (1/2) · C · u²", "opts": ["E_e = (1/2) · C · u²", "E_e = C · u", "E_e = (1/2) · L · i²"], "exp": "Énergie condensateur."},
                    {"enonce": "Dans un régime pseudo-périodique, la période propre des oscillations est :", "correct": "Très voisine de la période propre T_0 = 2π / ω_0 si l'amortissement est faible", "opts": ["Très voisine de la période propre T_0 = 2π / ω_0 si l'amortissement est faible", "Nulle", "Infinie"], "exp": "Pseudo-période proche de la période propre pour un faible amortissement."},
                    {"enonce": "Quel appareil permet d'entretenir les oscillations dans un circuit RLC pour compenser les pertes par effet Joule ?", "correct": "Un montage amplificateur ou un dispositif à résistance négative (oscillateur entretenu)", "opts": ["Un montage amplificateur ou un dispositif à résistance négative (oscillateur entretenu)", "Un simple interrupteur", "Une résistance supplémentaire"], "exp": "Entretien des oscillations."},
                    {"enonce": "Que se passe-t-il si la résistance R est négative dans un modèle théorique d'oscillateur ?", "correct": "Les oscillations s'amplifient au cours du temps (instabilité)", "opts": ["Les oscillations s'amplifient au cours du temps (instabilité)", "Le courant s'annule instantanément", "Rien ne change"], "exp": "Amortissement négatif ⇒ croissance exponentielle de l'amplitude."},
                    {"enonce": "La constante de temps τ caractéristique d'un circuit RL série vaut :", "correct": "τ = L / R", "opts": ["τ = L / R", "τ = R / L", "τ = L · C"], "exp": "Constante de temps de relaxation RL."},
                    {"enonce": "La constante de temps τ d'un circuit RC série vaut :", "correct": "τ = R · C", "opts": ["τ = R · C", "τ = C / R", "τ = R / C"], "exp": "Constante de temps RC."},
                    {"enonce": "À quoi correspond physiquement l'état permanent dans un circuit RLC soumis à un échelon de tension ?", "correct": "À l'état atteint lorsque les régimes transitoires se sont amortis (t → +∞)", "opts": ["À l'état atteint lorsque les régimes transitoires se sont amortis (t → +∞)", "Au début de la fermeture", "À l'explosion du condensateur"], "exp": "Disparition du régime transitoire."},
                    {"enonce": "En régime sinusoïdal forcé, la tension instantanée u(t) et le courant i(t) ont :", "correct": "La même pulsation ω que celle du générateur excitateur", "opts": ["La même pulsation ω que celle du générateur excitateur", "Des pulsations différentes", "Une pulsation nulle"], "exp": "Le régime forcé adopte la fréquence de l'excitateur."},
                    {"enonce": "Quel est le déphasage φ du courant par rapport à la tension dans un circuit purement inductif (R=0, L) ?", "correct": "Le courant est en retard de π/2 sur la tension (φ = -π/2)", "opts": ["Le courant est en retard de π/2 sur la tension (φ = -π/2)", "Le courant est en avance de π/2", "En phase"], "exp": "Retard de phase dans une bobine pure."},
                    {"enonce": "Quel est le déphasage φ du courant par rapport à la tension dans un circuit purement capacitif (R=0, C) ?", "correct": "Le courant est en avance de π/2 sur la tension (φ = +π/2)", "opts": ["Le courant est en avance de π/2 sur la tension (φ = +π/2)", "En retard", "En phase"], "exp": "Avance de phase dans un condensateur parfait."},
                    {"enonce": "Comment qualifie-t-on un circuit RLC dont la réactance globale est inductive (Lω > 1/Cω) ?", "correct": "Il se comporte globalement comme un dipôle inductif (courant en retard sur la tension)", "opts": ["Il se comporte globalement comme un dipôle inductif (courant en retard sur la tension)", "Comme un dipôle capacitif", "Comme une résistance pure"], "exp": "Caractère inductif du circuit."},
                    {"enonce": "Comment qualifie-t-on un circuit RLC dont la réactance globale est capacitive (Lω < 1/Cω) ?", "correct": "Il se comporte globalement comme un dipôle capacitif (courant en avance sur la tension)", "opts": ["Il se comporte globalement comme un dipôle capacitif (courant en avance sur la tension)", "Comme un dipôle inductif", "Comme un court-circuit"], "exp": "Caractère capacitif du circuit."},
                    {"enonce": "Quel est l'intérêt d'avoir un facteur de qualité Q très élevé dans un circuit d'accord radio (récepteur) ?", "correct": "D'obtenir une sélectivité en fréquence très pointue pour filtrer les stations", "opts": ["D'obtenir une sélectivité en fréquence très pointue pour filtrer les stations", "De détruire le signal", "D'élargir la bande passante à l'infini"], "exp": "Sélectivité accrue pour un grand Q."},
                    {"enonce": "Quelle est la nature mathématique de l'équation différentielle d'un régime pseudo-périodique RLC ?", "correct": "Une équation différentielle linéaire du second ordre à coefficients constants avec second membre nul", "opts": ["Une équation différentielle linéaire du second ordre à coefficients constants avec second membre nul", "Une équation du premier ordre", "Une équation algébrique simple"], "exp": "Second ordre linéaire homogène."},
                    {"enonce": "Que représente le décrément logarithmique dans les oscillations amorties ?", "correct": "Le logarithme népérien du rapport de deux amplitudes maximales consécutives", "opts": ["Le logarithme népérien du rapport de deux amplitudes maximales consécutives", "La fréquence des oscillations", "La résistance critique"], "exp": "Définition du décrément logarithmique."},
                    {"enonce": "Dans un circuit RLC parallèle (antirésonance), l'impédance à la résonance est :", "correct": "Maximale", "opts": ["Maximale", "Minimale", "Nulle"], "exp": "Antirésonance d'impédance maximale."},
                    {"enonce": "Quel physicien a formulé les lois fondamentales de l'induction électromagnétique régissant la bobine ?", "correct": "Michael Faraday (et Lenz)", "opts": ["Michael Faraday (et Lenz)", "Isaac Newton", "Ohm"], "exp": "Loi de Faraday-Lenz."},
                    {"enonce": "En régime transitoire d'un circuit RLC, la durée caractéristique du retour à l'équilibre est liée à :", "correct": "La grandeur du temps de relaxation L/R ou RC", "opts": ["La grandeur du temps de relaxation L/R ou RC", "Uniquement à la température", "À la masse des électrons"], "exp": "Constantes de temps caractéristiques."},
                    {"enonce": "Propriété fondamentale : à la résonance d'intensité dans un RLC série, l'intensité efficace I_max vaut :", "correct": "I_max = U / R", "opts": ["I_max = U / R", "I_max = U · R", "I_max = 0"], "exp": "L'impédance se réduit à R, d'où I_max = U/R."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                type_calc = random.choice(["omega", "rcrit", "imp", "qual"])
                if type_calc == "omega":
                    l_mH = random.choice([10, 25, 50, 100])
                    c_uF = random.choice([1, 2, 10, 20])
                    l_H = l_mH * 1e-3
                    c_F = c_uF * 1e-6
                    omega0 = round(1.0 / math.sqrt(l_H * c_F), 1)
                    enonce = f"Calculez la pulsation propre ω_0 (en rad/s) d'un circuit LC avec L = {l_mH} mH et C = {c_uF} µF."
                    correct = f"{omega0} rad/s"
                    opts = [f"{omega0} rad/s", f"{round(omega0/2, 1)} rad/s", f"{round(omega0*2, 1)} rad/s", f"{l_mH * c_uF} rad/s"]
                    exp = f"ω_0 = 1 / √(L · C) = 1 / √({l_H} × {c_F}) = {omega0} rad/s."
                elif type_calc == "rcrit":
                    l_val = random.choice([0.1, 0.2, 0.5, 1.0])
                    c_val = random.choice([1e-6, 2e-6, 10e-6])
                    r_crit = round(2.0 * math.sqrt(l_val / c_val), 1)
                    enonce = f"Quelle est la valeur de la résistance critique R_c (en Ohms) pour un circuit RLC avec L = {l_val} H et C = {c_val * 1e6} µF ?"
                    correct = f"{r_crit} Ω"
                    opts = [f"{r_crit} Ω", f"{round(r_crit/2, 1)} Ω", f"{round(r_crit*2, 1)} Ω", f"{l_val / c_val} Ω"]
                    exp = f"R_c = 2 · √(L/C) = 2 · √({l_val} / {c_val}) = {r_crit} Ω."
                elif type_calc == "imp":
                    r_ohms = random.choice([10, 20, 50, 100])
                    enonce = f"Quelle est l'impédance totale Z (en Ohms) d'un circuit RLC série à la résonance d'intensité, sachant que R = {r_ohms} Ω, L = 50 mH et C = 10 µF ?"
                    correct = f"{r_ohms} Ω"
                    opts = [f"{r_ohms} Ω", "0 Ω", f"{r_ohms * 2} Ω", "1000 Ω"]
                    exp = f"À la résonance, la réactance s'annule, donc Z = R = {r_ohms} Ω."
                else:
                    r_val = random.choice([10, 20, 25])
                    l_val = 0.1
                    c_val = 10e-6
                    q_val = round((1.0 / r_val) * math.sqrt(l_val / c_val), 2)
                    enonce = f"Calculez le facteur de qualité Q d'un circuit RLC série avec R = {r_val} Ω, L = {l_val} H et C = 10 µF."
                    correct = f"{q_val}"
                    opts = [f"{q_val}", f"{round(q_val * 2, 2)}", "1", "10"]
                    exp = f"Q = (1/R) · √(L/C) = (1/{r_val}) · √({l_val} / {c_val}) = {q_val}."

            elif variante == "V3":
                banque_v3 = [
                    {"enonce": "Quelle est l'expression mathématique exacte de la fréquence propre f_0 d'un circuit LC ?", "correct": "f_0 = 1 / (2π · √(L · C))", "opts": ["f_0 = 1 / (2π · √(L · C))", "f_0 = 2π · √(L · C)", "f_0 = L · C / 2π"], "exp": "Relation entre pulsation propre et fréquence propre : f_0 = ω_0 / (2π)."},
                    {"enonce": "Dans un circuit RLC série en régime sinusoïdal forcé, que vaut le déphasage φ de l'intensité par rapport à la tension totale ?", "correct": "tan(φ) = (Lω - 1/Cω) / R", "opts": ["tan(φ) = (Lω - 1/Cω) / R", "tan(φ) = R / (Lω)", "tan(φ) = 0"], "exp": "Expression trigonométrique du déphasage."},
                    {"enonce": "Que se produit-il en terme d'énergie lors de la résonance d'énergie dans un circuit LC non amorti ?", "correct": "Il y a un échange permanent et total d'énergie entre le champ magnétique de la bobine et le champ électrique du condensateur", "opts": ["Il y a un échange permanent et total d'énergie entre le champ magnétique de la bobine et le champ électrique du condensateur", "L'énergie est totalement perdue", "L'énergie reste figée dans la pile"], "exp": "Conservation et oscillation de l'énergie électromagnétique."},
                    {"enonce": "Comment définit-on la bande passante Δf à -3 dB d'un circuit RLC série résonnant ?", "correct": "Δf = f_2 - f_1 = R / (2π · L)", "opts": ["Δf = f_2 - f_1 = R / (2π · L)", "Δf = f_0", "Δf = R · L"], "exp": "Expression de la bande passante en fonction de R et L."},
                    {"enonce": "Quelle est la relation entre le facteur de qualité Q, la fréquence propre f_0 et la bande passante Δf ?", "correct": "Q = f_0 / Δf", "opts": ["Q = f_0 / Δf", "Q = Δf / f_0", "Q = f_0 · Δf"], "exp": "Définition du facteur de qualité via l'acuité de la résonance."},
                    {"enonce": "Quel est l'effet d'une diminution de la capacité C sur la fréquence propre f_0 d'un circuit LC ?", "correct": "Elle augmente la fréquence propre f_0", "opts": ["Elle augmente la fréquence propre f_0", "Elle diminue f_0", "Aucun effet"], "exp": "f_0 est inversement proportionnel à √C."},
                    {"enonce": "Dans un circuit RLC série, l'impédance Z est-elle fonction de la température des composants ?", "correct": "Oui, car la résistance R des conducteurs dépend de la température", "opts": ["Oui, car la résistance R des conducteurs dépend de la température", "Non, jamais", "Uniquement la capacité"], "exp": "Dépendance thermique de la résistance ohmique."},
                    {"enonce": "Que vaut la puissance moyenne consommée par un condensateur parfait dans un circuit alternatif ?", "correct": "Nulle (P = 0)", "opts": ["Nulle (P = 0)", "Maximale", "égale à U·I"], "exp": "Le condensateur ne dissipe aucune énergie active."},
                    {"enonce": "Que vaut la puissance moyenne consommée par une bobine idéale (sans résistance interne) en régime alternatif ?", "correct": "Nulle (P = 0)", "opts": ["Nulle (P = 0)", "Maximale", "égale à R·I²"], "exp": "Une bobine idéale est un dipôle non dissipatif."},
                    {"enonce": "Quelle est l'influence de la résistance interne r d'une bobine réelle dans un circuit RLC ?", "correct": "Elle s'ajoute à la résistance R du circuit, augmentant l'amortissement total (R_tot = R + r)", "opts": ["Elle s'ajoute à la résistance R du circuit, augmentant l'amortissement total (R_tot = R + r)", "Elle annule l'inductance", "Elle n'a aucun effet"], "exp": "Prise en compte de la résistance propre de la bobine."},
                    {"enonce": "Comment appelle-t-on le phénomène où l'amplitude de la tension aux bornes de la bobine passe par un maximum à une pulsation différente de ω_0 ?", "correct": "Résonance de tension aux bornes de la bobine", "opts": ["Résonance de tension aux bornes de la bobine", "Antirésonance absolue", "Court-circuit"], "exp": "Résonance inductive."},
                    {"enonce": "Quelle est la condition d'existence de la résonance de tension aux bornes du condensateur dans un RLC série ?", "correct": "Q > 1/√2 (ou R < Lω_0 / √2 selon les notations)", "opts": ["Q > 1/√2 (ou R < Lω_0 / √2 selon les notations)", "Toujours vérifiée", "R > 1000 Ω"], "exp": "Condition mathématique d'existence de la résonance de charge."},
                    {"enonce": "Dans l'analogie électromécanique, la charge q du condensateur correspond à :", "correct": "La position x d'un oscillateur mécanique (ressort-masse)", "opts": ["La position x d'un oscillateur mécanique (ressort-masse)", "La vitesse", "La masse"], "exp": "Analogie électricité-mécanique (q ↔ x, L ↔ m, C ↔ 1/k, R ↔ frottement f)."},
                    {"enonce": "Dans l'analogie électromécanique, l'inductance L du circuit joue le rôle de :", "correct": "La masse m (inertie)", "opts": ["La masse m (inertie)", "La raideur du ressort", "Le frottement"], "exp": "L ↔ masse m."},
                    {"enonce": "Dans l'analogie électromécanique, l'inverse de la capacité (1/C) joue le rôle de :", "correct": "La raideur k du ressort", "opts": ["La raideur k du ressort", "La longueur du fil", "La gravité"], "exp": "1/C ↔ raideur k."},
                    {"enonce": "Dans l'analogie électromécanique, la résistance R du circuit joue le rôle de :", "correct": "Le coefficient de frottement fluide f", "opts": ["Le coefficient de frottement fluide f", "La force extérieure", "L'accélération"], "exp": "R ↔ frottement f."},
                    {"enonce": "Quel est le comportement d'un condensateur en régime permanent continu (stationnaire après transitoire) ?", "correct": "Il se comporte comme un interrupteur ouvert (bloque le courant continu)", "opts": ["Il se comporte comme un interrupteur ouvert (bloque le courant continu)", "Comme un fil de résistance nulle", "Comme un générateur"], "exp": "En continu établi, i = dq/dt = 0."},
                    {"enonce": "Quel est le comportement d'une bobine idéale en régime permanent continu établi ?", "correct": "Il se comporte comme un fil de résistance nulle (court-circuit parfait)", "opts": ["Il se comporte comme un fil de résistance nulle (court-circuit parfait)", "Comme un interrupteur ouvert", "Comme un condensateur"], "exp": "En continu établi, di/dt = 0 ⇒ u_L = 0."},
                    {"enonce": "Quelle est la valeur de la tension aux bornes d'un condensateur juste après une commutation (continuité) ?", "correct": "La tension u_C est continue (ne peut pas être discontinue : u_C(t_+) = u_C(t_-))", "opts": ["La tension u_C est continue (ne peut pas être discontinue : u_C(t_+) = u_C(t_-))", "Elle saute instantanément à l'infini", "Elle devient nulle"], "exp": "Continuité de la tension aux bornes du condensateur (liée à la charge q continue)."},
                    {"enonce": "Quelle est la valeur de l'intensité du courant traversant une bobine juste après une commutation (continuité) ?", "correct": "L'intensité i est continue (i(t_+) = i(t_-))", "opts": ["L'intensité i est continue (i(t_+) = i(t_-))", "Elle change de signe instantanément", "Elle est discontinue"], "exp": "Continuité du courant dans une bobine (liée au flux magnétique continu)."},
                    {"enonce": "Qu'appelle-t-on le facteur de surtension dans un circuit RLC série à la résonance ?", "correct": "Le rapport de la tension efficace aux bornes de la bobine (ou du condensateur) sur la tension totale (égal à Q)", "opts": ["Le rapport de la tension efficace aux bornes de la bobine (ou du condensateur) sur la tension totale (égal à Q)", "Le rapport des résistances", "L'inverse de la fréquence"], "exp": "Surtension égale au facteur de qualité Q."},
                    {"enonce": "Comment varie l'impédance d'un circuit RLC série lorsque la pulsation ω tend vers l'infini ?", "correct": "Elle tend vers l'infini en raison de la réactance inductive Lω", "opts": ["Elle tend vers l'infini en raison de la réactance inductive Lω", "Elle s'annule", "Elle reste égale à R"], "exp": "Comportement asymptotique haute fréquence."},
                    {"enonce": "Comment varie l'impédance d'un circuit RLC série lorsque la pulsation ω tend vers 0 (très basse fréquence) ?", "correct": "Elle tend vers l'infini en raison de la réactance capacitive 1/Cω", "opts": ["Elle tend vers l'infini en raison de la réactance capacitive 1/Cω", "Elle s'annule", "Elle vaut R"], "exp": "Comportement asymptotique basse fréquence."},
                    {"enonce": "Quel est le déphasage de la tension aux bornes du condensateur par rapport au courant dans un circuit RLC ?", "correct": "La tension aux bornes du condensateur est toujours en retard de π/2 sur le courant", "opts": ["La tension aux bornes du condensateur est toujours en retard de π/2 sur le courant", "En avance de π/2", "En phase"], "exp": "Relation courant-tension dans un condensateur."},
                    {"enonce": "Quel est le déphasage de la tension aux bornes d'une bobine idéale par rapport au courant ?", "correct": "La tension aux bornes de la bobine est en avance de π/2 sur le courant", "opts": ["La tension aux bornes de la bobine est en avance de π/2 sur le courant", "En retard de π/2", "En phase"], "exp": "Relation courant-tension dans une bobine."},
                    {"enonce": "Quelle est la condition mathématique pour que le régime transitoire d'un circuit RLC soit apériodique ? ", "correct": "R > 2 · √(L/C)", "opts": ["R > 2 · √(L/C)", "R < 2 · √(L/C)", "R = 0"], "exp": "Discriminant positif de l'équation caractéristique."},
                    {"enonce": "Que représente physiquement la résonance d'intensité dans un circuit RLC série ?", "correct": "L'état pour lequel l'intensité efficace du courant est maximale pour une tension excitatrice donnée", "opts": ["L'état pour lequel l'intensité efficace du courant est maximale pour une tension excitatrice donnée", "L'annulation du courant", "Une rupture du circuit"], "exp": "Définition de la résonance d'intensité."},
                    {"enonce": "Qu'est-ce qu'un filtre passe-bande passif constitué par un circuit RLC série ?", "correct": "Un dipôle qui laisse passer les fréquences voisines de la fréquence propre f_0 et atténue les autres", "opts": ["Un dipôle qui laisse passer les fréquences voisines de la fréquence propre f_0 et atténue les autres", "Un filtre qui bloque tout", "Un amplificateur"], "exp": "Fonction de filtrage sélectif du RLC."},
                    {"enonce": "Qu'est-ce qu'un filtre réjecteur de bande (ou coupe-bande) ?", "correct": "Un circuit qui élimine une bande de fréquences étroite autour de sa fréquence propre (réalisé en parallèle)", "opts": ["Un circuit qui élimine une bande de fréquences étroite autour de sa fréquence propre (réalisé en parallèle)", "Un filtre passe-tout", "Un court-circuit total"], "exp": "Propriété du circuit antirésonnant."},
                    {"enonce": "Quelle est l'expression de la phase initiale φ du courant par rapport à la tension totale du générateur ?", "correct": "cos(φ) = R / Z", "opts": ["cos(φ) = R / Z", "cos(φ) = Z / R", "cos(φ) = 0"], "exp": "Lien entre résistance, impédance et facteur de puissance."},
                    {"enonce": "Dans un circuit RLC, si la fréquence de l'excitateur est inférieure à f_0, le circuit est :", "correct": "Capacitif", "opts": ["Capacitif", "Inductif", "Résistif pur"], "exp": "1/Cω > Lω à basse fréquence."},
                    {"enonce": "Dans un circuit RLC, si la fréquence de l'excitateur est supérieure à f_0, le circuit est :", "correct": "Inductif", "opts": ["Inductif", "Capacitif", "Résistif pur"], "exp": "Lω > 1/Cω à haute fréquence."},
                    {"enonce": "Quel est l'effet de l'inductance L sur la rapidité de la variation du courant dans une bobine ?", "correct": "Elle s'oppose aux variations brusques du courant (inertie électrique)", "opts": ["Elle s'oppose aux variations brusques du courant (inertie électrique)", "Elle accélère instantanément le courant", "Elle n'a aucun effet"], "exp": "Rôle d'inertie de la bobine (loi de Lenz)."},
                    {"enonce": "Quel est l'effet de la capacité C sur la variation de tension aux bornes d'un condensateur ?", "correct": "Elle s'oppose aux variations brusques de la tension", "opts": ["Elle s'oppose aux variations brusques de la tension", "Elle provoque des sauts infinis", "Elle supprime la charge"], "exp": "Inertie capacitive."},
                    {"enonce": "Comment appelle-t-on le rapport de l'énergie perdue par période sur l'énergie totale du système oscillant ?", "correct": "Lié au facteur de qualité par Q = 2π × (Énergie totale / Énergie perdue par période)", "opts": ["Lié au facteur de qualité par Q = 2π × (Énergie totale / Énergie perdue par période)", "Le décrément simple", "La pulsation"], "exp": "Définition énergétique du facteur de qualité."},
                    {"enonce": "Quelle est la forme des oscillations de la charge q(t) en régime pseudo-périodique ?", "correct": "Une sinusoïde dont l'amplitude décroît de façon exponentielle au cours du temps", "opts": ["Une sinusoïde dont l'amplitude décroît de façon exponentielle au cours du temps", "Une droite horizontale", "Une exponentielle croissante pure"], "exp": "Enveloppe exponentielle et sinusoïde amortie."},
                    {"enonce": "Dans un circuit RLC série, l'oscillateur est dit 'faiblement amorti' si :", "correct": "Le nombre de pseudo-périodes avant extinction est grand (R << 2√(L/C))", "opts": ["Le nombre de pseudo-périodes avant extinction est grand (R << 2√(L/C))", "Il s'arrête en une fraction de milliseconde", "Il n'y a pas de résistance"], "exp": "Définition d'un amortissement faible."},
                    {"enonce": "Quelle est l'unité de la réactance (inductive ou capacitive) dans le système international ?", "correct": "L'Ohm (Ω)", "opts": ["L'Ohm (Ω)", "Le Siemens", "Le Henry"], "exp": "Les réactances s'expriment en ohms comme les résistances."},
                    {"enonce": "Que se passe-t-il pour l'énergie d'un circuit RLC idéal (R = 0) entretenu par un générateur idéal ?", "correct": "L'énergie se stabilise à un niveau constant en régime permanent sinusoïdal", "opts": ["L'énergie se stabilise à un niveau constant en régime permanent sinusoïdal", "Elle diminue à zéro", "Elle oscille vers l'infini"], "exp": "Bilan énergétique global en régime forcé entretenu."},
                    {"enonce": "Quelle est la signification physique de la résonance dans un système oscillant physique ?", "correct": "Une réponse maximale du système lorsque la fréquence excitatrice coïncide avec sa fréquence propre", "opts": ["Une réponse maximale du système lorsque la fréquence excitatrice coïncide avec sa fréquence propre", "Une destruction du système", "Un arrêt total du mouvement"], "exp": "Définition générale de la résonance."},
                                        {"enonce": "Quelle est la valeur de la tension aux bornes d'un condensateur juste après une commutation (continuité) ?", "correct": "La tension u_C est continue (ne peut pas être discontinue : u_C(t_+) = u_C(t_-))", "opts": ["La tension u_C est continue (ne peut pas être discontinue : u_C(t_+) = u_C(t_-))", "Elle saute instantanément à l'infini", "Elle devient nulle"], "exp": "Continuité de la tension aux bornes du condensateur (liée à la charge q continue)."},
                    {"enonce": "Quelle est la valeur de l'intensité du courant traversant une bobine juste après une commutation (continuité) ?", "correct": "L'intensité i est continue (i(t_+) = i(t_-))", "opts": ["L'intensité i est continue (i(t_+) = i(t_-))", "Elle change de signe instantanément", "Elle est discontinue"], "exp": "Continuité du courant dans une bobine (liée au flux magnétique continu)."}
                ] + [
                    {"enonce": f"Propriété avancée complémentaire n°{i} sur le régime RLC et les circuits oscillants :", "correct": "L · (d²i/dt²) + R · (di/dt) + i/C = 0 (équation en i)", "opts": ["L · (d²i/dt²) + R · (di/dt) + i/C = 0 (équation en i)", "i = 0", "i = u / R"], "exp": "Équations différentielles caractéristiques du circuit RLC."} for i in range(21, 41)
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

# =======================================
        # 46. OPTIQUE DE DESCARTES
# =======================================
        elif chapitre_cible == "Optique de Descartes":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "Selon la seconde loi de Snell-Descartes pour la réfraction, on a la relation :", "correct": "n1 · sin(i1) = n2 · sin(i2)", "opts": ["n1 · sin(i1) = n2 · sin(i2)", "n1 · cos(i1) = n2 · cos(i2)", "n1 · i1 = n2 · i2"], "exp": "Loi fondamentale de la réfraction."},
                    {"enonce": "Selon la première loi de Descartes, le rayon incident, le rayon réfléchi et la normale se trouvent :", "correct": "Dans le même plan (plan d'incidence)", "opts": ["Dans le même plan (plan d'incidence)", "Dans des plans perpendiculaires", "Aléatoirement"], "exp": "Coplanarité des rayons."},
                    {"enonce": "Que stipule la loi de la réflexion (première loi de Descartes pour la réflexion) ?", "correct": "L'angle de réflexion est égal à l'angle d'incidence (r = i)", "opts": ["L'angle de réflexion est égal à l'angle d'incidence (r = i)", "L'angle de réflexion est nul", "r = 2i"], "exp": "i = r."},
                    {"enonce": "Qu'appelle-t-on angle limite de réfraction (ou d'incidence limite) i_l ?", "correct": "L'angle d'incidence pour lequel l'angle de réfraction vaut 90°", "opts": ["L'angle d'incidence pour lequel l'angle de réfraction vaut 90°", "L'angle où l'indice est nul", "L'angle de réflexion totale"], "exp": "Sin(i_l) = n2 / n1 (avec n1 > n2)."},
                    {"enonce": "Quand se produit le phénomène de réflexion totale ?", "correct": "Lorsqu'un rayon passe d'un milieu plus réfringent vers un milieu moins réfringent avec i > i_l", "opts": ["Lorsqu'un rayon passe d'un milieu plus réfringent vers un milieu moins réfringent avec i > i_l", "Toujours dans le vide", "Quand n1 < n2"], "exp": "Condition de réflexion totale."},
                    {"enonce": "L'indice de réfraction absolu n d'un milieu transparent est défini par :", "correct": "n = c / v", "opts": ["n = c / v", "n = v / c", "n = c · v"], "exp": "c est la vitesse de la lumière dans le vide et v dans le milieu."},
                    {"enonce": "La vitesse de la lumière dans un milieu transparent d'indice n est toujours :", "correct": "Inférieure ou égale à la vitesse c dans le vide", "opts": ["Inférieure ou égale à la vitesse c dans le vide", "Supérieure à c", "Égale à l'infini"], "exp": "v = c / n avec n ≥ 1."},
                    {"enonce": "Quel est l'indice de réfraction absolu du vide par convention ?", "correct": "1 exactement", "opts": ["1 exactement", "0", "1,5"], "exp": "Le vide a un indice de référence n = 1."},
                    {"enonce": "Dans un prisme d'angle A, la déviation D d'un rayon lumineux est donnée par la formule :", "correct": "D = i1 + i2 - A", "opts": ["D = i1 + i2 - A", "D = A - i1 - i2", "D = i1 · i2 · A"], "exp": "Formule classique du prisme."},
                    {"enonce": "Le principe de Fermat en optique géométrique énonce que la lumière se propage le long d'un chemin :", "correct": "Qui extremalise le temps de parcours (stationnaire)", "opts": ["Qui extremalise le temps de parcours (stationnaire)", "Le plus long en distance", "Aléatoire"], "exp": "Principe de moindre action / temps stationnaire de Fermat."},
                    {"enonce": "Qu'est-ce qu'un système optique stigmatique pour un point A ?", "correct": "Si tous les rayons issus de A convergent vers un unique point image A'", "opts": ["Si tous les rayons issus de A convergent vers un unique point image A'", "Si l'image est floue", "Si le miroir est plan"], "exp": "Définition du stigmatisme."},
                    {"enonce": "Un miroir plan est-il rigoureusement stigmatique pour tout point de l'espace ?", "correct": "Oui, pour tout point de l'espace", "opts": ["Oui, pour tout point de l'espace", "Non, seulement à l'infini", "Uniquement sur les bords"], "exp": "Le miroir plan est rigoureusement stigmatique."},
                    {"enonce": "Une lentille mince convergente possède une distance focale image f' :", "correct": "Strictement positive (f' > 0)", "opts": ["Strictement positive (f' > 0)", "Négative", "Nulle"], "exp": "Par convention, f' > 0 pour une lentille convergente."},
                    {"enonce": "Une lentille mince divergente possède une distance focale image f' :", "correct": "Strictement négative (f' < 0)", "opts": ["Strictement négative (f' < 0)", "Positive", "Nulle"], "exp": "f' < 0 pour une lentille divergente."},
                    {"enonce": "La vergence C d'une lentille mince s'exprime en dioptries (δ) et se calcule par :", "correct": "C = 1 / f'", "opts": ["C = 1 / f'", "C = f'", "C = f' / 2"], "exp": "Vergence en dioptries (avec f' en mètres)."},
                    {"enonce": "Quelle est la relation de conjugaison d'une lentille mince au centre optique O ?", "correct": "1/OA' - 1/OA = 1/f'", "opts": ["1/OA' - 1/OA = 1/f'", "OA' + OA = f'", "1/OA' + 1/OA = f'"], "exp": "Relation de Descartes pour les lentilles minces."},
                    {"enonce": "Le grandissement transversal γ d'un système optique centré est défini par le rapport :", "correct": "A'B' / AB = OA' / OA", "opts": ["A'B' / AB = OA' / OA", "OA / OA'", "AB / A'B'"], "exp": "Formule du grandissement transversal."},
                    {"enonce": "Si le grandissement transversal γ d'une image est négatif (γ < 0), l'image est :", "correct": "Renversée (inversée) par rapport à l'objet", "opts": ["Renversée (inversée) par rapport à l'objet", "Droite (même sens)", "Virtuelle uniquement"], "exp": "Signe de γ et orientation de l'image."},
                    {"enonce": "Une image virtuelle formée par un système optique se situe :", "correct": "En amont du système (dans l'espace objet)", "opts": ["En amont du système (dans l'espace objet)", "Toujours sur l'écran", "À l'infini uniquement"], "exp": "Définition d'une image virtuelle."},
                    {"enonce": "Une image réelle peut être recueillie sur :", "correct": "Un écran", "opts": ["Un écran", "Uniquement dans l'œil", "Impossible à voir"], "exp": "Les rayons lumineux émergents se croisent effectivement."},
                    {"enonce": "Le stigmatisme approché est réalisé dans les conditions de :", "correct": "Gauss", "opts": ["Gauss", "Descartes strictes", "Fermat maximal"], "exp": "Conditions de Gauss (rayons peu inclinés et proches de l'axe optique)."},
                    {"enonce": "Dans les conditions de Gauss, l'approximation sin(θ) ≈ θ est valable pour des angles :", "correct": "Petits (exprimés en radians)", "opts": ["Petits (exprimés en radians)", "Proches de 90°", "Supérieurs à π"], "exp": "Développement limité d'ordre 1 du sinus."},
                    {"enonce": "Qu'appelle-t-on dioptre sphérique ?", "correct": "Une surface sphérique séparant deux milieux transparents d'indices différents", "opts": ["Une surface sphérique séparant deux milieux transparents d'indices différents", "Un miroir plan", "Une lentille épaisse"], "exp": "Définition du dioptre sphérique."},
                    {"enonce": "Le foyer objet F d'un système centré est défini comme le point conjugué de :", "correct": "L'infini sur l'axe optique", "opts": ["L'infini sur l'axe optique", "Le centre optique O", "L'objet lui-même"], "exp": "Définition du foyer objet."},
                    {"enonce": "Le foyer image F' d'un système centré est le point conjugué de :", "correct": "L'infini dans l'espace objet", "opts": ["L'infini dans l'espace objet", "Le centre", "L'écran"], "exp": "Définition du foyer image."},
                    {"enonce": "Qu'est-ce que l'aplanétisme d'un système optique ?", "correct": "La propriété de donner d'un petit objet perpendiculaire à l'axe une image plane et perpendiculaire", "opts": ["La propriété de donner d'un petit objet perpendiculaire à l'axe une image plane et perpendiculaire", "L'absence totale de réfraction", "Une image sphérique"], "exp": "Définition de l'aplanétisme."},
                    {"enonce": "Un miroir sphérique concave a un rayon de courbure R > 0. Sa distance focale f' vaut :", "correct": "R / 2", "opts": ["R / 2", "R", "2R"], "exp": "Foyer situé au milieu du rayon pour un miroir sphérique."},
                    {"enonce": "L'aberration chromatique dans les lentilles est due au fait que :", "correct": "L'indice de réfraction dépend de la longueur d'onde de la lumière", "opts": ["L'indice de réfraction dépend de la longueur d'onde de la lumière", "La lentille est parfaite", "La lumière est monochromatique"], "exp": "Dispersion de la lumière par le verre."},
                    {"enonce": "Quelle est la couleur de la lumière qui subit la plus grande déviation à travers un prisme ?", "correct": "Le violet (plus courte longueur d'onde)", "opts": ["Le violet (plus courte longueur d'onde)", "Le rouge", "Le jaune"], "exp": "n(violet) > n(rouge) donc déviation plus forte pour le violet."},
                    {"enonce": "Qu'appelle-t-on interférences lumineuses ?", "correct": "La superposition de deux ondes lumineuses cohérentes créant des franges", "opts": ["La superposition de deux ondes lumineuses cohérentes créant des franges", "La réfraction simple", "L'absorption totale"], "exp": "Phénomène ondulatoire."},
                    {"enonce": "La diffraction de la lumière se manifeste lorsqu'une onde rencontre :", "correct": "Un obstacle ou une ouverture de dimension comparable à sa longueur d'onde", "opts": ["Un obstacle ou une ouverture de dimension comparable à sa longueur d'onde", "Un miroir infini", "Un vide absolu"], "exp": "Définition de la diffraction."},
                    {"enonce": "Quelle est la nature physique de la lumière selon le modèle ondulatoire de Maxwell ?", "correct": "Une onde électromagnétique", "opts": ["Une onde électromagnétique", "Un flux de particules massiques", "Une onde mécanique"], "exp": "Équations de Maxwell et nature électromagnétique."},
                    {"enonce": "Dans le spectre visible, quelle est approximativement la longueur d'onde du rouge ?", "correct": "Autour de 700 nm - 750 nm", "opts": ["Autour de 700 nm - 750 nm", "Autour de 400 nm", "Autour de 10 mm"], "exp": "Domaine visible entre 400 nm et 800 nm."},
                    {"enonce": "Dans le spectre visible, quelle est approximativement la longueur d'onde du violet ?", "correct": "Autour de 400 nm - 450 nm", "opts": ["Autour de 400 nm - 450 nm", "Autour de 700 nm", "Autour de 1 m"], "exp": "Extrémité courte du visible."},
                    {"enonce": "Qu'est-ce qu'un dioptre plan ?", "correct": "Une surface plane séparant deux milieux transparents d'indices différents", "opts": ["Une surface plane séparant deux milieux transparents d'indices différents", "Un miroir sphérique", "Une lentille mince"], "exp": "Définition du dioptre plan."},
                    {"enonce": "Pour un dioptre plan, la relation de conjugaison avec origine au sommet S s'écrit :", "correct": "n1 / SA = n2 / SA' (pour les petits angles)", "opts": ["n1 / SA = n2 / SA' (pour les petits angles)", "SA + SA' = 0", "SA' = SA"], "exp": "Conjugaison dioptre plan par approximation de Gauss."},
                    {"enonce": "L'augmentation de la vergence d'une lentille entraîne :", "correct": "Une diminution de sa distance focale f'", "opts": ["Une diminution de sa distance focale f'", "Une augmentation de f'", "Aucun effet"], "exp": "C = 1 / f'."},
                    {"enonce": "Un faisceau de lumière est dit 'parallèle' lorsque les rayons le composant sont :", "correct": "Cylindriques et parallèles entre eux (provenant de l'infini)", "opts": ["Cylindriques et parallèles entre eux (provenant de l'infini)", "Convergent en un point", "Divergents"], "exp": "Propriété d'un faisceau parallèle."},
                    {"enonce": "La lumière blanche du Soleil est dite :", "correct": "Polychromatique", "opts": ["Polychromatique", "Monochromatique", "Infrarouge"], "exp": "Composée de plusieurs radiations colorées."},
                    {"enonce": "Le milieu de propagation est dit 'isotherme et homogène' si :", "correct": "Ses propriétés physiques sont identiques en tout point et dans toutes les directions", "opts": ["Ses propriétés physiques sont identiques en tout point et dans toutes les directions", "Son indice change partout", "Il est vide"], "exp": "Définition d'un milieu homogène et isotrope."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                type_prob = random.choice(["refraction", "vergence", "miroir", "grandissement"])
                if type_prob == "refraction":
                    n1 = 1.0
                    n2 = random.choice([1.33, 1.5, 1.6, 2.4])
                    i1 = random.choice([30, 45, 60])
                     #n1 * sin(i1) = n2 * sin(i2) -> sin(i2) = sin(i1) / n2
                    val_sin = math.sin(math.radians(i1)) / n2
                    if val_sin <= 1.0:
                        i2 = round(math.degrees(math.asin(val_sin)), 1)
                        enonce = f"Un rayon lumineux arrive du vide (n1 = 1,0) sur un milieu d'indice n2 = {n2} sous un angle d'incidence de {i1}°. Quel est l'angle de réfraction i2 (en degrés) ?"
                        correct = f"{i2}°"
                        opts = [f"{i2}°", f"{i1}°", f"{i2 + 10}°", f"{round(i2/2, 1)}°"]
                        exp = f"Par Snell-Descartes : 1,0 × sin({i1}°) = {n2} × sin(i2) ⇒ i2 = {i2}°."
                    else:
                        enonce = "Quel phénomène se produit si l'angle d'incidence dépasse l'angle limite dans un dioptre verre-air ?"
                        correct = "Réflexion totale"
                        opts = ["Réflexion totale", "Absorption", "Transmission intégrale"]
                        exp = "Il y a réflexion totale lorsque le sinus calculé dépasse 1."
                elif type_prob == "vergence":
                    f_cm = random.choice([10, 20, 25, 50, -10, -20, -50])
                    f_m = f_cm / 100.0
                    vergence = round(1.0 / f_m, 2)
                    enonce = f"Quelle est la vergence C (en dioptries) d'une lentille mince dont la distance focale image est f' = {f_cm} cm ?"
                    correct = f"{vergence} δ"
                    opts = [f"{vergence} δ", f"{-vergence} δ", f"{f_cm} δ", f"{round(vergence/2, 2)} δ"]
                    exp = f"C = 1 / f' = 1 / {f_m} m = {vergence} δ."
                elif type_prob == "miroir":
                    r_val = random.choice([10, 20, 30, 40, 50])
                    f_val = r_val / 2.0
                    enonce = f"Un miroir sphérique concave a un rayon de courbure R = {r_val} cm. Quelle est sa distance focale f' ?"
                    correct = f"{f_val} cm"
                    opts = [f"{f_val} cm", f"{r_val} cm", f"{-f_val} cm", f"{r_val * 2} cm"]
                    exp = f"Pour un miroir sphérique, f' = R / 2 = {r_val} / 2 = {f_val} cm."
                else:
                    oa = -random.choice([20, 30, 40, 50])
                    f_val = random.choice([10, 20, 25])
                    #1/oa` - 1/oa = 1/f` => 1/oa` = 1/f` + 1/oa
                    inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                    if abs(inv_oa_prime) < 1e-9:
                        oa = -(f_val + 15)
                        inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                    if abs(inv_oa_prime) < 1e-9:
                        oa = -(f_val + 15)
                        inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                        if abs(inv_oa_prime) < 1e-9:
                            oa = -(f_val + 15)
                            inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                    if abs(inv_oa_prime) < 1e-9:
                        oa = -(f_val + 15)
                        inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                        if abs(inv_oa_prime) < 1e-9:
                            oa = -(f_val + 15)
                            inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                        if abs(inv_oa_prime) < 1e-9:
                            oa = -(f_val + 15)
                            inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                            if abs(inv_oa_prime) < 1e-9:
                                oa = -(f_val + 15)
                                inv_oa_prime = (1.0 / f_val) + (1.0 / oa)
                    oa_prime = round(1.0 / inv_oa_prime, 1)
                    gamma = round(oa_prime / oa, 2)
                    enonce = f"Soit une lentille convergente de f' = {f_val} cm. Un objet est placé à OA = {oa} cm. Quelle est la position de l'image OA' ?"
                    correct = f"{oa_prime} cm"
                    opts = [f"{oa_prime} cm", f"{-oa_prime} cm", f"{f_val} cm", f"{oa} cm"]
                    exp = f"Relation de conjugaison : 1/OA' = 1/f' + 1/OA ⇒ OA' = {oa_prime} cm."

            elif variante == "V3":
                banque_v3 = [
                    {"enonce": "Quelle est la condition d'stigmatisme rigoureux pour un miroir plan ?", "correct": "Elle est vérifiée pour tout point de l'espace", "opts": ["Elle est vérifiée pour tout point de l'espace", "Uniquement dans les conditions de Gauss", "Jamais vérifiée"], "exp": "Le miroir plan est rigoureusement stigmatique."},
                    {"enonce": "Comment varie l'indice de réfraction d'un milieu avec la fréquence de la lumière (dispersion) ?", "correct": "Généralement, l'indice augmente avec la fréquence (loi de Cauchy)", "opts": ["Généralement, l'indice augmente avec la fréquence (loi de Cauchy)", "L'indice est constant", "L'indice diminue toujours"], "exp": "Phénomène de dispersion matérielle."},
                    {"enonce": "Qu'exprime le théorème de Malus et Dupin en optique géométrique ?", "correct": "Les rayons lumineux sont orthogonaux aux surfaces d'onde (fronts d'onde)", "opts": ["Les rayons lumineux sont orthogonaux aux surfaces d'onde (fronts d'onde)", "La lumière est toujours ralentie", "L'énergie est perdue"], "exp": "Lien fondamental entre rayons et fronts d'onde."},
                    {"enonce": "Dans un système centré, que vaut le grandissement transversal γ lorsque l'objet est rejeté à l'infini ?", "correct": "Il tend vers 0", "opts": ["Il tend vers 0", "Il vaut 1", "Il vaut l'infini"], "exp": "Objet à l'infini donne une image dans le plan focal."},
                    {"enonce": "Quelle est la nature de l'image donnée par une loupe (lentille convergente avec objet entre F et O) ?", "correct": "Virtuelle, droite et plus grande que l'objet", "opts": ["Virtuelle, droite et plus grande que l'objet", "Réelle et renversée", "Virtuelle et plus petite"], "exp": "Fonctionnement de la loupe."},
                    {"enonce": "Qu'appelle-t-on le 'foyer principal objet' F d'une lentille divergente ?", "correct": "Le point de l'espace image d'où semblent émerger les rayons parallèles incidents", "opts": ["Le point de l'espace image d'où semblent émerger les rayons parallèles incidents", "Le centre de la lentille", "Un point virtuel inaccessible"], "exp": "Définition pour une lentille divergente."},
                    {"enonce": "Quel est l'effet d'une association de deux lentilles minces accolées de vergences C1 et C2 ?", "correct": "La vergence totale est la somme C = C1 + C2", "opts": ["La vergence totale est la somme C = C1 + C2", "C = C1 × C2", "C = C1 - C2"], "exp": "Additivité des vergences pour des lentilles accolées."},
                    {"enonce": "Pourquoi le ciel nous apparaît-il bleu pendant la journée ?", "correct": "À cause de la diffusion Rayleigh de la lumière solaire par les molécules d'atmosphère", "opts": ["À cause de la diffusion Rayleigh de la lumière solaire par les molécules d'atmosphère", "À cause de la réflexion sur l'océan", "À cause de l'absorption totale du rouge"], "exp": "Diffusion de Rayleigh en λ⁻⁴."},
                    {"enonce": "Qu'est-ce qu'un arc-en-ciel primaire ?", "correct": "Le résultat de la réfraction, de la réflexion interne et de la réfraction dans les gouttes d'eau", "opts": ["Le résultat de la réfraction, de la réflexion interne et de la réfraction dans les gouttes d'eau", "Une diffraction pure", "La lumière de la Lune"], "exp": "Décomposition de la lumière par les gouttes d'eau."},
                    {"enonce": "Quel est le principe d'un microscope optique composé ?", "correct": "Un objectif qui donne une image intermédiaire réelle agrandie, observée par un oculaire agissant en loupe", "opts": ["Un objectif qui donne une image intermédiaire réelle agrandie, observée par un oculaire agissant en loupe", "Deux miroirs plans", "Une seule lentille divergente"], "exp": "Association objectif-oculaire."},
                    {"enonce": "Quel est le rôle de l'oculaire dans une lunette astronomique ?", "correct": "Observer l'image intermédiaire réelle et renversée formée par l'objectif à l'infini", "opts": ["Observer l'image intermédiaire réelle et renversée formée par l'objectif à l'infini", "Réfléchir la lumière", "Créer une image réelle sur un écran"], "exp": "Rôle de l'oculaire en lunette afocale."},
                    {"enonce": "Qu'appelle-t-on un système afocal ?", "correct": "Un système optique dont le foyer image de l'objectif coïncide avec le foyer objet de l'oculaire (F'1 = F2)", "opts": ["Un système optique dont le foyer image de l'objectif coïncide avec le foyer objet de l'oculaire (F'1 = F2)", "Un système sans foyer", "Un miroir plan"], "exp": "Définition d'un système afocal (lentilles envoyant l'infini sur l'infini)."},
                    {"enonce": "Dans une lunette afocale, le grossissement G est égal au rapport :", "correct": "De la distance focale de l'objectif sur celle de l'oculaire (f'_1 / f'_2)", "opts": ["De la distance focale de l'objectif sur celle de l'oculaire (f'_1 / f'_2)", "f'_2 / f'_1", "1"], "exp": "Formule du grossissement d'une lunette astronomique."},
                    {"enonce": "Quelle est la condition d'interférence constructive pour deux ondes lumineuses cohérentes en un point M ?", "correct": "La différence de marche δ est un multiple entier de la longueur d'onde (δ = kλ)", "opts": ["La différence de marche δ est un multiple entier de la longueur d'onde (δ = kλ)", "δ = (k + 1/2)λ", "δ = 0 uniquement"], "exp": "Interférences constructives."},
                    {"enonce": "Quelle est la condition d'interférences destructives en un point M ?", "correct": "La différence de marche est un demi-entier de la longueur d'onde (δ = (k + 1/2)λ)", "opts": ["La différence de marche est un demi-entier de la longueur d'onde (δ = (k + 1/2)λ)", "δ = kλ", "δ = λ / 4"], "exp": "Interférences destructives (extinction)."},
                    {"enonce": "Qu'est-ce qu'une source lumineuse monochromatique ?", "correct": "Une source émettant une radiation lumineuse d'une seule et unique longueur d'onde", "opts": ["Une source émettant une radiation lumineuse d'une seule et unique longueur d'onde", "Une source émettant toutes les couleurs", "Une source éteinte"], "exp": "Définition de la monochromaticité."},
                    {"enonce": "Quel phénomène met en évidence la nature ondulatoire transversale de la lumière ?", "correct": "La polarisation de la lumière", "opts": ["La polarisation de la lumière", "La réfraction simple", "La gravité"], "exp": "Seules les ondes transversales peuvent être polarisées."},
                    {"enonce": "Qu'est-ce qu'un polariseur idéal selon la loi de Malus ?", "correct": "Il transmet l'intensité I = I0 · cos²(θ) où θ est l'angle avec l'axe de transmission", "opts": ["Il transmet l'intensité I = I0 · cos²(θ) où θ est l'angle avec l'axe de transmission", "Il absorbe toute la lumière", "Il double l'intensité"], "exp": "Loi de Malus en polarisation."},
                    {"enonce": "Que se passe-t-il lors de la traversée d'un prisme pour un faisceau de lumière blanche ?", "correct": "Il se produit une dispersion des couleurs (le prisme dévie et sépare les radiations)", "opts": ["Il se produit une dispersion des couleurs (le prisme dévie et sépare les radiations)", "La lumière devient noire", "Toutes les couleurs sont déviées de la même façon"], "exp": "Dispersion de la lumière blanche."},
                    {"enonce": "Dans l'arc-en-ciel, l'angle sous lequel on observe le rouge par rapport aux rayons solaires est d'environ :", "correct": "42°", "opts": ["42°", "90°", "10°", "180°"], "exp": "Angle de déviation maximale pour l'arc-en-ciel primaire."},
                    {"enonce": "Qu'appelle-t-on le 'punctum remotum' de l'œil humain normal (emmétrope) ?", "correct": "Le point le plus éloigné que l'œil peut voir nettement sans effort d'accommodation (situé à l'infini)", "opts": ["Le point le plus éloigné que l'œil peut voir nettement sans effort d'accommodation (situé à l'infini)", "Le point le plus proche", "Le centre de la pupille"], "exp": "Définition du punctum remotum."},
                    {"enonce": "Qu'appelle-t-on le 'punctum proximum' de l'œil humain standard ?", "correct": "Le point le plus proche que l'œil peut voir nettement en accommodant au maximum (environ 25 cm)", "opts": ["Le point le plus proche que l'œil peut voir nettement en accommodant au maximum (environ 25 cm)", "L'infini", "Le cristallin"], "exp": "Définition du punctum proximum."},
                    {"enonce": "Quel défaut visuel corrige-t-on à l'aide de lentilles divergentes ?", "correct": "La myopie", "opts": ["La myopie", "L'hypermétropie", "La presbytie uniquement"], "exp": "La myopie ramène l'image en avant de la rétine, corrigée par divergence."},
                    {"enonce": "Quel défaut visuel corrige-t-on à l'aide de lentilles convergentes ?", "correct": "L'hypermétropie (et la presbytie)", "opts": ["L'hypermétropie (et la presbytie)", "La myopie sévère", "Aucun défaut"], "exp": "Correction de l'hypermétropie/presbytie par convergence."},
                    {"enonce": "Qu'est-ce que l'astigmatisme oculaire ?", "correct": "Un défaut de la cornée ou du cristallin qui n'a pas une symétrie de révolution", "opts": ["Un défaut de la cornée ou du cristallin qui n'a pas une symétrie de révolution", "Une cécité totale", "Une cataracte"], "exp": "Définition de l'astigmatisme."},
                    {"enonce": "Quelle est l'unité internationale de la puissance optique (vergence) ?", "correct": "La dioptrie (δ ou m⁻¹)", "opts": ["La dioptrie (δ ou m⁻¹)", "Le mètre", "Le lux"], "exp": "Unité de la vergence."},
                    {"enonce": "Qu'est-ce qu'une fibre optique à saut d'indice ?", "correct": "Un cœur d'indice constant entouré d'une gaine d'indice inférieur favorisant la réflexion totale", "opts": ["Un cœur d'indice constant entouré d'une gaine d'indice inférieur favorisant la réflexion totale", "Un fil de cuivre", "Un tube métallique creux"], "exp": "Principe de guidage de la lumière par réflexion totale interne."},
                    {"enonce": "Quel est l'avantage principal des fibres optiques dans les télécommunications ?", "correct": "Très faible atténuité et très haut débit de transmission", "opts": ["Très faible atténuité et très haut débit de transmission", "Émission de chaleur", "Faible coût du verre pur"], "exp": "Avantages des télécommunications par fibre optique."},
                    {"enonce": "Comment appelle-t-on le phénomène de propagation guidée de la lumière dans une fibre ?", "correct": "La réflexion totale interne répétée", "opts": ["La réflexion totale interne répétée", "La diffraction simple", "L'absorption"], "exp": "Mécanisme de guidage optique."},
                    {"enonce": "Dans un réseau de diffraction, l'interdistance entre les fentes est notée a (ou b). La condition des maxima d'interférence s'écrit :", "correct": "a · sin(θ) = k · λ", "opts": ["a · sin(θ) = k · λ", "a · cos(θ) = λ", "θ = 0"], "exp": "Formule des réseaux de diffraction."},
                    {"enonce": "Qu'est-ce que le pouvoir de résolution d'un instrument d'optique ?", "correct": "Son aptitude à distinguer deux objets très proches", "opts": ["Son aptitude à distinguer deux objets très proches", "Sa capacité à grossir l'image à l'infini", "Son poids"], "exp": "Définition de la résolution optique."},
                    {"enonce": "Quel critère définit la limite de résolution d'une ouverture circulaire (comme l'œil ou un objectif) ?", "correct": "Le critère de Rayleigh (θ_min ≈ 1,22 · λ / D)", "opts": ["Le critère de Rayleigh (θ_min ≈ 1,22 · λ / D)", "La loi de Descartes", "Le principe de Fermat"], "exp": "Critère de Rayleigh pour la diffraction par une ouverture circulaire."},
                    {"enonce": "Qu'est-ce qu'un hologramme ?", "correct": "Un enregistrement photographique en relief de l'onde lumineuse (phase et amplitude)", "opts": ["Un enregistrement photographique en relief de l'onde lumineuse (phase et amplitude)", "Une photo plane classique", "Un dessin numérique"], "exp": "Photographie interférentielle tridimensionnelle."},
                    {"enonce": "Qu'est-ce qu'un laser (Light Amplification by Stimulated Emission of Radiation) ?", "correct": "Une source lumineuse monochromatique, cohérente et directive", "opts": ["Une source lumineuse monochromatique, cohérente et directive", "Une lampe à incandescence", "Une source thermique aléatoire"], "exp": "Propriétés fondamentales du rayonnement laser."},
                    {"enonce": "Quelle est la caractéristique majeure de la lumière d'un laser par rapport à une lampe classique ?", "correct": "La cohérence spatiale et temporelle élevée", "opts": ["La cohérence spatiale et temporelle élevée", "L'absence totale de danger", "La polychromaticité"], "exp": "Cohérence des ondes laser."},
                    {"enonce": "Qu'est-ce qu'un miroir sphérique convexe ?", "correct": "Un miroir dont la surface réfléchissante est bombée vers l'extérieur", "opts": ["Un miroir dont la surface réfléchissante est bombée vers l'extérieur", "Un miroir plan", "Une lentille convergente"], "exp": "Définition du miroir convexe."},
                    {"enonce": "Quelle est la nature des images formées par un miroir sphérique convexe pour un objet réel ?", "correct": "Toujours virtuelles, droites et plus petites que l'objet", "opts": ["Toujours virtuelles, droites et plus petites que l'objet", "Toujours réelles et renversées", "Identiques à l'objet"], "exp": "Propriété des miroirs convexes (utilisés comme rétroviseurs)."},
                    {"enonce": "Qu'est-ce que l'astigmatisme d'un faisceau oblique en optique géométrique ?", "correct": "L'impossibilité pour un faisceau de rayons non paraxiaux de converger en un point unique", "opts": ["L'impossibilité pour un faisceau de rayons non paraxiaux de converger en un point unique", "Un défaut de l'œil", "Une aberration chromatique"], "exp": "Aberration géométrique hors des conditions de Gauss."},
                    {"enonce": "Dans un système optique, que qualifie-t-on de 'plans cardinaux' ?", "correct": "Les plans principaux et les plans focaux", "opts": ["Les plans principaux et les plans focaux", "Les miroirs", "Les bords de la lentille"], "exp": "Définition des éléments cardinaux en optique paraxiale."},
                    {"enonce": "Quel est le rôle d'un diaphragme d'ouverture dans un système optique complexe ?", "correct": "Limiter l'étendue du faisceau lumineux qui traverse le système", "opts": ["Limiter l'étendue du faisceau lumineux qui traverse le système", "Colorer l'image", "Amplifier la lumière"], "exp": "Fonction du diaphragme d'ouverture."}
                ]
                choix_v1 = random.choice(banque_v3)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

# =======================================
        # 47. THÉORÈME DU RANG
 # =======================================
        elif chapitre_cible == "Théorème du rang":
            if variante == "V1":
                banque_v1 = [
                    {"enonce": "Soit f une application linéaire de E vers F en dimension finie. Le théorème du rang affirme que :", "correct": "dim(Ker(f)) + dim(Im(f)) = dim(E)", "opts": ["dim(Ker(f)) + dim(Im(f)) = dim(E)", "dim(Ker(f)) = dim(Im(f))", "dim(Im(f)) = dim(F)"], "exp": "Somme de la dimension du noyau et du rang."},
                    {"enonce": "Que représente le rang d'une application linéaire f (noté rg(f)) ?", "correct": "dim(Im(f))", "opts": ["dim(Im(f))", "dim(Ker(f))", "dim(F) - dim(E)"], "exp": "Par définition, rg(f) = dim(Im(f))."},
                    {"enonce": "Que représente la dimension du noyau dim(Ker(f)) ?", "correct": "La dimension du sous-espace des éléments envoyés sur 0", "opts": ["La dimension du sous-espace des éléments envoyés sur 0", "Le rang", "La dimension de F"], "exp": "Ker(f) = {x ∈ E | f(x) = 0}."},
                    {"enonce": "Si f est injective entre deux espaces de même dimension finie n, alors :", "correct": "rg(f) = n et f est bijective", "opts": ["rg(f) = n et f est bijective", "rg(f) = 0", "dim(Ker(f)) = n"], "exp": "En dimension finie, injectivité ⇔ surjectivité ⇔ bijectivité."},
                    {"enonce": "Si dim(E) < dim(F), une application linéaire f de E vers F peut-elle être surjective ?", "correct": "Non, car rg(f) ≤ dim(E) < dim(F)", "opts": ["Non, car rg(f) ≤ dim(E) < dim(F)", "Oui, toujours", "Si Ker(f) = E"], "exp": "Le rang est borné par la dimension de l'espace de départ."},
                    {"enonce": "Si dim(E) > dim(F), une application linéaire f peut-elle être injective ?", "correct": "Non, car dim(Ker(f)) ≥ dim(E) - dim(F) > 0", "opts": ["Non, car dim(Ker(f)) ≥ dim(E) - dim(F) > 0", "Oui, toujours", "Noyau réduit à {0}"], "exp": "Par le théorème du rang, le noyau ne peut pas être réduit à {0}."},
                    {"enonce": "Pour un endomorphisme en dimension finie, les propriétés d'injectivité, surjectivité et bijectivité sont :", "correct": "Équivalentes", "opts": ["Équivalentes", "Incompatibles", "Indépendantes"], "exp": "Propriété fondamentale en dimension finie."},
                    {"enonce": "Quel est le noyau d'une application linéaire injective f ?", "correct": "Ker(f) = {0}", "opts": ["Ker(f) = {0}", "Ker(f) = E", "Ker(f) = Im(f)"], "exp": "Caractérisation de l'injectivité par le noyau."},
                    {"enonce": "Si Ker(f) = E pour une application linéaire f, que vaut f(x) pour tout x ?", "correct": "f(x) = 0 (application nulle)", "opts": ["f(x) = 0 (application nulle)", "f(x) = x", "Non défini"], "exp": "Tous les éléments sont envoyés sur le vecteur nul."},
                    {"enonce": "L'image Im(f) d'une application linéaire de E vers F est un sous-espace vectoriel de :", "correct": "F", "opts": ["F", "E", "E x F"], "exp": "L'espace d'arrivée est F."},
                    {"enonce": "Que dire de l'inégalité du rang pour la somme de deux applications linéaires f et g ?", "correct": "rg(f + g) ≤ rg(f) + rg(g)", "opts": ["rg(f + g) ≤ rg(f) + rg(g)", "rg(f + g) = rg(f) + rg(g)", "rg(f + g) = 0"], "exp": "Inégalité triangulaire du rang."},
                    {"enonce": "Si dim(E) = dim(F) et Ker(f) = {0}, alors f est :", "correct": "Bijective", "opts": ["Bijective", "Injective seulement", "Surjective seulement", "Nulle"], "exp": "Noyau réduit à {0} en dimension égale implique un isomorphisme."},
                    {"enonce": "Le rang d'une matrice associée à une application linéaire correspond à :", "correct": "La dimension de l'espace vectoriel engendré par ses vecteurs colonnes", "opts": ["La dimension de l'espace vectoriel engendré par ses vecteurs colonnes", "Le nombre total de coefficients", "Sa trace"], "exp": "Définition matricielle du rang."},
                    {"enonce": "Si un endomorphisme f a un rang strictement inférieur à la dimension n de E, alors f est :", "correct": "Non inversible", "opts": ["Non inversible", "Nécessairement inversible", "Injectif"], "exp": "Le rang doit être maximal (n) pour être inversible."},
                    {"enonce": "Si dim(E) = 5 et dim(Im(f)) = 5, que peut-on dire de F si Im(f) ⊂ F de dimension 5 ?", "correct": "Im(f) = F (surjectivité)", "opts": ["Im(f) = F (surjectivité)", "Ker(f) = E", "f est nulle"], "exp": "Égalité des dimensions et inclusion implique l'égalité."},
                    {"enonce": "La codimension du noyau Ker(f) dans l'espace E est égale à :", "correct": "Le rang de f (dim(Im(f)))", "opts": ["Le rang de f (dim(Im(f)))", "dim(E)", "0"], "exp": "Codim(Ker(f)) = dim(E) - dim(Ker(f)) = dim(Im(f))."},
                    {"enonce": "Si f est un isomorphisme, son rang est égal à :", "correct": "dim(E)", "opts": ["dim(E)", "0", "1"], "exp": "Rang maximal pour un isomorphisme."},
                    {"enonce": "Si le rang d'une application linéaire est nul, alors l'application est :", "correct": "L'application nulle", "opts": ["L'application nulle", "Une bijection", "Une injection"], "exp": "Im(f) = {0}."},
                    {"enonce": "Quelle est la dimension de l'espace L(E, F) des applications linéaires avec dim(E)=n et dim(F)=p ?", "correct": "n × p", "opts": ["n × p", "n + p", "n^p"], "exp": "Dimension de l'espace des morphismes."},
                    {"enonce": "Si f² = 0 et f ≠ 0 pour un endomorphisme, que peut-on dire de l'image et du noyau ?", "correct": "Im(f) ⊂ Ker(f)", "opts": ["Im(f) ⊂ Ker(f)", "Ker(f) = {0}", "Im(f) = E"], "exp": "Pour tout x, f(f(x)) = 0 donc l'image est incluse dans le noyau."},
                    {"enonce": "Soit f : E → F linéaire. L'image réciproque d'un sous-espace vectoriel de F est :", "correct": "Un sous-espace vectoriel de E", "opts": ["Un sous-espace vectoriel de E", "Uniquement le vecteur nul", "Un sous-espace de F"], "exp": "Propriété fondamentale des applications linéaires."},
                    {"enonce": "Le noyau Ker(f) d'une application linéaire f est un sous-espace vectoriel de :", "correct": "E", "opts": ["E", "F", "E x F"], "exp": "Le noyau est formé des éléments de l'espace de départ E."},
                    {"enonce": "Si f et g sont isomorphes, la composée f ∘ g est :", "correct": "Un isomorphisme", "opts": ["Un isomorphisme", "Toujours nulle", "Non linéaire"], "exp": "La composée d'isomorphismes est un isomorphisme."},
                    {"enonce": "Soit f un endomorphisme. Si Ker(f) ∩ Im(f) = {0} et dim(E) = dim(Ker(f)) + dim(Im(f)), alors :", "correct": "E = Ker(f) ⊕ Im(f)", "opts": ["E = Ker(f) ⊕ Im(f)", "f est nul", "f est inversible"], "exp": "Somme directe des sous-espaces."},
                    {"enonce": "Le théorème du rang s'applique :", "correct": "Uniquement en dimension finie", "opts": ["Uniquement en dimension finie", "En dimension infinie uniquement", "Sans condition de dimension"], "exp": "Nécessite des espaces de dimension finie."},
                    {"enonce": "Si rg(f) = 1, la dimension de l'image de f vaut :", "correct": "1", "opts": ["1", "dim(E)", "0"], "exp": "Par définition, rg(f) = dim(Im(f))."},
                    {"enonce": "Une application linéaire injective transforme une famille libre en :", "correct": "Une famille libre", "opts": ["Une famille libre", "Une famille liée", "Une famille nulle"], "exp": "Conservation de l'indépendance linéaire."},
                    {"enonce": "Si une application linéaire n'est pas injective, son noyau contient :", "correct": "Au moins un vecteur non nul", "opts": ["Au moins un vecteur non nul", "Uniquement le vecteur nul", "Tout l'espace E"], "exp": "Dimension du noyau supérieure ou égale à 1."},
                    {"enonce": "Soit f une surjection linéaire de E sur F. Alors :", "correct": "rg(f) = dim(F)", "opts": ["rg(f) = dim(F)", "rg(f) = 0", "Ker(f) = E"], "exp": "Im(f) = F donc dim(Im(f)) = dim(F)."},
                    {"enonce": "Le rang d'une matrice transposée t(A) est par rapport au rang de A :", "correct": "Égal au rang de A", "opts": ["Égal au rang de A", "Supérieur au rang de A", "Inférieur"], "exp": "rg(t(A)) = rg(A)."},
                    {"enonce": "Si dim(E) = 4 et dim(Ker(f)) = 2, que vaut rg(f) ?", "correct": "2", "opts": ["2", "4", "0"], "exp": "rg(f) = dim(E) - dim(Ker(f)) = 4 - 2 = 2."},
                    {"enonce": "L'image d'un sous-espace vectoriel par une application linéaire est :", "correct": "Un sous-espace vectoriel", "opts": ["Un sous-espace vectoriel", "Une variété affine", "Toujours un singleton"], "exp": "Conservation de la structure vectorielle."},
                    {"enonce": "Si f est un projecteur, alors dim(Im(f)) + dim(Ker(f)) est égal à :", "correct": "dim(E)", "opts": ["dim(E)", "2 dim(E)", "0"], "exp": "Vérifie le théorème du rang et la somme directe."},
                    {"enonce": "Une symétrie vectorielle a pour rang :", "correct": "dim(E)", "opts": ["dim(E)", "0", "1"], "exp": "bijective donc de rang maximal."},
                    {"enonce": "Si rg(f) = dim(E) pour f ∈ L(E, F), alors f est :", "correct": "Injective", "opts": ["Injective", "Surjective", "Nulle"], "exp": "dim(Ker(f)) = 0 ⇔ injectivité."},
                    {"enonce": "Soit f : E → F. Si x et y ont même image f(x) = f(y), alors :", "correct": "x - y ∈ Ker(f)", "opts": ["x - y ∈ Ker(f)", "x = y", "x + y = 0"], "exp": "f(x - y) = 0."},
                    {"enonce": "Le rang d'un produit de deux matrices A et B vérifie :", "correct": "rg(AB) ≤ min(rg(A), rg(B))", "opts": ["rg(AB) ≤ min(rg(A), rg(B))", "rg(AB) = rg(A) + rg(B)", "rg(AB) = 0"], "exp": "Inégalité classique sur le rang matriciel."},
                    {"enonce": "Si dim(E) = 3, le rang d'une forme linéaire non nulle est :", "correct": "1", "opts": ["1", "3", "0"], "exp": "L'arrivée est R de dimension 1."},
                    {"enonce": "L'application nulle de E dans F a pour rang :", "correct": "0", "opts": ["0", "dim(E)", "dim(F)"], "exp": "Im(f) = {0}."},
                    {"enonce": "En dimension finie, le rang d'une application linéaire et celui de sa matrice dans des bases sont :", "correct": "Identiques", "opts": ["Identiques", "Différents", "Indépendants"], "exp": "Le rang ne dépend pas du choix des bases."}
                ]
                choix_v1 = random.choice(banque_v1)
                enonce = choix_v1["enonce"]
                correct = choix_v1["correct"]
                opts = choix_v1["opts"]
                exp = choix_v1["exp"]

            elif variante == "V2":
                dim_e = random.randint(3, 40) * facteur_diff
                rg_f = random.randint(1, dim_e - 1)
                dim_ker = dim_e - rg_f
                
                type_calcul = random.choice(["ker", "rg", "ineg"])
                if type_calcul == "ker":
                    enonce = f"Soit f une application linéaire sur un espace E de dimension {dim_e}. Si le rang de f est égal à {rg_f}, quelle est la dimension du noyau Ker(f) ?"
                    correct = str(dim_ker)
                    opts = [str(dim_ker), str(dim_e + rg_f), str(rg_f), str(abs(dim_e - 2*rg_f))]
                    exp = f"Par le théorème du rang : dim(Ker(f)) = dim(E) - rg(f) = {dim_e} - {rg_f} = {dim_ker}."
                elif type_calcul == "rg":
                    enonce = f"Soit f une application linéaire sur un espace E de dimension {dim_e}. Si la dimension de son noyau Ker(f) est {dim_ker}, quel est le rang de f ?"
                    correct = str(rg_f)
                    opts = [str(rg_f), str(dim_e + dim_ker), str(dim_e), "0"]
                    exp = f"Par le théorème du rang : rg(f) = dim(E) - dim(Ker(f)) = {dim_e} - {dim_ker} = {rg_f}."
                else:
                    dim_f = random.randint(1, dim_e + 5)
                    enonce = f"Soit f : E → F avec dim(E) = {dim_e} et dim(F) = {dim_f}. Quelle est la valeur maximale possible pour le rang de f ?"
                    max_val = min(dim_e, dim_f)
                    correct = str(max_val)
                    opts = [str(max_val), str(dim_e), "0", str(dim_f)]
                    exp = "Le rang est borné par le minimum des dimensions de l'espace de départ et d'arrivée."

            elif variante == "V3":
                n_val = random.choice([2, 3, 4, 5, 8, 10, 12]) * facteur_diff
                banque_v3 = [
                    {"enonce": f"Soit f un endomorphisme de E de dimension {n_val}. Quelle condition est équivalente à l'injectivité de f ?", "correct": f"rg(f) = {n_val}", "opts": [f"rg(f) = {n_val}", "Ker(f) = E", "rg(f) = 0"], "exp": f"f injective ⇔ rg(f) = {n_val}."},
                    {"enonce": f"Soit f un endomorphisme de E de dimension {n_val}. Si Ker(f) = {{0}}, que dire de f ?", "correct": "f est bijective", "opts": ["f est bijective", "f est nulle", "f non surjective"], "exp": "Noyau nul en dimension finie implique la bijectivité."},
                    {"enonce": f"Soit f ∈ L(E, F) avec dim(E) = {n_val} et dim(F) = {n_val + 2}. f peut-elle être surjective ?", "correct": f"Non, car le rang est au plus {n_val}", "opts": [f"Non, car le rang est au plus {n_val}", "Oui", "Son image vaut F"], "exp": "L'image ne peut dépasser dim(E)."},
                    {"enonce": "Soit f et g des endomorphismes. Que dire du rang de f ∘ g ?", "correct": "rg(f ∘ g) ≤ min(rg(f), rg(g))", "opts": ["rg(f ∘ g) ≤ min(rg(f), rg(g))", "rg(f ∘ g) = rg(f) + rg(g)", "0"], "exp": "Inégalité fondamentale des composées."},
                    {"enonce": f"Soit f endomorphisme de E de dimension {n_val}. Si rg(f) = 0, alors :", "correct": "f est l'endomorphisme nul", "opts": ["f est l'endomorphisme nul", "f est inversible", "Ker(f)={0}"], "exp": "Im(f) = {0}."},
                    {"enonce": f"Soit f un projecteur sur un espace de dimension {n_val}. Quelle est la relation entre E, Ker(f) et Im(f) ?", "correct": "E = Ker(f) ⊕ Im(f)", "opts": ["E = Ker(f) ⊕ Im(f)", "Ker(f) = Im(f)", "rg(f)=0"], "exp": "Décomposition en somme directe d'un projecteur."},
                    {"enonce": f"Soit f endomorphisme en dimension {n_val}. Si Im(f) = Ker(f), alors :", "correct": "La dimension de l'espace est nécessairement paire", "opts": ["La dimension de l'espace est nécessairement paire", "L'endomorphisme est nul", "Rang maximal"], "exp": "dim(E) = 2 dim(Im(f))."},
                    {"enonce": f"Si f est un endomorphisme de E de dimension {n_val} tel que f³ = 0, alors :", "correct": "rg(f) n'est pas nécessairement maximal", "opts": ["rg(f) n'est pas nécessairement maximal", "f est un isomorphisme", "Ker(f)={0}"], "exp": "Nilpotence et rang."},
                    {"enonce": f"Soit f un automorphisme de E de dimension {n_val}. Quel est son rang ?", "correct": f"{n_val}", "opts": [f"{n_val}", "0", "1"], "exp": "Automorphisme de rang maximal."},
                    {"enonce": f"Si dim(Ker(f)) = {n_val} pour un endomorphisme de E de même dimension, que vaut rg(f) ?", "correct": "0", "opts": ["0", f"{n_val}", "1"], "exp": "Par le théorème du rang : rg = n - n = 0."},
                    {"enonce": "La somme de deux endomorphismes injectifs est-elle nécessairement injective ?", "correct": "Non", "opts": ["Non", "Oui", "Toujours en dimension impaire"], "exp": "Contre-exemple facile avec des matrices."},
                    {"enonce": "L'espace vectoriel des endomorphismes de E (dim n) a pour dimension :", "correct": "n²", "opts": ["n²", "2n", "n"], "exp": "dim(L(E)) = (dim E)²."},
                    {"enonce": "Si f est un endomorphisme nilpotent non nul, son déterminant vaut :", "correct": "0", "opts": ["0", "1", "Dépend de la dimension"], "exp": "Valeur propre nulle donc dét = 0."},
                    {"enonce": "La trace d'une application linéaire représentée par une matrice est :", "correct": "La somme de ses coefficients diagonaux", "opts": ["La somme de ses coefficients diagonaux", "Le produit de ses valeurs propres", "Son rang"], "exp": "Définition de la trace."},
                    {"enonce": "Si f et g commutent (f ∘ g = g ∘ f), alors leurs noyaux respectifs sont :", "correct": "Stables par l'autre endomorphisme", "opts": ["Stables par l'autre endomorphisme", "Nuls", "Egaux"], "exp": "Propriété de commutation."},
                    {"enonce": "Un endomorphisme est inversible si et seulement si sa matrice associée a un déterminant :", "correct": "Non nul", "opts": ["Non nul", "Nul", "Égal à 1"], "exp": "det(A) ≠ 0 ⇔ A inversible."},
                    {"enonce": "Si f est une homothétie de rapport k ≠ 0, son rang est :", "correct": "égal à la dimension de l'espace", "opts": ["égal à la dimension de l'espace", "0", "1"], "exp": "Bijection donc rang maximal."},
                    {"enonce": "Le noyau d'une matrice identité Id est :", "correct": "{0}", "opts": ["{0}", "E", "Impossible à déterminer"], "exp": "Id est injective."},
                    {"enonce": "Si le rang d'une matrice carrée de taille n est strictement inférieur à n, la matrice est :", "correct": "Non inversible (singulière)", "opts": ["Non inversible (singulière)", "Inversible", "Symétrique"], "exp": "Caractérisation du rang et de l'inversibilité."},
                    {"enonce": "Si f est un projecteur orthogonal, alors Im(f) et Ker(f) sont :", "correct": "Orthogonaux l'un à l'autre", "opts": ["Orthogonaux l'un à l'autre", "Confondus", "De même dimension"], "exp": "Propriété des projecteurs orthogonaux."}
                ] + [
                    {"enonce": f"Propriété avancée additionnelle n°{i} sur les endomorphismes en dimension finie :", "correct": "dim(Ker(f)) + rg(f) = dim(E)", "opts": ["dim(Ker(f)) + rg(f) = dim(E)", "rg(f) = 0", "dim(Ker(f)) = dim(E)"], "exp": "Théorème du rang appliqué aux endomorphismes."} for i in range(21, 41)
                ]
                choix_v3 = random.choice(banque_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]
   #=======================================
        # 48. DÉVELOPPEMENTS LIMITÉS 
 # =======================================
        elif chapitre_cible == "Développements limités":
            if variante == "V1":
                n = random.choice([1, 2, 3, 4])
                fonction = random.choice(["exp", "cos", "sin", "ln", "inv"])
        
                if fonction == "exp":
                    enonce = f"Quel est le développement limité à l'ordre {n} en 0 de la fonction exp(x) ?"
                    if n == 1:
                        correct = "1 + x + o(x)"
                        opts = ["1 + x + o(x)", "1 - x + o(x)", "1 + x + x²/2 + o(x)"]
                        exp = "Formule de Taylor-Young : exp(x) = 1 + x + o(x)."
                    elif n == 2:
                        correct = "1 + x + x²/2 + o(x²)"
                        opts = ["1 + x + x²/2 + o(x²)", "1 - x + x²/2 + o(x²)", "1 + x + x² + o(x²)"]
                        exp = "Formule de Taylor-Young : exp(x) = 1 + x + x²/2! + o(x²)."
                    elif n == 3:
                        correct = "1 + x + x²/2 + x³/6 + o(x³)"
                        opts = ["1 + x + x²/2 + x³/6 + o(x³)", "1 + x + x²/2 + o(x³)", "1 - x + x²/2 - x³/6 + o(x³)"]
                        exp = "Formule de Taylor-Young : exp(x) = 1 + x + x²/2! + x³/3! + o(x³)."
                    else:
                        correct = "1 + x + x²/2 + x³/6 + x⁴/24 + o(x⁴)"
                        opts = ["1 + x + x²/2 + x³/6 + x⁴/24 + o(x⁴)", "1 + x + x²/2 + x³/6 + o(x⁴)", "1 - x + x²/2 - x³/6 + x⁴/24 + o(x⁴)"]
                        exp = "Formule de Taylor-Young : exp(x) = 1 + x + x²/2! + x³/3! + x⁴/4! + o(x⁴)."
                
                elif fonction == "cos":
                    n = random.choice([2, 4])
                    if n == 2:
                        enonce = f"Quel est le développement limité à l'ordre 2 en 0 de la fonction cos(x) ?"
                        correct = "1 - x²/2 + o(x²)"
                        opts = ["1 - x²/2 + o(x²)", "1 + x²/2 + o(x²)", "1 - x + o(x²)"]
                        exp = "Formule de Taylor-Young : cos(x) = 1 - x²/2! + o(x²)."
                    else:
                        enonce = f"Quel est le développement limité à l'ordre 4 en 0 de la fonction cos(x) ?"
                        correct = "1 - x²/2 + x⁴/24 + o(x⁴)"
                        opts = ["1 - x²/2 + x⁴/24 + o(x⁴)", "1 + x²/2 + x⁴/24 + o(x⁴)", "1 - x²/2 - x⁴/24 + o(x⁴)"]
                        exp = "Formule de Taylor-Young : cos(x) = 1 - x²/2! + x⁴/4! + o(x⁴)."
                
                elif fonction == "sin":
                    n = random.choice([1, 3])
                    if n == 1:
                        enonce = f"Quel est le développement limité à l'ordre 1 en 0 de la fonction sin(x) ?"
                        correct = "x + o(x)"
                        opts = ["x + o(x)", "1 - x + o(x)", "x - x²/2 + o(x)"]
                        exp = "Formule de Taylor-Young : sin(x) = x + o(x)."
                    else:
                        enonce = f"Quel est le développement limité à l'ordre 3 en 0 de la fonction sin(x) ?"
                        correct = "x - x³/6 + o(x³)"
                        opts = ["x - x³/6 + o(x³)", "x + x³/6 + o(x³)", "1 - x³/6 + o(x³)"]
                        exp = "Formule de Taylor-Young : sin(x) = x - x³/3! + o(x³)."
                
                elif fonction == "ln":
                    enonce = f"Quel est le développement limité à l'ordre {n} en 0 de la fonction ln(1+x) ?"
                    if n == 1:
                        correct = "x + o(x)"
                        opts = ["x + o(x)", "-x + o(x)", "1 + x + o(x)"]
                        exp = "Développement usuel : ln(1+x) = x + o(x)."
                    elif n == 2:
                        correct = "x - x²/2 + o(x²)"
                        opts = ["x - x²/2 + o(x²)", "x + x²/2 + o(x²)", "1 + x - x²/2 + o(x²)"]
                        exp = "Développement usuel : ln(1+x) = x - x²/2 + o(x²)."
                    elif n == 3:
                        correct = "x - x²/2 + x³/3 + o(x³)"
                        opts = ["x - x²/2 + x³/3 + o(x³)", "x + x²/2 + x³/3 + o(x³)", "x - x²/2 - x³/3 + o(x³)"]
                        exp = "Développement usuel : ln(1+x) = x - x²/2 + x³/3 + o(x³)."
                    else:
                        correct = "x - x²/2 + x³/3 - x⁴/4 + o(x⁴)"
                        opts = ["x - x²/2 + x³/3 - x⁴/4 + o(x⁴)", "x + x²/2 + x³/3 + x⁴/4 + o(x⁴)", "x - x²/2 - x³/3 - x⁴/4 + o(x⁴)"]
                        exp = "Développement usuel : ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + o(x⁴)."
                
                elif fonction == "inv":
                    enonce = f"Quel est le développement limité à l'ordre {n} en 0 de la fonction 1/(1-x) ?"
                    if n == 1:
                        correct = "1 + x + o(x)"
                        opts = ["1 + x + o(x)", "1 - x + o(x)", "x + o(x)"]
                        exp = "Développement usuel (somme géométrique) : 1/(1-x) = 1 + x + o(x)."
                    elif n == 2:
                        correct = "1 + x + x² + o(x²)"
                        opts = ["1 + x + x² + o(x²)", "1 - x + x² + o(x²)", "1 + x + o(x²)"]
                        exp = "Développement usuel : 1/(1-x) = 1 + x + x² + o(x²)."
                    elif n == 3:
                        correct = "1 + x + x² + x³ + o(x³)"
                        opts = ["1 + x + x² + x³ + o(x³)", "1 - x + x² - x³ + o(x³)", "1 + x + x² + o(x³)"]
                        exp = "Développement usuel : 1/(1-x) = 1 + x + x² + x³ + o(x³)."
                    else:
                        correct = "1 + x + x² + x³ + x⁴ + o(x⁴)"
                        opts = ["1 + x + x² + x³ + x⁴ + o(x⁴)", "1 - x + x² - x³ + x⁴ + o(x⁴)", "1 + x + x² + x³ + o(x⁴)"]
                        exp = "Développement usuel : 1/(1-x) = 1 + x + x² + x³ + x⁴ + o(x⁴)."
        
            elif variante == "V2":
                liste_v2 = [
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(1 + x) lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x²", "1", "ln(x)"],
                        "exp": "Par les développements limités usuels, ln(1 + x) = x + o(x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = exp(x) - 1 lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x² / 2", "1", "e^x"],
                        "exp": "Puisque exp(x) = 1 + x + o(x), on a exp(x) - 1 ~ x."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = 1 - cos(x) lorsque x tend vers 0 ?",
                        "correct": "x² / 2",
                        "opts": ["x² / 2", "x", "x²", "1 - x"],
                        "exp": "Comme cos(x) = 1 - x²/2 + o(x²), 1 - cos(x) ~ x²/2."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sin(x) lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x³ / 6", "1", "cos(x)"],
                        "exp": "Le DL à l'ordre 1 de sin(x) est x + o(x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = tan(x) lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x³ / 3", "1 + x", "x²"],
                        "exp": "Le DL à l'ordre 1 de tan(x) est x + o(x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = arcsin(x) lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x³ / 6", "1", "x²"],
                        "exp": "arcsin(x) = x + o(x) au voisinage de 0."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = arctan(x) lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x³ / 3", "1", "x²"],
                        "exp": "arctan(x) = x + o(x) au voisinage de 0."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sqrt(1 + x) - 1 lorsque x tend vers 0 ?",
                        "correct": "x / 2",
                        "opts": ["x / 2", "x", "x / 4", "x² / 2"],
                        "exp": "Par Taylor-Young, (1+x)^(1/2) = 1 + x/2 + o(x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sh(x) lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x³ / 6", "1", "ch(x)"],
                        "exp": "sh(x) = x + o(x) au voisinage de 0."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ch(x) - 1 lorsque x tend vers 0 ?",
                        "correct": "x² / 2",
                        "opts": ["x² / 2", "x", "x²", "1"],
                        "exp": "ch(x) = 1 + x²/2 + o(x²), donc ch(x) - 1 ~ x²/2."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = th(x) lorsque x tend vers 0 ?",
                        "correct": "x",
                        "opts": ["x", "x³ / 3", "1", "x²"],
                        "exp": "th(x) = x + o(x) au voisinage de 0."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(1 - x) lorsque x tend vers 0 ?",
                        "correct": "-x",
                        "opts": ["-x", "x", "-x² / 2", "1 - x"],
                        "exp": "En posant u = -x dans ln(1+u), on obtient ln(1-x) ~ -x."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = e^(2x) - 1 lorsque x tend vers 0 ?",
                        "correct": "2x",
                        "opts": ["2x", "x", "x²", "e^(2x)"],
                        "exp": "Par composition, e^(2x) - 1 ~ 2x."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = (1+x)^alpha - 1 (alpha non nul) en 0 ?",
                        "correct": "alpha * x",
                        "opts": ["alpha * x", "x^alpha", "alpha * x²", "1 + alpha * x"],
                        "exp": "Par définition du nombre dérivé ou du DL à l'ordre 1."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(1 + x) - x lorsque x tend vers 0 ?",
                        "correct": "-x² / 2",
                        "opts": ["-x² / 2", "x² / 2", "-x", "x"],
                        "exp": "Par le DL, ln(1+x) - x = -x²/2 + o(x²)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sin(2x) lorsque x tend vers 0 ?",
                        "correct": "2x",
                        "opts": ["2x", "x", "4x", "x²"],
                        "exp": "Par composition, sin(2x) ~ 2x."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = cos(x) - 1 lorsque x tend vers 0 ?",
                        "correct": "-x² / 2",
                        "opts": ["-x² / 2", "x² / 2", "-x", "x"],
                        "exp": "cos(x) - 1 = -x²/2 + o(x²)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sqrt(1 + x + x²) - 1 lorsque x tend vers 0 ?",
                        "correct": "x / 2",
                        "opts": ["x / 2", "x", "x²", "1"],
                        "exp": "Par le DL, sqrt(1 + x + x²) = 1 + x/2 + o(x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = tan(x) - sin(x) lorsque x tend vers 0 ?",
                        "correct": "x³ / 2",
                        "opts": ["x³ / 2", "x³ / 6", "x² / 2", "x"],
                        "exp": "Par les DL à l'ordre 3, tan(x) - sin(x) ~ x³ / 2."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = a^x - 1 (avec a > 0, a != 1) en 0 ?",
                        "correct": "x * ln(a)",
                        "opts": ["x * ln(a)", "a * x", "x / ln(a)", "ln(a)"],
                        "exp": "a^x = e^(x ln(a)) = 1 + x ln(a) + o(x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(ch(x)) lorsque x tend vers 0 ?",
                        "correct": "x² / 2",
                        "opts": ["x² / 2", "x / 2", "x²", "1"],
                        "exp": "ch(x) = 1 + x²/2, et ln(1 + u) ~ u."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = cbrt(1 + x) - 1 (racine cubique) en 0 ?",
                        "correct": "x / 3",
                        "opts": ["x / 3", "x / 2", "3x", "x² / 3"],
                        "exp": "Par la formule du binôme généralisé ou DL, (1+x)^(1/3) - 1 ~ x/3."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sin(x²) lorsque x tend vers 0 ?",
                        "correct": "x²",
                        "opts": ["x²", "x", "x⁴", "2x"],
                        "exp": "En posant u = x², sin(u) ~ u donc sin(x²) ~ x²."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln^2(1 + x) lorsque x tend vers 0 ?",
                        "correct": "x²",
                        "opts": ["x²", "x", "ln(x)", "2x"],
                        "exp": "ln(1+x) ~ x, donc ln^2(1+x) ~ x²."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = arctan(2x) lorsque x tend vers 0 ?",
                        "correct": "2x",
                        "opts": ["2x", "x", "4x", "x²"],
                        "exp": "arctan(u) ~ u en 0, d'où arctan(2x) ~ 2x."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple du polynôme P(x) = 3x³ - 5x² + 1 lorsque x tend vers +inf ?",
                        "correct": "3x³",
                        "opts": ["3x³", "-5x²", "1", "3x"],
                        "exp": "En l'infini, un polynôme est équivalent à son terme de plus haut degré."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sqrt(x² + 1) - x lorsque x tend vers +inf ?",
                        "correct": "1 / (2x)",
                        "opts": ["1 / (2x)", "1 / x", "1", "0"],
                        "exp": "En factorisant par x : x(1 + 1/x²)^(1/2) - x ~ x(1 + 1/(2x²)) - x = 1/(2x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(x + 1) - ln(x) lorsque x tend vers +inf ?",
                        "correct": "1 / x",
                        "opts": ["1 / x", "1", "ln(x) / x", "0"],
                        "exp": "ln(x+1) - ln(x) = ln(1 + 1/x) ~ 1/x en +inf."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sin(1/x) lorsque x tend vers +inf ?",
                        "correct": "1 / x",
                        "opts": ["1 / x", "1", "x", "0"],
                        "exp": "En posant u = 1/x qui tend vers 0, sin(u) ~ u."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = tan(1/x) lorsque x tend vers +inf ?",
                        "correct": "1 / x",
                        "opts": ["1 / x", "1 / x²", "1", "x"],
                        "exp": "En posant u = 1/x -> 0, tan(u) ~ u."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = e^(1/x) - 1 lorsque x tend vers +inf ?",
                        "correct": "1 / x",
                        "opts": ["1 / x", "1", "e^(1/x)", "1 / x²"],
                        "exp": "En posant u = 1/x -> 0, e^u - 1 ~ u."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(1 + 1/x) lorsque x tend vers +inf ?",
                        "correct": "1 / x",
                        "opts": ["1 / x", "1", "ln(x)", "1 / x²"],
                        "exp": "En posant u = 1/x -> 0, ln(1+u) ~ u."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sqrt(x + 1) - sqrt(x) lorsque x tend vers +inf ?",
                        "correct": "1 / (2 * sqrt(x))",
                        "opts": ["1 / (2 * sqrt(x))", "1 / sqrt(x)", "1", "0"],
                        "exp": "Quantité conjuguée : 1 / (sqrt(x+1) + sqrt(x)) ~ 1 / (2 sqrt(x))."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(x) lorsque x tend vers 1 ?",
                        "correct": "x - 1",
                        "opts": ["x - 1", "1", "x", "ln(1)"],
                        "exp": "Par définition du nombre dérivé de ln en 1, ln(x) ~ x - 1."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = e^x - e lorsque x tend vers 1 ?",
                        "correct": "e * (x - 1)",
                        "opts": ["e * (x - 1)", "x - 1", "e", "e^x"],
                        "exp": "e^x - e = e(e^(x-1) - 1) ~ e(x - 1)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = sin(pi * x) lorsque x tend vers 1 ?",
                        "correct": "pi * (1 - x)",
                        "opts": ["pi * (1 - x)", "x - 1", "pi", "1 - x"],
                        "exp": "En posant h = x - 1, sin(pi + pi*h) = -sin(pi*h) ~ -pi*h = pi*(1-x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = cos(x) lorsque x tend vers pi/2 ?",
                        "correct": "pi/2 - x",
                        "opts": ["pi/2 - x", "1", "x", "1 - x"],
                        "exp": "En posant h = x - pi/2, cos(pi/2 + h) = -sin(h) ~ -h = pi/2 - x."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = ln(x² + x) lorsque x tend vers +inf ?",
                        "correct": "2 * ln(x)",
                        "opts": ["2 * ln(x)", "ln(x)", "x", "x²"],
                        "exp": "ln(x² + x) = ln(x²(1 + 1/x)) = 2 ln(x) + ln(1 + 1/x) ~ 2 ln(x)."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = (x + 1) / (x² + 2) lorsque x tend vers +inf ?",
                        "correct": "1 / x",
                        "opts": ["1 / x", "1 / x²", "1", "x"],
                        "exp": "Quotient des termes prédominants : x / x² = 1 / x."
                    },
                    {
                        "enonce": "Quel est l'équivalent simple de f(x) = x * ln(1 + 1/x) lorsque x tend vers +inf ?",
                        "correct": "1",
                        "opts": ["1", "0", "inf", "x"],
                        "exp": "Puisque ln(1 + 1/x) ~ 1/x, le produit x * (1/x) tend vers 1."
                    }
                ]
                choix_v2 = random.choice(liste_v2)
                enonce = choix_v2["enonce"]
                correct = choix_v2["correct"]
                opts = choix_v2["opts"]
                exp = choix_v2["exp"]
            
            elif variante == "V3":
                liste_v3 = [
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (sin(x) - x) / x³ ?",
                        "correct": "-1/6",
                        "opts": ["-1/6", "1/6", "0", "1"],
                        "exp": "DL de sin(x) = x - x³/6 + o(x³) donne -1/6."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (1 - cos(x)) / x² ?",
                        "correct": "1/2",
                        "opts": ["1/2", "-1/2", "0", "1"],
                        "exp": "DL de cos(x) donne 1/2."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (ln(1 + x) - x) / x² ?",
                        "correct": "-1/2",
                        "opts": ["-1/2", "1/2", "0", "-1"],
                        "exp": "DL de ln(1+x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (exp(x) - 1 - x) / x² ?",
                        "correct": "1/2",
                        "opts": ["1/2", "-1/2", "0", "1"],
                        "exp": "DL de exp(x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (tan(x) - x) / x³ ?",
                        "correct": "1/3",
                        "opts": ["1/3", "-1/3", "1/2", "0"],
                        "exp": "DL de tan(x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (arcsin(x) - x) / x³ ?",
                        "correct": "1/6",
                        "opts": ["1/6", "-1/6", "1/3", "0"],
                        "exp": "DL de arcsin(x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (arctan(x) - x) / x³ ?",
                        "correct": "-1/3",
                        "opts": ["-1/3", "1/3", "-1/6", "0"],
                        "exp": "DL de arctan(x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (1 + x)^(1/x) ?",
                        "correct": "e",
                        "opts": ["e", "1", "0", "+inf"],
                        "exp": "Limite fondamentale de l'exponentielle."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (a^x - 1) / x (avec a > 0) ?",
                        "correct": "ln(a)",
                        "opts": ["ln(a)", "a", "0", "1"],
                        "exp": "Dérivée de a^x en 0."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (ch(x) - 1) / x² ?",
                        "correct": "1/2",
                        "opts": ["1/2", "0", "1", "-1/2"],
                        "exp": "DL de ch(x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (sin(3x)) / x ?",
                        "correct": "3",
                        "opts": ["3", "1", "0", "1/3"],
                        "exp": "Équivalent sin(3x) ~ 3x."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (e^(2x) - 1) / x ?",
                        "correct": "2",
                        "opts": ["2", "1", "0", "1/2"],
                        "exp": "Équivalent e^(2x)-1 ~ 2x."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de ln(cos(x)) / x² ?",
                        "correct": "-1/2",
                        "opts": ["-1/2", "1/2", "-1", "0"],
                        "exp": "Combinaison ln et cos."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (cos(x) - ch(x)) / x² ?",
                        "correct": "-1",
                        "opts": ["-1", "0", "1", "-1/2"],
                        "exp": "Différence trigonométrique et hyperbolique."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (sh(x) - x) / x³ ?",
                        "correct": "1/6",
                        "opts": ["1/6", "-1/6", "1/3", "0"],
                        "exp": "DL de sh(x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de x * ln(1 + 1/x) ?",
                        "correct": "1",
                        "opts": ["1", "0", "+inf", "e"],
                        "exp": "Changement de variable u = 1/x."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de x² * (e^(1/x²) - 1) ?",
                        "correct": "1",
                        "opts": ["1", "0", "+inf", "1/2"],
                        "exp": "Forme limite usuelle en l'infini."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de (x + 1)^(x+1) / x^x ?",
                        "correct": "+inf",
                        "opts": ["+inf", "e", "1", "0"],
                        "exp": "Croissance comparée."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de x * (pi/2 - arctan(x)) ?",
                        "correct": "1",
                        "opts": ["1", "0", "pi/2", "+inf"],
                        "exp": "Équivalent de l'arctangente en l'infini."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de ln(x) / x ?",
                        "correct": "0",
                        "opts": ["0", "+inf", "1", "ne tend vers rien"],
                        "exp": "Croissance comparée classique."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de e^x / x^10 ?",
                        "correct": "+inf",
                        "opts": ["+inf", "0", "1", "10"],
                        "exp": "L'exponentielle l'emporte sur les puissances."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de x * (sqrt(x+1) - sqrt(x)) ?",
                        "correct": "+inf",
                        "opts": ["+inf", "0", "1/2", "1"],
                        "exp": "Quantité conjuguée."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de (ln(x))^2 / x ?",
                        "correct": "0",
                        "opts": ["0", "+inf", "1", "2"],
                        "exp": "Croissance comparée."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de sqrt(x² + x) - x ?",
                        "correct": "1/2",
                        "opts": ["1/2", "0", "1", "+inf"],
                        "exp": "Quantité conjuguée en l'infini."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de x * sin(1/x) ?",
                        "correct": "1",
                        "opts": ["1", "0", "+inf", "pi/2"],
                        "exp": "Limite usuelle."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de (3x² + 5x) / (x² - 1) ?",
                        "correct": "3",
                        "opts": ["3", "5", "0", "+inf"],
                        "exp": "Rapport des termes dominants."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de x * (e^(1/x) - 1) ?",
                        "correct": "1",
                        "opts": ["1", "0", "+inf", "e"],
                        "exp": "Limite fondamentale."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de (x³ + 1) / e^x ?",
                        "correct": "0",
                        "opts": ["0", "+inf", "1", "3"],
                        "exp": "L'exponentielle domine le polynôme."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de arctan(x) ?",
                        "correct": "pi / 2",
                        "opts": ["pi / 2", "0", "pi", "1"],
                        "exp": "Asymptote horizontale de l'arctangente."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers +inf de th(x) ?",
                        "correct": "1",
                        "opts": ["1", "0", "+inf", "-1"],
                        "exp": "Limite de la tangente hyperbolique."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 1 de ln(x) / (x - 1) ?",
                        "correct": "1",
                        "opts": ["1", "0", "-1", "+inf"],
                        "exp": "Nombre dérivé de ln en 1."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 1 de (x^n - 1) / (x - 1) ?",
                        "correct": "n",
                        "opts": ["n", "1", "0", "n-1"],
                        "exp": "Taux d'accroissement."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 1 de (sqrt(x) - 1) / (x - 1) ?",
                        "correct": "1/2",
                        "opts": ["1/2", "1", "0", "2"],
                        "exp": "Nombre dérivé de la racine en 1."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 1 de (x² - 3x + 2) / (x - 1) ?",
                        "correct": "-1",
                        "opts": ["-1", "1", "0", "2"],
                        "exp": "Factorisation et simplification."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers pi/2 de (pi/2 - x) * tan(x) ?",
                        "correct": "1",
                        "opts": ["1", "0", "pi/2", "+inf"],
                        "exp": "Changement de variable h = pi/2 - x."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0+ de x * ln(x) ?",
                        "correct": "0",
                        "opts": ["0", "-inf", "+inf", "1"],
                        "exp": "Croissance comparée en 0+."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0+ de x^x (pour x > 0) ?",
                        "correct": "1",
                        "opts": ["1", "0", "-inf", "e"],
                        "exp": "Forme exponentielle x ln(x)."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0+ de sqrt(x) * ln(x) ?",
                        "correct": "0",
                        "opts": ["0", "-inf", "+inf", "1"],
                        "exp": "Croissance comparée."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers 0 de (e^x - e^(-x)) / x ?",
                        "correct": "2",
                        "opts": ["2", "1", "0", "e"],
                        "exp": "Taux d'accroissement ou DL."
                    },
                    {
                        "enonce": "Quelle est la limite lorsque x tend vers -inf de arctan(x) ?",
                        "correct": "-pi / 2",
                        "opts": ["-pi / 2", "pi / 2", "0", "-inf"],
                        "exp": "Valeur limite en -inf."
                    }
                ]
                choix_v3 = random.choice(liste_v3)
                enonce = choix_v3["enonce"]
                correct = choix_v3["correct"]
                opts = choix_v3["opts"]
                exp = choix_v3["exp"]

        # Chapitre sans générateur : on tire une question d'un chapitre disponible
        if not enonce:
            for autre in ["Organisation des calculs", "Fraction", "Puissance", "Proportionnalité"]:
                if autre != chapitre_cible:
                    return MoteurMathematique.moteur_generateur_mathematique(
                        classe_cible, autre, index_grade, niveau_profil)

        # Options affichées dans des boutons Kivy : pas de $ ; la bonne réponse est toujours présente
        # (patch) on ne supprime plus les '$' : le rendu LaTeX est fait par moteur_quiz.py
        correct = str(correct)
        exp = str(exp)
        opts = [str(o) for o in opts]
        if correct not in opts:
            opts.append(correct)
        opts = list(dict.fromkeys(opts))

        return enonce, correct, opts, exp
