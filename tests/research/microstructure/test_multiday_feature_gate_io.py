"""Phase 4bm-J IO helpers unit tests."""
# ruff: noqa: E501  (Phase 4bm-J: long v002 SHA literals + lineage column names)
from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure.multiday_feature_gate_io import (
    MultidayFeatureGateIOError,
    assert_path_under_feature_gate_reports,
    assert_path_under_microstructure,
    atomic_write_json,
    atomic_write_sidecar,
    compose_canonical_sidecar_body,
    compute_file_sha256,
    derive_gate_report_id,
    derive_gate_report_paths,
    read_json_file,
)


def test_canonical_sidecar_body_format() -> None:
    body = compose_canonical_sidecar_body(sha256_hex="a" * 64, basename="x.json")
    expected = b"a" * 64 + b"  x.json\n"
    assert body == expected
    assert body[64:66] == b"  "  # exactly two ASCII spaces
    assert body.endswith(b"\n")
    assert b"\r" not in body
    assert not body.startswith(b"\xef\xbb\xbf")


def test_canonical_sidecar_body_rejects_bad_inputs() -> None:
    with pytest.raises(MultidayFeatureGateIOError):
        compose_canonical_sidecar_body(sha256_hex="short", basename="x.json")
    with pytest.raises(MultidayFeatureGateIOError):
        compose_canonical_sidecar_body(sha256_hex="A" * 64, basename="x.json")  # uppercase
    with pytest.raises(MultidayFeatureGateIOError):
        compose_canonical_sidecar_body(sha256_hex="a" * 64, basename="")
    with pytest.raises(MultidayFeatureGateIOError):
        compose_canonical_sidecar_body(sha256_hex="a" * 64, basename="x\ny.json")


def test_assert_path_under_microstructure(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "foo.json"
    p.parent.mkdir(parents=True)
    p.write_text("x")
    assert_path_under_microstructure(p, label="t")  # PASS
    with pytest.raises(MultidayFeatureGateIOError):
        assert_path_under_microstructure(tmp_path / "elsewhere.json", label="t")


def test_assert_path_under_feature_gate_reports(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "gate-reports" / "features" / "r.json"
    p.parent.mkdir(parents=True)
    p.write_text("x")
    assert_path_under_feature_gate_reports(p, label="t")
    with pytest.raises(MultidayFeatureGateIOError):
        assert_path_under_feature_gate_reports(
            tmp_path / "data" / "microstructure" / "manifests" / "r.json", label="t"
        )


def test_derive_gate_report_id() -> None:
    rid = derive_gate_report_id(
        dataset_family="microstructure_features_aggtrades_v001",
        dataset_version="v002",
        phase_id="4bm-j",
        unix_ms=1_700_000_000_000,
        short_commit="0123456789ab",
    )
    assert rid == "microstructure_features_aggtrades_v001__v002__phase-4bm-j__1700000000000__0123456789ab"


def test_derive_gate_report_paths_requires_features_segment(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "features"
    output_root.mkdir(parents=True)
    j, s = derive_gate_report_paths(output_root=output_root, report_id="abc")
    assert j.name == "abc.json"
    assert s.name == "abc.json.sha256"

    bad = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    bad.mkdir(parents=True)
    with pytest.raises(MultidayFeatureGateIOError):
        derive_gate_report_paths(output_root=bad, report_id="abc")


def test_atomic_write_json_refuse_overwrite(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "features"
    output_root.mkdir(parents=True)
    p = output_root / "rep.json"
    sha, size = atomic_write_json(p, {"x": 1})
    assert p.exists()
    assert size > 0
    # Re-attempt must refuse.
    with pytest.raises(MultidayFeatureGateIOError):
        atomic_write_json(p, {"x": 2})


def test_atomic_write_sidecar(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "features"
    output_root.mkdir(parents=True)
    p = output_root / "rep.json"
    sha, _ = atomic_write_json(p, {"x": 1})
    side = output_root / "rep.json.sha256"
    sc_sha, sc_size = atomic_write_sidecar(
        side, target_basename=p.name, sha256_hex=sha, refuse_overwrite=True
    )
    assert side.read_bytes() == f"{sha}  rep.json\n".encode("ascii")
    # Re-attempt must refuse.
    with pytest.raises(MultidayFeatureGateIOError):
        atomic_write_sidecar(side, target_basename=p.name, sha256_hex=sha)


def test_compute_file_sha256(tmp_path: Path) -> None:
    p = tmp_path / "x.bin"
    p.write_bytes(b"hello")
    sha, size = compute_file_sha256(p)
    assert size == 5
    assert sha == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_read_json_file_rejects_invalid_json(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_bytes(b"not json {")
    with pytest.raises(MultidayFeatureGateIOError):
        read_json_file(p)


def test_read_json_file_rejects_top_level_non_object(tmp_path: Path) -> None:
    p = tmp_path / "arr.json"
    p.write_bytes(b"[1,2,3]")
    with pytest.raises(MultidayFeatureGateIOError):
        read_json_file(p)
