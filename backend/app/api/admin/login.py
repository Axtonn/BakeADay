from fastapi import APIRouter, Request, Response, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings
import hmac

router = APIRouter()

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

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

SESSION_COOKIE = "bakeaday-admin-session"

@router.post("/login")
async def admin_login(request: Request, response: Response):
    data = await request.json()
    password = data.get("password")
    if password and hmac.compare_digest(password, settings.ADMIN_PASSWORD):
        access_token = create_access_token({"auth": True})
        response = JSONResponse(content={"ok": True})
        response.set_cookie(
            SESSION_COOKIE,
            access_token,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 2,  # 2 hours
            # secure=True, # Enable with HTTPS
        )
        return response
    return JSONResponse(
        content={"ok": False, "error": "Invalid credentials"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )

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
