"""Phase 4bn-AZ — CF-1 realized-volatility substrate-test execution (orchestration only).

Single evidence-bearing runner for the frozen Phase 4bn-AY CF-1 contract. This script
owns **orchestration only** — every scientific primitive lives in
``prometheus.research.microstructure.cf1_realized_volatility_v001`` (RV kernel, validity,
boundary proof), ``…cf1_evaluation_v001`` (walk-forward OLS, QLIKE, bootstrap, verdict),
and ``…cf1_artifacts_v001`` (deterministic JSON / Parquet / sidecars / provenance).

Two-boundary workflow:

- **Preflight (no market data):** storage floor (D: >= 500 GiB), the deterministic
  synthetic timestamp-boundary proof, and existence of every openable-date source
  Parquet. Any failure is a ``PREFLIGHT_FAILURE`` — no market data is opened.
- **Evidence read (after the implementation commit is pushed):** write the synthetic
  proof artefact and the immutable access-start record, then open only the allowlisted
  2024-03-01..2024-10-31 (excluding 2024-10-01) normalized + feature partitions, build
  the compact RV target layer, validate the leakage/split/coverage proof, fit + score
  both models, run the one bootstrap, assign one verdict, and write all artefacts.

Source scope (read-only, integrity-verified against committed ``.sha256`` sidecars):

- prices / RV: ``microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o``;
- feature snapshots: ``microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s``.

No network, no credentials, no acquisition, no reserve read. November 2024 onward, the
consumed holdout, the v002 terminal window, and the v002 sealed test are never opened.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import pyarrow.parquet as pq

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from prometheus.research.microstructure import cf1_artifacts_v001 as art  # noqa: E402
from prometheus.research.microstructure import cf1_evaluation_v001 as ev  # noqa: E402
from prometheus.research.microstructure import cf1_realized_volatility_v001 as cf1  # noqa: E402

# On-disk source families (pre-v002 segment; gitignored).
NORMALIZED_FAMILY_DIR = "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o"
FEATURES_FAMILY_DIR = "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s"
NORMALIZED_ROOT = REPO_ROOT / "data" / "microstructure" / "normalized" / NORMALIZED_FAMILY_DIR
FEATURES_ROOT = REPO_ROOT / "data" / "microstructure" / "features" / FEATURES_FAMILY_DIR

D_DRIVE_MIN_FREE_GIB = 500
GIB = 1024**3

COMMAND = "uv run python scripts/phase4bn_az_cf1_realized_volatility_execution.py --run"

# Result-state strings (frozen; contract section 19).
STATE_PREFLIGHT = (
    "CF1_EXECUTION_PREFLIGHT_FAILURE__NO_MARKET_DATA_OPENED__NO_SCIENTIFIC_RESULT__"
    "SEPARATE_REAUTHORIZATION_REQUIRED"
)
STATE_INVALID = (
    "CF1_INVALID_RUN__NO_SCIENTIFIC_CLAIM__NO_RERUN_AUTHORIZED__"
    "SEPARATE_CORRECTIVE_PHASE_REQUIRED__RESERVES_UNTOUCHED"
)
STATE_VALID_FAIL = (
    "CF1_VALID_FAIL__PREREGISTERED_MAGNITUDE_LANE_MATERIALLY_NARROWED__"
    "NO_NEIGHBORING_RESCUE_VARIANT_AUTHORIZED__RESERVES_UNTOUCHED"
)
STATE_VALID_PASS = (
    "CF1_VALID_PASS__DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_"
    "SUPPORTED__DOCS_ONLY_FILTER_ASSESSMENT_ONLY__NO_DIRECTION_OR_PNL_AUTHORIZED__"
    "RESERVES_UNTOUCHED"
)


class Cf1ExecutionError(RuntimeError):
    """Raised on an orchestration precondition / integrity failure."""


class PreflightFailure(Cf1ExecutionError):
    """Raised when a pre-data gate fails (no market data opened)."""

    def __init__(self, gate: str, detail: str) -> None:
        super().__init__(f"{gate}: {detail}")
        self.gate = gate
        self.detail = detail


# ---------------------------------------------------------------------------
# Small orchestration helpers
# ---------------------------------------------------------------------------


def _git(args: list[str]) -> str:
    out = subprocess.run(
        ["git", *args], cwd=str(REPO_ROOT), capture_output=True, text=True, check=True
    )
    return out.stdout.strip()


def measure_d_free_gib() -> float:
    return shutil.disk_usage(REPO_ROOT).free / GIB


def _normalized_path(utc_date: str) -> Path:
    y, m, _d = utc_date.split("-")
    return NORMALIZED_ROOT / "BTCUSDT" / y / m / f"BTCUSDT-aggTrades-{utc_date}.parquet"


def _features_path(utc_date: str) -> Path:
    y, m, _d = utc_date.split("-")
    return FEATURES_ROOT / "BTCUSDT" / y / m / f"BTCUSDT-features-aggtrades-{utc_date}.parquet"


def _verify_sidecar(path: Path) -> str:
    """Verify a source Parquet against its committed ``.sha256`` sidecar; return the sha."""
    sidecar = path.with_suffix(path.suffix + ".sha256")
    if not path.is_file():
        raise Cf1ExecutionError(f"missing source parquet {path}")
    if not sidecar.is_file():
        raise Cf1ExecutionError(f"missing committed sidecar {sidecar}")
    digest = art.sha256_file(path)
    exp_sha, exp_name = art.parse_sidecar(sidecar.read_text(encoding="utf-8"))
    if exp_name != path.name or exp_sha != digest:
        raise Cf1ExecutionError(f"source integrity mismatch for {path.name}")
    return digest


def _segment_days(seg_start: str, seg_end: str) -> list[str]:
    days = [d for d in _date_range(seg_start, seg_end) if cf1.is_allowed_date(d)]
    # Fail closed if any forbidden date slipped into the plan.
    cf1.assert_partition_paths_allowed(days)
    return days


def _date_range(start: str, end: str) -> list[str]:
    from datetime import date, timedelta

    d0 = date.fromisoformat(start)
    d1 = date.fromisoformat(end)
    out: list[str] = []
    cur = d0
    while cur <= d1:
        out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


def _load_normalized_day(utc_date: str) -> tuple[npt.NDArray[np.int64], list[str], str]:
    cf1.assert_partition_allowed(utc_date)
    path = _normalized_path(utc_date)
    sha = _verify_sidecar(path)
    table = pq.read_table(path, columns=["transact_time_ms", "price", "row_index"])
    ts = table.column("transact_time_ms").to_numpy(zero_copy_only=False).astype(np.int64)
    ridx = table.column("row_index").to_numpy(zero_copy_only=False).astype(np.int64)
    px = table.column("price").to_pylist()
    if ts.shape[0] > 1 and not bool(np.all(ts[:-1] <= ts[1:])):
        order = np.lexsort((ridx, ts))
        ts = ts[order]
        px = np.array(px, dtype=object)[order].tolist()
    return ts, px, sha


def _load_feature_day(
    utc_date: str,
) -> tuple[
    npt.NDArray[np.int64],
    npt.NDArray[np.int64],
    list[str],
    list[str | None],
    npt.NDArray[np.int64],
    str,
]:
    cf1.assert_partition_allowed(utc_date)
    path = _features_path(utc_date)
    sha = _verify_sidecar(path)
    cols = [
        "feature_timestamp_ms",
        "row_index",
        "rolling_aggtrade_count_60s",
        "rolling_quantity_sum_60s",
        "rolling_quantity_mean_60s",
    ]
    table = pq.read_table(path, columns=cols)
    fts = table.column("feature_timestamp_ms").to_numpy(zero_copy_only=False).astype(np.int64)
    ridx = table.column("row_index").to_numpy(zero_copy_only=False).astype(np.int64)
    x1 = table.column("rolling_aggtrade_count_60s").to_numpy(zero_copy_only=False).astype(np.int64)
    x2 = table.column("rolling_quantity_sum_60s").to_pylist()
    x3 = table.column("rolling_quantity_mean_60s").to_pylist()
    if fts.shape[0] > 1 and not bool(np.all(fts[:-1] <= fts[1:])):
        order = np.lexsort((ridx, fts))
        fts, ridx, x1 = fts[order], ridx[order], x1[order]
        x2 = np.array(x2, dtype=object)[order].tolist()
        x3 = np.array(x3, dtype=object)[order].tolist()
    return fts, ridx, x2, x3, x1, sha  # noqa: E501 (order kept explicit below)


# ---------------------------------------------------------------------------
# Reader: build per-segment hourly RV series + feature snapshots
# ---------------------------------------------------------------------------


@dataclass
class FeatureSnapshot:
    x1: float
    x2: float
    x3: float
    snapshot_ts_ms: int
    snapshot_row_index: int
    valid: bool
    reason: str


@dataclass
class SegmentData:
    seg_id: str
    series: cf1.HourlySeries
    feature_snapshots: dict[int, FeatureSnapshot]
    normalized_shas: dict[str, str]
    feature_shas: dict[str, str]
    rows_read_normalized: int
    rows_read_features: int


def _feature_snapshot_from_row(
    fts: npt.NDArray[np.int64],
    ridx: npt.NDArray[np.int64],
    x1: npt.NDArray[np.int64],
    x2: list[str | None],
    x3: list[str | None],
    idx: int,
    seg_start_ms: int,
) -> FeatureSnapshot:
    mean_str = x3[idx]
    sum_str = x2[idx]
    snap_ts = int(fts[idx])
    if mean_str is None or sum_str is None:
        return FeatureSnapshot(0.0, 0.0, 0.0, snap_ts, int(ridx[idx]), False, "feature_null")
    # The upstream 60s window must not reach before the accessible segment start.
    if snap_ts - 60_000 < seg_start_ms:
        return FeatureSnapshot(
            0.0, 0.0, 0.0, snap_ts, int(ridx[idx]), False, "feature_window_crosses_inaccessible"
        )
    v1 = float(int(x1[idx]))
    v2 = float(Decimal(sum_str))
    v3 = float(Decimal(mean_str))
    if not (v1 > 0.0 and v2 > 0.0 and v3 > 0.0):
        return FeatureSnapshot(v1, v2, v3, snap_ts, int(ridx[idx]), False, "feature_non_positive")
    return FeatureSnapshot(v1, v2, v3, snap_ts, int(ridx[idx]), True, "")


def _build_segment(seg_id: str, seg_start: str, seg_end: str, *, progress: bool) -> SegmentData:
    grid = cf1.new_minute_grid(seg_id, seg_start, seg_end)
    days = _segment_days(seg_start, seg_end)
    normalized_shas: dict[str, str] = {}
    feature_shas: dict[str, str] = {}
    feature_snapshots: dict[int, FeatureSnapshot] = {}
    rows_norm = 0
    rows_feat = 0
    prev_last_ts: int | None = None
    prev_last_price: Decimal | None = None
    carry_row: (
        tuple[npt.NDArray[np.int64], npt.NDArray[np.int64], npt.NDArray[np.int64], list, list, int]
        | None
    ) = None

    for di, utc_date in enumerate(days):
        # --- prices / RV grid ---
        ts, px, nsha = _load_normalized_day(utc_date)
        normalized_shas[utc_date] = nsha
        rows_norm += int(ts.shape[0])
        day_start = cf1.utc_date_start_ms(utc_date)
        prev_last_ts, prev_last_price = cf1.fill_minute_grid_day(
            grid, day_start, ts, px, prev_last_ts, prev_last_price
        )
        del ts, px

        # --- feature snapshots for this day's hourly origins ---
        fts, fridx, x2, x3, x1, fsha = _load_feature_day(utc_date)
        feature_shas[utc_date] = fsha
        rows_feat += int(fts.shape[0])
        for hh in range(24):
            t = day_start + hh * cf1.HOUR_MS
            idx = cf1.p_at_index(fts, t)
            if idx >= 0:
                feature_snapshots[t] = _feature_snapshot_from_row(
                    fts, fridx, x1, x2, x3, idx, grid.seg_start_ms
                )
            elif carry_row is not None:
                cfts, cfridx, cx1, cx2, cx3, cidx = carry_row
                feature_snapshots[t] = _feature_snapshot_from_row(
                    cfts, cfridx, cx1, cx2, cx3, cidx, grid.seg_start_ms
                )
            else:
                feature_snapshots[t] = FeatureSnapshot(
                    0.0, 0.0, 0.0, 0, 0, False, "feature_unavailable"
                )
        if fts.shape[0] > 0:
            last = int(fts.shape[0] - 1)
            carry_row = (fts, fridx, x1, x2, x3, last)
        if progress and (di + 1) % 30 == 0:
            print(f"[read] segment {seg_id}: {di + 1}/{len(days)} days", flush=True)

    series = cf1.build_hourly_series(grid)
    return SegmentData(
        seg_id=seg_id,
        series=series,
        feature_snapshots=feature_snapshots,
        normalized_shas=normalized_shas,
        feature_shas=feature_shas,
        rows_read_normalized=rows_norm,
        rows_read_features=rows_feat,
    )


# ---------------------------------------------------------------------------
# Origin assembly
# ---------------------------------------------------------------------------


@dataclass
class AssembledOrigins:
    rows: list[ev.OriginRow]
    target_layer: list[dict[str, Any]]
    invalid_reason_counts: dict[str, int]
    valid_count: int
    zero_rv_count: int
    per_block_valid: dict[str, int]


def _assemble(segments: list[SegmentData]) -> AssembledOrigins:
    rows: list[ev.OriginRow] = []
    target_layer: list[dict[str, Any]] = []
    invalid_counts: dict[str, int] = {}
    per_block_valid: dict[str, int] = dict.fromkeys(cf1.BLOCK_IDS, 0)
    valid_count = 0
    zero_rv_count = 0

    for seg in segments:
        for origin_ms in cf1.candidate_origin_hours(seg.series):
            tgt = cf1.assemble_origin_target(seg.series, origin_ms)
            snap = seg.feature_snapshots.get(origin_ms)
            block_id = cf1.block_for_origin_ms(origin_ms) or ""
            reason = ""
            valid = False
            if not tgt.valid:
                reason = tgt.invalid_reason
            elif snap is None or not snap.valid:
                reason = snap.reason if snap is not None else "feature_unavailable"
            else:
                valid = True
            if valid and snap is not None:
                valid_count += 1
                if tgt.rv_target == 0.0:
                    zero_rv_count += 1
                if block_id:
                    per_block_valid[block_id] += 1
                rows.append(
                    ev.OriginRow(
                        origin_ms=origin_ms,
                        target_end_ms=tgt.target_end_ms,
                        block_id=block_id,
                        rv=tgt.rv_target,
                        log_rv=tgt.log_rv_target,
                        rv_h=tgt.rv_h,
                        rv_d=tgt.rv_d,
                        rv_w=tgt.rv_w,
                        x1=snap.x1,
                        x2=snap.x2,
                        x3=snap.x3,
                    )
                )
            else:
                invalid_counts[reason] = invalid_counts.get(reason, 0) + 1
            target_layer.append(
                {
                    "origin_timestamp_ms": origin_ms,
                    "origin_utc": cf1.utc_date_for_timestamp_ms(origin_ms)
                    + "T"
                    + f"{(origin_ms // cf1.HOUR_MS) % 24:02d}:00:00.000Z",
                    "origin_utc_date": cf1.utc_date_for_timestamp_ms(origin_ms),
                    "evaluation_block": block_id,
                    "target_end_timestamp_ms": tgt.target_end_ms,
                    "target_valid": bool(valid),
                    "target_invalid_reason": reason,
                    "covered_minute_count": int(tgt.covered_minutes),
                    "rv_target": float(tgt.rv_target) if valid else None,
                    "log_rv_target": float(tgt.log_rv_target) if valid else None,
                    "rv_h": float(tgt.rv_h) if valid else None,
                    "rv_d": float(tgt.rv_d) if valid else None,
                    "rv_w": float(tgt.rv_w) if valid else None,
                    "rolling_aggtrade_count_60s": (snap.x1 if (valid and snap) else None),
                    "rolling_quantity_sum_60s": (snap.x2 if (valid and snap) else None),
                    "rolling_quantity_mean_60s": (snap.x3 if (valid and snap) else None),
                    "feature_snapshot_timestamp_ms": (snap.snapshot_ts_ms if snap else None),
                    "feature_snapshot_row_index": (snap.snapshot_row_index if snap else None),
                    "source_segment": seg.seg_id,
                    "in_reserve": False,
                    "november_or_later_touched": False,
                }
            )
    return AssembledOrigins(
        rows=rows,
        target_layer=target_layer,
        invalid_reason_counts=invalid_counts,
        valid_count=valid_count,
        zero_rv_count=zero_rv_count,
        per_block_valid=per_block_valid,
    )


# ---------------------------------------------------------------------------
# Preflight (no market data)
# ---------------------------------------------------------------------------


def preflight(*, write_proof: bool, code_commit_sha: str) -> dict[str, Any]:
    """Run the pre-data gates. Raises :class:`PreflightFailure` on any gate failure."""
    d_free = measure_d_free_gib()
    if d_free < D_DRIVE_MIN_FREE_GIB:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__INSUFFICIENT_STORAGE",
            f"D: free {d_free:.1f} GiB < {D_DRIVE_MIN_FREE_GIB} GiB",
        )

    proof = cf1.run_synthetic_timestamp_boundary_proof()
    if proof.get("timestamp_boundary_proof_passed") is not True:
        raise PreflightFailure("PREFLIGHT_FAILURE__TIMESTAMP_BOUNDARY_PROOF", "proof failed")

    # Existence of every openable-date source parquet + its sidecar (no content read).
    missing: list[str] = []
    for utc_date in cf1.allowed_utc_dates():
        for p in (_normalized_path(utc_date), _features_path(utc_date)):
            if not p.is_file() or not p.with_suffix(p.suffix + ".sha256").is_file():
                missing.append(str(p))
    if missing:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__MISSING_SOURCE_PARTITION",
            f"{len(missing)} missing source files (first: {missing[0]})",
        )

    proof_path = None
    if write_proof:
        art.ensure_output_dirs(REPO_ROOT)
        prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
        payload = {**prov, **proof}
        unix_ms = int(prov["created_at_unix_ms"])
        name = art.compose_filename(
            family=art.FAMILY_TIMESTAMP_PROOF,
            context="v001",
            unix_ms=unix_ms,
            code_commit_sha=code_commit_sha,
            ext="json",
        )
        proof_path = art.output_root(REPO_ROOT) / "proofs" / name
        art.write_json_with_sidecar(proof_path, payload, REPO_ROOT)

    return {
        "d_free_gib": d_free,
        "timestamp_boundary_proof_passed": True,
        "source_files_present": True,
        "proof_path": str(proof_path) if proof_path else None,
    }


# ---------------------------------------------------------------------------
# Leakage / split / coverage proof
# ---------------------------------------------------------------------------


def _build_leakage_proof(
    assembled: AssembledOrigins, segments: list[SegmentData], *, code_commit_sha: str
) -> dict[str, Any]:
    opened_dates = sorted(
        {d for seg in segments for d in seg.normalized_shas}
        | {d for seg in segments for d in seg.feature_shas}
    )
    prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    proof = {
        **prov,
        "artifact_family": art.FAMILY_LEAKAGE_PROOF,
        "source_families": {
            "normalized": NORMALIZED_FAMILY_DIR,
            "features": FEATURES_FAMILY_DIR,
        },
        "partitions_opened_utc_dates": opened_dates,
        "partitions_opened_count": len(opened_dates),
        "october_1_opened": "2024-10-01" in opened_dates,
        "november_or_later_opened": any(d >= "2024-11-01" for d in opened_dates),
        "consumed_holdout_opened": any("2024-11-17" <= d <= "2024-11-30" for d in opened_dates),
        "terminal_opened": any(d >= "2024-12-01" for d in opened_dates),
        "sealed_opened": any("2025-02-14" <= d <= "2025-02-28" for d in opened_dates),
        "covered_minute_predicate": "tau_{k-1} < ts <= tau_k",
        "coverage_threshold": cf1.COVERAGE_MIN_COVERED_MINUTES,
        "feature_snapshot_rule": "feature_timestamp_ms <= t (greatest row_index tie)",
        "har_interval_rule": "(t - L, t]",
        "embargo_ms": cf1.EMBARGO_MS,
        "purge_ms": cf1.PURGE_MS,
        "per_block_valid_origins": assembled.per_block_valid,
        "valid_origin_count": assembled.valid_count,
        "invalid_reason_counts": assembled.invalid_reason_counts,
        "block_dates": {b[0]: [b[1], b[2]] for b in cf1.BLOCKS},
        "october_31_23_00_retained": False,
        "normalized_partition_shas": {
            d: seg.normalized_shas[d] for seg in segments for d in seg.normalized_shas
        },
        "feature_partition_shas": {
            d: seg.feature_shas[d] for seg in segments for d in seg.feature_shas
        },
    }
    return proof


def _validate_leakage_proof(proof: dict[str, Any]) -> tuple[bool, str]:
    if proof["october_1_opened"]:
        return False, "october_1_opened"
    if proof["november_or_later_opened"]:
        return False, "november_or_later_opened"
    if proof["consumed_holdout_opened"] or proof["terminal_opened"] or proof["sealed_opened"]:
        return False, "reserve_or_holdout_opened"
    if proof["partitions_opened_count"] != cf1.EXPECTED_ALLOWED_DATE_COUNT:
        return False, "partition_count_mismatch"
    if not art.validate_no_forbidden_dates_in_list(proof["partitions_opened_utc_dates"]):
        return False, "forbidden_date_in_partition_list"
    return True, ""


# ---------------------------------------------------------------------------
# Run (evidence-bearing)
# ---------------------------------------------------------------------------


def run(*, progress: bool = True) -> dict[str, Any]:
    """Execute the single CF-1 evidence-bearing run and write all artefacts."""
    t0 = time.monotonic()
    code_commit_sha = _git(["rev-parse", "HEAD"])
    out_root = art.ensure_output_dirs(REPO_ROOT)

    # One-run guard: refuse to overwrite an existing model-run manifest.
    existing = list((out_root / "manifests").glob(f"{art.FAMILY_MODEL_RUN_MANIFEST}__*.json"))
    if existing:
        raise Cf1ExecutionError(
            "CF-1 model-run manifest already exists; a rerun requires separate authorization"
        )

    # --- Preflight (no market data), writes the synthetic proof artefact ---
    pf = preflight(write_proof=True, code_commit_sha=code_commit_sha)
    if progress:
        print(f"[preflight] passed; D: free {pf['d_free_gib']:.1f} GiB", flush=True)

    # --- Access-start record (immediately before the first market-data read) ---
    prov0 = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    access_start = {
        **prov0,
        "artifact_family": art.FAMILY_ACCESS_START,
        "market_data_access_started": True,
        "allowed_date_list": list(cf1.allowed_utc_dates()),
        "forbidden_ranges": prov0["forbidden_utc_ranges"],
        "synthetic_proof_path": pf["proof_path"],
    }
    access_name = art.compose_filename(
        family=art.FAMILY_ACCESS_START,
        context="v001",
        unix_ms=int(prov0["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    access_path = out_root / "runs" / access_name
    art.write_json_with_sidecar(access_path, access_start, REPO_ROOT)
    if progress:
        print("[access-start] record written; opening market data", flush=True)

    # --- Bounded market-data read: build per-segment hourly RV + feature snapshots ---
    segments = [
        _build_segment(seg_id, lo, hi, progress=progress)
        for seg_id, lo, hi in cf1.ACCESSIBLE_SEGMENTS
    ]
    assembled = _assemble(segments)
    if progress:
        print(
            f"[assemble] valid origins={assembled.valid_count} "
            f"per_block={assembled.per_block_valid}",
            flush=True,
        )

    # --- Leakage / split / coverage proof (before any metric) ---
    leak = _build_leakage_proof(assembled, segments, code_commit_sha=code_commit_sha)
    ok, why = _validate_leakage_proof(leak)
    leak["leakage_split_coverage_proof_passed"] = ok
    leak["leakage_failure_reason"] = why
    leak_name = art.compose_filename(
        family=art.FAMILY_LEAKAGE_PROOF,
        context="v001",
        unix_ms=int(leak["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    leak_path = out_root / "proofs" / leak_name
    art.write_json_with_sidecar(leak_path, leak, REPO_ROOT)
    if not ok:
        return _finalize_invalid(
            out_root,
            code_commit_sha,
            assembled,
            segments,
            leak,
            reason=f"leakage_proof:{why}",
            elapsed=time.monotonic() - t0,
            progress=progress,
        )

    # --- Evaluation (one fit per block; QLIKE; one bootstrap; verdict) ---
    result = ev.evaluate(assembled.rows)
    if progress:
        print(f"[verdict] {result.verdict} delta_equal={result.delta_equal:.6e}", flush=True)

    # --- Write target layer + paired predictions + manifest + inventory ---
    entries: list[art.ArtifactEntry] = []
    entries.append(_register(out_root, leak_path))
    entries.append(_register(out_root, access_path))
    if pf["proof_path"]:
        entries.append(_register(out_root, Path(pf["proof_path"])))

    unix_ms = int(prov0["created_at_unix_ms"])
    target_tbl = art.target_layer_table(assembled.target_layer)
    target_path = (
        out_root
        / "targets"
        / art.compose_filename(
            family=art.FAMILY_TARGET_LAYER,
            context="v001",
            unix_ms=unix_ms,
            code_commit_sha=code_commit_sha,
            ext="parquet",
        )
    )
    art.write_parquet_with_sidecar(target_path, target_tbl, REPO_ROOT)
    entries.append(_register(out_root, target_path))

    pred_rows = _paired_prediction_rows(result)
    pred_path = (
        out_root
        / "runs"
        / art.compose_filename(
            family=art.FAMILY_PAIRED_PREDICTIONS,
            context="v001",
            unix_ms=unix_ms,
            code_commit_sha=code_commit_sha,
            ext="parquet",
        )
    )
    if pred_rows:
        art.write_parquet_with_sidecar(
            pred_path, art.paired_predictions_table(pred_rows), REPO_ROOT
        )
        entries.append(_register(out_root, pred_path))

    manifest = _build_manifest(
        code_commit_sha, assembled, segments, result, leak, elapsed=time.monotonic() - t0
    )
    man_path = (
        out_root
        / "manifests"
        / art.compose_filename(
            family=art.FAMILY_MODEL_RUN_MANIFEST,
            context="v001",
            unix_ms=unix_ms,
            code_commit_sha=code_commit_sha,
            ext="json",
        )
    )
    art.write_json_with_sidecar(man_path, manifest, REPO_ROOT)
    entries.append(_register(out_root, man_path))

    _write_inventory(out_root, code_commit_sha, entries)

    summary = {
        "verdict": result.verdict,
        "result_state": _state_for(result.verdict),
        "delta_equal": result.delta_equal,
        "rho": result.rho,
        "baseline_qlike_equal": result.baseline_qlike_equal,
        "augmented_qlike_equal": result.augmented_qlike_equal,
        "positive_block_count": result.positive_block_count,
        "lb95": result.lb95,
        "p1": result.p1,
        "p2": result.p2,
        "p3": result.p3,
        "p4": result.p4,
        "per_block_valid": assembled.per_block_valid,
        "code_commit_sha": code_commit_sha,
        "model_run_manifest": str(man_path),
        "elapsed_seconds": round(time.monotonic() - t0, 1),
    }
    if progress:
        print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return summary


def _state_for(verdict: str) -> str:
    return {
        ev.CF1_VALID_PASS: STATE_VALID_PASS,
        ev.CF1_VALID_FAIL: STATE_VALID_FAIL,
        ev.CF1_INVALID_RUN: STATE_INVALID,
    }[verdict]


def _register(out_root: Path, path: Path) -> art.ArtifactEntry:
    rel = str(path.relative_to(out_root)).replace("\\", "/")
    family = path.name.split("__", 1)[0]
    return art.ArtifactEntry(family, rel, art.sha256_file(path), rel + ".sha256")


def _paired_prediction_rows(result: ev.EvaluationResult) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for b in result.blocks:
        if not b.ok:
            continue
        for i, origin_ms in enumerate(b.eval_origin_ms):
            rows.append(
                {
                    "origin_timestamp_ms": int(origin_ms),
                    "evaluation_block": b.block_id,
                    "yhat_baseline": float(b.yhat_base[i]),
                    "yhat_augmented": float(b.yhat_aug[i]),
                    "qlike_baseline": float(b.qlike_base[i]),
                    "qlike_augmented": float(b.qlike_aug[i]),
                    "loss_differential": float(b.qlike_base[i] - b.qlike_aug[i]),
                }
            )
    return rows


def _finalize_invalid(
    out_root: Path,
    code_commit_sha: str,
    assembled: AssembledOrigins,
    segments: list[SegmentData],
    leak: dict[str, Any],
    *,
    reason: str,
    elapsed: float,
    progress: bool,
) -> dict[str, Any]:
    summary = {
        "verdict": ev.CF1_INVALID_RUN,
        "result_state": STATE_INVALID,
        "invalid_reason": reason,
        "per_block_valid": assembled.per_block_valid,
        "code_commit_sha": code_commit_sha,
        "elapsed_seconds": round(elapsed, 1),
    }
    if progress:
        print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return summary


def _build_manifest(
    code_commit_sha: str,
    assembled: AssembledOrigins,
    segments: list[SegmentData],
    result: ev.EvaluationResult,
    leak: dict[str, Any],
    *,
    elapsed: float,
) -> dict[str, Any]:
    prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    per_block = []
    for b in result.blocks:
        per_block.append(
            {
                "block_id": b.block_id,
                "n_train": b.n_train,
                "n_eval": b.n_eval,
                "baseline_qlike": b.baseline_qlike,
                "augmented_qlike": b.augmented_qlike,
                "d_i": b.d_i,
                "baseline_mse": b.baseline_mse,
                "augmented_mse": b.augmented_mse,
                "baseline_mz_r2": b.baseline_mz_r2,
                "augmented_mz_r2": b.augmented_mz_r2,
                "baseline_condition_number": b.baseline_condition_number,
                "augmented_condition_number": b.augmented_condition_number,
                "baseline_rank": b.baseline_rank,
                "augmented_rank": b.augmented_rank,
                "baseline_beta": b.baseline_beta,
                "augmented_beta": b.augmented_beta,
                "zero_rv_count": b.zero_rv_count,
                "ok": b.ok,
                "reason": b.reason,
            }
        )
    return {
        **prov,
        "artifact_family": art.FAMILY_MODEL_RUN_MANIFEST,
        "contract": {
            "interval": "(a, b]",
            "p_at_operator": "source_transact_time_ms <= u; greatest row_index tie",
            "horizon_ms": cf1.HORIZON_MS,
            "cadence": "top_of_utc_hour_non_overlapping",
            "coverage_predicate": "tau_{k-1} < ts <= tau_k",
            "coverage_threshold": cf1.COVERAGE_MIN_COVERED_MINUTES,
            "target_epsilon": cf1.TARGET_EPSILON,
            "standardization_epsilon": cf1.STANDARDIZATION_EPSILON,
            "features": list(cf1.FEATURE_COLUMNS),
            "har_lags_hours": [1, cf1.HAR_DAILY_HOURS, cf1.HAR_WEEKLY_HOURS],
            "estimator": "ols_lstsq_intercept",
            "condition_number_max": cf1.CONDITION_NUMBER_MAX,
            "min_train_origins": cf1.MIN_TRAIN_ORIGINS,
            "min_block_valid_origins": cf1.MIN_BLOCK_VALID_ORIGINS,
            "qlike": "v=RV+eps; h=max(exp(yhat),eps); ratio-ln(ratio)-1",
            "n_blocks": cf1.N_BLOCKS,
            "embargo_ms": cf1.EMBARGO_MS,
            "purge_ms": cf1.PURGE_MS,
            "bootstrap_method": "stratified_by_block_non_circular_moving_block",
            "bootstrap_seed": cf1.BOOTSTRAP_SEED,
            "bootstrap_replicates": cf1.BOOTSTRAP_REPLICATES,
            "bootstrap_quantile_method": "linear_0.05_lower",
        },
        "counts": {
            "source_partitions_opened": len(leak["partitions_opened_utc_dates"]),
            "rows_read_normalized": sum(s.rows_read_normalized for s in segments),
            "rows_read_features": sum(s.rows_read_features for s in segments),
            "valid_targets": assembled.valid_count,
            "invalid_targets_by_reason": assembled.invalid_reason_counts,
            "per_block_valid_origins": assembled.per_block_valid,
            "per_block_train_origins": {b.block_id: b.n_train for b in result.blocks},
            "zero_rv_origin_count": assembled.zero_rv_count,
            "bootstrap_block_lengths": result.bootstrap_block_lengths,
        },
        "per_block_metrics": per_block,
        "aggregate_metrics": {
            "baseline_qlike_equal_weighted": result.baseline_qlike_equal,
            "augmented_qlike_equal_weighted": result.augmented_qlike_equal,
            "delta_equal": result.delta_equal,
            "rho": result.rho,
            "positive_block_count": result.positive_block_count,
            "lb95": result.lb95,
            "baseline_mse_equal_weighted": float(np.mean([b.baseline_mse for b in result.blocks])),
            "augmented_mse_equal_weighted": float(
                np.mean([b.augmented_mse for b in result.blocks])
            ),
            "baseline_mz_r2_equal_weighted": float(
                np.mean([b.baseline_mz_r2 for b in result.blocks])
            ),
            "augmented_mz_r2_equal_weighted": float(
                np.mean([b.augmented_mz_r2 for b in result.blocks])
            ),
            "p1": result.p1,
            "p2": result.p2,
            "p3": result.p3,
            "p4": result.p4,
            "verdict": result.verdict,
            "result_state": _state_for(result.verdict),
        },
        "governance": {
            "no_november": True,
            "no_holdout": True,
            "no_terminal": True,
            "no_sealed": True,
            "no_network": True,
            "no_acquisition": True,
            "no_pnl": True,
            "no_direction": True,
        },
        "elapsed_seconds": round(elapsed, 1),
    }


def _write_inventory(
    out_root: Path, code_commit_sha: str, entries: list[art.ArtifactEntry]
) -> None:
    inv = art.build_inventory(code_commit_sha=code_commit_sha, command=COMMAND, entries=entries)
    unix_ms = int(inv["created_at_unix_ms"])
    inv_path = (
        out_root
        / "manifests"
        / art.compose_filename(
            family=art.FAMILY_ARTIFACT_INVENTORY,
            context="v001",
            unix_ms=unix_ms,
            code_commit_sha=code_commit_sha,
            ext="json",
        )
    )
    art.write_json_with_sidecar(inv_path, inv, REPO_ROOT)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 4bn-AZ CF-1 execution")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="preflight only; no market data")
    group.add_argument("--run", action="store_true", help="single evidence-bearing run")
    parser.add_argument("--no-progress", action="store_true")
    args = parser.parse_args(argv)
    progress = not args.no_progress
    try:
        if args.dry_run:
            code_sha = _git(["rev-parse", "HEAD"])
            pf = preflight(write_proof=False, code_commit_sha=code_sha)
            print(json.dumps({"mode": "dry_run", **pf}, indent=2, sort_keys=True))
            return 0
        run(progress=progress)
        return 0
    except PreflightFailure as exc:
        print(json.dumps({"result_state": STATE_PREFLIGHT, "gate": exc.gate, "detail": exc.detail}))
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
