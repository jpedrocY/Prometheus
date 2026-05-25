"""Phase 4bm-Q multi-day v002 label-family eligibility gate check suite.

Implements the deterministic, offline, fail-closed check suite for the
v002 multi-day label family ``microstructure_labels_aggtrades_v001 @
v002`` produced by Phase 4bm-O and structurally QA-passed by Phase
4bm-P. Checks are grouped A..G per the Phase 4bm-Q authorization
prompt:

- A. Locked preconditions (lineage SHAs + Phase 4bm-P verdict).
- B. Inventory / sidecar / gitignore.
- C. Schema / lineage / forbidden-substring detector.
- D. Row-count / partition / timestamp.
- E. Label semantics / censoring / value-domain.
- F. Upstream immutability.
- G. Non-authorization invariants.

The suite is read-only over ``data/microstructure/`` and never mutates
any artefact. Network and credential imports are statically forbidden
by the no-network static-import test.
"""
# ruff: noqa: E501  (Phase 4bm-Q: long v002 SHA literals + lineage column names)
from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

from .labels_schema_v002 import (
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002,
    LABEL_DATASET_FAMILY_V002,
    LABEL_DATASET_VERSION_V002,
    LABEL_HORIZON_MS_V002,
    LABEL_HORIZONS_V002,
    LABEL_LINEAGE_COLUMNS_V002,
    LABEL_NAMES_V002,
    LABEL_SCHEMA_V002,
    LABEL_SCHEMA_VERSION_V002,
    LABEL_SUPPORT_COLUMN_NAMES_V002,
    SOURCE_FEATURE_DATASET_FAMILY_V002,
    SOURCE_FEATURE_DATASET_VERSION_V002,
)
from .multiday_label_gate_io import (
    MultidayLabelGateIOError,
    compute_file_sha256,
    read_json_file,
)

# Locked v002 / Phase 4bm-O expected SHAs and identity facts.
EXPECTED_LABEL_MANIFEST_SHA = (
    "5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed"
)
EXPECTED_LABEL_MANIFEST_SIDECAR_SHA = (
    "451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd"
)
EXPECTED_LABEL_CONFIG_HASH = (
    "352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560"
)
EXPECTED_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)
EXPECTED_FEATURE_MANIFEST_SHA = (
    "512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"
)
EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA = (
    "22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34"
)
EXPECTED_PHASE_4BM_J_GATE_REPORT_SHA = (
    "3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242"
)
EXPECTED_PHASE_4BM_J_GATE_SIDECAR_SHA = (
    "14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125"
)
EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SHA = (
    "7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4"
)
EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SIDECAR_SHA = (
    "c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98"
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
EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA = (
    "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"
)
EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA = (
    "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d"
)

EXPECTED_SYMBOL = "BTCUSDT"
EXPECTED_DATE_START = "2024-12-01"
EXPECTED_DATE_END = "2025-02-28"
EXPECTED_DATE_COUNT = 90
EXPECTED_TOTAL_LABEL_ROW_COUNT = 155_153_449
EXPECTED_LABEL_SCHEMA_COLUMN_COUNT = 40
EXPECTED_LINEAGE_COLUMN_COUNT = 17
EXPECTED_LABEL_COLUMN_COUNT = 8
EXPECTED_SUPPORT_COLUMN_COUNT = 14
EXPECTED_ENVELOPE_TERMINAL_UNIX_MS = 1_740_787_199_996
EXPECTED_CENSORED_PER_HORIZON: Mapping[str, int] = {
    "1s": 14, "5s": 39, "15s": 170, "60s": 634,
}
EXPECTED_INVALID_PRICE_ROW_COUNT = 0

# Deterministic sample dates for deep scans (mirrors Phase 4bm-P sample).
SAMPLE_DATES: tuple[str, ...] = (
    "2024-12-01",
    "2024-12-31",
    "2025-01-15",
    "2025-01-31",
    "2025-02-15",
    "2025-02-28",
)

UTC_DAY_MS = 86_400_000


class MultidayLabelGateCheckStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ERROR = "ERROR"


@dataclass(frozen=True)
class MultidayLabelGateCheckResult:
    check_id: str
    group: str
    status: MultidayLabelGateCheckStatus
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
class MultidayLabelGateContext:
    """Per-run context resolved at orchestrator time."""

    repo_root: Path
    label_manifest_path: Path
    label_manifest_sidecar_path: Path
    labels_root: Path
    feature_manifest_path: Path
    feature_manifest_sidecar_path: Path
    phase_4bm_j_gate_report_path: Path
    phase_4bm_j_gate_sidecar_path: Path
    phase_4bm_l_successor_state_path: Path
    phase_4bm_l_successor_state_sidecar_path: Path
    derived_manifest_path: Path
    derived_manifest_sidecar_path: Path
    raw_manifest_path: Path
    acquisition_log_path: Path
    phase_4bm_d_gate_report_path: Path
    phase_4bm_d_sidecar_path: Path
    phase_4bm_f_successor_state_path: Path
    phase_4bm_f_successor_state_sidecar_path: Path
    phase_4bl_d_r_gate_report_path: Path
    phase_4bl_e_successor_state_path: Path
    structural_qa_phase: str = "4bm-P"
    structural_qa_verdict: str = "LABEL_STRUCTURAL_QA_PASS"


_Ctx = MultidayLabelGateContext
_Res = MultidayLabelGateCheckResult


def _result(
    check_id: str,
    group: str,
    ok: bool,
    *,
    blocking: bool = True,
    expected: Any = "",
    observed: Any = "",
    detail: str = "",
) -> MultidayLabelGateCheckResult:
    status = (
        MultidayLabelGateCheckStatus.PASS
        if ok
        else MultidayLabelGateCheckStatus.FAIL
    )
    return MultidayLabelGateCheckResult(
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


def _resolve_data_path(ctx: _Ctx, relative: str) -> Path:
    """Resolve a manifest-recorded ``data/``-relative path to an absolute path."""
    return ctx.repo_root / "data" / relative


# ---------------------------------------------------------------------------
# Group A — Locked preconditions
# ---------------------------------------------------------------------------


def check_a1_label_manifest_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.label_manifest_path)
    return _result(
        "A1", "A", sha == EXPECTED_LABEL_MANIFEST_SHA,
        expected=EXPECTED_LABEL_MANIFEST_SHA, observed=sha,
        detail="Phase 4bm-O label manifest SHA256 must match expected.",
    )


def check_a2_label_manifest_sidecar_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.label_manifest_sidecar_path)
    return _result(
        "A2", "A", sha == EXPECTED_LABEL_MANIFEST_SIDECAR_SHA,
        expected=EXPECTED_LABEL_MANIFEST_SIDECAR_SHA, observed=sha,
    )


def check_a3_label_manifest_sidecar_canonical(ctx: _Ctx) -> _Res:
    raw = ctx.label_manifest_sidecar_path.read_bytes()
    sha, _ = compute_file_sha256(ctx.label_manifest_path)
    basename = ctx.label_manifest_path.name
    expected = f"{sha}  {basename}\n".encode("ascii")
    ok = (raw == expected) and (b"\r" not in raw) and (not raw.startswith(b"\xef\xbb\xbf"))
    return _result(
        "A3", "A", ok,
        expected="canonical Phase 4bb-F format, no CRLF, no BOM",
        observed=f"len={len(raw)} bytes; equal_to_expected={raw == expected}",
    )


def check_a4_feature_manifest_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.feature_manifest_path)
    return _result(
        "A4", "A", sha == EXPECTED_FEATURE_MANIFEST_SHA,
        expected=EXPECTED_FEATURE_MANIFEST_SHA, observed=sha,
    )


def check_a5_feature_manifest_sidecar_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.feature_manifest_sidecar_path)
    return _result(
        "A5", "A", sha == EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA,
        expected=EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA, observed=sha,
    )


def check_a6_phase_4bm_j_gate_report_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_j_gate_report_path)
    return _result(
        "A6", "A", sha == EXPECTED_PHASE_4BM_J_GATE_REPORT_SHA,
        expected=EXPECTED_PHASE_4BM_J_GATE_REPORT_SHA, observed=sha,
    )


def check_a7_phase_4bm_j_gate_sidecar_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_j_gate_sidecar_path)
    return _result(
        "A7", "A", sha == EXPECTED_PHASE_4BM_J_GATE_SIDECAR_SHA,
        expected=EXPECTED_PHASE_4BM_J_GATE_SIDECAR_SHA, observed=sha,
    )


def check_a8_phase_4bm_l_successor_state_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_l_successor_state_path)
    return _result(
        "A8", "A", sha == EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SHA,
        expected=EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SHA, observed=sha,
    )


def check_a9_phase_4bm_l_successor_state_sidecar_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_l_successor_state_sidecar_path)
    return _result(
        "A9", "A", sha == EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SIDECAR_SHA,
        expected=EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SIDECAR_SHA, observed=sha,
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


def check_a12_phase_4bm_d_gate_report_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_d_gate_report_path)
    return _result(
        "A12", "A", sha == EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA,
        expected=EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA, observed=sha,
    )


def check_a13_phase_4bm_f_successor_state_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bm_f_successor_state_path)
    return _result(
        "A13", "A", sha == EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA,
        expected=EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA, observed=sha,
    )


def check_a14_phase_4bl_d_r_gate_report_sha(ctx: _Ctx) -> _Res:
    sha, _ = compute_file_sha256(ctx.phase_4bl_d_r_gate_report_path)
    return _result(
        "A14", "A", sha == EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA,
        expected=EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA, observed=sha,
    )


def check_a15_phase_4bm_p_verdict(ctx: _Ctx) -> _Res:
    return _result(
        "A15", "A", ctx.structural_qa_verdict == "LABEL_STRUCTURAL_QA_PASS",
        expected="LABEL_STRUCTURAL_QA_PASS", observed=ctx.structural_qa_verdict,
        detail="Phase 4bm-P structural QA verdict is a precondition for Phase 4bm-Q.",
    )


# ---------------------------------------------------------------------------
# Group B — Inventory / sidecar / gitignore
# ---------------------------------------------------------------------------


def check_b1_label_manifest_present(ctx: _Ctx) -> _Res:
    return _result(
        "B1", "B", ctx.label_manifest_path.exists(),
        expected="file exists", observed=str(ctx.label_manifest_path.exists()),
    )


def check_b2_label_manifest_sidecar_present(ctx: _Ctx) -> _Res:
    return _result(
        "B2", "B", ctx.label_manifest_sidecar_path.exists(),
        expected="file exists", observed=str(ctx.label_manifest_sidecar_path.exists()),
    )


def _list_per_day_parquets(ctx: _Ctx) -> list[Path]:
    return sorted((ctx.labels_root / "BTCUSDT").glob("*/*/*.parquet"))


def _list_per_day_sidecars(ctx: _Ctx) -> list[Path]:
    return sorted((ctx.labels_root / "BTCUSDT").glob("*/*/*.parquet.sha256"))


def check_b3_label_parquet_count(ctx: _Ctx) -> _Res:
    n = len(_list_per_day_parquets(ctx))
    return _result(
        "B3", "B", n == EXPECTED_DATE_COUNT,
        expected=str(EXPECTED_DATE_COUNT), observed=str(n),
    )


def check_b4_label_sidecar_count(ctx: _Ctx) -> _Res:
    n = len(_list_per_day_sidecars(ctx))
    return _result(
        "B4", "B", n == EXPECTED_DATE_COUNT,
        expected=str(EXPECTED_DATE_COUNT), observed=str(n),
    )


def check_b5_date_inventory_exact(ctx: _Ctx) -> _Res:
    parquets = _list_per_day_parquets(ctx)
    dates = sorted(
        p.name.replace("BTCUSDT-labels-aggtrades-", "").replace(".parquet", "")
        for p in parquets
    )
    expected = _expected_dates()
    return _result(
        "B5", "B", dates == expected,
        expected=f"{EXPECTED_DATE_COUNT} contiguous dates {EXPECTED_DATE_START}..{EXPECTED_DATE_END}",
        observed=f"first={dates[0] if dates else None} last={dates[-1] if dates else None} count={len(dates)}",
    )


def check_b6_symbol_only_BTCUSDT(ctx: _Ctx) -> _Res:
    subs = sorted(p.name for p in ctx.labels_root.iterdir() if p.is_dir())
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
        sp = _resolve_data_path(ctx, e["sidecar_path"])
        p = _resolve_data_path(ctx, e["path"])
        raw = sp.read_bytes()
        expected_content = f"{e['sha256']}  {p.name}\n".encode("ascii")
        canonical = (raw == expected_content) and (b"\r" not in raw) and (not raw.startswith(b"\xef\xbb\xbf"))
        side_sha = hashlib.sha256(raw).hexdigest()
        sha_match = side_sha == e["sidecar_sha256"]
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
        p = _resolve_data_path(ctx, e["path"])
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != e["sha256"]:
            bad.append((e["utc_date"], actual, e["sha256"]))
    return _result(
        "B10", "B", bad == [],
        expected="all 90 per-day parquet SHA256 match manifest",
        observed=f"{len(bad)} mismatches",
    )


# ---------------------------------------------------------------------------
# Group C — Schema / lineage / forbidden-substring detector
# ---------------------------------------------------------------------------


def check_c1_manifest_column_count(manifest: Mapping[str, Any]) -> _Res:
    n = manifest.get("column_count", -1)
    return _result(
        "C1", "C", n == EXPECTED_LABEL_SCHEMA_COLUMN_COUNT,
        expected=str(EXPECTED_LABEL_SCHEMA_COLUMN_COUNT), observed=str(n),
    )


def check_c2_manifest_schema_column_list_match(manifest: Mapping[str, Any]) -> _Res:
    cols = tuple(manifest.get("schema_column_list", []))
    return _result(
        "C2", "C", cols == LABEL_SCHEMA_V002,
        expected="LABEL_SCHEMA_V002 canonical 40-column order",
        observed=f"diff at first {next((i for i, (a, b) in enumerate(zip(cols, LABEL_SCHEMA_V002, strict=False)) if a != b), -1)}",
    )


def check_c3_lineage_columns_count(manifest: Mapping[str, Any]) -> _Res:
    n = len(manifest.get("lineage_column_list", []))
    return _result(
        "C3", "C", n == EXPECTED_LINEAGE_COLUMN_COUNT,
        expected=str(EXPECTED_LINEAGE_COLUMN_COUNT), observed=str(n),
    )


def check_c4_label_columns_count(manifest: Mapping[str, Any]) -> _Res:
    n = len(manifest.get("label_list", []))
    return _result(
        "C4", "C", n == EXPECTED_LABEL_COLUMN_COUNT,
        expected=str(EXPECTED_LABEL_COLUMN_COUNT), observed=str(n),
    )


def check_c5_support_columns_count(manifest: Mapping[str, Any]) -> _Res:
    n = len(manifest.get("support_column_list", []))
    return _result(
        "C5", "C", n == EXPECTED_SUPPORT_COLUMN_COUNT,
        expected=str(EXPECTED_SUPPORT_COLUMN_COUNT), observed=str(n),
    )


def check_c6_label_config_hash(manifest: Mapping[str, Any]) -> _Res:
    h = manifest.get("label_config_hash", "")
    return _result(
        "C6", "C", h == EXPECTED_LABEL_CONFIG_HASH,
        expected=EXPECTED_LABEL_CONFIG_HASH, observed=h,
    )


def check_c7_feature_config_hash(manifest: Mapping[str, Any]) -> _Res:
    h = manifest.get("feature_config_hash", "")
    return _result(
        "C7", "C", h == EXPECTED_FEATURE_CONFIG_HASH,
        expected=EXPECTED_FEATURE_CONFIG_HASH, observed=h,
    )


def check_c8_dataset_identity(manifest: Mapping[str, Any]) -> _Res:
    ok = (
        manifest.get("dataset_family") == LABEL_DATASET_FAMILY_V002
        and manifest.get("dataset_version") == LABEL_DATASET_VERSION_V002
        and manifest.get("label_schema_version") == LABEL_SCHEMA_VERSION_V002
        and manifest.get("source_feature_dataset_family") == SOURCE_FEATURE_DATASET_FAMILY_V002
        and manifest.get("source_feature_dataset_version") == SOURCE_FEATURE_DATASET_VERSION_V002
        and manifest.get("symbol") == EXPECTED_SYMBOL
        and manifest.get("utc_date_start") == EXPECTED_DATE_START
        and manifest.get("utc_date_end") == EXPECTED_DATE_END
        and manifest.get("date_count") == EXPECTED_DATE_COUNT
        and tuple(manifest.get("horizon_list", [])) == LABEL_HORIZONS_V002
        and tuple(manifest.get("horizon_ms_list", [])) == LABEL_HORIZON_MS_V002
    )
    return _result(
        "C8", "C", ok,
        expected="dataset/source/symbol/date-range/horizon identity literals match",
        observed=f"family={manifest.get('dataset_family')} version={manifest.get('dataset_version')} symbol={manifest.get('symbol')}",
    )


def check_c9_lineage_shas(manifest: Mapping[str, Any]) -> _Res:
    expected = {
        "source_feature_manifest_sha256": EXPECTED_FEATURE_MANIFEST_SHA,
        "source_feature_manifest_sidecar_sha256": EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA,
        "source_feature_successor_state_sha256": EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SHA,
        "source_feature_successor_state_sidecar_sha256": EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SIDECAR_SHA,
        "source_phase_4bm_j_gate_report_sha256": EXPECTED_PHASE_4BM_J_GATE_REPORT_SHA,
        "source_phase_4bm_j_gate_sidecar_sha256": EXPECTED_PHASE_4BM_J_GATE_SIDECAR_SHA,
        "source_normalized_manifest_sha256": EXPECTED_V002_DERIVED_MANIFEST_SHA,
        "source_normalized_manifest_sidecar_sha256": EXPECTED_V002_DERIVED_MANIFEST_SIDECAR_SHA,
        "source_phase_4bm_f_derived_successor_state_sha256": EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA,
        "source_phase_4bm_d_derived_gate_report_sha256": EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA,
        "source_raw_manifest_sha256": EXPECTED_V002_RAW_MANIFEST_SHA,
        "source_acquisition_log_sha256": EXPECTED_V002_ACQUISITION_LOG_SHA,
        "source_phase_4bl_e_raw_successor_state_sha256": EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA,
        "source_phase_4bl_d_r_raw_gate_report_sha256": EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA,
    }
    mismatches = [
        (k, manifest.get(k), v) for k, v in expected.items() if manifest.get(k) != v
    ]
    return _result(
        "C9", "C", mismatches == [],
        expected="all 14 manifest lineage SHA fields match expected",
        observed=f"{len(mismatches)} mismatches",
        detail=f"first: {mismatches[:2]}" if mismatches else "",
    )


def check_c10_no_forbidden_substrings(manifest: Mapping[str, Any]) -> _Res:
    cols = manifest.get("schema_column_list", [])
    hits = []
    for col in cols:
        lower = col.lower()
        for tok in FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002:
            if tok in lower:
                hits.append((col, tok))
                break
    return _result(
        "C10", "C", hits == [],
        expected="0 forbidden token hits across 40 schema columns",
        observed=f"{len(hits)} hits: {hits[:5]}" if hits else "0 hits",
    )


def check_c11_per_day_schema_identical(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    diffs = []
    for e in manifest["per_day_outputs"]:
        p = _resolve_data_path(ctx, e["path"])
        s = pq.read_schema(p)
        if tuple(s.names) != LABEL_SCHEMA_V002:
            diffs.append(e["utc_date"])
    return _result(
        "C11", "C", diffs == [],
        expected="all 90 parquets canonical 40-column schema",
        observed=f"{len(diffs)} schema diffs",
    )


# ---------------------------------------------------------------------------
# Group D — Row-count / partition / timestamp
# ---------------------------------------------------------------------------


def check_d1_total_row_count(manifest: Mapping[str, Any]) -> _Res:
    total = manifest.get("row_count", -1)
    return _result(
        "D1", "D", total == EXPECTED_TOTAL_LABEL_ROW_COUNT,
        expected=str(EXPECTED_TOTAL_LABEL_ROW_COUNT), observed=str(total),
    )


def check_d2_sum_per_day_equals_total(manifest: Mapping[str, Any]) -> _Res:
    s = sum(e["row_count"] for e in manifest["per_day_outputs"])
    return _result(
        "D2", "D", s == EXPECTED_TOTAL_LABEL_ROW_COUNT,
        expected=str(EXPECTED_TOTAL_LABEL_ROW_COUNT), observed=str(s),
    )


def check_d3_per_day_row_counts_match_features(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    fm = json.loads(ctx.feature_manifest_path.read_text(encoding="utf-8"))
    source_by_date = {e["utc_date"]: e["row_count"] for e in fm["per_day_outputs"]}
    mismatches = []
    for e in manifest["per_day_outputs"]:
        if source_by_date.get(e["utc_date"]) != e["row_count"]:
            mismatches.append((e["utc_date"], e["row_count"], source_by_date.get(e["utc_date"])))
    return _result(
        "D3", "D", mismatches == [],
        expected="per-day label row count == per-day feature row count",
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
        p = _resolve_data_path(ctx, e["path"])
        md = pq.ParquetFile(p).metadata
        if md.num_rows != e["row_count"]:
            bad.append((e["utc_date"], md.num_rows, e["row_count"]))
    return _result(
        "D5", "D", bad == [],
        expected="all 90 parquet num_rows match manifest",
        observed=f"{len(bad)} mismatches",
    )


def check_d6_sample_partition_invariants(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    violations = []
    for d in SAMPLE_DATES:
        entry = next((e for e in manifest["per_day_outputs"] if e["utc_date"] == d), None)
        if entry is None:
            violations.append((d, "missing_entry"))
            continue
        p = _resolve_data_path(ctx, entry["path"])
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
# Group E — Label semantics / censoring / value-domain
# ---------------------------------------------------------------------------


def check_e1_per_row_censoring_rule(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    """For sampled days × 4 horizons: horizon_censored_flag_H == (T + H_ms > envelope_terminal_unix_ms)."""
    envelope = int(manifest.get("envelope_terminal_unix_ms", -1))
    violations: list[tuple[str, str, int]] = []
    for d in SAMPLE_DATES:
        entry = next(e for e in manifest["per_day_outputs"] if e["utc_date"] == d)
        p = _resolve_data_path(ctx, entry["path"])
        t = pq.read_table(p)
        T = t.column("source_transact_time_ms").to_numpy(zero_copy_only=False)
        for h, h_ms in zip(LABEL_HORIZONS_V002, LABEL_HORIZON_MS_V002, strict=True):
            col = f"horizon_censored_flag_{h}"
            flags = t.column(col).to_numpy(zero_copy_only=False).astype(bool)
            expected = (T + h_ms) > envelope
            mism = int((flags != expected).sum())
            if mism:
                violations.append((d, h, mism))
    return _result(
        "E1", "E", violations == [],
        expected="per-row horizon_censored_flag_H matches (T + H_ms > envelope_terminal_unix_ms)",
        observed=f"{len(violations)} (date, horizon, mismatched_rows) tuples",
    )


def check_e2_censored_null_discipline(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    """When horizon_censored_flag_H==True the 4 per-horizon value columns are null; OR equals label_any_censored_flag."""
    violations: list[tuple[str, str, str]] = []
    for d in SAMPLE_DATES:
        entry = next(e for e in manifest["per_day_outputs"] if e["utc_date"] == d)
        p = _resolve_data_path(ctx, entry["path"])
        t = pq.read_table(p)
        any_flag = t.column("label_any_censored_flag").to_numpy(zero_copy_only=False).astype(bool)
        or_flag = None
        for h in LABEL_HORIZONS_V002:
            flag = t.column(f"horizon_censored_flag_{h}").to_numpy(zero_copy_only=False).astype(bool)
            or_flag = flag if or_flag is None else (or_flag | flag)
            # nulls in censored rows
            for col_prefix in (
                "forward_log_return_",
                "forward_direction_",
                "reference_row_index_",
                "reference_timestamp_ms_",
            ):
                arr = t.column(col_prefix + h)
                # pyarrow chunked array: count nulls
                mask = arr.is_null().to_numpy(zero_copy_only=False)
                if (flag & ~mask).any():
                    violations.append((d, col_prefix + h, "censored_row_not_null"))
        if or_flag is not None and not bool((any_flag == or_flag).all()):
            violations.append((d, "label_any_censored_flag", "ne_or_of_per_horizon"))
    return _result(
        "E2", "E", violations == [],
        expected="censored-row null discipline + label_any_censored_flag == OR(horizon_censored_flag_*)",
        observed=f"{len(violations)} violations",
        detail=f"first few: {violations[:5]}" if violations else "",
    )


def check_e3_direction_value_domain(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    """forward_direction_H values are in {-1, 0, +1, null}."""
    violations: list[tuple[str, str, list[Any]]] = []
    for d in SAMPLE_DATES:
        entry = next(e for e in manifest["per_day_outputs"] if e["utc_date"] == d)
        p = _resolve_data_path(ctx, entry["path"])
        t = pq.read_table(p)
        for h in LABEL_HORIZONS_V002:
            arr = t.column(f"forward_direction_{h}")
            vals = arr.to_pylist()
            bad = [v for v in vals if v is not None and v not in (-1, 0, 1)]
            if bad:
                violations.append((d, h, bad[:3]))
    return _result(
        "E3", "E", violations == [],
        expected="forward_direction_H in {-1, 0, +1, null}",
        observed=f"{len(violations)} violating sample days",
    )


def check_e4_invalid_price_flag_zero(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    """invalid_price_row_count==0 in manifest + sum across per-day == 0 + sampled rows all False."""
    top_zero = manifest.get("invalid_price_row_count", -1) == 0
    sum_zero = sum(e.get("invalid_price_row_count", 0) for e in manifest["per_day_outputs"]) == 0
    sample_zero = True
    for d in SAMPLE_DATES:
        entry = next(e for e in manifest["per_day_outputs"] if e["utc_date"] == d)
        p = _resolve_data_path(ctx, entry["path"])
        t = pq.read_table(p)
        if bool(t.column("label_invalid_price_flag").to_numpy(zero_copy_only=False).any()):
            sample_zero = False
            break
    ok = top_zero and sum_zero and sample_zero
    return _result(
        "E4", "E", ok,
        expected="invalid_price_row_count == 0 at top-level, per-day aggregate, and sampled rows",
        observed=f"top_zero={top_zero} sum_zero={sum_zero} sample_zero={sample_zero}",
    )


def check_e5_censored_per_horizon_aggregate(manifest: Mapping[str, Any]) -> _Res:
    top = dict(manifest.get("censored_per_horizon", {}))
    agg: dict[str, int] = {h: 0 for h in LABEL_HORIZONS_V002}
    for e in manifest["per_day_outputs"]:
        per_day = e.get("per_horizon_censored_counts", {})
        for h in LABEL_HORIZONS_V002:
            agg[h] += int(per_day.get(h, 0))
    expected = dict(EXPECTED_CENSORED_PER_HORIZON)
    ok = top == expected and agg == expected
    return _result(
        "E5", "E", ok,
        expected=f"censored_per_horizon == {expected} at top-level and aggregate",
        observed=f"top={top} aggregate={agg}",
    )


def check_e6_envelope_terminal_unix_ms(manifest: Mapping[str, Any]) -> _Res:
    v = manifest.get("envelope_terminal_unix_ms", -1)
    return _result(
        "E6", "E", v == EXPECTED_ENVELOPE_TERMINAL_UNIX_MS,
        expected=str(EXPECTED_ENVELOPE_TERMINAL_UNIX_MS), observed=str(v),
    )


def check_e7_censored_monotone_in_horizon(manifest: Mapping[str, Any]) -> _Res:
    """Censored counts are monotone non-decreasing in horizon length."""
    top = manifest.get("censored_per_horizon", {})
    vals = [int(top.get(h, 0)) for h in LABEL_HORIZONS_V002]
    ok = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
    return _result(
        "E7", "E", ok,
        expected="censored_per_horizon monotone non-decreasing in horizon order",
        observed=f"values={vals}",
    )


# ---------------------------------------------------------------------------
# Group F — Upstream immutability
# ---------------------------------------------------------------------------


def check_f1_feature_manifest_state_pending(ctx: _Ctx) -> _Res:
    fm = json.loads(ctx.feature_manifest_path.read_text(encoding="utf-8"))
    ok = (
        fm.get("research_eligible") is False
        and fm.get("eligibility_gate_status") == "pending"
        and fm.get("stage_4_feature_cleared") is False
    )
    return _result(
        "F1", "F", ok,
        expected="feature manifest research_eligible=False, eligibility_gate_status='pending', stage_4_feature_cleared=False",
        observed=f"re={fm.get('research_eligible')} egs={fm.get('eligibility_gate_status')} s4={fm.get('stage_4_feature_cleared')}",
    )


def check_f2_derived_manifest_state_pending(ctx: _Ctx) -> _Res:
    dm = json.loads(ctx.derived_manifest_path.read_text(encoding="utf-8"))
    ok = dm.get("research_eligible") is False and dm.get("eligibility_gate_status") == "pending"
    return _result(
        "F2", "F", ok,
        expected="derived manifest research_eligible=False, eligibility_gate_status='pending'",
        observed=f"re={dm.get('research_eligible')} egs={dm.get('eligibility_gate_status')}",
    )


def check_f3_raw_manifest_state_pending(ctx: _Ctx) -> _Res:
    rm = json.loads(ctx.raw_manifest_path.read_text(encoding="utf-8"))
    ok = rm.get("research_eligible") is False and rm.get("eligibility_gate_status") == "pending"
    return _result(
        "F3", "F", ok,
        expected="raw manifest research_eligible=False, eligibility_gate_status='pending'",
        observed=f"re={rm.get('research_eligible')} egs={rm.get('eligibility_gate_status')}",
    )


def check_f4_per_day_feature_parquet_sha_lineage(
    ctx: _Ctx, manifest: Mapping[str, Any]
) -> _Res:
    """For every day, label manifest's source_feature_parquet_sha256 equals
    the v002 feature manifest's per_day_outputs[i].feature_parquet_sha256."""
    fm = json.loads(ctx.feature_manifest_path.read_text(encoding="utf-8"))
    feat_by_date = {e["utc_date"]: e["feature_parquet_sha256"] for e in fm["per_day_outputs"]}
    mism = []
    for e in manifest["per_day_outputs"]:
        if feat_by_date.get(e["utc_date"]) != e.get("source_feature_parquet_sha256"):
            mism.append(e["utc_date"])
    return _result(
        "F4", "F", mism == [],
        expected="90/90 source_feature_parquet_sha256 lineage matches v002 feature manifest",
        observed=f"{len(mism)} mismatches",
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


def check_g3_manifest_stage_5_label_cleared_false(manifest: Mapping[str, Any]) -> _Res:
    return _result(
        "G3", "G", manifest.get("stage_5_label_cleared") is False,
        expected="False", observed=str(manifest.get("stage_5_label_cleared")),
    )


def check_g4_label_family_research_use_unauthorized(manifest: Mapping[str, Any]) -> _Res:
    return _result(
        "G4", "G", manifest.get("label_family_research_use_authorized") is False,
        expected="False", observed=str(manifest.get("label_family_research_use_authorized")),
    )


def check_g5_chronological_split_policy_not_yet_defined(manifest: Mapping[str, Any]) -> _Res:
    return _result(
        "G5", "G", manifest.get("chronological_split_policy") == "not_yet_defined",
        expected="not_yet_defined", observed=str(manifest.get("chronological_split_policy")),
    )


def check_g6_non_authorization_flags(manifest: Mapping[str, Any]) -> _Res:
    flags = (
        manifest.get("diagnostics_authorized"),
        manifest.get("ml_authorized"),
        manifest.get("strategy_authorized"),
        manifest.get("backtest_authorized"),
        manifest.get("acquisition_authorized"),
        manifest.get("successor_authorization_after"),
        manifest.get("label_family_eligibility_gate_authorized"),
        manifest.get("label_structural_qa_authorized"),
    )
    ok = all(f is False for f in flags)
    return _result(
        "G6", "G", ok,
        expected="all 8 non-authorization flags False",
        observed=str(flags),
    )


def check_g7_boundary_confirmations_all_true(manifest: Mapping[str, Any]) -> _Res:
    bc = manifest.get("boundary_confirmations", {})
    ok = (
        isinstance(bc, dict)
        and all(v is True for v in bc.values())
        and len(bc) >= 17
    )
    return _result(
        "G7", "G", ok,
        expected="all boundary_confirmations True; count >= 17",
        observed=f"count={len(bc) if isinstance(bc, dict) else 'n/a'} all_true={all(v is True for v in bc.values()) if isinstance(bc, dict) else False}",
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


CHECK_ORDER: tuple[str, ...] = (
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10",
    "A11", "A12", "A13", "A14", "A15",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11",
    "D1", "D2", "D3", "D4", "D5", "D6",
    "E1", "E2", "E3", "E4", "E5", "E6", "E7",
    "F1", "F2", "F3", "F4",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7",
)


def run_all_checks(
    ctx: MultidayLabelGateContext,
) -> tuple[tuple[MultidayLabelGateCheckResult, ...], Mapping[str, Any]]:
    """Run every check in deterministic order; return ``(results, manifest_dict)``."""
    try:
        manifest, _, _ = read_json_file(ctx.label_manifest_path)
    except MultidayLabelGateIOError:
        manifest = {}
    results: list[MultidayLabelGateCheckResult] = []

    def _safe(
        check_id: str,
        group: str,
        fn: "Callable[[], MultidayLabelGateCheckResult]",
    ) -> None:
        try:
            res = fn()
        except Exception as exc:
            res = MultidayLabelGateCheckResult(
                check_id=check_id,
                group=group,
                status=MultidayLabelGateCheckStatus.ERROR,
                blocking=True,
                expected="(no exception raised)",
                observed=f"{type(exc).__name__}: {exc}",
                detail="check raised; treated as ERROR",
            )
        results.append(res)

    # Group A
    _safe("A1", "A", lambda: check_a1_label_manifest_sha(ctx))
    _safe("A2", "A", lambda: check_a2_label_manifest_sidecar_sha(ctx))
    _safe("A3", "A", lambda: check_a3_label_manifest_sidecar_canonical(ctx))
    _safe("A4", "A", lambda: check_a4_feature_manifest_sha(ctx))
    _safe("A5", "A", lambda: check_a5_feature_manifest_sidecar_sha(ctx))
    _safe("A6", "A", lambda: check_a6_phase_4bm_j_gate_report_sha(ctx))
    _safe("A7", "A", lambda: check_a7_phase_4bm_j_gate_sidecar_sha(ctx))
    _safe("A8", "A", lambda: check_a8_phase_4bm_l_successor_state_sha(ctx))
    _safe("A9", "A", lambda: check_a9_phase_4bm_l_successor_state_sidecar_sha(ctx))
    _safe("A10", "A", lambda: check_a10_v002_derived_manifest_sha(ctx))
    _safe("A11", "A", lambda: check_a11_v002_raw_manifest_sha(ctx))
    _safe("A12", "A", lambda: check_a12_phase_4bm_d_gate_report_sha(ctx))
    _safe("A13", "A", lambda: check_a13_phase_4bm_f_successor_state_sha(ctx))
    _safe("A14", "A", lambda: check_a14_phase_4bl_d_r_gate_report_sha(ctx))
    _safe("A15", "A", lambda: check_a15_phase_4bm_p_verdict(ctx))
    # Group B
    _safe("B1", "B", lambda: check_b1_label_manifest_present(ctx))
    _safe("B2", "B", lambda: check_b2_label_manifest_sidecar_present(ctx))
    _safe("B3", "B", lambda: check_b3_label_parquet_count(ctx))
    _safe("B4", "B", lambda: check_b4_label_sidecar_count(ctx))
    _safe("B5", "B", lambda: check_b5_date_inventory_exact(ctx))
    _safe("B6", "B", lambda: check_b6_symbol_only_BTCUSDT(ctx))
    _safe("B7", "B", lambda: check_b7_per_day_outputs_length(manifest))
    _safe("B8", "B", lambda: check_b8_per_day_dates_unique(manifest))
    _safe("B9", "B", lambda: check_b9_all_sidecars_canonical(ctx, manifest))
    _safe("B10", "B", lambda: check_b10_all_per_day_parquet_shas_match(ctx, manifest))
    # Group C
    _safe("C1", "C", lambda: check_c1_manifest_column_count(manifest))
    _safe("C2", "C", lambda: check_c2_manifest_schema_column_list_match(manifest))
    _safe("C3", "C", lambda: check_c3_lineage_columns_count(manifest))
    _safe("C4", "C", lambda: check_c4_label_columns_count(manifest))
    _safe("C5", "C", lambda: check_c5_support_columns_count(manifest))
    _safe("C6", "C", lambda: check_c6_label_config_hash(manifest))
    _safe("C7", "C", lambda: check_c7_feature_config_hash(manifest))
    _safe("C8", "C", lambda: check_c8_dataset_identity(manifest))
    _safe("C9", "C", lambda: check_c9_lineage_shas(manifest))
    _safe("C10", "C", lambda: check_c10_no_forbidden_substrings(manifest))
    _safe("C11", "C", lambda: check_c11_per_day_schema_identical(ctx, manifest))
    # Group D
    _safe("D1", "D", lambda: check_d1_total_row_count(manifest))
    _safe("D2", "D", lambda: check_d2_sum_per_day_equals_total(manifest))
    _safe("D3", "D", lambda: check_d3_per_day_row_counts_match_features(ctx, manifest))
    _safe("D4", "D", lambda: check_d4_no_zero_row_day(manifest))
    _safe("D5", "D", lambda: check_d5_parquet_metadata_rowcount_matches(ctx, manifest))
    _safe("D6", "D", lambda: check_d6_sample_partition_invariants(ctx, manifest))
    # Group E
    _safe("E1", "E", lambda: check_e1_per_row_censoring_rule(ctx, manifest))
    _safe("E2", "E", lambda: check_e2_censored_null_discipline(ctx, manifest))
    _safe("E3", "E", lambda: check_e3_direction_value_domain(ctx, manifest))
    _safe("E4", "E", lambda: check_e4_invalid_price_flag_zero(ctx, manifest))
    _safe("E5", "E", lambda: check_e5_censored_per_horizon_aggregate(manifest))
    _safe("E6", "E", lambda: check_e6_envelope_terminal_unix_ms(manifest))
    _safe("E7", "E", lambda: check_e7_censored_monotone_in_horizon(manifest))
    # Group F
    _safe("F1", "F", lambda: check_f1_feature_manifest_state_pending(ctx))
    _safe("F2", "F", lambda: check_f2_derived_manifest_state_pending(ctx))
    _safe("F3", "F", lambda: check_f3_raw_manifest_state_pending(ctx))
    _safe("F4", "F", lambda: check_f4_per_day_feature_parquet_sha_lineage(ctx, manifest))
    # Group G
    _safe("G1", "G", lambda: check_g1_manifest_research_eligible_false(manifest))
    _safe("G2", "G", lambda: check_g2_manifest_eligibility_gate_status_pending(manifest))
    _safe("G3", "G", lambda: check_g3_manifest_stage_5_label_cleared_false(manifest))
    _safe("G4", "G", lambda: check_g4_label_family_research_use_unauthorized(manifest))
    _safe("G5", "G", lambda: check_g5_chronological_split_policy_not_yet_defined(manifest))
    _safe("G6", "G", lambda: check_g6_non_authorization_flags(manifest))
    _safe("G7", "G", lambda: check_g7_boundary_confirmations_all_true(manifest))

    observed = tuple(r.check_id for r in results)
    if observed != CHECK_ORDER:
        raise MultidayLabelGateIOError(
            f"check ordering drift: observed={observed} expected={CHECK_ORDER}"
        )
    return tuple(results), manifest


__all__ = [
    "CHECK_ORDER",
    "EXPECTED_CENSORED_PER_HORIZON",
    "EXPECTED_DATE_COUNT",
    "EXPECTED_DATE_END",
    "EXPECTED_DATE_START",
    "EXPECTED_ENVELOPE_TERMINAL_UNIX_MS",
    "EXPECTED_FEATURE_CONFIG_HASH",
    "EXPECTED_FEATURE_MANIFEST_SHA",
    "EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA",
    "EXPECTED_INVALID_PRICE_ROW_COUNT",
    "EXPECTED_LABEL_COLUMN_COUNT",
    "EXPECTED_LABEL_CONFIG_HASH",
    "EXPECTED_LABEL_MANIFEST_SHA",
    "EXPECTED_LABEL_MANIFEST_SIDECAR_SHA",
    "EXPECTED_LABEL_SCHEMA_COLUMN_COUNT",
    "EXPECTED_LINEAGE_COLUMN_COUNT",
    "EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA",
    "EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA",
    "EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA",
    "EXPECTED_PHASE_4BM_D_SIDECAR_SHA",
    "EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA",
    "EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SIDECAR_SHA",
    "EXPECTED_PHASE_4BM_J_GATE_REPORT_SHA",
    "EXPECTED_PHASE_4BM_J_GATE_SIDECAR_SHA",
    "EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SHA",
    "EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SIDECAR_SHA",
    "EXPECTED_SUPPORT_COLUMN_COUNT",
    "EXPECTED_SYMBOL",
    "EXPECTED_TOTAL_LABEL_ROW_COUNT",
    "EXPECTED_V002_ACQUISITION_LOG_SHA",
    "EXPECTED_V002_DERIVED_MANIFEST_SHA",
    "EXPECTED_V002_DERIVED_MANIFEST_SIDECAR_SHA",
    "EXPECTED_V002_RAW_MANIFEST_SHA",
    "MultidayLabelGateCheckResult",
    "MultidayLabelGateCheckStatus",
    "MultidayLabelGateContext",
    "SAMPLE_DATES",
    "run_all_checks",
]

# Used for unused-import warning suppression: re-export literally so the
# narrow __init__ re-export can import canonical schema fragments.
_ = LABEL_LINEAGE_COLUMNS_V002
_ = LABEL_NAMES_V002
_ = LABEL_SUPPORT_COLUMN_NAMES_V002
