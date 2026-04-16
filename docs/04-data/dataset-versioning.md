# Dataset Versioning

## Purpose

This document defines the dataset-versioning policy for the project’s historical research and backtesting environment.

Its purpose is to ensure that:

- historical datasets are reproducible,
- changes in data-processing logic are traceable,
- backtest and validation results can be tied to the exact data used,
- and dataset evolution does not silently invalidate research conclusions.

This document exists because the project uses a file-based analytical data stack, and file-based storage requires explicit versioning discipline if research is meant to remain trustworthy over time.

## Scope

This document governs versioning for:

- normalized datasets,
- derived datasets,
- metadata snapshots,
- reusable validation views,
- and the linkage between datasets and research outputs.

This document does **not** define raw source-fetch retention rules in full detail, nor does it define live-state database versioning.

## Background

The project’s research stack currently uses:

- official Binance USDⓈ-M futures endpoints as canonical source data,
- Parquet as the canonical historical research storage format,
- DuckDB as the default local research query engine,
- partitioned file layouts by symbol, interval, and time,
- and derived research tables for backtesting and validation.

This design is efficient and appropriate for analytical workloads, but it introduces a governance requirement:

> if the data-processing logic changes, the project must be able to identify exactly which dataset version each research result was built from.

Without this, the project risks:

- comparing results produced from inconsistent data,
- silently changing research assumptions midstream,
- and losing the ability to reproduce earlier findings.

## Versioning Philosophy

## Core principle

A dataset version is not just a collection of files.

A dataset version is a **defined research artifact** with:

- a stable identity,
- explicit source assumptions,
- a known schema,
- a known transformation history,
- and a clear link to the code or logic that produced it.

## Why versioning is required

Versioning is required because any of the following can change research outcomes materially:

- source endpoints,
- normalization logic,
- timestamp handling,
- bar-construction rules,
- schema definitions,
- funding joins,
- feature derivation,
- gap handling,
- or symbol/interval assumptions.

If those changes are not versioned explicitly, the project cannot reliably distinguish:

- a real strategy improvement,
- from a dataset change,
- from a normalization bug,
- from a silent schema drift.

## Versioning Scope

## Datasets that must be versioned

The following dataset categories require explicit versioning:

### Normalized datasets
Examples:
- standard futures klines
- mark-price klines
- funding-rate event tables
- metadata snapshot tables

### Derived datasets
Examples:
- internally derived 1h bars
- ATR / volatility tables
- breakout feature tables
- validation-ready joined tables

### Reusable validation views
Examples:
- train/validation/holdout views
- walk-forward fold inputs
- cost-sensitivity experiment inputs

## Datasets that do not require semantic versioning in the same way

### Raw payload storage
Raw payloads should remain source-faithful and traceable, but they do not need the same semantic dataset versioning model as processed research datasets.

Raw data should instead be governed by:

- source endpoint identity,
- fetch timestamp,
- request parameters,
- and storage integrity.

## When a New Dataset Version Is Required

A new dataset version must be created whenever any change affects the meaning, structure, or reproducibility of the dataset.

## Mandatory version bump conditions

A new version is required if any of the following change:

- source endpoint set
- symbol universe
- interval set
- schema
- normalization logic
- timestamp interpretation
- bar-construction or aggregation logic
- gap-handling rules
- missing-data policy
- funding join logic
- feature-engineering logic
- metadata-extraction logic
- partition logic if it affects reproducibility or discovery
- canonical source assumptions
- derived-table construction rules

## Practical rule

If a change could cause two backtests to produce different results from “the same” dataset name, then the dataset must receive a new version.

## Version Identifier Policy

## Required version identity

Every normalized or derived dataset must have an explicit version identifier.

## Recommended naming pattern

Recommended format:

- `<dataset_name>__vNNN`

Examples:
- `usdm_klines_btcusdt_15m__v001`
- `usdm_funding_rate__v002`
- `breakout_features_btcusdt_15m__v003`
- `validation_view_walkforward_a__v001`

## Why this pattern is selected

This pattern is:

- human-readable,
- machine-friendly,
- easy to sort,
- easy to reference in logs and reports,
- and stable enough for long-term use.

## Version numbering rule

Version numbers should increase monotonically for each dataset family.

Examples:
- `__v001`
- `__v002`
- `__v003`

The project should not reuse or overwrite a previously published version identifier.

## Dataset Manifest Policy

## Core rule

Every versioned dataset must have a manifest file.

## Recommended manifest names

Preferred options:

- `manifest.json`
- or `dataset_metadata.json`

Choose one project-wide standard and use it consistently.

## Manifest location

The manifest should live at the dataset-version root and describe that specific version.

## Minimum required manifest fields

Every manifest should include at least:

- dataset name
- dataset version ID
- dataset category
- creation timestamp
- canonical timezone
- canonical timestamp format
- symbol set
- interval set where relevant
- source endpoint(s)
- schema version
- transformation or pipeline version
- partitioning rules
- primary key definition
- author / generator identity if available
- notes / comments
- predecessor version if applicable

## Why the manifest is required

Parquet files and partition folders are excellent for storage and analytics, but they do not fully describe the semantic identity of the dataset.

The manifest provides the missing research contract.

## Schema Versioning Policy

## Schema version requirement

Every versioned dataset must track a schema version.

This schema version may be the same as the dataset version in simple cases, but the semantic distinction should still be preserved conceptually:

- dataset version = the research artifact version
- schema version = the structure definition version

## Additive vs breaking schema changes

The project must distinguish between:

### Additive schema changes
Examples:
- adding a new optional column
- adding new metadata fields
- adding non-breaking derived diagnostics

### Breaking schema changes
Examples:
- renaming core columns
- changing timestamp meaning
- changing canonical keys
- changing price or volume semantics
- changing data types in a way that affects logic
- changing how derived fields should be interpreted

## Required rule

Breaking schema changes must always produce a clearly new dataset version.

Additive changes should still produce a new dataset version if the resulting dataset is intended to be reused in research, even if backward compatibility is technically possible.

## Immutability Policy

## Core rule

Published dataset versions are immutable.

## Meaning of immutable

Once a dataset version is declared published or used for research:

- its files must not be silently modified,
- its schema must not be silently changed,
- its manifest must not be silently rewritten in a way that changes meaning.

## Correction policy

If a correction is needed:

- create a new version
- document what changed
- record the predecessor version

## Why immutability is required

Immutability protects reproducibility.

If an old version can change after research has already used it, then backtest and validation results lose their audit trail.

## Experiment Linkage Policy

## Core rule

Every backtest, validation run, or research report must record the dataset version(s) it used.

## Minimum required linkage fields

At minimum, each experiment or report should record:

- dataset name
- dataset version ID
- schema version
- feature dataset version if applicable
- validation-view version if applicable
- generation timestamp of the experiment

## Why this rule matters

This makes it possible to answer:

- which data produced this result,
- whether two experiments used the same or different datasets,
- and whether a change in results came from strategy changes or dataset changes.

## Partitioning vs Version Identity

## Core rule

Partition folders do not replace formal versioning.

### Example
A directory layout like:

- `symbol=BTCUSDT/interval=15m/year=2024/month=01`

is useful for storage organization, but it is **not** a complete dataset identity.

## Why this matters

Two datasets may share the same partition structure while differing in:

- normalization rules,
- schema,
- missing-data handling,
- or feature logic.

Therefore, partition structure is a storage concern, while dataset version identity is a governance concern.

## Dataset Family Examples

## Example 1 — Normalized BTCUSDT 15m klines

Possible dataset version:
- `usdm_klines_btcusdt_15m__v001`

Manifest may state:
- source endpoint: `GET /fapi/v1/klines`
- symbol: `BTCUSDT`
- interval: `15m`
- canonical key: `symbol, interval, open_time`
- canonical timezone: `UTC`
- canonical timestamp format: `Unix milliseconds`

## Example 2 — Funding-rate dataset

Possible dataset version:
- `usdm_funding_rate__v002`

Manifest may state:
- source endpoint: `GET /fapi/v1/fundingRate`
- symbols: `BTCUSDT, ETHUSDT`
- key: `symbol, funding_time`
- join policy: event-based funding timestamps

## Example 3 — Breakout feature table

Possible dataset version:
- `breakout_features_btcusdt_15m__v003`

Manifest may state:
- predecessor dataset versions used
- ATR calculation definition
- EMA configuration
- setup-window rules included
- transformation code version

## Publication States

The project may treat dataset versions as moving through simple publication states.

Recommended states:

- `draft`
- `published`
- `deprecated`
- `superseded`

## Meaning of each

### Draft
Still under development and not approved for stable research use.

### Published
Approved for use in research, backtesting, or validation.

### Deprecated
Still readable for historical reference, but not recommended for new work.

### Superseded
Replaced by a newer version, but retained for reproducibility.

## Recommended rule

Only `published` dataset versions should be used in formal backtests and validation reports.

## Change Documentation Policy

Whenever a new dataset version is created, the project should record:

- what changed,
- why it changed,
- and whether the change is expected to affect research results materially.

This can be done in:

- the dataset manifest,
- a changelog section,
- or a dataset-family registry file.

## Minimal Changelog Fields

Recommended minimum fields:

- previous version
- new version
- change date
- change summary
- reason for change
- expected research impact
- breaking or non-breaking classification

## Operational Rules

## Rule 1
Never overwrite a published dataset version in place.

## Rule 2
Never run formal validation on an untracked dataset version.

## Rule 3
Never compare backtest outcomes without recording which dataset version each used.

## Rule 4
Never assume that matching partition folders imply matching dataset semantics.

## Rule 5
Prefer creating a new version over silently “fixing” a reused one.

## What Is Explicitly In Scope

This versioning policy applies to:

- normalized market datasets
- normalized mark-price datasets
- funding datasets
- metadata snapshots
- derived 1h bars
- derived features
- reusable validation views
- backtest dataset references

## What Is Explicitly Out of Scope for Now

This policy does **not** yet define:

- a full data catalog service
- transaction-log lakehouse behavior
- object-store versioning systems
- live operational database migration/version policy
- enterprise-scale metadata registry tools

Those may become relevant later, but they are unnecessary for the current phase.

## Decisions

The following decisions are accepted for the dataset versioning policy:

- normalized and derived datasets must have explicit version IDs
- raw payload storage remains source-faithful and separately traceable
- new versions are required for meaningful schema or transformation changes
- published dataset versions are immutable
- every versioned dataset must have a manifest
- every backtest and validation run must record the dataset version used
- additive and breaking schema changes must be distinguished
- partition folders do not replace formal dataset versioning
- published dataset versions are the only acceptable source for formal validation work

## Open Questions

The following remain open:

1. Should the project maintain a central dataset registry file in addition to per-dataset manifests?
2. What exact publication workflow should move a dataset from `draft` to `published`?
3. Should feature datasets track predecessor source dataset versions explicitly in every manifest?
4. Should changelogs live inside each dataset manifest or in a separate dataset-family changelog file?
5. What naming convention should be standardized for author / generator identity fields?
6. Should deprecated versions remain in the default query path or require explicit inclusion?

## Next Steps

After this document, the next recommended files are:

1. `docs/09-operations/restart-procedure.md`
2. `docs/10-security/api-key-policy.md`
3. `docs/09-operations/incident-response.md`

## References

DuckDB references:

- DuckDB Partitioned Writes  
  https://duckdb.org/docs/current/data/partitioning/partitioned_writes.html

- DuckDB Combining Schemas  
  https://duckdb.org/docs/current/data/multiple_files/combining_schemas.html

Related internal project documents:

- `docs/04-data/historical-data-spec.md`
- `docs/04-data/timestamp-policy.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`