"""Tests for the microstructure raw_writer primitive (Phase 4aw)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.raw_writer import (
    RawWriter,
    RawWriterAlreadyExistsError,
    RawWriterError,
    RawWriterPathError,
)


def _expected_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_append_and_close_atomic(tmp_path: Path) -> None:
    target = tmp_path / "out.jsonl"
    writer = RawWriter(target)
    writer.append({"event_time_ms": 1_000, "x": 1})
    writer.append({"event_time_ms": 2_000, "x": 2})
    summary = writer.close()

    assert target.exists()
    sha_path = target.with_suffix(target.suffix + ".sha256")
    assert sha_path.exists()
    assert summary.event_count == 2
    assert summary.start_time_ms == 1_000
    assert summary.end_time_ms == 2_000
    assert summary.sha256 == _expected_sha(target)

    # JSONL contents are recoverable.
    lines = target.read_text(encoding="utf-8").splitlines()
    parsed = [json.loads(line) for line in lines]
    assert [r["event_time_ms"] for r in parsed] == [1_000, 2_000]


def test_tmp_file_disappears_after_close(tmp_path: Path) -> None:
    target = tmp_path / "out.jsonl"
    tmp_companion = target.with_suffix(target.suffix + ".tmp")
    writer = RawWriter(target)
    writer.append({"event_time_ms": 1})
    writer.close()
    assert target.exists()
    assert not tmp_companion.exists()


def test_no_overwrite_of_final_target(tmp_path: Path) -> None:
    target = tmp_path / "out.jsonl"
    target.write_text("preexisting\n", encoding="utf-8")
    with pytest.raises(RawWriterAlreadyExistsError):
        RawWriter(target)


def test_stale_tmp_blocks_construction(tmp_path: Path) -> None:
    target = tmp_path / "out.jsonl"
    stale_tmp = target.with_suffix(target.suffix + ".tmp")
    stale_tmp.write_text("partial\n", encoding="utf-8")
    with pytest.raises(RawWriterAlreadyExistsError):
        RawWriter(target)


def test_record_must_have_event_time_ms(tmp_path: Path) -> None:
    writer = RawWriter(tmp_path / "out.jsonl")
    with pytest.raises(RawWriterError):
        writer.append({"x": 1})  # missing event_time_ms
    writer.close()


def test_event_time_ms_must_be_int(tmp_path: Path) -> None:
    writer = RawWriter(tmp_path / "out.jsonl")
    with pytest.raises(RawWriterError):
        writer.append({"event_time_ms": "1234"})
    writer.close()


def test_record_must_be_dict(tmp_path: Path) -> None:
    writer = RawWriter(tmp_path / "out.jsonl")
    with pytest.raises(RawWriterError):
        writer.append([1, 2, 3])  # type: ignore[arg-type]
    writer.close()


def test_double_close_rejected(tmp_path: Path) -> None:
    writer = RawWriter(tmp_path / "out.jsonl")
    writer.append({"event_time_ms": 1})
    writer.close()
    with pytest.raises(RawWriterError):
        writer.close()


def test_append_after_close_rejected(tmp_path: Path) -> None:
    writer = RawWriter(tmp_path / "out.jsonl")
    writer.append({"event_time_ms": 1})
    writer.close()
    with pytest.raises(RawWriterError):
        writer.append({"event_time_ms": 2})


def test_directory_path_rejected(tmp_path: Path) -> None:
    with pytest.raises(RawWriterPathError):
        RawWriter(tmp_path)


def test_non_path_rejected() -> None:
    with pytest.raises(RawWriterPathError):
        RawWriter("not-a-path")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "fragment",
    [
        "data/microstructure/raw",
        "data/microstructure/normalized",
        "data\\microstructure\\raw",
    ],
)
def test_project_data_path_rejected(tmp_path: Path, fragment: str) -> None:
    # Construct a path string that contains the forbidden fragment without
    # actually creating files inside the real project tree.
    forbidden = tmp_path / fragment / "out.jsonl"
    with pytest.raises(RawWriterPathError):
        RawWriter(forbidden)


def test_sha256_matches_finalized_bytes(tmp_path: Path) -> None:
    writer = RawWriter(tmp_path / "out.jsonl")
    writer.append({"event_time_ms": 1})
    writer.append({"event_time_ms": 2})
    summary = writer.close()
    assert summary.sha256 == hashlib.sha256(
        Path(summary.path).read_bytes()
    ).hexdigest()
