#    EcoleDirecte Bot (aes.py)
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

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Encrypter le token
def encrypt_aes(token:str, key:bytes)->bytes:
    # Convertir le token en octet
    token = token.encode('utf-8')

    # S'assurer que le token est un multiple de 16 (taille du bloc AES)
    padder = padding.PKCS7(128).padder()
    # Encoder le token en octets avant le remplissage
    padded_data = padder.update(token) + padder.finalize()

    # Encrypter le token en utilisant AES-256 en mode CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_token = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_token

# Décrypter le token encrypté
def decrypt_aes(encrypted_token:bytes, key:bytes)->str:
    # Décrypter le token en utilisant AES-256 en mode CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\0' * 16), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_token) + decryptor.finalize()

    # Décompacter les données décryptées
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Retorune le token décrypté en chaîne de caractères
    return unpadded_data.decode("utf-8")
