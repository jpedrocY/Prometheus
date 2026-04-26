# Phase 2l — Gate 2 Pre-Commit Review

**Phase:** 2l — R3 First Execution.
**Branch:** `phase-2l/R3-first-execution`.
**Review date:** 2026-04-26 UTC.
**Authority:** Phase 2l operator-approved brief; Phase 2k Gate 1 plan (R3-first sequencing recommendation, Option A); Phase 2j memo §D (R3 spec); Phase 2i §1.7.3 project-level locks; Phase 2f §§ 8–11 thresholds (preserved unchanged per §11.3.5).

This Gate 2 review traces every operator-brief content requirement and process requirement to its Phase 2l artifact, confirms threshold preservation, confirms safety posture, and records what awaits operator approval before any `git add` / `git commit`.

## Scope confirmed against operator brief

Scope confirmed: implement R3 minimally (no R1a, no widening), execute H0 + R3 on R window for BTC + ETH at MEDIUM slippage / MARK_PRICE; if PROMOTE, run V-window + LOW/HIGH slippage + TRADE_PRICE sensitivity; produce comparison report + Gate 2 review; stop before any commit. **All scope requirements applied; no scope drift.**

## Docs written

| Path                                                                                              | Purpose                                       | Status              |
|---------------------------------------------------------------------------------------------------|-----------------------------------------------|---------------------|
| `docs/00-meta/implementation-reports/2026-04-26_phase-2l_R3_variant-comparison.md`                | Phase 2l comparison report (committable)      | drafted, untracked  |
| `docs/00-meta/implementation-reports/2026-04-26_phase-2l_gate-2-review.md` (this file)            | Phase 2l Gate 2 pre-commit review (committable) | this document       |

No Gate 1 plan file is committed because Phase 2l proceeded under the operator brief directly (no separate Gate 1 phase — the Phase 2k Gate 1 plan §§ 11.B / 13 / 16 already pre-specified the implementation scope and thresholds for R3, and the operator brief is the Gate 1 equivalent for Phase 2l).

The Phase 2l checkpoint report (per `.claude/rules/prometheus-phase-workflow.md`) will be drafted only after Gate 2 approval, immediately before commits.

## Code surface written (untracked at this time)

| Path                                                                  | Lines added (approx.) | Purpose                                                                                  |
|-----------------------------------------------------------------------|----------------------:|------------------------------------------------------------------------------------------|
| `src/prometheus/strategy/types.py`                                    |                  +5   | Add `TAKE_PROFIT` and `TIME_STOP` to `ExitReason` enum + docstring.                       |
| `src/prometheus/strategy/v1_breakout/variant_config.py`               |                 +35   | Add `ExitKind` StrEnum + 3 R3 fields with H0-preserving defaults + docstring.            |
| `src/prometheus/strategy/v1_breakout/__init__.py`                     |                  +2   | Export `ExitKind`.                                                                       |
| `src/prometheus/strategy/v1_breakout/management.py`                   |                 +60   | Add `_fixed_r_time_stop_decision` helper + extend `on_completed_bar` signature for dispatch. |
| `src/prometheus/strategy/v1_breakout/strategy.py`                     |                  +6   | Pass R3 kwargs through `V1BreakoutStrategy.manage`.                                       |
| `src/prometheus/research/backtest/report.py`                          |                  +7   | Extend `compute_summary_metrics` with `take_profit_exits` and `time_stop_exits` counters. |
| `tests/unit/strategy/v1_breakout/test_variant_config.py`              |                +220   | 8 R3 unit tests + H0-preservation regression on the new fields.                           |
| `scripts/phase2l_R3_first_execution.py`                               |                +395   | Phase 2l runner (mirrors Phase 2g pattern; H0/R3 variants; R/V/FULL windows; slippage/stop-trigger knobs). |
| `scripts/_phase2l_R3_analysis.py`                                     |                +325   | Internal analysis script (mirrors `_phase2g_wave1_analysis.py` pattern).                  |

## Ambiguity-log appends

**None.** Phase 2l carries forward GAP-20260424-031 (EMA slope), GAP-20260424-032 (mark-price stop-trigger sensitivity), and GAP-20260424-033 (R3 unconditional time-stop) per Phase 2k Gate 1 plan §16 — none requires update because Phase 2l's runs honor the existing dispositions exactly. GAP-20260424-030 (R3-related) was previously flagged for "SUPERSEDED-on-execution when R3 advances per Phase 2j memo §D.16" in the Phase 2k checkpoint; that supersession is now ready for the operator's optional disposition update at Phase 2l commit time, but this Gate 2 review does NOT propose a unilateral edit to the ambiguity log.

## Promotion / disqualification verdict (per Phase 2f §§ 10.3 / 10.4)

R-window verdict: **R3 PROMOTES**. Both BTC and ETH clear §10.3.a (Δexp ≥ +0.10 AND ΔPF ≥ +0.05) and §10.3.c strict-dominance (Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0). No §10.3 disqualification floor triggered: |maxDD| ratios are 0.588x (BTC) and 0.882x (ETH), both well below the 1.5x veto. §10.4 does not apply (Δn = 0). §11.4 ETH-as-comparison rule satisfied: BTC clears, ETH not catastrophic.

| Symbol  | Δexp     | ΔPF      | Δ|maxDD| (pp) | |maxDD| ratio | §10.3.a | §10.3.c |
|---------|---------:|---------:|---------------:|--------------:|---------|---------|
| BTCUSDT | +0.219   | +0.305   | −1.515 (better) | 0.588x        | clear   | clear   |
| ETHUSDT | +0.124   | +0.153   | −0.487 (better) | 0.882x        | clear   | clear   |

V-window confirms direction-of-improvement on both symbols (not a binding promotion gate per §11.3.5; sanity check only). Slippage sensitivity (LOW/MED/HIGH) shows monotone proportional cost effect; even at HIGH (3x) R3 still beats H0-at-MEDIUM. TRADE_PRICE sensitivity bit-identical (zero gap-through stops). No regime-driven artifact: per-fold expR shows R3 beats H0 in 4/5 BTC folds and 3/5 ETH folds (with the only ETH fold-3 regression at sample-noise scale of −0.006 R).

This is the **first PROMOTE verdict** in the project's research history. Phase 2g Wave-1 produced REJECT ALL on all four single-axis variants; Phase 2j R3 was the structural redesign chosen to break that pattern; Phase 2l confirms R3 clears.

## Implementation-bug check

R3 forbids `TRAILING_BREACH` and `STAGNATION` exits per Phase 2j §D.10. Both R3 R-window runs counted **zero** of either:

```
R3 BTCUSDT: TRAILING_BREACH+STAGNATION exits = 0 ✓
R3 ETHUSDT: TRAILING_BREACH+STAGNATION exits = 0 ✓
```

H0 control re-run reproduced Phase 2g/2k baseline numbers bit-for-bit:

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Phase 2g/2k baseline match |
|---------|-------:|-------:|--------:|------:|--------:|--------:|---------------------------|
| BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | yes                        |
| ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | yes                        |

This confirms: (a) the H0 default code path is preserved bit-for-bit by the new optional R3 fields and the `exit_kind` dispatch with default `STAGED_TRAILING`; (b) the Phase 2l engine version produces the same H0 result the Phase 2g/2k phases relied on; (c) R3's improvements are not contaminated by an inadvertent H0 regression.

## Mandatory diagnostics — produced

Per the Phase 2l brief and Phase 2k Gate 1 plan §11.B requirements:

| Diagnostic                                         | Status                                                                                                                                                                                                                                          |
|----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Per-regime expR (realized 1h volatility regime)    | Produced. Each trade entry classified by realized 1h ATR(20) percentile within trailing 1000-bar window (terciles 33/67). R3 improves expR in **all six** regime-symbol cells with the largest gains in BTC low_vol (Δexp +0.318) and BTC high_vol (Δexp +0.216) — the regimes where H0 was most broken. No regime-symbol cell shows R3 worse than H0. Reported in comparison memo §6.1. *(Corrected from the initial draft, which had incorrectly used trade-duration buckets as a proxy for the required diagnostic; the duration-bucket view is now retained only as an auxiliary supplemental diagnostic in §6.1.A.)* |
| MFE distribution                                   | Produced. Median / p25 / p75 unchanged (R3 doesn't alter excursion measurement); max-MFE drops modestly because the take-profit caps the right tail. Reported in §6.2.                                                                          |
| Long/short asymmetry                               | Produced. R3 narrows BTC asymmetry (longs −0.560 → −0.252; shorts −0.364 → −0.230). ETH shorts under R3 = +0.028 R / PF 1.07 — first positive direction-symbol cell observed in the project. Reported in §6.3.                                  |
| Per-fold (5 rolling, GAP-036)                      | Produced. R3 beats H0 in 4/5 BTC folds and 3/5 ETH folds. First positive BTC fold expR observed (F2 +0.015; F3 +0.100). Reported in §5.                                                                                                          |
| Extended exit-reason histogram (TP / TIME_STOP)    | Produced via aggregator extension (`take_profit_exits`, `time_stop_exits` columns) + summary-metrics + analysis-script breakdown. R3 BTC: STOP=8, TP=4, TS=21. R3 ETH: STOP=14, TP=5, TS=14. Reported in §3.                                    |
| TAKE_PROFIT R-multiple distribution                | Produced. BTC mean +1.643 R (target 2.0; gap explained by next-bar-open fill mechanics + fees + slippage). ETH mean +1.518 R. Not a bug — expected cost-model behavior. Reported in §6.4.                                                       |
| TIME_STOP bias diagnostic                          | Produced. BTC mean −0.169 R / median −0.090 / 52% negative; ETH mean −0.031 R / median −0.003 / 57% negative. Time-stop is approximately symmetric around zero, not selectively biting on slow-developing winners. Reported in §6.5.            |
| Implementation-bug check                           | Produced. Zero TRAILING_BREACH and zero STAGNATION exits in either R3 run. Reported in §6.6.                                                                                                                                                     |

## Threshold preservation

| Threshold / framework                          | Status                                                                                            |
|------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Phase 2f §10.3.a (Δexp + ΔPF improvement)      | applied unchanged                                                                                 |
| Phase 2f §10.3.b (rising count + Δexp ≥ 0)     | applied unchanged (does not fire; Δn = 0)                                                         |
| Phase 2f §10.3.c (strict dominance, exit-only) | applied unchanged (per Phase 2j §D.10)                                                            |
| Phase 2f §10.3 disqualification floor          | applied unchanged; not triggered                                                                  |
| Phase 2f §10.4 hard reject                     | applied unchanged; does not fire (Δn = 0)                                                         |
| Phase 2f §11.3 no-peeking                      | applied unchanged; V-window not consulted during R-window evaluation                              |
| Phase 2f §11.3.5 pre-committed thresholds      | applied unchanged; no post-hoc loosening or tightening                                            |
| Phase 2f §11.4 ETH-as-comparison rule          | applied unchanged; satisfied                                                                      |
| Phase 2f §11.6 cost-sensitivity                | applied via LOW/MED/HIGH slippage sensitivity; R3 still PROMOTES at HIGH compared to H0-at-MEDIUM |
| GAP-20260424-036 fold convention               | applied unchanged (5 rolling folds, fold 1 partial-train, all tests in R)                         |
| GAP-20260424-031 EMA slope                     | inherited; carry-forward                                                                          |
| GAP-20260424-032 stop-trigger sensitivity      | inherited; TRADE_PRICE sensitivity report cut produced                                            |
| GAP-20260424-033 R3 unconditional time-stop    | inherited; verified in code via `_fixed_r_time_stop_decision` helper (no MFE gate)                |

## Wave-1 historical evidence preservation

Phase 2g Wave-1's REJECT ALL verdict is preserved as historical evidence under the same framework. **No re-derivation, no re-ranking, no re-comparison to Wave-1 variants.** R3 is compared against H0 only, per Phase 2i §1.7.3 project-level locks (§ "H0-only anchor"). The variant-comparison report explicitly states wave-1 evidence is diagnostic input only, not a baseline.

## §1.7.3 project-level locks honored

| Lock                                                            | Status                                                                                                                                            |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| BTCUSDT primary; ETHUSDT comparison only                        | honored (§11.4 ETH-as-comparison rule applied)                                                                                                     |
| One-position max                                                | unchanged                                                                                                                                          |
| 0.25% risk fraction                                             | unchanged in BacktestConfig                                                                                                                        |
| 2x effective leverage cap                                       | unchanged                                                                                                                                          |
| Mark-price protective stop semantics                            | preserved as default; TRADE_PRICE only as sensitivity diagnostic per GAP-032                                                                       |
| v002 datasets (no data downloads in 2l)                         | preserved; no manifest changes                                                                                                                     |
| H0-only anchor for §10.3 / §10.4 evaluation                      | applied; wave-1 numbers cited as historical evidence only, not as comparison baselines                                                              |
| H0 bit-for-bit preservation under default config                 | enforced by `test_R3_default_path_preserves_H0_bitforbit_through_strategy` + verified by H0 R-window numerical match to Phase 2g/2k baseline       |

## Safety posture

| Check                                                        | Result |
|--------------------------------------------------------------|--------|
| Production Binance keys                                      | none   |
| Exchange-write code                                          | none   |
| REST / WebSocket / authenticated endpoints                   | none   |
| Credentials / `.env`                                         | none   |
| `.mcp.json`                                                  | absent |
| Graphify                                                     | disabled |
| MCP servers                                                  | not activated |
| Manual trading controls                                      | none   |
| Strategy structural changes                                  | R3 only — exit-machinery only; entry pipeline unchanged       |
| Risk framework changes                                       | none   |
| Dataset / manifest changes                                   | none   |
| Cost-model changes                                           | none (slippage applied via existing buckets; no fee-rate change) |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (`data/derived/backtests/phase-2l-*` git-ignored as designed) |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction)                                       |
| Phase 4 work                                                 | none (operator restriction)                                       |
| Fallback Wave 2 / H-D6 start                                 | none (operator restriction; superseded by R3 PROMOTE)             |
| Disguised parameter sweeps                                   | none (single committed value per R3 sub-parameter)                |
| R1a execution attempted                                      | none (operator restriction; deferred to a future phase)            |
| Wave-1 variant revival                                       | none                                                              |
| Live deployment / paper / shadow / tiny-live readiness claim | none                                                              |

## Operator-restriction compliance (Phase 2l brief)

| Restriction                                                                | Status                                                                                                              |
|----------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Implement R3 only (no R1a)                                                 | honored                                                                                                              |
| No widening of scope (no extra variants beyond H0 + R3)                    | honored                                                                                                              |
| No parameter sweeps (R-target = 2.0; time-stop = 8 singular)               | honored                                                                                                              |
| No fallback Wave 2 or H-D6 work                                            | honored (superseded by PROMOTE)                                                                                       |
| No Phase 4 work                                                            | honored                                                                                                              |
| No MCP / Graphify / `.mcp.json`                                            | honored                                                                                                              |
| No `docs/12-roadmap/technical-debt-register.md` edits                      | honored                                                                                                              |
| Apply Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged             | honored                                                                                                              |
| H0 control re-run on the same engine version                               | honored; bit-for-bit reproduces Phase 2g/2k baseline                                                                  |
| Stop before `git add` / `git commit` and await operator/ChatGPT review     | honored — this Gate 2 review is the stop point                                                                       |
| Flag bug if TRAILING_BREACH or STAGNATION appears in R3 trade log          | honored — implementation-bug check produced; zero leakage on both symbols                                            |

## Test suite

| When                                  | Result                |
|---------------------------------------|-----------------------|
| Pre-runner (after R3 unit tests added) | **404 passed** / 11.34s (was 396 + 8 new R3 tests) |
| Post-runs                              | unchanged (no source changes after the runs)         |
| Final pre-Gate-2 confirmation          | (to be re-run before commit, expected 404 passed)    |

`uv run ruff check .` ✓, `uv run ruff format --check .` ✓ (118 files), `uv run mypy` ✓ (49 source files; scripts are out of mypy scope per the existing project configuration, consistent with Phase 2g pattern).

## Gate 2 review-cycle note (2026-04-26)

The first Gate 2 submission was reviewed by ChatGPT/operator and returned NOT-YET-APPROVED with one required fix: the per-regime expR diagnostic had been produced as a trade-duration proxy rather than as a realized 1h volatility-regime classification. The fix has been applied:

- A realized-1h-volatility regime classifier was added to the internal analysis script (`scripts/_phase2l_R3_analysis.py`): trailing 1000 1h-bar window of Wilder ATR(20), tercile cutoffs at 33% / 67%, mid-rank tie convention. The classifier loads the existing v002 1h-bar dataset; no backtest re-run was required (the regime label is derived from the data and the existing trade-log entry timestamps, not from any strategy decision).
- The comparison report §6.1 was rewritten with the proper realized-volatility regime breakdown and the per-regime delta table.
- The duration-bucket view was retained as an auxiliary / supplemental diagnostic in §6.1.A, explicitly relabeled as a proxy and not as the required per-regime expR output.
- The R3 implementation, run results, promotion framework, committed sub-parameter values, and H0 baseline handling are unchanged.
- The promotion verdict from the corrected regime decomposition is consistent with §4: R3 improves expR in **all six** regime-symbol cells; no regime-symbol cell shows R3 worse than H0; the §10.3.a + §10.3.c verdict is not contradicted. **Verdict stays the same: PROMOTE.**

## Recommended next step

Operator/ChatGPT reviews:

1. The variant-comparison report at `docs/00-meta/implementation-reports/2026-04-26_phase-2l_R3_variant-comparison.md`.
2. This Gate 2 review.
3. The actual `git diff` (untracked code + test changes + new runner script + new analysis script + the two docs).
4. The R3 R-window summary metrics under `data/derived/backtests/phase-2l-r3-r/`.

If approved, the operator/Claude proceeds with the commit sequence (proposed in §1 below).

## Recommended commit structure (after Gate 2 approval)

Proposed sequence on `phase-2l/R3-first-execution`:

1. `phase-2l: R3 implementation + unit tests` — `src/prometheus/strategy/types.py`, `src/prometheus/strategy/v1_breakout/{variant_config,management,strategy,__init__}.py`, `src/prometheus/research/backtest/report.py`, `tests/unit/strategy/v1_breakout/test_variant_config.py` (the structural code change as one reviewable unit; pytest runs at 404 after this commit).
2. `phase-2l: runner + analysis script` — `scripts/phase2l_R3_first_execution.py`, `scripts/_phase2l_R3_analysis.py` (no test impact; pytest stays at 404).
3. `phase-2l: comparison report + Gate 2 review` — the two docs at `docs/00-meta/implementation-reports/2026-04-26_phase-2l_*` (no test impact).
4. `phase-2l: checkpoint report` — `docs/00-meta/implementation-reports/2026-04-26_phase-2l-checkpoint-report.md` (drafted after Gate 2 approval, immediately before this commit).

No `data/` commits. No `pyproject.toml` / `uv.lock` change. No `.claude/` change. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## Questions for ChatGPT / operator

- **Is Phase 2m the right next phase?** The variant-comparison report §11 recommends R1a structural-redesign execution as the primary path, with R1a + R3 combined as the secondary. Does the operator confirm or redirect?
- **GAP-20260424-030 disposition.** It was flagged for "SUPERSEDED-on-execution when R3 advances per Phase 2j memo §D.16" — does the operator want to mark it SUPERSEDED in the ambiguity log on the same commit, or defer the disposition update to a future docs phase?
- **TAKE_PROFIT mean-r below target interpretation.** The variant-comparison report §6.4 explains the +1.6 R (BTC) / +1.5 R (ETH) realized mean as a next-bar-open fill mechanic + fees + slippage effect, not edge erosion. Does the operator concur, or does this warrant a deeper investigation before proceeding to Phase 2m?
- **Any additional diagnostics** the operator wants emitted before commit (e.g., bootstrap CIs on the expR delta, monthly heat-map, MFE-vs-time curves) — these would be additive to the analysis script if needed.

---

**Stop point:** awaiting operator/ChatGPT Gate 2 approval. No `git add`, no `git commit`, no `git push`, no merge.
