#    EcoleDirecte Bot (keygen.py)
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

import yaml
from secrets import token_bytes

from config import CONFIG_FILENAME, ECOLEDIRECTE_DIR

def getkey()->bytes:
    # Obtenir le nom du fichier de la clé dans la config
    DB_KEY_FILENAME = None
    with open(f"{ECOLEDIRECTE_DIR}{CONFIG_FILENAME}", "r") as config_file:
        config = yaml.safe_load(config_file)
        DB_KEY_FILENAME = config["DB_KEY_FILENAME"]

    # Création/récupération de la clé
    try:
        # Ne modifie pas la clé si elle existe déjà
        keyfile = open(f"{ECOLEDIRECTE_DIR}{DB_KEY_FILENAME}", "rb")
    except FileNotFoundError:
        # Si la clé n'existe pas
        keyfile = open(f"{ECOLEDIRECTE_DIR}{DB_KEY_FILENAME}", "wb+")
        keyfile.write(token_bytes(32))
        keyfile.seek(0)
    finally:
        return keyfile.read(32)
