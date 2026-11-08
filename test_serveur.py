# -*- coding: utf-8 -*-
"""Test de bout en bout du serveur : python test_serveur.py"""
import os, tempfile, json, re
os.environ["MQ_DATA_DIR"] = tempfile.mkdtemp()
os.environ["ADMIN_TOKEN"] = "secret"
import flask_app as F

c = F.app.test_client()
TOK = {}                                   # identifiant -> jeton de session


def _jeton_pour(url, j):
    ident = j.get("identifiant") or j.get("hote_id")
    m = re.search(r"[?&]id=([^&]+)", url)
    ident = ident or (m.group(1) if m else None)
    return TOK.get(ident) or TOK.get("_defaut")       # sinon : un joueur quelconque connecté


def post(u, **j):
    t = _jeton_pour(u, j)
    return c.post(u, json=j, headers={"Authorization": f"Bearer {t}"} if t else {}).get_json()


def get(u, **h):
    t = _jeton_pour(u, {})
    if t:
        h = {"Authorization": f"Bearer {t}", **h}
    return c.get(u, headers=h).get_json()


def compte(nom, email, ile="Ngazidja", mdp="motdepasse1"):
    r = c.post("/api/inscription", json=dict(nom=nom, email=email, ile=ile, mot_de_passe=mdp)).get_json()
    assert r["status"] == "success", r
    TOK[r["identifiant"]] = r["jeton"]
    return r["identifiant"]


# --- sécurité des comptes ---------------------------------------------------------------
assert c.get("/api/joueurs/en_ligne").status_code == 401                      # rien sans compte
assert c.post("/api/sauvegarde", json=dict(identifiant="eleve01")).status_code == 401
assert c.post("/api/inscription", json=dict(nom="A", email="x", ile="Ngazidja", mot_de_passe="123456")).get_json()["status"] == "error"
assert c.post("/api/inscription", json=dict(nom="Sara", email="sara@ex.com", ile="Paris", mot_de_passe="123456")).get_json()["status"] == "error"
assert c.post("/api/inscription", json=dict(nom="Sara", email="sara@ex.com", ile="Maore", mot_de_passe="123")).get_json()["status"] == "error"
prof = compte("M. Ali", "ali@ex.com", "Ndzuani")
eleve1 = compte("Sara", "sara@ex.com", "Ngazidja")
eleve2 = compte("Omar", "omar@ex.com", "Mwali")
TOK["_defaut"] = TOK[eleve1]
assert c.post("/api/inscription", json=dict(nom="Autre", email="SARA@ex.com", ile="Maore", mot_de_passe="123456")).get_json()["status"] == "error"   # e-mail déjà pris
# connexion : les 5 informations doivent correspondre
ok_ = dict(nom="sara", identifiant=eleve1, email="Sara@ex.com", ile="Ngazidja", mot_de_passe="motdepasse1")
r = c.post("/api/connexion", json=ok_).get_json(); assert r["status"] == "success" and r["compte"]["nom"] == "Sara" and "mdp_hash" not in json.dumps(r)
for faux in (dict(mot_de_passe="mauvais123"), dict(ile="Maore"), dict(email="autre@ex.com"), dict(nom="Pierre")):
    assert c.post("/api/connexion", json={**ok_, **faux}).get_json()["status"] == "error"
assert c.post("/api/connexion", json={**ok_, "mot_de_passe": "zzzzzz1"}).status_code in (401, 429)
assert c.post("/api/connexion", json={**ok_, "mot_de_passe": "zzzzzz2"}).status_code in (401, 429)   # blocage après 5 échecs
assert c.post("/api/connexion", json=ok_).status_code == 429, "le blocage anti force-brute doit s'activer"
# usurpation : le jeton de Sara ne permet pas d'agir au nom d'Omar
assert c.post("/api/sauvegarde", json=dict(identifiant=eleve2, points_de_rang=9999),
              headers={"Authorization": f"Bearer {TOK[eleve1]}"}).status_code == 403
# le mot de passe n'est jamais stocké en clair
import sqlite3
con = sqlite3.connect(F.DB_PATH); h = con.execute("SELECT mdp_hash FROM joueurs WHERE identifiant=?", (eleve1,)).fetchone()[0]; con.close()
assert h and "motdepasse1" not in h
# vérification e-mail (code lu dans la base de test : en production il part par e-mail)
import hashlib
con = sqlite3.connect(F.DB_PATH); row = con.execute("SELECT code_hash FROM codes_email WHERE identifiant=?", (eleve1,)).fetchone(); con.close()
assert row and c.post("/api/verifier_email", json=dict(code="000000"), headers={"Authorization": f"Bearer {TOK[eleve1]}"}).get_json()["status"] == "error"
trouve = next(f"{n:06d}" for n in range(1000000) if hashlib.sha256((eleve1 + f"{n:06d}").encode()).hexdigest() == row[0])
assert c.post("/api/verifier_email", json=dict(code=trouve), headers={"Authorization": f"Bearer {TOK[eleve1]}"}).get_json()["compte"]["email_verifie"] is True

assert get("/api/ping")["status"] == "success"
for ident, nom in [(prof, "M. Ali"), (eleve1, "Sara"), (eleve2, "Omar")]:
    assert post("/api/sauvegarde", identifiant=ident, nom_utilisateur=nom, classe_utilisateur="3ème",
                points_de_rang=120 if ident == eleve1 else 10, consentement=True)["status"] == "success"

# --- professeur crée le salon (personnalisé)
r = post("/api/salon/creer", type="classe", hote_id=prof, hote_nom="M. Ali",
         config=dict(classe="3ème", chapitres=["Thales", "Equation et Inéquation"], nb_questions=3,
                     temps_par_question=0, avance="manuel", points_bonne=100))
code = r["code_pin"]; assert len(code) == 6 and r["nb_questions"] == 3
for i, n in [(eleve1, "Sara"), (eleve2, "Omar")]:
    assert post("/api/salon/rejoindre", code_pin=code, identifiant=i, nom=n)["status"] == "success"
assert get(f"/api/salon/{code}/etat?id={eleve1}")["statut"] == "attente"
assert post(f"/api/salon/{code}/lancer", hote_id=eleve1).get("message") == "réservé à l'hôte"   # un élève ne peut pas lancer
post(f"/api/salon/{code}/lancer", hote_id=prof)

for q in range(3):
    st = get(f"/api/salon/{code}/etat?id={eleve1}")
    assert st["statut"] == "question_active" and st["index_q"] == q
    qu = st["question"]
    assert "bonne_reponse" not in qu and "index_correct" not in qu and "explication" not in qu, "FUITE de la réponse !"
    assert get(f"/api/salon/{code}/etat?id={eleve1}")["a_repondu"] is False
    # Sara répond juste (via résultats hôte), Omar toujours 0
    det = get(f"/api/salon/{code}/resultats?id={prof}")
    bonne = det["questions"][q]["index_correct"]
    assert post(f"/api/salon/{code}/repondre", identifiant=eleve1, index_q=q, choix=bonne)["status"] == "success"
    assert post(f"/api/salon/{code}/repondre", identifiant=eleve2, index_q=q, choix=0)["status"] == "success"
    assert post(f"/api/salon/{code}/repondre", identifiant=eleve1, index_q=q, choix=bonne)["status"] == "error"  # 2e réponse refusée
    h = get(f"/api/salon/{code}/etat?id={prof}")
    assert h["eleves_ont_repondu"] == 2 and len(h["participants"]) == 2
    assert "participants" not in get(f"/api/salon/{code}/etat?id={eleve1}")           # élèves ne voient pas les autres
    post(f"/api/salon/{code}/suivante", hote_id=prof)

fin = get(f"/api/salon/{code}/etat?id={eleve2}")
assert fin["statut"] == "termine" and fin["classement"][0]["identifiant"] == eleve1 and fin["classement"][0]["score"] == 300
res = get(f"/api/salon/{code}/resultats?id={prof}"); assert len(res["questions"][0]["reponses"]) == 2
assert get(f"/api/salon/{code}/resultats?id={eleve1}")["message"] == "réservé à l'hôte"
post(f"/api/salon/{code}/cloturer_stats", hote_id=prof)

# --- recherche, en ligne, profil
p = get(f"/api/joueur/{eleve1}"); assert p["parties"] == 1 and p["total"] == 3 and p["precision"] == 100.0
assert [j["identifiant"] for j in get("/api/joueurs/recherche?q=Sara")["joueurs"]][:1] == [eleve1]
assert get("/api/joueurs/en_ligne")["nombre"] == 3
assert get("/api/joueur/inconnu123")["status"] == "error"

# --- duel en ligne (l'hôte joue aussi) + mode auto
d = post("/api/salon/creer", type="duel", hote_id=eleve1, hote_nom="Sara", config=dict(classe="6ème", nb_questions=2, avance="auto", temps_par_question=30))
assert d["config"]["hote_joue"] is True

# --- admin protégé
assert c.get("/api/admin/joueurs").status_code == 401
assert get("/api/admin/joueurs", **{"X-Admin-Token": "secret"})["joueurs"][0]["identifiant"]
csvtxt = c.get("/api/admin/joueurs?format=csv", headers={"X-Admin-Token": "secret"}).get_data(as_text=True)
assert csvtxt.startswith("identifiant,nom") and eleve1 in csvtxt
assert c.get("/api/voir_stats").status_code == 401
assert post("/api/joueur/supprimer", identifiant=eleve2)["status"] == "success"
assert get(f"/api/joueur/{eleve2}", **{})["status"] == "error"
# --- anti-triche : un profil ne peut pas s'attribuer des points impossibles
F._limites.clear()                                  # (limiteur d'inscriptions réinitialisé pour le test)
tr = compte("Tricheur", "tri@ex.com", "Maore")
r = post("/api/sauvegarde", identifiant=tr, points_de_rang=999999, xp=999999, niveau_profil=99, total=3)
assert r["points_rang_accepte"] <= 4 * 3 + 10 and r["niveau_profil_accepte"] <= 5, r
r = post("/api/sauvegarde", identifiant=tr, points_de_rang=999999, total=3)         # aucune réponse de plus
assert r["points_rang_accepte"] <= 22, r
r = post("/api/sauvegarde", identifiant=tr, points_de_rang=5, total=3)              # une baisse reste possible
assert r["points_rang_accepte"] == 5

print("✅ Tous les tests serveur passent (salon classe, anti-triche, stats, recherche, en ligne, admin, suppression)")
