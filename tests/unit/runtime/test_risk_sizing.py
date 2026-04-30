"""Phase 4a tests for the risk-sizing skeleton."""

from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.risk.sizing import (
    LOCKED_LIVE_LEVERAGE_CAP,
    LOCKED_LIVE_RISK_FRACTION,
    SizingError,
    SizingInputs,
    compute_sizing,
)


def _baseline_inputs(**overrides: object) -> SizingInputs:
    base = dict(
        symbol=Symbol.BTCUSDT,
        account_equity_usdt=10_000.0,
        strategy_allocated_equity_usdt=10_000.0,
        risk_fraction=LOCKED_LIVE_RISK_FRACTION,
        risk_usage_fraction=0.90,
        proposed_entry_price=50_000.0,
        initial_stop_price=49_500.0,
        side_is_long=True,
        leverage_cap=LOCKED_LIVE_LEVERAGE_CAP,
        notional_cap_usdt=20_000.0,
        quantity_step=0.001,
        min_quantity=0.001,
    )
    base.update(overrides)
    return SizingInputs(**base)  # type: ignore[arg-type]


def test_locked_constants_match_phase_1_7_3() -> None:
    assert LOCKED_LIVE_RISK_FRACTION == 0.0025
    assert LOCKED_LIVE_LEVERAGE_CAP == 2.0


def test_baseline_long_sizing_succeeds() -> None:
    result = compute_sizing(_baseline_inputs())
    # 0.25% of 10_000 = 25 USDT; 0.90 budget = 22.50 USDT.
    # stop distance = 500; raw = 22.50 / 500 = 0.045 BTC.
    # rounded down to 0.001 step = 0.045.
    assert result.stop_distance == pytest.approx(500.0)
    assert result.rounded_quantity == pytest.approx(0.045)
    assert result.notional_usdt == pytest.approx(2_250.0)
    assert result.effective_leverage == pytest.approx(0.225)


def test_long_stop_above_entry_rejected() -> None:
    with pytest.raises(SizingError):
        compute_sizing(_baseline_inputs(initial_stop_price=51_000.0))


def test_short_stop_below_entry_rejected() -> None:
    with pytest.raises(SizingError):
        compute_sizing(
            _baseline_inputs(side_is_long=False, initial_stop_price=49_500.0)
        )


def test_short_stop_above_entry_succeeds() -> None:
    result = compute_sizing(
        _baseline_inputs(side_is_long=False, initial_stop_price=50_500.0)
    )
    assert result.stop_distance == pytest.approx(500.0)


def test_below_minimum_quantity_rejects_rather_than_scaling_up() -> None:
    # Push stop distance way out: tiny implied quantity.
    with pytest.raises(SizingError):
        compute_sizing(
            _baseline_inputs(
                initial_stop_price=10_000.0,  # 40k stop distance
                min_quantity=0.01,
            )
        )


def test_notional_cap_violation_rejected() -> None:
    # Tight stop -> large quantity -> big notional.
    with pytest.raises(SizingError):
        compute_sizing(
            _baseline_inputs(
                initial_stop_price=49_995.0,  # tiny 5 USD stop distance
                notional_cap_usdt=100.0,
            )
        )


def test_leverage_cap_violation_rejected() -> None:
    # Force notional = 30_000 with sizing equity 10_000 -> leverage 3x > 2x cap.
    with pytest.raises(SizingError):
        compute_sizing(
            _baseline_inputs(
                initial_stop_price=49_990.0,
                notional_cap_usdt=1_000_000.0,
                leverage_cap=2.0,
            )
        )


def test_missing_equity_fails_closed_via_pydantic() -> None:
    # account_equity must be > 0; pydantic raises before compute_sizing runs.
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _baseline_inputs(account_equity_usdt=0)


def test_missing_quantity_step_fails_closed_via_pydantic() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _baseline_inputs(quantity_step=0)


def test_zero_risk_fraction_fails_closed() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _baseline_inputs(risk_fraction=0)


def test_strategy_allocated_equity_caps_sizing() -> None:
    """When strategy allocation < account equity, the smaller value wins."""
    result = compute_sizing(
        _baseline_inputs(
            account_equity_usdt=100_000.0,
            strategy_allocated_equity_usdt=10_000.0,
        )
    )
    assert result.sizing_equity_usdt == pytest.approx(10_000.0)
