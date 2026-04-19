from __future__ import annotations

from pathlib import Path

import prometheus


def test_package_importable() -> None:
    assert prometheus.__version__ == "0.0.0"


def test_dev_config_example_is_safe() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    dev_yaml = repo_root / "configs" / "dev.example.yaml"
    assert dev_yaml.exists(), f"missing {dev_yaml}"
    text = dev_yaml.read_text(encoding="utf-8")
    assert "exchange_write_enabled: false" in text
    assert "real_capital_enabled: false" in text
    assert "runtime_mode_on_start: SAFE_MODE" in text
