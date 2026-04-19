from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest

from prometheus.core.errors import DataIntegrityError
from prometheus.research.data.ingest import (
    _expected_bars_for_month,
    _is_kline_csv_header,
    _iter_months,
    extract_rows_from_zip,
    parse_binance_csv_row,
)

_HEADER_LINE = (
    "open_time,open,high,low,close,volume,close_time,quote_volume,"
    "count,taker_buy_volume,taker_buy_quote_volume,ignore"
)

# ---------------------------------------------------------------------------
# parse_binance_csv_row
# ---------------------------------------------------------------------------

# Open time | Open | High | Low | Close | Volume | Close time | Quote asset volume |
# Number of trades | Taker buy base asset volume | Taker buy quote asset volume | Ignore
_HAPPY_LINE = (
    "1774224000000,65000.0,65100.0,64900.0,65050.0,12.5,1774224899999,812500.0,42,6.0,390000.0,0"
)


def test_parse_happy() -> None:
    row = parse_binance_csv_row(_HAPPY_LINE, line_number=1)
    assert row["open_time"] == 1_774_224_000_000
    assert row["close_time"] == 1_774_224_899_999
    assert row["open"] == 65000.0
    assert row["trade_count"] == 42
    # No "ignore" field in the output — stripped.
    assert "ignore" not in row


def test_parse_rejects_wrong_column_count() -> None:
    short = _HAPPY_LINE.rsplit(",", 1)[0]  # drop trailing "Ignore" column
    with pytest.raises(DataIntegrityError) as exc_info:
        parse_binance_csv_row(short, line_number=5)
    assert "line 5" in str(exc_info.value)


def test_parse_rejects_non_numeric() -> None:
    parts = _HAPPY_LINE.split(",")
    parts[1] = "not-a-number"
    with pytest.raises(DataIntegrityError) as exc_info:
        parse_binance_csv_row(",".join(parts), line_number=7)
    assert "line 7" in str(exc_info.value)


# ---------------------------------------------------------------------------
# extract_rows_from_zip
# ---------------------------------------------------------------------------


def _make_zip(tmp_path: Path, *, member_name: str, body: str) -> Path:
    path = tmp_path / "sample.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(member_name, body)
    return path


def test_extract_single_member(tmp_path: Path) -> None:
    content = _HAPPY_LINE + "\n"
    zip_path = _make_zip(tmp_path, member_name="BTCUSDT-15m-2026-03.csv", body=content)
    rows = extract_rows_from_zip(zip_path)
    assert len(rows) == 1
    assert rows[0]["open_time"] == 1_774_224_000_000


def test_extract_rejects_multi_member(tmp_path: Path) -> None:
    path = tmp_path / "multi.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("a.csv", "x\n")
        archive.writestr("b.csv", "y\n")
    with pytest.raises(DataIntegrityError):
        extract_rows_from_zip(path)


def test_extract_ignores_blank_lines(tmp_path: Path) -> None:
    body = "\n" + _HAPPY_LINE + "\n\n" + _HAPPY_LINE + "\n"
    # Second line would duplicate the open_time; that's fine for THIS unit test
    # because we're only checking that blank lines are skipped, not uniqueness.
    zip_path = _make_zip(tmp_path, member_name="x.csv", body=body)
    rows = extract_rows_from_zip(zip_path)
    assert len(rows) == 2


def test_extract_empty_zip_rejects(tmp_path: Path) -> None:
    path = tmp_path / "empty.zip"
    with zipfile.ZipFile(path, "w"):
        pass
    with pytest.raises(DataIntegrityError):
        extract_rows_from_zip(path)


# ---------------------------------------------------------------------------
# Header-row handling (GAP-20260419-010)
# ---------------------------------------------------------------------------


def test_is_header_recognizes_open_time() -> None:
    assert _is_kline_csv_header(_HEADER_LINE) is True


def test_is_header_case_insensitive() -> None:
    assert _is_kline_csv_header(_HEADER_LINE.upper()) is True


def test_is_header_rejects_numeric_first_field() -> None:
    assert _is_kline_csv_header(_HAPPY_LINE) is False


def test_is_header_rejects_wrong_column_count() -> None:
    short = ",".join(_HEADER_LINE.split(",")[:5])
    assert _is_kline_csv_header(short) is False


def test_is_header_rejects_similar_but_wrong_name() -> None:
    # First field that isn't exactly "open_time" must not be treated as header.
    wrong = _HEADER_LINE.replace("open_time", "open", 1)
    assert _is_kline_csv_header(wrong) is False


def test_extract_skips_header_row(tmp_path: Path) -> None:
    body = _HEADER_LINE + "\n" + _HAPPY_LINE + "\n"
    path = _make_zip(tmp_path, member_name="x.csv", body=body)
    rows = extract_rows_from_zip(path)
    assert len(rows) == 1
    assert rows[0]["open_time"] == 1_774_224_000_000


def test_extract_works_without_header(tmp_path: Path) -> None:
    # Pre-existing behavior retained: header-absent files parse normally.
    body = (
        _HAPPY_LINE
        + "\n"
        + _HAPPY_LINE.replace("1774224000000", "1774224900000").replace(
            "1774224899999", "1774225799999"
        )
        + "\n"
    )
    path = _make_zip(tmp_path, member_name="x.csv", body=body)
    rows = extract_rows_from_zip(path)
    assert len(rows) == 2
    assert rows[0]["open_time"] == 1_774_224_000_000
    assert rows[1]["open_time"] == 1_774_224_900_000


def test_extract_header_skip_preserves_data_rows(tmp_path: Path) -> None:
    second = _HAPPY_LINE.replace("1774224000000", "1774224900000").replace(
        "1774224899999", "1774225799999"
    )
    with_header = _HEADER_LINE + "\n" + _HAPPY_LINE + "\n" + second + "\n"
    without_header = _HAPPY_LINE + "\n" + second + "\n"

    with_dir = tmp_path / "with"
    without_dir = tmp_path / "without"
    with_dir.mkdir()
    without_dir.mkdir()

    with_path = _make_zip(with_dir, member_name="x.csv", body=with_header)
    without_path = _make_zip(without_dir, member_name="x.csv", body=without_header)

    rows_with = extract_rows_from_zip(with_path)
    rows_without = extract_rows_from_zip(without_path)
    assert rows_with == rows_without


def test_extract_rejects_non_numeric_non_header_first_row(tmp_path: Path) -> None:
    # 12 columns but first field is not "open_time" and not numeric -> loud fail.
    bad_line = "hello,42.0,42.0,42.0,42.0,42.0,1774224899999,0.0,0,0.0,0.0,0"
    path = _make_zip(tmp_path, member_name="x.csv", body=bad_line + "\n" + _HAPPY_LINE + "\n")
    with pytest.raises(DataIntegrityError):
        extract_rows_from_zip(path)


def test_extract_rejects_wrong_column_count_first_row(tmp_path: Path) -> None:
    # Fewer columns -> not a header, not parseable data -> loud fail.
    bad_line = "open_time,open,high"  # 3 columns
    path = _make_zip(tmp_path, member_name="x.csv", body=bad_line + "\n" + _HAPPY_LINE + "\n")
    with pytest.raises(DataIntegrityError):
        extract_rows_from_zip(path)


# ---------------------------------------------------------------------------
# _iter_months
# ---------------------------------------------------------------------------


def test_iter_months_single_month() -> None:
    assert _iter_months(2026, 3, 2026, 3) == [(2026, 3)]


def test_iter_months_within_year() -> None:
    assert _iter_months(2026, 1, 2026, 3) == [(2026, 1), (2026, 2), (2026, 3)]


def test_iter_months_crosses_year() -> None:
    assert _iter_months(2025, 11, 2026, 2) == [
        (2025, 11),
        (2025, 12),
        (2026, 1),
        (2026, 2),
    ]


def test_iter_months_rejects_backwards() -> None:
    with pytest.raises(ValueError):
        _iter_months(2026, 5, 2026, 3)


# ---------------------------------------------------------------------------
# _expected_bars_for_month
# ---------------------------------------------------------------------------


def test_expected_bars_march_2026() -> None:
    from prometheus.core.intervals import Interval

    # 31 days * 96 bars/day for 15m
    assert _expected_bars_for_month(2026, 3, Interval.I_15M) == 31 * 96


def test_expected_bars_february_leap_2024() -> None:
    from prometheus.core.intervals import Interval

    assert _expected_bars_for_month(2024, 2, Interval.I_15M) == 29 * 96


def test_expected_bars_1h_interval() -> None:
    from prometheus.core.intervals import Interval

    # 31 days * 24 bars/day for 1h
    assert _expected_bars_for_month(2026, 3, Interval.I_1H) == 31 * 24


# ---------------------------------------------------------------------------
# Helper BytesIO-backed ZIP (reusable by integration test)
# ---------------------------------------------------------------------------


def make_zip_bytes(rows: list[str], *, member_name: str = "sample.csv") -> bytes:
    buf = io.BytesIO()
    body = "\n".join(rows) + "\n"
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member_name, body)
    return buf.getvalue()
