# Phase 2f — Strategy-Review Memo

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2f/strategy-review-variant-design`
**Author:** Claude Code (Phase 2f)
**Date:** 2026-04-24
**Scope:** Docs-only review of the locked v1 breakout strategy against the Phase 2e baseline, with a disciplined hypothesis shortlist and execution recommendations for a future variant-execution phase. No code edits, no runs, no tuning.

Memo structure (operator Gate 1 condition 5): three clearly separated parts —

- **Part 1** — Observations from the Phase 2e baseline (pure description).
- **Part 2** — Proposed hypotheses (shortlist only; no execution sequencing).
- **Part 3** — Execution recommendations for the later variant phase.

Each part opens with a one-paragraph summary and closes before the next begins. The structural / parametric classification is taken from the spec's own §Decisions vs. §Open Questions wording.

---

# Part 1 — Observations from the Phase 2e baseline

**Summary.** The Phase 2e baseline produced a 51-month (2022-01 → 2026-04), real-data, no-tuning run of the locked v1 breakout strategy on BTCUSDT and ETHUSDT, using Phase 3 locked defaults. Both symbols finished net-negative on per-trade expectancy with very few trades (~1 trade / symbol / ~3 months). The signal funnel shows the rejection mass is concentrated in three filters — `no valid setup` (~58% of decision bars), `neutral bias` (~37%), and `no close-break` (~5%) — while the trailing filters (ATR regime, close-location, stop-distance, sizing) together reject less than 0.5%. These findings are descriptive; they are the starting material for Part 2, not conclusions.

## 1.1 Baseline numbers (the control)

Source: `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md` (cross-checked against the Phase 2e Gate 2 review and the per-symbol `summary_metrics.json` in `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/`).

| Metric                          | BTCUSDT     | ETHUSDT     |
|---------------------------------|-------------|-------------|
| Trade count                     | 41          | 47          |
| Long / Short                    | 21 / 20     | 18 / 29     |
| Win rate (total)                | 29.27%      | 23.40%      |
| Expectancy (R/trade)            | −0.43       | −0.39       |
| Profit factor                   | 0.32        | 0.42        |
| Net PnL (USDT)                  | −394.87     | −407.31     |
| Net PnL (% of 10,000 equity)    | −3.95%      | −4.07%      |
| Max drawdown (USDT / %)         | −424.23 / −4.23% | −490.62 / −4.89% |
| Fees paid (entry + exit)        | 197.73      | 177.04      |
| Funding (net signed)            | −1.13       | +0.61       |
| Total time held (15m intervals) | 399         | 421         |
| Avg hold (bars)                 | ~9.73       | ~8.96       |
| Exit mix                        | STOP 22 / STAG 19 / TRAIL 0 | STOP 35 / STAG 11 / TRAIL 1 |
| Stop gap-through events         | 0           | 0           |

Worst years: BTC 2024 (−153.57 USDT on 8 trades); ETH 2023 (−263.91 USDT on 15 trades).

## 1.2 Signal-funnel rejection attribution

Source: per-symbol `funnel_total.json`. Both symbols evaluated 148,085 decision bars after warmup.

| Funnel stage / rejection bucket   | BTCUSDT        | ETHUSDT        |
|-----------------------------------|----------------|----------------|
| 15m bars loaded                   | 148,896        | 148,896        |
| 1h bars loaded                    | 37,224         | 37,224         |
| Decision bars evaluated           | 148,085        | 148,085        |
| Bias long                         | 48,280         | 44,744         |
| Bias short                        | 45,264         | 47,824         |
| Bias neutral (reject)             | **54,541 (36.8%)** | **55,517 (37.5%)** |
| Valid 8-bar setups detected       | 8,064          | 7,837          |
| Long breakout candidates          | 327            | 308            |
| Short breakout candidates         | 294            | 320            |
| Reject — no valid setup           | **85,480 (57.7%)** | **84,731 (57.2%)** |
| Reject — no close-break           | **7,443 (5.0%)** | **7,209 (4.9%)**  |
| Reject — TR < ATR                 | 216            | 173            |
| Reject — close-location           | 157            | 173            |
| Reject — ATR regime               | 4              | 21             |
| Reject — stop-distance            | 203            | 214            |
| Reject — sizing failed            | 0              | 0              |
| End-of-data (no fill)             | 0              | 0              |
| **Entry intents produced**        | **41**         | **47**         |

Accounting invariant (verified in both the baseline-summary and the Gate 2 review):
`bias_neutral + no_setup + no_close_break + TR<ATR + close_loc + ATR_regime + stop_dist + sizing + EOD + entries = decision_bars` — BTC 148,085 ✓, ETH 148,085 ✓.

## 1.3 Restrictiveness ranking

| Rank | Filter                  | BTCUSDT share | ETHUSDT share |
|-----:|-------------------------|---------------:|---------------:|
|    1 | No valid setup          |         57.7%  |         57.2%  |
|    2 | Neutral bias            |         36.8%  |         37.5%  |
|    3 | No close-break          |          5.0%  |          4.9%  |
|    4 | Stop-distance band      |          0.14% |          0.14% |
|    5 | TR < ATR                |          0.15% |          0.12% |
|    6 | Close-location          |          0.11% |          0.12% |
|    7 | ATR regime              |          0.003%|          0.014%|
|    8 | Sizing                  |          0.00% |          0.00% |

Rank 1–3 together eliminate ~99.5% of decision bars on both symbols. Ranks 4–8 combined reject ~0.5%. Sizing never bound, confirming the Phase 3 defaults were not the frequency constraint.

## 1.4 Structural vs. parametric classification

Classification by the spec's own language: items in `v1-breakout-strategy-spec.md` §Decisions are structural (the design decision itself is v1-locked; changing it constitutes a different strategy). Items in §Open Questions or the backtest plan's §Comparison Matrix are parametric (the value is a research default and explicitly revisable).

| Layer                                                          | Status                     | Rationale anchor                                       |
|----------------------------------------------------------------|----------------------------|--------------------------------------------------------|
| 15m signal / 1h bias timeframes                                | Structural                 | spec §Decisions                                        |
| Bar-close confirmation (no intrabar)                           | Structural                 | spec §Decisions; backtest-plan §Baseline fill          |
| Structural stop formula (min/max ± buffer)                     | Structural                 | spec §Stop (line 259)                                  |
| Exchange-side `STOP_MARKET`, `closePosition=true`, `MARK_PRICE` | Structural                 | spec §Protective Stop; safety docs                     |
| One position, no pyramiding, no reversal while positioned      | Structural                 | risk-docs + spec §Operational Rules                    |
| Isolated margin, one-way mode                                  | Structural                 | spec §Decisions                                        |
| Initial live risk 0.25%                                        | Structural for comparison  | shared baseline so variants are comparable             |
| Max leverage 2×                                                | Structural for comparison  | exposure-limits; shared baseline                       |
| Setup window length (8 bars)                                   | Parametric                 | spec Open Q #1                                         |
| Setup range width (1.75 × ATR20)                               | Parametric                 | spec §Setup (research default)                         |
| Net drift cap (0.35 × width)                                   | Parametric                 | spec §Setup (research default)                         |
| Breakout buffer (0.10 × ATR20)                                 | Parametric                 | spec Open Q #2; backtest-plan matrix                   |
| Breakout expansion (1.0 × ATR20)                               | Parametric                 | spec Open Q #3                                         |
| Close-location (top/bottom 25%)                                | Parametric                 | not in Open Qs but phrased as research default         |
| EMA pair (50 / 200)                                            | Parametric                 | spec Open Q #4; backtest-plan matrix                   |
| EMA slope definition                                           | Parametric + ambiguous     | GAP-20260424-031                                       |
| ATR regime (0.20% – 2.00%)                                     | Parametric                 | spec Open Q #5                                         |
| Stop-distance band (0.60 – 1.80 × ATR20)                       | Parametric                 | implied sensitivity                                    |
| Stop buffer (0.10 × ATR20)                                     | Parametric                 | backtest-plan matrix                                   |
| Stage-3 reduction (−0.25 R)                                    | Parametric                 | spec Open Q #7                                         |
| Break-even threshold (+1.5 R)                                  | Parametric; rule-text conflict | GAP-20260424-030 (spec line 380 vs. Open Q #8)     |
| Trailing multiplier (2.5 × ATR20)                              | Parametric                 | spec Open Q #6                                         |
| Stage-6 tightening at +3 R                                     | Parametric                 | spec §406–411 "benchmarking decision, not locked"      |
| Stagnation window (8 bars, +1.0 R gate)                        | Parametric                 | GAP-20260424-033                                       |

## 1.5 Implementation-verified conventions (documentation, not changes)

Two GAPs are verification-only. The implementation already encodes a clear convention; this memo records it so Part 2 hypotheses and Part 3 execution recommendations do not accidentally redefine it.

### GAP-20260424-034 — "previous 8 completed 15m candles" convention

`src/prometheus/strategy/v1_breakout/setup.py` lines 3–12 and 31–35 state the convention explicitly:

> "Use the previous 8 completed 15m candles. … The setup window is keyed by the first bar's open_time. The 'current' bar (breakout candidate) is NOT part of the window."

The docstring of `detect_setup(prior_8_15m_bars, atr_20_15m)` adds:

> "These are the 8 bars STRICTLY BEFORE the breakout candidate bar. `atr_20_15m` is the 15m ATR(20) value evaluated at the close of the LAST bar in the window (i.e., at position [-1]; NOT the breakout bar)."

Convention adopted by Phase 2f: the setup window is `[N−8 .. N−1]` when `N` is the breakout bar. Any hypothesis that varies window length (H-A1) applies the same "strictly-before" convention (e.g., `[N−10 .. N−1]` for a 10-bar window). No redefinition is proposed.

### GAP-20260424-035 — sizing formula, fully specified

`src/prometheus/research/backtest/sizing.py` lines 1–19 define the pipeline:

```
1.  risk_amount       = sizing_equity * risk_fraction
2.  risk_budget       = risk_amount * risk_usage_fraction
3.  raw_qty           = risk_budget / stop_distance
4.  leverage_cap_qty  = (sizing_equity * max_effective_leverage) / reference_price
5.  notional_cap_qty  = max_notional_internal / reference_price
6.  candidate_qty     = min(raw_qty, leverage_cap_qty, notional_cap_qty)
7.  Floor candidate_qty to LOT_SIZE.stepSize (ROUND_FLOOR, never nearest)
8.  If final_qty < LOT_SIZE.minQty          -> BELOW_MINQTY (reject)
9.  If final_qty * ref_price < MIN_NOTIONAL -> BELOW_MIN_NOTIONAL (reject)
10. Emit sizing_limited_by label: STOP_RISK | MAX_EFFECTIVE_LEVERAGE | INTERNAL_NOTIONAL_CAP | STEP_SIZE_FLOOR
```

At Phase 3 locked defaults (`equity=10_000`, `risk_fraction=0.0025`, `risk_usage=0.90`): `risk_amount = 25 USDT`, `risk_budget = 22.50 USDT`. Phase 2e reported zero sizing rejections, consistent with this pipeline being non-binding at baseline on BTC/ETH at 10 k equity. No code change is proposed; this is documentation only.

## 1.6 Trade-frequency sanity-check (diagnostic, not target)

Per operator Gate 1 condition 2, every future variant report must include the five diagnostics below per symbol. They are diagnostics, not a promotion target. A variant is not rejected by any single frequency signal; unusual combinations (e.g., setup-conversion 5× baseline with trade count unchanged) flag a likely implementation or spec problem that must be explained *before* the variant proceeds.

**Diagnostic definitions:**

- **Trades per month distribution** — the full per-month count series over the 51-month window, aggregated into min / median / max / mean (source: `trade_log.json → trades[*].entry_fill_time_ms`, bucketed by UTC year-month against the 51-month full grid with zero-trade months included).
- **Zero-trade months count** — number of calendar months with zero entries, reported over the full 51-month window and separately for the research window R (2022-01 → 2024-12, 36 months) and the validation window V (2025-01 → 2026-03, 15 months).
- **Hold time** — bars held per trade taken directly from `trade_log.json → trades[*].bars_in_trade`, reported as min / median / max / mean (15m bars).
- **Setup-to-entry conversion rate** — `entry_intents_produced / valid_setup_windows_detected` (both from `funnel_total.json`).
- **Candidate-to-entry conversion rate** — `entry_intents_produced / (long_breakout_candidates + short_breakout_candidates)` (from `funnel_total.json`).

**Baseline diagnostic snapshot — exact values recomputed from `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/<SYMBOL>/{trade_log.json, funnel_total.json}`:**

| Diagnostic                                              | BTCUSDT             | ETHUSDT             |
|---------------------------------------------------------|---------------------|---------------------|
| Trades per month — min                                  | 0                   | 0                   |
| Trades per month — median                               | 1                   | 1                   |
| Trades per month — max                                  | 5                   | 4                   |
| Trades per month — mean (average)                       | 0.8039              | 0.9216              |
| Zero-trade months — full 51-month window                | 23 / 51             | 20 / 51             |
| Zero-trade months — research window R (2022-01 → 2024-12) | 13 / 36           | 14 / 36             |
| Zero-trade months — validation window V (2025-01 → 2026-03) | 10 / 15         | 6 / 15              |
| Hold time — min (15m bars)                              | 0                   | 0                   |
| Hold time — median (15m bars)                           | 8                   | 7                   |
| Hold time — max (15m bars)                              | 38                  | 40                  |
| Hold time — mean (average, 15m bars)                    | 8.2439              | 7.2340              |
| Setup-to-entry conversion rate                          | 41 / 8,064 = 0.5084% | 47 / 7,837 = 0.5997% |
| Candidate-to-entry conversion rate                      | 41 / 621 = 6.6023%   | 47 / 628 = 7.4841%   |

Notes on the diagnostics:

- Both symbols show `bars_in_trade = 0` as the minimum hold time, meaning at least one trade on each symbol exited on the fill bar itself (effectively entry and exit on the same 15m completed bar per the backtester's conservative fill model). This is a low-count tail, not a pervasive pattern — the median sits at 8 (BTC) and 7 (ETH), and the mean is ~8 for both.
- Zero-trade months are noticeably more concentrated in the validation window V for BTC (10 of 15 months = 66.7%) than in the research window R (13 of 36 = 36.1%); for ETH the pattern is reversed (V: 6/15 = 40.0%; R: 14/36 = 38.9%). This is raw data, not an analysis — the memo records it so future variant reports can be compared against it.
- The setup-to-entry and candidate-to-entry ratios come directly from the funnel JSON and need no recomputation; they are quoted to four decimals so wave-1 reports can compare against them without rounding ambiguity.

Interpretation framing for future variants:

- **Too sparse** — if a variant's trades-per-month median stays at or below baseline with long zero-trade stretches, per-fold walk-forward statistics become unreliable; the variant fails §10.3 on sample-size grounds regardless of expectancy.
- **Balanced** — trades-per-month median roughly 2–5× baseline with expectancy stable or better; no single fold carries > 60% of total PnL.
- **Becoming too noisy** — trades rise substantially while expectancy falls below −0.50 R or PF below 0.30; §10.4 rejection applies regardless of sample size.

These definitions do **not** impose a fixed target; they set the framing for how frequency is interpreted alongside quality in Part 3.

## 1.7 Baseline control protection

The Phase 2e artifacts under `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/` are the control. Phase 2f does not re-run them, does not overwrite them, does not re-ingest their inputs. All variant runs in the future execution phase write to sibling `run_id` directories under a new `experiment_name` (e.g., `phase-2g-wave1-variant-HA1`), keeping the baseline row as row 0 of every comparison report.

---

# Part 2 — Proposed hypotheses

**Summary.** Wave 1 is capped at **four single-axis hypotheses** (operator Gate 1 condition 1). Three address the dominant Phase 2e rejection buckets (no-valid-setup, neutral-bias, no-close-break); one is the single allowed exit / trade-management variant (Gate 1 condition 3). Each hypothesis is a one-change-at-a-time modification of H0 with the rest of the strategy frozen. No bundled variants. No threshold sweeps beyond the single-value alternative specified. All four share the Phase 3 locked cost model, the v002 datasets, the locked risk/leverage frame, and the pre-declared §10.3/§10.4 promotion/rejection thresholds from the Gate 1 plan.

## H0 — Baseline (control; not run in 2f, not re-run in 2g)

- Identifier: `baseline-H0`.
- Source: `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/` (run_id = 2026-04-20T23-58-39Z).
- Row 0 of every variant-comparison report.
- No changes. Included for reference in every diff.

## H-A1 — Setup window length: 10 bars vs. 8

**Hypothesis ID:** `H-A1`
**Rule family:** A — setup-logic variants
**Spec anchor:** Open Question #1 (line 557 of `v1-breakout-strategy-spec.md`).

**Rationale.** `No valid setup` is the single largest rejection (~58% of decision bars on both symbols). A longer window lets mild mid-window pullbacks average into the range-width / drift-ratio checks, which should increase the share of bars that produce a valid setup. Baseline eliminated 85,480 (BTC) and 84,731 (ETH) decision bars on this filter alone; even a 20–30% loosening of that share adds meaningfully to candidate flow *before* any trigger filter applies.

**Exact rule change (before → after).**
- Before: `SETUP_SIZE = 8` in `src/prometheus/strategy/v1_breakout/setup.py:22`.
- After: `SETUP_SIZE = 10` (same "previous N completed 15m candles, strictly before the breakout bar" convention per GAP-034 verification in §1.5).
- Range-width cap `1.75 × ATR(20)` unchanged. Drift ratio `0.35 × width` unchanged. ATR(20) context bar unchanged (still the last bar of the window).

**Expected direction of trade count.** Up. Magnitude not predicted.

**Expected direction of expectancy / PF / DD.** Expectancy direction: uncertain — a longer window may admit setups whose range is less truly compressed, which can reduce follow-through after the breakout; PF may compress toward 1.0 if the added candidates are lower quality. Max DD: expected mildly worse if PF degrades.

**Overfitting risk.** MEDIUM. Window length is a discrete parameter with only a few operationally meaningful values (6/8/10/12); the scan is narrow and Open Q #1 pre-commits the test set. Risk is mitigated by the §11.2 walk-forward folds and the §11.3 top-1–2 discipline.

**Walk-forward scheme.** Five rolling folds on R (2022-01 → 2024-12), 12-month train / 6-month test, 6-month step. Fold-consistency (sign of expectancy across folds, no single fold carrying > 60% of PnL) required to pass §10.3.

**Pass criterion.** §10.3.a (expectancy ≥ +0.10 R improvement **and** PF ≥ +0.05) **or** §10.3.b (expectancy not worse **and** trade count +≥50% **and** DD not worse by > 1.0 pp). §10.4 rejection applies if expectancy drops below −0.50 R or PF below 0.30. Cost-sensitivity gate on LOW/HIGH slippage required before promotion to V.

## H-C1 — HTF bias EMA pair: 20 / 100 vs. 50 / 200

**Hypothesis ID:** `H-C1`
**Rule family:** C — HTF-bias variants
**Spec anchor:** Open Question #4 (line 560) and backtest-plan Comparison Matrix (lines 283–320).

**Rationale.** `Neutral bias` is the second-largest rejection (~37% of decision bars). The 50/200 pair is a slow regime filter that spends extended stretches neutral. A faster pair (20/100) shifts sides more often and is neutral less often; this directly increases eligible decision bars. The hypothesis tests whether the locked slow-bias assumption is the dominant contributor to bias-neutrality — and whether a faster bias either (a) preserves expectancy with more trades (a clean win), (b) adds trades with degraded quality (rejected per §10.4), or (c) makes no material difference (failed hypothesis; keep baseline).

**Exact rule change (before → after).**
- Before: 1h `EMA(50)` vs `EMA(200)` on completed 1h bars (spec lines 156–160, 164–168).
- After: 1h `EMA(20)` vs `EMA(100)` on completed 1h bars.
- Slope rule preserved literally (GAP-031 still open and flagged); slope window preserved at "versus 3 completed 1h candles earlier." Bias classification logic unchanged. Only the EMA periods change.

**Expected direction of trade count.** Up, plausibly ~1.3–1.7× baseline. Magnitude dominated by how often 20/100 is neutral vs. 50/200.

**Expected direction of expectancy / PF / DD.** Expectancy direction: uncertain — a faster bias more often aligns with the breakout but also more often flips direction mid-trend, admitting false-breakout setups. PF may improve or degrade. Max DD: expected similar or modestly worse.

**Overfitting risk.** LOW–MEDIUM. The 20/100 pair is a conventional faster-regime filter listed explicitly in the backtest plan's Comparison Matrix; this is not a fit-to-noise search but a pre-declared alternative. Risk is further reduced because §11.3 permits only top-1–2 promotion to V.

**Walk-forward scheme.** As H-A1.

**Pass criterion.** As H-A1. In addition: BTC must not degrade below §10.4 thresholds; ETH-only improvements are recorded but do not qualify H-C1 on BTC (§11.4).

**Open dependency.** GAP-20260424-031 (EMA slope wording). The memo treats "rising versus 3 completed 1h candles earlier" as a **discrete comparison** (`EMA[t] > EMA[t−3_hours_completed]`) per the implementation convention; any switch to a fitted slope is out of scope for wave 1 and would be a separate GAP-031 resolution and separate hypothesis.

## H-B2 — Breakout expansion: 0.75 × ATR(20) vs. 1.0 × ATR(20)

**Hypothesis ID:** `H-B2`
**Rule family:** B — breakout-trigger variants
**Spec anchor:** Open Question #3 (line 559) and backtest-plan matrix.

**Rationale.** `No close-break` (~5%) and `TR < ATR` (~0.15%) together filter out breakout candidates whose bar range is too small. The 1.0 × ATR(20) expansion gate is the primary gate among these; relaxing it to 0.75 × ATR(20) admits a controlled set of smaller-expansion breakouts. Combined with the much larger `no valid setup` bottleneck upstream, this is the most targeted way to test whether the trigger's strictness — not just the setup filter — is over-fitted to a "strong expansion or nothing" shape.

**Exact rule change (before → after).**
- Before: breakout-bar `true_range >= 1.0 × ATR(20)` (spec lines 207 and 219 for long/short symmetric).
- After: `true_range >= 0.75 × ATR(20)`.
- All other trigger conditions unchanged: close-break by 0.10 × ATR20 buffer, close-location (top/bottom 25% of bar range), ATR-regime bounds (0.20% – 2.00%), 1h bias alignment.
- Stop calculation unchanged.

**Expected direction of trade count.** Up, modest. Most of the bars this change could unlock are still gated by the setup filter upstream.

**Expected direction of expectancy / PF / DD.** Expectancy direction: down (weaker expansion historically has lower follow-through); PF likely compressed toward 1.0. Max DD: plausibly slightly worse. This hypothesis is in wave 1 not because we expect it to win but because we need to *measure* how severely expectancy degrades as the trigger is loosened — that answer directly informs whether the trigger's strictness is well-calibrated or over-tight.

**Overfitting risk.** LOW. Single parameter, two discrete values, pre-declared in Open Q #3.

**Walk-forward scheme.** As H-A1.

**Pass criterion.** As H-A1. Given the expected direction, H-B2 is more likely to be rejected by §10.4 than to clear §10.3 — and that outcome *is* informative. If H-B2 is rejected while H-A1 or H-C1 pass, the picture that emerges is "setup / bias were too restrictive; trigger strictness was appropriate." If H-B2 unexpectedly passes, that is a stronger signal about the trigger than about the setup.

## H-D3 — Break-even threshold: +2.0 R vs. +1.5 R

**Hypothesis ID:** `H-D3`
**Rule family:** D — stop / exit / trade-management variants (the one allowed variant per Gate 1 condition 3)
**Spec anchor:** Open Question #8 (line 564); resolves GAP-20260424-030 (spec rule-text vs. Open Q internal conflict).

**Rationale.** Baseline exits are dominated by STOP (BTC 22 of 41, ETH 35 of 47) and STAGNATION (BTC 19, ETH 11). TRAIL exits are 0 (BTC) and 1 (ETH) in the entire 51-month window. The Stage-3 → Stage-4 transition at MFE = +1.5 R moves the stop to break-even early — and the baseline never reaches +2.0 R MFE often enough to engage the trailing stage (Stage 5). A later break-even threshold gives winning trades more room to move into the trailing zone before the stop is tightened to break-even; if the underlying edge exists but is being cut short by early break-even, this hypothesis will detect it. This is the one exit variant in wave 1; the larger exit-model bake-off (H-D6) is deferred per condition 3.

**Exact rule change (before → after).**
- Before: Stage 4 triggers at `MFE ≥ +1.5 R` — stop moved to break-even (spec line 380).
- After: Stage 4 triggers at `MFE ≥ +2.0 R` — stop moved to break-even.
- Stage 3 (−0.25 R at `MFE ≥ +1.0 R`) unchanged. Stage 5 (trailing at `MFE ≥ +2.0 R` using 2.5 × ATR20) unchanged — meaning under H-D3, Stage 4 and Stage 5 coincide at the same MFE trigger, which is operationally equivalent to "skip explicit break-even and go straight to trailing at +2.0 R MFE." The memo records this equivalence as the intended semantics of H-D3.
- Stop-widening prohibition unchanged. Initial stop formula unchanged. Stagnation rule unchanged.

**Expected direction of trade count.** Unchanged (entries/exits preserved; only the intra-trade stop trajectory differs).

**Expected direction of expectancy / PF / DD.** Expectancy direction: expected up *if* the baseline is being cut short at break-even on modest winners that would otherwise reach trailing. PF: expected up similarly. Max DD: potentially slightly worse (break-even protection kicks in later, so a trade that retraces after +1.5 R can now fall further before the stop tightens).

**Overfitting risk.** LOW. Single parameter, two pre-declared values, direct resolution of a spec-internal conflict (GAP-030).

**Walk-forward scheme.** As H-A1.

**Pass criterion.** §10.3.a or §10.3.c (exit-model-style strict dominance on expectancy and DD). §10.4 rejection applies normally. Because this is the only exit variant in wave 1, special attention required to make sure the improvement is not a single-fold artifact; fold-consistency is weighted heavily in interpreting results.

## Why these four and no others in wave 1

- **H-A1, H-C1, H-B2** attack the three dominant rejection buckets in descending order (58% → 37% → 5%), satisfying Gate 1 condition 3's setup / trigger / bias prioritization.
- **H-D3** is the one exit / management variant (condition 3 cap) and doubles as a formal resolution of GAP-030.
- **H-A2, H-A3, H-B1, H-B3, H-C2, H-C3, H-D1, H-D2, H-D4, H-D5, H-D6** remain in the hypothesis menu but are deferred. Wave-2 candidacy for them depends on wave-1 results and an explicit separate approval per operator condition 1.
- **No bundled variants** (e.g., "H-A1 + H-C1 together"). Once single-axis signals are observed, a future wave may propose a carefully justified bundled variant; wave 1 must not conflate axes.

---

# Part 3 — Execution recommendations for the later variant phase

**Summary.** The execution phase that runs wave 1 (provisionally "Phase 2g") is docs-only-bounded until it begins. This Part describes how it should run: a hard-coded named-variant runner script, the research / validation window split with strict top-1–2 promotion and no peeking, a comparison-report contract that includes the §7.5 diagnostics as a mandatory appendix, a commit structure that keeps variant code and variant results cleanly separable from documentation, and a pre-declared safety checklist. No code is written in Phase 2f. Nothing in Part 3 should be read as a commitment to run wave 1; a separate Gate 1 plan for the execution phase is required.

## 3.1 How wave 1 is run

- **Runner.** One script, `scripts/phase2g_variant_wave1.py` (or equivalent name chosen at that phase's Gate 1). Mirror the structure of `scripts/phase2e_baseline_backtest.py` — load the same v002 datasets, apply the same cost model, write results to `data/derived/backtests/phase-2g-wave1/<run_id>/<variant_id>/<SYMBOL>/`. One variant per invocation.
- **Named variants, not a framework.** The four variants are hard-coded as named parameter sets. No generic "variant config" class or dataclass is introduced in wave 1 — premature abstraction with only four candidates.
- **Variant-scoped strategy code.** If `H-A1` or `H-B2` require parameter-passing into `setup.py` / `trigger.py`, add thin `variant_*` keyword parameters that default to baseline values. H0 is reproducible bit-for-bit without the new flags.
- **H-C1 implementation path.** The EMA period is read from a `BiasConfig` constant. Either (a) add a variant-scoped override, or (b) the runner script monkey-patches the constant in its own process; operator + ChatGPT choose in that phase's Gate 1 plan.
- **H-D3 implementation path.** The Stage-4 threshold lives in the management-logic module. The runner passes a `break_even_r` scalar defaulting to 1.5 through to the management logic; H-D3 sets it to 2.0.
- **Determinism.** Same seed / same ordering / no non-deterministic operations. The existing backtest engine is already deterministic; no changes required.
- **Dataset pinning.** All runs cite the same v002 manifest SHA256s. The variant report records the manifests alongside the run_id.

## 3.2 Research / validation split and walk-forward

- **R window:** 2022-01-01 → 2024-12-31 (36 months).
- **V window:** 2025-01-01 → 2026-04-01 (15 months).
- **Walk-forward on R:** five rolling folds of 12-month train / 6-month test, stepping 6 months. Each fold's per-symbol metrics are reported; robustness = consistency across folds (sign of expectancy, PF > 1 contribution pattern, DD shape).
- **Full-window R pass:** used alongside per-fold consistency for the §10.3 judgement.
- **V policy:**
  - V is untouched during R-ranking.
  - Only the top 1–2 R-surviving variants are run on V.
  - V results are pass / fail against §10.3 / §10.4 thresholds *declared before any runs*.
  - A variant that fails V is dropped; no re-running with adjusted parameters.
  - V is not used to re-rank the R leaderboard.
  - No iterative peeking loops.

## 3.3 Comparison report contract

Each variant in the wave produces:

1. A standard `backtest_report.manifest.json` with run_id, dataset versions, config snapshot, and accepted-limitations.
2. Per-symbol `summary_metrics.json`, `trade_log.parquet`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `funnel_total.json`, `monthly_breakdown.parquet`, `yearly_breakdown.parquet` — same layout as the baseline.
3. Fold-level metrics for each of the five walk-forward folds (both symbols).
4. The §7.5 trade-frequency sanity-check appendix, computed directly from the trade_log + funnel_total.

The wave produces a single aggregated `phase-2g_wave1_variant_comparison.md` (committed) and `phase-2g_wave1_variant_comparison.parquet` (git-ignored under `data/derived/backtests/`). The markdown report:

- Row 0 = H0 (baseline).
- Rows 1–4 = H-A1, H-C1, H-B2, H-D3 (full-window R).
- Per-fold tables attached.
- Promotion / rejection classification table per §10.3 / §10.4.
- Cost-sensitivity section (LOW / HIGH slippage) for every variant that clears the §10.3 base pass.
- §7.5 diagnostics appendix per variant and per symbol.
- Top-1–2 V-window results appended only after R-ranking is final.

## 3.4 Commit boundary for the execution phase

The execution phase is proposed to commit in this order (subject to its own Gate 1 plan):

1. Phase 2g Gate 1 plan.
2. Variant runner + minimal code changes (thin `variant_*` overrides in strategy modules; tests preserve H0 bit-for-bit).
3. Wave-1 R-window results + comparison markdown (no V results yet).
4. Top-1–2 promotion decision record.
5. V-window results on the promoted candidates.
6. Phase 2g Gate 2 review.
7. Phase 2g checkpoint report.

`data/` artifacts remain git-ignored. `scripts/` and strategy-module code changes are the only non-doc commits.

## 3.5 Safety checklist for the execution phase

| Check | Requirement |
|---|---|
| Production Binance keys | none |
| Exchange-write code | none |
| Credentials | none — no `.env`, no secrets in any artifact |
| `.mcp.json` | not created |
| Graphify | not enabled |
| MCP servers | not activated |
| Strategy structural changes | none — only Parametric-classified parameters modified |
| Risk-framework changes | none — same `risk_fraction`, `max_leverage`, `notional_cap` as baseline |
| Dataset changes | none — same v002 manifests as baseline |
| Cost-model changes | none except the explicit LOW/HIGH slippage sensitivity; no tuning of fee/funding |
| Baseline artifacts | untouched; Phase 2e run_id directory read-only |
| Binance public URLs | none fetched |
| New dependencies | none anticipated; if any become necessary, add via a separate dependency-only commit |
| `data/` commits | none |
| `technical-debt-register.md` edits | none unless operator lifts the 2f restriction |
| Phase 4 work | none — still deferred |

## 3.6 When may waves 2+ be proposed?

Wave 2 is *not* implicit. It requires a fresh operator approval and is conditional on:

- wave-1 R-window results being reviewed in full (both symbols, fold-by-fold),
- any winning variant having been validated on V or explicitly rejected,
- the §7.5 trade-frequency diagnostics having been inspected,
- no implementation surprises (e.g., unexpected funnel-invariant violations, unexpected H0 divergence, unexpected fold-concentration of PnL),
- a specific, pre-declared wave-2 hypothesis list (again ≤ 4, still single-axis, still prioritizing whichever bottleneck remains after wave 1).

Candidate wave-2 hypotheses from the menu in Part 2's universe (not an endorsement; a record): H-A2 (range-width ceiling), H-A3 (drift cap), H-B1 (breakout buffer), H-C2 (slope definition — requires GAP-031 resolution first), H-D6 (exit-model bake-off).

## 3.7 Relationship to deferred debt items

The strategy-review memo notes (without editing `technical-debt-register.md` per operator restriction):

- **TD-016** (statistical live-performance thresholds). Wave-1 results across both symbols, both windows, and all five folds directly inform TD-016. No early closure is proposed in 2f; the memo records the dependency so TD-016 can be addressed by the operator after wave-1 review.
- **TD-007** (Binance testnet vs. pure dry-run). Unaffected by Phase 2f. No recommendation proposed.
- **GAP-20260424-030..035** (this memo's appended GAPs). All documentation-level; none block Phase 2f acceptance or wave-1 design.

---

**End of memo.** Part 1 = observations only. Part 2 = four wave-1 hypotheses only. Part 3 = execution recommendations for the later phase. No code, no runs, no tuning performed in Phase 2f itself.
