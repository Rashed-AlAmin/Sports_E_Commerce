# backend/crud/category.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.product import Category  # Adjust path to where your Category model is
from backend.schemas.product import CategoryCreate # Adjust path to your schemas

async def create_category(db: AsyncSession, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()

async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    return result.scalars().first()