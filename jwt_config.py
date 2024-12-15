from jwt import encode, decode

def generar_token(dato: dict)->str:
    encode_token: str = encode(payload=dato, key='zenpassw0rd', algorithm='HS256')
    return encode_token

def validar_token(token: str)->dict:
    decode_token = decode(token, key = 'zenpassw0rd', algorithms=['HS256'])
    return decode_token
