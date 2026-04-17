from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    receipts = relationship("Receipt", back_populates="user")
    expenses = relationship("Expense", back_populates="user")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    image_url = Column(String, nullable=True)
    raw_text = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="receipts")
    expenses = relationship("Expense", back_populates="receipt")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    receipt_id = Column(Integer, ForeignKey("receipts.id", ondelete="SET NULL"), nullable=True)
    merchant = Column(String, nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    items = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="expenses")
    receipt = relationship("Receipt", back_populates="expenses")
