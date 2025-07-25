# app/schemas/review.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    user_name: str
    rating: int
    comment: Optional[str] = None
    image_url: Optional[str] = None  # Add image_url

class ReviewCreate(BaseModel):
    user_name: str
    rating: int
    comment: Optional[str] = None
    image_url: Optional[str] = None   # Only include this if your model/schema has it!


class Review(ReviewBase):
    id: int
    product_id: int
    created_at: datetime   # Use datetime, not str, for full type support

    class Config:
        orm_mode = True
