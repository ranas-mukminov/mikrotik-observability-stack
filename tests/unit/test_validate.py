from mosctl.config_loader import DevicesConfig, Device, SNMPSettings
from mosctl.validate import validate_devices


def test_detects_duplicates() -> None:
    config = DevicesConfig(
        routers=[
            Device(name="a", address="10.0.0.1", exporter="routeros", username="u", password="p"),
            Device(name="a", address="10.0.0.2", exporter="routeros", username="u", password="p"),
        ]
    )
    errors = validate_devices(config)
    assert any("duplicate device name" in err for err in errors)


def test_accepts_valid_config() -> None:
    config = DevicesConfig(
        routers=[
            Device(name="a", address="10.0.0.1", exporter="routeros", username="u", password="p"),
            Device(
                name="b",
                address="10.0.0.2",
                exporter="snmp",
                username="u",
                password="p",
                snmp=SNMPSettings(version="2c", community="obs", port=161),
            ),
        ]
    )
    errors = validate_devices(config)
    assert errors == []


def test_detects_duplicate_addresses() -> None:
    config = DevicesConfig(
        routers=[
            Device(name="a", address="10.0.0.1", exporter="routeros", username="u", password="p"),
            Device(name="b", address="10.0.0.1", exporter="routeros", username="u", password="p"),
        ]
    )
    errors = validate_devices(config)
    assert any("duplicate address" in err for err in errors)


def test_requires_router_entries() -> None:
    config = DevicesConfig(routers=[])
    errors = validate_devices(config)
    assert "no routers defined" in errors


def test_invalid_label_keys_are_reported() -> None:
    config = DevicesConfig(
        routers=[
            Device(
                name="a",
                address="10.0.0.1",
                exporter="routeros",
                username="u",
                password="p",
                labels={"bad key": "value"},
            )
        ]
    )
    errors = validate_devices(config)
    assert any("contains whitespace" in err for err in errors)


def test_empty_label_values_are_reported() -> None:
    config = DevicesConfig(
        routers=[
            Device(
                name="a",
                address="10.0.0.1",
                exporter="routeros",
                username="u",
                password="p",
                labels={"empty": ""},
            )
        ]
    )
    errors = validate_devices(config)
    assert any("is empty" in err for err in errors)
