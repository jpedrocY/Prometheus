"""Phase 4bm-Q report data-model and invariant tests."""
# ruff: noqa: E501
from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure.multiday_label_gate_checks import (
    CHECK_ORDER,
    MultidayLabelGateCheckResult,
    MultidayLabelGateCheckStatus,
)
from prometheus.research.microstructure.multiday_label_gate_report import (
    ALLOWED_GATE_VERDICTS,
    GATE_VERDICT_FAIL,
    GATE_VERDICT_INDETERMINATE,
    GATE_VERDICT_PASS,
    MultidayLabelGateReportError,
    build_report,
)


def _all_pass_results() -> tuple[MultidayLabelGateCheckResult, ...]:
    return tuple(
        MultidayLabelGateCheckResult(
            check_id=cid, group=cid[0],
            status=MultidayLabelGateCheckStatus.PASS, blocking=True,
        )
        for cid in CHECK_ORDER
    )


def _manifest_stub() -> dict:
    return {"row_count": 155_153_449}


def test_verdict_pass_when_all_pass() -> None:
    rep = build_report(
        results=_all_pass_results(),
        manifest=_manifest_stub(),
        label_manifest_path=Path("data/microstructure/manifests/x.json"),
        created_at_utc_ms=1_700_000_000_000,
        code_commit_sha="abcdef0123456789",
        label_parquet_count=90,
        label_sidecar_count=90,
    )
    assert rep.gate_verdict == GATE_VERDICT_PASS
    assert rep.overall_status == "pass"
    assert rep.pass_count == len(CHECK_ORDER)
    assert rep.fail_count == 0
    assert rep.blocking_fail_count == 0


def test_verdict_fail_on_blocking_fail() -> None:
    results = list(_all_pass_results())
    results[0] = MultidayLabelGateCheckResult(
        check_id="A1", group="A", status=MultidayLabelGateCheckStatus.FAIL,
        blocking=True, expected="x", observed="y",
    )
    rep = build_report(
        results=tuple(results),
        manifest=_manifest_stub(),
        label_manifest_path=Path("data/microstructure/manifests/x.json"),
        created_at_utc_ms=1, code_commit_sha="abcdef0123",
        label_parquet_count=90, label_sidecar_count=90,
    )
    assert rep.gate_verdict == GATE_VERDICT_FAIL
    assert rep.overall_status == "fail"
    assert rep.blocking_fail_count == 1


def test_verdict_indeterminate_on_error_only() -> None:
    results = list(_all_pass_results())
    results[0] = MultidayLabelGateCheckResult(
        check_id="A1", group="A", status=MultidayLabelGateCheckStatus.ERROR,
        blocking=True, expected="", observed="exc",
    )
    rep = build_report(
        results=tuple(results),
        manifest=_manifest_stub(),
        label_manifest_path=Path("data/microstructure/manifests/x.json"),
        created_at_utc_ms=1, code_commit_sha="abcdef0123",
        label_parquet_count=90, label_sidecar_count=90,
    )
    assert rep.gate_verdict == GATE_VERDICT_INDETERMINATE


def test_report_hard_invariants_preserved() -> None:
    rep = build_report(
        results=_all_pass_results(),
        manifest=_manifest_stub(),
        label_manifest_path=Path("data/microstructure/manifests/x.json"),
        created_at_utc_ms=1, code_commit_sha="abcdef0123",
        label_parquet_count=90, label_sidecar_count=90,
    )
    assert rep.research_eligible_after is False
    assert rep.eligibility_gate_status_after == "pending"
    assert rep.stage_5_label_cleared_after is False
    assert rep.label_family_research_use_authorized_after is False
    assert rep.chronological_split_policy_after == "not_yet_defined"
    assert rep.label_family_eligibility_gate_authorized_after is False
    assert rep.successor_state_authorized is False
    for f in (
        rep.diagnostics_authorized,
        rep.ml_authorized,
        rep.strategy_authorized,
        rep.backtest_authorized,
        rep.acquisition_authorized,
    ):
        assert f is False
    for t in (
        rep.no_manifest_mutation,
        rep.no_successor_state_created,
        rep.no_label_recomputation,
        rep.no_diagnostics_computed,
        rep.no_signal_computed,
        rep.no_ml_trained,
        rep.no_strategy_created,
        rep.no_backtest_run,
        rep.no_network_io,
        rep.no_credentials,
        rep.no_mcp_or_graphify,
        rep.no_exchange_write,
        rep.retained_verdicts_preserved,
        rep.governance_locks_preserved,
    ):
        assert t is True


def test_report_to_dict_round_trip_contains_all_locked_fields() -> None:
    rep = build_report(
        results=_all_pass_results(),
        manifest=_manifest_stub(),
        label_manifest_path=Path("data/microstructure/manifests/x.json"),
        created_at_utc_ms=1, code_commit_sha="abcdef0123",
        label_parquet_count=90, label_sidecar_count=90,
    )
    d = rep.to_dict()
    assert d["phase_id"] == "4bm-Q"
    assert d["dataset_family"] == "microstructure_labels_aggtrades_v001"
    assert d["dataset_version"] == "v002"
    assert d["gate_verdict"] in ALLOWED_GATE_VERDICTS
    assert d["research_eligible_after"] is False
    assert d["eligibility_gate_status_after"] == "pending"
    assert d["stage_5_label_cleared_after"] is False
    assert d["label_family_research_use_authorized_after"] is False
    assert d["chronological_split_policy_after"] == "not_yet_defined"
    assert d["boundary_confirmations"]["phase_4aw_flip_research_eligible_invariant_preserved"] is True
    assert all(v is True for v in d["boundary_confirmations"].values())
    assert "LABEL_GATE_PASS" in d["notes"] or rep.gate_verdict == GATE_VERDICT_PASS


def test_report_construction_rejects_invariant_violation() -> None:
    # Build a report normally then attempt to construct one with a forbidden value.
    from prometheus.research.microstructure.multiday_label_gate_report import (
        MultidayLabelGateReport,
    )

    base = build_report(
        results=_all_pass_results(),
        manifest=_manifest_stub(),
        label_manifest_path=Path("data/microstructure/manifests/x.json"),
        created_at_utc_ms=1, code_commit_sha="abcdef0123",
        label_parquet_count=90, label_sidecar_count=90,
    )
    d = base.to_dict()
    d["research_eligible_after"] = True
    d.pop("checks")
    d.pop("boundary_confirmations")
    d.pop("censored_per_horizon")
    with pytest.raises(MultidayLabelGateReportError):
        MultidayLabelGateReport(
            **{k: v for k, v in d.items() if k in MultidayLabelGateReport.__dataclass_fields__},
            checks=base.checks,
            boundary_confirmations=base.boundary_confirmations,
            censored_per_horizon=base.censored_per_horizon,
        )
