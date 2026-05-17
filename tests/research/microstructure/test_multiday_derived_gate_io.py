"""Phase 4bm-D I/O primitive tests for multiday_derived_gate_io.py.

These tests exercise every public helper in
:mod:`prometheus.research.microstructure.multiday_derived_gate_io`
exclusively under pytest ``tmp_path`` directories. They never touch
the real ``data/microstructure/`` tree.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.multiday_derived_gate_io import (
    PHASE_4BM_D_ID_SEGMENT,
    GateIOError,
    MultidayDerivedSourceArtefactPaths,
    MultidayGateReportPaths,
    MultidayPerFileArtefactPaths,
    assert_gate_report_path_under_namespace,
    assert_path_under_microstructure,
    atomic_write_json,
    compute_bytes_sha256,
    compute_file_sha256,
    compute_file_size,
    derive_report_id,
    derive_report_paths,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
    resolve_multiday_derived_source_artefact_paths,
    write_sha256_sidecar,
)


def _tmp_normalized_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _tmp_microstructure_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure"
    (root / "manifests").mkdir(parents=True, exist_ok=True)
    (root / "gate-reports" / "raw").mkdir(parents=True, exist_ok=True)
    (root / "successor-state").mkdir(parents=True, exist_ok=True)
    return root


# ---------------------------------------------------------------------------
# compute_file_sha256 / compute_bytes_sha256 / compute_file_size
# ---------------------------------------------------------------------------


def test_compute_file_sha256_matches_compute_bytes_sha256(tmp_path: Path) -> None:
    p = tmp_path / "a.bin"
    payload = b"hello-multiday\n"
    p.write_bytes(payload)
    assert compute_file_sha256(p) == compute_bytes_sha256(payload)


def test_compute_file_sha256_streams_with_chunk_size(tmp_path: Path) -> None:
    p = tmp_path / "big.bin"
    payload = b"A" * (3 * 1024 * 1024)
    p.write_bytes(payload)
    assert compute_file_sha256(p, chunk_size=1024) == compute_bytes_sha256(payload)


def test_compute_file_size_returns_byte_length(tmp_path: Path) -> None:
    p = tmp_path / "x.bin"
    p.write_bytes(b"0123456789")
    assert compute_file_size(p) == 10


# ---------------------------------------------------------------------------
# assert_path_under_microstructure / assert_gate_report_path_under_namespace
# ---------------------------------------------------------------------------


def test_assert_path_under_microstructure_accepts_canonical(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    assert_path_under_microstructure(p)


def test_assert_path_under_microstructure_rejects_outside(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "x.json"
    with pytest.raises(GateIOError, match="data/microstructure/"):
        assert_path_under_microstructure(p)


def test_assert_path_under_microstructure_uses_custom_label(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "x.json"
    with pytest.raises(GateIOError, match="custom_label"):
        assert_path_under_microstructure(p, label="custom_label")


def test_assert_gate_report_path_accepts_namespace(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    assert_gate_report_path_under_namespace(p)


def test_assert_gate_report_path_rejects_manifests_dir(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(GateIOError, match="gate-reports/normalized/"):
        assert_gate_report_path_under_namespace(p)


def test_assert_gate_report_path_rejects_outside_microstructure(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "report.json"
    with pytest.raises(GateIOError, match="gate-reports/normalized/"):
        assert_gate_report_path_under_namespace(p)


# ---------------------------------------------------------------------------
# read_manifest_bytes / parse_manifest_bytes / read_sidecar_first_64
# ---------------------------------------------------------------------------


def test_read_manifest_bytes_returns_raw_bytes(tmp_path: Path) -> None:
    p = tmp_path / "x.json"
    payload = b'{"k": 1}\n'
    p.write_bytes(payload)
    assert read_manifest_bytes(p) == payload


def test_parse_manifest_bytes_decodes_dict() -> None:
    payload = b'{"k": 1, "nested": {"a": [1, 2]}}'
    obj = parse_manifest_bytes(payload)
    assert obj == {"k": 1, "nested": {"a": [1, 2]}}


def test_parse_manifest_bytes_rejects_non_dict_root() -> None:
    with pytest.raises(GateIOError, match="root must be a dict"):
        parse_manifest_bytes(b"[1, 2]")


def test_parse_manifest_bytes_rejects_non_dict_scalar() -> None:
    with pytest.raises(GateIOError, match="root must be a dict"):
        parse_manifest_bytes(b'"string"')


def test_read_sidecar_first_64_returns_leading_hex(tmp_path: Path) -> None:
    p = tmp_path / "x.sha256"
    sha = "a" * 64
    p.write_text(f"{sha}  some-name\n", encoding="utf-8")
    assert read_sidecar_first_64(p) == sha


def test_read_sidecar_first_64_truncates_long_input(tmp_path: Path) -> None:
    p = tmp_path / "x.sha256"
    p.write_text(("0123456789abcdef" * 8) + "  basename\n", encoding="utf-8")
    out = read_sidecar_first_64(p)
    assert len(out) == 64
    assert out == "0123456789abcdef" * 4


# ---------------------------------------------------------------------------
# derive_report_id / derive_report_paths
# ---------------------------------------------------------------------------


def test_derive_report_id_uses_phase_4bm_d_segment() -> None:
    rid = derive_report_id(
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v002",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="abc1234567890abcdef0",
    )
    assert PHASE_4BM_D_ID_SEGMENT in rid
    assert rid == (
        "microstructure_normalized_aggtrades_v001__v002__"
        "phase-4bm-d__1700000000000__abc123456789"
    )


def test_derive_report_id_uses_short_commit_first_12() -> None:
    rid = derive_report_id(
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v002",
        generated_at_unix_ms=1,
        code_commit_sha="0" * 40,
    )
    assert rid.endswith("__" + "0" * 12)


def test_derive_report_paths_uses_namespace(tmp_path: Path) -> None:
    output_root = _tmp_normalized_root(tmp_path)
    paths = derive_report_paths(
        output_root=output_root,
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v002",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="testcommit01ab",
    )
    assert isinstance(paths, MultidayGateReportPaths)
    assert paths.report_path.parent == output_root.resolve()
    assert paths.sidecar_path == paths.report_path.with_suffix(".json.sha256")
    assert paths.report_id.endswith("__testcommit01")
    assert "phase-4bm-d" in paths.report_id


def test_derive_report_paths_rejects_output_root_outside_microstructure(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "elsewhere"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(GateIOError, match="data/microstructure/"):
        derive_report_paths(
            output_root=output_root,
            dataset_family="microstructure_normalized_aggtrades_v001",
            dataset_version="v002",
            generated_at_unix_ms=1,
            code_commit_sha="cccccccccccc",
        )


def test_derive_report_paths_rejects_manifests_output_root(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "manifests"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(GateIOError, match="gate-reports/normalized/"):
        derive_report_paths(
            output_root=output_root,
            dataset_family="microstructure_normalized_aggtrades_v001",
            dataset_version="v002",
            generated_at_unix_ms=1,
            code_commit_sha="cccccccccccc",
        )


# ---------------------------------------------------------------------------
# atomic_write_json
# ---------------------------------------------------------------------------


def test_atomic_write_json_writes_sorted_keys_and_returns_sha(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    sha, size = atomic_write_json(p, {"b": 2, "a": 1})
    assert p.exists()
    assert size > 0
    assert sha == compute_file_sha256(p)
    # sort_keys=True ⇒ "a" precedes "b" in the serialised body.
    text = p.read_text(encoding="utf-8")
    assert text.index('"a"') < text.index('"b"')
    parsed = json.loads(text)
    assert parsed == {"a": 1, "b": 2}


def test_atomic_write_json_refuses_overwrite_by_default(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    atomic_write_json(p, {"a": 1})
    with pytest.raises(GateIOError, match="refusing to overwrite"):
        atomic_write_json(p, {"a": 2})


def test_atomic_write_json_allows_overwrite_when_explicitly_disabled(
    tmp_path: Path,
) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    atomic_write_json(p, {"a": 1})
    sha, _ = atomic_write_json(p, {"a": 2}, refuse_overwrite=False)
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 2}
    assert sha == compute_file_sha256(p)


def test_atomic_write_json_creates_parent_directories(tmp_path: Path) -> None:
    deep = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized" / "sub"
    p = deep / "report.json"
    atomic_write_json(p, {"k": True})
    assert p.exists()


def test_atomic_write_json_cleans_up_tmp_file_on_success(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    p = root / "report.json"
    atomic_write_json(p, {"a": 1})
    leftovers = [
        x for x in root.iterdir() if x.name.startswith("report.json.") and x.name.endswith(".tmp")
    ]
    assert leftovers == []


# ---------------------------------------------------------------------------
# write_sha256_sidecar
# ---------------------------------------------------------------------------


def test_write_sha256_sidecar_uses_canonical_two_space_body(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    target = root / "report.json"
    target.write_bytes(b"{}\n")
    sha = compute_file_sha256(target)
    sidecar = root / "report.json.sha256"
    write_sha256_sidecar(sidecar, target_filename="report.json", sha256_hex=sha)
    body = sidecar.read_text(encoding="utf-8")
    assert body == f"{sha}  report.json\n"
    assert "\r" not in body


def test_write_sha256_sidecar_refuses_overwrite(tmp_path: Path) -> None:
    root = _tmp_normalized_root(tmp_path)
    sidecar = root / "report.json.sha256"
    write_sha256_sidecar(sidecar, target_filename="report.json", sha256_hex="0" * 64)
    with pytest.raises(GateIOError, match="refusing to overwrite existing sidecar"):
        write_sha256_sidecar(sidecar, target_filename="report.json", sha256_hex="1" * 64)


def test_write_sha256_sidecar_creates_parent_directories(tmp_path: Path) -> None:
    deep = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized" / "sub"
    sidecar = deep / "report.json.sha256"
    write_sha256_sidecar(sidecar, target_filename="report.json", sha256_hex="0" * 64)
    assert sidecar.exists()


# ---------------------------------------------------------------------------
# resolve_multiday_derived_source_artefact_paths
# ---------------------------------------------------------------------------


def _make_relative_inventory_entry(date: str) -> dict[str, object]:
    yyyy, mm, _ = date.split("-")
    parquet_rel = (
        f"microstructure/normalized/microstructure_normalized_aggtrades_v001/"
        f"BTCUSDT/{yyyy}/{mm}/BTCUSDT-aggTrades-{date}.parquet"
    )
    sidecar_rel = parquet_rel + ".sha256"
    zip_rel = (
        f"microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
        f"{yyyy}/{mm}/BTCUSDT-aggTrades-{date}.zip"
    )
    return {
        "date": date,
        "symbol": "BTCUSDT",
        "local_parquet_path": parquet_rel,
        "local_sidecar_path": sidecar_rel,
        "source_zip_path": zip_rel,
        "parquet_sha256": "b" * 64,
        "sidecar_sha256": "c" * 64,
        "source_file_sha256": "a" * 64,
        "parquet_size_bytes": 1024,
        "sidecar_size_bytes": 99,
        "event_count": 5,
        "first_transact_time_ms": 1_700_000_000_000,
        "last_transact_time_ms": 1_700_000_000_004,
        "min_agg_trade_id": 1_000,
        "max_agg_trade_id": 1_004,
    }


def _make_derived_manifest_for_resolve(
    *,
    micro_root: Path,
    inventory_dates: tuple[str, ...] = ("2024-12-01",),
) -> dict[str, object]:
    manifests_dir = micro_root / "manifests"
    return {
        "source_manifest_path": str(
            manifests_dir / "microstructure_raw_aggtrades_v001__v002.json"
        ),
        "source_acquisition_log_path": str(
            manifests_dir
            / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
        ),
        "source_gate_report_path": str(
            micro_root / "gate-reports" / "raw" / "report.json"
        ),
        "source_successor_state_path": str(
            micro_root / "successor-state" / "succ.json"
        ),
        "per_file_inventory": [
            _make_relative_inventory_entry(d) for d in inventory_dates
        ],
    }


def test_resolve_multiday_derived_source_artefact_paths_handles_relative_paths(
    tmp_path: Path,
) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / (
        "microstructure_normalized_aggtrades_v001__v002.json"
    )
    derived_path.write_text("{}", encoding="utf-8")

    derived_manifest = _make_derived_manifest_for_resolve(
        micro_root=micro_root, inventory_dates=("2024-12-01", "2025-01-15")
    )

    out = resolve_multiday_derived_source_artefact_paths(
        derived_manifest_path=derived_path,
        derived_manifest=derived_manifest,
    )
    assert isinstance(out, MultidayDerivedSourceArtefactPaths)
    assert out.derived_manifest_path == derived_path
    assert out.derived_manifest_sidecar_path == Path(str(derived_path) + ".sha256")
    assert out.raw_manifest_path.name.startswith(
        "microstructure_raw_aggtrades_v001__v002"
    )
    assert out.gate_report_path.parent.name == "raw"
    assert out.gate_report_path.parent.parent.name == "gate-reports"
    assert out.successor_state_path.parent.name == "successor-state"
    assert len(out.per_file) == 2
    first = out.per_file[0]
    assert isinstance(first, MultidayPerFileArtefactPaths)
    assert first.date == "2024-12-01"
    assert first.symbol == "BTCUSDT"
    assert first.parquet_path.name == "BTCUSDT-aggTrades-2024-12-01.parquet"
    assert first.parquet_sidecar_path.name.endswith(".parquet.sha256")
    assert first.source_zip_path.name == "BTCUSDT-aggTrades-2024-12-01.zip"
    assert first.expected_event_count == 5
    assert first.expected_first_transact_time_ms == 1_700_000_000_000
    assert first.expected_max_agg_trade_id == 1_004


def test_resolve_multiday_rejects_missing_source_manifest_path(tmp_path: Path) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    del derived_manifest["source_manifest_path"]
    with pytest.raises(GateIOError, match="source_manifest_path"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_missing_acquisition_log_path(tmp_path: Path) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    del derived_manifest["source_acquisition_log_path"]
    with pytest.raises(GateIOError, match="source_acquisition_log_path"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_missing_gate_report_path(tmp_path: Path) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    del derived_manifest["source_gate_report_path"]
    with pytest.raises(GateIOError, match="source_gate_report_path"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_missing_successor_state_path(tmp_path: Path) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    del derived_manifest["source_successor_state_path"]
    with pytest.raises(GateIOError, match="source_successor_state_path"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_empty_inventory(tmp_path: Path) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    derived_manifest["per_file_inventory"] = []
    with pytest.raises(GateIOError, match="per_file_inventory"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_non_list_inventory(tmp_path: Path) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    derived_manifest["per_file_inventory"] = "not-a-list"
    with pytest.raises(GateIOError, match="per_file_inventory"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_inventory_entry_missing_required_field(
    tmp_path: Path,
) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    bad_entry = _make_relative_inventory_entry("2024-12-02")
    del bad_entry["event_count"]
    derived_manifest["per_file_inventory"] = [bad_entry]
    with pytest.raises(GateIOError, match="event_count"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_inventory_entry_with_non_int_field(
    tmp_path: Path,
) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    bad_entry = _make_relative_inventory_entry("2024-12-02")
    bad_entry["event_count"] = "five"
    derived_manifest["per_file_inventory"] = [bad_entry]
    with pytest.raises(GateIOError, match="event_count"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )


def test_resolve_multiday_rejects_source_manifest_path_outside_microstructure(
    tmp_path: Path,
) -> None:
    micro_root = _tmp_microstructure_root(tmp_path)
    derived_path = micro_root / "manifests" / "derived.json"
    derived_path.write_text("{}", encoding="utf-8")
    derived_manifest = _make_derived_manifest_for_resolve(micro_root=micro_root)
    derived_manifest["source_manifest_path"] = str(tmp_path / "elsewhere" / "raw.json")
    with pytest.raises(GateIOError, match="source_manifest_path"):
        resolve_multiday_derived_source_artefact_paths(
            derived_manifest_path=derived_path,
            derived_manifest=derived_manifest,
        )
