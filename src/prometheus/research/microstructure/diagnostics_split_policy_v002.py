"""Phase 4bm-W — chronological split-policy helpers for descriptive diagnostics.

Pure, inert, offline policy logic implementing the Phase 4bm-U recorded
chronological split policy ``CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO``
for the multi-day v002 BTCUSDT label/feature family
(``microstructure_labels_aggtrades_v001 @ v002``; 90 contiguous UTC dates
2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s/5s/15s/60s).

This module never performs any I/O, never reads any manifest, never reads
any parquet, and never mutates anything. It encodes the split windows, the
two split-boundary UTC timestamps, and the minimum 60-second boundary
embargo, and it provides per-row assignment / embargo predicates used by the
descriptive diagnostics in
:mod:`prometheus.research.microstructure.descriptive_diagnostics_v002`.

Policy summary (Phase 4bm-U ``split_policy_status = "recorded"``):

- Train      : 2024-12-01 .. 2025-01-14 inclusive (45 UTC dates).
- Validation : 2025-01-15 .. 2025-02-13 inclusive (30 UTC dates).
- Test       : 2025-02-14 .. 2025-02-28 inclusive (15 UTC dates).
- Rows are assigned by ``source_transact_time_ms`` UTC date.
- Train/validation boundary ``T_TV`` = 2025-01-15T00:00:00Z = 1736899200000 ms.
- Validation/test boundary ``T_VT`` = 2025-02-14T00:00:00Z = 1739491200000 ms.
- Minimum 60-second boundary embargo at ``T_TV`` and ``T_VT`` (max declared
  horizon = 60s). Boundary-crossing rows are excluded from the *earlier*
  split only; they are never reassigned forward.
- No random / shuffled / k-fold-over-time / bootstrap / post-hoc temporal
  resampling split.
- The test / final holdout is single-use; a descriptive diagnostics phase may
  compute descriptive summaries on it but must never use it for feature
  selection, model selection, hyperparameter selection, threshold tuning,
  strategy design, diagnostic iteration, or eligibility rescue.

Phase 4bm-W runs descriptive diagnostics only. This module selects, ranks,
tunes, fits, trains, simulates, and designs nothing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

# ---------------------------------------------------------------------------
# Recorded policy constants (Phase 4bm-U)
# ---------------------------------------------------------------------------

SPLIT_POLICY_NAME = "CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO"

TRAIN = "train"
VALIDATION = "validation"
TEST = "test"
SPLIT_NAMES: tuple[str, str, str] = (TRAIN, VALIDATION, TEST)

TRAIN_START_DATE = "2024-12-01"
TRAIN_END_DATE = "2025-01-14"
VALIDATION_START_DATE = "2025-01-15"
VALIDATION_END_DATE = "2025-02-13"
TEST_START_DATE = "2025-02-14"
TEST_END_DATE = "2025-02-28"

EXPECTED_TRAIN_DATE_COUNT = 45
EXPECTED_VALIDATION_DATE_COUNT = 30
EXPECTED_TEST_DATE_COUNT = 15
EXPECTED_TOTAL_DATE_COUNT = 90

# Split-boundary UTC timestamps (epoch milliseconds).
BOUNDARY_TRAIN_VALIDATION_MS = 1736899200000  # 2025-01-15T00:00:00Z (T_TV)
BOUNDARY_VALIDATION_TEST_MS = 1739491200000  # 2025-02-14T00:00:00Z (T_VT)

# Minimum boundary embargo (max declared horizon = 60s).
MIN_BOUNDARY_EMBARGO_SECONDS = 60
MIN_BOUNDARY_EMBARGO_MS = MIN_BOUNDARY_EMBARGO_SECONDS * 1000

# Horizons (mirrors the locked v002 label schema).
HORIZONS: tuple[str, str, str, str] = ("1s", "5s", "15s", "60s")
HORIZON_MS: dict[str, int] = {"1s": 1000, "5s": 5000, "15s": 15000, "60s": 60000}

# Envelope-terminal censoring boundary (2025-02-28T23:59:59.996Z).
ENVELOPE_TERMINAL_UNIX_MS = 1740787199996

UTC_DAY_MS = 86_400_000

# The seven prohibited test-holdout uses (all forbidden by the recorded
# policy; recorded here so diagnostics can assert holdout protection).
PROHIBITED_TEST_HOLDOUT_USES: tuple[str, ...] = (
    "feature_selection",
    "model_selection",
    "hyperparameter_selection",
    "threshold_tuning",
    "strategy_design",
    "diagnostic_iteration",
    "eligibility_rescue",
)


class SplitPolicyError(ValueError):
    """Raised when a date or timestamp violates the recorded split policy."""


def _parse_iso_date(value: str) -> date:
    if not isinstance(value, str):
        raise SplitPolicyError(f"date must be a string, got {type(value)!r}")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:  # pragma: no cover - defensive
        raise SplitPolicyError(f"invalid ISO date {value!r}: {exc}") from exc


def _date_range_inclusive(start: str, end: str) -> list[str]:
    d0 = _parse_iso_date(start)
    d1 = _parse_iso_date(end)
    if d1 < d0:
        raise SplitPolicyError(f"end {end!r} precedes start {start!r}")
    out: list[str] = []
    cur = d0
    while cur <= d1:
        out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


def train_dates() -> list[str]:
    """Return the 45 train UTC date strings (inclusive)."""
    return _date_range_inclusive(TRAIN_START_DATE, TRAIN_END_DATE)


def validation_dates() -> list[str]:
    """Return the 30 validation UTC date strings (inclusive)."""
    return _date_range_inclusive(VALIDATION_START_DATE, VALIDATION_END_DATE)


def test_dates() -> list[str]:
    """Return the 15 test/final-holdout UTC date strings (inclusive)."""
    return _date_range_inclusive(TEST_START_DATE, TEST_END_DATE)


def all_dates() -> list[str]:
    """Return all 90 contiguous v002 UTC date strings (inclusive)."""
    return _date_range_inclusive(TRAIN_START_DATE, TEST_END_DATE)


def split_for_date(utc_date: str) -> str:
    """Return the split (``train`` / ``validation`` / ``test``) for *utc_date*.

    Raises :class:`SplitPolicyError` if the date is outside the locked
    90-day v002 envelope.
    """
    d = _parse_iso_date(utc_date)
    if _parse_iso_date(TRAIN_START_DATE) <= d <= _parse_iso_date(TRAIN_END_DATE):
        return TRAIN
    if (
        _parse_iso_date(VALIDATION_START_DATE)
        <= d
        <= _parse_iso_date(VALIDATION_END_DATE)
    ):
        return VALIDATION
    if _parse_iso_date(TEST_START_DATE) <= d <= _parse_iso_date(TEST_END_DATE):
        return TEST
    raise SplitPolicyError(
        f"date {utc_date!r} is outside the v002 envelope "
        f"{TRAIN_START_DATE}..{TEST_END_DATE}"
    )


def split_for_source_transact_time_ms(source_transact_time_ms: int) -> str:
    """Return the split for a row given its ``source_transact_time_ms``.

    Assignment is by UTC date of ``source_transact_time_ms`` (the recorded
    policy clock), independent of any partition filename.
    """
    if isinstance(source_transact_time_ms, bool) or not isinstance(
        source_transact_time_ms, int
    ):
        raise SplitPolicyError("source_transact_time_ms must be an int")
    dt = datetime.fromtimestamp(source_transact_time_ms / 1000.0, tz=UTC)
    return split_for_date(dt.date().isoformat())


def utc_date_start_ms(utc_date: str) -> int:
    """Return the epoch-ms timestamp of 00:00:00Z on *utc_date*."""
    d = _parse_iso_date(utc_date)
    dt = datetime(d.year, d.month, d.day, tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def earlier_split_embargo_window_ms(split: str) -> tuple[int, int] | None:
    """Return the ``[lo, hi)`` embargo window for *split* as the earlier split.

    A row of *split* whose ``source_transact_time_ms`` falls in ``[lo, hi)``
    is boundary-crossing under the 60-second embargo and is excluded from
    *split* (the earlier split) only. Returns ``None`` for the test split,
    which is never the earlier split at any boundary.
    """
    if split == TRAIN:
        return (
            BOUNDARY_TRAIN_VALIDATION_MS - MIN_BOUNDARY_EMBARGO_MS,
            BOUNDARY_TRAIN_VALIDATION_MS,
        )
    if split == VALIDATION:
        return (
            BOUNDARY_VALIDATION_TEST_MS - MIN_BOUNDARY_EMBARGO_MS,
            BOUNDARY_VALIDATION_TEST_MS,
        )
    if split == TEST:
        return None
    raise SplitPolicyError(f"unknown split {split!r}")


def is_embargoed(split: str, source_transact_time_ms: int) -> bool:
    """Return True if a *split* row is excluded by the 60-second embargo.

    Embargo applies to the earlier split at each boundary: train rows in
    ``[T_TV-60000, T_TV)`` and validation rows in ``[T_VT-60000, T_VT)``.
    """
    window = earlier_split_embargo_window_ms(split)
    if window is None:
        return False
    lo, hi = window
    return lo <= source_transact_time_ms < hi


def boundary_crossing_window_ms(split: str, horizon: str) -> tuple[int, int] | None:
    """Return the ``[lo, hi)`` window where a *split* row's *horizon* target crosses.

    For horizon ``H`` (ms ``H_ms``), an earlier-split row at ``T`` is
    boundary-crossing for that horizon when ``T + H_ms > boundary`` and
    ``T < boundary`` — i.e. ``T`` in ``[boundary - H_ms, boundary)``. This is
    a descriptive per-horizon sub-estimate of the single 60-second embargo
    (which is sized to the maximum horizon). Returns ``None`` for test.
    """
    if horizon not in HORIZON_MS:
        raise SplitPolicyError(f"unknown horizon {horizon!r}")
    h_ms = HORIZON_MS[horizon]
    if split == TRAIN:
        boundary = BOUNDARY_TRAIN_VALIDATION_MS
    elif split == VALIDATION:
        boundary = BOUNDARY_VALIDATION_TEST_MS
    elif split == TEST:
        return None
    else:
        raise SplitPolicyError(f"unknown split {split!r}")
    return (boundary - h_ms, boundary)


@dataclass(frozen=True)
class SplitPolicySnapshot:
    """An inert, serialisable snapshot of the recorded split policy."""

    split_policy_name: str = SPLIT_POLICY_NAME
    train_start_date: str = TRAIN_START_DATE
    train_end_date: str = TRAIN_END_DATE
    validation_start_date: str = VALIDATION_START_DATE
    validation_end_date: str = VALIDATION_END_DATE
    test_start_date: str = TEST_START_DATE
    test_end_date: str = TEST_END_DATE
    train_date_count: int = EXPECTED_TRAIN_DATE_COUNT
    validation_date_count: int = EXPECTED_VALIDATION_DATE_COUNT
    test_date_count: int = EXPECTED_TEST_DATE_COUNT
    total_date_count: int = EXPECTED_TOTAL_DATE_COUNT
    boundary_train_validation_ms: int = BOUNDARY_TRAIN_VALIDATION_MS
    boundary_validation_test_ms: int = BOUNDARY_VALIDATION_TEST_MS
    minimum_boundary_embargo_seconds: int = MIN_BOUNDARY_EMBARGO_SECONDS
    assignment_rule: str = "source_transact_time_ms_utc_date"
    boundary_crossing_rule: str = "exclude_from_earlier_split"
    no_shuffle_rule: bool = True
    random_split_allowed: bool = False
    shuffled_cv_allowed: bool = False
    bootstrap_split_allowed: bool = False
    test_holdout_rule: str = "single_use_final_holdout"

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable dict of the snapshot fields."""
        return {
            "split_policy_name": self.split_policy_name,
            "train_start_date": self.train_start_date,
            "train_end_date": self.train_end_date,
            "validation_start_date": self.validation_start_date,
            "validation_end_date": self.validation_end_date,
            "test_start_date": self.test_start_date,
            "test_end_date": self.test_end_date,
            "train_date_count": self.train_date_count,
            "validation_date_count": self.validation_date_count,
            "test_date_count": self.test_date_count,
            "total_date_count": self.total_date_count,
            "boundary_train_validation_ms": self.boundary_train_validation_ms,
            "boundary_validation_test_ms": self.boundary_validation_test_ms,
            "minimum_boundary_embargo_seconds": (
                self.minimum_boundary_embargo_seconds
            ),
            "assignment_rule": self.assignment_rule,
            "boundary_crossing_rule": self.boundary_crossing_rule,
            "no_shuffle_rule": self.no_shuffle_rule,
            "random_split_allowed": self.random_split_allowed,
            "shuffled_cv_allowed": self.shuffled_cv_allowed,
            "bootstrap_split_allowed": self.bootstrap_split_allowed,
            "test_holdout_rule": self.test_holdout_rule,
            "prohibited_test_holdout_uses": list(PROHIBITED_TEST_HOLDOUT_USES),
        }
