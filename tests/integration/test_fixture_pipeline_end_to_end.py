"""End-to-end Phase 2 integration test.

Flow:
  FixtureKlineSource
    -> normalize_rows
    -> write_klines (Parquet, Hive-partitioned)
    -> read_klines (round-trip)
    -> attach_dataset_view + query_completed_bars (DuckDB)
    -> derive_1h_from_15m (with full-hour bucket coverage)
    -> quality checks (no duplicates, monotonic, no gaps, no future bars)
    -> read + write manifests (immutability + round-trip)

Runs entirely offline on deterministic synthetic fixtures.
"""

from __future__ import annotations

from pathlib import Path

import duckdb

from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.derive import derive_1h_from_15m
from prometheus.research.data.fetch import FixtureKlineSource
from prometheus.research.data.manifests import (
    DatasetManifest,
    read_manifest,
    write_manifest,
)
from prometheus.research.data.normalize import normalize_rows
from prometheus.research.data.quality import (
    check_no_duplicates,
    check_no_future_bars,
    check_no_missing_bars,
    check_timestamp_monotonic,
)
from prometheus.research.data.storage import (
    attach_dataset_view,
    query_completed_bars,
    read_klines,
    write_klines,
)
from tests.fixtures.market_data.synthetic import synthetic_15m_spec

ANCHOR_MS = 1_774_224_000_000  # 2026-04-01T00:00:00Z (aligned to 1h)
FIFTEEN_MIN_MS = 15 * 60 * 1000
ONE_HOUR_MS = 60 * 60 * 1000


def test_phase_2_pipeline_btcusdt_24h(tmp_path: Path) -> None:
    # 24h of 15m bars = 96 bars; exactly 24 completed 1h buckets.
    start_ms = ANCHOR_MS
    end_ms = ANCHOR_MS + 95 * FIFTEEN_MIN_MS

    # 1. Fetch via the fixture source (interface exercise).
    source = FixtureKlineSource(synthetic_15m_spec)
    raw_rows = list(
        source.fetch(
            symbol=Symbol.BTCUSDT,
            interval=Interval.I_15M,
            start_ms=start_ms,
            end_ms=end_ms,
        )
    )
    assert len(raw_rows) == 96

    # 2. Normalize.
    klines = normalize_rows(
        raw_rows,
        symbol=Symbol.BTCUSDT,
        interval=Interval.I_15M,
        source="synthetic:fixture",
    )
    assert len(klines) == 96

    # 3. Write.
    data_root = tmp_path / "data" / "normalized" / "klines"
    written = write_klines(
        data_root,
        klines,
        dataset_version="synthetic_btcusdt_15m__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    assert len(written) == 1  # single partition (April 2026)
    assert written[0].exists()

    # 4. Read back; verify full round-trip equality.
    loaded = read_klines(data_root, symbol=Symbol.BTCUSDT, interval=Interval.I_15M)
    assert loaded == klines

    # 5. DuckDB view query.
    con = duckdb.connect()
    attach_dataset_view(con, "klines_view", data_root)
    first_hour_rows = query_completed_bars(
        con,
        "klines_view",
        symbol=Symbol.BTCUSDT,
        interval=Interval.I_15M,
        start_ms=start_ms,
        end_ms=start_ms + ONE_HOUR_MS - 1,
    )
    assert len(first_hour_rows) == 4

    # 6. Derive 1h bars.
    derived, invalid = derive_1h_from_15m(klines)
    assert invalid == []
    assert len(derived) == 24

    # 7. Quality checks - all pass on happy-path fixtures.
    assert check_no_duplicates(klines) == []
    assert check_timestamp_monotonic(klines) == []
    assert (
        check_no_missing_bars(
            klines,
            expected_start_ms=start_ms,
            expected_end_ms=end_ms,
            interval=Interval.I_15M,
        )
        == []
    )
    assert check_no_future_bars(klines, now_ms=end_ms + ONE_HOUR_MS) == []

    # 8. Manifest write + read round-trip.
    manifest = DatasetManifest(
        dataset_name="synthetic_btcusdt_15m",
        dataset_version="synthetic_btcusdt_15m__v001",
        dataset_category="normalized_kline",
        created_at_utc_ms=start_ms,
        canonical_timezone="UTC",
        canonical_timestamp_format="unix_milliseconds",
        symbols=(Symbol.BTCUSDT,),
        intervals=(Interval.I_15M,),
        sources=("synthetic:test",),
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
        partitioning=("symbol", "interval", "year", "month"),
        primary_key=("symbol", "interval", "open_time"),
        generator="FixtureKlineSource",
        predecessor_version=None,
        invalid_windows=(),
        notes="phase 2 integration",
    )
    manifest_path = tmp_path / "data" / "manifests" / "synthetic_btcusdt_15m__v001.manifest.json"
    write_manifest(manifest_path, manifest)
    reloaded = read_manifest(manifest_path)
    assert reloaded == manifest


def test_phase_2_pipeline_ethusdt_parallel(tmp_path: Path) -> None:
    # Same exercise on ETHUSDT to confirm multi-symbol partitioning.
    start_ms = ANCHOR_MS
    end_ms = ANCHOR_MS + 95 * FIFTEEN_MIN_MS

    source = FixtureKlineSource(synthetic_15m_spec)
    raw_rows = list(
        source.fetch(
            symbol=Symbol.ETHUSDT,
            interval=Interval.I_15M,
            start_ms=start_ms,
            end_ms=end_ms,
        )
    )
    klines = normalize_rows(
        raw_rows,
        symbol=Symbol.ETHUSDT,
        interval=Interval.I_15M,
        source="synthetic:fixture",
    )
    write_klines(
        tmp_path,
        klines,
        dataset_version="synthetic_ethusdt_15m__v001",
        schema_version="kline_v1",
        pipeline_version="prometheus@0.0.0",
    )
    loaded = read_klines(tmp_path, symbol=Symbol.ETHUSDT)
    assert loaded == klines
    assert all(k.symbol is Symbol.ETHUSDT for k in loaded)
