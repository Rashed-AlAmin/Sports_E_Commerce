from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List
from datetime import datetime

class OrderItemResponse(BaseModel):
    product_name: str
    product_price: float
    quantity: int
    subtotal: float

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)