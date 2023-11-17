# Bot EcoleDirecte pour Discord
# Par MrBeam89_

import discord
from discord.ext import commands
import logging
import ecoledirecte

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

# Au démarrage du bot
@bot.event
async def on_ready():
    logging.info("Bot pret!")

# Erreures générales
@bot.event
async def on_command_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await contexte.send("Commande invalide! Utilisez **!aide** pour afficher la liste des commandes disponibles")
        logging.info(f"Commande invalide de l'utilisateur {contexte.author.name}")

# Aide
@bot.command()
async def aide(contexte):
    aide_msg = '''**EcoleDirecte Bot** par Raticlette (@mrbeam89_)
EcoleDirecte dans Discord!
Commandes disponibles :
**!aide** : Ce message
**!login <identifiant> <motdepasse>** : Se connecter (test)
Envoyez-moi un MP en cas de souci!'''
    await contexte.send(aide_msg)

# Connexion
@bot.command()
async def login(contexte, username, password):
    await contexte.send("Veuillez patienter...")
    logging.info(f"Tentative d'authentification de l'utilisateur {contexte.author.name}")
    reponse = ecoledirecte.login(username, password)
    reponse_json = reponse.json()

    # Si identifiants corrects
    if reponse_json['code'] == 200:
        await contexte.send("Connexion réussie!")
        await contexte.send("Connecté en tant que :")

        nom = reponse_json["data"]["accounts"][0]["nom"]
        prenom = reponse_json["data"]["accounts"][0]["prenom"]
        classe = reponse_json["data"]["accounts"][0]["profile"]["classe"]["code"]
        await contexte.send(f"**Nom** : {nom}\n**Prénom** : {prenom}\n**Classe** : {classe}")
        logging.info(f"Authentification reussie de l'utilisateur {contexte.author.name} avec le compte de {nom} {prenom} {classe}")

    # Si identifiants incorrects
    if reponse_json['code'] == 505:
        logging.info(f"Echec de l'authentification de l'utilisateur {contexte.author.name}")
        await contexte.send("Identifiant et/ou mot de passe invalide!")

# Erreurs de !login
@login.error
async def login_error(contexte, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        logging.info(f"Syntaxe de !login invalide par l'utilisateur {contexte.author.name}")
        await contexte.send("Syntaxe invalide! : Utilisez !login <identifiant> <motdepasse>")

# Démarrer le bot
try:
    bot.run(token)
except discord.errors.LoginFailure:
    logging.error("Token invalide")
