from sqlalchemy import Column, Integer, String, Boolean
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
