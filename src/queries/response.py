from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import Response
from src.schemas import ResponseCreateSchema


async def get_responses(job_id: int, user_id: int, session: AsyncSession) -> list[Response]:
    query = select(Response).where((Response.job_id == job_id) & (Response.user_id == user_id))
    row_results = await session.execute(query)
    results = row_results.scalars().all()
    return results


async def create_response(response_schema: ResponseCreateSchema, user_id: int, session: AsyncSession):
    response = Response(job_id=response_schema.job_id, user_id=user_id, message=response_schema.message)
    session.add(response)
    await session.commit()
