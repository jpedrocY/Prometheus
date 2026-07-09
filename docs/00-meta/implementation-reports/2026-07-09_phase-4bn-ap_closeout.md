# Phase 4bn-AP — Closeout

## Branch

`phase-4bn-ap/longhorizon-ml-baseline-preregistration-contract`

## Base SHA

`4633a5ff5ddc9f418694b99990ffde8b2eacd161`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AO merge
closeout.)

## Phase type

Docs-only **long-horizon ML baseline preregistration / evaluation-contract memo**. Freezes
the design of a future, separately authorized long-horizon baseline evaluation; runs
nothing. No Parquet read; no ML; no namespace mutation; no successor execution authorized.

## Files created / modified

Created (committed — docs only):

- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ap_longhorizon-ml-baseline-preregistration-contract.md`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ap_closeout.md` (this file)

No source / test / script / config / manifest / gate / sidecar / split / ML-config /
`data/` artefact created or modified. `current-project-state.md` left unchanged (report
§39).

## Validation commands

- `git rev-parse main`/`origin/main`/`HEAD` (pre-branch) → all
  `4633a5ff5ddc9f418694b99990ffde8b2eacd161`.
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`;
  `git diff --name-only` (tracked) → empty.
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`.
- `git diff --check` → clean; `git diff --name-status main..HEAD` (after commit) → only
  the two Phase 4bn-AP docs.
- No Parquet read; no AN JSON re-read; no namespace mutation; no pytest/ruff/mypy required
  (docs-only).

## Concise preregistration outcome

The future long-horizon baseline evaluation is pre-registered at the design level.
Architecture: **`LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN`** (AH→AJ two-step).
Primary target **`forward_direction_5m`** (30m/1h secondary diagnostic only). Features: the
frozen 45-feature AH allowlist (labels are targets, not features; no feature selection).
Split: existing pre-v002 chrono split + 1-day embargo; v002/sealed/test excluded;
`test_rows_loaded = 0`; per-horizon censored labels excluded from that horizon's target.
Baselines (frozen, run-once): majority; persistence = `sign(rolling_log_return_past_window_60s)`
(horizon-matched persistence **rejected** — no 5m/30m/1h past-window feature exists, and no
new feature may be created); L2-logistic with frozen constants (epochs 1, batch 8192,
lr 0.1, L2 1e-4, grad-clip 10, seed 20260528, train-only standardization). Metrics: AE §13
registry vs **both** majority and persistence floors + block agreement + holdout
non-reversal + calibration/tail; **no** PnL/Sharpe/trade/turnover. Kill/continue: AE §16
frozen thresholds verbatim on 5m (accuracy ≥ +2.0 pp over both floors; macro-F1 ≥ +0.03
over majority; balanced-acc ≥ +1.0 pp over majority; block-majority agreement; holdout
non-reversal) → `CONTINUE_ONE_BOUNDED_FOLLOWUP` / `INVESTIGATE_AMBIGUOUS` /
`STOP_LONGHORIZON_ML_ARC`. Dependence: block-level (275 dates / 9 months; no per-row
significance; block bootstrap reserved-not-adopted). Cost 8/16 bps descriptive only; §19
M0 gate unsoftened.

## Final AP decision

**`RECOMMEND_LONGHORIZON_ML_DATASET_BUILD_AUTHORIZATION_MEMO_NEXT`** (option A).

## Recommended future authorization (if any)

Exactly one future **long-horizon ML dataset-build authorization phase** (data-reading, no
models): bind the AH 45-feature source ↔ AN long-horizon label family (`label_config_hash`
`edaeafde…`) over the admitted pre-v002 segment; emit a compact leakage-proof dataset spec
+ split index + train-only transform + source binding + sidecars (Phase 4bb-F, 125 GiB cap,
budget preflight); v002/sealed/test excluded; all non-authorization flags false;
local/gitignored; no data committed. The **fixed baseline run is a further separate
authorization after** this build. **No prompt generated; no evaluation/ML authorized.**

## Explicit boundary confirmations

- No Parquet read (no built labels, no source feature/normalized, no raw zip); no AN JSON
  re-read (no report inconsistency required it). ✅
- No output-namespace mutation; no build rerun. ✅
- No ML / training / scoring / prediction / inference; no feature selection / threshold
  optimization / model selection / hyperparameter search / calibration training /
  confidence-tail selection. ✅
- No cost-aware / magnitude / deadband label adopted; no threshold picked. ✅
- No strategy / signals / PnL / backtest / paper / shadow / live / exchange-write. ✅
- No v002 terminal / sealed test / test rows read. ✅
- No AH/AJ/AN namespace mutation; no AH builder / AI diagnostics / AJ baseline rerun; no
  AJ/AI/AH/AO metric revised. ✅
- No eligibility / authorization / manifest / gate / sidecar flag transition;
  `flip_research_eligible(...)` never invoked; frozen v002 family preserved as sibling. ✅
- Nothing committed under `data/`; `.claude/scheduled_tasks.lock` not committed. ✅
- Allowed claim scope (AE §8 a/b/c) and forbidden claim scope (AE §8/§19) preserved; locked
  cost 8 bps/side · 16 bps round-trip preserved; the AN materiality shares kept
  descriptive-only. ✅

## Remaining blockers before any row-level read / dataset build

A separate future operator authorization for the recommended long-horizon ML dataset-build
phase (itself data-reading, no models). Row-level reads happen only under that later
prompt. The build must preserve the AH compact-spec posture, the 125 GiB cap (budget
preflight), v002/sealed/test exclusion, and all non-authorization flags false, and commit
no data.

## Remaining blockers before any ML / baseline run

Beyond the dataset-build phase, a **further** separate authorization for the fixed baseline
run (phase 2). No model / training / scoring / prediction / inference until then; the run
must use the frozen §21 constants and the §25 kill/continue verdict verbatim. All
non-authorization flags remain false.

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility memo**
clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution feasibility, and
slippage/spread — which aggTrades-only data cannot support (mid/book required; the
`bookticker_midprice_data_admissibility_memo` remains deferred/unauthorized) — plus label
economic relevance, strategy admissibility vs the retained rejections and the M0 §7.D
microstructure-lane `NOT_RECOMMENDED_NOW` posture, the Phase 4al no-rescue constraints, and
separate authorization for each capability. No AP/AO/AN result, and no future baseline
result however favourable, softens this boundary.

## Recommended state

**Remain paused.** Preregistration recorded; one docs-authorized data-reading dataset-build
phase recommended but **not started** and awaiting a separate future operator prompt.

## Result state

`LONGHORIZON_ML_BASELINE_PREREGISTRATION_RECORDED__DATASET_BUILD_AUTHORIZATION_MEMO_RECOMMENDED__NO_ML__NO_PARQUET_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## Explicit no-successor execution statement

Phase 4bn-AP authorizes **no** successor execution phase. It does not generate the
recommended memo's prompt; read any Parquet for row-level analysis; build any
ML/dataset/label namespace; train/score/predict/infer; do feature selection / threshold
optimization / model selection / hyperparameter search; rerun the AN build / AH builder /
AI diagnostics / AJ baselines; do strategy / signals / PnL / backtest / paper-shadow / live
/ exchange-write; or authorize any Phase 5 / successor phase. Every retained verdict and
project lock is preserved verbatim (8 bps/side · 16 bps round-trip; the Phase 4aw
always-raises invariant — never invoked; Phase 4bb-F sidecar policy; the Phase 4bn-AE
claim-scope and §19 boundary; the 4bn-AH..AO results including the AK single-follow-up
selection, the AL/AM recommendations, the AN build, and the AO diagnostics). Do not merge
to main and do not push unless explicitly instructed in a later prompt; do not generate a
merge-closeout or the recommended next prompt unless explicitly instructed later.
