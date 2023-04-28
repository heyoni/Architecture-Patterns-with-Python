from database import Base
from sqlalchemy import Column, Integer, String
from typing import Optional
from datetime import date


class OrderLine(Base):
    order_id = Column(String(20), nullable=False)
    sku = Column(String(50), nullable=False)
    qty = Column(Integer, nullable=False)


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.refrence = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine) -> None:
        self.available_quantity -= line.qty

    def can_allocate(self, line) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
    