from fastapi.testclient import TestClient
from main import app
from unittest.mock import Mock, patch
import models
import pytest

client = TestClient(app)

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

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "<title>FastAPI - Swagger UI</title>" in response.text

# @pytest.fixture
# def mocked_database_fix(mocker):
#     return mocker.patch("main.Database")

@pytest.fixture
def mocked_database_fix2():
    with patch("main.Database") as mocked_database:
        database_instance = Mock()
        database_instance.get_all_books.return_value = [test_book1, test_book2]
        database_instance.get_one_book.return_value = test_book1
        database_instance.update_book.return_value = {"info": "Book with title Wesele modified in database"}
        database_instance.delete_book.return_value = {"info": "Book with title Wesele deleted from database"}
        database_instance.add_book.return_value = {"info": "Book with title Wesele added to database"}
        mocked_database.return_value = database_instance
        yield mocked_database

def test_all_books(mocked_database_fix2):
    response = client.get("/books")
    except_result = [{
        "title": "Wesele",
        "author": "Wyspiański",
        "year_of_release":  1980,
        "description": "desc1"
    },
    {
        "title": "Chłopi",
        "author": "Reymont",
        "year_of_release":  1988,
        "description": "desc2"
    }]
    assert response.status_code == 200
    assert response.json() == except_result

def test_book_one(mocked_database_fix2):
    response = client.get("/books/title_book")
    except_result = {
        "title": "Wesele",
        "author": "Wyspiański"
    }
    assert response.status_code == 200
    assert response.json() == except_result

def test_book_update(mocked_database_fix2):
    response = client.put("/books", json=test_book1.model_dump())
    assert response.status_code == 200
    assert response.json() == {"info": "Book with title Wesele modified in database"}

def test_delete_book(mocked_database_fix2):
    response = client.delete("/books/title_book")
    assert response.status_code == 200
    assert response.json() == {"info": "Book with title Wesele deleted from database"}

def test_add_book(mocked_database_fix2):
    response = client.post("/books", json=test_book1.model_dump())
    assert response.status_code == 201
    assert response.json() == {"info": "Book with title Wesele added to database"}

# @patch("main.Database")
# def test_all_books2(mocked_database_fix: Mock):
#     database_instance = Mock()
#     database_instance.get_all_books.return_value = [test_book1, test_book2]
#     mocked_database_fix.return_value = database_instance
#     response = client.get("/books")
#     except_result = [{
#         "title": "Wesele",
#         "author": "Wyspiański",
#         "year_of_release":  1980,
#         "description": "desc1"
#     },
#     {
#         "title": "Chłopi",
#         "author": "Reymont",
#         "year_of_release":  1988,
#         "description": "desc2"
#     }]
#     assert response.status_code == 200
#     assert response.json() == except_result

# @patch("main.Database")
# def test_all_books3(mocked_database: Mock):
#     mocked_database.return_value.get_all_books.return_value = [test_book1, test_book2]
#     response = client.get("/books")
#     except_result = [{
#         "title": "Wesele",
#         "author": "Wyspiański",
#         "year_of_release":  1980,
#         "description": "desc1"
#     },
#     {
#         "title": "Chłopi",
#         "author": "Reymont",
#         "year_of_release":  1988,
#         "description": "desc2"
#     }]
#     assert response.status_code == 200
#     assert response.json() == except_result