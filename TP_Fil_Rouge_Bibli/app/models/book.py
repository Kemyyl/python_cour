from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class BookCategory(str, Enum):
    """Catégories littéraires"""

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

class BookBase(SQLModel):
    title: str = Field(index=True)
    isbn: str = Field(unique=True, index=True, max_length=17)
    publication_year: int
    author_id: int = Field(foreign_key="authors.id", index=True)
    available_copies: int = Field(default=0, ge=0)
    total_copies: int = Field(gt=0)
    description: Optional[str] = Field(default=None)
    category: BookCategory = Field(default=BookCategory.AUTRE)
    language: str = Field(max_length=2)  # Code langue ISO
    pages: int = Field(gt=0)
    publisher: str

class Book(BookBase, table=True):
    "Modèle de données pour un livre"
    
    __tablename__ = "books"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    author: Optional["Author"] = Relationship(back_populates="books")

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
