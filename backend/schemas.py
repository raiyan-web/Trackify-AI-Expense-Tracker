from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class ReceiptCreate(BaseModel):
    merchant: str
    date: date
    total: float
    category: str
    items: Optional[List[dict]] = None
    raw_text: Optional[str] = None
    image_url: Optional[str] = None


class ReceiptRead(ReceiptCreate):
    id: int
    uploaded_at: Optional[str]

    class Config:
        orm_mode = True


class ExpenseCreate(BaseModel):
    merchant: str
    total: float
    date: date
    category: str
    items: Optional[List[dict]] = None
    receipt_id: Optional[int] = None


class ExpenseRead(ExpenseCreate):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True


class ExtractedReceipt(BaseModel):
    merchant: str
    date: date
    total: float
    items: List[dict]
    category: str
