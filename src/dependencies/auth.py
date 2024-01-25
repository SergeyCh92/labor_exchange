from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_session
from src.services import AuthService


async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session=session)
