from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.binance_bulk import (
    BulkFamily,
    monthly_checksum_url,
    monthly_zip_url,
)
from prometheus.research.data.mark_price import (
    _is_mark_price_csv_header,
    extract_mark_price_rows_from_zip,
    normalize_mark_price_rows,
    parse_mark_price_csv_row,
)

ANCHOR_MS = 1_774_224_000_000

_HEADER = (
    "open_time,open,high,low,close,volume,close_time,quote_volume,count,"
    "taker_buy_volume,taker_buy_quote_volume,ignore"
)
_ROW = f"{ANCHOR_MS},65000.0,65100.0,64900.0,65050.0,0,{ANCHOR_MS + 15 * 60 * 1000 - 1},0,0,0,0,0"


# ---------------------------------------------------------------------------
# URL construction via family
# ---------------------------------------------------------------------------


def test_mark_price_zip_url_uses_markPriceKlines_path() -> None:
    url = monthly_zip_url(
        Symbol.BTCUSDT,
        Interval.I_15M,
        2026,
        3,
        family=BulkFamily.MARK_PRICE_KLINES,
    )
    assert url == (
        "https://data.binance.vision/data/futures/um/monthly/markPriceKlines/"
        "BTCUSDT/15m/BTCUSDT-15m-2026-03.zip"
    )


def test_mark_price_checksum_url_uses_markPriceKlines_path() -> None:
    url = monthly_checksum_url(
        Symbol.ETHUSDT,
        Interval.I_15M,
        2026,
        3,
        family=BulkFamily.MARK_PRICE_KLINES,
    )
    assert url.endswith("markPriceKlines/ETHUSDT/15m/ETHUSDT-15m-2026-03.zip.CHECKSUM")


def test_standard_klines_family_url_unchanged() -> None:
    # Phase 2b default behavior must not drift.
    url = monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    assert "monthly/klines/" in url
    assert "markPriceKlines" not in url


# ---------------------------------------------------------------------------
# Header detection + CSV row parse
# ---------------------------------------------------------------------------


def test_is_mark_price_csv_header_happy() -> None:
    assert _is_mark_price_csv_header(_HEADER) is True


def test_is_mark_price_csv_header_rejects_numeric_first_field() -> None:
    assert _is_mark_price_csv_header(_ROW) is False


def test_is_mark_price_csv_header_rejects_wrong_column_count() -> None:
    short = ",".join(_HEADER.split(",")[:5])
    assert _is_mark_price_csv_header(short) is False


def test_parse_happy() -> None:
    row = parse_mark_price_csv_row(_ROW, line_number=1)
    assert row["open_time"] == ANCHOR_MS
    assert row["close_time"] == ANCHOR_MS + 15 * 60 * 1000 - 1
    assert row["open"] == 65000.0
    # volume / trade_count / taker fields are not present in the output.
    for forbidden in ("volume", "trade_count", "taker_buy_base_volume"):
        assert forbidden not in row


def test_parse_rejects_wrong_column_count() -> None:
    short = ",".join(_ROW.split(",")[:5])
    with pytest.raises(DataIntegrityError):
        parse_mark_price_csv_row(short, line_number=3)


def test_parse_rejects_non_numeric() -> None:
    parts = _ROW.split(",")
    parts[1] = "xyz"
    with pytest.raises(DataIntegrityError):
        parse_mark_price_csv_row(",".join(parts), line_number=7)


# ---------------------------------------------------------------------------
# ZIP extraction
# ---------------------------------------------------------------------------


def _make_zip(tmp_path: Path, *, member_name: str, body: str) -> Path:
    path = tmp_path / "mp.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(member_name, body)
    return path


def test_extract_header_is_skipped(tmp_path: Path) -> None:
    body = _HEADER + "\n" + _ROW + "\n"
    zp = _make_zip(tmp_path, member_name="x.csv", body=body)
    rows = extract_mark_price_rows_from_zip(zp)
    assert len(rows) == 1
    assert rows[0]["open_time"] == ANCHOR_MS


def test_extract_without_header(tmp_path: Path) -> None:
    body = _ROW + "\n"
    zp = _make_zip(tmp_path, member_name="x.csv", body=body)
    rows = extract_mark_price_rows_from_zip(zp)
    assert len(rows) == 1


def test_extract_rejects_multi_member(tmp_path: Path) -> None:
    path = tmp_path / "multi.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("a.csv", "x\n")
        archive.writestr("b.csv", "y\n")
    with pytest.raises(DataIntegrityError):
        extract_mark_price_rows_from_zip(path)


def test_extract_rejects_non_header_non_numeric_first_row(tmp_path: Path) -> None:
    bad = "hello,42,42,42,42,0,1,0,0,0,0,0"
    zp = _make_zip(tmp_path, member_name="x.csv", body=bad + "\n" + _ROW + "\n")
    with pytest.raises(DataIntegrityError):
        extract_mark_price_rows_from_zip(zp)


# ---------------------------------------------------------------------------
# Normalization to MarkPriceKline
# ---------------------------------------------------------------------------


def test_normalize_builds_valid_mark_price_kline() -> None:
    raw = parse_mark_price_csv_row(_ROW, line_number=1)
    klines = normalize_mark_price_rows(
        [raw], symbol=Symbol.BTCUSDT, interval=Interval.I_15M, source="test"
    )
    assert len(klines) == 1
    assert klines[0].symbol is Symbol.BTCUSDT
    assert klines[0].open_time == ANCHOR_MS


def test_normalize_reports_row_index_on_validation_failure() -> None:
    bad_raw = {
        "open_time": ANCHOR_MS,
        "close_time": ANCHOR_MS + 99,  # wrong close_time
        "open": 65000.0,
        "high": 65100.0,
        "low": 64900.0,
        "close": 65050.0,
    }
    with pytest.raises(DataIntegrityError) as exc_info:
        normalize_mark_price_rows(
            [bad_raw], symbol=Symbol.BTCUSDT, interval=Interval.I_15M, source="test"
        )
    assert "row 0" in str(exc_info.value)
