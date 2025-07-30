from sqlalchemy.orm import declarative_base
Base = declarative_base()

from .user import User
from .product import Product
from .order import Order
from .review import Review
