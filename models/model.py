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
        self._purchased_quantity = qty
        self._allocations = set()

    def allocate(self, line: OrderLine) -> None:
        self.available_quantity -= line.qty

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
    