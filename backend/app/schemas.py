from pydantic import BaseModel

class BookPost(BaseModel):
    name: str
    author: str
    about: str | None

class BookUpdate(BaseModel):
    name: str | None = None
    author: str | None = None
    about: str | None = None

class UploadCover(BaseModel):
    cover: str | None = None
