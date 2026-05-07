"""Public-only aggTrades-only microstructure collector skeleton.

Phase 4ax scaffold. This module is the next inert public-only
microstructure implementation layer on top of the Phase 4aw scaffold:
it validates mocked / offline aggTrade payloads, derives taker side,
enforces the public-only endpoint allowlist, builds dry-run collection
plans, and (when explicitly given a caller-provided path) composes
:class:`prometheus.research.microstructure.raw_writer.RawWriter` to
write validated payloads to a pytest temporary directory.

This module is inert: it does not contact endpoints, open WebSockets,
download archives, write under project ``data/microstructure/``, or
acquire real data. The Phase 4aw allowlist + denylist govern every
endpoint reference. The Phase 4aw raw-writer governs every file path.

Design choices:

- Pure standard library. No `httpx` / `requests` / `aiohttp` /
  `websockets` / `binance` / `urllib.request` / `socket` / `dotenv` /
  `os.environ` reads.
- ``Decimal`` for price and quantity to avoid float surprises. Inputs
  may be provided as strings (Binance public format) or numeric
  values, but are always normalised to ``Decimal``.
- Frozen dataclasses with explicit ``__post_init__`` validation.
- A :class:`TakerSide` enum (``BUY`` / ``SELL``) is derived from the
  ``m`` (buyer-is-maker) flag using the standard convention.
- No `data/microstructure/...` directory creation. Tests use pytest
  ``tmp_path`` only. The raw-writer enforces this boundary.
- No real manifest is created. Returning an
  :class:`AggTradeWriteResult` is the explicit handoff contract for a
  future caller that may translate it into a manifest entry; the
  translation step is **not** implemented in this phase.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal, DecimalException, getcontext
from enum import StrEnum
from pathlib import Path

from .allowlist import EndpointNotAllowedError, assert_endpoint_allowed
from .config import DEFAULT_SYMBOL_ALLOWLIST
from .raw_writer import RawWriter, RawWriterFileSummary

# Decimal precision: 28 is plenty for crypto price * quantity.
getcontext().prec = 28


# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #


class AggTradesError(RuntimeError):
    """Base exception for the aggTrades scaffold."""


class AggTradeValidationError(AggTradesError):
    """Raised when a payload fails validation."""


class AggTradePlanError(AggTradesError):
    """Raised when a dry-run plan is rejected."""


# --------------------------------------------------------------------------- #
# Enums
# --------------------------------------------------------------------------- #


class TakerSide(StrEnum):
    """Side of the *taker* in an aggregate trade.

    Convention: ``m`` is the *buyer-is-maker* flag in Binance aggTrade
    payloads. If ``m`` is true, the buyer was the maker, so the taker
    side is ``SELL``; otherwise the taker side is ``BUY``.
    """

    BUY = "BUY"
    SELL = "SELL"


class AggTradeMode(StrEnum):
    """Dry-run plan mode."""

    ARCHIVE = "archive"
    REST = "rest"
    WS = "ws"


# --------------------------------------------------------------------------- #
# Data models
# --------------------------------------------------------------------------- #


# Required and optional Binance aggTrade fields. ``E`` (event time) is
# present only on stream-shaped payloads.
_REQUIRED_FIELDS: tuple[str, ...] = ("a", "p", "q", "f", "l", "T", "m")
_OPTIONAL_FIELDS: tuple[str, ...] = ("E",)
_KNOWN_FIELDS: frozenset[str] = frozenset(_REQUIRED_FIELDS + _OPTIONAL_FIELDS)


@dataclass(frozen=True)
class AggTradePayload:
    """One validated Binance aggregate trade payload.

    Prices and quantities are stored as :class:`decimal.Decimal` to
    avoid float surprises. ``taker_side`` is derived from
    ``buyer_is_maker``. Unknown extra payload fields are preserved
    verbatim in :attr:`extra_fields` and do not affect validation.
    """

    aggregate_trade_id: int
    price: Decimal
    quantity: Decimal
    first_trade_id: int
    last_trade_id: int
    trade_time_ms: int
    buyer_is_maker: bool
    taker_side: TakerSide
    event_time_ms: int | None = None
    extra_fields: Mapping[str, object] = field(default_factory=dict)

    def to_record(self) -> dict[str, object]:
        """Serialize to a JSON-safe record for the raw writer.

        ``Decimal`` values are emitted as strings to preserve precision
        in JSONL output. ``event_time_ms`` is required by the raw
        writer; for REST-shaped payloads we use ``trade_time_ms`` as
        the event-time stand-in (the writer uses event time only for
        bound tracking, not for replay correctness).
        """
        et = self.event_time_ms if self.event_time_ms is not None else self.trade_time_ms
        record: dict[str, object] = {
            "event_time_ms": et,
            "aggregate_trade_id": self.aggregate_trade_id,
            "price": str(self.price),
            "quantity": str(self.quantity),
            "first_trade_id": self.first_trade_id,
            "last_trade_id": self.last_trade_id,
            "trade_time_ms": self.trade_time_ms,
            "buyer_is_maker": self.buyer_is_maker,
            "taker_side": self.taker_side.value,
        }
        if self.event_time_ms is not None:
            record["event_time_ms_source"] = "stream"
        else:
            record["event_time_ms_source"] = "trade_time"
        if self.extra_fields:
            record["extra_fields"] = dict(self.extra_fields)
        return record


@dataclass(frozen=True)
class AggTradePlan:
    """A dry-run aggTrades collection plan.

    Contains only descriptive metadata. No directory is created. No
    endpoint is contacted. No data is written.
    """

    symbol: str
    mode: AggTradeMode
    dataset_family: str
    endpoint_reference: str
    capture_mode_label: str
    planned_output_root: str | None
    planned_path_label: str
    start_time_ms: int | None
    end_time_ms: int | None


@dataclass(frozen=True)
class AggTradeWriteResult:
    """Summary of a temp-path writer run.

    The summary is the explicit handoff contract for a future caller
    that may translate it into a manifest entry. The translation step
    is **not** implemented in Phase 4ax.
    """

    target_path: str
    sha256: str
    record_count: int
    start_time_ms: int
    end_time_ms: int
    taker_side_buy_count: int
    taker_side_sell_count: int


# --------------------------------------------------------------------------- #
# Payload validation
# --------------------------------------------------------------------------- #


def validate_aggtrade_payload(payload: Mapping[str, object]) -> AggTradePayload:
    """Validate one aggTrade payload mapping and return an :class:`AggTradePayload`.

    Accepts both REST-shaped payloads (no ``E``) and stream-shaped
    payloads (with ``E``). Raises :class:`AggTradeValidationError` on
    any rejection.
    """
    if not isinstance(payload, Mapping):
        raise AggTradeValidationError(
            f"payload must be a Mapping, got {type(payload).__name__}"
        )

    for key in _REQUIRED_FIELDS:
        if key not in payload:
            raise AggTradeValidationError(f"missing required field {key!r}")

    aggregate_trade_id = _coerce_int(payload["a"], "a")
    if aggregate_trade_id < 0:
        raise AggTradeValidationError(f"a must be >= 0, got {aggregate_trade_id}")

    price = _coerce_positive_decimal(payload["p"], "p")
    quantity = _coerce_positive_decimal(payload["q"], "q")

    first_trade_id = _coerce_int(payload["f"], "f")
    if first_trade_id < 0:
        raise AggTradeValidationError(f"f must be >= 0, got {first_trade_id}")

    last_trade_id = _coerce_int(payload["l"], "l")
    if last_trade_id < first_trade_id:
        raise AggTradeValidationError(
            f"l ({last_trade_id}) must be >= f ({first_trade_id})"
        )

    trade_time_ms = _coerce_int(payload["T"], "T")
    if trade_time_ms <= 0:
        raise AggTradeValidationError(f"T must be > 0, got {trade_time_ms}")

    buyer_is_maker_raw = payload["m"]
    if not isinstance(buyer_is_maker_raw, bool):
        raise AggTradeValidationError(
            f"m must be a bool, got {type(buyer_is_maker_raw).__name__}"
        )
    buyer_is_maker = buyer_is_maker_raw
    taker_side = TakerSide.SELL if buyer_is_maker else TakerSide.BUY

    event_time_ms: int | None = None
    if "E" in payload:
        event_time_ms = _coerce_int(payload["E"], "E")
        if event_time_ms <= 0:
            raise AggTradeValidationError(f"E must be > 0 if present, got {event_time_ms}")

    extra: dict[str, object] = {
        k: v for k, v in payload.items() if k not in _KNOWN_FIELDS
    }

    return AggTradePayload(
        aggregate_trade_id=aggregate_trade_id,
        price=price,
        quantity=quantity,
        first_trade_id=first_trade_id,
        last_trade_id=last_trade_id,
        trade_time_ms=trade_time_ms,
        buyer_is_maker=buyer_is_maker,
        taker_side=taker_side,
        event_time_ms=event_time_ms,
        extra_fields=extra,
    )


def _coerce_int(value: object, field_label: str) -> int:
    """Coerce ``value`` to ``int``, rejecting bools and non-integer-shaped inputs."""
    if isinstance(value, bool):
        raise AggTradeValidationError(f"{field_label} must be an int, got bool")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError as exc:
            raise AggTradeValidationError(
                f"{field_label} must be an int-shaped string, got {value!r}"
            ) from exc
    raise AggTradeValidationError(
        f"{field_label} must be an int or int-shaped string, got {type(value).__name__}"
    )


def _coerce_positive_decimal(value: object, field_label: str) -> Decimal:
    """Coerce ``value`` to a positive :class:`decimal.Decimal`."""
    if isinstance(value, bool):
        raise AggTradeValidationError(f"{field_label} must be numeric, got bool")
    if isinstance(value, Decimal):
        decimal_value = value
    elif isinstance(value, int):
        decimal_value = Decimal(value)
    elif isinstance(value, str):
        if not value:
            raise AggTradeValidationError(f"{field_label} must not be empty")
        try:
            decimal_value = Decimal(value)
        except DecimalException as exc:
            raise AggTradeValidationError(
                f"{field_label} must be a decimal-shaped string, got {value!r}"
            ) from exc
    elif isinstance(value, float):
        # Floats are accepted for test convenience but converted via str
        # to avoid binary-float artifacts.
        try:
            decimal_value = Decimal(str(value))
        except DecimalException as exc:
            raise AggTradeValidationError(
                f"{field_label} float could not be converted to Decimal: {value!r}"
            ) from exc
    else:
        raise AggTradeValidationError(
            f"{field_label} must be numeric, got {type(value).__name__}"
        )
    if not decimal_value.is_finite():
        raise AggTradeValidationError(f"{field_label} must be finite, got {decimal_value}")
    if decimal_value <= 0:
        raise AggTradeValidationError(f"{field_label} must be > 0, got {decimal_value}")
    return decimal_value


# --------------------------------------------------------------------------- #
# Endpoint allowlist enforcement
# --------------------------------------------------------------------------- #


_AGGTRADES_ALLOWED_ENDPOINT_FRAGMENTS: tuple[str, ...] = (
    "/fapi/v1/aggTrades",
    "@aggTrade",
    "aggtrade_ws",
)


def assert_aggtrades_endpoint_allowed(endpoint: str) -> None:
    """Assert that ``endpoint`` is on the public-only allowlist *and* aggTrades-shaped.

    First defers to the Phase 4aw allowlist (which raises
    :class:`EndpointNotAllowedError` for denylisted or non-public-only
    references). Then requires that the endpoint contain at least one
    aggTrades-shaped fragment.
    """
    assert_endpoint_allowed(endpoint)
    lowered = endpoint.lower()
    for fragment in _AGGTRADES_ALLOWED_ENDPOINT_FRAGMENTS:
        if fragment.lower() in lowered:
            return
    raise EndpointNotAllowedError(
        f"endpoint reference {endpoint!r} is on the public-only allowlist but is not "
        "aggTrades-shaped (expected one of /fapi/v1/aggTrades, @aggTrade, aggtrade_ws)"
    )


# --------------------------------------------------------------------------- #
# Dry-run plan
# --------------------------------------------------------------------------- #


_MODE_TO_ENDPOINT_REFERENCE: dict[AggTradeMode, str] = {
    AggTradeMode.ARCHIVE: "data.binance.vision/futures-um-aggTrades-monthly",
    AggTradeMode.REST: "/fapi/v1/aggTrades",
    AggTradeMode.WS: "@aggTrade",
}


_MODE_TO_CAPTURE_LABEL: dict[AggTradeMode, str] = {
    AggTradeMode.ARCHIVE: "historical_archive",
    AggTradeMode.REST: "rest_polling",
    AggTradeMode.WS: "ws_live_capture_required",
}


def build_aggtrades_plan(
    *,
    symbol: str,
    mode: AggTradeMode | str,
    start_time_ms: int | None = None,
    end_time_ms: int | None = None,
    output_root: str | None = None,
    dataset_family: str = "microstructure_raw_aggtrades_v001",
    explicit_extra_symbols: Mapping[str, str] | None = None,
) -> AggTradePlan:
    """Build a dry-run aggTrades collection plan.

    No directories are created. No endpoints are contacted. No data is
    written. The returned :class:`AggTradePlan` is descriptive only.

    Symbol admission mirrors the Phase 4aw config validator: the
    default allowlist is ``("BTCUSDT", "ETHUSDT")``; alt symbols
    require explicit caller admission via ``explicit_extra_symbols``.
    """
    if not isinstance(symbol, str) or not symbol:
        raise AggTradePlanError("symbol must be a non-empty string")
    if not symbol.isupper() or not symbol.isalnum():
        raise AggTradePlanError(f"symbol {symbol!r} must be uppercase alphanumeric")
    if symbol not in DEFAULT_SYMBOL_ALLOWLIST:
        extras = explicit_extra_symbols or {}
        if symbol not in extras:
            raise AggTradePlanError(
                f"symbol {symbol!r} is not in the default allowlist and was not "
                "passed via explicit_extra_symbols"
            )

    if isinstance(mode, str) and not isinstance(mode, AggTradeMode):
        try:
            mode_enum = AggTradeMode(mode)
        except ValueError as exc:
            raise AggTradePlanError(
                f"mode must be one of {[m.value for m in AggTradeMode]}, got {mode!r}"
            ) from exc
    elif isinstance(mode, AggTradeMode):
        mode_enum = mode
    else:
        raise AggTradePlanError(
            f"mode must be an AggTradeMode or str, got {type(mode).__name__}"
        )

    if start_time_ms is not None and not isinstance(start_time_ms, int):
        raise AggTradePlanError("start_time_ms must be an int or None")
    if end_time_ms is not None and not isinstance(end_time_ms, int):
        raise AggTradePlanError("end_time_ms must be an int or None")
    if start_time_ms is not None and start_time_ms < 0:
        raise AggTradePlanError("start_time_ms must be >= 0")
    if end_time_ms is not None and end_time_ms < 0:
        raise AggTradePlanError("end_time_ms must be >= 0")
    if (
        start_time_ms is not None
        and end_time_ms is not None
        and start_time_ms > end_time_ms
    ):
        raise AggTradePlanError(
            f"start_time_ms ({start_time_ms}) must be <= end_time_ms ({end_time_ms})"
        )

    if not isinstance(dataset_family, str) or not dataset_family:
        raise AggTradePlanError("dataset_family must be a non-empty string")
    if not dataset_family.startswith("microstructure_raw_aggtrades"):
        raise AggTradePlanError(
            f"dataset_family must start with 'microstructure_raw_aggtrades', got "
            f"{dataset_family!r}"
        )

    if output_root is not None and not isinstance(output_root, str):
        raise AggTradePlanError("output_root must be a string or None")

    endpoint_reference = _MODE_TO_ENDPOINT_REFERENCE[mode_enum]
    if mode_enum is not AggTradeMode.ARCHIVE:
        # Allowlist-check the live endpoint label. The archive label is
        # a fixed bulk-archive descriptor and is not part of the
        # public-only API allowlist; allowlisting it is the
        # responsibility of a future archive-acquisition phase.
        assert_aggtrades_endpoint_allowed(endpoint_reference)

    capture_mode_label = _MODE_TO_CAPTURE_LABEL[mode_enum]
    planned_path_label = (
        f"{output_root or '<UNSET>'}/{dataset_family}/{symbol}/<dry-run-only>"
    )

    return AggTradePlan(
        symbol=symbol,
        mode=mode_enum,
        dataset_family=dataset_family,
        endpoint_reference=endpoint_reference,
        capture_mode_label=capture_mode_label,
        planned_output_root=output_root,
        planned_path_label=planned_path_label,
        start_time_ms=start_time_ms,
        end_time_ms=end_time_ms,
    )


# --------------------------------------------------------------------------- #
# Temp-path writer composition
# --------------------------------------------------------------------------- #


def write_validated_aggtrades_to_path(
    payloads: Sequence[Mapping[str, object]],
    target_path: Path,
) -> AggTradeWriteResult:
    """Validate and write ``payloads`` to ``target_path`` via :class:`RawWriter`.

    The caller-provided ``target_path`` is forwarded to
    :class:`RawWriter`, which refuses paths under
    ``data/microstructure/`` regardless of OS separator. Tests use
    pytest ``tmp_path``.

    Validation failure does NOT leave a finalized file behind: the
    underlying :class:`RawWriter` keeps a ``.tmp`` companion until
    ``close()`` is called, so an exception during validation aborts
    the write and leaves only the ``.tmp`` artefact for operator
    inspection. A future caller may translate the returned summary
    into a manifest entry; that translation is **not** implemented in
    Phase 4ax.
    """
    if not isinstance(payloads, Sequence) or isinstance(payloads, (str, bytes)):
        raise AggTradesError(
            f"payloads must be a Sequence of Mapping, got {type(payloads).__name__}"
        )

    buy_count = 0
    sell_count = 0
    summary: RawWriterFileSummary
    # Use ``with`` so that any exception during validation lets
    # :meth:`RawWriter.__exit__` release the underlying file handle
    # while leaving the ``.tmp`` companion on disk for operator
    # inspection (the writer never finalises on failure because
    # ``close()`` is reached only on the happy path).
    with RawWriter(target_path) as writer:
        for index, payload in enumerate(payloads):
            try:
                validated = validate_aggtrade_payload(payload)
            except AggTradeValidationError as exc:
                raise AggTradeValidationError(
                    f"payload at index {index} failed validation: {exc}"
                ) from exc
            writer.append(validated.to_record())
            if validated.taker_side is TakerSide.BUY:
                buy_count += 1
            else:
                sell_count += 1
        summary = writer.close()

    return AggTradeWriteResult(
        target_path=summary.path,
        sha256=summary.sha256,
        record_count=summary.event_count,
        start_time_ms=summary.start_time_ms,
        end_time_ms=summary.end_time_ms,
        taker_side_buy_count=buy_count,
        taker_side_sell_count=sell_count,
    )


__all__ = [
    "AggTradeMode",
    "AggTradePayload",
    "AggTradePlan",
    "AggTradePlanError",
    "AggTradeWriteResult",
    "AggTradeValidationError",
    "AggTradesError",
    "TakerSide",
    "assert_aggtrades_endpoint_allowed",
    "build_aggtrades_plan",
    "validate_aggtrade_payload",
    "write_validated_aggtrades_to_path",
]


def _supported_aggtrades_endpoint_fragments() -> tuple[str, ...]:
    """Public read-only accessor used by tests / introspection."""
    return _AGGTRADES_ALLOWED_ENDPOINT_FRAGMENTS
