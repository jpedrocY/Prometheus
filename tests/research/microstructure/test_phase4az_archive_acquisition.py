"""Tests for the Phase 4az BTCUSDT aggTrades archive acquisition script.

All tests are offline. The acquisition orchestrator is invoked with
``do_network=False`` and pre-staged fixture artefacts so that nothing
is fetched over the network. Every file write happens under pytest
``tmp_path`` only — never under the real project ``data/microstructure/``
tree.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

import pytest

from scripts import phase4az_acquire_btcusdt_aggtrades_archive as phase4az
from scripts.phase4az_acquire_btcusdt_aggtrades_archive import (
    AcquisitionError,
    acquire,
    assert_archive_url_allowed,
    parse_sha256_from_checksum,
    validate_aggtrades_archive,
)

# ---------------------------------------------------------------------------- #
# Helpers — build a deterministic, valid-looking aggTrades archive in tmp_path
# ---------------------------------------------------------------------------- #


def _make_csv_bytes(
    rows: list[tuple[int, str, str, int, int, int, str]],
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


def _zip_bytes(payload: bytes, member_name: str = "BTCUSDT-aggTrades-2025-01-15.csv") -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(member_name, payload)
    return out.getvalue()


# Default valid rows: trade times inside the requested 2025-01-15 UTC day.
DAY_START_MS = phase4az.DAY_START_MS  # 2025-01-15 00:00:00.000 UTC
_VALID_ROWS = [
    # (a, p, q, f, l, T, m)
    (1, "100000.50", "0.001", 1000, 1000, DAY_START_MS + 1_000, "false"),
    (2, "100000.60", "0.002", 1001, 1002, DAY_START_MS + 2_000, "true"),
    (3, "100000.40", "0.003", 1003, 1003, DAY_START_MS + 3_000, "false"),
]


def _stage_fixture(tmp_path: Path, rows: list[tuple] | None = None) -> tuple[Path, str]:
    """Pre-stage a checksum + ZIP fixture in the staging directory.

    Returns ``(staging_dir, sha256_hex)`` for assertions. The output_root
    used here is ``tmp_path/data/microstructure`` so the production
    ``data/microstructure`` discipline is observed under tmp.
    """
    if rows is None:
        rows = _VALID_ROWS
    csv_bytes = _make_csv_bytes(rows)
    zip_bytes = _zip_bytes(csv_bytes)
    sha256_hex = hashlib.sha256(zip_bytes).hexdigest()

    staging = (
        tmp_path / "data" / "microstructure" / "staging" / phase4az.DATASET_FAMILY /
        phase4az.SYMBOL / "2025" / "01"
    )
    staging.mkdir(parents=True, exist_ok=True)
    raw_filename = f"{phase4az.SYMBOL}-aggTrades-{phase4az.DATE_STR}.zip"
    (staging / f"{raw_filename}.tmp").write_bytes(zip_bytes)
    (staging / f"{raw_filename}.CHECKSUM").write_text(
        f"{sha256_hex}  {raw_filename}\n", encoding="utf-8"
    )
    return staging, sha256_hex


def _output_root(tmp_path: Path) -> Path:
    return tmp_path / "data" / "microstructure"


# ---------------------------------------------------------------------------- #
# Checksum parsing
# ---------------------------------------------------------------------------- #


def test_checksum_parsing_accepts_64_hex() -> None:
    sha = "a" * 64
    body = f"{sha}  BTCUSDT-aggTrades-2025-01-15.zip\n"
    assert parse_sha256_from_checksum(body) == sha


def test_checksum_parsing_lowercases_hex() -> None:
    sha = "A" * 64
    body = f"{sha}  file\n"
    assert parse_sha256_from_checksum(body) == sha.lower()


def test_checksum_parsing_rejects_short_hex() -> None:
    with pytest.raises(AcquisitionError):
        parse_sha256_from_checksum("a" * 60)


def test_checksum_parsing_rejects_non_hex() -> None:
    with pytest.raises(AcquisitionError):
        parse_sha256_from_checksum("z" * 64)


def test_checksum_parsing_rejects_empty() -> None:
    with pytest.raises(AcquisitionError):
        parse_sha256_from_checksum("")


def test_checksum_parsing_rejects_non_string() -> None:
    with pytest.raises(AcquisitionError):
        parse_sha256_from_checksum(b"deadbeef" * 8)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------- #
# URL allowlist
# ---------------------------------------------------------------------------- #


def test_url_allowlist_accepts_archive_zip() -> None:
    assert_archive_url_allowed(
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/"
        "BTCUSDT-aggTrades-2025-01-15.zip"
    )


def test_url_allowlist_accepts_checksum() -> None:
    assert_archive_url_allowed(
        "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/"
        "BTCUSDT-aggTrades-2025-01-15.zip.CHECKSUM"
    )


@pytest.mark.parametrize(
    "url",
    [
        "https://fapi.binance.com/fapi/v1/aggTrades?symbol=BTCUSDT",
        "https://fapi.binance.com/fapi/v1/order",
        "https://fapi.binance.com/fapi/v2/account",
        "https://fapi.binance.com/fapi/v2/positionRisk",
        "https://fapi.binance.com/fapi/v1/listenKey",
        "wss://fstream.binance.com/ws/userDataStream",
        "http://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/x.zip",
        "https://example.com/data/futures/um/daily/aggTrades/BTCUSDT/x.zip",
        "https://data.binance.vision/api_key/secret",
        "",
    ],
)
def test_url_allowlist_rejects_disallowed(url: str) -> None:
    with pytest.raises(AcquisitionError):
        assert_archive_url_allowed(url)


# ---------------------------------------------------------------------------- #
# CSV header / payload mapping
# ---------------------------------------------------------------------------- #


def test_header_csv_validates_into_phase4ax_payload(tmp_path: Path) -> None:
    csv_bytes = _make_csv_bytes(_VALID_ROWS)
    zip_bytes = _zip_bytes(csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    summary = validate_aggtrades_archive(zip_path)
    assert summary.event_count == 3
    assert summary.start_time_ms == DAY_START_MS + 1_000
    assert summary.end_time_ms == DAY_START_MS + 3_000
    assert summary.taker_side_buy_count + summary.taker_side_sell_count == 3


def test_headerless_csv_validates(tmp_path: Path) -> None:
    csv_bytes = _make_csv_bytes(_VALID_ROWS, include_header=False)
    zip_bytes = _zip_bytes(csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    summary = validate_aggtrades_archive(zip_path)
    assert summary.event_count == 3


def test_invalid_buyer_is_maker_string_fails(tmp_path: Path) -> None:
    bad = list(_VALID_ROWS)
    bad[0] = (1, "100000.50", "0.001", 1000, 1000, DAY_START_MS + 1_000, "yes")
    csv_bytes = _make_csv_bytes(bad)
    zip_bytes = _zip_bytes(csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    with pytest.raises(AcquisitionError):
        validate_aggtrades_archive(zip_path)


def test_duplicate_aggtrade_id_fails(tmp_path: Path) -> None:
    bad = list(_VALID_ROWS)
    bad[1] = (1, "100000.60", "0.002", 1001, 1002, DAY_START_MS + 2_000, "true")
    csv_bytes = _make_csv_bytes(bad)
    zip_bytes = _zip_bytes(csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    with pytest.raises(AcquisitionError):
        validate_aggtrades_archive(zip_path)


def test_out_of_order_aggtrade_id_fails(tmp_path: Path) -> None:
    bad = [
        (5, "1.0", "0.1", 1, 1, DAY_START_MS + 1_000, "false"),
        (4, "1.0", "0.1", 2, 2, DAY_START_MS + 2_000, "false"),
    ]
    csv_bytes = _make_csv_bytes(bad)
    zip_bytes = _zip_bytes(csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    with pytest.raises(AcquisitionError):
        validate_aggtrades_archive(zip_path)


def test_timestamp_outside_utc_day_fails(tmp_path: Path) -> None:
    bad = [
        (1, "1.0", "0.1", 1, 1, DAY_START_MS - 1, "false"),  # day before
    ]
    csv_bytes = _make_csv_bytes(bad)
    zip_bytes = _zip_bytes(csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    with pytest.raises(AcquisitionError):
        validate_aggtrades_archive(zip_path)


def test_timestamp_at_next_day_start_fails(tmp_path: Path) -> None:
    # day_end_ms is exclusive, so trade_time == DAY_END_MS must fail.
    bad = [
        (1, "1.0", "0.1", 1, 1, phase4az.DAY_END_MS, "false"),
    ]
    csv_bytes = _make_csv_bytes(bad)
    zip_bytes = _zip_bytes(csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    with pytest.raises(AcquisitionError):
        validate_aggtrades_archive(zip_path)


def test_empty_csv_fails(tmp_path: Path) -> None:
    zip_bytes = _zip_bytes(_make_csv_bytes([]))
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(zip_bytes)
    with pytest.raises(AcquisitionError):
        validate_aggtrades_archive(zip_path)


def test_zip_with_multiple_csv_members_fails(tmp_path: Path) -> None:
    csv_bytes = _make_csv_bytes(_VALID_ROWS)
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("a.csv", csv_bytes)
        zf.writestr("b.csv", csv_bytes)
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(out.getvalue())
    with pytest.raises(AcquisitionError):
        validate_aggtrades_archive(zip_path)


# ---------------------------------------------------------------------------- #
# End-to-end orchestrator (network=False, fixture pre-staged)
# ---------------------------------------------------------------------------- #


def test_successful_fixture_acquisition_writes_under_tmp_path(tmp_path: Path) -> None:
    _staging, sha = _stage_fixture(tmp_path)
    output_root = _output_root(tmp_path)

    result = acquire(
        output_root=output_root,
        fail_if_existing=True,
        do_network=False,
    )

    assert result.status == "SUCCESSFUL_ACQUISITION", result.failure_reason
    assert result.sha256_hex == sha
    assert result.event_count == 3

    raw_dir = (
        output_root / "raw" / phase4az.DATASET_FAMILY / phase4az.SYMBOL / "2025" / "01"
    )
    final_zip = raw_dir / f"{phase4az.SYMBOL}-aggTrades-{phase4az.DATE_STR}.zip"
    final_sha = raw_dir / f"{phase4az.SYMBOL}-aggTrades-{phase4az.DATE_STR}.zip.sha256"
    manifest_path = (
        output_root / "manifests"
        / f"{phase4az.DATASET_FAMILY}__{phase4az.DATASET_VERSION}.json"
    )
    log_path = (
        output_root / "manifests"
        / f"{phase4az.DATASET_FAMILY}__{phase4az.DATASET_VERSION}_acquisition_log.json"
    )

    assert final_zip.exists()
    assert final_sha.exists()
    assert manifest_path.exists()
    assert log_path.exists()


def test_manifest_research_eligible_false_and_pending(tmp_path: Path) -> None:
    _stage_fixture(tmp_path)
    output_root = _output_root(tmp_path)
    result = acquire(
        output_root=output_root,
        fail_if_existing=True,
        do_network=False,
    )
    assert result.status == "SUCCESSFUL_ACQUISITION"
    manifest_path = (
        output_root / "manifests"
        / f"{phase4az.DATASET_FAMILY}__{phase4az.DATASET_VERSION}.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["research_eligible"] is False
    assert manifest["eligibility_gate_status"] == "pending"
    # Governance-label preservation:
    labels = manifest["governance_labels"]
    assert labels["phase"] == "4az"
    assert labels["source_phase_boundary"] == "4ay"
    assert labels["validator"] == "phase_4ax_aggtrades_v001"
    assert labels["feature_computation"] == "forbidden"
    assert labels["strategy_use"] == "forbidden"


def test_no_feature_fields_in_manifest(tmp_path: Path) -> None:
    _stage_fixture(tmp_path)
    output_root = _output_root(tmp_path)
    acquire(
        output_root=output_root,
        fail_if_existing=True,
        do_network=False,
    )
    manifest_path = (
        output_root / "manifests"
        / f"{phase4az.DATASET_FAMILY}__{phase4az.DATASET_VERSION}.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    forbidden_keys = {
        "features",
        "feature_set",
        "feature_values",
        "edge",
        "expectancy",
        "sharpe",
        "trade_count",  # historical-strategy-shaped metadata
    }
    leaks = forbidden_keys & set(manifest.keys())
    assert not leaks, f"unexpected feature-shaped keys in manifest: {leaks}"


def test_failure_before_zip_when_checksum_invalid(tmp_path: Path) -> None:
    _staging, sha = _stage_fixture(tmp_path)
    # Corrupt the staged checksum file.
    raw_filename = f"{phase4az.SYMBOL}-aggTrades-{phase4az.DATE_STR}.zip"
    checksum_path = _staging / f"{raw_filename}.CHECKSUM"
    checksum_path.write_text("not-a-real-checksum", encoding="utf-8")

    output_root = _output_root(tmp_path)
    result = acquire(
        output_root=output_root,
        fail_if_existing=True,
        do_network=False,
    )

    assert result.status == "FAIL_CLOSED_NO_ACQUISITION"
    raw_dir = (
        output_root / "raw" / phase4az.DATASET_FAMILY / phase4az.SYMBOL / "2025" / "01"
    )
    final_zip = raw_dir / raw_filename
    manifest_path = (
        output_root / "manifests"
        / f"{phase4az.DATASET_FAMILY}__{phase4az.DATASET_VERSION}.json"
    )
    assert not final_zip.exists()
    assert not manifest_path.exists()


def test_failure_when_checksum_does_not_match_zip(tmp_path: Path) -> None:
    _staging, sha = _stage_fixture(tmp_path)
    # Tamper with the staged ZIP so its sha256 no longer matches the checksum.
    raw_filename = f"{phase4az.SYMBOL}-aggTrades-{phase4az.DATE_STR}.zip"
    zip_path = _staging / f"{raw_filename}.tmp"
    zip_path.write_bytes(zip_path.read_bytes() + b"\x00")  # tamper

    output_root = _output_root(tmp_path)
    result = acquire(
        output_root=output_root,
        fail_if_existing=True,
        do_network=False,
    )
    assert result.status == "FAIL_CLOSED_NO_ACQUISITION"
    assert "checksum mismatch" in (result.failure_reason or "")


def test_no_network_in_tests(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch urllib.request.urlopen to assert it is not called from tests."""
    def _fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError(
            "test attempted network I/O via urllib.request.urlopen; "
            "tests must run with do_network=False"
        )

    monkeypatch.setattr(
        "scripts.phase4az_acquire_btcusdt_aggtrades_archive.urllib.request.urlopen",
        _fail,
    )
    _stage_fixture(tmp_path)
    output_root = _output_root(tmp_path)
    result = acquire(
        output_root=output_root,
        fail_if_existing=True,
        do_network=False,
    )
    assert result.status == "SUCCESSFUL_ACQUISITION"


def test_dry_run_cli_prints_plan_without_network(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output_root = tmp_path / "data" / "microstructure"
    rc = phase4az.main(["--output-root", str(output_root), "--dry-run"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "Phase 4az dry-run plan" in captured.out
    assert "data.binance.vision" in captured.out
    # The dry-run must not create the directory tree.
    assert not output_root.exists()


def test_cli_rejects_output_root_outside_data_microstructure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = phase4az.main(["--output-root", str(tmp_path / "elsewhere"), "--dry-run"])
    assert rc == 2
