"""Research-only backtest engine for Prometheus v1.

The backtester consumes historical data from ``prometheus.research.data``
and simulates the ``prometheus.strategy.v1_breakout`` strategy on
completed 15m / 1h bars. It is strictly research-only:

    - no live trading
    - no exchange adapter
    - no credentials
    - no REST / WebSocket / authenticated endpoints
    - no persistence runtime (SAFE_MODE, kill switch, etc. live in Phase 4)
    - no .env, no .mcp.json

Adapter enum is intentionally FAKE-only in Phase 3. A mechanical
import-graph test (`tests/unit/research/backtest/test_import_graph.py`)
asserts this package does not import from
``prometheus.exchange`` or any Binance-network module.
"""

from __future__ import annotations

from .accounting import Accounting
from .config import BacktestAdapter, BacktestConfig, SlippageBucket, StopTriggerSource
from .diagnostics import SignalFunnelCounts, run_signal_funnel
from .engine import BacktestEngine, BacktestRunResult
from .fills import compute_fill_price, entry_fill_price
from .funding_join import apply_funding_accrual
from .report import (
    BacktestReportManifest,
    compute_drawdown_series,
    compute_equity_curve,
    compute_r_multiple_histogram,
    compute_summary_metrics,
    write_report,
)
from .simulation_clock import bar_visible_at, select_latest_completed_1h
from .sizing import SizingDecision, SizingLimitedBy, compute_size
from .stops import StopHit, evaluate_stop_hit
from .trade_log import (
    TradeRecord,
    trade_record_to_parquet_table,
    write_trade_log,
)

__all__ = [
    "Accounting",
    "BacktestAdapter",
    "BacktestConfig",
    "BacktestEngine",
    "BacktestReportManifest",
    "BacktestRunResult",
    "SignalFunnelCounts",
    "SizingDecision",
    "SizingLimitedBy",
    "SlippageBucket",
    "StopHit",
    "StopTriggerSource",
    "TradeRecord",
    "apply_funding_accrual",
    "bar_visible_at",
    "compute_drawdown_series",
    "compute_equity_curve",
    "compute_fill_price",
    "compute_r_multiple_histogram",
    "compute_size",
    "compute_summary_metrics",
    "entry_fill_price",
    "evaluate_stop_hit",
    "run_signal_funnel",
    "select_latest_completed_1h",
    "trade_record_to_parquet_table",
    "write_report",
    "write_trade_log",
]
