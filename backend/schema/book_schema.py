from pydantic import BaseModel

class BookCreate(BaseModel):
    name : str
    author : str
    isbn : str

class BookResponse(BaseModel):
    id : str
    name : str
    author : str

class BookUpdate(BaseModel):
    name : str | None = None
    author : str | None = None