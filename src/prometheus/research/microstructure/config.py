"""Public-only microstructure scaffold configuration model.

Phase 4aw scaffold-only. Pure data model + validators. No I/O. No env
reads. No HTTP. No WebSocket. No file-system writes. No real config
load is implemented in Phase 4aw — callers construct
:class:`MicrostructureConfig` explicitly and pass it to
:func:`validate_config`.

The config refuses any reference that resembles a credential, private
endpoint, user stream, listenKey, order / account / position /
leverage / margin endpoint, MCP, Graphify, or ``.mcp.json``. Denylist
patterns are enforced against every endpoint reference and every
free-form value in dataset family / threshold blocks.

This module is intentionally narrow. It does not load files, parse
TOML/JSON, or fetch anything. Future phases (separately authorized)
may introduce a dedicated loader.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from .allowlist import (
    DENYLIST_TOKENS,
    EndpointNotAllowedError,
    is_endpoint_allowed,
    is_endpoint_denied,
)


class ConfigValidationError(ValueError):
    """Raised when :func:`validate_config` rejects a configuration."""


# Default symbol allowlist for Phase 4aw scaffold. Phase 4ac core symbol
# set is wider, but the Phase 4aw default is the BTC + ETH conservative
# pair. Callers may explicitly extend in their config.
DEFAULT_SYMBOL_ALLOWLIST: tuple[str, ...] = ("BTCUSDT", "ETHUSDT")


@dataclass(frozen=True)
class DatasetFamilyConfig:
    """Per-family scaffold config entry.

    ``layer`` must be one of ``raw``, ``normalized``, ``derived``.
    ``capture_mode`` must be one of ``rest_polling``,
    ``ws_live_capture_required``, ``historical_archive``.
    """

    family: str
    layer: str
    capture_mode: str
    schema_version: str
    endpoint_docs_reference: str

    def __post_init__(self) -> None:
        _reject_credential_shaped(self.family, "dataset_family.family")
        _reject_credential_shaped(self.layer, "dataset_family.layer")
        _reject_credential_shaped(self.capture_mode, "dataset_family.capture_mode")
        _reject_credential_shaped(self.schema_version, "dataset_family.schema_version")
        _reject_credential_shaped(
            self.endpoint_docs_reference, "dataset_family.endpoint_docs_reference"
        )
        if self.layer not in {"raw", "normalized", "derived"}:
            raise ConfigValidationError(
                f"dataset_family.layer must be one of raw|normalized|derived, "
                f"got {self.layer!r}"
            )
        if self.capture_mode not in {
            "rest_polling",
            "ws_live_capture_required",
            "historical_archive",
        }:
            raise ConfigValidationError(
                "dataset_family.capture_mode must be one of "
                "rest_polling|ws_live_capture_required|historical_archive, "
                f"got {self.capture_mode!r}"
            )


@dataclass(frozen=True)
class InvalidWindowThresholds:
    """Bounds for invalid-window detection used by the future eligibility gate."""

    max_clock_skew_ms: int = 1_000
    max_gap_after_reconnect_ms: int = 10_000
    max_stale_stream_ms: int = 5_000

    def __post_init__(self) -> None:
        for name, value in (
            ("max_clock_skew_ms", self.max_clock_skew_ms),
            ("max_gap_after_reconnect_ms", self.max_gap_after_reconnect_ms),
            ("max_stale_stream_ms", self.max_stale_stream_ms),
        ):
            if value < 0:
                raise ConfigValidationError(
                    f"invalid_window_thresholds.{name} must be >= 0, got {value}"
                )


@dataclass(frozen=True)
class EligibilityGateThresholds:
    """Pass thresholds for the future eligibility gate.

    Phase 4aw does NOT implement the eligibility gate. These bounds are
    recorded for the future inert manifest data model only.
    """

    max_invalid_window_fraction: float = 0.001
    max_missing_sequence_count: int = 0

    def __post_init__(self) -> None:
        if not 0.0 <= self.max_invalid_window_fraction <= 1.0:
            raise ConfigValidationError(
                "eligibility_gate_thresholds.max_invalid_window_fraction must be in "
                f"[0.0, 1.0], got {self.max_invalid_window_fraction}"
            )
        if self.max_missing_sequence_count < 0:
            raise ConfigValidationError(
                "eligibility_gate_thresholds.max_missing_sequence_count must be >= 0, "
                f"got {self.max_missing_sequence_count}"
            )


@dataclass(frozen=True)
class MicrostructureConfig:
    """Top-level scaffold config.

    All fields are required to be explicit. ``storage_root`` is a
    string label only — Phase 4aw does NOT create directories. The
    raw-writer primitive consumes a caller-provided ``root_dir`` at
    call time and validates it independently.
    """

    endpoint_allowlist: tuple[str, ...]
    endpoint_denylist: tuple[str, ...]
    symbol_allowlist: tuple[str, ...]
    storage_root: str
    dataset_family_config: tuple[DatasetFamilyConfig, ...]
    invalid_window_thresholds: InvalidWindowThresholds = field(
        default_factory=InvalidWindowThresholds
    )
    eligibility_gate_thresholds: EligibilityGateThresholds = field(
        default_factory=EligibilityGateThresholds
    )


def validate_config(
    config: MicrostructureConfig,
    *,
    explicit_extra_symbols: Mapping[str, str] | None = None,
) -> None:
    """Validate ``config`` against the public-only scaffold rules.

    Raises :class:`ConfigValidationError` (or
    :class:`EndpointNotAllowedError` for endpoint-allowlist violations)
    on any rejection. Callers may pass ``explicit_extra_symbols`` to
    explicitly admit symbols beyond the default allowlist; doing so is
    a deliberate caller decision and is logged here only by structural
    validation.
    """

    _reject_credential_shaped(config.storage_root, "storage_root")

    if not config.endpoint_allowlist:
        raise ConfigValidationError("endpoint_allowlist must not be empty")

    seen_allow: set[str] = set()
    for endpoint in config.endpoint_allowlist:
        # Allowlist entries are scrubbed by ``is_endpoint_denied`` /
        # ``is_endpoint_allowed`` directly so that denylisted endpoints
        # raise the more specific :class:`EndpointNotAllowedError`. We
        # still verify the entry is a non-empty string.
        if not isinstance(endpoint, str) or not endpoint:
            raise ConfigValidationError(
                f"endpoint_allowlist entry must be a non-empty string, got {endpoint!r}"
            )
        if endpoint in seen_allow:
            raise ConfigValidationError(
                f"endpoint_allowlist contains duplicate entry {endpoint!r}"
            )
        seen_allow.add(endpoint)
        if is_endpoint_denied(endpoint):
            raise EndpointNotAllowedError(
                f"endpoint_allowlist entry {endpoint!r} matches a denylisted token"
            )
        if not is_endpoint_allowed(endpoint):
            raise EndpointNotAllowedError(
                f"endpoint_allowlist entry {endpoint!r} is not on the public-only allowlist"
            )

    seen_deny: set[str] = set()
    for token in config.endpoint_denylist:
        _reject_credential_shaped(token, "endpoint_denylist[]", allow_denylist_token=True)
        if token in seen_deny:
            raise ConfigValidationError(
                f"endpoint_denylist contains duplicate entry {token!r}"
            )
        seen_deny.add(token)

    if not config.symbol_allowlist:
        raise ConfigValidationError("symbol_allowlist must not be empty")
    seen_sym: set[str] = set()
    for symbol in config.symbol_allowlist:
        _reject_credential_shaped(symbol, "symbol_allowlist[]")
        if not symbol.isupper() or not symbol.isalnum():
            raise ConfigValidationError(
                f"symbol_allowlist entry {symbol!r} must be uppercase alphanumeric"
            )
        if symbol in seen_sym:
            raise ConfigValidationError(
                f"symbol_allowlist contains duplicate entry {symbol!r}"
            )
        seen_sym.add(symbol)
        if symbol not in DEFAULT_SYMBOL_ALLOWLIST:
            extras = explicit_extra_symbols or {}
            if symbol not in extras:
                raise ConfigValidationError(
                    f"symbol_allowlist entry {symbol!r} is not in the default allowlist "
                    f"and was not passed via explicit_extra_symbols"
                )

    if not config.dataset_family_config:
        raise ConfigValidationError("dataset_family_config must not be empty")
    seen_family: set[str] = set()
    for entry in config.dataset_family_config:
        _reject_credential_shaped(entry.family, "dataset_family_config[].family")
        if entry.family in seen_family:
            raise ConfigValidationError(
                f"dataset_family_config contains duplicate family {entry.family!r}"
            )
        seen_family.add(entry.family)


def _reject_credential_shaped(
    value: str,
    field_label: str,
    *,
    allow_denylist_token: bool = False,
) -> None:
    """Reject any value containing a denylist token.

    When ``allow_denylist_token`` is true (used for the explicit
    ``endpoint_denylist`` block), denylist tokens are accepted as
    legitimate denylist contents. Other contexts must never contain
    denylist tokens — that is the entire point of the scaffold
    boundary.
    """

    if not isinstance(value, str):
        raise ConfigValidationError(f"{field_label} must be a string, got {type(value).__name__}")
    if not value:
        raise ConfigValidationError(f"{field_label} must not be empty")
    if allow_denylist_token:
        return
    lowered = value.lower()
    for token in DENYLIST_TOKENS:
        if token.lower() in lowered:
            raise ConfigValidationError(
                f"{field_label} value contains forbidden token {token!r}: "
                "credential, private, authenticated, or tooling-config references "
                "are rejected"
            )
