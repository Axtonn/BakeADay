from pydantic import BaseModel
from typing import List, Dict, Any

class OrderBase(BaseModel):
    customer_name: str
    customer_email: str
    total: float
    items: Any

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    items: List[Dict[str, Any]]  # Each item: {product_id, name, price, quantity}
    total: float

class Order(OrderBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True
