"""Operator-facing Phase 3 smoke-run script (one-off, not committed to CI).

Runs the full backtester on real 2026-03 BTCUSDT + ETHUSDT data and
writes a report under ``data/derived/backtests/phase-3-smoke/<run_id>/``.

Usage::

    uv run python scripts/phase3_smoke_run.py

Not committed — this script is written explicitly for the Gate 2
real-data smoke check per Phase 3 Gate 1 condition A and may be
removed or rewritten in later phases.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from prometheus.core.exchange_info import ExchangeInfoSnapshot
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.backtest import (
    BacktestConfig,
    BacktestEngine,
    SlippageBucket,
    run_signal_funnel,
)
from prometheus.research.backtest.config import DEFAULT_SLIPPAGE_BPS
from prometheus.research.backtest.report import DatasetCitation, write_report
from prometheus.research.data.storage import (
    read_funding_rate_events,
    read_klines,
    read_mark_price_klines,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"


def _load_symbol_info(ei_path: Path, symbol: Symbol):  # type: ignore[no-untyped-def]
    snap = ExchangeInfoSnapshot.model_validate(json.loads(ei_path.read_text()))
    for si in snap.symbols:
        if si.symbol == symbol.value:
            return si
    raise RuntimeError(f"{symbol.value} not in exchangeInfo snapshot at {ei_path}")


def main() -> None:
    ei_candidates = sorted((DATA_ROOT / "derived" / "exchange_info").glob("*.json"))
    if not ei_candidates:
        raise SystemExit("No exchangeInfo snapshot found under data/derived/exchange_info/")
    ei_path = ei_candidates[-1]
    klines_root = DATA_ROOT / "normalized" / "klines"
    bars_1h_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    mark_root = DATA_ROOT / "normalized" / "mark_price_klines"
    funding_root = DATA_ROOT / "normalized" / "funding_rate"

    symbols = (Symbol.BTCUSDT, Symbol.ETHUSDT)
    k15: dict = {}
    k1h: dict = {}
    m15: dict = {}
    fund: dict = {}
    si_map: dict = {}
    for s in symbols:
        k15[s] = read_klines(klines_root, symbol=s, interval=Interval.I_15M)
        k1h[s] = read_klines(bars_1h_root, symbol=s, interval=Interval.I_1H)
        m15[s] = read_mark_price_klines(mark_root, symbol=s, interval=Interval.I_15M)
        fund[s] = read_funding_rate_events(funding_root, symbol=s)
        si_map[s] = _load_symbol_info(ei_path, s)

    if not k15[Symbol.BTCUSDT] or not k15[Symbol.ETHUSDT]:
        raise SystemExit("Real 2026-03 data missing; populate data/ via Phase 2b/2c first.")

    window_start = min(k15[s][0].open_time for s in symbols)
    window_end = max(k15[s][-1].close_time for s in symbols) + 1

    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    cfg = BacktestConfig(
        experiment_name="phase-3-smoke",
        run_id=run_id,
        symbols=symbols,
        window_start_ms=window_start,
        window_end_ms=window_end,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=SlippageBucket.MEDIUM,
        slippage_bps_map=dict(DEFAULT_SLIPPAGE_BPS),
        klines_root=klines_root,
        bars_1h_root=bars_1h_root,
        mark_price_root=mark_root,
        funding_root=funding_root,
        exchange_info_path=ei_path,
        reports_root=DATA_ROOT / "derived" / "backtests",
    )

    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol=k15,
        klines_1h_per_symbol=k1h,
        mark_15m_per_symbol=m15,
        funding_per_symbol=fund,
        symbol_info_per_symbol=si_map,
    )

    citations: list[DatasetCitation] = []
    for sym in symbols:
        ds_name = f"binance_usdm_{sym.value.lower()}_15m"
        manifest_path = DATA_ROOT / "manifests" / f"{ds_name}__v001.manifest.json"
        citations.append(
            DatasetCitation(
                dataset_name=ds_name,
                dataset_version=f"{ds_name}__v001",
                manifest_path=str(manifest_path),
            )
        )
    citations.append(
        DatasetCitation(
            dataset_name="exchange_info_snapshot",
            raw_file_path=str(ei_path),
            notes="GAP-20260419-020: 2026-04-19 snapshot used as 2026-03 proxy.",
        )
    )
    accepted_limits = [
        "GAP-018 + GAP-024: taker fee placeholder; commissionRate deferred to Phase 2d.",
        "GAP-020: exchangeInfo snapshot 2026-04-19 used as proxy for 2026-03 window.",
        "GAP-025: single-month window; insufficient for walk-forward / robustness gates.",
    ]
    run_dir = write_report(
        config=cfg,
        trades_by_symbol=result.per_symbol_trades,
        accounting_by_symbol=result.accounting_per_symbol,
        dataset_citations=citations,
        accepted_limitations=accepted_limits,
        dest_root=DATA_ROOT / "derived" / "backtests",
    )
    print(f"Run written to: {run_dir}")
    print(f"Total trades (all symbols): {result.total_trades}")
    for s in symbols:
        acc = result.accounting_per_symbol.get(s)
        trades = result.per_symbol_trades.get(s, [])
        if acc is None:
            continue
        print(
            f"  {s.value}: {len(trades)} trades | equity {acc.equity:.2f} | "
            f"realized PnL {acc.realized_pnl:+.2f}"
        )

    # Signal-funnel diagnostic (research-only; does not change strategy).
    print("")
    print("=" * 72)
    print("Signal-funnel diagnostic (no thresholds changed; no tuning)")
    print("=" * 72)
    for s in symbols:
        funnel = run_signal_funnel(
            symbol=s,
            klines_15m=k15[s],
            klines_1h=k1h[s],
            symbol_info=si_map[s],
            config=cfg,
        )
        print(funnel.summary())
        print("")


if __name__ == "__main__":
    main()
