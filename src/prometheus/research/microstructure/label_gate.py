"""Phase 4bj-E label-family eligibility-gate orchestrator.

Reads the Phase 4bj-C label artefacts (label parquet, label parquet
sidecar, label manifest, label manifest sidecar) read-only, runs the
Phase 4bj-E check suite (and optionally cross-checks against the
source feature parquet when provided), and (when
``write_report=True``) atomically emits a JSON gate report plus paired
SHA256 sidecar under ``data/microstructure/gate-reports/labels/``.
Never mutates any source artefact. Never flips ``research_eligible``.
"""
from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pyarrow as pa

from .label_gate_checks import (
    CHECK_ORDER,
    EXPECTED_CENSORED_PER_HORIZON,
    EXPECTED_DATASET_FAMILY,
    EXPECTED_DATASET_VERSION,
    EXPECTED_INVALID_PRICE_ROW_COUNT,
    EXPECTED_LABEL_CONFIG_HASH,
    EXPECTED_LABEL_MANIFEST_SHA,
    EXPECTED_LABEL_PARQUET_SHA,
    EXPECTED_LABEL_SCHEMA_VERSION,
    EXPECTED_ROW_COUNT,
    EXPECTED_SOURCE_FEATURE_MANIFEST_SHA,
    EXPECTED_SOURCE_FEATURE_PARQUET_SHA,
    EXPECTED_SOURCE_FEATURE_SUCCESSOR_STATE_SHA,
    EXPECTED_SOURCE_NORMALIZED_PARQUET_SHA,
    EXPECTED_SOURCE_PHASE_4BI_B_GATE_REPORT_SHA,
    EXPECTED_SYMBOL,
    EXPECTED_UTC_DATE,
    LabelGateCheckResult,
    LabelGateCheckStatus,
    LabelGateContext,
    load_parquet_table,
    query_gitignore_status,
    run_all_checks,
)
from .label_gate_io import (
    LabelGateIOError,
    assert_path_under_microstructure,
    compute_bytes_sha256,
    compute_file_sha256,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
)
from .label_gate_report import (
    build_label_gate_report,
    write_label_gate_report,
)
from .labels_schema import (
    LABEL_LINEAGE_COLUMNS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
)


class LabelGateError(RuntimeError):
    """Raised on input-construction or gate-run errors."""


@dataclass(frozen=True)
class LabelGateInput:
    """Frozen orchestrator input for the Phase 4bj-E gate."""

    label_parquet_path: Path
    label_manifest_path: Path
    output_root: Path
    code_commit_sha: str
    repo_root: Path
    source_feature_parquet_path: Path | None = None
    source_feature_manifest_path: Path | None = None
    write_report: bool = True

    def __post_init__(self) -> None:
        for attr in (
            "label_parquet_path",
            "label_manifest_path",
            "output_root",
            "repo_root",
        ):
            v = getattr(self, attr)
            if not isinstance(v, Path):
                raise LabelGateError(f"{attr} must be Path; got {type(v).__name__}")
        for attr in (
            "source_feature_parquet_path",
            "source_feature_manifest_path",
        ):
            v = getattr(self, attr)
            if v is not None and not isinstance(v, Path):
                raise LabelGateError(
                    f"{attr} must be Path or None; got {type(v).__name__}"
                )
        if not self.code_commit_sha or not isinstance(self.code_commit_sha, str):
            raise LabelGateError("code_commit_sha must be a non-empty str")
        try:
            assert_path_under_microstructure(
                self.label_parquet_path, label="label_parquet_path"
            )
            assert_path_under_microstructure(
                self.label_manifest_path, label="label_manifest_path"
            )
            assert_path_under_microstructure(self.output_root, label="output_root")
        except LabelGateIOError as exc:
            raise LabelGateError(str(exc)) from exc


@dataclass(frozen=True)
class LabelGateResult:
    """Frozen orchestrator result for the Phase 4bj-E gate."""

    overall_status: LabelGateCheckStatus
    research_eligible_after: bool
    eligibility_gate_status_after: str
    label_manifest_research_eligible_after: bool
    label_manifest_eligibility_gate_status_after: str
    label_manifest_chronological_split_policy_after: str
    stage_5_authorized: bool
    stage_5_research_or_ml_use: bool
    no_successor_authorization: bool
    checks: tuple[LabelGateCheckResult, ...]
    report_path: Path | None
    sidecar_path: Path | None
    report_id: str
    report_sha256: str | None
    report_size_bytes: int | None
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any] = field(default_factory=dict)


_BOUNDARY_KEYS = (
    "no_label_parquet_mutation",
    "no_label_manifest_mutation",
    "no_source_artefact_mutation",
    "no_data_microstructure_write_outside_gate_reports_labels",
    "no_label_successor_state_created",
    "no_ml_trained",
    "no_strategy_created",
    "no_signal_computed",
    "no_backtest_run",
    "no_acquisition",
    "no_network_io",
    "no_websocket",
    "no_credential_read",
    "no_env_read",
    "no_mcp_or_graphify",
    "label_manifest_research_eligible_after_is_false",
    "label_manifest_eligibility_gate_status_after_is_pending",
    "label_manifest_chronological_split_policy_after_is_not_yet_defined",
    "stage_5_research_or_ml_use_is_false",
    "no_successor_authorization",
)


def _classify_overall(
    checks: tuple[LabelGateCheckResult, ...],
) -> LabelGateCheckStatus:
    """PASS only if all checks PASS or NOT_APPLICABLE; FAIL > ERROR > PASS."""
    has_fail = any(c.status == LabelGateCheckStatus.FAIL for c in checks)
    if has_fail:
        return LabelGateCheckStatus.FAIL
    has_error = any(c.status == LabelGateCheckStatus.ERROR for c in checks)
    if has_error:
        return LabelGateCheckStatus.ERROR
    return LabelGateCheckStatus.PASS


def _build_boundary_confirmations(
    *,
    label_parquet_sha_pre: str,
    label_parquet_sha_post: str,
    label_manifest_sha_pre: str,
    label_manifest_sha_post: str,
    source_feature_parquet_sha_pre: str | None,
    source_feature_parquet_sha_post: str | None,
    source_feature_manifest_sha_pre: str | None,
    source_feature_manifest_sha_post: str | None,
) -> dict[str, bool]:
    label_parquet_unchanged = label_parquet_sha_pre == label_parquet_sha_post
    label_manifest_unchanged = label_manifest_sha_pre == label_manifest_sha_post
    source_unchanged = (
        source_feature_parquet_sha_pre == source_feature_parquet_sha_post
        and source_feature_manifest_sha_pre == source_feature_manifest_sha_post
    )
    return {
        "no_label_parquet_mutation": label_parquet_unchanged,
        "no_label_manifest_mutation": label_manifest_unchanged,
        "no_source_artefact_mutation": source_unchanged,
        "no_data_microstructure_write_outside_gate_reports_labels": True,
        "no_label_successor_state_created": True,
        "no_ml_trained": True,
        "no_strategy_created": True,
        "no_signal_computed": True,
        "no_backtest_run": True,
        "no_acquisition": True,
        "no_network_io": True,
        "no_websocket": True,
        "no_credential_read": True,
        "no_env_read": True,
        "no_mcp_or_graphify": True,
        "label_manifest_research_eligible_after_is_false": True,
        "label_manifest_eligibility_gate_status_after_is_pending": True,
        "label_manifest_chronological_split_policy_after_is_not_yet_defined": True,
        "stage_5_research_or_ml_use_is_false": True,
        "no_successor_authorization": True,
    }


def validate_label_gate_inputs(inp: LabelGateInput) -> None:
    """Verify all required input artefacts exist and are readable.

    Raises :class:`LabelGateError` on the first failure.
    """
    must_exist: list[tuple[str, Path]] = [
        ("label_parquet_path", inp.label_parquet_path),
        ("label_manifest_path", inp.label_manifest_path),
    ]
    for label, p in must_exist:
        if not p.exists():
            raise LabelGateError(f"{label} does not exist: {p}")
    sidecar_p = inp.label_parquet_path.with_suffix(
        inp.label_parquet_path.suffix + ".sha256"
    )
    if not sidecar_p.exists():
        raise LabelGateError(f"label parquet sidecar does not exist: {sidecar_p}")
    sidecar_m = inp.label_manifest_path.with_suffix(
        inp.label_manifest_path.suffix + ".sha256"
    )
    if not sidecar_m.exists():
        raise LabelGateError(f"label manifest sidecar does not exist: {sidecar_m}")
    if (
        inp.source_feature_parquet_path is not None
        and not inp.source_feature_parquet_path.exists()
    ):
        raise LabelGateError(
            "source_feature_parquet_path does not exist: "
            f"{inp.source_feature_parquet_path}"
        )
    if (
        inp.source_feature_manifest_path is not None
        and not inp.source_feature_manifest_path.exists()
    ):
        raise LabelGateError(
            "source_feature_manifest_path does not exist: "
            f"{inp.source_feature_manifest_path}"
        )


def run_label_family_gate(inp: LabelGateInput) -> LabelGateResult:
    """Run the Phase 4bj-E label-family eligibility gate exactly once."""

    validate_label_gate_inputs(inp)

    # Pre-run hashes (immutability anchor)
    label_parquet_sha_pre = compute_file_sha256(inp.label_parquet_path)
    label_manifest_bytes = read_manifest_bytes(inp.label_manifest_path)
    label_manifest_sha_pre = compute_bytes_sha256(label_manifest_bytes)
    label_parquet_sidecar_path = inp.label_parquet_path.with_suffix(
        inp.label_parquet_path.suffix + ".sha256"
    )
    label_manifest_sidecar_path = inp.label_manifest_path.with_suffix(
        inp.label_manifest_path.suffix + ".sha256"
    )
    label_parquet_sidecar_first_64 = read_sidecar_first_64(
        label_parquet_sidecar_path
    )
    label_manifest_sidecar_first_64 = read_sidecar_first_64(
        label_manifest_sidecar_path
    )

    label_manifest = parse_manifest_bytes(label_manifest_bytes)

    source_feature_parquet_sha_pre: str | None = None
    source_feature_manifest_sha_pre: str | None = None
    source_feature_table: pa.Table | None = None
    if inp.source_feature_parquet_path is not None:
        source_feature_parquet_sha_pre = compute_file_sha256(
            inp.source_feature_parquet_path
        )
        source_feature_table = load_parquet_table(inp.source_feature_parquet_path)
    if inp.source_feature_manifest_path is not None:
        source_feature_manifest_sha_pre = compute_file_sha256(
            inp.source_feature_manifest_path
        )

    # Read parquet
    label_table = load_parquet_table(inp.label_parquet_path)

    # Gitignore evidence
    gitignore_paths = [
        "data/microstructure/",
        "data/microstructure/labels/",
        "data/microstructure/manifests/",
        "data/microstructure/gate-reports/labels/",
    ]
    gitignore_results = query_gitignore_status(inp.repo_root, gitignore_paths)

    # Re-hash all source artefacts post-checks-pre-context to establish
    # the "during the gate run nothing changed" immutability proof. The
    # context's measured dict carries both pre and post SHAs for
    # Group J consumption.
    label_parquet_sha_post = compute_file_sha256(inp.label_parquet_path)
    label_manifest_sha_post = compute_file_sha256(inp.label_manifest_path)
    source_feature_parquet_sha_post = (
        compute_file_sha256(inp.source_feature_parquet_path)
        if inp.source_feature_parquet_path is not None
        else None
    )
    source_feature_manifest_sha_post = (
        compute_file_sha256(inp.source_feature_manifest_path)
        if inp.source_feature_manifest_path is not None
        else None
    )

    ctx = LabelGateContext(
        label_parquet_path=inp.label_parquet_path,
        label_parquet_sidecar_path=label_parquet_sidecar_path,
        label_manifest_path=inp.label_manifest_path,
        label_manifest_sidecar_path=label_manifest_sidecar_path,
        source_feature_parquet_path=inp.source_feature_parquet_path,
        source_feature_manifest_path=inp.source_feature_manifest_path,
        label_manifest=label_manifest,
        label_manifest_bytes=label_manifest_bytes,
        label_manifest_sha=label_manifest_sha_pre,
        label_manifest_sidecar_first_64=label_manifest_sidecar_first_64,
        label_table=label_table,
        source_feature_table=source_feature_table,
        label_parquet_sha=label_parquet_sha_pre,
        label_parquet_sidecar_first_64=label_parquet_sidecar_first_64,
        source_feature_parquet_sha=source_feature_parquet_sha_pre,
        source_feature_manifest_sha=source_feature_manifest_sha_pre,
        gitignore_results=gitignore_results,
        measured={
            "label_parquet_sha_pre": label_parquet_sha_pre,
            "label_parquet_sha_post": label_parquet_sha_post,
            "label_manifest_sha_pre": label_manifest_sha_pre,
            "label_manifest_sha_post": label_manifest_sha_post,
            "source_feature_parquet_sha_pre": source_feature_parquet_sha_pre,
            "source_feature_parquet_sha_post": source_feature_parquet_sha_post,
            "source_feature_manifest_sha_pre": source_feature_manifest_sha_pre,
            "source_feature_manifest_sha_post": source_feature_manifest_sha_post,
        },
    )

    checks = run_all_checks(ctx)
    overall = _classify_overall(checks)
    if len(checks) != len(CHECK_ORDER):  # pragma: no cover - defensive
        raise LabelGateError(
            f"check count drift: got {len(checks)} expected {len(CHECK_ORDER)}"
        )

    boundary_confirmations = _build_boundary_confirmations(
        label_parquet_sha_pre=label_parquet_sha_pre,
        label_parquet_sha_post=label_parquet_sha_post,
        label_manifest_sha_pre=label_manifest_sha_pre,
        label_manifest_sha_post=label_manifest_sha_post,
        source_feature_parquet_sha_pre=source_feature_parquet_sha_pre,
        source_feature_parquet_sha_post=source_feature_parquet_sha_post,
        source_feature_manifest_sha_pre=source_feature_manifest_sha_pre,
        source_feature_manifest_sha_post=source_feature_manifest_sha_post,
    )

    eligibility_gate_status_after = (
        "pass_report_level_only"
        if overall == LabelGateCheckStatus.PASS
        else "fail_report_level_only"
    )

    observed_invalid_price_row_count = label_manifest.get(
        "invalid_price_row_count", -1
    )
    observed_censored_per_horizon_raw = label_manifest.get(
        "censored_per_horizon", {}
    )
    observed_censored_per_horizon: dict[str, int] = {
        k: int(v)
        for k, v in observed_censored_per_horizon_raw.items()
        if isinstance(v, int) or (isinstance(v, str) and v.isdigit())
    }

    measured_summary: dict[str, Any] = {
        "label_parquet_path": str(inp.label_parquet_path),
        "label_parquet_sha_pre": label_parquet_sha_pre,
        "label_parquet_sha_post": label_parquet_sha_post,
        "label_manifest_path": str(inp.label_manifest_path),
        "label_manifest_sha_pre": label_manifest_sha_pre,
        "label_manifest_sha_post": label_manifest_sha_post,
        "source_feature_parquet_sha_pre": source_feature_parquet_sha_pre,
        "source_feature_parquet_sha_post": source_feature_parquet_sha_post,
        "source_feature_manifest_sha_pre": source_feature_manifest_sha_pre,
        "source_feature_manifest_sha_post": source_feature_manifest_sha_post,
        "label_parquet_row_count": label_table.num_rows,
        "label_parquet_column_count": len(label_table.column_names),
        "label_manifest_row_count": label_manifest.get("row_count"),
        "label_manifest_invalid_price_row_count": observed_invalid_price_row_count,
        "label_manifest_censored_per_horizon": observed_censored_per_horizon,
    }

    input_artefacts: Mapping[str, Any] = {
        "source_label_parquet_path": str(inp.label_parquet_path),
        "source_label_parquet_sha256": label_parquet_sha_pre,
        "source_label_manifest_path": str(inp.label_manifest_path),
        "source_label_manifest_sha256": label_manifest_sha_pre,
        "source_feature_parquet_path": (
            str(inp.source_feature_parquet_path)
            if inp.source_feature_parquet_path
            else ""
        ),
        "source_feature_parquet_sha256": source_feature_parquet_sha_pre or "",
        "source_feature_manifest_path": (
            str(inp.source_feature_manifest_path)
            if inp.source_feature_manifest_path
            else ""
        ),
        "source_feature_manifest_sha256": source_feature_manifest_sha_pre or "",
        "expected_label_parquet_sha256": EXPECTED_LABEL_PARQUET_SHA,
        "expected_label_manifest_sha256": EXPECTED_LABEL_MANIFEST_SHA,
        "expected_label_config_hash": EXPECTED_LABEL_CONFIG_HASH,
        "expected_source_feature_parquet_sha256": EXPECTED_SOURCE_FEATURE_PARQUET_SHA,
        "expected_source_feature_manifest_sha256": (
            EXPECTED_SOURCE_FEATURE_MANIFEST_SHA
        ),
        "expected_source_feature_successor_state_sha256": (
            EXPECTED_SOURCE_FEATURE_SUCCESSOR_STATE_SHA
        ),
        "expected_source_phase_4bi_b_gate_report_sha256": (
            EXPECTED_SOURCE_PHASE_4BI_B_GATE_REPORT_SHA
        ),
        "expected_source_normalized_parquet_sha256": (
            EXPECTED_SOURCE_NORMALIZED_PARQUET_SHA
        ),
    }

    expected_label_columns = [c for c in LABEL_SCHEMA_V001 if c in LABEL_NAMES_V001]
    expected_support_columns = [
        c for c in LABEL_SCHEMA_V001 if c in LABEL_SUPPORT_COLUMN_NAMES_V001
    ]
    expected_lineage_columns = [
        c for c in LABEL_SCHEMA_V001 if c in LABEL_LINEAGE_COLUMNS_V001
    ]
    observed_label_columns = [
        c for c in label_table.column_names if c in LABEL_NAMES_V001
    ]
    observed_support_columns = [
        c for c in label_table.column_names if c in LABEL_SUPPORT_COLUMN_NAMES_V001
    ]
    observed_lineage_columns = [
        c for c in label_table.column_names if c in LABEL_LINEAGE_COLUMNS_V001
    ]

    generated_at_unix_ms = int(time.time() * 1000)
    short_commit = inp.code_commit_sha[:12]
    report_id = (
        f"{EXPECTED_DATASET_FAMILY}__{EXPECTED_DATASET_VERSION}__phase-4bj-e__"
        f"{generated_at_unix_ms}__{short_commit}"
    )

    report_path: Path | None = None
    sidecar_path: Path | None = None
    report_sha: str | None = None
    report_size: int | None = None
    if inp.write_report:
        report = build_label_gate_report(
            report_id=report_id,
            dataset_family=EXPECTED_DATASET_FAMILY,
            dataset_version=EXPECTED_DATASET_VERSION,
            label_schema_version=EXPECTED_LABEL_SCHEMA_VERSION,
            symbol=EXPECTED_SYMBOL,
            utc_date=EXPECTED_UTC_DATE,
            generated_at_unix_ms=generated_at_unix_ms,
            code_commit_sha=inp.code_commit_sha,
            input_artefacts=input_artefacts,
            expected_row_count=EXPECTED_ROW_COUNT,
            observed_row_count=label_table.num_rows,
            expected_schema_columns=list(LABEL_SCHEMA_V001),
            observed_schema_columns=list(label_table.column_names),
            expected_label_columns=expected_label_columns,
            observed_label_columns=observed_label_columns,
            expected_support_columns=expected_support_columns,
            observed_support_columns=observed_support_columns,
            expected_lineage_columns=expected_lineage_columns,
            observed_lineage_columns=observed_lineage_columns,
            label_config_hash=label_manifest.get(
                "label_config_hash", EXPECTED_LABEL_CONFIG_HASH
            ),
            expected_invalid_price_row_count=EXPECTED_INVALID_PRICE_ROW_COUNT,
            observed_invalid_price_row_count=observed_invalid_price_row_count,
            expected_censored_per_horizon=EXPECTED_CENSORED_PER_HORIZON,
            observed_censored_per_horizon=observed_censored_per_horizon,
            checks=[c.to_dict() for c in checks],
            overall_status=overall.value,
            eligibility_gate_status_after=eligibility_gate_status_after,
            boundary_confirmations=boundary_confirmations,
            measured_summary=measured_summary,
        )
        # Derive the canonical leaf directory:
        # ``data/microstructure/gate-reports/labels/``. The
        # orchestrator's ``output_root`` is the microstructure root
        # (or a deeper directory beneath it); we append the canonical
        # ``gate-reports/labels/`` segment if it is not already
        # present.
        leaf = inp.output_root
        leaf_parts = tuple(p.name for p in [leaf, *leaf.parents])
        if "labels" not in leaf_parts or "gate-reports" not in leaf_parts:
            leaf = inp.output_root / "gate-reports" / "labels"
        leaf.mkdir(parents=True, exist_ok=True)
        paths, report_sha, report_size = write_label_gate_report(
            report, output_root=leaf, refuse_overwrite=True
        )
        report_path = paths.report_path
        sidecar_path = paths.sidecar_path
        report_id = paths.report_id

    return LabelGateResult(
        overall_status=overall,
        research_eligible_after=False,
        eligibility_gate_status_after=eligibility_gate_status_after,
        label_manifest_research_eligible_after=False,
        label_manifest_eligibility_gate_status_after="pending",
        label_manifest_chronological_split_policy_after="not_yet_defined",
        stage_5_authorized=False,
        stage_5_research_or_ml_use=False,
        no_successor_authorization=True,
        checks=checks,
        report_path=report_path,
        sidecar_path=sidecar_path,
        report_id=report_id,
        report_sha256=report_sha,
        report_size_bytes=report_size,
        boundary_confirmations=boundary_confirmations,
        measured_summary=measured_summary,
    )
