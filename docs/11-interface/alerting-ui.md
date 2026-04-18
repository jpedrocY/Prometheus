# Alerting UI

## Purpose

This document defines the alerting user-interface requirements for v1 Prometheus.

Its purpose is to define how alerts should appear to the operator across:

- the always-on local dashboard on the dedicated NUC monitor,
- optional Telegram notifications,
- optional n8n webhook routing,
- logs/audit records,
- and review workflows.

Prometheus is a safety-first, operator-supervised trading system. Alerts exist to make safety-relevant conditions visible and actionable.

The alerting UI must help the operator answer:

```text
What is wrong?
How severe is it?
Is live exposure involved?
Is the position protected?
Is trading blocked?
What action is required?
Has the alert been acknowledged?
Has the underlying condition been resolved?
Where can I review the related incident/reconciliation/order/trade record?
```

The key distinction is:

```text
Acknowledged does not mean resolved.
Delivered does not mean handled.
Resolved does not mean cleared for trading unless the required gates pass.
```

## Scope

This document applies to the v1 Prometheus alerting interface under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- one-way position mode,
- isolated margin mode,
- one live symbol first,
- one open position maximum,
- one active protective stop maximum,
- exchange-side protective stop is mandatory,
- restart begins in safe mode,
- exchange state is authoritative,
- default tiny-live host is a dedicated local NUC / mini PC,
- the NUC monitor displays the operator dashboard during operation,
- Telegram may be used for notifications,
- n8n may be used for routing/escalation/automation around notifications,
- v1 is supervised, not lights-out autonomous.

This document covers:

- alert philosophy,
- alert severity levels,
- alert classes,
- alert lifecycle,
- dashboard alert display,
- Telegram notification behavior,
- n8n routing behavior,
- acknowledgement vs resolution,
- grouping and deduplication,
- quieting/suppression rules,
- escalation expectations,
- alert history,
- audit requirements,
- secret redaction,
- setup/runbook topics,
- and testing requirements.

This document does **not** define:

- final frontend visual design,
- exact Telegram bot implementation,
- exact n8n workflow implementation,
- exact API route schemas,
- exact authentication implementation,
- exact alert delivery provider,
- exact first-run setup commands,
- or final enterprise incident-management tooling.

Those belong in implementation or later setup/runbook documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/dashboard-metrics.md`
- `docs/11-interface/manual-control-actions.md`
- `docs/11-interface/approval-workflows.md`
- `docs/08-architecture/observability-design.md`
- `docs/08-architecture/event-flows.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/database-design.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/rollback-procedure.md`
- `docs/10-security/audit-logging.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/10-security/secrets-management.md`
- `docs/07-risk/kill-switches.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/exposure-limits.md`

### Authority hierarchy

If this document conflicts with incident response on severity classification or containment behavior, incident response wins.

If this document conflicts with audit logging on audit record requirements, audit logging wins.

If this document conflicts with dashboard-metrics on required dashboard fields, dashboard-metrics wins for the metrics catalog.

If this document conflicts with manual-control-actions on allowed operator controls, manual-control-actions wins.

If this document conflicts with secrets-management on token handling, secrets-management wins.

---

## Core Principles

## 1. Alerts are safety signals, not cosmetic notifications

Alerts should represent conditions that affect:

- exposure safety,
- protective stop certainty,
- execution certainty,
- stream/trading readiness,
- recovery state,
- incidents,
- risk lockouts,
- security state,
- operator attention,
- or phase readiness.

Do not create noisy alerts for every debug detail.

## 2. Critical alerts must be impossible to miss

Critical states such as unprotected live position, unknown execution outcome, kill switch active, credential compromise, or unsafe reconciliation mismatch must dominate the dashboard.

They should not be hidden behind charts, PnL widgets, or scroll-only logs.

## 3. Alert acknowledgement is not resolution

Acknowledging an alert means the operator has seen it.

It does not mean the condition is fixed.

The UI must preserve both concepts:

```text
acknowledged = human has seen the alert
resolved = underlying condition no longer exists or was handled according to policy
```

## 4. Delivery is not handling

A Telegram or n8n notification being delivered does not mean the operator handled the alert.

The dashboard must still show active alerts until acknowledged/resolved according to policy.

## 5. Alerts must point to required action

Every important alert should answer:

```text
What should the operator do next?
```

Examples:

- review reconciliation,
- verify protective stop,
- approve or deny recovery,
- inspect incident,
- check exchange manually,
- rotate credentials,
- stop live operation,
- run backup/restore test,
- restore alert route.

## 6. Alerts must be redacted

Alerts may be routed through Telegram or n8n. These are external systems and must not receive secrets.

Alert payloads must not contain:

- Binance API secrets,
- full API keys,
- signed requests,
- listen keys,
- Telegram bot tokens,
- n8n webhook secrets,
- full `.env` contents,
- dashboard passwords,
- private IP details beyond approved summaries,
- unredacted credential material.

## 7. Alerting must fail visibly

If Telegram/n8n delivery fails, that should itself become visible on the dashboard.

Alert-route degradation can be a readiness blocker for paper/shadow or tiny-live operation.

---

## Alert Severity Levels

Prometheus should use a small severity model.

## `INFO`

Meaning:

- Useful operational information.
- No immediate safety concern.

Examples:

- process started,
- paper/shadow session started,
- daily review period closed,
- successful backup,
- successful test alert,
- routine reconnect succeeded while flat.

Default behavior:

- show in history,
- no urgent operator interruption,
- optional Telegram/n8n depending on configuration.

## `WARNING`

Meaning:

- A degraded condition exists.
- Operator should review.
- Trading may or may not be blocked depending on state.

Examples:

- market-data degraded while flat,
- user-stream degraded while flat,
- alert route degraded in non-live mode,
- backup overdue in dry-run,
- daily loss warning threshold crossed,
- drawdown watch/caution,
- dashboard stale data warning.

Default behavior:

- show prominently in dashboard alert panel,
- optional Telegram/n8n notification,
- acknowledgement recommended,
- escalation if repeated or persistent.

## `CRITICAL`

Meaning:

- Safety, capital, state certainty, credential, or live supervision may be at risk.
- Immediate operator attention is required.

Examples:

- position exists without confirmed protection,
- unknown execution outcome,
- unsafe reconciliation mismatch,
- kill switch activated,
- suspected credential compromise,
- exchange/local position mismatch,
- user stream stale while exposed,
- emergency flatten in progress,
- alert routing failed during tiny live,
- runtime DB unavailable during live-capable mode,
- dashboard unavailable during live exposure.

Default behavior:

- top-level dashboard display,
- audible/visual dashboard emphasis where implemented,
- Telegram/n8n notification if available,
- operator action required,
- audit/runtime event,
- incident linkage where appropriate.

## `EMERGENCY`

Optional stricter level.

Meaning:

- Immediate exposure or account safety action is required or underway.

Examples:

- unprotected live position and restoration failed,
- emergency flatten required,
- suspected active credential misuse,
- account state dangerous and uncertain,
- host compromise with possible live exposure.

Default behavior:

- highest-priority dashboard state,
- persistent until contained/resolved,
- Telegram/n8n urgent notification where configured,
- incident severity 4 linkage,
- operator review required before resumption.

If implementation prefers only `CRITICAL`, emergency can be modeled as `CRITICAL` with `incident_severity=4`.

---

## Alert Classes

Alerts should be categorized so the operator can filter and understand them.

Recommended alert classes:

```text
RUNTIME
MARKET_DATA
USER_STREAM
EXCHANGE_CONNECTIVITY
ORDER_EXECUTION
POSITION
PROTECTION
RECONCILIATION
INCIDENT
RISK_DAILY_LOSS
RISK_DRAWDOWN
KILL_SWITCH
OPERATOR_ACTION
APPROVAL
SECURITY
CREDENTIAL
HOST
DATABASE
BACKUP_RESTORE
DASHBOARD
ALERT_ROUTE
RELEASE_ROLLBACK
CONFIGURATION
PHASE_GATE
```

## Class examples

| Class | Example alert |
|---|---|
| `RUNTIME` | Runtime entered safe mode after crash. |
| `MARKET_DATA` | BTCUSDT 15m completed bar stream stale. |
| `USER_STREAM` | User stream stale while position exists. |
| `ORDER_EXECUTION` | Entry order status unknown after REST timeout. |
| `PROTECTION` | Position exists but protective stop not confirmed. |
| `RECONCILIATION` | Unsafe mismatch detected. |
| `RISK_DAILY_LOSS` | Daily lockout triggered. |
| `SECURITY` | API credential validation failed. |
| `HOST` | NUC time sync degraded. |
| `ALERT_ROUTE` | Telegram delivery failed. |

---

## Alert Lifecycle

Every alert should follow a clear lifecycle.

## States

Recommended states:

```text
ACTIVE
ACKNOWLEDGED
RESOLVED
SUPPRESSED
EXPIRED
ESCALATED
```

## `ACTIVE`

The alert condition currently exists or has not yet been reviewed.

## `ACKNOWLEDGED`

The operator has seen the alert.

The condition may still exist.

## `RESOLVED`

The underlying condition has been resolved or contained according to policy.

Resolution should include reason/evidence.

## `SUPPRESSED`

The alert is intentionally quieted under a documented, time-bounded rule.

Suppression must not hide critical unresolved conditions.

## `EXPIRED`

The alert is no longer relevant because the condition expired or was replaced by a more current alert.

## `ESCALATED`

The alert has been escalated into an incident, emergency action, or higher notification path.

## Lifecycle rules

### Rule 1 — Critical alerts should not auto-resolve silently

Critical alerts should require evidence of condition resolution.

### Rule 2 — Acknowledgement does not unblock trading

An acknowledged alert cannot clear `entries_blocked` by itself.

### Rule 3 — Resolved alerts remain in history

Resolved alerts should remain reviewable.

### Rule 4 — Repeated alerts should group, not spam

If the same condition repeats, group or update count rather than flood.

### Rule 5 — Alert lifecycle events should be auditable when safety-relevant

Acknowledgement, suppression, escalation, and resolution of critical alerts should produce audit events.

---

## Required Alert Fields

Each alert should support the following semantic fields.

```text
alert_id
alert_class
alert_type
severity
status
title
message
created_at_utc_ms
updated_at_utc_ms
first_seen_at_utc_ms
last_seen_at_utc_ms
resolved_at_utc_ms
acknowledged_at_utc_ms
acknowledged_by
suppressed_until_utc_ms
suppression_reason
escalated_at_utc_ms
source_component
symbol
trade_reference
order_reference
stop_reference
incident_id
reconciliation_id
runtime_mode
deployment_stage
environment
entries_blocked
operator_action_required
recommended_action
related_dashboard_panel
related_runbook_reference
dedupe_key
occurrence_count
delivery_status
payload_redaction_status
```

Implementation may split these across tables/models, but the dashboard and alert routes should preserve the meaning.

---

## Dashboard Alert Display

The dashboard is the primary alert surface.

## Top-level alert area

The dashboard should include a top-level alert strip/banner when:

- critical or emergency alert active,
- operator action required,
- kill switch active,
- unprotected position,
- unsafe reconciliation mismatch,
- credential/security issue,
- alert route failure during live-capable mode.

This top area should be visible without scrolling.

## Alert panel

The dashboard should include an alert panel with:

- active alerts,
- severity,
- class,
- status,
- created time,
- last seen time,
- acknowledgement state,
- recommended action,
- related incident/trade/order link,
- delivery status,
- escalation state.

## Alert detail view

Selecting an alert should show:

- full message,
- timeline,
- triggering event(s),
- related runtime state,
- affected symbol/trade/order,
- related incident/reconciliation,
- recommended next action,
- acknowledgement/resolution controls where allowed,
- audit/history references.

## Visual priority

Alert display should prioritize by:

1. emergency exposure/protection state,
2. critical security/credential state,
3. critical execution/state uncertainty,
4. active kill switch/incidents,
5. daily/drawdown hard blocks,
6. warning degradations,
7. informational events.

## Persistent critical state

If critical state exists, it should remain visible even if there are newer lower-severity alerts.

---

## Telegram Notification Behavior

Telegram may be used as a notification route.

## Role

Telegram should:

- notify operator of important alerts,
- summarize state,
- tell operator whether action is required,
- direct operator to dashboard,
- report when alert route tests pass/fail.

Telegram should not be treated as the authoritative control surface for high-risk approvals in v1.

## Recommended v1 Telegram use

Allowed:

- INFO summaries if enabled,
- WARNING notifications,
- CRITICAL notifications,
- emergency notification,
- daily review reminders,
- alert route health test messages,
- approval-needed notifications that direct back to dashboard.

Avoid initially:

- approving emergency flatten directly from Telegram,
- clearing kill switch directly from Telegram,
- enabling production trading from Telegram,
- increasing risk/leverage from Telegram.

## Telegram message content

A Telegram alert message should include:

```text
Prometheus alert title
Severity
Class
Environment/stage
Symbol if relevant
Position/protection summary if relevant
Entries allowed/blocked
Recommended action
Dashboard/review instruction
Timestamp
```

Example style:

```text
CRITICAL — Protective stop not confirmed

Stage: tiny_live
Symbol: BTCUSDT
Position: LONG 0.012 BTC
Protection: UNCERTAIN
Entries: BLOCKED
Action: Open dashboard, review protection emergency, reconcile/restore/flatten according to policy.
Time: 2026-04-18T12:30:00Z
```

## Telegram redaction

Telegram messages must not include:

- full API keys,
- secrets,
- full webhook URLs,
- signed requests,
- raw credential files,
- unredacted listen keys,
- passwords,
- private SSH keys.

## Delivery tracking

The dashboard should show:

- last Telegram success,
- last Telegram failure,
- last critical Telegram test,
- whether Telegram route is degraded.

Telegram delivery failure during tiny live should itself become a warning or critical alert depending on severity.

---

## n8n Routing Behavior

n8n may be used as an alert-routing or automation layer.

## Role

n8n may:

- route alerts to Telegram or other channels,
- create incident tickets/records where configured,
- send repeated reminders,
- escalate if critical alert remains unacknowledged,
- enrich notifications with safe metadata,
- create review tasks,
- log delivery status.

n8n must not bypass Prometheus backend safety controls.

## Recommended v1 n8n use

Allowed:

- receive redacted alert webhook,
- route notification,
- retry delivery,
- escalate unacknowledged critical alerts,
- send daily/weekly review reminders,
- record notification delivery.

Avoid initially:

- sending exchange orders,
- calling Binance directly,
- clearing kill switches,
- approving high-risk actions,
- mutating Prometheus runtime state,
- storing secrets unnecessarily.

## Webhook payload rules

n8n alert payloads must be redacted.

Allowed fields:

- alert ID,
- severity,
- class,
- title,
- safe message,
- stage/environment,
- symbol,
- safe state summary,
- recommended action,
- dashboard reference,
- timestamp.

Forbidden fields:

- API secrets,
- signed payloads,
- private keys,
- full webhook tokens,
- full `.env` contents,
- unredacted credential identifiers,
- sensitive host internals not needed for alerting.

## n8n route failure

If n8n delivery fails:

- record delivery failure,
- show route degraded on dashboard,
- alert locally if possible,
- block tiny-live launch if critical route has not been tested.

---

## Alert Acknowledgement

## Purpose

Acknowledgement records that the operator saw the alert.

## Allowed acknowledgement

The operator may acknowledge:

- info alerts,
- warning alerts,
- critical alerts,
- incident-linked alerts.

## Acknowledgement fields

Acknowledge action should record:

- operator identity,
- timestamp,
- optional note,
- alert ID,
- current alert status,
- related incident/state.

## Acknowledgement does not

Acknowledgement does not:

- clear incident,
- clear kill switch,
- clear daily lockout,
- clear drawdown pause,
- clear unknown execution outcome,
- confirm protective stop,
- resolve credential compromise,
- resume trading.

## Dashboard display

Dashboard should show:

```text
ACKNOWLEDGED, CONDITION STILL ACTIVE
```

when applicable.

---

## Alert Resolution

## Purpose

Resolution records that the underlying condition is no longer active or has been contained.

## Resolution requirements

For safety-relevant alerts, resolution should include evidence.

Examples:

- reconciliation completed clean,
- protective stop confirmed,
- position flattened,
- credential rotated,
- alert route test passed,
- dashboard restored,
- runtime DB restored,
- incident resolved.

## Manual resolution

Manual resolution should be limited.

The operator may record resolution only if supporting state/evidence exists.

The UI should not allow manual resolution of hard exchange-state facts without backend confirmation.

## Auto-resolution

Auto-resolution may be acceptable for low-severity technical alerts.

For critical alerts, auto-resolution should be conservative and should preserve review history.

Example:

- stream degraded while flat may resolve automatically after stable reconnection,
- unprotected position alert should not resolve without protection/flat confirmation.

---

## Alert Grouping and Deduplication

Alerts should avoid flooding the operator.

## Dedupe key

Each alert should have a dedupe key based on:

- alert class,
- alert type,
- symbol,
- related trade/order/incident where relevant,
- affected component.

## Occurrence count

Repeated occurrences should update:

- occurrence count,
- last seen time,
- current status,
- escalation state.

## Grouped display

Dashboard should show grouped alerts such as:

```text
User stream reconnect warning repeated 4 times in 30 minutes.
```

## Do not dedupe away severity change

If repeated events worsen severity, alert severity should escalate.

Example:

- user stream warning while flat,
- then user stream stale while exposed,
- should become critical.

---

## Quieting and Suppression Rules

Alert suppression is risky and should be limited.

## Allowed suppression

Suppression may be allowed for:

- known noisy warning during maintenance,
- non-live environment test noise,
- duplicate informational alerts,
- time-bounded planned outage.

## Requirements

Suppression must be:

- time-bounded,
- reasoned,
- visible,
- audited for safety-relevant alerts,
- reversible,
- not allowed to hide critical active exposure/protection emergencies.

## Forbidden suppression

Do not suppress:

- unprotected live position,
- unknown execution outcome,
- credential compromise,
- kill switch active,
- unsafe reconciliation mismatch,
- emergency flatten failure,
- manual/non-bot exposure in live mode,
- runtime DB unavailable during live-capable operation,
- dashboard unavailable during live exposure.

## Quiet mode

If quiet mode is implemented, it should not affect emergency/critical alerts.

---

## Escalation Rules

Escalation means increasing visibility or routing due to severity, persistence, or lack of acknowledgement.

## Escalation triggers

Possible escalation triggers:

- critical alert not acknowledged within configured time,
- same warning repeated frequently,
- user stream repeatedly stale,
- alert route failing,
- dashboard unavailable,
- protection uncertainty persists,
- recovery blocked awaiting operator,
- credential issue unresolved.

## Escalation actions

Allowed escalation actions:

- stronger dashboard banner,
- repeated Telegram message,
- n8n escalation route,
- incident creation,
- operator review required,
- kill switch activation if policy allows,
- entries blocked.

## Escalation limits

Escalation should not create exchange orders unless separately governed by incident/emergency policy.

Alerting UI routes should not bypass backend safety workflow.

---

## Alert History

The dashboard should provide alert history for review.

## Required history fields

- alert ID,
- severity,
- class,
- title,
- created time,
- acknowledged time,
- resolved time,
- duration active,
- occurrence count,
- related incident/trade/order,
- operator notes,
- delivery attempts,
- route failures,
- final status.

## Review use

Alert history should support:

- daily review,
- weekly review,
- incident review,
- phase-gate review,
- reliability review,
- dashboard/alert route testing review.

## Retention

Alert history retention should align with audit and observability retention policy.

Do not delete critical alert history casually.

---

## Alert Delivery Status

For each alert route, track delivery status.

## Dashboard route

Fields:

- local dashboard displayed yes/no,
- dashboard connected to backend yes/no,
- dashboard data freshness,
- alert rendered yes/no.

## Telegram route

Fields:

- enabled,
- last send status,
- last success,
- last failure,
- failure reason,
- last critical test.

## n8n route

Fields:

- enabled,
- last webhook status,
- last success,
- last failure,
- retry status,
- downstream route known/unknown.

## Route degradation alert

If a configured route fails, create an alert:

```text
ALERT_ROUTE_DEGRADED
```

Severity depends on stage:

- local/dev: info or warning,
- paper/shadow: warning,
- tiny live: warning or critical depending on loss of critical alert path,
- scaled live: critical if no alternate route exists.

---

## Alert Classes and Recommended Default Severity

| Alert condition | Default severity |
|---|---:|
| Process started | INFO |
| Safe mode entered on startup | INFO |
| Controlled restart requested | WARNING |
| Unexpected restart detected | WARNING or CRITICAL if exposure existed |
| Market data stale while flat | WARNING |
| Market data stale while exposed | WARNING/CRITICAL depending on management dependency |
| User stream stale while flat | WARNING |
| User stream stale while exposed | CRITICAL |
| Entry order rejected cleanly | WARNING |
| Entry order unknown outcome | CRITICAL |
| Position exists without confirmed stop | EMERGENCY/CRITICAL |
| Stop submission rejected while positioned | EMERGENCY/CRITICAL |
| Stop replacement unknown outcome | CRITICAL |
| Unsafe reconciliation mismatch | CRITICAL |
| Daily warning threshold reached | WARNING |
| Daily lockout reached | WARNING/CRITICAL depending on context |
| Drawdown watch | WARNING |
| Drawdown pause/hard review | WARNING/CRITICAL |
| Kill switch activated | CRITICAL |
| Emergency flatten requested | CRITICAL |
| Emergency flatten unknown outcome | EMERGENCY/CRITICAL |
| Credential validation failed | CRITICAL |
| Suspected credential compromise | EMERGENCY/CRITICAL |
| Runtime DB unavailable | CRITICAL in live-capable mode |
| Dashboard unavailable during live exposure | CRITICAL |
| Telegram/n8n failure in local dev | INFO/WARNING |
| Telegram/n8n failure in tiny live | WARNING/CRITICAL |

Implementation may tune severity, but must preserve safety intent.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical tasks should be captured later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

## Dashboard alert setup

- verify alert panel appears on NUC monitor,
- verify critical banner appears,
- verify acknowledgement works,
- verify acknowledgement does not resolve alert,
- verify alert history is visible,
- verify route status panel works.

## Telegram setup

- create Telegram bot/token at correct phase if used,
- store token securely,
- configure chat ID/channel safely,
- send test info/warning/critical messages,
- verify token is not logged,
- verify Telegram route failure is visible.

## n8n setup

- create n8n webhook route if used,
- store webhook URL/secret securely,
- verify payload redaction,
- test warning/critical routing,
- verify retries/escalation if configured,
- verify n8n does not call Binance or mutate live state.

## Launch readiness

- before paper/shadow, alert routing tested,
- before tiny live, critical alerts tested,
- verify alert-route degradation blocks or warns according to stage,
- verify dashboard remains primary approval/control surface,
- verify no high-risk approvals occur through Telegram/n8n in v1.

---

## Testing Requirements

## Unit tests

Test:

- severity classification,
- alert deduplication,
- alert lifecycle state transitions,
- acknowledgement behavior,
- resolution behavior,
- suppression eligibility,
- redaction rules,
- route payload generation,
- escalation trigger logic.

## Integration tests

Test alerts for:

- unprotected position,
- unknown entry outcome,
- user stream stale while exposed,
- market data stale,
- unsafe reconciliation mismatch,
- kill switch activation,
- daily lockout,
- drawdown pause,
- credential validation failure,
- runtime DB unavailable,
- dashboard route stale,
- Telegram delivery failure,
- n8n delivery failure.

## Dashboard tests

Test:

- critical alert banner visible,
- alert panel ordering by severity,
- acknowledged critical alert still visible if unresolved,
- resolved alert remains in history,
- grouped repeated alerts display count,
- suppressed alert visibly marked,
- route status visible,
- alert details link to incident/trade/order/reconciliation.

## Telegram tests

Test:

- warning message redacted,
- critical message redacted,
- no secrets in payload,
- delivery failure recorded,
- repeated alert grouping or rate limit behavior,
- approval-needed notification points back to dashboard.

## n8n tests

Test:

- webhook payload redacted,
- n8n route receives safe fields only,
- failure status returned/recorded,
- retry behavior if configured,
- no exchange-side action triggered from n8n in v1.

## Dry-run drills

Before tiny live, simulate:

- protective stop missing,
- unknown order outcome,
- user stream stale during exposure,
- alert route failure,
- dashboard disconnected,
- kill switch activation,
- emergency flatten alert,
- credential warning,
- critical alert acknowledgement and resolution.

---

## Forbidden Patterns

The following are not allowed:

- treating acknowledgement as resolution,
- hiding critical alerts after acknowledgement,
- sending secrets to Telegram or n8n,
- relying only on Telegram without dashboard visibility,
- allowing n8n to place exchange orders in v1,
- allowing Telegram to clear kill switch in v1,
- suppressing unprotected-position alerts,
- suppressing unknown-execution alerts,
- suppressing credential-compromise alerts,
- making PnL alerts more prominent than protection alerts,
- flooding operator with duplicate noise while hiding root condition,
- auto-clearing incidents because alert resolved,
- resuming trading because alert route delivered successfully,
- ignoring alert-route failure during tiny live,
- deleting alert history needed for incident review,
- showing stale state as current,
- failing silently when alert delivery fails.

---

## Non-Goals

This document does not define:

- exact dashboard CSS,
- exact Telegram bot code,
- exact n8n workflow nodes,
- exact alert transport library,
- exact authentication method,
- mobile app behavior,
- enterprise incident-management integration,
- final pager/on-call system,
- or exact setup commands.

It defines the alerting UI behavior and safety requirements for v1.

---

## Acceptance Criteria

`alerting-ui.md` is complete enough for v1 when it makes the following clear:

- alerts are safety signals, not cosmetic notifications,
- critical alerts dominate the dashboard,
- acknowledgement and resolution are separate,
- Telegram/n8n delivery does not equal handling,
- Telegram/n8n payloads must be redacted,
- the NUC dashboard remains the primary operator surface,
- Telegram/n8n may notify but should not initially approve high-risk actions,
- alert severity, class, lifecycle, and history are defined,
- alert grouping, dedupe, suppression, and escalation rules exist,
- alert route failures are visible,
- unprotected position, unknown execution outcome, unsafe reconciliation, and credential compromise cannot be suppressed casually,
- alert history supports incident and daily/weekly review,
- setup topics are deferred to the first-run checklist,
- and no alerting route may bypass runtime safety, approval, incident, or exchange reconciliation requirements.
