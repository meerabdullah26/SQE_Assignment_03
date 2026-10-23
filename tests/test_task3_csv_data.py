"""Task 3: parameterized unit tests that consume external CSV data."""
import csv
from pathlib import Path

import pytest
from calc_app.core import Calculator, CalculationError

CSV_PATH = Path(__file__).resolve().parents[1] / "test_data" / "task3_calculator_cases.csv"

def load_cases():
    with CSV_PATH.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

@pytest.mark.parametrize("case", load_cases(), ids=lambda case: case["test_id"])
def test_calculator_using_external_csv(case):
    calculator = Calculator()
    expression = case["expression"]
    if case["expected_type"] == "error":
        with pytest.raises(CalculationError):
            calculator.evaluate(expression)
    else:
        expected = float(case["expected_value"])
        assert calculator.evaluate(expression) == pytest.approx(expected)
