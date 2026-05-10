"""Phase 4bh feature dataset validation.

Validates a previously written feature parquet + manifest pair against
the Phase 4bh-B locked schema and the project's no-rescue / no-leakage
contract:

- exact 61-column schema and order;
- exact row_count parity vs source normalized parquet and feature
  manifest;
- no forbidden substrings (per Phase 4bh-B §13);
- lineage hash columns constant and matching the requested values;
- ``feature_config_hash`` constant and matching the requested value;
- ``feature_timestamp_ms == source_transact_time_ms`` for every row;
- no nulls in non-null columns; no NaN / inf in float columns;
- Decimal-as-string columns parse via :class:`Decimal`;
- count columns non-negative int64;
- ratio columns null or in [0, 1];
- bool columns are strict bool;
- output Parquet SHA matches sidecar;
- feature manifest SHA matches sidecar;
- feature manifest declares ``research_eligible=False`` and
  ``eligibility_gate_status="pending"``.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute features, labels, or signals;
- does NOT mutate any artefact.
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

from .features_io import (
    hash_source_file,
    read_normalized_parquet,
)
from .features_manifest import (
    REQUIRED_BOUNDARY_CONFIRMATIONS,
    REQUIRED_FEATURE_GOVERNANCE_KEYS,
)
from .features_schema import (
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_V001,
    FEATURE_SCHEMA_VERSION,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS,
    LINEAGE_COLUMNS_V001,
    SOURCE_NORMALIZED_DATASET_FAMILY,
    SOURCE_NORMALIZED_DATASET_VERSION,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    import pyarrow as pa


_NULLABLE_FLOAT_PREFIXES = (
    "rolling_aggressive_flow_ratio_",
    "rolling_log_return_past_window_",
)
_NULLABLE_DECIMAL_PREFIXES = ("rolling_quantity_mean_",)
_NON_NULL_DECIMAL_PREFIXES = (
    "rolling_quantity_sum_",
    "rolling_aggressive_buy_quantity_",
    "rolling_aggressive_sell_quantity_",
    "rolling_aggressive_quantity_imbalance_",
)
_INT64_COUNT_PREFIXES = (
    "rolling_aggtrade_count_",
    "rolling_aggressive_buy_count_",
    "rolling_aggressive_sell_count_",
)


class FeatureCheckStatus(StrEnum):
    """Tri-state validation result."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class FeatureCheckResult:
    """One check entry in the validation result."""

    check_id: str
    status: FeatureCheckStatus
    detail: str = ""


@dataclass(frozen=True)
class FeatureValidationResult:
    """Aggregated validation result."""

    overall_status: FeatureCheckStatus
    checks: tuple[FeatureCheckResult, ...]


class FeatureValidationError(RuntimeError):
    """Raised when validation cannot even be run (e.g. missing inputs)."""


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def validate_feature_dataset(
    *,
    feature_parquet_path: Path,
    feature_manifest_path: Path,
    source_normalized_parquet_path: Path,
    source_normalized_manifest_sha256: str,
    source_normalized_parquet_sha256: str,
    source_successor_state_sha256: str,
    source_phase_4bf_gate_report_sha256: str,
    feature_config_hash: str,
) -> FeatureValidationResult:
    """Validate a feature dataset + manifest pair.

    All input paths must exist. The validator hashes the on-disk
    feature parquet, sidecar (``.sha256``), feature manifest, and
    feature manifest sidecar; reads the feature parquet via pyarrow;
    reads the source normalized parquet to confirm row-count parity;
    and runs schema, type, value, and lineage checks against the
    Phase 4bh-B contract.
    """
    if not isinstance(feature_parquet_path, Path):
        raise FeatureValidationError("feature_parquet_path must be Path")
    if not isinstance(feature_manifest_path, Path):
        raise FeatureValidationError("feature_manifest_path must be Path")
    if not isinstance(source_normalized_parquet_path, Path):
        raise FeatureValidationError("source_normalized_parquet_path must be Path")

    checks: list[FeatureCheckResult] = []

    # --- 1. Sidecar SHA matches feature parquet bytes ---
    if not feature_parquet_path.exists():
        raise FeatureValidationError(
            f"feature parquet does not exist: {feature_parquet_path}"
        )
    sidecar_path = feature_parquet_path.with_suffix(
        feature_parquet_path.suffix + ".sha256"
    )
    if not sidecar_path.exists():
        raise FeatureValidationError(
            f"feature parquet sidecar does not exist: {sidecar_path}"
        )
    parquet_summary = hash_source_file(feature_parquet_path, label="feature parquet")
    sidecar_text = sidecar_path.read_text(encoding="ascii").strip()
    sidecar_sha = sidecar_text.split()[0] if sidecar_text else ""
    checks.append(
        _check(
            "4bh.parquet.sidecar_matches",
            parquet_summary.sha256 == sidecar_sha,
            f"recomputed={parquet_summary.sha256} sidecar={sidecar_sha}",
        )
    )

    # --- 2. Feature manifest sidecar matches manifest bytes ---
    if not feature_manifest_path.exists():
        raise FeatureValidationError(
            f"feature manifest does not exist: {feature_manifest_path}"
        )
    manifest_sidecar_path = feature_manifest_path.with_suffix(
        feature_manifest_path.suffix + ".sha256"
    )
    if not manifest_sidecar_path.exists():
        raise FeatureValidationError(
            f"feature manifest sidecar does not exist: {manifest_sidecar_path}"
        )
    manifest_summary = hash_source_file(
        feature_manifest_path, label="feature manifest"
    )
    manifest_sidecar_text = manifest_sidecar_path.read_text(encoding="ascii").strip()
    manifest_sidecar_sha = (
        manifest_sidecar_text.split()[0] if manifest_sidecar_text else ""
    )
    checks.append(
        _check(
            "4bh.manifest.sidecar_matches",
            manifest_summary.sha256 == manifest_sidecar_sha,
            f"recomputed={manifest_summary.sha256} sidecar={manifest_sidecar_sha}",
        )
    )

    # --- 3. Parse feature manifest ---
    manifest_dict = json.loads(feature_manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest_dict, dict):
        raise FeatureValidationError("feature manifest is not a JSON object")

    checks.append(
        _check(
            "4bh.manifest.dataset_family",
            manifest_dict.get("dataset_family") == FEATURE_DATASET_FAMILY,
            f"got={manifest_dict.get('dataset_family')!r}",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.dataset_version",
            manifest_dict.get("dataset_version") == FEATURE_DATASET_VERSION,
            f"got={manifest_dict.get('dataset_version')!r}",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.feature_schema_version",
            manifest_dict.get("feature_schema_version") == FEATURE_SCHEMA_VERSION,
            f"got={manifest_dict.get('feature_schema_version')!r}",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.research_eligible_false",
            manifest_dict.get("research_eligible") is False,
            f"got={manifest_dict.get('research_eligible')!r}",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.eligibility_gate_status_pending",
            manifest_dict.get("eligibility_gate_status") == "pending",
            f"got={manifest_dict.get('eligibility_gate_status')!r}",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.feature_list_matches",
            tuple(manifest_dict.get("feature_list") or ()) == FEATURE_NAMES_V001,
            "feature_list != FEATURE_NAMES_V001",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.window_list_matches",
            tuple(manifest_dict.get("window_list") or ()) == FEATURE_WINDOW_LABELS_V001,
            "window_list != FEATURE_WINDOW_LABELS_V001",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.window_ms_list_matches",
            tuple(manifest_dict.get("window_ms_list") or ()) == FEATURE_WINDOWS_MS_V001,
            "window_ms_list != FEATURE_WINDOWS_MS_V001",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.feature_config_hash_matches",
            manifest_dict.get("feature_config_hash") == feature_config_hash,
            f"got={manifest_dict.get('feature_config_hash')}",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.source_normalized_manifest_sha256_matches",
            (
                manifest_dict.get("source_normalized_manifest_sha256")
                == source_normalized_manifest_sha256
            ),
            "source_normalized_manifest_sha256 mismatch",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.source_normalized_parquet_sha256_matches",
            (
                manifest_dict.get("source_normalized_parquet_sha256")
                == source_normalized_parquet_sha256
            ),
            "source_normalized_parquet_sha256 mismatch",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.source_successor_state_sha256_matches",
            (
                manifest_dict.get("source_successor_state_sha256")
                == source_successor_state_sha256
            ),
            "source_successor_state_sha256 mismatch",
        )
    )
    checks.append(
        _check(
            "4bh.manifest.source_phase_4bf_gate_report_sha256_matches",
            (
                manifest_dict.get("source_phase_4bf_gate_report_sha256")
                == source_phase_4bf_gate_report_sha256
            ),
            "source_phase_4bf_gate_report_sha256 mismatch",
        )
    )
    governance = manifest_dict.get("governance_labels") or {}
    governance_ok = isinstance(governance, dict) and all(
        k in governance for k in REQUIRED_FEATURE_GOVERNANCE_KEYS
    )
    checks.append(
        _check(
            "4bh.manifest.governance_labels_keys",
            governance_ok,
            f"keys={sorted(governance) if isinstance(governance, dict) else governance!r}",
        )
    )
    boundary = manifest_dict.get("boundary_confirmations") or {}
    boundary_ok = isinstance(boundary, dict) and all(
        boundary.get(k) is True for k in REQUIRED_BOUNDARY_CONFIRMATIONS
    )
    checks.append(
        _check(
            "4bh.manifest.boundary_confirmations_all_true",
            boundary_ok,
            f"boundary={boundary!r}",
        )
    )
    files_entry = manifest_dict.get("files") or []
    files_ok = (
        isinstance(files_entry, list)
        and len(files_entry) == 1
        and isinstance(files_entry[0], dict)
        and files_entry[0].get("sha256") == parquet_summary.sha256
        and files_entry[0].get("row_count") == manifest_dict.get("row_count")
    )
    checks.append(
        _check(
            "4bh.manifest.files_entry_matches_parquet",
            files_ok,
            f"files={files_entry!r}",
        )
    )

    # --- 4. Read feature parquet ---
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment guard
        raise FeatureValidationError("pyarrow is required to validate") from exc
    feature_table = pq.read_table(feature_parquet_path)
    feature_names = tuple(feature_table.column_names)
    checks.append(
        _check(
            "4bh.parquet.column_order_matches",
            feature_names == FEATURE_SCHEMA_V001,
            "feature_table.column_names != FEATURE_SCHEMA_V001",
        )
    )
    checks.append(
        _check(
            "4bh.parquet.column_count_61",
            len(feature_names) == 61,
            f"len={len(feature_names)}",
        )
    )
    forbidden_hits = [
        col
        for col in feature_names
        for tok in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS
        if tok in col.lower()
    ]
    checks.append(
        _check(
            "4bh.parquet.no_forbidden_substrings",
            not forbidden_hits,
            f"hits={forbidden_hits!r}",
        )
    )

    # --- 5. Row-count parity ---
    if not source_normalized_parquet_path.exists():
        raise FeatureValidationError(
            f"source normalized parquet does not exist: {source_normalized_parquet_path}"
        )
    src_table, _src_sha, _src_size = read_normalized_parquet(
        source_normalized_parquet_path
    )
    src_n = src_table.num_rows
    feat_n = feature_table.num_rows
    declared_rc = manifest_dict.get("row_count")
    checks.append(
        _check(
            "4bh.row_count.parquet_eq_manifest",
            feat_n == declared_rc,
            f"parquet={feat_n} manifest={declared_rc}",
        )
    )
    checks.append(
        _check(
            "4bh.row_count.parquet_eq_source",
            feat_n == src_n,
            f"feature={feat_n} source={src_n}",
        )
    )

    # --- 6. Lineage column constancy ---
    if feat_n > 0:
        for col, expected in (
            ("dataset_family", FEATURE_DATASET_FAMILY),
            ("dataset_version", FEATURE_DATASET_VERSION),
            ("source_dataset_family", SOURCE_NORMALIZED_DATASET_FAMILY),
            ("source_dataset_version", SOURCE_NORMALIZED_DATASET_VERSION),
            ("source_feature_schema_version", FEATURE_SCHEMA_VERSION),
            (
                "source_normalized_parquet_sha256",
                source_normalized_parquet_sha256,
            ),
            (
                "source_normalized_manifest_sha256",
                source_normalized_manifest_sha256,
            ),
            ("source_successor_state_sha256", source_successor_state_sha256),
            (
                "source_phase_4bf_gate_report_sha256",
                source_phase_4bf_gate_report_sha256,
            ),
            ("feature_config_hash", feature_config_hash),
        ):
            arr = feature_table.column(col).to_pylist()
            ok = all(v == expected for v in arr)
            checks.append(
                _check(
                    f"4bh.lineage.{col}_constant",
                    ok,
                    f"unique_values={sorted({v for v in arr})}" if not ok else "",
                )
            )

    # --- 7. agg_trade_id / row_index parity with source ---
    src_agg_id = src_table.column("agg_trade_id").to_pylist()
    feat_agg_id = feature_table.column("agg_trade_id").to_pylist()
    checks.append(
        _check(
            "4bh.parity.agg_trade_id",
            src_agg_id == feat_agg_id,
            "agg_trade_id mismatch",
        )
    )
    src_row_index = src_table.column("row_index").to_pylist()
    feat_row_index = feature_table.column("row_index").to_pylist()
    checks.append(
        _check(
            "4bh.parity.row_index",
            src_row_index == feat_row_index,
            "row_index mismatch",
        )
    )
    src_T = src_table.column("transact_time_ms").to_pylist()
    feat_T = feature_table.column("source_transact_time_ms").to_pylist()
    feat_ft = feature_table.column("feature_timestamp_ms").to_pylist()
    checks.append(
        _check(
            "4bh.parity.source_transact_time_ms",
            src_T == feat_T,
            "source_transact_time_ms mismatch",
        )
    )
    checks.append(
        _check(
            "4bh.parity.feature_timestamp_eq_source",
            feat_T == feat_ft,
            "feature_timestamp_ms != source_transact_time_ms",
        )
    )

    # --- 8. Per-column type / value checks ---
    for col in feature_names:
        col_arr = feature_table.column(col)
        if col in LINEAGE_COLUMNS_V001:
            checks.extend(_check_lineage_col_no_null(col, col_arr))
            continue
        if col.startswith(_INT64_COUNT_PREFIXES):
            checks.extend(_check_int64_count(col, col_arr))
        elif col.startswith(_NULLABLE_FLOAT_PREFIXES):
            checks.extend(_check_nullable_float(col, col_arr))
        elif col.startswith(_NULLABLE_DECIMAL_PREFIXES):
            checks.extend(_check_nullable_decimal_string(col, col_arr))
        elif col.startswith(_NON_NULL_DECIMAL_PREFIXES):
            checks.extend(_check_non_null_decimal_string(col, col_arr))
        elif col == "utc_hour":
            checks.extend(_check_int_in_range(col, col_arr, lo=0, hi=23))
        elif col == "utc_minute":
            checks.extend(_check_int_in_range(col, col_arr, lo=0, hi=59))
        elif col == "milliseconds_since_day_start":
            checks.extend(_check_int_in_range(col, col_arr, lo=0, hi=86_399_999))
        elif col == "invalid_window_flag" or col == "rolling_missing_window_flag":
            checks.extend(_check_strict_bool(col, col_arr))

    # --- 9. Aggressive flow ratio bounded [0, 1] ---
    for label in FEATURE_WINDOW_LABELS_V001:
        col = f"rolling_aggressive_flow_ratio_{label}"
        ratios = feature_table.column(col).to_pylist()
        ok = True
        for v in ratios:
            if v is None:
                continue
            if not (isinstance(v, float) and 0.0 <= v <= 1.0 and math.isfinite(v)):
                ok = False
                break
        checks.append(
            _check(
                f"4bh.range.{col}",
                ok,
                "ratio out of [0, 1] or non-finite",
            )
        )

    overall = (
        FeatureCheckStatus.PASS
        if all(c.status == FeatureCheckStatus.PASS for c in checks)
        else FeatureCheckStatus.FAIL
    )
    return FeatureValidationResult(overall_status=overall, checks=tuple(checks))


# ---------------------------------------------------------------------------
# Per-column helpers
# ---------------------------------------------------------------------------


def _check(check_id: str, ok: bool, detail: str) -> FeatureCheckResult:
    return FeatureCheckResult(
        check_id=check_id,
        status=FeatureCheckStatus.PASS if ok else FeatureCheckStatus.FAIL,
        detail=detail if not ok else "",
    )


def _check_lineage_col_no_null(col: str, arr: pa.ChunkedArray) -> Iterable[
    FeatureCheckResult
]:
    null_count = arr.null_count
    yield _check(
        f"4bh.col_nonnull.{col}",
        null_count == 0,
        f"null_count={null_count}",
    )


def _check_int64_count(col: str, arr: pa.ChunkedArray) -> Iterable[FeatureCheckResult]:
    null_count = arr.null_count
    yield _check(
        f"4bh.col_nonnull.{col}",
        null_count == 0,
        f"null_count={null_count}",
    )
    values = arr.to_pylist()
    ok = all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in values)
    yield _check(
        f"4bh.col_nonneg_int64.{col}",
        ok,
        "negative or non-int value detected",
    )


def _check_nullable_float(
    col: str, arr: pa.ChunkedArray
) -> Iterable[FeatureCheckResult]:
    values = arr.to_pylist()
    ok = True
    for v in values:
        if v is None:
            continue
        if not isinstance(v, float):
            ok = False
            break
        if not math.isfinite(v):
            ok = False
            break
    yield _check(
        f"4bh.col_float_finite_or_null.{col}",
        ok,
        "NaN/inf or non-float detected",
    )


def _check_nullable_decimal_string(
    col: str, arr: pa.ChunkedArray
) -> Iterable[FeatureCheckResult]:
    values = arr.to_pylist()
    ok = True
    for v in values:
        if v is None:
            continue
        if not isinstance(v, str):
            ok = False
            break
        try:
            Decimal(v)
        except InvalidOperation:
            ok = False
            break
    yield _check(
        f"4bh.col_decimal_str_or_null.{col}",
        ok,
        "non-Decimal-parsable value detected",
    )


def _check_non_null_decimal_string(
    col: str, arr: pa.ChunkedArray
) -> Iterable[FeatureCheckResult]:
    null_count = arr.null_count
    yield _check(
        f"4bh.col_nonnull.{col}",
        null_count == 0,
        f"null_count={null_count}",
    )
    values = arr.to_pylist()
    ok = True
    for v in values:
        if not isinstance(v, str):
            ok = False
            break
        try:
            Decimal(v)
        except InvalidOperation:
            ok = False
            break
    yield _check(
        f"4bh.col_decimal_str.{col}",
        ok,
        "non-Decimal-parsable string detected",
    )


def _check_int_in_range(
    col: str, arr: pa.ChunkedArray, *, lo: int, hi: int
) -> Iterable[FeatureCheckResult]:
    null_count = arr.null_count
    yield _check(
        f"4bh.col_nonnull.{col}",
        null_count == 0,
        f"null_count={null_count}",
    )
    values = arr.to_pylist()
    ok = all(
        isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi for v in values
    )
    yield _check(
        f"4bh.col_int_in_range.{col}",
        ok,
        f"value out of [{lo}, {hi}]",
    )


def _check_strict_bool(col: str, arr: pa.ChunkedArray) -> Iterable[FeatureCheckResult]:
    null_count = arr.null_count
    yield _check(
        f"4bh.col_nonnull.{col}",
        null_count == 0,
        f"null_count={null_count}",
    )
    values = arr.to_pylist()
    ok = all(isinstance(v, bool) for v in values)
    yield _check(
        f"4bh.col_strict_bool.{col}",
        ok,
        "non-bool value detected",
    )


__all__ = [
    "FeatureCheckResult",
    "FeatureCheckStatus",
    "FeatureValidationError",
    "FeatureValidationResult",
    "validate_feature_dataset",
]
