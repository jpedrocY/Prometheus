# Phase 4bh-A — AggTrades Feature-Boundary Design Memo

**Phase identity:** Phase 4bh-A — AggTrades Feature-Boundary Design Memo.
**Phase type:** docs-only feature-boundary design memo.
**Date:** 2026-05-10.
**Branch:** `phase-4bh-a/aggtrades-feature-boundary-design`.
**Base:** `main` at the post-Phase-4bg-B merge-closeout state (`81747263a12b5593282f2f5cfbb17ed413a84cb3`); Phase 4bg-B merge commit `f134a7bbcf04b51139b8094ebc13839e50f5302e` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

This memo defines the feature boundary that any future feature work on the Stage-3 successor-state-normalized aggTrades family must respect before any feature-computation phase is authorized. It is **docs-only**: no feature is computed, no feature dataset is written, no manifest is created, no source code or test or script is added or modified, no data is acquired, and no successor phase is authorized.

The memo records the canonical input, the forbidden inputs, the proposed feature-family naming, the feature-stage model, definitions of feature / label / signal / feature-computation, the allowed and forbidden feature classes, the temporal-leakage boundary, the windowing / aggregation / precision / type / missing-window policies, the proposed output namespace and manifest, the validation gate sequence, the M0 admissibility boundary, the cooled-down lane boundary, the ML / strategy / backtest boundary, the acquisition boundary, the acceptance criteria for any future Phase 4bh, the fail-closed rules, and the recommended future options.

The Phase 4ak twelve-clause M0 mechanism-admissibility gate, the post-null cooldown rule, the cooled-down families list, the Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, every retained verdict, and every project lock are preserved verbatim by this phase.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bg-B merge commit (ancestor of `main`) | `f134a7bbcf04b51139b8094ebc13839e50f5302e` |
| `main == origin/main` (start of Phase 4bh-A) | `81747263a12b5593282f2f5cfbb17ed413a84cb3` |
| Raw family | `microstructure_raw_aggtrades_v001` |
| Raw manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` (immutable; permanent) |
| Derived family | `microstructure_normalized_aggtrades_v001` |
| Derived manifest `research_eligible` / `eligibility_gate_status` (original) | `false` / `pending` (immutable in this phase) |
| Phase 4bg-B successor-state JSON (gitignored, locally present) | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json` (SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`) |
| Successor-state contents | `successor_stage=Stage-3`, `successor_research_eligible=true`, `successor_eligibility_gate_status=pass` |
| Phase 4bf gate report SHA256 (gitignored, locally present) | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bb-D raw gate report SHA256 (gitignored, locally present) | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Normalized Parquet SHA256 | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Derived manifest SHA256 | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Raw manifest SHA256 | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip SHA256 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |

---

## 3. Inputs reviewed

- Phase 4az (acquisition; raw `microstructure_raw_aggtrades_v001`).
- Phase 4ba (5-stage eligibility ladder).
- Phase 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E (raw eligibility gate design, plan, primitive, execution, successor-state policy).
- Phase 4bc / 4bd-A / 4bd / 4be (normalization design, plan, implementation, structural QA).
- Phase 4bf-A / 4bf (derived-family eligibility-gate design, implementation and execution).
- Phase 4bg-A (research-eligibility decision; Option B / Decision form 2).
- Phase 4bg-B (successor-state recording; Outcome 1).
- Phase 4ak M0 governance adoption (twelve-clause gate, post-null cooldown, cooled-down families list, memo template).
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Project locks (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w).
- Retained verdict ledger (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1).

No prior memo's text was modified. No artefact under `data/microstructure/` was modified.

---

## 4. Scope

In scope for this memo:

- defining the canonical input family for any future feature work on aggTrades;
- defining forbidden inputs and forbidden feature classes;
- naming a future feature family without creating it;
- defining a future feature-stage model;
- defining the temporal-leakage / windowing / aggregation / precision / type / missing-window policies;
- defining the future output namespace and future manifest schema without creating either;
- defining the validation gate sequence that must follow any future Phase 4bh implementation;
- recording the M0 / cooled-down / no-rescue boundaries that any future feature work must respect;
- recording acceptance criteria for any future Phase 4bh implementation phase.

---

## 5. Non-scope

This memo does **not**:

- compute features;
- create feature files, datasets, manifests, or sidecar files;
- create JSONL, Parquet, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- modify source code, tests, scripts, configurations, README, `pyproject.toml`, `.gitignore`, or governance memo;
- run the normalizer, the raw eligibility gate, or the derived-family eligibility gate;
- generate a new gate report;
- create a replacement derived manifest, replacement raw manifest, or any sibling manifest;
- modify the successor-state artefact or create a new successor-state artefact;
- mutate any `research_eligible` field or any `eligibility_gate_status` field;
- acquire data; call public endpoints; call Binance APIs; open WebSockets; use private endpoints; use credentials; read or create `.env`; create `.mcp.json`; or enable MCP / Graphify;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- create labels, targets, or strategy signals;
- train ML, create strategy logic, run backtests, or run simulations;
- authorize feature computation, Stage-4 feature-cleared status, ML, strategy, or backtests;
- revise retained verdicts, change project locks, or amend M0;
- authorize Phase 4bh, Phase 4bh-B, Phase 4bi, Phase 4bj, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bg-B Stage-3 successor-state dependency

This memo treats the normalized derived family as Stage-3 only via the Phase 4bg-B successor-state artefact at:

`data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`

with SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`. The original derived manifest's `research_eligible=false` field is byte-immutable; tools that read only the original manifest must continue to treat the derived family as Stage-1-equivalent. Any future feature work must explicitly cite the successor-state SHA, refuse to interpret the original manifest alone as Stage-3, and preserve the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant.

---

## 7. Feature-boundary objective

- define exactly one canonical input family for future feature work;
- define forbidden inputs explicitly;
- define a future feature-family name without creating it;
- define a feature-stage model that mirrors the Phase 4ba 5-stage data-eligibility ladder;
- define what counts as a feature, a label, a signal, and feature computation;
- define the leakage boundary, the windowing policy, the aggregation policy, the precision/type policy, and the missing-window/invalid-window policy;
- define the future output namespace and the future feature manifest schema without creating either;
- record the validation gate sequence that any future Phase 4bh must respect;
- record the M0, cooled-down, and no-rescue boundaries;
- record the acceptance criteria for any future Phase 4bh implementation phase;
- record fail-closed rules.

---

## 8. Canonical input family

The only eligible input family for future feature design is the normalized derived family:

```text
microstructure_normalized_aggtrades_v001
```

with the canonical 19-column trade-record-level Phase 4bc schema:

`dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `symbol`, `utc_date`, `agg_trade_id` (`int64`), `price` (string-decimal), `quantity` (string-decimal), `first_trade_id` (`int64`), `last_trade_id` (`int64`), `transact_time_ms` (`int64`), `is_buyer_maker` (`bool`), `source_file_sha256`, `source_manifest_sha256`, `source_gate_report_id`, `source_gate_report_sha256`, `row_index` (`int64`), `normalization_schema_version`.

Stage-3 admissibility may be claimed only via the Phase 4bg-B successor-state artefact (§6). The original derived manifest alone must not be interpreted as `research_eligible=true`.

---

## 9. Forbidden input families

The following are forbidden as direct feature input sources unless separately authorized in a future acquisition / design phase that satisfies M0 admissibility:

- raw aggTrades family `microstructure_raw_aggtrades_v001` as direct feature source;
- raw zip as direct feature source;
- raw manifest as direct feature source;
- Phase 4bb-D raw gate report as data source;
- Phase 4bf derived-family gate report as data source;
- any future endpoint, WebSocket, or live feed;
- any external market-data source not separately authorized;
- any future price / outcome data not already inside the normalized Stage-3 family;
- any feature that requires mark price, order book, liquidation data, funding rate, open interest, or cross-symbol data;
- any feature that requires authenticated REST / private endpoints / public-endpoint calls in code / user stream / WebSocket / listenKey lifecycle / MCP / Graphify / `.mcp.json` / credentials.

---

## 10. Proposed feature-family naming

Proposed (NOT created by this memo):

- feature family name: `microstructure_features_aggtrades_v001`;
- relationship: **sibling derived family**, not a mutation of `microstructure_normalized_aggtrades_v001`;
- proposed future output namespace (NOT created): `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`;
- example future output path (NOT created): `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/`;
- proposed future feature manifest path (NOT created): `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json`;
- proposed future per-file SHA256 sidecar pattern: `<file>.sha256`.

The normalized derived family is **never overwritten** by feature work. The feature family exists as a sibling under `data/microstructure/features/` (a new subdirectory under the existing gitignored `data/microstructure/` namespace). No directory is created in this memo.

---

## 11. Proposed feature-stage model

Mirroring the Phase 4ba data-eligibility ladder (Stage-0 acquired → Stage-1 inspected → Stage-2 gate-passed → Stage-3 research-eligible → Stage-4 feature-cleared), the proposed **feature-family** stage model is:

| Stage | Name | Meaning | Reached by |
| ----- | ---- | ------- | ---------- |
| Feature Stage-0 | feature schema designed | feature schema, leakage policy, windowing, types, etc. predeclared on paper | **Phase 4bh-A (this memo)** |
| Feature Stage-1 | feature implementation exists, never executed | implementation merged but not yet executed on real artefacts | future Phase 4bh implementation, before the first run |
| Feature Stage-2 | feature artefacts exist locally, gitignored, with manifest | feature run produced local feature Parquet + feature manifest + sidecars under `data/microstructure/features/...` | future Phase 4bh execution |
| Feature Stage-3 | feature artefacts structurally QA-passed | future Phase 4bi-A structural QA memo |
| Feature Stage-4 | feature-family eligibility gate-passed | future Phase 4bi-B feature-family eligibility-gate memo + execution |
| Feature Stage-5 | research-use / ML-use decision | future Phase 4bi-C feature-family research-use decision memo, separately authorized |

Phase 4bh-A reaches **Feature Stage-0 only**. No feature artefact is created. No future-stage transition is authorized by Phase 4bh-A.

---

## 12. Feature vs label vs signal definitions

1. **Feature**: a deterministic input measurement computed only from information available at or before the feature timestamp `T`. A feature row at time `T` must use **only** rows with `transact_time_ms <= T`. Features are deterministic, reproducible, and free of future information.
2. **Label**: a future-outcome target used for evaluation or ML training (for example: future return over a horizon, future high / low, future volatility realization, hit/miss of a price level). Labels are **forbidden** in Phase 4bh-A and must require a separately authorized future label-boundary phase.
3. **Signal**: a trading decision, score, rule output, position recommendation, or strategy action. Signals are **forbidden** in Phase 4bh-A and any feature implementation it permits.
4. **Feature computation**: any materialization of a new data column or dataset derived from `microstructure_normalized_aggtrades_v001` beyond the 19-column canonical Phase 4bc schema. Feature computation is **not authorized** by Phase 4bh-A; it requires a separately authorized future Phase 4bh implementation phase.

---

## 13. Allowed feature classes (design-only)

The memo proposes the following first-pass feature *categories* as design candidates. **No feature is approved for computation by Phase 4bh-A.** Any future Phase 4bh must implement only the subset that is explicitly approved by the final Phase 4bh-A memo (this document) and that survives a final Phase 4bh-B schema-finalization memo if one is separately authorized.

### A. Count / intensity features

- `rolling_aggtrade_count` — count of aggTrade events whose `transact_time_ms` falls inside a trailing window ending at `T`.
- `rolling_unique_trade_id_span` — `last_trade_id` minus `first_trade_id` summed across events in a trailing window (proxy for raw-tape trade count subsumed by aggregation).
- `rolling_event_rate` — `rolling_aggtrade_count / window_seconds`.

### B. Volume features

- `rolling_quantity_sum` — sum of `quantity` (Decimal-as-string parsed to Decimal) over a trailing window.
- `rolling_quantity_mean`, `rolling_quantity_median` — descriptive central-tendency metrics over a trailing window.
- `rolling_large_trade_count` — count of aggTrades whose `quantity` exceeds **predeclared** size thresholds. Thresholds must be predeclared and **not** fitted on the same dataset.

### C. Taker-side flow features (using `is_buyer_maker`)

- `rolling_aggressive_buy_quantity` — sum of `quantity` over events with `is_buyer_maker = false` (taker = BUY) in a trailing window.
- `rolling_aggressive_sell_quantity` — sum of `quantity` over events with `is_buyer_maker = true` (taker = SELL) in a trailing window.
- `rolling_aggressive_buy_count` / `rolling_aggressive_sell_count` — count variants.
- `rolling_aggressive_flow_ratio` — `rolling_aggressive_buy_quantity / (rolling_aggressive_buy_quantity + rolling_aggressive_sell_quantity)` with explicit divide-by-zero handling and an explicit NaN policy (proposed: NaN if denominator == 0; never imputed).
- `rolling_aggressive_quantity_imbalance` — `rolling_aggressive_buy_quantity - rolling_aggressive_sell_quantity`.

### D. Price-path descriptive features (past / current data only)

- `rolling_open_price`, `rolling_high_price`, `rolling_low_price`, `rolling_close_price` — descriptive OHLC-like rollups computed only from rows in the trailing window ending at `T`. No carry of future prices, no resampling that synthesizes prices outside observed events.
- `rolling_log_return_past_window` — `log(close_T / close_T_minus_window)` using only past / current data.
- `rolling_realized_volatility_past_window` — realized-volatility estimator (e.g., sum of squared log returns) computed only from past / current observations.

### E. Time-of-day context

- `utc_hour` — `0..23` derived from `transact_time_ms`.
- `utc_minute` — `0..59`.
- `milliseconds_since_day_start` — non-negative integer derived from `transact_time_ms`.

### F. Data-quality / coverage features

- `rolling_missing_window_flag` — boolean indicating whether the trailing window intersects an `invalid_windows` entry.
- `rolling_event_count_coverage_ratio` — `actual_events_in_window / expected_events_in_window` if expected can be deterministically defined; otherwise omitted.
- `invalid_window_flag` — boolean copied from the per-event invalid-window propagation.

These are **design candidates only**. None is approved for computation by Phase 4bh-A.

---

## 14. Forbidden feature classes

The memo explicitly forbids the following from any future feature implementation that consumes Phase 4bh-A:

- future returns as features;
- next-window price movement;
- future high / low;
- future realized volatility;
- future volume;
- labels;
- target columns;
- strategy signals;
- entry / exit flags;
- PnL;
- MFE / MAE;
- R-multiple;
- equity curve;
- position state;
- liquidation, funding, open-interest, order-book, mark-price features unless separately acquired and governed;
- ML embeddings;
- learned representations;
- features using any row after the feature timestamp `T`;
- features that use the full-day distribution to normalize intraday points unless the normalization is explicitly causal (i.e., uses only past / current data);
- z-scores using future data;
- thresholds fitted on the same evaluation period without an explicit train-only fitting policy;
- any feature whose explicit purpose is to revise or rescue a previously rejected strategy verdict (R3 / R2 / F1 / D1-A / V2 / G1 / C1 or any other retained verdict).

---

## 15. Temporal leakage boundary

Binding on any future feature implementation:

- every feature row carries a feature timestamp `T` measured in UTC ms (`int64`);
- a feature at time `T` may only use rows with `transact_time_ms <= T`;
- rolling windows must be **trailing** windows only (closed-on-the-right at `T`);
- centered windows are **forbidden**;
- full-day statistics are **forbidden** unless used only in post-hoc descriptive docs and never in a research feature table;
- all train / validation / out-of-sample / evaluation splits must be **future work**, not part of Phase 4bh-A, not part of Phase 4bh implementation, and not part of any Phase 4bh-B schema-finalization memo;
- label construction is forbidden and must be a later phase (a separately authorized label-boundary phase under M0 admissibility).

---

## 16. Windowing policy

Proposed **candidate** trailing windows (no implementation authorized by Phase 4bh-A):

- 1 second;
- 5 seconds;
- 15 seconds;
- 30 seconds;
- 60 seconds;
- 5 minutes.

Any future Phase 4bh implementation must implement only the subset that is explicitly approved by the final Phase 4bh-A memo (this document) and / or by a future Phase 4bh-B schema-finalization memo. Windows wider than 5 minutes are **not** approved by Phase 4bh-A; they require a separately authorized future memo if ever proposed.

Windows are defined in event time (UTC ms), not in event count. Windows are right-closed at `T` and left-closed at `T - window_ms`. Window endpoints are deterministic; no fractional events are admitted.

---

## 17. Timestamp alignment policy

- feature timestamps `T` are sampled at deterministic offsets to be predeclared by future Phase 4bh-A finalization or future Phase 4bh-B (e.g., every 1 second on the second; every 5 seconds; aligned to event arrival times);
- any sampling cadence must be deterministic and reproducible from inputs alone;
- no clock drift;
- no rounding to local timezone;
- no DST adjustment;
- timestamps remain UTC ms `int64`;
- the half-open UTC day boundary `[2025-01-15T00:00:00.000Z, 2025-01-16T00:00:00.000Z)` from Phase 4bb-A / Phase 4be must be honored for any feature row whose `T` is computed from event arrivals.

---

## 18. Aggregation policy

- aggregation must be deterministic;
- row ordering must use `(transact_time_ms ASC, row_index ASC)`;
- ties must be resolved by `row_index` (ascending);
- no resampling may introduce synthetic trades;
- no forward-fill of price or quantity is permitted, except explicitly documented OHLC carry rules (e.g., "close at `T` is the last observed close at or before `T`"), which must be predeclared in writing and labeled as causal carry, not synthesis;
- no volume may be invented;
- invalid windows (per Phase 4bd `propagate_invalid_windows`) must propagate into feature rows via `invalid_window_flag` and `rolling_missing_window_flag`.

---

## 19. Precision and type policy

- `price` and `quantity` are read as strings (Decimal-as-string from the Phase 4bc canonical schema) and parsed using `Decimal` for intermediate exactness wherever feasible;
- output numeric column types must be declared explicitly in any future feature manifest;
- any unavoidable float output must be explicitly justified in writing and limited to derived ratios / statistics; **raw price** and **raw quantity** must never be stored as float in the future feature dataset;
- timestamps remain UTC ms `int64`;
- boolean columns are strict `bool`;
- `agg_trade_id` and `row_index` remain `int64`;
- every feature row must carry lineage references to the input normalized artefact (`source_dataset_family`, `source_dataset_version`, `source_normalized_parquet_sha256`, `source_normalized_manifest_sha256`) and the Phase 4bg-B successor-state artefact (`source_successor_state_sha256`).

---

## 20. Missing / invalid-window policy

- `invalid_windows` from the source normalized manifest must be propagated into the future feature manifest verbatim;
- per-event `invalid_window_flag` must propagate into per-feature-row `invalid_window_flag`;
- a feature row whose trailing window intersects an invalid window must carry `rolling_missing_window_flag = true`;
- features must **not** silently impute values in invalid windows;
- features must **not** forward-fill across invalid windows;
- the `rolling_event_count_coverage_ratio`, if implemented, must reflect missing observations;
- all NaN policies must be documented per feature; the default is "do not impute".

---

## 21. Output dataset policy

Proposed (NOT created by Phase 4bh-A):

- output format: Apache Parquet under `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-<YYYY-MM-DD>.parquet`;
- one feature dataset file per `(symbol, utc_date)` partition;
- paired SHA256 sidecar `<file>.sha256` with `<sha256>  <basename>\n` content;
- atomic write-then-rename via `os.replace`;
- refuse-to-overwrite at writer level;
- gitignored under the existing `.gitignore:85: data/microstructure/` rule (no `.gitignore` change required);
- no JSONL, no DuckDB, no per-row append-only file, no streaming output.

---

## 22. Manifest policy

Proposed future feature manifest (NOT created by Phase 4bh-A) at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` must include at minimum:

- `dataset_family = microstructure_features_aggtrades_v001`;
- `dataset_version = v001`;
- `feature_schema_version = v001` (or higher; explicit version bump on any schema change);
- `feature_computation_config_hash` (a deterministic hash of the feature config);
- `feature_list` (ordered list of feature column names);
- `window_list` (ordered list of windows used);
- source lineage:
  - `source_normalized_dataset_family = microstructure_normalized_aggtrades_v001`;
  - `source_normalized_dataset_version = v001`;
  - `source_normalized_manifest_sha256 = f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`;
  - `source_normalized_parquet_sha256 = 2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`;
  - `source_successor_state_sha256 = 8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`;
  - `source_phase_4bg_a_decision = "Option B / Decision form 2"`;
  - `source_phase_4bg_b_outcome = "Outcome 1 — Record successor state now"`;
- `invalid_windows` (propagated from source);
- `governance_labels` including:
  - `feature_computation = "allowed_by_successor_phase"` only if a future Phase 4bh is separately authorized; otherwise `"forbidden"`;
  - `labels = "forbidden"`;
  - `ml = "forbidden"`;
  - `strategy = "forbidden"`;
  - `backtest = "forbidden"`;
  - `stop_trigger_domain = "trade_price_backtest_candidate"` (preserved from Phase 4bd derived manifest);
  - `phase_id = "4bh"` (for the future implementation);
- `research_eligible = false` by default until a later feature-family eligibility gate;
- `eligibility_gate_status = pending` by default;
- `code_commit_sha` of the future Phase 4bh implementation;
- `capture_config_hash` (or feature-config equivalent);
- per-file entries with SHA256;
- `created_at_unix_ms`;
- the Phase 4aw `flip_research_eligible(...)` always-raises invariant must be preserved (Phase 4bd `MicrostructureManifest` must be the manifest type used).

---

## 23. Validation gate policy

Any future Phase 4bh feature implementation phase must be followed in order by:

1. **Phase 4bi-A — Feature Artefact Structural QA Memo** (analysis-and-docs; the feature-family equivalent of Phase 4be);
2. **Phase 4bi-B — Feature-Family Eligibility-Gate Design + Implementation + Execution** (the feature-family equivalent of Phase 4bf-A / Phase 4bf);
3. **Phase 4bi-C — Feature-Family Research-Eligibility Decision Memo** (the feature-family equivalent of Phase 4bg-A);
4. **Phase 4bi-D — Feature-Family Successor-State Recording** (the feature-family equivalent of Phase 4bg-B), if a research-eligibility decision authorizes it.

Phase 4bh-A does **not** collapse these later gates. Each transition through Feature Stage-3 / Stage-4 / Stage-5 requires its own separately authorized phase.

---

## 24. Test plan for a future Phase 4bh

The future Phase 4bh implementation phase must include, at minimum:

- per-feature unit tests covering: trailing-window correctness, leakage absence, NaN policy, invalid-window propagation, type stability, deterministic ordering;
- a per-feature golden-fixture test on a small synthetic input that exercises edge cases (single event, all-buyer-maker, all-seller-maker, mixed, invalid window, window-with-no-events);
- a one-symbol/one-day end-to-end run on the existing Phase 4bd / Phase 4be / Phase 4bf-passed normalized artefact (BTCUSDT 2025-01-15) producing a gitignored feature Parquet + manifest + sidecars under `data/microstructure/features/...`;
- a static no-network / no-credential / no-MCP / no-Graphify import-boundary test extending the existing `test_import_boundaries.py` to feature modules;
- a static no-overwrite test;
- a static schema-equality test that asserts the feature column set matches a module-level constant (`FEATURE_SCHEMA_V001`);
- whole-repo `ruff check .` clean;
- whole-repo `mypy src/prometheus` strict clean;
- whole-repo `pytest` clean except for the same pre-existing `KeyError: 'trade_count'` simulation failures.

---

## 25. M0 admissibility boundary

- Phase 4bh-A does **not** create a strategy hypothesis.
- Microstructure / order-flow / liquidity-timing remains a **cooled-down lane** and **NOT_RECOMMENDED_NOW** under Phase 4ak adoption unless a future M0 memo separately satisfies the twelve-clause M0 gate (with explicit M0.7 edge-rate plausibility, M0.10 forbidden-rescue check, and post-null cooldown re-evaluation).
- Feature design is **data infrastructure**, not strategy rescue.
- No retained verdict (R3 / R2 / F1 / D1-A / V2 / G1 / C1) may be revised by these features.
- §11.6 = 8 bps per side and §1.7.3 = 0.25% / 2× / one-position / mark-price stops remain binding.
- Any future strategy that ever consumes microstructure-derived features must independently satisfy the Phase 4ak M0 admissibility gate, the post-null cooldown rule, the Phase 4al refined no-rescue rule, and the Phase 4m 18-requirement fresh-hypothesis validity gate.

---

## 26. Cooled-down lane boundary

Phase 4bh-A does not reopen any cooled-down family. The following lanes remain cooled down per Phase 4ak adoption:

- price-only single-symbol directional continuation;
- cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors;
- derivatives-context directional lane;
- microstructure / order-flow / liquidity-timing lane;
- mark-price stop-domain / execution-realism lane.

Phase 4bh-A neither reopens nor amends any cooled-down family classification. Feature work is permitted as data infrastructure; any future strategy lane that consumes these features must independently clear M0.

---

## 27. ML / strategy / backtest boundary

Phase 4bh-A does **not** authorize:

- creating ML models;
- training ML on the normalized derived family or any future feature family;
- creating any strategy candidate (named or otherwise);
- creating any hypothesis-spec memo, strategy-spec memo, backtest-plan memo, or backtest-execution phase that consumes this dataset or any future feature dataset;
- running any backtest;
- running any simulation that uses this dataset or any future feature dataset as input;
- running any paper / shadow / live / exchange-write workflow.

---

## 28. Acquisition boundary

Phase 4bh-A does **not** authorize:

- acquiring additional aggTrades data (more days, more symbols);
- acquiring 5m, 1m, tick, mark-price 30m / 4h, order-book, funding, OI, or cross-venue data;
- acquiring metrics OI beyond the Phase 4j §11 governed subset;
- acquiring spot, COIN-M, options, or any other market type;
- acquiring any data via authenticated REST, private endpoints, public-endpoint code calls, user stream, WebSocket, listenKey lifecycle, MCP, Graphify, `.mcp.json`, or credentials.

---

## 29. Acceptance criteria for future Phase 4bh

A future Phase 4bh implementation phase, if separately authorized, must satisfy at minimum:

1. implements only the feature subset explicitly approved by Phase 4bh-A (this memo) and / or by a future Phase 4bh-B schema-finalization memo;
2. respects the canonical input (§8) and forbidden inputs (§9);
3. respects the temporal-leakage boundary (§15);
4. respects the windowing policy (§16);
5. respects the timestamp alignment policy (§17);
6. respects the aggregation policy (§18);
7. respects the precision / type policy (§19);
8. respects the missing / invalid-window policy (§20);
9. respects the output dataset policy (§21);
10. respects the manifest policy (§22);
11. respects the test plan (§24);
12. runs as a standalone phase with no `prometheus.runtime` / `prometheus.execution` / `prometheus.persistence` imports, no exchange adapters, no `requests/httpx/aiohttp/websockets/urllib`, no `.env` reads, no credentials, no Binance API, and no network I/O;
13. does not create labels, signals, ML models, strategies, or backtests;
14. does not flip `research_eligible` on any actual manifest, including the future feature manifest (which must default to `research_eligible=false / eligibility_gate_status=pending`);
15. preserves the Phase 4aw `flip_research_eligible(...)` always-raises invariant on every manifest;
16. does not modify any prior tracked file outside the four new feature modules (TBD by Phase 4bh-B or Phase 4bh) plus narrow `__init__.py` re-exports plus new test files plus new docs;
17. does not commit anything under `data/microstructure/`;
18. produces local gitignored output only;
19. is followed by a separately authorized Phase 4bi-A structural QA memo;
20. preserves every retained verdict and project lock verbatim.

---

## 30. Fail-closed rules

The following are binding on any future phase that consumes Phase 4bh-A as input:

1. **Path discipline.** No write may occur outside `data/microstructure/`. The Phase 4bd normalized Parquet path, the Phase 4bd derived manifest path, the Phase 4bf gate report path, and the Phase 4bg-B successor-state path must remain byte-immutable.
2. **Manifest-mutation discipline.** The original Phase 4bd derived manifest must not be mutated. Any future feature manifest is a new sibling artefact at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json`, never a replacement of the normalized derived manifest.
3. **Raw-family discipline.** The raw family `microstructure_raw_aggtrades_v001` remains `research_eligible=false` permanently. No phase consuming Phase 4bh-A may flip it.
4. **Successor-state discipline.** The Phase 4bg-B successor-state JSON must be cited by SHA in any future feature manifest. The original derived manifest alone is not a Stage-3 marker.
5. **Stage-3 discipline.** Stage-3 admissibility at policy / successor-state level is *not* a license for feature computation, ML, strategy, or backtests. A future Phase 4bh implementation requires its own authorization.
6. **Stage-4 discipline.** Stage-4 (feature-cleared) is not implied by Stage-3. A separately authorized feature-family eligibility gate is required.
7. **Network discipline.** No phase consuming Phase 4bh-A may call public endpoints, Binance APIs, authenticated REST, private endpoints, user stream, WebSocket, or read `.env` / credentials / `.mcp.json`.
8. **Static-import discipline.** The Phase 4bf static-scan policy on `derived_gate_*` modules continues. Future feature modules must remain free of forbidden imports (`prometheus.runtime`, `prometheus.execution`, `prometheus.persistence`, `requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`, `python_dotenv`, `os.environ`, `getenv`).
9. **Cooldown discipline.** Cooled-down family classifications are not loosened by Phase 4bh-A.
10. **Cost-realism discipline.** §11.6 = 8 bps per side and round-trip = 16 bps remain binding for any future strategy candidate that ever consumes microstructure-derived features.
11. **No-rescue discipline.** Phase 4al refined no-rescue rule remains binding. No retained verdict (R3 / R2 / F1 / D1-A / V2 / G1 / C1) may be revisited, rescued, or relabelled on the basis of Phase 4bh-A.
12. **Label / signal / ML discipline.** No future phase consuming Phase 4bh-A may create labels, signals, ML, strategies, or backtests without separate authorization beyond Phase 4bh.

---

## 31. What this phase proves

- that the project record contains a complete feature-boundary design for a future feature-implementation phase on the Stage-3 successor-state-normalized aggTrades family;
- that the canonical input, forbidden inputs, feature-stage model, leakage / windowing / aggregation / precision / type / missing-window policies, output / manifest schemas, validation gate sequence, and acceptance criteria are predeclared *before* any feature implementation exists;
- that the original derived manifest, the original raw manifest, the normalized Parquet, and the Phase 4bb-D / Phase 4bf gate reports remain byte-immutable;
- that the Phase 4bg-B successor-state record is cited as the only Stage-3 marker for the derived family;
- that Phase 4bh-A reaches Feature Stage-0 design only and does not authorize any successor.

---

## 32. What this phase does not prove

- that any feature is statistically meaningful for any specific research question;
- that any future Phase 4bh implementation will produce a Stage-2 feature artefact that passes structural QA;
- that any feature-family eligibility gate will pass;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible.

---

## 33. Preserved boundaries

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B results — all preserved.

---

## 34. Recommended future options

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | docs-only / no work | recommended |
| **Conditional next, if continuing** — Phase 4bh-B AggTrades Feature Schema Finalization Memo | docs-only | NOT authorized by this memo |
| **Conditional direct implementation** — Phase 4bh AggTrades Feature Schema / Feature Computation Implementation | code + docs + local gitignored feature artefacts only | NOT authorized by this memo |
| **Conditional after feature implementation** — Phase 4bi-A Feature Artefact Structural QA Memo | analysis + docs | NOT authorized by this memo |
| **Conditional cleanup** — Phase 4bb-F Gate Report Output Path Hygiene | code + docs; before any repeated raw gate execution | NOT authorized by this memo |
| **Conditional raw policy marker** — Phase 4bb-G Raw Manifest Successor-State Recording | docs-only or docs-and-local-gitignored-output | NOT authorized by this memo |
| Acquisition (additional days / symbols / data families) | docs + data | NOT authorized; not in scope |
| Feature computation, ML, strategy, backtests | code + data | FORBIDDEN by Phase 4bh-A |
| Paper / shadow / live / exchange-write / production keys | runtime | FORBIDDEN |

---

## 35. Closeout / lock preservation

Phase 4bh-A is docs-only and produces:

- this memo (`docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_aggtrades-feature-boundary-design.md`);
- the Phase 4bh-A closeout (`docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_closeout.md`);
- a narrow Phase 4bh-A paragraph + new "Current phase:" block in `docs/00-meta/current-project-state.md` (prior Phase 4bg-B block preserved as historical context).

No source code, tests, scripts, configs, READMEs, MCP files, runtime configuration, manifests, raw artefacts, gate reports, successor-state artefacts, or `.gitignore` entries were modified.

The `data/microstructure/` namespace is untouched. The Phase 4bd derived manifest, the normalized Parquet, the raw manifest, the raw zip, the raw sidecar, the acquisition log, the Phase 4bb-D gate report, the Phase 4bf gate report, and the Phase 4bg-B successor-state JSON all remain byte-identical.

The recorded outcome is: feature-boundary design complete at policy level. Feature Stage-0 reached for `microstructure_features_aggtrades_v001` (proposed name; not created). Original derived manifest remains `research_eligible=false / eligibility_gate_status=pending`. Raw family remains permanently `research_eligible=false`. Feature computation, ML, strategy, backtests, and acquisition all remain unauthorized. No successor phase is authorized by Phase 4bh-A.

**Recommended state: remain paused.**
