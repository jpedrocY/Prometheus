"""Public GET-only Binance REST client for Phase 2c.

## TD-006 verification evidence (2026-04-19)

Verified against official Binance sources on 2026-04-19 via WebFetch
of the developer-docs pages below:

1. Base URL: ``https://fapi.binance.com``. Exactly one host; no
   third-party mirrors, no testnet.

2. Endpoints approved for Phase 2c:
     * ``GET /fapi/v1/fundingRate``
       docs: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History
       params: ``symbol`` (optional), ``startTime`` (LONG ms, optional),
               ``endTime`` (LONG ms, optional), ``limit`` (INT, default 100, max 1000)
       response: array of {symbol (STRING), fundingRate (STRING decimal),
                 fundingTime (LONG ms), markPrice (STRING decimal)}
       rate limit: verbatim — "share 500/5min/IP rate limit with
                   GET /fapi/v1/fundingInfo"
       pagination: ascending order; if records exceed limit, returned as
                   startTime + limit; callers advance startTime past
                   the last returned fundingTime.
     * ``GET /fapi/v1/exchangeInfo``
       docs: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information
       params: none
       weight: 1
       response top-level: {timezone, serverTime, rateLimits,
                            exchangeFilters, assets, symbols}

3. Authentication boundary (HARD):
   This module has NO api_key parameter, NO secret parameter,
   NO HMAC-SHA256 code, NO request-signing code, NO X-MBX-APIKEY
   header construction. A mechanical negative-attribute test
   (``test_binance_rest_has_no_auth_surface``) guards against drift.
   Any future authenticated access requires a separate module under a
   new phase gate.

Not touched by Phase 2c:
   - /fapi/v1/klines (covered by bulk downloader Phase 2b)
   - /fapi/v1/markPriceKlines (bulk source used; REST deferred)
   - /fapi/v1/leverageBracket (account-authenticated)
   - /fapi/v2/commissionRate (signed request)
   - /fapi/v1/account/*, /fapi/v1/userDataStream, WebSockets
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx

from prometheus.core.errors import PrometheusError

DEFAULT_BASE_URL = "https://fapi.binance.com"
_DEFAULT_USER_AGENT = "Prometheus-Research/0.0.0 (+https://github.com/jpedrocY/Prometheus)"

# Conservative pacing. Binance's fundingRate endpoint shares a
# 500 requests / 5 minutes / IP rate limit with fundingInfo (verified
# 2026-04-19 per Get-Funding-Rate-History docs). 500 / 300s ~= 1.67/s;
# we pace at >= 1000ms to stay well under with margin. exchangeInfo
# has weight 1 (tiny); the same pacing is acceptable because we make
# at most a few requests per run.
_DEFAULT_PACE_MS = 1000

_MAX_RETRIES = 5
_BACKOFF_START_S = 1.0
_BACKOFF_CAP_S = 30.0


class RestRequestError(PrometheusError):
    """Raised when a REST request fails permanently after retries."""


class BinanceRestClient:
    """Public GET-only Binance USD-M futures REST client.

    Takes a pre-configured :class:`httpx.Client` so tests can inject an
    ``httpx.MockTransport``. Emits only GET requests and only to
    ``base_url``. Has no authentication surface.
    """

    # Explicitly NOT defined (guarded by test_binance_rest_has_no_auth_surface):
    #   api_key, secret, key, apikey, sign_request, _sign, _hmac

    def __init__(
        self,
        client: httpx.Client,
        *,
        base_url: str = DEFAULT_BASE_URL,
        user_agent: str = _DEFAULT_USER_AGENT,
        pace_ms: int = _DEFAULT_PACE_MS,
        clock: Callable[[], float] | None = None,
        sleep: Callable[[float], None] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._user_agent = user_agent
        self._pace_ms = pace_ms
        self._monotonic = clock or time.monotonic
        self._sleep = sleep or time.sleep
        self._rng = rng or random.Random()
        self._last_request_at: float | None = None
        self._last_response_weight_1m: int | None = None

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def last_response_weight_1m(self) -> int | None:
        """Most recent ``X-MBX-USED-WEIGHT-1M`` value, if the last
        response included it. None otherwise."""
        return self._last_response_weight_1m

    def _pace(self) -> None:
        if self._last_request_at is None:
            self._last_request_at = self._monotonic()
            return
        elapsed_s = self._monotonic() - self._last_request_at
        required_s = self._pace_ms / 1000.0
        if elapsed_s < required_s:
            self._sleep(required_s - elapsed_s)
        self._last_request_at = self._monotonic()

    def _should_retry_status(self, status: int) -> bool:
        return status in {408, 425, 429} or 500 <= status < 600

    def _backoff(self, attempt: int) -> None:
        base = min(_BACKOFF_CAP_S, _BACKOFF_START_S * (2 ** (attempt - 1)))
        jitter = self._rng.uniform(0.0, base * 0.25)
        self._sleep(base + jitter)

    def _read_weight_header(self, response: httpx.Response) -> None:
        value = response.headers.get("X-MBX-USED-WEIGHT-1M")
        if value is None:
            self._last_response_weight_1m = None
            return
        try:
            self._last_response_weight_1m = int(value)
        except ValueError:
            self._last_response_weight_1m = None

    def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Issue a GET request and return the parsed JSON body.

        ``path`` must start with ``/`` and is appended to ``base_url``.
        No authenticated headers are ever added. Retries on 408/425/429
        and 5xx with exponential backoff; non-retriable 4xx raises
        immediately.
        """
        if not path.startswith("/"):
            raise ValueError(f"path must start with '/': {path!r}")
        url = f"{self._base_url}{path}"
        headers = {"User-Agent": self._user_agent}

        last_error: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            self._pace()
            try:
                response = self._client.get(url, params=params, headers=headers)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt >= _MAX_RETRIES:
                    break
                self._backoff(attempt)
                continue

            self._read_weight_header(response)

            if self._should_retry_status(response.status_code):
                last_error = RestRequestError(f"retriable HTTP {response.status_code} from {url}")
                if attempt >= _MAX_RETRIES:
                    break
                self._backoff(attempt)
                continue

            if response.status_code >= 400:
                raise RestRequestError(
                    f"non-retriable HTTP {response.status_code} from {url}: {response.text[:200]}"
                )

            return response.json()

        raise RestRequestError(f"exhausted {_MAX_RETRIES} retries fetching {url}: {last_error!r}")

    def save_raw_response(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        dest_path: Path,
    ) -> tuple[Any, str]:
        """Fetch JSON, persist the raw bytes to disk, and return
        ``(parsed, sha256_hex)``.

        Used by Phase 2c for auditable raw-response capture. The raw
        bytes are written atomically via ``.partial`` + rename. Returns
        both the parsed body (for immediate use) and the SHA256 for
        manifest inclusion.
        """
        import hashlib
        import json
        import os

        if not path.startswith("/"):
            raise ValueError(f"path must start with '/': {path!r}")
        url = f"{self._base_url}{path}"
        headers = {"User-Agent": self._user_agent}

        last_error: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            self._pace()
            try:
                response = self._client.get(url, params=params, headers=headers)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt >= _MAX_RETRIES:
                    break
                self._backoff(attempt)
                continue

            self._read_weight_header(response)

            if self._should_retry_status(response.status_code):
                last_error = RestRequestError(f"retriable HTTP {response.status_code} from {url}")
                if attempt >= _MAX_RETRIES:
                    break
                self._backoff(attempt)
                continue

            if response.status_code >= 400:
                raise RestRequestError(
                    f"non-retriable HTTP {response.status_code} from {url}: {response.text[:200]}"
                )

            body_bytes = response.content
            sha = hashlib.sha256(body_bytes).hexdigest()

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            partial = dest_path.with_suffix(dest_path.suffix + ".partial")
            partial.write_bytes(body_bytes)
            os.replace(partial, dest_path)

            try:
                parsed = json.loads(body_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RestRequestError(
                    f"response from {url} is not valid UTF-8 JSON: {exc}"
                ) from exc
            return parsed, sha

        raise RestRequestError(f"exhausted {_MAX_RETRIES} retries fetching {url}: {last_error!r}")
