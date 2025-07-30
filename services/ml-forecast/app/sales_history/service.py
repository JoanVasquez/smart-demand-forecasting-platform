from app.sales_history.repository import HistoricalSaleRepository
# from app.create_sale_schema import HistoricalSaleCreate


class HistoricalSaleService:
    def __init__(self, repo: HistoricalSaleRepository):
        self.repo = repo

    async def create_historical_sale(self):
        return None
