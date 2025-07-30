from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.api.admin.login import router as admin_router
from app.api.admin.products import router as products_router
from app.api.admin.orders import router as orders_router
from app.api.products import router as user_products_router
from app.api.orders import router as user_orders_router
from app.api.reviews import router as user_reviews_router
from app.api.contact import router as user_contact_router
from app.api.admin.analytics import router as analytics_router
from app.core.config import settings
from itsdangerous import URLSafeSerializer, BadSignature
from jose import jwt, JWTError
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.0.37:3000",
        "http://163.47.70.74:3000",  # If needed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# admin routes
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(products_router, prefix="/api/admin/products", tags=["products"])
app.include_router(orders_router, prefix="/api/admin/orders", tags=["orders"])
app.include_router(analytics_router, prefix="/api/admin/analytics", tags=["analytics"])

# user routes
app.include_router(user_products_router, prefix="/api/products", tags=["products"])
app.include_router(user_orders_router, prefix="/api/orders", tags=["orders"])
app.include_router(user_reviews_router, prefix="/api/reviews", tags=["reviews"])
app.include_router(user_contact_router, prefix="/api/contact", tags=["contact"])


serializer = URLSafeSerializer(settings.SECRET_KEY, salt="admin-auth")
SESSION_COOKIE = "bakeaday-admin-session"

@app.middleware("http")
async def admin_protect_middleware(request: Request, call_next):
    # Allow all OPTIONS (CORS preflight) requests
    if request.method == "OPTIONS":
        return await call_next(request)

    # Protect /api/admin routes except /login and /logout
    if request.url.path.startswith("/api/admin") and not request.url.path.endswith(("login", "logout")):
        token = request.cookies.get(SESSION_COOKIE)
        if not token:
            resp = JSONResponse({"detail": "Not authenticated"}, status_code=401)
            # Add CORS headers!
            resp.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
            resp.headers["Access-Control-Allow-Credentials"] = "true"
            return resp
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if not payload.get("auth"):
                raise Exception()
        except Exception:
            resp = JSONResponse({"detail": "Invalid session"}, status_code=401)
            resp.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
            resp.headers["Access-Control-Allow-Credentials"] = "true"
            return resp
    response = await call_next(request)
    return response

@app.get("/api/health")
def health():
    return {"ok": True}
