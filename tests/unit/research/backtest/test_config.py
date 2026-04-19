from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from prometheus.core.symbols import Symbol
from prometheus.research.backtest.config import (
    BacktestAdapter,
    BacktestConfig,
    SlippageBucket,
)

from .conftest import default_config


def test_default_config_valid() -> None:
    cfg = default_config()
    assert cfg.adapter == BacktestAdapter.FAKE
    assert cfg.slippage_bps == 3.0  # MEDIUM
    assert cfg.symbols == (Symbol.BTCUSDT,)


def test_rejects_bad_window() -> None:
    with pytest.raises(ValidationError):
        BacktestConfig(
            experiment_name="x",
            run_id="r",
            symbols=(Symbol.BTCUSDT,),
            window_start_ms=2_000_000,
            window_end_ms=1_000_000,  # end <= start
            sizing_equity_usdt=10_000.0,
            risk_fraction=0.0025,
            risk_usage_fraction=0.9,
            max_effective_leverage=2.0,
            max_notional_internal_usdt=100_000.0,
            taker_fee_rate=0.0005,
            slippage_bucket=SlippageBucket.MEDIUM,
            klines_root=Path("."),
            mark_price_root=Path("."),
            funding_root=Path("."),
            bars_1h_root=Path("."),
            exchange_info_path=Path("."),
            reports_root=Path("."),
        )


def test_rejects_risk_above_5pct() -> None:
    base = dict(
        experiment_name="x",
        run_id="r",
        symbols=(Symbol.BTCUSDT,),
        window_start_ms=1_000_000,
        window_end_ms=2_000_000,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.10,  # 10% > 5% sanity cap
        risk_usage_fraction=0.9,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=SlippageBucket.MEDIUM,
        klines_root=Path("."),
        mark_price_root=Path("."),
        funding_root=Path("."),
        bars_1h_root=Path("."),
        exchange_info_path=Path("."),
        reports_root=Path("."),
    )
    with pytest.raises(ValidationError):
        BacktestConfig(**base)  # type: ignore[arg-type]


def test_rejects_leverage_above_10x() -> None:
    base = dict(
        experiment_name="x",
        run_id="r",
        symbols=(Symbol.BTCUSDT,),
        window_start_ms=1_000_000,
        window_end_ms=2_000_000,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.9,
        max_effective_leverage=20.0,  # >10x sanity cap
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=SlippageBucket.MEDIUM,
        klines_root=Path("."),
        mark_price_root=Path("."),
        funding_root=Path("."),
        bars_1h_root=Path("."),
        exchange_info_path=Path("."),
        reports_root=Path("."),
    )
    with pytest.raises(ValidationError):
        BacktestConfig(**base)  # type: ignore[arg-type]


def test_adapter_enum_has_only_fake() -> None:
    """Mechanical guardrail: BacktestAdapter must have no non-FAKE values.

    Any later phase adding a real adapter must fail this test until
    the accompanying phase-gate docs are updated.
    """
    values = [m.value for m in BacktestAdapter]
    assert values == ["FAKE"]


def test_slippage_map_must_cover_all_buckets() -> None:
    with pytest.raises(ValidationError):
        BacktestConfig(
            experiment_name="x",
            run_id="r",
            symbols=(Symbol.BTCUSDT,),
            window_start_ms=1_000_000,
            window_end_ms=2_000_000,
            sizing_equity_usdt=10_000.0,
            risk_fraction=0.0025,
            risk_usage_fraction=0.9,
            max_effective_leverage=2.0,
            max_notional_internal_usdt=100_000.0,
            taker_fee_rate=0.0005,
            slippage_bucket=SlippageBucket.MEDIUM,
            slippage_bps_map={SlippageBucket.LOW: 1.0},  # missing MEDIUM + HIGH
            klines_root=Path("."),
            mark_price_root=Path("."),
            funding_root=Path("."),
            bars_1h_root=Path("."),
            exchange_info_path=Path("."),
            reports_root=Path("."),
        )
