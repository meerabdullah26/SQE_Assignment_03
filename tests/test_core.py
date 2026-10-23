from __future__ import annotations

import pytest

from calc_app.core import CalculationError, Calculator


@pytest.fixture()
def calculator() -> Calculator:
    return Calculator()


def test_addition(calculator: Calculator) -> None:
    assert calculator.evaluate("2+2") == 4.0


def test_operator_precedence(calculator: Calculator) -> None:
    assert calculator.evaluate("2+3*4") == 14.0


def test_parentheses(calculator: Calculator) -> None:
    assert calculator.evaluate("(2+3)*4") == 20.0


def test_unary_negative(calculator: Calculator) -> None:
    assert calculator.evaluate("-5+2") == -3.0


def test_modulo(calculator: Calculator) -> None:
    assert calculator.evaluate("10%3") == 1.0


def test_division_by_zero(calculator: Calculator) -> None:
    with pytest.raises(CalculationError, match="Division by zero"):
        calculator.evaluate("10/0")


def test_modulo_by_zero(calculator: Calculator) -> None:
    with pytest.raises(CalculationError, match="Modulo by zero"):
        calculator.evaluate("10%0")


def test_invalid_expression(calculator: Calculator) -> None:
    with pytest.raises(
        CalculationError, match="Invalid expression|Unsupported expression"
    ):
        calculator.evaluate("2+")


def test_unsupported_expression_function_call(calculator: Calculator) -> None:
    with pytest.raises(CalculationError, match="Unsupported expression"):
        calculator.evaluate("abs(-1)")


def test_empty_expression(calculator: Calculator) -> None:
    with pytest.raises(CalculationError, match="Expression cannot be empty"):
        calculator.evaluate("   ")


def test_toggle_sign(calculator: Calculator) -> None:
    assert calculator.toggle_sign("5") == "-5"
    assert calculator.toggle_sign("-5") == "5"


def test_backspace(calculator: Calculator) -> None:
    assert calculator.backspace("123") == "12"
    assert calculator.backspace("") == ""
