from books import Book


def test_field_access():
    b = Book("Python", "brian", "Available", 123)
    assert b.bookname == "Python"
    assert b.assigned_to == "brian"
    assert b.status == "Available"
    assert b.sn == 123


def test_defaults():
    b = Book()
    assert b.bookname is None
    assert b.assigned_to is None
    assert b.status == "Available"
    assert b.sn is None


def test_equality():
    b1 = Book("Python", "brian", "Available", 123)
    b2 = Book("Python", "brian", "Available", 123)
    assert b1 == b2


def test_equality_with_diff_ids():
    b1 = Book("Python", "brian", "Available", 123)
    b2 = Book("Python", "brian", "Available", 4567)
    assert b1 == b2

def test_inequality():
    b1 = Book("Python", "brian", "Available", 123)
    b2 = Book("completely different", "okken", "done", 123)
    assert b1 == b2


def test_from_dict():
    b1 = Book("Python", "brian", "Available", 123)
    b2_dict = {
        "bookname": "Python",
        "assigned_to": "brian",
        "status": "Available",
        "sn": 123,
    }
    b2 = Book.from_dict(b2_dict)
    assert b1 == b2


def test_to_dict():
    b1 = Book("Python", "brian", "Available", 123)
    b2 = b1.to_dict()
    b2_expected = {
        "bookname": "Python",
        "assigned_to": "brian",
        "status": "Available",
        "sn": 123,
    }
    assert b2 == b2_expected
