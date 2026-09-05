from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, User, Admin, OrderItem, Product
from app.schemas import OrderResponse
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

@router.get('/orders', response_model=list[OrderResponse])
def get_user_orders(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Order) \
        .filter(Order.customer_id == current_user.id) \
        .all()



# # геттер конкретного заказа, если админ, то любой заказ, если юзер, то только его заказ
# @router.get("/{order_id}", response_model=OrderResponse)
# def get_order(
#     order_id: int, 
#     db: Session = Depends(get_db), 
#     current_entity = Depends(get_user_or_admin)
# ):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
        
#     if isinstance(current_entity, Admin) or order.customer_id == current_entity.id:
#         return order
        
#     raise HTTPException(status_code=403, detail="Not enough permissions")

# функция удаления заказа, юзер может удалить только свои заказы
@router.delete("/{order_id}")
def delete_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "cart" or order.is_paid == True :
        raise HTTPException(
            status_code=400,
            detail="You can delete only unpaid cart"
        )

        
    db_user = db.query(User) \
            .filter(User.id == order.customer_id) \
            .first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if db_user.id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can delete onlu your order"
        )

    try:
        orderItems = db.query(OrderItem) \
                    .filter(OrderItem.order_id == order.id) \
                    .all()
        for o in orderItems:
            db_product = db.query(Product) \
                .filter(Product.id == o.product_id) \
                .first()
            
            if db_product:
                db_product.amount += o.amount
                if db_product.amount > 0:
                    db_product.in_stock = True
            db.delete(o)

        db.delete(order)
        db.commit()
        return {"message": "Order deleted successfully"}
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))