import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from app.forecast.router.routes import router as v1_router

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="ML Forecast Service", version="1.0.0")
    app.include_router(v1_router, prefix="/api/v1")

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
