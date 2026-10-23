import pytest
from calc_app import cli


@pytest.mark.parametrize(("expression", "expected"), [
    ("0+0", "0"), ("9-12", "-3"), ("4*5", "20"),
    ("7/2", "3.5"), ("10%4", "2"),
])
def test_person2_cli_prints_results(monkeypatch, capsys, expression, expected):
    monkeypatch.setattr("sys.argv", ["calc", expression])
    cli.main()
    assert capsys.readouterr().out.strip() == expected


@pytest.mark.parametrize("expression", ["5/0", "5%0", "2**3", "abc"])
def test_person2_cli_exits_for_invalid_expression(monkeypatch, expression):
    monkeypatch.setattr("sys.argv", ["calc", expression])
    with pytest.raises(SystemExit, match="Error:"):
        cli.main()


def test_person2_cli_missing_argument_exits_with_usage(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["calc"])
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 2
    assert "usage:" in capsys.readouterr().err.lower()
