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

from collections.abc import Sequence
from dataclasses import dataclass, field

from prometheus.core.exchange_info import SymbolInfo
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.strategy.indicators import true_range, wilder_atr
from prometheus.strategy.types import Direction, TrendBias
from prometheus.strategy.v1_breakout.bias import (
    EMA_SLOW,
    SLOPE_LOOKBACK,
    evaluate_1h_bias,
)
from prometheus.strategy.v1_breakout.setup import SETUP_SIZE, detect_setup
from prometheus.strategy.v1_breakout.stop import (
    compute_initial_stop,
    passes_stop_distance_filter,
)
from prometheus.strategy.v1_breakout.trigger import (
    ATR_REGIME_MAX,
    ATR_REGIME_MIN,
    BREAKOUT_BUFFER_ATR_MULT,
    CLOSE_LOCATION_RATIO,
    TRUE_RANGE_ATR_MULT,
)

from .config import BacktestConfig
from .sizing import RejectionReason, compute_size

ATR_PERIOD = 20

MIN_1H_BARS_FOR_BIAS = EMA_SLOW + SLOPE_LOOKBACK
MIN_15M_BARS_FOR_SIGNAL = ATR_PERIOD + 1 + SETUP_SIZE + 1


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


def _atr_at_tail(bars: Sequence[NormalizedKline]) -> float:
    """Return Wilder ATR(20) at the last bar, or NaN if warmup insufficient."""
    if len(bars) < ATR_PERIOD + 1:
        return float("nan")
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    return wilder_atr(highs, lows, closes, ATR_PERIOD)[-1]


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
) -> SignalFunnelCounts:
    """Walk the 15m series and attribute each decision bar to a funnel bucket.

    ``symbol_info`` is needed to exercise the sizing pipeline. ``config``
    supplies sizing parameters (equity, risk_fraction, etc.).

    This function does NOT alter any strategy or engine state. It is
    purely observational.
    """
    counts = SignalFunnelCounts(symbol=symbol)
    counts.total_15m_bars_loaded = len(klines_15m)
    counts.total_1h_bars_loaded = len(klines_1h)

    if not klines_15m:
        counts.warnings.append("no 15m bars loaded")
        return counts
    if not klines_1h:
        counts.warnings.append("no 1h bars loaded")
        return counts

    # 1h window is fed as bars complete; we maintain a growing prefix.
    # Simulation clock mirrors the engine: at each 15m bar close we
    # advance to t_now_ms = bar.close_time + 1 and absorb any 1h bar
    # whose close_time < t_now_ms.
    bar_1h_idx = 0
    total_1h = len(klines_1h)
    fed_1h: list[NormalizedKline] = []

    # 15m rolling window; we feed bars in order.
    fed_15m: list[NormalizedKline] = []

    for bar_15m in klines_15m:
        t_now_ms = bar_15m.close_time + 1
        while bar_1h_idx < total_1h:
            cand = klines_1h[bar_1h_idx]
            if cand.close_time < t_now_ms:
                fed_1h.append(cand)
                bar_1h_idx += 1
            else:
                break
        fed_15m.append(bar_15m)

        # Warmup check: need MIN_1H_BARS_FOR_BIAS 1h bars AND
        # MIN_15M_BARS_FOR_SIGNAL 15m bars (latter == len(fed_15m)).
        if len(fed_1h) < MIN_1H_BARS_FOR_BIAS or len(fed_15m) < MIN_15M_BARS_FOR_SIGNAL:
            if len(fed_1h) < MIN_1H_BARS_FOR_BIAS:
                counts.warmup_1h_bars_excluded += 1
            if len(fed_15m) < MIN_15M_BARS_FOR_SIGNAL:
                counts.warmup_15m_bars_excluded += 1
            continue

        # Decision bar
        counts.decision_bars_evaluated += 1

        # ---- Bias ----
        bias = evaluate_1h_bias(fed_1h)
        if bias == TrendBias.LONG:
            counts.bias_long_count += 1
        elif bias == TrendBias.SHORT:
            counts.bias_short_count += 1
        else:
            counts.bias_neutral_count += 1
            counts.rejected_neutral_bias += 1
            continue

        # ---- Setup ----
        prior_8 = fed_15m[-(SETUP_SIZE + 1) : -1]
        atr_prior_15m = _atr_at_tail(fed_15m[:-1])
        if atr_prior_15m != atr_prior_15m:  # NaN
            counts.rejected_no_valid_setup += 1
            continue
        setup = detect_setup(prior_8, atr_prior_15m)
        if setup is None:
            counts.rejected_no_valid_setup += 1
            continue
        counts.valid_setup_windows_detected += 1

        # ---- Directional close-broke-level ----
        atr_15m_now = _atr_at_tail(fed_15m)
        atr_1h_now = _atr_at_tail(fed_1h)
        if atr_15m_now != atr_15m_now or atr_1h_now != atr_1h_now:
            # Indicator warmup at boundary; attribute to sizing-adjacent
            # "regime" bucket conservatively.
            counts.rejected_normalized_atr_regime_failed += 1
            continue

        direction: Direction | None = None
        if bias == TrendBias.LONG:
            trigger_level = setup.setup_high + BREAKOUT_BUFFER_ATR_MULT * atr_15m_now
            if bar_15m.close > trigger_level:
                direction = Direction.LONG
                counts.long_breakout_candidates += 1
        else:  # SHORT
            trigger_level = setup.setup_low - BREAKOUT_BUFFER_ATR_MULT * atr_15m_now
            if bar_15m.close < trigger_level:
                direction = Direction.SHORT
                counts.short_breakout_candidates += 1

        if direction is None:
            counts.rejected_close_did_not_break_level += 1
            continue

        # ---- True range ----
        prev_close = fed_15m[-2].close
        tr = true_range(bar_15m.high, bar_15m.low, prev_close)
        if tr < TRUE_RANGE_ATR_MULT * atr_15m_now:
            counts.rejected_true_range_too_small += 1
            continue

        # ---- Close location ----
        if not _passes_close_location(bar_15m, direction):
            counts.rejected_close_location_failed += 1
            continue

        # ---- Normalized ATR regime (1h ATR / latest 1h close) ----
        latest_1h_close = fed_1h[-1].close
        if latest_1h_close <= 0 or atr_1h_now <= 0:
            counts.rejected_normalized_atr_regime_failed += 1
            continue
        normalized = atr_1h_now / latest_1h_close
        if not (ATR_REGIME_MIN <= normalized <= ATR_REGIME_MAX):
            counts.rejected_normalized_atr_regime_failed += 1
            continue

        # ---- Stop-distance filter (uses signal-bar close as reference) ----
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

        # All filters passed — strategy would emit an EntryIntent.
        counts.entry_intents_produced += 1

        # Determine whether the engine could fill on the next bar.
        # The engine uses next-bar-open fill; if this is the last 15m
        # bar in the window, the fill would be END_OF_DATA.
        # Use the simple index: if there is a next bar in the LOADED
        # klines_15m sequence whose open_time == bar_15m.open_time + 15m.
        next_target = bar_15m.open_time + 15 * 60 * 1000
        next_bar_exists = False
        # Inline lookup; O(n) worst case but acceptable for a one-pass
        # diagnostic on a one-month window.
        remaining_idx = klines_15m.index(bar_15m) + 1
        if remaining_idx < len(klines_15m) and klines_15m[remaining_idx].open_time == next_target:
            next_bar_exists = True
        if not next_bar_exists:
            counts.end_of_data_no_fill += 1
            continue

        counts.trades_filled += 1
        # The diagnostic treats "trade filled" as "trade closed" for
        # the purpose of top-line counts, since the backtest engine
        # will close every filled trade eventually (in-window exit or
        # END_OF_DATA at window close). This number matches the
        # engine's final trade-log count only if no re-entry filters
        # bind; for the common 0-or-few-trades regime the numbers
        # should agree.
        counts.trades_closed += 1

    return counts
