#    EcoleDirecte Bot (config.py)
#    Copyright (C) 2023-2024 MrBeam89_
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

import yaml
import re

CONFIG_FILENAME = "config.yaml"

def get_config():
    # Vérification fichier de configuration
    try:
        print(f'Ouverture du fichier "{CONFIG_FILENAME}"...')
        with open(f"{CONFIG_FILENAME}", "r") as config_file:
            config = yaml.safe_load(config_file)
            print(f'Ouverture de "{CONFIG_FILENAME}" réussie!')
            BOT_TOKEN_FILENAME = config["BOT_TOKEN_FILENAME"]
            DB_KEY_FILENAME = config['DB_KEY_FILENAME']
            DB_FILENAME = config["DB_FILENAME"]
            BOT_COMMAND_PREFIX = config["BOT_COMMAND_PREFIX"]
            LOGGING_LEVEL = config["LOGGING_LEVEL"]
            COOLDOWN = config["COOLDOWN"]
            EMBED_COLOR = config["EMBED_COLOR"]

            config_file.close()

    except FileNotFoundError:
        print(f'"{CONFIG_FILENAME}" est introuvable!')
        input("Appuyez sur Entree pour quitter...")
        exit()

    # Vérification du fichier de token
    try:
        print(f'Ouverture du fichier "{BOT_TOKEN_FILENAME}"...')
        token_file = open(f"{BOT_TOKEN_FILENAME}", "r")
        print(f'Ouverture du fichier "{BOT_TOKEN_FILENAME}" réussie!')
        token_file.close()
    except FileNotFoundError:
        print(f'Fichier introuvable! Placez le token dans le fichier "{BOT_TOKEN_FILENAME}"')
        input("Appuyez sur Entree pour quitter...")
        exit()

    # Vérification du fichier de clé pour la base de données
    try:
        print(f'Ouverture du fichier "{DB_KEY_FILENAME}"...')
        db_key_file = open(f"{DB_KEY_FILENAME}", "r")
        print(f'Ouverture du fichier "{DB_KEY_FILENAME}", réussie!')
        db_key_file.close()

    except FileNotFoundError:
        from keygen import getkey
        print(f'Fichier introuvable! Création d\'une nouvelle clé dans le fichier "{DB_KEY_FILENAME}"...')
        getkey()
        print(f'Création d\'une nouvelle clé dans le fichier "{DB_KEY_FILENAME}" réussie!')
        print("/!\ ATTENTION /!\ La base de données (si non vide) ne fonctionnera pas correctement avec la nouvelle clé.")

    # Vérification du fichier de la base de données
    try:
        print(f'Ouverture du fichier "{DB_FILENAME}"...')
        db_key_file = open(f"{DB_FILENAME}", "r")
        print(f'Ouverture du fichier "{DB_FILENAME}" réussie!')
        db_key_file.close()

    except FileNotFoundError:
        print(f'Fichier introuvable! Création de la base de données "{DB_FILENAME}"...')

    # Vérification du préfixe du bot
    if not isinstance(BOT_COMMAND_PREFIX, str):
        print("Préfixe de commande de bot invalide!")
        input("Appuyez sur Entree pour quitter...")
        exit()
    else:
        print("Préfixe de commande de bot valide!")

    # Vérification du niveau de journalisation
    if not isinstance(LOGGING_LEVEL, int):
        print("Niveau de journalisation invalide!")
        input("Appuyez sur Entree pour quitter...")
        exit()
    else:
        print("Niveau de journalisation valide!")

    # Vérification du cooldown
    if not isinstance(COOLDOWN, int):
        print("Cooldown invalide!")
        input("Appuyez sur Entree pour quitter...")
        exit()
    else:
        print("Cooldown valide!")

    # Vérification de la couleur de l'embed
    if not isinstance(EMBED_COLOR, int):
        print("Couleur de l'embed invalide!")
        input("Appuyez sur Entree pour quitter...")
        exit()
    else:
        # Vérifie si le format 0x?????? est respecté (ignore les zéros en trop)
        hex_str = format(EMBED_COLOR, '06x')
        if len(hex_str) != 6:
            print("Couleur de l'embed invalide!")
            input("Appuyez sur Entree pour quitter...")
            exit()

        else:
            # Vérifie si le code couleur est valide
            r = int(hex_str[0:2], 16)
            v = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            if 0 <= r <= 255 and 0 <= v <= 255 and 0 <= b <= 255:
                print("Couleur de l'embed valide!")
            else:
                print("Couleur de l'embed invalide!")
                input("Appuyez sur Entree pour quitter...")
                exit()

    # Renvoie la configuration
    print("Configuration valide!")
    return config
