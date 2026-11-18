# -*- coding: utf-8 -*-
"""
rangs_core.py — rangs, badges et données de graphiques (SANS dépendance à Kivy : testable partout).

 * 51 rangs : Bronze … Grand Master (I à V) + Leadership ; seuil de chaque rang = 10 RP + 5 % par palier de couleur
 * badges : dossier ./badges, noms du type Bronze_1.png, Heroique_3.png, Or_5.jpg, Grand_Maitre_2.png…
   (insensible à la casse / aux accents / à l'extension ; si un badge manque on prend le niveau voisin du même
   palier, sinon la page dessine un emblème de secours aux couleurs du palier)
"""
import os
import unicodedata

TIERS = ["Bronze", "Argent", "Or", "Platine", "Diamant", "Héroïque", "Maître", "Grand Maître", "Master", "Grand Master",
         "Leadership"]

COULEURS = {            # couleur principale du palier (reprise par la page : cadre, lueur, jauges)
    "Bronze": "#d9823b", "Argent": "#cdd6e6", "Or": "#ffc93c", "Platine": "#6fe6ff", "Diamant": "#5aa2ff",
    "Héroïque": "#ff6a3d", "Maître": "#c5b3ff", "Grand Maître": "#b366ff", "Master": "#ff2bd6",
    "Grand Master": "#ff3b5c", "Leadership": "#39ff88",
}
TITRES = {
    "Bronze": "Recrue", "Argent": "Challenger", "Or": "Conquérant", "Platine": "Élite", "Diamant": "Prodige",
    "Héroïque": "Héros", "Maître": "Maître des maths", "Grand Maître": "Légende", "Master": "Mythe",
    "Grand Master": "Souverain", "Leadership": "Leader suprême",
}
EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
_ROMAIN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}


def _norm(s):
    """minuscule, sans accents, sans espaces / tirets / soulignés : 'Grand_Maître 2' -> 'grandmaitre2'"""
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return "".join(c for c in s if c.isalnum())


def parse_rang(nom):
    """'Grand Maître III ' -> ('Grand Maître', 3) ; 'Leadership' -> ('Leadership', 0)."""
    n = (nom or "").strip()
    if n == "Leadership":
        return "Leadership", 0
    base, _, fin = n.rpartition(" ")
    return (base, _ROMAIN.get(fin, 1)) if base else (n, 1)


def seuil_du_rang(i):
    """RP à gagner pour quitter le rang d'index i (même formule que determiner_rang_et_details)."""
    return max(1, int(round(10.0 * (1.0 + (i // 5) * 0.05))))


def index_depuis_points(points, nb_rangs=51):
    """Index du rang pour un total de RP (même logique que l'appli ; sert au classement des autres joueurs)."""
    reste = int(points or 0)
    for i in range(nb_rangs):
        s = seuil_du_rang(i)
        if reste < s or i == nb_rangs - 1:
            return i
        reste -= s
    return nb_rangs - 1


def indexer_badges(dossier):
    """{clé normalisée sans extension: nom de fichier} ; le PNG l'emporte sur le JPG si les deux existent."""
    res = {}
    try:
        for f in sorted(os.listdir(dossier)):
            stem, ext = os.path.splitext(f)
            if ext.lower() in EXTENSIONS:
                k = _norm(stem)
                if k not in res or ext.lower() == ".png":
                    res[k] = f
    except Exception:
        pass
    return res


def chemin_badge(tier, niv, index, sous_dossier="badges"):
    """Chemin relatif (pour la page / Kivy) du badge, ou None. Repli : niveau voisin du même palier."""
    base = _norm(tier)
    ordre = [niv] + [n for n in range(niv - 1, 0, -1)] + [n for n in range(niv + 1, 6)]
    if tier == "Leadership":
        ordre = [0, 1]
    for n in ordre:
        for cle in (f"{base}{n}", base) if n in (0, 1) else (f"{base}{n}",):
            if cle in index:
                return f"{sous_dossier}/{index[cle]}"
    return None


def construire_liste(liste_rangs, index_badges):
    """Liste complète des rangs pour la page : nom, palier, niveau, seuil, RP cumulés pour l'atteindre, badge, couleur."""
    out, cumul = [], 0
    for i, nom in enumerate(liste_rangs):
        tier, niv = parse_rang(nom)
        out.append({"i": i, "n": nom.strip(), "t": tier, "v": niv, "s": seuil_du_rang(i), "c": cumul,
                    "b": chemin_badge(tier, niv, index_badges), "col": COULEURS.get(tier, "#00f0ff"),
                    "ti": TITRES.get(tier, "")})
        cumul += seuil_du_rang(i)
    return out


def echantillonner(valeurs, maxi=150):
    """Réduit une longue série à `maxi` points en gardant le premier et le dernier."""
    v = [x for x in (valeurs or []) if isinstance(x, (int, float))]
    if len(v) <= maxi:
        return v
    pas = (len(v) - 1) / float(maxi - 1)
    return [v[int(round(i * pas))] for i in range(maxi)]


def chapitres_pour_page(stats):
    """[[chapitre, bonnes, total], …] sans les chapitres jamais joués."""
    out = []
    for nom, v in (stats or {}).items():
        try:
            b, t = int(v[0]), int(v[1])
        except Exception:
            continue
        if t > 0:
            out.append([nom, b, t])
    return out


def rythme(hist, fenetre=30):
    """(gain moyen de RP par réponse sur les dernières réponses, tendance en RP)."""
    h = [x for x in (hist or []) if isinstance(x, (int, float))]
    if len(h) < 2:
        return 0.0, 0
    part = h[-(fenetre + 1):]
    gain = part[-1] - part[0]
    return round(gain / max(1, len(part) - 1), 2), int(gain)


def lignes_classement(lignes, mon_id, liste_rangs, index_badges):
    """Réponse de /api/classement -> lignes prêtes pour la page (badge calculé depuis les points)."""
    info = construire_liste(liste_rangs, index_badges)
    out = []
    for pos, r in enumerate(lignes or [], 1):
        rp = int(r.get("points_rang") or 0)
        g = info[index_depuis_points(rp, len(liste_rangs))]
        out.append({"pos": pos, "nom": r.get("nom", "?"), "rp": rp, "rang": g["n"], "b": g["b"], "col": g["col"],
                    "t": g["t"], "v": g["v"], "moi": r.get("identifiant") == mon_id, "on": bool(r.get("en_ligne")),
                    "classe": r.get("classe", "")})
    return out
