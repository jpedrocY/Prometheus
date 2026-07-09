# Phase 4bn-AN — Longer-Horizon Label Build Implementation + Single Controlled Run

## 1. Branch

`phase-4bn-an/longer-horizon-label-build-single-run`

## 2. Base SHA

`ea8c6d9f8bfb116c6cfc45486be2836e77ee4a59`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AM merge
closeout. Verified in sync before branching.)

## 3. Files created / modified

Created (committed — source / tests / docs only):

- `src/prometheus/research/microstructure/longhorizon_labels_schema_v001.py`
  (sibling schema constants + config-hash builder).
- `src/prometheus/research/microstructure/longhorizon_labels_compute_v001.py`
  (sibling per-day label kernel — faithful transcription of the frozen v002
  kernel to the new horizon set — + research-namespace atomic writer).
- `scripts/phase4bn_an_build_longhorizon_labels.py` (bounded build orchestrator).
- `tests/research/microstructure/test_phase4bn_an_longhorizon_labels.py`
  (15 tests: schema, config hash, kernel reference/cross-day/censoring/direction,
  writer path discipline, orchestrator split/summary helpers).
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-an_longer-horizon-label-build-single-run.md`
  (this report) and `..._closeout.md`.

**Not** modified: any frozen module (`labels_schema_v002.py`,
`labels_compute_v002.py`, `labels_io.py`, `pre_v002_split_policy.py`, the W
orchestrator, any manifest / gate report / sidecar / split file / ML config).
`current-project-state.md` is **unchanged** (see §44). **No** local label output
was committed (the built artefacts live only under the gitignored research
namespace).

## 4. Exact documents / source inspected

Read-only (committed docs + committed source; README treated as potentially stale):
the Phase 4bn-AE preregistration, the Phase 4bn-AH/AI/AJ/AK/AL/AM reports +
closeouts + merge-closeouts, `docs/00-meta/process/`, and the committed source:
`pre_v002_ml_dataset_contract.py`, `labels_schema_v002.py`, `labels_compute_v002.py`,
`labels_io.py`, `pre_v002_split_policy.py`, `pre_v002_ml_dataset_run.py`,
`pre_v002_ml_dataset_proof.py`, and the frozen build driver
`scripts/phase4bn_w_compute_pre_v002_labels.py` (the exact pre-v002 label-build
template this phase parallels). The build **reuses** the W orchestrator's
`verify_preconditions` / `run_preflight` / `_read_feature_anchor_table` /
`_sha256_file` / `_git_head_sha` and the frozen `load_normalized_day_ref` verbatim.

## 5. Exact source data paths read

Read-only, admitted pre-v002 sources only (BTCUSDT; 2024-03-01..2024-11-30; 275
partitions):

- feature segment manifest
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  (+ sidecar) and the 275 feature Parquet partitions under
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/…`
  (only the 4 anchor columns `row_index, agg_trade_id, feature_timestamp_ms,
  source_transact_time_ms` were read per partition);
- normalized segment manifest
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  (+ sidecar) and the 275 normalized Parquet partitions under
  `…/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/…`
  (only `transact_time_ms, price, agg_trade_id, utc_date, row_index`);
- the Phase 4bn-T feature-layer gate report and the Phase 4bn-P normalized-layer
  gate report (for source binding).

Each source Parquet was SHA256-verified against its manifest-recorded hash before
compute (fail-closed on drift).

## 6. Confirmation allowed read scope

Confirmed. Only the already-admitted local pre-v002 aggTrades-derived feature +
normalized sources and their committed manifests / gate reports were read, over
2024-03-01..2024-11-30, BTCUSDT only, from the local gitignored
`data/microstructure/` namespace. No acquisition, endpoint, raw-zip, or
authenticated access occurred.

## 7. Confirmation forbidden read scope was not touched

Confirmed. No data outside the admitted pre-v002 segment; no acquisition; no
endpoint; no raw zip; no AH ML-dataset namespace; no AJ baseline namespace; no
unrelated `data/research` namespace; no credentials / private endpoints.

## 8. Confirmation no v002 terminal read

Confirmed. `v002_terminal_window_read = false`. The date guard in
`verify_preconditions` rejects any date `>= 2024-12-01`; the envelope terminal is
the max `source_transact_time_ms` on 2024-11-30; per-horizon censoring nulls every
label whose target exceeds it, so no 2024-12-01+ row is ever read.

## 9. Confirmation sealed test untouched

Confirmed. `sealed_test_split_touched = false`. The sealed test (2025-02-14..
2025-02-28) is outside the pre-v002 segment and was never read.

## 10. Confirmation test_rows_loaded = 0

Confirmed. `test_rows_loaded = 0` in the leakage/split/censoring proof and the
manifest.

## 11. Confirmation no AH/AJ output namespace mutation

Confirmed. The Phase 4bn-AH ML-dataset namespace and the Phase 4bn-AJ baseline
namespace were **not** read, hashed, listed, mutated, refreshed, created, or
deleted. The build reads only the feature + normalized source layers and writes
only its own new research namespace.

## 12. Confirmation no AH builder / AI diagnostics / AJ baseline rerun occurred

Confirmed. None of the Phase 4bn-AH dataset builder, the Phase 4bn-AI diagnostics,
or the Phase 4bn-AJ fixed baseline runner was executed. No model was trained,
scored, or evaluated; no AJ/AI/AH metric was revised or recomputed.

## 13. AM contract / spec summary

Phase 4bn-AM recorded `LABEL_CONTRACT_SPEC_RECORDED__LABEL_BUILD_AUTHORIZATION_
RECOMMENDED` and pre-registered a new sibling family
`microstructure_labels_longhorizon_aggtrades_v001` for horizons 5m (lead) / 30m /
1h over the admitted pre-v002 aggTrades segment: strict-sign direction policy (no
deadband / bp / cost / learned / optimised threshold); per-horizon
`forward_log_return_H` + `forward_direction_H` + support columns; the same
leakage/split/censoring invariants as the frozen v002 build; the compact-spec /
125 GiB-cap / local-gitignored-namespace / all-non-authorization-flags-false
posture; and **descriptive** continuous-return + 8/16 bps cost-clearing summaries
per horizon × split (economic materiality as a diagnostic, never a target). This
phase implements and runs exactly that contract.

## 14. Prospective family implemented

`microstructure_labels_longhorizon_aggtrades_v001` — a **new sibling** of the
frozen short-horizon family `microstructure_labels_aggtrades_v001` (which remains
untouched; its horizon set stays asserted `1s/5s/15s/60s`). Contract identity:
`microstructure_longhorizon_label_aggtrades_pre_v002_contract_v001`.

## 15. Horizon set

| Role | Horizon | ms | multiple of 60s |
| --- | --- | --- | --- |
| Primary / lead | `5m` | 300000 | 5× |
| Secondary diagnostic | `30m` | 1800000 | 30× |
| Secondary diagnostic | `1h` | 3600000 | 60× |

Every horizon is < one UTC day (86,400,000 ms), so the frozen v002 kernel's
current-day-or-next-day cross-day reference resolution remains valid unchanged.

## 16. Schema / column summary

35 columns in canonical order: 17 lineage + `label_config_hash` + 6 label
(`forward_log_return_{5m,30m,1h}`, `forward_direction_{5m,30m,1h}`) + 11 support
(`reference_row_index_H` / `reference_timestamp_ms_H` / `horizon_censored_flag_H`
per horizon, plus `label_invalid_price_flag`, `label_any_censored_flag`). The
forbidden-substring scan (imported verbatim from the frozen v002 schema) passes.
dtypes: int64 keys; nullable float64 returns; nullable int8 directions in
{-1,0,1}; non-null bool flags.

## 17. Direction policy summary

Strict sign of `forward_log_return_H` at a zero-log-return threshold: `+1` if
`>0`, `0` if `==0`, `-1` if `<0`, `null` if the return is null / censored /
invalid. **No** deadband, bp threshold, cost-based / learned / optimised
threshold; **no** cost-aware / magnitude / neutral-band label. The locked cost
(8 bps/side · 16 bps round-trip) is descriptive only and never enters the target.

## 18. Censoring policy summary

Per-horizon independent envelope-terminal censoring: `horizon_censored_flag_H =
true` and all `H` labels null when `feature_timestamp_ms + H_ms >
envelope_terminal_unix_ms`. `label_any_censored_flag = OR` of the per-horizon
flags. Cross-day reference allowed within the envelope; no per-day censoring; no
forward-fill beyond the envelope; no NaN/Inf in outputs. The censored fraction
grows with H and near the segment terminal (2024-11-30), and is measured/reported
(see §27).

## 19. Leakage / split proof summary

`The build produced a `leakage_split_censoring_proof.json` (+ sidecar) recording, over all 275 dates / 400,001,695 rows:

- **admitted source scope only**; source binding by SHA256 (feature + normalized segment manifests + Phase 4bn-T / 4bn-P gate reports); each source Parquet re-hashed vs its manifest SHA before compute (0 drift);
- strict per-row alignment over `row_index, agg_trade_id, feature_timestamp_ms, source_transact_time_ms, utc_date` (enforced by the kernel; feature-to-current-day normalized identity checked per row); **no source reorder; no lookahead; no future-derived features**;
- deterministic UTC-date split assignment; split date counts **train 214 / embargo 2 / validation 45 / holdout 14** (= 275); 1-day boundary embargo preserved; **embargo rows used in model splits = 0**;
- **per-horizon earlier-model-split boundary-crossing rows = 0** for every (train, validation) x (5m, 30m, 1h) - the build fails closed if any is non-zero. This holds because `max_horizon_ms = 3,600,000` < `one_day_purge_ms = 86,400,000` (`max_horizon_lt_embargo = true`): a late train/validation forward endpoint can reach at most into the embargo day, never a later model split;
- `v002_terminal_window_read = false`; `sealed_test_split_touched = false`; `test_rows_loaded = 0`; forbidden-substring scan clean; no NaN/Inf in non-null numeric outputs; `frozen_v002_family_mutated = false`; `data_committed = false`; all eight non-authorization flags `false`.`

## 20. Source binding summary

Bound to the admitted pre-v002 sources by SHA256 (verified before compute):
feature segment manifest `4881eb87…`; Phase 4bn-T feature-layer gate `db731d1b…`;
normalized segment manifest `0e96ae37…`; Phase 4bn-P normalized-layer gate
`3452fd9d…`; raw segment manifest `1659e6da…`; pre-v002 `feature_config_hash`
`0726b41d…` (never the published-v002 `819cfa7a…`). Sibling `label_config_hash`
(deterministic canonical-JSON over the family identity + policy strings + horizon
set + these witnesses): ``edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118``. Per-partition, each source feature
and normalized Parquet was additionally re-hashed against its manifest-recorded
SHA before compute.

## 21. Output namespace

`data/research/microstructure/labels/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/`
(local, gitignored via `.gitignore:88`). Per-day Parquet layout:
`…/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-longhorizon-aggtrades-<YYYY-MM-DD>.parquet`.
Manifest / proof / summary / run-record / inventory JSONs live under
`…/_manifest/`.

## 22. Output artefact list

`Under the output namespace (all gitignored):

1. **275** per-day label Parquet files (`BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-longhorizon-aggtrades-<date>.parquet`);
2. **275** paired canonical `.sha256` sidecars;
3. `_manifest/....sidecar_inventory.json` (+ sidecar) - 275 entries;
4. `_manifest/....manifest.json` (+ sidecar) - identity, source binding, boundary confirmations, non-authorization flags, per-day inventory;
5. `_manifest/....leakage_split_censoring_proof.json` (+ sidecar);
6. `_manifest/....continuous_return_cost_summary.json` (+ sidecar);
7. `_manifest/....build_run_record.json` (+ sidecar).

Total: 275 Parquet + 275 Parquet sidecars + 5 JSON artefacts + 5 JSON sidecars.`

## 23. Sidecar / hash validation summary

`Post-run verification (recomputed independently of the build): all **5** manifest/proof/summary/run-record/inventory JSON sidecars match their JSON body SHA256; a sample of per-day label Parquets across all four split regions (2024-03-01 train, 2024-09-30 train-end, 2024-10-01 embargo, 2024-11-15 validation-end, 2024-11-16 embargo, 2024-11-30 holdout-end) re-hash to their inventory SHA and their `.sha256` sidecar bodies are the canonical two-space form; the per-day inventory has **275 distinct dates**; the sum of per-day `row_count` = **400,001,695** = the manifest total = the expected pre-v002 row count.`

## 24. Build budget preflight

Reused the frozen Phase 4bn-L label caps via `run_preflight`: estimated label
footprint `400,001,695 × 160 B ≈ 59.6 GiB` (< 75 GiB warn, < 125 GiB hard);
D: free `1,166` GiB (≥ 500 GiB preflight floor); total-stack estimate
within caps. Preflight PASSED before any write.

## 25. Build runtime summary

`Single controlled run, one-run guard active (refuses to overwrite a populated output namespace). Runtime **4,716 s (~78.6 min)** for 275 days; well under the frozen `RUNTIME_HARD_SECONDS` (8 h) cap. Each day: SHA-verify feature + normalized source Parquet -> read 4 feature anchor columns + load current/next normalized day -> compute the sibling kernel -> atomic-write Parquet + sidecar -> fold into split-aware descriptive summaries. Streaming per-day; no wide feature matrix materialised.`

## 26. Row / partition counts

`**275 partitions**, one per UTC date 2024-03-01..2024-11-30; **400,001,695** total label rows (one label row per feature row, exactly matching the admitted source). Kept-row split totals: **train 304,816,127** (214 dates), **validation 68,578,296** (45 dates), **holdout 23,535,860** (14 dates), **embargo 2 dates** (labels produced; excluded from the model-split descriptive summaries). No target imputed; 0 invalid prices.`

## 27. Per-horizon support / censoring counts

`Per-horizon envelope-terminal censored-row totals (segment-wide): **5m = 1,528**, **30m = 9,916**, **1h = 23,650** - monotonically increasing with horizon, as expected, and confined to the holdout tail nearest the 2024-11-30 envelope terminal (train and validation have 0 censoring because their forward windows lie inside the envelope). Even at 1h the censored share is ~0.006% of all rows (~0.10% of holdout). `label_invalid_price_flag` total = **0**.`

## 28. Per-horizon / split class counts and fractions

``forward_direction_H` class balance (per horizon x split), near-binary with a tiny flat class (consistent with Phase 4bn-AI at 15s):

| split:H | -1 (%) | 0 (%) | +1 (%) |
| --- | --- | --- | --- |
| train:5m | 49.3 | 0.06 | 50.6 |
| train:30m | 48.8 | 0.02 | 51.2 |
| train:1h | 48.8 | 0.02 | 51.2 |
| validation:5m | 48.7 | 0.06 | 51.2 |
| validation:30m | 47.1 | 0.02 | 52.9 |
| validation:1h | 46.5 | 0.02 | 53.5 |
| holdout:5m | 49.5 | 0.05 | 50.4 |
| holdout:30m | 47.8 | 0.02 | 52.1 |
| holdout:1h | 46.2 | 0.01 | 53.8 |

The exactly-zero (flat) class shrinks as the horizon lengthens (fewer exactly-equal reference prices over longer windows).`

## 29. Per-horizon / split continuous-return summary

`Descriptive `|forward_log_return_H|` distribution in bps (histogram-estimated percentiles, 0.05 bps bin width; exact mean/max), per horizon x split:

| split:H | support | median | mean | p90 | p99 | max |
| --- | --- | --- | --- | --- | --- | --- |
| train:5m | 304,816,127 | 11.43 | 18.69 | 41.9 | 115.4 | 700.4 |
| train:30m | 304,816,127 | 25.33 | 40.49 | 92.2 | 238.6 | 1130.3 |
| train:1h | 304,816,127 | 34.43 | 55.11 | 126.7 | 318.7 | 1184.6 |
| validation:5m | 68,578,296 | 10.58 | 16.25 | 37.5 | 87.0 | 296.7 |
| validation:30m | 68,578,296 | 24.48 | 36.67 | 84.3 | 189.6 | 368.5 |
| validation:1h | 68,578,296 | 33.08 | 50.10 | 117.9 | 248.8 | 604.8 |
| holdout:5m | 23,534,374 | 10.73 | 14.44 | 32.4 | 60.3 | 113.7 |
| holdout:30m | 23,525,986 | 23.98 | 32.07 | 71.0 | 129.6 | 238.0 |
| holdout:1h | 23,512,252 | 32.68 | 43.02 | 94.4 | 165.0 | 315.5 |

The raw absolute move grows monotonically with horizon (median ~10-11 bps at 5m, ~24-25 bps at 30m, ~33-34 bps at 1h), consistent with dispersion increasing over longer windows. All values are in log-return bps (`|log_return| x 1e4`), the same convention as the Phase 4bn-AJ 15s cost stats.`

## 30. Per-horizon / split 8 bps / 16 bps cost-clearing shares

`Descriptive share of moves clearing the locked cost thresholds, per horizon x split (exact counters):

| split:H | share > 8 bps | share > 16 bps |
| --- | --- | --- |
| train:5m | 62.09% | 37.80% |
| train:30m | 81.61% | 65.27% |
| train:1h | 86.43% | 73.70% |
| validation:5m | 59.38% | 34.95% |
| validation:30m | 81.05% | 64.28% |
| validation:1h | 85.91% | 72.72% |
| holdout:5m | 60.65% | 33.80% |
| holdout:30m | 81.87% | 64.87% |
| holdout:1h | 86.40% | 73.29% |

For descriptive context only: at 15s (Phase 4bn-AJ) **2.47%** of validation moves exceeded the 16 bps round-trip; at 5m the validation share is ~35%, at 30m ~64%, at 1h ~73%. The raw last-trade-price move distribution is therefore far more often larger than the locked round-trip cost at longer horizons. **This is a descriptive property of the raw move distribution only** - see the binding interpretation note in section 30 below: it is not evidence of tradability, predictability, edge, or PnL, and aggTrades-only data cannot express the spread/slippage that a tradability claim would require.`

**Interpretation (binding).** These are **descriptive label-materiality
diagnostics only**. They are **not** evidence of tradability, profitability,
economic edge, PnL, strategy viability, backtest validity, execution viability, or
live-readiness, and must never be cited as such. They describe the raw
last-trade-price move distribution on aggTrades-only data (which cannot express
spread / slippage / mid-price) at longer horizons; they do not establish that any
move is capturable.

## 31. Per-month / per-date summary status

`Split-level summaries (train / validation / holdout) are chronological blocks by construction (train ~ 2024-03..09, validation ~ 2024-10..mid-11, holdout ~ tail of 2024-11), so sections 28-30 already report the coarse per-period breakdown. **Per-date** row counts, per-horizon censored counts, and invalid-price counts are carried for all 275 dates in the manifest `per_day_inventory`. Finer **per-month / per-date return distribution** summaries were **not** emitted in this run (to keep the summary artefact compact and within the descriptive build scope); a future, separately-authorized descriptive pass could add them from the already-built labels without a new data read. Recorded here as a scope note, not a gap in the built label layer.`

## 32. Storage footprint

`Total label footprint **11,940,496,483 bytes (~11.12 GiB / 12 GB on disk)** across the 275 Parquet files + sidecars - well under the frozen Phase 4bn-L 125 GiB hard cap (and under the 75 GiB warn threshold). Narrower than the frozen v002 pre-v002 W label segment (~15 GB for 4 horizons x 8 label + 14 support columns) because this sibling has 3 horizons x 6 label + 11 support columns. D: free after the run remained ~1.15 TB.`

## 33. Gitignored / local namespace confirmation

Confirmed. The entire output namespace resolves under `data/research/` and is
gitignored (`git check-ignore -v` → `.gitignore:88`). `git status --short` shows
**no** data file; only the source / test / docs files are tracked additions.

## 34. Confirmation no data committed

Confirmed. No Parquet, sidecar, manifest, proof, summary, or any file under
`data/microstructure/` or `data/research/` was staged or committed;
`.claude/scheduled_tasks.lock` was not committed.

## 35. Confirmation no ML / training / scoring / prediction / inference

Confirmed. This is a label-layer build only. No model / training / scoring /
prediction / inference occurred; all non-authorization flags remain `false`.

## 36. Confirmation no extra diagnostics beyond build-required descriptive summaries

Confirmed. The only diagnostics produced are the AM-required descriptive
continuous-return / cost-clearing / class-balance summaries per horizon × split.
No feature-importance, no model evaluation, no exploratory analysis beyond these.

## 37. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search

Confirmed. None occurred. The direction threshold is the fixed strict-sign zero
threshold; no threshold was tuned, learned, or selected after seeing the
distributions.

## 38. Confirmation no strategy / signals / PnL / backtest / live / exchange-write

Confirmed. None occurred.

## 39. Allowed claims preserved

Preserved verbatim (Phase 4bn-AE §8): (a) short-horizon directional information;
(b) v002 small-lift sign reproduction; (c) calibration / confidence-tail
assessment. This build adds only a **descriptive label-materiality** measurement
of the longer-horizon raw-return distributions; it asserts no new predictive or
economic claim.

## 40. Forbidden claims preserved

Preserved verbatim (Phase 4bn-AE §8 / §19): no tradability; profitability;
strategy / execution viability; slippage/spread adequacy; live / paper-shadow
readiness; PnL; backtest validity; production suitability; economic significance.
The longer-horizon cost-clearing shares are descriptive context, **not** evidence
of edge. The locked cost reference remains 8 bps/side · 16 bps round-trip. This
build does **not** claim longer horizons are tradable.

## 41. Validation commands and results

`- `git rev-parse main`/`origin/main`/`HEAD` (pre-branch) -> all `ea8c6d9f8bfb116c6cfc45486be2836e77ee4a59`. OK
- `git checkout -b phase-4bn-an/longer-horizon-label-build-single-run` at base SHA. OK
- `pytest tests/research/microstructure/test_phase4bn_an_longhorizon_labels.py` -> **15 passed**. OK
- `ruff check` (2 new src modules + orchestrator + test) -> **All checks passed**. OK
- `mypy` (2 new src modules) -> no errors attributed to the new modules (pre-existing errors remain only in unrelated frozen `features_compute*` / `multiday_feature_gate_checks` modules - the repo's existing baseline). OK
- Frozen regression: `test_labels_schema_v002` + `test_labels_compute_v002` + `test_phase4bn_aa_pre_v002_split_policy` -> **108 passed** (no regression). OK
- `git diff --check` -> clean. OK
- `git ls-files data/microstructure/` and `git ls-files data/research/` -> **0 tracked**. OK
- `git check-ignore -v data/microstructure/` -> `.gitignore:85`; `data/research/` -> `.gitignore:88`. OK
- `git status --short` -> no `data/` file; only the 5 source/test/docs additions (+ transient `.claude/scheduled_tasks.lock`, not committed). OK
- Independent post-run artefact verification: 5/5 JSON sidecars valid; sampled per-day Parquet SHAs + sidecars valid; 275 distinct dates; inventory rows sum = 400,001,695. OK
- `git diff --name-status main..HEAD` (after commit) -> only the 5 source/test/docs files. OK`

## 42. Git status

`Before commit: five untracked additions - the 2 new `src/.../longhorizon_labels_*` modules, the orchestrator `scripts/phase4bn_an_build_longhorizon_labels.py`, the test `tests/.../test_phase4bn_an_longhorizon_labels.py`, and the 2 report docs - plus the transient `?? .claude/scheduled_tasks.lock` (not committed). No `data/` file staged. The 12 GB built label layer under `data/research/...` is gitignored and untracked. Final committed SHA and post-commit `git status --short` are reproduced in the closeout and the final operator report.`

## 43. Result state

``LONGER_HORIZON_LABEL_BUILD_COMPLETE__LOCAL_LABEL_ARTEFACTS_WRITTEN__NO_ML__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED``

## 44. Recommended next state

**Remain paused.** The longer-horizon label layer is built locally and gitignored;
its descriptive summaries are recorded. No ML / diagnostics over the built labels,
and no strategy / PnL / backtest / live path, is authorized — each requires its own
separate future operator authorization (and, for any trading path, the Phase
4bn-AE §19 M0-style mechanism-admissibility gate). `current-project-state.md` is
left unchanged, matching the immediate Phase 4bn-AH..AM precedent (the update
convention at this arc point is not clear/consistent; per the operator instruction
it is not updated and is recorded here as unchanged).

## 45. Explicit no-successor execution statement

Phase 4bn-AN authorizes **no** successor execution phase. It does not, and does not
authorize anyone to: run ML / training / scoring / prediction / inference / new
diagnostics over the built labels; perform feature selection / threshold
optimization / model selection / hyperparameter search; do strategy / signals /
PnL / backtest / Sharpe / hit-rate / position sizing / execution / paper / shadow /
live-readiness / deployment / exchange-write; adopt a cost-aware / magnitude /
deadband label or tune any threshold; acquire data or call any endpoint; read the
v002 terminal / sealed test / test rows; mutate the frozen v002 family or any
published manifest / gate / sidecar / split file / ML config; or authorize any
Phase 5 / successor phase. Every retained verdict and project lock (H0 / R3 / R1a /
R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1; 8 bps/side · 16 bps
round-trip; the Phase 4ak M0 twelve-clause gate; Phase 4al no-rescue; the Phase 4aw
`flip_research_eligible(...)` always-raises invariant — never invoked; Phase 4bb-F
sidecar policy; the Phase 4bn-AA split artefact, 4bn-AC ML dataset contract, 4bn-AE
claim-scope, and the 4bn-AH..AM results including the AK single-follow-up selection,
the AL label-memo recommendation, and the AM contract / no-build-until-authorized
boundary) is preserved verbatim. Phase 4 canonical remains unauthorized. Do not
merge to main and do not push unless explicitly instructed in a later prompt; do
not generate a merge-closeout or the next-phase prompt unless explicitly instructed
later.
