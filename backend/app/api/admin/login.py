import email
from fastapi import APIRouter, Request, Response, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings
import hmac
from passlib.context import CryptContext
from app.core.config import settings

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
SESSION_COOKIE = "bakeaday-admin-session"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("auth") is not True:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login")
async def admin_login(request: Request, response: Response):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return JSONResponse(
            content={"ok": False, "error": "Missing credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Load env credentials
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD_HASH

    # Use constant-time comparison for security
    if not (hmac.compare_digest(email, admin_email) and pwd_context.verify(password, admin_password)):        
        return JSONResponse(
            content={"ok": False, "error": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    access_token = create_access_token({"auth": True, "sub": email})
    response = JSONResponse(content={"ok": True})
    response.set_cookie(
        SESSION_COOKIE,
        access_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 2,
    )
    return response

@router.post("/logout")
async def admin_logout(response: Response):
    response = JSONResponse(content={"ok": True})
    response.delete_cookie(SESSION_COOKIE)
    return response

@router.get("/hello")
async def hello(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    verify_token(token)
    return {"ok": True}
