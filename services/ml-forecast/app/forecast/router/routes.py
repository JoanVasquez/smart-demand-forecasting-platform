from fastapi import APIRouter
from app.forecast.controller import health

router = APIRouter()
router.include_router(health.router, tags=["Health"])