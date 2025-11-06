from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
postgres_url = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'

engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
