# Incident Response

## Purpose

This document defines how the trading system should respond to operational incidents during live or supervised operation.

Its purpose is to ensure that when something goes wrong, the system responds in a way that prioritizes:

- capital protection,
- state certainty,
- controlled recovery,
- and clear operator visibility.

This document exists because a production trading system must not improvise its behavior during failures.

## Scope

This document applies to incidents affecting:

- live trading operation,
- exchange connectivity,
- order and position state,
- protective stop integrity,
- authentication and permissions,
- restart recovery,
- and operator trust in system state.

This document applies to the v1 system assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only
- one-way mode
- isolated margin
- one position maximum
- one active protective stop maximum
- supervised deployment

This document does **not** replace:

- the restart procedure,
- the API key policy,
- or the detailed order-handling notes.

Instead, it defines the incident-management framework that sits above them.

## Background

The v1 system depends on:

- exchange-side order state,
- exchange-side position state,
- exchange-side protective stop state,
- user-stream events,
- market-data streams,
- signed API requests,
- and local persisted state.

When any of these become unreliable, the bot must not simply “keep trying” without structure.

Some failures are low-risk and recoverable. Others create uncertainty about whether the account is protected or even whether the bot’s local state matches reality.

This document establishes the rules for handling those situations.

## Incident Response Philosophy

## Core principle

**Containment comes before continuation.**

When an incident occurs, the first question is not:

> “How do we keep trading?”

The first question is:

> “Are we safe, protected, and sure about the current state?”

## State-certainty principle

If the bot cannot trust its view of:

- position state,
- protective stop state,
- or exchange execution state,

then normal strategy operation must stop until certainty is restored.

## Safe-mode principle

Incidents that create meaningful uncertainty must place the bot into:

- **safe mode**

In safe mode:

- no new entries are allowed
- strategy order generation is blocked
- only recovery, verification, cancellation, protection, or flattening actions are allowed

## Auditability principle

Every incident must leave an audit trail.

The system must be able to answer afterward:

- what happened,
- when it happened,
- what the bot did,
- what the operator did,
- and whether the system resumed safely.

## Incident Lifecycle

Every incident should follow this lifecycle:

1. **detect**
2. **classify**
3. **contain**
4. **verify state**
5. **recover or escalate**
6. **document**
7. **review afterward**

This sequence should be treated as the default pattern unless a documented emergency condition requires immediate flattening or forced halt.

## Severity Levels

## Severity 1 — Informational

This is a low-risk event that does not materially threaten trading safety or state certainty.

### Examples
- temporary recoverable warning with no open position
- expected reconnect that succeeds cleanly
- metadata refresh delay with no trading impact
- non-critical logging or monitoring issue

### Default response
- log the event
- continue normal operation if no safety boundary is crossed
- no operator interruption required unless repeated

## Severity 2 — Degraded but Contained

The system is degraded, but exposure risk is controlled and state certainty remains acceptable.

### Examples
- temporary market-data delay with no open position
- transient REST throttling without open exposure
- delayed non-critical account-read operation
- temporary stream interruption that recovers before state ambiguity is introduced

### Default response
- log and classify the incident
- monitor recovery
- optionally reduce confidence state
- do not necessarily enter safe mode if exposure and state certainty remain acceptable

## Severity 3 — Trading Impaired

The system’s ability to trade or manage state safely is impaired.

### Examples
- stale user stream while a position exists
- reconciliation mismatch
- repeated authorization failures
- unexpected open orders
- protective stop status uncertain
- restart recovery failure without immediate exposure-loss confirmation
- repeated unknown execution outcomes for non-trivial actions

### Default response
- enter safe mode
- block new entries
- verify exchange state
- recover or escalate before resuming
- operator visibility required

## Severity 4 — Emergency / Exposure Risk

This is an exposure-risk or account-risk emergency.

### Examples
- open position with no confirmed protective stop
- critical order returned unknown status and state cannot be confirmed quickly
- local and exchange position materially disagree
- suspected credential compromise
- kill switch triggered during live exposure
- recovery logic cannot determine whether the account is protected
- exchange state indicates dangerous ambiguity with live exposure

### Default response
- enter or remain in safe mode immediately
- block all new entries
- raise urgent operator-visible alert
- preserve or restore protection if possible
- flatten if protection cannot be trusted
- require explicit recovery review before any resumption

## Incident Classes

The following incident classes must be explicitly recognized by the system.

## 1. User-stream stale or unavailable

### Description
The private event stream becomes stale, disconnected, expired, or otherwise untrusted.

### Why it matters
The bot can no longer rely on live order, account, or protective-stop updates.

### Default severity
- Severity 2 if flat and no safety-critical action is in flight
- Severity 3 if a position exists or order state matters

### Default response
- block new entries if position exists or state uncertainty grows
- restore stream
- reconcile exchange state
- resume only after confidence is restored

## 2. Market-data stream stale

### Description
The required market-data feed becomes delayed, stale, or unavailable.

### Why it matters
The bot may lose the ability to evaluate signals or monitor bar completion correctly.

### Default severity
- Severity 2 if no open position and no action depends on live data
- Severity 3 if position management depends on the affected data stream

### Default response
- block new entries
- continue only if protection remains confirmed and management logic is still safe
- restore feed and verify freshness before resuming normal strategy activity

## 3. REST rate-limit / IP-ban risk

### Description
The bot receives throttling or request-rate warnings/errors suggesting API overuse or ban risk.

### Why it matters
Over-polling can degrade recovery capability and eventually prevent required safety actions.

### Default severity
- Severity 2 if no live exposure-risk consequence exists
- Severity 3 if recovery actions or state verification are impaired

### Default response
- reduce request rate
- prefer stream-based state where available
- preserve critical recovery budget
- escalate if protective verification becomes impaired

## 4. Unknown execution status

### Description
A critical exchange request returns a response where final execution outcome is not known with certainty.

### Why it matters
The bot may not know whether:
- the order was accepted,
- the order was filled,
- the order failed,
- or the account is now exposed.

### Default severity
- Severity 3 for non-trivial order ambiguity
- Severity 4 if exposure may exist and cannot be confirmed quickly

### Default response
- enter safe mode
- query exchange state
- inspect open orders, position, and relevant stream events
- do not retry blindly until state is known

## 5. Protective stop missing, rejected, or uncertain

### Description
A position exists, but the exchange-side protective stop is missing, rejected, stale, or cannot be confirmed.

### Why it matters
This is one of the most dangerous operational states in the system.

### Default severity
- Severity 4

### Default response
- emergency handling
- block all new entries
- restore protection immediately if possible
- flatten if protection cannot be restored safely
- require explicit review before resuming

## 6. Position mismatch

### Description
Local state and exchange state disagree about whether a position exists, its side, or its size.

### Why it matters
The bot cannot safely continue if it does not know its real exposure.

### Default severity
- Severity 3 if quickly recoverable
- Severity 4 if material and unresolved

### Default response
- enter safe mode
- reconcile using exchange state as authoritative
- restore local truth or flatten if necessary

## 7. Invalid credential / authorization failure

### Description
API requests fail due to invalid key, permission issue, IP restriction failure, or related authorization problem.

### Why it matters
Trading or recovery actions may no longer be possible, and credential integrity may be in question.

### Default severity
- Severity 3 for controlled configuration failures
- Severity 4 if compromise is suspected or live risk cannot be managed

### Default response
- fail closed
- block entries
- preserve current protective posture if possible
- escalate if exposure exists or compromise is suspected

## 8. Restart recovery failure

### Description
The restart procedure cannot complete safely.

### Why it matters
The process is online, but operational certainty has not been restored.

### Default severity
- Severity 3
- Severity 4 if exposure exists without confirmed protection

### Default response
- remain in safe mode
- escalate
- do not resume strategy activity

## 9. Exchange-side service degradation

### Description
The exchange or relevant service path behaves abnormally, including degraded responses or repeated service errors.

### Why it matters
Order actions or state queries may become unreliable even if the bot is working correctly.

### Default severity
- Severity 2 if no exposure-risk consequence exists
- Severity 3 or 4 if order state or protection is affected

### Default response
- reduce non-critical activity
- verify state through available channels
- block new exposure if certainty falls below acceptable threshold

## 10. Suspected secret exposure

### Description
An API credential may have been leaked, copied, logged, or otherwise exposed.

### Why it matters
This is an account-security incident, not just a software bug.

### Default severity
- Severity 4

### Default response
- halt or safe-mode the bot
- revoke or rotate affected credentials
- verify account state
- require explicit operator review before resuming

## Standard Response Pattern

## Step 1 — Detect

Detection may come from:

- automated health checks
- stream-freshness monitors
- exchange error codes
- reconciliation checks
- restart logic
- operator observation
- security alerts

## Step 2 — Classify

The incident must be assigned:

- an incident class
- a severity level
- and an exposure-risk flag if applicable

## Step 3 — Contain

Containment may include:

- entering safe mode
- blocking new entries
- stopping strategy actions
- canceling stale orders
- restoring protection
- or flattening if necessary

## Step 4 — Verify state

The bot must verify exchange truth using the appropriate sources, including where needed:

- user-stream state
- current position state
- open normal orders
- open algo orders
- local persisted state

## Step 5 — Recover or escalate

If the problem can be resolved safely:
- repair state
- log the repair
- and only then resume

If the problem cannot be resolved safely:
- remain blocked
- escalate visibly
- require operator decision or intervention

## Step 6 — Document

Every incident must be logged with enough detail to reconstruct:

- what happened
- what was known
- what the bot did
- and how the incident ended

## Step 7 — Review afterward

Severity 3 and 4 incidents require post-incident review.

## Safe-Mode Triggers

The bot must enter safe mode automatically when any of the following occurs:

- user stream is stale while a position exists
- open position exists without confirmed protective stop
- execution status of a critical action is unknown and cannot be confirmed immediately
- reconciliation mismatch remains unresolved
- restart recovery fails
- repeated authorization failures affect required trading or recovery actions
- local and exchange position materially disagree
- suspected credential compromise is detected
- kill switch is triggered

The bot may also enter safe mode for lower-severity conditions if configured conservatively.

## Operator Responsibilities

## Bot responsibilities

The bot should automatically:

- detect and classify incidents where possible
- enter safe mode when rules require it
- preserve logs and state summaries
- reconcile or attempt safe repair where appropriate
- block new exposure during uncertainty
- raise visible alerts

## Operator responsibilities

The operator is responsible for reviewing and deciding when incidents involve:

- suspected key compromise
- emergency exposure-risk conditions
- unresolved position mismatch
- repeated restart failure
- flatten-versus-preserve decisions in ambiguous situations
- approval to resume after severity 4 incidents
- approval to resume after severe repeated incidents

## Mandatory operator escalation

Operator escalation is mandatory for:

- Severity 4 incidents
- any position without confirmed protection
- suspected credential exposure
- repeated unresolved severity 3 incidents
- emergency flattening
- any incident where automated recovery cannot restore state certainty

## Logging Requirements

Every incident record should include at minimum:

- incident ID or unique reference
- incident class
- severity level
- detection timestamp
- symbol
- local state summary
- exchange state summary where applicable
- whether a position existed
- whether a protective stop was confirmed
- actions taken automatically
- actions taken by operator
- current system mode
- resolution status
- resume timestamp if resumed
- whether postmortem is required

## Resolution States

Each incident should end in one of the following states:

- `RESOLVED_AUTOMATICALLY`
- `RESOLVED_WITH_OPERATOR_ACTION`
- `CONTAINED_AWAITING_REVIEW`
- `UNRESOLVED_BLOCKED`
- `ESCALATED_EMERGENCY`

These resolution states should be visible in logs and summaries.

## Post-Incident Review Policy

## Required review threshold

A post-incident review is required for:

- all Severity 3 incidents
- all Severity 4 incidents

## Recommended review contents

Each review should capture:

- incident summary
- root cause or best-known cause
- state impact
- exposure impact
- actions taken
- what worked
- what failed
- whether procedures were followed
- what should change in code, docs, alerts, or operations

## Goal of post-incident review

The goal is not blame.

The goal is:
- learning,
- procedure improvement,
- and stronger future containment.

## Operational Restrictions for V1

The incident-response model assumes the following restrictions remain active in v1:

- BTCUSDT only
- one strategy only
- one-way mode only
- isolated margin only
- one position maximum
- one protective stop maximum
- operator-supervised deployment
- no autonomous multi-symbol incident choreography

These restrictions simplify containment and recovery.

## Examples of Expected Responses

## Example 1 — User stream stale while flat
- classify as Severity 2
- pause new entries if stream confidence drops below acceptable threshold
- restore stream
- verify state
- resume if clean

## Example 2 — User stream stale while position exists
- classify as Severity 3
- enter safe mode
- verify position and stop state through exchange queries
- restore stream
- resume only after reconciliation

## Example 3 — Position exists without confirmed stop
- classify as Severity 4
- enter safe mode
- raise urgent alert
- restore stop if possible
- flatten if protection cannot be restored safely
- do not resume without review

## Example 4 — Order returned unknown execution outcome
- classify as Severity 3 or 4 depending on exposure ambiguity
- do not retry blindly
- query exchange state
- inspect position and orders
- resolve state before continuing

## Example 5 — Suspected key exposure
- classify as Severity 4
- halt or safe-mode the bot
- revoke/rotate keys
- verify account and order state
- require operator review before resuming

## Decisions

The following decisions are accepted for incident response:

- incident handling is severity-based
- containment comes before strategy continuation
- safe mode is mandatory for state-uncertain incidents
- user-stream failure, missing stop protection, and execution-unknown states are explicit incident classes
- operator escalation is mandatory for emergency exposure-risk incidents
- every incident must leave an audit trail
- severity 3 and 4 incidents require post-incident review
- the bot must block new exposure during unresolved state uncertainty
- emergency exposure-risk incidents require explicit review before resuming normal operation

## Open Questions

The following remain open:

1. What exact thresholds should define market-data staleness and user-stream staleness?
2. What exact time window should separate a recoverable unknown execution state from an emergency one?
3. Under which conditions should the bot flatten automatically versus wait for operator confirmation?
4. What exact alert-routing channels should be used for severity 3 versus severity 4 incidents?
5. Should repeated severity 2 incidents within a short period automatically escalate to severity 3?
6. What exact postmortem template should be standardized for severity 3 and 4 incidents?

## Next Steps

After this document, the next recommended files are:

1. `docs/09-operations/operator-workflow.md`
2. `docs/10-security/secrets-management.md`
3. `docs/09-operations/daily-weekly-review-process.md`

## References

Binance references:

- Binance USDⓈ-M Futures General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info

- Binance USDⓈ-M Futures Error Code  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/error-code

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance Derivatives Change Log  
  https://developers.binance.com/docs/derivatives/change-log

Related internal project documents:

- `docs/09-operations/restart-procedure.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/10-security/api-key-policy.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`