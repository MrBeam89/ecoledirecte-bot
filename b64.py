import base64
def decode_base64(b64_string:str)->str:
    bytes = b64_string.encode("utf-8")
    converted_bytes = base64.b64decode(bytes)
    decoded_str = converted_bytes.decode("utf-8")
    return decoded_str