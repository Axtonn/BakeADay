from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.core.db import Base


class CustomOrder(Base):
    __tablename__ = "custom_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    base_type = Column(String, nullable=False)  # cake or cheesecake
    size = Column(String, nullable=True)
    flavor = Column(String, nullable=True)
    filling = Column(String, nullable=True)
    topping = Column(String, nullable=True)
    servings = Column(String, nullable=True)
    delivery_type = Column(String, nullable=True)  # pickup or delivery
    requested_date = Column(String, nullable=True)
    message = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
