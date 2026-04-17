# Observability Design

## Purpose

This document defines the observability design for the v1 Prometheus trading system.

Its purpose is to ensure that the runtime exposes enough information to support:

- capital protection,
- state certainty,
- restart and recovery confidence,
- incident handling,
- operator supervision,
- and disciplined daily / weekly review.

This document exists because the v1 system is not judged only by whether it can place orders.

It must also be judged by whether the operator can answer, at all times:

- is the bot healthy,
- is there live exposure,
- is that exposure protected,
- are required streams trusted,
- has reconciliation succeeded,
- is an incident active,
- and is human action required.

This document defines the observability contract for the live runtime.

It does **not** define:

- the full operator dashboard layout,
- the full runtime state model,
- generic infrastructure monitoring beyond what v1 needs,
- or code-level implementation details for logging libraries or telemetry backends.

## Scope

This observability design applies to the v1 system assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only in the first live-capable scope
- one-way mode
- isolated margin
- one open position maximum
- one active protective stop maximum
- supervised operation
- restart begins in safe mode
- incident handling is severity-based
- exchange-side protective stop is mandatory for live positions

This document covers:

- observability goals,
- structured event/log design,
- required event fields,
- health dimensions,
- alerts and escalation levels,
- restart and reconciliation visibility,
- incident visibility,
- operator action audit requirements,
- review-process support,
- and security / redaction requirements.

This document does **not** cover:

- final dashboard wireframes,
- host-level infrastructure monitoring policy in depth,
- enterprise SIEM design,
- or high-scale distributed tracing architecture.

## Background

The current project documents already define several observability-dependent requirements.

The timestamp policy requires canonical UTC timestamps and recommends tracking both event time and processing time where practical.

The order-handling notes require exchange-confirmed visibility into entry, position, and protective-stop status, plus deterministic client order IDs for traceability.

The restart procedure requires restart mode, exchange state, reconciliation classification, repair actions, and safe-mode exit to be logged clearly.

The incident-response model requires every incident to leave an audit trail with class, severity, actions, and resolution state.

The operator workflow and daily / weekly review process both assume that the operator can quickly understand:

- system mode,
- stream health,
- position state,
- protection state,
- incident state,
- kill-switch or pause state,
- restart/recovery status,
- and whether immediate action is required.

This document consolidates those requirements into one observability design.

## Observability Goals and Non-Goals

## Core Goals

The v1 observability design exists primarily to support:

### 1. Capital protection
The operator and the bot must be able to determine quickly whether live exposure exists and whether it is protected.

### 2. State certainty
The runtime must surface whether local and exchange state are aligned or whether reconciliation is required.

### 3. Recovery confidence
Restart, reconnect, and recovery flows must be observable enough to confirm whether safe resumption is justified.

### 4. Incident handling
Incidents must be detectable, classifiable, traceable, and reviewable afterward.

### 5. Operator supervision
The operator must be able to supervise without micromanaging and without guessing.

### 6. Review continuity
Daily and weekly reviews must be supported by durable records of important runtime behavior.

## Non-Goals

The v1 observability design is **not** primarily intended for:

- vanity dashboards,
- marketing-style performance displays,
- generic high-scale infrastructure monitoring,
- exhaustive distributed tracing,
- or speculative analytics unrelated to operational safety.

## Design Principle

The observability design for v1 should be:

- **state-centric**
- not **infrastructure-centric**

The primary question is not:

> “How many technical metrics can we emit?”

The primary question is:

> “Can we trust the bot’s exposure, protection, and recovery state, and can the operator prove that trust?”

## Core Observability Pillars

The v1 observability design should be built around four pillars.

## 1. Structured event logs

These provide the chronological record of what happened.

They should capture:

- runtime mode changes,
- execution lifecycle events,
- stream health changes,
- reconciliation and restart activity,
- incident activity,
- and operator actions.

Structured events are the main audit trail.

## 2. Health indicators

These provide the current-state view of whether the bot is trustworthy to continue normal operation.

Health indicators should answer questions such as:

- are streams healthy,
- is exchange connectivity acceptable,
- is a position open,
- is the position protected,
- is reconciliation required,
- is safe mode active,
- is an incident active,
- and is operator action required.

## 3. Alerts

These surface conditions that need attention.

The alert model should distinguish between:

- informational,
- warning,
- and critical conditions.

Alerts should be tied to operational safety, not just to noisy technical symptoms.

## 4. Operator-facing summaries

These provide a condensed current view suitable for supervised operation.

The operator must be able to understand quickly:

- current system mode,
- whether exposure exists,
- whether protection exists,
- whether recovery or incident handling is active,
- and whether manual action is required.

## Structured Event Model

The runtime should emit structured events organized into clear families.

## Event Family 1 — System and Runtime Events

These events describe top-level runtime behavior.

### Examples

- process started
- process stopping
- runtime mode changed
- safe mode entered
- safe mode exited
- recovering mode entered
- blocked-awaiting-operator mode entered
- operator review required set or cleared
- kill switch enabled or cleared
- operator pause enabled or cleared
- startup credential validation passed or failed
- startup configuration validation passed or failed

## Event Family 2 — Market-Data Events

These events describe the health and behavior of required market data.

### Examples

- market-data stream connected
- market-data stream disconnected
- market-data freshness degraded
- market-data marked stale
- market-data restored
- completed bar published
- bar-completion delay detected

## Event Family 3 — User-Stream and Account Events

These events describe the health of the private exchange event stream and important account-side event intake.

### Examples

- listen key obtained
- listen key keepalive succeeded
- listen key keepalive failed
- user stream connected
- user stream disconnected
- user stream marked stale
- user stream restored
- private event received
- order/account/algo update normalized

## Event Family 4 — Execution Events

These events describe strategy-owned execution workflow events.

### Examples

- entry submission started
- entry submitted
- entry acknowledged
- entry fill confirmed
- position confirmed
- protective stop submission started
- protective stop submitted
- protective stop confirmed
- stop replacement started
- stop cancellation confirmed
- replacement stop confirmed
- exit submission started
- exit confirmed
- execution uncertainty detected
- order rejected
- algo order rejected

## Event Family 5 — Reconciliation and Restart Events

These events describe confidence restoration behavior.

### Examples

- restart initiated
- restart mode identified
- local state loaded
- exchange position queried
- exchange open orders queried
- exchange open algo orders queried
- reconciliation required
- reconciliation started
- reconciliation classified clean
- reconciliation classified recoverable mismatch
- reconciliation classified unsafe mismatch
- repair action taken
- repair action succeeded or failed
- emergency branch entered
- restart completed
- safe mode exit allowed
- safe mode exit blocked

## Event Family 6 — Incident Events

These events describe incident lifecycle behavior.

### Examples

- incident opened
- incident class assigned
- incident severity assigned
- containment action taken
- operator escalation triggered
- incident resolution state changed
- incident resolved automatically
- incident resolved with operator action
- incident blocked pending review
- post-incident review required

## Event Family 7 — Operator Action Events

These events describe manual control actions taken by the operator.

### Examples

- operator pause enabled
- operator pause cleared
- kill switch enabled
- kill switch cleared
- restart requested
- recovery approved
- recovery denied
- emergency flatten requested
- live operation disabled
- operator note recorded if such capability exists later

## Event Family 8 — Review Support Events

These events are not necessarily user-facing alerts, but they support continuity and later review.

### Examples

- daily review period closed
- weekly review summary prepared
- repeated warning class threshold crossed
- incident pattern threshold crossed
- review follow-up required

## Required Event Fields

A consistent core field set should exist across important structured events.

## Core Required Fields

Where relevant, important events should include:

- canonical UTC timestamp
- event type
- event family
- runtime mode
- symbol
- strategy identifier or active strategy name
- protection state if relevant
- trade lifecycle state if relevant
- reconciliation state if relevant
- incident-active flag
- correlation or trace reference if available

## Time Fields

Where practical, event records should distinguish between:

- **event time**
- and
- **processing time**

### Event time
The timestamp associated with the underlying event itself.

Examples:
- order update event time
- account update event time
- bar close time
- funding time

### Processing time
The timestamp at which the bot processed or recorded the event.

### Why both matter
Tracking both helps with:

- delayed-event diagnosis,
- stale-stream detection,
- latency reasoning,
- and failure reconstruction.

## Exchange-Related Fields

Where relevant, execution and reconciliation events should include:

- client order ID
- exchange order ID
- order role
- side
- order type
- position side where relevant
- position size if relevant
- stop trigger reference where relevant

## Incident Fields

Incident events should include:

- incident ID
- incident class
- severity
- exposure-present yes/no
- protection-confirmed yes/no
- resolution state
- operator-review-required yes/no

## Operator Action Fields

Operator action events should include:

- action type
- operator identity or alias where available
- reason or note where available
- resulting runtime mode or control state change

## Health Model

The runtime should expose a minimum set of live health dimensions.

## 1. Exchange Connectivity Health

### Purpose
Indicates whether required REST interaction paths are currently reachable enough for safe operation and recovery.

### Minimum states
- healthy
- degraded
- unavailable

### Why it matters
Placement, cancellation, reconciliation, and recovery all depend on exchange reachability.

## 2. Market-Data Health

### Purpose
Indicates whether required market-data inputs are connected and fresh enough for strategy evaluation.

### Minimum states
- healthy
- degraded
- stale
- unavailable

### Why it matters
The strategy depends on completed bars and should not continue normal entry behavior if required market data is stale or unavailable.

## 3. User-Stream Health

### Purpose
Indicates whether the private stream is connected, maintained, and trustworthy.

### Minimum states
- healthy
- degraded
- stale
- unavailable
- restoring

### Why it matters
User-stream events are the primary live source of truth during normal operation.

## 4. Position and Protection Health

### Purpose
Indicates whether exposure exists and whether acceptable protective coverage is confirmed.

### Minimum states
- no position
- position unconfirmed
- position unprotected
- stop pending confirmation
- position protected
- protection uncertain
- emergency unprotected

### Why it matters
This is one of the highest-priority health dimensions in the system.

## 5. Reconciliation Health

### Purpose
Indicates whether local and exchange state are aligned enough for normal operation.

### Minimum states
- not required
- required
- in progress
- clean
- recoverable mismatch
- repaired pending recheck
- unsafe mismatch

## 6. Runtime Control Health

### Purpose
Indicates whether system-level controls are preventing normal progression.

### Minimum states / flags
- safe mode active yes/no
- recovering yes/no
- blocked awaiting operator yes/no
- kill switch active yes/no
- paused by operator yes/no
- operator review required yes/no
- entries blocked yes/no

## 7. Incident Health

### Purpose
Indicates whether any incident is open and whether escalation is active.

### Minimum fields
- incident active yes/no
- highest active severity
- active incident count
- escalation pending yes/no

## Health Summary Principle

The operator should be able to answer these questions immediately from the health model:

- Is the bot in normal operation?
- Is there open exposure?
- If yes, is that exposure protected?
- Are streams healthy enough to trust the bot’s view?
- Is reconciliation required?
- Is an incident active?
- Is human action required before continuation?

## Alert Model and Escalation

The alert model should be operationally meaningful and restrained.

## Alert Levels

### Informational

Used for:

- successful recoveries
- non-blocking lifecycle changes
- normal transitions worth recording
- actions that may matter later in review but do not require immediate intervention

### Warning

Used for:

- degraded but currently contained conditions
- repeated abnormal behavior that has not yet become emergency state
- conditions that should be reviewed soon and may escalate if repeated or combined with exposure

### Critical

Used for:

- conditions that threaten capital protection,
- materially undermine state certainty,
- or require immediate operator awareness

## Critical Alert Examples

The following should be treated as critical alerts in v1:

- open position without confirmed protective stop
- protection state uncertain while exposure exists
- user stream stale while exposure exists
- reconciliation classified `unsafe mismatch`
- critical execution outcome unknown while exposure may exist
- restart recovery failure while exposure exists
- emergency branch entered
- suspected credential or secret-security incident
- local and exchange position materially disagree

## Warning Alert Examples

The following should normally be warnings:

- repeated stream reconnects while flat
- repeated recoverable mismatches
- repeated delayed confirmation events
- stop-update delay while prior stop protection remains confirmed
- market-data freshness degraded without current exposure risk
- repeated severity-2 incidents of the same class

## Informational Alert Examples

The following are typically informational:

- clean restart completed
- stream restored cleanly
- operator pause enabled
- operator pause cleared
- reconciliation completed cleanly
- incident auto-resolved without exposure risk

## Escalation Rule

Alerting should favor:

- low false-negatives on protection/state-certainty failures
- and lower tolerance for noise on minor technical events

The system should avoid creating alert fatigue from trivial events while still escalating quickly when exposure, protection, or recovery trust is at stake.

## Restart and Reconciliation Visibility Requirements

The observability design must make restart and recovery behavior reviewable.

## Required restart visibility

At minimum, restart observability should expose:

- restart timestamp
- restart mode
- restart reason if known
- software/config version if available
- whether local state was loaded
- whether exchange position was checked
- whether normal open orders were checked
- whether algo open orders were checked
- whether user stream was restored
- reconciliation result
- repair actions taken
- emergency branch triggered yes/no
- safe mode exit allowed or blocked
- operator review required yes/no

## Required reconciliation visibility

At minimum, reconciliation observability should expose:

- why reconciliation was required
- when it started
- what sources were compared
- result classification
- mismatch summary
- repair action summary
- whether recheck succeeded
- whether normal operation remained blocked

## Visibility principle

A restart is not observably successful merely because the process is online.

It is successful only if the logs and status outputs show that state certainty was restored or that the system remained blocked safely.

## Incident Visibility Requirements

The observability design must support full incident lifecycle visibility.

## Required incident fields

At minimum, incident records should include:

- incident ID
- incident class
- severity
- detection timestamp
- symbol where relevant
- runtime mode at detection
- whether exposure existed
- whether protection was confirmed
- containment action taken
- escalation triggered yes/no
- operator review required yes/no
- resolution state
- resume timestamp if resumed
- post-incident review required yes/no

## Incident resolution states

Incident records should clearly expose one of:

- resolved automatically
- resolved with operator action
- contained awaiting review
- unresolved blocked
- escalated emergency

## Post-incident review support

Severity 3 and 4 incidents should leave enough observability detail to support a later review of:

- what happened
- what the bot knew
- what the exchange showed
- what action was taken
- and what should change

## Operator Action Audit Requirements

Manual interventions must never disappear into undocumented behavior.

## Required operator action visibility

At minimum, the system should record:

- what action was taken
- when it was taken
- who took it where identity is available
- what runtime or control state changed
- whether the action affected exposure, restart, or recovery
- and whether follow-up review is required

## Important operator actions to audit

- pause enabled / cleared
- kill switch enabled / cleared
- restart requested
- recovery approved / denied
- emergency flatten requested
- live operation disabled
- manual containment / manual resumption if added later

## Audit principle

The operator must not need to rely on memory alone to explain meaningful manual interventions later.

## Daily and Weekly Review Support Requirements

The observability design must support the review process already defined elsewhere.

## Daily review support

Observability outputs should make it easy to determine:

- whether the bot was active
- whether trades occurred
- whether exposure remained protected
- whether incidents occurred
- whether warnings occurred
- whether restart or reconciliation occurred
- whether any manual actions occurred
- whether unresolved issues remained at period end

## Weekly review support

Observability outputs should make it easy to summarize:

- active days count
- trade count
- incidents by severity
- warning patterns
- restart count
- stale-stream count
- mismatch count
- manual intervention count
- emergency action count
- recurring abnormal classes

## Review continuity principle

The logging and event model should make review possible without forcing the operator to manually reconstruct the whole week from raw unstructured text.

## Security and Redaction Rules

Observability must respect the project’s security rules.

## Forbidden in observability outputs

The system must not expose in normal logs, metrics, or status outputs:

- API secrets
- secret-bearing environment dumps
- full live API key material where avoidable
- raw signatures
- full authenticated payloads containing sensitive material
- copied secret-bearing configuration blobs

## Allowed with caution

The system may expose, where appropriate:

- key alias
- environment label
- masked identifier
- validation success/failure state
- permission or authorization category

## Redaction principle

Security-sensitive material must be redacted by default.

Observability should help diagnose credential and authorization problems without increasing secret-exposure risk.

## Design Preferences for V1

The v1 observability design should prefer:

- structured event logs over ad hoc free-text logs
- state-centric summaries over infrastructure trivia
- clear critical alerts over noisy low-value alerts
- durable incident and operator-action records
- enough detail for recovery review without excessive complexity

The design should avoid premature observability sprawl.

## Decisions

The following decisions are accepted for the v1 observability design:

- observability should be state-centric rather than infrastructure-centric
- structured event logs are required for major runtime, execution, restart, incident, and operator events
- event time and processing time should be tracked separately where practical
- the runtime must expose health dimensions for exchange connectivity, market data, user stream, position/protection, reconciliation, control state, and incidents
- alerting should use meaningful severity bands: informational, warning, and critical
- protection uncertainty and exposure-risk ambiguity are critical observability conditions
- restart and reconciliation behavior must be explicitly visible
- incident lifecycle records are mandatory
- operator manual actions must be auditable
- observability outputs must support daily and weekly operational review
- observability must respect secrets-management and API-key redaction rules

## Open Questions

The following remain open for later implementation and interface work:

1. What exact log schema and serialization format should be standardized for v1?
2. What exact thresholds should define stale market data and stale user-stream conditions in the alerting layer?
3. What exact channels should be used for warning versus critical alerts?
4. What exact counters and summaries should be materialized as metrics versus derived from event logs?
5. Should the first dashboard show raw event feeds, summarized state, or both?
6. What exact review summary generation should be automated later for daily and weekly operator workflows?

## Next Steps

After this document, the next recommended files are:

1. `docs/11-interface/operator-dashboard-requirements.md`
2. `docs/09-operations/release-process.md`
3. `docs/10-security/permission-scoping.md`
