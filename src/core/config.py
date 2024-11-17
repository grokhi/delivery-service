from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Delivery Service"
    DATABASE_URL: str
    REDIS_URL: str
    MONGO_URL: str

    REDIS_UPDATE_INTERVAL: int = 300
    MONGO_UPDATE_INTERVAL: int = 86400  # 60 * 60 * 24
    MONGO_EXPIRE_AT: int = 10  # days
    CURRENCY_API_URL: str
    PARCEL_TYPES: List[str]
    SERVICES_TYPES: List[str]
    SESSION_KEY: str = "sessionKey"
    LOG_LEVEL: str = "INFO"

    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str

    class Config:
        env_file = ".env"


settings = Settings()
