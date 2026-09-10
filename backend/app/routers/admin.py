from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.admin import get_current_admin
from app.schemas import AdminLogin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/login")
def login_admin(
    data: AdminLogin,
    current_admin = Depends(get_current_admin)
):
    return {
        "message": "Admin login successful",
        "admin_id": current_admin.id,
        "email": current_admin.email
    }