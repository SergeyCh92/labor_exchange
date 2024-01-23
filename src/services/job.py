from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.queries.job as job_queries
from src.database.tables import Job, User
from src.schemas.job import JobSchema


class JobService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_job(self, job_schema: JobSchema, current_user: User):
        self.check_is_company(
            current_user.is_company, "Вы не можете обновлять вакансии, т.к. являетесь физическим лицом."
        )
        await job_queries.create_new_job(job_schema, self.session)

    async def get_jobs(self, limit: int, skip: int) -> list[Job]:
        results = await job_queries.get_all_jobs(session=self.session, limit=limit, skip=skip)
        return results

    async def get_job(self, id: int) -> Job:
        result = await job_queries.get_job_by_id(id=id, session=self.session)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена.")
        return result

    async def update_job(self, job_id: int, job_schema: JobSchema, current_user: User):
        self.check_is_company(
            current_user.is_company, "Вы не можете обновлять вакансии, т.к. являетесь физическим лицом."
        )
        self.check_is_owner(job_id, current_user.id, "Вы не можете обновлять вакансию, которая не является Вашей.")

        old_job = await job_queries.get_job_by_id(id=job_id, session=self.session, lock=True)

        if old_job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена.")
        await job_queries.update_job_by_id(session=self.session, old_job=old_job, new_job=job_schema)

    @staticmethod
    def check_is_company(is_company: bool, error_message: str):
        if not is_company:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)

    @staticmethod
    def check_is_owner(job_user_id: int, current_user_id: int, error_message: str):
        if job_user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)
