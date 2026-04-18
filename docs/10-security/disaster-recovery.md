# Disaster Recovery

## Purpose

This document defines the disaster-recovery policy for the v1 Prometheus trading system.

Its purpose is to define how Prometheus should recover from major failures that threaten:

- capital protection,
- exchange-state certainty,
- runtime continuity,
- credential security,
- audit/review continuity,
- host availability,
- operator access,
- and safe staged operation.

Prometheus is designed as a safety-first, operator-supervised trading system. Disaster recovery must therefore prioritize:

```text
containment before continuation
exchange-state certainty before local-state trust
safe-mode-first rebuild before normal operation
credential safety before convenience
auditability before speed
```

A disaster-recovery event is not just a technical inconvenience. If the system cannot verify live exposure, protective stop coverage, credentials, runtime state, or operator control, then live operation must remain blocked until confidence is restored.

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- first live deployment host: dedicated local NUC / mini PC,
- attached desk monitor used for the operator dashboard,
- one-way position mode,
- isolated margin mode,
- one live symbol first,
- one active strategy,
- one open position maximum,
- one active protective stop maximum,
- runtime begins in safe mode after restart,
- exchange state is authoritative,
- user stream is primary live private-state source,
- REST is used for placement, cancellation, reconciliation, and recovery,
- production API keys are tightly scoped and protected,
- v1 is supervised, not lights-out autonomous.

This document covers recovery from:

- local NUC host loss,
- power failure and unclean shutdown,
- disk failure,
- runtime database corruption,
- runtime database loss,
- backup failure,
- lost or corrupted logs/audit records,
- credential compromise,
- secret-file loss or corruption,
- Binance/API disruption,
- internet/router/ISP outage,
- repository corruption,
- configuration corruption,
- dependency/environment corruption,
- operator dashboard loss,
- alert-routing loss,
- operator machine/access loss,
- and suspected host compromise.

This document does **not** define:

- exact shell commands,
- exact Linux recovery steps,
- exact backup scripts,
- exact Binance key-creation workflow,
- exact n8n/Telegram setup,
- full incident-response classification,
- full host-hardening baseline,
- or final first-run setup instructions.

Those practical steps should be defined later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

and should reference this disaster-recovery policy.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/rollback-procedure.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`
- `docs/10-security/permission-scoping.md`
- `docs/10-security/audit-logging.md`
- `docs/10-security/host-hardening.md`
- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/alerting-ui.md`
- `docs/11-interface/manual-control-actions.md`
- `docs/11-interface/approval-workflows.md`
- `docs/12-roadmap/phase-gates.md`

### Authority hierarchy

If this document conflicts with incident response on severity and containment behavior, the incident-response document wins.

If this document conflicts with restart procedure on normal restart sequencing, the restart procedure wins.

If this document conflicts with credential policy, the API-key, secrets-management, and permission-scoping documents win.

If this document conflicts with host-hardening on host baseline, the host-hardening document wins.

If this document conflicts with rollback policy on version rollback behavior, rollback-procedure wins.

---

## Core Principles

## 1. Disaster recovery is a safety process, not a productivity process

The goal is not to resume trading as quickly as possible.

The goal is to restore:

- exchange-state certainty,
- capital protection,
- credential integrity,
- runtime continuity,
- operator visibility,
- and auditability.

Only after those are restored may normal operation be considered.

## 2. Exchange state is authoritative after disaster

After any serious failure, local state must be treated as provisional.

The system must verify directly from the exchange:

- whether a BTCUSDT position exists,
- whether open normal orders exist,
- whether open algo/protective stop orders exist,
- whether a position is protected,
- whether manual/non-bot exposure exists,
- whether previous unknown execution outcomes remain unresolved.

The runtime database and backups help reconstruct intent and continuity, but they do not replace exchange reconciliation.

## 3. Safe-mode-first rebuild is mandatory

Any disaster recovery that restarts or rebuilds Prometheus must begin in:

```text
SAFE_MODE
```

New entries must remain blocked until:

- configuration is verified,
- secrets are verified,
- runtime database is restored or reinitialized safely,
- logs/audit behavior is available,
- dashboard/alert visibility is acceptable for the stage,
- exchange state is reconciled where applicable,
- incidents are reviewed,
- and operator approval is recorded when required.

## 4. Credentials are more important than convenience

If credential compromise is suspected, the correct response is not to keep the bot running for convenience.

The system must prioritize:

- revocation,
- rotation,
- permission review,
- IP restriction review,
- audit review,
- exchange activity review,
- and safe reconfiguration.

Trading can wait.

## 5. Disaster recovery must not erase audit history casually

Audit logs, runtime events, exchange-derived events, operator actions, reconciliation records, and incidents are part of system safety.

A disaster-recovery procedure must not delete or rewrite history to make the system appear clean.

If logs are missing or corrupted, that itself must be recorded as a recovery concern.

## 6. Recovery actions must be staged

A disaster-recovery event should proceed through stages:

1. contain,
2. preserve evidence where possible,
3. verify exchange state,
4. protect or flatten exposure if required,
5. restore/rebuild runtime,
6. verify configuration and credentials,
7. verify observability and dashboard access,
8. run reconciliation,
9. document recovery,
10. resume only after approval gates pass.

## 7. Manual exchange intervention is allowed only as emergency containment

In a severe failure, the operator may need to use Binance directly to verify or reduce exposure.

However, direct manual exchange actions must be treated as emergency actions:

- document the action,
- reconcile afterward,
- block new bot entries,
- preserve operator review requirement,
- update incident/audit records when the bot is restored.

The dashboard should remain the normal control surface, but disaster conditions may require emergency out-of-band action.

## 8. Recovery readiness must be tested before tiny live

Disaster recovery cannot be theoretical.

Before tiny live, the project should test:

- runtime DB backup,
- runtime DB restore,
- safe-mode-first restart,
- reconciliation after restore,
- alert-route failure behavior,
- dashboard restoration,
- service restart,
- host reboot,
- and emergency access.

---

## Disaster-Recovery Severity Categories

Disaster-recovery events should be classified by operational impact.

## DR-1 — Minor Recoverable Degradation

Meaning:

- no live exposure exists,
- no credential concern exists,
- no audit/log loss exists,
- recovery can be completed through normal restart or rollback paths.

Examples:

- dashboard process crashes but runtime remains safe,
- noncritical log rotation issue,
- local monitor disconnects while remote/local status remains available,
- temporary alert-route degradation in dry-run.

Default response:

- log issue,
- repair,
- verify dashboard/alert/status,
- continue only if stage gates allow.

## DR-2 — Operational Continuity Failure

Meaning:

- Prometheus cannot operate normally,
- but no immediate exposure-security emergency is confirmed.

Examples:

- local NUC reboots unexpectedly,
- runtime DB unavailable,
- dashboard unavailable during paper/shadow,
- alert route down before tiny live,
- dependency environment corrupted,
- network outage while flat.

Default response:

- enter/remain in safe mode,
- block entries,
- restore host/runtime/service,
- verify local state,
- reconcile if exchange connection exists,
- resume only after checks pass.

## DR-3 — State-Certainty or Protection Failure

Meaning:

- the system may not know whether exposure exists or is protected,
- or exchange state cannot be verified while it matters.

Examples:

- crash during order submission,
- runtime DB corruption after live entry attempt,
- user-stream and REST both unavailable during exposure,
- backup restore loses order/protection continuity,
- uncertain protective stop state after host failure.

Default response:

- treat as incident,
- block entries,
- verify exchange state urgently,
- preserve or restore protection if deterministic,
- flatten if protection cannot be trusted,
- require operator review before resumption.

## DR-4 — Security or Host Compromise

Meaning:

- credential, host, repository, or operator access may be compromised.

Examples:

- suspected Binance API key exposure,
- host malware or unauthorized login,
- secret file copied or leaked,
- unknown trade/order detected,
- repository/config tampering,
- stolen NUC,
- exposed Telegram/n8n tokens with control implications.

Default response:

- activate security/operational kill switch where possible,
- revoke or disable affected credentials,
- stop live operation,
- verify Binance account state manually and via trusted environment,
- rebuild from trusted source,
- restore only from trusted backups,
- require security review before any live resumption.

---

## Recovery Authority Rules

## Exchange authority

For exposure and order truth, Binance/exchange state is authoritative.

Local DB, backups, logs, and dashboard displays are supporting evidence, not final truth.

## Repository authority

For source code and docs, the trusted repository and reviewed release tags/commits are authoritative.

A local checkout on a possibly compromised host is not authoritative.

## Configuration authority

For live runtime configuration, the active approved config version is authoritative only if:

- it matches the expected hash/version,
- it was activated through approved process,
- it has not been corrupted,
- it matches the intended deployment stage.

## Operator authority

The operator may approve recovery/resumption only after required checks are complete.

Operator approval cannot bypass:

- active credential compromise,
- unknown exposure,
- unprotected position,
- missing reconciliation,
- failed host-hardening baseline,
- or unresolved severe incident.

---

## General Disaster-Recovery Sequence

The following sequence should be the default pattern for major recovery.

## Step 1 — Stop normal progression

Immediately ensure:

```text
entries_blocked = true
normal_strategy_progression_blocked = true
```

If runtime is still available:

- enter safe mode,
- activate pause or kill switch if appropriate,
- record incident/recovery event.

If runtime is unavailable:

- treat the next startup as disaster recovery,
- do not assume prior local state is safe.

## Step 2 — Determine whether exposure may exist

The operator/system must answer:

1. Was an order in flight?
2. Was a position open?
3. Was a protective stop confirmed?
4. Was stop replacement in progress?
5. Was emergency flatten in progress?
6. Was exchange state already uncertain?

If any answer is unknown:

```text
assume exposure may exist until exchange reconciliation proves otherwise
```

## Step 3 — Verify exchange state through trusted path

Use the safest available trusted method to determine:

- BTCUSDT position state,
- open normal orders,
- open algo/protective stop orders,
- recent fills/trades if needed,
- account mode and margin mode if relevant,
- unexpected manual/non-bot exposure.

If the Prometheus runtime is not trustworthy, use a clean trusted machine/session to inspect Binance account state.

## Step 4 — Preserve or reduce exposure risk

If exposure exists:

- verify whether a valid protective stop exists,
- preserve it if valid,
- restore protection if deterministic and safe,
- or flatten if protection cannot be trusted.

If direct manual action is required, document it and reconcile later.

## Step 5 — Contain credentials/security risk

If credential compromise is suspected:

- revoke affected Binance API keys,
- disable alert/webhook tokens if needed,
- rotate secrets,
- review IP restrictions,
- review recent exchange activity,
- inspect audit/operator actions,
- do not resume live operation until security review passes.

## Step 6 — Restore host/runtime

Depending on the failure, restore:

- NUC power/network,
- operating system,
- Prometheus service,
- runtime database,
- logs/audit path,
- config files,
- secret files,
- dashboard,
- alert routing.

Do not start normal trading during restore.

## Step 7 — Start Prometheus in safe mode

After restore or rebuild:

- start runtime,
- confirm safe mode,
- confirm entries blocked,
- load local state as provisional,
- verify config version,
- verify release version,
- verify DB migration state,
- verify secrets loaded safely,
- verify logs/audit enabled.

## Step 8 — Reconcile

Run startup/recovery reconciliation.

Classify result:

```text
CLEAN
RECOVERABLE_MISMATCH
UNSAFE_MISMATCH
```

Unsafe mismatch blocks resumption.

## Step 9 — Verify observability

Before resumption, verify:

- dashboard visible on monitor,
- critical alerts working,
- logs writable,
- audit records writable,
- operator can see current runtime status,
- incident/recovery state visible.

## Step 10 — Approve or deny resumption

Resumption requires:

- no unresolved severe incident,
- no unresolved credential concern,
- no unknown exposure,
- no unprotected position,
- reconciliation acceptable,
- operator review complete where required,
- deployment-stage gates still satisfied.

---

## Scenario 1 — Local NUC Host Loss

## Definition

The dedicated NUC becomes unavailable due to:

- hardware failure,
- power loss,
- disk failure,
- theft,
- physical damage,
- OS boot failure,
- unrecoverable local corruption.

## Immediate response

1. Assume Prometheus runtime is offline.
2. Determine whether live exposure may exist.
3. Use a trusted device/session to inspect Binance account state if live credentials were active.
4. Confirm position, open normal orders, and open algo/protective stops.
5. If exposure exists, verify protection or flatten according to emergency policy.
6. Activate/recommend kill switch state when runtime is restored.
7. Preserve failed host evidence if security compromise is possible.

## Recovery path

### If no exposure exists

- rebuild or replace host,
- restore repository from trusted source,
- restore approved config,
- restore runtime DB from backup if needed,
- verify secrets or recreate them,
- start in safe mode,
- reconcile,
- resume only after checks pass.

### If exposure exists

- prioritize exchange-side protection/flattening before host rebuild,
- record emergency/manual actions,
- rebuild host,
- restore runtime state,
- reconcile with exchange,
- require operator review before resumption.

### If host was stolen or possibly compromised

- revoke Binance API keys,
- revoke/rotate alert tokens,
- rotate dashboard credentials,
- review account activity,
- rebuild from trusted source,
- do not trust local backups stored only on stolen host,
- require security review before live resumption.

---

## Scenario 2 — Power Failure or Unclean Shutdown

## Definition

The NUC loses power, crashes, or shuts down unexpectedly.

## Required behavior

On next startup:

```text
Prometheus starts in SAFE_MODE.
```

It must not resume trading directly.

## Recovery steps

1. Restore power.
2. Confirm NUC boots.
3. Confirm runtime service state.
4. Confirm runtime DB is readable.
5. Confirm logs/audit are writable.
6. Start/restart Prometheus in safe mode.
7. Load local state as provisional.
8. Restore streams/connectivity.
9. Query exchange position/orders/stops.
10. Reconcile.
11. If clean, allow controlled resumption.
12. If mismatch exists, follow recovery/incident process.

## UPS considerations

A UPS is strongly recommended for tiny live.

If UPS is present, test:

- power-loss notification behavior if available,
- controlled shutdown behavior if configured,
- runtime DB integrity after simulated outage,
- router/network power dependency.

---

## Scenario 3 — Runtime Database Corruption

## Definition

The runtime database is unreadable, inconsistent, partially corrupted, or fails integrity checks.

## Why this matters

The runtime DB contains restart-critical evidence:

- runtime control state,
- active trade records,
- order records,
- protective stop records,
- reconciliation state,
- incident continuity,
- operator actions,
- audit/runtime events.

A corrupted DB can erase or distort local continuity.

## Immediate response

1. Stop normal runtime progression.
2. Do not attempt to trade.
3. Preserve corrupted DB copy if possible.
4. Determine whether live exposure may exist.
5. Query exchange state through trusted path.
6. Verify position/orders/stops.
7. Restore from latest known-good backup only after understanding exposure state.

## Restore policy

A database restore must not be treated as exchange truth.

After restore:

- start in safe mode,
- record restore event,
- mark state as requiring reconciliation,
- query exchange state,
- reconcile,
- classify mismatch,
- require operator review if live exposure existed or DB loss affected auditability.

## If no backup exists

If no usable runtime DB backup exists:

- rebuild database from clean schema,
- preserve available logs/audit exports,
- query exchange state,
- classify local continuity as lost,
- block resumption until exchange state is clean and operator review is complete.

If open exposure exists and local continuity is lost, treat as severe incident.

---

## Scenario 4 — Runtime Database Loss

## Definition

The database file is deleted, lost, overwritten, or unavailable.

## Required response

Runtime database loss during live-capable operation is a serious incident.

Immediate behavior:

```text
entries_blocked = true
operator_review_required = true
reconciliation_required = true
```

If runtime is still alive and detects DB loss:

- enter safe mode,
- stop live progression,
- alert operator.

If detected after restart:

- do not initialize a fresh DB and continue as if clean,
- first verify whether a backup exists,
- then reconcile exchange state.

## Recovery

1. Restore latest known-good backup if available.
2. If restore is not possible, initialize new DB only after exchange state is known.
3. Record continuity loss in incident/audit trail.
4. Reconcile exchange state.
5. Require operator review before any live resumption.

---

## Scenario 5 — Backup Failure

## Definition

Backups are missing, corrupted, stale, inaccessible, or have never been restore-tested.

## Policy

Backup failure does not always require immediate shutdown if the bot is flat and in non-live stages.

However, tiny-live promotion must be blocked if backups are not prepared and restore-tested.

## During live operation

If backup failure is discovered during tiny live:

- alert operator,
- block promotion/risk increase,
- consider pausing new entries until backup reliability is restored,
- do not perform risky migrations or releases,
- increase caution for rollback and recovery.

## Required review

Backup failures should be reviewed because they reduce disaster-recovery confidence.

---

## Scenario 6 — Lost or Corrupted Logs / Audit Records

## Definition

Runtime logs, audit logs, operator actions, exchange events, or incident records are missing, corrupted, or unrecoverable.

## Why this matters

Audit/review continuity is part of safety.

Lost audit logs can prevent the operator from understanding:

- what changed,
- who approved an action,
- whether a credential event happened,
- whether rollback occurred,
- whether an incident was handled correctly.

## Immediate response

- preserve remaining logs,
- stop log deletion/rotation if causing loss,
- verify runtime DB audit tables,
- verify current exchange state,
- open incident if live-capable operation is affected,
- block risk increase,
- require review before tiny-live/scaled-live continuation if loss is material.

## Resume policy

If audit loss is minor and no exposure/security ambiguity exists, operation may continue after repair.

If audit loss overlaps with live exposure, unknown execution outcome, credential concern, or emergency action:

```text
operator review required before resumption
```

---

## Scenario 7 — Credential Compromise

## Definition

A credential compromise exists or is suspected when any of the following occur:

- Binance API key/secret may have been exposed,
- secret file is copied to an unsafe location,
- secret appears in logs, screenshots, prompts, shell history, or git,
- unexpected orders/trades appear,
- unauthorized access is detected,
- alert/webhook token is exposed,
- dashboard/admin credential is exposed,
- host compromise may have exposed local secrets.

## Immediate response

1. Stop normal trading.
2. Activate security kill-switch behavior where possible.
3. Verify exchange position/orders/stops.
4. Preserve or reduce exposure risk.
5. Revoke affected Binance API keys.
6. Rotate affected secrets/tokens.
7. Review recent exchange/account activity.
8. Review audit logs and operator actions.
9. Rebuild or clean host if compromise may include host access.
10. Do not resume live operation until security review is complete.

## Binance API key handling

If Binance key compromise is suspected:

- revoke the key,
- do not reuse it,
- create new keys only after host and secrets path are trusted,
- reapply least-privilege permissions,
- reapply IP restrictions where possible,
- test in the correct phase,
- record credential rotation event.

## Alert tokens

If Telegram or n8n tokens/webhooks are exposed:

- rotate them,
- update secret storage,
- verify old token no longer works if possible,
- test alert route,
- confirm tokens are not logged.

## Security review

Resumption requires:

- no unresolved suspicious exchange activity,
- new credentials configured safely,
- secret redaction verified,
- audit event recorded,
- operator approval.

---

## Scenario 8 — Secret File Loss or Corruption

## Definition

Secret files are missing, unreadable, corrupted, have wrong permissions, or contain unexpected values.

## Required runtime behavior

If required live secrets cannot be loaded safely:

```text
live operation must fail closed
```

The runtime may start in safe mode for diagnosis but must not trade.

## Recovery

1. Do not print secret contents to logs.
2. Verify file path and permissions.
3. Restore from secure backup only if trusted.
4. If secret integrity is uncertain, rotate/recreate the secret.
5. Record credential/secret event.
6. Test redacted validation.
7. Resume only after configuration and permissions are verified.

---

## Scenario 9 — Binance/API Disruption

## Definition

Binance public/private APIs, REST, WebSocket, user stream, order endpoints, or account reads are unavailable, degraded, or returning abnormal errors.

## Immediate response

If flat:

- block new entries,
- monitor/retry according to backoff policy,
- avoid REST spam,
- alert if degradation persists.

If order in flight:

- enter safe/recovery mode,
- do not blindly retry exposure-changing actions,
- reconcile when API access returns.

If position exists:

- preserve existing exchange-side protection if confirmed,
- verify position/protection when possible,
- if protection cannot be verified and risk is unacceptable, follow emergency policy.

## Prohibited behavior

Do not:

- spam REST endpoints,
- place blind duplicate orders,
- assume flat because API is unavailable,
- clear incidents automatically after reconnect,
- continue new entries without restored confidence.

## Resume policy

Resumption requires:

- relevant APIs restored,
- user stream restored or reconciled,
- position/order/stop state verified,
- rate-limit/IP-ban risk cleared,
- operator visibility restored.

---

## Scenario 10 — Internet / Router / ISP Outage

## Definition

The local NUC loses internet connectivity or cannot reach Binance/alert endpoints due to local network, router, ISP, DNS, or routing failure.

## Why this is different from VPS

The default Prometheus host is local. The local network and router are therefore part of operational reliability.

## Immediate response

If Prometheus detects loss:

- mark connectivity degraded/unavailable,
- block new entries,
- mark streams stale as appropriate,
- enter recovery/safe mode if exposure or order certainty matters,
- alert locally if remote alerting is impossible.

## Operator response

The operator should check:

- router power,
- ISP status,
- local Ethernet connection,
- DNS/network settings,
- whether dashboard remains visible locally,
- whether Binance is reachable from another trusted connection.

If exposure exists and Binance cannot be reached from the NUC, the operator may need to inspect/act from another trusted device.

## Recovery

After connectivity returns:

- restore streams,
- verify REST connectivity,
- query exchange state,
- reconcile,
- verify alerts,
- resume only after gates pass.

---

## Scenario 11 — Repository Corruption or Code Tampering

## Definition

The local repository or application files are corrupted, unexpectedly modified, or suspected to be tampered with.

Examples:

- unknown file modifications,
- mismatched git commit,
- corrupted source files,
- unexpected dependency changes,
- malicious code suspicion,
- local checkout differs from approved release.

## Immediate response

- stop live operation,
- block entries,
- preserve current state,
- verify exchange state,
- compare local code to trusted repository/release,
- do not run unknown modified code with production credentials.

## Recovery

1. Restore code from trusted repository and approved release commit.
2. Verify release version.
3. Verify dependency lockfile.
4. Verify config compatibility.
5. Run required tests where applicable.
6. Start in safe mode.
7. Reconcile exchange state.
8. Record recovery/audit event.

If tampering is suspected, treat as security incident.

---

## Scenario 12 — Configuration Corruption

## Definition

Runtime configuration is missing, invalid, corrupted, unexpectedly changed, or inconsistent with the intended deployment stage.

Examples:

- risk fraction changed unexpectedly,
- adapter mode changed,
- symbol scope changed,
- alert route disabled,
- database path changed,
- wrong environment file loaded,
- production mode enabled in wrong environment,
- notional cap missing.

## Required response

Configuration corruption must fail closed.

Prometheus must not trade if:

- config version is unknown,
- config hash does not match expected value,
- risk settings are missing or invalid,
- live adapter mode is unexpectedly enabled,
- alerting requirements are not met for the stage,
- database/log paths are unsafe,
- secrets do not match environment.

## Recovery

- restore approved config version,
- verify hash/version,
- record config restoration,
- start in safe mode,
- reconcile if live-capable environment,
- require operator approval if risk or capability changed.

---

## Scenario 13 — Dependency or Python Environment Corruption

## Definition

The Python environment, dependency lockfile, package installation, or runtime environment becomes inconsistent.

Examples:

- dependency upgrade breaks Binance adapter,
- missing packages,
- incompatible Python version,
- corrupted virtual environment,
- dashboard dependency breakage,
- database driver issue.

## Immediate response

- stop normal operation,
- do not patch live environment ad hoc during exposure,
- preserve logs,
- verify exchange state if live-capable,
- rollback or rebuild environment from lockfile/release.

## Recovery

1. Recreate environment from approved lockfile.
2. Run required tests.
3. Verify database migration compatibility.
4. Verify adapter tests/fakes.
5. Start safe.
6. Reconcile.
7. Resume only after checks pass.

---

## Scenario 14 — Dashboard Loss

## Definition

The operator dashboard is unavailable, frozen, misleading, or not visible on the NUC monitor.

## Severity

Dashboard loss severity depends on deployment stage.

- local/dev: low,
- dry-run: degraded,
- paper/shadow: operational impairment,
- tiny live: serious if it affects supervision,
- scaled live: serious by default.

## Immediate response

If live-capable operation is active:

- alert operator through alternate route if possible,
- block new entries if operator visibility is insufficient,
- preserve existing protection,
- avoid normal progression if state cannot be supervised.

## Recovery

- restart dashboard process if separate,
- verify backend runtime state,
- verify dashboard values match backend state,
- verify open positions/orders/stops display correctly,
- verify incident/alert visibility,
- record dashboard recovery event.

The dashboard must not hide unresolved unsafe states after recovery.

---

## Scenario 15 — Alert Routing Loss

## Definition

Telegram, n8n, dashboard alerts, or other notification routes fail.

## Immediate response

If non-live:

- log and repair before promotion.

If paper/shadow:

- repair before treating stage as valid.

If tiny live:

- evaluate whether new entries should be paused until critical alerting is restored.

Critical exposure/protection alerts must be reachable by the operator before tiny-live launch.

## Recovery

- verify secret/token validity,
- verify webhook route,
- verify network path,
- send test warning and critical alerts,
- ensure tokens are not logged,
- record alert recovery event.

---

## Scenario 16 — Operator Machine or Access Loss

## Definition

The operator loses access to:

- local monitor,
- keyboard/mouse,
- SSH access,
- dashboard credentials,
- alert account,
- phone/Telegram,
- n8n management,
- or trusted device needed for emergency review.

## Immediate response

If live operation is active and operator cannot supervise:

```text
pause or kill switch should be activated where possible
```

If the runtime remains supervised locally by dashboard, the severity may be lower.

If no operator visibility/control exists:

- block new entries,
- preserve protection,
- avoid normal progression,
- restore operator access before resuming.

## Recovery

- restore local monitor/session,
- restore dashboard access,
- restore alert access,
- verify emergency controls,
- rotate credentials if access loss may imply compromise,
- record operator access recovery.

---

## Scenario 17 — Suspected Host Compromise

## Definition

The dedicated NUC may be compromised due to malware, unauthorized login, physical tampering, suspicious processes, unexpected files, or unexplained network behavior.

## Immediate response

1. Stop trusting the host.
2. Do not use it to inspect secrets.
3. Verify exchange state from another trusted device.
4. Preserve or reduce exposure risk.
5. Revoke or rotate credentials that may have been exposed.
6. Preserve evidence where practical.
7. Rebuild host from trusted installation media/source.
8. Restore only trusted backups.
9. Require security review before live resumption.

## Rebuild requirement

If compromise is credible, cleaning the existing host in place may not be enough.

Preferred recovery:

```text
fresh OS install
trusted repo clone
approved config restore
new credentials
safe-mode startup
full reconciliation
```

---

## Manual Exchange Access During Disaster

## When allowed

Manual Binance access may be required when:

- Prometheus host is unavailable,
- API/user stream cannot be trusted,
- position exists and protection cannot be verified,
- emergency flattening is required,
- credential revocation is required,
- operator must inspect account state from a trusted path.

## Required discipline

Manual exchange actions should be:

- limited to safety actions,
- documented,
- reconciled later,
- audited after Prometheus recovers,
- not used as discretionary trading.

Examples of allowed emergency manual actions:

- verify BTCUSDT position,
- verify open orders,
- verify protective stops,
- cancel dangerous/stale orders,
- flatten exposure if protection cannot be trusted,
- revoke API key.

Forbidden emergency misuse:

- discretionary entries,
- increasing leverage,
- increasing position size,
- moving stop farther away,
- bypassing daily/drawdown/kill-switch controls,
- hiding manual action from Prometheus review.

---

## Backup Policy

## Runtime DB backups

The runtime database should be backed up because it stores restart-critical state and audit/review information.

Backups should preserve:

- runtime control state,
- active trade records,
- order records,
- protective stop records,
- reconciliation runs,
- incidents,
- operator actions,
- audit/runtime/exchange events,
- daily loss state,
- drawdown state,
- config/release references.

## Backup timing

Backup policy should support:

- periodic backups,
- pre-deployment backups,
- pre-migration backups,
- pre-rollback backups,
- post-incident backup preservation,
- manual backup before risky maintenance.

## Backup location

Backups should not live only beside the original DB forever.

A reasonable v1 approach may include:

- local backup directory on NUC,
- periodic export to separate drive or trusted storage,
- encrypted or access-controlled backup location,
- documented restore path.

Final mechanism belongs in setup/runbook and disaster-recovery implementation work.

## Backup security

Backups may contain sensitive operational state.

They must be protected against:

- casual deletion,
- casual reading,
- accidental upload,
- inclusion in prompts/screenshots,
- unencrypted storage on removable media where inappropriate.

## Restore testing

A backup that has never been restored is not fully trusted.

Before tiny live, test:

- create backup,
- restore to test location,
- open restored DB,
- verify schema/migration state,
- verify critical tables,
- start runtime in safe mode using restored copy in non-live test,
- confirm reconciliation requirement is preserved.

---

## Restore Policy

## Restore does not prove truth

Restoring a database or config does not prove current exchange state.

After any restore:

```text
reconciliation is mandatory before live resumption
```

## Restore from known-good backup

A backup is known-good only if:

- it is from an expected time,
- it passes integrity checks,
- it matches expected schema/migration,
- it was not taken after suspected corruption/compromise unless explicitly used for forensics,
- it is compatible with the release/config being run.

## Restore during exposure

Restoring runtime DB while live exposure exists is high risk.

If exposure exists:

- verify exchange state first,
- preserve/restore protection or flatten,
- restore DB only with operator awareness,
- reconcile after restore,
- treat mismatches as incident conditions.

## Restore after compromise

After host compromise, do not blindly restore local backups from the compromised host.

Use trusted backups or rebuild state from exchange truth and reviewed records.

---

## Credential Revocation and Rotation

## Revocation triggers

Revoke or disable credentials when:

- API key secret may have been exposed,
- key appears in logs/prompts/screenshots/git,
- unauthorized access suspected,
- host compromised or stolen,
- unexpected exchange activity appears,
- IP restriction fails unexpectedly,
- permission anomaly detected,
- operator no longer trusts credential storage.

## Rotation sequence

Recommended high-level sequence:

1. block live operation,
2. verify current exposure,
3. preserve or reduce exposure risk,
4. revoke old credential,
5. create new credential only on trusted path,
6. apply correct permissions,
7. apply IP restrictions where possible,
8. update secret storage,
9. test read-only behavior if appropriate,
10. test order-writing only in approved phase,
11. record audit event,
12. require operator review.

## No premature key creation

Production trade-capable keys should not be created during early development or before phase gates.

Key creation belongs at the approved setup/launch phase.

---

## Rebuild from Scratch

A full rebuild may be required after:

- host loss,
- host compromise,
- OS corruption,
- disk failure,
- repository tampering,
- unrecoverable dependency corruption.

## Rebuild sequence

High-level rebuild sequence:

1. prepare trusted host,
2. install supported OS,
3. apply host-hardening baseline,
4. create runtime user,
5. restore or clone trusted repository,
6. select approved release/commit,
7. install dependencies from lockfile,
8. restore approved config,
9. restore or recreate secrets safely,
10. restore runtime DB backup if trusted,
11. restore logs/audit exports if available,
12. configure service manager,
13. configure dashboard display,
14. configure alert routing,
15. start in safe mode,
16. verify observability,
17. reconcile exchange state,
18. run required tests,
19. operator approves or denies resumption.

## If runtime DB cannot be trusted

If DB cannot be restored safely:

- initialize new DB only after exchange state is known,
- record continuity-loss incident,
- import/reference available audit/log material if possible,
- treat any existing exposure as unsafe until reconciled.

---

## Recovery From Safe Clean State

A clean recovery may be possible when:

- no position exists,
- no open normal orders exist,
- no open algo orders exist,
- no unknown execution outcome exists,
- no credential compromise exists,
- runtime DB is restored or safely initialized,
- config and release are approved,
- dashboard and alerts are functional,
- reconciliation is clean.

Even then, the runtime should not skip safe-mode-first startup and reconciliation.

---

## Recovery With Open Protected Position

If a disaster occurs while a position is open but a protective stop is confirmed:

1. preserve the stop,
2. avoid unnecessary cancellation,
3. restore runtime safely,
4. reconcile position and stop,
5. confirm ownership,
6. confirm stop is valid and not stale,
7. resume only if management policy and operator approval allow.

If normal strategy trailing cannot be trusted after recovery, the system may keep protection and block normal progression until operator review.

---

## Recovery With Unprotected or Uncertain Position

If a position exists and protective stop is missing, rejected, stale, or uncertain:

```text
Severity 4 emergency / exposure-risk condition
```

Required response:

- block all new entries,
- attempt deterministic stop restoration only if state is clear,
- otherwise flatten if protection cannot be restored safely,
- preserve evidence,
- record incident,
- require operator review before resumption.

This is one of the most important disaster-recovery branches.

---

## Recovery After Credential Compromise With Open Position

This is a high-risk case.

Priorities:

1. verify current exchange position,
2. verify whether protective stop exists,
3. decide whether to preserve, restore, or flatten,
4. revoke compromised API key,
5. use trusted path for further actions,
6. rotate credentials,
7. rebuild host/secrets if needed,
8. review exchange account activity,
9. reconcile after new runtime is trusted,
10. require security and operator review before resumption.

If a compromised credential may still have trading permission, revocation should not be delayed for convenience.

---

## Recovery Verification Checklist

Before returning to live-capable operation after disaster, verify:

### Exchange state

- [ ] BTCUSDT position state known
- [ ] open normal orders known
- [ ] open algo/protective stops known
- [ ] no unknown execution outcome remains
- [ ] manual/non-bot exposure reviewed
- [ ] account mode and margin mode acceptable where relevant

### Protection

- [ ] no position exists, or
- [ ] position exists with confirmed valid protective stop, or
- [ ] position was flattened/contained according to policy

### Runtime

- [ ] Prometheus starts in safe mode
- [ ] runtime DB available and integrity checked
- [ ] config version verified
- [ ] release version verified
- [ ] migration state verified
- [ ] logs writable
- [ ] audit records writable
- [ ] dashboard visible
- [ ] alert routing tested

### Security

- [ ] credentials verified or rotated
- [ ] secret file permissions verified
- [ ] IP restrictions reviewed
- [ ] no suspected compromise remains unresolved
- [ ] Telegram/n8n tokens verified or rotated if affected

### Operations

- [ ] reconciliation completed
- [ ] incidents recorded
- [ ] operator actions recorded
- [ ] backup state reviewed
- [ ] rollback implications reviewed
- [ ] operator approval recorded if required

### Resumption

- [ ] no active kill switch unless intentionally still active
- [ ] no unresolved severe incident
- [ ] no unresolved operator-review requirement
- [ ] daily/drawdown lockouts respected
- [ ] deployment-stage gate still valid
- [ ] resumption explicitly approved where required

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical tasks should later be captured in:

```text
docs/09-operations/first-run-setup-checklist.md
```

### Backup setup

- choose runtime DB backup location,
- choose backup frequency,
- create backup script/procedure,
- test backup integrity,
- test restore into a safe location,
- decide whether external/removable backup is used.

### NUC recovery

- document how to power cycle NUC safely,
- document BIOS/auto-boot behavior,
- document UPS behavior if used,
- document how to access local dashboard after reboot,
- document how to inspect service status.

### Rebuild

- document OS reinstall path,
- document repo clone path,
- document dependency install path,
- document config restore path,
- document secrets restore/rotation path,
- document service setup path.

### Credentials

- document when Binance production keys may be created,
- document how to revoke compromised keys,
- document how to rotate keys,
- document how to verify permissions,
- document how to verify IP restrictions.

### Alerts and dashboard

- document Telegram/n8n restoration,
- document alert test messages,
- document dashboard restore test,
- document local monitor startup behavior.

### Emergency access

- document trusted secondary device for Binance account inspection,
- document emergency manual exchange verification,
- document emergency flatten decision path,
- document operator contact/availability assumptions.

---

## Forbidden Disaster-Recovery Patterns

The following are not allowed:

- resuming trading after disaster without reconciliation,
- assuming restored DB equals exchange truth,
- treating backup restore as incident clearance,
- creating new production API keys before host/secrets path is trusted,
- continuing with suspected credential compromise,
- running live after host compromise without rebuild/review,
- deleting audit logs to hide recovery complexity,
- overwriting corrupted DB without preserving a copy where practical,
- restoring from untrusted backup after suspected compromise,
- manually editing runtime DB to force healthy state,
- using Binance manually for discretionary trades during recovery,
- moving a protective stop farther away during emergency recovery,
- retrying exposure-changing orders blindly after timeout,
- auto-clearing kill switch or incidents after rebuild,
- bypassing dashboard/alert verification before tiny-live resumption,
- treating a local NUC reboot as harmless without state verification,
- storing backup files in public or unprotected locations,
- putting secrets into prompts, docs, screenshots, logs, or shell history.

---

## Testing Requirements

## Before paper/shadow

Test:

- runtime DB backup creation,
- restore into non-live test path,
- safe-mode-first startup,
- dashboard restart,
- alert test route,
- local service restart,
- reconciliation simulation,
- log/audit write path.

## Before tiny live

Test:

- NUC reboot behavior,
- power-loss or controlled reboot behavior where practical,
- runtime DB backup and restore,
- backup integrity check,
- safe-mode-first restart from restored DB,
- dashboard visible after restart,
- Telegram/n8n alert route after restart,
- secret file permission check,
- configuration hash/version check,
- outbound IP/API key restriction readiness,
- emergency local access,
- manual exchange inspection path from trusted device,
- incident/audit record after recovery drill.

## Before scaled live

Test or review:

- full host rebuild drill or documented dry run,
- credential rotation drill,
- alert-route failure drill,
- dashboard loss drill,
- database corruption simulation in non-live environment,
- restore from latest backup,
- operator response time,
- incident review from logs/audits,
- unresolved DR exceptions.

---

## Non-Goals

This document does not define:

- exact backup commands,
- exact restore commands,
- exact VPS/cloud setup,
- exact NUC OS install guide,
- exact systemd unit file,
- exact Binance UI workflow,
- exact Telegram/n8n setup,
- exact dashboard implementation,
- exact database migration code,
- or exact disaster-recovery automation scripts.

Those belong in setup/runbook and implementation documents.

---

## Acceptance Criteria

`disaster-recovery.md` is complete enough for v1 when it makes the following clear:

- disaster recovery prioritizes containment and state certainty over speed,
- exchange state is authoritative after any disaster,
- all recovery starts safe-mode-first,
- local database restore does not prove exchange truth,
- runtime DB corruption/loss blocks normal operation until reconciled,
- backup and restore must be tested before tiny live,
- credential compromise triggers revocation/rotation and security review,
- host loss or compromise requires trusted rebuild/review,
- the dedicated NUC model creates power, physical, router, and outbound-IP responsibilities,
- dashboard and alert recovery are part of operator readiness,
- manual Binance access is allowed only for emergency containment and must be reconciled,
- recovery with unprotected or uncertain position is a severity-4 emergency,
- recovery cannot clear kill switches, incidents, lockouts, or review requirements automatically,
- and practical setup/recovery steps are deferred to the first-run setup checklist.
