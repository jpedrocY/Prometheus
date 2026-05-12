# Phase 4bj-K — Label Diagnostic Study Plan

**Phase identity:** Phase 4bj-K — Label Diagnostic Study Plan (docs-only).
**Date:** 2026-05-12.
**Phase type:** docs-only design / governance memo.
**Branch:** `phase-4bj-k/label-diagnostic-study-plan`.
**Base:** `main` at `13dac8ffb611ec14a728f99f98f85dd47ccda76c` (Phase 4bj-J SHA-chain-fixup commit on top of the Phase 4bj-J merge-closeout `5e5fc401d0776c7e86a4e0e0677cce87789b67b5`).
**Status:** drafted; pending operator review.

A note on the SHA-chain pattern: the Phase 4bj-J merge-closeout itself anchored its §2 final-`main` value at the merge-closeout commit `5e5fc40`. The one-commit fixup on top of that anchor (commit `13dac8f`) only records the final-`main` SHA back into §2 of the Phase 4bj-J merge-closeout; it does not change Phase 4bj-J lifecycle semantics. Phase 4bj-K branches from `13dac8f` because that is the post-fixup `main` state; the canonical "Phase 4bj-J project-complete" anchor remains the merge-closeout commit (`5e5fc40`).

---

## 1. Phase identity

- **Phase name:** Phase 4bj-K — Label Diagnostic Study Plan.
- **Phase type:** docs-only design / governance memo.
- **Branch:** `phase-4bj-k/label-diagnostic-study-plan`.
- **Base SHA:** `main` at `13dac8ffb611ec14a728f99f98f85dd47ccda76c`.
- **Predecessor anchor:** Phase 4bj-J merge-closeout `5e5fc401d0776c7e86a4e0e0677cce87789b67b5` (project-complete).
- **Authorization:** explicit operator authorization for Phase 4bj-K only.

Phase 4bj-K is **strictly docs-only**. It does **not**:

- run any diagnostic;
- compute any label statistic;
- read or process the label parquet beyond documentation-level reference already recorded in Phase 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-G / 4bj-H / 4bj-I / 4bj-J;
- create any diagnostic output;
- create train / validation / test partitions of any kind;
- create within-day descriptive segmentation artefacts;
- create split artefacts of any kind;
- create or modify any manifest, gate report, sidecar, parquet, raw zip, or successor-state artefact under `data/microstructure/`;
- rerun any eligibility gate;
- run any kernel, normalizer, or processing script;
- modify any source code, test, script, `pyproject.toml`, `README.md`, `.gitignore`, or MCP file;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any actual manifest (the label manifest's `chronological_split_policy` remains `"not_yet_defined"`);
- train ML, design ML architecture, rank features, or create meta-labeling;
- create a strategy, compute signals, or run backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output;
- acquire data of any kind (order-book, mark-price, spot, cross-venue, funding, open-interest, additional aggTrades, 5m / 1m / tick);
- call public, authenticated, or private endpoints;
- open WebSockets or user streams;
- create or read credentials, `.env`, or `.mcp.json`;
- enable MCP or Graphify;
- modify project locks, retained verdicts, or M0 governance;
- authorize Phase 4bj-L (label diagnostic study execution), any Phase 4bj-M / 4bj-N / 4bj-* successor, Phase 4 canonical, Phase 5, or any successor phase.

Tracked changes by Phase 4bj-K are exactly three new docs (this memo + the Phase 4bj-K closeout + narrow paragraph + "Current phase:" block update in `docs/00-meta/current-project-state.md`). No `data/microstructure/` artefact, no local gitignored file, no source / test / script / config file is created or modified.

---

## 2. Pre-state and evidence boundary

### 2.1 Phase 4bj-H label-evaluation boundary

Phase 4bj-H (project-complete at merge-closeout `65e9094`) recorded the **label-evaluation / chronological split boundary** at policy level. Label evaluation is a future controlled diagnostic activity, never a strategy or signal. No empirical label evaluation may run before a chronological split policy is recorded as a sibling artefact. Phase 4bj-H named Phase 4bj-I as the cleanest successor and did not authorize it.

### 2.2 Phase 4bj-I Option D no-formal-split policy

Phase 4bj-I (project-complete at merge-closeout `8f920e0`) recorded the **Option D recommended policy**: the single-day BTCUSDT 2025-01-15 label cell is insufficient for formal train / validation / test partitioning and must remain unsplit until multi-day data exists. Train / validation / test vocabulary is forbidden for the single-day cell. Future descriptive within-day segmentation (if ever authorized) must use neutral vocabulary, must remain descriptive-only, and must adopt a uniform 60s purge / embargo policy.

### 2.3 Phase 4bj-J no-split determination artefact

Phase 4bj-J (project-complete at merge-closeout `5e5fc40`) operationalized the Phase 4bj-I Option D decision into exactly one machine-readable sibling no-split determination JSON at `data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json` (14,236 bytes; SHA256 `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`; paired `.sha256` sidecar 141 bytes; sidecar SHA256 `9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8`; gitignored / not committed). The original label manifest remains byte-identical and the `chronological_split_policy` field on the manifest remains `"not_yet_defined"`.

### 2.4 Label-family state (preserved unchanged by Phase 4bj-K)

| Field | Value |
| --- | --- |
| Family | `microstructure_labels_aggtrades_v001` |
| Symbol | `BTCUSDT` |
| Date | `2025-01-15` (single UTC day) |
| Row count | `1,681,098` |
| Column count | `39` |
| Horizons | `["1s", "5s", "15s", "60s"]` |
| Horizon seconds | `[1, 5, 15, 60]` |
| `invalid_price_row_count` | `0` |
| `censored_per_horizon` | `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` |
| Label parquet SHA256 | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label parquet sidecar SHA256 | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` |
| Label manifest SHA256 | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| Label manifest sidecar SHA256 | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` |
| `label_config_hash` | `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00` |
| `research_eligible` | `false` (unchanged) |
| `eligibility_gate_status` | `"pending"` (unchanged) |
| `chronological_split_policy` | `"not_yet_defined"` (unchanged) |
| Phase 4bj-E label-family gate report SHA256 | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` (PASS; 72/72) |
| Phase 4bj-G label-family successor-state JSON SHA256 | `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5` |
| Phase 4bj-J no-split determination JSON SHA256 | `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6` |

### 2.5 What has not happened

- No empirical label evaluation has been run.
- No label statistics have been computed beyond the documentation-level summary values already recorded in the prior phases.
- No split / segmentation artefact exists on disk (the Phase 4bj-J sibling artefact is a no-split determination, not a split artefact).
- No diagnostic artefact exists.
- No ML, strategy, signal, backtest, acquisition, paper / shadow, or live work has been authorized at any point.
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).

---

## 3. Study-plan purpose

Phase 4bj-K is a **predeclared diagnostic plan only**. It is not execution.

The plan exists so that any future Phase 4bj-L-equivalent label diagnostic execution phase, if separately authorized, can run from a precise, reviewable, fail-closed contract rather than from ad-hoc choices made at execution time. Predeclaration is the central anti-overfitting discipline of the Prometheus research arc (Phase 4ak M0 §6 / §7; Phase 4k / 4q / 4w; Phase 4ay §10).

The plan asserts:

- **The plan is not execution.** Phase 4bj-K must not compute anything against the label parquet. It must not produce diagnostic artefacts.
- **Diagnostics are descriptive only.** Any future Phase 4bj-L outputs must be labelled "single-day descriptive diagnostics only" and must not be interpreted as predictive / generalisation evidence.
- **Diagnostics may characterize the one-day cell only.** The current research cell is BTCUSDT / 2025-01-15 / 1,681,098 rows / 4 horizons / 0 invalid-price rows / 676 censored rows total. Diagnostics describe this cell.
- **Diagnostics cannot imply generalisation.** Out-of-sample claims require multi-day data plus separately authorized split / acquisition phases. None of those exist.
- **Diagnostics cannot become ML, strategy, signals, or backtests.** No diagnostic result can short-cut M0 (Phase 4ak twelve-clause gate), the post-null cooldown rule (Phase 4ak §7), the Phase 4al no-rescue rule, or any retained verdict.
- **Any future execution requires a separate Phase 4bj-L-equivalent authorization.** Phase 4bj-K does not authorize execution.

---

## 4. Allowed future diagnostic categories

If a future Phase 4bj-L-equivalent is separately authorized, the following descriptive diagnostic categories are allowed. The list is exhaustive for the locked one-day cell; categories not enumerated below are not authorized.

### 4.1 Label schema / column-presence confirmation

Verify that the on-disk label parquet has the expected 39 columns, in the expected canonical order, with the expected dtypes, matching the Phase 4bj-C label schema. Verify the presence of every per-horizon column (`forward_log_return_*`, `forward_direction_*`, `reference_row_index_*`, `reference_timestamp_ms_*`, `horizon_censored_flag_*`), the two global flags (`label_invalid_price_flag`, `label_any_censored_flag`), the 16 lineage / identity / metadata columns, and the `label_config_hash` column. Verify the on-disk SHA256 matches the recorded label parquet SHA `ef50038a...e8d26`.

### 4.2 Row-count / row-order confirmation

Confirm `row_count = 1,681,098` exactly. Confirm `row_index` is contiguous `0..1,681,097` with no duplicates and no gaps. Confirm row ordering matches the source aggTrades ordering by `(transact_time_ms ASC, row_index ASC)`.

### 4.3 Per-horizon non-null / censored / valid count table

Per horizon, count:

- total rows (must equal 1,681,098);
- rows with `horizon_censored_flag_H = true` (must equal the recorded `censored_per_horizon[H]`);
- rows with `forward_log_return_H` null;
- rows with `forward_direction_H` null;
- rows with `reference_row_index_H` null;
- rows valid for label diagnostics (i.e., not censored, not invalid-price, label fields non-null).

### 4.4 Per-horizon forward return descriptive statistics

Per horizon, on the valid-for-label-diagnostics subset:

- count;
- mean (descriptive only; explicitly NOT an expected-return claim);
- standard deviation (descriptive only);
- min, max, p1, p5, p25, p50, p75, p95, p99 (descriptive distribution shape);
- skewness, kurtosis (descriptive only);
- fraction of non-finite values (must be 0).

These statistics characterize the one-day cell only. They are **not** predictive expectations; they are **not** signal evidence.

### 4.5 Per-horizon direction class balance

Per horizon, on the valid-for-label-diagnostics subset, count `forward_direction_H ∈ {-1, 0, +1}`. Report fractions. Report the strict-sign threshold (0.0) per Phase 4bj-B / 4bj-C.

### 4.6 Per-horizon zero / flat-rate review

Per horizon, count `forward_log_return_H == 0.0` (exact equality). Report the fraction. This is descriptive only; it characterizes microstructure flat-quote behavior in the single-day cell.

### 4.7 Censoring location review

Identify which `row_index` values are censored per horizon. Confirm that censoring concentrates at the right edge of the UTC day (rows whose forward window extends beyond the last source `transact_time_ms`). Confirm that the censored row sets nest: 1s ⊆ 5s ⊆ 15s ⊆ 60s (longer horizons must censor at least as many right-edge rows as shorter horizons). Report any violation as a stop condition.

### 4.8 Right-edge row review

Examine the last `max_forward_horizon_seconds = 60` worth of rows. Confirm they are correctly censored on the relevant horizons. Report no-action-required if the censoring nest is consistent.

### 4.9 Timestamp monotonicity and uniqueness checks

Confirm `source_transact_time_ms` is non-decreasing across `row_index`. Confirm `feature_timestamp_ms == source_transact_time_ms` for every row. Confirm `agg_trade_id` is non-decreasing across `row_index`. Confirm no two rows share the same `(agg_trade_id, row_index)` tuple.

### 4.10 Feature-label row-index alignment check

Confirm that the label parquet row-index range exactly matches the feature parquet row-index range. Verify by recomputing the feature parquet SHA `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` and the label parquet SHA. Cross-reference `row_count` from each manifest. No spot-row reading is required at this layer; the row-count and SHA matches are sufficient.

### 4.11 Feature-label timestamp alignment check

For a small predeclared set of row_index sentinels (e.g. row 0, row 100, row 1000, row 100,000, row 1,000,000, row 1,681,097), confirm the label parquet's `feature_timestamp_ms` matches the feature parquet's `feature_timestamp_ms` for the same row. The sentinel list must be predeclared in the Phase 4bj-L execution plan; it must not be expanded ad-hoc during execution.

### 4.12 Horizon-overlap leakage audit

Confirm that label horizons {1s, 5s, 15s, 60s} are forward-only and do not draw from rows before the anchor. Confirm the per-row reference-row-index / reference-timestamp policy is consistent with Phase 4bj-B § "Future-reference policy" (closest source aggTrade row at or after `T + H_ms`, censored if `T + H_ms` exceeds the last source `transact_time_ms` for the UTC day). Confirm no row uses `reference_row_index_H < row_index` for any horizon.

### 4.13 Documentation-only comparison against manifest summary values

Confirm that the recomputed per-horizon censored counts exactly match the recorded `censored_per_horizon` in the label manifest (`{"1s": 9, "5s": 42, "15s": 118, "60s": 507}`). Confirm that `invalid_price_row_count = 0` matches the recomputed value. Confirm that `label_config_hash` recomputed from the source schema matches the recorded `label_config_hash`.

### 4.14 Descriptive within-cell temporal stability check (conditional)

Only allowed **if** neutral segmentation is separately authorized in a future Phase 4bj-J-style segmentation-policy memo and a future Phase 4bj-J-style sibling segmentation artefact is recorded. In that conditional case, compute the same descriptive statistics (§4.4, §4.5, §4.6) per neutral segment (e.g. `fixture-A` / `fixture-B` / `fixture-C` or `early-day` / `mid-day` / `late-day`) and compare descriptively. No segment may be labelled `train` / `validation` / `test` / `calibration` / `holdout`. No segment may be used to fit, score, or rank a model. No segment may be used as a holdout.

### 4.15 Optional naive descriptive baselines (conditional)

Only allowed **if** separately authorized. Naive baselines (e.g. "fraction of rows where `forward_direction_60s = +1`", "mean unconditional `forward_log_return_60s`") may be computed on the valid-for-label-diagnostics subset as **descriptive context only**, and must be labelled "naive descriptive baselines; not signals; not strategy; not predictive expectations". They must not be used to predict, rank, or select. They must not be cost-adjusted. They must not be combined with feature columns to form decision rules. They must not be presented as edge claims.

---

## 5. Forbidden diagnostics and outputs

The following are explicitly forbidden in any future Phase 4bj-L-equivalent execution phase. They are not authorized by Phase 4bj-K, by any predecessor phase, by any project lock, or by any retained verdict.

- **Train / validation / test diagnostics.** Single-day cell cannot support generalisation evidence; partition vocabulary is banned by Phase 4bj-I §4 and Phase 4bj-J non-authorizations.
- **Model fitting, model scoring, model selection.** Fitting an ML model on the locked cell would convert descriptive diagnostics into strategy evidence and bypass M0 (Phase 4ak twelve-clause gate).
- **Feature ranking, feature importance.** Same M0 bypass; also risks cross-family rescue.
- **Label-to-signal conversion.** Labels remain not signals. No diagnostic output may be used to derive an entry / exit rule.
- **Threshold search, hyperparameter search.** Including direction-threshold sweeps, horizon selection by performance, or grid search on label transformations.
- **Strategy rules, entry / exit logic.** Strategy creation requires M0 admission plus separate authorization.
- **PnL, MFE, MAE, R-multiple, equity curves, position simulation.** These are strategy / backtest outputs, not label diagnostics.
- **Alpha / edge claims.** Diagnostics describe the locked cell; they cannot establish edge.
- **Backtests.** No backtest may be run as part of label diagnostics.
- **Paper / shadow / live-readiness claims.** Diagnostics never establish live-readiness.
- **Acquisition recommendations based only on diagnostics.** A future multi-day acquisition path requires its own data-requirements memo, its own acquisition phase, and its own integrity-gate phase. Label diagnostics on a one-day cell cannot bypass that path.
- **Any result that reopens an old failed strategy family.** R2 / F1 / D1-A / V2 / G1 / C1 first-spec hard rejects remain terminal. No diagnostic finding rescues them. The 5m thread remains operationally closed (Phase 3t).

---

## 6. Per-horizon exclusion and censoring rules

Future Phase 4bj-L execution must respect the following per-horizon handling rules.

### 6.1 Locked horizon set

Horizons: `["1s", "5s", "15s", "60s"]`. Seconds: `[1, 5, 15, 60]`. No additional horizons are authorized. 30s / 5m / 30m / 1h / 4h / longer-horizon label generation is explicitly forbidden by Phase 4bj-J §10 and remains forbidden.

### 6.2 Censoring counts (locked)

`censored_per_horizon = {"1s": 9, "5s": 42, "15s": 118, "60s": 507}`. These are the recorded counts in the label manifest. Phase 4bj-L must recompute these counts and stop the run if any value differs.

### 6.3 Per-horizon exclusion of censored labels

For per-horizon label statistics (§4.4, §4.5, §4.6), exclude rows where `horizon_censored_flag_H = true`. Report exclusion counts per horizon. Do not silently drop rows.

### 6.4 Retaining censored rows for non-label diagnostics

Censored rows are retained for non-label diagnostics (e.g. schema confirmation §4.1, row-count confirmation §4.2, timestamp monotonicity §4.9, feature-label alignment §4.10–§4.11, horizon-overlap leakage audit §4.12). Censoring is a per-horizon condition, not a row-level exclusion.

### 6.5 Reporting excluded row counts per horizon

Every per-horizon diagnostic output must include the per-horizon excluded row count, the per-horizon valid-for-label-diagnostics row count, and the resulting total used for the statistic.

### 6.6 Right-edge censoring

Censoring concentrates at the right edge of the UTC day. Phase 4bj-L must audit the right-edge censoring nest (§4.7, §4.8) and report any violation.

### 6.7 Invalid-price rows

`invalid_price_row_count = 0` for the current cell. Phase 4bj-L must recompute this count and stop the run if any row has `label_invalid_price_flag = true`.

### 6.8 No silent row dropping

Any row excluded from a diagnostic must be reported. The fraction of valid-for-label-diagnostics rows per horizon must be reported alongside the diagnostic statistic.

---

## 7. No-split / no-segmentation execution mode

Because Phase 4bj-J recorded the Option D no-split determination, the **default execution mode** for any future Phase 4bj-L is:

- no train / validation / test partitions;
- no `early-day` / `mid-day` / `late-day` segmentation;
- no `fixture-A` / `fixture-B` / `fixture-C` segmentation;
- diagnostics run on the **full single-day cell** only, with per-horizon censoring exclusions applied per §6;
- every output must carry an explicit `"single_day_descriptive_diagnostics_only": true` flag;
- every output must carry `"no_generalization_interpretation": true`;
- no interpretation of within-cell variation as out-of-sample evidence;
- no comparison to a different day, symbol, or regime (no such data exists in the current arc).

Future Phase 4bj-L authorization is conditional on adopting this default execution mode unless a separately authorized neutral segmentation memo (§8) and a separately authorized segmentation artefact phase have both been completed first.

---

## 8. Optional future neutral segmentation gate

If a future operator wants descriptive within-day segmentation **before** running Phase 4bj-L diagnostics, the following conditions apply. They are not authorized by Phase 4bj-K.

- **Separate authorization.** A separately authorized future memo (e.g. Phase 4bj-J-B "Neutral Within-Day Segmentation Policy Memo") must predeclare the segmentation rules before any segmentation artefact is recorded.
- **Neutral vocabulary only.** The segments must use neutral names from the Phase 4bj-J locked vocabulary list (`fixture-A`, `fixture-B`, `fixture-C`, `early-day`, `mid-day`, `late-day`) or an equivalent set approved by the segmentation memo. The forbidden vocabulary list (`train`, `validation`, `test`, `calibration`, `holdout`) remains forbidden.
- **No train / validation / test language.** Any document, code path, or output that uses the forbidden vocabulary in the context of the locked single-day cell fails closed.
- **Uniform 60s purge / embargo.** Phase 4bj-I §5 / §6 locked a uniform 60s purge / embargo policy because 60s is the maximum forward label horizon. Future segmentation must adopt this policy unconditionally.
- **Boundary-overlap masks.** Rows whose forward 60s window crosses a segment boundary must be masked as boundary-overlap and excluded from per-segment diagnostics.
- **Segmentation artefact as sibling gitignored JSON.** Following the Phase 4bg-B / 4bi-D / 4bj-G / 4bj-J precedent, any segmentation must be recorded as a sibling JSON under the canonical Phase 4bb-F `data/microstructure/successor-state/` namespace (or an equivalent canonical namespace if Phase 4bb-F is extended) with a paired `.sha256` sidecar. The original label manifest must remain byte-identical; `chronological_split_policy` on the original manifest must remain `"not_yet_defined"`.
- **No ML / strategy / backtest permission.** A segmentation artefact does not authorize ML, strategy, or backtests. It only authorizes per-segment descriptive diagnostics under the §4.14 / §4.15 conditional categories.
- **No segment treated as holdout / validation / test.** Even under neutral vocabulary, no segment may be used as a holdout, validation, or test partition. No model may be fit on one segment and scored on another.

---

## 9. Leakage-check requirements

Any future Phase 4bj-L execution must run and report the following leakage checks **before** interpreting any diagnostic statistic. Failure of any check is a Phase 4bj-L stop condition (§12).

- **Label timestamp not before feature timestamp.** For every row, `label.feature_timestamp_ms == feature.feature_timestamp_ms` (label is anchored at the feature's source timestamp; no label rows reference timestamps earlier than the anchor).
- **Feature rows do not use future information.** Confirmed at feature construction time (Phase 4bh §6.1 trailing-window rule with same-timestamp tie-break by `row_index ASC`). Phase 4bj-L must verify that the feature parquet SHA matches the recorded value `618d9b86...4c1691f`; no recomputation of features is authorized.
- **Feature-label row counts match.** Both parquets must have `row_count = 1,681,098`.
- **Feature-label row indexes align.** Per §4.10, the `row_index` range must match exactly. Phase 4bj-L must verify via SHA + row-count consistency; no per-row joining is required at this layer.
- **Feature-label timestamps align.** Per §4.11, on the predeclared sentinel set, label and feature `feature_timestamp_ms` must match exactly.
- **Horizon windows do not create cross-boundary leakage if segmentation is used.** Per §8 uniform 60s purge / embargo + boundary-overlap masks.
- **Censored rows are not treated as valid labels.** Per §6.3 / §6.8 per-horizon exclusion.
- **Right-edge rows are explicitly audited.** Per §4.8.
- **No random split used.** Random splits are forbidden under Phase 4bj-I §5 and Phase 4bj-J §6 (no random split allowed).
- **No train / validation / test terminology used.** Per Phase 4bj-J §6 forbidden segmentation vocabulary.

---

## 10. Future output artefact plan

Phase 4bj-K predeclares the future output paths and conventions. Phase 4bj-K does not create any output.

### 10.1 Suggested future diagnostic root

```text
data/microstructure/diagnostics/labels/
```

This namespace is currently empty. Any future Phase 4bj-L execution would create files only under this root and its subdirectories. The `data/microstructure/diagnostics/` parent is gitignored under `.gitignore:85: data/microstructure/`.

### 10.2 Suggested future diagnostic report filename pattern

```text
microstructure_labels_aggtrades_v001__v001__label_diagnostics__phase-4bj-l.json
```

This follows the Phase 4bb-F canonical filename pattern `<dataset_family>__<dataset_version>__<stage_marker>__phase-<phase_id>.json`, with `stage_marker = label_diagnostics` and `phase_id = 4bj-l`. The exact filename must be locked by the Phase 4bj-L authorization brief.

### 10.3 Required paired sidecar

A future Phase 4bj-L execution must produce exactly one paired `.sha256` sidecar at the same path + `.sha256` suffix. Sidecar body must follow the canonical Phase 4bb-F format `<json_sha256_hex>  <basename>\n` (two spaces; trailing newline; `sha256sum`-compatible). The sidecar must be written via `prometheus.research.microstructure.canonical_paths.write_paired_sha256_sidecar(...)` with `refuse_overwrite=True`.

### 10.4 Gitignored output only

Both the diagnostic JSON and the paired sidecar must be gitignored output only; neither may be committed.

### 10.5 Deterministic JSON

The diagnostic JSON must be serialized deterministically: sorted keys, `indent=2`, `ensure_ascii=False`, single trailing newline. This matches the Phase 4bb-G / 4bg-B / 4bi-D / 4bj-G / 4bj-J precedent.

### 10.6 Source artefact paths and SHAs embedded

Every diagnostic JSON must embed the full source artefact lineage (label parquet path + SHA, label manifest path + SHA, feature parquet path + SHA, feature manifest path + SHA, Phase 4bj-E gate report path + SHA, Phase 4bj-G successor-state path + SHA, Phase 4bj-J no-split determination path + SHA, `label_config_hash`, `code_commit_sha`).

### 10.7 No manifest mutation

The original label manifest must remain byte-identical. The label manifest's `chronological_split_policy` must remain `"not_yet_defined"`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant must be preserved.

### 10.8 No committed data/microstructure output

No `data/microstructure/` artefact may be committed by Phase 4bj-L. The diagnostic JSON and sidecar are local gitignored output only.

### 10.9 Clear descriptive-only flags

Every diagnostic JSON must carry explicit flags: `single_day_descriptive_diagnostics_only=true`, `no_generalization_interpretation=true`, `not_a_signal=true`, `not_a_strategy=true`, `not_an_edge_claim=true`.

### 10.10 Non-authorizations embedded

Every diagnostic JSON must enumerate the same non-authorization booleans recorded in the Phase 4bj-J no-split determination JSON (`ml_training_authorized=false`, `strategy_authorized=false`, `backtest_authorized=false`, `acquisition_authorized=false`, `paper_shadow_authorized=false`, `live_readiness_authorized=false`, `deployment_authorized=false`, `exchange_write_authorized=false`, and all sub-categories).

---

## 11. Future diagnostic result schema

A future Phase 4bj-L diagnostic JSON must include, at minimum, the following keys (alphabetised here for reviewability; serialised with sorted keys at execution time):

- `artefact_type`: `"label_diagnostic_result"`
- `base_commit_sha`: full 40-char SHA of the `main` commit at execution time
- `boundary_confirmations`: dict of boolean preservation confirmations matching the Phase 4bj-J pattern
- `censoring_summary`: per-horizon counts (total, censored, valid-for-label-diagnostics)
- `code_commit_sha`: full 40-char SHA of the commit recorded into the JSON at execution time
- `column_count`: `39`
- `created_at_unix_ms`: integer Unix millisecond timestamp
- `created_at_utc`: ISO-8601 UTC string (YYYY-MM-DDTHH:MM:SS.fffZ)
- `diagnostics_not_run`: list of allowed-but-not-run categories from §4 (with brief reason per item)
- `diagnostics_run`: list of categories from §4 actually executed
- `forbidden_diagnostics_attempted`: must be `[]` (empty); any non-empty value is a stop condition
- `governance_labels`: dict mirroring the Phase 4bj-J governance label block
- `horizon_seconds`: `[1, 5, 15, 60]`
- `horizons`: `["1s", "5s", "15s", "60s"]`
- `interpretation_limits`: dict capturing §13
- `label_config_hash`: `"fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00"`
- `leakage_checks`: dict of every §9 check with `pass`/`fail` and evidence
- `manifest_chronological_split_policy_after`: `"not_yet_defined"`
- `manifest_eligibility_gate_status_after`: `"pending"`
- `manifest_research_eligible_after`: `false`
- `no_split_determination_path`: path to the Phase 4bj-J no-split determination JSON
- `no_split_determination_sha256`: `"7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6"`
- `non_authorizations`: dict mirroring the Phase 4bj-J non-authorizations block
- `per_horizon_counts`: per-horizon table from §4.3
- `per_horizon_descriptive_statistics`: per-horizon distributions from §4.4 / §4.5 / §4.6
- `phase`: `"Phase 4bj-L"` (when executed)
- `phase_id`: `"4bj-L"` (when executed)
- `recommended_state`: typically `"remain_paused"` or `"author_multi_day_aggtrades_expansion_requirements_memo"` if diagnostics suggest a multi-day pivot
- `retained_verdict_ledger`: dict preserving the ledger verbatim
- `row_count`: `1681098`
- `schema_version`: `"v001"`
- `source_label_family`: `"microstructure_labels_aggtrades_v001"`
- `source_label_manifest_path`: `"data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json"`
- `source_label_manifest_sha256`: `"181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3"`
- `source_label_parquet_path`: `"data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet"`
- `source_label_parquet_sha256`: `"ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26"`
- `source_symbol`: `"BTCUSDT"`
- `source_utc_date`: `"2025-01-15"`
- `stop_conditions`: list of §12 conditions checked
- `successor_authorizes_next_phase`: `false`

A future Phase 4bj-L execution must write **exactly one** JSON at the canonical path (§10.2), with **exactly one** paired `.sha256` sidecar (§10.3). No additional artefact is permitted.

---

## 12. Stop conditions

A future Phase 4bj-L execution must fail closed on any of the following conditions. The diagnostic JSON, if any is written, must record `overall_status = "fail_closed"` with the failing condition recorded in a `stop_condition_triggered` field; no further interpretation is allowed.

- **Source SHA mismatch.** Recomputed label parquet SHA ≠ `ef50038a...e8d26`. Recomputed label manifest SHA ≠ `181a799c...e0f3`. Recomputed Phase 4bj-J no-split determination JSON SHA ≠ `7e461eb5...c4fa6`.
- **Row-count mismatch.** Recomputed label parquet row count ≠ `1,681,098`.
- **Manifest summary mismatch.** Recomputed `censored_per_horizon` ≠ `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}`. Recomputed `invalid_price_row_count` ≠ `0`. Recomputed `label_config_hash` ≠ `fe4633af...286f00`.
- **Label schema mismatch.** Column count ≠ 39; column names / order / dtypes deviate from the Phase 4bj-C locked schema.
- **Feature-label alignment failure.** Feature parquet SHA ≠ `618d9b86...4c1691f`. Feature parquet row count ≠ label parquet row count. Sentinel-row `feature_timestamp_ms` mismatch.
- **Timestamp monotonicity failure.** Any descending step in `source_transact_time_ms` across `row_index`. Any duplicate `(agg_trade_id, row_index)`.
- **Unexpected null / invalid counts.** Any label row with `label_invalid_price_flag = true`. Any non-finite value in `forward_log_return_*` outside the documented null-on-censored semantics.
- **Unexpected censoring mismatch.** Per-horizon censored count deviates from manifest summary. Censoring nest violation (e.g. 1s censored but 60s not).
- **Unapproved segmentation detected.** Any code path or input referring to `train` / `validation` / `test` / `calibration` / `holdout` partitions on the locked single-day cell.
- **Strategy / ML / signal / PnL metric attempted.** Any computation of model fit / score / threshold / hyperparameter / strategy rule / entry-exit / PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output.
- **External endpoint call attempted.** Any call to `requests` / `httpx` / `aiohttp` / `urllib.request` / `urllib3` / `socket` / `websockets` / `binance` / any Binance API / any authenticated REST / private endpoint / user stream / WebSocket / listenKey lifecycle. Any read of `.env`. Any creation of `.mcp.json`.
- **`data/microstructure/` mutation outside the approved diagnostics namespace.** Any write to `data/microstructure/` that is not the single new diagnostic JSON + its paired sidecar under `data/microstructure/diagnostics/labels/` (or an equivalent canonical namespace approved by the Phase 4bj-L brief).
- **Original artefact mutation.** Any modification of the label parquet, label manifest, label sidecars, raw / derived / feature manifests, raw zip, gate reports, or any prior successor-state artefact.

---

## 13. Interpretation limits

A future Phase 4bj-L diagnostic JSON can only support the following interpretations:

- **Descriptive characterization of the locked single-day cell.** The diagnostics describe BTCUSDT / 2025-01-15 specifically. The diagnostics do not characterize BTCUSDT generally, do not characterize other days, do not characterize other symbols, and do not characterize crypto microstructure broadly.
- **Possible recommendation for multi-day data requirements.** If the diagnostics show that the one-day cell is too small / too noisy / too censored / too pathological for the locked horizons, the recommendation may be to author a future docs-only multi-day aggTrades expansion requirements memo (analogous to Phase 4ah / 4ay).
- **Possible recommendation to remain paused.** This is the default.
- **Possible recommendation for a future failure-interpretation memo.** If diagnostics are null, degenerate, or pathological (e.g. uniformly-zero direction columns, near-zero variance returns, censoring that violates the nest, alignment failures), the recommendation may be to author a future docs-only failure-interpretation memo (analogous to Phase 3e / 3k / 4m / 4s / 4y) explaining what the one-day cell implies for future research.

A future Phase 4bj-L diagnostic JSON **cannot** support any of the following:

- **ML feasibility by themselves.** ML feasibility requires a separately authorized ML feasibility memo + Phase 4ak M0 admissibility + multi-day data. Phase 4bj-L diagnostics on a one-day cell are insufficient.
- **Strategy hypothesis by themselves.** Strategy hypotheses require M0 admission, predeclared baseline-superiority theory, cost realism (§11.6 = 8 bps per side preserved verbatim), opportunity-rate plausibility, edge-rate plausibility, design-family distance, forbidden-rescue check, falsification criteria, and post-null cooldown compliance.
- **Backtest authorization.** Backtests require a strategy spec memo + a backtest plan memo + a separately authorized backtest execution phase, none of which are authorized.
- **Acquisition authorization by themselves.** Acquisition requires a data-requirements memo + an acquisition authorization memo + an acquisition execution phase under Phase 4ay-style integrity gates.
- **Claims of edge, alpha, or predictive validity.** The diagnostics describe a one-day cell; they cannot establish edge.
- **Live-readiness.** Live-readiness requires the full Phase 4 canonical / Phase 5 gate sequence, which is not authorized.

---

## 14. Decision options

The operator has the following options after reviewing this memo. The preferred recommendation is Option B (see §15).

- **Option A — Remain paused, no diagnostic plan.** Phase 4bj-K is not merged. The project remains in the post-Phase-4bj-J state.
- **Option B — Docs-only label diagnostic study plan, no execution.** Merge Phase 4bj-K. Record the predeclared diagnostic contract. Do not authorize execution.
- **Option C — Future label diagnostic execution on full single-day cell, descriptive only.** After merging Phase 4bj-K, separately authorize a future Phase 4bj-L-equivalent execution phase that runs the §4 diagnostic categories on the full single-day cell with per-horizon censoring exclusions per §6. Produces one local gitignored diagnostic JSON + sidecar. Does not authorize ML / strategy / backtest / acquisition / live work.
- **Option D — Future neutral segmentation policy / artefact before diagnostics.** After merging Phase 4bj-K, separately authorize a future Phase 4bj-J-style neutral segmentation memo + segmentation artefact phase **before** running Phase 4bj-L. This would enable the conditional §4.14 / §4.15 diagnostic categories under neutral vocabulary.
- **Option E — Future multi-day acquisition requirements before diagnostics.** After merging Phase 4bj-K, pivot to a future docs-only multi-day aggTrades expansion requirements memo. The one-day diagnostics may be deferred or skipped if multi-day acquisition is the priority.
- **Option F — ML / strategy / backtest now.** **FORBIDDEN.** Not recommended under any circumstance. Bypasses M0 (Phase 4ak twelve-clause gate), the post-null cooldown rule, the Phase 4al no-rescue rule, the Phase 4bj-J non-authorizations, and every retained verdict.

---

## 15. Recommendation

**Primary recommendation: Option B now.**

Merge Phase 4bj-K to record the docs-only label diagnostic study plan. Do not authorize execution at this point.

**Conditional next, NOT authorized:**

- **Option C — Phase 4bj-L descriptive full-cell label diagnostic execution.** Useful for sanity-checking the label artefact. Low-stakes. Descriptive only. Recommended only if the operator wants empirical confirmation that the locked label cell is internally consistent before pivoting to multi-day acquisition or remaining paused.
- **Option E — Multi-day aggTrades expansion requirements memo.** Probably the more meaningful research path. The current arc has a single-day label cell that is structurally insufficient for ML, strategy, or backtest evidence (per Phase 4bj-I Option D, Phase 4bj-J non-authorizations, and Phase 4bj-K §13 interpretation limits). Meaningful empirical research likely requires multi-day data, which in turn requires a fresh data-requirements / acquisition / integrity-gate / normalization / feature / label arc.

**Acknowledgements (explicit):**

- Full-cell diagnostics on one day are **low-stakes and descriptive only**. They check that the label parquet is internally consistent (schema, counts, censoring nest, alignment with feature parquet) and that no leakage exists.
- They may be useful for sanity-checking the label artefact, especially for a future reviewer reading the label-family arc in isolation.
- They are **not enough for ML or strategy**. A one-day cell cannot support generalisation evidence.
- The more meaningful research path probably requires multi-day data after the current arc is closed. Whether that path is worth pursuing is an operator decision, not a Phase 4bj-K determination.

**Do not proceed directly to ML, strategy, backtests, or acquisition.** Each requires its own separately authorized successor phase that satisfies the Phase 4bk-A workflow standard, the Phase 4ak M0 twelve-clause gate, and the Phase 4al refined no-rescue rule.

---

## 16. Future phase ladder

The safe future sequence (all phases below are **NOT** authorized by Phase 4bj-K):

- **Phase 4bj-L or equivalent — Label Diagnostic Study Execution.** Descriptive full-cell diagnostics only; no ML / strategy / backtest. Output is one local gitignored JSON + sidecar under `data/microstructure/diagnostics/labels/`. No manifest mutation.
- **Alternative or parallel — Multi-day aggTrades Expansion Requirements Memo.** Docs-only memo translating Phase 4bj-I / 4bj-J / 4bj-K boundary into concrete future-data requirements for multi-day BTCUSDT (or expanded symbol scope) aggTrades acquisition.
- **Later — Acquisition authorization memo.** Docs-only memo authorizing a future Phase 4az-equivalent multi-day public-archive acquisition.
- **Later — Multi-day acquisition execution.** Docs-and-code phase under Phase 4ay-style strict integrity gate.
- **Later — Normalization / feature / label regeneration arcs for multi-day data.** Phase 4bd / Phase 4bh / Phase 4bj-C-equivalent reruns on the multi-day dataset.
- **Later — Split policy design for multi-day data.** Phase 4bj-I-equivalent that defines train / validation / test or rolling-window partitioning over multi-day data. Only at this point does train / validation / test vocabulary become admissible.
- **Later — Split artefact recording for multi-day data.** Phase 4bj-J-equivalent sibling artefact under the canonical namespace.
- **Later — Label diagnostics on multi-day data.** Phase 4bj-K / 4bj-L equivalent on the multi-day cell.
- **Later — ML feasibility memo.** Docs-only memo evaluating whether multi-day label data + features support ML feasibility under M0.
- **Later — Baseline ML diagnostic.** Conditional on ML feasibility memo authorization; descriptive baseline only.
- **Later — Failure interpretation / fallback selection memo.** Conditional on any prior failure.
- **Later — Strategy hypothesis under M0.** Docs-only memo proposing a fresh-hypothesis candidate under Phase 4ak M0 admissibility.
- **Later — Strategy spec memo.** Docs-only.
- **Later — Backtest plan memo.** Docs-only.
- **Later — Backtest execution.** Docs-and-code; standalone research script.
- **Paper / shadow / live only much later** and only after a separate explicit authorization sequence that satisfies the Phase 4bk-A workflow standard plus every retained verdict and project lock.

Every phase in this ladder is currently **NOT authorized**. None of them can be started without a separate operator authorization prompt for that specific phase.

---

## 17. M0 and no-rescue integration

- **Diagnostics are upstream of ML feasibility.** A descriptive label diagnostic on the locked one-day cell is a sanity check, not a feasibility claim. ML feasibility requires its own memo and its own data scope.
- **ML diagnostics are upstream of M0 strategy admission.** Even an ML feasibility memo does not bypass M0. A future strategy admission requires the full Phase 4ak twelve-clause gate, the Phase 4ak post-null cooldown rule, the Phase 4ak cooled-down-families list, the Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, and the Phase 4al refined no-rescue rule.
- **Diagnostics do not bypass M0.** No diagnostic result can be used as evidence that a cooled-down family (R2 / F1 / D1-A / V2 / G1 / C1) should be reopened, or as evidence that the post-null cooldown rule should be waived.
- **Labels are not signals.** This is a binding interpretation rule across Phase 4bj-H / 4bj-I / 4bj-J / 4bj-K. No label column may be treated as a trading signal. No combination of label columns with feature columns may be treated as a signal without explicit M0 admission.
- **No-split determination is not an edge claim.** The Phase 4bj-J no-split determination records a governance state (the single-day cell is insufficient for partitioning); it does not claim that the labels are or are not predictive.
- **One-day diagnostics are not generalisation evidence.** Per Phase 4bj-I §3 / §8 and Phase 4bj-K §13.
- **Retained failed strategy families remain closed.** R2 cost-fragility, F1 catastrophic-floor, D1-A mechanism / framework mismatch, V2 design-stage incompatibility, G1 regime-gate sparseness, and C1 fires-and-loses anti-validation all remain terminal for their first specs. No diagnostic result reopens any of them.
- **5m thread remains operationally closed.** Per Phase 3t. No diagnostic result reopens the 5m thread.

---

## 18. Explicit non-authorizations

Phase 4bj-K does NOT authorize:

- Phase 4bj-L (label diagnostic study execution) or any equivalent successor;
- label diagnostic execution of any kind;
- diagnostic artefact creation;
- split artefact creation;
- within-day descriptive segmentation artefact creation;
- ML implementation;
- ML training;
- ML model selection;
- feature ranking;
- meta-labeling;
- strategy implementation;
- signal computation;
- backtesting;
- additional data acquisition;
- order-book acquisition;
- mark-price acquisition;
- spot / cross-venue acquisition;
- funding / open-interest acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- production keys;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user stream;
- WebSocket implementation;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials;
- exchange-write;
- manifest transition;
- `research_eligible` flip;
- `eligibility_gate_status` transition;
- `chronological_split_policy` mutation on the original label manifest;
- Phase 5;
- Phase 4 canonical;
- any rescue / -prime / -narrow / -extension / hybrid of R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread;
- M0 amendment derived from Phase 4bj-K reasoning;
- broadening Phase 4bj-K study-plan language into binding cross-project governance beyond its docs-only scope.

---

## 19. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

---

## 20. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / mark-price stops
- M0 remains binding
- Phase 4ak M0 twelve-clause gate remains binding
- Phase 4ak post-null cooldown rule remains binding
- Phase 4ak cooled-down families list remains binding
- Phase 4al no-rescue rule remains binding (refined no-rescue + §13 boundary + §14 hierarchy)
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains binding
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy-spec
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy-spec
- Phase 4w C1 backtest-plan methodology
- Phase 4bb-F canonical path policy (raw → `gate-reports/raw/`, normalized → `gate-reports/normalized/`, features → `gate-reports/features/`, labels → `gate-reports/labels/`, successor-state → flat under `successor-state/`)

All prior phase results preserved verbatim.

---

## 21. Current-project-state update

The narrow update to `docs/00-meta/current-project-state.md` records:

- Phase 4bj-K is docs-only.
- It authorizes no diagnostic execution.
- It authorizes no diagnostic artefact.
- It authorizes no split / segmentation artefact.
- It authorizes no new data acquisition.
- It authorizes no ML / strategy / backtest / acquisition / paper-shadow / live / exchange-write.
- All retained verdicts and project locks preserved verbatim.
- Recommended state remains paused unless the operator separately authorizes a future Phase 4bj-L-equivalent diagnostic execution phase **or** pivots to a multi-day aggTrades expansion requirements memo.
- Conditional next, NOT authorized: Phase 4bj-L (descriptive full-cell label diagnostic execution; docs-and-code) **or** a docs-only multi-day aggTrades expansion requirements memo.

---

## 22. Validation

This memo is the validation contract for any future Phase 4bj-L execution phase. The current Phase 4bj-K branch work itself is docs-only:

- `git diff --check`: clean.
- `git status`: clean apart from the pre-existing untracked `.claude/scheduled_tasks.lock` and `data/research/`; no `data/microstructure/` file is staged or tracked.
- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bj-K modifies no source code, no tests, no scripts, no `pyproject.toml`, no `README.md`, and no `.gitignore`. The latest authoritative whole-repo validation remains the Phase 4bb-F-implementation merge: `ruff check .` PASS, `mypy src/prometheus` (strict) Success on 120 source files, `pytest tests/research/microstructure/` 915 passed + 1 skipped (pre-existing labelled placeholder), `pytest` (whole repo) 1698 passed + 1 skipped + 2 failed (the same pre-existing simulation `KeyError: 'trade_count'` failures in `tests/simulation/test_backtest_real_2026_03.py`; unchanged from prior phases; not introduced by this branch).

---

## Final note

Phase 4bj-K is **branch-complete only by this work**. Per the Phase 4bk-A workflow standard, Phase 4bj-K is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main`.

**Recommended state: remain paused** unless the operator separately authorizes:

- a future Phase 4bj-L-equivalent descriptive full-cell label diagnostic execution phase, or
- a future docs-only multi-day aggTrades expansion requirements memo.

Neither is authorized by Phase 4bj-K.
