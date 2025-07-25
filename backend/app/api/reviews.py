from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.db import get_db
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import Review as ReviewSchema, ReviewCreate
import os
import aiofiles

router = APIRouter()

UPLOAD_FOLDER = "static/images/reviews"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_review_image(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    async with aiofiles.open(path, "wb") as f:
        await f.write(await file.read())
    url = "/" + path.replace("\\", "/")
    return {"image_url": url}

@router.post("/product/{product_id}", response_model=ReviewSchema)
async def create_review(
    product_id: int,
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db)
):
    # Optionally: validate product exists
    result = await db.execute(select(Product).where(Product.id == product_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")
    db_review = Review(**review.dict(), product_id=product_id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

@router.get("/product/{product_id}", response_model=List[ReviewSchema])
async def get_reviews(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Review).where(Review.product_id == product_id)
    )
    return result.scalars().all()
