"""Research data ingestion, normalization, storage, and validation.

Phase 2 scope: synthetic fixtures.
Phase 2b scope: Binance public bulk historical klines (no credentials).
"""

from .binance_bulk import (
    BulkDownloader,
    BulkDownloadError,
    DownloadOutcome,
    monthly_checksum_url,
    monthly_zip_filename,
    monthly_zip_url,
    parse_checksum_line,
)
from .derive import derive_1h_from_15m
from .download_state import (
    DownloadState,
    DownloadStateError,
    DownloadStatus,
    MonthDownloadState,
    read_or_init_state,
    read_state,
    write_state,
)
from .fetch import FixtureKlineSource, HistoricalKlineSource, RawKlineRow
from .ingest import (
    IngestMonthResult,
    IngestRangeResult,
    extract_rows_from_zip,
    ingest_monthly_range,
    parse_binance_csv_row,
)
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
    "BulkDownloadError",
    "BulkDownloader",
    "DatasetManifest",
    "DownloadOutcome",
    "DownloadState",
    "DownloadStateError",
    "DownloadStatus",
    "DuplicateReport",
    "FixtureKlineSource",
    "HistoricalKlineSource",
    "IngestMonthResult",
    "IngestRangeResult",
    "InvalidWindow",
    "MissingWindow",
    "MonthDownloadState",
    "NORMALIZED_KLINE_ARROW_SCHEMA",
    "NORMALIZED_KLINE_COLUMNS",
    "RawKlineRow",
    "attach_dataset_view",
    "check_no_duplicates",
    "check_no_future_bars",
    "check_no_missing_bars",
    "check_timestamp_monotonic",
    "derive_1h_from_15m",
    "extract_rows_from_zip",
    "ingest_monthly_range",
    "monthly_checksum_url",
    "monthly_zip_filename",
    "monthly_zip_url",
    "normalize_rows",
    "parse_binance_csv_row",
    "parse_checksum_line",
    "partition_path",
    "read_klines",
    "read_manifest",
    "read_or_init_state",
    "read_state",
    "write_klines",
    "write_manifest",
    "write_state",
]
