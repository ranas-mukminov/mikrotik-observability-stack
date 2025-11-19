from pathlib import Path

import pytest

from mosctl.config_loader import ConfigLoaderError, load_devices_config


def test_load_valid_config(tmp_path: Path) -> None:
    config_file = tmp_path / "devices.yml"
    config_file.write_text(
        """
routers:
  - name: test
    address: 10.0.0.1
    exporter: routeros
    username: u
    password: p
"""
    )
    result = load_devices_config(config_file)
    assert result.config.routers[0].name == "test"


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ConfigLoaderError):
        load_devices_config(tmp_path / "missing.yml")


def test_invalid_yaml(tmp_path: Path) -> None:
    config_file = tmp_path / "broken.yml"
    config_file.write_text("routers: [")
    with pytest.raises(ConfigLoaderError):
        load_devices_config(config_file)


def test_missing_credentials_for_routeros(tmp_path: Path) -> None:
    config_file = tmp_path / "devices.yml"
    config_file.write_text(
        """
routers:
  - name: test
    address: 10.0.0.1
    exporter: routeros
    username: admin
"""
    )
    with pytest.raises(ConfigLoaderError, match="requires username and password"):
        load_devices_config(config_file)


def test_invalid_exporter_type(tmp_path: Path) -> None:
    config_file = tmp_path / "devices.yml"
    config_file.write_text(
        """
routers:
  - name: test
    address: 10.0.0.1
    exporter: bogus
    username: admin
    password: secret
"""
    )
    with pytest.raises(ConfigLoaderError):
        load_devices_config(config_file)


def test_snmp_requires_snmp_block(tmp_path: Path) -> None:
    config_file = tmp_path / "devices.yml"
    config_file.write_text(
        """
routers:
  - name: snmp-only
    address: 10.0.0.10
    exporter: snmp
    username: snmp
    password: secret
"""
    )
    with pytest.raises(ConfigLoaderError, match="requires snmp settings block"):
        load_devices_config(config_file)
