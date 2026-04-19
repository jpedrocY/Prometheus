from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from prometheus.core.events import FundingRateEvent
from prometheus.core.symbols import Symbol


def _kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "symbol": Symbol.BTCUSDT,
        "funding_time": 1_774_224_000_000,
        "funding_rate": 0.0001,  # 0.01%
        "mark_price": 65000.0,
        "source": "test",
    }
    base.update(overrides)
    return base


def test_valid_event_accepts() -> None:
    event = FundingRateEvent(**_kwargs())
    assert event.symbol is Symbol.BTCUSDT
    assert event.funding_rate == 0.0001


def test_frozen() -> None:
    event = FundingRateEvent(**_kwargs())
    with pytest.raises(ValidationError):
        event.funding_rate = 0.0  # type: ignore[misc]


def test_extra_field_rejected() -> None:
    with pytest.raises(ValidationError):
        FundingRateEvent(**_kwargs(), unknown="x")


def test_negative_funding_time_rejected() -> None:
    with pytest.raises(ValidationError):
        FundingRateEvent(**_kwargs(funding_time=-1))


def test_zero_funding_time_rejected() -> None:
    with pytest.raises(ValidationError):
        FundingRateEvent(**_kwargs(funding_time=0))


def test_funding_rate_magnitude_1_rejected() -> None:
    with pytest.raises(ValidationError):
        FundingRateEvent(**_kwargs(funding_rate=1.0))


def test_funding_rate_magnitude_minus_1_rejected() -> None:
    with pytest.raises(ValidationError):
        FundingRateEvent(**_kwargs(funding_rate=-1.0))


def test_negative_mark_price_rejected() -> None:
    with pytest.raises(ValidationError):
        FundingRateEvent(**_kwargs(mark_price=-1.0))


def test_zero_mark_price_rejected() -> None:
    with pytest.raises(ValidationError):
        FundingRateEvent(**_kwargs(mark_price=0.0))


def test_negative_funding_rate_accepted_under_bound() -> None:
    # Negative funding rates are legitimate (shorts pay longs).
    event = FundingRateEvent(**_kwargs(funding_rate=-0.0005))
    assert event.funding_rate == -0.0005
