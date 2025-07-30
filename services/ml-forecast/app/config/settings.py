import os
from pydantic_settings import BaseSettings

ENV_FILE = os.getenv("ENV_FILE", ".env")


class Settings(BaseSettings):
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 5433

    KAFKA_BOOTSTRAP_SERVERS: str = ""
    KAFKA_GROUP_ID: str = ""
    SCHEMA_REGISTRY_URL: str = ""

    model_config = {
	"env_file": ENV_FILE,
	"extra": "allow"
    }

settings = Settings()

