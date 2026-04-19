from __future__ import annotations

import pytest

from prometheus.core.intervals import Interval, interval_duration_ms


def test_interval_values() -> None:
    assert Interval.I_15M.value == "15m"
    assert Interval.I_1H.value == "1h"


def test_interval_duration_15m() -> None:
    assert interval_duration_ms(Interval.I_15M) == 15 * 60 * 1000


def test_interval_duration_1h() -> None:
    assert interval_duration_ms(Interval.I_1H) == 60 * 60 * 1000


def test_interval_unknown_string_rejected() -> None:
    with pytest.raises(ValueError):
        Interval("5m")
