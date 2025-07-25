from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.db import get_db
from app.models.order import Order
from app.schemas.order import Order as OrderSchema, OrderCreate
import json

router = APIRouter()

@router.post("/", response_model=OrderSchema)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        items=json.dumps(order.items),  # store as JSON
        total=order.total
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order
