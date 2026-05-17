"""Phase 4bm-D multi-day gate-report data-model + atomic writer tests.

Mirrors Phase 4bf ``test_derived_gate_report.py`` but exercises the
multi-day variant: ``utc_date_start`` / ``utc_date_end`` / ``date_count``
fields, the ``gate_verdict`` taxonomy (PASS / FAIL / INCOMPLETE), the
``ALLOWED_GATE_VERDICTS`` / ``ALLOWED_OVERALL_STATUSES`` whitelists, and
the additional ``phase-4bm-d`` filename segment.

All tests use pytest ``tmp_path``; no real ``data/microstructure/`` tree
is touched.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from prometheus.research.microstructure.multiday_derived_gate_io import (
    GateIOError,
    compute_file_sha256,
)
from prometheus.research.microstructure.multiday_derived_gate_report import (
    ALLOWED_GATE_VERDICTS,
    ALLOWED_OVERALL_STATUSES,
    GATE_VERDICT_FAIL,
    GATE_VERDICT_INCOMPLETE,
    GATE_VERDICT_PASS,
    PHASE_ID,
    REPORT_SCHEMA_VERSION,
    MultidayDerivedAggTradesGateReport,
    build_report,
    write_gate_report,
)

# --------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------- #


def _output_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _build_default_report(
    *,
    overall_status: str = "pass",
    gate_verdict: str = GATE_VERDICT_PASS,
    generated_at_unix_ms: int = 1_700_000_000_000,
    code_commit_sha: str = "testcommit01abcdef",
) -> MultidayDerivedAggTradesGateReport:
    return build_report(
        report_id=(
            "microstructure_normalized_aggtrades_v001__v002__"
            "phase-4bm-d__1700000000000__testcommit01"
        ),
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v002",
        symbol="BTCUSDT",
        utc_date_start="2024-12-01",
        utc_date_end="2025-02-28",
        date_count=90,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
        input_artefacts={
            "derived_manifest_path": "data/microstructure/manifests/x.json",
            "derived_manifest_sha256": "a" * 64,
        },
        checks=[{"check_id": "4bm-d.13.1", "status": "pass"}],
        overall_status=overall_status,
        gate_verdict=gate_verdict,
        eligibility_gate_status_after="pass",
        boundary_confirmations={
            "no_manifest_mutation": True,
            "no_successor_authorization_emitted_by_gate": True,
        },
        measured_summary={"total_row_count": 5},
    )


def _make_unsafe_report(**overrides: Any) -> MultidayDerivedAggTradesGateReport:
    """Construct via the unsafe dataclass constructor for invariant tests."""
    defaults: dict[str, Any] = {
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "phase_id": PHASE_ID,
        "report_id": "x",
        "dataset_family": "microstructure_normalized_aggtrades_v001",
        "dataset_version": "v002",
        "symbol": "BTCUSDT",
        "utc_date_start": "2024-12-01",
        "utc_date_end": "2025-02-28",
        "date_count": 90,
        "generated_at_unix_ms": 1,
        "code_commit_sha": "abc",
        "input_artefacts": {},
        "checks": [],
        "overall_status": "pass",
        "gate_verdict": GATE_VERDICT_PASS,
        "research_eligible_after": False,
        "eligibility_gate_status_after": "pass",
        "no_successor_authorization": True,
        "boundary_confirmations": {},
        "measured_summary": {},
    }
    defaults.update(overrides)
    return MultidayDerivedAggTradesGateReport(**defaults)


# --------------------------------------------------------------------- #
# Constants and verdict taxonomy
# --------------------------------------------------------------------- #


def test_constants_have_expected_values() -> None:
    assert REPORT_SCHEMA_VERSION == "v001"
    assert PHASE_ID == "4bm-d"
    assert GATE_VERDICT_PASS == "DERIVED_GATE_PASS"
    assert GATE_VERDICT_FAIL == "DERIVED_GATE_FAIL"
    assert GATE_VERDICT_INCOMPLETE == "DERIVED_GATE_INCOMPLETE"


def test_allowed_gate_verdicts_contains_exactly_three() -> None:
    assert frozenset(
        {GATE_VERDICT_PASS, GATE_VERDICT_FAIL, GATE_VERDICT_INCOMPLETE}
    ) == ALLOWED_GATE_VERDICTS
    assert len(ALLOWED_GATE_VERDICTS) == 3


def test_allowed_overall_statuses_contains_three_lowercase_values() -> None:
    assert frozenset({"pass", "fail", "incomplete"}) == ALLOWED_OVERALL_STATUSES
    assert all(s == s.lower() for s in ALLOWED_OVERALL_STATUSES)


# --------------------------------------------------------------------- #
# build_report hard invariants
# --------------------------------------------------------------------- #


def test_build_report_records_invariants_and_phase_id() -> None:
    report = _build_default_report()
    assert report.research_eligible_after is False
    assert report.no_successor_authorization is True
    assert report.phase_id == PHASE_ID == "4bm-d"
    assert report.report_schema_version == REPORT_SCHEMA_VERSION == "v001"


def test_build_report_records_multiday_fields() -> None:
    report = _build_default_report()
    assert report.utc_date_start == "2024-12-01"
    assert report.utc_date_end == "2025-02-28"
    assert report.date_count == 90
    assert report.dataset_version == "v002"


def test_build_report_records_gate_verdict() -> None:
    report = _build_default_report(gate_verdict=GATE_VERDICT_FAIL, overall_status="fail")
    assert report.gate_verdict == GATE_VERDICT_FAIL
    assert report.overall_status == "fail"


def test_build_report_copies_input_artefacts_dict() -> None:
    src = {"k": "v"}
    report = build_report(
        report_id="x",
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v002",
        symbol="BTCUSDT",
        utc_date_start="2024-12-01",
        utc_date_end="2025-02-28",
        date_count=90,
        generated_at_unix_ms=1,
        code_commit_sha="abc",
        input_artefacts=src,
        checks=[],
        overall_status="pass",
        gate_verdict=GATE_VERDICT_PASS,
        eligibility_gate_status_after="pass",
        boundary_confirmations={},
        measured_summary={},
    )
    src["mutated"] = "after"
    assert "mutated" not in report.input_artefacts


def test_build_report_copies_checks_list() -> None:
    checks: list[dict[str, Any]] = [{"check_id": "4bm-d.13.1", "status": "pass"}]
    report = build_report(
        report_id="x",
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v002",
        symbol="BTCUSDT",
        utc_date_start="2024-12-01",
        utc_date_end="2025-02-28",
        date_count=90,
        generated_at_unix_ms=1,
        code_commit_sha="abc",
        input_artefacts={},
        checks=checks,
        overall_status="pass",
        gate_verdict=GATE_VERDICT_PASS,
        eligibility_gate_status_after="pass",
        boundary_confirmations={},
        measured_summary={},
    )
    checks.append({"check_id": "intruder", "status": "pass"})
    assert len(report.checks) == 1
    assert report.checks[0]["check_id"] == "4bm-d.13.1"


# --------------------------------------------------------------------- #
# to_dict
# --------------------------------------------------------------------- #


def test_to_dict_round_trips_through_json() -> None:
    report = _build_default_report()
    payload = report.to_dict()
    serialised = json.dumps(payload, sort_keys=True)
    reloaded = json.loads(serialised)
    assert reloaded["research_eligible_after"] is False
    assert reloaded["no_successor_authorization"] is True
    assert reloaded["gate_verdict"] == GATE_VERDICT_PASS
    assert reloaded["overall_status"] == "pass"
    assert reloaded["utc_date_start"] == "2024-12-01"
    assert reloaded["utc_date_end"] == "2025-02-28"
    assert reloaded["date_count"] == 90


def test_to_dict_returns_serialisable_payload() -> None:
    report = _build_default_report()
    payload = report.to_dict()
    text = json.dumps(payload, sort_keys=True, indent=2)
    assert "research_eligible_after" in text
    assert "no_successor_authorization" in text
    assert "gate_verdict" in text


def test_dataclass_is_frozen() -> None:
    report = _build_default_report()
    with pytest.raises(AttributeError):
        report.gate_verdict = GATE_VERDICT_FAIL  # type: ignore[misc]


# --------------------------------------------------------------------- #
# write_gate_report happy path
# --------------------------------------------------------------------- #


def test_write_gate_report_writes_json_and_sidecar(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    paths, sha, size = write_gate_report(report, output_root=output_root)
    assert paths.report_path.exists()
    assert paths.sidecar_path.exists()
    assert size > 0
    assert sha == compute_file_sha256(paths.report_path)
    sidecar_text = paths.sidecar_path.read_text(encoding="utf-8")
    assert sidecar_text == f"{sha}  {paths.report_path.name}\n"


def test_write_gate_report_path_is_under_normalized_namespace(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    parts = paths.report_path.resolve().parts
    assert parts[-5:-1] == ("data", "microstructure", "gate-reports", "normalized")


def test_write_gate_report_filename_contains_phase_segment(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    assert "phase-4bm-d" in paths.report_path.name


def test_write_gate_report_payload_is_sorted_and_indented(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    text = paths.report_path.read_text(encoding="utf-8")
    parsed = json.loads(text)
    assert isinstance(parsed, dict)
    # sort_keys=True implies first top-level key alphabetically comes first
    first_key = next(iter(parsed))
    assert first_key == sorted(parsed.keys())[0]
    # indent=2 implies multi-line output
    assert "\n" in text


def test_write_gate_report_includes_all_required_fields(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    parsed = json.loads(paths.report_path.read_text(encoding="utf-8"))
    for required_key in (
        "report_schema_version",
        "phase_id",
        "report_id",
        "dataset_family",
        "dataset_version",
        "symbol",
        "utc_date_start",
        "utc_date_end",
        "date_count",
        "generated_at_unix_ms",
        "code_commit_sha",
        "input_artefacts",
        "checks",
        "overall_status",
        "gate_verdict",
        "research_eligible_after",
        "eligibility_gate_status_after",
        "no_successor_authorization",
        "boundary_confirmations",
        "measured_summary",
    ):
        assert required_key in parsed, f"missing {required_key}"


# --------------------------------------------------------------------- #
# write_gate_report invariant rejections
# --------------------------------------------------------------------- #


def test_write_gate_report_rejects_research_eligible_after_true(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(research_eligible_after=True)
    with pytest.raises(GateIOError, match="research_eligible_after"):
        write_gate_report(bad, output_root=output_root)


def test_write_gate_report_rejects_no_successor_authorization_false(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(no_successor_authorization=False)
    with pytest.raises(GateIOError, match="no_successor_authorization"):
        write_gate_report(bad, output_root=output_root)


def test_invariant_rejection_aborts_before_any_file_write(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(research_eligible_after=True)
    with pytest.raises(GateIOError):
        write_gate_report(bad, output_root=output_root)
    # No files must have been written under the output root.
    assert list(output_root.iterdir()) == []


def test_write_gate_report_rejects_invalid_gate_verdict(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(gate_verdict="NOT_A_REAL_VERDICT")
    with pytest.raises(GateIOError, match="gate_verdict"):
        write_gate_report(bad, output_root=output_root)


def test_write_gate_report_rejects_invalid_overall_status(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(overall_status="bogus_status")
    with pytest.raises(GateIOError, match="overall_status"):
        write_gate_report(bad, output_root=output_root)


def test_write_gate_report_invariant_check_order_is_eligible_then_successor(
    tmp_path: Path,
) -> None:
    """research_eligible_after must be checked before no_successor_authorization."""
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(
        research_eligible_after=True,
        no_successor_authorization=False,
    )
    with pytest.raises(GateIOError, match="research_eligible_after"):
        write_gate_report(bad, output_root=output_root)


def test_write_gate_report_invariant_check_order_is_successor_then_verdict(
    tmp_path: Path,
) -> None:
    """no_successor_authorization must be checked before gate_verdict."""
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(
        no_successor_authorization=False,
        gate_verdict="WRONG",
    )
    with pytest.raises(GateIOError, match="no_successor_authorization"):
        write_gate_report(bad, output_root=output_root)


def test_write_gate_report_invariant_check_order_is_verdict_then_overall_status(
    tmp_path: Path,
) -> None:
    """gate_verdict must be checked before overall_status."""
    output_root = _output_root(tmp_path)
    bad = _make_unsafe_report(gate_verdict="WRONG", overall_status="bogus")
    with pytest.raises(GateIOError, match="gate_verdict"):
        write_gate_report(bad, output_root=output_root)


# --------------------------------------------------------------------- #
# write_gate_report — verdict taxonomy acceptance
# --------------------------------------------------------------------- #


def test_write_gate_report_accepts_pass_verdict(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report(
        gate_verdict=GATE_VERDICT_PASS, overall_status="pass"
    )
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    parsed = json.loads(paths.report_path.read_text(encoding="utf-8"))
    assert parsed["gate_verdict"] == GATE_VERDICT_PASS


def test_write_gate_report_accepts_fail_verdict(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report(
        gate_verdict=GATE_VERDICT_FAIL, overall_status="fail"
    )
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    parsed = json.loads(paths.report_path.read_text(encoding="utf-8"))
    assert parsed["gate_verdict"] == GATE_VERDICT_FAIL
    assert parsed["overall_status"] == "fail"


def test_write_gate_report_accepts_incomplete_verdict(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report(
        gate_verdict=GATE_VERDICT_INCOMPLETE, overall_status="incomplete"
    )
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    parsed = json.loads(paths.report_path.read_text(encoding="utf-8"))
    assert parsed["gate_verdict"] == GATE_VERDICT_INCOMPLETE
    assert parsed["overall_status"] == "incomplete"


# --------------------------------------------------------------------- #
# write_gate_report — refuse-overwrite
# --------------------------------------------------------------------- #


def test_write_gate_report_refuses_overwrite_on_second_call(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    write_gate_report(report, output_root=output_root)
    with pytest.raises(GateIOError):
        write_gate_report(report, output_root=output_root)


def test_write_gate_report_refuse_overwrite_false_allows_replace(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    write_gate_report(report, output_root=output_root, refuse_overwrite=False)
    # Same report id → same path → must not raise when overwrite is permitted.
    paths, sha, _size = write_gate_report(
        report, output_root=output_root, refuse_overwrite=False
    )
    assert paths.report_path.exists()
    assert sha == compute_file_sha256(paths.report_path)
