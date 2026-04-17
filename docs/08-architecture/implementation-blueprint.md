# Implementation Blueprint

## Purpose

This document defines the high-level implementation architecture for the v1 Prometheus trading system.

Its purpose is to translate the current strategy, data, validation, execution, operations, and security decisions into an implementation-ready system shape.

This document is intended to answer:

- what the major system components are,
- what each component owns,
- how components interact,
- what must be persisted,
- what the exchange is authoritative for,
- how research and live runtime remain separated,
- and in what order the first implementation should be built.

This document is an architecture-level bridge document.

It does **not** define:

- the full runtime state machine,
- the full observability schema,
- the exact dashboard layout,
- or detailed code-level interfaces.

Those belong in follow-on documents.

## Scope

This blueprint applies to the v1 system assumptions:

- Binance USDⓈ-M futures
- BTCUSDT perpetual first
- ETHUSDT as first secondary research comparison
- breakout continuation with higher-timeframe trend filter
- 15m signal timeframe
- 1h higher-timeframe bias
- one-way mode
- isolated margin
- one symbol first
- one position first
- supervised deployment
- exchange-side protective stop
- safe-mode-first restart and incident handling

This document covers:

- architectural principles,
- component boundaries,
- research versus live-runtime separation,
- persistence categories,
- exchange-authority rules,
- runtime flow structure,
- and the recommended v1 implementation sequence.

This document does **not** define:

- multi-symbol orchestration,
- portfolio-level routing,
- distributed deployment architecture,
- hedge-mode support,
- machine-learning overlays,
- or full production infrastructure design.

## Background

The project has already made several major decisions that constrain the implementation shape.

At the strategy level, v1 is a rules-based breakout continuation system with 15m signal logic, 1h higher-timeframe bias, bar-close confirmation, and market entry after confirmed signal close.

At the research level, historical work uses official Binance USDⓈ-M futures data, Parquet storage, DuckDB querying, UTC Unix milliseconds, completed-bar-only logic, and explicit dataset versioning.

At the live-trading level, v1 uses one-way mode, isolated margin, exchange-side protective stops, user-stream events as the primary live state source, REST for placement/recovery/reconciliation, and supervised operator involvement.

At the operational level, the bot must:

- start in safe mode on restart,
- reconcile before resuming,
- treat exchange state as authoritative,
- classify incidents by severity,
- and fail closed on important execution or credential uncertainty.

Those decisions imply a system that must be:

- narrow,
- explicit,
- restart-safe,
- operationally observable,
- and resistant to accidental coupling between strategy logic and exchange mechanics.

## Architectural Principles

## 1. Modular monolith for v1

The v1 system should be implemented as a **modular monolith**, not as a distributed multi-service platform.

### Meaning

The system should be:

- one primary deployable runtime,
- with clear internal modules,
- explicit interfaces between those modules,
- and durable local persistence where required.

### Why this is selected

This fits the current project scope:

- one symbol,
- one position,
- supervised rollout,
- high recovery importance,
- and strong desire to minimize operational complexity.

A distributed system would add coordination, deployment, observability, and failure-surface complexity before the project has earned that complexity.

## 2. Strategy and execution remain separate

The strategy layer decides:

- what the market condition means,
- whether a signal exists,
- what the intended entry/exit decision is,
- and what stop logic the trade should follow.

The execution layer decides:

- how to express that decision safely on Binance,
- how to comply with exchange constraints,
- how to place/cancel/replace orders,
- and how to confirm exchange state.

This separation is mandatory.

## 3. Exchange state is authoritative

The exchange is the source of truth for:

- current position state,
- current open-order state,
- and current protective-stop state.

Local state is required for:

- orchestration,
- persistence,
- restart recovery,
- reconciliation,
- and operator visibility.

But local intent is not truth.

## 4. Safe continuation requires state certainty

If the bot cannot trust:

- position state,
- stop-protection state,
- execution outcome,
- or required stream freshness,

then normal strategy operation must stop.

The architecture must therefore support:

- safe mode,
- blocking states,
- reconciliation,
- and explicit operator escalation paths.

## 5. Research and live runtime are separate concerns

The historical research environment and the live trading runtime should remain conceptually and operationally distinct.

They may share strategy concepts and some reusable calculation logic, but they should not collapse into one blurred system.

### Why this matters

Research requires:

- reproducibility,
- versioned datasets,
- backtests,
- validation views,
- and controlled assumptions.

Live runtime requires:

- stream intake,
- exchange truth,
- order placement,
- protection,
- recovery,
- and incident handling.

The architecture should respect that difference.

## 6. Narrowness is a feature in v1

The v1 implementation should intentionally preserve these restrictions:

- BTCUSDT only
- one active strategy only
- one active position maximum
- one active protective stop maximum
- no hedge mode
- no portfolio logic
- no multi-venue routing
- no autonomous strategy switching

These restrictions reduce ambiguity and simplify safe behavior.

## Top-Level Component Model

The v1 architecture should be divided into the following major components.

## 1. Research Data Layer

### Responsibility

This layer owns historical research data and reproducible research inputs.

### Owns

- raw historical payload storage
- normalized datasets
- derived datasets
- dataset version linkage
- reusable validation views
- backtest-ready research inputs

### Does not own

- live stream handling
- runtime execution state
- order placement
- or restart/recovery logic

## 2. Strategy Engine

### Responsibility

This layer evaluates market structure and decides what the strategy intends to do.

### Owns

- higher-timeframe bias logic
- setup / consolidation logic
- breakout trigger logic
- strategy-side exit logic
- trade-stage logic at the strategy level
- no-trade filter evaluation
- completed-bar-only decision timing

### Inputs

- completed market bars
- configuration
- symbol metadata where relevant
- runtime guards such as “entries blocked”

### Outputs

- strategy decisions such as:
  - no action
  - candidate entry signal
  - stop update intent
  - market exit intent
  - trade-management stage transitions

### Does not own

- exchange order formatting
- exchange acknowledgements
- fill confirmation
- or reconciliation logic

## 3. Risk and Sizing Layer

### Responsibility

This layer converts strategy intent into risk-constrained trade parameters.

### Owns

- stop-distance-based sizing
- leverage-cap checks
- internal notional caps
- stage-specific risk limits
- symbol-rule awareness needed for tradability checks
- daily lockout / drawdown pause gating where those controls apply

### Inputs

- strategy decision
- account equity or usable risk reference
- stop distance
- symbol constraints
- leverage constraints
- runtime lockout state

### Outputs

- approved or rejected trade sizing decision
- executable quantity / notional guidance
- risk-related rejection reasons

### Does not own

- entry timing logic
- order submission
- or exchange confirmation

## 4. Execution Layer

### Responsibility

This layer safely expresses approved strategy/risk decisions on Binance.

### Owns

- market entry submission
- protective stop submission
- cancel-and-replace stop updates
- symbol rule compliance at order expression time
- deterministic client order ID generation
- submission acknowledgment handling
- exchange request discipline

### Inputs

- approved strategy/risk actions
- exchange metadata
- current runtime state
- safety gates
- credentials and exchange connectivity

### Outputs

- order submission attempts
- order role metadata
- execution event records
- exception signals when exchange outcome is uncertain

### Does not own

- signal generation
- operator approval logic
- long-term research data storage
- or final authority over position truth

## 5. Market-Data Ingestion Layer

### Responsibility

This layer ingests and normalizes live market data required by the strategy.

### Owns

- market-data stream intake
- bar-construction / bar-completion handling if needed in runtime
- freshness checks
- completed-bar publication to the strategy engine
- stale-data detection

### Must enforce

- completed-bar-only downstream strategy evaluation
- explicit freshness state
- blocking of new entries if market-data confidence is insufficient

## 6. User-Stream and Account Event Layer

### Responsibility

This layer ingests private exchange events and routes them into runtime state handling.

### Owns

- user-stream lifecycle management
- keepalive maintenance
- reconnect handling
- ingestion of order/account/algo updates
- event normalization
- routing to reconciliation/state handlers

### Importance

This layer is the primary live source of truth for normal operation and therefore should be treated as safety-critical.

## 7. State and Reconciliation Layer

### Responsibility

This layer maintains durable local runtime state and compares it with exchange truth when needed.

### Owns

- persisted runtime state
- order/position/stop references
- reconciliation workflows
- mismatch classification
- repair-or-escalate decisions
- restart recovery support

### Inputs

- local persisted state
- exchange position state
- open normal orders
- open algo orders
- user-stream updates
- execution outcomes

### Outputs

- updated local state
- reconciliation status
- clean / recoverable / unsafe classification
- blocking or escalation signals

## 8. Safety and Incident Control Layer

### Responsibility

This layer enforces system-level safety conditions.

### Owns

- safe mode
- kill-switch state
- pause / block states
- incident classification hooks
- severity routing
- recovery-required gating
- emergency branching when protection is uncertain

### Role

This layer should not be treated as optional glue.

It is part of the core runtime architecture because the bot must stop normal operation under meaningful uncertainty.

## 9. Operator Interface / Control Layer

### Responsibility

This layer exposes operator-visible state and manual controls consistent with supervised v1 operation.

### Owns

- top-level system state display
- health summaries
- position / stop visibility
- incident visibility
- pause / restart / kill-switch actions
- operator approval capture where required

### v1 scope

This can remain narrow in the first version, but the architecture must reserve a clean boundary for it.

## 10. Configuration and Secret Loading Layer

### Responsibility

This layer loads controlled runtime configuration and secrets and validates them at startup.

### Owns

- environment selection
- runtime configuration loading
- secret-loading integration
- credential presence / validity checks
- fail-closed startup behavior

### Important rule

This layer must not leak secrets into logs, docs, or routine status output.

## Responsibilities and Boundary Summary

## Strategy Engine vs Execution Layer

### Strategy Engine
- determines whether a trade should exist
- computes conceptual entry, stop, and management intent

### Execution Layer
- turns approved intent into exchange-safe actions
- handles exchange-specific behavior and acknowledgment paths

## Execution Layer vs State/Reconciliation Layer

### Execution Layer
- submits and attempts actions

### State/Reconciliation Layer
- decides whether actions are actually reflected in exchange truth
- maintains durable local representation
- handles mismatch and recovery logic

## Market Data vs User Stream

### Market Data
- drives signal evaluation and bar-completion logic

### User Stream
- drives order/account/protective-stop truth during normal live operation

These must not be blurred into one generic “stream” abstraction without preserving their different roles.

## Safety Layer vs Operator Interface

### Safety Layer
- enforces internal blocking and protection logic automatically

### Operator Interface
- exposes state and provides explicit manual controls and approvals

## Research World vs Live Runtime World

The project should explicitly maintain two distinct system domains.

## Research World

This includes:

- historical data ingestion for research
- normalization
- derived datasets
- dataset versioning
- backtests
- walk-forward validation
- holdout evaluation
- comparison reports

### Main characteristics
- file-based
- reproducible
- versioned
- point-in-time controlled
- not exchange-live

## Live Runtime World

This includes:

- live stream handling
- order placement
- user-stream events
- reconciliation
- restart recovery
- incident handling
- operator supervision
- runtime persistence

### Main characteristics
- exchange-connected
- stateful
- safety-critical
- recovery-sensitive
- operator-visible

## Shared Logic Principle

Where practical, reusable calculation logic may be shared across research and live runtime.

Examples may include:

- indicator calculations
- setup-window calculations
- ATR calculations
- trend-bias calculations
- strategy-rule evaluation logic

However, shared logic must not erase the difference between:

- historical simulation assumptions
- and live exchange-driven state handling.

## Exchange Authority and State Trust Model

## Exchange truth

The following are exchange-authoritative:

- whether a position exists
- position side and size
- whether a protective stop exists
- whether an order is open, filled, canceled, rejected, or unknown
- exchange-side account impacts relevant to live management

## Local truth

Local runtime state is authoritative only for:

- the bot’s intended workflow stage
- stored references to orders and stops
- local exception flags
- restart context
- operator-facing continuity
- internal control state such as safe mode or kill switch

## Architectural implication

Any conflict between local state and exchange state must be resolved in favor of exchange truth, with appropriate incident/recovery handling.

## Persistence Model

The v1 system should distinguish three persistence categories.

## 1. Research Persistence

### Purpose

Supports historical research, backtesting, and validation.

### Typical form

- Parquet datasets
- raw source payloads
- derived research datasets
- version manifests

### Characteristics

- immutable or versioned
- reproducible
- analytical

## 2. Runtime Operational Persistence

### Purpose

Supports restart safety, recovery, and runtime continuity.

### Should persist at minimum

- current strategy symbol
- strategy stage
- current signal reference
- entry order identifiers
- protective stop identifiers
- current position references
- stop-management stage
- trailing stage if active
- reconciliation timestamps
- exception flags
- safe mode / kill switch state

### Characteristics

- small
- durable
- restart-critical
- operational rather than analytical

## 3. Operational Logging and Observability Outputs

### Purpose

Supports debugging, incident review, operator visibility, and review workflows.

### Includes

- structured runtime events
- incident records
- restart/recovery logs
- order lifecycle events
- stream-health events
- operator action records
- alerting outputs

### Characteristics

- chronological
- diagnostic
- review-friendly
- must redact secrets appropriately

## Core Runtime Flows

## 1. Signal-to-Protected-Position Flow

```text
market-data intake
  -> completed 15m bar available
  -> strategy evaluation
  -> risk/sizing approval
  -> execution submits market entry
  -> exchange/user-stream confirms fill and position
  -> execution submits protective stop
  -> exchange/user-stream confirms stop
  -> protected live position state
```

### Important rule

The runtime should not treat a trade as safely active until the protective stop is also confirmed.

## 2. Strategy-Managed Stop Update Flow

```text
completed bar / trade-stage update
  -> strategy determines stop-update intent
  -> execution verifies current position and active stop
  -> cancel existing protective stop
  -> confirm cancellation
  -> submit replacement protective stop
  -> confirm replacement exists
  -> update local runtime state
```

### Important rule

If stop replacement cannot be confirmed, the runtime must enter an exception path rather than assume protection exists.

## 3. Restart and Recovery Flow

```text
process start / restart
  -> enter safe mode
  -> load persisted local state
  -> verify prerequisites
  -> restore user stream
  -> fetch exchange position state
  -> fetch open normal orders
  -> fetch open algo orders
  -> reconcile local vs exchange state
  -> classify clean / recoverable / unsafe
  -> repair or escalate
  -> exit safe mode only if state certainty is restored
```

## 4. Incident Handling Flow

```text
detect abnormality
  -> classify incident
  -> contain
  -> verify exchange truth
  -> recover if safe
  -> escalate if not safe
  -> operator review if required
  -> resume only after state confidence is restored
```

## Recommended v1 Process Model

## Core runtime model

The recommended v1 runtime is:

- one primary bot process
- one deployment unit
- one symbol scope
- one persistent local state store
- one operator-visible status surface

Within that runtime, internal modules should remain clearly separated.

## Why not microservices

A microservice or distributed event-driven design would add major costs:

- more moving parts
- more deployment complexity
- more coordination failures
- more logging/monitoring burden
- harder restart reasoning
- more ambiguous local-vs-remote failure states

Those costs are not justified for the current v1 scope.

## Internal modularity is still required

Choosing a modular monolith does **not** mean writing one giant undifferentiated process.

The codebase should still reflect the component boundaries defined here.

## Recommended Implementation Sequence

The architecture should be implemented in the following order.

## Phase A — shared foundations

Build first:

- configuration loading
- secret-loading integration
- exchange metadata access
- structured logging foundation
- runtime mode / safety-state primitives
- deterministic client order ID utility
- time and clock utilities

## Phase B — research/runtime strategy parity foundation

Build next:

- reusable strategy-calculation logic
- completed-bar handling
- strategy decision interfaces
- risk and sizing calculations

The goal here is to make strategy logic portable between research validation and live runtime where appropriate.

## Phase C — exchange execution core

Build next:

- entry order submission path
- protective stop submission path
- order-role tagging
- execution result normalization
- exchange-rule compliance checks

## Phase D — user stream and runtime state core

Build next:

- user-stream lifecycle
- private event normalization
- runtime state persistence
- order / position / stop state updates
- reconciliation helpers

## Phase E — restart and incident control

Build next:

- safe-mode startup
- reconciliation workflow
- restart classification
- incident classification hooks
- kill-switch behavior
- blocked / paused modes

## Phase F — operator surface

Build next:

- operator-visible status output
- manual controls
- recovery / pause / restart visibility
- approval capture where required

## Phase G — paper / shadow readiness

Only after the above:

- dry-run / test-order flows
- promotion-readiness checks
- review-process support
- release-process integration

## Explicit Non-Goals for V1

The following are not implementation goals for the first live-capable architecture:

- distributed microservice deployment
- multi-symbol concurrent orchestration
- portfolio-level risk routing
- hedge-mode support
- autonomous strategy switching
- machine-learning-driven live decisions
- alternative-data-driven live logic
- order-book / tick-level execution optimization
- complex event-bus infrastructure
- lights-out unattended production autonomy

## Decisions

The following decisions are accepted for the v1 implementation blueprint:

- v1 should be implemented as a **modular monolith**
- strategy and execution must remain separate
- exchange state is authoritative for live position/order/stop truth
- local runtime state exists for orchestration, persistence, recovery, and operator continuity
- research and live runtime remain separate system domains
- user-stream handling is a core architecture component, not a utility detail
- restart/recovery logic is a core architecture component, not an operational afterthought
- safety controls such as safe mode and kill switch are part of the runtime architecture
- the operator interface is part of the system boundary in supervised v1
- narrow scope is intentional and should be preserved through the first implementation phase

## Open Questions

The following remain open for the next architecture documents:

1. What exact runtime state model and state transitions should be standardized?
2. What exact persistent storage format should be used for runtime operational state?
3. What exact internal event and command interfaces should connect strategy, execution, and reconciliation layers?
4. What exact health metrics and alert schema should be required in v1?
5. What exact operator-visible actions and approvals should the first dashboard expose?
6. What exact release and promotion controls should gate paper / shadow and tiny live progression?

## Next Steps

After this document, the next recommended files are:

1. `docs/08-architecture/state-model.md`
2. `docs/08-architecture/observability-design.md`
3. `docs/11-interface/operator-dashboard-requirements.md`
4. `docs/09-operations/release-process.md`
