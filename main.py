#    EcoleDirecte Bot (main.py)
#    Copyright (C) 2023-2024 MrBeam89_
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

import discord
from discord.ext import commands
import logging
import re
import datetime
import os
import traceback

import config
import ecoledirecte
import aes
import keygen
import db_handler
import b64
import str_clean

print(f"{'-'*40}\nEcoleDirecte Bot (v0.9.0b) par MrBeam89_\n{'-'*40}")

# Récupération de la configuration
BOT_CONFIG = config.get_config()
BOT_TOKEN_FILENAME = BOT_CONFIG["BOT_TOKEN_FILENAME"]
DB_KEY_FILENAME = BOT_CONFIG["DB_KEY_FILENAME"]
DB_FILENAME = BOT_CONFIG["DB_FILENAME"]
BOT_COMMAND_PREFIX = BOT_CONFIG["BOT_COMMAND_PREFIX"]
LOGGING_LEVEL = BOT_CONFIG["LOGGING_LEVEL"]
COOLDOWN = BOT_CONFIG["COOLDOWN"]
EMBED_COLOR = BOT_CONFIG["EMBED_COLOR"]

# Journalisation
year, month, day, hour, minute, second = datetime.datetime.now().timetuple()[:6]
log_filename = f"log_{year}-{month}-{day}_{hour}-{minute}-{second}.log" # Format du nom de fichier
log_directory_path = os.path.join(config.ECOLEDIRECTE_DIR, "logs")

if not os.path.exists(log_directory_path):
    print(f'Création du répertoire "{log_directory_path}"...')
    os.mkdir(log_directory_path)
    print(f'Répertoire "{log_directory_path}" créé!')
else:
    print(f'Répertoire "{log_directory_path}" existe déjà!')

log_path = os.path.join(log_directory_path, log_filename)

# Application de la configuration et de la journalisation
bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, description="Bot EcoleDirecte", intents=discord.Intents.all())
print(f'Création du fichier de journalisation dans "{log_path}".')
logging.basicConfig(level=LOGGING_LEVEL, filename=log_path, filemode="w",
                    format="%(asctime)s [%(levelname)s] %(message)s")


# Au démarrage du bot
@bot.event
async def on_ready():
    print("Bot prêt!")


# Erreures générales
@bot.event
async def on_command_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await contexte.send(f"Commande invalide! Utilisez **{BOT_COMMAND_PREFIX}aide** pour afficher la liste des commandes disponibles")
        logging.info(f"Commande invalide de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
    # Afficher message d'exception si en niveau DEBUG
    elif LOGGING_LEVEL == 10:
        print(traceback.print_exception(type(error), error, error.__traceback__))


# Vérifie si la date est valide
def date_valide(input_string):
    # Vérifie si le format est correct
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if pattern.match(input_string):
        # Vérifie si le mois et les jours sont valides
        annee, mois, jour = map(int, input_string.split('-'))
        if 1 <= mois <= 12 and 1 <= jour <= 31:
            return True
    return False


# Vérifie si les données de l'utilisateur existent dans la base de données
def credentials_fetch(id):
    user_info = db_handler.fetch_user_info(id)
    if user_info:
        username = aes.decrypt_aes(user_info[2], keygen.getkey())
        password = aes.decrypt_aes(user_info[3], keygen.getkey())
        cn = aes.decrypt_aes(user_info[4], keygen.getkey())
        cv = aes.decrypt_aes(user_info[5], keygen.getkey())
        return (username, password, cn, cv)
    else:
        return ()


# Vérifie la validité des identifiants et renvoie le token et l'ID d'élève
def credentials_check(username, password, cn, cv):    
    login_data = ecoledirecte.login(username, password, cn, cv).json()
    
    # Si identifiants corrects
    if login_data['code'] == 200:
        token = login_data["token"]
        eleve_id = login_data["data"]["accounts"][0]["id"]
        return {"token": token, "eleve_id": eleve_id}
    
    # Si identifiants changés
    if login_data['code'] == 505:
        return ()


# Aide
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def aide(contexte):
    titre = "**EcoleDirecte Bot** par Raticlette (@mrbeam89_)"
    message = f'''
Commandes disponibles :
**{BOT_COMMAND_PREFIX}login <identifiant> <motdepasse>** : Se connecter (à utiliser qu'une seule fois!)
**{BOT_COMMAND_PREFIX}logout** : Se déconnecter
**{BOT_COMMAND_PREFIX}cdt <date>** : Cahier de texte de la date choisie (sous la forme AAAA-MM-JJ)
**{BOT_COMMAND_PREFIX}edt <date>** : Emploi du temps de la date choisie (sous la forme AAAA-MM-JJ)
**{BOT_COMMAND_PREFIX}vie_scolaire** : Vie scolaire (absences, retards, encouragements et punitions)
**{BOT_COMMAND_PREFIX}notes** : *(WIP)* Récupérer vos notes
**{BOT_COMMAND_PREFIX}aide** : Ce message
**{BOT_COMMAND_PREFIX}remerciements** : Merci à eux!
**{BOT_COMMAND_PREFIX}license** : Informations de licence'''
    footer = "Envoyez-moi un MP en cas de souci!"
    github_repo_url = "https://github.com/MrBeam89/ecoledirecte-bot"

    embed = discord.Embed(title=titre, description=message, url=github_repo_url, color=EMBED_COLOR)
    embed.set_thumbnail(url="https://raw.githubusercontent.com/MrBeam89/ecoledirecte-bot/main/docs/bot_icon.png")
    embed.set_footer(text=footer)

    await contexte.send(embed=embed)


# Connexion
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def login(contexte, username, password):
    # Si l'utilisateur est déjà connecté
    if db_handler.fetch_user_info(contexte.author.id):
        logging.info(f"Utilisateur {contexte.author.name} avec l'id {contexte.author.id} deja connecte")
        await contexte.send("Vous êtes déjà connecté!")
        return

    # Si l'utilisateur n'est pas encore connecté
    await contexte.send(":hourglass: Veuillez patienter...")
    logging.info(f"Tentative d'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
    reponse = ecoledirecte.login(username, password, '', '')
    reponse_json = reponse.json()

    # Si identifiants incorrects
    if reponse_json['code'] == 505:
        # Message de connexion ratée
        titre = ':x:  **Connexion ratée!**'
        message = "Identifiant et/ou mot de passe invalide!"

        embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)
        await contexte.send(embed=embed)

        logging.info(f"Echec de l'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")

    # Si connexion initiale
    if reponse_json['code'] == 250:
        token = reponse_json['token']
        
        # Obtenir le quiz de vérification et les propositions de réponse
        quiz_connexion_get_response = ecoledirecte.quiz_connexion_get(token).json()
        question = b64.decode_base64(quiz_connexion_get_response['data']['question'])
        propositions = quiz_connexion_get_response['data']['propositions']

        # Embed du quiz
        titre = "Veuillez répondre à la question suivante par le numéro à gauche de la réponse"
        message = f"**{question}**\n"
        for proposition_index in range(len(propositions)):
            message += f"{proposition_index} : {b64.decode_base64(propositions[proposition_index])}\n"

        # Envoyer le quiz
        embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)
        await contexte.send(embed=embed)

        # Vérifier que l'auteur de la réponse est le même que celui qui a essayé de se connecter
        def check_message(message):
            return message.author == contexte.message.author and contexte.message.channel == message.channel

        # Obtenir la réponse de l'uilisateur (index de la réponse)
        try:
            reponse_numero = await bot.wait_for("message", timeout = 30, check = check_message)
            index_reponse = int(reponse_numero.content)
        except TimeoutError:
            await contexte.send("Vous avez mis trop de temps à répondre. Annulation...")
            return
        except ValueError:
            await contexte.send("Réponse invalide! Annulation...")
            return

        # Envoyer la proposition avec l'index donné par l'utilisateur
        try:
            cn_et_cv = ecoledirecte.quiz_connexion_post(propositions[index_reponse]).json()['data']
        except IndexError:
            await contexte.send("Numéro invalide! Annulation...")
            return

        # Si le quiz a été raté
        if not cn_et_cv:
            # Embed de quiz raté
            titre = ':x:  **Quiz raté!**'
            message = "Mauvaise réponse!"
            embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)

            # Envoyer l'embed, ajouter au journal et quitter
            await contexte.send(embed=embed)
            logging.info(f"Quiz d'authentification raté par l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
            return

        # Si le quiz a été réussi

        # Embed de quiz réussi
        titre = ':white_check_mark:  **Quiz réussi!**'
        message = "Bonne réponse!"
        embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)

        # Envoyer l'embed et l'ajouter au journal
        await contexte.send(embed=embed)
        logging.info(f"Quiz d'authentification réussi par l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
        
        cn = cn_et_cv['cn']
        cv = cn_et_cv['cv']
        
        # Renvoyer une requêtre de connexion avec la double-authentification réussie
        await contexte.send(":hourglass: Veuillez patienter...")
        reponse = ecoledirecte.login(username, password, cn, cv)
        reponse_json = reponse.json()

        # Ajout des identifiants chiffrés dans la base de données
        encrypted_username = aes.encrypt_aes(username, keygen.getkey())
        encrypted_password = aes.encrypt_aes(password, keygen.getkey())
        encrypted_cn = aes.encrypt_aes(cn, keygen.getkey())
        encrypted_cv = aes.encrypt_aes(cv, keygen.getkey())

        logging.info(f"Ajout des informations de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
        db_handler.add_user_info(contexte.author.id, encrypted_username, encrypted_password, encrypted_cn, encrypted_cv)

        # Message de connexion réussie
        nom = reponse_json["data"]["accounts"][0]["nom"]
        prenom = reponse_json["data"]["accounts"][0]["prenom"]
        classe = reponse_json["data"]["accounts"][0]["profile"]["classe"]["code"]

        titre = ":white_check_mark:  **Connexion réussie!**"
        message = "Connecté(e) en tant que :\n"
        message += f"**Nom** : {nom}\n**Prénom** : {prenom}\n**Classe** : {classe}"

        embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)
        await contexte.send(embed=embed)
            
        logging.info(f"Authentification reussie de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id} avec le compte de {nom} {prenom} {classe}")


# Erreurs de !login
@login.error
async def login_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        logging.info(f"Syntaxe de {BOT_COMMAND_PREFIX}login invalide par l'utilisateur {contexte.author.name}")
        await contexte.send(f"Syntaxe invalide! : Utilisez {BOT_COMMAND_PREFIX}login <identifiant> <motdepasse>")


# Déconnexion
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def logout(contexte):
    if db_handler.delete_user(contexte.author.id):
        await contexte.send("Vous êtes maintenant déconnecté!")
        logging.info(f"Deconnexion de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
    else:
        await contexte.send("Vous n'êtes pas connecté!")
        logging.info(f"Tentative de deconnexion ratee de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")


# Cahier de texte
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def cdt(contexte, date):
    # Vérifie si la date est valide!e
    if not date_valide(date):
        await contexte.send("Date invalide!")
        return None

    # Vérifie si les identifiants de l'utilisateur sont dans la base de données et les récupère
    identifiants = credentials_fetch(contexte.author.id)
    if not identifiants:
        await contexte.send(f"Vous n'êtes pas connecté! Utilisez {BOT_COMMAND_PREFIX}login <identifiant> <motdepasse>")
        return None
    
    username = identifiants[0]
    password = identifiants[1]
    cn = identifiants[2]
    cv = identifiants[3]

    # Vérifie la validité des identifiants et obtenir token et ID d'élève
    await contexte.send(":hourglass: Veuillez patienter...")   
    api_credentials = credentials_check(username, password, cn, cv)
    if not api_credentials:
        logging.info(f"Echec de l'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
        await contexte.send(f"Identifiant et/ou mot de passe changés! Veuillez **{BOT_COMMAND_PREFIX}logout** puis **{BOT_COMMAND_PREFIX}login**")
        return None

    # Obtenir les infos pour l'API
    token = api_credentials["token"]
    eleve_id = api_credentials["eleve_id"]
    cdt_data = ecoledirecte.cahier_de_texte(eleve_id, token, date).json()["data"]

    # Contenu de l'embed
    titre = f":pencil:  **Devoirs à faire pour le {date}**\n\n"

    # Liste des devoirs
    message = ""
    for index in range(len(cdt_data["matieres"])):
        try:
            matiere = cdt_data["matieres"][index]["matiere"]
            texte = str_clean.clean(b64.decode_base64(cdt_data["matieres"][index]["aFaire"]["contenu"]))
            message += f"**{matiere}** : {texte}\n"
        except Exception:
            pass
    
    # Si il n'y a pas de devoirs
    if not message:
        message = ":tada: **Pas de devoirs pour ce jour-là !**"

    # Envoyer l'embed
    embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)
    await contexte.send(embed=embed)

    logging.info(f"Utilisateur {contexte.author.name} a utilisé {BOT_COMMAND_PREFIX}cdt")

     
# Emploi du temps
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def edt(contexte, date):
    # Vérifie si la date est valide
    if not date_valide(date):
        await contexte.send("Date invalide!")
        return None

    # Vérifie si les identifiants de l'utilisateur sont dans la base de données et les récupère
    identifiants = credentials_fetch(contexte.author.id)
    if not identifiants:
        await contexte.send(f"Vous n'êtes pas connecté! Utilisez {BOT_COMMAND_PREFIX}login <identifiant> <motdepasse>")
        return None
    
    username = identifiants[0]
    password = identifiants[1]
    cn = identifiants[2]
    cv = identifiants[3]

    # Vérifie la validité des identifiants et obtenir token et ID d'élève
    await contexte.send(":hourglass: Veuillez patienter...")   
    api_credentials = credentials_check(username, password, cn, cv)
    if not api_credentials:
        logging.info(f"Echec de l'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
        await contexte.send(f"Identifiant et/ou mot de passe changés! Veuillez **{BOT_COMMAND_PREFIX}logout** puis **{BOT_COMMAND_PREFIX}login**")
        return None

    # Obtenir les infos pour l'API
    token = api_credentials["token"]
    eleve_id = api_credentials["eleve_id"]

    edt_data = ecoledirecte.emploi_du_temps(eleve_id, token, date, date, "false").json()["data"]
    edt_data = sorted(edt_data, key=lambda x: x['start_date']) # Arranger les cours dans le bon ordre
    
    # Contenu de l'embed
    titre = f":calendar_spiral:  Emploi du temps du {date}"
    message = ""
    nb_de_cours = 0
    for cours in edt_data:
        if cours["matiere"].strip() : # Si cours n'est pas vide/permanence/congés
            heure_debut = cours["start_date"][-5:]
            heure_fin = cours["end_date"][-5:]
            salle = cours["salle"]
            nom = cours["text"]
            est_annule = cours["isAnnule"]
            if est_annule == True: # Si le cours est annulé
                message += f"~~**{heure_debut}-{heure_fin}** : {nom} en {salle}~~\n"
            else:
                message += f"**{heure_debut}-{heure_fin}** : {nom} en {salle}\n"
                nb_de_cours += 1
    
    if nb_de_cours > 0:
        embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)
        await contexte.send(embed=embed)
    else:
        embed = discord.Embed(title=titre, description="**:tada: Pas de cours ce jour-là !**", color=EMBED_COLOR)
        await contexte.send(embed=embed)

    logging.info(f"Utilisateur {contexte.author.name} a utilisé {BOT_COMMAND_PREFIX}edt")


# Vie scolaire
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def vie_scolaire(contexte):
    # Vérifie si les identifiants de l'utilisateur sont dans la base de données et les récupère
    identifiants = credentials_fetch(contexte.author.id)
    if not identifiants:
        await contexte.send(f"Vous n'êtes pas connecté! Utilisez {BOT_COMMAND_PREFIX}login <identifiant> <motdepasse>")
        logging.info(f"Utilisateur {contexte.author.name} a essaye de {BOT_COMMAND_PREFIX}vie_scolaire sans être connecte")
        return None
    
    username = identifiants[0]
    password = identifiants[1]
    cn = identifiants[2]
    cv = identifiants[3]

    # Vérifie la validité des identifiants et obtenir token et ID d'élève
    await contexte.send(":hourglass: Veuillez patienter...")   
    api_credentials = credentials_check(username, password, cn, cv)
    if not api_credentials:
        logging.info(f"Echec de l'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
        await contexte.send(f"Identifiant et/ou mot de passe changés! Veuillez **{BOT_COMMAND_PREFIX}logout** puis **{BOT_COMMAND_PREFIX}login**")
        return None

    # Obtenir les infos pour l'API
    token = api_credentials["token"]
    eleve_id = api_credentials["eleve_id"]
    vie_scolaire_data = ecoledirecte.vie_scolaire(eleve_id, token).json()["data"]

    # Contenu du message
    message = ":school: **Vie scolaire**\n\n"

    # Absences et retards
    absences = []
    retards = []
    
    # Tri absence/retard
    for element in vie_scolaire_data["absencesRetards"]:
        if element["typeElement"] == "Absence":
            absences.append(element)
        if element["typeElement"] == "Retard":
            retards.append(element)

    # Message des absences
    message +=  ":ghost: **Absences**\n"
    message += f"{len(absences)} absence(s)\n"
    for absence in absences:
        date = absence["displayDate"]
        if absence["justifie"] == True:
            justifiee = "Oui"
        else:
            justifiee = "Non"
        message += f"- {date}. Justifiée ? **{justifiee}**\n"

    message += "\n"
    
    # Message des retards
    message += ":hourglass: **Retards**\n"
    message += f"{len(retards)} retard(s)\n"
    for retard in retards:
        date = retard["displayDate"]
        duree = retard["libelle"]
        if retard["justifiee"]:
            justifiee = "Oui"
        else:
            justifiee = "Non"
        message += f"- {date} de {duree}. Justifiée ? **{justifiee}**\n"
    
    message += "\n"

    # Encouragements/punitions

    encouragements = []
    punitions = []

    for element in vie_scolaire_data["sanctionsEncouragements"]:
        if element["typeElement"] == "Punition":
            punitions.append(element)
        else:
            encouragements.append(element)

    # Encouragements
    message += ":thumbsup: **Encouragements**\n"
    message += f"{len(encouragements)} encouragement(s)\n"
    for encouragement in encouragements:
        date = encouragement["date"]
        motif = encouragement["motif"]
        message += f"- Le {date} pour {motif}"

    message += "\n"

    # Punitions
    message += ":boom: **Punitions**\n"
    message += f"{len(punitions)} punition(s)\n"
    for punition in punitions:
        date = punition["date"]
        libelle = punition["libelle"]
        motif = punition["motif"]
        duree = punition["aFaire"]
        message += f"- {libelle} le {date} pendant {duree} pour {motif}\n"

    await contexte.send(message)


# Notes (WIP)
@bot.command()
async def notes(contexte):
    # Vérifie si les identifiants de l'utilisateur sont dans la base de données et les récupère
    identifiants = credentials_fetch(contexte.author.id)
    if not identifiants:
        await contexte.send(f"Vous n'êtes pas connecté! Utilisez {BOT_COMMAND_PREFIX}login <identifiant> <motdepasse>")
        return None
    
    username = identifiants[0]
    password = identifiants[1]
    cn = identifiants[2]
    cv = identifiants[3]

    # Vérifie la validité des identifiants et obtenir token et ID d'élève
    await contexte.send(":hourglass: Veuillez patienter...")   
    api_credentials = credentials_check(username, password, cn, cv)
    if not api_credentials:
        logging.info(f"Echec de l'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
        await contexte.send(f"Identifiant et/ou mot de passe changés! Veuillez **{BOT_COMMAND_PREFIX}logout** puis **{BOT_COMMAND_PREFIX}login**")
        return None

    # Obtenir les infos pour l'API
    token = api_credentials["token"]
    eleve_id = api_credentials["eleve_id"]

    notes_data = ecoledirecte.notes(eleve_id, token).json()["data"]
    notes = notes_data["notes"]

    # Contenu du message                
    message_list = ["**:100: Notes (WIP)**\n"] # Pour scinder les messages trops longs en plusieurs morceaux (et titre)
    for index in range(len(notes)):
                    note = notes[index]
                    libelle  = note["libelleMatiere"]
                    valeur = note["valeur"]
                    notesur = note["noteSur"]
                    devoir = note["devoir"]
                    text = f"{libelle} : {valeur}/{notesur} pour {devoir}\n"

                    # Contourner la limite de caractères
                    if len(message_list[-1] + text) >= 2000:
                        message_list.append(text)
                    else:
                        message_list[-1] += text

    for message in message_list:
        await contexte.send(message)


# Remerciements
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def remerciements(contexte):
    titre = ":clap:  **Remerciements**"
    message = '''Merci à...
**L'équipe derrière la [documentation (non-officielle mais excellente) de l'API](https://github.com/EduWireApps/ecoledirecte-api-docs)** : Ce bot n'aurait jamais vu le jour sans eux !
**Aleocraft (@aleocraft)** : Premier Bêta-testeur !
**CreepinGenius (@redstonecreeper6)** : Aide et conseils (même s'il a pas voulu tester)
**:index_pointing_at_the_viewer: Vous** : Si vous utilisez ce bot ou si vous contribuez!'''
    
    embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)

    await contexte.send(embed=embed)


# Licence
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def license(contexte):
    titre = "📜  **Informations de Licence du Bot**"
    message = '''Ce bot est distribué sous la Licence Publique Affero Générale GNU version 3.0 (AGPLv3). Vous êtes libre d'utiliser, de modifier et de distribuer ce bot conformément aux termes de cette licence.

**Texte Complet de la Licence :** [GNU AGPL v3.0](https://www.gnu.org/licenses/agpl-3.0.html#license-text)

Pour plus de détails, veuillez consulter la licence. Si vous avez des questions, veuillez visitez la [FAQ](https://www.gnu.org/licenses/agpl-faq.html).'''
    
    embed = discord.Embed(title=titre, description=message, color=EMBED_COLOR)

    await contexte.send(embed=embed)


# Démarrer le bot
BOT_TOKEN_FILENAME = __file__.rstrip(os.path.basename(__file__)) + BOT_TOKEN_FILENAME
with open(f"{BOT_TOKEN_FILENAME}") as BOT_TOKEN_FILE:
    bot_token = BOT_TOKEN_FILE.read()

try:
    bot.run(bot_token)
except discord.errors.LoginFailure:
    logging.error("Token invalide")
