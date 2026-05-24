"""Phase 4bm-O — Multi-Day v002 aggTrades Label Computation orchestrator.

Standalone orchestrator authorised by the Phase 4bm-O authorization
prompt and the Phase 4bm-N label schema finalization memo
(``docs/00-meta/implementation-reports/2026-05-18_phase-4bm-n_multi-day-v002-label-schema-finalization-memo.md``).

This script computes the v002 multi-day label family
``microstructure_labels_aggtrades_v001 @ v002`` from:

- the v002 multi-day feature manifest + 90 v002 per-day feature
  parquets (Phase 4bm-H output; Phase 4bm-I structural QA PASS;
  Phase 4bm-J FEATURE_GATE_PASS; Phase 4bm-L Stage-5 admissible);
- the v002 derived multi-day index manifest + 90 v002 per-day
  normalized parquets (Phase 4bm-B output; Phase 4bm-D / 4bm-F PASS).

The script:

- verifies all upstream lineage SHAs match the Phase 4bm-N recorded
  values before writing any output (fail closed on any mismatch);
- verifies no target v002 label artefact already exists (refuse-to-
  overwrite policy);
- computes ``envelope_terminal_unix_ms`` as the maximum
  ``source_transact_time_ms`` across the entire 90-day v002 envelope;
- runs the v002 label kernel day-by-day with cross-day reference
  resolution into the next day's normalized parquet (bounded by the
  envelope-terminal timestamp);
- writes each per-day v002 label Parquet + canonical Phase 4bb-F
  sidecar atomically;
- builds and writes the multi-day v002 label manifest + canonical
  Phase 4bb-F sidecar atomically;
- re-hashes every upstream artefact AFTER all writes to confirm
  byte-identical immutability (Phase 4aw / 4bm-N fail-closed
  guarantee).

This script is intentionally narrow:

- Python standard library only (``hashlib``, ``json``, ``argparse``,
  ``os``, ``contextlib``, ``time``, ``datetime``, ``sys``, ``pathlib``)
  plus pyarrow plus the v001/v002 microstructure modules.
- NO network access (no ``urllib``, no ``requests``, no ``httpx``,
  no ``aiohttp``, no ``websockets``, no ``socket``, no ``binance``).
- NO credentials, no ``.env`` reads, no ``.mcp.json`` reads, no MCP,
  no Graphify.
- NO modification of any source artefact (v002 feature manifest +
  sidecar, 90 v002 per-day feature parquets + sidecars, Phase 4bm-L
  successor-state, Phase 4bm-J gate report, v002 derived multi-day
  index manifest, 90 v002 normalized parquets, Phase 4bm-F successor-
  state, Phase 4bm-D gate report, v002 raw manifest, v002 acquisition
  log, Phase 4bl-E raw successor-state, Phase 4bl-D-R raw gate report,
  prior v001 label artefacts).
- Refuses to overwrite an existing finalised output file.
- Atomic write-then-rename via ``os.replace`` and ``tempfile.mkstemp``.
- Pre/post SHA256 immutability check across all governance artefacts
  plus all 90 per-day feature parquets plus all 90 per-day normalized
  parquets.
- Strict fail-closed semantics: any precondition / per-day /
  immutability failure aborts the run BEFORE writing the label
  manifest. Partial per-day label Parquets that may have been written
  before the failure are preserved on disk (each is independently
  verifiable via its paired sidecar) but the label manifest is NOT
  written, so the v002 label family is not Stage-1-complete on
  failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure import (  # noqa: E402
    LABEL_DATE_COUNT_V002,
    LABEL_EXPECTED_ROW_COUNT_V002,
    LABEL_HORIZONS_V002,
    LABEL_SYMBOL_V002,
    LABEL_UTC_DATE_END_V002,
    LABEL_UTC_DATE_START_V002,
    LabelLineageV002,
    LabelMultiDaySummaryV002,
    build_label_config_hash_v002,
    build_label_manifest_v002,
    compute_aggtrade_labels_v002_for_day,
    derive_v002_label_manifest_path,
    derive_v002_label_parquet_path,
    load_normalized_day_ref,
    write_label_dataset_v002,
)
from prometheus.research.microstructure.labels_io import (  # noqa: E402
    atomic_write_label_manifest,
    write_label_sha256_sidecar,
)

# ---------------------------------------------------------------------------
# Locked precondition SHAs (Phase 4bm-N §11 evidence table)
# ---------------------------------------------------------------------------

LOCKED_PRECONDITIONS: dict[str, tuple[str, str]] = {
    "v002_feature_manifest": (
        "data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json",
        "512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d",
    ),
    "v002_feature_manifest_sidecar": (
        "data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json.sha256",
        "22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34",
    ),
    "phase_4bm_l_successor_state": (
        "data/microstructure/successor-state/microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json",
        "7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4",
    ),
    "phase_4bm_l_successor_state_sidecar": (
        "data/microstructure/successor-state/microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json.sha256",
        "c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98",
    ),
    "phase_4bm_j_gate_report": (
        "data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json",
        "3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242",
    ),
    "phase_4bm_j_gate_report_sidecar": (
        "data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json.sha256",
        "14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125",
    ),
    "v002_derived_manifest": (
        "data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json",
        "01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a",
    ),
    "v002_derived_manifest_sidecar": (
        "data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256",
        "d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888",
    ),
    "phase_4bm_f_derived_successor_state": (
        "data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json",
        "72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9",
    ),
    "phase_4bm_d_derived_gate_report": (
        "data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json",
        "3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a",
    ),
    "v002_raw_manifest": (
        "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json",
        "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485",
    ),
    "v002_acquisition_log": (
        "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json",
        "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314",
    ),
    "phase_4bl_e_raw_successor_state": (
        "data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json",
        "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d",
    ),
    "phase_4bl_d_r_raw_gate_report": (
        "data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json",
        "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46",
    ),
}

EXPECTED_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class Phase4bmOError(RuntimeError):
    """Raised when the Phase 4bm-O orchestrator fails closed."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stream_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_date_list() -> list[str]:
    start = date.fromisoformat(LABEL_UTC_DATE_START_V002)
    end = date.fromisoformat(LABEL_UTC_DATE_END_V002)
    out = []
    cur = start
    while cur <= end:
        out.append(cur.isoformat())
        cur = cur + timedelta(days=1)
    if len(out) != LABEL_DATE_COUNT_V002:
        raise Phase4bmOError(
            f"expected {LABEL_DATE_COUNT_V002} dates; computed {len(out)}"
        )
    return out


@dataclass(frozen=True)
class PerDayFeatureResolved:
    """Resolved per-day source paths and SHAs."""

    utc_date: str
    feature_parquet_path: Path
    feature_parquet_sha256: str
    feature_row_count: int
    normalized_parquet_path: Path
    normalized_parquet_sha256: str
    normalized_row_count: int


def _verify_preconditions(repo_root: Path) -> dict[str, Path]:
    """Recompute SHA256 for every locked precondition; fail closed on mismatch."""
    resolved: dict[str, Path] = {}
    for label, (rel, expected_sha) in LOCKED_PRECONDITIONS.items():
        p = repo_root / rel
        if not p.exists():
            raise Phase4bmOError(f"locked precondition missing: {label} -> {p}")
        actual = _stream_sha256(p)
        if actual != expected_sha:
            raise Phase4bmOError(
                f"locked precondition SHA mismatch for {label}: "
                f"expected {expected_sha} got {actual} ({p})"
            )
        resolved[label] = p
    return resolved


def _load_feature_per_day_inventory(
    *, feature_manifest_path: Path, repo_root: Path
) -> list[dict[str, Any]]:
    """Read the v002 feature manifest and return its ``per_day_outputs`` list."""
    data: dict[str, Any] = json.loads(
        feature_manifest_path.read_text(encoding="utf-8")
    )
    pdo = data.get("per_day_outputs")
    if not isinstance(pdo, list) or len(pdo) != LABEL_DATE_COUNT_V002:
        raise Phase4bmOError(
            f"v002 feature manifest per_day_outputs length "
            f"{len(pdo) if isinstance(pdo, list) else 'n/a'} "
            f"!= {LABEL_DATE_COUNT_V002}"
        )
    if data.get("feature_config_hash") != EXPECTED_FEATURE_CONFIG_HASH:
        raise Phase4bmOError(
            f"v002 feature manifest feature_config_hash "
            f"{data.get('feature_config_hash')!r} != expected "
            f"{EXPECTED_FEATURE_CONFIG_HASH!r}"
        )
    if data.get("research_eligible") is not False:
        raise Phase4bmOError(
            "v002 feature manifest must carry research_eligible=False"
        )
    if data.get("eligibility_gate_status") != "pending":
        raise Phase4bmOError(
            "v002 feature manifest must carry eligibility_gate_status='pending'"
        )
    return list(pdo)


def _load_normalized_per_day_inventory(
    *, derived_manifest_path: Path
) -> list[dict[str, Any]]:
    data: dict[str, Any] = json.loads(
        derived_manifest_path.read_text(encoding="utf-8")
    )
    pf = data.get("per_file_inventory")
    if not isinstance(pf, list) or len(pf) != LABEL_DATE_COUNT_V002:
        raise Phase4bmOError(
            f"v002 derived manifest per_file_inventory length "
            f"{len(pf) if isinstance(pf, list) else 'n/a'} "
            f"!= {LABEL_DATE_COUNT_V002}"
        )
    return list(pf)


def _resolve_per_day(
    *,
    repo_root: Path,
    feature_pdo: list[dict[str, Any]],
    normalized_pdo: list[dict[str, Any]],
) -> list[PerDayFeatureResolved]:
    """Combine per-day feature + normalized inventories into resolved records."""
    expected_dates = _build_date_list()
    out: list[PerDayFeatureResolved] = []
    for i, expected_date in enumerate(expected_dates):
        feat_entry = feature_pdo[i]
        norm_entry = normalized_pdo[i]
        if feat_entry["utc_date"] != expected_date:
            raise Phase4bmOError(
                f"feature per_day_outputs[{i}] utc_date "
                f"{feat_entry['utc_date']!r} != {expected_date!r}"
            )
        if norm_entry["date"] != expected_date:
            raise Phase4bmOError(
                f"normalized per_file_inventory[{i}] date "
                f"{norm_entry['date']!r} != {expected_date!r}"
            )
        if norm_entry["symbol"] != LABEL_SYMBOL_V002:
            raise Phase4bmOError(
                f"normalized per_file_inventory[{i}] symbol "
                f"{norm_entry['symbol']!r} != {LABEL_SYMBOL_V002!r}"
            )
        if (
            feat_entry["source_normalized_parquet_per_day_sha256"]
            != norm_entry["parquet_sha256"]
        ):
            raise Phase4bmOError(
                f"feature lineage SHA mismatch for {expected_date}: "
                f"feature_manifest source_normalized_parquet_per_day_sha256="
                f"{feat_entry['source_normalized_parquet_per_day_sha256']} "
                f"!= derived_manifest parquet_sha256={norm_entry['parquet_sha256']}"
            )
        # Feature manifest stores paths relative to data/ (Phase 4bm-H pattern):
        # "microstructure/features/..."; resolve under repo_root/data/.
        feature_parquet_path = repo_root / "data" / feat_entry["feature_parquet_path"]
        if not feature_parquet_path.exists():
            raise Phase4bmOError(
                f"v002 feature parquet missing for {expected_date}: "
                f"{feature_parquet_path}"
            )
        actual_feature_sha = _stream_sha256(feature_parquet_path)
        if actual_feature_sha != feat_entry["feature_parquet_sha256"]:
            raise Phase4bmOError(
                f"v002 feature parquet SHA mismatch for {expected_date}: "
                f"expected {feat_entry['feature_parquet_sha256']} "
                f"got {actual_feature_sha}"
            )
        normalized_parquet_path = repo_root / "data" / norm_entry["local_parquet_path"]
        if not normalized_parquet_path.exists():
            raise Phase4bmOError(
                f"v002 normalized parquet missing for {expected_date}: "
                f"{normalized_parquet_path}"
            )
        actual_norm_sha = _stream_sha256(normalized_parquet_path)
        if actual_norm_sha != norm_entry["parquet_sha256"]:
            raise Phase4bmOError(
                f"v002 normalized parquet SHA mismatch for {expected_date}: "
                f"expected {norm_entry['parquet_sha256']} got {actual_norm_sha}"
            )
        if int(feat_entry["row_count"]) != int(norm_entry["event_count"]):
            raise Phase4bmOError(
                f"per-day row_count mismatch for {expected_date}: "
                f"feature={feat_entry['row_count']} "
                f"normalized={norm_entry['event_count']}"
            )
        out.append(
            PerDayFeatureResolved(
                utc_date=expected_date,
                feature_parquet_path=feature_parquet_path,
                feature_parquet_sha256=feat_entry["feature_parquet_sha256"],
                feature_row_count=int(feat_entry["row_count"]),
                normalized_parquet_path=normalized_parquet_path,
                normalized_parquet_sha256=norm_entry["parquet_sha256"],
                normalized_row_count=int(norm_entry["event_count"]),
            )
        )
    return out


def _compute_envelope_terminal_unix_ms(
    *, normalized_pdo: list[dict[str, Any]]
) -> int:
    """Return the maximum ``last_transact_time_ms`` across the v002 envelope."""
    last_ts = [int(entry["last_transact_time_ms"]) for entry in normalized_pdo]
    if len(last_ts) != LABEL_DATE_COUNT_V002:
        raise Phase4bmOError(
            f"expected {LABEL_DATE_COUNT_V002} last_transact_time_ms entries; "
            f"got {len(last_ts)}"
        )
    envelope_terminal = max(last_ts)
    if envelope_terminal <= 0:
        raise Phase4bmOError(
            f"envelope_terminal_unix_ms must be positive (got {envelope_terminal})"
        )
    return envelope_terminal


def _verify_no_target_outputs_exist(
    *,
    manifest_root: Path,
    labels_root: Path,
    per_day: list[PerDayFeatureResolved],
) -> tuple[Path, Path]:
    """Refuse-to-overwrite check for the v002 label manifest + per-day outputs."""
    manifest_path = derive_v002_label_manifest_path(manifests_root=manifest_root)
    manifest_sidecar = manifest_path.with_suffix(manifest_path.suffix + ".sha256")
    for lbl, p in (
        ("v002 label manifest", manifest_path),
        ("v002 label manifest sidecar", manifest_sidecar),
    ):
        if p.exists():
            raise Phase4bmOError(
                f"refuse-to-overwrite: {lbl} already exists at {p}"
            )
    for entry in per_day:
        out_p = derive_v002_label_parquet_path(
            labels_root=labels_root,
            symbol=LABEL_SYMBOL_V002,
            utc_date=entry.utc_date,
        )
        side_p = out_p.with_suffix(out_p.suffix + ".sha256")
        if out_p.exists():
            raise Phase4bmOError(
                f"refuse-to-overwrite: v002 label parquet already exists at {out_p}"
            )
        if side_p.exists():
            raise Phase4bmOError(
                f"refuse-to-overwrite: v002 label sidecar already exists at {side_p}"
            )
    return manifest_path, manifest_sidecar


def _read_feature_table_minimal(parquet_path: Path) -> Any:
    """Read only the four feature columns the label kernel needs."""
    import pyarrow.parquet as pq

    return pq.read_table(
        parquet_path,
        columns=[
            "row_index",
            "agg_trade_id",
            "feature_timestamp_ms",
            "source_transact_time_ms",
        ],
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:  # noqa: C901
    parser = argparse.ArgumentParser(
        description=(
            "Phase 4bm-O multi-day v002 aggTrades label computation orchestrator"
        )
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
        raise Phase4bmOError(
            f"repo_root does not look like the Prometheus repo: {repo_root}"
        )

    print(f"[phase-4bm-o] repo_root         : {repo_root}", flush=True)
    print(f"[phase-4bm-o] code_commit_sha   : {args.code_commit_sha}", flush=True)
    print(f"[phase-4bm-o] dry_run           : {args.dry_run}", flush=True)

    # --- 1. Verify all locked precondition SHAs --------------------------
    print("[phase-4bm-o] verifying locked precondition SHAs...", flush=True)
    resolved = _verify_preconditions(repo_root)
    print(
        f"[phase-4bm-o] all {len(resolved)} preconditions OK", flush=True
    )

    feature_pdo = _load_feature_per_day_inventory(
        feature_manifest_path=resolved["v002_feature_manifest"],
        repo_root=repo_root,
    )
    normalized_pdo = _load_normalized_per_day_inventory(
        derived_manifest_path=resolved["v002_derived_manifest"]
    )
    per_day = _resolve_per_day(
        repo_root=repo_root,
        feature_pdo=feature_pdo,
        normalized_pdo=normalized_pdo,
    )
    print(
        f"[phase-4bm-o] resolved {len(per_day)} per-day "
        f"(feature + normalized) parquets",
        flush=True,
    )

    envelope_terminal_unix_ms = _compute_envelope_terminal_unix_ms(
        normalized_pdo=normalized_pdo
    )
    envelope_terminal_utc = (
        datetime.fromtimestamp(envelope_terminal_unix_ms / 1000, tz=UTC).isoformat()
    )
    print(
        f"[phase-4bm-o] envelope_terminal_unix_ms = {envelope_terminal_unix_ms} "
        f"({envelope_terminal_utc})",
        flush=True,
    )

    # --- 2. Verify no target outputs exist -------------------------------
    manifest_root = repo_root / "data" / "microstructure" / "manifests"
    labels_root = repo_root / "data" / "microstructure" / "labels"
    labels_root.mkdir(parents=True, exist_ok=True)
    label_manifest_path, label_manifest_sidecar = _verify_no_target_outputs_exist(
        manifest_root=manifest_root,
        labels_root=labels_root,
        per_day=per_day,
    )
    print(
        "[phase-4bm-o] no target outputs exist (refuse-to-overwrite OK)",
        flush=True,
    )

    if args.dry_run:
        print(
            "[phase-4bm-o] dry-run complete; exiting before compute / write",
            flush=True,
        )
        return 0

    # --- 3. Build label_config_hash --------------------------------------
    label_config_hash = build_label_config_hash_v002(
        source_feature_manifest_sha256=LOCKED_PRECONDITIONS["v002_feature_manifest"][1],
        source_feature_successor_state_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_l_successor_state"
        ][1],
        source_phase_4bm_j_gate_report_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_j_gate_report"
        ][1],
        source_normalized_manifest_sha256=LOCKED_PRECONDITIONS["v002_derived_manifest"][1],
        source_raw_manifest_sha256=LOCKED_PRECONDITIONS["v002_raw_manifest"][1],
        feature_config_hash=EXPECTED_FEATURE_CONFIG_HASH,
    )
    print(
        f"[phase-4bm-o] label_config_hash: {label_config_hash}", flush=True
    )

    # --- 4. Per-day computation with rolling current/next day normalized refs
    t_start = time.time()
    per_day_outputs: list[dict[str, Any]] = []
    multi_summary = LabelMultiDaySummaryV002()
    current_norm_ref = None
    next_norm_ref = None
    for i, day in enumerate(per_day):
        t0 = time.time()
        # Rolling load: next becomes current; load the day after current as
        # the new next. For day i, we need current_day and next_day (if i<89).
        if i == 0:
            current_norm_ref = load_normalized_day_ref(
                parquet_path=day.normalized_parquet_path
            )
        else:
            current_norm_ref = next_norm_ref
        if i + 1 < len(per_day):
            next_norm_ref = load_normalized_day_ref(
                parquet_path=per_day[i + 1].normalized_parquet_path
            )
        else:
            next_norm_ref = None

        feature_table = _read_feature_table_minimal(day.feature_parquet_path)
        if feature_table.num_rows != day.feature_row_count:
            raise Phase4bmOError(
                f"feature parquet row_count mismatch for {day.utc_date}: "
                f"parquet={feature_table.num_rows} "
                f"manifest={day.feature_row_count}"
            )

        lineage = LabelLineageV002(
            source_feature_manifest_sha256=LOCKED_PRECONDITIONS[
                "v002_feature_manifest"
            ][1],
            source_feature_parquet_sha256=day.feature_parquet_sha256,
            source_feature_successor_state_sha256=LOCKED_PRECONDITIONS[
                "phase_4bm_l_successor_state"
            ][1],
            source_phase_4bm_j_gate_report_sha256=LOCKED_PRECONDITIONS[
                "phase_4bm_j_gate_report"
            ][1],
            source_normalized_manifest_sha256=LOCKED_PRECONDITIONS[
                "v002_derived_manifest"
            ][1],
            source_raw_manifest_sha256=LOCKED_PRECONDITIONS["v002_raw_manifest"][1],
            label_config_hash=label_config_hash,
        )

        assert current_norm_ref is not None  # narrow for mypy
        label_table, day_summary = compute_aggtrade_labels_v002_for_day(
            feature_table=feature_table,
            current_day=current_norm_ref,
            next_day=next_norm_ref,
            envelope_terminal_unix_ms=envelope_terminal_unix_ms,
            symbol=LABEL_SYMBOL_V002,
            utc_date=day.utc_date,
            lineage=lineage,
        )
        multi_summary.absorb(day_summary)

        out_path = derive_v002_label_parquet_path(
            labels_root=labels_root,
            symbol=LABEL_SYMBOL_V002,
            utc_date=day.utc_date,
        )
        (
            written_path,
            parquet_sha,
            parquet_size,
            sidecar_path,
            sidecar_sha,
        ) = write_label_dataset_v002(
            table=label_table,
            output_path=out_path,
            write_sha256_sidecar=True,
        )
        assert sidecar_path is not None and sidecar_sha is not None
        rel_parquet = written_path.relative_to(repo_root / "data").as_posix()
        rel_sidecar = sidecar_path.relative_to(repo_root / "data").as_posix()
        sidecar_size = sidecar_path.stat().st_size
        per_day_outputs.append(
            {
                "utc_date": day.utc_date,
                "path": rel_parquet,
                "sha256": parquet_sha,
                "sidecar_path": rel_sidecar,
                "sidecar_sha256": sidecar_sha,
                "byte_size": int(parquet_size),
                "sidecar_byte_size": int(sidecar_size),
                "row_count": day_summary.row_count,
                "per_horizon_censored_counts": dict(day_summary.censored_per_horizon),
                "invalid_price_row_count": day_summary.invalid_price_row_count,
                "source_feature_parquet_sha256": day.feature_parquet_sha256,
            }
        )
        elapsed = time.time() - t0
        print(
            f"[phase-4bm-o] day {i + 1:02d}/{LABEL_DATE_COUNT_V002} {day.utc_date} "
            f"rows={day_summary.row_count:>8d} "
            f"censored_60s={day_summary.censored_per_horizon['60s']:>5d} "
            f"parquet_sha={parquet_sha[:12]}... ({elapsed:.1f}s)",
            flush=True,
        )

    if multi_summary.total_row_count != LABEL_EXPECTED_ROW_COUNT_V002:
        raise Phase4bmOError(
            f"total label row count {multi_summary.total_row_count} "
            f"!= expected {LABEL_EXPECTED_ROW_COUNT_V002}"
        )

    # --- 5. Build and write label manifest --------------------------------
    label_manifest = build_label_manifest_v002(
        symbol=LABEL_SYMBOL_V002,
        utc_date_start=LABEL_UTC_DATE_START_V002,
        utc_date_end=LABEL_UTC_DATE_END_V002,
        date_count=LABEL_DATE_COUNT_V002,
        row_count=multi_summary.total_row_count,
        per_day_outputs=per_day_outputs,
        label_config_hash=label_config_hash,
        feature_config_hash=EXPECTED_FEATURE_CONFIG_HASH,
        envelope_terminal_unix_ms=envelope_terminal_unix_ms,
        invalid_price_row_count=multi_summary.total_invalid_price_row_count,
        censored_per_horizon=multi_summary.censored_per_horizon,
        source_feature_manifest_sha256=LOCKED_PRECONDITIONS["v002_feature_manifest"][1],
        source_feature_manifest_sidecar_sha256=LOCKED_PRECONDITIONS[
            "v002_feature_manifest_sidecar"
        ][1],
        source_feature_successor_state_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_l_successor_state"
        ][1],
        source_feature_successor_state_sidecar_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_l_successor_state_sidecar"
        ][1],
        source_phase_4bm_j_gate_report_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_j_gate_report"
        ][1],
        source_phase_4bm_j_gate_sidecar_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_j_gate_report_sidecar"
        ][1],
        source_normalized_manifest_sha256=LOCKED_PRECONDITIONS["v002_derived_manifest"][
            1
        ],
        source_normalized_manifest_sidecar_sha256=LOCKED_PRECONDITIONS[
            "v002_derived_manifest_sidecar"
        ][1],
        source_phase_4bm_f_derived_successor_state_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_f_derived_successor_state"
        ][1],
        source_phase_4bm_d_derived_gate_report_sha256=LOCKED_PRECONDITIONS[
            "phase_4bm_d_derived_gate_report"
        ][1],
        source_raw_manifest_sha256=LOCKED_PRECONDITIONS["v002_raw_manifest"][1],
        source_acquisition_log_sha256=LOCKED_PRECONDITIONS["v002_acquisition_log"][1],
        source_phase_4bl_e_raw_successor_state_sha256=LOCKED_PRECONDITIONS[
            "phase_4bl_e_raw_successor_state"
        ][1],
        source_phase_4bl_d_r_raw_gate_report_sha256=LOCKED_PRECONDITIONS[
            "phase_4bl_d_r_raw_gate_report"
        ][1],
        code_commit_sha=args.code_commit_sha,
        created_at_unix_ms=int(time.time() * 1000),
    )

    manifest_sha, manifest_size = atomic_write_label_manifest(
        label_manifest_path, label_manifest, refuse_overwrite=True
    )
    print(
        f"[phase-4bm-o] label manifest written: "
        f"sha={manifest_sha} size={manifest_size}",
        flush=True,
    )

    sidecar_sha, sidecar_size = write_label_sha256_sidecar(
        label_manifest_sidecar,
        target_filename=label_manifest_path.name,
        sha256_hex=manifest_sha,
        refuse_overwrite=True,
    )
    print(
        f"[phase-4bm-o] label manifest sidecar written: "
        f"sha={sidecar_sha} size={sidecar_size}",
        flush=True,
    )

    # --- 6. Post-write immutability re-hash ------------------------------
    print("[phase-4bm-o] verifying upstream immutability...", flush=True)
    for label, (rel, expected_sha) in LOCKED_PRECONDITIONS.items():
        p = repo_root / rel
        actual = _stream_sha256(p)
        if actual != expected_sha:
            raise Phase4bmOError(
                f"POST-WRITE upstream immutability violation for {label}: "
                f"expected {expected_sha} got {actual} ({p})"
            )
    for day in per_day:
        actual_feature = _stream_sha256(day.feature_parquet_path)
        if actual_feature != day.feature_parquet_sha256:
            raise Phase4bmOError(
                f"POST-WRITE per-day feature parquet mutated for {day.utc_date}: "
                f"expected {day.feature_parquet_sha256} got {actual_feature}"
            )
        actual_norm = _stream_sha256(day.normalized_parquet_path)
        if actual_norm != day.normalized_parquet_sha256:
            raise Phase4bmOError(
                f"POST-WRITE per-day normalized parquet mutated for {day.utc_date}: "
                f"expected {day.normalized_parquet_sha256} got {actual_norm}"
            )
    elapsed = time.time() - t_start

    censored_summary_parts = [
        f"{h}={multi_summary.censored_per_horizon[h]}" for h in LABEL_HORIZONS_V002
    ]
    print(
        f"[phase-4bm-o] DONE total_row_count={multi_summary.total_row_count} "
        f"invalid_price_row_count={multi_summary.total_invalid_price_row_count} "
        f"censored=({', '.join(censored_summary_parts)}) "
        f"label_manifest_sha256={manifest_sha} "
        f"label_manifest_sidecar_sha256={sidecar_sha} "
        f"label_config_hash={label_config_hash} "
        f"envelope_terminal_unix_ms={envelope_terminal_unix_ms} "
        f"elapsed={elapsed:.1f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - script entry
    try:
        sys.exit(main())
    except Phase4bmOError as exc:
        print(f"[phase-4bm-o] FAIL_CLOSED: {exc}", file=sys.stderr, flush=True)
        sys.exit(2)
