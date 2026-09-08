from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, User, Admin, OrderItem, Product
from app.schemas import OrderResponse
from ..utils.user import get_current_user
from ..utils.admin import get_current_admin


router = APIRouter(
    prefix="/cart",
    tags=["Carts"],
)


@router.get('/')
def get_cart(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_order = db.query(Order) \
        .filter(
            Order.customer_id == current_user.id,
            Order.status == "cart",
            Order.is_paid == False
        ) \
        .first()

    if not db_order:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    db_items = db.query(OrderItem) \
        .filter(OrderItem.order_id == db_order.id) \
        .all()

    result = []

    for item in db_items:
        product = db.query(Product) \
            .filter(Product.id == item.product_id) \
            .first()

        result.append({
            "order_item_id": item.id,
            "product_id": product.id,
            "name": product.name,
            "description": product.description,
            "photo": product.photo,
            "price": product.cost,
            "amount": item.amount,
            "cost": item.cost
        })

    return {
        "order_id": db_order.id,
        "total_cost": db_order.total_cost,
        "items": result
    }