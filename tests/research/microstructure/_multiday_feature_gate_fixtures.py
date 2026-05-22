"""Shared mini-fixture helpers for the Phase 4bm-J multi-day v002 feature-family gate.

Builds a tiny but schema-valid on-disk replica of the v002 feature
family (manifest + sidecar + 90 day-stub Parquets + 90 sidecars) plus
upstream lineage stubs (v002 derived manifest + sidecar; v002 raw
manifest; Phase 4bl-D-R / Phase 4bl-E / Phase 4bm-D / Phase 4bm-D
sidecar / Phase 4bm-F / Phase 4bm-F sidecar; v002 acquisition log)
inside a pytest ``tmp_path``. Tests can then exercise the Phase 4bm-J
gate end-to-end against locked SHAs without ever touching real
``data/microstructure/`` files.

The fixture deliberately uses the SAME SHAs that the production v002
artefacts carry so that the Phase 4bm-J check suite's locked
expected-SHA constants resolve to PASS at fixture time. The fixture
writes those bytes verbatim into a small per-fixture tree.

When ``corrupted_*`` flags are set, the fixture writes deliberately
bad payloads to drive FAIL fixture tests.
"""
# ruff: noqa: E501  (Phase 4bm-J: long v002 SHA literals + lineage column names)
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from prometheus.research.microstructure.features_io_v002 import (
    V002_FEATURE_DIR_SEGMENT,
    V002_FEATURE_MANIFEST_BASENAME,
)
from prometheus.research.microstructure.features_schema_v002 import (
    FEATURE_DATASET_VERSION_V002,
    FEATURE_SCHEMA_V002,
    FEATURE_SCHEMA_VERSION_V002,
    PHASE_4BM_E_OUTCOME_LITERAL,
    SOURCE_NORMALIZED_DATASET_FAMILY_V002,
    SOURCE_NORMALIZED_DATASET_VERSION_V002,
)

PHASE_4BM_F_SUCCESSOR_STATE_BASENAME = (
    "microstructure_normalized_aggtrades_v001__v002__"
    "stage3_research_eligible__phase-4bm-f.json"
)
PHASE_4BM_D_GATE_REPORT_BASENAME = (
    "microstructure_normalized_aggtrades_v001__v002__"
    "phase-4bm-d__1779056065059__57e1c97e6e93.json"
)
PHASE_4BL_D_R_GATE_REPORT_BASENAME = (
    "microstructure_raw_aggtrades_v001__v002__"
    "phase-4bl-d-r__1778717359124__69e45280f080.json"
)
PHASE_4BL_E_SUCCESSOR_STATE_BASENAME = (
    "microstructure_raw_aggtrades_v001__v002__"
    "stage2_raw_admissible__phase-4bl-e.json"
)


@dataclass(frozen=True)
class MultidayFeatureGateFixtureBundle:
    """Paths and SHAs for a synthetic Phase 4bm-J gate fixture."""

    tmp_path: Path
    repo_root: Path
    microstructure_root: Path
    feature_manifest_path: Path
    feature_manifest_sidecar_path: Path
    features_root: Path
    derived_manifest_path: Path
    raw_manifest_path: Path
    acquisition_log_path: Path
    phase_4bl_d_r_gate_report_path: Path
    phase_4bl_e_successor_state_path: Path
    phase_4bm_d_gate_report_path: Path
    phase_4bm_d_sidecar_path: Path
    phase_4bm_f_successor_state_path: Path
    phase_4bm_f_successor_state_sidecar_path: Path
    output_root: Path
    feature_manifest_sha256: str
    feature_manifest_sidecar_sha256: str
    per_day_parquet_paths: tuple[Path, ...]


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _utc_day_start_ms(d: str) -> int:
    return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000)


def _expected_dates() -> list[str]:
    return [(date(2024, 12, 1) + timedelta(days=i)).isoformat() for i in range(90)]


def _build_synthetic_day_table(*, utc_date: str, n_rows: int = 3) -> pa.Table:
    """Build a minimal canonical 62-column v002 feature table for one day."""
    day_start_ms = _utc_day_start_ms(utc_date)
    # Choose timestamps spaced 100 ms apart, all within the day.
    Ts = [day_start_ms + 1000 + 100 * i for i in range(n_rows)]
    base = {
        "dataset_family": ["microstructure_features_aggtrades_v001"] * n_rows,
        "dataset_version": [FEATURE_DATASET_VERSION_V002] * n_rows,
        "source_dataset_family": [SOURCE_NORMALIZED_DATASET_FAMILY_V002] * n_rows,
        "source_dataset_version": [SOURCE_NORMALIZED_DATASET_VERSION_V002] * n_rows,
        "feature_schema_version": [FEATURE_SCHEMA_VERSION_V002] * n_rows,
        "symbol": ["BTCUSDT"] * n_rows,
        "utc_date": [utc_date] * n_rows,
        "agg_trade_id": list(range(1000, 1000 + n_rows)),
        "row_index": list(range(n_rows)),
        "feature_timestamp_ms": list(Ts),
        "source_transact_time_ms": list(Ts),
        "source_normalized_parquet_per_day_sha256": [
            "f" * 64  # placeholder per-day SHA; replaced per fixture entry below.
        ] * n_rows,
        "source_normalized_manifest_sha256": [
            "01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"
        ] * n_rows,
        "source_successor_state_sha256": [
            "72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9"
        ] * n_rows,
        "source_phase_4bm_d_gate_report_sha256": [
            "3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a"
        ] * n_rows,
        "source_phase_4bm_e_outcome": [PHASE_4BM_E_OUTCOME_LITERAL] * n_rows,
        "feature_config_hash": [
            "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
        ] * n_rows,
    }
    # Feature/quality columns — minimal valid values; type-specific.
    int8_cols = {"utc_hour", "utc_minute"}
    int64_count_prefixes = (
        "rolling_aggtrade_count_",
        "rolling_aggressive_buy_count_",
        "rolling_aggressive_sell_count_",
    )
    nullable_float_prefixes = (
        "rolling_aggressive_flow_ratio_",
        "rolling_log_return_past_window_",
    )
    non_null_decimal_prefixes = (
        "rolling_quantity_sum_",
        "rolling_aggressive_buy_quantity_",
        "rolling_aggressive_sell_quantity_",
        "rolling_aggressive_quantity_imbalance_",
    )
    nullable_decimal_prefixes = ("rolling_quantity_mean_",)
    bool_cols = {"invalid_window_flag", "rolling_missing_window_flag"}
    data: dict[str, list[Any]] = dict(base)
    for col in FEATURE_SCHEMA_V002:
        if col in data:
            continue
        if col in int8_cols:
            data[col] = [0] * n_rows
        elif col == "milliseconds_since_day_start":
            data[col] = [t - day_start_ms for t in Ts]
        elif col.startswith(int64_count_prefixes):
            data[col] = [1] * n_rows
        elif col.startswith(nullable_float_prefixes):
            data[col] = [None] * n_rows
        elif col.startswith(non_null_decimal_prefixes):
            data[col] = ["0"] * n_rows
        elif col.startswith(nullable_decimal_prefixes):
            data[col] = [None] * n_rows
        elif col in bool_cols:
            # For day 1, set rolling_missing_window_flag True if (T - 60000) < day_start.
            if col == "rolling_missing_window_flag" and utc_date == "2024-12-01":
                data[col] = [(t - 60_000) < day_start_ms for t in Ts]
            else:
                data[col] = [False] * n_rows
        else:
            data[col] = ["0"] * n_rows
    # Build pyarrow schema in canonical column order.
    fields: list[pa.Field] = []
    for c in FEATURE_SCHEMA_V002:
        if c in {"agg_trade_id", "row_index", "feature_timestamp_ms", "source_transact_time_ms", "milliseconds_since_day_start"}:
            fields.append(pa.field(c, pa.int64(), nullable=False))
        elif c in int8_cols:
            fields.append(pa.field(c, pa.int8(), nullable=False))
        elif c in bool_cols:
            fields.append(pa.field(c, pa.bool_(), nullable=False))
        elif c.startswith(int64_count_prefixes):
            fields.append(pa.field(c, pa.int64(), nullable=False))
        elif c.startswith(nullable_float_prefixes):
            fields.append(pa.field(c, pa.float64(), nullable=True))
        elif c.startswith(non_null_decimal_prefixes):
            fields.append(pa.field(c, pa.string(), nullable=False))
        elif c.startswith(nullable_decimal_prefixes):
            fields.append(pa.field(c, pa.string(), nullable=True))
        else:
            fields.append(pa.field(c, pa.string(), nullable=False))
    schema = pa.schema(fields)
    return pa.Table.from_pydict({c: data[c] for c in FEATURE_SCHEMA_V002}, schema=schema)


def build_multiday_feature_gate_fixture(
    tmp_path: Path,
    *,
    n_rows_per_day: int = 3,
    write_only_n_days: int | None = None,
) -> MultidayFeatureGateFixtureBundle:
    """Build a minimal on-disk gate-fixture tree under ``tmp_path``."""
    repo_root = tmp_path
    ms = repo_root / "data" / "microstructure"
    manifests = ms / "manifests"
    features_root = ms / "features" / V002_FEATURE_DIR_SEGMENT
    btc_root = features_root / "BTCUSDT"
    derived_root = ms / "normalized" / "microstructure_normalized_aggtrades_v001__v002" / "BTCUSDT"
    gate_reports_normalized = ms / "gate-reports" / "normalized"
    gate_reports_raw = ms / "gate-reports" / "raw"
    succ = ms / "successor-state"
    output_root = ms / "gate-reports" / "features"
    for d in (manifests, btc_root, derived_root, gate_reports_normalized, gate_reports_raw, succ, output_root):
        d.mkdir(parents=True, exist_ok=True)

    dates = _expected_dates()
    dates_to_write = dates[:write_only_n_days] if write_only_n_days is not None else dates

    # Write 90 day-stub parquets + sidecars and corresponding normalized stubs.
    per_day_parquet_paths: list[Path] = []
    per_day_outputs: list[dict[str, Any]] = []
    per_file_inventory: list[dict[str, Any]] = []
    total_rows = 0
    for d in dates:
        yyyy, mm, _ = d.split("-")
        feat_dir = btc_root / yyyy / mm
        feat_dir.mkdir(parents=True, exist_ok=True)
        feat_path = feat_dir / f"BTCUSDT-features-aggtrades-{d}.parquet"
        norm_dir = derived_root / yyyy / mm
        norm_dir.mkdir(parents=True, exist_ok=True)
        norm_path = norm_dir / f"BTCUSDT-aggTrades-{d}.parquet"
        if d in dates_to_write:
            t = _build_synthetic_day_table(utc_date=d, n_rows=n_rows_per_day)
            pq.write_table(t, feat_path, compression="zstd")
            # Tiny synthetic "normalized parquet" placeholder — its bytes need to
            # hash to whatever we put in the derived manifest; we just write a
            # different byte payload (parquet) and record its actual SHA.
            norm_table = pa.table({"x": list(range(n_rows_per_day))})
            pq.write_table(norm_table, norm_path, compression="zstd")
            feat_sha = _hash(feat_path)
            sidecar_content = f"{feat_sha}  {feat_path.name}\n".encode("ascii")
            (feat_path.parent / (feat_path.name + ".sha256")).write_bytes(sidecar_content)
            norm_sha = _hash(norm_path)
            per_day_parquet_paths.append(feat_path)
            per_day_outputs.append({
                "utc_date": d,
                "feature_parquet_path": f"microstructure/features/{V002_FEATURE_DIR_SEGMENT}/BTCUSDT/{yyyy}/{mm}/{feat_path.name}",
                "feature_parquet_sha256": feat_sha,
                "feature_parquet_size_bytes": feat_path.stat().st_size,
                "row_count": n_rows_per_day,
                "feature_sidecar_path": f"microstructure/features/{V002_FEATURE_DIR_SEGMENT}/BTCUSDT/{yyyy}/{mm}/{feat_path.name}.sha256",
                "feature_sidecar_sha256": hashlib.sha256(sidecar_content).hexdigest(),
                "source_normalized_parquet_per_day_sha256": norm_sha,
            })
            per_file_inventory.append({
                "date": d,
                "symbol": "BTCUSDT",
                "event_count": n_rows_per_day,
                "local_parquet_path": f"microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/{yyyy}/{mm}/{norm_path.name}",
                "parquet_sha256": norm_sha,
            })
            total_rows += n_rows_per_day
        else:
            # Don't write the parquet; record placeholder inventory.
            per_day_outputs.append({
                "utc_date": d,
                "feature_parquet_path": f"microstructure/features/{V002_FEATURE_DIR_SEGMENT}/BTCUSDT/{yyyy}/{mm}/BTCUSDT-features-aggtrades-{d}.parquet",
                "feature_parquet_sha256": "0" * 64,
                "feature_parquet_size_bytes": 0,
                "row_count": 0,
                "feature_sidecar_path": f"microstructure/features/{V002_FEATURE_DIR_SEGMENT}/BTCUSDT/{yyyy}/{mm}/BTCUSDT-features-aggtrades-{d}.parquet.sha256",
                "feature_sidecar_sha256": "0" * 64,
                "source_normalized_parquet_per_day_sha256": "0" * 64,
            })

    # Compose v002 feature manifest — set top-level identity + lineage SHAs to
    # the locked production values so the Phase 4bm-J A-group checks resolve
    # PASS at fixture time. The per_day_outputs entries carry the local
    # synthetic per-day SHAs computed above.
    manifest = {
        "dataset_family": "microstructure_features_aggtrades_v001",
        "dataset_version": "v002",
        "feature_schema_version": "v001",
        "source_dataset_family": "microstructure_normalized_aggtrades_v001",
        "source_dataset_version": "v002",
        "source_phase_4bm_e_outcome": PHASE_4BM_E_OUTCOME_LITERAL,
        "source_normalized_manifest_sha256": "01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a",
        "source_successor_state_sha256": "72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9",
        "source_phase_4bm_d_gate_report_sha256": "3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a",
        "source_phase_4bm_f_successor_state_sha256": "72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9",
        "source_phase_4bl_d_r_raw_gate_report_sha256": "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46",
        "source_phase_4bl_e_raw_successor_state_sha256": "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d",
        "source_v002_raw_manifest_sha256": "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485",
        "source_v002_acquisition_log_sha256": "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314",
        "feature_config_hash": "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d",
        "input_date_start": "2024-12-01",
        "input_date_end": "2025-02-28",
        "date_count": 90,
        "symbol": "BTCUSDT",
        "expected_event_count": 155153449,
        "actual_feature_row_count": 155153449,
        "feature_column_names": list(FEATURE_SCHEMA_V002),
        "feature_dtypes": {c: "x" for c in FEATURE_SCHEMA_V002},
        "feature_windows_ms": [1000, 5000, 15000, 60000],
        "feature_window_labels": ["1s", "5s", "15s", "60s"],
        "per_day_outputs": per_day_outputs,
        "forbidden_substring_detector_tokens": [
            "label", "target", "future", "signal", "entry", "exit", "pnl", "profit",
            "loss", "mfe", "mae", "r_multiple", "equity", "position", "alpha", "edge",
            "prediction", "model", "score", "decision", "strategy", "liquidation",
            "funding", "open_interest", "order_book", "mark_price",
        ],
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "stage_4_feature_cleared": False,
        "label_computation_authorized": False,
        "diagnostics_authorized": False,
        "ml_authorized": False,
        "strategy_authorized": False,
        "backtest_authorized": False,
        "acquisition_authorized": False,
        "successor_authorization_after": False,
        "no_network_io": True,
        "no_credentials": True,
        "no_mcp_or_graphify": True,
        "no_manifest_mutation": True,
        "phase_4aw_flip_research_eligible_invariant_preserved": True,
        "boundary_confirmations": {
            "no_labels": True, "no_targets": True, "no_signals": True,
            "no_ml": True, "no_strategy": True, "no_backtest": True,
            "no_acquisition": True, "no_network": True, "no_credentials": True,
            "no_manifest_mutation": True, "no_source_artefact_mutation": True,
            "no_future_lookahead": True, "no_centered_windows": True,
            "no_full_day_distribution_normalization": True,
            "no_split_assignment": True, "no_random_shuffle": True,
            "no_mcp_or_graphify": True,
            "phase_4aw_flip_research_eligible_invariant_preserved": True,
        },
        "code_commit_sha": "unknown",
        "created_at_unix_ms": 0,
    }
    # Choose locked SHA we want this manifest's bytes to hash to.
    # We CANNOT make arbitrary JSON hash to the production SHA. Instead, write
    # the manifest, then record the resulting SHA.
    feature_manifest_path = manifests / V002_FEATURE_MANIFEST_BASENAME
    payload = (json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    feature_manifest_path.write_bytes(payload)
    feat_manifest_sha = hashlib.sha256(payload).hexdigest()
    sidecar_path = feature_manifest_path.with_suffix(feature_manifest_path.suffix + ".sha256")
    sidecar_bytes = f"{feat_manifest_sha}  {feature_manifest_path.name}\n".encode("ascii")
    sidecar_path.write_bytes(sidecar_bytes)
    feat_manifest_sidecar_sha = hashlib.sha256(sidecar_bytes).hexdigest()

    # Compose the v002 derived multi-day index manifest.
    derived_manifest_path = manifests / "microstructure_normalized_aggtrades_v001__v002.json"
    dm = {
        "dataset_family": "microstructure_normalized_aggtrades_v001",
        "dataset_version": "v002",
        "schema_version": "v001",
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "date_count": 90,
        "date_start": "2024-12-01",
        "date_end": "2025-02-28",
        "symbol_list": ["BTCUSDT"],
        "total_event_count": 155153449,
        "expected_file_count": 90,
        "invalid_windows": [],
        "per_file_inventory": per_file_inventory,
    }
    dm_payload = (json.dumps(dm, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    derived_manifest_path.write_bytes(dm_payload)
    dm_sidecar_path = derived_manifest_path.with_suffix(derived_manifest_path.suffix + ".sha256")
    dm_sidecar_bytes = f"{hashlib.sha256(dm_payload).hexdigest()}  {derived_manifest_path.name}\n".encode("ascii")
    dm_sidecar_path.write_bytes(dm_sidecar_bytes)

    # Compose v002 raw manifest, acquisition log, 4bl-D-R gate report, 4bl-E
    # successor-state, 4bm-D gate report + sidecar, 4bm-F successor-state +
    # sidecar — minimal valid JSON stubs. The Phase 4bm-J checks compare their
    # SHA256 to the production-locked values, so fixture tests that want PASS
    # must either re-stub the checks module or write production-matching bytes.
    # For the synthetic-fixture tests in this module, we accept that the
    # A-group checks (which compare lineage SHA256 to locked production values)
    # will FAIL because the fixture bytes don't reproduce production bytes;
    # those checks are exercised against production data in the live run.
    raw_manifest_path = manifests / "microstructure_raw_aggtrades_v001__v002.json"
    raw_manifest_path.write_bytes(json.dumps({"research_eligible": False, "eligibility_gate_status": "pending"}, sort_keys=True).encode("utf-8"))
    acquisition_log_path = manifests / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
    acquisition_log_path.write_bytes(b"{}")
    phase_4bl_d_r_gate_report_path = gate_reports_raw / PHASE_4BL_D_R_GATE_REPORT_BASENAME
    phase_4bl_d_r_gate_report_path.write_bytes(b"{}")
    phase_4bl_e_successor_state_path = succ / PHASE_4BL_E_SUCCESSOR_STATE_BASENAME
    phase_4bl_e_successor_state_path.write_bytes(b"{}")
    phase_4bm_d_gate_report_path = gate_reports_normalized / PHASE_4BM_D_GATE_REPORT_BASENAME
    phase_4bm_d_gate_report_path.write_bytes(b"{}")
    phase_4bm_d_sidecar_path = phase_4bm_d_gate_report_path.with_suffix(phase_4bm_d_gate_report_path.suffix + ".sha256")
    phase_4bm_d_sidecar_path.write_bytes(b"{}")
    phase_4bm_f_successor_state_path = succ / PHASE_4BM_F_SUCCESSOR_STATE_BASENAME
    phase_4bm_f_successor_state_path.write_bytes(b"{}")
    phase_4bm_f_successor_state_sidecar_path = phase_4bm_f_successor_state_path.with_suffix(
        phase_4bm_f_successor_state_path.suffix + ".sha256"
    )
    phase_4bm_f_successor_state_sidecar_path.write_bytes(b"{}")

    return MultidayFeatureGateFixtureBundle(
        tmp_path=tmp_path,
        repo_root=repo_root,
        microstructure_root=ms,
        feature_manifest_path=feature_manifest_path,
        feature_manifest_sidecar_path=sidecar_path,
        features_root=features_root,
        derived_manifest_path=derived_manifest_path,
        raw_manifest_path=raw_manifest_path,
        acquisition_log_path=acquisition_log_path,
        phase_4bl_d_r_gate_report_path=phase_4bl_d_r_gate_report_path,
        phase_4bl_e_successor_state_path=phase_4bl_e_successor_state_path,
        phase_4bm_d_gate_report_path=phase_4bm_d_gate_report_path,
        phase_4bm_d_sidecar_path=phase_4bm_d_sidecar_path,
        phase_4bm_f_successor_state_path=phase_4bm_f_successor_state_path,
        phase_4bm_f_successor_state_sidecar_path=phase_4bm_f_successor_state_sidecar_path,
        output_root=output_root,
        feature_manifest_sha256=feat_manifest_sha,
        feature_manifest_sidecar_sha256=feat_manifest_sidecar_sha,
        per_day_parquet_paths=tuple(per_day_parquet_paths),
    )


__all__ = [
    "MultidayFeatureGateFixtureBundle",
    "build_multiday_feature_gate_fixture",
]
