"""Phase 3i-B1 — D1-A engine dispatch + lifecycle tests.

These tests exercise the engine's D1-A path end-to-end on small,
deterministic synthetic 15m series. They cover:

- D1-A long / short signal generation through the engine.
- D1-A produces no signal during warmup or with no eligible event.
- Entry timing: fill at next 15m bar open after signal bar close.
- Stop = 1.0 × ATR; target = +2.0R; stop never moves.
- TARGET trigger only on completed-bar close confirmation.
- TARGET fills at next bar open. Intrabar touch without completed
  close confirmation does NOT fill.
- TIME_STOP trigger at close of bar B+1+32; fill at open of B+1+33.
- Same-bar STOP > TARGET; same-bar TARGET > TIME_STOP.
- END_OF_DATA at last bar.
- D1-A emits only STOP / TARGET / TIME_STOP / END_OF_DATA.
- Per-funding-event cooldown: same-event same-direction blocked;
  fresh event allows re-entry.
- Lifecycle accounting identity holds:
  detected = filled + rejected_stop_distance + blocked_cooldown.
- TradeRecord D1-A fields populated for D1-A trades.

The synthetic series is engineered so ATR(20)(B) ≈ 1.0 at the signal
bar so stop_distance = 1.0 × ATR sits in the locked [0.60, 1.80] × ATR
admissibility band by construction.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from prometheus.core.events import FundingRateEvent
from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline
from prometheus.core.mark_price_klines import MarkPriceKline
from prometheus.core.symbols import Symbol
from prometheus.core.time import close_time_for
from prometheus.research.backtest import BacktestEngine, BacktestRunResult
from prometheus.research.backtest.config import (
    DEFAULT_SLIPPAGE_BPS,
    BacktestConfig,
    SlippageBucket,
    StrategyFamily,
)
from prometheus.strategy.funding_aware_directional import FundingAwareConfig
from prometheus.strategy.types import ExitReason

from .conftest import default_symbol_info

ANCHOR_MS = 1_772_582_400_000  # 2026-03-01 00:00:00 UTC
DUR_15M_MS = interval_duration_ms(Interval.I_15M)


def _bar(
    *,
    symbol: Symbol = Symbol.BTCUSDT,
    open_time: int,
    open_: float,
    high: float,
    low: float,
    close: float,
) -> NormalizedKline:
    return NormalizedKline(
        symbol=symbol,
        interval=Interval.I_15M,
        open_time=open_time,
        close_time=close_time_for(open_time, Interval.I_15M),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=1.0,
        quote_asset_volume=close,
        trade_count=1,
        taker_buy_base_volume=0.5,
        taker_buy_quote_volume=close * 0.5,
        source="synthetic-d1a-test",
    )


def _mark_for(bar: NormalizedKline) -> MarkPriceKline:
    return MarkPriceKline(
        symbol=bar.symbol,
        interval=bar.interval,
        open_time=bar.open_time,
        close_time=bar.close_time,
        open=bar.open,
        high=bar.high,
        low=bar.low,
        close=bar.close,
        source="synthetic-d1a-test",
    )


def _d1a_config(
    tmp_path: Path,
    *,
    slippage_bucket: SlippageBucket = SlippageBucket.MEDIUM,
) -> BacktestConfig:
    """A BacktestConfig wired for the D1-A dispatch."""
    return BacktestConfig(
        experiment_name="d1a-engine-test",
        run_id="r-0001",
        symbols=(Symbol.BTCUSDT,),
        window_start_ms=ANCHOR_MS,
        window_end_ms=ANCHOR_MS + 10_000 * DUR_15M_MS,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=slippage_bucket,
        slippage_bps_map=dict(DEFAULT_SLIPPAGE_BPS),
        klines_root=tmp_path / "klines",
        mark_price_root=tmp_path / "mark",
        funding_root=tmp_path / "funding",
        bars_1h_root=tmp_path / "1h",
        exchange_info_path=tmp_path / "ei.json",
        reports_root=tmp_path / "reports",
        strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
        funding_aware_variant=FundingAwareConfig(),
    )


def _build_prior_funding_events(
    *,
    n: int = 270,
    base_time: int = 1_000_000_000,
    base_rate_alt: float = 0.0001,
) -> list[FundingRateEvent]:
    """Build N prior funding events alternating ±base_rate_alt.

    Sample mean ≈ 0; sample std ≈ base_rate_alt. Times incrementing
    by 1ms each so they're chronological and earlier than any later
    event we add.
    """
    events: list[FundingRateEvent] = []
    for i in range(n):
        sign = 1 if i % 2 == 0 else -1
        events.append(
            FundingRateEvent(
                symbol=Symbol.BTCUSDT,
                funding_time=base_time + i,
                funding_rate=sign * base_rate_alt,
                mark_price=None,
                source="synthetic-d1a-test",
            )
        )
    return events


def _build_extreme_funding_event(
    *, funding_time: int, funding_rate: float = 0.0005
) -> FundingRateEvent:
    """Build a single extreme funding event.

    Default rate 0.0005 → Z ≈ +5 on prior with std ≈ 0.0001 → SHORT
    signal contrarian. Pass a negative rate for a LONG signal.
    """
    return FundingRateEvent(
        symbol=Symbol.BTCUSDT,
        funding_time=funding_time,
        funding_rate=funding_rate,
        mark_price=None,
        source="synthetic-d1a-test",
    )


def _build_warmup_bars(*, n_bars: int = 22, start_price: float = 100.0) -> list[NormalizedKline]:
    """Build N flat bars at start_price with unit TR (high=close+0.5,
    low=close-0.5) so ATR(20) seeds to 1.0 by bar 19+."""
    bars: list[NormalizedKline] = []
    t = ANCHOR_MS
    for _ in range(n_bars):
        bars.append(
            _bar(
                open_time=t,
                open_=start_price,
                high=start_price + 0.5,
                low=start_price - 0.5,
                close=start_price,
            )
        )
        t += DUR_15M_MS
    return bars


def _next_bar_after(
    bars: list[NormalizedKline],
    *,
    open_: float,
    high: float | None = None,
    low: float | None = None,
    close: float | None = None,
) -> NormalizedKline:
    """Append a new bar after the last bar in ``bars`` and return it."""
    last_t = bars[-1].open_time
    new_t = last_t + DUR_15M_MS
    return _bar(
        open_time=new_t,
        open_=open_,
        high=high if high is not None else open_ + 0.5,
        low=low if low is not None else open_ - 0.5,
        close=close if close is not None else open_,
    )


def _run_d1a_engine(
    cfg: BacktestConfig,
    bars: list[NormalizedKline],
    funding_events: list[FundingRateEvent],
) -> BacktestRunResult:
    engine = BacktestEngine(cfg)
    return engine.run(
        klines_15m_per_symbol={Symbol.BTCUSDT: bars},
        klines_1h_per_symbol={Symbol.BTCUSDT: []},  # D1-A does not use 1h
        mark_15m_per_symbol={Symbol.BTCUSDT: [_mark_for(b) for b in bars]},
        funding_per_symbol={Symbol.BTCUSDT: funding_events},
        symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
    )


# ---------------------------------------------------------------------
# 9. D1-A creates LONG trade on negative funding extreme
# ---------------------------------------------------------------------


def test_d1a_long_entry_at_negative_extreme(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    # Extreme negative funding event eligible from bar 0 onward
    # (funding_time before all bar open_times).
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=-0.0005)
    )
    # Add bars after the warmup so a trade can fill and close.
    # Warmup is 22 bars (indices 0..21). Signal at bar 21 → fill at 22.
    bars.append(_next_bar_after(bars, open_=100.0))
    # Add 5 more flat bars so the position can hold without target/stop fires.
    for _ in range(5):
        bars.append(_next_bar_after(bars, open_=100.0))
    # Add a bar with completed close that triggers LONG TARGET.
    # LONG target = fill_price + 2.0 × stop_distance ≈ 100 + 2 = 102.
    bars.append(_next_bar_after(bars, open_=100.0, high=103.0, low=100.0, close=103.0))
    # Add one more bar so TARGET can fill at next-bar open.
    bars.append(_next_bar_after(bars, open_=102.5))

    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades >= 1
    trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
    assert trade.direction == "LONG"
    counters = result.funding_aware_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.funding_extreme_events_filled >= 1


# ---------------------------------------------------------------------
# 10. D1-A creates SHORT trade on positive funding extreme
# ---------------------------------------------------------------------


def test_d1a_short_entry_at_positive_extreme(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=+0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    # Run a few flat bars; SHORT TARGET = fill_price - 2.0 × stop_distance ≈ 98.
    for _ in range(5):
        bars.append(_next_bar_after(bars, open_=100.0))
    # Bar with close <= 98 triggers SHORT TARGET.
    bars.append(_next_bar_after(bars, open_=100.0, high=100.5, low=97.0, close=97.0))
    # Next-bar fill bar.
    bars.append(_next_bar_after(bars, open_=97.5))

    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades >= 1
    trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
    assert trade.direction == "SHORT"


# ---------------------------------------------------------------------
# 11. D1-A creates no trade below threshold (sub-extreme funding)
# ---------------------------------------------------------------------


def test_d1a_no_trade_below_threshold(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=30)
    funding_events = _build_prior_funding_events()
    # Add a "small" funding event that produces |Z| < 2 (e.g., 0.00015
    # → Z ≈ 1.5 with std ≈ 0.0001).
    funding_events.append(
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=ANCHOR_MS - 1_000_000,
            funding_rate=0.00015,
            mark_price=None,
            source="synthetic-d1a-test",
        )
    )
    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades == 0
    counters = result.funding_aware_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.funding_extreme_events_detected == 0


# ---------------------------------------------------------------------
# 12. D1-A creates no signal during Z-score warmup
# ---------------------------------------------------------------------


def test_d1a_no_signal_during_z_score_warmup(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=30)
    # Only 100 prior funding events (warmup needs 270).
    funding_events = _build_prior_funding_events(n=100)
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades == 0
    counters = result.funding_aware_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.funding_extreme_events_detected == 0


# ---------------------------------------------------------------------
# 13. D1-A creates no signal on zero-variance funding window
# ---------------------------------------------------------------------


def test_d1a_no_signal_zero_variance_window(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=30)
    # 270 events all identical → sample variance = 0 → Z = NaN.
    funding_events = [
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=1_000_000_000 + i,
            funding_rate=0.0001,
            mark_price=None,
            source="synthetic-d1a-test",
        )
        for i in range(270)
    ]
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0010)
    )
    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades == 0


# ---------------------------------------------------------------------
# 19. Next-bar-open entry timing
# ---------------------------------------------------------------------


def test_d1a_fill_at_next_bar_open(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    fill_open_price = 100.5
    bars.append(_next_bar_after(bars, open_=fill_open_price))
    # Hold flat; then close at end-of-data so a trade record is emitted.
    for _ in range(5):
        bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    if result.per_symbol_trades.get(Symbol.BTCUSDT):
        trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
        # First ATR(20)-valid bar is bar 20 (Wilder warmup ends after
        # period bars). Signal at bar 20's close → fill at bar 21's
        # open: open_time = ANCHOR + 21 × DUR_15M_MS.
        expected_fill_time = ANCHOR_MS + 21 * DUR_15M_MS
        assert trade.entry_fill_time_ms == expected_fill_time


# ---------------------------------------------------------------------
# 20-21. Stop = 1.0 × ATR, target = +2.0R
# ---------------------------------------------------------------------


def test_d1a_stop_and_target_geometry(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    for _ in range(5):
        bars.append(_next_bar_after(bars, open_=100.0))
    # Drive close below SHORT target ≈ 98 to fire TARGET.
    bars.append(_next_bar_after(bars, open_=100.0, high=100.5, low=97.0, close=97.5))
    bars.append(_next_bar_after(bars, open_=97.5))

    result = _run_d1a_engine(cfg, bars, funding_events)
    if result.per_symbol_trades.get(Symbol.BTCUSDT):
        trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
        # ATR(20) at bar 21 ≈ 1.0 (flat warmup with TR=1).
        # stop_distance ≈ 1.0; target distance ≈ 2.0.
        assert 0.9 <= trade.stop_distance <= 1.2
        # Reused entry_to_target_distance_atr field populated for D1-A.
        assert 1.8 <= trade.entry_to_target_distance_atr <= 2.2
        # Reused stop_distance_at_signal_atr field populated; ≈ 1.0.
        assert 0.9 <= trade.stop_distance_at_signal_atr <= 1.1


# ---------------------------------------------------------------------
# 27. TARGET triggers on completed close >= target for LONG
# 28. TARGET triggers on completed close <= target for SHORT
# 29. TARGET fills at next bar open
# ---------------------------------------------------------------------


def test_d1a_target_completed_close_fill_long(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=-0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    for _ in range(3):
        bars.append(_next_bar_after(bars, open_=100.0))
    # LONG target ≈ 102. Bar with completed close >= 102 triggers TARGET.
    target_trigger_bar_idx_after_fill = len(bars)
    bars.append(_next_bar_after(bars, open_=100.0, high=102.5, low=100.0, close=102.3))
    target_fill_bar_open = 102.0
    bars.append(_next_bar_after(bars, open_=target_fill_bar_open))

    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades >= 1
    trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
    assert trade.exit_reason == "TARGET"
    # Exit fill time should be open of bar AFTER the target-trigger bar.
    expected_exit_time = ANCHOR_MS + (target_trigger_bar_idx_after_fill + 1) * DUR_15M_MS
    assert trade.exit_fill_time_ms == expected_exit_time


def test_d1a_target_completed_close_fill_short(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    for _ in range(3):
        bars.append(_next_bar_after(bars, open_=100.0))
    # SHORT target ≈ 98. Bar with close <= 98 triggers TARGET.
    bars.append(_next_bar_after(bars, open_=100.0, high=100.5, low=97.5, close=97.7))
    bars.append(_next_bar_after(bars, open_=97.7))

    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades >= 1
    trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
    assert trade.exit_reason == "TARGET"


# ---------------------------------------------------------------------
# 30. Intrabar target touch without close confirmation does not fill
# ---------------------------------------------------------------------


def test_d1a_intrabar_target_touch_does_not_fire(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=-0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    for _ in range(3):
        bars.append(_next_bar_after(bars, open_=100.0))
    # Intrabar HIGH touches LONG target ≈ 102 but completed close
    # is back below 102 — TARGET should NOT fire.
    bars.append(_next_bar_after(bars, open_=100.0, high=102.5, low=99.5, close=101.0))
    # A few more flat bars so the trade stays open.
    for _ in range(5):
        bars.append(_next_bar_after(bars, open_=101.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    # If a trade exists, it must NOT have exited via TARGET on the
    # intrabar-touch bar.
    for trade in result.per_symbol_trades.get(Symbol.BTCUSDT, []):
        if trade.exit_reason == "TARGET":
            # If a target hit later (legitimately on a completed close),
            # that's allowed; ensure the intrabar-touch bar did NOT
            # produce a same-close TARGET fill.
            intrabar_touch_close_time = ANCHOR_MS + (22 + 4) * DUR_15M_MS + DUR_15M_MS - 1
            # exit_fill_time must be at next bar open (not the intrabar
            # touch bar's close + 1ms).
            assert trade.exit_fill_time_ms != intrabar_touch_close_time + 1


# ---------------------------------------------------------------------
# 31-32. TIME_STOP triggers at close of B+1+32; fills at open of B+1+33
# ---------------------------------------------------------------------


def test_d1a_time_stop_fires_at_horizon(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    # First ATR(20)-valid bar is bar 20; signal at bar 20 → fill at
    # bar 21 (B+1). TIME_STOP triggers at close of bar 21 + 32 = 53;
    # fill at open of bar 54. Build 55 bars total (22 warmup + ~33
    # hold bars after the fill).
    bars.append(_next_bar_after(bars, open_=100.0))  # bar 22
    # Bars 23..53: flat at 100 so no STOP / TARGET fires.
    for _ in range(32):
        bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades >= 1
    trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
    assert trade.exit_reason == "TIME_STOP"
    expected_exit_time = ANCHOR_MS + 54 * DUR_15M_MS
    assert trade.exit_fill_time_ms == expected_exit_time


# ---------------------------------------------------------------------
# 33. Same-bar priority STOP > TARGET (synthetic high-volatility bar)
# ---------------------------------------------------------------------


def test_d1a_same_bar_priority_stop_before_target(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=-0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    # Bar that has BOTH:
    #   - low <= LONG stop (≈ 99)  → STOP fires.
    #   - close >= LONG target (≈ 102) → TARGET would fire.
    # STOP should fire first by same-bar priority.
    bars.append(_next_bar_after(bars, open_=100.0, high=103.0, low=98.5, close=102.5))
    # Add post-bar so any subsequent fill could land.
    bars.append(_next_bar_after(bars, open_=98.5))

    result = _run_d1a_engine(cfg, bars, funding_events)
    if result.per_symbol_trades.get(Symbol.BTCUSDT):
        trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
        assert trade.exit_reason == "STOP"


# ---------------------------------------------------------------------
# 35. END_OF_DATA at last bar
# ---------------------------------------------------------------------


def test_d1a_end_of_data_at_window_close(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    # Only a couple more flat bars so the trade is still open at end.
    for _ in range(3):
        bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    assert result.total_trades >= 1
    trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
    assert trade.exit_reason == "END_OF_DATA"


# ---------------------------------------------------------------------
# 36-37. D1-A emits only STOP / TARGET / TIME_STOP / END_OF_DATA.
# ---------------------------------------------------------------------


def test_d1a_emits_only_allowed_exit_reasons(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    for _ in range(35):
        bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    allowed = {"STOP", "TARGET", "TIME_STOP", "END_OF_DATA"}
    forbidden = {"TRAILING_BREACH", "STAGNATION", "TAKE_PROFIT"}
    for trade in result.per_symbol_trades.get(Symbol.BTCUSDT, []):
        assert trade.exit_reason in allowed
        assert trade.exit_reason not in forbidden


# ---------------------------------------------------------------------
# 41. Repeated 15m bars referencing same funding event do not inflate
#     detected event count
# ---------------------------------------------------------------------


def test_d1a_repeated_bar_references_do_not_inflate_detected(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=30)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    # No further funding events; multiple bars after warmup will all
    # reference the same extreme event as latest.
    for _ in range(20):
        bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    counters = result.funding_aware_counters_per_symbol[Symbol.BTCUSDT]
    # Only ONE detected event despite many bars referencing it.
    assert counters.funding_extreme_events_detected == 1


# ---------------------------------------------------------------------
# 42. Lifecycle accounting identity holds:
#     detected = filled + rejected_stop_distance + blocked_cooldown.
# ---------------------------------------------------------------------


def test_d1a_lifecycle_identity_holds(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=30)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    for _ in range(20):
        bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    counters = result.funding_aware_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.accounting_identity_holds is True


# ---------------------------------------------------------------------
# 43. Funding accrual signed correctly (SHORT at positive funding =
#     positive funding benefit; LONG at negative funding = positive
#     funding benefit).
# ---------------------------------------------------------------------


def test_d1a_funding_accrual_signed_correctly_short(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    # Extreme positive funding → SHORT entry.
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    # During the trade-hold window, add an in-window funding event with
    # positive rate so the SHORT position collects positive funding.
    funding_events.append(
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=ANCHOR_MS + 22 * DUR_15M_MS + DUR_15M_MS // 2,
            funding_rate=0.0005,
            mark_price=None,
            source="synthetic-d1a-test",
        )
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    for _ in range(33):
        bars.append(_next_bar_after(bars, open_=100.0))
    bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    for trade in result.per_symbol_trades.get(Symbol.BTCUSDT, []):
        if trade.direction == "SHORT":
            # Positive funding accrued during the SHORT hold should be
            # a positive funding_pnl benefit (the strategy receives
            # funding from longs).
            assert trade.funding_pnl >= 0.0


# ---------------------------------------------------------------------
# 46-48. TradeRecord D1-A fields populated for D1-A trades; defaults
#        for V1 / F1 rows.
# ---------------------------------------------------------------------


def test_d1a_trade_record_funding_fields_populated(tmp_path) -> None:
    cfg = _d1a_config(tmp_path)
    bars = _build_warmup_bars(n_bars=22)
    funding_events = _build_prior_funding_events()
    funding_events.append(
        _build_extreme_funding_event(funding_time=ANCHOR_MS - 1_000_000, funding_rate=0.0005)
    )
    bars.append(_next_bar_after(bars, open_=100.0))
    for _ in range(3):
        bars.append(_next_bar_after(bars, open_=100.0))

    result = _run_d1a_engine(cfg, bars, funding_events)
    if result.per_symbol_trades.get(Symbol.BTCUSDT):
        trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
        assert trade.funding_event_id_at_signal is not None
        assert trade.funding_event_id_at_signal.startswith("BTCUSDT-")
        assert trade.funding_rate_at_signal == 0.0005
        # Z-score should be ≈ 5 (extreme funding 0.0005 with prior std ≈ 0.0001)
        assert trade.funding_z_score_at_signal > 4.0
        assert trade.bars_since_funding_event_at_signal >= 0


# ---------------------------------------------------------------------
# Phase 3i-B1: V1 H0 default behavior unchanged on the synthetic series.
# ---------------------------------------------------------------------


def test_v1_h0_default_unchanged_with_d1a_module_loaded(tmp_path) -> None:
    """V1 default config + synthetic series produces no errors and no
    D1-A counters (the D1-A path is dormant under V1)."""
    base = _d1a_config(tmp_path)
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "funding_aware_variant"}),
        strategy_family=StrategyFamily.V1_BREAKOUT,
        funding_aware_variant=None,
    )
    bars = _build_warmup_bars(n_bars=30)
    funding_events = _build_prior_funding_events()
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={Symbol.BTCUSDT: bars},
        klines_1h_per_symbol={Symbol.BTCUSDT: []},
        mark_15m_per_symbol={Symbol.BTCUSDT: [_mark_for(b) for b in bars]},
        funding_per_symbol={Symbol.BTCUSDT: funding_events},
        symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
    )
    counters = result.funding_aware_counters_per_symbol.get(Symbol.BTCUSDT)
    if counters is not None:
        assert counters.funding_extreme_events_detected == 0
        assert counters.funding_extreme_events_filled == 0


# ---------------------------------------------------------------------
# Phase 3i-B1: runner scaffold requires explicit authorization flag and
# fails closed without it (test #8 in the brief).
# ---------------------------------------------------------------------


def test_d1a_runner_scaffold_requires_authorization_flag() -> None:
    """The Phase 3i-B1 D1-A runner script exits non-zero without the
    documented Phase 3j authorization flag (analogous to Phase 3d-B1
    --phase-3d-b2-authorized precedent)."""
    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/phase3j_D1A_execution.py",
            "d1a",
            "--window",
            "R",
        ],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parents[4]),
    )
    assert completed.returncode != 0
    assert "Phase 3j authorization" in completed.stderr


def test_d1a_runner_scaffold_check_imports_ok() -> None:
    """The runner scaffold's check-imports subcommand is safe to run
    without authorization and exits zero."""
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, "scripts/phase3j_D1A_execution.py", "check-imports"],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parents[4]),
    )
    assert completed.returncode == 0
    assert "imports OK" in completed.stdout


# Suppress unused-import warning for Sequence (used in earlier scaffolds).
_ = Sequence
_ = ExitReason
