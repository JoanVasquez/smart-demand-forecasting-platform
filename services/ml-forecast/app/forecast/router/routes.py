from fastapi import APIRouter
from app.forecast.controller import health
from app.forecast.controller import forecast_predictive

router = APIRouter()
router.include_router(health.router, tags=["Health"])
router.include_router(forecast_predictive.router, tags=["Forecast predictive"])

