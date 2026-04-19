from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from prometheus.core.errors import ManifestError
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.manifests import (
    DatasetManifest,
    InvalidWindow,
    read_manifest,
    write_manifest,
)


def _valid_payload() -> dict[str, object]:
    return {
        "dataset_name": "synthetic_btcusdt_15m",
        "dataset_version": "synthetic_btcusdt_15m__v001",
        "dataset_category": "normalized_kline",
        "created_at_utc_ms": 1_774_224_000_000,
        "canonical_timezone": "UTC",
        "canonical_timestamp_format": "unix_milliseconds",
        "symbols": (Symbol.BTCUSDT,),
        "intervals": (Interval.I_15M,),
        "sources": ("synthetic:phase-2-test",),
        "schema_version": "kline_v1",
        "pipeline_version": "prometheus@0.0.0",
        "partitioning": ("symbol", "interval", "year", "month"),
        "primary_key": ("symbol", "interval", "open_time"),
        "generator": "FixtureKlineSource",
        "predecessor_version": None,
        "invalid_windows": (),
        "notes": "",
    }


def test_valid_manifest_constructs() -> None:
    manifest = DatasetManifest(**_valid_payload())  # type: ignore[arg-type]
    assert manifest.dataset_name == "synthetic_btcusdt_15m"


def test_version_pattern_rejects_missing_suffix() -> None:
    payload = _valid_payload()
    payload["dataset_version"] = "synthetic_btcusdt_15m"
    with pytest.raises(ValidationError):
        DatasetManifest(**payload)  # type: ignore[arg-type]


def test_version_prefix_must_match_name() -> None:
    payload = _valid_payload()
    payload["dataset_version"] = "other_name__v001"
    with pytest.raises(ValidationError):
        DatasetManifest(**payload)  # type: ignore[arg-type]


def test_predecessor_cannot_equal_current() -> None:
    payload = _valid_payload()
    payload["predecessor_version"] = payload["dataset_version"]
    with pytest.raises(ValidationError):
        DatasetManifest(**payload)  # type: ignore[arg-type]


def test_valid_predecessor_accepted() -> None:
    payload = _valid_payload()
    payload["predecessor_version"] = "synthetic_btcusdt_15m__v000"
    DatasetManifest(**payload)  # type: ignore[arg-type]


def test_extra_fields_rejected() -> None:
    payload = _valid_payload()
    payload["surprise"] = "no"
    with pytest.raises(ValidationError):
        DatasetManifest(**payload)  # type: ignore[arg-type]


def test_empty_symbols_rejected() -> None:
    payload = _valid_payload()
    payload["symbols"] = ()
    with pytest.raises(ValidationError):
        DatasetManifest(**payload)  # type: ignore[arg-type]


def test_invalid_window_range_rejected() -> None:
    with pytest.raises(ValidationError):
        InvalidWindow(
            start_open_time_ms=1_000,
            end_open_time_ms=500,
            reason="backwards",
        )


def test_write_then_read_round_trip(tmp_path: Path) -> None:
    manifest = DatasetManifest(**_valid_payload())  # type: ignore[arg-type]
    path = tmp_path / "manifests" / "synthetic_btcusdt_15m__v001.manifest.json"
    write_manifest(path, manifest)
    loaded = read_manifest(path)
    assert loaded == manifest


def test_write_refuses_to_overwrite(tmp_path: Path) -> None:
    manifest = DatasetManifest(**_valid_payload())  # type: ignore[arg-type]
    path = tmp_path / "m.json"
    write_manifest(path, manifest)
    with pytest.raises(ManifestError):
        write_manifest(path, manifest)


def test_read_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ManifestError):
        read_manifest(tmp_path / "absent.json")


def test_stored_file_is_pretty_printed_json(tmp_path: Path) -> None:
    manifest = DatasetManifest(**_valid_payload())  # type: ignore[arg-type]
    path = tmp_path / "m.json"
    write_manifest(path, manifest)
    text = path.read_text(encoding="utf-8")
    parsed = json.loads(text)
    assert parsed["dataset_name"] == "synthetic_btcusdt_15m"
    assert "\n" in text  # indented output
