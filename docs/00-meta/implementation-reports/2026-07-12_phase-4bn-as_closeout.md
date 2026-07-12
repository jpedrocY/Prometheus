# Phase 4bn-AS — Closeout

## Branch

`phase-4bn-as/longhorizon-ml-ambiguity-decision-memo`

## Base SHA

`a94e85a1b9bd6faf805dbed6ebf0bf3b475e0dbf` (`main == origin/main == HEAD` at branch
time; tip after the Phase 4bn-AR merge closeout).

## Phase type

Docs-only scientific **decision memo**. It resolves the frozen Phase 4bn-AR
`INVESTIGATE_AMBIGUOUS` verdict into exactly one of two recommendations (stop the arc,
or recommend one bounded follow-up preregistration memo for later separate
authorization). It runs, implements, and authorizes **nothing**.

## Files created (docs only)

- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-as_longhorizon-ml-ambiguity-decision-memo.md`
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-as_closeout.md` (this file)

**No** source / test / script / manifest / gate / sidecar / split / config / `data/`
artefact created or modified. `current-project-state.md` unchanged.

## Documents inspected

Committed docs + committed source constants only (`README` not treated as authority):
`current-project-state.md`; the Phase 4bn-AE preregistration/contract amendment; the
Phase 4bn-AK ML-arc decision memo (prior single-follow-up selection); the Phase
4bn-AP long-horizon preregistration contract; the Phase 4bn-AR verdict report and
closeout (authoritative frozen evidence); the AH/AI/AJ reports and the AK/AL/AM/AN/AO
lineage as recovered through the AK/AP restatements; `docs/00-meta/process/` standards
(method only); and `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py`
frozen constants (`SUCCESS_ACCURACY_UPLIFT_PP=2.0`, `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP=1.0`,
`SUCCESS_MACRO_F1_UPLIFT=0.03`, `LOCKED_COST_BPS_PER_SIDE=8.0`, `LOCKED_ROUND_TRIP_COST_BPS=16.0`,
`CONTINUE_FOLLOWUP_CATEGORIES`, `CLAIM_SCOPE_ALLOWED`, `CLAIM_SCOPE_FORBIDDEN`). The
Phase 4bb-F sidecar policy and Phase 4bn-L budget policy were consulted via the
AH/AP/AR restatements. **No** committed report exhibited an inconsistency requiring
prohibited data access; the frozen evidence is internally consistent and matches the
operator-supplied figures verbatim.

## Evidence summary

5m primary (validation): L2 accuracy 0.51004 vs majority 0.51225 (**−0.222 pp**,
FAIL) / persistence 0.48876 (**+2.128 pp**, pass); balanced-acc 0.34113 vs 0.33333
(**+0.779 pp**, FAIL vs +1.0); macro-F1 0.33958 vs 0.22582 (+0.1138 over a
structurally-weak majority floor, ≈+0.012 over persistence). Blocks: dates 23/45
(0.511, bare pass) / months 1/2 (FAIL). Holdout: no full reversal (vs majority
+0.368 pp, vs persistence +2.097 pp). ≥0.8 tail acc 0.49656 < majority 0.51225
(FAIL), calibration **unusable** (ECE ≈0.0583). Secondaries 30m/1h fail the
majority-floor accuracy bar → not positive; cannot rescue. Four of eight frozen
continuation criteria fail; no hard-negative holdout reversal; two ambiguous
conditions match. AR verdict: `INVESTIGATE_AMBIGUOUS`
(`mixed_date_and_month_block_evidence`, `information_suggested_but_not_clean`).

## Exact decision

**`STOP_LONGHORIZON_ML_ARC`**

## Concise decision rationale

The decisive result is a **majority-floor failure** on the 5m primary (−0.222 pp),
worsening at 30m/1h — the clean 15s majority-floor win did not carry to the horizons
this follow-up was built to test. The only positive (beating the weak, below-base-rate
persistence floor by +~2.1 pp) is thin, largely a class-prior effect, and fails the
balanced-accuracy gate that isolates genuine skill (+0.779 < +1.0 pp). Block evidence
is mixed (bare dates, non-unanimous months) and the 5m calibration is unusable
(high-confidence tail below the floor). The pre-v002 holdout is now **consumed**, so no
untouched in-segment confirmation remains; every obvious next move (class weights, new
target, thresholds, recalibration, more capacity) is result-informed **post-hoc
rescue** with high multiple-testing risk. Testing follow-up classes against the
anti-rescue requirements, only a frozen-contract **new-data confirmation** formally
survives — but no credible, proportionate independent-confirmation design exists (the
only unseen reserves are scarce one-shot assets, out of scope), and even a clean
confirmation would remain sub-threshold, calibration-unusable, and information-
diagnostic only, unlocking no path. Expected information gain is low; cost and rescue
risk are high; the Decision B cost/benefit gate is not met. Per decision-precedence
step 3 (no credible independent-confirmation design ⇒ STOP), and honouring the rule
that "ambiguous" is not itself grounds for another run, the arc is stopped.

## Confirmation no data read

Confirmed. No feature/label Parquet, raw data, v002 terminal window, or sealed test
was read; no test row loaded (`test_rows_loaded = 0`). Only Git tracked-state checks
(`git status` / `ls-files` / `check-ignore`) touched `data/` paths.

## Confirmation no local output read

Confirmed. No local generated AQ or AR JSON output artefact was opened or inspected;
the AQ and AR output namespaces were neither read nor mutated. All figures are quoted
from committed Markdown reports.

## Confirmation no model run

Confirmed. No model trained, scored, calibrated, recalibrated, or used for
prediction/inference; no feature selection/engineering, no hyperparameter/threshold
search, no resampling/CV, no alternate seed/epochs/weights.

## Confirmation no rerun

Confirmed. No AR / AQ / AN / AH / AI / AJ builder, diagnostic, or baseline was rerun;
no second fixed baseline run.

## Confirmation no successor execution

Confirmed. No successor execution phase is authorized; no follow-up is implemented,
preregistered, or started; no successor / preregistration / model-run / data-
acquisition prompt is generated.

## Confirmation no strategy / PnL / backtest / live authorization

Confirmed. No strategy / signals / PnL / backtest / Sharpe / hit-rate / turnover /
position sizing / execution / paper / shadow / live-readiness / deployment /
exchange-write path is authorized. The Phase 4bn-AE §19 M0-style mechanism-
admissibility gate remains absolute; the locked 8 bps/side · 16 bps cost stays
descriptive only.

## Remaining blockers

- Any future ML work of any kind requires a **separate** operator authorization; this
  memo recommends **against** further ML follow-up on the current aggTrades-only
  long-horizon evidence.
- Any strategy/PnL/backtest/live path remains behind the absolute Phase 4bn-AE §19 M0
  gate (aggTrades-only data cannot express spread/slippage/mid/depth/impact), plus a
  separate authorization per capability.

## Recommended state

**Remain paused.**

## Explicit no-successor execution statement

Phase 4bn-AS authorizes **no** successor execution phase and generates no successor or
future-preregistration prompt. Every retained project lock and verdict is preserved
verbatim (Phase 4aw `flip_research_eligible` always-raises invariant — never invoked;
Phase 4ak M0 gate; Phase 4al no-rescue; Phase 4bb-F sidecar policy; Phase 4bn-L
budget policy; Phase 4bn-AE claim scope + §19 M0 boundary; Phase 4bn-AP frozen model +
verdict contract; Phase 4bn-AQ dataset identity / bindings / transform / split /
proof; Phase 4bn-AR exact metrics and `INVESTIGATE_AMBIGUOUS` verdict). All published
authorization flags remain `false`. Do not merge to main and do not push unless
explicitly instructed later; do not generate a merge-closeout or a successor prompt
unless explicitly instructed later. **No successor execution is authorized.**

## Result state

`LONGHORIZON_ML_AMBIGUITY_DECISION_MEMO_COMPLETE__STOP_LONGHORIZON_ML_ARC_RECOMMENDED__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`
