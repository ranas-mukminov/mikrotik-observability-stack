"""Additional validation helpers."""
from __future__ import annotations

from typing import List

from .config_loader import DevicesConfig

SUPPORTED_EXPORTERS = {"routeros", "snmp"}


def validate_devices(config: DevicesConfig) -> List[str]:
    """Return a list of validation error messages."""

    errors: List[str] = []
    seen_names: set[str] = set()
    seen_addresses: set[str] = set()

    for device in config.routers:
        if device.name in seen_names:
            errors.append(f"duplicate device name: {device.name}")
        else:
            seen_names.add(device.name)

        if device.address in seen_addresses:
            errors.append(f"duplicate address: {device.address}")
        else:
            seen_addresses.add(device.address)

        if device.exporter not in SUPPORTED_EXPORTERS:
            errors.append(f"unsupported exporter '{device.exporter}' on {device.name}")

        for key, value in device.labels.items():
            if " " in key:
                errors.append(f"label '{key}' on {device.name} contains whitespace")
            if not value:
                errors.append(f"label '{key}' on {device.name} is empty")

    if not config.routers:
        errors.append("no routers defined")

    return errors
