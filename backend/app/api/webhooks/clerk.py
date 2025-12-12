import hmac
import hashlib
import json
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_db
from app.core.config import settings
from app.models.user import User

router = APIRouter()


def _verify_signature(raw_body: bytes, signature: Optional[str]) -> None:
    """Verify Clerk webhook signature using CLERK_SIGNING_SECRET."""
    secret_value = settings.CLERK_SIGNING_SECRET
    if not secret_value:
        raise HTTPException(status_code=500, detail="Signing secret not configured")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    secret = secret_value.get_secret_value().encode("utf-8")
    expected = hmac.new(secret, raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")


async def _upsert_user(db: AsyncSession, data: Dict[str, Any]) -> User:
    clerk_id = data.get("id")
    email = (data.get("email_addresses") or [{}])[0].get("email_address")
    phone = (data.get("phone_numbers") or [{}])[0].get("phone_number")
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
    authorization: Optional[str] = Header(None),
):
    raw = await request.body()
    _verify_signature(raw, authorization)

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
