from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.future import select

# Correcting imports based on your structure
from backend.crud.categories import create_category, get_categories
from backend.schemas.product import CategoryCreate, CategoryResponse,CategoryUpdate
from backend.core.dependencies import get_db,get_current_admin
from backend.models.product import Category 

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

@router.get("/{category_id}", response_model=CategoryResponse)
async def api_get_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category

# UPDATE Category
@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, 
    category_data: CategoryUpdate, 
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin)
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_data.name is not None:
        category.name = category_data.name

    await db.commit()
    await db.refresh(category)
    return category

# DELETE Category
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin)
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(category)
    await db.commit()
    return None