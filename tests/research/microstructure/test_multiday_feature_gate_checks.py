"""Phase 4bm-J check suite + check-ordering unit tests."""
# ruff: noqa: E501  (Phase 4bm-J: long v002 SHA literals + lineage column names)
from __future__ import annotations

from pathlib import Path

from prometheus.research.microstructure.multiday_feature_gate_checks import (
    CHECK_ORDER,
    EXPECTED_DATE_COUNT,
    EXPECTED_FEATURE_CONFIG_HASH,
    EXPECTED_FEATURE_MANIFEST_SHA,
    EXPECTED_TOTAL_FEATURE_ROW_COUNT,
    SAMPLE_DATES,
    MultidayFeatureGateCheckStatus,
    check_b7_per_day_outputs_length,
    check_b8_per_day_dates_unique,
    check_c5_safe_lineage_column_present,
    check_c6_unsafe_decision_column_absent,
    check_c7_no_forbidden_substrings,
    check_d1_total_row_count,
    check_d2_sum_per_day_equals_total,
    check_g1_manifest_research_eligible_false,
    check_g2_manifest_eligibility_gate_status_pending,
    check_g3_manifest_stage_4_feature_cleared_false,
    run_all_checks,
)

from ._multiday_feature_gate_fixtures import build_multiday_feature_gate_fixture


def test_check_order_50_checks_in_canonical_order() -> None:
    # Stable canonical ordering: A1..A12, B1..B10, C1..C10, D1..D6, E1..E3, F1..F3, G1..G6
    assert CHECK_ORDER[0] == "A1"
    assert CHECK_ORDER[-1] == "G6"
    assert len(CHECK_ORDER) == 50
    # Group counts.
    groups = {c[0] for c in CHECK_ORDER}
    assert groups == {"A", "B", "C", "D", "E", "F", "G"}


def test_sample_dates_six_dates() -> None:
    assert SAMPLE_DATES == (
        "2024-12-01", "2024-12-31", "2025-01-15",
        "2025-01-31", "2025-02-15", "2025-02-28",
    )


def test_expected_locked_constants_v002() -> None:
    assert EXPECTED_FEATURE_MANIFEST_SHA == "512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"
    assert EXPECTED_FEATURE_CONFIG_HASH == "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
    assert EXPECTED_TOTAL_FEATURE_ROW_COUNT == 155_153_449
    assert EXPECTED_DATE_COUNT == 90


# ===== Manifest-content unit checks (work on dict input) =====

def test_c7_no_forbidden_substrings_pass() -> None:
    res = check_c7_no_forbidden_substrings({"feature_column_names": ["dataset_family", "utc_hour"]})
    assert res.status == MultidayFeatureGateCheckStatus.PASS


def test_c7_no_forbidden_substrings_fail_label() -> None:
    res = check_c7_no_forbidden_substrings({"feature_column_names": ["my_label_column"]})
    assert res.status == MultidayFeatureGateCheckStatus.FAIL


def test_c7_no_forbidden_substrings_fail_decision() -> None:
    res = check_c7_no_forbidden_substrings({"feature_column_names": ["source_phase_4bm_e_decision"]})
    assert res.status == MultidayFeatureGateCheckStatus.FAIL


def test_c5_safe_outcome_column_present() -> None:
    pass_res = check_c5_safe_lineage_column_present({"feature_column_names": ["source_phase_4bm_e_outcome"]})
    assert pass_res.status == MultidayFeatureGateCheckStatus.PASS
    fail_res = check_c5_safe_lineage_column_present({"feature_column_names": ["x"]})
    assert fail_res.status == MultidayFeatureGateCheckStatus.FAIL


def test_c6_unsafe_decision_column_absent() -> None:
    pass_res = check_c6_unsafe_decision_column_absent({"feature_column_names": ["x"]})
    assert pass_res.status == MultidayFeatureGateCheckStatus.PASS
    fail_res = check_c6_unsafe_decision_column_absent(
        {"feature_column_names": ["source_phase_4bm_e_decision"]}
    )
    assert fail_res.status == MultidayFeatureGateCheckStatus.FAIL


def test_g1_g2_g3_pass_when_manifest_clean() -> None:
    m = {
        "research_eligible": False, "eligibility_gate_status": "pending",
        "stage_4_feature_cleared": False,
    }
    assert check_g1_manifest_research_eligible_false(m).status == MultidayFeatureGateCheckStatus.PASS
    assert check_g2_manifest_eligibility_gate_status_pending(m).status == MultidayFeatureGateCheckStatus.PASS
    assert check_g3_manifest_stage_4_feature_cleared_false(m).status == MultidayFeatureGateCheckStatus.PASS


def test_g1_fail_when_research_eligible_true() -> None:
    res = check_g1_manifest_research_eligible_false({"research_eligible": True})
    assert res.status == MultidayFeatureGateCheckStatus.FAIL


def test_d1_total_row_count_mismatch_fail() -> None:
    res = check_d1_total_row_count({"actual_feature_row_count": 12345})
    assert res.status == MultidayFeatureGateCheckStatus.FAIL


def test_d2_sum_per_day_equals_total() -> None:
    m = {"per_day_outputs": [{"row_count": 1}, {"row_count": 2}]}
    res = check_d2_sum_per_day_equals_total(m)
    # Sum != EXPECTED_TOTAL_FEATURE_ROW_COUNT, so FAIL.
    assert res.status == MultidayFeatureGateCheckStatus.FAIL


def test_b7_per_day_outputs_length() -> None:
    assert check_b7_per_day_outputs_length({"per_day_outputs": [{}] * 90}).status == MultidayFeatureGateCheckStatus.PASS
    assert check_b7_per_day_outputs_length({"per_day_outputs": [{}] * 89}).status == MultidayFeatureGateCheckStatus.FAIL


def test_b8_per_day_dates_unique() -> None:
    dates = [{"utc_date": f"2024-12-{i + 1:02d}"} for i in range(90)]
    assert check_b8_per_day_dates_unique({"per_day_outputs": dates[:90]}).status == MultidayFeatureGateCheckStatus.PASS


# ===== Full-suite end-to-end against synthetic fixture =====

def test_run_all_checks_synthetic_returns_50_results_in_canonical_order(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    from prometheus.research.microstructure.multiday_feature_gate_checks import (
        MultidayFeatureGateContext,
    )

    ctx = MultidayFeatureGateContext(
        repo_root=bundle.repo_root,
        feature_manifest_path=bundle.feature_manifest_path,
        feature_manifest_sidecar_path=bundle.feature_manifest_sidecar_path,
        features_root=bundle.features_root,
        derived_manifest_path=bundle.derived_manifest_path,
        raw_manifest_path=bundle.raw_manifest_path,
        acquisition_log_path=bundle.acquisition_log_path,
        phase_4bl_d_r_gate_report_path=bundle.phase_4bl_d_r_gate_report_path,
        phase_4bl_e_successor_state_path=bundle.phase_4bl_e_successor_state_path,
        phase_4bm_d_gate_report_path=bundle.phase_4bm_d_gate_report_path,
        phase_4bm_d_sidecar_path=bundle.phase_4bm_d_sidecar_path,
        phase_4bm_f_successor_state_path=bundle.phase_4bm_f_successor_state_path,
        phase_4bm_f_successor_state_sidecar_path=bundle.phase_4bm_f_successor_state_sidecar_path,
    )
    results, manifest = run_all_checks(ctx)
    assert len(results) == 50
    assert tuple(r.check_id for r in results) == CHECK_ORDER
    # B/C/D/E/F/G groups should pass on the synthetic fixture (lineage SHAs in
    # A-group will FAIL because the fixture's lineage stubs don't reproduce the
    # production-locked SHAs by construction). That's expected fixture limit.
    a_group = [r for r in results if r.group == "A"]
    b_group = [r for r in results if r.group == "B"]
    g_group = [r for r in results if r.group == "G"]
    # Some A-group checks (those that compare lineage stubs against locked
    # production SHAs) will FAIL on the synthetic fixture, but the suite must
    # still return 50 results in canonical order.
    assert len(a_group) == 12
    assert len(b_group) == 10
    assert len(g_group) == 6
    # All G-group checks should PASS on the clean synthetic fixture.
    for r in g_group:
        assert r.status == MultidayFeatureGateCheckStatus.PASS, (r.check_id, r.observed)
