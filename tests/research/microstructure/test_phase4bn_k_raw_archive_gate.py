"""Offline tests for the Phase 4bn-K pre-v002 raw archive eligibility gate.

All tests are offline and never read the real project
``data/microstructure/`` tree, never touch any v002 terminal-window or
sealed-test artefact, and never contact any endpoint. They exercise the
gate's pure helpers (date-list discipline, segment boundary guard, UTC
day windows, canonical sidecar parsing, CSV header/row decoding, path
discipline, zip-basename layout, result-state mapping) and the
fail-closed boundary behaviour of ``validate_one_file`` on an
out-of-segment date (which returns before any filesystem access).
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from scripts import phase4bn_k_validate_pre_v002_raw_archive_gate as gate
from scripts.phase4bn_k_validate_pre_v002_raw_archive_gate import (
    DATE_COUNT,
    DATE_END,
    DATE_START,
    EXPECTED_FILE_COUNT,
    EXPECTED_TOTAL_ROW_COUNT,
    EXPECTED_TOTAL_SIZE_BYTES,
    V002_TERMINAL_START,
    AggTradeValidationError,
    GateRuntimeError,
    PerFileResult,
    _check_zip_basename_layout,
    _coerce_buyer_is_maker,
    _gate_result_state,
    _resolve_header_mapping,
    _row_to_payload,
    _sample_validate,
    assert_relative_under_microstructure,
    generate_expected_date_list,
    is_within_segment,
    parse_canonical_sidecar,
    utc_day_window_ms,
    validate_one_file,
)

_HEADER = [
    "agg_trade_id",
    "price",
    "quantity",
    "first_trade_id",
    "last_trade_id",
    "transact_time",
    "is_buyer_maker",
]


# --------------------------------------------------------------------------- #
# Locked-scope constants
# --------------------------------------------------------------------------- #


def test_locked_scope_constants() -> None:
    assert DATE_START == "2024-03-01"
    assert DATE_END == "2024-11-30"
    assert DATE_COUNT == 275
    assert EXPECTED_FILE_COUNT == 275
    assert V002_TERMINAL_START == "2024-12-01"
    assert EXPECTED_TOTAL_ROW_COUNT == 400_001_695
    assert EXPECTED_TOTAL_SIZE_BYTES == 5_140_686_147


# --------------------------------------------------------------------------- #
# Date list discipline
# --------------------------------------------------------------------------- #


def test_generate_expected_date_list_is_275_contiguous() -> None:
    dates = generate_expected_date_list(DATE_START, DATE_END)
    assert len(dates) == DATE_COUNT
    assert dates[0] == DATE_START
    assert dates[-1] == DATE_END
    # contiguity
    for prev, nxt in zip(dates, dates[1:], strict=False):
        assert date.fromisoformat(nxt) - date.fromisoformat(prev) == timedelta(days=1)
    # no duplicates
    assert len(set(dates)) == DATE_COUNT


def test_generate_expected_date_list_rejects_reversed() -> None:
    with pytest.raises(GateRuntimeError):
        generate_expected_date_list("2024-11-30", "2024-03-01")


def test_no_generated_date_reaches_terminal_window() -> None:
    dates = generate_expected_date_list(DATE_START, DATE_END)
    assert all(d < V002_TERMINAL_START for d in dates)


# --------------------------------------------------------------------------- #
# Segment boundary guard
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "d,expected",
    [
        ("2024-03-01", True),
        ("2024-07-15", True),
        ("2024-11-30", True),
        ("2024-12-01", False),  # v002 terminal window start
        ("2025-01-15", False),  # inside v002 terminal window
        ("2025-02-14", False),  # sealed test split start
        ("2025-02-28", False),  # sealed test split end
        ("2024-02-29", False),  # before segment
    ],
)
def test_is_within_segment(d: str, expected: bool) -> None:
    assert is_within_segment(d) is expected


def test_validate_one_file_fails_closed_on_terminal_date_without_io() -> None:
    """An out-of-segment date must fail closed and never open a file."""
    entry = {
        "date": "2024-12-01",
        "local_zip_path": "microstructure/raw/should/never/be/opened.zip",
        "local_sidecar_path": "microstructure/raw/should/never/opened.zip.sha256",
        "sha256": "0" * 64,
        "sha256_from_companion": "0" * 64,
        "size_bytes": 1,
        "row_count": 1,
        "first_trade_time_ms": 1,
        "last_trade_time_ms": 1,
        "min_agg_trade_id": 1,
        "max_agg_trade_id": 1,
    }
    result = validate_one_file(entry, sample_head=4, sample_tail=4)
    assert result.status == "fail"
    assert result.path_layout_error is not None
    assert "boundary fail-closed" in result.path_layout_error


def test_validate_one_file_fails_closed_on_sealed_split_date() -> None:
    entry = {
        "date": "2025-02-20",
        "local_zip_path": "microstructure/raw/x/2025/02/BTCUSDT-aggTrades-2025-02-20.zip",
        "local_sidecar_path": "microstructure/raw/x.sha256",
        "sha256": "0" * 64,
        "sha256_from_companion": "0" * 64,
        "size_bytes": 1,
        "row_count": 1,
        "first_trade_time_ms": 1,
        "last_trade_time_ms": 1,
        "min_agg_trade_id": 1,
        "max_agg_trade_id": 1,
    }
    result = validate_one_file(entry, sample_head=4, sample_tail=4)
    assert result.status == "fail"
    assert result.path_layout_error is not None


# --------------------------------------------------------------------------- #
# UTC day window
# --------------------------------------------------------------------------- #


def test_utc_day_window_ms_half_open() -> None:
    start, end = utc_day_window_ms("2024-03-01")
    assert start == 1709251200000  # 2024-03-01T00:00:00Z
    assert end == 1709337600000  # 2024-03-02T00:00:00Z
    assert end - start == 86_400_000


# --------------------------------------------------------------------------- #
# Canonical sidecar parsing
# --------------------------------------------------------------------------- #


def test_parse_canonical_sidecar_ok() -> None:
    sha = "a" * 64
    sha_out, base = parse_canonical_sidecar(f"{sha}  BTCUSDT-aggTrades-2024-03-01.zip\n")
    assert sha_out == sha
    assert base == "BTCUSDT-aggTrades-2024-03-01.zip"


@pytest.mark.parametrize(
    "text",
    [
        "a" * 64 + " base.zip\n",  # single space
        "a" * 64 + "  base.zip",  # missing trailing newline
        "a" * 63 + "  base.zip\n",  # short sha
        "﻿" + "a" * 64 + "  base.zip\n",  # BOM
        "A" * 64 + "  base.zip\n",  # upper-case hex not matched by regex
        "a" * 64 + "  base.zip\r\n",  # CRLF
    ],
)
def test_parse_canonical_sidecar_rejects_malformed(text: str) -> None:
    with pytest.raises(GateRuntimeError):
        parse_canonical_sidecar(text)


# --------------------------------------------------------------------------- #
# CSV header / row decoding
# --------------------------------------------------------------------------- #


def test_resolve_header_mapping_detects_header() -> None:
    mapping = _resolve_header_mapping(_HEADER)
    assert mapping is not None
    assert mapping == {"a": 0, "p": 1, "q": 2, "f": 3, "l": 4, "T": 5, "m": 6}


def test_resolve_header_mapping_headerless_returns_none() -> None:
    data_row = ["2041763940", "61203.4", "0.663", "1", "2", "1709251200019", "false"]
    assert _resolve_header_mapping(data_row) is None


def test_resolve_header_mapping_missing_field_raises() -> None:
    with pytest.raises(GateRuntimeError):
        _resolve_header_mapping(["agg_trade_id", "price", "quantity"])


@pytest.mark.parametrize(
    "token,expected",
    [("true", True), ("True", True), ("TRUE", True),
     ("false", False), ("False", False), ("FALSE", False)],
)
def test_coerce_buyer_is_maker_ok(token: str, expected: bool) -> None:
    assert _coerce_buyer_is_maker(token) is expected


def test_coerce_buyer_is_maker_rejects_garbage() -> None:
    with pytest.raises(AggTradeValidationError):
        _coerce_buyer_is_maker("maybe")


def test_row_to_payload_headerless_and_mapped_agree() -> None:
    row = ["2041763940", "61203.4", "0.663", "10", "11", "1709251200019", "false"]
    p_headerless = _row_to_payload(row, None)
    mapping = _resolve_header_mapping(_HEADER)
    p_mapped = _row_to_payload(row, mapping)
    assert p_headerless == p_mapped
    assert p_headerless["a"] == "2041763940"
    assert p_headerless["T"] == "1709251200019"
    assert p_headerless["m"] is False


def test_row_to_payload_short_row_raises() -> None:
    with pytest.raises(GateRuntimeError):
        _row_to_payload(["1", "2", "3"], None)


# --------------------------------------------------------------------------- #
# Bounded Phase 4ax sample validation
# --------------------------------------------------------------------------- #


def test_sample_validate_accepts_valid_row() -> None:
    result = PerFileResult(date="2024-03-01", local_zip_path="x", local_sidecar_path="y")
    row = ["2041763940", "61203.4", "0.663", "10", "11", "1709251200019", "false"]
    _sample_validate(row, None, 0, result)
    assert result.status != "fail"
    assert result.rows_sampled_validated == 1
    assert result.schema_validation_errors == 0


def test_sample_validate_rejects_bad_price() -> None:
    result = PerFileResult(date="2024-03-01", local_zip_path="x", local_sidecar_path="y")
    row = ["2041763940", "not-a-number", "0.663", "10", "11", "1709251200019", "false"]
    _sample_validate(row, None, 0, result)
    assert result.status == "fail"
    assert result.schema_validation_errors == 1


# --------------------------------------------------------------------------- #
# Path discipline
# --------------------------------------------------------------------------- #


def test_assert_relative_under_microstructure_ok() -> None:
    rel = (
        "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/03/"
        "BTCUSDT-aggTrades-2024-03-01.zip"
    )
    resolved = assert_relative_under_microstructure(rel, label="zip")
    assert resolved.as_posix().endswith(rel)


@pytest.mark.parametrize(
    "rel",
    [
        "raw/x.zip",  # not under microstructure/
        "/microstructure/raw/x.zip",  # absolute
        "./microstructure/raw/x.zip",  # dot-prefixed
        "microstructure\\raw\\x.zip",  # backslash
        "microstructure/../secrets.zip",  # parent ref
        "microstructure/raw/.hidden/x.zip",  # dotfile
    ],
)
def test_assert_relative_under_microstructure_rejects(rel: str) -> None:
    with pytest.raises(GateRuntimeError):
        assert_relative_under_microstructure(rel, label="zip")


# --------------------------------------------------------------------------- #
# Zip basename / path layout
# --------------------------------------------------------------------------- #


def test_check_zip_basename_layout_ok() -> None:
    result = PerFileResult(date="2024-03-01", local_zip_path="", local_sidecar_path="")
    rel = (
        "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/03/"
        "BTCUSDT-aggTrades-2024-03-01.zip"
    )
    _check_zip_basename_layout("2024-03-01", rel, result)
    assert result.path_layout_error is None


@pytest.mark.parametrize(
    "date_str,rel",
    [
        ("2024-03-01", "microstructure/raw/other/BTCUSDT-aggTrades-2024-03-01.zip"),
        (
            "2024-03-01",
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/03/"
            "ETHUSDT-aggTrades-2024-03-01.zip",
        ),
        (
            "2024-03-01",
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/04/"
            "BTCUSDT-aggTrades-2024-03-01.zip",
        ),  # month dir mismatch
        (
            "2024-03-02",
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/03/"
            "BTCUSDT-aggTrades-2024-03-01.zip",
        ),  # basename date != inventory date
    ],
)
def test_check_zip_basename_layout_rejects(date_str: str, rel: str) -> None:
    result = PerFileResult(date=date_str, local_zip_path="", local_sidecar_path="")
    _check_zip_basename_layout(date_str, rel, result)
    assert result.path_layout_error is not None


# --------------------------------------------------------------------------- #
# Result-state mapping
# --------------------------------------------------------------------------- #


def test_gate_result_state_mapping() -> None:
    assert _gate_result_state("pass") == (
        "RAW_ARCHIVE_GATE_PASSED__LOCAL_RAW_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
    )
    assert _gate_result_state("fail") == "RAW_ARCHIVE_GATE_FAILED__REMAIN_PAUSED"
    assert _gate_result_state("error") == "RAW_ARCHIVE_GATE_PARTIAL__FAIL_CLOSED__REMAIN_PAUSED"


# --------------------------------------------------------------------------- #
# Governance constants
# --------------------------------------------------------------------------- #


def test_non_authorizations_all_false() -> None:
    assert all(v is False for v in gate.NON_AUTHORIZATIONS.values())
    assert gate.NON_AUTHORIZATIONS["research_eligible_flip_authorized"] is False
    assert gate.NON_AUTHORIZATIONS["sealed_test_split_read_authorized"] is False
    assert gate.NON_AUTHORIZATIONS["v002_terminal_window_read_authorized"] is False
    assert gate.NON_AUTHORIZATIONS["normalization_authorized"] is False


def test_governance_labels_forbid_downstream() -> None:
    for key in ("feature_computation", "labels", "ml", "strategy", "diagnostics", "backtest"):
        assert gate.GOVERNANCE_LABELS[key] == "forbidden"


# --------------------------------------------------------------------------- #
# Scope-token denylist (regression: must not flag in-scope aggTrades paths)
# --------------------------------------------------------------------------- #


def test_scope_denylist_does_not_flag_inscope_aggtrades_paths() -> None:
    in_scope = [
        "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/03/"
        "BTCUSDT-aggTrades-2024-03-01.zip",
        "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/03/"
        "BTCUSDT-aggTrades-2024-03-01.zip.sha256",
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/"
        "BTCUSDT-aggTrades-2024-03-01.zip",
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/"
        "BTCUSDT-aggTrades-2024-03-01.zip.CHECKSUM",
    ]
    for path in in_scope:
        low = path.lower()
        hits = [tok for tok in gate._SCOPE_DENYLIST if tok in low]
        assert hits == [], f"in-scope aggTrades path falsely flagged by {hits}: {path}"


def test_scope_denylist_flags_out_of_scope_paths() -> None:
    out_of_scope = [
        ("ethusdt", "microstructure/raw/x/ETHUSDT/2024/03/ETHUSDT-aggTrades-2024-03-01.zip"),
        ("-trades-", "https://data.binance.vision/data/futures/um/daily/trades/BTCUSDT/"
                     "BTCUSDT-trades-2024-03-01.zip"),
        ("/trades/", "https://data.binance.vision/data/futures/um/daily/trades/BTCUSDT/"
                     "BTCUSDT-trades-2024-03-01.zip"),
        ("/spot/", "https://data.binance.vision/data/spot/daily/aggTrades/BTCUSDT/"
                   "BTCUSDT-aggTrades-2024-03-01.zip"),
        ("markprice", "https://data.binance.vision/data/futures/um/daily/markPriceKlines/x.zip"),
        ("orderbook", "microstructure/raw/orderbook/BTCUSDT-orderbook-2024-03-01.zip"),
    ]
    for _tok, path in out_of_scope:
        low = path.lower()
        hits = [tok for tok in gate._SCOPE_DENYLIST if tok in low]
        assert hits, f"out-of-scope path not flagged: {path}"
