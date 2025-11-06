from pydantic import BaseModel

class BookPost(BaseModel):
    name: str
    author: str
    about: str | None
    cover: str | None