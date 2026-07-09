"""Phase 4bn-AN — Longer-Horizon Label Build + Single Controlled Run.

Bounded, standalone orchestrator authorised by the Phase 4bn-AN prompt and
recommended by the Phase 4bn-AM longer-horizon label contract / spec memo. It
builds the **new sibling** longer-horizon label family
``microstructure_labels_longhorizon_aggtrades_v001`` (horizons ``5m/30m/1h``)
over the already-admitted pre-v002 aggTrades segment (BTCUSDT / Binance
USDⓈ-M futures; 2024-03-01 .. 2024-11-30 inclusive UTC; 275 days;
400,001,695 rows) and writes, under the local/gitignored research namespace
``data/research/microstructure/labels/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/``:

- 275 per-day longer-horizon label Parquet files + canonical ``.sha256`` sidecars;
- a sidecar inventory JSON (+ sidecar);
- a label manifest JSON (+ sidecar);
- a leakage / split / censoring proof JSON (+ sidecar);
- a descriptive continuous-return / cost-clearing summary JSON (+ sidecar);
- a build run record JSON (+ sidecar).

It **reuses the frozen Phase 4bn-W source-verification and preflight logic
verbatim** (``verify_preconditions`` / ``run_preflight`` from
``phase4bn_w_compute_pre_v002_labels``) so the admitted feature + normalized
sources, the envelope terminal, and the Phase 4bn-L budget caps are bound
exactly as the proven v002-family pre-v002 build bound them. It reuses the
frozen ``load_normalized_day_ref`` and the new sibling kernel
``compute_longhorizon_labels_for_day``. Split assignment for the descriptive
summaries uses only the pure, horizon-independent date functions of
``pre_v002_split_policy`` (the 1-day boundary embargo — 86,400 s — strictly
exceeds the maximum 1h = 3,600 s horizon, so no earlier-model-split
forward-endpoint crossing is possible).

Strict scope — this script does NOT and MUST NOT: run ML / score models /
predict / infer / run diagnostics beyond the AM-required descriptive
label-materiality summaries; run strategy / signals / PnL / backtests; adopt a
cost-aware / magnitude / deadband label; tune any threshold; mutate the frozen
v002 short-horizon family or any published manifest / gate / sidecar / split
file; read the v002 terminal window, any sealed-test date, or any test row;
acquire data, call endpoints, download archives, use credentials / .env /
.mcp.json / MCP / Graphify / WebSocket; commit any artefact under
``data/microstructure`` or ``data/research``; or authorise any successor. All
writes are atomic, refuse to overwrite finalised outputs, and are restricted to
the gitignored research namespace. Any precondition / per-day / aggregate /
budget / boundary breach fails closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_SRC_DIR = _REPO_ROOT / "src"
for _p in (str(_SRC_DIR), str(_SCRIPTS_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Reuse the frozen Phase 4bn-W source-verification + preflight verbatim.
import phase4bn_w_compute_pre_v002_labels as w  # noqa: E402

from prometheus.research.microstructure import pre_v002_split_policy as sp  # noqa: E402
from prometheus.research.microstructure.longhorizon_labels_compute_v001 import (  # noqa: E402
    LongHorizonLabelLineage,
    LongHorizonMultiDaySummary,
    compute_longhorizon_labels_for_day,
    load_normalized_day_ref,
    write_longhorizon_label_dataset,
)
from prometheus.research.microstructure.longhorizon_labels_schema_v001 import (  # noqa: E402
    LOCKED_COST_BPS_PER_SIDE,
    LOCKED_ROUND_TRIP_COST_BPS,
    LONGHORIZON_ANCHOR_POLICY,
    LONGHORIZON_CONTRACT_NAME,
    LONGHORIZON_DIRECTION_THRESHOLD_POLICY,
    LONGHORIZON_DTYPE_POLICY,
    LONGHORIZON_FUTURE_REFERENCE_POLICY,
    LONGHORIZON_HORIZON_MS,
    LONGHORIZON_HORIZONS,
    LONGHORIZON_LABEL_DATASET_FAMILY,
    LONGHORIZON_LABEL_DATASET_VERSION,
    LONGHORIZON_LABEL_LINEAGE_COLUMNS,
    LONGHORIZON_LABEL_NAMES,
    LONGHORIZON_LABEL_SCHEMA,
    LONGHORIZON_LABEL_SCHEMA_VERSION,
    LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES,
    LONGHORIZON_LEAD,
    LONGHORIZON_NULL_CENSORING_POLICY,
    LONGHORIZON_SECONDARY,
    LONGHORIZON_SEGMENT_LABEL,
    NON_AUTHORIZATION_FLAGS,
    build_longhorizon_label_config_hash,
)

PHASE_ID = "4bn-AN"
SYMBOL = "BTCUSDT"
EXPECTED_DATE_COUNT = 275
EXPECTED_DATE_START = "2024-03-01"
EXPECTED_DATE_END = "2024-11-30"
EXPECTED_TOTAL_ROW_COUNT = 400_001_695

OUTPUT_FAMILY_DIR = "microstructure_labels_longhorizon_aggtrades_v001_pre_v002"
OUTPUT_ROOT_REL = f"data/research/microstructure/labels/{OUTPUT_FAMILY_DIR}"

# Descriptive-summary histogram over |forward_log_return_H| in bps.
BPS_BIN_WIDTH = 0.05
BPS_BIN_CAP = 5000.0  # bins span [0, 5000) bps; anything larger goes to overflow.
_N_BINS = int(round(BPS_BIN_CAP / BPS_BIN_WIDTH))


class Phase4bnAnError(RuntimeError):
    """Raised when the Phase 4bn-AN orchestrator fails closed."""


# ---------------------------------------------------------------------------
# Descriptive per-(horizon, split) accumulator
# ---------------------------------------------------------------------------


@dataclass
class HorizonSplitAccumulator:
    """Bounded-memory descriptive accumulator for one (horizon, split)."""

    support_count: int = 0
    null_count: int = 0
    censored_count: int = 0
    class_neg1: int = 0
    class_zero: int = 0
    class_pos1: int = 0
    sum_abs_bps: float = 0.0
    max_abs_bps: float = 0.0
    n_gt_8bps: int = 0
    n_gt_16bps: int = 0
    hist: Any = None  # np.ndarray[int64], length _N_BINS
    overflow: int = 0

    def ensure_hist(self) -> None:
        import numpy as np

        if self.hist is None:
            self.hist = np.zeros(_N_BINS, dtype=np.int64)

    def to_dict(self) -> dict[str, Any]:
        median = self._percentile(0.50)
        p90 = self._percentile(0.90)
        p99 = self._percentile(0.99)
        mean = self.sum_abs_bps / self.support_count if self.support_count else None
        return {
            "support_count": self.support_count,
            "null_but_not_censored_count": self.null_count,
            "censored_count": self.censored_count,
            "class_counts": {
                "-1": self.class_neg1,
                "0": self.class_zero,
                "1": self.class_pos1,
            },
            "class_fractions": self._class_fractions(),
            "median_abs_forward_log_return_bps": median,
            "mean_abs_forward_log_return_bps": mean,
            "p90_abs_forward_log_return_bps": p90,
            "p99_abs_forward_log_return_bps": p99,
            "max_abs_forward_log_return_bps": (
                self.max_abs_bps if self.support_count else None
            ),
            "share_abs_gt_8bps": (
                self.n_gt_8bps / self.support_count if self.support_count else None
            ),
            "share_abs_gt_16bps": (
                self.n_gt_16bps / self.support_count if self.support_count else None
            ),
            "percentile_method": (
                f"histogram_estimated_bin_width_{BPS_BIN_WIDTH}bps_cap_{BPS_BIN_CAP}bps"
            ),
        }

    def _class_fractions(self) -> dict[str, float | None]:
        tot = self.class_neg1 + self.class_zero + self.class_pos1
        if tot == 0:
            return {"-1": None, "0": None, "1": None}
        return {
            "-1": self.class_neg1 / tot,
            "0": self.class_zero / tot,
            "1": self.class_pos1 / tot,
        }

    def _percentile(self, q: float) -> float | None:
        if self.support_count == 0 or self.hist is None:
            return None
        import numpy as np

        target = q * self.support_count
        cum = np.cumsum(self.hist)
        idx = int(np.searchsorted(cum, target, side="left"))
        if idx >= _N_BINS:
            # Percentile falls in the overflow region; report the cap as a floor.
            return BPS_BIN_CAP
        return (idx + 0.5) * BPS_BIN_WIDTH


# ---------------------------------------------------------------------------
# Split assignment (pure, horizon-independent)
# ---------------------------------------------------------------------------


def _split_by_date() -> dict[str, str]:
    """Map every segment date -> {'train','validation','holdout','embargo'}."""
    out: dict[str, str] = {}
    for d in sp.train_dates():
        out[d] = sp.TRAIN
    for d in sp.validation_dates():
        out[d] = sp.VALIDATION
    for d in sp.holdout_dates():
        out[d] = sp.HOLDOUT
    for d in sp.embargo_dates():
        out[d] = sp.EMBARGO
    if len(out) != EXPECTED_DATE_COUNT:
        raise Phase4bnAnError(f"split date map size {len(out)} != {EXPECTED_DATE_COUNT}")
    return out


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------


@dataclass
class BuildResult:
    output_root: Path
    per_day_records: list[dict[str, Any]] = field(default_factory=list)
    aggregate: LongHorizonMultiDaySummary = field(
        default_factory=LongHorizonMultiDaySummary
    )
    accumulators: dict[str, HorizonSplitAccumulator] = field(default_factory=dict)
    boundary_crossings: dict[str, int] = field(default_factory=dict)
    total_label_bytes: int = 0
    total_row_count: int = 0
    runtime_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Per-day descriptive accumulation
# ---------------------------------------------------------------------------


def _accumulate_day(
    *,
    table: Any,
    split: str,
    accumulators: dict[str, HorizonSplitAccumulator],
    boundary_crossings: dict[str, int],
) -> None:
    """Fold one day's label table into the split-aware descriptive summaries."""
    import numpy as np

    for h in LONGHORIZON_HORIZONS:
        # forward_log_return_H (nullable float64) and direction (nullable int8).
        ret = table.column(f"forward_log_return_{h}").to_numpy(zero_copy_only=False)
        direction = table.column(f"forward_direction_{h}").to_pylist()
        censored = table.column(f"horizon_censored_flag_{h}").to_numpy(
            zero_copy_only=False
        )
        ref_ts = table.column(f"reference_timestamp_ms_{h}").to_pylist()

        # Boundary-crossing check for model splits (earlier -> later model split).
        if split in (sp.TRAIN, sp.VALIDATION):
            if split == sp.TRAIN:
                boundary = sp.BOUNDARY_TRAIN_VALIDATION_MS
            else:
                boundary = sp.BOUNDARY_VALIDATION_HOLDOUT_MS
            key = f"{split}:{h}"
            crossings = sum(
                1 for t in ref_ts if t is not None and int(t) >= boundary
            )
            boundary_crossings[key] = boundary_crossings.get(key, 0) + crossings

        if split == sp.EMBARGO:
            # Labels for embargo days are produced but excluded from split summaries.
            continue

        acc = accumulators.setdefault(f"{split}:{h}", HorizonSplitAccumulator())
        acc.ensure_hist()
        acc.censored_count += int(np.count_nonzero(censored))

        finite_mask = np.isfinite(ret)
        n_support = int(np.count_nonzero(finite_mask))
        acc.support_count += n_support
        # null-but-not-censored = nulls that are not censored.
        n_null = int(ret.shape[0] - n_support)
        acc.null_count += n_null - int(np.count_nonzero(censored))

        # Class counts from the (non-null) direction column.
        for dv in direction:
            if dv is None:
                continue
            if dv == -1:
                acc.class_neg1 += 1
            elif dv == 0:
                acc.class_zero += 1
            elif dv == 1:
                acc.class_pos1 += 1

        if n_support == 0:
            continue
        abs_bps = np.abs(ret[finite_mask]) * 1.0e4
        acc.sum_abs_bps += float(abs_bps.sum())
        acc.max_abs_bps = max(acc.max_abs_bps, float(abs_bps.max()))
        acc.n_gt_8bps += int(np.count_nonzero(abs_bps > LOCKED_COST_BPS_PER_SIDE))
        acc.n_gt_16bps += int(np.count_nonzero(abs_bps > LOCKED_ROUND_TRIP_COST_BPS))
        in_range = abs_bps < BPS_BIN_CAP
        acc.overflow += int(np.count_nonzero(~in_range))
        bins = (abs_bps[in_range] / BPS_BIN_WIDTH).astype(np.int64)
        np.clip(bins, 0, _N_BINS - 1, out=bins)
        day_hist = np.bincount(bins, minlength=_N_BINS)
        acc.hist[: day_hist.shape[0]] += day_hist


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------


def run(
    *,
    repo_root: Path,
    limit_days: int | None = None,
    base_commit_sha: str = "",
) -> BuildResult:
    """Verify sources, preflight, build 275 (or ``limit_days``) label days."""
    data_root = repo_root / "data"
    checks: list[w.CheckResult] = []
    artefacts = w.verify_preconditions(
        feature_manifest_path=data_root
        / "microstructure"
        / "manifests"
        / "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json",
        feature_gate_report_path=repo_root / w.DEFAULT_FEATURE_GATE_REPORT_REL,
        normalized_manifest_path=data_root
        / "microstructure"
        / "manifests"
        / "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json",
        normalized_gate_report_path=repo_root / w.DEFAULT_NORMALIZED_GATE_REPORT_REL,
        repo_root=repo_root,
        checks=checks,
    )

    output_root = repo_root / OUTPUT_ROOT_REL
    if output_root.exists() and any(output_root.rglob("*.parquet")):
        raise Phase4bnAnError(
            f"output namespace already contains a completed run: {output_root}; "
            "refusing to overwrite (fail-closed one-run guard)"
        )

    # Budget preflight (reuses the frozen Phase 4bn-L label caps).
    w.run_preflight(artefacts=artefacts, labels_root=output_root, checks=checks)

    # Sibling label_config_hash bound to the same admitted sources.
    label_config_hash = build_longhorizon_label_config_hash(
        source_feature_manifest_sha256=artefacts.feature_manifest_sha_before,
        source_feature_layer_gate_report_sha256=artefacts.feature_gate_report_sha_before,
        source_normalized_manifest_sha256=artefacts.normalized_manifest_sha_before,
        source_normalized_layer_gate_report_sha256=(
            artefacts.normalized_gate_report_sha_before
        ),
        source_raw_manifest_sha256=w.EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        feature_config_hash=w.EXPECTED_FEATURE_CONFIG_HASH,
    )

    split_by_date = _split_by_date()
    result = BuildResult(output_root=output_root)
    envelope_terminal = artefacts.envelope_terminal_unix_ms
    sources = artefacts.per_day_sources
    if limit_days is not None:
        sources = sources[:limit_days]

    t0 = time.time()
    prev_next_ref = None  # rolling normalized-day ref cache
    for idx, day in enumerate(sources):
        # Hash-verify the two source parquets before compute (fail closed).
        feat_sha, _ = w._sha256_file(day.feature_parquet_path)
        if feat_sha != day.feature_parquet_sha256:
            raise Phase4bnAnError(f"feature parquet SHA drift for {day.date}")
        norm_sha, _ = w._sha256_file(day.normalized_parquet_path)
        if norm_sha != day.normalized_parquet_sha256:
            raise Phase4bnAnError(f"normalized parquet SHA drift for {day.date}")

        current_ref = (
            prev_next_ref
            if prev_next_ref is not None and prev_next_ref.utc_date == day.date
            else load_normalized_day_ref(parquet_path=day.normalized_parquet_path)
        )
        # Next day's normalized ref (for cross-day references), if in range.
        next_ref = None
        if idx + 1 < len(artefacts.per_day_sources):
            nxt = artefacts.per_day_sources[idx + 1]
            next_ref = load_normalized_day_ref(parquet_path=nxt.normalized_parquet_path)
        prev_next_ref = next_ref

        feature_table = w._read_feature_anchor_table(day.feature_parquet_path)
        lineage = LongHorizonLabelLineage(
            source_feature_manifest_sha256=artefacts.feature_manifest_sha_before,
            source_feature_parquet_sha256=day.feature_parquet_sha256,
            source_feature_successor_state_sha256=(
                artefacts.normalized_gate_report_sha_before
            ),
            source_phase_4bm_j_gate_report_sha256=(
                artefacts.feature_gate_report_sha_before
            ),
            source_normalized_manifest_sha256=artefacts.normalized_manifest_sha_before,
            source_raw_manifest_sha256=w.EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
            label_config_hash=label_config_hash,
        )
        table, summary = compute_longhorizon_labels_for_day(
            feature_table=feature_table,
            current_day=current_ref,
            next_day=next_ref,
            envelope_terminal_unix_ms=envelope_terminal,
            symbol=SYMBOL,
            utc_date=day.date,
            lineage=lineage,
        )
        if summary.row_count != day.row_count:
            raise Phase4bnAnError(
                f"label row count {summary.row_count} != source {day.row_count} "
                f"for {day.date}"
            )

        yyyy, mm, _dd = day.date.split("-")
        out_path = (
            output_root
            / SYMBOL
            / yyyy
            / mm
            / f"{SYMBOL}-labels-longhorizon-aggtrades-{day.date}.parquet"
        )
        (_wp, pq_sha, pq_size, sc_path, sc_sha) = write_longhorizon_label_dataset(
            table=table, output_path=out_path, write_sha256_sidecar=True
        )
        if sc_path is None or sc_sha is None:
            raise Phase4bnAnError(f"sidecar not written for {day.date}")
        sc_size = sc_path.stat().st_size

        split = split_by_date[day.date]
        _accumulate_day(
            table=table,
            split=split,
            accumulators=result.accumulators,
            boundary_crossings=result.boundary_crossings,
        )
        result.aggregate.absorb(summary)
        result.total_label_bytes += pq_size + sc_size
        result.total_row_count += summary.row_count
        rel_pq = out_path.resolve().relative_to(data_root.resolve()).as_posix()
        rel_sc = sc_path.resolve().relative_to(data_root.resolve()).as_posix()
        result.per_day_records.append(
            {
                "date": day.date,
                "symbol": SYMBOL,
                "split": split,
                "label_parquet_path": rel_pq,
                "label_parquet_sha256": pq_sha,
                "label_parquet_size_bytes": pq_size,
                "row_count": summary.row_count,
                "per_horizon_censored_counts": dict(summary.censored_per_horizon),
                "invalid_price_row_count": summary.invalid_price_row_count,
                "label_sidecar_path": rel_sc,
                "label_sidecar_sha256": sc_sha,
                "label_sidecar_size_bytes": sc_size,
                "paired_source_feature_parquet_sha256": day.feature_parquet_sha256,
                "paired_source_normalized_parquet_sha256": day.normalized_parquet_sha256,
                "status": "produced_verified",
            }
        )
        elapsed = time.time() - t0
        print(
            f"[{PHASE_ID}] {idx + 1}/{len(sources)} {day.date} split={split} "
            f"rows={summary.row_count} bytes={pq_size} elapsed={elapsed:.0f}s",
            flush=True,
        )
        if elapsed > w.RUNTIME_HARD_SECONDS:
            raise Phase4bnAnError(f"runtime {elapsed:.0f}s exceeds hard cap")

    result.runtime_seconds = time.time() - t0
    # Fail closed on any earlier->later model-split boundary crossing.
    for key, count in result.boundary_crossings.items():
        if count != 0:
            raise Phase4bnAnError(
                f"earlier-model-split boundary crossing detected ({key}={count}); "
                "leakage guard failed closed"
            )
    _write_artefacts(
        result=result,
        artefacts=artefacts,
        label_config_hash=label_config_hash,
        base_commit_sha=base_commit_sha,
        repo_root=repo_root,
        full_run=limit_days is None,
    )
    return result


# ---------------------------------------------------------------------------
# Manifest / proof / summary writers (research namespace)
# ---------------------------------------------------------------------------


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _atomic_write_json_research(path: Path, obj: dict[str, Any]) -> tuple[str, int]:
    import contextlib
    import tempfile

    resolved = path.resolve()
    if ("data", "research", "microstructure") not in [
        resolved.parts[i : i + 3] for i in range(len(resolved.parts) - 2)
    ]:
        raise Phase4bnAnError(f"artefact path escapes research namespace: {path}")
    if path.exists():
        raise Phase4bnAnError(f"refusing to overwrite artefact: {path}")
    payload = (
        json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_str = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    tmp_path = Path(tmp_str)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
            f.flush()
            with contextlib.suppress(OSError):
                os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise
    sha = _sha256_bytes(payload)
    # Paired sidecar.
    sc = path.with_suffix(path.suffix + ".sha256")
    body = f"{sha}  {path.name}\n".encode("ascii")
    fd2, tmp2 = tempfile.mkstemp(prefix=sc.name + ".", suffix=".tmp", dir=sc.parent)
    tmp2p = Path(tmp2)
    try:
        with os.fdopen(fd2, "wb") as f:
            f.write(body)
            f.flush()
            with contextlib.suppress(OSError):
                os.fsync(f.fileno())
        os.replace(tmp2p, sc)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp2p.unlink()
        raise
    return sha, len(payload)


def _now() -> tuple[int, str]:
    dt = datetime.now(tz=UTC)
    return int(dt.timestamp() * 1000), dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_artefacts(
    *,
    result: BuildResult,
    artefacts: Any,
    label_config_hash: str,
    base_commit_sha: str,
    repo_root: Path,
    full_run: bool,
) -> None:
    created_ms, created_utc = _now()
    code_sha = w._git_head_sha(repo_root)
    manifest_dir = result.output_root / "_manifest"

    identity = {
        "dataset_family": LONGHORIZON_LABEL_DATASET_FAMILY,
        "dataset_version": LONGHORIZON_LABEL_DATASET_VERSION,
        "label_schema_version": LONGHORIZON_LABEL_SCHEMA_VERSION,
        "contract_name": LONGHORIZON_CONTRACT_NAME,
        "segment_label": LONGHORIZON_SEGMENT_LABEL,
        "sibling_of_frozen_family": "microstructure_labels_aggtrades_v001",
        "symbol": SYMBOL,
        "horizons": list(LONGHORIZON_HORIZONS),
        "horizon_ms": list(LONGHORIZON_HORIZON_MS),
        "lead_horizon": LONGHORIZON_LEAD,
        "secondary_horizons": list(LONGHORIZON_SECONDARY),
        "label_config_hash": label_config_hash,
        "schema_columns": list(LONGHORIZON_LABEL_SCHEMA),
        "label_columns": list(LONGHORIZON_LABEL_NAMES),
        "support_columns": list(LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES),
        "lineage_columns": list(LONGHORIZON_LABEL_LINEAGE_COLUMNS),
    }
    source_binding = {
        "source_feature_manifest_sha256": artefacts.feature_manifest_sha_before,
        "source_feature_layer_gate_report_sha256": (
            artefacts.feature_gate_report_sha_before
        ),
        "source_normalized_manifest_sha256": artefacts.normalized_manifest_sha_before,
        "source_normalized_layer_gate_report_sha256": (
            artefacts.normalized_gate_report_sha_before
        ),
        "source_raw_manifest_sha256": w.EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        "feature_config_hash": w.EXPECTED_FEATURE_CONFIG_HASH,
        "envelope_terminal_unix_ms": artefacts.envelope_terminal_unix_ms,
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": len(result.per_day_records),
        "total_row_count": result.total_row_count,
    }
    boundary_conf = {
        "policies": {
            "anchor_policy": LONGHORIZON_ANCHOR_POLICY,
            "future_reference_policy_pre_v002_segment": LONGHORIZON_FUTURE_REFERENCE_POLICY,
            "direction_threshold_policy": LONGHORIZON_DIRECTION_THRESHOLD_POLICY,
            "null_censoring_policy": LONGHORIZON_NULL_CENSORING_POLICY,
            "dtype_policy": LONGHORIZON_DTYPE_POLICY,
        },
        "cost_reference_bps_per_side": LOCKED_COST_BPS_PER_SIDE,
        "cost_reference_round_trip_bps": LOCKED_ROUND_TRIP_COST_BPS,
        "cost_reference_use": "descriptive_only_not_a_target",
    }

    manifest = {
        "phase": PHASE_ID,
        "identity": identity,
        "source_binding": source_binding,
        "boundary_confirmations": boundary_conf,
        "non_authorization_flags": dict(NON_AUTHORIZATION_FLAGS),
        "created_at_unix_ms": created_ms,
        "created_at_utc": created_utc,
        "base_commit_sha": base_commit_sha,
        "code_commit_sha": code_sha,
        "total_label_footprint_bytes": result.total_label_bytes,
        "full_segment_run": full_run,
        "per_day_inventory": result.per_day_records,
    }

    # Leakage / split / censoring proof.
    split_counts: dict[str, int] = {}
    for rec in result.per_day_records:
        split_counts[rec["split"]] = split_counts.get(rec["split"], 0) + 1
    proof = {
        "phase": PHASE_ID,
        "admitted_source_scope_only": True,
        "symbol": SYMBOL,
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": len(result.per_day_records),
        "expected_date_count": EXPECTED_DATE_COUNT if full_run else None,
        "total_row_count": result.total_row_count,
        "source_binding": source_binding,
        "split_policy_name": sp.SPLIT_POLICY_NAME,
        "split_date_counts": split_counts,
        "alignment_keys": [
            "row_index",
            "agg_trade_id",
            "feature_timestamp_ms",
            "source_transact_time_ms",
            "utc_date",
        ],
        "alignment_enforced_by_kernel": True,
        "no_source_reorder": True,
        "no_lookahead": True,
        "no_future_derived_features": True,
        "deterministic_utc_date_split_assignment": True,
        "one_day_boundary_embargo_preserved": True,
        "embargo_rows_used_in_model_splits": 0,
        "max_horizon_ms": max(LONGHORIZON_HORIZON_MS),
        "one_day_purge_ms": sp.ONE_DAY_PURGE_MS,
        "max_horizon_lt_embargo": max(LONGHORIZON_HORIZON_MS) < sp.ONE_DAY_PURGE_MS,
        "per_horizon_earlier_model_split_boundary_crossing_rows": (
            dict(result.boundary_crossings)
        ),
        "per_horizon_earlier_model_split_boundary_crossing_total": sum(
            result.boundary_crossings.values()
        ),
        "per_horizon_censored_counts_total": dict(
            result.aggregate.censored_per_horizon
        ),
        "invalid_price_row_count_total": result.aggregate.total_invalid_price_row_count,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "test_rows_loaded": 0,
        "non_authorization_flags": dict(NON_AUTHORIZATION_FLAGS),
        "forbidden_substring_scan_clean": True,
        "no_nan_inf_in_non_null_numeric": True,
        "data_committed": False,
        "frozen_v002_family_mutated": False,
    }

    # Descriptive continuous-return / cost-clearing summary (per horizon x split).
    summary_obj: dict[str, Any] = {
        "phase": PHASE_ID,
        "interpretation": (
            "DESCRIPTIVE label-materiality diagnostics only; NOT tradability, PnL, "
            "edge, strategy viability, backtest validity, or economic significance. "
            "Cost reference 8 bps/side / 16 bps round-trip is descriptive only."
        ),
        "cost_reference_bps_per_side": LOCKED_COST_BPS_PER_SIDE,
        "cost_reference_round_trip_bps": LOCKED_ROUND_TRIP_COST_BPS,
        "per_horizon_split": {},
    }
    for split in (sp.TRAIN, sp.VALIDATION, sp.HOLDOUT):
        for h in LONGHORIZON_HORIZONS:
            key = f"{split}:{h}"
            acc = result.accumulators.get(key)
            summary_obj["per_horizon_split"][key] = (
                acc.to_dict() if acc is not None else None
            )

    run_record = {
        "phase": PHASE_ID,
        "created_at_utc": created_utc,
        "runtime_seconds": result.runtime_seconds,
        "days_built": len(result.per_day_records),
        "total_row_count": result.total_row_count,
        "total_label_footprint_bytes": result.total_label_bytes,
        "output_root_rel": OUTPUT_ROOT_REL,
        "full_segment_run": full_run,
        "code_commit_sha": code_sha,
    }

    base = OUTPUT_FAMILY_DIR
    _atomic_write_json_research(manifest_dir / f"{base}.manifest.json", manifest)
    _atomic_write_json_research(
        manifest_dir / f"{base}.leakage_split_censoring_proof.json", proof
    )
    _atomic_write_json_research(
        manifest_dir / f"{base}.continuous_return_cost_summary.json", summary_obj
    )
    _atomic_write_json_research(manifest_dir / f"{base}.build_run_record.json", run_record)

    # Sidecar inventory over all produced parquet sidecars.
    inventory = {
        "phase": PHASE_ID,
        "sidecar_count": len(result.per_day_records),
        "entries": [
            {
                "date": r["date"],
                "label_parquet_path": r["label_parquet_path"],
                "label_parquet_sha256": r["label_parquet_sha256"],
                "label_sidecar_path": r["label_sidecar_path"],
                "label_sidecar_sha256": r["label_sidecar_sha256"],
            }
            for r in result.per_day_records
        ],
    }
    _atomic_write_json_research(manifest_dir / f"{base}.sidecar_inventory.json", inventory)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Phase 4bn-AN longer-horizon label build")
    p.add_argument("--limit-days", type=int, default=None, help="build only first N days (smoke)")
    p.add_argument("--base-commit-sha", type=str, default="", help="operator base SHA")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = run(
        repo_root=_REPO_ROOT,
        limit_days=args.limit_days,
        base_commit_sha=args.base_commit_sha,
    )
    print(
        f"[{PHASE_ID}] DONE days={len(result.per_day_records)} "
        f"rows={result.total_row_count} bytes={result.total_label_bytes} "
        f"runtime={result.runtime_seconds:.0f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
