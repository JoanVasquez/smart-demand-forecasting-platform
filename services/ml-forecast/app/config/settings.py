import os
from pydantic_settings import BaseSettings

ENV_FILE = os.getenv("ENV_FILE", ".env")


class Settings(BaseSettings):
    ENV: str = ""
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT = 5432

    KAFKA_BOOTSTRAP_SERVERS: str = ""
    KAFKA_GROUP_ID: str = "fastapi-consumer-group"
    SCHEMA_REGISTRY_URL: str = ""

    class Config:
        env_file = ENV_FILE

settings = Settings()

