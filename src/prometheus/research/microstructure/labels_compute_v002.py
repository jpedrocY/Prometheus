"""Phase 4bm-O multi-day v002 aggTrades label computation kernel.

Implements the exact Phase 4bm-N v002 label schema:

- event-aligned output (one label row per feature row, per UTC day);
- causal future-reference allowed to cross UTC day boundaries **only**
  within the v002 90-day envelope: for horizon ``H`` the reference row
  is the largest-row-index normalized aggTrades row across the v002
  envelope with ``transact_time_ms <= feature_timestamp_ms + H_ms``;
- same-timestamp tie-break: largest ``row_index`` at that timestamp
  inside its per-day source parquet;
- envelope-terminal censoring per horizon when
  ``target_timestamp_ms > envelope_terminal_unix_ms`` (no per-day
  censoring; horizons may cross UTC day boundaries inside the 90-day
  envelope);
- Decimal parsing of price strings into ``Decimal``, ratio in
  ``Decimal``, and ``float64`` cast only at the natural-log step;
- ``forward_direction_H`` derived only from the sign of
  ``forward_log_return_H`` (``+1``, ``0``, ``-1``, or ``null``);
- ``label_invalid_price_flag = true`` when anchor or any reference
  price is ``<= 0`` (defensive; not expected in the v002 envelope
  given Phase 4bl-D-R + Phase 4bm-D PASS evidence);
- ``label_any_censored_flag = OR(horizon_censored_flag_*)``;
- no NaN / inf in any output column.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute strategy signals, returns into the future beyond
  the locked horizons, alpha, edge, prediction, model score, decision,
  strategy, PnL, MFE, MAE, R-multiple, equity, position, liquidation,
  funding, OI, order book, or mark price proxies;
- never reads or writes any artefact outside the gitignored
  ``data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/``
  and ``data/microstructure/manifests/`` namespaces;
- never mutates the source feature parquet, feature manifest, Phase
  4bm-J feature-family gate report, Phase 4bm-L successor-state JSON,
  normalized parquet, v002 derived multi-day index manifest, v002 raw
  manifest, raw zips, Phase 4bm-D / 4bm-F / 4bl-D-R / 4bl-E artefacts,
  any prior v001 label artefact, or any other on-disk governance
  artefact.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from decimal import Decimal, getcontext
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .labels_io import (
    atomic_write_label_parquet,
    write_label_sha256_sidecar,
)
from .labels_schema_v002 import (
    LABEL_DATASET_FAMILY_V002,
    LABEL_DATASET_VERSION_V002,
    LABEL_HORIZON_MS_V002,
    LABEL_HORIZONS_V002,
    LABEL_NAMES_V002,
    LABEL_SCHEMA_V002,
    LABEL_SCHEMA_VERSION_V002,
    LABEL_SUPPORT_COLUMN_NAMES_V002,
    SOURCE_FEATURE_DATASET_FAMILY_V002,
    SOURCE_FEATURE_DATASET_VERSION_V002,
    LabelSchemaErrorV002,
    assert_no_forbidden_label_substrings_v002,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    import pyarrow as pa


# Ensure Decimal context is wide enough for any aggTrade price string we
# encounter. Anchor and reference prices are parsed exactly, divided in
# Decimal, then cast to ``float64`` only for the natural-log step.
getcontext().prec = 50


class LabelComputationErrorV002(RuntimeError):
    """Raised when the Phase 4bm-O label kernel fails closed."""


@dataclass(frozen=True)
class LabelLineageV002:
    """Lineage SHAs threaded into every output row and the label manifest."""

    source_feature_manifest_sha256: str
    source_feature_parquet_sha256: str
    source_feature_successor_state_sha256: str
    source_phase_4bm_j_gate_report_sha256: str
    source_normalized_manifest_sha256: str
    source_raw_manifest_sha256: str
    label_config_hash: str


@dataclass(frozen=True)
class NormalizedDayRef:
    """One per-day normalized table loaded into reference arrays.

    All arrays are aligned 1:1 with the day's normalized parquet rows;
    ``row_index`` is implicit and equals ``np.arange(n)``.
    """

    utc_date: str
    transact_time_ms: Any  # np.ndarray[int64]
    prices_decimal: list[Decimal]
    agg_trade_id: Any  # np.ndarray[int64]


@dataclass(frozen=True)
class LabelComputationSummaryV002:
    """Per-run summary of computed labels for a single per-day output."""

    utc_date: str
    row_count: int
    invalid_price_row_count: int
    censored_per_horizon: dict[str, int]


@dataclass
class LabelMultiDaySummaryV002:
    """Aggregate summary across all per-day label computations in a run."""

    total_row_count: int = 0
    total_invalid_price_row_count: int = 0
    censored_per_horizon: dict[str, int] = field(
        default_factory=lambda: dict.fromkeys(LABEL_HORIZONS_V002, 0)
    )

    def absorb(self, day_summary: LabelComputationSummaryV002) -> None:
        """Fold *day_summary* into the running aggregate."""
        self.total_row_count += day_summary.row_count
        self.total_invalid_price_row_count += day_summary.invalid_price_row_count
        for h in LABEL_HORIZONS_V002:
            self.censored_per_horizon[h] += day_summary.censored_per_horizon[h]


# ---------------------------------------------------------------------------
# Normalized-day loader
# ---------------------------------------------------------------------------


def load_normalized_day_ref(*, parquet_path: Path) -> NormalizedDayRef:
    """Load a single day's normalized parquet into reference arrays.

    Reads only the columns required by the label kernel
    (``transact_time_ms``, ``price``, ``agg_trade_id``, ``utc_date``,
    ``row_index``) and validates the row contract:

    - ``row_index == np.arange(n)``
    - ``transact_time_ms`` is non-decreasing
    - all ``utc_date`` values are equal
    - prices parse cleanly to ``Decimal``
    """
    import numpy as np
    import pyarrow.parquet as pq

    if not isinstance(parquet_path, Path):
        raise LabelComputationErrorV002(
            "parquet_path must be a pathlib.Path"
        )
    if not parquet_path.exists():
        raise LabelComputationErrorV002(
            f"normalized parquet missing: {parquet_path}"
        )
    table = pq.read_table(
        parquet_path,
        columns=["transact_time_ms", "price", "agg_trade_id", "utc_date", "row_index"],
    )
    n = table.num_rows
    if n <= 0:
        raise LabelComputationErrorV002(
            f"normalized parquet {parquet_path} has zero rows"
        )
    row_index = (
        table.column("row_index").to_numpy(zero_copy_only=False).astype(np.int64)
    )
    if not np.array_equal(row_index, np.arange(n, dtype=np.int64)):
        raise LabelComputationErrorV002(
            f"normalized parquet {parquet_path} row_index != np.arange(n)"
        )
    transact_time_ms = (
        table.column("transact_time_ms")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
    )
    if n > 1 and not bool(np.all(transact_time_ms[1:] >= transact_time_ms[:-1])):
        raise LabelComputationErrorV002(
            f"normalized parquet {parquet_path} transact_time_ms not non-decreasing"
        )
    agg_trade_id = (
        table.column("agg_trade_id")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
    )
    utc_date_values = table.column("utc_date").to_pylist()
    if len(utc_date_values) == 0:
        raise LabelComputationErrorV002(
            f"normalized parquet {parquet_path} missing utc_date values"
        )
    first_date = utc_date_values[0]
    if not all(v == first_date for v in utc_date_values):
        raise LabelComputationErrorV002(
            f"normalized parquet {parquet_path} contains multiple utc_date values"
        )
    raw_prices: list[str] = table.column("price").to_pylist()
    prices_decimal: list[Decimal] = []
    for s in raw_prices:
        try:
            prices_decimal.append(Decimal(s))
        except (ArithmeticError, ValueError) as exc:
            raise LabelComputationErrorV002(
                f"non-Decimal-parsable price encountered in {parquet_path}: {s!r}"
            ) from exc
    return NormalizedDayRef(
        utc_date=first_date,
        transact_time_ms=transact_time_ms,
        prices_decimal=prices_decimal,
        agg_trade_id=agg_trade_id,
    )


# ---------------------------------------------------------------------------
# Per-day kernel (cross-day reference allowed via ``next_day``)
# ---------------------------------------------------------------------------


def compute_aggtrade_labels_v002_for_day(
    *,
    feature_table: pa.Table,
    current_day: NormalizedDayRef,
    next_day: NormalizedDayRef | None,
    envelope_terminal_unix_ms: int,
    symbol: str,
    utc_date: str,
    lineage: LabelLineageV002,
) -> tuple[pa.Table, LabelComputationSummaryV002]:
    """Compute the 40-column v002 label table for one UTC day.

    The returned :class:`pa.Table` is in canonical column order
    (:data:`LABEL_SCHEMA_V002`).

    Cross-day reference is resolved against *next_day* only when the
    target timestamp falls past the last ``transact_time_ms`` of
    *current_day*; this captures every cross-day case within the v002
    envelope because horizon offsets are bounded by ``60_000`` ms and
    each per-day normalized parquet covers ``86_400_000`` ms.
    """
    import numpy as np
    import pyarrow as pa

    assert_no_forbidden_label_substrings_v002(LABEL_SCHEMA_V002)

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
            raise LabelComputationErrorV002(
                f"feature_table must contain {col!r}"
            )
    n_feat = feature_table.num_rows
    if n_feat <= 0:
        raise LabelComputationErrorV002("feature_table must have > 0 rows")

    feat_row_index = (
        feature_table.column("row_index").to_numpy(zero_copy_only=False).astype(np.int64)
    )
    feat_agg_id = (
        feature_table.column("agg_trade_id")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
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
        raise LabelComputationErrorV002(
            "envelope_terminal_unix_ms must be positive"
        )
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
            raise LabelComputationErrorV002(
                f"next_day {next_day.utc_date} has zero rows"
            )

    # --- 4. Per-horizon target timestamps and reference arrays ---
    forward_log_return: dict[str, list[float | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V002
    }
    forward_direction: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V002
    }
    reference_row_index: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V002
    }
    reference_timestamp_ms: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V002
    }
    horizon_censored_flag: dict[str, list[bool]] = {
        label: [False] * n_feat for label in LABEL_HORIZONS_V002
    }
    label_invalid_price_flag = [False] * n_feat
    label_any_censored_flag = [False] * n_feat
    invalid_price_count = 0
    censored_per_horizon: dict[str, int] = dict.fromkeys(LABEL_HORIZONS_V002, 0)

    # Pre-compute per-horizon reference indices via vectorised
    # ``searchsorted`` on the current day's transact_time_ms (and on
    # next_day's transact_time_ms when needed). The cross-day branch
    # supersedes the current-day branch when next_day yields a valid
    # reference (any next_day row with ts <= target is globally later
    # than every current_day row, because day boundaries do not
    # overlap and rows are sorted by ts then row_index).
    cur_ts = current_day.transact_time_ms
    per_horizon_cur_ref_idx: dict[str, Any] = {}
    per_horizon_next_ref_idx: dict[str, Any] = {}
    per_horizon_censored_mask: dict[str, Any] = {}
    for h_label, h_ms in zip(
        LABEL_HORIZONS_V002, LABEL_HORIZON_MS_V002, strict=True
    ):
        target_ts = feat_ts_ms + np.int64(h_ms)
        censored = target_ts > np.int64(envelope_terminal_unix_ms)
        # Current-day candidate: searchsorted right-1 (always >= 0 for
        # non-censored anchors because target >= anchor_ts >= cur_ts[0]).
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
        for h_label in LABEL_HORIZONS_V002:
            censored_arr = per_horizon_censored_mask[h_label]
            if bool(censored_arr[i]):
                horizon_censored_flag[h_label][i] = True
                any_censored = True
                censored_per_horizon[h_label] += 1
                continue

            # Determine reference: prefer next_day if it has a valid
            # candidate (it is strictly later than every current_day
            # row), else use current_day.
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
                    # Defensive: target was not censored and anchor is
                    # in current day, so we must always find a current-
                    # day reference. Treat as invalid price (null
                    # label, flag set) rather than emit garbage.
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
    nullable_int64_cols = {f"reference_row_index_{label}" for label in LABEL_HORIZONS_V002}
    nullable_int64_cols.update(
        {f"reference_timestamp_ms_{label}" for label in LABEL_HORIZONS_V002}
    )
    nullable_float_cols = {f"forward_log_return_{label}" for label in LABEL_HORIZONS_V002}
    nullable_int8_cols = {f"forward_direction_{label}" for label in LABEL_HORIZONS_V002}
    bool_cols = {f"horizon_censored_flag_{label}" for label in LABEL_HORIZONS_V002}
    bool_cols.update({"label_invalid_price_flag", "label_any_censored_flag"})

    schema_fields: list[pa.Field] = []
    for col in LABEL_SCHEMA_V002:
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
    if tuple(schema.names) != LABEL_SCHEMA_V002:
        raise LabelSchemaErrorV002(
            "constructed schema does not match LABEL_SCHEMA_V002 column order"
        )

    # --- 7. Assemble column data ---
    column_data: dict[str, Any] = {}
    column_data["dataset_family"] = [LABEL_DATASET_FAMILY_V002] * n_feat
    column_data["dataset_version"] = [LABEL_DATASET_VERSION_V002] * n_feat
    column_data["label_schema_version"] = [LABEL_SCHEMA_VERSION_V002] * n_feat
    column_data["source_feature_dataset_family"] = (
        [SOURCE_FEATURE_DATASET_FAMILY_V002] * n_feat
    )
    column_data["source_feature_dataset_version"] = (
        [SOURCE_FEATURE_DATASET_VERSION_V002] * n_feat
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

    for label in LABEL_HORIZONS_V002:
        column_data[f"forward_log_return_{label}"] = forward_log_return[label]
    for label in LABEL_HORIZONS_V002:
        column_data[f"forward_direction_{label}"] = forward_direction[label]
    for label in LABEL_HORIZONS_V002:
        column_data[f"reference_row_index_{label}"] = reference_row_index[label]
        column_data[f"reference_timestamp_ms_{label}"] = reference_timestamp_ms[label]
        column_data[f"horizon_censored_flag_{label}"] = horizon_censored_flag[label]
    column_data["label_invalid_price_flag"] = label_invalid_price_flag
    column_data["label_any_censored_flag"] = label_any_censored_flag

    missing = [c for c in LABEL_SCHEMA_V002 if c not in column_data]
    if missing:
        raise LabelSchemaErrorV002(f"missing label columns: {missing!r}")

    ordered_data = {col: column_data[col] for col in LABEL_SCHEMA_V002}
    table = pa.Table.from_pydict(ordered_data, schema=schema)
    if tuple(table.column_names) != LABEL_SCHEMA_V002:
        raise LabelSchemaErrorV002(
            "constructed table column order diverged from LABEL_SCHEMA_V002"
        )
    if table.num_rows != n_feat:
        raise LabelComputationErrorV002(
            f"constructed table row count {table.num_rows} != "
            f"feature row count {n_feat}"
        )

    non_lineage = (
        ("label_config_hash",)
        + tuple(LABEL_NAMES_V002)
        + tuple(LABEL_SUPPORT_COLUMN_NAMES_V002)
    )
    schema_non_lineage = LABEL_SCHEMA_V002[len(LABEL_SCHEMA_V002) - len(non_lineage) :]
    if schema_non_lineage != non_lineage:
        raise LabelSchemaErrorV002(
            "non-lineage columns diverged from "
            "(label_config_hash,) + LABEL_NAMES_V002 + LABEL_SUPPORT_COLUMN_NAMES_V002"
        )

    summary = LabelComputationSummaryV002(
        utc_date=utc_date,
        row_count=n_feat,
        invalid_price_row_count=invalid_price_count,
        censored_per_horizon=dict(censored_per_horizon),
    )
    return table, summary


def write_label_dataset_v002(
    *,
    table: pa.Table,
    output_path: Path,
    write_sha256_sidecar: bool = True,
) -> tuple[Path, str, int, Path | None, str | None]:
    """Atomically write *table* to *output_path* as Parquet + paired sidecar.

    Returns ``(output_path, parquet_sha256, parquet_size,
    sidecar_path_or_None, sidecar_sha_or_None)``. Refuses to overwrite
    any pre-existing finalised file.
    """
    if tuple(table.column_names) != LABEL_SCHEMA_V002:
        raise LabelSchemaErrorV002(
            "table column order does not match LABEL_SCHEMA_V002"
        )
    output_sha, output_size = atomic_write_label_parquet(
        output_path, table, refuse_overwrite=True
    )
    sidecar_path: Path | None = None
    sidecar_sha: str | None = None
    if write_sha256_sidecar:
        sidecar_path = output_path.with_suffix(output_path.suffix + ".sha256")
        sidecar_sha, _ = write_label_sha256_sidecar(
            sidecar_path,
            target_filename=output_path.name,
            sha256_hex=output_sha,
            refuse_overwrite=True,
        )
    return output_path, output_sha, output_size, sidecar_path, sidecar_sha


__all__ = [
    "LabelComputationErrorV002",
    "LabelComputationSummaryV002",
    "LabelLineageV002",
    "LabelMultiDaySummaryV002",
    "NormalizedDayRef",
    "compute_aggtrade_labels_v002_for_day",
    "load_normalized_day_ref",
    "write_label_dataset_v002",
]
