"""Multi-day v002 feature kernel fixture helpers (Phase 4bm-H tests).

Builds tiny but schema-valid Phase 4bm-B v002 normalized aggTrades
Parquet files for two contiguous UTC days plus the canonical Phase
4bm-G feature-boundary lineage shape inside a pytest ``tmp_path``.
Tests can exercise the v002 multi-day kernel end-to-end without
touching real ``data/microstructure/`` files.

All fixtures live entirely within pytest temp directories arranged
to look like ``data/microstructure/...``.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SYNTHETIC_NORMALIZED_MANIFEST_SHA_V002 = "0" * 64
SYNTHETIC_SUCCESSOR_STATE_SHA_V002 = "1" * 64
SYNTHETIC_PHASE_4BM_D_GATE_REPORT_SHA = "2" * 64
SYNTHETIC_PHASE_4BM_F_SUCCESSOR_STATE_SHA = "3" * 64
SYNTHETIC_PHASE_4BL_D_R_RAW_GATE_REPORT_SHA = "4" * 64
SYNTHETIC_PHASE_4BL_E_RAW_SUCCESSOR_STATE_SHA = "5" * 64
SYNTHETIC_V002_RAW_MANIFEST_SHA = "6" * 64
SYNTHETIC_V002_ACQUISITION_LOG_SHA = "7" * 64


def _utc_day_start_ms(utc_date: str) -> int:
    return int(
        datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000
    )


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class MultidayV002FixtureBundle:
    """Paths and metadata for a v002 two-day Phase 4bm-H mini-fixture."""

    microstructure_root: Path
    normalized_root: Path
    features_root: Path
    manifests_root: Path

    symbol: str
    utc_date_day1: str
    utc_date_day2: str
    rows_day1: tuple[dict[str, Any], ...]
    rows_day2: tuple[dict[str, Any], ...]
    day1_parquet_path: Path
    day2_parquet_path: Path
    day1_parquet_sha256: str
    day2_parquet_sha256: str


def write_normalized_v002_parquet(
    path: Path,
    rows: Sequence[dict[str, Any]],
    *,
    symbol: str,
    utc_date: str,
) -> None:
    """Write a Phase 4bm-B 19-column v002 normalized aggTrades Parquet at *path*.

    The schema is identical to Phase 4bd v001 normalization output;
    only the ``dataset_version`` literal differs.
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    n = len(rows)
    schema = pa.schema(
        [
            ("dataset_family", pa.string()),
            ("dataset_version", pa.string()),
            ("source_dataset_family", pa.string()),
            ("source_dataset_version", pa.string()),
            ("symbol", pa.string()),
            ("utc_date", pa.string()),
            ("agg_trade_id", pa.int64()),
            ("price", pa.string()),
            ("quantity", pa.string()),
            ("first_trade_id", pa.int64()),
            ("last_trade_id", pa.int64()),
            ("transact_time_ms", pa.int64()),
            ("is_buyer_maker", pa.bool_()),
            ("source_file_sha256", pa.string()),
            ("source_manifest_sha256", pa.string()),
            ("source_gate_report_id", pa.string()),
            ("source_gate_report_sha256", pa.string()),
            ("row_index", pa.int64()),
            ("normalization_schema_version", pa.string()),
        ]
    )
    data: dict[str, list[Any]] = {
        "dataset_family": ["microstructure_normalized_aggtrades_v001"] * n,
        "dataset_version": ["v002"] * n,
        "source_dataset_family": ["microstructure_raw_aggtrades_v001"] * n,
        "source_dataset_version": ["v002"] * n,
        "symbol": [symbol] * n,
        "utc_date": [utc_date] * n,
        "agg_trade_id": [r["agg_trade_id"] for r in rows],
        "price": [r["price"] for r in rows],
        "quantity": [r["quantity"] for r in rows],
        "first_trade_id": [r["first_trade_id"] for r in rows],
        "last_trade_id": [r["last_trade_id"] for r in rows],
        "transact_time_ms": [r["transact_time_ms"] for r in rows],
        "is_buyer_maker": [r["is_buyer_maker"] for r in rows],
        "source_file_sha256": ["a" * 64] * n,
        "source_manifest_sha256": ["b" * 64] * n,
        "source_gate_report_id": ["test_phase4bl_d_r_gate_report"] * n,
        "source_gate_report_sha256": ["c" * 64] * n,
        "row_index": list(range(n)),
        "normalization_schema_version": ["v001"] * n,
    }
    table = pa.Table.from_pydict(data, schema=schema)
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path, compression="zstd")


def _make_row(
    *,
    base_ms: int,
    offset_ms: int,
    agg_trade_id: int,
    price: str,
    quantity: str,
    is_buyer_maker: bool,
) -> dict[str, Any]:
    return {
        "agg_trade_id": agg_trade_id,
        "price": price,
        "quantity": quantity,
        "first_trade_id": agg_trade_id,
        "last_trade_id": agg_trade_id,
        "transact_time_ms": base_ms + offset_ms,
        "is_buyer_maker": is_buyer_maker,
    }


def default_day1_rows(utc_date: str = "2024-12-01") -> list[dict[str, Any]]:
    """A small but schema-valid mixed-side row set for day 1.

    Includes rows in the first 60 s of the day (which must carry
    ``rolling_missing_window_flag = True`` because there's no prior
    day in scope), rows further into the day (flag=False), and rows
    in the last 60 s (which become prior-day tail context for day 2).
    """
    day_start_ms = _utc_day_start_ms(utc_date)
    day_end_ms = day_start_ms + 86_400_000
    raw = [
        # (offset_ms, agg_trade_id, price, quantity, is_buyer_maker)
        (0, 5000, "100.0", "0.500", False),
        (250, 5001, "100.1", "0.250", True),
        (500, 5002, "100.2", "0.100", False),
        (500, 5003, "100.2", "0.150", True),  # tie with 5002
        (61_000, 5004, "100.3", "0.300", False),  # > 60s into day
        (3_600_000, 5005, "100.4", "0.400", True),
        (day_end_ms - day_start_ms - 30_000, 5006, "100.5", "0.200", False),
        (day_end_ms - day_start_ms - 1, 5007, "100.6", "0.100", True),
    ]
    return [
        _make_row(
            base_ms=day_start_ms,
            offset_ms=off,
            agg_trade_id=int(a),
            price=p,
            quantity=q,
            is_buyer_maker=bool(m),
        )
        for off, a, p, q, m in raw
    ]


def default_day2_rows(utc_date: str = "2024-12-02") -> list[dict[str, Any]]:
    """A small but schema-valid mixed-side row set for day 2.

    Early rows fall inside the cross-day 60 s lookback window from
    day 1's tail; their feature aggregates should reflect day 1
    contributions (e.g., the 60 s window should include the very last
    rows of day 1).
    """
    day_start_ms = _utc_day_start_ms(utc_date)
    raw = [
        (0, 6000, "100.5", "0.200", False),
        (500, 6001, "100.4", "0.150", True),
        (5_000, 6002, "100.3", "0.300", False),
        (60_000, 6003, "100.2", "0.250", True),  # > 60s into day
        (3_600_000, 6004, "100.1", "0.400", False),
        (43_200_000, 6005, "99.9", "0.300", True),
    ]
    return [
        _make_row(
            base_ms=day_start_ms,
            offset_ms=off,
            agg_trade_id=int(a),
            price=p,
            quantity=q,
            is_buyer_maker=bool(m),
        )
        for off, a, p, q, m in raw
    ]


def all_buyer_maker_rows(
    utc_date: str = "2024-12-01", n: int = 6
) -> list[dict[str, Any]]:
    """Rows entirely on the aggressive-sell side (is_buyer_maker=True)."""
    day_start_ms = _utc_day_start_ms(utc_date)
    return [
        _make_row(
            base_ms=day_start_ms + 70_000,  # start past 60s so flag is False
            offset_ms=i * 500,
            agg_trade_id=7000 + i,
            price=f"{100.0 + i * 0.01:.2f}",
            quantity="0.100",
            is_buyer_maker=True,
        )
        for i in range(n)
    ]


def all_seller_maker_rows(
    utc_date: str = "2024-12-01", n: int = 6
) -> list[dict[str, Any]]:
    """Rows entirely on the aggressive-buy side (is_buyer_maker=False)."""
    day_start_ms = _utc_day_start_ms(utc_date)
    return [
        _make_row(
            base_ms=day_start_ms + 70_000,
            offset_ms=i * 500,
            agg_trade_id=8000 + i,
            price=f"{100.0 + i * 0.01:.2f}",
            quantity="0.100",
            is_buyer_maker=False,
        )
        for i in range(n)
    ]


def single_event_row(
    utc_date: str = "2024-12-01",
) -> list[dict[str, Any]]:
    """One row well past 60 s into the day, mixed schema-valid."""
    day_start_ms = _utc_day_start_ms(utc_date)
    return [
        _make_row(
            base_ms=day_start_ms + 90_000,
            offset_ms=0,
            agg_trade_id=9000,
            price="100.0",
            quantity="0.500",
            is_buyer_maker=False,
        )
    ]


def build_multiday_v002_fixture(
    tmp_path: Path,
    *,
    symbol: str = "BTCUSDT",
    utc_date_day1: str = "2024-12-01",
    utc_date_day2: str = "2024-12-02",
    rows_day1: Sequence[dict[str, Any]] | None = None,
    rows_day2: Sequence[dict[str, Any]] | None = None,
) -> MultidayV002FixtureBundle:
    """Build a two-day v002 multi-day Phase 4bm-H mini-fixture under *tmp_path*."""
    rows1: list[dict[str, Any]] = list(rows_day1 or default_day1_rows(utc_date_day1))
    rows2: list[dict[str, Any]] = list(rows_day2 or default_day2_rows(utc_date_day2))

    microstructure_root = tmp_path / "data" / "microstructure"
    normalized_root = microstructure_root / "normalized"
    manifests_root = microstructure_root / "manifests"
    features_root = microstructure_root / "features"
    for d in (normalized_root, manifests_root, features_root):
        d.mkdir(parents=True, exist_ok=True)

    family_dir = "microstructure_normalized_aggtrades_v001__v002"

    def _day_parquet_path(d: str) -> Path:
        yyyy, mm, _dd = d.split("-")
        return (
            normalized_root
            / family_dir
            / symbol
            / yyyy
            / mm
            / f"{symbol}-aggTrades-{d}.parquet"
        )

    day1_path = _day_parquet_path(utc_date_day1)
    day2_path = _day_parquet_path(utc_date_day2)
    write_normalized_v002_parquet(day1_path, rows1, symbol=symbol, utc_date=utc_date_day1)
    write_normalized_v002_parquet(day2_path, rows2, symbol=symbol, utc_date=utc_date_day2)

    return MultidayV002FixtureBundle(
        microstructure_root=microstructure_root,
        normalized_root=normalized_root,
        features_root=features_root,
        manifests_root=manifests_root,
        symbol=symbol,
        utc_date_day1=utc_date_day1,
        utc_date_day2=utc_date_day2,
        rows_day1=tuple(rows1),
        rows_day2=tuple(rows2),
        day1_parquet_path=day1_path,
        day2_parquet_path=day2_path,
        day1_parquet_sha256=_hash_file(day1_path),
        day2_parquet_sha256=_hash_file(day2_path),
    )


__all__ = [
    "SYNTHETIC_NORMALIZED_MANIFEST_SHA_V002",
    "SYNTHETIC_PHASE_4BL_D_R_RAW_GATE_REPORT_SHA",
    "SYNTHETIC_PHASE_4BL_E_RAW_SUCCESSOR_STATE_SHA",
    "SYNTHETIC_PHASE_4BM_D_GATE_REPORT_SHA",
    "SYNTHETIC_PHASE_4BM_F_SUCCESSOR_STATE_SHA",
    "SYNTHETIC_SUCCESSOR_STATE_SHA_V002",
    "SYNTHETIC_V002_ACQUISITION_LOG_SHA",
    "SYNTHETIC_V002_RAW_MANIFEST_SHA",
    "MultidayV002FixtureBundle",
    "all_buyer_maker_rows",
    "all_seller_maker_rows",
    "build_multiday_v002_fixture",
    "default_day1_rows",
    "default_day2_rows",
    "single_event_row",
    "write_normalized_v002_parquet",
]
