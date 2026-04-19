"""Real-data smoke tests for BTCUSDT / ETHUSDT 2026-03.

Per Phase 3 Gate 1 condition A: these tests are SKIPPED when the
local data tree is absent (i.e., on a clean clone). They are not
part of any default-pytest-run requirement. The data is operator-
downloaded; real runs are invoked explicitly.

When the data IS present (developer local machine after Phase 2b/2c),
these tests exercise the full engine on real 2026-03 bars and
assert only structural invariants:

    - engine completes without exceptions
    - trade records, if any, have sane field values
    - no NaN equity values emerge
    - dataset-manifest-cited data is loadable

Profitability, strategy quality, and parameter sensitivity are NOT
asserted — Phase 3 scope is conformance/mechanics only
(operator-approved §11.D.DS1).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from prometheus.core.exchange_info import ExchangeInfoSnapshot
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.backtest import (
    BacktestConfig,
    BacktestEngine,
    SlippageBucket,
)
from prometheus.research.backtest.config import DEFAULT_SLIPPAGE_BPS
from prometheus.research.data.storage import (
    read_funding_rate_events,
    read_klines,
    read_mark_price_klines,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "data"

# Phase 2b/2c real data paths; if any missing, the whole file is skipped.
_REQUIRED_PATHS = [
    DATA_ROOT
    / "normalized"
    / "klines"
    / "symbol=BTCUSDT"
    / "interval=15m"
    / "year=2026"
    / "month=03"
    / "part-0000.parquet",
    DATA_ROOT
    / "derived"
    / "bars_1h"
    / "standard"
    / "symbol=BTCUSDT"
    / "interval=1h"
    / "year=2026"
    / "month=03"
    / "part-0000.parquet",
    DATA_ROOT
    / "normalized"
    / "mark_price_klines"
    / "symbol=BTCUSDT"
    / "interval=15m"
    / "year=2026"
    / "month=03"
    / "part-0000.parquet",
    DATA_ROOT
    / "normalized"
    / "funding_rate"
    / "symbol=BTCUSDT"
    / "year=2026"
    / "month=03"
    / "part-0000.parquet",
]


def _exchange_info_path() -> Path | None:
    candidates = sorted((DATA_ROOT / "derived" / "exchange_info").glob("*.json"))
    return candidates[-1] if candidates else None


def _data_absent() -> bool:
    return not all(p.is_file() for p in _REQUIRED_PATHS) or _exchange_info_path() is None


pytestmark = pytest.mark.skipif(
    _data_absent(),
    reason=(
        "Real 2026-03 data not available; skipping real-data smoke tests. "
        "Populate data/ via the Phase 2b/2c operator-run ingest to enable."
    ),
)


def _load_symbol_info(exchange_info_path: Path, symbol: Symbol) -> object:
    payload = json.loads(exchange_info_path.read_text())
    snapshot = ExchangeInfoSnapshot.model_validate(payload)
    for si in snapshot.symbols:
        if si.symbol == symbol.value:
            return si
    raise RuntimeError(f"symbol {symbol} not in exchangeInfo snapshot")


def _build_cfg(
    symbol: Symbol, tmp_path: Path, window_start: int, window_end: int
) -> BacktestConfig:
    return BacktestConfig(
        experiment_name="phase-3-smoke-real",
        run_id=f"r-{symbol.value}",
        symbols=(symbol,),
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
        klines_root=DATA_ROOT / "normalized" / "klines",
        mark_price_root=DATA_ROOT / "normalized" / "mark_price_klines",
        funding_root=DATA_ROOT / "normalized" / "funding_rate",
        bars_1h_root=DATA_ROOT / "derived" / "bars_1h" / "standard",
        exchange_info_path=_exchange_info_path() or Path("."),
        reports_root=tmp_path / "reports",
    )


def _run_smoke(symbol: Symbol, tmp_path: Path) -> None:
    klines_root = DATA_ROOT / "normalized" / "klines"
    bars_1h_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    mark_root = DATA_ROOT / "normalized" / "mark_price_klines"
    funding_root = DATA_ROOT / "normalized" / "funding_rate"
    if not all(p.is_dir() for p in [klines_root, bars_1h_root, mark_root, funding_root]):
        pytest.skip(f"real 2026-03 data roots missing for {symbol.value}")

    # Use the storage helpers (Hive-aware) rather than reading single
    # Parquet files directly. Partition fields (symbol/interval/year/month)
    # are dictionary-encoded in the raw file; read_klines normalizes them.
    k15 = read_klines(klines_root, symbol=symbol, interval=Interval.I_15M)
    k1h = read_klines(bars_1h_root, symbol=symbol, interval=Interval.I_1H)
    m15 = read_mark_price_klines(mark_root, symbol=symbol, interval=Interval.I_15M)
    fund = read_funding_rate_events(funding_root, symbol=symbol)
    if not (k15 and k1h and m15 and fund):
        pytest.skip(f"real 2026-03 data partitions empty for {symbol.value}")
    si = _load_symbol_info(_exchange_info_path() or Path("."), symbol)
    cfg = _build_cfg(
        symbol, tmp_path, window_start=k15[0].open_time, window_end=k15[-1].close_time + 1
    )
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={symbol: k15},
        klines_1h_per_symbol={symbol: k1h},
        mark_15m_per_symbol={symbol: m15},
        funding_per_symbol={symbol: fund},
        symbol_info_per_symbol={symbol: si},  # type: ignore[dict-item]
    )
    # Structural invariants.
    assert not result.warnings
    acc = result.accounting_per_symbol[symbol]
    assert not math.isnan(acc.equity)
    for t in result.per_symbol_trades.get(symbol, []):
        assert t.quantity > 0
        assert t.entry_fill_time_ms > 0
        assert t.exit_fill_time_ms >= t.entry_fill_time_ms
        assert not math.isnan(t.net_pnl)


def test_real_2026_03_btcusdt(tmp_path: Path) -> None:
    _run_smoke(Symbol.BTCUSDT, tmp_path)


def test_real_2026_03_ethusdt(tmp_path: Path) -> None:
    _run_smoke(Symbol.ETHUSDT, tmp_path)
