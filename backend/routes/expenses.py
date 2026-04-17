from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.auth import get_current_user
from backend.database import get_db
from backend import models
from backend.schemas import ExpenseCreate, ExpenseRead

router = APIRouter()


@router.post("/", response_model=ExpenseRead)
async def create_expense(expense_in: ExpenseCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    expense = models.Expense(
        user_id=current_user.id,
        merchant=expense_in.merchant,
        total=expense_in.total,
        date=expense_in.date,
        category=expense_in.category,
        items=expense_in.items,
        receipt_id=expense_in.receipt_id,
    )
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


@router.get("/")
async def get_expenses(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Expense).where(models.Expense.user_id == current_user.id).order_by(models.Expense.date.desc()))
    return result.scalars().all()
