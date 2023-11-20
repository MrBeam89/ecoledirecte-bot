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

# Encrypt the token
def encrypt_aes(token:str, key:bytes)->bytes:
    # Convert token to bytes
    token = token.encode('utf-8')

    # Ensure the token is a multiple of 16 (AES block size)
    padder = padding.PKCS7(128).padder()
    # Encode the token to bytes before padding
    padded_data = padder.update(token) + padder.finalize()

    # Encrypt the token using AES-256 in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_token = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_token

# Decrypt the encrypted token
def decrypt_aes(encrypted_token:bytes, key:bytes)->str:
    # Decrypt the token using AES-256 in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\0' * 16), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_token) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Return the decrypted token as a string
    return unpadded_data.decode("utf-8")
