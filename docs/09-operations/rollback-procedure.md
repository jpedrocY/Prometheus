# Rollback Procedure

## Purpose

This document defines the rollback procedure for the v1 Prometheus trading system.

Its purpose is to ensure that when code, configuration, strategy parameters, risk settings, dependencies, database schema, deployment environment, alerting, dashboard behavior, or documentation references must be reverted, the system does not lose exchange-state certainty or bypass safety controls.

For Prometheus, rollback is not merely a source-control action.

Rollback is an operational safety procedure that must preserve:

- capital protection,
- exchange-state certainty,
- runtime control-state continuity,
- incident and operator-review continuity,
- auditability,
- database integrity,
- and operator visibility.

A rollback may restore a previous code or configuration version, but it does not by itself restore trust.

After rollback, Prometheus must still start safely, reconcile exchange state, verify position and protection state, preserve blocking safety flags, and only resume normal operation after all required gates pass.

---

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures,
- first live symbol: BTCUSDT perpetual,
- position mode: one-way mode,
- margin mode: isolated margin,
- one strategy-owned position maximum,
- one active protective stop maximum,
- supervised staged deployment,
- restart always begins in safe mode,
- exchange state is authoritative,
- runtime persistence is safety-critical,
- incidents are severity-classified,
- kill switch state persists and never auto-clears.

This document covers rollback for:

- application code,
- configuration,
- strategy parameters,
- risk settings,
- deployment environment stage,
- database migrations,
- dependencies,
- alerting and dashboard changes,
- documentation and release references,
- and operator-facing rollback verification.

This document does **not** define:

- the full release process,
- the full deployment model,
- full disaster recovery after host loss,
- full database schema,
- detailed shell commands for installation or service management,
- final CI/CD implementation,
- or final production infrastructure automation.

Those belong in related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/event-flows.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/observability-design.md`
- `docs/06-execution-exchange/failure-recovery.md`
- `docs/06-execution-exchange/position-state-model.md`
- `docs/06-execution-exchange/user-stream-reconciliation.md`
- `docs/07-risk/kill-switches.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/release-process.md`
- `docs/09-operations/operator-workflow.md`
- `docs/10-security/audit-logging.md`
- `docs/10-security/disaster-recovery.md`
- `docs/10-security/host-hardening.md`
- `docs/11-interface/approval-workflows.md`
- `docs/11-interface/manual-control-actions.md`
- `docs/12-roadmap/phase-gates.md`

### Authority hierarchy

If this document conflicts with the state model on runtime modes, the state model wins.

If this document conflicts with restart procedure on safe-mode-first startup and reconciliation, the restart procedure wins.

If this document conflicts with incident response on emergency containment, incident response wins.

If this document conflicts with kill-switch policy on activation or clearance, kill-switch policy wins.

If this document conflicts with security policy during suspected credential compromise or host compromise, the security and disaster-recovery documents win.

If rollback would reduce exchange-state certainty, exchange-state verification wins over rollback convenience.

---

## Core Principles

## 1. Rollback is not state clearance

Rollback must not silently clear:

```text
kill_switch_active
incident_active
operator_review_required
entries_blocked
paused_by_operator
daily_loss_lockout
drawdown_pause
reconciliation_required
unknown_execution_outcome
protection_uncertain
manual_or_external_exposure_detected
```

If any of those states are active before rollback, they must remain active after rollback unless cleared through their proper documented procedure.

Rollback may change software or configuration. It does not erase operational facts.

## 2. Rollback starts safe

Any runtime restart caused by rollback must begin in:

```text
SAFE_MODE
```

The runtime must not roll back and immediately resume live strategy activity.

After rollback, the runtime must:

1. load configuration,
2. load secrets where required,
3. open runtime persistence,
4. initialize logging and observability,
5. restore local state as provisional,
6. verify exchange connectivity where applicable,
7. restore user-stream capability where applicable,
8. reconcile exchange position/order/protection state,
9. expose operator-visible rollback status,
10. and only then consider safe-mode exit.

## 3. Exchange state outranks rollback target

A rollback target may say the bot should be flat, but Binance may show:

- an open position,
- an open normal order,
- an active protective stop,
- a stale strategy-owned order,
- a manual order,
- or an unknown/external position.

Exchange state wins.

Rollback is not complete until exchange state has been reconciled.

## 4. Rollback must preserve auditability

Rollback must not delete or rewrite audit history.

The system must preserve:

- runtime events,
- exchange-derived events,
- operator actions,
- incidents,
- reconciliation runs,
- order/protection records,
- migration records,
- release/config references,
- and rollback decisions.

The goal is not to pretend the bad release never happened. The goal is to recover safely and leave a traceable record.

## 5. Live exposure changes rollback priority

If no exposure exists and no order/protection uncertainty exists, rollback can usually be treated as a routine operational procedure.

If exposure exists or may exist, rollback becomes safety-sensitive.

When exposure exists, the first objective is:

```text
confirm or restore protection
```

not:

```text
make the repository or process version look clean
```

## 6. Risk-increasing rollback requires approval

A previous configuration is not automatically safer.

A rollback target may contain:

- higher risk per trade,
- higher notional cap,
- higher leverage cap,
- weaker daily loss limits,
- weaker drawdown controls,
- weaker alerting,
- broader exchange permissions,
- or a less restrictive adapter mode.

If rollback increases risk or capability, it must be treated like a new promotion or risk increase and require explicit approval.

## 7. Database rollback is exceptional

Rolling back application code is common.

Rolling back the runtime database is dangerous.

The runtime database contains restart-critical and audit-critical evidence. It should not be restored backward casually, especially after live exchange activity.

A database restore may be valid for disaster recovery, corruption recovery, or failed migration recovery, but it must preserve the ability to reconcile against current exchange state.

---

## Rollback Is Not State Clearance

Rollback must be explicitly separated from clearance of safety controls.

### Safety states that rollback must preserve

Rollback must not clear:

| State or flag | Clearance authority |
|---|---|
| `kill_switch_active` | Kill-switch clearance workflow |
| `incident_active` | Incident response workflow |
| `operator_review_required` | Operator approval workflow |
| `entries_blocked` | Underlying blocking reason must clear |
| `paused_by_operator` | Operator pause clearance |
| daily loss lockout | Daily loss rules / UTC reset / review policy |
| drawdown pause | Drawdown controls / review policy |
| `reconciliation_required` | Successful reconciliation |
| unknown execution outcome | Exchange-state resolution |
| protection uncertainty | Protection confirmation or emergency containment |
| manual/non-bot exposure | Operator review and exposure cleanup |

### Practical rule

After rollback, the runtime should assume:

```text
rollback_completed != safe_to_resume
```

Safe resumption requires a separate reconciliation and clearance decision.

---

## Rollback Preconditions

Before any rollback is started, the operator or deployment process should identify:

- current deployment stage,
- current release version,
- current git commit hash,
- current config version,
- current strategy version,
- current risk config version,
- current database migration version,
- current runtime mode,
- current active incident state,
- current kill-switch/pause state,
- whether exposure exists or may exist,
- whether protective stop state is confirmed,
- whether any execution outcome is unknown,
- whether the rollback target is known-good,
- whether rollback may increase risk or capability,
- whether operator approval is required.

If these facts cannot be determined, rollback should proceed only as a controlled recovery or emergency procedure, not as a routine rollback.

---

## Rollback Types

Prometheus should distinguish three rollback types.

---

## 1. Routine Rollback

A routine rollback applies when:

- no live exposure exists,
- no entry or exit order is in flight,
- no unknown execution outcome exists,
- no active protective stop exists unexpectedly,
- no severe incident is active,
- exchange state is clean or not relevant to the environment,
- the rollback is planned or low pressure.

Examples:

- dry-run dashboard bug,
- local development dependency issue,
- validation report formatting regression,
- non-live config regression with no exchange-write capability.

### Default behavior

Routine rollback should:

1. record rollback intent,
2. preserve current logs and DB state,
3. switch to the approved rollback target,
4. restart in safe mode if runtime restart is needed,
5. run appropriate tests or health checks,
6. verify operator-visible status,
7. resume only if environment gates permit.

### Operator approval

Routine rollback may not require high-severity approval if it occurs in local/dev/validation environments.

However, all rollback actions should still be logged.

---

## 2. Controlled Live Rollback

A controlled live rollback applies when:

- the system is in a live-capable environment,
- exchange-write capability may exist,
- but exchange state is confirmed clean and flat,
- no unknown execution outcome exists,
- rollback is needed before further operation.

Examples:

- tiny-live release has a non-critical bug while flat,
- alert routing regression discovered before next entry,
- strategy config typo detected before new exposure,
- dashboard status display regression in live-capable deployment.

### Default behavior

Controlled live rollback should:

1. activate or preserve entry block,
2. verify flat exchange state,
3. verify no open normal orders,
4. verify no open algo/protective orders unless expected for recovery,
5. back up runtime DB where needed,
6. switch code/config/deployment target,
7. restart in safe mode,
8. reconcile again after rollback,
9. verify alerts/dashboard/logs,
10. require operator approval before normal live resumption if policy requires it.

### Operator approval

Controlled live rollback should be operator-visible and normally require approval before live operation resumes.

---

## 3. Emergency Rollback

An emergency rollback applies when:

- the current release or config may be unsafe,
- exposure exists or may exist,
- protective state may be uncertain,
- current code cannot safely manage exposure,
- a severe incident is active,
- or rollback is part of containment.

Examples:

- current release fails to confirm protective stop state,
- current release repeatedly produces unknown order outcomes,
- current config accidentally enables unsafe exchange capability,
- dashboard or alerting failure hides emergency state,
- dependency update breaks user-stream or reconciliation behavior,
- current process cannot safely continue and a known previous version can.

### Default behavior

Emergency rollback is subordinate to exposure safety.

The system should:

1. enter or remain in safe mode,
2. activate or preserve kill switch if appropriate,
3. block new entries,
4. determine whether exposure exists,
5. determine whether confirmed protection exists,
6. restore protection or flatten if required by incident policy,
7. preserve runtime DB and logs if possible,
8. roll back code/config only when doing so does not worsen exposure uncertainty,
9. reconcile after rollback,
10. require explicit operator review before any resumption.

### Important rule

If a position is unprotected, emergency handling should focus first on:

```text
restore protection or flatten
```

not:

```text
complete a clean software rollback
```

---

## Rollback Categories

Rollback can affect different system layers. Each category has different risks.

---

## Code Rollback

Code rollback means returning the runtime implementation to a previous known-good git commit or release version.

### Common triggers

- runtime regression,
- exchange adapter regression,
- user-stream handling bug,
- dashboard/control regression,
- unexpected crash,
- dependency incompatibility introduced by code change,
- failed release validation.

### Required checks

Before code rollback, identify:

- current release version,
- rollback target release version,
- matching git commit hash,
- database migration compatibility,
- configuration compatibility,
- dependency lockfile compatibility,
- known incidents associated with both versions.

### Safety rules

Code rollback must not:

- clear safety flags,
- bypass reconciliation,
- erase order/protection records,
- disable audit logging,
- silently change adapter mode,
- silently increase exchange capability.

### Post-rollback requirements

After code rollback:

- runtime starts in safe mode,
- local state is treated as provisional,
- exchange state is reconciled where applicable,
- tests or smoke checks are run as stage-appropriate,
- operator-visible version is updated,
- rollback event is recorded.

---

## Configuration Rollback

Configuration rollback means restoring a previous approved runtime configuration.

Configuration may include:

- environment mode,
- adapter mode,
- symbol scope,
- risk fraction,
- max effective leverage,
- max notional cap,
- daily loss thresholds,
- drawdown thresholds,
- alert routing,
- dashboard bind address,
- database path,
- log path,
- feature flags,
- exchange capability flags.

### Common triggers

- bad config deployed,
- wrong environment selected,
- alert route broken,
- dashboard exposed incorrectly,
- risk value misconfigured,
- adapter mode mismatch,
- file path or permission issue.

### Safety rules

Config rollback must not silently increase risk.

If the rollback target has any of the following, it requires explicit approval:

- higher risk fraction,
- higher notional cap,
- higher leverage cap,
- broader symbol scope,
- exchange write capability where current config does not,
- weaker alert routing,
- weaker lockout thresholds,
- less restrictive operator controls.

### Recommended behavior

Configuration rollback should be recorded as:

- previous config version,
- target config version,
- config hash,
- operator identity if applicable,
- reason,
- risk/capability comparison,
- approval reference if needed.

---

## Strategy Parameter Rollback

Strategy parameter rollback means restoring a previous validated strategy variant or parameter set.

Examples:

- setup window,
- breakout buffer,
- ATR length,
- trend filter,
- stop buffer,
- stop-management stage thresholds,
- exit/trailing settings.

### Safety rules

Strategy rollback should normally apply to **future signals only**.

It must not casually rewrite the risk assumptions of an existing open trade.

For an active live position:

- existing risk-approved stop should remain authoritative unless a risk-reducing update is approved,
- stop widening remains forbidden in v1,
- strategy-stage changes must not cause duplicate exit/entry behavior,
- operator review may be required if the current release cannot manage the open trade under old strategy rules.

### Required checks

Before strategy parameter rollback:

- verify the target strategy version was validated,
- verify it matches current data/timeframe assumptions,
- verify it does not require incompatible state fields,
- verify it does not bypass current risk controls,
- verify it does not conflict with active trade management.

---

## Risk Setting Rollback

Risk setting rollback means restoring previous risk-related configuration.

Examples:

- risk fraction,
- risk usage buffer,
- effective leverage cap,
- notional cap,
- daily loss thresholds,
- drawdown thresholds,
- max concurrent positions,
- stop validation tolerances.

### Risk-reducing rollback

Examples:

- `0.50%` risk back to `0.25%`,
- lower notional cap,
- lower leverage cap,
- stricter daily lockout,
- stricter drawdown pause.

Risk-reducing rollback is generally acceptable if it does not disrupt management of an existing protected position.

### Risk-increasing rollback

Examples:

- `0.25%` risk back to `0.50%`,
- higher notional cap,
- higher leverage cap,
- looser daily lockout,
- looser drawdown controls.

Risk-increasing rollback requires the same standard as a new risk increase.

It should require:

- explicit operator approval,
- phase-gate compatibility,
- release/config audit record,
- no active blocking incident,
- no active drawdown/risk-increase block,
- clean reconciliation.

---

## Deployment Environment Rollback

Deployment environment rollback means demoting or restoring the system to a previous deployment stage or capability profile.

Examples:

```text
scaled_live -> tiny_live
tiny_live -> paper_shadow
paper_shadow -> dry_run
dry_run -> local_dev
```

### Safer-stage demotion

Demotion to a safer environment should be easy and favored when uncertainty exists.

Examples:

- live trading disabled,
- adapter mode changed to fake/simulated,
- exchange write capability disabled,
- risk config returned to paper/tiny mode,
- production key loading disabled.

### Promotion back upward

Promotion back upward after rollback is not automatic.

Returning from paper/shadow to tiny live, or from tiny live to scaled live, requires normal phase-gate and approval workflows.

### Important rule

Deployment rollback must not leave stale live credentials or exchange-write capability enabled in a non-live environment.

---

## Database Migration Rollback

Database migration rollback is one of the highest-risk rollback categories.

The runtime database stores restart-critical and audit-critical state. It must not be treated as disposable application cache.

### Required migration discipline

Before any runtime DB migration:

- current migration version must be known,
- target migration version must be known,
- runtime DB backup should be created,
- migration compatibility should be checked,
- rollback plan should be documented,
- live exposure state should be checked,
- tests should cover migration and rollback path where practical.

### Preferred migration policy

The preferred v1 policy is:

```text
forward-compatible migrations where practical
backup before migration
no destructive changes without explicit approval
preserve audit/event history
```

### Database rollback dangers

Database rollback can:

- erase evidence of exchange actions,
- erase unknown-outcome records,
- erase operator actions,
- erase incident state,
- create mismatch between local state and current Binance state,
- break deterministic reconciliation,
- make post-incident review unreliable.

### Live exposure rule

Do not restore an older runtime database while live exposure exists unless disaster recovery policy explicitly requires it and exchange reconciliation will be performed immediately.

### History preservation rule

Rollback must not delete append-only audit history merely to undo a bad release.

If data correction is required, prefer compensating records or marked supersession over destructive rewrite.

---

## Dependency Rollback

Dependency rollback means restoring previous Python package, lockfile, or system dependency versions.

### Common triggers

- WebSocket library regression,
- HTTP client behavior change,
- Binance API client incompatibility,
- serialization/deserialization bug,
- database driver issue,
- Decimal/timestamp handling regression,
- test framework or linting change that blocks development.

### Required checks

Dependency rollback should verify:

- lockfile version,
- Python version compatibility,
- runtime database compatibility,
- exchange adapter tests,
- user-stream normalization tests,
- timestamp handling tests,
- strategy calculation tests,
- restart/reconciliation tests where applicable.

### Safety rule

Dependency rollback must not occur silently in live-capable deployment without a release/config record.

---

## Alerting and Dashboard Rollback

Alerting and dashboard rollback means restoring operator visibility after a monitoring, alerting, UI, or control-surface regression.

Relevant systems may include:

- Telegram alert routing,
- n8n webhook routing,
- local logs,
- operator dashboard,
- dashboard backend/API,
- alert severity mapping,
- incident display,
- control confirmations.

### Safety rule

Tiny live should not continue normal operation if critical alerting or operator dashboard visibility is broken.

If critical operator visibility is degraded:

```text
block new entries
raise or preserve incident state
repair or roll back alerting/dashboard
verify visibility before resumption
```

### Required checks

After alerting/dashboard rollback:

- test critical alert route,
- verify dashboard displays runtime mode,
- verify position/protection status display,
- verify incident display,
- verify kill switch/pause status display,
- verify operator controls are not accidentally broadened.

---

## Documentation / Release Reference Rollback

Documentation rollback means restoring docs, release notes, runbooks, or version references to match the active system.

For Prometheus, documentation is part of the implementation source of truth.

### Safety rule

Release, configuration, strategy version, and documentation references must remain aligned.

If the runtime is rolled back to release `R1`, the operator should be able to identify:

- matching code commit,
- matching config version,
- matching strategy version,
- matching known limitations,
- matching risk policy,
- matching runbook expectations,
- matching rollback notes.

### Forbidden behavior

Do not leave the repo/documentation claiming the system is on a newer behavior model than the deployed runtime actually supports.

---

## Live Exposure and Rollback Blocking Rules

Rollback must check exposure state before ordinary rollback.

## Exposure states

The rollback procedure should classify exposure as one of:

```text
CONFIRMED_FLAT
POSSIBLY_EXPOSED
CONFIRMED_PROTECTED_POSITION
CONFIRMED_UNPROTECTED_POSITION
UNKNOWN_EXPOSURE_STATE
EXTERNAL_OR_MANUAL_EXPOSURE
```

## `CONFIRMED_FLAT`

Meaning:

- no exchange position,
- no open normal orders,
- no open algo/protective orders,
- no unknown execution outcomes,
- no unresolved mismatch.

Routine or controlled rollback may proceed.

## `POSSIBLY_EXPOSED`

Meaning:

- entry/exit status unknown,
- REST timeout occurred,
- user-stream gap may hide updates,
- local/exchange state has not been reconciled.

Ordinary rollback is blocked until reconciliation classifies state.

## `CONFIRMED_PROTECTED_POSITION`

Meaning:

- exchange confirms position,
- ownership is known,
- exactly one valid protective stop is confirmed,
- state is otherwise trusted.

Rollback may proceed only as controlled live rollback if the rollback target can safely manage or preserve the protected position.

Operator approval is recommended.

## `CONFIRMED_UNPROTECTED_POSITION`

Meaning:

- exchange confirms position,
- protective stop is missing, rejected, uncertain, or not confirmed.

Emergency policy applies.

Rollback is secondary to restoring protection or flattening.

## `UNKNOWN_EXPOSURE_STATE`

Meaning:

- the bot cannot currently determine whether position/order/protection state is safe.

Ordinary rollback is blocked.

Safe mode, reconciliation, and incident handling apply.

## `EXTERNAL_OR_MANUAL_EXPOSURE`

Meaning:

- exposure exists that cannot be classified as Prometheus-owned.

New entries remain blocked.

Rollback does not manage discretionary/manual exposure automatically.

Operator review is required.

---

## Safe-Mode-First Restart After Rollback

Any rollback that restarts the runtime must follow safe-mode-first behavior.

## Required sequence

```text
1. Persist rollback intent.
2. Block new entries.
3. Stop runtime safely where applicable.
4. Preserve runtime DB and logs.
5. Switch code/config/dependency/deployment target.
6. Start runtime in SAFE_MODE.
7. Load local state as provisional.
8. Initialize logs/observability.
9. Verify config and secrets boundary.
10. Restore exchange/user-stream capability where applicable.
11. Query exchange position/orders/algo orders where applicable.
12. Reconcile.
13. Classify rollback verification outcome.
14. Require operator approval if needed.
15. Only then allow normal resumption if all gates pass.
```

## Safe-mode exit rule

Rollback verification may allow safe-mode exit only when:

- reconciliation is clean or safely recoverable and repaired,
- no blocking incident remains,
- kill switch is not active,
- operator pause is not active,
- operator review is not required or has been completed,
- streams and exchange connectivity are trusted where needed,
- position/protection state is acceptable,
- config/release versions are known,
- alerting/dashboard visibility is acceptable for the stage.

---

## Reconciliation Requirements

Rollback must trigger reconciliation in live-capable environments when any of the following are true:

- runtime was restarted,
- code changed,
- execution/exchange adapter changed,
- runtime DB migration changed,
- previous state included open trade/protection records,
- user stream had been stale,
- order status was unknown,
- protective stop state was uncertain,
- deployment stage changed,
- credentials or adapter capability changed,
- operator or incident policy requires it.

## Reconciliation minimum checks

The rollback verification reconciliation should check:

- BTCUSDT position state,
- open normal orders,
- open algo/protective orders,
- expected strategy-owned order IDs,
- known stop IDs,
- manual or external exposure,
- unknown outcome records,
- stale order/protection records,
- runtime DB consistency.

## Reconciliation outcomes

Rollback should classify reconciliation as:

```text
ROLLBACK_RECONCILIATION_CLEAN
ROLLBACK_RECONCILIATION_RECOVERABLE
ROLLBACK_RECONCILIATION_UNSAFE
```

### `ROLLBACK_RECONCILIATION_CLEAN`

The rollback target and current exchange state are compatible.

Normal resumption may be considered if other gates pass.

### `ROLLBACK_RECONCILIATION_RECOVERABLE`

A mismatch exists but can be repaired deterministically.

Repair must be completed and logged before resumption.

### `ROLLBACK_RECONCILIATION_UNSAFE`

Mismatch cannot be repaired safely or automatically.

The runtime remains in safe mode or blocked awaiting operator.

Incident/escalation policy applies.

---

## Operator Approval Requirements

Operator approval is required when rollback involves any of the following:

- live-capable deployment,
- active or possible exposure,
- active incident,
- kill-switch clearance,
- operator-review-required clearance,
- risk-increasing config rollback,
- exchange-write capability change,
- database restore,
- database destructive migration rollback,
- emergency rollback,
- production secret or credential change,
- alerting/dashboard degradation in tiny live or beyond,
- promotion back to a higher deployment stage after rollback.

## Approval record

Approval should record:

- operator identity,
- timestamp,
- rollback reason,
- rollback type,
- current version,
- target version,
- known risks,
- exposure state,
- reconciliation status,
- approval decision,
- post-rollback verification result.

---

## Database Backup and Restore Requirements

## Backup before rollback

Before rollback in live-capable environments, the runtime database should be backed up if practical.

This is especially important before:

- database migrations,
- dependency rollback affecting storage,
- code rollback across schema versions,
- emergency rollback where state history is needed,
- host/service changes.

## Backup contents

A backup should preserve:

- runtime control state,
- trade records,
- order records,
- protective stop records,
- position observations,
- reconciliation runs,
- incidents,
- operator actions,
- runtime events,
- exchange events,
- daily loss state,
- drawdown state,
- config/release version records.

## Restore caution

Restoring a database does not restore exchange state.

After restore:

```text
exchange reconciliation is mandatory
```

## Do not overwrite current evidence casually

If restoring older DB state would overwrite newer audit evidence, incident records, or exchange-derived records, the operator must treat it as disaster recovery, not routine rollback.

---

## Observability and Audit Requirements

Rollback must be observable.

## Required rollback events

The runtime should emit structured events for:

- rollback requested,
- rollback type classified,
- rollback target selected,
- rollback prechecks started,
- rollback prechecks passed/failed,
- entries blocked for rollback,
- runtime stopped for rollback,
- runtime started after rollback,
- safe mode entered after rollback,
- config version loaded,
- release version loaded,
- database migration version checked,
- reconciliation started after rollback,
- reconciliation outcome classified,
- rollback verification passed/failed,
- operator approval requested,
- operator approval granted/denied,
- rollback completed,
- rollback failed,
- resumption allowed/blocked.

## Required audit fields

Rollback audit records should include:

- rollback ID,
- rollback type,
- rollback category,
- reason,
- initiating operator or process,
- current release/config/database version,
- target release/config/database version,
- deployment stage,
- exposure state before rollback,
- exposure state after rollback,
- reconciliation result,
- incident IDs if related,
- operator approval reference where applicable,
- timestamps,
- final status.

## Alerting

In paper/shadow and live-capable stages, rollback should produce operator-visible alerts when:

- rollback begins,
- rollback blocks entries,
- rollback fails,
- rollback requires operator decision,
- rollback completes but resumption is blocked,
- rollback completes and safe resumption is allowed.

---

## Rollback Verification Checklist

The following checklist defines the minimum verification questions after rollback.

### Version and configuration

- [ ] Current release version is visible.
- [ ] Current git commit hash is visible where applicable.
- [ ] Current config version is visible.
- [ ] Current strategy version is visible.
- [ ] Current database migration version is visible.
- [ ] Runtime stage is correct.
- [ ] Adapter mode is correct.
- [ ] Exchange-write capability is correct for the stage.

### Runtime state

- [ ] Runtime started in safe mode.
- [ ] Entries are blocked until verification completes.
- [ ] Kill switch state was preserved.
- [ ] Operator pause state was preserved.
- [ ] Incident state was preserved.
- [ ] Daily loss/drawdown state was preserved.
- [ ] Operator-review-required state was preserved.

### Exchange state

- [ ] Position state was queried where applicable.
- [ ] Open normal orders were queried where applicable.
- [ ] Open algo/protective orders were queried where applicable.
- [ ] Reconciliation was performed where required.
- [ ] Exposure state was classified.
- [ ] Protection state was confirmed if position exists.
- [ ] Unknown execution outcomes were resolved or remain blocking.

### Database and logs

- [ ] Runtime DB opened successfully.
- [ ] Required tables/migrations are compatible.
- [ ] Pre-rollback backup exists where required.
- [ ] Runtime events are being written.
- [ ] Operator actions are being written.
- [ ] Logs are being written to expected location.
- [ ] No secrets appear in logs/events.

### Operator visibility

- [ ] Dashboard/status output shows rollback version.
- [ ] Dashboard/status output shows runtime mode.
- [ ] Dashboard/status output shows entries allowed/blocked.
- [ ] Dashboard/status output shows position/protection state.
- [ ] Dashboard/status output shows incidents/kill switch/pause.
- [ ] Alert routing works where required.

### Resumption

- [ ] No blocking incident remains, or operator accepted continued blocked state.
- [ ] Kill switch clearance workflow completed if needed.
- [ ] Operator approval completed if needed.
- [ ] Safe-mode exit is allowed only if all gates pass.
- [ ] If gates do not pass, runtime remains safe/blocked.

---

## Forbidden Rollback Patterns

The following rollback patterns are forbidden for v1.

## 1. Rollback directly into live trading

Forbidden:

```text
rollback -> restart -> RUNNING_HEALTHY automatically
```

Required:

```text
rollback -> restart -> SAFE_MODE -> reconcile -> verify -> approve -> maybe resume
```

## 2. Clearing kill switch through rollback

A rollback must not clear a kill switch.

Kill switch clearance has its own workflow.

## 3. Clearing incidents through rollback

Rollback may help resolve an incident, but it does not automatically resolve it.

Incident resolution must be recorded separately.

## 4. Retrying unknown exchange actions after rollback

If an entry, exit, cancel, stop, or flatten outcome was unknown before rollback, the rolled-back runtime must not blindly retry it.

It must reconcile first.

## 5. Database restore without reconciliation

Restoring runtime DB from backup and then resuming without exchange reconciliation is forbidden.

## 6. Deleting audit records to undo a bad release

Audit/event/operator/exchange records must not be deleted merely to make rollback appear clean.

## 7. Risk-increasing rollback without approval

A rollback that raises risk, leverage, notional, symbol scope, or exchange-write capability requires explicit approval.

## 8. Live operation with broken critical alerting

Tiny live or scaled live must not continue normal entry behavior if critical alert routing or operator visibility is broken.

## 9. Strategy rollback that widens active stop risk

A strategy rollback must not widen an active live protective stop or increase risk on an existing trade unless a separately approved future policy allows it.

For v1, stop widening remains forbidden.

## 10. Rollback that ignores manual/non-bot exposure

Manual or external exposure remains a blocking condition regardless of code/config rollback.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

This document defines rollback policy and required safety behavior.

The practical step-by-step setup/runbook should be captured later in a dedicated operations checklist, likely:

```text
docs/09-operations/first-run-setup-checklist.md
```

That checklist should eventually include practical procedures for:

- identifying the currently deployed release/config version,
- identifying the rollback target,
- checking whether runtime is flat,
- backing up the runtime database,
- stopping and restarting the runtime service,
- applying code/config rollback,
- verifying database migration compatibility,
- verifying logs after rollback,
- verifying Telegram/n8n alert routing after rollback,
- verifying dashboard access after rollback,
- confirming safe-mode-first restart,
- confirming reconciliation before resumption,
- recording operator approval,
- and deciding whether to remain in paper/shadow, tiny live, or safe mode after rollback.

The setup checklist should not instruct the operator to create real Binance production keys before the correct phase gate.

---

## Testing Requirements

Rollback behavior must be testable.

## Required tests

The implementation should include tests for:

- rollback preserves kill switch state,
- rollback preserves operator pause state,
- rollback preserves incident state,
- rollback preserves operator-review-required state,
- rollback starts runtime in safe mode,
- rollback triggers reconciliation when required,
- rollback does not clear unknown execution outcome,
- risk-increasing rollback requires approval,
- database migration version mismatch blocks unsafe startup,
- duplicate rollback command does not duplicate audit events incorrectly,
- runtime event emitted for rollback request,
- runtime event emitted for rollback result,
- exchange-state mismatch after rollback blocks resumption,
- protected position after rollback remains protected or blocks resumption,
- unprotected position after rollback enters emergency handling,
- alert/dashboard rollback verification fails closed when critical visibility is missing.

## Simulation cases

The test suite should simulate:

- routine rollback while flat,
- controlled live rollback while flat,
- emergency rollback with protected position,
- emergency rollback with missing stop,
- rollback after REST timeout unknown outcome,
- rollback after user-stream stale condition,
- rollback after failed DB migration,
- rollback to config with higher risk,
- rollback with manual exposure detected.

## Manual rehearsal

Before tiny live, the operator should rehearse rollback in a non-live environment.

The rehearsal should prove:

- rollback target can be identified,
- runtime DB can be backed up,
- runtime starts safe after rollback,
- dashboard shows rollback state,
- alert route works,
- reconciliation flow executes,
- resumption remains blocked until gates pass.

---

## Non-Goals

This document does not attempt to define:

- final CI/CD tooling,
- exact shell commands,
- exact VPS service manager units,
- exact backup scripts,
- exact cloud provider setup,
- full disaster recovery after host compromise,
- full Git branching policy,
- complete release process,
- or final operator UI implementation.

Those details belong in:

- `docs/09-operations/release-process.md`,
- `docs/09-operations/first-run-setup-checklist.md` if created,
- `docs/10-security/host-hardening.md`,
- `docs/10-security/disaster-recovery.md`,
- `docs/11-interface/approval-workflows.md`,
- and implementation-specific deployment scripts.

---

## Acceptance Criteria

This document is considered satisfied when the implementation and operations plan can answer the following questions:

- What kinds of rollback does Prometheus support?
- When is rollback routine versus controlled live versus emergency?
- What safety states must rollback preserve?
- What preconditions must be checked before rollback?
- How does rollback behave when exposure exists?
- How does rollback behave when protection is uncertain?
- How does rollback interact with kill switch, incidents, daily loss, and drawdown controls?
- How does rollback interact with runtime database migrations?
- How does rollback preserve auditability?
- What operator approvals are required?
- What verification must happen after rollback?
- What rollback patterns are forbidden?
- What should be tested before tiny live?

The central rule is:

```text
Rollback may restore code or configuration, but it does not restore trust by itself.

After rollback, Prometheus must still start safe, preserve blocking safety flags,
reconcile exchange state, verify protection, preserve audit history, and require
operator approval when exposure, risk increase, database restore, or incident recovery is involved.
```
