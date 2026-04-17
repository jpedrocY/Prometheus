# Codebase Structure

## Purpose

This document defines the recommended source-code structure for the v1 Prometheus trading system.

Its purpose is to translate the existing architecture, state, persistence, execution, operations, and security documents into a concrete repository layout that can be implemented safely by a human developer or by Claude Code.

This document answers:

- where source code should live,
- how runtime modules should be separated,
- which modules may depend on which other modules,
- which boundaries must not be crossed,
- how research code should remain separate from live runtime code,
- where configuration, persistence, observability, and operator surfaces belong,
- how tests should be organized,
- and what structure Claude Code should follow when generating implementation files.

This document is a pre-implementation architecture contract. It is not application code.

---

## Scope

This document applies to the first implementation-ready version of Prometheus, under the current v1 assumptions:

- Binance USDⓈ-M futures,
- BTCUSDT perpetual as the first live-capable symbol,
- ETHUSDT perpetual as the first secondary research comparison symbol,
- 15m signal timeframe,
- 1h higher-timeframe trend bias,
- breakout continuation strategy,
- one-way mode,
- isolated margin,
- one active strategy,
- one symbol first,
- one open position maximum,
- one active protective stop maximum,
- operator-supervised deployment,
- safe-mode-first restart,
- exchange-authoritative reconciliation,
- restart-critical runtime persistence,
- state-centric observability,
- and strict secret-handling rules.

This document covers the future source-code layout, not the existing documentation tree alone.

This document does **not** define:

- final implementation code,
- exact class signatures,
- final third-party dependency versions,
- CI/CD implementation details,
- full frontend design,
- infrastructure provisioning,
- or multi-symbol / portfolio architecture.

---

## Background

The existing architecture documents already define the system shape:

- v1 should be a modular monolith,
- strategy and execution must remain separate,
- exchange state is authoritative for live position, order, and protective-stop truth,
- user-stream events are the primary live state source,
- REST is used for placement, cancellation, reconciliation, and recovery,
- runtime state must be persisted only where needed for safe restart and operator continuity,
- important internal communication must distinguish commands, events, and queries,
- and the operator surface must not bypass backend safety boundaries.

Those decisions need a concrete codebase structure before implementation begins.

Without this document, code generation could drift into:

- mixed strategy and exchange logic,
- hidden state mutation across modules,
- research code that accidentally depends on live execution code,
- frontend or operator controls that bypass backend safety logic,
- persistence scattered across unrelated components,
- or implementation shortcuts that make restart and reconciliation unsafe.

---

## Primary Implementation Direction

## Language direction

The recommended v1 implementation language is:

- **Python**

### Why Python is selected for v1

Python is appropriate for the first implementation because the project requires:

- historical research and backtesting,
- Parquet and DuckDB workflows,
- clear strategy and risk logic,
- exchange API integration,
- runtime orchestration,
- structured tests,
- and fast iteration under strict architecture boundaries.

This does not mean the system should be loose or script-like. The Python codebase should be typed, modular, testable, and organized around explicit interfaces.

## Runtime shape

The v1 system should be implemented as a:

> **Python modular monolith with strict internal module boundaries**

This means:

- one main backend/runtime codebase,
- one primary deployable trading process for v1,
- clear internal packages,
- explicit command/event/query contracts,
- local durable runtime persistence,
- and optional later interface/frontend components that communicate through approved backend surfaces.

It does **not** mean:

- one giant script,
- a distributed microservice system,
- a speculative event-bus platform,
- or a dashboard that talks directly to Binance.

---

## Target Repository Layout

The recommended future repository layout is:

```text
Prometheus/
  README.md
  pyproject.toml
  .gitignore
  .gitattributes

  docs/
    00-meta/
    01-foundations/
    02-market-structure/
    03-strategy-research/
    04-data/
    05-backtesting-validation/
    06-execution-exchange/
    07-risk/
    08-architecture/
    09-operations/
    10-security/
    11-interface/
    runbooks/
    templates/

  src/
    prometheus/
      __init__.py
      cli.py

      core/
      config/
      secrets/
      events/
      observability/

      market_data/
      strategy/
      risk/
      exchange/
      execution/
      state/
      persistence/
      reconciliation/
      safety/
      operator/
      runtime/
      research/

  tests/
    unit/
    integration/
    contract/
    simulation/
    fixtures/

  configs/
    README.md
    dev.example.yaml
    validation.example.yaml
    paper.example.yaml
    production.example.yaml

  scripts/
    README.md
    fetch_historical_data.py
    run_backtest.py
    run_validation.py
    run_runtime.py
    inspect_runtime_state.py

  data/
    .gitkeep

  var/
    .gitkeep
```

## Root-level policy

### `README.md`
The repository README remains the high-level project introduction.

### `pyproject.toml`
The project should use one standard Python project configuration file for:

- package metadata,
- dependency declarations,
- test configuration where practical,
- formatting / linting configuration where practical,
- and tool configuration.

### `docs/`
Documentation remains the canonical project memory and decision history.

### `src/prometheus/`
All package source code should live under `src/prometheus/`.

### `tests/`
All automated tests should live under `tests/` and should mirror the architecture boundaries.

### `configs/`
Version-controlled configuration examples may live here.

Live secrets must not live here.

### `scripts/`
Operational and development helper scripts may live here, but they must call into package modules rather than contain core business logic.

### `data/`
Local research datasets may be placed here during development if needed, but large datasets and generated data should remain untracked unless explicitly approved.

### `var/`
Local runtime artifacts may be placed here during development, such as runtime database files, local logs, or temporary state snapshots.

This directory should be ignored by git except for placeholder files.

---

## Source Package Overview

The source package should be organized as:

```text
src/prometheus/
  cli.py

  core/
  config/
  secrets/
  events/
  observability/

  market_data/
  strategy/
  risk/
  exchange/
  execution/
  state/
  persistence/
  reconciliation/
  safety/
  operator/
  runtime/
  research/
```

Each package must have a clear responsibility and must not become a miscellaneous dumping ground.

---

# Module Responsibilities

## `core/`

### Purpose

Shared foundational utilities and domain primitives used across the codebase.

### Owns

- UTC millisecond time utilities,
- canonical ID helpers,
- common domain types,
- shared exceptions,
- numeric helpers where safe and generic,
- symbol / interval primitives,
- deterministic client-order-ID utilities,
- and small pure functions with no infrastructure dependency.

### Does not own

- exchange API calls,
- strategy decisions,
- runtime state mutation,
- persistence writes,
- secrets,
- or operator controls.

### Suggested files

```text
core/
  __init__.py
  clock.py
  ids.py
  types.py
  enums.py
  errors.py
  math.py
```

---

## `config/`

### Purpose

Runtime and research configuration loading, validation, and environment selection.

### Owns

- environment selection,
- config file parsing,
- typed config models,
- validation of non-secret configuration,
- stage-specific config defaults,
- and config version identification.

### Does not own

- raw secret values,
- direct exchange API credentials,
- exchange calls,
- runtime state,
- or strategy execution.

### Suggested files

```text
config/
  __init__.py
  models.py
  loader.py
  validators.py
  environments.py
```

### Configuration rule

Configuration may describe:

- environment name,
- symbol,
- strategy version,
- risk limits,
- feature flags,
- logging levels,
- runtime persistence path,
- and paper/live mode.

Configuration must not contain:

- raw API secrets,
- live API keys where avoidable,
- withdrawal-related material,
- or signed request examples.

---

## `secrets/`

### Purpose

Controlled loading and validation of sensitive runtime inputs.

### Owns

- environment-variable secret loading,
- secret presence validation,
- secret redaction helpers,
- role-based credential references,
- and fail-closed behavior when required secrets are missing or invalid.

### Does not own

- strategy logic,
- exchange order placement decisions,
- runtime state transitions,
- or secret persistence.

### Suggested files

```text
secrets/
  __init__.py
  loader.py
  models.py
  redaction.py
  validation.py
```

### Hard rule

The `secrets/` package must never write raw secrets to logs, runtime persistence, docs, events, or normal error output.

---

## `events/`

### Purpose

Code-level representation of internal command, event, and query contracts.

### Owns

- shared message envelope,
- command models,
- event models,
- query models,
- correlation and causation fields,
- message validation helpers,
- and event naming conventions.

### Does not own

- message transport complexity,
- persistence decisions by itself,
- strategy calculations,
- or exchange calls.

### Suggested files

```text
events/
  __init__.py
  envelope.py
  commands.py
  runtime_events.py
  exchange_events.py
  incident_events.py
  queries.py
  names.py
```

### Contract rule

Commands, events, and queries must remain semantically distinct:

- commands express intent,
- events express facts,
- queries read state.

A command must never be treated as proof that something happened.

---

## `observability/`

### Purpose

Structured logging, event recording, health summaries, alert surfaces, and review-support outputs.

### Owns

- structured log formatting,
- operational event recording,
- health snapshot models,
- alert classification helpers,
- redaction integration,
- and operator-facing summary preparation where appropriate.

### Does not own

- strategy decisions,
- exchange truth,
- runtime state authority,
- or direct dashboard controls.

### Suggested files

```text
observability/
  __init__.py
  logger.py
  event_recorder.py
  health.py
  alerts.py
  redaction.py
```

### Rule

Observability must be state-centric, not vanity-metric-centric.

The highest priority is visibility into:

- runtime mode,
- open exposure,
- protection state,
- stream health,
- reconciliation state,
- incidents,
- and operator action requirements.

---

## `market_data/`

### Purpose

Live and historical market-data normalization needed by the strategy and research systems.

### Owns

- market-data models,
- kline/bar normalization,
- completed-bar detection,
- market-data freshness tracking,
- live market stream adapters at the semantic layer,
- and publication of completed-bar events.

### Does not own

- private user-stream events,
- order state,
- position state,
- strategy decisions,
- or exchange order placement.

### Suggested files

```text
market_data/
  __init__.py
  models.py
  bars.py
  completed_bar.py
  freshness.py
  streams.py
```

### Completed-bar rule

Only completed bars may be emitted to strategy evaluation paths.

Partial candle updates may be tracked for freshness or diagnostics, but they must not become strategy inputs as if they were final bars.

---

## `strategy/`

### Purpose

Rules-based strategy logic and strategy-side trade-management intent.

### Owns

- higher-timeframe bias logic,
- setup / consolidation logic,
- breakout trigger logic,
- stop-level calculation,
- strategy-side exit intent,
- strategy-stage transitions,
- no-trade filter evaluation,
- and pure calculation functions reusable by research and runtime.

### Does not own

- exchange API calls,
- order placement,
- fill confirmation,
- position truth,
- protective-stop truth,
- reconciliation classification,
- or operator controls.

### Suggested files

```text
strategy/
  __init__.py
  interfaces.py
  common/
    __init__.py
    indicators.py
    atr.py
    ema.py
    bars.py
  v1_breakout/
    __init__.py
    config.py
    signals.py
    bias.py
    setup.py
    stops.py
    exits.py
    decisions.py
```

### Strategy boundary rule

The strategy layer may say:

- “a signal exists,”
- “this is the intended side,”
- “this is the proposed stop,”
- “this stop update is desired,”
- or “this exit intent exists.”

The strategy layer must not say:

- “the entry filled,”
- “a position exists,”
- “the stop is confirmed,”
- “reconciliation is clean,”
- or “the account is protected.”

Those are exchange-derived or state/reconciliation facts.

---

## `risk/`

### Purpose

Risk gating, stop-distance-based sizing, leverage-cap checks, symbol-rule checks, and exposure constraints.

### Owns

- per-trade risk validation,
- stop-distance validation,
- quantity and notional sizing,
- leverage-cap enforcement,
- symbol precision / increment checks at the risk layer,
- daily / session lockout gates where implemented,
- and risk rejection reasons.

### Does not own

- strategy signal generation,
- direct exchange order placement,
- exchange fill confirmation,
- or operator override logic.

### Suggested files

```text
risk/
  __init__.py
  models.py
  sizing.py
  gates.py
  limits.py
  symbol_rules.py
  decisions.py
```

### Risk rule

Position size must be derived from:

- account risk allowance,
- stop distance,
- symbol constraints,
- leverage constraints,
- and internal caps.

Leverage is a sizing constraint/tool, not a target.

---

## `exchange/`

### Purpose

Exchange-specific connectivity, request signing, REST clients, user-stream handling, market-stream handling, and Binance USDⓈ-M futures API adaptation.

### Owns

- Binance USDⓈ-M REST adapter,
- signed request support,
- exchange metadata retrieval,
- user-data stream lifecycle,
- exchange event normalization,
- exchange-specific response models,
- and low-level API error normalization.

### Does not own

- strategy logic,
- risk policy,
- operator policy,
- final reconciliation decisions,
- or long-term runtime state authority.

### Suggested files

```text
exchange/
  __init__.py
  interfaces.py
  errors.py
  models.py
  binance_usdm/
    __init__.py
    rest_client.py
    auth.py
    endpoints.py
    metadata.py
    normal_orders.py
    algo_orders.py
    account.py
    user_stream.py
    market_stream.py
    normalizers.py
    rate_limits.py
```

### Exchange boundary rule

Raw Binance-specific logic should be contained inside `exchange/binance_usdm/` as much as practical.

Other modules should interact through stable exchange interfaces and normalized exchange events, not through scattered raw endpoint calls.

---

## `execution/`

### Purpose

Convert approved strategy/risk intent into exchange-safe actions.

### Owns

- entry order submission workflow,
- protective stop submission workflow,
- stop cancel-and-replace workflow,
- market exit workflow,
- emergency flatten command handling,
- deterministic client order ID assignment at execution boundary,
- order-role tagging,
- exchange-rule compliance checks at order-expression time,
- and execution uncertainty events.

### Does not own

- strategy signal generation,
- risk approval policy,
- final position truth,
- final protection truth,
- reconciliation classification,
- or direct operator UI behavior.

### Suggested files

```text
execution/
  __init__.py
  models.py
  client_order_ids.py
  entry.py
  protective_stop.py
  stop_replacement.py
  exits.py
  emergency.py
  coordinator.py
```

### Execution rule

The execution layer may emit submission and uncertainty events.

It must not treat submission as final truth. Final fill, position, and protective-stop confirmation must come from exchange-derived events and/or reconciliation.

---

## `state/`

### Purpose

In-memory representation and controlled transition logic for runtime state.

### Owns

- runtime mode state,
- trade lifecycle state,
- protection state,
- reconciliation state references,
- incident/control flags,
- state transition validation,
- invalid state combination checks,
- and current-state read models used by runtime logic.

### Does not own

- raw persistence mechanism,
- direct exchange API calls,
- strategy calculations,
- or operator UI rendering.

### Suggested files

```text
state/
  __init__.py
  runtime.py
  trade_lifecycle.py
  protection.py
  reconciliation.py
  incidents.py
  transitions.py
  read_models.py
```

### State rule

State changes must occur through explicit controlled transitions driven by accepted events or approved control commands.

Hidden cross-module mutation is forbidden.

---

## `persistence/`

### Purpose

Durable storage for restart-critical runtime facts and operational continuity.

### Owns

- embedded runtime store interface,
- runtime control record persistence,
- active trade record persistence,
- protection record persistence,
- reconciliation record persistence,
- incident continuity persistence,
- operator action record persistence,
- schema/migration support,
- and durable-write helpers.

### Does not own

- historical research Parquet datasets,
- raw exchange API clients,
- strategy logic,
- or secret storage.

### Suggested files

```text
persistence/
  __init__.py
  interfaces.py
  runtime_store.py
  sqlite_store.py
  schemas.py
  migrations/
    __init__.py
```

### Persistence rule

Runtime persistence is safety-critical.

If losing a transition would make restart or recovery less safe, the state must be persisted durably before the runtime proceeds past that transition where practical.

Secrets must never be persisted in runtime operational records.

---

## `reconciliation/`

### Purpose

Compare local persisted/in-memory state with exchange truth and classify mismatches.

### Owns

- startup reconciliation workflow,
- mid-run reconciliation workflow,
- position comparison,
- open-order comparison,
- protective-stop comparison,
- mismatch classification,
- repair recommendations,
- and safe/unsafe continuation decisions.

### Does not own

- strategy signal generation,
- exchange REST implementation,
- raw order placement except through approved execution paths,
- or operator decisions.

### Suggested files

```text
reconciliation/
  __init__.py
  models.py
  snapshots.py
  compare.py
  classify.py
  repair.py
  workflow.py
```

### Reconciliation rule

Exchange state is authoritative for whether exposure, orders, and protective stops exist.

Local state is provisional until reconciliation confirms or repairs it.

---

## `safety/`

### Purpose

System-level safety controls, incident classification hooks, safe mode, kill switch, pause state, emergency branching, and entry-blocking decisions.

### Owns

- safe-mode enforcement,
- kill-switch behavior,
- operator pause state,
- entries-blocked gates,
- incident severity routing,
- emergency unprotected-position handling,
- and rules that prevent normal operation under uncertainty.

### Does not own

- raw exchange API calls,
- direct frontend control bypasses,
- strategy calculations,
- or persistence schemas.

### Suggested files

```text
safety/
  __init__.py
  modes.py
  gates.py
  incidents.py
  kill_switch.py
  pause.py
  emergency.py
```

### Safety rule

If the system cannot trust position state, protective-stop state, execution outcome, or required stream freshness, new entries must be blocked until certainty is restored.

---

## `operator/`

### Purpose

Backend operator-facing query and command surface.

### Owns

- runtime summary queries,
- position/protection summary queries,
- reconciliation summary queries,
- incident summary queries,
- recent important events query surface,
- approved operator command handlers,
- and backend guardrails for manual actions.

### Does not own

- raw exchange credentials in a frontend,
- direct Binance calls from UI,
- strategy overrides,
- or unapproved manual trade entry.

### Suggested files

```text
operator/
  __init__.py
  api.py
  commands.py
  queries.py
  read_models.py
  approvals.py
```

### Operator boundary rule

The operator surface must interact through backend-approved commands and read-only queries.

It must not bypass safety, reconciliation, execution, or permission-scoping boundaries.

---

## `runtime/`

### Purpose

Runtime orchestration and process lifecycle for the live-capable bot.

### Owns

- process startup,
- safe-mode-first initialization,
- dependency wiring,
- startup validation,
- runtime loop orchestration,
- stream startup coordination,
- graceful shutdown,
- and handoff between components.

### Does not own

- business logic that belongs in strategy, risk, execution, reconciliation, or safety modules,
- raw secret handling beyond calling the secrets loader,
- or monolithic all-in-one logic.

### Suggested files

```text
runtime/
  __init__.py
  app.py
  bootstrap.py
  lifecycle.py
  wiring.py
  shutdown.py
```

### Runtime rule

The runtime layer coordinates modules. It should not become the place where module boundaries are bypassed.

---

## `research/`

### Purpose

Historical data workflows, backtesting, validation, dataset assembly, and research reports.

### Owns

- historical data ingestion orchestration,
- normalized and derived dataset workflows,
- Parquet / DuckDB research utilities,
- backtest runners,
- validation runners,
- parameter sweep orchestration,
- and research report generation.

### Does not own

- live exchange order placement,
- live runtime state,
- production secrets,
- operator controls,
- or direct live trading behavior.

### Suggested files

```text
research/
  __init__.py
  data/
    __init__.py
    fetch.py
    normalize.py
    manifests.py
    quality.py
  backtesting/
    __init__.py
    engine.py
    fills.py
    costs.py
    metrics.py
    reports.py
  validation/
    __init__.py
    walk_forward.py
    holdout.py
    comparisons.py
    checklist.py
```

### Research/live boundary rule

Research code may reuse pure strategy calculations from `strategy/` and generic helpers from `core/`.

Research code must not depend on:

- `execution/`,
- `operator/`,
- `runtime/`,
- live `persistence/`,
- or production `secrets/`.

---

# Dependency Direction Rules

## Dependency principle

Dependencies should point inward toward stable primitives and outward only through explicit interfaces.

The codebase should avoid circular dependencies and hidden cross-module state access.

## Allowed high-level dependency direction

```text
core
  ↑
config / secrets / events / observability
  ↑
market_data / strategy / risk / exchange
  ↑
execution / state / persistence / reconciliation / safety
  ↑
runtime / operator
  ↑
cli / scripts
```

This diagram is directional and approximate. It does not mean every upper module may freely import every lower module. Specific boundary rules still apply.

## Strict boundary table

| Module | May depend on | Must not depend on |
|---|---|---|
| `core` | standard library only where practical | all project business modules |
| `config` | `core` | `exchange`, `execution`, `runtime`, `operator` |
| `secrets` | `core`, `config` | `strategy`, `execution`, `operator UI` |
| `events` | `core` | concrete runtime modules |
| `observability` | `core`, `events`, `secrets.redaction` | strategy decisions, exchange truth authority |
| `market_data` | `core`, `events`, exchange interfaces where needed | `execution`, `operator`, `reconciliation` |
| `strategy` | `core`, `market_data` models, `events` | `exchange`, `execution`, `persistence`, `operator`, `secrets` |
| `risk` | `core`, `strategy` outputs, exchange metadata models | `execution`, `operator`, raw Binance clients |
| `exchange` | `core`, `config`, `secrets`, `events`, `observability` | `strategy`, `risk`, `operator`, `reconciliation decisions` |
| `execution` | `core`, `events`, `risk` outputs, `exchange` interfaces, `observability` | `strategy signal generation`, `operator UI` |
| `state` | `core`, `events` | raw exchange clients, strategy calculations |
| `persistence` | `core`, `state` models, `events` | `secrets`, raw exchange clients, strategy calculations |
| `reconciliation` | `core`, `events`, `state`, `persistence`, `exchange` interfaces | strategy signal generation, operator UI bypass |
| `safety` | `core`, `events`, `state`, `persistence`, `observability` | raw exchange clients except through approved execution paths |
| `operator` | `core`, `events`, `state`, `safety`, `observability`, controlled command handlers | raw Binance clients, raw secrets |
| `runtime` | approved modules for wiring | business logic hidden inside runtime |
| `research` | `core`, `strategy`, research data tools | `runtime`, `execution`, `operator`, production secrets |

---

# Forbidden Coupling Patterns

The following patterns are explicitly forbidden.

## 1. Strategy imports exchange client

Forbidden:

```text
strategy/ imports exchange/binance_usdm/rest_client.py
```

Reason:

The strategy must not know how Binance orders are placed or confirmed.

## 2. Strategy mutates runtime state directly

Forbidden:

```text
strategy/ directly changes state.runtime_mode or state.trade_lifecycle
```

Reason:

Strategy emits decisions/intents. State transitions happen through controlled event handling.

## 3. Execution decides strategy validity

Forbidden:

```text
execution/ recomputes breakout validity or higher-timeframe bias
```

Reason:

Execution expresses approved intent. It does not decide market logic.

## 4. Operator surface calls Binance directly

Forbidden:

```text
operator/ or future frontend directly calls exchange/binance_usdm/rest_client.py
```

Reason:

Operator actions must pass through backend safety, permission, and audit paths.

## 5. Research code uses production runtime secrets

Forbidden:

```text
research/ loads production trade-capable credentials for convenience
```

Reason:

Research does not require production trade authority.

## 6. Persistence stores secrets

Forbidden:

```text
persistence/ stores API keys, API secrets, signatures, or secret-bearing config blobs
```

Reason:

Runtime persistence is for restart-critical operational state, not secret storage.

## 7. Queries mutate state

Forbidden:

```text
query.runtime_summary changes runtime state as a side effect
```

Reason:

Queries are read-only.

## 8. Events act as disguised commands

Forbidden:

```text
incident.opened event secretly means “place this order now”
```

Reason:

Commands request work. Events record facts.

## 9. Runtime becomes a god module

Forbidden:

```text
runtime/app.py contains strategy logic, risk sizing, exchange calls, persistence mutation, and UI logic all together
```

Reason:

The runtime coordinates modules. It must not erase module boundaries.

---

# Interface Surface Guidelines

Each major module should expose a small, intentional public interface.

## Preferred pattern

Each package should have:

- internal implementation files,
- typed models,
- and one or more clear interface files.

Examples:

```text
strategy/interfaces.py
risk/decisions.py
exchange/interfaces.py
persistence/interfaces.py
operator/queries.py
```

## Public API rule

Other modules should import from public interface/model files where practical, not from deep implementation internals.

Preferred:

```python
from prometheus.exchange.interfaces import ExchangeClient
```

Discouraged:

```python
from prometheus.exchange.binance_usdm.rest_client import _sign_request
```

## Interface stability rule

Interfaces should be stable enough that implementation details can change without forcing unrelated modules to change.

For example:

- the risk layer should not care whether exchange metadata came from REST, cache, or a fixture,
- the strategy layer should not care whether bars came from historical files or a live stream,
- the operator layer should not care whether runtime summaries are assembled from SQLite, memory, or an event log.

---

# Naming Conventions

## Python modules and files

Use snake_case:

```text
protective_stop.py
client_order_ids.py
runtime_store.py
```

## Classes

Use PascalCase:

```text
RuntimeState
TradeLifecycleState
ProtectiveStopSpec
RiskDecision
```

## Functions and variables

Use snake_case:

```text
compute_position_size
validate_stop_distance
last_successful_reconciliation_at_utc_ms
```

## Enums

Use PascalCase for enum classes and UPPER_SNAKE_CASE for values:

```text
RuntimeMode.SAFE_MODE
RuntimeMode.RUNNING_HEALTHY
ProtectionState.POSITION_PROTECTED
```

## Timestamp fields

All canonical timestamp fields should use UTC Unix milliseconds and should be named clearly:

```text
occurred_at_utc_ms
updated_at_utc_ms
signal_confirmed_at_utc_ms
last_successful_reconciliation_at_utc_ms
```

## Identifiers

Use explicit names for IDs:

```text
message_id
correlation_id
causation_id
trade_reference
client_order_id
exchange_order_id
incident_id
```

## Configuration names

Use explicit config versioning names:

```text
config_version
strategy_id
strategy_version
runtime_environment
```

## Environment variables

Use a consistent prefix:

```text
PROMETHEUS_ENV
PROMETHEUS_CONFIG_PATH
PROMETHEUS_BINANCE_API_KEY
PROMETHEUS_BINANCE_API_SECRET
PROMETHEUS_RUNTIME_DB_PATH
```

Secrets must still be handled under the secrets-management policy.

---

# Configuration and Secrets Layout

## Version-controlled config examples

The `configs/` directory may include example files:

```text
configs/
  dev.example.yaml
  validation.example.yaml
  paper.example.yaml
  production.example.yaml
```

These files should document expected configuration shape.

They must contain only fake, non-sensitive, or placeholder values.

## Non-versioned real config

Real environment-specific config may exist outside the repo or in gitignored files, depending on final setup.

Examples:

```text
configs/dev.local.yaml
configs/paper.local.yaml
configs/production.local.yaml
```

These should be gitignored if they may contain sensitive or environment-specific operational information.

## Secrets

Secrets should be loaded from controlled runtime inputs such as:

- environment variables,
- a secure local runtime config mechanism,
- or a future dedicated secrets manager.

Secrets must not be committed into:

- `configs/`,
- `docs/`,
- `scripts/`,
- tests,
- notebooks,
- logs,
- or runtime persistence records.

---

# Data and Runtime Artifact Layout

## `data/`

The local `data/` directory may be used for development and research artifacts.

Recommended local shape:

```text
data/
  raw/
  normalized/
  derived/
  manifests/
```

These paths should be treated as local/generated unless explicitly approved otherwise.

Large Parquet datasets should not be committed casually.

## `var/`

The local `var/` directory may be used for runtime artifacts.

Recommended local shape:

```text
var/
  runtime/
    prometheus_runtime.sqlite
  logs/
  reports/
  tmp/
```

Runtime artifacts should generally remain untracked.

## Runtime database location

The runtime database path should be configurable, with a safe local development default such as:

```text
var/runtime/prometheus_runtime.sqlite
```

Production deployment may choose a different path, but it must still satisfy the runtime persistence specification.

---

# Test Structure

Automated tests must mirror the architecture and safety boundaries.

Recommended layout:

```text
tests/
  unit/
    core/
    strategy/
    risk/
    state/
    safety/

  integration/
    persistence/
    reconciliation/
    execution/
    runtime_startup/

  contract/
    events/
    exchange/
    operator/

  simulation/
    restart_recovery/
    paper_shadow/
    backtest_parity/

  fixtures/
    market_data/
    exchange_events/
    runtime_state/
    configs/
```

## Unit tests

Unit tests should cover pure logic and local state transitions.

High-priority unit tests:

- ATR and EMA calculations,
- completed-bar alignment,
- v1 breakout setup detection,
- higher-timeframe bias rules,
- stop calculation,
- stop-distance validation,
- position sizing,
- runtime state transitions,
- protection state transitions,
- incident severity classification,
- and client order ID generation.

## Integration tests

Integration tests should cover interactions between modules.

High-priority integration tests:

- persistence write/read behavior,
- safe-mode startup state,
- restart after existing runtime state,
- reconciliation clean outcome,
- reconciliation recoverable mismatch outcome,
- reconciliation unsafe mismatch outcome,
- stop replacement workflow,
- and execution uncertainty handling.

## Contract tests

Contract tests should verify interface and schema promises.

High-priority contract tests:

- command/event/query envelope validation,
- message correlation requirements,
- exchange adapter normalized responses,
- user-stream normalized event shapes,
- operator query read models,
- and secret redaction behavior.

## Simulation tests

Simulation tests should test end-to-end behavior without real capital.

High-priority simulation tests:

- signal → risk approval → entry command path,
- entry fill → position confirmed → protective stop confirmed path,
- crash after fill before stop confirmation,
- crash during stop replacement,
- stale user stream while flat,
- stale user stream while exposed,
- open position with missing protective stop,
- and kill-switch persistence across restart.

## Test safety rule

Tests must not require production credentials.

Any test requiring exchange credentials must be clearly separated, opt-in, and must use non-production/test credentials only.

---

# Scripts Policy

Scripts may exist for convenience, but they must not become the real application.

## Allowed scripts

Examples:

```text
scripts/fetch_historical_data.py
scripts/run_backtest.py
scripts/run_validation.py
scripts/run_runtime.py
scripts/inspect_runtime_state.py
```

## Script rules

Scripts should:

- parse command-line arguments,
- load configuration,
- call package-level functions/classes,
- and exit with clear status codes.

Scripts should not:

- contain core strategy logic,
- contain exchange order workflows,
- hide persistence behavior,
- hardcode secrets,
- or bypass runtime safety gates.

---

# CLI Policy

The package-level CLI entry point should live at:

```text
src/prometheus/cli.py
```

The CLI may expose commands such as:

```text
prometheus fetch-data
prometheus backtest
prometheus validate
prometheus runtime start
prometheus runtime status
prometheus runtime reconcile
prometheus runtime pause
prometheus runtime kill-switch
```

## CLI boundary rule

CLI commands must call approved backend modules.

They must not directly mutate runtime state or call Binance in ways that bypass execution, safety, or reconciliation boundaries.

---

# Operator Interface Structure

The first implementation does not need a rich frontend.

The first operator surface may be:

- CLI summaries,
- structured status JSON,
- a small local backend API,
- or a simple dashboard later.

Regardless of UI form, the source structure should preserve the operator boundary:

```text
operator/
  commands.py
  queries.py
  read_models.py
  approvals.py
```

A future dashboard may be added later under a separate application directory, for example:

```text
apps/
  dashboard/
```

But the dashboard must still communicate through approved backend operator APIs. It must never hold raw exchange credentials or directly call Binance.

---

# Research and Runtime Separation

Research and live runtime are different system domains.

## Research world

Research code handles:

- historical data fetching,
- data normalization,
- dataset versioning,
- feature derivation,
- backtesting,
- validation,
- reports,
- and strategy comparison.

Research may use:

- `core/`,
- `strategy/`,
- research-specific data utilities,
- and controlled public market-data workflows.

Research must not use:

- `execution/`,
- live `runtime/`,
- production `secrets/`,
- operator controls,
- or live exchange trade authority.

## Live runtime world

Live runtime code handles:

- startup,
- exchange connectivity,
- user-stream lifecycle,
- order submission,
- protective stops,
- runtime state,
- reconciliation,
- incident handling,
- and operator controls.

Live runtime may reuse pure strategy calculation code, but it must not rely on research-only backtest assumptions as if they were live execution facts.

---

# Exchange Adapter Structure

The exchange adapter should be organized so Binance-specific details do not leak across the whole system.

Recommended structure:

```text
exchange/
  interfaces.py
  models.py
  errors.py
  binance_usdm/
    rest_client.py
    auth.py
    endpoints.py
    metadata.py
    normal_orders.py
    algo_orders.py
    account.py
    user_stream.py
    market_stream.py
    normalizers.py
    rate_limits.py
```

## Interface examples

The adapter should expose normalized operations such as:

- get exchange metadata,
- get leverage brackets,
- get commission rates where needed,
- submit normal order,
- submit algo order,
- cancel normal order,
- cancel algo order,
- query open orders,
- query position state,
- maintain user stream,
- normalize private events.

## Adapter rule

Binance-specific request/response details should be normalized before reaching strategy, risk, state, reconciliation, or operator modules.

---

# Persistence Structure

Runtime persistence should be structurally separate from research datasets.

Recommended structure:

```text
persistence/
  interfaces.py
  runtime_store.py
  sqlite_store.py
  schemas.py
  migrations/
```

## Required persistence entities

The code should support the runtime persistence records already defined in the persistence specification:

- runtime control record,
- active trade record,
- protection record,
- reconciliation record,
- incident continuity record,
- operator action records.

## Persistence boundary rule

Persistence stores restart-critical facts.

It should not become:

- a strategy analytics warehouse,
- a UI cache dumping ground,
- a secret store,
- or a replacement for exchange truth.

---

# Internal Event Structure

The codebase should implement internal events as typed models rather than scattered strings.

Recommended structure:

```text
events/
  envelope.py
  commands.py
  runtime_events.py
  exchange_events.py
  incident_events.py
  queries.py
  names.py
```

## Message envelope fields

Important command/event/query models should include fields such as:

- `message_type`,
- `message_class`,
- `message_id`,
- `correlation_id`,
- `causation_id`,
- `occurred_at_utc_ms`,
- `source_component`,
- `symbol` where relevant,
- `strategy_id` where relevant,
- and `payload` or typed payload fields.

## Event implementation rule

The first implementation does not need a complex external event bus.

An in-process dispatcher or explicit coordinator can be acceptable for v1 if it preserves:

- command/event/query distinction,
- component ownership,
- correlation IDs,
- persistence-critical write triggers,
- and observability records.

---

# Observability Structure

Observability should be implemented early and treated as part of the system, not as a later cosmetic layer.

Recommended structure:

```text
observability/
  logger.py
  event_recorder.py
  health.py
  alerts.py
  redaction.py
```

## Required observability outputs

The runtime should be able to expose at minimum:

- current runtime mode,
- entries allowed yes/no,
- current position/protection state,
- user-stream health,
- market-data health,
- exchange connectivity health,
- reconciliation state,
- active incidents,
- operator review required yes/no,
- recent important events,
- and last successful reconciliation timestamp.

## Redaction rule

Observability must integrate secret redaction by default.

It must not log raw secrets, signatures, full secret-bearing configuration, or sensitive credential payloads.

---

# Build Order Reflected in Codebase

The implementation should follow a staged order that matches the architecture.

## Phase A — shared foundations

Implement first:

- `core/`,
- `config/`,
- `secrets/`,
- `events/`,
- basic `observability/`,
- deterministic client-order-ID utility,
- time utilities.

## Phase B — strategy and risk foundations

Implement next:

- `market_data/` completed-bar models,
- `strategy/common/`,
- `strategy/v1_breakout/`,
- `risk/` sizing and validation.

## Phase C — research validation path

Implement next:

- `research/data/`,
- `research/backtesting/`,
- `research/validation/`,
- backtest and validation scripts.

## Phase D — exchange and execution foundations

Implement next:

- `exchange/interfaces.py`,
- `exchange/binance_usdm/`,
- `execution/entry.py`,
- `execution/protective_stop.py`,
- `execution/stop_replacement.py`,
- execution contract tests.

## Phase E — runtime state, persistence, and reconciliation

Implement next:

- `state/`,
- `persistence/`,
- `reconciliation/`,
- startup restore behavior,
- crash/restart tests.

## Phase F — safety and incident control

Implement next:

- `safety/`,
- incident classification,
- safe mode,
- pause,
- kill switch,
- emergency unprotected-position handling.

## Phase G — runtime orchestration and operator surface

Implement next:

- `runtime/`,
- `operator/`,
- CLI status/control commands,
- paper/shadow readiness hooks.

---

# Claude Code Implementation Constraints

This section is included because the codebase structure will be used as context for AI-assisted code generation.

Claude Code or any implementation assistant must follow these constraints.

## Must preserve module boundaries

Do not implement strategy, risk, exchange, execution, persistence, reconciliation, and operator logic in one file.

## Must not create hidden live-trading shortcuts

Do not create code paths where:

- strategy directly places orders,
- operator UI directly calls Binance,
- runtime startup skips reconciliation,
- command submission is treated as fill confirmation,
- or local state is treated as more authoritative than exchange state.

## Must not introduce premature scope expansion

Do not add:

- multi-symbol live orchestration,
- hedge mode,
- portfolio routing,
- autonomous AI decision loops,
- ML-driven live trade selection,
- tick/order-book execution optimization,
- or unattended lights-out live operation

unless a later approved document explicitly changes scope.

## Must prefer typed, testable interfaces

The implementation should use:

- typed models,
- explicit interfaces,
- clear return objects,
- deterministic tests,
- and dependency injection where helpful.

## Must keep secrets out of generated artifacts

Generated code, tests, docs, fixtures, and logs must not contain real credentials or realistic secret material.

## Must keep scripts thin

Scripts should call package modules and should not become untested business-logic containers.

---

# Open Implementation Choices

The following choices may still be finalized during implementation or in the AI coding handoff document.

## 1. Exact Python version

Recommendation:

- Python 3.11 or newer.

Rationale:

- modern typing support,
- mature async support,
- broad compatibility with data and API libraries.

## 2. Runtime store technology

Recommendation:

- SQLite for v1, unless implementation constraints justify another embedded transactional store.

Rationale:

- local,
- inspectable,
- durable,
- transactional,
- sufficient for one runtime / one symbol / one position v1.

## 3. Typed model library

Options:

- standard dataclasses,
- Pydantic,
- or a combination.

Recommendation:

- use a typed validation approach for external inputs, config, exchange events, and internal message contracts.

## 4. Async versus sync runtime style

Open implementation detail.

Likely direction:

- async may be useful for streams,
- but safety-critical state transitions should remain explicit and testable.

The project should not allow async complexity to obscure state ownership or persistence boundaries.

## 5. Dashboard implementation

The first implementation may start with CLI/operator status commands.

A richer dashboard can be added later, but it must remain behind backend-approved operator APIs.

---

# Acceptance Criteria for This Codebase Structure

The codebase structure is considered acceptable when it enables the following:

- [ ] source code lives under `src/prometheus/`,
- [ ] modules map clearly to documented architecture components,
- [ ] strategy logic is separate from exchange and execution logic,
- [ ] research code is separate from live runtime code,
- [ ] exchange-specific code is contained behind adapter boundaries,
- [ ] internal commands/events/queries are represented with typed contracts,
- [ ] runtime state has a clear module,
- [ ] runtime persistence has a clear module,
- [ ] reconciliation has a clear module,
- [ ] safety and incident controls have a clear module,
- [ ] operator controls cannot bypass backend safety paths,
- [ ] config examples are versioned without secrets,
- [ ] runtime artifacts and datasets are not accidentally committed,
- [ ] tests mirror architecture boundaries,
- [ ] scripts remain thin wrappers over package code,
- [ ] and Claude Code can follow the structure without inventing unsafe shortcuts.

---

# Decisions

The following decisions are accepted for the v1 codebase structure:

- v1 source code should live under `src/prometheus/`.
- Python is the recommended first implementation language.
- The codebase should be a modular monolith, not a distributed system.
- Runtime modules must reflect the architecture component boundaries.
- Strategy, risk, execution, exchange, state, persistence, reconciliation, safety, operator, and research code must be separated.
- Research and live runtime code must remain distinct domains.
- Binance-specific implementation should be isolated under `exchange/binance_usdm/`.
- Runtime persistence should be isolated under `persistence/` and should not mix with historical research storage.
- Internal command/event/query contracts should be typed and centralized under `events/`.
- Tests should be organized by unit, integration, contract, simulation, and fixtures.
- Operator controls must go through backend-approved command paths.
- Secrets must not be stored in code, docs, config examples, logs, tests, or runtime persistence.
- Scripts must remain thin wrappers over package modules.

---

# Next Steps

After this document, the next recommended document is:

```text
docs/00-meta/ai-coding-handoff.md
```

That document should define:

- how Claude Code should read the repository,
- what order it should implement modules in,
- which files it may create first,
- what tests it must generate with each implementation phase,
- what architecture constraints it must not violate,
- and how implementation progress should be reviewed before moving toward paper/shadow operation.

---

## Document Status

- Status: ACTIVE
- Owner: Project operator
- Role: Pre-implementation codebase structure contract
- Recommended path: `docs/08-architecture/codebase-structure.md`
