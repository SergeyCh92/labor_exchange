from pydantic import BaseModel, EmailStr


class tokenSchema(BaseModel):
    access_token: str
    token_type: str


class loginSchema(BaseModel):
    email: EmailStr
    password: str
