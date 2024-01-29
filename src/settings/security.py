from pydantic import BaseSettings, Field


class SecuritySettings(BaseSettings):
    token_expire_minutes: int = Field(env="TOKEN_EXPIRE_MINUTES", default=60)
    refresh_token_expire_days: int = Field(env="REFRESH_TOKEN_EXPIRE_DAYS", default=1)
    algorithm: str = Field(env="ALGORITHM", default="HS256")
    secret_key: str = Field(env="SECRET_KEY")
