from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    # ADD THIS: So the database knows which category it belongs to
    category_id: Optional[int] = None 

class ProductCreate(ProductBase):
    pass 

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProductResponse(ProductBase):
    id: UUID
    is_active: bool
    category_id: Optional[int] = None
    # NEW: This nests the category details inside the product response
    category: Optional[CategoryResponse] = None 

    model_config = ConfigDict(from_attributes=True)