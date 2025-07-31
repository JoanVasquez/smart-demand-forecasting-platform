from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db import get_db
from app.forecast.service.forecast_service import ForecastService
from typing import List


router = APIRouter()


@router.get("/forecast", summary="Forecast predictive")
async def forecast_sales(db: AsyncSession = Depends(get_db)):
    service = ForecastService(db)
    forecast_result = await service.forecast_sales()
    return forecast_result

