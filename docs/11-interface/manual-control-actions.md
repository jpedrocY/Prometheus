# Manual Control Actions

## Purpose

This document defines the manual control actions allowed in the v1 Prometheus operator interface.

Its purpose is to make clear:

- what the operator may do from the dashboard or control surface,
- what actions are intentionally forbidden,
- which actions require confirmation,
- which actions require stronger approval,
- which runtime states disable specific controls,
- what backend commands each control should produce,
- what must be audited,
- and how manual controls preserve Prometheus as a safety-first, operator-supervised system rather than a discretionary trading terminal.

Prometheus is designed to run on a dedicated local NUC / mini PC with an attached monitor showing an always-available operator dashboard during operation.

That dashboard may be polished, information-rich, and visually similar in density to a professional exchange dashboard. It may show positions, open orders, protective stops, charts, setup/trade visualizations, risk state, alerts, and operational metrics.

However:

```text
The dashboard is a supervision and safety-control surface.
It is not a discretionary manual trading terminal.
```

## Scope

This document applies to the v1 Prometheus system under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- one-way position mode,
- isolated margin mode,
- one active strategy,
- one live symbol first,
- one open position maximum,
- one active protective stop maximum,
- no pyramiding in v1,
- no reversal entry while positioned in v1,
- exchange-side protective stop is mandatory,
- user stream is the primary live private-state source,
- REST is used for placement, cancellation, reconciliation, and recovery,
- restart begins in safe mode,
- exchange state is authoritative,
- the operator dashboard is always available on the dedicated NUC monitor during operation where practical,
- v1 is supervised, not lights-out autonomous.

This document covers:

- manual-control philosophy,
- allowed controls,
- restricted controls,
- forbidden controls,
- confirmation requirements,
- disabled-state requirements,
- backend command mapping,
- audit requirements,
- emergency flatten behavior,
- protection restoration workflow,
- reconciliation request workflow,
- pause and kill-switch controls,
- risk/deployment control boundaries,
- chart/trade visualization boundary,
- setup/runbook topics,
- testing requirements,
- and acceptance criteria.

This document does **not** define:

- final dashboard visual design,
- complete dashboard metrics catalog,
- alert UI layout,
- authentication implementation,
- exact frontend framework,
- exact API routes,
- exact command payload schemas,
- exact Binance endpoint implementation,
- or the first-run setup procedure.

Those are covered by related documents or later setup/runbook work.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/event-flows.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/rollback-procedure.md`
- `docs/10-security/audit-logging.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/approval-workflows.md`
- `docs/11-interface/dashboard-metrics.md`
- `docs/11-interface/alerting-ui.md`
- `docs/07-risk/kill-switches.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`

### Authority hierarchy

If this document conflicts with the kill-switch policy, the kill-switch policy wins for kill-switch activation and clearance behavior.

If this document conflicts with incident response, incident response wins for emergency classification and containment.

If this document conflicts with stop-loss policy, stop-loss policy wins for protective stop requirements.

If this document conflicts with approval-workflows after that document is created, approval-workflows wins for detailed approval sequencing.

If this document conflicts with security/audit policy, security/audit policy wins for logging, redaction, and credential handling.

---

## Core Principles

## 1. Manual controls exist for safety and supervision

Manual controls should help the operator:

- pause the system,
- activate kill switch,
- approve or deny recovery,
- request reconciliation,
- acknowledge alerts,
- add notes,
- request controlled restart,
- restore protection where policy allows,
- clean up stale orders where policy allows,
- emergency-flatten exposure where needed,
- and verify operating state.

Manual controls should not let the operator casually trade around the strategy.

## 2. The dashboard may display rich trading information

The operator dashboard may show:

- candle charts,
- setup ranges,
- entry/exit markers,
- protective stop markers,
- stop updates,
- open orders,
- algo/protective stop orders,
- PnL,
- R-multiple,
- risk state,
- drawdown,
- daily loss,
- trade history,
- and rule-check diagnostics.

This is allowed and desirable.

The boundary is:

```text
Display and review are allowed.
Unrestricted manual trading from the dashboard is not allowed in v1.
```

## 3. Controls must map to backend commands

A dashboard button must not directly manipulate database rows, exchange state, runtime flags, or order endpoints.

Each control must produce an internal backend command that is:

- validated,
- permission-checked,
- state-checked,
- audited,
- and processed by the owning backend component.

## 4. Controls must be disabled when unsafe

A control that is unsafe in the current state must not remain casually clickable.

The interface should disable, hide, or require escalation for controls when:

- runtime state is unknown,
- exposure is uncertain,
- reconciliation is required,
- user stream is stale,
- kill switch is active,
- incident is unresolved,
- operator approval is missing,
- a conflicting command is already in flight,
- or the action would increase risk.

## 5. Confirmation must match consequence

Not all manual actions require the same confirmation.

Acknowledge alert is low consequence.

Emergency flatten is high consequence.

Clear kill switch is high consequence.

Increase risk is high consequence.

The UI and backend must reflect this difference.

## 6. Manual controls must be auditable

Any manual action that changes:

- runtime state,
- trading permission,
- recovery state,
- incident state,
- risk posture,
- deployment state,
- exchange orders,
- position state,
- protective stop state,
- or emergency handling

must leave a durable audit record.

## 7. Manual actions must not clear truth requirements

A manual action cannot make unknown exchange state known.

The operator may request reconciliation, approve recovery after reconciliation, or trigger emergency containment.

The operator may not simply declare an unknown position safe.

## 8. Emergency actions prioritize containment

When emergency controls are used, the goal is not strategy optimization.

The goal is to:

- reduce or contain exposure risk,
- preserve or restore protection,
- flatten if required,
- stop new entries,
- and support later review.

---

## Dashboard Display vs Manual Control

The dashboard has two distinct roles.

## Display role

The dashboard should display information continuously on the dedicated NUC monitor.

Display panels may include:

- runtime status,
- open position,
- open normal orders,
- open algo/protective stop orders,
- entry order status,
- exit order status,
- emergency flatten status,
- protective stop status,
- user-stream health,
- market-data health,
- reconciliation state,
- incidents,
- alerts,
- daily loss state,
- drawdown state,
- release/config versions,
- logs/events,
- strategy signal state,
- completed-bar state,
- and trade/setup chart visualizations.

Display information can be rich and visually polished.

## Control role

The dashboard may expose a limited set of manual controls.

Controls must be safety-scoped and backend-validated.

Examples:

- pause,
- kill switch,
- request reconciliation,
- approve recovery,
- emergency flatten,
- acknowledge alert,
- add operator note.

## Chart/trade visualization

A future dashboard may include a TradingView-like candle chart for each setup or trade.

Allowed chart features:

- completed candles,
- setup window highlight,
- setup high/low,
- breakout bar marker,
- higher-timeframe bias annotation,
- entry marker,
- entry price line,
- initial stop line,
- current protective stop line,
- stop update markers,
- exit marker,
- PnL/R-multiple label,
- rule-pass/rule-fail annotations,
- trade lifecycle state overlay.

Purpose:

```text
Visual verification that the bot followed its written rules.
```

Forbidden chart behavior in v1:

- click-to-buy,
- click-to-sell,
- drag stop to widen risk,
- drag order to discretionary price,
- manual chart trading,
- one-click reversal,
- one-click pyramiding,
- manual strategy override to force entry.

Chart visualization should support review, not discretionary trading.

---

## Manual Action Classes

Manual controls should be grouped into clear action classes.

## Class 1 — Informational / Review Actions

Low-consequence actions that do not change trading state.

Examples:

- acknowledge informational alert,
- mark alert reviewed,
- add operator note,
- export selected logs,
- view trade details,
- view setup/trade chart,
- view reconciliation report,
- view audit record.

These actions still may be logged, but they do not directly affect trading permission or exchange state.

## Class 2 — Soft Control Actions

Actions that block or organize activity without creating exchange exposure.

Examples:

- pause new entries,
- clear operator pause,
- request reconciliation,
- request status refresh,
- request controlled restart,
- request dashboard refresh.

These may affect runtime state and must be audited when they change control flags.

## Class 3 — Recovery Actions

Actions that help restore state certainty.

Examples:

- approve recovery resumption,
- deny recovery resumption,
- request stale-order cleanup,
- request protection restoration,
- request stream reconnection/recovery,
- request config reload in safe mode.

These require stronger validation and may require operator confirmation.

## Class 4 — Emergency Actions

Actions intended to contain risk.

Examples:

- activate kill switch,
- request emergency flatten,
- confirm emergency flatten,
- disable live trading mode,
- block all new entries,
- mark operator review required.

Emergency actions must be highly visible, confirmed where needed, and audited.

## Class 5 — Governance / Risk Actions

Actions that change risk or deployment posture.

Examples:

- request daily lockout override,
- request drawdown pause clearance,
- request risk fraction increase,
- request notional cap increase,
- request leverage cap increase,
- request deployment stage promotion,
- request production trading enablement,
- request release promotion.

These should normally be handled through approval workflows, not casual dashboard buttons.

---

## Allowed Manual Actions

The following manual actions are allowed in v1 if implemented with required validation and audit behavior.

## Pause new entries

Purpose:

```text
Block new strategy entries without declaring a system-trust failure.
```

Allowed when:

- operator wants temporary halt,
- supervision will be unavailable,
- market conditions seem abnormal,
- maintenance is planned,
- alerts need investigation.

Effects:

- set `paused_by_operator = true`,
- set or derive `entries_blocked = true`,
- do not cancel existing valid protective stop,
- do not flatten automatically.

Must audit:

- operator identity,
- timestamp,
- reason,
- pre-action state,
- post-action state.

## Clear operator pause

Purpose:

```text
Remove operator pause after conditions are acceptable.
```

Allowed only when:

- no kill switch active,
- no unresolved blocking incident,
- no unresolved reconciliation requirement,
- no unknown execution outcome,
- daily/drawdown controls allow entries,
- streams and state confidence are acceptable for current stage.

Clearing pause does not automatically force `RUNNING_HEALTHY`.

It only removes one blocking condition.

## Activate kill switch

Purpose:

```text
Hard-block normal strategy progression because system trust is reduced or operator wants emergency halt.
```

Allowed at any time.

Effects:

- set `kill_switch_active = true`,
- set `entries_blocked = true`,
- set `operator_review_required = true`,
- block normal strategy progression,
- allow only safety/recovery actions.

This action should be easy to trigger but hard to miss after activation.

## Request kill-switch clearance

Purpose:

```text
Begin the process of clearing an active kill switch.
```

This should not immediately clear the kill switch.

It should produce a request that checks:

- incident state,
- reconciliation state,
- exposure/protection state,
- stream health,
- operator approval requirements,
- audit requirements.

Actual clearance requires approval workflow.

## Acknowledge alert

Purpose:

```text
Mark that the operator has seen an alert.
```

Acknowledge does not resolve the underlying condition.

The UI must distinguish:

```text
alert acknowledged
```

from:

```text
condition resolved
```

Critical alerts should remain visible while the condition persists.

## Add operator note

Purpose:

```text
Record human context for later review.
```

Examples:

- reason for pause,
- observation during incident,
- note about internet outage,
- note about Binance manual action,
- note about failed alert route.

Notes must not contain secrets.

## Request reconciliation

Purpose:

```text
Ask backend to reconcile local state with exchange state.
```

Allowed when:

- operator wants state verification,
- stream recovered,
- restart occurred,
- unknown state exists,
- manual action occurred,
- dashboard state seems stale.

This action is read/recovery-oriented and must not place new exposure.

## Request controlled restart

Purpose:

```text
Request a planned restart of the Prometheus runtime.
```

Allowed only when safe according to state.

If exposure exists, controlled restart must preserve safety:

- confirm protective stop state,
- preserve local state,
- restart into safe mode,
- reconcile before resumption.

A restart request must not bypass active incidents or kill switch.

## Approve recovery resumption

Purpose:

```text
Allow the system to leave recovery/blocked state after required checks pass.
```

Allowed only when backend reports all required recovery conditions are satisfied.

Approval must not be possible if:

- exchange state is unknown,
- protection is uncertain,
- unprotected position exists,
- kill switch clearance not complete,
- severe incident unresolved,
- credential compromise unresolved,
- daily/drawdown lockout blocks entries unless separate approved override exists.

## Deny recovery resumption

Purpose:

```text
Keep system blocked after recovery review.
```

Allowed when operator does not trust state or wants further investigation.

Must audit reason.

## Request stale-order cleanup

Purpose:

```text
Ask backend to cancel or clear orders classified as stale/unexpected where policy allows.
```

This action may cancel orders, so it must be controlled.

Allowed only when:

- order ownership and role are known,
- cancellation is risk-reducing or cleanup-oriented,
- backend validates no harmful side effect,
- reconciliation context exists.

If cancellation outcome is unknown, failure-recovery policy applies.

## Request protection restoration

Purpose:

```text
Ask backend to restore exchange-side protective stop when a position exists and restoration is deterministic.
```

Allowed only when:

- position side is known,
- position ownership is known,
- expected stop price is known and valid,
- no conflicting active stop exists or conflict is resolved,
- restoration is risk-reducing/safety-restoring,
- backend validates order fields.

If state is ambiguous, use emergency branch instead.

## Request emergency flatten

Purpose:

```text
Ask backend to flatten live exposure to contain risk.
```

This is a high-consequence action.

It must require strong confirmation unless immediate automated emergency policy triggers it.

Allowed when:

- position exists,
- protection cannot be trusted,
- operator wants to contain exposure,
- incident policy requires flatten,
- recovery cannot safely restore protection.

Emergency flatten must not be confused with discretionary exit.

## Disable live trading mode

Purpose:

```text
Disable production trade-capable behavior.
```

This may be used after incidents, before maintenance, or during demotion.

It should:

- block new entries,
- prevent new live exposure,
- preserve recovery/safety actions,
- require config/deployment review before re-enabling.

---

## Restricted Manual Actions

Restricted actions are not ordinary dashboard clicks.

They require approval workflow, stronger confirmation, and durable audit records.

## Clear kill switch

Clearing kill switch is restricted.

Requirements:

- operator intent,
- active condition reviewed,
- reconciliation acceptable,
- incidents reviewed,
- no unprotected position,
- no unknown execution outcome,
- credential state trusted,
- approval audit record.

Kill switch must never auto-clear.

## Override daily lockout

Daily lockout override is restricted and generally discouraged.

Allowed only when:

- the daily lockout is known to be due to operational/accounting classification issue, or
- documented emergency/risk-reducing action requires it.

It must not be used to keep trading after normal losses just because the operator wants more trades.

## Clear drawdown pause / hard review

Drawdown pause clearance is restricted.

Requirements:

- drawdown state reviewed,
- cause of drawdown understood,
- no unresolved abnormal execution issues,
- operator approval,
- phase-gate implications considered.

## Increase risk fraction

Increasing risk is restricted.

Requires:

- phase-gate approval,
- validation evidence,
- paper/tiny-live evidence,
- no unresolved incidents,
- config version change,
- audit record,
- release/review record.

Manual dashboard should not casually expose a slider that increases risk.

## Increase notional cap

Increasing notional cap is restricted.

Same approval standard as risk increase or stronger.

## Increase leverage cap

Increasing leverage cap is restricted.

It must require explicit review because leverage affects liquidation proximity, fees, slippage sensitivity, and operational urgency.

## Enable production trade-capable mode

Enabling production write capability is restricted.

Requirements:

- phase gate,
- host hardening,
- secrets configured,
- API permissions verified,
- IP restrictions verified or documented exception,
- alerts tested,
- dashboard visible,
- emergency access tested,
- operator approval.

## Promote deployment stage

Promotion from dry-run to paper/shadow, paper/shadow to tiny live, or tiny live to scaled live is restricted.

This should be governed by phase gates.

## Rollback with live implications

Rollback actions that affect live runtime, database schema, config, or risk posture are restricted.

Must follow rollback procedure.

---

## Forbidden Manual Actions

The following controls must not exist in v1.

## Arbitrary manual order entry

Forbidden:

- manual market buy,
- manual market sell,
- manual limit buy,
- manual limit sell,
- manual stop entry,
- manual take-profit entry,
- chart-click order placement.

Reason:

```text
Prometheus is not a discretionary manual trading terminal.
```

## Manual pyramiding

Forbidden:

- add to existing long,
- add to existing short,
- average into a losing position,
- scale into a winning position manually.

V1 has no pyramiding.

## Manual reversal

Forbidden:

- manually reverse from long to short,
- manually reverse from short to long,
- one-click flip position.

V1 has no reversal entry while positioned.

## Manual stop widening

Forbidden:

- move stop farther away from risk-approved stop,
- widen stop after entry,
- cancel stop to “give trade room,”
- drag stop on chart to increase risk.

Stops may reduce risk, not increase it.

## Bypass reconciliation

Forbidden:

- force state to clean,
- mark position protected without exchange evidence,
- declare flat while orders/stops are unknown,
- skip reconciliation after restart/recovery.

## Bypass kill switch or incident review

Forbidden:

- force `RUNNING_HEALTHY`,
- hide kill switch,
- hide incident,
- clear incident without required review,
- clear kill switch automatically.

## Casual risk changes

Forbidden:

- slider-based leverage increase,
- one-click risk increase,
- changing notional cap without approval,
- changing strategy parameters mid-trade to justify discretionary action.

## Concealment controls

Forbidden:

- delete audit events,
- hide critical alerts,
- suppress incident display,
- hide manual action history,
- overwrite recovery notes.

---

## Confirmation Requirements

Manual actions should use confirmation levels.

## Level 0 — No confirmation

Allowed for read-only actions.

Examples:

- view chart,
- view order details,
- view audit event,
- view reconciliation report.

## Level 1 — Simple confirmation

Used for low-impact actions.

Examples:

- acknowledge noncritical alert,
- add note,
- refresh status.

## Level 2 — Explicit confirmation

Used for actions that change runtime control state.

Examples:

- pause new entries,
- clear pause,
- request reconciliation,
- request controlled restart while flat,
- deny recovery.

Confirmation should show:

- action name,
- current runtime mode,
- exposure state,
- whether entries are blocked,
- expected result.

## Level 3 — High-risk confirmation

Used for actions that affect recovery, incidents, or exchange-side actions.

Examples:

- request stale-order cleanup,
- request protection restoration,
- approve recovery resumption,
- request emergency flatten,
- request kill-switch clearance.

Confirmation should show:

- position state,
- protection state,
- open orders,
- open algo orders,
- incident state,
- reconciliation state,
- risk consequences,
- irreversible aspects.

## Level 4 — Governance approval

Used for restricted risk/deployment changes.

Examples:

- increase risk,
- increase leverage cap,
- increase notional cap,
- enable production trade-capable mode,
- promote to tiny live,
- clear hard drawdown review.

These should be handled by approval workflows, not simple button confirmation.

---

## Disabled-State Requirements

The dashboard must disable or block controls when required conditions are not met.

## General disabled states

Controls should be disabled when:

- backend unavailable,
- runtime state unknown,
- database unavailable,
- operator identity unavailable where required,
- current command already in flight,
- action conflicts with active incident,
- action would violate deployment stage,
- action would violate risk/security policy.

## Entry-enabling controls disabled when

Controls that may lead to resumption of entries must be disabled when:

- kill switch active and not cleared,
- operator pause active unless clearing pause,
- incident active and blocking,
- reconciliation required,
- unknown execution outcome exists,
- position/protection state uncertain,
- user stream stale while state certainty matters,
- market data stale for strategy operation,
- daily loss lockout active,
- drawdown pause/hard review active,
- credential/security concern unresolved,
- host/dashboard/alert readiness not met for stage.

## Protection restoration disabled when

Protection restoration must be disabled when:

- no position exists,
- position side unknown,
- ownership unknown,
- stop price unknown,
- stop price invalid,
- conflicting active stop state unresolved,
- adapter/exchange capability unavailable,
- credential permission missing,
- backend cannot validate fields.

## Emergency flatten disabled only rarely

Emergency flatten should be available when exposure exists and backend can safely express the action.

It may be disabled if:

- no position exists,
- position state unknown and backend cannot determine side/quantity,
- exchange connectivity unavailable,
- credentials unavailable,
- another flatten action is already in flight.

If emergency flatten is disabled while exposure may exist, the dashboard must show what alternative emergency action is required, including manual exchange verification if needed.

---

## Backend Command Mapping

Manual controls must map to internal commands.

Recommended conceptual mappings:

| Dashboard action | Backend command |
|---|---|
| Pause new entries | `control.pause_entries` |
| Clear pause | `control.clear_pause` |
| Activate kill switch | `control.activate_kill_switch` |
| Request kill-switch clearance | `control.request_kill_switch_clearance` |
| Acknowledge alert | `operator.acknowledge_alert` |
| Add operator note | `operator.add_note` |
| Request reconciliation | `reconciliation.request_run` |
| Request controlled restart | `runtime.request_controlled_restart` |
| Approve recovery resumption | `recovery.approve_resumption` |
| Deny recovery resumption | `recovery.deny_resumption` |
| Request stale-order cleanup | `execution.request_stale_order_cleanup` |
| Request protection restoration | `execution.request_protection_restoration` |
| Request emergency flatten | `execution.request_emergency_flatten` |
| Disable live trading mode | `control.disable_live_trading` |
| Request risk increase | `approval.request_risk_increase` |
| Request deployment promotion | `approval.request_stage_promotion` |

The exact command schema belongs in implementation, but the command ownership must remain clear.

## Command ownership

- Operator interface emits control requests.
- Backend validates state and permissions.
- Execution layer owns exchange-side order actions.
- State/reconciliation layer owns truth classification.
- Incident/safety layer owns incident and emergency state.
- Risk layer owns risk-setting validation.
- Approval workflow owns restricted approvals.

Dashboard frontend must not call exchange adapter directly.

---

## Audit Requirements

Audit logs are mandatory for manual controls that affect safety or state.

## Must audit

- pause enabled,
- pause cleared,
- kill switch activated,
- kill-switch clearance requested,
- kill switch cleared,
- recovery approved,
- recovery denied,
- reconciliation requested,
- controlled restart requested,
- stale-order cleanup requested,
- protection restoration requested,
- emergency flatten requested,
- emergency flatten confirmed,
- live trading disabled,
- daily lockout override requested/approved,
- drawdown clearance requested/approved,
- risk increase requested/approved,
- leverage cap change requested/approved,
- notional cap change requested/approved,
- production trade mode enabled,
- deployment promotion,
- rollback-related manual actions,
- operator notes,
- alert acknowledgements for critical alerts.

## Required audit fields

At minimum:

- action type,
- operator identity or local operator marker,
- timestamp,
- deployment stage,
- runtime mode,
- entries blocked state,
- position state,
- protection state,
- incident state,
- pre-action state hash where practical,
- post-action state hash where practical,
- reason,
- confirmation level,
- result,
- related trade/reference/incident/reconciliation where applicable.

## Failed and denied actions

Failed, rejected, and denied manual actions should also be audited when they are safety-relevant.

Example:

```text
operator attempted to clear kill switch but reconciliation was unsafe
```

This is important review information.

## No secrets in audit records

Operator notes and action payloads must not contain:

- API secrets,
- tokens,
- passwords,
- full webhook URLs,
- full secret files,
- screenshots containing secrets.

---

## Alert and Incident Interaction

Manual controls must interact clearly with alerts and incidents.

## Alert acknowledgement

Acknowledging an alert only means:

```text
operator has seen the alert
```

It does not mean:

```text
condition is resolved
```

## Incident acknowledgement

Acknowledging an incident does not resolve it.

Incident resolution requires the incident-specific resolution path.

## Critical alert persistence

Critical alerts should remain visible until underlying condition is resolved or deliberately suppressed through approved workflow.

## Alert suppression

Casual suppression of critical alerts is forbidden.

If quieting/silencing is later implemented, it must be:

- time-bound,
- reasoned,
- audited,
- visible,
- and not allowed to hide active exposure/protection emergencies.

---

## Emergency Flatten Workflow

Emergency flatten is one of the most serious manual controls.

## Purpose

Emergency flatten exists to reduce or eliminate exposure when the system cannot safely continue managing the position.

## Not a discretionary exit

Emergency flatten must not be used as a discretionary take-profit/stop-loss override.

It exists for containment.

## Required pre-checks where possible

Before confirmation, dashboard should show:

- current position side,
- position size,
- current mark/last price reference,
- protective stop state,
- open normal orders,
- open algo orders,
- active incidents,
- exchange connectivity,
- user stream health,
- whether another flatten is already in flight.

## Confirmation

Emergency flatten should require high-risk confirmation.

The confirmation should clearly state:

```text
This may close the current live position at market.
This action is for risk containment, not strategy optimization.
```

## Backend behavior

Backend should:

1. block new entries,
2. persist command intent,
3. submit approved flatten action if exchange state is known,
4. track order outcome,
5. reconcile position after action,
6. cancel/clean stale protective stops where appropriate,
7. record incident/audit events,
8. require operator review before normal resumption.

## Unknown flatten outcome

If flatten outcome is unknown:

- do not retry blindly,
- block entries,
- reconcile,
- escalate if state cannot be classified.

---

## Protection Restoration Workflow

## Purpose

Protection restoration exists to restore exchange-side protective stop coverage when a strategy-owned position exists and stop coverage is missing or uncertain.

## Allowed only when deterministic

The backend may proceed only if:

- position exists,
- position side is known,
- position ownership is known,
- approved stop price is known,
- stop fields are valid,
- no conflicting active stop exists or conflict is classified,
- restoration is risk-reducing/safety-restoring.

## Dashboard display

The dashboard should show:

- current position,
- expected stop price,
- current protective stop state,
- reason protection is missing/uncertain,
- whether restore is automatic or operator-requested,
- risks if restore fails.

## If restoration fails

Failure to restore protection while position exists is emergency behavior.

The system should either:

- escalate to emergency flatten path,
- or block awaiting operator if exchange connectivity/permissions prevent action.

---

## Reconciliation Request Workflow

## Purpose

The operator may request reconciliation to restore confidence in state.

## Allowed contexts

- after restart,
- after stream gap,
- after manual Binance inspection/action,
- after dashboard inconsistency,
- after unknown order status,
- before clearing pause/kill switch,
- before live resumption.

## Behavior

Backend should:

1. set reconciliation in progress,
2. block new entries while reconciliation matters,
3. query exchange position state,
4. query open normal orders,
5. query open algo orders,
6. compare local state,
7. classify clean/recoverable/unsafe,
8. persist result,
9. update dashboard,
10. emit audit/runtime events.

## Operator expectation

The operator may request reconciliation.

The operator may not choose the reconciliation result.

---

## Kill-Switch and Pause Controls

## Pause

Pause is a normal operational halt.

It blocks new entries but does not automatically indicate system distrust.

Clearing pause should be allowed only when other gates are clean.

## Kill switch

Kill switch is a trust-boundary control.

It blocks normal strategy progression and requires review before clearance.

Kill switch activation should be easy.

Kill switch clearance should be deliberate.

## Dashboard display

The dashboard must display active pause and active kill switch prominently.

It should not bury these states in logs.

---

## Risk and Deployment Change Controls

Risk and deployment changes should generally be routed through approval workflows.

## Do not implement casual controls

The dashboard should not provide casual controls such as:

- risk slider,
- leverage slider,
- one-click scale to live,
- one-click enable production,
- one-click increase notional.

## Use request/approval model

For v1, the dashboard may eventually allow requests such as:

- request risk increase,
- request stage promotion,
- request production enablement.

But those requests must be governed by phase gates, approval workflow, config versioning, audit logging, and release process.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical topics should be handled later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

They are not implemented by this document.

## Dashboard/control setup

- configure local dashboard display on the NUC monitor,
- decide whether dashboard opens automatically on boot/login,
- verify dashboard does not expose secrets,
- verify dashboard shows runtime status,
- verify dashboard shows open positions/orders/stops,
- verify dashboard shows chart/setup/trade review panel when implemented,
- verify controls are disabled when backend is unavailable.

## Operator access

- configure operator login/access,
- test pause action,
- test kill-switch activation,
- test alert acknowledgement,
- test operator note,
- test reconciliation request,
- test emergency flatten in dry-run only,
- verify audit records are created.

## Alert/control integration

- verify Telegram/n8n alerts include safe links or references,
- verify critical alerts cannot be mistaken for resolved after acknowledgement,
- verify alert secrets are not exposed.

## Launch readiness

- before paper/shadow, test manual controls in simulated/fake mode,
- before tiny live, verify emergency controls, dashboard display, and audit logging,
- verify no unrestricted manual trading controls exist.

---

## Testing Requirements

Manual controls must be tested before live use.

## Unit tests

Test:

- allowed action mapping,
- forbidden action rejection,
- disabled-state logic,
- confirmation-level assignment,
- audit-event generation,
- command payload validation,
- operator note redaction.

## Integration tests

Test:

- pause blocks entries,
- clearing pause does not bypass other blocks,
- kill switch blocks normal progression,
- kill switch does not block safety actions,
- recovery approval requires clean state,
- reconciliation request produces reconciliation run,
- stale-order cleanup validates state,
- protection restoration validates deterministic state,
- emergency flatten command is persisted before exchange call,
- unknown emergency flatten outcome blocks entries and reconciles.

## Dashboard tests

Test:

- dashboard displays pause/kill switch prominently,
- disabled controls cannot be clicked,
- confirmation modals show correct state,
- open orders and stops are visible,
- emergency flatten cannot be triggered accidentally,
- chart visualization is read-only,
- no arbitrary manual trade controls are present.

## Audit tests

Test that audit records are created for:

- pause,
- clear pause,
- kill switch,
- kill-switch clearance request,
- recovery approval/denial,
- reconciliation request,
- protection restoration request,
- emergency flatten request/confirmation,
- critical alert acknowledgement,
- operator note,
- denied restricted action.

## Dry-run drills

Before tiny live, run dry-run drills for:

- pause and resume,
- kill-switch activation,
- failed kill-switch clearance,
- reconciliation request,
- protection restoration simulation,
- emergency flatten simulation,
- dashboard restart,
- alert acknowledgement,
- chart/trade review.

---

## Non-Goals

This document does not define:

- final frontend design,
- exact CSS/style system,
- charting library choice,
- final API schemas,
- user authentication implementation,
- multi-operator permission model,
- mobile app behavior,
- full alert-routing UX,
- final setup commands,
- or arbitrary manual trading tools.

It defines the safety boundary for manual controls.

---

## Acceptance Criteria

`manual-control-actions.md` is complete enough for v1 when it makes the following clear:

- the dashboard may be rich, stylish, always-visible, and information-dense,
- the dashboard may show candle charts, setup/trade visualizations, open orders, stops, PnL, and state metrics,
- chart visualization is read-only and used for rule verification,
- manual controls are safety/recovery/governance controls, not discretionary trading controls,
- arbitrary manual buy/sell and chart trading are forbidden in v1,
- pause and kill switch controls are explicitly allowed and audited,
- recovery approval, protection restoration, stale-order cleanup, and emergency flatten are controlled workflows,
- restricted actions require approval workflows,
- controls must be disabled when unsafe,
- all safety-relevant manual actions must produce backend commands and audit events,
- emergency flatten is for containment, not strategy optimization,
- operator acknowledgement does not equal condition resolution,
- setup/runbook work is deferred to the first-run checklist,
- and no interface control may bypass exchange reconciliation, incidents, kill switch, risk gates, or protective-stop requirements.
