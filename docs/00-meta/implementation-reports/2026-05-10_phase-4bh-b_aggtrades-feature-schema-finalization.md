# Phase 4bh-B — AggTrades Feature Schema Finalization Memo

**Phase identity:** Phase 4bh-B — AggTrades Feature Schema Finalization Memo.
**Phase type:** docs-only feature schema finalization memo.
**Date:** 2026-05-10.
**Branch:** `phase-4bh-b/aggtrades-feature-schema-finalization`.
**Base:** `main` at the post-Phase-4bh-A merge-closeout state (`714a2730d2a03ffb9ef16daba7eea28fc359611c`); Phase 4bh-A merge commit `c85b0ec9efd8a00b05eb4f39fe156eb31fe07875` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

This memo finalizes the exact feature schema, windows, timestamp cadence, output row model, dtypes, null / NaN policies, decimal / float policies, invalid-window propagation policies, causal windowing rules, lineage and metadata columns, feature manifest schema, feature config schema, future module / test plan, and acceptance criteria for any future Phase 4bh implementation that ever computes features from `microstructure_normalized_aggtrades_v001`.

The memo is **docs-only**. It computes nothing, writes nothing under `data/microstructure/`, modifies no source code, tests, or scripts, acquires no data, mutates no manifest, and authorizes no successor phase. Phase 4bh-A's Feature Stage-0 design is converted into a precise implementation contract; the Feature Stage-1 / Stage-2 transitions remain a separately authorized future Phase 4bh.

The Phase 4ak twelve-clause M0 mechanism-admissibility gate, the post-null cooldown rule, the cooled-down families list, the Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, every retained verdict, and every project lock are preserved verbatim by this phase.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bh-A merge commit (ancestor of `main`) | `c85b0ec9efd8a00b05eb4f39fe156eb31fe07875` |
| `main == origin/main` (start of Phase 4bh-B) | `714a2730d2a03ffb9ef16daba7eea28fc359611c` |
| Raw family | `microstructure_raw_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending`, immutable |
| Original derived manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`, SHA256 `f6f0d947…`, `research_eligible=false`, `eligibility_gate_status=pending`, immutable in this phase |
| Normalized Parquet | `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet`, SHA256 `2b3d6978…`, immutable in this phase |
| Phase 4bg-B successor-state JSON | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`, SHA256 `8bcc7d01…`, immutable in this phase |
| Phase 4bf gate report | SHA256 `dd4e0c1c…`, immutable in this phase |
| Phase 4bb-D gate report | SHA256 `96f09159…`, immutable in this phase |
| `data/microstructure/features/` | does not exist |
| `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` | does not exist |

---

## 3. Inputs reviewed

- Phase 4az / Phase 4ba / Phase 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E (raw acquisition, eligibility ladder, raw gate sequence, successor-state policy).
- Phase 4bc / 4bd-A / 4bd / 4be (normalization design, plan, implementation, structural QA).
- Phase 4bf-A / 4bf (derived-family eligibility-gate design, implementation and execution).
- Phase 4bg-A / 4bg-B (Stage-3 admissibility decision, successor-state recording).
- **Phase 4bh-A** (feature-boundary design memo; this memo finalizes it).
- Phase 4ak M0 governance adoption.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Project locks (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w).
- Retained verdict ledger (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1).

No prior memo's text was modified. No artefact under `data/microstructure/` was modified.

---

## 4. Scope

In scope for this memo:

- finalizing the feature family name, output namespace, output file path, sidecar path, and feature manifest path (none created);
- finalizing the output row model (event-aligned), the timestamp cadence, the windows, and the exact feature column list;
- finalizing required lineage / identity / metadata columns;
- finalizing the full output schema (columns × roles × dtypes × computation rules × leakage rules × null policies);
- finalizing the dtype, null / NaN, decimal / float, invalid-window, and causal windowing policies;
- finalizing the forbidden columns / forbidden transforms;
- finalizing the feature manifest schema and the feature config schema;
- proposing the future Phase 4bh module / test layout (none created);
- specifying acceptance criteria and fail-closed rules for any future Phase 4bh implementation.

---

## 5. Non-scope

This memo does **not**:

- compute features;
- create feature files, datasets, manifests, sidecars, or feature-config files;
- create JSONL, Parquet, DuckDB, label, signal, proxy, ML, or strategy artefacts;
- modify source code, tests, scripts, configurations, README, `pyproject.toml`, `.gitignore`, or governance memo;
- run the normalizer, the raw eligibility gate, or the derived-family eligibility gate;
- generate a new gate report;
- create a replacement derived manifest, replacement raw manifest, or any sibling manifest;
- modify the Phase 4bg-B successor-state artefact or create a new successor-state artefact;
- mutate any `research_eligible` field or any `eligibility_gate_status` field;
- acquire data; call public endpoints; call Binance APIs; open WebSockets; use private endpoints; use credentials; read or create `.env`; create `.mcp.json`; or enable MCP / Graphify;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- create labels, targets, or strategy signals;
- train ML, create strategy logic, or run backtests;
- authorize feature computation, Phase 4bh implementation, Stage-4 feature-cleared status, ML, strategy, or backtests;
- revise retained verdicts, change project locks, or amend M0;
- authorize Phase 4bh-C, Phase 4bh, Phase 4bi-A, Phase 4bi-B, Phase 4bi-C, Phase 4bi-D, Phase 4bj, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bh-A dependency

Phase 4bh-A merged into `main` at commit `c85b0ec…` and reached **Feature Stage-0** (feature schema designed). It defined: the canonical input (`microstructure_normalized_aggtrades_v001`), forbidden inputs, the feature-stage model, the proposed feature-family naming, the temporal-leakage / windowing / aggregation / precision / type / missing-window policies, the proposed candidate windows (1 s, 5 s, 15 s, 30 s, 60 s, 5 min), the proposed allowed feature categories (count/intensity, volume, taker-side flow, past/current price-path, time-of-day, data-quality), the proposed forbidden classes, the proposed validation gate sequence (Phase 4bi-A → 4bi-B → 4bi-C → 4bi-D), and 20 acceptance criteria + 12 fail-closed rules.

Phase 4bh-B converts that broad Phase 4bh-A boundary into an exact, implementable schema. It narrows the candidate windows from six to four, names every feature column explicitly, defines the full output schema table, defines the manifest and feature-config schemas, and defines the future implementation module / test layout.

The Phase 4bh-A boundaries (canonical input, Stage-3 marker via Phase 4bg-B successor-state JSON only, forbidden inputs, forbidden feature classes, leakage rule, M0 / cooled-down / no-rescue boundaries) all remain binding on Phase 4bh-B and on any future Phase 4bh implementation.

---

## 7. Feature schema finalization objective

- finalize the feature family name as `microstructure_features_aggtrades_v001`;
- finalize the canonical input as `microstructure_normalized_aggtrades_v001` with Stage-3 admissibility cited only via the Phase 4bg-B successor-state JSON SHA `8bcc7d01…`;
- finalize the future output namespace and file paths (none created);
- finalize the output row model (event-aligned);
- finalize the timestamp cadence (`feature_timestamp_ms = source transact_time_ms`);
- finalize the four-window subset {1 s, 5 s, 15 s, 60 s};
- finalize the 45 feature columns (40 windowed × 4 windows + 3 time-context + 2 data-quality);
- finalize the 16 lineage / identity / metadata columns;
- finalize the dtype, null / NaN, decimal / float, invalid-window, and causal windowing policies;
- finalize the manifest and feature-config schemas;
- record acceptance criteria and fail-closed rules for any future Phase 4bh implementation;
- preserve every retained verdict and project lock.

---

## 8. Canonical input confirmation

The only allowed input for any future Phase 4bh implementation is the normalized derived family:

```text
microstructure_normalized_aggtrades_v001
```

with the Phase 4bc 19-column trade-record-level canonical schema. Stage-3 admissibility is cited **only** via the Phase 4bg-B successor-state artefact at:

```text
data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json
```

with SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`. The original derived manifest alone (with `research_eligible=false / eligibility_gate_status=pending`) **must not** be interpreted as `research_eligible=true`. Any future Phase 4bh implementation must read both the derived manifest (for source dataset metadata and lineage SHAs) and the successor-state JSON (for the Stage-3 marker), and must include both SHAs in the future feature manifest.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end. No future Phase 4bh implementation may invoke that helper on the original manifests.

---

## 9. Feature-family name confirmation

Finalized future feature family name (NOT created by this memo):

```text
microstructure_features_aggtrades_v001
```

This is a **sibling derived family**, not a mutation of `microstructure_normalized_aggtrades_v001`.

Finalized future output namespace (NOT created):

```text
data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/
```

Finalized future feature file (NOT created):

```text
data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet
```

Finalized future feature sidecar (NOT created):

```text
data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet.sha256
```

Finalized future feature manifest (NOT created):

```text
data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json
```

All paths are gitignored under the existing `.gitignore:85: data/microstructure/` rule (no `.gitignore` change required).

---

## 10. Output row model

**Event-aligned, one feature row per normalized aggTrade row.**

For each row in the source normalized Parquet (`microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet`; row count `1,681,098`), the future feature dataset emits **exactly one** feature row preserving:

- `row_index`,
- `agg_trade_id`,
- `transact_time_ms` (mirrored as `source_transact_time_ms`),
- `symbol`,
- `utc_date`.

Each feature row at time `T` uses **only** rows with `transact_time_ms <= T` (and same-timestamp rows with `row_index <= R`; see §16 / §22).

**Justification for event-aligned:**

- avoids synthetic timestamps (no resampling);
- preserves bit-perfect one-to-one lineage with normalized rows (every feature row maps to exactly one source `agg_trade_id` and `row_index`);
- avoids edge cases at empty resampled windows (no fabricated rows);
- avoids ambiguity about how to summarize features across multiple events that share a resampled bucket.

Bar-aligned / resampled output is **not** chosen. If a future phase ever proposes a resampled output, that proposal must justify in writing why event-aligned cannot suffice and must satisfy a separate Phase 4bh-C-style review.

Expected row count for the future feature dataset: **`1,681,098`** rows for BTCUSDT 2025-01-15 (matches the Phase 4bd / Phase 4be / Phase 4bf-passed normalized row count).

---

## 11. Timestamp cadence

Finalized:

- `feature_timestamp_ms` = source `transact_time_ms` for each aggTrade row;
- `source_transact_time_ms` = same value (kept for explicit lineage);
- no fixed resampling cadence in Phase 4bh;
- no synthetic timestamps;
- no forward-filled feature rows;
- no generated empty-window rows;
- the half-open UTC day boundary `[2025-01-15T00:00:00.000Z, 2025-01-16T00:00:00.000Z)` from Phase 4bb-A / Phase 4be is honored by definition because the feature timestamps are exactly the source `transact_time_ms` values.

`feature_timestamp_ms` is `int64` UTC milliseconds.

---

## 12. Finalized feature windows

Finalized initial window subset (chosen from the Phase 4bh-A candidates):

| Window | Window length (ms) | Status |
| ------ | ------------------ | ------ |
| 1s | 1,000 | finalized |
| 5s | 5,000 | finalized |
| 15s | 15,000 | finalized |
| 60s | 60,000 | finalized |

Explicitly **deferred** (not authorized by Phase 4bh-B; require a future separately authorized memo):

- 30 seconds;
- 5 minutes.

**Rationale:** the first implementation should be smaller, easier to validate, and less likely to create computational or leakage ambiguity. {1s, 5s, 15s, 60s} spans roughly two orders of magnitude (~60×) which is sufficient to surface leakage, performance, and edge-case issues without inflating the feature column count.

The finalized `window_list` for the future feature manifest is `["1s", "5s", "15s", "60s"]` with corresponding `window_ms` values `[1000, 5000, 15000, 60000]`.

---

## 13. Finalized feature column list

For each window in `{1s, 5s, 15s, 60s}`, the future feature dataset must include the following 10 windowed feature columns (40 total windowed columns):

| Class | Column (with `<window>` substituted) |
| ----- | ------------------------------------ |
| count / intensity | `rolling_aggtrade_count_<window>` |
| volume | `rolling_quantity_sum_<window>` |
| volume | `rolling_quantity_mean_<window>` |
| taker-side flow | `rolling_aggressive_buy_quantity_<window>` |
| taker-side flow | `rolling_aggressive_sell_quantity_<window>` |
| taker-side flow | `rolling_aggressive_buy_count_<window>` |
| taker-side flow | `rolling_aggressive_sell_count_<window>` |
| taker-side flow | `rolling_aggressive_flow_ratio_<window>` |
| taker-side flow | `rolling_aggressive_quantity_imbalance_<window>` |
| past-only price | `rolling_log_return_past_window_<window>` |

Plus 3 time-context features (one row each, not windowed):

- `utc_hour`
- `utc_minute`
- `milliseconds_since_day_start`

Plus 2 data-quality features:

- `invalid_window_flag`
- `rolling_missing_window_flag`

**Total feature columns: 45** (`40 + 3 + 2`).

---

## 14. Required lineage and identity columns

The future feature dataset must include the following **16 non-feature** columns (identity + lineage + metadata). These are **not** features:

| # | Column | Role | Notes |
| - | ------ | ---- | ----- |
| 1 | `dataset_family` | identity | constant `"microstructure_features_aggtrades_v001"` |
| 2 | `dataset_version` | identity | constant `"v001"` |
| 3 | `source_dataset_family` | lineage | constant `"microstructure_normalized_aggtrades_v001"` |
| 4 | `source_dataset_version` | lineage | constant `"v001"` |
| 5 | `source_feature_schema_version` | lineage | constant `"v001"` |
| 6 | `symbol` | identity | constant per partition (e.g., `"BTCUSDT"`) |
| 7 | `utc_date` | identity | constant per partition (e.g., `"2025-01-15"`) |
| 8 | `agg_trade_id` | identity | from source normalized row |
| 9 | `row_index` | identity | from source normalized row |
| 10 | `feature_timestamp_ms` | identity | == `source_transact_time_ms` |
| 11 | `source_transact_time_ms` | lineage | from source normalized row |
| 12 | `source_normalized_parquet_sha256` | lineage | constant per partition (e.g., `"2b3d6978…"`) |
| 13 | `source_normalized_manifest_sha256` | lineage | constant per partition (e.g., `"f6f0d947…"`) |
| 14 | `source_successor_state_sha256` | lineage | constant per partition (e.g., `"8bcc7d01…"`) |
| 15 | `source_phase_4bf_gate_report_sha256` | lineage | constant per partition (e.g., `"dd4e0c1c…"`) |
| 16 | `feature_config_hash` | metadata | constant per run; deterministic hash of canonicalized feature config |

Total schema column count: **16 lineage/identity/metadata + 45 feature = 61 columns**.

---

## 15. Full output schema table

| # | Column | Role | Dtype | Nullable | Computation rule | Leakage rule | Null policy |
| - | ------ | ---- | ----- | -------- | ---------------- | ------------ | ----------- |
| 1 | `dataset_family` | identity | string | no | constant | n/a | n/a |
| 2 | `dataset_version` | identity | string | no | constant | n/a | n/a |
| 3 | `source_dataset_family` | lineage | string | no | constant | n/a | n/a |
| 4 | `source_dataset_version` | lineage | string | no | constant | n/a | n/a |
| 5 | `source_feature_schema_version` | lineage | string | no | constant | n/a | n/a |
| 6 | `symbol` | identity | string | no | constant per partition | n/a | n/a |
| 7 | `utc_date` | identity | string | no | constant per partition | n/a | n/a |
| 8 | `agg_trade_id` | identity | int64 | no | source row | n/a | n/a |
| 9 | `row_index` | identity | int64 | no | source row | n/a | n/a |
| 10 | `feature_timestamp_ms` | identity | int64 | no | == source `transact_time_ms` | n/a | n/a |
| 11 | `source_transact_time_ms` | lineage | int64 | no | source row | n/a | n/a |
| 12 | `source_normalized_parquet_sha256` | lineage | string | no | constant per partition | n/a | n/a |
| 13 | `source_normalized_manifest_sha256` | lineage | string | no | constant per partition | n/a | n/a |
| 14 | `source_successor_state_sha256` | lineage | string | no | constant per partition | n/a | n/a |
| 15 | `source_phase_4bf_gate_report_sha256` | lineage | string | no | constant per partition | n/a | n/a |
| 16 | `feature_config_hash` | metadata | string | no | constant per run; canonical-JSON SHA256 of feature config | n/a | n/a |
| 17 | `rolling_aggtrade_count_1s` | feature | int64 | no | count of source rows with `T - 1000 < transact_time_ms <= T` AND same-timestamp tie-break `row_index <= R` | causal trailing | `0` if empty window |
| 18 | `rolling_quantity_sum_1s` | feature | string (Decimal-as-string) | no | sum of `Decimal(quantity)` over trailing window | causal trailing | `"0"` if empty window |
| 19 | `rolling_quantity_mean_1s` | feature | string (Decimal-as-string) | yes | `Decimal(quantity_sum) / Decimal(count)` over trailing window | causal trailing | null if empty window |
| 20 | `rolling_aggressive_buy_quantity_1s` | feature | string (Decimal-as-string) | no | sum of `Decimal(quantity)` over trailing window where `is_buyer_maker=false` | causal trailing | `"0"` if no aggressive-buy events |
| 21 | `rolling_aggressive_sell_quantity_1s` | feature | string (Decimal-as-string) | no | sum of `Decimal(quantity)` over trailing window where `is_buyer_maker=true` | causal trailing | `"0"` if no aggressive-sell events |
| 22 | `rolling_aggressive_buy_count_1s` | feature | int64 | no | count over trailing window where `is_buyer_maker=false` | causal trailing | `0` if none |
| 23 | `rolling_aggressive_sell_count_1s` | feature | int64 | no | count over trailing window where `is_buyer_maker=true` | causal trailing | `0` if none |
| 24 | `rolling_aggressive_flow_ratio_1s` | feature | float64 | yes | `aggressive_buy_quantity / (aggressive_buy_quantity + aggressive_sell_quantity)` (Decimal arithmetic, then cast to float64) | causal trailing | null if denominator == 0 |
| 25 | `rolling_aggressive_quantity_imbalance_1s` | feature | string (Decimal-as-string) | no | `aggressive_buy_quantity - aggressive_sell_quantity` (Decimal) | causal trailing | `"0"` if both sides empty |
| 26 | `rolling_log_return_past_window_1s` | feature | float64 | yes | `ln(price(R) / prior_reference_price)` per §22 rule | causal trailing | null if no prior reference price |
| 27 | `rolling_aggtrade_count_5s` | feature | int64 | no | count over 5,000 ms trailing window | causal trailing | `0` if empty |
| 28 | `rolling_quantity_sum_5s` | feature | string | no | Decimal sum over 5,000 ms trailing window | causal trailing | `"0"` if empty |
| 29 | `rolling_quantity_mean_5s` | feature | string | yes | Decimal mean over 5,000 ms trailing window | causal trailing | null if empty |
| 30 | `rolling_aggressive_buy_quantity_5s` | feature | string | no | Decimal sum over 5,000 ms trailing window, `is_buyer_maker=false` | causal trailing | `"0"` if none |
| 31 | `rolling_aggressive_sell_quantity_5s` | feature | string | no | Decimal sum over 5,000 ms trailing window, `is_buyer_maker=true` | causal trailing | `"0"` if none |
| 32 | `rolling_aggressive_buy_count_5s` | feature | int64 | no | count over 5,000 ms trailing window, `is_buyer_maker=false` | causal trailing | `0` if none |
| 33 | `rolling_aggressive_sell_count_5s` | feature | int64 | no | count over 5,000 ms trailing window, `is_buyer_maker=true` | causal trailing | `0` if none |
| 34 | `rolling_aggressive_flow_ratio_5s` | feature | float64 | yes | as above for 5,000 ms | causal trailing | null if denominator == 0 |
| 35 | `rolling_aggressive_quantity_imbalance_5s` | feature | string | no | as above for 5,000 ms | causal trailing | `"0"` if empty |
| 36 | `rolling_log_return_past_window_5s` | feature | float64 | yes | as above for 5,000 ms | causal trailing | null if no prior reference price |
| 37 | `rolling_aggtrade_count_15s` | feature | int64 | no | count over 15,000 ms trailing window | causal trailing | `0` if empty |
| 38 | `rolling_quantity_sum_15s` | feature | string | no | Decimal sum over 15,000 ms trailing window | causal trailing | `"0"` if empty |
| 39 | `rolling_quantity_mean_15s` | feature | string | yes | Decimal mean over 15,000 ms trailing window | causal trailing | null if empty |
| 40 | `rolling_aggressive_buy_quantity_15s` | feature | string | no | Decimal sum over 15,000 ms trailing window, `is_buyer_maker=false` | causal trailing | `"0"` if none |
| 41 | `rolling_aggressive_sell_quantity_15s` | feature | string | no | Decimal sum over 15,000 ms trailing window, `is_buyer_maker=true` | causal trailing | `"0"` if none |
| 42 | `rolling_aggressive_buy_count_15s` | feature | int64 | no | count over 15,000 ms trailing window, `is_buyer_maker=false` | causal trailing | `0` if none |
| 43 | `rolling_aggressive_sell_count_15s` | feature | int64 | no | count over 15,000 ms trailing window, `is_buyer_maker=true` | causal trailing | `0` if none |
| 44 | `rolling_aggressive_flow_ratio_15s` | feature | float64 | yes | as above for 15,000 ms | causal trailing | null if denominator == 0 |
| 45 | `rolling_aggressive_quantity_imbalance_15s` | feature | string | no | as above for 15,000 ms | causal trailing | `"0"` if empty |
| 46 | `rolling_log_return_past_window_15s` | feature | float64 | yes | as above for 15,000 ms | causal trailing | null if no prior reference price |
| 47 | `rolling_aggtrade_count_60s` | feature | int64 | no | count over 60,000 ms trailing window | causal trailing | `0` if empty |
| 48 | `rolling_quantity_sum_60s` | feature | string | no | Decimal sum over 60,000 ms trailing window | causal trailing | `"0"` if empty |
| 49 | `rolling_quantity_mean_60s` | feature | string | yes | Decimal mean over 60,000 ms trailing window | causal trailing | null if empty |
| 50 | `rolling_aggressive_buy_quantity_60s` | feature | string | no | Decimal sum over 60,000 ms trailing window, `is_buyer_maker=false` | causal trailing | `"0"` if none |
| 51 | `rolling_aggressive_sell_quantity_60s` | feature | string | no | Decimal sum over 60,000 ms trailing window, `is_buyer_maker=true` | causal trailing | `"0"` if none |
| 52 | `rolling_aggressive_buy_count_60s` | feature | int64 | no | count over 60,000 ms trailing window, `is_buyer_maker=false` | causal trailing | `0` if none |
| 53 | `rolling_aggressive_sell_count_60s` | feature | int64 | no | count over 60,000 ms trailing window, `is_buyer_maker=true` | causal trailing | `0` if none |
| 54 | `rolling_aggressive_flow_ratio_60s` | feature | float64 | yes | as above for 60,000 ms | causal trailing | null if denominator == 0 |
| 55 | `rolling_aggressive_quantity_imbalance_60s` | feature | string | no | as above for 60,000 ms | causal trailing | `"0"` if empty |
| 56 | `rolling_log_return_past_window_60s` | feature | float64 | yes | as above for 60,000 ms | causal trailing | null if no prior reference price |
| 57 | `utc_hour` | feature | int8 | no | `(transact_time_ms / 1000 / 3600) % 24` derived as integer hour 0..23 | n/a (point-in-time) | n/a |
| 58 | `utc_minute` | feature | int8 | no | `((transact_time_ms / 1000) / 60) % 60` derived as integer minute 0..59 | n/a (point-in-time) | n/a |
| 59 | `milliseconds_since_day_start` | feature | int64 | no | `transact_time_ms - utc_day_start_ms` for the row's `utc_date` | n/a (point-in-time) | n/a |
| 60 | `invalid_window_flag` | quality | bool | no | `true` iff the source row's `transact_time_ms` intersects any source-propagated `invalid_windows` entry | n/a | n/a |
| 61 | `rolling_missing_window_flag` | quality | bool | no | `true` iff any trailing window for this row intersects an `invalid_windows` entry | causal trailing | n/a |

**Final column count: 61** (16 identity / lineage / metadata + 45 features).

---

## 16. Dtype policy

| Column class | Dtype | Notes |
| ------------ | ----- | ----- |
| identity strings | `string` | non-null |
| `symbol`, `utc_date` | `string` | non-null |
| `agg_trade_id`, `row_index` | `int64` | non-null |
| `feature_timestamp_ms`, `source_transact_time_ms` | `int64` | non-null |
| hash columns | `string` | non-null |
| `feature_config_hash` | `string` | non-null |
| count features | `int64` | non-null |
| quantity sums / aggressive-side quantities / quantity means / quantity imbalances | `string` (Decimal-as-string) | nullable only for `rolling_quantity_mean_<window>` |
| `rolling_aggressive_flow_ratio_<window>` | `float64` | nullable; null when denominator == 0 |
| `rolling_log_return_past_window_<window>` | `float64` | nullable; null when no prior reference price |
| `utc_hour` | `int8` | non-null; 0..23 |
| `utc_minute` | `int8` | non-null; 0..59 |
| `milliseconds_since_day_start` | `int64` | non-null |
| `invalid_window_flag`, `rolling_missing_window_flag` | `bool` | non-null |

If pyarrow `int8` is impractical at storage time, `int16` is acceptable for `utc_hour` and `utc_minute`; `int8` and `int16` are both equivalent semantically.

---

## 17. Null / NaN policy

- count features (`rolling_aggtrade_count_<window>`, `rolling_aggressive_*_count_<window>`): `0` if empty window, never null;
- quantity sums (`rolling_quantity_sum_<window>`, `rolling_aggressive_*_quantity_<window>`): `"0"` (Decimal-as-string) if empty / no events, never null;
- quantity means (`rolling_quantity_mean_<window>`): null if empty window;
- aggressive flow ratios (`rolling_aggressive_flow_ratio_<window>`): null if `aggressive_buy_quantity + aggressive_sell_quantity == 0`; never produced from float NaN arithmetic without an explicit zero-denominator check;
- aggressive-quantity imbalance (`rolling_aggressive_quantity_imbalance_<window>`): `"0"` if both sides empty (Decimal-as-string of zero);
- log returns (`rolling_log_return_past_window_<window>`): null if no prior reference price exists at `T - window_ms` (or earlier); never NaN; never `-inf` / `+inf`;
- time-context columns (`utc_hour`, `utc_minute`, `milliseconds_since_day_start`): non-null;
- quality flags (`invalid_window_flag`, `rolling_missing_window_flag`): non-null bools;
- identity / lineage / metadata columns: non-null.

**No imputation.** Across invalid windows, no forward-fill, no carry-over, no mean substitution.

---

## 18. Decimal / float policy

- raw `price` and raw `quantity` from the source normalized Parquet are always read as Decimal-as-string and parsed with `Decimal`;
- raw `price` and raw `quantity` must **never** be stored as float in the future feature dataset;
- quantity sums, aggressive-side quantities, quantity means, and aggressive quantity imbalances must be stored as Decimal-as-string in Parquet;
- aggressive flow ratios may be stored as `float64` because they are derived ratios bounded in `[0, 1]` (or null);
- log returns may be stored as `float64` because they are derived statistics; the `Decimal` price is converted to `float` only at the moment of `math.log` (or equivalent) computation;
- any future float column must be explicitly identified as a derived statistic, not a source value;
- `rolling_quantity_mean_<window>` is stored as Decimal-as-string (to preserve exactness) computed as `Decimal(quantity_sum) / Decimal(count)`; the future implementation must use `Decimal` arithmetic and a documented Decimal context (precision/rounding) and may not introduce float in the divisor.

The future Phase 4bh implementation **must** declare the Decimal context (precision, rounding mode) in the feature config and include the context in `feature_config_hash`.

---

## 19. Invalid-window propagation policy

Current expected: `invalid_windows = []` (Phase 4be / Phase 4bf evidence). Future feature implementation must still support invalid-window propagation:

- if the source manifest's `invalid_windows == []` at runtime, then every row's `invalid_window_flag = false` and `rolling_missing_window_flag = false`;
- if invalid windows ever exist, any row whose `transact_time_ms` falls inside an invalid window has `invalid_window_flag = true`;
- any row whose any trailing window of length `window_ms` intersects an invalid window has `rolling_missing_window_flag = true` (note: this is a row-level flag computed once per feature row; it is `OR`ed across all four windows);
- alternatively, a future implementation may emit per-window flags (`rolling_missing_window_flag_<window>`); the schema in §15 specifies a single combined flag;
- no imputation across invalid windows;
- no forward-fill across invalid windows;
- the source `invalid_windows` list must be propagated verbatim into the future feature manifest.

---

## 20. Causal windowing rules

For a feature row at source `transact_time_ms = T` and `row_index = R`:

- the trailing window of length `window_ms` includes source rows whose `transact_time_ms` falls in `(T - window_ms, T]`;
- ties at `T` are tie-broken by `row_index <= R` to prevent same-timestamp future-row leakage; specifically, only source rows with `(transact_time_ms < T)` OR `(transact_time_ms == T AND row_index <= R)` may contribute to the feature row;
- ordering key: `(transact_time_ms ASC, row_index ASC)`;
- no source row with `(transact_time_ms > T)` OR `(transact_time_ms == T AND row_index > R)` may contribute to the feature row;
- this same-timestamp tie-break rule is **mandatory**; future test plan §24 requires explicit unit tests covering same-timestamp ties.

---

## 21. Aggressive-side rule

Using Binance aggTrades `is_buyer_maker`:

- `is_buyer_maker = false` ⇒ buyer was the taker / aggressive buyer;
- `is_buyer_maker = true` ⇒ seller was the taker / aggressive seller.

Therefore:

- `rolling_aggressive_buy_*_<window>` aggregates source rows in the trailing window with `is_buyer_maker = false`;
- `rolling_aggressive_sell_*_<window>` aggregates source rows in the trailing window with `is_buyer_maker = true`.

This convention is consistent with Phase 4ax `aggtrades.py`'s `derive_taker_side()` which returns `TakerSide.BUY` for `m=False` and `TakerSide.SELL` for `m=True`. The future Phase 4bh implementation **must** use this convention verbatim.

---

## 22. Price rule for `rolling_log_return_past_window_<window>`

For row `R` with timestamp `T`:

1. **current price** = `Decimal(price)` of source row `R`.
2. **prior reference price** = the price of the **last** source row whose `transact_time_ms <= T - window_ms`, with same-timestamp tie-break by `row_index ASC` (i.e., among ties, the largest `row_index` whose `transact_time_ms` is exactly `T - window_ms` or less). If no such prior row exists, output null.
3. **log return** = `ln(float(current_price) / float(prior_reference_price))`.
4. parse `price` strings as `Decimal` first; convert to `float` only at the moment of the `log` call;
5. no future high / low / close may be used; no peeking at any row with `transact_time_ms > T`.

Special cases:

- if the prior reference price is `Decimal("0")` (should never happen given Phase 4ax validator), output null and treat as a data-quality issue;
- if the current price is `Decimal("0")`, output null;
- if the dataset begins inside an invalid window or has insufficient history at `T - window_ms`, output null;
- if `prior_reference_price` lies in or is bounded by an invalid window, output null AND set `rolling_missing_window_flag = true`.

The future implementation may optimize this lookup using a sorted index over `transact_time_ms` (the source Parquet is already monotonic non-decreasing on `transact_time_ms`), but the behavioural contract above is binding.

---

## 23. Forbidden columns and forbidden transforms

Any future Phase 4bh implementation **must fail closed at validation time** if any output column name (lowercased) contains any of the following substrings:

```text
label
target
future
signal
entry
exit
pnl
profit
loss
mfe
mae
r_multiple
equity
position
alpha
edge
prediction
model
score
decision
strategy
liquidation
funding
open_interest
order_book
mark_price
```

The substring check is enforced verbatim by the future Phase 4bh validation module. Exceptions are not granted by Phase 4bh-B; if a future column name conflicts, the future Phase 4bh implementation must rename (e.g., a column intended as a "future-time-context" descriptor must avoid the substring "future" — there is no such column in the finalized schema).

Forbidden transforms include:

- using rows with `(transact_time_ms > T)` OR `(transact_time_ms == T AND row_index > R)`;
- centered windows;
- forward-filling across invalid windows;
- forward-filling across an empty window;
- imputing a future-known statistic;
- z-scores using full-day or future-data normalization;
- thresholds fitted on the same evaluation period without an explicit train-only fitting policy;
- any transform that revises or rescues a previously rejected strategy verdict.

---

## 24. Feature manifest schema

The future feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` (NOT created by this memo) must include at minimum:

| Field | Value / Description |
| ----- | ------------------- |
| `dataset_family` | `"microstructure_features_aggtrades_v001"` |
| `dataset_version` | `"v001"` |
| `feature_schema_version` | `"v001"` |
| `symbol` | `"BTCUSDT"` |
| `utc_date` | `"2025-01-15"` |
| `source_normalized_dataset_family` | `"microstructure_normalized_aggtrades_v001"` |
| `source_normalized_dataset_version` | `"v001"` |
| `source_normalized_manifest_sha256` | `"f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9"` |
| `source_normalized_parquet_sha256` | `"2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa"` |
| `source_successor_state_sha256` | `"8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e"` |
| `source_phase_4bf_gate_report_sha256` | `"dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6"` |
| `feature_config_hash` | deterministic SHA256 over canonical-JSON serialization of the feature config |
| `feature_list` | ordered tuple of 45 feature names exactly as listed in §13 (windowed columns ordered by `(window_ms ASC, feature_class)`) |
| `window_list` | `["1s", "5s", "15s", "60s"]` |
| `window_ms_list` | `[1000, 5000, 15000, 60000]` |
| `row_count` | expected `1681098` for BTCUSDT 2025-01-15 |
| `invalid_windows` | propagated from source normalized manifest verbatim |
| `files` | array of `{path, sha256, row_count}` for each feature Parquet file |
| `governance_labels` | nested object including: `phase_id="4bh"`, `feature_computation="allowed_by_phase_4bh_only_if_separately_authorized"`, `labels="forbidden"`, `ml="forbidden"`, `strategy="forbidden"`, `backtest="forbidden"`, `acquisition="unauthorized"`, `stop_trigger_domain="trade_price_backtest_candidate"` (preserved) |
| `research_eligible` | `false` |
| `eligibility_gate_status` | `"pending"` |
| `code_commit_sha` | git commit SHA at runtime |
| `created_at_unix_ms` | `int64` UTC ms |

The future feature manifest must be implemented using a `MicrostructureManifest`-equivalent type that preserves the Phase 4aw `flip_research_eligible(...)` always-raises invariant.

---

## 25. Feature config schema

The future feature config object (NOT created by this memo) must be a deterministic JSON-serializable dict containing:

| Key | Description |
| --- | ----------- |
| `dataset_family` | `"microstructure_features_aggtrades_v001"` |
| `dataset_version` | `"v001"` |
| `feature_schema_version` | `"v001"` |
| `input_paths` | list of source Parquet paths (one per partition) |
| `source_normalized_manifest_path` | path to source normalized manifest |
| `source_successor_state_path` | path to source successor-state JSON |
| `output_paths` | list of feature Parquet output paths |
| `output_manifest_path` | path to feature manifest JSON |
| `windows_ms` | ordered list `[1000, 5000, 15000, 60000]` |
| `feature_names` | ordered tuple of 45 feature names exactly as in §13 |
| `timestamp_alignment` | `"event_aligned"` |
| `causal_window_rule` | `"trailing_right_open_left"` (window is `(T - window_ms, T]`) |
| `same_timestamp_tie_rule` | `"row_index_le_R"` |
| `null_policy` | object describing per-column null rules per §17 |
| `invalid_window_policy` | object describing propagation per §19 |
| `decimal_policy` | object: `{precision: int, rounding: str, decimal_columns: [...]}` |
| `code_commit_sha` | git commit SHA at runtime |

`feature_config_hash = sha256(canonical_json(config))` where `canonical_json` is `json.dumps(config, sort_keys=True, separators=(',', ':'), ensure_ascii=True)`. The hash must be deterministic and reproducible.

---

## 26. Implementation module plan for future Phase 4bh

Proposed (NOT created by this memo) future module layout under `src/prometheus/research/microstructure/`:

| Module | Purpose |
| ------ | ------- |
| `features_schema.py` | `FEATURE_SCHEMA_V001`, `FEATURE_NAMES`, `WINDOWS_MS`, `FORBIDDEN_SUBSTRINGS`, dataclass-based row model, exceptions |
| `features_io.py` | read-only loaders for normalized Parquet, derived manifest, successor-state JSON; atomic feature Parquet writer; refuse-to-overwrite; paired SHA256 sidecar; path discipline |
| `features_compute.py` | causal trailing-window aggregations; deterministic ordering; Decimal arithmetic for quantity / sum / mean / imbalance; float casts only at log / ratio computation; same-timestamp tie-break |
| `features_manifest.py` | feature manifest builder + atomic JSON writer; `MicrostructureManifest`-equivalent that preserves the `flip_research_eligible(...)` always-raises invariant |
| `features_validation.py` | full schema-equality assertion; forbidden-substring scan; null / NaN policy enforcement; lineage SHA verification; row-count parity (`row_count == 1681098`) |
| `__init__.py` | narrow re-export update only (no prior export removed) |

No `scripts/...` entrypoint required; future Phase 4bh should be invokable via direct module import from a one-shot orchestrator if separately authorized (similar to Phase 4bf's `run_derived_aggtrades_gate` pattern).

---

## 27. Test plan for future Phase 4bh

Proposed (NOT created by this memo) future test layout under `tests/research/microstructure/`:

| Test file | Coverage |
| --------- | -------- |
| `_features_fixtures.py` (optional) | shared synthetic fixtures (same-timestamp ties, all-buyer-maker, all-seller-maker, mixed, invalid-window, single-event, empty-window) |
| `test_features_schema.py` | `FEATURE_SCHEMA_V001` constant tests; ordered name list; forbidden-substring detector smoke tests |
| `test_features_io.py` | atomic write, refuse-to-overwrite, path discipline (writes only under `data/microstructure/features/` and `data/microstructure/manifests/`), sidecar SHA match |
| `test_features_compute.py` | per-feature unit tests for trailing-window correctness, leakage absence, NaN policy, invalid-window propagation, type stability, deterministic ordering, same-timestamp tie-break, log-return null cases |
| `test_features_manifest.py` | manifest builder, lineage SHA propagation, governance-label invariants, `flip_research_eligible(...)` always-raises preserved |
| `test_features_validation.py` | full schema-equality, forbidden-substring scan (positive + negative), null policy enforcement, row-count parity, null-policy tests per column class |
| `test_features_no_network.py` | static scan that the new feature modules contain no `prometheus.runtime`/`execution`/`persistence` imports, no `requests`/`httpx`/`aiohttp`/`urllib.request`/`urllib3`/`socket`/`websockets`/`binance`/`dotenv`/`python_dotenv`/`os.environ`/`getenv`, and no credential / `.mcp.json` / Graphify tokens |

Test plan also requires:

- per-feature golden-fixture tests on a small synthetic input;
- a one-symbol/one-day end-to-end run on the existing Phase 4bd / Phase 4be / Phase 4bf-passed normalized artefact (BTCUSDT 2025-01-15) producing a gitignored feature Parquet + manifest + sidecar under `data/microstructure/features/...`;
- whole-repo `ruff check .` clean;
- whole-repo `mypy src/prometheus` strict clean;
- whole-repo `pytest` clean except for the same pre-existing `KeyError: 'trade_count'` simulation failures.

---

## 28. Acceptance criteria for future Phase 4bh

A future Phase 4bh implementation is acceptable only if:

1. implements **exactly** the finalized schema in §15 (16 lineage / identity / metadata + 45 features = 61 columns);
2. respects the canonical input (§8) and forbidden inputs (Phase 4bh-A §9);
3. respects the Phase 4bg-B successor-state Stage-3 marker (§8) and refuses to interpret the original derived manifest alone as Stage-3;
4. uses event-aligned output rows with expected `row_count = 1,681,098` for BTCUSDT 2025-01-15 (§10);
5. uses `feature_timestamp_ms = source transact_time_ms` (§11);
6. implements only the four windows `{1s, 5s, 15s, 60s}` (§12);
7. respects the temporal-leakage boundary and the same-timestamp tie-break rule (§20);
8. respects the dtype policy (§16);
9. respects the null / NaN policy (§17);
10. respects the decimal / float policy (§18);
11. respects the invalid-window propagation policy (§19);
12. respects the aggressive-side rule (§21);
13. respects the price rule for `rolling_log_return_past_window_<window>` (§22);
14. fails closed if any output column name contains a forbidden substring (§23);
15. emits a feature manifest matching §24, including all required lineage SHAs and governance labels;
16. emits a feature config matching §25, including a deterministic `feature_config_hash`;
17. writes only under `data/microstructure/features/` and `data/microstructure/manifests/` (for the feature manifest); refuses overwrite at writer level; produces paired SHA256 sidecars; writes are atomic (write-then-rename);
18. preserves all source artefact SHAs byte-identically pre/post run (derived manifest `f6f0d947…`, normalized Parquet `2b3d6978…`, raw manifest `a371edd4…`, raw zip `f560c2e5…`, Phase 4bb-D gate report `96f09159…`, Phase 4bf gate report `dd4e0c1c…`, Phase 4bg-B successor-state JSON `8bcc7d01…`);
19. preserves the Phase 4aw `flip_research_eligible(...)` always-raises invariant on every manifest type used;
20. creates no labels, targets, signals, ML, strategy, or backtest artefacts;
21. emits feature manifest with `research_eligible=false` and `eligibility_gate_status=pending`;
22. runs as a standalone phase with no `prometheus.runtime` / `prometheus.execution` / `prometheus.persistence` imports, no exchange adapters, no `requests/httpx/aiohttp/websockets/urllib`, no `.env` reads, no credentials, no Binance API, and no network I/O;
23. passes `ruff check .`, `mypy src/prometheus` strict, targeted feature tests, microstructure tests, and whole-repo `pytest` with only the pre-existing simulation failures;
24. does not commit anything under `data/microstructure/`;
25. is followed by a separately authorized Phase 4bi-A structural QA memo before any feature-family eligibility-gate work begins;
26. authorizes no successor.

---

## 29. Fail-closed rules

The following are binding on any future Phase 4bh implementation:

1. **Path discipline.** No write may occur outside `data/microstructure/features/` and `data/microstructure/manifests/`. The Phase 4bd normalized Parquet path, the Phase 4bd derived manifest path, the Phase 4bf gate report path, and the Phase 4bg-B successor-state path must remain byte-immutable.
2. **Manifest-mutation discipline.** The original Phase 4bd derived manifest must not be mutated. The future feature manifest is a new sibling artefact, never a replacement of the normalized derived manifest.
3. **Raw-family discipline.** The raw family `microstructure_raw_aggtrades_v001` remains `research_eligible=false` permanently.
4. **Successor-state discipline.** The Phase 4bg-B successor-state JSON must be cited by SHA in the future feature manifest. The original derived manifest alone is not a Stage-3 marker.
5. **Stage-3 discipline.** Stage-3 admissibility at successor-state level is not a license for feature computation by itself; a future Phase 4bh implementation requires its own authorization.
6. **Stage-4 discipline.** Stage-4 (feature-family eligibility-gate-passed) is not implied. A separately authorized Phase 4bi-B is required.
7. **Network discipline.** No network / endpoint / credential / `.env` / `.mcp.json` / MCP / Graphify access by any future Phase 4bh module.
8. **Static-import discipline.** `test_features_no_network.py` must remain green and must scan the new feature modules.
9. **Forbidden-substring discipline.** Output column names must not contain any forbidden substring (§23).
10. **Decimal discipline.** Raw `price` and raw `quantity` may never be stored as `float`.
11. **Tie-break discipline.** Same-timestamp tie-break by `row_index <= R` is mandatory.
12. **Refuse-overwrite discipline.** Feature Parquet, sidecar, and feature manifest writers must refuse to overwrite existing artefacts.
13. **Row-count parity.** The future feature dataset must emit exactly `1,681,098` rows for BTCUSDT 2025-01-15. Mismatch is a fail-closed condition.
14. **Cooldown discipline.** Cooled-down family classifications are not loosened by Phase 4bh-B or any future Phase 4bh.
15. **Cost-realism discipline.** §11.6 = 8 bps per side and round-trip = 16 bps remain binding for any future strategy candidate that ever consumes microstructure-derived features.
16. **No-rescue discipline.** Phase 4al refined no-rescue rule remains binding.
17. **Label / signal / ML discipline.** No future phase consuming Phase 4bh-B may create labels, signals, ML, strategies, or backtests without separate authorization beyond Phase 4bh.

---

## 30. What this phase proves

- that the project record contains a complete, finalized feature schema for any future Phase 4bh implementation, with exact column list, dtype policy, null / NaN policy, decimal / float policy, invalid-window propagation policy, causal windowing rules, lineage and metadata columns, manifest schema, feature-config schema, future module / test layout, and acceptance criteria;
- that the Phase 4bh-A boundary (canonical input, forbidden inputs, forbidden classes, leakage rule, M0 / cooled-down / no-rescue boundaries) is preserved verbatim and converted into an implementable contract;
- that the original derived manifest, the normalized Parquet, the Phase 4bb-D / Phase 4bf gate reports, and the Phase 4bg-B successor-state JSON are not modified;
- that no feature is computed and no successor is authorized by Phase 4bh-B.

---

## 31. What this phase does not prove

- that the finalized features will be statistically meaningful for any specific research question;
- that any future Phase 4bh implementation will produce a Stage-2 feature artefact that passes structural QA;
- that any feature-family eligibility gate will pass;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible.

---

## 32. Preserved boundaries

- H0 — FRAMEWORK ANCHOR.
- R3 — BASELINE-OF-RECORD.
- R1a / R1b-narrow — RETAINED — NON-LEADING.
- R2 — FAILED — §11.6.
- F1 — HARD REJECT.
- D1-A — MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread — OPERATIONALLY CLOSED (Phase 3t).
- V2 — HARD REJECT — terminal for V2 first-spec.
- G1 — HARD REJECT — terminal for G1 first-spec.
- C1 — HARD REJECT — terminal for C1 first-spec.
- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A results — all preserved.

---

## 33. Recommended future options

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | docs-only / no work | recommended |
| **Conditional next, if more review desired** — Phase 4bh-C Feature Schema Finalization Review / Red-Team Memo | docs-only | NOT authorized by this memo |
| **Conditional direct implementation** — Phase 4bh AggTrades Feature Schema / Feature Computation Implementation, code + docs + local gitignored feature artefacts only, using the exact Phase 4bh-B finalized schema | code + docs | NOT authorized by this memo |
| **Conditional after feature implementation** — Phase 4bi-A Feature Artefact Structural QA Memo | analysis + docs | NOT authorized by this memo |
| **Conditional cleanup** — Phase 4bb-F Gate Report Output Path Hygiene, before any repeated raw gate execution | code + docs | NOT authorized by this memo |
| **Conditional raw policy marker** — Phase 4bb-G Raw Manifest Successor-State Recording | docs-only or docs-and-local-gitignored-output | NOT authorized by this memo |
| Acquisition (additional days / symbols / data families) | docs + data | NOT authorized; not in scope |
| Feature computation, ML, strategy, backtests | code + data | FORBIDDEN by Phase 4bh-A and Phase 4bh-B |
| Paper / shadow / live / exchange-write / production keys | runtime | FORBIDDEN |

---

## 34. Closeout / lock preservation

Phase 4bh-B is docs-only and produces:

- this memo (`docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_aggtrades-feature-schema-finalization.md`);
- the Phase 4bh-B closeout (`docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_closeout.md`);
- a narrow Phase 4bh-B paragraph + new "Current phase:" block in `docs/00-meta/current-project-state.md` (prior Phase 4bh-A block preserved as historical context).

No source code, tests, scripts, configs, READMEs, MCP files, runtime configuration, manifests, raw artefacts, gate reports, successor-state artefacts, feature artefacts, or `.gitignore` entries were modified.

The `data/microstructure/` namespace is untouched. The Phase 4bd derived manifest, the normalized Parquet, the raw manifest, the raw zip, the raw sidecar, the acquisition log, the Phase 4bb-D gate report, the Phase 4bf gate report, and the Phase 4bg-B successor-state JSON all remain byte-identical.

The recorded outcome is: **feature schema finalized at policy level**. Feature Stage-0 design (Phase 4bh-A) is converted to an implementable contract. Original derived manifest remains `research_eligible=false / eligibility_gate_status=pending`. Raw family remains permanently `research_eligible=false`. Feature computation, ML, strategy, backtests, and acquisition all remain unauthorized. No successor phase is authorized by Phase 4bh-B.

**Recommended state: remain paused.**
