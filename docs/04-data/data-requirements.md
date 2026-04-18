# Data Requirements

## Purpose

This document defines the high-level data requirements for the v1 Prometheus trading system.

Its purpose is to connect the existing detailed data documents into one requirements index so that implementation, validation, operations, and setup work do not treat data handling as scattered assumptions.

This is a bridge document.

It does **not** duplicate the full schemas or detailed procedures already defined in:

- `docs/04-data/historical-data-spec.md`
- `docs/04-data/live-data-spec.md`
- `docs/04-data/timestamp-policy.md`
- `docs/04-data/dataset-versioning.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`

Instead, this document answers:

```text
What data must exist?
What data quality rules must be enforced?
Which document owns the detailed definition?
Which data requirements block validation, paper/shadow, tiny live, or coding readiness?
```

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- first secondary research comparison: ETHUSDT perpetual,
- strategy family: breakout continuation with higher-timeframe trend filter,
- signal timeframe: 15m,
- higher-timeframe bias: 1h,
- bar-close confirmation only,
- historical research uses reproducible datasets,
- live runtime uses completed bars only for strategy logic,
- all canonical timestamps use UTC Unix milliseconds,
- historical storage and runtime persistence are separate concerns,
- staged rollout proceeds from research to validation to paper/shadow to tiny live.

This document covers:

- canonical data principles,
- historical data requirements,
- live data requirements,
- timestamp and alignment requirements,
- dataset versioning requirements,
- validation data requirements,
- research vs runtime storage separation,
- data freshness and quality gates,
- setup/runbook topics for data bootstrap,
- and coding-readiness implications.

This document does **not** define:

- the full raw/normalized/derived schema,
- exchange API endpoint wrappers,
- runtime database schema,
- final data-ingestion code,
- exact local folder setup commands,
- exact DuckDB SQL views,
- or final dashboard implementation.

Those are defined elsewhere or should be implemented later.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/04-data/historical-data-spec.md`
- `docs/04-data/live-data-spec.md`
- `docs/04-data/timestamp-policy.md`
- `docs/04-data/dataset-versioning.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/event-flows.md`
- `docs/08-architecture/observability-design.md`
- `docs/11-interface/dashboard-metrics.md`
- `docs/12-roadmap/phase-gates.md`
- `docs/00-meta/ai-coding-handoff.md`

### Authority hierarchy

If this document conflicts with `historical-data-spec.md`, the historical data specification wins for historical dataset details.

If this document conflicts with `live-data-spec.md`, the live data specification wins for live market-data behavior.

If this document conflicts with `timestamp-policy.md`, the timestamp policy wins for all time-handling rules.

If this document conflicts with `dataset-versioning.md`, the dataset-versioning document wins for dataset manifests and version rules.

If this document conflicts with validation checklist requirements, the validation checklist wins for promotion-gate evidence.

If this document conflicts with runtime persistence/database design, the runtime persistence/database documents win for live runtime DB storage.

---

## Core Data Principles

## 1. Completed bars only

Strategy logic must use completed bars only.

This applies to:

- historical backtests,
- validation,
- dry-run,
- paper/shadow,
- tiny live,
- dashboard rule verification,
- and trade/setup chart annotations.

Partial candles may be displayed for operator context only if clearly labeled as forming.

They must not be used as confirmed strategy inputs.

## 2. UTC Unix milliseconds are canonical

All canonical timestamps must use UTC Unix milliseconds.

Human-readable timestamps may be displayed in reports or dashboard views, but they must be derived from canonical UTC millisecond timestamps.

## 3. `open_time` is the canonical bar key

Bar identity must be based on:

```text
symbol
interval
open_time
```

`close_time` should be retained where useful, but it is not the canonical bar identity.

## 4. Higher-timeframe alignment must be point-in-time valid

When 15m signal logic uses 1h higher-timeframe bias, the 1h bar must be the most recent fully completed 1h bar available at the 15m decision time.

The system must not use currently forming 1h candles for bias.

## 5. Historical and live behavior should remain comparable

Historical research and live runtime should use comparable logic:

- completed bars only,
- same timestamp rules,
- same higher-timeframe alignment principles,
- consistent symbol/interval semantics,
- explicit treatment of slippage/fills in validation,
- and documented differences where exact parity is impossible.

## 6. Dataset versions must be immutable

Once a normalized or derived dataset version is used for validation or decision-making, it should not be silently modified.

Corrections require a new dataset version.

## 7. Research storage and runtime database are separate

Historical data storage is for research and validation.

Runtime database storage is for live state, restart safety, auditability, orders, incidents, reconciliation, and operator actions.

They must not be merged into one ambiguous storage system.

---

## Required Historical Data

The detailed historical requirements are owned by `historical-data-spec.md`.

This document summarizes the implementation requirements.

## Required symbols

V1 historical research requires at least:

```text
BTCUSDT perpetual
ETHUSDT perpetual
```

BTCUSDT is the first live symbol.

ETHUSDT is the first secondary comparison symbol and must not be promoted to live trading unless separately approved.

## Required historical datasets

At minimum, research and validation require:

| Dataset | Purpose |
|---|---|
| Standard futures kline data | Primary OHLCV strategy/backtest data. |
| Derived 1h standard bars | Higher-timeframe bias for v1. |
| Mark-price kline data | Mark-price behavior, stop/slippage/liquidation context where applicable. |
| Funding-rate data | Funding/cost analysis and validation context. |
| Exchange-rule metadata | Tick size, step size, order constraints, symbol metadata. |

## Required interval focus

V1 strategy requires:

```text
15m signal timeframe
1h higher-timeframe bias
```

Historical storage may include additional intervals if useful, but v1 validation must clearly identify the intervals used.

## Historical data source policy

Historical datasets should be sourced from official Binance USDⓈ-M futures data where possible.

Any non-official or fallback source must be explicitly documented and should not silently mix with canonical datasets.

## Historical data must support

Historical data must support:

- strategy research,
- backtesting,
- validation reports,
- robustness checks,
- BTCUSDT vs ETHUSDT comparison,
- cost/funding review,
- trade replay,
- rule-conformity review,
- dashboard trade/setup chart reconstruction where feasible.

---

## Required Live Data

The detailed live requirements are owned by `live-data-spec.md`.

This document summarizes the implementation requirements.

## Mandatory live market data

V1 runtime requires live or live-like access to:

| Data | Purpose |
|---|---|
| BTCUSDT 15m kline stream or completed-bar source | Signal timeframe. |
| BTCUSDT 1h completed-bar source | Higher-timeframe bias. |
| Mark-price stream/source | Stop/protection context and dashboard visibility. |
| Exchange metadata refresh path | Symbol filters, precision, supported order types. |
| Private user stream | Order/account/algo events for live state. |

## Completed-bar publication

The live market-data layer must publish completed bars only to the strategy engine.

The live dashboard may show forming candles if labeled, but the strategy engine must not consume them as completed bars.

## Live freshness as trading gate

Market data freshness must affect trading permission.

If required market data is stale or unavailable:

```text
new entries must be blocked
```

If stale market data affects open-position management, the system must enter the appropriate degraded/recovery/incident path.

## User stream is not market data

Private user-stream events are live private state, not strategy market data.

They are required for:

- order lifecycle,
- fill confirmation,
- position updates,
- protective stop/algo events,
- state confidence,
- reconciliation triggers.

Live data setup must distinguish market streams from private account streams.

---

## Timestamp and Alignment Requirements

The detailed timestamp rules are owned by `timestamp-policy.md`.

Implementation and validation must enforce:

## Canonical timestamp requirements

- UTC timezone,
- Unix milliseconds,
- numeric canonical storage where possible,
- human-readable display derived from canonical timestamps.

## Bar requirements

- canonical bar key is `symbol + interval + open_time`,
- `close_time` retained where available,
- no local timezone storage for canonical data,
- no daylight-saving-time-dependent logic.

## Signal decision requirements

For v1:

```text
15m signal may be evaluated only after the 15m signal bar has fully closed.
1h bias may use only the most recent completed 1h bar available at that 15m decision time.
```

## Event-time and processing-time

Live data and execution events should track both where practical:

- exchange/event time,
- local processing time.

This supports latency analysis, stream-staleness detection, debugging, and incident review.

---

## Dataset Versioning Requirements

The detailed versioning rules are owned by `dataset-versioning.md`.

Implementation and research workflow must enforce:

## Versioned datasets

The following should be versioned when used for validation:

- normalized historical datasets,
- derived datasets,
- reusable validation views,
- feature datasets,
- backtest-ready datasets.

## Raw payload storage

Raw payload storage should preserve original source data where practical.

Raw payloads may not require the same semantic versioning as normalized datasets, but raw provenance must remain traceable.

## Dataset manifests

Each dataset version should have a manifest that records at least:

- dataset name,
- dataset version,
- source,
- symbol(s),
- interval(s),
- date range,
- schema version,
- generation code/reference,
- generation timestamp,
- quality checks,
- known issues,
- parent/raw dataset references.

## Immutability

A dataset version used in validation must not be silently edited.

Corrections create new versions.

## Experiment linkage

Backtests and reports must record which dataset version they used.

A validation result without dataset version linkage is not acceptable evidence for promotion.

---

## Validation Data Requirements

The detailed gate checks are owned by `v1-breakout-validation-checklist.md`.

This document summarizes the data-related requirements.

## Data integrity gate

Before strategy validation, data must pass checks for:

- expected symbols,
- expected intervals,
- required date ranges,
- duplicate bars,
- missing bars,
- timestamp monotonicity,
- OHLC sanity,
- volume sanity,
- timezone consistency,
- dataset version linkage,
- completed-bar-only validity.

## Strategy conformity gate

Validation must prove the strategy uses:

- completed 15m bars,
- correct 1h completed bias alignment,
- correct setup window,
- correct breakout confirmation,
- correct initial stop logic,
- correct no-trade filters,
- no look-ahead data.

## Simulation realism gate

Backtests must clearly define:

- next-bar-open fill assumption,
- fee assumptions,
- slippage assumptions,
- funding treatment,
- stop behavior assumptions,
- market vs mark price assumptions,
- limitations of the model.

## Paper/shadow readiness

Paper/shadow requires live-like data behavior:

- live market data freshness,
- completed-bar publication,
- dashboard visibility,
- runtime DB writes,
- fake/paper execution lifecycle,
- alerting for stale/missing data.

## Tiny-live readiness

Tiny-live requires data systems to be operationally reliable:

- market-data freshness gate,
- user-stream health visible,
- exchange metadata validated,
- restart/reconciliation behavior tested,
- dashboard shows stale/unknown state clearly,
- alerts work for market/user stream degradation.

---

## Research Storage Requirements

Historical research storage should support reproducible data analysis.

Recommended conceptual structure:

```text
data/
  raw/
    binance_usdm/
  normalized/
    binance_usdm/
  derived/
  manifests/
  validation/
  reports/
```

Exact setup paths and commands should be defined later in `first-run-setup-checklist.md`.

## Storage format

The project has already oriented toward:

- Parquet for data files,
- DuckDB for local analytical querying,
- manifests for dataset versions,
- reproducible dataset generation.

## Requirements

Research storage must support:

- append/preserve raw source data,
- generate immutable normalized versions,
- generate derived 1h bars,
- query data efficiently,
- reproduce validation runs,
- link reports to dataset versions.

## Not runtime DB

Research storage must not be used as the live runtime truth store.

Live runtime state belongs in the runtime database.

---

## Runtime Data Requirements

Runtime data requirements are owned by:

- `runtime-persistence-spec.md`,
- `database-design.md`,
- `observability-design.md`.

This document summarizes the data intersection.

Runtime database must store:

- runtime control state,
- active trade state,
- order records,
- protective stop records,
- position observations,
- reconciliation runs,
- incidents,
- operator actions,
- audit/runtime/exchange events,
- daily loss state,
- drawdown state,
- config/release references.

Runtime database should not store:

- raw historical datasets,
- full Parquet research data,
- API secrets,
- unredacted webhook tokens,
- arbitrary debug dumps,
- unsigned/unredacted private payloads.

---

## Live Data Quality Gates

The live runtime should enforce data-quality gates before allowing trading.

## Market-data gate

Block entries if:

- required 15m data stale/unavailable,
- required 1h bias data stale/unavailable,
- completed-bar publication uncertain,
- market-data timestamp alignment invalid,
- partial candle would be required to decide signal.

## User-stream gate

Block entries and reconcile if:

- user stream stale,
- listen key expired,
- private event gap detected,
- expected order/account/algo update missing,
- private stream cannot be trusted while state matters.

## Metadata gate

Block entries if:

- exchange metadata missing,
- tick/step size unknown,
- symbol status unknown,
- order type support unknown,
- price precision invalid,
- leverage/margin metadata unavailable.

## Dataset gate

Block validation promotion if:

- dataset version missing,
- manifest missing,
- data integrity checks fail,
- strategy report lacks dataset version,
- date range insufficient,
- BTCUSDT/ETHUSDT comparison incomplete where required.

---

## Dashboard and Review Data Requirements

The dashboard and review process require data outputs beyond raw strategy inputs.

Dashboard must be able to display:

- completed candles,
- forming candle if labeled,
- setup range,
- breakout bar,
- entry marker,
- stop lines,
- stop updates,
- exit marker,
- open normal orders,
- open algo/protective orders,
- position state,
- risk state,
- daily/drawdown state,
- stream freshness,
- reconciliation state,
- incidents and alerts.

Review reports should link:

- trade reference,
- signal time,
- dataset/live data source,
- bar references,
- strategy version,
- config version,
- risk decision,
- order/protection lifecycle,
- realized result,
- rule-conformity notes.

---

## Data Requirements by Project Phase

## Research

Required:

- historical BTCUSDT data,
- historical ETHUSDT comparison data,
- dataset manifests,
- reproducible backtest inputs,
- validation reports.

No production secrets required.

## Validation

Required:

- versioned datasets,
- integrity checks,
- strategy conformity checks,
- simulation assumptions,
- reports linked to dataset versions.

No live trading credentials required.

## Dry-run

Required:

- live or replayed market data,
- fake exchange adapter data,
- runtime DB writes,
- dashboard state data,
- alert/test events.

No production order-writing credentials required.

## Paper / shadow

Required:

- live market data,
- paper/simulated execution state,
- user-stream-like events if simulated,
- dashboard/alerts,
- restart/recovery data,
- event/audit records.

Production trade-enabled credentials should not be required.

## Tiny live

Required:

- live market data,
- private user stream,
- REST reconciliation,
- exchange metadata,
- runtime DB,
- dashboard/alerts,
- backups,
- audit logs,
- operator review records.

Production trade-enabled credentials only after phase-gate approval.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical tasks should be captured later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

## Historical data setup

- create data directory structure,
- configure raw/normalized/derived data paths,
- install DuckDB/Parquet dependencies,
- download or ingest official Binance historical data,
- generate normalized datasets,
- generate derived 1h bars,
- create dataset manifests,
- run data integrity checks.

## Validation setup

- run validation checklist,
- produce validation reports,
- link reports to dataset versions,
- store validation artifacts,
- compare BTCUSDT and ETHUSDT as required.

## Live data setup

- configure public market-data streams,
- configure mark-price stream,
- configure exchange metadata refresh,
- configure user-stream setup in dry-run/paper/live stages,
- test stale-data alerts,
- test completed-bar publication.

## Dashboard data setup

- verify chart panel receives completed candles,
- verify forming candles are labeled,
- verify open orders/protective stops display,
- verify stale data appears stale,
- verify trade/setup review panel can load sample trades.

## Runtime storage setup

- initialize runtime DB separately from research data,
- configure logs/audit paths,
- configure backup path,
- verify database backup/restore.

---

## Implementation Readiness Notes

Before Claude Code implementation begins, this document should help the coding handoff make these requirements explicit:

- implement data layer first,
- build ingestion and validation before strategy execution,
- prove historical data integrity before backtests,
- prove strategy logic against hand-checkable examples,
- build live runtime data handling before live execution,
- keep exchange write paths disabled until later phases,
- log ambiguity/spec gaps instead of guessing silently,
- use phased runnable checkpoints.

The coding handoff should not ask Claude Code to implement the full trading system in one monolithic step.

Data work should have its own acceptance criteria.

---

## Testing Requirements

## Historical data tests

Test:

- duplicate detection,
- missing bar detection,
- timestamp monotonicity,
- OHLC sanity,
- volume sanity,
- interval consistency,
- UTC millisecond storage,
- manifest presence,
- dataset version linkage.

## Alignment tests

Test:

- 15m completed-bar signal timing,
- 1h completed-bias selection,
- no partial 1h usage,
- no future bar leakage,
- strategy decision timestamps.

## Live data tests

Test:

- completed-bar publication,
- partial candle exclusion from strategy,
- stream stale detection,
- REST backfill/recovery behavior,
- mark-price freshness,
- metadata refresh,
- user-stream health state.

## Dashboard data tests

Test:

- stale values labeled,
- open orders displayed,
- protective stops displayed,
- chart overlays match trade records,
- completed vs forming candles distinguished,
- rule-check annotations align with strategy decisions.

## Dataset versioning tests

Test:

- manifest generation,
- version immutability,
- new version on schema/source change,
- reports link to dataset version,
- validation cannot proceed without version reference.

---

## Forbidden Patterns

The following are not allowed:

- using partial candles as confirmed strategy inputs,
- using local timezone as canonical time,
- using current forming 1h bar for 15m decision bias,
- silently modifying validation datasets,
- running validation without dataset manifests,
- mixing research storage with runtime DB truth,
- using dashboard-displayed forming candle as signal confirmation,
- treating market data as position/account truth,
- treating REST market data recovery as a substitute for private-state reconciliation,
- promoting to paper/tiny-live without data integrity checks,
- hiding stale data on dashboard,
- using unversioned datasets for promotion evidence,
- allowing Claude Code to guess unresolved data semantics silently.

---

## Non-Goals

This document does not define:

- exact schemas for every dataset,
- exact SQL queries,
- exact download commands,
- exact data vendor alternatives,
- exact Parquet partitioning implementation,
- exact dashboard charting implementation,
- exact runtime DB tables,
- exact Binance client code,
- or exact first-run setup commands.

It defines the bridge requirements and ownership map for data.

---

## Acceptance Criteria

`data-requirements.md` is complete enough for v1 when it makes the following clear:

- detailed historical data definitions live in `historical-data-spec.md`,
- detailed live data definitions live in `live-data-spec.md`,
- detailed timestamp rules live in `timestamp-policy.md`,
- detailed versioning rules live in `dataset-versioning.md`,
- validation evidence must satisfy `v1-breakout-validation-checklist.md`,
- BTCUSDT and ETHUSDT historical research requirements are explicit,
- completed bars only is a hard rule,
- UTC Unix milliseconds are canonical,
- 1h bias alignment must be point-in-time valid,
- historical research storage and runtime DB are separate,
- dataset manifests and version linkage are required,
- live market-data/user-stream freshness are trading gates,
- dashboard chart/review data must distinguish completed from forming candles,
- setup/bootstrap tasks are deferred to the first-run setup checklist,
- and Claude Code implementation should proceed through phased data checkpoints rather than one-shot full-system generation.
