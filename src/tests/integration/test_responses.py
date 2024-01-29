import pytest
from sqlalchemy import select

import src.queries.response as response_query
from src.database.tables import Response
from src.fixtures import JobFactory, ResponseFactory, UserFactory
from src.schemas import ResponseCreateSchema


@pytest.mark.asyncio
async def test_get_all_responses(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()

    response = ResponseFactory.build(user_id=user.id, job_id=job.id)
    sa_session.add(response)
    await sa_session.flush()

    all_responses = await response_query.get_responses(job.id, user.id, sa_session)
    assert all_responses
    assert len(all_responses) == 1
    assert all_responses[0] == response
    assert all_responses[0].message == response.message


@pytest.mark.asyncio
async def test_create_responses(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()

    response_schema = ResponseCreateSchema(job_id=job.id, message="test_message")

    await response_query.create_response(response_schema, user.id, sa_session)

    query = select(Response).where(Response.user_id == user.id)
    raw_created_response = await sa_session.execute(query)
    created_response = raw_created_response.scalar()

    assert created_response is not None
    assert created_response.job_id == response_schema.job_id
    assert created_response.message == response_schema.message
