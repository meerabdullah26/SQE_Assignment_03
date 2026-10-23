import ast
import pytest
from calc_app.core import Calculator, CalculationError


@pytest.mark.parametrize(("expression", "expected"), [
    ("2+3", 5.0), ("9-4", 5.0), ("3*4", 12.0),
    ("8/2", 4.0), ("2*(3+4)", 14.0),
])
def test_person1_evaluate_valid_expressions(expression, expected):
    assert Calculator().evaluate(expression) == expected


@pytest.mark.parametrize("expression", ["", "   ", "2+", "1/0", "__import__('os')"])
def test_person1_evaluate_invalid_expressions(expression):
    with pytest.raises(CalculationError):
        Calculator().evaluate(expression)


@pytest.mark.parametrize(("value", "expected"), [
    ("", "-"), ("  ", "-"), ("12", "-12"), ("-12", "12"), (" 7 ", "-7"),
])
def test_person1_toggle_sign(value, expected):
    assert Calculator().toggle_sign(value) == expected


@pytest.mark.parametrize(("value", "expected"), [
    ("", ""), ("7", ""), ("123", "12"), ("-5", "-"), ("hello", "hell"),
])
def test_person1_backspace(value, expected):
    assert Calculator().backspace(value) == expected


@pytest.mark.parametrize(("expression", "expected"), [
    ("42", 42.0), ("+5", 5.0), ("-5", -5.0), ("2+3", 5.0), ("8%3", 2.0),
])
def test_person1_eval_node_supported_ast_nodes(expression, expected):
    node = ast.parse(expression, mode="eval").body
    assert Calculator()._eval_node(node) == expected


@pytest.mark.parametrize(("left", "right", "operator", "expected"), [
    (2, 3, ast.Add(), 5), (8, 3, ast.Sub(), 5), (2, 4, ast.Mult(), 8),
    (8, 2, ast.Div(), 4), (8, 3, ast.Mod(), 2),
])
def test_person1_apply_binary_operator(left, right, operator, expected):
    assert Calculator()._apply_binary_operator(left, right, operator) == expected


def test_person1_calculation_error_is_value_error():
    assert issubclass(CalculationError, ValueError)


@pytest.mark.parametrize(("expression", "expected"), [
    ("1+1", 2.0), ("10-3", 7.0), ("4*5", 20.0),
    ("9/3", 3.0), ("10%4", 2.0),
])
def test_person1_calculator_class_integration(expression, expected):
    calculator = Calculator()
    assert calculator.evaluate(expression) == expected
