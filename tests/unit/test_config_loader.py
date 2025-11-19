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
