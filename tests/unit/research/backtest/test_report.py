from __future__ import annotations

import json

import pytest

from prometheus.core.symbols import Symbol
from prometheus.research.backtest.accounting import Accounting
from prometheus.research.backtest.config import SlippageBucket
from prometheus.research.backtest.report import (
    BacktestReportManifest,
    DatasetCitation,
    compute_drawdown_series,
    compute_equity_curve,
    compute_r_multiple_histogram,
    compute_summary_metrics,
    write_report,
)
from prometheus.research.backtest.sizing import SizingLimitedBy
from prometheus.research.backtest.trade_log import TradeRecord

from .conftest import default_config


def _trade(
    net_pnl: float, r: float, exit_time: int, direction: str = "LONG", reason: str = "STOP"
) -> TradeRecord:
    return TradeRecord(
        trade_id=f"t-{exit_time}",
        symbol=Symbol.BTCUSDT,
        direction=direction,
        signal_bar_open_time_ms=exit_time - 1000,
        entry_fill_time_ms=exit_time - 900,
        entry_fill_price=50_000.0,
        initial_stop=49_000.0,
        stop_distance=1000.0,
        quantity=0.01,
        notional_usdt=500.0,
        sizing_limited_by=SizingLimitedBy.STOP_RISK,
        realized_risk_usdt=10.0,
        exit_reason=reason,
        exit_fill_time_ms=exit_time,
        exit_fill_price=49_000.0 if net_pnl < 0 else 51_000.0,
        gross_pnl=net_pnl + 0.5,
        entry_fee=0.25,
        exit_fee=0.25,
        funding_pnl=0.0,
        net_pnl=net_pnl,
        net_r_multiple=r,
        mfe_r=abs(r),
        mae_r=abs(r),
        bars_in_trade=5,
        slippage_bucket=SlippageBucket.MEDIUM,
        fee_rate_assumption=0.0005,
        stop_was_gap_through=False,
    )


class TestEquityCurve:
    def test_monotonic_accumulation(self) -> None:
        trades = [_trade(5.0, 0.5, 1_000), _trade(-3.0, -0.3, 2_000), _trade(10.0, 1.0, 3_000)]
        table = compute_equity_curve(trades, starting_equity=100.0)
        assert table.num_rows == 3
        vals = table.column("equity_usdt").to_pylist()
        assert vals[0] == pytest.approx(105.0)
        assert vals[1] == pytest.approx(102.0)
        assert vals[2] == pytest.approx(112.0)

    def test_empty_trades_empty_curve(self) -> None:
        table = compute_equity_curve([], starting_equity=100.0)
        assert table.num_rows == 0

    def test_rejects_non_positive_equity(self) -> None:
        with pytest.raises(ValueError):
            compute_equity_curve([], starting_equity=0.0)


class TestDrawdown:
    def test_drawdown_series(self) -> None:
        trades = [_trade(5.0, 0.5, 1_000), _trade(-3.0, -0.3, 2_000), _trade(-2.0, -0.2, 3_000)]
        eq = compute_equity_curve(trades, starting_equity=100.0)
        dd = compute_drawdown_series(eq)
        assert dd.num_rows == 3
        # peak after t1 = 105; t2 equity = 102, drawdown = -3.
        dds = dd.column("drawdown_usdt").to_pylist()
        assert dds[1] == pytest.approx(-3.0)
        assert dds[2] == pytest.approx(-5.0)

    def test_empty_input(self) -> None:
        import pyarrow as pa

        empty = pa.table(
            {
                "exit_fill_time_ms": pa.array([], type=pa.int64()),
                "equity_usdt": pa.array([], type=pa.float64()),
            }
        )
        dd = compute_drawdown_series(empty)
        assert dd.num_rows == 0


class TestRMultipleHistogram:
    def test_bins_trades_correctly(self) -> None:
        trades = [
            _trade(5.0, -1.5, 1_000),  # [-2, -1)
            _trade(5.0, 0.3, 2_000),  # [0, 0.5)
            _trade(5.0, 0.7, 3_000),  # [0.5, 1.0)
            _trade(5.0, 2.5, 4_000),  # [2, 3)
            _trade(5.0, 100.0, 5_000),  # overflow
        ]
        hist = compute_r_multiple_histogram(trades)
        counts = {
            label: count
            for label, count in zip(
                hist.column("bin_label").to_pylist(), hist.column("count").to_pylist(), strict=True
            )
        }
        assert counts["[-2.0,-1.0)"] == 1
        assert counts["[0.0,0.5)"] == 1
        assert counts["[0.5,1.0)"] == 1
        assert counts["[2.0,3.0)"] == 1
        assert counts["(10.0,+inf)"] == 1


class TestSummaryMetrics:
    def test_empty_trades(self) -> None:
        acc = Accounting.start(starting_equity=100.0)
        m = compute_summary_metrics([], acc)
        assert m["trade_count"] == 0
        assert m["win_rate"] == 0.0

    def test_basic_counts(self) -> None:
        acc = Accounting.start(starting_equity=100.0)
        trades = [
            _trade(5.0, 0.5, 1_000, direction="LONG", reason="STOP"),
            _trade(-3.0, -0.3, 2_000, direction="LONG", reason="STAGNATION"),
            _trade(10.0, 1.0, 3_000, direction="SHORT", reason="TRAILING_BREACH"),
        ]
        m = compute_summary_metrics(trades, acc)
        assert m["trade_count"] == 3
        assert m["win_count"] == 2
        assert m["loss_count"] == 1
        assert m["win_rate"] == pytest.approx(2 / 3)
        assert m["long_count"] == 2
        assert m["short_count"] == 1
        assert m["stop_exits"] == 1
        assert m["stagnation_exits"] == 1
        assert m["trailing_exits"] == 1
        assert m["total_net_pnl_usdt"] == pytest.approx(12.0)


class TestWriteReport:
    def test_emits_expected_artifacts(self, tmp_path) -> None:
        cfg = default_config(tmp_path)
        trades = [_trade(5.0, 0.5, 1_000)]
        acc = Accounting.start(starting_equity=10_000.0)
        acc.apply_trade(
            __import__(
                "prometheus.research.backtest.accounting", fromlist=["compute_trade_pnl"]
            ).compute_trade_pnl(
                direction_long=True,
                entry_price=50_000.0,
                exit_price=50_500.0,
                quantity=0.01,
                stop_distance=1000.0,
                taker_fee_rate=0.0,
                funding_accrued=0.0,
            )
        )
        citation = DatasetCitation(
            dataset_name="binance_usdm_btcusdt_15m",
            dataset_version="binance_usdm_btcusdt_15m__v001",
        )
        run_dir = write_report(
            config=cfg,
            trades_by_symbol={Symbol.BTCUSDT: trades},
            accounting_by_symbol={Symbol.BTCUSDT: acc},
            dataset_citations=[citation],
            accepted_limitations=[
                "Phase 3 uses exchangeInfo 2026-04-19 snapshot as 2026-03 proxy."
            ],
            dest_root=tmp_path / "reports",
        )
        assert (run_dir / "backtest_report.manifest.json").is_file()
        assert (run_dir / "config_snapshot.json").is_file()
        sym_dir = run_dir / "BTCUSDT"
        assert (sym_dir / "trade_log.parquet").is_file()
        assert (sym_dir / "trade_log.json").is_file()
        assert (sym_dir / "equity_curve.parquet").is_file()
        assert (sym_dir / "drawdown.parquet").is_file()
        assert (sym_dir / "r_multiple_hist.parquet").is_file()
        assert (sym_dir / "summary_metrics.json").is_file()
        # Manifest roundtrips through the model.
        payload = json.loads((run_dir / "backtest_report.manifest.json").read_text())
        manifest = BacktestReportManifest.model_validate(payload)
        assert manifest.total_trades == 1
        assert len(manifest.dataset_citations) == 1
        assert manifest.accepted_limitations
