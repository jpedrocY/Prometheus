"""Tests for the microstructure manifest data model (Phase 4aw)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.invalid_window import (
    DownstreamEligibilityAction,
    InvalidWindow,
    InvalidWindowReason,
    InvalidWindowSeverity,
)
from prometheus.research.microstructure.manifest import (
    EligibilityGateStatus,
    FileEntry,
    ManifestImmutableError,
    MicrostructureManifest,
)


def _valid_manifest() -> MicrostructureManifest:
    return MicrostructureManifest(
        dataset_family="microstructure_raw_aggtrades_v001",
        version="v001",
        symbol="BTCUSDT",
        source="binance_usdm_futures_public",
        endpoint="@aggTrade",
        capture_mode="ws_live_capture_required",
        schema_version="v001",
        endpoint_docs_reference="phase-4at-section-6.1",
        capture_config_hash="abc",
        code_commit_sha="def",
        governance_labels={"stop_trigger_domain": "trade_price_backtest"},
    )


def _valid_file_entry(path: str = "raw/agg/btcusdt_2026-05-07.jsonl") -> FileEntry:
    return FileEntry(
        path=path,
        sha256="0" * 64,
        event_count=100,
        start_time_ms=1_000,
        end_time_ms=2_000,
    )


def _valid_window() -> InvalidWindow:
    return InvalidWindow(
        start_time_ms=1_500,
        end_time_ms=1_700,
        family="microstructure_raw_aggtrades_v001",
        symbol="BTCUSDT",
        reason=InvalidWindowReason.GAP_AFTER_RECONNECT,
        severity=InvalidWindowSeverity.WARN,
        downstream_eligibility_action=DownstreamEligibilityAction.FLAG,
        evidence={"gap_ms": 200},
    )


def test_default_research_eligible_is_false() -> None:
    m = _valid_manifest()
    assert m.research_eligible is False


def test_default_eligibility_gate_status_is_pending() -> None:
    m = _valid_manifest()
    assert m.eligibility_gate_status is EligibilityGateStatus.PENDING


def test_flip_research_eligible_always_raises() -> None:
    m = _valid_manifest()
    with pytest.raises(ManifestImmutableError):
        m.flip_research_eligible()


def test_append_file_updates_counters_and_window() -> None:
    m = _valid_manifest()
    m.append_file(_valid_file_entry("raw/a.jsonl"))
    m.append_file(
        FileEntry(
            path="raw/b.jsonl",
            sha256="1" * 64,
            event_count=50,
            start_time_ms=2_000,
            end_time_ms=3_000,
        )
    )
    assert m.file_count == 2
    assert m.event_count == 150
    assert m.start_time_ms == 1_000
    assert m.end_time_ms == 3_000


def test_append_invalid_window_appends() -> None:
    m = _valid_manifest()
    m.append_invalid_window(_valid_window())
    assert len(m.invalid_windows) == 1


def test_invalid_sha256_rejected() -> None:
    with pytest.raises(ValueError):
        FileEntry(
            path="raw/a.jsonl",
            sha256="too-short",
            event_count=1,
            start_time_ms=0,
            end_time_ms=0,
        )


def test_round_trip_to_from_dict() -> None:
    m = _valid_manifest()
    m.append_file(_valid_file_entry())
    m.append_invalid_window(_valid_window())
    restored = MicrostructureManifest.from_dict(m.to_dict())
    assert restored.dataset_family == m.dataset_family
    assert restored.file_count == 1
    assert restored.event_count == m.event_count
    assert restored.invalid_windows[0].reason is InvalidWindowReason.GAP_AFTER_RECONNECT


def test_save_to_tmp_path_and_load(tmp_path: Path) -> None:
    m = _valid_manifest()
    m.append_file(_valid_file_entry())
    target = tmp_path / "manifest.json"
    m.save(target)
    assert target.exists()
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["research_eligible"] is False
    assert payload["eligibility_gate_status"] == "pending"
    loaded = MicrostructureManifest.load(target)
    assert loaded.dataset_family == m.dataset_family


def test_save_refuses_to_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "manifest.json"
    target.write_text("{}", encoding="utf-8")
    m = _valid_manifest()
    with pytest.raises(ManifestImmutableError):
        m.save(target)


def test_serialized_payload_research_eligible_false_by_default() -> None:
    payload = _valid_manifest().to_dict()
    assert payload["research_eligible"] is False
    assert payload["eligibility_gate_status"] == "pending"


def test_empty_required_field_rejected() -> None:
    with pytest.raises(ValueError):
        MicrostructureManifest(
            dataset_family="",
            version="v001",
            symbol="BTCUSDT",
            source="binance_usdm_futures_public",
            endpoint="@aggTrade",
            capture_mode="ws_live_capture_required",
            schema_version="v001",
            endpoint_docs_reference="phase-4at-section-6.1",
            capture_config_hash="abc",
            code_commit_sha="def",
        )
