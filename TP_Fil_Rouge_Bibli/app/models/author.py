from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.book import Book


class Author(SQLModel, table=True):
    __tablename__ = "authors"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    birth_date: date
    nationality: str = Field(max_length=2, index=True)
    biography: Optional[str] = None
    death_date: Optional[date] = None
    website: Optional[str] = None

    books: list["Book"] = Relationship(back_populates="author")
