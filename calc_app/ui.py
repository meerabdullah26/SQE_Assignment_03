"""Tkinter GUI for the calculator."""

from __future__ import annotations

import tkinter as tk

from .core import CalculationError, Calculator


class CalculatorApp:
    def __init__(self) -> None:
        self.calculator = Calculator()

        self.window = tk.Tk()
        self.window.configure(bg="#15155D")
        self.window.title("My Calculator")
        self.window.geometry("500x700")

        self.display = tk.Entry(
            self.window,
            font=("Arial", 60),
            justify="right",
            bg="#D3D8CD",
        )
        self.display.pack(
            padx=10,
            pady=20,
            fill="x",
            ipady=25,
        )

        self.button_frame = tk.Frame(self.window, bg="#B08F85")
        self.button_frame.pack()

        self._build_buttons()

    def run(self) -> None:
        self.window.mainloop()

    def _insert(self, value: str) -> None:
        self.display.insert(tk.END, value)

    def _clear(self) -> None:
        self.display.delete(0, tk.END)

    def _backspace(self) -> None:
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, self.calculator.backspace(current))

    def _toggle_sign(self) -> None:
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, self.calculator.toggle_sign(current))

    def _calculate(self) -> None:
        expression = self.display.get()
        try:
            result = self.calculator.evaluate(expression)
            self.display.delete(0, tk.END)
            self.display.insert(0, self._format_result(result))
        except CalculationError:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")

    @staticmethod
    def _format_result(value: float) -> str:
        if value.is_integer():
            return str(int(value))
        return str(value)

    def _build_buttons(self) -> None:
        tk.Button(
            self.button_frame,
            text="=",
            font=("Arial", 20),
            width=6,
            height=2,
            command=self._calculate,
            bg="#DADA12",
        ).grid(row=4, column=3, padx=5, pady=5)

        tk.Button(
            self.button_frame,
            text="+",
            font=("Arial", 20),
            width=6,
            height=2,
            command=lambda: self._insert("+"),
            bg="#A785D8",
        ).grid(row=3, column=3, padx=5, pady=5)
        tk.Button(
            self.button_frame,
            text="-",
            font=("Arial", 20),
            width=6,
            height=2,
            command=lambda: self._insert("-"),
            bg="#A785D8",
        ).grid(row=2, column=3, padx=5, pady=5)
        tk.Button(
            self.button_frame,
            text="x",
            font=("Arial", 20),
            width=6,
            height=2,
            command=lambda: self._insert("*"),
            bg="#A785D8",
        ).grid(row=1, column=3, padx=5, pady=5)
        tk.Button(
            self.button_frame,
            text="/",
            font=("Arial", 20),
            width=6,
            height=2,
            command=lambda: self._insert("/"),
            bg="#A785D8",
        ).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(
            self.button_frame,
            text="%",
            font=("Arial", 20),
            width=6,
            height=2,
            command=lambda: self._insert("%"),
            bg="#A785D8",
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            self.button_frame,
            text="+/-",
            font=("Arial", 20),
            width=6,
            height=2,
            command=self._toggle_sign,
            bg="#A785D8",
        ).grid(row=4, column=0, padx=5, pady=5)

        tk.Button(
            self.button_frame,
            text="C",
            font=("Arial", 20),
            width=6,
            height=2,
            command=self._clear,
            bg="#DB5D27",
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(
            self.button_frame,
            text="⌫",
            font=("Arial", 20),
            width=6,
            height=2,
            command=self._backspace,
            bg="#4893A5",
        ).grid(row=0, column=1, padx=5, pady=5)

        self._build_number_buttons()

    def _build_number_buttons(self) -> None:
        positions = [
            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("0", 4, 1),
            (".", 4, 2),
        ]

        for label, row, column in positions:
            tk.Button(
                self.button_frame,
                text=label,
                font=("Arial", 20),
                width=6,
                height=2,
                command=lambda char=label: self._insert(char),
            ).grid(row=row, column=column)


def main() -> None:
    app = CalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
