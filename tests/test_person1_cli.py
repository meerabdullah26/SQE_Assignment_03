import pytest
from calc_app import cli


@pytest.mark.parametrize(("expression", "expected"), [
    ("2+3", "5"), ("10-4", "6"), ("3*7", "21"),
    ("8/2", "4"), ("1/2", "0.5"),
])
def test_person1_cli_prints_results(monkeypatch, capsys, expression, expected):
    monkeypatch.setattr("sys.argv", ["calc", expression])
    cli.main()
    assert capsys.readouterr().out.strip() == expected


@pytest.mark.parametrize("expression", ["1/0", "2+"])
def test_person1_cli_reports_calculation_errors(monkeypatch, expression):
    monkeypatch.setattr("sys.argv", ["calc", expression])
    with pytest.raises(SystemExit, match="Error:"):
        cli.main()


def test_person1_cli_missing_expression_exits(monkeypatch):
    monkeypatch.setattr("sys.argv", ["calc"])
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 2
