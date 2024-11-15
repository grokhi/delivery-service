from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Delivery Service"
    DATABASE_URL: str
    REDIS_URL: str
    CURRENCY_API_URL: str
    UPDATE_INTERVAL: int = 300
    SECRET_KEY: str
    DEBUG: bool
    PARCEL_TYPES: List[str]
    SESSION_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
