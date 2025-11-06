from fastapi import FastAPI, UploadFile, Form
from .db.database import create_db_and_tables, SessionDep
from .db.model import Book
from .schemas import BookPost
from pydantic import BaseModel
import os

app = FastAPI()


class BookCreate(BaseModel):
    name: str
    author: str
    about: str | None


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/books/", response_model=BookPost)
def create_book(session: SessionDep, file_u: UploadFile, name: str = Form(...), author: str = Form(...),
                about: str = Form(None)) -> Book:
    file = file_u.file
    filename = file_u.filename
    with open(f"{os.path.abspath(os.path.join(os.path.dirname( __file__ )))}/../files/{filename}", "wb") as f:
        f.write(file.read())

    db_book = Book(
        name=name,
        author=author,
        about=about,
        cover=f"{os.getcwd()}/files/{filename}"
    )

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book
