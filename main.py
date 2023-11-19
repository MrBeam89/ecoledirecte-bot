# Bot EcoleDirecte pour Discord
# Par MrBeam89_

import discord
from discord.ext import commands
import logging
import ecoledirecte
import aes
import keygen
import db_handler
import b64
import str_clean

# Configuration du journal
logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="a",
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


# Au démarrage du bot
@bot.event
async def on_ready():
    logging.info("Bot pret!")


# Erreures générales
@bot.event
async def on_command_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await contexte.send("Commande invalide! Utilisez **!aide** pour afficher la liste des commandes disponibles")
        logging.info(f"Commande invalide de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")


# Aide
@bot.command()
async def aide(contexte):
    aide_msg = '''**EcoleDirecte Bot** par Raticlette (@mrbeam89_)
EcoleDirecte dans Discord!
Commandes disponibles :
**!aide** : Ce message
**!remerciements** : Merci à eux!
**!login <identifiant> <motdepasse>** : Se connecter (à utiliser qu'une seule fois!)
Envoyez-moi un MP en cas de souci!
**!logout** : Se déconnecter
**!cdt <date>** : Cahier de texte de la date choisie (sous la forme AAAA-MM-JJ)'''
    await contexte.send(aide_msg)


# Connexion
@bot.command()
async def login(contexte, username, password):
    # Si l'utilisateur est déjà connecté
    if db_handler.fetch_user_info(contexte.author.id):
        logging.info(f"Utilisateur {contexte.author.name} avec l'id {contexte.author.id} deja connecte")
        await contexte.send("Vous êtes déjà connecté!")

    # Si l'utilisateur n'est pas encore connecté
    else:
        await contexte.send("Veuillez patienter...")
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


# Déconnexion
@bot.command()
async def logout(contexte):
    if db_handler.delete_user(contexte.author.id):
        await contexte.send("Vous êtes maintenant déconnecté!")
        logging.info(f"Deconnexion de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")
    else:
        await contexte.send("Vous n'êtes pas connecté!")
        logging.info(f"Tentative de deconnexion ratee de l'utilisateur {contexte.author.name} avec l'id {contexte.author.id}")


# Erreurs de !login
@login.error
async def login_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        logging.info(f"Syntaxe de !login invalide par l'utilisateur {contexte.author.name}")
        await contexte.send("Syntaxe invalide! : Utilisez !login <identifiant> <motdepasse>")


# DEBUG Obtenir token
@bot.command()
async def token_get(contexte):
    encrypted_token = db_handler.fetch_user_info(contexte.author.id)
    if encrypted_token:
        token = aes.decrypt_aes(encrypted_token, keygen.getkey())
        await contexte.send(token)
    else:
        await contexte.send("Vous n'êtes pas connecté! Utilisez !login <identifiant> <motdepasse>")


# Emploi du temps
@bot.command()
async def cdt(contexte, date):
    await contexte.send("Veuillez patienter...")
    user_info = db_handler.fetch_user_info(contexte.author.id)
    if user_info:
        username = aes.decrypt_aes(user_info[2], keygen.getkey())
        password = aes.decrypt_aes(user_info[3], keygen.getkey())
        login_data = ecoledirecte.login(username, password).json()
        token = login_data["token"]
        eleve_id = login_data["data"]["accounts"][0]["id"]

        message = ""
        cdt_data = ecoledirecte.cahier_de_texte(eleve_id, token, date).json()["data"]

        message += f"Devoirs à faire pour le {date}\n"
        for index in range(len(cdt_data["matieres"])):
            try:
                matiere = cdt_data["matieres"][index]["matiere"]
                texte = str_clean.clean(b64.decode_base64(cdt_data["matieres"][index]["aFaire"]["contenu"]))
                message += f"**{matiere}** : {texte}\n"
            except Exception:
                pass
        await contexte.send(message)

    else:
        await contexte.send("Vous n'êtes pas connecté! Utilisez !login <identifiant> <motdepasse>")

# Remerciements
@bot.command()
async def remerciements(contexte):
    message = "Merci à...\n"
    message += "**CreepinGenius (@redstonecreeper6)** : Aide et conseils (même s'il a pas voulu tester)"
    await contexte.send(message)

# Démarrer le bot
try:
    bot.run(token)
except discord.errors.LoginFailure:
    logging.error("Token invalide")


# classe_id = login_data["data"]["accounts"][0]["profile"]["classe"]["id"]