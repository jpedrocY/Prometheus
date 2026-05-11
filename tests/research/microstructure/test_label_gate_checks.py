"""Phase 4bj-E label-gate check-suite tests.

These tests exercise individual check functions against the synthetic
mini-fixture. The fixture deliberately uses synthetic lineage SHAs so
that production-locked equality checks (Group F SHA-equality, Group G
expected-count checks, Group H per-horizon-count parity vs production
constants) FAIL on the fixture by design. The tests confirm that:

- each PASS check returns ``PASS`` on a well-formed fixture;
- each FAIL check is correctly classified;
- ``run_all_checks`` returns exactly ``len(CHECK_ORDER)`` results.
"""
from __future__ import annotations

from pathlib import Path

import pyarrow.parquet as pq

from prometheus.research.microstructure.label_gate_checks import (
    CHECK_ORDER,
    LabelGateCheckStatus,
    LabelGateContext,
    check_a01,
    check_a02,
    check_a03,
    check_a04,
    check_b01,
    check_b02,
    check_b03,
    check_b04,
    check_c01,
    check_c02,
    check_c03,
    check_c04,
    check_c05,
    check_c07,
    check_c08,
    check_c09,
    check_c10,
    check_d01,
    check_d02,
    check_d03,
    check_d04,
    check_d05,
    check_d06,
    check_d07,
    check_d08,
    check_d09,
    check_d10,
    check_e03,
    check_e04,
    check_f02,
    check_f04,
    check_i01,
    check_i02,
    check_i05,
    check_i06,
    check_i07,
    check_i08,
    check_j01,
    check_j02,
    check_k01,
    check_l01,
    check_l03,
    check_l04,
    check_m01,
    check_m02,
    check_n01,
    check_o01,
    load_parquet_table,
    run_all_checks,
)
from prometheus.research.microstructure.label_gate_io import (
    compute_bytes_sha256,
    compute_file_sha256,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
)

from ._label_gate_fixtures import build_label_gate_fixture


def _ctx_from_fixture(tmp_path: Path) -> LabelGateContext:
    bundle = build_label_gate_fixture(tmp_path)
    label_parquet_bytes_sha = compute_file_sha256(bundle.label_parquet_path)
    label_manifest_bytes = read_manifest_bytes(bundle.label_manifest_path)
    label_manifest_sha = compute_bytes_sha256(label_manifest_bytes)
    manifest = parse_manifest_bytes(label_manifest_bytes)
    label_table = load_parquet_table(bundle.label_parquet_path)
    source_feature_table = pq.read_table(bundle.feature_parquet_path)
    gitignore_results = {
        "data/microstructure/": True,
        "data/microstructure/labels/": True,
        "data/microstructure/manifests/": True,
        "data/microstructure/gate-reports/labels/": True,
    }
    return LabelGateContext(
        label_parquet_path=bundle.label_parquet_path,
        label_parquet_sidecar_path=bundle.label_parquet_sidecar_path,
        label_manifest_path=bundle.label_manifest_path,
        label_manifest_sidecar_path=bundle.label_manifest_sidecar_path,
        source_feature_parquet_path=bundle.feature_parquet_path,
        source_feature_manifest_path=bundle.feature_manifest_path,
        label_manifest=manifest,
        label_manifest_bytes=label_manifest_bytes,
        label_manifest_sha=label_manifest_sha,
        label_manifest_sidecar_first_64=read_sidecar_first_64(
            bundle.label_manifest_sidecar_path
        ),
        label_table=label_table,
        source_feature_table=source_feature_table,
        label_parquet_sha=label_parquet_bytes_sha,
        label_parquet_sidecar_first_64=read_sidecar_first_64(
            bundle.label_parquet_sidecar_path
        ),
        source_feature_parquet_sha=None,
        source_feature_manifest_sha=None,
        gitignore_results=gitignore_results,
        measured={
            "label_parquet_sha_pre": label_parquet_bytes_sha,
            "label_parquet_sha_post": label_parquet_bytes_sha,
            "label_manifest_sha_pre": label_manifest_sha,
            "label_manifest_sha_post": label_manifest_sha,
        },
    )


# --------------------------------------------------------------------
# Group A — Artefact presence (PASS on fixture)
# --------------------------------------------------------------------


def test_a01_a02_a03_a04_pass_on_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (check_a01, check_a02, check_a03, check_a04):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


def test_a01_fails_if_label_parquet_missing(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.label_parquet_path.unlink()
    r = check_a01(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


# --------------------------------------------------------------------
# Group B — Gitignore boundary (PASS by fixture stub)
# --------------------------------------------------------------------


def test_b01_b02_b03_b04_pass_when_gitignore_stub_says_so(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (check_b01, check_b02, check_b03, check_b04):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


def test_b01_fails_when_gitignore_stub_says_not_ignored(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.gitignore_results["data/microstructure/"] = False
    r = check_b01(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


# --------------------------------------------------------------------
# Group C — Manifest governance (PASS on fixture for keys the fixture sets)
# --------------------------------------------------------------------


def test_c01_through_c05_match_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (check_c01, check_c02, check_c03, check_c04, check_c05):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


def test_c07_c08_c09_pass_when_manifest_is_default_state(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (check_c07, check_c08, check_c09):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


def test_c07_fails_when_research_eligible_flipped(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.label_manifest["research_eligible"] = True
    r = check_c07(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


def test_c08_fails_when_eligibility_gate_status_not_pending(
    tmp_path: Path,
) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.label_manifest["eligibility_gate_status"] = "pass"
    r = check_c08(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


def test_c09_fails_when_chronological_split_policy_changed(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.label_manifest["chronological_split_policy"] = "defined"
    r = check_c09(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


def test_c10_pass_with_fixture_governance(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_c10(ctx)
    assert r.status == LabelGateCheckStatus.PASS, r


def test_c10_fails_when_governance_label_loosened(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    gov = dict(ctx.label_manifest["governance_labels"])
    gov["ml"] = "allowed"
    ctx.label_manifest["governance_labels"] = gov
    r = check_c10(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


# --------------------------------------------------------------------
# Group D — Schema (PASS on fixture)
# --------------------------------------------------------------------


def test_group_d_pass_on_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (
        check_d01,
        check_d02,
        check_d03,
        check_d04,
        check_d05,
        check_d06,
        check_d07,
        check_d08,
        check_d09,
        check_d10,
    ):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


# --------------------------------------------------------------------
# Group E — row alignment subset
# --------------------------------------------------------------------


def test_e03_pass_on_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_e03(ctx)
    assert r.status == LabelGateCheckStatus.PASS


def test_e04_pass_on_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_e04(ctx)
    assert r.status == LabelGateCheckStatus.PASS


def test_e04_fail_when_manifest_files_empty(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.label_manifest["files"] = []
    r = check_e04(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


# --------------------------------------------------------------------
# Group F — SHA / sidecar (sidecar self-consistency PASS on fixture;
# absolute SHA-equality FAILS on fixture by design)
# --------------------------------------------------------------------


def test_f02_sidecar_self_consistency_pass(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_f02(ctx)
    assert r.status == LabelGateCheckStatus.PASS


def test_f04_manifest_sidecar_self_consistency_pass(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_f04(ctx)
    assert r.status == LabelGateCheckStatus.PASS


# --------------------------------------------------------------------
# Group I — dtype (PASS on fixture)
# --------------------------------------------------------------------


def test_group_i_dtype_checks_pass_on_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (check_i01, check_i02, check_i05, check_i06, check_i07, check_i08):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


# --------------------------------------------------------------------
# Group J — pre/post immutability
# --------------------------------------------------------------------


def test_j01_j02_pass_when_measured_pre_post_match(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (check_j01, check_j02):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


def test_j01_fail_when_pre_post_differ(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.measured["label_parquet_sha_post"] = "0" * 64
    r = check_j01(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


def test_j02_error_when_pre_post_missing(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.measured.pop("label_manifest_sha_pre")
    r = check_j02(ctx)
    assert r.status == LabelGateCheckStatus.ERROR


# --------------------------------------------------------------------
# Group K — one-row-per-feature-row (with optional feature parquet)
# --------------------------------------------------------------------


def test_k01_pass_when_feature_table_present(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_k01(ctx)
    assert r.status == LabelGateCheckStatus.PASS


def test_k01_not_applicable_when_feature_table_absent(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    ctx.source_feature_table = None
    r = check_k01(ctx)
    assert r.status == LabelGateCheckStatus.NOT_APPLICABLE


# --------------------------------------------------------------------
# Group L — consistency / nested censoring
# --------------------------------------------------------------------


def test_l01_label_any_censored_matches_or_of_per_horizon(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_l01(ctx)
    assert r.status == LabelGateCheckStatus.PASS


def test_l03_nested_censoring_pass(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_l03(ctx)
    assert r.status == LabelGateCheckStatus.PASS


def test_l04_pass_on_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    r = check_l04(ctx)
    assert r.status == LabelGateCheckStatus.PASS


def test_l04_fails_when_a_required_boundary_missing(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    bc = dict(ctx.label_manifest["boundary_confirmations"])
    bc.pop("no_ml")
    ctx.label_manifest["boundary_confirmations"] = bc
    r = check_l04(ctx)
    assert r.status == LabelGateCheckStatus.FAIL


# --------------------------------------------------------------------
# Group M / N / O — stage interpretation
# --------------------------------------------------------------------


def test_m01_m02_n01_o01_pass_on_fixture(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    for fn in (check_m01, check_m02, check_n01, check_o01):
        r = fn(ctx)
        assert r.status == LabelGateCheckStatus.PASS, r


# --------------------------------------------------------------------
# Orchestrator-level check count
# --------------------------------------------------------------------


def test_run_all_checks_emits_exactly_check_order_count(tmp_path: Path) -> None:
    ctx = _ctx_from_fixture(tmp_path)
    results = run_all_checks(ctx)
    assert len(results) == len(CHECK_ORDER)
    # Status values must be members of the StrEnum.
    for r in results:
        assert isinstance(r.status, LabelGateCheckStatus)


def test_check_order_ids_are_unique() -> None:
    ids = [cid for (cid, _fn) in CHECK_ORDER]
    assert len(ids) == len(set(ids))
