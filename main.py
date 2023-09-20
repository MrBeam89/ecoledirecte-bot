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

# Emploi du temps
EMPLOI_DU_TEMPS_URL = f"https://api.ecoledirecte.com/v3/E/{eleve_id}/emploidutemps.awp?verbe=get"
dateDebut = "2023-09-21"
dateFin = "2023-09-21"
avecTrous = "true"
emploi_du_temps_request = f'data={{"dateDebut": "{dateDebut}", "dateFin": "{dateFin}", "avecTrous": {avecTrous}}}'

emploi_du_temps_reponse = requests.post(url=EMPLOI_DU_TEMPS_URL, data=emploi_du_temps_request, headers=header)
emploi_du_temps_json_data = emploi_du_temps_reponse.json()

print(login_response.text)
print("\n")
print(emploi_du_temps_json_data["data"])
