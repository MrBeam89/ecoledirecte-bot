#    EcoleDirecte Bot (main.py)
#    Copyright (C) 2023 MrBeam89_
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
import logging
import ecoledirecte
import aes
import keygen
import db_handler
import b64
import str_clean

COOLDOWN = 5 # En secondes

# Configuration du journal
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                    format="%(asctime)s [%(levelname)s] %(message)s")

# Paramètres du bot
# PLACER TOKEN DANS LE FICHIER token.txt
bot = commands.Bot(command_prefix="!", description="Bot EcoleDirecte", intents=discord.Intents.all())
try:
    logging.info("Ouverture du fichier token.txt")
    token_file = open("token.txt", "r")
    token = token_file.read()
except FileNotFoundError:
    logging.error("Fichier introuvable! Placer token dans un fichier token.txt")
    exit()

# Au démarrage du bot
@bot.event
async def on_ready():
    logging.info("Bot pret!")


# Erreures générales
@bot.event
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def on_command_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await contexte.send("Commande invalide! Utilisez **!aide** pour afficher la liste des commandes disponibles")
        logging.info(f"Commande invalide de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")


# Aide
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def aide(contexte):
    aide_msg = '''**EcoleDirecte Bot** par Raticlette (@mrbeam89_)
EcoleDirecte dans Discord!
Commandes disponibles :
**!login <identifiant> <motdepasse>** : Se connecter (à utiliser qu'une seule fois!)
Envoyez-moi un MP en cas de souci!
**!logout** : Se déconnecter
**!cdt <date>** : Cahier de texte de la date choisie (sous la forme AAAA-MM-JJ)
**!vie_scolaire** : Vie scolaire (absences, retards, encouragements et punitions)
**!aide** : Ce message
**!remerciements** : Merci à eux!
**!license** : Informations de license'''
    await contexte.send(aide_msg)

# Remerciements
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def remerciements(contexte):
    message = "Merci à...\n"
    message += "**CreepinGenius (@redstonecreeper6)** : Aide et conseils (même s'il a pas voulu tester)"
    await contexte.send(message)

# License
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def license(contexte):
    message = '''🤖 **Informations de Licence du Bot**

Ce bot est distribué sous la Licence Publique Générale GNU version 3.0 (GPLv3). Vous êtes libre d'utiliser, de modifier et de distribuer ce bot conformément aux termes de cette licence.

📜 **Texte Complet de la Licence :**
[GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html)

Pour plus de détails, veuillez consulter la licence. Si vous avez des questions, n'hésitez pas à contacter le développeur du bot.'''
    await contexte.send(message)

# Connexion
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def login(contexte, username, password):
    # Si l'utilisateur est déjà connecté
    if db_handler.fetch_user_info(contexte.author.id):
        logging.info(f"Utilisateur {contexte.author.name} avec l'id {contexte.author.id} deja connecte")
        await contexte.send("Vous êtes déjà connecté!")

    # Si l'utilisateur n'est pas encore connecté
    else:
        await contexte.send(":hourglass: Veuillez patienter...")
        logging.info(f"Tentative d'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
        reponse = ecoledirecte.login(username, password)
        reponse_json = reponse.json()

        # Si identifiants corrects
        if reponse_json['code'] == 200:
            # Ajout du token encrypté, l'id d'élève et l'id de classe dans la base de donnée
            encrypted_username = aes.encrypt_aes(username, keygen.getkey())
            encrypted_password = aes.encrypt_aes(password, keygen.getkey())

            logging.info(f"Ajout des informations de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
            db_handler.add_user_info(contexte.author.id, encrypted_username, encrypted_password)

            # Message de connexion réussie
            nom = reponse_json["data"]["accounts"][0]["nom"]
            prenom = reponse_json["data"]["accounts"][0]["prenom"]
            classe = reponse_json["data"]["accounts"][0]["profile"]["classe"]["code"]
            await contexte.send("Connexion réussie!")
            await contexte.send("Connecté en tant que :")
            await contexte.send(f"**Nom** : {nom}\n**Prénom** : {prenom}\n**Classe** : {classe}")
                
            logging.info(f"Authentification reussie de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id} avec le compte de {nom} {prenom} {classe}")

        # Si identifiants incorrects
        if reponse_json['code'] == 505:
            logging.info(f"Echec de l'authentification de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
            await contexte.send("Identifiant et/ou mot de passe invalide!")


# Erreurs de !login
@login.error
async def login_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        logging.info(f"Syntaxe de !login invalide par l'utilisateur {contexte.author.name}")
        await contexte.send("Syntaxe invalide! : Utilisez !login <identifiant> <motdepasse>")


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


# Emploi du temps
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def cdt(contexte, date):
    await contexte.send(":hourglass: Veuillez patienter...")
    user_info = db_handler.fetch_user_info(contexte.author.id)
    if user_info:
        username = aes.decrypt_aes(user_info[2], keygen.getkey())
        password = aes.decrypt_aes(user_info[3], keygen.getkey())
        login_data = ecoledirecte.login(username, password).json()
        token = login_data["token"]
        eleve_id = login_data["data"]["accounts"][0]["id"]

        message = ""
        cdt_data = ecoledirecte.cahier_de_texte(eleve_id, token, date).json()["data"]

        message += f":pencil: **Devoirs à faire pour le {date}**\n\n"
        for index in range(len(cdt_data["matieres"])):
            try:
                matiere = cdt_data["matieres"][index]["matiere"]
                texte = str_clean.clean(b64.decode_base64(cdt_data["matieres"][index]["aFaire"]["contenu"]))
                message += f"**{matiere}** : {texte}\n\n"
            except Exception:
                pass
        await contexte.send(message)
        logging.info(f"Utilisateur {contexte.author.name} a utilisé !cdt")

    else:
        await contexte.send("Vous n'êtes pas connecté! Utilisez !login <identifiant> <motdepasse>")
        logging.info(f"Utilisateur {contexte.author.name} a essaye de !cdt sans être connecte")

# Vie scolaire
@bot.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def vie_scolaire(contexte):
    await contexte.send(":hourglass: Veuillez patienter...")
    user_info = db_handler.fetch_user_info(contexte.author.id)
    if user_info:
        username = aes.decrypt_aes(user_info[2], keygen.getkey())
        password = aes.decrypt_aes(user_info[3], keygen.getkey())
        login_data = ecoledirecte.login(username, password).json()
        token = login_data["token"]
        eleve_id = login_data["data"]["accounts"][0]["id"]

        message = ""
        vie_scolaire_data = ecoledirecte.vie_scolaire(eleve_id, token).json()["data"]

        message += ":school: **Vie scolaire**\n\n"

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
        message += f"{len(punitions)} punition(s)"
        for punition in punitions:
            date = punition["date"]
            libelle = punition["libelle"]
            motif = punition["motif"]
            duree = punition["aFaire"]
            message += f"- {libelle} le {date} pendant {duree} pour {motif}\n"

        await contexte.send(message)

# Démarrer le bot
try:
    bot.run(token)
except discord.errors.LoginFailure:
    logging.error("Token invalide")
