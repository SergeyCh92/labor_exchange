from src.schemas.base import BaseSchema


class ResponseCreateSchema(BaseSchema):
    id: int | None = None
    job_id: int
    message: str | None = None


class ResponseSchema(ResponseCreateSchema):
    user_id: int
