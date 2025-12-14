import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_db
from app.core.config import settings
from app.models.custom_order import CustomOrder
from app.schemas.order import CustomOrder as CustomOrderSchema, CustomOrderCreate
from app.utils.email import send_contact_email

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

router = APIRouter()


@router.post("/", response_model=CustomOrderSchema)
async def create_custom_order(payload: CustomOrderCreate, db: AsyncSession = Depends(get_db)):
    delivery_distance_km = None
    delivery_fee = None
    if payload.delivery_type == "delivery":
        if not payload.delivery_address:
            raise HTTPException(status_code=400, detail="Delivery address required")
        delivery_distance_km = await _distance_km(payload.delivery_address)
        if delivery_distance_km > MAX_DELIVERY_KM:
            raise HTTPException(status_code=400, detail="Delivery address is beyond 50km radius")
        delivery_fee = 0

    db_order = CustomOrder(
        **payload.dict(),
        delivery_distance_km=delivery_distance_km,
        delivery_fee=delivery_fee,
    )
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
        f"Delivery address: {payload.delivery_address}",
        f"Delivery distance (km): {delivery_distance_km}",
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
