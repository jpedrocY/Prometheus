# Historical Data Specification

## Purpose

This document defines the historical data contract for the v1 research and backtesting environment.

Its purpose is to make historical research:

- reproducible,
- auditable,
- point-in-time correct,
- and consistent across strategy design, backtesting, validation, and later implementation.

This specification exists because a rules-based trading system can be invalidated quietly by weak data discipline long before any code bug is obvious.

## Scope

This document defines:

- the canonical historical data source policy,
- the required datasets for v1 research,
- the distinction between fetched and derived datasets,
- the storage-layer model,
- the key schema and identity principles,
- the timestamp and time-alignment rules at the data-contract level,
- the gap and invalidity policy,
- and the recommended directory layout.

This document does **not** define:

- live ingestion behavior,
- exchange execution-state storage,
- full feature-engineering rules,
- final backtest implementation code,
- or full observability / monitoring design.

Detailed timestamp governance is defined separately in `docs/04-data/timestamp-policy.md`.

Detailed dataset-versioning governance is defined separately in `docs/04-data/dataset-versioning.md`.

## Background

The project is currently targeting:

- Binance USDⓈ-M futures,
- BTCUSDT as the primary symbol,
- ETHUSDT as the first secondary comparison symbol,
- 15m signal logic,
- 1h higher-timeframe bias,
- and a rules-based breakout continuation strategy.

Because the v1 strategy depends on:

- completed 15m breakout-bar confirmation,
- higher-timeframe context from completed 1h bars,
- conservative next-bar-open baseline fills in backtests,
- and realistic funding / fee / slippage treatment,

the historical dataset must be internally consistent and point-in-time trustworthy.

Historical research becomes unreliable quickly when:

- multiple data vendors are mixed without explicit reconciliation,
- 1h context is built inconsistently,
- timestamps are handled loosely,
- missing bars are silently repaired,
- or metadata assumptions are inferred rather than snapshotted.

## Canonical Source Policy

## Primary source

For v1 research, the canonical historical source is:

- **official Binance USDⓈ-M futures endpoints only**

This means the project uses Binance-provided historical and rule data as the base truth for the first research environment.

## Why this policy is selected

Using a single canonical venue source reduces avoidable inconsistency.

It helps avoid:

- mismatched timestamp conventions,
- inconsistent candle construction,
- differing vendor adjustment rules,
- and silent differences in mark-price or funding data.

## Included official source categories

The historical research stack should use official Binance USDⓈ-M endpoints for:

- standard futures klines,
- mark-price klines,
- funding-rate history,
- exchange information,
- leverage brackets,
- and commission rates.

## Required Datasets

The required datasets below are grouped by function and by whether they are:

- **fetched canonical datasets**, or
- **derived research datasets**

This distinction matters because the project wants a clean audit trail between source data and internal research views.

## 1. Standard futures kline dataset

This is the primary market-price dataset for the strategy.

### Dataset role
- **fetched canonical dataset**

### Required symbols
- BTCUSDT
- ETHUSDT

### Required fetched interval
- 15m

### Intended use
This dataset is used for:

- setup detection,
- breakout detection,
- ATR calculations,
- entry-timing logic,
- baseline fill timing,
- and the derivation of 1h higher-timeframe context.

### Canonical status
This is the primary price dataset for v1 strategy research.

### Important rule
For v1 research, the canonical fetched strategy-price dataset is:

- **standard futures klines**
- at **15m**
- from official Binance USDⓈ-M futures endpoints

## 2. Derived 1h standard-bar dataset

This is the required higher-timeframe context dataset for the strategy.

### Dataset role
- **derived research dataset**

### Required symbols
- BTCUSDT
- ETHUSDT

### Required derived interval
- 1h

### Intended use
This dataset is used for:

- higher-timeframe trend-bias calculations,
- 1h EMA calculations,
- 1h normalized ATR regime filters,
- and point-in-time alignment with 15m decision timestamps.

### Preferred construction rule
The preferred v1 policy is:

- derive **1h bars internally from the canonical 15m standard futures kline dataset**

### Why this policy is selected
This keeps the research stack internally consistent.

Benefits include:

- one canonical fetched bar source,
- fewer silent mismatches,
- easier reproducibility,
- easier auditability,
- and simpler comparison between signal data and higher-timeframe context.

### Optional sanity-check input
Directly fetched 1h standard futures klines may be retrieved for audit or sanity-check purposes, but they are not the preferred primary research base.

If such comparisons are performed, they should be treated as validation inputs, not as the canonical strategy dataset.

## 3. Mark-price kline dataset

This is a separate reference-price dataset.

### Dataset role
- **fetched canonical dataset for stop-sensitivity research**

### Required symbols
- BTCUSDT
- ETHUSDT

### Required fetched interval for phase 1
- 15m

### Intended use
This dataset is used for:

- stop-behavior sensitivity analysis,
- comparison between trade-price-driven and mark-price-driven protective logic,
- and research into protective-stop realism.

### Important rule
Mark-price klines must be stored separately from standard futures klines.

They are **not** a replacement for the main signal dataset.

### Phase-1 scope rule
For v1 phase-1 research, the minimum required mark-price dataset is:

- **15m mark-price klines**

A derived or directly fetched 1h mark-price view may be added later if needed for specific sensitivity analysis, but it is not required to define the initial historical contract.

## 4. Funding-rate dataset

This is an event-based dataset, not a bar dataset.

### Dataset role
- **fetched canonical dataset**

### Required symbols
- BTCUSDT
- ETHUSDT

### Intended use
This dataset is used for:

- funding-cost modeling,
- long/short carry analysis,
- and realistic net-PnL calculation in backtests.

### Important rule
Funding must be stored as a separate event table keyed by funding timestamp.

It must **not** be flattened into candle rows during ingestion.

## 5. Exchange-rule metadata dataset

This is a snapshot dataset.

### Dataset role
- **fetched canonical snapshot dataset**

### Required data
- symbol information
- price precision
- quantity precision
- minimum and maximum quantity rules
- notional and filter rules
- order-type availability where relevant

### Intended use
This dataset is used for:

- validating research assumptions,
- checking whether simulated sizes would be tradable,
- and aligning future execution logic with exchange constraints.

### Important rule
This data should be stored as time-stamped snapshots.

## 6. Leverage-bracket metadata dataset

This is a snapshot dataset.

### Dataset role
- **fetched canonical snapshot dataset**

### Required data
- symbol-level leverage bracket information
- notional bracket limits
- maintenance-related bracket structure where available

### Intended use
This dataset is used for:

- bracket-aware sizing research,
- realistic leverage-cap validation,
- and later risk-engine design.

### Important rule
This data should also be stored as time-stamped snapshots.

## 7. Commission-rate metadata dataset

This is an account-related snapshot dataset.

### Dataset role
- **fetched canonical snapshot dataset**

### Required data
- symbol-specific commission rates where applicable

### Intended use
This dataset is used for:

- realistic fee assumptions in backtests,
- and later account-specific cost calibration.

### Important rule
Commission assumptions must be explicit and saved as snapshots rather than silently assumed.

## Fetched vs Derived Dataset Policy

## Core principle

The historical research stack must distinguish clearly between:

- **fetched canonical datasets**
- and
- **derived research datasets**

### Fetched canonical datasets for v1

These are the primary source datasets:

- standard futures klines at 15m
- mark-price klines at 15m
- funding-rate history
- exchange-info snapshots
- leverage-bracket snapshots
- commission-rate snapshots

### Derived research datasets for v1

These are built internally from fetched canonical datasets:

- derived standard 1h bars
- derived volatility tables
- derived validation views
- derived feature tables
- any later regime or analysis tables

## Why this distinction is required

This makes it possible to answer clearly:

- what came directly from Binance,
- what was derived internally,
- which logic created the derived dataset,
- and which dataset version a research result actually used.

## Storage Architecture

The historical data stack should use a three-layer model.

## 1. Raw layer

The raw layer stores:

- original API payloads,
- fetch timestamps,
- endpoint metadata,
- request context where practical,
- and enough source information to support reprocessing and audit.

### Rules
- raw payloads should be treated as immutable
- no silent cleaning in the raw layer
- preserve source fidelity as much as practical

### Purpose
The raw layer exists for:

- auditability,
- reproducibility,
- debugging,
- and reprocessing.

## 2. Normalized layer

The normalized layer stores:

- typed,
- cleaned,
- schema-stable,
- analysis-ready tables
- built directly from canonical fetched datasets.

### Canonical format
The canonical normalized format is:

- **Parquet**

### Normalized-layer scope for v1
The normalized layer should contain at minimum:

- standard futures klines at 15m
- mark-price klines at 15m
- funding-rate events
- metadata snapshots

### Why Parquet is selected
Parquet is efficient for analytical workloads, compresses well, and fits the project’s file-based research design.

## 3. Derived layer

The derived layer stores:

- internally aggregated 1h bars,
- ATR / volatility tables,
- validation views,
- feature tables,
- and other reusable research outputs derived from normalized data.

### Rules
- the derived layer must be reproducible from the normalized layer
- no derived dataset should become an opaque black box
- all transformations should be documented
- derived datasets used in formal research should be versioned explicitly

## Query Engine Policy

The default local research query engine is:

- **DuckDB**

### Why DuckDB is selected

DuckDB works well with Parquet, is lightweight, and is appropriate for local research workflows over historical datasets.

It is a strong fit for:

- exploratory analysis,
- backtest dataset assembly,
- validation views,
- and reproducible research queries.

## Timestamp and Key Principles

## Canonical timestamp standard

All canonical timestamps must be stored in:

- **UTC**
- as **Unix milliseconds**

### Rule
Human-readable timestamps may be exposed in derived views or reports, but they must not replace canonical UTC millisecond timestamps in stored datasets.

## Bar identity rule

Bars are keyed canonically by:

- `symbol`
- `interval`
- `open_time`

### Rule
`open_time` is the canonical bar identifier.

`close_time` should be retained where available, but it is not the primary identity key.

## Completed-bar rule

Only completed bars may be used for strategy logic.

### Implications
This means:

- only completed 15m bars may generate signals
- only completed 1h bars may provide higher-timeframe bias
- partial-candle updates must not be treated as final historical truth

## Point-in-time rule

Only information that would have been known at the simulated decision time may be used in backtests and reusable research views.

This means:

- only completed bars are valid for signal generation
- only historically effective funding data may be applied
- and metadata assumptions must be explicit rather than silently borrowed from later states

## Higher-timeframe alignment rule

The 1h bar used at a 15m decision timestamp must be:

- the most recent fully completed 1h bar available at that time

This is necessary to prevent subtle time leakage.

## Minimum Schema and Key Principles

## Standard futures kline schema

Minimum required fields:

- `symbol`
- `interval`
- `open_time`
- `close_time`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `quote_asset_volume`
- `trade_count`
- `taker_buy_base_volume`
- `taker_buy_quote_volume`
- `source`

### Primary key
- `symbol`
- `interval`
- `open_time`

## Mark-price kline schema

Minimum required fields:

- `symbol`
- `interval`
- `open_time`
- `close_time`
- `open`
- `high`
- `low`
- `close`
- `source`

### Primary key
- `symbol`
- `interval`
- `open_time`

## Funding-rate schema

Minimum required fields:

- `symbol`
- `funding_time`
- `funding_rate`
- `mark_price`
- `source`

### Primary key
- `symbol`
- `funding_time`

## Metadata snapshot schema

Minimum required fields:

- `dataset_type`
- `snapshot_time`
- `symbol` where applicable
- `payload_version`
- `source`

### Primary key
- `dataset_type`
- `snapshot_time`
- optional `symbol`

## Data Quality Policy

## Missing bars

Missing bars must be:

- detected,
- logged,
- and explicitly handled.

### Forbidden behavior
Do **not**:
- silently forward-fill missing price bars,
- invent bars,
- or repair gaps without logging them.

### Allowed behavior
Missing intervals may be:

- excluded from valid backtest windows,
- or marked invalid for signal generation.

But they must always be explicit.

## Duplicate records

If duplicate records are detected for a key:

- log the conflict,
- inspect the source data,
- resolve deterministically,
- and document the rule used.

## Out-of-order records

Normalized datasets must be sorted deterministically by:

- symbol,
- interval where relevant,
- and open time or event time as appropriate.

Out-of-order raw fetches should be corrected during normalization, not ignored.

## Schema drift

If Binance changes endpoint fields or metadata structure:

- preserve raw payloads,
- version the normalization logic,
- and document the change.

Do not silently reinterpret old data under new schema assumptions.

## Gap and Invalidity Policy

The system must support explicit invalid windows.

Examples include:

- missing price bars,
- malformed candles,
- broken 1h aggregation logic,
- incomplete funding history relevant to held positions,
- unresolved metadata conflicts,
- or broken joins required for formal validation views.

These windows should be flagged so that:

- signals are not generated,
- trades are not simulated,
- and results are not polluted by silent bad data.

## Recommended Directory Layout

```text
research/data/
  raw/
    binance/
      usdm/
        klines/
        mark_price_klines/
        funding_rate/
        exchange_info/
        leverage_brackets/
        commission_rate/

  normalized/
    klines/
      symbol=BTCUSDT/
        interval=15m/
          year=YYYY/
            month=MM/
      symbol=ETHUSDT/
        interval=15m/
          year=YYYY/
            month=MM/

    mark_price_klines/
      symbol=BTCUSDT/
        interval=15m/
          year=YYYY/
            month=MM/
      symbol=ETHUSDT/
        interval=15m/
          year=YYYY/
            month=MM/

    funding_rate/
      symbol=BTCUSDT/
        year=YYYY/
          month=MM/
      symbol=ETHUSDT/
        year=YYYY/
          month=MM/

    metadata_snapshots/
      exchange_info/
      leverage_brackets/
      commission_rate/

  derived/
    bars_1h/
      standard/
      mark_price_optional/
    volatility/
    validation_views/
    features/

    ## Directory-layout notes

### 1. Normalized standard klines
For v1, normalized standard klines should store the canonical fetched 15m dataset.

### 2. Derived 1h bars
The preferred location for internally aggregated 1h bars is:

- `derived/bars_1h/`

### 3. Optional 1h mark-price views
If a 1h mark-price dataset is later required for specific analysis, it should be treated explicitly as either:

- a derived research dataset,
- or a clearly labeled optional fetched comparison dataset.

It should not be quietly mixed into the canonical strategy-price stack.

## Dataset Versioning Cross-Reference

Normalized and derived datasets used in formal research must follow the policy defined in:

- `docs/04-data/dataset-versioning.md`

### Core implication
Formal backtests and validation runs should reference only:

- explicitly versioned datasets,
- with stable identities,
- and with documented manifests and generation assumptions.

This document does not redefine the full versioning policy. It only defines the historical data contract that those versioned datasets must implement.

## What Is Explicitly In Scope for Phase 1

Phase 1 includes:

- BTCUSDT and ETHUSDT
- standard futures klines at 15m
- derived standard 1h bars
- mark-price klines at 15m
- funding history
- exchange-info snapshots
- leverage-bracket snapshots
- commission-rate snapshots
- normalized and derived Parquet datasets
- DuckDB access for research

## What Is Explicitly Out of Scope for Phase 1

Phase 1 does **not** require:

- order-book snapshots
- tick / trade-level research storage
- open-interest datasets
- liquidation feeds
- index-price datasets as core inputs
- on-chain data
- sentiment / news data
- cross-exchange data reconciliation
- portfolio-level merged research tables

These may be added later, but they should not complicate the initial historical contract.

## Decisions

The following decisions are accepted for the v1 historical data specification:

- official Binance USDⓈ-M endpoints are the canonical historical source
- standard futures klines at 15m are the canonical fetched strategy-price dataset
- BTCUSDT is the primary symbol
- ETHUSDT is the first secondary comparison symbol
- required 1h strategy context should be derived internally from canonical 15m standard futures data where practical
- mark-price klines are stored separately from standard futures klines
- phase-1 mark-price minimum is 15m data
- funding is stored as a separate event table
- exchange info, leverage brackets, and commission rates are stored as snapshots
- Parquet is the canonical historical research file format
- DuckDB is the default local research query engine
- canonical timestamps are UTC Unix milliseconds
- bars are keyed canonically by `open_time`
- missing bars must be logged, not silently repaired
- invalid research windows must be explicit

## Open Questions

The following remain open:

1. What exact historical start date should be used for phase 1 research?
2. How long should raw payload retention be maintained?
3. Should direct 1h standard futures klines also be stored permanently for audit, or only derived 1h datasets?
4. Should a 1h mark-price research view be added in phase 1 or deferred?
5. Should index-price datasets be added in a later phase?
6. Should open interest be added in phase 2?
7. What metadata fields should be elevated into normalized columns versus kept only as raw payload snapshots?
8. Should research datasets be partitioned only by year/month, or also by day for some tables?

## Next Steps

After this document, the next recommended files are:

1. `docs/00-meta/current-project-state.md`
2. `docs/08-architecture/implementation-blueprint.md`
3. `docs/08-architecture/state-model.md`

## References

Binance references:

- Binance USDⓈ-M Futures Kline/Candlestick Data  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data

- Binance USDⓈ-M Futures Mark Price Kline/Candlestick Data  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data

- Binance USDⓈ-M Futures Get Funding Rate History  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History

- Binance USDⓈ-M Futures Exchange Information  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information

- Binance USDⓈ-M Futures Notional and Leverage Brackets  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Notional-and-Leverage-Brackets

- Binance USDⓈ-M Futures User Commission Rate  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/User-Commission-Rate

DuckDB references:

- DuckDB Parquet Overview  
  https://duckdb.org/docs/current/data/parquet/overview.html

Related internal project documents:

- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`
- `docs/04-data/timestamp-policy.md`
- `docs/04-data/dataset-versioning.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`