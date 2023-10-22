# ecoledirecte : module pour obtenir les données EcoleDirecte via l'API
import requests

# En-tête, nécessaire pour toutes les requêtes
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

def login(identifiant, motdepasse):
    '''
    login : connexion avec identifiants EcoleDirecte
    Arguments:
    identifiant: votre identifiant EcoleDirecte
    motdepasse: votre mot de passe EcoleDirecte
    Renvoie (si connexion réussie):
    login_response_json_data : données en JSON de votre compte EcoleDirecte
    '''

    LOGIN_URL = "https://api.ecoledirecte.com/v3/login.awp?v=4.43.0"
    login_request = f'data={{"uuid": "", "identifiant": "{identifiant}", "isRelogin": false, "motdepasse": "{motdepasse}"}}'
    # Tentative de connexion
    login_response = requests.post(url=LOGIN_URL, data=login_request, headers=header)

    login_response_json_data = login_response.json()

    # Obtient le token et l'identifiant d'élève
    token = login_response_json_data["token"] 
    eleve_id = login_response_json_data["data"]["accounts"][0]["id"]
    header["X-Token"] = token

    return login_response_json_data

def timeline(eleve_id, token):
    '''
    timeline : Timeline
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    timeline_json_data : données en JSON de votre timeline
    '''

    TIMELINE_URL = f'https://api.ecoledirecte.com/v3/eleves/{eleve_id}/timeline.awp?verbe=get'
    timeline_request = f'data={{"token": "{token}"}}'
    timeline_reponse = requests.post(url=TIMELINE_URL, data=timeline_request, headers=header)
    timeline_json_data = timeline_reponse.json()
    return timeline_json_data

def emploi_du_temps(eleve_id, token, date_debut, date_fin, avec_trous):
    '''
    emploi_du_temps : Emploi du temps
    Arguments :
    eleve_id : votre identifiant élève
    date_debut : date de début de votre emploi du temps
    date_fin : date de fin de votre emploi du temps
    avec_trous : affiche ou pas les trous
    /!\ avec_trous doit être soit "true" ou "false" (pas en booléen)
    Renvoie (si réussi) :
    emploi_du_temps_json_data : données en JSON de votre emploi du temps 
    '''

    EMPLOI_DU_TEMPS_URL = f"https://api.ecoledirecte.com/v3/E/{eleve_id}/emploidutemps.awp?verbe=get"
    emploi_du_temps_request = f'data={{"dateDebut": "{date_debut}", "dateFin": "{date_fin}", "avecTrous": {avec_trous}}}'
    emploi_du_temps_reponse = requests.post(url=EMPLOI_DU_TEMPS_URL, data=emploi_du_temps_request, headers=header)
    emploi_du_temps_json_data = emploi_du_temps_reponse.json()
    return emploi_du_temps_json_data

def cahier_de_texte(eleve_id, token, date):
    '''
    cahier_de_texte : Cahier de texte
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    date : jour de votre cahier de texte
    Renvoie (si réussi) :
    cahier_de_texte_json_data : données en JSON de votre cahier de texte
    '''

    CAHIER_DE_TEXTE_URL = f'https://api.ecoledirecte.com/v3/Eleves/{eleve_id}/cahierdetexte/{date}.awp?v=3&verbe=get&'
    cahier_de_texte_request = f'data={{"token": "{token}"}}'
    cahier_de_texte_reponse = requests.post(url=CAHIER_DE_TEXTE_URL, data=cahier_de_texte_request, headers=header)
    cahier_de_texte_json_data = cahier_de_texte_reponse.json()
    return cahier_de_texte_json_data

def notes(eleve_id, token):
    '''
    notes : Notes
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    notes_json_data : données en JSON de vos notes
    '''

    NOTES_URL = f'https://api.ecoledirecte.com/v3/eleves/{eleve_id}/notes.awp?v=3&verbe=get&'
    notes_request = f'data={{"token": "{token}"}}'
    notes_reponse = requests.post(url=NOTES_URL, data=notes_request, headers=header)
    notes_json_data = notes_reponse.json()
    return notes_json_data

def vie_scolaire(eleve_id, token):
    '''
    vie_scolaire : Vie scolaire
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    vie_scolaire_json_data : données en JSON de votre vie scolaire
    '''

    VIE_SCOLAIRE_URL = f'https://api.ecoledirecte.com/v3/eleves/{eleve_id}/viescolaire.awp?verbe=get'
    vie_scolaire_request = f'data={{"token": "{token}"}}'
    vie_scolaire_reponse = requests.post(url=VIE_SCOLAIRE_URL, data=vie_scolaire_request, headers=header)
    vie_scolaire_json_data = vie_scolaire_reponse.json()
    return vie_scolaire_json_data
