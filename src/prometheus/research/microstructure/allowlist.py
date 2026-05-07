"""Public-only Binance USDⓈ-M endpoint allowlist and denylist.

Phase 4aw scaffold-only. This module is pure data + pure functions:
no HTTP, no WebSocket, no URL opening, no `.env` reads, no
credential lookup. The allowlist and denylist are both immutable
tuples; lookups use string membership and prefix/substring tests.

Denylist dominates allowlist: if any denylist token matches, the
endpoint is denied even if it also appears in the allowlist. This
preserves the Phase 4at / 4au / 4av governance that private,
authenticated, user stream, listenKey, order / account / position /
leverage / margin endpoints, MCP, Graphify, and ``.mcp.json``
references must never be admitted by this scaffold.

Mark-price endpoint references are listed in the allowlist for
completeness — Phase 3r §8 / Phase 3v §8 mark-price-domain governance
remains binding and any future mark-price work requires separate
authorization. This module does not consume those endpoints.
"""

from __future__ import annotations

# Public-only allowlist. Patterns reference Binance USDⓈ-M Futures
# public market data endpoints documented in Phase 4at §6 and
# Phase 4au §10. Matching is case-insensitive substring containment.
ALLOWLIST_PATTERNS: tuple[str, ...] = (
    # WebSocket public stream families
    "@aggTrade",
    "@bookTicker",
    "@depth",
    "@depth5",
    "@depth10",
    "@depth20",
    "@forceOrder",
    "@markPrice",
    "@indexPrice",
    # REST public endpoints (paths)
    "/fapi/v1/aggTrades",
    "/fapi/v1/depth",
    "/fapi/v1/klines",
    "/fapi/v1/markPriceKlines",
    "/fapi/v1/indexPriceKlines",
    "/fapi/v1/premiumIndexKlines",
    "/fapi/v1/fundingRate",
    "/fapi/v1/fundingInfo",
    "/fapi/v1/openInterest",
    "/futures/data/openInterestHist",
    "/futures/data/topLongShortAccountRatio",
    "/futures/data/topLongShortPositionRatio",
    "/futures/data/globalLongShortAccountRatio",
    "/futures/data/takerlongshortRatio",
    # Logical labels used by the future capture stack
    "aggtrade_ws",
    "book_ticker_ws",
    "diff_depth_ws",
    "partial_depth_ws",
    "force_order_ws",
    "mark_price_ws",
    "index_price_ws",
    "rest_depth_snapshot",
    "rest_funding_rate_history",
    "rest_open_interest_snapshot",
    "rest_open_interest_hist",
    "rest_long_short_ratio",
    "rest_taker_long_short_ratio",
)

# Denylist patterns. Any value containing one of these (case-insensitive)
# is denied regardless of allowlist membership.
DENYLIST_TOKENS: tuple[str, ...] = (
    # private / authenticated REST endpoint paths
    "/fapi/v1/order",
    "/fapi/v1/allOrders",
    "/fapi/v1/openOrders",
    "/fapi/v1/forceOrders",  # user-scope authenticated; do not confuse with @forceOrder WS
    "/fapi/v2/account",
    "/fapi/v2/positionRisk",
    "/fapi/v2/balance",
    "/fapi/v1/leverage",
    "/fapi/v1/marginType",
    "/fapi/v1/positionMargin",
    "/fapi/v1/income",
    "/fapi/v1/listenKey",
    "/fapi/v1/userTrades",
    # user data stream / listenKey
    "userDataStream",
    "listenKey",
    # credential-shaped strings
    "api_key",
    "apiKey",
    "secret_key",
    "secretKey",
    "X-MBX-APIKEY",
    "signature",
    # tooling & config we explicitly forbid in scaffold contexts
    ".mcp.json",
    "MCP",
    "Graphify",
    # generic credential references
    ".env",
)


class EndpointNotAllowedError(ValueError):
    """Raised when an endpoint reference is denied or absent from the allowlist."""


def is_endpoint_denied(value: str) -> bool:
    """Return True if ``value`` matches any denylist token (case-insensitive)."""
    if not isinstance(value, str) or not value:
        return False
    lowered = value.lower()
    return any(token.lower() in lowered for token in DENYLIST_TOKENS)


def is_endpoint_allowed(value: str) -> bool:
    """Return True if ``value`` is on the public-only allowlist and not denied.

    Denylist dominates: a value matching any denylist token returns
    ``False`` even if it also matches an allowlist pattern.
    """
    if not isinstance(value, str) or not value:
        return False
    if is_endpoint_denied(value):
        return False
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in ALLOWLIST_PATTERNS)


def assert_endpoint_allowed(value: str) -> None:
    """Raise :class:`EndpointNotAllowedError` unless ``value`` is allowed.

    The error message distinguishes denylist dominance ("denied") from
    plain absence from the allowlist ("not on allowlist").
    """
    if not isinstance(value, str) or not value:
        raise EndpointNotAllowedError(
            f"endpoint reference must be a non-empty string, got {value!r}"
        )
    if is_endpoint_denied(value):
        raise EndpointNotAllowedError(
            f"endpoint reference {value!r} matches a denylisted token "
            "(private / authenticated / user stream / listenKey / order / account / "
            "leverage / margin / MCP / Graphify / credential-shaped)"
        )
    if not is_endpoint_allowed(value):
        raise EndpointNotAllowedError(
            f"endpoint reference {value!r} is not on the public-only allowlist"
        )
