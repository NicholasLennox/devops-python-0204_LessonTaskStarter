import pytest
from src.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Health check

def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_status_ok(client):
    response = client.get("/health")
    data = response.get_json()
    assert data["status"] == "broken"


def test_health_returns_environment(client):
    response = client.get("/health")
    data = response.get_json()
    assert data["environment"]


# Get all books

def test_get_books_returns_200(client):
    response = client.get("/books")
    assert response.status_code == 200


def test_get_books_returns_list(client):
    response = client.get("/books")
    assert isinstance(response.get_json(), list)


def test_get_books_filter_by_author(client):
    response = client.get("/books?author=robert c. martin")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Clean Code"


def test_get_books_filter_by_unknown_author_returns_empty_list(client):
    response = client.get("/books?author=Nobody")
    assert response.get_json() == []


# Get book by ID

def test_get_existing_book_returns_200(client):
    response = client.get("/books/2")
    assert response.status_code == 200


def test_get_existing_book_returns_correct_id(client):
    response = client.get("/books/2")
    data = response.get_json()
    assert data["id"] == 2


def test_get_missing_book_returns_404(client):
    response = client.get("/books/999")
    assert response.status_code == 404


# Create book

def test_create_book_returns_201(client):
    response = client.post(
        "/books",
        json={"title": "Test Book", "author": "Test Author"}
    )
    assert response.status_code == 201


def test_create_book_returns_correct_fields(client):
    response = client.post(
        "/books",
        json={"title": "Test Book", "author": "Test Author"}
    )
    data = response.get_json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"


def test_create_book_missing_title_returns_400(client):
    response = client.post("/books", json={"author": "Test Author"})
    assert response.status_code == 400


def test_create_book_missing_author_returns_400(client):
    response = client.post("/books", json={"title": "Test Book"})
    assert response.status_code == 400


# Update book

def test_update_existing_book_returns_200(client):
    response = client.put(
        "/books/2",
        json={"title": "Updated Title", "author": "Updated Author"}
    )
    assert response.status_code == 200


def test_update_existing_book_returns_updated_fields(client):
    response = client.put(
        "/books/2",
        json={"title": "Updated Title", "author": "Updated Author"}
    )
    data = response.get_json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"


def test_update_missing_book_returns_404(client):
    response = client.put(
        "/books/999",
        json={"title": "Updated Title", "author": "Updated Author"}
    )
    assert response.status_code == 404


def test_update_book_missing_fields_returns_400(client):
    response = client.put("/books/2", json={})
    assert response.status_code == 400


# Delete book

def test_delete_existing_book_returns_204(client):
    response = client.delete("/books/1")
    assert response.status_code == 204


def test_delete_missing_book_returns_404(client):
    response = client.delete("/books/999")
    assert response.status_code == 404
