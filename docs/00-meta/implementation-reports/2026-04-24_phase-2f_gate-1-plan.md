# Phase 2f — Gate 1 Plan: Strategy Review, Variant Design, and Validation Planning

**Working directory:** `C:\Prometheus`
**Plan date:** 2026-04-24
**Branch:** `phase-2f/strategy-review-variant-design` (created from `main`)
**Scope:** Docs-only strategy-review / variant-design / validation-planning phase. No strategy code edits, no backtester code edits, no variant runs, no threshold tuning, no data downloads, no Binance/public URL calls, no MCP/Graphify, no `.mcp.json`, no Phase 4 work, no edits to `docs/12-roadmap/technical-debt-register.md`.

Gate 1 operator approval recorded 2026-04-24 with six conditions, all applied below.

---

## Context — why this phase, why now

Phase 2e produced the first real wide-range baseline for the locked v1 breakout strategy over 51 months of BTCUSDT + ETHUSDT 15m + 1h + mark-price + funding data (v002 manifests, zero invalid windows). The run used the Phase 3 locked defaults (`risk_fraction=0.0025`, `risk_usage=0.90`, `max_leverage=2.0`, `notional_cap=100_000`, `taker=0.0005`, `slippage=MEDIUM`, `adapter=FAKE`, `equity=10_000`) with no tuning and zero sensitivity variants, per operator Gate 1 condition.

Descriptive baseline result (not promotion evidence, not live-readiness):

| Symbol  | Trades | Win rate | Expectancy | Profit factor | Net PnL | Max DD | Long / Short | Exit mix                            |
|---------|-------:|---------:|-----------:|--------------:|--------:|-------:|-------------:|-------------------------------------|
| BTCUSDT |     41 |   29.27% |   −0.43 R  |          0.32 | −3.95%  | −4.23% |    21 / 20   | STOP 22, STAGNATION 19, TRAIL 0     |
| ETHUSDT |     47 |   23.40% |   −0.39 R  |          0.42 | −4.07%  | −4.89% |    18 / 29   | STOP 35, STAGNATION 11, TRAIL 1     |

Phase 2e signal-funnel bottlenecks (decision bars = 148,085 per symbol, accounting invariant verified):

| Rejection bucket        | BTCUSDT (% of bars) | ETHUSDT (% of bars) |
|-------------------------|---------------------:|---------------------:|
| No valid setup          |   85,480 (57.7%)     |   84,731 (57.2%)     |
| Neutral bias            |   54,541 (36.8%)     |   55,517 (37.5%)     |
| No close-break          |    7,443 (5.0%)      |    7,209 (4.9%)      |
| TR < ATR                |      216             |      173             |
| Close location          |      157             |      173             |
| Stop-distance filter    |      203             |      214             |
| ATR regime              |        4             |       21             |
| Sizing failed           |        0             |        0             |
| **Entry intents**       |     **41**           |     **47**           |

This baseline warrants a structured strategy-review phase because: (a) both symbols are net-negative with negative per-trade expectancy on a long real-data window, (b) trade frequency is ~1 trade / symbol / ~3 months, a property of the six-condition trigger + stop-distance band rather than a bug, (c) the Phase 2e Gate 2 review explicitly deferred sensitivity, walk-forward, and exit-model comparison to "a separate future phase" while forbidding threshold tuning in 2e, and (d) the strategy spec itself (`v1-breakout-strategy-spec.md` §Open Questions, lines 553–567) lists testable questions the baseline has not yet examined. Phase 2f addresses this deliberately — with a disciplined hypothesis list, anti-overfitting plan, and defined comparison framework — *before* any variant code runs.

---

## 1. Executive summary

Phase 2f is a **planning and review phase**, not an execution phase. Its work product is:

- a strategy-review memo (three clearly separated parts: observations / hypotheses / execution recommendations),
- a small disciplined hypothesis list (≤ 4 variants for wave 1),
- a variant-design taxonomy with one-change-at-a-time discipline,
- a comparison framework with pre-declared promotion / rejection thresholds,
- an anti-overfitting / validation plan (research window vs. validation window; walk-forward; no peeking; top-1–2 promotion),
- a trade-frequency sanity-check diagnostic (not a target),
- a scaffolding proposal for a future execution phase,
- six appended ambiguity-log GAP entries.

The Phase 2e locked baseline is the control and remains untouched. No thresholds are tuned in 2f; no variants are run in 2f.

## 2. Plain-English statement

In Phase 2e we built the real 51-month dataset and ran the locked v1 strategy as-is. It lost ~4% on both symbols with very few trades. Before changing anything, Phase 2f asks: *which filters are doing the rejecting, which of those are structural (cannot change in v1) vs. parametric (testable), and which small set of rule changes would be worth running next — with a comparison framework good enough that we can tell "better" from "lucky"?*

## 3. Branch and status verification commands

```
git -C c:/Prometheus status --short
git -C c:/Prometheus rev-parse --abbrev-ref HEAD
git -C c:/Prometheus fetch origin
git -C c:/Prometheus log --oneline -6
git -C c:/Prometheus checkout -b phase-2f/strategy-review-variant-design
```

Abort gate at start of phase: if working tree is not clean or branch is not `main`, stop and escalate.

## 4. Exact scope

- Review the Phase 2e baseline signal-funnel and trade-log artifacts (read-only; files under `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/`).
- Map each filter layer in the v1 spec (setup consolidation, HTF bias, breakout trigger, ATR regime, stop-distance band, close-positioning) to its Phase 2e rejection count and to its classification (structural vs. parametric).
- Produce a written strategy-review memo capturing findings, open questions from the spec, and doc/spec conflicts found during review.
- Propose a disciplined hypothesis list (≤ 4 variants for wave 1) with rationale, affected rule(s), expected impact, overfitting risk per hypothesis.
- Propose a variant taxonomy + naming convention.
- Propose a comparison framework (metrics, reporting cuts, signal-funnel diffs, cost/funding/slippage discipline, long/short split, exit-reason differences, "promising" vs "more trades but worse quality" definitions).
- Propose an anti-overfitting / validation plan (research/validation split over the 51-month window, walk-forward segmentation scheme, ETH-as-comparison rule, no-peeking discipline, top-1–2 promotion to validation).
- Propose a trade-frequency sanity-check with required diagnostics (diagnostic, not target).
- Propose a minimal experimental-execution design: how many variants in wave 1, one-change-at-a-time discipline, baseline-as-control, rule-relaxation-before-structure-change ordering.
- Propose the file/directory scaffolding for a future execution phase, without creating it in 2f.
- Log every ambiguity / spec-conflict found as a GAP-20260424-nnn entry in the existing ambiguity log.
- Produce a Gate 2 review format and checkpoint-report format.

## 5. Explicit non-goals (hard boundaries)

- No parameter tuning.
- No threshold sweeps.
- No running of variants, sensitivity, or walk-forward in 2f itself.
- No data download, no re-backfill, no new dataset versions.
- No Binance API calls (authenticated or public).
- No live-trading code, no exchange-write, no production keys.
- No MCP enablement, no `.mcp.json`, no Graphify indexing.
- No Phase 4 work (risk/state/persistence runtime).
- No changes to the Phase 2e baseline control artifacts.
- No edits to `docs/12-roadmap/technical-debt-register.md` (operator restriction).
- No `data/` commits.

## 6. Phase 2e baseline recap — the control

Authoritative descriptive numbers (quoted from `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md` and cross-checked against the Gate 2 review):

- Window: 2022-01-01 → 2026-04-01 UTC (51 months).
- Datasets: v002 manifests × 8, zero invalid windows, 204/204 SHA256 matches.
- BTCUSDT: 41 trades, WR 29.27%, expectancy −0.43 R, PF 0.32, net −3.95%, max DD −4.23%, L/S 21/20.
- ETHUSDT: 47 trades, WR 23.40%, expectancy −0.39 R, PF 0.42, net −4.07%, max DD −4.89%, L/S 18/29.
- Funnel dominant rejections (both symbols): `no valid setup` (~57–58%), `neutral bias` (~37%), `no close-break` (~5%); other filters each < 0.5%.
- Sizing never bound (0 rejections) at the Phase 3 defaults.
- Mark-price gap impact on held-position intervals: **zero** trades affected (BTC 0 / ETH 0) — baseline PnL/stops unaffected by 2022–2023 mark-price sparsity.

These numbers are the control against which any future variant is compared. Phase 2f does not modify them.

## 7. Strategy-review framework

### 7.1 Filter-layer inventory

Enumerate every filter with its exact rule and the Phase 2e rejection count attributed to it. The inventory is produced by cross-referencing `v1-breakout-strategy-spec.md` §§ Setup / HTF bias / Entry trigger / Stop distance / No-trade rules with the per-symbol `funnel_total.json` in the baseline run directory. No new code; this is a mapping exercise.

### 7.2 Restrictiveness ranking

Rank filters by rejection share. Phase 2e already tells us the order: (1) no valid setup ≫ (2) neutral bias ≫ (3) no close-break ≫ trailing filters. The memo records this ranking with exact percentages per symbol and flags that the setup filter alone eliminates ~58% of all decision bars.

### 7.3 Structural vs. parametric classification

Classify each filter per the spec's own language (§Decisions = structural; §Open Questions or §Comparison Matrix = parametric). This is the boundary that bounds which rules a variant may touch in a future execution phase.

| Layer                                     | Status           | Rationale anchor                                           |
|-------------------------------------------|------------------|------------------------------------------------------------|
| 15m signal / 1h bias TFs                  | Structural       | spec §Decisions                                            |
| Bar-close confirmation                    | Structural       | spec §Decisions; backtest-plan next-bar-open               |
| Structural stop formula                   | Structural       | spec line 259                                              |
| Exchange-side STOP_MARKET                 | Structural       | safety requirement                                         |
| One position, no pyramiding, no reversal while positioned | Structural | risk docs + spec §Operational Rules                 |
| Isolated margin, one-way mode             | Structural       | spec §Decisions                                            |
| Initial live risk 0.25%                   | Structural for comparison | risk-sizing; variants share to be comparable       |
| Max leverage 2x                           | Structural for comparison | exposure-limits                                    |
| Setup window length (8 bars)              | Parametric       | spec Open Q #1                                             |
| Setup range width (1.75 × ATR20)          | Parametric       | spec §Setup                                                |
| Net drift cap (0.35 × width)              | Parametric       | spec §Setup                                                |
| Breakout buffer (0.10 × ATR20)            | Parametric       | spec Open Q #2                                             |
| Breakout expansion (1.0 × ATR20)          | Parametric       | spec Open Q #3                                             |
| Close-location (top/bottom 25%)           | Parametric       | revisable                                                  |
| EMA pair (50/200)                         | Parametric       | spec Open Q #4                                             |
| EMA slope vs −3 bars                      | Parametric (ambiguous wording) | GAP-20260424-031                             |
| ATR regime (0.20% – 2.00%)                | Parametric       | spec Open Q #5                                             |
| Stop-distance band (0.60 – 1.80 × ATR20)  | Parametric       | implied sensitivity                                        |
| Stop buffer (0.10 × ATR20)                | Parametric       | backtest-plan matrix                                       |
| Stage-3 reduction (−0.25 R)               | Parametric       | spec Open Q #7                                             |
| Break-even threshold (+1.5 R)             | Parametric       | spec Open Q #8 — conflicts with fixed rule text (GAP-030)  |
| Trailing multiplier (2.5 × ATR20)         | Parametric       | spec Open Q #6                                             |
| Stage-6 tightening at +3 R                | Parametric       | spec §406–411 ("benchmarking decision")                    |
| Stagnation window (8 bars, +1 R gate)     | Parametric       | GAP-20260424-033                                           |

### 7.4 Trade-frequency is a diagnostic, not a target

More trades is not automatically better. A variant that doubles trade count while halving per-trade expectancy or tripling drawdown fails. A variant that preserves expectancy while increasing trade count and maintaining robustness is a candidate.

### 7.5 Trade-frequency sanity-check — diagnostic, not target (operator condition 2)

The strategy-review memo includes a dedicated section titled **"Trade-frequency sanity-check (diagnostic, not target)"** that defines how future variant reports assess whether trade flow is:

- **too sparse** — too few trades to evaluate edge; per-fold sample too low; long zero-trade stretches,
- **balanced** — steady enough frequency that per-fold signal is visible, without artificial inflation,
- **becoming too noisy / overtraded** — trade count rising while per-trade quality collapses (→ §10.4 rejection).

No fixed trade-count target is imposed. Future variant reports are **required** to include, per symbol:

- **Trades per month** — full distribution (min / median / max / per-month series).
- **Zero-trade months count** — separately for research and validation windows.
- **Median hold time** — median bars held per trade, with min/max.
- **Setup-to-entry conversion rate** — ratio of "valid 8-bar setups detected" to "entry intents produced."
- **Candidate-to-entry conversion rate** — ratio of "breakout candidates" (long + short) to "entry intents produced."

A variant is not rejected for any single frequency signal alone, but unusual combinations (e.g., setup-conversion 5× baseline with trade count unchanged) flag a likely implementation or spec problem that must be explained before the variant proceeds.

## 8. Hypothesis design menu (universe)

Final wave-1 selection is ≤ 4 of the below. Each hypothesis is a single-axis change.

**A. Setup-logic variants** (attack ~58% "no valid setup")
- H-A1 — *Window length*: test 6 / 10 / 12 bars vs. 8 (spec Open Q #1).
- H-A2 — *Range-width ceiling*: 2.00 × ATR20 vs. 1.75 × ATR20.
- H-A3 — *Drift cap*: 0.50 vs. 0.35 (weaker compression).

**B. Breakout-trigger variants**
- H-B1 — *Breakout buffer*: 0.05 / 0.15 × ATR20 vs. 0.10 (spec Open Q #2).
- H-B2 — *Expansion threshold*: 0.75 × ATR20 vs. 1.0 × ATR20 (spec Open Q #3).
- H-B3 — *Close-location*: top/bottom 35% vs. 25%.

**C. HTF-bias variants** (attack ~37% "neutral bias")
- H-C1 — *EMA pair*: 20/100 vs. 50/200 (spec Open Q #4).
- H-C2 — *Slope definition*: discrete EMA[now] > EMA[−3] vs. fitted slope (GAP-20260424-031).
- H-C3 — *Slope window*: 1 / 3 / 5 bars back.

**D. Stop / exit / trade-management variants** (at most one selected for wave 1)
- H-D1 — *Stop buffer*: 0.05 / 0.15 × ATR20 vs. 0.10.
- H-D2 — *Stop-distance band*: 0.50 – 2.20 × ATR20 (sensitivity only).
- H-D3 — *Break-even threshold*: +2.0 R vs. +1.5 R (spec Open Q #8; resolves GAP-030).
- H-D4 — *Trailing multiplier*: 2.0 / 3.0 × ATR20 vs. 2.5 (spec Open Q #6).
- H-D5 — *Stagnation window*: 6 / 10 / 12 bars vs. 8; +0.5 R vs. +1.0 R gate.
- H-D6 — *Exit-model bake-off*: fixed 2 R, fixed 3 R, staged+trailing, opposite-signal (deferred to a later wave per operator condition 3).

Per-hypothesis template (one page each in the memo):

```
Hypothesis ID:
Rule family:
Rationale:
Exact rule(s) changed (before → after, with spec line references):
Expected direction of trade count:
Expected direction of expectancy / PF / DD:
Overfitting risk (LOW / MEDIUM / HIGH) with justification:
Walk-forward scheme that will test it (per §11):
Pass criterion (per §10 comparison framework):
```

## 9. Variant-design rules

1. **One change at a time.** Each variant differs from H0 in exactly one parameter (or one coherent multi-parameter rule like an exit-model swap). Bundled variants forbidden.
2. **Wave-1 cap: ≤ 4 single-axis variants** (operator condition 1). Additional variants require a separate approval.
3. **Wave-1 family prioritization** (operator condition 3). Wave 1 must prioritize setup / trigger / HTF-bias families; at most **one** exit / trade-management variant in wave 1.
4. **Baseline is frozen.** Phase 2e run directory is the control — not re-run, not overwritten. Variant runs write to sibling `run_id` directories under a new `experiment_name`.
5. **Shared dataset version.** Every variant uses the same v002 manifests as baseline.
6. **Shared cost model.** Same taker/slippage/funding model as baseline unless the hypothesis is a cost-sensitivity test.
7. **No bundled tuning.** Variants scored in one pass; no re-running after peeking.
8. **Research vs. validation split enforced** (§11) before any variant result counts as "promising."

## 10. Comparison framework

### 10.1 Required metrics (per symbol, per variant, vs. baseline)

- Trade count (total, long, short).
- Win rate (total, long, short).
- Average winner (R and %), average loser (R and %).
- Expectancy (R/trade).
- Profit factor.
- Net PnL (USDT + % of sizing equity).
- Gross PnL + explicit fee / funding / slippage breakdown.
- Max drawdown (USDT + %).
- Longest losing streak.
- Exit-reason histogram (STOP / TRAILING / STAGNATION / END_OF_DATA).
- Signal-funnel bucket counts + percentages (accounting invariant required).
- Point-in-time rule conformity check.

### 10.2 Required reporting cuts

- Per-symbol.
- Per-year and per-month breakdown.
- Long vs. short split.
- Exit-reason split.
- Cost-sensitivity pass (LOW / MEDIUM / HIGH slippage) on every variant that clears the base pass.
- §7.5 trade-frequency diagnostics appendix.

### 10.3 "Promising enough to continue" — pre-declared operational definition

A variant is a **candidate** for validation if, vs. baseline, on the research window:

- expectancy improved by ≥ 0.10 R/trade **and** PF improved by ≥ 0.05, **or**
- expectancy unchanged or improved **and** trade count increased ≥ 50% **and** max DD not worse by > 1.0 pp, **or**
- the variant is an exit-model bake-off (H-D6, future wave) that strictly dominates baseline on both expectancy and max DD.

A variant is **disqualified** if any of: expectancy worsens, PF worsens, max DD > 1.5× baseline, any signal-funnel invariant breaks, or conformity check fails.

### 10.4 "More trades but worse quality" — explicit rejection rule

If trade count rises but expectancy falls below −0.50 R/trade or PF falls below 0.30, the variant is rejected regardless of sample size. This prevents rewarding variants that merely "unlock more trades."

### 10.5 Variant-comparison report format

A single `variant_comparison.md` + `variant_comparison.parquet` per wave, committed to `docs/00-meta/implementation-reports/` (markdown) with parquet row-level data kept in `data/derived/backtests/<experiment>/` (git-ignored). Baseline row included as row 0.

## 11. Anti-overfitting / validation plan

### 11.1 Window split

- **Research window (R):** 2022-01-01 → 2024-12-31 (36 months). Variants examined/ranked here.
- **Validation window (V):** 2025-01-01 → 2026-04-01 (15 months). Used only for the final surviving variants; not mined.
- **Holdout policy:** V is the holdout during 2f/2g wave 1. A true out-of-sample "holdout-holdout" is deferred to a later phase when live-forward data accumulates.

### 11.2 Walk-forward segmentation

On R (36 months), use five rolling folds of 12-month train / 6-month test, stepping 6 months (folds overlap on train but not on test). Each fold reports per-symbol metrics; robustness = consistency across folds. A variant that wins only one fold does not pass §10.3.

### 11.3 Validation discipline — no peeking, no re-ranking (operator condition 4)

- **Ranking happens only on R.** Candidates are ranked on research-window results alone.
- **Only the top 1–2 candidates proceed to validation (V).** No matter how many survive R, at most the top two are promoted to V.
- **Validation is not used to re-rank the full field.** V-window results on promoted candidates are pass/fail judgements against pre-declared §10.3/§10.4 thresholds, not a second beauty contest.
- **No iterative peeking loops.** Once a variant is measured on V, it is not re-run with adjusted parameters, re-scored, and re-promoted. A failure on V ends that variant's candidacy for this wave.
- **Pre-declared success thresholds.** §10.3 and §10.4 are committed **before** wave 1 runs. Operators cannot tighten/loosen them after seeing results.

### 11.4 ETH as a comparison, not a constraint

ETH results are reported and considered, but a variant is not required to improve on both symbols; it is required to **not catastrophically fail** on ETH. Explicit rule: a variant passes if BTC shows clear improvement and ETH does not degrade beyond §10.4 rejection thresholds. ETH-only wins are recorded but do not qualify a variant on BTC.

### 11.5 Avoiding regime-fit

Fold-consistency plus year/month breakdowns (§10.2) guard against regime-fit. The memo additionally requires per-variant commentary on whether improvement concentrates in one regime (e.g., 2022 bear / 2024–2025 trend) and how that should modulate operator confidence.

### 11.6 Cost sensitivity as a gate

Any variant that clears §10.3 on MEDIUM slippage must also be run on LOW and HIGH slippage. If HIGH slippage inverts the pass, the variant is demoted to "fragile" and does not proceed.

## 12. Proposed experiment design (first wave)

1. **H0 control** — already on disk; not re-run.
2. **Wave-1 cap: ≤ 4 single-axis hypotheses** (operator condition 1). Wave 1 prioritizes setup / trigger / HTF-bias families; at most one exit / trade-management variant (operator condition 3).

   Recommended allocation (subject to memo refinement):
   - **H-A1** — setup window length 10 bars (attacks ~58% "no valid setup").
   - **H-C1** — HTF EMA pair 20/100 (attacks ~37% "neutral bias").
   - **H-B2** — breakout expansion 0.75 × ATR20 (attacks 5% "no close-break" and TR<ATR).
   - **H-D3** — break-even at +2.0 R (the single allowed exit variant; resolves GAP-030).

3. **Rule-relaxation before structure change.** Structure-changing hypotheses (different setup concept, different bar-close semantics, intrabar logic) are deferred — they are v2 strategy work, not v1 variants.
4. **Strategy-review memo first, code second.** The memo is the Phase 2f deliverable; any code scaffolding is documentation-level only.
5. **Named variants, not a variant framework (yet).** First wave uses hard-coded named variants invoked from a runner script (mirroring `scripts/phase2e_baseline_backtest.py`). A generic variant-config framework is deferred.

## 12.A Strategy-review memo — required structure (operator condition 5)

The memo must present its content in three **clearly separated top-level sections**:

1. **Part 1 — Observations from the Phase 2e baseline.** Filter-layer inventory (§7.1), restrictiveness ranking (§7.2), structural vs. parametric classification (§7.3), trade-frequency sanity-check diagnostics from the baseline (§7.5). Pure description. No recommendations, no hypotheses.
2. **Part 2 — Proposed hypotheses.** The 4-hypothesis shortlist (per §12), each documented with the per-hypothesis template from §8. Hypothesis list only; no execution sequencing.
3. **Part 3 — Execution recommendations for the later variant phase.** How the wave would run (named variants, runner script), research/validation split enforcement (§11), anti-peeking discipline (§11.3), comparison report contents (§10 + §7.5 diagnostics), proposed commit boundary for the future phase, safety checklist for the future phase, conditions under which waves 2+ may be proposed.

Each part opens with a one-paragraph summary and closes cleanly before the next begins.

## 13. Proposed files / directories — created in a later execution phase, not in 2f

Phase 2f produces **docs only**:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-1-plan.md` — this plan.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_strategy-review-memo.md` — three-part memo.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-2-review.md` — pre-commit review.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2f-checkpoint-report.md` — phase checkpoint (written at end).
- `docs/00-meta/implementation-ambiguity-log.md` — append GAP-20260424-030..035 (append only).

Deferred to the next execution phase (**not created in 2f**):
- `scripts/phase2f_variant_wave1.py` — wave-1 runner.
- `src/prometheus/strategy/v1_breakout/variants/` — optional module for named variants.
- `src/prometheus/research/backtest/comparisons.py` — variant-vs-baseline report generator.
- `src/prometheus/research/validation/walk_forward.py` — walk-forward orchestration.

## 14. No code / dependency changes in 2f

No new runtime dependencies are needed for planning. No new top-level packages. No changes to `pyproject.toml` in 2f.

## 15. Output artifacts

- **Committed (to git, after Gate 2 approval):** Gate 1 plan, strategy-review memo, Gate 2 review, checkpoint report, ambiguity-log appends.
- **Not committed:** any intermediate analysis parquet; any per-variant run output (those live under `data/derived/backtests/` and are git-ignored).
- **Presented to operator / ChatGPT:** concise markdown summaries with tables. No screenshots. Numbers quoted exactly.

## 16. Ambiguities / spec-gap items to log

Appended to `docs/00-meta/implementation-ambiguity-log.md` (append only — no rewrite of existing entries; no edits to `technical-debt-register.md`):

| GAP ID              | Area     | Conflict                                                                                                  | Blocking                                                  |
|---------------------|----------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| GAP-20260424-030    | STRATEGY | Break-even rule text asserts +1.5 R (spec line 380) but spec Open Q #8 flags it as undecided.             | NON_BLOCKING                                              |
| GAP-20260424-031    | STRATEGY | EMA slope wording ("rising versus 3 completed 1h candles earlier") ambiguous between discrete comparison and fitted slope. | NON_BLOCKING for planning; PRE_DRY_RUN for implementation |
| GAP-20260424-032    | STRATEGY | Backtest uses trade-price stops by default; live uses MARK_PRICE stops. Mark-price sensitivity must be a required report cut. | NON_BLOCKING for 2f; PRE_PAPER_SHADOW for live readiness  |
| GAP-20260424-033    | STRATEGY | Stagnation window (8 bars, +1 R gate) is not listed in Open Questions but treated as a metric in the backtest plan — ambiguous about testability. | NON_BLOCKING                                              |
| GAP-20260424-034    | STRATEGY | "Previous 8 completed 15m candles" — off-by-one: does the setup exclude the breakout bar? Verify against implementation; record the convention in the memo. | NON_BLOCKING (verification, not redefinition)             |
| GAP-20260424-035    | STRATEGY | Sizing formula not written out in spec (§Sizing lines 317–323 describe the min() but not the per-factor formula). Document the actual formula used in `sizing.py`. | NON_BLOCKING                                              |

These GAPs are documentation-only and carry no live-readiness implication for 2f.

## 17. Technical-debt register — no edits

`docs/12-roadmap/technical-debt-register.md` is NOT edited in Phase 2f. Any items there that are affected by 2f findings (TD-016 statistical thresholds; TD-007 testnet vs. dry-run) are noted in the memo only; the register itself is unchanged until the operator lifts the restriction.

## 18. Proposed commit structure (end of Phase 2f)

Five commits on `phase-2f/strategy-review-variant-design`, after two operator gate approvals (Gate 1 = this plan; Gate 2 = pre-commit review). Every commit runs `uv run pytest` first and expects 387 passing.

1. `phase-2f: Gate 1 plan` — this file.
2. `phase-2f: strategy-review memo` — three-part memo.
3. `phase-2f: ambiguity log appends (GAP-030..035)`.
4. `phase-2f: Gate 2 review`.
5. `phase-2f: checkpoint report`.

No `data/` commits. No `src/` commits. No script commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator.

## 19. Gate 2 review format

```
Phase: 2f — Strategy Review, Variant Design, and Validation Planning
Scope confirmed against Gate 1 plan: yes / no + diffs
Docs written: list
Ambiguity-log appends: list (GAP IDs)
Filter inventory completeness check: mapping count matches §7.1 expected
Hypothesis list: count (target ≤ 4) + single-axis discipline confirmed
Validation plan: research/validation split recorded + walk-forward fold scheme recorded + no-peeking rules recorded
Comparison framework: metrics + cuts + promotion rules + rejection rules recorded + §7.5 diagnostics required
Baseline control preserved: yes (no edits to Phase 2e artifacts)
Safety posture: no code, no data, no APIs, no MCP, no Graphify, no TD-register edits
Operator restrictions honoured: yes
Test suite: pytest 387 passed (no code change expected)
Known gaps: GAP-030..035 recorded
Recommended next step: operator decision on Phase 2g (variant execution) vs. Phase 4 vs. Phase 2-data-follow-up
Questions for operator: list or "none"
```

## 20. Checkpoint report format

Follows `.claude/rules/prometheus-phase-workflow.md` exactly: Phase, Goal, Summary, Files changed (all docs), Files created (all docs), Commands run (pytest + git status/diff only), Installations performed (none), Configuration changed (none), Tests/checks passed (pytest 387 expected), Tests/checks failed (none), Known gaps (GAP-030..035), Safety constraints verified (full table), Current runtime capability (research-only, unchanged), Exchange connectivity status (zero), Exchange-write capability (disabled), Recommended next step (proposal only).

## 21. Safety checklist

| Check                                   | Requirement                                            |
|-----------------------------------------|--------------------------------------------------------|
| Production Binance keys                 | none                                                   |
| Exchange-write code                     | none                                                   |
| Credentials                             | none; no `.env`, no secrets                            |
| `.mcp.json`                             | not created                                            |
| Graphify                                | not enabled                                            |
| MCP servers                             | not activated                                          |
| Manual trading controls                 | none                                                   |
| Strategy logic edits                    | none in 2f                                             |
| Risk engine edits                       | none in 2f                                             |
| Data ingestion edits                    | none in 2f                                             |
| Exchange adapter edits                  | none in 2f                                             |
| Binance public URLs                     | none fetched                                           |
| `.claude/settings.json`                 | preserved                                              |
| Destructive git commands                | none proposed                                          |
| Changes outside working tree            | none                                                   |
| New dependencies                        | none                                                   |
| `data/` commits                         | none                                                   |
| `technical-debt-register.md` edits      | none (operator restriction)                            |
| Phase 4 work                            | none (operator restriction)                            |

## 22. Approval gates

- **Gate 1 — this plan.** Approved 2026-04-24 with six conditions (all applied).
- **Gate 2 — pre-commit review.** After memo + GAP appends + Gate 2 review + checkpoint report drafted, operator reviews diff + pytest output before any `git add` / `git commit`.

## 23. Gate 1 operator conditions applied (2026-04-24)

1. **Wave-1 cap ≤ 4** — §9 rule 2, §12 item 2.
2. **Trade-frequency sanity-check in memo** — §7.5 specifies required diagnostics.
3. **Wave-1 family prioritization** — §9 rule 3; §12 allocation (H-A1, H-C1, H-B2 + H-D3).
4. **Validation discipline** — §11.3 (rank on R only; top 1–2 to V; no re-rank; no peeking; pre-declared thresholds).
5. **Memo structure separation** — §12.A (Part 1 Observations / Part 2 Hypotheses / Part 3 Execution recommendations).
6. **Still-forbidden items re-affirmed** — §§ 5 and 21.

## 24. Post-approval execution sequence (docs-only)

1. Create the working branch (done: `phase-2f/strategy-review-variant-design`).
2. Write this Gate 1 plan to `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-1-plan.md`.
3. Draft the strategy-review memo at `docs/00-meta/implementation-reports/2026-04-24_phase-2f_strategy-review-memo.md` in the three-part structure from §12.A.
4. Append GAP-20260424-030..035 to `docs/00-meta/implementation-ambiguity-log.md`.
5. Draft Gate 2 review at `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-2-review.md` using the §19 format.
6. Stop. Show `git status`, `git diff --stat`, and `uv run pytest` output (expect 387 passed). Do **not** run `git add` / `git commit`. Await operator/ChatGPT Gate 2 review.

The Phase 2f checkpoint report (§20) is produced after Gate 2 approval, immediately before the commit sequence (§18).
