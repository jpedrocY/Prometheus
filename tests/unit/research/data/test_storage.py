from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb
import pyarrow.parquet as pq
import pytest

from prometheus.core.intervals import Interval
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.research.data.storage import (
    NORMALIZED_KLINE_COLUMNS,
    attach_dataset_view,
    partition_path,
    query_completed_bars,
    read_klines,
    write_klines,
)

ANCHOR_MS = 1_774_224_000_000  # 2026-04-01T00:00:00Z
FIFTEEN_MIN_MS = 15 * 60 * 1000


def _kline(i: int, symbol: Symbol = Symbol.BTCUSDT) -> NormalizedKline:
    base_price = 65000.0 if symbol is Symbol.BTCUSDT else 3500.0
    return NormalizedKline(
        symbol=symbol,
        interval=Interval.I_15M,
        open_time=ANCHOR_MS + i * FIFTEEN_MIN_MS,
        close_time=ANCHOR_MS + (i + 1) * FIFTEEN_MIN_MS - 1,
        open=base_price + i,
        high=base_price + i + 10,
        low=base_price + i - 10,
        close=base_price + i + 5,
        volume=1.0 + i,
        quote_asset_volume=base_price * (1.0 + i),
        trade_count=10 + i,
        taker_buy_base_volume=0.5,
        taker_buy_quote_volume=base_price / 2,
        source="test",
    )


def test_partition_path_format(tmp_path: Path) -> None:
    path = partition_path(tmp_path, Symbol.BTCUSDT, Interval.I_15M, 2026, 4)
    assert path == tmp_path / "symbol=BTCUSDT" / "interval=15m" / "year=2026" / "month=04"


def test_partition_path_rejects_invalid_month(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        partition_path(tmp_path, Symbol.BTCUSDT, Interval.I_15M, 2026, 13)


def test_write_and_read_round_trip(tmp_path: Path) -> None:
    klines = [_kline(i) for i in range(4)]
    written = write_klines(
        tmp_path,
        klines,
        dataset_version="synthetic_btcusdt_15m__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    assert len(written) == 1
    assert written[0].exists()

    loaded = read_klines(tmp_path)
    assert loaded == klines


def test_write_preserves_custom_file_metadata(tmp_path: Path) -> None:
    klines = [_kline(i) for i in range(2)]
    written = write_klines(
        tmp_path,
        klines,
        dataset_version="synthetic_btcusdt_15m__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    parquet_file = pq.ParquetFile(written[0])
    metadata: dict[bytes, bytes] | None = parquet_file.schema_arrow.metadata
    assert metadata is not None
    assert metadata[b"dataset_version"] == b"synthetic_btcusdt_15m__v001"
    assert metadata[b"schema_version"] == b"kline_v1"
    assert metadata[b"pipeline_version"] == b"prometheus@0.0.0"


def test_write_writes_expected_columns(tmp_path: Path) -> None:
    klines = [_kline(0)]
    written = write_klines(
        tmp_path,
        klines,
        dataset_version="synthetic_btcusdt_15m__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    # Read as a single Parquet file (no partition discovery from path).
    table = pq.ParquetFile(written[0]).read()
    assert tuple(table.column_names) == NORMALIZED_KLINE_COLUMNS


def test_write_groups_symbols_into_separate_partitions(tmp_path: Path) -> None:
    klines = [_kline(0, Symbol.BTCUSDT), _kline(0, Symbol.ETHUSDT)]
    written = write_klines(
        tmp_path,
        klines,
        dataset_version="multi_symbol__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    assert len(written) == 2
    btc_files = [p for p in written if "symbol=BTCUSDT" in p.as_posix()]
    eth_files = [p for p in written if "symbol=ETHUSDT" in p.as_posix()]
    assert len(btc_files) == 1
    assert len(eth_files) == 1


def test_read_klines_filters_by_symbol(tmp_path: Path) -> None:
    klines = [_kline(0, Symbol.BTCUSDT), _kline(0, Symbol.ETHUSDT)]
    write_klines(
        tmp_path,
        klines,
        dataset_version="multi_symbol__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    btc_only = read_klines(tmp_path, symbol=Symbol.BTCUSDT)
    assert all(k.symbol is Symbol.BTCUSDT for k in btc_only)
    assert len(btc_only) == 1


def test_read_klines_on_empty_root_returns_empty(tmp_path: Path) -> None:
    assert read_klines(tmp_path / "nonexistent") == []


def test_duckdb_view_row_count(tmp_path: Path) -> None:
    klines = [_kline(i) for i in range(8)]
    write_klines(
        tmp_path,
        klines,
        dataset_version="synthetic_btcusdt_15m__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    con = duckdb.connect()
    attach_dataset_view(con, "klines_view", tmp_path)
    result: tuple[Any, ...] | None = con.execute("SELECT COUNT(*) FROM klines_view").fetchone()
    assert result is not None
    (count,) = result
    assert count == 8


def test_duckdb_query_completed_bars_window(tmp_path: Path) -> None:
    klines = [_kline(i) for i in range(8)]
    write_klines(
        tmp_path,
        klines,
        dataset_version="synthetic_btcusdt_15m__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    con = duckdb.connect()
    attach_dataset_view(con, "klines_view", tmp_path)
    rows = query_completed_bars(
        con,
        "klines_view",
        symbol=Symbol.BTCUSDT,
        interval=Interval.I_15M,
        start_ms=ANCHOR_MS + 2 * FIFTEEN_MIN_MS,
        end_ms=ANCHOR_MS + 4 * FIFTEEN_MIN_MS,
    )
    assert len(rows) == 3
    assert [r["open_time"] for r in rows] == [
        ANCHOR_MS + 2 * FIFTEEN_MIN_MS,
        ANCHOR_MS + 3 * FIFTEEN_MIN_MS,
        ANCHOR_MS + 4 * FIFTEEN_MIN_MS,
    ]


def test_attach_dataset_view_rejects_bad_view_name(tmp_path: Path) -> None:
    con = duckdb.connect()
    with pytest.raises(ValueError):
        attach_dataset_view(con, "bad;view", tmp_path)


# ---------------------------------------------------------------------------
# Funding-rate nullable mark_price round-trip (GAP-20260420-029)
# ---------------------------------------------------------------------------


def test_funding_rate_round_trip_with_none_mark_price(tmp_path: Path) -> None:
    """A FundingRateEvent with mark_price=None must survive Parquet round-trip."""
    from prometheus.core.events import FundingRateEvent
    from prometheus.research.data.storage import (
        read_funding_rate_events,
        write_funding_rate_events,
    )

    events = [
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=1_640_995_200_006,  # 2022-01-01
            funding_rate=0.00010000,
            mark_price=None,  # pre-2024 Binance behavior
            source="test",
        ),
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=1_704_067_200_000,  # 2024-01-01
            funding_rate=0.00037409,
            mark_price=42313.90,  # populated
            source="test",
        ),
    ]
    write_funding_rate_events(
        tmp_path,
        events,
        dataset_version="binance_usdm_btcusdt_funding__v002",
        schema_version="funding_rate_event_v1",
        pipeline_version="test",
    )
    read_back = read_funding_rate_events(tmp_path, symbol=Symbol.BTCUSDT)
    assert len(read_back) == 2
    # Sort by funding_time for deterministic comparison (storage sorts by
    # symbol then funding_time already, but be explicit in assertions).
    read_back_sorted = sorted(read_back, key=lambda e: e.funding_time)
    assert read_back_sorted[0].mark_price is None
    assert read_back_sorted[0].funding_rate == 0.00010000
    assert read_back_sorted[1].mark_price == 42313.90
    assert read_back_sorted[1].funding_rate == 0.00037409


def test_funding_rate_round_trip_only_none_mark_prices(tmp_path: Path) -> None:
    """A window containing only pre-2024 events (all None) must round-trip."""
    from prometheus.core.events import FundingRateEvent
    from prometheus.research.data.storage import (
        read_funding_rate_events,
        write_funding_rate_events,
    )

    events = [
        FundingRateEvent(
            symbol=Symbol.ETHUSDT,
            funding_time=1_640_995_200_000 + i * 8 * 60 * 60 * 1000,
            funding_rate=0.00005 * (i + 1),
            mark_price=None,
            source="test",
        )
        for i in range(3)
    ]
    write_funding_rate_events(
        tmp_path,
        events,
        dataset_version="binance_usdm_ethusdt_funding__v002",
        schema_version="funding_rate_event_v1",
        pipeline_version="test",
    )
    read_back = read_funding_rate_events(tmp_path, symbol=Symbol.ETHUSDT)
    assert len(read_back) == 3
    assert all(e.mark_price is None for e in read_back)
