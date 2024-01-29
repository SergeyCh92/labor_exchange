from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.services import UserService


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session=session)
