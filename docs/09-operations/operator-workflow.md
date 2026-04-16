# Operator Workflow

## Purpose

This document defines the operator workflow for the v1 trading system.

Its purpose is to specify:

- what the human operator is responsible for,
- what the bot may handle automatically,
- what must be checked before trading is allowed,
- what must be monitored during runtime,
- what actions the operator may take,
- and what situations require explicit review or approval.

This document exists because v1 is a **supervised trading system**, not a fully autonomous one.

## Scope

This workflow applies to the v1 deployment assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only
- one-way mode
- isolated margin
- one position maximum
- one active protective stop maximum
- supervised operation
- operator-visible health and incident state

This document covers:

- pre-run checks,
- runtime supervision,
- manual intervention boundaries,
- incident-related operator actions,
- and post-run review expectations.

This document does **not** define:

- full incident procedures,
- restart internals,
- or UI implementation details.

Those are covered by related documents.

## Background

The v1 system is intentionally designed to be:

- rules-based,
- tightly scoped,
- safety-first,
- and operator-supervised.

That means the operator is part of the system.

The operator is not expected to micromanage every trade decision, but is expected to:

- verify readiness before live operation,
- monitor system health,
- respond to defined alerts,
- approve recovery after serious incidents,
- and prevent the system from running in unsafe uncertainty.

## Operator Role Definition

## Core operator responsibilities

The operator is responsible for:

- approving live readiness before trading is enabled
- verifying that the system is not in an unsafe or uncertain state
- monitoring health, synchronization, and incident signals
- responding to alerts and escalations
- deciding on pause, restart, kill-switch, or emergency intervention when required
- reviewing trading behavior and operational outcomes after runtime periods
- preserving disciplined operation rather than improvising around problems

## What the operator is not supposed to do

The operator should **not** casually:

- override strategy logic ad hoc
- place manual exchange trades that bypass bot awareness during normal operation
- silently restart the system without following restart procedure
- change live parameters informally mid-run
- ignore state uncertainty because “it probably fixed itself”

## Operational Philosophy

## Core principle

The operator supervises the bot, but does not constantly interfere with normal system behavior.

### This means:
- normal strategy operation should proceed without manual micromanagement
- manual action should occur when:
  - a defined alert is raised,
  - a required approval gate is reached,
  - a policy threshold is crossed,
  - or system state becomes uncertain

## Safety principle

If there is uncertainty about:

- position state,
- protective stop state,
- exchange synchronization,
- stream health,
- or execution correctness,

then the operator should favor:

- pausing,
- safe mode,
- restart with reconciliation,
- or controlled de-risking

over “letting it continue and hoping.”

## Operator-Visible System States

The operator workflow assumes the system exposes a clear top-level operating state.

Recommended operator-visible states:

- `RUNNING_HEALTHY`
- `SAFE_MODE`
- `RECOVERING`
- `INCIDENT_ACTIVE`
- `KILL_SWITCH_ACTIVE`
- `BLOCKED_AWAITING_OPERATOR`
- `PAUSED_BY_OPERATOR`

## Meaning of each state

### `RUNNING_HEALTHY`
The system is operating normally.

Requirements:
- no blocking incident
- no unresolved mismatch
- streams healthy
- state synchronized
- normal strategy operation allowed

### `SAFE_MODE`
The system has blocked new entries due to uncertainty or control policy.

Requirements:
- no new exposure
- only safety, recovery, verification, or exit actions allowed

### `RECOVERING`
The system is executing restart or reconciliation logic.

Requirements:
- operator should observe
- system should not be treated as normal
- new trading not allowed until recovery completes

### `INCIDENT_ACTIVE`
An incident is currently being handled.

Requirements:
- operator should review classification and containment
- follow incident policy

### `KILL_SWITCH_ACTIVE`
The kill switch has been triggered.

Requirements:
- trading remains halted
- operator review is required before any resumption

### `BLOCKED_AWAITING_OPERATOR`
The bot cannot safely proceed without explicit human decision.

Requirements:
- operator action required
- no automatic continuation

### `PAUSED_BY_OPERATOR`
The bot has been intentionally paused by the operator.

Requirements:
- no new entries
- remain paused until operator clears the condition

## Pre-Run Workflow

Before enabling live trading or supervised runtime, the operator should complete the pre-run checklist.

## Pre-run checklist

- [ ] Correct environment is loaded
- [ ] Correct strategy version is deployed
- [ ] Correct configuration version is loaded
- [ ] API credentials are present and valid
- [ ] Required permissions are available
- [ ] No credential-security warning is active
- [ ] Exchange connectivity is healthy
- [ ] Market-data stream is healthy
- [ ] User-data stream is healthy
- [ ] Local state has loaded correctly
- [ ] Restart or reconciliation has completed successfully
- [ ] No unresolved incident is active
- [ ] System is not in safe mode
- [ ] Kill switch is not active
- [ ] No unexpected open position exists
- [ ] No unexpected open order exists
- [ ] If a position exists intentionally, protective stop is confirmed
- [ ] Risk controls are active
- [ ] Logging and monitoring are active
- [ ] Operator is available for supervision during the intended runtime window

## Pre-run decision rule

If any checklist item fails in a way that affects state certainty or safety, the system should not be allowed to proceed into normal live trading.

The operator should favor delay over unsafe activation.

## Runtime Workflow

## Normal runtime expectations

During normal operation, the operator should monitor:

- overall system mode
- stream health
- exchange connectivity
- current position state
- protective stop confirmation
- active incidents or warnings
- reconciliation warnings
- kill-switch status
- risk lockouts or trading pauses

## Runtime supervision principle

The operator should supervise the system actively enough to catch meaningful abnormalities, but should not interfere unnecessarily with normal strategy execution.

### Good operator behavior
- watch health and status
- respond to meaningful alerts
- verify that the system remains synchronized
- let the bot execute its defined logic normally

### Bad operator behavior
- changing behavior impulsively without documented reason
- manual interventions that are not logged or reconciled
- overriding the bot repeatedly because of discomfort rather than policy

## Runtime health checks

The operator should be able to answer these questions during runtime:

- Is the bot in a healthy operating state?
- Is there an open position?
- If yes, is the protective stop confirmed?
- Are streams healthy and current?
- Is there an active incident?
- Is the bot blocked, paused, or in safe mode?
- Has any unexpected order or mismatch appeared?
- Has any emergency control been triggered?

## Manual Operator Actions

The following operator actions are legitimate within the supervised v1 design.

## Allowed manual actions

### 1. Pause new entries
The operator may pause new entries when:
- uncertainty is growing
- conditions appear abnormal
- an incident is being investigated
- or supervision cannot continue reliably

### 2. Activate kill switch
The operator may activate the kill switch when:
- exposure safety is uncertain
- repeated incidents suggest unsafe operation
- system behavior is no longer trusted
- or emergency halt is required

### 3. Request controlled restart
The operator may trigger restart when:
- stream confidence is lost
- reconciliation is needed
- a restart is required by policy
- maintenance is needed

### 4. Approve recovery resumption
The operator may approve resumption after incidents or recovery when the relevant policy says human approval is required.

### 5. Emergency flattening
The operator may decide to flatten exposure during an emergency if:
- protection cannot be trusted
- state cannot be reconciled safely
- incident policy requires de-risking

### 6. Disable live operation
The operator may suspend or disable the bot after repeated abnormal behavior or unresolved risk conditions.

## Actions that should not be done casually

The operator should not casually:

- place manual exchange trades that the bot does not know about
- cancel bot-managed orders without following recovery logic
- modify live parameters mid-run outside controlled procedure
- ignore incident states and continue operation
- resume after serious incidents without review

## Approval Boundaries

The workflow should distinguish between situations where the bot may continue automatically and situations where explicit operator approval is required.

## Automatic continuation may be allowed for

- clean startup or restart
- severity 1 incidents
- some severity 2 incidents with no exposure risk
- self-healing conditions where state certainty remains intact

## Explicit operator approval is required for

- recovery after severity 3 incidents
- any severity 4 incident
- recovery from a recoverable restart mismatch
- emergency flattening aftermath
- kill-switch clearance
- suspected credential or security incident
- repeated abnormal behavior that triggered manual pause
- any situation where the system enters `BLOCKED_AWAITING_OPERATOR`

## Operator Response to Incidents

## Severity 1
Operator may simply review logs later unless repetition suggests escalation.

## Severity 2
Operator should monitor recovery and verify no escalation is occurring.

## Severity 3
Operator review is required before trusting resumed operation.  
The operator should confirm:
- incident classification is understood
- state has been reconciled
- exposure is protected
- restart/recovery outcome is acceptable

## Severity 4
Operator escalation is mandatory.  
The operator must confirm:
- whether exposure exists
- whether protection exists
- whether flattening is required
- whether credentials or trust boundaries are compromised
- whether operation should remain halted after containment

## Daily Operator Workflow

At least once during or after each active trading day, the operator should review:

- whether the bot traded
- whether any incidents occurred
- whether any unexpected warnings appeared
- whether any restart or recovery took place
- whether positions and exits matched expectations at a high level
- whether logs and monitoring remained healthy
- whether any unresolved questions should be documented

This does not need to be a heavy manual process in v1, but it should be consistent.

## Weekly Operator Workflow

At least once per week during active operation, the operator should review:

- incident frequency
- restart frequency
- stream-health stability
- order-handling anomalies
- protective-stop reliability
- whether any manual interventions were required
- whether current operating restrictions remain appropriate
- whether any docs, thresholds, or alerts need refinement

## Operator Notes and Recordkeeping

The operator should maintain brief records of meaningful events, including:

- pauses
- kill-switch activations
- emergency flattening decisions
- manual restart decisions
- repeated warnings
- unusual exchange behavior
- resumption approvals after serious incidents

These notes can be lightweight, but they are important for continuity and later review.

## Healthy Operation Criteria

The system may be considered in healthy supervised operation when all of the following are true:

- `RUNNING_HEALTHY` state is active
- no blocking incident is active
- no unresolved mismatch exists
- streams are healthy
- exchange connectivity is normal
- no unauthorized or degraded credential state exists
- position and protective-stop state are synchronized
- operator remains available for supervision

If these conditions are not met, the operator should assume the system is degraded until proven otherwise.

## Escalation Triggers

Immediate operator attention is required when any of the following occurs:

- position exists without confirmed protective stop
- kill switch activates
- system enters `BLOCKED_AWAITING_OPERATOR`
- restart recovery fails
- repeated reconciliation mismatch occurs
- user stream becomes stale while exposure exists
- execution status becomes unknown on a critical order
- suspected credential exposure or authorization anomaly appears
- local and exchange position materially disagree

## Relationship to Future Interface

This workflow implies that the future operator interface should expose, at minimum:

- current system mode
- stream health
- exchange connectivity health
- open position status
- protective stop status
- active incident state
- restart/recovery state
- kill-switch status
- manual pause status
- operator action controls
- alert summaries

This document therefore serves as an operational requirements input for the future desk monitor / dashboard.

## Failure Modes in Operator Workflow

The operator workflow is expected to guard against these human/system interaction failures:

### 1. Passive supervision
The operator is present but not actually monitoring health or incident state.

### 2. Excessive interference
The operator disrupts normal bot behavior without policy reason.

### 3. Unsafe resumption
The system is resumed after an incident without sufficient review.

### 4. Unlogged manual intervention
The operator acts manually but leaves no trace of what was done.

### 5. Alert fatigue
Warnings accumulate until serious signals are no longer treated seriously.

### 6. Ambiguous human/bot responsibility
Neither the system nor the operator has a clearly defined duty during an incident.

This workflow exists partly to avoid those failures.

## Decisions

The following decisions are accepted for the operator workflow:

- v1 is a supervised system, not a lights-out autonomous system
- the operator is responsible for startup readiness, incident review, and resumption approval where required
- the operator should supervise normal operation without constant interference
- pre-run checks are mandatory before live operation
- the operator may pause, restart, activate kill switch, approve recovery, and emergency-flatten when required
- explicit approval is required after serious incidents and emergency states
- operator-visible system state must be clear and limited to a well-defined set of modes
- daily and weekly operator review routines are part of normal supervised operation

## Open Questions

The following remain open:

1. What exact operator dashboard layout will best support this workflow?
2. Which alerts should require immediate notification versus passive logging only?
3. What exact conditions should trigger automatic operator escalation outside the current severity framework?
4. Should there be a formal sign-off record for resumption after severity 4 incidents?
5. What exact retention policy should apply to operator notes and action history?
6. Should operator approval for resumption be captured directly in the future interface or only in external notes/logs?

## Next Steps

After this document, the next recommended files are:

1. `docs/10-security/secrets-management.md`
2. `docs/09-operations/daily-weekly-review-process.md`
3. `docs/11-interface/operator-dashboard-requirements.md`

## References

Related internal project documents:

- `docs/09-operations/incident-response.md`
- `docs/09-operations/restart-procedure.md`
- `docs/10-security/api-key-policy.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`