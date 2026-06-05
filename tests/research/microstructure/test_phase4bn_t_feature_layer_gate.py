"""Offline tests for the Phase 4bn-T feature-layer eligibility gate.

Loads ``scripts/phase4bn_t_validate_feature_pre_v002_gate.py`` by file path and
exercises the gate's sidecar/date/manifest validators, per-file + bounded
row-level checks, predecessor integrity, fail-closed paths, and gate-report
posture — using only temp directories and small synthetic feature Parquet
fixtures with the locked 62-column FEATURE_SCHEMA_V002. No network, no real
production data, no sealed-test data.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

_REPO_ROOT: Path = Path(__file__).resolve().parents[3]
_SCRIPT_PATH: Path = (
    _REPO_ROOT / "scripts" / "phase4bn_t_validate_feature_pre_v002_gate.py"
)


def _load() -> object:
    name = "phase4bn_t_validate_feature_pre_v002_gate_under_test"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, _SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gate() -> object:
    return _load()


def _gr_root(base: Path) -> Path:
    return base / "data" / "microstructure" / "gate-reports" / "features"


@pytest.fixture
def short_tmp() -> Iterator[Path]:
    base = Path(tempfile.mkdtemp(prefix="p4bnt_"))
    try:
        yield base
    finally:
        shutil.rmtree(base, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Synthetic fixtures
# --------------------------------------------------------------------------- #


def _write_feature_parquet(
    gate: object, *, date: str, repo_root: Path, n: int, base_a: int,
    forbidden_col: bool = False, wrong_schema: bool = False,
) -> dict:
    """Write a synthetic 62-column feature parquet + sidecar; return inventory entry."""
    day_start = int(datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000)
    a = [base_a + i for i in range(n)]
    t = [day_start + 1000 + i * 100 for i in range(n)]
    lineage_values = {
        "dataset_family": gate.FEATURE_DATASET_FAMILY,
        "dataset_version": "v002",
        "source_dataset_family": "microstructure_normalized_aggtrades_v001",
        "source_dataset_version": "v002",
        "feature_schema_version": "v001",
        "symbol": "BTCUSDT",
        "utc_date": date,
        "agg_trade_id": None,  # filled below
        "row_index": None,
        "feature_timestamp_ms": None,
        "source_transact_time_ms": None,
        "source_normalized_parquet_per_day_sha256": "a" * 64,
        "source_normalized_manifest_sha256": "b" * 64,
        "source_successor_state_sha256": "non_eligible_pre_v002_segment_no_successor_state",
        "source_phase_4bm_d_gate_report_sha256": "c" * 64,
        "source_phase_4bm_e_outcome": "Option B / Decision form 2",
        "feature_config_hash": "d" * 64,
    }
    cols: dict[str, list] = {}
    for name in gate.FEATURE_SCHEMA_V002:
        if name == "agg_trade_id":
            cols[name] = a
        elif name == "row_index":
            cols[name] = list(range(n))
        elif name in ("feature_timestamp_ms", "source_transact_time_ms"):
            cols[name] = list(t)
        elif name in lineage_values:
            cols[name] = [lineage_values[name]] * n
        else:
            # one of the 45 feature / quality columns: simple float fill
            cols[name] = [float(i) for i in range(n)]
    if wrong_schema:
        cols.pop("feature_config_hash")
    if forbidden_col:
        cols["alpha_signal"] = [0.0] * n
    table = pa.table(cols)
    yyyy, mm, _dd = date.split("-")
    fam = gate.FAMILY_DIR_NAME
    pq_path = (
        repo_root / "data" / "microstructure" / "features" / fam / "BTCUSDT"
        / yyyy / mm / f"BTCUSDT-features-aggtrades-{date}.parquet"
    )
    pq_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, pq_path, compression="zstd")
    sha = hashlib.sha256(pq_path.read_bytes()).hexdigest()
    size = pq_path.stat().st_size
    sc_path = pq_path.with_suffix(pq_path.suffix + ".sha256")
    sc_path.write_bytes(f"{sha}  {pq_path.name}\n".encode("ascii"))
    rel = (
        f"microstructure/features/{fam}/BTCUSDT/{yyyy}/{mm}/"
        f"BTCUSDT-features-aggtrades-{date}.parquet"
    )
    norm_rel = (
        "microstructure/normalized/"
        "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/"
        f"BTCUSDT/{yyyy}/{mm}/BTCUSDT-aggTrades-{date}.parquet"
    )
    return {
        "date": date, "symbol": "BTCUSDT",
        "feature_parquet_path": rel,
        "feature_parquet_sha256": sha,
        "feature_parquet_size_bytes": size,
        "feature_sidecar_path": rel + ".sha256",
        "feature_sidecar_sha256": hashlib.sha256(sc_path.read_bytes()).hexdigest(),
        "feature_sidecar_size_bytes": sc_path.stat().st_size,
        "first_transact_time_ms": t[0], "last_transact_time_ms": t[-1],
        "min_agg_trade_id": min(a), "max_agg_trade_id": max(a),
        "paired_source_normalized_parquet_path": norm_rel,
        "paired_source_normalized_parquet_sha256": "e" * 64,
        "row_count": n, "status": "produced_verified",
    }


def _full_governance_manifest(gate: object, inv: list[dict], total_rows: int,
                              total_bytes: int, dates: list[str]) -> dict:
    """Build a complete feature segment manifest satisfying the contract."""
    boundary = {k: True for k in gate.REQUIRED_BOUNDARY_CONFIRMATION_KEYS}
    nonauth = {k: False for k in gate.REQUIRED_NON_AUTHORIZATION_FLAG_KEYS}
    return {
        "dataset_family": "microstructure_features_aggtrades_v001",
        "dataset_version": "v002", "version": "v002", "feature_schema_version": "v001",
        "segment_label": "pre_v002_segment", "data_family": "aggTrades",
        "symbol": "BTCUSDT", "symbol_list": ["BTCUSDT"], "market": "usdm_futures",
        "dataset_category": "features", "phase": "4bn-S", "phase_id": "phase-4bn-s",
        "source_phase_boundary": "4bn-P", "created_at_unix_ms": 1, "created_at_utc": "x",
        "code_commit_sha": gate.EXPECTED_BASE_COMMIT_SHA,
        "base_commit_sha": gate.EXPECTED_BASE_COMMIT_SHA,
        "feature_config_hash": gate.EXPECTED_FEATURE_CONFIG_HASH,
        "feature_schema_hash": gate.EXPECTED_FEATURE_SCHEMA_HASH,
        "feature_column_count": 62, "lineage_column_count": 17,
        "feature_quality_column_count": 45,
        "feature_column_names": list(gate.FEATURE_SCHEMA_V002),
        "lineage_column_names": list(gate.LINEAGE_COLUMNS_V002),
        "computed_feature_column_names": list(gate.FEATURE_NAMES_V002),
        "feature_dtypes": {c: "x" for c in gate.FEATURE_SCHEMA_V002},
        "feature_family_id": "microstructure_features_aggtrades_v001",
        "leakage_policy": "causal_only_no_future_lookahead",
        "cross_day_lookback_policy": "causal_cross_day_lookback",
        "cross_day_tail_buffer_ms": 60000,
        "feature_windows_ms": [1000, 5000, 15000, 60000],
        "feature_window_labels": ["1s", "5s", "15s", "60s"],
        "window_boundary_policy": "trailing_right_closed_left_open",
        "invalid_window_policy": {"x": True},
        "same_timestamp_tie_rule": "row_index_le_R",
        "timestamp_policy": "event_aligned_utc_ms_int64",
        "forbidden_substring_detector_tokens": [str(i) for i in range(26)],
        "date_start": dates[0], "date_end": dates[-1], "date_count": len(dates),
        "date_list": dates, "expected_file_count": len(dates),
        "produced_file_count": len(dates), "total_row_count": total_rows,
        "actual_feature_row_count": total_rows, "total_footprint_bytes": total_bytes,
        "per_file_inventory": inv,
        "source_dataset_family": "microstructure_normalized_aggtrades_v001",
        "source_dataset_version": "v002",
        "source_normalized_segment_manifest_path":
            "data/microstructure/manifests/norm_seg.json",
        "source_normalized_segment_manifest_sha256": "1" * 64,
        "source_normalized_segment_manifest_sidecar_sha256": "2" * 64,
        "source_normalized_layer_gate_report_path":
            "data/microstructure/gate-reports/normalized/norm_gate.json",
        "source_normalized_layer_gate_report_sha256": "3" * 64,
        "source_normalized_schema_version": "NORMALIZED_SCHEMA_V001",
        "source_eligibility_posture": "non_eligible_gate_passed_pending",
        "existing_v002_feature_reference": {
            "path": gate.PUBLISHED_V002_FEATURE_MANIFEST_REL,
            "window_start": "2024-12-01", "window_end": "2025-02-28",
            "read": False, "mutated": False},
        "full_intended_envelope_start": "2024-03-01",
        "full_intended_envelope_end": "2025-02-28",
        "research_eligible": False, "eligibility_gate_status": "pending",
        "governance_labels": {
            "labels": "forbidden", "ml": "forbidden", "diagnostics": "forbidden",
            "strategy": "forbidden", "backtest": "forbidden",
            "research_use": "forbidden", "acquisition": "unauthorized"},
        "no_successor_authorization": True,
        "boundary_confirmations": boundary, "non_authorization_flags": nonauth,
        "v002_terminal_window_mode": "by_reference",
        "existing_v002_terminal_window": {
            "read": False, "normalized_dates_read": False,
            "start": "2024-12-01", "end": "2025-02-28"},
        "sealed_test_split_touched": False,
        "existing_v002_sealed_test_split": {
            "touched": False, "start": "2025-02-14", "end": "2025-02-28"},
        "test_holdout_touched": False, "test_rows_loaded": 0,
        "partitioning_rule": "<SYMBOL>/<YYYY>/<MM>/",
        "primary_key": ["symbol", "utc_date", "agg_trade_id", "row_index"],
        "storage_format": "parquet_zstd", "sidecar_policy": "canonical_two_space_sha256",
        "invalid_windows": [],
        "budget_witnesses": {"hard_caps_crossed": False},
        "lineage_column_value_map": {"source_normalized_manifest_sha256": "1" * 64},
    }


def _build_mini_segment(gate: object, repo_root: Path) -> tuple[Path, int, int]:
    """Build a 2-day synthetic feature segment + manifest + predecessor stubs."""
    inv1 = _write_feature_parquet(gate, date="2024-03-01", repo_root=repo_root, n=5, base_a=1000)
    inv2 = _write_feature_parquet(gate, date="2024-03-02", repo_root=repo_root, n=4, base_a=2000)
    total_rows = inv1["row_count"] + inv2["row_count"]
    total_bytes = (
        inv1["feature_parquet_size_bytes"] + inv1["feature_sidecar_size_bytes"]
        + inv2["feature_parquet_size_bytes"] + inv2["feature_sidecar_size_bytes"]
    )
    man_dir = repo_root / "data" / "microstructure" / "manifests"
    man_dir.mkdir(parents=True, exist_ok=True)

    # Predecessor stubs: normalized manifest + its sidecar, and the normalized
    # gate report with a 25/25 PASS verdict.
    norm_man = man_dir / "norm_seg.json"
    norm_man.write_text('{"x":1}\n', encoding="utf-8")
    norm_man_sha = hashlib.sha256(norm_man.read_bytes()).hexdigest()
    norm_sc = norm_man.with_suffix(norm_man.suffix + ".sha256")
    norm_sc.write_bytes(f"{norm_man_sha}  {norm_man.name}\n".encode("ascii"))
    norm_sc_sha = hashlib.sha256(norm_sc.read_bytes()).hexdigest()
    gate_dir = repo_root / "data" / "microstructure" / "gate-reports" / "normalized"
    gate_dir.mkdir(parents=True, exist_ok=True)
    gate_report = gate_dir / "norm_gate.json"
    gate_report.write_text(
        json.dumps({
            "overall_status": "pass",
            "gate_result_state": gate.REQUIRED_SOURCE_NORMALIZED_GATE_VERDICT,
            "segment_non_eligible": True, "research_eligible_after": False,
            "checks": [{"status": "pass"} for _ in range(25)],
        }) + "\n", encoding="utf-8")
    gate_sha = hashlib.sha256(gate_report.read_bytes()).hexdigest()

    inv = [inv1, inv2]
    manifest = _full_governance_manifest(
        gate, inv, total_rows, total_bytes, ["2024-03-01", "2024-03-02"])
    manifest["source_normalized_segment_manifest_sha256"] = norm_man_sha
    manifest["source_normalized_segment_manifest_sidecar_sha256"] = norm_sc_sha
    manifest["source_normalized_layer_gate_report_sha256"] = gate_sha

    man_path = man_dir / gate.SEGMENT_MANIFEST_BASENAME
    man_bytes = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{man_sha}  {man_path.name}\n".encode("ascii"))
    return man_path, total_rows, total_bytes


def _patch_mini(gate: object, mp, man_path: Path, total_rows: int, total_bytes: int) -> None:
    man = json.loads(man_path.read_bytes())
    mp.setattr(gate, "EXPECTED_DATE_END", "2024-03-02")
    mp.setattr(gate, "EXPECTED_DATE_COUNT", 2)
    mp.setattr(gate, "EXPECTED_TOTAL_ROW_COUNT", total_rows)
    mp.setattr(gate, "EXPECTED_TOTAL_FOOTPRINT_BYTES", total_bytes)
    mp.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_path.read_bytes()).hexdigest())
    mp.setattr(gate, "EXPECTED_SOURCE_NORMALIZED_MANIFEST_SHA",
               man["source_normalized_segment_manifest_sha256"])
    mp.setattr(gate, "EXPECTED_SOURCE_NORMALIZED_MANIFEST_SIDECAR_SHA",
               man["source_normalized_segment_manifest_sidecar_sha256"])
    mp.setattr(gate, "EXPECTED_SOURCE_NORMALIZED_GATE_REPORT_SHA",
               man["source_normalized_layer_gate_report_sha256"])


# --------------------------------------------------------------------------- #
# Section 1 — constants
# --------------------------------------------------------------------------- #


def test_constants(gate: object) -> None:
    assert gate.PHASE_ID == "phase-4bn-t"
    assert gate.BASE_MAIN_SHA == "e647435c81d784f610b9cf8b5e2f2dc8ee0e914e"
    assert gate.FAMILY_DIR_NAME == (
        "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s")
    assert gate.EXPECTED_DATE_COUNT == 275
    assert gate.EXPECTED_TOTAL_ROW_COUNT == 400_001_695
    assert gate.EXPECTED_TOTAL_FOOTPRINT_BYTES == 54_254_406_538
    assert gate.EXPECTED_MANIFEST_SHA == (
        "4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52")


def test_locked_schema_62_columns(gate: object) -> None:
    assert len(gate.FEATURE_SCHEMA_V002) == 62
    assert len(gate.LINEAGE_COLUMNS_V002) == 17
    assert len(gate.FEATURE_NAMES_V002) == 45
    assert gate.FEATURE_SCHEMA_VERSION_V002 == "v001"


def test_gate_result_states(gate: object) -> None:
    assert gate.GATE_PASS.startswith("FEATURE_LAYER_GATE_PASSED")
    assert "NON_ELIGIBLE" in gate.GATE_PASS and "REMAIN_PAUSED" in gate.GATE_PASS


# --------------------------------------------------------------------------- #
# Section 2 — sidecar + date validators
# --------------------------------------------------------------------------- #


def test_sidecar_valid(gate: object, short_tmp: Path) -> None:
    p = short_tmp / "x.parquet.sha256"
    p.write_bytes(f"{'a' * 64}  x.parquet\n".encode("ascii"))
    ok, sha, _ = gate._validate_canonical_sidecar(p, "x.parquet")
    assert ok and sha == "a" * 64


def test_sidecar_rejects_bad_forms(gate: object, short_tmp: Path) -> None:
    cases = {
        "bom": b"\xef\xbb\xbf" + (f"{'a' * 64}  x.parquet\n").encode(),
        "cr": (f"{'a' * 64}  x.parquet\r\n").encode(),
        "noeol": (f"{'a' * 64}  x.parquet").encode(),
        "extra": (f"{'a' * 64}  x.parquet\n{'b' * 64}  y\n").encode(),
        "onespace": (f"{'a' * 64} x.parquet\n").encode(),
        "badname": (f"{'a' * 64}  y.parquet\n").encode(),
        "badsha": (f"{'z' * 64}  x.parquet\n").encode(),
    }
    for name, body in cases.items():
        p = short_tmp / f"{name}.sha256"
        p.write_bytes(body)
        ok, _, _ = gate._validate_canonical_sidecar(p, "x.parquet")
        assert not ok, name


def test_date_in_segment_window(gate: object) -> None:
    assert gate._date_in_segment("2024-03-01")
    assert gate._date_in_segment("2024-11-30")
    assert not gate._date_in_segment("2024-12-01")   # >= v002 terminal
    assert not gate._date_in_segment("2025-02-14")   # sealed-test
    assert not gate._date_in_segment("2024-02-29")   # before window


def test_sample_dates(gate: object) -> None:
    dl = ["2024-03-01", "2024-03-15", "2024-04-01", "2024-11-30"]
    s = gate._sample_dates(dl)
    assert "2024-03-01" in s and "2024-04-01" in s and "2024-11-30" in s


# --------------------------------------------------------------------------- #
# Section 3 — manifest contract
# --------------------------------------------------------------------------- #


def test_manifest_contract_pass(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is True
    assert all(c.status == "pass" for c in checks)


def test_manifest_rejects_eligible_flip(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["research_eligible"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_eligibility_transition(
    gate: object, monkeypatch, short_tmp: Path
) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["eligibility_gate_status"] = "eligible"
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_ml_authorized_flip(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["non_authorization_flags"]["ml_authorized"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_successor_authorization(
    gate: object, monkeypatch, short_tmp: Path
) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["non_authorization_flags"]["successor_authorization_after"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_forbidden_field(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["label_horizon_ms"] = 60000
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_chronological_split_policy(
    gate: object, monkeypatch, short_tmp: Path
) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["chronological_split_policy"] = "train_test"
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_missing_field(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    del man["budget_witnesses"]
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_v002_feature_reference_read(
    gate: object, monkeypatch, short_tmp: Path
) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["existing_v002_feature_reference"]["read"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_terminal_window_read(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["existing_v002_terminal_window"]["normalized_dates_read"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


# --------------------------------------------------------------------------- #
# Section 4 — end-to-end gate
# --------------------------------------------------------------------------- #


def test_gate_pass(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    gr_root = _gr_root(short_tmp)
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=gr_root,
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.result_state == gate.GATE_PASS, [c for c in res.checks if c.status != "pass"]
    assert res.overall_status == "pass"
    assert res.parquet_count == 2 and res.sidecar_count == 2
    assert res.recomputed_total_rows == tr
    assert res.recomputed_total_footprint_bytes == tb
    # report + canonical sidecar.
    assert res.report_path is not None and res.report_path.exists()
    body = res.report_sidecar_path.read_bytes()
    assert body.endswith(b"\n") and b"  " in body and b"\r\n" not in body
    report = json.loads(res.report_path.read_bytes())
    assert report["segment_non_eligible"] is True
    assert report["research_eligible_after"] is False
    assert report["eligibility_gate_status_after"] == "pending"
    assert report["no_successor_authorization"] is True
    assert report["feature_execution_rerun"] is False
    assert report["v002_terminal_window_read"] is False
    assert report["sealed_test_split_touched"] is False
    assert report["published_v002_mutated"] is False
    assert report["data_committed"] is False
    assert report["gate_result_state"] == gate.GATE_PASS


def test_gate_missing_manifest(gate: object, short_tmp: Path) -> None:
    res = gate.run_gate(manifest_path=short_tmp / "nope.json",
                        gate_reports_root=_gr_root(short_tmp), repo_root=short_tmp,
                        write_report=True, refuse_overwrite=True)
    assert res.result_state == gate.GATE_NOT_RUN_MISSING
    assert res.overall_status == "not_run"


def test_gate_fail_on_hash_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    fam = gate.FAMILY_DIR_NAME
    target = (short_tmp / "data" / "microstructure" / "features" / fam / "BTCUSDT"
              / "2024" / "03" / "BTCUSDT-features-aggtrades-2024-03-01.parquet")
    target.write_bytes(target.read_bytes() + b"corrupt")
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.result_state == gate.GATE_FAIL
    assert res.overall_status == "fail"


def test_gate_fail_on_missing_sidecar(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    fam = gate.FAMILY_DIR_NAME
    sc = (short_tmp / "data" / "microstructure" / "features" / fam / "BTCUSDT"
          / "2024" / "03" / "BTCUSDT-features-aggtrades-2024-03-01.parquet.sha256")
    sc.unlink()
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"


def test_gate_fail_on_predecessor_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    monkeypatch.setattr(gate, "EXPECTED_SOURCE_NORMALIZED_MANIFEST_SHA", "0" * 64)
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id == "predecessor.normalized_manifest" and c.status == "fail"
               for c in res.checks)


def test_gate_fail_on_predecessor_verdict(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    # Rewrite the normalized gate report with a non-PASS verdict but keep the SHA
    # pin in sync so only the verdict/PASS-count check trips.
    gate_report = (short_tmp / "data" / "microstructure" / "gate-reports"
                   / "normalized" / "norm_gate.json")
    gate_report.write_text(
        json.dumps({"overall_status": "fail", "gate_result_state": "X",
                    "segment_non_eligible": True, "research_eligible_after": False,
                    "checks": [{"status": "pass"} for _ in range(25)]}) + "\n",
        encoding="utf-8")
    new_sha = hashlib.sha256(gate_report.read_bytes()).hexdigest()
    monkeypatch.setattr(gate, "EXPECTED_SOURCE_NORMALIZED_GATE_REPORT_SHA", new_sha)
    man = json.loads(man_path.read_bytes())
    man["source_normalized_layer_gate_report_sha256"] = new_sha
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_bytes).hexdigest())
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id == "predecessor.normalized_gate" and c.status == "fail"
               for c in res.checks)


def _repoint_first_inventory(gate: object, man_path: Path, monkeypatch, bad: dict) -> None:
    man = json.loads(man_path.read_bytes())
    man["per_file_inventory"][0] = bad
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{hashlib.sha256(man_bytes).hexdigest()}  {man_path.name}\n".encode("ascii"))
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_bytes).hexdigest())


def test_gate_fail_on_schema_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    bad = _write_feature_parquet(gate, date="2024-03-01", repo_root=short_tmp, n=5,
                                 base_a=1000, wrong_schema=True)
    _repoint_first_inventory(gate, man_path, monkeypatch, bad)
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.schema" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_forbidden_column(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    bad = _write_feature_parquet(gate, date="2024-03-01", repo_root=short_tmp, n=5,
                                 base_a=1000, forbidden_col=True)
    _repoint_first_inventory(gate, man_path, monkeypatch, bad)
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id in ("files.schema", "files.forbidden_columns") and c.status == "fail"
               for c in res.checks)


def test_gate_fail_on_v003_path_escape(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["per_file_inventory"][0]["feature_parquet_path"] = (
        "microstructure/features/v003/BTCUSDT/2024/03/"
        "BTCUSDT-features-aggtrades-2024-03-01.parquet")
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{hashlib.sha256(man_bytes).hexdigest()}  {man_path.name}\n".encode("ascii"))
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_bytes).hexdigest())
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.path_layout" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_published_v002_path(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["per_file_inventory"][0]["feature_parquet_path"] = (
        f"microstructure/features/{gate.PUBLISHED_V002_FAMILY_DIR_NAME}/BTCUSDT/2024/03/"
        "BTCUSDT-features-aggtrades-2024-03-01.parquet")
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{hashlib.sha256(man_bytes).hexdigest()}  {man_path.name}\n".encode("ascii"))
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_bytes).hexdigest())
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.path_layout" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_rowcount_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    man = json.loads(man_path.read_bytes())
    man["per_file_inventory"][0]["row_count"] = 999
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{hashlib.sha256(man_bytes).hexdigest()}  {man_path.name}\n".encode("ascii"))
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_bytes).hexdigest())
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id in ("files.row_counts", "files.sample_deep", "aggregate.rows")
               and c.status == "fail" for c in res.checks)


def test_gate_refuse_overwrite_report(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb)
    gr_root = _gr_root(short_tmp)
    res1 = gate.run_gate(manifest_path=man_path, gate_reports_root=gr_root,
                         repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res1.report_path is not None
    # Re-writing the same report basename must refuse (different run_id avoids it
    # in practice; force collision by reusing the same path).
    from prometheus.research.microstructure.normalize_io import NormalizationIOError
    with pytest.raises(NormalizationIOError):
        gate._atomic_write_json(res1.report_path, {"x": 1}, refuse_overwrite=True)


# --------------------------------------------------------------------------- #
# Section 5 — static no-network scan
# --------------------------------------------------------------------------- #


def test_no_forbidden_imports() -> None:
    src = _SCRIPT_PATH.read_text(encoding="utf-8")
    for forbidden in ("requests", "httpx", "aiohttp", "urllib.request", "urllib3",
                      "socket", "websockets", "binance", "dotenv"):
        pat = re.compile(rf"^\s*(?:import|from)\s+{re.escape(forbidden)}(?:\b|\.)", re.MULTILINE)
        assert not pat.search(src), forbidden


def test_no_credential_tokens() -> None:
    raw = _SCRIPT_PATH.read_text(encoding="utf-8")
    in_triple = False
    lines: list[str] = []
    for line in raw.splitlines():
        if line.strip().count('"""') + line.strip().count("'''") == 1:
            in_triple = not in_triple
            continue
        if in_triple:
            continue
        lines.append(line.split("#", 1)[0])
    code = "\n".join(lines).lower()
    # Neutralise the legitimate governance boundary-confirmation key, which
    # asserts the absence of MCP/Graphify work, before scanning for real tokens.
    code = code.replace("no_mcp_or_graphify", "")
    for token in ("api_key", "api-key", "listenkey", ".mcp.json", "graphify", ".env"):
        assert token not in code, token
