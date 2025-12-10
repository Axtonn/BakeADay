from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.db import get_db
from app.models.order import Order, OrderItem
from app.schemas.order import Order as OrderSchema, OrderCreate

router = APIRouter()

@router.post("/", response_model=OrderSchema)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        total=order.total,
    )
    db.add(db_order)
    await db.flush()  # get order.id

    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
        )
        db.add(db_item)

    await db.commit()
    await db.refresh(db_order)
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == db_order.id)
    )
    return result.scalar_one()
