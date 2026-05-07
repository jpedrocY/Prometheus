"""Public-only Binance USDⓈ-M microstructure research scaffold.

Phase 4aw scope: scaffold-only. This package exposes inert primitives
intended to back a future public-only microstructure capture stack:

- ``config``: typed config model and validators (no I/O, no env reads);
- ``allowlist``: immutable public endpoint allowlist with denylist
  dominance for non-public surfaces;
- ``invalid_window``: 17-value invalid-window taxonomy with severity and
  downstream eligibility action enums plus a frozen dataclass model;
- ``manifest``: dataset manifest data model with ``research_eligible``
  defaulting to ``False`` and no public flip helper;
- ``raw_writer``: atomic write-then-rename raw event writer primitive
  with paired-SHA256 finalization; tests use pytest temp directories.

The scaffold is inert: it does not acquire data, contact endpoints,
open streams, download archives, run collectors / normalizers /
replay / eligibility gate, write to project ``data/microstructure/``,
or authorize any successor phase. See
``docs/00-meta/implementation-reports/2026-05-07_phase-4aw_*`` and
``docs/00-meta/implementation-reports/2026-05-07_phase-4av_*``.
"""

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
