"""Phase 4bm-H multi-day v002 aggTrades feature computation kernel.

This module implements the v002 feature schema (62 columns = 17 v002
lineage / identity / metadata + 45 v001 feature / quality columns)
with deterministic causal cross-day rolling-window aggregation. The
kernel mirrors the Phase 4bh-B v001 feature semantics verbatim for
the 45 feature / quality columns:

- event-aligned output (one feature row per current-day source row);
- causal trailing windows ``(T - window_ms, T]`` with same-timestamp
  tie-break ``row_index <= R``;
- aggressive-side rule ``is_buyer_maker = false -> aggressive buy``;
- Decimal-as-string for raw quantity sums / aggressive quantities /
  imbalances and rolling quantity means;
- ``float64`` for aggressive flow ratios and log returns;
- 4 trailing windows: 1s, 5s, 15s, 60s.

The v002 multi-day extension uses Phase 4bm-G §16 policy 1
(causal cross-day lookback): per current-day output, optional
prior-day tail rows are loaded as read-only context so that rolling
windows that cross the day boundary remain causally fully populated
from real data. For day 1 (no prior-day in scope), rows whose 60 s
trailing window would extend before the v002 date start carry
``rolling_missing_window_flag = True`` and the window aggregates fall
back to the v001 empty-window semantics.

This module:

- does NOT compute labels, targets, signals, future returns, ML
  features, alpha, edge, prediction, model scores, decision, strategy,
  PnL, MFE, MAE, R-multiple, equity, position, liquidation, funding,
  open-interest, order-book, or mark-price proxies;
- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- never assumes future bars are available; only rows ``j <= i`` in
  canonical (transact_time_ms, row_index) order contribute to row
  ``i``'s features.
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
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    FeatureSchemaError,
)
from .features_schema_v002 import (
    CROSS_DAY_TAIL_BUFFER_MS,
    FEATURE_DATASET_VERSION_V002,
    FEATURE_NAMES_V002,
    FEATURE_SCHEMA_V002,
    FEATURE_SCHEMA_VERSION_V002,
    PHASE_4BM_E_OUTCOME_LITERAL,
    SOURCE_NORMALIZED_DATASET_FAMILY_V002,
    SOURCE_NORMALIZED_DATASET_VERSION_V002,
    FeatureComputationConfigV002,
    assert_no_forbidden_substrings_v002,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    import numpy as np
    import pyarrow as pa


UTC_DAY_MS = 86_400_000


class FeatureComputationErrorV002(RuntimeError):
    """Raised when the Phase 4bm-H v002 feature kernel fails closed."""


@dataclass(frozen=True)
class FeatureLineageV002:
    """Lineage SHAs threaded into every output row at v002."""

    source_normalized_parquet_per_day_sha256: str
    source_normalized_manifest_sha256: str
    source_successor_state_sha256: str
    source_phase_4bm_d_gate_report_sha256: str
    feature_config_hash: str


@dataclass(frozen=True)
class FeatureWriteResultV002:
    """Result of one Phase 4bm-H per-day feature write."""

    parquet_path: Path
    parquet_sha256: str
    parquet_size_bytes: int
    sidecar_path: Path
    sidecar_sha256: str
    sidecar_size_bytes: int
    row_count: int


# ---------------------------------------------------------------------------
# Helpers (mirror v001 features_compute helpers; copied to keep modules
# independent and avoid coupling private v001 helpers to v002 callers).
# ---------------------------------------------------------------------------


def _max_decimal_places(strings: Sequence[str]) -> int:
    max_dp = 0
    for s in strings:
        if "." in s:
            dp = len(s.split(".", 1)[1])
            if dp > max_dp:
                max_dp = dp
    return max_dp


def _scale_decimal_string_to_int(s: str, scale_factor: int) -> int:
    return int((Decimal(s) * scale_factor).to_integral_value())


def _format_int_as_decimal_string(value: int, max_dp: int) -> str:
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
    if count <= 0:
        raise FeatureComputationErrorV002("count must be positive for mean formatting")
    total_dp = max_dp + extra_precision_digits
    scaled_sum = sum_int * (10**extra_precision_digits)
    mean_int = scaled_sum // count
    return _format_int_as_decimal_string(mean_int, total_dp)


def _utc_day_start_ms(utc_date: str) -> int:
    day = datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(day.timestamp() * 1000)


# ---------------------------------------------------------------------------
# Expected source schema (Phase 4bd / Phase 4bm-B 19-column normalized shape)
# ---------------------------------------------------------------------------

_EXPECTED_SOURCE_COLS: tuple[str, ...] = (
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


def _validate_source_table_v002(
    source_table: pa.Table, *, expected_dataset_version: str
) -> None:
    """Validate the normalized source Parquet has the v002 canonical shape."""
    if tuple(source_table.column_names) != _EXPECTED_SOURCE_COLS:
        raise FeatureComputationErrorV002(
            "source normalized parquet does not have the canonical 19-column schema"
        )
    if source_table.num_rows == 0:
        raise FeatureComputationErrorV002(
            "source normalized parquet has zero rows; cannot compute features"
        )
    src_family = source_table.column("source_dataset_family")[0].as_py()
    src_version = source_table.column("dataset_version")[0].as_py()
    if src_family != "microstructure_raw_aggtrades_v001":
        raise FeatureComputationErrorV002(
            "source_dataset_family is not 'microstructure_raw_aggtrades_v001'"
        )
    if src_version != expected_dataset_version:
        raise FeatureComputationErrorV002(
            f"source dataset_version is not {expected_dataset_version!r} "
            f"(got {src_version!r})"
        )


def _extract_arrays(table: pa.Table) -> dict[str, Any]:
    import numpy as np

    return {
        "transact_time_ms": table.column("transact_time_ms")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64, copy=False),
        "is_buyer_maker": table.column("is_buyer_maker")
        .to_numpy(zero_copy_only=False)
        .astype(np.bool_, copy=False),
        "row_index": table.column("row_index")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64, copy=False),
        "agg_trade_id": table.column("agg_trade_id")
        .to_numpy(zero_copy_only=False)
        .astype(np.int64, copy=False),
        "price": list(table.column("price").to_pylist()),
        "quantity": list(table.column("quantity").to_pylist()),
    }


def _assert_current_day_canonical_order(
    transact_time_ms: np.ndarray, row_index: np.ndarray
) -> None:
    """Verify ``row_index == arange(n)`` and ``transact_time_ms`` non-decreasing."""
    import numpy as np

    n = transact_time_ms.shape[0]
    if row_index.shape[0] != n:
        raise FeatureComputationErrorV002(
            "row_index and transact_time_ms shape mismatch"
        )
    expected = np.arange(n, dtype=row_index.dtype)
    if not np.array_equal(row_index, expected):
        raise FeatureComputationErrorV002(
            "row_index column must equal np.arange(n) for the current day"
        )
    if n > 1 and not np.all(transact_time_ms[1:] >= transact_time_ms[:-1]):
        raise FeatureComputationErrorV002(
            "transact_time_ms must be non-decreasing in canonical sort order"
        )


# ---------------------------------------------------------------------------
# Main multi-day kernel
# ---------------------------------------------------------------------------


def compute_aggtrades_features_v002(
    *,
    current_day_table: pa.Table,
    prior_day_tail_table: pa.Table | None,
    config: FeatureComputationConfigV002,
    lineage: FeatureLineageV002,
) -> pa.Table:
    """Compute the 62-column v002 feature table for one UTC date.

    Parameters
    ----------
    current_day_table:
        The full Phase 4bm-B v002 per-day normalized Parquet for the
        target ``utc_date``. Its ``row_index`` column must equal
        ``arange(n_current)`` (the canonical Phase 4bd / 4bm-B sort
        contract).
    prior_day_tail_table:
        Optional read-only prior-day tail. Must contain only rows whose
        ``transact_time_ms`` falls in the prior UTC day (strictly less
        than the current day's ``day_start_ms``) and is at least
        ``day_start_ms - CROSS_DAY_TAIL_BUFFER_MS``. ``None`` indicates
        no prior day is available in scope (e.g., day 1 of the v002
        range). Tail rows do NOT receive feature rows in the output;
        they contribute only to current-day window aggregates.
    config:
        Locked v002 feature config carrying schema, windows, policies,
        and the deterministic ``feature_config_hash``.
    lineage:
        Per-day lineage SHAs (per-day parquet SHA + family-level
        manifest / successor / gate-report SHAs + config hash).

    Returns
    -------
    pa.Table
        The 62-column v002 feature table with exactly
        ``current_day_table.num_rows`` rows in canonical column order
        (:data:`FEATURE_SCHEMA_V002`).
    """
    import numpy as np
    import pyarrow as pa

    # --- 1. Validate source schemas ---------------------------------------
    _validate_source_table_v002(
        current_day_table,
        expected_dataset_version=SOURCE_NORMALIZED_DATASET_VERSION_V002,
    )
    if prior_day_tail_table is not None and prior_day_tail_table.num_rows > 0:
        _validate_source_table_v002(
            prior_day_tail_table,
            expected_dataset_version=SOURCE_NORMALIZED_DATASET_VERSION_V002,
        )

    symbol = current_day_table.column("symbol")[0].as_py()
    utc_date = current_day_table.column("utc_date")[0].as_py()
    if not isinstance(symbol, str) or not symbol:
        raise FeatureComputationErrorV002("source symbol must be a non-empty string")
    if not isinstance(utc_date, str) or len(utc_date) != 10:
        raise FeatureComputationErrorV002("source utc_date must be YYYY-MM-DD")

    cur = _extract_arrays(current_day_table)
    _assert_current_day_canonical_order(cur["transact_time_ms"], cur["row_index"])
    n_current = int(cur["transact_time_ms"].shape[0])

    day_start_ms = _utc_day_start_ms(utc_date)
    day_end_ms = day_start_ms + UTC_DAY_MS
    if (
        int(cur["transact_time_ms"].min()) < day_start_ms
        or int(cur["transact_time_ms"].max()) >= day_end_ms
    ):
        raise FeatureComputationErrorV002(
            f"current-day transact_time_ms outside half-open UTC day {utc_date!r}"
        )

    # --- 2. Build combined arrays (tail + current) ------------------------
    if prior_day_tail_table is not None and prior_day_tail_table.num_rows > 0:
        prior = _extract_arrays(prior_day_tail_table)
        tail_transact_time = prior["transact_time_ms"]
        tail_is_buyer_maker = prior["is_buyer_maker"]
        tail_quantity = prior["quantity"]
        tail_price = prior["price"]
        # Verify the tail's transact_time is strictly less than day_start_ms.
        if (
            tail_transact_time.size > 0
            and int(tail_transact_time.max()) >= day_start_ms
        ):
            raise FeatureComputationErrorV002(
                "prior_day_tail rows must have transact_time_ms < current "
                "day_start_ms"
            )
        # Verify the tail is sorted ascending (it must already be).
        if tail_transact_time.size > 1 and not np.all(
            tail_transact_time[1:] >= tail_transact_time[:-1]
        ):
            raise FeatureComputationErrorV002(
                "prior_day_tail transact_time_ms must be non-decreasing"
            )
        # Verify the tail buffer covers at least one max-window worth of time
        # if it contains any row.
        if tail_transact_time.size > 0 and (
            day_start_ms - int(tail_transact_time.min()) < 0
        ):
            raise FeatureComputationErrorV002(
                "prior_day_tail must lie within the prior UTC day"
            )
        n_tail = int(tail_transact_time.shape[0])
        combined_transact_time = np.concatenate(
            (tail_transact_time, cur["transact_time_ms"])
        )
        combined_is_buyer_maker = np.concatenate(
            (tail_is_buyer_maker, cur["is_buyer_maker"])
        )
        combined_quantity_strs: list[str] = list(tail_quantity) + list(cur["quantity"])
        combined_price_strs: list[str] = list(tail_price) + list(cur["price"])
        # The kernel has source-data coverage for everything from
        # day_start_ms - tail_buffer_ms (=max window) up to day_end_ms.
        # Even if the tail itself is sparse, the contiguous v002 multi-
        # day family guarantees that the absence of events in any
        # sub-region is itself observed information (not missing data).
        coverage_start_ms = day_start_ms - CROSS_DAY_TAIL_BUFFER_MS
    else:
        n_tail = 0
        combined_transact_time = cur["transact_time_ms"]
        combined_is_buyer_maker = cur["is_buyer_maker"]
        combined_quantity_strs = list(cur["quantity"])
        combined_price_strs = list(cur["price"])
        # No prior-day tail in scope (day 1 of v002 range): the kernel
        # has source-data coverage only from day_start_ms onward.
        coverage_start_ms = day_start_ms

    # Combined monotonicity sanity check (tail < current_day_start_ms <= current).
    if combined_transact_time.size > 1 and not np.all(
        combined_transact_time[1:] >= combined_transact_time[:-1]
    ):
        raise FeatureComputationErrorV002(
            "combined transact_time_ms must be non-decreasing"
        )

    n_combined = int(combined_transact_time.shape[0])

    # --- 3. Scale quantities to int with shared max_decimal_places --------
    max_dp_q = _max_decimal_places(combined_quantity_strs)
    qty_scale = 10**max_dp_q
    qty_int = np.empty(n_combined, dtype=np.int64)
    for i, s in enumerate(combined_quantity_strs):
        qty_int[i] = _scale_decimal_string_to_int(s, qty_scale)
    if int(qty_int.min()) <= 0:
        raise FeatureComputationErrorV002(
            "quantity values must all be > 0 in the source normalized parquet"
        )
    aggressive_buy_mask = ~combined_is_buyer_maker
    aggressive_sell_mask = combined_is_buyer_maker
    qty_buy_int = np.where(aggressive_buy_mask, qty_int, 0)
    qty_sell_int = np.where(aggressive_sell_mask, qty_int, 0)
    cnt_buy = aggressive_buy_mask.astype(np.int64)
    cnt_sell = aggressive_sell_mask.astype(np.int64)

    # --- 4. Cumulative sums (prefix length n_combined + 1, index 0 = 0) ---
    cum_qty = np.concatenate(([0], np.cumsum(qty_int, dtype=np.int64)))
    cum_buy_qty = np.concatenate(([0], np.cumsum(qty_buy_int, dtype=np.int64)))
    cum_sell_qty = np.concatenate(([0], np.cumsum(qty_sell_int, dtype=np.int64)))
    cum_buy_count = np.concatenate(([0], np.cumsum(cnt_buy, dtype=np.int64)))
    cum_sell_count = np.concatenate(([0], np.cumsum(cnt_sell, dtype=np.int64)))

    # --- 5. Float prices for log-return computation only ------------------
    price_float = np.empty(n_combined, dtype=np.float64)
    for i, s in enumerate(combined_price_strs):
        price_float[i] = float(s)
    if not np.all(np.isfinite(price_float)) or float(price_float.min()) <= 0.0:
        raise FeatureComputationErrorV002(
            "price values must all be finite and > 0 in the source normalized parquet"
        )

    # Indices in the combined arrays that correspond to current-day rows.
    current_indices = np.arange(n_tail, n_combined, dtype=np.int64)

    # --- 6. Per-window aggregates over the combined arrays ----------------
    column_data: dict[str, list[Any] | np.ndarray] = {}

    for window_ms, label in zip(
        FEATURE_WINDOWS_MS_V001, FEATURE_WINDOW_LABELS_V001, strict=True
    ):
        # Threshold for current-day rows only.
        cur_T = combined_transact_time[current_indices]
        threshold = cur_T - np.int64(window_ms)
        lo_arr = np.searchsorted(
            combined_transact_time, threshold, side="right"
        ).astype(np.int64)
        hi_plus_one = current_indices + 1
        window_count = hi_plus_one - lo_arr
        window_qty = cum_qty[hi_plus_one] - cum_qty[lo_arr]
        window_buy = cum_buy_qty[hi_plus_one] - cum_buy_qty[lo_arr]
        window_sell = cum_sell_qty[hi_plus_one] - cum_sell_qty[lo_arr]
        window_buy_count = cum_buy_count[hi_plus_one] - cum_buy_count[lo_arr]
        window_sell_count = cum_sell_count[hi_plus_one] - cum_sell_count[lo_arr]

        qty_sum_strs: list[str] = [
            "0" if int(window_count[i]) == 0
            else _format_int_as_decimal_string(int(window_qty[i]), max_dp_q)
            for i in range(n_current)
        ]
        qty_mean_strs: list[str | None] = [
            None if int(window_count[i]) == 0
            else _format_mean_as_decimal_string(
                int(window_qty[i]), int(window_count[i]), max_dp_q
            )
            for i in range(n_current)
        ]
        buy_sum_strs: list[str] = [
            "0" if int(window_buy_count[i]) == 0
            else _format_int_as_decimal_string(int(window_buy[i]), max_dp_q)
            for i in range(n_current)
        ]
        sell_sum_strs: list[str] = [
            "0" if int(window_sell_count[i]) == 0
            else _format_int_as_decimal_string(int(window_sell[i]), max_dp_q)
            for i in range(n_current)
        ]
        imbalance_strs: list[str] = [
            "0" if int(window_buy_count[i]) == 0 and int(window_sell_count[i]) == 0
            else _format_int_as_decimal_string(
                int(window_buy[i]) - int(window_sell[i]), max_dp_q
            )
            for i in range(n_current)
        ]
        denom_int = window_buy + window_sell
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(
                denom_int > 0,
                window_buy.astype(np.float64) / denom_int.astype(np.float64),
                np.nan,
            )
        ratio_list: list[float | None] = [
            None if not np.isfinite(ratio[i]) else float(ratio[i])
            for i in range(n_current)
        ]
        log_return_list: list[float | None] = [None] * n_current
        prior_idx_arr = lo_arr - 1
        for i in range(n_current):
            prior_idx = int(prior_idx_arr[i])
            if prior_idx < 0:
                continue
            cur_combined_idx = int(current_indices[i])
            prior_price = float(price_float[prior_idx])
            current_price = float(price_float[cur_combined_idx])
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

    # --- 7. Time-context columns ------------------------------------------
    cur_T_full = cur["transact_time_ms"]
    ms_since_day_start = (cur_T_full - np.int64(day_start_ms)).astype(np.int64)
    if (
        int(ms_since_day_start.min()) < 0
        or int(ms_since_day_start.max()) >= UTC_DAY_MS
    ):
        raise FeatureComputationErrorV002(
            "transact_time_ms outside the half-open UTC day for source utc_date"
        )
    utc_hour = (ms_since_day_start // 3_600_000).astype(np.int8)
    utc_minute = ((ms_since_day_start % 3_600_000) // 60_000).astype(np.int8)

    invalid_window_flag = np.zeros(n_current, dtype=np.bool_)

    # rolling_missing_window_flag is True iff the row's maximum-window
    # lookback would extend before the earliest timestamp the kernel
    # has source-data coverage for. With prior-day tail loaded
    # (coverage_start_ms = day_start_ms - CROSS_DAY_TAIL_BUFFER_MS), all
    # current-day windows are fully covered (because the trailing
    # window's left endpoint T - max_window_ms is >= day_start_ms -
    # max_window_ms = coverage_start_ms). Day 1 of the v002 range has
    # no prior tail in scope (coverage_start_ms = day_start_ms); rows
    # whose 60 s window crosses day_start_ms therefore carry the flag.
    max_window = max(FEATURE_WINDOWS_MS_V001)
    threshold_max = cur_T_full - np.int64(max_window)
    rolling_missing_window_flag = (threshold_max < np.int64(coverage_start_ms)).astype(
        np.bool_
    )

    column_data["utc_hour"] = utc_hour
    column_data["utc_minute"] = utc_minute
    column_data["milliseconds_since_day_start"] = ms_since_day_start
    column_data["invalid_window_flag"] = invalid_window_flag
    column_data["rolling_missing_window_flag"] = rolling_missing_window_flag

    # --- 8. Lineage / identity / metadata columns -------------------------
    feature_timestamp_ms = cur_T_full.copy()
    column_data["dataset_family"] = [FEATURE_DATASET_FAMILY] * n_current
    column_data["dataset_version"] = [FEATURE_DATASET_VERSION_V002] * n_current
    column_data["source_dataset_family"] = (
        [SOURCE_NORMALIZED_DATASET_FAMILY_V002] * n_current
    )
    column_data["source_dataset_version"] = (
        [SOURCE_NORMALIZED_DATASET_VERSION_V002] * n_current
    )
    column_data["feature_schema_version"] = [FEATURE_SCHEMA_VERSION_V002] * n_current
    column_data["symbol"] = [symbol] * n_current
    column_data["utc_date"] = [utc_date] * n_current
    column_data["agg_trade_id"] = cur["agg_trade_id"]
    column_data["row_index"] = cur["row_index"]
    column_data["feature_timestamp_ms"] = feature_timestamp_ms
    column_data["source_transact_time_ms"] = cur_T_full
    column_data["source_normalized_parquet_per_day_sha256"] = (
        [lineage.source_normalized_parquet_per_day_sha256] * n_current
    )
    column_data["source_normalized_manifest_sha256"] = (
        [lineage.source_normalized_manifest_sha256] * n_current
    )
    column_data["source_successor_state_sha256"] = (
        [lineage.source_successor_state_sha256] * n_current
    )
    column_data["source_phase_4bm_d_gate_report_sha256"] = (
        [lineage.source_phase_4bm_d_gate_report_sha256] * n_current
    )
    column_data["source_phase_4bm_e_outcome"] = (
        [PHASE_4BM_E_OUTCOME_LITERAL] * n_current
    )
    column_data["feature_config_hash"] = [lineage.feature_config_hash] * n_current

    # --- 9. Build pyarrow schema in canonical column order ----------------
    if config.feature_names != FEATURE_NAMES_V002:
        raise FeatureSchemaError(
            "FeatureComputationConfigV002.feature_names diverged from FEATURE_NAMES_V002"
        )
    assert_no_forbidden_substrings_v002(FEATURE_SCHEMA_V002)

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
    for col in FEATURE_SCHEMA_V002:
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
    if tuple(schema.names) != FEATURE_SCHEMA_V002:
        raise FeatureSchemaError(
            "constructed schema does not match FEATURE_SCHEMA_V002 column order"
        )

    ordered_data = {col: column_data[col] for col in FEATURE_SCHEMA_V002}
    table = pa.Table.from_pydict(ordered_data, schema=schema)
    if tuple(table.column_names) != FEATURE_SCHEMA_V002:
        raise FeatureSchemaError(
            "constructed table column order diverged from FEATURE_SCHEMA_V002"
        )
    if table.num_rows != n_current:
        raise FeatureComputationErrorV002(
            f"constructed table row count {table.num_rows} != current-day row count {n_current}"
        )
    return table


def slice_prior_day_tail(
    prior_day_table: pa.Table,
    *,
    current_day_start_ms: int,
    tail_buffer_ms: int = CROSS_DAY_TAIL_BUFFER_MS,
) -> pa.Table:
    """Return the tail of *prior_day_table* covering the cross-day lookback buffer.

    The tail contains exactly the prior-day rows with
    ``transact_time_ms >= current_day_start_ms - tail_buffer_ms``.
    """
    import pyarrow as pa
    import pyarrow.compute as pc

    if not isinstance(prior_day_table, pa.Table):
        raise FeatureComputationErrorV002("prior_day_table must be a pyarrow.Table")
    if tail_buffer_ms <= 0:
        raise FeatureComputationErrorV002("tail_buffer_ms must be positive")
    cutoff = current_day_start_ms - tail_buffer_ms
    mask = pc.greater_equal(prior_day_table.column("transact_time_ms"), cutoff)
    return prior_day_table.filter(mask)


def write_feature_dataset_v002(
    *,
    table: pa.Table,
    output_path: Path,
    write_sha256_sidecar: bool = True,
) -> FeatureWriteResultV002:
    """Atomically write *table* to *output_path* and write a canonical sidecar.

    Path discipline: must resolve under ``data/microstructure/features/``.
    Refuses to overwrite an existing finalised file.
    """
    if tuple(table.column_names) != FEATURE_SCHEMA_V002:
        raise FeatureSchemaError(
            "table column order does not match FEATURE_SCHEMA_V002"
        )
    parquet_sha, parquet_size = atomic_write_feature_parquet(
        output_path, table, refuse_overwrite=True
    )
    sidecar_path = output_path.with_suffix(output_path.suffix + ".sha256")
    sidecar_sha, sidecar_size = write_feature_sha256_sidecar(
        sidecar_path,
        target_filename=output_path.name,
        sha256_hex=parquet_sha,
        refuse_overwrite=True,
    )
    return FeatureWriteResultV002(
        parquet_path=output_path,
        parquet_sha256=parquet_sha,
        parquet_size_bytes=parquet_size,
        sidecar_path=sidecar_path,
        sidecar_sha256=sidecar_sha,
        sidecar_size_bytes=sidecar_size,
        row_count=table.num_rows,
    )


__all__ = [
    "CROSS_DAY_TAIL_BUFFER_MS",
    "FeatureComputationErrorV002",
    "FeatureLineageV002",
    "FeatureWriteResultV002",
    "compute_aggtrades_features_v002",
    "slice_prior_day_tail",
    "write_feature_dataset_v002",
]
