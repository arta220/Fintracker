from datetime import datetime, timedelta, UTC
import jwt

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"

def generate_token(user_id: int, token_type) ->str:
    now = datetime.now(UTC)
    if token_type == "access":
        expire = now + timedelta(hours=100)
    elif token_type == "refresh":
        expire = now + timedelta(hours=100)
    else:
        expire = now + timedelta(hours=100)
    payload = {
        "sub":str(user_id),
        "iat":now,
        "type":token_type,
        "exp":expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token:str) -> dict:
    payload=jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return payload

#todo: secret key generator
#def get_jwt_secret_key()

