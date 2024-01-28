import asyncio
import datetime
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import src.core.security as security
from src.database.engine import Base, engine
from src.dependencies import get_auth_service, get_job_service, get_response_service
from src.fixtures import JobFactory, ResponseFactory, UserFactory
from src.main import app
from src.queries import user as user_queries
from src.schemas import ResponseCreateSchema, ResponseSchema, UpdateUserSchema, UserInSchema, UserSchema, JobSchema
from src.services import AuthService, JobService, ResponseService
from src.settings import DataBaseSettings, SecuritySettings

settings = DataBaseSettings()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def job_schema() -> JobSchema:
    return JobSchema(user_id=1, title="test_title")


@pytest.fixture
def response_schema() -> ResponseSchema:
    return ResponseSchema(id=0, job_id=1, user_id=2, message="test_message")


@pytest.fixture
def response_create_schema() -> ResponseCreateSchema:
    return ResponseCreateSchema(job_id=1)


@pytest.fixture
def update_user_schema() -> UpdateUserSchema:
    return UpdateUserSchema(name="test_name_2")


@pytest.fixture
def user_in_schema() -> UserInSchema:
    return UserInSchema(
        name="test_user", email="test@example.com", is_company=True, password="12345678", password2="12345678"
    )


@pytest.fixture
def user_schema() -> UserSchema:
    return UserSchema(
        id=1, name="test_user", email="test@example.com", is_company=True, created_at=datetime.datetime.utcnow()
    )


# мокаем авторизацию для тестов
@pytest.fixture
def auth_token(monkeypatch):
    async def mock_query(*args, **kwargs):
        return UserSchema(
            id=1, name="test_user", email="test@example.com", is_company=True, created_at=datetime.datetime.utcnow()
        )

    async def mock_jwt(*args, **kwargs):
        return {"sub": "test@example.com", "exp": 1706474902}

    monkeypatch.setattr(security.JWTBearer, "__call__", mock_jwt)
    monkeypatch.setattr(user_queries, "get_by_email", mock_query)
    return {"accessToken": "test_token"}


# предполагается использование тестовой базы, т.е. тесты не проводятся на базе,
# которая используется для разработки
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="module")
async def auth_service() -> AuthService:
    return await get_auth_service()


@pytest_asyncio.fixture(scope="module")
async def job_service() -> JobService:
    return await get_job_service()


@pytest_asyncio.fixture(scope="module")
async def response_service() -> ResponseService:
    return await get_response_service()


@pytest.fixture
def security_settings() -> SecuritySettings:
    return SecuritySettings()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture
async def sa_session():
    engine = create_async_engine(settings.dsn)
    connection = await engine.connect()
    trans = await connection.begin()

    session_factory = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = session_factory()

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
def setup_factories(sa_session: AsyncSession):
    UserFactory.session = sa_session
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session
