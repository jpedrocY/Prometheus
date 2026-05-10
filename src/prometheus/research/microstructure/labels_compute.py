"""Phase 4bj-C aggTrades label computation kernel.

Implements the exact Phase 4bj-B v001 label schema:

- event-aligned output (one label row per feature row);
- causal future-reference: for horizon ``H`` the reference row is the
  latest source normalized aggTrade row with
  ``transact_time_ms <= feature_timestamp_ms + H_ms``;
- same-timestamp tie-break: largest ``row_index`` at that timestamp;
- right-edge censoring per horizon when the target timestamp exceeds
  the final source ``transact_time_ms`` for the day;
- Decimal parsing of price strings into Decimal, ratio in Decimal, and
  ``float64`` cast only at the natural-log step;
- ``forward_direction_H`` derived only from the sign of
  ``forward_log_return_H`` (``+1``, ``0``, ``-1``, or ``null``);
- ``label_invalid_price_flag = true`` when anchor or any reference
  price is ``<= 0`` (defensive; not expected in the Phase 4bd source);
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
  ``data/microstructure/labels/`` and
  ``data/microstructure/manifests/`` namespaces;
- never mutates the source feature parquet, feature manifest, Phase
  4bi-B feature-family gate report, Phase 4bi-D successor-state JSON,
  normalized parquet, original derived manifest, raw manifest, or
  raw zip.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from decimal import Decimal, getcontext
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .labels_io import (
    atomic_write_label_parquet,
    write_label_sha256_sidecar,
)
from .labels_schema import (
    LABEL_DATASET_FAMILY_V001,
    LABEL_DATASET_VERSION_V001,
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_V001,
    LABEL_SCHEMA_VERSION_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
    SOURCE_FEATURE_DATASET_FAMILY_V001,
    SOURCE_FEATURE_DATASET_VERSION_V001,
    LabelSchemaError,
    assert_no_forbidden_label_substrings,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    import numpy as np
    import pyarrow as pa


# Ensure Decimal context is wide enough for any aggTrade price string we
# encounter. Anchor and reference prices are parsed exactly, divided in
# Decimal, then cast to ``float64`` only for the natural-log step.
getcontext().prec = 50


class LabelComputationError(RuntimeError):
    """Raised when the Phase 4bj-C label kernel fails closed."""


@dataclass(frozen=True)
class LabelLineage:
    """Lineage SHAs threaded into every output row and the label manifest."""

    source_feature_manifest_sha256: str
    source_feature_parquet_sha256: str
    source_feature_successor_state_sha256: str
    source_phase_4bi_b_gate_report_sha256: str
    source_normalized_parquet_sha256: str
    label_config_hash: str


@dataclass(frozen=True)
class LabelComputationSummary:
    """Per-run summary of computed labels."""

    row_count: int
    invalid_price_row_count: int
    censored_per_horizon: dict[str, int]


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------


def compute_aggtrade_labels_v001(
    *,
    feature_table: pa.Table,
    normalized_table: pa.Table,
    symbol: str,
    utc_date: str,
    lineage: LabelLineage,
) -> tuple[pa.Table, LabelComputationSummary]:
    """Compute the 39-column label table from feature + normalized inputs.

    The returned :class:`pa.Table` is in canonical column order
    (:data:`LABEL_SCHEMA_V001`) with the 17 lineage / identity /
    metadata columns first, then the 8 label columns, then the 14
    support columns. The kernel never reads or computes any forbidden
    quantity (PnL, MFE, MAE, R-multiple, etc.).
    """
    import numpy as np
    import pyarrow as pa

    assert_no_forbidden_label_substrings(LABEL_SCHEMA_V001)

    # --- 1. Validate feature table shape and per-row alignment ---
    feat_names = tuple(feature_table.column_names)
    if "row_index" not in feat_names:
        raise LabelComputationError("feature_table must contain row_index")
    if "agg_trade_id" not in feat_names:
        raise LabelComputationError("feature_table must contain agg_trade_id")
    if "feature_timestamp_ms" not in feat_names:
        raise LabelComputationError("feature_table must contain feature_timestamp_ms")
    if "source_transact_time_ms" not in feat_names:
        raise LabelComputationError(
            "feature_table must contain source_transact_time_ms"
        )
    n_feat = feature_table.num_rows
    if n_feat <= 0:
        raise LabelComputationError("feature_table must have > 0 rows")

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
        raise LabelComputationError(
            "feature_table row_index must equal np.arange(n_feat)"
        )
    if not np.array_equal(feat_ts_ms, feat_src_ts_ms):
        raise LabelComputationError(
            "feature feature_timestamp_ms must equal source_transact_time_ms per row"
        )

    # --- 2. Validate normalized table shape and per-row alignment ---
    norm_names = tuple(normalized_table.column_names)
    for req in (
        "row_index",
        "agg_trade_id",
        "transact_time_ms",
        "price",
        "symbol",
        "utc_date",
    ):
        if req not in norm_names:
            raise LabelComputationError(
                f"normalized_table must contain column {req!r}"
            )
    n_norm = normalized_table.num_rows
    if n_norm != n_feat:
        raise LabelComputationError(
            f"normalized_table row count {n_norm} != feature_table row count {n_feat}"
        )

    norm_row_index = (
        normalized_table.column("row_index")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
    )
    norm_agg_id = (
        normalized_table.column("agg_trade_id")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
    )
    norm_ts_ms = (
        normalized_table.column("transact_time_ms")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64)
    )
    norm_prices: list[str] = normalized_table.column("price").to_pylist()

    if not np.array_equal(norm_row_index, np.arange(n_norm, dtype=np.int64)):
        raise LabelComputationError(
            "normalized_table row_index must equal np.arange(n_norm)"
        )
    if not np.array_equal(norm_agg_id, feat_agg_id):
        raise LabelComputationError(
            "normalized_table agg_trade_id must equal feature_table agg_trade_id "
            "per row"
        )
    if not np.array_equal(norm_ts_ms, feat_src_ts_ms):
        raise LabelComputationError(
            "normalized_table transact_time_ms must equal feature_table "
            "source_transact_time_ms per row"
        )
    if n_norm > 1 and not np.all(norm_ts_ms[1:] >= norm_ts_ms[:-1]):
        raise LabelComputationError(
            "normalized_table transact_time_ms must be non-decreasing"
        )

    # --- 3. Parse Decimal anchor prices and build float64 helper view ---
    anchor_decimal: list[Decimal] = []
    for s in norm_prices:
        try:
            anchor_decimal.append(Decimal(s))
        except (ArithmeticError, ValueError) as exc:
            raise LabelComputationError(
                f"non-Decimal-parsable price encountered: {s!r}"
            ) from exc

    # --- 4. Pre-compute per-horizon reference indices via searchsorted ---
    final_ts = int(norm_ts_ms[-1])
    horizon_reference_idx: dict[str, np.ndarray] = {}
    horizon_censored_mask: dict[str, np.ndarray] = {}
    for label, h_ms in zip(LABEL_HORIZONS_V001, LABEL_HORIZON_MS_V001, strict=True):
        target_ts = feat_ts_ms + np.int64(h_ms)
        censored = target_ts > final_ts
        # ``np.searchsorted(side='right')`` returns the insertion index
        # such that ``norm_ts_ms[insert-1] <= target_ts``. We then back
        # off to the largest row at exactly that timestamp (which is
        # exactly ``insert - 1`` because ``row_index`` is the canonical
        # within-timestamp tiebreaker for the normalized parquet).
        insert = np.searchsorted(norm_ts_ms, target_ts, side="right").astype(np.int64)
        ref_idx = insert - 1
        ref_idx[censored] = -1
        # Defensive: a non-censored target must produce a valid ref_idx
        # in ``[0, n_norm - 1]``.
        valid_mask = ~censored
        if np.any(valid_mask) and np.any(ref_idx[valid_mask] < 0):
            raise LabelComputationError(
                f"horizon {label}: non-censored target produced negative ref_idx"
            )
        horizon_reference_idx[label] = ref_idx
        horizon_censored_mask[label] = censored

    # --- 5. Compute labels per row ---
    forward_log_return: dict[str, list[float | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V001
    }
    forward_direction: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V001
    }
    reference_row_index: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V001
    }
    reference_timestamp_ms: dict[str, list[int | None]] = {
        label: [None] * n_feat for label in LABEL_HORIZONS_V001
    }
    horizon_censored_flag: dict[str, list[bool]] = {
        label: [False] * n_feat for label in LABEL_HORIZONS_V001
    }
    label_invalid_price_flag = [False] * n_feat
    label_any_censored_flag = [False] * n_feat

    invalid_price_count = 0
    censored_per_horizon: dict[str, int] = dict.fromkeys(LABEL_HORIZONS_V001, 0)

    for i in range(n_feat):
        anchor_price = anchor_decimal[i]
        anchor_invalid = anchor_price <= 0
        if anchor_invalid:
            label_invalid_price_flag[i] = True
            invalid_price_count += 1

        any_censored = False
        for label in LABEL_HORIZONS_V001:
            censored_arr = horizon_censored_mask[label]
            if bool(censored_arr[i]):
                horizon_censored_flag[label][i] = True
                any_censored = True
                censored_per_horizon[label] += 1
                # forward_log_return / forward_direction /
                # reference_row_index / reference_timestamp_ms remain
                # None per their initialised values.
                continue

            ref_idx_arr = horizon_reference_idx[label]
            ref_idx = int(ref_idx_arr[i])
            ref_price = anchor_decimal[ref_idx]
            reference_row_index[label][i] = ref_idx
            reference_timestamp_ms[label][i] = int(norm_ts_ms[ref_idx])

            ref_invalid = ref_price <= 0
            if ref_invalid:
                if not label_invalid_price_flag[i]:
                    label_invalid_price_flag[i] = True
                    invalid_price_count += 1
                # Leave forward_log_return / forward_direction as None.
                continue
            if anchor_invalid:
                # Anchor invalid implies forward labels are null for
                # every horizon, but support columns are still populated
                # with the reference info we just computed.
                continue

            ratio = ref_price / anchor_price
            log_ret = math.log(float(ratio))
            if not math.isfinite(log_ret):
                # Defensive: a degenerate ratio (extremely small / large)
                # could produce a non-finite log under float64. Treat as
                # invalid price to keep the null/censoring contract
                # intact rather than emit NaN/inf.
                if not label_invalid_price_flag[i]:
                    label_invalid_price_flag[i] = True
                    invalid_price_count += 1
                continue
            forward_log_return[label][i] = log_ret
            if log_ret > 0.0:
                forward_direction[label][i] = 1
            elif log_ret < 0.0:
                forward_direction[label][i] = -1
            else:
                forward_direction[label][i] = 0

        if any_censored:
            label_any_censored_flag[i] = True

    # --- 6. Build pyarrow schema in canonical column order ---
    if tuple(LABEL_NAMES_V001).count("forward_log_return_1s") != 1:
        raise LabelSchemaError("LABEL_NAMES_V001 invariant broken")

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
        "source_phase_4bi_b_gate_report_sha256",
        "symbol",
        "utc_date",
        "source_normalized_parquet_sha256",
        "label_config_hash",
    }
    nullable_int64_cols = {f"reference_row_index_{label}" for label in LABEL_HORIZONS_V001}
    nullable_int64_cols.update(
        {f"reference_timestamp_ms_{label}" for label in LABEL_HORIZONS_V001}
    )
    nullable_float_cols = {f"forward_log_return_{label}" for label in LABEL_HORIZONS_V001}
    nullable_int8_cols = {f"forward_direction_{label}" for label in LABEL_HORIZONS_V001}
    bool_cols = {f"horizon_censored_flag_{label}" for label in LABEL_HORIZONS_V001}
    bool_cols.update({"label_invalid_price_flag", "label_any_censored_flag"})

    schema_fields: list[pa.Field] = []
    for col in LABEL_SCHEMA_V001:
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
            raise LabelSchemaError(f"unclassified label column {col!r}")
    schema = pa.schema(schema_fields)
    if tuple(schema.names) != LABEL_SCHEMA_V001:
        raise LabelSchemaError(
            "constructed schema does not match LABEL_SCHEMA_V001 column order"
        )

    # --- 7. Assemble column data ---
    column_data: dict[str, Any] = {}
    column_data["dataset_family"] = [LABEL_DATASET_FAMILY_V001] * n_feat
    column_data["dataset_version"] = [LABEL_DATASET_VERSION_V001] * n_feat
    column_data["label_schema_version"] = [LABEL_SCHEMA_VERSION_V001] * n_feat
    column_data["source_feature_dataset_family"] = (
        [SOURCE_FEATURE_DATASET_FAMILY_V001] * n_feat
    )
    column_data["source_feature_dataset_version"] = (
        [SOURCE_FEATURE_DATASET_VERSION_V001] * n_feat
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
    column_data["source_phase_4bi_b_gate_report_sha256"] = (
        [lineage.source_phase_4bi_b_gate_report_sha256] * n_feat
    )
    column_data["symbol"] = [symbol] * n_feat
    column_data["utc_date"] = [utc_date] * n_feat
    column_data["row_index"] = feat_row_index
    column_data["agg_trade_id"] = feat_agg_id
    column_data["feature_timestamp_ms"] = feat_ts_ms
    column_data["source_transact_time_ms"] = feat_src_ts_ms
    column_data["source_normalized_parquet_sha256"] = (
        [lineage.source_normalized_parquet_sha256] * n_feat
    )
    column_data["label_config_hash"] = [lineage.label_config_hash] * n_feat

    for label in LABEL_HORIZONS_V001:
        column_data[f"forward_log_return_{label}"] = forward_log_return[label]
    for label in LABEL_HORIZONS_V001:
        column_data[f"forward_direction_{label}"] = forward_direction[label]
    for label in LABEL_HORIZONS_V001:
        column_data[f"reference_row_index_{label}"] = reference_row_index[label]
        column_data[f"reference_timestamp_ms_{label}"] = reference_timestamp_ms[label]
        column_data[f"horizon_censored_flag_{label}"] = horizon_censored_flag[label]
    column_data["label_invalid_price_flag"] = label_invalid_price_flag
    column_data["label_any_censored_flag"] = label_any_censored_flag

    # Defensive: ensure every canonical column has been populated.
    missing = [c for c in LABEL_SCHEMA_V001 if c not in column_data]
    if missing:
        raise LabelSchemaError(f"missing label columns: {missing!r}")

    ordered_data = {col: column_data[col] for col in LABEL_SCHEMA_V001}
    table = pa.Table.from_pydict(ordered_data, schema=schema)
    if tuple(table.column_names) != LABEL_SCHEMA_V001:
        raise LabelSchemaError(
            "constructed table column order diverged from LABEL_SCHEMA_V001"
        )
    if table.num_rows != n_feat:
        raise LabelComputationError(
            f"constructed table row count {table.num_rows} != feature row count {n_feat}"
        )

    # Strict support-column sanity: union of LABEL_NAMES + support must
    # cover the non-lineage columns of LABEL_SCHEMA_V001.
    non_lineage = tuple(LABEL_NAMES_V001) + tuple(LABEL_SUPPORT_COLUMN_NAMES_V001)
    schema_non_lineage = LABEL_SCHEMA_V001[len(LABEL_SCHEMA_V001) - len(non_lineage) :]
    if schema_non_lineage != non_lineage:
        raise LabelSchemaError(
            "non-lineage columns diverged from LABEL_NAMES_V001 + "
            "LABEL_SUPPORT_COLUMN_NAMES_V001"
        )

    summary = LabelComputationSummary(
        row_count=n_feat,
        invalid_price_row_count=invalid_price_count,
        censored_per_horizon=dict(censored_per_horizon),
    )
    return table, summary


def write_label_dataset_v001(
    *,
    table: pa.Table,
    output_path: Path,
    write_sha256_sidecar: bool = True,
) -> tuple[Path, str, int, Path | None, str | None]:
    """Atomically write *table* to *output_path*.

    Returns ``(output_path, output_sha256, output_size,
    sidecar_path_or_None, sidecar_sha_or_None)``. The output and
    sidecar paths are restricted to
    ``data/microstructure/labels/`` and the writer refuses to
    overwrite a pre-existing finalised file.
    """
    if tuple(table.column_names) != LABEL_SCHEMA_V001:
        raise LabelSchemaError(
            "table column order does not match LABEL_SCHEMA_V001"
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
    "LabelComputationError",
    "LabelComputationSummary",
    "LabelLineage",
    "compute_aggtrade_labels_v001",
    "write_label_dataset_v001",
]
