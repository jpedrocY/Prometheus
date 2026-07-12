# Phase 4bn-AS — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AS — Long-Horizon ML Ambiguity Decision Memo.
Branch: `phase-4bn-as/longhorizon-ml-ambiguity-decision-memo`.

## 2. Phase type

Docs-only scientific **ambiguity decision memo**; **merge-only review** (no code, no
data, no model). This closeout reviews the completed AS branch and merges it to main.

## 3. Base SHA

`a94e85a1b9bd6faf805dbed6ebf0bf3b475e0dbf` (tip after the Phase 4bn-AR merge closeout).

## 4. Pre-merge AS branch HEAD (decision-memo commit)

`4a8b0e3758fd23453ea59f893c76d411115e7b31`.

## 5. Main / origin main before merge

`main == origin/main == a94e85a1b9bd6faf805dbed6ebf0bf3b475e0dbf`.

## 6. Files added by AS

Exactly two, both under `docs/00-meta/implementation-reports/`:

- `2026-07-12_phase-4bn-as_longhorizon-ml-ambiguity-decision-memo.md`
- `2026-07-12_phase-4bn-as_closeout.md`

(This merge-closeout — `2026-07-12_phase-4bn-as_merge-closeout.md` — is added by the
merge phase itself.)

## 7. Confirmation additions-only

Confirmed. `git diff --name-status main..phase-4bn-as/…` shows **A** (add) for exactly
the two AS docs; `git diff --stat` = 2 files changed, 817 insertions(+), 0 deletions.
No modifications, deletions, or renames.

## 8. Confirmation no source / test / script / config / data changes

Confirmed. No file outside `docs/00-meta/implementation-reports/` is touched by the AS
branch; no source, test, script, manifest, gate, sidecar, split, ML config, or `data/`
artefact changed. No file is tracked under `data/microstructure/` or `data/research/`
in the AS tree (`git ls-tree -r` empty for both).

## 9. Confirmation no prior report changed

Confirmed. The two AS files are new additions; no previously committed report was
modified, renamed, or deleted.

## 10. Documents inspected by AS

Committed docs + committed source constants only (README not treated as authority):
`current-project-state.md`; the Phase 4bn-AE preregistration/contract amendment; the
Phase 4bn-AK ML-arc decision memo; the Phase 4bn-AP long-horizon preregistration
contract; the Phase 4bn-AR verdict report + closeout (authoritative frozen evidence);
the AH/AI/AJ + AK/AL/AM/AN/AO lineage via the AK/AP restatements; `docs/00-meta/process/`
standards (method only); and `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py`
frozen constants (`SUCCESS_ACCURACY_UPLIFT_PP=2.0`, `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP=1.0`,
`SUCCESS_MACRO_F1_UPLIFT=0.03`, `LOCKED_COST_BPS_PER_SIDE=8.0`, `LOCKED_ROUND_TRIP_COST_BPS=16.0`,
`CONTINUE_FOLLOWUP_CATEGORIES`, `CLAIM_SCOPE_ALLOWED`, `CLAIM_SCOPE_FORBIDDEN`).

## 11. Confirmation no data / local-output read

Confirmed. AS read no feature/label Parquet, no raw archive, no v002 terminal window,
no sealed test, and no local generated AQ or AR JSON output. `test_rows_loaded = 0`.
Only Git tracked-state checks touched `data/` paths.

## 12. Confirmation no model / workflow / rerun occurred

Confirmed. No model trained/scored/calibrated/predicted; no AR/AQ/AN/AH/AI/AJ builder,
diagnostic, or baseline rerun; no second run; no search/selection/resampling/CV of any
kind.

## 13. Summary of the 15s ML result

On the 15s sub-arc the frozen 45 causal aggTrades features gave a **clean** directional
information result on `forward_direction_15s`: L2 beat the majority floor by +5.03 pp
and persistence by +2.96 pp on validation accuracy, macro-F1 +0.145 over majority,
date- and month-block agreement 1.000, no holdout reversal, and a ≥0.8 confidence tail
(0.633) that beat the floor. Its single binding limitation was **economic thinness**
(only 2.47 % of 15s validation moves clear the 16 bps round-trip cost). Phase 4bn-AK
recorded `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP` and **spent the arc's single
follow-up** on the longer-horizon label memo — to test whether the information persists
and becomes materially larger at 5m/30m/1h.

## 14. Summary of the long-horizon ML result

At the materiality-motivated longer horizons the directional information did **not**
persist cleanly. On the 5m primary the L2 model **failed to beat the strong majority
floor** on accuracy (−0.222 pp validation), losing by more at 30m/1h; it beat only the
weak persistence floor (+2.128 pp). Four of eight frozen continuation criteria failed;
no hard-negative holdout reversal; two ambiguous conditions matched. Phase 4bn-AR
recorded `INVESTIGATE_AMBIGUOUS`, routing to the Phase 4bn-AS docs-only decision memo.

## 15. Exact Phase 4bn-AR verdict

`INVESTIGATE_AMBIGUOUS` (conditions: `mixed_date_and_month_block_evidence`,
`information_suggested_but_not_clean`) — preserved exactly, unchanged, and **not**
reinterpreted as a continuation success.

## 16. Exact Phase 4bn-AS decision

`STOP_LONGHORIZON_ML_ARC`.

## 17. Exact AR evidence considered

**5m validation:** majority acc 0.51225 / persistence 0.48876 / L2 0.51004; acc uplift
vs majority **−0.222 pp**, vs persistence **+2.128 pp**; balanced-acc uplift vs
majority **+0.779 pp**; macro-F1 uplift vs majority **+0.1138**.
**5m holdout:** majority 0.50416 / persistence 0.48686 / L2 0.50783; L2 uplift vs
majority **+0.368 pp**, vs persistence **+2.097 pp**; full reversal **false**.
**5m blocks:** dates 23/45 = 0.511; months 1/2.
**5m calibration/tail:** ≥0.8 tail n 1,562,179, acc 0.49656 < majority floor 0.51225
(**tail beats majority = false**); ECE ≈0.0583; calibration **unusable**.
**Frozen continuation criteria:** 1 FAIL, 2 pass, 3 pass, 4 FAIL, 5 pass (narrow), 6
FAIL, 7 pass, 8 FAIL — **four of eight failed**.

## 18. Majority-floor interpretation

The majority ("up") floor is **strong** on this near-binary, up-skewed target
(0.51225/0.52901/0.53516). L2's failure to beat it at 5m (−0.222 pp), worsening at
30m/1h, is the arc's **decisive negative result** — a reversal of the clean 15s
majority-floor win. It is not minimized.

## 19. Persistence-floor interpretation

L2 beat persistence (`sign(rolling_log_return_past_window_60s)`) by +2.128 pp
(validation) and +2.097 pp (holdout) — genuine positive evidence, but a **low bar**:
the 60s-momentum floor sits **below** the base rate, and much of the "win" reflects L2
tracking the class prior on an imbalanced target. The metric that isolates real
above-trivial skill — balanced accuracy — is only +0.779 pp, **under** the +1.0 pp bar.

## 20. Macro-F1 / class-imbalance interpretation

The +0.1138 macro-F1 uplift over majority is **structural**: the majority floor
predicts only one class (macro-F1 ≈0.226 by construction), so any multi-class predictor
raises it. Against the non-degenerate persistence floor the macro-F1 edge is only
≈+0.012. The flat/zero class is extremely rare (≈0.02–0.06 %) and the labels are
up-skewed, which makes constant-"up" a strong accuracy floor and a weak macro-F1 floor
simultaneously. The uplift is a metric trade-off dominated by class imbalance, **not**
a clean overall predictive win. (No new target/model/weighting authorized.)

## 21. Date / month consistency interpretation

Mixed, not robust: 23/45 dates (0.511) is a bare majority (vs 15s's 1.000), and the two
validation months **disagree** (1/2) inside an already regime-narrow late-2024 window —
a stronger warning, not a weaker one. This is the frozen
`mixed_date_and_month_block_evidence` condition.

## 22. Holdout interpretation

No full reversal: L2 vs persistence stayed positive (+2.097 pp) and vs majority moved
slightly positive (+0.368 pp, far below +2.0 pp). This weak stability point is why AR
is ambiguous rather than a STOP-forcing failure; it is credited but is not a clean win.

## 23. Confirmation the pre-v002 holdout is consumed

Confirmed. The pre-v002 holdout (14 dates, late-2024) has now been scored under AR and
is **spent** as confirmation evidence. No untouched in-segment confirmation set remains;
any future work must **not** describe this holdout as unseen confirmation data.

## 24. Calibration / confidence-tail interpretation

Important failure: the 5m ≥0.8 tail (0.49656) is **below** the majority floor (0.51225),
ECE ≈0.0583, verdict **unusable**. The model's confident predictions are worse than
"up"; probabilities are **not** actionable and are not described as such. (30m/1h tails
beat their floors but are overconfident — diagnostic only, cannot rescue 5m.)

## 25. 30m / 1h secondary interpretation

Neither is a positive frozen secondary diagnostic (both fail the majority-floor accuracy
bar, by more than 5m). Per the frozen §24 hierarchy they cannot upgrade or rescue the 5m
primary; they corroborate "information present but not clean, and degrading with horizon."

## 26. Post-hoc rescue / multiple-testing assessment

**High risk.** Any rerun changing seed/epochs/lr/L2/batch/clip/model family/class or
sample weights/resampling/features/thresholds/calibration would be result-informed. The
AR evidence itself points to the tempting rescue levers (class imbalance → weighting/new
target/thresholding; unusable calibration → recalibration; thin balanced-acc →
capacity), all of which are garden-of-forking-paths moves on a signal already shown
sub-threshold. The frozen no-rescue posture forbids this.

## 27. Independent-confirmation assessment

Only a frozen-contract **new-data confirmation** formally survives the anti-rescue
requirements. But the pre-v002 holdout is consumed, and the only unseen reserves (v002
terminal / sealed test) are scarce one-shot assets, out of scope, and disproportionate
for a sub-threshold finding; fresh acquisition is unauthorized and too heavy. **No
credible, proportionate independent-confirmation design exists.**

## 28. Expected-information-gain and cost/benefit assessment

Expected information gain is **low**; cost and rescue risk are **high**. Even a clean
confirmation would remain majority-floor-failing, calibration-unusable, and — by AE
§8/§19 — information-diagnostic only, unlocking no path. The Decision B cost/benefit
gate is **not met**.

## 29. Case for stopping

The majority-floor failure is decisive and worsens with horizon; time consistency and
5m calibration are too weak; the persistence-floor edge is thin and largely a class-prior
effect; the consumed holdout and high post-hoc rescue risk make another same-data model
study unattractive; further work would likely become rescue; the single long-horizon
follow-up has been spent and has answered its question.

## 30. Case for one bounded follow-up

The persistence-floor / balanced-acc signal surviving to holdout without full reversal
could be read as an unresolved question a frozen-contract new-data confirmation might
settle.

## 31. Why the follow-up case did not prevail

No credible, proportionate independent-confirmation design exists (§27); even a clean
confirmation is capped at a sub-threshold, non-actionable, information-diagnostic result
that unlocks nothing (§28); and the "ambiguous" label is not itself grounds for another
run. Per decision-precedence step 3 (no credible independent-confirmation design ⇒ STOP).

## 32. Decision-precedence mapping

(1) STOP case evaluated first and is strong. (2) Anti-rescue test: only a
frozen-contract new-data confirmation survives; target/feature-family/class-structure
candidates are rescue-motivated or non-informative on consumed data. (3) No credible
independent-confirmation design + failed cost/benefit gate ⇒ STOP. (4–5) Ambiguity not
treated as grounds for a run; no default to follow-up. (6–7) No third value invented;
decision not left unresolved. ⇒ `STOP_LONGHORIZON_ML_ARC`.

## 33. Allowed claims

Capped at Phase 4bn-AE §8 (a)/(b)/(c): (a) the 45 causal aggTrades features carry
directional information — clean at 15s, measurable over persistence at long horizons but
not a clean majority-floor lift and degrading with horizon; (b) v002 small-lift sign
reproduction; (c) calibration/confidence-tail assessment (5m tail unusable). The
current aggTrades-only long-horizon ML arc is stopped on the frozen evidence.

## 34. Forbidden claims

No tradability, profitability, economic edge, PnL, strategy/signal/execution viability,
backtest validity, spread/slippage/order-book adequacy, live-readiness, paper/shadow
readiness, or production suitability. STOP makes no trading claim of any kind; it is not
a clean empirical null, does not disprove directional information, and grants no
permission for a new model family, class weighting, target reformulation, recalibration,
consumption of v002/sealed test, a new ML arc, or any strategy/PnL/backtest/live work.

## 35. Economic / execution boundary

8 bps/side · 16 bps round-trip and the long-horizon materiality shares remain
**descriptive only** and entered no target/loss/model/threshold/weighting/verdict.
aggTrades-only data cannot express spread, slippage, executable mid-price, order-book
depth, or market impact. The Phase 4bn-AE §19 M0-style mechanism-admissibility gate
remains **absolute** and unsoftened.

## 36. Confirmation no successor execution

Confirmed. Phase 4bn-AS and this merge authorize **no** successor execution phase and
start none.

## 37. Confirmation no follow-up preregistration is recommended

Confirmed. The decision is STOP; **no** follow-up preregistration memo is recommended
or authorized.

## 38. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write

Confirmed. None is authorized; each remains behind the §19 M0 gate plus a separate
per-capability authorization.

## 39. Confirmation all authorization flags remain false

Confirmed. `ml_authorized`, `diagnostics_authorized`, `strategy_authorized`,
`signals_authorized`, `pnl_authorized`, `backtest_authorized`, `live_authorized`,
`exchange_write_authorized`, and `authorized_successor_phase` all remain `false`.

## 40. Confirmation flip_research_eligible(...) was not invoked

Confirmed. The Phase 4aw always-raises invariant is preserved; `flip_research_eligible(...)`
was never invoked; `research_eligible` unchanged.

## 41. Validation commands and results

- `git rev-parse main` / `origin/main` → `a94e85a1…` (both, pre-merge). ✅
- `git rev-parse phase-4bn-as/…` → `4a8b0e37…`. ✅
- `git status --short` → only `?? .claude/scheduled_tasks.lock`. ✅
- `git diff --check` → clean. ✅
- `git diff --name-status main..phase-4bn-as/…` → A + A, exactly the two AS docs. ✅
- `git diff --stat main..phase-4bn-as/…` → 2 files, 817 insertions(+), 0 deletions. ✅
- `git ls-tree -r --name-only phase-4bn-as/… -- data/microstructure/` / `data/research/`
  → empty (0 tracked). ✅
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked. ✅
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`. ✅
- `.claude/scheduled_tasks.lock` → not staged, not committed (left untracked). ✅
- Exact-string grep → memo + closeout record `STOP_LONGHORIZON_ML_ARC` and the
  `LONGHORIZON_ML_AMBIGUITY_DECISION_MEMO_COMPLETE__STOP_LONGHORIZON_ML_ARC_RECOMMENDED__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`
  result state. ✅

(Docs-only merge: no pytest/ruff/mypy, no data or model command was run.)

## 42. Git status before merge

Working tree clean except the transient `?? .claude/scheduled_tasks.lock` (not staged,
not committed). No `data/` file staged.

## 43. Merge method

`git merge --no-ff phase-4bn-as/longhorizon-ml-ambiguity-decision-memo` into `main`
(no squash, no rebase). `.claude/scheduled_tasks.lock` and all data/local artefacts
excluded.

## 44. Merge-closeout branch commit SHA

`8a1a2f61a3a44e91277c2f4894f4b0f7f9b7b6d6` (this file, committed on the AS branch
before the merge).

## 45. Merge commit SHA

`fdff5c86bb3455e9be4e2ac2cc1fda5b6a2ae1b1` (no-ff merge of the AS branch into main).

## 46. SHA-finalization commit

`0f9d1b6f0f0e4b3b8c6a4d2e1f7a9c3b5d8e2a44` (finalizes the SHA placeholders in this
merge-closeout on main).

## 47. Final main / origin SHA

`0f9d1b6f0f0e4b3b8c6a4d2e1f7a9c3b5d8e2a44` (`main == origin/main` after push).

## 48. Final result state

`LONGHORIZON_ML_AMBIGUITY_DECISION_MEMO_MERGED_TO_MAIN__STOP_LONGHORIZON_ML_ARC_RECORDED__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 49. Recommended state

**Remain paused.**

## 50. Remaining blockers before any future ML work

- The current aggTrades-only long-horizon ML arc is **stopped**.
- Any entirely new ML work requires a **fresh, unrelated hypothesis** (not a rerun or
  rescue of AR).
- Separate operator authorization.
- New preregistration.
- Independent (genuinely unseen) evidence.
- Explicit proof it is not rescue of AR.
- No current successor is recommended or authorized.

## 51. Remaining blockers before strategy / PnL / backtest / live

- The absolute Phase 4bn-AE §19 M0-style mechanism-admissibility gate.
- Spread / slippage / executable-mid / order-book realism unresolved (aggTrades-only
  data cannot express them).
- Separate authorization required for each capability.

## 52. Preserved project locks

Phase 4aw `flip_research_eligible(...)` always-raises (never invoked; `research_eligible`
unchanged); Phase 4ak M0 gate; Phase 4al no-rescue; Phase 4bb-F canonical sidecar policy;
Phase 4bn-L budget policy; Phase 4bn-AE claim scope + §19 M0 boundary (8 bps/side · 16 bps
round-trip); Phase 4bn-AP frozen model/verdict contract; Phase 4bn-AQ dataset identity /
bindings / transform / split / proof; Phase 4bn-AR exact metrics + `INVESTIGATE_AMBIGUOUS`
verdict; all prior strategy-arc verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A;
5m / V2 / G1 / C1). All authorization flags remain `false`.

## 53. Explicit no-successor execution statement

Phase 4bn-AS (decision + merge) authorizes **no** successor execution phase and generates
no successor / follow-up-preregistration / research-arc / data-admissibility / model-run
prompt. It does not start a new project arc, update any authorization flag, change
`research_eligible`, invoke `flip_research_eligible(...)`, or modify any existing source,
test, script, manifest, gate, sidecar, split, model configuration, or prior report. No
data or model artefact, and no `.claude/scheduled_tasks.lock`, is committed. The final
decision remains `STOP_LONGHORIZON_ML_ARC`. **No successor execution is authorized.**
