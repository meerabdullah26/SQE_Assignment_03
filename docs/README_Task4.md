# Task 4 — Parallel execution, test suites/groups, parameterization, and order

## Files
- `pytest.ini`: registers test-group markers.
- `conftest.py`: automatically tags existing test files as `core`, `cli`, `ui`, or `task3`.
- `tests/test_task4_suite_demo.py`: demonstrates parameterized cases, groups, and ordering.
- Keep your existing six Task 2 test files and Task 3 CSV test.

## Add to your repository
Copy `pytest.ini` and `conftest.py` into the repository root. Copy `test_task4_suite_demo.py` into the existing `tests` folder. If `pytest.ini` or `conftest.py` already exists, merge the settings/code rather than overwriting it. Do not replace your whole `tests` folder.

## Install the Task 4 plugins
From the repository root, activate the same virtual environment used for Task 2, then run:
```bash
python -m pip install pytest pytest-xdist pytest-order
```

## Run all tests
```bash
python -m pytest -v
```

## Run groups/suites separately
```bash
python -m pytest -v -m core
python -m pytest -v -m cli
python -m pytest -v -m ui
python -m pytest -v -m task3
```
The markers are assigned automatically from the test filename by `conftest.py`.

## Run tests in parallel
```bash
python -m pytest -v -n auto
```
If `auto` is not supported in your environment, use a fixed number such as `-n 2`.

## Run the ordered demonstration suite
```bash
python -m pytest -v tests/test_task4_suite_demo.py
```
`pytest-order` uses `@pytest.mark.order(...)` to order the demonstration tests. The three parameterized operations are individual test cases.

## Important note about ordering and parallel execution
A global execution order cannot be guaranteed when tests run in parallel across multiple workers. Use the ordered command without `-n` when you need to demonstrate a specific sequence; use `-n auto` separately to demonstrate parallel execution. Tests should ideally be independent and not depend on a previous test's state.

## Evidence and reporting
Run the commands yourself and capture the actual terminal output/screenshots for your report or video. Do not claim tests passed until you have run them in your local repository. If a marker group reports no tests, inspect filenames and the marker assignment in `conftest.py`.
