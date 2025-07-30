import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tenacity import retry, wait_fixed, stop_after_delay
from dotenv import load_dotenv
from app.forecast.router.routes import router as v1_router
from app.config.db import engine, Base
from app.exceptions.handlers import add_exception_handlers


load_dotenv()


@retry(wait=wait_fixed(3), stop=stop_after_delay(30))
async def init_service():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_service()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="ML Forecast Service",
        version="1.0.0",
        lifespan=lifespan
    )

    app.include_router(v1_router, prefix="/api/v1")
    add_exception_handlers(app)

    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        workers=1
    )
