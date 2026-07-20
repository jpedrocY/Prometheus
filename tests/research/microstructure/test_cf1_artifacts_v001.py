"""Phase 4bn-AZ — tests for the CF-1 artefact writers (JSON, Parquet, sidecars, inventory).

Covers: deterministic JSON serialization, required provenance / governance / non-authorization
fields, the ``.sha256`` sidecar format, inventory hashing, refusal to write outside the CF-1
output root, the canonical filename convention, and Parquet + sidecar round-trip. All writes
land under a ``tmp_path`` output root; no market data is opened.
"""

from __future__ import annotations

from pathlib import Path

import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import cf1_artifacts_v001 as art
from prometheus.research.microstructure import cf1_realized_volatility_v001 as cf1

CODE_SHA = "a" * 40


def test_output_root_is_under_research_and_gitignored_path() -> None:
    assert art.OUTPUT_ROOT_REL == "data/research/cf1_realized_volatility_substrate_test_v001"


def test_compose_filename_convention() -> None:
    name = art.compose_filename(
        family=art.FAMILY_TARGET_LAYER,
        context="v001",
        unix_ms=1_700_000_000_000,
        code_commit_sha=CODE_SHA,
        ext="parquet",
    )
    assert name == f"{art.FAMILY_TARGET_LAYER}__v001__1700000000000__aaaaaaaaaaaa.parquet"


def test_sidecar_body_format() -> None:
    sha = "0" * 64
    body = art.compose_sidecar_body(sha, "x.json")
    assert body == f"{sha}  x.json\n".encode()
    parsed_sha, parsed_name = art.parse_sidecar(body.decode())
    assert parsed_sha == sha and parsed_name == "x.json"


def test_deterministic_json_bytes_sorted_keys() -> None:
    a = art.canonical_json_bytes({"b": 1, "a": 2})
    b = art.canonical_json_bytes({"a": 2, "b": 1})
    assert a == b  # key order does not affect bytes
    assert a.endswith(b"\n")


def test_provenance_block_required_fields_and_flags() -> None:
    block = art.provenance_block(code_commit_sha=CODE_SHA, command="uv run x")
    for key in (
        "created_at_unix_ms",
        "created_at_utc",
        "base_main_commit_sha",
        "phase_4bn_ay_merge_commit_sha",
        "phase_4bn_ay_contract_tip_sha",
        "code_commit_sha",
        "command",
        "python_version",
        "numpy_version",
        "pyarrow_version",
        "symbol",
        "allowed_utc_dates",
        "forbidden_utc_ranges",
        "non_authorization_flags",
    ):
        assert key in block, key
    assert block["symbol"] == "BTCUSDT"
    assert block["base_main_commit_sha"] == cf1.BASE_MAIN_COMMIT_SHA
    # Every authorization flag is false.
    assert all(v is False for v in block["non_authorization_flags"].values())
    # Governance flags.
    assert block["v002_terminal_window_read"] is False
    assert block["sealed_test_split_touched"] is False
    assert block["test_rows_loaded"] == 0
    assert block["november_buffer_opened"] is False
    assert block["network_used"] is False
    assert block["data_acquisition_used"] is False
    assert len(block["allowed_utc_dates"]) == 244


def test_write_json_with_sidecar_roundtrip(tmp_path: Path) -> None:
    root = art.ensure_output_dirs(tmp_path)
    path = root / "proofs" / "x.json"
    payload = art.provenance_block(code_commit_sha=CODE_SHA, command="cmd")
    payload["hello"] = "world"
    sha, written = art.write_json_with_sidecar(path, payload, tmp_path)
    assert written.is_file()
    assert art.validate_json_sidecar(path) is True
    assert sha == art.sha256_file(path)


def test_refuses_write_outside_output_root(tmp_path: Path) -> None:
    art.ensure_output_dirs(tmp_path)
    outside = tmp_path / "elsewhere" / "y.json"
    with pytest.raises(art.Cf1ArtifactError):
        art.write_json_with_sidecar(outside, {"a": 1}, tmp_path)


def test_parquet_write_and_sidecar(tmp_path: Path) -> None:
    root = art.ensure_output_dirs(tmp_path)
    rows = [
        {"origin_ms": 1, "rv_target": 0.0, "evaluation_block": "B1"},
        {"origin_ms": 2, "rv_target": 1.5, "evaluation_block": "B1"},
    ]
    table = art.target_layer_table(rows)
    path = root / "targets" / "t.parquet"
    sha, written = art.write_parquet_with_sidecar(path, table, tmp_path)
    assert written.is_file()
    sidecar = path.with_suffix(path.suffix + ".sha256")
    assert sidecar.is_file()
    parsed_sha, parsed_name = art.parse_sidecar(sidecar.read_text())
    assert parsed_sha == sha and parsed_name == path.name
    back = pq.read_table(path)
    assert back.num_rows == 2


def test_inventory_hashes_and_forbidden_date_validation(tmp_path: Path) -> None:
    entries = [
        art.ArtifactEntry("fam", "proofs/x.json", "0" * 64, "proofs/x.json.sha256"),
    ]
    inv = art.build_inventory(code_commit_sha=CODE_SHA, command="cmd", entries=entries)
    assert inv["artifact_count"] == 1
    assert inv["entries"][0]["relative_path"] == "proofs/x.json"
    # Allowed-date list passes; a forbidden date fails.
    assert art.validate_no_forbidden_dates_in_list(["2024-06-01", "2024-09-30"]) is True
    assert art.validate_no_forbidden_dates_in_list(["2024-11-01"]) is False
    assert art.validate_no_forbidden_dates_in_list(["2024-10-01"]) is False
