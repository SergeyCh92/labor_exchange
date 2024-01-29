import logging

import uvicorn
from fastapi import APIRouter, FastAPI

from src.routers import auth_router, job_router, response_router, user_router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - PID:%(process)d - threadName:%(thread)d - %(message)s"
)

router_healthcheck = APIRouter(tags=["Health"])


@router_healthcheck.get("/")
def health_check():
    return {"status": "labor_exchange is healthy"}


app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(job_router)
app.include_router(response_router)
app.include_router(router_healthcheck)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
