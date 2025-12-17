from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class AuthorCreate(SQLModel):
    first_name: str
    last_name: str
    birth_date: date
    nationality: str = Field(max_length=2)
    biography: Optional[str] = None
    death_date: Optional[date] = None
    website: Optional[str] = None


class AuthorRead(AuthorCreate):
    id: int


class AuthorUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = Field(default=None, max_length=2)
    biography: Optional[str] = None
    death_date: Optional[date] = None
    website: Optional[str] = None
