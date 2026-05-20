"""Phase 4bm-H — Multi-Day v002 aggTrades Feature Computation orchestrator.

Standalone orchestrator authorised by the Phase 4bm-H authorization
prompt and the Phase 4bm-G feature-boundary design memo
(``docs/00-meta/implementation-reports/2026-05-18_phase-4bm-g_multi-day-v002-feature-boundary-design-memo.md``).

This script computes the v002 multi-day feature family
``microstructure_features_aggtrades_v001 @ v002`` from the 90
contiguous BTCUSDT UTC daily Parquets at
``microstructure_normalized_aggtrades_v001 @ v002`` (Phase 4bm-B
output; Phase 4bm-C / 4bm-D / 4bm-E / 4bm-F admitted at Stage-3).

The script:

- verifies all upstream lineage SHAs match the Phase 4bm-G recorded
  values before writing any output (fail closed on any mismatch);
- verifies no target v002 feature artefact already exists (refuse-to-
  overwrite policy);
- runs the v002 feature kernel day-by-day with Phase 4bm-G §16 policy
  1 causal cross-day lookback (prior-day tail loaded for each day
  >= 2); day 1 has no prior tail in scope so its early rows get
  ``rolling_missing_window_flag = True`` per the v002 schema;
- writes each per-day v002 feature Parquet + canonical Phase 4bb-F
  sidecar atomically;
- builds and writes the multi-day v002 feature manifest + canonical
  Phase 4bb-F sidecar atomically;
- re-hashes every upstream artefact AFTER all writes to confirm
  byte-identical immutability (Phase 4aw / 4bm-G fail-closed
  guarantee).

This script is intentionally narrow:

- Python standard library only (``hashlib``, ``json``, ``argparse``,
  ``os``, ``contextlib``, ``time``, ``datetime``, ``sys``, ``pathlib``)
  plus pyarrow plus the v001 Phase 4bh I/O scaffold plus the new
  v002 modules.
- NO network access (no ``urllib``, no ``requests``, no ``httpx``,
  no ``aiohttp``, no ``websockets``, no ``socket``, no ``binance``).
- NO credentials, no ``.env`` reads, no ``.mcp.json`` reads, no MCP,
  no Graphify.
- NO modification of any source artefact (v002 derived manifest,
  v002 raw manifest, v002 acquisition log, 90 v002 normalized
  Parquets, 90 v002 normalized sidecars, Phase 4bm-D gate report,
  Phase 4bm-F successor-state JSON, Phase 4bl-D-R raw gate report,
  Phase 4bl-E raw successor-state JSON, prior v001 normalized /
  feature / label artefacts).
- Refuses to overwrite an existing finalised output file.
- Atomic write-then-rename via ``os.replace`` and ``tempfile.mkstemp``.
- Pre/post SHA256 immutability check across all 10 governance
  artefacts plus all 90 per-day normalized Parquets (= 100
  immutability witnesses).
- Strict fail-closed semantics: any precondition / per-day /
  immutability failure aborts the run BEFORE writing the multi-day
  feature manifest. Partial per-day feature Parquets that may have
  been written before the failure are preserved on disk (each is
  independently verifiable via its paired sidecar) but the feature
  manifest is NOT written, so the v002 feature family is not
  Stage-2-complete on failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure import (  # noqa: E402
    CROSS_DAY_TAIL_BUFFER_MS,
    FeatureLineageV002,
    build_feature_config_v002,
    build_feature_manifest_v002,
    compute_aggtrades_features_v002,
    derive_v002_feature_manifest_path,
    derive_v002_feature_parquet_path,
    feature_dtypes_v002,
    slice_prior_day_tail,
    write_feature_dataset_v002,
)
from prometheus.research.microstructure.features_io import (  # noqa: E402
    atomic_write_feature_manifest,
    write_feature_sha256_sidecar,
)

# ---------------------------------------------------------------------------
# Locked precondition SHAs (Phase 4bm-G §5 lineage table)
# ---------------------------------------------------------------------------

LOCKED_PRECONDITIONS: dict[str, tuple[str, str]] = {
    "v002_derived_manifest": (
        "data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json",
        "01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a",
    ),
    "v002_derived_manifest_sidecar": (
        "data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256",
        "d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888",
    ),
    "v002_raw_manifest": (
        "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json",
        "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485",
    ),
    "v002_acquisition_log": (
        "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json",
        "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314",
    ),
    "phase_4bl_d_r_raw_gate_report": (
        "data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json",
        "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46",
    ),
    "phase_4bl_e_raw_successor_state": (
        "data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json",
        "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d",
    ),
    "phase_4bm_d_gate_report": (
        "data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json",
        "3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a",
    ),
    "phase_4bm_d_gate_report_sidecar": (
        "data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json.sha256",
        "8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711",
    ),
    "phase_4bm_f_successor_state": (
        "data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json",
        "72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9",
    ),
    "phase_4bm_f_successor_state_sidecar": (
        "data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json.sha256",
        "1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97",
    ),
}

EXPECTED_DATE_START = "2024-12-01"
EXPECTED_DATE_END = "2025-02-28"
EXPECTED_DATE_COUNT = 90
EXPECTED_SYMBOL = "BTCUSDT"
EXPECTED_TOTAL_EVENT_COUNT = 155_153_449


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class Phase4bmHError(RuntimeError):
    """Raised when the Phase 4bm-H orchestrator fails closed."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stream_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _utc_day_start_ms(utc_date: str) -> int:
    return int(
        datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000
    )


def _build_date_list() -> list[str]:
    start = date.fromisoformat(EXPECTED_DATE_START)
    end = date.fromisoformat(EXPECTED_DATE_END)
    out = []
    cur = start
    while cur <= end:
        out.append(cur.isoformat())
        cur = cur + timedelta(days=1)
    if len(out) != EXPECTED_DATE_COUNT:
        raise Phase4bmHError(
            f"expected {EXPECTED_DATE_COUNT} dates; computed {len(out)}"
        )
    return out


@dataclass(frozen=True)
class PerDayResolved:
    """Resolved per-day source paths and SHAs from the v002 derived manifest."""

    utc_date: str
    parquet_path: Path
    parquet_sha256: str
    expected_event_count: int


def _verify_preconditions(repo_root: Path) -> dict[str, Path]:
    """Recompute SHA256 for every locked precondition; fail closed on mismatch."""
    resolved: dict[str, Path] = {}
    for label, (rel, expected_sha) in LOCKED_PRECONDITIONS.items():
        p = repo_root / rel
        if not p.exists():
            raise Phase4bmHError(f"locked precondition missing: {label} -> {p}")
        actual = _stream_sha256(p)
        if actual != expected_sha:
            raise Phase4bmHError(
                f"locked precondition SHA mismatch for {label}: "
                f"expected {expected_sha} got {actual} ({p})"
            )
        resolved[label] = p
    return resolved


def _load_per_day_inventory(
    manifest_path: Path, repo_root: Path
) -> list[PerDayResolved]:
    """Read v002 derived multi-day index manifest and resolve per-day paths."""
    data: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    pf: list[dict[str, Any]] = data["per_file_inventory"]
    if len(pf) != EXPECTED_DATE_COUNT:
        raise Phase4bmHError(
            f"per_file_inventory length {len(pf)} != {EXPECTED_DATE_COUNT}"
        )
    if data["date_count"] != EXPECTED_DATE_COUNT:
        raise Phase4bmHError(
            f"manifest date_count {data['date_count']} != {EXPECTED_DATE_COUNT}"
        )
    if data["date_start"] != EXPECTED_DATE_START:
        raise Phase4bmHError(
            f"manifest date_start {data['date_start']} != {EXPECTED_DATE_START}"
        )
    if data["date_end"] != EXPECTED_DATE_END:
        raise Phase4bmHError(
            f"manifest date_end {data['date_end']} != {EXPECTED_DATE_END}"
        )
    if data["total_event_count"] != EXPECTED_TOTAL_EVENT_COUNT:
        raise Phase4bmHError(
            f"manifest total_event_count {data['total_event_count']} "
            f"!= {EXPECTED_TOTAL_EVENT_COUNT}"
        )
    if data["symbol_list"] != [EXPECTED_SYMBOL]:
        raise Phase4bmHError(
            f"manifest symbol_list {data['symbol_list']} != [{EXPECTED_SYMBOL!r}]"
        )
    if data["research_eligible"] is not False:
        raise Phase4bmHError(
            "v002 derived manifest must carry research_eligible=False"
        )
    if data["eligibility_gate_status"] != "pending":
        raise Phase4bmHError(
            "v002 derived manifest must carry eligibility_gate_status='pending'"
        )
    expected_dates = _build_date_list()
    out: list[PerDayResolved] = []
    for entry, expected_date in zip(pf, expected_dates, strict=True):
        if entry["date"] != expected_date:
            raise Phase4bmHError(
                f"per_file_inventory date {entry['date']} != {expected_date}"
            )
        if entry["symbol"] != EXPECTED_SYMBOL:
            raise Phase4bmHError(
                f"per_file_inventory symbol {entry['symbol']} != {EXPECTED_SYMBOL}"
            )
        # local_parquet_path is recorded relative to data/ (so it begins with
        # "microstructure/normalized/..."). Resolve under repo_root/data/.
        parquet_path = repo_root / "data" / entry["local_parquet_path"]
        if not parquet_path.exists():
            raise Phase4bmHError(
                f"per-day parquet missing for {entry['date']}: {parquet_path}"
            )
        actual_sha = _stream_sha256(parquet_path)
        if actual_sha != entry["parquet_sha256"]:
            raise Phase4bmHError(
                f"per-day parquet SHA mismatch for {entry['date']}: "
                f"expected {entry['parquet_sha256']} got {actual_sha}"
            )
        out.append(
            PerDayResolved(
                utc_date=entry["date"],
                parquet_path=parquet_path,
                parquet_sha256=entry["parquet_sha256"],
                expected_event_count=int(entry["event_count"]),
            )
        )
    return out


def _verify_no_target_outputs_exist(
    *, manifest_root: Path, features_root: Path, per_day: list[PerDayResolved]
) -> tuple[Path, Path]:
    """Refuse-to-overwrite check for the v002 feature manifest + per-day outputs."""
    manifest_path = derive_v002_feature_manifest_path(manifests_root=manifest_root)
    manifest_sidecar = manifest_path.with_suffix(manifest_path.suffix + ".sha256")
    for label, p in (
        ("v002 feature manifest", manifest_path),
        ("v002 feature manifest sidecar", manifest_sidecar),
    ):
        if p.exists():
            raise Phase4bmHError(
                f"refuse-to-overwrite: {label} already exists at {p}"
            )
    for entry in per_day:
        out_p = derive_v002_feature_parquet_path(
            features_root=features_root,
            symbol=EXPECTED_SYMBOL,
            utc_date=entry.utc_date,
        )
        side_p = out_p.with_suffix(out_p.suffix + ".sha256")
        if out_p.exists():
            raise Phase4bmHError(
                f"refuse-to-overwrite: v002 feature parquet already exists at {out_p}"
            )
        if side_p.exists():
            raise Phase4bmHError(
                f"refuse-to-overwrite: v002 feature sidecar already exists at {side_p}"
            )
    return manifest_path, manifest_sidecar


# ---------------------------------------------------------------------------
# Per-day computation
# ---------------------------------------------------------------------------


def _compute_one_day(
    *,
    day: PerDayResolved,
    prior_day: PerDayResolved | None,
    features_root: Path,
    config: Any,
    lineage_const: Mapping[str, str],
) -> dict[str, Any]:
    """Compute one day's v002 feature Parquet + sidecar; return per-day record."""
    import pyarrow.parquet as pq

    current_table = pq.read_table(day.parquet_path)
    if current_table.num_rows != day.expected_event_count:
        raise Phase4bmHError(
            f"row_count mismatch for {day.utc_date}: "
            f"parquet={current_table.num_rows} manifest={day.expected_event_count}"
        )
    prior_tail = None
    if prior_day is not None:
        prior_table = pq.read_table(prior_day.parquet_path)
        cur_start_ms = _utc_day_start_ms(day.utc_date)
        prior_tail = slice_prior_day_tail(
            prior_table,
            current_day_start_ms=cur_start_ms,
            tail_buffer_ms=CROSS_DAY_TAIL_BUFFER_MS,
        )
    lineage = FeatureLineageV002(
        source_normalized_parquet_per_day_sha256=day.parquet_sha256,
        source_normalized_manifest_sha256=lineage_const["normalized_manifest_sha256"],
        source_successor_state_sha256=lineage_const["successor_state_sha256"],
        source_phase_4bm_d_gate_report_sha256=lineage_const[
            "phase_4bm_d_gate_report_sha256"
        ],
        feature_config_hash=config.feature_config_hash,
    )
    feature_table = compute_aggtrades_features_v002(
        current_day_table=current_table,
        prior_day_tail_table=prior_tail,
        config=config,
        lineage=lineage,
    )
    out_path = derive_v002_feature_parquet_path(
        features_root=features_root,
        symbol=EXPECTED_SYMBOL,
        utc_date=day.utc_date,
    )
    write_result = write_feature_dataset_v002(
        table=feature_table,
        output_path=out_path,
        write_sha256_sidecar=True,
    )
    rel_parquet = out_path.relative_to(features_root.parent.parent).as_posix()
    rel_sidecar = write_result.sidecar_path.relative_to(
        features_root.parent.parent
    ).as_posix()
    return {
        "utc_date": day.utc_date,
        "feature_parquet_path": rel_parquet,
        "feature_parquet_sha256": write_result.parquet_sha256,
        "feature_parquet_size_bytes": write_result.parquet_size_bytes,
        "row_count": write_result.row_count,
        "feature_sidecar_path": rel_sidecar,
        "feature_sidecar_sha256": write_result.sidecar_sha256,
        "feature_sidecar_size_bytes": write_result.sidecar_size_bytes,
        "source_normalized_parquet_per_day_sha256": day.parquet_sha256,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4bm-H multi-day v002 aggTrades feature computation orchestrator"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=_REPO_ROOT,
        help="repository root (defaults to script's parent)",
    )
    parser.add_argument(
        "--code-commit-sha",
        type=str,
        default="unknown",
        help="40-char lowercase hex code commit SHA (or 'unknown')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="run preconditions and exit before any compute / write",
    )
    args = parser.parse_args(argv)
    repo_root: Path = args.repo_root.resolve()
    if not (repo_root / "src" / "prometheus").exists():
        raise Phase4bmHError(
            f"repo_root does not look like the Prometheus repo: {repo_root}"
        )

    print(f"[phase-4bm-h] repo_root         : {repo_root}", flush=True)
    print(f"[phase-4bm-h] code_commit_sha   : {args.code_commit_sha}", flush=True)
    print(f"[phase-4bm-h] dry_run           : {args.dry_run}", flush=True)

    # --- 1. Verify all locked precondition SHAs --------------------------
    print("[phase-4bm-h] verifying locked precondition SHAs...", flush=True)
    resolved = _verify_preconditions(repo_root)
    print(
        f"[phase-4bm-h] all {len(resolved)} preconditions OK", flush=True
    )

    derived_manifest_path = resolved["v002_derived_manifest"]
    per_day = _load_per_day_inventory(derived_manifest_path, repo_root)
    print(
        f"[phase-4bm-h] resolved {len(per_day)} per-day source parquets", flush=True
    )

    # --- 2. Verify no target outputs exist -------------------------------
    manifest_root = repo_root / "data" / "microstructure" / "manifests"
    features_root = repo_root / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True, exist_ok=True)
    feat_manifest_path, feat_manifest_sidecar = _verify_no_target_outputs_exist(
        manifest_root=manifest_root, features_root=features_root, per_day=per_day
    )
    print("[phase-4bm-h] no target outputs exist (refuse-to-overwrite OK)", flush=True)

    if args.dry_run:
        print("[phase-4bm-h] dry-run complete; exiting before compute / write", flush=True)
        return 0

    # --- 3. Build feature config with deterministic hash -----------------
    config = build_feature_config_v002(
        source_normalized_manifest_path=str(
            derived_manifest_path.relative_to(repo_root).as_posix()
        ),
        source_successor_state_path=str(
            resolved["phase_4bm_f_successor_state"].relative_to(repo_root).as_posix()
        ),
        output_feature_manifest_path=str(
            feat_manifest_path.relative_to(repo_root).as_posix()
        ),
        output_feature_root_dir=str(features_root.relative_to(repo_root).as_posix()),
        code_commit_sha=args.code_commit_sha,
    )
    print(
        f"[phase-4bm-h] feature_config_hash: {config.feature_config_hash}", flush=True
    )

    lineage_const = {
        "normalized_manifest_sha256": LOCKED_PRECONDITIONS["v002_derived_manifest"][1],
        "successor_state_sha256": LOCKED_PRECONDITIONS["phase_4bm_f_successor_state"][1],
        "phase_4bm_d_gate_report_sha256": LOCKED_PRECONDITIONS[
            "phase_4bm_d_gate_report"
        ][1],
    }

    # --- 4. Per-day computation -----------------------------------------
    t_start = time.time()
    per_day_outputs: list[dict[str, Any]] = []
    total_row_count = 0
    for i, day in enumerate(per_day):
        prior_day = per_day[i - 1] if i > 0 else None
        t0 = time.time()
        record = _compute_one_day(
            day=day,
            prior_day=prior_day,
            features_root=features_root,
            config=config,
            lineage_const=lineage_const,
        )
        per_day_outputs.append(record)
        total_row_count += int(record["row_count"])
        elapsed = time.time() - t0
        sha_prefix = record["feature_parquet_sha256"][:12]
        print(
            f"[phase-4bm-h] day {i + 1:02d}/{EXPECTED_DATE_COUNT} {day.utc_date} "
            f"rows={record['row_count']:>8d} parquet_sha={sha_prefix}... "
            f"({elapsed:.1f}s)",
            flush=True,
        )

    if total_row_count != EXPECTED_TOTAL_EVENT_COUNT:
        raise Phase4bmHError(
            f"total feature row count {total_row_count} != "
            f"expected {EXPECTED_TOTAL_EVENT_COUNT}"
        )

    # --- 5. Build and write feature manifest -----------------------------
    feat_manifest = build_feature_manifest_v002(
        symbol=EXPECTED_SYMBOL,
        input_date_start=EXPECTED_DATE_START,
        input_date_end=EXPECTED_DATE_END,
        date_count=EXPECTED_DATE_COUNT,
        expected_event_count=EXPECTED_TOTAL_EVENT_COUNT,
        actual_feature_row_count=total_row_count,
        per_day_outputs=per_day_outputs,
        feature_dtypes=feature_dtypes_v002(),
        feature_config_hash=config.feature_config_hash,
        source_normalized_manifest_path=str(
            derived_manifest_path.relative_to(repo_root).as_posix()
        ),
        source_normalized_manifest_sha256=LOCKED_PRECONDITIONS["v002_derived_manifest"][
            1
        ],
        source_successor_state_path=str(
            resolved["phase_4bm_f_successor_state"].relative_to(repo_root).as_posix()
        ),
        source_successor_state_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_f_successor_state"
        ][1],
        source_phase_4bm_d_gate_report_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_d_gate_report"
        ][1],
        source_phase_4bm_f_successor_state_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_f_successor_state"
        ][1],
        source_phase_4bl_d_r_raw_gate_report_sha256=LOCKED_PRECONDITIONS[
            "phase_4bl_d_r_raw_gate_report"
        ][1],
        source_phase_4bl_e_raw_successor_state_sha256=LOCKED_PRECONDITIONS[
            "phase_4bl_e_raw_successor_state"
        ][1],
        source_v002_raw_manifest_sha256=LOCKED_PRECONDITIONS["v002_raw_manifest"][1],
        source_v002_acquisition_log_sha256=LOCKED_PRECONDITIONS["v002_acquisition_log"][
            1
        ],
        code_commit_sha=args.code_commit_sha,
        created_at_unix_ms=int(time.time() * 1000),
    )

    manifest_sha, manifest_size = atomic_write_feature_manifest(
        feat_manifest_path, feat_manifest, refuse_overwrite=True
    )
    print(
        f"[phase-4bm-h] feature manifest written: sha={manifest_sha} size={manifest_size}",
        flush=True,
    )

    sidecar_sha, sidecar_size = write_feature_sha256_sidecar(
        feat_manifest_sidecar,
        target_filename=feat_manifest_path.name,
        sha256_hex=manifest_sha,
        refuse_overwrite=True,
    )
    print(
        f"[phase-4bm-h] feature manifest sidecar written: sha={sidecar_sha} size={sidecar_size}",
        flush=True,
    )

    # --- 6. Post-write immutability re-hash ------------------------------
    print("[phase-4bm-h] verifying upstream immutability...", flush=True)
    for label, (rel, expected_sha) in LOCKED_PRECONDITIONS.items():
        p = repo_root / rel
        actual = _stream_sha256(p)
        if actual != expected_sha:
            raise Phase4bmHError(
                f"POST-WRITE upstream immutability violation for {label}: "
                f"expected {expected_sha} got {actual} ({p})"
            )
    for day in per_day:
        actual = _stream_sha256(day.parquet_path)
        if actual != day.parquet_sha256:
            raise Phase4bmHError(
                f"POST-WRITE per-day normalized parquet mutated for {day.utc_date}: "
                f"expected {day.parquet_sha256} got {actual}"
            )
    elapsed = time.time() - t_start
    print(
        f"[phase-4bm-h] DONE total_row_count={total_row_count} "
        f"feature_manifest_sha256={manifest_sha} "
        f"feature_manifest_sidecar_sha256={sidecar_sha} "
        f"elapsed={elapsed:.1f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - script entry
    try:
        sys.exit(main())
    except Phase4bmHError as exc:
        print(f"[phase-4bm-h] FAIL_CLOSED: {exc}", file=sys.stderr, flush=True)
        sys.exit(2)
