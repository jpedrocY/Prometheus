# Phase 3d-B1 Merge Report

**Phase:** 3d-B1 — F1 (mean-reversion-after-overextension) engine wiring + F1 output fields + lifecycle counters + runner scaffolding + tests + quality gates + H0/R3 control reproduction.

**Date:** 2026-04-28 UTC.

**Status:** **Merged into `main`.** Phase 3d-B1's engine-wiring objective passed; the F1 dispatch is now part of `main` and runnable through `BacktestEngine` (subject to the deliberate Phase 3d-B2 runner scaffold guard). H0/R3 V1 baselines reproduced bit-for-bit on all 48 metric cells. **F1 remains deliberately unrun** — no F1 candidate backtest, §7.2 first-execution gate, §9 mechanism (M1/M2/M3), or V-window run was executed in Phase 3d-B1. Phase 3d-B2 not started.

---

## 1. Phase 3d-B1 branch tip SHA before merge

```
c682e22d8af9b453963918a2ecbed3fa20c90d48
```

(Branch `phase-3d-b1/f1-engine-wiring-controls`; 4 commits ahead of `main`'s pre-merge tip `e820acd71d9c9c3384a7c448666d9bcb8159af5c`.)

## 2. Merge commit hash

```
cbe5f672a8d6c958f98a0c7d2165c6b861859d6d
```

`--no-ff` merge of `phase-3d-b1/f1-engine-wiring-controls` into `main`. Merge commit message: `Merge Phase 3d-B1 (F1 engine wiring + control reproduction) into main`.

## 3. Merge-report commit hash

The merge-report commit hash is recorded in the final chat response after this report file is committed to `main` and pushed.

## 4. Main / origin sync confirmation

After the merge push:

```
local  main HEAD: cbe5f672a8d6c958f98a0c7d2165c6b861859d6d
origin main HEAD: cbe5f672a8d6c958f98a0c7d2165c6b861859d6d
```

Local `main` and `origin/main` are synced at the merge commit.

## 5. Git status

```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

(State as of immediately after the merge push, before this merge-report commit. After the merge-report commit and push, both local `main` and `origin/main` advance one further commit and remain synced.)

## 6. Latest 5 commits

After the merge push, before this merge-report commit:

```
cbe5f67 Merge Phase 3d-B1 (F1 engine wiring + control reproduction) into main
c682e22 docs(phase-3d-B1): fix closeout §3 file-count to 9
701ee4f docs(phase-3d-B1): record full closeout §4 commit chain
1da8748 docs(phase-3d-B1): clerical fix to closeout §4 commit-hash listing
fd0a9ca phase-3d-B1: F1 engine wiring + tests + quality gates + H0/R3 control reproduction
```

After the merge-report commit and push, the latest commit advances to the merge-report commit (recorded in §3 / final chat response).

## 7. Files included in the merge

The merge introduces **9 files** to `main` (vs the pre-merge tip `e820acd`):

### 7.1 Modified — engine + config + trade_log (3 files)

- `src/prometheus/research/backtest/config.py` (+29 / −12) — Phase 3d-A guard lifted; positive F1 dispatch validation requiring `mean_reversion_variant` non-None and forbidding non-default V1 `strategy_variant` on the F1 path.
- `src/prometheus/research/backtest/engine.py` (+480 / −16) — F1 engine wiring: `_F1TradeMetadata`, `F1LifecycleCounters`, `_OpenTrade.f1_metadata`, `_SymbolRun.f1_*` fields, `BacktestRunResult.f1_counters_per_symbol`, `BacktestEngine._mean_reversion_strategy`, `is_f1` dispatch in `run`, `_run_symbol_f1` per-bar lifecycle, `_open_f1_trade`, `_close_f1_trade_*` close helpers, F1-field population in `_record_trade`.
- `src/prometheus/research/backtest/trade_log.py` (+24 / −0) — 4 F1 NaN-default fields on `TradeRecord` and 4 corresponding columns in the parquet schema.

### 7.2 Modified — tests (2 files)

- `tests/unit/research/backtest/test_config.py` (+63 / −0) — 5 new F1 BacktestConfig validator tests.
- `tests/unit/research/backtest/test_trade_log.py` (+6 / −0) — Added the 4 F1 column names to the parquet schema assertion.

### 7.3 Created — F1 engine-dispatch test file + runner scaffold + reports (4 files)

- `tests/unit/research/backtest/test_engine_f1_dispatch.py` (~580 lines; 20 engine-level F1 tests).
- `scripts/phase3d_F1_execution.py` (~140 lines; deliberately-guarded Phase 3d-B2 scaffold).
- `docs/00-meta/implementation-reports/2026-04-28_phase-3d-B1_F1_engine-wiring-control-checkpoint.md` (Phase 3d-B1 checkpoint report).
- `docs/00-meta/implementation-reports/2026-04-28_phase-3d-B1_closeout-report.md` (Phase 3d-B1 closeout report).

Total: 9 files; +1997 / −28 net lines.

## 8. Confirmation that Phase 3d-B1 engine-wiring objective passed

Confirmed. Per the Phase 3d-B1 checkpoint report (§5–§6) and closeout report:

- All four quality gates green: `uv run pytest` (567 passed; 542 → 567 with no V1 regressions), `uv run ruff check .` (clean), `uv run ruff format --check .` (clean), `uv run mypy src` (clean).
- H0/R3 control reproduction bit-for-bit on all 48 metric cells (4 control runs × 2 symbols × 6 metrics):
  - H0 R MED MARK: BTC n=33 expR=−0.4590 PF=0.2552; ETH n=33 expR=−0.4752 PF=0.3207.
  - H0 V MED MARK: BTC n=8 expR=−0.3132 PF=0.5410; ETH n=14 expR=−0.1735 PF=0.6950.
  - R3 R MED MARK: BTC n=33 expR=−0.2403 PF=0.5602; ETH n=33 expR=−0.3511 PF=0.4736.
  - R3 V MED MARK: BTC n=8 expR=−0.2873 PF=0.5799; ETH n=14 expR=−0.0932 PF=0.8242.
- F1 engine path is wired and tested through 25 new tests (5 BacktestConfig validator tests + 20 engine-dispatch / lifecycle / invariant tests).
- F1 funnel-counter accounting identity (`detected = filled + rejected_stop_distance + blocked_cooldown`) is enforced by the engine and tested.
- F1 emits only the spec'd exit reasons (STOP / TARGET / TIME_STOP / END_OF_DATA) — no V1-only exit-reason leakage.
- F1 frozen-target / frozen-stop invariants hold and are tested.
- F1 cooldown gating is correctly implemented (block-then-release tested end-to-end).
- F1 same-bar exit priority STOP > TARGET > TIME_STOP holds.

## 9. Confirmation that Phase 3d-B2 was not started

Confirmed. Phase 3d-B2 work — F1 R-window candidate runs (#1–#4), conditional F1 V-window run (#5), §7.2 first-execution-gate evaluation, §9 M1/M2/M3 mechanism computation, §8 mandatory diagnostics, runner full run-loop, analysis script, variant-comparison report — was not commenced in Phase 3d-B1 and is reserved for a separately-authorized Phase 3d-B2 phase. The merged `scripts/phase3d_F1_execution.py` runner scaffold's `f1` action is hard-guarded by `--phase-3d-b2-authorized`; without that flag it exits with status 2 and a "Phase 3d-B1 forbids F1 candidate backtest execution" message. Phase 3d-B1 invoked the runner only with `check-imports` (no run-loop) and to verify the hard guard.

## 10. Confirmation that no F1 candidate backtests were run or interpreted

Confirmed. The only backtests executed during Phase 3d-B1 were the four V1 H0/R3 control runs (`phase2l_R3_first_execution.py --variant H0/R3 --window R/V`) used to verify bit-for-bit baseline preservation. No F1 candidate backtest was invoked. No F1 trade was produced. No F1 trade log, summary metrics, equity curve, drawdown series, or report artifact exists. F1 candidate execution and interpretation are reserved for Phase 3d-B2.

## 11. Confirmation that no F1 first-execution gate was evaluated

Confirmed. Phase 3c §7.2 first-execution gate has five conditions (i)–(v):
- (i) Absolute BTC edge at MED slippage — NOT EVALUATED
- (ii) M1 BTC mechanism — NOT EVALUATED
- (iii) ETH non-catastrophic per §11.4 — NOT EVALUATED
- (iv) §11.6 HIGH-slippage cost-sensitivity (BTC HIGH expR > 0; ETH HIGH non-catastrophic) — NOT EVALUATED
- (v) §10.4-style hard-reject absolute thresholds — NOT EVALUATED

None were computed in Phase 3d-B1. They are reserved for Phase 3d-B2.

## 12. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after the merge shows zero `data/` entries. The four V1 control runs wrote into the git-ignored `data/derived/backtests/` tree only. No `git add data/` was executed. The merge commit and all four branch commits (`fd0a9ca`, `1da8748`, `701ee4f`, `c682e22`) are limited to source code, tests, scripts/, and `docs/00-meta/implementation-reports/`.

## 13. Confirmation that no forbidden areas changed

Confirmed across all forbidden categories per the Phase 3d-B1 operator brief:

| Category | Status |
|----------|--------|
| Phase 3b F1 spec axes (overextension window 8 / threshold 1.75 / mean-reference window 8 / stop-buffer 0.10 / time-stop 8 / stop-distance band [0.60, 1.80]) | LOCKED VERBATIM in `MeanReversionConfig` (Phase 3d-A) and consumed unmodified by Phase 3d-B1 engine code |
| Phase 3d-A F1 module + primitives + locked config | PRESERVED VERBATIM |
| V1 breakout strategy module (`src/prometheus/strategy/v1_breakout/`) | UNCHANGED |
| V1 strategy logic, V1 entry/exit machinery, V1 setup predicate, V1 bias filter | UNCHANGED (control reproduction bit-for-bit on all 48 metric cells) |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH) | PRESERVED VERBATIM |
| Strategy parameters (R3 sub-parameters; H0 baseline; R1a / R1b-narrow / R2 sub-parameters) | PRESERVED VERBATIM |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) | PRESERVED VERBATIM |
| Phase 3c §6 run inventory | PRESERVED (no run-set expansion; F1 candidate runs reserved for Phase 3d-B2) |
| MCP / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Paper/shadow planning | NOT PROPOSED, NOT AUTHORIZED |
| Phase 4 (runtime / state / persistence) work | NOT PROPOSED, NOT AUTHORIZED |
| Live-readiness work, deployment, exchange-write capability, production keys | NOT PROPOSED, NOT AUTHORIZED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |

**Project-state preservation:** R3 V1-breakout baseline-of-record per Phase 2p §C.1 stands; H0 V1-breakout framework anchor per Phase 2i §1.7.3 stands; R1a / R1b-narrow / R2 retained-research-evidence stand; R2 framework verdict FAILED — §11.6 cost-sensitivity blocks stands; §11.6 = 8 bps HIGH numerical threshold per Phase 2y closeout stands; Phase 2f §11.3.5 binding rule preserved; Phase 3b F1 spec preserved verbatim per Phase 3c §3 / Phase 3d-A scope.

---

**End of Phase 3d-B1 merge report.** Phase 3d-B1 merged to `main` at `cbe5f672a8d6c958f98a0c7d2165c6b861859d6d`. F1 engine path is on `main` and runnable through `BacktestEngine`; the runner scaffold's `f1` action is hard-guarded against accidental F1 execution. **F1 remains deliberately unrun.** No F1 candidate backtest, §7.2 first-execution gate, §9 mechanism (M1/M2/M3), or V-window run was executed in Phase 3d-B1. Phase 3d-B2 not started; the operator decides whether to authorize it. Awaiting operator review.
