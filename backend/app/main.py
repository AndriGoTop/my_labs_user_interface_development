from fastapi import FastAPI, UploadFile, Form, Query, status, HTTPException, Response
from .db.database import create_db_and_tables, SessionDep
from .db.model import Book
from .schemas import BookPost, BookUpdate, UploadCover
import os
from typing import Annotated
from sqlmodel import select

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/books/", response_model=BookPost)
def create_book(session: SessionDep, book: BookPost) -> Book:
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@app.get('/books/')
def get_books(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Book]:
    books = session.exec(select(Book).order_by(-Book.id).offset(offset).limit(limit))
    return books


@app.get('/books/find')
def find_book(session: SessionDep, name_book: str) -> list[Book]:
    books = session.exec(select(Book).order_by(-Book.id).where(Book.name == name_book))
    return books


@app.get('/books/{book_id}')
def get_books(session: SessionDep, book_id: int) -> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {book_id} was not found')
    return book


@app.patch("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="book not found")
    if not book.name:
        book.name = book_db.name
    if not book.author:
        book.author = book_db.author
    if not book.about:
        book.about = book_db.about
    book_data = book.model_dump(exclude_unset=True)
    book_db.sqlmodel_update(book_data)
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    return book_db


@app.patch("/books/upload_cover/{book_id}")
def upload_cover(book_id: int, session: SessionDep, file_u: UploadFile):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    file = file_u.file
    filename = file_u.filename
    cover = f"{os.path.abspath(os.path.join(os.path.dirname(__file__)))}/../files/{filename}"
    with open(cover, "wb") as f:
        f.write(file.read())
    book.cover = cover
    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    session.delete(book)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
