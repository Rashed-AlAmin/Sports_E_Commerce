from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.order import OrderResponse
from typing import List
from uuid import UUID

from datetime import datetime

from backend.core.dependencies import get_db, get_current_user
from backend.models import CartItem, Order, OrderItem, User, Cart


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/checkout")
async def checkout(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch CartItems AND Products in one query (Efficiency!)
    result = await db.execute(
        select(CartItem)
        .options(selectinload(CartItem.product)) # Eager load the product
        .join(Cart)
        .where(Cart.user_id == current_user.id)
    )
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(400, "Cart empty")

    # 2. Create the Order object
    order = Order(
        user_id=current_user.id,
        created_at=datetime.utcnow(),
        total_amount=0, # Will update this shortly
        status="paid"
    )
    db.add(order)
    await db.flush() # Flushes to get 'order.id' without committing the whole transaction yet

    total = 0

    # 3. Process items
    for item in cart_items:
        # No need for 'db.get(Product)' because we used selectinload above!
        product = item.product 
        subtotal = product.price * item.quantity
        total += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            product_price=product.price,
            quantity=item.quantity,
            subtotal=subtotal
        )
        db.add(order_item)
        
        # Mark cart item for deletion
        await db.delete(item)

    # 4. Finalize and Commit
    order.total_amount = total
    await db.commit() 

    return {
        "message": "Order placed successfully",
        "order_id": order.id
    }

@router.get("/my", response_model=List[OrderResponse])
async def order_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Use selectinload to fetch the 'items' relationship eagerly
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items)) 
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc()) # Good practice for history
    )
    
    orders = result.scalars().all()
    
    # Now when FastAPI passes these orders to OrderResponse, 
    # the 'items' are already loaded in memory, so no error!
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_detail(
    order_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items)) # 👈 Add this here too!
        .where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalars().first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return order
