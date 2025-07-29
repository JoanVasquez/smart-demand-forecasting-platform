from pydantic import BaseModel

class HistoricalSaleCreate(BaseModel):
    sale_id: str
    product_id: str
    quantity: int
    sale_date: str
