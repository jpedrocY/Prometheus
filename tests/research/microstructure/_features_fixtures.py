"""Shared mini-fixture helpers for the Phase 4bh feature kernel tests.

Builds a tiny but schema-valid normalized aggTrades Parquet file plus
a derived manifest and a Phase 4bg-B-style successor-state JSON inside
a pytest ``tmp_path``. Tests can then exercise the feature kernel
end-to-end without ever touching the real
``data/microstructure/`` tree.

All fixtures live entirely within pytest temp directories that are
arranged to look like ``data/microstructure/...``.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Test-only synthetic SHAs used as lineage placeholders.
SYNTHETIC_NORMALIZED_PARQUET_SHA = "a" * 64
SYNTHETIC_NORMALIZED_MANIFEST_SHA = "b" * 64
SYNTHETIC_SUCCESSOR_STATE_SHA = "c" * 64
SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA = "d" * 64
SYNTHETIC_FEATURE_CONFIG_HASH = "e" * 64


@dataclass(frozen=True)
class FeatureFixtureBundle:
    """Paths and metadata for a Phase 4bh feature mini-fixture."""

    microstructure_root: Path
    normalized_root: Path
    manifests_root: Path
    features_root: Path
    successor_state_root: Path

    normalized_parquet_path: Path
    normalized_manifest_path: Path
    successor_state_path: Path

    feature_parquet_path: Path
    feature_manifest_path: Path

    symbol: str
    utc_date: str
    rows: tuple[dict[str, Any], ...]
    row_count: int
    normalized_parquet_sha256: str
    normalized_manifest_sha256: str
    successor_state_sha256: str


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _default_rows(utc_date: str = "2025-01-15") -> list[dict[str, Any]]:
    """Return a small, schema-valid set of normalized aggTrade rows.

    Times are spaced by 500 ms so that several windows are exercised:
    1s window covers ~2 events, 5s covers ~10, etc. Includes both
    aggressive-buy (``is_buyer_maker=False``) and aggressive-sell
    (``is_buyer_maker=True``) rows, plus duplicates at the same
    timestamp to exercise the same-timestamp tie-break.
    """
    from datetime import UTC, datetime

    day_start_ms = int(
        datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000
    )
    base = day_start_ms + 60_000  # one minute after midnight
    raw = [
        # (offset_ms, agg_trade_id, price, quantity, is_buyer_maker)
        (0, 1000, "100.0", "0.500", False),
        (250, 1001, "100.1", "0.250", True),
        (500, 1002, "100.2", "0.100", False),
        (500, 1003, "100.2", "0.150", True),  # same timestamp as 1002
        (1500, 1004, "100.3", "0.300", False),
        (5500, 1005, "100.4", "0.400", True),
        (8000, 1006, "100.0", "0.200", False),
        (15500, 1007, "99.9", "0.100", True),
        (60500, 1008, "99.5", "0.500", False),
        (61000, 1009, "99.6", "0.250", True),
    ]
    return [
        {
            "agg_trade_id": int(a),
            "price": p,
            "quantity": q,
            "first_trade_id": int(a),
            "last_trade_id": int(a),
            "transact_time_ms": base + int(off),
            "is_buyer_maker": bool(m),
        }
        for off, a, p, q, m in raw
    ]


def write_normalized_parquet(
    path: Path,
    rows: Sequence[dict[str, Any]],
    *,
    symbol: str,
    utc_date: str,
    raw_zip_sha: str = "f" * 64,
    raw_manifest_sha: str = "9" * 64,
    gate_report_id: str = "test_phase4bb_d_gate_report",
    gate_report_sha: str = "8" * 64,
) -> None:
    """Write a 19-column normalized aggTrades Parquet file at *path*."""
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
        "dataset_version": ["v001"] * n,
        "source_dataset_family": ["microstructure_raw_aggtrades_v001"] * n,
        "source_dataset_version": ["v001"] * n,
        "symbol": [symbol] * n,
        "utc_date": [utc_date] * n,
        "agg_trade_id": [r["agg_trade_id"] for r in rows],
        "price": [r["price"] for r in rows],
        "quantity": [r["quantity"] for r in rows],
        "first_trade_id": [r["first_trade_id"] for r in rows],
        "last_trade_id": [r["last_trade_id"] for r in rows],
        "transact_time_ms": [r["transact_time_ms"] for r in rows],
        "is_buyer_maker": [r["is_buyer_maker"] for r in rows],
        "source_file_sha256": [raw_zip_sha] * n,
        "source_manifest_sha256": [raw_manifest_sha] * n,
        "source_gate_report_id": [gate_report_id] * n,
        "source_gate_report_sha256": [gate_report_sha] * n,
        "row_index": list(range(n)),
        "normalization_schema_version": ["v001"] * n,
    }
    table = pa.Table.from_pydict(data, schema=schema)
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path, compression="zstd")


def write_normalized_manifest(
    path: Path,
    *,
    symbol: str,
    utc_date: str,
    parquet_relative_path: str,
    parquet_sha256: str,
    row_count: int,
    start_time_ms: int,
    end_time_ms: int,
) -> None:
    """Write a Phase 4bd-shaped normalized manifest at *path*."""
    manifest = {
        "dataset_family": "microstructure_normalized_aggtrades_v001",
        "version": "v001",
        "symbol": symbol,
        "source": "derived_from_microstructure_raw_aggtrades_v001",
        "endpoint": "derived",
        "capture_mode": "derived",
        "schema_version": "v001",
        "endpoint_docs_reference": "derived_no_endpoint",
        "capture_config_hash": "x" * 64,
        "code_commit_sha": "0" * 40,
        "governance_labels": {
            "phase": "4bd",
            "source_phase_boundary": "4bb-D",
            "source_dataset_family": "microstructure_raw_aggtrades_v001",
            "source_dataset_version": "v001",
            "validator": "phase_4ax_aggtrades_v001",
            "stop_trigger_domain": "trade_price_backtest_candidate",
            "feature_computation": "forbidden",
            "strategy_use": "forbidden",
        },
        "start_time_ms": start_time_ms,
        "end_time_ms": end_time_ms,
        "event_count": row_count,
        "file_count": 1,
        "files": [
            {
                "path": parquet_relative_path,
                "sha256": parquet_sha256,
                "event_count": row_count,
                "start_time_ms": start_time_ms,
                "end_time_ms": end_time_ms,
            }
        ],
        "invalid_windows": [],
        "retention_warning": None,
        "proxy_warning": None,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, sort_keys=True, indent=2), encoding="utf-8")


def write_successor_state(
    path: Path,
    *,
    normalized_manifest_sha: str,
    normalized_parquet_sha: str,
) -> None:
    """Write a Phase 4bg-B-shaped successor-state JSON at *path*."""
    payload = {
        "schema_version": "v001",
        "phase_id": "4bg-B",
        "dataset_family": "microstructure_normalized_aggtrades_v001",
        "dataset_version": "v001",
        "successor_state_kind": "research_eligibility_successor_state",
        "successor_stage": "Stage-3",
        "successor_research_eligible": True,
        "successor_eligibility_gate_status": "pass",
        "original_manifest_sha256": normalized_manifest_sha,
        "original_manifest_research_eligible": False,
        "original_manifest_eligibility_gate_status": "pending",
        "raw_family_research_eligible": False,
        "raw_family_eligibility_gate_status": "pending",
        "raw_manifest_sha256": "9" * 64,
        "raw_zip_sha256": "f" * 64,
        "normalized_parquet_sha256": normalized_parquet_sha,
        "feature_computation": "forbidden",
        "labels": "forbidden",
        "ml": "forbidden",
        "strategy": "forbidden",
        "backtest": "forbidden",
        "acquisition": "unauthorized",
        "stage_4_feature_cleared": False,
        "no_successor_authorization": True,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")


def build_feature_fixture(
    tmp_path: Path,
    *,
    symbol: str = "BTCUSDT",
    utc_date: str = "2025-01-15",
    rows: Sequence[dict[str, Any]] | None = None,
) -> FeatureFixtureBundle:
    """Build a Phase 4bh feature mini-fixture under *tmp_path*."""
    rows_seq: list[dict[str, Any]] = list(rows or _default_rows(utc_date=utc_date))
    microstructure_root = tmp_path / "data" / "microstructure"
    normalized_root = microstructure_root / "normalized"
    manifests_root = microstructure_root / "manifests"
    features_root = microstructure_root / "features"
    successor_state_root = microstructure_root / "successor-state"
    for d in (
        normalized_root,
        manifests_root,
        features_root,
        successor_state_root,
    ):
        d.mkdir(parents=True, exist_ok=True)

    yyyy = utc_date.split("-", 1)[0]
    mm = utc_date.split("-")[1]
    family = "microstructure_normalized_aggtrades_v001"
    parquet_path = (
        normalized_root
        / family
        / symbol
        / yyyy
        / mm
        / f"{symbol}-aggTrades-{utc_date}.parquet"
    )
    write_normalized_parquet(parquet_path, rows_seq, symbol=symbol, utc_date=utc_date)
    parquet_sha = _hash_file(parquet_path)

    rel_parquet = (
        f"normalized/{family}/{symbol}/{yyyy}/{mm}/{symbol}-aggTrades-{utc_date}.parquet"
    )
    manifest_path = manifests_root / f"{family}__v001.json"
    write_normalized_manifest(
        manifest_path,
        symbol=symbol,
        utc_date=utc_date,
        parquet_relative_path=rel_parquet,
        parquet_sha256=parquet_sha,
        row_count=len(rows_seq),
        start_time_ms=int(rows_seq[0]["transact_time_ms"]),
        end_time_ms=int(rows_seq[-1]["transact_time_ms"]),
    )
    manifest_sha = _hash_file(manifest_path)

    successor_state_path = (
        successor_state_root
        / f"{family}__v001__stage3_research_eligible__phase-4bg-b.json"
    )
    write_successor_state(
        successor_state_path,
        normalized_manifest_sha=manifest_sha,
        normalized_parquet_sha=parquet_sha,
    )
    successor_state_sha = _hash_file(successor_state_path)

    feature_family = "microstructure_features_aggtrades_v001"
    feature_parquet_path = (
        features_root
        / feature_family
        / symbol
        / yyyy
        / mm
        / f"{symbol}-features-aggtrades-{utc_date}.parquet"
    )
    feature_manifest_path = manifests_root / f"{feature_family}__v001.json"

    return FeatureFixtureBundle(
        microstructure_root=microstructure_root,
        normalized_root=normalized_root,
        manifests_root=manifests_root,
        features_root=features_root,
        successor_state_root=successor_state_root,
        normalized_parquet_path=parquet_path,
        normalized_manifest_path=manifest_path,
        successor_state_path=successor_state_path,
        feature_parquet_path=feature_parquet_path,
        feature_manifest_path=feature_manifest_path,
        symbol=symbol,
        utc_date=utc_date,
        rows=tuple(rows_seq),
        row_count=len(rows_seq),
        normalized_parquet_sha256=parquet_sha,
        normalized_manifest_sha256=manifest_sha,
        successor_state_sha256=successor_state_sha,
    )


__all__ = [
    "SYNTHETIC_FEATURE_CONFIG_HASH",
    "SYNTHETIC_NORMALIZED_MANIFEST_SHA",
    "SYNTHETIC_NORMALIZED_PARQUET_SHA",
    "SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA",
    "SYNTHETIC_SUCCESSOR_STATE_SHA",
    "FeatureFixtureBundle",
    "build_feature_fixture",
    "write_normalized_manifest",
    "write_normalized_parquet",
    "write_successor_state",
]
