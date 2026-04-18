# Approval Workflows

## Purpose

This document defines the approval workflows for v1 Prometheus.

Its purpose is to define when an operator decision is required before the system may:

- resume after recovery,
- clear a kill switch,
- override or clear risk lockouts,
- increase risk,
- increase notional or leverage caps,
- promote deployment stages,
- enable production trade-capable mode,
- approve emergency or recovery actions,
- accept security exceptions,
- or proceed after incidents.

Prometheus is a safety-first, operator-supervised trading system. Approval workflows exist to prevent important state, risk, security, and deployment changes from becoming casual dashboard clicks.

The core rule is:

```text
Any action that increases risk, restores trading permission, clears a safety block,
changes live capability, or accepts a security/operational exception requires
explicit approval under a documented workflow.
```

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- first secondary research comparison: ETHUSDT perpetual,
- one-way position mode,
- isolated margin mode,
- one active strategy,
- one live symbol first,
- one open position maximum,
- one active protective stop maximum,
- no pyramiding in v1,
- no reversal entry while positioned in v1,
- exchange-side protective stop is mandatory,
- restart begins in safe mode,
- exchange state is authoritative,
- v1 is supervised and staged,
- default tiny-live host is a dedicated local NUC / mini PC with dashboard monitor.

This document covers approval workflows for:

- live enablement,
- recovery resumption,
- kill-switch clearance,
- daily lockout override,
- drawdown pause/hard-review clearance,
- incident resolution acceptance,
- risk fraction increase,
- notional cap increase,
- leverage cap increase,
- deployment stage promotion,
- release promotion,
- rollback approval,
- emergency flatten confirmation where applicable,
- protection restoration where operator approval is required,
- stale-order cleanup where operator approval is required,
- production key readiness,
- security exception acceptance,
- and setup/runbook topics for later first-run checklist.

This document does **not** define:

- final frontend UI design,
- exact API schemas,
- exact authentication/authorization implementation,
- exact Binance key creation steps,
- exact release tooling,
- exact setup commands,
- exact dashboard wireframes,
- or exact multi-operator enterprise workflow.

Those belong in implementation and first-run setup documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/event-flows.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/database-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/rollback-procedure.md`
- `docs/09-operations/release-process.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`
- `docs/10-security/permission-scoping.md`
- `docs/10-security/audit-logging.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/manual-control-actions.md`
- `docs/11-interface/alerting-ui.md`
- `docs/11-interface/dashboard-metrics.md`
- `docs/12-roadmap/phase-gates.md`

### Authority hierarchy

If this document conflicts with incident response on emergency containment, incident response wins.

If this document conflicts with kill-switch policy, kill-switch policy wins for activation/clearance requirements.

If this document conflicts with phase gates, phase-gates wins for stage-promotion evidence requirements.

If this document conflicts with security policy, security documents win for credential and permission requirements.

If this document conflicts with manual-control-actions on allowed/forbidden controls, manual-control-actions wins for interface control boundaries.

---

## Core Principles

## 1. Approval is a safety gate, not a formality

Approval must represent an actual review of state, evidence, and consequences.

An approval button is not enough if the underlying requirements have not been met.

## 2. Approval cannot make unknown state known

The operator cannot approve away uncertainty.

If exchange state is unknown, position protection is uncertain, execution outcome is unknown, or credential state is untrusted, approval must be blocked until the underlying issue is resolved or escalated through emergency containment.

## 3. Approval must be explicit

Important actions must not be approved implicitly by:

- restart,
- timeout,
- dashboard refresh,
- closing a modal,
- acknowledging an alert,
- successful backup,
- successful code deploy,
- or successful rollback.

Approval must be recorded as a deliberate operator/system-governance event.

## 4. Approval must be auditable

Every approval decision must create a durable audit record.

The audit trail should answer:

- who or what approved it,
- what was approved,
- when it was approved,
- why it was approved,
- what preconditions were checked,
- what state existed before approval,
- what state changed after approval,
- and which incident/trade/release/config it relates to.

## 5. Approval may deny as well as allow

The workflow must support denial.

A denial should keep the system blocked, paused, or under review as appropriate.

Denied approvals are important audit events.

## 6. Risk-increasing approvals require stronger evidence

Increasing risk fraction, leverage cap, notional cap, deployment stage, or production write capability requires stronger evidence than risk-reducing actions.

A previous setting is not automatically safe simply because it existed before.

## 7. Emergency containment may precede approval

Some emergency actions may need immediate execution before full approval flow completes.

Examples:

- automatic kill switch,
- automatic entries blocked,
- deterministic stop restoration,
- emergency flatten under defined policy.

When this occurs, the action must still be logged and reviewed afterward.

## 8. Dashboard convenience must not weaken approval discipline

The dedicated NUC dashboard should make approvals clear and usable.

It should not turn high-consequence approvals into casual clicks.

---

## Approval Concepts

## Approval request

An approval request is a structured request to allow a restricted action.

It should include:

- requested action,
- reason,
- initiating actor,
- current runtime state,
- current exposure state,
- current protection state,
- incident state,
- relevant evidence,
- required checks,
- expiration if applicable.

## Approval decision

An approval decision is the final operator/system-governance response.

Allowed decisions:

```text
APPROVED
DENIED
DEFERRED
EXPIRED
CANCELLED
```

## Approval scope

Approval must be scoped.

Examples:

- approve recovery for this incident only,
- approve risk increase for this config version only,
- approve tiny-live launch for this release only,
- approve emergency flatten for this current position only.

Open-ended approvals are dangerous.

## Approval expiration

Some approvals should expire if not used quickly.

Examples:

- recovery resumption approval,
- production trade-enable approval,
- emergency flatten confirmation,
- deployment promotion approval.

Expiration prevents stale approvals from being used after conditions change.

## Approval evidence

Approval should reference evidence such as:

- reconciliation result,
- incident report,
- test results,
- validation report,
- paper/shadow review,
- host-hardening checklist,
- alert test result,
- backup restore test,
- release notes,
- config diff,
- risk review.

---

## Approval Levels

Prometheus should distinguish approval levels by consequence.

## Level 0 — No approval required

Read-only actions and routine display behavior.

Examples:

- view dashboard,
- view chart,
- view open orders,
- view audit record,
- view trade details.

## Level 1 — Operator acknowledgement

Used when the operator only confirms awareness.

Examples:

- acknowledge informational alert,
- acknowledge noncritical warning,
- add note.

Acknowledgement does not resolve the condition.

## Level 2 — Operational approval

Used for ordinary controlled operations that affect runtime state but do not increase risk.

Examples:

- clear operator pause,
- request controlled restart,
- approve recovery after clean reconciliation,
- acknowledge incident containment.

## Level 3 — Safety-critical approval

Used when resuming after uncertainty, clearing hard safety blocks, or authorizing risk-reducing exchange-side action.

Examples:

- clear kill switch,
- approve recovery after incident,
- approve stale-order cleanup,
- approve protection restoration where automatic restoration is not enough,
- confirm emergency flatten when operator confirmation is available,
- accept rollback after live-capable failure.

## Level 4 — Governance approval

Used for risk, deployment, security, or production-capability changes.

Examples:

- enable production trade-capable mode,
- promote paper/shadow to tiny live,
- promote tiny live to scaled live,
- increase risk fraction,
- increase notional cap,
- increase leverage cap,
- accept security exception,
- proceed without IP restriction,
- clear drawdown hard review,
- approve release promotion to live.

Governance approvals require the strongest evidence and audit trail.

---

## Required Approval Record

Every approval request and decision should be stored durably.

Minimum fields:

```text
approval_id
approval_type
approval_level
requested_action
requested_by
requested_at_utc_ms
decision
decided_by
decided_at_utc_ms
expires_at_utc_ms
deployment_stage
environment
runtime_mode
entries_blocked
kill_switch_active
paused_by_operator
incident_active
highest_active_incident_severity
operator_review_required
symbol
trade_reference
position_state_summary
protection_state_summary
reconciliation_state
daily_loss_state
drawdown_state
config_version
release_version
risk_config_summary
evidence_references
reason
decision_notes
pre_decision_state_hash
post_decision_state_hash
audit_event_id
created_at_utc_ms
updated_at_utc_ms
```

The implementation may split this across approval and audit tables, but the semantic information must be preserved.

---

## Approval Workflow Pattern

Most approval workflows should follow this pattern.

## Step 1 — Request

A request is created by:

- operator action,
- incident workflow,
- recovery workflow,
- phase-gate workflow,
- release workflow,
- risk review workflow,
- security workflow.

The request must clearly state what is being requested.

## Step 2 — Precondition check

Backend evaluates objective preconditions.

Examples:

- exchange state known,
- protection confirmed,
- no unknown execution outcome,
- reconciliation completed,
- incident state compatible,
- stage gate evidence available,
- host readiness complete,
- alert route tested,
- config version known,
- release version known.

If hard preconditions fail, approval cannot proceed.

## Step 3 — Evidence display

Dashboard/control surface shows:

- requested action,
- current state,
- reason,
- evidence,
- risks,
- required checks,
- what will happen if approved,
- what remains blocked if denied.

## Step 4 — Operator decision

Operator chooses:

```text
APPROVE
DENY
DEFER
CANCEL
```

For high-consequence decisions, require explicit typed confirmation or equivalent deliberate confirmation.

## Step 5 — Persist decision before action

The approval decision must be durably stored before the backend performs the approved restricted action.

## Step 6 — Execute scoped action

The backend executes only the approved action.

Approval must not grant broad permission for unrelated actions.

## Step 7 — Verify outcome

After execution:

- update runtime state,
- verify exchange state where applicable,
- reconcile if required,
- update dashboard,
- write audit/runtime events.

## Step 8 — Review

For high-consequence approvals, include the decision in daily/weekly or post-incident review.

---

## Live Enablement Approval

## Purpose

Live enablement approval allows Prometheus to operate with production trade-capable behavior.

This is a Level 4 approval.

## Required before production trade-capable mode

The following must be true:

- deployment stage allows live operation,
- dedicated NUC host baseline satisfied,
- dashboard visible on attached monitor,
- alert routing tested,
- runtime DB initialized and backed up,
- backup restore tested,
- safe-mode-first restart tested,
- reconciliation tested,
- exchange adapter tested in non-production mode,
- production API key permissions reviewed,
- IP restriction configured or exception approved,
- secrets stored correctly,
- logs/audit working,
- emergency access tested,
- kill switch tested,
- emergency flatten dry-run tested,
- current release approved,
- current config approved,
- phase gate passed.

## Approval effect

Approval permits production trade-capable mode only for the approved:

- release version,
- config version,
- deployment stage,
- host,
- account,
- symbol scope.

Changing any of those may require re-approval.

## Not allowed

Live enablement approval must not:

- bypass safe-mode-first startup,
- clear incidents automatically,
- clear kill switch automatically,
- override daily/drawdown controls,
- allow unbounded manual trading,
- allow production keys before the approved phase.

---

## Recovery Resumption Approval

## Purpose

Recovery resumption approval allows Prometheus to leave recovery/blocked state after restart, incident, stream gap, unknown outcome, or mismatch recovery.

This is usually Level 2 or Level 3 depending on severity.

## Required preconditions

Before approval:

- reconciliation must be completed,
- current position state must be known,
- open normal orders must be known,
- open algo/protective orders must be known,
- no unknown execution outcome remains,
- if position exists, protection must be confirmed or emergency state resolved,
- user stream and market data must be acceptable for the stage,
- runtime DB/log/audit are functioning,
- incident state must allow resumption,
- kill switch must be inactive or separately cleared,
- operator pause must be cleared or intentionally remain active.

## Approval effect

If approved:

- recovery block may be cleared,
- operator review requirement may be cleared if no longer required,
- runtime may move toward allowed operation,
- entries may only resume if all other gates permit.

Approval does not force entries allowed if another block remains.

## Denial effect

If denied:

- system remains blocked or safe,
- operator review remains required,
- reason is audited.

---

## Kill-Switch Clearance Approval

## Purpose

Kill-switch clearance approval clears a hard trust-boundary halt.

This is Level 3 at minimum.

Security-related kill switches may require Level 4 approval.

## Required preconditions

Before clearance:

- kill-switch activation reason reviewed,
- active incident reviewed,
- exchange position state known,
- protection state known,
- no unknown execution outcome,
- reconciliation acceptable,
- credentials trusted,
- dashboard/alerts functional,
- operator notes/reason recorded,
- no unresolved severe incident,
- rollback/recovery complete if relevant.

## Approval effect

If approved:

- `kill_switch_active` may be set false,
- operator review requirement may be cleared if appropriate,
- entries remain blocked if any other gate still blocks.

## Not allowed

Kill-switch clearance must not:

- auto-clear after timeout,
- auto-clear after restart,
- auto-clear after reconciliation alone,
- be hidden from dashboard,
- clear daily/drawdown lockouts unless separately approved,
- clear security concerns without security review.

---

## Daily Lockout Override Approval

## Purpose

Daily lockout override allows entries despite a daily loss lockout.

This is Level 3 or Level 4 depending on cause.

## Default policy

Daily lockout should usually not be overridden.

It exists to prevent loss clustering from becoming uncontrolled behavior.

## Allowed cases

Possible allowed cases:

- lockout triggered by accounting/data error,
- emergency/risk-reducing action requires temporary override,
- manual correction approved after review.

## Forbidden cases

Override is forbidden when:

- operator wants “one more trade,”
- normal losses triggered the lockout,
- drawdown controls also block,
- incident is unresolved,
- unknown execution outcome exists,
- stop/protection issue contributed to loss,
- risk increase is being attempted.

## Required evidence

- daily loss state,
- trade list,
- reason for lockout,
- whether losses were normal or abnormal,
- incident review if abnormal,
- operator reason.

## Approval effect

If approved, override must be scoped and time-limited.

It should not permanently disable daily loss rules.

---

## Drawdown Pause / Hard Review Clearance

## Purpose

This approval clears drawdown pause or hard review.

This is Level 3 or Level 4.

## Required evidence

- current drawdown state,
- high watermark,
- realized and mark-to-market drawdown,
- trade sequence review,
- comparison to expected backtest/tiny-live behavior,
- incident review,
- execution/protection reliability review,
- operator notes,
- risk posture review.

## Required conditions

Before clearance:

- no unresolved abnormal execution incident,
- no unresolved protection failure,
- no unresolved reconciliation mismatch,
- no unresolved security issue,
- no risk increase requested simultaneously unless separate governance approval exists.

## Approval effect

If approved:

- drawdown pause/hard review may be cleared,
- entries may resume only if all other gates permit,
- risk increases remain blocked unless separately approved.

---

## Risk Increase Approval

## Purpose

Risk increase approval permits raising the live risk fraction.

Examples:

```text
0.25% -> 0.50%
0.50% -> 0.75%
0.75% -> 1.00%
```

This is Level 4.

## Required evidence

- validated backtest evidence,
- paper/shadow behavior,
- tiny-live behavior if already live,
- execution reliability,
- stop placement/replacement reliability,
- reconciliation reliability,
- incident history,
- daily/weekly review results,
- drawdown behavior,
- slippage/fee behavior,
- operator readiness,
- host/dashboard/alert readiness,
- current config/release version.

## Required conditions

- no active kill switch,
- no active severe incident,
- no unresolved protection issue,
- no unresolved unknown outcome,
- no drawdown caution/pause/hard review that blocks risk increase,
- no daily lockout,
- phase gate permits increase.

## Approval effect

Risk increase should create:

- new config version,
- release/review note,
- audit event,
- operator approval record,
- staged rollout decision.

It should affect future trades only unless explicitly documented otherwise.

## Forbidden pattern

Risk must not be increased because recent trades were profitable.

Risk increase requires process evidence, not excitement.

---

## Notional Cap Increase Approval

## Purpose

Approves increasing maximum position notional.

This is Level 4.

## Required evidence

- reason for notional increase,
- sizing behavior,
- liquidity/slippage review,
- leverage implication,
- fee implication,
- risk cap consistency,
- exchange bracket review,
- tiny-live performance if applicable,
- operator approval.

## Required conditions

Same as risk increase, plus:

- notional cap remains compatible with account size,
- liquidation/margin behavior reviewed,
- internal notional cap explicitly configured.

## Approval effect

Creates a new risk/config version.

---

## Leverage Cap Increase Approval

## Purpose

Approves increasing maximum effective leverage cap.

This is Level 4.

## Required evidence

- why leverage increase is needed,
- stop-distance/sizing analysis,
- liquidation proximity review,
- fees/slippage review,
- bracket review,
- operational failure sensitivity review,
- stop/reconciliation reliability,
- incident history,
- operator approval.

## Required conditions

- no unresolved incidents,
- no unresolved protection failures,
- host/alert/dashboard readiness confirmed,
- risk model still sizes from stop distance,
- leverage is not being treated as a target.

## Approval effect

Creates a new config version and release/risk review record.

## Forbidden pattern

Do not increase leverage merely because Binance allows it.

---

## Deployment Stage Promotion Approval

## Purpose

Approves promotion between stages.

Examples:

```text
local/dev -> validation
validation -> dry-run
dry-run -> paper/shadow
paper/shadow -> tiny live
tiny live -> scaled live
```

This is Level 4 for paper/shadow to tiny live and above.

## Required evidence by stage

### Dry-run promotion

- unit tests pass,
- fake adapter works,
- runtime DB writes verified,
- dashboard basic status works,
- no live credentials required,
- logs/audit work.

### Paper/shadow promotion

- dry-run event flows validated,
- completed-bar timing verified,
- alerts tested,
- dashboard visible on NUC monitor,
- restart/safe-mode behavior tested,
- fake/paper execution lifecycle verified.

### Tiny-live promotion

- phase gate passed,
- host-hardening baseline complete,
- production keys created only at approved phase,
- API permissions scoped,
- IP restriction verified or exception approved,
- secrets configured safely,
- runtime DB backup/restore tested,
- dashboard visible on monitor,
- Telegram/n8n alerts tested,
- emergency controls tested in dry-run,
- rollback procedure understood,
- incident response understood,
- risk set to approved tiny-live default.

### Scaled-live promotion

- tiny-live review passed,
- no unresolved severe incidents,
- execution/protection reliability proven,
- drawdown behavior acceptable,
- operator review process stable,
- risk/notional/leverage changes separately approved.

## Approval effect

Promotion approval allows the deployment stage to change.

It does not automatically enable production trading unless that is part of the approved scoped action.

---

## Release Promotion Approval

## Purpose

Approves a code/config/documentation release for a target environment.

This is Level 2 through Level 4 depending on target stage.

## Required evidence

- release notes,
- git commit/version,
- config version,
- migration status,
- test results,
- rollback plan,
- affected modules,
- risk/execution/security implications,
- docs alignment if relevant.

## Live release requirements

Before live release promotion:

- no active unknown execution outcome,
- safe deployment window,
- runtime DB backup,
- rollback path,
- safe-mode-first restart,
- reconciliation after deploy,
- dashboard/alerts verified.

## Approval effect

Release becomes approved for a specific environment/stage.

---

## Rollback Approval

## Purpose

Approves rollback of code, config, dependency, deployment stage, or database migration.

This may be Level 2 to Level 4.

## Required evidence

- rollback reason,
- current exposure state,
- current protection state,
- current incident state,
- rollback target,
- database compatibility,
- config compatibility,
- release notes,
- backup state,
- expected restart behavior.

## Required conditions

Ordinary rollback should prefer flat/clean state.

If exposure exists, rollback must be subordinate to exposure safety.

Emergency rollback may be part of incident containment, but it must not bypass reconciliation.

## Approval effect

Allows rollback workflow to proceed.

After rollback:

- runtime starts safe,
- state is reconciled,
- dashboard/alerts verified,
- operator review remains if required.

---

## Emergency Flatten Confirmation

## Purpose

Confirms an emergency flatten action when operator confirmation is available.

This is Level 3.

## When confirmation may be bypassed

If automated emergency policy determines flatten is immediately required and confirmation is impossible or too slow, the system may act according to incident/emergency policy.

Such action still requires post-action audit and review.

## Required display before confirmation

Dashboard should show:

- position side,
- position size,
- current protection state,
- current open orders,
- current open algo orders,
- current incident,
- likely consequence,
- warning that action may close position at market.

## Approval effect

Allows backend to execute emergency flatten command.

It does not allow arbitrary manual trade.

---

## Protection Restoration Approval

## Purpose

Approves restoring protective stop coverage when automatic restoration requires operator involvement.

This is Level 3.

## Required preconditions

- position exists,
- position ownership known,
- position side known,
- stop price known,
- stop price valid,
- no conflicting stop ambiguity,
- restoration is risk-reducing/safety-restoring,
- exchange adapter available.

## Approval effect

Allows backend to submit protective stop restoration.

If restoration fails, emergency policy applies.

---

## Stale-Order Cleanup Approval

## Purpose

Approves cleanup of stale or unexpected orders when backend determines cleanup is safe but operator approval is required.

This is Level 3.

## Required preconditions

- order identity known,
- order role classified,
- cancellation effect understood,
- no harmful exposure effect expected,
- current position/protection context known,
- reconciliation context exists.

## Approval effect

Allows backend to cancel or clean up the approved order(s).

Unknown cancellation outcome enters failure-recovery policy.

---

## Production API Key Readiness Approval

## Purpose

Approves creation/use of production trade-capable API keys at the correct phase.

This is Level 4.

## Required preconditions

- tiny-live phase gate not premature,
- dedicated NUC prepared,
- host-hardening baseline complete,
- outbound IP stability reviewed,
- IP restriction plan ready,
- permissions scoped,
- secrets path prepared,
- audit logging ready,
- no production keys stored in git/docs/prompts,
- operator understands revocation/rotation path.

## Approval effect

Allows operator to create/configure keys according to security policy.

This approval should happen close to the correct phase, not during early design/coding.

---

## Security Exception Approval

## Purpose

Approves temporary or explicit exception to security baseline.

Examples:

- production API key without IP restriction,
- temporary alert-route degradation during non-live stage,
- temporary local dashboard access exception,
- delayed OS update,
- backup route exception.

This is Level 4 for any live-capable exception.

## Required evidence

- exception description,
- reason,
- risk,
- mitigation,
- expiration,
- review date,
- affected stage,
- operator approval.

## Forbidden exceptions

Some exceptions should not be accepted for live operation:

- known credential compromise,
- unprotected live position,
- no runtime DB,
- no audit logging,
- dashboard unavailable for tiny live,
- unsupported OS with production keys,
- secrets in git,
- live runtime as root,
- impossible emergency access.

---

## Dashboard Approval UX Requirements

The dashboard should make approvals clear and difficult to misuse.

## Required UX behavior

For approval workflows, dashboard should show:

- what is being approved,
- current runtime mode,
- current exposure state,
- current protection state,
- current incident state,
- current reconciliation status,
- risk/deployment impact,
- required evidence,
- unmet preconditions,
- confirmation level,
- expiration if applicable.

## High-risk approvals

For Level 3 and Level 4 approvals:

- use explicit confirmation,
- require reason/note,
- prevent accidental double-click,
- show consequences,
- show whether action is reversible,
- audit both request and decision.

## Disabled approvals

If approval preconditions fail, the approval control should be disabled and explain why.

Example:

```text
Cannot clear kill switch: reconciliation status is UNSAFE_MISMATCH.
```

---

## Telegram / n8n Approval Boundary

Telegram and n8n may be used for alert routing.

For v1, approval workflows should be conservative about remote approvals.

## Recommended v1 policy

Telegram/n8n may:

- notify operator of approval needed,
- include incident/alert summary,
- direct operator to dashboard,
- confirm that approval was recorded,
- send reminders/escalations.

Telegram/n8n should not initially be the primary channel for high-consequence approvals such as:

- emergency flatten,
- kill-switch clearance,
- production trade enablement,
- risk increase,
- leverage increase,
- stage promotion.

Reason:

```text
The dedicated NUC dashboard is the primary controlled supervision surface.
```

Future remote approvals may be considered only after authentication, audit, and replay/confirmation risks are addressed.

## Secret handling

Telegram bot tokens and n8n webhook secrets must be treated as secrets.

Approval notifications must not leak:

- API keys,
- secret values,
- signed URLs,
- full environment details,
- unredacted webhook tokens.

---

## Approval Expiration and Revocation

## Expiration

High-consequence approvals should expire.

Examples:

- live enablement approval expires if config/release changes,
- recovery approval expires if state changes before execution,
- emergency flatten confirmation expires if position changes,
- stage promotion approval expires if readiness evidence becomes stale.

## Revocation

Operator may revoke pending approval before execution.

Revocation should be audited.

## State change invalidation

Approval should become invalid if relevant state changes.

Examples:

- new incident opens,
- position opens/closes,
- protection becomes uncertain,
- config version changes,
- release changes,
- alert route fails,
- credential issue appears,
- reconciliation becomes stale.

---

## Approval Denial and Deferral

## Denial

Denial should:

- keep system in safe/blocked state where applicable,
- preserve operator-review requirement if still needed,
- record reason,
- create audit event.

## Deferral

Deferral means more evidence or review is needed.

Deferred approval should not be treated as approval.

The dashboard should show pending/deferred approvals clearly.

## Cancellation

Approval request may be cancelled if no longer relevant.

Example:

- emergency flatten request cancelled because position already closed and reconciliation confirmed flat.

Cancellation should be audited if safety-relevant.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical tasks should be included later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

## Approval setup

- verify dashboard can create approval requests,
- verify dashboard can approve/deny in dry-run,
- verify audit records are created,
- verify high-risk approvals require explicit confirmation,
- verify disabled approval controls explain missing preconditions.

## Phase readiness

- verify live enablement approval checklist,
- verify production API key readiness approval checklist,
- verify tiny-live stage promotion approval checklist,
- verify risk increase approval is disabled before evidence exists,
- verify security exception workflow is documented.

## Alert integration

- verify Telegram/n8n sends approval-needed alerts,
- verify Telegram/n8n does not expose secrets,
- verify remote alerts direct operator back to dashboard for high-risk approvals.

## Emergency drills

- dry-run emergency flatten confirmation,
- kill-switch clearance denial,
- recovery approval after clean reconciliation,
- recovery denial after unsafe mismatch,
- failed risk increase request due to drawdown state.

---

## Testing Requirements

Approval workflows must be tested before live use.

## Unit tests

Test:

- approval level classification,
- required precondition checks,
- approval expiration,
- state-change invalidation,
- denial/deferral/cancellation behavior,
- approval record creation,
- audit event creation,
- secret redaction.

## Integration tests

Test:

- recovery approval after clean reconciliation,
- recovery approval blocked after unsafe mismatch,
- kill-switch clearance blocked with active incident,
- kill-switch clearance blocked with unknown protection,
- daily lockout override rejected under normal-loss condition,
- drawdown clearance requires review,
- risk increase requires phase-gate evidence,
- notional cap increase creates config-change requirement,
- production trade enablement requires host/security/alert checks,
- emergency flatten confirmation maps to backend command.

## Dashboard tests

Test:

- high-risk approvals show state summary,
- disabled approval controls explain blockers,
- approval request cannot be reused after expiration,
- approval request invalidates when state changes,
- typed confirmation or equivalent is required for high-consequence actions,
- approval denial keeps system blocked,
- approval does not force `RUNNING_HEALTHY`.

## Dry-run drills

Before tiny live, perform dry-run drills for:

- approving recovery after restart,
- denying recovery after unsafe mismatch,
- requesting kill-switch clearance,
- failing kill-switch clearance due to unresolved incident,
- emergency flatten confirmation in simulated environment,
- production enablement approval blocked due to missing prerequisite,
- risk increase approval blocked due to insufficient evidence.

---

## Forbidden Approval Patterns

The following are not allowed:

- auto-approving live resumption after restart,
- auto-clearing kill switch,
- auto-clearing incidents,
- approving unknown exchange state,
- approving unprotected live position as safe,
- approving production trading without host/dashboard/alert readiness,
- approving risk increase during active drawdown controls,
- approving leverage increase casually,
- approving daily lockout override for “one more trade,”
- using alert acknowledgement as approval,
- using rollback success as approval to resume,
- using backup restore as approval to resume,
- allowing approval without audit record,
- allowing stale approval after state changes,
- allowing unrestricted remote approvals through Telegram/n8n in v1,
- using approval workflow to bypass forbidden manual trading controls.

---

## Non-Goals

This document does not define:

- exact frontend implementation,
- exact authentication mechanism,
- exact multi-user role model,
- exact approval API schema,
- exact database schema migrations,
- exact Telegram/n8n workflow configuration,
- exact first-run setup commands,
- or exact legal/compliance requirements.

It defines the operational approval policy for v1.

---

## Acceptance Criteria

`approval-workflows.md` is complete enough for v1 when it makes the following clear:

- approvals are safety gates, not formality,
- approval cannot make unknown exchange state known,
- high-consequence approvals require explicit evidence and audit trail,
- kill switch clearance is deliberate and never automatic,
- recovery resumption requires reconciliation and state certainty,
- daily lockout overrides are exceptional and discouraged,
- drawdown pause/hard-review clearance requires review,
- risk, notional, and leverage increases require governance approval,
- production trade-capable mode requires host/security/dashboard/alert readiness,
- stage promotion is governed by evidence and phase gates,
- emergency flatten confirmation is for containment, not discretionary trading,
- approval requests are scoped and may expire,
- Telegram/n8n may notify but should not initially approve high-risk actions,
- denied and failed approvals are audit-relevant,
- and no approval workflow may bypass protective-stop, reconciliation, incident, kill-switch, exposure, or security requirements.
