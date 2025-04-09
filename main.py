from fastapi import FastAPI, HTTPException, status
from typing import Optional
from pydantic import BaseModel
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
from pymongo import MongoClient;

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    year_of_release: int
    description: Optional[str] = None

class BookSimple(BaseModel):
    title: str
    author: str

@app.get("/books", response_model=list[BookSimple], tags=["books"])
def books_all():
    """Get all books from database"""
    books_collection = CheckDatabaseConnection()
    book_data = books_collection.find({})
    # for document in cursor:
    #     print(document)
    return list(book_data)

@app.get("/books/{book_title}", response_model= BookSimple, tags=["books"])
def book_one(book_title: str):
    """Get book from database by title"""
    books_collection = CheckDatabaseConnection()

    book_data = books_collection.find_one({"title": {"$regex": book_title, "$options": "i"}})
    if book_data is None:
        raise HTTPException(status_code=404, detail=f"Book with title {book_title} not found in database")
    return {"info": f"Book with title {book_title} is found in database"}

@app.put("/books", tags=["books"])
def book_update(book: Book):
    """Book update in database"""
    books_collection = CheckDatabaseConnection()

    book_data = books_collection.replace_one({"title": book.title}, book.model_dump())
    if book_data.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Book with title {book.title} not found in database")
    return {"info": f"Book with title {book.title} modified in database"}

@app.delete("/books/{book_title}", tags=["books"])
def delete_book_by_title(book_title: str):
    """Delete book from database by title"""
    books_collection = CheckDatabaseConnection()
    book_data = books_collection.delete_one({"title": {"$regex": book_title, "$options": "i"}})
    
    if book_data.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Book with title {book_title} not found in database")
    return {"info": f"Book with title {book_title} deleted from database"}

class Message(BaseModel):
    detail: str

@app.post("/books", status_code=status.HTTP_201_CREATED, tags=["books"], responses={409: {"model": Message}})
def add_book(book: Book):
    """Add new book to database"""
    books_collection = CheckDatabaseConnection()

    try:
        books_collection.insert_one(book.model_dump())
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail=f"Book is exist {book.title}")
    return {"info": f"Book with title {book.title} added to database"}

def CheckDatabaseConnection():
    client = MongoClient(serverSelectionTimeoutMS=5000)
    try:
        client.server_info()
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail="Problem with connecting to Database")
    books_collection = client['books_base']['books_collection']
    return books_collection

