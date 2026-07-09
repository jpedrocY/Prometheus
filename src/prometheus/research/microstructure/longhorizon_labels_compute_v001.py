"""Phase 4bn-AN longer-horizon aggTrades label computation kernel (sibling).

Faithful transcription of the frozen Phase 4bm-O v002 label kernel
(``labels_compute_v002.compute_aggtrade_labels_v002_for_day``), parametrised
to the **new** longer-horizon set ``5m / 30m / 1h`` and emitting the sibling
schema :data:`longhorizon_labels_schema_v001.LONGHORIZON_LABEL_SCHEMA`.

The reference-resolution algorithm is **identical** to the v002 kernel: for
horizon ``H`` the reference row is the largest-row-index normalized aggTrades
row across the pre-v002 envelope with ``transact_time_ms <=
feature_timestamp_ms + H_ms``; the cross-day branch resolves against
``next_day`` only. That branch remains valid for this family because every
longer horizon (max 1h = 3_600_000 ms) is strictly less than one UTC day
(86_400_000 ms), so a target timestamp can fall at most into the immediately
following day — exactly the case the v002 kernel already handles. Prices are
parsed exactly to ``Decimal``, the ratio is taken in ``Decimal``, and a
``float64`` cast happens only at the natural-log step, identical to v002.

This module:

- reuses ``load_normalized_day_ref`` from the frozen v002 kernel unchanged
  (it is horizon-agnostic);
- does **not** mutate the frozen v002 family, schema, or kernel;
- performs **no** networking, endpoint, credential, or environment access;
- computes **no** strategy / signal / PnL / edge / prediction / model score;
- writes only via :func:`write_longhorizon_label_dataset`, which is
  restricted to the gitignored ``data/research/microstructure/`` namespace and
  refuses to overwrite a finalised file.
"""

from __future__ import annotations

import contextlib
import math
import os
import tempfile
from dataclasses import dataclass, field
from decimal import Decimal, getcontext
from pathlib import Path
from typing import TYPE_CHECKING, Any

# Reuse the frozen, horizon-agnostic normalized-day loader verbatim.
from .labels_compute_v002 import (
    LabelComputationErrorV002,
    NormalizedDayRef,
    load_normalized_day_ref,
)
from .labels_schema_v002 import (
    LabelSchemaErrorV002,
    assert_no_forbidden_label_substrings_v002,
)
from .longhorizon_labels_schema_v001 import (
    LONGHORIZON_HORIZON_MS,
    LONGHORIZON_HORIZONS,
    LONGHORIZON_LABEL_DATASET_FAMILY,
    LONGHORIZON_LABEL_DATASET_VERSION,
    LONGHORIZON_LABEL_NAMES,
    LONGHORIZON_LABEL_SCHEMA,
    LONGHORIZON_LABEL_SCHEMA_VERSION,
    LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES,
    SOURCE_FEATURE_DATASET_FAMILY,
    SOURCE_FEATURE_DATASET_VERSION,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    import pyarrow as pa

getcontext().prec = 50

# Re-export the loader + shared error for orchestrator convenience.
__all__ = [
    "LabelComputationErrorV002",
    "LongHorizonLabelLineage",
    "LongHorizonLabelSummary",
    "NormalizedDayRef",
    "compute_longhorizon_labels_for_day",
    "load_normalized_day_ref",
    "write_longhorizon_label_dataset",
]


@dataclass(frozen=True)
class LongHorizonLabelLineage:
    """Lineage SHAs threaded into every output row and the label manifest."""

    source_feature_manifest_sha256: str
    source_feature_parquet_sha256: str
    source_feature_successor_state_sha256: str
    source_phase_4bm_j_gate_report_sha256: str
    source_normalized_manifest_sha256: str
    source_raw_manifest_sha256: str
    label_config_hash: str


@dataclass(frozen=True)
class LongHorizonLabelSummary:
    """Per-day summary of computed longer-horizon labels."""

    utc_date: str
    row_count: int
    invalid_price_row_count: int
    censored_per_horizon: dict[str, int]


@dataclass
class LongHorizonMultiDaySummary:
    """Aggregate summary across all per-day longer-horizon computations."""

    total_row_count: int = 0
    total_invalid_price_row_count: int = 0
    censored_per_horizon: dict[str, int] = field(
        default_factory=lambda: dict.fromkeys(LONGHORIZON_HORIZONS, 0)
    )

    def absorb(self, day_summary: LongHorizonLabelSummary) -> None:
        self.total_row_count += day_summary.row_count
        self.total_invalid_price_row_count += day_summary.invalid_price_row_count
        for h in LONGHORIZON_HORIZONS:
            self.censored_per_horizon[h] += day_summary.censored_per_horizon[h]


def compute_longhorizon_labels_for_day(
    *,
    feature_table: pa.Table,
    current_day: NormalizedDayRef,
    next_day: NormalizedDayRef | None,
    envelope_terminal_unix_ms: int,
    symbol: str,
    utc_date: str,
    lineage: LongHorizonLabelLineage,
) -> tuple[pa.Table, LongHorizonLabelSummary]:
    """Compute the longer-horizon label table for one UTC day.

    Structurally identical to the frozen v002 kernel, iterating over the
    longer-horizon set instead of ``1s/5s/15s/60s``. Returns a
    :class:`pa.Table` in canonical :data:`LONGHORIZON_LABEL_SCHEMA` order.
    """
    import numpy as np
    import pyarrow as pa

    assert_no_forbidden_label_substrings_v002(LONGHORIZON_LABEL_SCHEMA)

    # --- 1. Validate feature table shape and per-row alignment ---
    feat_names = tuple(feature_table.column_names)
    required_feat_cols = (
        "row_index",
        "agg_trade_id",
        "feature_timestamp_ms",
        "source_transact_time_ms",
    )
    for col in required_feat_cols:
        if col not in feat_names:
            raise LabelComputationErrorV002(f"feature_table must contain {col!r}")
    n_feat = feature_table.num_rows
    if n_feat <= 0:
        raise LabelComputationErrorV002("feature_table must have > 0 rows")

    feat_row_index = (
        feature_table.column("row_index").to_numpy(zero_copy_only=False).astype(np.int64)
    )
    feat_agg_id = (
        feature_table.column("agg_trade_id").to_numpy(zero_copy_only=False).astype(np.int64)
    )
    feat_ts_ms = (
        feature_table.column("feature_timestamp_ms")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
    )
    feat_src_ts_ms = (
        feature_table.column("source_transact_time_ms")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
    )

    if not np.array_equal(feat_row_index, np.arange(n_feat, dtype=np.int64)):
        raise LabelComputationErrorV002(
            "feature_table row_index must equal np.arange(n_feat)"
        )
    if not np.array_equal(feat_ts_ms, feat_src_ts_ms):
        raise LabelComputationErrorV002(
            "feature feature_timestamp_ms must equal source_transact_time_ms per row"
        )

    # --- 2. Validate current_day alignment with feature table ---
    if current_day.utc_date != utc_date:
        raise LabelComputationErrorV002(
            f"current_day.utc_date {current_day.utc_date!r} != {utc_date!r}"
        )
    n_norm = len(current_day.transact_time_ms)
    if n_norm != n_feat:
        raise LabelComputationErrorV002(
            f"current_day row count {n_norm} != feature_table row count {n_feat}"
        )
    if not np.array_equal(current_day.agg_trade_id, feat_agg_id):
        raise LabelComputationErrorV002(
            "current_day agg_trade_id must equal feature_table agg_trade_id per row"
        )
    if not np.array_equal(current_day.transact_time_ms, feat_src_ts_ms):
        raise LabelComputationErrorV002(
            "current_day transact_time_ms must equal feature_table "
            "source_transact_time_ms per row"
        )

    # --- 3. Envelope-terminal sanity ---
    if envelope_terminal_unix_ms <= 0:
        raise LabelComputationErrorV002("envelope_terminal_unix_ms must be positive")
    cur_last_ts = int(current_day.transact_time_ms[-1])
    if cur_last_ts > envelope_terminal_unix_ms:
        raise LabelComputationErrorV002(
            f"current_day last transact_time_ms {cur_last_ts} > "
            f"envelope_terminal_unix_ms {envelope_terminal_unix_ms}"
        )

    next_ts: Any | None = None
    next_prices: list[Decimal] | None = None
    if next_day is not None:
        next_ts = next_day.transact_time_ms
        next_prices = next_day.prices_decimal
        if len(next_ts) <= 0:
            raise LabelComputationErrorV002(f"next_day {next_day.utc_date} has zero rows")

    # --- 4. Per-horizon target timestamps and reference arrays ---
    forward_log_return: dict[str, list[float | None]] = {
        label: [None] * n_feat for label in LONGHORIZON_HORIZONS
    }
    forward_direction: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LONGHORIZON_HORIZONS
    }
    reference_row_index: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LONGHORIZON_HORIZONS
    }
    reference_timestamp_ms: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LONGHORIZON_HORIZONS
    }
    horizon_censored_flag: dict[str, list[bool]] = {
        label: [False] * n_feat for label in LONGHORIZON_HORIZONS
    }
    label_invalid_price_flag = [False] * n_feat
    label_any_censored_flag = [False] * n_feat
    invalid_price_count = 0
    censored_per_horizon: dict[str, int] = dict.fromkeys(LONGHORIZON_HORIZONS, 0)

    cur_ts = current_day.transact_time_ms
    per_horizon_cur_ref_idx: dict[str, Any] = {}
    per_horizon_next_ref_idx: dict[str, Any] = {}
    per_horizon_censored_mask: dict[str, Any] = {}
    for h_label, h_ms in zip(
        LONGHORIZON_HORIZONS, LONGHORIZON_HORIZON_MS, strict=True
    ):
        target_ts = feat_ts_ms + np.int64(h_ms)
        censored = target_ts > np.int64(envelope_terminal_unix_ms)
        insert_cur = np.searchsorted(cur_ts, target_ts, side="right").astype(np.int64)
        ref_idx_cur = insert_cur - 1
        ref_idx_cur[censored] = -1
        per_horizon_cur_ref_idx[h_label] = ref_idx_cur

        if next_ts is not None:
            insert_next = np.searchsorted(next_ts, target_ts, side="right").astype(
                np.int64
            )
            ref_idx_next = insert_next - 1
            ref_idx_next[censored] = -1
            per_horizon_next_ref_idx[h_label] = ref_idx_next
        else:
            per_horizon_next_ref_idx[h_label] = None
        per_horizon_censored_mask[h_label] = censored

    # --- 5. Compute labels row-by-row ---
    for i in range(n_feat):
        anchor_price = current_day.prices_decimal[i]
        anchor_invalid = anchor_price <= 0
        if anchor_invalid:
            label_invalid_price_flag[i] = True
            invalid_price_count += 1
        any_censored = False
        for h_label in LONGHORIZON_HORIZONS:
            censored_arr = per_horizon_censored_mask[h_label]
            if bool(censored_arr[i]):
                horizon_censored_flag[h_label][i] = True
                any_censored = True
                censored_per_horizon[h_label] += 1
                continue

            next_arr = per_horizon_next_ref_idx[h_label]
            ref_in_next = next_arr is not None and int(next_arr[i]) >= 0
            if ref_in_next:
                ref_local_idx = int(next_arr[i])
                ref_ts = int(next_ts[ref_local_idx])  # type: ignore[index]
                assert next_prices is not None  # narrow type for mypy
                ref_price = next_prices[ref_local_idx]
            else:
                cur_arr = per_horizon_cur_ref_idx[h_label]
                ref_local_idx = int(cur_arr[i])
                if ref_local_idx < 0:
                    if not label_invalid_price_flag[i]:
                        label_invalid_price_flag[i] = True
                        invalid_price_count += 1
                    continue
                ref_ts = int(cur_ts[ref_local_idx])
                ref_price = current_day.prices_decimal[ref_local_idx]

            reference_row_index[h_label][i] = ref_local_idx
            reference_timestamp_ms[h_label][i] = ref_ts

            ref_invalid = ref_price <= 0
            if ref_invalid:
                if not label_invalid_price_flag[i]:
                    label_invalid_price_flag[i] = True
                    invalid_price_count += 1
                continue
            if anchor_invalid:
                continue

            ratio = ref_price / anchor_price
            log_ret = math.log(float(ratio))
            if not math.isfinite(log_ret):
                if not label_invalid_price_flag[i]:
                    label_invalid_price_flag[i] = True
                    invalid_price_count += 1
                continue
            forward_log_return[h_label][i] = log_ret
            if log_ret > 0.0:
                forward_direction[h_label][i] = 1
            elif log_ret < 0.0:
                forward_direction[h_label][i] = -1
            else:
                forward_direction[h_label][i] = 0

        if any_censored:
            label_any_censored_flag[i] = True

    # --- 6. Build pyarrow schema in canonical column order ---
    int64_cols = {
        "row_index",
        "agg_trade_id",
        "feature_timestamp_ms",
        "source_transact_time_ms",
    }
    string_cols = {
        "dataset_family",
        "dataset_version",
        "label_schema_version",
        "source_feature_dataset_family",
        "source_feature_dataset_version",
        "source_feature_manifest_sha256",
        "source_feature_parquet_sha256",
        "source_feature_successor_state_sha256",
        "source_phase_4bm_j_gate_report_sha256",
        "source_normalized_manifest_sha256",
        "source_raw_manifest_sha256",
        "symbol",
        "utc_date",
        "label_config_hash",
    }
    nullable_int64_cols = {
        f"reference_row_index_{label}" for label in LONGHORIZON_HORIZONS
    }
    nullable_int64_cols.update(
        {f"reference_timestamp_ms_{label}" for label in LONGHORIZON_HORIZONS}
    )
    nullable_float_cols = {
        f"forward_log_return_{label}" for label in LONGHORIZON_HORIZONS
    }
    nullable_int8_cols = {
        f"forward_direction_{label}" for label in LONGHORIZON_HORIZONS
    }
    bool_cols = {f"horizon_censored_flag_{label}" for label in LONGHORIZON_HORIZONS}
    bool_cols.update({"label_invalid_price_flag", "label_any_censored_flag"})

    schema_fields: list[pa.Field] = []
    for col in LONGHORIZON_LABEL_SCHEMA:
        if col in int64_cols:
            schema_fields.append(pa.field(col, pa.int64(), nullable=False))
        elif col in string_cols:
            schema_fields.append(pa.field(col, pa.string(), nullable=False))
        elif col in nullable_int64_cols:
            schema_fields.append(pa.field(col, pa.int64(), nullable=True))
        elif col in nullable_float_cols:
            schema_fields.append(pa.field(col, pa.float64(), nullable=True))
        elif col in nullable_int8_cols:
            schema_fields.append(pa.field(col, pa.int8(), nullable=True))
        elif col in bool_cols:
            schema_fields.append(pa.field(col, pa.bool_(), nullable=False))
        else:  # pragma: no cover - defensive
            raise LabelSchemaErrorV002(f"unclassified label column {col!r}")
    schema = pa.schema(schema_fields)
    if tuple(schema.names) != LONGHORIZON_LABEL_SCHEMA:
        raise LabelSchemaErrorV002(
            "constructed schema does not match LONGHORIZON_LABEL_SCHEMA column order"
        )

    # --- 7. Assemble column data ---
    column_data: dict[str, Any] = {}
    column_data["dataset_family"] = [LONGHORIZON_LABEL_DATASET_FAMILY] * n_feat
    column_data["dataset_version"] = [LONGHORIZON_LABEL_DATASET_VERSION] * n_feat
    column_data["label_schema_version"] = [LONGHORIZON_LABEL_SCHEMA_VERSION] * n_feat
    column_data["source_feature_dataset_family"] = (
        [SOURCE_FEATURE_DATASET_FAMILY] * n_feat
    )
    column_data["source_feature_dataset_version"] = (
        [SOURCE_FEATURE_DATASET_VERSION] * n_feat
    )
    column_data["source_feature_manifest_sha256"] = (
        [lineage.source_feature_manifest_sha256] * n_feat
    )
    column_data["source_feature_parquet_sha256"] = (
        [lineage.source_feature_parquet_sha256] * n_feat
    )
    column_data["source_feature_successor_state_sha256"] = (
        [lineage.source_feature_successor_state_sha256] * n_feat
    )
    column_data["source_phase_4bm_j_gate_report_sha256"] = (
        [lineage.source_phase_4bm_j_gate_report_sha256] * n_feat
    )
    column_data["source_normalized_manifest_sha256"] = (
        [lineage.source_normalized_manifest_sha256] * n_feat
    )
    column_data["source_raw_manifest_sha256"] = (
        [lineage.source_raw_manifest_sha256] * n_feat
    )
    column_data["symbol"] = [symbol] * n_feat
    column_data["utc_date"] = [utc_date] * n_feat
    column_data["row_index"] = feat_row_index
    column_data["agg_trade_id"] = feat_agg_id
    column_data["feature_timestamp_ms"] = feat_ts_ms
    column_data["source_transact_time_ms"] = feat_src_ts_ms
    column_data["label_config_hash"] = [lineage.label_config_hash] * n_feat

    for label in LONGHORIZON_HORIZONS:
        column_data[f"forward_log_return_{label}"] = forward_log_return[label]
    for label in LONGHORIZON_HORIZONS:
        column_data[f"forward_direction_{label}"] = forward_direction[label]
    for label in LONGHORIZON_HORIZONS:
        column_data[f"reference_row_index_{label}"] = reference_row_index[label]
        column_data[f"reference_timestamp_ms_{label}"] = reference_timestamp_ms[label]
        column_data[f"horizon_censored_flag_{label}"] = horizon_censored_flag[label]
    column_data["label_invalid_price_flag"] = label_invalid_price_flag
    column_data["label_any_censored_flag"] = label_any_censored_flag

    missing = [c for c in LONGHORIZON_LABEL_SCHEMA if c not in column_data]
    if missing:
        raise LabelSchemaErrorV002(f"missing label columns: {missing!r}")

    ordered_data = {col: column_data[col] for col in LONGHORIZON_LABEL_SCHEMA}
    table = pa.Table.from_pydict(ordered_data, schema=schema)
    if tuple(table.column_names) != LONGHORIZON_LABEL_SCHEMA:
        raise LabelSchemaErrorV002(
            "constructed table column order diverged from LONGHORIZON_LABEL_SCHEMA"
        )
    if table.num_rows != n_feat:
        raise LabelComputationErrorV002(
            f"constructed table row count {table.num_rows} != feature row count {n_feat}"
        )

    non_lineage = (
        ("label_config_hash",)
        + tuple(LONGHORIZON_LABEL_NAMES)
        + tuple(LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES)
    )
    schema_non_lineage = LONGHORIZON_LABEL_SCHEMA[
        len(LONGHORIZON_LABEL_SCHEMA) - len(non_lineage) :
    ]
    if schema_non_lineage != non_lineage:
        raise LabelSchemaErrorV002(
            "non-lineage columns diverged from "
            "(label_config_hash,) + LONGHORIZON_LABEL_NAMES + "
            "LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES"
        )

    summary = LongHorizonLabelSummary(
        utc_date=utc_date,
        row_count=n_feat,
        invalid_price_row_count=invalid_price_count,
        censored_per_horizon=dict(censored_per_horizon),
    )
    return table, summary


# ---------------------------------------------------------------------------
# Research-namespace atomic writer (gitignored data/research/microstructure/)
# ---------------------------------------------------------------------------

_RESEARCH_PARTS = ("data", "research", "microstructure")


def _assert_under_research_microstructure(path: Path, *, label: str) -> None:
    """Fail closed unless *path* resolves under data/research/microstructure/."""
    if not isinstance(path, Path):
        raise LabelComputationErrorV002(f"{label} must be a pathlib.Path")
    resolved = path.resolve()
    parts = resolved.parts
    ok = any(
        parts[i : i + len(_RESEARCH_PARTS)] == _RESEARCH_PARTS
        for i in range(len(parts) - len(_RESEARCH_PARTS) + 1)
    )
    if not ok:
        raise LabelComputationErrorV002(
            f"{label} must resolve under data/research/microstructure/ (got {path!s})"
        )


def _atomic_write_parquet_research(
    path: Path, table: pa.Table, *, refuse_overwrite: bool = True
) -> tuple[str, int]:
    """Atomically write *table* as zstd Parquet under the research namespace."""
    import hashlib

    _assert_under_research_microstructure(path, label="longhorizon label parquet path")
    if refuse_overwrite and path.exists():
        raise LabelComputationErrorV002(f"refusing to overwrite existing file: {path}")
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment guard
        raise LabelComputationErrorV002("pyarrow is required") from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_str = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    tmp_path = Path(tmp_str)
    try:
        os.close(fd)
        pq.write_table(table, tmp_path, compression="zstd")
        h = hashlib.sha256()
        size = 0
        with tmp_path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
                size += len(chunk)
        with tmp_path.open("rb") as f, contextlib.suppress(OSError):
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
        return h.hexdigest(), size
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


def write_longhorizon_label_dataset(
    *,
    table: pa.Table,
    output_path: Path,
    write_sha256_sidecar: bool = True,
) -> tuple[Path, str, int, Path | None, str | None]:
    """Atomically write *table* to *output_path* + paired ``.sha256`` sidecar.

    Restricted to the gitignored ``data/research/microstructure/`` namespace;
    refuses to overwrite any finalised file. Returns
    ``(output_path, parquet_sha256, parquet_size, sidecar_path, sidecar_sha)``.
    """
    if tuple(table.column_names) != LONGHORIZON_LABEL_SCHEMA:
        raise LabelSchemaErrorV002(
            "table column order does not match LONGHORIZON_LABEL_SCHEMA"
        )
    output_sha, output_size = _atomic_write_parquet_research(
        output_path, table, refuse_overwrite=True
    )
    sidecar_path: Path | None = None
    sidecar_sha: str | None = None
    if write_sha256_sidecar:
        import hashlib

        sidecar_path = output_path.with_suffix(output_path.suffix + ".sha256")
        _assert_under_research_microstructure(sidecar_path, label="sidecar path")
        if sidecar_path.exists():
            raise LabelComputationErrorV002(f"refusing to overwrite sidecar: {sidecar_path}")
        body = f"{output_sha}  {output_path.name}\n".encode("ascii")
        sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_str = tempfile.mkstemp(
            prefix=sidecar_path.name + ".", suffix=".tmp", dir=sidecar_path.parent
        )
        tmp_path = Path(tmp_str)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(body)
                f.flush()
                with contextlib.suppress(OSError):
                    os.fsync(f.fileno())
            os.replace(tmp_path, sidecar_path)
        except BaseException:
            with contextlib.suppress(OSError):
                tmp_path.unlink()
            raise
        sidecar_sha = hashlib.sha256(body).hexdigest()
    return output_path, output_sha, output_size, sidecar_path, sidecar_sha
