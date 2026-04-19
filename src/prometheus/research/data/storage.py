"""Parquet storage and DuckDB views for normalized kline datasets.

Hive partitioning: ``symbol=<SYM>/interval=<INTV>/year=YYYY/month=MM``.
Parquet files use zstd level 3 compression; each file carries custom
key-value metadata identifying the dataset version, schema version, and
pipeline version that produced it.
"""

from __future__ import annotations

import datetime as dt
from collections import defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any, cast

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

from prometheus.core.intervals import Interval
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol

NORMALIZED_KLINE_COLUMNS: tuple[str, ...] = (
    "symbol",
    "interval",
    "open_time",
    "close_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "quote_asset_volume",
    "trade_count",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
    "source",
)

NORMALIZED_KLINE_ARROW_SCHEMA: pa.Schema = pa.schema(
    [
        pa.field("symbol", pa.string(), nullable=False),
        pa.field("interval", pa.string(), nullable=False),
        pa.field("open_time", pa.int64(), nullable=False),
        pa.field("close_time", pa.int64(), nullable=False),
        pa.field("open", pa.float64(), nullable=False),
        pa.field("high", pa.float64(), nullable=False),
        pa.field("low", pa.float64(), nullable=False),
        pa.field("close", pa.float64(), nullable=False),
        pa.field("volume", pa.float64(), nullable=False),
        pa.field("quote_asset_volume", pa.float64(), nullable=False),
        pa.field("trade_count", pa.int64(), nullable=False),
        pa.field("taker_buy_base_volume", pa.float64(), nullable=False),
        pa.field("taker_buy_quote_volume", pa.float64(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
    ]
)

_ROW_GROUP_SIZE = 65_536
_COMPRESSION = "zstd"
_COMPRESSION_LEVEL = 3


def partition_path(
    root: Path,
    symbol: Symbol,
    interval: Interval,
    year: int,
    month: int,
) -> Path:
    """Return the Hive-partitioned directory for a (symbol, interval, year, month)."""
    if not 1 <= month <= 12:
        raise ValueError(f"month must be in [1, 12], got {month}")
    return (
        root
        / f"symbol={symbol.value}"
        / f"interval={interval.value}"
        / f"year={year:04d}"
        / f"month={month:02d}"
    )


def _year_month_for_open_time(open_time_ms: int) -> tuple[int, int]:
    stamp = dt.datetime.fromtimestamp(open_time_ms / 1000, tz=dt.UTC)
    return stamp.year, stamp.month


def _table_from_klines(klines: Sequence[NormalizedKline]) -> pa.Table:
    columns: dict[str, list[Any]] = {col: [] for col in NORMALIZED_KLINE_COLUMNS}
    for kline in klines:
        columns["symbol"].append(kline.symbol.value)
        columns["interval"].append(kline.interval.value)
        columns["open_time"].append(kline.open_time)
        columns["close_time"].append(kline.close_time)
        columns["open"].append(kline.open)
        columns["high"].append(kline.high)
        columns["low"].append(kline.low)
        columns["close"].append(kline.close)
        columns["volume"].append(kline.volume)
        columns["quote_asset_volume"].append(kline.quote_asset_volume)
        columns["trade_count"].append(kline.trade_count)
        columns["taker_buy_base_volume"].append(kline.taker_buy_base_volume)
        columns["taker_buy_quote_volume"].append(kline.taker_buy_quote_volume)
        columns["source"].append(kline.source)
    return pa.table(columns, schema=NORMALIZED_KLINE_ARROW_SCHEMA)


def write_klines(
    root: Path,
    klines: Sequence[NormalizedKline],
    *,
    dataset_version: str,
    schema_version: str,
    pipeline_version: str,
) -> list[Path]:
    """Write klines to a Hive-partitioned Parquet tree under ``root``.

    Groups by ``(symbol, interval, year, month)`` partition. Returns the
    list of Parquet file paths written, in the order of first partition
    encounter.
    """
    if not klines:
        return []

    partitions: dict[tuple[Symbol, Interval, int, int], list[NormalizedKline]] = defaultdict(list)
    for kline in klines:
        year, month = _year_month_for_open_time(kline.open_time)
        partitions[(kline.symbol, kline.interval, year, month)].append(kline)

    custom_metadata = {
        b"dataset_version": dataset_version.encode("utf-8"),
        b"schema_version": schema_version.encode("utf-8"),
        b"pipeline_version": pipeline_version.encode("utf-8"),
    }

    written_paths: list[Path] = []
    for (symbol, interval, year, month), group in partitions.items():
        group.sort(key=lambda k: k.open_time)
        directory = partition_path(root, symbol, interval, year, month)
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / "part-0000.parquet"
        table = _table_from_klines(group)
        table_with_meta = table.replace_schema_metadata(custom_metadata)
        pq.write_table(
            table_with_meta,
            file_path,
            compression=_COMPRESSION,
            compression_level=_COMPRESSION_LEVEL,
            row_group_size=_ROW_GROUP_SIZE,
        )
        written_paths.append(file_path)
    return written_paths


def _row_to_kline(row: dict[str, Any]) -> NormalizedKline:
    # Parquet stores partition keys and enum-valued columns as plain strings.
    # Pydantic strict mode does not coerce str -> StrEnum, so convert here.
    return NormalizedKline.model_validate(
        {
            "symbol": Symbol(row["symbol"]),
            "interval": Interval(row["interval"]),
            "open_time": row["open_time"],
            "close_time": row["close_time"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row["volume"],
            "quote_asset_volume": row["quote_asset_volume"],
            "trade_count": row["trade_count"],
            "taker_buy_base_volume": row["taker_buy_base_volume"],
            "taker_buy_quote_volume": row["taker_buy_quote_volume"],
            "source": row["source"],
        }
    )


def read_klines(
    root: Path,
    *,
    symbol: Symbol | None = None,
    interval: Interval | None = None,
) -> list[NormalizedKline]:
    """Read all klines under ``root``, optionally filtered by symbol/interval.

    Reads the Hive-partitioned tree with pyarrow's dataset reader. Rows
    are re-validated through :class:`NormalizedKline`, so any on-disk
    drift from the declared schema surfaces as a validation error.
    """
    import pyarrow.dataset as pads  # local import to keep cold-start light

    if not root.exists():
        return []
    dataset = pads.dataset(
        str(root),
        format="parquet",
        partitioning="hive",
    )
    filter_expr: Any = None
    if symbol is not None:
        filter_expr = pads.field("symbol") == symbol.value
    if interval is not None:
        interval_expr = pads.field("interval") == interval.value
        filter_expr = interval_expr if filter_expr is None else filter_expr & interval_expr

    table = dataset.to_table(filter=filter_expr) if filter_expr is not None else dataset.to_table()
    rows = cast(list[dict[str, Any]], table.to_pylist())
    klines = [_row_to_kline(row) for row in rows]
    klines.sort(key=lambda k: (k.symbol.value, k.interval.value, k.open_time))
    return klines


def attach_dataset_view(
    con: duckdb.DuckDBPyConnection,
    view_name: str,
    root: Path,
) -> None:
    """Create or replace a DuckDB view over the partitioned Parquet tree.

    Uses ``read_parquet(..., hive_partitioning=1)`` so predicate pushdown
    on ``symbol``/``interval``/``year``/``month`` works without scanning
    every file.
    """
    if not view_name.replace("_", "").isalnum():
        raise ValueError(f"invalid view_name: {view_name!r}")
    pattern = f"{root.as_posix()}/**/*.parquet"
    if "'" in pattern:
        raise ValueError(f"root path must not contain single quotes: {root}")
    # DuckDB rejects prepared parameters for read_parquet's path argument,
    # so the pattern is inlined. The single-quote guard above prevents
    # injection from unexpected root paths.
    con.execute(
        f"CREATE OR REPLACE VIEW {view_name} AS "
        f"SELECT * FROM read_parquet('{pattern}', hive_partitioning=1)"
    )


def query_completed_bars(
    con: duckdb.DuckDBPyConnection,
    view_name: str,
    *,
    symbol: Symbol,
    interval: Interval,
    start_ms: int,
    end_ms: int,
) -> list[dict[str, Any]]:
    """Return bars in ``[start_ms, end_ms]`` sorted by open_time."""
    if not view_name.replace("_", "").isalnum():
        raise ValueError(f"invalid view_name: {view_name!r}")
    cursor = con.execute(
        f"SELECT * FROM {view_name} "
        "WHERE symbol = ? AND interval = ? "
        "AND open_time BETWEEN ? AND ? "
        "ORDER BY open_time",
        [symbol.value, interval.value, start_ms, end_ms],
    )
    column_names = [d[0] for d in cursor.description]
    fetched: Iterable[tuple[Any, ...]] = cursor.fetchall()
    return [dict(zip(column_names, row, strict=True)) for row in fetched]
