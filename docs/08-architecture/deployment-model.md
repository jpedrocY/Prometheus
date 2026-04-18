# Deployment Model

## Purpose

This document defines the deployment model for the v1 Prometheus trading system.

Its purpose is to make the runtime environments, deployment stages, process boundaries, configuration boundaries, secrets boundaries, persistence locations, operator access assumptions, and stage-promotion expectations explicit before implementation begins.

Prometheus is not deployed as one undifferentiated script that can accidentally become live simply because credentials are available. Deployment is a safety boundary.

This document answers:

- where the system may run,
- which capabilities are allowed in each environment,
- what configuration and secrets each environment may use,
- what persistence and log locations must exist,
- how the operator supervises the system,
- how alerts are routed,
- how startup and restart behave,
- and what must be true before moving from one deployment stage to the next.

This document also captures setup/runbook topics that should later be converted into a practical first-run checklist.

## Scope

This deployment model applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- first secondary research comparison: ETHUSDT perpetual,
- v1 live symbol scope: BTCUSDT only,
- strategy family: breakout continuation with higher-timeframe trend filter,
- signal timeframe: 15m,
- higher-timeframe bias: 1h,
- position mode: one-way mode,
- margin mode: isolated margin,
- one active strategy,
- one open position maximum,
- one active protective stop maximum,
- exchange-side protective stop required for live positions,
- supervised staged deployment,
- restart always begins in safe mode,
- exchange state is authoritative.

This document covers:

- deployment stage definitions,
- runtime process model,
- research/runtime separation,
- configuration model,
- secrets boundary,
- runtime database and file-location expectations,
- logs and observability locations,
- operator access model,
- alert-routing deployment hooks,
- startup/restart expectations,
- host assumptions by stage,
- environment capability matrix,
- promotion and demotion rules,
- setup topics deferred to the future first-run checklist,
- forbidden deployment patterns,
- and testing requirements.

This document does **not** define:

- exact shell commands for installation,
- final Python dependency manager choice,
- final CI/CD implementation,
- full host-hardening procedure,
- complete disaster-recovery procedure,
- final dashboard UI layout,
- exact Telegram or n8n setup steps,
- exact Binance API key creation steps,
- or the final AI coding handoff.

Those belong in related documents and the later first-run setup checklist.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/00-meta/current-project-state.md`
- `docs/08-architecture/implementation-blueprint.md`
- `docs/08-architecture/codebase-structure.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/event-flows.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/observability-design.md`
- `docs/04-data/historical-data-spec.md`
- `docs/04-data/live-data-spec.md`
- `docs/04-data/dataset-versioning.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/06-execution-exchange/failure-recovery.md`
- `docs/06-execution-exchange/user-stream-reconciliation.md`
- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/kill-switches.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/release-process.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`
- `docs/10-security/permission-scoping.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/alerting-ui.md`
- `docs/12-roadmap/phase-gates.md`

### Authority hierarchy

If this document conflicts with security policy on credential handling, secrets, API permissions, IP restrictions, or host access, the security document wins.

If this document conflicts with the restart procedure on startup/reconciliation behavior, the restart procedure wins.

If this document conflicts with the state model on runtime modes, blocking states, or protection-state semantics, the state model wins.

If this document conflicts with phase gates on promotion requirements, phase gates win.

If this document conflicts with the final first-run setup checklist on practical commands, the setup checklist may provide implementation detail, but it must not weaken this deployment model.

---

# Core Principles

## 1. Deployment is a safety boundary

Prometheus must not gain live trading capability accidentally.

A deployment environment must explicitly define:

- whether exchange connectivity is allowed,
- whether exchange reads are allowed,
- whether exchange writes are allowed,
- whether real capital can be affected,
- which config file is active,
- which secrets source is active,
- what runtime mode is allowed,
- and whether operator approval is required.

## 2. Credentials alone do not permit trading

The presence of Binance credentials is not sufficient to allow order placement.

The runtime must also require explicit environment and configuration permission for exchange-write capability.

Example:

```text
credentials_present = true
exchange_write_enabled = false
```

must mean:

```text
live order submission remains blocked
```

## 3. V1 remains supervised

V1 deployment is not lights-out autonomous operation.

The system may automate strategy evaluation, risk checks, order placement, protection, reconciliation, and recovery actions within approved boundaries, but live-capable stages require operator visibility and controlled escalation.

## 4. Every live-capable runtime starts in safe mode

No deployed runtime may start directly into `RUNNING_HEALTHY`.

On startup or restart, the runtime must:

1. enter safe mode,
2. load local state as provisional,
3. initialize observability,
4. verify configuration and secrets,
5. establish required connectivity,
6. reconcile exchange state where applicable,
7. verify position/protection state where applicable,
8. expose status to the operator,
9. and only then allow safe-mode exit if all gates pass.

## 5. Research and live runtime remain separate

Historical research, backtesting, dataset preparation, and validation reports are separate from the live trading runtime.

They may share strategy calculation code where safe, but they must not share live credentials, live order permissions, or live runtime state.

## 6. Deployment capability is stage-specific

Each stage has different allowed capabilities.

A local development environment should not have production write credentials.
A validation environment should not be able to place live orders.
A dry-run environment should exercise runtime logic without real exchange-side order placement.
Tiny live should be enabled only after explicit phase-gate approval.

## 7. Runtime persistence and logs are safety artifacts

Runtime database files, structured logs, event logs, operator actions, incident records, reconciliation records, and backups are part of the safety system.

They must be durable enough to support restart, review, recovery, and audit.

## 8. Deployment must fail closed

If required deployment state is missing, inconsistent, stale, or ambiguous, the runtime must block new entries and remain in safe mode or a blocked recovery state.

Examples:

- config missing,
- secrets missing,
- runtime DB unavailable,
- log directory unavailable,
- exchange mode mismatch,
- unexpected production credentials in local mode,
- time sync unavailable,
- user stream unavailable while exposure exists,
- alert route untested in live-capable mode,
- kill switch persisted active.

---

# Deployment Stage Overview

Prometheus should use a staged deployment path:

```text
LOCAL_DEVELOPMENT
  -> VALIDATION_RESEARCH
    -> DRY_RUN_RUNTIME
      -> PAPER_SHADOW
        -> TINY_LIVE
          -> SCALED_LIVE
```

The stages are not merely labels. Each stage defines allowed capabilities and required evidence before promotion.

---

## Stage 1 — Local Development

### Purpose

Local development exists to build, test, and debug Prometheus safely without real exchange-side trading capability.

### Typical environment

- developer machine,
- local repository checkout,
- local virtual environment,
- fake exchange adapter,
- local runtime database,
- local logs,
- local test fixtures,
- optional historical-data folders for research tests.

### Allowed activities

- run unit tests,
- run integration tests with fake adapters,
- run strategy calculation tests,
- run risk/sizing tests,
- run database migration tests,
- run linting, formatting, and type checks,
- run local dashboard/status prototype,
- run local dry-run simulations,
- inspect generated reports.

### Forbidden activities

- production order placement,
- live production emergency flattening,
- storing production API keys on casual development machines,
- unattended live runtime operation,
- using local dev mode as tiny-live deployment,
- bypassing fake adapter boundaries.

### Required setup hooks

The later first-run setup checklist should define:

- supported Python version,
- dependency manager,
- repository clone process,
- environment bootstrap,
- `.env` or equivalent local secret/config file creation,
- test runner command,
- lint command,
- type-check command,
- local runtime DB initialization,
- local logs path,
- local fake-exchange configuration.

This document does not define those exact commands.

---

## Stage 2 — Validation / Research

### Purpose

Validation/research deployment exists to run historical data preparation, backtests, walk-forward tests, robustness checks, and strategy reports.

This stage is analytical, not live trading.

### Typical environment

- local machine or dedicated research workspace,
- Parquet historical datasets,
- DuckDB query engine,
- dataset manifests,
- validation reports,
- research notebooks or scripts where approved,
- no production trading write permissions.

### Allowed activities

- fetch and normalize historical datasets,
- build derived datasets,
- validate data completeness,
- run backtests,
- run parameter sensitivity tests,
- run walk-forward validation,
- generate reports,
- compare BTCUSDT and ETHUSDT research results,
- prepare paper/shadow candidate evidence.

### Forbidden activities

- live production order placement,
- storing production trade-enabled API keys,
- using research results to automatically modify live configuration,
- mixing experimental datasets with validated dataset versions without manifest updates,
- silently overwriting historical dataset versions.

### Data storage expectation

Historical research storage should remain separate from runtime persistence.

Conceptual paths:

```text
data/historical/
data/research/
data/derived/
reports/backtests/
reports/validation/
```

The exact layout is governed by the historical data, dataset versioning, and data requirements documents.

---

## Stage 3 — Dry-Run Runtime

### Purpose

Dry-run runtime exists to exercise live-like runtime behavior without sending real exchange orders.

Dry-run is not the same as historical backtesting. It is a runtime integration stage.

### Typical environment

- local machine or test host,
- live or simulated market data,
- fake exchange adapter,
- fake fills / fake protective stops,
- runtime database,
- structured logs,
- event stream,
- dashboard/status surface where available.

### Allowed activities

- load runtime configuration,
- publish completed bars,
- generate strategy signals,
- run risk approvals/rejections,
- simulate entry submission,
- simulate fill confirmation,
- simulate protective stop confirmation,
- simulate stop replacement,
- simulate reconciliation,
- test restart behavior,
- test incident and kill-switch behavior,
- test dashboard/status output,
- test alert routing with non-production messages.

### Forbidden activities

- real exchange order placement,
- real production emergency flatten,
- use of trade-enabled production credentials,
- treating fake fills as performance evidence,
- skipping persistence tests because no real capital is used.

### Promotion evidence

Before moving beyond dry-run runtime, Prometheus should demonstrate:

- safe-mode-first startup,
- runtime DB writes for critical state transitions,
- exchange-event dedupe logic where simulated,
- unknown outcome handling,
- stop confirmation gating,
- restart recovery logic,
- operator-visible blocked states,
- kill-switch persistence,
- alert-route test success.

---

## Stage 4 — Paper / Shadow

### Purpose

Paper/shadow deployment exists to observe live market behavior and live-like runtime state without risking production capital.

The exact implementation may use:

- fake adapter with live market data,
- Binance testnet where appropriate,
- a controlled paper engine,
- or a shadow runtime that observes signals but does not place live production orders.

This document does not force a single implementation method before coding. It defines the required behavior and safety boundaries.

### Allowed activities

- ingest live market data,
- evaluate completed-bar signals,
- record paper trades,
- simulate or test exchange-style fills,
- simulate protective stop lifecycle,
- exercise runtime DB and event flows,
- test dashboard and alerts,
- perform planned restarts,
- rehearse reconciliation scenarios,
- rehearse operator workflows.

### Forbidden activities

- production capital exposure,
- production trade-enabled API keys unless explicitly read-only and approved for observation,
- unattended live trading,
- treating paper results as sufficient for scaled live,
- bypassing unresolved alert/dashboard failures.

### Required readiness

Paper/shadow should not start until:

- validation gates support the candidate strategy,
- dry-run runtime flows are tested,
- runtime persistence is working,
- logs are available,
- alert routing is configured and tested,
- dashboard or status surface is available,
- restart behavior is tested,
- operator understands pause/kill-switch behavior.

---

## Stage 5 — Tiny Live

### Purpose

Tiny live is the first real-capital deployment stage.

It exists to validate that Prometheus can operate safely with real exchange mechanics, real fills, real protective stops, real reconciliation, and real operator supervision at intentionally small risk.

### Initial tiny-live policy

Tiny live should use the approved initial risk and exposure constraints:

```text
risk_fraction = 0.0025
max_effective_leverage = 2.0
symbol = BTCUSDT
max_positions = 1
position_mode = one-way
margin_mode = isolated
```

An explicit internal notional cap is mandatory.

### Typical environment

- dedicated or carefully controlled host,
- production Binance account prepared for v1 constraints,
- trade-enabled keys only after approval,
- IP restriction where supported,
- secrets storage configured,
- runtime database on durable disk,
- structured logs,
- backups,
- alert routing,
- operator dashboard/status access,
- process/service supervision,
- emergency access path.

### Allowed activities

- live BTCUSDT strategy operation under approved tiny-live constraints,
- exchange-side protective stop placement,
- stop replacement within policy,
- controlled market exit,
- emergency flatten through approved path,
- reconciliation,
- incident handling,
- operator pause/kill switch,
- daily/weekly review.

### Forbidden activities

- multi-symbol live trading,
- pyramiding,
- reversal entry while positioned,
- hedge-mode operation,
- cross-margin operation,
- risk above approved tiny-live risk,
- leverage cap increase without review,
- missing notional cap,
- trading without alert route tested,
- trading without restart/reconciliation tested,
- trading with unprotected position as normal operation,
- treating tiny-live as unattended scaled production.

### Required readiness

Tiny live must not begin until:

- strategy has passed required validation/paper gates,
- operator approval has been recorded,
- production host assumptions are satisfied,
- API key policy is satisfied,
- permissions are scoped,
- IP restriction is configured where applicable,
- secrets are stored correctly,
- runtime DB is initialized,
- backup/restore has been rehearsed at least at a basic level,
- alert route has been tested,
- dashboard/status access has been tested,
- safe-mode restart has been tested,
- reconciliation has been tested,
- kill switch has been tested,
- rollback procedure is understood,
- emergency recovery path is understood.

The later first-run setup checklist should convert these requirements into practical steps.

---

## Stage 6 — Scaled Live

### Purpose

Scaled live is any live operation beyond tiny-live constraints.

This may include:

- increased risk fraction,
- increased notional cap,
- increased leverage cap,
- broader operating duration,
- more operator confidence,
- eventually more symbols or strategies in future versions.

For v1, scaled live still remains supervised and constrained.

### Required evidence

Scaled live requires:

- successful tiny-live operating history,
- clean stop-placement and stop-replacement history,
- no unresolved severe incidents,
- no unresolved security issues,
- acceptable slippage and fee behavior,
- acceptable drawdown behavior,
- reviewed daily/weekly reports,
- tested backup/restore path,
- tested rollback path,
- explicit operator approval,
- config version change,
- release record,
- updated risk review.

### Forbidden assumptions

Scaled live must not be treated as:

- automatic reward for early wins,
- a parameter-only config change,
- permission to bypass daily/drawdown controls,
- permission to run without supervision,
- permission to introduce additional symbols without separate design.

---

# Runtime Process Model

## V1 default

Prometheus v1 should deploy as a modular monolith:

```text
prometheus-runtime
  market-data ingestion
  user-stream ingestion
  strategy engine
  risk and sizing
  execution orchestration
  state and reconciliation
  runtime persistence
  incident/safety control
  observability/event emission
  operator status/control surface where appropriate
```

This model uses one primary deployable runtime with clear internal module boundaries.

## Recommended process boundaries

### Primary runtime process

The primary runtime process owns:

- live market-data ingestion,
- user-stream/private event intake,
- strategy/risk/execution orchestration,
- exchange adapter access,
- runtime state transitions,
- persistence writes,
- reconciliation,
- incident control,
- alert emission,
- operator command handling where enabled.

### Research/backtest tools

Research and backtest tools should run as separate CLI/script processes.

They may read historical datasets and produce reports, but they must not require live trading credentials.

### Dashboard/status surface

For v1, the dashboard/status surface may be:

- embedded in the runtime process,
- a local web UI served by the runtime,
- a lightweight separate process reading from controlled backend APIs,
- or a CLI/status endpoint in early stages.

The dashboard must not directly access exchange credentials or bypass backend safety controls.

## Future process splits

Future versions may split the runtime into separate services, but v1 should avoid distributed complexity unless implementation evidence clearly justifies it.

Potential future splits:

```text
runtime process
dashboard process
worker/scheduler process
alert dispatcher
```

These are not v1 requirements.

---

# Research vs Runtime Deployment Separation

Research deployment and live runtime deployment must remain separate.

## Research deployment owns

- historical data fetch/normalization,
- Parquet datasets,
- DuckDB query views,
- dataset manifests,
- derived research datasets,
- backtest reports,
- validation reports,
- robustness experiments.

## Runtime deployment owns

- live market-data intake,
- user stream,
- exchange placement/cancellation/reconciliation,
- active trade/protection state,
- runtime database,
- operator controls,
- incident handling,
- alert routing,
- restart/recovery.

## Shared code policy

Shared code is allowed where safe, especially:

- strategy calculations,
- indicator calculations,
- stop formula calculations,
- symbol metadata models,
- validation helpers.

Shared code must not cause:

- research tools to import live credentials,
- backtests to call live exchange endpoints,
- live runtime to depend on mutable research notebooks,
- runtime decisions to use unversioned research artifacts.

---

# Configuration Model

## Configuration goals

Configuration must make deployment capability explicit and auditable.

Each environment configuration should answer:

- what stage is this,
- what exchange adapter mode is active,
- can the runtime read exchange state,
- can the runtime place/cancel orders,
- what symbol is allowed,
- what risk settings are active,
- what notional/leverage caps are active,
- where the runtime DB lives,
- where logs are written,
- which alert routes are enabled,
- whether dashboard/control endpoints are enabled,
- whether operator approval is required for startup or clearance.

## Recommended configuration families

Recommended conceptual configuration files:

```text
config/local.example.yaml
config/validation.example.yaml
config/dry_run.example.yaml
config/paper_shadow.example.yaml
config/tiny_live.example.yaml
config/scaled_live.example.yaml
```

Actual local/private config files must not be committed if they contain secrets or environment-specific sensitive values.

## Required stage enum

Recommended deployment stage values:

```text
LOCAL_DEVELOPMENT
VALIDATION_RESEARCH
DRY_RUN_RUNTIME
PAPER_SHADOW
TINY_LIVE
SCALED_LIVE
```

## Required adapter mode enum

Recommended exchange adapter modes:

```text
FAKE_EXCHANGE
SIMULATED_EXCHANGE
BINANCE_TESTNET_OR_EQUIVALENT
BINANCE_PRODUCTION_READ_ONLY
BINANCE_PRODUCTION_TRADE_ENABLED
```

Implementation may refine the exact names, but it must preserve the capability separation.

## Capability flags

Recommended explicit capability flags:

```text
exchange_read_enabled
exchange_write_enabled
order_placement_enabled
order_cancellation_enabled
emergency_flatten_enabled
production_credentials_allowed
operator_approval_required
alerts_required
reconciliation_required_on_startup
```

Live order placement should require both:

```text
exchange_write_enabled = true
order_placement_enabled = true
```

and a deployment stage that permits the capability.

## Risk and exposure configuration

Live-capable configurations must explicitly include:

```text
allowed_symbols
max_open_positions
max_open_positions_per_symbol
risk_fraction
max_effective_leverage
max_position_notional_usdt
position_mode_required
margin_mode_required
protective_stop_required
```

If `max_position_notional_usdt` is missing in a live-capable environment, the runtime must reject live entry capability.

## Config versioning

Every deployed config should have:

- config version,
- config hash,
- activation timestamp,
- deployment stage,
- release reference where applicable,
- operator approval reference where applicable.

Config version should be recorded in runtime events, trades, orders, incidents, and review outputs where relevant.

---

# Secrets Boundary

## Core rule

Secrets must never be committed to the repository.

This includes:

- Binance API keys,
- Binance API secrets,
- webhook secrets,
- Telegram bot tokens,
- n8n webhook tokens,
- database passwords where applicable,
- signed request payloads,
- credential-bearing screenshots,
- production `.env` files,
- private host keys.

## Secrets are not runtime facts

The runtime database must not store raw secrets.

Structured events, logs, incident records, and operator actions must not include secret material.

## Secret loading by stage

### Local development

Should use no real production trade-enabled credentials.

If any credentials are used for read-only experiments, they must be explicitly separated and treated conservatively.

### Validation/research

Should not require production trade-enabled credentials.

### Dry-run

Should use fake or simulated credentials where possible.

### Paper/shadow

May use testnet or read-only credentials depending on the final implementation path.

### Tiny live and scaled live

May use production trade-enabled credentials only after security, permission, IP restriction, operator approval, and phase-gate requirements are satisfied.

## Missing or inconsistent secrets

If a deployment mode requires secrets and they are missing or inconsistent, the runtime must:

```text
remain in SAFE_MODE
block entries
emit operator-visible error
avoid partial startup into live capability
```

## Secret setup deferred

Practical secret creation, environment-variable naming, `.env` file creation, and host secret installation steps should be defined in the later first-run setup checklist and security documents.

This document intentionally does not ask the operator to create real Binance API keys.

---

# Runtime Database and File Locations

## Runtime database role

The runtime database is part of the safety system.

It stores restart-critical local state, command intent, exchange-derived evidence, operator actions, reconciliation outcomes, incident state, daily loss state, drawdown state, and audit events.

The runtime database is not exchange truth.

## V1 database engine expectation

The database design document recommends a relational runtime database, with SQLite + WAL as the v1 default and PostgreSQL-compatible discipline where practical.

Deployment should support that direction.

## Conceptual local paths

For local and early-stage operation, conceptual paths may be:

```text
var/prometheus/runtime/prometheus.sqlite
var/prometheus/logs/
var/prometheus/backups/
var/prometheus/reports/
data/historical/
data/research/
```

## Conceptual production paths

For production-like Linux deployment, conceptual paths may be:

```text
/etc/prometheus/              # non-secret config where appropriate
/var/lib/prometheus/          # runtime DB and durable state
/var/log/prometheus/          # logs
/var/backups/prometheus/      # backups
```

The exact path policy should be finalized in host-hardening and first-run setup documentation.

## File permissions

Runtime DB, logs, backups, and config files must use restrictive permissions appropriate for the deployment stage.

Secrets require stricter handling than normal config.

## Persistence expectations by stage

| Stage | Runtime DB required? | Durable logs required? | Backups required? |
|---|---:|---:|---:|
| Local development | Yes for runtime tests | Recommended | Optional |
| Validation/research | Not for live runtime | Reports/logs recommended | Dataset backup/versioning as needed |
| Dry-run runtime | Yes | Yes | Recommended |
| Paper/shadow | Yes | Yes | Recommended |
| Tiny live | Yes | Yes | Yes |
| Scaled live | Yes | Yes | Yes |

---

# Logs and Observability Locations

## Required observability outputs

Each deployed runtime should produce:

- structured runtime events,
- exchange-derived event records where applicable,
- reconciliation records,
- incident records,
- operator action records,
- process logs,
- alert events,
- dashboard/status summaries.

## Log location policy

Logs should be stored outside the source tree for production-like deployments.

Local development may use local project-relative paths for convenience, but those paths must not be confused with production retention.

## Redaction

Logs and events must redact:

- API keys,
- API secrets,
- signatures,
- webhook secrets,
- private tokens,
- raw credential-bearing headers,
- sensitive host-specific values where appropriate.

## Alert-worthy deployment failures

The deployment layer should produce alerts for:

- failed startup,
- unsafe config,
- missing secrets in live-capable mode,
- runtime DB unavailable,
- log path unavailable,
- exchange connectivity unavailable in live-capable mode,
- user stream unavailable where required,
- reconciliation failure,
- kill switch active after restart,
- backup failure in live-capable mode,
- alert route failure in live-capable mode.

---

# Operator Access Model

## Core rule

The operator interface is a supervision and control surface, not a discretionary trading terminal.

It should expose state, health, alerts, incidents, recovery status, and approved control actions.

It must not provide casual manual trade placement.

## Access by stage

| Stage | Minimum operator access |
|---|---|
| Local development | CLI output, logs, test reports |
| Validation/research | Backtest/validation reports, logs |
| Dry-run runtime | CLI/status summary; dashboard preferred |
| Paper/shadow | Dashboard/status surface plus alerts |
| Tiny live | Dashboard/status surface, alerts, emergency access |
| Scaled live | Dashboard/status surface, alerts, emergency access, stronger audit/review |

## Operator capabilities by stage

| Capability | Local | Validation | Dry-run | Paper/shadow | Tiny live | Scaled live |
|---|---:|---:|---:|---:|---:|---:|
| View runtime status | Yes | Limited | Yes | Yes | Yes | Yes |
| View logs/events | Yes | Yes | Yes | Yes | Yes | Yes |
| Enable pause | Simulated | N/A | Yes | Yes | Yes | Yes |
| Enable kill switch | Simulated | N/A | Yes | Yes | Yes | Yes |
| Clear kill switch | Simulated | N/A | Controlled | Controlled | Approval required | Approval required |
| Approve recovery | Simulated | N/A | Controlled | Controlled | Approval required | Approval required |
| Emergency flatten | No real action | N/A | Simulated | Simulated/testnet only | Approved path only | Approved path only |
| Place discretionary trade | No | No | No | No | No | No |

## Access security

Production-like operator access should be restricted.

The host-hardening and interface documents should define:

- authentication approach,
- network binding,
- local vs remote access,
- logging of operator actions,
- confirmation requirements,
- emergency access expectations.

---

# Alert Routing Deployment Hooks

## Supported alert routes

Prometheus may support alert routes such as:

- local logs,
- dashboard alerts,
- Telegram notifications,
- n8n webhook routing,
- future email or incident tools.

This document does not define exact bot tokens, webhook URLs, or routing commands.

## Stage requirements

| Stage | Alert routing requirement |
|---|---|
| Local development | Optional / local only |
| Validation/research | Optional report notifications |
| Dry-run runtime | Recommended test route |
| Paper/shadow | Required test route |
| Tiny live | Required working route |
| Scaled live | Required working route with review |

## Alert test requirement

Paper/shadow and tiny-live deployment must not begin until alert routing has been tested.

Minimum alert-route tests should include:

- startup test alert,
- warning alert,
- critical alert,
- kill-switch active alert,
- incident active alert,
- recovery/reconciliation failure alert where simulated,
- alert-route failure behavior.

## Alert routing safety

Alert routes must not leak secrets or full raw exchange payloads.

Webhook URLs, tokens, and bot credentials must be treated as secrets.

---

# Startup and Restart Behavior

## Universal startup rule

Every runtime starts in:

```text
SAFE_MODE
```

This applies even after a clean shutdown.

## Startup sequence

A deployed runtime should follow this sequence:

1. process starts,
2. enter `SAFE_MODE`,
3. initialize structured logging,
4. load configuration,
5. validate deployment stage and capability flags,
6. load secrets if required for the stage,
7. open runtime database,
8. load persisted local state as provisional,
9. initialize alert routing where configured,
10. initialize market-data connectivity where required,
11. initialize exchange/user-stream connectivity where required,
12. run startup reconciliation where applicable,
13. surface status to operator,
14. remain blocked or exit safe mode only if all gates pass.

## Local state is provisional

Persisted local runtime state supports recovery and continuity.

It does not prove exchange truth.

Live-capable deployments must reconcile against exchange state before normal operation.

## Kill switch and pause persistence

If kill switch or operator pause was active before restart, it must remain active after restart.

Restart must not clear:

- kill switch,
- operator pause,
- unresolved incident,
- operator review required,
- daily loss lockout,
- drawdown pause,
- unresolved reconciliation mismatch,
- unknown execution outcome,
- emergency branch.

## Startup failure behavior

If startup cannot complete required checks, the runtime must:

- stay in safe mode,
- block entries,
- emit logs/events,
- alert the operator if alert routing is available,
- avoid partial live capability.

---

# Host Assumptions by Stage

## Local development host

Expected properties:

- suitable Python development environment,
- repository checkout,
- ability to run tests,
- local filesystem for DB/logs,
- no requirement for production uptime,
- no requirement for production secrets.

## Validation/research host

Expected properties:

- enough disk for historical datasets,
- stable dataset storage,
- DuckDB/Parquet support,
- enough CPU/memory for backtests,
- reproducible report generation.

## Dry-run host

Expected properties:

- runtime DB durability,
- stable enough networking for live data if used,
- logs and events available,
- alert route testing possible,
- safe fake/simulated adapter.

## Paper/shadow host

Expected properties:

- stable network,
- stable runtime process,
- durable DB/log paths,
- tested alert route,
- operator access,
- safe restart behavior,
- no real capital exposure.

## Tiny-live host

Expected properties:

- stable network,
- stable outbound IP if API keys are IP-restricted,
- reliable time synchronization,
- restricted host access,
- OS update baseline,
- firewall/SSH hygiene,
- process/service supervision,
- durable DB/log paths,
- backup path,
- alert route,
- operator dashboard/status access,
- emergency access path.

Detailed host-hardening requirements belong in `docs/10-security/host-hardening.md`.

## Scaled-live host

Expected properties:

- all tiny-live requirements,
- stronger monitoring/review,
- tested restore path,
- tested rollback path,
- documented release/config management,
- higher operator confidence,
- no unresolved operational/security debt that blocks scaling.

---

# Environment Capability Matrix

| Capability | Local Dev | Validation | Dry-Run | Paper/Shadow | Tiny Live | Scaled Live |
|---|---:|---:|---:|---:|---:|---:|
| Historical data processing | Yes | Yes | Optional | Optional | No normal need | No normal need |
| Strategy backtesting | Yes | Yes | No normal need | No normal need | No | No |
| Live market-data ingestion | Optional | No | Optional/Yes | Yes | Yes | Yes |
| User stream/private state | No | No | Simulated | Simulated/testnet/read-only where approved | Yes | Yes |
| Exchange read access | No/optional | No | Simulated | Optional/read-only/testnet | Yes | Yes |
| Exchange write access | No | No | No | No production writes | Yes, gated | Yes, gated |
| Real capital exposure | No | No | No | No | Yes, tiny | Yes, approved |
| Runtime DB | Yes for runtime tests | Optional | Yes | Yes | Yes | Yes |
| Alerts | Optional | Optional | Recommended | Required | Required | Required |
| Operator dashboard/status | Optional | Reports | Recommended | Required | Required | Required |
| Safe-mode startup | Yes for runtime | N/A | Yes | Yes | Yes | Yes |
| Reconciliation on startup | Simulated | N/A | Simulated | Required where applicable | Required | Required |
| Kill switch | Simulated | N/A | Yes | Yes | Yes | Yes |
| Emergency flatten | No real action | N/A | Simulated | Simulated/testnet only | Approved real path | Approved real path |

---

# Promotion and Demotion Rules

## Promotion principle

Promotion to a more capable environment requires evidence.

The system must not be promoted merely because code runs.

## Required promotion properties

Before promotion, the current stage should demonstrate:

- expected functionality works,
- safety gates work,
- failure paths are tested,
- runtime persistence is reliable,
- alerts are working where required,
- operator actions are auditable where required,
- restart/reconciliation is tested where required,
- documentation and config versions are recorded.

## Demotion principle

Prometheus should support moving backward to a safer stage.

Examples:

- scaled live back to tiny live,
- tiny live back to paper/shadow,
- paper/shadow back to dry-run,
- any live-capable stage back to safe mode.

Demotion may be required after:

- severe incident,
- protection failure,
- reconciliation failure,
- repeated unknown execution outcomes,
- credential/security concern,
- unexpected drawdown,
- failed release,
- operator loss of confidence.

## Live capability removal

Demoting a live-capable deployment should include:

- disabling exchange write capability,
- preserving logs and DB state,
- reconciling exchange state,
- confirming no unprotected exposure,
- recording operator action,
- recording incident/release context where applicable.

---

# Setup and Runbook Topics Deferred to First-Run Checklist

A dedicated practical setup/runbook document should be created later, likely:

```text
docs/09-operations/first-run-setup-checklist.md
```

This should happen before `docs/00-meta/ai-coding-handoff.md` is finalized.

The first-run setup checklist should provide the guided path for:

1. installing prerequisites,
2. configuring local development,
3. preparing historical data storage,
4. preparing dry-run/paper/shadow runtime,
5. setting up alerts,
6. preparing production/tiny-live infrastructure,
7. creating keys safely only at the correct phase,
8. validating operator readiness,
9. launching paper/shadow,
10. launching tiny live,
11. verifying emergency access and recovery.

## Topics to include later

The setup checklist should cover at least:

- supported Python version,
- dependency manager setup,
- repository clone,
- local environment bootstrap,
- local config file creation,
- local secret file pattern,
- test runner,
- linting,
- formatting,
- type checking,
- runtime database initialization,
- runtime database migration,
- local logs path,
- historical data folders,
- DuckDB/Parquet setup,
- dataset manifest checks,
- dry-run config,
- paper/shadow config,
- Binance testnet or simulated exchange setup if used,
- Binance production account preparation,
- production API key creation timing,
- API key permissions,
- IP restriction,
- secrets storage,
- environment variables,
- production host or VPS preparation,
- firewall baseline,
- SSH hygiene,
- OS update baseline,
- time synchronization,
- process/service management,
- production logging locations,
- backup setup,
- restore rehearsal,
- Telegram alert setup,
- n8n alert setup,
- operator dashboard access,
- paper/shadow launch checklist,
- tiny-live launch checklist,
- emergency access checklist,
- recovery checklist.

## Topics not to perform now

This project should not yet perform or request:

- real Binance production API key creation,
- real trade-enabled credential setup,
- real production VPS changes,
- real firewall/SSH modifications,
- real capital deployment,
- emergency flatten testing on a live position.

Those belong to later approved phases.

---

# Forbidden Deployment Patterns

The following deployment patterns are forbidden for v1.

## 1. Production credentials in casual local development

Production trade-enabled credentials must not be used casually on a development machine.

## 2. Live writes enabled by default

Exchange-write capability must never be the default.

## 3. Live trading without explicit stage config

A runtime must not infer live mode merely from credentials, host name, or operator intent.

## 4. Startup directly into healthy mode

No runtime may start directly into `RUNNING_HEALTHY` without safe-mode startup and required checks.

## 5. Trading without runtime persistence

Live-capable deployment must not trade if the runtime database is unavailable.

## 6. Trading without logs/events

Live-capable deployment must not trade if structured logging/event recording is unavailable.

## 7. Trading without alert route in paper/tiny-live stages

Paper/shadow and tiny-live stages require tested alert routing.

## 8. Trading without reconciliation capability

Live-capable deployment must not trade if it cannot reconcile positions, normal orders, and protective stops.

## 9. Trading with unresolved kill switch or incident

Restart, redeploy, or config change must not silently clear blocking safety states.

## 10. Manual dashboard trading

The dashboard must not become a discretionary manual trading terminal.

## 11. Research scripts with live order permissions

Research/backtest tools must not have production trading write permissions.

## 12. Secrets in repository, logs, docs, screenshots, or database

Secret leakage through convenience tooling is forbidden.

---

# Testing Requirements

Deployment behavior must be testable.

## Configuration tests

Required tests:

- local config cannot place live orders,
- validation config cannot place live orders,
- dry-run config uses fake/simulated adapter,
- paper/shadow config cannot place production live orders unless explicitly designed and approved otherwise,
- tiny-live config requires notional cap,
- tiny-live config requires risk fraction and leverage cap,
- production write mode requires explicit flags,
- missing required config fails closed,
- invalid stage/adapter combination fails closed.

## Secrets tests

Required tests:

- missing required secret in live-capable mode fails closed,
- secrets are not written to runtime DB,
- secrets are not written to structured logs,
- redaction works for known secret-like fields,
- fake/local mode does not require production secrets.

## Startup/restart tests

Required tests:

- startup enters safe mode,
- restart preserves kill switch,
- restart preserves operator pause,
- restart preserves active incident/blocking state,
- restart loads local state as provisional,
- live-capable restart requires reconciliation,
- failed DB open blocks live operation,
- failed log initialization blocks live operation where required,
- failed alert route blocks paper/tiny-live start where required by config.

## Runtime capability tests

Required tests:

- credentials present but write disabled cannot submit orders,
- exchange write enabled but stage not live-capable cannot submit orders,
- emergency flatten unavailable in dry-run except simulated,
- local fake adapter cannot reach Binance trade endpoints,
- dashboard control cannot bypass backend safety gates.

## File/path tests

Required tests:

- runtime DB path is writable before live operation,
- log path is writable before live operation,
- backup path exists for live-capable mode where required,
- historical data path is separate from runtime DB path,
- production config path does not require writing into repository.

## Alert tests

Required tests:

- test alert can be emitted,
- warning alert can be emitted,
- critical alert can be emitted,
- alert redaction works,
- alert-route failure is detected,
- paper/shadow and tiny-live cannot start if required alert route is not verified.

---

# Non-Goals

This document does not attempt to define:

- exact installation commands,
- exact package manager commands,
- exact Python version lock,
- exact Linux service file,
- final CI/CD provider,
- final cloud/VPS provider,
- final dashboard authentication implementation,
- final Telegram or n8n setup sequence,
- final API key creation walkthrough,
- final disaster-recovery checklist,
- final rollback commands,
- or the Claude Code handoff.

Those should be handled in later operational, security, interface, roadmap, and meta documents.

---

# Acceptance Criteria

This deployment model is acceptable when it clearly establishes that:

- deployment stage controls system capability,
- credentials alone do not permit trading,
- local development cannot accidentally become live trading,
- research and runtime deployments remain separate,
- dry-run/paper/tiny-live/scaled-live stages are distinct,
- every live-capable runtime starts in safe mode,
- restart requires reconciliation before normal operation,
- runtime persistence and logs are required safety artifacts,
- alert routing is required before paper/shadow and tiny live,
- operator dashboard is supervision/control, not discretionary trading,
- production host expectations are identified but not over-specified,
- first-run setup checklist topics are captured for later,
- real Binance key creation is deferred to the correct phase,
- and forbidden deployment patterns are explicit enough for implementation and review.

---

# Summary Policy

Prometheus deployment is intentionally staged and capability-gated.

A runtime environment must explicitly declare what it is allowed to do. Live exchange write capability requires the right deployment stage, the right configuration, the right secrets, the right operator approval, the right runtime state, the right persistence, the right alerting, and successful reconciliation.

No system state, credential file, host environment, or code path may silently upgrade Prometheus into live trading capability.
