from books import Book


def pytest_generate_tests(metafunc):
    if "start_state" in metafunc.fixturenames:
        metafunc.parametrize("start_state", ["Available", "Assining", "Returned"])


def test_finish(books_db, start_state):
    b = Book("write a book", status=start_state)
    index = books_db.add_book(b)
    books_db.finish(index)
    book = books_db.get_book(index)
    assert book.status == "Available"
