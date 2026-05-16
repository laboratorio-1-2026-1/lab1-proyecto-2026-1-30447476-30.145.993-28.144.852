from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartGym API"
    VERSION:      str = "1.0.0"
    API_V1_STR:   str = "/api/v1"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/smartgym_db"
    )
    SECRET_KEY:   str = os.getenv(
        "SECRET_KEY",
        "super-secret-key-smartgym-2026"
    )
    ALGORITHM:                  str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"


settings = Settings()