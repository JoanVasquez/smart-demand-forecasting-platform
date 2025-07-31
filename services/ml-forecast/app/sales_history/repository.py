from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.sales_history.historical_sale import HistoricalSale
from app.create_sale_schema import HistoricalSaleCreate

class HistoricalSaleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self, historical_sale_schema: HistoricalSaleCreate) -> HistoricalSale:
        new_historical_sale = HistoricalSale(**historical_sale_schema.model_dump())
        self.db.add(new_historical_sale)
        await self.db.commit()
        await self.db.refresh(new_historical_sale)
        return new_historical_sale


    async def findAll(self) -> List[HistoricalSale]:
        result = await self.db.execute(select(HistoricalSale))
        return result.scalars().all()

