from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from app.config.db import Base


class HistoricalSale(Base):
    __tablename__: str = "historical_sales"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True, autoincrement=True)
    sale_id = Column(String(15), nullable=False, unique=True)
    product_id = Column(String(15), nullable=False)
    quantity= Column(Integer, nullable=False)
    sale_date = Column(DateTime, nullable=False)

