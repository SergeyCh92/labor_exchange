from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.queries.job as job_queries
from src.database.tables import Job
from src.schemas import UserSchema
from src.schemas.job import JobSchema


class JobService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_job(self, job_schema: JobSchema, current_user: UserSchema):
        self.check_is_company(
            current_user.is_company, "Вы не можете обновлять вакансии, т.к. являетесь физическим лицом."
        )
        await job_queries.create_new_job(job_schema, self.session)

    async def get_jobs(self, limit: int, skip: int) -> list[Job]:
        results = await job_queries.get_all_jobs(session=self.session, limit=limit, skip=skip)
        return results

    async def get_job(self, id: int) -> Job:
        job = await job_queries.get_job_by_id(id=id, session=self.session)
        self.check_job_exists(job, "Выбранная Вами вакансия не существует.")
        return job

    async def update_job(self, job_id: int, job_schema: JobSchema, current_user: UserSchema):
        self.check_is_company(
            current_user.is_company, "Вы не можете обновлять вакансии, т.к. являетесь физическим лицом."
        )
        self.check_is_owner(
            job_schema.user_id, current_user.id, "Вы не можете обновлять вакансию, которая не является Вашей."
        )

        old_job = await job_queries.get_job_by_id(id=job_id, session=self.session, lock=True)
        self.check_job_exists(old_job, "Выбранная Вами вакансия не существует.")
        await job_queries.update_job_by_id(session=self.session, old_job=old_job, new_job=job_schema)

    async def delete_job(self, job_id: int, current_user: UserSchema):
        self.check_is_company(
            current_user.is_company, "Вы не можете обновлять вакансии, т.к. являетесь физическим лицом."
        )
        # можно не получать вакансию из базы и сразу удалить ее с условием, где совпадает id вакансии и
        # id пользователя, создавшего вакансию. экономим 1 запрос в базу, но с точки зрения UX, неплохо
        # явно сообщить об отсутствии фактического удаления данных

        job = await job_queries.get_job_by_id(id=job_id, session=self.session, lock=True)
        self.check_job_exists(job, "Выбранная Вами вакансия не существует.")
        self.check_is_owner(job.user_id, current_user.id, "У вас нет прав на удаление этой вакансии.")
        await job_queries.delete_job_by_id(job_id, self.session)

    @staticmethod
    def check_is_company(is_company: bool, error_message: str):
        if not is_company:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)

    @staticmethod
    def check_is_owner(job_user_id: int, current_user_id: int, error_message: str):
        if job_user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)

    @staticmethod
    def check_job_exists(job: Job | None, error_message: str):
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
