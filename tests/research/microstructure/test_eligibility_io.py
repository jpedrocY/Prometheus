"""Phase 4bb-C tests for read-only artefact loaders."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from _eligibility_fixtures import build_happy_fixture, sha256_of_file  # noqa: E402

from prometheus.research.microstructure import GateIOError  # noqa: E402
from prometheus.research.microstructure.eligibility_io import (  # noqa: E402
    assert_path_under_microstructure,
    compute_bytes_sha256,
    compute_file_sha256,
    read_acquisition_log,
    read_manifest_and_hash,
    read_sidecar,
    resolve_artefact_paths,
    scan_csv_rows_in_zip,
    scan_text_for_forbidden_tokens,
    serialise_for_token_scan,
    utc_day_start_from_archive_path,
)


def test_assert_path_under_microstructure_accepts_microstructure_path(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()
    assert_path_under_microstructure(p, label="x")


def test_assert_path_under_microstructure_rejects_other_paths(tmp_path: Path) -> None:
    bad = tmp_path / "data" / "research" / "x.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.touch()
    with pytest.raises(GateIOError):
        assert_path_under_microstructure(bad, label="bad")


def test_compute_file_sha256_matches_compute_bytes_sha256(tmp_path: Path) -> None:
    p = tmp_path / "x.bin"
    body = b"abc123\n"
    p.write_bytes(body)
    file_sha, size = compute_file_sha256(p)
    assert file_sha == compute_bytes_sha256(body)
    assert size == len(body)


def test_resolve_artefact_paths_maps_phase4az_layout(tmp_path: Path) -> None:
    fb = build_happy_fixture(tmp_path)
    paths = resolve_artefact_paths(fb.manifest_path)
    assert paths.manifest_path == fb.manifest_path
    assert paths.raw_zip_path == fb.raw_zip_path
    assert paths.sidecar_path == fb.sidecar_path
    assert paths.acquisition_log_path == fb.acquisition_log_path


def test_read_manifest_and_hash_returns_consistent_sha(tmp_path: Path) -> None:
    fb = build_happy_fixture(tmp_path)
    manifest, sha, length = read_manifest_and_hash(fb.manifest_path)
    assert manifest.symbol == "BTCUSDT"
    assert length == fb.manifest_path.stat().st_size
    assert sha == compute_bytes_sha256(fb.manifest_path.read_bytes())


def test_read_sidecar_extracts_first_64_hex(tmp_path: Path) -> None:
    fb = build_happy_fixture(tmp_path)
    text, first_64 = read_sidecar(fb.sidecar_path)
    assert len(first_64) == 64
    assert first_64 == sha256_of_file(fb.raw_zip_path)
    assert first_64 in text


def test_read_acquisition_log_returns_dict_and_sha(tmp_path: Path) -> None:
    fb = build_happy_fixture(tmp_path)
    log, sha = read_acquisition_log(fb.acquisition_log_path)
    assert isinstance(log, dict)
    assert "event_count" in log
    assert sha == compute_bytes_sha256(fb.acquisition_log_path.read_bytes())


def test_scan_csv_rows_in_zip_records_canonical_column_order(tmp_path: Path) -> None:
    fb = build_happy_fixture(tmp_path)
    summary, anomalies, size, members, ok, err = scan_csv_rows_in_zip(
        fb.raw_zip_path, expected_utc_day_start=1736899200000
    )
    assert ok is True
    assert err is None
    assert len(members) == 1
    assert summary.row_count == 8
    assert summary.csv_column_order[:7] == ("a", "p", "q", "f", "l", "T", "m")
    assert summary.unexpected_extra_columns == ()
    assert summary.duplicate_a_count == 0
    assert summary.out_of_order_a_count == 0
    assert summary.in_day_count == 8
    assert summary.out_day_count == 0


def test_scan_text_for_forbidden_tokens_detects_credential_strings() -> None:
    matches = scan_text_for_forbidden_tokens(
        "this contains api_key and listenKey and /fapi/v1/order pieces"
    )
    assert "api_key" in matches
    assert "listenkey" in matches
    assert "/fapi/v1/order" in matches


def test_scan_text_for_forbidden_tokens_returns_empty_for_clean_text() -> None:
    assert scan_text_for_forbidden_tokens("hello world") == []


def test_serialise_for_token_scan_serialises_arbitrary_values() -> None:
    out = serialise_for_token_scan({"a": 1, "b": [2, 3]})
    assert "a" in out
    out2 = serialise_for_token_scan("plain string")
    assert out2 == "plain string"


def test_utc_day_start_from_archive_path_parses_phase4az_filename(tmp_path: Path) -> None:
    p = Path("foo/bar/BTCUSDT-aggTrades-2025-01-15.zip")
    assert utc_day_start_from_archive_path(p) == 1736899200000


def test_utc_day_start_from_archive_path_returns_none_when_unparseable(tmp_path: Path) -> None:
    p = Path("foo/bar/no-date.zip")
    assert utc_day_start_from_archive_path(p) is None
