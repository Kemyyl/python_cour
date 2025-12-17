from datetime import datetime, timedelta
from enum import Enum

class LoanStatus(Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class Loan:
    def __init__(self, loan_id, book_id, member_id, loan_date=None, due_date=None, return_date=None):
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.loan_date = loan_date or datetime.now()
        self.due_date = due_date or (self.loan_date + timedelta(days=14))
        self.return_date = return_date
        self.status = LoanStatus.ACTIVE

    def return_book(self, return_date=None):
        self.return_date = return_date or datetime.now()
        self.status = LoanStatus.RETURNED

    def is_overdue(self):
        if self.status == LoanStatus.RETURNED:
            return False
        return datetime.now() > self.due_date

    def update_status(self):
        if self.is_overdue():
            self.status = LoanStatus.OVERDUE
        elif self.return_date:
            self.status = LoanStatus.RETURNED

    def __repr__(self):
        return f"Loan(id={self.loan_id}, book={self.book_id}, member={self.member_id}, status={self.status.value})"