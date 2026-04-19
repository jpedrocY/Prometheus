"""Manufactured synthetic fixture that deliberately produces a valid
v1 breakout signal and exercises the full positive trade path:

    bias LONG -> valid 8-bar setup -> breakout signal (all 6 conditions)
      -> stop-distance filter passes -> sizing approves -> entry fills
      on next bar open -> management runs -> stagnation exit at bar 8
      -> exit fills on next bar open -> trade_log + equity_curve +
      drawdown + r_multiple_hist + summary_metrics + manifest written.

Every numeric choice is a FIXTURE construction detail. The strategy
thresholds, sizing constants, and filter multipliers are NOT altered;
this test is structurally identical to the real engine path — only
the inputs are arranged to satisfy the v1 filters.

This complements ``test_backtest_synthetic_end_to_end.py`` (which
verifies the pipeline runs cleanly on a fixture that happens to
produce 0 trades) and closes the Gate 2 operator-requested evidence
gap: "does the engine actually produce a closed trade + artifacts on
the full path?"
"""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow.parquet as pq

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.symbols import Symbol
from prometheus.research.backtest import (
    BacktestConfig,
    BacktestEngine,
    SlippageBucket,
    run_signal_funnel,
)
from prometheus.research.backtest.config import DEFAULT_SLIPPAGE_BPS
from prometheus.research.backtest.report import DatasetCitation, write_report
from tests.unit.research.backtest.conftest import default_symbol_info
from tests.unit.strategy.conftest import ANCHOR_MS, kline, mark

# --- Fixture construction --------------------------------------------------
#
# Phase 1 (warmup): 900 15m bars of gentle +0.01%/bar drift. Produces
# ~225 completed 1h bars, enough for EMA(200)+slope warmup. Each 15m
# bar has a wide enough hi/lo spread to keep the 15m ATR around
# 0.21% of price, which implies a 1h normalized ATR in the
# [0.20%, 2.00%] regime band by the time the breakout fires.
#
# Phase 2 (compression): 8 15m bars with a tight range (~24 price
# units) and near-zero net drift, designed to satisfy
#   setup_range_width <= 1.75 * ATR(20)_15m
#   abs(close[-1] - open[0]) <= 0.35 * range
#
# Phase 3 (breakout bar): 1 15m bar whose close is beyond
# setup_high + 0.10*ATR, whose true range exceeds ATR, and whose
# close sits at the bar's high (top-25% location). The upward body
# is sized so stop_distance lands inside [0.60, 1.80] * ATR.
#
# Phase 4 (post-breakout): 10 15m bars that stay near entry so MFE
# never reaches +1R, forcing a Stage-7 stagnation exit at
# bars_in_trade=8 and an exit fill on bar 9 after entry.

WARMUP_BARS = 900
CONSOLIDATION_BARS = 8
POST_BREAKOUT_BARS = 10


def _make_trade_path_fixture(
    symbol: Symbol = Symbol.BTCUSDT,
):
    bars_15m = []
    bars_1h = []
    mark_15m = []
    d15 = interval_duration_ms(Interval.I_15M)
    d1h = interval_duration_ms(Interval.I_1H)

    # Phase 1: warmup
    t = ANCHOR_MS
    price = 50_000.0
    for _ in range(WARMUP_BARS):
        o = price
        c = price * 1.0001  # +0.01% per bar
        hi = c * 1.001
        lo = o * 0.999
        bars_15m.append(kline(symbol=symbol, open_time=t, open=o, high=hi, low=lo, close=c))
        mark_15m.append(mark(symbol=symbol, open_time=t, open=o, high=hi, low=lo, close=c))
        t += d15
        price = c

    # Phase 2: 8-bar consolidation around `price`
    center = price
    for i in range(CONSOLIDATION_BARS):
        o = center + ((-1) ** i) * 2.0
        c = center + ((-1) ** (i + 1)) * 2.0
        hi = center + 12.0
        lo = center - 12.0
        hi = max(hi, o, c)
        lo = min(lo, o, c)
        bars_15m.append(kline(symbol=symbol, open_time=t, open=o, high=hi, low=lo, close=c))
        mark_15m.append(mark(symbol=symbol, open_time=t, open=o, high=hi, low=lo, close=c))
        t += d15

    # Phase 3: breakout bar (close at high, 125-unit upward body)
    b_open = center
    b_close = center + 120.0
    b_high = b_close
    b_low = b_open - 5.0
    bars_15m.append(
        kline(symbol=symbol, open_time=t, open=b_open, high=b_high, low=b_low, close=b_close)
    )
    mark_15m.append(
        mark(symbol=symbol, open_time=t, open=b_open, high=b_high, low=b_low, close=b_close)
    )
    t += d15

    # Phase 4: quiet post-breakout bars (MFE stays below +1R -> stagnation)
    post = b_close
    for i in range(POST_BREAKOUT_BARS):
        o = post
        c = post + ((-1) ** i) * 2.0
        hi = max(o, c) + 5.0
        lo = min(o, c) - 5.0
        bars_15m.append(kline(symbol=symbol, open_time=t, open=o, high=hi, low=lo, close=c))
        mark_15m.append(mark(symbol=symbol, open_time=t, open=o, high=hi, low=lo, close=c))
        t += d15
        post = c

    # Aggregate 15m -> 1h by grouping 4 consecutive 15m bars per hour.
    total_15m = len(bars_15m)
    n_1h = total_15m // 4
    for h in range(n_1h):
        group = bars_15m[h * 4 : (h + 1) * 4]
        bars_1h.append(
            kline(
                symbol=symbol,
                interval=Interval.I_1H,
                open_time=ANCHOR_MS + h * d1h,
                open=group[0].open,
                high=max(b.high for b in group),
                low=min(b.low for b in group),
                close=group[-1].close,
            )
        )
    return bars_15m, bars_1h, mark_15m


def _build_config(tmp_path: Path, klines_15m) -> BacktestConfig:
    return BacktestConfig(
        experiment_name="phase-3-manufactured",
        run_id="r-0001",
        symbols=(Symbol.BTCUSDT,),
        window_start_ms=ANCHOR_MS,
        window_end_ms=klines_15m[-1].close_time + 1,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=SlippageBucket.MEDIUM,
        slippage_bps_map=dict(DEFAULT_SLIPPAGE_BPS),
        klines_root=tmp_path / "k",
        mark_price_root=tmp_path / "m",
        funding_root=tmp_path / "f",
        bars_1h_root=tmp_path / "h",
        exchange_info_path=tmp_path / "ei.json",
        reports_root=tmp_path / "reports",
    )


# --------------------------------------------------------------------------


def test_manufactured_breakout_produces_filled_closed_trade(tmp_path: Path) -> None:
    """End-to-end: engine takes the manufactured scenario, fills, and closes."""
    k15, k1h, m15 = _make_trade_path_fixture()
    cfg = _build_config(tmp_path, k15)

    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={Symbol.BTCUSDT: k15},
        klines_1h_per_symbol={Symbol.BTCUSDT: k1h},
        mark_15m_per_symbol={Symbol.BTCUSDT: m15},
        funding_per_symbol={Symbol.BTCUSDT: []},
        symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
    )
    assert not result.warnings, f"unexpected warnings: {result.warnings}"
    trades = result.per_symbol_trades.get(Symbol.BTCUSDT, [])
    assert len(trades) >= 1, "manufactured fixture failed to produce a filled trade"
    t = trades[0]
    assert t.direction == "LONG"
    assert t.quantity > 0
    assert t.entry_fill_time_ms > 0
    assert t.exit_fill_time_ms >= t.entry_fill_time_ms
    assert t.exit_reason in {"STAGNATION", "STOP", "TRAILING_BREACH", "END_OF_DATA"}


def test_manufactured_breakout_produces_report_artifacts(tmp_path: Path) -> None:
    """End-to-end: report writer emits per-symbol Parquet + JSON + manifest."""
    k15, k1h, m15 = _make_trade_path_fixture()
    cfg = _build_config(tmp_path, k15)

    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={Symbol.BTCUSDT: k15},
        klines_1h_per_symbol={Symbol.BTCUSDT: k1h},
        mark_15m_per_symbol={Symbol.BTCUSDT: m15},
        funding_per_symbol={Symbol.BTCUSDT: []},
        symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
    )
    assert result.total_trades >= 1

    run_dir = write_report(
        config=cfg,
        trades_by_symbol=result.per_symbol_trades,
        accounting_by_symbol=result.accounting_per_symbol,
        dataset_citations=[
            DatasetCitation(
                dataset_name="manufactured-synthetic",
                dataset_version=None,
                notes="in-memory fixture; not persisted",
            )
        ],
        accepted_limitations=["synthetic trade-path fixture; not a real-market result"],
        dest_root=tmp_path / "reports",
    )
    assert (run_dir / "backtest_report.manifest.json").is_file()
    assert (run_dir / "config_snapshot.json").is_file()

    sym_dir = run_dir / "BTCUSDT"
    assert sym_dir.is_dir()
    assert (sym_dir / "trade_log.parquet").is_file()
    assert (sym_dir / "trade_log.json").is_file()
    assert (sym_dir / "equity_curve.parquet").is_file()
    assert (sym_dir / "drawdown.parquet").is_file()
    assert (sym_dir / "r_multiple_hist.parquet").is_file()
    assert (sym_dir / "summary_metrics.json").is_file()

    # Parquet sanity: trade_log has at least one row with matching schema.
    table = pq.read_table(sym_dir / "trade_log.parquet")
    assert table.num_rows >= 1
    row = table.to_pylist()[0]
    assert row["symbol"] == "BTCUSDT"
    assert row["direction"] == "LONG"
    assert row["quantity"] > 0
    assert row["exit_fill_time_ms"] >= row["entry_fill_time_ms"]

    # Summary metrics sanity.
    metrics = json.loads((sym_dir / "summary_metrics.json").read_text())
    assert metrics["trade_count"] >= 1
    assert metrics["long_count"] >= 1


def test_manufactured_fixture_signal_funnel_reaches_entry_intent(tmp_path: Path) -> None:
    """Verify via the diagnostic that the manufactured fixture actually
    clears every filter stage — the entry_intents counter must reach 1."""
    k15, k1h, _ = _make_trade_path_fixture()
    cfg = _build_config(tmp_path, k15)

    counts = run_signal_funnel(
        symbol=Symbol.BTCUSDT,
        klines_15m=k15,
        klines_1h=k1h,
        symbol_info=default_symbol_info(),
        config=cfg,
    )
    assert counts.bias_long_count > 0, "warmup fixture failed to produce LONG bias"
    assert counts.valid_setup_windows_detected >= 1
    assert counts.long_breakout_candidates >= 1
    assert counts.rejected_stop_distance_filter_failed == 0
    assert counts.rejected_sizing_failed == 0
    assert counts.entry_intents_produced >= 1
    assert counts.trades_filled >= 1
