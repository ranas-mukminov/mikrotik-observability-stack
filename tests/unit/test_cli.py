from pathlib import Path
from typer.testing import CliRunner

import mosctl.cli as cli

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
    result = runner.invoke(cli.app, ["print-plan"])
    assert result.exit_code == 0
    assert "Minimal profile" in result.stdout


def test_generate_targets(tmp_path: Path) -> None:
    cfg = tmp_path / "config.yml"
    write_sample_config(cfg)
    routeros_output = tmp_path / "routeros.json"
    snmp_output = tmp_path / "snmp.json"
    result = runner.invoke(
        cli.app,
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


def test_validate_config_valid(tmp_path: Path) -> None:
    cfg = tmp_path / "valid.yml"
    write_sample_config(cfg)
    result = runner.invoke(cli.app, ["validate-config", "--config", str(cfg)])
    assert result.exit_code == 0
    assert "Configuration valid" in result.stdout


def test_validate_config_invalid(tmp_path: Path) -> None:
    cfg = tmp_path / "invalid.yml"
    cfg.write_text(
        """
routers:
  - name: r1
    address: 10.0.0.1
    exporter: routeros
    username: u
    password: p
  - name: r1
    address: 10.0.0.2
    exporter: routeros
    username: u
    password: p
"""
    )
    result = runner.invoke(cli.app, ["validate-config", "--config", str(cfg)])
    assert result.exit_code == 2
    assert "duplicate device name" in result.stdout


def test_validate_config_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.yml"
    result = runner.invoke(cli.app, ["validate-config", "--config", str(missing)])
    assert result.exit_code == 1
    normalized = " ".join(result.stdout.split())
    assert "does not exist" in normalized


def test_check_connectivity(monkeypatch, tmp_path: Path) -> None:
    cfg = tmp_path / "devices.yml"
    write_sample_config(cfg)
    calls: list[str] = []

    def fake_router_reachable(device) -> bool:
        calls.append(device.name)
        return True

    monkeypatch.setattr(cli, "router_reachable", fake_router_reachable)
    result = runner.invoke(cli.app, ["check-connectivity", "--config", str(cfg)])
    assert result.exit_code == 0
    assert "Connectivity" in result.stdout
    assert calls == ["r1", "r2"]


def test_resolve_config_path_returns_absolute(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "devices.yml"
    write_sample_config(cfg)
    monkeypatch.chdir(tmp_path)
    resolved = cli.resolve_config_path(cfg)
    assert resolved == cfg


def test_resolve_config_path_prefers_current_directory(monkeypatch, tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    default_file = config_dir / "mikrotik-devices.yml"
    default_file.write_text("routers: []")
    monkeypatch.chdir(tmp_path)
    resolved = cli.resolve_config_path(None)
    assert resolved == default_file


def test_resolve_config_path_falls_back_to_example(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    resolved = cli.resolve_config_path(None)
    expected = (cli.PROJECT_ROOT / cli.FALLBACK_CONFIG).resolve()
    assert resolved == expected
