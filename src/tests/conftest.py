import asyncio
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from fixtures.users import UserFactory
from main import app
from src.dependencies import get_auth_service, get_job_service, get_response_service
from src.services import AuthService, JobService, ResponseService
from src.settings import DataBaseSettings, SecuritySettings

settings = DataBaseSettings()


@pytest_asyncio.fixture
async def auth_service() -> AuthService:
    return await get_auth_service()


@pytest_asyncio.fixture
async def job_service() -> JobService:
    return await get_job_service()


@pytest_asyncio.fixture
async def response_service() -> ResponseService:
    return await get_response_service()


@pytest.fixture
def security_settings() -> SecuritySettings:
    return SecuritySettings()


@pytest.fixture
def client_app():
    client = TestClient(app)
    return client


@pytest_asyncio.fixture
async def sa_session():
    engine = create_async_engine(settings.dsn)  # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    async def mock_delete(instance):
        session.expunge(instance)
        return await asyncio.sleep(0)

    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()


# регистрация фабрик
@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session
