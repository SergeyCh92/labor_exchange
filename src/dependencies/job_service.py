from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_session
from src.services import JobService


async def get_job_service(session: AsyncSession = Depends(get_session)) -> JobService:
    return JobService(session=session)
