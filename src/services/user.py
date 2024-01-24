from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.queries.user as user_queries
from src.database.tables import User
from src.schemas import updateUserSchema, userInSchema


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self, limit: int, skip: int) -> list[User]:
        results = await user_queries.get_all_users(session=self.session, limit=limit, skip=skip)
        return results

    async def create_user(self, user_schema: userInSchema):
        await user_queries.create(session=self.session, user_schema=user_schema)

    async def update_user(self, user_id: int, current_user: User, update_user_schema: updateUserSchema):
        old_user = await user_queries.get_by_id(session=self.session, id=user_id, lock=True)
        self.check_user_is_correct(old_user=old_user, current_user=current_user)
        await user_queries.update(session=self.session, old_user=old_user, new_user=update_user_schema)

    async def get_user(self, user_id: int) -> User:
        user = await user_queries.get_by_id(session=self.session, id=user_id)
        self.check_user_is_correct(old_user=user)
        return user

    @staticmethod
    def check_user_is_correct(old_user: User | None, current_user: User | None = None):
        raise_exception = False
        if not old_user:
            raise_exception = True
        elif current_user:
            raise_exception = True if old_user.email != current_user.email else False
        if raise_exception:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
