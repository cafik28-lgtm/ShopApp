from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

import os
import shutil

from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate, ProductResponse

from app.models import User
from app.models import Category

from ..utils.admin import check_admin
from ..utils.user import get_current_user, check_user

from datetime import datetime

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

MEDIAS_DIR = 'media'
os.makedirs(MEDIAS_DIR, exist_ok=True)

@router.get('/', response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get('/{product_id}', response_model=ProductResponse)
def get_product(product_id : int, db: Session = Depends(get_db)):
    product = db.query(Product) \
                .filter(Product.id == product_id) \
                .first()

    if not product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found"
        )

    return product

@router.post('/seller={user_id}/create/', response_model=ProductResponse)
def create_product(
    user_id: int,
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
    ):

    db_user = db.query(User) \
        .filter(User.id == product.seller_id) \
        .first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if current_user.id !=  user_id:
        raise HTTPException(
            status_code=403, 
            detail="You can add product only on your page"
        )

    db_category = db.query(Category) \
                        .filter(Category.id == product.category_id) \
                        .first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    try:
        db_product = Product(
            name = product.name,
            description = product.description or None,
            cost = product.cost,
            amount = product.amount,
            in_stock = product.in_stock,
            photo = None,
            created_at =  datetime.utcnow(),
            seller_id = db_user.id,
            category_id = product.category_id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )

@router.put('/{product_id}', response_model=ProductResponse)
def update_product(product: ProductUpdate, 
                   product_id: int,
                   db: Session = Depends(get_db),
                   current_user = Depends(get_current_user)
                   ):
    
    db_product = db.query(Product) \
                    .filter(Product.id == product_id) \
                    .first()
    if not db_product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found"
        )
    
    db_user = db.query(User) \
            .filter(User.id == db_product.seller_id) \
            .first()
    
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if current_user.id != db_product.seller_id:
        raise HTTPException(
            status_code=403, 
            detail="You can update product only on your products"
        )

    try:
        if product.name is not None:
            db_product.name = product.name

        if product.description is not None:
            db_product.description = product.description

        if product.cost is not None:
            db_product.cost = product.cost

        if product.amount is not None:
            db_product.amount = product.amount

        if product.in_stock is not None:
            db_product.in_stock = product.in_stock

        if product.photo is not None:
            db_product.photo = product.photo

        if product.category_id is not None:
            db_product.category_id = product.category_id

        db_product.created_at =  datetime.utcnow()

        db.commit()
        db.refresh(db_product)
        return db_product

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )

@router.put('/{product_id}/media', response_model=ProductResponse)
def upload_product_media(
        product_id: int,
        media: UploadFile = File(...), 
        db: Session = Depends(get_db), 
        current_user = Depends(get_current_user)
    ):
    db_product = db.query(Product) \
                        .filter(Product.id == product_id) \
                        .first()
    if not db_product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found"
        )

    db_user = db.query(User).filter(User.id == db_product.seller_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404, 
            detail='User not found'
        )

    if current_user.id != db_product.seller_id:
            raise HTTPException(
                status_code=403, 
                detail='You can only update your products media'
            )
        
   
    try:
        file_extension = os.path.splitext(media.filename)[1]
        new_filename = f"product_{db_product.name}_{db_product.id}{file_extension}"     
        file_path = os.path.join(MEDIAS_DIR, new_filename)
            
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
            
        db_product.photo = file_path
        db.commit()
        db.refresh(db_product)
        return db_product
    
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=str(err)
        )

@router.delete('/{product_id}')
def delete_product(
        product_id: int,
        email: str,
        password: str,
        db: Session = Depends(get_db), 
    ):
     
    db_product = db.query(Product) \
                    .filter(Product.id == product_id) \
                    .first()
    if not db_product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found"
        )

    is_admin = check_admin(email, password, db)
    is_seller = check_user(email, password, db)

    if not is_admin and not is_seller:
        raise HTTPException(
            status_code=403,
            detail="Only seller or admin can delete product"
        )

    if is_seller:
        user = db.query(User).filter(User.email == email).first()

        if user.id != db_product.seller_id and not is_admin:
            raise HTTPException(
                status_code=403,
                detail="You can only delete your products"
            )

    try:
        db.delete(db_product)
        db.commit()

        return {'message': 'Product deleted successfully'}

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )
            
    
    