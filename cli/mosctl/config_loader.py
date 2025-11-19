"""Configuration loader for MikroTik devices."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Literal, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError, model_validator

ExporterType = Literal["routeros", "snmp"]


class SNMPSettings(BaseModel):
    """Settings for SNMP exporters."""

    version: Literal["2c", "3"] = "2c"
    community: str = Field(..., min_length=1)
    port: int = Field(161, ge=1, le=65535)


class Device(BaseModel):
    """Representation of a MikroTik device entry."""

    name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=3)
    exporter: ExporterType
    api_port: int = Field(8728, ge=1, le=65535)
    username: Optional[str] = None
    password: Optional[str] = None
    snmp: Optional[SNMPSettings] = None
    labels: Dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_credentials(self) -> "Device":
        if self.exporter == "routeros":
            if not self.username or not self.password:
                raise ValueError("routeros exporter requires username and password")
        if self.exporter == "snmp" and self.snmp is None:
            raise ValueError("snmp exporter requires snmp settings block")
        return self

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.address})"


class DevicesConfig(BaseModel):
    """Top-level configuration."""

    routers: List[Device]


@dataclass
class ConfigLoadResult:
    path: Path
    config: DevicesConfig


class ConfigLoaderError(RuntimeError):
    """Raised when a configuration file cannot be parsed."""


def load_devices_config(path: Path) -> ConfigLoadResult:
    """Load and validate MikroTik devices configuration."""

    if not path.exists():
        raise ConfigLoaderError(f"Configuration file {path} does not exist")

    try:
        raw = yaml.safe_load(path.read_text()) or {}
        config = DevicesConfig(**raw)
    except (yaml.YAMLError, ValidationError, ValueError) as exc:
        raise ConfigLoaderError(f"Failed to parse {path}: {exc}") from exc

    return ConfigLoadResult(path=path, config=config)
