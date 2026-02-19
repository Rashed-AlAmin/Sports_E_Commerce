from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from backend.models.product import Product
from backend.schemas.product import ProductCreate, ProductResponse
from backend.core.dependencies import get_db, get_current_admin
from typing import List,Optional

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,  # NEW: Optional filter parameter
    db: AsyncSession = Depends(get_db)
):
    # Start the base query
    query = select(Product).options(joinedload(Product.category)).where(Product.is_active == True)

    # NEW: If the user provided a category_id, add a filter to the query
    if category_id:
        query = query.where(Product.category_id == category_id)

    result = await db.execute(
        query.offset(skip).limit(limit)
    )

    return result.scalars().all()


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):

    new_product = Product(**product_data.model_dump())

    db.add(new_product)

    await db.commit()
    await db.refresh(new_product)

    return new_product


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):

    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(404, "Product not found")

    product.is_active = False

    await db.commit()

    return {"message": "Product deleted"}


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # Convert string ID to actual UUID object to avoid database type errors
    try:
        target_id = uuid.UUID(product_id)
    except ValueError:
        raise HTTPException(400, "Invalid UUID format")

    # Use joinedload if you want the response to include the category name immediately
    result = await db.execute(
        select(Product)
        .options(joinedload(Product.category)) 
        .where(Product.id == target_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(404, "Product not found")

    # Update basic fields
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    
    # Update Category ID (allows setting to an integer or back to None/null)
    product.category_id = product_data.category_id

    await db.commit()
    await db.refresh(product)

    return product


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Product)
        .where(
            Product.id == product_id,
            Product.is_active == True
        )
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(404, "Product not found")

    return product
