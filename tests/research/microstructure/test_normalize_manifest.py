"""Phase 4bd tests for the derived-manifest builder."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure.invalid_window import (
    DownstreamEligibilityAction,
    InvalidWindow,
    InvalidWindowReason,
    InvalidWindowSeverity,
)
from prometheus.research.microstructure.manifest import (
    EligibilityGateStatus,
    ManifestImmutableError,
)
from prometheus.research.microstructure.normalize_manifest import (
    REQUIRED_GOVERNANCE_LABEL_KEYS,
    NormalizationManifestDraft,
    NormalizationManifestError,
    propagate_invalid_windows,
)


def _valid_governance() -> dict[str, str]:
    labels: dict[str, str] = {
        "phase": "4bd",
        "source_phase_boundary": "4bb-D",
        "source_dataset_family": "microstructure_raw_aggtrades_v001",
        "source_dataset_version": "v001",
        "source_manifest_path": "manifests/microstructure_raw_aggtrades_v001__v001.json",
        "source_manifest_sha256": "a" * 64,
        "source_raw_zip_path": "raw/microstructure_raw_aggtrades_v001/x.zip",
        "source_raw_zip_sha256": "f" * 64,
        "source_gate_report_id": "microstructure_raw_aggtrades_v001__v001__1__abc",
        "source_gate_report_sha256": "9" * 64,
        "source_gate_report_code_commit_sha": "a" * 40,
        "validator": "phase_4ax_aggtrades_v001",
        "stop_trigger_domain": "trade_price_backtest_candidate",
        "feature_computation": "forbidden",
        "strategy_use": "forbidden",
    }
    return labels


def _valid_draft(**overrides) -> NormalizationManifestDraft:
    base: dict = dict(
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        start_time_ms=1736899201000,
        end_time_ms=1736899208000,
        event_count=8,
        output_relative_path="normalized/.../BTCUSDT-aggTrades-2025-01-15.parquet",
        output_sha256="b" * 64,
        governance_labels=_valid_governance(),
        invalid_windows=(),
        capture_config_hash="cafe" * 16,
        code_commit_sha="0" * 40,
    )
    base.update(overrides)
    return NormalizationManifestDraft(**base)


def test_required_governance_label_keys_count() -> None:
    assert len(REQUIRED_GOVERNANCE_LABEL_KEYS) == 15


def test_draft_constructs_with_valid_input() -> None:
    draft = _valid_draft()
    assert draft.symbol == "BTCUSDT"


def test_draft_rejects_missing_governance_key() -> None:
    incomplete = _valid_governance()
    del incomplete["validator"]
    with pytest.raises(NormalizationManifestError):
        _valid_draft(governance_labels=incomplete)


def test_draft_rejects_feature_computation_allowed() -> None:
    bad = _valid_governance()
    bad["feature_computation"] = "allowed"
    with pytest.raises(NormalizationManifestError):
        _valid_draft(governance_labels=bad)


def test_draft_rejects_strategy_use_allowed() -> None:
    bad = _valid_governance()
    bad["strategy_use"] = "allowed"
    with pytest.raises(NormalizationManifestError):
        _valid_draft(governance_labels=bad)


def test_draft_rejects_lowercase_symbol() -> None:
    with pytest.raises(NormalizationManifestError):
        _valid_draft(symbol="btcusdt")


def test_draft_rejects_negative_event_count() -> None:
    with pytest.raises(NormalizationManifestError):
        _valid_draft(event_count=-1)


def test_draft_rejects_end_before_start() -> None:
    with pytest.raises(NormalizationManifestError):
        _valid_draft(start_time_ms=10, end_time_ms=5)


def test_draft_to_manifest_defaults_research_eligible_false() -> None:
    draft = _valid_draft()
    manifest = draft.to_manifest()
    assert manifest.research_eligible is False
    assert manifest.eligibility_gate_status == EligibilityGateStatus.PENDING


def test_to_manifest_records_one_file_entry() -> None:
    draft = _valid_draft()
    manifest = draft.to_manifest()
    assert manifest.file_count == 1
    assert manifest.event_count == draft.event_count
    assert manifest.files[0].sha256 == draft.output_sha256


def test_to_manifest_preserves_governance_labels() -> None:
    draft = _valid_draft()
    manifest = draft.to_manifest()
    for k in REQUIRED_GOVERNANCE_LABEL_KEYS:
        assert k in manifest.governance_labels


def test_to_manifest_flip_research_eligible_still_raises() -> None:
    draft = _valid_draft()
    manifest = draft.to_manifest()
    with pytest.raises(ManifestImmutableError):
        manifest.flip_research_eligible()


def test_propagate_invalid_windows_source_only() -> None:
    src = (
        InvalidWindow(
            start_time_ms=1, end_time_ms=2,
            family="microstructure_raw_aggtrades_v001",
            symbol="BTCUSDT",
            reason=InvalidWindowReason.MISSING_SEQUENCE,
            severity=InvalidWindowSeverity.WARN,
            downstream_eligibility_action=DownstreamEligibilityAction.FLAG,
            evidence={"row_index": 0},
        ),
    )
    out = propagate_invalid_windows(source_invalid_windows=src)
    assert len(out) == 1


def test_propagate_invalid_windows_runtime_appended() -> None:
    runtime = (
        InvalidWindow(
            start_time_ms=10, end_time_ms=20,
            family="microstructure_raw_aggtrades_v001",
            symbol="BTCUSDT",
            reason=InvalidWindowReason.OUT_OF_ORDER_EVENT,
            severity=InvalidWindowSeverity.ERROR,
            downstream_eligibility_action=DownstreamEligibilityAction.EXCLUDE,
            evidence={"row_index": 5},
        ),
    )
    out = propagate_invalid_windows(normalization_runtime_invalid_windows=runtime)
    assert len(out) == 1
