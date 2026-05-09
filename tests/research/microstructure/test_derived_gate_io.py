"""Phase 4bf I/O primitive tests for derived_gate_io.py."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.derived_gate_io import (
    GateIOError,
    assert_gate_report_path_under_namespace,
    assert_path_under_microstructure,
    atomic_write_json,
    compute_bytes_sha256,
    compute_file_sha256,
    derive_report_id,
    derive_report_paths,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
    resolve_derived_source_artefact_paths,
    write_sha256_sidecar,
)


def _tmp_normalized_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    root.mkdir(parents=True, exist_ok=True)
    return root


def test_compute_file_sha256_matches_compute_bytes_sha256(tmp_path: Path) -> None:
    p = tmp_path / "a.bin"
    payload = b"hello-world\n"
    p.write_bytes(payload)
    assert compute_file_sha256(p) == compute_bytes_sha256(payload)


def test_assert_path_under_microstructure_accepts_canonical(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    assert_path_under_microstructure(p)


def test_assert_path_under_microstructure_rejects_outside(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "x.json"
    with pytest.raises(GateIOError, match="must resolve under data/microstructure/"):
        assert_path_under_microstructure(p)


def test_assert_gate_report_path_accepts_namespace(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    assert_gate_report_path_under_namespace(p)


def test_assert_gate_report_path_rejects_other_namespace(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(GateIOError, match="gate-reports/normalized/"):
        assert_gate_report_path_under_namespace(p)


def test_atomic_write_json_writes_and_returns_sha(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    sha, size = atomic_write_json(p, {"a": 1, "b": [1, 2]})
    assert p.exists()
    assert size > 0
    assert sha == compute_file_sha256(p)
    payload = p.read_bytes()
    parsed = json.loads(payload.decode("utf-8"))
    assert parsed == {"a": 1, "b": [1, 2]}


def test_atomic_write_json_refuses_overwrite_by_default(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    atomic_write_json(p, {"a": 1})
    with pytest.raises(GateIOError, match="refusing to overwrite"):
        atomic_write_json(p, {"a": 2})


def test_atomic_write_json_allows_overwrite_when_disabled(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    atomic_write_json(p, {"a": 1})
    sha, _ = atomic_write_json(p, {"a": 2}, refuse_overwrite=False)
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 2}
    assert sha == compute_file_sha256(p)


def test_write_sha256_sidecar_pairs_with_target(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    target = root / "report.json"
    target.write_bytes(b"{}\n")
    sha = compute_file_sha256(target)
    sidecar = root / "report.json.sha256"
    write_sha256_sidecar(sidecar, target_filename="report.json", sha256_hex=sha)
    assert sidecar.exists()
    text = sidecar.read_text(encoding="utf-8").strip()
    assert text == f"{sha}  report.json"


def test_write_sha256_sidecar_refuses_overwrite(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    sidecar = root / "report.json.sha256"
    write_sha256_sidecar(sidecar, target_filename="report.json", sha256_hex="0" * 64)
    with pytest.raises(GateIOError, match="refusing to overwrite existing sidecar"):
        write_sha256_sidecar(sidecar, target_filename="report.json", sha256_hex="1" * 64)


def test_read_manifest_bytes_returns_raw_bytes(tmp_path: Path) -> None:
    p = tmp_path / "x.json"
    payload = b'{"k": 1}\n'
    p.write_bytes(payload)
    assert read_manifest_bytes(p) == payload


def test_parse_manifest_bytes_decodes_dict() -> None:
    payload = b'{"k": 1}'
    obj = parse_manifest_bytes(payload)
    assert obj == {"k": 1}


def test_parse_manifest_bytes_rejects_non_dict_root() -> None:
    with pytest.raises(GateIOError, match="root must be a dict"):
        parse_manifest_bytes(b"[1, 2]")


def test_read_sidecar_first_64_returns_leading_hex(tmp_path: Path) -> None:
    p = tmp_path / "x.sha256"
    p.write_text("a" * 64 + "  some-name\n", encoding="utf-8")
    assert read_sidecar_first_64(p) == "a" * 64


def test_derive_report_id_includes_short_commit() -> None:
    rid = derive_report_id(
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v001",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="abc1234567890abc",
    )
    assert rid.endswith("__abc123456789")
    assert "microstructure_normalized_aggtrades_v001__v001__1700000000000__" in rid


def test_derive_report_paths_uses_namespace(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    paths = derive_report_paths(
        output_root=output_root,
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v001",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="testcommit01",
    )
    assert paths.report_path.parent == output_root
    assert paths.sidecar_path == paths.report_path.with_suffix(".json.sha256")
    assert paths.report_id.startswith("microstructure_normalized_aggtrades_v001__v001__")


def test_derive_report_paths_rejects_output_root_outside_namespace(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "manifests"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(GateIOError, match="gate-reports/normalized/"):
        derive_report_paths(
            output_root=output_root,
            dataset_family="microstructure_normalized_aggtrades_v001",
            dataset_version="v001",
            generated_at_unix_ms=1_700_000_000_000,
            code_commit_sha="testcommit01",
        )


def test_resolve_derived_source_artefact_paths_handles_relative_paths(
    tmp_path: Path,
) -> None:
    micro_root = tmp_path / "data" / "microstructure"
    manifests = micro_root / "manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    derived_path = manifests / "microstructure_normalized_aggtrades_v001__v001.json"
    raw_path = manifests / "microstructure_raw_aggtrades_v001__v001.json"
    derived_path.write_text("{}", encoding="utf-8")
    raw_path.write_text("{}", encoding="utf-8")

    parquet_relpath = (
        "normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/"
        "2025/01/file.parquet"
    )
    raw_relpath = (
        "raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/file.zip"
    )
    derived_manifest = {
        "files": [
            {
                "path": parquet_relpath,
                "sha256": "0" * 64,
            }
        ],
        "governance_labels": {
            "source_gate_report_id": "microstructure_raw_aggtrades_v001__v001__1__abc",
        },
    }
    raw_manifest = {
        "files": [{"path": raw_relpath, "sha256": "f" * 64}],
    }

    out = resolve_derived_source_artefact_paths(
        derived_manifest_path=derived_path,
        derived_manifest=derived_manifest,
        raw_manifest_path=raw_path,
        raw_manifest=raw_manifest,
    )
    assert out.normalized_parquet_path == (micro_root / parquet_relpath).resolve()
    assert out.raw_zip_path == (micro_root / raw_relpath).resolve()
    assert out.acquisition_log_path.name.endswith("_acquisition_log.json")
    assert out.gate_report_path.parent.name == "gate-reports"


def test_resolve_derived_source_artefact_paths_rejects_missing_files(
    tmp_path: Path,
) -> None:
    micro_root = tmp_path / "data" / "microstructure"
    manifests = micro_root / "manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    derived_path = manifests / "microstructure_normalized_aggtrades_v001__v001.json"
    raw_path = manifests / "microstructure_raw_aggtrades_v001__v001.json"
    derived_path.write_text("{}", encoding="utf-8")
    raw_path.write_text("{}", encoding="utf-8")

    with pytest.raises(GateIOError, match="derived manifest has no files"):
        resolve_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest={"files": []},
            raw_manifest_path=raw_path,
            raw_manifest={"files": [{"path": "x", "sha256": "0" * 64}]},
        )


def test_resolve_derived_source_artefact_paths_rejects_missing_gate_report_id(
    tmp_path: Path,
) -> None:
    micro_root = tmp_path / "data" / "microstructure"
    manifests = micro_root / "manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    derived_path = manifests / "microstructure_normalized_aggtrades_v001__v001.json"
    raw_path = manifests / "microstructure_raw_aggtrades_v001__v001.json"
    derived_path.write_text("{}", encoding="utf-8")
    raw_path.write_text("{}", encoding="utf-8")

    derived_manifest = {
        "files": [{"path": "normalized/x.parquet", "sha256": "0" * 64}],
        "governance_labels": {},
    }
    raw_manifest = {"files": [{"path": "raw/x.zip", "sha256": "0" * 64}]}

    with pytest.raises(GateIOError, match="source_gate_report_id"):
        resolve_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
            raw_manifest_path=raw_path,
            raw_manifest=raw_manifest,
        )
