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
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol

from ..indicators import wilder_atr
from ..types import (
    BreakoutSignal,
    EntryIntent,
    ExitIntent,
    StopUpdateIntent,
    TrendBias,
)
from .bias import EMA_SLOW, SLOPE_LOOKBACK, evaluate_1h_bias
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

    The session maintains bounded-size windows so long simulations
    do not grow unbounded. Window caps are generous (several multiples
    of indicator lookbacks) and never clipped below a safe floor.
    """

    symbol: Symbol
    _1h_window: deque[NormalizedKline] = field(default_factory=lambda: deque(maxlen=400))
    _15m_window: deque[NormalizedKline] = field(default_factory=lambda: deque(maxlen=400))
    _active_trade: _ActiveTrade | None = None
    _last_exit_close_time_ms: int | None = None
    _bars_since_last_exit: int = 0

    def observe_1h_bar(self, bar: NormalizedKline) -> None:
        """Append a completed 1h bar to the bias window."""
        if bar.symbol != self.symbol:
            raise ValueError(f"bar.symbol {bar.symbol} != session.symbol {self.symbol}")
        if bar.interval != Interval.I_1H:
            raise ValueError(f"observe_1h_bar got interval {bar.interval}")
        if self._1h_window and bar.open_time <= self._1h_window[-1].open_time:
            raise ValueError("1h bars must be strictly monotonic in open_time")
        self._1h_window.append(bar)

    def observe_15m_bar(self, bar: NormalizedKline) -> None:
        """Append a completed 15m bar to the signal window."""
        if bar.symbol != self.symbol:
            raise ValueError(f"bar.symbol {bar.symbol} != session.symbol {self.symbol}")
        if bar.interval != Interval.I_15M:
            raise ValueError(f"observe_15m_bar got interval {bar.interval}")
        if self._15m_window and bar.open_time <= self._15m_window[-1].open_time:
            raise ValueError("15m bars must be strictly monotonic in open_time")
        self._15m_window.append(bar)
        if self._active_trade is None and self._last_exit_close_time_ms is not None:
            self._bars_since_last_exit += 1

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
        """Re-entry requires a new complete setup window AFTER the last exit.

        We approximate "new complete setup window" as: at least
        SETUP_SIZE full 15m bars have closed since the exit. A more
        restrictive interpretation (new VALID setup) is enforced
        implicitly because ``detect_setup`` is run on each candidate.
        """
        if self._last_exit_close_time_ms is None:
            return True
        return self._bars_since_last_exit >= SETUP_SIZE

    def current_1h_atr_20(self) -> float:
        """Return the 1h ATR(20) evaluated at the latest completed 1h bar."""
        bars = list(self._1h_window)
        if len(bars) < ATR_PERIOD + 1:
            return float("nan")
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        closes = [b.close for b in bars]
        series = wilder_atr(highs, lows, closes, ATR_PERIOD)
        return series[-1]

    def current_15m_atr_20(self) -> float:
        """Return the 15m ATR(20) evaluated at the latest completed 15m bar."""
        bars = list(self._15m_window)
        if len(bars) < ATR_PERIOD + 1:
            return float("nan")
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        closes = [b.close for b in bars]
        series = wilder_atr(highs, lows, closes, ATR_PERIOD)
        return series[-1]

    def prior_15m_atr_20(self) -> float:
        """Return the 15m ATR(20) evaluated at the bar BEFORE the last one.

        Used by the setup detector: ATR(20) at ``[-1]`` of the prior
        8 bars, i.e., the bar immediately before the breakout
        candidate.
        """
        bars = list(self._15m_window)
        if len(bars) < ATR_PERIOD + 2:
            return float("nan")
        highs = [b.high for b in bars[:-1]]
        lows = [b.low for b in bars[:-1]]
        closes = [b.close for b in bars[:-1]]
        series = wilder_atr(highs, lows, closes, ATR_PERIOD)
        return series[-1]

    def latest_1h_close(self) -> float:
        if not self._1h_window:
            return float("nan")
        return self._1h_window[-1].close

    def on_entry_filled(
        self,
        *,
        signal: BreakoutSignal,
        fill_price: float,
        fill_time_ms: int,
        fill_bar: NormalizedKline,
        initial_stop: float,
    ) -> None:
        """Register that the engine filled an entry for this signal.

        After this call, ``in_trade`` is True and management becomes
        active.
        """
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
        """Register that the engine closed the position."""
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
        """Evaluate all six long + short trigger conditions.

        Returns an ``EntryIntent`` if a long OR short trigger fires
        on the most recent 15m bar in ``session``. Returns None
        otherwise (no signal, or session not yet in_trade rules
        satisfied).

        Both long and short triggers are evaluated; at most one can
        fire for a given bar because bias is long XOR short XOR
        neutral.
        """
        if not session.flat:
            return None
        if not session.can_re_enter:
            return None
        if not session.ready_to_signal:
            return None

        bars_15m = list(session._15m_window)
        breakout_bar = bars_15m[-1]
        prev_bar = bars_15m[-2]
        prior_8 = bars_15m[-(SETUP_SIZE + 1) : -1]  # indices [-9..-2], exclusive of breakout
        assert len(prior_8) == SETUP_SIZE

        bias = evaluate_1h_bias(list(session._1h_window))
        if bias == TrendBias.NEUTRAL:
            return None

        atr_15m_at_prior = session.prior_15m_atr_20()
        if atr_15m_at_prior != atr_15m_at_prior:  # NaN check
            return None
        setup = detect_setup(prior_8, atr_15m_at_prior)
        if setup is None:
            return None

        atr_15m_now = session.current_15m_atr_20()
        atr_1h = session.current_1h_atr_20()
        latest_1h_close = session.latest_1h_close()
        if atr_15m_now != atr_15m_now or atr_1h != atr_1h:  # NaN
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
        """Run stage management for the currently open trade.

        ``latest_bar`` must be the most recently observed 15m bar in
        the session (the caller is responsible for supplying it to
        avoid re-iterating the window).
        """
        active = session.active_trade
        if active is None:
            return None, None
        if latest_bar.close_time <= active.last_processed_close_time:
            # Idempotency guard: same bar, don't re-process.
            return None, None
        active.last_processed_close_time = latest_bar.close_time
        atr_15m = session.current_15m_atr_20()
        if atr_15m != atr_15m:  # NaN
            return None, None
        intent, diag = active.management.on_completed_bar(latest_bar, atr_15m)
        return intent, diag


def expected_15m_follow_open_time(bar: NormalizedKline) -> int:
    """Return the open_time of the 15m bar that immediately follows ``bar``."""
    if bar.interval != Interval.I_15M:
        raise ValueError("expected a 15m bar")
    return bar.open_time + interval_duration_ms(Interval.I_15M)
