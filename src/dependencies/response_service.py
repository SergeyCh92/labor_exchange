from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.services import ResponseService


async def get_response_service(session: AsyncSession = Depends(get_session)) -> ResponseService:
    return ResponseService(session=session)