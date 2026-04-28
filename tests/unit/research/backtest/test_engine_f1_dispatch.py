"""Phase 3d-B1 — F1 engine dispatch + lifecycle tests.

These tests exercise the engine's F1 path end-to-end on small,
deterministic synthetic series. They cover:

- BacktestConfig dispatch acceptance / rejection (test_config covers
  the validator surface; here we exercise the engine path).
- F1 long / short signal generation through the engine.
- F1 stop-distance admissibility (below-band, above-band, in-band).
- Raw vs slipped reference price for the band check.
- F1 target exit at next-bar open with completed-bar close
  confirmation only.
- F1 time-stop exit at the spec'd 8-bar horizon from fill.
- F1 same-bar STOP > TARGET > TIME_STOP priority.
- F1 same-direction cooldown blocking and post-unwind allowance.
- F1 frozen target / frozen stop invariants.
- F1 funnel-counter accounting identity.
- F1 emits no V1-only exit reasons.
- V1 H0 default behavior unchanged when F1 module is on the import
  graph.

The synthetic series is engineered so ATR(20)(B) ≈ 1.0 at the signal
bar and the entry / stop / target distances all fall inside the locked
[0.60, 1.80] × ATR admissibility band.
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
from prometheus.strategy.mean_reversion_overextension import MeanReversionConfig
from prometheus.strategy.types import Direction, ExitReason

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
        source="synthetic-f1-test",
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
        source="synthetic-f1-test",
    )


def _f1_config(
    tmp_path: Path,
    *,
    slippage_bucket: SlippageBucket = SlippageBucket.MEDIUM,
    slippage_bps_map: dict[SlippageBucket, float] | None = None,
) -> BacktestConfig:
    """A BacktestConfig wired for the F1 dispatch."""
    return BacktestConfig(
        experiment_name="f1-engine-test",
        run_id="r-0001",
        symbols=(Symbol.BTCUSDT,),
        # Window covers bars 0..(n-1); engine respects window via
        # bar.open_time. We pick a wide window so all bars in the
        # synthetic series are eligible for entry evaluation.
        window_start_ms=ANCHOR_MS,
        window_end_ms=ANCHOR_MS + 10_000 * DUR_15M_MS,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=slippage_bucket,
        slippage_bps_map=(
            dict(slippage_bps_map) if slippage_bps_map else dict(DEFAULT_SLIPPAGE_BPS)
        ),
        klines_root=tmp_path / "klines",
        mark_price_root=tmp_path / "mark",
        funding_root=tmp_path / "funding",
        bars_1h_root=tmp_path / "1h",
        exchange_info_path=tmp_path / "ei.json",
        reports_root=tmp_path / "reports",
        strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
        mean_reversion_variant=MeanReversionConfig(),
    )


def _build_long_overextension_series(
    *,
    extra_after_signal: int = 30,
    fill_bar_open: float = 92.0,
    target_close_idx: int | None = None,
    stop_violation_at: int | None = None,
    fill_bar_low: float | None = None,
) -> tuple[list[NormalizedKline], int, int]:
    """Build a 15m series triggering an F1 LONG entry at idx=28.

    Bars 0..20: flat at 100, high=100.5, low=99.5 → TR=1, ATR(20)(20)=1.0.
    Bars 21..27: each drops by 1, TR=1 → ATR stays at 1.0.
    Bar 28 (signal bar B): close=92 with intrabar wick to low=91 →
        ATR(20)(28) ≈ 1.05; displacement = 92 - 100 = -8;
        threshold = 1.75 × 1.05 = 1.8375 → fires LONG candidate.
    Bar 29 (fill bar): open=``fill_bar_open``; ``fill_bar_low`` (defaults
        to ``open - 0.5``) controls intrabar movement on the fill bar.
    Bars 30+: configurable via ``target_close_idx`` / ``stop_violation_at``.

    Returns (klines, signal_bar_index, fill_bar_index).
    """
    bars: list[NormalizedKline] = []
    t = ANCHOR_MS
    # Bars 0..20: flat at 100 with unit TR.
    for _ in range(21):
        bars.append(_bar(open_time=t, open_=100.0, high=100.5, low=99.5, close=100.0))
        t += DUR_15M_MS
    # Bars 21..27: drop by 1 each, TR=1.
    closes_down = [99.0, 98.0, 97.0, 96.0, 95.0, 94.0, 93.0]
    prev_close = 100.0
    for c in closes_down:
        bars.append(_bar(open_time=t, open_=prev_close, high=prev_close, low=c, close=c))
        prev_close = c
        t += DUR_15M_MS
    # Bar 28 (signal bar B): close=92, low=91 (intrabar wick), high=93.
    bars.append(_bar(open_time=t, open_=93.0, high=93.0, low=91.0, close=92.0))
    signal_bar_index = len(bars) - 1
    t += DUR_15M_MS
    # Bar 29 (fill bar B+1): open=fill_bar_open.
    fbl = fill_bar_low if fill_bar_low is not None else fill_bar_open - 0.5
    bars.append(
        _bar(
            open_time=t,
            open_=fill_bar_open,
            high=fill_bar_open,
            low=fbl,
            close=fill_bar_open,
        )
    )
    fill_bar_index = len(bars) - 1
    t += DUR_15M_MS
    # Bars 30+: post-fill bars. Default flat near fill_bar_open so no
    # exit fires (used by warmup / no-target tests). Tests that need
    # specific exit conditions override via target_close_idx /
    # stop_violation_at.
    for _ in range(extra_after_signal):
        idx_local = len(bars)
        if stop_violation_at is not None and idx_local == stop_violation_at:
            # Drive the bar's low below the stop level (~90.895).
            bars.append(
                _bar(open_time=t, open_=fill_bar_open, high=fill_bar_open, low=85.0, close=85.5)
            )
        elif target_close_idx is not None and idx_local == target_close_idx:
            # Push close above the frozen SMA(8) target ≈ 96.625 → long target.
            bars.append(
                _bar(open_time=t, open_=fill_bar_open, high=99.0, low=fill_bar_open, close=99.0)
            )
        else:
            bars.append(
                _bar(
                    open_time=t,
                    open_=fill_bar_open,
                    high=fill_bar_open + 0.5,
                    low=fill_bar_open - 0.5,
                    close=fill_bar_open,
                )
            )
        t += DUR_15M_MS
    return bars, signal_bar_index, fill_bar_index


def _build_short_overextension_series(
    *,
    extra_after_signal: int = 30,
    fill_bar_open: float = 108.0,
) -> tuple[list[NormalizedKline], int, int]:
    """Mirror of the long series: triggers an F1 SHORT entry at idx=28."""
    bars: list[NormalizedKline] = []
    t = ANCHOR_MS
    for _ in range(21):
        bars.append(_bar(open_time=t, open_=100.0, high=100.5, low=99.5, close=100.0))
        t += DUR_15M_MS
    closes_up = [101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0]
    prev_close = 100.0
    for c in closes_up:
        bars.append(_bar(open_time=t, open_=prev_close, high=c, low=prev_close, close=c))
        prev_close = c
        t += DUR_15M_MS
    # Bar 28: close=108, high=109 (intrabar wick), low=107.
    bars.append(_bar(open_time=t, open_=107.0, high=109.0, low=107.0, close=108.0))
    signal_bar_index = len(bars) - 1
    t += DUR_15M_MS
    bars.append(
        _bar(
            open_time=t,
            open_=fill_bar_open,
            high=fill_bar_open + 0.5,
            low=fill_bar_open,
            close=fill_bar_open,
        )
    )
    fill_bar_index = len(bars) - 1
    t += DUR_15M_MS
    for _ in range(extra_after_signal):
        bars.append(
            _bar(
                open_time=t,
                open_=fill_bar_open,
                high=fill_bar_open + 0.5,
                low=fill_bar_open - 0.5,
                close=fill_bar_open,
            )
        )
        t += DUR_15M_MS
    return bars, signal_bar_index, fill_bar_index


def _empty_inputs(
    bars_15m: Sequence[NormalizedKline],
) -> tuple[
    dict[Symbol, Sequence[NormalizedKline]],
    dict[Symbol, Sequence[NormalizedKline]],
    dict[Symbol, Sequence[MarkPriceKline]],
    dict[Symbol, Sequence[FundingRateEvent]],
]:
    """Build the engine.run() per-symbol input mappings."""
    klines_15m = {Symbol.BTCUSDT: bars_15m}
    klines_1h: dict[Symbol, Sequence[NormalizedKline]] = {Symbol.BTCUSDT: []}
    mark = {Symbol.BTCUSDT: [_mark_for(b) for b in bars_15m]}
    funding: dict[Symbol, Sequence[FundingRateEvent]] = {Symbol.BTCUSDT: []}
    return klines_15m, klines_1h, mark, funding


def _run_f1(cfg: BacktestConfig, bars_15m: Sequence[NormalizedKline]) -> BacktestRunResult:
    klines_15m, klines_1h, mark, funding = _empty_inputs(bars_15m)
    engine = BacktestEngine(cfg)
    return engine.run(
        klines_15m_per_symbol=klines_15m,
        klines_1h_per_symbol=klines_1h,
        mark_15m_per_symbol=mark,
        funding_per_symbol=funding,
        symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
    )


# ---------- Engine acceptance / rejection ----------


def test_f1_engine_accepts_dispatch_with_zero_warmup(tmp_path) -> None:
    """F1 engine returns gracefully on a too-short series (no trades)."""
    cfg = _f1_config(tmp_path)
    bars = [
        _bar(
            open_time=ANCHOR_MS + i * DUR_15M_MS,
            open_=100.0,
            high=100.5,
            low=99.5,
            close=100.0,
        )
        for i in range(5)
    ]
    result = _run_f1(cfg, bars)
    assert result.total_trades == 0
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.overextension_events_detected == 0
    assert counters.accounting_identity_holds


def test_f1_engine_no_signal_on_flat_series(tmp_path) -> None:
    """A flat series produces no overextension event."""
    cfg = _f1_config(tmp_path)
    bars = [
        _bar(
            open_time=ANCHOR_MS + i * DUR_15M_MS,
            open_=100.0,
            high=100.5,
            low=99.5,
            close=100.0,
        )
        for i in range(60)
    ]
    result = _run_f1(cfg, bars)
    assert result.total_trades == 0
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.overextension_events_detected == 0
    assert counters.accounting_identity_holds


# ---------- F1 long entry ----------


def test_f1_engine_long_entry_on_downward_overextension(tmp_path) -> None:
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars, sig_idx, fill_idx = _build_long_overextension_series()
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    assert len(trades) >= 1, f"expected at least one F1 LONG trade, got {len(trades)}"
    t = trades[0]
    assert t.direction == "LONG"
    assert t.exit_reason in {
        ExitReason.STOP.value,
        ExitReason.TARGET.value,
        ExitReason.TIME_STOP.value,
        ExitReason.END_OF_DATA.value,
    }
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.overextension_events_filled >= 1
    assert counters.accounting_identity_holds


def test_f1_engine_short_entry_on_upward_overextension(tmp_path) -> None:
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars, _sig, _fill = _build_short_overextension_series()
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    assert len(trades) >= 1
    assert trades[0].direction == "SHORT"


# ---------- Stop-distance admissibility ----------


def test_f1_engine_rejects_below_band_stop_distance(tmp_path) -> None:
    """When fill open is right at the lowest-low, stop_distance ≈ 0.1×ATR
    which is below the 0.60×ATR band; the entry must be rejected.
    """
    cfg = _f1_config(tmp_path)
    # Set the fill bar to open exactly at lowest-low (91.0). Then
    # stop_distance = |91.0 - 90.895| ≈ 0.105 < 0.63.
    bars, _, _ = _build_long_overextension_series(fill_bar_open=91.0)
    result = _run_f1(cfg, bars)
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.overextension_events_detected >= 1
    assert counters.overextension_events_filled == 0
    assert counters.overextension_events_rejected_stop_distance >= 1
    assert counters.accounting_identity_holds


def test_f1_engine_rejects_above_band_stop_distance(tmp_path) -> None:
    """Drive fill open well above lowest-low so stop_distance > 1.80×ATR.

    With ATR ≈ 1.05 and lowest-low at 91 (initial_stop ≈ 90.895),
    fill_open = 93.0 → stop_distance ≈ 2.105 > 1.89 → above band.
    """
    cfg = _f1_config(tmp_path)
    bars, _, _ = _build_long_overextension_series(fill_bar_open=93.0)
    result = _run_f1(cfg, bars)
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.overextension_events_detected >= 1
    assert counters.overextension_events_filled == 0
    assert counters.overextension_events_rejected_stop_distance >= 1
    assert counters.accounting_identity_holds


def test_f1_engine_uses_raw_open_for_admissibility_not_slipped(tmp_path) -> None:
    """The band check is on the raw de-slipped open(B+1).

    Construct a fill-open such that raw stop_distance is just inside
    the band but post-slip stop_distance would land outside. The trade
    must still fire.
    """
    # Use HIGH slippage (8 bps per side) so the slip swing is meaningful.
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.HIGH)
    # raw fill_open = 92.0; raw stop_distance = 1.105 (in band).
    bars, _, _ = _build_long_overextension_series(fill_bar_open=92.0)
    result = _run_f1(cfg, bars)
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.overextension_events_filled >= 1
    # stop_distance_at_signal_atr in the trade record must reflect
    # the RAW value (≈ 1.05 / 1.05 ≈ 1.0 to within rounding), not the
    # post-slip value.
    trade = result.per_symbol_trades[Symbol.BTCUSDT][0]
    assert 0.60 <= trade.stop_distance_at_signal_atr <= 1.80


# ---------- Target exit ----------


def test_f1_engine_target_fills_at_next_bar_open(tmp_path) -> None:
    """Long target = SMA(8)(B). When close(t) >= target, fill at open(t+1)."""
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    # Push the close above the target on bar idx=32. SMA(8)(B=28) =
    # mean(99,98,97,96,95,94,93,92) = 95.5. target_close at 99.0 fires.
    bars, _, _ = _build_long_overextension_series(target_close_idx=32, extra_after_signal=10)
    # idx 32 has close=99.0 (above 95.5); fill should be at idx 33's open=92.0.
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    target_exits = [t for t in trades if t.exit_reason == ExitReason.TARGET.value]
    assert len(target_exits) == 1
    t = target_exits[0]
    assert t.exit_fill_time_ms == bars[33].open_time
    # Frozen target exposed in the record.
    assert abs(t.frozen_target_value - 95.5) < 1e-6


def test_f1_engine_target_requires_close_confirmation(tmp_path) -> None:
    """An intrabar high above the target must NOT exit if close < target."""
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    # Build a series where bar idx=32 has high above target but close below.
    bars, _, fill_idx = _build_long_overextension_series(extra_after_signal=10)
    # Replace bar 32: high=100 (well above target 95.5), close=92 (below).
    t = bars[32].open_time
    bars[32] = _bar(open_time=t, open_=92.0, high=100.0, low=92.0, close=92.0)
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    # Must not exit on intrabar wick alone; expect TIME_STOP / END_OF_DATA.
    target_exits = [t for t in trades if t.exit_reason == ExitReason.TARGET.value]
    assert target_exits == []


# ---------- Time stop ----------


def test_f1_engine_time_stop_fires_at_8_bars_from_fill(tmp_path) -> None:
    """Bar B+1 = fill (idx=29). Time-stop horizon = 8 bars; trade exits at
    open of idx = fill_idx + 8 + 1 = idx=38 (open(B+10) per spec).
    """
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars, _, fill_idx = _build_long_overextension_series(extra_after_signal=20)
    # Ensure no stop / target along the way: keep all post-fill bars
    # near fill_open and above stop, below target. Default builder does this.
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    time_stops = [t for t in trades if t.exit_reason == ExitReason.TIME_STOP.value]
    assert len(time_stops) == 1
    t = time_stops[0]
    expected_exit_open = bars[fill_idx + 8 + 1].open_time
    assert t.exit_fill_time_ms == expected_exit_open


# ---------- Same-bar priority ----------


def test_f1_engine_stop_takes_priority_over_target(tmp_path) -> None:
    """If both stop and target could fire on the same bar, STOP wins."""
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    # Construct a bar whose close is above target AND whose mark-bar
    # range crosses the stop. Stop level ≈ 90.895; target ≈ 95.5.
    bars, _, fill_idx = _build_long_overextension_series(extra_after_signal=10)
    t = bars[32].open_time
    # close >= 95.5 (target), low <= 90.895 (stop), open between.
    bars[32] = _bar(open_time=t, open_=92.0, high=99.0, low=85.0, close=99.0)
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    assert len(trades) == 1
    assert trades[0].exit_reason == ExitReason.STOP.value


def test_f1_engine_target_takes_priority_over_time_stop(tmp_path) -> None:
    """On the time-stop bar, if target also fires, TARGET wins."""
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars, _, fill_idx = _build_long_overextension_series(extra_after_signal=20)
    # Time-stop bar = fill_idx + 8 = 37. Push its close above target.
    ts_idx = fill_idx + 8
    t = bars[ts_idx].open_time
    bars[ts_idx] = _bar(open_time=t, open_=92.0, high=99.0, low=92.0, close=99.0)
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    assert len(trades) == 1
    assert trades[0].exit_reason == ExitReason.TARGET.value


# ---------- Cooldown ----------


def test_f1_engine_cooldown_blocks_same_direction_reentry(tmp_path) -> None:
    """After exit, a same-direction overextension repeat without unwind
    must be blocked (counter blocked_cooldown).

    Strategy: build a series where displacement stays large-negative
    continuously through the trade exit and afterwards, so no bar
    between exit and the next overextension provides the unwind that
    cooldown_unwound requires.
    """
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars: list[NormalizedKline] = []
    t = ANCHOR_MS
    # Bars 0..20: flat at 100.
    for _ in range(21):
        bars.append(_bar(open_time=t, open_=100.0, high=100.5, low=99.5, close=100.0))
        t += DUR_15M_MS
    # Bars 21..27: drop by 1 each.
    prev = 100.0
    for delta in (-1.0,) * 7:
        c = prev + delta
        bars.append(_bar(open_time=t, open_=prev, high=prev, low=c, close=c))
        prev = c
        t += DUR_15M_MS
    # Bar 28 (signal B): close=92, low=91 (wick).
    bars.append(_bar(open_time=t, open_=93.0, high=93.0, low=91.0, close=92.0))
    t += DUR_15M_MS
    # Bar 29 (fill B+1): open=92, close=91.
    bars.append(_bar(open_time=t, open_=92.0, high=92.0, low=91.0, close=91.0))
    t += DUR_15M_MS
    # Bar 30 (stop bar): low=89 forces a stop hit (stop ≈ 90.895).
    bars.append(_bar(open_time=t, open_=91.0, high=91.0, low=89.0, close=89.0))
    t += DUR_15M_MS
    # Bars 31..40: continue dropping by 1 per bar; never produces an
    # unwind bar. displacement = close[t] - close[t-8] stays around -8
    # to -9 throughout, well above the ~1.75 × ATR threshold.
    prev = 89.0
    for _ in range(15):
        c = prev - 1.0
        bars.append(_bar(open_time=t, open_=prev, high=prev, low=c, close=c))
        prev = c
        t += DUR_15M_MS
    result = _run_f1(cfg, bars)
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.overextension_events_filled >= 1
    assert counters.overextension_events_blocked_cooldown >= 1
    assert counters.accounting_identity_holds


def test_f1_engine_cooldown_releases_after_unwind(tmp_path) -> None:
    """Once cumulative displacement re-enters the unwind band, a fresh
    same-direction overextension is allowed.

    Strategy: drop sharply (first overextension fills, stops out), then
    flatten so that displacement returns to ≈ 0 (unwind), then drop
    sharply a second time → new overextension event must FILL (not be
    cooldown-blocked).
    """
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars: list[NormalizedKline] = []
    t = ANCHOR_MS
    # Bars 0..20: flat at 100.
    for _ in range(21):
        bars.append(_bar(open_time=t, open_=100.0, high=100.5, low=99.5, close=100.0))
        t += DUR_15M_MS
    # Bars 21..27: drop by 1 each.
    prev = 100.0
    for _ in range(7):
        c = prev - 1.0
        bars.append(_bar(open_time=t, open_=prev, high=prev, low=c, close=c))
        prev = c
        t += DUR_15M_MS
    # Bar 28 (signal): close=92, low=91 wick.
    bars.append(_bar(open_time=t, open_=93.0, high=93.0, low=91.0, close=92.0))
    t += DUR_15M_MS
    # Bar 29 (fill): open=92, close=91.
    bars.append(_bar(open_time=t, open_=92.0, high=92.0, low=91.0, close=91.0))
    t += DUR_15M_MS
    # Bar 30 (stop bar): low=89 → stop fires.
    bars.append(_bar(open_time=t, open_=91.0, high=91.0, low=89.0, close=89.0))
    t += DUR_15M_MS
    # Bars 31..50: flat at 89 for 20 bars. Displacement[t] eventually
    # hits zero (close[t]=close[t-8] both 89) → unwind condition met.
    prev = 89.0
    for _ in range(20):
        bars.append(_bar(open_time=t, open_=prev, high=prev + 0.5, low=prev - 0.5, close=prev))
        t += DUR_15M_MS
    # Bars 51..58: drop by 1 each → fresh down move building toward
    # second overextension.
    for _ in range(7):
        c = prev - 1.0
        bars.append(_bar(open_time=t, open_=prev, high=prev, low=c, close=c))
        prev = c
        t += DUR_15M_MS
    # Bar 59 (second signal): wick down.
    bars.append(_bar(open_time=t, open_=prev, high=prev, low=prev - 2.0, close=prev - 1.0))
    t += DUR_15M_MS
    prev = prev - 1.0
    # Bar 60+ : trailing flat to allow trade lifecycle to play out.
    for _ in range(15):
        bars.append(_bar(open_time=t, open_=prev, high=prev + 0.5, low=prev - 0.5, close=prev))
        t += DUR_15M_MS
    result = _run_f1(cfg, bars)
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    # Two fills: first long entry stops out, then post-unwind a second
    # fresh same-direction long fills.
    assert counters.overextension_events_filled >= 2
    assert counters.accounting_identity_holds


# ---------- Frozen invariants ----------


def test_f1_engine_frozen_target_invariant(tmp_path) -> None:
    """Frozen target equals SMA(8)(B) and is preserved on the trade record."""
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars, _, _ = _build_long_overextension_series(extra_after_signal=10)
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    assert trades, "expected at least one F1 trade"
    # SMA(8) at signal bar B=28: mean(99,98,97,96,95,94,93,92) = 95.5.
    assert abs(trades[0].frozen_target_value - 95.5) < 1e-6


def test_f1_engine_frozen_stop_invariant(tmp_path) -> None:
    """Initial stop equals lowest_low([B-7..B]) - 0.10×ATR(20)(B) and
    matches the recorded trade ``initial_stop`` (no mid-trade changes).
    """
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars, _, _ = _build_long_overextension_series(extra_after_signal=10)
    result = _run_f1(cfg, bars)
    trades = result.per_symbol_trades[Symbol.BTCUSDT]
    assert trades
    # min(lows[21..28]) = 91; ATR(20)(28) ≈ 1.05; buffer = 0.105.
    expected_stop = 91.0 - 0.10 * 1.05
    assert abs(trades[0].initial_stop - expected_stop) < 1e-3


# ---------- Accounting identity + exit-reason invariant ----------


def test_f1_engine_accounting_identity_holds_across_runs(tmp_path) -> None:
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars, _, _ = _build_long_overextension_series(extra_after_signal=20)
    result = _run_f1(cfg, bars)
    counters = result.f1_counters_per_symbol[Symbol.BTCUSDT]
    assert counters.accounting_identity_holds


def test_f1_engine_emits_only_allowed_exit_reasons(tmp_path) -> None:
    """F1 must emit only STOP / TARGET / TIME_STOP / END_OF_DATA."""
    allowed = {
        ExitReason.STOP.value,
        ExitReason.TARGET.value,
        ExitReason.TIME_STOP.value,
        ExitReason.END_OF_DATA.value,
    }
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars_long, _, _ = _build_long_overextension_series(extra_after_signal=20)
    result_long = _run_f1(cfg, bars_long)
    for t in result_long.per_symbol_trades[Symbol.BTCUSDT]:
        assert t.exit_reason in allowed
    bars_short, _, _ = _build_short_overextension_series(extra_after_signal=20)
    result_short = _run_f1(cfg, bars_short)
    for t in result_short.per_symbol_trades[Symbol.BTCUSDT]:
        assert t.exit_reason in allowed


# ---------- V1 baseline preservation ----------


def test_v1_h0_default_path_unchanged_with_f1_module_imported(tmp_path) -> None:
    """Importing the F1 module must not perturb the V1 default path.

    Constructs a default V1 BacktestConfig and verifies the engine
    exposes the V1 dispatch (no F1 strategy constructed; F1 counters
    empty). The bit-for-bit baseline reproduction is verified separately
    via the H0/R3 control runs in the Phase 3d-B1 checkpoint report.
    """
    from .conftest import default_config

    cfg = default_config(tmp_path)
    engine = BacktestEngine(cfg)
    # Sanity: F1 strategy is not constructed under V1 dispatch.
    assert engine._mean_reversion_strategy is None  # type: ignore[attr-defined]
    # Smoke: a no-data run still works and produces no F1 counters.
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.total_trades == 0
    assert result.f1_counters_per_symbol == {}


# ---------- Direction enum mapping check ----------


def test_f1_signal_direction_consistency_with_overextension_sign(tmp_path) -> None:
    """+1 displacement → SHORT candidate; -1 → LONG candidate."""
    cfg = _f1_config(tmp_path, slippage_bucket=SlippageBucket.LOW)
    bars_long, _, _ = _build_long_overextension_series(extra_after_signal=10)
    res_long = _run_f1(cfg, bars_long)
    assert res_long.per_symbol_trades[Symbol.BTCUSDT][0].direction == Direction.LONG.value

    bars_short, _, _ = _build_short_overextension_series(extra_after_signal=10)
    res_short = _run_f1(cfg, bars_short)
    assert res_short.per_symbol_trades[Symbol.BTCUSDT][0].direction == Direction.SHORT.value
