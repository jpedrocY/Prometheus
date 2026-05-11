"""Phase 4bj-E label-gate I/O primitive tests.

Tests cover:

- ``assert_path_under_microstructure`` rejects non-microstructure paths;
- ``assert_label_gate_report_path`` rejects paths outside
  ``data/microstructure/gate-reports/labels/``;
- ``derive_label_gate_report_id`` produces the canonical id pattern;
- ``derive_label_gate_report_paths`` derives report + sidecar paths
  under the labels namespace;
- ``atomic_write_json`` writes deterministic sorted-keys JSON;
- ``atomic_write_json`` refuses to overwrite an existing finalised
  file;
- ``write_sha256_sidecar`` writes the standard ``<sha>  <name>`` line;
- ``write_sha256_sidecar`` refuses to overwrite;
- ``read_sidecar_first_64`` returns the 64-hex prefix;
- ``compute_file_sha256`` and ``compute_bytes_sha256`` agree with
  ``hashlib.sha256`` directly.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.label_gate_io import (
    LabelGateIOError,
    assert_label_gate_report_path,
    assert_path_under_microstructure,
    atomic_write_json,
    compute_bytes_sha256,
    compute_file_sha256,
    derive_label_gate_report_id,
    derive_label_gate_report_paths,
    read_sidecar_first_64,
    write_sha256_sidecar,
)


def test_assert_path_under_microstructure_accepts_microstructure_path(
    tmp_path: Path,
) -> None:
    p = tmp_path / "data" / "microstructure" / "labels" / "x"
    assert_path_under_microstructure(p, label="x")


def test_assert_path_under_microstructure_rejects_outside(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "x"
    with pytest.raises(LabelGateIOError):
        assert_path_under_microstructure(p, label="x")


def test_assert_label_gate_report_path_rejects_outside_labels_namespace(
    tmp_path: Path,
) -> None:
    # Under data/microstructure but not under gate-reports/labels — rejected
    p = tmp_path / "data" / "microstructure" / "x.json"
    with pytest.raises(LabelGateIOError):
        assert_label_gate_report_path(p, label="report")


def test_assert_label_gate_report_path_accepts_labels_namespace(
    tmp_path: Path,
) -> None:
    p = (
        tmp_path
        / "data"
        / "microstructure"
        / "gate-reports"
        / "labels"
        / "x.json"
    )
    assert_label_gate_report_path(p, label="report")


def test_derive_label_gate_report_id_format() -> None:
    rid = derive_label_gate_report_id(
        dataset_family="microstructure_labels_aggtrades_v001",
        dataset_version="v001",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="abcdef" * 7,  # 42-char; only first 12 used
    )
    assert rid.startswith("microstructure_labels_aggtrades_v001__v001__phase-4bj-e__")
    assert rid.endswith("__abcdefabcdef")
    assert "1700000000000" in rid


def test_derive_label_gate_report_paths(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    output_root.mkdir(parents=True, exist_ok=True)
    paths = derive_label_gate_report_paths(
        output_root=output_root,
        dataset_family="microstructure_labels_aggtrades_v001",
        dataset_version="v001",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="abcdef" * 7,
    )
    assert paths.report_path.parent == output_root.resolve()
    assert paths.sidecar_path == paths.report_path.with_suffix(".json.sha256")
    assert paths.report_id.endswith(".json") is False


def test_derive_label_gate_report_paths_rejects_non_path() -> None:
    with pytest.raises(LabelGateIOError):
        derive_label_gate_report_paths(
            output_root="not-a-path",  # type: ignore[arg-type]
            dataset_family="microstructure_labels_aggtrades_v001",
            dataset_version="v001",
            generated_at_unix_ms=0,
            code_commit_sha="0" * 12,
        )


def test_atomic_write_json_round_trip(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "gate-reports" / "labels" / "r.json"
    sha, size = atomic_write_json(p, {"a": 1, "z": 2})
    assert p.exists()
    payload = p.read_bytes()
    assert compute_bytes_sha256(payload) == sha
    assert size == len(payload)
    obj = json.loads(payload.decode("utf-8"))
    assert obj == {"a": 1, "z": 2}
    # sorted keys
    assert payload.decode("utf-8").index('"a"') < payload.decode("utf-8").index('"z"')


def test_atomic_write_json_refuse_overwrite(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "gate-reports" / "labels" / "r.json"
    atomic_write_json(p, {"a": 1})
    with pytest.raises(LabelGateIOError):
        atomic_write_json(p, {"a": 2})


def test_write_sha256_sidecar_format(tmp_path: Path) -> None:
    sc = (
        tmp_path
        / "data"
        / "microstructure"
        / "gate-reports"
        / "labels"
        / "r.json.sha256"
    )
    sha = "0" * 64
    write_sha256_sidecar(sc, target_filename="r.json", sha256_hex=sha)
    assert sc.exists()
    text = sc.read_text(encoding="ascii")
    assert text == f"{sha}  r.json\n"


def test_write_sha256_sidecar_refuse_overwrite(tmp_path: Path) -> None:
    sc = (
        tmp_path
        / "data"
        / "microstructure"
        / "gate-reports"
        / "labels"
        / "r.json.sha256"
    )
    write_sha256_sidecar(sc, target_filename="r.json", sha256_hex="0" * 64)
    with pytest.raises(LabelGateIOError):
        write_sha256_sidecar(sc, target_filename="r.json", sha256_hex="1" * 64)


def test_read_sidecar_first_64(tmp_path: Path) -> None:
    sc = tmp_path / "f.sha256"
    sha = "abc" + "1" * 61
    sc.write_text(f"{sha}  f.txt\n", encoding="ascii")
    out = read_sidecar_first_64(sc)
    assert len(out) == 64
    assert out == sha


def test_compute_file_sha256_matches_hashlib(tmp_path: Path) -> None:
    p = tmp_path / "f.bin"
    payload = b"hello world\n" * 100
    p.write_bytes(payload)
    assert compute_file_sha256(p) == hashlib.sha256(payload).hexdigest()


def test_compute_bytes_sha256_matches_hashlib() -> None:
    payload = b"\x00\x01\x02\x03 hello"
    assert compute_bytes_sha256(payload) == hashlib.sha256(payload).hexdigest()


def test_read_sidecar_first_64_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(LabelGateIOError):
        read_sidecar_first_64(tmp_path / "no-such-file.sha256")
