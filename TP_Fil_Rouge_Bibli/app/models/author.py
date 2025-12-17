from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class AuthorBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    birth_date: date
    nationality: str = Field(max_length=2)  # Code pays ISO
    biography: Optional[str] = Field(default=None)
    death_date: Optional[date] = Field(default=None)
    website: Optional[str] = Field(default=None)

class Author(AuthorBase, table=True):
    "Modèle de données pour un auteur"
    
    __tablename__ = "authors"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    books: List["Book"] = Relationship(back_populates="author")

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
