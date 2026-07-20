"""Phase 4bn-AZ — CF-1 realized-volatility substrate: frozen constants + causal RV kernel.

Implements the execution-bearing scientific primitives frozen by the Phase 4bn-AY
CF-1 contract (``2026-07-15_phase-4bn-ay_cf1-target-feature-baseline-and-evaluation-
contract.md``). This module owns:

- the immutable CF-1 constants (horizon, cadence, floors, thresholds, dates, blocks);
- the single canonical grid-price operator ``P_at(u)`` (``source_transact_time_ms <= u``,
  greatest ``row_index`` tie);
- the causal completed-interval ``(a, b]`` realized-variance kernel over a 1-minute UTC
  grid, reduced to a per-segment minute grid for bounded memory;
- covered-minute counting under the predicate ``tau_{k-1} < ts <= tau_k``;
- HAR ``(t - L, t]`` lookback assembly (``RV_h`` / ``RV_d`` / ``RV_w``);
- origin validity (target endpoint inside execution access; weekly lookback inside the
  same accessible segment; coverage; positivity);
- the no-forbidden-partition guards (the only openable dates are 2024-03-01..2024-10-31
  excluding 2024-10-01);
- the deterministic synthetic timestamp-boundary proof (no market data, no reserve).

The realized-variance interval is **always** the causal completed interval ``(a, b]``; the
sole boundary operator is ``P_at(u)`` (``<= u``). No live ``[a, b)`` interval, ``P_minus``,
``P_start``, strict ``<`` at a grid boundary, mixed operators, or left-limit terminal price
exists anywhere in this module. Prices are combined in :class:`decimal.Decimal` and cast to
``float64`` only at the ``ln`` step (the committed label-compute convention).

This module performs **no** data I/O at import, opens **no** market-data / feature file,
uses **no** network, credential, endpoint, ``.env``, or MCP. It declares constants and pure
functions over numpy / :class:`decimal.Decimal` arrays; the reader that materialises the
minute grid from on-disk aggTrades lives in the orchestration script and hands numpy /
Decimal arrays to these functions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import numpy as np
import numpy.typing as npt

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------

PHASE_ID = "phase-4bn-az"
SYMBOL = "BTCUSDT"
TARGET_DATASET_FAMILY = "cf1_realized_volatility_substrate_test_v001"
CONTRACT_VERSION = "v001"

# Provenance SHAs frozen by Phase 4bn-AY (recorded, never recomputed here).
BASE_MAIN_COMMIT_SHA = "e65feb849c8020b5e157d1c472b1a075244c7d9d"
PHASE_4BN_AY_MERGE_COMMIT_SHA = "cd5a3b7128bb7bc8d887fb4c7ea1c1538e5b1305"
PHASE_4BN_AY_CONTRACT_TIP_SHA = "0fb560656aa9b50cf110602e15be8222b7343623"

# ---------------------------------------------------------------------------
# Frozen numeric contract (contract sections in comments)
# ---------------------------------------------------------------------------

HORIZON_MINUTES = 60  # contract section 4
MINUTE_MS = 60_000
HOUR_MS = 3_600_000
HORIZON_MS = HORIZON_MINUTES * MINUTE_MS  # 3_600_000 (H = 60 min)
GRID_STEPS = 60  # M = 60 one-minute returns per RV interval

TARGET_EPSILON = 1e-16  # contract section 3: y = ln(RV + 1e-16); v = RV + 1e-16
STANDARDIZATION_EPSILON = 1e-8  # contract section 14 (matches committed ml_baseline_design)

COVERAGE_MIN_COVERED_MINUTES = 30  # contract section 7: >= 30 of 60
COVERAGE_TOTAL_MINUTES = 60

HAR_HOUR_LAG_HOURS = 1  # RV_h = RV(t - 1h, t]
HAR_DAILY_HOURS = 24  # RV_d = mean of 24 completed hourly RV intervals
HAR_WEEKLY_HOURS = 168  # RV_w = mean of 168 completed hourly RV intervals

# Feature contract (section 11): exactly three sign-invariant 60s columns.
FEATURE_COLUMNS: tuple[str, str, str] = (
    "rolling_aggtrade_count_60s",
    "rolling_quantity_sum_60s",
    "rolling_quantity_mean_60s",
)

# Model / numerical guards (section 19).
BASELINE_N_PARAMS = 4  # intercept + RV_h + RV_d + RV_w
AUGMENTED_N_PARAMS = 7  # + 3 standardized log microstructure features
CONDITION_NUMBER_MAX = 1e10
MIN_TRAIN_ORIGINS = 70  # 10 * augmented parameters
MIN_BLOCK_VALID_ORIGINS = 100

# Bootstrap (section 29).
BOOTSTRAP_REPLICATES = 10_000
BOOTSTRAP_SEED = 20260715
BOOTSTRAP_LOWER_QUANTILE = 0.05

# Purge / embargo (section 24).
EMBARGO_MS = 86_400_000  # 1 calendar day
PURGE_MS = HORIZON_MS  # 1 hour, subsumed by the embargo

# ---------------------------------------------------------------------------
# Execution-access dates (contract section 21) and forbidden ranges
# ---------------------------------------------------------------------------

ACCESS_START_DATE = "2024-03-01"
ACCESS_END_DATE = "2024-10-31"
EXCLUDED_EMBARGO_DATE = "2024-10-01"  # inside [ACCESS_START, ACCESS_END] but excluded
EXPECTED_ALLOWED_DATE_COUNT = 244

WARMUP_START_DATE = "2024-03-01"  # train-only warmup
WARMUP_END_DATE = "2024-03-31"

# Forbidden ranges that must never be opened, loaded, hashed for new use, or parsed.
NOVEMBER_BUFFER_START_DATE = "2024-11-01"
NOVEMBER_BUFFER_END_DATE = "2024-11-15"
VALIDATION_HOLDOUT_EMBARGO_DATE = "2024-11-16"
CONSUMED_HOLDOUT_START_DATE = "2024-11-17"
CONSUMED_HOLDOUT_END_DATE = "2024-11-30"
TERMINAL_START_DATE = "2024-12-01"
TERMINAL_END_DATE = "2025-02-28"
SEALED_START_DATE = "2025-02-14"
SEALED_END_DATE = "2025-02-28"

# Evaluation blocks B1..B7 (contract section 22).
BLOCKS: tuple[tuple[str, str, str], ...] = (
    ("B1", "2024-04-01", "2024-04-30"),
    ("B2", "2024-05-01", "2024-05-31"),
    ("B3", "2024-06-01", "2024-06-30"),
    ("B4", "2024-07-01", "2024-07-31"),
    ("B5", "2024-08-01", "2024-08-31"),
    ("B6", "2024-09-01", "2024-09-30"),
    ("B7", "2024-10-02", "2024-10-31"),
)
BLOCK_IDS: tuple[str, ...] = tuple(b[0] for b in BLOCKS)
N_BLOCKS = 7

# The two accessible contiguous segments (no carry-forward stitch across the
# 2024-10-01 embargo or the outer boundaries).
ACCESSIBLE_SEGMENTS: tuple[tuple[str, str, str], ...] = (
    ("A", "2024-03-01", "2024-09-30"),
    ("B", "2024-10-02", "2024-10-31"),
)


class Cf1ContractError(RuntimeError):
    """Raised when a CF-1 frozen-contract invariant fails closed."""


class Cf1ForbiddenPartitionError(Cf1ContractError):
    """Raised when a forbidden UTC date / partition is referenced for opening."""


# ---------------------------------------------------------------------------
# Date / timestamp helpers (pure; UTC only)
# ---------------------------------------------------------------------------


def _coerce_date(value: str | date) -> date:
    if isinstance(value, datetime):
        raise Cf1ContractError("pass an ISO date string or datetime.date, not a datetime")
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise Cf1ContractError(f"date must be ISO str or date, got {type(value)!r}")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise Cf1ContractError(f"invalid ISO date {value!r}: {exc}") from exc


def utc_date_start_ms(utc_date: str | date) -> int:
    """Return the epoch-ms timestamp of 00:00:00.000Z on *utc_date*."""
    d = _coerce_date(utc_date)
    return int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp() * 1000)


def utc_date_for_timestamp_ms(ts_ms: int) -> str:
    """Return the UTC calendar date (ISO string) of an epoch-ms timestamp."""
    if isinstance(ts_ms, bool) or not isinstance(ts_ms, int):
        raise Cf1ContractError("ts_ms must be an int")
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=UTC).date().isoformat()


def _date_range_inclusive(start: str, end: str) -> list[str]:
    d0 = _coerce_date(start)
    d1 = _coerce_date(end)
    if d1 < d0:
        raise Cf1ContractError(f"end {end!r} precedes start {start!r}")
    out: list[str] = []
    cur = d0
    while cur <= d1:
        out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


def allowed_utc_dates() -> tuple[str, ...]:
    """Return the 244 openable UTC dates: 2024-03-01..2024-10-31 excluding 2024-10-01."""
    dates = [
        d
        for d in _date_range_inclusive(ACCESS_START_DATE, ACCESS_END_DATE)
        if d != EXCLUDED_EMBARGO_DATE
    ]
    if len(dates) != EXPECTED_ALLOWED_DATE_COUNT:
        raise Cf1ContractError(f"allowed date count {len(dates)} != {EXPECTED_ALLOWED_DATE_COUNT}")
    return tuple(dates)


_ALLOWED_DATE_SET: frozenset[str] = frozenset(allowed_utc_dates())


def is_allowed_date(utc_date: str | date) -> bool:
    """Return True iff *utc_date* is one of the 244 openable CF-1 dates."""
    return _coerce_date(utc_date).isoformat() in _ALLOWED_DATE_SET


def forbidden_date_ranges() -> tuple[tuple[str, str, str], ...]:
    """Return ``(reason, start, end)`` triples for every forbidden UTC range."""
    return (
        ("october_boundary_embargo", EXCLUDED_EMBARGO_DATE, EXCLUDED_EMBARGO_DATE),
        (
            "november_unused_non_reserve_buffer",
            NOVEMBER_BUFFER_START_DATE,
            NOVEMBER_BUFFER_END_DATE,
        ),
        (
            "validation_holdout_embargo",
            VALIDATION_HOLDOUT_EMBARGO_DATE,
            VALIDATION_HOLDOUT_EMBARGO_DATE,
        ),
        ("consumed_pre_v002_holdout", CONSUMED_HOLDOUT_START_DATE, CONSUMED_HOLDOUT_END_DATE),
        ("v002_terminal_window", TERMINAL_START_DATE, TERMINAL_END_DATE),
        ("v002_sealed_test", SEALED_START_DATE, SEALED_END_DATE),
    )


def assert_partition_allowed(utc_date: str | date) -> str:
    """Return the ISO date after fail-closing if *utc_date* may not be opened.

    This is the no-forbidden-partition guard: only the 244 CF-1 execution-access
    dates may be opened. Every other date — including 2024-10-01, the
    2024-11-01..2024-11-15 buffer, 2024-11-16, the consumed holdout, the v002
    terminal window, and the v002 sealed test — raises
    :class:`Cf1ForbiddenPartitionError`.
    """
    iso = _coerce_date(utc_date).isoformat()
    if iso not in _ALLOWED_DATE_SET:
        raise Cf1ForbiddenPartitionError(
            f"UTC date {iso!r} is outside CF-1 execution access "
            f"(openable dates: 2024-03-01..2024-10-31 excluding 2024-10-01)"
        )
    return iso


def assert_partition_paths_allowed(utc_dates: list[str]) -> None:
    """Fail closed if any date in *utc_dates* is not an openable CF-1 date."""
    for d in utc_dates:
        assert_partition_allowed(d)


def segment_for_timestamp_ms(ts_ms: int) -> str | None:
    """Return the accessible-segment id ('A' or 'B') for *ts_ms*, else ``None``."""
    d = utc_date_for_timestamp_ms(ts_ms)
    for seg_id, lo, hi in ACCESSIBLE_SEGMENTS:
        if lo <= d <= hi:
            return seg_id
    return None


def block_for_origin_ms(origin_ms: int) -> str | None:
    """Return the evaluation-block id for an origin timestamp, else ``None``.

    Assignment is by the UTC date of the origin ``t`` (contract section 22). An
    origin in the March warmup or on 2024-10-01 returns ``None`` (no block).
    """
    d = utc_date_for_timestamp_ms(origin_ms)
    for block_id, lo, hi in BLOCKS:
        if lo <= d <= hi:
            return block_id
    return None


def is_hour_aligned(ts_ms: int) -> bool:
    """Return True iff *ts_ms* is a top-of-UTC-hour instant."""
    return ts_ms % HOUR_MS == 0


# ---------------------------------------------------------------------------
# Canonical grid-price operator P_at over raw trades (definition; used by the
# synthetic proof and by the minute-grid reducer).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IntervalRv:
    """Result of one causal completed-interval ``(a, b]`` realized-variance computation."""

    rv: float
    covered_minutes: int
    valid: bool
    reason: str  # "" when valid; otherwise a machine-readable invalid reason


def p_at_index(ts_sorted: npt.NDArray[np.int64], u: int) -> int:
    """Return the index of ``P_at(u)`` in *ts_sorted*, or -1 if no trade has ``ts <= u``.

    *ts_sorted* must be canonically sorted ascending by ``(transact_time_ms,
    row_index)``. Because equal timestamps are ordered by increasing ``row_index``,
    the rightmost position with ``ts <= u`` is the greatest ``row_index`` among the
    latest timestamp ``<= u`` — exactly the committed ``row_index_le_R`` tie rule.
    """
    pos = int(np.searchsorted(ts_sorted, u, side="right"))
    return pos - 1


def _decimal_ratio_log(numer: Decimal, denom: Decimal) -> float:
    """Return ``ln(numer / denom)`` with the division done in Decimal, cast at ln only."""
    if numer <= 0 or denom <= 0:
        raise Cf1ContractError("grid prices must be strictly positive")
    ratio = numer / denom
    return math.log(float(ratio))


def compute_rv_over_trades(
    ts_sorted: npt.NDArray[np.int64],
    prices: list[Decimal],
    a_ms: int,
    b_ms: int,
) -> IntervalRv:
    """Compute ``RV(a, b]`` directly over raw trades using the ``P_at`` operator.

    The interval must be exactly 60 minutes (``b - a == HOUR_MS``). ``tau_k = a +
    k*60000`` for ``k = 0..60``; ``G_k = P_at(tau_k)``; ``r_k = ln(G_k / G_{k-1})``;
    ``RV = sum r_k^2``. A minute ``(tau_{k-1}, tau_k]`` is covered iff at least one
    trade satisfies ``tau_{k-1} < ts <= tau_k``. Returns ``valid=False`` (never
    raising) when any grid price is missing / non-positive; raising is reserved for
    contract-structural errors.
    """
    if b_ms - a_ms != HOUR_MS:
        raise Cf1ContractError(f"interval length {b_ms - a_ms} != {HOUR_MS} (60 min)")
    if ts_sorted.shape[0] != len(prices):
        raise Cf1ContractError("ts / prices length mismatch")
    taus = [a_ms + k * MINUTE_MS for k in range(GRID_STEPS + 1)]
    grid_prices: list[Decimal] = []
    for tau in taus:
        idx = p_at_index(ts_sorted, tau)
        if idx < 0:
            return IntervalRv(0.0, 0, False, "no_price_at_boundary")
        px = prices[idx]
        if not (px > 0):
            return IntervalRv(0.0, 0, False, "non_positive_price")
        grid_prices.append(px)
    rv = 0.0
    for k in range(1, GRID_STEPS + 1):
        r = _decimal_ratio_log(grid_prices[k], grid_prices[k - 1])
        if not math.isfinite(r):
            return IntervalRv(0.0, 0, False, "non_finite_return")
        rv += r * r
    # Covered-minute count via searchsorted on the (right-closed) minute grid.
    right = np.searchsorted(ts_sorted, taus[1:], side="right")
    left = np.searchsorted(ts_sorted, taus[:-1], side="right")
    covered = int(np.count_nonzero((right - left) > 0))
    if not math.isfinite(rv):
        return IntervalRv(0.0, covered, False, "non_finite_rv")
    valid = covered >= COVERAGE_MIN_COVERED_MINUTES
    return IntervalRv(rv, covered, valid, "" if valid else "insufficient_target_coverage")


# ---------------------------------------------------------------------------
# Per-segment minute grid (bounded-memory reduction of the P_at operator)
# ---------------------------------------------------------------------------


@dataclass
class MinuteGrid:
    """A per-segment 1-minute UTC price grid: ``P_at`` sampled at every minute boundary.

    ``price[i]`` is ``P_at(seg_start_ms + i*60000)`` (a :class:`decimal.Decimal`, or
    ``None`` when no in-segment trade precedes that boundary). ``covered[i]`` is True
    iff at least one trade satisfies ``boundary_{i-1} < ts <= boundary_i`` (undefined /
    False at ``i == 0``). Carry-forward never crosses a segment boundary, so no
    stitching across the 2024-10-01 embargo or the outer access edges can occur.
    """

    seg_id: str
    seg_start_ms: int  # first minute boundary (00:00:00.000Z of the segment's first date)
    n_minutes: int  # number of minute boundaries stored
    price: list[Decimal | None]
    price_known: npt.NDArray[np.bool_]
    covered: npt.NDArray[np.bool_]

    def minute_index(self, boundary_ms: int) -> int:
        """Return the grid index of *boundary_ms* (may be out of range)."""
        if (boundary_ms - self.seg_start_ms) % MINUTE_MS != 0:
            raise Cf1ContractError("boundary not minute-aligned to the segment grid")
        return (boundary_ms - self.seg_start_ms) // MINUTE_MS


def segment_boundaries(seg_start_date: str, seg_end_date: str) -> tuple[int, int]:
    """Return ``(seg_start_ms, seg_last_boundary_ms)`` for an accessible segment.

    The last stored boundary is one minute before 00:00 of the day after the last
    allowed date, so no boundary is ever created on a forbidden date (2024-10-01 for
    segment A; 2024-11-01 for segment B).
    """
    seg_start_ms = utc_date_start_ms(seg_start_date)
    day_after = _coerce_date(seg_end_date) + timedelta(days=1)
    seg_last_boundary_ms = utc_date_start_ms(day_after) - MINUTE_MS
    return seg_start_ms, seg_last_boundary_ms


def new_minute_grid(seg_id: str, seg_start_date: str, seg_end_date: str) -> MinuteGrid:
    """Allocate an empty :class:`MinuteGrid` for an accessible segment."""
    seg_start_ms, seg_last_boundary_ms = segment_boundaries(seg_start_date, seg_end_date)
    n = (seg_last_boundary_ms - seg_start_ms) // MINUTE_MS + 1
    return MinuteGrid(
        seg_id=seg_id,
        seg_start_ms=seg_start_ms,
        n_minutes=n,
        price=[None] * n,
        price_known=np.zeros(n, dtype=np.bool_),
        covered=np.zeros(n, dtype=np.bool_),
    )


def fill_minute_grid_from_trades(
    grid: MinuteGrid,
    ts_sorted: npt.NDArray[np.int64],
    prices: list[Decimal],
) -> None:
    """Populate *grid* from a canonically-sorted trade batch (the ``P_at`` reduction).

    For every minute boundary in the grid, ``price[i] = P_at(boundary_i)`` using all
    trades with ``ts <= boundary_i`` present in *ts_sorted* (which must include any
    prior in-segment trades needed for carry-forward). ``covered[i]`` marks whether a
    trade falls in ``(boundary_{i-1}, boundary_i]``. This applies the identical
    right-closed operator used by :func:`compute_rv_over_trades`; the synthetic proof
    and the production reader share this single reduction.
    """
    if ts_sorted.shape[0] != len(prices):
        raise Cf1ContractError("ts / prices length mismatch")
    boundaries = grid.seg_start_ms + np.arange(grid.n_minutes, dtype=np.int64) * MINUTE_MS
    pos = np.searchsorted(ts_sorted, boundaries, side="right")  # count of trades <= boundary
    prev = np.empty(grid.n_minutes, dtype=np.int64)
    prev[0] = 0
    prev[1:] = pos[:-1]
    for i in range(grid.n_minutes):
        p = int(pos[i])
        if p > 0:
            grid.price[i] = prices[p - 1]
            grid.price_known[i] = True
        if i > 0 and p - int(prev[i]) > 0:
            grid.covered[i] = True


def fill_minute_grid_day(
    grid: MinuteGrid,
    day_start_ms: int,
    ts_sorted: npt.NDArray[np.int64],
    price_strings: list[str],
    prev_last_ts: int | None,
    prev_last_price: Decimal | None,
) -> tuple[int | None, Decimal | None]:
    """Incrementally fill one UTC day's minute boundaries into the segment grid.

    Fills boundaries ``m = day_start .. min(D 23:59, seg_last)`` using the day's
    canonically-sorted trades (``P_at`` at each boundary; covered per minute), with a
    single-day forward carry (``prev_last_ts`` / ``prev_last_price``) used **only** at
    the midnight boundary to supply the pre-day price and to mark the cross-midnight
    minute covered. ``price_strings`` are the raw decimal price strings; only the
    chosen boundary prices are cast to :class:`decimal.Decimal` (never the whole day).
    Returns the updated carry (this day's last trade ts / price). The caller resets the
    carry to ``None`` at each accessible-segment start, so no carry-forward ever crosses
    the 2024-10-01 embargo or the outer access edges.
    """
    n = ts_sorted.shape[0]
    if n != len(price_strings):
        raise Cf1ContractError("ts / prices length mismatch")
    seg_last = grid.seg_start_ms + (grid.n_minutes - 1) * MINUTE_MS
    day_last = day_start_ms + 1439 * MINUTE_MS  # D 23:59
    hi = min(day_last, seg_last)
    if hi < day_start_ms:
        return prev_last_ts, prev_last_price
    n_b = (hi - day_start_ms) // MINUTE_MS + 1
    boundaries = day_start_ms + np.arange(n_b, dtype=np.int64) * MINUTE_MS
    pos = np.searchsorted(ts_sorted, boundaries, side="right")
    pos_prev = np.searchsorted(ts_sorted, boundaries - MINUTE_MS, side="right")
    for j in range(n_b):
        off = grid.minute_index(int(boundaries[j]))
        p = int(pos[j])
        if p > 0:
            grid.price[off] = Decimal(price_strings[p - 1])
            grid.price_known[off] = True
        elif j == 0 and prev_last_price is not None:
            grid.price[off] = prev_last_price
            grid.price_known[off] = True
        covered = (p - int(pos_prev[j])) > 0
        if j == 0 and prev_last_ts is not None and prev_last_ts > int(boundaries[0]) - MINUTE_MS:
            covered = True
        grid.covered[off] = bool(covered)
    if n > 0:
        return int(ts_sorted[-1]), Decimal(price_strings[-1])
    return prev_last_ts, prev_last_price


def hourly_rv_from_grid(grid: MinuteGrid, hour_start_ms: int) -> IntervalRv:
    """Compute ``RV(hour_start, hour_start + 1h]`` from the segment minute grid."""
    i0 = grid.minute_index(hour_start_ms)
    if i0 < 0 or i0 + GRID_STEPS >= grid.n_minutes:
        return IntervalRv(0.0, 0, False, "boundary_outside_segment")
    for k in range(GRID_STEPS + 1):
        if not bool(grid.price_known[i0 + k]):
            return IntervalRv(0.0, 0, False, "no_price_at_boundary")
    rv = 0.0
    for k in range(1, GRID_STEPS + 1):
        g_k = grid.price[i0 + k]
        g_prev = grid.price[i0 + k - 1]
        if g_k is None or g_prev is None or not (g_k > 0) or not (g_prev > 0):
            return IntervalRv(0.0, 0, False, "non_positive_price")
        r = _decimal_ratio_log(g_k, g_prev)
        if not math.isfinite(r):
            return IntervalRv(0.0, 0, False, "non_finite_return")
        rv += r * r
    covered = int(np.count_nonzero(grid.covered[i0 + 1 : i0 + 1 + GRID_STEPS]))
    if not math.isfinite(rv):
        return IntervalRv(0.0, covered, False, "non_finite_rv")
    valid = covered >= COVERAGE_MIN_COVERED_MINUTES
    return IntervalRv(rv, covered, valid, "" if valid else "insufficient_coverage")


# ---------------------------------------------------------------------------
# Per-segment hourly RV series + origin assembly
# ---------------------------------------------------------------------------


@dataclass
class HourlySeries:
    """The per-hour RV series for one accessible segment (indexed by hour offset)."""

    seg_id: str
    seg_start_ms: int  # 00:00 of the segment's first date (hour-aligned)
    n_hours: int
    rv: npt.NDArray[np.float64]
    valid: npt.NDArray[np.bool_]
    covered: npt.NDArray[np.int64]

    def hour_index(self, hour_start_ms: int) -> int:
        if (hour_start_ms - self.seg_start_ms) % HOUR_MS != 0:
            raise Cf1ContractError("hour_start not hour-aligned to the segment")
        return (hour_start_ms - self.seg_start_ms) // HOUR_MS


def build_hourly_series(grid: MinuteGrid) -> HourlySeries:
    """Compute the hourly RV series over an entire segment from its minute grid.

    Hour ``j`` is the interval ``(seg_start + j*3600000, seg_start + (j+1)*3600000]``.
    Only complete hours whose 61 minute boundaries lie inside the grid are produced.
    """
    n_hours = (grid.n_minutes - 1) // GRID_STEPS
    rv = np.zeros(n_hours, dtype=np.float64)
    valid = np.zeros(n_hours, dtype=np.bool_)
    covered = np.zeros(n_hours, dtype=np.int64)
    for j in range(n_hours):
        res = hourly_rv_from_grid(grid, grid.seg_start_ms + j * HOUR_MS)
        rv[j] = res.rv
        valid[j] = res.valid
        covered[j] = res.covered_minutes
    return HourlySeries(
        seg_id=grid.seg_id,
        seg_start_ms=grid.seg_start_ms,
        n_hours=n_hours,
        rv=rv,
        valid=valid,
        covered=covered,
    )


@dataclass(frozen=True)
class OriginTarget:
    """The assembled RV target + HAR lookbacks for one hourly origin."""

    origin_ms: int
    valid: bool
    invalid_reason: str
    covered_minutes: int
    rv_target: float
    log_rv_target: float
    rv_h: float
    rv_d: float
    rv_w: float
    target_end_ms: int


def assemble_origin_target(series: HourlySeries, origin_ms: int) -> OriginTarget:
    """Assemble the causal RV target and HAR lookbacks for an hourly origin.

    Returns ``valid=False`` with a machine-readable reason if: the target endpoint
    lies outside execution access; the 168h weekly lookback would leave the segment
    (a forbidden carry-forward / stitch); the target hour or any HAR hourly interval
    is not a valid completed interval; or the target endpoint date is forbidden.
    """
    empty = 0.0
    target_end_ms = origin_ms + HORIZON_MS
    # Right-endpoint-inside-execution-access rule (section 8/21). The endpoint's own
    # UTC date must be openable; a target ending at 00:00 of a forbidden date (e.g.
    # 2024-11-01 for the 2024-10-31T23:00 origin) is invalid.
    end_date = utc_date_for_timestamp_ms(target_end_ms)
    # The endpoint instant belongs to the interval ENDING at it; its date is that of
    # the instant, but a right endpoint at exactly 00:00 of day D still requires day
    # D to be openable because P_at(endpoint) uses ts <= endpoint.
    if not is_allowed_date(end_date):
        return OriginTarget(
            origin_ms,
            False,
            "target_crosses_inaccessible_boundary",
            0,
            empty,
            empty,
            empty,
            empty,
            empty,
            target_end_ms,
        )
    if segment_for_timestamp_ms(origin_ms) != series.seg_id:
        return OriginTarget(
            origin_ms,
            False,
            "origin_outside_segment",
            0,
            empty,
            empty,
            empty,
            empty,
            empty,
            target_end_ms,
        )
    jt = series.hour_index(origin_ms)  # hour starting at t == target hour (t, t+1h]
    # Weekly lookback must lie within the segment: hours [jt-168 .. jt-1] and target
    # hour jt all present.
    if jt - HAR_WEEKLY_HOURS < 0 or jt >= series.n_hours:
        return OriginTarget(
            origin_ms,
            False,
            "har_unavailable",
            0,
            empty,
            empty,
            empty,
            empty,
            empty,
            target_end_ms,
        )
    target = series.valid[jt]
    if not bool(target):
        return OriginTarget(
            origin_ms,
            False,
            "insufficient_target_coverage",
            int(series.covered[jt]),
            empty,
            empty,
            empty,
            empty,
            empty,
            target_end_ms,
        )
    # HAR hourly intervals ending at t: hour jt-1 (RV_h), jt-24..jt-1 (daily),
    # jt-168..jt-1 (weekly). All must be valid completed intervals.
    weekly_slice = series.valid[jt - HAR_WEEKLY_HOURS : jt]
    if not bool(np.all(weekly_slice)):
        return OriginTarget(
            origin_ms,
            False,
            "har_coverage_failure",
            int(series.covered[jt]),
            empty,
            empty,
            empty,
            empty,
            empty,
            target_end_ms,
        )
    rv_target = float(series.rv[jt])
    rv_h = float(series.rv[jt - 1])
    rv_d = float(np.mean(series.rv[jt - HAR_DAILY_HOURS : jt]))
    rv_w = float(np.mean(series.rv[jt - HAR_WEEKLY_HOURS : jt]))
    log_rv = math.log(rv_target + TARGET_EPSILON)
    if not (
        math.isfinite(rv_target)
        and math.isfinite(rv_h)
        and math.isfinite(rv_d)
        and math.isfinite(rv_w)
        and math.isfinite(log_rv)
    ):
        return OriginTarget(
            origin_ms,
            False,
            "non_finite_target",
            int(series.covered[jt]),
            empty,
            empty,
            empty,
            empty,
            empty,
            target_end_ms,
        )
    return OriginTarget(
        origin_ms=origin_ms,
        valid=True,
        invalid_reason="",
        covered_minutes=int(series.covered[jt]),
        rv_target=rv_target,
        log_rv_target=log_rv,
        rv_h=rv_h,
        rv_d=rv_d,
        rv_w=rv_w,
        target_end_ms=target_end_ms,
    )


def candidate_origin_hours(series: HourlySeries) -> list[int]:
    """Return the hour-aligned origin timestamps to consider for a segment.

    An origin is a top-of-UTC-hour instant whose UTC date is openable. Validity of
    each candidate is decided by :func:`assemble_origin_target`.
    """
    out: list[int] = []
    for j in range(series.n_hours):
        origin_ms = series.seg_start_ms + j * HOUR_MS
        if is_allowed_date(utc_date_for_timestamp_ms(origin_ms)):
            out.append(origin_ms)
    return out


# ---------------------------------------------------------------------------
# Deterministic synthetic timestamp-boundary proof (no market data, no reserve)
# ---------------------------------------------------------------------------


def _proof_trades() -> tuple[npt.NDArray[np.int64], list[Decimal]]:
    """Build the frozen synthetic aggTrade set for the boundary proof.

    Prices: 100 at 09:59:59.999; 110 at exactly 10:00:00.000 (a boundary); stable
    afterwards; another change (120) exactly at 11:00:00.000. Two trades share the
    exact instant 10:00:00.000 (row_index 4 then 5) to exercise the greatest-row_index
    tie rule. Timestamps are relative to a synthetic 2024-06-01 base so all instants
    are hour-aligned to the UTC grid.
    """
    base = utc_date_start_ms("2024-06-01")
    h09 = base + 9 * HOUR_MS
    h10 = base + 10 * HOUR_MS
    h11 = base + 11 * HOUR_MS
    # (ts, row_index, price). Sorted canonically by (ts, row_index).
    rows: list[tuple[int, int, Decimal]] = [
        (h09 - 3600_000, 0, Decimal("100")),  # 08:00:00.000 seed for carry-forward
        (h09 - 1, 1, Decimal("100")),  # 08:59:59.999
        (h09, 2, Decimal("100")),  # 09:00:00.000 exactly (left endpoint seed)
        (h10 - 1, 3, Decimal("100")),  # 09:59:59.999
        (h10, 4, Decimal("105")),  # 10:00:00.000 exactly (lower row_index)
        (h10, 5, Decimal("110")),  # 10:00:00.000 exactly (greatest row_index wins)
        (h10 + 30_000, 6, Decimal("110")),  # 10:00:30.000 stable
        (h11 - 1, 7, Decimal("110")),  # 10:59:59.999
        (h11, 8, Decimal("120")),  # 11:00:00.000 exactly
        (h11 + 30_000, 9, Decimal("120")),  # 11:00:30.000 stable
    ]
    ts = np.array([r[0] for r in rows], dtype=np.int64)
    prices = [r[2] for r in rows]
    return ts, prices


def run_synthetic_timestamp_boundary_proof() -> dict[str, object]:
    """Run the deterministic synthetic timestamp-boundary proof (contract section 33).

    Opens no market-data or feature file and touches no reserve; all rows are
    hard-coded synthetic prices. Returns a deterministic result dict whose
    ``timestamp_boundary_proof_passed`` is True only if every required example passes.
    """
    ts, prices = _proof_trades()
    base = utc_date_start_ms("2024-06-01")
    h09, h10, h11 = base + 9 * HOUR_MS, base + 10 * HOUR_MS, base + 11 * HOUR_MS
    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    # Greatest-row_index tie at 10:00:00.000 -> 110 (not 105).
    idx = p_at_index(ts, h10)
    tie_ok = prices[idx] == Decimal("110")
    record("same_timestamp_greatest_row_index_tie", tie_ok, f"P_at(10:00)={prices[idx]}")

    # (09:00, 10:00] captures the move into 110 (r_60 = ln(110/100) != 0).
    rv_0910 = compute_rv_over_trades(ts, prices, h09, h10)
    g59 = prices[p_at_index(ts, h10 - MINUTE_MS)]
    g60 = prices[p_at_index(ts, h10)]
    captures = rv_0910.rv > 0.0 and g60 == Decimal("110") and g59 == Decimal("100")
    record(
        "interval_0900_1000_captures_boundary_jump",
        captures,
        f"RV={rv_0910.rv:.8e} G59={g59} G60={g60}",
    )

    # RV_h(10:00) = RV(09:00, 10:00] may include the exactly-10:00 trade (terminal).
    rvh_ok = prices[p_at_index(ts, h10)] == Decimal("110") and rv_0910.rv > 0.0
    record("rv_h_1000_may_include_exact_1000_trade", rvh_ok, "terminal P_at(10:00)=110")

    # (10:00, 11:00] starts from 110 (G_0 = P_at(10:00) = 110) and does not re-count.
    g0_1011 = prices[p_at_index(ts, h10)]
    starts_from_110 = g0_1011 == Decimal("110")
    record(
        "interval_1000_1100_starts_from_110_no_recount",
        starts_from_110,
        f"G0=P_at(10:00)={g0_1011}",
    )

    # RV_target(10:00) = RV(10:00, 11:00] excludes the pre-10:00 -> 10:00 jump: its
    # first return is ln(P_at(10:01)/P_at(10:00)) = ln(110/110) = 0, so the 100->110
    # jump is absent; the only variance is the 110->120 jump at 11:00.
    rv_1011 = compute_rv_over_trades(ts, prices, h10, h11)
    first_ret = _decimal_ratio_log(
        prices[p_at_index(ts, h10 + MINUTE_MS)], prices[p_at_index(ts, h10)]
    )
    excludes_origin_jump = abs(first_ret) < 1e-15 and rv_1011.rv > 0.0
    record(
        "rv_target_1000_excludes_origin_time_jump",
        excludes_origin_jump,
        f"first_return={first_ret:.3e} RV={rv_1011.rv:.8e}",
    )

    # A trade exactly at 11:00 IS included in target (10:00, 11:00] (terminal G_60=120).
    g60_1011 = prices[p_at_index(ts, h11)]
    includes_1100 = g60_1011 == Decimal("120")
    record(
        "trade_at_1100_included_in_target_1000_1100", includes_1100, f"G60=P_at(11:00)={g60_1011}"
    )

    # Feature snapshot at 10:00 may include the 10:00 row (feature ts <= t).
    snap_ok = p_at_index(ts, h10) >= 0 and ts[p_at_index(ts, h10)] == h10
    record("feature_snapshot_1000_may_include_1000_row", snap_ok, "last ts<=t is exactly t")

    # Boundary trade assigned exactly once (to the interval ENDING at its timestamp).
    # The 10:00 trade is the terminal of (09:00,10:00] and the origin of (10:00,11:00];
    # it contributes to r_60 of the first interval and is not re-counted as a return in
    # the second (first return of the second interval is 0).
    once_ok = captures and excludes_origin_jump
    record("boundary_trade_assigned_exactly_once", once_ok, "terminal-only assignment")

    # Strict '<' / [a,b) variant would OMIT the boundary jump: a left-limit terminal
    # price P_minus(10:00) = last trade with ts < 10:00 = 100, so RV[09:00,10:00) would
    # miss the 100->110 jump. Prove the correct (<=) operator differs from the wrong (<).
    p_minus_1000_idx = int(np.searchsorted(ts, h10, side="left")) - 1
    p_minus_1000 = prices[p_minus_1000_idx]
    strict_lt_omits = p_minus_1000 == Decimal("100") and prices[p_at_index(ts, h10)] == Decimal(
        "110"
    )
    record(
        "strict_lt_or_half_open_variant_fails_validation",
        strict_lt_omits,
        f"P_minus(10:00)={p_minus_1000} != P_at(10:00)=110 (wrong operator omits jump)",
    )

    # Coverage predicate (tau_{k-1} < ts <= tau_k): a trade exactly at tau_k belongs to
    # the current minute, exactly at tau_{k-1} to the preceding minute.
    right = int(np.searchsorted(ts, h10, side="right"))
    left = int(np.searchsorted(ts, h10 - MINUTE_MS, side="right"))
    cov_ok = (right - left) > 0  # (09:59, 10:00] is covered (contains the 10:00 trade)
    record("covered_minute_predicate_right_closed", cov_ok, "trade at tau_k in current minute")

    # Final October origin rejection without opening November data.
    origin_2200 = utc_date_start_ms("2024-10-31") + 22 * HOUR_MS
    origin_2300 = utc_date_start_ms("2024-10-31") + 23 * HOUR_MS
    end_2200 = utc_date_for_timestamp_ms(origin_2200 + HORIZON_MS)  # 2024-10-31T23:00
    end_2300 = utc_date_for_timestamp_ms(origin_2300 + HORIZON_MS)  # 2024-11-01T00:00
    oct_ok = is_allowed_date(end_2200) and not is_allowed_date(end_2300)
    record(
        "oct31_2200_valid_2300_invalid",
        oct_ok,
        f"end(22:00)->{end_2200} allowed; end(23:00)->{end_2300} forbidden",
    )

    # No query plan / partition open includes November 1 or October 1.
    nov1_rejected = _raises_forbidden("2024-11-01")
    oct1_rejected = _raises_forbidden("2024-10-01")
    record(
        "november_1_partition_rejected_before_open",
        nov1_rejected,
        "assert_partition_allowed raises",
    )
    record(
        "october_1_partition_rejected_before_open", oct1_rejected, "assert_partition_allowed raises"
    )

    # No broad glob can include forbidden partitions: the allowlist has exactly 244
    # dates and contains none of the forbidden ranges.
    allowed = allowed_utc_dates()
    forbidden_touch = any(
        d in _ALLOWED_DATE_SET
        for reason, lo, hi in forbidden_date_ranges()
        for d in _date_range_inclusive(lo, hi)
    )
    allowlist_ok = len(allowed) == EXPECTED_ALLOWED_DATE_COUNT and not forbidden_touch
    record(
        "allowlist_excludes_all_forbidden_partitions",
        allowlist_ok,
        f"allowed={len(allowed)} forbidden_overlap={forbidden_touch}",
    )

    passed = all(bool(c["passed"]) for c in checks)
    return {
        "proof_family": "cf1_timestamp_boundary_proof_v001",
        "phase_id": PHASE_ID,
        "symbol": SYMBOL,
        "base_main_commit_sha": BASE_MAIN_COMMIT_SHA,
        "phase_4bn_ay_merge_commit_sha": PHASE_4BN_AY_MERGE_COMMIT_SHA,
        "phase_4bn_ay_contract_tip_sha": PHASE_4BN_AY_CONTRACT_TIP_SHA,
        "market_data_opened": False,
        "feature_data_opened": False,
        "reserve_touched": False,
        "n_checks": len(checks),
        "checks": checks,
        "timestamp_boundary_proof_passed": bool(passed),
    }


def _raises_forbidden(utc_date: str) -> bool:
    try:
        assert_partition_allowed(utc_date)
    except Cf1ForbiddenPartitionError:
        return True
    return False


__all__ = [
    "ACCESSIBLE_SEGMENTS",
    "ACCESS_END_DATE",
    "ACCESS_START_DATE",
    "AUGMENTED_N_PARAMS",
    "BASELINE_N_PARAMS",
    "BASE_MAIN_COMMIT_SHA",
    "BLOCKS",
    "BLOCK_IDS",
    "BOOTSTRAP_LOWER_QUANTILE",
    "BOOTSTRAP_REPLICATES",
    "BOOTSTRAP_SEED",
    "CONDITION_NUMBER_MAX",
    "CONTRACT_VERSION",
    "COVERAGE_MIN_COVERED_MINUTES",
    "COVERAGE_TOTAL_MINUTES",
    "Cf1ContractError",
    "Cf1ForbiddenPartitionError",
    "EMBARGO_MS",
    "EXCLUDED_EMBARGO_DATE",
    "EXPECTED_ALLOWED_DATE_COUNT",
    "FEATURE_COLUMNS",
    "GRID_STEPS",
    "HAR_DAILY_HOURS",
    "HAR_WEEKLY_HOURS",
    "HORIZON_MS",
    "HOUR_MS",
    "HourlySeries",
    "IntervalRv",
    "MINUTE_MS",
    "MIN_BLOCK_VALID_ORIGINS",
    "MIN_TRAIN_ORIGINS",
    "MinuteGrid",
    "N_BLOCKS",
    "OriginTarget",
    "PHASE_4BN_AY_CONTRACT_TIP_SHA",
    "PHASE_4BN_AY_MERGE_COMMIT_SHA",
    "PHASE_ID",
    "PURGE_MS",
    "STANDARDIZATION_EPSILON",
    "SYMBOL",
    "TARGET_DATASET_FAMILY",
    "TARGET_EPSILON",
    "allowed_utc_dates",
    "assemble_origin_target",
    "assert_partition_allowed",
    "assert_partition_paths_allowed",
    "block_for_origin_ms",
    "build_hourly_series",
    "candidate_origin_hours",
    "compute_rv_over_trades",
    "fill_minute_grid_day",
    "fill_minute_grid_from_trades",
    "forbidden_date_ranges",
    "hourly_rv_from_grid",
    "is_allowed_date",
    "is_hour_aligned",
    "new_minute_grid",
    "p_at_index",
    "run_synthetic_timestamp_boundary_proof",
    "segment_boundaries",
    "segment_for_timestamp_ms",
    "utc_date_for_timestamp_ms",
    "utc_date_start_ms",
]
