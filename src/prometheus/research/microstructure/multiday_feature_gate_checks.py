"""Phase 4bm-J multi-day v002 feature-family eligibility gate check suite.

Implements the deterministic, offline, fail-closed check suite for the
v002 multi-day feature family ``microstructure_features_aggtrades_v001
@ v002`` produced by Phase 4bm-H and structurally QA-passed by Phase
4bm-I. Checks are grouped A..G per the Phase 4bm-J authorization
prompt:

- A. Locked preconditions (lineage SHAs + Phase 4bm-I verdict).
- B. Inventory / sidecar / gitignore.
- C. Schema / lineage / forbidden-substring detector.
- D. Row-count / partition / timestamp.
- E. Quality flags / cross-day boundary.
- F. Upstream immutability.
- G. Non-authorization invariants.

The suite is read-only over data/microstructure/ and never mutates any
artefact. Network and credential imports are statically forbidden by
the no-network static-import test.
"""
# ruff: noqa: E501  (Phase 4bm-J: long v002 SHA literals + lineage column names)
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

from .features_schema_v002 import (
    FEATURE_DATASET_VERSION_V002,
    FEATURE_NAMES_V002,
    FEATURE_SCHEMA_V002,
    FEATURE_SCHEMA_VERSION_V002,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002,
    LINEAGE_COLUMNS_V002,
    PHASE_4BM_E_OUTCOME_LITERAL,
)
from .multiday_feature_gate_io import (
    MultidayFeatureGateIOError,
    compute_file_sha256,
    read_json_file,
)

# Locked v002 / Phase 4bm-H expected SHAs and identity facts.
EXPECTED_FEATURE_MANIFEST_SHA = (
    "512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"
)
EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA = (
    "22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34"
)
EXPECTED_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)
EXPECTED_V002_DERIVED_MANIFEST_SHA = (
    "01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"
)
EXPECTED_V002_DERIVED_MANIFEST_SIDECAR_SHA = (
    "d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888"
)
EXPECTED_V002_RAW_MANIFEST_SHA = (
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
)
EXPECTED_V002_ACQUISITION_LOG_SHA = (
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
)
EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA = (
    "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"
)
EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA = (
    "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d"
)
EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA = (
    "3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a"
)
EXPECTED_PHASE_4BM_D_SIDECAR_SHA = (
    "8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711"
)
EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA = (
    "72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9"
)
EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SIDECAR_SHA = (
    "1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97"
)

EXPECTED_SYMBOL = "BTCUSDT"
EXPECTED_DATE_START = "2024-12-01"
EXPECTED_DATE_END = "2025-02-28"
EXPECTED_DATE_COUNT = 90
EXPECTED_TOTAL_FEATURE_ROW_COUNT = 155_153_449
EXPECTED_FEATURE_SCHEMA_COLUMN_COUNT = 62
EXPECTED_LINEAGE_COLUMN_COUNT = 17
EXPECTED_FEATURE_COLUMN_COUNT = 45

# Deterministic sample dates for deep scans (Phase 4bm-I sampled the same set).
SAMPLE_DATES: tuple[str, ...] = (
    "2024-12-01",
    "2024-12-31",
    "2025-01-15",
    "2025-01-31",
    "2025-02-15",
    "2025-02-28",
)

UTC_DAY_MS = 86_400_000


class MultidayFeatureGateCheckStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ERROR = "ERROR"


@dataclass(frozen=True)
class MultidayFeatureGateCheckResult:
    check_id: str
    group: str
    status: MultidayFeatureGateCheckStatus
    blocking: bool
    expected: str = ""
    observed: str = ""
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "group": self.group,
            "status": self.status.value,
            "blocking": bool(self.blocking),
            "expected": self.expected,
            "observed": self.observed,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class MultidayFeatureGateContext:
    """Per-run context resolved at orchestrator time."""

    repo_root: Path
    feature_manifest_path: Path
    feature_manifest_sidecar_path: Path
    features_root: Path
    derived_manifest_path: Path
    raw_manifest_path: Path
    acquisition_log_path: Path
    phase_4bl_d_r_gate_report_path: Path
    phase_4bl_e_successor_state_path: Path
    phase_4bm_d_gate_report_path: Path
    phase_4bm_d_sidecar_path: Path
    phase_4bm_f_successor_state_path: Path
    phase_4bm_f_successor_state_sidecar_path: Path
    structural_qa_phase: str = "4bm-I"
    structural_qa_verdict: str = "FEATURE_STRUCTURAL_QA_PASS"


# Internal type aliases to keep check function signatures under ruff line length.
_Ctx = MultidayFeatureGateContext
_Res = MultidayFeatureGateCheckResult


def _result(
    check_id: str,
    group: str,
    ok: bool,
    *,
    blocking: bool = True,
    expected: Any = "",
    observed: Any = "",
    detail: str = "",
) -> MultidayFeatureGateCheckResult:
    status = (
        MultidayFeatureGateCheckStatus.PASS
        if ok
        else MultidayFeatureGateCheckStatus.FAIL
    )
    return MultidayFeatureGateCheckResult(
        check_id=check_id,
        group=group,
        status=status,
        blocking=blocking,
        expected=repr(expected) if not isinstance(expected, str) else expected,
        observed=repr(observed) if not isinstance(observed, str) else observed,
        detail=detail,
    )


def _expected_dates() -> list[str]:
    return [
        (date(2024, 12, 1) + timedelta(days=i)).isoformat()
        for i in range(EXPECTED_DATE_COUNT)
    ]


def _utc_day_start_ms(d: str) -> int:
    return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000)


# ---------------------------------------------------------------------------
# Group A — Locked preconditions
# ---------------------------------------------------------------------------


def check_a1_feature_manifest_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.feature_manifest_path)
    return _result(
        "A1", "A", sha == EXPECTED_FEATURE_MANIFEST_SHA,
        expected=EXPECTED_FEATURE_MANIFEST_SHA, observed=sha,
        detail="Phase 4bm-H feature manifest SHA256 must match expected.",
    )


def check_a2_feature_manifest_sidecar_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.feature_manifest_sidecar_path)
    return _result(
        "A2", "A", sha == EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA,
        expected=EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA, observed=sha,
    )


def check_a3_feature_manifest_sidecar_canonical(ctx: _Ctx) -> _Res:
    raw = ctx.feature_manifest_sidecar_path.read_bytes()
    sha, _ = compute_file_sha256(ctx.feature_manifest_path)
    basename = ctx.feature_manifest_path.name
    expected = f"{sha}  {basename}\n".encode("ascii")
    ok = (raw == expected) and (b"\r" not in raw) and (not raw.startswith(b"\xef\xbb\xbf"))
    return _result(
        "A3", "A", ok,
        expected="canonical Phase 4bb-F format, no CRLF, no BOM",
        observed=f"len={len(raw)} bytes; equal_to_expected={raw == expected}",
    )


def check_a4_phase_4bm_d_gate_report_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_d_gate_report_path)
    return _result(
        "A4", "A", sha == EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA,
        expected=EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA, observed=sha,
    )


def check_a5_phase_4bm_d_sidecar_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_d_sidecar_path)
    return _result(
        "A5", "A", sha == EXPECTED_PHASE_4BM_D_SIDECAR_SHA,
        expected=EXPECTED_PHASE_4BM_D_SIDECAR_SHA, observed=sha,
    )


def check_a6_phase_4bm_f_successor_state_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_f_successor_state_path)
    return _result(
        "A6", "A", sha == EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA,
        expected=EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA, observed=sha,
    )


def check_a7_phase_4bm_f_successor_state_sidecar_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_f_successor_state_sidecar_path)
    return _result(
        "A7", "A", sha == EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SIDECAR_SHA,
        expected=EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SIDECAR_SHA, observed=sha,
    )


def check_a8_phase_4bl_d_r_gate_report_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bl_d_r_gate_report_path)
    return _result(
        "A8", "A", sha == EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA,
        expected=EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA, observed=sha,
    )


def check_a9_phase_4bl_e_successor_state_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bl_e_successor_state_path)
    return _result(
        "A9", "A", sha == EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA,
        expected=EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA, observed=sha,
    )


def check_a10_v002_derived_manifest_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.derived_manifest_path)
    return _result(
        "A10", "A", sha == EXPECTED_V002_DERIVED_MANIFEST_SHA,
        expected=EXPECTED_V002_DERIVED_MANIFEST_SHA, observed=sha,
    )


def check_a11_v002_raw_manifest_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.raw_manifest_path)
    return _result(
        "A11", "A", sha == EXPECTED_V002_RAW_MANIFEST_SHA,
        expected=EXPECTED_V002_RAW_MANIFEST_SHA, observed=sha,
    )


def check_a12_phase_4bm_i_verdict(ctx: _Ctx) -> _Res:
    return _result(
        "A12", "A", ctx.structural_qa_verdict == "FEATURE_STRUCTURAL_QA_PASS",
        expected="FEATURE_STRUCTURAL_QA_PASS", observed=ctx.structural_qa_verdict,
        detail="Phase 4bm-I structural QA verdict is a precondition for Phase 4bm-J.",
    )


# ---------------------------------------------------------------------------
# Group B — Inventory / sidecar / gitignore
# ---------------------------------------------------------------------------


def check_b1_feature_manifest_present(ctx: _Ctx) -> _Res:
    return _result(
        "B1", "B", ctx.feature_manifest_path.exists(),
        expected="file exists", observed=str(ctx.feature_manifest_path.exists()),
    )


def check_b2_feature_manifest_sidecar_present(ctx: _Ctx) -> _Res:
    return _result(
        "B2", "B", ctx.feature_manifest_sidecar_path.exists(),
        expected="file exists", observed=str(ctx.feature_manifest_sidecar_path.exists()),
    )


def _list_per_day_parquets(ctx: MultidayFeatureGateContext) -> list[Path]:
    return sorted((ctx.features_root / "BTCUSDT").glob("*/*/*.parquet"))


def _list_per_day_sidecars(ctx: MultidayFeatureGateContext) -> list[Path]:
    return sorted((ctx.features_root / "BTCUSDT").glob("*/*/*.parquet.sha256"))


def check_b3_feature_parquet_count(ctx: _Ctx) -> _Res:
    n = len(_list_per_day_parquets(ctx))
    return _result(
        "B3", "B", n == EXPECTED_DATE_COUNT,
        expected=str(EXPECTED_DATE_COUNT), observed=str(n),
    )


def check_b4_feature_sidecar_count(ctx: _Ctx) -> _Res:
    n = len(_list_per_day_sidecars(ctx))
    return _result(
        "B4", "B", n == EXPECTED_DATE_COUNT,
        expected=str(EXPECTED_DATE_COUNT), observed=str(n),
    )


def check_b5_date_inventory_exact(ctx: _Ctx) -> _Res:
    parquets = _list_per_day_parquets(ctx)
    dates = sorted(
        p.name.replace("BTCUSDT-features-aggtrades-", "").replace(".parquet", "")
        for p in parquets
    )
    expected = _expected_dates()
    return _result(
        "B5", "B", dates == expected,
        expected=f"{EXPECTED_DATE_COUNT} contiguous dates {EXPECTED_DATE_START}..{EXPECTED_DATE_END}",
        observed=f"first={dates[0] if dates else None} last={dates[-1] if dates else None} count={len(dates)}",
    )


def check_b6_symbol_only_BTCUSDT(ctx: _Ctx) -> _Res:
    subs = sorted(p.name for p in ctx.features_root.iterdir() if p.is_dir())
    return _result(
        "B6", "B", subs == [EXPECTED_SYMBOL],
        expected=f"['{EXPECTED_SYMBOL}']", observed=str(subs),
    )


def check_b7_per_day_outputs_length(manifest: Mapping[str, Any]) -> _Res:
    n = len(manifest.get("per_day_outputs", []))
    return _result(
        "B7", "B", n == EXPECTED_DATE_COUNT,
        expected=str(EXPECTED_DATE_COUNT), observed=str(n),
    )


def check_b8_per_day_dates_unique(manifest: Mapping[str, Any]) -> _Res:
    entries = manifest.get("per_day_outputs", [])
    unique = len({e["utc_date"] for e in entries})
    return _result(
        "B8", "B", unique == EXPECTED_DATE_COUNT,
        expected=str(EXPECTED_DATE_COUNT), observed=str(unique),
    )


def check_b9_all_sidecars_canonical(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    bad = []
    for e in manifest["per_day_outputs"]:
        sp = ctx.repo_root / "data" / e["feature_sidecar_path"]
        p = ctx.repo_root / "data" / e["feature_parquet_path"]
        raw = sp.read_bytes()
        expected_content = f"{e['feature_parquet_sha256']}  {p.name}\n".encode("ascii")
        canonical = (raw == expected_content) and (b"\r" not in raw) and (not raw.startswith(b"\xef\xbb\xbf"))
        side_sha = hashlib.sha256(raw).hexdigest()
        sha_match = side_sha == e["feature_sidecar_sha256"]
        if not (canonical and sha_match):
            bad.append((e["utc_date"], canonical, sha_match))
    return _result(
        "B9", "B", bad == [],
        expected="all 90 sidecars canonical and SHA-consistent",
        observed=f"{len(bad)} violations",
        detail=f"first few: {bad[:3]}" if bad else "",
    )


def check_b10_all_per_day_parquet_shas_match(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    bad = []
    for e in manifest["per_day_outputs"]:
        p = ctx.repo_root / "data" / e["feature_parquet_path"]
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != e["feature_parquet_sha256"]:
            bad.append((e["utc_date"], actual, e["feature_parquet_sha256"]))
    return _result(
        "B10", "B", bad == [],
        expected="all 90 per-day parquet SHA256 match manifest",
        observed=f"{len(bad)} mismatches",
    )


# ---------------------------------------------------------------------------
# Group C — Schema / lineage / forbidden-substring detector
# ---------------------------------------------------------------------------


def check_c1_manifest_feature_column_count(manifest: Mapping[str, Any]) -> _Res:
    n = len(manifest.get("feature_column_names", []))
    return _result(
        "C1", "C", n == EXPECTED_FEATURE_SCHEMA_COLUMN_COUNT,
        expected=str(EXPECTED_FEATURE_SCHEMA_COLUMN_COUNT), observed=str(n),
    )


def check_c2_manifest_feature_column_names_match(manifest: Mapping[str, Any]) -> _Res:
    cols = tuple(manifest.get("feature_column_names", []))
    return _result(
        "C2", "C", cols == FEATURE_SCHEMA_V002,
        expected="FEATURE_SCHEMA_V002 canonical order",
        observed=f"diff at first {next((i for i, (a, b) in enumerate(zip(cols, FEATURE_SCHEMA_V002, strict=False)) if a != b), -1)}",
    )


def check_c3_lineage_columns_count(manifest: Mapping[str, Any]) -> _Res:
    cols = manifest.get("feature_column_names", [])
    lineage_present = [c for c in LINEAGE_COLUMNS_V002 if c in cols]
    return _result(
        "C3", "C", len(lineage_present) == EXPECTED_LINEAGE_COLUMN_COUNT,
        expected=str(EXPECTED_LINEAGE_COLUMN_COUNT), observed=str(len(lineage_present)),
    )


def check_c4_feature_columns_count(manifest: Mapping[str, Any]) -> _Res:
    cols = manifest.get("feature_column_names", [])
    feat_present = [c for c in FEATURE_NAMES_V002 if c in cols]
    return _result(
        "C4", "C", len(feat_present) == EXPECTED_FEATURE_COLUMN_COUNT,
        expected=str(EXPECTED_FEATURE_COLUMN_COUNT), observed=str(len(feat_present)),
    )


def check_c5_safe_lineage_column_present(manifest: Mapping[str, Any]) -> _Res:
    cols = manifest.get("feature_column_names", [])
    return _result(
        "C5", "C", "source_phase_4bm_e_outcome" in cols,
        expected="source_phase_4bm_e_outcome present",
        observed=str("source_phase_4bm_e_outcome" in cols),
    )


def check_c6_unsafe_decision_column_absent(manifest: Mapping[str, Any]) -> _Res:
    cols = manifest.get("feature_column_names", [])
    return _result(
        "C6", "C", "source_phase_4bm_e_decision" not in cols,
        expected="source_phase_4bm_e_decision absent",
        observed=str("source_phase_4bm_e_decision" not in cols),
    )


def check_c7_no_forbidden_substrings(manifest: Mapping[str, Any]) -> _Res:
    cols = manifest.get("feature_column_names", [])
    hits = []
    for col in cols:
        lower = col.lower()
        for tok in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002:
            if tok in lower:
                hits.append((col, tok))
                break
    return _result(
        "C7", "C", hits == [],
        expected="0 forbidden token hits",
        observed=f"{len(hits)} hits: {hits[:5]}" if hits else "0 hits",
    )


def check_c8_feature_config_hash(manifest: Mapping[str, Any]) -> _Res:
    fh = manifest.get("feature_config_hash", "")
    return _result(
        "C8", "C", fh == EXPECTED_FEATURE_CONFIG_HASH,
        expected=EXPECTED_FEATURE_CONFIG_HASH, observed=fh,
    )


def check_c9_dataset_identity(manifest: Mapping[str, Any]) -> _Res:
    ok = (
        manifest.get("dataset_family") == "microstructure_features_aggtrades_v001"
        and manifest.get("dataset_version") == FEATURE_DATASET_VERSION_V002
        and manifest.get("feature_schema_version") == FEATURE_SCHEMA_VERSION_V002
        and manifest.get("source_dataset_family") == "microstructure_normalized_aggtrades_v001"
        and manifest.get("source_dataset_version") == "v002"
        and manifest.get("source_phase_4bm_e_outcome") == PHASE_4BM_E_OUTCOME_LITERAL
    )
    return _result(
        "C9", "C", ok,
        expected="dataset_family/version/schema/source/outcome literals match",
        observed=f"family={manifest.get('dataset_family')} version={manifest.get('dataset_version')}",
    )


def check_c10_per_day_schema_identical(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    diffs = []
    for e in manifest["per_day_outputs"]:
        p = ctx.repo_root / "data" / e["feature_parquet_path"]
        s = pq.read_schema(p)
        if tuple(s.names) != FEATURE_SCHEMA_V002:
            diffs.append(e["utc_date"])
    return _result(
        "C10", "C", diffs == [],
        expected="all 90 parquets canonical 62-column schema",
        observed=f"{len(diffs)} schema diffs",
    )


# ---------------------------------------------------------------------------
# Group D — Row-count / partition / timestamp
# ---------------------------------------------------------------------------


def check_d1_total_row_count(manifest: Mapping[str, Any]) -> _Res:
    total = manifest.get("actual_feature_row_count", -1)
    return _result(
        "D1", "D", total == EXPECTED_TOTAL_FEATURE_ROW_COUNT,
        expected=str(EXPECTED_TOTAL_FEATURE_ROW_COUNT), observed=str(total),
    )


def check_d2_sum_per_day_equals_total(manifest: Mapping[str, Any]) -> _Res:
    s = sum(e["row_count"] for e in manifest["per_day_outputs"])
    return _result(
        "D2", "D", s == EXPECTED_TOTAL_FEATURE_ROW_COUNT,
        expected=str(EXPECTED_TOTAL_FEATURE_ROW_COUNT), observed=str(s),
    )


def check_d3_per_day_row_counts_match_source(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    dm = json.loads(ctx.derived_manifest_path.read_text(encoding="utf-8"))
    source_by_date = {e["date"]: e["event_count"] for e in dm["per_file_inventory"]}
    mismatches = []
    for e in manifest["per_day_outputs"]:
        if source_by_date.get(e["utc_date"]) != e["row_count"]:
            mismatches.append((e["utc_date"], e["row_count"], source_by_date.get(e["utc_date"])))
    return _result(
        "D3", "D", mismatches == [],
        expected="per-day feature row count == source normalized event count",
        observed=f"{len(mismatches)} mismatches",
    )


def check_d4_no_zero_row_day(manifest: Mapping[str, Any]) -> _Res:
    zero = [e["utc_date"] for e in manifest["per_day_outputs"] if e["row_count"] <= 0]
    return _result(
        "D4", "D", zero == [],
        expected="all 90 days have row_count > 0",
        observed=f"{len(zero)} zero-row days",
    )


def check_d5_parquet_metadata_rowcount_matches(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    bad = []
    for e in manifest["per_day_outputs"]:
        p = ctx.repo_root / "data" / e["feature_parquet_path"]
        md = pq.ParquetFile(p).metadata
        if md.num_rows != e["row_count"]:
            bad.append((e["utc_date"], md.num_rows, e["row_count"]))
    return _result(
        "D5", "D", bad == [],
        expected="all 90 parquet num_rows match manifest",
        observed=f"{len(bad)} mismatches",
    )


def check_d6_sample_partition_timestamp_invariants(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    violations = []
    for d in SAMPLE_DATES:
        entry = next((e for e in manifest["per_day_outputs"] if e["utc_date"] == d), None)
        if entry is None:
            violations.append((d, "missing_entry"))
            continue
        p = ctx.repo_root / "data" / entry["feature_parquet_path"]
        t = pq.read_table(p)
        n = t.num_rows
        ri = t.column("row_index").to_numpy(zero_copy_only=False)
        T = t.column("feature_timestamp_ms").to_numpy(zero_copy_only=False)
        src_T = t.column("source_transact_time_ms").to_numpy(zero_copy_only=False)
        day_start = _utc_day_start_ms(d)
        day_end = day_start + UTC_DAY_MS
        checks = {
            "row_index_0..n-1": bool((ri[0] == 0) and (ri[-1] == n - 1) and (ri.shape[0] == n)),
            "row_index_step_1": bool(((ri[1:] - ri[:-1]) == 1).all()),
            "T_monotonic": bool((T[1:] >= T[:-1]).all()),
            "T_eq_src_T": bool((src_T == T).all()),
            "in_day_partition": bool(((day_start <= T) & (day_end > T)).all()),
            "symbol_const": set(t.column("symbol").to_pylist()) == {EXPECTED_SYMBOL},
            "utc_date_const": set(t.column("utc_date").to_pylist()) == {d},
            "dataset_version_const_v002": set(t.column("dataset_version").to_pylist()) == {"v002"},
        }
        for name, ok in checks.items():
            if not ok:
                violations.append((d, name))
    return _result(
        "D6", "D", violations == [],
        expected="6 sample dates all pass partition/timestamp/lineage invariants",
        observed=f"{len(violations)} violations",
        detail=f"first few: {violations[:5]}" if violations else "",
    )


# ---------------------------------------------------------------------------
# Group E — Quality flags / cross-day boundary
# ---------------------------------------------------------------------------


def check_e1_day1_missing_window_rule(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    entry = next(e for e in manifest["per_day_outputs"] if e["utc_date"] == "2024-12-01")
    p = ctx.repo_root / "data" / entry["feature_parquet_path"]
    t = pq.read_table(p)
    T = t.column("source_transact_time_ms").to_numpy(zero_copy_only=False)
    flags = t.column("rolling_missing_window_flag").to_numpy(zero_copy_only=False).astype(bool)
    day_start = _utc_day_start_ms("2024-12-01")
    expected = day_start > (T - 60_000)
    ok = bool((flags == expected).all())
    return _result(
        "E1", "E", ok,
        expected="day-1 rolling_missing_window_flag matches (T - 60_000) < day_start",
        observed=f"matches={ok}",
    )


def check_e2_days_2_to_90_no_missing_window(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    sample = [d for d in SAMPLE_DATES if d != "2024-12-01"]
    violations = []
    for d in sample:
        entry = next(e for e in manifest["per_day_outputs"] if e["utc_date"] == d)
        p = ctx.repo_root / "data" / entry["feature_parquet_path"]
        t = pq.read_table(p)
        flags = t.column("rolling_missing_window_flag").to_numpy(zero_copy_only=False).astype(bool)
        if flags.any():
            violations.append((d, int(flags.sum())))
    return _result(
        "E2", "E", violations == [],
        expected="days 2..90 sampled all rolling_missing_window_flag=False",
        observed=f"{len(violations)} sample days with True flags",
    )


def check_e3_invalid_window_flag_all_false(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    violations = []
    for d in SAMPLE_DATES:
        entry = next(e for e in manifest["per_day_outputs"] if e["utc_date"] == d)
        p = ctx.repo_root / "data" / entry["feature_parquet_path"]
        t = pq.read_table(p)
        inv = t.column("invalid_window_flag").to_numpy(zero_copy_only=False).astype(bool)
        if inv.any():
            violations.append((d, int(inv.sum())))
    return _result(
        "E3", "E", violations == [],
        expected="6 sample dates all invalid_window_flag=False",
        observed=f"{len(violations)} sample dates with True invalid_window_flag",
    )


# ---------------------------------------------------------------------------
# Group F — Upstream immutability
# ---------------------------------------------------------------------------


def check_f1_v002_normalized_per_day_immutability(
    ctx: _Ctx,
) -> _Res:
    dm = json.loads(ctx.derived_manifest_path.read_text(encoding="utf-8"))
    bad = []
    for e in dm["per_file_inventory"]:
        p = ctx.repo_root / "data" / e["local_parquet_path"]
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != e["parquet_sha256"]:
            bad.append((e["date"], actual, e["parquet_sha256"]))
    return _result(
        "F1", "F", bad == [],
        expected="all 90 v002 normalized parquets byte-identical to derived manifest",
        observed=f"{len(bad)} mismatches",
    )


def check_f2_v002_derived_manifest_state(ctx: _Ctx) -> _Res:
    dm = json.loads(ctx.derived_manifest_path.read_text(encoding="utf-8"))
    ok = dm.get("research_eligible") is False and dm.get("eligibility_gate_status") == "pending"
    return _result(
        "F2", "F", ok,
        expected="research_eligible=False, eligibility_gate_status='pending'",
        observed=f"re={dm.get('research_eligible')} egs={dm.get('eligibility_gate_status')}",
    )


def check_f3_v002_raw_manifest_state(ctx: _Ctx) -> _Res:
    rm = json.loads(ctx.raw_manifest_path.read_text(encoding="utf-8"))
    ok = rm.get("research_eligible") is False and rm.get("eligibility_gate_status") == "pending"
    return _result(
        "F3", "F", ok,
        expected="research_eligible=False, eligibility_gate_status='pending'",
        observed=f"re={rm.get('research_eligible')} egs={rm.get('eligibility_gate_status')}",
    )


# ---------------------------------------------------------------------------
# Group G — Non-authorization
# ---------------------------------------------------------------------------


def check_g1_manifest_research_eligible_false(manifest: Mapping[str, Any]) -> _Res:
    return _result(
        "G1", "G", manifest.get("research_eligible") is False,
        expected="False", observed=str(manifest.get("research_eligible")),
    )


def check_g2_manifest_eligibility_gate_status_pending(manifest: Mapping[str, Any]) -> _Res:
    return _result(
        "G2", "G", manifest.get("eligibility_gate_status") == "pending",
        expected="pending", observed=str(manifest.get("eligibility_gate_status")),
    )


def check_g3_manifest_stage_4_feature_cleared_false(manifest: Mapping[str, Any]) -> _Res:
    return _result(
        "G3", "G", manifest.get("stage_4_feature_cleared") is False,
        expected="False", observed=str(manifest.get("stage_4_feature_cleared")),
    )


def check_g4_no_label_diagnostics_ml_strategy_backtest(manifest: Mapping[str, Any]) -> _Res:
    flags = (
        manifest.get("label_computation_authorized"),
        manifest.get("diagnostics_authorized"),
        manifest.get("ml_authorized"),
        manifest.get("strategy_authorized"),
        manifest.get("backtest_authorized"),
        manifest.get("acquisition_authorized"),
        manifest.get("successor_authorization_after"),
    )
    ok = all(f is False for f in flags)
    return _result(
        "G4", "G", ok,
        expected="all 7 non-authorization flags False",
        observed=str(flags),
    )


def check_g5_no_network_credentials_mcp(manifest: Mapping[str, Any]) -> _Res:
    flags = (
        manifest.get("no_network_io"),
        manifest.get("no_credentials"),
        manifest.get("no_mcp_or_graphify"),
        manifest.get("no_manifest_mutation"),
        manifest.get("phase_4aw_flip_research_eligible_invariant_preserved"),
    )
    ok = all(f is True for f in flags)
    return _result(
        "G5", "G", ok,
        expected="all 5 immutability flags True",
        observed=str(flags),
    )


def check_g6_boundary_confirmations_all_true(manifest: Mapping[str, Any]) -> _Res:
    bc = manifest.get("boundary_confirmations", {})
    ok = isinstance(bc, dict) and all(v is True for v in bc.values()) and len(bc) >= 18
    return _result(
        "G6", "G", ok,
        expected="all boundary_confirmations True; count >= 18",
        observed=f"count={len(bc) if isinstance(bc, dict) else 'n/a'} all_true={all(v is True for v in bc.values()) if isinstance(bc, dict) else False}",
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


CHECK_ORDER: tuple[str, ...] = (
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
    "D1", "D2", "D3", "D4", "D5", "D6",
    "E1", "E2", "E3",
    "F1", "F2", "F3",
    "G1", "G2", "G3", "G4", "G5", "G6",
)


def run_all_checks(
    ctx: MultidayFeatureGateContext,
) -> tuple[tuple[MultidayFeatureGateCheckResult, ...], Mapping[str, Any]]:
    """Run every check in deterministic order; return (results, manifest_dict)."""
    # Missing feature manifest is recoverable here: file-existence checks (B1,
    # B2) will fail explicitly and the manifest-content checks fall back to an
    # empty dict so they report FAIL with concrete expected/observed pairs.
    try:
        manifest, _, _ = read_json_file(ctx.feature_manifest_path)
    except MultidayFeatureGateIOError:
        manifest = {}
    results: list[MultidayFeatureGateCheckResult] = []

    def _safe(check_id: str, group: str, fn) -> None:
        try:
            res = fn()
        except Exception as exc:
            res = MultidayFeatureGateCheckResult(
                check_id=check_id,
                group=group,
                status=MultidayFeatureGateCheckStatus.ERROR,
                blocking=True,
                expected="(no exception raised)",
                observed=f"{type(exc).__name__}: {exc}",
                detail="check raised; treated as ERROR",
            )
        results.append(res)

    # Group A
    _safe("A1", "A", lambda: check_a1_feature_manifest_sha(ctx))
    _safe("A2", "A", lambda: check_a2_feature_manifest_sidecar_sha(ctx))
    _safe("A3", "A", lambda: check_a3_feature_manifest_sidecar_canonical(ctx))
    _safe("A4", "A", lambda: check_a4_phase_4bm_d_gate_report_sha(ctx))
    _safe("A5", "A", lambda: check_a5_phase_4bm_d_sidecar_sha(ctx))
    _safe("A6", "A", lambda: check_a6_phase_4bm_f_successor_state_sha(ctx))
    _safe("A7", "A", lambda: check_a7_phase_4bm_f_successor_state_sidecar_sha(ctx))
    _safe("A8", "A", lambda: check_a8_phase_4bl_d_r_gate_report_sha(ctx))
    _safe("A9", "A", lambda: check_a9_phase_4bl_e_successor_state_sha(ctx))
    _safe("A10", "A", lambda: check_a10_v002_derived_manifest_sha(ctx))
    _safe("A11", "A", lambda: check_a11_v002_raw_manifest_sha(ctx))
    _safe("A12", "A", lambda: check_a12_phase_4bm_i_verdict(ctx))
    # Group B
    _safe("B1", "B", lambda: check_b1_feature_manifest_present(ctx))
    _safe("B2", "B", lambda: check_b2_feature_manifest_sidecar_present(ctx))
    _safe("B3", "B", lambda: check_b3_feature_parquet_count(ctx))
    _safe("B4", "B", lambda: check_b4_feature_sidecar_count(ctx))
    _safe("B5", "B", lambda: check_b5_date_inventory_exact(ctx))
    _safe("B6", "B", lambda: check_b6_symbol_only_BTCUSDT(ctx))
    _safe("B7", "B", lambda: check_b7_per_day_outputs_length(manifest))
    _safe("B8", "B", lambda: check_b8_per_day_dates_unique(manifest))
    _safe("B9", "B", lambda: check_b9_all_sidecars_canonical(ctx, manifest))
    _safe("B10", "B", lambda: check_b10_all_per_day_parquet_shas_match(ctx, manifest))
    # Group C
    _safe("C1", "C", lambda: check_c1_manifest_feature_column_count(manifest))
    _safe("C2", "C", lambda: check_c2_manifest_feature_column_names_match(manifest))
    _safe("C3", "C", lambda: check_c3_lineage_columns_count(manifest))
    _safe("C4", "C", lambda: check_c4_feature_columns_count(manifest))
    _safe("C5", "C", lambda: check_c5_safe_lineage_column_present(manifest))
    _safe("C6", "C", lambda: check_c6_unsafe_decision_column_absent(manifest))
    _safe("C7", "C", lambda: check_c7_no_forbidden_substrings(manifest))
    _safe("C8", "C", lambda: check_c8_feature_config_hash(manifest))
    _safe("C9", "C", lambda: check_c9_dataset_identity(manifest))
    _safe("C10", "C", lambda: check_c10_per_day_schema_identical(ctx, manifest))
    # Group D
    _safe("D1", "D", lambda: check_d1_total_row_count(manifest))
    _safe("D2", "D", lambda: check_d2_sum_per_day_equals_total(manifest))
    _safe("D3", "D", lambda: check_d3_per_day_row_counts_match_source(ctx, manifest))
    _safe("D4", "D", lambda: check_d4_no_zero_row_day(manifest))
    _safe("D5", "D", lambda: check_d5_parquet_metadata_rowcount_matches(ctx, manifest))
    _safe("D6", "D", lambda: check_d6_sample_partition_timestamp_invariants(ctx, manifest))
    # Group E
    _safe("E1", "E", lambda: check_e1_day1_missing_window_rule(ctx, manifest))
    _safe("E2", "E", lambda: check_e2_days_2_to_90_no_missing_window(ctx, manifest))
    _safe("E3", "E", lambda: check_e3_invalid_window_flag_all_false(ctx, manifest))
    # Group F
    _safe("F1", "F", lambda: check_f1_v002_normalized_per_day_immutability(ctx))
    _safe("F2", "F", lambda: check_f2_v002_derived_manifest_state(ctx))
    _safe("F3", "F", lambda: check_f3_v002_raw_manifest_state(ctx))
    # Group G
    _safe("G1", "G", lambda: check_g1_manifest_research_eligible_false(manifest))
    _safe("G2", "G", lambda: check_g2_manifest_eligibility_gate_status_pending(manifest))
    _safe("G3", "G", lambda: check_g3_manifest_stage_4_feature_cleared_false(manifest))
    _safe("G4", "G", lambda: check_g4_no_label_diagnostics_ml_strategy_backtest(manifest))
    _safe("G5", "G", lambda: check_g5_no_network_credentials_mcp(manifest))
    _safe("G6", "G", lambda: check_g6_boundary_confirmations_all_true(manifest))

    # Sanity: results ordering matches CHECK_ORDER.
    observed = tuple(r.check_id for r in results)
    if observed != CHECK_ORDER:
        raise MultidayFeatureGateIOError(
            f"check ordering drift: observed={observed} expected={CHECK_ORDER}"
        )
    return tuple(results), manifest


__all__ = [
    "CHECK_ORDER",
    "EXPECTED_DATE_COUNT",
    "EXPECTED_DATE_END",
    "EXPECTED_DATE_START",
    "EXPECTED_FEATURE_COLUMN_COUNT",
    "EXPECTED_FEATURE_CONFIG_HASH",
    "EXPECTED_FEATURE_MANIFEST_SHA",
    "EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA",
    "EXPECTED_FEATURE_SCHEMA_COLUMN_COUNT",
    "EXPECTED_LINEAGE_COLUMN_COUNT",
    "EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA",
    "EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA",
    "EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA",
    "EXPECTED_PHASE_4BM_D_SIDECAR_SHA",
    "EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA",
    "EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SIDECAR_SHA",
    "EXPECTED_SYMBOL",
    "EXPECTED_TOTAL_FEATURE_ROW_COUNT",
    "EXPECTED_V002_DERIVED_MANIFEST_SHA",
    "EXPECTED_V002_DERIVED_MANIFEST_SIDECAR_SHA",
    "EXPECTED_V002_RAW_MANIFEST_SHA",
    "EXPECTED_V002_ACQUISITION_LOG_SHA",
    "MultidayFeatureGateCheckResult",
    "MultidayFeatureGateCheckStatus",
    "MultidayFeatureGateContext",
    "SAMPLE_DATES",
    "run_all_checks",
]
