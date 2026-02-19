from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Correcting imports based on your structure
from backend.crud.categories import create_category, get_categories, get_category
from backend.schemas.product import CategoryCreate, CategoryResponse
from backend.core.dependencies import get_db,get_current_admin

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
async def api_create_category(
    category: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin) # Only admins can POST
):
    return await create_category(db=db, category=category)

@router.get("/", response_model=List[CategoryResponse])
async def api_read_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
    # No admin dependency here so customers can see categories
):
    return await get_categories(db=db, skip=skip, limit=limit)