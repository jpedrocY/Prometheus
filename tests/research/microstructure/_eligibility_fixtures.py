"""Shared mini-fixture builders for the Phase 4bb-C eligibility-gate tests.

All fixtures live entirely within pytest ``tmp_path`` directories that are
arranged to look like ``data/microstructure/...``. They never touch the real
project ``data/microstructure/`` tree.
"""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FixtureRow:
    """A single aggTrade-style row used by mini-fixtures.

    The field name ``l`` (last-trade-id) deliberately mirrors the Binance
    public archive aggTrades CSV column ``l``; the linter's ambiguous-name
    warning is locally suppressed for the same reason.
    """

    a: int
    p: str
    q: str
    f: int
    l: int  # noqa: E741 — canonical aggTrades column name (last-trade-id)
    T: int
    m: bool


def make_default_rows(
    *,
    n: int = 8,
    start_T: int = 1736899200000 + 1000,  # 2025-01-15 00:00:01.000 UTC
    base_a: int = 1_000_000,
) -> list[FixtureRow]:
    """Return *n* contiguous rows with monotonically increasing IDs and T."""
    rows: list[FixtureRow] = []
    for i in range(n):
        rows.append(
            FixtureRow(
                a=base_a + i,
                p=f"{100000 + i}",  # any positive integer-shaped price
                q="0.001",
                f=10 * (base_a + i),
                l=10 * (base_a + i) + 1,
                T=start_T + i * 1000,
                m=(i % 2 == 0),
            )
        )
    return rows


def write_csv_zip(
    zip_path: Path,
    rows: Iterable[FixtureRow],
    *,
    header: bool = True,
    members: int = 1,
) -> int:
    """Write *rows* into a single-member ZIP archive at *zip_path*.

    Returns the byte count of the underlying CSV (uncompressed).
    """
    csv_buf = io.StringIO()
    if header:
        csv_buf.write("agg_trade_id,price,quantity,first_trade_id,last_trade_id,transact_time,is_buyer_maker\n")
    for r in rows:
        csv_buf.write(
            f"{r.a},{r.p},{r.q},{r.f},{r.l},{r.T},{'true' if r.m else 'false'}\n"
        )
    body = csv_buf.getvalue().encode("utf-8")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("BTCUSDT-aggTrades-2025-01-15.csv", body)
        if members >= 2:
            zf.writestr("extra_member.txt", b"unexpected\n")
    return len(body)


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_sidecar(sidecar_path: Path, sha: str) -> None:
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar_path.write_text(f"{sha}  {sidecar_path.with_suffix('').name}\n", encoding="utf-8")


def build_manifest_dict(
    *,
    relative_zip_path: str,
    file_sha256: str,
    event_count: int,
    start_time_ms: int,
    end_time_ms: int,
    research_eligible: bool = False,
    eligibility_gate_status: str = "pending",
    governance_overrides: dict[str, str] | None = None,
    invalid_windows: list[dict[str, Any]] | None = None,
    code_commit_sha: str | None = None,
) -> dict[str, Any]:
    """Construct a manifest dict mirroring the Phase 4az shape."""
    governance: dict[str, str] = {
        "phase": "4az",
        "source_phase_boundary": "4ay",
        "validator": "phase_4ax_aggtrades_v001",
        "stop_trigger_domain": "trade_price_backtest_candidate",
        "symbol_scope_source": "archive_path",
        "feature_computation": "forbidden",
        "strategy_use": "forbidden",
    }
    if governance_overrides:
        governance.update(governance_overrides)

    return {
        "dataset_family": "microstructure_raw_aggtrades_v001",
        "version": "v001",
        "symbol": "BTCUSDT",
        "source": "binance_data_archive",
        "endpoint": "data.binance.vision/data/futures/um/daily/aggTrades",
        "endpoint_docs_reference": (
            "https://github.com/binance/binance-public-data#trades "
            "(futures aggTrades daily archive convention)"
        ),
        "capture_mode": "historical_archive",
        "schema_version": "v001",
        "capture_config_hash": "d7508638b2184f4754900b6f2c2165a9499d5e79d0494600a62516738368010d",
        "code_commit_sha": code_commit_sha or "0000000000000000000000000000000000000000",
        "governance_labels": governance,
        "start_time_ms": start_time_ms,
        "end_time_ms": end_time_ms,
        "event_count": event_count,
        "file_count": 1,
        "files": [
            {
                "path": relative_zip_path,
                "sha256": file_sha256,
                "event_count": event_count,
                "start_time_ms": start_time_ms,
                "end_time_ms": end_time_ms,
            }
        ],
        "invalid_windows": invalid_windows or [],
        "retention_warning": None,
        "proxy_warning": None,
        "research_eligible": research_eligible,
        "eligibility_gate_status": eligibility_gate_status,
    }


def build_acquisition_log_dict(
    *,
    start_time_ms: int,
    end_time_ms: int,
    event_count: int,
    code_commit_sha: str = "0000000000000000000000000000000000000000",
) -> dict[str, Any]:
    return {
        "phase": "4az",
        "start_time_ms": start_time_ms,
        "end_time_ms": end_time_ms,
        "event_count": event_count,
        "code_commit_sha": code_commit_sha,
        "endpoint_docs_reference": (
            "https://github.com/binance/binance-public-data#trades "
            "(futures aggTrades daily archive convention)"
        ),
    }


@dataclass(frozen=True)
class FixtureBundle:
    """Paths to the synthesised mini-fixture artefacts."""

    microstructure_root: Path
    manifest_path: Path
    raw_zip_path: Path
    sidecar_path: Path
    acquisition_log_path: Path
    output_root: Path
    code_commit_sha: str


def build_happy_fixture(
    tmp_path: Path,
    *,
    rows: list[FixtureRow] | None = None,
    code_commit_sha: str | None = None,
    research_eligible: bool = False,
    eligibility_gate_status: str = "pending",
    governance_overrides: dict[str, str] | None = None,
    invalid_windows: list[dict[str, Any]] | None = None,
    write_sidecar_correctly: bool = True,
    write_acquisition_log: bool = True,
    multiple_zip_members: bool = False,
    omit_header: bool = False,
    extra_column: bool = False,
) -> FixtureBundle:
    """Build a complete mini-fixture rooted at ``tmp_path/data/microstructure/``."""
    rows = rows or make_default_rows()

    microstructure_root = tmp_path / "data" / "microstructure"
    raw_dir = (
        microstructure_root
        / "raw"
        / "microstructure_raw_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
    )
    manifests_dir = microstructure_root / "manifests"

    raw_zip_path = raw_dir / "BTCUSDT-aggTrades-2025-01-15.zip"
    sidecar_path = raw_zip_path.with_suffix(".zip.sha256")
    manifest_path = manifests_dir / "microstructure_raw_aggtrades_v001__v001.json"
    acquisition_log_path = (
        manifests_dir
        / "microstructure_raw_aggtrades_v001__v001_acquisition_log.json"
    )

    # Build CSV body manually if extra_column requested.
    if extra_column:
        csv_buf = io.StringIO()
        csv_buf.write(
            "agg_trade_id,price,quantity,first_trade_id,last_trade_id,transact_time,is_buyer_maker,unknown_extra\n"
        )
        for r in rows:
            csv_buf.write(
                f"{r.a},{r.p},{r.q},{r.f},{r.l},{r.T},{'true' if r.m else 'false'},X\n"
            )
        body = csv_buf.getvalue().encode("utf-8")
        raw_zip_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(raw_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("BTCUSDT-aggTrades-2025-01-15.csv", body)
    else:
        write_csv_zip(
            raw_zip_path,
            rows,
            header=not omit_header,
            members=2 if multiple_zip_members else 1,
        )

    sha = sha256_of_file(raw_zip_path)
    if write_sidecar_correctly:
        write_sidecar(sidecar_path, sha)

    start_T = rows[0].T
    end_T = rows[-1].T

    sha_for_manifest = sha
    code_sha = code_commit_sha or "0000000000000000000000000000000000000000"

    manifest = build_manifest_dict(
        relative_zip_path="raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip",
        file_sha256=sha_for_manifest,
        event_count=len(rows),
        start_time_ms=start_T,
        end_time_ms=end_T,
        research_eligible=research_eligible,
        eligibility_gate_status=eligibility_gate_status,
        governance_overrides=governance_overrides,
        invalid_windows=invalid_windows,
        code_commit_sha=code_sha,
    )
    manifests_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    if write_acquisition_log:
        acquisition_log_path.write_text(
            json.dumps(
                build_acquisition_log_dict(
                    start_time_ms=start_T,
                    end_time_ms=end_T,
                    event_count=len(rows),
                    code_commit_sha=code_sha,
                ),
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

    output_root = microstructure_root  # Output reports under same root.

    return FixtureBundle(
        microstructure_root=microstructure_root,
        manifest_path=manifest_path,
        raw_zip_path=raw_zip_path,
        sidecar_path=sidecar_path,
        acquisition_log_path=acquisition_log_path,
        output_root=output_root,
        code_commit_sha=code_sha,
    )


def utc_day_start_ms(year: int, month: int, day: int) -> int:
    return int(datetime(year, month, day, 0, 0, 0, tzinfo=UTC).timestamp() * 1000)
