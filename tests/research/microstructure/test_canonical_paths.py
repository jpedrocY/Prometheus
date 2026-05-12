"""Phase 4bb-F-implementation tests for the canonical path policy helpers.

These tests verify:

- canonical gate-report id construction (with ``phase-<id>`` tag);
- canonical successor-state filename construction;
- family subdirectory mapping (raw / normalized / features / labels);
- canonical gate-report path composition;
- canonical successor-state path composition;
- sidecar body format (``<sha>  <basename>\\n`` -- two spaces, trailing
  newline);
- ``write_paired_sha256_sidecar`` atomic write + refuse-to-overwrite;
- path validation helpers (microstructure root / gate-reports family /
  successor-state);
- argument validation (empty / non-string / non-hex / bad lengths /
  path separators / wrong types).

All filesystem writes use pytest ``tmp_path`` only. The tests never
read, write, or touch any path under the project's real
``data/microstructure/`` directory.

This module is offline-only: no network I/O, no credentials, no
``.env`` / ``.mcp.json`` reads.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from prometheus.research.microstructure import (  # noqa: E402
    FAMILY_SUBDIRS,
    GATE_REPORTS_ROOT_PARTS,
    MICROSTRUCTURE_ROOT_PARTS,
    SUCCESSOR_STATE_ROOT_PARTS,
    CanonicalPathError,
    assert_canonical_path_under_microstructure,
    assert_path_under_gate_reports_subdir,
    assert_path_under_successor_state,
    compose_canonical_gate_report_id,
    compose_canonical_sidecar_body,
    compose_canonical_successor_state_filename,
    compute_canonical_file_sha256,
    derive_canonical_gate_report_path,
    derive_canonical_successor_state_path,
    derive_short_commit,
    derive_sidecar_path,
    normalize_family,
    write_paired_sha256_sidecar,
)

_FULL_SHA = "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"


def _make_microstructure_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure"
    root.mkdir(parents=True, exist_ok=True)
    return root


def test_family_subdirs_recognised() -> None:
    assert FAMILY_SUBDIRS == {
        "raw": "raw",
        "normalized": "normalized",
        "features": "features",
        "labels": "labels",
    }


def test_root_parts_locked() -> None:
    assert MICROSTRUCTURE_ROOT_PARTS == ("data", "microstructure")
    assert GATE_REPORTS_ROOT_PARTS == ("data", "microstructure", "gate-reports")
    assert SUCCESSOR_STATE_ROOT_PARTS == (
        "data",
        "microstructure",
        "successor-state",
    )


@pytest.mark.parametrize(
    "family,expected",
    [
        ("raw", "raw"),
        ("RAW", "raw"),
        ("Normalized", "normalized"),
        ("features", "features"),
        ("LABELS", "labels"),
    ],
)
def test_normalize_family_accepts_recognised(family: str, expected: str) -> None:
    assert normalize_family(family) == expected


@pytest.mark.parametrize("bad", ["", "unknown", "Raw1", "raw-extra"])
def test_normalize_family_rejects_unknown(bad: str) -> None:
    with pytest.raises(CanonicalPathError):
        normalize_family(bad)


def test_normalize_family_rejects_non_string() -> None:
    with pytest.raises(CanonicalPathError):
        normalize_family(123)  # type: ignore[arg-type]


def test_derive_short_commit_default_length_is_12() -> None:
    assert derive_short_commit(_FULL_SHA) == _FULL_SHA[:12]


def test_derive_short_commit_explicit_length() -> None:
    assert derive_short_commit(_FULL_SHA, length=7) == _FULL_SHA[:7]


@pytest.mark.parametrize(
    "value,length",
    [
        ("abc", 7),
        ("", 12),
        ("xyz_not_hex_!!", 12),
        (_FULL_SHA, 6),  # length below the floor
        (_FULL_SHA, 65),  # length exceeds sha length
    ],
)
def test_derive_short_commit_rejects_invalid(value: str, length: int) -> None:
    with pytest.raises(CanonicalPathError):
        derive_short_commit(value, length=length)


def test_derive_short_commit_rejects_non_string() -> None:
    with pytest.raises(CanonicalPathError):
        derive_short_commit(12345)  # type: ignore[arg-type]


def test_canonical_gate_report_id_format() -> None:
    report_id = compose_canonical_gate_report_id(
        dataset_family="microstructure_raw_aggtrades_v001",
        dataset_version="v001",
        phase_id="4bb-F",
        generated_at_unix_ms=1778351069361,
        code_commit_sha=_FULL_SHA,
    )
    assert report_id == (
        "microstructure_raw_aggtrades_v001__v001__phase-4bb-F__"
        "1778351069361__abcdef012345"
    )


def test_canonical_gate_report_id_supports_short_phase_id() -> None:
    report_id = compose_canonical_gate_report_id(
        dataset_family="fam",
        dataset_version="v1",
        phase_id="x",
        generated_at_unix_ms=0,
        code_commit_sha="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    )
    assert report_id == "fam__v1__phase-x__0__0123456789ab"


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "dataset_family": "",
            "dataset_version": "v1",
            "phase_id": "p",
            "generated_at_unix_ms": 1,
            "code_commit_sha": _FULL_SHA,
        },
        {
            "dataset_family": "fam",
            "dataset_version": "",
            "phase_id": "p",
            "generated_at_unix_ms": 1,
            "code_commit_sha": _FULL_SHA,
        },
        {
            "dataset_family": "fam",
            "dataset_version": "v1",
            "phase_id": "",
            "generated_at_unix_ms": 1,
            "code_commit_sha": _FULL_SHA,
        },
        {
            "dataset_family": "fam",
            "dataset_version": "v1",
            "phase_id": "p",
            "generated_at_unix_ms": -1,
            "code_commit_sha": _FULL_SHA,
        },
        {
            "dataset_family": "fam",
            "dataset_version": "v1",
            "phase_id": "p",
            "generated_at_unix_ms": True,
            "code_commit_sha": _FULL_SHA,
        },
    ],
)
def test_canonical_gate_report_id_rejects_invalid(kwargs: dict) -> None:
    with pytest.raises(CanonicalPathError):
        compose_canonical_gate_report_id(**kwargs)


def test_canonical_successor_state_filename_format() -> None:
    name = compose_canonical_successor_state_filename(
        dataset_family="microstructure_labels_aggtrades_v001",
        dataset_version="v001",
        stage_marker="stage5_research_ml_admissible",
        phase_id="4bj-G",
    )
    assert name == (
        "microstructure_labels_aggtrades_v001__v001__"
        "stage5_research_ml_admissible__phase-4bj-G"
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"dataset_family": "", "dataset_version": "v1", "stage_marker": "s", "phase_id": "p"},
        {"dataset_family": "f", "dataset_version": "", "stage_marker": "s", "phase_id": "p"},
        {"dataset_family": "f", "dataset_version": "v1", "stage_marker": "", "phase_id": "p"},
        {"dataset_family": "f", "dataset_version": "v1", "stage_marker": "s", "phase_id": ""},
    ],
)
def test_canonical_successor_state_filename_rejects_invalid(kwargs: dict) -> None:
    with pytest.raises(CanonicalPathError):
        compose_canonical_successor_state_filename(**kwargs)


def test_derive_canonical_gate_report_path_places_under_family_subdir(
    tmp_path: Path,
) -> None:
    root = _make_microstructure_root(tmp_path)
    p = derive_canonical_gate_report_path(
        microstructure_root=root,
        family="raw",
        dataset_family="microstructure_raw_aggtrades_v001",
        dataset_version="v001",
        phase_id="4bb-F",
        generated_at_unix_ms=42,
        code_commit_sha=_FULL_SHA,
    )
    assert p.parent.name == "raw"
    assert p.parent.parent.name == "gate-reports"
    assert p.parent.parent.parent == root
    assert p.suffix == ".json"
    assert "phase-4bb-F" in p.name
    # The helper does NOT create directories.
    assert not p.parent.exists()


@pytest.mark.parametrize(
    "family,expected_subdir",
    [
        ("raw", "raw"),
        ("normalized", "normalized"),
        ("features", "features"),
        ("labels", "labels"),
    ],
)
def test_derive_canonical_gate_report_path_each_family(
    tmp_path: Path, family: str, expected_subdir: str
) -> None:
    root = _make_microstructure_root(tmp_path)
    p = derive_canonical_gate_report_path(
        microstructure_root=root,
        family=family,
        dataset_family="fam",
        dataset_version="v1",
        phase_id="p",
        generated_at_unix_ms=1,
        code_commit_sha=_FULL_SHA,
    )
    assert p.parent.name == expected_subdir


def test_derive_canonical_gate_report_path_rejects_non_path(tmp_path: Path) -> None:
    with pytest.raises(CanonicalPathError):
        derive_canonical_gate_report_path(
            microstructure_root="not-a-path",  # type: ignore[arg-type]
            family="raw",
            dataset_family="fam",
            dataset_version="v1",
            phase_id="p",
            generated_at_unix_ms=1,
            code_commit_sha=_FULL_SHA,
        )


def test_derive_canonical_successor_state_path_places_under_successor_state(
    tmp_path: Path,
) -> None:
    root = _make_microstructure_root(tmp_path)
    p = derive_canonical_successor_state_path(
        microstructure_root=root,
        dataset_family="microstructure_labels_aggtrades_v001",
        dataset_version="v001",
        stage_marker="stage5",
        phase_id="4bj-G",
    )
    assert p.parent.name == "successor-state"
    assert p.parent.parent == root
    assert p.suffix == ".json"
    assert "phase-4bj-G" in p.name
    assert not p.parent.exists()


def test_derive_canonical_successor_state_path_rejects_non_path() -> None:
    with pytest.raises(CanonicalPathError):
        derive_canonical_successor_state_path(
            microstructure_root="not-a-path",  # type: ignore[arg-type]
            dataset_family="f",
            dataset_version="v1",
            stage_marker="s",
            phase_id="p",
        )


def test_derive_sidecar_path_appends_sha256() -> None:
    p = Path("a/b/c.json")
    assert derive_sidecar_path(p) == Path("a/b/c.json.sha256")


def test_derive_sidecar_path_rejects_non_path() -> None:
    with pytest.raises(CanonicalPathError):
        derive_sidecar_path("a/b/c.json")  # type: ignore[arg-type]


def test_compose_canonical_sidecar_body_format() -> None:
    sha = "0" * 64
    body = compose_canonical_sidecar_body(
        json_sha256_hex=sha, json_basename="report.json"
    )
    assert body == (sha + "  report.json\n").encode("utf-8")


@pytest.mark.parametrize(
    "sha,basename",
    [
        ("", "x.json"),
        ("not-hex", "x.json"),
        ("0" * 63, "x.json"),
        ("0" * 65, "x.json"),
        ("0" * 64, ""),
        ("0" * 64, "sub/x.json"),
        ("0" * 64, "sub\\x.json"),
    ],
)
def test_compose_canonical_sidecar_body_rejects_invalid(
    sha: str, basename: str
) -> None:
    with pytest.raises(CanonicalPathError):
        compose_canonical_sidecar_body(
            json_sha256_hex=sha, json_basename=basename
        )


def test_write_paired_sha256_sidecar_writes_two_spaces_and_newline(
    tmp_path: Path,
) -> None:
    json_path = tmp_path / "report.json"
    body = b'{"x": 1}\n'
    json_path.write_bytes(body)
    sha = hashlib.sha256(body).hexdigest()
    sidecar = write_paired_sha256_sidecar(
        json_path=json_path, json_sha256_hex=sha
    )
    assert sidecar == json_path.with_suffix(".json.sha256")
    text = sidecar.read_text(encoding="utf-8")
    assert text == f"{sha}  report.json\n"


def test_write_paired_sha256_sidecar_refuses_overwrite(tmp_path: Path) -> None:
    json_path = tmp_path / "report.json"
    json_path.write_bytes(b"x")
    sha = hashlib.sha256(b"x").hexdigest()
    write_paired_sha256_sidecar(json_path=json_path, json_sha256_hex=sha)
    with pytest.raises(CanonicalPathError):
        write_paired_sha256_sidecar(json_path=json_path, json_sha256_hex=sha)


def test_write_paired_sha256_sidecar_overwrite_when_explicitly_allowed(
    tmp_path: Path,
) -> None:
    json_path = tmp_path / "report.json"
    json_path.write_bytes(b"x")
    sha = hashlib.sha256(b"x").hexdigest()
    first = write_paired_sha256_sidecar(json_path=json_path, json_sha256_hex=sha)
    # Allow overwrite explicitly.
    second = write_paired_sha256_sidecar(
        json_path=json_path,
        json_sha256_hex=sha,
        refuse_overwrite=False,
    )
    assert second == first


def test_write_paired_sha256_sidecar_creates_parent_dirs(tmp_path: Path) -> None:
    json_path = tmp_path / "deep" / "nested" / "report.json"
    json_path.parent.mkdir(parents=True)
    json_path.write_bytes(b"y")
    sha = hashlib.sha256(b"y").hexdigest()
    sidecar = write_paired_sha256_sidecar(
        json_path=json_path, json_sha256_hex=sha
    )
    assert sidecar.exists()
    assert sidecar.parent == json_path.parent


def test_write_paired_sha256_sidecar_rejects_non_path_json(tmp_path: Path) -> None:
    with pytest.raises(CanonicalPathError):
        write_paired_sha256_sidecar(
            json_path="not-a-path",  # type: ignore[arg-type]
            json_sha256_hex="0" * 64,
        )


def test_assert_path_under_microstructure_accepts(tmp_path: Path) -> None:
    root = _make_microstructure_root(tmp_path)
    p = root / "any" / "file.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"")
    assert_canonical_path_under_microstructure(p, label="p")


def test_assert_path_under_microstructure_rejects(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(CanonicalPathError):
        assert_canonical_path_under_microstructure(p, label="p")


def test_assert_path_under_microstructure_rejects_non_path() -> None:
    with pytest.raises(CanonicalPathError):
        assert_canonical_path_under_microstructure(
            "data/microstructure/x.json",  # type: ignore[arg-type]
            label="p",
        )


def test_assert_path_under_gate_reports_subdir_accepts(tmp_path: Path) -> None:
    root = _make_microstructure_root(tmp_path)
    p = root / "gate-reports" / "raw" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"")
    assert_path_under_gate_reports_subdir(p, family="raw", label="p")


def test_assert_path_under_gate_reports_subdir_rejects_wrong_family(
    tmp_path: Path,
) -> None:
    root = _make_microstructure_root(tmp_path)
    p = root / "gate-reports" / "raw" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(CanonicalPathError):
        assert_path_under_gate_reports_subdir(p, family="normalized", label="p")


def test_assert_path_under_gate_reports_subdir_rejects_outside(
    tmp_path: Path,
) -> None:
    p = tmp_path / "elsewhere" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(CanonicalPathError):
        assert_path_under_gate_reports_subdir(p, family="raw", label="p")


def test_assert_path_under_successor_state_accepts(tmp_path: Path) -> None:
    root = _make_microstructure_root(tmp_path)
    p = root / "successor-state" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    assert_path_under_successor_state(p, label="p")


def test_assert_path_under_successor_state_rejects(tmp_path: Path) -> None:
    root = _make_microstructure_root(tmp_path)
    p = root / "gate-reports" / "raw" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(CanonicalPathError):
        assert_path_under_successor_state(p, label="p")


def test_compute_canonical_file_sha256_matches_hashlib(tmp_path: Path) -> None:
    body = b"hello world\n"
    p = tmp_path / "f.bin"
    p.write_bytes(body)
    assert compute_canonical_file_sha256(p) == hashlib.sha256(body).hexdigest()


def test_compute_canonical_file_sha256_rejects_non_path() -> None:
    with pytest.raises(CanonicalPathError):
        compute_canonical_file_sha256("not-a-path")  # type: ignore[arg-type]
