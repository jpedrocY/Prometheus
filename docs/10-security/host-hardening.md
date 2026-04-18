# Host Hardening

## Purpose

This document defines the host-hardening baseline for Prometheus live-capable operation.

Its purpose is to make clear what the machine running Prometheus must provide before the system is allowed to operate in paper/shadow, tiny-live, or scaled-live modes.

Prometheus is a safety-first, operator-supervised trading system. The host that runs it is therefore part of the trading safety boundary.

A weak, unstable, casually used, poorly monitored, or poorly secured host can invalidate otherwise good strategy, risk, execution, reconciliation, and incident-handling design.

This document defines the required posture for the default v1 live host:

```text
a dedicated local NUC / mini PC used only for Prometheus,
with an attached desk monitor showing the operator dashboard.
```

## Scope

This document applies to host security and operational hardening for Prometheus v1 under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- position mode: one-way mode,
- margin mode: isolated margin,
- one active strategy,
- one live symbol first,
- one open position maximum,
- one active protective stop maximum,
- supervised staged deployment,
- safe-mode-first restart,
- exchange state is authoritative,
- the operator dashboard is a core supervision surface,
- tiny-live default deployment runs on a dedicated local NUC / mini PC.

This document covers:

- stage-specific host requirements,
- the default local NUC deployment model,
- physical security,
- OS baseline,
- update policy,
- firewall baseline,
- SSH and local access policy,
- dedicated runtime user,
- process/service management,
- filesystem permissions,
- runtime database/log/backup protection,
- secrets file permissions,
- time synchronization,
- power and internet reliability,
- outbound IP stability,
- dashboard and monitor expectations,
- dependency update discipline,
- emergency access expectations,
- testing requirements,
- and forbidden host patterns.

This document does **not** define:

- exact shell commands,
- full Linux installation steps,
- exact systemd unit content,
- exact firewall commands,
- exact dashboard implementation,
- Binance API key creation steps,
- full disaster recovery procedure,
- or the final first-run operator checklist.

Those practical steps should be defined later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

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
- `docs/10-security/disaster-recovery.md`
- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/dashboard-metrics.md`
- `docs/11-interface/alerting-ui.md`
- `docs/12-roadmap/phase-gates.md`

### Authority hierarchy

If this document conflicts with secrets-management policy, the secrets-management policy wins for secret storage details.

If this document conflicts with permission-scoping policy, the permission-scoping policy wins for exchange/API permission rules.

If this document conflicts with disaster recovery, the disaster-recovery document wins for restore and rebuild procedures.

If this document conflicts with the deployment model on environment boundaries, the deployment model wins.

If this document conflicts with the operator dashboard requirements on dashboard role and controls, the dashboard/interface documents win.

---

## Core Principles

## 1. The host is part of the trading safety boundary

The runtime host is not a neutral container.

It holds or accesses:

- runtime configuration,
- runtime database,
- logs,
- audit records,
- alert routing configuration,
- dashboard access,
- possibly exchange credentials,
- and process control.

A compromised or unstable host can create capital risk.

## 2. The default tiny-live host is a dedicated local NUC / mini PC

For v1 tiny-live, the preferred deployment target is:

```text
Dedicated local NUC / mini PC
Used only for Prometheus
Physically controlled by the operator
Connected to a desk monitor
Running the operator dashboard during operation
```

The key requirement is dedication and control, not cloud hosting.

A VPS may be considered later as an alternative deployment model, but it is not the default v1 assumption.

## 3. The host must not be a general-purpose personal computer

A live-capable Prometheus host must not be used for:

- casual browsing,
- gaming,
- unrelated coding experiments,
- personal file storage,
- discretionary exchange trading,
- unrelated bots,
- downloading untrusted software,
- or general daily computing.

The machine should exist to run and supervise Prometheus.

## 4. The local monitor is part of operator readiness

The attached desk monitor should display the Prometheus operator dashboard whenever the monitor is on during operation.

The dashboard should provide a clear, always-available view of:

- runtime mode,
- entries allowed / blocked state,
- open position state,
- protective stop state,
- open normal orders,
- open algo/protective stop orders,
- user-stream and market-data health,
- reconciliation state,
- incidents and alerts,
- daily loss state,
- drawdown state,
- recent critical events,
- and operator action requirements.

The dashboard may be visually polished and Binance-like in information density, but it must remain a supervision and control surface, not a discretionary trading terminal.

## 5. Physical access matters

A local NUC is physically reachable.

That is useful for emergency access, but it also creates a physical security responsibility.

The operator must control who can access the machine, keyboard, monitor, local session, and removable media.

## 6. Safe-mode-first restart remains mandatory

A hardened host may restart the Prometheus process automatically after a crash or reboot.

That is acceptable only because Prometheus itself must always restart into safe mode, reload local state as provisional, reconcile exchange state, and block new entries until required gates pass.

No host-level auto-start behavior may bypass runtime safe-mode-first logic.

## 7. Secrets must remain protected on disk, in memory, and in logs

Secrets must not be stored in git, docs, prompts, screenshots, runtime DB records, audit logs, or unredacted application logs.

Host-hardening must protect:

- Binance API keys and secrets,
- Telegram bot tokens,
- n8n webhook URLs or secrets,
- dashboard admin credentials,
- SSH private keys,
- `.env` files,
- and any local credential material.

## 8. Operational reliability is a security concern

For a trading system, power loss, unstable internet, broken time sync, missing backups, or inaccessible alerts can become safety problems.

The host must be reliable enough for the selected deployment stage.

---

## Stage-Specific Host Requirements

## Local Development

Purpose:

```text
Develop and test Prometheus safely with no production trade-capable credentials.
```

Host requirements:

- can be a developer workstation,
- may use fake adapters and test fixtures,
- may use local sample databases,
- must not store production Binance trade-enabled credentials,
- must not be treated as the live trading host,
- must keep test secrets separate from production secrets.

Local development is not live operation.

## Validation / Research

Purpose:

```text
Run historical data preparation, backtests, reports, and validation workflows.
```

Host requirements:

- sufficient disk for historical data,
- clear separation from live runtime database,
- no production trade-capable credentials required,
- reproducible data paths,
- ability to run tests and validation reports.

Validation/research may share the dedicated NUC only if it does not interfere with live runtime operation. Once the NUC is promoted to live-capable operation, unrelated heavy research workloads should be avoided on that machine during operation.

## Dry-Run Runtime

Purpose:

```text
Run live-like orchestration without real exchange order-writing capability.
```

Host requirements:

- local runtime DB and logs behave similarly to production,
- fake/simulated exchange adapter or read-only data paths,
- dashboard/status display tested,
- alert routing may be tested,
- no production order-writing keys.

Dry-run is a rehearsal for runtime behavior, not capital exposure.

## Paper / Shadow

Purpose:

```text
Run live-like supervision, alerting, and runtime state handling without real capital exposure.
```

Host requirements:

- dedicated NUC preferred,
- dashboard should be visible on monitor,
- alert routing should be configured and tested,
- runtime logs and DB should persist across restarts,
- safe-mode-first restart should be tested,
- backup behavior should be tested,
- no production trade-enabled keys unless explicitly required for read-only exchange state and approved.

Paper/shadow should prove operational supervision before tiny live.

## Tiny Live

Purpose:

```text
First real-capital operation with conservative risk and strict supervision.
```

Host requirements:

- dedicated local NUC / mini PC used only for Prometheus,
- controlled physical access,
- stable power and internet,
- time synchronization verified,
- runtime process managed by service manager or equivalent,
- local dashboard visible on attached monitor,
- alert routing tested,
- runtime DB/log/audit paths protected,
- backups prepared and restore-tested,
- secrets stored securely,
- API key permission and IP restriction readiness verified,
- emergency access tested,
- safe-mode-first restart tested,
- rollback and incident procedures understood.

Tiny live must not begin on an unprepared host.

## Scaled Live

Purpose:

```text
Larger live operation after evidence and approval.
```

Host requirements:

- all tiny-live requirements,
- stronger backup/review discipline,
- stricter access review,
- improved monitoring,
- stronger audit/export process,
- confirmed operator availability model,
- reviewed dependency/update process,
- no unresolved security or operational incidents.

Scaled live is not just tiny live with larger risk.

---

## Default Local NUC Deployment Model

## Physical role

The default v1 live host is a dedicated local NUC / mini PC placed in a controlled location.

It should be connected to:

- power,
- network,
- desk monitor,
- keyboard/mouse for local emergency access where appropriate,
- optional UPS,
- and optionally local network access for maintenance.

## Usage policy

The NUC should be used only for Prometheus-related operation.

Allowed use:

- Prometheus runtime,
- operator dashboard,
- Prometheus logs/status,
- approved maintenance,
- approved updates,
- backups,
- deployment/release actions,
- incident response.

Forbidden use:

- general web browsing,
- social media,
- gaming,
- personal email,
- unrelated coding experiments,
- unrelated bots,
- discretionary exchange trading,
- downloading untrusted software,
- exposing secrets to screenshots/prompts,
- using the monitor as a casual trading workstation.

## Monitor policy

The attached monitor is intended to show the Prometheus dashboard.

The dashboard should be available whenever the monitor is turned on during operation.

The display may show:

- high-level system status,
- charts and strategy context,
- open positions,
- open orders,
- protective stops,
- PnL and risk metrics,
- logs/events,
- alerts,
- exchange connectivity state,
- and required operator actions.

The display must not expose secrets.

If the dashboard has manual controls, they must remain limited to approved operational controls such as pause, kill switch, recovery approval, and emergency actions defined elsewhere.

It must not provide unrestricted manual order-entry features.

---

## Physical Security

## Required physical controls

For tiny-live and above, the NUC should be kept in a controlled environment.

Minimum expectations:

- operator knows where the machine is,
- casual third-party access is prevented,
- screen is locked when unattended if local session exposes controls,
- terminals should not display secrets,
- removable media use is controlled,
- keyboard/mouse access is operator-controlled,
- emergency physical access remains possible.

## Full-disk encryption

Full-disk encryption should be considered for the dedicated NUC, especially if the machine could be stolen or accessed by others.

Tradeoff:

- encryption improves protection of local files at rest,
- but may complicate unattended reboot after power loss.

If full-disk encryption is used, the operator must understand how Prometheus behaves after reboot and how safe-mode-first restart is preserved.

If full-disk encryption is not used, filesystem permissions, physical access control, and backup security become even more important.

## Screen/session locking

The operator dashboard may be visible during operation, but privileged shells, secret files, admin consoles, or exchange accounts must not remain open and visible.

If dashboard controls can trigger safety-relevant actions, the dashboard should include appropriate confirmations and access controls.

---

## Power and Internet Reliability

## Power reliability

The NUC should use stable power.

For tiny live and above, a UPS is strongly recommended.

The purpose of a UPS is not to keep trading during all possible outages. It is to:

- reduce abrupt shutdowns,
- allow controlled shutdown where possible,
- protect runtime DB integrity,
- give the operator time to respond,
- and reduce restart/recovery incidents.

## Power-loss behavior

The operator should decide and document host behavior after power restoration.

Possible host BIOS/firmware behavior:

- remain off after power loss,
- power on automatically after power returns.

Either can be acceptable only if Prometheus runtime behavior remains safe.

If the NUC auto-boots after power returns:

```text
Prometheus must still start in SAFE_MODE.
```

Auto-boot must not mean auto-trade.

## Internet reliability

The NUC should use the most stable available connection.

Preferred:

- wired Ethernet to the router,
- reliable router,
- stable ISP connection.

Avoid relying on unstable Wi-Fi where possible.

If internet connectivity is lost:

- market data may become stale,
- user stream may become unavailable,
- REST reconciliation may fail,
- alerts may fail,
- and exchange-state confidence may be reduced.

Prometheus must block new entries and enter appropriate recovery behavior when connectivity affects safety.

## Router reliability

Because the NUC is local, the router and local network are part of operational reliability.

Before tiny live, the operator should know:

- router location,
- power dependency,
- whether router is on UPS,
- whether ISP outages are common,
- whether public IP changes unexpectedly,
- whether local network access to dashboard is stable.

---

## Supported Host and OS Baseline

## Operating system

For live-capable deployment, the NUC should run a supported operating system with active security updates.

Recommended direction:

```text
A stable Linux distribution suitable for long-running services.
```

Examples that may be considered:

- Ubuntu Server LTS,
- Debian stable,
- another explicitly supported Linux environment.

The final choice should prioritize:

- stability,
- security update availability,
- service management,
- ease of backup,
- predictable Python/runtime behavior,
- operator familiarity.

Unsupported or end-of-life operating systems are not acceptable for live operation.

## Desktop vs server environment

Because the NUC has an attached monitor showing the dashboard, a minimal desktop environment may be acceptable.

However:

- the desktop should not become a general-purpose workstation,
- browser exposure should be minimized,
- unnecessary software should be avoided,
- auto-login should be reviewed carefully,
- and local UI convenience must not weaken secrets or controls.

A possible model:

```text
Server-style hardened host
+ local dashboard browser/session
+ limited administrative use
```

## Host identity

The live host should have a clear identity, such as:

```text
prometheus-nuc
```

This helps distinguish it from development machines and reduces operator confusion.

---

## Operating System Update Policy

## Security updates

Security updates should be applied promptly after basic compatibility review.

The update process should respect:

- current exposure state,
- runtime DB backup state,
- operator availability,
- restart procedure,
- rollback procedure.

## Reboot-requiring updates

If updates require reboot:

1. verify no unknown execution outcome exists,
2. verify exposure/protection state,
3. prefer flat state where possible,
4. activate pause or safe mode as appropriate,
5. stop/restart through approved process,
6. allow Prometheus to restart in safe mode,
7. reconcile before resumption.

## Package updates

Do not casually update packages on a live-capable host during active operation.

Package changes that may affect Prometheus should go through release discipline.

This includes:

- Python versions,
- dependency manager versions,
- Binance client libraries,
- WebSocket libraries,
- database drivers,
- serialization libraries,
- dashboard dependencies.

## Unsupported system state

If the host is missing security updates, running unsupported software, or has unclear package state, tiny-live promotion should be blocked until reviewed.

---

## Firewall Baseline

## Default policy

Live-capable host firewall posture should be:

```text
deny unsolicited inbound traffic by default
allow only explicitly required inbound access
```

Allowed inbound access should be minimal.

Potential inbound needs:

- local SSH from approved operator machine,
- local dashboard access if dashboard is accessed from another device,
- no public database access,
- no public debug server,
- no broad development ports.

## Dashboard exposure

The dashboard should not be exposed publicly without explicit security design.

Recommended v1 default:

```text
Dashboard visible locally on the NUC monitor
and optionally available only on the trusted local network.
```

If remote dashboard access is later required, it must be designed deliberately with authentication, transport security, and audit logging.

## Outbound access

Outbound access must allow approved connections required for:

- Binance public/private APIs,
- package updates during maintenance,
- Telegram/n8n alert routing if enabled,
- time synchronization,
- approved backup/export destinations if used.

Outbound access should not be used as an excuse to run unrelated network services on the host.

---

## SSH Access Policy

## Purpose

SSH may be useful for maintenance, deployment, logs, and emergency diagnosis.

For a local NUC, SSH is optional but recommended if managed safely.

Primary operator supervision is the local dashboard/monitor. SSH is a maintenance path, not the normal trading interface.

## Requirements

For tiny-live and above:

- use key-based SSH authentication where possible,
- avoid direct root login for routine use,
- restrict SSH access to approved operators,
- avoid shared operator accounts,
- protect private SSH keys,
- do not store SSH private keys in the repo,
- do not paste SSH keys into prompts/docs,
- keep an emergency access method documented.

Password-based SSH should be avoided for production-like operation unless explicitly justified and controlled.

## Local login

Local login should be restricted to approved operator/admin accounts.

If auto-login is enabled for dashboard convenience, it must not expose admin shells, secrets, or unrestricted controls.

---

## Operator Account Policy

## Separate identities

The host should distinguish between:

- administrative user,
- Prometheus runtime user,
- dashboard/operator user where applicable.

The runtime process should not run under the everyday administrative user.

## Shared accounts

Shared accounts should be avoided where possible.

If only one operator exists initially, the account model can remain simple, but it should not prevent later auditability.

## Least privilege

Each account should have only the permissions it needs.

Examples:

- admin account can maintain the host,
- runtime user can run Prometheus and access runtime files,
- dashboard user can view/control through approved interface,
- no account should casually expose secrets or runtime DB write access unless needed.

---

## Dedicated Runtime User

## Requirement

Prometheus should run under a dedicated least-privilege OS user.

Example conceptual identity:

```text
prometheus
```

The exact username may differ, but the role must be clear.

## Runtime user may access

The runtime user may access:

- Prometheus application directory,
- runtime database path,
- runtime log path,
- configuration files required by the runtime,
- secret files required by the runtime,
- backup output path where required,
- historical data read paths where required.

## Runtime user should not access

The runtime user should not have broad access to:

- `/root`,
- admin SSH keys,
- unrelated user home directories,
- unrelated secrets,
- system package manager,
- arbitrary writable system directories,
- unrelated application data.

## Root avoidance

Prometheus runtime should not run as root.

If a privileged operation is required, it should be handled by system configuration, not by granting the trading runtime broad root privileges.

---

## Process and Service Management

## Managed service expectation

For paper/shadow, tiny live, and scaled live, Prometheus should run under an explicit process/service management model.

For a Linux NUC, this will likely mean a service manager such as systemd.

The service definition should specify:

- runtime user,
- working directory,
- environment/config file path,
- restart behavior,
- log handling,
- dependency on network readiness where appropriate,
- resource limits where useful,
- and safe shutdown behavior.

## Automatic restart

Automatic restart may be allowed after crash.

However:

```text
automatic process restart must not mean automatic trading resumption
```

Prometheus must still:

- start in safe mode,
- load local state as provisional,
- initialize logs/observability,
- restore streams where applicable,
- reconcile exchange state,
- and require required gates before normal operation.

## Manual start/stop

The operator should have a documented way to:

- start service,
- stop service,
- check service status,
- inspect logs,
- perform controlled restart,
- identify last restart reason.

Exact commands belong in the first-run setup checklist.

---

## Service Sandboxing Expectations

Service sandboxing should be used where practical, but not in a way that breaks required runtime behavior.

Potential protections to evaluate:

- no new privileges,
- restricted writable directories,
- private temporary directory,
- read-only system paths,
- explicit environment file,
- limited home directory access,
- controlled restart behavior.

Sandboxing must still allow:

- runtime DB writes,
- log writes,
- backup writes if performed by service,
- network access to Binance and alert endpoints,
- reading approved config and secret files,
- dashboard serving if embedded.

The sandbox policy should be tested before tiny live.

---

## Time Synchronization

## Requirement

Live hosts must have working time synchronization.

Prometheus depends on accurate time for:

- UTC millisecond timestamps,
- signed exchange requests,
- bar-close logic,
- stream freshness checks,
- event ordering,
- audit logs,
- reconciliation timing,
- incident timelines.

## Startup check

Prometheus should verify clock/time-sync health during startup where practical.

If clock health is unknown, degraded, or obviously wrong:

```text
live operation should remain blocked
```

## Canonical time

Application logic and persisted timestamps remain UTC Unix milliseconds.

The dashboard may display local time for operator convenience, but canonical state must use UTC.

---

## Filesystem Layout and Permissions

## Conceptual production paths

For the dedicated NUC, exact paths may vary, but the host should separate:

```text
application code
configuration
secrets
runtime database
logs
backups
historical data
reports
```

Example conceptual layout:

```text
/opt/prometheus/             # application checkout or release
/etc/prometheus/             # non-secret config
/etc/prometheus/secrets/     # secret files, restricted
/var/lib/prometheus/         # runtime DB and persistent state
/var/log/prometheus/         # logs
/var/backups/prometheus/     # backups
/data/prometheus/            # historical/research data if stored locally
```

The final layout should be decided in setup/runbook work.

## Permission principles

- runtime DB directory must not be world-writable,
- log directory must not be world-writable,
- secret directory must be readable only by required identities,
- backup directory must be protected,
- application code should not be casually writable by runtime process unless required,
- temporary directories must not hold durable runtime state.

## Temporary storage prohibition

Runtime DB, active audit logs, active incident records, and important backups must not be stored only in temporary directories.

---

## Runtime Database, Logs, and Backup Permissions

## Runtime DB

The runtime database is a safety artifact.

It stores restart-critical local state, audit events, incidents, orders, protection records, reconciliation results, and operator actions.

The runtime DB should be:

- on durable local storage,
- protected from casual deletion,
- backed up according to disaster-recovery policy,
- readable/writable by the Prometheus runtime user,
- not world-readable,
- not edited manually during operation.

## Logs

Logs and audit exports should be:

- durable enough for incident review,
- protected from casual deletion,
- rotated safely,
- redacted,
- included in backup/review planning where appropriate.

## Backups

Backup files may contain sensitive operational state.

They should be protected similarly to runtime DB files.

Before tiny live, backup creation and restore validation should be tested.

Backups must not contain unredacted secrets unless explicitly designed and protected for that purpose.

---

## Secrets File Permissions

## Secret storage

Secrets should be stored outside git and outside normal docs.

Possible local pattern:

```text
restricted .env or secret file read by runtime service
```

The exact mechanism belongs to secrets-management and first-run setup.

## Required protections

Secret files should:

- be readable only by required runtime/admin identities,
- not be world-readable,
- not be copied into logs,
- not be committed,
- not be sent to AI prompts,
- not be included in screenshots,
- not be printed at startup.

## Secret categories

Treat all of the following as secrets:

- Binance API key,
- Binance API secret,
- Telegram bot token,
- Telegram chat IDs if sensitive,
- n8n webhook URL/token,
- dashboard admin credential,
- SSH private keys,
- backup encryption keys,
- any future database credential.

## Shell history risk

Operators must avoid pasting or exporting production secrets in ways that persist in shell history.

This should be addressed practically in the first-run setup checklist.

---

## Outbound IP Stability and Exchange Access

## Why this matters

Production Binance API keys should use IP restriction where possible.

A dedicated local NUC may run behind a home/office internet connection whose public IP may change.

This is a critical readiness item before creating production trade-capable API keys.

## Required check

Before tiny-live production keys are created, the operator must determine whether the NUC's outbound public IP is stable enough for API key IP restriction.

Possible solutions include:

- static IP from ISP,
- fixed VPN egress,
- dedicated secure egress host,
- other approved network design.

No solution should be adopted casually, because network indirection can create new failure modes.

## Security exception

Running production trade-capable keys without IP restriction should be treated as a security exception requiring explicit approval and documentation.

It should not be the default plan.

---

## Dependency and Package Update Policy

## No ad hoc live changes

Do not make unreviewed dependency or package changes directly on the live-capable host during active operation.

Examples of risky live changes:

- upgrading Python during live runtime,
- changing dependency lockfiles on the host,
- installing random packages,
- changing WebSocket libraries,
- changing Binance API wrappers,
- modifying database drivers,
- modifying dashboard dependencies.

## Required update path

Dependency changes should follow:

1. local development test,
2. dry-run validation,
3. relevant unit/integration tests,
4. release process,
5. planned deployment,
6. safe-mode-first restart,
7. reconciliation where applicable,
8. operator review if required.

## System package updates

Security and OS updates are required, but should still be managed deliberately.

For tiny-live and above, updates requiring reboot should be treated as maintenance events.

---

## Dashboard and Alert Access Requirements

## Dashboard role

The dashboard is the primary local supervision surface.

It should be visible on the attached monitor during operation.

It should show high-value operational information clearly, including:

- runtime mode,
- entries allowed/blocked,
- current deployment stage,
- current symbol,
- position side/size/notional,
- open normal orders,
- open algo/protective stop orders,
- protective stop status,
- stop trigger price,
- user-stream health,
- market-data health,
- exchange connectivity,
- reconciliation state,
- incidents,
- alerts,
- daily loss state,
- drawdown state,
- recent important events,
- operator action required.

## Dashboard safety boundary

The dashboard must not become a discretionary trading interface.

Forbidden dashboard capabilities for v1:

- arbitrary manual entry orders,
- arbitrary manual limit/market trading,
- casual leverage changes,
- casual risk increases,
- discretionary stop widening,
- bypassing kill switch or reconciliation,
- hiding unresolved incidents to show a false healthy state.

Allowed dashboard controls should be limited and audited, such as:

- pause,
- kill switch,
- recovery approval,
- emergency flatten workflow,
- acknowledgement of alerts,
- operator notes,
- controlled resumption where policy allows.

## Alert routing

For paper/shadow and tiny-live stages, alert routing should be tested.

Supported alert channels may include:

- dashboard alerts,
- Telegram,
- n8n webhook route,
- local logs.

Tokens and webhook secrets must be treated as secrets.

Alert tests should include at minimum:

- normal warning,
- critical exposure/protection alert,
- incident alert,
- kill-switch alert,
- alert-route failure or degraded status where practical.

---

## Monitoring and Health Checks

The host and runtime should expose enough health information to determine whether operation is safe.

Important host-level checks:

- disk space,
- runtime DB path writable,
- log path writable,
- backup path writable,
- time sync healthy,
- network connectivity,
- alert route reachable,
- service running,
- dashboard reachable,
- CPU/memory within acceptable range,
- system reboot or crash detected.

Host monitoring does not replace Prometheus state monitoring.

The key operator question remains:

```text
Can the bot's exposure, protection, and recovery state be trusted?
```

---

## Emergency Access Requirements

## Local emergency access

Because the default host is a local NUC, physical emergency access is available and should be preserved.

The operator should know how to:

- view dashboard locally,
- check whether service is running,
- stop service if needed,
- access logs,
- trigger approved kill switch/emergency controls,
- power down safely if required,
- recover after reboot.

Exact steps belong in the first-run setup checklist and disaster-recovery documents.

## Remote emergency access

Remote access is optional but useful.

If enabled, it must be restricted and secured.

Remote access should not weaken the host baseline.

## Emergency access does not bypass policy

Emergency access should support safety actions, not discretionary trading.

Even in emergency mode, actions should be logged and reconciled where possible.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical tasks should be included later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

They are not implemented by this document.

### Host preparation

- choose and prepare the dedicated NUC / mini PC,
- install supported OS,
- set host identity,
- configure local monitor/dashboard startup,
- configure keyboard/mouse/emergency local access,
- decide desktop vs server environment.

### Access and security

- create admin/operator account,
- create dedicated Prometheus runtime user,
- configure SSH if used,
- configure firewall,
- disable unnecessary services,
- configure screen/session lock,
- review physical security.

### Filesystem

- create application directory,
- create config directory,
- create secrets directory,
- create runtime DB directory,
- create log directory,
- create backup directory,
- create data/research directory if used locally,
- apply permissions.

### Runtime setup

- install Python/tooling,
- clone repository,
- install dependencies,
- initialize local/runtime database,
- configure environment files,
- configure service manager,
- test start/stop/status/log access.

### Reliability

- verify time synchronization,
- verify power/UPS behavior,
- verify internet/router stability,
- verify outbound public IP,
- decide API key IP restriction approach,
- test reboot behavior.

### Alerts and dashboard

- configure dashboard local display,
- configure Telegram/n8n alert routes,
- verify secrets are not logged,
- test warning and critical alerts,
- verify dashboard always-visible use case.

### Backup and recovery

- configure backup path,
- test runtime DB backup,
- test restore procedure,
- verify logs/audit export,
- document emergency access.

### Phase readiness

- confirm no production secrets in local dev,
- confirm paper/shadow readiness,
- confirm tiny-live host baseline,
- confirm production key creation should occur only at approved phase.

---

## Forbidden Host Patterns

The following patterns are not allowed for tiny-live or scaled-live operation:

- running Prometheus on a general-purpose personal laptop,
- running Prometheus on a gaming/work desktop used for unrelated tasks,
- running the live runtime as root,
- storing production secrets in git,
- storing production secrets in screenshots/prompts,
- keeping production keys in shell history,
- exposing the dashboard publicly without explicit security design,
- exposing the runtime database over the network,
- using world-writable runtime DB/log directories,
- storing runtime DB only in a temporary folder,
- running unsupported/EOL operating systems,
- disabling time sync,
- ignoring outbound IP instability for IP-restricted keys,
- continuing tiny-live when dashboard/critical alerts are broken,
- applying unreviewed dependency changes directly on the live host,
- auto-resuming trading after reboot without safe-mode/reconciliation,
- using the monitor/dashboard as a discretionary manual trading terminal,
- hiding or deleting audit logs to make state appear cleaner.

---

## Testing Requirements

Host-hardening requirements should be testable before paper/shadow and tiny-live.

## Required tests before paper/shadow

- runtime can start and stop cleanly,
- runtime DB path is writable,
- log path is writable,
- dashboard can be displayed on monitor,
- alert route can send test notification,
- safe-mode-first startup is visible,
- no production trade-enabled credentials are required.

## Required tests before tiny live

- dedicated NUC is used only for Prometheus,
- physical access is controlled,
- supported OS and updates are verified,
- firewall policy is reviewed,
- runtime user is least-privilege,
- secrets file permissions are verified,
- runtime DB/log/backup permissions are verified,
- time synchronization is verified,
- service restart behavior is verified,
- safe-mode-first restart is verified,
- dashboard is visible on monitor,
- dashboard does not expose secrets,
- alert routing is tested,
- backup creation is tested,
- restore process is tested at least once,
- outbound IP/API key restriction plan is verified,
- emergency local access is tested,
- no unrelated services or workloads are present.

## Required tests before scaled live

- tiny-live host behavior reviewed,
- incident history reviewed,
- backup/restore review passed,
- alerting reliability reviewed,
- operator access model reviewed,
- dependency/update process reviewed,
- no unresolved security exceptions,
- no unresolved host-hardening exceptions.

---

## Non-Goals

This document does not define:

- exact Linux commands,
- exact systemd unit files,
- exact firewall configuration syntax,
- exact OS installation process,
- exact dashboard frontend implementation,
- exact Binance API key creation workflow,
- exact Telegram/n8n setup workflow,
- full disaster-recovery rebuild procedure,
- or final scaled-live infrastructure design.

Those belong in setup, security, interface, and operations documents.

---

## Acceptance Criteria

`host-hardening.md` is complete enough for v1 when it makes the following clear:

- the default tiny-live host is a dedicated local NUC / mini PC,
- the NUC is used only for Prometheus,
- the attached monitor is expected to display the dashboard during operation,
- the dashboard is a supervision/control surface, not a discretionary trading terminal,
- physical access, power, internet, and outbound IP stability are safety-relevant,
- the host must run a supported OS with update discipline,
- live runtime must not run as root,
- secrets must be protected and never logged,
- runtime DB/logs/backups are protected safety artifacts,
- time synchronization is mandatory,
- process/service management must preserve safe-mode-first restart,
- alerts and dashboard access are required before tiny live,
- host readiness is stage-specific,
- practical setup steps are deferred to the first-run setup checklist,
- and any host that cannot meet the tiny-live baseline must not run production trade-capable Prometheus.
