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
    delivery_type: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_distance_km: Optional[float] = None
    delivery_fee: Optional[float] = None
    scheduled_date: Optional[str] = None


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
    delivery_type: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_distance_km: Optional[float] = None
    delivery_fee: Optional[float] = None
    requested_date: Optional[str] = None
    size: Optional[str] = None
    flavor: Optional[str] = None
    filling: Optional[str] = None
    topping: Optional[str] = None
    servings: Optional[str] = None
    message: Optional[str] = None


class CustomOrder(CustomOrderCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
