import math
import pytest

# Adjust the import to match your module name/file.
# If your functions sit in calculator.py, this works:
from calculator import add, subtract, multiply, divide

@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0, 0),
        (1, 2, 3),
        (-5, 3, -2),
        (1.5, 2.5, 4.0),
        (1e12, 1e12, 2e12),
    ],
)
def test_add(x, y, expected):
    assert add(x, y) == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0, 0),
        (5, 2, 3),
        (-5, -3, -2),
        (2.5, 1.25, 1.25),
        (1e12, 1e6, 1e12 - 1e6),
    ],
)
def test_subtract(x, y, expected):
    assert subtract(x, y) == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0, 0),
        (3, 0, 0),
        (3, 4, 12),
        (-2, 8, -16),
        (1.5, 2, 3.0),
    ],
)
def test_multiply(x, y, expected):
    assert multiply(x, y) == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (4, 2, 2.0),
        (-9, 3, -3.0),
        (7.5, 2.5, 3.0),
        (1, 3, 1 / 3),  # floating division
    ],
)
def test_divide(x, y, expected):
    assert divide(x, y) == expected


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


# Some simple algebraic properties (nice extra checks)

@pytest.mark.parametrize("x, y", [(0, 0), (1, 2), (-3, 7), (1.5, 2.25)])
def test_add_commutative(x, y):
    assert add(x, y) == add(y, x)


@pytest.mark.parametrize("x, y", [(0, 0), (1, 2), (-3, 7), (1.5, 2.25)])
def test_multiply_commutative(x, y):
    assert multiply(x, y) == multiply(y, x)


@pytest.mark.parametrize("x", [0, 1, -4, 2.5])
def test_multiply_identity(x):
    assert multiply(x, 1) == x
    assert multiply(x, 0) == 0


@pytest.mark.parametrize("x", [0, 1, -4, 2.5])
def test_divide_identity(x):
    assert divide(x, 1) == x
