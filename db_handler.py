import sqlite3

# Ajouter le token d'un nouvel utilisateur
def add_token(user_id:int, token:bytes)->bool:
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    try:
        new_user = (cursor.lastrowid, user_id, token)
        cursor.execute("INSERT INTO users VALUES (?,?,?)", new_user)
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        connection.rollback()
        connection.close()
        return False

# Obtenir le token d'un utilisateur
def fetch_token(user_id:int)->bytes:
    user_id = (user_id,)
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", user_id)
    user_data = cursor.fetchone()
    if user_data:
        token = user_data[2]
        connection.close()
        return token
    else:
        connection.close()
        return b''

