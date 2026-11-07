# -*- coding: utf-8 -*-
"""
moteur_quiz.py  (version 2 — rendu LaTeX/KaTeX)
===============================================
Façade unique utilisée par l'application ET par le serveur Flask.

    q = MoteurMathematique.generer_question("3ème", "Thales", index_grade=2, niveau_profil=4)
    q = {
        "enonce":        "Texte avec $maths$ en LaTeX",
        "options":       ["$...$", "$...$", "$...$", "$...$"],   # mélangées
        "index_correct": 2,                                       # position de la bonne réponse
        "bonne_reponse": "$...$",
        "explication":   "...",
        "chapitre": "Thales", "classe": "3ème",
        "enonce_txt", "options_txt", "explication_txt"            # versions texte brut (secours)
    }

Corrections apportées par rapport à l'ancienne version
------------------------------------------------------
 * la bonne réponse est identifiée par INDEX (plus de comparaison de chaînes) ;
 * 4 choix systématiquement (complétés intelligemment) sauf questions Oui/Non ;
 * plus de suppression des "$" : tout est rendu en LaTeX ;
 * le chapitre demandé est respecté (l'ancien code pouvait en changer en silence) ;
 * 11 chapitres du programme sans générateur sont maintenant couverts ;
 * bug Optique de Descartes (UnboundLocalError) corrigé dans moteur_legacy.py ;
 * difficulté plafonnée (les nombres n'explosent plus avec le niveau du profil).
"""
import random
import re

from latex_utils import texte_vers_latex, latex_vers_texte
from generateurs_latex import REGISTRE as GEN_NATIFS
from moteur_legacy import MoteurMathematique as _Legacy

PROGRESSION_OFFICIELLE = {
    "6ème": ["Arithmétiques", "Droites et Segments", "Nombres décimaux", "Les angles", "Fraction", "Triangles",
             "Organisation des calculs", "Cercle et parallélogramme",
             "Entier relatifs et nombres décimaux relatifs", "Symétrie centrale et axiale",
             "Initiation aux calculs littéraux", "Proportionnalité", "Cube – Pavé droit – Cylindre",
             "Pourcentage et échelle"],
    "5ème": ["Nombres décimaux relatifs", "Puissance", "Arithmétique", "Distance entre deux points", "Angles",
             "Fraction", "Calcul littérale", "Notion d’équation", "Symétrie centrale et orthogonale",
             "Médiatrice d’un segment", "Repérage sur un quadrillage", "Proportionnalité", "Pourcentage et échelle",
             "Polygone", "Prisme droit", "Pyramide"],
    "4ème": ["PGDC et PPCM", "Nombres rationnels", "Distance d’un point à une droite", "Secteurs angulaires",
             "Symétrie centrale et orthogonale", "Projection", "Les triangles", "Cercle", "Outil vectoriel",
             "Puissance", "Calcul sur les expressions algébriques", "Equation, Intervalle et Inéquation",
             "Proportionnalité", "Statistique", "Repérage", "Sphère et boule", "Polygone régulier",
             "Pyramide et cône de révolution"],
    "3ème": ["Renforcement de capacité", "Racine carrée et Valeur absolue", "Triangle rectangle",
             "Monôme et polynôme", "Thales", "Equation et Inéquation", "Vecteur et Homothétie", "Repère",
             "Equation d’une droite", "Application affine", "Système dans IR²", "Statistique",
             "Angles et Rotation", "Symétrie centrale et Axiale", "Pyramide et cône", "Sujet types"],
    "2nde": ["Vecteurs et repérage", "Valeur absolue et intervalles"],
    "1ére": ["Dérivation fonctionnelle", "Polynômes du second degré"],
    "Terminale": ["Nombres complexes", "Calcul intégral"],
    "1ére année": ["Cinématique absolue", "Analyse 1", "Analyse 2", "Accélération de Coriolis", "Frenet",
                   "Régime RLC", "Optique de Descartes", "Théorème du rang", "Développements limités"],
}
CLASSES = list(PROGRESSION_OFFICIELLE.keys())
NIVEAUX = {"Collège": ["6ème", "5ème", "4ème", "3ème"], "Lycée": ["2nde", "1ére", "Terminale"],
           "Université": ["1ére année"]}


def _norm(s):
    return (s or "").replace("’", "'").strip().lower()


_ALIAS = {"aanalyse 1": "Analyse 1"}


def _facteur(index_grade, niveau_profil):
    return min(5, 1 + (max(0, index_grade) // 5) + (max(1, niveau_profil) // 3))


# ----------------------------------------------------------------------------
# Complétion des choix
# ----------------------------------------------------------------------------
_NUM = re.compile(r"^\s*(-?\d+(?:[.,]\d+)?)\s*(.*)$")
_cache_distracteurs = {}


def _voisins_numeriques(texte):
    """'12 cm' -> ['13 cm', '11 cm', '24 cm', '6 cm', ...] (plausibles)."""
    m = _NUM.match(texte)
    if not m:
        return []
    brut, suffixe = m.group(1), m.group(2)
    virg = "," in brut
    try:
        n = float(brut.replace(",", "."))
    except ValueError:
        return []
    ent = float(n).is_integer()
    cands = [n + 1, n - 1, n * 2, n / 2, n + 10, n - 10, -n, n * 10, n / 10, n + 2, n - 2, n * 3]
    sortie = []
    for c in cands:
        if c == n or (c < 0 and n > 0 and random.random() < .6):
            continue
        if ent and not float(c).is_integer():
            c = round(c, 1)
        txt = ("%d" % c) if float(c).is_integer() else ("%g" % c)
        if virg:
            txt = txt.replace(".", ",")
        sortie.append((txt + (" " + suffixe if suffixe else "")).strip())
    random.shuffle(sortie)
    return sortie


def _distracteurs_chapitre(classe, chapitre, index_grade, niveau_profil):
    """Réponses d'autres tirages du même chapitre (servent de faux choix plausibles)."""
    cle = (classe, chapitre)
    if cle not in _cache_distracteurs:
        pool = []
        for _ in range(30):
            try:
                _, c, _, _ = _Legacy.moteur_generateur_mathematique(classe, chapitre, min(index_grade, 14), min(niveau_profil, 9))
                pool.append(str(c))
            except Exception:
                break
        _cache_distracteurs[cle] = list(dict.fromkeys(pool))
    return list(_cache_distracteurs[cle])


def _meme_nature(a, b):
    na, nb_ = bool(re.search(r"\d", a)), bool(re.search(r"\d", b))
    if na != nb_:
        return False
    la, lb = max(1, len(a)), max(1, len(b))
    return 0.4 <= la / lb <= 2.5


def _est_oui_non(textes):
    return {t.strip().lower() for t in textes} <= {"oui", "non"}


def _construire(enonce, correct, opts, exp, classe, chapitre, index_grade, niveau_profil, deja_latex, nb_options=4):
    opts = [str(o) for o in opts]
    correct = str(correct)
    if correct not in opts:
        opts.append(correct)
    opts = list(dict.fromkeys(opts))

    # compléter à nb_options choix (sauf Oui/Non)
    if len(opts) < nb_options and not _est_oui_non(opts):
        plain_ref = latex_vers_texte(correct) if deja_latex else correct
        if deja_latex:
            # le générateur natif a déjà tout en LaTeX : on ne complète que les réponses purement numériques
            candidats = []
            if re.fullmatch(r"-?\d+(?:,\d+)?", plain_ref.strip()):
                candidats = [texte_vers_latex(v) for v in _voisins_numeriques(plain_ref)]
        else:
            candidats = _voisins_numeriques(correct)
            if (not candidats or len(opts) + len(candidats) < nb_options) and _NUM.match(plain_ref):
                # réponse numérique : on peut piocher d'autres valeurs numériques du chapitre.
                # Réponses TEXTE : on garde 3 choix plutôt que d'ajouter des faux choix absurdes
                # tirés d'autres questions (ils rendaient la bonne réponse évidente).
                candidats += [d for d in _distracteurs_chapitre(classe, chapitre, index_grade, niveau_profil)
                              if _NUM.match(d) and _meme_nature(d, plain_ref)]
        for c in candidats:
            if len(opts) >= nb_options:
                break
            if c not in opts and c.strip() != correct.strip():
                opts.append(c)

    random.shuffle(opts)
    if deja_latex:
        fmt = lambda t: t
    else:
        fmt = texte_vers_latex
    enonce_l = fmt(enonce)
    opts_l = [fmt(o) for o in opts]
    correct_l = fmt(correct)
    exp_l = fmt(exp)
    # sécurité : après conversion deux options ne doivent pas devenir identiques
    vus, finales, idx_ok = set(), [], 0
    for brut, o in zip(opts, opts_l):
        if o in vus:
            if brut == correct:                 # la bonne réponse devenue doublon d'un autre choix
                idx_ok = finales.index(o)
            continue
        vus.add(o)
        if brut == correct:
            idx_ok = len(finales)
        finales.append(o)
    # filet de sécurité : la bonne réponse convertie doit se trouver à l'index annoncé
    if correct_l in finales:
        idx_ok = finales.index(correct_l)
    return {
        "enonce": enonce_l,
        "options": finales,
        "index_correct": idx_ok,
        "bonne_reponse": correct_l,
        "explication": exp_l,
        "chapitre": chapitre,
        "classe": classe,
        "enonce_txt": latex_vers_texte(enonce_l),
        "options_txt": [latex_vers_texte(o) for o in finales],
        "explication_txt": latex_vers_texte(exp_l),
    }


class MoteurMathematique:
    PROGRESSION = PROGRESSION_OFFICIELLE
    CLASSES = CLASSES
    NIVEAUX = NIVEAUX

    # -------------------------------------------------------------- API utile
    @staticmethod
    def chapitres_de(classe):
        return list(PROGRESSION_OFFICIELLE.get(classe, []))

    @staticmethod
    def niveau_de(classe):
        for niv, cl in NIVEAUX.items():
            if classe in cl:
                return niv
        return "Lycée"

    @staticmethod
    def generer_question(classe, chapitre=None, index_grade=0, niveau_profil=1, nb_options=4):
        """Renvoie un dict (voir en-tête). Si chapitre est None : chapitre aléatoire de la classe."""
        chapitres = PROGRESSION_OFFICIELLE.get(classe) or PROGRESSION_OFFICIELLE["3ème"]
        if not chapitre:
            chapitre = random.choice(chapitres)
        chapitre = _ALIAS.get(_norm(chapitre), chapitre)
        fd = _facteur(index_grade, niveau_profil)

        gen = GEN_NATIFS.get(chapitre) or GEN_NATIFS.get(chapitre.replace("’", "'"))
        if gen is not None:
            e, c, faux, x = gen(fd)
            return _construire(e, c, [c] + list(faux), x, classe, chapitre, index_grade, niveau_profil,
                               deja_latex=True, nb_options=nb_options)
        # ancien moteur (banques de questions) + conversion LaTeX automatique
        e, c, o, x = _Legacy.moteur_generateur_mathematique(classe, chapitre, min(index_grade, 14), min(niveau_profil, 9))
        return _construire(e, c, o, x, classe, chapitre, index_grade, niveau_profil, deja_latex=False,
                           nb_options=nb_options)

    @staticmethod
    def generer_serie(classe, chapitres, nombre, index_grade=0, niveau_profil=1):
        """Série de questions SANS doublon d'énoncé (mode classe / examen)."""
        chapitres = [c for c in (chapitres or []) if c] or PROGRESSION_OFFICIELLE.get(classe, [])
        vus, serie, essais = set(), [], 0
        while len(serie) < nombre and essais < nombre * 12:
            essais += 1
            q = MoteurMathematique.generer_question(classe, random.choice(chapitres), index_grade, niveau_profil)
            if q["enonce"] in vus:
                continue
            vus.add(q["enonce"])
            serie.append(q)
        return serie

    @staticmethod
    def verifier(q, index_choisi):
        return int(index_choisi) == int(q["index_correct"])

    # ----------------------------------------------------- compatibilité main.py
    @staticmethod
    def moteur_generateur_mathematique(classe_cible, chapitre_cible, index_grade=0, niveau_profil=1):
        """Ancienne signature : (enonce, correct, opts, exp) — en LaTeX désormais."""
        q = MoteurMathematique.generer_question(classe_cible, chapitre_cible, index_grade, niveau_profil)
        return q["enonce"], q["bonne_reponse"], q["options"], q["explication"]


if __name__ == "__main__":
    import json
    print(json.dumps(MoteurMathematique.generer_question("3ème", "Thales"), ensure_ascii=False, indent=2))
