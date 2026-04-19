"""Equity curve, drawdown, R-multiple histogram, summary metrics, and manifest.

Phase 3 Gate 1 §8.D and §13 define the artifacts this module emits.
All paths are relative to ``config.reports_root``; nothing outside
that directory is touched.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from prometheus.core.symbols import Symbol

from .accounting import Accounting
from .config import BacktestConfig
from .trade_log import TradeRecord

REPORT_SCHEMA_VERSION = "backtest_report_v1"


def _as_tuple(value: object) -> object:
    if isinstance(value, list):
        return tuple(value)
    return value


def _as_symbol_tuple(value: object) -> object:
    if isinstance(value, list | tuple):
        return tuple(Symbol(v) if isinstance(v, str) else v for v in value)
    return value


class DatasetCitation(BaseModel):
    """One dataset consumed by a backtest run.

    Either cites a DatasetManifest by its version (primary), or a
    raw file path + sha256 for artifacts that do not yet have a
    manifest (per GAP-20260419-020 for the exchangeInfo snapshot).
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    dataset_name: str
    dataset_version: str | None = None  # e.g., "binance_usdm_btcusdt_15m__v001"
    manifest_path: str | None = None
    raw_file_path: str | None = None
    raw_file_sha256: str | None = None
    notes: str | None = None


class BacktestReportManifest(BaseModel):
    """Provenance record emitted alongside each backtest run.

    Captures:
        - run identity (experiment, run_id, timestamp)
        - config used (the full BacktestConfig serialized)
        - dataset citations (one per input)
        - summary metrics snapshot
        - engine + strategy version hints
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    schema_version: str = REPORT_SCHEMA_VERSION
    experiment_name: str
    run_id: str
    generated_at_utc_ms: int
    engine_version: str = "phase-3-v1"
    strategy_version: str = "v1_breakout"
    config_snapshot: dict[str, object]
    dataset_citations: Annotated[tuple[DatasetCitation, ...], BeforeValidator(_as_tuple)] = Field(
        default_factory=tuple
    )
    symbols: Annotated[tuple[Symbol, ...], BeforeValidator(_as_symbol_tuple)]
    window_start_ms: int
    window_end_ms: int
    total_trades: int
    accepted_limitations: Annotated[tuple[str, ...], BeforeValidator(_as_tuple)] = Field(
        default_factory=tuple
    )


# ---------------------------------------------------------------------------
# Equity curve / drawdown / R-multiple histogram
# ---------------------------------------------------------------------------


def compute_equity_curve(trades: Sequence[TradeRecord], starting_equity: float) -> pa.Table:
    """Flat (non-compounding) equity curve keyed by exit_fill_time_ms."""
    if starting_equity <= 0:
        raise ValueError("starting_equity must be positive")
    sorted_trades = sorted(trades, key=lambda t: t.exit_fill_time_ms)
    times: list[int] = []
    equity_series: list[float] = []
    realized = 0.0
    for t in sorted_trades:
        realized += t.net_pnl
        times.append(t.exit_fill_time_ms)
        equity_series.append(starting_equity + realized)
    schema = pa.schema([("exit_fill_time_ms", pa.int64()), ("equity_usdt", pa.float64())])
    return pa.Table.from_arrays(
        [pa.array(times, type=pa.int64()), pa.array(equity_series, type=pa.float64())],
        schema=schema,
    )


def compute_drawdown_series(equity_table: pa.Table) -> pa.Table:
    """Rolling max-drawdown from peak."""
    if equity_table.num_rows == 0:
        schema = pa.schema(
            [
                ("exit_fill_time_ms", pa.int64()),
                ("peak_equity_usdt", pa.float64()),
                ("drawdown_usdt", pa.float64()),
                ("drawdown_fraction", pa.float64()),
            ]
        )
        return pa.Table.from_arrays(
            [
                pa.array([], type=pa.int64()),
                pa.array([], type=pa.float64()),
                pa.array([], type=pa.float64()),
                pa.array([], type=pa.float64()),
            ],
            schema=schema,
        )
    times = equity_table.column("exit_fill_time_ms").to_pylist()
    equity = equity_table.column("equity_usdt").to_pylist()
    peaks: list[float] = []
    dds: list[float] = []
    dd_fracs: list[float] = []
    running_peak = equity[0]
    for value in equity:
        if value > running_peak:
            running_peak = value
        peaks.append(running_peak)
        dd = value - running_peak  # <= 0
        dds.append(dd)
        frac = dd / running_peak if running_peak > 0 else 0.0
        dd_fracs.append(frac)
    schema = pa.schema(
        [
            ("exit_fill_time_ms", pa.int64()),
            ("peak_equity_usdt", pa.float64()),
            ("drawdown_usdt", pa.float64()),
            ("drawdown_fraction", pa.float64()),
        ]
    )
    return pa.Table.from_arrays(
        [
            pa.array(times, type=pa.int64()),
            pa.array(peaks, type=pa.float64()),
            pa.array(dds, type=pa.float64()),
            pa.array(dd_fracs, type=pa.float64()),
        ],
        schema=schema,
    )


def compute_r_multiple_histogram(
    trades: Sequence[TradeRecord],
    bin_edges: Sequence[float] = (-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0),
) -> pa.Table:
    """Histogram of net R-multiples across trades.

    Bin boundaries are LEFT-inclusive / RIGHT-exclusive, except the
    final bin which is fully closed. Trades below the lowest edge
    are placed in an underflow bin; trades above the highest edge
    in an overflow bin.
    """
    edges = list(bin_edges)
    if any(edges[i] >= edges[i + 1] for i in range(len(edges) - 1)):
        raise ValueError("bin_edges must be strictly increasing")
    counts = [0] * (len(edges) + 1)  # underflow, [e0,e1), ..., [e_{n-1}, e_n], overflow
    for t in trades:
        r = t.net_r_multiple
        if r < edges[0]:
            counts[0] += 1
            continue
        placed = False
        for i in range(len(edges) - 1):
            if edges[i] <= r < edges[i + 1]:
                counts[i + 1] += 1
                placed = True
                break
        if not placed:
            if edges[-2] <= r <= edges[-1]:
                counts[-2] += 1
            else:
                counts[-1] += 1
    labels = [f"(-inf,{edges[0]})"]
    for i in range(len(edges) - 1):
        labels.append(f"[{edges[i]},{edges[i + 1]})")
    labels.append(f"({edges[-1]},+inf)")
    schema = pa.schema([("bin_label", pa.string()), ("count", pa.int64())])
    return pa.Table.from_arrays(
        [pa.array(labels, type=pa.string()), pa.array(counts, type=pa.int64())],
        schema=schema,
    )


# ---------------------------------------------------------------------------
# Summary metrics
# ---------------------------------------------------------------------------


def compute_summary_metrics(
    trades: Sequence[TradeRecord], accounting: Accounting
) -> dict[str, float | int]:
    """Compute top-level summary metrics over a single-symbol run."""
    n = len(trades)
    if n == 0:
        return {
            "trade_count": 0,
            "win_count": 0,
            "loss_count": 0,
            "win_rate": 0.0,
            "expectancy_r": 0.0,
            "profit_factor": 0.0,
            "total_net_pnl_usdt": 0.0,
            "total_return_fraction": 0.0,
            "max_drawdown_usdt": 0.0,
            "max_drawdown_fraction": 0.0,
            "long_count": 0,
            "short_count": 0,
            "stop_exits": 0,
            "trailing_exits": 0,
            "stagnation_exits": 0,
            "end_of_data_exits": 0,
            "total_fees_usdt": 0.0,
            "total_funding_usdt": 0.0,
            "gap_through_stops": 0,
        }
    wins = [t for t in trades if t.net_pnl > 0]
    losses = [t for t in trades if t.net_pnl < 0]
    win_rate = len(wins) / n
    expectancy_r = sum(t.net_r_multiple for t in trades) / n
    gross_win = sum(t.net_pnl for t in wins)
    gross_loss = -sum(t.net_pnl for t in losses)  # positive
    profit_factor = (
        (gross_win / gross_loss) if gross_loss > 0 else float("inf") if gross_win > 0 else 0.0
    )
    total_net = sum(t.net_pnl for t in trades)
    total_fees = sum(t.entry_fee + t.exit_fee for t in trades)
    total_funding = sum(t.funding_pnl for t in trades)
    long_count = sum(1 for t in trades if t.direction == "LONG")
    short_count = sum(1 for t in trades if t.direction == "SHORT")
    stop_exits = sum(1 for t in trades if t.exit_reason == "STOP")
    trailing_exits = sum(1 for t in trades if t.exit_reason == "TRAILING_BREACH")
    stagnation_exits = sum(1 for t in trades if t.exit_reason == "STAGNATION")
    end_exits = sum(1 for t in trades if t.exit_reason == "END_OF_DATA")
    gap_through = sum(1 for t in trades if t.stop_was_gap_through)

    # Drawdown from equity curve.
    equity_table = compute_equity_curve(trades, accounting.starting_equity)
    dd_table = compute_drawdown_series(equity_table)
    if dd_table.num_rows > 0:
        max_dd = min(dd_table.column("drawdown_usdt").to_pylist())
        max_dd_frac = min(dd_table.column("drawdown_fraction").to_pylist())
    else:
        max_dd = 0.0
        max_dd_frac = 0.0

    return {
        "trade_count": n,
        "win_count": len(wins),
        "loss_count": len(losses),
        "win_rate": win_rate,
        "expectancy_r": expectancy_r,
        "profit_factor": profit_factor,
        "total_net_pnl_usdt": total_net,
        "total_return_fraction": total_net / accounting.starting_equity,
        "max_drawdown_usdt": max_dd,
        "max_drawdown_fraction": max_dd_frac,
        "long_count": long_count,
        "short_count": short_count,
        "stop_exits": stop_exits,
        "trailing_exits": trailing_exits,
        "stagnation_exits": stagnation_exits,
        "end_of_data_exits": end_exits,
        "total_fees_usdt": total_fees,
        "total_funding_usdt": total_funding,
        "gap_through_stops": gap_through,
    }


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------


def _utc_now_ms() -> int:
    return int(datetime.now(tz=UTC).timestamp() * 1000)


def write_report(
    *,
    config: BacktestConfig,
    trades_by_symbol: dict[Symbol, list[TradeRecord]],
    accounting_by_symbol: dict[Symbol, Accounting],
    dataset_citations: Sequence[DatasetCitation],
    accepted_limitations: Sequence[str],
    dest_root: Path,
) -> Path:
    """Write all report artifacts for a single run.

    Returns the run-specific output directory path.
    """
    run_dir = dest_root / config.experiment_name / config.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Per-symbol artifacts.
    all_trades: list[TradeRecord] = []
    for symbol, trades in trades_by_symbol.items():
        if not trades:
            continue
        from .trade_log import write_trade_log  # local import to avoid cycle

        per_symbol_dir = run_dir / symbol.value
        per_symbol_dir.mkdir(parents=True, exist_ok=True)
        write_trade_log(
            trades,
            per_symbol_dir / "trade_log.parquet",
            per_symbol_dir / "trade_log.json",
        )
        accounting = accounting_by_symbol[symbol]
        equity = compute_equity_curve(trades, accounting.starting_equity)
        pq.write_table(equity, per_symbol_dir / "equity_curve.parquet")
        dd = compute_drawdown_series(equity)
        pq.write_table(dd, per_symbol_dir / "drawdown.parquet")
        hist = compute_r_multiple_histogram(trades)
        pq.write_table(hist, per_symbol_dir / "r_multiple_hist.parquet")
        metrics = compute_summary_metrics(trades, accounting)
        (per_symbol_dir / "summary_metrics.json").write_text(
            json.dumps(metrics, indent=2, sort_keys=True)
        )
        all_trades.extend(trades)

    # Manifest + config snapshot at run level.
    config_snapshot = json.loads(config.model_dump_json())
    manifest = BacktestReportManifest(
        experiment_name=config.experiment_name,
        run_id=config.run_id,
        generated_at_utc_ms=_utc_now_ms(),
        config_snapshot=config_snapshot,
        dataset_citations=tuple(dataset_citations),
        symbols=config.symbols,
        window_start_ms=config.window_start_ms,
        window_end_ms=config.window_end_ms,
        total_trades=len(all_trades),
        accepted_limitations=tuple(accepted_limitations),
    )
    (run_dir / "backtest_report.manifest.json").write_text(manifest.model_dump_json(indent=2))
    (run_dir / "config_snapshot.json").write_text(
        json.dumps(config_snapshot, indent=2, sort_keys=True)
    )
    return run_dir


# Silence unused.
_ = asdict
