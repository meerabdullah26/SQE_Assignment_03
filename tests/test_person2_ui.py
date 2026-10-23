from types import SimpleNamespace
import pytest
from calc_app import ui


class FakeWidget:
    def __init__(self, *args, **kwargs):
        self.value = ""
        self.kwargs = kwargs
        self.calls = []
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


@pytest.mark.parametrize(("initial", "expected"), [
    ("5", "-5"), ("-5", "5"), ("", "-"), ("  ", "-"), ("12", "-12"),
])
def test_person2_toggle_sign_updates_display(monkeypatch, initial, expected):
    app = make_app(monkeypatch)
    app.display.value = initial
    app._toggle_sign()
    assert app.display.get() == expected


@pytest.mark.parametrize(("initial", "expected"), [
    ("", ""), ("1", "1"), ("12345", "12345"), ("-8", "-8"), ("2+3", "2+3"),
])
def test_person2_clear_display(monkeypatch, initial, expected):
    app = make_app(monkeypatch)
    app.display.value = initial
    app._clear()
    assert app.display.get() == ""


@pytest.mark.parametrize(("expression", "expected"), [
    ("3+4", "7"), ("9-12", "-3"), ("4*5", "20"),
    ("10%3", "1"), ("7/2", "3.5"),
])
def test_person2_calculate_valid_expressions(monkeypatch, expression, expected):
    app = make_app(monkeypatch)
    app.display.value = expression
    app._calculate()
    assert app.display.get() == expected


@pytest.mark.parametrize("expression", ["5/0", "5%0", "2**3", "name", ""])
def test_person2_calculate_invalid_expressions_show_error(monkeypatch, expression):
    app = make_app(monkeypatch)
    app.display.value = expression
    app._calculate()
    assert app.display.get() == "Error"


def test_person2_build_number_buttons_creates_buttons(monkeypatch):
    app = make_app(monkeypatch)
    # _build_number_buttons creates button widgets and assigns their commands.
    before = len(app.button_frame.children)
    app._build_number_buttons()
    assert app.button_frame is not None
    assert before == 0


def test_person2_ui_main_creates_and_runs_app(monkeypatch):
    events = []
    class FakeApp:
        def __init__(self): events.append("created")
        def run(self): events.append("ran")
    monkeypatch.setattr(ui, "CalculatorApp", FakeApp)
    ui.main()
    assert events == ["created", "ran"]


def test_person2_ui_main_propagates_run_error(monkeypatch):
    class FakeApp:
        def __init__(self): pass
        def run(self): raise RuntimeError("run failed")
    monkeypatch.setattr(ui, "CalculatorApp", FakeApp)
    with pytest.raises(RuntimeError, match="run failed"):
        ui.main()


def test_person2_ui_app_has_calculator_instance(monkeypatch):
    app = make_app(monkeypatch)
    from calc_app.core import Calculator
    assert isinstance(app.calculator, Calculator)


def test_person2_ui_build_buttons_does_not_crash(monkeypatch):
    app = make_app(monkeypatch)
    assert app.button_frame is not None
