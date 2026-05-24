"""Phase 4bm-O v002 label test fixtures: tiny synthetic feature + normalized parquets.

These helpers build self-consistent, very small pyarrow tables that match
the Phase 4bm-G / 4bm-H feature contract and the Phase 4bm-N v002 label
schema well enough for label unit tests (anchor policy, cross-day
future-reference policy, envelope-terminal censoring, sign, invalid-
price, tie-break). Tests use pytest ``tmp_path`` only and never read or
write under the real ``data/microstructure/`` namespace.
"""

from __future__ import annotations

from pathlib import Path

import pyarrow as pa


def build_normalized_table_v002(
    *,
    transact_time_ms: list[int],
    prices: list[str],
    agg_trade_id_offset: int = 1_000_000,
    symbol: str = "BTCUSDT",
    utc_date: str = "2024-12-01",
) -> pa.Table:
    """Build a normalized aggTrades-shaped pyarrow Table.

    The returned table has the 19 canonical normalized columns in
    canonical order. ``row_index`` is ``np.arange(n)`` and
    ``agg_trade_id`` is monotonically increasing per row. Quantity is
    a constant ``"1"``. The price column is the caller-provided
    Decimal-as-string list.
    """
    n = len(transact_time_ms)
    if len(prices) != n:
        raise ValueError("transact_time_ms and prices must have the same length")
    quantities = ["1"] * n
    first_trade_ids = list(range(1, n + 1))
    last_trade_ids = list(range(1, n + 1))
    agg_trade_ids = [agg_trade_id_offset + i for i in range(n)]
    row_indices = list(range(n))
    schema = pa.schema(
        [
            pa.field("dataset_family", pa.string(), nullable=False),
            pa.field("dataset_version", pa.string(), nullable=False),
            pa.field("source_dataset_family", pa.string(), nullable=False),
            pa.field("source_dataset_version", pa.string(), nullable=False),
            pa.field("symbol", pa.string(), nullable=False),
            pa.field("utc_date", pa.string(), nullable=False),
            pa.field("agg_trade_id", pa.int64(), nullable=False),
            pa.field("price", pa.string(), nullable=False),
            pa.field("quantity", pa.string(), nullable=False),
            pa.field("first_trade_id", pa.int64(), nullable=False),
            pa.field("last_trade_id", pa.int64(), nullable=False),
            pa.field("transact_time_ms", pa.int64(), nullable=False),
            pa.field("is_buyer_maker", pa.bool_(), nullable=False),
            pa.field("source_file_sha256", pa.string(), nullable=False),
            pa.field("source_manifest_sha256", pa.string(), nullable=False),
            pa.field("source_gate_report_id", pa.string(), nullable=False),
            pa.field("source_gate_report_sha256", pa.string(), nullable=False),
            pa.field("row_index", pa.int64(), nullable=False),
            pa.field("normalization_schema_version", pa.string(), nullable=False),
        ]
    )
    data = {
        "dataset_family": ["microstructure_normalized_aggtrades_v001"] * n,
        "dataset_version": ["v002"] * n,
        "source_dataset_family": ["microstructure_raw_aggtrades_v001"] * n,
        "source_dataset_version": ["v002"] * n,
        "symbol": [symbol] * n,
        "utc_date": [utc_date] * n,
        "agg_trade_id": agg_trade_ids,
        "price": prices,
        "quantity": quantities,
        "first_trade_id": first_trade_ids,
        "last_trade_id": last_trade_ids,
        "transact_time_ms": transact_time_ms,
        "is_buyer_maker": [False] * n,
        "source_file_sha256": ["a" * 64] * n,
        "source_manifest_sha256": ["b" * 64] * n,
        "source_gate_report_id": ["microstructure_raw_aggtrades_v001__v002__fixture"] * n,
        "source_gate_report_sha256": ["c" * 64] * n,
        "row_index": row_indices,
        "normalization_schema_version": ["v001"] * n,
    }
    return pa.Table.from_pydict(data, schema=schema)


def build_feature_table_v002(*, normalized: pa.Table) -> pa.Table:
    """Build a minimal feature-shaped pyarrow Table aligned 1:1 with *normalized*.

    The v002 label kernel reads only four columns from the feature table
    (``row_index``, ``agg_trade_id``, ``feature_timestamp_ms``,
    ``source_transact_time_ms``); the test fixture exposes just those
    four (intentionally minimal to keep fixtures fast and side-effect-
    free).
    """
    schema = pa.schema(
        [
            pa.field("row_index", pa.int64(), nullable=False),
            pa.field("agg_trade_id", pa.int64(), nullable=False),
            pa.field("feature_timestamp_ms", pa.int64(), nullable=False),
            pa.field("source_transact_time_ms", pa.int64(), nullable=False),
        ]
    )
    transact_time_ms = normalized.column("transact_time_ms").to_pylist()
    agg_trade_id = normalized.column("agg_trade_id").to_pylist()
    row_index = normalized.column("row_index").to_pylist()
    data = {
        "row_index": row_index,
        "agg_trade_id": agg_trade_id,
        "feature_timestamp_ms": transact_time_ms,
        "source_transact_time_ms": transact_time_ms,
    }
    return pa.Table.from_pydict(data, schema=schema)


def write_temp_parquet(path: Path, table: pa.Table) -> Path:
    """Atomically write *table* to *path* under a pytest ``tmp_path``."""
    import pyarrow.parquet as pq

    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path)
    return path


__all__ = [
    "build_feature_table_v002",
    "build_normalized_table_v002",
    "write_temp_parquet",
]
