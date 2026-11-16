import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

environment = os.environ.get("ENVIRONMENT")

books = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"},
]

next_book_id = 3

REQUIRED_FIELDS = ("title", "author")


def missing_fields(data):
    if not data:
        return list(REQUIRED_FIELDS)
    return [field for field in REQUIRED_FIELDS if field not in data]


def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


@app.route("/health")
def health():
    return {
        "status": "okay",
        "environment": environment
    }


@app.route("/books", methods=["GET"])
def get_books():
    author = request.args.get("author")
    if author:
        return [book for book in books if book["author"].lower() == author.lower()]
    return books


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)
    if book is None:
        return {"error": "Book not found"}, 404
    return book


@app.route("/books", methods=["POST"])
def create_book():
    global next_book_id

    data = request.get_json(silent=True)
    missing = missing_fields(data)
    if missing:
        return {"error": f"Missing required field(s): {', '.join(missing)}"}, 400

    book = {
        "id": next_book_id,
        "title": data["title"],
        "author": data["author"]
    }

    next_book_id += 1
    books.append(book)

    return book, 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json(silent=True)
    missing = missing_fields(data)
    if missing:
        return {"error": f"Missing required field(s): {', '.join(missing)}"}, 400

    book = find_book(book_id)
    if book is None:
        return {"error": "Book not found"}, 404

    book["title"] = data["title"]
    book["author"] = data["author"]
    return book


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)
    if book is None:
        return {"error": "Book not found"}, 404

    books.remove(book)
    return "", 204
