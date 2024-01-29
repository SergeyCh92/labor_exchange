import pytest
from pydantic import ValidationError
from sqlalchemy import select

from fixtures.users import UserFactory
from queries import user as user_query
from schemas import UserInSchema, UpdateUserSchema
from src.database.tables import User


@pytest.mark.asyncio
async def test_get_all(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    all_users = await user_query.get_all_users(sa_session)
    assert all_users
    assert len(all_users) == 1
    assert all_users[0] == user


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    current_user = await user_query.get_by_id(user.id, sa_session)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_get_by_email(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    current_user = await user_query.get_by_email(sa_session, user.email)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserInSchema(
        name="Uchpochmak", email="bashkort@example.com", password="eshkere!", password2="eshkere!", is_company=False
    )

    await user_query.create(sa_session, user_schema=user)
    query = select(User).where(User.email == user.email)
    raw_created_user = await sa_session.execute(query)
    created_user = raw_created_user.scalar()
    assert created_user is not None
    assert created_user.name == "Uchpochmak"
    assert created_user.hashed_password != "eshkere!"


@pytest.mark.asyncio
async def test_create_password_mismatch(sa_session):
    with pytest.raises(ValidationError):
        user = UserInSchema(
            name="Uchpochmak", email="bashkort@example.com", password="eshkere!", password2="eshkero!", is_company=False
        )
        await user_query.create(sa_session, user_schema=user)


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    updated_user_schema = UpdateUserSchema(name="updated_name")
    updated_user = await user_query.update(sa_session, old_user=user, new_user=updated_user_schema)

    query = select(User).where(User.id == user.id)
    raw_updated_user = await sa_session.execute(query)
    updated_user = raw_updated_user.scalar()
    assert user.id == updated_user.id
    assert updated_user.name == "updated_name"
