from src.schemas.base import BaseSchema


class JobSchema(BaseSchema):
    id: int | None = None
    user_id: int
    title: str | None = None
    description: str = None
    salary_from: float | None = None
    salary_to: float | None = None
    is_active: bool = True
