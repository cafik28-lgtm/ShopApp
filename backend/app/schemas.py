from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    hashed_password: str
    email: str
    phone: str | None = None
    country: str | None = None
    city: str | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    hashed_password: str | None = None
    email: str | None = None
    phone: str | None = None
    country: str | None = None
    city: str | None = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    avatar: str | None = None
    country: str | None = None
    city: str | None = None

    class Config:
        from_attributes = True


class AdminCreate(BaseModel):
    email: str
    hashed_password: str

class AdminResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    cost: int
    amount: int
    in_stock: bool = True
    photo: str | None = None
    created_at: datetime
    seller_id: int
    category_id: int

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    cost: int | None = None
    amount: int | None = None
    in_stock: bool | bool = True
    photo: str | None = None
    created_at: datetime | None = None
    category_id: int | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    cost: int
    amount: int
    in_stock: bool = True
    photo: str | None = None
    created_at: datetime
    seller_id: int
    category_id: int

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    sender_id: int
    chat_id: int
    created_at: datetime
    is_read: bool = False
    text: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    chat_id: int
    created_at: datetime
    is_read: bool = False
    text: str

    class Config:
        from_attributes = True

class ChatCreate(BaseModel):
    customer_id: int
    seller_id: int
    created_at: datetime

class ChatResponse(BaseModel):
    id: int
    customer_id: int
    seller_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SellerFeedbackCreate(BaseModel):
    seller_id: int
    customer_id: int
    feedback: str
    rating: int
    created_at: datetime

class SellerFeedbackResponse(BaseModel):
    id: int
    seller_id: int
    customer_id: int
    feedback: str
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductFeedbackCreate(BaseModel):
    product_id: int
    customer_id: int
    feedback: str
    rating: int
    created_at: datetime

class ProductFeedbackResponse(BaseModel):
    id: int
    product_id: int
    customer_id: int
    feedback: str
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    amount: int
    cost: int

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    amount: int
    cost: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_id: int
    total_cost: int
    created_at: datetime
    status: str = "pending"
    delivery_address: str
    is_delivered: bool = False

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    total_cost: int
    created_at: datetime
    status: str = "pending"
    delivery_address: str
    is_delivered: bool = False

    class Config:
        from_attributes = True

class FavoriteCreate(BaseModel):
    user_id: int
    product_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    product_id: int

    class Config:
        from_attributes = True