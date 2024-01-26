import datetime

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from src.settings.security import SecuritySettings

settings = SecuritySettings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.token_expire_minutes)})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token() -> str:
    to_encode = {}
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(days=settings.refresh_token_expire_days)})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict[str, str | int] | None:
    try:
        encoded_jwt = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.JWSError:
        encoded_jwt = None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict[str, str | int]:
        credentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
        if credentials:
            token_data = decode_token(credentials.credentials)
            if token_data is None:
                raise exp
            return token_data
        else:
            raise exp
