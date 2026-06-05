"""Offline tests for the Phase 4bn-S pre-v002 feature execution orchestrator.

These tests load ``scripts/phase4bn_s_compute_pre_v002_features.py`` directly by
file path (it lives under ``scripts/`` and is not a package) and exercise the
bounded runner's guards, non-eligible-source precondition enforcement, per-day
v002 feature computation, segment-manifest builder, budget enforcement, and
static no-network posture — using only temp directories and small synthetic
v002 normalized Parquet fixtures.

They do NOT use the network, do NOT read any real local ``data/`` artefact, do
NOT require the 275-day normalized dataset, and do NOT read sealed-test data.
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
from pathlib import Path

import pyarrow.parquet as pq
import pytest

# Reuse the locked Phase 4bm-H v002 normalized-Parquet fixture writer + rows.
from ._multiday_features_fixtures_v002 import (
    default_day1_rows,
    default_day2_rows,
    write_normalized_v002_parquet,
)

_REPO_ROOT: Path = Path(__file__).resolve().parents[3]
_SCRIPT_PATH: Path = (
    _REPO_ROOT / "scripts" / "phase4bn_s_compute_pre_v002_features.py"
)

_NORMALIZED_SEG_DIR = (
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o"
)


def _load() -> object:
    module_name = "phase4bn_s_compute_pre_v002_features_under_test"
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
    """A short-pathed temp dir (the segment family directory name is long)."""
    base = Path(tempfile.mkdtemp(prefix="p4bns_"))
    try:
        yield base
    finally:
        shutil.rmtree(base, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Synthetic 2-day non-eligible source fixture (normalized segment + 4bn-P gate)
# --------------------------------------------------------------------------- #


def _write_normalized_day(
    *, tmp_path: Path, date: str, rows: list[dict]
) -> tuple[dict, Path]:
    """Write a synthetic v002 normalized Parquet + sidecar; return inventory entry."""
    yyyy, mm, _dd = date.split("-")
    parquet_path = (
        tmp_path
        / "data"
        / "microstructure"
        / "normalized"
        / _NORMALIZED_SEG_DIR
        / "BTCUSDT"
        / yyyy
        / mm
        / f"BTCUSDT-aggTrades-{date}.parquet"
    )
    write_normalized_v002_parquet(parquet_path, rows, symbol="BTCUSDT", utc_date=date)
    parquet_sha = hashlib.sha256(parquet_path.read_bytes()).hexdigest()
    sidecar_path = parquet_path.with_suffix(parquet_path.suffix + ".sha256")
    sidecar_body = f"{parquet_sha}  {parquet_path.name}\n"
    sidecar_path.write_bytes(sidecar_body.encode("ascii"))  # LF only (no CRLF)
    sidecar_sha = hashlib.sha256(sidecar_body.encode("ascii")).hexdigest()

    rel = (
        f"microstructure/normalized/{_NORMALIZED_SEG_DIR}/BTCUSDT/"
        f"{yyyy}/{mm}/BTCUSDT-aggTrades-{date}.parquet"
    )
    tts = [r["transact_time_ms"] for r in rows]
    aids = [r["agg_trade_id"] for r in rows]
    entry = {
        "date": date,
        "symbol": "BTCUSDT",
        "local_parquet_path": rel,
        "local_sidecar_path": rel + ".sha256",
        "parquet_sha256": parquet_sha,
        "sidecar_sha256": sidecar_sha,
        "parquet_size_bytes": parquet_path.stat().st_size,
        "sidecar_size_bytes": len(sidecar_body.encode("ascii")),
        "event_count": len(rows),
        "first_transact_time_ms": min(tts),
        "last_transact_time_ms": max(tts),
        "min_agg_trade_id": min(aids),
        "max_agg_trade_id": max(aids),
        "source_zip_sha256": "f" * 64,
        "source_zip_path": rel.replace("normalized", "raw").replace(".parquet", ".zip"),
        "status": "produced_verified",
    }
    return entry, parquet_path


def _build_mini_source(
    orch: object, tmp_path: Path
) -> tuple[Path, Path, Path, int, int]:
    """Build a 2-date non-eligible normalized segment + 4bn-P gate report.

    Returns ``(segment_manifest_path, gate_report_path, repo_root, events, bytes)``.
    """
    rows1 = default_day1_rows("2024-03-01")
    rows2 = default_day2_rows("2024-03-02")
    inv1, _p1 = _write_normalized_day(tmp_path=tmp_path, date="2024-03-01", rows=rows1)
    inv2, _p2 = _write_normalized_day(tmp_path=tmp_path, date="2024-03-02", rows=rows2)
    total_events = inv1["event_count"] + inv2["event_count"]
    total_bytes = inv1["parquet_size_bytes"] + inv2["parquet_size_bytes"]

    manifests_dir = tmp_path / "data" / "microstructure" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    seg = {
        "dataset_family": "microstructure_normalized_aggtrades_v001",
        "dataset_version": "v002",
        "version": "v002",
        "schema_version": "v001",
        "segment_label": "pre_v002_segment",
        "data_family": "aggTrades",
        "symbol_list": ["BTCUSDT"],
        "market": "usdm_futures",
        "dataset_category": "normalized",
        "date_start": "2024-03-01",
        "date_end": "2024-03-02",
        "date_count": 2,
        "date_list": ["2024-03-01", "2024-03-02"],
        "expected_file_count": 2,
        "produced_file_count": 2,
        "total_row_count": total_events,
        "total_event_count": total_events,
        "total_normalized_footprint_bytes": total_bytes,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "v002_terminal_window_mode": "by_reference",
        "sealed_test_split_touched": False,
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        "existing_v002_terminal_window": {"read": False},
        "existing_v002_sealed_test_split": {"touched": False},
        "per_file_inventory": [inv1, inv2],
    }
    seg_path = manifests_dir / (
        "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
    )
    seg_body = json.dumps(seg, sort_keys=True, indent=2) + "\n"
    seg_path.write_text(seg_body, encoding="utf-8")
    seg_sha = hashlib.sha256(seg_path.read_bytes()).hexdigest()
    sidecar_body = f"{seg_sha}  {seg_path.name}\n"
    seg_path.with_suffix(seg_path.suffix + ".sha256").write_bytes(
        sidecar_body.encode("ascii")
    )

    gate_dir = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    gate_dir.mkdir(parents=True, exist_ok=True)
    gate = {
        "overall_status": "pass",
        "gate_verdict": "NORMALIZED_LAYER_GATE_PASS",
        "gate_result_state": orch.REQUIRED_GATE_RESULT_STATE,
        "checks": [{"check_id": f"c{i}", "status": "pass"} for i in range(25)],
        "segment_non_eligible": True,
        "research_eligible_after": False,
        "eligibility_gate_status_after": "pending",
        "no_successor_authorization": True,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "published_v002_mutated": False,
        "data_committed": False,
        "input_normalized_manifest_sha256": seg_sha,
    }
    gate_path = gate_dir / (
        "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__"
        "phase-4bn-p__1__abc.json"
    )
    gate_path.write_text(json.dumps(gate, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return seg_path, gate_path, tmp_path, total_events, total_bytes


def _patch_for_mini(
    orch: object, monkeypatch, seg_path: Path, gate_path: Path, events: int, total_bytes: int
) -> None:
    monkeypatch.setattr(orch, "EXPECTED_DATE_END", "2024-03-02")
    monkeypatch.setattr(orch, "EXPECTED_DATE_COUNT", 2)
    monkeypatch.setattr(orch, "EXPECTED_TOTAL_EVENT_COUNT", events)
    monkeypatch.setattr(orch, "EXPECTED_TOTAL_NORMALIZED_FOOTPRINT_BYTES", total_bytes)
    monkeypatch.setattr(
        orch,
        "EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA",
        hashlib.sha256(seg_path.read_bytes()).hexdigest(),
    )
    sidecar = seg_path.with_suffix(seg_path.suffix + ".sha256")
    monkeypatch.setattr(
        orch,
        "EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA",
        hashlib.sha256(sidecar.read_bytes()).hexdigest(),
    )
    monkeypatch.setattr(
        orch,
        "EXPECTED_NORMALIZED_GATE_REPORT_SHA",
        hashlib.sha256(gate_path.read_bytes()).hexdigest(),
    )
    # Bypass the 500 GiB D: preflight floor (exercised directly elsewhere).
    monkeypatch.setattr(orch, "_disk_free_bytes", lambda _p: orch.D_FREE_FLOOR_BYTES * 2)


# --------------------------------------------------------------------------- #
# Section 1 — Locked identity / naming / budget constants
# --------------------------------------------------------------------------- #


def test_identity_constants(orch: object) -> None:
    assert orch.PHASE_ID == "4bn-S"
    assert orch.PHASE_ID_FULL == "phase-4bn-s"
    assert orch.FEATURE_FAMILY_ID == "microstructure_features_aggtrades_v001"
    assert orch.FEATURE_DATASET_VERSION == "v002"
    assert orch.VERSION == "v002"
    assert orch.FEATURE_SCHEMA_VERSION == "v001"
    assert orch.SEGMENT_LABEL == "pre_v002_segment"
    assert orch.DATA_FAMILY == "aggTrades"
    assert orch.MARKET == "usdm_futures"
    assert orch.DATASET_CATEGORY == "features"
    assert orch.SYMBOL == "BTCUSDT"


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
        == "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s"
    )
    assert (
        orch.SEGMENT_MANIFEST_BASENAME
        == "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json"
    )
    assert "v003" not in orch.FAMILY_DIR_NAME
    assert orch.FAMILY_DIR_NAME != orch.PUBLISHED_V002_FEATURE_DIR_NAME
    orch._assert_segment_naming()


def test_expected_input_shas(orch: object) -> None:
    assert orch.EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA == (
        "0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa"
    )
    assert orch.EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA == (
        "5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402"
    )
    assert orch.EXPECTED_NORMALIZED_GATE_REPORT_SHA == (
        "3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134"
    )
    assert orch.BASE_COMMIT_SHA_4BN_R_FINAL == (
        "40f0b3e54392e0e108b8664beedf25169a2d9778"
    )


def test_budget_caps(orch: object) -> None:
    gib = 1024**3
    assert 50 * gib == orch.FEATURE_WARN_BYTES
    assert 100 * gib == orch.FEATURE_HARD_BYTES
    assert orch.RUNTIME_WARN_SECONDS == 4 * 3600
    assert orch.RUNTIME_HARD_SECONDS == 8 * 3600
    assert 50 * gib == orch.TEMP_WARN_BYTES
    assert 100 * gib == orch.TEMP_HARD_BYTES
    assert 250 * gib == orch.TOTAL_STACK_WARN_BYTES
    assert 300 * gib == orch.TOTAL_STACK_HARD_BYTES
    assert 500 * gib == orch.D_FREE_FLOOR_BYTES
    assert 350 * gib == orch.D_FREE_MIN_BYTES


def test_locked_feature_schema(orch: object) -> None:
    assert len(orch.FEATURE_SCHEMA_V002) == 62
    assert len(orch.LINEAGE_COLUMNS_V002) == 17
    assert len(orch.FEATURE_NAMES_V002) == 45
    assert orch.FEATURE_SCHEMA_VERSION_V002 == "v001"
    # Forbidden-substring column guard passes for the locked schema.
    orch.assert_no_forbidden_substrings_v002(orch.FEATURE_SCHEMA_V002)


# --------------------------------------------------------------------------- #
# Section 2 — Date / symbol / family / scope-token guards
# --------------------------------------------------------------------------- #


def test_date_guard_accepts_segment_dates(orch: object) -> None:
    orch._assert_date_in_segment("2024-03-01")
    orch._assert_date_in_segment("2024-11-30")
    orch._assert_date_in_segment("2024-07-15")


def test_date_guard_rejects_terminal_window(orch: object) -> None:
    for bad in ("2024-12-01", "2025-01-15", "2025-02-28"):
        with pytest.raises(orch.Phase4bnSValidationError):
            orch._assert_date_in_segment(bad)


def test_date_guard_rejects_before_segment(orch: object) -> None:
    for bad in ("2024-02-29", "2023-12-31", "2024-02-01"):
        with pytest.raises(orch.Phase4bnSValidationError):
            orch._assert_date_in_segment(bad)


def test_date_guard_rejects_after_segment(orch: object, monkeypatch) -> None:
    # Exercise the explicit `date > EXPECTED_DATE_END` branch with an earlier end.
    monkeypatch.setattr(orch, "EXPECTED_DATE_END", "2024-06-30")
    with pytest.raises(orch.Phase4bnSValidationError):
        orch._assert_date_in_segment("2024-07-01")


def test_date_guard_rejects_malformed(orch: object) -> None:
    with pytest.raises(orch.Phase4bnSValidationError):
        orch._assert_date_in_segment("2024-13-40")


def test_date_guard_rejects_sealed_test(orch: object) -> None:
    for bad in ("2025-02-14", "2025-02-20", "2025-02-28"):
        with pytest.raises(orch.Phase4bnSValidationError):
            orch._assert_date_in_segment(bad)


def test_symbol_guard(orch: object) -> None:
    orch._assert_symbol("BTCUSDT")
    for bad in ("ETHUSDT", "btcusdt", "SOLUSDT", ""):
        with pytest.raises(orch.Phase4bnSValidationError):
            orch._assert_symbol(bad)


def test_family_guard(orch: object) -> None:
    orch._assert_data_family("aggTrades")
    for bad in ("trades", "klines", "markPrice", "bookTicker"):
        with pytest.raises(orch.Phase4bnSValidationError):
            orch._assert_data_family(bad)


def test_scope_token_guard(orch: object) -> None:
    orch._assert_no_forbidden_scope_tokens("BTCUSDT aggTrades usdm_futures", where="x")
    for bad in (
        "ETHUSDT",
        "mark-price",
        "mark_price",
        "spot",
        "order-book",
        "order_book",
        "tick",
        "cross-venue",
        "funding",
        "open_interest",
        "v003",
    ):
        with pytest.raises(orch.Phase4bnSValidationError):
            orch._assert_no_forbidden_scope_tokens(bad, where="x")


def test_feature_parquet_path_naming(orch: object, short_tmp: Path) -> None:
    features_root = short_tmp / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True, exist_ok=True)
    out = orch._derive_feature_parquet_path(
        features_root=features_root, symbol="BTCUSDT", utc_date="2024-05-09"
    )
    assert orch.FAMILY_DIR_NAME in out.as_posix()
    assert out.name == "BTCUSDT-features-aggtrades-2024-05-09.parquet"
    assert out.parent.as_posix().endswith("BTCUSDT/2024/05")
    # Must not resolve under the published __v002 feature dir.
    assert f"{orch.PUBLISHED_V002_FEATURE_DIR_NAME}/" not in out.as_posix()


# --------------------------------------------------------------------------- #
# Section 3 — Preflight fail-closed behaviour
# --------------------------------------------------------------------------- #


def test_preflight_d_free_floor_fail_closed(orch: object, monkeypatch, short_tmp: Path) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    monkeypatch.setattr(orch, "_disk_free_bytes", lambda _p: orch.D_FREE_FLOOR_BYTES - 1)
    checks: list = []
    artefacts = orch.verify_preconditions(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        repo_root=repo_root,
        checks=checks,
    )
    features_root = short_tmp / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.run_preflight(artefacts=artefacts, features_root=features_root, checks=[])
    assert "below preflight floor" in str(ei.value).lower()


def test_preflight_feature_hard_cap_fail_closed(orch: object, monkeypatch, short_tmp: Path) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    # Inflate per-event estimate so the feature footprint blows the 100 GiB cap.
    monkeypatch.setattr(orch, "PREFLIGHT_BYTES_PER_EVENT", 20 * 1024**3)
    checks: list = []
    artefacts = orch.verify_preconditions(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        repo_root=repo_root,
        checks=checks,
    )
    features_root = short_tmp / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.run_preflight(artefacts=artefacts, features_root=features_root, checks=[])
    assert "hard cap" in str(ei.value).lower()


def test_preflight_temp_hard_cap_fail_closed(orch: object, monkeypatch, short_tmp: Path) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    checks: list = []
    artefacts = orch.verify_preconditions(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        repo_root=repo_root,
        checks=checks,
    )
    # Shrink the temp hard cap below a single day's estimate.
    monkeypatch.setattr(orch, "PREFLIGHT_BYTES_PER_EVENT", 1024)
    monkeypatch.setattr(orch, "TEMP_HARD_BYTES", 1)
    features_root = short_tmp / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.run_preflight(artefacts=artefacts, features_root=features_root, checks=[])
    assert "temp" in str(ei.value).lower()


# --------------------------------------------------------------------------- #
# Section 4 — Non-eligible-source precondition enforcement
# --------------------------------------------------------------------------- #


def test_preconditions_happy_path(orch: object, monkeypatch, short_tmp: Path) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    checks: list = []
    artefacts = orch.verify_preconditions(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        repo_root=repo_root,
        checks=checks,
    )
    assert len(artefacts.per_day_sources) == 2
    assert all(c.status in ("pass", "warn") for c in checks)


def test_preconditions_manifest_sha_mismatch(orch: object, monkeypatch, short_tmp: Path) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    monkeypatch.setattr(orch, "EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA", "0" * 64)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.verify_preconditions(
            segment_manifest_path=seg_path,
            gate_report_path=gate_path,
            repo_root=repo_root,
            checks=[],
        )
    assert "sha mismatch" in str(ei.value).lower()


def test_preconditions_gate_not_pass(orch: object, monkeypatch, short_tmp: Path) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    gate = json.loads(gate_path.read_bytes())
    gate["overall_status"] = "fail"
    gate_path.write_text(json.dumps(gate, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.verify_preconditions(
            segment_manifest_path=seg_path,
            gate_report_path=gate_path,
            repo_root=repo_root,
            checks=[],
        )
    assert "overall_status" in str(ei.value).lower()


def test_preconditions_gate_not_25_pass(orch: object, monkeypatch, short_tmp: Path) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    gate = json.loads(gate_path.read_bytes())
    gate["checks"] = gate["checks"][:24]  # only 24 PASS checks
    gate_path.write_text(json.dumps(gate, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.verify_preconditions(
            segment_manifest_path=seg_path,
            gate_report_path=gate_path,
            repo_root=repo_root,
            checks=[],
        )
    assert "25/25" in str(ei.value) or "25" in str(ei.value)


def test_preconditions_source_research_eligible_rejected(
    orch: object, monkeypatch, short_tmp: Path
) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    seg = json.loads(seg_path.read_bytes())
    seg["research_eligible"] = True  # must remain False
    seg_body = json.dumps(seg, sort_keys=True, indent=2) + "\n"
    seg_path.write_text(seg_body, encoding="utf-8")
    seg_sha = hashlib.sha256(seg_path.read_bytes()).hexdigest()
    seg_path.with_suffix(seg_path.suffix + ".sha256").write_bytes(
        f"{seg_sha}  {seg_path.name}\n".encode("ascii")
    )
    # Re-link gate report to the mutated manifest SHA.
    gate = json.loads(gate_path.read_bytes())
    gate["input_normalized_manifest_sha256"] = seg_sha
    gate_path.write_text(json.dumps(gate, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.verify_preconditions(
            segment_manifest_path=seg_path,
            gate_report_path=gate_path,
            repo_root=repo_root,
            checks=[],
        )
    assert "research_eligible" in str(ei.value).lower()


def test_preconditions_source_not_pending_rejected(
    orch: object, monkeypatch, short_tmp: Path
) -> None:
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, short_tmp)
    seg = json.loads(seg_path.read_bytes())
    seg["eligibility_gate_status"] = "eligible"  # must remain 'pending'
    seg_path.write_text(json.dumps(seg, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    seg_sha = hashlib.sha256(seg_path.read_bytes()).hexdigest()
    seg_path.with_suffix(seg_path.suffix + ".sha256").write_bytes(
        f"{seg_sha}  {seg_path.name}\n".encode("ascii")
    )
    gate = json.loads(gate_path.read_bytes())
    gate["input_normalized_manifest_sha256"] = seg_sha
    gate_path.write_text(json.dumps(gate, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.verify_preconditions(
            segment_manifest_path=seg_path,
            gate_report_path=gate_path,
            repo_root=repo_root,
            checks=[],
        )
    assert "pending" in str(ei.value).lower()


# --------------------------------------------------------------------------- #
# Section 5 — End-to-end mini run (2-day synthetic segment)
# --------------------------------------------------------------------------- #


def _run_mini(orch: object, monkeypatch, tmp_path: Path):
    seg_path, gate_path, repo_root, events, total_bytes = _build_mini_source(orch, tmp_path)
    _patch_for_mini(orch, monkeypatch, seg_path, gate_path, events, total_bytes)
    monkeypatch.setattr(orch, "EXPECTED_TOTAL_EVENT_COUNT", events)
    features_root = tmp_path / "data" / "microstructure" / "features"
    manifests_root = tmp_path / "data" / "microstructure" / "manifests"
    features_root.mkdir(parents=True, exist_ok=True)
    result = orch.run(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        features_root=features_root,
        manifests_root=manifests_root,
        repo_root=repo_root,
        refuse_overwrite=True,
        code_commit_sha="cd" * 20,
        base_commit_sha=orch.BASE_COMMIT_SHA_4BN_R_FINAL,
    )
    return result, features_root, manifests_root, events


def test_end_to_end_mini_run(orch: object, monkeypatch, short_tmp: Path) -> None:
    result, features_root, _manifests_root, events = _run_mini(orch, monkeypatch, short_tmp)
    assert result.overall_status == "pass", result.failure_message
    assert result.produced_file_count == 2
    assert result.total_feature_row_count == events
    assert result.result_state == (
        "FEATURE_EXECUTION_SUCCEEDED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
    )

    # 2 feature parquets + 2 canonical sidecars under the segment dir.
    seg_dir = features_root / orch.FAMILY_DIR_NAME
    parquets = sorted(seg_dir.rglob("*.parquet"))
    sidecars = sorted(seg_dir.rglob("*.parquet.sha256"))
    assert len(parquets) == 2
    assert len(sidecars) == 2
    # Published __v002 feature dir was NOT written.
    assert not (features_root / orch.PUBLISHED_V002_FEATURE_DIR_NAME).exists()

    # Each feature parquet has exactly the 62-column FEATURE_SCHEMA_V002.
    for p in parquets:
        schema = pq.read_schema(p)
        assert tuple(schema.names) == orch.FEATURE_SCHEMA_V002
    # Canonical sidecar format: "<64hex>  <basename>\n", LF only, no BOM.
    for sc in sidecars:
        body = sc.read_bytes()
        assert body.endswith(b"\n") and b"\r\n" not in body and not body.startswith(b"\xef")
        text = body.decode("ascii")
        digest, _, name = text.rstrip("\n").partition("  ")
        assert len(digest) == 64 and name.endswith(".parquet")


def test_end_to_end_manifest_contract_and_posture(
    orch: object, monkeypatch, short_tmp: Path
) -> None:
    result, _features_root, manifests_root, events = _run_mini(orch, monkeypatch, short_tmp)
    assert result.overall_status == "pass", result.failure_message
    manifest_path = manifests_root / orch.SEGMENT_MANIFEST_BASENAME
    assert manifest_path.exists()
    m = json.loads(manifest_path.read_bytes())
    orch.assert_manifest_field_contract(m)

    # Versioning convention (Phase 4bn-R carried forward).
    assert m["dataset_family"] == "microstructure_features_aggtrades_v001"
    assert m["dataset_version"] == "v002" and m["version"] == "v002"
    assert m["feature_schema_version"] == "v001"
    assert m["segment_label"] == "pre_v002_segment"
    assert m["feature_column_count"] == 62
    assert m["lineage_column_count"] == 17
    assert m["feature_quality_column_count"] == 45
    assert tuple(m["feature_column_names"]) == orch.FEATURE_SCHEMA_V002
    assert m["base_commit_sha"] == orch.BASE_COMMIT_SHA_4BN_R_FINAL

    # Non-eligible posture (Phase 4bn-R precondition carried forward).
    assert m["research_eligible"] is False
    assert m["eligibility_gate_status"] == "pending"
    assert m["no_successor_authorization"] is True
    assert m["source_eligibility_posture"] == "non_eligible_gate_passed_pending"
    assert all(m["boundary_confirmations"].values())
    assert m["boundary_confirmations"]["no_future_lookahead"] is True
    assert (
        m["boundary_confirmations"]["phase_4aw_flip_research_eligible_invariant_preserved"]
        is True
    )
    assert not any(m["non_authorization_flags"].values())
    assert m["non_authorization_flags"]["successor_authorization_after"] is False

    # By-reference posture for published v002 + terminal + sealed test.
    assert m["existing_v002_feature_reference"]["read"] is False
    assert m["existing_v002_feature_reference"]["mutated"] is False
    assert m["existing_v002_terminal_window"]["read"] is False
    assert m["existing_v002_terminal_window"]["normalized_dates_read"] is False
    assert m["sealed_test_split_touched"] is False
    assert m["test_rows_loaded"] == 0
    assert m["v002_terminal_window_mode"] == "by_reference"

    # Source linkage records the non-eligible normalized segment + 4bn-P gate.
    assert m["source_dataset_family"] == "microstructure_normalized_aggtrades_v001"
    assert "source_normalized_layer_gate_report_sha256" in m
    assert "source_normalized_segment_manifest_sha256" in m
    # No Stage-3 successor-state field is present in the manifest.
    assert "source_successor_state_path" not in m
    assert "source_phase_4bm_f_successor_state_sha256" not in m

    # Per-file inventory completeness.
    assert len(m["per_file_inventory"]) == 2
    for e in m["per_file_inventory"]:
        for key in (
            "feature_parquet_path",
            "feature_parquet_sha256",
            "feature_sidecar_path",
            "feature_sidecar_sha256",
            "paired_source_normalized_parquet_path",
            "paired_source_normalized_parquet_sha256",
            "first_transact_time_ms",
            "min_agg_trade_id",
            "max_agg_trade_id",
            "status",
        ):
            assert key in e


def test_manifest_has_no_forbidden_fields(orch: object, monkeypatch, short_tmp: Path) -> None:
    result, _features_root, manifests_root, _events = _run_mini(orch, monkeypatch, short_tmp)
    m = json.loads((manifests_root / orch.SEGMENT_MANIFEST_BASENAME).read_bytes())

    def _keys(obj, skip):
        out = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                out.append(str(k))
                if k in skip:
                    continue
                out.extend(_keys(v, skip))
        elif isinstance(obj, list):
            for it in obj:
                out.extend(_keys(it, skip))
        return out

    keys = _keys(m, orch._DECLARATION_SUBTREES)
    for forbidden in (
        "label_",
        "target_",
        "future_",
        "_score",
        "model",
        "prediction",
        "signal",
        "pnl",
        "barrier",
        "mark_price",
        "funding",
        "v003",
        "chronological_split_policy",
    ):
        assert all(forbidden not in k.lower() for k in keys), forbidden


def test_manifest_forbidden_field_scan_rejects_injection(
    orch: object, monkeypatch, short_tmp: Path
) -> None:
    """The field-name contract rejects a forbidden key injected into a valid manifest."""
    result, _features_root, manifests_root, _events = _run_mini(orch, monkeypatch, short_tmp)
    m = json.loads((manifests_root / orch.SEGMENT_MANIFEST_BASENAME).read_bytes())
    # Sanity: the genuine manifest passes the contract.
    orch.assert_manifest_field_contract(m)
    # Injecting a forbidden top-level key must now fail closed.
    m["label_horizon_ms"] = 1000
    with pytest.raises(orch.Phase4bnSValidationError) as ei:
        orch.assert_manifest_field_contract(m)
    assert "forbidden manifest field substring" in str(ei.value).lower()


def test_refuse_overwrite(orch: object, monkeypatch, short_tmp: Path) -> None:
    result, features_root, manifests_root, _events = _run_mini(orch, monkeypatch, short_tmp)
    assert result.overall_status == "pass"
    seg_path = (
        short_tmp
        / "data"
        / "microstructure"
        / "manifests"
        / "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
    )
    gate_path = next(
        (short_tmp / "data" / "microstructure" / "gate-reports" / "normalized").glob("*.json")
    )
    # A second run must fail closed (refuse-to-overwrite) without mutating outputs.
    result2 = orch.run(
        segment_manifest_path=seg_path,
        gate_report_path=gate_path,
        features_root=features_root,
        manifests_root=manifests_root,
        repo_root=short_tmp,
        refuse_overwrite=True,
        code_commit_sha="cd" * 20,
        base_commit_sha=orch.BASE_COMMIT_SHA_4BN_R_FINAL,
    )
    assert result2.overall_status == "fail_closed"
    assert "overwrite" in (result2.failure_message or "").lower()


# --------------------------------------------------------------------------- #
# Section 6 — Static no-network / no-credential scan
# --------------------------------------------------------------------------- #


def test_no_forbidden_imports() -> None:
    src = _SCRIPT_PATH.read_text(encoding="utf-8")
    for forbidden in (
        "requests",
        "httpx",
        "aiohttp",
        "urllib.request",
        "urllib3",
        "socket",
        "websockets",
        "binance",
        "dotenv",
        "subprocess",
    ):
        pattern = re.compile(
            rf"^\s*(?:import|from)\s+{re.escape(forbidden)}(?:\b|\.)", re.MULTILINE
        )
        assert not pattern.search(src), f"forbidden import {forbidden!r}"


def test_no_credential_or_network_tokens() -> None:
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
    for token in ("api_key", "api-key", "listenkey", ".mcp.json", "graphify", ".env", "http://", "https://"):
        assert token not in code, f"forbidden token {token!r} in code"
