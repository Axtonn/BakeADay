from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select
from app.core.db import get_db
from app.models.order import Order

router = APIRouter()

@router.get("/")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    # Total orders
    total_orders_result = await db.execute(select(func.count()).select_from(Order))
    total_orders = total_orders_result.scalar_one()

    # Total sales
    total_sales_result = await db.execute(select(func.sum(Order.total)))
    total_sales = total_sales_result.scalar() or 0

    return {
        "total_orders": total_orders,
        "total_sales": float(total_sales),
    }
