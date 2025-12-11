import os
import re
import shutil
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.db import get_db
from app.models.product import Product
from app.schemas.product import Product as ProductSchema, ProductCreate

UPLOAD_FOLDER = "static/images/products"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
router = APIRouter()


def _slugify(name: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return base or "product"


async def _ensure_unique_slug(
    db: AsyncSession, candidate: str, exclude_id: Optional[int] = None
) -> str:
    slug = candidate
    suffix = 1
    while True:
        query = select(Product.id).where(Product.slug == slug)
        if exclude_id is not None:
            query = query.where(Product.id != exclude_id)
        result = await db.execute(query)
        existing = result.scalar_one_or_none()
        if existing is None:
            return slug
        suffix += 1
        slug = f"{candidate}-{suffix}"


@router.get("/", response_model=List[ProductSchema])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).options(selectinload(Product.reviews))
    )
    products = result.scalars().all()
    return products

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).options(selectinload(Product.reviews)).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductSchema)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    incoming = product.dict(exclude_none=True)
    base_slug = incoming.pop("slug", None) or _slugify(product.name)
    slug = await _ensure_unique_slug(db, base_slug)

    db_product = Product(**incoming, slug=slug)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    # Eager load relationships for serialization
    result = await db.execute(
        select(Product).options(selectinload(Product.reviews)).where(Product.id == db_product.id)
    )
    db_product = result.scalar_one_or_none()
    return db_product

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1]
    if file_ext.lower() not in [".jpg", ".jpeg", ".png"]:
        return JSONResponse({"error": "Unsupported file type"}, status_code=400)
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = f"/static/images/products/{file.filename}"
    return {"url": url}

@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    # Find the product
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    incoming = product.dict(exclude_none=True)
    base_slug = incoming.pop("slug", None) or _slugify(product.name or db_product.name)
    slug = await _ensure_unique_slug(db, base_slug, exclude_id=product_id)

    for key, value in incoming.items():
        setattr(db_product, key, value)
    db_product.slug = slug

    await db.commit()
    await db.refresh(db_product)
    # Eager load relationships for serialization
    result = await db.execute(
        select(Product).options(selectinload(Product.reviews)).where(Product.id == db_product.id)
    )
    db_product = result.scalar_one_or_none()
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return {"ok": True}
