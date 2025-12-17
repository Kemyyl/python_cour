from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select

from app.database import get_session
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/books", tags=["Livres"])


@router.post("/", response_model=BookRead, status_code=201)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    # Vérifier auteur
    author = session.get(Author, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Auteur inexistant")

    # Vérifier ISBN unique
    existing = session.exec(select(Book).where(Book.isbn == book.isbn)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Un livre avec cet ISBN existe déjà")

    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.get("/", response_model=PaginatedResponse[BookRead])
def list_books(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    category: str | None = None,
    language: str | None = None,
    author_id: int | None = None,
    sort_by: str = Query("title", pattern="^(title|publication_year|pages|publisher)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
):
    statement = select(Book)

    if search:
        statement = statement.where(
            (Book.title.ilike(f"%{search}%"))
            | (Book.isbn.ilike(f"%{search}%"))
            | (Book.publisher.ilike(f"%{search}%"))
        )

    if category:
        statement = statement.where(Book.category == category)

    if language:
        statement = statement.where(Book.language == language.lower())

    if author_id:
        statement = statement.where(Book.author_id == author_id)

    sort_column = getattr(Book, sort_by)
    statement = statement.order_by(sort_column.desc() if order == "desc" else sort_column)

    count_statement = select(func.count()).select_from(statement.subquery())
    total = session.exec(count_statement).one()

    offset = (page - 1) * page_size
    books = session.exec(statement.offset(offset).limit(page_size)).all()
    total_pages = (total + page_size - 1) // page_size

    return PaginatedResponse(
        items=books,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

    data = book_update.model_dump(exclude_unset=True)

    # Si author_id change → vérifier auteur
    if "author_id" in data:
        author = session.get(Author, data["author_id"])
        if not author:
            raise HTTPException(status_code=404, detail="Auteur inexistant")

    # Si isbn change → vérifier unique
    if "isbn" in data:
        exists = session.exec(
            select(Book).where(Book.isbn == data["isbn"], Book.id != book_id)
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="ISBN déjà utilisé")

    for k, v in data.items():
        setattr(db_book, k, v)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.delete("/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

    session.delete(db_book)
    session.commit()
    return {"message": "Livre supprimé"}
