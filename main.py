# Bot EcoleDirecte pour Discord
# Par MrBeam89_

import discord
from discord.ext import commands
import ecoledirecte

# Paramètres
# PLACER TOKEN DANS LE FICHIER token.txt
bot = commands.Bot(command_prefix="!", description="Bot EcoleDirecte", intents=discord.Intents.all())
try:
    token_file = open("token.txt", "r")
    token = token_file.read()
except FileNotFoundError:
    print("FICHIER INTROUVABLE : Placer le token dans le fichier token.txt")

# Au démarrage du bot
@bot.event
async def on_ready():
    print("Bot prêt!")

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

    # Si identifiants incorrects
    if reponse_json['code'] == 505:
        await contexte.send("Identifiant et/ou mot de passe invalide!")

# Démarrer le bot
bot.run(token)
