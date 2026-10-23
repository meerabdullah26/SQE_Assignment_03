Here are the testing notes for each module in your SQA Assignment 3. You can use these notes in your assignment documentation to explain what will be tested, which test cases will be used, and what each test is intended to verify.

# Testing Notes for Each Module

## 1. `core.py` — Core Calculator Module

Purpose: To test the calculator's main logic, mathematical operations, and input handling without involving the GUI.

| Function / Class                      | What will be tested                                                                                                                                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CalculationError`                    | Verify that it behaves as a `ValueError` and that expected error messages are raised.                                                                                                                                           |
| `Calculator.evaluate()`               | Test addition, subtraction, multiplication, division, modulo, operator precedence, decimal numbers, and negative numbers. Also test empty input, invalid syntax, division by zero, modulo by zero, and unsupported expressions. |
| `Calculator.toggle_sign()`            | Test empty strings, whitespace, positive numbers, negative numbers, and values containing text.                                                                                                                                 |
| `Calculator.backspace()`              | Test empty input, a single character, multiple characters, negative numbers, and text input.                                                                                                                                    |
| `Calculator._eval_node()`             | Test numeric constants, unary plus, unary minus, binary expressions, and unsupported AST nodes.                                                                                                                                 |
| `Calculator._apply_binary_operator()` | Test all supported operators (`+`, `-`, `*`, `/`, `%`), division by zero, modulo by zero, and unsupported operators.                                                                                                            |
| `Calculator` class                    | Test that its methods work together correctly when evaluating expressions and handling input.                                                                                                                                   |

### Example test cases

- Input: `2+3` → Expected: `5.0`
- Input: `2*(3+4)` → Expected: `14.0`
- Input: `1/0` → Expected: `CalculationError`
- Input: empty string → Expected: `CalculationError`
- Input: `-12` for `toggle_sign()` → Expected: `12`

## 2. `cli.py` — Command-Line Interface Module

Purpose: To verify that the command-line interface accepts expressions, calls the calculator correctly, displays results, and reports errors.

| Function / Component | What will be tested                                                                                            |
| -------------------- | -------------------------------------------------------------------------------------------------------------- |
| `main()`             | Verify that it reads the expression from command-line arguments and invokes the calculator.                    |
| Argument parsing     | Test valid input, missing arguments, and malformed expressions.                                                |
| Result formatting    | Verify that whole-number results are printed without `.0`, while decimal results retain their decimal portion. |
| Error handling       | Verify that `CalculationError` produces a user-readable error message and exits.                               |
| Module entry point   | Verify that the CLI starts when executed as a script.                                                          |

### Example test cases

- Input: `2+3` → Expected output: `5`
- Input: `1/2` → Expected output: `0.5`
- Input: `10%4` → Expected output: `2`
- Input: `1/0` → Expected: error message and program exit
- Input: no expression → Expected: argument-parsing error

## 3. `ui.py` — Graphical User Interface Module

Purpose: To test the calculator's GUI behavior, display updates, button actions, and interaction with the core calculator.

| Function / Component                    | What will be tested                                                                               |
| --------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `CalculatorApp.__init__()`              | Verify that the window, display, button frame, and calculator instance are initialized.           |
| `CalculatorApp.run()`                   | Verify that the GUI event loop starts.                                                            |
| `CalculatorApp._insert()`               | Test inserting digits, decimal points, and operators into the display.                            |
| `CalculatorApp._clear()`                | Verify that the display is cleared regardless of its previous contents.                           |
| `CalculatorApp._backspace()`            | Verify that the final character is removed from the display.                                      |
| `CalculatorApp._toggle_sign()`          | Test changing positive values to negative and negative values to positive, including empty input. |
| `CalculatorApp._calculate()`            | Test valid expressions, decimal results, and errors such as division by zero and invalid syntax.  |
| `CalculatorApp._format_result()`        | Test formatting whole numbers, decimals, zero, and negative results.                              |
| `CalculatorApp._build_buttons()`        | Verify that operation buttons are created and connected to their intended actions.                |
| `CalculatorApp._build_number_buttons()` | Verify that number and decimal-point buttons are created with the correct labels and callbacks.   |
| `main()`                                | Verify that the application is created and its `run()` method is called.                          |

### Example test cases

- Display contains `123`; press backspace → Expected: `12`
- Display contains `123`; press clear → Expected: empty display
- Display contains `2+3`; calculate → Expected: `5`
- Display contains `1/0`; calculate → Expected: `Error`
- Format `2.0` → Expected: `"2"`
- Format `2.5` → Expected: `"2.5"`

Testing approach: GUI tests can use fake Tkinter widgets so that display and button behavior can be tested without opening a real window.

## Summary of module testing

| Module    | Main focus                                            | Testing technique                  |
| --------- | ----------------------------------------------------- | ---------------------------------- |
| `core.py` | Mathematical logic and error handling                 | Unit tests and parameterized tests |
| `cli.py`  | Input arguments, output, and program exits            | Unit tests with mocked arguments   |
| `ui.py`   | Display behavior, button actions, and GUI integration | Unit tests with simulated widgets  |

These notes describe the intended test coverage. Before submitting, compare them with your actual test files and confirm that every listed behavior is implemented as a test.