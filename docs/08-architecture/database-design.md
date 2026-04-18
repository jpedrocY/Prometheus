# Database Design

## Purpose

This document defines the live runtime database design for the v1 Prometheus trading system.

Its purpose is to turn the project’s runtime persistence, state model, observability, event-contract, restart, reconciliation, risk-control, and incident-response requirements into an implementation-support storage design.

The runtime database exists so that Prometheus can:

- restart safely,
- preserve critical control state,
- journal exposure-changing intent before external exchange actions,
- track order, position, and protective-stop continuity,
- preserve reconciliation evidence,
- audit operator actions,
- support incident review,
- enforce daily loss and drawdown lockouts across restart,
- and provide a durable chronological record of important runtime behavior.

The runtime database is part of the safety system.

It is not a performance-reporting convenience feature.

---

## Scope

This design applies to the v1 Prometheus live runtime under the following assumptions:

- venue: Binance USDⓈ-M futures,
- first live symbol: BTCUSDT perpetual,
- first secondary research comparison symbol: ETHUSDT perpetual,
- v1 live symbol scope: BTCUSDT only,
- position mode: one-way mode,
- margin mode: isolated margin,
- one active strategy,
- one open position maximum,
- one active protective stop maximum,
- supervised staged deployment,
- exchange-side protective stop is mandatory,
- restart begins in safe mode,
- exchange state is authoritative,
- unknown execution outcomes fail closed.

This document covers:

- runtime database philosophy,
- runtime database engine recommendation,
- separation from historical research storage,
- current-state tables versus append-only audit/event tables,
- core entity design,
- table responsibilities,
- minimum fields,
- critical indexes and constraints,
- transaction and durability rules,
- startup read behavior,
- backup and restore expectations,
- migration expectations,
- retention guidance,
- testing requirements,
- and acceptance criteria.

This document does **not** define:

- historical Parquet/DuckDB research dataset schemas,
- full backtest result schema,
- complete frontend API schema,
- production cloud database infrastructure,
- exact SQL migration files,
- ORM implementation details,
- or long-term multi-strategy / multi-symbol portfolio storage.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/observability-design.md`
- `docs/08-architecture/event-flows.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/binance-usdm-order-model.md`
- `docs/06-execution-exchange/user-stream-reconciliation.md`
- `docs/06-execution-exchange/failure-recovery.md`
- `docs/06-execution-exchange/position-state-model.md`
- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/kill-switches.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/10-security/secrets-management.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/permission-scoping.md`
- `docs/11-interface/operator-dashboard-requirements.md`

### Authority hierarchy

If this document conflicts with the runtime persistence specification on what must survive restart, the runtime persistence specification wins.

If this document conflicts with the state model on runtime modes, lifecycle states, protection states, or reconciliation states, the state model wins.

If this document conflicts with execution/exchange documents on order or exchange-state semantics, the execution/exchange documents win.

If this document conflicts with risk documents on daily loss, drawdown, kill-switch, exposure, or stop policy, the risk documents win.

If this document conflicts with security documents on credential handling, redaction, or secret storage, the security documents win.

---

## Core Principles

## 1. The runtime database is part of the safety system

The runtime database preserves the local facts required for safe restart, deterministic reconciliation, operator accountability, and incident review.

If critical local state is lost, Prometheus must behave more conservatively after restart.

The database should therefore be designed as a safety component, not as a generic application cache.

## 2. Exchange truth outranks database truth

The runtime database stores Prometheus local state, prior observations, command intent, and audit history.

It does **not** become final truth for:

- whether a position exists,
- whether an order remains open,
- whether a protective stop still exists,
- whether an exchange action succeeded,
- or whether the account is safe.

Those facts must still be verified against exchange state during restart, reconciliation, and confidence-loss recovery.

## 3. Persist intent before external side effects

For any action that may create, reduce, cancel, repair, or otherwise change live exposure or protection, Prometheus must persist command intent before sending the external exchange request.

This is required because an exchange request and a local database write cannot be made truly atomic.

The next-best safety pattern is:

```text
1. Generate deterministic identifiers.
2. Persist command intent and in-flight state.
3. Commit.
4. Send exchange request.
5. Persist acknowledgement, rejection, timeout, or unknown outcome.
6. Reconcile if final truth is not established.
```

This pattern applies to:

- entry order submission,
- market exit order submission,
- emergency flatten submission,
- protective stop submission,
- protective stop cancellation,
- stop replacement,
- stale order cleanup,
- and any future exposure-changing command.

## 4. Current state and append-only history are both required

Prometheus should not rely only on append-only events and should not rely only on mutable current-state rows.

V1 should use both:

- current-state tables for fast restart and operator summaries,
- append-only event/audit tables for traceability and incident review.

This is simpler than pure event sourcing while still preserving auditability.

## 5. Commands are not facts

The database must preserve the distinction between:

- requested actions,
- submitted requests,
- acknowledged requests,
- exchange-derived facts,
- reconciled truth,
- and local control decisions.

For example:

```text
entry command persisted != entry filled
entry submitted != position confirmed
stop submitted != protection confirmed
cancel requested != stop canceled
flatten submitted != account flat
```

## 6. Unknown outcomes must be durable

If an exchange request may have reached Binance but Prometheus cannot determine its outcome, that uncertainty must be persisted immediately.

At minimum, the database must support:

```text
unknown_outcome = true
reconciliation_required = true
entries_blocked = true
```

The runtime must not continue in a way that forgets the uncertainty.

## 7. Operator actions must be audit-grade

Manual controls are safety-sensitive.

The database must preserve durable records for operator actions such as:

- pause activation / clearance,
- kill-switch activation / clearance,
- recovery approval,
- emergency flatten request,
- manual lockout override where allowed,
- release promotion approval,
- risk increase approval,
- and incident resolution.

Operator-action records should include who acted, when, why, what was requested, whether confirmation was required, and what state existed before/after the action.

## 8. Secrets must never be stored in runtime tables

The runtime database must not store:

- API keys,
- API secrets,
- listen-key secrets if treated as sensitive,
- signed request payloads,
- request signatures,
- raw authorization headers,
- private credentials,
- or unredacted exception traces containing secret material.

Raw exchange payloads may be retained only if redacted and safe.

Where useful, the database may store hashes of raw events for deduplication.

## 9. Timestamps use canonical UTC milliseconds

All runtime database timestamps used for logic must be stored as UTC Unix milliseconds.

Human-readable timestamps may be derived for reports and dashboard display, but must not replace canonical timestamp fields.

## 10. Schema design should preserve future migration options

V1 may use SQLite, but table naming, field naming, constraints, and JSON usage should remain disciplined enough that PostgreSQL migration is possible later.

Avoid SQLite-only assumptions where practical.

---

## Runtime Database vs Historical Research Storage

Prometheus has two separate storage domains.

## Historical research storage

Historical research storage is used for:

- Binance historical klines,
- mark-price klines,
- funding-rate history,
- exchange metadata snapshots,
- derived 1h bars,
- feature tables,
- validation views,
- backtest datasets,
- dataset manifests,
- reproducible research artifacts.

The historical research stack is based on:

```text
Parquet + DuckDB + explicit dataset versioning
```

It is analytical storage.

## Live runtime database

The live runtime database is used for:

- runtime control state,
- active trade continuity,
- order and protective-stop continuity,
- exchange-derived observations,
- reconciliation runs,
- incidents,
- operator actions,
- structured event logs,
- daily loss state,
- drawdown state,
- config and release references.

It is operational storage.

## Required separation

The live runtime database must not become the canonical historical kline store.

The runtime may record selected market-data health events and completed-bar event references, but it should not store the full historical market-data archive by default.

Likewise, research Parquet files must not be treated as live runtime state.

---

## Recommended V1 Database Engine

## Initial recommendation

The recommended v1 runtime database engine is:

```text
SQLite with WAL mode
```

The schema should be designed with PostgreSQL-compatible discipline where practical.

## Why SQLite is acceptable for v1

V1 is intentionally narrow:

- one primary runtime process,
- modular monolith,
- one live symbol,
- one active strategy,
- one open position maximum,
- one active protective stop maximum,
- supervised operation,
- modest write volume.

SQLite is sufficient for this scope if implementation uses:

- WAL mode,
- foreign keys enabled,
- explicit transactions,
- durable commits for safety-critical state,
- careful backup procedure,
- and disciplined migration files.

## Why not require PostgreSQL immediately

PostgreSQL is a strong future option, especially for:

- multi-process runtime architecture,
- remote dashboards,
- concurrent operators,
- multi-symbol trading,
- centralized audit storage,
- larger deployments.

But it adds v1 complexity:

- separate service management,
- additional credentials,
- network failure modes,
- more infrastructure hardening,
- more backup/restore complexity.

The v1 design should avoid this until the project has earned the operational complexity.

## PostgreSQL migration posture

Even if SQLite is used initially, the design should:

- avoid ambiguous dynamic typing in critical fields,
- use explicit migrations,
- avoid relying on rowid semantics for business identity,
- avoid storing critical relational data only inside JSON blobs,
- use stable primary keys,
- keep timestamps numeric and consistent,
- and isolate database access behind repository/service boundaries.

---

## Database Configuration Requirements

For SQLite v1, the runtime should configure:

```text
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = configured_nonzero_value;
```

The implementation should also consider:

```text
PRAGMA synchronous = FULL or NORMAL, stage-dependent;
```

For tiny live, safety-critical writes should favor durability over raw write speed.

The final implementation should document the selected `synchronous` value and why it is acceptable for the deployment stage.

---

## Data Ownership and Authority Rules

## Local database owns

The runtime database owns durable local records of:

- Prometheus command intent,
- local trade lifecycle state,
- known order identifiers,
- known stop identifiers,
- local control flags,
- operator actions,
- reconciliation attempts and outcomes,
- incident lifecycle,
- structured runtime events,
- normalized exchange events received or fetched,
- daily loss and drawdown control state,
- active config/release references.

## Exchange owns

The exchange remains authoritative for:

- live position existence,
- live position side and size,
- open normal orders,
- open algo/conditional orders,
- protective stop existence,
- filled order status,
- current account-side position facts.

## Derived runtime state

Some state may be derived from current-state rows and exchange observations, such as:

- dashboard summaries,
- entries allowed yes/no,
- active warning counts,
- operator action required yes/no,
- clean-flat summary.

Derived state may be cached for convenience, but the canonical restart-critical fields must still be stored explicitly where required by the persistence spec.

---

## Current-State Tables vs Append-Only Logs

## Current-state tables

Current-state tables store the latest local operational posture.

Examples:

- `runtime_control_state`
- `trades`
- `orders`
- `protective_stops`
- `reconciliation_runs`
- `incidents`
- `daily_loss_state`
- `drawdown_state`

These tables support:

- startup loading,
- dashboard current summaries,
- active-trade continuity,
- active-control decisions,
- safe-mode/recovery decisions.

## Append-only logs

Append-only or append-mostly tables preserve history.

Examples:

- `runtime_events`
- `exchange_events`
- `operator_actions`
- `incident_events`
- `state_transition_audit`

These tables support:

- incident reconstruction,
- deduplication,
- audit review,
- daily and weekly review,
- debugging delayed or duplicated exchange events,
- verifying that safety-critical state transitions had durable evidence.

## Mutation policy

Current-state rows may be updated.

Audit/event rows should generally not be updated except to add clearly controlled metadata such as:

- redaction status correction,
- archival marker,
- export marker,
- or schema migration bookkeeping.

Do not rewrite event history to hide mistakes.

---

## Timestamp and ID Policy

## Timestamp fields

Every operational table should include:

```text
created_at_utc_ms
updated_at_utc_ms
```

where applicable.

Events should also distinguish:

```text
occurred_at_utc_ms
processed_at_utc_ms
```

Exchange-derived events should preserve exchange event time where available.

## Business identifiers

The database should use stable business identifiers for workflows, not only integer primary keys.

Important identifiers include:

- `trade_reference`
- `signal_reference`
- `client_order_id`
- `exchange_order_id`
- `client_algo_id`
- `exchange_algo_id`
- `correlation_id`
- `causation_id`
- `incident_id`
- `reconciliation_id`
- `operator_action_id`
- `config_version`
- `release_version`

## Correlation IDs

Every important workflow should have a `correlation_id`.

Examples:

- one entry attempt,
- one trade lifecycle,
- one stop replacement,
- one restart reconciliation,
- one incident,
- one emergency flatten action,
- one operator approval workflow.

## Causation IDs

Where practical, important messages/events should record `causation_id` to link the immediate prior command/event that caused them.

---

## Redaction and Secret-Storage Prohibition

## Forbidden fields

The database must never store:

- API key values,
- API secret values,
- signatures,
- signed query strings,
- raw request headers containing credentials,
- unredacted environment variables,
- seed phrases or wallet-like secrets,
- password material,
- or sensitive host credentials.

## Exchange payload handling

Exchange payloads may be useful for debugging.

Allowed approach:

```text
normalized_payload_json
raw_payload_redacted_json
raw_event_hash
redaction_status
```

The raw payload must be redacted before storage.

If safe redaction cannot be guaranteed, store only:

- normalized fields,
- event hash,
- source,
- timestamps,
- and high-level status.

## Error handling

Exception messages should be sanitized before writing to persistent event tables.

If an exception may contain credentials or signed material, write a redacted error code/category and preserve detailed raw logs only if the logging system has confirmed safe redaction.

---

# Entity Overview

The v1 runtime database should include the following core table families.

| Family | Tables | Purpose |
|---|---|---|
| Runtime control | `runtime_control_state` | Current top-level operating posture. |
| Trade lifecycle | `trades`, `orders`, `protective_stops` | Local continuity for active and historical trade attempts. |
| Exchange observations | `position_observations`, `exchange_events` | Exchange-derived evidence and deduplication. |
| Reconciliation | `reconciliation_runs`, `reconciliation_findings` | Startup/recovery confidence restoration. |
| Incidents | `incidents`, `incident_events` | Incident lifecycle and audit. |
| Operator audit | `operator_actions` | Manual controls, approvals, overrides. |
| Runtime audit | `runtime_events`, `state_transition_audit` | Structured chronological runtime history. |
| Risk controls | `daily_loss_state`, `drawdown_state` | Persistent risk-control gates. |
| Versioning | `config_versions`, `release_versions` | Auditable config/release linkage. |

---

# Table 1 — `runtime_control_state`

## Purpose

Stores the current top-level runtime posture.

This is a singleton-style table.

It is restart-critical.

## Minimum fields

```text
id
runtime_mode
entries_blocked
entries_blocked_reason
paused_by_operator
kill_switch_active
incident_active
operator_review_required
reconciliation_required
active_strategy_id
config_version
release_version
last_started_at_utc_ms
last_clean_shutdown_at_utc_ms
last_safe_mode_entered_at_utc_ms
last_running_healthy_at_utc_ms
updated_at_utc_ms
created_at_utc_ms
```

## Field notes

### `runtime_mode`

Expected values should align with the state model, such as:

```text
SAFE_MODE
RUNNING_HEALTHY
RECOVERING
BLOCKED_AWAITING_OPERATOR
```

### `entries_blocked`

This may be derived from several conditions, but it should still be persisted because it is operationally important and useful on restart.

### `entries_blocked_reason`

Recommended as a concise enum or structured field such as:

```text
STARTUP_SAFE_MODE
KILL_SWITCH
OPERATOR_PAUSE
INCIDENT_ACTIVE
RECONCILIATION_REQUIRED
UNKNOWN_EXECUTION_OUTCOME
UNPROTECTED_POSITION
DAILY_LOSS_LOCKOUT
DRAWDOWN_PAUSE
STALE_STREAM
CONFIG_INVALID
```

### `kill_switch_active`

Must persist across restart.

Must never auto-clear.

### `paused_by_operator`

Must persist across restart.

### `operator_review_required`

Must persist across restart when active.

## Constraints

Recommended:

```text
primary key(id)
check(id = 1)
```

Only one row should exist.

## Critical write requirements

Update this table in the same transaction as the corresponding runtime event when:

- entering safe mode,
- leaving safe mode,
- entering recovery,
- blocking entries,
- clearing entries blocked,
- activating kill switch,
- clearing kill switch,
- enabling operator pause,
- clearing operator pause,
- setting operator review required,
- clearing operator review required,
- marking reconciliation required.

---

# Table 2 — `trades`

## Purpose

Stores Prometheus trade lifecycle records.

A trade row represents a strategy-approved or strategy-attempted workflow, not necessarily a completed live trade.

Rejected or aborted attempts may be stored if they reached a stage useful for audit or debugging.

## Minimum fields

```text
trade_reference
symbol
strategy_id
strategy_version
config_version
release_version
signal_reference
side
intended_quantity
approved_entry_reference_price
approved_stop_price
risk_fraction
risk_amount_usdt
risk_usage_fraction
max_effective_leverage
max_notional_usdt
trade_lifecycle_state
strategy_stage
risk_stage
trailing_stage
entry_submitted_at_utc_ms
entry_acknowledged_at_utc_ms
entry_fill_confirmed_at_utc_ms
position_confirmed_at_utc_ms
average_fill_price
position_size
position_side
protection_confirmed_at_utc_ms
exit_submitted_at_utc_ms
closed_at_utc_ms
close_reason
realized_pnl_usdt
fees_usdt
funding_usdt
created_at_utc_ms
updated_at_utc_ms
```

## Field notes

### `trade_reference`

Stable internal identifier for the trade lifecycle.

Should be included in related orders, stops, events, incidents, and operator actions.

### `trade_lifecycle_state`

Expected values should align with the state model, such as:

```text
FLAT
SIGNAL_CONFIRMED
ENTRY_SUBMITTED
ENTRY_ACKNOWLEDGED
ENTRY_FILL_CONFIRMED
POSITION_CONFIRMED
PROTECTIVE_STOP_SUBMITTED
POSITION_PROTECTED
RISK_STAGE_INITIAL
RISK_STAGE_REDUCED
RISK_STAGE_BREAKEVEN
RISK_STAGE_TRAILING
EXIT_PENDING
CLOSED
ABORTED
UNKNOWN
```

### `average_fill_price` and `position_size`

These are local last-known values.

They must be reconciled against exchange state where safety depends on them.

## Constraints

Recommended:

```text
primary key(trade_reference)
index(symbol)
index(strategy_id)
index(trade_lifecycle_state)
index(created_at_utc_ms)
```

Optional v1 invariant:

```text
At most one trade may be active at a time.
```

This may be enforced in application logic or with a partial unique index where supported.

## Important rule

The `trades` table is not exchange truth.

It is local lifecycle continuity.

---

# Table 3 — `orders`

## Purpose

Tracks normal Binance order continuity.

This table covers:

- entry market orders,
- market exit orders,
- emergency flatten orders,
- stale cleanup normal orders,
- any future approved normal-order action.

It does not track algo/conditional protective stops. Those belong in `protective_stops`.

## Minimum fields

```text
order_record_id
trade_reference
symbol
order_role
order_category
client_order_id
exchange_order_id
side
position_side
order_type
quantity
reduce_only
submission_state
order_status
last_known_exchange_status
unknown_outcome
reconciliation_required
submitted_at_utc_ms
acknowledged_at_utc_ms
rejected_at_utc_ms
terminal_at_utc_ms
last_checked_at_utc_ms
correlation_id
causation_id
error_category
error_code
error_message_redacted
created_at_utc_ms
updated_at_utc_ms
```

## Expected `order_role` values

```text
ENTRY
EXIT
EMERGENCY_FLATTEN
STALE_CLEANUP
UNKNOWN_EXTERNAL
```

## Expected `order_category`

```text
NORMAL
```

## Expected `submission_state` values

```text
PENDING_LOCAL_JOURNAL
SUBMITTING
SUBMITTED
ACKNOWLEDGED
REJECTED
UNKNOWN_OUTCOME
TERMINAL_CONFIRMED
```

## Constraints

Recommended:

```text
primary key(order_record_id)
unique(client_order_id)
unique(exchange_order_id) where exchange_order_id is not null
index(trade_reference)
index(symbol)
index(order_role)
index(unknown_outcome)
index(order_status)
```

## Critical rules

### Before exchange submission

An `orders` row must be committed before submitting a normal order to Binance.

At minimum, it must contain:

```text
trade_reference
symbol
order_role
client_order_id
side
order_type
quantity
correlation_id
submission_state
```

### Unknown outcome

If submission times out or returns an ambiguous result:

```text
unknown_outcome = true
reconciliation_required = true
submission_state = UNKNOWN_OUTCOME
```

The runtime must block new entries and reconcile.

---

# Table 4 — `protective_stops`

## Purpose

Tracks algo/conditional protective stop continuity.

This table covers:

- initial protective stops,
- replacement protective stops,
- canceled stops,
- triggered stops,
- stale stop cleanup,
- and stop-replacement groups.

## Minimum fields

```text
stop_record_id
trade_reference
symbol
stop_role
client_algo_id
exchange_algo_id
side
position_side
stop_type
trigger_price
working_type
price_protect
close_position
submission_state
stop_status
protection_state
replacement_group_id
previous_stop_record_id
unknown_outcome
reconciliation_required
submitted_at_utc_ms
acknowledged_at_utc_ms
confirmed_at_utc_ms
cancel_requested_at_utc_ms
cancel_confirmed_at_utc_ms
triggered_at_utc_ms
terminal_at_utc_ms
last_checked_at_utc_ms
correlation_id
causation_id
error_category
error_code
error_message_redacted
created_at_utc_ms
updated_at_utc_ms
```

## Expected `stop_role` values

```text
PROTECTIVE_STOP
REPLACEMENT_PROTECTIVE_STOP
STALE_CLEANUP
UNKNOWN_EXTERNAL
```

## Expected stop settings for v1

```text
stop_type = STOP_MARKET
working_type = MARK_PRICE
price_protect = true
close_position = true
```

## Expected `protection_state` values

Should align with the state model and stop-loss policy, such as:

```text
NO_PROTECTION
PROTECTION_SUBMITTED
PROTECTION_CONFIRMED
PROTECTION_REPLACEMENT_IN_PROGRESS
PROTECTION_UNCERTAIN
PROTECTION_FAILED
PROTECTION_TRIGGERED
PROTECTION_TERMINAL
```

## Constraints

Recommended:

```text
primary key(stop_record_id)
unique(client_algo_id)
unique(exchange_algo_id) where exchange_algo_id is not null
index(trade_reference)
index(symbol)
index(protection_state)
index(unknown_outcome)
index(replacement_group_id)
```

## Active stop invariant

For v1:

```text
For one active strategy-owned position, at most one active confirmed protective stop should exist.
```

This should be enforced by application logic and tested.

If the database supports partial unique indexes, the implementation may add one for active confirmed stops, but the exact condition should be chosen carefully to avoid blocking valid replacement history.

## Replacement tracking

Stop replacement must never overwrite the previous stop row.

A replacement creates a new stop row linked by:

```text
replacement_group_id
previous_stop_record_id
```

This preserves the chain:

```text
old stop -> cancel requested -> cancel confirmed/unknown -> new stop submitted -> new stop confirmed/failed
```

## Unknown cancel rule

If cancel status is unknown:

```text
unknown_outcome = true
reconciliation_required = true
protection_state = PROTECTION_UNCERTAIN
```

Do not assume canceled.

Do not assume still active.

Reconcile.

---

# Table 5 — `position_observations`

## Purpose

Stores exchange-derived position observations.

This table records what Prometheus observed from:

- REST position snapshots,
- user-stream `ACCOUNT_UPDATE` events,
- reconciliation reads,
- recovery reads.

It does not by itself prove that the bot may resume trading.

## Minimum fields

```text
observation_id
symbol
source
event_time_utc_ms
processed_at_utc_ms
position_side_raw
position_side_normalized
signed_position_size
absolute_position_size
entry_price
break_even_price
mark_price
notional_usdt
unrealized_pnl_usdt
liquidation_price
margin_type
isolated_wallet
isolated_margin
update_time_utc_ms
ownership_classification
raw_event_hash
created_at_utc_ms
```

## Expected `source` values

```text
REST_POSITION_RISK
ACCOUNT_UPDATE
REST_RECONCILIATION
STARTUP_RECONCILIATION
MANUAL_OPERATOR_REFRESH
```

## Expected normalized side values

```text
FLAT
LONG
SHORT
UNKNOWN
```

## Ownership classification

Suggested values:

```text
NO_POSITION
STRATEGY_POSITION
POSSIBLE_STRATEGY_POSITION
EXTERNAL_OR_MANUAL_POSITION
UNKNOWN_POSITION_OWNERSHIP
```

## Constraints

Recommended:

```text
primary key(observation_id)
index(symbol)
index(source)
index(event_time_utc_ms)
index(processed_at_utc_ms)
index(ownership_classification)
```

## Important rule

A fresh position observation is evidence.

It is not by itself a complete reconciliation result.

Clean flat requires position, order, protective stop, unknown-outcome, and mismatch checks.

---

# Table 6 — `reconciliation_runs`

## Purpose

Stores each reconciliation attempt and its outcome.

Reconciliation is required on:

- startup,
- restart,
- stale user stream,
- unknown execution outcome,
- local/exchange mismatch,
- stop uncertainty,
- manual/external exposure detection,
- operator-requested refresh where safety depends on result.

## Minimum fields

```text
reconciliation_id
reason
started_at_utc_ms
completed_at_utc_ms
status
classification
symbol
position_result
normal_order_result
algo_order_result
unknown_outcome_present
manual_or_external_exposure_present
repair_required
repair_action_taken
repair_status
operator_required
incident_opened
notes
created_at_utc_ms
updated_at_utc_ms
```

## Expected `status` values

```text
STARTED
IN_PROGRESS
COMPLETED
FAILED
ABORTED
```

## Expected `classification` values

```text
CLEAN
RECOVERABLE_MISMATCH
UNSAFE_MISMATCH
INCONCLUSIVE
```

## Constraints

Recommended:

```text
primary key(reconciliation_id)
index(reason)
index(status)
index(classification)
index(started_at_utc_ms)
index(completed_at_utc_ms)
```

## Critical rule

If reconciliation is required and does not complete cleanly or with a safely repaired recoverable mismatch, Prometheus must not enter `RUNNING_HEALTHY`.

---

# Table 7 — `reconciliation_findings`

## Purpose

Stores detailed findings for a reconciliation run.

One reconciliation run may have multiple findings.

## Minimum fields

```text
finding_id
reconciliation_id
finding_type
severity
symbol
related_trade_reference
related_order_record_id
related_stop_record_id
description
resolved
resolution_action
created_at_utc_ms
updated_at_utc_ms
```

## Expected finding examples

```text
LOCAL_EXPECTED_POSITION_EXCHANGE_FLAT
EXCHANGE_POSITION_LOCAL_FLAT
MISSING_PROTECTIVE_STOP
MULTIPLE_PROTECTIVE_STOPS
STALE_PROTECTIVE_STOP_WHILE_FLAT
UNKNOWN_ENTRY_ORDER_STATUS
MANUAL_POSITION_DETECTED
HEDGE_MODE_DETECTED
CROSS_MARGIN_DETECTED
OPEN_ORDER_UNCLASSIFIED
REST_QUERY_FAILED
```

## Constraints

Recommended:

```text
primary key(finding_id)
foreign key(reconciliation_id) references reconciliation_runs(reconciliation_id)
index(reconciliation_id)
index(finding_type)
index(severity)
index(resolved)
```

---

# Table 8 — `incidents`

## Purpose

Stores active and historical incidents.

An incident row captures the operational problem and its lifecycle.

Detailed incident activity may be stored in `incident_events` and `runtime_events`.

## Minimum fields

```text
incident_id
incident_class
severity
status
opened_at_utc_ms
contained_at_utc_ms
resolved_at_utc_ms
blocking
operator_review_required
related_trade_reference
related_reconciliation_id
related_order_record_id
related_stop_record_id
summary
resolution_summary
created_at_utc_ms
updated_at_utc_ms
```

## Expected `severity` values

```text
SEVERITY_1_INFORMATIONAL
SEVERITY_2_DEGRADED_CONTAINED
SEVERITY_3_TRADING_IMPAIRED
SEVERITY_4_EMERGENCY_EXPOSURE_RISK
```

## Expected `status` values

```text
OPEN
CONTAINED
BLOCKED_AWAITING_OPERATOR
RECOVERING
RESOLVED
CLOSED_AFTER_REVIEW
```

## Constraints

Recommended:

```text
primary key(incident_id)
index(status)
index(severity)
index(blocking)
index(opened_at_utc_ms)
```

## Critical rule

If an incident is active and blocking, the runtime control state must reflect that entries are blocked.

The incident row and runtime control update should be committed in the same transaction where practical.

---

# Table 9 — `incident_events`

## Purpose

Stores detailed lifecycle events for incidents.

## Minimum fields

```text
incident_event_id
incident_id
event_type
occurred_at_utc_ms
source_component
operator_identity
payload_json
payload_redaction_status
created_at_utc_ms
```

## Expected event types

```text
INCIDENT_OPENED
SEVERITY_ASSIGNED
CONTAINMENT_STARTED
CONTAINMENT_COMPLETED
RECONCILIATION_LINKED
OPERATOR_ESCALATED
OPERATOR_NOTE_ADDED
RECOVERY_ACTION_TAKEN
RESOLUTION_PROPOSED
RESOLVED
POST_INCIDENT_REVIEW_REQUIRED
CLOSED_AFTER_REVIEW
```

## Constraints

Recommended:

```text
primary key(incident_event_id)
foreign key(incident_id) references incidents(incident_id)
index(incident_id)
index(event_type)
index(occurred_at_utc_ms)
```

---

# Table 10 — `operator_actions`

## Purpose

Stores audit records for operator actions.

This table is required for manual-control accountability and approval workflows.

## Minimum fields

```text
operator_action_id
action_type
operator_identity
requested_at_utc_ms
confirmed_at_utc_ms
executed_at_utc_ms
status
requires_confirmation
confirmation_method
confirmation_token_or_hash
reason
related_incident_id
related_trade_reference
related_reconciliation_id
related_order_record_id
related_stop_record_id
pre_action_state_hash
post_action_state_hash
created_at_utc_ms
updated_at_utc_ms
```

## Expected `action_type` values

```text
ENABLE_PAUSE
CLEAR_PAUSE
ENABLE_KILL_SWITCH
REQUEST_KILL_SWITCH_CLEARANCE
CLEAR_KILL_SWITCH
APPROVE_RECOVERY_RESUMPTION
DENY_RECOVERY_RESUMPTION
REQUEST_EMERGENCY_FLATTEN
CONFIRM_EMERGENCY_FLATTEN
APPROVE_DAILY_LOCKOUT_OVERRIDE
APPROVE_DRAWDOWN_PAUSE_CLEARANCE
APPROVE_RISK_INCREASE
APPROVE_LEVERAGE_CAP_INCREASE
APPROVE_RELEASE_PROMOTION
ADD_OPERATOR_NOTE
```

## Expected `status` values

```text
REQUESTED
CONFIRMATION_REQUIRED
CONFIRMED
EXECUTED
DENIED
FAILED
CANCELED
```

## Constraints

Recommended:

```text
primary key(operator_action_id)
index(action_type)
index(operator_identity)
index(status)
index(requested_at_utc_ms)
```

## Critical write rule

For pause and kill-switch activation:

```text
Persist runtime control change first.
Append operator action and runtime event in the same transaction.
Only then acknowledge success to the operator.
```

---

# Table 11 — `runtime_events`

## Purpose

Stores append-only structured runtime events.

This is the main chronological audit stream for Prometheus behavior.

## Minimum fields

```text
event_id
message_type
message_class
correlation_id
causation_id
occurred_at_utc_ms
processed_at_utc_ms
source_component
symbol
strategy_id
trade_reference
severity
payload_json
payload_redaction_status
created_at_utc_ms
```

## Expected `message_class` values

```text
command
event
query
```

Most rows in `runtime_events` should be factual events. Commands may be logged where useful for audit.

## Expected event families

The table should support the observability event families, including:

- system/runtime events,
- market-data events,
- user-stream/account events,
- execution events,
- reconciliation/restart events,
- incident events,
- operator action events,
- review-support events.

## Constraints

Recommended:

```text
primary key(event_id)
index(message_type)
index(message_class)
index(correlation_id)
index(causation_id)
index(occurred_at_utc_ms)
index(source_component)
index(symbol)
index(trade_reference)
index(severity)
```

## Append-only rule

`runtime_events` should be append-only.

Do not modify existing rows to change historical meaning.

---

# Table 12 — `exchange_events`

## Purpose

Stores normalized exchange-derived events for deduplication and later review.

This table is especially useful for:

- user-stream duplicate events,
- delayed events,
- out-of-order events,
- reconciliation evidence,
- post-incident debugging.

## Minimum fields

```text
exchange_event_id
event_family
symbol
event_time_utc_ms
processed_at_utc_ms
source
client_order_id
exchange_order_id
client_algo_id
exchange_algo_id
event_hash
normalized_payload_json
raw_payload_redacted_json
redaction_status
created_at_utc_ms
```

## Expected `event_family` values

```text
ORDER_TRADE_UPDATE
ACCOUNT_UPDATE
ALGO_UPDATE
REST_ORDER_STATUS
REST_POSITION_SNAPSHOT
REST_OPEN_ORDERS
REST_OPEN_ALGO_ORDERS
REST_ACCOUNT_SNAPSHOT
UNKNOWN_EXCHANGE_EVENT
```

## Expected `source` values

```text
USER_STREAM
REST_RECONCILIATION
REST_RECOVERY
STARTUP_RECONCILIATION
```

## Constraints

Recommended:

```text
primary key(exchange_event_id)
unique(event_hash)
index(event_family)
index(symbol)
index(event_time_utc_ms)
index(processed_at_utc_ms)
index(client_order_id)
index(exchange_order_id)
index(client_algo_id)
index(exchange_algo_id)
```

## Dedupe rule

When processing exchange events:

```text
1. Compute event_hash from stable normalized payload components.
2. Insert into exchange_events.
3. If unique constraint reports duplicate, do not apply state transition again.
4. Still record a lightweight duplicate observation if useful for diagnostics.
```

This prevents duplicate fills or duplicate status updates from corrupting local state.

---

# Table 13 — `state_transition_audit`

## Purpose

Stores explicit before/after records for critical state transitions.

This table is optional if `runtime_events` and current-state tables already capture enough detail, but it is recommended for safety-critical transitions.

## Minimum fields

```text
transition_id
entity_type
entity_id
field_name
old_value
new_value
reason
correlation_id
causation_id
changed_at_utc_ms
source_component
created_at_utc_ms
```

## Use cases

Recommended for:

- runtime mode changes,
- entries blocked changes,
- trade lifecycle transitions,
- protection state transitions,
- reconciliation classification changes,
- incident status changes,
- kill-switch changes,
- operator pause changes,
- daily loss lockout changes,
- drawdown state changes.

## Constraints

Recommended:

```text
primary key(transition_id)
index(entity_type, entity_id)
index(changed_at_utc_ms)
index(correlation_id)
```

---

# Table 14 — `daily_loss_state`

## Purpose

Stores the current UTC daily risk-control state.

Daily loss state must survive restart and must not silently reset due to process restart.

## Minimum fields

```text
session_date_utc
daily_realized_pnl_usdt
daily_realized_pnl_fraction
consecutive_losing_trades_today
full_risk_losses_today
daily_risk_consumed_fraction
open_position_remaining_risk_fraction
daily_state
entries_blocked_by_daily_loss
warning_triggered_at_utc_ms
lockout_triggered_at_utc_ms
hard_review_triggered_at_utc_ms
updated_at_utc_ms
created_at_utc_ms
```

## Expected `daily_state` values

```text
NORMAL
WARNING
LOCKOUT
HARD_REVIEW
UNKNOWN
```

## Constraints

Recommended:

```text
primary key(session_date_utc)
index(daily_state)
index(entries_blocked_by_daily_loss)
```

## Reset rule

A new UTC day may create a new `daily_loss_state` row.

It must not clear:

- active kill switch,
- active incident,
- operator pause,
- unresolved reconciliation requirement,
- unprotected position state,
- operator review requirement.

---

# Table 15 — `drawdown_state`

## Purpose

Stores current longer-term drawdown control state.

Drawdown controls must survive restart.

## Minimum fields

```text
id
strategy_id
deployment_stage
strategy_equity_high_watermark_usdt
current_strategy_equity_usdt
strategy_drawdown_fraction
realized_drawdown_fraction
mark_to_market_drawdown_fraction
max_drawdown_fraction_since_deployment
max_drawdown_fraction_current_week
drawdown_state
entries_blocked_by_drawdown
risk_increase_blocked
operator_review_required
last_high_watermark_update_at_utc_ms
last_state_change_at_utc_ms
updated_at_utc_ms
created_at_utc_ms
```

## Expected `drawdown_state` values

```text
DRAWDOWN_NORMAL
DRAWDOWN_WATCH
DRAWDOWN_CAUTION
DRAWDOWN_PAUSE
DRAWDOWN_HARD_REVIEW
DRAWDOWN_ESCALATED_TO_INCIDENT
UNKNOWN
```

## Constraints

Recommended:

```text
primary key(id)
index(strategy_id)
index(deployment_stage)
index(drawdown_state)
index(entries_blocked_by_drawdown)
```

## Critical rule

Risk increases must be blocked when drawdown state requires caution, pause, hard review, or incident escalation.

---

# Table 16 — `config_versions`

## Purpose

Stores activated configuration identity and hashes.

This table helps answer:

```text
Which config produced this trade, order, incident, or runtime state?
```

## Minimum fields

```text
config_version
config_hash
strategy_version
risk_config_hash
execution_config_hash
deployment_config_hash
created_at_utc_ms
activated_at_utc_ms
deactivated_at_utc_ms
activated_by
activation_reason
notes
```

## Constraints

Recommended:

```text
primary key(config_version)
unique(config_hash)
index(strategy_version)
index(activated_at_utc_ms)
```

## Critical rule

Live config changes that affect risk, execution, symbol scope, stop behavior, or deployment stage must be versioned.

---

# Table 17 — `release_versions`

## Purpose

Stores deployed release identity.

This table links runtime behavior to code and documentation state.

## Minimum fields

```text
release_version
git_commit_hash
docs_version_reference
created_at_utc_ms
deployed_at_utc_ms
deployment_stage
deployed_by
rollback_from_release_version
notes
```

## Constraints

Recommended:

```text
primary key(release_version)
index(git_commit_hash)
index(deployed_at_utc_ms)
index(deployment_stage)
```

## Critical rule

A live deployment should record the release version before normal operation begins.

Restart logs and runtime events should include the active release version.

---

# Critical Write Flows

## Flow 1 — Startup safe-mode write

On process start:

```text
BEGIN TRANSACTION
  update runtime_control_state:
    runtime_mode = SAFE_MODE
    entries_blocked = true
    entries_blocked_reason = STARTUP_SAFE_MODE
    last_started_at_utc_ms = now
  insert runtime_events:
    message_type = runtime.started
    message_type = runtime.safe_mode_entered
COMMIT
```

Then startup prerequisites and reconciliation may begin.

The bot must not start directly into `RUNNING_HEALTHY` from persisted state.

## Flow 2 — Entry submission journaling

Before submitting an entry market order:

```text
BEGIN TRANSACTION
  insert trades if not already present
  insert orders:
    order_role = ENTRY
    client_order_id = deterministic ID
    submission_state = PENDING_LOCAL_JOURNAL
  update trades:
    trade_lifecycle_state = ENTRY_SUBMITTED or equivalent pending state
  insert runtime_events:
    execution.entry_submission_journaled
COMMIT
```

Then submit REST request.

After response:

```text
if ACK:
    persist acknowledged state
elif rejection:
    persist rejected terminal state
elif timeout/unknown:
    persist unknown_outcome = true
    set entries_blocked = true
    set reconciliation_required = true
```

## Flow 3 — Protective stop submission journaling

Before submitting protective stop:

```text
BEGIN TRANSACTION
  insert protective_stops:
    stop_role = PROTECTIVE_STOP
    client_algo_id = deterministic ID
    trigger_price = approved stop
    submission_state = PENDING_LOCAL_JOURNAL
  update trades:
    trade_lifecycle_state = PROTECTIVE_STOP_SUBMITTED
  insert runtime_events:
    protection.stop_submission_journaled
COMMIT
```

Then submit algo order.

Stop submission acknowledgement is not protection confirmation.

## Flow 4 — Stop replacement journaling

Before replacing a stop:

```text
BEGIN TRANSACTION
  create replacement_group_id
  mark current stop replacement state
  insert new protective_stops row for replacement stop
  insert runtime_events:
    protection.replacement_started
COMMIT
```

Then proceed through cancel-and-replace according to execution policy.

Do not overwrite the old stop row.

## Flow 5 — Exchange event processing

When user-stream or REST recovery produces an exchange-derived event:

```text
BEGIN TRANSACTION
  insert exchange_events by event_hash
  if duplicate:
      COMMIT without state mutation
  else:
      apply allowed state transition
      update current-state rows
      insert runtime_events
      optionally insert state_transition_audit
COMMIT
```

## Flow 6 — Unknown execution outcome

When unknown outcome occurs:

```text
BEGIN TRANSACTION
  update relevant orders/protective_stops:
    unknown_outcome = true
    reconciliation_required = true
  update runtime_control_state:
    runtime_mode = SAFE_MODE or RECOVERING
    entries_blocked = true
    entries_blocked_reason = UNKNOWN_EXECUTION_OUTCOME
    reconciliation_required = true
  insert runtime_events:
    execution.unknown_outcome_detected
    reconciliation.required
  optionally open incident
COMMIT
```

## Flow 7 — Kill-switch activation

When operator or automatic policy activates kill switch:

```text
BEGIN TRANSACTION
  update runtime_control_state:
    kill_switch_active = true
    entries_blocked = true
    operator_review_required = true
  insert operator_actions if operator-triggered
  insert runtime_events:
    kill_switch.activated
  insert state_transition_audit rows
COMMIT
```

Only after commit may the system acknowledge that the kill switch is active.

## Flow 8 — Incident opening

When incident opens:

```text
BEGIN TRANSACTION
  insert incidents
  insert incident_events:
    INCIDENT_OPENED
  update runtime_control_state if blocking
  insert runtime_events:
    incident.opened
COMMIT
```

## Flow 9 — Daily loss lockout

When trade closure updates daily loss:

```text
BEGIN TRANSACTION
  update daily_loss_state
  if threshold crossed:
      daily_state = LOCKOUT or HARD_REVIEW
      entries_blocked_by_daily_loss = true
      update runtime_control_state.entries_blocked = true
  insert runtime_events
  insert state_transition_audit where relevant
COMMIT
```

## Flow 10 — Drawdown pause

When drawdown state changes:

```text
BEGIN TRANSACTION
  update drawdown_state
  if pause/hard review:
      entries_blocked_by_drawdown = true
      risk_increase_blocked = true
      update runtime_control_state.entries_blocked = true
  insert runtime_events
COMMIT
```

---

# Startup Read Flow

On startup, Prometheus should:

## Step 1 — open database safely

- Open runtime DB.
- Enable foreign keys.
- Confirm schema version.
- Confirm WAL configuration where applicable.
- Verify database file permissions where applicable.

## Step 2 — enter safe mode

Before exchange reconciliation, write safe-mode state as described above.

## Step 3 — read persisted control state

Load:

- kill switch,
- operator pause,
- active incident flag,
- operator review required,
- previous runtime mode,
- previous config and release version,
- reconciliation required flag.

These values guide recovery, but do not allow direct healthy resumption.

## Step 4 — read active trade continuity

Load active or recent unresolved rows from:

- `trades`,
- `orders`,
- `protective_stops`,
- `reconciliation_runs`,
- `incidents`.

## Step 5 — reconstruct local expectations

Build a provisional local expectation such as:

```text
expected flat
expected entry in flight
expected position exists
expected protective stop exists
unknown outcome exists
operator review required
```

## Step 6 — query exchange

Use exchange adapter to fetch:

- current BTCUSDT position,
- open normal orders,
- open algo orders,
- and any required order details.

## Step 7 — reconcile

Create a `reconciliation_runs` row and classify:

```text
CLEAN
RECOVERABLE_MISMATCH
UNSAFE_MISMATCH
INCONCLUSIVE
```

## Step 8 — only then consider healthy mode

Prometheus may enter `RUNNING_HEALTHY` only when:

- reconciliation is acceptable,
- no kill switch is active,
- no operator pause is active,
- no blocking incident is active,
- no operator review is required,
- required streams are trusted,
- and if a position exists, protection is confirmed.

---

# Backup and Restore Expectations

## Backup purpose

Runtime DB backups exist to support:

- incident review,
- host recovery,
- rollback investigation,
- continuity after disk/host failure.

Backups do not replace exchange reconciliation.

## Backup minimum

The system should support safe backup of:

- runtime database file,
- WAL file where applicable,
- migration files,
- active config version,
- active release version,
- and relevant non-secret runtime configuration.

## Backup timing

Recommended backup moments:

- before release deployment,
- after clean shutdown,
- after incident resolution,
- daily during active deployment,
- before risky migration,
- before rollback.

## Restore rule

After restoring a runtime database backup:

```text
Prometheus must start in safe mode and reconcile exchange state before any strategy resumption.
```

A restored database may be stale relative to exchange state.

Exchange state wins.

---

# Retention Policy

V1 retention can be simple but must be explicit.

## Current-state rows

Keep current-state rows indefinitely or until replaced by formal archival/migration.

## Runtime events

Keep all runtime events for the lifetime of v1 unless storage constraints become material.

## Exchange events

Keep exchange events at least through the review period for the deployment stage.

Recommended v1 default:

```text
retain all exchange_events during paper, tiny-live, and early scaled-live stages
```

## Incidents and operator actions

Keep indefinitely.

These are audit records.

## Historical market data

Do not store full historical market data in runtime DB by default.

That belongs in the historical research data stack.

---

# Migration Policy

## Migration requirement

All schema changes must be performed through explicit migration files.

Avoid ad hoc runtime schema modification.

## Migration metadata

The database should include a migration tracking mechanism such as:

```text
schema_migrations
```

Minimum fields:

```text
migration_id
applied_at_utc_ms
checksum
notes
```

## Migration safety

Before applying migrations in live-capable environments:

- bot must not be actively opening new exposure,
- backup should be taken,
- release/version should be recorded,
- migration result should be logged,
- startup after migration must still enter safe mode and reconcile.

## Breaking migrations

Breaking migrations require:

- release note,
- rollback plan,
- test migration on representative database copy,
- explicit operator approval for live-capable stages.

---

# Testing Requirements

## Unit tests

The implementation should test:

- table creation,
- constraints,
- foreign keys,
- unique client order IDs,
- unique client algo IDs,
- exchange event dedupe,
- singleton runtime control behavior,
- enum validation where implemented.

## Transaction tests

Required transaction tests:

- entry intent persists before mocked exchange submission,
- protective stop intent persists before mocked exchange submission,
- unknown outcome persists and blocks entries,
- kill switch persists before acknowledgement,
- operator pause persists before acknowledgement,
- runtime state update and runtime event write occur atomically,
- duplicate exchange event does not double-apply state mutation.

## Restart tests

Required restart tests:

- restart always writes safe mode first,
- kill switch survives restart,
- operator pause survives restart,
- active incident survives restart,
- unknown execution outcome survives restart,
- active trade/protection continuity can be loaded,
- clean flat is not assumed from local DB alone,
- restored backup still requires reconciliation.

## Reconciliation tests

Required reconciliation DB tests:

- clean reconciliation records `CLEAN`,
- recoverable mismatch records repair result,
- unsafe mismatch blocks entries,
- missing protective stop opens/links incident where required,
- external/manual exposure classification persists,
- multiple protective stops classification persists.

## Incident and audit tests

Required incident/audit tests:

- incident open updates control state when blocking,
- incident resolution does not clear kill switch automatically,
- operator action records required confirmation,
- emergency flatten request is auditable,
- recovery approval links to reconciliation run.

## Redaction tests

Required redaction tests:

- API keys are never written to DB,
- API secrets are never written to DB,
- signed payloads are never written to DB,
- raw exchange payload storage is redacted or omitted,
- exception payloads are sanitized.

---

# Critical Invariants

The implementation should enforce and test these invariants:

```text
1. Runtime always starts in SAFE_MODE.
2. Kill switch survives restart.
3. Operator pause survives restart.
4. Active blocking incident survives restart.
5. Unknown execution outcome blocks entries.
6. Position without confirmed protection cannot be represented as healthy.
7. Stop submission is not protection confirmation.
8. Stop cancellation request is not cancellation confirmation.
9. Stop replacement preserves old and new stop records.
10. Duplicate exchange event does not double-apply fills or state transitions.
11. Clean flat requires no position, no open strategy orders, no active stop, no unknown outcome, and no unresolved mismatch.
12. Runtime DB never stores secrets or signed request material.
13. Runtime state transition and corresponding audit event are committed together where practical.
14. Operator kill-switch activation is persisted before success is shown to the operator.
15. Daily loss lockout survives restart until its policy reset conditions are met.
16. Drawdown pause / hard review survives restart until explicitly cleared by policy.
17. Restored DB backup does not allow direct healthy resumption without reconciliation.
```

---

# Non-Goals

This database design does not attempt to provide:

- full analytical market-data warehouse,
- full tax/accounting ledger,
- high-frequency tick storage,
- multi-strategy portfolio accounting,
- generalized trade journal UI,
- order-book history,
- cloud-native distributed event store,
- enterprise SIEM replacement,
- or permanent raw secret-bearing payload archive.

Those may be considered later only after v1 proves stable.

---

# Open Questions

These questions should be resolved during implementation or before live deployment:

1. Exact SQLite `synchronous` setting for paper, tiny live, and scaled live.
2. Whether to implement `state_transition_audit` as a separate table or rely on `runtime_events` plus current-state history.
3. Exact enum implementation method in Python and database migrations.
4. Exact database backup location and encryption policy.
5. Exact retention period once live runtime history becomes large.
6. Whether operator identity is local-only initially or integrated with stronger authentication later.
7. Whether the dashboard reads directly from DB in v1 or only through backend read models.
8. Exact migration framework selected by Claude Code.

None of these open questions should weaken the core safety rules.

---

# Acceptance Criteria

This document is satisfied when the implementation provides a runtime database that can:

- persist runtime control state across restart,
- persist active trade, order, and protective-stop continuity,
- journal exposure-changing intent before exchange calls,
- persist unknown execution outcomes and block entries,
- record exchange-derived events with deduplication,
- record reconciliation attempts and outcomes,
- record incidents and operator actions,
- preserve daily loss and drawdown lockout state,
- link trades and runtime behavior to config/release versions,
- support safe-mode-first restart,
- support post-incident review,
- avoid storing secrets,
- and pass tests for the critical invariants listed above.

The implementation should be considered incomplete if it can place orders but cannot reconstruct, after a restart, why it believed a position existed, whether that position was protected, what exchange actions were in flight, whether an unknown outcome existed, and whether operator review was required.
