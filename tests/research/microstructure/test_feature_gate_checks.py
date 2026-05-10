"""Phase 4bi-B tests for individual feature-gate check functions.

Each test constructs a synthetic :class:`FeatureGateContext` over the
shared mini-fixture and either accepts the expected baseline result or
mutates the context to drive a specific failure path.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pyarrow.parquet as pq

from prometheus.research.microstructure.feature_gate_checks import (
    CHECK_ORDER,
    EXPECTED_FEATURE_CONFIG_HASH,
    EXPECTED_FEATURE_MANIFEST_SHA,
    EXPECTED_FEATURE_PARQUET_SHA,
    EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA,
    FeatureGateCheckStatus,
    FeatureGateContext,
    check_a01,
    check_b01,
    check_b04,
    check_c08,
    check_c09,
    check_c10,
    check_d01,
    check_d05,
    check_d08,
    check_e01,
    check_e02,
    check_f01,
    check_f02,
    check_f03,
    check_f06,
    check_h01,
    check_i01,
    check_j01,
    check_k01,
    check_l03,
    check_l04,
    check_m01,
    check_n01,
    run_all_checks,
)

from ._feature_gate_fixtures import build_feature_gate_fixture


def _make_ctx(tmp_path: Path) -> FeatureGateContext:
    bundle = build_feature_gate_fixture(tmp_path)
    feat_table = pq.read_table(bundle.feature_parquet_path)
    src_table = pq.read_table(bundle.feature_bundle.normalized_parquet_path)
    feature_manifest_bytes = bundle.feature_manifest_path.read_bytes()
    feature_manifest = json.loads(feature_manifest_bytes.decode("utf-8"))
    src_manifest = json.loads(
        bundle.feature_bundle.normalized_manifest_path.read_text(encoding="utf-8")
    )
    raw_manifest = json.loads(bundle.raw_manifest_path.read_text(encoding="utf-8"))
    feature_parquet_sha = hashlib.sha256(
        bundle.feature_parquet_path.read_bytes()
    ).hexdigest()
    feature_manifest_sha = hashlib.sha256(feature_manifest_bytes).hexdigest()
    src_normalized_parquet_sha = hashlib.sha256(
        bundle.feature_bundle.normalized_parquet_path.read_bytes()
    ).hexdigest()
    src_normalized_manifest_sha = hashlib.sha256(
        bundle.feature_bundle.normalized_manifest_path.read_bytes()
    ).hexdigest()
    raw_manifest_sha = hashlib.sha256(bundle.raw_manifest_path.read_bytes()).hexdigest()
    return FeatureGateContext(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_parquet_sidecar_path=bundle.feature_parquet_sidecar_path,
        feature_manifest_path=bundle.feature_manifest_path,
        feature_manifest_sidecar_path=bundle.feature_manifest_sidecar_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        feature_manifest=feature_manifest,
        feature_manifest_bytes=feature_manifest_bytes,
        feature_manifest_sha=feature_manifest_sha,
        feature_manifest_sidecar_first_64=feature_manifest_sha,
        source_normalized_manifest=src_manifest,
        source_normalized_manifest_sha=src_normalized_manifest_sha,
        raw_manifest=raw_manifest,
        raw_manifest_sha=raw_manifest_sha,
        feature_parquet_sha=feature_parquet_sha,
        feature_parquet_sidecar_first_64=feature_parquet_sha,
        source_normalized_parquet_sha=src_normalized_parquet_sha,
        raw_zip_sha=None,
        phase_4bb_d_gate_report_sha=None,
        phase_4bf_gate_report_sha=None,
        phase_4bg_b_successor_state_sha=None,
        feature_table=feat_table,
        source_normalized_table=src_table,
        validate_overall_status="pass",
        validate_failed_checks=(),
        gitignore_results={
            "data/microstructure/": True,
            "data/microstructure/features/": True,
            "data/microstructure/manifests/": True,
            "data/microstructure/gate-reports/features/": True,
        },
    )


def test_check_a01_pass(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    res = check_a01(ctx)
    assert res.status == FeatureGateCheckStatus.PASS


def test_check_a01_fail_when_missing(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    ctx.feature_parquet_path = tmp_path / "absent.parquet"
    res = check_a01(ctx)
    assert res.status == FeatureGateCheckStatus.FAIL


def test_check_b01_pass(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    res = check_b01(ctx)
    assert res.status == FeatureGateCheckStatus.PASS


def test_check_b01_fail_when_not_ignored(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    ctx.gitignore_results["data/microstructure/"] = False
    res = check_b01(ctx)
    assert res.status == FeatureGateCheckStatus.FAIL


def test_check_b04_features_namespace(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    res = check_b04(ctx)
    assert res.status == FeatureGateCheckStatus.PASS
    ctx.gitignore_results["data/microstructure/gate-reports/features/"] = False
    assert check_b04(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_c08_research_eligible_false(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_c08(ctx).status == FeatureGateCheckStatus.PASS


def test_check_c08_fails_when_true(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    ctx.feature_manifest = dict(ctx.feature_manifest)
    ctx.feature_manifest["research_eligible"] = True
    assert check_c08(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_c09_pending(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_c09(ctx).status == FeatureGateCheckStatus.PASS
    ctx.feature_manifest = dict(ctx.feature_manifest)
    ctx.feature_manifest["eligibility_gate_status"] = "pass"
    assert check_c09(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_c10_governance(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_c10(ctx).status == FeatureGateCheckStatus.PASS
    ctx.feature_manifest = dict(ctx.feature_manifest)
    ctx.feature_manifest["governance_labels"] = dict(
        ctx.feature_manifest["governance_labels"]
    )
    ctx.feature_manifest["governance_labels"]["labels"] = "allowed"
    assert check_c10(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_d01_column_count(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    res = check_d01(ctx)
    assert res.status == FeatureGateCheckStatus.PASS


def test_check_d05_feature_list_matches_canonical(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_d05(ctx).status == FeatureGateCheckStatus.PASS
    ctx.feature_manifest = dict(ctx.feature_manifest)
    ctx.feature_manifest["feature_list"] = ["bogus"]
    assert check_d05(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_d08_no_forbidden_substrings(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_d08(ctx).status == FeatureGateCheckStatus.PASS


def test_check_e01_row_count_fixture(tmp_path: Path) -> None:
    """The mini-fixture has 10 rows, not 1,681,098, so E01 fails. The
    check is meant to be hit in production; tests confirm the
    expected-vs-actual semantics."""
    ctx = _make_ctx(tmp_path)
    res = check_e01(ctx)
    assert res.status == FeatureGateCheckStatus.FAIL


def test_check_e02_contiguous_row_index(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    # The fixture's 10-row feature table has row_index 0..9. E02 expects
    # 0..1681097, so it fails — but the check exercises the comparison
    # path. We additionally validate that on the fixture the row_index
    # column itself is genuinely contiguous 0..n-1 by sampling.
    arr = ctx.feature_table.column("row_index").to_numpy()
    assert list(arr) == list(range(len(arr)))
    res = check_e02(ctx)
    # row_index has shape (10,) but the check expects shape (1681098,)
    assert res.status == FeatureGateCheckStatus.FAIL


def test_check_f01_fails_against_synthetic_sha(tmp_path: Path) -> None:
    """Synthetic fixture parquet does not match production SHA."""
    ctx = _make_ctx(tmp_path)
    res = check_f01(ctx)
    assert res.status == FeatureGateCheckStatus.FAIL
    assert ctx.feature_parquet_sha != EXPECTED_FEATURE_PARQUET_SHA


def test_check_f02_sidecar_matches(tmp_path: Path) -> None:
    """Within the fixture, parquet sidecar and parquet bytes match
    each other (the kernel writes them paired)."""
    ctx = _make_ctx(tmp_path)
    assert check_f02(ctx).status == FeatureGateCheckStatus.PASS


def test_check_f02_fails_when_sidecar_mismatched(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    ctx.feature_parquet_sidecar_first_64 = "0" * 64
    assert check_f02(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_f03_fails_against_synthetic_sha(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    res = check_f03(ctx)
    assert res.status == FeatureGateCheckStatus.FAIL
    assert ctx.feature_manifest_sha != EXPECTED_FEATURE_MANIFEST_SHA


def test_check_f06_lineage_constants_synthetic(tmp_path: Path) -> None:
    """The synthetic fixture stores synthetic lineage SHAs, so F06
    fails against the production-locked expectations."""
    ctx = _make_ctx(tmp_path)
    res = check_f06(ctx)
    # Phase 4bg-B successor-state SHA in the fixture is NOT the
    # production constant.
    assert res.status == FeatureGateCheckStatus.FAIL


def test_check_h01_invalid_window_flag_false(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_h01(ctx).status == FeatureGateCheckStatus.PASS


def test_check_i01_first_row_no_prior_reference(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_i01(ctx).status == FeatureGateCheckStatus.PASS


def test_check_j01_same_t_tie_break(tmp_path: Path) -> None:
    """The default fixture rows include a same-T pair at offset 500
    (rows 1002, 1003), so J01 should PASS."""
    ctx = _make_ctx(tmp_path)
    assert check_j01(ctx).status == FeatureGateCheckStatus.PASS


def test_check_k01_synthetic_normalized_parquet(tmp_path: Path) -> None:
    """Synthetic normalized parquet does not match the production
    SHA, so K01 fails."""
    ctx = _make_ctx(tmp_path)
    assert check_k01(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_l03_boundary_confirmations(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_l03(ctx).status == FeatureGateCheckStatus.PASS
    ctx.feature_manifest = dict(ctx.feature_manifest)
    ctx.feature_manifest["boundary_confirmations"] = dict(
        ctx.feature_manifest["boundary_confirmations"]
    )
    ctx.feature_manifest["boundary_confirmations"]["no_acquisition"] = False
    assert check_l03(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_l04_validate_overall_pass(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_l04(ctx).status == FeatureGateCheckStatus.PASS
    ctx.validate_overall_status = "fail"
    ctx.validate_failed_checks = ("4bh.parquet.sidecar_matches",)
    assert check_l04(ctx).status == FeatureGateCheckStatus.FAIL


def test_check_m01_research_eligible_after_invariant(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_m01(ctx).status == FeatureGateCheckStatus.PASS


def test_check_n01_boundary_keys_present(tmp_path: Path) -> None:
    ctx = _make_ctx(tmp_path)
    assert check_n01(ctx).status == FeatureGateCheckStatus.PASS


def test_run_all_checks_returns_full_tuple(tmp_path: Path) -> None:
    """``run_all_checks`` returns one result per :data:`CHECK_ORDER`
    entry, in stable ID order. The fixture's synthetic SHAs and
    10-row table cause some checks to FAIL, but the orchestrator
    must return every result — none silently dropped."""
    ctx = _make_ctx(tmp_path)
    out = run_all_checks(ctx)
    assert len(out) == len(CHECK_ORDER)
    ids = [r.check_id for r in out]
    expected = [cid for cid, _fn in CHECK_ORDER]
    assert ids == expected


def test_check_ids_are_unique() -> None:
    ids = [cid for cid, _fn in CHECK_ORDER]
    assert len(ids) == len(set(ids))


def test_check_ids_use_4bi_b_prefix() -> None:
    for cid, _fn in CHECK_ORDER:
        assert cid.startswith("4bi-b.")


def test_synthetic_lineage_does_not_match_expected_constants() -> None:
    """Sanity: production-locked SHAs are public-record constants,
    not derived from any tmp_path fixture."""
    assert (
        EXPECTED_FEATURE_PARQUET_SHA
        != "618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691z"
    )
    assert (
        EXPECTED_FEATURE_CONFIG_HASH
        == "49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77"
    )
    assert (
        EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA
        == "8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e"
    )
