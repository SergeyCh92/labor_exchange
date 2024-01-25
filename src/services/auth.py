import hashlib

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.queries.user as user_queries
from src.core.security import create_access_token, create_refresh_token, verify_password
from src.database.tables import User
from src.schemas import LoginSchema, TokenSchema


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_token_schema(self, login: LoginSchema) -> TokenSchema:
        user = await user_queries.get_by_email(session=self.session, email=login.email)
        if user is None or not verify_password(login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль"
            )

        access_token, refresh_token = self.generate_tokens(user)
        await self.update_token_hash(refresh_token, user)
        return TokenSchema(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token_schema(self, refresh_token: str) -> TokenSchema:
        hashed_refresh_token = self.get_string_hash(refresh_token)
        user = await user_queries.get_user_by_hashed_refresh_token(
            session=self.session, hashed_refresh_token=hashed_refresh_token
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный refresh-токен")

        access_token, refresh_token = self.generate_tokens(user)
        await self.update_token_hash(refresh_token, user)
        return TokenSchema(access_token=access_token, refresh_token=refresh_token)

    async def update_token_hash(self, refresh_token: str, user: User):
        hashed_refresh_token = self.get_string_hash(refresh_token)
        user.hashed_refresh_token = hashed_refresh_token
        self.session.add(user)
        await self.session.commit()

    @staticmethod
    def generate_tokens(user: User) -> tuple[str, str]:
        data = {"sub": user.email}
        access_token = create_access_token(data)
        refresh_token = create_refresh_token()
        return access_token, refresh_token

    @staticmethod
    def get_string_hash(text: str) -> str:
        return hashlib.sha256(text.encode("UTF-8")).hexdigest()
