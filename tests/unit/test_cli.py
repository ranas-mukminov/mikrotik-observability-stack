from pathlib import Path

from typer.testing import CliRunner

from mosctl.cli import app

runner = CliRunner()


def write_sample_config(path: Path) -> None:
    path.write_text(
        """
routers:
  - name: r1
    address: 10.0.0.1
    exporter: routeros
    username: u
    password: p
  - name: r2
    address: 10.0.0.2
    exporter: snmp
    username: u
    password: p
    snmp:
      version: 2c
      community: obs
      port: 161
"""
    )


def test_print_plan() -> None:
    result = runner.invoke(app, ["print-plan"])
    assert result.exit_code == 0
    assert "Minimal profile" in result.stdout


def test_generate_targets(tmp_path: Path) -> None:
    cfg = tmp_path / "config.yml"
    write_sample_config(cfg)
    routeros_output = tmp_path / "routeros.json"
    snmp_output = tmp_path / "snmp.json"
    result = runner.invoke(
        app,
        [
            "generate-prometheus-targets",
            "--config",
            str(cfg),
            "--routeros-output",
            str(routeros_output),
            "--snmp-output",
            str(snmp_output),
        ],
    )
    assert result.exit_code == 0
    assert routeros_output.exists()
    assert snmp_output.exists()
