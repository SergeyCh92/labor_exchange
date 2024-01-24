from pydantic import BaseModel


class responseSchema(BaseModel):
    id: int
    job_id: int
    user_id: int
    message: str | None = None
