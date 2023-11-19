import sqlite3
from ecoledirecte import login
from aes import *
from keygen import *

# Ajouter les informations d'un nouvel utilisateur
def add_user_info(user_id:int, identifiant:str, motdepasse:str)->bool:
    connection = sqlite3.connect("db.sqlite3")
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
    connection = sqlite3.connect("db.sqlite3")
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
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        connection.commit()
        connection.close()
        return True
    else:
        return False
