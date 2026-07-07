# Phase 4bn-AE — ML Baseline Pre-Registration + Contract Amendment Memo

## 1. Purpose

This memo pre-registers the **evaluation and interpretation layer** for the first
pre-v002 ML baseline, and **amends** the Phase 4bn-AC ML dataset contract
(`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`) accordingly,
**before** any code-only ML dataset builder skeleton is authorized or written.

It exists because a code-only skeleton, if authorized against the current
Phase 4bn-AC contract, would encode an **incomplete** contract: the contract
locks the source scope, split, target, feature allowlist, filtering, alignment,
leakage-proof, and budget-preflight obligations, but it does **not** specify (a)
what the first baseline may and may not claim, (b) how the heavy statistical
dependence of overlapping 15s forward labels must be handled, (c) which metrics
are mandatory and how they must be sliced by time, (d) how calibration and the
confidence tail must be reported, (e) how the locked 16 bps round-trip cost
bounds interpretation, (f) pre-registered success / continue / kill criteria
declared before any result is seen, or (g) a finite arc budget with a
stopping-rule posture. This memo records exactly those rules so that a later
skeleton encodes the **amended** contract, and so that a later baseline result
is interpreted against **pre-declared** criteria rather than post-hoc.

This phase is **docs-only**. It reads no local data, creates no local data, adds
no code / tests / scripts, creates no split file / research matrix / ML dataset /
ML config / manifest / gate report / sidecar, transitions no manifest field, and
authorizes no successor. It amends a contract the way an amendment amends a
specification: future tooling and future evaluation must obey it, but nothing is
built or run here.

**Framing (critical):** Phase 4bn-AE does **not** replace Phase 4bn-AC. The
Phase 4bn-AC contract remains the **source contract** for source scope, split,
target, features, filtering, alignment, leakage proof, and budget preflight.
Phase 4bn-AE **adds** a pre-registered evaluation / interpretation / decision
layer **on top of** Phase 4bn-AC and carries it forward as version
`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001` **amendment 001**
(docs-level version tag only; no config or manifest is created or set).

---

## 2. Authority and repository state

- **Authorized by:** the operator, following the Phase 4bn-AD decision
  `RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  and a subsequent independent external strategic review (recorded in §5) that
  recommended inserting one docs-only pre-registration phase before the skeleton.
- **Branch:** `phase-4bn-ae/ml-baseline-preregistration-contract-amendment`.
- **Base `main` SHA:** `925592961c824cd28c1115710f674b0debef753d`
  (`docs(phase-4bn-ad): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 92559296…` verified.
- **Predecessor chain on `main`:** Phase 4bn-AD SHA-finalization `9255929`,
  merge-closeout `c4880c2`, merge `3b659f1`, branch `ddb9871`; Phase 4bn-AC
  finalization `0331aea` present.
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Gitignored namespaces:** `data/microstructure/` (`.gitignore:85`),
  `data/research/` (`.gitignore:88`).
- **Working-tree:** only the expected untracked transient
  `.claude/scheduled_tasks.lock`.

---

## 3. Phase type and strict scope

- **Phase type:** docs-only / ML baseline pre-registration / contract amendment /
  evaluation design / dependence policy / success-kill criteria / no-data-read
  memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3, because it amends the
  already-recorded Phase 4bn-AC contract before implementation. It defines the
  evaluation rules, dependence handling, success/continue/kill criteria,
  regime-sliced reporting, economic-interpretation boundaries, and arc-budget
  posture that any later code-only skeleton and data-reading builder must obey.
  If this phase is wrong or omitted, later code may encode an incomplete contract
  and future results may be interpreted post-hoc.

**Strict scope (all enforced):** no code, no tests, no scripts, no data read, no
data created, no inspection of any file under `data/microstructure/` or
`data/research/`, no inspection of raw zip / normalized / feature / label Parquet
/ manifest / gate report / sidecar, no v002-terminal read, no sealed-test read,
no split file, no research matrix, no ML dataset, no ML config, no manifest, no
gate report, no sidecar, no training, no scoring, no prediction, no diagnostics,
no strategy / signals / PnL / backtests, no `research_eligible` flip, no
`eligibility_gate_status` transition, no `chronological_split_policy` set, no
invocation of the Phase 4aw `flip_research_eligible(...)` always-raises
invariant, no successor authorization.

---

## 4. Evidence base and input boundary

This memo was written from **committed docs + committed source/tests only**. No
local artefact under `data/microstructure/` or `data/research/` was read or
inspected. The README is treated as potentially stale and is **not** used as a
current-state authority.

Committed source grounding (read-only, for pre-registration precision):

- `src/prometheus/research/microstructure/pre_v002_split_policy.py` — the Phase
  4bn-AA split artefact (214 / 1 / 45 / 1 / 14 windows, boundary timestamps,
  allowed horizons).
- `src/prometheus/research/microstructure/features_schema_v002.py` /
  `features_schema.py` — the 45 causal computed feature columns and the
  forbidden-substring guard.
- `src/prometheus/research/microstructure/labels_schema_v002.py` — the 40-column
  label schema, the four horizons, `DIRECTION_THRESHOLD_POLICY_V002`
  (strict-sign, no deadband), and the null/censoring policy.
- `src/prometheus/research/microstructure/ml_baseline_design_v002.py` — the Phase
  4bn-B locked design constants (frozen 45-column matrix, excluded lineage
  columns, `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`, train-only transform rules,
  3-class signed framing, non-authorization flags) — reused **as
  column/contract precedent only**; identity-bound to the v002 terminal and
  **not** the pre-v002 binding.
- `src/prometheus/research/microstructure/ml_baseline_dataset_v002.py` — the
  v002-terminal-bound data-reading loader; **inadmissible** to pre-v002; not
  reused.

Committed docs grounding: the process standards
(`merge-closeout-standard`, `phase-risk-tiering-standard`,
`phase-workflow-standard`, `phase-prompt-template`, `operator-report-standard`);
the Phase 4bn-Y / Z / AA / AB / AC / AD implementation reports and closeouts; and
the Phase 4bn-A / B / C ML-baseline design, implementation, and
evidence-interpretation reports.

**Carried-forward numeric evidence** (from committed reports; not re-derived by
reading data here). The Phase 4bn-B / 4bn-C **v002-terminal** baseline (a
different segment and a different split from the pre-v002 first baseline this
memo pre-registers) produced, on the **v002 validation split**, at the **15s**
horizon:

- majority-class accuracy floor **0.4938**; majority macro-F1 floor **~0.2204**
  (the majority baseline predicts one class only); majority balanced accuracy
  **0.3333**.
- L2 multinomial logistic accuracy **0.5435** (**+~5.0 pp** over the majority
  floor); balanced accuracy **0.3654** (**+3.2 pp**); macro-F1 **0.3638**
  (**+0.1434**); L1 essentially identical to L2 at the metric level.
- train − validation deltas **~−0.005** (no overfitting at the descriptive
  level).
- persistence beats majority on hard accuracy by **+2.3 pp** at 15s but is
  **~18×** worse on log-loss and **~2×** worse on Brier (hard one-hot outputs are
  uncalibrated).
- calibration: **~86%** of L2-15s validation predictions fall in the 0.5–0.6
  confidence bin and that bin is well-calibrated; the **high-confidence tail is
  badly miscalibrated** — at claimed 0.84–0.94 confidence (~178K rows) empirical
  accuracy is **0.49–0.55**, i.e. **at or below the majority floor**, and the
  0.8–0.9 bin sits **below** the floor.
- the **flat / zero class** (prevalence **0.15–1.09%**) is **never predicted** by
  the L1/L2 models (per-class P/R/F1 = 0/0/0 in every cell).
- at **60s** the accuracy lift shrinks to **+~1.5 pp** and predictions become
  strongly down-biased (38.8M `pred_down` vs 18.0M `pred_up`).

These numbers are the empirical anchor for the pre-registered thresholds in §16
and the calibration policy in §14. They describe the **v002** segment; the
pre-v002 first baseline is a **different, larger, earlier** segment on a
**different split**, and the whole point of pre-registration is to declare the
decision rule before its numbers exist.

---

## 5. External strategic-review finding carried forward

An independent external strategic review was conducted after Phase 4bn-AD. It is
recorded here as the motivation for this phase; it is advisory, not authoritative
over the project locks. Its load-bearing findings:

1. The code-only skeleton is **safe and useful**, but **premature by one
   docs-only phase**, because the Phase 4bn-AC contract lacks a pre-registered
   evaluation / interpretation / decision layer.
2. The contract lacks **pre-registered success / kill criteria**; without them
   the first baseline would, like the v002 baseline, end in a post-hoc
   "small but real lift" interpretation with no falsifiable decision.
3. The contract lacks an **overlapping-label dependence policy**: 400,001,695
   event rows are **not** 400,001,695 independent samples, because each row's 15s
   forward label overlaps hundreds of neighbouring rows' labels. Per-row sample
   size is not evidential; per-row significance language would be invalid by
   orders of magnitude.
4. `forward_direction_15s` (strict sign at zero, aggTrades-only) is a useful
   **information / pipeline diagnostic** target but must **not** be treated as
   economic evidence: with trades only, the forward return is measured
   last-trade-to-last-trade and can embed **bid-ask bounce**, so part of any lift
   may be untradeable bounce prediction rather than mid-price movement.
5. The locked **16 bps round-trip** cost means any short-horizon direction signal
   must be interpreted against a cost the signal almost certainly cannot clear at
   15s; cost-realism must be reported descriptively.
6. The single validation / internal-holdout layout is **regime-narrow** (it sits
   on the Oct–Nov 2024 window) and must require **regime / monthly / subperiod**
   reporting rather than one aggregate metric.
7. The project should **pre-declare** what result would continue, kill, or
   redirect the ML arc **before** seeing pre-v002 results.
8. **No** result of the first baseline, however strong, should authorize
   strategy, signals, PnL, or backtests without a separate future **M0-style**
   memo clearing cost realism and strategy admissibility.
9. The future code-only skeleton should encode the **amended** evaluation
   contract, not the current incomplete one.

The review also flagged that `current-project-state.md` is a broken
single-source-of-truth (2.7 MB; stale tail dated 2026-04-29; phase blocks
inserted mid-file) and recommended a compact-state-consolidation phase. That is
**out of scope** for this amendment but is carried into §25 / §30 as a
recommended near-term docs-only successor option.

This memo **adopts findings 1–9** and encodes them below. It does **not** adopt
any part of the review that would authorize data reads, new acquisition, or any
loosening of the locks; the review has no such authority.

---

## 6. Phase 4bn-AC contract carried forward

The Phase 4bn-AC contract is carried verbatim as the source contract. Unchanged
by this amendment:

- **Contract name:** `microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`.
- **Source:** BTCUSDT / Binance USDⓈ-M futures / aggTrades.
- **Segment:** pre-v002 only, 2024-03-01 .. 2024-11-30 inclusive UTC (275 dates;
  400,001,695 rows by reference).
- **Feature source:** Phase 4bn-S segment (manifest `4881eb87…9b52`;
  `feature_config_hash 0726b41d…114c`; feature-layer gate `db731d1b…6ab08`
  27/27).
- **Label source:** Phase 4bn-W segment (manifest `69746c88…b161`;
  `label_config_hash b3bd5d2b…8970`; label-layer gate `ffb5b092…8984` 40/40).
- **Normalized lineage:** Phase 4bn-O (manifest `0e96ae37…d9fa`;
  normalized-layer gate `3452fd9d…f134` 25/25) by reference.
- **Split policy:** Phase 4bn-AA `pre_v002_split_policy.py`
  (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; train
  2024-03-01..2024-09-30 = 214; embargo 2024-10-01; validation
  2024-10-02..2024-11-15 = 45; embargo 2024-11-16; internal holdout / dry-run
  2024-11-17..2024-11-30 = 14).
- **Primary target:** `forward_direction_15s`, 3-class signed `{-1, 0, +1}`, zero
  class preserved, per `DIRECTION_THRESHOLD_POLICY_V002` (strict sign at zero; no
  deadband; no threshold optimization).
- **Feature allowlist:** exactly the 45 causal computed `FEATURE_SCHEMA_V002`
  columns.
- **Forbidden columns, filtering, alignment, execution order, train-only
  transforms, leakage proof, budget preflight, output namespace, non-authorization
  boundaries:** all as Phase 4bn-AC §9–§21, unchanged.
- **Admissibility posture (Phase 4bn-AB):** `source_admissible_for_dataset_contract
  = true`; `source_admissible_for_data_read = false`;
  `source_admissible_for_dataset_builder = false`; `ml_authorized = false`;
  `diagnostics_authorized = false`; manifest `research_eligible = false`;
  `eligibility_gate_status = pending`; `chronological_split_policy = not set`.

This amendment changes **none** of the above. It adds §8–§20 below.

---

## 7. Pre-registration question

This memo answers, by reference only and before any result exists:

1. Should the pre-v002 first baseline remain `forward_direction_15s`? — **Yes**
   (§9), reframed explicitly as an information diagnostic.
2. What is its exact interpretation, and what may it and may it not claim? — §8,
   §9.
3. How must overlapping 15s label dependence be handled? — §10.
4. What time-block reporting is mandatory, and is decimation used? — §10, §11.
5. What regime / subperiod reporting is required? — §12.
6. Which metrics are pre-registered as mandatory? — §13.
7. What calibration / confidence-tail checks are mandatory? — §14.
8. What cost-realism descriptive checks are mandatory? — §15.
9. What thresholds define continue / kill / investigate? — §16, §17.
10. What is the finite arc budget and stopping-rule posture? — §18.
11. What is the strategy / PnL / backtest hard boundary? — §19.
12. What must a future code-only skeleton encode from this amendment? — §20.

---

## 8. Evaluation claim scope

The first pre-v002 ML baseline, **if and when it is ever separately authorized,
built, and run**, may claim **only**:

- **(a)** whether the existing 45 causal aggTrades feature set contains
  **short-horizon directional information** about the selected label on the
  pre-v002 segment;
- **(b)** whether the **directional sign** of the v002 small-lift result
  (linear models beat the majority and persistence floors on hard accuracy /
  macro-F1) is **reproduced** across the larger, earlier pre-v002 regime span, or
  is **not** reproduced;
- **(c)** whether the **calibration / confidence-tail** behaviour of the
  probability outputs is adequate, marginal, or fails (carrying forward the v002
  finding that high-confidence bins did not beat the majority floor).

The first baseline may **not** claim, imply, or be cited as evidence of:

- tradability;
- profitability;
- strategy viability;
- execution viability;
- slippage / spread adequacy;
- live-readiness;
- paper / shadow readiness;
- PnL of any kind;
- backtest validity;
- production suitability;
- economic significance of any effect size.

Any report, closeout, or state update that states a baseline result **must**
restate this claim scope and must not exceed it. A result that beats every
statistical floor still licenses **only** claim (a)/(b)/(c), never an economic or
strategy claim (see §19).

---

## 9. Target interpretation amendment

**Decision: the active first-baseline target remains `forward_direction_15s`.**
No conflict with the Phase 4bn-AC contract was found; the target is retained. But
the amendment records its interpretation explicitly:

- It is a **first-baseline information-diagnostic target**. Its purpose is to
  probe whether the frozen 45-feature aggTrades set carries any short-horizon
  directional information, and whether that information survives the larger
  pre-v002 regime span.
- It is **not an economic target.** A strict-sign-at-zero 15s direction says
  nothing about whether a move is large enough to clear cost.
- It is **not a strategy label.** No entry/exit/position/PnL semantics attach to
  it.
- It is **not a PnL label.**
- It **may contain last-trade-to-last-trade / bid-ask-bounce artifacts** because
  **only aggTrades are available** and no mid-price / order-book data exists in
  the segment. A classifier fed aggressor-flow features can, in principle, beat
  the majority floor partly by predicting which side of the spread the next
  trades print on — an effect with **zero** mid-price movement and therefore
  **zero** economic content. The first baseline **cannot** decompose bounce from
  genuine directional prediction with aggTrades alone; this limitation must be
  stated in any result report.
- The strict-sign, no-deadband, zero-preserving definition is **retained as
  anti-tuning discipline** (it forbids threshold optimization), but it is
  **acknowledged** that it makes the target dominated by sub-basis-point,
  frequently bounce-driven moves, and that the rare exact-zero "flat" class
  (v002 prevalence 0.15–1.09%) is a tick-structure artifact that no baseline
  predicted.

**Any economically anchored target** — a cost-anchored deadband label
(e.g. `|forward_log_return_15s| > 16 bps`), a mid-price label, a triple-barrier /
target-before-stop label, an MFE/MAE/R-multiple label, a longer-horizon
(5m/30m/1h) label, or any volatility-scaled label — is **out of scope for this
contract and this first baseline**. Each would require a **separate future
contract revision** and, in most cases, **new data or new labels** (mid-price /
book data, or a new label-layer build), each separately authorized. This memo
**does not** authorize any of them; it merely records that they are the correct
locus for economic questions, not the 15s strict-sign target.

The horizon remains **15s** as the single first-baseline horizon (1s/5s/60s
contract-known, model use deferred). This memo records that the Phase 4bn-AC
rationale for 15s-over-60s (terminal-censor counts 42 vs 216 out of 400M rows) is
a **negligible** coverage argument and should **not** be presented as a
substantive basis; the honest reasons to prefer a single short horizon here are
(i) comparability with the v002 15s baseline for the sign-reproduction check
(claim (b)), and (ii) 15s is less tie/noise-dominated than 1s/5s. Longer horizons
are where cost could plausibly be cleared and are the correct subject of a future
label memo, not this baseline.

---

## 10. Overlapping-label dependence policy

This is a **mandatory** evaluation policy binding on any future evaluator and on
the code-only skeleton's interface reservations.

**Problem.** aggTrades on BTCUSDT arrive at high frequency; each row's 15s
forward window overlaps the forward windows of hundreds of neighbouring rows.
The label series is therefore **heavily autocorrelated**. The 400,001,695 rows
contain **far fewer** effectively independent observations than their count
suggests. Per-row metrics remain arithmetically valid as **descriptive
summaries**, but **any inferential statement** ("the lift is real / significant")
that treats rows as independent is invalid by orders of magnitude.

**Selected policy — Option 1 (date/month-block aggregation; no data-derived
decimation).**

- **Row-level metrics are descriptive only.** They may be reported. They must
  never be used as the sole basis for a continue/kill decision and must never be
  accompanied by per-row significance / confidence-interval / p-value language.
- **The unit of decision evidence is the time block, not the row.** Required
  decision metrics are computed **per UTC date** and aggregated **per UTC month**,
  within each split. Continue / kill criteria (§16) require evidence **across
  date/month blocks**, not aggregate row-level metrics.
- **The future evaluator must report**, for each split: row counts and **date
  counts**; per-UTC-date metric summaries; per-UTC-month metric summaries; and an
  explicit **effective-sample caveat** stating that rows are not independent and
  that block-level evidence governs the decision.
- **No statistical-significance language** (p-values, confidence intervals,
  "significant") may be used **unless** a future separately-authorized phase
  first defines a dependence-aware inference method (e.g. a **block bootstrap** or
  **block/date-level jackknife** over non-overlapping date blocks). Until then,
  evidence is reported as **descriptive block agreement** (e.g. "the accuracy
  lift over the majority floor is positive in K of N evaluated validation dates
  and in M of P evaluated validation months"), not as significance.

**Why not Option 2 (fixed decimation / stride) as the primary policy.** A fixed
decimation stride that reduces overlap cannot be pre-registered honestly without
knowing the segment's trade-arrival rate, and pre-committing a stride blindly
risks either under-thinning (dependence remains) or over-thinning (discarding
regime coverage). Option 2 is therefore **reserved, not selected**: a future
phase **may** add a fixed, justified decimation/stride **on top of** Option 1 if
it can be pre-registered from committed evidence (e.g. from the descriptive
dataset-diagnostics phase §18 Phase 4bn-AH, which would measure arrival rate
without training anything). If ever adopted, the stride must be an **explicit
pre-registered constant with a written justification**, applied **before**
evaluation, and it must **never** be tuned to change a result. This memo does
**not** adopt a stride.

---

## 11. Date-block / month-block reporting policy

Binding on any future evaluator and reserved as skeleton interface schema:

- Every reported metric (§13) must be emitted at **three granularities**:
  **aggregate** (per split), **per UTC month** (within split), and **per UTC
  date** (within split), except where a metric is only meaningful at aggregate
  scale (e.g. a single confusion matrix may be aggregate + monthly).
- Each split's report must include **row counts and date counts** at each
  granularity, **before and after** target filtering (null / censored / invalid
  drops, §13 of Phase 4bn-AC).
- The report must include the **date inventory** actually evaluated per split
  (from `pre_v002_split_policy.policy_date_inventory`), so that missing or
  short dates are visible.
- **No single aggregate metric may be used alone** for a continue / kill /
  investigate decision (§16). The decision is a function of block-level agreement.
- The evaluator must record the **effective-sample caveat** (from §10) adjacent
  to every aggregate metric.

**Honest limitation recorded now:** the pre-v002 split places **validation**
entirely within 2024-10-02 .. 2024-11-15 and the **internal holdout** within
2024-11-17 .. 2024-11-30. Both decision windows fall in the **same ~2-month
late-2024 regime**. Monthly slicing of the **decision** windows therefore spans
at most Oct-2024 + partial Nov-2024 (validation) and partial Nov-2024 (holdout) —
this is **regime-narrow**, and cross-month agreement within validation is a
**weak** regime-robustness test. To partially compensate, the evaluator must
**also** report **descriptive per-month train-split metrics** across
Mar–Sep 2024 (7 months). Train metrics are **not** a generalization test and
**cannot** be used for continue/kill by themselves, but their **month-to-month
stability** is descriptive evidence of whether the feature-set's directional
signal is regime-stable or regime-specific. This limitation is a reason the
continue bucket (§16) is deliberately conservative and the "investigate" bucket
(§17) is broad.

---

## 12. Regime / subperiod reporting policy

Future reports (evaluator or diagnostics) must show, at minimum:

- **train / validation / internal-holdout date counts** (214 / 45 / 14) and the
  embargo dates dropped (2024-10-01, 2024-11-16);
- **monthly row counts** per split;
- **monthly target-class distribution** per split (down / flat / up shares),
  including the **flat/zero-class prevalence** per month;
- **monthly supervised-row counts after filtering** (post null / censored /
  invalid drops) per split;
- **monthly metrics** for validation and internal holdout (where a month has
  enough evaluated dates to be meaningful);
- **validation split metrics** as a whole **and** by month;
- **internal-holdout dry-run metrics** as a whole **and** by month, with the
  standing reminder that the holdout is a **one-time dry-run** — never used for
  model selection, hyperparameter tuning, threshold tuning, feature selection, or
  final/strategy/production claims;
- **descriptive train-split monthly metrics** (Mar–Sep 2024) per §11.

No continue/kill decision may rest on a single aggregate figure; the decision
must reference the block/month pattern.

---

## 13. Metric registry

The following metrics are **pre-registered as mandatory** for any future
pre-v002 baseline evaluation. Reporting a subset, or cherry-picking one metric,
is a **contract violation**. All are computed on **validation** and **internal
holdout**, at aggregate / monthly / date granularity per §11, and descriptively
on **train** per §11–§12. None are computed on the sealed test
(`test_rows_loaded = 0`).

**Floors / references (mandatory):**

- **majority-class accuracy floor** (predict the modal class);
- **majority-class balanced accuracy** and **majority-class macro-F1** floors;
- **persistence baseline** (sign of the past-window return), reported on the same
  metrics, since the contract's feature set includes
  `rolling_log_return_past_window` and the v002 baseline ran persistence.

**Classification metrics (mandatory):**

- **accuracy**;
- **balanced accuracy**;
- **macro-F1**;
- **per-class precision / recall / F1** for each of `{-1, 0, +1}` (down / flat /
  up);
- **confusion matrix** (aggregate and monthly);
- **predicted-class distribution** (to detect degenerate single-class prediction,
  as the v002 60s model exhibited);
- **zero-class prevalence** (true) and **predicted zero-class rate** (the v002
  models never predicted flat — this must be surfaced, not hidden).

**Probabilistic metrics (mandatory where a model emits calibrated
probabilities):**

- **log loss**;
- **Brier score**;
- **calibration / reliability table** (confidence bins vs empirical accuracy);
- **high-confidence-tail size and accuracy** (see §14).

**Generalization-gap metrics (mandatory):**

- **train − validation deltas** and **validation − internal-holdout deltas** for
  accuracy, balanced accuracy, macro-F1, log loss (where defined). A holdout that
  **reverses the sign** of the validation uplift is a kill signal (§16).

**Counts (mandatory):**

- **row counts and date counts after filtering**, by split and month;
- **dropped-row counts by split and reason** (null / censored / invalid), from
  the Phase 4bn-AC §13 filtering.

The evaluator must present floors and model metrics **side by side** so that
every model figure is read against its floor.

---

## 14. Calibration / confidence-tail policy

The single most decision-relevant v002 finding was that **confident predictions
were no better than the majority floor**. This policy makes that check
mandatory and pre-registered.

Any future evaluation whose model emits probabilities must report:

- **confidence bins** (at least deciles, plus an explicit high-confidence tail
  bin ≥ 0.8);
- **empirical accuracy by bin**;
- **predicted confidence vs empirical accuracy** (reliability curve) per split
  and per month;
- **high-confidence-tail size** (row count with predicted confidence ≥ 0.8) and
  **empirical accuracy in that tail**;
- **whether each high-confidence bin beats the majority accuracy floor** — a
  boolean, pre-registered as a first-class output, not buried;
- an explicit verdict field: probabilities are **usable**, **ranking-only**, or
  **unusable**.

**Pre-registered calibration rule.** If the high-confidence tail (≥ 0.8) does
**not** exceed the majority accuracy floor by a positive margin, the probability
outputs are declared **unusable for confidence-gated interpretation**, and any
"trade only when confident" framing is **pre-emptively rejected** (the v002
evidence already refutes it). This is a **kill contributor** (§16), not on its
own a full kill, because classification lift can be real even when probability
calibration is poor — but an unusable-calibration finding **caps** the claim at
§8(a)/(b) and forbids §8(c)-positive language.

---

## 15. Cost-realism descriptive reporting policy

The project locks §11.6 = **8 bps per side**, round-trip = **16 bps**. This
policy makes cost context a **mandatory descriptive** part of any baseline
report. It is **descriptive only**: it defines **no** trading rule, authorizes
**no** cost-aware label, and authorizes **no** PnL or backtest.

Required descriptive reporting (computed on the dataset's already-present
`forward_log_return_15s` support column, by reference — no new label, no new
computation authorized beyond summary statistics):

- the **distribution** of `forward_log_return_15s` by split and by month
  (at least: median absolute value, and selected quantiles);
- the **share of rows** where `|forward_log_return_15s|` exceeds **16 bps**
  (round-trip cost) — the fraction of 15s moves that could **even in principle**
  clear round-trip cost;
- optionally, the **share of rows** where `|forward_log_return_15s|` exceeds
  **8 bps** (one-way), if judged useful.

Interpretation rule (pre-registered): if the share of rows with
`|forward_log_return_15s| > 16 bps` is **very small** (which the segment's
microstructure makes highly likely at 15s), the report must state plainly that
**the 15s horizon is almost never economically relevant at the locked cost**, and
that the baseline's value is therefore confined to the **information-diagnostic**
claims of §8. This does **not** by itself kill the arc (the diagnostic question
remains answerable), but it **forecloses** any economic reading of the result and
feeds the §16 kill bucket only in combination with a failed information
diagnostic.

This section authorizes **no** cost-aware label, **no** deadband target, **no**
threshold, **no** PnL, and **no** backtest. Those require a separate future
M0-style memo (§19).

---

## 16. Success / continue / kill criteria

Pre-registered **before any pre-v002 result exists.** All thresholds are stated
as **minimum margins over the matched majority-class floor** on the **pre-v002
validation split** (45 dates, 2024-10-02..2024-11-15), corroborated by the
**internal-holdout dry-run** (14 dates) and by **date/month-block agreement** per
§10–§12. Row-level aggregate metrics alone are never sufficient.

Thresholds are deliberately **conservative but not impossible**, anchored to the
v002 evidence (which showed +~5 pp accuracy / +0.14 macro-F1 at 15s on its own
split): a genuine, regime-stable signal should clear them; a marginal or
regime-specific artifact should not.

**KILL / CLOSE-THE-ML-ARC** — record `CLOSE_ML_BASELINE_ARC` if **any** of:

- the model does **not** beat **both** the majority and the persistence floors on
  validation accuracy by at least **+2.0 pp**; **or**
- balanced accuracy does not improve over the majority floor by at least
  **+1.0 pp**, **and** macro-F1 does not improve by at least **+0.03** absolute
  (both fail); **or**
- the aggregate improvement is **concentrated in a single month / a minority of
  evaluated date-blocks** and disappears in the date/month summaries (i.e. it is
  regime-specific, not a stable feature-set signal); **or**
- the internal-holdout dry-run **reverses the sign** of the validation uplift on
  accuracy or macro-F1 (materially, beyond noise); **or**
- calibration is **unusable** (high-confidence tail ≤ majority floor, per §14)
  **and** classification lift also fails the accuracy/macro-F1 margins above; **or**
- the cost-descriptive statistics (§15) show the horizon is **almost never
  economically relevant** **and** the information-diagnostic lift also fails the
  margins above (no diagnostic value remains).

**CONTINUE TO EXACTLY ONE LIMITED FOLLOW-UP** — record `CONTINUE_ONE_FOLLOWUP`
only if **all** of:

- the model beats **both** floors on validation accuracy by at least **+2.0 pp**
  **and** on macro-F1 by at least **+0.03** absolute; **and**
- the internal-holdout dry-run **does not reverse** the sign of the uplift; **and**
- the improvement appears in a **majority of evaluated validation date-blocks**
  and in a **majority of evaluated validation months** (per §10–§12); **and**
- calibration is at least **directionally usable or plausibly fixable** (or, if
  unusable, the classification lift is strong and stable enough to justify a
  ranking-only follow-up); **and**
- the cost-descriptive statistics are acknowledged (the signal is understood to
  be **not tradable** at 15s but retains **information-diagnostic** value).

A `CONTINUE_ONE_FOLLOWUP` result authorizes **exactly one** bounded, separately
authorized follow-up, chosen from:

- **(a)** a longer-horizon label memo (5m/30m/1h; new label layer);
- **(b)** a bookTicker / mid-price data-admissibility memo (bounce-free labels;
  new data);
- **(c)** a code-only evaluation-framework extension (e.g. block-bootstrap
  inference);
- **(d)** one fixed-capacity model-comparison memo (a single, pre-registered,
  run-once shallow model to bound the "is capacity the bottleneck" question).

It does **not** authorize strategy / signals / PnL / backtests (§19).

**INVESTIGATE / AMBIGUOUS** — record `INVESTIGATE_AMBIGUOUS` — see §17.

**Threshold governance.** These thresholds are pre-registered and may **not** be
relaxed after a result is seen. They may only be changed by a **separate future
docs-only amendment authorized before the baseline is run** and justified from
committed evidence — never to rescue a near-miss.

---

## 17. Ambiguous-result handling

Record `INVESTIGATE_AMBIGUOUS` — which authorizes **only** one further docs-only
decision memo, **not** any data-reading or ML follow-up — if the result is mixed,
specifically if **any** of:

- aggregate metrics clear the continue margins but the **date/month-block
  evidence is mixed** (improvement present in only about half of blocks); **or**
- **validation improves** but the **internal-holdout dry-run does not** (without a
  full sign reversal that would trigger kill); **or**
- **classification improves** past the margins but **calibration fails** and it is
  unclear whether a ranking-only follow-up is warranted; **or**
- the result **suggests information** but is not clean enough for
  `CONTINUE_ONE_FOLLOWUP` without another explicit docs-only decision.

An `INVESTIGATE_AMBIGUOUS` outcome must **not** silently become a continue. It
forces a **separate, docs-only** arc-decision memo (the §18 Phase 4bn-AJ slot, or
an earlier explicitly authorized decision memo) that either closes the arc or
authorizes exactly one bounded follow-up under the §16 continue rules. The
default posture on ambiguity is **remain paused**.

---

## 18. Arc-budget / stopping-rule posture

The ML-baseline arc is **finite** from this amendment forward. Phase letters are
renumbered because the pre-registration memo consumed the `Phase 4bn-AE` slot
that the Phase 4bn-AD memo had tentatively reserved for the skeleton; the
recommended future modules / test path from Phase 4bn-AD (`pre_v002_ml_dataset_*`
and `test_phase4bn_ae_pre_v002_ml_dataset_builder_skeleton.py`) should be
renamed to the `af` phase tag when that phase is authored, but this is a naming
note only and authorizes nothing.

**Pre-registered finite arc budget** (each step separately authorized; none
authorized here):

- **Phase 4bn-AF** — code-only ML dataset builder skeleton (synthetic fixtures +
  offline tests; **no data read**), encoding this amendment (§20). *Recommended
  next; not authorized here.*
- **Phase 4bn-AG** — data-reading dataset builder authorization + a **single**
  builder run producing the pre-v002 dataset, with leakage proof + budget
  preflight. *Requires the still-absent `source_admissible_for_data_read` /
  `source_admissible_for_dataset_builder` authorizations.*
- **Phase 4bn-AH** — pre-declared **descriptive dataset diagnostics** (no models):
  class balance, label-overlap / effective-sample statistics (which may
  retroactively justify a §10 Option-2 stride), `forward_log_return_15s`
  distribution vs the 16 bps lock, per-month regime slices.
- **Phase 4bn-AI** — the **fixed baseline run** (majority / persistence / linear,
  run once each, no selection) evaluated against §13–§16, producing the verdict
  under §16/§17.
- **Phase 4bn-AJ** — **arc-decision memo**: on the §16/§17 verdict, either
  **close the arc** or authorize **exactly one** bounded follow-up (§16 (a)–(d)).

**Stopping rule.** After Phase 4bn-AJ the arc **must** either close or authorize
exactly one bounded follow-up; it may not spawn an open-ended sequence of further
readiness / contract / interpretation memos. Any `KILL` verdict at Phase 4bn-AI
closes the arc at Phase 4bn-AJ. This budget is a **posture**, not an
authorization: every phase in it still requires explicit per-phase operator
authorization, and the operator may close the arc at any point.

The letters `AF..AJ` are indicative; the operator may re-letter or compress
steps (e.g. combine AH descriptive diagnostics into AI), but the **finite,
five-step-then-decide** shape is pre-registered.

---

## 19. Strategy / PnL / backtest hard boundary

**No result of the pre-v002 first baseline, however strong, authorizes any of:**

- strategy construction;
- signal generation;
- threshold trading / confidence-gated trading;
- backtesting;
- PnL computation;
- position sizing;
- execution logic;
- live-readiness;
- paper / shadow trading;
- exchange-write.

Any path toward those requires a **separate future M0-style mechanism-admissibility
memo** (per the Phase 4ak M0 twelve-clause gate) that clears, at minimum:

- **M0.5 cost realism** at the locked 8 bps/side · 16 bps round-trip — never
  deferred as it was at the microstructure reset (Phase 4as);
- execution feasibility;
- slippage / spread assumptions (which aggTrades-only data cannot currently
  support — mid-price / book data would be required);
- **label economic relevance** (the 15s strict-sign target is explicitly
  non-economic per §9);
- strategy admissibility against the retained rejections (R2 / F1 / D1-A / V2 /
  G1 / C1) and the M0 §7.D microstructure-lane `NOT_RECOMMENDED_NOW` posture;
- the Phase 4al no-rescue constraints.

This boundary is **absolute** and is not softened by any baseline metric.

---

## 20. Skeleton amendment obligations

If a future code-only ML dataset builder skeleton (Phase 4bn-AF) is separately
authorized, it must **encode or reserve inert interfaces for** the following, in
addition to the Phase 4bn-AC / 4bn-AD skeleton scope (contract constants, split
import, allowlist, forbidden-scan, filtering, alignment, train-only transforms,
proof-sidecar, no-data-I/O controls, fail-closed controls):

- an **evaluation-metrics registry** enumerating the §13 mandatory metrics
  (floors, classification, probabilistic, generalization-gap, counts) as
  constants / schema — exercised against synthetic fixtures only;
- **date-block / month-block reporting** schema fields (aggregate / monthly /
  date granularity per §11), including per-split row **and date** counts
  before/after filtering;
- **dependence-caveat fields** (the §10 effective-sample caveat; a boolean marking
  that per-row significance language is forbidden; a reserved, unset
  decimation-stride field defaulting to "none");
- **pre-registered success / kill / investigate bucket constants** (the §16/§17
  thresholds: accuracy +2.0 pp over both floors, balanced accuracy +1.0 pp,
  macro-F1 +0.03, majority-of-blocks agreement, holdout-no-sign-reversal,
  calibration-tail rule) as **frozen constants**, not tunable parameters;
- a **confidence-bin / calibration output schema** (§14: bins, empirical accuracy
  per bin, high-confidence-tail size and accuracy, beats-majority booleans,
  usable/ranking-only/unusable verdict field);
- **cost-descriptive fields** (§15: `forward_log_return_15s` summary statistics,
  share > 16 bps, optional share > 8 bps) as **descriptive-only** schema, with an
  explicit flag that they authorize no trading rule / label / PnL;
- **non-authorization flags** (mirroring `ml_baseline_design_v002`
  `NON_AUTHORIZATION_FLAGS`: all false for ML / diagnostics / strategy / signals /
  PnL / backtest / live / exchange-write);
- an explicit **no-strategy-boundary** constant encoding §19;
- **proof fields for row / date / month counts** by split and reason;
- the **no-data-I/O controls** and **fail-closed controls** from Phase 4bn-AD
  (no import-time side effects; no filesystem read/write calls; no network; a test
  proving zero file reads/writes/directory creations; the no-output-namespace
  proof).

The skeleton must still use **synthetic in-memory fixtures only** and **read no
data**, create no output directory, write no Parquet, mutate no manifest, and
produce no `data/research` / `data/microstructure` artefact. The success/kill
constants and metric/calibration/cost/dependence schemas are **encoded and
tested against synthetic fixtures**; they are **not** run against real data by the
skeleton.

---

## 21. Remaining blockers before code-only skeleton

Before a code-only skeleton (Phase 4bn-AF) may be authored:

- this pre-registration + contract amendment recorded (**this phase**); **and**
- separate operator authorization for the code-only skeleton phase (the
  Phase 4bn-AD `RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON`
  recommendation stands, now to be encoded against the **amended** contract).

The skeleton itself remains **not blocked** by `source_admissible_for_data_read`
/ `source_admissible_for_dataset_builder` (both false), because it reads no data
and creates no output — the same basis that made the Phase 4bn-AA pure split
artefact and the Phase 4bn-AD readiness decision safe.

---

## 22. Remaining blockers before data reads

Unchanged from Phase 4bn-AC §23. A data read on the pre-v002 segment remains
blocked until **all** of: the recorded contract (done) + this amendment (done); a
code-level builder bound to the passed gates (`3452fd9d…` / `db731d1b…` /
`ffb5b09…`), the manifests/hashes, and the Phase 4bn-AA split artefact; the
leakage / split-integrity proof and the Phase 4bn-L budget preflight bound into
the builder; **and** a separate operator authorization for data reads
(`source_admissible_for_data_read = false`).

---

## 23. Remaining blockers before real dataset builder

Unchanged from Phase 4bn-AC §24, plus this amendment. A dataset builder remains
blocked until: the recorded contract + amendment; the Phase 4bn-AD
builder-readiness decision (done — code-only first); a passing code-only skeleton
with synthetic validation **encoding this amendment**; the leakage proof + budget
preflight designed into the builder; **and** a separate operator authorization
(`source_admissible_for_dataset_builder = false`).

---

## 24. Remaining blockers before ML training

Unchanged from Phase 4bn-AC §25, plus this amendment. ML training remains blocked
until: all §22 and §23 blockers; the per-task target / horizon / filtering
locked by contract (`forward_direction_15s`, 15s, 3-class signed — done) **and
the evaluation / dependence / success-kill layer pre-registered (done, this
phase)**; a committed end-to-end pre-v002 trainer (does **not** exist); **and** a
separate operator authorization (`ml_authorized = false`).

---

## 25. Candidate next phases considered

1. **Code-only ML dataset builder skeleton (Phase 4bn-AF)** encoding this
   amendment (synthetic fixtures, no data read). **Lowest-risk code step; now
   safe because the evaluation contract is complete.** *Selected recommendation.*
2. **Current-state consolidation memo (docs-only)** — freeze the 2.7 MB
   `current-project-state.md`, publish a compact authoritative current-state
   doc. Genuinely worthwhile (the external review flagged the state doc as a
   broken source-of-truth), but **not a prerequisite** for the code-only skeleton
   (the skeleton reads no state doc). Recommended as a **near-term parallel**
   docs-only option, not as the blocking next step.
3. **Additional evaluation-design memo** — another docs-only evaluation memo.
   **Rejected as redundant:** this amendment *is* the evaluation-design memo;
   another would be process bloat.
4. **Source-admissibility gate artefact (code-level)** — not required before the
   skeleton (Phase 4bn-AB already established the docs-level admissibility
   posture); defer.
5. **Data-reading builder** — **not** a candidate now; both admissibility flags
   are false and no skeleton exists.
6. **Close the ML-baseline arc** — defensible but premature: the pre-registered
   arc can still answer one real diagnostic question at modest cost; closing
   before Phase 4bn-AI forfeits it.

---

## 26. Selected next recommendation

**Recommend authorizing a code-only ML dataset builder skeleton (Phase 4bn-AF),
subject to separate operator authorization**, now that the evaluation /
interpretation / decision layer is pre-registered and the contract is amended.
The skeleton must encode the amended contract (§20), use synthetic fixtures only,
and read no data.

A **current-state consolidation memo** is **also recommended** as a near-term,
parallel docs-only phase (§25 option 2); it is not a blocker for the skeleton and
either order is acceptable, but the state doc should be repaired before many more
phases append to it.

No successor is authorized from inside Phase 4bn-AE.

---

## 27. Explicit non-authorizations

Phase 4bn-AE does **not**, and does not authorize anyone to: read or create any
local data; inspect any file under `data/microstructure/` or `data/research/`;
inspect any raw zip / normalized / feature / label Parquet / manifest / gate
report / sidecar; read the v002 terminal window; touch the sealed v002 test split
(`test_rows_loaded = 0`); create a split file / research matrix / ML dataset / ML
config / manifest / sidecar / gate report; create the future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`; mutate any
manifest / sidecar / gate report / successor-state artefact; flip
`research_eligible`; transition `eligibility_gate_status` /
`chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`; invoke
or alter the Phase 4aw `flip_research_eligible(...)` always-raises invariant;
train / score / predict; run diagnostics / strategy / signals / PnL / backtests;
acquire data; call any public / authenticated / private endpoint; download any
archive / CHECKSUM; run a HEAD preflight; rerun any acquisition / raw /
normalization / feature / label execution or any layer gate; create a database /
`.duckdb` / `.sqlite`; compact Parquet; migrate storage; create v003; create or
commit any `data/microstructure` or `data/research` artefact; use credentials /
`.env` / `.mcp.json` / MCP / Graphify; open any WebSocket / user stream; authorize
Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production
keys, or any successor phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side; round-trip = 16 bps;
§1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j
§11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause
gate + post-null cooldown; Phase 4al refined no-rescue rule; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F
canonical path + sidecar policy; Phase 4bl-F risk tiers; Phase 4bm-U / 4bm-W v002
split policy; Phase 4bn-J-R1 raw-only cap amendment; Phase 4bn-L derived-stack
storage budget; Phase 4bn-N normalization manifest/versioning; Phase 4bn-R feature
manifest/versioning; Phase 4bn-V label manifest/versioning; Phase 4bn-Y
chronological split/holdout policy; Phase 4bn-Z ML-baseline readiness memo; Phase
4bn-AA pre-v002 split-policy artefact; Phase 4bn-AB source-admissibility posture;
Phase 4bn-AC ML dataset contract; Phase 4bn-AD ML dataset builder readiness
verdict) is preserved verbatim. Phase 4 canonical remains unauthorized.

---

## 28. Result state

`ML_BASELINE_PREREGISTRATION_RECORDED__CONTRACT_AMENDED__SKELETON_NEXT__NO_DATA_READ__REMAIN_PAUSED`

The ML-baseline evaluation / interpretation / decision layer is pre-registered
and the Phase 4bn-AC contract is amended (amendment 001); no data reads are
authorized; no dataset builder is authorized; no ML is authorized;
`source_admissible_for_dataset_contract` remains true;
`source_admissible_for_data_read` and `source_admissible_for_dataset_builder`
remain false; manifest state is unchanged; the code-only skeleton (Phase 4bn-AF)
is the recommended next step subject to separate authorization.

---

## 29. Decision

`RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`

Rationale: with the evaluation / dependence / success-kill / cost-realism /
strategy-boundary layer now pre-registered, a code-only skeleton can safely
encode the **amended** contract against synthetic fixtures only. It reads no data
and remains subject to separate operator authorization. A current-state
consolidation memo is separately recommended as a near-term parallel docs-only
option but is not a blocker.

---

## 30. Recommended state and successor options

**Recommended state: remain paused. No next phase authorized.**

Operator options (each subject to separate authorization after the
branch-complete report):

- remain paused;
- request a merge prompt for Phase 4bn-AE;
- separately authorize a **code-only ML dataset builder skeleton** (Phase 4bn-AF)
  encoding this amendment (**preferred**);
- separately authorize a **current-state consolidation memo** (near-term parallel
  docs-only option);
- separately authorize an **additional evaluation-design memo** only if a genuine
  gap in this amendment is identified (not recommended — this amendment is the
  evaluation design);
- separately authorize a **source-admissibility gate artefact** if preferred;
- separately authorize a **full-envelope reference-assembly memo** only if a
  future path combines pre-v002 + v002 data;
- separately authorize a **holdout-boundary memo** only if a future scope touches
  the v002 terminal or sealed-test dates;
- reject further ML-baseline successors and **close the ML arc**.

No data-reading builder / ML / diagnostics / strategy / signals / PnL / backtest /
storage-migration / paper / shadow / live / exchange-write option is valid from
this state unless separately authorized after this branch is merged.

---

## 31. Current-project-state update summary

`current-project-state.md` is updated **additively only**: one new Phase 4bn-AE
paragraph appended after the Phase 4bn-AD paragraph, and one new `Current phase:`
block inserted ahead of the Phase 4bn-AD block. All prior content (Phase 4bn-A …
4bn-AD paragraphs and blocks, every retained verdict and project lock) is
preserved verbatim. No manifest field, eligibility flag, or split-policy field is
set. The update records: ML-baseline pre-registration recorded; Phase 4bn-AC
contract amended (amendment 001); `forward_direction_15s` retained as a
first-baseline **information-diagnostic** (non-economic) target; overlapping-label
dependence policy (Option 1: date/month-block aggregation, row-level metrics
descriptive-only, no per-row significance, decimation reserved-not-adopted);
date/month-block + regime reporting policy; mandatory metric registry;
calibration / confidence-tail policy (carrying the v002 high-confidence-tail
finding); cost-realism descriptive policy (share of 15s moves exceeding the
16 bps lock; descriptive only); pre-registered success (+2.0 pp accuracy over both
floors, +0.03 macro-F1, majority-of-blocks, holdout-no-sign-reversal) / kill /
investigate criteria; finite arc budget (Phase 4bn-AF skeleton → AG builder →
AH diagnostics → AI baseline run → AJ arc-decision, then close or one bounded
follow-up); strategy / PnL / backtest hard boundary (requires a future M0-style
memo clearing cost realism); skeleton amendment obligations; result
`ML_BASELINE_PREREGISTRATION_RECORDED__CONTRACT_AMENDED__SKELETON_NEXT__NO_DATA_READ__REMAIN_PAUSED`;
decision
`RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
remain paused; no successor authorized.
