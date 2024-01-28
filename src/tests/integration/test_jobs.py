import pytest
from sqlalchemy import select

import src.queries.job as job_query
from src.database.tables import Job
from src.fixtures import JobFactory, UserFactory


@pytest.mark.asyncio
async def test_get_all(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()

    all_jobs = await job_query.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job


@pytest.mark.asyncio
async def test_get_job_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()

    current_job = await job_query.get_job_by_id(job.id, sa_session)
    assert current_job is not None
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_delete_job_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()

    await job_query.delete_job_by_id(job.id, sa_session)

    query = select(Job).where(Job.id == job.id)
    raw_deleted_job = await sa_session.execute(query)
    deleted_job = raw_deleted_job.scalar()

    assert deleted_job is None
