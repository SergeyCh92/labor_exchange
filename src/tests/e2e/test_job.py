import datetime

import pytest

import src.services as services
from src.database.tables import Job
from src.schemas import JobSchema
from tests.utils import convert_data_to_model


@pytest.mark.asyncio
async def test_get_job(monkeypatch, client, auth_token):
    async def mock_get_job(*args, **kwargs):
        return Job(
            id=0,
            user_id=1,
            title="test_title",
            description="test",
            salary_from=0,
            salary_to=100,
            is_active=True,
            created_at=datetime.datetime.utcnow(),
        )

    monkeypatch.setattr(services.JobService, "get_job", mock_get_job)
    response = await client.get("/jobs/job/1", headers=auth_token)
    assert response.status_code == 200
    data = convert_data_to_model(response.text, JobSchema)
    assert data.title == "test_title"


@pytest.mark.asyncio
async def test_create_job(monkeypatch, client, auth_token, job_schema):
    async def mock_create_job(*args, **kwargs):
        ...

    monkeypatch.setattr(services.JobService, "create_job", mock_create_job)
    response = await client.post("/jobs/job", headers=auth_token, data=job_schema.json())
    assert response.status_code == 201
