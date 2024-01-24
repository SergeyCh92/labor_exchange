from pydantic import EmailStr

from src.schemas.base import BaseSchema


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


class LoginSchema(BaseSchema):
    email: EmailStr
    password: str
