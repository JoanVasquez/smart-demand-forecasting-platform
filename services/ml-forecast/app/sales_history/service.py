from app.sales_history.repository import HistoricalSaleRepository
from app.create_sale_schema import HistoricalSaleCreate
from app.exceptions.types import DatabaseError
from sqlalchemy.exc import SQLAlchemyError


class HistoricalSaleService:
    def __init__(self, repo: HistoricalSaleRepository):
        self.repo = repo

    async def create_historical_sale(self, sale_data: HistoricalSaleCreate):
        try:
            new_sale = await self.repo.create(sale_data)
            return new_sale
        except SQLAlchemyError as exc:
            raise DatabaseError("Error inserting historical sale into database") from exc

