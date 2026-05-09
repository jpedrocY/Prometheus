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

Phase 4bb-C adds the offline eligibility-gate primitive:

- ``eligibility_io``: read-only artefact loaders + single-pass row
  scanner used by the gate;
- ``eligibility_gate``: value objects, enums, errors, and the public
  ``run_eligibility_gate`` orchestrator;
- ``eligibility_checks``: the 45 Phase 4ba §10 eligibility-time check
  functions plus the orchestrator entry point ``run_all_checks``;
- ``eligibility_report``: ``AggTradesGateReport`` data model + atomic
  JSON write under ``data/microstructure/gate-reports/``.

The eligibility-gate primitive is offline-only: no Binance endpoint, no
WebSocket, no credential, no ``.env`` / ``.mcp.json``. It never mutates
the original manifest, raw zip, sidecar, or acquisition log, and it
never flips ``research_eligible`` to ``True`` for raw aggTrades
families.

Phase 4bd adds the offline aggTrades normalizer:

- ``normalize_io``: read-only source-artefact loaders, output-path
  discipline under ``data/microstructure/normalized/``, atomic Parquet
  + JSON write helpers, SHA256 helpers;
- ``normalize_aggtrades``: ``NormalizedAggTradeRow`` dataclass,
  ``NormalizeAggTradesInput`` / ``NormalizeAggTradesResult``, the
  ``run_normalize_aggtrades`` orchestrator, and the canonical
  ``NORMALIZED_SCHEMA_V001`` 19-column constant;
- ``normalize_manifest``: ``NormalizationManifestDraft`` and the
  ``REQUIRED_GOVERNANCE_LABEL_KEYS`` for the derived family;
- ``normalize_validation``: 27 Phase 4bc validation checks
  (``4bc.24.1`` .. ``4bc.24.27``), ``NormalizationCheckStatus``,
  ``NormalizationCheckResult``, ``NormalizationValidationContext``,
  and ``run_all_checks``.

The normalizer is offline-only: no Binance endpoint, no WebSocket, no
credential, no ``.env`` / ``.mcp.json``. It never mutates the original
manifest, raw zip, sidecar, or acquisition log, and the derived
manifest is always written with ``research_eligible=False`` and
``eligibility_gate_status=pending`` (Stage-0 derived artefacts only).
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
from .eligibility_gate import (
    AggTradesEligibilityCheckResult,
    AggTradesEligibilityCheckStatus,
    AggTradesEligibilityGateInput,
    AggTradesEligibilityGateResult,
    AggTradesGateInputError,
    AggTradesGateUnsupportedError,
    InvalidWindowCandidate,
    run_eligibility_gate,
)
from .eligibility_io import GateIOError
from .eligibility_report import AggTradesGateReport
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
from .normalize_aggtrades import (
    NORMALIZATION_SCHEMA_VERSION,
    NORMALIZED_SCHEMA_V001,
    NormalizationLineage,
    NormalizationValidationError,
    NormalizeAggTradesInput,
    NormalizeAggTradesResult,
    NormalizedAggTradeRow,
    run_normalize_aggtrades,
)
from .normalize_io import NormalizationIOError
from .normalize_manifest import (
    NormalizationManifestDraft,
    NormalizationManifestError,
)
from .normalize_validation import (
    NormalizationCheckResult,
    NormalizationCheckStatus,
    NormalizationValidationResult,
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
    # eligibility_gate / eligibility_report / eligibility_io (Phase 4bb-C)
    "AggTradesEligibilityCheckResult",
    "AggTradesEligibilityCheckStatus",
    "AggTradesEligibilityGateInput",
    "AggTradesEligibilityGateResult",
    "AggTradesGateInputError",
    "AggTradesGateReport",
    "AggTradesGateUnsupportedError",
    "GateIOError",
    "InvalidWindowCandidate",
    "run_eligibility_gate",
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
    # normalize (Phase 4bd)
    "NORMALIZATION_SCHEMA_VERSION",
    "NORMALIZED_SCHEMA_V001",
    "NormalizationCheckResult",
    "NormalizationCheckStatus",
    "NormalizationIOError",
    "NormalizationLineage",
    "NormalizationManifestDraft",
    "NormalizationManifestError",
    "NormalizationValidationError",
    "NormalizationValidationResult",
    "NormalizeAggTradesInput",
    "NormalizeAggTradesResult",
    "NormalizedAggTradeRow",
    "run_normalize_aggtrades",
    # raw_writer
    "RawWriter",
    "RawWriterAlreadyExistsError",
    "RawWriterError",
    "RawWriterFileSummary",
    "RawWriterPathError",
]
