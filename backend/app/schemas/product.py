# app/schemas/product.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.review import Review


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    in_stock: int
    category: Optional[str] = None
    is_active: bool = True
    is_featured: bool = False
    slug: Optional[str] = None  # allow provided slug; fallback to generated in API


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    slug: str
    reviews: List[Review] = []

    class Config:
        orm_mode = True
