from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config.settings import settings
from contextlib import asynccontextmanager


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.ML_FORECAST_DB_USER}:{settings.ML_FORECAST_DB_PASSWORD}@"
    f"{settings.ML_FORECAST_DB_HOST}:{settings.ML_FORECAST_DB_PORT}/{settings.ML_FORECAST_DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# @asynccontextmanager
async def get_db():
    async with async_session() as session:
        yield session
