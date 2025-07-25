# app/schemas/product.py
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.review import Review

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    in_stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    reviews: List[Review] = []
    class Config:
        orm_mode = True
