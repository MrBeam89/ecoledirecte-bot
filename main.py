#!/usr/bin/env python3
# /!\ Les devoirs et les contenus de séances sont encodés en Base64
import requests
import json

identifiant = input("Identifiant: ")
motdepasse = input("Mot de passe: ")

LOGIN_URL = "https://api.ecoledirecte.com/v3/login.awp"
login_request = f'data={{"uuid": "", "identifiant": "{identifiant}", "motdepasse": "{motdepasse}"}}'
header = {
            'authority': 'api.ecoledirecte.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-gpc': '1',
            'origin': 'https://www.ecoledirecte.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.ecoledirecte.com/',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        }

# Tentative de connexion
login_response = requests.post(url=LOGIN_URL, data=login_request, headers=header)
login_response_json_data = login_response.json()

# Obtient le token et l'identifiant d'élève
token = login_response_json_data["token"]
header["X-Token"] = token
eleve_id = login_response_json_data["data"]["accounts"][0]["id"]

# Timeline
TIMELINE_URL = f'https://api.ecoledirecte.com/v3/eleves/{eleve_id}/timeline.awp?verbe=get'
timeline_request = f'data={{"token": "{token}"}}'

timeline_reponse = requests.post(url=TIMELINE_URL, data=timeline_request, headers=header)
timeline_json_data = timeline_reponse.json()

# Emploi du temps
EMPLOI_DU_TEMPS_URL = f"https://api.ecoledirecte.com/v3/E/{eleve_id}/emploidutemps.awp?verbe=get"

dateDebut = input("Emploi du temps (AAAA-MM-JJ): ")
dateFin = dateDebut
avecTrous = "false"
emploi_du_temps_request = f'data={{"dateDebut": "{dateDebut}", "dateFin": "{dateFin}", "avecTrous": {avecTrous}}}'

emploi_du_temps_reponse = requests.post(url=EMPLOI_DU_TEMPS_URL, data=emploi_du_temps_request, headers=header)
emploi_du_temps_json_data = emploi_du_temps_reponse.json()

# Cahier de texte
date_cahier_de_texte = input("Cahier de texte (AAAA-MM-JJ): ")
CAHIER_DE_TEXTE_URL = f'https://api.ecoledirecte.com/v3/Eleves/{eleve_id}/cahierdetexte/{date_cahier_de_texte}.awp?v=3&verbe=get&'
cahier_de_texte_request = f'data={{"token": "{token}"}}'

cahier_de_texte_reponse = requests.post(url=CAHIER_DE_TEXTE_URL, data=cahier_de_texte_request, headers=header)
cahier_de_texte_json_data = cahier_de_texte_reponse.json()

# Notes
NOTES_URL = f'https://api.ecoledirecte.com/v3/eleves/{eleve_id}/notes.awp?v=3&verbe=get&'
notes_request = f'data={{"token": "{token}"}}'

notes_reponse = requests.post(url=NOTES_URL, data=notes_request, headers=header)
notes_json_data = notes_reponse.json()

# Vie scolaire
VIE_SCOLAIRE_URL = f'https://api.ecoledirecte.com/v3/eleves/{eleve_id}/viescolaire.awp?verbe=get'
vie_scolaire_request = f'data={{"token": "{token}"}}'

vie_scolaire_reponse = requests.post(url=VIE_SCOLAIRE_URL, data=vie_scolaire_request, headers=header)
vie_scolaire_json_data = vie_scolaire_reponse.json()

# Pour tester
print("\n")
print("===LOGIN===")
print(json.dumps(login_response_json_data, indent=4))
print("\n")
print("===TIMELINE===")
print(json.dumps(timeline_json_data, indent=4))
print("\n")
print("===EMPLOI DU TEMPS===")
print(json.dumps(emploi_du_temps_json_data, indent=4))
print("\n")
print("===CAHIER DE TEXTE===")
print(json.dumps(cahier_de_texte_json_data, indent=4))
print("\n")
print("===NOTES===")
print(json.dumps(notes_json_data, indent=4))
print("\n")
print("===VIE SCOLAIRE===")
print(json.dumps(vie_scolaire_json_data, indent=4))
