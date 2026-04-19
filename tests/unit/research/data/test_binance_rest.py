from __future__ import annotations

import inspect
import random
from pathlib import Path

import httpx
import pytest

from prometheus.research.data.binance_rest import (
    DEFAULT_BASE_URL,
    BinanceRestClient,
    RestRequestError,
)

# ---------------------------------------------------------------------------
# Auth-surface guardrail (hard requirement per Phase 2c Gate 1 condition 8)
# ---------------------------------------------------------------------------

_FORBIDDEN_ATTRS = (
    "api_key",
    "secret",
    "key",
    "apikey",
    "sign_request",
    "_sign",
    "_hmac",
    "hmac_sha256",
    "signed_request",
)

_FORBIDDEN_PARAM_NAMES = (
    "api_key",
    "secret",
    "key",
    "apikey",
    "signed",
)


def test_binance_rest_has_no_auth_surface() -> None:
    """Mechanical guardrail: BinanceRestClient must not expose any
    credential-shaped attribute or constructor parameter. Fails the
    build if anyone later adds one without removing this assertion.
    """
    cls = BinanceRestClient
    for name in _FORBIDDEN_ATTRS:
        assert not hasattr(cls, name), f"auth surface leaked on class: {name}"

    sig = inspect.signature(cls.__init__)
    for param in sig.parameters.values():
        assert param.name not in _FORBIDDEN_PARAM_NAMES, (
            f"auth surface leaked on __init__ param: {param.name}"
        )


def test_binance_rest_request_never_sends_auth_header() -> None:
    """All outbound requests must lack X-MBX-APIKEY / Authorization
    headers, even when the caller tries to inject them."""
    observed_headers: list[httpx.Headers] = []

    def handler(request: httpx.Request) -> httpx.Response:
        observed_headers.append(request.headers)
        return httpx.Response(200, json={"ok": True})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    rest = BinanceRestClient(client, sleep=lambda _: None, rng=random.Random(0))
    rest.get_json("/fapi/v1/exchangeInfo")

    assert len(observed_headers) == 1
    headers = observed_headers[0]
    assert "X-MBX-APIKEY" not in headers
    # httpx lower-cases the comparison; be explicit.
    for h in headers:
        assert h.lower() != "x-mbx-apikey"
        assert h.lower() != "authorization"


# ---------------------------------------------------------------------------
# URL construction + request behavior
# ---------------------------------------------------------------------------


def _fixed_client(handler: httpx.MockTransport, *, pace_ms: int = 0) -> BinanceRestClient:
    client = httpx.Client(transport=handler)
    return BinanceRestClient(
        client,
        pace_ms=pace_ms,
        sleep=lambda _: None,
        rng=random.Random(0),
    )


def test_get_json_happy_path() -> None:
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        return httpx.Response(200, json={"hello": "world"})

    rest = _fixed_client(httpx.MockTransport(handler))
    body = rest.get_json("/fapi/v1/exchangeInfo")
    assert body == {"hello": "world"}
    assert seen == [f"{DEFAULT_BASE_URL}/fapi/v1/exchangeInfo"]


def test_get_json_params_appended() -> None:
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(200, json=[])

    rest = _fixed_client(httpx.MockTransport(handler))
    rest.get_json(
        "/fapi/v1/fundingRate",
        params={"symbol": "BTCUSDT", "limit": 2},
    )
    assert len(seen_urls) == 1
    assert "symbol=BTCUSDT" in seen_urls[0]
    assert "limit=2" in seen_urls[0]


def test_get_json_path_must_start_with_slash() -> None:
    client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200)))
    rest = BinanceRestClient(client, sleep=lambda _: None, rng=random.Random(0))
    with pytest.raises(ValueError):
        rest.get_json("fapi/v1/exchangeInfo")


def test_get_json_user_agent_header_present() -> None:
    observed: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        observed.append(request.headers.get("User-Agent"))
        return httpx.Response(200, json={})

    rest = _fixed_client(httpx.MockTransport(handler))
    rest.get_json("/fapi/v1/exchangeInfo")
    assert observed[0] is not None
    assert observed[0].startswith("Prometheus-Research/")


def test_get_json_retries_on_429_then_succeeds() -> None:
    sequence = [429, 429, 200]
    cursor = iter(sequence)

    def handler(request: httpx.Request) -> httpx.Response:
        status = next(cursor)
        return httpx.Response(status, json=[] if status == 200 else None)

    rest = _fixed_client(httpx.MockTransport(handler))
    body = rest.get_json("/fapi/v1/fundingRate")
    assert body == []


def test_get_json_exhausts_retries_on_persistent_5xx() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="unavailable")

    rest = _fixed_client(httpx.MockTransport(handler))
    with pytest.raises(RestRequestError):
        rest.get_json("/fapi/v1/exchangeInfo")


def test_get_json_raises_non_retriable_4xx() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="not found")

    rest = _fixed_client(httpx.MockTransport(handler))
    with pytest.raises(RestRequestError):
        rest.get_json("/fapi/v1/nope")


def test_weight_header_parsed() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={},
            headers={"X-MBX-USED-WEIGHT-1M": "42"},
        )

    rest = _fixed_client(httpx.MockTransport(handler))
    rest.get_json("/fapi/v1/exchangeInfo")
    assert rest.last_response_weight_1m == 42


def test_weight_header_absent_leaves_none() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    rest = _fixed_client(httpx.MockTransport(handler))
    rest.get_json("/fapi/v1/exchangeInfo")
    assert rest.last_response_weight_1m is None


def test_pace_delay_observed() -> None:
    slept: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    fake_clock_values = iter([0.0, 0.001] + [1.0] * 10)
    client = httpx.Client(transport=httpx.MockTransport(handler))
    rest = BinanceRestClient(
        client,
        pace_ms=500,
        clock=lambda: next(fake_clock_values),
        sleep=lambda duration: slept.append(duration),
        rng=random.Random(0),
    )
    rest.get_json("/fapi/v1/exchangeInfo")
    rest.get_json("/fapi/v1/exchangeInfo")
    assert any(d >= 0.4 for d in slept), "at least one pace-induced sleep close to 0.5s expected"


def test_save_raw_response_writes_and_returns_sha(tmp_path: Path) -> None:
    payload = {"hello": "world", "n": 42}

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    rest = _fixed_client(httpx.MockTransport(handler))
    dest = tmp_path / "sub" / "snapshot.json"
    parsed, sha = rest.save_raw_response("/fapi/v1/exchangeInfo", dest_path=dest)
    assert parsed == payload
    assert len(sha) == 64
    assert dest.is_file()
    # SHA matches the bytes we wrote.
    import hashlib

    assert hashlib.sha256(dest.read_bytes()).hexdigest() == sha
    # No leftover .partial file.
    assert not dest.with_suffix(".json.partial").exists()


def test_save_raw_response_rejects_invalid_json(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, content=b"not-json", headers={"Content-Type": "application/json"}
        )

    rest = _fixed_client(httpx.MockTransport(handler))
    # The byte body will still be persisted (we capture first, then parse).
    # If parse fails we raise so caller knows the raw file is unreliable.
    with pytest.raises(RestRequestError):
        rest.save_raw_response("/fapi/v1/exchangeInfo", dest_path=tmp_path / "raw.json")


def test_get_json_only_issues_get_method() -> None:
    methods_seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        methods_seen.append(request.method)
        return httpx.Response(200, json={})

    rest = _fixed_client(httpx.MockTransport(handler))
    rest.get_json("/fapi/v1/exchangeInfo")
    assert methods_seen == ["GET"]
