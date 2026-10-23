"""Task 4: assign suite markers automatically based on test filename.

This allows commands such as:
    python -m pytest -m core
    python -m pytest -m cli
    python -m pytest -m ui
    python -m pytest -m task3
"""
import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        name = item.path.name.lower()
        if "core" in name:
            item.add_marker(pytest.mark.core)
        elif "cli" in name:
            item.add_marker(pytest.mark.cli)
        elif "ui" in name:
            item.add_marker(pytest.mark.ui)
        elif "task3" in name:
            item.add_marker(pytest.mark.task3)
        elif "task4" in name:
            item.add_marker(pytest.mark.task4)
