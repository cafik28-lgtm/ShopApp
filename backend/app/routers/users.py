import os
import shutil
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse, UserLogin
from  ..utils.password import hash_password
from  ..utils.admin import get_current_admin
from  ..utils.user import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

AVATARS_DIR = 'avatars'
os.makedirs(AVATARS_DIR, exist_ok=True)


@router.post("/login")
def login_admin(
    data: UserLogin,
    current_user = Depends(get_current_user)
):
    return {
        "message": "User login successful",
        "admin_id": current_user.id,
        "email": current_user.email
    }

# получаем список всех пользователей
@router.get('/', response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# получаем пользователя по id
@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# создаем нового пользователя
@router.post('/', response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    email_check = db.query(User).filter(User.email == user_in.email).first()
    if email_check:
        raise HTTPException(status_code=400, detail='Email already registered')

    if user_in.phone:
        phone_check = db.query(User).filter(User.phone == user_in.phone).first()
        if phone_check:
            raise HTTPException(status_code=400, detail='Phone already registered')

    try:
        db_user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            hashed_password=hash_password(user_in.hashed_password),
            email=user_in.email,
            phone=user_in.phone or None,
            avatar=None,
            country=user_in.country,
            city=user_in.city
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

# обновляем инфу о пользователе
@router.put('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')   

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail='You can only update your own profile')

    # Проверка уникальности почты (уже была)
    if user_in.email is not None:
        email_check = db.query(User).filter(User.email == user_in.email, User.id != user_id).first()
        if email_check:
            raise HTTPException(status_code=400, detail='Email already in use')

    # Новая проверка уникальности телефона
    if user_in.phone is not None:
        phone_check = db.query(User).filter(User.phone == user_in.phone, User.id != user_id).first()
        if phone_check:
            raise HTTPException(status_code=400, detail='Phone already in use')

    try:
        if user_in.first_name is not None:
            db_user.first_name = user_in.first_name

        if user_in.last_name is not None:
            db_user.last_name = user_in.last_name
        
        if user_in.hashed_password is not None:
            db_user.hashed_password = hash_password(user_in.hashed_password)
        
        if user_in.email is not None:
            db_user.email = user_in.email

        if user_in.phone is not None:
            db_user.phone = user_in.phone

        if user_in.country is not None:
            db_user.country = user_in.country
        
        if user_in.city is not None:
            db_user.city = user_in.city

        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

# чисто аву обновить
@router.put('/{user_id}/avatar', response_model=UserResponse)
def upload_user_avatar(user_id: int, avatar: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail='You can only update your own avatar')
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    try:
        safe_email = db_user.email.replace('@', '_at_').replace('.', '_')
        file_extension = os.path.splitext(avatar.filename)[1]
        new_filename = f"user_{db_user.id}_{safe_email}{file_extension}"
        file_path = os.path.join(AVATARS_DIR, new_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)

        db_user.avatar = file_path
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

# и уничтожаем пользователя по id
@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )

    try:
        db.delete(db_user)
        db.commit()

        return {'message': 'User deleted successfully'}

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )
