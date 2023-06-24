from pathlib import Path
from tempfile import TemporaryDirectory
import books

import pytest


@pytest.fixture()
def books_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = books.BooksDB(db_path)
        yield db
        db.close()


def test_empty(books_db):
    assert books_db.count() == 0



def test_two(books_db):
    books_db.add_book(books.Book("first"))
    books_db.add_book(books.Book("second"))
    assert books_db.count() == 2


