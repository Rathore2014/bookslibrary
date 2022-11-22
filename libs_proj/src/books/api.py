"""
API for the library project
"""
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

from .db import DB

__all__ = [
    "Book",
    "BooksDB",
    "BooksException",
    "MissingBookName",
    "InvalidBookSn",
]


@dataclass
class Book:
    bookname: str = None
    assigned_to: str = None
    status: str = "Available"
    sn: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, n):
        return Book(**n)
    def to_dict(self):
        return asdict(self)


class BooksException(Exception):
    pass


class MissingBookName(BooksException):
    pass


class InvalidBookSn(BooksException):
    pass


class BooksDB:
    def __init__(self, db_path):
        self._db_path = db_path
        self._db = DB(db_path, ".books_db")

    def add_book(self, book: Book) -> int:
        """Add a book, return the sn of book."""
        if not book.bookname:
            raise MissingBookName
        if book.assigned_to is None:
            book.assigned_to = ""
        sn = self._db.create(book.to_dict())
        self._db.update(sn, {"sn": sn})
        return sn

    def get_book(self, book_sn: int) -> Book:
        """Return a book with a matching sn."""
        db_item = self._db.read(book_sn)
        if db_item is not None:
            return Book.from_dict(db_item)
        else:
            raise InvalidBookSn(book_sn)

    def list_books(self, assigned_to=None, status=None):
        """Return a list of books."""
        all = self._db.read_all()
        if (assigned_to is not None) and (status is not None):
            return [
                Book.from_dict(t)
                for t in all
                if (t["assigned_to"] == assigned_to and t["status"] == status)
            ]
        elif assigned_to is not None:
            return [
                Book.from_dict(t) for t in all if t["assigned_to"] == assigned_to
            ]
        elif status is not None:
            return [
                Book.from_dict(t) for t in all if t["status"] == status
            ]
        else:
            return [Book.from_dict(t) for t in all]

    def count(self) -> int:
        """Return the number of books in db."""
        return self._db.count()

    def update_book(self, book_sn: int, book_mods: Book) -> None:
        """Update a book with modifications."""
        try:
            self._db.update(book_sn, book_mods.to_dict())
        except KeyError as exc:
            raise InvalidBookSn(book_sn) from exc

    def start(self, book_sn: int):
        """Set a book status to 'in prog'."""
        self.update_book(book_sn, Book(status="Assigning"))

    def finish(self, book_sn: int):
        """Set a book status to 'Released'."""
        self.update_book(book_sn, Book(status="Available", assigned_to="None"))

    def delete_book(self, book_sn: int) -> None:
        """Remove a book from db with given book_sn."""
        try:
            self._db.delete(book_sn)
        except KeyError as exc:
            raise InvalidBookSn(book_sn) from exc

    def delete_all(self) -> None:
        """Remove all books from db."""
        self._db.delete_all()

    def close(self):
        self._db.close()

    def path(self):
        return self._db_path
