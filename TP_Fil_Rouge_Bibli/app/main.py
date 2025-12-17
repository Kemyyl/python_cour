from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers.author import router as authors_router
from app.routers.book import router as books_router

app = FastAPI()

app.include_router(authors_router)
app.include_router(books_router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
