"""Phase 4bi-B tests for feature-gate I/O primitives."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.feature_gate_io import (
    FeatureGateIOError,
    FeatureGateReportPaths,
    assert_feature_gate_report_path,
    assert_path_under_microstructure,
    atomic_write_json,
    compute_bytes_sha256,
    compute_file_sha256,
    derive_feature_gate_report_id,
    derive_feature_gate_report_paths,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
    write_sha256_sidecar,
)


def test_compute_bytes_sha256_matches_hashlib() -> None:
    payload = b"hello"
    assert compute_bytes_sha256(payload) == hashlib.sha256(payload).hexdigest()


def test_compute_file_sha256_matches_hashlib(tmp_path: Path) -> None:
    p = tmp_path / "x.bin"
    p.write_bytes(b"some bytes")
    assert compute_file_sha256(p) == hashlib.sha256(b"some bytes").hexdigest()


def test_assert_path_under_microstructure_accepts(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "x"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("y")
    assert_path_under_microstructure(p, label="p")


def test_assert_path_under_microstructure_rejects_outside(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "x"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("y")
    with pytest.raises(FeatureGateIOError):
        assert_path_under_microstructure(p, label="p")


def test_assert_path_under_microstructure_rejects_non_path() -> None:
    with pytest.raises(FeatureGateIOError):
        assert_path_under_microstructure("data/microstructure/x", label="p")  # type: ignore[arg-type]


def test_assert_feature_gate_report_path_accepts(tmp_path: Path) -> None:
    p = (
        tmp_path
        / "data"
        / "microstructure"
        / "gate-reports"
        / "features"
        / "report.json"
    )
    p.parent.mkdir(parents=True, exist_ok=True)
    assert_feature_gate_report_path(p, label="p")


def test_assert_feature_gate_report_path_rejects_normalized_namespace(
    tmp_path: Path,
) -> None:
    p = (
        tmp_path
        / "data"
        / "microstructure"
        / "gate-reports"
        / "normalized"
        / "report.json"
    )
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FeatureGateIOError):
        assert_feature_gate_report_path(p, label="p")


def test_assert_feature_gate_report_path_rejects_features_root(tmp_path: Path) -> None:
    """Bare features/ (without gate-reports/) is rejected."""
    p = tmp_path / "data" / "microstructure" / "features" / "report.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FeatureGateIOError):
        assert_feature_gate_report_path(p, label="p")


def test_read_manifest_bytes_and_parse(tmp_path: Path) -> None:
    p = tmp_path / "m.json"
    obj = {"a": 1, "b": "two"}
    p.write_text(json.dumps(obj), encoding="utf-8")
    raw = read_manifest_bytes(p)
    parsed = parse_manifest_bytes(raw)
    assert parsed == obj


def test_read_manifest_bytes_rejects_missing(tmp_path: Path) -> None:
    p = tmp_path / "missing.json"
    with pytest.raises(FeatureGateIOError):
        read_manifest_bytes(p)


def test_parse_manifest_bytes_rejects_non_dict_root() -> None:
    with pytest.raises(FeatureGateIOError):
        parse_manifest_bytes(b"[1, 2, 3]")


def test_read_sidecar_first_64(tmp_path: Path) -> None:
    p = tmp_path / "p.sha256"
    full = "a" * 64 + "  filename.txt\n"
    p.write_text(full, encoding="ascii")
    assert read_sidecar_first_64(p) == "a" * 64


def test_read_sidecar_first_64_rejects_missing(tmp_path: Path) -> None:
    p = tmp_path / "missing.sha256"
    with pytest.raises(FeatureGateIOError):
        read_sidecar_first_64(p)


def test_derive_feature_gate_report_id_format() -> None:
    rid = derive_feature_gate_report_id(
        dataset_family="microstructure_features_aggtrades_v001",
        dataset_version="v001",
        generated_at_unix_ms=1700000000000,
        code_commit_sha="abcdef1234567890",
    )
    assert rid == (
        "microstructure_features_aggtrades_v001__v001__phase-4bi-b__"
        "1700000000000__abcdef123456"
    )


def test_derive_feature_gate_report_paths(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "features"
    output_root.mkdir(parents=True, exist_ok=True)
    paths = derive_feature_gate_report_paths(
        output_root=output_root,
        dataset_family="microstructure_features_aggtrades_v001",
        dataset_version="v001",
        generated_at_unix_ms=1700000000000,
        code_commit_sha="abcdef1234567890",
    )
    assert isinstance(paths, FeatureGateReportPaths)
    assert paths.report_path.name.endswith(".json")
    assert paths.sidecar_path.name.endswith(".json.sha256")
    assert "phase-4bi-b" in paths.report_id


def test_derive_feature_gate_report_paths_rejects_non_microstructure_root(
    tmp_path: Path,
) -> None:
    with pytest.raises(FeatureGateIOError):
        derive_feature_gate_report_paths(
            output_root=tmp_path / "elsewhere",
            dataset_family="microstructure_features_aggtrades_v001",
            dataset_version="v001",
            generated_at_unix_ms=1700000000000,
            code_commit_sha="abcdef1234567890",
        )


def test_atomic_write_json_writes_and_returns_sha(tmp_path: Path) -> None:
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "features" / "x.json"
    sha, size = atomic_write_json(out, {"k": "v"}, refuse_overwrite=True)
    assert out.exists()
    on_disk = out.read_bytes()
    assert hashlib.sha256(on_disk).hexdigest() == sha
    assert size == len(on_disk)


def test_atomic_write_json_refuses_overwrite(tmp_path: Path) -> None:
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "features" / "x.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("{}", encoding="utf-8")
    with pytest.raises(FeatureGateIOError):
        atomic_write_json(out, {"k": "v"}, refuse_overwrite=True)


def test_write_sha256_sidecar_writes_format(tmp_path: Path) -> None:
    sidecar = (
        tmp_path
        / "data"
        / "microstructure"
        / "gate-reports"
        / "features"
        / "x.json.sha256"
    )
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    write_sha256_sidecar(
        sidecar,
        target_filename="x.json",
        sha256_hex="a" * 64,
        refuse_overwrite=True,
    )
    text = sidecar.read_text(encoding="utf-8")
    assert text == "a" * 64 + "  x.json\n"


def test_write_sha256_sidecar_refuses_overwrite(tmp_path: Path) -> None:
    sidecar = (
        tmp_path
        / "data"
        / "microstructure"
        / "gate-reports"
        / "features"
        / "x.json.sha256"
    )
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    sidecar.write_text("zzz", encoding="utf-8")
    with pytest.raises(FeatureGateIOError):
        write_sha256_sidecar(
            sidecar,
            target_filename="x.json",
            sha256_hex="a" * 64,
            refuse_overwrite=True,
        )
