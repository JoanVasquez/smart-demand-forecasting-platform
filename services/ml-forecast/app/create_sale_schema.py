from pydantic import BaseModel
from datetime import datetime


class HistoricalSaleCreate(BaseModel):
    sale_id: str
    product_id: str
    quantity: int
    sale_date: datetime
