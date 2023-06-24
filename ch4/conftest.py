import books
import pytest


@pytest.fixture(scope="session")
def db(tmp_path_factory):
    """CardsDB object connected to a temporary database"""
    db_path = tmp_path_factory.mktemp("books_db")
    db_ = books.CardsDB(db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def books_db(db):
    """CardsDB object that's empty"""
    db.delete_all()
    return db


@pytest.fixture(scope="session")
def some_books():
    """List of different Card objects"""
    return [
        books.Card("write book", "Brian", "done"),
        books.Card("edit book", "Katie", "done"),
        books.Card("write 2nd edition", "Brian", "todo"),
        books.Card("edit 2nd edition", "Katie", "todo"),
    ]


@pytest.fixture(scope="function")
def non_empty_db(books_db, some_books):
    """CardsDB object that's been populated with 'some_books'"""
    for c in some_books:
        books_db.add_book(c)
    return books_db
