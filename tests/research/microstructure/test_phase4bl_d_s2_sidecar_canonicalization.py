"""Offline tests for Phase 4bl-D-S2 controlled sidecar canonicalization.

These tests exercise the canonicalization script in isolation using
pytest tmp_path. They do not touch real Phase 4az artefacts; they do
not require the data/microstructure/ tree to exist; they do not run
the Phase 4bl-D gate; they do not perform any network I/O.

Forbidden-import scan ensures the canonicalization script imports
nothing outside the Python standard library and contains no
credential / network / MCP / Graphify tokens.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections.abc import Iterable
from pathlib import Path

import pytest

# Resolve the script under test by file path (the scripts/ directory is
# not a package, so we import via importlib.util.spec_from_file_location).
REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPO_ROOT / "scripts" / "phase4bl_d_s2_canonicalize_sidecar.py"


@pytest.fixture(scope="module")
def script_module():
    spec = importlib.util.spec_from_file_location(
        "phase4bl_d_s2_canonicalize_sidecar", SCRIPT_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["phase4bl_d_s2_canonicalize_sidecar"] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Constants used by fixture builders
# ---------------------------------------------------------------------------

EXPECTED_ZIP_SHA = (
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
)
EXPECTED_ZIP_SIZE = 21_271_119
EXPECTED_TARGET_BASENAME = "BTCUSDT-aggTrades-2025-01-15.zip"
EXPECTED_V002_MANIFEST_SHA = (
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
)
EXPECTED_V002_ACQ_LOG_SHA = (
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
)
EXPECTED_PHASE_4BL_D_GATE_REPORT_SHA = (
    "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7"
)


def _setup_fake_repo(
    tmp_path: Path,
    *,
    sidecar_line_ending: str | None = "CRLF",
    embedded_sha_override: str | None = None,
    embedded_basename_override: str | None = None,
    sidecar_pad: bytes = b"",
) -> tuple[Path, dict]:
    """Build a tmp repo tree and return (repo_root, fakes).

    Creates stub raw zip / manifest / acq log / gate report files (whose
    SHA256s become the "expected" values via monkeypatch), then writes a
    sidecar whose embedded SHA is the fake raw zip's SHA. The line
    ending of the sidecar is selected by ``sidecar_line_ending`` (CRLF /
    LF / None). Optional overrides allow building intentionally
    malformed sidecars for negative-path tests.
    """
    raw_dir = (
        tmp_path
        / "data"
        / "microstructure"
        / "raw"
        / "microstructure_raw_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
    )
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifests_dir = tmp_path / "data" / "microstructure" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    gate_dir = tmp_path / "data" / "microstructure" / "gate-reports" / "raw"
    gate_dir.mkdir(parents=True, exist_ok=True)

    raw_zip = raw_dir / EXPECTED_TARGET_BASENAME
    raw_zip.write_bytes(b"FAKE-ZIP")
    raw_zip_sha = hashlib.sha256(raw_zip.read_bytes()).hexdigest()

    manifest = manifests_dir / "microstructure_raw_aggtrades_v001__v002.json"
    manifest.write_bytes(b'{"fake": "manifest"}')
    manifest_sha = hashlib.sha256(manifest.read_bytes()).hexdigest()

    acq_log = (
        manifests_dir
        / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
    )
    acq_log.write_bytes(b'{"fake": "log"}')
    acq_log_sha = hashlib.sha256(acq_log.read_bytes()).hexdigest()

    gate_report = (
        gate_dir
        / "microstructure_raw_aggtrades_v001__v002__phase-4bl-d__"
        "1778627360966__2576a004c18a.json"
    )
    gate_report.write_bytes(b'{"fake": "gate-report"}')
    gate_report_sha = hashlib.sha256(gate_report.read_bytes()).hexdigest()

    fakes = {
        "raw_zip_size": raw_zip.stat().st_size,
        "raw_zip_sha": raw_zip_sha,
        "manifest_sha": manifest_sha,
        "acq_log_sha": acq_log_sha,
        "gate_report_sha": gate_report_sha,
    }

    if sidecar_line_ending is not None:
        embedded_sha = embedded_sha_override or raw_zip_sha
        embedded_basename = (
            embedded_basename_override or EXPECTED_TARGET_BASENAME
        )
        line_terminator = b"\r\n" if sidecar_line_ending == "CRLF" else b"\n"
        sidecar_body = (
            embedded_sha.encode("ascii")
            + b"  "
            + embedded_basename.encode("ascii")
            + sidecar_pad
            + line_terminator
        )
        sidecar_path = raw_dir / (EXPECTED_TARGET_BASENAME + ".sha256")
        sidecar_path.write_bytes(sidecar_body)

    return tmp_path, fakes


def _patch_expected_constants(monkeypatch, module, fakes) -> None:
    monkeypatch.setattr(module, "EXPECTED_ZIP_SIZE", fakes["raw_zip_size"])
    monkeypatch.setattr(module, "EXPECTED_ZIP_SHA", fakes["raw_zip_sha"])
    monkeypatch.setattr(
        module, "EXPECTED_V002_MANIFEST_SHA", fakes["manifest_sha"]
    )
    monkeypatch.setattr(
        module, "EXPECTED_V002_ACQ_LOG_SHA", fakes["acq_log_sha"]
    )
    monkeypatch.setattr(
        module,
        "EXPECTED_PHASE_4BL_D_GATE_REPORT_SHA",
        fakes["gate_report_sha"],
    )


# ---------------------------------------------------------------------------
# parse_canonical_sidecar_body
# ---------------------------------------------------------------------------


def test_parse_crlf_sidecar(script_module):
    body = (
        b"f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
        b"  BTCUSDT-aggTrades-2025-01-15.zip\r\n"
    )
    sha, basename, line_ending = script_module.parse_canonical_sidecar_body(
        body
    )
    assert sha == EXPECTED_ZIP_SHA
    assert basename == EXPECTED_TARGET_BASENAME
    assert line_ending == "CRLF"
    assert len(body) == 100


def test_parse_lf_sidecar(script_module):
    body = (
        b"f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
        b"  BTCUSDT-aggTrades-2025-01-15.zip\n"
    )
    sha, basename, line_ending = script_module.parse_canonical_sidecar_body(
        body
    )
    assert sha == EXPECTED_ZIP_SHA
    assert basename == EXPECTED_TARGET_BASENAME
    assert line_ending == "LF"
    assert len(body) == 99


def test_parse_missing_newline_raises(script_module):
    body = b"f" * 64 + b"  basename.zip"
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.parse_canonical_sidecar_body(body)


def test_parse_one_space_separator_raises(script_module):
    body = b"f" * 64 + b" basename.zip\n"
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.parse_canonical_sidecar_body(body)


def test_parse_non_hex_sha_raises(script_module):
    body = b"g" * 64 + b"  basename.zip\n"
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.parse_canonical_sidecar_body(body)


def test_parse_wrong_length_sha_raises(script_module):
    body = b"f" * 63 + b"  basename.zip\n"
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.parse_canonical_sidecar_body(body)


def test_parse_empty_basename_raises(script_module):
    body = b"f" * 64 + b"  \n"
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.parse_canonical_sidecar_body(body)


# ---------------------------------------------------------------------------
# render_canonical_sidecar_body
# ---------------------------------------------------------------------------


def test_render_canonical_size_is_99(script_module):
    body = script_module.render_canonical_sidecar_body(
        EXPECTED_ZIP_SHA, EXPECTED_TARGET_BASENAME
    )
    assert len(body) == 99
    assert body.endswith(b"\n")
    assert not body.endswith(b"\r\n")


def test_render_canonical_two_spaces(script_module):
    body = script_module.render_canonical_sidecar_body(
        EXPECTED_ZIP_SHA, EXPECTED_TARGET_BASENAME
    )
    decoded = body.decode("ascii").rstrip("\n")
    sha, basename = decoded.split("  ", 1)
    assert sha == EXPECTED_ZIP_SHA
    assert basename == EXPECTED_TARGET_BASENAME


def test_render_canonical_rejects_path_separator(script_module):
    with pytest.raises(ValueError):
        script_module.render_canonical_sidecar_body(
            EXPECTED_ZIP_SHA, "path/to/file.zip"
        )
    with pytest.raises(ValueError):
        script_module.render_canonical_sidecar_body(
            EXPECTED_ZIP_SHA, "path\\to\\file.zip"
        )


def test_render_canonical_rejects_bad_sha(script_module):
    with pytest.raises(ValueError):
        script_module.render_canonical_sidecar_body(
            "g" * 64, EXPECTED_TARGET_BASENAME
        )
    with pytest.raises(ValueError):
        script_module.render_canonical_sidecar_body(
            "f" * 63, EXPECTED_TARGET_BASENAME
        )


# ---------------------------------------------------------------------------
# atomic_write_bytes
# ---------------------------------------------------------------------------


def test_atomic_write_writes_payload(script_module, tmp_path):
    target = tmp_path / "out.bin"
    script_module.atomic_write_bytes(target, b"hello-world\n")
    assert target.read_bytes() == b"hello-world\n"


def test_atomic_write_refuses_missing_parent(script_module, tmp_path):
    target = tmp_path / "nonexistent" / "out.bin"
    with pytest.raises(script_module.CanonicalizationPathRefusedError):
        script_module.atomic_write_bytes(target, b"x")


def test_atomic_write_overwrites_existing(script_module, tmp_path):
    target = tmp_path / "out.bin"
    target.write_bytes(b"old")
    script_module.atomic_write_bytes(target, b"new\n")
    assert target.read_bytes() == b"new\n"


# ---------------------------------------------------------------------------
# Path discipline
# ---------------------------------------------------------------------------


def test_assert_target_sidecar_rejects_other_path(
    script_module, tmp_path
):
    repo_root, _ = _setup_fake_repo(tmp_path)
    bogus = tmp_path / "somewhere_else.sha256"
    bogus.write_bytes(b"x")
    with pytest.raises(script_module.CanonicalizationPathRefusedError):
        script_module.assert_target_sidecar_path(bogus, repo_root)


def test_assert_target_sidecar_accepts_expected(
    script_module, tmp_path
):
    repo_root, _ = _setup_fake_repo(tmp_path)
    expected = repo_root / script_module.TARGET_SIDECAR_REL
    # Should not raise.
    script_module.assert_target_sidecar_path(expected, repo_root)


def test_assert_report_path_rejects_outside_root(
    script_module, tmp_path
):
    outside = tmp_path / "outside_report.json"
    with pytest.raises(script_module.CanonicalizationPathRefusedError):
        script_module.assert_report_path_under_canonicalization_reports(
            outside, tmp_path
        )


def test_assert_report_path_accepts_inside_root(
    script_module, tmp_path
):
    inside = (
        tmp_path
        / "data"
        / "microstructure"
        / "canonicalization-reports"
        / "raw"
        / "report.json"
    )
    inside.parent.mkdir(parents=True, exist_ok=True)
    # Should not raise.
    script_module.assert_report_path_under_canonicalization_reports(
        inside, tmp_path
    )


# ---------------------------------------------------------------------------
# verify_preconditions
# ---------------------------------------------------------------------------


def test_verify_preconditions_happy_path(
    script_module, tmp_path, monkeypatch
):
    repo_root, fakes = _setup_fake_repo(tmp_path, sidecar_line_ending="CRLF")
    _patch_expected_constants(monkeypatch, script_module, fakes)
    pre = script_module.verify_preconditions(repo_root)
    assert pre["pre_sidecar_size"] == 100
    assert pre["pre_sidecar_line_ending"] == "CRLF"
    assert pre["embedded_sha"] == fakes["raw_zip_sha"]
    assert pre["embedded_basename"] == EXPECTED_TARGET_BASENAME
    assert pre["raw_zip_sha_before"] == fakes["raw_zip_sha"]
    assert pre["v002_manifest_sha_before"] == fakes["manifest_sha"]
    assert pre["v002_acq_log_sha_before"] == fakes["acq_log_sha"]
    assert (
        pre["phase_4bl_d_gate_report_sha_before"] == fakes["gate_report_sha"]
    )


def test_verify_preconditions_refuses_lf_sidecar(
    script_module, tmp_path, monkeypatch
):
    repo_root, fakes = _setup_fake_repo(tmp_path, sidecar_line_ending="LF")
    _patch_expected_constants(monkeypatch, script_module, fakes)
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.verify_preconditions(repo_root)


def test_verify_preconditions_refuses_wrong_embedded_sha(
    script_module, tmp_path, monkeypatch
):
    # Override the embedded SHA with a clearly-wrong 64-char hex string;
    # body length stays 100 bytes so the size check passes and the
    # embedded-SHA check fires.
    repo_root, fakes = _setup_fake_repo(
        tmp_path,
        sidecar_line_ending="CRLF",
        embedded_sha_override="a" * 64,
    )
    _patch_expected_constants(monkeypatch, script_module, fakes)
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.verify_preconditions(repo_root)


def test_verify_preconditions_refuses_wrong_basename(
    script_module, tmp_path, monkeypatch
):
    # Override the embedded basename with a same-length wrong basename
    # so the size check passes and the basename check fires.
    wrong_basename = "ZTCUSDT-aggTrades-2025-01-15.zip"
    assert len(wrong_basename) == len(EXPECTED_TARGET_BASENAME)
    repo_root, fakes = _setup_fake_repo(
        tmp_path,
        sidecar_line_ending="CRLF",
        embedded_basename_override=wrong_basename,
    )
    _patch_expected_constants(monkeypatch, script_module, fakes)
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.verify_preconditions(repo_root)


def test_verify_preconditions_refuses_wrong_raw_zip_sha(
    script_module, tmp_path, monkeypatch
):
    repo_root, fakes = _setup_fake_repo(tmp_path, sidecar_line_ending="CRLF")
    _patch_expected_constants(monkeypatch, script_module, fakes)
    # Corrupt the raw zip after fakes are computed; expected SHA still
    # points at the original FAKE-ZIP SHA, so verify_preconditions must
    # detect the mismatch.
    raw_zip = (
        tmp_path
        / "data"
        / "microstructure"
        / "raw"
        / "microstructure_raw_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / EXPECTED_TARGET_BASENAME
    )
    raw_zip.write_bytes(b"DIFFERENT-CONTENT")
    with pytest.raises(script_module.CanonicalizationPreconditionError):
        script_module.verify_preconditions(repo_root)


# ---------------------------------------------------------------------------
# End-to-end main()
# ---------------------------------------------------------------------------


def test_main_happy_path(script_module, tmp_path, monkeypatch, capsys):
    repo_root, fakes = _setup_fake_repo(tmp_path, sidecar_line_ending="CRLF")
    _patch_expected_constants(monkeypatch, script_module, fakes)

    argv = [
        "--repo-root",
        str(repo_root),
        "--base-commit-sha",
        "0d51bd7bac1eec1e11d7bad280e480dd8674a97f",
        "--code-commit-sha",
        "0d51bd7bac1eec1e11d7bad280e480dd8674a97f",
    ]
    rc = script_module.main(argv)
    assert rc == 0

    # Verify the target sidecar is now LF, 99 bytes.
    target = repo_root / script_module.TARGET_SIDECAR_REL
    body = target.read_bytes()
    assert len(body) == 99
    assert body.endswith(b"\n")
    assert not body.endswith(b"\r\n")
    # Embedded SHA in the canonicalized sidecar must equal the fake raw
    # zip's SHA (which is what the test fixture writes into the
    # pre-state sidecar).
    assert body.decode("ascii").startswith(fakes["raw_zip_sha"] + "  ")
    assert body.decode("ascii").rstrip("\n").endswith(EXPECTED_TARGET_BASENAME)

    # Verify a canonicalization report and sidecar were produced.
    reports_dir = (
        repo_root
        / "data"
        / "microstructure"
        / "canonicalization-reports"
        / "raw"
    )
    reports = list(reports_dir.glob("*.json"))
    assert len(reports) == 1
    sidecars = list(reports_dir.glob("*.json.sha256"))
    assert len(sidecars) == 1

    payload = reports[0].read_bytes()
    data = json.loads(payload.decode("utf-8"))
    assert data["schema_version"] == "v001"
    assert data["phase_id"] == "4bl-D-S2"
    assert data["mutation_type"] == (
        "metadata_sidecar_line_ending_canonicalization"
    )
    assert data["pre_sidecar_size_bytes"] == 100
    assert data["post_sidecar_size_bytes"] == 99
    assert data["byte_delta"] == -1
    assert data["only_target_sidecar_mutated"] is True
    assert data["raw_zip_mutated"] is False
    assert data["manifest_mutated"] is False
    assert data["acquisition_log_mutated"] is False
    assert data["gate_report_mutated"] is False
    assert data["successor_authorized"] is False
    assert data["phase_4bl_d_r_authorized"] is False
    assert data["phase_4bl_e_authorized"] is False
    assert data["embedded_zip_sha256_before"] == data["embedded_zip_sha256_after"]
    assert data["target_zip_sha256_before"] == data["target_zip_sha256_after"]
    assert (
        data["v002_manifest_sha256_before"]
        == data["v002_manifest_sha256_after"]
    )
    assert (
        data["v002_acquisition_log_sha256_before"]
        == data["v002_acquisition_log_sha256_after"]
    )
    assert (
        data["phase_4bl_d_gate_report_sha256_before"]
        == data["phase_4bl_d_gate_report_sha256_after"]
    )

    # Sidecar body must use canonical two-space + LF format.
    sidecar_bytes = sidecars[0].read_bytes()
    assert sidecar_bytes.endswith(b"\n")
    assert not sidecar_bytes.endswith(b"\r\n")
    decoded = sidecar_bytes.decode("ascii").rstrip("\n")
    sha, basename = decoded.split("  ", 1)
    assert len(sha) == 64
    assert basename == reports[0].name
    # Sidecar SHA must equal SHA256 of the report file.
    expected_sha = hashlib.sha256(payload).hexdigest()
    assert sha == expected_sha


def test_main_dry_run_does_not_mutate(
    script_module, tmp_path, monkeypatch, capsys
):
    repo_root, fakes = _setup_fake_repo(tmp_path, sidecar_line_ending="CRLF")
    _patch_expected_constants(monkeypatch, script_module, fakes)
    target = repo_root / script_module.TARGET_SIDECAR_REL
    pre_bytes = target.read_bytes()
    rc = script_module.main(["--repo-root", str(repo_root), "--dry-run"])
    assert rc == 0
    assert target.read_bytes() == pre_bytes
    reports_dir = (
        repo_root
        / "data"
        / "microstructure"
        / "canonicalization-reports"
        / "raw"
    )
    assert not reports_dir.exists() or not list(reports_dir.glob("*"))


def test_report_serialization_is_deterministic(script_module):
    report = {
        "z": 1,
        "a": 2,
        "nested": {"b": 1, "a": 2},
    }
    s1 = script_module.serialize_report(report)
    s2 = script_module.serialize_report(report)
    assert s1 == s2
    assert s1.endswith(b"\n")
    assert s1.count(b"\r\n") == 0


# ---------------------------------------------------------------------------
# Forbidden-import scan (static)
# ---------------------------------------------------------------------------


FORBIDDEN_IMPORT_MODULES: Iterable[str] = (
    "requests",
    "httpx",
    "aiohttp",
    "urllib3",
    "websockets",
    "binance",
    "dotenv",
    "python_dotenv",
    "socket",
    "urllib.request",
    "urllib.parse",
    "urllib.error",
    "urllib",
)

FORBIDDEN_RUNTIME_TOKENS: Iterable[str] = (
    "API_KEY",
    "secret(",
    "signature(",
    "listenKey",
    "userDataStream",
    "/fapi/v1/order",
    "/fapi/v2/account",
    "/fapi/v2/positionRisk",
    "/fapi/v1/leverage",
    "/fapi/v1/marginType",
    "/fapi/v1/forceOrders",
    "Graphify",
    "os.environ",
    "os.getenv",
    "getpass",
)


def _iter_import_lines(source: str):
    """Yield logical import lines from *source* (excluding comments)."""
    for raw_line in source.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            continue
        if stripped.startswith(("import ", "from ")):
            yield stripped


def test_script_has_no_forbidden_imports():
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    import_lines = list(_iter_import_lines(source))
    # Build a simple "module head" string for each import statement.
    head_tokens: list[str] = []
    for line in import_lines:
        # Drop trailing comments
        head = line.split("#", 1)[0].strip()
        # Strip ' as X' alias suffix
        head = head.split(" as ", 1)[0]
        # Normalize whitespace
        parts = head.split()
        if not parts:
            continue
        if parts[0] == "import":
            head_tokens.extend(parts[1:])
        elif parts[0] == "from" and len(parts) >= 2:
            head_tokens.append(parts[1])
    for forbidden in FORBIDDEN_IMPORT_MODULES:
        for tok in head_tokens:
            assert not tok.startswith(forbidden), (
                f"forbidden import found: {tok!r} (matches {forbidden!r})"
            )


def test_script_has_no_runtime_credential_tokens():
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    # Drop the module docstring header (which is allowed to mention these
    # tokens descriptively in the safety preamble).
    stripped = source.split('"""', 2)
    body = stripped[2] if len(stripped) == 3 else source
    body = "\n".join(
        line for line in body.splitlines() if not line.lstrip().startswith("#")
    )
    for tok in FORBIDDEN_RUNTIME_TOKENS:
        assert tok not in body, f"forbidden runtime token found: {tok!r}"
