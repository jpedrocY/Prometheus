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

Phase 4bf adds the offline derived-family eligibility gate:

- ``derived_gate_io``: read-only artefact loaders + atomic gate-report
  writer + paired-SHA256 sidecar + path discipline
  (``data/microstructure/gate-reports/normalized/``);
- ``derived_gate_checks``: 55 Phase 4bf-A checks
  (``4bf.13.1`` .. ``4bf.13.55``), ``DerivedAggTradesCheckStatus``,
  ``DerivedAggTradesCheckResult``, ``DerivedGateContext``, and
  ``run_all_checks``;
- ``derived_gate_report``: ``DerivedAggTradesGateReport`` data model +
  atomic JSON write + paired SHA256 sidecar;
- ``derived_gate``: ``DerivedAggTradesGateInput`` /
  ``DerivedAggTradesGateResult`` and the public
  ``run_derived_aggtrades_gate`` orchestrator.

The derived-family gate is offline-only and read-only: it never mutates
the derived manifest, the normalized Parquet, the raw artefacts, or the
Phase 4bb-D gate report. ``research_eligible_after`` is invariant
``False`` and ``no_successor_authorization`` is invariant ``True``.
``eligibility_gate_status_after`` is recorded on the report only and
never written to the actual derived manifest.

Phase 4bh adds the offline aggTrades feature kernel:

- ``features_schema``: the 61-column ``FEATURE_SCHEMA_V001`` (16
  lineage / identity / metadata + 45 feature / quality columns), the
  45 ``FEATURE_NAMES_V001``, the 4 trailing windows
  ``FEATURE_WINDOWS_MS_V001 = (1000, 5000, 15000, 60000)``, the 26
  ``FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS``, and the deterministic
  :class:`FeatureComputationConfig` (``feature_config_hash`` derived
  from canonical-JSON over locked schema fields);
- ``features_io``: read-only loaders for the source normalized Parquet,
  source normalized manifest, and Phase 4bg-B successor-state JSON;
  atomic Parquet/JSON writers restricted to
  ``data/microstructure/features/`` and
  ``data/microstructure/manifests/``; paired-SHA256 sidecar writer;
- ``features_compute``: causal trailing-window kernel that computes
  the 61-column event-aligned feature table via vectorised cumulative
  sums plus deterministic Decimal-as-string formatting for
  rolling quantity sums / aggressive quantities / imbalances and
  rolling quantity means; ``float64`` for aggressive flow ratios and
  log returns; aggressive-side rule
  ``is_buyer_maker = false -> aggressive buy``; same-timestamp
  tie-break ``row_index <= R``;
- ``features_manifest``: ``build_feature_manifest`` produces a
  JSON-friendly manifest with ``research_eligible=False`` and
  ``eligibility_gate_status="pending"`` defaults preserved, governance
  labels (``feature_computation = "allowed_by_phase_4bh"``,
  ``labels = "forbidden"``, ``ml = "forbidden"``,
  ``strategy = "forbidden"``, ``backtest = "forbidden"``,
  ``acquisition = "unauthorized"``,
  ``stop_trigger_domain = "trade_price_backtest_candidate"``), and
  full lineage SHAs for the source normalized parquet, source
  normalized manifest, Phase 4bg-B successor-state JSON, and the
  Phase 4bf derived gate report;
- ``features_validation``: ``validate_feature_dataset`` runs schema,
  type, value, and lineage checks against the Phase 4bh-B contract
  (61-column order; row_count parity with source; no forbidden
  substrings; lineage hashes constant; ratio in ``[0, 1]``;
  Decimal-as-string columns parse via :class:`Decimal`).

The feature kernel is offline-only: no Binance endpoint, no WebSocket,
no credential, no environment file. It never mutates the source
normalized parquet, source normalized manifest, raw artefacts, Phase
4bb-D / 4bf gate reports, or Phase 4bg-B successor-state artefact, and
it never flips ``research_eligible`` to ``True`` for the feature
family. Phase 4bh produces local Stage-2 feature artefacts only; the
feature-family eligibility gate is the only path that may flip those
flags in a separately authorized future phase.

Phase 4bi-B adds the offline feature-family eligibility gate:

- ``feature_gate_io``: read-only artefact loaders + atomic gate-report
  writer + paired-SHA256 sidecar + path discipline
  (``data/microstructure/gate-reports/features/``);
- ``feature_gate_checks``: Phase 4bi-B check suite
  (``4bi-b.A01`` .. ``4bi-b.N01``), :class:`FeatureGateCheckStatus`,
  :class:`FeatureGateCheckResult`, :class:`FeatureGateContext`, and
  ``run_all_checks``;
- ``feature_gate_report``: :class:`FeatureGateReport` data model +
  atomic JSON write + paired SHA256 sidecar + invariant enforcement;
- ``feature_gate``: :class:`FeatureGateInput` /
  :class:`FeatureGateResult`, :func:`validate_feature_gate_inputs`, and
  the public :func:`run_feature_family_gate` orchestrator.

The feature-family gate is offline-only and read-only: it never mutates
the feature parquet, the feature manifest, the source normalized
parquet, the source normalized manifest, the raw artefacts, the Phase
4bb-D / 4bf gate reports, or the Phase 4bg-B successor-state artefact.
``research_eligible_after`` is invariant ``False`` and
``no_successor_authorization`` is invariant ``True``.
``eligibility_gate_status_after`` is recorded on the report only and
never written to the actual feature manifest.

Phase 4bj-C adds the offline label kernel:

- ``labels_schema``: the 39-column ``LABEL_SCHEMA_V001`` (17 lineage /
  identity / metadata + 8 label columns + 14 support columns), the
  8 ``LABEL_NAMES_V001``, the 4 horizons
  ``LABEL_HORIZONS_V001 = ("1s", "5s", "15s", "60s")`` paired with
  ``LABEL_HORIZON_MS_V001 = (1000, 5000, 15000, 60000)``, the
  ``FORBIDDEN_LABEL_COLUMN_SUBSTRINGS`` detector, and the
  deterministic ``build_label_config_hash`` helper;
- ``labels_io``: atomic Parquet / JSON writers restricted to
  ``data/microstructure/labels/`` and ``data/microstructure/manifests/``
  plus paired-SHA256 sidecar writer; refuses to overwrite;
- ``labels_compute``: ``compute_aggtrade_labels_v001`` builds the
  39-column event-aligned label table from the source feature parquet
  and the source normalized aggTrades parquet; right-edge per-horizon
  censoring; Decimal-into-ratio with float64 cast only at the
  natural-log step; strict sign threshold at ``0.0`` for
  ``forward_direction_*``; no NaN / inf in any output column;
- ``labels_manifest``: ``build_label_manifest_v001`` produces a
  JSON-friendly manifest with ``research_eligible=False`` and
  ``eligibility_gate_status="pending"`` defaults preserved, governance
  labels (``labels = "allowed_by_phase_4bj_c"``,
  ``targets = "allowed_by_phase_4bj_c"``, ``ml = "forbidden"``,
  ``strategy = "forbidden"``, ``backtest = "forbidden"``,
  ``acquisition = "unauthorized"``,
  ``paper_shadow_live = "forbidden"``,
  ``deployment = "forbidden"``,
  ``exchange_write = "forbidden"``), 13 boundary confirmations all
  ``True``, and full lineage SHAs (source feature parquet, source
  feature manifest, Phase 4bi-D successor-state JSON, Phase 4bi-B
  feature-family gate report, source normalized parquet);
- ``labels_validation``: ``validate_label_dataset_v001`` runs schema,
  type, value, lineage, support, censoring, sign, and upstream-
  immutability checks against the Phase 4bj-B contract.

The label kernel is offline-only: no Binance endpoint, no WebSocket,
no credential, no environment file. It never mutates the source
feature parquet, source feature manifest, Phase 4bi-B feature-family
gate report, Phase 4bi-D successor-state artefact, normalized parquet,
original derived manifest, raw manifest, or raw zip, and the label
manifest is always written with ``research_eligible=False`` and
``eligibility_gate_status="pending"``. Phase 4bj-C does NOT create a
label gate report or a label successor-state artefact, and does NOT
authorize Phase 4bj-D or any successor.

Phase 4bj-E adds the offline label-family eligibility gate:

- ``label_gate_io``: read-only artefact loaders + atomic gate-report
  writer + paired-SHA256 sidecar + path discipline
  (``data/microstructure/gate-reports/labels/``);
- ``label_gate_checks``: Phase 4bj-E check suite
  (``4bj-e.A01`` .. ``4bj-e.O01``), :class:`LabelGateCheckStatus`,
  :class:`LabelGateCheckResult`, :class:`LabelGateContext`, and
  ``run_all_checks``;
- ``label_gate_report``: :class:`LabelGateReport` data model +
  atomic JSON write + paired SHA256 sidecar + invariant enforcement;
- ``label_gate``: :class:`LabelGateInput` / :class:`LabelGateResult`,
  :func:`validate_label_gate_inputs`, and the public
  :func:`run_label_family_gate` orchestrator.

The label-family gate is offline-only and read-only: it never mutates
the label parquet, the label manifest, the source feature parquet, the
source feature manifest, or any sidecar. ``research_eligible_after`` is
invariant ``False`` and ``no_successor_authorization`` is invariant
``True``. ``eligibility_gate_status_after`` is recorded on the report
only and never written to the actual label manifest. The label
manifest's ``chronological_split_policy`` is preserved at
``"not_yet_defined"``. The gate report is written under
``data/microstructure/gate-reports/labels/`` with paired ``.sha256``
sidecar via atomic write-then-rename + refuse-to-overwrite discipline.
Phase 4bj-E does NOT authorize Phase 4bj-F (research / ML-use
decision) or Phase 4bj-G (successor-state recording).

Phase 4bb-F-implementation adds the canonical path policy helpers and
narrow backward-compatible threading of the policy through the raw-gate
writer / orchestrator:

- ``canonical_paths``: ``FAMILY_SUBDIRS`` (raw / normalized / features /
  labels), ``compose_canonical_gate_report_id`` (with ``phase-<id>``
  tag), ``compose_canonical_successor_state_filename``,
  ``derive_canonical_gate_report_path``,
  ``derive_canonical_successor_state_path``, canonical sidecar body
  composer + writer (``<sha>  <basename>\\n``; two spaces, trailing
  newline; refuse-overwrite; atomic write-then-rename), path validation
  helpers for gate-reports / successor-state / microstructure-root, and
  ``derive_short_commit``.
- ``eligibility_gate.AggTradesEligibilityGateInput`` gains two optional
  fields: ``family_subdir`` (default ``None``) and ``phase_id`` (default
  ``None``). When set, the raw-gate writer skips the legacy
  ``gate-reports`` subdir injection and uses canonical placement under
  ``<output_root>/<family_subdir>/``; the report identifier switches to
  ``<family>__<version>__phase-<id>__<unix_ms>__<short>``. Defaults
  preserve Phase 4bb-C behaviour verbatim so existing tests and the
  prior Phase 4bb-D recorded path are unaffected.
- ``eligibility_report.write_report_atomic`` gains a corresponding
  optional ``family_subdir`` kwarg with the same semantics.

This sub-phase is implementation-only. It does not rerun the raw or
derived gate, does not migrate any existing local gitignored artefact,
does not produce a new gate report or successor-state file, does not
mutate any manifest, does not flip ``research_eligible`` on any
family, and does not authorize Phase 4bb-G, Phase 4bj-H, label
evaluation, ML, strategy, or any successor phase.
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
from .canonical_paths import (
    FAMILY_SUBDIRS,
    GATE_REPORTS_ROOT_PARTS,
    MICROSTRUCTURE_ROOT_PARTS,
    SUCCESSOR_STATE_ROOT_PARTS,
    CanonicalPathError,
    assert_path_under_gate_reports_subdir,
    assert_path_under_successor_state,
    compose_canonical_gate_report_id,
    compose_canonical_sidecar_body,
    compose_canonical_successor_state_filename,
    derive_canonical_gate_report_path,
    derive_canonical_successor_state_path,
    derive_short_commit,
    derive_sidecar_path,
    normalize_family,
    write_paired_sha256_sidecar,
)
from .canonical_paths import (
    assert_path_under_microstructure as assert_canonical_path_under_microstructure,
)
from .canonical_paths import (
    compute_file_sha256 as compute_canonical_file_sha256,
)
from .config import (
    ConfigValidationError,
    DatasetFamilyConfig,
    EligibilityGateThresholds,
    InvalidWindowThresholds,
    MicrostructureConfig,
    validate_config,
)
from .derived_gate import (
    DerivedAggTradesGateInput,
    DerivedAggTradesGateInputError,
    DerivedAggTradesGateResult,
    DerivedAggTradesGateUnsupportedError,
    run_derived_aggtrades_gate,
)
from .derived_gate_checks import (
    DerivedAggTradesCheckResult,
    DerivedAggTradesCheckStatus,
)
from .derived_gate_report import DerivedAggTradesGateReport
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
from .feature_gate import (
    FeatureGateError,
    FeatureGateInput,
    FeatureGateResult,
    run_feature_family_gate,
    validate_feature_gate_inputs,
)
from .feature_gate_checks import (
    FeatureGateCheckResult,
    FeatureGateCheckStatus,
    FeatureGateContext,
)
from .feature_gate_io import (
    FeatureGateIOError,
    FeatureGateReportPaths,
)
from .feature_gate_report import (
    FeatureGateReport,
    FeatureGateReportError,
    build_feature_gate_report,
    write_feature_gate_report,
)
from .features_compute import (
    FeatureComputationError,
    FeatureComputationResult,
    FeatureLineage,
    compute_aggtrades_features,
    write_feature_dataset,
)
from .features_io import (
    FEATURES_FAMILY_SUBDIR,
    FeatureIOError,
    SourceArtefactSummary,
    assert_manifest_output_path_under_manifests,
    assert_output_path_under_features,
    assert_path_under_data_microstructure,
    atomic_write_feature_manifest,
    atomic_write_feature_parquet,
    derive_feature_manifest_output_path,
    derive_feature_output_path,
    hash_source_file,
    read_normalized_parquet,
    read_source_normalized_manifest,
    read_successor_state,
    resolve_default_manifests_root,
    write_feature_sha256_sidecar,
)
from .features_manifest import (
    FORBIDDEN_FEATURE_GOVERNANCE_VALUES,
    REQUIRED_BOUNDARY_CONFIRMATIONS,
    REQUIRED_FEATURE_GOVERNANCE_KEYS,
    FeatureManifestError,
    build_feature_manifest,
)
from .features_schema import (
    DECIMAL_POLICY_V001,
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_V001,
    FEATURE_SCHEMA_VERSION,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS,
    INVALID_WINDOW_POLICY_V001,
    LINEAGE_COLUMNS_V001,
    NULL_POLICY_V001,
    PER_WINDOW_FEATURE_TEMPLATES,
    SOURCE_NORMALIZED_DATASET_FAMILY,
    SOURCE_NORMALIZED_DATASET_VERSION,
    FeatureComputationConfig,
    FeatureSchemaError,
    assert_no_forbidden_substrings,
    build_feature_config,
    compute_feature_config_hash,
)
from .features_validation import (
    FeatureCheckResult,
    FeatureCheckStatus,
    FeatureValidationError,
    FeatureValidationResult,
    validate_feature_dataset,
)
from .invalid_window import (
    DownstreamEligibilityAction,
    InvalidWindow,
    InvalidWindowReason,
    InvalidWindowSeverity,
)
from .label_gate import (
    LabelGateError,
    LabelGateInput,
    LabelGateResult,
    run_label_family_gate,
    validate_label_gate_inputs,
)
from .label_gate_checks import (
    LabelGateCheckResult,
    LabelGateCheckStatus,
    LabelGateContext,
)
from .label_gate_io import (
    LabelGateIOError,
    LabelGateReportPaths,
)
from .label_gate_report import (
    LabelGateReport,
    LabelGateReportError,
    build_label_gate_report,
    write_label_gate_report,
)
from .labels_compute import (
    LabelComputationError,
    LabelComputationSummary,
    LabelLineage,
    compute_aggtrade_labels_v001,
    write_label_dataset_v001,
)
from .labels_io import (
    LABELS_FAMILY_SUBDIR,
    LabelIOError,
    assert_label_manifest_path_under_manifests,
    assert_label_path_under_data_microstructure,
    assert_output_path_under_labels,
    atomic_write_label_manifest,
    atomic_write_label_parquet,
    derive_label_manifest_output_path,
    derive_label_output_path,
    write_label_sha256_sidecar,
)
from .labels_manifest import (
    FORBIDDEN_LABEL_GOVERNANCE_VALUES,
    REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS,
    REQUIRED_LABEL_GOVERNANCE_KEYS,
    LabelManifestError,
    build_label_manifest_v001,
)
from .labels_schema import (
    ANCHOR_POLICY_V001,
    DIRECTION_THRESHOLD_POLICY_V001,
    DTYPE_POLICY_V001,
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS,
    FUTURE_REFERENCE_POLICY_V001,
    LABEL_DATASET_FAMILY_V001,
    LABEL_DATASET_VERSION_V001,
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_LINEAGE_COLUMNS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_COLUMNS_V001,
    LABEL_SCHEMA_V001,
    LABEL_SCHEMA_VERSION_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
    NULL_CENSORING_POLICY_V001,
    LabelSchemaError,
    assert_no_forbidden_label_substrings,
    build_label_config_hash,
)
from .labels_validation import (
    LabelCheckResult,
    LabelCheckStatus,
    LabelValidationError,
    LabelValidationResult,
    validate_label_dataset_v001,
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
    # canonical_paths (Phase 4bb-F-implementation)
    "CanonicalPathError",
    "FAMILY_SUBDIRS",
    "GATE_REPORTS_ROOT_PARTS",
    "MICROSTRUCTURE_ROOT_PARTS",
    "SUCCESSOR_STATE_ROOT_PARTS",
    "assert_canonical_path_under_microstructure",
    "assert_path_under_gate_reports_subdir",
    "assert_path_under_successor_state",
    "compose_canonical_gate_report_id",
    "compose_canonical_sidecar_body",
    "compose_canonical_successor_state_filename",
    "compute_canonical_file_sha256",
    "derive_canonical_gate_report_path",
    "derive_canonical_successor_state_path",
    "derive_short_commit",
    "derive_sidecar_path",
    "normalize_family",
    "write_paired_sha256_sidecar",
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
    # derived_gate (Phase 4bf)
    "DerivedAggTradesCheckResult",
    "DerivedAggTradesCheckStatus",
    "DerivedAggTradesGateInput",
    "DerivedAggTradesGateInputError",
    "DerivedAggTradesGateReport",
    "DerivedAggTradesGateResult",
    "DerivedAggTradesGateUnsupportedError",
    "run_derived_aggtrades_gate",
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
    # features (Phase 4bh)
    "DECIMAL_POLICY_V001",
    "FEATURES_FAMILY_SUBDIR",
    "FEATURE_DATASET_FAMILY",
    "FEATURE_DATASET_VERSION",
    "FEATURE_NAMES_V001",
    "FEATURE_SCHEMA_V001",
    "FEATURE_SCHEMA_VERSION",
    "FEATURE_WINDOW_LABELS_V001",
    "FEATURE_WINDOWS_MS_V001",
    "FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS",
    "FORBIDDEN_FEATURE_GOVERNANCE_VALUES",
    "FeatureCheckResult",
    "FeatureCheckStatus",
    "FeatureComputationConfig",
    "FeatureComputationError",
    "FeatureComputationResult",
    "FeatureIOError",
    "FeatureLineage",
    "FeatureManifestError",
    "FeatureSchemaError",
    "FeatureValidationError",
    "FeatureValidationResult",
    "INVALID_WINDOW_POLICY_V001",
    "LINEAGE_COLUMNS_V001",
    "NULL_POLICY_V001",
    "PER_WINDOW_FEATURE_TEMPLATES",
    "REQUIRED_BOUNDARY_CONFIRMATIONS",
    "REQUIRED_FEATURE_GOVERNANCE_KEYS",
    "SOURCE_NORMALIZED_DATASET_FAMILY",
    "SOURCE_NORMALIZED_DATASET_VERSION",
    "SourceArtefactSummary",
    "assert_manifest_output_path_under_manifests",
    "assert_no_forbidden_substrings",
    "assert_output_path_under_features",
    "assert_path_under_data_microstructure",
    "atomic_write_feature_manifest",
    "atomic_write_feature_parquet",
    "build_feature_config",
    "build_feature_manifest",
    "compute_aggtrades_features",
    "compute_feature_config_hash",
    "derive_feature_manifest_output_path",
    "derive_feature_output_path",
    "hash_source_file",
    "read_normalized_parquet",
    "read_source_normalized_manifest",
    "read_successor_state",
    "resolve_default_manifests_root",
    "validate_feature_dataset",
    "write_feature_dataset",
    "write_feature_sha256_sidecar",
    # feature_gate (Phase 4bi-B)
    "FeatureGateCheckResult",
    "FeatureGateCheckStatus",
    "FeatureGateContext",
    "FeatureGateError",
    "FeatureGateIOError",
    "FeatureGateInput",
    "FeatureGateReport",
    "FeatureGateReportError",
    "FeatureGateReportPaths",
    "FeatureGateResult",
    "build_feature_gate_report",
    "run_feature_family_gate",
    "validate_feature_gate_inputs",
    "write_feature_gate_report",
    # labels (Phase 4bj-C)
    "ANCHOR_POLICY_V001",
    "DIRECTION_THRESHOLD_POLICY_V001",
    "DTYPE_POLICY_V001",
    "FORBIDDEN_LABEL_COLUMN_SUBSTRINGS",
    "FORBIDDEN_LABEL_GOVERNANCE_VALUES",
    "FUTURE_REFERENCE_POLICY_V001",
    "LABELS_FAMILY_SUBDIR",
    "LABEL_DATASET_FAMILY_V001",
    "LABEL_DATASET_VERSION_V001",
    "LABEL_HORIZONS_V001",
    "LABEL_HORIZON_MS_V001",
    "LABEL_LINEAGE_COLUMNS_V001",
    "LABEL_NAMES_V001",
    "LABEL_SCHEMA_COLUMNS_V001",
    "LABEL_SCHEMA_V001",
    "LABEL_SCHEMA_VERSION_V001",
    "LABEL_SUPPORT_COLUMN_NAMES_V001",
    "LabelCheckResult",
    "LabelCheckStatus",
    "LabelComputationError",
    "LabelComputationSummary",
    "LabelIOError",
    "LabelLineage",
    "LabelManifestError",
    "LabelSchemaError",
    "LabelValidationError",
    "LabelValidationResult",
    "NULL_CENSORING_POLICY_V001",
    "REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS",
    "REQUIRED_LABEL_GOVERNANCE_KEYS",
    "assert_label_manifest_path_under_manifests",
    "assert_label_path_under_data_microstructure",
    "assert_no_forbidden_label_substrings",
    "assert_output_path_under_labels",
    "atomic_write_label_manifest",
    "atomic_write_label_parquet",
    "build_label_config_hash",
    "build_label_manifest_v001",
    "compute_aggtrade_labels_v001",
    "derive_label_manifest_output_path",
    "derive_label_output_path",
    "validate_label_dataset_v001",
    "write_label_dataset_v001",
    "write_label_sha256_sidecar",
    # label_gate (Phase 4bj-E)
    "LabelGateCheckResult",
    "LabelGateCheckStatus",
    "LabelGateContext",
    "LabelGateError",
    "LabelGateIOError",
    "LabelGateInput",
    "LabelGateReport",
    "LabelGateReportError",
    "LabelGateReportPaths",
    "LabelGateResult",
    "build_label_gate_report",
    "run_label_family_gate",
    "validate_label_gate_inputs",
    "write_label_gate_report",
]
