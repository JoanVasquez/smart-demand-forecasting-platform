import os
from pydantic_settings import BaseSettings

ENV_FILE = os.getenv("ENV_FILE", ".env")


class Settings(BaseSettings):
    ML_FORECAST_DB_NAME: str = ""
    ML_FORECAST_DB_USER: str = ""
    ML_FORECAST_DB_PASSWORD: str = ""
    ML_FORECAST_DB_HOST: str = ""
    ML_FORECAST_DB_PORT: int = 5432

    KAFKA_BROKER: str = ""
    ML_FORECAST_KAFKA_GROUP_ID: str = ""
    SCHEMA_REGISTRY_URL: str = ""

    REDIS_HOST: str = ""

    model_config = {
	    "env_file": ENV_FILE,
	    "extra": "allow"
    }

settings = Settings()

