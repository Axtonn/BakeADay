import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.db import get_db
from app.core.config import settings
from app.models.order import Order, OrderItem
from app.schemas.order import Order as OrderSchema, OrderCreate

router = APIRouter()

GOOGLE_ORIGIN = "Caulfield Station VIC 3145"
MAX_DELIVERY_KM = 50.0


async def _distance_km(destination: str) -> float:
    if not settings.GOOGLE_MAPS_API_KEY:
        raise HTTPException(status_code=500, detail="Maps API key not configured")
    params = {
        "origins": GOOGLE_ORIGIN,
        "destinations": destination,
        "key": settings.GOOGLE_MAPS_API_KEY.get_secret_value(),
        "units": "metric",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json", params=params
        )
    data = resp.json()
    try:
        element = data["rows"][0]["elements"][0]
        if element.get("status") != "OK":
            raise ValueError(element.get("status"))
        meters = element["distance"]["value"]
        return meters / 1000.0
    except Exception:
        raise HTTPException(status_code=400, detail="Could not compute delivery distance")


@router.post("/", response_model=OrderSchema)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    delivery_distance_km = None
    delivery_fee = None

    if order.delivery_type == "delivery":
        if not order.delivery_address:
            raise HTTPException(status_code=400, detail="Delivery address required")
        delivery_distance_km = await _distance_km(order.delivery_address)
        if delivery_distance_km > MAX_DELIVERY_KM:
            raise HTTPException(status_code=400, detail="Delivery address is beyond 50km radius")
        delivery_fee = 0  # placeholder for future fee calculation

    db_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        delivery_type=order.delivery_type,
        delivery_address=order.delivery_address,
        delivery_distance_km=delivery_distance_km,
        delivery_fee=delivery_fee,
        scheduled_date=order.scheduled_date,
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
