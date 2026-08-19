import random
import math

class MoteurMathematique:
    @staticmethod
    def moteur_generateur_mathematique(classe_cible, chapitre_cible, index_grade, niveau_profil):
        enonce, correct, opts, exp = "", "", [], ""
        variante = random.choice(["V1", "V2", "V3"])
        
        facteur_diff = 1 + (index_grade // 5) + (niveau_profil // 3)
        
        if chapitre_cible in ["Arithmétiques"]:
            if variante == "V1":
                div = random.choice([2, 4, 8, 1, 7, 6, 3, 5, 9])
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
            elif variante == "V3":
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
                enonce = f"Combien de points d'intersection possèdent deux droites de l'espace plane qui sont strictement parallèles ?"
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
            elif variante == "V3":
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
            elif variante =="V3":
                enonce = "Sur une carte de géographie construite à l'échelle linéaire 1/100, une longueur mesurée de 1 cm correspond sur le terrain à :"
                correct = "100 cm (1 m)"
                opts = ["100 cm (1 m)", "10 cm", "1000 cm"]
                exp = "E = d / D ⇒ D = 100 cm"

        elif chapitre_cible == "Puissance":
            b = random.randint(2, 99)
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
            if variante == "V1":
                enonce = "Lors d'une projection affine ou orthogonale sur une droite du plan, quelle propriété est invariante ?"
                correct = "L'alignement des points"
                opts = ["L'alignement des points", "La longueur des segments", "La mesure des angles"]
                exp = "Conservation des applications affines"
            elif variante =="V2":
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
            if variante == "V1":
                enonce = "Si deux droites représentant un système d'équations linéaires dans IR² possèdent des coefficients directeurs distincts, le système admet :"
                correct = "Une solution unique"
                opts = ["Une solution unique", "Aucune solution", "Une infinité de solutions"]
                exp = "m1 ≠ m2 ⇒ Unique point d'intersection D1 ∩ D2"
            elif variante =="V2":
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
            enonce = "Selon la seconde loi de Snell-Descartes pour la réfraction, la relation liant les angles d'incidence (i1) et de réfraction (i2) est :"
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
