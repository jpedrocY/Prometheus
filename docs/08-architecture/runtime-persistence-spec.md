# Runtime Persistence Specification

## Purpose

This document defines the runtime persistence specification for the v1 Prometheus trading system.

Its purpose is to make live runtime persistence explicit enough that:

- restart behavior is safe,
- reconciliation behavior is deterministic,
- operator continuity is preserved,
- important control-state changes are not lost,
- and the implementation does not improvise unsafe storage behavior.

This document exists because v1 depends on:

- safe-mode-first restart,
- exchange-authoritative reconciliation,
- persistent runtime control state,
- explicit protection-state tracking,
- and operator-supervised recovery.

Those requirements cannot be satisfied robustly if runtime persistence remains informal.

This document defines what runtime state must be persisted, what may remain derived, when writes must happen, and what correctness properties the persistence layer must support.

## Scope

This specification applies to live runtime persistence for the v1 system assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only in first live-capable scope
- one-way mode
- isolated margin
- one active strategy
- one open position maximum
- one active protective stop maximum
- supervised deployment
- restart begins in safe mode
- exchange state is authoritative for position/order/protection truth

This document covers:

- runtime persistence goals
- persistence categories
- required persisted entities and fields
- persisted versus derived state boundaries
- write timing rules
- durable-write requirements
- crash-safety principles
- restore/read behavior on startup
- retention and mutation rules
- and implementation constraints for v1

This document does **not** define:

- historical research dataset persistence
- Parquet / DuckDB research storage
- frontend/browser storage
- cloud/object-store architecture
- or full database product selection beyond v1 guidance

## Background

The project already defines:

- a modular-monolith runtime architecture
- a hierarchical state model
- explicit internal event contracts
- restart and reconciliation workflows
- incident and safe-mode behavior
- and operator-visible control states

Those documents together imply that runtime persistence must preserve the minimum operational facts required to answer, after a restart:

- what mode the bot was in,
- whether entries were blocked,
- whether a trade lifecycle was active,
- whether a position was believed to exist,
- whether protection was believed to exist,
- what order identifiers were known,
- whether reconciliation had already failed,
- and whether operator review or kill-switch state was active.

Without a clear persistence spec, the implementation risks:

- losing critical control-state changes on crash,
- resuming from stale assumptions,
- corrupting recovery behavior,
- and making incident reconstruction ambiguous.

## Persistence Philosophy

## 1. Persist restart-critical facts, not convenience state

Runtime persistence should store the smallest set of facts needed for:

- safe restart,
- reconciliation,
- control continuity,
- incident continuity,
- and operator continuity.

It should not become a dumping ground for every computed field or UI convenience summary.

## 2. Exchange truth outranks persisted local assumptions

Persisted local state exists to support restart and recovery.

It is not the final authority over:

- whether a position exists,
- whether protection exists,
- or whether an order is still open.

Those truths must still be re-established against exchange state during startup or confidence loss.

## 3. Persistence is part of the safety system

Runtime persistence is not just an implementation detail.

If important state can be lost between a critical transition and a crash, the bot may restart unsafely or require overly broad emergency handling.

## 4. Writes should follow explicit event boundaries

Important persistent state changes should happen in response to explicit message/event boundaries, not hidden side effects scattered across modules.

This aligns runtime persistence with:

- the state model
- the internal event contracts
- and the observability design

## Persistence Categories

The runtime should distinguish three categories of persisted information.

## 1. Core Runtime Control State

This category preserves top-level operating posture.

Examples:

- primary runtime mode
- pause state
- kill-switch state
- operator-review-required flag
- entries-blocked flag
- active strategy identifier
- last known restart context

## 2. Active Trade / Protection Continuity State

This category preserves the bot’s last known local view of the active trade workflow.

Examples:

- trade lifecycle state
- protection state
- current strategy stage
- current risk stage
- current trailing stage if active
- current signal reference
- order identifiers
- stop identifiers
- position reference fields

## 3. Recovery / Incident Continuity State

This category preserves enough information to continue recovery safely after interruption.

Examples:

- reconciliation state
- last successful reconciliation timestamp
- current mismatch classification if any
- active incident identifiers
- incident severity summary if needed for control continuity
- emergency-branch flag
- latest exception flags

## Required Persisted Entities

The v1 runtime should persist a small number of clear entities rather than an unstructured blob with unclear ownership.

## Entity 1 — Runtime Control Record

### Purpose
Represents current top-level runtime posture.

### Minimum required fields

- `runtime_mode`
- `incident_active`
- `kill_switch_active`
- `paused_by_operator`
- `operator_review_required`
- `entries_blocked`
- `active_strategy_id`
- `config_version`
- `updated_at_utc_ms`

### Notes
This record is central to startup continuity and operator continuity.

## Entity 2 — Active Trade Record

### Purpose
Represents the local runtime’s current or most recent active trade workflow.

### Minimum required fields

- `trade_reference`
- `symbol`
- `trade_lifecycle_state`
- `strategy_stage`
- `risk_stage`
- `trailing_stage` where applicable
- `expected_entry_side`
- `signal_reference`
- `signal_confirmed_at_utc_ms`
- `entry_fill_confirmed_at_utc_ms` if known
- `average_fill_price` if known
- `position_side` if known
- `position_size` if known
- `updated_at_utc_ms`

### Notes
This record is local continuity state, not exchange truth.

## Entity 3 — Protection Record

### Purpose
Represents the local runtime’s current or most recent protection posture for the active trade.

### Minimum required fields

- `trade_reference`
- `symbol`
- `protection_state`
- `protective_stop_client_order_id` if known
- `protective_stop_exchange_order_id` if known
- `stop_trigger_price` if known
- `stop_stage`
- `last_protection_confirmation_at_utc_ms` if known
- `updated_at_utc_ms`

### Notes
This record is especially important because a position without confirmed protection is an emergency condition in v1.

## Entity 4 — Reconciliation Record

### Purpose
Represents the current recovery/reconciliation posture.

### Minimum required fields

- `reconciliation_state`
- `reconciliation_reason`
- `last_successful_reconciliation_at_utc_ms`
- `reconciliation_started_at_utc_ms` if active
- `mismatch_class` if relevant
- `repair_required`
- `repair_in_progress`
- `updated_at_utc_ms`

### Notes
This record supports both startup recovery and mid-run confidence-loss recovery.

## Entity 5 — Incident Continuity Record

### Purpose
Preserves the minimum blocking and emergency context needed across restart.

### Minimum required fields

- `active_incident_id` if one blocking incident is primary
- `highest_active_severity`
- `emergency_branch_active`
- `blocking_reason`
- `updated_at_utc_ms`

### Notes
This does not need to replace full incident history. It only preserves continuity for the current operational condition.

## Entity 6 — Operator Action Record Store

### Purpose
Provides durable continuity for major manual actions.

### Minimum required fields per record

- `action_id`
- `action_type`
- `operator_identity_or_alias` where available
- `reason`
- `resulting_runtime_mode` if applicable
- `occurred_at_utc_ms`

### Notes
This supports both recovery interpretation and later review.

## Persisted vs Derived Boundaries

The runtime should distinguish clearly between what must be persisted and what may remain derived.

## Persisted State

The following should be persisted because losing them would make restart or recovery materially less safe:

- runtime mode
- pause / kill-switch / operator-review-required state
- entries-blocked state
- trade lifecycle state
- protection state
- reconciliation state
- active trade identifiers and order identifiers
- stop identifiers
- emergency-branch flag
- major operator actions
- last successful reconciliation timestamp
- major blocking reasons

## Derived State

The following may generally remain derived or recomputable:

- operator summary banners
- UI convenience labels
- non-authoritative health rollups
- recent event summaries if the underlying event log exists separately
- purely cosmetic status text
- values that can be safely recomputed from persisted facts plus fresh exchange state

## Boundary principle

If loss of a field would change restart safety, reconciliation correctness, or control continuity, it should be persisted.

If a field is only a convenience rendering or can be safely recomputed after fresh exchange reads, it should remain derived.

## Recommended Storage Model for V1

The v1 runtime should favor a simple, durable local persistence model appropriate for a modular monolith.

## Recommended characteristics

The runtime persistence mechanism should be:

- local
- durable
- easy to inspect
- easy to back up
- simple to reason about
- and supportive of atomic updates for small critical records

## Recommended direction

For v1, an embedded local durable store is appropriate.

Examples could include:

- SQLite
- or another small embedded transactional store

### Why this direction is preferred

It fits:

- one runtime
- one symbol
- one position
- one host
- and the need for crash-safe, inspectable persistence without distributed complexity

## Important note

This document does not require a specific product choice beyond the durability and correctness properties described here.

## Write Timing Rules

Persistence must follow explicit state/event boundaries.

## Events that should normally trigger durable writes before continuation

The following transitions should trigger durable state updates before the runtime proceeds past them.

## Runtime/control transitions

- runtime mode changed
- pause enabled
- pause cleared
- kill switch enabled
- kill switch cleared
- operator review required set/cleared
- entries blocked state changed

## Trade continuity transitions

- signal confirmed
- trade lifecycle changed
- entry fill confirmed
- position confirmed at local continuity level
- exit confirmed at local continuity level
- trade closed

## Protection transitions

- protection state changed
- stop submitted reference recorded
- stop confirmed reference recorded
- stop replacement started
- protection uncertainty entered
- emergency unprotected state entered

## Reconciliation/recovery transitions

- reconciliation required
- reconciliation started
- reconciliation classified clean
- reconciliation classified recoverable mismatch
- reconciliation classified unsafe mismatch
- repair action started/completed
- restart context initialized

## Incident/control transitions

- blocking incident opened
- incident severity escalated into blocking/emergency class
- emergency branch entered
- major operator action recorded

## Write-before-continue principle

If a crash immediately after a state transition would leave restart behavior materially less safe unless the transition were durable, the runtime should persist that transition before proceeding.

## Atomicity and Consistency Requirements

The persistence layer should support small atomic updates for related critical facts.

## Minimum requirement

A critical persistence update should not leave the runtime in a half-written state where:

- runtime mode changed but blocking flags did not
- trade lifecycle advanced but protection state did not
- reconciliation started but reason/mismatch context was not stored
- emergency branch entered but incident continuity was not persisted

## Preferred rule

Related fields that define one logical transition should be persisted atomically where practical.

### Examples

#### Example 1 — Safe mode entry due to emergency
Persist together:
- runtime mode = `SAFE_MODE`
- entries_blocked = true
- incident_active = true
- operator_review_required = true
- emergency_branch_active = true
- blocking_reason

#### Example 2 — Protection uncertainty transition
Persist together:
- protection_state = `PROTECTION_UNCERTAIN`
- trade lifecycle may move to exception-related state
- entries_blocked = true if required by policy
- updated timestamps and related stop reference

## Startup Restore Behavior

On startup, the runtime should load persisted operational state before attempting normal operation.

## Required restore sequence

At minimum:

1. load runtime control record
2. load active trade record if present
3. load protection record if present
4. load reconciliation record
5. load incident continuity record
6. load recent operator action continuity if relevant
7. mark loaded state as provisional until exchange reconciliation completes

## Important rule

Loaded local state must be treated as:

- necessary
- but provisional

It is used to guide recovery, not to replace exchange truth.

## Startup read principle

Persistence restore is successful only if the runtime can determine:

- what control state it was in
- whether a trade workflow was active
- whether protection was believed to exist
- whether reconciliation was already required or failed
- whether operator review or kill-switch state was active

## Mutation and Retention Rules

## Current-state records

The runtime may maintain current-state records for:

- runtime control
- active trade
- protection
- reconciliation
- incident continuity

These may be updated in place if:

- history is captured elsewhere through event logging
- and the update preserves crash-safe current-state continuity

## Historical continuity

Meaningful operator actions and important incident/recovery changes should also remain recoverable historically through durable event records or append-only history tables/logs.

## Important principle

Current-state persistence is not a replacement for operational event history.

The runtime needs both:

- current continuity records
- and historical event records

## Cleanup rules

Closed trade continuity records may eventually be archived or rotated, but only after:

- the trade is fully closed
- exchange state is confirmed flat
- no blocking reconciliation remains
- and the retention policy for review/diagnostics is respected

## Forbidden Persistence Patterns

The following patterns are explicitly forbidden.

## 1. Persisting secrets with runtime operational records

Runtime persistence must not store:

- raw API secrets
- secret-bearing config dumps
- signatures
- raw credential payloads

## 2. Persisting exchange truth as if it were final local authority

The runtime may store its last known local view of position/order/protection status, but must not treat persisted local fields as authoritative substitutes for fresh exchange reconciliation.

## 3. Relying on memory-only state for critical safety controls

The following must not remain memory-only:

- kill-switch state
- pause state
- operator-review-required state
- protection state
- reconciliation state
- emergency-branch state

## 4. Writing critical multi-field transitions non-deterministically

The runtime must not scatter one logical safety transition across uncontrolled writes such that a crash produces ambiguous continuity.

## 5. Persisting excessive convenience state

The runtime should not bloat operational persistence with large UI-only or diagnostic-only fields that add drift risk without helping recovery.

## Validation and Correctness Expectations

The persistence design should support validation of the following behaviors.

## 1. Crash after mode change
If the process crashes immediately after entering safe mode, restart should still know it was in a blocked/safe posture.

## 2. Crash after fill confirmation but before stop confirmation
Restart should know that a live trade workflow was active and that protection may still need verification urgently.

## 3. Crash during stop replacement
Restart should know that protection continuity was mid-transition and may be uncertain.

## 4. Crash during reconciliation
Restart should know reconciliation was required or already in progress and should not assume healthy mode by default.

## 5. Crash after operator kill-switch action
Restart should preserve the kill-switch condition until explicitly cleared.

## Decisions

The following decisions are accepted for the v1 runtime persistence specification:

- runtime persistence is a safety-critical part of the live system
- restart-critical facts must be persisted explicitly
- exchange truth remains authoritative over persisted local assumptions
- runtime persistence should be organized around a small number of clear continuity records
- related critical state transitions should be persisted atomically where practical
- important control, protection, reconciliation, and operator-action transitions should trigger durable writes
- startup must load persisted state before recovery logic proceeds
- loaded local state is provisional until exchange reconciliation confirms or corrects it
- the v1 system should prefer a simple embedded durable local store rather than distributed persistence complexity
- secrets must never be persisted in runtime operational records

## Open Questions

The following remain open for implementation detail:

1. What exact embedded storage technology should be selected for v1?
2. Which critical transitions require strict write-before-continue behavior versus tolerated eventual write within the same process step?
3. Should current-state records live in separate tables/documents or in one strongly structured state store with typed sections?
4. What exact retention period should apply to closed trade continuity records versus append-only event history?
5. Which historical records should be queryable directly by the operator interface versus derived from observability logs?

## Next Steps

After this document, the next recommended files are:

1. `docs/08-architecture/codebase-structure.md`
2. `docs/00-meta/ai-coding-handoff.md`
3. `docs/09-operations/first-run-setup-checklist.md`
