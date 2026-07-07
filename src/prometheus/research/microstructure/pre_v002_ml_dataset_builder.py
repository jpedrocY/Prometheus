"""Phase 4bn-AF — pre-v002 ML dataset builder skeleton (pure, offline).

Pure, in-memory **validators and skeleton planners** for the conservative
pre-v002-only ML dataset path. This module is a *skeleton*: it encodes the
Phase 4bn-AC source contract, the Phase 4bn-AD no-data-I/O readiness controls,
and the Phase 4bn-AE amendment-001 evaluation obligations as executable
invariants, and exercises them **only against synthetic in-memory objects**.

It is **not** a data-reading builder. It performs no I/O: it reads no manifest,
Parquet, sidecar, or gate report; it writes nothing; it resolves no filesystem
path; it creates no directory and never creates the future output namespace. It
imports only the standard library, the sibling inert contract-constant module,
and the Phase 4bn-AA inert split-policy artefact.

Every public function is deterministic and side-effect-free. Contract violations
and forbidden scope fail closed with :class:`PreV002MlDatasetError`.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from . import pre_v002_ml_dataset_contract as contract
from . import pre_v002_split_policy as split_policy


class PreV002MlDatasetError(RuntimeError):
    """Raised when a pre-v002 ML dataset skeleton invariant fails closed."""


# ---------------------------------------------------------------------------
# 1. Source-scope validation
# ---------------------------------------------------------------------------


def validate_source_scope(manifest_like: Mapping[str, object]) -> None:
    """Fail closed unless *manifest_like* describes the exact pre-v002 scope.

    Critical keys (must be present and correct): ``symbol``, ``market``,
    ``source_family``, ``start_date``, ``end_date``. Optional keys are checked
    only when present: partition counts (must equal 275), ``row_count`` (must
    equal :data:`contract.EXPECTED_ROW_COUNT`), and the danger flags
    ``contains_v002_terminal`` / ``contains_sealed_test`` / ``full_envelope`` /
    ``private_source`` / ``authenticated_source`` / ``external_source`` (must be
    absent or falsey).
    """
    required = ("symbol", "market", "source_family", "start_date", "end_date")
    for key in required:
        if key not in manifest_like:
            raise PreV002MlDatasetError(f"source scope missing required key {key!r}")

    if manifest_like["symbol"] != contract.SYMBOL:
        raise PreV002MlDatasetError(
            f"symbol must be {contract.SYMBOL!r}, got {manifest_like['symbol']!r}"
        )
    if manifest_like["market"] != contract.MARKET:
        raise PreV002MlDatasetError(
            f"market must be {contract.MARKET!r}, got {manifest_like['market']!r}"
        )
    if manifest_like["source_family"] != contract.SOURCE_FAMILY:
        raise PreV002MlDatasetError(
            f"source_family must be {contract.SOURCE_FAMILY!r}, "
            f"got {manifest_like['source_family']!r}"
        )
    if manifest_like["start_date"] != contract.START_DATE:
        raise PreV002MlDatasetError(
            f"start_date must be {contract.START_DATE!r}, "
            f"got {manifest_like['start_date']!r}"
        )
    if manifest_like["end_date"] != contract.END_DATE:
        raise PreV002MlDatasetError(
            f"end_date must be {contract.END_DATE!r}, "
            f"got {manifest_like['end_date']!r}"
        )

    for count_key in (
        "feature_partition_count",
        "label_partition_count",
        "normalized_partition_count",
    ):
        if count_key in manifest_like and manifest_like[count_key] != 275:
            raise PreV002MlDatasetError(
                f"{count_key} must be 275, got {manifest_like[count_key]!r}"
            )

    if "row_count" in manifest_like and (
        manifest_like["row_count"] != contract.EXPECTED_ROW_COUNT
    ):
        raise PreV002MlDatasetError(
            f"row_count must be {contract.EXPECTED_ROW_COUNT}, "
            f"got {manifest_like['row_count']!r}"
        )

    for danger_flag in (
        "contains_v002_terminal",
        "contains_sealed_test",
        "full_envelope",
        "private_source",
        "authenticated_source",
        "external_source",
    ):
        if manifest_like.get(danger_flag):
            raise PreV002MlDatasetError(
                f"forbidden source condition {danger_flag!r} is set true"
            )


# ---------------------------------------------------------------------------
# 2. Manifest / hash / gate binding
# ---------------------------------------------------------------------------


def _check_hash(actual: object, expected: str, *, label: str) -> None:
    if actual != expected:
        raise PreV002MlDatasetError(
            f"{label} mismatch: expected {expected!r}, got {actual!r}"
        )


def _reject_v002_hash(actual: object, prefix: str, full: str, *, label: str) -> None:
    if isinstance(actual, str) and (actual == full or actual.startswith(prefix)):
        raise PreV002MlDatasetError(
            f"{label} is the rejected v002-terminal identity ({actual!r})"
        )


def validate_manifest_hashes(
    normalized_like: Mapping[str, object],
    feature_like: Mapping[str, object],
    label_like: Mapping[str, object],
) -> None:
    """Fail closed unless the three manifests match the recorded pre-v002 hashes.

    Verifies the normalized / feature / label manifest SHA256s, the feature and
    label config hashes, and (when present) the per-layer gate-report SHA256s and
    partition counts. Rejects the v002-terminal ``819cfa7a…`` / ``352bad41…``
    config hashes.
    """
    if "manifest_sha256" not in normalized_like:
        raise PreV002MlDatasetError("normalized manifest missing manifest_sha256")
    _check_hash(
        normalized_like["manifest_sha256"],
        contract.EXPECTED_NORMALIZED_MANIFEST_SHA256,
        label="normalized manifest_sha256",
    )

    if "manifest_sha256" not in feature_like:
        raise PreV002MlDatasetError("feature manifest missing manifest_sha256")
    _check_hash(
        feature_like["manifest_sha256"],
        contract.EXPECTED_FEATURE_MANIFEST_SHA256,
        label="feature manifest_sha256",
    )
    if "feature_config_hash" not in feature_like:
        raise PreV002MlDatasetError("feature manifest missing feature_config_hash")
    _reject_v002_hash(
        feature_like["feature_config_hash"],
        contract.REJECTED_V002_FEATURE_CONFIG_HASH_PREFIX,
        contract.REJECTED_V002_FEATURE_CONFIG_HASH,
        label="feature_config_hash",
    )
    _check_hash(
        feature_like["feature_config_hash"],
        contract.EXPECTED_FEATURE_CONFIG_HASH,
        label="feature_config_hash",
    )

    if "manifest_sha256" not in label_like:
        raise PreV002MlDatasetError("label manifest missing manifest_sha256")
    _check_hash(
        label_like["manifest_sha256"],
        contract.EXPECTED_LABEL_MANIFEST_SHA256,
        label="label manifest_sha256",
    )
    if "label_config_hash" not in label_like:
        raise PreV002MlDatasetError("label manifest missing label_config_hash")
    _reject_v002_hash(
        label_like["label_config_hash"],
        contract.REJECTED_V002_LABEL_CONFIG_HASH_PREFIX,
        contract.REJECTED_V002_LABEL_CONFIG_HASH,
        label="label_config_hash",
    )
    _check_hash(
        label_like["label_config_hash"],
        contract.EXPECTED_LABEL_CONFIG_HASH,
        label="label_config_hash",
    )

    # Optional gate-report bindings (verified only when provided).
    for layer, mapping, expected in (
        (
            "normalized",
            normalized_like,
            contract.EXPECTED_NORMALIZED_GATE_REPORT_SHA256,
        ),
        ("feature", feature_like, contract.EXPECTED_FEATURE_GATE_REPORT_SHA256),
        ("label", label_like, contract.EXPECTED_LABEL_GATE_REPORT_SHA256),
    ):
        if "gate_report_sha256" in mapping:
            _check_hash(
                mapping["gate_report_sha256"],
                expected,
                label=f"{layer} gate_report_sha256",
            )

    # Optional partition-count bindings.
    for layer, mapping in (
        ("normalized", normalized_like),
        ("feature", feature_like),
        ("label", label_like),
    ):
        if "partition_count" in mapping and mapping["partition_count"] != 275:
            raise PreV002MlDatasetError(
                f"{layer} partition_count must be 275, "
                f"got {mapping['partition_count']!r}"
            )


# ---------------------------------------------------------------------------
# 3 + 4. Feature allowlist and forbidden-column scan
# ---------------------------------------------------------------------------


def find_forbidden_columns(columns: Sequence[str]) -> tuple[str, ...]:
    """Return the subset of *columns* forbidden from the model matrix (no raise).

    A column is forbidden if it is a lineage column, a label/support column,
    contains any :data:`contract.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS` token, or is a
    raw-price column.
    """
    forbidden: list[str] = []
    excluded = set(contract.EXCLUDED_LINEAGE_COLUMNS)
    label_cols = set(contract.LABEL_COLUMNS) | set(contract.LABEL_SUPPORT_COLUMNS)
    raw_price = set(contract.FORBIDDEN_RAW_PRICE_COLUMNS)
    for col in columns:
        lower = col.lower()
        if col in excluded or col in label_cols or col in raw_price:
            forbidden.append(col)
            continue
        if any(sub in lower for sub in contract.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS):
            forbidden.append(col)
    return tuple(forbidden)


def scan_forbidden_columns(columns: Sequence[str]) -> tuple[str, ...]:
    """Return forbidden columns found in *columns* (empty tuple if none).

    Non-raising inspection helper; pair with :func:`assert_no_forbidden_columns`
    for the fail-closed validator.
    """
    return find_forbidden_columns(columns)


def assert_no_forbidden_columns(columns: Sequence[str]) -> None:
    """Fail closed if any forbidden column appears in *columns*."""
    found = find_forbidden_columns(columns)
    if found:
        raise PreV002MlDatasetError(
            f"forbidden model-matrix columns present: {found!r}"
        )


def validate_feature_allowlist(columns: Sequence[str]) -> tuple[str, ...]:
    """Require exactly the 45 allowed feature columns; return canonical order.

    Fails closed on any missing, extra, duplicate, or forbidden (raw-price /
    label / split / censor / forward / lineage) column. Input order is
    irrelevant; the returned tuple is the canonical contract order.
    """
    seen = list(columns)
    if len(seen) != len(set(seen)):
        raise PreV002MlDatasetError("duplicate feature columns present")
    assert_no_forbidden_columns(seen)
    allowed = set(contract.ALLOWED_FEATURE_COLUMNS)
    given = set(seen)
    missing = allowed - given
    extra = given - allowed
    if missing:
        raise PreV002MlDatasetError(f"missing allowed feature columns: {sorted(missing)!r}")
    if extra:
        raise PreV002MlDatasetError(f"unexpected feature columns: {sorted(extra)!r}")
    return contract.ALLOWED_FEATURE_COLUMNS


# ---------------------------------------------------------------------------
# 5. Target filtering
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FilterResult:
    """Result of target filtering over synthetic rows (never imputes)."""

    valid_rows: tuple[Mapping[str, object], ...]
    dropped_by_reason: dict[str, int]

    @property
    def total_dropped(self) -> int:
        return sum(self.dropped_by_reason.values())


# Drop-reason precedence (a row is attributed to the first matching reason).
DROP_REASONS: tuple[str, ...] = (
    "invalid_price",
    "censored",
    "null_direction",
    "null_log_return",
)


def filter_targets(
    rows: Sequence[Mapping[str, object]],
    *,
    direction_field: str = contract.PRIMARY_TARGET,
    log_return_field: str = contract.PRIMARY_LOG_RETURN,
    censored_field: str = contract.PRIMARY_CENSORED_FLAG,
    invalid_price_field: str = contract.LABEL_INVALID_PRICE_FLAG,
) -> FilterResult:
    """Drop null / censored / invalid target rows; never impute.

    A row is dropped (and attributed once, by :data:`DROP_REASONS` precedence)
    when the invalid-price flag is true, the horizon censored flag is true, the
    direction target is null, or the log-return is null. Valid rows are preserved
    in input order. No target value is ever imputed or modified.
    """
    valid: list[Mapping[str, object]] = []
    dropped: dict[str, int] = {reason: 0 for reason in DROP_REASONS}
    for row in rows:
        if row.get(invalid_price_field) is True:
            dropped["invalid_price"] += 1
            continue
        if row.get(censored_field) is True:
            dropped["censored"] += 1
            continue
        if row.get(direction_field) is None:
            dropped["null_direction"] += 1
            continue
        if row.get(log_return_field) is None:
            dropped["null_log_return"] += 1
            continue
        valid.append(row)
    return FilterResult(valid_rows=tuple(valid), dropped_by_reason=dropped)


# ---------------------------------------------------------------------------
# 6. Strict alignment
# ---------------------------------------------------------------------------


def assert_strict_alignment(
    feature_keys: Sequence[Mapping[str, object]],
    label_keys: Sequence[Mapping[str, object]],
) -> None:
    """Fail closed unless feature and label rows are strictly positionally aligned.

    Compares, per row and in order, the mandatory alignment keys
    (:data:`contract.ALIGNMENT_KEYS`) plus any optional keys
    (:data:`contract.OPTIONAL_ALIGNMENT_KEYS`) present in both. No join repair,
    no reordering, no fill, no tolerance merge, no heuristic dedup.
    """
    if len(feature_keys) != len(label_keys):
        raise PreV002MlDatasetError(
            f"row count mismatch: features {len(feature_keys)} != "
            f"labels {len(label_keys)}"
        )
    for i, (frow, lrow) in enumerate(zip(feature_keys, label_keys, strict=True)):
        for key in contract.ALIGNMENT_KEYS:
            if key not in frow or key not in lrow:
                raise PreV002MlDatasetError(
                    f"row {i}: missing alignment key {key!r}"
                )
            if frow[key] != lrow[key]:
                raise PreV002MlDatasetError(
                    f"row {i}: alignment key {key!r} mismatch "
                    f"({frow[key]!r} != {lrow[key]!r})"
                )
        for key in contract.OPTIONAL_ALIGNMENT_KEYS:
            if key in frow and key in lrow and frow[key] != lrow[key]:
                raise PreV002MlDatasetError(
                    f"row {i}: optional alignment key {key!r} mismatch "
                    f"({frow[key]!r} != {lrow[key]!r})"
                )


# ---------------------------------------------------------------------------
# 7 + 8. Split assignment
# ---------------------------------------------------------------------------


def assign_split(source_transact_time_ms: int) -> str:
    """Return the split label for a row via the Phase 4bn-AA split artefact.

    Returns one of ``train`` / ``validation`` / ``holdout`` / ``embargo``
    (the :mod:`pre_v002_split_policy` label values). Hard-raises
    :class:`PreV002MlDatasetError` for any out-of-segment date, including every
    v002-terminal and sealed-test date.
    """
    try:
        return split_policy.split_for_timestamp_ms(source_transact_time_ms)
    except split_policy.PreV002SplitPolicyError as exc:
        raise PreV002MlDatasetError(str(exc)) from exc


def should_drop_for_split(split_label: str) -> bool:
    """Return True iff rows of *split_label* are dropped (embargo only).

    False for train / validation / holdout. Fails closed on any unknown label.
    """
    if split_label == split_policy.EMBARGO:
        return True
    if split_label in split_policy.MODEL_ELIGIBLE_SPLITS:
        return False
    raise PreV002MlDatasetError(f"unknown split label {split_label!r}")


# ---------------------------------------------------------------------------
# 9. Boundary-crossing validation
# ---------------------------------------------------------------------------


def validate_no_boundary_crossing(
    source_transact_time_ms: int, horizon_ms: int
) -> None:
    """Fail closed if an earlier-split row's forward target crosses its boundary.

    Uses the Phase 4bn-AA :func:`is_earlier_split_boundary_crossing` helper for
    the active horizon. Holdout never crosses (it is the latest pre-v002 split);
    embargo rows are dropped, so a boundary-crossing check on them fails closed.
    """
    try:
        split_policy.validate_horizon_ms(horizon_ms)
        split = split_policy.split_for_timestamp_ms(source_transact_time_ms)
        if split == split_policy.EMBARGO:
            raise PreV002MlDatasetError(
                "embargo rows are dropped; boundary crossing is undefined"
            )
        if split_policy.is_earlier_split_boundary_crossing(
            source_transact_time_ms, horizon_ms, split
        ):
            raise PreV002MlDatasetError(
                f"row at {source_transact_time_ms} (split {split!r}) crosses its "
                f"earlier-split boundary at horizon {horizon_ms} ms"
            )
    except split_policy.PreV002SplitPolicyError as exc:
        raise PreV002MlDatasetError(str(exc)) from exc


# ---------------------------------------------------------------------------
# 10. Train-only transform planning
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TransformPlan:
    """Inert train-only transform plan (no data is fit)."""

    fit_split: str
    standardization_rule: str
    standardization_epsilon: float
    imputation_rule: str
    imputation_fill_value: float
    standardize_boolean_flags: bool
    applied_splits: tuple[str, ...]


def plan_train_only_transform(
    fit_split: str = contract.TRAIN_ONLY_FIT_SPLIT,
) -> TransformPlan:
    """Return an inert train-only transform plan; fail closed on non-train fit.

    The standardization statistics are conceptually fit on the ``train`` split
    only; fixed-zero imputation is fit-free (locked v002 design); boolean quality
    flags pass through unstandardized. Any *fit_split* other than ``train`` (in
    particular ``validation`` / ``holdout`` / the sealed ``test``) fails closed.
    """
    if fit_split != split_policy.TRAIN:
        raise PreV002MlDatasetError(
            f"transforms may be fit on the train split only, not {fit_split!r}"
        )
    return TransformPlan(
        fit_split=split_policy.TRAIN,
        standardization_rule=contract.STANDARDIZATION_RULE,
        standardization_epsilon=contract.STANDARDIZATION_EPSILON,
        imputation_rule=contract.IMPUTATION_RULE,
        imputation_fill_value=contract.IMPUTATION_FILL_VALUE,
        standardize_boolean_flags=contract.STANDARDIZE_BOOLEAN_FLAGS,
        applied_splits=(split_policy.VALIDATION, split_policy.HOLDOUT),
    )


# ---------------------------------------------------------------------------
# 11. Evaluation-schema validation (Phase 4bn-AE amendment obligations)
# ---------------------------------------------------------------------------


def validate_evaluation_schema(schema_like: Mapping[str, object]) -> None:
    """Fail closed unless *schema_like* satisfies the Phase 4bn-AE obligations.

    Requires: all mandatory metrics present; aggregate/month/date granularity;
    row-level-metrics-descriptive-only flag true; a dependence caveat; decimation
    stride unset (None); the pre-registered success constants; a calibration
    schema; descriptive cost fields; and a no-strategy boundary.
    """
    metrics = schema_like.get("metrics")
    if not isinstance(metrics, (list, tuple, set)):
        raise PreV002MlDatasetError("evaluation schema missing 'metrics' collection")
    missing_metrics = set(contract.MANDATORY_METRICS) - set(metrics)
    if missing_metrics:
        raise PreV002MlDatasetError(
            f"evaluation schema missing mandatory metrics: {sorted(missing_metrics)!r}"
        )

    granularities = schema_like.get("granularities")
    if not isinstance(granularities, (list, tuple, set)):
        raise PreV002MlDatasetError("evaluation schema missing 'granularities'")
    missing_gran = set(contract.METRIC_GRANULARITIES) - set(granularities)
    if missing_gran:
        raise PreV002MlDatasetError(
            f"evaluation schema missing granularities: {sorted(missing_gran)!r}"
        )

    if schema_like.get("row_level_metrics_descriptive_only") is not True:
        raise PreV002MlDatasetError(
            "row_level_metrics_descriptive_only must be True"
        )
    if not schema_like.get("dependence_caveat"):
        raise PreV002MlDatasetError("evaluation schema missing dependence_caveat")
    if schema_like.get("decimation_stride") is not None:
        raise PreV002MlDatasetError(
            "decimation_stride must be None (reserved, not adopted)"
        )

    success = schema_like.get("success_thresholds")
    if not isinstance(success, Mapping):
        raise PreV002MlDatasetError("evaluation schema missing success_thresholds")
    _require_value(success, "accuracy_uplift_pp", contract.SUCCESS_ACCURACY_UPLIFT_PP)
    _require_value(
        success,
        "balanced_accuracy_uplift_pp",
        contract.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP,
    )
    _require_value(success, "macro_f1_uplift", contract.SUCCESS_MACRO_F1_UPLIFT)

    if not schema_like.get("calibration_schema"):
        raise PreV002MlDatasetError("evaluation schema missing calibration_schema")
    if not schema_like.get("cost_descriptive_fields"):
        raise PreV002MlDatasetError(
            "evaluation schema missing cost_descriptive_fields"
        )
    if schema_like.get("no_strategy_boundary") is not True:
        raise PreV002MlDatasetError("evaluation schema missing no_strategy_boundary")


def _require_value(mapping: Mapping[str, object], key: str, expected: object) -> None:
    if key not in mapping:
        raise PreV002MlDatasetError(f"success_thresholds missing {key!r}")
    if mapping[key] != expected:
        raise PreV002MlDatasetError(
            f"success_thresholds[{key!r}] must be {expected!r}, got {mapping[key]!r}"
        )


# ---------------------------------------------------------------------------
# 12. Skeleton plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SkeletonPlan:
    """Inert summary of the pre-v002 dataset-builder skeleton."""

    contract_name: str
    amendment_id: str
    symbol: str
    market: str
    source_family: str
    start_date: str
    end_date: str
    split_policy_name: str
    primary_target: str
    primary_horizon_ms: int
    feature_count: int
    output_namespace_path: str
    non_authorization_flags: tuple[tuple[str, bool], ...]
    no_data_io: bool = True
    creates_output_namespace: bool = False


def build_skeleton_plan() -> SkeletonPlan:
    """Return an inert :class:`SkeletonPlan` from contract constants only."""
    return SkeletonPlan(
        contract_name=contract.CONTRACT_NAME,
        amendment_id=contract.CONTRACT_AMENDMENT_ID,
        symbol=contract.SYMBOL,
        market=contract.MARKET,
        source_family=contract.SOURCE_FAMILY,
        start_date=contract.START_DATE,
        end_date=contract.END_DATE,
        split_policy_name=split_policy.SPLIT_POLICY_NAME,
        primary_target=contract.PRIMARY_TARGET,
        primary_horizon_ms=contract.PRIMARY_HORIZON_MS,
        feature_count=len(contract.ALLOWED_FEATURE_COLUMNS),
        output_namespace_path=contract.OUTPUT_NAMESPACE_PATH,
        non_authorization_flags=tuple(contract.NON_AUTHORIZATION_FLAGS.items()),
        no_data_io=True,
        creates_output_namespace=False,
    )


__all__ = [
    "DROP_REASONS",
    "FilterResult",
    "PreV002MlDatasetError",
    "SkeletonPlan",
    "TransformPlan",
    "assert_no_forbidden_columns",
    "assert_strict_alignment",
    "assign_split",
    "build_skeleton_plan",
    "filter_targets",
    "find_forbidden_columns",
    "plan_train_only_transform",
    "scan_forbidden_columns",
    "should_drop_for_split",
    "validate_evaluation_schema",
    "validate_feature_allowlist",
    "validate_manifest_hashes",
    "validate_no_boundary_crossing",
    "validate_source_scope",
]
