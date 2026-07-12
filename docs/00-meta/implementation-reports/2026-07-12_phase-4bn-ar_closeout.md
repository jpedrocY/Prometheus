# Phase 4bn-AR — Closeout

## Branch

`phase-4bn-ar/fixed-longhorizon-baseline-run-verdict`

## Base SHA

`5a1d2c88a35ffb9e48f5db1c95ee66b27c1885fc` (main == origin/main == HEAD at branch
time; tip after the Phase 4bn-AQ merge closeout).

## Phase type

Fixed, **run-once, no-search** long-horizon baseline evaluation — phase 2 of the
Phase 4bn-AP `LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN` architecture,
over the verified Phase 4bn-AQ dataset specification. Information-diagnostic only; no
strategy / PnL / backtest / live path.

## Committed files (source / tests / scripts / docs only)

- `src/prometheus/research/microstructure/longhorizon_fixed_baseline_run_v001.py`
- `src/prometheus/research/microstructure/longhorizon_baseline_verdict_v001.py`
- `scripts/phase4bn_ar_run_fixed_longhorizon_baselines.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_contract.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_metrics.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_verdict.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_run.py`
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_fixed-longhorizon-baseline-run-verdict.md`
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_closeout.md`

**No data / model artefact committed.** `current-project-state.md` unchanged.

## Local output namespace

`data/research/microstructure/ml_baselines/longhorizon_pre_v001_fixed_run/`
(gitignored, `.gitignore:88`; 12 compact JSON artefacts + 12 `.sha256` sidecars;
217,859 bytes / ~213 KiB total; one-run/no-overwrite guard enforced).

## Source / data bindings

- dataset family `microstructure_ml_dataset_longhorizon_pre_v001`; contract
  `microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001`;
  `dataset_contract_hash a310eabf…c3873`;
- features: 45; feature-list hash `8e705ba8…3df9`; feature manifest `4881eb87…4b52`;
  feature config `0726b41d…d114c`; feature gate `db731d1b…6d8ab08`;
- labels: `microstructure_labels_longhorizon_aggtrades_v001`; `label_config_hash
  edaeafde…c118`; AN manifest `b1ee9afd…f4a0`;
- split `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` (train 214 /
  embargo 2 / validation 45 / holdout 14); transform
  `subtract_train_mean_divide_by_max_train_std_epsilon` (ε 1e-8; fit on train only;
  applied, never recomputed).

## Frozen config

3 baselines (majority / persistence = `sign(rolling_log_return_past_window_60s)` /
L2 multinomial-logistic). L2: epochs 1, batch 8192, lr 0.1, L2 1e-4, grad-clip 10.0,
seed 20260528, class order (−1, 0, +1). One independent L2 per horizon (5m primary;
30m/1h secondary). No search of any kind.

## Validation results (tests / lint / type / integrity)

49 AR tests pass; AJ + AQ suites pass; import-boundary tests pass; ruff clean; mypy
clean on the two new modules; `git diff --check` clean; all AR + AQ sidecars verify;
AQ namespace byte-identical after the run; 0 tracked data files.

## Model-run outcome (concise)

Runtime 2,075.6 s (~34.6 min). Train 304,816,127 rows/horizon (37,315 batches each);
eval 92.1M rows/horizon (validation 68,578,296 + per-horizon holdout). Majority class
= +1 ("up") for all horizons. Numerical guard: all L2 weights finite.

## Exact metrics justifying the verdict (5m primary)

Validation accuracy: majority 0.51225 / persistence 0.48876 / **L2 0.51004**.
Validation balanced-acc: majority 0.33333 / **L2 0.34113**. Validation macro-F1:
majority 0.22582 / **L2 0.33958**. L2 uplift (validation): vs majority **−0.222 pp**,
vs persistence **+2.128 pp**, balanced-acc vs majority **+0.779 pp**, macro-F1 vs
majority **+0.1138**. Date blocks beating both floors 23/45 (0.511); month blocks
1/2. Holdout L2 uplift: vs majority +0.368 pp, vs persistence +2.097 pp → **no full
reversal**. ≥0.8 confidence tail: n 1,562,179, acc 0.4966 < majority floor 0.5122 →
does **not** beat floor; calibration **unusable** (ECE 0.058). Secondaries (30m/1h)
not positive (fail the majority-floor accuracy bar), so cannot upgrade the primary.

## Exact final verdict

**`INVESTIGATE_AMBIGUOUS`** — CONTINUE fails (accuracy-vs-majority, balanced-accuracy,
month-block, and ≥0.8-tail criteria all fail); no hard-negative holdout reversal; two
Phase 4bn-AP ambiguous conditions match (`mixed_date_and_month_block_evidence`,
`information_suggested_but_not_clean`). Authorizes no further run.

## Claim-scope interpretation

Allowed (Phase 4bn-AE §8 a/b/c): a directional-**information** diagnostic — the
frozen 45-feature set carries measurable long-horizon directional information over
the **persistence** floor (~+2 pp accuracy at 5m; +~0.11 macro-F1 across horizons;
holding on holdout), but not a clean lift over the strong majority floor and not a
usable 5m high-confidence tail. Forbidden: any tradability / profitability / edge /
PnL / strategy / execution / backtest / live claim. Raw-move materiality shares and
the 8/16 bps cost are descriptive context only and entered no target/model/verdict.

## Boundary confirmations

No v002 terminal / sealed test / test rows read (`test_rows_loaded = 0`). No AH / AJ
/ AN / AQ namespace mutated; AQ re-verified byte-identical. No AH / AI / AJ / AN / AQ
builder or diagnostic rerun. No second run; no seed / config change. No row-level
prediction, model binary, or transformed matrix written. No data / model artefact
committed; `.claude/scheduled_tasks.lock` not committed. All published authorization
flags remain `false`; `flip_research_eligible(...)` never invoked; `research_eligible`
unchanged.

## Remaining blockers before any follow-up ML work

A follow-up requires a **separate operator authorization**. The `INVESTIGATE_AMBIGUOUS`
verdict recommends at most a future **docs-only** decision memo (not a model run) to
weigh whether persistence-floor-only information — without a majority-floor lift,
clean block agreement, or usable 5m calibration — justifies any bounded follow-up,
and if so to pre-register it. No follow-up model / feature / calibration / threshold
work is authorized by this phase.

## Remaining blockers before strategy / PnL / backtest / live

Unchanged and absolute: the Phase 4bn-AE §19 M0-style mechanism-admissibility gate.
aggTrades-only data cannot express spread / slippage / executable mid / depth /
impact, so no strategy / signals / PnL / backtest / Sharpe / hit-rate / paper /
shadow / live / exchange-write path is admissible. Each such capability needs its own
separate authorization behind the M0 gate; none is authorized.

## Recommended state

**Remain paused.**

## Explicit no-successor execution statement

Phase 4bn-AR authorizes **no** successor execution phase and generates no successor
prompt. Do not merge to main and do not push unless explicitly instructed later; do
not generate a merge-closeout or a successor prompt unless explicitly instructed
later. Every retained project lock and verdict is preserved verbatim (Phase 4aw
`flip_research_eligible` always-raises invariant — never invoked; Phase 4bb-F sidecar
policy; Phase 4bn-AE claim scope + §19 M0 boundary; Phase 4bn-AP frozen model +
verdict contract; Phase 4bn-AQ dataset identity / bindings / transform / split /
proof).

## Result state

`LONGHORIZON_FIXED_BASELINE_RUN_COMPLETE__INVESTIGATE_AMBIGUOUS_RECORDED__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`
