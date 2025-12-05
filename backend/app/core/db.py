# app/core/db.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

def _normalize_async_db_url(url: str) -> str:
    """
    Ensure that the URL uses an async PostgreSQL driver (asyncpg).

    Handles cases like:
    - postgres://user:pass@host/db
    - postgresql://user:pass@host/db
    - postgresql+psycopg2://user:pass@host/db
    """
    if url.startswith("postgres://"):
        # Heroku-style URL → asyncpg
        return url.replace("postgres://", "postgresql+asyncpg://", 1)

    if url.startswith("postgresql://") and "+asyncpg" not in url:
        # Standard postgres URL without explicit driver
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)

    if "+psycopg2" in url:
        # Explicit sync driver → async driver
        return url.replace("+psycopg2", "+asyncpg", 1)

    # Already async or some other explicit async driver
    return url

DATABASE_URL = _normalize_async_db_url(settings.DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,        # turn off noisy SQL logs in prod
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
