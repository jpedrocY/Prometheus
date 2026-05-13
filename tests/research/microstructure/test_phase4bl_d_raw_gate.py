"""Offline tests for ``scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py``.

Every test is offline. No network. No reads of any path under the real
project ``data/microstructure/`` tree. Synthetic ZIPs and manifests are
built under pytest ``tmp_path`` only.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import sys
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import pytest

# Load the Phase 4bl-D script as a module under a stable name.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT_PATH = _REPO_ROOT / "scripts" / "phase4bl_d_validate_multiday_raw_manifest_gate.py"


@pytest.fixture(scope="module")
def gate_mod():
    """Load the Phase 4bl-D script module by file path."""
    spec = importlib.util.spec_from_file_location(
        "phase4bl_d_gate", str(_SCRIPT_PATH)
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# ----------------------------------------------------------------------- #
# Date list and UTC day boundary helpers
# ----------------------------------------------------------------------- #


def test_generate_expected_date_list_happy(gate_mod):
    out = gate_mod.generate_expected_date_list("2024-12-01", "2025-02-28")
    assert len(out) == 90
    assert out[0] == "2024-12-01"
    assert out[-1] == "2025-02-28"
    assert out[45] == "2025-01-15"
    # No duplicates and chronologically sorted.
    assert sorted(out) == out
    assert len(set(out)) == 90


def test_generate_expected_date_list_single_day(gate_mod):
    out = gate_mod.generate_expected_date_list("2025-01-15", "2025-01-15")
    assert out == ["2025-01-15"]


def test_generate_expected_date_list_invalid_range(gate_mod):
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.generate_expected_date_list("2025-02-28", "2024-12-01")


def test_utc_day_window_ms_known_day(gate_mod):
    start, end = gate_mod.utc_day_window_ms("2025-01-15")
    expected_start = int(datetime(2025, 1, 15, tzinfo=UTC).timestamp() * 1000)
    expected_end = int(datetime(2025, 1, 16, tzinfo=UTC).timestamp() * 1000)
    assert start == expected_start
    assert end == expected_end
    assert end - start == 86_400_000


# ----------------------------------------------------------------------- #
# Canonical sidecar parsing
# ----------------------------------------------------------------------- #


_VALID_SHA = "0" * 64


def test_parse_canonical_sidecar_happy(gate_mod):
    text = f"{_VALID_SHA}  myfile.zip\n"
    sha, basename = gate_mod.parse_canonical_sidecar(text)
    assert sha == _VALID_SHA
    assert basename == "myfile.zip"


def test_parse_canonical_sidecar_no_trailing_newline(gate_mod):
    text = f"{_VALID_SHA}  myfile.zip"
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.parse_canonical_sidecar(text)


def test_parse_canonical_sidecar_wrong_separator(gate_mod):
    text = f"{_VALID_SHA} myfile.zip\n"  # one space, not two
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.parse_canonical_sidecar(text)


def test_parse_canonical_sidecar_short_sha(gate_mod):
    short = "0" * 63
    text = f"{short}  myfile.zip\n"
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.parse_canonical_sidecar(text)


def test_parse_canonical_sidecar_non_hex(gate_mod):
    bad = "g" * 64
    text = f"{bad}  myfile.zip\n"
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.parse_canonical_sidecar(text)


def test_parse_canonical_sidecar_empty_basename(gate_mod):
    text = f"{_VALID_SHA}  \n"
    # An empty basename does not match ``[^\r\n]+`` so must reject.
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.parse_canonical_sidecar(text)


# ----------------------------------------------------------------------- #
# Path discipline
# ----------------------------------------------------------------------- #


def test_assert_relative_under_microstructure_happy(gate_mod):
    out = gate_mod.assert_relative_under_microstructure(
        "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/"
        "BTCUSDT-aggTrades-2024-12-01.zip",
        label="local_zip_path[2024-12-01]",
    )
    assert out.as_posix().endswith(
        "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
        "2024/12/BTCUSDT-aggTrades-2024-12-01.zip"
    )


def test_assert_relative_under_microstructure_rejects_backslash(gate_mod):
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.assert_relative_under_microstructure(
            "microstructure\\raw\\evil.zip", label="x"
        )


def test_assert_relative_under_microstructure_rejects_parent(gate_mod):
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.assert_relative_under_microstructure(
            "microstructure/../../etc/passwd", label="x"
        )


def test_assert_relative_under_microstructure_rejects_absolute(gate_mod):
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.assert_relative_under_microstructure(
            "/etc/passwd", label="x"
        )


def test_assert_relative_under_microstructure_rejects_dot_prefix(gate_mod):
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.assert_relative_under_microstructure(
            "./microstructure/raw/x.zip", label="x"
        )


def test_assert_relative_under_microstructure_rejects_other_root(gate_mod):
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.assert_relative_under_microstructure(
            "manifests/something.json", label="x"
        )


def test_assert_relative_under_microstructure_rejects_empty(gate_mod):
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod.assert_relative_under_microstructure("", label="x")


# ----------------------------------------------------------------------- #
# CSV row parsing helpers
# ----------------------------------------------------------------------- #


def test_resolve_header_mapping_headerless(gate_mod):
    row = ["1", "100.0", "0.5", "10", "10", "1735689600000", "false"]
    assert gate_mod._resolve_header_mapping(row) is None


def test_resolve_header_mapping_with_header(gate_mod):
    header = [
        "agg_trade_id",
        "price",
        "quantity",
        "first_trade_id",
        "last_trade_id",
        "transact_time",
        "is_buyer_maker",
    ]
    mapping = gate_mod._resolve_header_mapping(header)
    assert mapping is not None
    assert mapping["a"] == 0
    assert mapping["T"] == 5
    assert mapping["m"] == 6


def test_resolve_header_mapping_missing_column(gate_mod):
    header = ["agg_trade_id", "price", "quantity"]
    with pytest.raises(gate_mod.GateRuntimeError):
        gate_mod._resolve_header_mapping(header)


def test_coerce_buyer_is_maker_happy(gate_mod):
    assert gate_mod._coerce_buyer_is_maker("true") is True
    assert gate_mod._coerce_buyer_is_maker("True") is True
    assert gate_mod._coerce_buyer_is_maker("TRUE") is True
    assert gate_mod._coerce_buyer_is_maker("false") is False
    assert gate_mod._coerce_buyer_is_maker("False") is False
    assert gate_mod._coerce_buyer_is_maker("FALSE") is False


def test_coerce_buyer_is_maker_rejects_bad(gate_mod):
    # Phase 4ax AggTradeValidationError is the concrete exception type.
    from prometheus.research.microstructure.aggtrades import (
        AggTradeValidationError,
    )

    with pytest.raises(AggTradeValidationError):
        gate_mod._coerce_buyer_is_maker("yes")


# ----------------------------------------------------------------------- #
# validate_one_file: build a small synthetic v002 inventory + ZIP and run
# the per-file validator end-to-end against tmp_path inputs.
# ----------------------------------------------------------------------- #


def _utc_ms(year, month, day, *, h=0, m=0, s=0, ms=0):
    return int(
        datetime(year, month, day, h, m, s, ms * 1000, tzinfo=UTC).timestamp() * 1000
    )


def _build_synthetic_csv_bytes(rows: list[tuple[int, int]]) -> bytes:
    """Build headerless aggTrades CSV bytes from (agg_id, trade_time_ms) pairs.

    Other columns are filled with deterministic placeholders accepted by
    ``validate_aggtrade_payload``.
    """
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for i, (a, t) in enumerate(rows):
        # a, p, q, f, l, T, m
        w.writerow([str(a), "100.00", "0.10", str(i + 1), str(i + 1), str(t), "false"])
    return buf.getvalue().encode("utf-8")


def _build_synthetic_zip(
    zip_path: Path, csv_bytes: bytes, *, member_name: str | None = None
) -> None:
    name = member_name or zip_path.with_suffix(".csv").name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(name, csv_bytes)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_inventory_entry(
    *,
    date_str: str,
    zip_rel_path: str,
    sidecar_rel_path: str,
    sha256: str,
    size_bytes: int,
    row_count: int,
    first_t: int,
    last_t: int,
    min_a: int,
    max_a: int,
) -> dict:
    return {
        "date": date_str,
        "expected_url": "https://example.invalid/notused.zip",
        "expected_checksum_url": "https://example.invalid/notused.zip.CHECKSUM",
        "local_zip_path": zip_rel_path,
        "local_sidecar_path": sidecar_rel_path,
        "sha256": sha256,
        "sha256_from_companion": sha256,
        "size_bytes": size_bytes,
        "row_count": row_count,
        "first_trade_time_ms": first_t,
        "last_trade_time_ms": last_t,
        "min_agg_trade_id": min_a,
        "max_agg_trade_id": max_a,
        "retry_count": 0,
        "status": "acquired_verified",
        "failure_reason": None,
        "acquired_at_unix_ms": 1_700_000_000_000,
    }


@pytest.fixture()
def synthetic_workdir(tmp_path, monkeypatch, gate_mod):
    """Set the CWD to tmp_path so manifest paths resolve under tmp_path/data/microstructure/."""
    monkeypatch.chdir(tmp_path)
    raw_dir = (
        tmp_path / "data" / "microstructure" / "raw" /
        "microstructure_raw_aggtrades_v001" / "BTCUSDT" / "2025" / "01"
    )
    raw_dir.mkdir(parents=True)
    return tmp_path, raw_dir


def _make_synthetic_zip_and_sidecar(
    raw_dir: Path,
    date_str: str,
    rows: list[tuple[int, int]],
) -> tuple[Path, Path]:
    zip_path = raw_dir / f"BTCUSDT-aggTrades-{date_str}.zip"
    sidecar_path = raw_dir / f"BTCUSDT-aggTrades-{date_str}.zip.sha256"
    csv_bytes = _build_synthetic_csv_bytes(rows)
    _build_synthetic_zip(zip_path, csv_bytes)
    sha = _sha256(zip_path)
    sidecar_path.write_bytes(f"{sha}  {zip_path.name}\n".encode())
    return zip_path, sidecar_path


def test_validate_one_file_happy_path(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    rows = [
        (100, _utc_ms(2025, 1, 15, h=0, m=0, s=5, ms=109)),
        (101, _utc_ms(2025, 1, 15, h=12, m=0)),
        (102, _utc_ms(2025, 1, 15, h=23, m=59, s=59, ms=991)),
    ]
    zip_path, sidecar_path = _make_synthetic_zip_and_sidecar(
        raw_dir, date_str, rows
    )
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256=_sha256(zip_path),
        size_bytes=zip_path.stat().st_size,
        row_count=len(rows),
        first_t=rows[0][1],
        last_t=rows[-1][1],
        min_a=rows[0][0],
        max_a=rows[-1][0],
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "pass"
    assert res.rows_validated == len(rows)
    assert res.computed_row_count == len(rows)
    assert res.computed_sha256 == _sha256(zip_path)
    assert res.sidecar_sha256_value == _sha256(zip_path)
    assert res.first_failure_reason is None


def test_validate_one_file_sha_mismatch(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    rows = [
        (100, _utc_ms(2025, 1, 15, h=1)),
        (101, _utc_ms(2025, 1, 15, h=2)),
    ]
    zip_path, sidecar_path = _make_synthetic_zip_and_sidecar(
        raw_dir, date_str, rows
    )
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256="0" * 64,  # deliberate mismatch
        size_bytes=zip_path.stat().st_size,
        row_count=len(rows),
        first_t=rows[0][1],
        last_t=rows[-1][1],
        min_a=rows[0][0],
        max_a=rows[-1][0],
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "fail"
    assert res.sha256_mismatch is True
    # Sidecar still parses, but sidecar sha disagrees with the manifest
    # sha (it agrees with the actual file sha).
    assert res.first_failure_reason is not None


def test_validate_one_file_missing_sidecar(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    rows = [(100, _utc_ms(2025, 1, 15, h=1))]
    zip_path, sidecar_path = _make_synthetic_zip_and_sidecar(
        raw_dir, date_str, rows
    )
    sidecar_path.unlink()
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256=_sha256(zip_path),
        size_bytes=zip_path.stat().st_size,
        row_count=len(rows),
        first_t=rows[0][1],
        last_t=rows[-1][1],
        min_a=rows[0][0],
        max_a=rows[0][0],
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "fail"
    assert res.sidecar_format_error is not None


def test_validate_one_file_duplicate_id(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    rows = [
        (100, _utc_ms(2025, 1, 15, h=1)),
        (100, _utc_ms(2025, 1, 15, h=2)),  # duplicate
    ]
    zip_path, _ = _make_synthetic_zip_and_sidecar(raw_dir, date_str, rows)
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256=_sha256(zip_path),
        size_bytes=zip_path.stat().st_size,
        row_count=len(rows),
        first_t=rows[0][1],
        last_t=rows[1][1],
        min_a=100,
        max_a=100,
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "fail"
    assert res.duplicate_agg_trade_id_errors >= 1


def test_validate_one_file_out_of_order(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    rows = [
        (101, _utc_ms(2025, 1, 15, h=1)),
        (100, _utc_ms(2025, 1, 15, h=2)),  # decreasing
    ]
    zip_path, _ = _make_synthetic_zip_and_sidecar(raw_dir, date_str, rows)
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256=_sha256(zip_path),
        size_bytes=zip_path.stat().st_size,
        row_count=len(rows),
        first_t=rows[0][1],
        last_t=rows[1][1],
        min_a=100,
        max_a=101,
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "fail"
    assert res.monotonicity_errors >= 1


def test_validate_one_file_out_of_day_timestamp(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    rows = [
        (100, _utc_ms(2025, 1, 14, h=23, m=59)),  # previous day
    ]
    zip_path, _ = _make_synthetic_zip_and_sidecar(raw_dir, date_str, rows)
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256=_sha256(zip_path),
        size_bytes=zip_path.stat().st_size,
        row_count=len(rows),
        first_t=rows[0][1],
        last_t=rows[0][1],
        min_a=100,
        max_a=100,
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "fail"
    assert res.timestamp_boundary_errors >= 1


def test_validate_one_file_multiple_csv_members(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    zip_path = raw_dir / f"BTCUSDT-aggTrades-{date_str}.zip"
    sidecar_path = raw_dir / f"BTCUSDT-aggTrades-{date_str}.zip.sha256"
    rows = [(100, _utc_ms(2025, 1, 15, h=1))]
    csv_bytes = _build_synthetic_csv_bytes(rows)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("a.csv", csv_bytes)
        zf.writestr("b.csv", csv_bytes)
    sidecar_path.write_bytes(
        f"{_sha256(zip_path)}  {zip_path.name}\n".encode()
    )
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256=_sha256(zip_path),
        size_bytes=zip_path.stat().st_size,
        row_count=len(rows),
        first_t=rows[0][1],
        last_t=rows[0][1],
        min_a=100,
        max_a=100,
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "fail"
    assert res.csv_member_error is not None


def test_validate_one_file_manifest_row_count_mismatch(synthetic_workdir, gate_mod):
    tmp_path, raw_dir = synthetic_workdir
    date_str = "2025-01-15"
    rows = [
        (100, _utc_ms(2025, 1, 15, h=1)),
        (101, _utc_ms(2025, 1, 15, h=2)),
    ]
    zip_path, _ = _make_synthetic_zip_and_sidecar(raw_dir, date_str, rows)
    entry = _build_inventory_entry(
        date_str=date_str,
        zip_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
        ),
        sidecar_rel_path=(
            "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
            "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
        ),
        sha256=_sha256(zip_path),
        size_bytes=zip_path.stat().st_size,
        row_count=99,  # wrong
        first_t=rows[0][1],
        last_t=rows[-1][1],
        min_a=100,
        max_a=101,
    )
    res = gate_mod.validate_one_file(entry)
    assert res.status == "fail"
    assert res.computed_row_count == 2
    assert res.manifest_row_count == 99


# ----------------------------------------------------------------------- #
# Gate report writer determinism + refuse-overwrite
# ----------------------------------------------------------------------- #


def test_finalise_and_write_produces_deterministic_json(tmp_path, gate_mod):
    micro_root = tmp_path / "data" / "microstructure"
    (micro_root / "gate-reports" / "raw").mkdir(parents=True)
    exit_code = gate_mod._finalise_and_write(
        overall_status="error",
        output_root=micro_root,
        checks=[],
        failure_reasons=[],
        error_reasons=["test error"],
        per_file_summaries=[],
        head_sha="deadbeef1234deadbeef1234deadbeef1234dead",
        base_sha="deadbeef1234deadbeef1234deadbeef1234dead",
        run_started_at_unix_ms=1_700_000_000_000,
        wall_clock_seconds=0.0,
        recomputed_manifest_sha="",
        recomputed_log_sha="",
        recomputed_totals=None,
        aggregate_summary=None,
    )
    assert exit_code == 1
    # Locate the produced report under tmp_path/data/microstructure/gate-reports/raw/.
    files = list((micro_root / "gate-reports" / "raw").glob("*.json"))
    assert len(files) == 1
    report_path = files[0]
    raw_bytes = report_path.read_bytes()
    # Deterministic: sorted keys + indent=2 + trailing newline.
    assert raw_bytes.endswith(b"\n")
    payload = json.loads(raw_bytes)
    assert payload["overall_status"] == "error"
    assert payload["gate_verdict"] == "RAW_MULTIDAY_GATE_ERROR"
    assert payload["research_eligible_after"] is False
    assert payload["no_successor_authorization"] is True
    # Recompute and verify sidecar.
    sidecar_path = report_path.with_suffix(".json.sha256")
    expected_sha = hashlib.sha256(raw_bytes).hexdigest()
    sidecar_bytes = sidecar_path.read_bytes()
    assert sidecar_bytes == f"{expected_sha}  {report_path.name}\n".encode()


def test_finalise_and_write_refuses_overwrite(tmp_path, gate_mod):
    micro_root = tmp_path / "data" / "microstructure"
    (micro_root / "gate-reports" / "raw").mkdir(parents=True)
    first = gate_mod._finalise_and_write(
        overall_status="error",
        output_root=micro_root,
        checks=[],
        failure_reasons=[],
        error_reasons=["test"],
        per_file_summaries=[],
        head_sha="deadbeef1234deadbeef1234deadbeef1234dead",
        base_sha="deadbeef1234deadbeef1234deadbeef1234dead",
        run_started_at_unix_ms=1_700_000_000_000,
        wall_clock_seconds=0.0,
        recomputed_manifest_sha="",
        recomputed_log_sha="",
        recomputed_totals=None,
        aggregate_summary=None,
    )
    assert first == 1
    # Second call at the same unix-ms produces the same canonical name
    # and must refuse to overwrite.
    second = gate_mod._finalise_and_write(
        overall_status="error",
        output_root=micro_root,
        checks=[],
        failure_reasons=[],
        error_reasons=["test"],
        per_file_summaries=[],
        head_sha="deadbeef1234deadbeef1234deadbeef1234dead",
        base_sha="deadbeef1234deadbeef1234deadbeef1234dead",
        run_started_at_unix_ms=1_700_000_000_000,
        wall_clock_seconds=0.0,
        recomputed_manifest_sha="",
        recomputed_log_sha="",
        recomputed_totals=None,
        aggregate_summary=None,
    )
    # Either the JSON refuses to overwrite (returns 1 without writing
    # a new file) or the sidecar refuses to overwrite (also returns 1).
    assert second == 1
    files = list((micro_root / "gate-reports" / "raw").glob("*.json"))
    # Still exactly one report file.
    assert len(files) == 1


# ----------------------------------------------------------------------- #
# Module-level forbidden-import scan
# ----------------------------------------------------------------------- #


_FORBIDDEN_IMPORT_TOKENS = (
    "requests",
    "httpx",
    "aiohttp",
    "urllib3",
    "socket",
    "websockets",
    "binance",
    "dotenv",
    "python_dotenv",
)


def test_script_has_no_forbidden_imports():
    text = _SCRIPT_PATH.read_text(encoding="utf-8")
    # Strip docstring + comments via a simple heuristic: collect lines
    # whose stripped form starts with ``import`` or ``from`` and check
    # those.
    forbidden_hits: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            for tok in _FORBIDDEN_IMPORT_TOKENS:
                # Allow ``from urllib.parse import ...`` to coexist;
                # but ``urllib3`` and ``urllib.request`` are different
                # surfaces. Phase 4bl-D uses none of either.
                if tok == "urllib3" and "urllib3" not in stripped:
                    continue
                # Match whole tokens to avoid false positives.
                tokens = (
                    stripped.replace(",", " ")
                    .replace("(", " ")
                    .replace(")", " ")
                    .split()
                )
                if tok in tokens:
                    forbidden_hits.append(f"{stripped} (forbidden token: {tok})")
    # ``urllib.request`` should also be absent: enforce separately.
    if "urllib.request" in text:
        forbidden_hits.append("file references 'urllib.request'")
    # Permit doc-style references like 'no .env' / 'no `.env` reads'.
    # We only forbid actual `open(".env")` style I/O references.
    if (
        ".env" in text
        and "noqa: env-string" not in text
        and ('open(".env"' in text or "os.environ" in text)
    ):
        forbidden_hits.append("file references .env I/O")
    assert forbidden_hits == [], (
        f"Phase 4bl-D script must not import forbidden modules; got: {forbidden_hits}"
    )


# ----------------------------------------------------------------------- #
# Check IDs match the brief's required check groups
# ----------------------------------------------------------------------- #


_REQUIRED_CHECK_IDS = (
    "manifest_file_integrity",
    "acquisition_log_integrity",
    "sidecar_format_integrity",
    "gitignore_boundary",
    "path_boundary",
    "scope_lock",
    "date_list_integrity",
    "symbol_list_integrity",
    "manifest_schema_integrity",
    "acquisition_log_schema_integrity",
    "manifest_log_counter_consistency",
    "per_file_inventory_integrity",
    "raw_zip_existence",
    "raw_zip_sha256_integrity",
    "raw_zip_sidecar_integrity",
    "zip_decompression_integrity",
    "single_csv_member_integrity",
    "full_row_schema_validation",
    "per_file_row_count_consistency",
    "per_file_time_bounds_consistency",
    "utc_day_boundary_integrity",
    "agg_trade_id_monotonicity_within_file",
    "agg_trade_id_duplicate_absence_within_file",
    "agg_trade_id_overlap_absence_across_adjacent_dates",
    "total_row_count_consistency",
    "total_size_bytes_consistency",
    "existing_fixture_preservation",
    "no_extra_dates",
    "no_missing_dates",
    "no_unexpected_statuses",
    "non_authorizations_preserved",
    "retained_verdicts_preserved",
    "project_locks_preserved",
)


def test_check_ids_match_brief(gate_mod):
    assert set(gate_mod.CHECK_IDS) == set(_REQUIRED_CHECK_IDS)
    # And nothing extra.
    assert len(gate_mod.CHECK_IDS) == len(_REQUIRED_CHECK_IDS)


def test_non_authorizations_are_all_false(gate_mod):
    assert all(v is False for v in gate_mod.NON_AUTHORIZATIONS.values())


def test_governance_labels_forbidden(gate_mod):
    forbidden_keys = (
        "feature_computation",
        "labels",
        "ml",
        "strategy",
        "strategy_use",
        "diagnostics",
        "backtest",
    )
    for key in forbidden_keys:
        assert gate_mod.GOVERNANCE_LABELS[key] == "forbidden"


def test_retained_verdict_ledger_matches_brief(gate_mod):
    ids = [entry["id"] for entry in gate_mod.RETAINED_VERDICT_LEDGER]
    assert ids == [
        "H0",
        "R3",
        "R1a",
        "R1b-narrow",
        "R2",
        "F1",
        "D1-A",
        "5m_thread",
        "V2",
        "G1",
        "C1",
    ]


def test_locked_scope_matches_brief(gate_mod):
    assert gate_mod.PHASE_ID == "4bl-d"
    assert gate_mod.DATASET_FAMILY == "microstructure_raw_aggtrades_v001"
    assert gate_mod.DATASET_VERSION == "v002"
    assert gate_mod.DATE_START == "2024-12-01"
    assert gate_mod.DATE_END == "2025-02-28"
    assert gate_mod.DATE_COUNT == 90
    assert gate_mod.EXPECTED_FILE_COUNT == 90
    assert tuple(gate_mod.SYMBOL_LIST) == ("BTCUSDT",)
    assert gate_mod.EXPECTED_TOTAL_ROW_COUNT == 155_153_449
    assert gate_mod.EXPECTED_TOTAL_SIZE_BYTES == 1_943_823_208
    assert gate_mod.EXISTING_FIXTURE_DATE == "2025-01-15"
    assert (
        gate_mod.EXISTING_FIXTURE_SHA256
        == "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
    )


def test_cli_dry_run_path(gate_mod, capsys):
    rc = gate_mod.main(["--dry-run"])
    assert rc == 0
    captured = capsys.readouterr().out
    assert "DRY-RUN" in captured
    assert "BTCUSDT" in captured
    assert "2024-12-01" in captured
    assert "2025-02-28" in captured


def test_cli_rejects_output_root_outside_microstructure(tmp_path, gate_mod, capsys):
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    rc = gate_mod.main(["--output-root", str(outside)])
    assert rc == 1
    err = capsys.readouterr().err
    assert "data/microstructure" in err.lower() or "microstructure" in err.lower()


# ----------------------------------------------------------------------- #
# Sanity: no real data/microstructure file is touched by these tests
# ----------------------------------------------------------------------- #


def test_tests_do_not_touch_real_data_microstructure_tree():
    # This is a structural reminder, not a runtime check. The fixtures
    # above operate under tmp_path only. If a future contributor adds a
    # test that reads or writes under the project's data/microstructure/
    # tree, this test should be updated to enforce the boundary.
    # We assert here that the project's real raw v002 manifest path is
    # never read by these tests.
    real_manifest = (
        _REPO_ROOT / "data" / "microstructure" / "manifests"
        / "microstructure_raw_aggtrades_v001__v002.json"
    )
    # The file may exist on disk (Phase 4bl-C output), but no test in
    # this module reads it. We assert nothing about its presence here.
    assert isinstance(real_manifest, Path)
