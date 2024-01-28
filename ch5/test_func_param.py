import pytest
from books import Book


@pytest.mark.parametrize(
    "book_name, status",
    [
        ("Python", "Available"),
        ("C++", "Assigning"),
        ("Kubernete", "Returned"),
    ],
)
def test_finish(books_db, book_name, status):
    initial_book = Book(bookname=book_name, status=status)
    index = books_db.add_book(initial_book)

    books_db.finish(index)

    book = books_db.get_book(index)
    assert book.status == "Available"



@pytest.mark.parametrize("status", ["Available", "Assigning", "Returned"])
def test_finish_simple(books_db, status):
    c = Book("write a book", status=status)
    index = books_db.add_book(c)
    books_db.finish(index)
    book = books_db.get_book(index)
    assert book.status == "Available"


