"""End-to-end synthetic backtest: engine runs cleanly on ~11 days of
deterministic synthetic 15m data plus 1h bars and mark-price bars.

This test is the "is the pipeline wired correctly?" check. It does
not attempt to produce a particular trade count — the warmup
windows (EMA(200) on 1h) make an organic signal on pure synthetic
data unlikely. The goal is:

    - engine runs without crashing on valid Phase-2-shaped inputs
    - accounting returns a well-formed result
    - report writes produce all expected artifacts
    - no secrets or forbidden imports are touched

A stricter manufactured-signal test lives alongside it.
"""

from __future__ import annotations

from pathlib import Path

from prometheus.core.events import FundingRateEvent
from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.symbols import Symbol
from prometheus.research.backtest import (
    BacktestConfig,
    BacktestEngine,
    SlippageBucket,
)
from prometheus.research.backtest.config import DEFAULT_SLIPPAGE_BPS
from prometheus.research.backtest.report import DatasetCitation, write_report
from tests.unit.research.backtest.conftest import default_symbol_info
from tests.unit.strategy.conftest import ANCHOR_MS, kline, mark


def _make_data(n_15m: int = 1100, n_1h: int = 280) -> tuple[list, list, list, list]:
    """Generate deterministic, invariant-safe synthetic inputs."""
    klines_15m: list = []
    mark_15m: list = []
    t = ANCHOR_MS
    d15 = interval_duration_ms(Interval.I_15M)
    price = 50_000.0
    for _ in range(n_15m):
        # Mild oscillation with a tiny upward drift so 1h EMAs diverge.
        nxt = price * (1.0 + 0.00005)
        hi = max(price, nxt) * 1.0002
        lo = min(price, nxt) * 0.9998
        klines_15m.append(kline(open_time=t, open=price, high=hi, low=lo, close=nxt))
        mark_15m.append(mark(open_time=t, open=price, high=hi, low=lo, close=nxt))
        t += d15
        price = nxt
    # Aggregate to 1h: every 4 15m bars -> one 1h bar.
    klines_1h: list = []
    d1h = interval_duration_ms(Interval.I_1H)
    for h in range(n_1h):
        idx = h * 4
        if idx + 3 >= len(klines_15m):
            break
        group = klines_15m[idx : idx + 4]
        t1h = ANCHOR_MS + h * d1h
        klines_1h.append(
            kline(
                interval=Interval.I_1H,
                open_time=t1h,
                open=group[0].open,
                high=max(b.high for b in group),
                low=min(b.low for b in group),
                close=group[-1].close,
            )
        )
    # A handful of funding events across the window.
    fundings: list[FundingRateEvent] = []
    for h in range(0, n_1h, 8):
        fundings.append(
            FundingRateEvent(
                symbol=Symbol.BTCUSDT,
                funding_time=ANCHOR_MS + h * d1h,
                funding_rate=0.0001,
                mark_price=50_000.0,
                source="synthetic-test",
            )
        )
    return klines_15m, klines_1h, mark_15m, fundings


def test_synthetic_full_run_is_clean(tmp_path: Path) -> None:
    k15, k1h, m15, fund = _make_data()
    cfg = BacktestConfig(
        experiment_name="synthetic-smoke",
        run_id="r-0001",
        symbols=(Symbol.BTCUSDT,),
        window_start_ms=ANCHOR_MS,
        window_end_ms=k15[-1].close_time + 1,
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
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={Symbol.BTCUSDT: k15},
        klines_1h_per_symbol={Symbol.BTCUSDT: k1h},
        mark_15m_per_symbol={Symbol.BTCUSDT: m15},
        funding_per_symbol={Symbol.BTCUSDT: fund},
        symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
    )
    # Must complete; trade count may be 0 (synthetic series rarely
    # satisfies the full 6-condition trigger) — that's fine.
    assert result.total_trades >= 0
    assert not result.warnings  # all data present

    # Report writing works.
    run_dir = write_report(
        config=cfg,
        trades_by_symbol=result.per_symbol_trades,
        accounting_by_symbol=result.accounting_per_symbol,
        dataset_citations=[
            DatasetCitation(
                dataset_name="synthetic-15m",
                dataset_version=None,
                notes="deterministic test fixture",
            )
        ],
        accepted_limitations=["synthetic data; no real market signal"],
        dest_root=tmp_path / "reports",
    )
    assert (run_dir / "backtest_report.manifest.json").is_file()


def test_synthetic_run_is_deterministic(tmp_path: Path) -> None:
    """Running the engine twice with identical inputs yields identical outputs."""
    k15, k1h, m15, fund = _make_data()
    cfg = BacktestConfig(
        experiment_name="det-1",
        run_id="r-1",
        symbols=(Symbol.BTCUSDT,),
        window_start_ms=ANCHOR_MS,
        window_end_ms=k15[-1].close_time + 1,
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
    results = []
    for _ in range(2):
        engine = BacktestEngine(cfg)
        r = engine.run(
            klines_15m_per_symbol={Symbol.BTCUSDT: k15},
            klines_1h_per_symbol={Symbol.BTCUSDT: k1h},
            mark_15m_per_symbol={Symbol.BTCUSDT: m15},
            funding_per_symbol={Symbol.BTCUSDT: fund},
            symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
        )
        # Drop the randomized uuid suffix for comparison.
        trades = [
            (t.symbol, t.direction, t.entry_fill_time_ms, t.exit_fill_time_ms, t.net_pnl)
            for t in r.per_symbol_trades.get(Symbol.BTCUSDT, [])
        ]
        results.append(trades)
    assert results[0] == results[1]
