"""Command Line Interface (CLI) for Library project."""
import os
from io import StringIO
import pathlib
import rich
from rich.table import Table
from contextlib import contextmanager
from typing import List

import books

import typer

app = typer.Typer(add_completion=False)


@app.command()
def version():
    """Return version of Library application"""
    print(books.__version__)


@app.command()
def add(
    bookname: List[str], assigned_to: str = typer.Option(None, "-a", "--assigned_to")
):
    """Add a book to library database, while adding it can be assigned to Reader"""
    bookname = " ".join(bookname) if bookname else None
    with books_db() as db:
        db.add_book(books.Book(bookname, assigned_to, status="Available"))


@app.command()
def remove(book_sn: int):
    """Remove book from library db with given sn."""
    with books_db() as db:
        try:
            db.delete_book(book_sn)
        except books.InvalidBookSn:
            print(f"Error: Invalid book sn {book_sn}")


@app.command("list")
def list_books(
    assigned_to: str = typer.Option(None, "-a", "--assigned_to"),
    status: str = typer.Option(None, "-s", "--status"),
):
    """
    List books from library database.
    """
    with books_db() as db:
        the_books = db.list_books(assigned_to=assigned_to, status=status)
        table = Table(box=rich.box.SIMPLE)
        table.add_column("SN")
        table.add_column("Status")
        table.add_column("Assigned_To")
        table.add_column("BookName")
        for t in the_books:
            assigned_to = "" if t.assigned_to is None else t.assigned_to
            table.add_row(str(t.sn), t.status, assigned_to, t.bookname)
        out = StringIO()
        rich.print(table, file=out)
        print(out.getvalue())


@app.command()
def update(
    book_sn: int,
    assigned_to: str = typer.Option(None, "-a", "--assigned_to"),
    bookname: List[str] = typer.Option(None, "-b", "--bookname"),
):
    """Update a book in db with given sn with new info."""
    bookname = " ".join(bookname) if bookname else None
    with books_db() as db:
        try:
            db.update_book(
                book_sn, books.Book(bookname, assigned_to, status=None)
            )
        except books.InvalidBookSn:
            print(f"Error: Invalid book sn {book_sn}")


@app.command()
def issue(
    book_sn: int,
    assigned_to: str = typer.Option(None, "-a", "--assigned_to"),
):
    """Issue a book in db with given sn with new Reader"""
    with books_db() as db:
        try:
            db.update_book(
                book_sn, books.Book(assigned_to=assigned_to, status="Assigned")
            )
        except books.InvalidBookSn:
            print(f"Error: Invalid book sn {book_sn}")


@app.command()
def start(book_sn: int):
    """Set a book status to 'Assigning'."""
    with books_db() as db:
        try:
            db.start(book_sn)
        except books.InvalidBookSn:
            print(f"Error: Invalid book sn {book_sn}")


@app.command("return")
def finish(book_sn: int):
    """As book is returned to library set status to 'Avaiable'."""
    with books_db() as db:
        try:
            db.finish(book_sn)
        except books.InvalidBookSn:
            print(f"Error: Invalid book sn {book_sn}")


@app.command()
def config():
    """List the path to the Books db."""
    with books_db() as db:
        print(db.path())


@app.command()
def count():
    """Return number of books in library db."""
    with books_db() as db:
        print(db.count())


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Lib is a small command line book tracking application.
    """
    if ctx.invoked_subcommand is None:
        list_books(assigned_to=None, status=None)


def get_path():
    db_path_env = os.getenv("CARDS_DB_DIR", "")
    if db_path_env:
        db_path = pathlib.Path(db_path_env)
    else:
        db_path = pathlib.Path.home() / "bookslib_db"
    return db_path


@contextmanager
def books_db():
    db_path = get_path()
    db = books.BooksDB(db_path)
    yield db
    db.close()
