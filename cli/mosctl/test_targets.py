"""Connectivity helpers and Prometheus target generation."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Iterable, List, Tuple

from .config_loader import Device, DevicesConfig


def ping_host(address: str, attempts: int = 1, timeout: int = 1) -> bool:
    """Ping a host if the system ping command is available."""

    ping_bin = shutil.which("ping")
    if not ping_bin:
        return False

    try:
        result = subprocess.run(
            [ping_bin, "-c", str(attempts), "-W", str(timeout), address],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except OSError:
        return False


def tcp_probe(address: str, port: int, timeout: float = 3.0) -> bool:
    """Attempt a TCP connection."""

    try:
        with socket.create_connection((address, port), timeout=timeout):
            return True
    except OSError:
        return False


def router_reachable(device: Device) -> bool:
    if device.exporter == "routeros":
        return tcp_probe(device.address, device.api_port)
    return ping_host(device.address)


def build_routeros_targets(devices: Iterable[Device]) -> List[dict]:
    entries: List[dict] = []
    for device in devices:
        if device.exporter != "routeros":
            continue
        labels = {"router": device.name, "address": device.address, "exporter": device.exporter}
        labels.update(device.labels)
        entries.append({"targets": ["routeros-exporter:9436"], "labels": labels})
    return entries


def build_snmp_targets(devices: Iterable[Device]) -> List[dict]:
    entries: List[dict] = []
    for device in devices:
        if device.exporter != "snmp" or device.snmp is None:
            continue
        labels = {
            "router": device.name,
            "snmp_target": device.address,
            "exporter": device.exporter,
        }
        labels.update(device.labels)
        entries.append({"targets": ["snmp-exporter:9116"], "labels": labels})
    return entries


def write_file_sd(entries: List[dict], path: Path) -> None:
    """Persist Prometheus file_sd entries with explicit permission checks."""

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RuntimeError(f"Failed to create directory {path.parent}: {exc}") from exc

    if not os.access(path.parent, os.W_OK):
        raise RuntimeError(f"Directory {path.parent} is not writable")

    payload = json.dumps(entries, indent=2, sort_keys=True)
    try:
        path.write_text(payload)
    except OSError as exc:
        raise RuntimeError(f"Failed to write {path}: {exc}") from exc


def generate_file_sd(
    config: DevicesConfig, routeros_path: Path, snmp_path: Path
) -> Tuple[int, int]:
    router_entries = build_routeros_targets(config.routers)
    snmp_entries = build_snmp_targets(config.routers)
    write_file_sd(router_entries, routeros_path)
    write_file_sd(snmp_entries, snmp_path)
    return len(router_entries), len(snmp_entries)
