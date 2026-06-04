"""Offline tests for the Phase 4bn-P normalized-layer eligibility gate.

Loads ``scripts/phase4bn_p_validate_normalized_pre_v002_gate.py`` by file path
and exercises the gate's sidecar/date/manifest validators, per-file + deep
row-level checks, predecessor integrity, fail-closed paths, and gate-report
posture — using only temp directories and small synthetic Parquet fixtures.
No network, no real production data, no sealed-test data.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

_REPO_ROOT: Path = Path(__file__).resolve().parents[3]
_SCRIPT_PATH: Path = (
    _REPO_ROOT / "scripts" / "phase4bn_p_validate_normalized_pre_v002_gate.py"
)


def _load() -> object:
    name = "phase4bn_p_validate_normalized_pre_v002_gate_under_test"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, _SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gate() -> object:
    return _load()


def _gr_root(base: Path) -> Path:
    return base / "data" / "microstructure" / "gate-reports" / "normalized"


@pytest.fixture
def short_tmp() -> Iterator[Path]:
    base = Path(tempfile.mkdtemp(prefix="p4bnp_"))
    try:
        yield base
    finally:
        shutil.rmtree(base, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Synthetic fixtures
# --------------------------------------------------------------------------- #


def _write_norm_parquet(
    gate: object, *, date: str, repo_root: Path, n: int, base_a: int,
    forbidden_col: bool = False, wrong_schema: bool = False,
) -> dict:
    """Write a synthetic normalized parquet + canonical sidecar; return inventory entry."""
    day_start = int(datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000)
    a = [base_a + i for i in range(n)]
    t = [day_start + 1000 + i * 100 for i in range(n)]
    cols = {
        "dataset_family": ["microstructure_normalized_aggtrades_v001"] * n,
        "dataset_version": ["v002"] * n,
        "source_dataset_family": ["microstructure_raw_aggtrades_v001"] * n,
        "source_dataset_version": ["v002"] * n,
        "symbol": ["BTCUSDT"] * n,
        "utc_date": [date] * n,
        "agg_trade_id": a,
        "price": [f"{100000 + i}.5" for i in range(n)],
        "quantity": ["0.001"] * n,
        "first_trade_id": [10 * x for x in a],
        "last_trade_id": [10 * x + 1 for x in a],
        "transact_time_ms": t,
        "is_buyer_maker": [i % 2 == 0 for i in range(n)],
        "source_file_sha256": ["a" * 64] * n,
        "source_manifest_sha256": ["b" * 64] * n,
        "source_gate_report_id": ["gid"] * n,
        "source_gate_report_sha256": ["c" * 64] * n,
        "row_index": list(range(n)),
        "normalization_schema_version": ["v001"] * n,
    }
    if wrong_schema:
        cols.pop("normalization_schema_version")
    if forbidden_col:
        cols["alpha_signal"] = [0] * n
    table = pa.table(cols)
    yyyy, mm, _dd = date.split("-")
    fam = gate.FAMILY_DIR_NAME
    pq_path = (
        repo_root / "data" / "microstructure" / "normalized" / fam / "BTCUSDT"
        / yyyy / mm / f"BTCUSDT-aggTrades-{date}.parquet"
    )
    pq_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, pq_path, compression="zstd")
    sha = hashlib.sha256(pq_path.read_bytes()).hexdigest()
    size = pq_path.stat().st_size
    sc_path = pq_path.with_suffix(pq_path.suffix + ".sha256")
    sc_path.write_bytes(f"{sha}  {pq_path.name}\n".encode("ascii"))
    rel = (
        f"microstructure/normalized/{fam}/BTCUSDT/{yyyy}/{mm}/"
        f"BTCUSDT-aggTrades-{date}.parquet"
    )
    return {
        "date": date, "symbol": "BTCUSDT", "local_parquet_path": rel,
        "local_sidecar_path": rel + ".sha256", "parquet_sha256": sha,
        "sidecar_sha256": hashlib.sha256(sc_path.read_bytes()).hexdigest(),
        "parquet_size_bytes": size, "sidecar_size_bytes": sc_path.stat().st_size,
        "event_count": n, "row_count": n,
        "first_transact_time_ms": t[0], "last_transact_time_ms": t[-1],
        "min_agg_trade_id": min(a), "max_agg_trade_id": max(a),
        "source_zip_sha256": "d" * 64, "source_zip_path": "microstructure/raw/x.zip",
        "status": "produced_verified",
    }


def _build_mini_segment(gate: object, repo_root: Path) -> tuple[Path, int, int]:
    """Build a 2-day synthetic normalized segment + manifest + predecessor stubs."""
    inv1 = _write_norm_parquet(gate, date="2024-03-01", repo_root=repo_root, n=5, base_a=1000)
    inv2 = _write_norm_parquet(gate, date="2024-03-02", repo_root=repo_root, n=4, base_a=2000)
    total_rows = inv1["row_count"] + inv2["row_count"]
    # Footprint = parquet + sidecar bytes (matches Phase 4bn-O definition).
    total_bytes = (
        inv1["parquet_size_bytes"] + inv1["sidecar_size_bytes"]
        + inv2["parquet_size_bytes"] + inv2["sidecar_size_bytes"]
    )
    man_dir = repo_root / "data" / "microstructure" / "manifests"
    man_dir.mkdir(parents=True, exist_ok=True)

    # Predecessor stubs.
    raw_man_rel = "data/microstructure/manifests/raw_seg.json"
    gate_rel = "data/microstructure/gate-reports/raw/raw_gate.json"
    acq_rel = "data/microstructure/manifests/raw_seg_acq.json"
    (repo_root / raw_man_rel).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / gate_rel).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / raw_man_rel).write_text('{"x":1}\n', encoding="utf-8")
    (repo_root / gate_rel).write_text(
        json.dumps({"overall_status": "pass", "gate_verdict": "RAW_X_PASS"}) + "\n",
        encoding="utf-8")
    (repo_root / acq_rel).write_text('{"y":2}\n', encoding="utf-8")
    raw_man_sha = hashlib.sha256((repo_root / raw_man_rel).read_bytes()).hexdigest()
    gate_sha = hashlib.sha256((repo_root / gate_rel).read_bytes()).hexdigest()
    acq_sha = hashlib.sha256((repo_root / acq_rel).read_bytes()).hexdigest()

    manifest = {
        "dataset_family": "microstructure_normalized_aggtrades_v001",
        "dataset_version": "v002", "version": "v002", "schema_version": "v001",
        "segment_label": "pre_v002_segment", "data_family": "aggTrades",
        "symbol_list": ["BTCUSDT"], "market": "usdm_futures",
        "dataset_category": "normalized", "phase": "4bn-O", "phase_id": "4bn-O",
        "source_phase_boundary": "4bn-K", "created_at_unix_ms": 1, "created_at_utc": "x",
        "code_commit_sha": "cd" * 20,
        "base_commit_sha": "f55b47ff94637e72ebacc40f1a133a5526afaef6",
        "capture_config_hash": "cc" * 32,
        "date_start": "2024-03-01", "date_end": "2024-03-02", "date_count": 2,
        "date_list": ["2024-03-01", "2024-03-02"], "expected_file_count": 2,
        "produced_file_count": 2, "total_event_count": total_rows,
        "total_row_count": total_rows, "per_file_inventory": [inv1, inv2],
        "total_normalized_footprint_bytes": total_bytes,
        "source_dataset_family": "microstructure_raw_aggtrades_v001",
        "source_dataset_version": "v002",
        "source_raw_segment_manifest_path": raw_man_rel,
        "source_raw_segment_manifest_sha256": raw_man_sha,
        "source_raw_gate_report_path": gate_rel,
        "source_raw_gate_report_id": "rawgate", "source_raw_gate_report_sha256": gate_sha,
        "source_raw_acquisition_log_path": acq_rel,
        "source_raw_acquisition_log_sha256": acq_sha,
        "existing_v002_normalized_reference": {
            "path": "x", "window_start": "2024-12-01", "window_end": "2025-02-28",
            "read": False, "mutated": False},
        "full_intended_envelope_start": "2024-03-01",
        "full_intended_envelope_end": "2025-02-28",
        "research_eligible": False, "eligibility_gate_status": "pending",
        "governance_labels": {"feature_computation": "forbidden", "strategy_use": "forbidden"},
        "no_successor_authorization": True, "v002_terminal_window_mode": "by_reference",
        "existing_v002_terminal_window": {
            "read": False, "overwritten": False, "redownloaded": False, "re_normalized": False},
        "sealed_test_split_touched": False,
        "existing_v002_sealed_test_split": {"touched": False},
        "test_holdout_touched": False, "test_rows_loaded": 0,
        "partitioning_rule": "<SYMBOL>/<YYYY>/<MM>/",
        "primary_key": ["symbol", "utc_date", "agg_trade_id"],
        "storage_format": "parquet_zstd", "sidecar_policy": "canonical_two_space_sha256",
        "invalid_windows": [], "budget_witnesses": {"hard_caps_crossed": False},
    }
    man_path = man_dir / gate.SEGMENT_MANIFEST_BASENAME
    man_bytes = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{man_sha}  {man_path.name}\n".encode("ascii"))
    return man_path, total_rows, total_bytes


def _patch_mini(gate: object, mp, man_path: Path, total_rows: int, total_bytes: int,
                repo_root: Path) -> None:
    man = json.loads(man_path.read_bytes())
    mp.setattr(gate, "EXPECTED_DATE_END", "2024-03-02")
    mp.setattr(gate, "EXPECTED_DATE_COUNT", 2)
    mp.setattr(gate, "EXPECTED_TOTAL_EVENT_COUNT", total_rows)
    mp.setattr(gate, "EXPECTED_TOTAL_FOOTPRINT_BYTES", total_bytes)
    mp.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_path.read_bytes()).hexdigest())
    mp.setattr(gate, "EXPECTED_RAW_SEGMENT_MANIFEST_SHA",
               man["source_raw_segment_manifest_sha256"])
    mp.setattr(gate, "EXPECTED_RAW_GATE_REPORT_SHA", man["source_raw_gate_report_sha256"])
    mp.setattr(gate, "EXPECTED_RAW_ACQUISITION_LOG_SHA",
               man["source_raw_acquisition_log_sha256"])


# --------------------------------------------------------------------------- #
# Section 1 — constants
# --------------------------------------------------------------------------- #


def test_constants(gate: object) -> None:
    assert gate.PHASE_ID == "phase-4bn-p"
    assert gate.BASE_MAIN_SHA == "3fd795ceac4fc6804015301f7f21b4ef7b22f78b"
    assert gate.FAMILY_DIR_NAME == (
        "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o")
    assert gate.EXPECTED_DATE_COUNT == 275
    assert gate.EXPECTED_TOTAL_EVENT_COUNT == 400_001_695
    assert gate.EXPECTED_TOTAL_FOOTPRINT_BYTES == 3_954_532_918
    assert gate.EXPECTED_MANIFEST_SHA == (
        "0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa")


def test_schema_19_columns(gate: object) -> None:
    assert len(gate.NORMALIZED_SCHEMA_V001) == 19


# --------------------------------------------------------------------------- #
# Section 2 — sidecar + date validators
# --------------------------------------------------------------------------- #


def test_sidecar_valid(gate: object, short_tmp: Path) -> None:
    p = short_tmp / "x.parquet.sha256"
    p.write_bytes(f"{'a' * 64}  x.parquet\n".encode("ascii"))
    ok, sha, _ = gate._validate_canonical_sidecar(p, "x.parquet")
    assert ok and sha == "a" * 64


def test_sidecar_rejects_bom_cr_extralines_badbasename(gate: object, short_tmp: Path) -> None:
    cases = {
        "bom": b"\xef\xbb\xbf" + (f"{'a' * 64}  x.parquet\n").encode(),
        "cr": (f"{'a' * 64}  x.parquet\r\n").encode(),
        "noeol": (f"{'a' * 64}  x.parquet").encode(),
        "extra": (f"{'a' * 64}  x.parquet\n{'b' * 64}  y\n").encode(),
        "onespace": (f"{'a' * 64} x.parquet\n").encode(),
        "badname": (f"{'a' * 64}  y.parquet\n").encode(),
        "badsha": (f"{'z' * 64}  x.parquet\n").encode(),
    }
    for name, body in cases.items():
        p = short_tmp / f"{name}.sha256"
        p.write_bytes(body)
        ok, _, _ = gate._validate_canonical_sidecar(p, "x.parquet")
        assert not ok, name


def test_date_in_segment(gate: object) -> None:
    assert gate._date_in_segment("2024-03-01")
    assert gate._date_in_segment("2024-11-30")
    assert not gate._date_in_segment("2024-12-01")
    assert not gate._date_in_segment("2025-02-14")
    assert not gate._date_in_segment("2024-02-29")


def test_sample_dates(gate: object) -> None:
    dl = ["2024-03-01", "2024-03-15", "2024-04-01", "2024-11-30"]
    s = gate._sample_dates(dl)
    assert "2024-03-01" in s and "2024-04-01" in s and "2024-11-30" in s


# --------------------------------------------------------------------------- #
# Section 3 — manifest contract
# --------------------------------------------------------------------------- #


def test_manifest_contract_pass(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    man = json.loads(man_path.read_bytes())
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is True
    assert all(c.status == "pass" for c in checks)


def test_manifest_contract_rejects_forbidden_field(
    gate: object, monkeypatch, short_tmp: Path
) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    man = json.loads(man_path.read_bytes())
    man["ml_authorized"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_contract_rejects_eligible_flip(
    gate: object, monkeypatch, short_tmp: Path
) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    man = json.loads(man_path.read_bytes())
    man["research_eligible"] = True
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


def test_manifest_contract_rejects_missing_field(
    gate: object, monkeypatch, short_tmp: Path
) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    man = json.loads(man_path.read_bytes())
    del man["budget_witnesses"]
    checks: list = []
    assert gate._check_manifest_contract(man, checks) is False


# --------------------------------------------------------------------------- #
# Section 4 — end-to-end gate
# --------------------------------------------------------------------------- #


def test_gate_pass(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    gr_root = _gr_root(short_tmp)
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=gr_root,
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.result_state == gate.GATE_PASS, [c for c in res.checks if c.status != "pass"]
    assert res.overall_status == "pass"
    assert res.parquet_count == 2 and res.sidecar_count == 2
    assert res.recomputed_total_rows == tr
    assert res.recomputed_total_footprint_bytes == tb
    # report + canonical sidecar.
    assert res.report_path is not None and res.report_path.exists()
    body = res.report_sidecar_path.read_bytes()
    assert body.endswith(b"\n") and b"  " in body and b"\r\n" not in body
    report = json.loads(res.report_path.read_bytes())
    assert report["segment_non_eligible"] is True
    assert report["research_eligible_after"] is False
    assert report["eligibility_gate_status_after"] == "pending"
    assert report["no_successor_authorization"] is True
    assert report["v002_terminal_window_read"] is False
    assert report["sealed_test_split_touched"] is False
    assert report["published_v002_mutated"] is False
    assert report["data_committed"] is False
    assert report["gate_result_state"] == gate.GATE_PASS


def test_gate_missing_manifest(gate: object, short_tmp: Path) -> None:
    res = gate.run_gate(manifest_path=short_tmp / "nope.json",
                        gate_reports_root=_gr_root(short_tmp), repo_root=short_tmp,
                        write_report=True, refuse_overwrite=True)
    assert res.result_state == gate.GATE_NOT_RUN_MISSING
    assert res.overall_status == "not_run"


def test_gate_fail_on_hash_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    # Corrupt one parquet (changes its real SHA vs the manifest inventory).
    fam = gate.FAMILY_DIR_NAME
    target = (short_tmp / "data" / "microstructure" / "normalized" / fam / "BTCUSDT"
              / "2024" / "03" / "BTCUSDT-aggTrades-2024-03-01.parquet")
    target.write_bytes(target.read_bytes() + b"corrupt")
    gr_root = _gr_root(short_tmp)
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=gr_root,
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.result_state == gate.GATE_FAIL
    assert res.overall_status == "fail"


def test_gate_fail_on_missing_sidecar(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    fam = gate.FAMILY_DIR_NAME
    sc = (short_tmp / "data" / "microstructure" / "normalized" / fam / "BTCUSDT"
          / "2024" / "03" / "BTCUSDT-aggTrades-2024-03-01.parquet.sha256")
    sc.unlink()
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"


def test_gate_fail_on_predecessor_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    monkeypatch.setattr(gate, "EXPECTED_RAW_SEGMENT_MANIFEST_SHA", "0" * 64)
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id == "predecessor.raw_manifest" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_schema_mismatch(gate: object, monkeypatch, short_tmp: Path) -> None:
    # Build manifest+files, then overwrite one parquet with a wrong schema and
    # repoint the inventory sha so hash passes but schema fails.
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    man = json.loads(man_path.read_bytes())
    bad = _write_norm_parquet(gate, date="2024-03-01", repo_root=short_tmp, n=5,
                              base_a=1000, wrong_schema=True)
    man["per_file_inventory"][0] = bad
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{hashlib.sha256(man_bytes).hexdigest()}  {man_path.name}\n".encode("ascii"))
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_bytes).hexdigest())
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id == "files.schema" and c.status == "fail" for c in res.checks)


def test_gate_fail_on_forbidden_column(gate: object, monkeypatch, short_tmp: Path) -> None:
    man_path, tr, tb = _build_mini_segment(gate, short_tmp)
    _patch_mini(gate, monkeypatch, man_path, tr, tb, short_tmp)
    man = json.loads(man_path.read_bytes())
    bad = _write_norm_parquet(gate, date="2024-03-01", repo_root=short_tmp, n=5,
                              base_a=1000, forbidden_col=True)
    man["per_file_inventory"][0] = bad
    man_bytes = (json.dumps(man, sort_keys=True, indent=2) + "\n").encode("utf-8")
    man_path.write_bytes(man_bytes)
    man_path.with_suffix(man_path.suffix + ".sha256").write_bytes(
        f"{hashlib.sha256(man_bytes).hexdigest()}  {man_path.name}\n".encode("ascii"))
    monkeypatch.setattr(gate, "EXPECTED_MANIFEST_SHA", hashlib.sha256(man_bytes).hexdigest())
    res = gate.run_gate(manifest_path=man_path, gate_reports_root=_gr_root(short_tmp),
                        repo_root=short_tmp, write_report=True, refuse_overwrite=True)
    assert res.overall_status == "fail"
    assert any(c.check_id in ("files.schema", "files.forbidden_columns") and c.status == "fail"
               for c in res.checks)


# --------------------------------------------------------------------------- #
# Section 5 — static no-network scan
# --------------------------------------------------------------------------- #


def test_no_forbidden_imports() -> None:
    src = _SCRIPT_PATH.read_text(encoding="utf-8")
    for forbidden in ("requests", "httpx", "aiohttp", "urllib.request", "urllib3",
                      "socket", "websockets", "binance", "dotenv"):
        pat = re.compile(rf"^\s*(?:import|from)\s+{re.escape(forbidden)}(?:\b|\.)", re.MULTILINE)
        assert not pat.search(src), forbidden


def test_no_credential_tokens() -> None:
    raw = _SCRIPT_PATH.read_text(encoding="utf-8")
    in_triple = False
    lines: list[str] = []
    for line in raw.splitlines():
        if line.strip().count('"""') + line.strip().count("'''") == 1:
            in_triple = not in_triple
            continue
        if in_triple:
            continue
        lines.append(line.split("#", 1)[0])
    code = "\n".join(lines).lower()
    for token in ("api_key", "api-key", "listenkey", ".mcp.json", "graphify", ".env"):
        assert token not in code, token
