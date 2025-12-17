from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/loans", tags=["Loans"])

class LoanBase(BaseModel):
    book_id: int
    user_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    
    class Config:
        from_attributes = True

# Mock database
loans_db = []

@router.get("/", response_model=List[Loan])
async def get_loans():
    """Get all loans"""
    return loans_db

@router.get("/{loan_id}", response_model=Loan)
async def get_loan(loan_id: int):
    """Get a specific loan"""
    loan = next((l for l in loans_db if l.get("id") == loan_id), None)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    return loan

@router.post("/", response_model=Loan, status_code=status.HTTP_201_CREATED)
async def create_loan(loan: LoanCreate):
    """Create a new loan"""
    new_loan = loan.dict()
    new_loan["id"] = len(loans_db) + 1
    loans_db.append(new_loan)
    return new_loan

@router.put("/{loan_id}", response_model=Loan)
async def update_loan(loan_id: int, loan: LoanCreate):
    """Update a loan"""
    loan_index = next((i for i, l in enumerate(loans_db) if l.get("id") == loan_id), None)
    if loan_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    loans_db[loan_index] = {**loan.dict(), "id": loan_id}
    return loans_db[loan_index]

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_loan(loan_id: int):
    """Delete a loan"""
    global loans_db
    loans_db = [l for l in loans_db if l.get("id") != loan_id]
    return None
