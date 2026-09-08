from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import ProductFeedback, Product
from app.schemas import ProductFeedbackCreate, ProductFeedbackResponse
from ..utils.user import get_current_user

router = APIRouter(
    prefix="/feedbacks",
    tags=["Feedbacks"]
)

@router.get('/', response_model=list[ProductFeedbackResponse])
def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(ProductFeedback).all()

@router.get('/product/{product_id}', response_model=list[ProductFeedbackResponse])
def get_product_feedbacks(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db.query(ProductFeedback).filter(ProductFeedback.product_id == product_id).all()

@router.post('/', response_model=ProductFeedbackResponse)
def create_feedback(
    feedback_in: ProductFeedbackCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == feedback_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        db_feedback = ProductFeedback(
            product_id=feedback_in.product_id,
            customer_id=current_user.id,
            feedback=feedback_in.feedback,
            rating=feedback_in.rating,
            created_at=datetime.utcnow()
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

@router.delete('/{feedback_id}')
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_feedback = db.query(ProductFeedback).filter(ProductFeedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if db_feedback.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own feedback")

    try:
        db.delete(db_feedback)
        db.commit()
        return {"message": "Feedback deleted successfully"}
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))