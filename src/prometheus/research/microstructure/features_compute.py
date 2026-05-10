"""Phase 4bh aggTrades feature computation kernel.

This module implements the Phase 4bh-B locked feature schema:

- event-aligned output (one feature row per source aggTrade row);
- causal trailing windows ``(T - window_ms, T]`` with same-timestamp
  tie-break ``row_index <= R``;
- aggressive-side rule: ``is_buyer_maker = false`` -> aggressive buy;
- Decimal-as-string for raw quantity sums / aggressive quantities /
  imbalances and rolling quantity means;
- ``float64`` for aggressive flow ratios and log returns;
- 4 trailing windows only: 1s, 5s, 15s, 60s;
- 45 feature/quality columns (40 windowed + 3 time-context + 2 quality);
- 16 lineage / identity / metadata columns;
- 61-column total schema in canonical column order.

This module:

- does NOT compute labels, targets, signals, ML features, returns into
  the future, alpha, edge, prediction, model score, decision, strategy,
  PnL, MFE, MAE, R-multiple, equity, position, liquidation, funding,
  open-interest, order-book, or mark-price proxies;
- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- never assumes future bars are available; only rows ``j <= i`` (in
  canonical sort order) contribute to row ``i``'s features.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .features_io import (
    atomic_write_feature_parquet,
    write_feature_sha256_sidecar,
)
from .features_schema import (
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_V001,
    FEATURE_SCHEMA_VERSION,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    SOURCE_NORMALIZED_DATASET_FAMILY,
    SOURCE_NORMALIZED_DATASET_VERSION,
    FeatureComputationConfig,
    FeatureSchemaError,
    assert_no_forbidden_substrings,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    import numpy as np
    import pyarrow as pa


UTC_DAY_MS = 86_400_000


class FeatureComputationError(RuntimeError):
    """Raised when the Phase 4bh feature kernel fails closed."""


@dataclass(frozen=True)
class FeatureLineage:
    """Lineage SHAs threaded into every output row."""

    source_normalized_parquet_sha256: str
    source_normalized_manifest_sha256: str
    source_successor_state_sha256: str
    source_phase_4bf_gate_report_sha256: str
    feature_config_hash: str


@dataclass(frozen=True)
class FeatureComputationResult:
    """Result of one Phase 4bh feature run."""

    output_path: Path
    output_sha256: str
    output_size_bytes: int
    output_sidecar_path: Path
    output_sidecar_sha256: str
    row_count: int
    file_count: int
    column_count: int
    lineage_column_count: int
    feature_column_count: int
    feature_config_hash: str
    config: FeatureComputationConfig
    research_eligible_after: bool
    no_successor_authorization: bool


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _max_decimal_places(strings: Sequence[str]) -> int:
    """Return the maximum number of fractional decimal places across *strings*."""
    max_dp = 0
    for s in strings:
        if "." in s:
            dp = len(s.split(".", 1)[1])
            if dp > max_dp:
                max_dp = dp
    return max_dp


def _scale_decimal_string_to_int(s: str, scale_factor: int) -> int:
    """Convert a decimal string to a scaled int using stdlib :class:`Decimal`."""
    return int((Decimal(s) * scale_factor).to_integral_value())


def _format_int_as_decimal_string(value: int, max_dp: int) -> str:
    """Format a scaled integer back as a Decimal-as-string with *max_dp* decimals.

    For ``max_dp = 0`` returns the integer's :func:`str` representation.
    For ``max_dp > 0`` returns a fixed-point string with *max_dp* digits
    after the decimal point. Negative values get a leading minus sign.
    Returns ``"0"`` exactly when *value* is zero.
    """
    if value == 0:
        return "0"
    if max_dp == 0:
        return str(value)
    sign = "-" if value < 0 else ""
    abs_val = abs(value)
    base = 10**max_dp
    integer_part = abs_val // base
    fractional_part = abs_val % base
    return f"{sign}{integer_part}.{fractional_part:0{max_dp}d}"


def _format_mean_as_decimal_string(
    sum_int: int,
    count: int,
    max_dp: int,
    *,
    extra_precision_digits: int = 12,
) -> str:
    """Format ``sum_int / (count * 10**max_dp)`` as a fixed-point decimal string.

    The output has ``max_dp + extra_precision_digits`` digits after the
    decimal point. ``count`` must be > 0; the caller is responsible for
    short-circuiting the empty-window case to ``None``.
    """
    if count <= 0:
        raise FeatureComputationError("count must be positive for mean formatting")
    total_dp = max_dp + extra_precision_digits
    scaled_sum = sum_int * (10**extra_precision_digits)
    mean_int = scaled_sum // count
    return _format_int_as_decimal_string(mean_int, total_dp)


def _utc_day_start_ms(utc_date: str) -> int:
    """Return the UTC ms timestamp at midnight of *utc_date* (``YYYY-MM-DD``)."""
    day = datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(day.timestamp() * 1000)


def _assert_sorted_and_row_index_aligned(
    transact_time_ms: np.ndarray,
    row_index: np.ndarray,
) -> None:
    """Verify the canonical sort order ``(transact_time_ms ASC, row_index ASC)``.

    Phase 4bh requires the source normalized parquet to already be in
    canonical sort order with ``row_index[i] == i`` for every row. This
    is the contract Phase 4bd produces. We assert it explicitly here so
    that any departure fails closed before any feature is written.
    """
    n = transact_time_ms.shape[0]
    if row_index.shape[0] != n:
        raise FeatureComputationError("row_index and transact_time_ms shape mismatch")
    import numpy as np

    expected = np.arange(n, dtype=row_index.dtype)
    if not np.array_equal(row_index, expected):
        raise FeatureComputationError(
            "row_index column must equal np.arange(n) (canonical position)"
        )
    if n > 1 and not np.all(transact_time_ms[1:] >= transact_time_ms[:-1]):
        raise FeatureComputationError(
            "transact_time_ms must be non-decreasing in canonical sort order"
        )


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------


def compute_aggtrades_features(
    *,
    source_table: pa.Table,
    config: FeatureComputationConfig,
    lineage: FeatureLineage,
) -> pa.Table:
    """Compute the 61-column feature table from a normalized aggTrades table.

    The returned :class:`pa.Table` is in canonical column order
    (:data:`FEATURE_SCHEMA_V001`) with the lineage / identity /
    metadata columns first and the 45 feature / quality columns
    afterward. The feature kernel never reads or computes any forbidden
    quantity (labels, targets, future returns, etc.); column names are
    scanned against
    :data:`features_schema.FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS` before
    the table is constructed.
    """
    import numpy as np
    import pyarrow as pa

    # --- 1. Validate the source schema is the Phase 4bd 19-column shape ---
    expected_source_cols = (
        "dataset_family",
        "dataset_version",
        "source_dataset_family",
        "source_dataset_version",
        "symbol",
        "utc_date",
        "agg_trade_id",
        "price",
        "quantity",
        "first_trade_id",
        "last_trade_id",
        "transact_time_ms",
        "is_buyer_maker",
        "source_file_sha256",
        "source_manifest_sha256",
        "source_gate_report_id",
        "source_gate_report_sha256",
        "row_index",
        "normalization_schema_version",
    )
    if tuple(source_table.column_names) != expected_source_cols:
        raise FeatureComputationError(
            "source normalized parquet does not have the canonical Phase 4bd schema"
        )
    if source_table.num_rows == 0:
        raise FeatureComputationError(
            "source normalized parquet has zero rows; cannot compute features"
        )

    # --- 2. Pull symbol / utc_date / lineage constants from the first row ---
    symbol = source_table.column("symbol")[0].as_py()
    utc_date = source_table.column("utc_date")[0].as_py()
    if not isinstance(symbol, str) or not symbol:
        raise FeatureComputationError("source symbol must be a non-empty string")
    if not isinstance(utc_date, str) or len(utc_date) != 10:
        raise FeatureComputationError("source utc_date must be YYYY-MM-DD")
    src_family = source_table.column("source_dataset_family")[0].as_py()
    src_version = source_table.column("source_dataset_version")[0].as_py()
    if src_family != "microstructure_raw_aggtrades_v001":
        raise FeatureComputationError(
            "source_dataset_family is not 'microstructure_raw_aggtrades_v001'"
        )
    if src_version != "v001":
        raise FeatureComputationError("source_dataset_version is not 'v001'")

    # --- 3. Extract numpy arrays for the columns we need ---
    transact_time_ms = source_table.column("transact_time_ms").to_numpy(
        zero_copy_only=False
    ).astype(np.int64, copy=False)
    is_buyer_maker = source_table.column("is_buyer_maker").to_numpy(
        zero_copy_only=False
    ).astype(np.bool_, copy=False)
    row_index = source_table.column("row_index").to_numpy(
        zero_copy_only=False
    ).astype(np.int64, copy=False)
    agg_trade_id = source_table.column("agg_trade_id").to_numpy(
        zero_copy_only=False
    ).astype(np.int64, copy=False)
    price_strs: list[str] = source_table.column("price").to_pylist()
    quantity_strs: list[str] = source_table.column("quantity").to_pylist()

    # --- 4. Verify canonical sort order ---
    _assert_sorted_and_row_index_aligned(transact_time_ms, row_index)
    n = int(transact_time_ms.shape[0])

    # --- 5. Decimal-string -> int64 scaling for quantity ---
    max_dp_q = _max_decimal_places(quantity_strs)
    qty_scale = 10**max_dp_q
    qty_int = np.empty(n, dtype=np.int64)
    for i, s in enumerate(quantity_strs):
        qty_int[i] = _scale_decimal_string_to_int(s, qty_scale)
    if int(qty_int.min()) <= 0:
        raise FeatureComputationError(
            "quantity values must all be > 0 in the source normalized parquet"
        )
    aggressive_buy_mask = ~is_buyer_maker
    aggressive_sell_mask = is_buyer_maker
    qty_buy_int = np.where(aggressive_buy_mask, qty_int, 0)
    qty_sell_int = np.where(aggressive_sell_mask, qty_int, 0)
    cnt_buy = aggressive_buy_mask.astype(np.int64)
    cnt_sell = aggressive_sell_mask.astype(np.int64)

    # --- 6. Cumulative sums (prefix length n + 1; index 0 is zero) ---
    cum_qty = np.concatenate(([0], np.cumsum(qty_int, dtype=np.int64)))
    cum_buy_qty = np.concatenate(([0], np.cumsum(qty_buy_int, dtype=np.int64)))
    cum_sell_qty = np.concatenate(([0], np.cumsum(qty_sell_int, dtype=np.int64)))
    cum_buy_count = np.concatenate(([0], np.cumsum(cnt_buy, dtype=np.int64)))
    cum_sell_count = np.concatenate(([0], np.cumsum(cnt_sell, dtype=np.int64)))

    # --- 7. Float prices for log-return computation only ---
    price_float = np.empty(n, dtype=np.float64)
    for i, s in enumerate(price_strs):
        price_float[i] = float(s)
    if not np.all(np.isfinite(price_float)) or float(price_float.min()) <= 0.0:
        raise FeatureComputationError(
            "price values must all be finite and > 0 in the source normalized parquet"
        )

    # --- 8. Per-window aggregates ---
    n_indices = np.arange(n, dtype=np.int64)
    column_data: dict[str, list[Any] | np.ndarray] = {}

    for window_ms, label in zip(
        FEATURE_WINDOWS_MS_V001, FEATURE_WINDOW_LABELS_V001, strict=True
    ):
        threshold = transact_time_ms - np.int64(window_ms)
        lo_arr = np.searchsorted(transact_time_ms, threshold, side="right").astype(
            np.int64
        )
        window_count = (n_indices + 1) - lo_arr
        window_qty = cum_qty[n_indices + 1] - cum_qty[lo_arr]
        window_buy = cum_buy_qty[n_indices + 1] - cum_buy_qty[lo_arr]
        window_sell = cum_sell_qty[n_indices + 1] - cum_sell_qty[lo_arr]
        window_buy_count = cum_buy_count[n_indices + 1] - cum_buy_count[lo_arr]
        window_sell_count = cum_sell_count[n_indices + 1] - cum_sell_count[lo_arr]

        qty_sum_strs: list[str] = [
            "0" if int(window_count[i]) == 0
            else _format_int_as_decimal_string(int(window_qty[i]), max_dp_q)
            for i in range(n)
        ]
        qty_mean_strs: list[str | None] = [
            None if int(window_count[i]) == 0
            else _format_mean_as_decimal_string(
                int(window_qty[i]), int(window_count[i]), max_dp_q
            )
            for i in range(n)
        ]
        buy_sum_strs: list[str] = [
            "0" if int(window_buy_count[i]) == 0
            else _format_int_as_decimal_string(int(window_buy[i]), max_dp_q)
            for i in range(n)
        ]
        sell_sum_strs: list[str] = [
            "0" if int(window_sell_count[i]) == 0
            else _format_int_as_decimal_string(int(window_sell[i]), max_dp_q)
            for i in range(n)
        ]
        imbalance_strs: list[str] = [
            "0" if int(window_buy_count[i]) == 0 and int(window_sell_count[i]) == 0
            else _format_int_as_decimal_string(
                int(window_buy[i]) - int(window_sell[i]), max_dp_q
            )
            for i in range(n)
        ]
        denom_int = window_buy + window_sell
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(
                denom_int > 0,
                window_buy.astype(np.float64) / denom_int.astype(np.float64),
                np.nan,
            )
        ratio_list: list[float | None] = [
            None if not np.isfinite(ratio[i]) else float(ratio[i]) for i in range(n)
        ]
        log_return_list: list[float | None] = [None] * n
        prior_idx_arr = lo_arr - 1
        for i in range(n):
            prior_idx = int(prior_idx_arr[i])
            if prior_idx < 0:
                continue
            prior_price = float(price_float[prior_idx])
            current_price = float(price_float[i])
            if prior_price <= 0.0 or current_price <= 0.0:
                continue
            log_return_list[i] = float(np.log(current_price / prior_price))

        column_data[f"rolling_aggtrade_count_{label}"] = window_count
        column_data[f"rolling_quantity_sum_{label}"] = qty_sum_strs
        column_data[f"rolling_quantity_mean_{label}"] = qty_mean_strs
        column_data[f"rolling_aggressive_buy_quantity_{label}"] = buy_sum_strs
        column_data[f"rolling_aggressive_sell_quantity_{label}"] = sell_sum_strs
        column_data[f"rolling_aggressive_buy_count_{label}"] = window_buy_count
        column_data[f"rolling_aggressive_sell_count_{label}"] = window_sell_count
        column_data[f"rolling_aggressive_flow_ratio_{label}"] = ratio_list
        column_data[f"rolling_aggressive_quantity_imbalance_{label}"] = imbalance_strs
        column_data[f"rolling_log_return_past_window_{label}"] = log_return_list

    # --- 9. Time-context columns ---
    day_start_ms = _utc_day_start_ms(utc_date)
    ms_since_day_start = (transact_time_ms - np.int64(day_start_ms)).astype(np.int64)
    if int(ms_since_day_start.min()) < 0 or int(ms_since_day_start.max()) >= UTC_DAY_MS:
        raise FeatureComputationError(
            "transact_time_ms outside the half-open UTC day for source utc_date"
        )
    utc_hour = (ms_since_day_start // 3_600_000).astype(np.int8)
    utc_minute = ((ms_since_day_start % 3_600_000) // 60_000).astype(np.int8)

    invalid_window_flag = np.zeros(n, dtype=np.bool_)
    rolling_missing_window_flag = np.zeros(n, dtype=np.bool_)

    column_data["utc_hour"] = utc_hour
    column_data["utc_minute"] = utc_minute
    column_data["milliseconds_since_day_start"] = ms_since_day_start
    column_data["invalid_window_flag"] = invalid_window_flag
    column_data["rolling_missing_window_flag"] = rolling_missing_window_flag

    # --- 10. Lineage / identity / metadata columns ---
    feature_timestamp_ms = transact_time_ms.copy()
    column_data["dataset_family"] = [FEATURE_DATASET_FAMILY] * n
    column_data["dataset_version"] = [FEATURE_DATASET_VERSION] * n
    column_data["source_dataset_family"] = [SOURCE_NORMALIZED_DATASET_FAMILY] * n
    column_data["source_dataset_version"] = [SOURCE_NORMALIZED_DATASET_VERSION] * n
    column_data["source_feature_schema_version"] = [FEATURE_SCHEMA_VERSION] * n
    column_data["symbol"] = [symbol] * n
    column_data["utc_date"] = [utc_date] * n
    column_data["agg_trade_id"] = agg_trade_id
    column_data["row_index"] = row_index
    column_data["feature_timestamp_ms"] = feature_timestamp_ms
    column_data["source_transact_time_ms"] = transact_time_ms
    column_data["source_normalized_parquet_sha256"] = (
        [lineage.source_normalized_parquet_sha256] * n
    )
    column_data["source_normalized_manifest_sha256"] = (
        [lineage.source_normalized_manifest_sha256] * n
    )
    column_data["source_successor_state_sha256"] = (
        [lineage.source_successor_state_sha256] * n
    )
    column_data["source_phase_4bf_gate_report_sha256"] = (
        [lineage.source_phase_4bf_gate_report_sha256] * n
    )
    column_data["feature_config_hash"] = [lineage.feature_config_hash] * n

    # --- 11. Build pyarrow schema in canonical column order ---
    if config.feature_names != FEATURE_NAMES_V001:
        raise FeatureSchemaError(
            "FeatureComputationConfig.feature_names diverged from FEATURE_NAMES_V001"
        )
    assert_no_forbidden_substrings(FEATURE_SCHEMA_V001)

    int64_cols = {
        "agg_trade_id",
        "row_index",
        "feature_timestamp_ms",
        "source_transact_time_ms",
        "milliseconds_since_day_start",
    }
    int8_cols = {"utc_hour", "utc_minute"}
    bool_cols = {"invalid_window_flag", "rolling_missing_window_flag"}
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

    schema_fields: list[pa.Field] = []
    for col in FEATURE_SCHEMA_V001:
        if col in int64_cols:
            schema_fields.append(pa.field(col, pa.int64(), nullable=False))
        elif col in int8_cols:
            schema_fields.append(pa.field(col, pa.int8(), nullable=False))
        elif col in bool_cols:
            schema_fields.append(pa.field(col, pa.bool_(), nullable=False))
        elif col.startswith(int64_count_prefixes):
            schema_fields.append(pa.field(col, pa.int64(), nullable=False))
        elif col.startswith(nullable_float_prefixes):
            schema_fields.append(pa.field(col, pa.float64(), nullable=True))
        elif col.startswith(non_null_decimal_prefixes):
            schema_fields.append(pa.field(col, pa.string(), nullable=False))
        elif col.startswith(nullable_decimal_prefixes):
            schema_fields.append(pa.field(col, pa.string(), nullable=True))
        else:
            schema_fields.append(pa.field(col, pa.string(), nullable=False))

    schema = pa.schema(schema_fields)
    if tuple(schema.names) != FEATURE_SCHEMA_V001:
        raise FeatureSchemaError(
            "constructed schema does not match FEATURE_SCHEMA_V001 column order"
        )

    ordered_data = {col: column_data[col] for col in FEATURE_SCHEMA_V001}
    table = pa.Table.from_pydict(ordered_data, schema=schema)
    if tuple(table.column_names) != FEATURE_SCHEMA_V001:
        raise FeatureSchemaError(
            "constructed table column order diverged from FEATURE_SCHEMA_V001"
        )
    if table.num_rows != n:
        raise FeatureComputationError(
            f"constructed table row count {table.num_rows} != source row count {n}"
        )
    return table


def write_feature_dataset(
    *,
    table: pa.Table,
    output_path: Path,
    write_sha256_sidecar: bool = True,
) -> tuple[Path, str, int, Path | None, str | None]:
    """Atomically write *table* to *output_path*.

    Returns ``(output_path, output_sha256, output_size,
    sidecar_path_or_None, sidecar_sha_or_None)``. The output and sidecar
    paths are restricted to ``data/microstructure/features/``; the
    writer refuses to overwrite an existing finalised file.
    """
    if tuple(table.column_names) != FEATURE_SCHEMA_V001:
        raise FeatureSchemaError(
            "table column order does not match FEATURE_SCHEMA_V001"
        )
    output_sha, output_size = atomic_write_feature_parquet(
        output_path, table, refuse_overwrite=True
    )
    sidecar_path: Path | None = None
    sidecar_sha: str | None = None
    if write_sha256_sidecar:
        sidecar_path = output_path.with_suffix(output_path.suffix + ".sha256")
        sidecar_sha, _ = write_feature_sha256_sidecar(
            sidecar_path,
            target_filename=output_path.name,
            sha256_hex=output_sha,
            refuse_overwrite=True,
        )
    return output_path, output_sha, output_size, sidecar_path, sidecar_sha


__all__ = [
    "FeatureComputationError",
    "FeatureComputationResult",
    "FeatureLineage",
    "compute_aggtrades_features",
    "write_feature_dataset",
]
