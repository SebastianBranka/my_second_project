from fastapi import FastAPI, status
import models
from src.database import Database

app = FastAPI()

@app.get("/books", response_model=list[models.Book], tags=["books"])
def books_all():
    """Get all books from database"""
    return Database().get_all_books()

@app.get("/books/{book_title}", response_model= models.BookSimple, tags=["books"])
def book_one(book_title: str):
    """Get book from database by title"""
    return Database().get_one_book(book_title)

@app.put("/books", tags=["books"])
def book_update(book: models.Book):
    """Book update in database"""
    return Database().update_book(book)

@app.delete("/books/{book_title}", tags=["books"])
def delete_book_by_title(book_title: str):
    """Delete book from database by title"""
    return Database().delete_book(book_title)

@app.post("/books", status_code=status.HTTP_201_CREATED, tags=["books"], responses={409: {"model": models.Message}})
def add_book(book: models.Book):
    """Add new book to database"""
    return Database().add_book(book)