# app/models/order.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.db import Base
import datetime

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)

    # Total order amount (money) – use Numeric
    total = Column(Numeric(10, 2), nullable=False)

    # Delivery / pickup info for future features
    delivery_type = Column(String, nullable=True)          # "delivery" or "pickup"
    delivery_address = Column(String, nullable=True)
    delivery_distance_km = Column(Float, nullable=True)
    delivery_fee = Column(Numeric(10, 2), nullable=True)

    status = Column(String, default="pending_payment", nullable=False)
    scheduled_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Price per unit (money) – use Numeric
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
