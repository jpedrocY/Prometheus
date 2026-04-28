# Phase 3d-A Merge Report

**Phase:** 3d-A — F1 (mean-reversion-after-overextension) implementation, tests, quality gates, and H0/R3 control reproduction. **First phase to authorize source code, tests, and scripts on the F1 family.** Merged into `main` after operator review and two operator-mandated docs-only clarifications (scope-accounting clarification + §4 commit-hash clerical fix).

**Merge date:** 2026-04-28 UTC.

**Branch merged:** `phase-3d-a/f1-implementation-controls` → `main`.

**Status:** Merge complete. Local `main` and `origin/main` synced. Phase 3d-B **not** started. Phase 3b F1 spec preserved verbatim per Phase 3c §3. All Phase 2f thresholds, §1.7.3 project-level locks, R3 V1-breakout baseline-of-record, H0 V1-breakout framework anchor, and R1a / R1b-narrow / R2 retained-research-evidence preserved.

---

## 1. Phase 3d-A branch tip SHA before merge

```
50dd121c69abd159b19a40263ad9bb4f99d77729
```

Short SHA: `50dd121`. This was the docs-only clerical-fix commit that corrected the closeout §4 commit-hash listing — the most recent commit on `phase-3d-a/f1-implementation-controls` immediately before the `--no-ff` merge into `main`.

The full Phase 3d-A branch commit chain (3 commits ahead of `main` at `b477c2d` before the merge):

```
50dd121  docs(phase-3d-A): clerical fix to closeout §4 commit-hash listing
1a53423  docs(phase-3d-A): clarify implementation-control objective vs Phase 3d-B deferrals
06ad2a8  phase-3d-A: F1 implementation + tests + quality gates + H0/R3 control reproduction
```

Full SHAs:

| Commit | Full SHA |
|--------|----------|
| Original Phase 3d-A artifact commit | `06ad2a886653e567a434f64c8dd7a14b84d6da09` |
| Operator-mandated scope-accounting clarification | `1a53423e6f8692c4b933025559d6b590cab26128` |
| §4 commit-hash clerical fix | `50dd121c69abd159b19a40263ad9bb4f99d77729` |

## 2. Merge commit hash

```
f23b7f8bed48a1f598e8cbafc6bbfaaa304431ee
```

Short SHA: `f23b7f8`. Title: `Merge Phase 3d-A (F1 implementation + control reproduction) into main`. Author: `jpedrocY`. Date: 2026-04-28 UTC.

`--no-ff` merge per the prior Phase 2x / Phase 2y / slippage-cleanup / Phase 3a / Phase 3b / Phase 3c merge convention. The merge preserves all 3 phase-3d-a commits in history and produces a single explicit merge commit on `main` referencing the Phase 3d-A phase boundary.

## 3. Merge-report commit hash

This file's commit on `main` produces the merge-report commit. Full SHA recorded by the commit operation; visible via `git log --oneline -1` immediately after the commit lands. The post-commit chat report records the full SHA explicitly.

## 4. Main/origin sync confirmation

After `git push origin main`:

```
To https://github.com/jpedrocY/Prometheus.git
   b477c2d..f23b7f8  main -> main
```

Local `main` SHA: `f23b7f8bed48a1f598e8cbafc6bbfaaa304431ee`.
Origin `main` SHA: `f23b7f8bed48a1f598e8cbafc6bbfaaa304431ee`.

Identical. Confirmed via `git rev-parse main` and `git rev-parse origin/main` returning the same SHA.

(After the merge-report commit lands, `main` and `origin/main` will both advance to the merge-report commit's SHA.)

## 5. Git status

Immediately after the merge push (before this merge-report commit):

```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

## 6. Latest 5 commits

After the merge push (before this merge-report commit):

```
f23b7f8  Merge Phase 3d-A (F1 implementation + control reproduction) into main
50dd121  docs(phase-3d-A): clerical fix to closeout §4 commit-hash listing
1a53423  docs(phase-3d-A): clarify implementation-control objective vs Phase 3d-B deferrals
06ad2a8  phase-3d-A: F1 implementation + tests + quality gates + H0/R3 control reproduction
b477c2d  docs(phase-3c): merge report
```

The three phase-3d-a commits (`06ad2a8`, `1a53423`, `50dd121`) are now part of `main` history. The merge commit `f23b7f8` explicitly demarcates the Phase 3d-A phase boundary on `main`.

## 7. Files included in the merge

`git diff b477c2d..f23b7f8 --stat`:

**18 files changed; +2305 / −2 lines.**

### 7.1 New F1 source module (7 files; ~720 lines)

- `src/prometheus/strategy/mean_reversion_overextension/__init__.py` (70 lines)
- `src/prometheus/strategy/mean_reversion_overextension/variant_config.py` (138 lines)
- `src/prometheus/strategy/mean_reversion_overextension/features.py` (139 lines)
- `src/prometheus/strategy/mean_reversion_overextension/stop.py` (116 lines)
- `src/prometheus/strategy/mean_reversion_overextension/target.py` (51 lines)
- `src/prometheus/strategy/mean_reversion_overextension/cooldown.py` (102 lines)
- `src/prometheus/strategy/mean_reversion_overextension/strategy.py` (146 lines)

### 7.2 New F1 unit tests (7 files; ~975 lines; 68 tests)

- `tests/unit/strategy/mean_reversion_overextension/__init__.py` (0 lines)
- `tests/unit/strategy/mean_reversion_overextension/test_variant_config.py` (118 lines, 14 tests)
- `tests/unit/strategy/mean_reversion_overextension/test_features.py` (165 lines, 15 tests)
- `tests/unit/strategy/mean_reversion_overextension/test_stop.py` (187 lines, 11 tests)
- `tests/unit/strategy/mean_reversion_overextension/test_target.py` (74 lines, 8 tests)
- `tests/unit/strategy/mean_reversion_overextension/test_cooldown.py` (210 lines, 11 tests)
- `tests/unit/strategy/mean_reversion_overextension/test_strategy.py` (220 lines, 9 tests)

### 7.3 Modified V1 contact surface (2 files; +46 / −2 lines)

- `src/prometheus/strategy/types.py` (+6 / −2): added `TARGET = "TARGET"` to `ExitReason` StrEnum + docstring update.
- `src/prometheus/research/backtest/config.py` (+40): added `StrategyFamily` enum + `strategy_family` field + `mean_reversion_variant` field + validator clauses + import.

### 7.4 New documentation reports (2 files)

- `docs/00-meta/implementation-reports/2026-04-27_phase-3d-A_F1_implementation-control-checkpoint.md` (~352 lines after both clarifications): Phase 3d-A checkpoint with §1.1 explicit Completed/Deferred boundary list.
- `docs/00-meta/implementation-reports/2026-04-27_phase-3d-A_closeout-report.md` (~171 lines after both clarifications): Phase 3d-A closeout with §5.1/§5.2/§5.3 explicit scope-accounting and §4 multi-commit chain table.

### 7.5 Files NOT touched by the merge

- `src/prometheus/research/backtest/engine.py` — engine dispatch logic untouched.
- `src/prometheus/strategy/v1_breakout/` — entire V1 module unchanged.
- `src/prometheus/research/backtest/trade_log.py`, `diagnostics.py`, `report.py` — unchanged (F1-specific TradeRecord fields + funnel counters reserved for Phase 3d-B).
- All existing 474 V1 tests — unchanged; pre-existing test surface preserved.
- `scripts/` — no new runner script; existing Phase 2l runner used unmodified for control reproduction.
- `data/`, `.claude/`, `.mcp.json`, configuration / credentials — untouched.
- All existing docs (current-project-state, ai-coding-handoff, phase-gates, technical-debt-register, validation-checklist, cost-modeling, backtesting-principles, data-requirements, dataset-versioning, v1-breakout-strategy-spec, Phase 3a/3b/3c memos and merge reports) — unchanged.

## 8. Confirmation that Phase 3d-A implementation-control objective passed

Confirmed. Per Phase 3c §10.4 sequencing requirement:

1. **Implementation done** — F1 module + locked config + dispatch surface guard + 68 unit tests.
2. **Quality gates green** — `uv run pytest`: 542 passed; `uv run ruff check .`: All checks passed; `uv run ruff format --check .`: 142 files already formatted; `uv run mypy src`: Success no issues found in 57 source files.
3. **H0/R3 control reproduction bit-for-bit** on all 48 metric cells (H0 R/V × R3 R/V × BTC/ETH × 6 metrics).

Phase 3d-A's narrow implementation-control objective is met: the F1 toolkit exists, is locked at Phase 3b §4 values, has unit-test coverage of the 26 brief-required spec items (directly and architecturally), and demonstrably does not perturb V1 H0/R3 baselines.

**Per the closeout §5.1/§5.2 scope-accounting:** "implementation-control objective passed" applies to the Phase 3d-A scope only. Items in §5.2 (engine F1 dispatch wiring, F1 TradeRecord output fields, F1 lifecycle / funnel counters, F1 time-stop engine integration, F1 same-bar priority engine behavior, F1 target next-bar-open fill integration, F1 runner script, F1 diagnostics + first-execution-gate analysis, F1 R/V candidate backtests) are mandatory Phase 3d-B work before any F1 result can be produced or interpreted.

## 9. Confirmation that Phase 3d-B was not started

Confirmed. Phase 3d-B is the first phase that would authorize:

- F1 engine dispatch wiring (`BacktestEngine._run_symbol` extension).
- F1 TradeRecord output fields with NaN/None defaults for V1 rows.
- F1 lifecycle / funnel counters (analogous to `R2LifecycleCounters`).
- F1 same-bar priority engine behavior (STOP > TARGET > TIME_STOP).
- F1 time-stop engine integration (exit at `open(B+10)`).
- F1 target next-bar-open fill integration.
- F1 runner script (e.g., `scripts/phase3d_F1_execution.py`).
- F1 diagnostics + first-execution-gate analysis script.
- F1 R/V candidate backtests + first-execution-gate evaluation.
- Lifting the BacktestConfig MEAN_REVERSION_OVEREXTENSION rejection.

**None of these have been started.** The BacktestConfig validator's hard-rejection of `MEAN_REVERSION_OVEREXTENSION` enforces this at the type-construction level: even an attempted F1 backtest construction fails at config-validation time.

## 10. Confirmation that no F1 backtests were run or interpreted

Confirmed. The only backtests executed during Phase 3d-A were the four V1 H0/R3 control runs (per Phase 3c §6.3 / §6.4 reference re-runs) using the existing Phase 2l runner script:

- H0 R MED MARK
- H0 V MED MARK
- R3 R MED MARK
- R3 V MED MARK

All 48 metric cells (n, WR%, expR, PF, netPct, maxDD across 2 symbols × 4 runs) reproduced locked Phase 2e/2l/2s baselines bit-for-bit. No invocation of any F1 strategy code through the engine occurred. No F1 trade record exists.

## 11. Confirmation that no F1 first-execution gate was evaluated

Confirmed. Phase 3c §7.2 first-execution gate has five conditions (i)–(v):

- **(i) Absolute BTC edge** at MED slippage: `expR(F1, BTCUSDT, R, MED, MARK) > 0` — NOT EVALUATED (no F1 trades exist).
- **(ii) M1 BTC mechanism**: post-entry counter-displacement at 8-bar horizon ≥ +0.10 R AND fraction non-negative ≥ 50% — NOT EVALUATED.
- **(iii) ETH non-catastrophic per §11.4**: `expR(ETH, R, MED) > −0.50` AND `PF > 0.30` — NOT EVALUATED.
- **(iv) §11.6 HIGH-slippage cost-sensitivity (per Phase 3c amended gate)**: `expR(F1, BTCUSDT, R, HIGH, MARK) > 0` AND ETH HIGH non-catastrophic — NOT EVALUATED.
- **(v) §10.4-style hard-reject absolute thresholds at MED**: BTC and ETH `expR > −0.50` AND `PF > 0.30` — NOT EVALUATED.

None of these were computed in Phase 3d-A. Phase 3c §9 M1/M2/M3 mechanism predictions also not computed. They are reserved for Phase 3d-B.

## 12. Confirmation that no `data/` artifacts were committed

Confirmed. `git diff b477c2d..f23b7f8 --name-only` shows zero `data/` entries. The four V1 H0/R3 control runs wrote into the git-ignored `data/derived/backtests/` tree only (`.gitignore` excludes `data/`). No `git add data/` was executed.

## 13. Confirmation that no forbidden areas changed

Confirmed across all forbidden categories per the Phase 3d-A operator brief and the merge-task brief:

| Category | Status in merge |
|----------|-----------------|
| V1 breakout strategy module (`src/prometheus/strategy/v1_breakout/`) | UNCHANGED |
| V1 strategy logic, V1 entry/exit machinery, V1 setup predicate, V1 bias filter, R3 / R1a / R1b-narrow / R2 dispatch | UNCHANGED |
| Engine dispatch logic (`src/prometheus/research/backtest/engine.py`) | UNCHANGED |
| Trade log schema (`src/prometheus/research/backtest/trade_log.py`) | UNCHANGED |
| Diagnostics, report writer | UNCHANGED |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH numerical threshold) | PRESERVED VERBATIM |
| Strategy parameters (R3 sub-parameters; H0 baseline; R1a / R1b-narrow / R2 sub-parameters; F1 §4 axes from Phase 3b spec) | PRESERVED VERBATIM (control reproduction proves V1 bit-for-bit; F1 spec locked in `MeanReversionConfig` Field constraints + `model_post_init` defense) |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) | PRESERVED VERBATIM |
| MCP / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Paper/shadow planning | NOT PROPOSED, NOT AUTHORIZED |
| Phase 4 (runtime / state / persistence) work | NOT PROPOSED, NOT AUTHORIZED |
| Live-readiness work, deployment, exchange-write capability, production keys | NOT PROPOSED, NOT AUTHORIZED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |

**Project-state preservation:** R3 V1-breakout baseline-of-record per Phase 2p §C.1 stands; H0 V1-breakout framework anchor per Phase 2i §1.7.3 stands; R1a / R1b-narrow / R2 retained-research-evidence per Phase 2p §D / Phase 2s §13 / Phase 2w §16.3 stand; R2 framework verdict FAILED — §11.6 cost-sensitivity blocks stands; §11.6 = 8 bps HIGH numerical threshold per Phase 2y closeout stands; Phase 2f §11.3.5 binding rule preserved; Phase 3b F1 spec preserved verbatim per Phase 3c §3.

---

**End of Phase 3d-A merge report.** Phase 3d-A is now merged to `main` and pushed to `origin`. F1 toolkit (self-contained module + locked config + dispatch surface guard + 68 unit tests) lands on `main` with V1 dispatch path bit-for-bit preserved. F1 deliberately non-runnable through `BacktestConfig` validator until Phase 3d-B authorization. **No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / credentials / `data/` work.** Phase 3d-B not started. Awaiting any future operator instruction.
