from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoanBase(BaseModel):
    book_id: int
    user_id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    return_date: Optional[datetime] = None
    due_date: Optional[datetime] = None

class Loan(LoanBase):
    id: int
    
    class Config:
        from_attributes = True