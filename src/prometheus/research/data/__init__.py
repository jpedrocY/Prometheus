"""Research data ingestion, normalization, storage, and validation.

Phase 2 scope: synthetic fixtures only. No network, no exchange, no
credentials.
"""

from .derive import derive_1h_from_15m
from .fetch import FixtureKlineSource, HistoricalKlineSource, RawKlineRow
from .manifests import DatasetManifest, InvalidWindow, read_manifest, write_manifest
from .normalize import normalize_rows
from .quality import (
    DuplicateReport,
    MissingWindow,
    check_no_duplicates,
    check_no_future_bars,
    check_no_missing_bars,
    check_timestamp_monotonic,
)
from .storage import (
    NORMALIZED_KLINE_ARROW_SCHEMA,
    NORMALIZED_KLINE_COLUMNS,
    attach_dataset_view,
    partition_path,
    read_klines,
    write_klines,
)

__all__ = [
    "DatasetManifest",
    "DuplicateReport",
    "FixtureKlineSource",
    "HistoricalKlineSource",
    "InvalidWindow",
    "MissingWindow",
    "NORMALIZED_KLINE_ARROW_SCHEMA",
    "NORMALIZED_KLINE_COLUMNS",
    "RawKlineRow",
    "attach_dataset_view",
    "check_no_duplicates",
    "check_no_future_bars",
    "check_no_missing_bars",
    "check_timestamp_monotonic",
    "derive_1h_from_15m",
    "normalize_rows",
    "partition_path",
    "read_klines",
    "read_manifest",
    "write_klines",
    "write_manifest",
]
