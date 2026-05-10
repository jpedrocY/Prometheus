"""Phase 4bi-B feature-family eligibility-gate orchestrator.

Reads the Phase 4bh feature artefacts read-only, runs the Phase 4bi-B
check suite, calls :func:`features_validation.validate_feature_dataset`
as additional read-only evidence, and (when ``write_report=True``)
atomically emits a JSON gate report plus paired SHA256 sidecar under
``data/microstructure/gate-reports/features/``. Never mutates any
source artefact. Never flips ``research_eligible``.
"""
from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .feature_gate_checks import (
    CHECK_ORDER,
    EXPECTED_FEATURE_CONFIG_HASH,
    EXPECTED_NORMALIZED_MANIFEST_SHA,
    EXPECTED_NORMALIZED_PARQUET_SHA,
    EXPECTED_PHASE_4BB_D_GATE_REPORT_SHA,
    EXPECTED_PHASE_4BF_GATE_REPORT_SHA,
    EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA,
    EXPECTED_RAW_MANIFEST_SHA,
    EXPECTED_RAW_ZIP_SHA,
    EXPECTED_ROW_COUNT,
    FeatureGateCheckResult,
    FeatureGateCheckStatus,
    FeatureGateContext,
    load_parquet_table,
    query_gitignore_status,
    run_all_checks,
)
from .feature_gate_io import (
    FeatureGateIOError,
    assert_path_under_microstructure,
    compute_bytes_sha256,
    compute_file_sha256,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
)
from .feature_gate_report import (
    build_feature_gate_report,
    write_feature_gate_report,
)
from .features_schema import (
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_V001,
    FEATURE_SCHEMA_VERSION,
    LINEAGE_COLUMNS_V001,
)
from .features_validation import (
    FeatureCheckStatus,
    validate_feature_dataset,
)


class FeatureGateError(RuntimeError):
    """Raised on input-construction or gate-run errors."""


@dataclass(frozen=True)
class FeatureGateInput:
    """Frozen orchestrator input for the Phase 4bi-B gate."""

    feature_parquet_path: Path
    feature_manifest_path: Path
    source_normalized_parquet_path: Path
    source_normalized_manifest_path: Path
    source_raw_manifest_path: Path
    output_root: Path
    code_commit_sha: str
    repo_root: Path
    raw_zip_path: Path | None = None
    phase_4bb_d_gate_report_path: Path | None = None
    phase_4bf_gate_report_path: Path | None = None
    phase_4bg_b_successor_state_path: Path | None = None
    write_report: bool = True

    def __post_init__(self) -> None:
        for attr in (
            "feature_parquet_path",
            "feature_manifest_path",
            "source_normalized_parquet_path",
            "source_normalized_manifest_path",
            "source_raw_manifest_path",
            "output_root",
            "repo_root",
        ):
            v = getattr(self, attr)
            if not isinstance(v, Path):
                raise FeatureGateError(f"{attr} must be Path; got {type(v).__name__}")
        for attr in (
            "raw_zip_path",
            "phase_4bb_d_gate_report_path",
            "phase_4bf_gate_report_path",
            "phase_4bg_b_successor_state_path",
        ):
            v = getattr(self, attr)
            if v is not None and not isinstance(v, Path):
                raise FeatureGateError(
                    f"{attr} must be Path or None; got {type(v).__name__}"
                )
        if not self.code_commit_sha or not isinstance(self.code_commit_sha, str):
            raise FeatureGateError("code_commit_sha must be a non-empty str")
        try:
            assert_path_under_microstructure(
                self.feature_parquet_path, label="feature_parquet_path"
            )
            assert_path_under_microstructure(
                self.feature_manifest_path, label="feature_manifest_path"
            )
            assert_path_under_microstructure(self.output_root, label="output_root")
        except FeatureGateIOError as exc:
            raise FeatureGateError(str(exc)) from exc


@dataclass(frozen=True)
class FeatureGateResult:
    """Frozen orchestrator result for the Phase 4bi-B gate."""

    overall_status: FeatureGateCheckStatus
    research_eligible_after: bool
    eligibility_gate_status_after: str
    feature_manifest_research_eligible_after: bool
    feature_manifest_eligibility_gate_status_after: str
    stage_5_authorized: bool
    stage_5_research_or_ml_use: bool
    no_successor_authorization: bool
    checks: tuple[FeatureGateCheckResult, ...]
    report_path: Path | None
    sidecar_path: Path | None
    report_id: str
    report_sha256: str | None
    report_size_bytes: int | None
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any] = field(default_factory=dict)


_BOUNDARY_KEYS = (
    "no_feature_manifest_mutation",
    "no_source_artefact_mutation",
    "no_data_microstructure_write_outside_gate_reports_features",
    "no_label_computed",
    "no_signal_computed",
    "no_ml_trained",
    "no_strategy_created",
    "no_backtest_run",
    "no_acquisition",
    "no_network_io",
    "no_websocket",
    "no_credential_read",
    "no_env_read",
    "no_mcp_or_graphify",
    "feature_manifest_research_eligible_after_is_false",
    "stage_5_research_or_ml_use_is_false",
    "no_successor_authorization",
)


def _classify_overall(
    checks: tuple[FeatureGateCheckResult, ...],
) -> FeatureGateCheckStatus:
    """PASS only if all checks PASS or NOT_APPLICABLE; FAIL > ERROR > PASS."""
    has_fail = any(c.status == FeatureGateCheckStatus.FAIL for c in checks)
    if has_fail:
        return FeatureGateCheckStatus.FAIL
    has_error = any(c.status == FeatureGateCheckStatus.ERROR for c in checks)
    if has_error:
        return FeatureGateCheckStatus.ERROR
    return FeatureGateCheckStatus.PASS


def _build_boundary_confirmations(
    *,
    feature_parquet_sha_pre: str,
    feature_parquet_sha_post: str,
    feature_manifest_sha_pre: str,
    feature_manifest_sha_post: str,
    normalized_parquet_sha_pre: str,
    normalized_parquet_sha_post: str,
    normalized_manifest_sha_pre: str,
    normalized_manifest_sha_post: str,
    raw_manifest_sha_pre: str,
    raw_manifest_sha_post: str,
    raw_zip_sha_pre: str | None,
    raw_zip_sha_post: str | None,
    phase_4bb_d_sha_pre: str | None,
    phase_4bb_d_sha_post: str | None,
    phase_4bf_sha_pre: str | None,
    phase_4bf_sha_post: str | None,
    phase_4bg_b_sha_pre: str | None,
    phase_4bg_b_sha_post: str | None,
) -> dict[str, bool]:
    feature_manifest_unchanged = feature_manifest_sha_pre == feature_manifest_sha_post
    source_unchanged = (
        feature_parquet_sha_pre == feature_parquet_sha_post
        and normalized_parquet_sha_pre == normalized_parquet_sha_post
        and normalized_manifest_sha_pre == normalized_manifest_sha_post
        and raw_manifest_sha_pre == raw_manifest_sha_post
        and (raw_zip_sha_pre == raw_zip_sha_post)
        and (phase_4bb_d_sha_pre == phase_4bb_d_sha_post)
        and (phase_4bf_sha_pre == phase_4bf_sha_post)
        and (phase_4bg_b_sha_pre == phase_4bg_b_sha_post)
    )
    return {
        "no_feature_manifest_mutation": feature_manifest_unchanged,
        "no_source_artefact_mutation": source_unchanged,
        "no_data_microstructure_write_outside_gate_reports_features": True,
        "no_label_computed": True,
        "no_signal_computed": True,
        "no_ml_trained": True,
        "no_strategy_created": True,
        "no_backtest_run": True,
        "no_acquisition": True,
        "no_network_io": True,
        "no_websocket": True,
        "no_credential_read": True,
        "no_env_read": True,
        "no_mcp_or_graphify": True,
        "feature_manifest_research_eligible_after_is_false": True,
        "stage_5_research_or_ml_use_is_false": True,
        "no_successor_authorization": True,
    }


def validate_feature_gate_inputs(inp: FeatureGateInput) -> None:
    """Verify all required input artefacts exist and are readable.

    Raises :class:`FeatureGateError` on the first failure.
    """
    must_exist: list[tuple[str, Path]] = [
        ("feature_parquet_path", inp.feature_parquet_path),
        ("feature_manifest_path", inp.feature_manifest_path),
        ("source_normalized_parquet_path", inp.source_normalized_parquet_path),
        ("source_normalized_manifest_path", inp.source_normalized_manifest_path),
        ("source_raw_manifest_path", inp.source_raw_manifest_path),
    ]
    for label, p in must_exist:
        if not p.exists():
            raise FeatureGateError(f"{label} does not exist: {p}")
    sidecar_p = inp.feature_parquet_path.with_suffix(
        inp.feature_parquet_path.suffix + ".sha256"
    )
    if not sidecar_p.exists():
        raise FeatureGateError(f"feature parquet sidecar does not exist: {sidecar_p}")
    sidecar_m = inp.feature_manifest_path.with_suffix(
        inp.feature_manifest_path.suffix + ".sha256"
    )
    if not sidecar_m.exists():
        raise FeatureGateError(f"feature manifest sidecar does not exist: {sidecar_m}")


def run_feature_family_gate(inp: FeatureGateInput) -> FeatureGateResult:
    """Run the Phase 4bi-B feature-family eligibility gate exactly once."""

    validate_feature_gate_inputs(inp)

    # Pre-run hashes (immutability anchor)
    feature_parquet_sha_pre = compute_file_sha256(inp.feature_parquet_path)
    feature_manifest_bytes = read_manifest_bytes(inp.feature_manifest_path)
    feature_manifest_sha_pre = compute_bytes_sha256(feature_manifest_bytes)
    feature_parquet_sidecar_path = inp.feature_parquet_path.with_suffix(
        inp.feature_parquet_path.suffix + ".sha256"
    )
    feature_manifest_sidecar_path = inp.feature_manifest_path.with_suffix(
        inp.feature_manifest_path.suffix + ".sha256"
    )
    feature_parquet_sidecar_first_64 = read_sidecar_first_64(
        feature_parquet_sidecar_path
    )
    feature_manifest_sidecar_first_64 = read_sidecar_first_64(
        feature_manifest_sidecar_path
    )

    feature_manifest = parse_manifest_bytes(feature_manifest_bytes)

    normalized_parquet_sha_pre = compute_file_sha256(
        inp.source_normalized_parquet_path
    )
    normalized_manifest_bytes = read_manifest_bytes(
        inp.source_normalized_manifest_path
    )
    normalized_manifest_sha_pre = compute_bytes_sha256(normalized_manifest_bytes)
    source_normalized_manifest = parse_manifest_bytes(normalized_manifest_bytes)

    raw_manifest_bytes = read_manifest_bytes(inp.source_raw_manifest_path)
    raw_manifest_sha_pre = compute_bytes_sha256(raw_manifest_bytes)
    raw_manifest = parse_manifest_bytes(raw_manifest_bytes)

    raw_zip_sha_pre = (
        compute_file_sha256(inp.raw_zip_path) if inp.raw_zip_path else None
    )
    phase_4bb_d_sha_pre = (
        compute_file_sha256(inp.phase_4bb_d_gate_report_path)
        if inp.phase_4bb_d_gate_report_path
        else None
    )
    phase_4bf_sha_pre = (
        compute_file_sha256(inp.phase_4bf_gate_report_path)
        if inp.phase_4bf_gate_report_path
        else None
    )
    phase_4bg_b_sha_pre = (
        compute_file_sha256(inp.phase_4bg_b_successor_state_path)
        if inp.phase_4bg_b_successor_state_path
        else None
    )

    # Read parquets
    feature_table = load_parquet_table(inp.feature_parquet_path)
    source_normalized_table = load_parquet_table(inp.source_normalized_parquet_path)

    # Run validate_feature_dataset for cross-evidence
    validate_overall_status: str = "fail"
    validate_failed_checks: tuple[str, ...] = ()
    try:
        result = validate_feature_dataset(
            feature_parquet_path=inp.feature_parquet_path,
            feature_manifest_path=inp.feature_manifest_path,
            source_normalized_parquet_path=inp.source_normalized_parquet_path,
            source_normalized_manifest_sha256=normalized_manifest_sha_pre,
            source_normalized_parquet_sha256=normalized_parquet_sha_pre,
            source_successor_state_sha256=(
                phase_4bg_b_sha_pre or EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA
            ),
            source_phase_4bf_gate_report_sha256=(
                phase_4bf_sha_pre or EXPECTED_PHASE_4BF_GATE_REPORT_SHA
            ),
            feature_config_hash=feature_manifest.get(
                "feature_config_hash", EXPECTED_FEATURE_CONFIG_HASH
            ),
        )
        validate_overall_status = result.overall_status.value
        validate_failed_checks = tuple(
            c.check_id for c in result.checks if c.status != FeatureCheckStatus.PASS
        )
    except Exception as exc:  # pragma: no cover - defensive
        validate_overall_status = "error"
        validate_failed_checks = (f"{type(exc).__name__}: {exc}",)

    # Gitignore evidence
    gitignore_paths = [
        "data/microstructure/",
        "data/microstructure/features/",
        "data/microstructure/manifests/",
        "data/microstructure/gate-reports/features/",
    ]
    gitignore_results = query_gitignore_status(inp.repo_root, gitignore_paths)

    ctx = FeatureGateContext(
        feature_parquet_path=inp.feature_parquet_path,
        feature_parquet_sidecar_path=feature_parquet_sidecar_path,
        feature_manifest_path=inp.feature_manifest_path,
        feature_manifest_sidecar_path=feature_manifest_sidecar_path,
        source_normalized_parquet_path=inp.source_normalized_parquet_path,
        source_normalized_manifest_path=inp.source_normalized_manifest_path,
        source_raw_manifest_path=inp.source_raw_manifest_path,
        feature_manifest=feature_manifest,
        feature_manifest_bytes=feature_manifest_bytes,
        feature_manifest_sha=feature_manifest_sha_pre,
        feature_manifest_sidecar_first_64=feature_manifest_sidecar_first_64,
        source_normalized_manifest=source_normalized_manifest,
        source_normalized_manifest_sha=normalized_manifest_sha_pre,
        raw_manifest=raw_manifest,
        raw_manifest_sha=raw_manifest_sha_pre,
        feature_parquet_sha=feature_parquet_sha_pre,
        feature_parquet_sidecar_first_64=feature_parquet_sidecar_first_64,
        source_normalized_parquet_sha=normalized_parquet_sha_pre,
        raw_zip_sha=raw_zip_sha_pre,
        phase_4bb_d_gate_report_sha=phase_4bb_d_sha_pre,
        phase_4bf_gate_report_sha=phase_4bf_sha_pre,
        phase_4bg_b_successor_state_sha=phase_4bg_b_sha_pre,
        feature_table=feature_table,
        source_normalized_table=source_normalized_table,
        validate_overall_status=validate_overall_status,
        validate_failed_checks=validate_failed_checks,
        gitignore_results=gitignore_results,
    )

    checks = run_all_checks(ctx)
    overall = _classify_overall(checks)
    if len(checks) != len(CHECK_ORDER):  # pragma: no cover - defensive
        raise FeatureGateError(
            f"check count drift: got {len(checks)} expected {len(CHECK_ORDER)}"
        )

    # Re-hash all source artefacts post-checks to confirm immutability.
    feature_parquet_sha_post = compute_file_sha256(inp.feature_parquet_path)
    feature_manifest_sha_post = compute_file_sha256(inp.feature_manifest_path)
    normalized_parquet_sha_post = compute_file_sha256(
        inp.source_normalized_parquet_path
    )
    normalized_manifest_sha_post = compute_file_sha256(
        inp.source_normalized_manifest_path
    )
    raw_manifest_sha_post = compute_file_sha256(inp.source_raw_manifest_path)
    raw_zip_sha_post = (
        compute_file_sha256(inp.raw_zip_path) if inp.raw_zip_path else None
    )
    phase_4bb_d_sha_post = (
        compute_file_sha256(inp.phase_4bb_d_gate_report_path)
        if inp.phase_4bb_d_gate_report_path
        else None
    )
    phase_4bf_sha_post = (
        compute_file_sha256(inp.phase_4bf_gate_report_path)
        if inp.phase_4bf_gate_report_path
        else None
    )
    phase_4bg_b_sha_post = (
        compute_file_sha256(inp.phase_4bg_b_successor_state_path)
        if inp.phase_4bg_b_successor_state_path
        else None
    )

    boundary_confirmations = _build_boundary_confirmations(
        feature_parquet_sha_pre=feature_parquet_sha_pre,
        feature_parquet_sha_post=feature_parquet_sha_post,
        feature_manifest_sha_pre=feature_manifest_sha_pre,
        feature_manifest_sha_post=feature_manifest_sha_post,
        normalized_parquet_sha_pre=normalized_parquet_sha_pre,
        normalized_parquet_sha_post=normalized_parquet_sha_post,
        normalized_manifest_sha_pre=normalized_manifest_sha_pre,
        normalized_manifest_sha_post=normalized_manifest_sha_post,
        raw_manifest_sha_pre=raw_manifest_sha_pre,
        raw_manifest_sha_post=raw_manifest_sha_post,
        raw_zip_sha_pre=raw_zip_sha_pre,
        raw_zip_sha_post=raw_zip_sha_post,
        phase_4bb_d_sha_pre=phase_4bb_d_sha_pre,
        phase_4bb_d_sha_post=phase_4bb_d_sha_post,
        phase_4bf_sha_pre=phase_4bf_sha_pre,
        phase_4bf_sha_post=phase_4bf_sha_post,
        phase_4bg_b_sha_pre=phase_4bg_b_sha_pre,
        phase_4bg_b_sha_post=phase_4bg_b_sha_post,
    )

    eligibility_gate_status_after = (
        "pass_report_level_only"
        if overall == FeatureGateCheckStatus.PASS
        else "fail_report_level_only"
    )

    measured_summary: dict[str, Any] = {
        "feature_parquet_path": str(inp.feature_parquet_path),
        "feature_parquet_sha_pre": feature_parquet_sha_pre,
        "feature_parquet_sha_post": feature_parquet_sha_post,
        "feature_manifest_path": str(inp.feature_manifest_path),
        "feature_manifest_sha_pre": feature_manifest_sha_pre,
        "feature_manifest_sha_post": feature_manifest_sha_post,
        "source_normalized_parquet_sha_pre": normalized_parquet_sha_pre,
        "source_normalized_parquet_sha_post": normalized_parquet_sha_post,
        "source_normalized_manifest_sha_pre": normalized_manifest_sha_pre,
        "source_normalized_manifest_sha_post": normalized_manifest_sha_post,
        "raw_manifest_sha_pre": raw_manifest_sha_pre,
        "raw_manifest_sha_post": raw_manifest_sha_post,
        "raw_zip_sha_pre": raw_zip_sha_pre,
        "raw_zip_sha_post": raw_zip_sha_post,
        "phase_4bb_d_gate_report_sha_pre": phase_4bb_d_sha_pre,
        "phase_4bb_d_gate_report_sha_post": phase_4bb_d_sha_post,
        "phase_4bf_gate_report_sha_pre": phase_4bf_sha_pre,
        "phase_4bf_gate_report_sha_post": phase_4bf_sha_post,
        "phase_4bg_b_successor_state_sha_pre": phase_4bg_b_sha_pre,
        "phase_4bg_b_successor_state_sha_post": phase_4bg_b_sha_post,
        "feature_parquet_row_count": feature_table.num_rows,
        "feature_parquet_column_count": len(feature_table.column_names),
        "validate_feature_dataset_overall_status": validate_overall_status,
        "validate_feature_dataset_failed_checks": list(validate_failed_checks),
    }

    input_artefacts: Mapping[str, Any] = {
        "source_feature_parquet_path": str(inp.feature_parquet_path),
        "source_feature_parquet_sha256": feature_parquet_sha_pre,
        "source_feature_manifest_path": str(inp.feature_manifest_path),
        "source_feature_manifest_sha256": feature_manifest_sha_pre,
        "source_normalized_parquet_path": str(inp.source_normalized_parquet_path),
        "source_normalized_parquet_sha256": normalized_parquet_sha_pre,
        "source_normalized_manifest_path": str(inp.source_normalized_manifest_path),
        "source_normalized_manifest_sha256": normalized_manifest_sha_pre,
        "source_raw_manifest_path": str(inp.source_raw_manifest_path),
        "source_raw_manifest_sha256": raw_manifest_sha_pre,
        "source_raw_zip_path": (
            str(inp.raw_zip_path) if inp.raw_zip_path else ""
        ),
        "source_raw_zip_sha256": raw_zip_sha_pre or "",
        "source_phase_4bb_d_gate_report_path": (
            str(inp.phase_4bb_d_gate_report_path)
            if inp.phase_4bb_d_gate_report_path
            else ""
        ),
        "source_phase_4bb_d_gate_report_sha256": phase_4bb_d_sha_pre or "",
        "source_phase_4bf_gate_report_path": (
            str(inp.phase_4bf_gate_report_path)
            if inp.phase_4bf_gate_report_path
            else ""
        ),
        "source_phase_4bf_gate_report_sha256": phase_4bf_sha_pre or "",
        "source_phase_4bg_b_successor_state_path": (
            str(inp.phase_4bg_b_successor_state_path)
            if inp.phase_4bg_b_successor_state_path
            else ""
        ),
        "source_phase_4bg_b_successor_state_sha256": phase_4bg_b_sha_pre or "",
        "source_phase_4bh_merge_commit": "03100d4267e0984342c622c88cb204218f953367",
        "source_phase_4bi_a_merge_commit": "97f9d760698d89900fb4c43d57c7bbc559c8a52e",
        "expected_feature_parquet_sha256": (
            "618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f"
        ),
        "expected_feature_manifest_sha256": (
            "624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718"
        ),
        "expected_normalized_parquet_sha256": EXPECTED_NORMALIZED_PARQUET_SHA,
        "expected_normalized_manifest_sha256": EXPECTED_NORMALIZED_MANIFEST_SHA,
        "expected_raw_manifest_sha256": EXPECTED_RAW_MANIFEST_SHA,
        "expected_raw_zip_sha256": EXPECTED_RAW_ZIP_SHA,
        "expected_phase_4bb_d_gate_report_sha256": (
            EXPECTED_PHASE_4BB_D_GATE_REPORT_SHA
        ),
        "expected_phase_4bf_gate_report_sha256": EXPECTED_PHASE_4BF_GATE_REPORT_SHA,
        "expected_phase_4bg_b_successor_state_sha256": (
            EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA
        ),
    }

    expected_feature_columns = [
        c for c in FEATURE_SCHEMA_V001 if c in FEATURE_NAMES_V001
    ]
    expected_lineage_columns = [
        c for c in FEATURE_SCHEMA_V001 if c in LINEAGE_COLUMNS_V001
    ]
    observed_feature_columns = [
        c for c in feature_table.column_names if c in FEATURE_NAMES_V001
    ]
    observed_lineage_columns = [
        c for c in feature_table.column_names if c in LINEAGE_COLUMNS_V001
    ]

    generated_at_unix_ms = int(time.time() * 1000)
    short_commit = inp.code_commit_sha[:12]
    report_id = (
        f"{FEATURE_DATASET_FAMILY}__{FEATURE_DATASET_VERSION}__phase-4bi-b__"
        f"{generated_at_unix_ms}__{short_commit}"
    )

    report_path: Path | None = None
    sidecar_path: Path | None = None
    report_sha: str | None = None
    report_size: int | None = None
    if inp.write_report:
        report = build_feature_gate_report(
            report_id=report_id,
            dataset_family=FEATURE_DATASET_FAMILY,
            dataset_version=FEATURE_DATASET_VERSION,
            feature_schema_version=FEATURE_SCHEMA_VERSION,
            symbol="BTCUSDT",
            utc_date="2025-01-15",
            generated_at_unix_ms=generated_at_unix_ms,
            code_commit_sha=inp.code_commit_sha,
            input_artefacts=input_artefacts,
            expected_row_count=EXPECTED_ROW_COUNT,
            observed_row_count=feature_table.num_rows,
            expected_schema_columns=list(FEATURE_SCHEMA_V001),
            observed_schema_columns=list(feature_table.column_names),
            expected_feature_columns=expected_feature_columns,
            observed_feature_columns=observed_feature_columns,
            expected_lineage_columns=expected_lineage_columns,
            observed_lineage_columns=observed_lineage_columns,
            feature_config_hash=feature_manifest.get(
                "feature_config_hash", EXPECTED_FEATURE_CONFIG_HASH
            ),
            checks=[c.to_dict() for c in checks],
            overall_status=overall.value,
            eligibility_gate_status_after=eligibility_gate_status_after,
            boundary_confirmations=boundary_confirmations,
            measured_summary=measured_summary,
        )
        # Derive the canonical leaf directory:
        # ``data/microstructure/gate-reports/features/``. The
        # orchestrator's ``output_root`` is the microstructure root
        # (or a deeper directory beneath it); we append the canonical
        # ``gate-reports/features/`` segment if it is not already
        # present.
        leaf = inp.output_root
        leaf_parts = tuple(p.name for p in [leaf, *leaf.parents])
        if "features" not in leaf_parts or "gate-reports" not in leaf_parts:
            leaf = inp.output_root / "gate-reports" / "features"
        leaf.mkdir(parents=True, exist_ok=True)
        paths, report_sha, report_size = write_feature_gate_report(
            report, output_root=leaf, refuse_overwrite=True
        )
        report_path = paths.report_path
        sidecar_path = paths.sidecar_path
        report_id = paths.report_id

    return FeatureGateResult(
        overall_status=overall,
        research_eligible_after=False,
        eligibility_gate_status_after=eligibility_gate_status_after,
        feature_manifest_research_eligible_after=False,
        feature_manifest_eligibility_gate_status_after="pending",
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
