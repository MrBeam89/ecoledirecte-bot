from secrets import token_bytes
def getkey()->bytes:
    try:
        # Ne modifie pas la clé si elle existe déjà
        keyfile = open("keyfile.bin", "rb")
    except FileNotFoundError:
        # Si la clé n'existe pas
        keyfile = open("keyfile.bin", "wb+")
        keyfile.write(token_bytes(32))
        keyfile.seek(0)
    finally:
        return keyfile.read(32)
