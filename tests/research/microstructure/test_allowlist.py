"""Tests for the public-only microstructure endpoint allowlist (Phase 4aw)."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure.allowlist import (
    ALLOWLIST_PATTERNS,
    DENYLIST_TOKENS,
    EndpointNotAllowedError,
    assert_endpoint_allowed,
    is_endpoint_allowed,
    is_endpoint_denied,
)

# Public endpoint references that must be admitted.
ALLOWED_PUBLIC_ENDPOINTS: tuple[str, ...] = (
    "wss://fstream.binance.com/ws/btcusdt@aggTrade",
    "wss://fstream.binance.com/ws/btcusdt@bookTicker",
    "wss://fstream.binance.com/ws/btcusdt@depth",
    "wss://fstream.binance.com/ws/btcusdt@depth5",
    "wss://fstream.binance.com/ws/btcusdt@depth20",
    "wss://fstream.binance.com/ws/btcusdt@forceOrder",
    "wss://fstream.binance.com/ws/btcusdt@markPrice",
    "wss://fstream.binance.com/ws/btcusdt@indexPrice",
    "https://fapi.binance.com/fapi/v1/aggTrades",
    "https://fapi.binance.com/fapi/v1/depth",
    "https://fapi.binance.com/fapi/v1/klines",
    "https://fapi.binance.com/fapi/v1/markPriceKlines",
    "https://fapi.binance.com/fapi/v1/indexPriceKlines",
    "https://fapi.binance.com/fapi/v1/premiumIndexKlines",
    "https://fapi.binance.com/fapi/v1/fundingRate",
    "https://fapi.binance.com/fapi/v1/openInterest",
    "https://fapi.binance.com/futures/data/openInterestHist",
    "https://fapi.binance.com/futures/data/topLongShortAccountRatio",
    "https://fapi.binance.com/futures/data/topLongShortPositionRatio",
    "https://fapi.binance.com/futures/data/globalLongShortAccountRatio",
    "https://fapi.binance.com/futures/data/takerlongshortRatio",
)

# References that must be denied. Each must trigger denylist dominance.
DENIED_REFERENCES: tuple[str, ...] = (
    # private / authenticated REST
    "https://fapi.binance.com/fapi/v1/order",
    "https://fapi.binance.com/fapi/v1/openOrders",
    "https://fapi.binance.com/fapi/v1/allOrders",
    "https://fapi.binance.com/fapi/v1/forceOrders",  # authenticated REST, not @forceOrder WS
    "https://fapi.binance.com/fapi/v2/account",
    "https://fapi.binance.com/fapi/v2/positionRisk",
    "https://fapi.binance.com/fapi/v2/balance",
    "https://fapi.binance.com/fapi/v1/leverage",
    "https://fapi.binance.com/fapi/v1/marginType",
    "https://fapi.binance.com/fapi/v1/positionMargin",
    "https://fapi.binance.com/fapi/v1/income",
    "https://fapi.binance.com/fapi/v1/listenKey",
    "https://fapi.binance.com/fapi/v1/userTrades",
    # user data stream / listenKey
    "wss://fstream.binance.com/ws/userDataStream",
    "listenKey=xxxx",
    # credential-shaped strings
    "api_key=ABC",
    "apiKey=ABC",
    "secret_key=XYZ",
    "secretKey=XYZ",
    "X-MBX-APIKEY: header",
    "signature=xxxxxxxx",
    # forbidden tooling / config
    "/path/to/.mcp.json",
    "MCP server",
    "Graphify integration",
    # generic credential references
    ".env file content",
)


def test_allowlist_patterns_non_empty() -> None:
    assert len(ALLOWLIST_PATTERNS) > 0


def test_denylist_tokens_non_empty() -> None:
    assert len(DENYLIST_TOKENS) > 0


@pytest.mark.parametrize("value", ALLOWED_PUBLIC_ENDPOINTS)
def test_allowed_public_endpoints_pass(value: str) -> None:
    assert is_endpoint_allowed(value), f"expected allowed: {value!r}"
    assert not is_endpoint_denied(value), f"expected not denied: {value!r}"
    assert_endpoint_allowed(value)


@pytest.mark.parametrize("value", DENIED_REFERENCES)
def test_denied_references_blocked(value: str) -> None:
    assert is_endpoint_denied(value), f"expected denied: {value!r}"
    assert not is_endpoint_allowed(value), f"expected not allowed: {value!r}"
    with pytest.raises(EndpointNotAllowedError):
        assert_endpoint_allowed(value)


def test_denylist_dominates_allowlist() -> None:
    # @forceOrder is a legitimate public WS subscription pattern.
    public_ref = "wss://fstream.binance.com/ws/btcusdt@forceOrder"
    assert is_endpoint_allowed(public_ref)

    # /fapi/v1/forceOrders is the user-scope authenticated REST endpoint.
    # Even if @forceOrder substring matched, the denylist must dominate.
    auth_ref = "https://fapi.binance.com/fapi/v1/forceOrders"
    assert is_endpoint_denied(auth_ref)
    assert not is_endpoint_allowed(auth_ref)


def test_empty_value_returns_false() -> None:
    assert not is_endpoint_allowed("")
    assert not is_endpoint_denied("")
    with pytest.raises(EndpointNotAllowedError):
        assert_endpoint_allowed("")


def test_non_string_value_returns_false() -> None:
    # Non-strings must not crash; they simply fail closed.
    assert not is_endpoint_allowed(123)  # type: ignore[arg-type]
    assert not is_endpoint_denied(123)  # type: ignore[arg-type]
    with pytest.raises(EndpointNotAllowedError):
        assert_endpoint_allowed(None)  # type: ignore[arg-type]


def test_case_insensitive_matching() -> None:
    # Allowlist is case-insensitive on substrings.
    assert is_endpoint_allowed("/FAPI/V1/AGGTRADES")
    # Denylist is also case-insensitive.
    assert is_endpoint_denied("API_KEY=ABC")
