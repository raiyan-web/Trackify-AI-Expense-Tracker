import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.auth import get_current_user
from backend.database import get_db
from backend import models
from backend.ai.extractor import extract_receipt

router = APIRouter()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    image_path = os.path.join(UPLOAD_DIR, filename)
    with open(image_path, "wb") as f:
        f.write(image_bytes)

    extracted = extract_receipt(image_bytes)
    receipt = models.Receipt(
        user_id=current_user.id,
        image_url=f"/uploads/{filename}",
        raw_text=extracted.get("raw_text", ""),
    )
    db.add(receipt)
    await db.commit()
    await db.refresh(receipt)

    return {"status": "success", "data": extracted, "receipt_id": receipt.id}


@router.get("/")
async def list_receipts(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Receipt).where(models.Receipt.user_id == current_user.id))
    receipts = result.scalars().all()
    return receipts
