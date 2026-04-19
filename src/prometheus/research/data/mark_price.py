"""Mark-price kline bulk CSV parser and ingest helpers.

## TD-006 verification evidence (2026-04-19)

1. Path: ``data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYM>/<INTV>/``
   confirmed by direct fetch of
   ``https://data.binance.vision/data/futures/um/monthly/markPriceKlines/BTCUSDT/15m/BTCUSDT-15m-2024-01.zip.CHECKSUM``
   which returned 90 bytes (``aa64b8b7...698c926  BTCUSDT-15m-2024-01.zip``).
   Path segment ``markPriceKlines`` is distinct from standard klines'
   ``klines`` segment; the ZIP filename convention
   ``<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip`` is shared.

2. CHECKSUM format: identical to standard klines' two-space
   ``<sha256hex>  <filename>`` (verified 2026-04-19).

3. 2026-03 target files verified to exist on 2026-04-19:
   * BTCUSDT-15m-2026-03.zip sha256
     79edfb409a35630cfb8894b883c2bcc4d5a3d6f78bf4d449585cc9e6e8f475e3
   * ETHUSDT-15m-2026-03.zip sha256
     d30d71f35e0935783bedadcbc905537153c1e8980c1336a7c0403be12ba73762

4. CSV column layout: NOT documented in the github.com/binance/binance-public-data
   README (confirmed 2026-04-19). Mark-price klines from the REST endpoint
   ``/fapi/v1/markPriceKlines`` return 12-element arrays where most
   volume-related fields are placeholders (typically zero strings).
   The bulk CSV is assumed to mirror that 12-column layout; only
   ``open_time``, ``open``, ``high``, ``low``, ``close``, and ``close_time``
   carry meaningful values. The remaining 6 fields are ignored by this
   parser. Runtime first-row column-count check enforces 12; any
   divergence raises :class:`DataIntegrityError`.

5. Header-row handling mirrors GAP-20260419-010: defensive detection
   via ``_is_mark_price_csv_header`` (first field ``open_time``, exactly
   12 fields). Non-numeric non-header first rows fail loudly.
"""

from __future__ import annotations

import io
import zipfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval
from prometheus.core.mark_price_klines import MarkPriceKline
from prometheus.core.symbols import Symbol

_MARK_PRICE_CSV_COLUMNS = 12  # same positional shape as standard klines


def _is_mark_price_csv_header(line: str) -> bool:
    """Recognize a Binance mark-price kline CSV header row strictly.

    Matches GAP-20260419-010's discipline: require both a 12-column
    shape AND the first field normalized/lowercased equals ``open_time``.
    """
    parts = line.strip().split(",")
    if len(parts) != _MARK_PRICE_CSV_COLUMNS:
        return False
    return parts[0].strip().lower() == "open_time"


def parse_mark_price_csv_row(line: str, *, line_number: int) -> dict[str, Any]:
    """Parse a mark-price bulk CSV row into fields relevant to Prometheus.

    Fields extracted by position: open_time (0), open (1), high (2),
    low (3), close (4), close_time (6). All other positional fields
    (volume/trades/taker columns from the kline layout) are ignored
    because they are placeholder values for mark-price klines.

    Raises :class:`DataIntegrityError` on column-count mismatch or
    non-numeric numeric fields.
    """
    parts = line.strip().split(",")
    if len(parts) != _MARK_PRICE_CSV_COLUMNS:
        raise DataIntegrityError(
            f"mark-price CSV line {line_number}: expected "
            f"{_MARK_PRICE_CSV_COLUMNS} columns, got {len(parts)}"
        )
    try:
        return {
            "open_time": int(parts[0]),
            "open": float(parts[1]),
            "high": float(parts[2]),
            "low": float(parts[3]),
            "close": float(parts[4]),
            "close_time": int(parts[6]),
        }
    except ValueError as exc:
        raise DataIntegrityError(
            f"mark-price CSV line {line_number}: failed to cast numeric field ({exc})"
        ) from exc


def extract_mark_price_rows_from_zip(zip_path: Path) -> list[dict[str, Any]]:
    """Open a Binance mark-price bulk ZIP and parse its single CSV entry.

    Skips a recognized header row; raises on empty/multi-member archives
    and on non-numeric non-header first rows.
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
                    if _is_mark_price_csv_header(raw_line):
                        continue
                rows.append(parse_mark_price_csv_row(raw_line, line_number=index))
            return rows


def normalize_mark_price_rows(
    raw_rows: Sequence[dict[str, Any]],
    *,
    symbol: Symbol,
    interval: Interval,
    source: str,
) -> list[MarkPriceKline]:
    """Construct :class:`MarkPriceKline` values from parsed raw rows.

    Raises :class:`DataIntegrityError` with the row index if any
    :class:`MarkPriceKline` validator fails.
    """
    from pydantic import ValidationError

    result: list[MarkPriceKline] = []
    for index, row in enumerate(raw_rows):
        payload = {
            "symbol": symbol,
            "interval": interval,
            "source": source,
            "open_time": row["open_time"],
            "close_time": row["close_time"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
        }
        try:
            kline = MarkPriceKline.model_validate(payload)
        except ValidationError as exc:
            raise DataIntegrityError(
                f"mark-price row {index} failed validation: {exc.errors()}"
            ) from exc
        result.append(kline)
    return result
