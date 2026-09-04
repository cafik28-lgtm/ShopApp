from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Admin, User
from .password import hash_password, verify_password

def create_default_admin(db: Session):
    admin = db.query(Admin).first()

    if not admin:
        admin = Admin(
            email="admin@gmail.com",
            hashed_password=hash_password("1234")
        )

        db.add(admin)
        db.commit()

def get_current_admin(email: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == email).first()

    if not admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    if not verify_password(password, admin.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return admin

def check_admin(email: str, password: str, db: Session):
    admin = db.query(Admin).filter(Admin.email == email).first()

    if admin and verify_password(password, admin.hashed_password):
        return True

    return False
