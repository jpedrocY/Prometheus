# Phase 4bn-AK — ML Arc Decision Memo

## 1. Branch

`phase-4bn-ak/ml-arc-decision-memo`

## 2. Base SHA

`3e38fc87d148ed51ef23bfd76cf2f674a73fc8a0`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AJ merge
closeout). Verified in sync before branching.

## 3. Phase type and strict scope

Docs-only ML **arc-decision** memo. It reviews the completed Phase 4bn-AH /
4bn-AI / 4bn-AJ evidence, applies the pre-registered Phase 4bn-AE §16/§17/§18
arc-decision framework, and records the arc decision. It reads **no data**, trains
**nothing**, scores **nothing**, reruns **no** builder/diagnostics/baseline,
creates **no** data output, mutates **no** namespace, and authorizes **no**
successor execution phase. It is the pre-registered locus (Phase 4bn-AE §17/§18)
at which the arc must either close or authorize exactly one bounded follow-up.

## 4. Files created / modified

Created (committed):

- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_closeout.md`.

No source module, test, script, manifest, gate report, sidecar, split file, ML
config, research matrix, or `data/` artefact was created or modified. No dataset
namespace was created or mutated. `current-project-state.md` is **unchanged**
(see §29).

## 5. Exact documents / source inspected

Read-only (committed docs + committed source only; README treated as potentially
stale and not used as current-state authority):

- `docs/00-meta/current-project-state.md` (head + tail + ML-arc paragraphs;
  navigational summary, not binding authority).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`
  (§8 claim scope, §9 target interpretation, §10 dependence policy, §11–§12
  block/regime reporting, §13 metric registry, §14 calibration, §15 cost-realism,
  §16/§17 success/continue/kill/investigate, §18 arc budget & stopping rule, §19
  strategy/PnL/backtest/live hard boundary, §20 skeleton obligations).
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ah_data-reading-ml-dataset-builder-single-run.md`
  (dataset builder + single run).
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ai_descriptive-dataset-diagnostics-no-models.md`
  (descriptive diagnostics, no models).
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-aj_fixed-pre-v002-baseline-run-verdict.md`
  (fixed baseline run + verdict).
- Process standards under `docs/00-meta/process/` (phase-workflow, merge-closeout,
  phase-risk-tiering, operator-report, phase-prompt-template) — for method only.
- Committed source constants:
  `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py`
  (`SUCCESS_ACCURACY_UPLIFT_PP = 2.0`, `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP = 1.0`,
  `SUCCESS_MACRO_F1_UPLIFT = 0.03`, `LOCKED_COST_BPS_PER_SIDE = 8.0`,
  `LOCKED_ROUND_TRIP_COST_BPS = 16.0`, `CONTINUE_FOLLOWUP_CATEGORIES`,
  `CLAIM_SCOPE_ALLOWED`, `CLAIM_SCOPE_FORBIDDEN`);
  `pre_v002_fixed_baseline_run.py`, `ml_baseline_design_v002.py`,
  `ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py` (baseline family,
  frozen SGD hyperparameters, cost lock, calibration/stability helpers) — read for
  constant confirmation only; none modified.

Note on phase-letter re-lettering (Phase 4bn-AG recorded it): the Phase 4bn-AE §18
budget nominally listed `AF..AJ`, but the executed arc was re-lettered by one when
the `AG` slot was consumed by a data-reading authorization memo. The **current,
authoritative** sequence is: **AH** = data-reading builder + single run; **AI** =
descriptive diagnostics (no models); **AJ** = fixed baseline run + verdict; **AK**
= arc-decision memo (this phase). Obsolete earlier-memo letters are not trusted;
the substance is mapped to the current letters throughout.

## 6. Confirmation no data files were read

Confirmed. This phase read **no** feature/label Parquet row, **no** v002 terminal
window, **no** sealed test split, **no** raw zip, **no** AH/AJ local result
artefact under `data/research/` or `data/microstructure/`, and called **no**
endpoint. All evidence was recovered from committed Markdown reports and committed
source constants. No file under `data/microstructure/` or `data/research/` was
opened, listed for content, hashed, or otherwise inspected.

## 7. Confirmation no AH builder rerun occurred

Confirmed. The Phase 4bn-AH data-reading dataset builder was **not** re-run. Its
one-run guard remains untouched; its output namespace was not read or mutated.

## 8. Confirmation no AJ baseline rerun occurred

Confirmed. The Phase 4bn-AJ fixed baseline runner (`majority` / `persistence` /
`L2`) was **not** re-run. No model was trained, scored, or evaluated. No AJ metric
was recomputed, revised, or re-derived; every figure below is quoted verbatim from
the committed AJ verdict report.

## 9. Phase 4bn-AH evidence summary

Phase 4bn-AH implemented the pre-v002 data-reading ML dataset builder
(`pre_v002_ml_dataset_run.py`) and executed **exactly one** controlled local run
(1152.6 s), streaming all 400,001,695 pre-v002 rows across 275 partitions and
producing a **compact leakage-proof dataset specification** (train-only transform
stats + per-date split/filter index + per-split/per-month summaries + manifest +
leakage/split-integrity proof), not a re-materialised feature matrix (a full
matrix would breach the Phase 4bn-L 125 GiB derived cap).

Load-bearing findings:

- **Dataset builder success.** All pre-read checks PASS (source scope; full
  manifest/config/gate-report SHA256; 550 per-Parquet `.sha256` sidecars +
  inventory; 275/275 partitions; split-authority binding). Budget preflight PASSED
  (D: 1166.24 GiB free ≥ 500 GiB). The leakage/split-integrity proof **VALIDATED
  before any write**.
- **Leakage / split proof validated.** Strict positional alignment over 4 keys +
  `utc_date` on all 400,001,695 rows, **0 mismatches**, no join/reorder/fill.
  Per-horizon earlier-split boundary-crossing rows = **0** at 1s/5s/15s/60s.
  `no_random / no_shuffle / no_kfold / no_bootstrap = true`; deterministic
  UTC-date split assignment; 0 embargo rows used; 45-column allowlist with an
  **empty** forbidden-column scan; train-only transform fitted on the train split
  only.
- **No v002 terminal read.** `v002_terminal_window_read = false`; the v002-terminal
  config hashes are rejected by value + prefix; v002 window mode `by_reference`.
- **No sealed test.** `sealed_test_split_touched = false`; the sealed test
  (2025-02-14..2025-02-28) is outside the pre-v002 segment and was never read.
- **`test_rows_loaded = 0`** in both the proof and the dataset manifest.
- **Local/gitignored dataset-spec namespace.** Exactly one namespace created:
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
  (`.gitignore:88`); 4 JSON artefacts + 4 `.sha256` sidecars; **0 tracked** files.
- **No ML / no strategy.** All 8 non-authorization flags `false`; no model, score,
  prediction, diagnostic, strategy, signal, PnL, or backtest was produced.

Split kept-row counts: train 304,816,127; validation 68,578,296; holdout
23,535,860 (holdout censored drop 42; all other drop cells 0; no target imputed).

## 10. Phase 4bn-AI evidence summary

Phase 4bn-AI ran **read-only descriptive diagnostics** over the four AH artefacts
(all sidecars re-verified byte-identical; AH namespace unchanged). **No models, no
scoring, no predictions, no row-level Parquet read, no new namespace.** Committed
change set was docs-only.

Load-bearing findings:

- **Near-binary target.** `forward_direction_15s` class balance: the flat/zero
  class is a ~1% minority in every split (train 1.18%, validation 1.48%, holdout
  0.97%); the ±1 directional classes are near-balanced (~49–50% each). The task is
  effectively a near-binary directional problem with a rare tick-structure flat
  class.
- **Date/month block caveat.** Splits are concentrated by chronological
  construction: train = 2024-03..2024-09 (7 months), validation = 2024-10..mid-11,
  holdout = tail of 2024-11. Validation and holdout therefore both sit in the same
  late-2024 regime — a **regime-narrow** decision window (as Phase 4bn-AE §11
  pre-recorded). Decision blocks are 275 UTC dates / 9 UTC months; the ~397M kept
  rows are **not** ~397M independent observations (heavy 15s label overlap).
- **Continuous forward-return distribution not available from AH artefacts alone.**
  The AH artefacts carry the **categorical** `forward_direction_15s` counts and the
  **past-window** `rolling_log_return_past_window_15s` feature stats, but **no**
  location/dispersion/tail statistics of the continuous **forward** 15s log-return.
  A descriptive comparison of the forward-return distribution to the 16 bps cost
  therefore **could not be computed from AH artefacts alone**; AI recorded this as
  an explicit limitation rather than performing an unauthorized row-level read.
  (That continuous distribution was later measured, under authorization, during the
  Phase 4bn-AJ row-level baseline read — see §11.)
- **No models / no row-level reads / no strategy.** No feature selection, no
  importance ranking, no predictive interpretation, no economic inference. All
  forbidden-boundary confirmations recorded (§21 of the AI report).

## 11. Phase 4bn-AJ evidence summary

Phase 4bn-AJ ran the three pre-registered fixed baselines **exactly once each**
(majority / persistence / L2 multinomial-logistic, frozen Phase 4bn-B
hyperparameters), over an authorized row-level read of the AH-verified pre-v002
feature/label sources only (no v002 terminal, no sealed test, no raw zip,
`test_rows_loaded = 0`, 0 embargo rows). Single ~47.0-min run; each baseline once;
one-run guard active; nine compact JSON result artefacts written to one gitignored
namespace (no model binaries, no row-level predictions). AH namespace re-hashed
4/4 byte-identical (unmutated).

Validation metrics (15s), quoted verbatim:

- majority accuracy **0.49499 (0.4950)**; balanced acc 0.33333; macro-F1 0.22073.
- persistence accuracy **0.51576 (0.5158)**; balanced acc 0.40128; macro-F1
  **0.40191 (0.402)**.
- **L2 accuracy 0.54531 (0.5453)**; balanced acc 0.36892; **macro-F1 0.36600
  (0.3660)**.
- **L2 accuracy uplift over majority = +5.03 pp**; **over persistence = +2.96 pp**;
  balanced-acc uplift over majority = +3.56 pp; **macro-F1 uplift over majority =
  +0.145**.
- **Validation date-block agreement = 1.000** and **month-block agreement = 1.000**
  (L2 accuracy exceeds the majority floor in every evaluated validation date and in
  both validation months: 2024-10 L2 0.5546 vs 0.4909; 2024-11 L2 0.5352 vs
  0.4994).
- **Holdout: no sign reversal** (holdout L2 0.5417 vs majority 0.5003; validation−
  holdout accuracy −0.0036; validation−train +0.0078 → no overfitting).
- **High-confidence tail (proba ≥ 0.8): accuracy 0.633, beats the majority floor
  0.4950** on every split (holdout 0.659, train 0.604) — a notable improvement over
  v002 (where the tail sat at/below the floor) — **but overconfident in level**
  (e.g. validation 0.8–0.9 bin: mean predicted 0.843 vs empirical 0.589):
  usable for ranking/diagnostic reading, not as calibrated probabilities.
- **Cost realism (descriptive only): 2.47%** of validation 15s moves have
  `|forward_log_return_15s| > 16 bps` round-trip (11.97% > 8 bps one-way; median
  |return| 2.53 bps; p99 23.0 bps). Holdout > 16 bps = 1.20%. Only ~1 in 40 15s
  moves even in principle clears the locked round-trip cost.

**Recorded verdict: `CONTINUE_ONE_FOLLOWUP`** (Phase 4bn-AE §16). `kill_reasons =
[]`.

**Recorded caveat (verbatim substance):** persistence macro-F1 (0.402) exceeds
L2 macro-F1 (0.366) **solely because of the degenerate flat class** — persistence
occasionally predicts flat (validation flat recall 0.162) whereas L2 essentially
never does (predicted-zero rate 1.3e-5), the same degeneracy Phase 4bn-B saw on
v002; on the two **directional** classes L2's per-class F1 is higher (down 0.534
vs 0.518; up 0.563 vs 0.524). A **stricter "both-floors" macro-F1 reading** would
therefore yield `INVESTIGATE_AMBIGUOUS`. AJ recorded that **both readings converge
on the Phase 4bn-AK arc decision and remain paused**, and explicitly did **not**
resolve the arc question (deferring it to this memo under §17/§18).

## 12. Recovered Phase 4bn-AE decision framework

Recovered verbatim / by close paraphrase from the committed AE memo and the frozen
`pre_v002_ml_dataset_contract.py` constants.

**Allowed claim scope (§8 / `CLAIM_SCOPE_ALLOWED`).** A baseline may claim only:
(a) whether the 45 causal aggTrades features contain **short-horizon directional
information**; (b) whether the **directional sign** of the v002 small-lift result
is **reproduced** on the larger, earlier pre-v002 regime; (c) whether the
**calibration / confidence-tail** behaviour is adequate/marginal/fails.

**Forbidden claim scope (§8 / `CLAIM_SCOPE_FORBIDDEN`).** tradability;
profitability; strategy viability; execution viability; slippage/spread adequacy;
live-readiness; paper/shadow readiness; PnL; backtest validity; production
suitability; economic significance. A result that beats every statistical floor
still licenses only (a)/(b)/(c).

**Success / continue / kill criteria (§16), frozen constants.**
`SUCCESS_ACCURACY_UPLIFT_PP = 2.0` over **both** the majority and persistence
floors; `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP = 1.0` over the **majority** floor;
`SUCCESS_MACRO_F1_UPLIFT = 0.03` over the **majority** floor. The §16 KILL clause
and its "+0.14 macro-F1" v002 anchor both state the macro-F1 threshold **relative
to the majority floor** (majority→L2), which fixes the reading of the macro-F1
gate as majority-referenced.

- **KILL / `CLOSE_ML_BASELINE_ARC`** if **any** of: fails to beat both floors on
  validation accuracy by ≥ +2.0 pp; **or** fails +1.0 pp balanced-acc over majority
  **and** +0.03 macro-F1 (both fail); **or** improvement concentrated in a single
  month / minority of date-blocks; **or** holdout **reverses the sign** of the
  uplift; **or** calibration unusable (≥0.8 tail ≤ majority floor) **and**
  classification lift also fails the margins; **or** cost stats show the horizon is
  almost never economically relevant **and** the information-diagnostic lift also
  fails the margins.
- **CONTINUE / `CONTINUE_ONE_FOLLOWUP`** only if **all** of: beats both floors on
  validation accuracy by ≥ +2.0 pp **and** macro-F1 by ≥ +0.03 (majority-
  referenced); **and** holdout does not reverse the sign; **and** improvement in a
  **majority** of validation date-blocks **and** months; **and** calibration at
  least directionally usable/fixable (or, if unusable, classification lift strong
  and stable enough for a ranking-only follow-up); **and** cost stats acknowledged
  (not tradable at 15s, retains information-diagnostic value).
- Thresholds are pre-registered and **may not be relaxed after a result is seen**.

**§16 follow-up categories** (`CONTINUE_FOLLOWUP_CATEGORIES`, exactly four; a
`CONTINUE_ONE_FOLLOWUP` result authorizes **exactly one**):
1. `longer_horizon_label_memo` — longer-horizon (5m/30m/1h) label memo; new label
   layer;
2. `bookticker_midprice_data_admissibility_memo` — bookTicker / mid-price
   data-admissibility memo (bounce-free labels; new data);
3. `code_only_evaluation_framework_extension` — e.g. **block-bootstrap** inference
   framework;
4. `fixed_capacity_model_comparison_memo` — one fixed-capacity, run-once
   model-comparison memo.

**Ambiguous handling (§17).** `INVESTIGATE_AMBIGUOUS` on mixed block evidence,
validation-improves-but-holdout-does-not (without full reversal),
classification-improves-but-calibration-fails, or information-suggested-but-not-
clean. It must **not** silently become a continue; it **forces a separate,
docs-only arc-decision memo** that either closes the arc or authorizes exactly one
bounded follow-up under the §16 continue rules. **Default posture on ambiguity is
remain paused.**

**§17 / §18 arc budget and decision boundary.** The arc is **finite**: AH builder
+ run → AI diagnostics → AJ baseline run + verdict → **AK arc-decision** (current
letters). **Stopping rule:** after the baseline verdict the arc **must** either
close **or** authorize exactly one bounded follow-up; it may **not** spawn an
open-ended sequence of further memos. Every phase is separately operator-authorized.

**§19 strategy / PnL / backtest / live boundary (absolute).** No baseline result,
however strong, authorizes strategy / signals / threshold or confidence-gated
trading / backtest / PnL / position sizing / execution / live-readiness / paper /
shadow / exchange-write. Any such path requires a separate future **M0-style
mechanism-admissibility memo** clearing M0.5 cost realism at 8 bps/side · 16 bps
round-trip, execution feasibility, slippage/spread (which aggTrades-only data
cannot support — mid/book data required), label economic relevance (the 15s
strict-sign target is non-economic), strategy admissibility vs the retained
rejections, and the no-rescue constraints — **plus** separate authorization for
each of strategy/signals/PnL/backtest/paper-shadow/live/exchange-write.

**Dependence policy (§10, Option 1).** Row-level metrics are descriptive only; the
unit of decision evidence is the UTC **date/month block**; **no** per-row
significance / p-value / confidence-interval language until a future phase defines
a dependence-aware method (block bootstrap / date-level jackknife); fixed
decimation/stride (Option 2) is **reserved-not-adopted**.

**Cost-realism policy (§15).** Report the `forward_log_return_15s` distribution and
the share > 16 bps (and optionally > 8 bps), **descriptively only** — no trading
rule, no cost-aware label, no PnL. A very small > 16 bps share means 15s is
"almost never economically relevant," which **forecloses an economic reading** but
does **not by itself** kill the arc.

**Calibration / confidence-tail policy (§14).** Mandatory confidence bins,
empirical accuracy per bin, reliability curves, ≥ 0.8 tail size + accuracy,
beats-majority booleans, and a usable/ranking-only/unusable verdict. If the ≥ 0.8
tail does **not** beat the majority floor, probabilities are declared **unusable**
and "trade only when confident" is pre-emptively rejected; this **caps** claims at
§8(a)/(b) and forbids §8(c)-positive language, and is a kill **contributor** (not
alone a full kill).

## 13. AJ verdict interpretation

The Phase 4bn-AJ verdict `CONTINUE_ONE_FOLLOWUP` is **not** a trading, strategy,
PnL, backtest, or live-readiness verdict, and this memo does not read it as one. It
is the pre-registered §16 evidence verdict meaning only that the recorded evidence
**may** justify exactly one bounded follow-up decision, subject to this AK memo and
later separate operator authorization.

Applying the frozen §16 CONTINUE gates to the recorded AJ evidence (no metric
revised, no rerun):

| §16 CONTINUE gate | Recorded AJ evidence | Result |
| --- | --- | --- |
| accuracy ≥ +2.0 pp over **both** floors | +5.03 pp (majority), +2.96 pp (persistence) | **PASS** |
| macro-F1 ≥ +0.03 over the majority floor | +0.145 | **PASS** (majority-referenced) |
| holdout does not reverse the sign | holdout L2 +4.1 pp over majority; no reversal | **PASS** |
| improvement in a majority of validation date-blocks **and** months | date agreement 1.000; month agreement 1.000 (all blocks) | **PASS** |
| calibration ≥ directionally usable/fixable | ≥0.8 tail 0.633 > floor 0.4950 (overconfident in level) | **PASS** |
| cost stats acknowledged (not tradable at 15s, retains diagnostic value) | 2.47% > 16 bps; acknowledged non-economic | **PASS** |

All six CONTINUE gates are satisfied under the literal (majority-referenced)
macro-F1 reading, and **no** KILL clause fires (in particular, the cost-irrelevance
KILL requires *both* near-zero economic relevance *and* a failed information
diagnostic — the diagnostic passed decisively, so KILL is pre-registered-OFF).
The AJ `CONTINUE_ONE_FOLLOWUP` verdict is therefore consistent with the frozen §16
continue rules on its own terms. This memo neither softens a kill the rules do not
require nor upgrades ambiguity into success; it records the pre-registered mapping
faithfully.

## 14. Treatment of the macro-F1 caveat

The macro-F1 caveat is the single interpretive wrinkle and is treated explicitly,
not softened away:

- **Fact.** L2 validation macro-F1 (0.366) is **below** persistence macro-F1
  (0.402). This is caused **entirely** by the degenerate flat/zero class:
  persistence predicts flat with recall 0.162 (earning nonzero flat-class F1),
  whereas L2 — like the v002 baseline — essentially never predicts flat
  (predicted-zero rate 1.3e-5). On the two economically-meaningful **directional**
  classes, L2's per-class F1 exceeds persistence's (down 0.534 vs 0.518; up 0.563
  vs 0.524).
- **Pre-registration status.** The §16 macro-F1 gate is stated **relative to the
  majority floor** (the KILL clause and the "+0.14 macro-F1" v002 anchor both read
  majority→L2), and L2 clears it by +0.145. The pre-registration does **not** make
  persistence a macro-F1 gate for the continue decision — persistence is a floor
  for **accuracy** ("beats both floors on validation accuracy"), which L2 also
  clears (+2.96 pp). The flat-class degeneracy was **anticipated** by the
  pre-registration: §13 mandates surfacing the predicted-zero rate and the
  never-predict-flat behaviour precisely so it is not hidden, and §8 caps every
  claim at the information-diagnostic level regardless.
- **The stricter reading is recorded, not dismissed.** Under a "both-floors"
  macro-F1 reading, the result would be `INVESTIGATE_AMBIGUOUS`. Per §17/§18, an
  `INVESTIGATE_AMBIGUOUS` outcome **also** routes to this AK arc-decision memo,
  whose mandate is to resolve into close **or** exactly one bounded follow-up under
  the §16 continue rules. Because the accuracy evidence is unambiguous and strong
  (both floors cleared, all blocks agree, holdout stable, no overfitting) and the
  only wrinkle is a pre-anticipated flat-class artifact that the pre-registration's
  own thresholds do not treat as disqualifying and that §8 caps anyway, the caveat
  does **not** block a clean resolution. Both readings therefore converge on the
  **same** AK resolution.

## 15. Treatment of the 2.47% > 16 bps cost finding

Treated per §15 as **decisive for the economic reading but not for the arc**:

- Only **2.47%** of validation 15s moves (1.20% holdout) exceed the locked 16 bps
  round-trip cost; median |return| is 2.53 bps. The 15s strict-sign target is
  therefore **almost never economically relevant** at the locked cost — exactly the
  microstructure-thinness the pre-registration expected.
- This **forecloses any economic reading** of the AJ result. It is descriptive
  context only; it is **not** evidence of tradability, edge, PnL, or economic
  significance, and it authorizes **no** trading rule, cost-aware label, or
  backtest.
- Under §15/§16 it does **not** kill the arc, because the information-diagnostic
  question was answered decisively (the KILL clause needs cost-irrelevance **and**
  a failed diagnostic; only the former holds).
- It is, however, the **single most decision-relevant limitation** the arc has
  surfaced, and it is the primary driver of the follow-up selection in §16: the
  correct next question is whether directional information persists **and** becomes
  economically material at **longer horizons**, which §9 explicitly names as "where
  cost could plausibly be cleared."

## 16. Treatment of dependence / block structure

Treated per the §10 Option-1 dependence policy, unchanged and unrelaxed:

- The ~397M kept rows are **not** ~397M independent observations: aggTrades 15s
  forward labels overlap heavily, so labels are strongly autocorrelated at the
  sub-15s scale. The natural decision blocks are **275 UTC dates / 9 UTC months**.
- The AJ verdict correctly rests on **block agreement** (validation date agreement
  1.000, month agreement 1.000), **not** on row-level metrics, and uses **no**
  p-value / confidence-interval / significance language.
- Consequently, the AJ evidence supports a **descriptive** statement of stability
  ("the accuracy lift over the majority floor is positive in every evaluated
  validation date and both validation months") but **not** an inferential one. A
  dependence-aware inference method (block bootstrap / date-level jackknife) has
  **not** been built; §10 forbids significance language until it is. This is a real
  methodological gap, evaluated as a candidate follow-up in §17 (category 3), but it
  is **not** the binding limitation on the arc's relevance (the economic thinness
  of §15 is), and formalizing inference would not change the block agreement that is
  already maximal (1.000).
- The block structure also caps regime-robustness: validation and holdout both sit
  in the same late-2024 regime (§10 of the AI evidence; §11 of AE), so cross-month
  agreement within validation is a **weak** regime test. The AJ result is therefore
  read as regime-**stable within a narrow window**, not as regime-general.

## 17. Evaluation of each possible follow-up category

Exactly one may be selected under §16. Each is evaluated against the AJ evidence.

**1. Longer-horizon label memo (`longer_horizon_label_memo`, §16(a)) — SELECTED.**
The AJ evidence establishes real short-horizon directional information whose single
binding limitation is **economic thinness at 15s** (2.47% > 16 bps). §9 explicitly
records that "longer horizons are where cost could plausibly be cleared and are the
correct subject of a future label memo." A longer-horizon label memo is the most
directly responsive next docs question: does the demonstrated directional
information persist at 5m/30m/1h, and do longer-horizon **raw** moves clear the
16 bps cost materially more often? It is also the most **bounded** and
**lowest-cost** of the four — it stays within the existing aggTrades label-layer
lineage (no new data source), and it is the cheapest gate that can either
economically-invalidate the microstructure lane (if longer-horizon moves are still
rarely material) **or** motivate the heavier mid/book path (category 2) if they
are. This memo **selects** it and nothing more; it does **not** authorize any label
implementation, data generation, or new label build.

**2. bookTicker / mid-price data-admissibility memo
(`bookticker_midprice_data_admissibility_memo`, §16(b)) — REJECTED / DEFERRED.**
Genuinely important and mechanism-relevant: aggTrades-only data cannot support
spread/slippage/mid-price realism, the 15s target may embed bid-ask bounce, and any
future strategy/PnL/backtest/live path **will** require bounce-free mid/book data
(§19). But it is **premature now**: it opens a heavier new-data-source admissibility
path, and there is no point investing in bounce-free **measurement** until we know
longer-horizon raw moves are even materially large enough to clear cost. If the
selected longer-horizon memo shows longer-horizon moves routinely clear 16 bps,
mid/book admissibility becomes the natural subsequent gate. Deferred, not
foreclosed. It acquires **no** data here.

**3. Block-bootstrap inference framework
(`code_only_evaluation_framework_extension`, §16(c)) — REJECTED / DEFERRED.**
The dependence caveat is real and this would let the project make dependence-aware
inferential statements. But the AJ block agreement is already **maximal** (1.000
across all validation dates and months) and the holdout shows no reversal, so
formalizing inference would most likely confirm what the descriptive block evidence
already shows, and it would **not** touch the binding economic constraint. It is
methodological polish that is more valuable **after** the economic-materiality
question is resolved (a longer-horizon result is what would most need
dependence-aware uncertainty). Deferred. It computes **no** new inference / p-values
here.

**4. One fixed-capacity model-comparison memo
(`fixed_capacity_model_comparison_memo`, §16(d)) — REJECTED / DEFERRED.**
The AJ evidence gives no indication that **model capacity** is the bottleneck: a
single L2 linear model already extracts a stable directional signal across all
blocks. The binding constraint is **economic materiality**, not model
expressiveness, so added capacity would at best marginally raise accuracy while
leaving the 15s cost problem untouched — and it carries the **highest** risk of
drifting into open-ended model-shopping (the pre-registration warns against exactly
this). Least justified of the four. Deferred. It trains **no** model here.

## 18. Final AK decision

**`CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`.**

The pre-registered §16 continue gates are all satisfied on the recorded AJ evidence
(§13); no KILL clause fires; and the sole interpretive wrinkle (the macro-F1
caveat, §14) is a pre-anticipated flat-class artifact that the pre-registration's
own thresholds do not treat as disqualifying and that §8 caps regardless. Both the
`CONTINUE_ONE_FOLLOWUP` and the stricter `INVESTIGATE_AMBIGUOUS` readings route to
this AK memo under §17/§18, and both resolve the same way. Closing the arc would
forfeit a cleanly-demonstrated, regime-stable information-diagnostic result that
the pre-registration explicitly designed a bounded follow-up for; recording
open-ended ambiguity would violate the §18 stopping rule when a clean resolution
exists.

This is an **evidence-driven** decision, not deference to the AJ label and not a
default toward continuation: it rests on the frozen §16 gates applied to the
metrics. It is emphatically **not** a trading, strategy, PnL, backtest, economic, or
live-readiness decision — those remain absolutely barred by §19.

## 19. Selected follow-up category and why (continuing)

**Selected (exactly one): category 1 — `longer_horizon_label_memo` (§16(a)): a
longer-horizon (5m/30m/1h) label memo.**

Why: the AJ evidence establishes short-horizon directional **information** that is
real, regime-stable within the window, and reproduces the v002 sign, but whose one
binding limitation is that the 15s strict-sign target is **economically thin**
(2.47% of moves clear 16 bps) and **non-economic by design** (§9). §9 nominates the
longer-horizon label memo as the correct locus for the economic-materiality
question — "where cost could plausibly be cleared." It is the most responsive,
most bounded, and lowest-cost single next docs step, and it is the cheapest gate
that can either economically-invalidate or advance the microstructure lane.

**This selection does not start the follow-up.** Per §16/§18, the selected
longer-horizon label memo still requires a **separate future operator prompt**
before any work begins. This AK memo authorizes **no** implementation, **no** label
build, **no** data generation, **no** data read, and **no** successor execution
phase. Recommended posture: **remain paused**.

## 20. Explicit rejection / deferral of the other three categories (continuing)

For this arc decision, the other three §16 categories are **explicitly rejected /
deferred** and are **not** authorized:

- **`bookticker_midprice_data_admissibility_memo` (§16(b))** — deferred: important
  for any eventual tradability path but premature before longer-horizon economic
  materiality is established; opens a heavier new-data path; acquires no data.
- **`code_only_evaluation_framework_extension` / block-bootstrap (§16(c))** —
  deferred: methodological polish over already-maximal (1.000) block agreement; does
  not touch the binding economic constraint; more valuable after a longer-horizon
  result exists.
- **`fixed_capacity_model_comparison_memo` (§16(d))** — deferred: capacity is not
  the evidenced bottleneck; highest model-shopping-drift risk; least justified.

Selecting one follow-up **consumes** the single-follow-up budget: only the
longer-horizon label memo is licensed by this decision, and only via a separate
future operator prompt.

## 21. If closing — N/A

Not applicable; the decision is `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`, not
closure. No arc closure is recorded. (Had the evidence required closure, this memo
would have closed the arc and stated that no further ML follow-up is authorized.)

## 22. If ambiguous — N/A

Not applicable; the verdict/caveat resolved cleanly into exactly one bounded
follow-up without violating pre-registration (§14, §18). No unresolved blocker
prevents a clean decision. (Had the readings failed to reconcile with the §16
rules, this memo would have recorded `RECORD_AMBIGUOUS_REMAIN_PAUSED` with the
exact evidence gap.) The macro-F1 two-reading question is documented (§14) but is
**resolved**, not left ambiguous.

## 23. Allowed claims preserved

Preserved verbatim (§8 / `CLAIM_SCOPE_ALLOWED`). The AJ result licenses **only**:
(a) the 45 causal aggTrades features contain **short-horizon directional
information** about `forward_direction_15s` on the pre-v002 segment; (b) the
**directional sign** of the v002 small-lift result **is reproduced** on the larger,
earlier pre-v002 regime; (c) the probability outputs' **calibration/confidence
tail** beats the majority floor on accuracy but is overconfident in level — usable
for ranking/diagnostic reading, not as calibrated probabilities. This AK decision
adds **no** new claim beyond (a)/(b)/(c).

## 24. Forbidden claims preserved

Preserved verbatim (§8 / `CLAIM_SCOPE_FORBIDDEN`, §19). Nothing in this memo may be
cited as evidence of: tradability; profitability; strategy viability; execution
viability; slippage/spread adequacy; live-readiness; paper/shadow readiness; PnL;
backtest validity; production suitability; economic significance. The
2.47%-of-moves-clear-cost figure is descriptive context, **not** evidence of edge.
`forward_direction_15s` remains an **information-diagnostic**, non-economic target
that may embed bid-ask bounce (aggTrades-only, no mid/book). The locked cost
reference remains **8 bps per side / 16 bps round-trip**. The `CONTINUE` decision is
**not** a trading verdict. The §19 strategy/PnL/backtest/live boundary is absolute
and unsoftened.

## 25. Exact validation commands and results

Docs-only phase (no source/test/script changed), so no pytest/ruff/mypy required.
Run:

- `git rev-parse main` / `origin/main` / `HEAD` (pre-branch) → all
  `3e38fc87d148ed51ef23bfd76cf2f674a73fc8a0`. ✅
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`. ✅
- `git ls-files data/microstructure/` → **0 tracked**. ✅
- `git ls-files data/research/` → **0 tracked**. ✅
- `git check-ignore -v data/microstructure/` → `.gitignore:85`. ✅
- `git check-ignore -v data/research/` → `.gitignore:88`. ✅
- `.claude/scheduled_tasks.lock` → not staged, not committed (`git check-ignore`
  returns nothing; it is left untracked and excluded from the commit). ✅
- `git diff --check` → clean. ✅
- `git diff --name-status main..HEAD` (after commit) → only the two new
  `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_*.md` files. ✅
- No data-output tracked-file check → no file under `data/` staged or committed. ✅

(Exact post-commit command outputs are reproduced in the closeout and the final
operator report.)

## 26. Git status

Before commit: the two new Phase 4bn-AK docs untracked, plus the transient
`?? .claude/scheduled_tasks.lock` (not committed). No `data/` file staged. Final
committed SHA(s) and post-commit `git status --short` are reproduced in the
closeout and the final operator report.

## 27. Result state

`ML_ARC_DECISION_RECORDED__EXACTLY_ONE_BOUNDED_FOLLOWUP_SELECTED__NO_STRATEGY__FOLLOWUP_NOT_STARTED__REMAIN_PAUSED`

## 28. Recommended next state

**Remain paused.** The ML arc decision is recorded: `CONTINUE_EXACTLY_ONE_BOUNDED_
FOLLOWUP`, with exactly one follow-up selected — the longer-horizon (5m/30m/1h)
label memo — and the other three §16 categories explicitly deferred. The selected
follow-up is **not started** and requires a **separate future operator prompt**
before any work begins. No strategy/signals/PnL/backtest/paper-shadow/live/
exchange-write path is authorized (that remains behind the §19 M0-style gate). The
operator may: remain paused; request a merge prompt for Phase 4bn-AK; or, later and
separately, authorize the selected longer-horizon label memo.

## 29. current-project-state.md update note

`current-project-state.md` is **left unchanged** by this phase. The update
convention at this point in the arc is **not clear/consistent**: the docs-only
decision memos Phase 4bn-AE and 4bn-AG each added a `current-project-state.md`
paragraph, but the three most recent phases — Phase 4bn-AH, 4bn-AI, and 4bn-AJ
(including the AJ verdict phase, the immediate predecessor) — did **not** (no
paragraph exists for any of them, and their tracked-file lists exclude the state
doc). The state doc is additionally flagged by the Phase 4bn-AE external review as
an oversized/stale single-source-of-truth pending a consolidation memo. Per the
operator instruction ("if there is no clear current-project-state update convention
for this point, do not update it; record that it remains unchanged"), and matching
the immediate AH/AI/AJ precedent, this phase records the arc decision **only** in
this report + closeout and leaves `current-project-state.md` untouched. Should the
operator prefer an additive paragraph at merge time, that can be added under a
later merge prompt.

## 30. Explicit no-successor execution statement

Phase 4bn-AK authorizes **no** successor execution phase. It does **not**, and does
not authorize anyone to: implement, run, or start the selected longer-horizon label
memo (or any follow-up); create the selected follow-up's prompt; build any label
layer or generate any data; read any feature/label Parquet / v002 terminal / sealed
test / raw zip / AH / AJ data artefact; train / score / predict / infer; run new
diagnostics; perform feature selection / threshold optimization / model selection /
hyperparameter search; rerun the AH builder, AI diagnostics, or AJ baselines;
acquire data or call any endpoint; create/mutate any dataset or baseline namespace;
do strategy / signals / PnL / backtest / Sharpe / hit-rate / position sizing /
execution / paper / shadow / live-readiness / deployment / exchange-write; use
credentials / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user stream; or
authorize any Phase 5 or any successor phase. Every retained verdict and project
lock (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1;
§11.6 = 8 bps per side / 16 bps round-trip; the Phase 4ak M0 twelve-clause gate;
Phase 4al no-rescue; Phase 4aw `flip_research_eligible(...)` always-raises invariant
— never invoked; Phase 4bb-F sidecar policy; the Phase 4bn-AA split artefact, 4bn-AB
source-admissibility posture, 4bn-AC ML dataset contract, 4bn-AE pre-registration
amendment, and the 4bn-AF..AJ results) is preserved verbatim. Phase 4 canonical
remains unauthorized. The selected follow-up begins only under a separate future
operator prompt.
