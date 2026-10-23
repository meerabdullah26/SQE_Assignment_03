"""Small Task 4 demonstration of parameterization, groups, and ordering.

These are demonstration tests for the Calculator core. Existing test files remain
unchanged. The order markers work when pytest-order is installed and tests are
run without parallel workers.
"""
import pytest
from calc_app.core import Calculator, CalculationError


@pytest.mark.task4
@pytest.mark.core
@pytest.mark.order(1)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1+1", 2.0),
        ("5-2", 3.0),
        ("3*4", 12.0),
    ],
    ids=["addition", "subtraction", "multiplication"],
)
def test_task4_basic_operations_in_order(expression, expected):
    assert Calculator().evaluate(expression) == pytest.approx(expected)


@pytest.mark.task4
@pytest.mark.core
@pytest.mark.order(2)
def test_task4_division_by_zero_error():
    with pytest.raises(CalculationError):
        Calculator().evaluate("5/0")


@pytest.mark.task4
@pytest.mark.core
@pytest.mark.order(3)
def test_task4_parentheses_precedence():
    assert Calculator().evaluate("2*(3+4)") == pytest.approx(14.0)
