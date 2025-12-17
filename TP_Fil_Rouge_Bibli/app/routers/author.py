from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Author, AuthorCreate, AuthorRead

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/", response_model=list[AuthorRead])
def list_authors(session: Session = Depends(get_session)):
    return session.exec(select(Author)).all()


@router.post("/", response_model=AuthorRead, status_code=201)
def create_author(payload: AuthorCreate, session: Session = Depends(get_session)):
    author = Author.model_validate(payload)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    return author

@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    session.delete(author)
    session.commit()
    return

