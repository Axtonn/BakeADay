import json
import hmac
import hashlib

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pydantic import SecretStr

from app.main import app
from app.core.config import settings
from app.core.db import Base, get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Ensure signing secret present for tests
settings.CLERK_SIGNING_SECRET = SecretStr("testsecret")

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine = create_async_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def sign(body: bytes) -> str:
    secret_value = settings.CLERK_SIGNING_SECRET or settings.SECRET_KEY
    return hmac.new(
        secret_value.get_secret_value().encode("utf-8"), body, hashlib.sha256
    ).hexdigest()


@pytest.mark.asyncio
async def test_clerk_user_created_upsert():
    payload = {
        "type": "user.created",
        "data": {
            "id": "user_123",
            "email_addresses": [{"email_address": "alice@example.com"}],
            "first_name": "Alice",
            "last_name": "Baker",
            "image_url": "http://example.com/a.png",
        },
    }
    body = json.dumps(payload).encode("utf-8")
    signature = sign(body)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/webhooks/clerk", content=body, headers={"authorization": signature}
        )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["ok"] is True
    assert data["clerk_id"] == "user_123"


@pytest.mark.asyncio
async def test_clerk_user_deleted():
    # Create first
    payload = {
        "type": "user.created",
        "data": {
            "id": "user_456",
            "email_addresses": [{"email_address": "bob@example.com"}],
        },
    }
    body = json.dumps(payload).encode("utf-8")
    signature = sign(body)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/webhooks/clerk", content=body, headers={"authorization": signature}
        )

    # Delete
    del_payload = {"type": "user.deleted", "data": {"id": "user_456"}}
    del_body = json.dumps(del_payload).encode("utf-8")
    del_sig = sign(del_body)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/webhooks/clerk", content=del_body, headers={"authorization": del_sig}
        )
    assert resp.status_code == 200, resp.text
    assert resp.json()["ok"] is True
