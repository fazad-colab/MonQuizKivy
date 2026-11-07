# -*- coding: utf-8 -*-
"""
generateurs_latex.py
====================
Générateurs de questions écrits directement en LaTeX (KaTeX).
Chaque générateur : f(fd) -> (enonce, bonne_reponse, [distracteurs], explication)
   fd = facteur de difficulté (>= 1)

- corrigent les chapitres qui avaient une erreur de logique dans l'ancien moteur
  (Arithmétique, Fraction, Puissance, PGCD/PPCM) ;
- ajoutent les chapitres du programme qui n'avaient AUCUN générateur
  (Notion d'équation, Équations/Inéquations, Repérage, Polygone, Polygone régulier,
   Vecteur et Homothétie, Analyse 1, Analyse 2).
Toutes les bonnes réponses sont CALCULÉES (jamais écrites à la main).
"""
import math
import random
from fractions import Fraction


# ----------------------------------------------------------------------------
# Outils d'écriture LaTeX
# ----------------------------------------------------------------------------
def M(s):
    """Entoure d'un environnement math en ligne.
    '@' est un alias d'antislash (permet d'écrire du LaTeX dans des f-strings, compatible Python 3.8+)."""
    return "$" + str(s).replace("@", "\\") + "$"


def nb(x):
    """Nombre -> LaTeX (virgule décimale française, signe moins propre)."""
    if isinstance(x, Fraction):
        return fr(x)
    if isinstance(x, float):
        if x == int(x):
            return str(int(x))
        t = ("%.4f" % x).rstrip("0").rstrip(".")
        return t.replace(".", "{,}")
    return str(x)


def fr(f):
    """Fraction -> \\frac{a}{b} (ou entier)."""
    f = Fraction(f)
    if f.denominator == 1:
        return str(f.numerator)
    signe = "-" if f < 0 else ""
    return signe + r"\frac{" + str(abs(f.numerator)) + "}{" + str(f.denominator) + "}"


def pm(x, var="x"):
    """Terme '+ 3x' / '- 3x' pour écrire un polynôme."""
    if x == 0:
        return ""
    signe = "+" if x > 0 else "-"
    a = abs(x)
    return f" {signe} {'' if a == 1 and var else a}{var}" if var else f" {signe} {a}"


def poly(a, b, c=None):
    """a x^2 + b x + c  (ou a x + b si c est None) en LaTeX."""
    if c is None:
        t = ("-" if a == -1 else "" if a == 1 else str(a)) + "x"
        return (t + pm(b, "")).strip()
    t = ("-" if a == -1 else "" if a == 1 else str(a)) + "x^{2}"
    return (t + pm(b, "x") + pm(c, "")).strip()


def intervalle(borne, sens, strict):
    """Solution d'une inéquation sous forme d'intervalle (notation ouverte [ ] française)."""
    b = nb(borne)
    if sens == "<":      # x < b  ou x <= b
        return r"\left]-\infty\,;\,%s\right%s" % (b, "[" if strict else "]")
    return r"\left%s%s\,;\,+\infty\right[" % ("]" if strict else "[", b)


def cf(a):
    """Coefficient devant une variable : 1 -> '' (on écrit x et non 1x)."""
    return "" if a == 1 else ("-" if a == -1 else str(a))


def _autres(correct, candidats):
    """Retire doublons / la bonne réponse."""
    vus, sortie = {correct}, []
    for c in candidats:
        if c not in vus:
            vus.add(c)
            sortie.append(c)
    return sortie


# ----------------------------------------------------------------------------
# 1. ARITHMÉTIQUE (corrigé : une seule bonne réponse garantie)
# ----------------------------------------------------------------------------
def gen_arithmetique(fd):
    v = random.choice(["div", "premier", "euclide", "crit"])
    if v == "div":
        d = random.choice([2, 3, 4, 5, 6, 8, 9, 11])
        base = random.randint(20 * fd, 400 * fd)
        vrai = base - base % d
        if vrai == 0:
            vrai = d
        faux = set()
        while len(faux) < 3:
            c = vrai + random.randint(1, 60) * random.choice([-1, 1])
            if c > 0 and c % d != 0:
                faux.add(c)
        exp = M(f"{vrai} = {d} \\times {vrai // d}") + f" : {vrai} est un multiple de {d}."
        return (f"Lequel de ces nombres est divisible par {M(d)} ?", M(vrai), [M(f) for f in faux], exp)
    if v == "premier":
        premiers = [p for p in range(2, 60 * fd + 40) if all(p % i for i in range(2, int(p ** .5) + 1))]
        if random.random() < .5:
            n = random.choice(premiers[-15:])
            ok = True
        else:
            n = random.choice([p * q for p in (3, 7, 11, 13) for q in (3, 7, 11, 17, 19) if p != q] + [91, 119, 143, 221])
            ok = False
        if ok:
            exp = f"Aucun nombre premier {M('@leq @sqrt{' + str(n) + '}')} ne divise {M(n)} : il est premier."
        else:
            f = next(i for i in range(2, n) if n % i == 0)
            exp = M(f"{n} = {f} \\times {n // f}") + " : il admet d'autres diviseurs que 1 et lui-même."
        return (f"Le nombre {M(n)} est-il premier ?", "Oui" if ok else "Non", ["Non" if ok else "Oui"], exp)
    if v == "euclide":
        d = random.randint(7, 30 * fd)
        q = random.randint(3, 40)
        r = random.randint(1, d - 1)
        n = d * q + r
        cands = [str(r), str(q), str(d - r), str(r + 1 if r + 1 < d else r - 1)]
        exp = M(f"{n} = {d} \\times {q} + {r}") + f" avec {M(f'0 @leq {r} < {d}')}."
        return (f"Quel est le reste de la division euclidienne de {M(n)} par {M(d)} ?", M(r),
                [M(c) for c in _autres(str(r), cands)], exp)
    # critères de divisibilité par 3 / 9
    d = random.choice([3, 9])
    n = random.randint(100, 9999)
    somme = sum(map(int, str(n)))
    ok = somme % d == 0
    exp = f"Somme des chiffres : {M(str(somme))}. " + ("Elle" if ok else "Elle ne") + f" est {'' if ok else 'pas '}multiple de {d}."
    return (f"Le nombre {M(n)} est-il divisible par {M(d)} ?", "Oui" if ok else "Non", ["Non" if ok else "Oui"], exp)


# ----------------------------------------------------------------------------
# 2. FRACTION (corrigé : fraction vraiment irréductible, décimaux exacts)
# ----------------------------------------------------------------------------
def gen_fraction(fd):
    v = random.choice(["simplifier", "somme", "produit", "decimal", "comparer"])
    if v == "simplifier":
        while True:
            n, d = random.randint(1, 12 * fd), random.randint(2, 12 * fd)
            if math.gcd(n, d) == 1 and n != d:
                break
        k = random.randint(2, 9)
        correct = fr(Fraction(n, d))
        cands = [fr(Fraction(n * 2, d * 2)) if False else f"\\frac{{{n * 2}}}{{{d * 2}}}",
                 f"\\frac{{{n + 1}}}{{{d}}}", f"\\frac{{{n}}}{{{d + 1}}}", f"\\frac{{{d}}}{{{n}}}"]
        exp = M("@text{PGCD}(%d@,;@,%d) = %d" % (n * k, d * k, k)) + " donc " + \
              M("@frac{%d}{%d} = @frac{%d}{%d}" % (n * k, d * k, n, d))
        return (f"Simplifier au maximum la fraction {M(f'@frac{{{n * k}}}{{{d * k}}}')}.", M(correct),
                [M(c) for c in _autres(correct, cands)], exp)
    if v in ("somme", "produit"):
        a, b = Fraction(random.randint(1, 9), random.randint(2, 9)), Fraction(random.randint(1, 9), random.randint(2, 9))
        if v == "somme":
            res = a + b
            op, sym = r"+", "somme"
            fausse = Fraction(a.numerator + b.numerator, a.denominator + b.denominator)
            exp = M(f"{fr(a)} + {fr(b)} = {fr(res)}") + " (mise au même dénominateur)."
        else:
            res = a * b
            op, sym = r"\times", "produit"
            fausse = Fraction(a.numerator * b.numerator, a.denominator + b.denominator)
            exp = M(f"{fr(a)} \\times {fr(b)} = {fr(res)}") + " (on multiplie numérateurs et dénominateurs)."
        cands = [fr(fausse), fr(res + Fraction(1, res.denominator)), fr(abs(a - b) if a != b else res + 1),
                 fr(Fraction(res.denominator, res.numerator))]
        return (f"Calculer : {M(f'{fr(a)} {op} {fr(b)}')} (résultat sous forme de fraction simplifiée).", M(fr(res)),
                [M(c) for c in _autres(fr(res), cands)], exp)
    if v == "decimal":
        d = random.choice([2, 4, 5, 8, 10, 20, 25])
        n = random.randint(1, 3 * d)
        val = Fraction(n, d)
        correct = nb(float(val))
        cands = [nb(float(Fraction(d, n))) if n else "0", nb(float(val) * 10), nb(float(val) / 10), f"{n}{{,}}{d}"]
        exp = M(f"\\frac{{{n}}}{{{d}}} = {correct}")
        return (f"Donner l'écriture décimale de {M(f'@frac{{{n}}}{{{d}}}')}.", M(correct),
                [M(c) for c in _autres(correct, cands)], exp)
    # comparer
    while True:
        a, b = Fraction(random.randint(1, 9), random.randint(2, 9)), Fraction(random.randint(1, 9), random.randint(2, 9))
        if a != b and a.denominator > 1 and b.denominator > 1:
            break
    plus = a if a > b else b
    moins = b if plus == a else a
    return (f"Quelle est la plus grande des deux fractions {M(fr(a))} et {M(fr(b))} ?", M(fr(plus)),
            [M(fr(moins)), "Elles sont égales", "On ne peut pas les comparer"],
            f"En réduisant au même dénominateur : {M(fr(plus))} {M('>')} {M(fr(moins))}.")


# ----------------------------------------------------------------------------
# 3. PUISSANCE (corrigé : exposants propres, tout en LaTeX)
# ----------------------------------------------------------------------------
def gen_puissance(fd):
    v = random.choice(["produit", "quotient", "puissance", "zero_neg", "dix"])
    a = random.choice([2, 3, 5, 7, 10])
    m, n = random.randint(2, 9), random.randint(2, 6)
    if v == "produit":
        c = f"{a}^{{{m + n}}}"
        cands = [f"{a}^{{{m * n}}}", f"{a * a}^{{{m + n}}}", f"{a}^{{{abs(m - n)}}}", f"{a}^{{{m + n + 1}}}"]
        return (f"Écrire sous la forme {M(f'{a}^{{p}}')} : {M(f'{a}^{{{m}}} @times {a}^{{{n}}}')}.", M(c),
                [M(x) for x in _autres(c, cands)], M(f"a^m \\times a^n = a^{{m+n}} \\Rightarrow {c}"))
    if v == "quotient":
        m = n + random.randint(1, 6)
        c = f"{a}^{{{m - n}}}"
        cands = [f"{a}^{{{m + n}}}", f"{a}^{{{m // n if m % n == 0 else m * n}}}", f"1^{{{m - n}}}", f"{a}^{{{m - n + 1}}}"]
        return (f"Simplifier : {M(f'@frac{{{a}^{{{m}}}}}{{{a}^{{{n}}}}}')}.", M(c), [M(x) for x in _autres(c, cands)],
                M(f"\\frac{{a^m}}{{a^n}} = a^{{m-n}} = {c}"))
    if v == "puissance":
        c = f"{a}^{{{m * n}}}"
        cands = [f"{a}^{{{m + n}}}", f"{a}^{{{m ** 2 if m > 1 else 2}}}", f"{a * n}^{{{m}}}", f"{a}^{{{m * n + 1}}}"]
        return (f"Écrire sous la forme {M(f'{a}^{{p}}')} : {M(f'@left({a}^{{{m}}}@right)^{{{n}}}')}.", M(c),
                [M(x) for x in _autres(c, cands)], M(f"(a^m)^n = a^{{mn}} = {c}"))
    if v == "zero_neg":
        k = random.randint(1, 4)
        if random.random() < .5:
            return (f"Que vaut {M(f'{a}^{{0}}')} ?", M("1"), [M("0"), M(str(a)), M("-1")], M("a^{0} = 1 \\ (a \\neq 0)"))
        c = f"\\frac{{1}}{{{a ** k}}}"
        cands = [f"-{a ** k}", f"\\frac{{1}}{{{a * k}}}", f"{a ** k}", f"-\\frac{{1}}{{{a ** k}}}"]
        return (f"Écrire {M(f'{a}^{{-{k}}}')} sous forme de fraction.", M(c), [M(x) for x in _autres(c, cands)],
                M(f"a^{{-n}} = \\frac{{1}}{{a^{{n}}}} \\Rightarrow {a}^{{-{k}}} = \\frac{{1}}{{{a}^{{{k}}}}} = {c}"))
    k = random.randint(2, 7)
    x = random.randint(11, 99)
    c = f"{x / 10:g}".replace(".", "{,}") + f" \\times 10^{{{k + 1}}}"
    return (f"Écrire en notation scientifique : {M(f'{x}@times 10^{{{k}}}')}.", M(c),
            [M(f"{x / 10:g}".replace(".", "{,}") + f" \\times 10^{{{k}}}"), M(f"{x * 10} \\times 10^{{{k - 1}}}"),
             M(f"{x / 100:g}".replace(".", "{,}") + f" \\times 10^{{{k + 1}}}")],
            M(f"{x} = {x / 10:g}".replace(".", "{,}") + f" \\times 10 \\Rightarrow {c}"))


# ----------------------------------------------------------------------------
# 4. PGCD / PPCM
# ----------------------------------------------------------------------------
def gen_pgcd(fd):
    g = random.randint(2, 12)
    a, b = g * random.randint(2, 9), g * random.randint(2, 9)
    while a == b:
        b = g * random.randint(2, 9)
    d = math.gcd(a, b)
    m = a * b // d
    if random.random() < .5:
        c = str(d)
        cands = [str(m), str(abs(a - b) or 1), str(d * 2), str(max(1, d - 1))]
        exp = M(f"PGCD({a}\\,;\\,{b}) = {d}".replace("PGCD", r"\text{PGCD}"))
        return (f"Calculer {M(f'@text{{PGCD}}({a}@,;@,{b})')}.", M(c), [M(x) for x in _autres(c, cands)], exp)
    c = str(m)
    cands = [str(a * b) if a * b != m else str(m * 2), str(d), str(a + b), str(m + d)]
    exp = M(f"\\text{{PPCM}} = \\frac{{{a} \\times {b}}}{{\\text{{PGCD}}}} = \\frac{{{a * b}}}{{{d}}} = {m}")
    return (f"Calculer {M(f'@text{{PPCM}}({a}@,;@,{b})')}.", M(c), [M(x) for x in _autres(c, cands)], exp)


# ----------------------------------------------------------------------------
# 5. NOTION D'ÉQUATION
# ----------------------------------------------------------------------------
def gen_equation(fd):
    x = random.randint(-9, 12)
    a = random.choice([2, 3, 4, 5, 6, 7])
    b = random.randint(-15, 15)
    c = a * x + b
    eq = f"{poly(a, b)} = {c}"
    cands = [str(x + 1), str(x - 1), str(-x if x else 7), str(Fraction(c, a).__str__() if (c % a) else c // a + b), str(c - b)]
    cands = [s for s in cands if "/" not in s]
    exp = M(f"{poly(a, b)} = {c} \\Rightarrow {a}x = {c - b} \\Rightarrow x = {x}")
    return (f"Résoudre dans {M(chr(92) + 'mathbb{R}')} : {M(eq)}.", M(f"x = {x}"),
            [M(f"x = {s}") for s in _autres(str(x), cands)], exp)


# ----------------------------------------------------------------------------
# 6. ÉQUATIONS ET INÉQUATIONS / INTERVALLES
# ----------------------------------------------------------------------------
def gen_inequation(fd):
    v = random.choice(["ineq", "ineq", "carre", "intervalle"])
    if v == "ineq":
        a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        x0 = random.randint(-8, 8)
        b = random.randint(-10, 10)
        c = a * x0 + b
        sym = random.choice(["<", r"\leq", ">", r"\geq"])
        strict = sym in ("<", ">")
        # sens de la solution
        sens = "<" if (sym in ("<", r"\leq")) == (a > 0) else ">"
        sol = intervalle(x0, sens, strict)
        mauvais_sens = ">" if sens == "<" else "<"
        cands = [intervalle(x0, mauvais_sens, strict), intervalle(x0, sens, not strict),
                 intervalle(-x0 if x0 else 1, sens, strict), intervalle(c - b, sens, strict)]
        exp = M(f"{poly(a, b)} {sym} {c} \\Rightarrow {a}x {sym} {c - b}") + (
            " ; on divise par " + M(str(a)) + (" (négatif : le sens change)." if a < 0 else "."))
        return (f"Résoudre {M(f'{poly(a, b)} {sym} {c}')} : donner l'ensemble des solutions.", M(sol),
                [M(x) for x in _autres(sol, cands)], exp)
    if v == "carre":
        k = random.randint(2, 14)
        c = f"\\{{-{k}\\,;\\,{k}\\}}"
        cands = [f"\\{{{k}\\}}", f"\\{{{k * k}\\}}", f"\\{{-{k * k}\\,;\\,{k * k}\\}}", r"\varnothing"]
        return (f"Résoudre dans {M(chr(92) + 'mathbb{R}')} : {M(f'x^{{2}} = {k * k}')}.", M(c),
                [M(x) for x in cands], M(f"x^{{2}} = {k * k} \\Rightarrow x = \\sqrt{{{k * k}}} \\ \\text{{ou}} \\ x = -\\sqrt{{{k * k}}}"))
    a, b = random.randint(-9, 2), 0
    b = a + random.randint(2, 9)
    ferm_g, ferm_d = random.choice([("[", "]"), ("]", "["), ("[", "["), ("]", "]")])
    sg = r"\leq" if ferm_g == "[" else "<"
    sd = r"\leq" if ferm_d == "]" else "<"
    ineq = f"{a} {sg} x {sd} {b}"
    c = f"\\left{ferm_g}{a}\\,;\\,{b}\\right{ferm_d}"
    cands = [f"\\left{'[' if ferm_g == ']' else ']'}{a}\\,;\\,{b}\\right{ferm_d}",
             f"\\left{ferm_g}{a}\\,;\\,{b}\\right{'[' if ferm_d == ']' else ']'}",
             f"\\left{ferm_g}{b}\\,;\\,{a}\\right{ferm_d}", f"\\left]-\\infty\\,;\\,{b}\\right]"]
    return (f"Écrire sous forme d'intervalle l'ensemble des réels {M('x')} tels que {M(ineq)}.", M(c),
            [M(x) for x in _autres(c, cands)], "Un crochet tourné vers l'intérieur de l'intervalle signifie que la borne est incluse.")


# ----------------------------------------------------------------------------
# 7. REPÉRAGE / REPÈRE
# ----------------------------------------------------------------------------
def gen_reperage(fd):
    v = random.choice(["milieu", "distance", "quadrant", "vecteur"])
    xa, ya, xb, yb = [random.randint(-8, 8) for _ in range(4)]
    if v == "milieu":
        if (xa + xb) % 2:
            xb += 1
        if (ya + yb) % 2:
            yb += 1
        c = f"({(xa + xb) // 2}\\,;\\,{(ya + yb) // 2})"
        cands = [f"({(xb - xa) // 2}\\,;\\,{(yb - ya) // 2})", f"({xa + xb}\\,;\\,{ya + yb})",
                 f"({(ya + yb) // 2}\\,;\\,{(xa + xb) // 2})", f"({(xa + xb) // 2 + 1}\\,;\\,{(ya + yb) // 2})"]
        exp = M(f"I\\left(\\frac{{x_A + x_B}}{{2}}\\,;\\,\\frac{{y_A + y_B}}{{2}}\\right)") + " = " + M(f"I{c}")
        return (f"Dans un repère, on donne {M(f'A({xa}@,;@,{ya})')} et {M(f'B({xb}@,;@,{yb})')}. Quelles sont les coordonnées du milieu {M('I')} de {M('[AB]')} ?",
                M(c), [M(x) for x in _autres(c, cands)], exp)
    if v == "distance":
        trip = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)])
        dx, dy, d = trip
        xb, yb = xa + dx, ya + dy
        c = str(d)
        cands = [str(dx + dy), f"\\sqrt{{{dx + dy}}}", str(d * d), str(abs(dx - dy))]
        exp = M(f"AB = \\sqrt{{({xb}-({xa}))^{{2}} + ({yb}-({ya}))^{{2}}}} = \\sqrt{{{dx ** 2} + {dy ** 2}}} = {d}")
        return (f"Dans un repère orthonormé, {M(f'A({xa}@,;@,{ya})')} et {M(f'B({xb}@,;@,{yb})')}. Calculer la distance {M('AB')}.",
                M(c), [M(x) for x in _autres(c, cands)], exp)
    if v == "quadrant":
        x = random.choice([-1, 1]) * random.randint(1, 9)
        y = random.choice([-1, 1]) * random.randint(1, 9)
        noms = {(1, 1): "premier quadrant", (-1, 1): "deuxième quadrant", (-1, -1): "troisième quadrant",
                (1, -1): "quatrième quadrant"}
        c = noms[(1 if x > 0 else -1, 1 if y > 0 else -1)]
        return (f"Dans quel quadrant se trouve le point {M(f'P({x}@,;@,{y})')} ?", c, _autres(c, list(noms.values())),
                f"Abscisse {'positive' if x > 0 else 'négative'} et ordonnée {'positive' if y > 0 else 'négative'}.")
    c = f"({xb - xa}\\,;\\,{yb - ya})"
    cands = [f"({xa - xb}\\,;\\,{ya - yb})", f"({xa + xb}\\,;\\,{ya + yb})", f"({yb - ya}\\,;\\,{xb - xa})",
             f"({xb - xa}\\,;\\,{ya + yb})"]
    return (f"On donne {M(f'A({xa}@,;@,{ya})')} et {M(f'B({xb}@,;@,{yb})')}. Coordonnées du vecteur {M(chr(92) + 'overrightarrow{AB}')} ?",
            M(c), [M(x) for x in _autres(c, cands)], M(f"\\overrightarrow{{AB}}(x_B - x_A\\,;\\,y_B - y_A) = {c}"))


# ----------------------------------------------------------------------------
# 8. POLYGONE
# ----------------------------------------------------------------------------
NOMS_POLY = {3: "triangle", 4: "quadrilatère", 5: "pentagone", 6: "hexagone", 7: "heptagone", 8: "octogone",
             9: " ennéagone", 10: "décagone", 12: "dodécagone"}


def gen_polygone(fd):
    v = random.choice(["somme", "diagonales", "nom", "perimetre"])
    n = random.choice(list(NOMS_POLY))
    if v == "somme":
        s = (n - 2) * 180
        c = f"{s}^{{\\circ}}"
        cands = [f"{(n - 1) * 180}^{{\\circ}}", f"{n * 180}^{{\\circ}}", f"{(n - 2) * 90}^{{\\circ}}", f"{360}^{{\\circ}}"]
        return (f"Quelle est la somme des angles intérieurs d'un {NOMS_POLY[n]} convexe ({M(f'{n}')} côtés) ?", M(c),
                [M(x) for x in _autres(c, cands)], M(f"S = (n-2) \\times 180^{{\\circ}} = {n - 2} \\times 180^{{\\circ}} = {c}"))
    if v == "diagonales":
        d = n * (n - 3) // 2
        cands = [n * (n - 1) // 2, n * (n - 2) // 2, n * n // 2, n - 3]
        return (f"Combien de diagonales possède un {NOMS_POLY[n]} ?", M(str(d)), [M(str(x)) for x in _autres(str(d), map(str, cands))],
                M(f"\\frac{{n(n-3)}}{{2}} = \\frac{{{n} \\times {n - 3}}}{{2}} = {d}"))
    if v == "nom":
        c = NOMS_POLY[n]
        return (f"Comment s'appelle un polygone à {M(f'{n}')} côtés ?", c, _autres(c, random.sample(list(NOMS_POLY.values()), 5))[:3],
                f"Un polygone à {n} côtés est un {c}.")
    cote = random.randint(2, 15)
    nn = random.choice([3, 4, 5, 6, 8])
    p = cote * nn
    cands = [cote + nn, cote * cote, p + cote, cote * (nn - 1)]
    return (f"Un polygone régulier à {M(str(nn))} côtés a un côté de {M(f'{cote}@text{{ cm}}')}. Quel est son périmètre ?",
            M(f"{p}\\text{{ cm}}"), [M(f"{x}\\text{{ cm}}") for x in _autres(p, cands)],
            M(f"P = {nn} \\times {cote} = {p}\\text{{ cm}}"))


# ----------------------------------------------------------------------------
# 9. POLYGONE RÉGULIER
# ----------------------------------------------------------------------------
def gen_polygone_regulier(fd):
    n = random.choice([3, 4, 5, 6, 8, 9, 10, 12])
    v = random.choice(["central", "interieur", "exterieur"])
    central = Fraction(360, n)
    inter = 180 - central
    f = lambda q: (str(int(q)) if Fraction(q).denominator == 1 else nb(float(q))) + "^{\\circ}"
    if v == "central":
        c = f(central)
        cands = [f(inter), f(Fraction(180, n)), f(Fraction(360, n + 1)), f(central * 2)]
        return (f"Quel est l'angle au centre d'un polygone régulier à {M(str(n))} côtés ?", M(c),
                [M(x) for x in _autres(c, cands)], M(f"\\frac{{360^{{\\circ}}}}{{n}} = \\frac{{360^{{\\circ}}}}{{{n}}} = {c}"))
    if v == "interieur":
        c = f(inter)
        cands = [f(central), f(180 - Fraction(180, n)), f((n - 2) * 180), f(inter + 10)]
        return (f"Quelle est la mesure d'un angle intérieur d'un polygone régulier à {M(str(n))} côtés ?", M(c),
                [M(x) for x in _autres(c, cands)], M(f"\\frac{{(n-2) \\times 180^{{\\circ}}}}{{n}} = {c}"))
    c = f(central)
    cands = [f(inter), f(central / 2), f(180), f(Fraction(180, n))]
    return (f"Quelle est la mesure d'un angle extérieur d'un polygone régulier à {M(str(n))} côtés ?", M(c),
            [M(x) for x in _autres(c, cands)], "La somme des angles extérieurs d'un polygone convexe vaut " + M("360^{\\circ}") + ".")


# ----------------------------------------------------------------------------
# 10. VECTEUR ET HOMOTHÉTIE
# ----------------------------------------------------------------------------
def gen_homothetie(fd):
    v = random.choice(["image", "longueur", "aire", "vecteur", "chasles"])
    if v == "image":
        k = random.choice([2, 3, -1, -2, 4])
        x, y = random.randint(-6, 6), random.randint(-6, 6)
        while x == 0 and y == 0:
            x = random.randint(-6, 6)
        c = f"({k * x}\\,;\\,{k * y})"
        cands = [f"({x + k}\\,;\\,{y + k})", f"({x * k}\\,;\\,{y})", f"({x // k if k and x % k == 0 else x}\\,;\\,{y})",
                 f"({-k * x}\\,;\\,{-k * y})"]
        return (f"Dans un repère d'origine {M('O')}, l'homothétie {M(f'h')} de centre {M('O')} et de rapport {M(str(k))} envoie {M(f'A({x}@,;@,{y})')} sur {M(chr(39).join(['A', '']))}. Coordonnées de {M(chr(39).join(['A', '']))} ?",
                M(c), [M(s) for s in _autres(c, cands)], M(f"\\overrightarrow{{OA'}} = {k}\\,\\overrightarrow{{OA}} \\Rightarrow A'{c}"))
    if v == "longueur":
        k = random.choice([2, 3, -2, -3, Fraction(1, 2), Fraction(3, 2)])
        L = random.choice([2, 4, 6, 8, 10, 12])
        res = abs(Fraction(k) * L)
        c = nb(res) + "\\text{ cm}"
        cands = [nb(Fraction(k) * L) + "\\text{ cm}", nb(res * abs(Fraction(k))) + "\\text{ cm}", nb(L + abs(Fraction(k))) + "\\text{ cm}",
                 nb(L / abs(Fraction(k)) if k else L) + "\\text{ cm}"]
        return (f"Une homothétie de rapport {M(fr(Fraction(k)))} transforme un segment de {M(f'{L}@text{{ cm}}')}. Quelle est la longueur de son image ?",
                M(c), [M(x) for x in _autres(c, cands)], M(f"A'B' = |k| \\times AB = {fr(abs(Fraction(k)))} \\times {L} = {c}"))
    if v == "aire":
        k = random.choice([2, 3, 4, 5])
        A = random.choice([3, 5, 6, 10, 12])
        res = k * k * A
        c = f"{res}\\text{{ cm}}^{{2}}"
        cands = [f"{k * A}\\text{{ cm}}^{{2}}", f"{k ** 3 * A}\\text{{ cm}}^{{2}}", f"{A + k}\\text{{ cm}}^{{2}}", f"{A * 2 * k}\\text{{ cm}}^{{2}}"]
        return (f"Une figure d'aire {M(f'{A}@text{{ cm}}^{{2}}')} subit une homothétie de rapport {M(str(k))}. Quelle est l'aire de l'image ?",
                M(c), [M(x) for x in _autres(c, cands)], M(f"\\mathcal{{A}}' = k^{{2}}\\,\\mathcal{{A}} = {k}^{{2}} \\times {A} = {res}"))
    if v == "vecteur":
        a, b, c1, d = [random.randint(-6, 6) for _ in range(4)]
        while a == 0 and b == 0:
            a = random.randint(-6, 6)
        k = random.choice([2, 3, -1, -2])
        c = f"({k * a}\\,;\\,{k * b})"
        cands = [f"({a + k}\\,;\\,{b + k})", f"({k * a}\\,;\\,{b})", f"({a * b}\\,;\\,{k})", f"({-k * a}\\,;\\,{-k * b})"]
        return (f"Soit {M(f'@vec{{u}}({a}@,;@,{b})')}. Quelles sont les coordonnées de {M(f'{k}@vec{{u}}')} ?", M(c),
                [M(x) for x in _autres(c, cands)], M(f"k\\vec{{u}}(ka\\,;\\,kb) = {c}"))
    c = r"\overrightarrow{AC}"
    cands = [r"\overrightarrow{CA}", r"\overrightarrow{BC}", r"\overrightarrow{AB} - \overrightarrow{BC}", r"\overrightarrow{0}"]
    return (f"Simplifier {M('@overrightarrow{AB} + @overrightarrow{BC}')}.", M(c), [M(x) for x in cands], "Relation de Chasles : " + M(r"\overrightarrow{AB} + \overrightarrow{BC} = \overrightarrow{AC}") + ".")


# ----------------------------------------------------------------------------
# 11. ANALYSE 1 (limites, suites, dérivées)
# ----------------------------------------------------------------------------
def gen_analyse1(fd):
    v = random.choice(["derivee", "limite_inf", "suite_arith", "suite_geo", "limite_rat"])
    if v == "derivee":
        a, b, c = random.randint(1, 6), random.randint(-8, 8), random.randint(-8, 8)
        n = random.choice([2, 3, 4])
        f = f"{a}x^{{{n}}}" + pm(b, "x") + pm(c, "")
        d = f"{a * n}x^{{{n - 1}}}" if n > 2 else f"{a * n}x"
        d += pm(b, "")
        cands = [f"{a}x^{{{n - 1}}}" + pm(b, ""), f"{a * n}x^{{{n}}}" + pm(b, "") ,
                 f"{a * n}x^{{{n - 1}}}" + pm(b, "x") + pm(c, "") if n > 2 else f"{a * n}x" + pm(b, "x"),
                 f"{a * n}x^{{{n - 1}}}" + pm(-b, "")]
        return (f"Calculer la dérivée de {M(f'f(x) = {f}')}.", M(f"f'(x) = {d}"),
                [M(f"f'(x) = {x}") for x in _autres(d, cands)], M(f"(x^{{n}})' = n\\,x^{{n-1}}"))
    if v == "limite_inf":
        a = random.randint(2, 9)
        res = random.choice([("+\\infty", a > 0)])
        n = random.choice([2, 3])
        c = "+\\infty" if a > 0 else "-\\infty"
        return (f"Déterminer {M(f'@lim_{{x @to +@infty}} {cf(a)}x^{{{n}}}')}.", M(c), [M(x) for x in _autres(c, ["0", "+\\infty", "-\\infty", str(a)])][:3],
                "Un monôme de degré " + M(str(n)) + " tend vers l'infini avec le signe de son coefficient.")
    if v == "limite_rat":
        a, b = random.randint(1, 9), random.randint(1, 9)
        c = fr(Fraction(a, b))
        cands = ["0", "+\\infty", fr(Fraction(b, a)), "1"]
        return (f"Déterminer {M(f'@lim_{{x @to +@infty}} @frac{{{a}x + 3}}{{{b}x - 1}}')}.", M(c), [M(x) for x in _autres(c, cands)],
                "On factorise par " + M("x") + " : le quotient des coefficients dominants donne la limite.")
    if v == "suite_arith":
        u0, r, n = random.randint(-5, 10), random.randint(2, 9), random.randint(5, 20)
        c = u0 + n * r
        cands = [u0 + (n - 1) * r, u0 + (n + 1) * r, u0 * r ** n if abs(u0 * r ** n) < 10 ** 6 else n * r, u0 + r * n * 2]
        return (f"{M('(u_n)')} est arithmétique de premier terme {M(f'u_0 = {u0}')} et de raison {M(f'r = {r}')}. Calculer {M(f'u_{{{n}}}')}.",
                M(str(c)), [M(str(x)) for x in _autres(c, cands)], M(f"u_n = u_0 + n\\,r = {u0} + {n} \\times {r} = {c}"))
    u0, q, n = random.randint(1, 4), random.choice([2, 3]), random.randint(3, 7)
    c = u0 * q ** n
    cands = [u0 * q ** (n - 1), u0 * q ** (n + 1), u0 + n * q, (u0 * q) ** n if (u0 * q) ** n < 10 ** 7 else n * q]
    return (f"{M('(u_n)')} est géométrique de premier terme {M(f'u_0 = {u0}')} et de raison {M(f'q = {q}')}. Calculer {M(f'u_{{{n}}}')}.",
            M(str(c)), [M(str(x)) for x in _autres(c, cands)], M(f"u_n = u_0\\,q^{{n}} = {u0} \\times {q}^{{{n}}} = {c}"))


# ----------------------------------------------------------------------------
# 12. ANALYSE 2 (primitives, intégrales)
# ----------------------------------------------------------------------------
def gen_analyse2(fd):
    v = random.choice(["primitive", "integrale", "integrale", "valeur_moy"])
    if v == "primitive":
        a, b = random.choice([2, 4, 6, 8]), random.randint(1, 9)
        n = random.choice([2, 3])
        f = f"{a * n}x^{{{n - 1}}}" if n > 2 else f"{a * n}x"
        F = f"{a}x^{{{n}}}" + pm(b, "")
        F = f"{a}x^{{{n}}} + C"
        cands = [f"{a * n}x^{{{n}}} + C", f"\\frac{{{a}}}{{{n}}}x^{{{n}}} + C", f"{a}x^{{{n - 1}}} + C", f"{a * n * n}x^{{{n + 1}}} + C"]
        return (f"Donner une primitive de {M(f'f(x) = {f}')}.", M(F), [M(x) for x in _autres(F, cands)],
                M(f"\\int x^{{n}}\\,dx = \\frac{{x^{{n+1}}}}{{n+1}} + C"))
    if v == "integrale":
        a, n = random.randint(1, 6), random.choice([1, 2, 3])
        b = random.randint(1, 4)
        val = Fraction(a * b ** (n + 1), n + 1)
        c = fr(val)
        cands = [fr(Fraction(a * b ** n, 1)), fr(Fraction(a * b ** (n + 1), 1) * (n + 1)), fr(Fraction(b ** (n + 1), n + 1)), fr(val + a)]
        return (f"Calculer {M(f'@int_{{0}}^{{{b}}} {cf(a)}x^{{{n}}}@,dx')}.", M(c), [M(x) for x in _autres(c, cands)],
                M(f"\\left[\\frac{{{a}x^{{{n + 1}}}}}{{{n + 1}}}\\right]_{{0}}^{{{b}}} = {c}"))
    if v == "valeur_moy":
        k = random.randint(1, 5)
        a2 = random.randint(2, 6)
        res = Fraction(a2 ** 2, 2) * k
        return (f"Calculer {M(f'@int_{{0}}^{{{a2}}} {cf(k)}x@,dx')}.", M(fr(res)),
                [M(x) for x in _autres(fr(res), [fr(Fraction(k * a2)), fr(Fraction(k * a2 * a2)), fr(res + k)])],
                M(f"\\left[\\frac{{{k}x^{{2}}}}{{2}}\\right]_{{0}}^{{{a2}}} = {fr(res)}"))
    return gen_analyse2(fd)


# ----------------------------------------------------------------------------
# Registre : chapitre (toutes graphies du programme) -> générateur
# ----------------------------------------------------------------------------
REGISTRE = {}


def _reg(fn, *noms):
    for n in noms:
        REGISTRE[n] = fn


_reg(gen_arithmetique, "Arithmétiques", "Arithmétique")
_reg(gen_fraction, "Fraction")
_reg(gen_puissance, "Puissance")
_reg(gen_pgcd, "PGCD et PPCM", "PGDC et PPCM")
_reg(gen_equation, "Notion d’équation", "Notion d'équation")
_reg(gen_inequation, "Equation et Inéquation", "Equation, Intervalle et Inéquation", "Équation et Inéquation")
_reg(gen_reperage, "Repérage sur un quadrillage", "Repérage", "Repère")
_reg(gen_polygone, "Polygone")
_reg(gen_polygone_regulier, "Polygone régulier")
_reg(gen_homothetie, "Vecteur et Homothétie")
_reg(gen_analyse1, "Analyse 1", "aAnalyse 1")
_reg(gen_analyse2, "Analyse 2")
