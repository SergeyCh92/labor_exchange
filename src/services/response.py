from fastapi import HTTPException, status
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession

import src.queries.response as response_queries
from src.database.tables import User
from src.schemas import ResponseCreateSchema, ResponseSchema, UserSchema


class ResponseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_response(self, response_schema: ResponseCreateSchema, current_user: User):
        self.check_is_company(
            current_user.is_company, "Вы не можете откликнуться на вакансию, т.к. зарегистрированы как работодатель."
        )
        await response_queries.create_response(
            response_schema=response_schema, user_id=current_user.id, session=self.session
        )

    async def get_responses(self, job_id: int, user_schema: UserSchema) -> list[ResponseSchema]:
        self.check_is_user(
            user_schema.is_company, "Вы не можете откликнуться на вакансию, т.к. зарегистрированы как физическое лицо."
        )
        responses = await response_queries.get_responses(job_id=job_id, user_id=user_schema.id, session=self.session)
        return parse_obj_as(list[ResponseSchema], responses)

    @staticmethod
    def check_is_company(is_company: bool, error_message: str):
        if is_company:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)

    @staticmethod
    def check_is_user(is_company: bool, error_message: str):
        if not is_company:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)
