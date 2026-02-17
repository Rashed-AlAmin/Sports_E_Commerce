from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from backend.schemas.cart import CartResponse
from backend.core.dependencies import get_current_user, get_db
from backend.models.cart import Cart
from backend.models.cart_item import CartItem
from backend.models.product import Product
from backend.models.user import User

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.post("/add/{product_id}")
async def add_to_cart(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check product exists
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Get or create cart
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalars().first()

    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)

    # Check if product already in cart
    result = await db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
    )
    cart_item = result.scalars().first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=1
        )
        db.add(cart_item)

    await db.commit()
    return {"message": "Product added to cart"}

@router.get("/", response_model=CartResponse)
async def view_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # We use selectinload to pull the items AND the product info in one go
    result = await db.execute(
        select(Cart)
        .options(
            selectinload(Cart.items).selectinload(CartItem.product)
        )
        .where(Cart.user_id == current_user.id)
    )
    cart = result.scalars().first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Just return the database object! 
    # FastAPI and your CartResponse schema will do the rest.
    return cart