from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    customer_name: str
    customer_email: str
    total: float = Field(..., ge=0)


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        orm_mode = True


class CustomOrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    phone: Optional[str] = None
    base_type: str
    size: Optional[str] = None
    flavor: Optional[str] = None
    filling: Optional[str] = None
    topping: Optional[str] = None
    servings: Optional[str] = None
    delivery_type: Optional[str] = None
    requested_date: Optional[str] = None
    message: Optional[str] = None


class CustomOrder(CustomOrderCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
