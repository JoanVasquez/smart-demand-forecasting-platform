import pandas as pd
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.sales_history.repository import HistoricalSaleRepository
from app.config.prophet_config import get_prophet_model


class ForecastService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def forecast_sales(self):
        repo = HistoricalSaleRepository(self.db)
        sales = await repo.findAll()

        if len(sales) < 2:
            return {"error": "Not enough data for forecasting. At least 2 records required."}

        df = pd.DataFrame([
            {"ds": s.sale_date, "y": s.quantity} for s in sales
        ])

        model = get_prophet_model()
        model.fit(df)

        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        return forecast.to_dict(orient="records")
