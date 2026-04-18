# Kill Switches

## Purpose

This document defines the kill-switch policy for the v1 Prometheus trading system.

Its purpose is to define the hard halt controls used when the system is no longer trusted to continue normal strategy operation.

A pause means:

> Stop opening new positions for now.

A kill switch means:

> The system is not trusted to continue normal strategy operation until reviewed, reconciled, and explicitly cleared.

The kill-switch policy exists to protect:

- capital,
- exchange-state certainty,
- stop-protection integrity,
- operator control,
- and recovery discipline.

This document replaces the previous TBD placeholder for:

```text
docs/07-risk/kill-switches.md
```

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- v1 live scope: one symbol
- v1 live position limit: one position
- position mode: one-way mode
- margin mode: isolated margin
- exchange-side protective stop is mandatory
- deployment model: supervised staged rollout
- runtime begins in safe mode on restart
- exchange state is authoritative
- incidents are severity-classified

This document covers:

- kill-switch definition,
- pause versus kill switch distinction,
- kill-switch types,
- activation triggers,
- automatic and operator activation,
- effects on runtime behavior,
- allowed actions while active,
- protected and unprotected position handling,
- persistence requirements,
- clearance requirements,
- observability requirements,
- event expectations,
- testing requirements,
- and implementation boundaries.

This document does **not** define:

- daily loss thresholds,
- drawdown thresholds,
- full rollback procedure,
- full stop-loss policy,
- final dashboard visual design,
- final infrastructure controls,
- or exact numeric auto-trigger thresholds.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/release-process.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`
- `docs/10-security/permission-scoping.md`
- `docs/11-interface/operator-dashboard-requirements.md`

### Authority hierarchy

If this document conflicts with incident response on severity handling, incident response wins.

If this document conflicts with the state model on runtime modes and flags, the state model wins.

If this document conflicts with restart procedure on startup/reconciliation behavior, restart procedure wins.

If this document conflicts with security policy on suspected credential compromise, security policy wins.

---

## Core Principles

## 1. Kill switch is a trust-boundary control

A kill switch is activated when the system should not continue normal strategy operation because trust has been reduced or lost.

This may be due to:

- exposure uncertainty,
- protection uncertainty,
- repeated operational failure,
- unknown execution outcome,
- security concern,
- operator judgment,
- or emergency halt requirement.

## 2. Kill switch is stronger than pause

A pause blocks new entries.

A kill switch blocks normal strategy progression and requires explicit review before resumption.

## 3. Kill switch must block new exposure

When kill switch is active:

```text
new entries are always blocked
```

No strategy signal may create new live exposure while kill switch is active.

## 4. Kill switch does not block safety actions

The kill switch must not prevent the system from protecting capital.

While active, controlled safety actions may still be allowed, including:

- exchange state reads,
- reconciliation,
- stop restoration,
- risk-reducing stop repair,
- stale order cancellation,
- emergency flattening,
- logging,
- and operator review workflow.

## 5. Kill switch must persist across restart

Kill-switch state is restart-critical.

If the process restarts while kill switch is active, it must remain active after restart.

## 6. Kill switch must never auto-clear

A kill switch may not be silently or automatically cleared.

Clearing requires explicit operator action and required safety conditions.

## 7. Kill switch prioritizes containment over optimization

When kill switch is active, the system should stop trying to optimize trade outcome.

It should preserve or reduce risk, restore certainty, and support controlled recovery.

---

## Pause Versus Kill Switch

## Pause

A pause is a normal operational control.

Use a pause when:

- the operator wants to stop new entries temporarily,
- supervision will be unavailable,
- conditions look questionable,
- a minor investigation is needed,
- or the operator wants a low-severity halt without declaring system distrust.

Effects:

```text
new entries blocked
existing protected position may continue normal management if policy permits
pause can be cleared when other gates are clean
```

## Kill Switch

A kill switch is a hard trust-control.

Use a kill switch when:

- runtime state is not trusted,
- exposure safety is uncertain,
- serious incident occurred,
- repeated abnormal behavior appears,
- protective stop integrity is uncertain,
- credential/security concern exists,
- operator wants emergency halt.

Effects:

```text
new entries blocked
normal strategy progression blocked
operator review required
runtime remains safe/blocked until cleared
reconciliation required before normal resumption
```

## Practical distinction

| Control | Blocks new entries | Blocks normal strategy progression | Requires operator review | Persists across restart |
|---|---:|---:|---:|---:|
| Pause | Yes | Usually no | Sometimes | Yes |
| Kill switch | Yes | Yes | Yes | Yes |

---

## Kill-Switch Types

The system should distinguish three kill-switch types.

## 1. Operator Kill Switch

Activated manually by the operator.

Examples:

- operator no longer trusts runtime state,
- operator observes abnormal behavior,
- operator cannot supervise,
- operator wants emergency hard halt,
- operator wants to stop live operation pending review.

## 2. Automatic Safety Kill Switch

Activated automatically by system policy.

Examples:

- position exists without confirmed protective stop,
- local/exchange position materially disagree,
- repeated unsafe reconciliation mismatches,
- repeated unknown execution statuses,
- repeated stop replacement failures,
- repeated restart recovery failures,
- critical stream failure while exposed,
- emergency flattening path was triggered.

## 3. Security Kill Switch

Activated by security-relevant conditions.

Examples:

- suspected API key exposure,
- suspected host compromise,
- permission anomaly,
- IP restriction failure,
- repeated unexpected authorization errors,
- unrecognized live trading action,
- evidence of credential misuse.

Security kill switches require both operational review and security review before clearance.

---

## Kill-Switch Runtime Effects

When a kill switch activates, the runtime should set or preserve:

```text
kill_switch_active = true
entries_blocked = true
operator_review_required = true
```

The runtime mode should move to one of:

```text
SAFE_MODE
BLOCKED_AWAITING_OPERATOR
```

or remain in a more severe emergency/recovery mode if already there.

## Required immediate effects

On activation:

- block all new entries,
- block strategy-generated live order creation,
- block normal strategy progression,
- block automatic transition to `RUNNING_HEALTHY`,
- raise operator-visible alert,
- persist kill-switch state,
- emit kill-switch activation event,
- record activation reason/source,
- preserve or trigger incident state where appropriate.

## Actions blocked while active

Kill switch blocks:

- new market entry orders,
- new live exposure,
- same-direction scale-in,
- reversal entry,
- strategy-driven entry evaluation that can lead to live orders,
- discretionary stop widening,
- automatic risk increase,
- automatic leverage increase,
- automatic return to running healthy,
- parameter changes intended to bypass the halt.

## Actions allowed while active

Kill switch may allow controlled safety actions:

- exchange position reads,
- open order reads,
- open algo order reads,
- reconciliation,
- user-stream recovery,
- market-data recovery,
- cancellation of stale/unexpected orders when safe,
- submission of replacement protective stop when deterministic,
- risk-reducing stop update or repair,
- emergency flattening,
- incident logging,
- operator action recording,
- dashboard status reads,
- kill-switch clearance request workflow.

---

## Strategy Behavior While Kill Switch Is Active

## Normal strategy progression

Normal strategy progression is blocked.

This includes:

- generating new live entries,
- advancing toward new exposure,
- allowing a fresh breakout signal to place an order,
- optimizing open trade outcome as if runtime is healthy.

## Existing protected position

If a protected position exists, kill switch does not mean the bot should ignore it.

The system may still:

- preserve confirmed protective stop,
- repair protection if needed,
- reduce risk if deterministic,
- exit/flatten if safety policy requires,
- reconcile state.

## Trailing behavior

Normal strategy-managed trailing is suspended while kill switch is active unless the action is clearly risk-reducing and safety-approved.

Policy:

```text
Kill switch blocks normal strategy progression.
Existing protected positions may still receive safety-preserving or risk-reducing management actions.
Profit-optimizing behavior is suspended unless explicitly treated as risk-reducing safety action.
```

## Stop widening

Stop widening is never allowed because kill switch is active.

A kill switch is a containment control, not permission to increase risk.

---

## Kill Switch With No Open Position

If kill switch activates while flat:

Required behavior:

- block new entries,
- cancel stale strategy-owned entry orders if safe,
- reconcile exchange state,
- surface reason to operator,
- remain blocked until operator clearance.

No flattening is needed because no exposure exists.

If unexpected open orders exist while flat:

- block entries,
- classify orders,
- cancel if deterministic and strategy-owned,
- require operator review if ambiguous.

---

## Kill Switch With Protected Open Position

If kill switch activates while a position exists and a valid protective stop is confirmed:

Required behavior:

- block new entries,
- keep protective stop active,
- preserve or improve protection only,
- suspend profit-optimizing normal strategy progression,
- allow controlled flatten if operator/emergency policy requires,
- maintain high operator visibility,
- require reconciliation and review before resumption.

Allowed actions:

- confirm protective stop still exists,
- repair stop if needed,
- move stop only in risk-reducing direction if policy-approved,
- flatten exposure if operator or emergency logic requires.

Forbidden actions:

- add to position,
- reverse position,
- widen stop,
- disable stop,
- clear kill switch automatically,
- resume normal trailing as if healthy.

---

## Kill Switch With Unprotected Position

If kill switch activates while a position exists and protective stop is not confirmed:

```text
emergency exposure-risk condition
```

Required behavior:

- block all new entries,
- raise critical alert,
- enter or remain in emergency branch,
- attempt deterministic protection restore if conditions are met,
- flatten if protection cannot be restored with high confidence,
- require operator review before resumption.

This case should generally be treated as a severity-4 incident.

## Deterministic restore conditions

A restore-protection attempt may be allowed if:

- position side is known,
- position size is known or `closePosition=true` safely applies,
- intended stop price is known,
- no conflicting open orders exist,
- exchange connectivity is usable,
- protective stop submission path is available,
- confirmation can be checked.

If those are not true, the system should flatten or block awaiting operator according to emergency policy.

---

## Activation Triggers

## Manual activation triggers

The operator may activate kill switch when:

- runtime behavior is not trusted,
- exchange state looks uncertain,
- protective stop state is uncertain,
- repeated warnings are occurring,
- supervision cannot continue,
- abnormal execution behavior is observed,
- deployment/release appears unsafe,
- security concern exists,
- emergency halt is desired.

## Immediate automatic triggers

The system should automatically activate kill switch or enter equivalent emergency block when:

- position exists without confirmed protective stop,
- position/protection state is materially uncertain,
- local and exchange position materially disagree,
- critical order status is unknown and cannot be resolved quickly,
- repeated unsafe reconciliation mismatch occurs,
- emergency flattening path is triggered,
- suspected credential exposure occurs,
- suspected unauthorized activity occurs.

## Threshold-based automatic triggers

The system may activate kill switch after configured thresholds for:

- repeated user-stream stale events,
- repeated market-data stale events affecting management,
- repeated stop placement anomalies,
- repeated stop update failures,
- repeated restart recovery failures,
- repeated rate-limit or IP-ban risk,
- repeated authorization failures,
- repeated unknown execution statuses,
- repeated operator pauses for the same safety concern.

Exact thresholds should be defined in config or phase-gate documents.

## Security triggers

Security-related kill switches should activate on:

- API key appears in logs/docs/screenshots/chats,
- suspected host compromise,
- production key copied outside production boundary,
- IP restriction failure,
- withdrawal permission discovered on bot key,
- unrecognized trading action,
- repeated authentication anomalies.

Security kill switches should require security review before clearing.

---

## Clearance Policy

## Core rule

Kill switch must never auto-clear.

## Required clearance conditions

Before kill switch can be cleared:

- operator explicitly requests clearance,
- reason/note is recorded,
- kill-switch cause is understood,
- no unprotected exposure exists,
- reconciliation is clean or safely resolved,
- no active severity-3/4 blocking incident remains,
- no unresolved security concern remains,
- no unknown execution status remains,
- protective stop is confirmed if position exists,
- runtime state is visible to operator,
- required logs/events are preserved.

## Clearance blocked if

Clearance must be blocked if:

- position exists without confirmed protection,
- reconciliation is required/in progress/unsafe,
- active severe incident remains,
- security review is required but not completed,
- kill-switch cause is unknown,
- exchange state cannot be queried,
- operator review note is missing where required,
- kill switch was activated by security trigger and security clearance is absent.

## After clearance

Clearing kill switch does not automatically mean:

```text
RUNNING_HEALTHY
```

After clearance:

```text
remain or enter SAFE_MODE
run required reconciliation/readiness checks
confirm all gates clean
then allow transition to RUNNING_HEALTHY if policy permits
```

---

## Persistence Requirements

Kill-switch state is restart-critical.

Minimum persisted fields:

```text
kill_switch_active
kill_switch_type
kill_switch_reason
kill_switch_source
activated_at_utc_ms
activated_by
activation_event_id
related_incident_id
related_reconciliation_id
operator_review_required
entries_blocked
cleared_at_utc_ms
cleared_by
clear_reason
clearance_event_id
security_review_required
security_review_completed
updated_at_utc_ms
```

## Startup behavior

On restart, if persisted `kill_switch_active` is true:

- restore kill switch as active,
- remain in safe/blocked mode,
- show operator-visible status,
- require reconciliation,
- do not clear automatically.

## Persistence timing

Durably write kill-switch state when:

- activation requested,
- activation confirmed,
- activation fails,
- clearance requested,
- clearance blocked,
- clearance accepted,
- clearance rejected,
- restart restores active kill switch.

---

## Event Contract Expectations

Recommended events:

```text
kill_switch.activation_requested
kill_switch.activated
kill_switch.activation_failed
kill_switch.clearance_requested
kill_switch.clearance_blocked
kill_switch.clearance_rejected
kill_switch.cleared
kill_switch.state_persisted
kill_switch.restart_restored_active
```

## Activation event payload

Minimum payload:

```text
kill_switch_type
source
reason
operator_identity_or_system_source
runtime_mode
position_present
protection_confirmed
incident_id if relevant
reconciliation_state
occurred_at_utc_ms
```

## Clearance event payload

Minimum payload:

```text
requested_by
clear_reason
clearance_result
blocked_reasons if any
runtime_mode
reconciliation_state
protection_state
operator_review_required
occurred_at_utc_ms
```

## Redaction

Kill-switch events must not include secrets, raw credentials, signatures, or sensitive config dumps.

---

## Operator Visibility Requirements

The operator dashboard must show kill-switch state prominently.

Required fields:

```text
kill_switch_active
kill_switch_type
activation_source
activation_reason
activated_at_utc_ms
related_incident_id
operator_review_required
entries_blocked
current_allowed_actions
clearance_available yes/no
clearance_blocked_reason
security_review_required yes/no
reconciliation_state
protection_state
```

## Required controls

Dashboard should support:

- activate kill switch,
- request clearance,
- show blocked clearance reasons,
- record operator reason/note.

## Confirmation requirements

Activating kill switch should require explicit confirmation unless triggered automatically by emergency logic.

Clearing kill switch must require explicit confirmation.

## Visual priority

Kill-switch active state must be top-level and hard to miss.

It should not be buried in logs or secondary panels.

---

## Interaction With Incidents

Kill switch and incident state are related but distinct.

## Kill switch may open incident

A kill switch activation may open or update an incident if the cause is incident-worthy.

Examples:

- unprotected position,
- unknown execution state,
- credential concern,
- repeated unsafe mismatch.

## Incident may activate kill switch

A severity-4 incident should usually activate kill switch or equivalent hard block.

## Clearing incident does not clear kill switch

Incident resolution and kill-switch clearance are separate actions.

A kill switch remains active until explicitly cleared.

## Clearing kill switch does not erase incident

Incident records must remain for audit and review.

---

## Interaction With Restart

Restart does not clear kill switch.

On restart:

1. runtime enters safe mode,
2. persisted kill-switch state is loaded,
3. if active, kill switch remains active,
4. entries remain blocked,
5. reconciliation runs,
6. operator review remains required,
7. normal operation resumes only after explicit clearance and clean gates.

If restart occurs during kill-switch activation or clearance workflow:

- restore most conservative state,
- keep kill switch active if uncertain,
- require operator review.

---

## Interaction With Rollback and Release

Kill switch may trigger rollback review.

Examples:

- new release creates execution inconsistency,
- observability fails during live operation,
- state model behaves unexpectedly,
- stop placement fails after deployment,
- repeated incidents begin after release.

Release rollback should not automatically clear kill switch.

Rollback and kill-switch clearance are separate controlled actions.

---

## Interaction With Security

Security kill switch is a special class.

## Security kill-switch triggers

- suspected credential exposure,
- production secret appears in logs/docs/chats/screenshots,
- unauthorized exchange activity,
- IP restriction failure,
- withdrawal permission discovered,
- host compromise suspicion,
- repeated unexplained authorization failures.

## Required response

Security kill switch requires:

- halt normal strategy operation,
- block new entries,
- verify account state,
- preserve protection if exposure exists,
- rotate/revoke credentials where appropriate,
- review permissions,
- require security review before clearance.

## Security clearance

Security kill switch cannot be cleared by ordinary operational readiness alone.

It requires security cause resolution.

---

## Configuration Requirements

Recommended configuration fields:

```yaml
kill_switch:
  enabled: true
  auto_activate_on_unprotected_position: true
  auto_activate_on_unsafe_mismatch: true
  auto_activate_on_suspected_credential_exposure: true
  auto_activate_on_unknown_execution_status: true
  auto_activate_on_emergency_flatten: true
  require_operator_clearance: true
  require_reconciliation_before_clearance: true
  require_security_review_for_security_trigger: true
  suspend_normal_trailing_while_active: true
  allow_risk_reducing_stop_actions_while_active: true
  allow_emergency_flatten_while_active: true
```

Defaults must be conservative.

---

## Implementation Boundaries

## Safety/incident layer owns

- kill-switch activation,
- kill-switch clearance gates,
- incident interaction,
- operator review requirement,
- entries blocked state.

## Persistence layer owns

- durable kill-switch state,
- action records,
- restart continuity.

## Operator control layer owns

- operator activation request,
- operator clearance request,
- reason/note capture,
- dashboard exposure of state.

## Execution layer owns

- controlled safety actions while kill switch is active,
- order cancellation,
- stop restoration,
- emergency flatten execution when approved.

## Strategy layer does not own

- kill-switch clearance,
- kill-switch override,
- decision to trade while kill switch active.

## Exchange adapter does not own

- kill-switch policy,
- kill-switch clearance,
- incident classification.

---

## Testing Requirements

Implementation must include tests for the following.

## Activation tests

- operator activation sets kill switch active,
- automatic unprotected-position trigger activates kill switch,
- security trigger activates security kill switch,
- activation persists state,
- activation blocks entries.

## Runtime behavior tests

- new entry rejected while kill switch active,
- strategy progression blocked,
- safety reads still allowed,
- reconciliation still allowed,
- stop restoration allowed if deterministic,
- emergency flatten allowed if policy permits.

## Position state tests

- flat + kill switch blocks entries,
- protected position + kill switch preserves/repairs protection,
- unprotected position + kill switch enters emergency path,
- trailing/profit optimization suspended while active,
- risk-reducing stop action allowed where policy permits.

## Clearance tests

- kill switch does not auto-clear,
- restart does not clear kill switch,
- clearance blocked when reconciliation required,
- clearance blocked when position unprotected,
- clearance blocked when severe incident active,
- security kill switch requires security review,
- successful clearance persists state,
- cleared kill switch does not automatically enter running healthy.

## Operator tests

- activation reason recorded,
- clearance reason recorded,
- dashboard state includes blocked reasons,
- operator review required flag set,
- active kill switch visible in status read model.

## Boundary tests

- strategy cannot clear kill switch,
- exchange adapter cannot clear kill switch,
- dashboard cannot bypass clearance gates,
- config cannot silently disable active kill switch.

---

## V1 Non-Goals

The kill-switch policy does not include:

- autonomous strategy replacement after kill switch,
- automatic return to live trading after timer expires,
- profit-maximizing trade management while halted,
- manual discretionary trading terminal controls,
- multi-symbol portfolio kill-switch hierarchy,
- exchange-account-wide liquidation logic,
- cloud infrastructure failover controls,
- direct hardware power controls,
- bypass mode for “small trades.”

These may be considered later but are not v1 behavior.

---

## Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact automatic trigger thresholds

This document defines trigger classes.

Exact repeated-event thresholds should be configured and validated later.

## 2. Emergency flatten automation

Incident policy should define when flattening is automatic versus blocked awaiting operator.

## 3. Security review workflow

Security-triggered kill-switch clearance should be connected to future security runbooks.

## 4. Release rollback integration

Rollback procedure should define how kill switch interacts with version rollback.

## 5. Dashboard visual priority

Interface supplement docs should define exact UI presentation.

---

## Acceptance Criteria

This kill-switch policy is satisfied when implementation can demonstrate:

- kill switch is distinct from pause,
- kill switch blocks all new entries,
- kill switch blocks normal strategy progression,
- kill switch suspends normal trailing/profit optimization,
- deterministic risk-reducing safety actions remain allowed,
- protected positions remain protected,
- unprotected positions enter emergency path,
- operator activation works,
- automatic safety activation works,
- security activation works,
- active kill switch persists across restart,
- kill switch never auto-clears,
- clearance requires operator action,
- clearance is blocked under unsafe conditions,
- security kill switch requires security review,
- dashboard exposes active state and blocked-clearance reason,
- activation and clearance are logged,
- and strategy/exchange modules cannot bypass kill-switch policy.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Risk hard-halt control policy
