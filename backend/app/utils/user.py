from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from .password import verify_password
from app.schemas import UserLogin

def get_current_user_headers(
    email: str = Header(...),
    password: str = Header(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=403,
            detail="User access required"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return user

def get_current_user_from_headers(
    email: str = Header(...),
    password: str = Header(...),
    db: Session = Depends(get_db)
):
    return get_current_user_headers(email=email, password=password, db=db)

def get_current_user(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=403,
            detail="User access required"
        )

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return user

def check_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if user and verify_password(password, user.hashed_password):
        return True

    return False