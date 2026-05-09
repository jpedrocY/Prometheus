"""Phase 4bb-C per-check tests for the offline aggTrades eligibility gate.

All tests are offline and use ``pytest tmp_path`` only.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from _eligibility_fixtures import (  # noqa: E402
    FixtureRow,
    build_happy_fixture,
    make_default_rows,
    sha256_of_file,
    write_sidecar,
)

from prometheus.research.microstructure import (  # noqa: E402
    AggTradesEligibilityCheckStatus,
    AggTradesEligibilityGateInput,
    run_eligibility_gate,
)


def _git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()


def _run(fb_input_kwargs: dict, fb) -> dict:
    sha = _git_head()
    inp = AggTradesEligibilityGateInput(
        manifest_path=fb.manifest_path,
        output_root=fb.output_root,
        code_commit_sha=sha,
        write_report=False,
        **fb_input_kwargs,
    )
    res = run_eligibility_gate(inp)
    return {c.check_id: c for c in res.checks}, res  # type: ignore[return-value]


def _ids_of(status: AggTradesEligibilityCheckStatus, results) -> list[str]:
    return [c.check_id for c in results.checks if c.status is status]


def test_happy_path_yields_no_fail_no_error(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    assert _ids_of(AggTradesEligibilityCheckStatus.FAIL, res) == []
    assert _ids_of(AggTradesEligibilityCheckStatus.ERROR, res) == []


def test_sha_mismatch_fails_at_10_2_7(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    # Perturb the manifest's recorded SHA.
    data = json.loads(fb.manifest_path.read_text(encoding="utf-8"))
    data["files"][0]["sha256"] = "0" * 64
    fb.manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    sha_check = next(c for c in res.checks if c.check_id == "10.2.7")
    assert sha_check.status is AggTradesEligibilityCheckStatus.FAIL


def test_missing_sidecar_causes_sha_check_fail(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    fb.sidecar_path.unlink()
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    sha_check = next(c for c in res.checks if c.check_id == "10.2.7")
    assert sha_check.status is AggTradesEligibilityCheckStatus.FAIL
    companion = next(c for c in res.checks if c.check_id == "10.2.8")
    assert companion.status is AggTradesEligibilityCheckStatus.FAIL


def test_missing_acquisition_log_fails_at_10_12_45(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    fb.acquisition_log_path.unlink()
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    log_check = next(c for c in res.checks if c.check_id == "10.12.45")
    assert log_check.status is AggTradesEligibilityCheckStatus.FAIL


def test_multiple_zip_csv_members_fail_at_10_10_33(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(
        tmp_path, code_commit_sha=sha, multiple_zip_members=True
    )
    # Re-stamp the manifest sha because the zip changed.
    new_sha = sha256_of_file(fb.raw_zip_path)
    data = json.loads(fb.manifest_path.read_text(encoding="utf-8"))
    data["files"][0]["sha256"] = new_sha
    fb.manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    write_sidecar(fb.sidecar_path, new_sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    members_check = next(c for c in res.checks if c.check_id == "10.10.33")
    assert members_check.status is AggTradesEligibilityCheckStatus.FAIL


def test_malformed_row_fails_at_10_4_14(tmp_path: Path) -> None:
    sha = _git_head()
    rows = make_default_rows(n=8)
    # Replace one row's price with a non-positive value.
    bad = rows[3]
    rows[3] = FixtureRow(
        a=bad.a, p="0", q=bad.q, f=bad.f, l=bad.l, T=bad.T, m=bad.m
    )
    fb = build_happy_fixture(tmp_path, rows=rows, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    schema_check = next(c for c in res.checks if c.check_id == "10.4.14")
    assert schema_check.status is AggTradesEligibilityCheckStatus.FAIL


def test_duplicate_aggregate_trade_id_fails_at_10_7_24(tmp_path: Path) -> None:
    sha = _git_head()
    rows = make_default_rows(n=8)
    rows[5] = FixtureRow(
        a=rows[4].a, p=rows[5].p, q=rows[5].q, f=rows[5].f, l=rows[5].l, T=rows[5].T, m=rows[5].m
    )
    fb = build_happy_fixture(tmp_path, rows=rows, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    dup = next(c for c in res.checks if c.check_id == "10.7.24")
    assert dup.status is AggTradesEligibilityCheckStatus.FAIL


def test_out_of_order_a_fails_at_10_6_21(tmp_path: Path) -> None:
    sha = _git_head()
    rows = make_default_rows(n=8)
    swapped = list(rows)
    swapped[3], swapped[4] = swapped[4], swapped[3]
    fb = build_happy_fixture(tmp_path, rows=swapped, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    mono = next(c for c in res.checks if c.check_id == "10.6.21")
    assert mono.status is AggTradesEligibilityCheckStatus.FAIL


def test_out_of_day_T_fails_at_10_5_20(tmp_path: Path) -> None:
    sha = _git_head()
    rows = make_default_rows(n=8)
    # Move last row past the UTC day boundary.
    rows[-1] = FixtureRow(
        a=rows[-1].a, p=rows[-1].p, q=rows[-1].q, f=rows[-1].f, l=rows[-1].l,
        T=1736985600000 + 1000, m=rows[-1].m,
    )
    fb = build_happy_fixture(tmp_path, rows=rows, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    utc_check = next(c for c in res.checks if c.check_id == "10.5.20")
    assert utc_check.status is AggTradesEligibilityCheckStatus.FAIL


def test_manifest_sidecar_sha_disagreement_fails_at_10_2_7(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    # Replace the sidecar with an incorrect digest while leaving the manifest alone.
    fb.sidecar_path.write_text("0" * 64 + "  ignored\n", encoding="utf-8")
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    sha_check = next(c for c in res.checks if c.check_id == "10.2.7")
    assert sha_check.status is AggTradesEligibilityCheckStatus.FAIL


def test_manifest_row_count_mismatch_fails_at_10_8_27(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    data = json.loads(fb.manifest_path.read_text(encoding="utf-8"))
    data["event_count"] = 9999  # Wrong on purpose.
    data["files"][0]["event_count"] = 9999
    fb.manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    rc = next(c for c in res.checks if c.check_id == "10.8.27")
    assert rc.status is AggTradesEligibilityCheckStatus.FAIL


def test_missing_governance_label_fails_at_10_3_11(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    data = json.loads(fb.manifest_path.read_text(encoding="utf-8"))
    data["governance_labels"].pop("validator")
    fb.manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    gov = next(c for c in res.checks if c.check_id == "10.3.11")
    assert gov.status is AggTradesEligibilityCheckStatus.FAIL


def test_feature_computation_not_forbidden_fails_at_10_12_41(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(
        tmp_path,
        code_commit_sha=sha,
        governance_overrides={"feature_computation": "allowed"},
    )
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.12.41")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL


def test_strategy_use_not_forbidden_fails_at_10_12_42(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(
        tmp_path,
        code_commit_sha=sha,
        governance_overrides={"strategy_use": "allowed"},
    )
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.12.42")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL


def test_raw_family_research_eligible_true_fails_at_10_3_10(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha, research_eligible=True)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.3.10")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL
    # The result-level invariant still holds: raw families never get
    # research_eligible_after = True.
    assert res.research_eligible_after is False


def test_eligibility_status_inconsistent_with_research_eligible_fails(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(
        tmp_path,
        code_commit_sha=sha,
        research_eligible=True,
        eligibility_gate_status="pass",
    )
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.3.10")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL


def test_invalid_window_evidence_missing_fails_at_10_11_38(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(
        tmp_path,
        code_commit_sha=sha,
        invalid_windows=[
            {
                "start_time_ms": 1736899200000,
                "end_time_ms": 1736899300000,
                "family": "microstructure_raw_aggtrades_v001",
                "symbol": "BTCUSDT",
                "reason": "out_of_order_event",
                "severity": "error",
                "downstream_eligibility_action": "exclude",
                "evidence": {},  # empty -> Phase 4aw InvalidWindow rejects construction.
            }
        ],
    )
    # Phase 4aw enforces non-empty evidence on InvalidWindow construction;
    # MicrostructureManifest.from_dict will raise on load. The gate should
    # surface this as an ERROR/FAIL through the manifest read path.
    from prometheus.research.microstructure import GateIOError

    with pytest.raises((GateIOError, ValueError)):
        run_eligibility_gate(
            AggTradesEligibilityGateInput(
                manifest_path=fb.manifest_path,
                output_root=fb.output_root,
                code_commit_sha=sha,
                write_report=False,
            )
        )


def test_no_silent_omission_fails_at_10_11_40(tmp_path: Path) -> None:
    """Per-row anomaly without manifest invalid_windows entry triggers FAIL."""
    sha = _git_head()
    rows = make_default_rows(n=8)
    rows[5] = FixtureRow(
        a=rows[4].a, p=rows[5].p, q=rows[5].q, f=rows[5].f, l=rows[5].l, T=rows[5].T, m=rows[5].m
    )
    fb = build_happy_fixture(tmp_path, rows=rows, code_commit_sha=sha)
    # No invalid_windows recorded -> 10.11.40 should FAIL.
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.11.40")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL


def test_unexpected_extra_columns_fails_at_10_4_16(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha, extra_column=True)
    new_sha = sha256_of_file(fb.raw_zip_path)
    data = json.loads(fb.manifest_path.read_text(encoding="utf-8"))
    data["files"][0]["sha256"] = new_sha
    fb.manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    write_sidecar(fb.sidecar_path, new_sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.4.16")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL


def test_unknown_code_commit_sha_yields_fail_at_10_3_12(tmp_path: Path) -> None:
    fb = build_happy_fixture(tmp_path, code_commit_sha="0" * 40)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha="0" * 40,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.3.12")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL


def test_capture_mode_wrong_fails_at_10_1_5(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    data = json.loads(fb.manifest_path.read_text(encoding="utf-8"))
    data["capture_mode"] = "live_capture"
    fb.manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    chk = next(c for c in res.checks if c.check_id == "10.1.5")
    assert chk.status is AggTradesEligibilityCheckStatus.FAIL
