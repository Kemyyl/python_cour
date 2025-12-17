from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Book, BookCreate, BookRead, Author

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookRead])
def list_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()


@router.post("/", response_model=BookRead, status_code=201)
def create_book(payload: BookCreate, session: Session = Depends(get_session)):
    author = session.get(Author, payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Auteur inexistant")

    book = Book.model_validate(payload)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return book
