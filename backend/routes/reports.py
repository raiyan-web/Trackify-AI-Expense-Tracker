from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, extract
from backend.auth import get_current_user
from backend.database import get_db
from backend import models

router = APIRouter()


from sqlalchemy.future import select

@router.get("/monthly")
async def monthly_report(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    stmt = (
        select(models.Expense.category, func.sum(models.Expense.total).label("total"))
        .where(models.Expense.user_id == current_user.id)
        .where(extract("month", models.Expense.date) == month)
        .where(extract("year", models.Expense.date) == year)
        .group_by(models.Expense.category)
    )
    result = await db.execute(stmt)
    rows = result.all()
    total_spent = sum(r.total for r in rows)
    return {
        "month": month,
        "year": year,
        "total_spent": float(total_spent),
        "by_category": [{"category": r.category, "total": float(r.total)} for r in rows],
    }
