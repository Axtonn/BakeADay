# app/api/admin/login.py
from datetime import datetime, timedelta
import secrets

from fastapi import APIRouter, HTTPException, Response, Depends
from pydantic import BaseModel, EmailStr
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

router = APIRouter()

# same cookie name as used in app.main middleware
SESSION_COOKIE_NAME = "bakeaday-admin-session"

# password hashing context (for ADMIN_PASSWORD_HASH)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminLoginResponse(BaseModel):
    message: str


def _verify_admin_password(plain_password: str) -> bool:
    """
    Verify the admin password using either:
    - ADMIN_PASSWORD (plaintext), or
    - ADMIN_PASSWORD_HASH (bcrypt hash).
    """
    # Prefer hash if present
    if settings.ADMIN_PASSWORD_HASH:
        try:
            hash_value = settings.ADMIN_PASSWORD_HASH.get_secret_value()
            return pwd_context.verify(plain_password, hash_value)
        except Exception:
            # Misconfigured hash → treat as failure for safety
            return False

    # Fallback to plaintext env var
    if settings.ADMIN_PASSWORD:
        return secrets.compare_digest(plain_password, settings.ADMIN_PASSWORD)

    # No password configured at all → hard fail (server misconfig)
    raise HTTPException(status_code=500, detail="Admin password is not configured")


@router.post(
    "/login",
    response_model=AdminLoginResponse,
    summary="Admin Login",
)
async def admin_login(payload: AdminLoginRequest, response: Response):
    """
    Validate admin credentials against environment-configured admin email/password.
    On success, sets an HTTP-only session cookie used by the admin middleware.
    """

    # 1) Check email
    if payload.email.lower() != settings.ADMIN_EMAIL.lower():
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2) Check password (hash-aware)
    if not _verify_admin_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3) Create a short-lived JWT session token
    now = datetime.utcnow()
    expire = now + timedelta(hours=8)  # adjust as you like

    token_data = {
        "sub": settings.ADMIN_EMAIL,
        "auth": True,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    token = jwt.encode(
        token_data,
        settings.SECRET_KEY.get_secret_value(),
        algorithm="HS256",
    )

    # 4) Set cookie so admin middleware in app.main sees it
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,          # you’re on HTTPS on Render
        samesite="lax",
        max_age=int((expire - now).total_seconds()),
    )

    return AdminLoginResponse(message="Logged in successfully")


@router.get(
    "/hello",
    summary="Admin Session Check",
)
async def admin_hello():
    """
    Simple endpoint to check if admin session is valid.
    Protected by middleware, so if this returns 200, session is valid.
    """
    return {"message": "Authenticated", "status": "ok"}


@router.post(
    "/logout",
    response_model=AdminLoginResponse,
    summary="Admin Logout",
)
async def admin_logout(response: Response):
    """
    Clear the admin session cookie.
    """
    response.delete_cookie(SESSION_COOKIE_NAME)
    return AdminLoginResponse(message="Logged out successfully")
