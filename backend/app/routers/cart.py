from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, User, Admin, OrderItem, Product
from app.schemas import OrderResponse
from ..utils.user import get_current_user_headers
from ..utils.admin import get_current_admin


router = APIRouter(
    prefix="/cart",
    tags=["Carts"],
)


@router.get('/')
def get_cart(
    current_user = Depends(get_current_user_headers),
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

@router.post('/add')
def add_to_cart(
    product_id: int,
    amount: int = 1,
    current_user = Depends(get_current_user_headers),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.amount < amount:
        raise HTTPException(status_code=400, detail="Not enough items in stock")

    cart = db.query(Order).filter(
        Order.customer_id == current_user.id,
        Order.status == "cart",
        Order.is_paid == False
    ).first()

    if not cart:
        cart = Order(
            customer_id=current_user.id,
            total_cost=0,
            status="cart",
            is_paid=False
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)

    order_item = db.query(OrderItem).filter(
        OrderItem.order_id == cart.id,
        OrderItem.product_id == product.id
    ).first()

    if order_item:
        order_item.amount += amount
        order_item.cost = order_item.amount * product.cost
    else:
        order_item = OrderItem(
            order_id=cart.id,
            product_id=product.id,
            amount=amount,
            cost=product.cost * amount
        )
        db.add(order_item)

    db.commit()

    items = db.query(OrderItem).filter(OrderItem.order_id == cart.id).all()
    cart.total_cost = sum(i.cost for i in items)
    db.commit()

    return {"message": "Product added to cart successfully"}

@router.delete('/item/{order_item_id}')
def remove_from_cart(
    order_item_id: int,
    current_user = Depends(get_current_user_headers),
    db: Session = Depends(get_db)
):
    item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    cart = db.query(Order).filter(Order.id == item.order_id, Order.customer_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(item)
    db.commit()

    # Пересчет суммы
    items = db.query(OrderItem).filter(OrderItem.order_id == cart.id).all()
    cart.total_cost = sum(i.cost for i in items)
    db.commit()

    return {"message": "Item removed from cart"}

@router.post('/checkout')
def checkout_cart(
    address: str = "Default address",
    current_user = Depends(get_current_user_headers),
    db: Session = Depends(get_db)
):
    cart = db.query(Order).filter(
        Order.customer_id == current_user.id,
        Order.status == "cart",
        Order.is_paid == False
    ).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = db.query(OrderItem).filter(OrderItem.order_id == cart.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            if product.amount < item.amount:
                raise HTTPException(status_code=400, detail=f"Product {product.name} out of stock")
            product.amount -= item.amount
            if product.amount == 0:
                product.in_stock = False

    cart.status = "pending"
    cart.delivery_address = address
    cart.is_paid = True 
    db.commit()

    return {"message": "Order placed successfully", "order_id": cart.id}