from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.core.dependencies import get_db, get_current_user
from backend.models import CartItem, Order, OrderItem, Product, User, Cart

router = APIRouter(prefix="/orders", tags=["Orders"])


# CHECKOUT
@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_items = (
        db.query(CartItem)
        .join(Cart)
        .filter(Cart.user_id == current_user.id)
        .all()
    )

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total = 0

    order = Order(
        user_id=current_user.id,
        created_at=datetime.utcnow(),
        total_amount=0,
        status="pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:

        product = db.get(Product, item.product_id)

        subtotal = product.price * item.quantity
        total += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,     # FIX
            product_price=product.price,  # FIX
            quantity=item.quantity,
            subtotal=subtotal             # FIX
        )

        db.add(order_item)

        db.delete(item)

    order.total_amount = total   # FIX
    order.status = "paid"

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "total": total
    }


# ORDER HISTORY
@router.get("/my")
def order_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )


# ORDER DETAILS
@router.get("/{order_id}")
def order_detail(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if not order:
        raise HTTPException(404, "Order not found")

    items = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    return {
        "order": order,
        "items": items
    }
