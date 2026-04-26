# Phase 2k — Gate 1 Plan: Structural Redesign Execution Planning

**Working directory:** `C:\Prometheus`
**Plan date:** 2026-04-24
**Branch (current):** `main` at `c078eaa` — verified clean working tree, synchronized with `origin/main` after the Phase 2j PR #11 merge
**Proposed Phase 2k working branch:** `phase-2k/redesign-execution-planning` (proposal only — branch is created after Gate 1 approval per the operator's restriction)
**Scope:** Docs-only execution-planning phase. No code, no edits to source, no new backtests, no new variants, no new data, no Binance API calls, no MCP/Graphify, no `.mcp.json`, no Phase 4 work, no fallback-Wave-2 start, no edits to `docs/12-roadmap/technical-debt-register.md`.

This Gate 1 plan is currently a draft sitting in the working tree as an untracked file pending Gate 1 approval. After Gate 1 approval the file is committed to the proposed branch alongside the Gate 2 review and the checkpoint report. Phase 2k produces no separate "execution-plan memo" — the Gate 1 plan itself is the substantive planning artifact.

**Note on operator-brief docs inconsistency.** The operator's Phase 2k brief read-list included `scripts/phase2g_wave1_variants.py` but the actual on-disk path is `scripts/phase2g_variant_wave1.py` (per the Phase 2g commit `ce4ba65`). Verified by `ls c:/Prometheus/scripts/phase2g*` returning a single file. This is a minor brief-vs-disk filename inconsistency surfaced explicitly per the operator's process requirement 6 ("If prior docs conflict, surface the conflict explicitly"). It has no effect on Phase 2k planning content; the actual runner script will inform the Phase 2l implementation when it runs.

---

## Context — why this phase, why now

Phase 2j wrote complete rule specs for both Phase 2i carry-forward candidates (R1a Volatility-percentile setup; R3 Fixed-R exit with time stop), pinning singular committed sub-parameter values, defining candidate-specific falsifiable hypotheses, mapping GAP dispositions, and rating both as **READY** for a future operator-approved execution-planning phase. The Phase 2j memo §H provisional recommendation was: both advance, with R3 prioritized for first execution. The operator approved Phase 2j Gate 2 and authorized starting Phase 2k.

**Phase 2k is execution-planning only.** It plans exactly how R1a and R3 would be executed against the existing v002 datasets under the unchanged Phase 2f validation framework, without writing code, running anything, or starting a future implementation phase. The output is a set of decisions (execution order, implementation scope, report contract, validation framework restatement, readiness risks, fallback relationships, next-phase recommendation) that a future operator-approved Phase 2l can pick up directly.

---

## 1. Executive summary

Phase 2k produces a single committable Gate 1 plan (this file), a Gate 2 pre-commit review, and a checkpoint report. The Gate 1 plan addresses 14 required content sections per the operator's brief: fixed evidence recap; execution-order analysis (4 options); recommended order with reasoning; per-candidate implementation-scope planning; mandatory R3 forwarding notes; mandatory R1a execution notes; execution-plan structure (combined vs. sequential; reusable scaffolding; minimal-implementation definition; H0-bit-for-bit preservation); report-contract planning; validation framework restatement; execution-readiness risks; relationship to fallback paths; 5 next-phase options after 2k; provisional recommendation; "what would change this recommendation".

**Headline recommendation, provisional and subject to operator review:** **Phase 2l Option A — Execute R3 first, then decide on R1a (sequential).** R3 has the smaller implementation surface, lower fitting risk, sub-parameters anchored to existing project conventions, and sharper falsifiability (Phase 2f §10.3.c strict-dominance applies for an exit-philosophy-only structural change). R3's result — whether positive or negative — is informative input for whether R1a's first execution should run with H0's exit logic (R1a spec as written) or whether the operator wants to first commit to a different exit philosophy. Sequential execution preserves the Phase 2g wave-1 pattern (smaller blast radius per phase, sequential evidence, separate Gate 2 review per candidate). Fallback: **Phase 2l Option B — Implement both R1a and R3, run independently in one phase** (only if the operator wants parallel implementation evidence and accepts the larger code-change surface in a single phase). Phase 4 stays deferred.

## 2. Plain-English statement

Phase 2j said "R1a and R3 are ready to execute; R3 first." Phase 2k says: here is exactly how that execution would work — what code surfaces would change, what reports each candidate would produce, what failure modes we'd watch for during implementation, and which of four sequencing options is the disciplined choice. Phase 2k does NOT execute. Phase 2k does NOT write code. Phase 2k writes the *plan* for the future Phase 2l that does the implementation and runs.

## 3. Branch and status verification commands

After Gate 1 approval, run:

```
git -C c:/Prometheus status --short
git -C c:/Prometheus rev-parse --abbrev-ref HEAD
git -C c:/Prometheus fetch origin
git -C c:/Prometheus log --oneline -10
git -C c:/Prometheus checkout -b phase-2k/redesign-execution-planning
```

Abort gate at start of phase: if working tree is not clean (apart from this Gate 1 plan as an untracked file) or current branch is not `main`, stop and escalate.

## 4. Exact scope

- Read the Phase 2e baseline summary, Phase 2g wave-1 comparison report, Phase 2i redesign-analysis memo + checkpoint, Phase 2j structural-redesign memo + Gate 2 review + checkpoint, plus the supporting v1 spec / backtest plan / validation checklist / risk docs / strategy package source. Confirm the recap and design choices below match the on-disk record.
- Produce this Gate 1 plan with 14 required sections per the operator's brief.
- Produce a Gate 2 pre-commit review.
- Produce a Phase 2k checkpoint report.
- Stop before any commit awaiting operator/ChatGPT Gate 2 approval.

## 5. Explicit non-goals (hard boundaries)

- No code changes. No new tests. No new backtests, runs, or variants.
- No execution of R1a or R3.
- No re-running of H0 or any wave-1 H-* variant.
- No expansion of the carry-forward set beyond R1a + R3.
- No introduction of additional candidates (R1b, R2, or any new family).
- No revival of rejected wave-1 variants (H-A1, H-B2, H-C1, H-D3).
- No fallback Wave 2 / H-D6 start.
- No turning committed sub-parameter values into sweep ranges (R1a: X=25, N=200; R3: R_TARGET=2.0, TIME_STOP_BARS=8; all single committed values).
- No tightening or loosening of any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold.
- No new data downloads, no new dataset versions, no manifest changes.
- No Binance API calls (authenticated or public).
- No live-trading code, no exchange-write, no production keys.
- No MCP enablement, no `.mcp.json`, no Graphify indexing.
- No Phase 4 work.
- No edits to `docs/12-roadmap/technical-debt-register.md` (operator restriction held).
- No `data/` commits.
- No re-derivation or re-ranking of the wave-1 verdict (REJECT ALL preserved per Phase 2g).
- No re-framing of the Phase 2h, Phase 2i, or Phase 2j recommendations (all are inputs).
- No live deployment, paper/shadow readiness, or capital exposure proposal.

## 6. Fixed evidence recap

### 6.1 Why R1a is READY

Per Phase 2j memo §G.1 + supporting §C.1–C.16:

- **Spec is complete on all 16 Gate-1 checklist items**: thesis; rule shape; inputs; timeframes; predicate; replaced-vs-kept; committed sub-parameters X=25 / N=200 / warmup 221 bars; relationship to existing logic; replaced rules; preserved rules; implementation impact (descriptive); expected mechanism; expected failure mode; structural-vs-parametric justification; GAP dispositions; falsifiable hypothesis; candidate-specific diagnostics.
- **Sub-parameter values are research defaults**: X=25 (bottom quartile is the standard volatility-contraction cutoff); N=200 (≈ 50 hours of 15m bars covers multi-session vol context). Singular values; not a sweep.
- **No hidden degrees of freedom**: tie-breaking convention pinned (stable order); boundary cases (NaN seeds, ties at 25th-percentile boundary) explicitly resolved; warmup floor recomputation explicit (lookback + ATR_PERIOD + 1 = 221 bars).
- **Falsifiable hypothesis pre-committed**: passes §10.3.a or §10.3.b on R vs. H0; FALSIFIED if §10.3 fails or §10.3 disqualification triggers.

### 6.2 Why R3 is READY

Per Phase 2j memo §G.2 + supporting §D.1–D.18:

- **Spec is complete on all 18 Gate-1 checklist items**: thesis; exit philosophy; take-profit rule; time-stop rule; interaction with initial stop; committed sub-parameters R_TARGET=2.0 / TIME_STOP_BARS=8; whether staged management remains (No); whether break-even remains (Removed); whether trailing remains (Removed); replaced rules; preserved rules; implementation impact (descriptive); expected mechanism; expected failure mode; structural-vs-parametric justification; GAP dispositions; falsifiable hypothesis with §10.3.c note; candidate-specific diagnostics.
- **Sub-parameter values are anchored to existing project conventions**: R_TARGET = 2.0 (matches H0's `STAGE_5_MFE_R = 2.0` trailing-activation threshold); TIME_STOP_BARS = 8 (matches H0's `STAGNATION_BARS = 8`). Singular values; not a sweep.
- **No hidden degrees of freedom**: same-bar STOP-vs-TAKE_PROFIT priority pinned (STOP wins); time-stop fires unconditionally (no MFE gate); initial structural stop never moves intra-trade.
- **Falsifiable hypothesis pre-committed**: passes §10.3.a, §10.3.b, OR §10.3.c (strict-dominance for exit-philosophy change applicable) on R vs. H0; FALSIFIED if §10.3 fails or §10.3 disqualification triggers.

### 6.3 Why R3 is prioritized first

Per Phase 2j memo §E and §H:

- **Smaller implementation surface**: ~5–7 source files modified (TradeManagement extension or sibling class; ExitReason enum extension; engine/report/trade_log routing for new exit reasons; tests). R1a's surface is ~10 source files (rolling ATR-percentile cache; new setup-predicate dispatch; warmup floor recomputation; funnel-attribution branch; tests).
- **Lower fitting risk**: R3's two sub-parameters both align with existing project conventions. R1a's two sub-parameters have wider plausible alternative ranges (X = 20/25/30; N = 100/200/500), making the "research default" claim more defensible but the underlying space wider.
- **Sharper falsifiability**: §10.3.c (exit-model bake-off strict dominance) is applicable to R3 because R3 changes only the exit philosophy. R1a is not eligible for §10.3.c. Three promotion paths > two.
- **Sub-parameters anchored to existing conventions**: R3's 2.0R = H0's STAGE_5_MFE_R; R3's 8 bars = H0's STAGNATION_BARS. R1a's 25th percentile / 200-bar lookback are project-new.

### 6.4 What remains unchanged from Phase 2f / 2g / 2i / 2j

- **Phase 2g wave-1 verdict (REJECT ALL).** No re-derivation. No re-ranking. Wave-1 numbers may be cited diagnostically but do not serve as comparison baselines for R1a or R3.
- **H0 as the sole comparison anchor.** All §10.3 / §10.4 evaluation is computed vs. H0, never vs. wave-1 variants.
- **Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds.** Applied unchanged.
- **Phase 2f §11.3.5 pre-committed-thresholds discipline.** Thresholds are pre-committed and cannot be tightened or loosened after seeing results.
- **Phase 2f §11.1 R/V split.** R = 2022-01-01 → 2025-01-01 (36 months); V = 2025-01-01 → 2026-04-01 (15 months).
- **GAP-20260424-036 fold convention.** 5 rolling folds, fold 1 partial-train, all tests within R.
- **Phase 2i §1.7 binding structural-vs-parametric test.** R1a and R3's structural classification under §1.7 stays.
- **Phase 2i §1.7.3 project-level locks.** BTCUSDT live primary; one-position max; isolated margin; 0.25% live risk; 2x leverage; mark-price stops; v002 datasets.
- **Phase 2j R1a + R3 specs.** Sub-parameter values committed singularly. No sweep. No re-spec without operator authorization.
- **Phase 2h provisional recommendation framing.** Phase 2h is the input that led to Phase 2i/2j/2k. Not a target for revision.

---

## 7. Execution-order analysis (4 options)

The operator's brief required comparing at least four sequencing options. Each is evaluated on pros / cons / contamination risk / wasted-effort risk / expected value of information.

### 7.1 Option 1 — R3 first, then R1a (sequential)

| Aspect | Detail |
|---|---|
| Pros | Smaller implementation surface per phase; sequential evidence (R3 result informs R1a planning); same proven Phase 2g wave-1 pattern; cleaner Gate 2 review per candidate; smaller blast radius if implementation has a bug |
| Cons | Two phase-init costs (Gate 1 plan + Gate 2 review per phase × 2); slower wall-clock to get both candidates evaluated |
| Contamination risk | LOW. R3 and R1a touch disjoint code surfaces (R3 = TradeManagement + ExitReason enum; R1a = setup detector + StrategySession ATR-history cache). Sequential commits land on separate branches with separate Gate 2 reviews |
| Wasted-effort risk | LOW. R3 implementation is a pre-investment that R1a can reuse for the V1BreakoutConfig extension pattern |
| EVI | HIGH. R3's clean falsifiability gives a high-info first result regardless of outcome |

### 7.2 Option 2 — R1a first, then R3 (sequential, reverse order)

| Aspect | Detail |
|---|---|
| Pros | Targets the dominant 58% no-valid-setup funnel rejection first; if R1a has a positive result, R3 can be designed against the new setup distribution rather than H0 |
| Cons | Larger implementation surface in the first phase (R1a needs rolling ATR-percentile cache + new dispatch + warmup recomputation + funnel-attribution branch); higher up-front complexity; R1a's per-fold sample-size sensitivity makes its result harder to interpret cleanly |
| Contamination risk | LOW (same as Option 1) |
| Wasted-effort risk | MEDIUM. If R1a turns out to need spec refinement (e.g., the percentile predicate needs different sub-params for credibility), the project has invested effort in larger code surfaces before the cleaner R3 test has run |
| EVI | MEDIUM. R1a's two sub-parameters and wider implementation surface mean the result is somewhat more dependent on the spec choices than R3's |

### 7.3 Option 3 — Both implemented in one execution phase but run independently

| Aspect | Detail |
|---|---|
| Pros | Single phase-init cost; the V1BreakoutConfig extension pattern lands once for both candidates; runs are still independent (R1a vs. H0; R3 vs. H0; no cross-comparison); shared scaffolding across runners |
| Cons | Larger code-change surface in a single phase (~12–17 source files modified, plus tests for both); more difficult Gate 2 review (two specs to verify in one diff); larger H0-preservation test surface (must prove BOTH R1a defaults preserve H0 AND R3 defaults preserve H0); higher implementation-bug blast radius |
| Contamination risk | MEDIUM. The two candidates' code paths touch shared infrastructure (V1BreakoutConfig, StrategySession constructor, Engine init). A bug in one path could corrupt the other's tests |
| Wasted-effort risk | LOW-MEDIUM. If both ship cleanly, this is the most efficient option. If implementation drags, the bundling slows both candidates |
| EVI | MEDIUM-HIGH. Both candidates' results land at once, enabling a side-by-side comparison; but without sequential evidence, design decisions cannot be informed by the first result |

### 7.4 Option 4 — Only one candidate implemented first; the other deferred

| Aspect | Detail |
|---|---|
| Pros | Most cautious; smallest implementation surface; if the first candidate fails cleanly, the second can be re-evaluated against new evidence rather than committed prematurely |
| Cons | Defers the question on the deferred candidate indefinitely; requires explicit operator authorization to drop one candidate from carry-forward, which is a Phase 2i ≤ 2 cap discipline modification |
| Contamination risk | LOW |
| Wasted-effort risk | LOW for the implemented candidate; HIGH for the deferred candidate if it stays deferred and then the operator asks for it later (the spec is fresh now; cold spec re-review is harder) |
| EVI | MEDIUM. One candidate's result is informative; the other's is delayed |

### 7.5 Comparison summary

| Option | Surface per phase | Sequential evidence? | Phase-init cost | Best when |
|---|---|---|---|---|
| 1 — R3 first, R1a after | Small (R3 only) | Yes | 2× | Default; same as Phase 2g pattern |
| 2 — R1a first, R3 after | Medium-large (R1a only) | Yes | 2× | If operator wants funnel-rejection axis evidence first |
| 3 — Both in one phase | Large (both) | No | 1× | If operator wants parallel evidence and accepts the larger surface |
| 4 — One only, other deferred | Smallest | n/a | 1× | If operator decides to drop one candidate (Phase 2i cap deviation) |

## 8. Recommended execution order

**Recommendation: Option 1 — R3 first, then R1a (sequential).**

Reasoning:

1. **Smaller implementation surface per phase.** R3's ~5–7 source files vs. R1a's ~10 source files makes R3's first-execution Gate 2 review cleaner; the H0-preservation surface is smaller; bugs are easier to isolate.
2. **Sharper falsifiability.** §10.3.c strict-dominance is applicable to R3 because R3 changes only the exit philosophy. R3's outcome is more clearly attributable to the exit-philosophy change.
3. **Sub-parameters anchored to existing project conventions.** R3's R_TARGET=2.0 = H0's STAGE_5_MFE_R; R3's TIME_STOP_BARS=8 = H0's STAGNATION_BARS. These values land without introducing new "what is this number?" questions.
4. **Sequential evidence informs the next candidate's planning.** R3's result (whether positive or negative) is an input for whether R1a's first execution should keep H0's exit logic (R1a spec as written) or whether the operator wants to first commit to a different exit philosophy. R1a-first does not have this advantage because the setup-redesign is upstream of any exit decision.
5. **Same proven Phase 2g pattern.** Phase 2g executed wave-1 variants sequentially within a single phase, but with one variant per invocation and separate output directories. Phase 2k inherits the runner / report-contract / Gate-2 pattern; sequential execution across phases is the natural Phase 2g extension.
6. **Phase 2j memo §H already recommended R3 first** with the same reasoning; Phase 2k validates rather than overrides.

**Fallback recommendation: Option 3 — Both in one phase.** If the operator wants both R1a and R3 results in parallel and accepts the larger surface in a single phase, Option 3 is the next-best choice. Still strictly sequential within the phase (run R3 to completion before running R1a, so any state-leak bug surfaces on R3 first); but commits land in one branch, the V1BreakoutConfig extension pattern is established once, and the comparison report is a single document.

Options 2 (R1a first) and 4 (one only) are not recommended without explicit operator preference.

## 9. Implementation-scope planning

For each candidate, the future Phase 2l execution phase would change the following code surfaces. **Phase 2k does not write any of this code; the surface descriptions are derived from the Phase 2j memo §C.10 and §D.12 implementation-impact paragraphs.**

### 9.1 R3 — Fixed-R exit with time stop

**V1BreakoutConfig (`src/prometheus/strategy/v1_breakout/variant_config.py`).** Add three new fields:

- `exit_kind: Literal["STAGED_TRAILING", "FIXED_R_TIME_STOP"] = "STAGED_TRAILING"` (default preserves H0).
- `exit_r_target: float = 2.0` (used only when `exit_kind == FIXED_R_TIME_STOP`).
- `exit_time_stop_bars: int = 8` (same).

**Strategy package (`src/prometheus/strategy/v1_breakout/management.py`).** Either extend `TradeManagement.on_completed_bar` to dispatch on `exit_kind` OR add a sibling `FixedRTimeStopManagement` class. Extension to `ExitReason` enum: add `TAKE_PROFIT` and `TIME_STOP` values. Same-bar priority enforcement: when both protective stop and take-profit fire on the same bar, the protective stop wins (mirrors H0's `_close_trade_on_stop` priority in `engine.py`).

**Strategy orchestrator (`src/prometheus/strategy/v1_breakout/strategy.py`).** `V1BreakoutStrategy.manage` routes through the new dispatcher (or constructs the appropriate management class at entry time).

**Backtester (`src/prometheus/research/backtest/engine.py`).** Handle the two new exit reasons in the existing managed-exit and stop-close paths. The new exit reasons may need new internal handler methods (e.g., `_close_trade_take_profit`, `_close_trade_time_stop`) but more likely reuse `_close_trade_managed` with the new ExitReason values passed through.

**Trade log (`src/prometheus/research/backtest/trade_log.py`).** Verify `TradeRecord.exit_reason` accepts the new ExitReason enum values (currently a string field per Phase 2g); no schema migration needed for parquet/json round-trips.

**Reporter (`src/prometheus/research/backtest/report.py`).** Extend the monthly/yearly aggregator counters to track `take_profit_exits` and `time_stop_exits` separately. The existing `stop_exits`, `trailing_exits`, `stagnation_exits`, `end_of_data_exits` columns stay (R3 just won't emit `trailing_exits` or `stagnation_exits`).

**Diagnostics (`src/prometheus/research/backtest/diagnostics.py`).** No change — `run_signal_funnel` is observational and tracks pre-entry rejections; R3 is a post-entry exit-logic change.

**Tests (`tests/unit/strategy/v1_breakout/test_redesign_R3.py` new file).** Prove (a) defaults preserve H0 bit-for-bit; (b) `FIXED_R_TIME_STOP` with R_TARGET=2.0 / TIME_STOP_BARS=8 produces the expected behavior on hand-checkable fixtures; (c) same-bar STOP-and-TAKE_PROFIT priority resolves to STOP; (d) `TIME_STOP` fires unconditionally at 8 bars regardless of MFE; (e) initial protective stop is never moved during the trade.

**Runner script (`scripts/phase2l_redesign_R3.py` new file).** Mirror `scripts/phase2g_variant_wave1.py` (the actual on-disk filename, not the operator-brief filename `phase2g_wave1_variants.py`). One invocation per (variant=H0|R3, window=R|V, slippage=LOW|MEDIUM|HIGH, stop_trigger=MARK_PRICE|TRADE_PRICE).

**Comparison report and analysis helper.** A `scripts/_phase2l_R3_analysis.py` (gitignored or read-only utility) plus a committed `docs/00-meta/implementation-reports/<date>_phase-2l_R3_variant-comparison.md`.

### 9.2 R1a — Volatility-percentile setup

**V1BreakoutConfig.** Add three new fields:

- `setup_predicate_kind: Literal["RANGE_BASED", "VOLATILITY_PERCENTILE"] = "RANGE_BASED"` (default preserves H0).
- `setup_percentile_threshold: int = 25` (used only when `setup_predicate_kind == VOLATILITY_PERCENTILE`).
- `setup_percentile_lookback: int = 200`.

**Strategy package (`src/prometheus/strategy/v1_breakout/setup.py`).** Add sibling `detect_setup_volatility_percentile(prior_bars, atr_prior_15m, atr_history, *, percentile_threshold: int, lookback: int) -> SetupWindow | None`. Tie-breaking convention: stable order (per Phase 2j memo §C.5).

**Strategy session (`src/prometheus/strategy/v1_breakout/strategy.py`).** `StrategySession` maintains a rolling deque of `atr_prior_15m` values of length `setup_percentile_lookback` (similar pattern to the existing `_1h_ema_fast_history`). `MIN_15M_BARS_FOR_SIGNAL` becomes config-aware: for `VOLATILITY_PERCENTILE`, the warmup floor is `lookback + ATR_PERIOD + 1` (= 221 at committed values).

**Strategy orchestrator.** `V1BreakoutStrategy.maybe_entry` dispatches on `config.setup_predicate_kind` to call either `detect_setup` (H0) or `detect_setup_volatility_percentile` (R1a).

**Diagnostics (`src/prometheus/research/backtest/diagnostics.py`).** `_IncrementalIndicators` maintains a parallel ATR-history ring for the funnel's `rejected_no_valid_setup` attribution to remain accurate per-config.

**Funnel attribution.** R1a still attributes a failing setup to `rejected_no_valid_setup` (no new bucket needed; the rejection reason is the same — just computed via a different predicate).

**Backtester / Trade log / Reporter.** No change. R1a does not change exit logic, sizing, or trade-record schema.

**Tests (`tests/unit/strategy/v1_breakout/test_redesign_R1a.py` new file).** Prove (a) defaults preserve H0 bit-for-bit; (b) `VOLATILITY_PERCENTILE` with X=25 / N=200 produces the expected admit/reject behavior; (c) tie-breaking is stable; (d) NaN-seed boundary cases reject; (e) warmup floor of 221 bars is respected; (f) the funnel still increments `rejected_no_valid_setup` on rejection.

**Runner script (`scripts/phase2l_redesign_R1a.py` new file).** Mirror Phase 2g pattern.

**Comparison report.** Same structure as R3's, with R1a-specific diagnostic columns added.

### 9.3 Reusable scaffolding between candidates

If Option 3 (both in one phase) is chosen:

- The V1BreakoutConfig extension pattern is shared (one file edit adds both candidates' fields).
- Runner-script helpers (data loading, dataset citations, manifest writing) are shared via the existing `phase2g_variant_wave1.py` pattern.
- The comparison-report Python helper is shared.

If Option 1 (sequential) is chosen, R3's Phase 2l establishes the V1BreakoutConfig extension pattern; R1a's later phase reuses it without churn.

### 9.4 Minimal-implementation definition

For each candidate, "minimal implementation" means:

- Add only the new V1BreakoutConfig fields needed for that candidate.
- Add only the new strategy-package code paths for that candidate.
- Add only the new tests for that candidate (plus regression tests proving H0 preservation).
- Add the runner script.
- No refactoring of existing code beyond what is strictly required to support the new dispatch path.
- No new dependencies.
- No schema migrations beyond the optional ExitReason enum extension for R3.

### 9.5 H0 bit-for-bit preservation requirements

Every implementation phase must prove:

- `V1BreakoutConfig()` (no overrides) produces a config equivalent to the locked Phase 2e baseline.
- `StrategySession(symbol=..., config=V1BreakoutConfig())` produces session state equivalent to the locked Phase 2e baseline.
- `BacktestEngine(BacktestConfig(..., strategy_variant=V1BreakoutConfig()))` produces a run equivalent to Phase 2g's H0 run.
- A regression test re-runs H0 on R and asserts identical trade counts (BTC 33, ETH 33), identical expR, identical PF, identical exit-reason histogram. **This test is mandatory** — without it, H0-preservation is unverified.

Phase 2g's existing tests already provide most of this surface; the Phase 2l implementation phase extends the regression-test coverage.

## 10. Required R3 forwarding notes (preserved from operator non-blocking note in Phase 2j)

These items were called out by the operator in the Phase 2j Gate 2 approval message and were recorded verbatim in the Phase 2j checkpoint report's "Forwarding notes for Phase 2k" section. They are now restated explicitly in this Gate 1 plan so they are not lost in transit to Phase 2l:

- **R3 same-bar priority: STOP over TAKE_PROFIT.** When a single 15m bar simultaneously satisfies the protective-stop hit condition AND the take-profit condition (price reaches `entry_price + R_TARGET × initial_R` in the same bar that the mark-price stops out), the protective stop wins. This is the conservative, H0-aligned choice. Phase 2j memo §D.3 records the convention; the Phase 2l implementation must enforce it (typically by checking the protective-stop branch first, before the take-profit check, in the per-bar loop).
- **New exit reasons: `TAKE_PROFIT` and `TIME_STOP`.** The `ExitReason` enum extends with these two values. The trade-record schema, the monthly/yearly aggregator, and the funnel/report schemas all need to handle them. R3 will not emit `TRAILING_BREACH` or `STAGNATION` because the underlying logic is removed; if either appears in an R3 trade log, that is an implementation bug and the report should flag it.
- **R3 remains under the same Phase 2f framework.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds apply unchanged. The §11.3.5 pre-committed-thresholds discipline is binding. There is no special "R3 framework" or "redesign framework"; the same comparison anchors, the same disqualification floor, the same disciplines apply.
- **§10.3.c is treated as an additional strict-dominance path if applicable, not as a framework rewrite.** R3's primary promotion paths are §10.3.a (Δexp ≥ +0.10R AND ΔPF ≥ +0.05) and §10.3.b (Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse > 1.0pp). §10.3.c is available because R3 is structurally an exit-philosophy change; if R3 strictly dominates H0 on both expR and maxDD, that qualifies as promotion regardless of the trade-count change. §10.3.c does NOT replace §10.3.a/b — it is additional.

## 11. Required R1a execution notes (preserved explicitly per operator brief)

The operator's Phase 2k brief required these items to be preserved explicitly. They are restated here for the Phase 2l implementation:

- **The 8-bar setup window remains.** R1a does not change the window length. The 8 bars strictly before the breakout candidate still define `setup_high` (max of those 8 bars' high) and `setup_low` (min of those 8 bars' low) — used downstream by the trigger. `SETUP_SIZE = 8` in `setup.py` stays.
- **The percentile predicate replaces only the setup-validity rule.** R1a does not change the trigger, the bias, the entry timing, the stop calculation, the exit logic, or the sizing pipeline. The `MAX_RANGE_ATR_MULT = 1.75` and `MAX_DRIFT_RATIO = 0.35` constants are no longer in the predicate logic when `setup_predicate_kind == VOLATILITY_PERCENTILE`, but they stay in the file (used when `setup_predicate_kind == RANGE_BASED` for H0).
- **X = 25 and N = 200 are single committed values, not sweep ranges.** The Phase 2l implementation cannot test 20/25/30 or 100/200/500. If the operator wants different values, it requires a new operator-approved spec (a separate Phase 2j-equivalent for a sibling candidate, e.g., R1a' with X=20).
- **Warmup floor implications must be handled explicitly.** When `setup_predicate_kind == VOLATILITY_PERCENTILE`, the `MIN_15M_BARS_FOR_SIGNAL` floor must become `setup_percentile_lookback + ATR_PERIOD + 1` = 221 bars (vs. H0's 30 bars). This affects the very first valid signal date in the R window: at Phase 2g's wave-1 indices the warmup-excluded count is 29 bars; for R1a with N=200 it would be 220 bars. The Phase 2g v002 dataset has 148,896 15m bars per symbol, so warmup-excluded ~220 is an immaterial fraction of the window, but the comparison-report's funnel attribution must show the higher warmup count for R1a and the comparison must recognize it.
- **Funnel attribution must remain interpretable.** R1a still attributes a setup-validity failure to `rejected_no_valid_setup` — same bucket as H0. The comparison report should add a per-fold "setup-validity-rate" diagnostic that shows how often R1a's predicate accepts vs. how often H0's predicate accepts, so the reader can see whether R1a is genuinely capturing more compressions or genuinely fewer (per Phase 2j memo §C.16 mandatory diagnostics).

## 12. Execution-plan structure

### 12.1 One combined phase or one candidate at a time?

Per §8 recommendation: **one candidate at a time** (Option 1 sequential — R3 first, then R1a). If the operator chooses Option 3 (both in one phase), the structure changes to one combined phase with strict sequential execution within it (R3 to completion before R1a starts).

### 12.2 Reusable scaffolding

Per §9.3:

- V1BreakoutConfig extension pattern (new optional fields with H0-preserving defaults). One Python file edit.
- Runner-script helpers (data loading, manifest writing, dataset citations). Shared via the existing `phase2g_variant_wave1.py` pattern.
- Comparison-report Python helper. Shared.

R3's phase establishes these patterns; R1a's later phase reuses them. No second-phase rework.

### 12.3 Minimal-implementation definition

Per §9.4. The definition is binding for both candidates: only what's strictly needed for that candidate, no opportunistic refactoring.

### 12.4 H0 bit-for-bit preservation

Per §9.5. The mandatory regression test re-runs H0 on R and asserts identical trade counts / metrics. This is not negotiable. If the regression fails, the implementation has a bug, and Phase 2l stops and escalates.

## 13. Report-contract planning

Each future execution phase produces:

### 13.1 Per-symbol per-variant artifacts (mirroring Phase 2g)

Per the existing `phase2g_variant_wave1.py` output structure, every run produces:

- `data/derived/backtests/<experiment>/<run_id>/<symbol>/trade_log.{parquet,json}`
- `data/derived/backtests/<experiment>/<run_id>/<symbol>/summary_metrics.json`
- `data/derived/backtests/<experiment>/<run_id>/<symbol>/funnel_total.json`
- `data/derived/backtests/<experiment>/<run_id>/<symbol>/equity_curve.parquet`
- `data/derived/backtests/<experiment>/<run_id>/<symbol>/drawdown.parquet`
- `data/derived/backtests/<experiment>/<run_id>/<symbol>/r_multiple_hist.parquet`
- `data/derived/backtests/<experiment>/<run_id>/<symbol>/monthly_breakdown.parquet`
- `data/derived/backtests/<experiment>/<run_id>/<symbol>/yearly_breakdown.parquet`
- `data/derived/backtests/<experiment>/<run_id>/backtest_report.manifest.json`
- `data/derived/backtests/<experiment>/<run_id>/config_snapshot.json`

All under git-ignored `data/derived/`.

### 13.2 Candidate-specific outputs (in addition to existing schema)

**R1a-specific (per Phase 2j memo §C.16):**

- `setup_validity_rate_per_fold.parquet` (per-fold setup-validity rate for R1a vs. H0).
- `atr_percentile_distribution_at_entries.parquet` (the realized percentile rank of `atr_prior_15m` at each filled entry).

**R3-specific (per Phase 2j memo §D.18):**

- `exit_reason_histogram_extended.parquet` (per fold per symbol counts for STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA — should not contain TRAILING_BREACH or STAGNATION for R3 trades; if it does, the report flags an implementation bug).
- `take_profit_r_multiple_distribution.parquet` (realized R-multiple at TAKE_PROFIT fills; should cluster near +2.0 R minus slippage).
- `time_stop_bias_diagnostic.json` (fraction of TIME_STOP exits where MFE was positive at fire vs. negative).

### 13.3 Common diagnostics (mandatory for both candidates per Phase 2i §2.5.5)

- **Per-regime expR.** Trade entries classified by realized 1h volatility regime (low/medium/high based on trailing-percentile classification of 1h ATR(20) at entry).
- **MFE distribution.** Histogram of MFE in R-multiples to characterize where in the trade lifecycle profit is captured.
- **Per-direction long/short asymmetry.** Separate expR / PF / win rate for long-only and short-only subsets.
- **GAP-032 mark-price stop-trigger sensitivity.** Each promoted candidate runs with `stop_trigger_source=TRADE_PRICE` and reports the comparison vs. MARK_PRICE.

### 13.4 Committed comparison report

A `docs/00-meta/implementation-reports/<date>_phase-2l_<candidate>_variant-comparison.md` per execution phase. The committed report:

- Quotes H0's R-window numbers as the comparison anchor (per §F.1 of Phase 2j memo).
- Shows R-window per-variant table.
- Shows deltas vs. H0.
- Shows per-fold breakdown (5 rolling folds per GAP-036).
- Shows §3.A supplemental 6-half-year appendix (descriptive only, not for ranking).
- Shows signal-funnel diff (R1a's `rejected_no_valid_setup` count vs. H0's; R3's funnel will be identical to H0's pre-entry).
- Shows §7.5 trade-frequency sanity-check diagnostics.
- Applies §10.3 / §10.4 classification.
- Documents promotion / disqualification per pre-declared thresholds.
- For promoted candidates: V-window results + slippage sensitivity (LOW/HIGH) + GAP-032 mark-price sensitivity.

### 13.5 H0 comparison presentation

Each comparison report's row 0 is H0 (re-run on R for the candidate's window). All subsequent rows are the candidate(s). Deltas vs. row 0 are shown for every metric. Wave-1 variants do NOT appear in the comparison-report row set — they may appear only in a separate "Historical evidence (Phase 2g)" appendix for context, clearly labeled as not-a-comparison-baseline (per Phase 2j §F.2).

### 13.6 R/V and fold separation

- Run R first. Apply §10.3 / §10.4 thresholds on R only.
- If candidate clears §10.3 (with no §10.3 disqualification), promote to V per §11.3 top-1–2 rule.
- If candidate triggers §10.3 disqualification on R, no V run (per §11.3 no-peeking).
- Per-fold breakdown is computed on R only (5 rolling folds per GAP-036). V is treated as a single 15-month window.
- The committed comparison report shows R results, fold breakdown, and (if applicable) V results in three clearly-separated sections.

## 14. Validation framework restatement

Preserved exactly from Phase 2j memo §F. Restated here for Phase 2l hand-off:

### 14.1 H0 only anchor

H0 (locked Phase 2e baseline re-run on R) is the only comparison anchor for any redesign candidate. All §10.3 / §10.4 evaluation for R1a or R3 is computed vs. H0's R-window numbers, never vs. wave-1 variants.

### 14.2 Wave-1 historical evidence only

Phase 2g wave-1 variants (H-A1, H-B2, H-C1, H-D3) are historical evidence only, not promotion baselines. Their R-window numbers may be cited diagnostically but they do not serve as comparison anchors for any redesign §10.3 / §10.4 evaluation.

### 14.3 Unchanged §10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework

- **§10.3 promotion paths**: §10.3.a (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05); §10.3.b (Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse > 1.0 pp); §10.3.c (exit-model bake-off strict dominance — applicable to R3 only).
- **§10.3 disqualification floor**: worse expR, worse PF, |maxDD| > 1.5× baseline, broken funnel invariant, failed conformity check.
- **§10.4 hard reject**: rising trades AND (expR < −0.50 OR PF < 0.30).
- **§11.3 no-peeking + top-1–2 promotion to V.**
- **§11.4 ETH-as-comparison**: BTC must clear; ETH must not catastrophically fail.
- **§11.6 cost-sensitivity**: any §10.3 pass on MEDIUM slippage must also pass on LOW and HIGH; HIGH-slippage inversion demotes to "fragile".

All thresholds applied unchanged. **§11.3.5 binding: thresholds are pre-committed and cannot be tightened or loosened after seeing results.**

### 14.4 Unchanged R/V split

R = 2022-01-01 → 2025-01-01 (36 months). V = 2025-01-01 → 2026-04-01 (15 months). Reserved for top-1–2 promoted candidates only.

### 14.5 Unchanged GAP-036 fold convention

5 rolling folds, fold 1 partial-train, all tests within R. Supplemental 6-half-year appendix retained for descriptive coverage (per Phase 2g §3.A).

### 14.6 No post-hoc threshold loosening

Per §11.3.5: thresholds are pre-committed. The Phase 2l execution phase cannot loosen thresholds because the redesign hypothesis is "different". If a redesign disqualifies under §10.3, it disqualifies. The discipline is binding.

## 15. Execution-readiness risks (what could still go wrong during implementation)

### 15.1 R1a implementation risks

- **Rolling ATR-percentile cache leaking state across symbols.** If `StrategySession` is constructed once per symbol (it is, per `engine.py:_SymbolRun`), the per-symbol ATR-history deque is isolated. But if a future refactor accidentally shares state, the percentile would be cross-contaminated. Mitigation: explicit unit test that two `StrategySession` instances have independent ATR-history buffers.
- **Tie-breaking convention inconsistency.** If the tie-breaking implementation deviates from "stable order" (e.g., using `sorted()` in a way that's not deterministic across runs), the result becomes non-reproducible. Mitigation: explicit unit test fixture that constructs an ATR-history with ties at the 25th-percentile boundary and asserts the predicate's accept/reject decision is bit-for-bit consistent across runs.
- **Warmup floor recomputation regression.** If H0 default's warmup floor (30 bars) is accidentally changed to R1a's warmup floor (221 bars) or vice versa, H0 trade counts would change. Mitigation: the H0 bit-for-bit preservation regression test (§9.5) catches this.
- **Funnel attribution double-counting.** If R1a's predicate-failure path increments `rejected_no_valid_setup` but the diagnostics also increments it via a separate path, the funnel invariant (`sum of all rejection buckets + entries = decision_bars`) breaks. Mitigation: unit test that asserts the invariant on a fixture run.

### 15.2 R3 implementation risks

- **Same-bar STOP-vs-TAKE_PROFIT priority bug.** If the priority is implemented in the wrong order (take-profit checked before stop), R3's results would diverge from spec on every bar where both fire. Mitigation: explicit unit test fixture with a bar that simultaneously hits both, asserting the trade closes at `STOP` not `TAKE_PROFIT`.
- **ExitReason enum extension breaking trade_log Pydantic validation.** If `TradeRecord.exit_reason` validation rejects the new strings, deserialization of R3 trade logs fails. Mitigation: unit test that round-trips a `TradeRecord` with `exit_reason="TAKE_PROFIT"` and `"TIME_STOP"` through Pydantic + parquet + json.
- **Stage 3 / 4 / 5 logic accidentally retained when `exit_kind=FIXED_R_TIME_STOP`.** If the dispatch path leaks even one Stage transition into R3's path, the trade-management state machine produces unexpected stop moves. Mitigation: unit test that asserts an R3 trade emits zero `StopUpdateIntent` events (because the stop never moves intra-trade for R3).
- **Initial structural stop accidentally moved.** If a refactor introduces a path where R3's stop is moved (e.g., a residual break-even check), R3 behavior diverges from spec. Mitigation: unit test that constructs a long trade reaching MFE +1.5R, then drifting back, and asserts the stop level is unchanged.
- **Existing ExitReason values still emitted by R3.** If `TRAILING_BREACH` or `STAGNATION` appears in an R3 trade log, the dispatch path leaked H0 logic. Mitigation: comparison-report check (§13.2) that flags any unexpected exit-reason emission.

### 15.3 What requires stop-and-escalate during the future execution phase

Phase 2l (or any execution phase) must STOP and ESCALATE if any of the following occurs:

- **H0 bit-for-bit preservation regression test fails.** The regression must produce identical trade counts and metrics. Any divergence is a bug.
- **A pytest test in the existing 396-test baseline fails.** No `--no-verify`. No skipping. The code change must preserve all existing tests.
- **A sub-parameter sweep is proposed.** R1a's X=25, N=200 and R3's R_TARGET=2.0, TIME_STOP_BARS=8 are committed singularly. A sweep is forbidden by Phase 2j and operator process requirement 4. If implementation finds the spec underdetermined, escalate to docs.
- **A cross-candidate dependency surfaces.** If R3's implementation accidentally affects R1a's behavior or vice versa, the two should not be implemented in the same phase. Stop and escalate.
- **The §10.3 / §10.4 thresholds are proposed to change.** Per §11.3.5 they are pre-committed. Stop and escalate.
- **A new ExitReason value beyond TAKE_PROFIT and TIME_STOP is proposed.** R3's spec is final; new exit reasons require operator authorization.
- **Any Phase 2i §1.7.3 project-level lock is proposed to change.** Locks are not negotiable in Phase 2l.

## 16. Relationship to fallback paths

### 16.1 When fallback H-D6 Wave 2 should still supersede redesign execution

Per Phase 2h §3.3 and Phase 2i §3.4 switch conditions: fallback Wave 2 with H-D6 supersedes redesign execution if:

- The operator concludes that exit-model evidence (H-D6 bake-off) should precede any structural redesign.
- The Phase 2k / 2l analysis surfaces a hidden DOF in R1a or R3 that requires more docs work, and the operator prefers parameter-search evidence in the meantime.
- An operator-approved review concludes that the structural-redesign space is design-vacuum-prone and parameter-search has more EVI on the exit axis.

Phase 2k does not propose this switch; the Phase 2j §H recommendation favors structural redesign. The switch remains available per §I.4 of the Phase 2j memo.

### 16.2 When Phase 4 should still remain deferred

Phase 4 stays deferred (existing operator policy) unless:

- Operator policy explicitly changes to accept building operational infrastructure without strategy-edge confirmation.
- Phase 2l execution produces a clean negative on both R3 and R1a, AND the operator concludes that further structural-redesign exhaustion (R1b, R2) is not worth pursuing, AND the operator wants operational readiness work next.

Phase 2k does not propose advancing Phase 4.

### 16.3 When a docs-only clarification phase would still be preferable

A docs-only clarification phase supersedes Phase 2l execution if:

- Phase 2k Gate 2 review (this phase's later step) discovers a documentation inconsistency in the Phase 2j R1a or R3 specs that requires correction before implementation.
- Operator decides to refine the §11.3.5 threshold-application discipline (e.g., explicit guidance on tie-breaking at ratio boundaries) before any execution.
- A new ambiguity surfaces during Phase 2k planning that affects R1a or R3 specs (currently no new GAP anticipated; if surfaces, this is the trigger).

Phase 2k anticipates that no clarification is needed; if surfaces during Gate 2 review, this is a switch condition.

## 17. Proposed next-phase options after 2k (5-option comparison)

### Option A — Phase 2l: Execute R3 first, then decide on R1a

| Aspect | Detail |
|---|---|
| Pros | Smaller implementation surface; sharper falsifiability (§10.3.c applies); sub-parameters anchored to existing project conventions; sequential evidence (R3 result informs R1a planning); same proven Phase 2g pattern |
| Cons | Two separate phase-init costs; slower wall-clock to evaluate both candidates |
| Wasted-effort risk | LOW |
| EVI | HIGH — clean R3 falsifiability; informative whatever the outcome |

### Option B — Phase 2l: Implement both R1a and R3, run independently in one phase

| Aspect | Detail |
|---|---|
| Pros | Single phase-init cost; V1BreakoutConfig extension pattern lands once; comparison report is a single document; both candidate results land at once |
| Cons | Larger code-change surface in one phase (~12–17 source files); harder Gate 2 review (two specs to verify in one diff); larger H0-preservation test surface; higher implementation-bug blast radius |
| Wasted-effort risk | LOW-MEDIUM (depends on whether both implementations land cleanly) |
| EVI | MEDIUM-HIGH — parallel evidence; but no sequential learning |

### Option C — Another docs-only clarification phase

| Aspect | Detail |
|---|---|
| Pros | Most cautious; resolves any spec ambiguity surfaced during Phase 2k Gate 2 review before code |
| Cons | Slows progress; Phase 2j memo §G already rated both candidates READY, so a new docs phase is redundant unless a real ambiguity surfaces |
| Wasted-effort risk | LOW (a clarification phase always pays for itself if a real ambiguity exists) |
| EVI | LOW — only useful if there's a real ambiguity to resolve |

### Option D — Fallback Wave 2 with H-D6

| Aspect | Detail |
|---|---|
| Pros | Tests an axis Wave 1 left untouched (exit-model bake-off across multiple philosophies); uses existing infrastructure |
| Cons | Pauses redesign discipline; takes a parameter-search step that wave-1 evidence already suggested is the wrong direction (per Phase 2h §3.3); R3 is a structural commitment to one philosophy that absorbs the H-D6 question if executed |
| Wasted-effort risk | MEDIUM-LOW (H-D6 has high info value regardless); MEDIUM (the structural-redesign question stays unanswered) |
| EVI | HIGH for H-D6 result; structural-redesign question deferred |

### Option E — Phase 4: Runtime / state / persistence

| Aspect | Detail |
|---|---|
| Pros | Decoupled from strategy debate; required for any future paper/shadow/live |
| Cons | Premature without strategy-edge confirmation (current operator policy is against this); strategy-coupled parts will need re-review after redesign execution |
| Wasted-effort risk | LOW for strategy-agnostic parts; MEDIUM-HIGH for strategy-coupled parts |
| EVI | LOW on strategy question |

## 18. Final recommendation (provisional; subject to operator/ChatGPT review)

This recommendation is **provisional and evidence-based, not definitive**. It is a judgement about the highest-value next step given the current evidence. It is explicitly **not** any of the following:

- It is **not** a claim that R3 first is permanently the right ordering. Operator may legitimately prefer Option B (both at once).
- It is **not** a claim that R1a or R3 will produce a positive result. Each is a research bet with a falsifiable hypothesis.
- It is **not** a recommendation for live deployment, paper/shadow readiness, or any capital exposure.

With those caveats explicit:

**Primary (provisional): Option A — Phase 2l: Execute R3 first, then decide on R1a (sequential).**

Reasoning:

1. R3's smaller implementation surface (~5–7 source files) and lower fitting risk (sub-parameters anchored to existing project conventions) make the first execution phase cleaner — smaller H0-preservation test surface, easier Gate 2 review, easier to isolate bugs.
2. R3's sharper falsifiability (§10.3.c strict-dominance applies because the change is exit-philosophy-only) gives a high-info first result regardless of outcome — even a clean negative tells us "exit-philosophy redesign isn't the answer".
3. R3's outcome is informative input for R1a's planning. If R3 produces clean evidence in either direction, R1a's later phase can either (a) keep H0's exit logic if R3 was negative or (b) consider whether R1a's spec should be re-written against R3's exit if R3 was positive (this is a separate Phase 2j-equivalent, not a sweep).
4. Sequential execution is the same proven Phase 2g pattern. Each phase is a contained evidence step. Phase 2g's wave-1 had four variants in one phase but each was independently evaluated against H0; sequential phases extend that pattern.
5. The Phase 2j memo §H already arrived at this recommendation for the same reasons. Phase 2k validates it after the operator's brief explicitly required comparing alternatives.

**Secondary (fallback, provisional): Option B — Phase 2l: Implement both R1a and R3, run independently in one phase.**

Appropriate only if the operator wants both candidate results in parallel and accepts the larger code-change surface in a single phase. The fallback's reasoning: shared scaffolding lands once; comparison report covers both candidates; no sequential learning.

**Phase 4 stays deferred** per existing operator policy. Phase 2k does not propose advancing it.

## 19. What would change this recommendation

The recommendation is provisional. The following kinds of evidence or reasoning would justify switching paths:

### 19.1 Switch from Option A (sequential R3-first) to Option B (both in one phase)

- Operator preference for parallel evidence over sequential learning.
- Recognition that R3 and R1a are non-overlapping enough that simultaneous implementation does not increase contamination risk meaningfully.
- Project timeline pressure to evaluate both candidates faster.

### 19.2 Switch from Option A (R3-first) to a different sequential ordering (R1a-first)

- Operator preference for funnel-rejection-axis evidence first (the dominant 58% no-valid-setup is the largest single attrition source; R1a targets it).
- Recognition that R1a's evidence is more important to the strategic question (does the breakout family work at all?) than R3's exit-redesign evidence.

### 19.3 Switch from Option A to Option C (another docs phase)

- Phase 2k Gate 2 review surfaces a documentation inconsistency in R1a or R3 specs that requires correction.
- A new ambiguity surfaces during Phase 2k planning that affects R1a or R3 specs.
- Operator decides to refine the §11.3.5 threshold-application discipline before any execution.

### 19.4 Switch from Option A to Option D (fallback Wave 2 with H-D6)

- Phase 2h §3.3 / Phase 2i §3.4 / Phase 2j §I.4 switch conditions still apply unchanged.
- Operator reconsiders the structural-redesign vs. parameter-search tradeoff and prefers H-D6's parameter-search axis evidence first.

### 19.5 Switch from Option A to Option E (Phase 4)

- Explicit operator policy change accepting that operational infrastructure should be built without strategy-edge confirmation. Current policy is against this; this plan does not propose changing it.

### 19.6 Switch from Option A to "drop one candidate" (Phase 2i ≤ 2 cap deviation)

- Operator decides that R1a or R3 alone is the right scope for the project given new constraints (timeline, capital, scope) and authorizes Phase 2i ≤ 2 cap deviation. Phase 2k does not propose this.

---

## 20. Proposed files / directories to create or modify in Phase 2k

Phase 2k produces docs only:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-1-plan.md` — this plan, committed after Gate 1 approval (currently sitting as an untracked draft on `main` per the operator's branch-creation restriction).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-2-review.md` — pre-commit review.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2k-checkpoint-report.md` — checkpoint.

**No separate execution-planning memo.** This Gate 1 plan is the substantive planning artifact; no second memo is needed.

**No ambiguity-log changes anticipated.** If a real ambiguity surfaces during Gate 2 review, GAP-20260424-037 (next available identifier) would be appended; current expectation is no new GAP.

No other files touched. No `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `.claude/`, `data/`, or `technical-debt-register.md` edits.

## 21. No code / dependency changes

No source code changes. No tests added or modified. No new top-level packages. No new dependencies. No `pyproject.toml` or `uv.lock` change.

## 22. Output artifacts

- **Committed (to git, after Gate 2 approval):** Gate 1 plan (this file), Gate 2 review, checkpoint report.
- **Not committed:** none — Phase 2k produces no intermediate parquet, no run output, no notebook artifact, no code artifact.
- **Presented to operator / ChatGPT:** concise markdown summaries with tables. No screenshots.

## 23. Safety constraints

| Check | Requirement |
|---|---|
| Production Binance keys | none, not requested, not referenced |
| Exchange-write code | none |
| Credentials | none — no `.env`, no secrets in any artifact |
| `.mcp.json` | not created |
| Graphify | not enabled |
| MCP servers | not activated |
| Manual trading controls | none |
| Strategy logic edits | none |
| Risk engine edits | none |
| Data ingestion edits | none |
| Exchange adapter edits | none |
| Binance public URLs | none fetched |
| `.claude/settings.json` | preserved |
| Destructive git commands | none proposed |
| Changes outside working tree | none |
| New dependencies | none |
| `data/` commits | none |
| `technical-debt-register.md` edits | none (operator restriction) |
| Phase 4 work | none (operator restriction) |
| Phase 2l work | none (this phase proposes 2l, does not start it) |
| Fallback Wave 2 / H-D6 start | none (operator restriction) |
| Carry-forward expansion beyond R1a + R3 | none (Phase 2i ≤ 2 cap) |
| Wave-1 variant revival | none (operator restriction) |
| Sub-parameter sweeps disguised as structural changes | none (Phase 2j single committed values preserved) |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold changes | none |
| Re-derivation of wave-1 verdict | none — REJECT ALL preserved |
| Re-framing of Phase 2h / 2i / 2j recommendations | none — all are inputs |

## 24. Ambiguity / spec-gap items to log

**No new GAP anticipated.** Phase 2j Gate 2 review §2 confirmed no new GAP was needed; the §1.7 binding test plus existing thresholds plus per-candidate spec disciplines handled all judgements. Phase 2k inherits this state.

If during Phase 2k Gate 2 review a real ambiguity surfaces (e.g., a Phase 2j R1a or R3 spec corner case that materially affects implementation planning), the memo would record it inline OR append GAP-20260424-037 to `docs/00-meta/implementation-ambiguity-log.md`. Most likely no new GAP is needed.

## 25. Technical-debt register — no edits

`docs/12-roadmap/technical-debt-register.md` is NOT edited in Phase 2k. TD-016 (statistical live-performance thresholds) is informationally affected by future R1a / R3 execution results (any positive or negative result is direct evidence for TD-016) but the register itself stays untouched per operator restriction.

## 26. Proposed commit structure (end of Phase 2k)

Three commits on `phase-2k/redesign-execution-planning`, after two operator gate approvals (Gate 1 = this plan; Gate 2 = pre-commit review). Pytest runs before each commit and is expected at 396 passed (no code change anywhere).

1. `phase-2k: Gate 1 plan` — this file.
2. `phase-2k: Gate 2 review` — pre-commit review.
3. `phase-2k: checkpoint report` — phase closure.

If a new GAP is needed (unlikely), one additional commit would be inserted after commit 1: `phase-2k: ambiguity log append (GAP-20260424-037)`. Default is no GAP commit.

No `data/` commits. No `src/` or `tests/` commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## 27. Gate 2 review format (to be produced at end of 2k)

```
Phase: 2k — Structural Redesign Execution Planning
Scope confirmed against Gate 1 plan: yes / no + diffs
Docs written: list
Ambiguity-log appends: list (GAP IDs) — likely empty
Carry-forward discipline preserved: only R1a + R3; no third candidate
Sub-parameter values preserved as singular: R1a X=25, N=200; R3 R_TARGET=2.0, TIME_STOP_BARS=8
Execution-order analysis: 4 options compared (R3-first; R1a-first; both-in-one; one-only-other-deferred)
Recommended order: R3 first, then R1a (sequential)
Implementation-scope planning: per-candidate code-surface breakdown + minimal-implementation definition + H0 bit-for-bit preservation requirement
R3 forwarding notes preserved: same-bar STOP-over-TAKE_PROFIT priority; new ExitReason TAKE_PROFIT and TIME_STOP; same Phase 2f framework; §10.3.c additional path not framework rewrite
R1a execution notes preserved: 8-bar setup window remains; percentile predicate replaces only setup-validity; X=25/N=200 singular; warmup floor 221 bars explicit; funnel attribution interpretable
Report-contract planning: per-symbol artifacts + candidate-specific outputs + common diagnostics + comparison report layout + R/V separation
Validation framework restated: H0-only anchor; wave-1 historical-only; §10.3/§10.4/§11.3/§11.4/§11.6 unchanged; R/V split unchanged; GAP-036 fold convention unchanged; §11.3.5 no-loosening
Execution-readiness risks: per-candidate failure modes + stop-and-escalate triggers
Fallback relationships: when H-D6 supersedes; when Phase 4 stays deferred; when docs phase preferable
Five-option next-phase comparison: A (R3 sequential), B (both in one), C (docs phase), D (H-D6), E (Phase 4)
Recommendation: A primary (provisional); B fallback
"What would change this recommendation": 6 switch-condition blocks
Wave-1 result preserved: REJECT ALL stands
H0 anchor preserved: yes
Phase 2h / 2i / 2j recommendations preserved: all inputs, none re-framed
Threshold preservation: §10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged
§1.7.3 project-level locks preserved: yes
Disguised parameter sweeps avoided: yes
Safety posture: no code, no data, no APIs, no MCP, no Graphify, no TD-register edits
Operator restrictions honoured: yes
Test suite: pytest 396 passed (no code change expected)
Recommended next step: operator decides among Phase 2l Option A (recommended) / B (fallback) / C / D / E / drop one
Questions for operator: list or "none"
```

## 28. Checkpoint report format

Follows `.claude/rules/prometheus-phase-workflow.md` exactly: Phase, Goal, Summary, Files changed (all docs), Files created (all docs), Commands run (none safety-relevant — pytest + git status/diff), Installations performed (none), Configuration changed (none), Tests/checks passed (pytest 396 expected), Tests/checks failed (none), Known gaps (likely none new; pre-existing GAPs unchanged), Safety constraints verified (full table), Current runtime capability (research-only, unchanged), Exchange connectivity status (zero), Exchange-write capability (disabled), Recommended next step (proposal only — operator decides).

## 29. Approval gates

- **Gate 1 — this plan.** Pre-approved by the operator's "Approved to start Phase 2k planning only" message. The plan file is currently an untracked draft on `main`; the proposed branch `phase-2k/redesign-execution-planning` is created only after Gate 1 approval.
- **Gate 2 — pre-commit review.** After Gate 2 review + checkpoint report drafted, operator reviews diff + pytest output before any `git add` / `git commit`.

## 30. Post-approval execution sequence (docs-only)

After Gate 1 approval, proceed in this order and **stop before any `git add` / `git commit`**:

1. Verify branch state (working tree should show this Gate 1 plan as untracked; branch is `main`).
2. Create the working branch:
   ```
   git -C c:/Prometheus checkout -b phase-2k/redesign-execution-planning
   git -C c:/Prometheus status --short
   ```
3. The Gate 1 plan file is already at `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-1-plan.md` (sitting in the working tree from this drafting step); it follows the branch.
4. Draft Gate 2 review at `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-2-review.md` using the §27 format.
5. Stop. Show operator `git status`, `git diff --stat`, and `uv run pytest` output (expect 396 passed). Do not run `git add` / `git commit`. Await operator/ChatGPT Gate 2 review.

The Phase 2k checkpoint report (§28) is produced after Gate 2 approval, immediately before the commit sequence (§26).
