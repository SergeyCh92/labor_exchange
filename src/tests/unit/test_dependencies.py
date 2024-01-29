import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_auth_service, get_job_service, get_response_service, get_session, get_user_service
from src.services import AuthService, JobService, ResponseService, UserService


@pytest.mark.asyncio
async def test_get_auth_service():
    auth_service = await get_auth_service()
    assert isinstance(auth_service, AuthService)


@pytest.mark.asyncio
async def test_get_job_service():
    job_service = await get_job_service()
    assert isinstance(job_service, JobService)


@pytest.mark.asyncio
async def test_get_response_service():
    response_service = await get_response_service()
    assert isinstance(response_service, ResponseService)


@pytest.mark.asyncio
async def test_get_session():
    session = await anext(get_session())
    assert isinstance(session, AsyncSession)


@pytest.mark.asyncio
async def test_get_user_service():
    user_service = await get_user_service()
    assert isinstance(user_service, UserService)
