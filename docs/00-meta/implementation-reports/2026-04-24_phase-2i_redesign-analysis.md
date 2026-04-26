# Phase 2i — Structural Breakout Redesign Analysis Memo

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2i/structural-redesign-planning` (created from `main` at `61696a6` — verified clean working tree, synchronized with `origin/main` after the Phase 2h PR #9 merge)
**Author:** Claude Code (Phase 2i)
**Date:** 2026-04-24
**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict); Phase 2h decision memo (provisional Option B primary recommendation); Phase 2i Gate 1 plan §§ 6–14.A and §26 (three operator Gate 1 conditions applied).
**Scope:** Decision/planning memo only. No code, no new backtests, no new variants, no data downloads, no Binance API calls, no MCP/Graphify, no `.mcp.json`, no Phase 4 work, no edits to `docs/12-roadmap/technical-debt-register.md`.

This memo presents three parts:

- **Part 1 — Factual recap and structural-vs-parametric definition.** Locked facts from Phase 2e/2f/2g/2h; explicit binding test for what counts as structural redesign.
- **Part 2 — Redesign-axis analysis and candidate shortlist.** Five-axis evaluation, R1 coherence test per Gate 1 condition 2, candidate shortlist with each candidate's thesis / problem / replaced-vs-kept / new risks, GAP-030/031/032/033 disposition matrix, validation framework with the explicit H0-anchor statement per Gate 1 condition 3.
- **Part 3 — Recommendation (provisional).** Recommended carry-forward set capped at ≤ 2 per Gate 1 condition 1, primary and fallback next-phase options, "What would change this recommendation" with switch conditions, and the explicit non-proposal list.

---

# Part 1 — Factual recap and structural-vs-parametric definition

## 1.1 Phase 2e baseline (FULL window, untouched control)

Source: `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md`.

- Window: 2022-01-01 → 2026-04-01 UTC (51 months); v002 manifests; zero invalid windows.
- BTCUSDT: 41 trades, WR 29.27%, expR −0.43, PF 0.32, net −3.95%, max DD −4.23%, L/S 21/20, exits STOP 22 / STAGNATION 19 / TRAIL 0.
- ETHUSDT: 47 trades, WR 23.40%, expR −0.39, PF 0.42, net −4.07%, max DD −4.89%, L/S 18/29, exits STOP 35 / STAGNATION 11 / TRAIL 1.
- Funnel dominant rejections (both symbols): `no valid setup` ~57–58%, `neutral bias` ~37%, `no close-break` ~5%; trailing filters each <0.5%.

This is the descriptive baseline and the comparison anchor.

## 1.2 Phase 2f review conclusions (committed)

Source: `docs/00-meta/implementation-reports/2026-04-24_phase-2f_strategy-review-memo.md`, `2026-04-24_phase-2f_gate-1-plan.md`.

- Filter inventory + structural/parametric classification of 25 strategy elements.
- Six new GAP entries: GAP-20260424-030..035 (4 OPEN strategy items + 2 RESOLVED verification-only).
- Pre-declared §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds; §11.3.5 no-post-hoc-loosening discipline.
- Wave-1 cap = 4 single-axis variants; ≤ 1 exit/management variant per wave.

## 1.3 Phase 2g wave-1 result (committed; preserved unchanged)

R-window headline (entries filtered to R = 2022-01..2025-01):

| Variant | BTC trades / WR / expR / PF / netPct / maxDD                          | ETH trades / WR / expR / PF / netPct / maxDD                          |
|---------|-----------------------------------------------------------------------|-----------------------------------------------------------------------|
| H0      | 33 / 30.30% / −0.459 / 0.26 / −3.39% / 3.67%                          | 33 / 21.21% / −0.475 / 0.32 / −3.53% / 4.13%                          |
| H-A1    | 13 / 15.38% / −0.831 / 0.10 / −2.42% / 2.21%                          | 11 / 18.18% / −0.360 / 0.49 / −0.89% / 1.75%                          |
| H-B2    | 69 / 30.43% / −0.326 / 0.43 / −5.07% / 5.53%                          | 57 / 24.56% / −0.440 / 0.35 / −5.65% / 6.53%                          |
| H-C1    | 30 / 26.67% / −0.499 / 0.24 / −3.35% / 3.28%                          | 32 / 15.62% / −0.495 / 0.29 / −3.56% / 3.99%                          |
| H-D3    | 33 / 30.30% / −0.475 / 0.25 / −3.51% / 3.79%                          | 33 / 21.21% / −0.491 / 0.31 / −3.64% / 4.20%                          |

Per-fold consistency (Phase 2f §11.2 5-rolling-folds, fold 1 partial-train per GAP-036): no variant produces a positive expR on **any** BTC test fold. §10.3 / §10.4 verdict: **all four variants disqualified on BTC**.

The wave-1 verdict is **REJECT ALL**. It is preserved unchanged. This memo does not re-derive or re-rank any of these numbers.

## 1.4 Phase 2h provisional recommendation (committed; preserved unchanged)

Phase 2h decision memo §3.1 issued a provisional recommendation:

- Primary (provisional): Option B — Phase 2i: Structural Breakout Redesign Planning, docs-only → this is the phase being executed now.
- Fallback (provisional): Option A — Phase 2i: narrow Wave 2 with H-D6 exit-model bake-off as the centerpiece.
- Phase 4 stays deferred.
- §3.3 enumerated four switch-condition blocks (B → A, B → C, B → defer, any → D).

The Phase 2h provisional recommendation is the input to Phase 2i, not a target for revision. This memo does not re-frame it.

## 1.5 What is now known technically

- The data layer (v002 manifests, 51-month coverage, mark-price + funding joins) is research-credible.
- The backtester is deterministic at fixed inputs.
- The variant-config + stop-trigger-source infrastructure works and is in place.
- Pre-declared §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds applied without post-hoc adjustment produce a clean verdict.
- The fold-scheme convention is pinned (GAP-20260424-036): 5 rolling folds with fold 1 partial-train, all tests inside R.

## 1.6 What remains unresolved strategically

- Is the locked v1 breakout family viable on BTCUSDT/ETHUSDT 15m + 1h with v002 data? Wave 1 says "not on these four axes"; it does not say "not at all".
- Do exit-model decisions matter (the H-D6 question)? Untested.
- Is there a structural redesign axis that meaningfully changes rule shapes (not values) and produces a falsifiable hypothesis? **This is the question this memo answers.**

## 1.7 Definition of structural redesign — binding test

This is the definition that prevents Phase 2j from quietly relabeling parameter tweaks as "structural" (Gate 1 plan §7).

### 1.7.1 What counts as structural

A change is **structural** if it is one of the following:

- A change to **rule shape** (the form of the predicate, not the threshold value). Example: replacing `range_width <= 1.75 × ATR20` with `current_ATR <= percentile_20(rolling_500_bar_ATR)` — the predicate's form changes from "range-based ratio" to "percentile-based ranking".
- A change to **rule input domain** (which signals the rule consumes). Example: replacing 1h `EMA(50) vs EMA(200) + slope` with `ADX threshold + volatility-regime classifier` — the bias rule consumes different signals.
- A change to **rule output coupling** (how a rule's result flows to other rules). Example: replacing the current "if bias is NEUTRAL → reject" gate with "bias acts as a position-size multiplier" — the bias signal stops being a binary gate and becomes a continuous modifier.
- A change to **trade-lifecycle topology** (the sequence and conditions under which lifecycle events fire). Example: replacing "market entry on next-bar open after breakout-bar close" with "limit-order entry at setup boundary, valid for N bars after breakout" — entry topology changes from immediate-fill to conditional-pending.
- A change to **risk/position-management interaction** that introduces a new dimension. Example: introducing volatility-regime-scaled risk_fraction.

### 1.7.2 What counts as parametric (NOT structural)

- Changing a numeric threshold (e.g., 1.75 → 2.00, 0.10 → 0.15, +1.5R → +2.0R).
- Changing a window length while keeping the same rule shape (e.g., setup window 8 → 10).
- Changing an indicator period (e.g., EMA(50) → EMA(20)).
- Combining two parametric changes into a "bundle" without changing any rule shape.

Wave 1 was a parameter search on parametric axes. This memo's candidates must be rule-shape changes, not parameter-search results in disguise.

### 1.7.3 What remains fixed (project-level locks)

The following are **outside the scope** of redesign — project-level locks that no candidate may silently revisit:

- BTCUSDT live primary; ETHUSDT research/comparison only.
- One-way mode, isolated margin, one position max, one active protective stop max, no pyramiding, no reversal while positioned.
- Initial live risk 0.25%; effective leverage cap 2x; internal notional cap mandatory.
- Exchange state authoritative; commands not facts; restart begins in SAFE_MODE.
- Mark-price stops as live protective-stop type.
- v002 datasets, manifests, 51-month coverage window.

### 1.7.4 What must not be silently redefined

- The §10.3 disqualification floor and §10.4 hard reject.
- The §11.3 no-peeking discipline; §11.4 ETH-as-comparison; §11.6 cost-sensitivity gate.
- The §11.3.5 pre-declared-thresholds rule.
- The Phase 2g wave-1 verdict (REJECT ALL).
- The Phase 2h provisional recommendation framing.

---

# Part 2 — Redesign-axis analysis and candidate shortlist

## 2.1 Five-axis evaluation

### 2.1.1 Family S — Setup-pattern redesign

**Rationale.** The dominant 58% "no valid setup" funnel rejection is the largest single source of decision-bar attrition. H-A1 (window length tweak) showed length is not the binding parameter. The shape itself — range-width as a fraction of ATR — may be the issue.

**Evidence from prior phases.** Wave-1 H-A1 collapsed trade frequency without recovering edge. H-A2 (range-width ceiling tweak) and H-A3 (drift-cap tweak) are untested but parametric.

**Candidate rule-shape changes:**
- Volatility-contraction pattern (VCP): setup valid when 15m ATR(20) is below the X-th percentile of its trailing-N distribution.
- Multi-window consolidation: composite signal across 6/8/12 windows.
- Bollinger-band squeeze: setup valid when band-width is at a trailing-N low.

**Expected effect on trade frequency.** Plausibly moderate increase if the new shape captures more genuine compressions; could equally produce fewer if more discriminating.

**Expected effect on expectancy/drawdown.** Uncertain. If percentile-based capture is regime-aligned better than range-based, expR could improve.

**Overfitting risk.** MEDIUM. Percentile-based shapes have implicit lookback parameters; multiple sub-parameter choices once the shape is committed.

**Implementation complexity.** MEDIUM (rolling-percentile computation in incremental indicator cache).

**Validation burden.** Standard §10.3/§10.4 + GAP-036 fold scheme + the mandatory regime-tagging diagnostic.

### 2.1.2 Family B — HTF bias / regime redesign

**Rationale.** The 37% "neutral bias" funnel rejection is the second-largest source of attrition. H-C1 showed EMA-pair speed is not the binding parameter. The bias *shape* may be.

**Evidence from prior phases.** H-C1 (EMA 50/200 → 20/100) marginally worse on both symbols. H-C2 (slope-rule definition) and H-C3 (slope window) untested but parametric. No structural alternative tested.

**Candidate rule-shape changes:**
- ADX-based trend-strength filter: ADX(14) > 20 (or comparable).
- Regime-switching detector (HMM or rule-based: trending / chopping / volatile-breakout).
- Volatility-adjusted bias (combine trend + volatility regime).
- Multi-timeframe confirmation (1h AND 4h).

**Expected effect on trade frequency.** Plausibly increases by reducing NEUTRAL hits.

**Expected effect on expectancy/drawdown.** Uncertain. If current EMA-slope NEUTRAL is genuinely filtering chop, replacement may admit chop and worsen expectancy.

**Overfitting risk.** MEDIUM-HIGH. Regime classifiers have more degrees of freedom.

**Implementation complexity.** MEDIUM (ADX) to HIGH (HMM; HMM also introduces non-deterministic state-estimation that the current backtester is not designed for).

**Validation burden.** Standard. ETH-as-comparison cross-symbol robustness becomes harder.

### 2.1.3 Family E — Entry-timing redesign

**Rationale.** Wave-1 H0 BTC stops out 22/41 trades (54%). Stop-out-on-entry-bar may indicate entry timing is too eager.

**Evidence from prior phases.** No entry-timing redesign tested. Wave 1 used "market entry on next-bar open after breakout-bar close".

**Candidate rule-shape changes:**
- Breakout retest: enter on first pullback to the breakout level within N bars.
- Limit-order entry near setup level.
- Momentum confirmation lag (N additional continuation bars).

**Expected effect on trade frequency.** Plausibly *decreases* — opposite direction from setup/bias redesigns.

**Expected effect on expectancy/drawdown.** Plausibly improves expectancy (better entry quality) but may reduce sample size.

**Overfitting risk.** MEDIUM. Multiple sub-parameters.

**Implementation complexity.** MEDIUM. Backtester currently does next-bar-open fills only; pending-limit logic needs adding.

**Validation burden.** Standard, with reduced trade count making per-fold consistency harder to assess.

### 2.1.4 Family X — Exit-philosophy redesign

**Rationale.** H-D3 was tested in wave 1 but only changed one threshold within the same staged-trailing exit philosophy. Phase 2h flagged the exit-philosophy gap as the strongest case for fallback Wave 2 (H-D6). Family X is the structural-redesign equivalent.

**Evidence from prior phases.** H-B2 hint: "more trades + worse drawdown" suggests exit machinery may be the binding constraint. Wave-1 trail exit count: 0/41 BTC, 1/47 ETH — trailing logic almost never fires. Stagnation exits dominate (BTC 19/41).

**Candidate rule-shape changes:**
- Fixed R-multiple targets (2R or 3R take-profit + time-based fallback).
- Volatility-adaptive trailing (ATR-percentile-scaled).
- Time-based exit (max-hold N bars).
- Opposite-signal exit.
- MAE-aware exit.

**Expected effect on trade frequency.** Unchanged (exit changes don't gate entries).

**Expected effect on expectancy/drawdown.** Highest-leverage axis on expectancy reshaping.

**Overfitting risk.** MEDIUM. Each exit shape has 1–2 parameters.

**Implementation complexity.** LOW-MEDIUM. Exit logic is the most localized strategy-module surface.

**Validation burden.** Standard. Regime-tagging analytic especially valuable for exit redesign.

### 2.1.5 Family R — Risk / position-management interaction redesign

**Rationale.** Phase 2g sizing was never bound. Risk per trade is fixed at 0.25%. There is no equity-curve-aware risk reduction.

**Evidence from prior phases.** Per-fold tables show universally bad fold (2024H1) on every variant on both symbols. Fixed-risk sizing makes the strategy as exposed in bad regimes as in good ones.

**Candidate rule-shape changes:**
- Volatility-targeted sizing (scale risk by inverse of ATR-percentile).
- Equity-curve-aware risk dampening.
- Cooldown after consecutive losses.
- Concurrent-trade allowance — **OUT OF SCOPE per §1.7.3 (violates one-position lock)**.

**Expected effect on trade frequency.** Cooldown and equity-aware reduce frequency in bad runs.

**Expected effect on expectancy/drawdown.** Volatility-targeted shifts the per-trade R distribution; equity-aware and cooldown change drawdown profile substantially.

**Overfitting risk.** HIGH. Equity-curve-aware rules can fit historical drawdown precisely without generalizing.

**Implementation complexity.** MEDIUM. Some shapes (equity-aware) are Phase 4-adjacent.

**Validation burden.** HIGH. Risk-policy changes interact with §1.7.3 project-level locks.

**Family-R disposition.** Excluded from Phase 2i candidate shortlist because: (a) Phase 2g sizing was never bound, so the evidence motivation is weak; (b) any candidate that touches sizing crosses into §1.7.3 project-level locks, requiring explicit operator authorization to revisit those locks. A Family-R candidate could be a legitimate Phase 2j addition only with explicit operator authorization, which Phase 2i does not propose.

## 2.2 R1 coherence test (per Gate 1 condition 2)

The Phase 2i Gate 1 plan listed Candidate R1 as "Volatility-regime breakout" — combining a Family-S setup-pattern change (range-based ratio → volatility-percentile ranking) AND a Family-B bias rule change (EMA-pair-slope → ADX/regime). The operator's Gate 1 condition 2 requires this memo to test whether R1 is one coherent thesis or two separable ideas.

### 2.2.1 The unifying-thesis case

The argument for treating R1 as one coherent thesis: "The strategy's edge problem is not a localized parameter issue but a regime-mismatch issue. A volatility-regime-aware reformulation that consistently uses volatility/regime metrics across both setup and bias is one coherent design, not two — the unifying frame is 'trade breakouts only when volatility-contraction in setup AND volatility/trend regime in bias jointly support it'."

### 2.2.2 The separable-ideas case

The argument for splitting R1 into two candidates: the Family-S change (volatility-percentile setup) and the Family-B change (ADX/regime bias) consume different signals on different timeframes (15m ATR percentiles vs. 1h ADX). Each one would meaningfully change the strategy on its own. Each one targets a distinct funnel rejection (S targets 58% no-valid-setup; B targets 37% neutral-bias). The "unifying frame" is more of a *packaging* than a *thesis* — saying "we'll use volatility metrics in two places" is not the same as "these two changes share a single mechanism".

### 2.2.3 Conclusion of the coherence test

**R1 is two separable ideas, not one coherent thesis.** The two changes:
- target different funnel rejections,
- consume different signals on different timeframes,
- can be implemented and validated independently,
- have different overfitting risk profiles (Family-S MEDIUM; Family-B MEDIUM-HIGH),
- have different implementation complexity (S MEDIUM; B MEDIUM-HIGH).

Carrying R1 forward as a bundled candidate would be a multi-axis structural change without a unifying mechanism — i.e., effectively a bundled variant in disguise. Per Phase 2f §9.1 and the Gate 1 condition 2 discipline, this memo splits R1 into two independent candidates: **R1a (Family-S setup-pattern volatility)** and **R1b (Family-B HTF bias/regime)**.

If a future operator-approved phase finds genuine evidence that R1a and R1b's mechanisms must be co-designed (e.g., R1a only works when paired with R1b because the setup signal depends on the regime classifier), that would be a legitimate Phase 2k bundled-candidate proposal under explicit Phase 2f §9.1 deviation — but the current evidence does not support it.

## 2.3 Redesign-candidate shortlist (4 candidates)

Each candidate is a single-axis structural rule-shape change. Multi-axis structural is forbidden in Phase 2i unless defended as one coherent thesis (R1 above did not pass that test).

### Candidate R1a — "Volatility-percentile setup"

- **Thesis.** The dominant 58% no-valid-setup rejection results from a setup shape (range-based ratio with fixed ATR multiplier) that does not reliably capture volatility-contraction periods preceding genuine breakouts. A percentile-based shape that ranks the current ATR against its trailing distribution is more regime-aware and should capture more genuine compressions while excluding chop.
- **Problem from Phase 2e/2g it tries to solve.** 58% "no valid setup" funnel rejection on the dominant axis where wave-1 H-A1 (window length) failed.
- **What of the current v1 family it replaces.** Setup-pattern rule (range-width ≤ 1.75 × ATR20 + drift cap 0.35 × range → current 15m ATR(20) ≤ X-th percentile of trailing-N ATR distribution).
- **What it keeps.** 8-bar window (still defines "what bars are checked"), 15m signal, 1h bias rule (unchanged), bar-close confirmation, structural stop formula, exchange-side STOP_MARKET, all §1.7.3 project-level locks.
- **New risks.** Implicit sub-parameters (percentile threshold X, lookback-N) become the new tunable surface. May admit setups during regime transitions where ATR-percentile is briefly low for non-genuine reasons.
- **Family map.** S (single-axis structural).

### Candidate R1b — "ADX/regime HTF bias"

- **Thesis.** The 37% neutral-bias rejection results from a bias shape (EMA-pair + slope) that excludes too many bars while also failing to filter chop-prone regimes. An ADX trend-strength filter (or a rule-based regime classifier) consumes a different signal that more directly captures whether a trend is genuinely present, regardless of EMA-pair direction agreement.
- **Problem from Phase 2e/2g it tries to solve.** 37% "neutral bias" funnel rejection where wave-1 H-C1 (EMA pair speed) failed.
- **What of the current v1 family it replaces.** HTF bias rule (1h EMA(50) vs EMA(200) + slope rule → 1h ADX(14) ≥ threshold OR rule-based regime classifier with explicit trending/chopping output).
- **What it keeps.** 1h timeframe for bias, setup rule (unchanged), trigger, entry timing, stop, exit, all §1.7.3 project-level locks.
- **New risks.** ADX threshold is a new parametric surface; rule-based regime classifier has higher DOF. Cross-symbol robustness (§11.4 ETH-as-comparison) is harder because regime classifiers may behave differently on BTC vs ETH.
- **Family map.** B (single-axis structural).

### Candidate R2 — "Pullback-confirmed entry"

- **Thesis.** Wave-1 H0 BTC stops out 22 of 41 trades (54%); a substantial fraction of stop-outs occur shortly after the entry bar, indicating immediate next-bar-open entry on a breakout close gets whipsawed in the 15m timeframe. Pullback-confirmed entries reduce false-start rate at the cost of lower frequency.
- **Problem from Phase 2e/2g it tries to solve.** The high stop-out rate on the BTC wave-1 baseline that no parametric exit tweak (H-D3) addressed.
- **What of the current v1 family it replaces.** Entry-timing rule (next-bar-open after breakout close → pending limit at setup boundary, valid for N bars after breakout).
- **What it keeps.** Setup-pattern, bias, trigger condition (breakout bar still defines the candidate), stop, exit, all §1.7.3 project-level locks.
- **New risks.** Lower trade count (some breakouts won't retest within N bars). Per-fold sample-size issues. Backtester needs new pending-limit-fill logic (not currently implemented).
- **Family map.** E (single-axis structural).

### Candidate R3 — "Fixed-R exit with time stop"

- **Thesis.** The current staged-trailing exit clips profits during retracements (trailing rarely fires: 0/41 BTC, 1/47 ETH) while exposing trades to multi-bar adverse moves. A clean fixed-2R take-profit with a time-based 8-bar fallback aligns exits with how trades actually behave and removes the largely-inactive trailing machinery.
- **Problem from Phase 2e/2g it tries to solve.** Trail exit count near-zero in the wave-1 baseline; stagnation dominates exits on BTC (19/41); H-D3 (a parametric break-even tweak) did not move the needle.
- **What of the current v1 family it replaces.** Exit philosophy (Stage 3–7 staged-trailing → fixed-2R take-profit + time-based 8-bar fallback exit). Stage-3 risk-reduction (−0.25R move), break-even at Stage 4, Stage-5 trailing, and the +1R MFE stagnation gate are all removed.
- **What it keeps.** Setup, bias, trigger, entry timing, structural stop formula (initial stop preserved), exchange-side STOP_MARKET protective stop, all §1.7.3 project-level locks.
- **New risks.** Fixed-2R may clip real big winners. The R-multiple choice (2R vs 3R vs other) is itself a parameter that becomes structural-rule-shape only if pre-declared as a single value with justification — otherwise R3 collapses into a sweep that is functionally H-D6.
- **Family map.** X (single-axis structural).

### Why these four and not more

- The shortlist intentionally splits R1 into R1a + R1b per the §2.2 coherence test result — preventing multi-axis structural change without a unifying mechanism.
- R2 is the cleanest entry-timing redesign that motivates wave-1's high stop-out rate.
- R3 is the cleanest exit-philosophy redesign that contains the H-D6 question into a single committed shape.
- Family-R candidates are excluded per §2.1.5 (project-level locks).
- Bias-only structural change (B alone) is now R1b; setup-only structural change (S alone) is now R1a; multi-axis "regime breakout" (S + B together) is rejected per §2.2.

## 2.4 GAP-030 / 031 / 032 / 033 disposition matrix

Per Gate 1 plan §10. Each candidate's disposition is explicit:

| GAP | Topic | R1a (S) | R1b (B) | R2 (E) | R3 (X) |
|---|---|---|---|---|---|
| GAP-20260424-030 | Break-even +1.5R vs +2.0R rule-text conflict | CARRIED | CARRIED | CARRIED | **SUPERSEDED** — R3 removes break-even from the exit machinery; the conflict becomes moot. To be marked SUPERSEDED in the ambiguity log when R3 is selected for execution. |
| GAP-20260424-031 | EMA slope wording (discrete vs. fitted) | CARRIED | **SUPERSEDED** — R1b replaces EMA-slope with ADX/regime; the slope-wording question becomes moot. To be marked SUPERSEDED when R1b is selected for execution. | CARRIED | CARRIED |
| GAP-20260424-032 | Backtest trade-price stop vs. live MARK_PRICE stop sensitivity | CARRIED — execution-realism question, survives any redesign. Mark-price sensitivity must be a required report cut for any promoted redesign per §2.5.6. | CARRIED | CARRIED | CARRIED |
| GAP-20260424-033 | Stagnation window (8 bars, +1R gate) classification | CARRIED | CARRIED | CARRIED | **CARRIED-AND-EXTENDED** — R3's time-based 8-bar fallback overlaps the stagnation window concept; the redesign should explicitly state whether the time-based fallback is the "new stagnation" or whether stagnation is removed entirely. To be addressed in R3's Phase 2j rule spec. |

The earlier Gate 1 plan §10 used a 3-candidate matrix (R1, R2, R3); the matrix is now 4 candidates because of the §2.2 split. R1 is removed; R1a inherits the Family-S row, R1b inherits the Family-B row.

## 2.5 Validation framework for redesigned candidates

### 2.5.1 H0-anchor statement (per Gate 1 condition 3)

**Two binding statements about the comparison anchor for any redesign candidate:**

- **H0 remains the only comparison anchor for redesign candidates.** All redesign performance is computed vs. the locked Phase 2e baseline H0 re-run on R, never vs. wave-1 variants. Redesign §10.3 / §10.4 evaluation uses H0's R-window numbers as the denominator for Δexp, ΔPF, and |maxDD| ratio computations.
- **Phase 2g wave-1 variants (H-A1, H-B2, H-C1, H-D3) are historical evidence only, not promotion baselines.** Their R-window numbers may be cited diagnostically (e.g., "H-B2's near-pass on §10.3.a illustrates that trigger looseness can improve expR" — diagnostic citation) but they do not serve as comparison anchors for any redesign §10.3 / §10.4 evaluation. A redesign that improves over H-B2 but worsens over H0 is disqualified.

### 2.5.2 Pre-declared thresholds

Redesigned candidates use the **same** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds as wave 1 — applied to the redesign's R-window result vs. the H0 baseline (per §2.5.1). No threshold tightening or loosening because the hypothesis is "different". Per §11.3.5, the thresholds are pre-committed and cannot be adjusted after seeing results — for any wave, including a redesign wave.

### 2.5.3 Per-candidate spec must pre-declare

Each Phase 2j carry-forward candidate's spec must pre-declare:

- The exact rule shape (form of the predicate, indicator inputs, output coupling).
- Any sub-parameter values (e.g., R3's R-multiple = 2.0; R1a's percentile = 20th; R1b's ADX threshold = 20). Each value is committed, not swept.
- The §10.3 / §10.4 thresholds (reused unchanged from Phase 2f).
- Any candidate-specific success-criterion that supplements §10.3 (e.g., R3 may add a per-symbol "fixed-2R hit rate ≥ X%" diagnostic gate).

### 2.5.4 R/V split and fold scheme

R/V split per Phase 2f §11.1 stays: R = 2022-01..2025-01, V = 2025-01..2026-04. Fold scheme per GAP-20260424-036: 5 rolling folds, fold 1 partial-train, all tests within R. Supplemental 6-half-year appendix per Phase 2g §3.A retained for descriptive coverage.

### 2.5.5 Mandatory diagnostics for redesigns

Every redesign report must include (in addition to the §10.1–§10.2 cuts already required by Phase 2f):

- **Per-regime expR**: classify each trade's entry by realized 1h volatility regime (low/medium/high based on trailing percentile) and compute per-regime expR.
- **MFE distribution**: histogram of MFE in R-multiples.
- **Per-direction long/short asymmetry**: separate expR / PF / win rate for long-only and short-only subsets.
- **GAP-032 mark-price sensitivity**: every promoted redesign candidate must run with `stop_trigger_source=TRADE_PRICE` and report the comparison vs. MARK_PRICE.

### 2.5.6 Why redesigned candidates compare to H0 and not to each other

Comparing redesigned candidates to each other risks an implicit "tournament" that selects whichever candidate is best on R, which is a peeking violation — equivalent to running multiple variants and picking the winner without a pre-declared selection rule. Each candidate is judged independently against H0, with the §10.3 / §10.4 thresholds. If multiple candidates pass, the §11.3 top-1–2-to-V rule still applies, which is a pre-declared selection.

## 2.6 Relationship to fallback Wave 2 (Phase 2h Option A)

Phase 2h §3.1 fallback was Wave 2 narrowly bounded to H-D6 (exit-model bake-off). The conceptual relationship to Candidate R3:

- **H-D6** is a comparative bake-off — tests four exit philosophies side-by-side as parametric variants on H0's other rules.
- **Candidate R3** is a structural commitment to one specific exit philosophy (fixed-2R + 8-bar fallback) with a single committed sub-parameter set.

If Phase 2j carries R3 forward, the H-D6 axis is implicitly resolved by R3's commitment. If the project switches to fallback Wave 2 (Phase 2h §3.3 condition), R3 is not pursued; H-D6's bake-off result then becomes input for any future redesign.

## 2.7 Relationship to Phase 4

Phase 2h §2.10 / §3.3 noted Phase 4 stays deferred. This memo further strengthens the case for deferral: Phase 4's strategy-coupled parts (entry-intent contracts, exit-reason taxonomy, management lifecycle, dispatch hooks) interact with the v1 spec; redesigned candidates will reshape those contracts (especially R3 which removes most of the management-stage taxonomy). Building Phase 4 first risks reshaping it for redesigned strategies. Phase 2h §3.3 "any → D" switch block (explicit operator policy change) remains the only condition under which Phase 4 advances.

---

# Part 3 — Recommendation (provisional)

## 3.1 Recommendation framing (provisional, evidence-based)

This recommendation is **provisional and evidence-based, not definitive**. It is a judgement about the highest-value next research step given the evidence currently in hand. It is explicitly **not** any of the following:

- It is **not** a claim that structural redesign automatically produces a better strategy. Redesign is a research bet that may itself produce a clean negative.
- It is **not** a claim that the breakout family is permanently viable. Wave-1 evidence rules out four single-axis paths on this spec on this data; redesign tests whether different rule shapes on this data produce edge.
- It is **not** a claim that fallback Wave 2 is invalid. Wave 2 with H-D6 remains a legitimate alternative path.

## 3.2 Recommended carry-forward set to Phase 2j (≤ 2 per Gate 1 condition 1)

**Recommended carry-forward (provisional): R1a + R3.**

Reasoning:

- **R1a (Volatility-percentile setup)** targets the largest funnel rejection (58% no-valid-setup) on a single axis whose parametric equivalent (H-A1 window length) was tested and failed. A volatility-percentile shape consumes a different signal-form (rolling-percentile of ATR) than range-based ratio, making it a genuine rule-shape change. Implementation is contained to the setup detector. Highest-evidence-grounded structural candidate among Family S.
- **R3 (Fixed-R exit with time stop)** targets a structurally inactive part of the current strategy (trailing-exit count near zero) with an exit-philosophy commitment that removes most of the staged-trailing machinery. Cleanly contained to TradeManagement. Phase 2j rule spec is the most achievable for R3 because the exit form is the simplest to pre-declare.

**NOT recommended for carry-forward:**

- **R1b (ADX/regime HTF bias).** Strong motivation but higher overfitting risk and higher implementation complexity (especially if HMM-style classifier is the chosen shape). ETH-as-comparison cross-symbol robustness is harder for regime classifiers. Carrying both R1a and R1b would exceed the ≤ 2 cap and would also constitute a multi-axis structural change spanning S + B that the §2.2 coherence test rejected.
- **R2 (Pullback-confirmed entry).** Plausible but the wave-1 stop-out evidence is indirect (the high BTC stop-out rate could equally be a setup or trigger problem rather than entry-timing). Backtester needs new pending-limit-fill logic before R2 can be executed, which is additional implementation cost. Also reduces trade count, making per-fold consistency harder to establish.

The carry-forward set is provisional. Operator may choose differently (e.g., R1a + R1b if regime-aware bias is judged more important than exit redesign; or R3 + R2 if entry+exit reshape is judged the right pair). The §3.4 switch conditions enumerate when the recommendation should change.

## 3.3 Recommended next-phase choice

**Primary (provisional): Phase 2j Option A — Structural redesign memo only (docs-only).** Phase 2j writes full rule specs for the carry-forward set (R1a + R3) with falsifiable hypotheses, pre-declared sub-parameter values (no sweeps), and pre-declared §10.3 / §10.4 thresholds (reused from Phase 2f). This is the same docs-only step Phase 2f executed for the v1 spec axes; doing it for redesigns is the consistent path.

**Secondary (fallback, provisional): Phase 2j Option B — Redesign candidate execution planning.** Appropriate only if the carry-forward set narrows to a single fully-specified candidate during Phase 2j Option A's spec writing. Most plausibly applies to R3 alone (the most contained candidate); less plausibly to R1a alone or to R1a + R3 together.

**Phase 4 stays deferred** per existing operator policy. Phase 2i does not propose advancing it.

## 3.4 What would change this recommendation

The recommendation is provisional. The following kinds of evidence or reasoning would justify switching paths:

### Switch carry-forward set (R1a + R3 → different pair)

- Operator preference for entry-redesign evidence (R2) over setup-redesign evidence (R1a) given the wave-1 stop-out rate.
- A reasoned argument that R1a and R1b are co-design-critical (i.e., R1a only works when paired with R1b because the setup signal depends on a regime classifier) — would require explicit Phase 2f §9.1 deviation approval to bundle.
- A reasoned argument that bias redesign (R1b) is more directly evidence-grounded than setup redesign (R1a) given that wave-1 H-C1 was the closest fail among the bias-axis tweaks.

### Switch Option A (memo) → Option B (execution planning)

- Phase 2i analysis converges on a single candidate (most plausibly R3 alone) with a complete rule spec and no remaining design decisions.
- Operator preference for execution evidence over additional docs-only spec writing once the candidate space is narrowed to one.

### Switch Option A → Option C (fallback Wave 2 with H-D6)

- Phase 2j (when it runs) concludes that no redesign candidate produces a falsifiable hypothesis without unmanageable parameter-overfitting risk.
- Operator preference for execution evidence on the exit-model axis specifically before any structural redesign.

### Switch Option A → Option D (Phase 4)

- Explicit operator policy change that operational infrastructure should be built without strategy-edge confirmation. Current policy is against this; this memo does not propose changing it.

### Switch Option A → defer (no new phase)

- Discovery during Phase 2j of a documentation inconsistency requiring a docs-only correction phase.
- Operator decision to pause strategy work and prioritize a different operational concern.
- A new operator restriction (timing, capital, scope) that makes the current options materially less attractive.

## 3.5 What this memo does NOT propose

To keep the boundary explicit:

- Any code change, test addition, or backtest run.
- Any threshold tightening or loosening on §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- Any re-derivation or re-ranking of the wave-1 result. The verdict is REJECT ALL per Phase 2g and stays REJECT ALL.
- Any V-window run, slippage sensitivity, or stop-trigger sensitivity.
- Any live deployment, paper/shadow readiness, or capital exposure proposal.
- Any edits to `docs/12-roadmap/technical-debt-register.md` (operator restriction held).
- Any MCP / Graphify enablement.
- Any Phase 4 work.
- Any Family-R risk/sizing redesign (excluded per §2.1.5).
- Any multi-axis bundled candidate (R1 split per §2.2).
- Any silent re-classification of parametric tweaks as structural (the §1.7 binding test applies).
- Any comparison of redesigned candidates to wave-1 variants as promotion baselines (per §2.5.1).

---

**End of memo.** Phase 2i is decision/planning only; Part 3's recommendation hands the next-boundary decision (Phase 2j Option A or Option B; or fallback Option C; or deferred Option D) to the operator with the conditions that would change either choice spelled out explicitly.
