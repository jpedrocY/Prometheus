"""Signal-funnel diagnostic (research-only; no defaults changed).

Walks pre-loaded historical bars and tallies, per symbol, how many
bars survive each strategy filter step. The diagnostic does NOT:

    - mutate any threshold,
    - change any fill/sizing behavior,
    - call any network,
    - alter engine results.

It replays the same primitives used by the production strategy
(``evaluate_1h_bias``, ``detect_setup``, trigger conditions, stop
formula, sizing pipeline) but attributes rejections to the first
short-circuit — producing a funnel report useful for understanding
"0-trade" outcomes on short data windows without tuning parameters.

Funnel stages (in order; each bar attributed to the FIRST
short-circuit reason):

    warmup  (insufficient 1h or 15m history)
    -> decision bar evaluated
       bias: LONG | SHORT | NEUTRAL
       if NEUTRAL: rejected_neutral_bias (done)
       else:
         setup: VALID | INVALID
         if INVALID: rejected_no_valid_setup (done)
         else:
           # directional trigger conditions
           close-broke-level?
           if not: rejected_close_did_not_break_level (done)
           else:
             true_range >= ATR?
             if not: rejected_true_range_too_small (done)
             else:
               close in top/bottom 25%?
               if not: rejected_close_location_failed (done)
               else:
                 normalized ATR in [0.20%, 2.00%]?
                 if not: rejected_normalized_atr_regime_failed (done)
                 else:
                   stop-distance filter pass?
                   if not: rejected_stop_distance_filter_failed (done)
                   else:
                     sizing approves?
                     if not: rejected_sizing_failed (+ sub-reason) (done)
                     else:
                       entry_intents_produced += 1
                       next bar exists?
                       if not: end_of_data_no_fill += 1 (done)
                       else: trades_filled += 1
"""

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass, field

from prometheus.core.exchange_info import SymbolInfo
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.strategy.indicators import true_range
from prometheus.strategy.types import Direction, TrendBias
from prometheus.strategy.v1_breakout.bias import (
    EMA_FAST,  # noqa: F401 — re-exported for backwards-compatible imports
    EMA_SLOW,  # noqa: F401 — re-exported for backwards-compatible imports
    SLOPE_LOOKBACK,
)
from prometheus.strategy.v1_breakout.setup import SETUP_SIZE, detect_setup  # noqa: F401
from prometheus.strategy.v1_breakout.stop import (
    compute_initial_stop,
    passes_stop_distance_filter,
)
from prometheus.strategy.v1_breakout.trigger import (
    ATR_REGIME_MAX,
    ATR_REGIME_MIN,
    BREAKOUT_BUFFER_ATR_MULT,
    CLOSE_LOCATION_RATIO,
    TRUE_RANGE_ATR_MULT,  # noqa: F401 — re-exported for backwards-compatible imports
)
from prometheus.strategy.v1_breakout.variant_config import V1BreakoutConfig

from .config import BacktestConfig
from .sizing import RejectionReason, compute_size

ATR_PERIOD = 20

# Baseline warmup constants retained for backwards-compatible imports.
# Per-variant runs compute warmup thresholds from the active config.
MIN_1H_BARS_FOR_BIAS = EMA_SLOW + SLOPE_LOOKBACK
MIN_15M_BARS_FOR_SIGNAL = ATR_PERIOD + 1 + SETUP_SIZE + 1


class _IncrementalIndicators:
    """O(1)-per-bar Wilder ATR + EMA state, matching the StrategySession pattern.

    Maintained inline in ``run_signal_funnel`` so the diagnostic runs
    in O(bars) rather than O(bars * window). Seeding conventions
    match the standalone ``wilder_atr`` / ``ema`` functions exactly.

    ``ema_fast_period`` / ``ema_slow_period`` default to the locked
    baseline (50/200) and are overridden per-variant.
    """

    def __init__(self, *, ema_fast_period: int = EMA_FAST, ema_slow_period: int = EMA_SLOW) -> None:
        self.ema_fast_period = ema_fast_period
        self.ema_slow_period = ema_slow_period
        # 15m ATR
        self.tr15_warmup: list[float] = []
        self.atr15_latest: float = float("nan")
        self.atr15_before: float = float("nan")
        self.bars15: int = 0
        self.prev15_close: float | None = None
        # 1h ATR
        self.tr1h_warmup: list[float] = []
        self.atr1h_latest: float = float("nan")
        self.bars1h: int = 0
        self.prev1h_close: float | None = None
        # 1h EMA fast + slow + slope ring
        self.ema_fast_warmup: list[float] = []
        self.ema_slow_warmup: list[float] = []
        self.ema_fast_latest: float = float("nan")
        self.ema_slow_latest: float = float("nan")
        self.ema_fast_history: deque[float] = deque(maxlen=SLOPE_LOOKBACK + 1)

    def ingest_15m(self, bar: NormalizedKline) -> None:
        tr = true_range(bar.high, bar.low, self.prev15_close)
        self.prev15_close = bar.close
        self.atr15_before = self.atr15_latest
        self.bars15 += 1
        if self.bars15 <= ATR_PERIOD:
            self.tr15_warmup.append(tr)
        elif self.bars15 == ATR_PERIOD + 1:
            self.atr15_latest = sum(self.tr15_warmup[:ATR_PERIOD]) / ATR_PERIOD
            self.tr15_warmup = []
        else:
            self.atr15_latest = ((ATR_PERIOD - 1) * self.atr15_latest + tr) / ATR_PERIOD

    def ingest_1h(self, bar: NormalizedKline) -> None:
        tr = true_range(bar.high, bar.low, self.prev1h_close)
        self.prev1h_close = bar.close
        self.bars1h += 1
        if self.bars1h <= ATR_PERIOD:
            self.tr1h_warmup.append(tr)
        elif self.bars1h == ATR_PERIOD + 1:
            self.atr1h_latest = sum(self.tr1h_warmup[:ATR_PERIOD]) / ATR_PERIOD
            self.tr1h_warmup = []
        else:
            self.atr1h_latest = ((ATR_PERIOD - 1) * self.atr1h_latest + tr) / ATR_PERIOD
        # EMA fast
        close = bar.close
        ema_fast = self.ema_fast_period
        ema_slow = self.ema_slow_period
        if self.ema_fast_latest != self.ema_fast_latest:  # NaN
            self.ema_fast_warmup.append(close)
            if len(self.ema_fast_warmup) == ema_fast:
                self.ema_fast_latest = sum(self.ema_fast_warmup) / ema_fast
                self.ema_fast_warmup = []
        else:
            a = 2.0 / (ema_fast + 1.0)
            self.ema_fast_latest = a * close + (1.0 - a) * self.ema_fast_latest
        if self.ema_fast_latest == self.ema_fast_latest:  # not NaN
            self.ema_fast_history.append(self.ema_fast_latest)
        # EMA slow
        if self.ema_slow_latest != self.ema_slow_latest:
            self.ema_slow_warmup.append(close)
            if len(self.ema_slow_warmup) == ema_slow:
                self.ema_slow_latest = sum(self.ema_slow_warmup) / ema_slow
                self.ema_slow_warmup = []
        else:
            a = 2.0 / (ema_slow + 1.0)
            self.ema_slow_latest = a * close + (1.0 - a) * self.ema_slow_latest

    def current_bias(self, latest_1h_close: float) -> TrendBias:
        if self.ema_fast_latest != self.ema_fast_latest:
            return TrendBias.NEUTRAL
        if self.ema_slow_latest != self.ema_slow_latest:
            return TrendBias.NEUTRAL
        if len(self.ema_fast_history) < SLOPE_LOOKBACK + 1:
            return TrendBias.NEUTRAL
        fast_now = self.ema_fast_latest
        slow_now = self.ema_slow_latest
        fast_then = self.ema_fast_history[0]
        long_ok = (fast_now > slow_now) and (latest_1h_close > fast_now) and (fast_now > fast_then)
        short_ok = (fast_now < slow_now) and (latest_1h_close < fast_now) and (fast_now < fast_then)
        if long_ok and not short_ok:
            return TrendBias.LONG
        if short_ok and not long_ok:
            return TrendBias.SHORT
        return TrendBias.NEUTRAL


@dataclass
class SignalFunnelCounts:
    """Per-symbol funnel breakdown.

    Each post-warmup decision bar contributes to exactly ONE rejection
    bucket (the first short-circuit). Bias counts are orthogonal (every
    decision bar contributes to exactly one bias bucket too).
    """

    symbol: Symbol

    # Volume
    total_15m_bars_loaded: int = 0
    total_1h_bars_loaded: int = 0
    warmup_15m_bars_excluded: int = 0
    warmup_1h_bars_excluded: int = 0
    decision_bars_evaluated: int = 0

    # Bias (orthogonal to rejections)
    bias_long_count: int = 0
    bias_short_count: int = 0
    bias_neutral_count: int = 0

    # Setup
    valid_setup_windows_detected: int = 0

    # Candidates (passed bias + setup + close-broke-level; still subject
    # to TR/location/regime/stop-distance/sizing)
    long_breakout_candidates: int = 0
    short_breakout_candidates: int = 0

    # Rejection buckets (each decision bar -> at most one)
    rejected_neutral_bias: int = 0
    rejected_no_valid_setup: int = 0
    rejected_close_did_not_break_level: int = 0
    rejected_true_range_too_small: int = 0
    rejected_close_location_failed: int = 0
    rejected_normalized_atr_regime_failed: int = 0
    rejected_stop_distance_filter_failed: int = 0
    rejected_sizing_failed: int = 0
    end_of_data_no_fill: int = 0

    # Sizing sub-reasons
    sizing_below_minqty: int = 0
    sizing_below_min_notional: int = 0
    sizing_missing_filters: int = 0

    # Flow endpoints
    entry_intents_produced: int = 0
    trades_filled: int = 0
    trades_closed: int = 0

    # Warnings / context
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """Human-readable one-symbol summary block."""
        lines = [
            f"symbol={self.symbol.value}",
            f"  bars loaded:          15m={self.total_15m_bars_loaded}  "
            f"1h={self.total_1h_bars_loaded}",
            f"  warmup excluded:      15m={self.warmup_15m_bars_excluded}  "
            f"1h={self.warmup_1h_bars_excluded}",
            f"  decision bars:        {self.decision_bars_evaluated}",
            f"  bias:                 long={self.bias_long_count}  "
            f"short={self.bias_short_count}  neutral={self.bias_neutral_count}",
            f"  setups valid:         {self.valid_setup_windows_detected}",
            f"  candidates:           long={self.long_breakout_candidates}  "
            f"short={self.short_breakout_candidates}",
            "  rejections:",
            f"    neutral bias:       {self.rejected_neutral_bias}",
            f"    no valid setup:     {self.rejected_no_valid_setup}",
            f"    no close-break:     {self.rejected_close_did_not_break_level}",
            f"    TR < ATR:           {self.rejected_true_range_too_small}",
            f"    close location:     {self.rejected_close_location_failed}",
            f"    ATR regime:         {self.rejected_normalized_atr_regime_failed}",
            f"    stop-dist filter:   {self.rejected_stop_distance_filter_failed}",
            f"    sizing failed:      {self.rejected_sizing_failed}  "
            f"(minQty={self.sizing_below_minqty}  minNotional={self.sizing_below_min_notional}  "
            f"missing_filters={self.sizing_missing_filters})",
            f"    end-of-data:        {self.end_of_data_no_fill}",
            f"  entry intents:        {self.entry_intents_produced}",
            f"  trades filled:        {self.trades_filled}",
            f"  trades closed:        {self.trades_closed}",
        ]
        return "\n".join(lines)


def _passes_close_location(bar: NormalizedKline, direction: Direction) -> bool:
    span = bar.high - bar.low
    if span <= 0:
        return False
    location = (bar.close - bar.low) / span
    if direction == Direction.LONG:
        return location >= CLOSE_LOCATION_RATIO
    return location <= (1.0 - CLOSE_LOCATION_RATIO)


def run_signal_funnel(
    *,
    symbol: Symbol,
    klines_15m: Sequence[NormalizedKline],
    klines_1h: Sequence[NormalizedKline],
    symbol_info: SymbolInfo,
    config: BacktestConfig,
    strategy_config: V1BreakoutConfig | None = None,
) -> SignalFunnelCounts:
    """Walk the 15m series and attribute each decision bar to a funnel bucket.

    ``symbol_info`` is needed to exercise the sizing pipeline. ``config``
    supplies sizing parameters (equity, risk_fraction, etc.).

    ``strategy_config`` supplies the variant overrides (setup_size,
    expansion_atr_mult, ema_fast, ema_slow, break_even_r). Defaults to
    the locked baseline, which reproduces the Phase 2e funnel shape.

    This function does NOT alter any strategy or engine state. It is
    purely observational.
    """
    sc = strategy_config if strategy_config is not None else V1BreakoutConfig()
    setup_size = sc.setup_size
    expansion_atr_mult = sc.expansion_atr_mult
    min_1h_bars_for_bias = sc.ema_slow + SLOPE_LOOKBACK
    min_15m_bars_for_signal = ATR_PERIOD + 1 + setup_size + 1

    counts = SignalFunnelCounts(symbol=symbol)
    counts.total_15m_bars_loaded = len(klines_15m)
    counts.total_1h_bars_loaded = len(klines_1h)

    if not klines_15m:
        counts.warnings.append("no 15m bars loaded")
        return counts
    if not klines_1h:
        counts.warnings.append("no 1h bars loaded")
        return counts

    # Incremental indicator state (O(1) per-bar updates).
    ind = _IncrementalIndicators(ema_fast_period=sc.ema_fast, ema_slow_period=sc.ema_slow)

    # 1h window is fed as bars complete; we track a counter (not a
    # growing list) for warmup gating. Latest 1h close is needed for
    # the ATR regime filter; we cache it as a scalar.
    bar_1h_idx = 0
    total_1h = len(klines_1h)
    fed_1h_count = 0
    latest_1h_close_cache: float = float("nan")

    # 15m bookkeeping — small ring for setup + TR lookup:
    # setup_size bars (prior) + 1 breakout + 1 slot for TR prev_close = setup_size + 2.
    recent15: deque[NormalizedKline] = deque(maxlen=setup_size + 2)
    fed_15m_count = 0
    total_15m = len(klines_15m)

    for idx_15m, bar_15m in enumerate(klines_15m):
        t_now_ms = bar_15m.close_time + 1
        while bar_1h_idx < total_1h:
            cand = klines_1h[bar_1h_idx]
            if cand.close_time < t_now_ms:
                ind.ingest_1h(cand)
                latest_1h_close_cache = cand.close
                fed_1h_count += 1
                bar_1h_idx += 1
            else:
                break
        ind.ingest_15m(bar_15m)
        recent15.append(bar_15m)
        fed_15m_count += 1

        # Warmup check.
        if fed_1h_count < min_1h_bars_for_bias or fed_15m_count < min_15m_bars_for_signal:
            if fed_1h_count < min_1h_bars_for_bias:
                counts.warmup_1h_bars_excluded += 1
            if fed_15m_count < min_15m_bars_for_signal:
                counts.warmup_15m_bars_excluded += 1
            continue

        counts.decision_bars_evaluated += 1

        # ---- Bias (cached) ----
        bias = ind.current_bias(latest_1h_close_cache)
        if bias == TrendBias.LONG:
            counts.bias_long_count += 1
        elif bias == TrendBias.SHORT:
            counts.bias_short_count += 1
        else:
            counts.bias_neutral_count += 1
            counts.rejected_neutral_bias += 1
            continue

        # ---- Setup (uses ATR value as of the bar before the current one) ----
        atr_prior_15m = ind.atr15_before
        if atr_prior_15m != atr_prior_15m:  # NaN
            counts.rejected_no_valid_setup += 1
            continue
        # prior = the setup_size bars immediately before the current bar.
        # recent15 has maxlen = setup_size + 2.
        if len(recent15) < setup_size + 1:
            counts.rejected_no_valid_setup += 1
            continue
        prior_bars = list(recent15)[-(setup_size + 1) : -1]
        setup = detect_setup(prior_bars, atr_prior_15m, setup_size=setup_size)
        if setup is None:
            counts.rejected_no_valid_setup += 1
            continue
        counts.valid_setup_windows_detected += 1

        # ---- Directional close-broke-level ----
        atr_15m_now = ind.atr15_latest
        atr_1h_now = ind.atr1h_latest
        if atr_15m_now != atr_15m_now or atr_1h_now != atr_1h_now:
            counts.rejected_normalized_atr_regime_failed += 1
            continue

        direction: Direction | None = None
        if bias == TrendBias.LONG:
            trigger_level = setup.setup_high + BREAKOUT_BUFFER_ATR_MULT * atr_15m_now
            if bar_15m.close > trigger_level:
                direction = Direction.LONG
                counts.long_breakout_candidates += 1
        else:
            trigger_level = setup.setup_low - BREAKOUT_BUFFER_ATR_MULT * atr_15m_now
            if bar_15m.close < trigger_level:
                direction = Direction.SHORT
                counts.short_breakout_candidates += 1

        if direction is None:
            counts.rejected_close_did_not_break_level += 1
            continue

        # ---- True range (uses prior 15m close from the ring) ----
        prev_close = recent15[-2].close
        tr = true_range(bar_15m.high, bar_15m.low, prev_close)
        if tr < expansion_atr_mult * atr_15m_now:
            counts.rejected_true_range_too_small += 1
            continue

        # ---- Close location ----
        if not _passes_close_location(bar_15m, direction):
            counts.rejected_close_location_failed += 1
            continue

        # ---- Normalized ATR regime ----
        if latest_1h_close_cache <= 0 or atr_1h_now <= 0:
            counts.rejected_normalized_atr_regime_failed += 1
            continue
        normalized = atr_1h_now / latest_1h_close_cache
        if not (ATR_REGIME_MIN <= normalized <= ATR_REGIME_MAX):
            counts.rejected_normalized_atr_regime_failed += 1
            continue

        # ---- Stop-distance filter ----
        initial_stop = compute_initial_stop(direction, setup, bar_15m, atr_15m_now)
        reference_price = bar_15m.close
        stop_distance = abs(reference_price - initial_stop)
        if not passes_stop_distance_filter(stop_distance, atr_15m_now):
            counts.rejected_stop_distance_filter_failed += 1
            continue

        # ---- Sizing ----
        decision = compute_size(
            sizing_equity_usdt=config.sizing_equity_usdt,
            risk_fraction=config.risk_fraction,
            risk_usage_fraction=config.risk_usage_fraction,
            stop_distance=stop_distance,
            reference_price=reference_price,
            max_effective_leverage=config.max_effective_leverage,
            max_notional_internal_usdt=config.max_notional_internal_usdt,
            symbol_info=symbol_info,
        )
        if not decision.approved:
            counts.rejected_sizing_failed += 1
            if decision.rejection_reason == RejectionReason.BELOW_MINQTY:
                counts.sizing_below_minqty += 1
            elif decision.rejection_reason == RejectionReason.BELOW_MIN_NOTIONAL:
                counts.sizing_below_min_notional += 1
            elif decision.rejection_reason == RejectionReason.MISSING_FILTERS:
                counts.sizing_missing_filters += 1
            continue

        counts.entry_intents_produced += 1

        # Next-bar-exists check: O(1) using the current loop index.
        next_idx = idx_15m + 1
        next_target = bar_15m.open_time + 15 * 60 * 1000
        if next_idx < total_15m and klines_15m[next_idx].open_time == next_target:
            counts.trades_filled += 1
            counts.trades_closed += 1
        else:
            counts.end_of_data_no_fill += 1

    return counts
