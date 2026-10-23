import ast
import pytest
from calc_app.core import Calculator, CalculationError


@pytest.mark.parametrize(("expression", "expected"), [
    ("0+0", 0.0), ("-3+8", 5.0), ("2*0", 0.0),
    ("7/2", 3.5), ("(10-2)%3", 2.0),
])
def test_person2_evaluate_valid_expressions(expression, expected):
    assert Calculator().evaluate(expression) == expected


@pytest.mark.parametrize("expression", ["(", "2//3", "4/0", "3%0", "2**3"])
def test_person2_evaluate_rejects_invalid_or_unsupported_expressions(expression):
    with pytest.raises(CalculationError):
        Calculator().evaluate(expression)


@pytest.mark.parametrize(("value", "expected"), [
    ("9", "-9"), ("-0", "0"), ("--4", "-4"), ("abc", "-abc"), ("  -8 ", "8 "),
])
def test_person2_toggle_sign(value, expected):
    assert Calculator().toggle_sign(value) == expected


@pytest.mark.parametrize(("value", "expected"), [
    ("a", ""), ("abcd", "abc"), ("1000", "100"), ("-12", "-1"), ("  ", " "),
])
def test_person2_backspace(value, expected):
    assert Calculator().backspace(value) == expected


@pytest.mark.parametrize(("expression", "expected"), [
    ("3.5", 3.5), ("-2.5", -2.5), ("+9", 9.0), ("5-8", -3.0), ("6*7", 42.0),
])
def test_person2_eval_node_supported_ast_nodes(expression, expected):
    node = ast.parse(expression, mode="eval").body
    assert Calculator()._eval_node(node) == expected


@pytest.mark.parametrize(("left", "right", "operator", "expected"), [
    (5, 7, ast.Add(), 12), (5, 7, ast.Sub(), -2), (3, 5, ast.Mult(), 15),
    (7, 2, ast.Div(), 3.5), (7, 4, ast.Mod(), 3),
])
def test_person2_apply_binary_operator(left, right, operator, expected):
    assert Calculator()._apply_binary_operator(left, right, operator) == expected


def test_person2_division_by_zero_raises_calculation_error():
    with pytest.raises(CalculationError, match="Division by zero"):
        Calculator()._apply_binary_operator(1, 0, ast.Div())


def test_person2_modulo_by_zero_raises_calculation_error():
    with pytest.raises(CalculationError, match="Modulo by zero"):
        Calculator()._apply_binary_operator(1, 0, ast.Mod())


def test_person2_unsupported_ast_node_raises_calculation_error():
    node = ast.parse("some_name", mode="eval").body
    with pytest.raises(CalculationError, match="Unsupported expression"):
        Calculator()._eval_node(node)


def test_person2_unsupported_operator_raises_calculation_error():
    with pytest.raises(CalculationError, match="Unsupported operator"):
        Calculator()._apply_binary_operator(2, 3, ast.Pow())
