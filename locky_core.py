# -*- coding: utf-8 -*-
"""
locky_core.py — logique de Locky, SANS dépendance à Kivy (donc testable partout).

 * progression quotidienne : +1 point par jour de connexion, 7 points = +1 niveau de Locky
 * analyse du joueur (réussite / échec, points forts / faibles)
 * messages contextuels (Locky réagit à ce que fait le joueur, plus de messages aléatoires)
 * règles d'autorisation de la calculatrice
 * petit évaluateur sûr (ast) pour la calculatrice de secours sur PC
"""
import ast
import datetime
import math
import random
import time

JOURS_PAR_NIVEAU = 7
SEUIL_ANALYSE = 3                    # nb mini de réponses dans un chapitre pour le classer fort / faible
ACTIVITES_SANS_CALCULATRICE = ("Calcul Mental Éclair",)     # défis de calcul mental : interdite PAR LE SYSTÈME


def aujourd_hui():
    return datetime.date.today().isoformat()


# ------------------------------------------------------------------ progression
def maj_connexion(jours, dernier_jour, points, niveau, jour=None):
    """Enregistre la connexion du jour. Retourne (jours, dernier_jour, points, niveau, evenement).
    evenement : None (déjà compté aujourd'hui) | 'jour' | 'niveau'."""
    jour = jour or aujourd_hui()
    if dernier_jour == jour:
        return jours, dernier_jour, points, niveau, None
    jours += 1
    points += 1
    evt = "jour"
    if points >= JOURS_PAR_NIVEAU:
        points = 0
        niveau += 1
        evt = "niveau"
    return jours, jour, points, niveau, evt


# ------------------------------------------------------------------ analyse du joueur
def analyser(stats_chapitres):
    """stats_chapitres : {chapitre: [bonnes, total]} -> pourcentages + points forts / faibles."""
    total = bonnes = 0
    lignes = []
    for chap, v in (stats_chapitres or {}).items():
        try:
            b, t = int(v[0]), int(v[1])
        except Exception:
            continue
        total += t
        bonnes += b
        if t >= SEUIL_ANALYSE:
            lignes.append((chap, round(100.0 * b / t), t))
    reussite = round(100.0 * bonnes / total) if total else 0
    forts = sorted([x for x in lignes if x[1] >= 60], key=lambda x: (-x[1], -x[2]))[:3]
    faibles = sorted([x for x in lignes if x[1] < 60], key=lambda x: (x[1], -x[2]))[:3]
    return {"total": total, "reussite": reussite, "echec": (100 - reussite) if total else 0,
            "forts": [[c, p] for c, p, _ in forts], "faibles": [[c, p] for c, p, _ in faibles]}


# ------------------------------------------------------------------ calculatrice : qui a le droit ?
def calculatrice_permise(defi_actif=False, defi_genre="", defi_cle="", defi_titre="",
                         multi_actif=False, multi_autorisee=True, salle_active=False, salle_autorisee=True):
    """(autorisée, raison). Le système l'interdit dans les défis de calcul mental ;
    en session de groupe c'est le choix fait à la création de la session."""
    if defi_actif:
        if defi_cle in ACTIVITES_SANS_CALCULATRICE or "mental" in (defi_titre or "").lower() \
                or "mental" in (defi_cle or "").lower():
            return False, "Défi de calcul mental : calculatrice interdite par le système."
    if multi_actif and not multi_autorisee:
        return False, "Session de groupe : calculatrice non autorisée."
    if salle_active and not salle_autorisee:
        return False, "Salle en ligne : calculatrice non autorisée par l'hôte."
    return True, ""


# ------------------------------------------------------------------ messages contextuels
_T = {
    "menu": ["Salut {nom} ! Choisis ton activité.", "Prêt à grimper en grade, {nom} ?",
             "Un petit défi pour t'échauffer ?", "Je suis là si tu as besoin de moi !"],
    "choix_mode": ["{mode} : choisis ton cycle."],
    "choix_classe": ["Choisis ta classe, {nom}."],
    "entrainement": ["Entraînement : chaque erreur t'apprend quelque chose.", "Prends ton temps, la correction arrive après chaque réponse."],
    "examen": ["Examen : 10 questions, concentre-toi !", "Pas de correction avant la fin. Respire."],
    "defi": ["Défi « {titre} » : à toi de jouer !"],
    "defi_calcul_mental": ["Calcul mental : calculatrice interdite, tout dans la tête !"],
    "casse_tete": ["Choisis un casse-tête, ça muscle le cerveau."],
    "activites": ["Chaque activité débloque la suivante. Vise le grade requis !"],
    "multi": ["Session de groupe : bonne chance à tous !"],
    "hub_multi": ["Seul ou en groupe, c'est toi qui choisis."],
    "salle_attente": ["On attend les participants…"],
    "salle_question": ["Question {n} : lis bien avant de répondre."],
    "salle_fin": ["Session terminée, bravo à tous !"],
    "cours": ["Relis bien ces formules, elles reviendront !"],
    "stats": ["Voici ta progression, {nom}."],
    "evolution": ["Regarde ton évolution : tu avances !"],
    "ia": ["Pose ta question, je t'aide à comprendre."],
    "parametres": ["Ici tu règles l'appli. Touche-moi pour mon profil !"],
    "bonne": ["Bien joué !", "Exact !", "Parfait, continue !"],
    "bonne_rapide": ["Rapide et juste, bravo !"],
    "bonne_serie3": ["{combo} bonnes réponses d'affilée !"],
    "bonne_serie5": ["{combo} d'affilée ! Tu es en feu !"],
    "bonne_serie10": ["{combo} d'affilée ! Incroyable, {nom} !"],
    "fausse": ["Raté. Lis la démonstration, elle t'aidera.", "Pas grave, regarde l'explication."],
    "fausse2": ["Deux erreurs de suite : respire, relis l'énoncé."],
    "fausse3": ["Ça bloque ? Ouvre les Fiches Cours pour revoir la méthode."],
    "reponse_notee": ["Réponse enregistrée."],
    "bilan_examen_top": ["{note}/20 ! Excellent travail, {nom} !"],
    "bilan_examen_ok": ["{note}/20 : moyenne validée, continue !"],
    "bilan_examen_bas": ["{note}/20 : on retravaille ça ensemble."],
    "bilan_defi_top": ["{score}/{nb} : défi réussi !"],
    "bilan_defi_bas": ["{score}/{nb} : retente, tu vas y arriver."],
    "bilan_multi": ["Fin de partie ! Qui est le meilleur ?"],
    "niveau": ["Niveau {niveau} atteint ! Locky évolue !"],
    "promotion": ["Promotion ! Tu passes {rang} !", "{rang} ! Les autres joueurs ont du souci à se faire."],
    "jour": ["Jour {jours} ! +1 point de connexion ({pts}/7)."],
    "calc_interdite": ["Pas de calculatrice ici !"],
    "idle_question": ["Tu bloques ? Relis l'énoncé calmement.", "Élimine d'abord les réponses impossibles."],
    "idle_menu": ["Je m'ennuie… on fait un défi ?"],
}
_IMPORTANTS = {"promotion", "niveau", "jour", "calc_interdite", "bilan_examen_top", "bilan_examen_ok", "bilan_examen_bas",
               "bilan_defi_top", "bilan_defi_bas", "bilan_multi", "salle_fin"}
_ESPACEMENT = {"calme": 12.0, "normal": 4.0, "bavard": 2.0}
CTX_QUESTION = ("entrainement", "examen", "defi", "defi_calcul_mental", "salle_question", "multi")


class MessagesLocky:
    """Choisit le message selon l'événement ; limite la cadence (Locky ne parle plus n'importe quand)."""

    def __init__(self):
        self.dernier = 0.0
        self.serie_ko = 0
        self.dernier_texte = ""

    def reinit_series(self):
        self.serie_ko = 0

    def choisir(self, evt, freq="normal", **kw):
        if evt == "bonne":
            self.serie_ko = 0
            combo = int(kw.get("combo", 0))
            evt = ("bonne_serie10" if combo >= 10 and combo % 5 == 0 else
                   "bonne_serie5" if combo >= 5 and combo % 5 == 0 else
                   "bonne_serie3" if combo == 3 else
                   "bonne_rapide" if kw.get("rapide") else "bonne")
        elif evt == "fausse":
            self.serie_ko += 1
            evt = "fausse3" if self.serie_ko == 3 else "fausse2" if self.serie_ko == 2 else "fausse"
        if evt.startswith("idle") and freq == "calme":
            return None
        modeles = _T.get(evt)
        if not modeles:
            return None
        now = time.time()
        if evt not in _IMPORTANTS and now - self.dernier < _ESPACEMENT.get(freq, 4.0):
            return None
        pool = [m for m in modeles if m != self.dernier_texte] or modeles
        texte = random.choice(pool)
        try:
            texte = texte.format(**{"nom": "", "mode": "", "titre": "", "n": "", "combo": "", "note": "", "score": "",
                                    "nb": "", "niveau": "", "jours": "", "pts": "", "rang": "", **kw}).replace("  ", " ").replace(" !", " !")
        except Exception:
            pass
        self.dernier, self.dernier_texte = now, texte
        return texte


# ------------------------------------------------------------------ évaluateur sûr (calculatrice de secours PC)
_FONCTIONS = {n: getattr(math, n) for n in
              ("sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "log10", "log2", "exp",
               "floor", "ceil", "factorial", "fabs")}
_FONCTIONS.update({"ln": math.log, "log": math.log10, "abs": abs, "cbrt": lambda x: math.copysign(abs(x) ** (1 / 3), x),
                   "C": math.comb, "P": math.perm})
_CONST = {"pi": math.pi, "e": math.e, "phi": (1 + 5 ** 0.5) / 2}


def calcul_python(expression, mode_angle="DEG", ans=0.0):
    """Évalue une expression de calculatrice sans eval(). Lève ValueError en cas d'erreur."""
    s = (expression or "").replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**") \
        .replace("π", "pi").replace("φ", "phi").replace("√", "sqrt").replace(";", ",")
    import re
    s = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", s)
    s = re.sub(r"(\d+)!", r"factorial(\1)", s)
    try:
        arbre = ast.parse(s, mode="eval")
    except SyntaxError:
        raise ValueError("Syntaxe")

    def conv(x):
        return math.radians(x) if mode_angle == "DEG" else (x * math.pi / 200 if mode_angle == "GRAD" else x)

    def inv(x):
        return math.degrees(x) if mode_angle == "DEG" else (x * 200 / math.pi if mode_angle == "GRAD" else x)

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add): return a + b
            if isinstance(n.op, ast.Sub): return a - b
            if isinstance(n.op, ast.Mult): return a * b
            if isinstance(n.op, ast.Div):
                if b == 0: raise ValueError("Division par zéro")
                return a / b
            if isinstance(n.op, ast.Pow):
                if abs(b) > 1000: raise ValueError("Exposant trop grand")
                return a ** b
            if isinstance(n.op, ast.Mod): return a % b
        if isinstance(n, ast.UnaryOp):
            v = ev(n.operand)
            if isinstance(n.op, ast.USub): return -v
            if isinstance(n.op, ast.UAdd): return v
        if isinstance(n, ast.Name):
            if n.id == "ans": return ans
            if n.id in _CONST: return _CONST[n.id]
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FONCTIONS and not n.keywords:
            nom, args = n.func.id, [ev(a) for a in n.args]
            if nom in ("sin", "cos", "tan"): args = [conv(args[0])]
            r = _FONCTIONS[nom](*args)
            if nom in ("asin", "acos", "atan"): r = inv(r)
            return r
        raise ValueError("Expression non autorisée")
    try:
        r = ev(arbre)
    except ZeroDivisionError:
        raise ValueError("Division par zéro")
    except (TypeError, OverflowError) as e:
        raise ValueError("Erreur")
    if isinstance(r, complex) or r != r or r in (float("inf"), float("-inf")):
        raise ValueError("Résultat indéfini")
    return r


def formater(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return ("%.10g" % x)
