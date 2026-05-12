"""Offline tests for the Phase 4bl-C BTCUSDT aggTrades multi-day acquisition script.

All tests are offline. The script's network helper ``_http_get_bytes``
is never invoked under network mode; the orchestrator is exercised
either via the ``do_network=False`` hook or via direct unit tests of
pure helpers (URL allowlist, date-list generation, sidecar format,
SHA256 helpers, path discipline). Every file write happens under
pytest ``tmp_path`` only — never under the real project
``data/microstructure/`` tree.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

import pytest

from scripts import phase4bl_c_acquire_btcusdt_aggtrades_multiday as p4bl_c
from scripts.phase4bl_c_acquire_btcusdt_aggtrades_multiday import (
    DATASET_FAMILY,
    DATASET_VERSION,
    DATE_END,
    DATE_START,
    EXISTING_FIXTURE_DATE,
    EXISTING_FIXTURE_SHA256,
    EXPECTED_DATE_COUNT,
    SYMBOL,
    SYMBOL_LIST,
    AcquisitionFailClosed,
    assert_archive_url_allowed,
    assert_path_under_microstructure,
    atomic_write_bytes,
    atomic_write_text,
    compute_capture_config_hash,
    generate_locked_date_list,
    inventory_and_validate_zip,
    make_sidecar_body,
    parse_sha256_from_checksum,
    sha256_bytes,
    sha256_file,
)

# ---------------------------------------------------------------------------- #
# Date list generation
# ---------------------------------------------------------------------------- #


def test_date_list_cardinality_is_90() -> None:
    dates = generate_locked_date_list()
    assert len(dates) == EXPECTED_DATE_COUNT == 90


def test_date_list_first_and_last() -> None:
    dates = generate_locked_date_list()
    assert dates[0] == "2024-12-01"
    assert dates[-1] == "2025-02-28"
    assert DATE_START.isoformat() == dates[0]
    assert DATE_END.isoformat() == dates[-1]


def test_date_list_is_contiguous_and_chronological() -> None:
    dates = generate_locked_date_list()
    from datetime import date, timedelta

    prev = None
    for d in dates:
        parsed = date.fromisoformat(d)
        if prev is not None:
            assert (parsed - prev) == timedelta(days=1), (
                f"non-contiguous: {prev} -> {parsed}"
            )
        prev = parsed


def test_date_list_no_duplicates() -> None:
    dates = generate_locked_date_list()
    assert len(set(dates)) == len(dates)


def test_date_list_per_month_counts() -> None:
    dates = generate_locked_date_list()
    counts = {"2024-12": 0, "2025-01": 0, "2025-02": 0}
    for d in dates:
        counts[d[:7]] += 1
    assert counts == {"2024-12": 31, "2025-01": 31, "2025-02": 28}


def test_date_list_includes_existing_fixture_at_index_45() -> None:
    dates = generate_locked_date_list()
    assert EXISTING_FIXTURE_DATE in dates
    # Element 46 = index 45.
    assert dates.index(EXISTING_FIXTURE_DATE) == 45


# ---------------------------------------------------------------------------- #
# URL allowlist
# ---------------------------------------------------------------------------- #


def test_assert_archive_url_allowed_accepts_locked_urls() -> None:
    url = (
        "https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "BTCUSDT/BTCUSDT-aggTrades-2024-12-01.zip"
    )
    assert_archive_url_allowed(url)
    assert_archive_url_allowed(url + ".CHECKSUM")


def test_assert_archive_url_allowed_accepts_existing_fixture_url() -> None:
    url = (
        "https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip"
    )
    assert_archive_url_allowed(url)


@pytest.mark.parametrize(
    "url",
    [
        # Non-binance host
        "https://fapi.binance.com/fapi/v1/aggTrades",
        # api.binance.com forbidden token + non-archive host
        "https://api.binance.com/api/v3/aggTrades",
        # stream.binance.com forbidden
        "https://stream.binance.com/ws/btcusdt@aggTrade",
        # monthly archives are forbidden
        "https://data.binance.vision/data/futures/um/monthly/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01.zip",
        # non-aggTrades daily families forbidden
        "https://data.binance.vision/data/futures/um/daily/klines/BTCUSDT/15m/BTCUSDT-klines-2025-01-15.zip",
        "https://data.binance.vision/data/futures/um/daily/markPriceKlines/BTCUSDT/15m/x.zip",
        "https://data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/x.zip",
        # COIN-M futures
        "https://data.binance.vision/data/futures/cm/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip",
        # Spot
        "https://data.binance.vision/data/spot/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip",
        # Options
        "https://data.binance.vision/data/option/daily/aggTrades/x.zip",
        # http (not https)
        "http://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip",
        # path traversal
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/../../api/v3/x.zip",
        # forbidden credential-shaped token
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip?api_key=abc",
    ],
)
def test_assert_archive_url_allowed_rejects_forbidden(url: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_archive_url_allowed(url)


@pytest.mark.parametrize("bad", ["", None, 42, "ftp://data.binance.vision/x"])
def test_assert_archive_url_allowed_rejects_invalid_inputs(bad: object) -> None:
    with pytest.raises(AcquisitionFailClosed):
        assert_archive_url_allowed(bad)  # type: ignore[arg-type]


def test_assert_archive_url_allowed_rejects_wrong_symbol_path() -> None:
    # The locked path pattern requires .../aggTrades/BTCUSDT/...
    url = (
        "https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "ETHUSDT/ETHUSDT-aggTrades-2024-12-01.zip"
    )
    with pytest.raises(AcquisitionFailClosed):
        assert_archive_url_allowed(url)


def test_assert_archive_url_allowed_rejects_wrong_filename_pattern() -> None:
    url = (
        "https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "BTCUSDT/BTCUSDT-otherFile-2024-12-01.zip"
    )
    with pytest.raises(AcquisitionFailClosed):
        assert_archive_url_allowed(url)


# ---------------------------------------------------------------------------- #
# Path discipline
# ---------------------------------------------------------------------------- #


def test_assert_path_under_microstructure_accepts_proper_path(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    child = output_root / "raw" / DATASET_FAMILY / SYMBOL / "2024" / "12" / "x.zip"
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
    body = make_sidecar_body(sha, "BTCUSDT-aggTrades-2024-12-01.zip")
    assert body == f"{sha}  BTCUSDT-aggTrades-2024-12-01.zip\n"
    # Exactly two spaces between hash and basename.
    assert body[64:66] == "  "
    # Single trailing LF.
    assert body.endswith("\n")
    assert not body.endswith("\r\n")


def test_make_sidecar_body_lowercases_uppercase_hex() -> None:
    sha_upper = "F" * 64
    body = make_sidecar_body(sha_upper, "x.zip")
    assert body == f"{'f' * 64}  x.zip\n"


@pytest.mark.parametrize(
    "bad_sha", ["", "abc", "0" * 63, "0" * 65, "X" * 64]
)
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
    body = "abcdef" * 10 + "abcd  BTCUSDT-aggTrades-2025-01-15.zip\n"
    assert parse_sha256_from_checksum(body) == ("abcdef" * 10 + "abcd").lower()


def test_parse_sha256_from_checksum_accepts_bytes() -> None:
    body = ("0" * 64 + "  x.zip\n").encode("utf-8")
    assert parse_sha256_from_checksum(body) == "0" * 64


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "   ",
        "abc",
        "x" * 64,  # not hex
        ("0" * 63),  # wrong length
        ("0" * 65),  # wrong length
    ],
)
def test_parse_sha256_from_checksum_rejects_bad(bad: str) -> None:
    with pytest.raises(AcquisitionFailClosed):
        parse_sha256_from_checksum(bad)


def test_parse_sha256_from_checksum_handles_invalid_utf8_bytes() -> None:
    with pytest.raises(AcquisitionFailClosed):
        parse_sha256_from_checksum(b"\xff\xfe\xfd")


# ---------------------------------------------------------------------------- #
# SHA256 helpers
# ---------------------------------------------------------------------------- #


def test_sha256_bytes_matches_hashlib() -> None:
    payload = b"the quick brown fox"
    expected = hashlib.sha256(payload).hexdigest()
    assert sha256_bytes(payload) == expected


def test_sha256_file_matches_bytes(tmp_path: Path) -> None:
    payload = b"a" * (3 * 1024 * 1024 + 7)  # ensure multiple chunks
    p = tmp_path / "x.bin"
    p.write_bytes(payload)
    assert sha256_file(p) == hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------------------- #
# Atomic write
# ---------------------------------------------------------------------------- #


def test_atomic_write_bytes_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "subdir" / "x.bin"
    atomic_write_bytes(target, b"hello")
    assert target.read_bytes() == b"hello"


def test_atomic_write_bytes_noop_on_identical(tmp_path: Path) -> None:
    target = tmp_path / "x.bin"
    target.write_bytes(b"hello")
    atomic_write_bytes(target, b"hello")  # should not raise
    assert target.read_bytes() == b"hello"


def test_atomic_write_bytes_refuses_overwrite_different(tmp_path: Path) -> None:
    target = tmp_path / "x.bin"
    target.write_bytes(b"hello")
    with pytest.raises(AcquisitionFailClosed):
        atomic_write_bytes(target, b"different")


def test_atomic_write_text_writes_utf8(tmp_path: Path) -> None:
    target = tmp_path / "x.txt"
    atomic_write_text(target, "hello\n")
    assert target.read_text(encoding="utf-8") == "hello\n"


# ---------------------------------------------------------------------------- #
# Capture-config hash
# ---------------------------------------------------------------------------- #


def test_compute_capture_config_hash_is_deterministic() -> None:
    dates = generate_locked_date_list()
    h1 = compute_capture_config_hash(dates, "abc123")
    h2 = compute_capture_config_hash(dates, "abc123")
    assert h1 == h2
    assert len(h1) == 64


def test_compute_capture_config_hash_changes_with_commit_sha() -> None:
    dates = generate_locked_date_list()
    h1 = compute_capture_config_hash(dates, "abc")
    h2 = compute_capture_config_hash(dates, "def")
    assert h1 != h2


# ---------------------------------------------------------------------------- #
# Inventory + row-sample validation on a tmp_path-built ZIP
# ---------------------------------------------------------------------------- #


def _make_csv_bytes(
    rows: list[tuple],
    *,
    include_header: bool = True,
) -> bytes:
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
        (i, "100000.50", "0.001", 1000 + i, 1000 + i, 1733011200000 + i * 1000, "false")
        for i in range(1, 251)
    ]
    csv_bytes = _make_csv_bytes(rows)
    zip_bytes = _zip_bytes(csv_bytes, "BTCUSDT-aggTrades-2024-12-01.csv")
    p = tmp_path / "BTCUSDT-aggTrades-2024-12-01.zip"
    p.write_bytes(zip_bytes)
    inv = inventory_and_validate_zip(p, date_str="2024-12-01")
    assert inv.decompression_failure_reason is None
    assert inv.row_count == 250
    assert inv.min_agg_trade_id == 1
    assert inv.max_agg_trade_id == 250
    assert inv.first_trade_time_ms == 1733011200000 + 1000
    assert inv.last_trade_time_ms == 1733011200000 + 250 * 1000
    assert inv.row_sample_validation_passed


def test_inventory_and_validate_zip_handles_short_archive(tmp_path: Path) -> None:
    rows = [
        (i, "100000.50", "0.001", 1000 + i, 1000 + i, 1733011200000 + i * 1000, "true")
        for i in range(1, 6)
    ]
    csv_bytes = _make_csv_bytes(rows)
    zip_bytes = _zip_bytes(csv_bytes, "BTCUSDT-aggTrades-2024-12-02.csv")
    p = tmp_path / "BTCUSDT-aggTrades-2024-12-02.zip"
    p.write_bytes(zip_bytes)
    inv = inventory_and_validate_zip(p, date_str="2024-12-02")
    assert inv.decompression_failure_reason is None
    assert inv.row_count == 5
    assert inv.row_sample_validation_passed


def test_inventory_and_validate_zip_detects_zero_rows(tmp_path: Path) -> None:
    csv_bytes = _make_csv_bytes([])
    zip_bytes = _zip_bytes(csv_bytes, "BTCUSDT-aggTrades-2024-12-03.csv")
    p = tmp_path / "BTCUSDT-aggTrades-2024-12-03.zip"
    p.write_bytes(zip_bytes)
    inv = inventory_and_validate_zip(p, date_str="2024-12-03")
    assert inv.decompression_failure_reason is not None


def test_inventory_and_validate_zip_detects_multi_member(tmp_path: Path) -> None:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("a.csv", "x\n")
        zf.writestr("b.csv", "y\n")
    p = tmp_path / "multi.zip"
    p.write_bytes(out.getvalue())
    inv = inventory_and_validate_zip(p, date_str="2024-12-04")
    assert inv.decompression_failure_reason is not None
    assert "exactly one CSV member" in (inv.decompression_failure_reason or "")


def test_inventory_and_validate_zip_detects_bad_zip(tmp_path: Path) -> None:
    p = tmp_path / "bad.zip"
    p.write_bytes(b"not a zip")
    inv = inventory_and_validate_zip(p, date_str="2024-12-05")
    assert inv.decompression_failure_reason is not None


def test_inventory_and_validate_zip_detects_invalid_row(tmp_path: Path) -> None:
    rows = [
        (1, "100.0", "0.001", 100, 100, 1733011200000, "false"),
        # row 2: negative price triggers validate_aggtrade_payload failure.
        (2, "-100.0", "0.001", 101, 101, 1733011201000, "true"),
    ]
    csv_bytes = _make_csv_bytes(rows)
    zip_bytes = _zip_bytes(csv_bytes, "BTCUSDT-aggTrades-2024-12-06.csv")
    p = tmp_path / "BTCUSDT-aggTrades-2024-12-06.zip"
    p.write_bytes(zip_bytes)
    inv = inventory_and_validate_zip(p, date_str="2024-12-06")
    assert inv.decompression_failure_reason is None
    assert inv.row_count == 2
    assert not inv.row_sample_validation_passed
    assert inv.row_sample_failure_reason is not None


# ---------------------------------------------------------------------------- #
# Orchestrator: confirm static guarantees, no network calls
# ---------------------------------------------------------------------------- #


def test_module_does_not_import_forbidden_libraries() -> None:
    # The script must use only stdlib + the Phase 4ax / 4aw scaffold.
    text = Path(p4bl_c.__file__).read_text(encoding="utf-8")
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
    # And the only non-stdlib import comes from the Phase 4ax aggtrades module.
    assert (
        "from prometheus.research.microstructure.aggtrades"
        in text
    )


def test_constants_are_locked() -> None:
    assert DATASET_FAMILY == "microstructure_raw_aggtrades_v001"
    assert DATASET_VERSION == "v002"
    assert SYMBOL == "BTCUSDT"
    assert SYMBOL_LIST == ("BTCUSDT",)
    assert EXPECTED_DATE_COUNT == 90
    assert EXISTING_FIXTURE_DATE == "2025-01-15"
    assert EXISTING_FIXTURE_SHA256 == (
        "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
    )
    assert p4bl_c.SCHEMA_VERSION == "v001"
    assert p4bl_c.PHASE_ID == "4bl-C"
    assert p4bl_c.SOURCE_PHASE_BOUNDARY == "4bl-B"
    assert (
        p4bl_c.BASE_COMMIT_SHA
        == "dc2240e7a43047823c8b964d52112432b7a61c79"
    )


def test_url_templates_match_locked_pattern() -> None:
    url = p4bl_c.ARCHIVE_URL_TEMPLATE.format(date="2024-12-01")
    assert url.startswith("https://data.binance.vision/")
    assert "BTCUSDT-aggTrades-2024-12-01.zip" in url
    assert_archive_url_allowed(url)
    chk = p4bl_c.CHECKSUM_URL_TEMPLATE.format(date="2024-12-01")
    assert chk == url + ".CHECKSUM"
    assert_archive_url_allowed(chk)


# ---------------------------------------------------------------------------- #
# acquire_one_date with do_network=False on existing-fixture branch
# ---------------------------------------------------------------------------- #


def _stage_existing_fixture(tmp_root: Path, sha_hex: str | None = None) -> Path:
    """Plant a fake 2025-01-15 fixture in tmp_root/raw/.../2025/01/ with a sidecar."""
    raw_dir = (
        tmp_root
        / "raw"
        / DATASET_FAMILY
        / SYMBOL
        / "2025"
        / "01"
    )
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        (i, "100000.0", "0.001", 1000 + i, 1000 + i, 1736899205000 + i * 1000, "false")
        for i in range(1, 11)
    ]
    csv_bytes = _make_csv_bytes(rows)
    zip_bytes = _zip_bytes(csv_bytes, "BTCUSDT-aggTrades-2025-01-15.csv")
    final_zip = raw_dir / "BTCUSDT-aggTrades-2025-01-15.zip"
    final_zip.write_bytes(zip_bytes)
    if sha_hex is None:
        sha_hex = hashlib.sha256(zip_bytes).hexdigest()
    sidecar = final_zip.with_suffix(final_zip.suffix + ".sha256")
    sidecar.write_text(f"{sha_hex}  {final_zip.name}\n", encoding="utf-8")
    return final_zip


def test_acquire_one_date_existing_fixture_sha_mismatch_path(tmp_path: Path) -> None:
    """If a 'fixture' exists locally but its SHA does not match the recorded
    Phase 4az SHA, the script must record checksum_mismatch and NOT overwrite."""
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    # Stage a fake fixture whose SHA will NOT match EXISTING_FIXTURE_SHA256.
    final_zip = _stage_existing_fixture(output_root)
    pre_sha = sha256_file(final_zip)
    assert pre_sha != EXISTING_FIXTURE_SHA256

    events: list[dict] = []
    res = p4bl_c.acquire_one_date(
        EXISTING_FIXTURE_DATE,
        output_root=output_root,
        events=events,
        do_network=False,
    )
    assert res.status == "checksum_mismatch"
    # File MUST NOT have been overwritten.
    assert final_zip.exists()
    assert sha256_file(final_zip) == pre_sha


def test_acquire_one_date_no_network_no_fixture_returns_retry_exhausted(
    tmp_path: Path,
) -> None:
    """With do_network=False and no fixture, the date should fail without
    contacting the network. The orchestrator must not raise."""
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    events: list[dict] = []
    res = p4bl_c.acquire_one_date(
        "2024-12-15",
        output_root=output_root,
        events=events,
        do_network=False,
    )
    # do_network=False with no fake response = no acquisition.
    assert res.status in {"retry_exhausted", "missing_404"}
    # No file under raw/.
    raw_dir = output_root / "raw" / DATASET_FAMILY / SYMBOL / "2024" / "12"
    assert not raw_dir.exists() or not list(raw_dir.iterdir())


# ---------------------------------------------------------------------------- #
# CLI dry-run smoke test
# ---------------------------------------------------------------------------- #


def test_cli_dry_run_emits_plan(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)
    rc = p4bl_c.main(
        [
            "--dry-run",
            "--output-root",
            str(output_root),
        ]
    )
    assert rc == 0
    captured = capsys.readouterr()
    out = captured.out
    assert "Phase 4bl-C dry-run plan" in out
    assert "date_count     : 90" in out
    assert "2024-12-01" in out
    assert "2025-02-28" in out
    assert "No download will be performed." in out


def test_cli_rejects_output_root_outside_microstructure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out_dir = tmp_path / "elsewhere"
    out_dir.mkdir()
    rc = p4bl_c.main(["--output-root", str(out_dir)])
    assert rc == 2
    captured = capsys.readouterr()
    assert "refusing to use --output-root outside data/microstructure/" in captured.err


# ---------------------------------------------------------------------------- #
# JSON determinism: log/manifest emit sorted-key JSON with trailing newline
# ---------------------------------------------------------------------------- #


def test_acquisition_log_and_manifest_sort_keys(tmp_path: Path) -> None:
    """Synthesize a tiny one-entry result and confirm the writers produce
    deterministic sorted-key JSON ending with a newline."""
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True)

    entry = p4bl_c.DateResult(
        date="2024-12-01",
        expected_url=p4bl_c.ARCHIVE_URL_TEMPLATE.format(date="2024-12-01"),
        expected_checksum_url=p4bl_c.CHECKSUM_URL_TEMPLATE.format(date="2024-12-01"),
        local_zip_path=(
            f"microstructure/raw/{DATASET_FAMILY}/{SYMBOL}/2024/12/"
            f"{SYMBOL}-aggTrades-2024-12-01.zip"
        ),
        local_sidecar_path=(
            f"microstructure/raw/{DATASET_FAMILY}/{SYMBOL}/2024/12/"
            f"{SYMBOL}-aggTrades-2024-12-01.zip.sha256"
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
    log_filename = (
        f"{DATASET_FAMILY}__{DATASET_VERSION}_acquisition_log.json"
    )
    log_path = output_root / "manifests" / log_filename
    test_event = {
        "timestamp_unix_ms": 1500,
        "event_type": "test",
        "date": "2024-12-01",
        "details": {},
    }
    p4bl_c.write_acquisition_log(
        log_path,
        acquisition_run_id="test-run-id",
        code_commit_sha="abc",
        started_at_unix_ms=1000,
        finished_at_unix_ms=2000,
        date_list=["2024-12-01"],
        events=[test_event],
        entries=[entry],
        overall_status="FAIL_CLOSED_NO_ACQUISITION",
        strict_fail_closed=True,
    )
    raw = log_path.read_text(encoding="utf-8")
    assert raw.endswith("\n")
    parsed = json.loads(raw)
    # Top-level keys are sorted in the serialised output.
    keys = list(parsed.keys())
    assert keys == sorted(keys)
    # Required fields present.
    for required in (
        "acquisition_run_id",
        "base_commit_sha",
        "code_commit_sha",
        "dataset_family",
        "dataset_version",
        "date_count",
        "date_list",
        "summary",
        "phase",
        "phase_id",
        "non_authorizations",
    ):
        assert required in parsed, f"missing log key: {required}"

    manifest_path = output_root / "manifests" / f"{DATASET_FAMILY}__{DATASET_VERSION}.json"
    p4bl_c.write_multiday_manifest(
        manifest_path,
        code_commit_sha="abc",
        date_list=["2024-12-01"],
        entries=[entry],
        acquisition_log_path=log_path,
        acquisition_log_sha256=sha256_file(log_path),
        output_root=output_root,
    )
    raw_m = manifest_path.read_text(encoding="utf-8")
    assert raw_m.endswith("\n")
    parsed_m = json.loads(raw_m)
    keys_m = list(parsed_m.keys())
    assert keys_m == sorted(keys_m)
    assert parsed_m["dataset_family"] == DATASET_FAMILY
    assert parsed_m["dataset_version"] == DATASET_VERSION
    assert parsed_m["research_eligible"] is False
    assert parsed_m["eligibility_gate_status"] == "pending"
    assert parsed_m["expected_file_count"] == EXPECTED_DATE_COUNT
    assert parsed_m["date_count"] == EXPECTED_DATE_COUNT
    # Governance labels block present and all-forbidden.
    gov = parsed_m["governance_labels"]
    for k in (
        "feature_computation",
        "labels",
        "ml",
        "strategy",
        "strategy_use",
    ):
        assert gov[k] == "forbidden"
    assert gov["phase"] == "4bl-C"
    assert gov["source_phase_boundary"] == "4bl-B"
    assert gov["validator"] == "phase_4ax_aggtrades_v001"
    assert gov["stop_trigger_domain"] == "trade_price_backtest_candidate"
