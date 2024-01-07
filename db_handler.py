#    EcoleDirecte Bot (db_handler).py)
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

import sqlite3
import yaml

from ecoledirecte import login
from aes import *
from keygen import *

from config import CONFIG_FILENAME

# Obtenir le nom de la base de données
config_file = open(f"{CONFIG_FILENAME}", "r")
config = yaml.safe_load(config_file)
DB_FILENAME = config["DB_FILENAME"]

# Créer la base de données et ajouter la table si elle n'existe pas
connection = sqlite3.connect(f"{DB_FILENAME}")
cursor = connection.cursor()
create_table_sql = '''
CREATE TABLE IF NOT EXISTS users (
    db_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    identifiant BLOB,
    motdepasse BLOB
);
'''
cursor.execute(create_table_sql)
connection.commit()
connection.close()

# Ajouter les informations d'un nouvel utilisateur
def add_user_info(user_id:int, identifiant:str, motdepasse:str)->bool:
    connection = sqlite3.connect(f"{DB_FILENAME}")
    cursor = connection.cursor()
    try:
        new_user = (cursor.lastrowid, user_id, identifiant, motdepasse)
        cursor.execute("INSERT INTO users VALUES (?,?,?,?)", new_user)
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        connection.rollback()
        connection.close()
        return False

# Obtenir les informations d'un utilisateur
def fetch_user_info(user_id:int):
    connection = sqlite3.connect(f"{DB_FILENAME}")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        connection.close()
        return user_data
    else:
        connection.close()
        return ()

# Supprimer l'utilisateur
def delete_user(user_id:int)->bool:
    if fetch_user_info(user_id):
        connection = sqlite3.connect(f"{DB_FILENAME}")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        connection.commit()
        connection.close()
        return True
    else:
        return False
