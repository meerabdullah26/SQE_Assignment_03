"""Core calculator logic with a safe arithmetic evaluator."""

from __future__ import annotations

import ast
from dataclasses import dataclass


class CalculationError(ValueError):
    """Raised when an expression cannot be evaluated safely."""


@dataclass(slots=True)
class Calculator:
    """Calculator operations that are independent from any UI."""

    def evaluate(self, expression: str) -> float:
        """Evaluate a math expression using a restricted AST.

        Supported operators:
        - Binary: +, -, *, /, %
        - Unary: +, -
        - Parentheses and numeric literals
        """
        sanitized = expression.strip()
        if not sanitized:
            raise CalculationError("Expression cannot be empty")

        try:
            parsed = ast.parse(sanitized, mode="eval")
        except SyntaxError as exc:
            raise CalculationError("Invalid expression") from exc

        result = self._eval_node(parsed.body)
        return float(result)

    def toggle_sign(self, value: str) -> str:
        """Toggle the sign of a numeric string representation."""
        current = value.strip()
        if not current:
            return "-"
        if current.startswith("-"):
            return current[1:]
        return f"-{current}"

    def backspace(self, value: str) -> str:
        """Remove the last character from a string."""
        return value[:-1]

    def _eval_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            return -operand

        if isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)
        ):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self._apply_binary_operator(left, right, node.op)

        raise CalculationError("Unsupported expression")

    def _apply_binary_operator(
        self, left: float, right: float, operator: ast.operator
    ) -> float:
        if isinstance(operator, ast.Add):
            return left + right
        if isinstance(operator, ast.Sub):
            return left - right
        if isinstance(operator, ast.Mult):
            return left * right
        if isinstance(operator, ast.Div):
            if right == 0:
                raise CalculationError("Division by zero")
            return left / right
        if isinstance(operator, ast.Mod):
            if right == 0:
                raise CalculationError("Modulo by zero")
            return left % right
        raise CalculationError("Unsupported operator")
