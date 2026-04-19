from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.data.download_state import (
    DownloadState,
    DownloadStateError,
    DownloadStatus,
    MonthDownloadState,
    read_or_init_state,
    read_state,
    write_state,
)

NOW_MS = 1_774_224_000_000


def _empty_state(name: str = "binance_usdm_btcusdt_15m") -> DownloadState:
    return DownloadState(dataset_name=name, last_updated_utc_ms=NOW_MS, months={})


def test_empty_state_status_is_pending() -> None:
    state = _empty_state()
    assert state.status_for(2026, 3) is DownloadStatus.PENDING


def test_with_month_returns_new_instance() -> None:
    state = _empty_state()
    month_state = MonthDownloadState(status=DownloadStatus.DOWNLOADED)
    updated = state.with_month(2026, 3, month_state, NOW_MS + 1)
    assert state is not updated
    assert state.status_for(2026, 3) is DownloadStatus.PENDING
    assert updated.status_for(2026, 3) is DownloadStatus.DOWNLOADED
    assert updated.last_updated_utc_ms == NOW_MS + 1


def test_month_key_format() -> None:
    state = _empty_state().with_month(
        2026, 3, MonthDownloadState(status=DownloadStatus.VERIFIED), NOW_MS
    )
    assert "2026-03" in state.months


def test_read_or_init_fresh(tmp_path: Path) -> None:
    state = read_or_init_state(tmp_path / "state.json", "binance_usdm_btcusdt_15m", NOW_MS)
    assert state.dataset_name == "binance_usdm_btcusdt_15m"
    assert state.months == {}


def test_read_or_init_existing(tmp_path: Path) -> None:
    original = _empty_state().with_month(
        2026, 3, MonthDownloadState(status=DownloadStatus.NORMALIZED), NOW_MS
    )
    path = tmp_path / "state.json"
    write_state(path, original)
    loaded = read_or_init_state(path, "binance_usdm_btcusdt_15m", NOW_MS + 100)
    assert loaded == original


def test_read_or_init_dataset_mismatch(tmp_path: Path) -> None:
    original = _empty_state("binance_usdm_btcusdt_15m")
    path = tmp_path / "state.json"
    write_state(path, original)
    with pytest.raises(DownloadStateError):
        read_or_init_state(path, "binance_usdm_ethusdt_15m", NOW_MS)


def test_write_is_atomic_no_partial_left_behind(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    write_state(path, _empty_state())
    assert path.is_file()
    assert not path.with_suffix(".json.partial").exists()


def test_write_read_round_trip_full_month_state(tmp_path: Path) -> None:
    month = MonthDownloadState(
        status=DownloadStatus.NORMALIZED,
        zip_sha256="ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8",
        downloaded_at_utc_ms=NOW_MS + 1,
        verified_at_utc_ms=NOW_MS + 2,
        normalized_at_utc_ms=NOW_MS + 3,
        raw_path="data/raw/.../BTCUSDT-15m-2026-03.zip",
        normalized_path="data/normalized/.../part-0000.parquet",
        row_count=2976,
    )
    state = _empty_state().with_month(2026, 3, month, NOW_MS)
    path = tmp_path / "state.json"
    write_state(path, state)
    reloaded = read_state(path)
    assert reloaded == state


def test_read_raises_on_malformed_json(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(DownloadStateError):
        read_state(path)


def test_read_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_state(tmp_path / "absent.json")


def test_status_enum_values() -> None:
    # Lifecycle contains both success path and failure terminals.
    assert DownloadStatus.PENDING.value == "PENDING"
    assert DownloadStatus.NORMALIZED.value == "NORMALIZED"
    assert DownloadStatus.FAILED_CHECKSUM.value == "FAILED_CHECKSUM"
