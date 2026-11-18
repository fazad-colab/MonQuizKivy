# -*- coding: utf-8 -*-
"""
modules_defis.py — modules « Niveaux d'Activités » (16) et « Sujets Casse-Tête » (3)
=====================================================================================
Chaque générateur renvoie une question au MÊME format que moteur_quiz.generer_question :

    {"enonce": "texte avec $maths$", "options": ["$...$", ...], "index_correct": 2,
     "bonne_reponse": "$...$", "explication": "...", "enonce_txt", "options_txt", "explication_txt",
     "chapitre": "...", "classe": "..."}

Tout est écrit en LaTeX : l'affichage passe donc par la page KaTeX (rendu mathématique).

    q = generer_activite("Équations du 1er Degré", difficulte=2)
    q = generer_casse_tete("Paradoxes")
"""
import math
import random
from fractions import Fraction

from latex_utils import latex_vers_texte

LISTE_ACTIVITES = [
    "Calcul Mental Éclair", "Arithmétique de Base", "Fractions & Proportions",
    "Équations du 1er Degré", "Puissances & Racines", "Identités Remarquables",
    "Systèmes Linéaires", "Dérivation & Limites", "Nombres Complexes",
    "Calcul Intégral", "Mécanique du Point", "Thermodynamique Appliquée",
    "Optique Géométrique", "Électrostatique Avancée", "Théorèmes Vectoriels Complexes",
    "Physique Quantique 101",
]
TYPES_CASSE_TETE = {"Paradoxes": "Paradoxes Mathématiques",
                    "Énigmes": "Énigmes Algébriques",
                    "Géométrie": "Défis Géométriques Poussés"}


# ----------------------------------------------------------------------------
# Outils de mise en forme
# ----------------------------------------------------------------------------
def _n(x, nd=2):
    """Nombre -> LaTeX (virgule décimale française, fraction si Fraction)."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return ("-" if x < 0 else "") + r"\dfrac{%d}{%d}" % (abs(x.numerator), x.denominator)
    if isinstance(x, int):
        return str(x)
    if float(x).is_integer():
        return str(int(x))
    return ("%.*f" % (nd, x)).rstrip("0").rstrip(".").replace(".", "{,}")


def _mil(n):
    """84000 -> 84\\,000"""
    s = "{:,}".format(int(n)).replace(",", r"\,")
    return s


def _sci(x):
    """0.0135 -> 1{,}35\\times10^{-2}"""
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = x / (10 ** e)
    return r"%s\times10^{%d}" % (_n(round(m, 2)), e)


def _sg(n, premier=False):
    """Entier relatif -> ' + 3' / ' - 3' (ou '3' / '-3' en tête d'expression)."""
    if premier:
        return str(n)
    return (" + %d" % n) if n >= 0 else (" - %d" % abs(n))


def _coef(a, var, premier=False):
    """Terme a·var avec signe correct : _coef(-1,'x') -> ' - x'."""
    if a == 0:
        return ""
    corps = var if abs(a) == 1 else "%d%s" % (abs(a), var)
    if premier:
        return ("-" if a < 0 else "") + corps
    return (" - " if a < 0 else " + ") + corps


def _lin2(a, b, v1="x", v2="y"):
    s = _coef(a, v1, True) + _coef(b, v2, a == 0)
    return s or "0"


def _faux_num(v, k=3, entier=True):
    """Valeurs plausibles ≠ v (formatées par _n)."""
    cands = [v + 1, v - 1, v + 2, v - 2, v * 2, v + 10, v - 10, -v, v + 5, v - 5]
    if not (isinstance(v, Fraction) or not entier):
        cands += [v * 3, v + 3, v - 3]
    random.shuffle(cands)
    sortie = []
    for c in cands:
        if c != v and _n(c) != _n(v) and _n(c) not in sortie:
            sortie.append(_n(c))
        if len(sortie) >= k:
            break
    return sortie


def _construire(enonce, bonne, faux, explication, chapitre, classe="Défi", math_opts=True):
    """Assemble le dict question : 4 choix mélangés, indice de la bonne réponse, versions texte brut."""
    faux = [f for f in dict.fromkeys(faux) if f != bonne]
    random.shuffle(faux)
    opts = [bonne] + faux[:3]
    k = 1
    while len(opts) < 4:                      # sécurité : ne jamais renvoyer moins de 4 choix
        extra = r"%d" % (random.randint(2, 99) + k) if math_opts else "Aucune de ces réponses (%d)" % k
        if extra not in opts:
            opts.append(extra)
        k += 1
    random.shuffle(opts)
    idx = opts.index(bonne)
    if math_opts:
        opts = ["$" + o + "$" for o in opts]
    bonne_aff = opts[idx]
    return {
        "enonce": enonce, "options": opts, "index_correct": idx, "bonne_reponse": bonne_aff,
        "explication": explication, "chapitre": chapitre, "classe": classe,
        "enonce_txt": latex_vers_texte(enonce), "options_txt": [latex_vers_texte(o) for o in opts],
        "explication_txt": latex_vers_texte(explication),
    }


def _num_q(enonce, v, explication, chapitre, unite="", classe="Activité", fmt=None):
    """Question à réponse numérique : distracteurs générés automatiquement."""
    f = fmt or _n
    u = (r"\,\text{%s}" % unite) if unite else ""
    bonne = f(v) + u
    faux = [f(x) + u for x in [v + 1, v - 1, v * 2, v + 10, v - 10, v + 2, v - 2, -v, v + 5, v * 10]
            if x != v and f(x) != f(v)]
    return _construire(enonce, bonne, faux, explication, chapitre, classe)


# ----------------------------------------------------------------------------
# 16 ACTIVITÉS  (d = difficulté 1..5)
# ----------------------------------------------------------------------------
def a_calcul_mental(d):
    t = random.choice(["add", "mul", "pct", "sq"])
    if t == "add":
        a, b = random.randint(20, 40 * d + 60), random.randint(15, 40 * d + 50)
        return _num_q(f"Calculer mentalement : ${a} + {b}$.", a + b,
                      f"${a} + {b} = {a + b}$ (on additionne les dizaines puis les unités).", "Calcul mental")
    if t == "mul":
        a, b = random.randint(6, 9 + d), random.randint(6, 9 + d)
        return _num_q(f"Calculer mentalement : ${a} \\times {b}$.", a * b,
                      f"${a} \\times {b} = {a * b}$.", "Calcul mental")
    if t == "pct":
        n, p = random.choice([40, 60, 80, 120, 200, 240]), random.choice([5, 10, 15, 20, 25, 50])
        v = n * p // 100
        return _num_q(f"Combien font ${p}\\,\\%$ de ${n}$ ?", v,
                      f"${p}\\,\\% \\text{{ de }} {n} = {n} \\times \\dfrac{{{p}}}{{100}} = {v}$.", "Calcul mental")
    a = random.randint(11, 14 + 2 * d)
    return _num_q(f"Calculer : ${a}^2$.", a * a, f"${a}^2 = {a} \\times {a} = {a * a}$.", "Calcul mental")


def _pgcd_ppcm(d):
    g = random.randint(2, 9)
    while True:
        m, n = random.randint(2, 9), random.randint(2, 9)
        if m != n and math.gcd(m, n) == 1:
            break
    a, b = g * m, g * n
    ppcm = a * b // g
    if random.random() < .5:
        return _construire(f"Quel est le PGCD de ${a}$ et ${b}$ ?", str(g),
                           [str(ppcm), str(g * 2), str(max(1, g - 1)), str(g + 1)],
                           f"${a} = {g}\\times{m}$ et ${b} = {g}\\times{n}$ : le plus grand diviseur commun est ${g}$.",
                           "Arithmétique", "Activité")
    return _construire(f"Quel est le PPCM de ${a}$ et ${b}$ ?", str(ppcm),
                       [str(g), str(a * b), str(ppcm * 2), str(ppcm + g)],
                       f"$\\text{{PPCM}} = \\dfrac{{{a}\\times{b}}}{{\\text{{PGCD}}}} = \\dfrac{{{a * b}}}{{{g}}} = {ppcm}$.",
                       "Arithmétique", "Activité")


def a_arithmetique(d):
    t = random.choice(["pgcd", "premier", "div"])
    if t == "pgcd":
        return _pgcd_ppcm(d)
    if t == "premier":
        p = random.choice([23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])
        comp = random.sample([21, 27, 33, 39, 49, 51, 57, 63, 77, 87, 91, 93, 99], 3)
        return _construire("Lequel de ces nombres est premier ?", str(p), [str(c) for c in comp],
                           f"${p}$ n'est divisible que par $1$ et par lui-même ; les autres propositions ont un diviseur "
                           "différent de $1$ (par exemple $3$ ou $7$).", "Arithmétique", "Activité")
    n = random.choice([12, 18, 20, 24, 28, 30, 36, 45, 48])
    nb = sum(1 for k in range(1, n + 1) if n % k == 0)
    return _num_q(f"Combien le nombre ${n}$ possède-t-il de diviseurs positifs ?", nb,
                  f"On compte les diviseurs de ${n}$ : il y en a ${nb}$.", "Arithmétique")


def a_fractions(d):
    t = random.choice(["somme", "produit", "trois"])
    if t in ("somme", "produit"):
        b, dd = random.choice([2, 3, 4, 5, 6]), random.choice([2, 3, 4, 5, 6])
        a, c = random.randint(1, b + 1), random.randint(1, dd + 1)
        f1, f2 = Fraction(a, b), Fraction(c, dd)
        if t == "somme":
            r = f1 + f2
            faux = [Fraction(a + c, b + dd), f1 * f2, r + Fraction(1, b * dd), r - Fraction(1, b * dd), r + 1]
            expl = (f"On met au même dénominateur : ${_n(f1)} + {_n(f2)} = {_n(r)}$ "
                    "(on n'additionne jamais les dénominateurs).")
            enonce = f"Calculer ${_n(f1)} + {_n(f2)}$."
        else:
            r = f1 * f2
            faux = [f1 + f2, Fraction(a * c, b + dd), r * 2, r + Fraction(1, b * dd), f1 / f2 if f2 else r + 3]
            expl = f"On multiplie numérateurs et dénominateurs : ${_n(f1)} \\times {_n(f2)} = {_n(r)}$."
            enonce = f"Calculer ${_n(f1)} \\times {_n(f2)}$."
        return _construire(enonce, _n(r), [_n(x) for x in faux if x != r], expl, "Fractions", "Activité")
    n1, p1 = random.randint(2, 6), random.choice([150, 200, 250, 300, 450, 600])
    n2 = n1 + random.randint(2, 6)
    unit = p1 // n1 if p1 % n1 == 0 else None
    if unit is None:
        p1 = n1 * random.choice([50, 75, 100, 125])
        unit = p1 // n1
    v = unit * n2
    return _num_q(f"${n1}$ cahiers coûtent ${p1}$ francs. Combien coûtent ${n2}$ cahiers (même prix) ?", v,
                  f"Un cahier coûte ${p1}\\div{n1} = {unit}$ francs, donc ${n2}\\times{unit} = {v}$ francs.",
                  "Proportionnalité", "francs")


def a_equation(d):
    x = random.randint(-9, 12)
    a = random.randint(2, 6 + d)
    b = random.randint(-9, 12)
    if random.random() < .5:
        c = a * x + b
        enonce = f"Résoudre : ${_coef(a, 'x', True)}{_sg(b)} = {c}$."
        faux = [Fraction(c + b, a), Fraction(c - b, a) * -1, x + 1, x - 1, Fraction(c, a) + b]
        expl = f"${_coef(a, 'x', True)} = {c - b}$ donc $x = \\dfrac{{{c - b}}}{{{a}}} = {x}$."
    else:
        c = random.choice([k for k in range(-5, 6) if k != a and k != 0])
        e = a * x + b - c * x
        enonce = f"Résoudre : ${_coef(a, 'x', True)}{_sg(b)} = {_coef(c, 'x', True)}{_sg(e)}$."
        faux = [x + 1, x - 1, -x, Fraction(e - b, a + c) if a + c else x + 2, Fraction(b - e, a - c) * -1]
        expl = (f"On regroupe : ${_coef(a - c, 'x', True)} = {e - b}$ donc $x = \\dfrac{{{e - b}}}{{{a - c}}} = {x}$.")
    faux = ["x = " + _n(Fraction(f)) for f in faux if Fraction(f) != x]
    return _construire(enonce, f"x = {x}", faux, expl, "Équations", "Activité")


def a_puissances(d):
    if random.random() < .5:
        a, b = random.randint(2, 6), random.choice([2, 3, 5, 6, 7])
        N = a * a * b
        return _construire(f"Simplifier $\\sqrt{{{N}}}$.", f"{a}\\sqrt{{{b}}}",
                           [f"{b}\\sqrt{{{a}}}", f"{a + 1}\\sqrt{{{b}}}", f"{a * a}\\sqrt{{{b}}}", f"{a}\\sqrt{{{b + 1}}}"],
                           f"${N} = {a * a}\\times{b}$ donc $\\sqrt{{{N}}} = \\sqrt{{{a * a}}}\\times\\sqrt{{{b}}} = {a}\\sqrt{{{b}}}$.",
                           "Racines", "Activité")
    a, m, n = random.randint(2, 9), random.randint(2, 7), random.randint(2, 7)
    return _construire(f"Écrire sous la forme $a^k$ : ${a}^{{{m}}} \\times {a}^{{{n}}}$.", f"{a}^{{{m + n}}}",
                       [f"{a}^{{{m * n}}}", f"{a}^{{{abs(m - n) or 1}}}", f"{a * a}^{{{m + n}}}", f"{a}^{{{m + n + 1}}}"],
                       f"$a^m\\times a^n = a^{{m+n}}$ donc ${a}^{{{m}}}\\times{a}^{{{n}}} = {a}^{{{m + n}}}$.",
                       "Puissances", "Activité")


def a_identites(d):
    a = random.randint(2, 4 + d)
    t = random.choice(["plus", "moins", "diff"])
    if t == "plus":
        return _construire(f"Développer $(x + {a})^2$.", f"x^2 + {2 * a}x + {a * a}",
                           [f"x^2 + {a * a}", f"x^2 + {a}x + {a * a}", f"x^2 + {2 * a}x + {a}", f"x^2 - {2 * a}x + {a * a}"],
                           f"$(a+b)^2 = a^2 + 2ab + b^2$ avec $a = x$ et $b = {a}$ : $x^2 + {2 * a}x + {a * a}$.",
                           "Identités remarquables", "Activité")
    if t == "moins":
        return _construire(f"Développer $(x - {a})^2$.", f"x^2 - {2 * a}x + {a * a}",
                           [f"x^2 - {a * a}", f"x^2 + {2 * a}x + {a * a}", f"x^2 - {2 * a}x - {a * a}", f"x^2 - {a}x + {a * a}"],
                           f"$(a-b)^2 = a^2 - 2ab + b^2$ : $x^2 - {2 * a}x + {a * a}$.", "Identités remarquables", "Activité")
    return _construire(f"Factoriser $x^2 - {a * a}$.", f"(x - {a})(x + {a})",
                       [f"(x - {a})^2", f"(x + {a})^2", f"(x - {a * a})(x + 1)", f"(x - {a})(x - {a})"],
                       f"$a^2 - b^2 = (a-b)(a+b)$ avec $a = x$ et $b = {a}$.", "Identités remarquables", "Activité")


def a_systemes(d):
    while True:
        x, y = random.randint(-5, 8), random.randint(-5, 8)
        a1, b1, a2, b2 = [random.randint(-4, 5) for _ in range(4)]
        if a1 * b2 - a2 * b1 != 0 and 0 not in (a1, b1, a2, b2) and x != y:
            break
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    enonce = (f"Résoudre le système : $\\begin{{cases}} {_lin2(a1, b1)} = {c1} \\\\ {_lin2(a2, b2)} = {c2} "
              f"\\end{{cases}}$")
    f = lambda p, q: f"(x\\,;\\,y) = ({p}\\,;\\,{q})"
    return _construire(enonce, f(x, y), [f(y, x), f(-x, y), f(x, -y), f(x + 1, y - 1), f(x - 1, y + 1)],
                       f"On élimine une inconnue (combinaison linéaire) : on trouve $x = {x}$ puis $y = {y}$. "
                       f"Vérification : ${a1}\\times({x}){_sg(b1)}\\times({y}) = {c1}$.", "Systèmes", "Activité")


def a_derivation(d):
    t = random.choice(["poly", "valeur", "limite"])
    if t == "poly":
        a, b, c = random.randint(1, 5), random.randint(1, 6), random.randint(1, 9)
        fx = f"{a}x^3 + {b}x^2 + {c}x"
        bonne = f"{3 * a}x^2 + {2 * b}x + {c}"
        return _construire(f"Calculer la dérivée de $f(x) = {fx}$.", bonne,
                           [f"{a}x^2 + {b}x + {c}", f"{3 * a}x^2 + {b}x + {c}", f"{3 * a}x^2 + {2 * b}x",
                            f"{a}x^4/4 + {b}x^3/3 + {c}x^2/2".replace("/4", "").replace("/3", "").replace("/2", "")],
                           f"$(x^n)' = n x^{{n-1}}$ terme à terme : $f'(x) = {bonne}$.", "Dérivation", "Activité")
    if t == "valeur":
        a, b, k = random.randint(1, 5), random.randint(-6, 6), random.randint(1, 6)
        v = 2 * a * k + b
        return _num_q(f"Soit $f(x) = {a}x^2{_sg(b)}x$. Calculer $f'({k})$.", v,
                      f"$f'(x) = {2 * a}x{_sg(b)}$ donc $f'({k}) = {2 * a}\\times{k}{_sg(b)} = {v}$.", "Dérivation")
    a = random.randint(2, 9)
    return _construire(f"Calculer $\\displaystyle\\lim_{{x \\to {a}}} \\dfrac{{x^2 - {a * a}}}{{x - {a}}}$.", str(2 * a),
                       [str(a), str(a * a), "0", r"+\infty"],
                       f"$\\dfrac{{x^2-{a * a}}}{{x-{a}}} = x + {a}$ pour $x \\neq {a}$, et sa limite en ${a}$ est ${2 * a}$.",
                       "Limites", "Activité")


def a_complexes(d):
    t = random.choice(["produit", "module", "puissance"])
    if t == "produit":
        a, b, c, e = [random.randint(-4, 5) for _ in range(4)]
        if 0 in (a, b, c, e):
            a, b, c, e = 2, 3, 1, -2
        re_, im = a * c - b * e, a * e + b * c
        fmt = lambda r, i: f"{r}{_sg(i)}i"
        z1, z2 = f"{a}{_sg(b)}i", f"{c}{_sg(e)}i"
        return _construire(f"Calculer $({z1})({z2})$.", fmt(re_, im),
                           [fmt(a * c + b * e, im), fmt(re_, -im), fmt(a * c, b * e), fmt(im, re_)],
                           f"$(a+ib)(c+id) = (ac-bd) + (ad+bc)i$ avec $i^2 = -1$ : ${fmt(re_, im)}$.", "Complexes", "Activité")
    if t == "module":
        a, b = random.choice([(3, 4), (5, 12), (8, 15), (6, 8), (7, 24), (9, 12)])
        r = int(math.hypot(a, b))
        return _construire(f"Calculer le module de $z = {a} + {b}i$.", str(r),
                           [str(a + b), str(a * a + b * b), str(r + 1), f"\\sqrt{{{a + b}}}"],
                           f"$|z| = \\sqrt{{{a}^2 + {b}^2}} = \\sqrt{{{a * a + b * b}}} = {r}$.", "Complexes", "Activité")
    k = random.randint(5, 40)
    val = {0: "1", 1: "i", 2: "-1", 3: "-i"}[k % 4]
    return _construire(f"Calculer $i^{{{k}}}$.", val, [v for v in ("1", "i", "-1", "-i") if v != val],
                       f"$i^4 = 1$ et ${k} = 4\\times{k // 4} + {k % 4}$ donc $i^{{{k}}} = i^{{{k % 4}}} = {val}$.",
                       "Complexes", "Activité")


def a_integrale(d):
    t = random.choice(["lin", "puiss", "ln"])
    if t == "lin":
        a, b, c = random.randint(1, 6), random.choice([2, 4, 6, 3]), random.randint(1, 7)
        v = Fraction(b * a * a, 2) + c * a
        return _num_q(f"Calculer $\\displaystyle\\int_0^{{{a}}} ({b}x + {c})\\,dx$.", v,
                      f"Primitive : $\\dfrac{{{b}}}{{2}}x^2 + {c}x$. En ${a}$ : ${_n(v)}$ ; en $0$ : $0$.", "Intégrales", fmt=_n)
    if t == "puiss":
        k, n = random.randint(1, 6), random.randint(1, 4)
        v = Fraction(k, n + 1)
        return _construire(f"Calculer $\\displaystyle\\int_0^1 {k}x^{{{n}}}\\,dx$.", _n(v),
                           [_n(Fraction(k)), _n(Fraction(k, n)), _n(Fraction(k * (n + 1))), _n(v + 1)],
                           f"Primitive : $\\dfrac{{{k}}}{{{n + 1}}}x^{{{n + 1}}}$, évaluée entre $0$ et $1$ : ${_n(v)}$.",
                           "Intégrales", "Activité")
    a = random.choice([2, 3, 5, 7])
    return _construire(f"Calculer $\\displaystyle\\int_1^{{{a}}} \\dfrac{{1}}{{x}}\\,dx$.", f"\\ln {a}",
                       [f"\\dfrac{{1}}{{{a}}}", f"{a}\\ln {a}", f"\\ln {a} - 1", f"{a} - 1"],
                       f"Une primitive de $\\dfrac{{1}}{{x}}$ est $\\ln x$ : $\\ln {a} - \\ln 1 = \\ln {a}$.", "Intégrales", "Activité")


def a_mecanique(d):
    t = random.choice(["vitesse", "mrua", "newton", "chute"])
    if t == "vitesse":
        v, tt = random.randint(20, 90), random.randint(2, 5)
        return _num_q(f"Un véhicule parcourt ${v * tt}\\,\\text{{km}}$ en ${tt}\\,\\text{{h}}$. Quelle est sa vitesse moyenne ?", v,
                      f"$v = \\dfrac{{d}}{{t}} = \\dfrac{{{v * tt}}}{{{tt}}} = {v}\\,\\text{{km/h}}$.", "Mécanique", "km/h", "Activité")
    if t == "mrua":
        v0, a, tt = random.randint(0, 10), random.choice([2, 4, 6]), random.randint(2, 6)
        x = v0 * tt + a * tt * tt // 2
        return _num_q(f"Un mobile part avec $v_0 = {v0}\\,\\text{{m/s}}$ et une accélération constante $a = {a}\\,\\text{{m/s}}^2$. "
                      f"Quelle distance parcourt-il en ${tt}\\,\\text{{s}}$ ?", x,
                      f"$x = v_0 t + \\dfrac{{1}}{{2}}at^2 = {v0}\\times{tt} + \\dfrac{{1}}{{2}}\\times{a}\\times{tt}^2 = {x}\\,\\text{{m}}$.",
                      "Mécanique", "m", "Activité")
    if t == "newton":
        m, a = random.randint(2, 40), random.randint(2, 9)
        return _num_q(f"Quelle force faut-il appliquer à une masse de ${m}\\,\\text{{kg}}$ pour lui donner une accélération de ${a}\\,\\text{{m/s}}^2$ ?",
                      m * a, f"Deuxième loi de Newton : $F = ma = {m}\\times{a} = {m * a}\\,\\text{{N}}$.", "Mécanique", "N", "Activité")
    tt = random.randint(2, 6)
    return _num_q(f"Un objet tombe sans vitesse initiale (on prend $g = 10\\,\\text{{m/s}}^2$, frottements négligés). "
                  f"Quelle hauteur a-t-il parcourue au bout de ${tt}\\,\\text{{s}}$ ?", 5 * tt * tt,
                  f"$h = \\dfrac{{1}}{{2}}gt^2 = 5\\times{tt}^2 = {5 * tt * tt}\\,\\text{{m}}$.", "Mécanique", "m", "Activité")


def a_thermo(d):
    t = random.choice(["chaleur", "boyle", "premier", "rendement"])
    if t == "chaleur":
        m, dT = random.choice([0.5, 1, 2]), random.choice([10, 20, 25, 40])
        Q = int(4200 * m * dT)
        return _construire(f"Quelle énergie faut-il pour chauffer ${_n(m)}\\,\\text{{kg}}$ d'eau de ${dT}\\,^\\circ\\text{{C}}$ ? "
                           "($c_{eau} = 4200\\,\\text{J}\\cdot\\text{kg}^{-1}\\cdot\\text{K}^{-1}$)",
                           f"{_mil(Q)}\\,\\text{{J}}",
                           [f"{_mil(Q * 10)}\\,\\text{{J}}", f"{_mil(Q // 2)}\\,\\text{{J}}", f"{_mil(Q + 4200)}\\,\\text{{J}}",
                            f"{_mil(Q * 2)}\\,\\text{{J}}"],
                           f"$Q = mc\\Delta T = {_n(m)}\\times4200\\times{dT} = {_mil(Q)}\\,\\text{{J}}$.", "Thermodynamique", "Activité")
    if t == "boyle":
        P1, V1, k = random.choice([1, 2, 3]), random.choice([4, 6, 8]), random.choice([2, 4])
        V2 = V1 // k if V1 % k == 0 else V1 // 2
        k = V1 // V2
        P2 = P1 * k
        return _num_q(f"Un gaz parfait à température constante occupe ${V1}\\,\\text{{L}}$ sous ${P1}\\,\\text{{bar}}$. "
                      f"On le comprime à ${V2}\\,\\text{{L}}$. Quelle est la nouvelle pression ?", P2,
                      f"Loi de Boyle-Mariotte : $P_1V_1 = P_2V_2$ donc $P_2 = \\dfrac{{{P1}\\times{V1}}}{{{V2}}} = {P2}\\,\\text{{bar}}$.",
                      "Thermodynamique", "bar", "Activité")
    if t == "premier":
        Q, W = random.choice([300, 500, 800, 1000]), random.choice([-200, -100, 150, 200, 400])
        U = Q + W
        return _num_q(f"Un système reçoit une chaleur $Q = {Q}\\,\\text{{J}}$ et un travail $W = {W}\\,\\text{{J}}$. Quelle est la variation d'énergie interne $\\Delta U$ ?",
                      U, f"Premier principe : $\\Delta U = Q + W = {Q}{_sg(W)} = {U}\\,\\text{{J}}$.", "Thermodynamique", "J", "Activité")
    Tf, Tc = random.choice([(300, 600), (300, 500), (250, 500), (400, 800), (300, 1200)])
    eta = round(100 * (1 - Tf / Tc))
    return _num_q(f"Quel est le rendement maximal (de Carnot) d'une machine fonctionnant entre ${Tc}\\,\\text{{K}}$ (source chaude) et ${Tf}\\,\\text{{K}}$ (source froide) ?",
                  eta, f"$\\eta = 1 - \\dfrac{{T_f}}{{T_c}} = 1 - \\dfrac{{{Tf}}}{{{Tc}}} = {eta}\\,\\%$.", "Thermodynamique", r"\%", "Activité")


def a_optique(d):
    t = random.choice(["lentille", "snell", "miroir"])
    if t == "lentille":
        f, p = random.choice([(10, 15), (10, 20), (10, 30), (20, 30), (20, 40), (20, 60), (15, 30), (15, 20)])
        pp = Fraction(f * -p, -p + f)
        return _num_q(f"Une lentille mince convergente a une distance focale $f' = {f}\\,\\text{{cm}}$. Un objet est placé à ${p}\\,\\text{{cm}}$ devant elle. "
                      "À quelle distance de la lentille se forme l'image ?", int(pp),
                      f"Conjugaison : $\\dfrac{{1}}{{p'}} - \\dfrac{{1}}{{p}} = \\dfrac{{1}}{{f'}}$ avec $p = -{p}$ : "
                      f"$\\dfrac{{1}}{{p'}} = \\dfrac{{1}}{{{f}}} - \\dfrac{{1}}{{{p}}}$ donc $p' = {int(pp)}\\,\\text{{cm}}$.",
                      "Optique", "cm", "Activité")
    if t == "snell":
        n1 = Fraction(random.choice([1, 2]))
        n2 = Fraction(random.choice([3, 4, 5]), 2) if n1 == 1 else Fraction(random.choice([3, 4]))
        r = n1 * Fraction(1, 2) / n2
        return _construire(f"Un rayon passe d'un milieu d'indice $n_1 = {_n(n1)}$ à un milieu d'indice $n_2 = {_n(n2)}$ avec un angle d'incidence "
                           f"$i_1 = 30^\\circ$. Que vaut $\\sin i_2$ ?", _n(r),
                           [_n(r * 2), _n(Fraction(1, 2)), _n(r + Fraction(1, 4)), _n(Fraction(n2, n1) * Fraction(1, 2))],
                           f"Loi de Snell-Descartes : $n_1\\sin i_1 = n_2\\sin i_2$ donc $\\sin i_2 = \\dfrac{{{_n(n1)}\\times\\frac12}}{{{_n(n2)}}} = {_n(r)}$.",
                           "Optique", "Activité")
    ang = random.choice([20, 25, 30, 35, 40, 55])
    return _construire(f"Un rayon lumineux fait un angle de ${ang}^\\circ$ avec la surface d'un miroir plan. Quel est l'angle de réflexion (mesuré par rapport à la normale) ?",
                       f"{90 - ang}^\\circ", [f"{ang}^\\circ", f"{90 + ang}^\\circ", f"{2 * ang}^\\circ", f"{180 - ang}^\\circ"],
                       f"L'angle d'incidence vaut $90^\\circ - {ang}^\\circ = {90 - ang}^\\circ$ ; l'angle de réflexion lui est égal.", "Optique", "Activité")


def a_electro(d):
    t = random.choice(["coulomb", "champ", "capa", "energie"])
    if t == "coulomb":
        q1, q2, r = random.randint(1, 5), random.randint(1, 5), random.choice([1, 2, 3])
        F = 9e9 * q1 * q2 * 1e-12 / (r * r)
        return _construire(f"Deux charges $q_1 = {q1}\\,\\mu\\text{{C}}$ et $q_2 = {q2}\\,\\mu\\text{{C}}$ sont distantes de ${r}\\,\\text{{m}}$. "
                           "Quelle est la valeur de la force électrostatique ? ($k = 9\\times10^9\\,\\text{SI}$)",
                           _sci(F) + r"\,\text{N}",
                           [_sci(F * 10) + r"\,\text{N}", _sci(F / 10) + r"\,\text{N}", _sci(F * r) + r"\,\text{N}" if r > 1 else _sci(F * 3) + r"\,\text{N}",
                            _sci(F * 100) + r"\,\text{N}"],
                           f"$F = k\\dfrac{{q_1q_2}}{{r^2}} = 9\\times10^9\\times\\dfrac{{{q1}\\times10^{{-6}}\\times{q2}\\times10^{{-6}}}}{{{r}^2}} = {_sci(F)}\\,\\text{{N}}$.",
                           "Électrostatique", "Activité")
    if t == "champ":
        q, r = random.randint(1, 8), random.choice([1, 2, 3, 6])
        E = 9e3 * q / (r * r)
        return _construire(f"Quelle est l'intensité du champ électrique créé par une charge $q = {q}\\,\\mu\\text{{C}}$ à ${r}\\,\\text{{m}}$ de celle-ci ?",
                           _sci(E) + r"\,\text{V/m}", [_sci(E * 10) + r"\,\text{V/m}", _sci(E * r) + r"\,\text{V/m}" if r > 1 else _sci(E / 10) + r"\,\text{V/m}",
                                                       _sci(E / 10) + r"\,\text{V/m}", _sci(E * 100) + r"\,\text{V/m}"],
                           f"$E = k\\dfrac{{q}}{{r^2}} = 9\\times10^9\\times\\dfrac{{{q}\\times10^{{-6}}}}{{{r}^2}} = {_sci(E)}\\,\\text{{V/m}}$.",
                           "Électrostatique", "Activité")
    if t == "capa":
        U, C = random.choice([10, 20, 50, 100]), random.choice([2, 4, 5, 10])
        Q = C * U
        return _construire(
            f"Un condensateur est chargé avec $Q = {Q}\\,\\mu\\text{{C}}$ sous une tension $U = {U}\\,\\text{{V}}$. Quelle est sa capacité ?",
            f"{C}\\,\\mu\\text{{F}}",
            [f"{C * 2}\\,\\mu\\text{{F}}", f"{max(1, C // 2)}\\,\\mu\\text{{F}}", f"{Q * U}\\,\\mu\\text{{F}}", f"{C + 1}\\,\\mu\\text{{F}}"],
            f"$C = \\dfrac{{Q}}{{U}} = \\dfrac{{{Q}}}{{{U}}} = {C}\\,\\mu\\text{{F}}$.", "Électrostatique", "Activité")
    C, U = random.choice([2, 4, 6]), random.choice([10, 20, 30])
    W = C * U * U // 2
    return _construire(f"Quelle énergie est stockée dans un condensateur de ${C}\\,\\mu\\text{{F}}$ chargé sous ${U}\\,\\text{{V}}$ ?",
                       f"{W}\\,\\mu\\text{{J}}", [f"{W * 2}\\,\\mu\\text{{J}}", f"{W // 2}\\,\\mu\\text{{J}}", f"{C * U}\\,\\mu\\text{{J}}", f"{W + C}\\,\\mu\\text{{J}}"],
                       f"$W = \\dfrac{{1}}{{2}}CU^2 = \\dfrac{{1}}{{2}}\\times{C}\\times{U}^2 = {W}\\,\\mu\\text{{J}}$.", "Électrostatique", "Activité")


def _vec(v):
    return r"\begin{pmatrix}%s\end{pmatrix}" % r"\\".join(str(c) for c in v)


def a_vectoriel(d):
    t = random.choice(["scalaire", "norme", "ortho", "croix"])
    if t == "scalaire":
        u, v = [[random.randint(-4, 5) for _ in range(3)] for _ in range(2)]
        s = sum(a * b for a, b in zip(u, v))
        return _num_q(f"Calculer le produit scalaire $\\vec{{u}}\\cdot\\vec{{v}}$ avec $\\vec{{u}}={_vec(u)}$ et $\\vec{{v}}={_vec(v)}$.", s,
                      f"$\\vec u\\cdot\\vec v = {u[0]}\\times({v[0]}) + {u[1]}\\times({v[1]}) + {u[2]}\\times({v[2]}) = {s}$.", "Vecteurs")
    if t == "norme":
        a, b, c, n = random.choice([(1, 2, 2, 3), (2, 3, 6, 7), (2, 6, 9, 11), (1, 4, 8, 9), (4, 4, 7, 9), (2, 10, 11, 15)])
        return _construire(f"Calculer la norme de $\\vec{{u}} = {_vec([a, b, c])}$.", str(n),
                           [str(a + b + c), str(a * a + b * b + c * c), str(n + 1), f"\\sqrt{{{a + b + c}}}"],
                           f"$\\|\\vec u\\| = \\sqrt{{{a}^2+{b}^2+{c}^2}} = \\sqrt{{{a * a + b * b + c * c}}} = {n}$.", "Vecteurs", "Activité")
    if t == "ortho":
        for _ in range(300):
            a, b, dd, e, k = (random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, 4))
            if (a * dd + b * e) % k == 0:
                c = -(a * dd + b * e) // k
                break
        else:
            a, b, c, dd, e, k = 1, 2, -3, 1, 2, 1
        return _num_q(f"Pour quelle valeur de $k$ les vecteurs $\\vec{{u}}={_vec([a, b, c])}$ et $\\vec{{v}}={_vec([dd, e, 'k'])}$ sont-ils orthogonaux ?", k,
                      f"Orthogonaux $\\Leftrightarrow \\vec u\\cdot\\vec v = 0$ : ${a * dd + b * e} {_sg(c)}k = 0$ donc $k = {k}$.", "Vecteurs")
    a, b, c, e = [random.randint(-4, 5) for _ in range(4)]
    z = a * e - b * c
    return _num_q(f"Calculer la composante en $z$ du produit vectoriel $\\vec{{u}}\\wedge\\vec{{v}}$ avec $\\vec{{u}}={_vec([a, b, 0])}$ et $\\vec{{v}}={_vec([c, e, 0])}$.", z,
                  f"Pour deux vecteurs du plan, $(\\vec u\\wedge\\vec v)_z = u_xv_y - u_yv_x = {a}\\times({e}) - ({b})\\times({c}) = {z}$.", "Vecteurs")


def a_quantique(d):
    t = random.choice(["bohr", "transition", "broglie", "proba"])
    if t == "bohr":
        n = random.randint(2, 4)
        E = round(-13.6 / n ** 2, 2)
        return _construire(f"Dans le modèle de Bohr de l'atome d'hydrogène, quelle est l'énergie du niveau $n = {n}$ ? ($E_n = -\\dfrac{{13{{,}}6}}{{n^2}}$ eV)",
                           _n(E) + r"\,\text{eV}", [_n(round(-13.6 / (n - 1) ** 2, 2)) + r"\,\text{eV}", _n(round(13.6 / n ** 2, 2)) + r"\,\text{eV}",
                                                    _n(round(-13.6 / n, 2)) + r"\,\text{eV}", _n(round(-13.6 * n, 2)) + r"\,\text{eV}"],
                           f"$E_{{{n}}} = -\\dfrac{{13{{,}}6}}{{{n}^2}} = {_n(E)}\\,\\text{{eV}}$.", "Quantique", "Activité")
    if t == "transition":
        n, m = random.choice([(3, 2), (2, 1), (4, 2), (3, 1), (4, 1)])
        dE = round(13.6 * (1 / m ** 2 - 1 / n ** 2), 2)
        return _construire(f"Un électron de l'atome d'hydrogène passe du niveau $n = {n}$ au niveau $n = {m}$. Quelle est l'énergie du photon émis ?",
                           _n(dE) + r"\,\text{eV}", [_n(round(13.6 * (1 / m - 1 / n), 2)) + r"\,\text{eV}", _n(round(13.6 * (m - n) ** 0 / m ** 2, 2)) + r"\,\text{eV}",
                                                    _n(round(dE * 2, 2)) + r"\,\text{eV}", _n(round(13.6 / n ** 2, 2)) + r"\,\text{eV}"],
                           f"$\\Delta E = 13{{,}}6\\left(\\dfrac{{1}}{{{m}^2}} - \\dfrac{{1}}{{{n}^2}}\\right) = {_n(dE)}\\,\\text{{eV}}$.", "Quantique", "Activité")
    if t == "broglie":
        k = random.choice([2, 3, 4, 5])
        return _construire(f"D'après la relation de de Broglie $\\lambda = \\dfrac{{h}}{{p}}$, que devient la longueur d'onde d'une particule si sa quantité de mouvement $p$ est multipliée par ${k}$ ?",
                           f"\\text{{divisée par }}{k}", [f"\\text{{multipliée par }}{k}", f"\\text{{multipliée par }}{k * k}", "\\text{inchangée}",
                                                           f"\\text{{divisée par }}{k * k}"],
                           f"$\\lambda$ est inversement proportionnelle à $p$ : si $p \\to {k}p$ alors $\\lambda \\to \\dfrac{{\\lambda}}{{{k}}}$.", "Quantique", "Activité")
    a, b = random.choice([(3, 4), (5, 12), (8, 15)])
    h = int(math.hypot(a, b))
    return _construire(f"Un état quantique est $|\\psi\\rangle = \\dfrac{{{a}}}{{{h}}}|0\\rangle + \\dfrac{{{b}}}{{{h}}}|1\\rangle$. Quelle est la probabilité de mesurer $|1\\rangle$ ?",
                       f"\\dfrac{{{b * b}}}{{{h * h}}}", [f"\\dfrac{{{b}}}{{{h}}}", f"\\dfrac{{{a * a}}}{{{h * h}}}", f"\\dfrac{{{a * b}}}{{{h * h}}}", f"\\dfrac{{{b + 1}}}{{{h}}}"],
                       f"La probabilité est le carré du module de l'amplitude : $\\left(\\dfrac{{{b}}}{{{h}}}\\right)^2 = \\dfrac{{{b * b}}}{{{h * h}}}$.", "Quantique", "Activité")


_ACTIVITES = dict(zip(LISTE_ACTIVITES, [
    a_calcul_mental, a_arithmetique, a_fractions, a_equation, a_puissances, a_identites, a_systemes, a_derivation,
    a_complexes, a_integrale, a_mecanique, a_thermo, a_optique, a_electro, a_vectoriel, a_quantique]))


# ----------------------------------------------------------------------------
# SUJETS CASSE-TÊTE
# ----------------------------------------------------------------------------
_PARADOXES = [
    ("Dans l'hôtel de Hilbert (une infinité de chambres numérotées $1, 2, 3, \\dots$), toutes les chambres sont occupées. Un nouveau client arrive. Que fait le réceptionniste ?",
     "Il déplace le client de la chambre $n$ dans la chambre $n+1$, puis loge le nouveau en chambre $1$.",
     ["Il refuse : l'hôtel est plein.", "Il construit une chambre supplémentaire à la fin.", "Il met deux clients dans la chambre $1$ sans déplacer personne."],
     "Un ensemble infini peut être mis en bijection avec une partie de lui-même : $n \\mapsto n+1$ libère la chambre $1$."),
    ("Que vaut $0{,}999\\ldots$ (une infinité de $9$) ?",
     "Exactement $1$.", ["Un nombre juste inférieur à $1$.", "$0{,}999\\ldots9$ avec un $9$ de moins que $1$.", "Ce nombre n'existe pas."],
     "$x = 0{,}999\\ldots$ donne $10x - x = 9$, donc $x = 1$. On peut aussi écrire $3\\times\\dfrac{1}{3} = 3\\times0{,}333\\ldots = 0{,}999\\ldots = 1$."),
    ("Achille court deux fois plus vite que la tortue qui a une avance. Zénon affirme qu'il ne la rattrapera jamais. Pourquoi est-ce faux ?",
     "Parce qu'une somme infinie de durées de plus en plus petites peut être finie : $\\sum_{k\\geq1} 2^{-k} = 1$.",
     ["Parce que la tortue finit par s'arrêter.", "Parce qu'une somme infinie vaut toujours l'infini.", "Parce que le temps n'est pas divisible."],
     "Les durées successives forment une série géométrique convergente : $\\dfrac12 + \\dfrac14 + \\dfrac18 + \\cdots = 1$."),
    ("Dans un groupe de $23$ personnes, la probabilité que deux d'entre elles au moins aient le même anniversaire est :",
     "Un peu plus de $50\\,\\%$.", ["Environ $6\\,\\%$ ($23/365$).", "Environ $25\\,\\%$.", "Moins de $1\\,\\%$."],
     "On calcule la probabilité inverse : $\\prod_{k=0}^{22}\\dfrac{365-k}{365} \\approx 0{,}49$, donc la probabilité cherchée vaut $\\approx 0{,}51$."),
    ("Paradoxe de Monty Hall : $3$ portes, une voiture derrière l'une d'elles. Tu choisis une porte, l'animateur (qui sait) ouvre une autre porte perdante. Que vaut-il mieux faire ?",
     "Changer de porte : on gagne avec une probabilité de $\\dfrac23$.", ["Garder sa porte : $\\dfrac23$.", "Cela ne change rien : $\\dfrac12$ dans les deux cas.", "Changer de porte : $\\dfrac13$."],
     "Ta première porte est bonne avec la probabilité $\\dfrac13$. Dans les $\\dfrac23$ des cas restants, changer fait gagner."),
    ("« Preuve » que $1 = 2$ : on pose $a = b$, d'où $a^2 = ab$, $a^2 - b^2 = ab - b^2$, $(a-b)(a+b) = b(a-b)$, puis on simplifie par $(a-b)$ : $a + b = b$ donc $2b = b$ et $2 = 1$. Où est l'erreur ?",
     "On divise par $a - b$, qui vaut $0$.", ["Le développement de $a^2 - b^2$ est faux.", "On n'a pas le droit de poser $a = b$.", "L'égalité $2b = b$ est valable."],
     "Comme $a = b$, on a $a - b = 0$ et la division par zéro est interdite."),
    ("Paradoxe du barbier : « Le barbier rase tous les hommes du village qui ne se rasent pas eux-mêmes, et seulement eux. » Que peut-on conclure ?",
     "Un tel barbier ne peut pas exister.", ["Le barbier se rase lui-même.", "Le barbier ne se rase pas lui-même.", "Le village est infini."],
     "S'il se rase lui-même, il ne devrait pas ; s'il ne se rase pas, il devrait. C'est le paradoxe de Russell sur l'ensemble des ensembles qui ne se contiennent pas."),
    ("Que prouve l'argument diagonal de Cantor ?",
     "Il y a strictement plus de réels que d'entiers naturels.", ["Les réels et les entiers sont aussi nombreux.", "Il n'y a pas d'infini.", "Les entiers sont plus nombreux que les réels."],
     "Pour toute liste de réels, on construit un réel différent du $n$-ième par sa $n$-ième décimale : $\\mathbb{R}$ n'est pas dénombrable."),
    ("« Preuve » que $-1 = 1$ : $-1 = i\\times i = \\sqrt{-1}\\times\\sqrt{-1} = \\sqrt{(-1)\\times(-1)} = \\sqrt{1} = 1$. Quelle égalité est fausse ?",
     "$\\sqrt{-1}\\times\\sqrt{-1} = \\sqrt{(-1)\\times(-1)}$, valable seulement pour des réels positifs.", ["$i\\times i = -1$.", "$\\sqrt{1} = 1$.", "$(-1)\\times(-1) = 1$."],
     "La règle $\\sqrt{a}\\sqrt{b} = \\sqrt{ab}$ n'est valable que pour $a, b \\geq 0$."),
    ("Une feuille de papier d'épaisseur $0{,}1\\,\\text{mm}$ est pliée $42$ fois sur elle-même (en théorie). Quelle est l'épaisseur obtenue ?",
     "Environ $4{,}4\\times10^5\\,\\text{km}$ : à peu près la distance Terre–Lune.", ["Environ $4{,}2\\,\\text{m}$.", "Environ $420\\,\\text{m}$.", "Environ $4\\,\\text{km}$."],
     "$0{,}1\\,\\text{mm}\\times2^{42} \\approx 4{,}4\\times10^{11}\\,\\text{mm} \\approx 4{,}4\\times10^{5}\\,\\text{km}$ : la croissance exponentielle est trompeuse."),
]


def _casse_tete_paradoxe():
    enonce, bonne, faux, expl = random.choice(_PARADOXES)
    return _construire(enonce, bonne, faux, expl, "Paradoxes", "Casse-tête", math_opts=False)


def _enigme():
    t = random.choice(["nombre", "somme_produit", "ages", "consecutifs", "inverse", "suite", "balance"])
    if t == "nombre":
        n, k = random.randint(3, 20), random.randint(2, 9)
        return _num_q(f"Je pense à un nombre. Je le double, j'ajoute ${2 * k}$, je divise par $2$, puis je retire le nombre de départ. Quel est le résultat ?", k,
                      f"Avec le nombre $n$ : $\\dfrac{{2n + {2 * k}}}{{2}} - n = {k}$ ; le résultat ne dépend pas de $n$.", "Énigmes", classe="Casse-tête")
    if t == "somme_produit":
        x, y = random.sample(range(2, 10), 2)
        S, P = x + y, x * y
        return _num_q(f"Deux nombres ont pour somme ${S}$ et pour produit ${P}$. Que vaut la somme de leurs carrés ?", S * S - 2 * P,
                      f"$x^2 + y^2 = (x+y)^2 - 2xy = {S}^2 - 2\\times{P} = {S * S - 2 * P}$.", "Énigmes", classe="Casse-tête")
    if t == "ages":
        k = random.choice([4, 5, 6, 8, 10])
        return _num_q(f"Un père a $4$ fois l'âge de son fils. Dans ${k}$ ans, il aura $3$ fois l'âge de son fils. Quel est l'âge actuel du père ?", 8 * k,
                      f"Fils $f$, père $4f$ : $4f + {k} = 3(f + {k})$ donc $f = {2 * k}$ et le père a $4f = {8 * k}$ ans.", "Énigmes", "ans", "Casse-tête")
    if t == "consecutifs":
        n = random.randint(5, 40)
        return _num_q(f"La somme de trois entiers consécutifs est ${3 * n}$. Quel est le plus grand des trois ?", n + 1,
                      f"Les trois entiers sont $x-1, x, x+1$ de somme $3x = {3 * n}$ : $x = {n}$, le plus grand est ${n + 1}$.", "Énigmes", classe="Casse-tête")
    if t == "inverse":
        k = random.randint(3, 8)
        return _num_q(f"Soit $x$ un réel non nul tel que $x + \\dfrac{{1}}{{x}} = {k}$. Que vaut $x^2 + \\dfrac{{1}}{{x^2}}$ ?", k * k - 2,
                      f"$\\left(x + \\dfrac1x\\right)^2 = x^2 + 2 + \\dfrac1{{x^2}}$ donc $x^2 + \\dfrac1{{x^2}} = {k}^2 - 2 = {k * k - 2}$.", "Énigmes", classe="Casse-tête")
    if t == "suite":
        a = random.randint(1, 4)
        termes = [n * (n + a) for n in range(1, 6)]
        return _num_q(f"Quel est le terme suivant de la suite ${', '.join(map(str, termes))}, \\ldots$ ?", 6 * (6 + a),
                      f"Le terme de rang $n$ vaut $n(n + {a})$ ; pour $n = 6$ : $6\\times{6 + a} = {6 * (6 + a)}$.", "Énigmes", classe="Casse-tête")
    p, b = random.randint(1, 9), random.randint(1, 9)
    s1, s2 = 2 * p + b, p + 2 * b
    return _num_q(f"$2$ pommes et $1$ banane coûtent ${s1}$ francs ; $1$ pomme et $2$ bananes coûtent ${s2}$ francs. Combien coûtent ensemble $1$ pomme et $1$ banane ?", p + b,
                  f"En additionnant : $3p + 3b = {s1 + s2}$ donc $p + b = {p + b}$ francs (sans résoudre le système).", "Énigmes", "francs", "Casse-tête")


def _geometrie():
    t = random.choice(["angle", "diagonales", "cube", "inscrit", "carre", "equi", "sphere", "paves"])
    if t == "angle":
        n = random.choice([5, 6, 8, 9, 10, 12])
        v = (n - 2) * 180 // n
        return _construire(f"Quelle est la mesure d'un angle intérieur d'un polygone régulier à ${n}$ côtés ?", f"{v}^\\circ",
                           [f"{v + 10}^\\circ", f"{v - 12}^\\circ", f"{360 // n}^\\circ", f"{(n - 1) * 180 // n}^\\circ"],
                           f"Somme des angles : $(n-2)\\times180^\\circ$, donc chaque angle vaut $\\dfrac{{({n}-2)\\times180}}{{{n}}} = {v}^\\circ$.", "Géométrie", "Casse-tête")
    if t == "diagonales":
        n = random.randint(6, 12)
        return _num_q(f"Combien de diagonales possède un polygone convexe à ${n}$ côtés ?", n * (n - 3) // 2,
                      f"Chaque sommet envoie $n - 3$ diagonales et chacune est comptée deux fois : $\\dfrac{{{n}\\times{n - 3}}}{{2}} = {n * (n - 3) // 2}$.", "Géométrie", classe="Casse-tête")
    if t == "cube":
        k = random.randint(2, 9)
        return _construire(f"Quelle est la longueur de la grande diagonale d'un cube d'arête ${k}$ ?", f"{k}\\sqrt{{3}}",
                           [f"{k}\\sqrt{{2}}", f"{3 * k}", f"{k}\\sqrt{{6}}", f"{k * k}\\sqrt{{3}}"],
                           f"$d = \\sqrt{{a^2 + a^2 + a^2}} = a\\sqrt3$ avec $a = {k}$.", "Géométrie", "Casse-tête")
    if t == "inscrit":
        a, b, c, r = random.choice([(3, 4, 5, 1), (5, 12, 13, 2), (8, 15, 17, 3), (6, 8, 10, 2), (9, 12, 15, 3), (7, 24, 25, 3)])
        return _num_q(f"Quel est le rayon du cercle inscrit dans le triangle rectangle de côtés ${a}$, ${b}$ et ${c}$ ?", r,
                      f"Pour un triangle rectangle, $r = \\dfrac{{a + b - c}}{{2}} = \\dfrac{{{a} + {b} - {c}}}{{2}} = {r}$.", "Géométrie", classe="Casse-tête")
    if t == "carre":
        k = random.randint(2, 7)
        return _construire(f"Un carré est inscrit dans un cercle de rayon ${k}$. Quelle est son aire ?", f"{2 * k * k}",
                           [f"{k * k}", f"{4 * k * k}", f"{k * k}\\pi", f"{2 * k}"],
                           f"La diagonale du carré vaut $2R = {2 * k}$ ; son aire est $\\dfrac{{d^2}}{{2}} = \\dfrac{{{4 * k * k}}}{{2}} = {2 * k * k}$.", "Géométrie", "Casse-tête")
    if t == "equi":
        k = random.randint(2, 8)
        return _construire(f"Quelle est l'aire d'un triangle équilatéral de côté ${2 * k}$ ?", f"{k * k}\\sqrt{{3}}",
                           [f"{2 * k * k}\\sqrt{{3}}", f"{k * k}", f"{k}\\sqrt{{3}}", f"{k * k}\\sqrt{{2}}"],
                           f"$\\mathcal A = \\dfrac{{\\sqrt3}}{{4}}c^2 = \\dfrac{{\\sqrt3}}{{4}}\\times{4 * k * k} = {k * k}\\sqrt3$.", "Géométrie", "Casse-tête")
    if t == "sphere":
        return _construire("Une sphère est inscrite dans un cube. Quel est le rapport $\\dfrac{\\text{volume de la sphère}}{\\text{volume du cube}}$ ?", "\\dfrac{\\pi}{6}",
                           ["\\dfrac{\\pi}{4}", "\\dfrac{\\pi}{3}", "\\dfrac{2\\pi}{3}", "\\dfrac{\\pi}{8}"],
                           "Arête $2R$ : $\\dfrac{\\frac43\\pi R^3}{(2R)^3} = \\dfrac{\\frac43\\pi R^3}{8R^3} = \\dfrac{\\pi}{6}$.", "Géométrie", "Casse-tête")
    a, b, c, n = random.choice([(1, 2, 2, 3), (2, 3, 6, 7), (2, 6, 9, 11), (1, 4, 8, 9), (4, 4, 7, 9)])
    return _num_q(f"Quelle est la diagonale d'un pavé droit de dimensions ${a}\\times{b}\\times{c}$ ?", n,
                  f"$d = \\sqrt{{{a}^2 + {b}^2 + {c}^2}} = \\sqrt{{{a * a + b * b + c * c}}} = {n}$.", "Géométrie", classe="Casse-tête")


_CASSE_TETE = {"Paradoxes": _casse_tete_paradoxe, "Énigmes": _enigme, "Géométrie": _geometrie}


# ----------------------------------------------------------------------------
# API publique
# ----------------------------------------------------------------------------
def _sans_erreur(fabrique, *args):
    """Une question valide quoi qu'il arrive (réessaie en cas de tirage dégénéré)."""
    derniere = None
    for _ in range(25):
        try:
            q = fabrique(*args)
            if q and len(q["options"]) == 4 and len(set(q["options"])) == 4 and 0 <= q["index_correct"] < 4:
                return q
        except Exception as e:                     # noqa: BLE001
            derniere = e
    raise RuntimeError(f"génération impossible : {derniere}")


def generer_activite(nom, difficulte=1):
    """Question de l'activité « nom » (voir LISTE_ACTIVITES). difficulte : 1 à 5."""
    d = max(1, min(5, int(difficulte)))
    gen = _ACTIVITES.get(nom, a_calcul_mental)
    q = _sans_erreur(gen, d)
    q["chapitre"] = nom
    return q


def generer_casse_tete(type_defi):
    """Question du casse-tête « Paradoxes », « Énigmes » ou « Géométrie »."""
    q = _sans_erreur(_CASSE_TETE.get(type_defi, _enigme))
    return q
