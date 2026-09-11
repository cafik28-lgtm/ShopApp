from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Admin
from app.utils.password import verify_password
from app.schemas import AdminLogin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/login")
def login_admin(
    data: AdminLogin,
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.email == data.email).first()

    if not admin or not verify_password(data.password, admin.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Admin login successful",
        "admin_id": admin.id,
        "email": admin.email
    }