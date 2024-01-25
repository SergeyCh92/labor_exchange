from pydantic import EmailStr

from src.schemas.base import BaseSchema


class TokenSchema(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class LoginSchema(BaseSchema):
    email: EmailStr
    password: str


class RefreshTokenSchema(BaseSchema):
    token: str
