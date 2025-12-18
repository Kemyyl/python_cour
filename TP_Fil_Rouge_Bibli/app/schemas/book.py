from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class BookCategory(str, Enum):
    FICTION = "Fiction"
    SCIENCE = "Science"
    HISTOIRE = "Histoire"
    PHILOSOPHIE = "Philosophie"
    BIOGRAPHIE = "Biographie"
    POESIE = "Poésie"
    THEATRE = "Théâtre"
    JEUNESSE = "Jeunesse"
    BD = "BD"
    AUTRE = "Autre"


class BookCreate(SQLModel):
    title: str
    isbn: str
    publication_year: int
    author_id: int
    available_copies: int = Field(default=0, ge=0)
    total_copies: int = Field(gt=0)
    description: Optional[str] = None
    category: str
    language: str
    pages: int = Field(gt=0)
    publisher: str


class BookRead(BookCreate):
    id: int


class BookUpdate(SQLModel):
    title: Optional[str] = None
    isbn: Optional[str] = Field(default=None, max_length=13)
    publication_year: Optional[int] = None
    author_id: Optional[int] = None
    available_copies: Optional[int] = Field(default=None, ge=0)
    total_copies: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = None
    category: Optional[BookCategory] = None
    language: Optional[str] = Field(default=None, max_length=2)
    pages: Optional[int] = Field(default=None, gt=0)
    publisher: Optional[str] = None
