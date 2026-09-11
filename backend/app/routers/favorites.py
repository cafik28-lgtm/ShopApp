from fastapi import APIRouter, Depends, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, Favorite
from app.schemas import FavoriteResponse
from app.models import User

from ..utils.user import get_current_user_headers




router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)

@router.post('/', response_model=FavoriteResponse)
def create_favorite(
    product_id: int,
    current_user = Depends(get_current_user_headers),
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

    db_favorite = db.query(Favorite) \
                    .filter(Favorite.user_id == current_user.id,
                            Favorite.product_id == db_product.id) \
                    .first()

    if db_favorite:
        raise HTTPException(
            status_code=403, 
            detail="This product already in your favorites"
        )

    try:
        db_favorite = Favorite(
            user_id = current_user.id,
            product_id = db_product.id
        )

        db.add(db_favorite)
        db.commit()
        db.refresh(db_favorite)
        return db_favorite
    
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )

@router.delete('/favorite/{product_id}/delete')
def delete_favorite(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_headers)
):
    db_fav = db.query(Favorite) \
    .filter(
        Favorite.product_id == product_id,
        Favorite.user_id == current_user.id
    ) \
    .first()

    if not db_fav:
        raise HTTPException(
            status_code=404,
            detail="Favorite not found"
        )

    try:
        db.delete(db_fav)
        db.commit()
        return {'message': 'Favorite deleted successfuly'}

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )
            
@router.get('/')
def get_favorites(
    current_user = Depends(get_current_user_headers),
    db: Session = Depends(get_db)
):
    db_favorite = db.query(Favorite) \
                    .filter(Favorite.user_id == current_user.id) \
                    .all()
    
    if not db_favorite:
        raise HTTPException(
            status_code=403, 
            detail="Favorites don't found"
        )

    result = []
    for f in db_favorite:
        product = db.query(Product) \
            .filter(Product.id == f.product_id) \
            .first()

        result.append({
            "user_id": current_user.id,
            "user_name": current_user.first_name + " " + current_user.last_name,
            "product_id": product.id,
            "name": product.name,
            "description": product.description,
            "photo": product.photo,
            "price": product.cost,
        })

    return {
        "user_id": current_user.id,
        "items": result
    }
    
   
    