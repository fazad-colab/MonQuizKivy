# -*- coding: utf-8 -*-
"""Test de bout en bout du serveur : python test_serveur.py"""
import os, tempfile, json
os.environ["MQ_DATA_DIR"] = tempfile.mkdtemp()
os.environ["ADMIN_TOKEN"] = "secret"
import flask_app as F

c = F.app.test_client()
def post(u, **j): return c.post(u, json=j).get_json()
def get(u, **h): return c.get(u, headers=h).get_json()

assert get("/api/ping")["status"] == "success"
for ident, nom in [("prof001", "M. Ali"), ("eleve01", "Sara"), ("eleve02", "Omar")]:
    assert post("/api/sauvegarde", identifiant=ident, nom_utilisateur=nom, classe_utilisateur="3ème",
                points_de_rang=120 if ident == "eleve01" else 10, consentement=True)["status"] == "success"
assert post("/api/sauvegarde", identifiant="x", nom_utilisateur="a")["status"] == "error"          # id invalide

# --- professeur crée le salon (personnalisé)
r = post("/api/salon/creer", type="classe", hote_id="prof001", hote_nom="M. Ali",
         config=dict(classe="3ème", chapitres=["Thales", "Equation et Inéquation"], nb_questions=3,
                     temps_par_question=0, avance="manuel", points_bonne=100))
code = r["code_pin"]; assert len(code) == 6 and r["nb_questions"] == 3
for i, n in [("eleve01", "Sara"), ("eleve02", "Omar")]:
    assert post("/api/salon/rejoindre", code_pin=code, identifiant=i, nom=n)["status"] == "success"
assert get(f"/api/salon/{code}/etat?id=eleve01")["statut"] == "attente"
assert post(f"/api/salon/{code}/lancer", hote_id="eleve01").get("message") == "réservé à l'hôte"   # un élève ne peut pas lancer
post(f"/api/salon/{code}/lancer", hote_id="prof001")

for q in range(3):
    st = get(f"/api/salon/{code}/etat?id=eleve01")
    assert st["statut"] == "question_active" and st["index_q"] == q
    qu = st["question"]
    assert "bonne_reponse" not in qu and "index_correct" not in qu and "explication" not in qu, "FUITE de la réponse !"
    assert get(f"/api/salon/{code}/etat?id=eleve01")["a_repondu"] is False
    # Sara répond juste (via résultats hôte), Omar toujours 0
    det = get(f"/api/salon/{code}/resultats?id=prof001")
    bonne = det["questions"][q]["index_correct"]
    assert post(f"/api/salon/{code}/repondre", identifiant="eleve01", index_q=q, choix=bonne)["status"] == "success"
    assert post(f"/api/salon/{code}/repondre", identifiant="eleve02", index_q=q, choix=0)["status"] == "success"
    assert post(f"/api/salon/{code}/repondre", identifiant="eleve01", index_q=q, choix=bonne)["status"] == "error"  # 2e réponse refusée
    h = get(f"/api/salon/{code}/etat?id=prof001")
    assert h["eleves_ont_repondu"] == 2 and len(h["participants"]) == 2
    assert "participants" not in get(f"/api/salon/{code}/etat?id=eleve01")           # élèves ne voient pas les autres
    post(f"/api/salon/{code}/suivante", hote_id="prof001")

fin = get(f"/api/salon/{code}/etat?id=eleve02")
assert fin["statut"] == "termine" and fin["classement"][0]["identifiant"] == "eleve01" and fin["classement"][0]["score"] == 300
res = get(f"/api/salon/{code}/resultats?id=prof001"); assert len(res["questions"][0]["reponses"]) == 2
assert get(f"/api/salon/{code}/resultats?id=eleve01")["message"] == "réservé à l'hôte"
post(f"/api/salon/{code}/cloturer_stats", hote_id="prof001")

# --- recherche, en ligne, profil
p = get("/api/joueur/eleve01"); assert p["parties"] == 1 and p["total"] == 3 and p["precision"] == 100.0
assert [j["identifiant"] for j in get("/api/joueurs/recherche?q=eleve")["joueurs"]][:1] == ["eleve01"]
assert get("/api/joueurs/en_ligne")["nombre"] == 3
assert get("/api/joueur/inconnu123")["status"] == "error"

# --- duel en ligne (l'hôte joue aussi) + mode auto
d = post("/api/salon/creer", type="duel", hote_id="eleve01", hote_nom="Sara", config=dict(classe="6ème", nb_questions=2, avance="auto", temps_par_question=30))
assert d["config"]["hote_joue"] is True

# --- admin protégé
assert c.get("/api/admin/joueurs").status_code == 401
assert get("/api/admin/joueurs", **{"X-Admin-Token": "secret"})["joueurs"][0]["identifiant"]
csvtxt = c.get("/api/admin/joueurs?format=csv", headers={"X-Admin-Token": "secret"}).get_data(as_text=True)
assert csvtxt.startswith("identifiant,nom") and "eleve01" in csvtxt
assert c.get("/api/voir_stats").status_code == 401
assert post("/api/joueur/supprimer", identifiant="eleve02")["status"] == "success"
assert get("/api/joueur/eleve02")["status"] == "error"
print("✅ Tous les tests serveur passent (salon classe, anti-triche, stats, recherche, en ligne, admin, suppression)")
