import logging

from fastapi import APIRouter, Depends, Response, status

from src.database.tables import User
from src.dependencies import get_current_user, get_job_service
from src.schemas.job import jobSchema
from src.services import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/job", response_class=Response)
async def create_job(
    job_schema: jobSchema,
    job_service: JobService = Depends(get_job_service),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"the job creation request was received from user id {job_schema.user_id}")
    await job_service.create_job(job_schema=job_schema, current_user=current_user)
    logging.info(f"the vacancy has been created, the owner is the user id {job_schema.user_id}")
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/jobs", response_model=list[jobSchema])
async def get_jobs(
    limit: int = 100,
    skip: int = 0,
    job_service: JobService = Depends(get_job_service),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"request was received to receive {limit} users, offset {skip}")
    results = await job_service.get_jobs(limit=limit, skip=skip)
    logging.info(f"{len(results)} users have been successfully received")
    return results


@router.get("/job/{id}", response_model=jobSchema)
async def get_job(
    id: int, job_service: JobService = Depends(get_job_service), current_user: User = Depends(get_current_user)
):
    logging.info(f"data on the {id} id job has been requested")
    job = await job_service.get_job(id=id)
    logging.info(f"the data on the job {id} id has been received")
    return job


@router.put("/job/{job_id}", response_class=Response)
async def update_job(
    job_id: int,
    job_schema: jobSchema,
    job_service: JobService = Depends(get_job_service),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"the request was received to update job id {job_id} data")
    await job_service.update_job(job_id=job_id, job_schema=job_schema, current_user=current_user)
    logging.info(f"the data of the job id {id} has been updated")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
