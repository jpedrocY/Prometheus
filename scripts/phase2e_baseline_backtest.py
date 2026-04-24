"""Phase 2e baseline backtest runner.

Runs the locked Phase 3 v1 breakout strategy over the widened
2022-01 through 2026-03 BTCUSDT + ETHUSDT datasets produced by
``scripts/phase2e_backfill.py``. Emits the full Phase 3 artifact
bundle per symbol plus two new breakdown artifacts
(``monthly_breakdown.parquet``, ``yearly_breakdown.parquet``) and
per-(symbol, year, month) signal-funnel counts.

Per Phase 2e Gate 1 + operator approvals:

  - Locked Phase 3 defaults ONLY. No tuning. No threshold changes.
  - risk_fraction=0.0025, risk_usage=0.90, max_leverage=2.0,
    max_notional=100_000, taker=0.0005, slippage=MEDIUM, adapter=FAKE.
  - No sensitivity variants. No profitability or live-readiness
    claims in the output.
  - Backtest artifacts under data/derived/backtests/phase-2e-baseline/
    are git-ignored.

Usage::

    uv run python scripts/phase2e_baseline_backtest.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from prometheus.core.exchange_info import ExchangeInfoSnapshot
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.backtest import (
    BacktestConfig,
    BacktestEngine,
    SignalFunnelCounts,
    SlippageBucket,
    run_signal_funnel,
)
from prometheus.research.backtest.config import DEFAULT_SLIPPAGE_BPS
from prometheus.research.backtest.report import DatasetCitation, write_report
from prometheus.research.backtest.trade_log import TradeRecord
from prometheus.research.data.storage import (
    read_funding_rate_events,
    read_klines,
    read_mark_price_klines,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"

SYMBOLS = (Symbol.BTCUSDT, Symbol.ETHUSDT)

# Window: 2022-01-01 00:00:00 UTC through 2026-04-01 00:00:00 UTC (exclusive)
WINDOW_START_MS = 1_640_995_200_000
WINDOW_END_MS = 1_775_001_600_000


def _banner(title: str) -> None:
    bar = "=" * 72
    print(f"\n{bar}\n{title}\n{bar}")


def _exchange_info_path() -> Path:
    candidates = sorted((DATA_ROOT / "derived" / "exchange_info").glob("*.json"))
    if not candidates:
        raise RuntimeError("No exchangeInfo snapshot under data/derived/exchange_info/")
    return candidates[-1]


def _load_symbol_info(ei_path: Path, symbol: Symbol):  # type: ignore[no-untyped-def]
    snap = ExchangeInfoSnapshot.model_validate(json.loads(ei_path.read_text()))
    for si in snap.symbols:
        if si.symbol == symbol.value:
            return si
    raise RuntimeError(f"{symbol.value} not in exchangeInfo snapshot {ei_path}")


def _ym_for_ms(ms: int) -> tuple[int, int]:
    """Return (year, month) UTC for a UTC-ms timestamp."""
    dt = datetime.fromtimestamp(ms / 1000.0, tz=UTC)
    return dt.year, dt.month


# ---------------------------------------------------------------------------
# Aggregators (kept in this script per Gate-1 §11 D3 Option A)
# ---------------------------------------------------------------------------


def _aggregate_trades_by_month(trades: list[TradeRecord]) -> pa.Table:
    """Per-(year, month) rollup of trade count, wins, losses, net PnL, etc."""
    by_ym: dict[tuple[int, int], dict[str, float | int]] = defaultdict(
        lambda: {
            "trade_count": 0,
            "win_count": 0,
            "loss_count": 0,
            "long_count": 0,
            "short_count": 0,
            "stop_exits": 0,
            "trailing_exits": 0,
            "stagnation_exits": 0,
            "end_of_data_exits": 0,
            "gross_pnl": 0.0,
            "net_pnl": 0.0,
            "fees": 0.0,
            "funding": 0.0,
            "sum_r": 0.0,
        }
    )
    for t in trades:
        ym = _ym_for_ms(t.exit_fill_time_ms)
        row = by_ym[ym]
        row["trade_count"] = int(row["trade_count"]) + 1
        if t.net_pnl > 0:
            row["win_count"] = int(row["win_count"]) + 1
        elif t.net_pnl < 0:
            row["loss_count"] = int(row["loss_count"]) + 1
        if t.direction == "LONG":
            row["long_count"] = int(row["long_count"]) + 1
        else:
            row["short_count"] = int(row["short_count"]) + 1
        if t.exit_reason == "STOP":
            row["stop_exits"] = int(row["stop_exits"]) + 1
        elif t.exit_reason == "TRAILING_BREACH":
            row["trailing_exits"] = int(row["trailing_exits"]) + 1
        elif t.exit_reason == "STAGNATION":
            row["stagnation_exits"] = int(row["stagnation_exits"]) + 1
        elif t.exit_reason == "END_OF_DATA":
            row["end_of_data_exits"] = int(row["end_of_data_exits"]) + 1
        row["gross_pnl"] = float(row["gross_pnl"]) + t.gross_pnl
        row["net_pnl"] = float(row["net_pnl"]) + t.net_pnl
        row["fees"] = float(row["fees"]) + t.entry_fee + t.exit_fee
        row["funding"] = float(row["funding"]) + t.funding_pnl
        row["sum_r"] = float(row["sum_r"]) + t.net_r_multiple

    rows = []
    for (y, m), agg in sorted(by_ym.items()):
        tc = int(agg["trade_count"])
        row = {
            "year": y,
            "month": m,
            **{k: v for k, v in agg.items()},
            "avg_r": float(agg["sum_r"]) / tc if tc > 0 else 0.0,
        }
        rows.append(row)
    if not rows:
        return pa.table({"year": pa.array([], type=pa.int32())})
    columns = {k: [r[k] for r in rows] for k in rows[0]}
    return pa.table(columns)


def _aggregate_trades_by_year(trades: list[TradeRecord]) -> pa.Table:
    by_y: dict[int, dict[str, float | int]] = defaultdict(
        lambda: {
            "trade_count": 0,
            "win_count": 0,
            "loss_count": 0,
            "long_count": 0,
            "short_count": 0,
            "stop_exits": 0,
            "trailing_exits": 0,
            "stagnation_exits": 0,
            "end_of_data_exits": 0,
            "gross_pnl": 0.0,
            "net_pnl": 0.0,
            "fees": 0.0,
            "funding": 0.0,
            "sum_r": 0.0,
        }
    )
    for t in trades:
        y, _ = _ym_for_ms(t.exit_fill_time_ms)
        row = by_y[y]
        row["trade_count"] = int(row["trade_count"]) + 1
        if t.net_pnl > 0:
            row["win_count"] = int(row["win_count"]) + 1
        elif t.net_pnl < 0:
            row["loss_count"] = int(row["loss_count"]) + 1
        if t.direction == "LONG":
            row["long_count"] = int(row["long_count"]) + 1
        else:
            row["short_count"] = int(row["short_count"]) + 1
        if t.exit_reason == "STOP":
            row["stop_exits"] = int(row["stop_exits"]) + 1
        elif t.exit_reason == "TRAILING_BREACH":
            row["trailing_exits"] = int(row["trailing_exits"]) + 1
        elif t.exit_reason == "STAGNATION":
            row["stagnation_exits"] = int(row["stagnation_exits"]) + 1
        elif t.exit_reason == "END_OF_DATA":
            row["end_of_data_exits"] = int(row["end_of_data_exits"]) + 1
        row["gross_pnl"] = float(row["gross_pnl"]) + t.gross_pnl
        row["net_pnl"] = float(row["net_pnl"]) + t.net_pnl
        row["fees"] = float(row["fees"]) + t.entry_fee + t.exit_fee
        row["funding"] = float(row["funding"]) + t.funding_pnl
        row["sum_r"] = float(row["sum_r"]) + t.net_r_multiple

    rows = []
    for y, agg in sorted(by_y.items()):
        tc = int(agg["trade_count"])
        row = {
            "year": y,
            **{k: v for k, v in agg.items()},
            "avg_r": float(agg["sum_r"]) / tc if tc > 0 else 0.0,
        }
        rows.append(row)
    if not rows:
        return pa.table({"year": pa.array([], type=pa.int32())})
    columns = {k: [r[k] for r in rows] for k in rows[0]}
    return pa.table(columns)


def _funnel_summary_dict(c: SignalFunnelCounts) -> dict[str, int]:
    return {
        "total_15m_bars_loaded": c.total_15m_bars_loaded,
        "total_1h_bars_loaded": c.total_1h_bars_loaded,
        "warmup_15m_bars_excluded": c.warmup_15m_bars_excluded,
        "warmup_1h_bars_excluded": c.warmup_1h_bars_excluded,
        "decision_bars_evaluated": c.decision_bars_evaluated,
        "bias_long_count": c.bias_long_count,
        "bias_short_count": c.bias_short_count,
        "bias_neutral_count": c.bias_neutral_count,
        "valid_setup_windows_detected": c.valid_setup_windows_detected,
        "long_breakout_candidates": c.long_breakout_candidates,
        "short_breakout_candidates": c.short_breakout_candidates,
        "rejected_neutral_bias": c.rejected_neutral_bias,
        "rejected_no_valid_setup": c.rejected_no_valid_setup,
        "rejected_close_did_not_break_level": c.rejected_close_did_not_break_level,
        "rejected_true_range_too_small": c.rejected_true_range_too_small,
        "rejected_close_location_failed": c.rejected_close_location_failed,
        "rejected_normalized_atr_regime_failed": c.rejected_normalized_atr_regime_failed,
        "rejected_stop_distance_filter_failed": c.rejected_stop_distance_filter_failed,
        "rejected_sizing_failed": c.rejected_sizing_failed,
        "end_of_data_no_fill": c.end_of_data_no_fill,
        "sizing_below_minqty": c.sizing_below_minqty,
        "sizing_below_min_notional": c.sizing_below_min_notional,
        "sizing_missing_filters": c.sizing_missing_filters,
        "entry_intents_produced": c.entry_intents_produced,
        "trades_filled": c.trades_filled,
        "trades_closed": c.trades_closed,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    _banner(
        "Phase 2e baseline backtest\n"
        "Window: 2022-01-01 through 2026-03-31 UTC\n"
        "Locked Phase 3 defaults: risk=0.25% / usage=0.90 / leverage<=2x / "
        "notional cap=100k USDT / taker=5bps / slippage=MEDIUM / adapter=FAKE"
    )

    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    reports_root = DATA_ROOT / "derived" / "backtests"
    run_dir = reports_root / "phase-2e-baseline" / run_id

    # Load inputs via Hive-partitioned storage helpers.
    klines_root = DATA_ROOT / "normalized" / "klines"
    bars_1h_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    mark_root = DATA_ROOT / "normalized" / "mark_price_klines"
    funding_root = DATA_ROOT / "normalized" / "funding_rate"
    ei_path = _exchange_info_path()

    k15: dict = {}
    k1h: dict = {}
    m15: dict = {}
    fund: dict = {}
    si_map: dict = {}

    for s in SYMBOLS:
        print(f"\nLoading {s.value}...")
        k15[s] = read_klines(klines_root, symbol=s, interval=Interval.I_15M)
        k1h[s] = read_klines(bars_1h_root, symbol=s, interval=Interval.I_1H)
        m15[s] = read_mark_price_klines(mark_root, symbol=s, interval=Interval.I_15M)
        fund[s] = read_funding_rate_events(funding_root, symbol=s)
        si_map[s] = _load_symbol_info(ei_path, s)
        print(
            f"  15m={len(k15[s]):,}  1h={len(k1h[s]):,}  mark={len(m15[s]):,}  "
            f"funding={len(fund[s]):,}"
        )

    cfg = BacktestConfig(
        experiment_name="phase-2e-baseline",
        run_id=run_id,
        symbols=SYMBOLS,
        window_start_ms=WINDOW_START_MS,
        window_end_ms=WINDOW_END_MS,
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
        reports_root=reports_root,
    )

    _banner("Running engine over widened dataset")
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol=k15,
        klines_1h_per_symbol=k1h,
        mark_15m_per_symbol=m15,
        funding_per_symbol=fund,
        symbol_info_per_symbol=si_map,
    )
    if result.warnings:
        print(f"Engine warnings: {result.warnings}")

    print(f"\nTotal trades (all symbols): {result.total_trades}")
    for s in SYMBOLS:
        acc = result.accounting_per_symbol.get(s)
        trades = result.per_symbol_trades.get(s, [])
        if acc is None:
            continue
        print(
            f"  {s.value}: {len(trades)} trades | equity {acc.equity:.2f} | "
            f"realized PnL {acc.realized_pnl:+.2f} USDT "
            f"({acc.return_fraction * 100:+.2f}%)"
        )

    # Dataset citations: the v002 manifests.
    citations: list[DatasetCitation] = []
    for s in SYMBOLS:
        for dataset, ds_cat in [
            ("15m", "15m"),
            ("1h_derived", "1h derived"),
            ("markprice_15m", "mark-price 15m"),
            ("funding", "funding-rate events"),
        ]:
            ds_name = f"binance_usdm_{s.value.lower()}_{dataset}"
            citations.append(
                DatasetCitation(
                    dataset_name=ds_name,
                    dataset_version=f"{ds_name}__v002",
                    manifest_path=str(DATA_ROOT / "manifests" / f"{ds_name}__v002.manifest.json"),
                    notes=f"{ds_cat} dataset for {s.value}",
                )
            )
    citations.append(
        DatasetCitation(
            dataset_name="exchange_info_snapshot",
            raw_file_path=str(ei_path),
            notes="GAP-20260419-020: 2026-04-19 snapshot proxy for entire range.",
        )
    )

    accepted_limits = [
        "GAP-20260419-018: taker commission placeholder (0.05%); commissionRate "
        "authenticated endpoint deferred to Phase 2d.",
        "GAP-20260419-020: exchangeInfo snapshot (2026-04-19) used as proxy across "
        "2022-01 through 2026-03; BTCUSDT/ETHUSDT filters change rarely but may "
        "introduce minor anachronism.",
        "GAP-20260419-024: leverageBracket + commissionRate authenticated endpoints "
        "deferred to Phase 2d; 2x leverage cap is well below any published bracket "
        "threshold so this is not binding.",
        "GAP-20260420-029: Binance fundingRate returns empty markPrice for pre-2024 "
        "funding events; mark_price is None for those events. Funding PnL is "
        "computed from funding_rate + position notional and is unaffected.",
        "Phase 2e is descriptive baseline statistics only, NOT promotion or "
        "live-readiness evidence. No parameter tuning.",
    ]

    written_dir = write_report(
        config=cfg,
        trades_by_symbol=result.per_symbol_trades,
        accounting_by_symbol=result.accounting_per_symbol,
        dataset_citations=citations,
        accepted_limitations=accepted_limits,
        dest_root=reports_root,
    )
    assert written_dir == run_dir, f"expected {run_dir}, got {written_dir}"
    print(f"\nReport written to: {run_dir}")

    # Per-symbol monthly/yearly/funnel breakdowns and overall funnel.
    _banner("Signal-funnel and per-symbol breakdowns")
    for s in SYMBOLS:
        trades = result.per_symbol_trades.get(s, [])
        sym_dir = run_dir / s.value
        sym_dir.mkdir(parents=True, exist_ok=True)

        monthly = _aggregate_trades_by_month(trades)
        yearly = _aggregate_trades_by_year(trades)
        pq.write_table(monthly, sym_dir / "monthly_breakdown.parquet")
        pq.write_table(yearly, sym_dir / "yearly_breakdown.parquet")
        print(
            f"  {s.value}: monthly_breakdown.parquet rows={monthly.num_rows}, "
            f"yearly_breakdown.parquet rows={yearly.num_rows}"
        )

        # Whole-run signal funnel. Per-month funnel diagnostic is out of
        # scope for Phase 2e's minimal runner (would require re-running
        # the diagnostic on monthly slices). Overall funnel is emitted
        # and summarized in the Gate 2 / baseline summary markdown.
        funnel = run_signal_funnel(
            symbol=s,
            klines_15m=k15[s],
            klines_1h=k1h[s],
            symbol_info=si_map[s],
            config=cfg,
        )
        (sym_dir / "funnel_total.json").write_text(
            json.dumps(_funnel_summary_dict(funnel), indent=2, sort_keys=True)
        )
        print(funnel.summary())
        print("")

    # Funding markPrice coverage (per operator condition 5 on GAP-029).
    _banner("Funding markPrice coverage (per GAP-20260420-029)")
    funding_coverage: dict[str, dict[str, int]] = {}
    for s in SYMBOLS:
        events = fund[s]
        with_mp = sum(1 for e in events if e.mark_price is not None)
        without_mp = sum(1 for e in events if e.mark_price is None)
        funding_coverage[s.value] = {
            "funding_events_total": len(events),
            "funding_events_with_mark_price": with_mp,
            "funding_events_missing_mark_price": without_mp,
        }
        print(f"  {s.value}: total={len(events)}, with_mp={with_mp}, without_mp={without_mp}")
    (run_dir / "funding_mark_price_coverage.json").write_text(
        json.dumps(funding_coverage, indent=2, sort_keys=True)
    )

    _banner(f"Phase 2e baseline complete. Run: {run_id}")


if __name__ == "__main__":
    main()
