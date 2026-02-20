## BakeADay
Full-stack bakery ordering platform with a Next.js frontend, FastAPI backend, PostgreSQL database, admin dashboard, and Dockerized local deployment.

## What This Codebase Currently Does
- Displays active bakery products with product detail pages and customer reviews.
- Supports customer cart and checkout flow for standard product orders.
- Supports custom order submissions (cakes / basque cheesecakes) with delivery or pickup details.
- Validates delivery distance through Google Distance Matrix API for delivery orders.
- Sends contact/custom-order notification emails to admin via SMTP.
- Provides admin authentication (email/password from env), admin session cookie, and protected admin APIs.
- Provides admin CRUD for products, order listing, and simple analytics (total orders + total sales).
- Syncs Clerk user lifecycle events via signed Clerk webhook (`user.created`, `user.updated`, `user.deleted`).

## Not Implemented Yet (Present As Placeholders)
- Stripe or any live payment gateway integration.
- AI chatbot backend integration (frontend chatbot is a demo UI response only).
- Dedicated delivery checker utility/service modules (`backend/app/utils/delivery_checker.py` and service placeholders are empty).
- Complete backend test suite for orders/payments (`backend/tests/test_orders.py` and `backend/tests/test_payments.py` are empty).

## Tech Stack
- Frontend: Next.js 15 (App Router), React 18, TypeScript, Tailwind CSS, Clerk, Framer Motion
- Backend: FastAPI, SQLAlchemy (async), Alembic, PostgreSQL, Pydantic Settings
- Infra: Docker, Docker Compose, Nginx reverse proxy, Render config
- Integrations: Clerk webhooks (Svix signature verification), Google Distance Matrix API, SMTP email (aiosmtplib)

## Repository Structure
```text
backend/
  app/
    api/                 # Admin + public API routers
    core/                # Config + DB session setup
    models/              # SQLAlchemy models
    schemas/             # Pydantic schemas
    utils/               # Email helper + placeholders
  alembic/               # DB migrations
frontend/
  src/app/               # App Router pages/components
infra/
  nginx/nginx.conf       # Reverse proxy config
  render/render.yaml     # Render backend deploy spec
docker-compose*.yml      # Local/dev/prod compose variants
```

## Backend API Overview
- Health
  - `GET /api/health`
- Public/customer
  - `GET /api/products`
  - `GET /api/products/{product_id}`
  - `POST /api/orders`
  - `POST /api/custom-orders`
  - `GET /api/custom-orders`
  - `POST /api/reviews/upload`
  - `POST /api/reviews/product/{product_id}`
  - `GET /api/reviews/product/{product_id}`
  - `POST /api/contact`
- Admin (cookie-auth protected except login/logout)
  - `POST /api/admin/login`
  - `POST /api/admin/logout`
  - `GET /api/admin/hello`
  - `GET /api/admin/products`
  - `GET /api/admin/products/{product_id}`
  - `POST /api/admin/products`
  - `PUT /api/admin/products/{product_id}`
  - `DELETE /api/admin/products/{product_id}`
  - `POST /api/admin/products/upload`
  - `GET /api/admin/orders`
  - `GET /api/admin/orders/{order_id}`
  - `POST /api/admin/orders`
  - `DELETE /api/admin/orders/{order_id}`
  - `GET /api/admin/analytics`
- Webhooks
  - `POST /webhooks/clerk`

## Data Model (Current)
- `products`: catalog items with slug, inventory, active/featured flags, timestamps
- `orders` + `order_items`: standard checkout orders and line items
- `custom_orders`: custom cake/cheesecake request details
- `reviews`: product reviews with optional uploaded image
- `users`: Clerk-linked user profiles + admin flag

## Environment Variables
Use the provided examples:
- `backend/.env.example`
- `frontend/.env.example`

Important backend variables:
- `DATABASE_URL`
- `SECRET_KEY`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `CLERK_SIGNING_SECRET`
- `GOOGLE_MAPS_API_KEY`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `ADMIN_RECEIVER_EMAIL`
- `CORS_ORIGINS`

Important frontend variables:
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- `CLERK_SECRET_KEY`

## Local Development
### Option A: Docker Compose (recommended)
1. Create env files:
   - `backend/.env`
   - `frontend/.env.local`
2. From repository root:
```bash
docker compose -f docker-compose.dev.yml up --build
```
3. Services:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`
   - Nginx: `http://localhost:80`

### Option B: Run services separately
Backend:
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Deployment Notes
- `infra/render/render.yaml` defines backend deployment on Render with Alembic migration on startup.
- Root compose files include dev/prod variants and Nginx reverse proxy setup.
- GitHub workflow (`.github/workflows/deploy.yml`) currently installs backend dependencies on push to `main`.

## Testing Status
- Existing webhook tests: `backend/tests/test_clerk_webhook.py`
- Placeholder/empty tests:
  - `backend/tests/test_orders.py`
  - `backend/tests/test_payments.py`
