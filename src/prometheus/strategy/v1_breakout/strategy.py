"""V1 breakout strategy public entry point.

StrategySession holds rolling bar windows and computed indicators.
V1BreakoutStrategy composes bias / setup / trigger decisions and
produces typed intents. Neither class touches network, persistence,
or exchange state.

Backtest engine lifecycle (consumer's responsibility):

    session = StrategySession(symbol=...)
    strategy = V1BreakoutStrategy()

    for completed_1h_bar in completed_1h_bars_stream:
        session.observe_1h_bar(completed_1h_bar)

    for completed_15m_bar in completed_15m_bars_stream:
        session.observe_15m_bar(completed_15m_bar)
        if session.flat and session.ready_to_signal:
            entry = strategy.maybe_entry(session)
            if entry is not None:
                # engine fills on next bar's open, calls
                # session.on_entry_filled(...) afterwards
                ...
        elif session.in_trade:
            intent = strategy.manage(session, completed_15m_bar)
            # engine applies StopUpdateIntent or ExitIntent

Indicator-caching optimization (Phase 2e):

    The 15m / 1h Wilder ATR(20) and 1h EMA(50) / EMA(200) are now
    updated incrementally on each ``observe_*_bar`` call:

      - Seed once from the first period samples (matching the
        standalone ``wilder_atr`` / ``ema`` functions' conventions).
      - After the seed, each new bar updates the cached scalar via
        the Wilder / EMA recursion in O(1) time.

    This replaces the prior implementation that re-ran the full
    indicator over the 400-bar deque on every accessor call. For
    long backtests the prior implementation was O(bars × window);
    the incremental version is O(bars). Indicator values match
    the standalone functions exactly for the first ``maxlen`` bars
    and converge to within machine epsilon thereafter (Wilder /
    EMA half-life << deque length; see the unit tests for
    round-trip proof).

    The standalone ``wilder_atr`` and ``ema`` functions are
    untouched — they remain the reference used by test_indicators
    and by the signal-funnel diagnostic.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol

from ..indicators import true_range
from ..types import (
    BreakoutSignal,
    EntryIntent,
    ExitIntent,
    StopUpdateIntent,
    TrendBias,
)
from .bias import EMA_FAST, EMA_SLOW, SLOPE_LOOKBACK
from .management import ManagementBarDiagnostic, TradeManagement
from .setup import SETUP_SIZE, detect_setup
from .stop import compute_initial_stop, passes_stop_distance_filter
from .trigger import evaluate_long_trigger, evaluate_short_trigger

ATR_PERIOD = 20

# Minimum bar counts required before any signal can be evaluated.
MIN_1H_BARS_FOR_BIAS = EMA_SLOW + SLOPE_LOOKBACK  # 203
MIN_15M_BARS_FOR_SIGNAL = (
    ATR_PERIOD + 1 + SETUP_SIZE + 1  # 20 ATR warmup + 8 setup + 1 breakout
)


def _nan() -> float:
    return float("nan")


def _is_nan(x: float) -> bool:
    return x != x


@dataclass
class _ActiveTrade:
    """Per-trade bookkeeping held on the session while positioned."""

    entry_signal: BreakoutSignal
    entry_fill_time_ms: int
    entry_fill_price: float
    management: TradeManagement
    # open_time of the LAST completed 15m bar seen while positioned.
    # Used to ensure management processes each bar exactly once.
    last_processed_close_time: int = 0


@dataclass
class StrategySession:
    """Rolling state for one symbol's v1 strategy evaluation.

    The session maintains bounded-size bar deques plus incremental
    indicator caches (Wilder ATR(20) for 15m and 1h; EMA(50) and
    EMA(200) for 1h, plus a short slope-lookback history).
    """

    symbol: Symbol
    _1h_window: deque[NormalizedKline] = field(default_factory=lambda: deque(maxlen=400))
    _15m_window: deque[NormalizedKline] = field(default_factory=lambda: deque(maxlen=400))
    _active_trade: _ActiveTrade | None = None
    _last_exit_close_time_ms: int | None = None
    _bars_since_last_exit: int = 0

    # --- 15m ATR(20) incremental state ---
    _15m_tr_warmup: list[float] = field(default_factory=list)
    _15m_atr_latest: float = field(default_factory=_nan)
    _15m_atr_before_latest: float = field(default_factory=_nan)
    _15m_bars_observed: int = 0
    _15m_prev_close: float | None = None

    # --- 1h ATR(20) incremental state ---
    _1h_tr_warmup: list[float] = field(default_factory=list)
    _1h_atr_latest: float = field(default_factory=_nan)
    _1h_bars_observed: int = 0
    _1h_prev_close: float | None = None

    # --- 1h EMA(50), EMA(200) incremental state + slope history ---
    _1h_ema_fast_warmup: list[float] = field(default_factory=list)
    _1h_ema_slow_warmup: list[float] = field(default_factory=list)
    _1h_ema_fast_latest: float = field(default_factory=_nan)
    _1h_ema_slow_latest: float = field(default_factory=_nan)
    # History ring for the -3-bar slope check: keeps the last
    # SLOPE_LOOKBACK + 1 EMA-fast values, oldest first.
    _1h_ema_fast_history: deque[float] = field(
        default_factory=lambda: deque(maxlen=SLOPE_LOOKBACK + 1)
    )

    # Cached bias updated on each 1h observation once warmed up.
    _current_1h_bias: TrendBias = TrendBias.NEUTRAL

    # ----- Public observation API -----

    def observe_1h_bar(self, bar: NormalizedKline) -> None:
        """Append a completed 1h bar to the bias window and update indicators."""
        if bar.symbol != self.symbol:
            raise ValueError(f"bar.symbol {bar.symbol} != session.symbol {self.symbol}")
        if bar.interval != Interval.I_1H:
            raise ValueError(f"observe_1h_bar got interval {bar.interval}")
        if self._1h_window and bar.open_time <= self._1h_window[-1].open_time:
            raise ValueError("1h bars must be strictly monotonic in open_time")

        prev_close = self._1h_prev_close
        self._1h_window.append(bar)
        self._1h_prev_close = bar.close

        # Wilder ATR(20) incremental update.
        tr = true_range(bar.high, bar.low, prev_close)
        self._1h_bars_observed += 1
        if self._1h_bars_observed <= ATR_PERIOD:
            # Bars 1..20: accumulate TRs for the seed. No ATR yet.
            self._1h_tr_warmup.append(tr)
        elif self._1h_bars_observed == ATR_PERIOD + 1:
            # Match the reference wilder_atr: seed is placed at the
            # (period+1)-th observed bar; the TR from this bar is
            # deliberately not consumed (first recursion uses bar+1).
            self._1h_atr_latest = sum(self._1h_tr_warmup[:ATR_PERIOD]) / ATR_PERIOD
            self._1h_tr_warmup = []  # release
        else:
            self._1h_atr_latest = ((ATR_PERIOD - 1) * self._1h_atr_latest + tr) / ATR_PERIOD

        # EMA(50) + EMA(200) incremental updates.
        close = bar.close
        self._update_ema_fast(close)
        self._update_ema_slow(close)

        # Recompute bias if both EMAs are seeded and we have slope history.
        self._update_1h_bias()

    def observe_15m_bar(self, bar: NormalizedKline) -> None:
        """Append a completed 15m bar to the signal window and update indicators."""
        if bar.symbol != self.symbol:
            raise ValueError(f"bar.symbol {bar.symbol} != session.symbol {self.symbol}")
        if bar.interval != Interval.I_15M:
            raise ValueError(f"observe_15m_bar got interval {bar.interval}")
        if self._15m_window and bar.open_time <= self._15m_window[-1].open_time:
            raise ValueError("15m bars must be strictly monotonic in open_time")

        prev_close = self._15m_prev_close
        self._15m_window.append(bar)
        self._15m_prev_close = bar.close
        if self._active_trade is None and self._last_exit_close_time_ms is not None:
            self._bars_since_last_exit += 1

        # Wilder ATR(20) incremental update (matches reference wilder_atr).
        tr = true_range(bar.high, bar.low, prev_close)
        self._15m_atr_before_latest = self._15m_atr_latest
        self._15m_bars_observed += 1
        if self._15m_bars_observed <= ATR_PERIOD:
            self._15m_tr_warmup.append(tr)
        elif self._15m_bars_observed == ATR_PERIOD + 1:
            self._15m_atr_latest = sum(self._15m_tr_warmup[:ATR_PERIOD]) / ATR_PERIOD
            self._15m_tr_warmup = []
        else:
            self._15m_atr_latest = ((ATR_PERIOD - 1) * self._15m_atr_latest + tr) / ATR_PERIOD

    # ----- Private EMA + bias helpers (1h only) -----

    def _update_ema_fast(self, close: float) -> None:
        alpha = 2.0 / (EMA_FAST + 1.0)
        if _is_nan(self._1h_ema_fast_latest):
            self._1h_ema_fast_warmup.append(close)
            if len(self._1h_ema_fast_warmup) == EMA_FAST:
                seed = sum(self._1h_ema_fast_warmup) / EMA_FAST
                self._1h_ema_fast_latest = seed
                self._1h_ema_fast_warmup = []
        else:
            self._1h_ema_fast_latest = alpha * close + (1.0 - alpha) * self._1h_ema_fast_latest
        # Track the last SLOPE_LOOKBACK+1 values for slope lookup.
        if not _is_nan(self._1h_ema_fast_latest):
            self._1h_ema_fast_history.append(self._1h_ema_fast_latest)

    def _update_ema_slow(self, close: float) -> None:
        alpha = 2.0 / (EMA_SLOW + 1.0)
        if _is_nan(self._1h_ema_slow_latest):
            self._1h_ema_slow_warmup.append(close)
            if len(self._1h_ema_slow_warmup) == EMA_SLOW:
                seed = sum(self._1h_ema_slow_warmup) / EMA_SLOW
                self._1h_ema_slow_latest = seed
                self._1h_ema_slow_warmup = []
        else:
            self._1h_ema_slow_latest = alpha * close + (1.0 - alpha) * self._1h_ema_slow_latest

    def _update_1h_bias(self) -> None:
        """Recompute the cached 1h bias from the incremental EMAs.

        Mirrors the logic of ``bias.evaluate_1h_bias`` but on cached
        scalars. Requires both EMAs seeded AND the slope-lookback
        ring full (SLOPE_LOOKBACK + 1 values).
        """
        if _is_nan(self._1h_ema_fast_latest) or _is_nan(self._1h_ema_slow_latest):
            self._current_1h_bias = TrendBias.NEUTRAL
            return
        if len(self._1h_ema_fast_history) < SLOPE_LOOKBACK + 1:
            self._current_1h_bias = TrendBias.NEUTRAL
            return
        fast_now = self._1h_ema_fast_latest
        slow_now = self._1h_ema_slow_latest
        fast_then = self._1h_ema_fast_history[0]  # SLOPE_LOOKBACK bars earlier
        close_now = self._1h_window[-1].close
        long_ok = (fast_now > slow_now) and (close_now > fast_now) and (fast_now > fast_then)
        short_ok = (fast_now < slow_now) and (close_now < fast_now) and (fast_now < fast_then)
        if long_ok and not short_ok:
            self._current_1h_bias = TrendBias.LONG
        elif short_ok and not long_ok:
            self._current_1h_bias = TrendBias.SHORT
        else:
            self._current_1h_bias = TrendBias.NEUTRAL

    # ----- Read-only cached accessors (all O(1)) -----

    @property
    def flat(self) -> bool:
        return self._active_trade is None

    @property
    def in_trade(self) -> bool:
        return self._active_trade is not None

    @property
    def ready_to_signal(self) -> bool:
        """Enough bars to evaluate bias + setup + trigger."""
        return (
            len(self._1h_window) >= MIN_1H_BARS_FOR_BIAS
            and len(self._15m_window) >= MIN_15M_BARS_FOR_SIGNAL
        )

    @property
    def can_re_enter(self) -> bool:
        """Re-entry requires a new complete setup window AFTER the last exit."""
        if self._last_exit_close_time_ms is None:
            return True
        return self._bars_since_last_exit >= SETUP_SIZE

    def current_1h_atr_20(self) -> float:
        return self._1h_atr_latest

    def current_15m_atr_20(self) -> float:
        return self._15m_atr_latest

    def prior_15m_atr_20(self) -> float:
        """ATR(20) value as it stood BEFORE the latest 15m bar was observed."""
        return self._15m_atr_before_latest

    def latest_1h_close(self) -> float:
        if not self._1h_window:
            return float("nan")
        return self._1h_window[-1].close

    def current_1h_bias(self) -> TrendBias:
        """Return the cached 1h bias. NEUTRAL when insufficient warmup."""
        return self._current_1h_bias

    # ----- Trade-lifecycle hooks -----

    def on_entry_filled(
        self,
        *,
        signal: BreakoutSignal,
        fill_price: float,
        fill_time_ms: int,
        fill_bar: NormalizedKline,
        initial_stop: float,
    ) -> None:
        if self._active_trade is not None:
            raise ValueError("cannot enter: already in_trade")
        self._active_trade = _ActiveTrade(
            entry_signal=signal,
            entry_fill_time_ms=fill_time_ms,
            entry_fill_price=fill_price,
            management=TradeManagement.start(
                symbol=self.symbol,
                direction=signal.direction,
                entry_price=fill_price,
                initial_stop=initial_stop,
                entry_bar_high=fill_bar.high,
                entry_bar_low=fill_bar.low,
            ),
            last_processed_close_time=fill_bar.close_time,
        )

    def on_exit_recorded(self, exit_close_time_ms: int) -> None:
        if self._active_trade is None:
            raise ValueError("cannot exit: not in_trade")
        self._active_trade = None
        self._last_exit_close_time_ms = exit_close_time_ms
        self._bars_since_last_exit = 0

    @property
    def active_trade(self) -> _ActiveTrade | None:
        return self._active_trade


class V1BreakoutStrategy:
    """Stateless orchestrator. Decisions depend only on session state."""

    def maybe_entry(self, session: StrategySession) -> EntryIntent | None:
        """Evaluate all six long + short trigger conditions."""
        if not session.flat:
            return None
        if not session.can_re_enter:
            return None
        if not session.ready_to_signal:
            return None

        bars_15m = list(session._15m_window)
        breakout_bar = bars_15m[-1]
        prev_bar = bars_15m[-2]
        prior_8 = bars_15m[-(SETUP_SIZE + 1) : -1]
        assert len(prior_8) == SETUP_SIZE

        bias = session.current_1h_bias()
        if bias == TrendBias.NEUTRAL:
            return None

        atr_15m_at_prior = session.prior_15m_atr_20()
        if _is_nan(atr_15m_at_prior):
            return None
        setup = detect_setup(prior_8, atr_15m_at_prior)
        if setup is None:
            return None

        atr_15m_now = session.current_15m_atr_20()
        atr_1h = session.current_1h_atr_20()
        latest_1h_close = session.latest_1h_close()
        if _is_nan(atr_15m_now) or _is_nan(atr_1h):
            return None

        signal = evaluate_long_trigger(
            bias=bias,
            setup=setup,
            breakout_bar=breakout_bar,
            prev_15m_close=prev_bar.close,
            atr_20_15m=atr_15m_now,
            atr_20_1h=atr_1h,
            latest_1h_close=latest_1h_close,
        ) or evaluate_short_trigger(
            bias=bias,
            setup=setup,
            breakout_bar=breakout_bar,
            prev_15m_close=prev_bar.close,
            atr_20_15m=atr_15m_now,
            atr_20_1h=atr_1h,
            latest_1h_close=latest_1h_close,
        )
        if signal is None:
            return None

        initial_stop = compute_initial_stop(signal.direction, setup, breakout_bar, atr_15m_now)
        reference_price = breakout_bar.close  # per GAP-20260419-015
        stop_distance = abs(reference_price - initial_stop)
        if not passes_stop_distance_filter(stop_distance, atr_15m_now):
            return None
        return EntryIntent(
            symbol=session.symbol,
            direction=signal.direction,
            signal=signal,
            reference_price=reference_price,
            initial_stop=initial_stop,
            stop_distance=stop_distance,
        )

    def manage(
        self, session: StrategySession, latest_bar: NormalizedKline
    ) -> tuple[StopUpdateIntent | ExitIntent | None, ManagementBarDiagnostic | None]:
        active = session.active_trade
        if active is None:
            return None, None
        if latest_bar.close_time <= active.last_processed_close_time:
            return None, None
        active.last_processed_close_time = latest_bar.close_time
        atr_15m = session.current_15m_atr_20()
        if _is_nan(atr_15m):
            return None, None
        intent, diag = active.management.on_completed_bar(latest_bar, atr_15m)
        return intent, diag


def expected_15m_follow_open_time(bar: NormalizedKline) -> int:
    """Return the open_time of the 15m bar that immediately follows ``bar``."""
    if bar.interval != Interval.I_15M:
        raise ValueError("expected a 15m bar")
    return bar.open_time + interval_duration_ms(Interval.I_15M)
