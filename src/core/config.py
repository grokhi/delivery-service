from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Delivery Service"
    DATABASE_URL: str
    REDIS_URL: str

    UPDATE_INTERVAL: int = 300
    CURRENCY_API_URL: str
    PARCEL_TYPES: List[str]
    SESSION_KEY: str = "sessionKey"
    LOG_LEVEL: str = "INFO"

    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str

    class Config:
        env_file = ".env"


settings = Settings()
