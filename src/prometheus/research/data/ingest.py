"""Phase 2b ingest orchestrator.

Drives the full Binance-bulk → Parquet pipeline for a single symbol/interval
monthly range. Reuses Phase 2 primitives:

    BulkDownloader (this package)
      -> extracted CSV rows
      -> parse_binance_csv_row
      -> normalize_rows (Phase 2)
      -> write_klines (Phase 2)
    read_klines + derive_1h_from_15m + write_klines
    DatasetManifest write (Phase 2)
"""

from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.core.time import utc_now_ms

from .binance_bulk import BulkDownloader
from .derive import derive_1h_from_15m
from .download_state import (
    DownloadState,
    DownloadStatus,
    MonthDownloadState,
    read_or_init_state,
    write_state,
)
from .manifests import DatasetManifest, InvalidWindow, write_manifest
from .normalize import normalize_rows
from .quality import (
    check_no_duplicates,
    check_no_future_bars,
    check_no_missing_bars,
    check_timestamp_monotonic,
)
from .storage import read_klines, write_klines

# ---------------------------------------------------------------------------
# Binance CSV parsing
# ---------------------------------------------------------------------------

_BINANCE_CSV_COLUMNS = 12  # open_time, O, H, L, C, volume, close_time, quote_vol,
# trade_count, taker_buy_base_vol, taker_buy_quote_vol, ignore


def parse_binance_csv_row(line: str, *, line_number: int) -> dict[str, Any]:
    """Parse a single Binance public-bulk CSV row into a normalize-compatible dict.

    Raises :class:`DataIntegrityError` on column-count mismatch or
    non-numeric numeric fields. The CSV has no header row.
    """
    parts = line.strip().split(",")
    if len(parts) != _BINANCE_CSV_COLUMNS:
        raise DataIntegrityError(
            f"CSV line {line_number}: expected {_BINANCE_CSV_COLUMNS} columns, got {len(parts)}"
        )
    try:
        return {
            "open_time": int(parts[0]),
            "open": float(parts[1]),
            "high": float(parts[2]),
            "low": float(parts[3]),
            "close": float(parts[4]),
            "volume": float(parts[5]),
            "close_time": int(parts[6]),
            "quote_asset_volume": float(parts[7]),
            "trade_count": int(parts[8]),
            "taker_buy_base_volume": float(parts[9]),
            "taker_buy_quote_volume": float(parts[10]),
        }
    except ValueError as exc:
        raise DataIntegrityError(
            f"CSV line {line_number}: failed to cast numeric field ({exc})"
        ) from exc


def _is_kline_csv_header(line: str) -> bool:
    """Return True iff ``line`` is a Binance kline CSV header row.

    Recognized strictly: the first field must normalize to ``"open_time"``
    (case-insensitive, whitespace-stripped) AND the total field count must
    match the expected 12-column Binance layout. Any other non-numeric
    first row is NOT silently skipped; the downstream parser will raise
    :class:`DataIntegrityError` on it.

    See GAP-20260419-010: real BTCUSDT-15m-2026-03 CSV was observed to
    contain a header row as its first line. Older files may or may not.
    """
    parts = line.strip().split(",")
    if len(parts) != _BINANCE_CSV_COLUMNS:
        return False
    return parts[0].strip().lower() == "open_time"


def extract_rows_from_zip(zip_path: Path) -> list[dict[str, Any]]:
    """Open a Binance bulk ZIP and parse its single CSV entry.

    The README does not document the internal filename convention, so
    this opens whatever single member the archive contains. If the first
    non-empty line is a recognized kline header it is skipped; otherwise
    it is parsed as data. Any non-numeric, non-header first row raises
    :class:`DataIntegrityError` (loud failure, no silent skipping).

    Raises :class:`DataIntegrityError` on empty/multi-member archives.
    """
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        if len(names) != 1:
            raise DataIntegrityError(f"expected exactly one member in {zip_path}, got {names}")
        with archive.open(names[0]) as fh:
            text_stream = io.TextIOWrapper(fh, encoding="utf-8", newline="")
            rows: list[dict[str, Any]] = []
            seen_non_empty = False
            for index, raw_line in enumerate(text_stream, start=1):
                if not raw_line.strip():
                    continue
                if not seen_non_empty:
                    seen_non_empty = True
                    if _is_kline_csv_header(raw_line):
                        # Skip the recognized header; continue to data rows.
                        continue
                rows.append(parse_binance_csv_row(raw_line, line_number=index))
            return rows


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def _iter_months(
    start_year: int, start_month: int, end_year: int, end_month: int
) -> list[tuple[int, int]]:
    if (start_year, start_month) > (end_year, end_month):
        raise ValueError("start must be <= end")
    result: list[tuple[int, int]] = []
    year, month = start_year, start_month
    while (year, month) <= (end_year, end_month):
        result.append((year, month))
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    return result


def _expected_bars_for_month(year: int, month: int, interval: Interval) -> int:
    # Days in month (proleptic Gregorian): Python's calendar handles this.
    import calendar

    days = calendar.monthrange(year, month)[1]
    return days * 24 * 60 * 60 * 1000 // interval_duration_ms(interval)


@dataclass(frozen=True)
class IngestMonthResult:
    year: int
    month: int
    zip_url: str
    zip_sha256: str
    row_count: int
    normalized_path: Path
    was_cached: bool


@dataclass(frozen=True)
class IngestRangeResult:
    symbol: Symbol
    interval: Interval
    months: list[IngestMonthResult]
    total_row_count: int
    invalid_windows_15m: list[InvalidWindow]
    derived_1h_row_count: int
    derived_invalid_windows: list[InvalidWindow]
    manifest_15m_path: Path
    manifest_1h_path: Path


def ingest_monthly_range(
    downloader: BulkDownloader,
    *,
    symbol: Symbol,
    interval: Interval,
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    normalized_root: Path,
    derived_root: Path,
    manifests_root: Path,
    state_root: Path,
    dataset_version_15m: str,
    dataset_version_1h: str,
    schema_version: str = "kline_v1",
    pipeline_version: str = "prometheus@0.0.0",
) -> IngestRangeResult:
    """Download, normalize, derive, manifest a month range for one symbol/interval.

    Idempotent: months already in ``NORMALIZED`` state are skipped. The
    1h derivation runs over the full symbol range after all monthly
    writes complete, then is written to ``derived_root``.
    """
    if interval is not Interval.I_15M:
        raise ValueError("Phase 2b ingest supports only Interval.I_15M in 2b scope")

    dataset_name_15m = dataset_version_15m.rsplit("__v", 1)[0]
    dataset_name_1h = dataset_version_1h.rsplit("__v", 1)[0]
    state_path = state_root / f"{dataset_name_15m}__state.json"
    state = read_or_init_state(state_path, dataset_name_15m, utc_now_ms())

    month_results: list[IngestMonthResult] = []
    invalid_windows_15m: list[InvalidWindow] = []
    source_urls: list[str] = []

    for year, month in _iter_months(start_year, start_month, end_year, end_month):
        existing_status = state.status_for(year, month)
        if existing_status is DownloadStatus.NORMALIZED:
            normalized_path = _month_normalized_path(normalized_root, symbol, interval, year, month)
            existing_record = state.months[f"{year:04d}-{month:02d}"]
            assert existing_record.zip_sha256 is not None
            assert existing_record.row_count is not None
            month_results.append(
                IngestMonthResult(
                    year=year,
                    month=month,
                    zip_url=_zip_url(downloader, symbol, interval, year, month),
                    zip_sha256=existing_record.zip_sha256,
                    row_count=existing_record.row_count,
                    normalized_path=normalized_path,
                    was_cached=True,
                )
            )
            source_urls.append(_zip_url(downloader, symbol, interval, year, month))
            continue

        outcome = downloader.download_month(symbol, interval, year, month)
        source_urls.append(outcome.url)

        state = state.with_month(
            year,
            month,
            MonthDownloadState(
                status=DownloadStatus.VERIFIED,
                zip_sha256=outcome.sha256,
                downloaded_at_utc_ms=utc_now_ms(),
                verified_at_utc_ms=utc_now_ms(),
                raw_path=str(outcome.local_path),
            ),
            utc_now_ms(),
        )
        write_state(state_path, state)

        raw_rows = extract_rows_from_zip(outcome.local_path)
        klines = normalize_rows(raw_rows, symbol=symbol, interval=interval, source=outcome.url)

        if not klines:
            raise DataIntegrityError(f"no rows extracted from {outcome.local_path}")

        expected = _expected_bars_for_month(year, month, interval)
        if len(klines) != expected:
            invalid_windows_15m.append(
                InvalidWindow(
                    start_open_time_ms=klines[0].open_time,
                    end_open_time_ms=klines[-1].open_time,
                    reason=f"row_count_mismatch:got_{len(klines)}_expected_{expected}",
                )
            )

        written = write_klines(
            normalized_root,
            klines,
            dataset_version=dataset_version_15m,
            schema_version=schema_version,
            pipeline_version=pipeline_version,
        )
        assert len(written) == 1
        normalized_path = written[0]

        state = state.with_month(
            year,
            month,
            MonthDownloadState(
                status=DownloadStatus.NORMALIZED,
                zip_sha256=outcome.sha256,
                downloaded_at_utc_ms=utc_now_ms(),
                verified_at_utc_ms=utc_now_ms(),
                normalized_at_utc_ms=utc_now_ms(),
                raw_path=str(outcome.local_path),
                normalized_path=str(normalized_path),
                row_count=len(klines),
            ),
            utc_now_ms(),
        )
        write_state(state_path, state)

        month_results.append(
            IngestMonthResult(
                year=year,
                month=month,
                zip_url=outcome.url,
                zip_sha256=outcome.sha256,
                row_count=len(klines),
                normalized_path=normalized_path,
                was_cached=outcome.was_cached,
            )
        )

    # After monthly writes, run range-wide quality checks.
    all_klines: list[NormalizedKline] = read_klines(
        normalized_root, symbol=symbol, interval=interval
    )
    invalid_windows_15m.extend(_invalid_windows_from_checks(all_klines, interval, month_results))

    # Derive 1h bars from the full range.
    derived_1h, derive_invalid_windows = derive_1h_from_15m(all_klines)
    if derived_1h:
        write_klines(
            derived_root,
            derived_1h,
            dataset_version=dataset_version_1h,
            schema_version=schema_version,
            pipeline_version=pipeline_version,
        )

    # Write manifests.
    manifest_15m_path = manifests_root / f"{dataset_version_15m}.manifest.json"
    manifest_1h_path = manifests_root / f"{dataset_version_1h}.manifest.json"

    if not manifest_15m_path.exists():
        write_manifest(
            manifest_15m_path,
            _build_manifest(
                dataset_name=dataset_name_15m,
                dataset_version=dataset_version_15m,
                category="normalized_kline",
                symbol=symbol,
                interval=interval,
                sources=source_urls,
                schema_version=schema_version,
                pipeline_version=pipeline_version,
                invalid_windows=invalid_windows_15m,
                notes=(
                    f"Phase 2b bulk ingest from data.binance.vision. "
                    f"Months: {start_year:04d}-{start_month:02d} to "
                    f"{end_year:04d}-{end_month:02d}."
                ),
            ),
        )

    if not manifest_1h_path.exists():
        write_manifest(
            manifest_1h_path,
            _build_manifest(
                dataset_name=dataset_name_1h,
                dataset_version=dataset_version_1h,
                category="derived_kline",
                symbol=symbol,
                interval=Interval.I_1H,
                sources=[f"derived:{dataset_version_15m}"],
                schema_version=schema_version,
                pipeline_version=pipeline_version,
                invalid_windows=list(derive_invalid_windows),
                notes=(
                    f"Derived 1h bars from {dataset_version_15m}. "
                    f"Partial 1h buckets recorded as invalid_windows."
                ),
            ),
        )

    return IngestRangeResult(
        symbol=symbol,
        interval=interval,
        months=month_results,
        total_row_count=sum(m.row_count for m in month_results),
        invalid_windows_15m=invalid_windows_15m,
        derived_1h_row_count=len(derived_1h),
        derived_invalid_windows=list(derive_invalid_windows),
        manifest_15m_path=manifest_15m_path,
        manifest_1h_path=manifest_1h_path,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _zip_url(
    downloader: BulkDownloader,
    symbol: Symbol,
    interval: Interval,
    year: int,
    month: int,
) -> str:
    from .binance_bulk import monthly_zip_url as _u

    return _u(symbol, interval, year, month, base_url=downloader._base_url)  # noqa: SLF001


def _month_normalized_path(
    normalized_root: Path,
    symbol: Symbol,
    interval: Interval,
    year: int,
    month: int,
) -> Path:
    return (
        normalized_root
        / f"symbol={symbol.value}"
        / f"interval={interval.value}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / "part-0000.parquet"
    )


def _invalid_windows_from_checks(
    klines: list[NormalizedKline],
    interval: Interval,
    month_results: list[IngestMonthResult],
) -> list[InvalidWindow]:
    if not klines:
        return []
    invalid: list[InvalidWindow] = []

    duplicates = check_no_duplicates(klines)
    for d in duplicates:
        invalid.append(
            InvalidWindow(
                start_open_time_ms=d.open_time,
                end_open_time_ms=d.open_time,
                reason=f"duplicate_bar:count_{d.count}",
            )
        )

    monotonic_violations = check_timestamp_monotonic(klines)
    for previous, current in monotonic_violations:
        invalid.append(
            InvalidWindow(
                start_open_time_ms=min(previous, current),
                end_open_time_ms=max(previous, current),
                reason="non_monotonic_timestamps",
            )
        )

    future_bars = check_no_future_bars(klines, now_ms=utc_now_ms())
    for fb in future_bars:
        invalid.append(
            InvalidWindow(
                start_open_time_ms=fb.open_time,
                end_open_time_ms=fb.open_time,
                reason="future_open_time",
            )
        )

    # Per-month missing-bar check covers only the downloaded range.
    for mr in month_results:
        first_ms = klines[0].open_time
        last_ms = klines[-1].open_time
        # Bound to this result's month range.
        expected_start = max(first_ms, _first_bar_of_month(mr.year, mr.month))
        expected_end = min(last_ms, _last_bar_of_month(mr.year, mr.month, interval))
        if expected_end < expected_start:
            continue
        missing = check_no_missing_bars(
            klines,
            expected_start_ms=expected_start,
            expected_end_ms=expected_end,
            interval=interval,
        )
        for m in missing:
            invalid.append(
                InvalidWindow(
                    start_open_time_ms=m.start_open_time_ms,
                    end_open_time_ms=m.end_open_time_ms,
                    reason=f"missing_bars:count_{m.missing_count}",
                )
            )

    return invalid


def _first_bar_of_month(year: int, month: int) -> int:
    import datetime as dt

    return int(dt.datetime(year, month, 1, tzinfo=dt.UTC).timestamp() * 1000)


def _last_bar_of_month(year: int, month: int, interval: Interval) -> int:
    import calendar

    days = calendar.monthrange(year, month)[1]
    first = _first_bar_of_month(year, month)
    return first + (days * 24 * 60 * 60 * 1000) - interval_duration_ms(interval)


def _build_manifest(
    *,
    dataset_name: str,
    dataset_version: str,
    category: str,
    symbol: Symbol,
    interval: Interval,
    sources: list[str],
    schema_version: str,
    pipeline_version: str,
    invalid_windows: list[InvalidWindow],
    notes: str,
) -> DatasetManifest:
    return DatasetManifest(
        dataset_name=dataset_name,
        dataset_version=dataset_version,
        dataset_category=category,
        created_at_utc_ms=utc_now_ms(),
        canonical_timezone="UTC",
        canonical_timestamp_format="unix_milliseconds",
        symbols=(symbol,),
        intervals=(interval,),
        sources=tuple(sources),
        schema_version=schema_version,
        pipeline_version=pipeline_version,
        partitioning=("symbol", "interval", "year", "month"),
        primary_key=("symbol", "interval", "open_time"),
        generator="prometheus.research.data.ingest.ingest_monthly_range",
        predecessor_version=None,
        invalid_windows=tuple(invalid_windows),
        notes=notes,
    )


__all__ = [
    "IngestMonthResult",
    "IngestRangeResult",
    "extract_rows_from_zip",
    "ingest_monthly_range",
    "parse_binance_csv_row",
]


# Re-export DownloadState to satisfy the ingest orchestrator's dependency
# graph for downstream tools that import the orchestrator module directly.
_ = DownloadState  # re-export marker, no-op
