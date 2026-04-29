from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from prometheus.core.symbols import Symbol
from prometheus.research.backtest.config import (
    BacktestAdapter,
    BacktestConfig,
    SlippageBucket,
    StrategyFamily,
)
from prometheus.strategy.funding_aware_directional import FundingAwareConfig
from prometheus.strategy.mean_reversion_overextension import MeanReversionConfig
from prometheus.strategy.v1_breakout import V1BreakoutConfig

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


# ---------- Phase 3d-B1: F1 strategy-family dispatch validation ----------


def test_default_strategy_family_is_v1_breakout() -> None:
    """Default ``BacktestConfig`` preserves V1_BREAKOUT dispatch."""
    cfg = default_config()
    assert cfg.strategy_family == StrategyFamily.V1_BREAKOUT
    assert cfg.mean_reversion_variant is None


def test_v1_breakout_rejects_mean_reversion_variant() -> None:
    """V1_BREAKOUT family must keep ``mean_reversion_variant`` None."""
    base = default_config()
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(exclude={"strategy_family", "mean_reversion_variant"}),
            strategy_family=StrategyFamily.V1_BREAKOUT,
            mean_reversion_variant=MeanReversionConfig(),
        )


def test_f1_family_accepts_mean_reversion_variant() -> None:
    """F1 dispatch is admissible when ``mean_reversion_variant`` is set."""
    base = default_config()
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "mean_reversion_variant"}),
        strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
        mean_reversion_variant=MeanReversionConfig(),
    )
    assert cfg.strategy_family == StrategyFamily.MEAN_REVERSION_OVEREXTENSION
    assert cfg.mean_reversion_variant is not None


def test_f1_family_requires_mean_reversion_variant() -> None:
    """F1 dispatch without a config payload is rejected."""
    base = default_config()
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(exclude={"strategy_family", "mean_reversion_variant"}),
            strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
            mean_reversion_variant=None,
        )


def test_f1_family_rejects_non_default_v1_strategy_variant() -> None:
    """F1 must not be combined with non-default V1 strategy_variant."""
    base = default_config()
    non_default_v1 = V1BreakoutConfig(setup_size=10)
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(
                exclude={"strategy_family", "mean_reversion_variant", "strategy_variant"}
            ),
            strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
            mean_reversion_variant=MeanReversionConfig(),
            strategy_variant=non_default_v1,
        )


# ---------- Phase 3i-A: D1-A funding-aware dispatch validation ----------


def test_strategy_family_funding_aware_directional_exists() -> None:
    """Phase 3i-A: enum has the new D1-A value."""
    assert StrategyFamily.FUNDING_AWARE_DIRECTIONAL == "FUNDING_AWARE_DIRECTIONAL"


def test_default_config_has_no_funding_aware_variant() -> None:
    """Default config remains V1_BREAKOUT with no funding_aware_variant."""
    cfg = default_config()
    assert cfg.strategy_family == StrategyFamily.V1_BREAKOUT
    assert cfg.funding_aware_variant is None


def test_v1_breakout_rejects_funding_aware_variant() -> None:
    """V1_BREAKOUT family must keep ``funding_aware_variant`` None."""
    base = default_config()
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(exclude={"strategy_family", "funding_aware_variant"}),
            strategy_family=StrategyFamily.V1_BREAKOUT,
            funding_aware_variant=FundingAwareConfig(),
        )


def test_f1_family_rejects_funding_aware_variant() -> None:
    """F1 family must not be combined with a funding_aware_variant."""
    base = default_config()
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(
                exclude={
                    "strategy_family",
                    "mean_reversion_variant",
                    "funding_aware_variant",
                }
            ),
            strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
            mean_reversion_variant=MeanReversionConfig(),
            funding_aware_variant=FundingAwareConfig(),
        )


def test_d1a_family_accepts_funding_aware_variant() -> None:
    """D1-A dispatch is admissible when ``funding_aware_variant`` is set."""
    base = default_config()
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "funding_aware_variant"}),
        strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
        funding_aware_variant=FundingAwareConfig(),
    )
    assert cfg.strategy_family == StrategyFamily.FUNDING_AWARE_DIRECTIONAL
    assert cfg.funding_aware_variant is not None


def test_d1a_family_requires_funding_aware_variant() -> None:
    """D1-A dispatch without a config payload is rejected."""
    base = default_config()
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(exclude={"strategy_family", "funding_aware_variant"}),
            strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
            funding_aware_variant=None,
        )


def test_d1a_family_rejects_mean_reversion_variant() -> None:
    """D1-A must not be combined with a mean_reversion_variant."""
    base = default_config()
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(
                exclude={
                    "strategy_family",
                    "mean_reversion_variant",
                    "funding_aware_variant",
                }
            ),
            strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
            funding_aware_variant=FundingAwareConfig(),
            mean_reversion_variant=MeanReversionConfig(),
        )


def test_d1a_family_rejects_non_default_v1_strategy_variant() -> None:
    """D1-A must not be combined with non-default V1 strategy_variant
    (Phase 3g §14 / Phase 3h §3 forbid V1/D1 hybrid)."""
    base = default_config()
    non_default_v1 = V1BreakoutConfig(setup_size=10)
    with pytest.raises(ValidationError):
        BacktestConfig(
            **base.model_dump(
                exclude={
                    "strategy_family",
                    "funding_aware_variant",
                    "strategy_variant",
                }
            ),
            strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
            funding_aware_variant=FundingAwareConfig(),
            strategy_variant=non_default_v1,
        )
