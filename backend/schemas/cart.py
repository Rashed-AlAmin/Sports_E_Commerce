from pydantic import BaseModel, ConfigDict, computed_field
from uuid import UUID
from typing import List
from .product import ProductResponse # Import your existing ProductResponse

class CartItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    product: ProductResponse # This pulls in the full product details

    model_config = ConfigDict(from_attributes=True)

class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemResponse]

    @computed_field
    @property
    def total(self) -> float:
        return sum(item.product.price * item.quantity for item in self.items)

    model_config = ConfigDict(from_attributes=True)