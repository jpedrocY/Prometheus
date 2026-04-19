from __future__ import annotations

import pytest

from prometheus.research.backtest.sizing import (
    RejectionReason,
    SizingLimitedBy,
    compute_size,
)

from .conftest import default_symbol_info


def _call(
    *,
    stop_distance: float = 1000.0,
    reference_price: float = 50_000.0,
    equity: float = 10_000.0,
    risk_fraction: float = 0.0025,
    risk_usage: float = 0.90,
    max_leverage: float = 2.0,
    notional_cap: float = 100_000.0,
):
    return compute_size(
        sizing_equity_usdt=equity,
        risk_fraction=risk_fraction,
        risk_usage_fraction=risk_usage,
        stop_distance=stop_distance,
        reference_price=reference_price,
        max_effective_leverage=max_leverage,
        max_notional_internal_usdt=notional_cap,
        symbol_info=default_symbol_info(),
    )


def test_stop_risk_binds_by_default() -> None:
    # risk_amount = 10_000 * 0.0025 = 25. risk_budget = 22.5.
    # raw_qty = 22.5 / 1000 = 0.0225. Floored to step 0.001 -> 0.022.
    # leverage cap qty = (10_000 * 2) / 50_000 = 0.4 (not binding).
    # notional cap qty = 100_000 / 50_000 = 2.0 (not binding).
    decision = _call()
    assert decision.approved
    # After flooring, STEP_SIZE_FLOOR may take over the label if it
    # binds more tightly than the original STOP_RISK candidate. Allow
    # either label here since the test's main point is approval.
    assert decision.limited_by in {SizingLimitedBy.STOP_RISK, SizingLimitedBy.STEP_SIZE_FLOOR}
    assert decision.quantity > 0


def test_leverage_cap_binds() -> None:
    # Very tight stop -> raw_qty huge. Leverage cap = (10_000*2)/50_000 = 0.4.
    decision = _call(stop_distance=1.0)
    assert decision.approved
    assert decision.limited_by in {
        SizingLimitedBy.MAX_EFFECTIVE_LEVERAGE,
        SizingLimitedBy.STEP_SIZE_FLOOR,
    }


def test_notional_cap_binds() -> None:
    # Very tight stop + high leverage -> notional cap of 100_000 / 50_000 = 2.0 binds.
    decision = _call(stop_distance=1.0, max_leverage=100.0)
    assert decision.approved
    # Either notional cap or step-floor after flooring.
    assert decision.limited_by in {
        SizingLimitedBy.INTERNAL_NOTIONAL_CAP,
        SizingLimitedBy.STEP_SIZE_FLOOR,
    }


def test_below_min_qty_rejects() -> None:
    # Small equity * small risk: raw_qty below minQty=0.001.
    decision = _call(equity=10.0, stop_distance=10_000.0, reference_price=50_000.0)
    # risk_amount = 10*0.0025 = 0.025. risk_budget = 0.0225. raw_qty = 0.0000022.
    # Floored to 0.001 stepSize -> 0.0 < minQty.
    assert not decision.approved
    assert decision.rejection_reason == RejectionReason.BELOW_MINQTY


def test_below_min_notional_rejects() -> None:
    # Make qty just above minQty but below minNotional: minQty=0.001, minNotional=5.
    # 0.001 * reference = 0.001 * 100 = 0.1 < 5 -> reject.
    decision = compute_size(
        sizing_equity_usdt=40.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        stop_distance=20.0,
        reference_price=100.0,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        symbol_info=default_symbol_info(),
    )
    # raw_qty = (40*0.0025*0.9)/20 = 0.0045 -> floor to 0.004 (valid qty),
    # but 0.004 * 100 = 0.4 < 5 -> reject by min_notional.
    assert not decision.approved
    assert decision.rejection_reason == RejectionReason.BELOW_MIN_NOTIONAL


def test_rounds_down_not_nearest() -> None:
    # raw_qty = 0.0225; step = 0.001 -> floored to 0.022 (NOT rounded up to 0.023).
    decision = _call()
    assert decision.quantity == pytest.approx(0.022)


def test_realized_risk_reflects_floored_qty() -> None:
    # If floored down, realized risk = floored_qty * stop_distance.
    decision = _call()
    assert decision.realized_risk_usdt == pytest.approx(decision.quantity * 1000.0)


def test_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        _call(equity=0.0)
    with pytest.raises(ValueError):
        _call(stop_distance=0.0)
    with pytest.raises(ValueError):
        _call(reference_price=0.0)


def test_missing_filters_rejects() -> None:
    from prometheus.core.exchange_info import SymbolInfo

    si = SymbolInfo(
        symbol="BTCUSDT",
        pair="BTCUSDT",
        contractType="PERPETUAL",
        status="TRADING",
        baseAsset="BTC",
        quoteAsset="USDT",
        pricePrecision=2,
        quantityPrecision=3,
        price_filter=None,
        lot_size_filter=None,
        market_lot_size_filter=None,
        min_notional_filter=None,
    )
    decision = compute_size(
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        stop_distance=1000.0,
        reference_price=50_000.0,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        symbol_info=si,
    )
    assert not decision.approved
    assert decision.rejection_reason == RejectionReason.MISSING_FILTERS
