"""Phase 4bn-BB — corrected CF-1 realized-volatility substrate-test execution (orchestration).

Single evidence-bearing runner for the merged Phase 4bn-BA corrected CF-1 contract. This script
owns **orchestration only** — every scientific primitive lives in
``prometheus.research.microstructure.cf1_corrected_contract_v002`` (corrected constants,
symbolic estimability proof), ``…cf1_corrected_evaluation_v002`` (two-feature walk-forward OLS,
QLIKE, bootstrap, verdict), ``…cf1_corrected_artifacts_v002`` (deterministic JSON / Parquet /
sidecars / provenance), and the inherited-unchanged target/timestamp primitives in
``…cf1_realized_volatility_v001`` (RV kernel, ``P_at``, allowlist, synthetic boundary proof).

Two-boundary workflow (Phase 4bn-BB §9):

- **Preflight (no market-data content):** repository/authorization state (main SHA, pushed,
  lineage commits); BB output root absent/empty; storage floor (D: >= 500 GiB); existence of
  every openable-date source Parquet + sidecar; the 244-date allowlist; the static symbolic
  estimability proof; the deterministic synthetic timestamp-boundary proof (inherited cases +
  corrected-feature cases). Any failure is a ``PREFLIGHT_FAILURE`` — no market data opened, no
  evidence consumed, no scientific result. ``--preflight`` writes no persistent artefact.
- **Evidence read (``--run``, once):** rerun the full preflight, then atomically write the
  symbolic estimability proof, the synthetic timestamp-boundary proof, and the immutable
  access-start record; then open **only** the allowlisted 2024-03-01..2024-10-31 (excluding
  2024-10-01) normalized + feature partitions, build the RV target layer and the **two**
  feature snapshots per origin, validate the leakage/split/coverage proof, fit + score both
  models, run the one bootstrap, assign one verdict, and write all artefacts.

Source scope (read-only, integrity-verified against committed ``.sha256`` sidecars):

- prices / RV: ``microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o``
  (columns ``transact_time_ms``, ``price``, ``row_index``);
- feature snapshots: ``microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s``
  (columns ``feature_timestamp_ms``, ``row_index``, ``rolling_aggtrade_count_60s``,
  ``rolling_quantity_sum_60s`` — the prohibited ``rolling_quantity_mean_60s`` is never read).

No network, no credentials, no acquisition, no reserve read, no access to the Phase 4bn-AZ v001
output root. November 2024 onward, the consumed holdout, the v002 terminal window, and the v002
sealed test are never opened.
"""

from __future__ import annotations

import argparse
import json
import math
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

from prometheus.research.microstructure import cf1_corrected_artifacts_v002 as art  # noqa: E402
from prometheus.research.microstructure import cf1_corrected_contract_v002 as cc  # noqa: E402
from prometheus.research.microstructure import cf1_corrected_evaluation_v002 as ev  # noqa: E402
from prometheus.research.microstructure import cf1_realized_volatility_v001 as cf1  # noqa: E402

# On-disk source families (pre-v002 segment; gitignored).
NORMALIZED_FAMILY_DIR = "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o"
FEATURES_FAMILY_DIR = "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s"
NORMALIZED_ROOT = REPO_ROOT / "data" / "microstructure" / "normalized" / NORMALIZED_FAMILY_DIR
FEATURES_ROOT = REPO_ROOT / "data" / "microstructure" / "features" / FEATURES_FAMILY_DIR

D_DRIVE_MIN_FREE_GIB = 500
GIB = 1024**3

COMMAND = "uv run python scripts/phase4bn_bb_cf1_corrected_realized_volatility_execution.py --run"


class Cf1CorrectedExecutionError(RuntimeError):
    """Raised on an orchestration precondition / integrity failure."""


class PreflightFailure(Cf1CorrectedExecutionError):
    """Raised when a pre-data gate fails (no market data opened, no evidence consumed)."""

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


def _git_ok(args: list[str]) -> tuple[bool, str]:
    out = subprocess.run(["git", *args], cwd=str(REPO_ROOT), capture_output=True, text=True)
    return out.returncode == 0, out.stdout.strip()


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
        raise Cf1CorrectedExecutionError(f"missing source parquet {path}")
    if not sidecar.is_file():
        raise Cf1CorrectedExecutionError(f"missing committed sidecar {sidecar}")
    digest = art.sha256_file(path)
    exp_sha, exp_name = art.parse_sidecar(sidecar.read_text(encoding="utf-8"))
    if exp_name != path.name or exp_sha != digest:
        raise Cf1CorrectedExecutionError(f"source integrity mismatch for {path.name}")
    return digest


def _segment_days(seg_start: str, seg_end: str) -> list[str]:
    days = [d for d in _date_range(seg_start, seg_end) if cf1.is_allowed_date(d)]
    cf1.assert_partition_paths_allowed(days)  # fail closed if any forbidden date slipped in
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


_FeatureDay = tuple[
    npt.NDArray[np.int64], npt.NDArray[np.int64], npt.NDArray[np.int64], list[str | None], str
]
_CarryRow = tuple[
    npt.NDArray[np.int64], npt.NDArray[np.int64], npt.NDArray[np.int64], list[str | None], int
]


def _load_feature_day(utc_date: str) -> _FeatureDay:
    """Load one feature day, requesting **only** the four corrected source columns.

    The prohibited ``rolling_quantity_mean_60s`` is never in the requested column list.
    Returns ``(feature_timestamp_ms, row_index, rolling_aggtrade_count_60s,
    rolling_quantity_sum_60s, sha)``.
    """
    cf1.assert_partition_allowed(utc_date)
    path = _features_path(utc_date)
    sha = _verify_sidecar(path)
    cols = list(cc.FEATURE_SOURCE_COLUMNS)
    assert cc.PROHIBITED_FEATURE_COLUMN not in cols  # defensive: never request the mean column
    table = pq.read_table(path, columns=cols)
    fts = table.column("feature_timestamp_ms").to_numpy(zero_copy_only=False).astype(np.int64)
    ridx = table.column("row_index").to_numpy(zero_copy_only=False).astype(np.int64)
    x1 = table.column("rolling_aggtrade_count_60s").to_numpy(zero_copy_only=False).astype(np.int64)
    x2 = table.column("rolling_quantity_sum_60s").to_pylist()
    if fts.shape[0] > 1 and not bool(np.all(fts[:-1] <= fts[1:])):
        order = np.lexsort((ridx, fts))
        fts, ridx, x1 = fts[order], ridx[order], x1[order]
        x2 = np.array(x2, dtype=object)[order].tolist()
    return fts, ridx, x1, x2, sha


# ---------------------------------------------------------------------------
# Feature snapshot validity (shared by the reader and the timestamp proof)
# ---------------------------------------------------------------------------


def feature_values_valid(x1: float, x2: float) -> tuple[bool, str]:
    """Corrected origin-validity predicate on the two retained feature values.

    Invalid if ``rolling_aggtrade_count_60s < 1``, or ``rolling_quantity_sum_60s <= 0``, or
    either value is non-finite. No mean column participates.
    """
    if not (math.isfinite(x1) and math.isfinite(x2)):
        return False, "feature_non_finite"
    if not (x1 >= 1.0):
        return False, "count_below_one"
    if not (x2 > 0.0):
        return False, "quantity_sum_non_positive"
    return True, ""


@dataclass
class FeatureSnapshot:
    x1: float
    x2: float
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
    idx: int,
    seg_start_ms: int,
) -> FeatureSnapshot:
    sum_str = x2[idx]
    snap_ts = int(fts[idx])
    if sum_str is None:
        return FeatureSnapshot(0.0, 0.0, snap_ts, int(ridx[idx]), False, "feature_null")
    # The upstream 60s window must not reach before the accessible segment start.
    if snap_ts - 60_000 < seg_start_ms:
        return FeatureSnapshot(
            0.0, 0.0, snap_ts, int(ridx[idx]), False, "feature_window_crosses_inaccessible"
        )
    v1 = float(int(x1[idx]))
    v2 = float(Decimal(sum_str))
    ok, reason = feature_values_valid(v1, v2)
    return FeatureSnapshot(v1, v2, snap_ts, int(ridx[idx]), ok, reason)


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
    carry_row: _CarryRow | None = None

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

        # --- feature snapshots for this day's hourly origins (two columns only) ---
        fts, fridx, x1, x2, fsha = _load_feature_day(utc_date)
        feature_shas[utc_date] = fsha
        rows_feat += int(fts.shape[0])
        for hh in range(24):
            t = day_start + hh * cf1.HOUR_MS
            idx = cf1.p_at_index(fts, t)
            if idx >= 0:
                feature_snapshots[t] = _feature_snapshot_from_row(
                    fts, fridx, x1, x2, idx, grid.seg_start_ms
                )
            elif carry_row is not None:
                cfts, cfridx, cx1, cx2, cidx = carry_row
                feature_snapshots[t] = _feature_snapshot_from_row(
                    cfts, cfridx, cx1, cx2, cidx, grid.seg_start_ms
                )
            else:
                feature_snapshots[t] = FeatureSnapshot(0.0, 0.0, 0, 0, False, "feature_unavailable")
        if fts.shape[0] > 0:
            carry_row = (fts, fridx, x1, x2, int(fts.shape[0] - 1))
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
    candidate_count: int
    valid_count: int
    invalid_count: int
    zero_rv_count: int
    per_block_valid: dict[str, int]


def _assemble(segments: list[SegmentData]) -> AssembledOrigins:
    rows: list[ev.OriginRow] = []
    target_layer: list[dict[str, Any]] = []
    invalid_counts: dict[str, int] = {}
    per_block_valid: dict[str, int] = dict.fromkeys(cf1.BLOCK_IDS, 0)
    candidate_count = 0
    valid_count = 0
    invalid_count = 0
    zero_rv_count = 0

    for seg in segments:
        for origin_ms in cf1.candidate_origin_hours(seg.series):
            candidate_count += 1
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
                    )
                )
            else:
                invalid_count += 1
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
        candidate_count=candidate_count,
        valid_count=valid_count,
        invalid_count=invalid_count,
        zero_rv_count=zero_rv_count,
        per_block_valid=per_block_valid,
    )


# ---------------------------------------------------------------------------
# Corrected deterministic synthetic timestamp-boundary proof (Phase 4bn-BB §14)
# ---------------------------------------------------------------------------


def build_corrected_timestamp_proof(code_commit_sha: str) -> dict[str, Any]:
    """Inherited timestamp cases + corrected-feature cases; a new BB artefact, no market data."""
    inherited = cf1.run_synthetic_timestamp_boundary_proof()
    checks: list[dict[str, Any]] = list(inherited["checks"])  # type: ignore[arg-type]

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    # Feature snapshot contains exactly count and quantity sum (no mean column requested).
    record(
        "feature_snapshot_exactly_count_and_quantity_sum",
        cc.CORRECTED_FEATURE_COLUMNS
        == ("rolling_aggtrade_count_60s", "rolling_quantity_sum_60s")
        and len(cc.CORRECTED_FEATURE_COLUMNS) == 2,
        f"features={list(cc.CORRECTED_FEATURE_COLUMNS)}",
    )
    record(
        "no_mean_column_in_requested_source_columns",
        cc.PROHIBITED_FEATURE_COLUMN not in cc.FEATURE_SOURCE_COLUMNS,
        f"requested={list(cc.FEATURE_SOURCE_COLUMNS)}",
    )
    # Invalid if count < 1.
    inv_count_ok, _r = feature_values_valid(0.0, 10.0)
    record("invalid_if_count_below_one", inv_count_ok is False, "count=0 -> invalid")
    # Invalid if quantity sum <= 0.
    inv_sum_ok, _r2 = feature_values_valid(3.0, 0.0)
    record("invalid_if_quantity_sum_non_positive", inv_sum_ok is False, "sum=0 -> invalid")
    # A valid positive snapshot passes.
    val_ok, _r3 = feature_values_valid(3.0, 12.5)
    record("valid_positive_snapshot_accepted", val_ok is True, "count=3,sum=12.5 -> valid")
    # No explicit mean or ratio feature is formed.
    record(
        "no_explicit_mean_or_ratio_feature_formed",
        len(cc.CORRECTED_FEATURE_COLUMNS) == 2
        and cc.PROHIBITED_FEATURE_COLUMN not in cc.CORRECTED_FEATURE_COLUMNS,
        "only ln(x1), ln(x2); no x2/x1 model feature",
    )

    passed = bool(inherited["timestamp_boundary_proof_passed"]) and all(
        bool(c["passed"]) for c in checks
    )
    return {
        "proof_family": art.FAMILY_TIMESTAMP_PROOF,
        "phase_id": cc.PHASE_ID,
        "symbol": cc.SYMBOL,
        "contract_version": cc.CONTRACT_VERSION,
        "code_commit_sha": code_commit_sha,
        "base_main_commit_sha": cc.BASE_MAIN_COMMIT_SHA,
        "phase_4bn_ba_merge_commit_sha": cc.PHASE_4BN_BA_MERGE_COMMIT_SHA,
        "inherited_proof_family": inherited["proof_family"],
        "market_data_opened": False,
        "feature_data_opened": False,
        "reserve_touched": False,
        "n_checks": len(checks),
        "checks": checks,
        "timestamp_boundary_proof_passed": passed,
    }


# ---------------------------------------------------------------------------
# Preflight (no market-data content)
# ---------------------------------------------------------------------------


def _output_root_evidence_files(repo_root: Path) -> list[Path]:
    root = art.output_root(repo_root)
    if not root.exists():
        return []
    return [p for p in root.rglob("*") if p.is_file()]


def _missing_source_files(allowed_dates: tuple[str, ...]) -> list[str]:
    """Return source Parquet / sidecar paths that do not exist (stat only; no content read)."""
    missing: list[str] = []
    for utc_date in allowed_dates:
        for p in (_normalized_path(utc_date), _features_path(utc_date)):
            if not p.is_file() or not p.with_suffix(p.suffix + ".sha256").is_file():
                missing.append(str(p))
    return missing


def _verify_repo_state(code_commit_sha: str) -> None:
    main_sha = _git(["rev-parse", "main"])
    if main_sha != cc.BASE_MAIN_COMMIT_SHA:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__BASE_MAIN_SHA",
            f"main {main_sha} != required {cc.BASE_MAIN_COMMIT_SHA}",
        )
    pushed, upstream = _git_ok(["rev-parse", "@{u}"])
    if not pushed:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__NOT_PUSHED", "no upstream configured (implementation not pushed)"
        )
    if upstream != code_commit_sha:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__NOT_PUSHED",
            f"HEAD {code_commit_sha} != origin {upstream} (implementation not pushed)",
        )
    for sha in (
        cc.PHASE_4BN_BA_MERGE_COMMIT_SHA,
        cc.PHASE_4BN_BA_CONTRACT_TIP_SHA,
        cc.PHASE_4BN_AY_CONTRACT_TIP_SHA,
        cc.PHASE_4BN_AZ_IMPLEMENTATION_SHA,
        cc.PHASE_4BN_AZ_MERGE_COMMIT_SHA,
    ):
        ok, kind = _git_ok(["cat-file", "-t", sha])
        if not ok or kind != "commit":
            raise PreflightFailure(
                "PREFLIGHT_FAILURE__MISSING_LINEAGE_COMMIT", f"{sha} not a commit"
            )


def preflight(*, code_commit_sha: str, verify_repo: bool = True) -> dict[str, Any]:
    """Run the pre-data gates. Raises :class:`PreflightFailure` on any gate failure.

    Opens no market-data content and writes no persistent artefact.
    """
    if verify_repo:
        _verify_repo_state(code_commit_sha)

    existing = _output_root_evidence_files(REPO_ROOT)
    if existing:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__OUTPUT_ROOT_NOT_EMPTY",
            f"{len(existing)} pre-existing BB artefact(s) (first: {existing[0]})",
        )

    d_free = measure_d_free_gib()
    if d_free < D_DRIVE_MIN_FREE_GIB:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__INSUFFICIENT_STORAGE",
            f"D: free {d_free:.1f} GiB < {D_DRIVE_MIN_FREE_GIB} GiB",
        )

    sym = cc.run_symbolic_estimability_proof(code_commit_sha)
    sym_ok, sym_why = cc.validate_symbolic_estimability_proof(sym)
    if not sym_ok:
        raise PreflightFailure("PREFLIGHT_FAILURE__SYMBOLIC_ESTIMABILITY_PROOF", sym_why)

    ts_proof = build_corrected_timestamp_proof(code_commit_sha)
    if ts_proof.get("timestamp_boundary_proof_passed") is not True:
        raise PreflightFailure("PREFLIGHT_FAILURE__TIMESTAMP_BOUNDARY_PROOF", "proof failed")

    allowed = cf1.allowed_utc_dates()
    if len(allowed) != cc.EXPECTED_ALLOWED_DATE_COUNT:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__ALLOWLIST_COUNT",
            f"{len(allowed)} != {cc.EXPECTED_ALLOWED_DATE_COUNT}",
        )
    if not art.validate_no_forbidden_dates_in_list(list(allowed)):
        raise PreflightFailure("PREFLIGHT_FAILURE__FORBIDDEN_DATE_IN_ALLOWLIST", "forbidden date")

    missing = _missing_source_files(allowed)
    if missing:
        raise PreflightFailure(
            "PREFLIGHT_FAILURE__MISSING_SOURCE_PARTITION",
            f"{len(missing)} missing source files (first: {missing[0]})",
        )

    return {
        "code_commit_sha": code_commit_sha,
        "base_main_commit_sha": cc.BASE_MAIN_COMMIT_SHA,
        "phase_4bn_ba_merge_commit_sha": cc.PHASE_4BN_BA_MERGE_COMMIT_SHA,
        "phase_4bn_ba_contract_tip_sha": cc.PHASE_4BN_BA_CONTRACT_TIP_SHA,
        "phase_4bn_ay_contract_tip_sha": cc.PHASE_4BN_AY_CONTRACT_TIP_SHA,
        "output_root_empty": True,
        "d_free_gib": d_free,
        "symbolic_estimability_proof_passed": True,
        "timestamp_boundary_proof_passed": True,
        "allowed_utc_date_count": len(allowed),
        "source_files_present": True,
        "network_used": False,
        "reserve_touched": False,
        "result_state": "PREFLIGHT_PASS",
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
    return {
        **prov,
        "artifact_family": art.FAMILY_LEAKAGE_PROOF,
        "source_families": {"normalized": NORMALIZED_FAMILY_DIR, "features": FEATURES_FAMILY_DIR},
        "feature_columns_read": list(cc.FEATURE_SOURCE_COLUMNS),
        "prohibited_feature_read": cc.PROHIBITED_FEATURE_COLUMN in cc.FEATURE_SOURCE_COLUMNS,
        "partitions_opened_utc_dates": opened_dates,
        "partitions_opened_count": len(opened_dates),
        "october_1_opened": "2024-10-01" in opened_dates,
        "november_or_later_opened": any(d >= "2024-11-01" for d in opened_dates),
        "consumed_holdout_opened": any("2024-11-17" <= d <= "2024-11-30" for d in opened_dates),
        "terminal_opened": any(d >= "2024-12-01" for d in opened_dates),
        "sealed_opened": any("2025-02-14" <= d <= "2025-02-28" for d in opened_dates),
        "az_output_root_read": False,
        "covered_minute_predicate": "tau_{k-1} < ts <= tau_k",
        "coverage_threshold": cf1.COVERAGE_MIN_COVERED_MINUTES,
        "feature_snapshot_rule": "feature_timestamp_ms <= t (greatest row_index tie)",
        "har_interval_rule": "(t - L, t]",
        "embargo_ms": cf1.EMBARGO_MS,
        "purge_ms": cf1.PURGE_MS,
        "per_block_valid_origins": assembled.per_block_valid,
        "candidate_origin_count": assembled.candidate_count,
        "valid_origin_count": assembled.valid_count,
        "invalid_origin_count": assembled.invalid_count,
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


def _validate_leakage_proof(proof: dict[str, Any]) -> tuple[bool, str]:
    if proof["prohibited_feature_read"]:
        return False, "prohibited_feature_read"
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
    """Execute the single corrected CF-1 evidence-bearing run and write all artefacts."""
    t0 = time.monotonic()
    code_commit_sha = _git(["rev-parse", "HEAD"])

    # --- Full preflight rerun (no market-data content, no persistent artefact) ---
    pf = preflight(code_commit_sha=code_commit_sha, verify_repo=True)
    if progress:
        print(f"[preflight] PREFLIGHT_PASS; D: free {pf['d_free_gib']:.1f} GiB", flush=True)

    out_root = art.ensure_output_dirs(REPO_ROOT)

    # --- Atomically write the two pre-data proofs + the access-start record ---
    sym = cc.run_symbolic_estimability_proof(code_commit_sha)
    sym_prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    sym_payload = {**sym_prov, **sym}
    sym_path = out_root / "proofs" / art.compose_filename(
        family=art.FAMILY_SYMBOLIC_PROOF,
        context=art.FILENAME_CONTEXT,
        unix_ms=int(sym_prov["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    art.write_json_with_sidecar(sym_path, sym_payload, REPO_ROOT)

    ts_proof = build_corrected_timestamp_proof(code_commit_sha)
    ts_prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    ts_payload = {**ts_prov, **ts_proof}
    ts_path = out_root / "proofs" / art.compose_filename(
        family=art.FAMILY_TIMESTAMP_PROOF,
        context=art.FILENAME_CONTEXT,
        unix_ms=int(ts_prov["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    art.write_json_with_sidecar(ts_path, ts_payload, REPO_ROOT)

    access_prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    access_start = {
        **access_prov,
        "artifact_family": art.FAMILY_ACCESS_START,
        "market_data_access_started": True,
        "evidence_bearing_run_consumed": True,
        "symbolic_proof_path": str(sym_path),
        "timestamp_proof_path": str(ts_path),
        "allowed_date_list": list(cf1.allowed_utc_dates()),
        "forbidden_ranges": access_prov["forbidden_utc_ranges"],
    }
    access_path = out_root / "runs" / art.compose_filename(
        family=art.FAMILY_ACCESS_START,
        context=art.FILENAME_CONTEXT,
        unix_ms=int(access_prov["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    art.write_json_with_sidecar(access_path, access_start, REPO_ROOT)
    if progress:
        print("[access-start] written; opening market data (BB run now consumed)", flush=True)

    base_entries = [
        _register(out_root, sym_path),
        _register(out_root, ts_path),
        _register(out_root, access_path),
    ]

    # --- Post-access section: any failure routes fail-closed to CF1_INVALID_RUN ---
    try:
        return _run_after_access(
            out_root, code_commit_sha, base_entries, t0=t0, progress=progress
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed post-access routing
        summary = _finalize_invalid_minimal(
            out_root, code_commit_sha, base_entries, reason=f"post_access_exception:{exc!r}", t0=t0
        )
        if progress:
            print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
        return summary


def _run_after_access(
    out_root: Path,
    code_commit_sha: str,
    base_entries: list[art.ArtifactEntry],
    *,
    t0: float,
    progress: bool,
) -> dict[str, Any]:
    # --- Bounded market-data read: per-segment hourly RV + two feature snapshots ---
    segments = [
        _build_segment(seg_id, lo, hi, progress=progress)
        for seg_id, lo, hi in cf1.ACCESSIBLE_SEGMENTS
    ]
    assembled = _assemble(segments)
    if progress:
        print(
            f"[assemble] candidates={assembled.candidate_count} valid={assembled.valid_count} "
            f"per_block={assembled.per_block_valid}",
            flush=True,
        )

    # --- Leakage / split / coverage proof (before any metric) ---
    leak = _build_leakage_proof(assembled, segments, code_commit_sha=code_commit_sha)
    ok, why = _validate_leakage_proof(leak)
    leak["leakage_split_coverage_proof_passed"] = ok
    leak["leakage_failure_reason"] = why
    leak_path = out_root / "proofs" / art.compose_filename(
        family=art.FAMILY_LEAKAGE_PROOF,
        context=art.FILENAME_CONTEXT,
        unix_ms=int(leak["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    art.write_json_with_sidecar(leak_path, leak, REPO_ROOT)
    entries = list(base_entries)
    entries.append(_register(out_root, leak_path))

    # --- Always write the target layer (regardless of verdict) ---
    unix_ms = int(art.now_provenance()["created_at_unix_ms"])
    target_tbl = art.target_layer_table(assembled.target_layer)
    target_path = out_root / "targets" / art.compose_filename(
        family=art.FAMILY_TARGET_LAYER,
        context=art.FILENAME_CONTEXT,
        unix_ms=unix_ms,
        code_commit_sha=code_commit_sha,
        ext="parquet",
    )
    art.write_parquet_with_sidecar(target_path, target_tbl, REPO_ROOT)
    entries.append(_register(out_root, target_path))

    if not ok:
        result = ev.EvaluationResult(
            verdict=ev.CF1_INVALID_RUN,
            invalid_reason=f"leakage_proof:{why}",
            blocks=[],
            delta_equal=0.0,
            rho=0.0,
            baseline_qlike_equal=0.0,
            augmented_qlike_equal=0.0,
            positive_block_count=0,
            lb95=0.0,
            bootstrap_block_lengths=[],
            valid=False,
            p1=False,
            p2=False,
            p3=False,
        )
        return _finalize(
            out_root, code_commit_sha, assembled, segments, leak, result, entries,
            t0=t0, progress=progress, scored=False,
        )

    # --- Evaluation (one fit per block; QLIKE; one bootstrap; verdict) ---
    result = ev.evaluate(assembled.rows)
    if progress:
        print(f"[verdict] {result.verdict} delta_equal={result.delta_equal:.6e}", flush=True)

    # --- Paired predictions only if at least one block produced valid forecasts ---
    pred_rows = _paired_prediction_rows(result)
    if pred_rows:
        pred_path = out_root / "runs" / art.compose_filename(
            family=art.FAMILY_PAIRED_PREDICTIONS,
            context=art.FILENAME_CONTEXT,
            unix_ms=unix_ms,
            code_commit_sha=code_commit_sha,
            ext="parquet",
        )
        art.write_parquet_with_sidecar(
            pred_path, art.paired_predictions_table(pred_rows), REPO_ROOT
        )
        entries.append(_register(out_root, pred_path))

    return _finalize(
        out_root, code_commit_sha, assembled, segments, leak, result, entries,
        t0=t0, progress=progress, scored=True,
    )


def _finalize(
    out_root: Path,
    code_commit_sha: str,
    assembled: AssembledOrigins,
    segments: list[SegmentData],
    leak: dict[str, Any],
    result: ev.EvaluationResult,
    entries: list[art.ArtifactEntry],
    *,
    t0: float,
    progress: bool,
    scored: bool,
) -> dict[str, Any]:
    # "computed" fields exist only for a valid (pass/fail) scored run; an invalid verdict
    # leaves the aggregate decision statistics not-computed (null), never 0.0 placeholders.
    computed = scored and result.verdict != ev.CF1_INVALID_RUN
    manifest = _build_manifest(
        code_commit_sha, assembled, segments, leak, result, elapsed=time.monotonic() - t0,
        scored=scored, computed=computed,
    )
    man_path = out_root / "manifests" / art.compose_filename(
        family=art.FAMILY_MODEL_RUN_MANIFEST,
        context=art.FILENAME_CONTEXT,
        unix_ms=int(manifest["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    art.write_json_with_sidecar(man_path, manifest, REPO_ROOT)
    entries.append(_register(out_root, man_path))

    _write_inventory(out_root, code_commit_sha, entries)

    summary = {
        "verdict": result.verdict,
        "result_state": cc.long_state_for_verdict(result.verdict),
        "invalid_reason": result.invalid_reason,
        "delta_equal": result.delta_equal if computed else None,
        "rho": result.rho if computed else None,
        "baseline_qlike_equal": result.baseline_qlike_equal if computed else None,
        "augmented_qlike_equal": result.augmented_qlike_equal if computed else None,
        "positive_block_count": result.positive_block_count if computed else None,
        "lb95": result.lb95 if computed else None,
        "p1": result.p1 if computed else None,
        "p2": result.p2 if computed else None,
        "p3": result.p3 if computed else None,
        "valid": result.valid,
        "candidate_origins": assembled.candidate_count,
        "valid_origins": assembled.valid_count,
        "per_block_valid": assembled.per_block_valid,
        "code_commit_sha": code_commit_sha,
        "model_run_manifest": str(man_path),
        "evidence_bearing_run_consumed": True,
        "elapsed_seconds": round(time.monotonic() - t0, 1),
    }
    if progress:
        print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return summary


def _finalize_invalid_minimal(
    out_root: Path,
    code_commit_sha: str,
    entries: list[art.ArtifactEntry],
    *,
    reason: str,
    t0: float,
) -> dict[str, Any]:
    """Fail-closed finalization when a post-access exception prevents normal scoring."""
    prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    manifest = {
        **prov,
        "artifact_family": art.FAMILY_MODEL_RUN_MANIFEST,
        "verdict": ev.CF1_INVALID_RUN,
        "result_state": cc.LONG_STATE_INVALID_RUN,
        "invalid_reason": reason,
        "scored": False,
        "evidence_bearing_run_consumed": True,
        "elapsed_seconds": round(time.monotonic() - t0, 1),
    }
    try:
        man_path = out_root / "manifests" / art.compose_filename(
            family=art.FAMILY_MODEL_RUN_MANIFEST,
            context=art.FILENAME_CONTEXT,
            unix_ms=int(prov["created_at_unix_ms"]),
            code_commit_sha=code_commit_sha,
            ext="json",
        )
        art.write_json_with_sidecar(man_path, manifest, REPO_ROOT)
        entries = list(entries) + [_register(out_root, man_path)]
        _write_inventory(out_root, code_commit_sha, entries)
    except Exception:  # noqa: BLE001 — best-effort; run remains consumed regardless
        pass
    return {
        "verdict": ev.CF1_INVALID_RUN,
        "result_state": cc.LONG_STATE_INVALID_RUN,
        "invalid_reason": reason,
        "code_commit_sha": code_commit_sha,
        "evidence_bearing_run_consumed": True,
        "elapsed_seconds": round(time.monotonic() - t0, 1),
    }


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


def _build_manifest(
    code_commit_sha: str,
    assembled: AssembledOrigins,
    segments: list[SegmentData],
    leak: dict[str, Any],
    result: ev.EvaluationResult,
    *,
    elapsed: float,
    scored: bool,
    computed: bool,
) -> dict[str, Any]:
    prov = art.provenance_block(code_commit_sha=code_commit_sha, command=COMMAND)
    per_block = [
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
        for b in result.blocks
    ]
    aggregate = {
        "baseline_qlike_equal_weighted": result.baseline_qlike_equal if computed else None,
        "augmented_qlike_equal_weighted": result.augmented_qlike_equal if computed else None,
        "delta_equal": result.delta_equal if computed else None,
        "rho": result.rho if computed else None,
        "positive_block_count": result.positive_block_count if computed else None,
        "lb95": result.lb95 if computed else None,
        "bootstrap_block_lengths": result.bootstrap_block_lengths if computed else None,
        "p1": result.p1 if computed else None,
        "p2": result.p2 if computed else None,
        "p3": result.p3 if computed else None,
        "valid": result.valid,
        "verdict": result.verdict,
        "result_state": cc.long_state_for_verdict(result.verdict),
    }
    if computed and result.blocks:
        aggregate["baseline_mse_equal_weighted"] = float(
            np.mean([b.baseline_mse for b in result.blocks])
        )
        aggregate["augmented_mse_equal_weighted"] = float(
            np.mean([b.augmented_mse for b in result.blocks])
        )
        aggregate["baseline_mz_r2_equal_weighted"] = float(
            np.mean([b.baseline_mz_r2 for b in result.blocks])
        )
        aggregate["augmented_mz_r2_equal_weighted"] = float(
            np.mean([b.augmented_mz_r2 for b in result.blocks])
        )
    return {
        **prov,
        "artifact_family": art.FAMILY_MODEL_RUN_MANIFEST,
        "scored": scored,
        "contract": {
            "interval": "(a, b]",
            "p_at_operator": "source_transact_time_ms <= u; greatest row_index tie",
            "horizon_ms": cf1.HORIZON_MS,
            "cadence": "top_of_utc_hour_non_overlapping",
            "coverage_predicate": "tau_{k-1} < ts <= tau_k",
            "coverage_threshold": cf1.COVERAGE_MIN_COVERED_MINUTES,
            "target_epsilon": cf1.TARGET_EPSILON,
            "standardization_epsilon": cf1.STANDARDIZATION_EPSILON,
            "feature_list": list(cc.CORRECTED_FEATURE_COLUMNS),
            "feature_count": cc.CORRECTED_FEATURE_COUNT,
            "prohibited_feature": cc.PROHIBITED_FEATURE_COLUMN,
            "har_lags_hours": [1, cf1.HAR_DAILY_HOURS, cf1.HAR_WEEKLY_HOURS],
            "estimator": "ols_lstsq_intercept",
            "baseline_parameter_count": cc.BASELINE_N_PARAMS,
            "augmented_parameter_count": cc.AUGMENTED_N_PARAMS,
            "expected_baseline_rank": cc.EXPECTED_BASELINE_RANK,
            "expected_augmented_rank": cc.EXPECTED_AUGMENTED_RANK,
            "condition_number_max": cc.CONDITION_NUMBER_MAX,
            "min_training_origins": cc.MIN_TRAIN_ORIGINS,
            "min_block_valid_origins": cc.MIN_BLOCK_VALID_ORIGINS,
            "qlike": "v=RV+eps; h=max(exp(yhat),eps); ratio-ln(ratio)-1",
            "n_blocks": cf1.N_BLOCKS,
            "embargo_ms": cf1.EMBARGO_MS,
            "purge_ms": cf1.PURGE_MS,
            "bootstrap_method": "stratified_by_block_non_circular_moving_block",
            "bootstrap_seed": cc.BOOTSTRAP_SEED,
            "bootstrap_replicates": cc.BOOTSTRAP_REPLICATES,
            "bootstrap_quantile_method": "linear_0.05_lower",
        },
        "counts": {
            "source_partitions_opened": len(leak["partitions_opened_utc_dates"]),
            "rows_read_normalized": sum(s.rows_read_normalized for s in segments),
            "rows_read_features": sum(s.rows_read_features for s in segments),
            "candidate_origins": assembled.candidate_count,
            "valid_targets": assembled.valid_count,
            "invalid_targets": assembled.invalid_count,
            "invalid_targets_by_reason": assembled.invalid_reason_counts,
            "per_block_valid_origins": assembled.per_block_valid,
            "per_block_train_origins": {b.block_id: b.n_train for b in result.blocks},
            "zero_rv_origin_count": assembled.zero_rv_count,
            "bootstrap_block_lengths": result.bootstrap_block_lengths if computed else [],
        },
        "per_block_metrics": per_block,
        "aggregate_metrics": aggregate,
        "governance": {
            "no_october_1": True,
            "no_november": True,
            "no_holdout": True,
            "no_terminal": True,
            "no_sealed": True,
            "no_network": True,
            "no_acquisition": True,
            "no_az_output_root_read": True,
            "no_prohibited_mean_feature": cc.PROHIBITED_FEATURE_COLUMN
            not in cc.CORRECTED_FEATURE_COLUMNS,
            "no_pnl": True,
            "no_direction": True,
        },
        "non_authorization_flags": dict(art.NON_AUTHORIZATION_FLAGS),
        "elapsed_seconds": round(elapsed, 1),
    }


def _write_inventory(
    out_root: Path, code_commit_sha: str, entries: list[art.ArtifactEntry]
) -> None:
    inv = art.build_inventory(code_commit_sha=code_commit_sha, command=COMMAND, entries=entries)
    inv_path = out_root / "manifests" / art.compose_filename(
        family=art.FAMILY_ARTIFACT_INVENTORY,
        context=art.FILENAME_CONTEXT,
        unix_ms=int(inv["created_at_unix_ms"]),
        code_commit_sha=code_commit_sha,
        ext="json",
    )
    art.write_json_with_sidecar(inv_path, inv, REPO_ROOT)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 4bn-BB corrected CF-1 execution")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight", action="store_true", help="preflight only; no market data")
    group.add_argument("--run", action="store_true", help="single evidence-bearing run")
    parser.add_argument("--no-progress", action="store_true")
    args = parser.parse_args(argv)
    progress = not args.no_progress
    try:
        if args.preflight:
            code_sha = _git(["rev-parse", "HEAD"])
            pf = preflight(code_commit_sha=code_sha, verify_repo=True)
            print(json.dumps({"mode": "preflight", **pf}, indent=2, sort_keys=True))
            return 0
        run(progress=progress)
        return 0
    except PreflightFailure as exc:
        print(
            json.dumps(
                {
                    "result_state": cc.LONG_STATE_PREFLIGHT_FAILURE,
                    "short_state": "PREFLIGHT_FAILURE",
                    "gate": exc.gate,
                    "detail": exc.detail,
                    "market_data_opened": False,
                    "evidence_consumed": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
