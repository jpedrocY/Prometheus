# Phase 4bn-AJ — Closeout

## Branch

`phase-4bn-aj/fixed-pre-v002-baseline-run-verdict`

## Base SHA

`f33831c8577764c5fbc059a9e23ab4f13f0c8ed2`
(`docs(phase-4bn-ai): finalize merge closeout shas`).

## Phase type

Narrow, pre-registered **fixed-baseline ML phase**: read the Phase 4bn-AH
dataset-spec artefacts read-only; read the AH-verified pre-v002 feature/label
Parquet; run the three pre-registered fixed baselines (majority / persistence / L2
linear) **once each**; evaluate against the frozen Phase 4bn-AE metric registry,
dependence policy, calibration/cost schema, and success/continue/kill criteria;
record the pre-registered verdict. **No model selection, no hyperparameter search,
no strategy/PnL/backtest, no successor.**

## Files created / modified

Created (committed): `src/prometheus/research/microstructure/pre_v002_fixed_baseline_run.py`;
`tests/research/microstructure/test_phase4bn_aj_pre_v002_fixed_baseline_run.py`;
this closeout; the implementation report
`2026-07-08_phase-4bn-aj_fixed-pre-v002-baseline-run-verdict.md`.

No existing source modified. Created local **gitignored/uncommitted**:
`data/research/microstructure/ml_baselines/pre_v002_fixed_baseline_v001/` (9 JSON
artefacts + 9 `.sha256` sidecars; no model binaries; no row-level predictions).

## Validation commands

- `pytest test_phase4bn_aj…` → 23 passed; AF+AH+AJ combined → 146 passed (no
  regression).
- `ruff check` (new module + test) → All checks passed.
- `mypy` new module → 0 direct errors (residual errors pre-existing in imported
  v002 sibling modules under `strict=true`, unmodified).
- `git diff --check` → clean.
- AH namespace re-hash → 4/4 byte-identical (unmutated).
- AJ namespace → 9 artefacts + 9 sidecars verify; gitignored (`.gitignore:88`);
  0 tracked. `git ls-files data/microstructure/ data/research/` → 0 tracked.
- Real Phase 4bn-L budget preflight → PASSED (D: 1166.24 GiB).

## Concise baseline outcome

Single run, ~47 min, 304,816,127 train rows fit once, 396,930,283 rows evaluated
once. Validation (15s) accuracy: majority 0.4950 / persistence 0.5158 / **L2
0.5453**. L2 uplift over majority **+5.03 pp** accuracy, **+0.145** macro-F1, **+3.56
pp** balanced accuracy; over persistence **+2.96 pp** accuracy. Validation date- and
month-block agreement **1.000**; no holdout sign reversal (holdout L2 +4.1 pp);
no overfitting (validation−train accuracy +0.008). L2 high-confidence tail (≥0.8)
beats the majority floor on all splits (validation tail acc 0.633 vs floor 0.495)
though overconfident in level. Cost: only **2.47%** of validation 15s moves exceed
the 16 bps round-trip cost (descriptive only). The flat/zero class is essentially
never predicted by L2 (as in v002). This **reproduces the v002 small-lift sign**
on the larger pre-v002 regime.

## Verdict

**`CONTINUE_ONE_FOLLOWUP`** (Phase 4bn-AE §16) — all "all of" conditions met on the
frozen thresholds; `kill_reasons = []`. Recorded caveat: the only mixed signal is
that persistence's macro-F1 (0.402) exceeds L2's (0.366) **solely** because
persistence predicts the degenerate ~1.5% flat class; on the directional classes L2
dominates, and the +0.03 macro-F1 threshold is majority-floor-referenced (matching
the §16 v002 "+0.14 macro-F1" anchor). Under a stricter "macro-F1 over both floors"
reading the verdict would be `INVESTIGATE_AMBIGUOUS`; **both readings converge on the
same action** — a separately-authorized Phase 4bn-AK arc-decision, remain paused, no
successor here. Not softened, not upgraded.

Allowed claims (§8): (a) directional information present; (b) v002 sign reproduced;
(c) calibration-tail beats floor but overconfident. Forbidden: tradability /
profitability / strategy / PnL / backtest / economic significance.

## Explicit boundary confirmations

No AH rerun; no AH namespace mutation (byte-identical); no v002 terminal read; no
sealed test touch; `test_rows_loaded = 0` preserved; no unregistered models; no
model selection; no hyperparameter search; no feature selection; no threshold
optimization; no strategy / signals / PnL / backtest; no Sharpe / hit-rate; no
paper / shadow / live; no exchange-write; no credentials; no eligibility / manifest
/ gate mutation; `flip_research_eligible(...)` never invoked; each baseline run once;
no data committed.

## Remaining blockers before Phase 4bn-AK

Separate operator authorization of Phase 4bn-AK (the pre-registered arc-decision
memo). Default posture: remain paused.

## Remaining blockers before ML training (beyond baselines)

A separately-authorized ML phase (`ml_authorized = false`); any capacity/model
follow-up is one of the §16 (a)–(d) options and requires Phase 4bn-AK authorization
first.

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (§19): a future M0-style mechanism-admissibility memo (M0.5 cost realism,
execution feasibility, slippage/spread — requiring mid/book data aggTrades cannot
supply, label economic relevance, no-rescue constraints) **plus** separate operator
authorization for each of strategy / signals / PnL / backtest / paper-shadow / live
/ exchange-write. No AJ result softens this.

## Recommended state

**Remain paused.**

## No successor authorized

No successor is authorized from inside Phase 4bn-AJ. Phase 4bn-AK (arc-decision),
any §16 (a)–(d) follow-up, ML training, model scoring, predictions, inference,
strategy, signals, PnL, backtests, additional data reads, an AH builder rerun, a
new dataset namespace, v003, compacted Parquet, database outputs, paper/shadow,
live-readiness, deployment, exchange-write, credentials, private/authenticated
endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, and all other
candidates each require **separate operator authorization**.

## Result state

`FIXED_PRE_V002_BASELINE_RUN_RECORDED__PRE_REGISTERED_VERDICT_RECORDED__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`
