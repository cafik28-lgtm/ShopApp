from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Order, User, Admin
from app.schemas import OrderCreate, OrderResponse, OrderUpdate
from ..utils.user import get_current_user
from ..utils.admin import get_current_admin

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

# функция, которая чекает есть ли юзер админом
def get_user_or_admin(email: str = None, password: str = None, db: Session = Depends(get_db)):
    try:
        if email and password:
            return get_current_admin(email=email, password=password, db=db)
    except HTTPException:
        pass
    
    try:
        if email and password:
            return get_current_user(email=email, password=password, db=db)
    except HTTPException:
        pass
        
    raise HTTPException(status_code=401, detail="Authentication required")

# геттер всех заказов, если админ, то все заказы, если юзер, то только его заказы
@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db), 
    current_entity = Depends(get_user_or_admin)
):
    if isinstance(current_entity, Admin):
        return db.query(Order).all()
    return db.query(Order).filter(Order.customer_id == current_entity.id).all()

# геттер конкретного заказа, если админ, то любой заказ, если юзер, то только его заказ
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int, 
    db: Session = Depends(get_db), 
    current_entity = Depends(get_user_or_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if isinstance(current_entity, Admin) or order.customer_id == current_entity.id:
        return order
        
    raise HTTPException(status_code=403, detail="Not enough permissions")

# функция создания заказа, доступна только для юзеров
@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        new_order = Order(
            customer_id=current_user.id,
            total_cost=order_data.total_cost,
            created_at=order_data.created_at,
            status=order_data.status,
            delivery_address=order_data.delivery_address,
            is_delivered=order_data.is_delivered
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

# функция обновления заказа, доступна для админов и юзеров, но юзер может обновлять только свои заказы
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_entity = Depends(get_user_or_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not isinstance(current_entity, Admin) and order.customer_id != current_entity.id:
        raise HTTPException(status_code=403, detail="You can only update your own orders")

    try:
        if order_update.status is not None:
            order.status = order_update.status
        if order_update.delivery_address is not None:
            order.delivery_address = order_update.delivery_address
        if order_update.is_delivered is not None:
            order.is_delivered = order_update.is_delivered

        db.commit()
        db.refresh(order)
        return order
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

# функция удаления заказа, админ может удалить любой заказ, юзер может удалить только свои заказы
@router.delete("/{order_id}")
def delete_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_entity = Depends(get_user_or_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if not isinstance(current_entity, Admin) and order.customer_id != current_entity.id:
        raise HTTPException(status_code=403, detail="You can only delete your own orders")

    try:
        db.delete(order)
        db.commit()
        return {"message": "Order deleted successfully"}
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))