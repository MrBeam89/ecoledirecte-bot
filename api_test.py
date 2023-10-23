# Code de test
import ecoledirecte
import json

username = input("Nom d'utilisateur : ")
password = input("Mot de passe : ")
date = input("Date (AAAA-MM-JJ) : ")
archive = input("Années (AAAA-AAAA) : ")

print("===LOGIN===")
login_out = ecoledirecte.login(username, password)

token = login_out["token"] 
eleve_id = login_out["data"]["accounts"][0]["id"]
classe_id = login_out["data"]["accounts"][0]["profile"]["classe"]["id"]

print(f"Token : {token}")
print(f"Id d'élève : {eleve_id}")
print(f"Id de classe : {classe_id}")

print(json.dumps(login_out["data"], indent=4))
print("\n")

print("===TIMELINE===")
print(json.dumps(ecoledirecte.timeline(eleve_id, token), indent=4))
print("\n")

print("===EMPLOI DU TEMPS===")
print(json.dumps(ecoledirecte.emploi_du_temps(eleve_id, token, date, date, "true"), indent=4))
print("\n")

print("===CAHIER DE TEXTE===")
print(json.dumps(ecoledirecte.cahier_de_texte(eleve_id, token, date), indent=4))
print("\n")

print("===NOTES===")
print(json.dumps(ecoledirecte.notes(eleve_id, token), indent=4))
print("\n")

print("===VIE SCOLAIRE===")
print(json.dumps(ecoledirecte.vie_scolaire(eleve_id, token), indent=4))
print("\n")

print("===TIMELINE COMMUNE===")
print(json.dumps(ecoledirecte.timeline_commune(eleve_id, token), indent=4))
print("\n")

print("===CARNET DE CORRESPONDANCE===")
print(json.dumps(ecoledirecte.carnet_de_correspondance(eleve_id, token), indent=4))
print("\n")

print("===DOCUMENTS ADMINISTRATIFS===")
print(json.dumps(ecoledirecte.documents_administratifs(token, archive), indent=4))
print("\n")

print("===QCMS===")
print(json.dumps(ecoledirecte.qcms(eleve_id, token), indent=4))
print("\n")

print("===MANUELS NUMERIQUES===")
print(json.dumps(ecoledirecte.manuels_numeriques(eleve_id, token), indent=4))
print("\n")

print("===VIE DE CLASSE===")
print(json.dumps(ecoledirecte.vie_de_classe(token, classe_id), indent=4))
print("\n")

print(dir(ecoledirecte))