from fastapi.testclient import TestClient
from main import app
from unittest.mock import Mock, patch
import models

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

@patch("main.Database")
def test_all_books2(mocked_database: Mock):
    database_instance = Mock()
    database_instance.get_all_books.return_value = [test_book1, test_book2]
    mocked_database.return_value = database_instance
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

# @patch("main.Database")
# def test_all_books(mocked_database: Mock):
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