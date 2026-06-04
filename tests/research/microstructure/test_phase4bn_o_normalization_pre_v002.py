"""Offline tests for the Phase 4bn-O pre-v002 normalization orchestrator.

These tests load ``scripts/phase4bn_o_normalize_pre_v002_aggtrades.py``
directly by file path (it lives under ``scripts/`` and is not a package) and
exercise the bounded runner's guards, per-day normalization, segment manifest
builder, budget enforcement, and static no-network posture — using only temp
directories and small synthetic raw-zip fixtures. They do NOT use the network,
do NOT read any real local ``data/`` artefact, do NOT require the 275-day raw
dataset, and do NOT read sealed-test data.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import re
import shutil
import sys
import tempfile
import zipfile
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pyarrow.parquet as pq
import pytest

_REPO_ROOT: Path = Path(__file__).resolve().parents[3]
_SCRIPT_PATH: Path = (
    _REPO_ROOT / "scripts" / "phase4bn_o_normalize_pre_v002_aggtrades.py"
)


def _load() -> object:
    module_name = "phase4bn_o_normalize_pre_v002_aggtrades_under_test"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, _SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def orch() -> object:
    return _load()


@pytest.fixture
def short_tmp() -> Iterator[Path]:
    """A short-pathed temp dir.

    The segment family directory name is long; combined with pytest's deep
    ``tmp_path`` it can exceed the Windows MAX_PATH (260) limit during the
    atomic Parquet ``.tmp`` write. A shallow ``mkdtemp`` base keeps the full
    output path comfortably under the limit. The runner itself runs from the
    short repo path ``D:\\Prometheus`` and is unaffected in production.
    """
    base = Path(tempfile.mkdtemp(prefix="p4bno_"))
    try:
        yield base
    finally:
        shutil.rmtree(base, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Synthetic fixtures
# --------------------------------------------------------------------------- #


def _build_zip_and_inventory(
    *, date: str, tmp_path: Path, n: int = 5, base_a: int = 2_000_000
) -> tuple[dict[str, object], Path, str]:
    """Build a synthetic raw zip + inventory entry under a mini micro tree."""
    day_start_ms = int(
        datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000
    )
    csv_buf = io.StringIO()
    csv_buf.write(
        "agg_trade_id,price,quantity,first_trade_id,last_trade_id,"
        "transact_time,is_buyer_maker\n"
    )
    rows = []
    for i in range(n):
        a = base_a + i
        t = day_start_ms + 1000 + i * 100
        csv_buf.write(
            f"{a},{100000 + i}.5,0.001,{10 * a},{10 * a + 1},{t},"
            f"{'true' if i % 2 == 0 else 'false'}\n"
        )
        rows.append((a, t))
    body = csv_buf.getvalue().encode("utf-8")

    yyyy, mm, _dd = date.split("-")
    zip_path = (
        tmp_path
        / "data"
        / "microstructure"
        / "raw"
        / "microstructure_raw_aggtrades_v001"
        / "BTCUSDT"
        / yyyy
        / mm
        / f"BTCUSDT-aggTrades-{date}.zip"
    )
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"BTCUSDT-aggTrades-{date}.csv", body)
    raw_sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()

    sidecar_path = zip_path.with_suffix(zip_path.suffix + ".sha256")
    sidecar_path.write_text(f"{raw_sha}  {zip_path.name}\n", encoding="ascii")

    rel = (
        f"microstructure/raw/microstructure_raw_aggtrades_v001/"
        f"BTCUSDT/{yyyy}/{mm}/BTCUSDT-aggTrades-{date}.zip"
    )
    inventory = {
        "date": date,
        "sha256": raw_sha,
        "size_bytes": zip_path.stat().st_size,
        "row_count": n,
        "first_trade_time_ms": rows[0][1],
        "last_trade_time_ms": rows[-1][1],
        "min_agg_trade_id": rows[0][0],
        "max_agg_trade_id": rows[-1][0],
        "local_zip_path": rel,
        "local_sidecar_path": rel + ".sha256",
        "status": "acquired_verified",
    }
    return inventory, zip_path, raw_sha


# --------------------------------------------------------------------------- #
# Section 1 — Locked identity / naming constants
# --------------------------------------------------------------------------- #


def test_identity_constants(orch: object) -> None:
    assert orch.PHASE_ID == "4bn-O"
    assert orch.NORMALIZED_DATASET_FAMILY == "microstructure_normalized_aggtrades_v001"
    assert orch.NORMALIZED_DATASET_VERSION == "v002"
    assert orch.SCHEMA_VERSION == "v001"
    assert orch.SEGMENT_LABEL == "pre_v002_segment"
    assert orch.SYMBOL == "BTCUSDT"
    assert orch.DATA_FAMILY == "aggTrades"


def test_window_constants(orch: object) -> None:
    assert orch.EXPECTED_DATE_START == "2024-03-01"
    assert orch.EXPECTED_DATE_END == "2024-11-30"
    assert orch.EXPECTED_DATE_COUNT == 275
    assert orch.EXPECTED_TOTAL_EVENT_COUNT == 400_001_695
    assert orch.FULL_ENVELOPE_START == "2024-03-01"
    assert orch.FULL_ENVELOPE_END == "2025-02-28"


def test_segment_naming(orch: object) -> None:
    assert (
        orch.FAMILY_DIR_NAME
        == "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o"
    )
    assert (
        orch.SEGMENT_MANIFEST_BASENAME
        == "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
    )
    assert "v003" not in orch.FAMILY_DIR_NAME
    assert orch.FAMILY_DIR_NAME != orch.PUBLISHED_V002_FAMILY_DIR_NAME


def test_expected_input_shas(orch: object) -> None:
    assert orch.EXPECTED_RAW_SEGMENT_MANIFEST_SHA == (
        "1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1"
    )
    assert orch.EXPECTED_RAW_GATE_REPORT_SHA == (
        "051bed7b3a146278e389bd8e265243d30fd541b5f36061d0573f3522920f9c24"
    )
    assert orch.EXPECTED_RAW_ACQUISITION_LOG_SHA == (
        "0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93"
    )


def test_budget_caps(orch: object) -> None:
    gib = 1024**3
    assert 100 * gib == orch.NORMALIZED_WARN_BYTES
    assert 150 * gib == orch.NORMALIZED_HARD_BYTES
    assert orch.RUNTIME_WARN_SECONDS == 4 * 3600
    assert orch.RUNTIME_HARD_SECONDS == 8 * 3600
    assert 50 * gib == orch.TEMP_WARN_BYTES
    assert 100 * gib == orch.TEMP_HARD_BYTES
    assert 250 * gib == orch.TOTAL_STACK_WARN_BYTES
    assert 300 * gib == orch.TOTAL_STACK_HARD_BYTES
    assert 500 * gib == orch.D_FREE_FLOOR_BYTES
    assert 350 * gib == orch.D_FREE_MIN_BYTES


# --------------------------------------------------------------------------- #
# Section 2 — Schema discipline
# --------------------------------------------------------------------------- #


def test_schema_19_columns(orch: object) -> None:
    assert len(orch.NORMALIZED_SCHEMA_V001) == 19
    assert tuple(orch._pa_schema().names) == orch.NORMALIZED_SCHEMA_V001


def test_no_forbidden_column_substring(orch: object) -> None:
    # Must not raise.
    orch._assert_no_forbidden_columns()


# --------------------------------------------------------------------------- #
# Section 3 — Date / symbol / family / scope guards
# --------------------------------------------------------------------------- #


def test_date_guard_accepts_segment_dates(orch: object) -> None:
    orch._assert_date_in_segment("2024-03-01")
    orch._assert_date_in_segment("2024-11-30")
    orch._assert_date_in_segment("2024-07-15")


def test_date_guard_rejects_v002_terminal(orch: object) -> None:
    for d in ("2024-12-01", "2025-01-15", "2025-02-28"):
        with pytest.raises(orch.Phase4bnOValidationError):
            orch._assert_date_in_segment(d)


def test_date_guard_rejects_before_segment(orch: object) -> None:
    with pytest.raises(orch.Phase4bnOValidationError):
        orch._assert_date_in_segment("2024-02-29")


def test_date_guard_rejects_after_segment(orch: object) -> None:
    with pytest.raises(orch.Phase4bnOValidationError):
        orch._assert_date_in_segment("2024-12-31")


def test_date_guard_rejects_sealed_test(orch: object) -> None:
    for d in ("2025-02-14", "2025-02-20", "2025-02-28"):
        with pytest.raises(orch.Phase4bnOValidationError):
            orch._assert_date_in_segment(d)


def test_symbol_guard(orch: object) -> None:
    orch._assert_symbol("BTCUSDT")
    for bad in ("ETHUSDT", "btcusdt", "SOLUSDT"):
        with pytest.raises(orch.Phase4bnOValidationError):
            orch._assert_symbol(bad)


def test_family_guard(orch: object) -> None:
    orch._assert_data_family("aggTrades")
    for bad in ("trades", "klines", "markPriceKlines", "bookTicker"):
        with pytest.raises(orch.Phase4bnOValidationError):
            orch._assert_data_family(bad)


def test_scope_token_guard(orch: object) -> None:
    orch._assert_no_forbidden_scope_tokens("BTCUSDT aggTrades binance_usdm_futures", where="x")
    for bad in (
        "ETHUSDT", "mark_price", "spot", "order_book", "tick stream",
        "cross_venue", "funding rate", "open_interest", "v003 family",
    ):
        with pytest.raises(orch.Phase4bnOValidationError):
            orch._assert_no_forbidden_scope_tokens(bad, where="x")


# --------------------------------------------------------------------------- #
# Section 4 — normalize_one_date happy path + naming + sidecar
# --------------------------------------------------------------------------- #


def test_normalize_one_date_happy_path(orch: object, short_tmp: Path) -> None:
    tmp_path = short_tmp
    inv, zip_path, raw_sha = _build_zip_and_inventory(
        date="2024-03-01", tmp_path=tmp_path, n=5
    )
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    rec = orch.normalize_one_date(
        inventory_entry=inv,
        raw_zip_path=zip_path,
        raw_zip_sha=raw_sha,
        source_manifest_sha="a" * 64,
        gate_report_id="gid",
        gate_report_sha="b" * 64,
        output_root=output_root,
        refuse_overwrite=True,
    )
    assert rec.date == "2024-03-01"
    assert rec.symbol == "BTCUSDT"
    assert rec.event_count == 5
    assert rec.status == "produced_verified"
    target = (
        output_root
        / orch.FAMILY_DIR_NAME
        / "BTCUSDT"
        / "2024"
        / "03"
        / "BTCUSDT-aggTrades-2024-03-01.parquet"
    )
    assert target.exists()
    sidecar = target.with_suffix(target.suffix + ".sha256")
    assert sidecar.exists()
    body = sidecar.read_bytes()
    assert body.endswith(b"\n")
    assert b"  " in body  # two-space separator
    assert b"\r\n" not in body  # LF only
    assert not body.startswith(b"\xef\xbb\xbf")  # no BOM
    assert body.decode("ascii") == f"{rec.parquet_sha256}  {target.name}\n"

    table = pq.read_table(target)
    assert table.num_rows == 5
    assert tuple(table.schema.names) == orch.NORMALIZED_SCHEMA_V001
    cols = {n: table.column(n).to_pylist() for n in table.schema.names}
    assert cols["dataset_family"][0] == orch.NORMALIZED_DATASET_FAMILY
    assert cols["dataset_version"][0] == "v002"
    assert cols["source_dataset_version"][0] == "v002"
    assert cols["symbol"][0] == "BTCUSDT"
    assert cols["utc_date"][0] == "2024-03-01"
    assert cols["row_index"] == [0, 1, 2, 3, 4]
    assert isinstance(cols["price"][0], str)
    assert all(isinstance(v, bool) for v in cols["is_buyer_maker"])
    # local path uses microstructure-relative prefix into the segment dir.
    assert rec.local_parquet_path.startswith(
        "microstructure/normalized/" + orch.FAMILY_DIR_NAME + "/"
    )


def test_normalize_one_date_refuse_overwrite(orch: object, short_tmp: Path) -> None:
    tmp_path = short_tmp
    inv, zip_path, raw_sha = _build_zip_and_inventory(
        date="2024-03-02", tmp_path=tmp_path, n=3
    )
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    kwargs = dict(
        inventory_entry=inv,
        raw_zip_path=zip_path,
        raw_zip_sha=raw_sha,
        source_manifest_sha="a" * 64,
        gate_report_id="g",
        gate_report_sha="b" * 64,
        output_root=output_root,
        refuse_overwrite=True,
    )
    orch.normalize_one_date(**kwargs)
    with pytest.raises(RuntimeError):
        orch.normalize_one_date(**kwargs)


def test_normalize_one_date_rejects_terminal_date(orch: object, tmp_path: Path) -> None:
    inv, zip_path, raw_sha = _build_zip_and_inventory(
        date="2024-12-01", tmp_path=tmp_path, n=3
    )
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bnOValidationError):
        orch.normalize_one_date(
            inventory_entry=inv,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )


def test_normalize_one_date_row_count_mismatch(orch: object, tmp_path: Path) -> None:
    inv, zip_path, raw_sha = _build_zip_and_inventory(
        date="2024-03-03", tmp_path=tmp_path, n=4
    )
    bad = dict(inv)
    bad["row_count"] = 99
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bnOValidationError) as ei:
        orch.normalize_one_date(
            inventory_entry=bad,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )
    assert "row count" in str(ei.value).lower()


# --------------------------------------------------------------------------- #
# Section 5 — Budget enforcement
# --------------------------------------------------------------------------- #


def test_enforce_budgets_normalized_hard_cap(orch: object) -> None:
    with pytest.raises(orch.Phase4bnOValidationError):
        orch._enforce_budgets(
            running_norm_bytes=orch.NORMALIZED_HARD_BYTES + 1,
            elapsed=1.0,
            d_free=orch.D_FREE_FLOOR_BYTES,
            temp_peak=0,
            warnings_crossed=[],
        )


def test_enforce_budgets_runtime_hard_cap(orch: object) -> None:
    with pytest.raises(orch.Phase4bnOValidationError):
        orch._enforce_budgets(
            running_norm_bytes=0,
            elapsed=orch.RUNTIME_HARD_SECONDS + 1,
            d_free=orch.D_FREE_FLOOR_BYTES,
            temp_peak=0,
            warnings_crossed=[],
        )


def test_enforce_budgets_temp_hard_cap(orch: object) -> None:
    with pytest.raises(orch.Phase4bnOValidationError):
        orch._enforce_budgets(
            running_norm_bytes=0,
            elapsed=1.0,
            d_free=orch.D_FREE_FLOOR_BYTES,
            temp_peak=orch.TEMP_HARD_BYTES + 1,
            warnings_crossed=[],
        )


def test_enforce_budgets_d_free_floor(orch: object) -> None:
    with pytest.raises(orch.Phase4bnOValidationError):
        orch._enforce_budgets(
            running_norm_bytes=0,
            elapsed=1.0,
            d_free=orch.D_FREE_MIN_BYTES - 1,
            temp_peak=0,
            warnings_crossed=[],
        )


def test_enforce_budgets_records_warnings(orch: object) -> None:
    crossed: list[str] = []
    orch._enforce_budgets(
        running_norm_bytes=orch.NORMALIZED_WARN_BYTES + 1,
        elapsed=orch.RUNTIME_WARN_SECONDS + 1,
        d_free=orch.D_FREE_FLOOR_BYTES,
        temp_peak=orch.TEMP_WARN_BYTES + 1,
        warnings_crossed=crossed,
    )
    assert "normalized_warn" in crossed
    assert "runtime_warn" in crossed
    assert "temp_warn" in crossed


def test_preflight_d_free_floor_fail_closed(orch: object, monkeypatch, tmp_path: Path) -> None:
    artefacts = orch.SourceArtefactSet(
        segment_manifest_path=tmp_path / "m.json",
        segment_manifest_sha_before="a" * 64,
        segment_manifest_parsed={"per_file_inventory": [{"row_count": 10}]},
        acquisition_log_path=tmp_path / "a.json",
        acquisition_log_sha_before="b" * 64,
        gate_report_path=tmp_path / "g.json",
        gate_report_sha_before="c" * 64,
        gate_report_id="gid",
        gate_report_code_commit_sha="x",
        raw_zip_paths=[],
        raw_zip_sha_before=[],
        raw_zip_size_before=[],
        raw_zip_sidecar_paths=[],
        raw_zip_sidecar_sha_before=[],
    )
    monkeypatch.setattr(orch, "_disk_free_bytes", lambda _p: orch.D_FREE_FLOOR_BYTES - 1)
    out = tmp_path / "data" / "microstructure" / "normalized"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bnOValidationError) as ei:
        orch.run_preflight(artefacts=artefacts, output_root=out, checks=[])
    assert "free space" in str(ei.value).lower()


def test_preflight_normalized_estimate_hard_cap(orch: object, monkeypatch, tmp_path: Path) -> None:
    artefacts = orch.SourceArtefactSet(
        segment_manifest_path=tmp_path / "m.json",
        segment_manifest_sha_before="a" * 64,
        segment_manifest_parsed={
            "per_file_inventory": [{"row_count": 100_000_000_000}]
        },
        acquisition_log_path=tmp_path / "a.json",
        acquisition_log_sha_before="b" * 64,
        gate_report_path=tmp_path / "g.json",
        gate_report_sha_before="c" * 64,
        gate_report_id="gid",
        gate_report_code_commit_sha="x",
        raw_zip_paths=[],
        raw_zip_sha_before=[],
        raw_zip_size_before=[],
        raw_zip_sidecar_paths=[],
        raw_zip_sidecar_sha_before=[],
    )
    monkeypatch.setattr(orch, "_disk_free_bytes", lambda _p: orch.D_FREE_FLOOR_BYTES * 2)
    out = tmp_path / "data" / "microstructure" / "normalized"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bnOValidationError) as ei:
        orch.run_preflight(artefacts=artefacts, output_root=out, checks=[])
    assert "hard cap" in str(ei.value).lower()


# --------------------------------------------------------------------------- #
# Section 6 — Segment manifest builder + field contract
# --------------------------------------------------------------------------- #


def _minimal_artefacts(orch: object, tmp_path: Path) -> object:
    return orch.SourceArtefactSet(
        segment_manifest_path=tmp_path / "seg.json",
        segment_manifest_sha_before="m" * 64,
        segment_manifest_parsed={"date_list": ["2024-03-01"]},
        acquisition_log_path=tmp_path / "log.json",
        acquisition_log_sha_before="l" * 64,
        gate_report_path=tmp_path / "gate.json",
        gate_report_sha_before="g" * 64,
        gate_report_id="gate-id",
        gate_report_code_commit_sha="cc" * 20,
        raw_zip_paths=[],
        raw_zip_sha_before=[],
        raw_zip_size_before=[],
        raw_zip_sidecar_paths=[],
        raw_zip_sidecar_sha_before=[],
    )


def _one_record(orch: object) -> object:
    return orch.PerDayProductionRecord(
        date="2024-03-01",
        symbol="BTCUSDT",
        local_parquet_path="microstructure/normalized/x.parquet",
        local_sidecar_path="microstructure/normalized/x.parquet.sha256",
        parquet_sha256="p" * 64,
        sidecar_sha256="s" * 64,
        parquet_size_bytes=1000,
        sidecar_size_bytes=90,
        event_count=10,
        first_transact_time_ms=1,
        last_transact_time_ms=10,
        min_agg_trade_id=1,
        max_agg_trade_id=10,
        source_zip_sha256="r" * 64,
        source_zip_path="microstructure/raw/x.zip",
        status="produced_verified",
    )


def _build_manifest(orch: object, tmp_path: Path) -> dict:
    return orch.build_segment_manifest(
        artefacts=_minimal_artefacts(orch, tmp_path),
        per_day_records=[_one_record(orch)],
        base_commit_sha="ab" * 20,
        code_commit_sha="cd" * 20,
        capture_config_hash="cc" * 32,
        created_at_unix_ms=1_700_000_000_000,
        created_at_utc="2026-06-04T00:00:00+00:00",
        total_normalized_footprint_bytes=1090,
        budget_witnesses={"hard_caps_crossed": False},
        repo_root=tmp_path,
    )


def test_segment_manifest_required_fields(orch: object, tmp_path: Path) -> None:
    m = _build_manifest(orch, tmp_path)
    assert m["dataset_family"] == orch.NORMALIZED_DATASET_FAMILY
    assert m["dataset_version"] == "v002"
    assert m["version"] == "v002"
    assert m["schema_version"] == "v001"
    assert m["segment_label"] == "pre_v002_segment"
    assert m["data_family"] == "aggTrades"
    assert m["symbol_list"] == ["BTCUSDT"]
    assert m["market"] == "usdm_futures"
    assert m["dataset_category"] == "normalized"
    assert m["phase"] == "4bn-O"
    assert m["phase_id"] == "4bn-O"
    assert m["date_start"] == "2024-03-01"
    assert m["date_end"] == "2024-11-30"
    assert m["date_count"] == 275
    assert m["full_intended_envelope_start"] == "2024-03-01"
    assert m["full_intended_envelope_end"] == "2025-02-28"
    assert m["source_dataset_family"] == "microstructure_raw_aggtrades_v001"
    assert m["source_dataset_version"] == "v002"
    assert m["primary_key"] == ["symbol", "utc_date", "agg_trade_id"]
    assert m["storage_format"] == "parquet_zstd"
    # passes the full field contract
    orch.assert_manifest_field_contract(m)


def test_segment_manifest_non_eligible_posture(orch: object, tmp_path: Path) -> None:
    m = _build_manifest(orch, tmp_path)
    assert m["research_eligible"] is False
    assert m["eligibility_gate_status"] == "pending"
    assert m["no_successor_authorization"] is True
    assert m["v002_terminal_window_mode"] == "by_reference"
    assert m["sealed_test_split_touched"] is False
    assert m["test_holdout_touched"] is False
    assert m["test_rows_loaded"] == 0
    assert m["governance_labels"]["feature_computation"] == "forbidden"
    assert m["governance_labels"]["strategy_use"] == "forbidden"


def test_segment_manifest_v002_reference_by_reference(orch: object, tmp_path: Path) -> None:
    m = _build_manifest(orch, tmp_path)
    ref = m["existing_v002_normalized_reference"]
    assert ref["read"] is False
    assert ref["mutated"] is False
    assert ref["path"].endswith("microstructure_normalized_aggtrades_v001__v002.json")
    term = m["existing_v002_terminal_window"]
    assert term["read"] is False
    assert term["overwritten"] is False
    assert term["redownloaded"] is False
    assert term["re_normalized"] is False


def test_segment_manifest_no_forbidden_fields(orch: object, tmp_path: Path) -> None:
    """No forbidden field NAME may appear (governance_labels subtree excluded)."""
    m = _build_manifest(orch, tmp_path)

    def _collect_keys(obj: object, *, skip_governance: bool) -> list[str]:
        out: list[str] = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                out.append(str(k).lower())
                if skip_governance and k == "governance_labels":
                    continue
                out.extend(_collect_keys(v, skip_governance=skip_governance))
        elif isinstance(obj, list):
            for item in obj:
                out.extend(_collect_keys(item, skip_governance=skip_governance))
        return out

    keys = _collect_keys(m, skip_governance=True)
    for forbidden in (
        "prediction", "model", "label_", "target_", "future_", "_future",
        "signal", "backtest", "alpha", "edge", "mfe", "mae", "r_multiple",
        "mark_price", "funding", "open_interest", "order_book",
        "chronological_split_policy", "diagnostics_authorized", "ml_authorized",
        "v003",
    ):
        assert all(forbidden not in k for k in keys), (
            f"forbidden field-name token {forbidden!r} in a manifest key"
        )


def test_field_contract_rejects_eligible_flip(orch: object, tmp_path: Path) -> None:
    m = _build_manifest(orch, tmp_path)
    m["research_eligible"] = True
    with pytest.raises(orch.Phase4bnOValidationError):
        orch.assert_manifest_field_contract(m)


def test_field_contract_rejects_forbidden_key(orch: object, tmp_path: Path) -> None:
    m = _build_manifest(orch, tmp_path)
    m["ml_authorized"] = True
    with pytest.raises(orch.Phase4bnOValidationError):
        orch.assert_manifest_field_contract(m)


# --------------------------------------------------------------------------- #
# Section 7 — verify_preconditions integration (2-day synthetic, monkeypatched)
# --------------------------------------------------------------------------- #


def _build_mini_repo(orch: object, tmp_path: Path) -> tuple[Path, Path, Path, int]:
    """Build a 2-date synthetic repo and return (manifest, gate, repo_root, events)."""
    inv1, _z1, _s1 = _build_zip_and_inventory(date="2024-03-01", tmp_path=tmp_path, n=5)
    inv2, _z2, _s2 = _build_zip_and_inventory(
        date="2024-03-02", tmp_path=tmp_path, n=4, base_a=2_000_010
    )
    total_events = inv1["row_count"] + inv2["row_count"]
    total_bytes = inv1["size_bytes"] + inv2["size_bytes"]
    manifests_dir = tmp_path / "data" / "microstructure" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    seg = {
        "dataset_family": "microstructure_raw_aggtrades_v001",
        "dataset_version": "v002",
        "version": "v002",
        "schema_version": "v001",
        "segment_label": "pre_v002_segment",
        "data_family": "aggTrades",
        "symbol_list": ["BTCUSDT"],
        "market": "binance_usdm_futures",
        "date_start": "2024-03-01",
        "date_end": "2024-03-02",
        "date_count": 2,
        "date_list": ["2024-03-01", "2024-03-02"],
        "expected_file_count": 2,
        "total_row_count": total_events,
        "total_size_bytes": total_bytes,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        "existing_v002_terminal_window": {"read": False},
        "existing_v002_sealed_test_split": {"touched": False},
        "per_file_inventory": [inv1, inv2],
    }
    seg_path = (
        manifests_dir
        / "microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json"
    )
    seg_path.write_text(json.dumps(seg, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    acq_path = seg_path.with_name(seg_path.stem + "_acquisition_log.json")
    acq_path.write_text(json.dumps({"phase": "4bn-J-R2"}) + "\n", encoding="utf-8")

    gate_dir = tmp_path / "data" / "microstructure" / "gate-reports" / "raw"
    gate_dir.mkdir(parents=True, exist_ok=True)
    gate_path = gate_dir / "microstructure_raw_aggtrades_v001__v002__phase-4bn-k__1__abc.json"
    gate_path.write_text(
        json.dumps(
            {
                "overall_status": "pass",
                "gate_verdict": "RAW_ARCHIVE_GATE_PASSED__X__REMAIN_PAUSED",
                "report_id": gate_path.stem,
                "code_commit_sha": "cf7dc4f7e663",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return seg_path, gate_path, tmp_path, total_events


def _patch_for_mini(
    orch: object, monkeypatch, seg_path: Path, gate_path: Path, events: int
) -> None:
    monkeypatch.setattr(orch, "EXPECTED_DATE_END", "2024-03-02")
    monkeypatch.setattr(orch, "EXPECTED_DATE_COUNT", 2)
    monkeypatch.setattr(orch, "EXPECTED_TOTAL_EVENT_COUNT", events)
    monkeypatch.setattr(
        orch, "EXPECTED_RAW_SEGMENT_MANIFEST_SHA", hashlib.sha256(seg_path.read_bytes()).hexdigest()
    )
    acq_path = seg_path.with_name(seg_path.stem + "_acquisition_log.json")
    monkeypatch.setattr(
        orch, "EXPECTED_RAW_ACQUISITION_LOG_SHA", hashlib.sha256(acq_path.read_bytes()).hexdigest()
    )
    monkeypatch.setattr(
        orch, "EXPECTED_RAW_GATE_REPORT_SHA", hashlib.sha256(gate_path.read_bytes()).hexdigest()
    )


def test_verify_preconditions_happy_path(orch: object, monkeypatch, tmp_path: Path) -> None:
    seg_path, gate_path, repo_root, events = _build_mini_repo(orch, tmp_path)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events)
    checks: list = []
    artefacts = orch.verify_preconditions(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        repo_root=repo_root,
        checks=checks,
    )
    assert len(artefacts.raw_zip_paths) == 2
    assert all(c.status in ("pass", "warn") for c in checks)


def test_verify_preconditions_sha_mismatch(orch: object, monkeypatch, tmp_path: Path) -> None:
    seg_path, gate_path, repo_root, events = _build_mini_repo(orch, tmp_path)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events)
    monkeypatch.setattr(orch, "EXPECTED_RAW_SEGMENT_MANIFEST_SHA", "0" * 64)
    with pytest.raises(orch.Phase4bnOValidationError) as ei:
        orch.verify_preconditions(
            segment_manifest_path=seg_path,
            gate_report_path=gate_path,
            repo_root=repo_root,
            checks=[],
        )
    assert "sha mismatch" in str(ei.value).lower()


def test_end_to_end_mini_run(orch: object, monkeypatch, short_tmp: Path) -> None:
    """Full run() over the 2-day synthetic repo writes a valid segment manifest."""
    tmp_path = short_tmp
    seg_path, gate_path, repo_root, events = _build_mini_repo(orch, tmp_path)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events)
    # The synthetic repo lives on whatever drive the temp dir uses; bypass the
    # 500 GiB D: preflight floor (it is exercised directly elsewhere).
    monkeypatch.setattr(orch, "_disk_free_bytes", lambda _p: orch.D_FREE_FLOOR_BYTES * 2)
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    manifests_root = tmp_path / "data" / "microstructure" / "manifests"
    output_root.mkdir(parents=True, exist_ok=True)
    result = orch.run(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        output_root=output_root,
        manifests_root=manifests_root,
        repo_root=repo_root,
        refuse_overwrite=True,
        code_commit_sha="cd" * 20,
        base_commit_sha="ab" * 20,
    )
    assert result.overall_status == "pass", result.failure_message
    assert result.produced_file_count == 2
    assert result.total_event_count == events
    assert result.output_manifest_path.name == orch.SEGMENT_MANIFEST_BASENAME
    # manifest + sidecar exist; sidecar canonical.
    assert result.output_manifest_path.exists()
    sc = result.output_manifest_sidecar_path
    assert sc.exists()
    body = sc.read_bytes()
    assert body.endswith(b"\n") and b"  " in body and b"\r\n" not in body
    # parquet outputs live under the segment dir (not the published __v002 dir).
    seg_dir = output_root / orch.FAMILY_DIR_NAME
    parquets = list(seg_dir.rglob("*.parquet"))
    assert len(parquets) == 2
    assert not (output_root / orch.PUBLISHED_V002_FAMILY_DIR_NAME).exists()
    # manifest content passes field contract.
    m = json.loads(result.output_manifest_path.read_bytes())
    orch.assert_manifest_field_contract(m)
    assert m["produced_file_count"] == 2


# --------------------------------------------------------------------------- #
# Section 8 — Static no-network / no-credential scan
# --------------------------------------------------------------------------- #


def test_no_forbidden_imports() -> None:
    src = _SCRIPT_PATH.read_text(encoding="utf-8")
    for forbidden in (
        "requests", "httpx", "aiohttp", "urllib.request", "urllib3",
        "socket", "websockets", "binance", "dotenv",
    ):
        pattern = re.compile(
            rf"^\s*(?:import|from)\s+{re.escape(forbidden)}(?:\b|\.)", re.MULTILINE
        )
        assert not pattern.search(src), f"forbidden import {forbidden!r}"


def test_no_credential_tokens() -> None:
    raw = _SCRIPT_PATH.read_text(encoding="utf-8")
    in_triple = False
    code_lines: list[str] = []
    for line in raw.splitlines():
        s = line.strip()
        if s.count('"""') + s.count("'''") == 1:
            in_triple = not in_triple
            continue
        if in_triple:
            continue
        code_lines.append(line.split("#", 1)[0])
    code = "\n".join(code_lines).lower()
    for token in ("api_key", "api-key", "listenkey", ".mcp.json", "graphify", ".env"):
        assert token not in code, f"forbidden token {token!r} in code"
