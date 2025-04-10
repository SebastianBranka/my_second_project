from pymongo import MongoClient;
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
from fastapi import HTTPException
import models

class Database:
    def __init__(self) -> None:
        client = MongoClient(serverSelectionTimeoutMS=5000)
        try:
            client.server_info()
        except ServerSelectionTimeoutError as e:
            raise HTTPException(status_code=503, detail="Problem with connecting to Database")
        self.books_collection = client['books_base']['books_collection']
    
    def get_all_books(self) -> list[models.Book]:
        """Method for fetching data from mango DB about all books

        Returns:
            list[models.Book]: Return list of books in Book model format.
        """
        book_data = self.books_collection.find({})
        return list(book_data)
    
    def get_one_book(self, book_title: str) -> models.Book:
        book_data = self.books_collection.find_one({"title": {"$regex": book_title, "$options": "i"}})
        if book_data is None:
            raise HTTPException(status_code=404, detail=f"Book with title {book_title} not found in database")
        return book_data

    def update_book(self, book: models.Book) -> dict[str, str]:
        book_data = self.books_collection.replace_one({"title": book.title}, book.model_dump())
        if book_data.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Book with title {book.title} not found in database")
        return {"info": f"Book with title {book.title} modified in database"}

    def delete_book(self, book_title: str) -> dict[str, str]:
        book_data = self.books_collection.delete_one({"title": {"$regex": book_title, "$options": "i"}}) 
        if book_data.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Book with title {book_title} not found in database")
        return {"info": f"Book with title {book_title} deleted from database"}

    def add_book(self, book: models.Book) -> dict[str, str]:
        try:
            self.books_collection.insert_one(book.model_dump())
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail=f"Book with title {book.title} already exists")
        return {"info": f"Book with title {book.title} added to database"}        