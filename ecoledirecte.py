#    EcoleDirecte Bot (ecoledirecte.py)
#    Copyright 2023-2024 MrBeam89_
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

# ecoledirecte : module pour obtenir les données EcoleDirecte via l'API
import requests

# URLs pour les requêtes
urls = {
            "LOGIN_URL": "https://api.ecoledirecte.com/v3/login.awp?v=4.44.0",
            "QUIZ_CONNEXION_GET_URL": "https://api.ecoledirecte.com/v3/connexion/doubleauth.awp?verbe=get&v=4.53.4",
            "QUIZ_CONNEXION_POST_URL": "https://api.ecoledirecte.com/v3/connexion/doubleauth.awp?verbe=post&v=4.53.4",
            "TIMELINE_URL": f"https://api.ecoledirecte.com/v3/eleves/{{eleve_id}}/timeline.awp?verbe=get&v=4.44.1",
            "EMPLOI_DU_TEMPS_URL": f"https://api.ecoledirecte.com/v3/E/{{eleve_id}}/emploidutemps.awp?v=4.46.3&verbe=get",
            "CAHIER_DE_TEXTE_URL": f"https://api.ecoledirecte.com/v3/Eleves/{{eleve_id}}/cahierdetexte/{{date}}.awp?verbe=get&v=4.44.1",
            "NOTES_URL": f"https://api.ecoledirecte.com/v3/eleves/{{eleve_id}}/notes.awp?verbe=get&v=4.44.1",
            "VIE_SCOLAIRE_URL": f"https://api.ecoledirecte.com/v3/eleves/{{eleve_id}}/viescolaire.awp?verbe=get&v=4.44.1",
            "TIMELINE_COMMUNE_URL": f"https://api.ecoledirecte.com/v3/E/{{eleve_id}}/timelineAccueilCommun.awp?verbe=get&v=4.44.1",
            "CARNET_DE_CORRESPONDANCE_URL": f"https://api.ecoledirecte.com/v3/eleves/{{eleve_id}}/eleveCarnetCorrespondance.awp?verbe=get&v=4.44.1",
            "DOCUMENTS_ADMINISTRATIFS_URL": f"https://api.ecoledirecte.com/v3/elevesDocuments.awp?verbe=get&v=4.44.1?archive={{archive}}",
            "QCMS_URL": f"https://api.ecoledirecte.com/v3/eleves/{{eleve_id}}/qcms/0/associations.awp?verbe=get&v=4.44.1",
            "MANUELS NUMERIQUES_URL": f"https://api.ecoledirecte.com/v3/Eleves/{{eleve_id}}/manuelsNumeriques.awp?verbe=get&v=4.44.1",
            "VIE_DE_CLASSE_URL": f"https://api.ecoledirecte.com/v3/Classes/{{classe_id}}/viedelaclasse.awp?verbe=get&v=4.44.1",
            "FORMULAIRES_URL": "https://api.ecoledirecte.com/v3/edforms.awp?verbe=getlist&v=4.46.3"
    }

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

def login(identifiant, motdepasse, cn, cv):
    '''
    login : connexion avec identifiants EcoleDirecte
    Arguments:
    identifiant: votre identifiant EcoleDirecte
    motdepasse: votre mot de passe EcoleDirecte
    cn : Utilisé pour double-authentification
    cv : Utilisé pour double-authentification
    Renvoie (si connexion réussie):
    login_reponse : réponse d'EcoleDirecte pour la connexion
    '''

    url = urls["LOGIN_URL"]
    login_request = f'data={{"uuid": "", "identifiant": "{identifiant}", "isRelogin": false, "motdepasse": "{motdepasse}", "fa": [{{"cn": "{cn}", "cv": "{cv}"}}]}}'
    login_response = requests.post(url=url, data=login_request, headers=header)
    
    return login_response

def quiz_connexion_get(token):
    '''
    quiz_connexion_get : Obtenir le QCM donné lors d'une connexion à partir d'un nouvel appareil
    Arguments :
    token : Token
    '''

    url = urls["QUIZ_CONNEXION_GET_URL"]
    quiz_connexion_get_request = 'data={}'
    header["x-token"] = token
    qcm_connexion_get_response = requests.post(url=url, data=quiz_connexion_get_request, headers=header)

    return qcm_connexion_get_response

def quiz_connexion_post(proposition):
    '''
    quiz_connexion_post : Renvoyer la réponse du QCM donné lors d'une connexion à partir d'un nouvel appareil
    Arguments :
    proposition : Proposition du QCM
    '''

    url = urls["QUIZ_CONNEXION_POST_URL"]
    quiz_connexion_post_request = f'data={{"choix": "{proposition}"}}'
    quiz_connexion_post_response = requests.post(url=url, data=quiz_connexion_post_request, headers=header)

    return quiz_connexion_post_response

def timeline(eleve_id, token):
    '''
    timeline : Timeline
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    timeline_reponse : réponse d'EcoleDirecte pour la timeline
    '''
    header["X-Token"] = token

    url = urls["TIMELINE_URL"].format(eleve_id=eleve_id)
    timeline_request = f'data={{"token": "{token}"}}'
    timeline_reponse = requests.post(url=url, data=timeline_request, headers=header)
    
    return timeline_reponse

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
    emploi_du_temps_reponse : réponse d'EcoleDirecte pour l'emploi du temps à la date choisie/l'intervalle choisi
    '''
    header["X-Token"] = token
    
    url = urls["EMPLOI_DU_TEMPS_URL"].format(eleve_id=eleve_id)
    emploi_du_temps_request = f'data={{"dateDebut": "{date_debut}", "dateFin": "{date_fin}", "avecTrous": {avec_trous}}}'
    emploi_du_temps_reponse = requests.post(url=url, data=emploi_du_temps_request, headers=header)

    return emploi_du_temps_reponse

def cahier_de_texte(eleve_id, token, date):
    '''
    cahier_de_texte : Cahier de texte
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    date : jour de votre cahier de texte
    Renvoie (si réussi) :
    cahier_de_texte_reponse : réponse d'EcoleDirecte pour le cahier de texte à la date choisie
    '''
    header["X-Token"] = token

    url = urls["CAHIER_DE_TEXTE_URL"].format(eleve_id=eleve_id, date=date)
    cahier_de_texte_request = f'data={{"token": "{token}"}}'
    cahier_de_texte_reponse = requests.post(url=url, data=cahier_de_texte_request, headers=header)
    
    return cahier_de_texte_reponse

def notes(eleve_id, token):
    '''
    notes : Notes
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    notes_reponse : réponse d'EcoleDirecte pour les notes
    '''
    header["X-Token"] = token

    url = urls["NOTES_URL"].format(eleve_id=eleve_id)
    notes_request = f'data={{"token": "{token}"}}'
    notes_reponse = requests.post(url=url, data=notes_request, headers=header)

    return notes_reponse

def vie_scolaire(eleve_id, token):
    '''
    vie_scolaire : Vie scolaire
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    vie_scolaire_reponse : réponse d'EcoleDirecte pour la vie scolaire
    '''
    header["X-Token"] = token

    url = urls["VIE_SCOLAIRE_URL"].format(eleve_id=eleve_id)
    vie_scolaire_request = f'data={{"token": "{token}"}}'
    vie_scolaire_reponse = requests.post(url=url, data=vie_scolaire_request, headers=header)

    return vie_scolaire_reponse

def timeline_commune(eleve_id, token):
    '''
    timeline_commune : Timeline commune
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    timeline_commune_reponse : réponse d'EcoleDirecte pour la timeline commune
    '''
    header["X-Token"] = token

    url = urls["TIMELINE_COMMUNE_URL"].format(eleve_id=eleve_id)
    timeline_commune_request = f'data={{"token": "{token}"}}'
    timeline_commune_reponse = requests.post(url=url, data=timeline_commune_request, headers=header)

    return timeline_commune_reponse

def carnet_de_correspondance(eleve_id, token):
    '''
    carnet_de_correspondance : Carnet de correspondance
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    carnet_de_correspondance_reponse : réponse d'EcoleDirecte pour le carnet de correspondance
    '''
    header["X-Token"] = token
    
    url = urls["CARNET_DE_CORRESPONDANCE_URL"].format(eleve_id=eleve_id)
    carnet_de_correspondance_request = f'data={{"token": "{token}"}}'
    carnet_de_correspondance_reponse = requests.post(url=url, data=carnet_de_correspondance_request, headers=header)

    return carnet_de_correspondance_reponse

def documents_administratifs(token, archive):
    '''
    documents_administratifs
    Arguments :
    token : votre token
    archive : année associée aux documents sous la forme (AAAA-AAAA), laisser vide pour l'année actuelle
    Renvoie (si réussi) :
    documents_administratifs_reponse : réponse d'EcoleDirecte pour les documents administratifs de l'année choisie
    '''
    header["X-Token"] = token

    url = urls["DOCUMENTS_ADMINISTRATIFS_URL"].format(archive=archive)
    documents_administratifs_request = f'data={{"token": "{token}"}}'
    documents_administratifs_reponse = requests.post(url=url, data=documents_administratifs_request, headers=header)
    
    return documents_administratifs_reponse

def qcms(eleve_id, token):
    '''
    qcms : QCMs
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    qcms_reponse : réponse d'EcoleDirecte pour les QCMs
    '''
    header["X-Token"] = token
    
    url = urls["QCMS_URL"].format(eleve_id=eleve_id)
    qcms_request = f'data={{"token": "{token}"}}'
    qcms_reponse = requests.post(url=url, data=qcms_request, headers=header)
    
    return qcms_reponse

def manuels_numeriques(eleve_id, token):
    '''
    manuels_numeriques : Manuels numériques
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    Renvoie (si réussi) :
    manuels_numeriques_reponse : réponse d'EcoleDirecte pour les manuels numériques
    '''
    header["X-Token"] = token

    url = urls["MANUELS NUMERIQUES_URL"].format(eleve_id=eleve_id)
    manuels_numeriques_request = f'data={{"token": "{token}"}}'
    manuels_numeriques_reponse = requests.post(url=url, data=manuels_numeriques_request, headers=header)
    
    return manuels_numeriques_reponse

def vie_de_classe(token, classe_id):
    '''
    vie_de_classe : Vie de classe
    Arguments :
    token : votre token
    classe_id : votre identifiant de classe
    Renvoie (si réussi) :
    vie_de_classe_reponse : réponse d'EcoleDirecte pour la vie de classe
    '''
    header["X-Token"] = token

    url = urls["VIE_DE_CLASSE_URL"].format(classe_id=classe_id)
    vie_de_classe_request = f'data={{"token": "{token}"}}'
    vie_de_classe_reponse = requests.post(url=url, data=vie_de_classe_request, headers=header)

    return vie_de_classe_reponse

def formulaires(eleve_id, token, annee_scolaire):
    '''
    formulaires : Formulaires
    Arguments :
    eleve_id : votre identifiant élève
    token : votre token
    annee_scolaire : année scolaire sous le format AAAA-AAAA
    Renvoie (si réussi) :
    formulaires_reponse : réponse d'EcoleDirecte pour les formulaires
    '''

    url = urls["FORMULAIRES_URL"].format(eleve_id=eleve_id, annee_scolaire=annee_scolaire)
    formulaires_request = f'data={{"token": "{token}", "anneeForms": "{annee_scolaire}", "typeEntity": "E", "idEntity": {eleve_id}}}'
    formulaires_reponse = requests.post(url=url, data=formulaires_request, headers=header)
    
    return formulaires_reponse