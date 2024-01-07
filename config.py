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
            
            config_file.close()

    except FileNotFoundError:
        print(f'"{CONFIG_FILENAME}" est introuvable!')
        input("Appuyez sur Entree pour quitter...")
        exit()

    # Vérification du fichier de token
    try:
        print(f'Ouverture du fichier "{BOT_TOKEN_FILENAME}"...')
        token_file = open(f"{BOT_TOKEN_FILENAME}", "r")
        print(f'Ouverture du fichier "{BOT_TOKEN_FILENAME} réussie!"')
        token_file.close()
    except FileNotFoundError:
        print(f"Fichier introuvable! Placer token dans le fichier {bot_token_file}")
        input("Appuyez sur Entree pour quitter...")
        exit()

    # Vérification du fichier de clé de DB
    try:
        print(f'Ouverture du fichier "{DB_KEY_FILENAME}"...')
        db_key_file = open(f"{DB_KEY_FILENAME}", "r")
        print(f'Ouverture du fichier "{DB_KEY_FILENAME}", réussie!')
        db_key_file.close()

    except FileNotFoundError:
        print(f"Fichier introuvable! Placer clé de DB dans le fichier {bot_token_file}")
        input("Appuyez sur Entree pour quitter...")

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
    
    # Renvoie la configuration
    print("Configuration valide!")
    return config
