from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
from backend.routes import receipts, expenses, reports

app = FastAPI(title="trackify")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Trackify API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Trackify API is running"}

# Mock receipt upload endpoint
@app.post("/api/upload")
async def upload_receipt():
    """Mock receipt upload - returns simulated extraction"""
    
    # Simulated extraction result
    extraction_result = {
        "merchant": "Coffee Shop",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": 5.99,
        "items": [
            {"name": "Espresso", "price": 3.50},
            {"name": "Croissant", "price": 2.49}
        ],
        "category": "Food & Drink"
    }
    
    return {
        "status": "success",
        "message": "Receipt processed",
        "data": extraction_result
    }

# Mock expenses endpoint
@app.get("/api/expenses")
async def get_expenses():
    """Get all expenses"""
    return {
        "status": "success",
        "data": [
            {
                "id": 1,
                "merchant": "Starbucks",
                "total": 5.99,
                "date": "2024-04-15",
                "category": "Food & Drink"
            },
            {
                "id": 2,
                "merchant": "Uber",
                "total": 12.50,
                "date": "2024-04-14",
                "category": "Transportation"
            },
            {
                "id": 3,
                "merchant": "Target",
                "total": 45.23,
                "date": "2024-04-13",
                "category": "Shopping"
            }
        ]
    }

# Mock monthly report
@app.get("/api/reports/monthly")
async def monthly_report(month: int = 4, year: int = 2024):
    """Get monthly spending report - mock endpoint"""
    return {
        "status": "success",
        "data": {
            "month": month,
            "year": year,
            "total_spent": 63.72,
            "by_category": {
                "Food & Drink": 5.99,
                "Transportation": 12.50,
                "Shopping": 45.23
            }
        }
    }

# Commented out - these require database and auth
# Uncomment after setting up PostgreSQL and authentication
# app.include_router(receipts.router, prefix="/api/receipts", tags=["receipts"])
# app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
# app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
