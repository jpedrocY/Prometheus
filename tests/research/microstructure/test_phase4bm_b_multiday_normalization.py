"""Offline tests for the Phase 4bm-B multi-day normalization orchestrator.

These tests load ``scripts/phase4bm_b_normalize_multiday_aggtrades.py``
directly by file path (it lives under ``scripts/`` and is not a package)
and exercise:

1. Locked identity constants match the Phase 4bm-A design memo verbatim.
2. Pure helpers ``_utc_date_to_day_start_ms``, ``_sha256_file``, and
   ``_pa_schema`` behave as documented.
3. The pyarrow schema column names equal
   :data:`NORMALIZED_SCHEMA_V001` byte-for-byte.
4. ``normalize_one_date`` produces a Parquet + sidecar with the correct
   row count, lineage columns, schema, and atomic-write / refuse-overwrite
   semantics on a synthetic 1-row fixture.
5. ``normalize_one_date`` fails closed on inventory mismatch
   (row count, agg-trade-id bounds, transact-time bounds, day-boundary
   violations, duplicate agg-trade-id, non-monotone agg-trade-id, etc.).
6. ``build_multiday_manifest`` produces the brief-mandated top-level
   structure with all governance / non-authorization / boundary keys.
7. The orchestrator's CLI exposes the documented flags and accepts
   ``--dry-run`` without writing anything.
8. The script never references forbidden network / credential / MCP /
   Graphify tokens.

The tests do NOT execute the orchestrator against the real on-disk
v002 raw artefacts; that is the end-to-end run reported separately.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pyarrow.parquet as pq
import pytest

from ._eligibility_fixtures import FixtureRow

# --------------------------------------------------------------------------- #
# Load the orchestrator module by file path.
# --------------------------------------------------------------------------- #

_REPO_ROOT: Path = Path(__file__).resolve().parents[3]
_SCRIPT_PATH: Path = (
    _REPO_ROOT / "scripts" / "phase4bm_b_normalize_multiday_aggtrades.py"
)


def _load_orchestrator() -> object:
    module_name = "phase4bm_b_normalize_multiday_aggtrades_under_test"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(
        module_name,
        _SCRIPT_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def orch() -> object:
    return _load_orchestrator()


# --------------------------------------------------------------------------- #
# Section 1 — Locked identity constants
# --------------------------------------------------------------------------- #


def test_phase_id_constant(orch: object) -> None:
    assert orch.PHASE_ID == "4bm-B"


def test_normalized_dataset_family_constant(orch: object) -> None:
    assert (
        orch.NORMALIZED_DATASET_FAMILY
        == "microstructure_normalized_aggtrades_v001"
    )


def test_normalized_dataset_version_is_v002(orch: object) -> None:
    assert orch.NORMALIZED_DATASET_VERSION == "v002"


def test_source_dataset_family_constant(orch: object) -> None:
    assert orch.SOURCE_DATASET_FAMILY == "microstructure_raw_aggtrades_v001"


def test_source_dataset_version_is_v002(orch: object) -> None:
    assert orch.SOURCE_DATASET_VERSION == "v002"


def test_symbol_btcusdt(orch: object) -> None:
    assert orch.SYMBOL == "BTCUSDT"


def test_date_count_90(orch: object) -> None:
    assert orch.EXPECTED_DATE_COUNT == 90


def test_total_event_count_constant(orch: object) -> None:
    assert orch.EXPECTED_TOTAL_EVENT_COUNT == 155_153_449


def test_date_range(orch: object) -> None:
    assert orch.EXPECTED_DATE_START == "2024-12-01"
    assert orch.EXPECTED_DATE_END == "2025-02-28"


# --------------------------------------------------------------------------- #
# Section 2 — Expected SHA constants match Phase 4bm-A §4 verbatim
# --------------------------------------------------------------------------- #


def test_expected_source_manifest_sha_phase_4bm_a_value(orch: object) -> None:
    assert orch.EXPECTED_SOURCE_MANIFEST_SHA == (
        "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
    )


def test_expected_source_manifest_sidecar_sha_phase_4bm_a_value(
    orch: object,
) -> None:
    assert orch.EXPECTED_SOURCE_MANIFEST_SIDECAR_SHA == (
        "adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26"
    )


def test_expected_acquisition_log_sha_phase_4bm_a_value(orch: object) -> None:
    assert orch.EXPECTED_ACQUISITION_LOG_SHA == (
        "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
    )


def test_expected_gate_report_sha_phase_4bm_a_value(orch: object) -> None:
    assert orch.EXPECTED_GATE_REPORT_SHA == (
        "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"
    )


def test_expected_successor_state_sha_phase_4bm_a_value(orch: object) -> None:
    assert orch.EXPECTED_SUCCESSOR_STATE_SHA == (
        "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d"
    )


# --------------------------------------------------------------------------- #
# Section 3 — Schema discipline
# --------------------------------------------------------------------------- #


def test_normalized_schema_has_19_columns(orch: object) -> None:
    assert len(orch.NORMALIZED_SCHEMA_V001) == 19


def test_normalization_schema_version_v001(orch: object) -> None:
    assert orch.NORMALIZATION_SCHEMA_VERSION == "v001"


def test_pa_schema_column_names_match_v001(orch: object) -> None:
    schema = orch._pa_schema()
    assert tuple(schema.names) == orch.NORMALIZED_SCHEMA_V001


def test_no_forbidden_column_substring_in_schema(orch: object) -> None:
    forbidden = (
        "label", "target", "future", "signal", "entry", "exit",
        "pnl", "profit", "loss", "mfe", "mae", "r_multiple",
        "equity", "alpha", "edge", "prediction", "model",
        "score", "decision", "strategy", "liquidation", "funding",
        "open_interest", "order_book", "mark_price",
    )
    for col in orch.NORMALIZED_SCHEMA_V001:
        for needle in forbidden:
            assert needle not in col.lower(), (
                f"column {col!r} contains forbidden substring {needle!r}"
            )


# --------------------------------------------------------------------------- #
# Section 4 — Pure helpers
# --------------------------------------------------------------------------- #


def test_utc_date_to_day_start_ms_known_value(orch: object) -> None:
    # 2024-12-01 00:00:00 UTC
    assert orch._utc_date_to_day_start_ms("2024-12-01") == 1_733_011_200_000


def test_utc_date_to_day_start_ms_jan_first(orch: object) -> None:
    # 2025-01-01 00:00:00 UTC
    assert orch._utc_date_to_day_start_ms("2025-01-01") == 1_735_689_600_000


def test_sha256_file_matches_hashlib(orch: object, tmp_path: Path) -> None:
    import hashlib

    f = tmp_path / "x.bin"
    body = b"hello prometheus\n" * 100
    f.write_bytes(body)
    h, size = orch._sha256_file(f)
    assert h == hashlib.sha256(body).hexdigest()
    assert size == len(body)


# --------------------------------------------------------------------------- #
# Section 5 — normalize_one_date happy path on a synthetic fixture
# --------------------------------------------------------------------------- #


def _build_synthetic_inventory_and_zip(
    *,
    date: str,
    tmp_path: Path,
    n: int = 6,
) -> tuple[dict[str, object], Path, str]:
    """Build a 1-day synthetic raw zip + inventory entry under *tmp_path*."""
    from datetime import UTC, datetime

    day_start_ms = int(
        datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp()
        * 1000
    )
    rows = [
        FixtureRow(
            a=2_000_000 + i,
            p=f"{100000 + i}",
            q="0.001",
            f=10 * (2_000_000 + i),
            l=10 * (2_000_000 + i) + 1,
            T=day_start_ms + 1000 + i * 100,
            m=(i % 2 == 0),
        )
        for i in range(n)
    ]
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
    # Use the eligibility fixture writer but override the in-zip member name
    # to match the canonical date.
    import io
    import zipfile

    csv_buf = io.StringIO()
    csv_buf.write(
        "agg_trade_id,price,quantity,first_trade_id,last_trade_id,"
        "transact_time,is_buyer_maker\n"
    )
    for r in rows:
        csv_buf.write(
            f"{r.a},{r.p},{r.q},{r.f},{r.l},{r.T},"
            f"{'true' if r.m else 'false'}\n"
        )
    body = csv_buf.getvalue().encode("utf-8")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"BTCUSDT-aggTrades-{date}.csv", body)

    import hashlib

    raw_zip_sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()

    inventory = {
        "date": date,
        "sha256": raw_zip_sha,
        "size_bytes": zip_path.stat().st_size,
        "row_count": n,
        "first_trade_time_ms": rows[0].T,
        "last_trade_time_ms": rows[-1].T,
        "min_agg_trade_id": rows[0].a,
        "max_agg_trade_id": rows[-1].a,
        "local_zip_path": (
            f"microstructure/raw/microstructure_raw_aggtrades_v001/"
            f"BTCUSDT/{yyyy}/{mm}/BTCUSDT-aggTrades-{date}.zip"
        ),
        "local_sidecar_path": (
            f"microstructure/raw/microstructure_raw_aggtrades_v001/"
            f"BTCUSDT/{yyyy}/{mm}/BTCUSDT-aggTrades-{date}.zip.sha256"
        ),
        "status": "acquired_verified",
    }
    return inventory, zip_path, raw_zip_sha


def test_normalize_one_date_happy_path(orch: object, tmp_path: Path) -> None:
    inventory, zip_path, raw_zip_sha = _build_synthetic_inventory_and_zip(
        date="2024-12-01", tmp_path=tmp_path, n=5
    )
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    record = orch.normalize_one_date(
        inventory_entry=inventory,
        raw_zip_path=zip_path,
        raw_zip_sha=raw_zip_sha,
        source_manifest_sha="a" * 64,
        gate_report_id="microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1__deadbeef",
        gate_report_sha="b" * 64,
        output_root=output_root,
        refuse_overwrite=True,
    )
    assert record.date == "2024-12-01"
    assert record.symbol == "BTCUSDT"
    assert record.event_count == 5
    assert record.source_file_sha256 == raw_zip_sha
    assert record.status == "produced_verified"
    # Parquet file exists at the canonical path. Family directory is
    # version-suffixed (`__v002`) so v002 multi-day output coexists cleanly
    # with the existing Phase 4bd v001 single-day Parquet at the same date
    # (per Phase 4bm-A design memo §7).
    target = (
        output_root
        / "microstructure_normalized_aggtrades_v001__v002"
        / "BTCUSDT"
        / "2024"
        / "12"
        / "BTCUSDT-aggTrades-2024-12-01.parquet"
    )
    assert target.exists()
    sidecar = target.with_suffix(target.suffix + ".sha256")
    assert sidecar.exists()
    # Sidecar parses to canonical Phase 4bb-F format.
    sidecar_body = sidecar.read_text(encoding="utf-8")
    assert sidecar_body.endswith("\n")
    assert "  " in sidecar_body  # two spaces separator
    assert "\r\n" not in sidecar_body  # LF only

    # Round-trip Parquet and verify schema + row count + a few values.
    table = pq.read_table(target)
    assert table.num_rows == 5
    assert tuple(table.schema.names) == orch.NORMALIZED_SCHEMA_V001
    df_cols = {n: table.column(n).to_pylist() for n in table.schema.names}
    assert df_cols["dataset_family"][0] == orch.NORMALIZED_DATASET_FAMILY
    assert df_cols["dataset_version"][0] == "v002"
    assert df_cols["source_dataset_version"][0] == "v002"
    assert df_cols["symbol"][0] == "BTCUSDT"
    assert df_cols["utc_date"][0] == "2024-12-01"
    assert df_cols["row_index"] == [0, 1, 2, 3, 4]
    assert df_cols["source_file_sha256"][0] == raw_zip_sha
    # price / quantity stored as strings.
    assert isinstance(df_cols["price"][0], str)
    assert isinstance(df_cols["quantity"][0], str)
    # is_buyer_maker is bool.
    assert all(isinstance(v, bool) for v in df_cols["is_buyer_maker"])


def test_normalize_one_date_refuse_overwrite(
    orch: object, tmp_path: Path
) -> None:
    inventory, zip_path, raw_zip_sha = _build_synthetic_inventory_and_zip(
        date="2024-12-02", tmp_path=tmp_path, n=3
    )
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    orch.normalize_one_date(
        inventory_entry=inventory,
        raw_zip_path=zip_path,
        raw_zip_sha=raw_zip_sha,
        source_manifest_sha="a" * 64,
        gate_report_id="g",
        gate_report_sha="b" * 64,
        output_root=output_root,
        refuse_overwrite=True,
    )
    # Second call must refuse to overwrite. The writer raises a
    # ``NormalizationIOError`` subclass; we tolerate any subclass of
    # ``RuntimeError`` here to avoid coupling to the writer's exact
    # exception path beyond what the orchestrator-level contract
    # guarantees.
    with pytest.raises(RuntimeError):
        orch.normalize_one_date(
            inventory_entry=inventory,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_zip_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )


# --------------------------------------------------------------------------- #
# Section 6 — normalize_one_date fail-closed paths
# --------------------------------------------------------------------------- #


def test_normalize_one_date_row_count_mismatch_fails_closed(
    orch: object, tmp_path: Path
) -> None:
    inventory, zip_path, raw_zip_sha = _build_synthetic_inventory_and_zip(
        date="2024-12-03", tmp_path=tmp_path, n=4
    )
    # Pretend the manifest expected 99 rows.
    inventory_bad = dict(inventory)
    inventory_bad["row_count"] = 99
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bmBValidationError) as ei:
        orch.normalize_one_date(
            inventory_entry=inventory_bad,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_zip_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )
    assert "row count" in str(ei.value).lower()


def test_normalize_one_date_first_ms_mismatch_fails_closed(
    orch: object, tmp_path: Path
) -> None:
    inventory, zip_path, raw_zip_sha = _build_synthetic_inventory_and_zip(
        date="2024-12-04", tmp_path=tmp_path, n=4
    )
    inventory_bad = dict(inventory)
    inventory_bad["first_trade_time_ms"] = (
        int(inventory["first_trade_time_ms"]) + 1
    )
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bmBValidationError) as ei:
        orch.normalize_one_date(
            inventory_entry=inventory_bad,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_zip_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )
    assert "first_transact_time_ms" in str(ei.value)


def test_normalize_one_date_min_agg_id_mismatch_fails_closed(
    orch: object, tmp_path: Path
) -> None:
    inventory, zip_path, raw_zip_sha = _build_synthetic_inventory_and_zip(
        date="2024-12-05", tmp_path=tmp_path, n=4
    )
    inventory_bad = dict(inventory)
    inventory_bad["min_agg_trade_id"] = int(inventory["min_agg_trade_id"]) - 1
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bmBValidationError) as ei:
        orch.normalize_one_date(
            inventory_entry=inventory_bad,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_zip_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )
    assert "min_agg_trade_id" in str(ei.value)


def test_normalize_one_date_multiple_zip_members_fails_closed(
    orch: object, tmp_path: Path
) -> None:
    import zipfile

    date = "2024-12-06"
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
    # Two CSVs inside.
    csv = (
        "agg_trade_id,price,quantity,first_trade_id,last_trade_id,"
        "transact_time,is_buyer_maker\n1,1,0.001,10,11,1733443200001,true\n"
    )
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"BTCUSDT-aggTrades-{date}.csv", csv.encode("utf-8"))
        zf.writestr("extra.csv", csv.encode("utf-8"))

    import hashlib

    raw_zip_sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    inventory = {
        "date": date,
        "row_count": 1,
        "first_trade_time_ms": 1733443200001,
        "last_trade_time_ms": 1733443200001,
        "min_agg_trade_id": 1,
        "max_agg_trade_id": 1,
        "local_zip_path": "...",
    }
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bmBValidationError) as ei:
        orch.normalize_one_date(
            inventory_entry=inventory,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_zip_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )
    assert "exactly one CSV member" in str(ei.value)


def test_normalize_one_date_out_of_day_ms_fails_closed(
    orch: object, tmp_path: Path
) -> None:
    """Transact-time-ms outside half-open day bounds must fail closed."""
    import hashlib
    import zipfile

    date = "2024-12-07"
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
    # row T = day_start_ms - 1 (out of half-open window)
    day_start_ms = orch._utc_date_to_day_start_ms(date)
    out_T = day_start_ms - 1
    csv = (
        "agg_trade_id,price,quantity,first_trade_id,last_trade_id,"
        "transact_time,is_buyer_maker\n"
        f"1,1,0.001,10,11,{out_T},true\n"
    )
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"BTCUSDT-aggTrades-{date}.csv", csv.encode("utf-8"))
    raw_zip_sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    inventory = {
        "date": date,
        "row_count": 1,
        "first_trade_time_ms": out_T,
        "last_trade_time_ms": out_T,
        "min_agg_trade_id": 1,
        "max_agg_trade_id": 1,
        "local_zip_path": "...",
    }
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bmBValidationError) as ei:
        orch.normalize_one_date(
            inventory_entry=inventory,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_zip_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )
    assert "half-open day bound" in str(ei.value)


def test_normalize_one_date_duplicate_agg_id_fails_closed(
    orch: object, tmp_path: Path
) -> None:
    import hashlib
    import zipfile

    date = "2024-12-08"
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
    day_start_ms = orch._utc_date_to_day_start_ms(date)
    csv = (
        "agg_trade_id,price,quantity,first_trade_id,last_trade_id,"
        "transact_time,is_buyer_maker\n"
        f"100,1,0.001,10,11,{day_start_ms + 1000},true\n"
        f"100,1,0.001,12,13,{day_start_ms + 2000},false\n"
    )
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"BTCUSDT-aggTrades-{date}.csv", csv.encode("utf-8"))
    raw_zip_sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    inventory = {
        "date": date,
        "row_count": 2,
        "first_trade_time_ms": day_start_ms + 1000,
        "last_trade_time_ms": day_start_ms + 2000,
        "min_agg_trade_id": 100,
        "max_agg_trade_id": 100,
        "local_zip_path": "...",
    }
    output_root = tmp_path / "data" / "microstructure" / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(orch.Phase4bmBValidationError) as ei:
        orch.normalize_one_date(
            inventory_entry=inventory,
            raw_zip_path=zip_path,
            raw_zip_sha=raw_zip_sha,
            source_manifest_sha="a" * 64,
            gate_report_id="g",
            gate_report_sha="b" * 64,
            output_root=output_root,
            refuse_overwrite=True,
        )
    assert "duplicate" in str(ei.value).lower()


# --------------------------------------------------------------------------- #
# Section 7 — build_multiday_manifest shape
# --------------------------------------------------------------------------- #


def _minimal_artefacts(orch: object, tmp_path: Path) -> object:
    """Construct a minimal SourceArtefactSet for manifest-shape tests."""
    return orch.SourceArtefactSet(
        source_manifest_path=tmp_path / "manifest.json",
        source_manifest_sha_before="m" * 64,
        source_manifest_parsed={
            "dataset_family": orch.SOURCE_DATASET_FAMILY,
            "dataset_version": orch.SOURCE_DATASET_VERSION,
            "schema_version": "v001",
            "symbol_list": ["BTCUSDT"],
            "date_start": "2024-12-01",
            "date_end": "2025-02-28",
            "date_count": 90,
            "date_list": ["2024-12-01"],
            "total_row_count": orch.EXPECTED_TOTAL_EVENT_COUNT,
            "acquired_at_unix_ms": 1,
            "code_commit_sha": "deadbeef" * 5,
            "base_commit_sha": "feedface" * 5,
        },
        source_manifest_sidecar_path=tmp_path / "manifest.json.sha256",
        source_manifest_sidecar_sha_before="ms" * 32,
        acquisition_log_path=tmp_path / "log.json",
        acquisition_log_sha_before="al" * 32,
        acquisition_log_sidecar_path=tmp_path / "log.json.sha256",
        acquisition_log_sidecar_sha_before="als" * 21 + "f",
        gate_report_path=tmp_path / "gate.json",
        gate_report_sha_before="g" * 64,
        gate_report_sidecar_path=tmp_path / "gate.json.sha256",
        gate_report_sidecar_sha_before="gs" * 32,
        successor_state_path=tmp_path / "ss.json",
        successor_state_sha_before="s" * 64,
        successor_state_sidecar_path=tmp_path / "ss.json.sha256",
        successor_state_sidecar_sha_before="ss" * 32,
        raw_zip_paths=[],
        raw_zip_sha_before=[],
        raw_zip_sidecar_paths=[],
        raw_zip_sidecar_sha_before=[],
        raw_zip_size_before=[],
    )


def test_build_multiday_manifest_required_top_level_keys(
    orch: object, tmp_path: Path
) -> None:
    artefacts = _minimal_artefacts(orch, tmp_path)
    record = orch.PerDayProductionRecord(
        date="2024-12-01",
        symbol="BTCUSDT",
        local_parquet_path="microstructure/normalized/.../x.parquet",
        local_sidecar_path="microstructure/normalized/.../x.parquet.sha256",
        parquet_sha256="p" * 64,
        sidecar_sha256="ps" * 32,
        parquet_size_bytes=12345,
        sidecar_size_bytes=100,
        event_count=10,
        first_transact_time_ms=1,
        last_transact_time_ms=10,
        min_agg_trade_id=1,
        max_agg_trade_id=10,
        source_file_sha256="r" * 64,
        source_zip_path="microstructure/raw/.../x.zip",
        status="produced_verified",
    )
    manifest = orch.build_multiday_manifest(
        artefacts=artefacts,
        per_day_records=[record],
        gate_report_id=(
            "microstructure_raw_aggtrades_v001__v002__"
            "phase-4bl-d-r__1__deadbeef"
        ),
        gate_report_code_commit_sha="ba" * 20,
        base_commit_sha="cd" * 20,
        code_commit_sha="ab" * 20,
        capture_config_hash="cc" * 32,
        created_at_unix_ms=1_700_000_000_000,
        created_at_utc="2025-12-01T00:00:00Z",
        source_manifest_path=artefacts.source_manifest_path,
        repo_root=tmp_path,
    )
    # Identity.
    assert manifest["dataset_family"] == orch.NORMALIZED_DATASET_FAMILY
    assert manifest["dataset_version"] == "v002"
    assert manifest["schema_version"] == "v001"
    assert manifest["symbol_list"] == ["BTCUSDT"]
    assert manifest["date_start"] == "2024-12-01"
    assert manifest["date_end"] == "2025-02-28"
    assert manifest["date_count"] == 90
    # Invariants.
    assert manifest["research_eligible"] is False
    assert manifest["eligibility_gate_status"] == "pending"
    # Lineage.
    assert manifest["source_dataset_family"] == orch.SOURCE_DATASET_FAMILY
    assert manifest["source_dataset_version"] == "v002"
    assert manifest["source_manifest_sha256"].endswith("m" * 8)
    # Inventory.
    assert manifest["produced_file_count"] == 1
    assert len(manifest["per_file_inventory"]) == 1
    inv = manifest["per_file_inventory"][0]
    assert inv["date"] == "2024-12-01"
    assert inv["parquet_sha256"] == "p" * 64
    # Governance labels block contains the Phase 4bm-A §8 16 required keys.
    gl = manifest["governance_labels"]
    for key in (
        "phase",
        "source_phase_boundary",
        "source_dataset_family",
        "source_dataset_version",
        "source_manifest_path",
        "source_manifest_sha256",
        "source_gate_report_id",
        "source_gate_report_sha256",
        "source_gate_report_code_commit_sha",
        "source_successor_state_sha256",
        "validator",
        "stop_trigger_domain",
        "feature_computation",
        "strategy_use",
        "phase_4bm_b_no_successor_authorization",
        "multi_day",
    ):
        assert key in gl, f"governance_labels missing {key}"
    # Phase identity recorded.
    assert gl["phase"] == "4bm-B"
    # No-successor invariant (governance label).
    assert gl["phase_4bm_b_no_successor_authorization"] == "true"
    # Forbidden labels.
    assert gl["feature_computation"] == "forbidden"
    assert gl["strategy_use"] == "forbidden"


# --------------------------------------------------------------------------- #
# Section 8 — CLI surface
# --------------------------------------------------------------------------- #


def test_cli_parser_exposes_required_flags(orch: object) -> None:
    parser = orch._build_parser()
    actions = {a.dest for a in parser._actions}
    for required in (
        "source_manifest",
        "gate_report",
        "successor_state",
        "output_root",
        "manifests_root",
        "dry_run",
        "allow_overwrite",
    ):
        assert required in actions, f"--{required.replace('_', '-')} missing"


# --------------------------------------------------------------------------- #
# Section 9 — Static no-network / no-credentials scan
# --------------------------------------------------------------------------- #


def test_orchestrator_does_not_import_forbidden_modules() -> None:
    src = _SCRIPT_PATH.read_text(encoding="utf-8")
    # Strip comments and docstring lines for the static scan.
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
    ):
        # match imports specifically (e.g. "import requests", "from requests")
        pattern = re.compile(
            rf"^\s*(?:import|from)\s+{re.escape(forbidden)}(?:\b|\.)",
            re.MULTILINE,
        )
        assert not pattern.search(src), (
            f"orchestrator imports forbidden module {forbidden!r}"
        )


def test_orchestrator_does_not_reference_credential_tokens() -> None:
    """No literal credential / secret tokens may appear in executable code.

    Docstrings and comments legitimately discuss the absence of these
    things, so the scan operates on code lines only (stripping ``#``
    comments and triple-quoted blocks).
    """
    raw = _SCRIPT_PATH.read_text(encoding="utf-8")
    # Strip module-level docstring (first triple-quoted block) and any
    # subsequent triple-quoted docstring lines, then strip inline ``#``
    # comments.
    in_triple = False
    code_lines: list[str] = []
    for line in raw.splitlines():
        s = line.strip()
        # Detect triple-quote toggles (very simple: count triple-quote
        # occurrences on the line).
        triple_count = s.count('"""') + s.count("'''")
        if triple_count == 1:
            in_triple = not in_triple
            continue
        if in_triple:
            continue
        # Drop everything from the first ``#`` (inline comment).
        cleaned = line.split("#", 1)[0]
        code_lines.append(cleaned)
    code_only = "\n".join(code_lines).lower()
    for token in (
        "api_key",
        "api-key",
        "listenkey",
        ".mcp.json",
        "graphify",
    ):
        assert token not in code_only, (
            f"orchestrator code references forbidden token {token!r}"
        )
