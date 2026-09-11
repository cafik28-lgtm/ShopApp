from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate

from  ..utils.admin import get_current_admin

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.get('/', response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get('/{category_id}', response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post('/', response_model=CategoryResponse)
def create_category(cat: CategoryCreate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    try:
        db_cat = Category(
            name=cat.name,
            description=cat.description
        )
        db.add(db_cat)
        db.commit()
        db.refresh(db_cat)
        return db_cat
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

@router.put('/{category_id}', response_model=CategoryResponse)
def update_category(category_id: int, cat: CategoryUpdate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    db_cat = db.query(Category).filter(Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        if cat.name is not None:
            db_cat.name = cat.name
        if cat.description is not None:
            db_cat.description = cat.description
        db.commit()
        db.refresh(db_cat)
        return db_cat
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(err))

@router.delete('/{category_id}')
def delete_category(category_id: int, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    db_cat = db.query(Category).filter(Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        db.delete(db_cat)
        db.commit()
        return {'message': 'Category deleted successfully'}
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(err))