# Phase 4bn-AI — Descriptive Dataset Diagnostics, No Models

## 1. Branch

`phase-4bn-ai/descriptive-dataset-diagnostics-no-models`

## 2. Base SHA

`6e3361f1675d6e0adfc42835cd623fce4d7af1c2`
(`main` / `origin/main` tip after the Phase 4bn-AH merge closeout).

## 3. Phase type

Read-only descriptive diagnostics over the Phase 4bn-AH dataset-specification
artefacts. **No models, no scoring, no predictions, no strategy, no data
acquisition.** Docs-only committed change set (a read-only ad-hoc diagnostics
script was executed from the scratchpad and is **not** committed; every number
below is reproducible from the four committed-by-hash AH artefacts).

## 4. Files created / modified

Created (committed):

- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ai_descriptive-dataset-diagnostics-no-models.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ai_closeout.md`.

No source module, test, manifest, gate report, sidecar, split file, ML config, or
`data/` artefact was created or modified. No new dataset namespace was created. A
transient read-only diagnostics script (`ai_diag.py`) was run from the
session scratchpad (outside the repository) and is intentionally not committed.

## 5. Exact AH artefacts read

All under `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
(local, gitignored, uncommitted):

- `dataset_manifest.json` (+ `.sha256`)
- `train_only_transform.json` (+ `.sha256`)
- `split_index.json` (+ `.sha256`)
- `leakage_split_integrity_proof.json` (+ `.sha256`)

No other file was opened. No feature/label Parquet, no v002 terminal window, no
sealed test split, no raw zip, no endpoint.

## 6. Confirmation all reads were read-only

Confirmed. Every artefact was opened in read (`rb` / `r`) mode only. Nothing under
`data/microstructure/` or `data/research/` was written, overwritten, deleted,
mutated, or refreshed. The AH namespace still contains exactly the 8 files it held
before this phase (verified by directory listing and by recomputing all four
SHA256 hashes, which still match the committed sidecars — see §7).

## 7. Sidecar verification results

Recomputed SHA256 for each artefact and compared against its `.sha256` sidecar;
verified canonical two-space format and that the sidecar basename matches the
artefact basename.

| Artefact | Computed SHA256 | Sidecar match | Format / basename |
| --- | --- | --- | --- |
| `dataset_manifest.json` | `36a13213…4b0f659c` | ✅ | two-space, name ok |
| `train_only_transform.json` | `85f6ea35…e2d28ee5` | ✅ | two-space, name ok |
| `split_index.json` | `d1681acd…bf9f0e35` | ✅ | two-space, name ok |
| `leakage_split_integrity_proof.json` | `e36c9163…9783a4a8` | ✅ | two-space, name ok |

All four **PASS**. No mismatch. (Full hashes match the AH closeout §"Data outputs
gitignored" values and the AH merge-closeout.)

## 8. Proof preservation check results

Loaded `leakage_split_integrity_proof.json` read-only. All required flags remain
as recorded by Phase 4bn-AH:

| Field | Value | Required | OK |
| --- | --- | --- | --- |
| `v002_terminal_window_read` | `false` | false | ✅ |
| `sealed_test_split_touched` | `false` | false | ✅ |
| `test_rows_loaded` | `0` | 0 | ✅ |
| `non_authorization.ml_authorized` | `false` | false | ✅ |
| `non_authorization.diagnostics_authorized` | `false` | false | ✅ |
| `non_authorization.strategy_authorized` | `false` | false | ✅ |
| `non_authorization.signals_authorized` | `false` | false | ✅ |
| `non_authorization.pnl_authorized` | `false` | false | ✅ |
| `non_authorization.backtest_authorized` | `false` | false | ✅ |
| `non_authorization.live_authorized` | `false` | false | ✅ |
| `non_authorization.exchange_write_authorized` | `false` | false | ✅ |

Split integrity:

- `no_random = true`, `no_shuffle = true`, `no_kfold = true`, `no_bootstrap = true`.
- `deterministic_assignment_by_source_transact_time_ms_utc_date = true`.
- `no_embargo_date_used = true` (zero embargo rows used in any split).
- `per_horizon_boundary_crossing_rows = {1000ms:0, 5000ms:0, 15000ms:0, 60000ms:0}`
  and `per_horizon_zero_earlier_split_boundary_crossing_rows = true`.
- `forbidden_column_scan_empty = true`.
- Date counts `train=214`, `validation=45`, `holdout=14`,
  `train_validation_embargo=1`, `validation_holdout_embargo=1` → sum **275**.

Proof result **remains valid and preserved**. Note: `diagnostics_authorized`
inside the artefact is a *builder-run* flag that stays `false`; the current
operator prompt authorizes this descriptive-diagnostics phase externally. This
phase did not flip it (or any flag) — the artefact is unchanged.

## 9. Dataset manifest consistency check results

Loaded `dataset_manifest.json` read-only. Values match the AH single-run report
and merge-closeout exactly:

| Quantity | Manifest | AH report | OK |
| --- | --- | --- | --- |
| streamed / total | 400,001,695 | 400,001,695 | ✅ |
| train raw | 304,816,127 | 304,816,127 | ✅ |
| embargo raw | 3,071,370 | 3,071,370 | ✅ |
| validation raw | 68,578,296 | 68,578,296 | ✅ |
| holdout raw | 23,535,902 | 23,535,902 | ✅ |
| train kept | 304,816,127 | 304,816,127 | ✅ |
| validation kept | 68,578,296 | 68,578,296 | ✅ |
| holdout kept | 23,535,860 | 23,535,860 | ✅ |
| holdout censored drop | 42 | 42 | ✅ |

- Sum of raw split rows (incl. embargo) `= 400,001,695 =` `streamed_row_count`. ✅
- `targets_imputed = false` (no imputation of labels). ✅
- Posture is a **compact dataset specification** (train-only transform stats +
  per-date split/filter index + per-month/class summaries + proof + manifest),
  **not** a full materialised feature matrix. ✅ (`decimation_policy =
  reserved_not_adopted`, `decimation_stride = null`.)

## 10. Split index consistency check results

Loaded `split_index.json` read-only.

- `per_date` entries: **275**; unique dates: **275**; duplicates: **0**;
  out-of-segment: **0**; no missing / multi-assigned dates.
- Date counts by split from the index: `train=214`, `embargo=2`, `validation=45`,
  `holdout=14`. This equals the proof's `214 + 45 + 14 + 1 + 1` (the proof counts
  the two 1-day boundary embargoes separately as `train_validation_embargo=1` and
  `validation_holdout_embargo=1`; the index labels both dates `embargo`). ✅
- Chronological order preserved: first `2024-03-01` (train) → last `2024-11-30`
  (holdout), with the two embargo dates `2024-10-01` (train↔validation) and
  `2024-11-16` (validation↔holdout).
- Per-date schema present: `date`, `split`, `raw_row_count`,
  `filtered_row_count`, `dropped_by_reason`. Month blocks present in the manifest
  (`month_block_split_rows`). ✅
- Row reconciliation (filtered rows summed from the index vs manifest kept):
  `train 304,816,127`, `validation 68,578,296`, `holdout 23,535,860` — all match.
  Grand total kept `= 396,930,283`. The two embargo dates carry
  `filtered_row_count = 0` with `dropped_by_reason.embargo_date_dropped` summing
  to `1,998,100 + 1,073,270 = 3,071,370`, exactly the manifest embargo raw count.
  (Embargo rows are streamed then excluded — raw ≠ kept by design, not a defect.)

## 11. Train-only transform consistency check results

Loaded `train_only_transform.json` read-only.

- `fit_split = "train"`; every per-feature `*_count` is a **train** count. No
  validation/holdout/test statistic contributes to the fitted transform. ✅
- 45 features have fitted stats; `feature_count = 45`.
- Feature-list hash equality: manifest `feature_list_hash` == transform
  `feature_list_hash` == proof `active_feature_list_hash` ==
  `8e705ba8800421ae0ccc55cdbf115a36dce9f27f8682e552e2b59c4ab83df7b9`. ✅
- Forbidden-column scan: proof `forbidden_column_scan_empty = true` (no forward
  label / future-derived column in the 45-column allowlist). ✅
- Standardisation rule: `subtract_train_mean_divide_by_max_train_std_epsilon`
  (`epsilon = 1e-08`), boolean flags not standardised; imputation rule
  `fixed_zero_for_null_numeric` (fill `0.0`) — applies to feature nulls, **not**
  to labels (labels are dropped, never imputed).

All required pre-diagnostics checks **PASS**. Diagnostics proceed.

---

## 12. Split / population summary

| Split | Raw rows | Kept rows | Dropped (total) | Drop reasons | Retained % |
| --- | --- | --- | --- | --- | --- |
| train | 304,816,127 | 304,816,127 | 0 | — | 100.000000% |
| validation | 68,578,296 | 68,578,296 | 0 | — | 100.000000% |
| holdout | 23,535,902 | 23,535,860 | 42 | censored 42 | 99.999822% |
| embargo | 3,071,370 | 0 (excluded) | 3,071,370 | embargo_date_dropped | 0% (by design) |

- Embargo rows excluded from every split: **3,071,370** (two 1-day boundary
  embargoes). Not available to train, validation, or holdout.
- Only drop across the three usable splits: **42** holdout rows, all
  `censored` (segment-terminal 15s censoring), matching the label manifest's 15s
  count. `invalid_price = 0`, `null_direction = 0`, `null_log_return = 0`
  everywhere.
- **No imputation** of targets (`targets_imputed = false`). Kept total across
  usable splits: **396,930,283**.

## 13. Class-balance diagnostics (`forward_direction_15s`, classes {-1, 0, 1})

| Split | class -1 | class 0 | class 1 | minority share |
| --- | --- | --- | --- | --- |
| train | 150,077,008 (49.2353%) | 3,590,082 (1.1778%) | 151,149,037 (49.5870%) | 1.1778% (class 0) |
| validation | 33,619,134 (49.0230%) | 1,013,759 (1.4783%) | 33,945,403 (49.4988%) | 1.4783% (class 0) |
| holdout | 11,532,338 (48.9990%) | 228,247 (0.9698%) | 11,775,275 (50.0312%) | 0.9698% (class 0) |

- The task is **near-binary**: the flat class `0` is a ~1% minority in every
  split; the ±1 directional classes are close to balanced (each ~49–50%).
- Train→validation class drift (pp): `-1: -0.21`, `0: +0.30`, `1: -0.09`.
- Validation→holdout class drift (pp): `-1: -0.02`, `0: -0.51`, `1: +0.53`.
- Month-level class distribution is **not** carried per-month in the AH artefacts
  (`month_block_split_rows` holds row counts by month/split, not per-month class
  counts). Class counts are available at the split granularity only — see §20.
- **Descriptive only.** These are population frequencies of the label field; they
  are not model outputs and imply nothing about predictability.

## 14. Date / month block diagnostics

Rows by UTC month (kept/filtered), from `split_index.json`:

| Month | Rows (kept) | % of kept | Splits present |
| --- | --- | --- | --- |
| 2024-03 | 66,512,993 | 16.757% | train |
| 2024-04 | 52,506,247 | 13.228% | train |
| 2024-05 | 38,945,717 | 9.812% | train |
| 2024-06 | 26,121,815 | 6.581% | train |
| 2024-07 | 37,540,956 | 9.458% | train |
| 2024-08 | 47,852,373 | 12.056% | train |
| 2024-09 | 35,336,026 | 8.902% | train |
| 2024-10 | 35,631,236 | 8.977% | validation (+ embargo 0 kept) |
| 2024-11 | 56,482,920 | 14.230% | validation 32,947,060 + holdout 23,535,860 |

- **Dominant month:** 2024-03 at 16.757% of kept rows. No single month exceeds
  ~17%; the sample is spread across 9 UTC months (2024-03 … 2024-11).
- **Split concentration is by design (chronological):** train occupies
  2024-03 → 2024-09; validation 2024-10 → mid-2024-11; holdout the tail of
  2024-11. Validation and holdout are therefore concentrated in the two most
  recent months by construction of the
  `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` policy — not a
  sampling artefact.
- Rows are unevenly distributed across dates (per-date kept counts range from
  <1M to >5M) reflecting real activity variation; summarised here at month
  granularity rather than dumping all 275 date rows.

## 15. Target / drop diagnostics

- Censored rows by split: holdout **42** (`censored`), train **0**, validation
  **0**. These are segment-terminal rows whose 15s forward window extends past the
  end of the data segment (2024-11-30), so no valid forward label exists — they
  are **dropped, not imputed**.
- Null direction / null log-return / invalid-price drops: **0** across all splits.
- Per-horizon earlier-split boundary-crossing rows: **0** at all four horizons
  (1s/5s/15s/60s) — no label window reaches back into an earlier split.
- Segment-terminal censoring explanation: only the horizon-length tail of the
  final segment date is affected; 42 rows is the exact 15s-horizon terminal count.
- **No imputation.**

## 16. Effective sample / dependence caveat diagnostics

- AH `dependence_caveat` (verbatim): *"aggTrades 15s forward labels overlap
  heavily; rows are NOT independent; per-row metrics are descriptive only and
  per-row significance language is forbidden (Phase 4bn-AE Option 1)."*
- `row_level_metrics_descriptive_only = true`; `decision_block_units =
  [utc_date, utc_month]`.
- The **~397M kept rows are not ~397M independent observations.** Consecutive
  aggTrade rows share heavily overlapping 15s forward-label windows, so labels are
  strongly autocorrelated at the sub-15s scale; the natural decision blocks are
  **275 UTC dates** and **9 UTC months**.
- **Effective sample size is not computed here.** Deriving it exactly requires
  row-level autocorrelation / block analysis, which needs the original Parquet
  rows — **not authorized** in this phase. Recorded as a limitation (§20), not
  estimated or invented. The block counts (275 dates / 9 months) frame the
  dependence structure without asserting a specific effective-N.

## 17. Feature-transform descriptive diagnostics

- 45 train-fitted features; `fit_split = train`; each stat carries a train count,
  mean, std, and null count.
- **Null coverage:** only the four past-window log-return features carry any train
  nulls — `rolling_log_return_past_window_15s` 519,
  `rolling_log_return_past_window_1s` 16, `rolling_log_return_past_window_5s` 155,
  `rolling_log_return_past_window_60s` 2,093 — total **2,783** nulls across
  304,816,127 train rows (≈9.1e-6 of train cells for those columns; all other 41
  features have **0** nulls). Nulls are filled with fixed `0.0` per the imputation
  rule (feature-level only).
- Descriptive location/dispersion is present per feature (train mean/std/count).
  Illustrative examples (train split): `rolling_aggtrade_count_60s` mean
  2813.68 / std 4381.28; `rolling_aggressive_flow_ratio_15s` mean 0.4950 / std
  0.2356; `rolling_aggressive_quantity_imbalance_60s` mean −20.50 / std 377.82;
  `rolling_log_return_past_window_15s` mean −2.52e-05 / std 1.12e-03;
  `milliseconds_since_day_start` mean 4.53e7 / std 2.33e7.
- **No feature selection, no importance ranking, no predictive interpretation, no
  include/exclude recommendation.** These are population descriptive statistics of
  the *input features* only.

## 18. Economic-relevance boundary diagnostics

- Project lock §11.6: **8 bps per side, 16 bps round-trip.** The AH proof records
  `evaluation.locked_round_trip_cost_bps = 16.0`, matching the lock.
- **`forward_log_return_15s` distribution fields are NOT present in the AH
  artefacts.** The manifest's `primary_target` is `forward_direction_15s` (the
  sign/class field); the artefacts carry class *counts* for the categorical label
  but **no** location/dispersion/tail statistics of the continuous forward
  15s log-return. The only log-return statistics present are for the **past-window
  feature** `rolling_log_return_past_window_15s` (train mean −2.52e-05, std
  1.12e-03) — a lookback feature, **not** the forward label, and therefore not a
  basis for any cost comparison.
- Consequently, a descriptive comparison of the forward-return distribution to the
  16 bps round-trip cost **cannot be computed from AH artefacts alone** without an
  unauthorized row-level read. Recorded as a limitation (§20).
- **No tradability, edge, or strategy-viability inference is made or implied.**

## 19. Calibration / metric-registry readiness

Present in the AH proof `evaluation` block (schema only — nothing run):

- `calibration_schema_present = true`; `cost_descriptive_fields_present = true`;
  `dependence_caveat_present = true`; `high_confidence_threshold = 0.8`.
- 21 `mandatory_metrics` pre-registered (majority/persistence floors, accuracy /
  balanced-accuracy / macro-F1, per-class P/R/F1, confusion matrix, predicted-class
  distribution, zero-class prevalence & predicted-zero rate, log-loss, Brier,
  calibration reliability table, high-confidence tail size/accuracy, train↔val and
  val↔holdout deltas, filtered-row date counts, dropped-rows-by-reason).
- `metric_granularities = [aggregate, utc_month, utc_date]`;
  `claim_scope_allowed = [directional_information_diagnostic,
  v002_small_lift_sign_reproduction, calibration_confidence_tail_assessment]`;
  `claim_scope_forbidden` includes tradability, profitability, strategy/execution
  viability, slippage/spread adequacy, live/paper-shadow readiness, PnL, backtest
  validity, production suitability, economic significance.
- What this **enables in a future, separately-authorized baseline phase (4bn-AJ):**
  a pre-registered, leakage-guarded evaluation harness with fixed success/kill
  thresholds and forbidden claim scope. **Nothing was calibrated, trained, or
  scored here.**

## 20. Diagnostics completed vs not possible from AH artefacts alone

**Completed from AH artefacts (read-only):**

1. Sidecar SHA256 verification (4/4).
2. Proof preservation + authorization/leakage flag check.
3. Dataset manifest consistency (streamed/split/kept/drop counts).
4. Split index consistency (275 dates, no dup/missing/multi-assign, reconciliation).
5. Train-only transform provenance + 45-column hash equality + forbidden scan.
6. Split/population summary (raw/kept/dropped/retained%, embargo exclusion).
7. Class-balance diagnostics by split (+ split-to-split drift).
8. Date/month block diagnostics (rows by month, dominant month, split coverage).
9. Target/drop diagnostics (censoring, per-horizon boundary crossings).
10. Effective-sample dependence framing (block counts 275 dates / 9 months).
11. Feature-transform descriptive stats (train mean/std/count/null per feature).
12. Calibration / metric-registry readiness (schema presence and contents).

**Not possible from AH artefacts alone (would require unauthorized row-level
reads — NOT performed):**

1. `forward_log_return_15s` continuous-distribution statistics (location /
   dispersion / tails) and any descriptive comparison to the 16 bps round-trip
   cost — the artefacts carry only the categorical `forward_direction_15s` counts
   and the *past-window* log-return feature stats.
2. Exact effective sample size / autocorrelation-adjusted N — needs row-level
   temporal analysis.
3. Per-month or per-date **class** distributions — the artefacts carry per-month
   *row* counts and per-split *class* counts, but not their cross-tabulation.
4. Any feature↔label association, mutual information, or predictive signal — out of
   scope and would in any case require row-level joins.

**Explicit confirmation:** no unauthorized source was read to fill any of the
above; each was recorded as a limitation instead.

## 21. Explicit forbidden-boundary confirmations

- No AH builder rerun. ✅
- No feature/label Parquet row read. ✅
- No v002 terminal window read. ✅
- No sealed test touch. ✅
- `test_rows_loaded = 0` preserved. ✅
- No ML. ✅ No model. ✅ No scoring. ✅ No predictions. ✅ No inference. ✅
- No feature selection. ✅ No threshold optimization. ✅
- No strategy / signals / PnL / backtest. ✅
- No accuracy/AUC/precision/recall/F1/calibration-curve/Sharpe/PnL/hit-rate
  computed. ✅
- No feature importance ranking / candidate selection / strategy proposal. ✅
- No data acquisition. ✅ No endpoint calls. ✅ No raw-zip read. ✅
- No data-output mutation (AH namespace byte-identical; hashes re-verified). ✅
- No new dataset namespace created. ✅
- No eligibility / authorization / gate / manifest / sidecar flag transition. ✅
- `flip_research_eligible(...)` always-raises invariant preserved (never invoked). ✅

## 22. Validation commands and results

- `git rev-parse main` / `origin/main` / `HEAD` (pre-branch) → all
  `6e3361f1675d6e0adfc42835cd623fce4d7af1c2`. ✅
- `git check-ignore -v data/microstructure/` → `.gitignore:85`. ✅
- `git check-ignore -v data/research/` → `.gitignore:88`. ✅
- `git check-ignore -v data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
  → `.gitignore:88`. ✅
- `git ls-files data/microstructure/` / `data/research/` /
  `…/pre_v002_contract_v001/` → **0 tracked files** each. ✅
- AH namespace listing → exactly 4 JSON + 4 `.sha256` (8 files). ✅
- `sha256sum` recompute of all four artefacts → matches all four sidecars
  (two-space canonical, basenames match). ✅
- `git diff --check` → clean. ✅
- `git status --short` → only `?? .claude/scheduled_tasks.lock` plus the two new
  committed docs (see §23). ✅
- No pytest/ruff/mypy required (docs-only; no source or test files changed). The
  read-only diagnostics script ran outside the repo from the scratchpad.

## 23. Git status

Before commit: the two new report/closeout docs untracked, plus the transient
`?? .claude/scheduled_tasks.lock` (not committed). No `data/` file staged. Final
committed SHA(s) and post-commit `git status --short` are reproduced in the
closeout and the final operator report.

## 24. Result state

`DESCRIPTIVE_DATASET_DIAGNOSTICS_RECORDED__AH_PROOF_PRESERVED__NO_MODELS__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## 25. Recommended next state

**Remain paused.** No successor authorized. A future Phase 4bn-AJ (fixed baseline
run applying the pre-registered Phase 4bn-AE success/kill evaluation) is
*recommended-not-authorized* and requires separate operator authorization plus a
committed end-to-end pre-v002 trainer (which does not yet exist) and an
`ml_authorized` transition.
