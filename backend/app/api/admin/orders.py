from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.db import get_db
from app.models.order import Order, OrderItem
from app.schemas.order import Order as OrderSchema, OrderCreate

router = APIRouter()

@router.get("/", response_model=List[OrderSchema])
async def list_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .filter(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderSchema)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        total=order.total,
    )
    db.add(db_order)
    await db.flush()

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

@router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.delete(order)
    await db.commit()
    return {"ok": True}
