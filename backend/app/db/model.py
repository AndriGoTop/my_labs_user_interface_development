from sqlmodel import Field, SQLModel

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    author: str = Field(index=True)
    about: str | None = Field(default=None, index=True)
    cover: str | None = Field(default=None)
