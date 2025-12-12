from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    clerk_id: str
    email: str
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None
    is_admin: bool = False

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
