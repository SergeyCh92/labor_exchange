from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import Response
from src.schemas import ResponseSchema


async def create_response(response_schema: ResponseSchema, session: AsyncSession):
    response = Response(job_id=response_schema.job_id, user_id=response_schema.user_id, message=response_schema.message)
    session.add(response)
    await session.commit()
