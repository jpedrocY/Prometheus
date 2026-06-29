"""Phase 4bn-AA — pre-v002 chronological split-policy artefact (pure, offline).

This module operationalises the Phase 4bn-Y **Candidate A** chronological split /
holdout policy for the locally-gated **pre-v002 BTCUSDT aggTrades label segment**
(``microstructure_labels_aggtrades_v001 @ v002``; pre-v002 backward segment;
275 contiguous UTC dates 2024-03-01 .. 2024-11-30) as pure date / window
arithmetic. It is the code-level counterpart of the recorded v002 split policy in
:mod:`prometheus.research.microstructure.diagnostics_split_policy_v002`, but
segment-scoped to the pre-v002 dates and strictly more conservative at the
boundaries (a full-UTC-date purge ≫ the 60-second label horizon).

Policy name:
``CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO``.

Segment partition (Phase 4bn-Y §11, exact):

- **Train**      : 2024-03-01 .. 2024-09-30 inclusive (214 UTC dates).
- *Embargo*      : 2024-10-01 (1 date; dropped from all splits).
- **Validation** : 2024-10-02 .. 2024-11-15 inclusive (45 UTC dates).
- *Embargo*      : 2024-11-16 (1 date; dropped from all splits).
- **Holdout**    : 2024-11-17 .. 2024-11-30 inclusive (14 UTC dates) — an
  internal dry-run only; **not** the sealed test.
- Total          : 214 + 1 + 45 + 1 + 14 = **275** = full gated pre-v002 segment.

Design invariants:

- Rows are assigned by ``source_transact_time_ms`` UTC date. Chronological-only;
  never shuffled, randomly split, k-fold-over-time, bootstrapped, or post-hoc
  temporally resampled. There is no RNG anywhere in this module.
- The primary operational embargo drops one full UTC date at each internal
  boundary (2024-10-01 and 2024-11-16). The formal floor is a ≥ 60-second
  row-level earlier-split embargo (max label horizon = 60 s = 60000 ms); the
  one-day purge (86,400 s) strictly dominates it.
- The internal holdout (2024-11-17 .. 2024-11-30) is a one-time dry-run only; it
  is **not** the project's single-use sealed test (the v002 TEST split
  2025-02-14 .. 2025-02-28, which this module never touches).
- Any date outside the pre-v002 segment raises :class:`PreV002SplitPolicyError`,
  including every v002-terminal date (2024-12-01 .. 2025-02-28) and every
  sealed-test date (2025-02-14 .. 2025-02-28).

This module performs **no I/O**: it reads no manifest, no Parquet, no gate
report, no sealed-test file, and no v002-terminal window; it writes nothing and
mutates nothing. It declares no local data-path constants. It does not build an
ML dataset, create a research matrix, train or score models, generate
predictions, run diagnostics, set any manifest ``chronological_split_policy``
field, flip eligibility, or authorize any successor. It is pure date / window
arithmetic that future ML-dataset tooling can depend on as a machine-checkable
split contract.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

# ---------------------------------------------------------------------------
# Policy identity
# ---------------------------------------------------------------------------

SPLIT_POLICY_NAME = "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"

# Split labels (typed literal values).
TRAIN = "train"
VALIDATION = "validation"
HOLDOUT = "holdout"
EMBARGO = "embargo"

# Splits that may carry model-eligible rows (embargo dates are dropped).
MODEL_ELIGIBLE_SPLITS: tuple[str, str, str] = (TRAIN, VALIDATION, HOLDOUT)
# Every assignment value emitted for an in-segment date.
ALL_SPLITS: tuple[str, str, str, str] = (TRAIN, VALIDATION, HOLDOUT, EMBARGO)

# ---------------------------------------------------------------------------
# Segment / split date constants (Phase 4bn-Y Candidate A, verbatim)
# ---------------------------------------------------------------------------

PRE_V002_START_DATE = "2024-03-01"
PRE_V002_END_DATE = "2024-11-30"

TRAIN_START_DATE = "2024-03-01"
TRAIN_END_DATE = "2024-09-30"

TRAIN_VALIDATION_EMBARGO_DATE = "2024-10-01"

VALIDATION_START_DATE = "2024-10-02"
VALIDATION_END_DATE = "2024-11-15"

VALIDATION_HOLDOUT_EMBARGO_DATE = "2024-11-16"

HOLDOUT_START_DATE = "2024-11-17"
HOLDOUT_END_DATE = "2024-11-30"

# Expected date counts (Phase 4bn-Y §11; 214 + 1 + 45 + 1 + 14 = 275).
EXPECTED_TRAIN_DATE_COUNT = 214
EXPECTED_VALIDATION_DATE_COUNT = 45
EXPECTED_HOLDOUT_DATE_COUNT = 14
EXPECTED_EMBARGO_DATE_COUNT = 2
EXPECTED_TOTAL_DATE_COUNT = 275

# ---------------------------------------------------------------------------
# Boundary timestamps and embargo / horizon constants
# ---------------------------------------------------------------------------

# Internal split-boundary UTC timestamps (epoch milliseconds). The validation
# split starts at 2024-10-02T00:00:00Z; the holdout split starts at
# 2024-11-17T00:00:00Z. The embargo dates 2024-10-01 and 2024-11-16 sit
# immediately before these boundaries and are dropped in full.
BOUNDARY_TRAIN_VALIDATION_MS = 1727827200000  # 2024-10-02T00:00:00Z (T_TV)
BOUNDARY_VALIDATION_HOLDOUT_MS = 1731801600000  # 2024-11-17T00:00:00Z (T_VH)

# Formal row-level earlier-split embargo floor (max declared horizon = 60 s).
MIN_BOUNDARY_EMBARGO_SECONDS = 60
MIN_BOUNDARY_EMBARGO_MS = MIN_BOUNDARY_EMBARGO_SECONDS * 1000

# Maximum forward label horizon governed by the policy.
MAX_LABEL_HORIZON_SECONDS = 60
MAX_LABEL_HORIZON_MS = MAX_LABEL_HORIZON_SECONDS * 1000

# The one-day purge is strictly more conservative than the 60-second floor.
ONE_DAY_PURGE_SECONDS = 86_400
ONE_DAY_PURGE_MS = ONE_DAY_PURGE_SECONDS * 1000

# Allowed forward label horizons (mirrors the locked v002 label schema).
ALLOWED_HORIZONS_MS: tuple[int, int, int, int] = (1000, 5000, 15000, 60000)

UTC_DAY_MS = 86_400_000

# ---------------------------------------------------------------------------
# Out-of-scope reference windows (never assigned, never read; raise on use)
# ---------------------------------------------------------------------------

# The published v002 terminal family and its sealed test are out of scope for
# this pre-v002 artefact. They are recorded here only so the contract can state
# their exclusion; this module never reads them and assigns them to no split.
V002_TERMINAL_START_DATE = "2024-12-01"
V002_TERMINAL_END_DATE = "2025-02-28"
SEALED_TEST_START_DATE = "2025-02-14"
SEALED_TEST_END_DATE = "2025-02-28"


class PreV002SplitPolicyError(ValueError):
    """Raised when a date / timestamp / horizon violates the pre-v002 policy."""


# ---------------------------------------------------------------------------
# Date helpers (pure)
# ---------------------------------------------------------------------------


def _coerce_date(value: str | date) -> date:
    """Coerce *value* (ISO ``str`` or :class:`datetime.date`) to a ``date``."""
    if isinstance(value, datetime):
        # Reject datetimes: split assignment is by calendar date only and a
        # naive/aware datetime here would invite timezone ambiguity.
        raise PreV002SplitPolicyError(
            "pass an ISO date string or datetime.date, not a datetime"
        )
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise PreV002SplitPolicyError(
            f"date must be an ISO string or datetime.date, got {type(value)!r}"
        )
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise PreV002SplitPolicyError(f"invalid ISO date {value!r}: {exc}") from exc


def _date_range_inclusive(start: str, end: str) -> list[str]:
    d0 = _coerce_date(start)
    d1 = _coerce_date(end)
    if d1 < d0:
        raise PreV002SplitPolicyError(f"end {end!r} precedes start {start!r}")
    out: list[str] = []
    cur = d0
    while cur <= d1:
        out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


def train_dates() -> list[str]:
    """Return the 214 train UTC date strings (inclusive)."""
    return _date_range_inclusive(TRAIN_START_DATE, TRAIN_END_DATE)


def validation_dates() -> list[str]:
    """Return the 45 validation UTC date strings (inclusive)."""
    return _date_range_inclusive(VALIDATION_START_DATE, VALIDATION_END_DATE)


def holdout_dates() -> list[str]:
    """Return the 14 internal-holdout / dry-run UTC date strings (inclusive)."""
    return _date_range_inclusive(HOLDOUT_START_DATE, HOLDOUT_END_DATE)


def embargo_dates() -> list[str]:
    """Return the 2 embargo UTC date strings (dropped from all splits)."""
    return [TRAIN_VALIDATION_EMBARGO_DATE, VALIDATION_HOLDOUT_EMBARGO_DATE]


def segment_dates() -> list[str]:
    """Return all 275 contiguous pre-v002 UTC date strings (inclusive)."""
    return _date_range_inclusive(PRE_V002_START_DATE, PRE_V002_END_DATE)


def utc_date_start_ms(utc_date: str | date) -> int:
    """Return the epoch-ms timestamp of 00:00:00Z on *utc_date*."""
    d = _coerce_date(utc_date)
    dt = datetime(d.year, d.month, d.day, tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def utc_date_for_timestamp_ms(source_transact_time_ms: int) -> str:
    """Return the UTC date (ISO string) of an epoch-ms timestamp.

    Assignment uses the UTC calendar date only; the local machine timezone
    cannot affect the result because the conversion is pinned to ``UTC``.
    """
    if isinstance(source_transact_time_ms, bool) or not isinstance(
        source_transact_time_ms, int
    ):
        raise PreV002SplitPolicyError("source_transact_time_ms must be an int")
    dt = datetime.fromtimestamp(source_transact_time_ms / 1000.0, tz=UTC)
    return dt.date().isoformat()


# ---------------------------------------------------------------------------
# Split assignment
# ---------------------------------------------------------------------------


def split_for_date(utc_date: str | date) -> str:
    """Return the split for *utc_date*.

    Returns one of :data:`TRAIN`, :data:`VALIDATION`, :data:`HOLDOUT`, or
    :data:`EMBARGO` for any date inside the pre-v002 segment (2024-03-01 ..
    2024-11-30). The two embargo dates (2024-10-01, 2024-11-16) return
    :data:`EMBARGO`; their rows are dropped from every model-eligible split.

    Raises :class:`PreV002SplitPolicyError` for any date outside the segment —
    including every v002-terminal date (2024-12-01 .. 2025-02-28) and every
    sealed-test date (2025-02-14 .. 2025-02-28).
    """
    d = _coerce_date(utc_date)
    seg_lo = _coerce_date(PRE_V002_START_DATE)
    seg_hi = _coerce_date(PRE_V002_END_DATE)
    if d < seg_lo or d > seg_hi:
        raise PreV002SplitPolicyError(
            f"date {d.isoformat()!r} is outside the pre-v002 segment "
            f"{PRE_V002_START_DATE}..{PRE_V002_END_DATE} "
            "(v002-terminal and sealed-test dates are out of scope)"
        )
    if _coerce_date(TRAIN_START_DATE) <= d <= _coerce_date(TRAIN_END_DATE):
        return TRAIN
    if d == _coerce_date(TRAIN_VALIDATION_EMBARGO_DATE):
        return EMBARGO
    if _coerce_date(VALIDATION_START_DATE) <= d <= _coerce_date(VALIDATION_END_DATE):
        return VALIDATION
    if d == _coerce_date(VALIDATION_HOLDOUT_EMBARGO_DATE):
        return EMBARGO
    if _coerce_date(HOLDOUT_START_DATE) <= d <= _coerce_date(HOLDOUT_END_DATE):
        return HOLDOUT
    # Unreachable: the segment is contiguous and exactly partitioned.
    raise PreV002SplitPolicyError(  # pragma: no cover - defensive
        f"date {d.isoformat()!r} fell through the pre-v002 partition"
    )


def split_for_timestamp_ms(source_transact_time_ms: int) -> str:
    """Return the split for a row given its ``source_transact_time_ms``.

    Assignment is by the UTC date of ``source_transact_time_ms`` (the recorded
    policy clock), independent of any partition filename or local timezone.
    """
    return split_for_date(utc_date_for_timestamp_ms(source_transact_time_ms))


def is_train_date(utc_date: str | date) -> bool:
    """Return True iff *utc_date* is a train date."""
    return split_for_date(utc_date) == TRAIN


def is_validation_date(utc_date: str | date) -> bool:
    """Return True iff *utc_date* is a validation date."""
    return split_for_date(utc_date) == VALIDATION


def is_holdout_date(utc_date: str | date) -> bool:
    """Return True iff *utc_date* is an internal-holdout / dry-run date."""
    return split_for_date(utc_date) == HOLDOUT


def is_embargo_date(utc_date: str | date) -> bool:
    """Return True iff *utc_date* is one of the two embargo (dropped) dates."""
    return split_for_date(utc_date) == EMBARGO


def is_model_eligible_split(split: str) -> bool:
    """Return True iff *split* may carry model-eligible rows.

    Embargo rows are dropped and are never model-eligible. Raises for any
    unknown split label.
    """
    if split in MODEL_ELIGIBLE_SPLITS:
        return True
    if split == EMBARGO:
        return False
    raise PreV002SplitPolicyError(f"unknown split {split!r}")


def policy_date_inventory() -> tuple[tuple[str, str], ...]:
    """Return ``(utc_date, split)`` for every date in the pre-v002 segment.

    Includes embargo dates (assigned :data:`EMBARGO`). The result covers all
    275 in-segment dates in chronological order with no duplicates and no gaps.
    """
    return tuple((d, split_for_date(d)) for d in segment_dates())


# ---------------------------------------------------------------------------
# Embargo / boundary-crossing arithmetic
# ---------------------------------------------------------------------------


def validate_horizon_ms(horizon_ms: int) -> int:
    """Validate that *horizon_ms* is an allowed label horizon and return it.

    Allowed horizons are 1000 / 5000 / 15000 / 60000 ms. Raises
    :class:`PreV002SplitPolicyError` otherwise.
    """
    if isinstance(horizon_ms, bool) or not isinstance(horizon_ms, int):
        raise PreV002SplitPolicyError("horizon_ms must be an int")
    if horizon_ms not in ALLOWED_HORIZONS_MS:
        raise PreV002SplitPolicyError(
            f"horizon_ms {horizon_ms!r} not in allowed horizons "
            f"{ALLOWED_HORIZONS_MS}"
        )
    return horizon_ms


def earlier_split_embargo_window_ms(split: str) -> tuple[int, int] | None:
    """Return the ``[lo, hi)`` ≥ 60 s embargo window for *split* as earlier split.

    A row of *split* whose ``source_transact_time_ms`` falls in ``[lo, hi)`` is
    boundary-crossing under the formal 60-second floor and is excluded from
    *split* (the earlier split) only; rows are never reassigned forward.
    Returns ``None`` for :data:`HOLDOUT`, which is the latest pre-v002 split and
    never the earlier split at any internal boundary. Raises for
    :data:`EMBARGO` (dropped; not an assignable earlier split) and unknown
    labels.
    """
    if split == TRAIN:
        return (
            BOUNDARY_TRAIN_VALIDATION_MS - MIN_BOUNDARY_EMBARGO_MS,
            BOUNDARY_TRAIN_VALIDATION_MS,
        )
    if split == VALIDATION:
        return (
            BOUNDARY_VALIDATION_HOLDOUT_MS - MIN_BOUNDARY_EMBARGO_MS,
            BOUNDARY_VALIDATION_HOLDOUT_MS,
        )
    if split == HOLDOUT:
        return None
    raise PreV002SplitPolicyError(f"unknown earlier split {split!r}")


def is_embargoed(split: str, source_transact_time_ms: int) -> bool:
    """Return True iff a *split* row is excluded by the ≥ 60 s earlier-split embargo."""
    if isinstance(source_transact_time_ms, bool) or not isinstance(
        source_transact_time_ms, int
    ):
        raise PreV002SplitPolicyError("source_transact_time_ms must be an int")
    window = earlier_split_embargo_window_ms(split)
    if window is None:
        return False
    lo, hi = window
    return lo <= source_transact_time_ms < hi


def _earlier_split_boundary_ms(split: str) -> int | None:
    if split == TRAIN:
        return BOUNDARY_TRAIN_VALIDATION_MS
    if split == VALIDATION:
        return BOUNDARY_VALIDATION_HOLDOUT_MS
    if split == HOLDOUT:
        return None
    raise PreV002SplitPolicyError(f"unknown split {split!r}")


def is_earlier_split_boundary_crossing(
    source_transact_time_ms: int, horizon_ms: int, split: str
) -> bool:
    """Return True iff an earlier-split row's forward target crosses its boundary.

    For a row in *split* at ``T = source_transact_time_ms`` with forward label
    horizon ``H = horizon_ms``, the target time is ``T + H``. A boundary
    crossing exists when ``T + H >= boundary`` where:

    - for :data:`TRAIN`, ``boundary`` is the validation start
      ``2024-10-02T00:00:00Z`` (:data:`BOUNDARY_TRAIN_VALIDATION_MS`);
    - for :data:`VALIDATION`, ``boundary`` is the holdout start
      ``2024-11-17T00:00:00Z`` (:data:`BOUNDARY_VALIDATION_HOLDOUT_MS`);
    - for :data:`HOLDOUT`, there is no later pre-v002 split, so this is always
      ``False`` (label-envelope censoring at the segment terminal is a label
      concern handled outside this split-policy artefact).

    Raises :class:`PreV002SplitPolicyError` if *horizon_ms* is not an allowed
    horizon, if ``T``'s UTC date is outside the pre-v002 segment, or if *split*
    is :data:`EMBARGO` (dropped rows) or unknown.
    """
    validate_horizon_ms(horizon_ms)
    # Out-of-segment rows are never assignable under this policy.
    utc_date_for_timestamp_ms(source_transact_time_ms)  # int guard
    split_for_timestamp_ms(source_transact_time_ms)  # raises if out of segment
    if split == EMBARGO:
        raise PreV002SplitPolicyError(
            "embargo rows are dropped; boundary crossing is undefined for them"
        )
    boundary = _earlier_split_boundary_ms(split)
    if boundary is None:  # HOLDOUT
        return False
    return source_transact_time_ms + horizon_ms >= boundary


def boundary_crossing_window_ms(split: str, horizon_ms: int) -> tuple[int, int] | None:
    """Return the ``[lo, hi)`` window where a *split* row's *horizon* target crosses.

    For horizon ``H`` an earlier-split row at ``T`` is boundary-crossing for that
    horizon when ``T in [boundary - H, boundary)``. This is a per-horizon
    sub-estimate of the single ≥ 60 s embargo (sized to the maximum horizon).
    Returns ``None`` for :data:`HOLDOUT`. Raises for invalid horizons, embargo,
    or unknown splits.
    """
    validate_horizon_ms(horizon_ms)
    if split == EMBARGO:
        raise PreV002SplitPolicyError(
            "embargo rows are dropped; boundary crossing is undefined for them"
        )
    boundary = _earlier_split_boundary_ms(split)
    if boundary is None:  # HOLDOUT
        return None
    return (boundary - horizon_ms, boundary)


# ---------------------------------------------------------------------------
# Arithmetic / contract proofs
# ---------------------------------------------------------------------------


def validate_policy_arithmetic() -> bool:
    """Assert the 214 / 1 / 45 / 1 / 14 = 275 partition is exact.

    Returns ``True`` on success; raises :class:`PreV002SplitPolicyError` if any
    count, the total, or the segment partition is inconsistent.
    """
    n_train = len(train_dates())
    n_val = len(validation_dates())
    n_hold = len(holdout_dates())
    n_emb = len(embargo_dates())
    n_total = len(segment_dates())

    checks: tuple[tuple[str, int, int], ...] = (
        ("train", n_train, EXPECTED_TRAIN_DATE_COUNT),
        ("validation", n_val, EXPECTED_VALIDATION_DATE_COUNT),
        ("holdout", n_hold, EXPECTED_HOLDOUT_DATE_COUNT),
        ("embargo", n_emb, EXPECTED_EMBARGO_DATE_COUNT),
        ("total", n_total, EXPECTED_TOTAL_DATE_COUNT),
    )
    for name, got, expected in checks:
        if got != expected:
            raise PreV002SplitPolicyError(
                f"{name} date count {got} != expected {expected}"
            )

    if n_train + n_emb + n_val + n_hold != n_total:
        raise PreV002SplitPolicyError(
            "partition arithmetic mismatch: "
            f"{n_train} + {n_emb} + {n_val} + {n_hold} != {n_total}"
        )
    if EXPECTED_TOTAL_DATE_COUNT != 214 + 1 + 45 + 1 + 14:
        raise PreV002SplitPolicyError("214 + 1 + 45 + 1 + 14 != 275")

    # Inventory covers every in-segment date exactly once with no overlap.
    inv = policy_date_inventory()
    inv_dates = [d for d, _ in inv]
    if len(inv_dates) != n_total or len(set(inv_dates)) != n_total:
        raise PreV002SplitPolicyError("inventory has missing or duplicate dates")
    train_set = set(train_dates())
    val_set = set(validation_dates())
    hold_set = set(holdout_dates())
    emb_set = set(embargo_dates())
    if train_set & val_set or train_set & hold_set or val_set & hold_set:
        raise PreV002SplitPolicyError("model-eligible splits overlap")
    if emb_set & (train_set | val_set | hold_set):
        raise PreV002SplitPolicyError("embargo date assignable to another split")
    if train_set | emb_set | val_set | hold_set != set(inv_dates):
        raise PreV002SplitPolicyError("split union does not equal the segment")
    return True


def build_split_policy_contract() -> dict[str, object]:
    """Return an inert, JSON-serialisable contract for the pre-v002 split policy.

    Records the policy name, the segment / split / embargo dates and counts, the
    boundary timestamps, the embargo and horizon settings, the v002-terminal /
    sealed-test exclusions, the future allowed source scope (pre-v002 only), and
    the non-authorization / no-data-I/O evidence flags. This helper reads and
    writes no files and mutates nothing.
    """
    return {
        "split_policy_name": SPLIT_POLICY_NAME,
        "segment_start_date": PRE_V002_START_DATE,
        "segment_end_date": PRE_V002_END_DATE,
        "train_start_date": TRAIN_START_DATE,
        "train_end_date": TRAIN_END_DATE,
        "train_validation_embargo_date": TRAIN_VALIDATION_EMBARGO_DATE,
        "validation_start_date": VALIDATION_START_DATE,
        "validation_end_date": VALIDATION_END_DATE,
        "validation_holdout_embargo_date": VALIDATION_HOLDOUT_EMBARGO_DATE,
        "holdout_start_date": HOLDOUT_START_DATE,
        "holdout_end_date": HOLDOUT_END_DATE,
        "train_date_count": EXPECTED_TRAIN_DATE_COUNT,
        "validation_date_count": EXPECTED_VALIDATION_DATE_COUNT,
        "holdout_date_count": EXPECTED_HOLDOUT_DATE_COUNT,
        "embargo_date_count": EXPECTED_EMBARGO_DATE_COUNT,
        "total_date_count": EXPECTED_TOTAL_DATE_COUNT,
        "embargo_dates": list(embargo_dates()),
        "boundary_train_validation_ms": BOUNDARY_TRAIN_VALIDATION_MS,
        "boundary_validation_holdout_ms": BOUNDARY_VALIDATION_HOLDOUT_MS,
        "min_boundary_embargo_seconds": MIN_BOUNDARY_EMBARGO_SECONDS,
        "min_boundary_embargo_ms": MIN_BOUNDARY_EMBARGO_MS,
        "max_label_horizon_seconds": MAX_LABEL_HORIZON_SECONDS,
        "max_label_horizon_ms": MAX_LABEL_HORIZON_MS,
        "one_day_purge_seconds": ONE_DAY_PURGE_SECONDS,
        "allowed_horizons_ms": list(ALLOWED_HORIZONS_MS),
        "assignment_rule": "source_transact_time_ms_utc_date",
        "ordering_rule": "chronological_only",
        "boundary_crossing_rule": "exclude_from_earlier_split",
        "holdout_is_sealed_test": False,
        "holdout_role": "internal_dry_run_only",
        "v002_terminal_start_date": V002_TERMINAL_START_DATE,
        "v002_terminal_end_date": V002_TERMINAL_END_DATE,
        "sealed_test_start_date": SEALED_TEST_START_DATE,
        "sealed_test_end_date": SEALED_TEST_END_DATE,
        "future_allowed_source_scope": "pre_v002_only",
        "future_allowed_source_start_date": PRE_V002_START_DATE,
        "future_allowed_source_end_date": PRE_V002_END_DATE,
        # Evidence flags — all conservative, all recorded as proof.
        "no_shuffle": True,
        "no_random_split": True,
        "no_kfold_over_time": True,
        "no_bootstrap": True,
        "no_post_hoc_temporal_resampling": True,
        "no_data_io": True,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "test_rows_loaded": 0,
        "set_manifest_chronological_split_policy": False,
        "flipped_research_eligible": False,
        "transitioned_eligibility_gate_status": False,
        "no_successor_authorization": True,
    }


__all__ = [
    "SPLIT_POLICY_NAME",
    "TRAIN",
    "VALIDATION",
    "HOLDOUT",
    "EMBARGO",
    "MODEL_ELIGIBLE_SPLITS",
    "ALL_SPLITS",
    "PRE_V002_START_DATE",
    "PRE_V002_END_DATE",
    "TRAIN_START_DATE",
    "TRAIN_END_DATE",
    "TRAIN_VALIDATION_EMBARGO_DATE",
    "VALIDATION_START_DATE",
    "VALIDATION_END_DATE",
    "VALIDATION_HOLDOUT_EMBARGO_DATE",
    "HOLDOUT_START_DATE",
    "HOLDOUT_END_DATE",
    "EXPECTED_TRAIN_DATE_COUNT",
    "EXPECTED_VALIDATION_DATE_COUNT",
    "EXPECTED_HOLDOUT_DATE_COUNT",
    "EXPECTED_EMBARGO_DATE_COUNT",
    "EXPECTED_TOTAL_DATE_COUNT",
    "BOUNDARY_TRAIN_VALIDATION_MS",
    "BOUNDARY_VALIDATION_HOLDOUT_MS",
    "MIN_BOUNDARY_EMBARGO_SECONDS",
    "MIN_BOUNDARY_EMBARGO_MS",
    "MAX_LABEL_HORIZON_SECONDS",
    "MAX_LABEL_HORIZON_MS",
    "ONE_DAY_PURGE_SECONDS",
    "ONE_DAY_PURGE_MS",
    "ALLOWED_HORIZONS_MS",
    "UTC_DAY_MS",
    "V002_TERMINAL_START_DATE",
    "V002_TERMINAL_END_DATE",
    "SEALED_TEST_START_DATE",
    "SEALED_TEST_END_DATE",
    "PreV002SplitPolicyError",
    "train_dates",
    "validation_dates",
    "holdout_dates",
    "embargo_dates",
    "segment_dates",
    "utc_date_start_ms",
    "utc_date_for_timestamp_ms",
    "split_for_date",
    "split_for_timestamp_ms",
    "is_train_date",
    "is_validation_date",
    "is_holdout_date",
    "is_embargo_date",
    "is_model_eligible_split",
    "policy_date_inventory",
    "validate_horizon_ms",
    "earlier_split_embargo_window_ms",
    "is_embargoed",
    "is_earlier_split_boundary_crossing",
    "boundary_crossing_window_ms",
    "validate_policy_arithmetic",
    "build_split_policy_contract",
]
