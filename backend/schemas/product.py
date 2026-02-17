from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0) # Price must be greater than 0

class ProductCreate(ProductBase):
    pass # Used for POST

class ProductResponse(ProductBase):
    id: UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True) # The Pydantic V2 way