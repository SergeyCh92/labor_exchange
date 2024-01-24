from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import Response
from src.schemas import ResponseCreateSchema


async def create_response(response_schema: ResponseCreateSchema, user_id: int, session: AsyncSession):
    response = Response(job_id=response_schema.job_id, user_id=user_id, message=response_schema.message)
    session.add(response)
    await session.commit()
