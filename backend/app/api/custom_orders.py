from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_db
from app.models.custom_order import CustomOrder
from app.schemas.order import CustomOrder as CustomOrderSchema, CustomOrderCreate
from app.utils.email import send_contact_email

router = APIRouter()


@router.post("/", response_model=CustomOrderSchema)
async def create_custom_order(payload: CustomOrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = CustomOrder(**payload.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # Send email to admin with summary
    summary_lines = [
        f"Customer: {payload.customer_name} ({payload.customer_email}{' / ' + payload.phone if payload.phone else ''})",
        f"Base: {payload.base_type}",
        f"Size: {payload.size}",
        f"Flavor: {payload.flavor}",
        f"Filling: {payload.filling}",
        f"Topping: {payload.topping}",
        f"Servings: {payload.servings}",
        f"Delivery: {payload.delivery_type}",
        f"Requested Date: {payload.requested_date}",
        f"Message: {payload.message}",
    ]
    summary = "\n".join([line for line in summary_lines if line is not None])
    try:
        await send_contact_email(payload.customer_email, summary)
    except Exception:
        # Don't fail the order on email issues
        pass

    return db_order


@router.get("/", response_model=list[CustomOrderSchema])
async def list_custom_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomOrder).order_by(CustomOrder.created_at.desc()))
    return result.scalars().all()
