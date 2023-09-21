#!/usr/bin/env python3
# Code de test
import ecoledirecte
import json

date = "2023-09-22"

print("===LOGIN===")
login_out = ecoledirecte.login("NolanCV", "AZE.rty123")

eleve_id = login_out[1]
token = login_out[2]

print(json.dumps(login_out[0], indent=4))
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

print(dir(ecoledirecte))