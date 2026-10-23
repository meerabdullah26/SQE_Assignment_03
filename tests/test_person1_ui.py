from types import SimpleNamespace
import pytest
from calc_app import ui


class FakeWidget:
    def __init__(self, *args, **kwargs):
        self.value = ""
        self.kwargs = kwargs
        self.calls = []
        self.children = []

    def configure(self, *args, **kwargs): self.calls.append(("configure", args, kwargs))
    def title(self, *args): self.calls.append(("title", args))
    def geometry(self, *args): self.calls.append(("geometry", args))
    def pack(self, *args, **kwargs): self.calls.append(("pack", args, kwargs))
    def grid(self, *args, **kwargs): self.calls.append(("grid", args, kwargs))
    def mainloop(self): self.calls.append(("mainloop",))
    def insert(self, index, value):
        if index == 0: self.value = str(value) + self.value
        else: self.value += str(value)
    def delete(self, start, end=None): self.value = ""
    def get(self): return self.value


class FakeButton(FakeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = kwargs.get("command")
        self.label = kwargs.get("text")


def install_fake_tk(monkeypatch):
    monkeypatch.setattr(ui, "tk", SimpleNamespace(
        Tk=FakeWidget, Entry=FakeWidget, Frame=FakeWidget,
        Button=FakeButton, END="end"
    ))


def make_app(monkeypatch):
    install_fake_tk(monkeypatch)
    return ui.CalculatorApp()


def test_person1_app_initializes_window(monkeypatch):
    app = make_app(monkeypatch)
    assert app.window is not None
    assert ("title", ("My Calculator",)) in app.window.calls


def test_person1_app_initializes_display(monkeypatch):
    app = make_app(monkeypatch)
    assert app.display is not None
    assert app.display.kwargs["justify"] == "right"


def test_person1_app_creates_button_frame(monkeypatch):
    app = make_app(monkeypatch)
    assert app.button_frame is not None


def test_person1_run_calls_mainloop(monkeypatch):
    app = make_app(monkeypatch)
    app.run()
    assert ("mainloop",) in app.window.calls


@pytest.mark.parametrize(("value", "expected"), [
    (2.0, "2"), (2.5, "2.5"), (0.0, "0"), (-4.0, "-4"), (10.25, "10.25"),
])
def test_person1_format_result(value, expected):
    assert ui.CalculatorApp._format_result(value) == expected


@pytest.mark.parametrize(("initial", "insert", "expected"), [
    ("", "7", "7"), ("1", "2", "12"), ("-3", "4", "-34"),
    ("0", ".", "0."), ("55", "+", "55+"),
])
def test_person1_insert_adds_text(monkeypatch, initial, insert, expected):
    app = make_app(monkeypatch)
    app.display.value = initial
    app._insert(insert)
    assert app.display.get() == expected


@pytest.mark.parametrize(("initial", "expected"), [
    ("123", "12"), ("7", ""), ("", ""), ("-4", "-"), ("abc", "ab"),
])
def test_person1_backspace_updates_display(monkeypatch, initial, expected):
    app = make_app(monkeypatch)
    app.display.value = initial
    app._backspace()
    assert app.display.get() == expected


@pytest.mark.parametrize(("expression", "expected"), [
    ("2+3", "5"), ("8/2", "4"), ("1/2", "0.5"),
    ("1/0", "Error"), ("2+", "Error"),
])
def test_person1_calculate_updates_display(monkeypatch, expression, expected):
    app = make_app(monkeypatch)
    app.display.value = expression
    app._calculate()
    assert app.display.get() == expected


def test_person1_clear_empties_display(monkeypatch):
    app = make_app(monkeypatch)
    app.display.value = "123"
    app._clear()
    assert app.display.get() == ""
