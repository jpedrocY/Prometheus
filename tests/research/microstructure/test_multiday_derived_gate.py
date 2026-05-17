"""Phase 4bm-D orchestrator end-to-end tests.

These tests build a fully-materialized canonical 5x5 PASS-shape fixture
entirely under ``tmp_path`` (5 contiguous UTC dates, 5 events per
date), exercise the real :func:`run_multiday_derived_aggtrades_gate`
orchestrator end-to-end, and verify the multi-day gate verdict,
boundary confirmations, hard invariants, on-disk report layout, and
refuse-overwrite discipline.

The fixture uses parser-format ``per_file_inventory`` keys
(``local_parquet_path`` / ``local_sidecar_path`` / ``source_zip_path``
/ ``parquet_sha256`` / ``sidecar_sha256`` / ``source_file_sha256`` /
``parquet_size_bytes`` / ``sidecar_size_bytes`` / ``event_count`` /
``first_transact_time_ms`` / ``last_transact_time_ms`` /
``min_agg_trade_id`` / ``max_agg_trade_id``) so the orchestrator's
I/O resolver consumes the manifest without translation.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import multiday_derived_gate as mdg
from prometheus.research.microstructure import multiday_derived_gate_checks as mdc
from prometheus.research.microstructure.multiday_derived_gate import (
    _BOUNDARY_KEYS,
    MultidayDerivedAggTradesGateInput,
    MultidayDerivedAggTradesGateInputError,
    MultidayDerivedAggTradesGateResult,
    run_multiday_derived_aggtrades_gate,
)
from prometheus.research.microstructure.multiday_derived_gate_io import GateIOError
from prometheus.research.microstructure.multiday_derived_gate_report import (
    GATE_VERDICT_FAIL,
    GATE_VERDICT_PASS,
)

_DATES: tuple[str, ...] = (
    "2024-12-01",
    "2024-12-02",
    "2024-12-03",
    "2024-12-04",
    "2024-12-05",
)
_EVENTS_PER_DATE = 5
_TOTAL_EVENTS = _EVENTS_PER_DATE * len(_DATES)
_CODE_COMMIT = "0123456789ab" + "0" * 28  # 40 hex chars


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _build_sample_table(
    *,
    date: str,
    first_t: int,
    min_id: int,
    n: int,
    zip_sha: str,
    raw_manifest_sha: str,
    gate_report_sha: str,
    gate_report_id: str,
) -> pa.Table:
    """Build one canonical sample Parquet table for a single date.

    Mirrors the schema and per-row lineage assertions enforced by
    ``check_4bm_d_13_22`` through ``check_4bm_d_13_37``.
    """
    row_indices = list(range(n))
    columns: dict[str, list[Any]] = {
        "dataset_family": [mdc.CANONICAL_DATASET_FAMILY] * n,
        "dataset_version": [mdc.CANONICAL_DATASET_VERSION] * n,
        "source_dataset_family": [mdc.CANONICAL_SOURCE_DATASET_FAMILY] * n,
        "source_dataset_version": [mdc.CANONICAL_SOURCE_DATASET_VERSION] * n,
        "symbol": [mdc.CANONICAL_SYMBOL] * n,
        "utc_date": [date] * n,
        "agg_trade_id": [min_id + i for i in row_indices],
        "price": ["100000.0"] * n,
        "quantity": ["0.001"] * n,
        "first_trade_id": [10_000 + i * 10 for i in row_indices],
        "last_trade_id": [10_005 + i * 10 for i in row_indices],
        "transact_time_ms": [first_t + i for i in row_indices],
        "is_buyer_maker": [True] * n,
        "source_file_sha256": [zip_sha] * n,
        "source_manifest_sha256": [raw_manifest_sha] * n,
        "source_gate_report_id": [gate_report_id] * n,
        "source_gate_report_sha256": [gate_report_sha] * n,
        "row_index": row_indices,
        "normalization_schema_version": [
            mdc.CANONICAL_NORMALIZATION_SCHEMA_VERSION
        ] * n,
    }
    schema = pa.schema(
        [
            pa.field("dataset_family", pa.string()),
            pa.field("dataset_version", pa.string()),
            pa.field("source_dataset_family", pa.string()),
            pa.field("source_dataset_version", pa.string()),
            pa.field("symbol", pa.string()),
            pa.field("utc_date", pa.string()),
            pa.field("agg_trade_id", pa.int64()),
            pa.field("price", pa.string()),
            pa.field("quantity", pa.string()),
            pa.field("first_trade_id", pa.int64()),
            pa.field("last_trade_id", pa.int64()),
            pa.field("transact_time_ms", pa.int64()),
            pa.field("is_buyer_maker", pa.bool_()),
            pa.field("source_file_sha256", pa.string()),
            pa.field("source_manifest_sha256", pa.string()),
            pa.field("source_gate_report_id", pa.string()),
            pa.field("source_gate_report_sha256", pa.string()),
            pa.field("row_index", pa.int64()),
            pa.field("normalization_schema_version", pa.string()),
        ]
    )
    return pa.Table.from_pydict(columns, schema=schema)


@dataclass
class OrchestratorFixture:
    """Handle to a fully-materialized PASS-shape orchestrator fixture."""

    tmp_path: Path
    micro_root: Path
    derived_manifest_path: Path
    output_root: Path
    qa_stub: Path
    closeout_stub: Path
    merge_closeout_stub: Path
    raw_manifest_path: Path
    raw_manifest_sha: str
    derived_manifest_sha: str


def _setup_passing_orchestrator(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> OrchestratorFixture:
    """Build a fully-materialized canonical PASS-shape orchestrator fixture."""
    monkeypatch.chdir(tmp_path)

    micro_root = tmp_path / "data" / "microstructure"
    (micro_root / "manifests").mkdir(parents=True, exist_ok=True)
    (micro_root / "gate-reports" / "raw").mkdir(parents=True, exist_ok=True)
    (micro_root / "gate-reports" / "normalized").mkdir(parents=True, exist_ok=True)
    (micro_root / "successor-state").mkdir(parents=True, exist_ok=True)

    # Phase 4bm-C stub files live outside the microstructure namespace
    # — these are docs/process artefacts, not data artefacts.
    phase_4bmc_dir = tmp_path / "phase_4bmc_stubs"
    phase_4bmc_dir.mkdir()
    qa_stub = phase_4bmc_dir / "qa_memo.md"
    closeout_stub = phase_4bmc_dir / "closeout.md"
    merge_closeout_stub = phase_4bmc_dir / "merge_closeout.md"
    qa_stub.write_text(
        "Verdict: All 28 predeclared QA questions return PASS.\n",
        encoding="utf-8",
    )
    closeout_stub.write_text("Phase 4bm-C closeout stub.\n", encoding="utf-8")
    merge_closeout_stub.write_text(
        "Phase 4bm-C merge-closeout stub.\n", encoding="utf-8"
    )

    # Date / sample constants need patching in BOTH the checks module
    # (whose check functions read them) and the orchestrator module
    # (which imports them by-name at module load).
    monkeypatch.setattr(mdc, "EXPECTED_TOTAL_EVENT_COUNT", _TOTAL_EVENTS)
    monkeypatch.setattr(mdc, "EXPECTED_DATE_COUNT", len(_DATES))
    monkeypatch.setattr(mdc, "CANONICAL_DATE_START", _DATES[0])
    monkeypatch.setattr(mdc, "CANONICAL_DATE_END", _DATES[-1])
    monkeypatch.setattr(mdc, "SAMPLE_DATES", _DATES)
    monkeypatch.setattr(mdc, "PHASE_4BMC_QA_PATH", qa_stub)
    monkeypatch.setattr(mdc, "PHASE_4BMC_CLOSEOUT_PATH", closeout_stub)
    monkeypatch.setattr(mdc, "PHASE_4BMC_MERGE_CLOSEOUT_PATH", merge_closeout_stub)
    monkeypatch.setattr(mdg, "EXPECTED_DATE_COUNT", len(_DATES))
    monkeypatch.setattr(mdg, "CANONICAL_DATE_START", _DATES[0])
    monkeypatch.setattr(mdg, "CANONICAL_DATE_END", _DATES[-1])
    monkeypatch.setattr(mdg, "SAMPLE_DATES", _DATES)
    monkeypatch.setattr(mdg, "PHASE_4BMC_QA_PATH", qa_stub)
    monkeypatch.setattr(mdg, "PHASE_4BMC_CLOSEOUT_PATH", closeout_stub)
    monkeypatch.setattr(mdg, "PHASE_4BMC_MERGE_CLOSEOUT_PATH", merge_closeout_stub)

    # Materialize governance artefacts first and patch EXPECTED_*_SHA
    # to the freshly-computed values. Per-file Parquets need to embed
    # the patched SHAs as per-row lineage so check 4bm-d.13.37 passes.
    raw_manifest_path = micro_root / "manifests" / (
        "microstructure_raw_aggtrades_v001__v002.json"
    )
    raw_manifest_body = {
        "dataset_family": "microstructure_raw_aggtrades_v001",
        "dataset_version": "v002",
        "symbol_list": [mdc.CANONICAL_SYMBOL],
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "total_row_count": _TOTAL_EVENTS,
        "date_count": len(_DATES),
    }
    raw_manifest_bytes = json.dumps(raw_manifest_body, sort_keys=True).encode("utf-8")
    raw_manifest_path.write_bytes(raw_manifest_bytes)
    raw_manifest_sha = _sha256_bytes(raw_manifest_bytes)
    Path(str(raw_manifest_path) + ".sha256").write_text(
        f"{raw_manifest_sha}  {raw_manifest_path.name}\n", encoding="utf-8"
    )

    acquisition_log_path = micro_root / "manifests" / (
        "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
    )
    acquisition_log_path.write_text("acquisition log stub\n", encoding="utf-8")
    acquisition_log_sha = _sha256_file(acquisition_log_path)
    Path(str(acquisition_log_path) + ".sha256").write_text(
        f"{acquisition_log_sha}  {acquisition_log_path.name}\n",
        encoding="utf-8",
    )

    gate_report_path = (
        micro_root / "gate-reports" / "raw"
        / f"{mdc.EXPECTED_GATE_REPORT_ID}.json"
    )
    gate_report_path.write_text("raw gate report stub\n", encoding="utf-8")
    gate_report_sha = _sha256_file(gate_report_path)
    Path(str(gate_report_path) + ".sha256").write_text(
        f"{gate_report_sha}  {gate_report_path.name}\n", encoding="utf-8"
    )

    successor_state_path = (
        micro_root / "successor-state" / "phase-4bl-e_successor_state.json"
    )
    successor_state_path.write_text("successor state stub\n", encoding="utf-8")
    successor_state_sha = _sha256_file(successor_state_path)
    Path(str(successor_state_path) + ".sha256").write_text(
        f"{successor_state_sha}  {successor_state_path.name}\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(mdc, "EXPECTED_RAW_MANIFEST_SHA", raw_manifest_sha)
    monkeypatch.setattr(mdc, "EXPECTED_ACQUISITION_LOG_SHA", acquisition_log_sha)
    monkeypatch.setattr(mdc, "EXPECTED_GATE_REPORT_SHA", gate_report_sha)
    monkeypatch.setattr(mdc, "EXPECTED_SUCCESSOR_STATE_SHA", successor_state_sha)

    # PERFILE_INVARIANT_LINEAGE_COLUMNS is a module-level tuple that
    # bakes in the EXPECTED_*_SHA values at import time. Rebuild it
    # with the patched values so check 4bm-d.13.37's per-row lineage
    # comparison reads the right expected SHAs.
    monkeypatch.setattr(
        mdc,
        "PERFILE_INVARIANT_LINEAGE_COLUMNS",
        (
            ("dataset_family", mdc.CANONICAL_DATASET_FAMILY),
            ("dataset_version", mdc.CANONICAL_DATASET_VERSION),
            ("source_dataset_family", mdc.CANONICAL_SOURCE_DATASET_FAMILY),
            ("source_dataset_version", mdc.CANONICAL_SOURCE_DATASET_VERSION),
            ("symbol", mdc.CANONICAL_SYMBOL),
            ("source_manifest_sha256", raw_manifest_sha),
            ("source_gate_report_id", mdc.EXPECTED_GATE_REPORT_ID),
            ("source_gate_report_sha256", gate_report_sha),
            (
                "normalization_schema_version",
                mdc.CANONICAL_NORMALIZATION_SCHEMA_VERSION,
            ),
        ),
    )

    # Materialize the 5 per-date Parquet+sidecar+raw-zip triples.
    per_file_inventory: list[dict[str, Any]] = []
    base_id = 1_000
    for i, date in enumerate(_DATES):
        yyyy, mm, _ = date.split("-")
        day_start_ms = int(
            dt.datetime.strptime(date, "%Y-%m-%d")
            .replace(tzinfo=dt.UTC)
            .timestamp()
            * 1000
        )
        first_t = day_start_ms + 1_000  # 1s past UTC day start (within the day)
        last_t = first_t + _EVENTS_PER_DATE - 1
        min_id = base_id + i * 1_000
        max_id = min_id + _EVENTS_PER_DATE - 1

        parquet_dir = (
            micro_root
            / "normalized"
            / mdc.CANONICAL_DATASET_FAMILY
            / mdc.CANONICAL_SYMBOL
            / yyyy
            / mm
        )
        parquet_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = (
            parquet_dir / f"{mdc.CANONICAL_SYMBOL}-aggTrades-{date}.parquet"
        )
        sidecar_path = (
            parquet_dir / f"{mdc.CANONICAL_SYMBOL}-aggTrades-{date}.parquet.sha256"
        )

        zip_dir = (
            micro_root
            / "raw"
            / "microstructure_raw_aggtrades_v001"
            / mdc.CANONICAL_SYMBOL
            / yyyy
            / mm
        )
        zip_dir.mkdir(parents=True, exist_ok=True)
        zip_path = zip_dir / f"{mdc.CANONICAL_SYMBOL}-aggTrades-{date}.zip"
        zip_payload = b"raw-zip-stub-" + date.encode("ascii")
        zip_path.write_bytes(zip_payload)
        zip_sha = _sha256_bytes(zip_payload)

        table = _build_sample_table(
            date=date,
            first_t=first_t,
            min_id=min_id,
            n=_EVENTS_PER_DATE,
            zip_sha=zip_sha,
            raw_manifest_sha=raw_manifest_sha,
            gate_report_sha=gate_report_sha,
            gate_report_id=mdc.EXPECTED_GATE_REPORT_ID,
        )
        pq.write_table(table, parquet_path)
        parquet_sha = _sha256_file(parquet_path)
        parquet_size = parquet_path.stat().st_size
        sidecar_path.write_text(
            f"{parquet_sha}  {parquet_path.name}\n", encoding="utf-8"
        )
        sidecar_sha = _sha256_file(sidecar_path)
        sidecar_size = sidecar_path.stat().st_size

        parquet_rel = (
            f"microstructure/normalized/{mdc.CANONICAL_DATASET_FAMILY}/"
            f"{mdc.CANONICAL_SYMBOL}/{yyyy}/{mm}/"
            f"{mdc.CANONICAL_SYMBOL}-aggTrades-{date}.parquet"
        )
        zip_rel = (
            f"microstructure/raw/microstructure_raw_aggtrades_v001/"
            f"{mdc.CANONICAL_SYMBOL}/{yyyy}/{mm}/"
            f"{mdc.CANONICAL_SYMBOL}-aggTrades-{date}.zip"
        )
        per_file_inventory.append(
            {
                "date": date,
                "symbol": mdc.CANONICAL_SYMBOL,
                "local_parquet_path": parquet_rel,
                "local_sidecar_path": parquet_rel + ".sha256",
                "source_zip_path": zip_rel,
                "parquet_sha256": parquet_sha,
                "sidecar_sha256": sidecar_sha,
                "source_file_sha256": zip_sha,
                "parquet_size_bytes": parquet_size,
                "sidecar_size_bytes": sidecar_size,
                "event_count": _EVENTS_PER_DATE,
                "first_transact_time_ms": first_t,
                "last_transact_time_ms": last_t,
                "min_agg_trade_id": min_id,
                "max_agg_trade_id": max_id,
            }
        )

    derived_manifest = {
        "dataset_family": mdc.CANONICAL_DATASET_FAMILY,
        "dataset_version": mdc.CANONICAL_DATASET_VERSION,
        "schema_version": "v001",
        "source_dataset_family": "microstructure_raw_aggtrades_v001",
        "source_dataset_version": "v002",
        "source_phase_boundary": "4bl-E",
        "source_manifest_path": str(raw_manifest_path),
        "source_manifest_sha256": raw_manifest_sha,
        "source_acquisition_log_path": str(acquisition_log_path),
        "source_acquisition_log_sha256": acquisition_log_sha,
        "source_gate_report_path": str(gate_report_path),
        "source_gate_report_id": mdc.EXPECTED_GATE_REPORT_ID,
        "source_gate_report_sha256": gate_report_sha,
        "source_successor_state_path": str(successor_state_path),
        "source_successor_state_sha256": successor_state_sha,
        "symbol_list": [mdc.CANONICAL_SYMBOL],
        "date_start": _DATES[0],
        "date_end": _DATES[-1],
        "date_count": len(_DATES),
        "date_list": list(_DATES),
        "expected_file_count": len(_DATES),
        "produced_file_count": len(_DATES),
        "total_event_count": _TOTAL_EVENTS,
        "per_file_inventory": per_file_inventory,
        "invalid_windows": [],
        "governance_labels": {
            "phase": "4bm-b",
            "source_phase_boundary": "4bl-E",
            "validator": "phase_4ax_aggtrades_v001",
            "stop_trigger_domain": "trade_price_backtest_candidate",
            "feature_computation": "forbidden",
            "strategy_use": "forbidden",
            "source_dataset_family": "microstructure_raw_aggtrades_v001",
            "source_dataset_version": "v002",
            "source_manifest_path": str(raw_manifest_path),
            "source_manifest_sha256": raw_manifest_sha,
            "source_gate_report_id": mdc.EXPECTED_GATE_REPORT_ID,
            "source_gate_report_sha256": gate_report_sha,
            "source_gate_report_code_commit_sha": "0" * 40,
            "source_successor_state_sha256": successor_state_sha,
            "multi_day": True,
            "phase_4bm_b_no_successor_authorization": True,
        },
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "code_commit_sha": "0" * 40,
        "base_commit_sha": "0" * 40,
        "capture_config_hash": "deadbeef" * 8,
        "created_at_unix_ms": 1_700_000_000_000,
        "created_at_utc": "2024-12-01T00:00:00Z",
        "phase": "4bm-b",
    }
    derived_manifest_path = micro_root / "manifests" / (
        "microstructure_normalized_aggtrades_v001__v002.json"
    )
    derived_manifest_bytes = json.dumps(
        derived_manifest, sort_keys=True
    ).encode("utf-8")
    derived_manifest_path.write_bytes(derived_manifest_bytes)
    derived_manifest_sha = _sha256_bytes(derived_manifest_bytes)
    Path(str(derived_manifest_path) + ".sha256").write_text(
        f"{derived_manifest_sha}  {derived_manifest_path.name}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mdc, "EXPECTED_DERIVED_MANIFEST_SHA", derived_manifest_sha)

    return OrchestratorFixture(
        tmp_path=tmp_path,
        micro_root=micro_root,
        derived_manifest_path=derived_manifest_path,
        output_root=micro_root / "gate-reports" / "normalized",
        qa_stub=qa_stub,
        closeout_stub=closeout_stub,
        merge_closeout_stub=merge_closeout_stub,
        raw_manifest_path=raw_manifest_path,
        raw_manifest_sha=raw_manifest_sha,
        derived_manifest_sha=derived_manifest_sha,
    )


def _run(fx: OrchestratorFixture) -> MultidayDerivedAggTradesGateResult:
    return run_multiday_derived_aggtrades_gate(
        MultidayDerivedAggTradesGateInput(
            derived_manifest_path=fx.derived_manifest_path,
            output_root=fx.output_root,
            code_commit_sha=_CODE_COMMIT,
        )
    )


# ---------------------------------------------------------------------------
# Input rejection tests
# ---------------------------------------------------------------------------


def test_input_rejects_non_path_derived_manifest_path(tmp_path: Path) -> None:
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(
        MultidayDerivedAggTradesGateInputError, match="derived_manifest_path"
    ):
        MultidayDerivedAggTradesGateInput(
            derived_manifest_path="not-a-path",  # type: ignore[arg-type]
            output_root=out,
            code_commit_sha="c" * 40,
        )


def test_input_rejects_non_path_output_root(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"{}")
    with pytest.raises(MultidayDerivedAggTradesGateInputError, match="output_root"):
        MultidayDerivedAggTradesGateInput(
            derived_manifest_path=p,
            output_root="not-a-path",  # type: ignore[arg-type]
            code_commit_sha="c" * 40,
        )


def test_input_rejects_empty_code_commit_sha(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"{}")
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(
        MultidayDerivedAggTradesGateInputError, match="code_commit_sha"
    ):
        MultidayDerivedAggTradesGateInput(
            derived_manifest_path=p,
            output_root=out,
            code_commit_sha="",
        )


def test_input_rejects_path_not_under_microstructure(tmp_path: Path) -> None:
    bad = tmp_path / "elsewhere" / "manifest.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_bytes(b"{}")
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(
        MultidayDerivedAggTradesGateInputError, match="derived_manifest_path"
    ):
        MultidayDerivedAggTradesGateInput(
            derived_manifest_path=bad,
            output_root=out,
            code_commit_sha="c" * 40,
        )


# ---------------------------------------------------------------------------
# End-to-end happy-path orchestrator tests
# ---------------------------------------------------------------------------


def test_run_happy_path_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    res = _run(fx)
    if res.overall_status != "pass":
        failing = [
            f"{c.check_id}({c.status.name}): {c.detail}"
            for c in res.checks
            if c.status != mdc.MultidayDerivedAggTradesCheckStatus.PASS
        ]
        pytest.fail(
            f"expected overall pass, got {res.overall_status!r}; "
            f"failing checks: {failing}"
        )
    assert res.gate_verdict == GATE_VERDICT_PASS
    assert len(res.checks) == 60
    assert res.report_path is not None
    assert res.report_path.exists()
    sidecar_path = res.report_path.with_suffix(".json.sha256")
    assert sidecar_path.exists(), f"missing sidecar at {sidecar_path}"


def test_run_happy_path_preserves_pre_post_immutability(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    tracked_paths = [
        fx.derived_manifest_path,
        Path(str(fx.derived_manifest_path) + ".sha256"),
        fx.raw_manifest_path,
        Path(str(fx.raw_manifest_path) + ".sha256"),
    ]
    # Track every per-file Parquet + sidecar + raw zip too.
    manifest_obj = json.loads(fx.derived_manifest_path.read_bytes())
    for inv in manifest_obj["per_file_inventory"]:
        tracked_paths.extend(
            [
                fx.tmp_path / "data" / inv["local_parquet_path"],
                fx.tmp_path / "data" / inv["local_sidecar_path"],
                fx.tmp_path / "data" / inv["source_zip_path"],
            ]
        )
    pre = {p: _sha256_file(p) for p in tracked_paths}
    res = _run(fx)
    post = {p: _sha256_file(p) for p in tracked_paths}
    assert pre == post
    assert res.boundary_confirmations["no_manifest_mutation"] is True
    assert res.boundary_confirmations["no_per_file_parquet_mutation"] is True
    assert res.boundary_confirmations["no_per_file_sidecar_mutation"] is True
    assert res.boundary_confirmations["no_raw_zip_mutation"] is True


def test_run_happy_path_writes_canonical_report_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    res = _run(fx)
    assert res.report_path is not None
    parts = res.report_path.parts
    for needle in ("data", "microstructure", "gate-reports", "normalized"):
        assert needle in parts, f"{needle} not found in {parts}"
    assert "phase-4bm-d" in res.report_path.name
    assert res.report_id.startswith(
        f"{mdc.CANONICAL_DATASET_FAMILY}__{mdc.CANONICAL_DATASET_VERSION}__"
        f"phase-4bm-d__"
    )
    assert res.report_id.endswith(_CODE_COMMIT[:12])


def test_run_happy_path_returns_19_boundary_confirmations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    res = _run(fx)
    assert len(_BOUNDARY_KEYS) == 19
    assert set(res.boundary_confirmations.keys()) == set(_BOUNDARY_KEYS)
    assert all(
        res.boundary_confirmations[k] is True for k in _BOUNDARY_KEYS
    ), res.boundary_confirmations


def test_run_happy_path_invariants(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    res = _run(fx)
    assert res.research_eligible_after is False
    assert res.no_successor_authorization is True
    assert res.eligibility_gate_status_after == "pass"


# ---------------------------------------------------------------------------
# Failure-path orchestrator tests
# ---------------------------------------------------------------------------


def test_run_fails_when_derived_manifest_sha_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    monkeypatch.setattr(mdc, "EXPECTED_DERIVED_MANIFEST_SHA", "f" * 64)
    res = _run(fx)
    assert res.overall_status == "fail"
    assert res.gate_verdict == GATE_VERDICT_FAIL
    by_id = {c.check_id: c for c in res.checks}
    assert (
        by_id["4bm-d.13.3"].status
        == mdc.MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_run_fails_when_phase_4bmc_merge_closeout_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    fx.merge_closeout_stub.unlink()
    res = _run(fx)
    assert res.overall_status == "fail"
    assert res.gate_verdict == GATE_VERDICT_FAIL
    by_id = {c.check_id: c for c in res.checks}
    assert (
        by_id["4bm-d.13.40"].status
        == mdc.MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_run_refuses_overwrite_on_second_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _setup_passing_orchestrator(tmp_path, monkeypatch)
    fixed_time = 1_715_000_000.0
    monkeypatch.setattr(mdg.time, "time", lambda: fixed_time)
    first = _run(fx)
    assert first.report_path is not None and first.report_path.exists()
    with pytest.raises(GateIOError, match="refusing to overwrite"):
        _run(fx)
