from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol


def test_symbol_values() -> None:
    assert Symbol.BTCUSDT.value == "BTCUSDT"
    assert Symbol.ETHUSDT.value == "ETHUSDT"


def test_symbol_unknown_rejected() -> None:
    with pytest.raises(ValueError):
        Symbol("XRPUSDT")
