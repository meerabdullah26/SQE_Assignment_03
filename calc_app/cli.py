"""CLI entry point for the calculator."""

from __future__ import annotations

import argparse

from .core import CalculationError, Calculator


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate a simple arithmetic expression"
    )
    parser.add_argument("expression", help="Expression to evaluate, e.g. '2*(3+4)'")
    args = parser.parse_args()

    calculator = Calculator()
    try:
        result = calculator.evaluate(args.expression)
    except CalculationError as exc:
        raise SystemExit(f"Error: {exc}")

    if result.is_integer():
        print(int(result))
    else:
        print(result)


if __name__ == "__main__":
    main()
