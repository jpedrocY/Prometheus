# Phase 4bn-AJ — Fixed Pre-v002 Baseline Run + Verdict

## 1. Branch

`phase-4bn-aj/fixed-pre-v002-baseline-run-verdict`

## 2. Base SHA

`f33831c8577764c5fbc059a9e23ab4f13f0c8ed2`
(`docs(phase-4bn-ai): finalize merge closeout shas`).

## 3. Files created / modified

Created (committed):

- `src/prometheus/research/microstructure/pre_v002_fixed_baseline_run.py` — the
  fixed-baseline runner (loader + train-only standardizer + fit + eval + verdict +
  compact-artefact writer).
- `tests/research/microstructure/test_phase4bn_aj_pre_v002_fixed_baseline_run.py`
  — 23 offline synthetic-fixture tests.
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-aj_fixed-pre-v002-baseline-run-verdict.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-aj_closeout.md`.

No existing source module was modified. The three v002 baseline modules
(`ml_baseline_models_v002`, `ml_baseline_metrics_v002`, `ml_baseline_design_v002`)
and the Phase 4bn-AF/AH modules (`pre_v002_ml_dataset_contract`,
`pre_v002_ml_dataset_run`, `pre_v002_split_policy`) were **imported and reused**,
not edited.

Created (local, **gitignored, uncommitted**) — the single AJ result namespace
`data/research/microstructure/ml_baselines/pre_v002_fixed_baseline_v001/`: 9
compact JSON artefacts + 9 Phase 4bb-F `.sha256` sidecars (no model binaries, no
row-level predictions).

## 4. Exact documents / source inspected

- Phase 4bn-AE memo (§8 claim scope, §9 target interpretation, §10 dependence,
  §11–§12 block reporting, §13 metric registry, §14 calibration, §15 cost-realism,
  §16/§17 success/continue/kill, §18 arc budget, §19 strategy boundary).
- Phase 4bn-AH single-run report, closeout, merge-closeout; Phase 4bn-AI report,
  closeout, merge-closeout; Phase 4bn-AG memo; Phase 4bn-AF skeleton report.
- Committed source: `pre_v002_ml_dataset_contract.py` (AE constants + column
  allowlist + success thresholds + claim scope + mandatory metrics),
  `pre_v002_ml_dataset_run.py` (verified read path), `pre_v002_split_policy.py`
  (214/1/45/1/14 splits), `ml_baseline_models_v002.py` (majority / persistence /
  L2 / L1 pure-numpy suite + `StreamingEvaluator`), `ml_baseline_design_v002.py`
  (frozen SGD hyperparameters + cost lock), `ml_baseline_metrics_v002.py`
  (`CalibrationSummary`, `ClassBalance`, stability deltas).
- `docs/00-meta/current-project-state.md` (head; treated as authority, README not).

## 5. Exact AH artefacts read (read-only)

Under `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`:
`dataset_manifest.json`, `train_only_transform.json`, `split_index.json`,
`leakage_split_integrity_proof.json` (+ their four `.sha256` sidecars).

## 6. AH artefact reads were read-only

Confirmed. The runner opens the AH artefacts in read mode only and re-verifies
their sidecars. After the run, all four AH artefact SHA256 still match their
sidecars (byte-identical: `36a13213…`, `85f6ea35…`, `d1681acd…`, `e36c9163…`).
The AH namespace was **not** mutated.

## 7. Feature/label Parquet rows read — yes (authorized by this phase)

Yes. Under the Phase 4bn-AJ authorization ("may read only the already-authorized
pre-v002 local feature/label Parquet sources needed to run the fixed baselines"),
the runner read the AH-verified pre-v002 sources only:

- feature segment `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s`
  (275 partitions; manifest `4881eb87…`, feature_config_hash `0726b41d…`, gate
  `db731d1b…`);
- label segment `microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w`
  (275 partitions; manifest `69746c88…`, label_config_hash `b3bd5d2b…`, gate
  `ffb5b09…`).

No other source was read: **no v002 terminal window, no sealed test, no raw zip,
no external/authenticated/private source, no endpoint.** The v002-terminal config
hashes (`819cfa7a…` / `352bad41…`) are rejected by the reused
`builder.validate_manifest_hashes` binding.

## 8. Sidecar verification results

- Four AH artefacts: recomputed SHA256 == sidecar, canonical two-space, basenames
  match — **PASS** (before the run and byte-identical after).
- 550 per-Parquet sidecars (275 feature + 275 label): full byte-level re-hash +
  sidecar + manifest-inventory match via the reused
  `verify_per_parquet_sidecars_and_inventory` — **PASS** (275/275 partitions).
- Nine AJ output artefacts: canonical two-space `.sha256` sidecars written and
  re-verified — **PASS**.

## 9. AH proof preservation results

`leakage_split_integrity_proof.json` re-loaded read-only; all required flags hold:
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`test_rows_loaded = 0`; `no_random / no_shuffle / no_kfold / no_bootstrap = true`;
`no_embargo_date_used = true`; per-horizon boundary crossings all `0`;
`ml/diagnostics/strategy/signals/pnl/backtest/live/exchange_write_authorized =
false`. Preserved.

## 10. Dataset manifest / split index / train-only transform consistency

- Manifest: streamed 400,001,695; train raw/kept 304,816,127; embargo raw
  3,071,370; validation 68,578,296; holdout raw 23,535,902 / kept 23,535,860;
  holdout censored drop 42; no imputation — all reconcile. **The run re-derived
  train class counts `{-1:150,077,008; 0:3,590,082; 1:151,149,037}` by a full
  streaming pass and cross-checked them against the AH manifest (exact match) —
  fail-closed on any drift.**
- Split index: 275 dates; the fit/eval passes touched **0** embargo rows.
- Train-only transform: `fit_split = train`; 45-column feature-list hash equal
  across manifest / transform / proof (`8e705ba8…`); the runner **applies** these
  AH-fitted statistics (subtract train mean / divide by max(train std, 1e-8);
  booleans pass through; nulls → fixed 0.0) and refits nothing on
  validation/holdout.

Rows fit on `train`: **304,816,127**. Rows evaluated (train+validation+holdout):
**396,930,283**. Both equal the AH kept totals exactly.

## 11. Recovered Phase 4bn-AE pre-registration

**Baselines (§13/§18):** majority (modal train class); persistence
(`sign(rolling_log_return_past_window_15s)`, matched to the 15s horizon); linear =
**L2 multinomial-logistic softmax regression** — the single pre-registered linear
family, fit once with the **frozen** Phase 4bn-B constants (1 epoch, batch 8192,
lr 0.1, L2 strength 1e-4, grad-clip 10, seed 20260528). The L1 variant exists in
the committed suite but is **not** part of the AJ three-baseline set (running it
would be a second model family).

**Mandatory metrics (§13, 21):** majority accuracy/balanced-accuracy/macro-F1
floors; persistence baseline; accuracy; balanced accuracy; macro-F1; per-class
P/R/F1; confusion matrix; predicted-class distribution; zero-class prevalence;
predicted-zero rate; log-loss; Brier; calibration reliability table;
high-confidence-tail size/accuracy; train↔validation delta; validation↔holdout
delta; filtered-row date counts; dropped-rows-by-reason. Granularities: aggregate
/ UTC-month / UTC-date.

**Success/continue/kill (§16/§17), frozen:**
`SUCCESS_ACCURACY_UPLIFT_PP = 2.0` over **both** the majority and persistence
floors; `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP = 1.0` over the majority floor;
`SUCCESS_MACRO_F1_UPLIFT = 0.03` over the majority floor (the §16 v002 anchor
"+0.14 macro-F1" is exactly majority→L2); majority-of-blocks agreement (>50% of
validation date **and** month blocks); holdout must not reverse the sign of the
uplift; calibration-tail rule. KILL if any §16 clause; CONTINUE only if all;
otherwise INVESTIGATE_AMBIGUOUS.

**Claim scope (§8):** allowed = directional-information diagnostic / v002 small-lift
sign reproduction / calibration-tail assessment; forbidden = tradability,
profitability, strategy/execution viability, slippage/spread adequacy,
live/paper-shadow readiness, PnL, backtest validity, production suitability,
economic significance.

## 12. Baseline definitions used

Exactly the three above, reused verbatim from the committed `ml_baseline_models_v002`
pure-numpy implementations (`fit_majority_class_baseline`, `PersistenceBaseline`,
`build_l2_logistic_regression_trainer` → `SoftmaxTrainer`). Majority label =
**+1 (up)** — the modal pre-v002 train class.

## 13. Implementation summary

`pre_v002_fixed_baseline_run.py` re-verifies the AH artefacts + 550 Parquet
sidecars via the reused AH read path, runs a real Phase 4bn-L budget preflight
(D: ≥ 500 GiB; measured 1166.24), applies the AH train-only transform, then makes
**two streaming, bounded-memory passes**: a *fit pass* over the 214 train dates
(L2 SGD + re-derived train class counts) and an *eval pass* over all
model-eligible dates (majority / persistence / L2 predictions accumulated per
family × split × UTC-month × UTC-date, plus L2 calibration bins and a
`forward_log_return_15s` cost histogram). It excludes the two embargo dates, drops
invalid/censored/null rows exactly as AH did (never imputes a target), fits only
on `train`, and writes nine compact JSON artefacts + Phase 4bb-F sidecars to the
one gitignored AJ namespace. Fail-closed throughout; a one-run guard prevents
overwrite.

## 14. Run summary

Single controlled run, **2,822.8 s (~47.0 min)**. 275/275 partitions verified;
304,816,127 train rows fit (once); 396,930,283 rows evaluated (once). Each baseline
run exactly once. `test_rows_loaded = 0`; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; 0 embargo rows used. No rerun.

## 15. Resource / budget preflight

Real Phase 4bn-L preflight **PASSED** before any read (D: free 1166.24 GiB ≥ 500
GiB floor); live `assert_budget_during` (≥ 350 GiB) checked every 25 partitions.
The compact artefacts total ~0.4 MB. No full model matrix was materialized;
streaming/chunked design throughout (SGD batch 8192).

## 16. Aggregate metrics by baseline and split (15s)

Accuracy / balanced-accuracy / macro-F1:

| Split | Baseline | Accuracy | Balanced acc | Macro-F1 |
| --- | --- | --- | --- | --- |
| **validation** | majority (floor) | 0.49499 | 0.33333 | 0.22073 |
| | persistence (floor) | 0.51576 | 0.40128 | 0.40191 |
| | **L2 linear** | **0.54531** | **0.36892** | **0.36600** |
| **holdout** | majority | 0.50031 | 0.33333 | 0.22231 |
| | persistence | 0.51300 | 0.38002 | 0.38030 |
| | **L2 linear** | **0.54169** | **0.36456** | **0.36276** |
| **train** | majority | 0.49587 | 0.33333 | 0.22100 |
| | persistence | 0.50632 | 0.38824 | 0.38873 |
| | **L2 linear** | **0.53748** | **0.36253** | **0.36019** |

L2 uplift on **validation**: **+5.03 pp** accuracy over majority, **+2.96 pp** over
persistence; **+3.56 pp** balanced accuracy over majority; **+0.145** macro-F1 over
majority. Log-loss/Brier (validation): L2 0.7456 / 0.5109 vs majority 0.7602 /
0.5145 vs persistence 13.38 / 0.968 (persistence's one-hot hard outputs are
badly-calibrated by construction).

Per-class / distribution notes (mandatory, §13): the **flat/zero class** (validation
prevalence 1.48%) is essentially **never predicted by L2** (predicted-zero rate
1.3e-5; flat recall 6.4e-5) — the same degenerate behaviour Phase 4bn-B saw on
v002. Persistence *does* predict flat (validation flat recall 0.162), which is the
sole reason its macro-F1 (0.402) exceeds L2's (0.366); on the two **directional**
classes L2's per-class F1 is higher (down 0.534 vs 0.518; up 0.563 vs 0.524).

## 17. UTC month/date block metrics

Validation date-block agreement **1.000** and month-block agreement **1.000**
(L2 accuracy exceeds the majority floor in **every** evaluated validation date and
in **both** validation months): 2024-10 L2 0.5546 vs majority 0.4909; 2024-11 L2
0.5352 vs majority 0.4994. Holdout month 2024-11: L2 0.5417 vs majority 0.5003
(no reversal). Generalization deltas (L2): validation−train accuracy **+0.0078**
(validation slightly *better* than train → no overfitting); validation−holdout
accuracy **−0.0036** (small, no sign reversal). Full per-date tables are in the
gitignored `date_block_metrics.json`.

## 18. Calibration / confidence-tail results

L2 high-confidence tail (predicted proba ≥ 0.8) **beats the majority accuracy
floor on every split** — a notable difference from the v002 baseline (where the
tail sat at/below the floor):

| Split | tail size | tail accuracy | majority floor | beats floor |
| --- | --- | --- | --- | --- |
| validation | 914,670 | 0.6332 | 0.4950 | **yes** |
| holdout | 156,652 | 0.6589 | 0.5003 | **yes** |
| train | 8,716,089 | 0.6037 | 0.4959 | **yes** |

Caveat: the high-confidence bins are **overconfident** (negative reliability gaps,
e.g. validation 0.8–0.9 bin: mean predicted 0.843 vs empirical 0.589). Probabilities
are therefore usable for *ranking / confidence-gated diagnostic reading* but are
**not** well-calibrated in level. This licenses only §8(c) (calibration-tail
assessment), not any confidence-gated trading framing (§14/§19).

## 19. Cost-realism descriptive fields (§15; descriptive only)

`forward_log_return_15s` distribution was available during the authorized row-level
read. Validation split: median |return| **2.53 bps**, mean **3.84 bps**, p90 **9.66
bps**, p99 **23.0 bps**, max 180 bps. Share of 15s moves with |return| **> 16 bps
round-trip = 2.47%**; **> 8 bps one-way = 11.97%**. Holdout: > 16 bps = 1.20%;
train: comparable. **Interpretation (pre-registered, descriptive only):** only ~1
in 40 15s moves even *in principle* clears the locked 16 bps round-trip cost; the
15s horizon is **rarely economically relevant** at the locked cost. This is
**descriptive context only** — it defines no trading rule and is **not** a
tradability, edge, PnL, or economic-significance claim (§15/§19). It does **not**
kill the arc (the information-diagnostic question is answered).

## 20. Dependence caveat

Carried verbatim from AH: *"aggTrades 15s forward labels overlap heavily; rows are
NOT independent; per-row metrics are descriptive only and per-row significance
language is forbidden (Phase 4bn-AE Option 1)."* The ~397M rows are **not** ~397M
independent samples; the decision blocks are **275 UTC dates / 9 UTC months**. No
p-value / confidence-interval / significance language is used; the verdict rests on
**block agreement** (fraction of validation date/month blocks with positive
uplift), not on row-level metrics.

## 21. Verdict under the pre-registered criteria

**`CONTINUE_ONE_FOLLOWUP`** (Phase 4bn-AE §16). Every "all of" condition is met on
the frozen thresholds:

- L2 beats **both** floors on validation accuracy by ≥ +2.0 pp (majority **+5.03**,
  persistence **+2.96**) **and** macro-F1 over the majority floor by ≥ +0.03
  (**+0.145**); ✓
- internal-holdout dry-run does **not** reverse the sign (holdout L2 +4.1 pp over
  majority); ✓
- improvement present in a **majority** of validation blocks — in fact **all**
  (date agreement 1.000, month agreement 1.000); ✓
- calibration is usable (high-confidence tail beats the majority floor on all
  splits); ✓
- cost-descriptive statistics acknowledged (signal understood as **not tradable**
  at 15s, retaining information-diagnostic value only). ✓

No KILL clause fired (`kill_reasons = []`). This **reproduces the v002 small-lift
sign** on the larger, earlier pre-v002 regime (+5.03 pp accuracy vs v002's +5.0 pp;
+0.145 macro-F1 vs v002's +0.14) with stronger block-stability and — unlike v002 —
a high-confidence tail that beats the floor.

**Recorded interpretation caveat (not a softening):** `CONTINUE_ONE_FOLLOWUP` and
`INVESTIGATE_AMBIGUOUS` differ only in whether the §16 macro-F1 clause is read as
"over the majority floor" (adopted here, matching the KILL clause's explicit
majority-floor reference and the §16 "+0.14 macro-F1" v002 anchor) or as "over both
floors" (under which L2's 0.366 < persistence's 0.402 — driven entirely by the
degenerate flat class — would yield `INVESTIGATE_AMBIGUOUS`). **Both readings lead
to the identical next action:** a separately-authorized Phase 4bn-AK arc-decision
memo, default posture *remain paused*, no successor authorized here. This report
does not resolve that arc question; §17/§18 place it at Phase 4bn-AK.

## 22. Claims allowed by this result (§8, exhaustive)

- **(a)** the 45 causal aggTrades features contain **short-horizon directional
  information** about `forward_direction_15s` on the pre-v002 segment (L2 clears
  every statistical floor, stably across all validation blocks, with no
  overfitting);
- **(b)** the **directional sign** of the v002 small-lift result **is reproduced**
  on the larger, earlier pre-v002 regime;
- **(c)** the probability outputs' **calibration/confidence tail** beats the
  majority floor on accuracy but is overconfident in level — usable for
  ranking/diagnostic reading, not as calibrated probabilities.

## 23. Forbidden claims (must not be inferred from this result)

Tradability; profitability; strategy viability; execution viability;
slippage/spread adequacy; live/paper-shadow readiness; PnL; backtest validity;
production suitability; economic significance. The 2.47%-of-moves-clear-cost figure
is descriptive context, **not** evidence of edge. The 15s strict-sign target is
non-economic (§9) and may embed bid-ask-bounce (aggTrades-only, no mid/book).

## 24. Validation commands and results

- `pytest test_phase4bn_aj…` → **23 passed**; combined with AF+AH → **146 passed**
  (23 AJ + 97 AF + 26 AH), no regression.
- `ruff check` (new module + test) → **All checks passed**.
- `mypy` (new module) → **0 direct errors**; residual errors are pre-existing in
  imported v002 sibling modules (`ml_baseline_models_v002` / `_metrics_v002` and
  the AH module) under `strict=true` (bare-`np.ndarray` convention), unmodified by
  this phase.
- `git diff --check` → clean.
- Budget preflight → **PASSED** (D: 1166.24 GiB).
- AH namespace re-hash → 4/4 byte-identical (unmutated).
- AJ namespace → 9 artefacts + 9 sidecars verify; `git check-ignore` → `.gitignore:88`;
  `git ls-files …/pre_v002_fixed_baseline_v001/` → 0 tracked.
- `git ls-files data/microstructure/ data/research/` → 0 tracked.

## 25. Git status

Only the two new source/test files and the transient `?? .claude/scheduled_tasks.lock`
are untracked before commit; the AJ data namespace is gitignored and not shown. No
data staged. Final committed SHA(s) in the closeout and final operator report.

## 26. Baseline reruns

**None.** Each baseline ran exactly once; the one-run guard refuses overwrite. No
result-seeking rerun occurred.

## 27. Local AJ output namespace

Created: `data/research/microstructure/ml_baselines/pre_v002_fixed_baseline_v001/`
— exactly one namespace, **gitignored (`.gitignore:88`), uncommitted**. 9 compact
JSON result/proof artefacts + 9 canonical `.sha256` sidecars. **No model binaries;
no row-level predictions** (only aggregate/block/histogram summaries). The AH
namespace was not mutated.

## 28. Explicit boundary confirmations

- no AH rerun; no AH namespace mutation (4/4 byte-identical after run); ✓
- no v002 terminal read; no sealed test touch; `test_rows_loaded = 0` preserved; ✓
- no unregistered models (exactly majority / persistence / L2); no model selection;
  no hyperparameter search (frozen constants); no feature selection; no threshold
  optimization; ✓
- no strategy / signals / PnL / backtest; no Sharpe / trading hit-rate; ✓
- no paper / shadow / live; no exchange-write; no credentials; ✓
- no eligibility / manifest / gate / sidecar mutation; `flip_research_eligible(...)`
  never invoked; ✓
- no data acquisition / endpoint / raw-zip read; each baseline run once; ✓

## 29. Remaining blockers before Phase 4bn-AK arc-decision

Separate operator authorization of Phase 4bn-AK (not granted here). Phase 4bn-AK is
the pre-registered locus (§17/§18) to either close the arc or authorize **exactly
one** bounded follow-up from §16 (a) longer-horizon label memo, (b) bookTicker /
mid-price data-admissibility memo, (c) block-bootstrap inference framework, (d) one
fixed-capacity model-comparison memo — each itself separately authorized.

## 30. Remaining blockers before any strategy / PnL / backtest / live path

Absolute (§19): a separate future **M0-style mechanism-admissibility memo** clearing
M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution feasibility,
slippage/spread (which aggTrades-only data cannot currently support — mid/book data
required), label economic relevance (the 15s strict-sign target is non-economic),
strategy admissibility against the retained rejections, and the Phase 4al no-rescue
constraints — **plus** separate operator authorization for each of strategy /
signals / PnL / backtest / paper-shadow / live / exchange-write. No AJ result
softens this boundary.

## 31. Recommended next state

**Remain paused.** No successor authorized from within Phase 4bn-AJ. The result is
recorded; the arc decision is deferred to a separately-authorized Phase 4bn-AK.

## Result state

`FIXED_PRE_V002_BASELINE_RUN_RECORDED__PRE_REGISTERED_VERDICT_RECORDED__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`
