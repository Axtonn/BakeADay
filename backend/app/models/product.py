# app/models/product.py
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.core.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    # Use Numeric for money; avoid float rounding issues
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String)
    in_stock = Column(Integer, default=0)

    # Use string class name; avoids circular import
    reviews = relationship("Review", back_populates="product")
