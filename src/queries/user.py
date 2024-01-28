from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import hash_password
from src.database.tables import User
from src.schemas import UpdateUserSchema, UserInSchema


async def get_all_users(session: AsyncSession, limit: int = 100, skip: int = 0) -> list[User]:
    query = select(User).limit(limit).offset(skip)
    results = await session.execute(query)
    return results.scalars().all()


async def get_by_id(id: int, session: AsyncSession, lock: bool = False) -> User | None:
    query = select(User).where(User.id == id)
    if lock:
        query = query.with_for_update(nowait=False)
    result = await session.execute(query)
    return result.scalar()


async def create(session: AsyncSession, user_schema: UserInSchema):
    user = User(
        name=user_schema.name,
        email=user_schema.email,
        hashed_password=hash_password(user_schema.password),
        is_company=user_schema.is_company,
    )
    session.add(user)
    # в данной случае предлагаю отказаться от рефреша, т.к. он порождает дополнительный запрос в базу,
    # при уровне изолированности read committed и выше, до фиксации данные недоступны для чтения другим транзакциями,
    # следовательно не могут быть изменены
    await session.commit()


async def update(session: AsyncSession, old_user: User, new_user: UpdateUserSchema):
    old_user.name = new_user.name if new_user.name is not None else old_user.name
    old_user.email = new_user.email if new_user.email is not None else old_user.email
    old_user.is_company = new_user.is_company if new_user.is_company is not None else old_user.is_company

    session.add(old_user)
    await session.commit()


async def get_by_email(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user


async def get_user_by_hashed_refresh_token(session: AsyncSession, hashed_refresh_token: str) -> User | None:
    query = select(User).where(User.hashed_refresh_token == hashed_refresh_token)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user


async def delete_user_by_id(session: AsyncSession, user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()
