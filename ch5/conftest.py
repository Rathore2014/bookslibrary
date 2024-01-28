import books
import pytest


@pytest.fixture(scope="session")
def db(tmp_path_factory):
    """BooksDB object connected to a temporary database"""
    db_path = tmp_path_factory.mktemp("books_db")
    db_ = books.BooksDB(db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def books_db(db):
    """BooksDB object that's empty"""
    db.delete_all()
    return db


@pytest.fixture(scope="session")
def some_books():
    """List of different Book objects"""
    return [
        books.Book("write book", "Brian", "done"),
        books.Book("edit book", "Katie", "done"),
        books.Book("write 2nd edition", "Brian", "todo"),
        books.Book("edit 2nd edition", "Katie", "todo"),
    ]


@pytest.fixture(scope="function")
def non_empty_db(books_db, some_books):
    """BooksDB object that's been populated with 'some_books'"""
    for c in some_books:
        books_db.add_book(c)
    return books_db
