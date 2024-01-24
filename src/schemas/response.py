from src.schemas.base import BaseSchema


class ResponseSchema(BaseSchema):
    id: int
    job_id: int
    user_id: int
    message: str | None = None
