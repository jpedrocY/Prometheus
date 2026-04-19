"""Shared helpers for backtest unit tests."""

from __future__ import annotations

from pathlib import Path

from prometheus.core.exchange_info import (
    LotSizeFilter,
    MarketLotSizeFilter,
    MinNotionalFilter,
    PriceFilter,
    SymbolInfo,
)
from prometheus.core.symbols import Symbol
from prometheus.research.backtest.config import (
    DEFAULT_SLIPPAGE_BPS,
    BacktestConfig,
    SlippageBucket,
)


def default_symbol_info(symbol: Symbol = Symbol.BTCUSDT) -> SymbolInfo:
    """A minimal BTCUSDT-like SymbolInfo for sizing tests."""
    return SymbolInfo(
        symbol=str(symbol.value),
        pair=str(symbol.value),
        contractType="PERPETUAL",
        status="TRADING",
        baseAsset="BTC" if symbol == Symbol.BTCUSDT else "ETH",
        quoteAsset="USDT",
        pricePrecision=2,
        quantityPrecision=3,
        price_filter=PriceFilter(
            filterType="PRICE_FILTER",
            minPrice="100.0",
            maxPrice="1000000.0",
            tickSize="0.1",
        ),
        lot_size_filter=LotSizeFilter(
            filterType="LOT_SIZE",
            minQty="0.001",
            maxQty="10000.0",
            stepSize="0.001",
        ),
        market_lot_size_filter=MarketLotSizeFilter(
            filterType="MARKET_LOT_SIZE",
            minQty="0.001",
            maxQty="10000.0",
            stepSize="0.001",
        ),
        min_notional_filter=MinNotionalFilter(
            filterType="MIN_NOTIONAL",
            notional="5.0",
        ),
    )


def default_config(tmp_path: Path | None = None) -> BacktestConfig:
    root = tmp_path or Path(".")
    return BacktestConfig(
        experiment_name="unit-test",
        run_id="r-0001",
        symbols=(Symbol.BTCUSDT,),
        window_start_ms=1_000_000,
        window_end_ms=2_000_000,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=SlippageBucket.MEDIUM,
        slippage_bps_map=dict(DEFAULT_SLIPPAGE_BPS),
        klines_root=root / "klines",
        mark_price_root=root / "mark",
        funding_root=root / "funding",
        bars_1h_root=root / "1h",
        exchange_info_path=root / "ei.json",
        reports_root=root / "reports",
    )
