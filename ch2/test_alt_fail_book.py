import pytest
from books import Book


def test_with_fail():
    b1 = Book("C++", "Luksa")
    b2 = Book("Java", "Manning")
    if b1 != b2:
        pytest.fail("they don't match")
