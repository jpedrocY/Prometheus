# Audit Logging

## Purpose

This document defines the audit-logging policy for the v1 Prometheus trading system.

Its purpose is to ensure that all safety-relevant human and system actions are:

- durable,
- timestamped,
- redacted,
- reviewable,
- attributable where practical,
- and usable for incident review, rollback review, release review, and operator accountability.

Audit logging exists because Prometheus is a supervised, safety-first trading system. The operator must be able to answer, after any important action:

- what changed,
- who or what caused the change,
- when it happened,
- why it was allowed,
- what state existed before the action,
- what state existed after the action,
- whether live exposure was open or possible,
- whether protection was confirmed,
- whether approval was required,
- and whether the action affected trading permission, risk, deployment, credentials, recovery, or emergency state.

Audit logs are part of the operational safety system.

They are not optional debug output.

---

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- v1 live scope: one symbol,
- one-way mode,
- isolated margin,
- one position maximum,
- one active protective stop maximum,
- supervised deployment,
- staged rollout from research to validation to paper/shadow to tiny live to scaled live,
- exchange state is authoritative,
- restart begins in safe mode,
- operator actions and recovery decisions must be reviewable.

This document covers audit requirements for:

- operator actions,
- runtime control changes,
- credential and secret-related events,
- configuration changes,
- risk setting changes,
- release and deployment changes,
- rollback actions,
- kill-switch actions,
- pause actions,
- approval and override workflows,
- recovery and reconciliation approvals,
- emergency flattening,
- incident lifecycle events,
- security-relevant events,
- audit retention,
- redaction,
- tamper-resistance expectations,
- backup/review/export expectations,
- and testing requirements.

This document does **not** define:

- the full observability event catalog,
- the complete runtime database schema,
- the final dashboard UI,
- host hardening steps,
- full disaster recovery procedure,
- or exact implementation commands.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/08-architecture/observability-design.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/state-model.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/rollback-procedure.md`
- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/release-process.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`
- `docs/10-security/permission-scoping.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/approval-workflows.md`
- `docs/11-interface/manual-control-actions.md`

### Authority hierarchy

If this document conflicts with secrets-management policy on secret handling, the secrets-management policy wins.

If this document conflicts with incident response on incident severity or emergency handling, the incident-response document wins.

If this document conflicts with the runtime database design on table names or schema implementation, the database-design document wins for schema details.

If this document conflicts with the internal event contracts on message envelope semantics, the internal-event-contracts document wins.

If this document conflicts with legal, regulatory, or exchange requirements introduced later, the stricter requirement should be reviewed and adopted before live use.

---

## Core Principles

## 1. Audit logs are safety records

Audit logs exist to preserve a reliable record of actions and decisions that affect system safety.

They are required for:

- accountability,
- incident review,
- rollback review,
- release review,
- emergency action review,
- security review,
- and live-stage promotion review.

## 2. Important actions must be durable before they are acknowledged

When an operator action changes safety state, the system should persist the audit event before telling the operator that the action succeeded.

Examples:

- enabling a pause,
- enabling a kill switch,
- clearing a kill switch,
- approving recovery,
- approving live enablement,
- requesting emergency flattening.

If persistence fails, the action must not be presented as successfully recorded.

## 3. Audit logs must not contain secrets

Audit logs must never store secret material.

They may record that a secret-related event occurred, but not the secret itself.

## 4. Audit logs must be reviewable

Audit logs must be structured enough that an operator can answer practical review questions without reading unstructured debug noise.

## 5. Audit logs must preserve denied and failed actions

Denied, rejected, failed, or aborted actions can be safety-relevant.

They must be auditable when they involve:

- trading permission,
- risk settings,
- credentials,
- recovery,
- emergency action,
- kill switch,
- rollback,
- deployment promotion,
- or operator approval.

## 6. Audit logs should connect cause and effect

Audit records should carry correlation and causation identifiers where practical.

This makes it possible to trace chains such as:

```text
operator approves recovery
→ reconciliation rerun starts
→ reconciliation classified clean
→ safe-mode exit allowed
→ runtime mode changes
```

## 7. Audit logging should fail safe

If an audit-critical action cannot be recorded, the system should block or fail the action unless the action is required for immediate capital protection.

If an emergency safety action must proceed despite audit-write failure, the system must raise an urgent alert and reconstruct the audit trail as soon as possible.

---

## Audit Logging Philosophy

Prometheus should not audit every technical event.

Audit logging should focus on events that matter for:

- safety,
- permission,
- accountability,
- security,
- recovery,
- release control,
- capital protection,
- and operator decision-making.

The audit log is not the same as a debug log.

The audit log should remain small enough and structured enough to review after:

- a paper/shadow session,
- a tiny-live session,
- an incident,
- a rollback,
- a security warning,
- a risk-setting change,
- or a live-stage promotion request.

---

## Audit Logs vs Runtime Events vs Debug Logs

Prometheus should distinguish three record types.

| Record type | Purpose | Example |
|---|---|---|
| Debug log | Developer troubleshooting | WebSocket reconnect retry detail |
| Runtime event | Operational state transition | `runtime.mode_changed` |
| Audit event | Reviewable control/security/action record | `kill_switch.cleared_by_operator` |

Some runtime events should also produce audit events.

Examples:

- kill switch activation,
- kill switch clearance,
- emergency flatten request,
- recovery approval,
- deployment promotion,
- rollback completion,
- configuration activation.

Not every runtime event should be an audit event.

Examples that usually do not require audit records by themselves:

- routine market-data tick processing,
- ordinary completed-bar publication,
- non-critical reconnect debug messages,
- ordinary dashboard polling,
- internal cache refresh events.

---

## Mandatory Audit Event Classes

Prometheus should support at least the following audit event classes.

```text
OPERATOR_ACTION
RUNTIME_CONTROL_CHANGE
CONFIG_CHANGE
RISK_SETTING_CHANGE
RELEASE_CHANGE
DEPLOYMENT_STAGE_CHANGE
CREDENTIAL_EVENT
SECRET_ACCESS_EVENT
SECURITY_EVENT
INCIDENT_EVENT
RECOVERY_EVENT
RECONCILIATION_EVENT
ROLLBACK_EVENT
EMERGENCY_ACTION
APPROVAL_EVENT
SYSTEM_STARTUP_SHUTDOWN
AUDIT_SYSTEM_EVENT
```

## `OPERATOR_ACTION`

Manual action initiated by an operator.

Examples:

- pause requested,
- kill switch enabled,
- recovery approved,
- emergency flatten requested,
- operator note recorded.

## `RUNTIME_CONTROL_CHANGE`

Change to runtime control state.

Examples:

- entries blocked,
- safe mode entered,
- safe mode exit approved,
- operator review required set or cleared.

## `CONFIG_CHANGE`

Change to non-risk runtime configuration.

Examples:

- adapter mode changed,
- dashboard bind address changed,
- alert route enabled,
- database path changed.

## `RISK_SETTING_CHANGE`

Change to risk or exposure settings.

Examples:

- risk fraction changed,
- leverage cap changed,
- notional cap changed,
- daily loss threshold changed,
- drawdown threshold changed.

## `RELEASE_CHANGE`

Change to deployed code or release version.

Examples:

- new release deployed,
- release rollback completed,
- dependency lockfile changed,
- migration version changed.

## `DEPLOYMENT_STAGE_CHANGE`

Change in operating stage.

Examples:

- dry-run promoted to paper/shadow,
- paper/shadow promoted to tiny live,
- tiny live demoted to paper/shadow,
- scaled live request denied.

## `CREDENTIAL_EVENT`

Event related to API credentials or credential policy.

Examples:

- key configured,
- key rotated,
- key revoked,
- permission check failed,
- IP restriction mismatch detected.

## `SECRET_ACCESS_EVENT`

Event related to secret loading or validation.

Examples:

- secret load succeeded,
- secret load failed,
- expected secret missing,
- secret file permissions invalid.

This must never include secret values.

## `SECURITY_EVENT`

Security-relevant system or account event.

Examples:

- repeated authorization failures,
- suspected credential compromise,
- unexpected trading permission detected,
- host access anomaly if implemented later.

## `INCIDENT_EVENT`

Incident lifecycle event.

Examples:

- incident opened,
- severity assigned,
- containment action recorded,
- incident resolved,
- post-incident review required.

## `RECOVERY_EVENT`

Recovery or repair action event.

Examples:

- recovery started,
- repair action attempted,
- protection restore attempted,
- recovery failed,
- recovery approved.

## `RECONCILIATION_EVENT`

Exchange/local state reconciliation event.

Examples:

- reconciliation started,
- mismatch found,
- mismatch classified,
- reconciliation classified clean,
- reconciliation classified unsafe.

## `ROLLBACK_EVENT`

Rollback-related event.

Examples:

- rollback requested,
- rollback target selected,
- rollback started,
- rollback completed,
- rollback blocked by live exposure,
- post-rollback reconciliation completed.

## `EMERGENCY_ACTION`

Emergency capital-protection action.

Examples:

- emergency unprotected-position branch entered,
- emergency stop restore attempted,
- emergency flatten requested,
- emergency flatten submitted,
- emergency flatten outcome unknown,
- emergency flatten confirmed.

## `APPROVAL_EVENT`

Approval or denial of an action that requires operator or governance approval.

Examples:

- tiny-live enablement approved,
- risk increase denied,
- kill-switch clearance approved,
- daily lockout override denied.

## `SYSTEM_STARTUP_SHUTDOWN`

Startup, shutdown, restart, or process lifecycle event relevant to safety.

Examples:

- process started,
- safe-mode startup entered,
- clean shutdown recorded,
- unclean restart detected,
- restart recovery required.

## `AUDIT_SYSTEM_EVENT`

Event concerning the audit system itself.

Examples:

- audit logging initialized,
- audit write failed,
- audit export generated,
- audit backup completed,
- audit redaction repair performed.

---

## Mandatory Audit Event Triggers

The system must emit audit records for the following trigger categories.

---

## Operator Control Triggers

Audit records are required for:

- operator pause enabled,
- operator pause clearance requested,
- operator pause cleared,
- kill switch enabled,
- kill switch clearance requested,
- kill switch cleared,
- recovery approved,
- recovery denied,
- restart requested,
- manual note recorded where supported,
- emergency flatten requested,
- emergency flatten confirmed by operator where applicable,
- emergency flatten submitted,
- emergency flatten result known or unknown.

### Required policy

Operator control actions must record:

- operator identity or actor label,
- action type,
- reason where provided or required,
- whether confirmation was required,
- current runtime mode,
- whether exposure existed or may have existed,
- whether protection was confirmed,
- result,
- and timestamp.

---

## Configuration Change Triggers

Audit records are required for changes to:

- runtime environment,
- adapter mode,
- exchange write capability,
- symbol scope,
- dashboard bind/interface settings,
- alert routing settings,
- runtime database path,
- log path,
- feature flags,
- data source configuration,
- reconciliation thresholds,
- stream staleness thresholds,
- stop-management configuration.

### Required policy

Configuration changes must record:

- previous config version,
- new config version,
- config hash where available,
- changed fields summary,
- operator or deployment actor,
- approval reference if required,
- activation time,
- and rollback reference where applicable.

Do not store full secret-bearing config files in the audit log.

---

## Risk Setting Change Triggers

Audit records are required for changes to:

- risk fraction,
- risk-usage buffer,
- max effective leverage,
- internal notional cap,
- daily warning threshold,
- daily lockout threshold,
- daily hard review threshold,
- drawdown thresholds,
- symbol exposure limits,
- manual override permissions,
- emergency flatten policy,
- approval workflow rules.

### Required policy

Risk-setting audit records must classify the change as:

```text
RISK_REDUCING
RISK_NEUTRAL
RISK_INCREASING
UNKNOWN_RISK_EFFECT
```

Risk-increasing changes require explicit approval.

A rollback to a previous config is still risk-increasing if the previous config allows higher risk than the current one.

---

## Release and Deployment Triggers

Audit records are required for:

- release deployment,
- release promotion,
- release rollback,
- dependency lockfile update,
- database migration start,
- database migration completion,
- database migration failure,
- deployment stage promotion,
- deployment stage demotion,
- paper/shadow enablement,
- tiny-live enablement,
- scaled-live enablement,
- live operation disablement.

### Required policy

Release/deployment audit records should include:

- release version,
- git commit hash where available,
- config version,
- database migration version,
- deployment stage,
- actor,
- approval reference,
- pre-deploy state,
- post-deploy state,
- and whether restart/reconciliation was required.

---

## Credential and Secret Triggers

Audit records are required for:

- expected secret missing,
- secret load failure,
- secret load success for live-capable mode,
- API key configured,
- API key validation passed,
- API key validation failed,
- API key permission mismatch,
- API key rotation recorded,
- API key revocation recorded,
- IP restriction mismatch,
- unexpected authorization failure pattern,
- suspected credential compromise,
- Telegram token configured or rotated,
- n8n webhook secret configured or rotated.

### Required policy

Credential and secret audit records must not include secret values.

They may include:

- secret alias,
- credential alias,
- hashed key identifier,
- permission summary,
- validation result,
- IP restriction status,
- created/rotated/revoked timestamp,
- and operator or system actor.

---

## Incident and Recovery Triggers

Audit records are required for:

- incident opened,
- incident severity assigned or changed,
- containment action taken,
- operator escalation triggered,
- incident acknowledged,
- incident resolved,
- incident reopened,
- post-incident review required,
- reconciliation started,
- reconciliation completed,
- mismatch classified,
- repair action attempted,
- repair action succeeded,
- repair action failed,
- emergency branch entered,
- recovery approved,
- recovery denied.

### Required policy

Incident and recovery audit records must preserve:

- incident ID,
- severity,
- class,
- exposure status,
- protection status,
- reconciliation status,
- actions taken,
- actor,
- and review requirement.

---

## Emergency Action Triggers

Audit records are required for:

- unprotected position detected,
- protective stop missing,
- protective stop uncertain,
- deterministic stop restore attempted,
- stop restore failed,
- emergency flatten path entered,
- emergency flatten requested,
- emergency flatten submitted,
- emergency flatten confirmed,
- emergency flatten outcome unknown,
- emergency action manually approved or denied.

### Required policy

Emergency audit events must be high priority and must be linked to incident records.

If an emergency action cannot be recorded before execution because immediate capital protection is required, the system should:

1. take the safety action if permitted by emergency policy,
2. raise an urgent audit-write-failure alert,
3. record a reconstructed audit entry as soon as persistence is restored,
4. require operator review before normal resumption.

---

## Startup, Shutdown, and Restart Triggers

Audit records are required for:

- process start,
- process stop if clean,
- unclean restart detected,
- safe mode entered on startup,
- persisted state loaded,
- startup prerequisite failure,
- credential validation failure,
- reconciliation required after startup,
- safe-mode exit allowed,
- safe-mode exit blocked.

### Required policy

Startup audit records must not imply that the system is safe merely because the process started.

Startup is not complete until required reconciliation and health checks pass.

---

## Required Audit Event Fields

Audit records should use a structured model compatible with the internal event envelope.

Minimum recommended fields:

```text
audit_event_id
audit_event_type
audit_event_class
occurred_at_utc_ms
recorded_at_utc_ms
operator_identity_or_system_actor
source_component
environment
deployment_stage
release_version
config_version
symbol
trade_reference
correlation_id
causation_id
pre_action_state_hash
post_action_state_hash
approval_reference
reason
result
severity
redaction_status
payload_json
created_at_utc_ms
```

## Field notes

### `audit_event_id`

Unique identifier for the audit event.

### `audit_event_type`

Specific action or event name.

Examples:

```text
operator.pause_enabled
kill_switch.clearance_requested
risk_config.changed
credential.validation_failed
rollback.completed
emergency_flatten.submitted
```

### `audit_event_class`

One of the mandatory audit event classes.

### `occurred_at_utc_ms`

Canonical UTC millisecond timestamp when the event occurred.

### `recorded_at_utc_ms`

Canonical UTC millisecond timestamp when the audit event was persisted.

### `operator_identity_or_system_actor`

Identity of the operator or system actor.

Examples:

```text
operator:local_admin
system:runtime
system:reconciliation
system:deployment
```

For early v1, this may be simple. Later versions may integrate stronger authentication.

### `source_component`

Component that emitted the audit record.

Examples:

```text
operator_control
incident_control
release_manager
secrets_loader
runtime_state
reconciliation_engine
```

### `environment`

Environment name.

Examples:

```text
LOCAL_DEV
DRY_RUN
PAPER_SHADOW
TINY_LIVE
SCALED_LIVE
```

### `deployment_stage`

Current deployment stage if different from environment.

### `release_version`

Release identifier or git commit reference where available.

### `config_version`

Active configuration version.

### `symbol`

Symbol when relevant. For v1 live operation, usually `BTCUSDT`.

### `trade_reference`

Trade lifecycle reference when relevant.

### `correlation_id`

Identifier tying related events together.

### `causation_id`

Identifier of the event or command that caused this event.

### `pre_action_state_hash`

Hash or summary hash of the relevant pre-action state where practical.

This is intended for review integrity, not for storing full state blobs.

### `post_action_state_hash`

Hash or summary hash of the relevant post-action state where practical.

### `approval_reference`

Identifier of the approval record, if approval was required.

### `reason`

Operator or system reason for the action.

Some actions should require a reason.

Examples:

- kill switch clearance,
- risk increase,
- live enablement,
- rollback,
- daily lockout override,
- emergency flatten.

### `result`

Outcome of the audited action.

Examples:

```text
SUCCEEDED
FAILED
DENIED
BLOCKED
PARTIAL
UNKNOWN
```

### `severity`

Severity or importance level.

Recommended values:

```text
INFO
WARNING
CRITICAL
EMERGENCY
```

### `redaction_status`

Status of payload redaction.

Recommended values:

```text
NO_SECRET_FIELDS
REDACTED
REDACTION_FAILED_BLOCKED
REDACTION_REPAIRED
```

### `payload_json`

Structured, redacted payload with event-specific data.

Must not contain secret material.

---

## Operator Action Audit Requirements

Every operator action that affects runtime control must be audited.

Required audit actions include:

```text
pause.enable
pause.clear_request
pause.clear
kill_switch.enable
kill_switch.clear_request
kill_switch.clear
recovery.approve
recovery.deny
restart.request
emergency_flatten.request
emergency_flatten.confirm
manual_note.record
```

## Confirmation requirements

If an action requires confirmation, the audit record should distinguish:

- requested,
- confirmed,
- executed,
- failed,
- denied,
- canceled.

Example sequence:

```text
operator.kill_switch_clear_requested
operator.kill_switch_clear_confirmed
runtime.kill_switch_cleared
```

## Operator reason requirements

A reason should be required for:

- kill switch clearance,
- recovery approval,
- risk increase,
- leverage cap increase,
- notional cap increase,
- deployment promotion to tiny live,
- deployment promotion to scaled live,
- emergency flatten,
- daily lockout override,
- drawdown pause clearance,
- rollback during live-capable stage.

---

## Configuration and Risk Change Audit Requirements

Configuration and risk changes must be auditable before activation.

## Required sequence

Recommended sequence:

```text
config change prepared
→ config diff summarized
→ approval checked if required
→ audit record written
→ config version activated
→ runtime state updated
→ activation audit record written
```

## Required fields for config/risk changes

At minimum:

- old config version,
- new config version,
- changed field summary,
- risk effect classification,
- approval reference if required,
- actor,
- activation timestamp,
- rollback target if available.

## Risk-increasing changes

Risk-increasing changes must not be activated without explicit approval.

Examples:

- increasing risk fraction,
- increasing leverage cap,
- increasing notional cap,
- weakening daily loss lockout,
- weakening drawdown pause,
- enabling production trade adapter,
- expanding symbol scope,
- disabling alert routing for live stage.

---

## Release and Rollback Audit Requirements

Release and rollback actions must leave durable audit trails.

## Release audit records

Required for:

- release prepared,
- release deployed,
- migration started,
- migration completed,
- config activated,
- post-deploy restart started,
- post-deploy reconciliation completed,
- release accepted,
- release rejected.

## Rollback audit records

Required for:

- rollback requested,
- rollback target selected,
- rollback preconditions checked,
- rollback blocked,
- rollback started,
- rollback completed,
- rollback failed,
- post-rollback safe-mode restart,
- post-rollback reconciliation,
- post-rollback operator approval.

## Rollback does not clear safety state

Audit records must make clear that rollback does not by itself clear:

- kill switch,
- incidents,
- operator review requirement,
- unknown execution outcome,
- reconciliation requirement,
- daily loss lockout,
- drawdown pause.

---

## Credential and Secret Event Audit Requirements

Credential and secret-related audit records must provide accountability without exposing secret values.

## Required audit events

Audit events are required for:

- credential configured,
- credential validation passed,
- credential validation failed,
- permission scope mismatch,
- IP restriction mismatch,
- credential rotated,
- credential revoked,
- suspected credential compromise,
- secret missing,
- secret load failed,
- secret file permission invalid,
- webhook secret configured or rotated.

## Allowed credential audit data

Allowed fields include:

- key alias,
- credential hash identifier,
- permission summary,
- IP restriction status,
- environment,
- created/rotated/revoked timestamp,
- validation result.

## Forbidden credential audit data

Forbidden fields include:

- API secret,
- full API key where unsafe,
- signed payload,
- authorization header,
- listen key,
- Telegram bot token,
- n8n webhook token,
- raw `.env` content,
- raw secret file content.

---

## Incident and Recovery Audit Requirements

Incident and recovery records must be audit-grade.

## Required incident audit fields

At minimum:

- incident ID,
- incident class,
- severity,
- status,
- opened timestamp,
- contained timestamp if applicable,
- resolved timestamp if applicable,
- exposure status,
- protection status,
- reconciliation status,
- actor,
- actions taken,
- review requirement.

## Required recovery audit fields

At minimum:

- recovery reason,
- recovery action,
- reconciliation ID where applicable,
- repair action attempted,
- repair outcome,
- operator approval reference if applicable,
- final runtime mode,
- entries blocked state.

## Unsafe mismatch handling

If reconciliation finds an unsafe mismatch, audit logs must preserve:

- mismatch class,
- affected symbol,
- exchange state summary,
- local state summary,
- active orders/protective stops summary,
- whether exposure exists,
- whether protection is confirmed,
- required next action.

---

## Emergency Action Audit Requirements

Emergency actions require the strongest audit trail.

## Required emergency audit fields

At minimum:

- emergency class,
- incident ID,
- symbol,
- trade reference if known,
- position side and size if known,
- protection state,
- action requested,
- action submitted,
- action confirmed or unknown,
- operator identity if manual,
- system actor if automatic,
- reason,
- result,
- post-action reconciliation requirement.

## Emergency flatten audit policy

Emergency flatten must produce audit records for:

1. emergency branch entered,
2. flatten requested or selected,
3. flatten approval/confirmation if required,
4. flatten order intent persisted,
5. flatten order submitted,
6. flatten outcome known/unknown,
7. position flat confirmation,
8. stale stop cleanup,
9. incident state after flatten.

If the flatten outcome is unknown, that uncertainty itself must be audited and must block normal resumption.

---

## Redaction and Secret-Handling Rules

## Absolute prohibition

Audit logs must never contain:

```text
API secrets
raw private keys
signed request payloads
authorization headers
listen keys
passwords
2FA codes
full .env contents
full secret files
unredacted webhook tokens
Telegram bot tokens
n8n webhook secrets
session cookies
SSH private keys
```

## Allowed redacted information

Audit logs may contain:

```text
credential alias
key identifier hash
permission summary
IP restriction enabled yes/no
secret loaded yes/no
secret validation passed/failed
redacted token alias
webhook route alias
last four characters only if approved safe
```

## Redaction failure policy

If the system cannot guarantee that an audit payload is redacted, it must not persist the unsafe payload.

Recommended behavior:

```text
persist minimal safe audit event
set redaction_status = REDACTION_FAILED_BLOCKED
raise alert
block non-emergency action if audit detail is required
```

## Screenshots and exported logs

Operators must not paste screenshots containing secrets into issue trackers, chats, or documentation.

Exported audit logs must be redacted before sharing outside the secure operating environment.

---

## Immutability and Tamper-Resistance Expectations

V1 does not require enterprise-grade immutable logging infrastructure before implementation begins.

However, v1 audit logs must still follow append-only discipline.

## Required v1 expectations

- audit events are append-only,
- audit events are not silently deleted,
- audit events are not casually edited,
- redaction repair must create a new audit event explaining the repair,
- audit tables/logs are included in backup planning,
- audit records are retained through incidents and rollbacks,
- audit write failures are themselves audit/security events where possible.

## Recommended v1 implementation

Recommended initial implementation:

```text
runtime DB audit/event tables
+ structured log export
+ local backups
+ optional off-host backup later
```

## Future upgrade path

Future versions may add:

- remote append-only log sink,
- immutable object storage,
- signed audit chain,
- SIEM integration,
- external alert audit stream,
- multi-operator identity provider integration.

These are future improvements, not v1 blockers unless deployment risk changes.

---

## Retention and Backup Expectations

## Retention principle

Audit logs should be retained long enough to support:

- incident review,
- daily and weekly reviews,
- release review,
- rollback review,
- security review,
- tiny-live promotion evidence,
- scaled-live promotion evidence.

## Minimum v1 retention recommendation

For early v1:

```text
retain audit records indefinitely unless explicitly archived
```

Because the system is narrow and low-volume in v1, storage pressure should not be a major concern.

## Backup requirement

Audit logs should be included in backup planning with the runtime database.

Backups must not expose secrets.

If backups contain audit payloads, the same redaction and access-control expectations apply.

---

## Review and Export Requirements

The system should support audit review for:

- operator actions,
- emergency actions,
- incidents,
- security events,
- release changes,
- risk-setting changes,
- rollback actions,
- live-stage promotions.

## Review filters

The operator should be able to filter or export audit records by:

- time range,
- event class,
- severity,
- operator/system actor,
- incident ID,
- trade reference,
- release version,
- config version,
- symbol.

## Export policy

Audit exports must be redacted.

Exports should include enough metadata to reconstruct context without exposing secrets.

Recommended export fields:

- event ID,
- event type,
- event class,
- timestamps,
- actor,
- environment,
- deployment stage,
- release/config version,
- correlation ID,
- related incident/trade/reconciliation IDs,
- result,
- redacted payload.

---

## Alerting Integration

Some audit events should also trigger alerts.

## Alert-worthy audit events

Examples:

- kill switch enabled,
- kill switch clearance requested,
- kill switch cleared,
- emergency flatten requested,
- emergency flatten submitted,
- unprotected position detected,
- credential validation failed,
- suspected credential compromise,
- production trade capability enabled,
- risk increased,
- leverage cap increased,
- live deployment promoted,
- rollback failed,
- audit write failure.

## Alert routing

Alert routing may include:

- dashboard alert panel,
- Telegram,
- n8n webhook,
- local logs.

Alert-routing details are defined in observability/interface/deployment documents.

Audit logging must ensure alert tokens and webhook secrets are not stored in audit payloads.

---

## Database and Storage Expectations

The runtime database design should provide durable storage for audit-relevant records.

Recommended audit-related storage categories:

- structured runtime events,
- operator action records,
- incident records,
- reconciliation records,
- exchange event records,
- release/config version records,
- audit event records if separated from runtime events.

## Append-only expectation

The audit stream should be append-only.

If current-state tables are updated, those updates should have corresponding audit/runtime events.

## State hashes

For important operator actions, the system should store pre-action and post-action state hashes where practical.

This is useful for review without storing huge snapshots.

## No secret storage

The audit database must not store secrets, signed request payloads, or unredacted credential material.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical setup topics should be handled later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

or a future concrete operator runbook.

They are recorded here so they are not forgotten.

## Future checklist items

- confirm audit logging is enabled in local development,
- confirm audit logging is enabled before paper/shadow,
- confirm audit logging is enabled before tiny live,
- identify runtime audit log/database location,
- verify audit records are written for operator pause and kill switch,
- verify audit records are written for recovery approval/denial,
- verify audit records are written for emergency flatten request path,
- verify audit records are written for config/risk/release changes,
- verify audit records are included in runtime database backups,
- verify logs do not contain API keys or secrets,
- verify Telegram/n8n tokens are redacted,
- test audit export for incident review,
- test audit review after paper/shadow session,
- test audit write failure behavior where practical,
- confirm operator identity labeling convention,
- confirm audit files/backups have appropriate file permissions,
- confirm audit logs survive service restart,
- confirm audit logs survive rollback.

No real Binance API keys should be created solely for audit-log testing before the correct phase gate.

---

## Testing Requirements

Audit logging must be tested.

## Unit tests

Required unit test categories:

- audit event creation uses required fields,
- audit event timestamps use UTC milliseconds,
- audit event class validation works,
- audit redaction removes forbidden fields,
- audit redaction blocks unsafe payloads,
- operator action audit records are generated,
- config/risk change audit records are generated,
- credential event audit records never include secret values,
- emergency action audit records include incident/correlation context.

## Integration tests

Required integration test categories:

- enabling pause creates audit record,
- clearing pause creates audit record,
- enabling kill switch creates audit record,
- kill-switch clearance request and clearance create audit records,
- recovery approval creates audit record,
- rollback request creates audit record,
- config activation creates audit record,
- risk increase requires approval audit reference,
- emergency flatten path creates required audit records,
- audit events persist across restart,
- duplicate exchange event does not duplicate audit side effects where not appropriate.

## Security tests

Required security test categories:

- API secrets are not written to audit logs,
- signed request payloads are not written to audit logs,
- listen keys are not written to audit logs,
- Telegram/n8n tokens are redacted,
- `.env` content is not dumped into audit logs,
- audit export is redacted.

## Failure tests

Required failure test categories:

- audit DB write failure blocks non-emergency operator control action,
- emergency action can proceed only under documented emergency policy if audit write fails,
- audit write failure raises alert,
- redaction failure does not persist unsafe payload,
- audit initialization failure blocks live-capable startup.

---

## Forbidden Patterns

The following patterns are forbidden.

## Secret leakage

Do not store:

- raw API secrets,
- signed payloads,
- authorization headers,
- listen keys,
- webhook tokens,
- full `.env` contents,
- full secret file contents.

## Silent audit deletion

Do not delete audit records silently.

If archival or redaction repair is required, it must be documented and audited.

## Unlogged operator control

Do not allow operator controls that change runtime safety state without audit records.

## Unlogged risk change

Do not activate risk-setting changes without audit records.

## Unlogged live enablement

Do not enable production trade capability without audit records and required approval.

## Audit as debug dumping ground

Do not dump large raw debug payloads into audit logs.

## Audit success without persistence

Do not tell the operator that an audit-critical action succeeded if the audit record failed to persist, except in a documented emergency exception.

## Rollback as audit erasure

Do not use rollback to erase audit history.

Rollback must preserve or explicitly carry forward audit and incident context.

---

## Non-Goals

This document does not require v1 to implement:

- enterprise SIEM integration,
- external immutable audit infrastructure,
- multi-user role-based access control,
- cryptographic audit-chain signing,
- legal/regulatory reporting automation,
- centralized cloud logging,
- or full forensic tooling.

Those may be added later if the project grows beyond the v1 supervised one-symbol scope.

---

## Acceptance Criteria

This document is satisfied when the implementation and related documentation ensure that:

- all safety-relevant operator actions create audit records,
- kill-switch, pause, recovery, rollback, and emergency actions are audited,
- config, risk, release, and deployment changes are audited,
- credential and secret events are audited without exposing secrets,
- incident and recovery lifecycle events are audit-reviewable,
- audit records use canonical UTC millisecond timestamps,
- audit records are correlated with relevant trades/incidents/reconciliation runs,
- audit logs are append-only in normal operation,
- audit logs are included in backup planning,
- audit exports are redacted,
- audit write failure is itself treated as a safety issue,
- audit behavior is covered by tests,
- and no secret material is stored in audit logs, runtime events, database records, or exported audit files.

