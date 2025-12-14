import json
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from svix.webhooks import Webhook, WebhookVerificationError

from app.core.db import get_db
from app.core.config import settings
from app.models.user import User

router = APIRouter()


def _verify_svix(request: Request, raw_body: bytes) -> None:
    secret_value = settings.CLERK_SIGNING_SECRET
    if not secret_value:
        raise HTTPException(status_code=500, detail="Signing secret not configured")
    headers = {
        "svix-id": request.headers.get("svix-id"),
        "svix-timestamp": request.headers.get("svix-timestamp"),
        "svix-signature": request.headers.get("svix-signature"),
    }
    if not all(headers.values()):
        raise HTTPException(status_code=400, detail="Missing Svix signature headers")
    wh = Webhook(secret_value.get_secret_value())
    try:
        wh.verify(raw_body, headers)
    except WebhookVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")


def _extract_primary_email(data: Dict[str, Any]) -> Optional[str]:
    email_addresses = data.get("email_addresses") or []
    primary_id = data.get("primary_email_address_id")
    if primary_id:
        for entry in email_addresses:
            if entry.get("id") == primary_id:
                return entry.get("email_address")
    if email_addresses:
        return email_addresses[0].get("email_address")
    return None


def _extract_primary_phone(data: Dict[str, Any]) -> Optional[str]:
    phone_numbers = data.get("phone_numbers") or []
    primary_id = data.get("primary_phone_number_id")
    if primary_id:
        for entry in phone_numbers:
            if entry.get("id") == primary_id:
                return entry.get("phone_number")
    if phone_numbers:
        return phone_numbers[0].get("phone_number")
    return None


async def _upsert_user(db: AsyncSession, data: Dict[str, Any]) -> User:
    clerk_id = data.get("id")
    email = _extract_primary_email(data)
    phone = _extract_primary_phone(data)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    image_url = data.get("image_url")

    if not clerk_id or not email:
        raise HTTPException(status_code=400, detail="Missing clerk_id or email")

    result = await db.execute(select(User).where(User.clerk_id == clerk_id))
    user = result.scalar_one_or_none()
    if user:
        user.email = email
        user.phone = phone
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
    else:
        user = User(
            clerk_id=clerk_id,
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
            is_admin=False,
        )
        db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/webhooks/clerk")
async def clerk_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    raw = await request.body()
    _verify_svix(request, raw)

    payload = json.loads(raw)
    event_type = payload.get("type")
    data = payload.get("data") or {}

    if event_type in {"user.created", "user.updated"}:
        user = await _upsert_user(db, data)
        return {"ok": True, "id": user.id, "clerk_id": user.clerk_id}
    if event_type == "user.deleted":
        clerk_id = data.get("id")
        if not clerk_id:
            raise HTTPException(status_code=400, detail="Missing clerk_id")
        result = await db.execute(select(User).where(User.clerk_id == clerk_id))
        user = result.scalar_one_or_none()
        if user:
            await db.delete(user)
            await db.commit()
        return {"ok": True}

    return {"ok": True, "ignored": event_type}
