is this the full document?

# Historical Data Specification

## Purpose

This document defines the historical data contract for the v1 research and backtesting environment.

The goal of this specification is to make all historical research reproducible, auditable, and consistent across:

- strategy design,
- backtesting,
- validation,
- and later implementation.

This document is intended to prevent hidden inconsistencies in data sourcing, timestamp handling, bar construction, and metadata usage.

## Scope

This document defines:

- the canonical historical data sources,
- the required datasets for v1 research,
- the storage layers,
- the schema and key principles,
- the timestamp policy,
- the gap and quality policy,
- and the recommended directory layout.

This document does **not** define live ingestion behavior, execution-state storage, or full feature-engineering rules.

## Background

The project is currently targeting:

- Binance USDⓈ-M futures,
- BTCUSDT as the primary symbol,
- ETHUSDT as the first secondary comparison symbol,
- 15m signal logic,
- 1h higher-timeframe bias,
- and a rules-based breakout system.

Because the strategy relies on strict bar-close logic, the historical dataset must be:

- point-in-time correct,
- internally consistent,
- and reproducible from a known canonical source.

Historical backtests become unreliable very quickly when:

- multiple vendors are mixed without careful reconciliation,
- time alignment is inconsistent,
- missing bars are silently repaired,
- or rule metadata is assumed rather than snapshotted.

## Canonical Source Policy

### Primary source

For v1 research, the canonical historical source is:

- **official Binance USDⓈ-M futures endpoints only**

This means the project will use Binance-provided historical and rule data as the base truth for the first research environment.

### Why this policy is selected

The purpose of this policy is to reduce unnecessary inconsistency.

Using a single canonical venue source helps avoid:

- mismatched timestamp conventions,
- inconsistent candle construction,
- different vendor adjustment rules,
- and silent differences in mark-price or funding data.

### Included official source categories

The historical research stack should use official Binance USDⓈ-M endpoints for:

- standard futures klines,
- mark-price klines,
- funding-rate history,
- exchange information,
- leverage brackets,
- and commission rates.

## Required Datasets

## 1. Standard futures kline dataset

This is the primary market-price dataset.

### Required symbols
- BTCUSDT
- ETHUSDT

### Required intervals
- 15m
- 1h

### Intended use
This dataset is used for:

- setup detection,
- breakout detection,
- ATR calculations,
- trend-bias calculations,
- signal timing,
- and next-bar-open backtest fills.

### Canonical priority
This is the main price dataset for strategy logic.

## 2. Mark-price kline dataset

This is a separate reference-price dataset.

### Required symbols
- BTCUSDT
- ETHUSDT

### Required intervals
- 15m
- 1h

### Intended use
This dataset is used for:

- stop-behavior sensitivity analysis,
- later comparison between trade-price-driven and mark-price-driven protective logic,
- and research into protective-stop realism.

### Important rule
Mark-price klines must be stored separately from standard futures klines.

They are **not** a replacement for the main signal dataset.

## 3. Funding-rate dataset

This is an event-based dataset, not a bar dataset.

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

It should **not** be flattened into candle rows during ingestion.

## 4. Exchange rule metadata

This is snapshot metadata.

### Required data
- symbol information
- price precision
- quantity precision
- min/max quantity rules
- notional and filter rules
- order-type availability where relevant

### Intended use
This dataset is used for:

- validating research assumptions,
- checking whether simulated sizes would be tradable,
- and aligning future execution logic with exchange constraints.

### Important rule
This data should be saved as time-stamped snapshots.

## 5. Leverage bracket metadata

This is snapshot metadata.

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

## 6. Commission-rate metadata

This is account-related snapshot metadata.

### Required data
- symbol-specific commission rates where applicable

### Intended use
This dataset is used for:

- realistic fee assumptions in backtests,
- and later account-specific cost calibration.

### Important rule
Commission assumptions must be explicit and saved as snapshots rather than silently assumed.

## Canonical Dataset Policy

## Primary market-price dataset

The canonical market-price dataset for v1 strategy research is:

- **standard futures klines**
- for **BTCUSDT** and **ETHUSDT**
- at **15m**
- with **1h derived or matched consistently**

This dataset is the source of truth for:

- signal generation,
- setup construction,
- and baseline execution simulation.

## Higher-timeframe policy

The preferred policy is:

- derive **1h bars internally from the canonical 15m dataset**

### Why this policy is selected

This keeps the research stack internally consistent.

Benefits:
- one canonical bar source,
- fewer silent mismatches,
- easier reproducibility,
- easier auditability.

### Alternative
Direct 1h klines may still be fetched for comparison or sanity-checking, but the preferred research rule is to keep higher-timeframe context derived from the same canonical source used by the signal timeframe.

## Storage Architecture

The historical data stack should use a three-layer storage model.

## 1. Raw layer

The raw layer stores:

- original API payloads,
- fetch timestamps,
- endpoint metadata,
- and any request context needed for later auditing.

### Rules
- raw payloads should be treated as immutable
- no silent cleaning in the raw layer
- preserve source fidelity as much as possible

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
- analysis-ready tables.

### Format
The canonical normalized format should be:

- **Parquet**

### Why Parquet is selected

Parquet is efficient for analytical workloads, compresses well, and is suitable for column-oriented research queries.

## 3. Derived layer

The derived layer stores:

- internally aggregated 1h bars,
- ATR columns,
- normalized volatility measures,
- validation views,
- and later feature tables if needed.

### Rules
- the derived layer must be reproducible from the normalized layer
- no derived dataset should become an opaque black box
- all transformations should be documented

## Query Engine Policy

The default local research query engine should be:

- **DuckDB**

### Why DuckDB is selected

DuckDB works well with Parquet, is lightweight, and is appropriate for local research workflows over historical datasets.

This makes it a strong fit for:

- exploratory analysis,
- backtest dataset assembly,
- and reproducible research views.

## Timestamp Policy

## Canonical timestamp standard

All canonical timestamps must be stored in:

- **UTC**
- as **Unix milliseconds**

### Human-readable representation
Readable ISO-8601 timestamps may be exposed in derived views or reports, but they must not replace canonical UTC millisecond timestamps in storage.

## Bar timestamp rule

Bars are keyed by:

- **open time**

This should be treated as the canonical bar identifier.

## Point-in-time rule

Only information that would have been known at the simulated decision time may be used in backtests and research views.

That means:

- only completed bars are valid for signal generation,
- only historically effective funding data may be applied,
- and rule metadata must reflect the intended research assumptions explicitly.

## Schema and Key Principles

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
- excluded from the valid backtest window,
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
- interval,
- open time.

Any out-of-order raw fetches should be corrected during normalization, not ignored.

## Schema drift

If Binance changes endpoint fields or metadata structure:

- preserve raw payloads,
- version the normalization logic,
- and document the schema change.

Do not silently reinterpret old data with new schema assumptions.

## Gap and Invalidity Policy

The system must support explicit invalid windows.

Examples of invalid research windows:
- missing price bars,
- malformed candles,
- incomplete funding history for a tested holding window,
- broken aggregation logic,
- or unresolved metadata conflicts.

These windows should be flagged so that:

- signals are not generated,
- trades are not simulated,
- and results are not polluted by silent bad data.

## Directory Layout

Recommended structure:

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
        interval=1h/
          year=YYYY/
            month=MM/
      symbol=ETHUSDT/
        interval=15m/
          year=YYYY/
            month=MM/
        interval=1h/
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
    volatility/
    validation_views/
    features/

    ## Dataset Versioning Principles

Every normalized and derived dataset should support version tracking.

Minimum versioning fields or metadata should include:

- dataset name
- version identifier
- generation timestamp
- source endpoint(s)
- normalization code version
- notes about schema assumptions

The purpose is to make it possible to answer:

- where did this dataset come from,
- how was it produced,
- and which logic version created it.

## What Is Explicitly In Scope for Phase 1

Phase 1 includes:

- BTCUSDT and ETHUSDT
- standard futures klines
- mark-price klines
- funding history
- exchange info snapshots
- leverage bracket snapshots
- commission-rate snapshots
- normalized and derived Parquet datasets
- DuckDB access for research

## What Is Explicitly Out of Scope for Phase 1

Phase 1 does **not** require:

- order-book snapshots
- tick/trade-level research storage
- open-interest datasets
- liquidation feeds
- on-chain data
- sentiment/news data
- cross-exchange data reconciliation
- portfolio-level merged research tables

These may be added later, but they should not complicate the first historical contract.

## Decisions

The following decisions are accepted for the v1 historical data specification:

- official Binance USDⓈ-M endpoints are the canonical historical source
- standard futures klines are the canonical signal dataset
- BTCUSDT is the primary symbol
- ETHUSDT is the first secondary comparison symbol
- 1h context should be derived internally from canonical market-bar data where practical
- mark-price klines are stored separately from standard klines
- funding is stored as a separate event table
- exchange info, leverage brackets, and commission rates are stored as snapshots
- Parquet is the canonical historical research file format
- DuckDB is the default local research query engine
- canonical timestamps are UTC Unix milliseconds
- missing bars must be logged, not silently repaired

## Open Questions

The following remain open:

1. What exact historical start date should be used for phase 1 research?
2. How long should raw payload retention be maintained?
3. Should direct 1h klines also be stored permanently, or only derived 1h datasets?
4. Should index-price klines be added in a later phase?
5. Should open interest be added in phase 2?
6. What metadata fields should be elevated into normalized columns versus kept only as raw payload snapshots?
7. Should research datasets be partitioned only by year/month, or also by day for some tables?
8. Should mark-price 1h datasets be stored immediately or derived later from 15m mark-price data?

## Next Steps

After this document, the next recommended file is:

- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`

After that, the next data-related documents should likely be:

- `docs/04-data/timestamp-policy.md`
- `docs/04-data/dataset-versioning.md`
- `docs/04-data/live-data-spec.md`

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