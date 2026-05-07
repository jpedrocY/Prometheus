"""Public-only Binance USDⓈ-M microstructure research scaffold.

Phase 4aw scope: scaffold-only inert primitives:

- ``config``: typed config model and validators (no I/O, no env reads);
- ``allowlist``: immutable public endpoint allowlist with denylist
  dominance for non-public surfaces;
- ``invalid_window``: 17-value invalid-window taxonomy with severity and
  downstream eligibility action enums plus a frozen dataclass model;
- ``manifest``: dataset manifest data model with ``research_eligible``
  defaulting to ``False`` and no public flip helper;
- ``raw_writer``: atomic write-then-rename raw event writer primitive
  with paired-SHA256 finalization; tests use pytest temp directories.

Phase 4ax adds an aggTrades-only collector skeleton:

- ``aggtrades``: payload validator (REST or stream-shaped Binance
  aggTrade payloads), taker-side derivation, dry-run plan builder,
  and an explicit caller-provided-path writer that composes
  :class:`raw_writer.RawWriter` for use in pytest temp directories.

Both layers are inert: no data acquisition, no endpoint contact, no
streams, no archive downloads, no collectors / normalizers / replay /
eligibility-gate execution, no writes under project
``data/microstructure/``, no successor authorization. See
``docs/00-meta/implementation-reports/2026-05-07_phase-4aw_*`` and
``docs/00-meta/implementation-reports/2026-05-07_phase-4ax_*``.
"""

from .aggtrades import (
    AggTradeMode,
    AggTradePayload,
    AggTradePlan,
    AggTradePlanError,
    AggTradesError,
    AggTradeValidationError,
    AggTradeWriteResult,
    TakerSide,
    assert_aggtrades_endpoint_allowed,
    build_aggtrades_plan,
    validate_aggtrade_payload,
    write_validated_aggtrades_to_path,
)
from .allowlist import (
    EndpointNotAllowedError,
    assert_endpoint_allowed,
    is_endpoint_allowed,
    is_endpoint_denied,
)
from .config import (
    ConfigValidationError,
    DatasetFamilyConfig,
    EligibilityGateThresholds,
    InvalidWindowThresholds,
    MicrostructureConfig,
    validate_config,
)
from .invalid_window import (
    DownstreamEligibilityAction,
    InvalidWindow,
    InvalidWindowReason,
    InvalidWindowSeverity,
)
from .manifest import (
    EligibilityGateStatus,
    FileEntry,
    ManifestImmutableError,
    MicrostructureManifest,
)
from .raw_writer import (
    RawWriter,
    RawWriterAlreadyExistsError,
    RawWriterError,
    RawWriterFileSummary,
    RawWriterPathError,
)

__all__ = [
    # aggtrades
    "AggTradeMode",
    "AggTradePayload",
    "AggTradePlan",
    "AggTradePlanError",
    "AggTradeValidationError",
    "AggTradeWriteResult",
    "AggTradesError",
    "TakerSide",
    "assert_aggtrades_endpoint_allowed",
    "build_aggtrades_plan",
    "validate_aggtrade_payload",
    "write_validated_aggtrades_to_path",
    # config
    "ConfigValidationError",
    "DatasetFamilyConfig",
    "EligibilityGateThresholds",
    "InvalidWindowThresholds",
    "MicrostructureConfig",
    "validate_config",
    # allowlist
    "EndpointNotAllowedError",
    "assert_endpoint_allowed",
    "is_endpoint_allowed",
    "is_endpoint_denied",
    # invalid_window
    "DownstreamEligibilityAction",
    "InvalidWindow",
    "InvalidWindowReason",
    "InvalidWindowSeverity",
    # manifest
    "EligibilityGateStatus",
    "FileEntry",
    "ManifestImmutableError",
    "MicrostructureManifest",
    # raw_writer
    "RawWriter",
    "RawWriterAlreadyExistsError",
    "RawWriterError",
    "RawWriterFileSummary",
    "RawWriterPathError",
]
