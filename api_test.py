# Code de test
import ecoledirecte
import json

print("Creating file \"out.txt\"")
file = open("out.txt", "w")
file.close()
file = open("out.txt", "w")

username = input("Username : ")
password = input("Password : ")
date = input("Date (AAAA-MM-JJ) : ")
archive = input("Years (AAAA-AAAA) : ")

print("Writing LOGIN info")
file.write("===LOGIN===")
login_out = ecoledirecte.login(username, password)

token = login_out["token"] 
eleve_id = login_out["data"]["accounts"][0]["id"]
classe_id = login_out["data"]["accounts"][0]["profile"]["classe"]["id"]

file.write("\n")
file.write(f"Token : {token}")
file.write("\n")
file.write(f"Id d'élève : {eleve_id}")
file.write("\n")
file.write(f"Id de classe : {classe_id}")

file.write("\n")
file.write(json.dumps(login_out["data"], indent=4))
file.write("\n")
file.write("\n")

print("Writing TIMELINE info")
file.write("===TIMELINE===")
file.write(json.dumps(ecoledirecte.timeline(eleve_id, token), indent=4))
file.write("\n")
file.write("\n")

print("Writing EMPLOI DU TEMPS info")
file.write("===EMPLOI DU TEMPS===")
file.write("\n")
file.write(json.dumps(ecoledirecte.emploi_du_temps(eleve_id, token, date, date, "true"), indent=4))
file.write("\n")
file.write("\n")

print("Writing CAHIER DE TEXTE info")
file.write("===CAHIER DE TEXTE===")
file.write("\n")
file.write(json.dumps(ecoledirecte.cahier_de_texte(eleve_id, token, date), indent=4))
file.write("\n")
file.write("\n")

print("Writing NOTES info")
file.write("===NOTES===")
file.write("\n")
file.write(json.dumps(ecoledirecte.notes(eleve_id, token), indent=4))
file.write("\n")
file.write("\n")

print("Writing VIE SCOLAIRE info")
file.write("===VIE SCOLAIRE===")
file.write("\n")
file.write(json.dumps(ecoledirecte.vie_scolaire(eleve_id, token), indent=4))
file.write("\n")
file.write("\n")

print("Writing TIMELINE COMMUNE info")
file.write("===TIMELINE COMMUNE===")
file.write("\n")
file.write(json.dumps(ecoledirecte.timeline_commune(eleve_id, token), indent=4))
file.write("\n")
file.write("\n")

print("Writing CARNET DE CORRESPONDANCE info")
file.write("===CARNET DE CORRESPONDANCE===")
file.write("\n")
file.write(json.dumps(ecoledirecte.carnet_de_correspondance(eleve_id, token), indent=4))
file.write("\n")
file.write("\n")

print("Writing DOCUMENTS ADMINISTRATIFS info")
file.write("===DOCUMENTS ADMINISTRATIFS===")
file.write("\n")
file.write(json.dumps(ecoledirecte.documents_administratifs(token, archive), indent=4))
file.write("\n")
file.write("\n")

print("Writing QCMS info")
file.write("===QCMS===")
file.write("\n")
file.write(json.dumps(ecoledirecte.qcms(eleve_id, token), indent=4))
file.write("\n")
file.write("\n")

print("Writing MANUELS NUMERIQUES info")
file.write("===MANUELS NUMERIQUES===")
file.write("\n")
file.write(json.dumps(ecoledirecte.manuels_numeriques(eleve_id, token), indent=4))
file.write("\n")
file.write("\n")

print("Writing VIE DE CLASSE info")
file.write("===VIE DE CLASSE===")
file.write("\n")
file.write(json.dumps(ecoledirecte.vie_de_classe(token, classe_id), indent=4))
file.write("\n")

print("Done!")

