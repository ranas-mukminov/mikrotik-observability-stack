"""Entry point for mosctl."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .config_loader import ConfigLoaderError, load_devices_config
from .test_targets import generate_file_sd, router_reachable
from .validate import validate_devices

app = typer.Typer(help="Control utility for the MikroTik Observability Stack.")
console = Console()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = Path("config/mikrotik-devices.yml")
FALLBACK_CONFIG = Path("config/mikrotik-devices.example.yml")


def resolve_config_path(path: Optional[Path]) -> Path:
    """Return a resolved configuration path from user input or defaults."""

    cwd = Path.cwd()
    if path:
        expanded = path.expanduser()
        if expanded.is_absolute():
            return expanded
        return (cwd / expanded).resolve()

    search_roots = [cwd]
    if PROJECT_ROOT not in search_roots:
        search_roots.append(PROJECT_ROOT)

    for root in search_roots:
        candidate = (root / DEFAULT_CONFIG).resolve()
        if candidate.exists():
            return candidate

    for root in search_roots:
        candidate = (root / FALLBACK_CONFIG).resolve()
        if candidate.exists():
            return candidate

    # No file exists yet; return the fallback location under the project root.
    return (search_roots[-1] / FALLBACK_CONFIG).resolve()


@app.command("validate-config")
def validate_config_cmd(
    config: Optional[Path] = typer.Option(None, "--config", path_type=Path)
) -> None:
    """Validate a MikroTik device inventory file."""

    cfg_path = resolve_config_path(config)
    console.print(f"Validating [cyan]{cfg_path}[/cyan] ...")
    try:
        result = load_devices_config(cfg_path)
    except ConfigLoaderError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc

    errors = validate_devices(result.config)
    if errors:
        for error in errors:
            console.print(f"[red]- {error}[/red]")
        raise typer.Exit(2)

    console.print("[green]Configuration valid[/green]")


@app.command("check-connectivity")
def check_connectivity_cmd(
    config: Optional[Path] = typer.Option(None, "--config", path_type=Path),
) -> None:
    """Probe each router via API/SNMP reachability checks."""

    cfg_path = resolve_config_path(config)
    try:
        result = load_devices_config(cfg_path)
    except ConfigLoaderError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc

    table = Table(title="Connectivity", show_header=True, header_style="bold magenta")
    table.add_column("Router")
    table.add_column("Address")
    table.add_column("Exporter")
    table.add_column("Reachable")

    failures = 0
    for device in result.config.routers:
        ok = router_reachable(device)
        table.add_row(device.name, device.address, device.exporter, "✅" if ok else "❌")
        if not ok:
            failures += 1

    console.print(table)
    if failures:
        console.print(f"[red]{failures} device(s) unreachable[/red]")
        raise typer.Exit(3)


@app.command("generate-prometheus-targets")
def generate_targets_cmd(
    config: Optional[Path] = typer.Option(None, "--config", path_type=Path),
    routeros_output: Path = typer.Option(
        Path("docker/prometheus/file_sd/targets-mikrotik.json"),
        "--routeros-output",
        writable=True,
        path_type=Path,
    ),
    snmp_output: Path = typer.Option(
        Path("docker/prometheus/file_sd/snmp-targets.json"),
        "--snmp-output",
        writable=True,
        path_type=Path,
    ),
) -> None:
    """Render Prometheus file_sd JSON targets from the device inventory."""

    cfg_path = resolve_config_path(config)
    try:
        result = load_devices_config(cfg_path)
    except ConfigLoaderError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    try:
        router_count, snmp_count = generate_file_sd(result.config, routeros_output, snmp_output)
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(4) from exc
    console.print(f"[green]Wrote {router_count} routeros and {snmp_count} snmp targets[/green]")


@app.command("print-plan")
def print_plan_cmd() -> None:
    """Show which services run in minimal vs full profiles."""

    minimal = ["Prometheus", "Grafana", "RouterOS exporter"]
    full = minimal + ["SNMP exporter", "Loki", "Promtail", "Alertmanager"]

    console.print("[bold]Minimal profile[/bold]")
    for svc in minimal:
        console.print(f"  - {svc}")

    console.print("[bold]\nFull profile[/bold]")
    for svc in full:
        console.print(f"  - {svc}")


def main() -> None:  # pragma: no cover - console script
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
