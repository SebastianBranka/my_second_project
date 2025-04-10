from typing import Optional
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    year_of_release: int
    description: Optional[str] = None

class BookSimple(BaseModel):
    title: str
    author: str