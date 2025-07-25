# app/models/product.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.db import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    in_stock = Column(Integer, default=0)
    reviews = relationship("Review", back_populates="product")

from app.models.review import Review