from src.database import Database
from unittest.mock import patch, Mock, MagicMock
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
import pytest
from fastapi import HTTPException
import models

mocked_db_data = [
    {
        "id": 1,
        "name": "book1"
    },
     {
        "id": 2,
        "name": "book2"
    },
    {
        "id": 3,
        "name": "book3"
    }
]

test_book1 = models.Book(
    title="Wesele",
    author="Wyspiański",
    year_of_release= 1980,
    description="desc1"
)

test_book2 = models.Book(
    title="Chłopi",
    author="Reymont",
    year_of_release= 1988,
    description="desc2"
)

mocked_db_data2 = [test_book1, test_book2]

@patch("src.database.MongoClient")
def test_Database_init(mocked_database):
    database_instance = MagicMock()
    database_instance.server_info.return_value = "some server info"
    database_instance.__getitem__.return_value.__getitem__.return_value = mocked_db_data
    mocked_database.return_value = database_instance
    database_object = Database()
    assert database_object.books_collection == mocked_db_data

@patch("src.database.MongoClient")
def test_Database_init_error(mocked_database):
    database_instance = Mock()
    database_instance.server_info.side_effect = ServerSelectionTimeoutError(message="mocked error")
    mocked_database.return_value = database_instance
    with pytest.raises(HTTPException) as e_info:
        Database()
    assert "status_code=503, detail='Problem with connecting to Database" in str(e_info)

@patch("src.database.MongoClient")
def test_Database_init_error2(mocked_database):
    database_instance = Mock()
    database_instance.server_info.side_effect = TypeError()
    mocked_database.return_value = database_instance
    with pytest.raises(TypeError) as e_info:
        Database()

@pytest.fixture
def mocked_database_fix():
    with patch("src.database.MongoClient") as mocked_database:
        database_instance = MagicMock()
        database_instance.server_info.return_value = "some server info"
        database_instance.__getitem__.return_value.__getitem__.return_value = mocked_db_data2
        mocked_database.return_value =database_instance
        yield mocked_database

def test_database_init2(mocked_database_fix):
    database_object = Database()
    assert database_object.books_collection == mocked_db_data2

def test_Database_get_all_books(mocked_database_fix):
    database_object = Database()
    mocked_collection = Mock()
    mocked_collection.find.return_value = test_book1
    database_object.books_collection = mocked_collection
    result = database_object.get_all_books()
    assert result == [('title', 'Wesele'), ('author', 'Wyspiański'), ('year_of_release', 1980), ('description', 'desc1')]

def test_Database_get_one_book(mocked_database_fix):
    database_object = Database()
    mocked_collection = Mock()
    mocked_collection.find_one.return_value = test_book1
    database_object.books_collection = mocked_collection
    result = database_object.get_one_book(book_title = "Wesele")
    assert result == test_book1

def test_Database_get_one_book_error(mocked_database_fix):
    database_object = Database()
    mocked_collection = Mock()
    mocked_collection.find_one.return_value = None
    database_object.books_collection = mocked_collection
    with pytest.raises(HTTPException) as e_info:
        database_object.get_one_book(book_title = "Wesele")
    assert "status_code=404, detail='Book with title Wesele not found in database'" in str(e_info)

def test_Database_update_book(mocked_database_fix):
    database_object = Database()
    mocked_book_data = Mock()
    mocked_book_data.modified_count = 1
    mocked_collection = Mock()
    mocked_collection.replace_one.return_value = mocked_book_data
    database_object.books_collection = mocked_collection
    result = database_object.update_book(book = test_book1)
    assert result == {"info": f"Book with title {test_book1.title} modified in database"}

def test_Database_update_book_error(mocked_database_fix):
    database_object = Database()
    mocked_book_data = Mock()
    mocked_book_data.modified_count = 0
    mocked_collection = Mock()
    mocked_collection.replace_one.return_value = mocked_book_data
    database_object.books_collection = mocked_collection
    with pytest.raises(HTTPException) as e_info:
        database_object.update_book(book = test_book1)
    assert f"status_code=404, detail='Book with title {test_book1.title} not found in database'"

def test_Database_delete_book(mocked_database_fix):
    database_object = Database()
    mocked_book_data = Mock()
    mocked_book_data.deleted_count = 1
    mocked_collection = Mock()
    mocked_collection.delete_one.return_value = mocked_book_data
    database_object.books_collection = mocked_collection
    result = database_object.delete_book(book_title = "Wesele")
    assert result == {"info": f"Book with title {test_book1.title} deleted from database"}

def test_Database_delete_book_error(mocked_database_fix):
    database_object = Database()
    mocked_book_data = Mock()
    mocked_book_data.deleted_count = 0
    mocked_collection = Mock()
    mocked_collection.delete_one.return_value = mocked_book_data
    database_object.books_collection = mocked_collection
    with pytest.raises(HTTPException) as e_info:
        database_object.delete_book(book_title = "Wesele")
    assert f"status_code=404, detail='Book with title {test_book1.title} not found in database'"    

@pytest.fixture()
def mocked_collection_fix():
    mocked_book_data = Mock()
    mocked_book_data.deleted_count = 1
    mocked_book_data.modified_count = 1
    mocked_collection = Mock()
    mocked_collection.delete_one.return_value = mocked_book_data
    mocked_collection.replace_one.return_value = mocked_book_data
    mocked_collection.insert_one.return_value = mocked_book_data
    return mocked_collection

@pytest.fixture()
def mocked_collection_fix_error():
    mocked_book_data = Mock()
    mocked_book_data.deleted_count = 0
    mocked_book_data.modified_count = 0
    mocked_collection = Mock()
    # mocked_collection.delete_one.return_value = mocked_book_data
    # mocked_collection.replace_one.return_value = mocked_book_data
    mocked_collection.insert_one.side_effect = DuplicateKeyError(error= "MockedError")
    return mocked_collection

def test_Database_delete_book2(mocked_database_fix, mocked_collection_fix):
    database_object = Database()
    database_object.books_collection = mocked_collection_fix
    result = database_object.delete_book(book_title = "Wesele")
    assert result == {"info": f"Book with title {test_book1.title} deleted from database"}

def test_Database_add_book(mocked_database_fix, mocked_collection_fix):
    database_object = Database()
    database_object.books_collection = mocked_collection_fix
    result = database_object.add_book(book= test_book1)
    assert result == {"info": f"Book with title {test_book1.title} added to database"}  

def test_Database_add_book_error(mocked_collection_fix, mocked_collection_fix_error):
    database_object = Database()
    database_object.books_collection = mocked_collection_fix_error
    with pytest.raises(HTTPException) as e_info:
        database_object.add_book(book=test_book1)
    assert f"status_code=409, detail='Book with title {test_book1.title} already exists'"    
