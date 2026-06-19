"""Offline tests for the Phase 4bn-X label-layer eligibility gate.

Loads ``scripts/phase4bn_x_validate_label_pre_v002_gate.py`` by file path and
exercises the gate's sidecar/date/manifest validators, full per-row label
scan (schema / forbidden-column / constant-lineage / censoring / direction /
any-censored OR / reference-bound / invalid-price), label_config_hash
recomputation, predecessor integrity, fail-closed paths, gate-report path
guards, and gate-report posture — using only temp directories and small
synthetic 40-column LABEL_SCHEMA_V002 label Parquet fixtures. No network, no
real production data, no sealed-test data, no data/research output.
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
    _REPO_ROOT / "scripts" / "phase4bn_x_validate_label_pre_v002_gate.py"
)


def _load() -> object:
    name = "phase4bn_x_validate_label_pre_v002_gate_under_test"
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
    return base / "data" / "microstructure" / "gate-reports" / "labels"


@pytest.fixture
def short_tmp() -> Iterator[Path]:
    base = Path(tempfile.mkdtemp(prefix="p4bnx_"))
    try:
        yield base
    finally:
        shutil.rmtree(base, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Synthetic label parquet builder
# --------------------------------------------------------------------------- #


def _label_schema(gate: object) -> pa.Schema:
    """Construct a pyarrow schema in LABEL_SCHEMA_V002 canonical order."""
    horizons = gate.LABEL_HORIZONS_V002
    int64_cols = {"row_index", "agg_trade_id", "feature_timestamp_ms",
                  "source_transact_time_ms"}
    string_cols = {
        "dataset_family", "dataset_version", "label_schema_version",
        "source_feature_dataset_family", "source_feature_dataset_version",
        "source_feature_manifest_sha256", "source_feature_parquet_sha256",
        "source_feature_successor_state_sha256",
        "source_phase_4bm_j_gate_report_sha256",
        "source_normalized_manifest_sha256", "source_raw_manifest_sha256",
        "symbol", "utc_date", "label_config_hash",
    }
    nint64 = {f"reference_row_index_{h}" for h in horizons} | {
        f"reference_timestamp_ms_{h}" for h in horizons}
    nfloat = {f"forward_log_return_{h}" for h in horizons}
    nint8 = {f"forward_direction_{h}" for h in horizons}
    bools = {f"horizon_censored_flag_{h}" for h in horizons} | {
        "label_invalid_price_flag", "label_any_censored_flag"}
    fields = []
    for col in gate.LABEL_SCHEMA_V002:
        if col in int64_cols:
            fields.append(pa.field(col, pa.int64(), nullable=False))
        elif col in string_cols:
            fields.append(pa.field(col, pa.string(), nullable=False))
        elif col in nint64:
            fields.append(pa.field(col, pa.int64(), nullable=True))
        elif col in nfloat:
            fields.append(pa.field(col, pa.float64(), nullable=True))
        elif col in nint8:
            fields.append(pa.field(col, pa.int8(), nullable=True))
        elif col in bools:
            fields.append(pa.field(col, pa.bool_(), nullable=False))
        else:  # pragma: no cover - defensive
            raise AssertionError(f"unclassified {col}")
    return pa.schema(fields)


def _gen_label_columns(gate: object, *, ts_list, terminal, lineage):
    """Build a column dict + per-horizon censored counts for a day's rows."""
    horizons = gate.LABEL_HORIZONS_V002
    horizon_ms = dict(zip(horizons, gate.LABEL_HORIZON_MS_V002, strict=True))
    n = len(ts_list)
    cols: dict[str, list] = {}
    const = {
        "dataset_family": "microstructure_labels_aggtrades_v001",
        "dataset_version": "v002", "label_schema_version": "v001",
        "source_feature_dataset_family": "microstructure_features_aggtrades_v001",
        "source_feature_dataset_version": "v002",
        "source_feature_manifest_sha256": lineage["feat_man"],
        "source_feature_parquet_sha256": "f" * 64,
        "source_feature_successor_state_sha256": lineage["norm_gate"],
        "source_phase_4bm_j_gate_report_sha256": lineage["feat_gate"],
        "source_normalized_manifest_sha256": lineage["norm_man"],
        "source_raw_manifest_sha256": lineage["raw_man"],
        "symbol": "BTCUSDT", "utc_date": lineage["date"],
        "label_config_hash": lineage["label_config_hash"],
    }
    for k, v in const.items():
        cols[k] = [v] * n
    cols["row_index"] = list(range(n))
    cols["agg_trade_id"] = [lineage["base_agg"] + i for i in range(n)]
    cols["feature_timestamp_ms"] = list(ts_list)
    cols["source_transact_time_ms"] = list(ts_list)
    counts = dict.fromkeys(horizons, 0)
    any_flags = [False] * n
    flr = {h: [None] * n for h in horizons}
    fdir = {h: [None] * n for h in horizons}
    rri = {h: [None] * n for h in horizons}
    rts = {h: [None] * n for h in horizons}
    flags = {h: [False] * n for h in horizons}
    for i, ft in enumerate(ts_list):
        for h in horizons:
            target = ft + horizon_ms[h]
            censored = target > terminal
            flags[h][i] = censored
            if censored:
                counts[h] += 1
                any_flags[i] = True
            else:
                rri[h][i] = i
                rts[h][i] = target  # <= target and <= terminal
                flr[h][i] = 0.001
                fdir[h][i] = 1
    for h in horizons:
        cols[f"forward_log_return_{h}"] = flr[h]
    for h in horizons:
        cols[f"forward_direction_{h}"] = fdir[h]
    for h in horizons:
        cols[f"reference_row_index_{h}"] = rri[h]
        cols[f"reference_timestamp_ms_{h}"] = rts[h]
        cols[f"horizon_censored_flag_{h}"] = flags[h]
    cols["label_invalid_price_flag"] = [False] * n
    cols["label_any_censored_flag"] = any_flags
    return cols, counts


def _write_label_parquet(gate: object, *, date, repo_root, ts_list, terminal,
                         lineage, drop_col=False, forbidden_col=False,
                         break_flag=False, bad_ref=False, bad_dir=False,
                         set_invalid=False, break_or=False):
    """Write a synthetic 40-column label parquet + sidecar; return inventory entry."""
    cols, counts = _gen_label_columns(gate, ts_list=ts_list, terminal=terminal,
                                      lineage=lineage)
    if break_flag:  # flip a censor flag away from truth
        cols["horizon_censored_flag_60s"][0] = not cols["horizon_censored_flag_60s"][0]
    if bad_ref:  # reference timestamp beyond the envelope terminal
        cols["reference_timestamp_ms_1s"][0] = terminal + 10_000
    if bad_dir:  # direction outside {-1,0,1}
        cols["forward_direction_1s"][0] = 2
    if set_invalid:  # invalid-price flag set while manifest count stays 0
        cols["label_invalid_price_flag"][0] = True
    if break_or:  # any-censored flag inconsistent with horizon OR
        cols["label_any_censored_flag"][0] = not cols["label_any_censored_flag"][0]
    schema = _label_schema(gate)
    if drop_col:
        cols.pop("label_config_hash")
        schema = pa.schema([f for f in schema if f.name != "label_config_hash"])
    if forbidden_col:
        cols["alpha_signal"] = [0.0] * len(ts_list)
        schema = pa.schema(list(schema) + [pa.field("alpha_signal", pa.float64())])
    table = pa.Table.from_pydict(cols, schema=schema)
    yyyy, mm, _dd = date.split("-")
    fam = gate.FAMILY_DIR_NAME
    pq_path = (repo_root / "data" / "microstructure" / "labels" / fam / "BTCUSDT"
               / yyyy / mm / f"BTCUSDT-labels-aggtrades-{date}.parquet")
    pq_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, pq_path, compression="zstd")
    sha = hashlib.sha256(pq_path.read_bytes()).hexdigest()
    size = pq_path.stat().st_size
    sc_path = pq_path.with_suffix(pq_path.suffix + ".sha256")
    sc_path.write_bytes(f"{sha}  {pq_path.name}\n".encode("ascii"))
    rel = (f"microstructure/labels/{fam}/BTCUSDT/{yyyy}/{mm}/"
           f"BTCUSDT-labels-aggtrades-{date}.parquet")
    return {
        "date": date, "symbol": "BTCUSDT",
        "label_parquet_path": rel, "label_parquet_sha256": sha,
        "label_parquet_size_bytes": size,
        "label_sidecar_path": rel + ".sha256",
        "label_sidecar_sha256": hashlib.sha256(sc_path.read_bytes()).hexdigest(),
        "label_sidecar_size_bytes": sc_path.stat().st_size,
        "row_count": len(ts_list),
        "per_horizon_censored_counts": counts,
        "invalid_price_row_count": 0,
        "paired_source_feature_parquet_sha256": "f" * 64,
        "paired_source_normalized_parquet_sha256": "e" * 64,
        "status": "produced_verified",
    }, size, counts


def _stub_predecessors(gate: object, repo_root: Path, monkeypatch):
    """Create predecessor stub files + monkeypatch gate EXPECTED_* SHAs; return lineage."""
    man_dir = repo_root / "data" / "microstructure" / "manifests"
    man_dir.mkdir(parents=True, exist_ok=True)
    feat_gr = repo_root / "data" / "microstructure" / "gate-reports" / "features"
    norm_gr = repo_root / "data" / "microstructure" / "gate-reports" / "normalized"
    feat_gr.mkdir(parents=True, exist_ok=True)
    norm_gr.mkdir(parents=True, exist_ok=True)

    def _write_manifest(path: Path, body: dict) -> tuple[str, str]:
        b = (json.dumps(body, sort_keys=True, indent=2) + "\n").encode("utf-8")
        path.write_bytes(b)
        sha = hashlib.sha256(b).hexdigest()
        sc = path.with_suffix(path.suffix + ".sha256")
        sc.write_bytes(f"{sha}  {path.name}\n".encode("ascii"))
        return sha, hashlib.sha256(sc.read_bytes()).hexdigest()

    feat_man = man_dir / "feat_seg.json"
    feat_man_sha, feat_man_sc_sha = _write_manifest(feat_man, {
        "research_eligible": False, "eligibility_gate_status": "pending",
        "feature_config_hash": gate.EXPECTED_FEATURE_CONFIG_HASH})
    norm_man = man_dir / "norm_seg.json"
    norm_man_sha, norm_man_sc_sha = _write_manifest(norm_man, {
        "research_eligible": False, "eligibility_gate_status": "pending"})
    raw_man = man_dir / "raw_seg.json"
    raw_man_sha, _ = _write_manifest(raw_man, {"x": 1})

    feat_gate = feat_gr / "feat_gate.json"
    feat_gate.write_text(json.dumps({
        "overall_status": "pass",
        "gate_result_state": gate.REQUIRED_FEATURE_GATE_VERDICT,
        "segment_non_eligible": True, "research_eligible_after": False,
        "checks": [{"status": "pass"} for _ in range(27)]}) + "\n", encoding="utf-8")
    feat_gate_sha = hashlib.sha256(feat_gate.read_bytes()).hexdigest()
    norm_gate = norm_gr / "norm_gate.json"
    norm_gate.write_text(json.dumps({
        "overall_status": "pass",
        "gate_result_state": gate.REQUIRED_NORMALIZED_GATE_VERDICT,
        "segment_non_eligible": True, "research_eligible_after": False,
        "checks": [{"status": "pass"} for _ in range(25)]}) + "\n", encoding="utf-8")
    norm_gate_sha = hashlib.sha256(norm_gate.read_bytes()).hexdigest()

    monkeypatch.setattr(gate, "EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA", feat_man_sha)
    monkeypatch.setattr(gate, "EXPECTED_FEATURE_SEGMENT_MANIFEST_SIDECAR_SHA", feat_man_sc_sha)
    monkeypatch.setattr(gate, "EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA", feat_gate_sha)
    monkeypatch.setattr(gate, "EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA", norm_man_sha)
    monkeypatch.setattr(gate, "EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA", norm_man_sc_sha)
    monkeypatch.setattr(gate, "EXPECTED_NORMALIZED_GATE_REPORT_SHA", norm_gate_sha)
    monkeypatch.setattr(gate, "EXPECTED_RAW_SEGMENT_MANIFEST_SHA", raw_man_sha)

    label_config_hash = gate.recompute_segment_label_config_hash(
        source_feature_manifest_sha256=feat_man_sha,
        source_feature_layer_gate_report_sha256=feat_gate_sha,
        source_normalized_manifest_sha256=norm_man_sha,
        source_normalized_layer_gate_report_sha256=norm_gate_sha,
        source_raw_manifest_sha256=raw_man_sha,
        feature_config_hash=gate.EXPECTED_FEATURE_CONFIG_HASH)
    monkeypatch.setattr(gate, "EXPECTED_LABEL_CONFIG_HASH", label_config_hash)
    return {
        "feat_man": feat_man_sha, "feat_man_sc": feat_man_sc_sha,
        "feat_gate": feat_gate_sha, "norm_man": norm_man_sha,
        "norm_man_sc": norm_man_sc_sha, "norm_gate": norm_gate_sha,
        "raw_man": raw_man_sha, "label_config_hash": label_config_hash,
        "feat_man_path": "feat_seg.json", "feat_gate_path": "feat_gate.json",
        "norm_man_path": "norm_seg.json", "norm_gate_path": "norm_gate.json",
        "raw_man_path": "raw_seg.json",
    }


def _build_manifest(gate: object, lineage, inv, counts, total_rows, total_bytes,
                    terminal, dates) -> dict:
    return {
        "dataset_family": "microstructure_labels_aggtrades_v001",
        "dataset_version": "v002", "version": "v002", "label_schema_version": "v001",
        "label_family_id": "microstructure_labels_aggtrades_v001",
        "segment_label": "pre_v002_segment", "data_family": "aggTrades",
        "symbol": "BTCUSDT", "symbol_list": ["BTCUSDT"], "market": "usdm_futures",
        "dataset_category": "labels", "phase": "4bn-W", "phase_id": "phase-4bn-w",
        "source_phase_boundary": "4bn-T", "created_at_unix_ms": 1, "created_at_utc": "x",
        "code_commit_sha": gate.BASE_MAIN_SHA, "base_commit_sha": gate.BASE_MAIN_SHA,
        "label_config_hash": lineage["label_config_hash"],
        "feature_config_hash": gate.EXPECTED_FEATURE_CONFIG_HASH,
        "column_count": 40, "label_column_count": 8, "support_column_count": 14,
        "lineage_column_count": 17,
        "schema_column_list": list(gate.LABEL_SCHEMA_V002),
        "label_list": list(gate.LABEL_NAMES_V002),
        "support_column_list": list(gate.LABEL_SUPPORT_COLUMN_NAMES_V002),
        "lineage_column_list": list(gate.LABEL_LINEAGE_COLUMNS_V002),
        "horizon_list": list(gate.LABEL_HORIZONS_V002),
        "horizon_ms_list": list(gate.LABEL_HORIZON_MS_V002),
        "envelope_terminal_unix_ms": terminal,
        "envelope_terminal_utc_date": dates[-1],
        "censored_per_horizon": counts, "invalid_price_row_count": 0,
        "anchor_policy": "x", "future_reference_policy": "x",
        "direction_threshold_policy": "x", "null_censoring_policy": "x",
        "dtype_policy": "x",
        "label_config_hash_input_fields": ["x"],
        "lineage_column_reinterpretation": {
            "source_phase_4bm_j_gate_report_sha256": {
                "bound_artefact": "phase_4bn_t_feature_layer_gate_report",
                "value": lineage["feat_gate"]},
            "source_feature_successor_state_sha256": {
                "bound_artefact": "phase_4bn_p_normalized_layer_gate_report",
                "value": lineage["norm_gate"]}},
        "date_start": dates[0], "date_end": dates[-1], "date_count": len(dates),
        "date_list": dates, "expected_file_count": len(dates),
        "produced_file_count": len(dates), "total_row_count": total_rows,
        "total_footprint_bytes": total_bytes, "per_day_outputs": inv,
        "source_feature_dataset_family": "microstructure_features_aggtrades_v001",
        "source_feature_dataset_version": "v002",
        "source_feature_segment_manifest_path":
            "data/microstructure/manifests/feat_seg.json",
        "source_feature_segment_manifest_sha256": lineage["feat_man"],
        "source_feature_segment_manifest_sidecar_sha256": lineage["feat_man_sc"],
        "source_feature_layer_gate_report_path":
            "data/microstructure/gate-reports/features/feat_gate.json",
        "source_feature_layer_gate_report_sha256": lineage["feat_gate"],
        "source_feature_schema_version": "FEATURE_SCHEMA_V002",
        "source_normalized_dataset_family": "microstructure_normalized_aggtrades_v001",
        "source_normalized_dataset_version": "v002",
        "source_normalized_segment_manifest_path":
            "data/microstructure/manifests/norm_seg.json",
        "source_normalized_segment_manifest_sha256": lineage["norm_man"],
        "source_normalized_segment_manifest_sidecar_sha256": lineage["norm_man_sc"],
        "source_normalized_layer_gate_report_path":
            "data/microstructure/gate-reports/normalized/norm_gate.json",
        "source_normalized_layer_gate_report_sha256": lineage["norm_gate"],
        "source_normalized_schema_version": "NORMALIZED_SCHEMA_V001",
        "source_raw_segment_manifest_path":
            "data/microstructure/manifests/raw_seg.json",
        "source_raw_segment_manifest_sha256": lineage["raw_man"],
        "source_eligibility_posture": "non_eligible_gate_passed_pending",
        "existing_v002_label_reference": {
            "path": gate.PUBLISHED_V002_LABEL_MANIFEST_REL,
            "window_start": "2024-12-01", "window_end": "2025-02-28",
            "read": False, "mutated": False},
        "existing_v002_terminal_window": {
            "read": False, "feature_normalized_raw_dates_read": False,
            "start": "2024-12-01", "end": "2025-02-28"},
        "existing_v002_sealed_test_split": {
            "touched": False, "start": "2025-02-14", "end": "2025-02-28"},
        "full_intended_envelope_start": "2024-03-01",
        "full_intended_envelope_end": "2025-02-28",
        "research_eligible": False, "eligibility_gate_status": "pending",
        "no_successor_authorization": True, "ml_use": "forbidden",
        "diagnostics_use": "forbidden", "strategy_use": "forbidden",
        "backtest_use": "forbidden", "chronological_split_policy": "not_yet_defined",
        "governance_labels": {
            "ml": "forbidden", "diagnostics": "forbidden", "strategy": "forbidden",
            "backtest": "forbidden", "research_use": "forbidden",
            "paper_shadow_live": "forbidden", "deployment": "forbidden",
            "exchange_write": "forbidden", "acquisition": "unauthorized",
            "labels": "allowed_by_future_phase_only"},
        "boundary_confirmations": {"no_ml": True, "no_backtest": True},
        "non_authorization_flags": {
            "acquisition_authorized": False, "backtest_authorized": False,
            "diagnostics_authorized": False,
            "label_family_research_use_authorized": False, "ml_authorized": False,
            "stage_5_label_cleared": False, "strategy_authorized": False,
            "successor_authorization_after": False},
        "v002_terminal_window_mode": "by_reference",
        "sealed_test_split_touched": False, "test_holdout_touched": False,
        "test_rows_loaded": 0, "partitioning_rule": "<SYMBOL>/<YYYY>/<MM>/",
        "primary_key": ["symbol", "utc_date", "agg_trade_id", "row_index"],
        "storage_format": "parquet_zstd", "sidecar_policy": "canonical_two_space_sha256",
        "budget_witnesses": {"hard_caps_crossed": False},
    }


def _build_mini(gate: object, repo_root: Path, monkeypatch, **pq_kwargs):
    """Build a 2-day synthetic label segment + predecessor stubs + manifest; patch EXPECTED_*."""
    (repo_root / ".gitignore").write_text(
        "data/microstructure/\ndata/research/\n", encoding="utf-8")
    lineage = _stub_predecessors(gate, repo_root, monkeypatch)
    d1, d2 = "2024-03-01", "2024-03-02"

    def _day_start(d):
        return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000)

    # terminal == last ts of the final day; final-day rows straddle the terminal.
    terminal = _day_start(d2) + 80_000
    ts1 = [_day_start(d1) + 1000 + i * 1000 for i in range(5)]  # far from terminal
    ts2 = [terminal - 80_000, terminal - 60_000, terminal - 40_000,
           terminal - 20_000, terminal]

    lin1 = {**lineage, "date": d1, "base_agg": 1000}
    lin2 = {**lineage, "date": d2, "base_agg": 5000}
    inv1, b1, c1 = _write_label_parquet(
        gate, date=d1, repo_root=repo_root, ts_list=ts1, terminal=terminal, lineage=lin1)
    inv2, b2, c2 = _write_label_parquet(
        gate, date=d2, repo_root=repo_root, ts_list=ts2, terminal=terminal, lineage=lin2,
        **pq_kwargs)
    total_rows = inv1["row_count"] + inv2["row_count"]
    total_bytes = (b1 + inv1["label_sidecar_size_bytes"]
                   + b2 + inv2["label_sidecar_size_bytes"])
    counts = {h: c1[h] + c2[h] for h in gate.LABEL_HORIZONS_V002}

    manifest = _build_manifest(gate, lineage, [inv1, inv2], counts, total_rows,
                               total_bytes, terminal, [d1, d2])
    man_dir = repo_root / "data" / "microstructure" / "manifests"
    man_path = man_dir / gate.SEGMENT_MANIFEST_BASENAME
    man_bytes = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    sc = man_path.with_suffix(man_path.suffix + ".sha256")
    sc.write_bytes(f"{man_sha}  {man_path.name}\n".encode("ascii"))

    monkeypatch.setattr(gate, "EXPECTED_DATE_START", d1)
    monkeypatch.setattr(gate, "EXPECTED_DATE_END", d2)
    monkeypatch.setattr(gate, "EXPECTED_DATE_COUNT", 2)
    monkeypatch.setattr(gate, "EXPECTED_TOTAL_ROW_COUNT", total_rows)
    monkeypatch.setattr(gate, "EXPECTED_TOTAL_FOOTPRINT_BYTES", total_bytes)
    monkeypatch.setattr(gate, "EXPECTED_ENVELOPE_TERMINAL_UNIX_MS", terminal)
    monkeypatch.setattr(gate, "EXPECTED_ENVELOPE_TERMINAL_UTC_DATE", d2)
    monkeypatch.setattr(gate, "EXPECTED_CENSORED_PER_HORIZON", counts)
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", man_sha)
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SIDECAR_SHA",
                        hashlib.sha256(sc.read_bytes()).hexdigest())
    return man_path


def _run(gate, man_path, repo_root):
    return gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(repo_root),
                         repo_root=repo_root, write_report=True, refuse_overwrite=True)


def _failed(res):
    return [f"{c.check_id}: {c.detail}" for c in res.checks if c.status != "pass"]


# --------------------------------------------------------------------------- #
# Section 1 — constants / static scans
# --------------------------------------------------------------------------- #


def test_constants(gate: object) -> None:
    assert gate.PHASE_ID == "phase-4bn-x"
    assert gate.BASE_MAIN_SHA == "5bcae53ee843759a6c81c14d71a66dc241023e31"
    assert gate.FAMILY_DIR_NAME == (
        "microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w")
    assert gate.EXPECTED_DATE_COUNT == 275
    assert gate.EXPECTED_TOTAL_ROW_COUNT == 400_001_695
    assert gate.EXPECTED_TOTAL_FOOTPRINT_BYTES == 15_654_082_679
    assert gate.EXPECTED_ENVELOPE_TERMINAL_UNIX_MS == 1_733_011_199_331
    assert gate.EXPECTED_CENSORED_PER_HORIZON == {"1s": 3, "5s": 20, "15s": 42, "60s": 216}
    assert gate.EXPECTED_INVALID_PRICE_ROW_COUNT == 0
    assert gate.EXPECTED_MANIFEST_SHA == (
        "69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161")


def test_locked_schema_40_columns(gate: object) -> None:
    assert len(gate.LABEL_SCHEMA_V002) == 40
    assert len(gate.LABEL_NAMES_V002) == 8
    assert len(gate.LABEL_SUPPORT_COLUMN_NAMES_V002) == 14
    assert len(gate.LABEL_LINEAGE_COLUMNS_V002) == 17


def test_gate_result_states(gate: object) -> None:
    assert gate.GATE_PASS.startswith("LABEL_LAYER_GATE_PASSED")
    assert "NON_ELIGIBLE" in gate.GATE_PASS and "REMAIN_PAUSED" in gate.GATE_PASS


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
    code = code.replace("no_mcp_or_graphify", "")
    # ``.env`` is a substring of the legitimate domain word "envelope"; neutralise
    # it before scanning for the real dotfile token.
    code = code.replace("envelope", "")
    for token in ("api_key", "api-key", "listenkey", ".mcp.json", "graphify", ".env"):
        assert token not in code, token


# --------------------------------------------------------------------------- #
# Section 2 — sidecar / date / hash unit validators
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


def test_label_config_hash_recompute_deterministic(gate: object) -> None:
    kw = dict(
        source_feature_manifest_sha256=gate.EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA,
        source_feature_layer_gate_report_sha256=gate.EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA,
        source_normalized_manifest_sha256=gate.EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA,
        source_normalized_layer_gate_report_sha256=gate.EXPECTED_NORMALIZED_GATE_REPORT_SHA,
        source_raw_manifest_sha256=gate.EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        feature_config_hash=gate.EXPECTED_FEATURE_CONFIG_HASH)
    h1 = gate.recompute_segment_label_config_hash(**kw)
    h2 = gate.recompute_segment_label_config_hash(**kw)
    assert h1 == h2 == gate.EXPECTED_LABEL_CONFIG_HASH


def test_label_config_hash_mismatch_on_changed_input(gate: object) -> None:
    base = gate.recompute_segment_label_config_hash(
        source_feature_manifest_sha256=gate.EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA,
        source_feature_layer_gate_report_sha256=gate.EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA,
        source_normalized_manifest_sha256=gate.EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA,
        source_normalized_layer_gate_report_sha256=gate.EXPECTED_NORMALIZED_GATE_REPORT_SHA,
        source_raw_manifest_sha256=gate.EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        feature_config_hash=gate.EXPECTED_FEATURE_CONFIG_HASH)
    other = gate.recompute_segment_label_config_hash(
        source_feature_manifest_sha256="a" * 64,
        source_feature_layer_gate_report_sha256=gate.EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA,
        source_normalized_manifest_sha256=gate.EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA,
        source_normalized_layer_gate_report_sha256=gate.EXPECTED_NORMALIZED_GATE_REPORT_SHA,
        source_raw_manifest_sha256=gate.EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        feature_config_hash=gate.EXPECTED_FEATURE_CONFIG_HASH)
    assert base != other


def test_recompute_rejects_published_v002_feature_hash(gate: object) -> None:
    with pytest.raises(gate.NormalizationIOError):
        gate.recompute_segment_label_config_hash(
            source_feature_manifest_sha256=gate.EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA,
            source_feature_layer_gate_report_sha256=gate.EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA,
            source_normalized_manifest_sha256=gate.EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA,
            source_normalized_layer_gate_report_sha256=gate.EXPECTED_NORMALIZED_GATE_REPORT_SHA,
            source_raw_manifest_sha256=gate.EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
            feature_config_hash=gate.PUBLISHED_V002_FEATURE_CONFIG_HASH)


# --------------------------------------------------------------------------- #
# Section 3 — gate report path guards
# --------------------------------------------------------------------------- #


def test_report_path_guard_rejects_outside(gate: object, short_tmp: Path) -> None:
    with pytest.raises(gate.NormalizationIOError):
        gate._assert_under_gate_reports_labels(short_tmp / "evil.json", short_tmp)


def test_report_path_guard_rejects_other_microstructure_dir(gate: object, short_tmp: Path) -> None:
    bad = short_tmp / "data" / "microstructure" / "labels" / "x.json"
    with pytest.raises(gate.NormalizationIOError):
        gate._assert_under_gate_reports_labels(bad, short_tmp)


def test_report_path_guard_allows_labels_gate_dir(gate: object, short_tmp: Path) -> None:
    good = _gr_root(short_tmp) / "r.json"
    gate._assert_under_gate_reports_labels(good, short_tmp)  # no raise


def test_atomic_write_refuses_overwrite(gate: object, short_tmp: Path) -> None:
    p = _gr_root(short_tmp) / "r.json"
    gate._atomic_write_json(p, {"x": 1}, repo_root=short_tmp, refuse_overwrite=True)
    with pytest.raises(gate.NormalizationIOError):
        gate._atomic_write_json(p, {"x": 2}, repo_root=short_tmp, refuse_overwrite=True)


# --------------------------------------------------------------------------- #
# Section 4 — manifest contract
# --------------------------------------------------------------------------- #


def test_manifest_contract_pass(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is True, [
        c.detail for c in checks if c.status != "pass"]


@pytest.mark.parametrize("mutate", [
    ("research_eligible", True),
    ("eligibility_gate_status", "eligible"),
    ("no_successor_authorization", False),
    ("ml_use", "allowed"),
    ("backtest_use", "allowed"),
    ("v002_terminal_window_mode", "read"),
    ("sealed_test_split_touched", True),
    ("test_holdout_touched", True),
    ("test_rows_loaded", 5),
    ("chronological_split_policy", "train_test"),
])
def test_manifest_rejects_posture_flips(gate, monkeypatch, short_tmp, mutate) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    man[mutate[0]] = mutate[1]
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_ml_authorized_flag(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    man["non_authorization_flags"]["ml_authorized"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_governance_allowed(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    man["governance_labels"]["ml"] = "allowed"
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_published_v002_read(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    man["existing_v002_label_reference"]["read"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_terminal_dates_read(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    man["existing_v002_terminal_window"]["feature_normalized_raw_dates_read"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_missing_field(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    del man["budget_witnesses"]
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_forbidden_field(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    man["model_score"] = 1
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_rejects_broken_lineage_remap(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    man = json.loads(man_path.read_bytes())
    man["lineage_column_reinterpretation"][
        "source_phase_4bm_j_gate_report_sha256"]["value"] = "0" * 64
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


# --------------------------------------------------------------------------- #
# Section 5 — end-to-end gate
# --------------------------------------------------------------------------- #


def test_gate_pass(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.result_state == gate.GATE_PASS, _failed(res)
    assert res.overall_status == "pass"
    assert res.parquet_count == 2 and res.sidecar_count == 2
    assert res.recomputed_total_rows == 10
    assert res.recomputed_invalid_price_row_count == 0
    assert res.recomputed_envelope_terminal_unix_ms == gate.EXPECTED_ENVELOPE_TERMINAL_UNIX_MS
    assert res.recomputed_label_config_hash == gate.EXPECTED_LABEL_CONFIG_HASH
    # report + canonical sidecar
    assert res.report_path is not None and res.report_path.exists()
    body = res.report_sidecar_path.read_bytes()
    assert body.endswith(b"\n") and b"  " in body and b"\r\n" not in body
    report = json.loads(res.report_path.read_bytes())
    assert report["segment_non_eligible"] is True
    assert report["research_eligible_after"] is False
    assert report["eligibility_gate_status_after"] == "pending"
    assert report["no_successor_authorization"] is True
    assert report["label_execution_rerun"] is False
    assert report["v002_terminal_window_read"] is False
    assert report["sealed_test_split_touched"] is False
    assert report["published_v002_label_mutated"] is False
    assert report["data_committed"] is False
    assert report["gate_result_state"] == gate.GATE_PASS
    # output confined to gate-reports/labels
    assert res.report_path.parent == _gr_root(short_tmp)


def test_gate_missing_manifest(gate: object, short_tmp: Path) -> None:
    res = gate.run_gate(manifest_path=short_tmp / "nope.json",
                        gate_reports_root=_gr_root(short_tmp), repo_root=short_tmp,
                        write_report=True, refuse_overwrite=True)
    assert res.result_state == gate.GATE_NOT_RUN_MISSING
    assert res.overall_status == "not_run"


def test_gate_fail_on_hash_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    fam = gate.FAMILY_DIR_NAME
    target = (short_tmp / "data" / "microstructure" / "labels" / fam / "BTCUSDT"
              / "2024" / "03" / "BTCUSDT-labels-aggtrades-2024-03-01.parquet")
    target.write_bytes(target.read_bytes() + b"corrupt")
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.hash_integrity" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_missing_sidecar(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    fam = gate.FAMILY_DIR_NAME
    sc = (short_tmp / "data" / "microstructure" / "labels" / fam / "BTCUSDT"
          / "2024" / "03" / "BTCUSDT-labels-aggtrades-2024-03-01.parquet.sha256")
    sc.unlink()
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"


def test_gate_fail_on_schema_drop_column(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch, drop_col=True)
    # rewrite manifest sha after the parquet sha changed
    _resync_manifest(gate, man_path, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id in ("files.schema", "files.full_scan") and c.status == "fail"
               for c in res.checks)


def test_gate_fail_on_forbidden_column(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch, forbidden_col=True)
    _resync_manifest(gate, man_path, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id in ("files.forbidden_columns", "files.schema", "files.full_scan")
               and c.status == "fail" for c in res.checks)


def test_gate_fail_on_censor_flag_flip(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch, break_flag=True)
    _resync_manifest(gate, man_path, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.full_scan" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_reference_past_terminal(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch, bad_ref=True)
    _resync_manifest(gate, man_path, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.full_scan" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_direction_domain(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch, bad_dir=True)
    _resync_manifest(gate, man_path, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.full_scan" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_any_censored_or(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch, break_or=True)
    _resync_manifest(gate, man_path, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.full_scan" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_invalid_price_flag(gate: object, monkeypatch, short_tmp: Path) -> None:
    # invalid flag set on a row while manifest invalid count stays 0 -> full_scan fail
    man_path = _build_mini(gate, short_tmp, monkeypatch, set_invalid=True)
    _resync_manifest(gate, man_path, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"


def test_gate_fail_on_predecessor_manifest_mismatch(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    monkeypatch.setattr(gate, "EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA", "0" * 64)
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "predecessor.normalized_manifest" and c.status == "fail"
               for c in res.checks)


def test_gate_fail_on_predecessor_gate_not_pass(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    gate_report = (short_tmp / "data" / "microstructure" / "gate-reports"
                   / "features" / "feat_gate.json")
    gate_report.write_text(json.dumps({
        "overall_status": "fail", "gate_result_state": "X",
        "segment_non_eligible": True, "research_eligible_after": False,
        "checks": [{"status": "pass"} for _ in range(27)]}) + "\n", encoding="utf-8")
    monkeypatch.setattr(gate, "EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA",
                        hashlib.sha256(gate_report.read_bytes()).hexdigest())
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "predecessor.feature_gate" and c.status == "fail"
               for c in res.checks)


def test_gate_fail_on_predecessor_eligible(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    feat_man = short_tmp / "data" / "microstructure" / "manifests" / "feat_seg.json"
    body = {"research_eligible": True, "eligibility_gate_status": "eligible",
            "feature_config_hash": gate.EXPECTED_FEATURE_CONFIG_HASH}
    b = (json.dumps(body, sort_keys=True, indent=2) + "\n").encode("utf-8")
    feat_man.write_bytes(b)
    monkeypatch.setattr(gate, "EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA",
                        hashlib.sha256(b).hexdigest())
    res = _run(gate, man_path, short_tmp)
    assert res.overall_status == "fail"
    assert any(c.check_id == "predecessor.feature_manifest" and c.status == "fail"
               for c in res.checks)


def test_gate_writes_only_under_gate_reports_labels(gate, monkeypatch, short_tmp) -> None:
    man_path = _build_mini(gate, short_tmp, monkeypatch)
    res = _run(gate, man_path, short_tmp)
    rel = res.report_path.resolve().relative_to(short_tmp.resolve()).as_posix()
    assert rel.startswith("data/microstructure/gate-reports/labels/")
    assert not (short_tmp / "data" / "research").exists()


def _resync_manifest(gate, man_path, monkeypatch) -> None:
    """Re-pin per_day_outputs SHAs/sizes and manifest SHA after a parquet was regenerated."""
    man = json.loads(man_path.read_bytes())
    repo_root = man_path.resolve().parents[3]
    for entry in man["per_day_outputs"]:
        pq_path = gate._resolve_local_path(repo_root, entry["label_parquet_path"])
        sha = hashlib.sha256(pq_path.read_bytes()).hexdigest()
        entry["label_parquet_sha256"] = sha
        entry["label_parquet_size_bytes"] = pq_path.stat().st_size
        sc = pq_path.with_suffix(pq_path.suffix + ".sha256")
        sc.write_bytes(f"{sha}  {pq_path.name}\n".encode("ascii"))
        entry["label_sidecar_sha256"] = hashlib.sha256(sc.read_bytes()).hexdigest()
        entry["label_sidecar_size_bytes"] = sc.stat().st_size
    total_bytes = sum(e["label_parquet_size_bytes"] + e["label_sidecar_size_bytes"]
                      for e in man["per_day_outputs"])
    man["total_footprint_bytes"] = total_bytes
    monkeypatch.setattr(gate, "EXPECTED_TOTAL_FOOTPRINT_BYTES", total_bytes)
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    sc = man_path.with_suffix(man_path.suffix + ".sha256")
    sc.write_bytes(f"{man_sha}  {man_path.name}\n".encode("ascii"))
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", man_sha)
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SIDECAR_SHA",
                        hashlib.sha256(sc.read_bytes()).hexdigest())
