from io import StringIO

import pytest
from click.testing import CliRunner

import scp.cli
from scp.cli import cli
from scp.water import Water


def test_cli_reports_verbose_property_output() -> None:
    result = CliRunner().invoke(cli, ["--fluid", "water", "--property", "density", "--temperature", "25"])

    assert result.exit_code == 0
    assert "Fluid:    water" in result.output
    assert "Property: density" in result.output
    assert "Units:    [kg/m3]" in result.output


def test_cli_reports_quick_property_output() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "propylene_glycol",
            "--concentration",
            "0.4",
            "--property",
            "density",
            "--temperature",
            "20",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert float(result.output) == pytest.approx(1032.3, rel=0.001)


def test_cli_uses_freeze_point_concentration() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "propylene_glycol",
            "--concentration",
            "0.4",
            "--property",
            "freeze_point",
            "--temperature",
            "20",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert float(result.output) == pytest.approx(-20.568, abs=0.01)


def test_cli_zero_mixture_concentration_uses_water(monkeypatch) -> None:
    stderr = StringIO()
    monkeypatch.setattr(scp.cli, "stderr", stderr)

    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "propylene_glycol",
            "--property",
            "density",
            "--temperature",
            "25",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert "Mixture requested, but concentration zero" in stderr.getvalue()
    assert float(result.output) == pytest.approx(Water().density(25.0))


def test_cli_nonzero_water_concentration_uses_water(monkeypatch) -> None:
    stderr = StringIO()
    monkeypatch.setattr(scp.cli, "stderr", stderr)

    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "water",
            "--concentration",
            "0.4",
            "--property",
            "density",
            "--temperature",
            "25",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert "Pure water requested, but nonzero concentration entered" in stderr.getvalue()
    assert float(result.output) == pytest.approx(Water().density(25.0))
