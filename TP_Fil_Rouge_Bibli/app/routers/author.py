from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select

from app.database import get_session
from app.models.author import Author
from app.models.book import Book
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/authors", tags=["Auteurs"])


@router.post("/", response_model=AuthorRead, status_code=201)
def create_author(author: AuthorCreate, session: Session = Depends(get_session)):
    statement = select(Author).where(
        Author.first_name == author.first_name,
        Author.last_name == author.last_name,
    )
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Un auteur avec le nom {author.first_name} {author.last_name} existe déjà",
        )

    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.get("/", response_model=PaginatedResponse[AuthorRead])
def list_authors(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    nationality: str | None = None,
    sort_by: str = Query("last_name", pattern="^(last_name|first_name|birth_date)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
):
    statement = select(Author)

    if search:
        statement = statement.where(
            (Author.first_name.ilike(f"%{search}%")) | (Author.last_name.ilike(f"%{search}%"))
        )
    if nationality:
        statement = statement.where(Author.nationality == nationality.upper())

    sort_column = getattr(Author, sort_by)
    statement = statement.order_by(sort_column.desc() if order == "desc" else sort_column)

    count_statement = select(func.count()).select_from(statement.subquery())
    total = session.exec(count_statement).one()

    offset = (page - 1) * page_size
    authors = session.exec(statement.offset(offset).limit(page_size)).all()

    total_pages = (total + page_size - 1) // page_size

    return PaginatedResponse(
        items=authors,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.patch("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int,
    author_update: AuthorUpdate,
    session: Session = Depends(get_session),
):
    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")

    data = author_update.model_dump(exclude_unset=True)

    # check unicité si nom change
    if "first_name" in data or "last_name" in data:
        first_name = data.get("first_name", db_author.first_name)
        last_name = data.get("last_name", db_author.last_name)
        exists = session.exec(
            select(Author).where(
                Author.first_name == first_name,
                Author.last_name == last_name,
                Author.id != author_id,
            )
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Nom complet déjà utilisé")

    for k, v in data.items():
        setattr(db_author, k, v)

    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.delete("/{author_id}")
def delete_author(author_id: int, session: Session = Depends(get_session)):
    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")

    books_count = session.exec(select(func.count()).where(Book.author_id == author_id)).one()
    if books_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Impossible de supprimer l'auteur car il a {books_count} livre(s) associé(s)",
        )

    session.delete(db_author)
    session.commit()
    return {"message": "Auteur supprimé"}
