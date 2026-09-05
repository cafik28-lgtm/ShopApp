from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, Order, OrderItem
from app.schemas import OrderItemCreate, OrderItemResponse, OrderItemUpdate

from app.models import User, Admin

from ..utils.admin import check_admin
from ..utils.user import get_current_user, check_user

from datetime import datetime

router = APIRouter(
    prefix="/orderItems",
    tags=["OrderItems"]
)

@router.post('/', response_model=OrderItemResponse)
def create_ori(
    user_id: int,
    product_id: int,
    ori: OrderItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_user = db.query(User) \
            .filter(User.id == user_id) \
            .first()
    
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if current_user.id !=  user_id:
        raise HTTPException(
            status_code=403, 
            detail="You can add product to cart only on your page"
        )

    db_product = db.query(Product) \
                        .filter(Product.id == product_id) \
                        .first()
    if not db_product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found"
        )

    if not db_product.in_stock:
        raise HTTPException(
            status_code=400,
            detail="Product is out of stock"
        )

    if ori.amount > db_product.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough products in stock. Available: {db_product.amount}"
        )   

    db_order = db.query(Order) \
            .filter(Order.customer_id == user_id, Order.status=="cart") \
            .first()

    if not db_order:
        db_order = Order(
            customer_id = user_id,
            total_cost = 0,
            created_at = datetime.utcnow(),
            status = "cart",
            delivery_address = None,
            is_delivered = False
        )

        db.add(db_order)
        db.commit()
        db.refresh(db_order)

    db_ori = db.query(OrderItem) \
            .filter(OrderItem.order_id == db_order.id, OrderItem.product_id == product_id) \
            .first()

    try:
        if db_ori:

            db_ori.amount += ori.amount
            db_ori.cost = db_ori.amount * db_product.cost

            db_product.amount -= ori.amount

            if db_product.amount == 0:
                db_product.in_stock = False

            db.add(db_ori)
            db.commit()
            db.refresh(db_ori)

            return db_ori

        db_ori = OrderItem(
            order_id=db_order.id,
            product_id=db_product.id,
            amount=ori.amount,
            cost=ori.amount * db_product.cost
        )

        db_product.amount -= ori.amount

        if db_product.amount == 0:
            db_product.in_stock = False

        db.add(db_ori)
        db.commit()
        db.refresh(db_ori)

        return db_ori

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )
    
@router.put('/{ori_id}', response_model=OrderItemResponse)
def update_ori(
    ori: OrderItemUpdate,
    ori_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_ori = db.query(OrderItem) \
            .filter(OrderItem.id == ori_id) \
            .first()

    if not db_ori:
        raise HTTPException(
            status_code=404,
            detail="Order Item not found"
        )

    db_order = db.query(Order) \
            .filter(Order.id == db_ori.order_id) \
            .first()

    db_user = db.query(User) \
            .filter(User.id == db_order.customer_id) \
            .first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User nor found"
        )

    if current_user.id != db_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can update only your order item"
        )

    try:
        difference = ori.amount - db_ori.amount

        prod = db.query(Product) \
            .filter(Product.id == db_ori.product_id) \
            .first()

        if not prod:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if difference > 0:

            if difference > prod.amount:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough products in stock. Available: {prod.amount}"
                )

            prod.amount -= difference

        elif difference < 0:
            prod.amount += abs(difference)
            prod.in_stock = True

        if prod.amount == 0:
            prod.in_stock = False

        db_ori.amount = ori.amount
        db_ori.cost = ori.amount * prod.cost

        db.commit()
        db.refresh(db_ori)

        return db_ori

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )

@router.delete('/{ori_id}')
def delete_ori(
    ori_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    db_ori = db.query(OrderItem) \
            .filter(OrderItem.id == ori_id) \
            .first()
    
    if not db_ori:
        raise HTTPException(
            status_code=404,
            detail="Order Item not found"
        )
    
    db_order = db.query(Order) \
            .filter(Order.id == db_ori.order_id) \
            .first()
    
    db_user = db.query(User) \
            .filter(User.id == db_order.customer_id) \
            .first()
    
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User nor found"
        )
    
    if current_user.id != db_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can delete only your order item"
        )

    try:
        db_product = db.query(Product) \
            .filter(Product.id == db_ori.product_id) \
            .first()

        if db_product:
            db_product.amount += db_ori.amount
            if db_product.amount > 0:
                db_product.in_stock = True
        db.delete(db_ori)
        db.commit()

        return {'message': 'Order Item deleted successfuly'}
    
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )