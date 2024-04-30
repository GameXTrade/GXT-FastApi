from fastapi import Depends
from app.operations.token import check_request_token, Token
from functools import wraps
from passlib.context import CryptContext

md5_crypt_context = CryptContext(schemes=[ "md5_crypt"])


def generate_hash_password(password):
    return md5_crypt_context.hash(password)

def verify_password(plain, hashed) -> bool:
    return md5_crypt_context.verify(plain, hashed)


def authenticate_route(func):
    @wraps(func)
    async def wrapper(*args, token_data: Token = Depends(check_request_token), **kwargs):
        # Führe hier deine Authentifizierungslogik aus, z.B. Zugriffsberechtigungen überprüfen
        # Du kannst auch auf token_data zugreifen, um auf Benutzerinformationen zuzugreifen
        return await func(*args, **kwargs)
    return wrapper