# -*- coding: utf-8 -*-
"""
latex_utils.py
==============
Convertit n'importe quel texte de quiz (prose française + maths écrites en
Unicode ou en ASCII : "x², √x, pi/2, +inf, a/b, x_1 ...") en texte où chaque
expression mathématique est entourée de $...$ en LaTeX propre.

 - Si le texte contient déjà des $...$ il est considéré comme déjà en LaTeX.
 - latex_vers_texte() fait l'inverse (version lisible sans KaTeX, pour PC/secours).
"""
import re

# ----------------------------------------------------------------------------
# Tables de conversion
# ----------------------------------------------------------------------------
UNICODE_TEX = {
    "×": r"\times ", "·": r"\cdot ", "÷": r"\div ", "±": r"\pm ", "∓": r"\mp ",
    "≤": r"\leq ", "≥": r"\geq ", "≠": r"\neq ", "≈": r"\approx ", "≡": r"\equiv ",
    "∞": r"\infty ", "→": r"\to ", "⟶": r"\to ", "↦": r"\mapsto ", "⇒": r"\Rightarrow ",
    "⇔": r"\Leftrightarrow ", "⟹": r"\Rightarrow ", "⟺": r"\Leftrightarrow ",
    "∈": r"\in ", "∉": r"\notin ", "⊂": r"\subset ", "⊃": r"\supset ", "⊆": r"\subseteq ",
    "∀": r"\forall ", "∃": r"\exists ", "∩": r"\cap ", "∪": r"\cup ", "∅": r"\emptyset ",
    "∑": r"\sum ", "∏": r"\prod ", "∫": r"\int ", "∂": r"\partial ", "∇": r"\nabla ",
    "∤": r"\nmid ", "∣": r"\mid ", "⊥": r"\perp ", "∥": r"\parallel ", "∠": r"\angle ",
    "°": r"^{\circ}", "′": "'", "∝": r"\propto ", "∘": r"\circ ", "−": "-", "–": "-",
    "ℝ": r"\mathbb{R}", "ℕ": r"\mathbb{N}", "ℤ": r"\mathbb{Z}", "ℚ": r"\mathbb{Q}", "ℂ": r"\mathbb{C}",
    "α": r"\alpha ", "β": r"\beta ", "γ": r"\gamma ", "δ": r"\delta ", "ε": r"\varepsilon ",
    "θ": r"\theta ", "λ": r"\lambda ", "μ": r"\mu ", "π": r"\pi ", "ρ": r"\rho ",
    "σ": r"\sigma ", "τ": r"\tau ", "φ": r"\varphi ", "ω": r"\omega ", "ψ": r"\psi ",
    "Δ": r"\Delta ", "Σ": r"\Sigma ", "Ω": r"\Omega ", "Φ": r"\Phi ", "Γ": r"\Gamma ",
    "Π": r"\Pi ", "Θ": r"\Theta ", "Λ": r"\Lambda ", "ν": r"\nu ", "η": r"\eta ", "κ": r"\kappa ",
    "ℓ": r"\ell ", "⃗": "",
}
SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7",
       "⁸": "8", "⁹": "9", "⁺": "+", "⁻": "-", "ⁿ": "n"}
SUB = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7",
       "₈": "8", "₉": "9", "₊": "+", "₋": "-", "ₙ": "n"}

GREC_ASCII = {"alpha", "beta", "gamma", "delta", "theta", "lambda", "omega", "mu", "phi", "epsilon", "sigma", "rho", "tau", "Delta", "Omega"}
UNITES = "cm|mm|km|dm|kg|ms|Hz|rad|mol|min|N|J|W|V|s|h|m"
FONCTIONS = {"sin", "cos", "tan", "arctan", "arcsin", "arccos", "ln", "log", "exp", "lim",
             "det", "dim", "ker", "Ker", "Im", "rg", "max", "min", "sh", "ch", "th", "cotan"}
MOTS_OPS = {"sqrt", "pi", "inf", "infini"} | GREC_ASCII
SYMBOLES = set("=<>+*/^_√∑∫∏≤≥≠≈≡∞→⇒⇔∈∉⊂⊃∀∃∩∪∅∂∇∤⊥∥∠·×÷±°′∝∘ℝℕℤℚℂ%|") \
    | set(UNICODE_TEX) | set(SUP) | set(SUB)
LETTRES_AMBIGUES = {"a", "à", "y", "A", "I", "l", "L", "O"}
MOTS_FR = {"et", "ou", "de", "du", "la", "le", "les", "un", "une", "des", "si", "est", "en", "au", "aux", "par", "sur", "que", "qui", "ne", "pas", "ce", "se", "sa", "son", "ses", "on", "il", "elle", "ni", "car", "or", "donc", "dans", "pour", "avec", "sans", "sous", "vers", "tel", "tout", "peu", "mon", "ma", "tu"}
MAJ_STOP = {"QUI", "LES", "UNE", "NON", "OUI", "DES", "SUR", "PAR", "EST", "ET", "OU", "SI", "UN", "LE", "LA"}


# ----------------------------------------------------------------------------
# Étape 1 : un fragment mathématique (ASCII/Unicode) -> LaTeX
# ----------------------------------------------------------------------------
def _groupe_equilibre(s, i):
    """s[i] == '(' -> renvoie l'index de la parenthèse fermante correspondante (ou -1)."""
    prof = 0
    for j in range(i, len(s)):
        if s[j] == "(":
            prof += 1
        elif s[j] == ")":
            prof -= 1
            if prof == 0:
                return j
    return -1


def _remplacer_sqrt(s):
    """sqrt(...) et √(...) / √x  ->  \\sqrt{...}"""
    out, i = "", 0
    while i < len(s):
        if s.startswith("sqrt(", i) or (s[i] == "√" and i + 1 < len(s) and s[i + 1] == "("):
            ouv = s.index("(", i)
            fin = _groupe_equilibre(s, ouv)
            if fin != -1:
                out += r"\sqrt{" + _remplacer_sqrt(s[ouv + 1:fin]) + "}"
                i = fin + 1
                continue
        if s[i] == "√" and i + 1 < len(s) and s[i + 1] == "[":
            fin = s.find("]", i + 2)
            if fin != -1:
                out += r"\sqrt{" + _remplacer_sqrt(s[i + 2:fin]) + "}"
                i = fin + 1
                continue
        if s[i] == "√":
            m = re.match(r"\{[^}]*\}|[\w.]+", s[i + 1:])
            if m:
                arg = m.group(0)
                if arg.startswith("{"):
                    arg = arg[1:-1]
                out += r"\sqrt{" + arg + "}"
                i += 1 + m.end()
                continue
            out += r"\sqrt{}"
            i += 1
            continue
        out += s[i]
        i += 1
    return out


OPERANDE_G = r"(?:\([^()]*\)|[-+]?\\[a-zA-Z]+(?:\{[^{}]*\})?|[-+]?[\w.]+(?:'|\^\{[^{}]*\}|\^-?\w+|_\{[^{}]*\}|_\w+)*(?:\([^()]*\))?)"


def _fractions(s):
    """a/b -> \\frac{a}{b} (opérandes simples ou parenthésés)."""
    motif = re.compile(r"(" + OPERANDE_G + r")\s*/\s*(" + OPERANDE_G + r")")
    for _ in range(4):
        def rep(m):
            a, b = m.group(1), m.group(2)
            if a.startswith("(") and a.endswith(")"):
                a = a[1:-1]
            if b.startswith("(") and b.endswith(")"):
                b = b[1:-1]
            return r"\frac{" + a + "}{" + b + "}"
        n = motif.sub(rep, s)
        if n == s:
            break
        s = n
    return s


def _proteger_accolades(s):
    """{a, b} (ensemble) -> \\{a, b\\} ; on laisse intactes les accolades de ^{..} et _{..}."""
    out, pile = [], []
    for i, c in enumerate(s):
        if c == "{":
            garde = i > 0 and s[i - 1] in "^_"
            pile.append(garde)
            out.append("{" if garde else "\x01")
        elif c == "}":
            garde = pile.pop() if pile else False
            out.append("}" if garde else "\x02")
        else:
            out.append(c)
    return "".join(out)


def maths_vers_latex(s):
    """Convertit un fragment mathématique en LaTeX (sans $)."""
    s = s.strip()
    if not s:
        return s
    s = re.sub(r"√\{([^{}]*)\}", r"√(\1)", s)
    s = _proteger_accolades(s)
    # exposants / indices Unicode
    s = re.sub("[" + "".join(SUP) + "]+", lambda m: "^{" + "".join(SUP[c] for c in m.group(0)) + "}", s)
    s = re.sub("[" + "".join(SUB) + "]+", lambda m: "_{" + "".join(SUB[c] for c in m.group(0)) + "}", s)
    s = re.sub(r"\b(?:vec|vect)\(([^()]*)\)", r"\\vec{\1}", s)
    s = re.sub(r"\b([xyzXYZ])([A-Z])\b", r"\1_{\2}", s)
    s = _remplacer_sqrt(s)
    # mots ASCII
    s = re.sub(r"([+-]?)\binf\b", lambda m: (m.group(1) + r"\infty "), s)
    s = re.sub(r"\bpi\b", r"\\pi ", s)
    s = re.sub(r"\b(?:e\^)\(?-?", lambda m: m.group(0), s)
    # ^(...)  ->  ^{...}
    def _exp_par(s):
        out, i = "", 0
        while i < len(s):
            if s[i] == "^" and i + 1 < len(s) and s[i + 1] == "(":
                fin = _groupe_equilibre(s, i + 1)
                if fin != -1:
                    out += "^{" + s[i + 2:fin] + "}"
                    i = fin + 1
                    continue
            out += s[i]
            i += 1
        return out
    s = _exp_par(s)
    s = re.sub(r"\^(-?[A-Za-z0-9.]+)", lambda m: "^{" + m.group(1) + "}" if len(m.group(1)) > 1 else "^" + m.group(1), s)
    s = re.sub(r"_(-?\d{2,}|[A-Za-z]{2,})", lambda m: "_{" + m.group(1) + "}", s)
    # nombres flottants Python : 1e-05, 9.999999999999999e-07, 0.30000000000000004
    def _sci(m):
        mant = float(m.group(1))
        e = int(m.group(2))
        mant = round(mant, 3)
        if mant == int(mant):
            mant = int(mant)
        if mant == 1:
            return "10^{%d}" % e
        return "(%s \\times 10^{%d})" % (mant, e)
    s = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)e([+-]?\d+)(?![\w.])", _sci, s)
    s = re.sub(r"(?<![\w.])(\d+\.\d{5,})", lambda m: ("%.4f" % float(m.group(1))).rstrip("0").rstrip("."), s)
    # vitesses / accélérations : m/s, m/s^2 ...
    s = re.sub(r"\b(km|cm|m|rad)\s*/\s*(s|h)\^\{(\d)\}", lambda m: r"\mathrm{%s\cdot %s^{-%s}}" % (m.group(1), m.group(2), m.group(3)), s)
    s = re.sub(r"\b(km|cm|m|rad)\s*/\s*(s|h)\b", lambda m: r"\mathrm{%s\cdot %s^{-1}}" % (m.group(1), m.group(2)), s)
    s = _fractions(s)
    # décimales : 20.0 -> 20 ; 1.5 / 1,5 -> 1{,}5
    s = re.sub(r"(?<![\w.])(\d+)\.0\b(?!\d)", r"\1", s)
    s = re.sub(r"(?<=\d)[.,](?=\d)", "{,}", s)
    # nombre + unité : 10 m  ->  10\,\mathrm{m}
    s = re.sub(r"(?<=[\d}])\s*(" + UNITES + r")(\^\{[-\d]+\})?(?![A-Za-z\\])",
               lambda m: r"\,\mathrm{" + m.group(1) + (m.group(2) or "") + "}", s)
    # lettres grecques écrites en toutes lettres
    s = re.sub(r"\b(" + "|".join(sorted(GREC_ASCII, key=len, reverse=True)) + r")\b", lambda m: "\\" + m.group(1) + " ", s)
    # symboles unicode -> macros
    s = "".join(UNICODE_TEX.get(c, c) for c in s)
    # fonctions usuelles
    s = re.sub(r"(?<![\\A-Za-z])(" + "|".join(sorted(FONCTIONS, key=len, reverse=True)) + r")(?![A-Za-z])",
               lambda m: "\\" + m.group(1) if m.group(1) not in {"rg", "Ker", "Im", "ker", "sh", "ch", "th", "cotan"}
               else r"\operatorname{" + m.group(1) + "}", s)
    s = re.sub(r"(?<=\d)([+-])$", r"^{\1}", s)
    s = s.replace("%", r"\%")
    s = re.sub(r"\s+", " ", s).strip()
    # lim_{x\to a}
    s = s.replace("\x01", r"\{").replace("\x02", r"\}")
    return s


# ----------------------------------------------------------------------------
# Étape 2 : prose + maths -> texte avec $...$
# ----------------------------------------------------------------------------
_PONCT_FIN = ".,;:?!»\""
_PONCT_DEB = "«\""


def _cle_math(tok):
    """Le jeton ressemble-t-il à des maths ? (ne décide pas des lettres ambiguës)"""
    core = tok.strip(_PONCT_FIN + _PONCT_DEB)
    if not core:
        return False
    if re.fullmatch(r"[nN]°\d*", core) or re.fullmatch(r"_+", core):
        return False
    if any(c.isdigit() for c in core):
        return True
    if any(c in SYMBOLES for c in core):
        return True
    mf = re.fullmatch(r"([A-Za-z]+)'*\(.*\)?'*", core)             # f(x)  f'(x)  ln(x)
    if mf and (len(mf.group(1)) == 1 or mf.group(1) in FONCTIONS):
        return True
    base = core.strip("()[]{}").lstrip("+-")
    if base.lower() in MOTS_OPS or base in FONCTIONS:
        return True
    if re.fullmatch(r"[a-z][A-Z]", base) or re.fullmatch(r"(?:vec|vect)\(.*", base):
        return True
    if re.fullmatch(r"[A-Z]{1,4}'?", base) and base not in MAJ_STOP and len(base) <= 4:
        return True                                               # AB  OA'  ABCD
    if re.fullmatch(r"[A-Za-z]'*", base) and base not in LETTRES_AMBIGUES:
        return True                                               # x  n  f
    if re.fullmatch(r"[\(\[][A-Z][\)\]]", core):                # (D) [A]
        return True
    return False


def _est_ambigu(tok):
    return tok.strip(_PONCT_FIN + _PONCT_DEB + "()[]") in LETTRES_AMBIGUES


def texte_vers_latex(texte):
    """Prose + maths en vrac  ->  prose avec expressions entre $...$.
    Texte déjà en LaTeX (contient $) : renvoyé tel quel."""
    if texte is None:
        return ""
    texte = str(texte)
    if "$" in texte:
        return texte
    lignes = []
    for ligne in texte.split("\n"):
        lignes.append(_ligne_vers_latex(ligne))
    return "\n".join(lignes)


def _ligne_vers_latex(ligne):
    toks = ligne.split(" ")
    n = len(toks)
    est_math = [(_cle_math(t) and not _est_ambigu(t)) for t in toks]
    # lettres ambiguës (a, y, I...) : maths seulement si voisines d'un opérateur/maths
    for i, t in enumerate(toks):
        if _cle_math(t) and _est_ambigu(t):
            gauche = i > 0 and est_math[i - 1] and any(c in SYMBOLES for c in toks[i - 1])
            droite = i + 1 < n and any(c in SYMBOLES for c in toks[i + 1]) and _cle_math(toks[i + 1])
            est_math[i] = gauche or droite
    # "+" / "-" isolés collés à des maths : font partie de l'expression
    for _ in range(3):
        for i, t in enumerate(toks):
            if t in {"-", "+", "–", "−"} and not est_math[i]:
                if (i > 0 and est_math[i - 1]) or (i + 1 < n and est_math[i + 1]):
                    est_math[i] = True
    # mots courts (bx, ab, cd) voisins d'un opérateur pur (+ - = * /) -> maths
    OPS = {"+", "-", "=", "*", "/", "<", ">", "·", "×", "−", "÷", "≤", "≥", "≠", "≈"}
    for i, t in enumerate(toks):
        if not est_math[i] and re.fullmatch(r"[A-Za-z]{1,3}'*", t.strip(_PONCT_FIN)) \
                and t.strip(_PONCT_FIN).lower() not in MOTS_FR:
            g = i > 0 and toks[i - 1] in OPS
            d = i + 1 < n and toks[i + 1] in OPS
            if g or d:
                est_math[i] = True
    # un petit mot "et/ou/de" entre deux maths : reste prose. Fusion des suites math.
    out, i = [], 0
    while i < n:
        if not est_math[i]:
            out.append(toks[i])
            i += 1
            continue
        j = i
        while j + 1 < n and est_math[j + 1]:
            j += 1
        # crochet/parenthèse ouvert dans l'expression : on avale le jeton fermant isolé "]" ")"
        while j + 1 < n and re.fullmatch(r"[\])}]+[.,;:?!]*", toks[j + 1]) and \
                " ".join(toks[i:j + 1]).count("[") > " ".join(toks[i:j + 1]).count("]"):
            j += 1
        run = toks[i:j + 1]
        # ponctuation de tête / de queue sortie du bloc maths
        avant = ""
        while run[0] and run[0][0] in _PONCT_DEB:
            avant += run[0][0]
            run[0] = run[0][1:]
        apres = ""
        while run[-1] and run[-1][-1] in _PONCT_FIN:
            apres = run[-1][-1] + apres
            run[-1] = run[-1][:-1]
        # parenthèses déséquilibrées : on laisse en dehors
        corps = " ".join(run)
        if corps.count("(") != corps.count(")"):
            corps = corps.strip("()")
        if corps.strip():
            out.append(avant + "$" + maths_vers_latex(corps) + "$" + apres)
        else:
            out.append(avant + corps + apres)
        i = j + 1
    return " ".join(out)


# ----------------------------------------------------------------------------
# LaTeX -> texte lisible (boutons / PC / notifications)
# ----------------------------------------------------------------------------
_TEX_VERS_TXT = [
    (r"\\times", "×"), (r"\\cdot", "·"), (r"\\div", "÷"), (r"\\pm", "±"), (r"\\leq", "≤"), (r"\\geq", "≥"),
    (r"\\neq", "≠"), (r"\\approx", "≈"), (r"\\equiv", "≡"), (r"\\infty", "∞"), (r"\\to", "→"),
    (r"\\Rightarrow", "⇒"), (r"\\Leftrightarrow", "⇔"), (r"\\in", "∈"), (r"\\forall", "∀"), (r"\\exists", "∃"),
    (r"\\pi", "π"), (r"\\theta", "θ"), (r"\\alpha", "α"), (r"\\beta", "β"), (r"\\lambda", "λ"),
    (r"\\omega", "ω"), (r"\\Delta", "Δ"), (r"\\varphi", "φ"), (r"\\gamma", "γ"), (r"\\mu", "μ"),
    (r"\\circ", "°"), (r"\\mathbb\{R\}", "ℝ"), (r"\\mathbb\{C\}", "ℂ"), (r"\\mathbb\{N\}", "ℕ"),
    (r"\\mathbb\{Z\}", "ℤ"), (r"\\mathbb\{Q\}", "ℚ"), (r"\\varepsilon", "ε"), (r"\\sigma", "σ"),
    (r"\\left", ""), (r"\\right", ""), (r"\\,", " "), (r"\\;", " "), (r"\\!", ""), (r"\\%", "%"),
    (r"\\cup", "∪"), (r"\\cap", "∩"), (r"\\emptyset", "∅"), (r"\\perp", "⊥"), (r"\\parallel", "∥"),
    (r"\\int", "∫"), (r"\\sum", "Σ"), (r"\\partial", "∂"), (r"\\vec\{([^{}]*)\}", r"\1⃗"),
    (r"\\overrightarrow\{([^{}]*)\}", r"\1⃗"), (r"\\widehat\{([^{}]*)\}", r"\1̂"),
    (r"\\(sin|cos|tan|ln|log|exp|lim|arctan|det|dim)", r"\1"), (r"\\operatorname\{([^{}]*)\}", r"\1"),
    (r"\\text\{([^{}]*)\}", r"\1"), (r"\\mathrm\{([^{}]*)\}", r"\1"),
]
_SUP_INV = {v: k for k, v in SUP.items()}
_SUB_INV = {v: k for k, v in SUB.items()}


def latex_vers_texte(t):
    """Version texte brut approximative d'une chaîne avec $...$."""
    if not t:
        return ""
    t = str(t).replace("$$", "").replace("$", "")
    for motif, rep in _TEX_VERS_TXT:
        t = re.sub(motif, rep, t)
    t = re.sub(r"\^\{([^{}]*)\}", lambda m: _sup(m.group(1)), t)
    t = re.sub(r"\^(\w)", lambda m: _sup(m.group(1)), t)
    t = re.sub(r"_\{([^{}]*)\}", lambda m: _sub(m.group(1)), t)
    t = re.sub(r"_(\w)", lambda m: _sub(m.group(1)), t)
    for _ in range(4):
        t = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", lambda m: _par(m.group(1)) + "/" + _par(m.group(2)), t)
        t = re.sub(r"\\sqrt\[(\d+)\]\{([^{}]*)\}", lambda m: m.group(1) + "√(" + m.group(2) + ")", t)
        t = re.sub(r"\\sqrt\{([^{}]*)\}", lambda m: "√" + (m.group(1) if re.fullmatch(r"[\w.]+", m.group(1)) else "(" + m.group(1) + ")"), t)
    t = t.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"[ \t]+", " ", t).strip()


def _par(x):
    return x if re.fullmatch(r"[\w.,]+", x) else "(" + x + ")"


def _sup(x):
    return "".join(_SUP_INV.get(c, None) or "" for c in x) if all(c in _SUP_INV for c in x) else "^(" + x + ")"


def _sub(x):
    return "".join(_SUB_INV[c] for c in x) if all(c in _SUB_INV for c in x) else "_" + x


if __name__ == "__main__":
    tests = [
        "Si le discriminant Δ < 0, combien de racines réelles possède le polynôme ?",
        "S² - 2P", "a · (x + b/(2a))² - (Δ / (4a))", "n1 · sin(i1) = n2 · sin(i2)",
        "Quelle est la limite lorsque x tend vers 0+ de x * ln(x) ?", "pi / 2", "-pi / 2", "+inf",
        "Que vaut la somme S des racines x_1 et x_2 d'un polynôme ax² + bx + c lorsque Δ ≥ 0 ?",
        "1/OA' - 1/OA = 1/f'", "e^(-x)", "√(x² + 1)", "Le nombre 47 est-il un nombre premier ?",
        "La dérivée de f(x) = x³ + 2x vaut :", "f'(x) = 2ax + b",
    ]
    for t in tests:
        r = texte_vers_latex(t)
        print(t, "\n   ->", r, "\n   =>", latex_vers_texte(r))
