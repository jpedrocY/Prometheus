# Phase 4bn-AO — Longer-Horizon Label Descriptive Diagnostics, No Models

## 1. Branch

`phase-4bn-ao/longhorizon-label-descriptive-diagnostics-no-models`

## 2. Base SHA

`7e70b13a6753f7f77f60051182f259831a78b69e`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AN merge
closeout. Verified in sync before branching.)

## 3. Phase type and strict scope

Docs + **local-JSON-artefact-only** descriptive diagnostics memo. It inspects the
five Phase 4bn-AN `_manifest/*.json` artefacts (+ their `.sha256` sidecars),
summarizes the built long-horizon label layer's integrity and descriptive
materiality, and recommends (or declines) a **future, separately authorized**
docs-only ML baseline preregistration/evaluation-contract memo. It reads **no
Parquet** (neither the 275 built label files nor any source feature/normalized
Parquet), runs **no model**, mutates **nothing**, reruns **no** build, and
authorizes **no** successor execution phase.

## 4. Files created / modified

Created (committed — docs only):

- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ao_longhorizon-label-descriptive-diagnostics-no-models.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ao_closeout.md`.

No source, test, script, manifest, gate report, sidecar, split file, ML config, or
`data/` artefact was created or modified. `current-project-state.md` is **unchanged**
(see §31 note). No data file was committed.

## 5. Exact documents / source inspected

Read-only (committed docs + committed source; README not treated as authority): the
Phase 4bn-AE preregistration; the Phase 4bn-AH / AI / AJ / AK / AL / AM / AN reports +
closeouts + merge-closeouts; `docs/00-meta/process/`; and committed source
`pre_v002_ml_dataset_contract.py`, `labels_schema_v002.py`,
`longhorizon_labels_schema_v001.py`, `longhorizon_labels_compute_v001.py`,
`scripts/phase4bn_an_build_longhorizon_labels.py`.

## 6. Exact local JSON artefacts inspected

Only the five Phase 4bn-AN output-namespace JSON artefacts + their `.sha256` sidecars
under
`data/research/microstructure/labels/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/_manifest/`:
`…manifest.json`, `…leakage_split_censoring_proof.json`,
`…continuous_return_cost_summary.json`, `…build_run_record.json`,
`…sidecar_inventory.json`. All five sidecars were re-verified (each JSON body SHA256
matches its `.sha256`).

## 7. Confirmation no Parquet files were read

Confirmed. **No** built per-day label Parquet, **no** source feature Parquet, **no**
source normalized Parquet, **no** raw zip was read. Only the five `_manifest` JSON
artefacts (+ sidecars) were opened, plus `git` tracked-state checks.

## 8. Confirmation no output namespace mutation occurred

Confirmed. Nothing under the Phase 4bn-AN output namespace was created, overwritten,
deleted, refreshed, or re-hashed en masse. The five JSON artefacts were opened
read-only.

## 9. Confirmation no build rerun occurred

Confirmed. `scripts/phase4bn_an_build_longhorizon_labels.py` was **not** executed.

## 10. Confirmation no v002 terminal / sealed test / test rows

Confirmed from the AN proof (re-read): `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; `test_rows_loaded = 0`. This phase itself read no
data window at all.

## 11. Confirmation no AH/AJ namespace mutation

Confirmed. The Phase 4bn-AH ML-dataset namespace and the Phase 4bn-AJ baseline
namespace were **not** read, mutated, refreshed, created, or deleted.

## 12. Confirmation no AH builder / AI diagnostics / AJ baseline rerun

Confirmed. None was executed. No model was trained/scored/evaluated; no prior-phase
metric was recomputed (all quoted verbatim).

## 13. AN build summary

Phase 4bn-AN built the new sibling family
`microstructure_labels_longhorizon_aggtrades_v001` (horizons 5m/30m/1h) over the
admitted pre-v002 aggTrades segment: 275 partitions / 400,001,695 rows, one
controlled run (~4,716 s), ~11.12 GiB, local/gitignored, `label_config_hash`
`edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`. Strict-sign
direction policy; per-horizon envelope-terminal censoring; the descriptive
continuous-return / cost-clearing summaries this memo reads.

## 14. Artefact integrity summary

**Internally consistent and complete.** From the five JSON artefacts:

- **Identity:** family `microstructure_labels_longhorizon_aggtrades_v001`; contract
  `microstructure_longhorizon_label_aggtrades_pre_v002_contract_v001`; sibling of the
  frozen `microstructure_labels_aggtrades_v001`; horizons `[5m,30m,1h]` /
  `[300000,1800000,3600000]` ms; lead `5m`; `label_config_hash` `edaeafde…`.
- **Counts:** `date_count = 275`; `total_row_count = 400,001,695`; `full_segment_run
  = true`; footprint `11,940,496,483` bytes.
- **Per-day inventory:** 275 entries, **275 distinct dates**, `Σ row_count =
  400,001,695`. Sidecar inventory: **275** entries.
- **Non-authorization flags:** all eight `false`; `data_committed = false`;
  `frozen_v002_family_mutated = false`.
- **All five JSON sidecars verify** (body SHA256 == `.sha256`).
- **Holdout row reconciliation (minor, benign):** the AN per-day inventory holdout
  total is **23,535,902** rows (labels keep *all* feature rows per the
  `keep_all_feature_rows` policy), which with train 304,816,127 + embargo 3,071,370 +
  validation 68,578,296 sums to **exactly 400,001,695**. The AN report §26 cited
  holdout **23,535,860** — the Phase 4bn-AH ML-dataset holdout *kept*-count (42 fewer,
  because AH applied its own 42-row censored drop when building the 15s ML dataset).
  The AN label artefacts are authoritative and self-consistent; no build defect — a
  citation nuance only.

## 15. Leakage / scope invariant summary

All preserved (from the AN proof JSON):

- `admitted_source_scope_only = true`; `v002_terminal_window_read = false`;
  `sealed_test_split_touched = false`; `test_rows_loaded = 0`.
- **Per-horizon earlier-model-split boundary-crossing rows = 0** (total 0 across
  train/validation × 5m/30m/1h). `embargo_rows_used_in_model_splits = 0`.
- `max_horizon_ms = 3,600,000` < `one_day_purge_ms = 86,400,000`
  (`max_horizon_lt_embargo = true`) — the 1-day embargo strictly exceeds the 1h max
  horizon, so no earlier-model-split forward endpoint can reach a later model split.
- `invalid_price_row_count_total = 0`; `no_nan_inf_in_non_null_numeric = true`;
  `forbidden_substring_scan_clean = true`.
- No AH/AJ namespace mutation; no source manifest / gate / sidecar / split file
  mutation (the AN branch diff was six added files only).

## 16. Split / row / censoring summary and per-horizon descriptive materiality

Split totals (per-day inventory): **train 304,816,127** (214 dates), **embargo
3,071,370** (2 dates), **validation 68,578,296** (45 dates), **holdout 23,535,902**
(14 dates). Per-horizon envelope-terminal censoring (holdout tail only; train +
validation 0): **5m 1,528 / 30m 9,916 / 1h 23,650** — monotone in horizon, ~0.006% of
all rows even at 1h. Invalid prices 0.

Descriptive `|forward_log_return_H|` (bps; histogram-estimated percentiles at 0.05 bps
resolution; exact shares), per horizon × split:

| split:H | support | median | p90 | p99 | > 8 bps | > 16 bps | class −1/0/+1 (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| train:5m | 304,816,127 | 11.43 | 41.9 | 115.4 | 62.09% | 37.80% | 49.3/0.06/50.6 |
| train:30m | 304,816,127 | 25.33 | 92.2 | 238.6 | 81.61% | 65.27% | 48.8/0.02/51.2 |
| train:1h | 304,816,127 | 34.43 | 126.7 | 318.7 | 86.43% | 73.70% | 48.8/0.02/51.2 |
| validation:5m | 68,578,296 | 10.58 | 37.5 | 87.0 | 59.38% | 34.95% | 48.7/0.06/51.2 |
| validation:30m | 68,578,296 | 24.48 | 84.3 | 189.6 | 81.05% | 64.28% | 47.1/0.02/52.9 |
| validation:1h | 68,578,296 | 33.08 | 117.9 | 248.8 | 85.91% | 72.72% | 46.5/0.02/53.5 |
| holdout:5m | 23,534,374 | 10.73 | 32.4 | 60.3 | 60.65% | 33.80% | 49.5/0.05/50.4 |
| holdout:30m | 23,525,986 | 23.98 | 71.0 | 129.6 | 81.87% | 64.87% | 47.8/0.02/52.1 |
| holdout:1h | 23,512,252 | 32.68 | 94.4 | 165.0 | 86.40% | 73.29% | 46.2/0.01/53.8 |

(Summary "support" = non-null non-censored rows; the holdout support totals differ
from the inventory holdout row count exactly by the per-horizon censored counts.)

## 17. 15s vs 5m / 30m / 1h materiality comparison

At the **descriptive raw-move** level, longer horizons are dramatically more
cost-relevant than 15s. Validation share of `|move| > 16 bps` round-trip:

| horizon | validation share > 16 bps |
| --- | --- |
| 15s (Phase 4bn-AJ reference) | **2.47%** |
| 5m | **34.95%** |
| 30m | **64.28%** |
| 1h | **72.72%** |

Median absolute move: 15s ≈ 2.53 bps (AJ) → 5m ≈ 10–11 bps → 30m ≈ 24–25 bps → 1h ≈
33–34 bps. The share and magnitude rise monotonically and are **stable across all
three chronological split blocks** (train/validation/holdout agree closely per
horizon). This resolves, at the label-materiality level, the "economic thinness at
15s" limitation that Phase 4bn-AJ/AK/AL identified: longer-horizon raw last-trade
moves clear the locked round-trip cost far more often.

## 18. Direction / class-balance summary

`forward_direction_H` is near-binary with a tiny exactly-flat class, matching the
Phase 4bn-AI 15s structure. The flat (0) class shrinks with horizon (~0.06% at 5m →
~0.01–0.02% at 30m/1h — fewer exactly-equal reference prices over longer windows). A
small but consistent **up-skew** appears and grows with horizon (e.g. validation +1
class 51.2% → 52.9% → 53.5%; holdout up to 53.8%), consistent with mild positive price
drift over the 2024 pre-v002 window. This skew means the majority-class floor for a
future baseline is modestly above 50% and rises with horizon — a pre-registration
detail, not an edge.

## 19. Longer-horizon risk assessment

The strong materiality numbers must **not** be over-read. Real risks that a future
evaluation must confront:

- **Materiality ≠ predictability.** Larger raw moves clearing cost is a property of the
  return *distribution*, not evidence that the 45 short-memory microstructure features
  can *predict* the direction of a 5m/30m/1h move. That is the open question — unmeasured
  here.
- **Feature–target signal decay.** The features are short-memory (order-flow imbalance,
  trade intensity, recent past-window returns); their predictive link to a 1h-ahead
  direction is very plausibly much weaker than to 15s. The AJ 15s directional lift
  (+5.03 pp) may attenuate or vanish at longer horizons.
- **Lower effective independence / heavier overlap.** 15s labels already overlap
  heavily; at 30m/1h consecutive rows' forward windows overlap almost entirely,
  collapsing the effective independent-sample count. The §10 date/month block structure
  (275 dates / 9 months) becomes even more binding — decision evidence must stay at the
  block level, never per-row significance.
- **Regime narrowness.** Validation and holdout both sit in the same late-2024 regime;
  cross-block agreement within that window is a weak regime-generalisation test.
- **30m / 1h "material by magnitude, not necessarily predictable."** These horizons have
  the largest cost-clearing shares but the weakest plausible feature→target link — treat
  any favourable future result there with particular caution.
- **aggTrades-only limitation (unchanged).** No spread, slippage, or mid-price realism;
  the labels are last-trade-price moves that may embed bid-ask bounce (reduced at longer
  horizons but not eliminated). Materiality here can never establish execution viability.
- **Direction skew.** The mild up-skew (§18) must be handled by pre-registered
  majority/persistence floors so a "predict up" degenerate baseline is not mistaken for
  signal.
- **Censoring.** Small but grows with horizon and is confined to the holdout tail; a
  future evaluation must account for the slightly reduced holdout support at 1h.

## 20. Claim-scope interpretation

Within Phase 4bn-AE §8: this memo asserts only (a) **artefact integrity** (the AN
long-horizon label layer is internally consistent, leakage-safe, and complete) and (b)
a **descriptive label-materiality** reading (longer-horizon raw moves clear the locked
cost far more often than 15s). It asserts **no** predictive, tradability, or economic
claim. The §8 forbidden scope (tradability / profitability / strategy / execution /
slippage-spread / live / paper-shadow / PnL / backtest / production / economic
significance) is preserved, and the §19 M0-style mechanism-admissibility gate for any
future strategy/PnL/backtest/live path is **unsoftened**.

## 21. Final AO decision

**`RECOMMEND_LONGHORIZON_ML_BASELINE_PREREGISTRATION_MEMO_NEXT`.**

Reasoning (evidence-driven; not over-reacting to the large cost-clearing shares; not
biased toward closing):

- **The built labels are integrity-clean and complete** (§14–§15): 275/275 dates,
  400,001,695 rows, all invariants preserved, all sidecars verify — they are a sound
  substrate for a *future* evaluation.
- **The one limitation the whole arc has circled — 15s economic thinness — is resolved
  at the label-materiality level** (§17): longer-horizon moves clear cost far more
  often. This makes the *next* question — does directional **information** survive at
  the horizons where cost is materially clearable? — both well-posed and worth a
  pre-registered test.
- **Closing (option B) would be premature.** The predictability question is genuinely
  open and answerable by a fixed, no-strategy baseline; declining it on unmeasured
  pessimism repeats the error Phase 4bn-AL warned against. **Insufficient-evidence
  (option C) does not apply** — the JSON diagnostics are complete and sufficient to
  decide *whether to recommend a preregistration memo* (they are; the unmeasured
  predictability is precisely what that memo would set up to test, not a blocker to
  recommending it).
- The correct, bounded next step is therefore a **docs-only preregistration /
  evaluation-contract memo** that freezes success/kill criteria *before* any model runs
  — exactly as Phase 4bn-AE did for the 15s AJ baseline.

This recommendation authorizes **no** ML, **no** row-level Parquet read, and **no**
successor phase.

## 22. Recommended future preregistration memo scope (option A)

Recommend **exactly one** future **docs-only** phase: a long-horizon **ML baseline
preregistration / evaluation-contract memo**. At a high level it must decide:

- **Target horizon(s):** recommend **5m as the primary/lead** target (best
  signal-persistence-vs-materiality tradeoff), with **30m and 1h as secondary
  diagnostic** targets (report but weight cautiously given weaker plausible
  predictability); the memo must justify whether to evaluate 5m-only or all three.
- **Baseline families:** fixed, run-once baselines mirroring Phase 4bn-AJ — majority
  floor, persistence, and an L2 multinomial-logistic with **frozen** hyperparameters;
  **no** model selection, no capacity search.
- **Train/validation/holdout treatment:** reuse the existing pre-v002 chrono split +
  1-day embargo; leakage-safe; train-only transform; decision evidence at the UTC
  date/month **block** level (overlap is heavier at long horizons — no per-row
  significance).
- **Dependence / block evidence:** 275 dates / 9 months; block-agreement and holdout
  no-reversal, not p-values; a dependence-aware method remains reserved-not-adopted.
- **Metrics:** the Phase 4bn-AE §13 mandatory registry (accuracy / balanced-accuracy /
  macro-F1 vs **both** majority and persistence floors; calibration reliability + ≥0.8
  confidence-tail; predicted-zero rate; cost realism reported **descriptively**).
- **Cost / materiality interpretation:** the §17 descriptive shares are context only;
  claims capped at Phase 4bn-AE §8(a)/(b)/(c); **non-economic** target reading preserved.
- **Kill / continue criteria:** pre-registered *before* any result is seen and **not
  relaxed afterward** (mirroring Phase 4bn-AE §16), keyed to accuracy uplift over both
  floors, block-agreement, holdout non-reversal, and calibration.
- **Absolute boundary:** the memo must restate that **no** baseline result authorizes
  strategy / signals / PnL / backtest / paper-shadow / live / exchange-write — that
  remains behind the §19 M0-style mechanism-admissibility gate, and aggTrades-only data
  cannot support the required spread/slippage/mid realism.

It must also record that the evaluation itself (any **row-level read** of the built
long-horizon labels + features, or building a long-horizon ML dataset) is a **further,
separately authorized** step **beyond** the preregistration memo — mirroring the
AH (dataset build) → AJ (baseline run) sequence.

## 23. No prompt generated / no ML authorized (option A)

This memo **does not generate** the recommended preregistration memo's prompt and
**does not authorize** any ML, any row-level Parquet read, any dataset build, or any
successor execution phase. The recommended memo is itself **docs-only** and begins only
under a **separate future operator prompt**; the evaluation it would pre-register needs
its own further separate authorization beyond it.

## 24. If no ML recommended — N/A

Not applicable; the decision is
`RECOMMEND_LONGHORIZON_ML_BASELINE_PREREGISTRATION_MEMO_NEXT`. (Had the labels been
unsuitable or ML unwarranted, this memo would have recorded
`RECOMMEND_NO_ML_OVER_LONGHORIZON_LABELS` with the reason and remained paused.)

## 25. If insufficient evidence — N/A

Not applicable; all five JSON artefacts were present, valid, and internally consistent
(§14). (Had an artefact been missing or invalid, this memo would have stopped and
recorded `RECORD_INSUFFICIENT_LONGHORIZON_DIAGNOSTIC_EVIDENCE` with the exact gap, per
the prompt's fail-closed instruction — no Parquet fallback, no rebuild.)

## 26. Allowed claims preserved

Preserved verbatim (Phase 4bn-AE §8): (a) short-horizon directional information; (b)
v002 small-lift sign reproduction; (c) calibration/confidence-tail assessment. This
memo adds only **artefact-integrity** and **descriptive label-materiality** readings of
the AN long-horizon labels; it asserts no new predictive or economic claim.

## 27. Forbidden claims preserved

Preserved verbatim (Phase 4bn-AE §8 / §19). Nothing here may be cited as evidence of
tradability, profitability, economic edge, PnL, strategy viability, backtest validity,
execution viability, slippage/spread adequacy, or live-readiness. **The large
30m/1h cost-clearing shares are descriptive raw-move-distribution properties only — not
predictive edge and not tradability.** aggTrades-only data cannot express
spread/slippage/mid-price realism. The locked cost reference remains 8 bps/side · 16 bps
round-trip. The §19 M0 gate is unsoftened.

## 28. Validation commands and results

Docs + local-JSON-only phase (no source/test changed), so no pytest/ruff/mypy required.

- `git rev-parse main`/`origin/main`/`HEAD` (pre-branch) → all
  `7e70b13a6753f7f77f60051182f259831a78b69e`. ✅
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`. ✅
- `git checkout -b phase-4bn-ao/longhorizon-label-descriptive-diagnostics-no-models` at
  base SHA. ✅
- Verified the **5** AN `_manifest` JSON sidecars (body SHA256 == `.sha256`): all OK. ✅
- Read only those 5 JSON artefacts; **no Parquet read**; **no namespace mutation**;
  **no build rerun**. ✅
- `git ls-files data/microstructure/` / `data/research/` → **0 tracked**. ✅
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`. ✅
- `git diff --check` → clean. ✅
- `git diff --name-status main..HEAD` (after commit) → only the two Phase 4bn-AO docs. ✅
- No data-output tracked-file check → no file under `data/` staged or committed. ✅

## 29. Git status

Before commit: the two new Phase 4bn-AO docs untracked, plus the transient
`?? .claude/scheduled_tasks.lock` (not committed). No `data/` file staged. The
~11.12 GiB AN label layer under `data/research/…` remains gitignored, untracked, and
unmutated. Final committed SHA and post-commit `git status --short` are reproduced in
the closeout and the final operator report.

## 30. Result state

`LONGHORIZON_LABEL_DIAGNOSTICS_RECORDED__ML_BASELINE_PREREGISTRATION_MEMO_RECOMMENDED__NO_ML__NO_PARQUET_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## 31. Recommended next state

**Remain paused.** The long-horizon label diagnostics are recorded; the labels are
integrity-clean and descriptively far more cost-relevant than 15s. Recommended next
step: exactly one **docs-only** ML baseline preregistration/evaluation-contract memo,
**not started**, requiring a **separate future operator prompt**. No ML, no row-level
Parquet read, no dataset build, no strategy/PnL/backtest/live path is authorized (each
requires its own separate authorization; any trading path remains behind the §19 M0
gate). `current-project-state.md` is left unchanged, matching the immediate Phase
4bn-AH..AN precedent (the update convention at this arc point is not clear/consistent;
per the operator instruction it is not updated and is recorded here as unchanged).

## 32. Explicit no-successor execution statement

Phase 4bn-AO authorizes **no** successor execution phase. It does **not**, and does not
authorize anyone to: generate the recommended preregistration memo's prompt; run any ML
/ training / scoring / prediction / inference; read any built label Parquet or source
Parquet for row-level analysis; build any ML/dataset/label namespace; perform feature
selection / threshold optimization / model selection / hyperparameter search /
calibration training / confidence-tail selection; rerun the AN build, the AH builder,
the AI diagnostics, or the AJ baselines; do strategy / signals / PnL / backtest / Sharpe
/ hit-rate / position sizing / execution / paper / shadow / live-readiness / deployment
/ exchange-write; acquire data or call any endpoint; use credentials / `.env` /
`.mcp.json` / MCP / Graphify / WebSocket / user stream; or authorize any Phase 5 /
successor phase. Every retained verdict and project lock (H0 / R3 / R1a / R1b-narrow /
R2 / F1 / D1-A / 5m thread / V2 / G1 / C1; 8 bps/side · 16 bps round-trip; the Phase 4ak
M0 twelve-clause gate; Phase 4al no-rescue; the Phase 4aw `flip_research_eligible(...)`
always-raises invariant — never invoked; Phase 4bb-F sidecar policy; the Phase 4bn-AA
split artefact, 4bn-AC ML dataset contract, 4bn-AE preregistration claim-scope, and the
4bn-AH..AN results including the AK single-follow-up selection, the AL/AM
recommendations, and the AN build + no-ML/no-strategy/no-successor boundary) is
preserved verbatim. Phase 4 canonical remains unauthorized. Do not merge to main and do
not push unless explicitly instructed in a later prompt; do not generate a
merge-closeout or the recommended next prompt unless explicitly instructed later.
