"""Phase 4bj-C label dataset validation.

Offline read-only validator that proves a previously written label
parquet + manifest pair matches the Phase 4bj-B locked schema and the
project's no-rescue / no-leakage contract:

- exact 39-column schema and order;
- exact row_count parity vs feature parquet and label manifest;
- no forbidden substrings (per Phase 4bj-B);
- lineage hash columns constant and matching the requested values;
- ``label_config_hash`` constant across rows and matching the manifest;
- ``feature_timestamp_ms == source_transact_time_ms`` for every row;
- ``forward_log_return_*`` values are null or finite (no NaN / inf);
- ``forward_direction_*`` values are null or in ``{-1, 0, 1}``;
- ``reference_row_index_*`` values are null or valid feature row indices;
- ``reference_timestamp_ms_*`` values are null or ``<= target_ts`` per
  horizon;
- ``horizon_censored_flag_*`` is strict bool and equals
  ``target_ts > final_source_T``;
- ``label_invalid_price_flag`` and ``label_any_censored_flag`` are
  strict bool;
- ``label_any_censored_flag`` equals OR of the per-horizon flags;
- censored counts match observed counts;
- label parquet SHA matches paired sidecar;
- label manifest SHA matches paired sidecar;
- label manifest declares ``research_eligible=False`` and
  ``eligibility_gate_status="pending"``;
- upstream feature parquet, feature manifest, Phase 4bi-D successor-
  state, Phase 4bi-B gate report, normalized parquet, original
  derived manifest, raw manifest, and raw zip SHAs unchanged.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute labels or signals;
- does NOT mutate any artefact;
- does NOT create a gate report (the validator returns an in-memory
  result; no Phase 4bj-C output is a gate-report file).
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .labels_schema import (
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS,
    LABEL_DATASET_FAMILY_V001,
    LABEL_DATASET_VERSION_V001,
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_LINEAGE_COLUMNS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_V001,
    LABEL_SCHEMA_VERSION_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
    SOURCE_FEATURE_DATASET_FAMILY_V001,
    SOURCE_FEATURE_DATASET_VERSION_V001,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    pass


class LabelCheckStatus(StrEnum):
    """Tri-state validation result."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class LabelCheckResult:
    """One check entry in the validation result."""

    check_id: str
    status: LabelCheckStatus
    detail: str = ""


@dataclass(frozen=True)
class LabelValidationResult:
    """Aggregated validation result."""

    overall_status: LabelCheckStatus
    checks: tuple[LabelCheckResult, ...]


class LabelValidationError(RuntimeError):
    """Raised when validation cannot even be run (missing inputs)."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _check(check_id: str, ok: bool, detail: str = "") -> LabelCheckResult:
    return LabelCheckResult(
        check_id=check_id,
        status=LabelCheckStatus.PASS if ok else LabelCheckStatus.FAIL,
        detail=detail if not ok else "",
    )


def _hash_path(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def _read_sidecar_sha(path: Path) -> str:
    text = path.read_text(encoding="ascii").strip()
    if not text:
        return ""
    return text.split()[0]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def validate_label_dataset_v001(
    *,
    label_parquet_path: Path,
    label_manifest_path: Path,
    feature_parquet_path: Path,
    feature_manifest_path: Path,
    normalized_parquet_path: Path,
    source_feature_manifest_sha256: str,
    source_feature_parquet_sha256: str,
    source_feature_successor_state_sha256: str,
    source_phase_4bi_b_gate_report_sha256: str,
    source_normalized_parquet_sha256: str,
    expected_label_config_hash: str,
    extra_upstream_shas: Mapping[str, tuple[Path, str]] | None = None,
) -> LabelValidationResult:
    """Validate a label dataset + manifest pair.

    All input paths must exist. The validator hashes the on-disk label
    parquet, label parquet sidecar, label manifest, and label manifest
    sidecar; reads the label parquet via pyarrow; reads the source
    feature parquet to confirm per-row alignment; reads the source
    normalized parquet to confirm the future-reference policy on
    sampled rows; and runs schema, type, value, and lineage checks
    against the Phase 4bj-B contract.

    ``extra_upstream_shas`` is an optional mapping of
    ``{label: (path, expected_sha256)}`` that the validator hashes
    on disk and confirms unchanged. The Phase 4bj-C orchestrator passes
    the Phase 4bb-D / 4bf gate-report and raw-zip SHAs through this
    parameter so that pre/post immutability is checked alongside the
    in-line feature / normalized / successor-state references.
    """
    if not isinstance(label_parquet_path, Path):
        raise LabelValidationError("label_parquet_path must be Path")
    if not isinstance(label_manifest_path, Path):
        raise LabelValidationError("label_manifest_path must be Path")
    if not isinstance(feature_parquet_path, Path):
        raise LabelValidationError("feature_parquet_path must be Path")
    if not isinstance(feature_manifest_path, Path):
        raise LabelValidationError("feature_manifest_path must be Path")
    if not isinstance(normalized_parquet_path, Path):
        raise LabelValidationError("normalized_parquet_path must be Path")

    checks: list[LabelCheckResult] = []

    if not label_parquet_path.exists():
        raise LabelValidationError(
            f"label parquet does not exist: {label_parquet_path}"
        )
    if not label_manifest_path.exists():
        raise LabelValidationError(
            f"label manifest does not exist: {label_manifest_path}"
        )
    if not feature_parquet_path.exists():
        raise LabelValidationError(
            f"feature parquet does not exist: {feature_parquet_path}"
        )
    if not feature_manifest_path.exists():
        raise LabelValidationError(
            f"feature manifest does not exist: {feature_manifest_path}"
        )
    if not normalized_parquet_path.exists():
        raise LabelValidationError(
            f"normalized parquet does not exist: {normalized_parquet_path}"
        )

    # --- 1. Sidecar SHA matches label parquet bytes ---
    parquet_sidecar = label_parquet_path.with_suffix(
        label_parquet_path.suffix + ".sha256"
    )
    if not parquet_sidecar.exists():
        raise LabelValidationError(
            f"label parquet sidecar missing: {parquet_sidecar}"
        )
    parquet_sha, _parquet_size = _hash_path(label_parquet_path)
    checks.append(
        _check(
            "4bj-c.parquet.sidecar_matches",
            parquet_sha == _read_sidecar_sha(parquet_sidecar),
            f"recomputed={parquet_sha} sidecar={_read_sidecar_sha(parquet_sidecar)}",
        )
    )

    # --- 2. Sidecar SHA matches label manifest bytes ---
    manifest_sidecar = label_manifest_path.with_suffix(
        label_manifest_path.suffix + ".sha256"
    )
    if not manifest_sidecar.exists():
        raise LabelValidationError(
            f"label manifest sidecar missing: {manifest_sidecar}"
        )
    manifest_sha, _manifest_size = _hash_path(label_manifest_path)
    checks.append(
        _check(
            "4bj-c.manifest.sidecar_matches",
            manifest_sha == _read_sidecar_sha(manifest_sidecar),
            f"recomputed={manifest_sha} sidecar={_read_sidecar_sha(manifest_sidecar)}",
        )
    )

    # --- 3. Parse label manifest ---
    manifest_dict = json.loads(label_manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest_dict, dict):
        raise LabelValidationError("label manifest is not a JSON object")

    checks.append(
        _check(
            "4bj-c.manifest.dataset_family",
            manifest_dict.get("dataset_family") == LABEL_DATASET_FAMILY_V001,
            f"got={manifest_dict.get('dataset_family')!r}",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.dataset_version",
            manifest_dict.get("dataset_version") == LABEL_DATASET_VERSION_V001,
            f"got={manifest_dict.get('dataset_version')!r}",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.label_schema_version",
            manifest_dict.get("label_schema_version") == LABEL_SCHEMA_VERSION_V001,
            f"got={manifest_dict.get('label_schema_version')!r}",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.research_eligible_false",
            manifest_dict.get("research_eligible") is False,
            f"got={manifest_dict.get('research_eligible')!r}",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.eligibility_gate_status_pending",
            manifest_dict.get("eligibility_gate_status") == "pending",
            f"got={manifest_dict.get('eligibility_gate_status')!r}",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.label_list_matches",
            tuple(manifest_dict.get("label_list") or ()) == LABEL_NAMES_V001,
            "label_list != LABEL_NAMES_V001",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.support_column_list_matches",
            tuple(manifest_dict.get("support_column_list") or ())
            == LABEL_SUPPORT_COLUMN_NAMES_V001,
            "support_column_list != LABEL_SUPPORT_COLUMN_NAMES_V001",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.schema_column_list_matches",
            tuple(manifest_dict.get("schema_column_list") or ()) == LABEL_SCHEMA_V001,
            "schema_column_list != LABEL_SCHEMA_V001",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.horizon_list_matches",
            tuple(manifest_dict.get("horizon_list") or ()) == LABEL_HORIZONS_V001,
            "horizon_list != LABEL_HORIZONS_V001",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.horizon_ms_list_matches",
            tuple(manifest_dict.get("horizon_ms_list") or ()) == LABEL_HORIZON_MS_V001,
            "horizon_ms_list != LABEL_HORIZON_MS_V001",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.label_config_hash_matches",
            manifest_dict.get("label_config_hash") == expected_label_config_hash,
            f"got={manifest_dict.get('label_config_hash')}",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.source_feature_manifest_sha256_matches",
            manifest_dict.get("source_feature_manifest_sha256")
            == source_feature_manifest_sha256,
            "source_feature_manifest_sha256 mismatch",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.source_feature_parquet_sha256_matches",
            manifest_dict.get("source_feature_parquet_sha256")
            == source_feature_parquet_sha256,
            "source_feature_parquet_sha256 mismatch",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.source_feature_successor_state_sha256_matches",
            manifest_dict.get("source_feature_successor_state_sha256")
            == source_feature_successor_state_sha256,
            "source_feature_successor_state_sha256 mismatch",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.source_phase_4bi_b_gate_report_sha256_matches",
            manifest_dict.get("source_phase_4bi_b_gate_report_sha256")
            == source_phase_4bi_b_gate_report_sha256,
            "source_phase_4bi_b_gate_report_sha256 mismatch",
        )
    )
    checks.append(
        _check(
            "4bj-c.manifest.source_normalized_parquet_sha256_matches",
            manifest_dict.get("source_normalized_parquet_sha256")
            == source_normalized_parquet_sha256,
            "source_normalized_parquet_sha256 mismatch",
        )
    )
    governance = manifest_dict.get("governance_labels") or {}
    governance_required = (
        "phase_id",
        "labels",
        "targets",
        "ml",
        "strategy",
        "backtest",
        "acquisition",
        "paper_shadow_live",
        "deployment",
        "exchange_write",
    )
    governance_ok = isinstance(governance, dict) and all(
        k in governance for k in governance_required
    )
    checks.append(
        _check(
            "4bj-c.manifest.governance_labels_keys",
            governance_ok,
            f"keys={sorted(governance) if isinstance(governance, dict) else governance!r}",
        )
    )
    if isinstance(governance, dict):
        checks.append(
            _check(
                "4bj-c.manifest.governance_ml_forbidden",
                governance.get("ml") == "forbidden",
                f"got={governance.get('ml')!r}",
            )
        )
        checks.append(
            _check(
                "4bj-c.manifest.governance_strategy_forbidden",
                governance.get("strategy") == "forbidden",
                f"got={governance.get('strategy')!r}",
            )
        )
        checks.append(
            _check(
                "4bj-c.manifest.governance_backtest_forbidden",
                governance.get("backtest") == "forbidden",
                f"got={governance.get('backtest')!r}",
            )
        )
        checks.append(
            _check(
                "4bj-c.manifest.governance_acquisition_unauthorized",
                governance.get("acquisition") == "unauthorized",
                f"got={governance.get('acquisition')!r}",
            )
        )
    boundary = manifest_dict.get("boundary_confirmations") or {}
    boundary_required = (
        "no_ml",
        "no_strategy",
        "no_backtest",
        "no_acquisition",
        "no_network",
        "no_credentials",
        "no_feature_manifest_mutation",
        "no_feature_parquet_mutation",
        "no_feature_successor_state_mutation",
        "no_feature_gate_report_mutation",
        "no_label_gate_report",
        "no_label_successor_state",
        "no_successor_authorization",
    )
    boundary_ok = isinstance(boundary, dict) and all(
        boundary.get(k) is True for k in boundary_required
    )
    checks.append(
        _check(
            "4bj-c.manifest.boundary_confirmations_all_true",
            boundary_ok,
            f"boundary={boundary!r}",
        )
    )
    files_entry = manifest_dict.get("files") or []
    files_ok = (
        isinstance(files_entry, list)
        and len(files_entry) == 1
        and isinstance(files_entry[0], dict)
        and files_entry[0].get("sha256") == parquet_sha
        and files_entry[0].get("row_count") == manifest_dict.get("row_count")
    )
    checks.append(
        _check(
            "4bj-c.manifest.files_entry_matches_parquet",
            files_ok,
            f"files={files_entry!r}",
        )
    )

    # --- 4. Read label parquet ---
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment guard
        raise LabelValidationError("pyarrow is required to validate") from exc
    label_table = pq.read_table(label_parquet_path)
    label_names = tuple(label_table.column_names)
    checks.append(
        _check(
            "4bj-c.parquet.column_order_matches",
            label_names == LABEL_SCHEMA_V001,
            "label_table.column_names != LABEL_SCHEMA_V001",
        )
    )
    checks.append(
        _check(
            "4bj-c.parquet.column_count_39",
            len(label_names) == 39,
            f"len={len(label_names)}",
        )
    )
    forbidden_hits = [
        col
        for col in label_names
        for tok in FORBIDDEN_LABEL_COLUMN_SUBSTRINGS
        if tok in col.lower()
    ]
    checks.append(
        _check(
            "4bj-c.parquet.no_forbidden_substrings",
            not forbidden_hits,
            f"hits={forbidden_hits!r}",
        )
    )

    # --- 5. Row-count parity ---
    feat_table = pq.read_table(feature_parquet_path)
    feat_n = feat_table.num_rows
    label_n = label_table.num_rows
    declared_rc = manifest_dict.get("row_count")
    checks.append(
        _check(
            "4bj-c.row_count.parquet_eq_manifest",
            label_n == declared_rc,
            f"parquet={label_n} manifest={declared_rc}",
        )
    )
    checks.append(
        _check(
            "4bj-c.row_count.parquet_eq_feature",
            label_n == feat_n,
            f"label={label_n} feature={feat_n}",
        )
    )

    # --- 6. Per-row alignment with feature parquet ---
    feat_row_index = feat_table.column("row_index").to_pylist()
    label_row_index = label_table.column("row_index").to_pylist()
    checks.append(
        _check(
            "4bj-c.parity.row_index",
            feat_row_index == label_row_index,
            "row_index mismatch",
        )
    )
    feat_agg_id = feat_table.column("agg_trade_id").to_pylist()
    label_agg_id = label_table.column("agg_trade_id").to_pylist()
    checks.append(
        _check(
            "4bj-c.parity.agg_trade_id",
            feat_agg_id == label_agg_id,
            "agg_trade_id mismatch",
        )
    )
    feat_ts_ms = feat_table.column("feature_timestamp_ms").to_pylist()
    label_ts_ms = label_table.column("feature_timestamp_ms").to_pylist()
    checks.append(
        _check(
            "4bj-c.parity.feature_timestamp_ms",
            feat_ts_ms == label_ts_ms,
            "feature_timestamp_ms mismatch",
        )
    )
    label_src_ts_ms = label_table.column("source_transact_time_ms").to_pylist()
    checks.append(
        _check(
            "4bj-c.parity.feature_timestamp_eq_source",
            label_src_ts_ms == label_ts_ms,
            "label feature_timestamp_ms != source_transact_time_ms",
        )
    )

    # --- 7. Lineage constants ---
    constant_checks = (
        ("dataset_family", LABEL_DATASET_FAMILY_V001),
        ("dataset_version", LABEL_DATASET_VERSION_V001),
        ("label_schema_version", LABEL_SCHEMA_VERSION_V001),
        ("source_feature_dataset_family", SOURCE_FEATURE_DATASET_FAMILY_V001),
        ("source_feature_dataset_version", SOURCE_FEATURE_DATASET_VERSION_V001),
        ("source_feature_manifest_sha256", source_feature_manifest_sha256),
        ("source_feature_parquet_sha256", source_feature_parquet_sha256),
        (
            "source_feature_successor_state_sha256",
            source_feature_successor_state_sha256,
        ),
        (
            "source_phase_4bi_b_gate_report_sha256",
            source_phase_4bi_b_gate_report_sha256,
        ),
        ("source_normalized_parquet_sha256", source_normalized_parquet_sha256),
        ("label_config_hash", expected_label_config_hash),
    )
    for col, expected in constant_checks:
        arr = label_table.column(col).to_pylist()
        ok = all(v == expected for v in arr)
        unique_preview = sorted({v for v in arr})[:3]
        checks.append(
            _check(
                f"4bj-c.lineage.{col}_constant",
                ok,
                f"unique={unique_preview!r}" if not ok else "",
            )
        )

    symbol_col = label_table.column("symbol").to_pylist()
    if symbol_col:
        first_symbol = symbol_col[0]
        symbol_ok = isinstance(first_symbol, str) and all(
            v == first_symbol for v in symbol_col
        )
        checks.append(
            _check(
                "4bj-c.lineage.symbol_constant",
                symbol_ok,
                "symbol not constant",
            )
        )
    utc_date_col = label_table.column("utc_date").to_pylist()
    if utc_date_col:
        first_date = utc_date_col[0]
        date_ok = isinstance(first_date, str) and all(
            v == first_date for v in utc_date_col
        )
        checks.append(
            _check(
                "4bj-c.lineage.utc_date_constant",
                date_ok,
                "utc_date not constant",
            )
        )

    # --- 8. Forward log return / direction value checks ---
    direction_valid = {-1, 0, 1}
    for label in LABEL_HORIZONS_V001:
        ret_col = label_table.column(f"forward_log_return_{label}").to_pylist()
        dir_col = label_table.column(f"forward_direction_{label}").to_pylist()
        ret_ok = True
        dir_ok = True
        sign_ok = True
        for r, d in zip(ret_col, dir_col, strict=True):
            if r is None:
                if d is not None:
                    dir_ok = False
                    sign_ok = False
                    break
            else:
                if not isinstance(r, float) or not math.isfinite(r):
                    ret_ok = False
                    break
                if d not in direction_valid:
                    dir_ok = False
                    break
                expected_sign = 1 if r > 0 else (-1 if r < 0 else 0)
                if d != expected_sign:
                    sign_ok = False
                    break
        checks.append(
            _check(
                f"4bj-c.label.forward_log_return_{label}_finite_or_null",
                ret_ok,
                "NaN/inf or non-float detected",
            )
        )
        checks.append(
            _check(
                f"4bj-c.label.forward_direction_{label}_domain",
                dir_ok,
                "forward_direction value outside {null, -1, 0, 1}",
            )
        )
        checks.append(
            _check(
                f"4bj-c.label.forward_direction_{label}_matches_sign",
                sign_ok,
                "forward_direction does not match strict sign of log return",
            )
        )

    # --- 9. Support column checks ---
    norm_table = pq.read_table(normalized_parquet_path)
    norm_ts_ms = norm_table.column("transact_time_ms").to_pylist()
    final_ts = norm_ts_ms[-1] if norm_ts_ms else None
    n_norm = norm_table.num_rows
    for label, h_ms in zip(LABEL_HORIZONS_V001, LABEL_HORIZON_MS_V001, strict=True):
        ref_idx_col = label_table.column(f"reference_row_index_{label}").to_pylist()
        ref_ts_col = label_table.column(f"reference_timestamp_ms_{label}").to_pylist()
        cens_col = label_table.column(f"horizon_censored_flag_{label}").to_pylist()
        idx_ok = True
        ts_ok = True
        cens_ok = True
        for i in range(label_n):
            target_ts = label_ts_ms[i] + h_ms
            should_censor = final_ts is None or target_ts > final_ts
            if cens_col[i] is not should_censor:
                cens_ok = False
                break
            if should_censor:
                if ref_idx_col[i] is not None or ref_ts_col[i] is not None:
                    idx_ok = False
                    ts_ok = False
                    break
            else:
                if not (isinstance(ref_idx_col[i], int) and 0 <= ref_idx_col[i] < n_norm):
                    idx_ok = False
                    break
                if not (isinstance(ref_ts_col[i], int) and ref_ts_col[i] <= target_ts):
                    ts_ok = False
                    break
        checks.append(
            _check(
                f"4bj-c.support.horizon_censored_flag_{label}_matches_target",
                cens_ok,
                "horizon_censored_flag != (target > final_source_T)",
            )
        )
        checks.append(
            _check(
                f"4bj-c.support.reference_row_index_{label}_valid",
                idx_ok,
                "reference_row_index out of range or non-null when censored",
            )
        )
        checks.append(
            _check(
                f"4bj-c.support.reference_timestamp_ms_{label}_valid",
                ts_ok,
                "reference_timestamp_ms exceeds target or non-null when censored",
            )
        )

    # --- 10. label_any_censored_flag = OR of per-horizon flags ---
    any_cens_col = label_table.column("label_any_censored_flag").to_pylist()
    invalid_price_col = label_table.column("label_invalid_price_flag").to_pylist()
    horizon_flag_lists = [
        label_table.column(f"horizon_censored_flag_{label}").to_pylist()
        for label in LABEL_HORIZONS_V001
    ]
    or_ok = True
    for i in range(label_n):
        observed = any(horizon_flag_lists[h][i] for h in range(len(LABEL_HORIZONS_V001)))
        if any_cens_col[i] != observed:
            or_ok = False
            break
    checks.append(
        _check(
            "4bj-c.support.label_any_censored_flag_or_invariant",
            or_ok,
            "label_any_censored_flag != OR of horizon_censored_flag_*",
        )
    )
    invalid_ok = all(isinstance(v, bool) for v in invalid_price_col)
    checks.append(
        _check(
            "4bj-c.support.label_invalid_price_flag_strict_bool",
            invalid_ok,
            "label_invalid_price_flag has non-bool value",
        )
    )
    any_strict_bool = all(isinstance(v, bool) for v in any_cens_col)
    checks.append(
        _check(
            "4bj-c.support.label_any_censored_flag_strict_bool",
            any_strict_bool,
            "label_any_censored_flag has non-bool value",
        )
    )
    for label in LABEL_HORIZONS_V001:
        col_list = label_table.column(f"horizon_censored_flag_{label}").to_pylist()
        strict_ok = all(isinstance(v, bool) for v in col_list)
        checks.append(
            _check(
                f"4bj-c.support.horizon_censored_flag_{label}_strict_bool",
                strict_ok,
                "non-bool value",
            )
        )

    # --- 11. Censored counts match observed ---
    observed_censored = {
        label: sum(1 for v in label_table.column(f"horizon_censored_flag_{label}").to_pylist() if v)
        for label in LABEL_HORIZONS_V001
    }
    declared_censored = manifest_dict.get("censored_per_horizon") or {}
    checks.append(
        _check(
            "4bj-c.manifest.censored_per_horizon_matches",
            isinstance(declared_censored, dict)
            and {k: int(v) for k, v in declared_censored.items()} == observed_censored,
            f"observed={observed_censored} declared={declared_censored}",
        )
    )
    observed_invalid = sum(1 for v in invalid_price_col if v)
    checks.append(
        _check(
            "4bj-c.manifest.invalid_price_row_count_matches",
            manifest_dict.get("invalid_price_row_count") == observed_invalid,
            f"observed={observed_invalid} declared={manifest_dict.get('invalid_price_row_count')}",
        )
    )

    # --- 12. Lineage column null checks ---
    for col in LABEL_LINEAGE_COLUMNS_V001:
        null_count = label_table.column(col).null_count
        checks.append(
            _check(
                f"4bj-c.col_nonnull.{col}",
                null_count == 0,
                f"null_count={null_count}",
            )
        )

    # --- 13. Upstream immutability ---
    upstream_specs: list[tuple[str, Path, str]] = [
        (
            "source_feature_parquet",
            feature_parquet_path,
            source_feature_parquet_sha256,
        ),
        (
            "source_feature_manifest",
            feature_manifest_path,
            source_feature_manifest_sha256,
        ),
        (
            "source_normalized_parquet",
            normalized_parquet_path,
            source_normalized_parquet_sha256,
        ),
    ]
    if extra_upstream_shas:
        for label, (p, expected) in extra_upstream_shas.items():
            upstream_specs.append((label, p, expected))
    for label, path, expected in upstream_specs:
        recomputed, _ = _hash_path(path)
        checks.append(
            _check(
                f"4bj-c.immutability.{label}_unchanged",
                recomputed == expected,
                f"recomputed={recomputed} expected={expected}",
            )
        )

    # --- 14. Aggregate ---
    overall = (
        LabelCheckStatus.PASS
        if all(c.status == LabelCheckStatus.PASS for c in checks)
        else LabelCheckStatus.FAIL
    )
    return LabelValidationResult(overall_status=overall, checks=tuple(checks))


def iter_failures(result: LabelValidationResult) -> Iterable[LabelCheckResult]:
    """Yield only failing check entries; convenience for callers."""
    for r in result.checks:
        if r.status != LabelCheckStatus.PASS:
            yield r


def to_summary_dict(result: LabelValidationResult) -> dict[str, Any]:
    """Return a JSON-friendly summary; never written to disk by this module."""
    failures = list(iter_failures(result))
    return {
        "overall_status": str(result.overall_status),
        "checks_total": len(result.checks),
        "checks_pass": sum(
            1 for c in result.checks if c.status == LabelCheckStatus.PASS
        ),
        "checks_fail": sum(
            1 for c in result.checks if c.status == LabelCheckStatus.FAIL
        ),
        "checks_not_applicable": sum(
            1 for c in result.checks if c.status == LabelCheckStatus.NOT_APPLICABLE
        ),
        "failed_check_ids": [c.check_id for c in failures],
        "failed_check_details": [
            {"check_id": c.check_id, "detail": c.detail} for c in failures
        ],
    }


__all__ = [
    "LabelCheckResult",
    "LabelCheckStatus",
    "LabelValidationError",
    "LabelValidationResult",
    "iter_failures",
    "to_summary_dict",
    "validate_label_dataset_v001",
]
