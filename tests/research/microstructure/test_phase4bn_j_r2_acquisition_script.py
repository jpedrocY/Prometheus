"""Offline tests for the Phase 4bn-J-R2 BTCUSDT aggTrades pre-v002 retry script.

All tests are offline. The script's network helpers (``_http_get_bytes``,
``_http_head_content_length``) are never invoked under network mode; the
orchestrator is exercised either via the ``do_network=False`` hook or via
direct unit tests of pure helpers (segment date guard, symbol/family
guards, URL allowlist, sidecar format, SHA256 helpers, path discipline,
cap evaluation). Every file write happens under pytest ``tmp_path`` only
— never under the real project ``data/microstructure/`` tree, and never
touching any v002 terminal or sealed-test artefact.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from datetime import date, timedelta
from pathlib import Path

import pytest

from scripts import phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002 as p4r2
from scripts.phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002 import (
    DATA_FAMILY,
    DATASET_FAMILY,
    DATASET_VERSION,
    DATE_END,
    DATE_START,
    EXPECTED_DATE_COUNT,
    MANIFEST_STEM,
    RAW_HARD_BYTES,
    RAW_WARN_BYTES,
    RUNTIME_HARD_SECONDS,
    RUNTIME_WARN_SECONDS,
    SYMBOL,
    SYMBOL_LIST,
    AcquisitionFailClosed,
    assert_archive_url_allowed,
    assert_date_in_segment,
    assert_family_aggtrades,
    assert_path_under_microstructure,
    assert_scope_token_allowed,
    assert_symbol_btcusdt,
    atomic_write_bytes,
    atomic_write_text,
    build_archive_url,
    build_checksum_url,
    compute_capture_config_hash,
    evaluate_caps,
    generate_segment_date_list,
    inventory_and_validate_zip,
    make_sidecar_body,
    parse_sha256_from_checksum,
    sha256_bytes,
    sha256_file,
)

# ---------------------------------------------------------------------------- #
# Exact 275-date generation
# ---------------------------------------------------------------------------- #


def test_date_list_cardinality_is_275() -> None:
    dates = generate_segment_date_list()
    assert len(dates) == EXPECTED_DATE_COUNT == 275


def test_date_list_first_and_last() -> None:
    dates = generate_segment_date_list()
    assert dates[0] == "2024-03-01"
    assert dates[-1] == "2024-11-30"
    assert DATE_START.isoformat() == dates[0]
    assert DATE_END.isoformat() == dates[-1]


def test_date_list_is_contiguous_and_chronological() -> None:
    dates = generate_segment_date_list()
    prev = None
    for d in dates:
        parsed = date.fromisoformat(d)
        if prev is not None:
            assert (parsed - prev) == timedelta(days=1), (
                f"non-contiguous: {prev} -> {parsed}"
            )
        prev = parsed


def test_date_list_no_duplicates() -> None:
    dates = generate_segment_date_list()
    assert len(set(dates)) == len(dates)


def test_date_list_per_month_counts() -> None:
    dates = generate_segment_date_list()
    counts: dict[str, int] = {}
    for d in dates:
        counts[d[:7]] = counts.get(d[:7], 0) + 1
    assert counts == {
        "2024-03": 31,
        "2024-04": 30,
        "2024-05": 31,
        "2024-06": 30,
        "2024-07": 31,
        "2024-08": 31,
        "2024-09": 30,
        "2024-10": 31,
        "2024-11": 30,
    }


def test_date_list_excludes_all_v002_and_post_v002_dates() -> None:
    dates = set(generate_segment_date_list())
    # v002 terminal window and sealed test split must be absent.
    for forbidden in (
        "2024-12-01",
        "2024-12-31",
        "2025-01-15",  # the Phase 4az fixture date (v002 window)
        "2025-02-13",
        "2025-02-14",  # sealed test split start
        "2025-02-28",  # sealed test split / v002 end
    ):
        assert forbidden not in dates


# ---------------------------------------------------------------------------- #
# Segment date guard
# ---------------------------------------------------------------------------- #


def test_assert_date_in_segment_accepts_boundaries() -> None:
    assert assert_date_in_segment("2024-03-01") == date(2024, 3, 1)
    assert assert_date_in_segment("2024-11-30") == date(2024, 11, 30)
    assert assert_date_in_segment("2024-07-15") == date(2024, 7, 15)


@pytest.mark.parametrize(
    "bad_date",
    [
        "2024-12-01",  # v002 terminal window start
        "2024-12-15",
        "2025-01-15",  # Phase 4az fixture (v002 window)
        "2025-02-14",  # sealed test split start
        "2025-02-28",  # v002 / sealed test end
        "2025-03-01",  # post-v002
    ],
)
def test_assert_date_in_segment_rejects_v002_and_post_v002(bad_date: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_date_in_segment(bad_date)


@pytest.mark.parametrize(
    "bad_date",
    [
        "2024-02-29",  # before segment start (leap day)
        "2024-02-28",
        "2023-12-31",
        "2024-01-01",
    ],
)
def test_assert_date_in_segment_rejects_pre_segment(bad_date: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_date_in_segment(bad_date)


@pytest.mark.parametrize("bad", ["", "not-a-date", "2024-13-01", "2024/03/01", None])
def test_assert_date_in_segment_rejects_malformed(bad: object) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_date_in_segment(bad)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------- #
# Symbol / family / scope guards
# ---------------------------------------------------------------------------- #


def test_assert_symbol_btcusdt_accepts_btcusdt() -> None:
    assert_symbol_btcusdt("BTCUSDT")


@pytest.mark.parametrize(
    "bad", ["ETHUSDT", "btcusdt", "BTCUSD", "XBTUSD", "", "BTCUSDT ", None]
)
def test_assert_symbol_btcusdt_rejects_others(bad: object) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_symbol_btcusdt(bad)  # type: ignore[arg-type]


def test_assert_family_aggtrades_accepts_aggtrades() -> None:
    assert_family_aggtrades("aggTrades")


@pytest.mark.parametrize(
    "bad", ["trades", "klines", "markPriceKlines", "metrics", "", None]
)
def test_assert_family_aggtrades_rejects_others(bad: object) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_family_aggtrades(bad)  # type: ignore[arg-type]


def test_assert_scope_token_allowed_accepts_clean_value() -> None:
    assert_scope_token_allowed("BTCUSDT")
    assert_scope_token_allowed("aggTrades")
    assert_scope_token_allowed("2024-03-01")


@pytest.mark.parametrize(
    "bad",
    [
        "ETHUSDT",
        "BTCUSDT-markPrice",
        "spot-BTCUSDT",
        "futures/cm/BTCUSDT",
        "orderbook",
        "bookDepth",
        "BTCUSDT-trades",
        "klines",
        "metrics",
        "fundingRate",
        "openInterest",
        "v003",
        "cross-venue",
    ],
)
def test_assert_scope_token_allowed_rejects_forbidden(bad: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_scope_token_allowed(bad)


# ---------------------------------------------------------------------------- #
# URL allowlist + segment-aware builders
# ---------------------------------------------------------------------------- #


def test_build_archive_url_allows_segment_dates() -> None:
    url = build_archive_url("2024-03-01")
    assert url == (
        "https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "BTCUSDT/BTCUSDT-aggTrades-2024-03-01.zip"
    )
    chk = build_checksum_url("2024-03-01")
    assert chk == url + ".CHECKSUM"


@pytest.mark.parametrize("bad_date", ["2024-12-01", "2025-02-28", "2024-02-29"])
def test_build_archive_url_rejects_out_of_segment(bad_date: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        build_archive_url(bad_date)
    with pytest.raises(AcquisitionFailClosed):
        build_checksum_url(bad_date)


def test_assert_archive_url_allowed_accepts_locked_urls() -> None:
    url = (
        "https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "BTCUSDT/BTCUSDT-aggTrades-2024-03-01.zip"
    )
    assert_archive_url_allowed(url)
    assert_archive_url_allowed(url + ".CHECKSUM")


@pytest.mark.parametrize(
    "url",
    [
        "https://fapi.binance.com/fapi/v1/aggTrades",
        "https://api.binance.com/api/v3/aggTrades",
        "https://stream.binance.com/ws/btcusdt@aggTrade",
        "https://data.binance.vision/data/futures/um/monthly/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2024-03.zip",
        "https://data.binance.vision/data/futures/um/daily/klines/BTCUSDT/15m/x.zip",
        "https://data.binance.vision/data/futures/um/daily/markPriceKlines/BTCUSDT/15m/x.zip",
        "https://data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/x.zip",
        "https://data.binance.vision/data/futures/cm/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2024-03-01.zip",
        "https://data.binance.vision/data/spot/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2024-03-01.zip",
        "https://data.binance.vision/data/option/daily/aggTrades/x.zip",
        "http://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2024-03-01.zip",
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/../../api/v3/x.zip",
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2024-03-01.zip?api_key=abc",
    ],
)
def test_assert_archive_url_allowed_rejects_forbidden(url: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_archive_url_allowed(url)


def test_assert_archive_url_allowed_rejects_ethusdt_path() -> None:
    url = (
        "https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "ETHUSDT/ETHUSDT-aggTrades-2024-03-01.zip"
    )
    with pytest.raises(AcquisitionFailClosed):
        assert_archive_url_allowed(url)


# ---------------------------------------------------------------------------- #
# Path discipline
# ---------------------------------------------------------------------------- #


def test_assert_path_under_microstructure_accepts_proper_path(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    child = output_root / "raw" / DATASET_FAMILY / SYMBOL / "2024" / "03" / "x.zip"
    assert_path_under_microstructure(child, output_root)


def test_assert_path_under_microstructure_rejects_outside_root(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    outside = tmp_path / "elsewhere" / "file.zip"
    with pytest.raises(AcquisitionFailClosed):
        assert_path_under_microstructure(outside, output_root)


def test_assert_path_under_microstructure_rejects_non_microstructure_root(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "data_raw"
    output_root.mkdir(parents=True)
    child = output_root / "x.zip"
    with pytest.raises(AcquisitionFailClosed):
        assert_path_under_microstructure(child, output_root)


# ---------------------------------------------------------------------------- #
# Sidecar format
# ---------------------------------------------------------------------------- #


def test_make_sidecar_body_canonical_format() -> None:
    sha = "0" * 64
    body = make_sidecar_body(sha, "BTCUSDT-aggTrades-2024-03-01.zip")
    assert body == f"{sha}  BTCUSDT-aggTrades-2024-03-01.zip\n"
    assert body[64:66] == "  "
    assert body.endswith("\n")
    assert not body.endswith("\r\n")


def test_make_sidecar_body_lowercases_uppercase_hex() -> None:
    body = make_sidecar_body("F" * 64, "x.zip")
    assert body == f"{'f' * 64}  x.zip\n"


@pytest.mark.parametrize("bad_sha", ["", "abc", "0" * 63, "0" * 65, "X" * 64])
def test_make_sidecar_body_rejects_bad_sha(bad_sha: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        make_sidecar_body(bad_sha, "x.zip")


@pytest.mark.parametrize("bad_name", ["", "a/b.zip", "a\\b.zip"])
def test_make_sidecar_body_rejects_bad_basename(bad_name: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        make_sidecar_body("0" * 64, bad_name)


# ---------------------------------------------------------------------------- #
# Checksum parsing
# ---------------------------------------------------------------------------- #


def test_parse_sha256_from_checksum_canonical() -> None:
    body = "abcdef" * 10 + "abcd  BTCUSDT-aggTrades-2024-03-01.zip\n"
    assert parse_sha256_from_checksum(body) == ("abcdef" * 10 + "abcd").lower()


def test_parse_sha256_from_checksum_accepts_bytes() -> None:
    body = ("0" * 64 + "  x.zip\n").encode("utf-8")
    assert parse_sha256_from_checksum(body) == "0" * 64


@pytest.mark.parametrize(
    "bad", ["", "   ", "abc", "x" * 64, "0" * 63, "0" * 65]
)
def test_parse_sha256_from_checksum_rejects_bad(bad: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        parse_sha256_from_checksum(bad)


def test_parse_sha256_from_checksum_handles_invalid_utf8_bytes() -> None:
    with pytest.raises(AcquisitionFailClosed):
        parse_sha256_from_checksum(b"\xff\xfe\xfd")


# ---------------------------------------------------------------------------- #
# SHA256 helpers + atomic write
# ---------------------------------------------------------------------------- #


def test_sha256_bytes_matches_hashlib() -> None:
    payload = b"the quick brown fox"
    assert sha256_bytes(payload) == hashlib.sha256(payload).hexdigest()


def test_sha256_file_matches_bytes(tmp_path: Path) -> None:
    payload = b"a" * (3 * 1024 * 1024 + 7)
    p = tmp_path / "x.bin"
    p.write_bytes(payload)
    assert sha256_file(p) == hashlib.sha256(payload).hexdigest()


def test_atomic_write_bytes_refuses_overwrite_different(tmp_path: Path) -> None:
    target = tmp_path / "x.bin"
    target.write_bytes(b"hello")
    with pytest.raises(AcquisitionFailClosed):
        atomic_write_bytes(target, b"different")


def test_atomic_write_bytes_noop_on_identical(tmp_path: Path) -> None:
    target = tmp_path / "x.bin"
    target.write_bytes(b"hello")
    atomic_write_bytes(target, b"hello")
    assert target.read_bytes() == b"hello"


def test_atomic_write_text_writes_utf8(tmp_path: Path) -> None:
    target = tmp_path / "x.txt"
    atomic_write_text(target, "hello\n")
    assert target.read_text(encoding="utf-8") == "hello\n"


# ---------------------------------------------------------------------------- #
# Capture-config hash
# ---------------------------------------------------------------------------- #


def test_compute_capture_config_hash_is_deterministic() -> None:
    dates = generate_segment_date_list()
    h1 = compute_capture_config_hash(dates, "abc123")
    h2 = compute_capture_config_hash(dates, "abc123")
    assert h1 == h2
    assert len(h1) == 64


def test_compute_capture_config_hash_changes_with_commit_sha() -> None:
    dates = generate_segment_date_list()
    assert compute_capture_config_hash(dates, "abc") != (
        compute_capture_config_hash(dates, "def")
    )


# ---------------------------------------------------------------------------- #
# Cap evaluation (pure; no network)
# ---------------------------------------------------------------------------- #


def test_evaluate_caps_no_breach_under_thresholds() -> None:
    caps = evaluate_caps(cumulative_bytes=1 * 1024 ** 3, elapsed_seconds=60.0)
    assert not caps.warn_disk
    assert not caps.hard_disk
    assert not caps.warn_runtime
    assert not caps.hard_runtime
    assert not caps.hard_breached


def test_evaluate_caps_disk_warning_threshold() -> None:
    caps = evaluate_caps(cumulative_bytes=RAW_WARN_BYTES, elapsed_seconds=0.0)
    assert caps.warn_disk
    assert not caps.hard_disk
    assert not caps.hard_breached


def test_evaluate_caps_disk_hard_cap() -> None:
    caps = evaluate_caps(cumulative_bytes=RAW_HARD_BYTES + 1, elapsed_seconds=0.0)
    assert caps.warn_disk
    assert caps.hard_disk
    assert caps.hard_breached


def test_evaluate_caps_runtime_warning_threshold() -> None:
    caps = evaluate_caps(cumulative_bytes=0, elapsed_seconds=RUNTIME_WARN_SECONDS)
    assert caps.warn_runtime
    assert not caps.hard_runtime
    assert not caps.hard_breached


def test_evaluate_caps_runtime_hard_cap() -> None:
    caps = evaluate_caps(cumulative_bytes=0, elapsed_seconds=RUNTIME_HARD_SECONDS)
    assert caps.hard_runtime
    assert caps.hard_breached


# ---------------------------------------------------------------------------- #
# Inventory + row-sample validation on a tmp_path-built ZIP
# ---------------------------------------------------------------------------- #


def _make_csv_bytes(rows: list[tuple], *, include_header: bool = True) -> bytes:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    if include_header:
        writer.writerow(
            [
                "agg_trade_id",
                "price",
                "quantity",
                "first_trade_id",
                "last_trade_id",
                "transact_time",
                "is_buyer_maker",
            ]
        )
    for row in rows:
        writer.writerow(list(row))
    return buf.getvalue().encode("utf-8")


def _zip_bytes(payload: bytes, member_name: str) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(member_name, payload)
    return out.getvalue()


def test_inventory_and_validate_zip_happy_path(tmp_path: Path) -> None:
    rows = [
        (i, "100000.50", "0.001", 1000 + i, 1000 + i, 1709251200000 + i * 1000, "false")
        for i in range(1, 251)
    ]
    csv_bytes = _make_csv_bytes(rows)
    zip_bytes = _zip_bytes(csv_bytes, "BTCUSDT-aggTrades-2024-03-01.csv")
    p = tmp_path / "BTCUSDT-aggTrades-2024-03-01.zip"
    p.write_bytes(zip_bytes)
    inv = inventory_and_validate_zip(p, date_str="2024-03-01")
    assert inv.decompression_failure_reason is None
    assert inv.row_count == 250
    assert inv.min_agg_trade_id == 1
    assert inv.max_agg_trade_id == 250
    assert inv.row_sample_validation_passed


def test_inventory_and_validate_zip_detects_bad_zip(tmp_path: Path) -> None:
    p = tmp_path / "bad.zip"
    p.write_bytes(b"not a zip")
    inv = inventory_and_validate_zip(p, date_str="2024-03-02")
    assert inv.decompression_failure_reason is not None


def test_inventory_and_validate_zip_detects_invalid_row(tmp_path: Path) -> None:
    rows = [
        (1, "100.0", "0.001", 100, 100, 1709251200000, "false"),
        (2, "-100.0", "0.001", 101, 101, 1709251201000, "true"),
    ]
    csv_bytes = _make_csv_bytes(rows)
    zip_bytes = _zip_bytes(csv_bytes, "BTCUSDT-aggTrades-2024-03-03.csv")
    p = tmp_path / "BTCUSDT-aggTrades-2024-03-03.zip"
    p.write_bytes(zip_bytes)
    inv = inventory_and_validate_zip(p, date_str="2024-03-03")
    assert inv.decompression_failure_reason is None
    assert not inv.row_sample_validation_passed
    assert inv.row_sample_failure_reason is not None


# ---------------------------------------------------------------------------- #
# Static guarantees
# ---------------------------------------------------------------------------- #


def test_module_does_not_import_forbidden_libraries() -> None:
    text = Path(p4r2.__file__).read_text(encoding="utf-8")
    for token in (
        "import requests",
        "import httpx",
        "import aiohttp",
        "import websockets",
        "from requests",
        "from httpx",
        "from aiohttp",
        "from websockets",
    ):
        assert token not in text, f"forbidden import token present: {token}"
    assert "from prometheus.research.microstructure.aggtrades" in text


def test_constants_are_locked() -> None:
    assert DATASET_FAMILY == "microstructure_raw_aggtrades_v001"
    assert DATASET_VERSION == "v002"
    assert SYMBOL == "BTCUSDT"
    assert SYMBOL_LIST == ("BTCUSDT",)
    assert DATA_FAMILY == "aggTrades"
    assert EXPECTED_DATE_COUNT == 275
    assert date(2024, 3, 1) == DATE_START
    assert date(2024, 11, 30) == DATE_END
    assert RAW_WARN_BYTES == 10 * 1024 ** 3
    assert RAW_HARD_BYTES == 25 * 1024 ** 3
    assert RUNTIME_WARN_SECONDS == 2 * 60 * 60
    assert RUNTIME_HARD_SECONDS == 4 * 60 * 60
    assert p4r2.SCHEMA_VERSION == "v001"
    assert p4r2.PHASE_ID == "4bn-J-R2"
    assert p4r2.SOURCE_PHASE_BOUNDARY == "4bn-J-R1"
    assert p4r2.BASE_COMMIT_SHA == (
        "03dc876cab9ecd3db982beb0ba51712858cbdf9c"
    )


def test_manifest_stem_is_distinct_from_published_v002() -> None:
    # The segment manifest must NOT collide with the published v002 manifest.
    assert f"{DATASET_FAMILY}__{DATASET_VERSION}" != MANIFEST_STEM
    assert MANIFEST_STEM == (
        "microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2"
    )


def test_url_templates_match_locked_pattern() -> None:
    url = p4r2.ARCHIVE_URL_TEMPLATE.format(date="2024-03-01")
    assert url.startswith("https://data.binance.vision/")
    assert "BTCUSDT-aggTrades-2024-03-01.zip" in url
    assert_archive_url_allowed(url)
    chk = p4r2.CHECKSUM_URL_TEMPLATE.format(date="2024-03-01")
    assert chk == url + ".CHECKSUM"
    assert_archive_url_allowed(chk)


# ---------------------------------------------------------------------------- #
# acquire_one_date with do_network=False
# ---------------------------------------------------------------------------- #


def test_acquire_one_date_no_network_no_fixture_returns_retry_exhausted(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    events: list[dict] = []
    res = p4r2.acquire_one_date(
        "2024-03-15",
        output_root=output_root,
        events=events,
        do_network=False,
    )
    assert res.status in {"retry_exhausted", "missing_404"}
    raw_dir = output_root / "raw" / DATASET_FAMILY / SYMBOL / "2024" / "03"
    assert not raw_dir.exists() or not list(raw_dir.iterdir())


def test_acquire_one_date_rejects_out_of_segment_date(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    events: list[dict] = []
    with pytest.raises(AcquisitionFailClosed):
        p4r2.acquire_one_date(
            "2024-12-01",
            output_root=output_root,
            events=events,
            do_network=False,
        )


def test_acquire_one_date_refuses_overwrite_different_sha(tmp_path: Path) -> None:
    """A pre-existing non-identical local zip must not be overwritten."""
    output_root = tmp_path / "data" / "microstructure"
    raw_dir = output_root / "raw" / DATASET_FAMILY / SYMBOL / "2024" / "03"
    raw_dir.mkdir(parents=True)
    rows = [
        (i, "100000.0", "0.001", 1000 + i, 1000 + i, 1709251200000 + i * 1000, "false")
        for i in range(1, 11)
    ]
    zip_bytes = _zip_bytes(
        _make_csv_bytes(rows), "BTCUSDT-aggTrades-2024-03-10.csv"
    )
    final_zip = raw_dir / "BTCUSDT-aggTrades-2024-03-10.zip"
    final_zip.write_bytes(zip_bytes)
    pre_sha = sha256_file(final_zip)
    # do_network=False: companion cannot be fetched, so the path returns
    # before any overwrite. The file must remain byte-identical.
    events: list[dict] = []
    res = p4r2.acquire_one_date(
        "2024-03-10",
        output_root=output_root,
        events=events,
        do_network=False,
    )
    assert res.status in {"retry_exhausted", "checksum_companion_unavailable"}
    assert final_zip.exists()
    assert sha256_file(final_zip) == pre_sha


# ---------------------------------------------------------------------------- #
# CLI dry-run + output-root guard
# ---------------------------------------------------------------------------- #


def test_cli_dry_run_emits_plan(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    rc = p4r2.main(["--dry-run", "--output-root", str(output_root)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Phase 4bn-J-R2 dry-run plan" in out
    assert "date_count     : 275" in out
    assert "2024-03-01" in out
    assert "2024-11-30" in out
    assert "No download will be performed." in out


def test_cli_rejects_output_root_outside_microstructure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out_dir = tmp_path / "elsewhere"
    out_dir.mkdir()
    rc = p4r2.main(["--output-root", str(out_dir)])
    assert rc == 2
    assert "refusing to use --output-root outside data/microstructure/" in (
        capsys.readouterr().err
    )


# ---------------------------------------------------------------------------- #
# JSON determinism + non-eligible seed (manifest/log writers)
# ---------------------------------------------------------------------------- #


def _one_entry() -> p4r2.DateResult:
    return p4r2.DateResult(
        date="2024-03-01",
        expected_url=p4r2.ARCHIVE_URL_TEMPLATE.format(date="2024-03-01"),
        expected_checksum_url=p4r2.CHECKSUM_URL_TEMPLATE.format(date="2024-03-01"),
        local_zip_path=(
            f"microstructure/raw/{DATASET_FAMILY}/{SYMBOL}/2024/03/"
            f"{SYMBOL}-aggTrades-2024-03-01.zip"
        ),
        local_sidecar_path=(
            f"microstructure/raw/{DATASET_FAMILY}/{SYMBOL}/2024/03/"
            f"{SYMBOL}-aggTrades-2024-03-01.zip.sha256"
        ),
        status="missing_404",
        sha256=None,
        sha256_from_companion=None,
        size_bytes=None,
        row_count=None,
        first_trade_time_ms=None,
        last_trade_time_ms=None,
        min_agg_trade_id=None,
        max_agg_trade_id=None,
        retry_count=0,
        failure_reason="archive HTTP 404",
        acquired_at_unix_ms=None,
    )


def test_acquisition_log_and_manifest_sort_keys_and_non_eligible(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    entry = _one_entry()

    log_path = output_root / "manifests" / f"{MANIFEST_STEM}_acquisition_log.json"
    p4r2.write_acquisition_log(
        log_path,
        acquisition_run_id="test-run-id",
        code_commit_sha="abc",
        started_at_unix_ms=1000,
        finished_at_unix_ms=2000,
        date_list=["2024-03-01"],
        events=[{"timestamp_unix_ms": 1500, "event_type": "test",
                 "date": "2024-03-01", "details": {}}],
        entries=[entry],
        overall_status="FAIL_CLOSED_NO_ACQUISITION",
        strict_fail_closed=True,
        warnings=[],
        hard_caps_crossed=False,
        fail_closed_stop_conditions=[],
    )
    raw = log_path.read_text(encoding="utf-8")
    assert raw.endswith("\n")
    parsed = json.loads(raw)
    assert list(parsed.keys()) == sorted(parsed.keys())
    assert parsed["summary"]["test_holdout_touched"] is False
    assert parsed["summary"]["test_rows_loaded"] == 0
    assert parsed["summary"]["research_eligible_after_acquisition"] is False

    manifest_path = output_root / "manifests" / f"{MANIFEST_STEM}.json"
    p4r2.write_segment_manifest(
        manifest_path,
        code_commit_sha="abc",
        date_list=["2024-03-01"],
        entries=[entry],
        acquisition_log_path=log_path,
        acquisition_log_sha256=sha256_file(log_path),
        output_root=output_root,
        warnings=[],
        hard_caps_crossed=False,
        fail_closed_stop_conditions=[],
        runtime_seconds=1,
    )
    raw_m = manifest_path.read_text(encoding="utf-8")
    assert raw_m.endswith("\n")
    parsed_m = json.loads(raw_m)
    assert list(parsed_m.keys()) == sorted(parsed_m.keys())
    assert parsed_m["dataset_family"] == DATASET_FAMILY
    assert parsed_m["dataset_version"] == DATASET_VERSION
    assert parsed_m["segment_label"] == "pre_v002_segment"
    assert parsed_m["research_eligible"] is False
    assert parsed_m["eligibility_gate_status"] == "pending"
    assert parsed_m["test_holdout_touched"] is False
    assert parsed_m["test_rows_loaded"] == 0
    assert parsed_m["acquired_segment_start"] == "2024-03-01"
    assert parsed_m["acquired_segment_end"] == "2024-11-30"
    assert parsed_m["base_commit_sha"] == (
        "03dc876cab9ecd3db982beb0ba51712858cbdf9c"
    )
    assert parsed_m["existing_v002_terminal_window"]["read"] is False
    assert parsed_m["existing_v002_sealed_test_split"]["touched"] is False
    gov = parsed_m["governance_labels"]
    for k in ("feature_computation", "labels", "ml", "strategy", "strategy_use"):
        assert gov[k] == "forbidden"
    assert gov["phase"] == "4bn-J-R2"
    assert gov["validator"] == "phase_4ax_aggtrades_v001"
