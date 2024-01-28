import pytest
from books import Book


@pytest.fixture(params=["Available", "Assigning", "Returned"])
def start_state(request):
    return request.param


def test_finish(books_db, start_state):
    c = Book("write a book", status=start_state)
    index = books_db.add_book(c)
    books_db.finish(index)
    book = books_db.get_book(index)
    assert book.status == "Available"
