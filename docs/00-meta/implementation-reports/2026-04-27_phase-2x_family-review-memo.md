# Phase 2x — V1 Breakout Family-Level Review Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL preserved); Phase 2h decision memo; Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary; ETHUSDT research/comparison only); Phase 2j memo §C / §D; Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE; baseline-of-record per Phase 2p §C.1); Phase 2m comparison report (R1a+R3 mixed-PROMOTE; retained-for-future-hypothesis-planning per Phase 2p §D); Phase 2n strategy-review memo (R3 = research-leading); Phase 2o asymmetry-review memo (BTC/ETH asymmetry diagnosed as market-structure × strategy interaction); Phase 2p consolidation memo (R3 baseline-of-record locked; future-resumption pre-conditions §F); Phase 2r R1b-narrow spec memo; Phase 2s R1b-narrow comparison report (PROMOTE / PASS with sample-size caveats); Phase 2t / 2u / 2v / 2w-A / 2w-B / 2w-C R2 family of memos and execution reports; Phase 2w R2 variant comparison report (FAILED — §11.6 cost-sensitivity blocks); Post-Phase-2w consolidation report.

**Phase:** 2x — Family-level review of the V1 breakout-continuation strategy arc. **Docs-only.** No code, no backtests, no variants, no parameter changes, no project-lock changes.

**Branch:** `phase-2x/family-review`. **Memo date:** 2026-04-27 UTC.

**Status:** Recommendation drafted. R3 remains baseline-of-record. H0 remains framework anchor. R1a, R1b-narrow, R2 remain retained as research evidence / non-leading. No paper/shadow, Phase 4, live-readiness, or deployment work authorized. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 2x is deciding

Phase 2x is a family-level review, not a candidate-level review.

Phase 2 of the Prometheus project executed a disciplined research arc on a single strategy family: V1 breakout-continuation with higher-timeframe trend bias. The arc produced one locked baseline (H0), one cleanly-promoted structural redesign (R3 — exit philosophy), and three post-R3 structural redesigns under unchanged framework discipline (R1a — setup-validity predicate; R1b-narrow — bias-strength predicate; R2 — entry-lifecycle topology). Each candidate has been reported, reviewed, and consolidated; R3 is the locked baseline-of-record per Phase 2p §C.1; R1a, R1b-narrow, and R2 are retained as research evidence / non-leading per Phase 2p §D and the post-Phase-2w consolidation.

The candidate-level work has run its course. The next decision is not "which candidate to test next" — it is **family-level**: whether the V1 breakout family, as a class of strategies, has reached its useful ceiling under the current framework, and if so, what the right next move is.

Phase 2x weighs four mutually-exclusive possibilities:

1. **Remain paused.** Hold the consolidation state established by Phase 2p + post-Phase-2w. No new research phase is authorized; the family arc is complete-as-of-now and any future direction-change is operator-driven later.
2. **One more narrowly-justified breakout-family research phase.** Authorize one additional docs-only spec-writing phase for a specific evidence-grounded hypothesis (e.g., regime-conditional R1a-prime per Phase 2o §F.1, or another candidate not yet enumerated).
3. **Independent slippage/cost-policy review.** Authorize a docs-only operator-policy review of the framework's HIGH-slippage threshold (Phase 2f §11.6, currently 8 bps) given Binance's actual BTCUSDT futures slippage profile, prompted by R2's §11.6 failure. Not a strategy-redesign decision; a framework-calibration decision.
4. **Pivot toward planning a new strategy family.** Authorize a docs-only survey of candidate non-breakout families (mean-reversion, funding-rate arbitrage, cross-symbol relative momentum, etc.) as a deliberate family-shift.

Phase 2x's job is to make the family-level case for one of these explicitly, with reasoning grounded in the accumulated evidence. The recommendation is provisional; the operator decides.

Phase 2x does NOT decide whether to deploy R3, whether to begin Phase 4, whether to authorize paper/shadow, or whether to lift any project-level lock. Those are separate decisions outside Phase 2x scope.

---

## 2. Summary table of the V1 breakout-family arc

R-window evidence: 2022-01-01 → 2025-01-01, MEDIUM slippage, MARK_PRICE stop-trigger, locked Phase 2e v002 datasets, BTCUSDT primary, ETHUSDT comparison.

| Candidate | Phase | Structural axis | BTC trades | BTC expR | BTC PF | BTC \|maxDD\| | ETH trades | ETH expR | ETH PF | ETH \|maxDD\| | §10.3 verdict (vs H0) | Combined verdict |
|-----------|-------|-----------------|-----------:|---------:|-------:|---------------:|-----------:|---------:|-------:|---------------:|------------------------|------------------|
| **H0** (baseline) | 2e | locked anchor | 33 | −0.459 | 0.255 | 3.67% | 33 | −0.475 | 0.321 | 4.13% | (anchor) | locked anchor |
| **R3** | 2l | exit philosophy (FIXED_R + 8-bar time-stop, no trailing) | 33 | **−0.240** | **0.560** | **2.16%** | 33 | **−0.351** | **0.474** | **3.65%** | PROMOTE (§10.3.a + §10.3.c on both) | **PROMOTE — baseline-of-record** |
| **R1a + R3** | 2m | setup-validity predicate (volatility-percentile, X = 25 / N = 200) on top of R3 | 22 | −0.420 | 0.355 | 2.33% | 23 | **−0.114** | **0.833** | 2.96% | PROMOTE (BTC §10.3.c only; ETH §10.3.a + §10.3.c) | **mixed-PROMOTE — retained research evidence; non-leading** |
| **R1b-narrow** | 2s | bias-validity predicate (slope-strength magnitude S = 0.0020) on top of R3 | 10 | −0.263 | 0.561 | 1.09% | 12 | −0.224 | 0.622 | 1.28% | PROMOTE (§10.3.a + §10.3.c on both — first such) | **PROMOTE / PASS-with-caveats — retained research evidence; non-leading** |
| **R2 + R3** | 2w | entry-lifecycle topology (pullback-retest with 8-bar validity window) on top of R3 | 23 | −0.275 | 0.529 | 1.65% | 19 | −0.432 | 0.454 | 2.48% | MED-slip §10.3 PROMOTE; **§11.6 HIGH-slip gate FAILS** | **FAILED — §11.6 cost-sensitivity blocks; retained research evidence** |

Key out-of-sample (V-window 2025-01-01 → 2026-04-01) observations across the arc:

- **R3 V**: direction-of-improvement holds on both symbols (BTC expR −0.287; ETH expR −0.093 — both improvements vs H0 V).
- **R1a + R3 V**: ETH netPct **+0.69%** (first positive V-window in project history); BTC catastrophic at n=4 (0% WR / expR −0.990).
- **R1b-narrow V**: ETH netPct **+0.28%** (second positive V-window); BTC n=1 (uninterpretable; single losing trade).
- **R2 + R3 V**: ETH near-parity with R3 V (n=12, expR −0.108); BTC n=5 sample-fragile (expR −0.901).

Slippage / cost-sensitivity behavior across the arc:

- **R3**: cost-robust. PROMOTES on both symbols at LOW / MEDIUM / HIGH (8 bps).
- **R1a + R3**: cost-monotone. ETH essentially break-even at LOW (expR −0.022).
- **R1b-narrow**: cost-monotone. PROMOTES at HIGH on both symbols.
- **R2 + R3**: cost-fragile. **§11.6 FAILS** at HIGH on both symbols (BTC Δexp_H0 −0.014; ETH Δexp_H0 −0.230). The first §11.6 failure in the family arc.

---

## 3. Per-candidate summary

For each candidate: what mechanism it tested, what it improved, what failed, whether it changed the baseline, whether it remains useful as research evidence.

### 3.1 H0 — locked Phase 2e baseline

- **Mechanism:** None. H0 is the baseline, not a candidate. Range-based setup-validity (range-width ≤ 1.75 × ATR(20) AND |close[−1] − open[−8]| ≤ 0.35 × range_width); 1h binary slope-3 direction-sign bias + EMA(50) / EMA(200) position; 0.10 × ATR breakout buffer; staged-trailing exit topology (Stage 3 risk reduction at +1.0 R, Stage 4 break-even at +1.5 R, Stage 5 trailing at +2.0 R, Stage 7 stagnation at 8 bars without +1.0 R MFE); structural stop with 0.10 × ATR(20) buffer.
- **Improvement:** Not applicable.
- **Failure:** Aggregate negative R-window expR on both symbols (BTC −0.459; ETH −0.475).
- **Baseline change:** None — H0 *is* the baseline. Phase 2i §1.7.3 designates H0 as the **sole** §10.3 / §10.4 anchor for all candidates.
- **Research-evidence value:** **Foundational.** All candidate comparisons are anchored on H0. H0's bit-for-bit reproducibility across phases (Phase 2g, 2k, 2l, 2m, 2s, 2w-A) is itself a project-discipline artifact.

### 3.2 R3 — Fixed-R + time-stop exit philosophy

- **Mechanism tested:** Replace H0's staged-trailing topology with a two-rule terminal exit: take-profit at +2.0 R; unconditional time-stop at 8 bars; protective stop never moved intra-trade.
- **What it improved:** Broad-based and clean. R3 improves expR in **all 6 regime-symbol cells** (Phase 2l §6.1). Per-fold (5 rolling, GAP-036): R3 beats H0 in **4/5 BTC folds and 3/5 ETH folds**. First-ever positive-expR BTC folds (F2 +0.015, F3 +0.100). V-window confirms direction-of-improvement on both symbols. ETH shorts under R3 produce the **first positive direction-symbol cell** (+0.028 R / PF 1.07). Implementation cleanliness: zero TRAILING_BREACH / STAGNATION leakage; H0 control reproduces baseline bit-for-bit.
- **What failed:** Aggregate R-window expR remains negative (BTC −0.240; ETH −0.351). PF below 1 on both symbols. R3 is "less negative than H0", not break-even.
- **Baseline change:** **YES.** R3 is the **baseline-of-record** per Phase 2p §C.1. Future structural-redesign hypotheses are specified as "X on top of R3"; future operational scaffolding (when authorized) targets R3 as the deployable variant.
- **Research-evidence value:** **Strongest single candidate evidence in the project.** R3 is the only clean broad-based cross-symbol PROMOTE. It is robust to slippage (clears HIGH at BTC −0.445 / ETH −0.549), bit-identical between MARK_PRICE and TRADE_PRICE stop-triggers (zero gap-throughs), and consistent across regime decomposition. Phase 2n committed R3 as research-leading; Phase 2o §G.2 stated the BTC/ETH asymmetry **increases** confidence in R3.

### 3.3 R1a — volatility-percentile setup predicate (on top of R3)

- **Mechanism tested:** Replace H0's range-based setup-validity predicate with a percentile-rank predicate (15m ATR(20) at close of bar B−1 in bottom X = 25th percentile of trailing N = 200-bar ATR distribution).
- **What it improved:** Symbol-asymmetric. **ETH improvement is substantial and clear** — Δexp +0.362 R / ΔPF +0.512 vs H0; Δexp_R3 +0.237 / ΔPF_R3 +0.359 vs R3. ETH V-window: **first positive netPct** in project history (+0.69%, 8 trades / 62.5% WR / expR +0.386 R / PF 2.222). ETH low-vol R-window: first cell with positive expR AND PF > 1 (n=11 / +0.281 / 1.353). ETH shorts: strongest direction-symbol cell ever (n=16 / +0.387 R / PF 1.906). Implementation cleanliness: 100% of R1a entries at ATR percentile ≤ 25% (predicate working as designed).
- **What failed:** **BTC degrades vs R3.** Δexp_R3 −0.180 R; ΔPF_R3 −0.205. BTC R-window §10.3.a does NOT clear (Δexp +0.039 below the +0.10 magnitude threshold; only §10.3.c strict-dominance fires). BTC V-window catastrophic at n=4 (0% WR, expR −0.990). The compression-bar selection is mechanically correct on BTC too, but the post-compression follow-through differs by symbol. Phase 2o §C diagnosis: market-structure × directional-bias interaction, not a fixable rule defect.
- **Baseline change:** No. R1a+R3 is the **promoted-but-non-leading branch** per Phase 2n; **retained-for-future-hypothesis-planning** per Phase 2p §D. The §1.7.3 BTCUSDT-primary lock makes a BTC-degrading variant ineligible for v1 deployment.
- **Research-evidence value:** **High.** R1a's ETH evidence is unprecedented under unchanged framework discipline (the only positive V-window netPct over +0.5%). The ETH-asymmetry finding is informative for any future regime-conditional R1a-prime hypothesis (Phase 2o §F.1). The BTC degradation is informative as a real fact about market-structure × strategy interaction, not a design flaw.

### 3.4 R1b-narrow — bias-strength magnitude predicate (on top of R3)

- **Mechanism tested:** Replace H0's binary slope-3 direction-sign check with a magnitude check at threshold S = 0.0020 (anchored to the existing `ATR_REGIME_MIN` constant per Phase 2r §F).
- **What it improved:** **First candidate to clear §10.3.a on both symbols simultaneously** at the magnitude threshold (BTC Δexp +0.196 / ΔPF +0.305; ETH Δexp +0.251 / ΔPF +0.301). |maxDD| ratios 0.296× BTC / 0.308× ETH — well below the 1.5× veto floor. Cost-monotone; PROMOTES at HIGH slippage. ETH V-window: second positive netPct (+0.28%, 8 trades / 50% WR / +0.154 R / PF 1.408). First-time positive BTC-shorts cell (n=4, +0.136 R / PF 1.524). On the formal-framework metric, R1b-narrow is the strongest result the project has produced.
- **What failed:** **Trade-count drops 65–70%.** BTC 33 → 10; ETH 33 → 12. Per-fold sample sizes collapse (BTC 0/2/1/2/3; ETH 3/2/1/2/2). V-window BTC has n=1 (uninterpretable; single losing trade). Zero entries in the strong-strength bucket (≥ 0.0100); entries concentrate in marginal-and-moderate buckets. **R3-anchor view: roughly neutral marginal contribution on BTC** (Δexp_R3 −0.023; ΔPF_R3 +0.000) — R1b-narrow's R-window improvement vs H0 is **dominated by R3's exit-machinery contribution plus the bias-strength filter's trade-count concentration**, not by genuine per-trade-expectancy gain on top of R3.
- **Baseline change:** No. Phase 2s §13 explicitly states "R1b-narrow does not replace R3 as the baseline-of-record without operator decision". The post-2s operator/ChatGPT joint interpretation was that **bias-strength was not the missing mechanism** — the formal §10.3.a-on-both clearance is real, but the absolute-edge case is sample-fragile and dominated by R3.
- **Research-evidence value:** **Medium.** R1b-narrow's PROMOTE-with-caveats demonstrated that the formal framework can produce the strongest-yet result via trade-count concentration without a corresponding absolute-edge gain. It is informative as a methodological observation about §10.3 small-sample behavior. The first-time positive BTC-shorts cell is informative but n=4-fragile.

### 3.5 R2 — pullback-retest entry-lifecycle topology (on top of R3)

- **Mechanism tested:** Replace H0's market-on-next-bar-open entry with conditional-pending pullback-retest entry. Signal at bar B → register PendingCandidate → wait up to 8 bars for low ≤ setup_high (LONG) AND close > structural_stop → fill at next-bar open after confirmation. Phase 2v Gate 2 amendment added STRUCTURAL_INVALIDATION cancellation at precedence position 3.
- **What it improved:** Per-trade expectancy on intersection trades. **M1 PASS on BTC** (Δexp +0.123 R per trade on intersection trades vs R3 — direction-symmetric: longs +0.116, shorts +0.128). **M3 PASS** on both symbols (mechanical R-distance reduction; ratios 0.844 BTC / 0.815 ETH). MED-slip §10.3 vs H0: PROMOTE (BTC §10.3.a + §10.3.c; ETH §10.3.c). ETH low-vol cell positive (n=7, +0.091 / PF 1.115 — second-time observation after R1a+R3). MFE distribution improvement (BTC R2 mean +1.10 vs R3 +0.79; ETH R2 +1.13 vs R3 +1.06). Implementation cleanliness: all P.14 hard-block checks pass; no engine bugs; H0 / R3 controls reproduce bit-for-bit.
- **What failed:** **§11.6 cost-sensitivity gate FAILS** on both symbols at HIGH slippage (BTC Δexp_H0 −0.014; ETH Δexp_H0 −0.230). The first §11.6 failure in the family arc. R2's edge is **slippage-fragile** — at HIGH slippage (8 bps), the cost increase ≈ M1's per-trade gain (+0.12 R BTC). **M2 FAILS** on both symbols (BTC stop-exit fraction R2 0.261 > R3 0.242; ETH 0.526 > 0.424). The R2 thesis ("smaller stop + larger position ⇒ fewer stop-outs") is partially refuted: pullback fills are stopped at a slightly higher rate than R3's broader pool. Per-trade expectancy gain comes from price geometry (smaller R-distance → larger payoff per ATR), not from selecting trades with lower stop-out rates. **R3-anchor view negative** (BTC Δexp_R3 −0.035; ETH Δexp_R3 −0.081). V-window BTC n=5 (sample-fragile, expR −0.901).
- **Baseline change:** No. Phase 2w §16.2 explicitly preserves R3 as baseline-of-record. R2 cannot displace R3; its framework verdict is FAILED.
- **Research-evidence value:** **Medium-high.** R2's evidence is the most diagnostically rich of the post-R3 candidates. The M1 + M3 pass with M2 fail is a precise mechanism-level finding. The §11.6 cost-sensitivity failure is documented and anticipated (Phase 2t §11.6 entry #2 explicitly warned of this failure mode). R2 establishes that entry-timing-redesigns produce real per-trade-expectancy gains at the price of cost-fragility. The diagnostic-only limit-at-pullback fill model showed BTC fill-model divergence Δexp +0.24 R between committed next-bar-open and intrabar limit fills — informative for any future paper/shadow phase as a backtest-vs-live realism flag.

---

## 4. Family-level diagnosis

### 4.1 What has been learned about exits

R3 alone is the cleanest, most robust, broadest-based improvement the project has produced. It cleared §10.3 paths (a) and (c) on both symbols at non-trivial magnitude, improved every regime-symbol cell, beat H0 in 7/10 fold-symbol cells, confirmed direction-of-improvement out-of-sample, was robust to slippage and stop-trigger source, and produced the project's first positive direction-symbol cell (ETH shorts).

The lesson: **H0's staged-trailing topology was actively destroying edge that existed.** Stage 3 risk reduction at +1.0 R, Stage 4 break-even at +1.5 R, and Stage 5 trailing at +2.0 R, combined with Stage 7 stagnation at 8 bars without +1.0 R MFE, were systematically converting potential winners into breakevens or losses. R3's two-rule terminal exit (fixed +2.0 R take-profit + unconditional 8-bar time-stop) captures that latent edge cleanly.

The **ceiling on exit-side improvement** appears to be R3's exact configuration. Phase 2j memo §D pre-committed the R3 sub-parameters (R-target = 2.0; time-stop = 8 bars) singularly, anchoring them to existing H0 stage-trigger thresholds. No subsequent phase has tested alternative R-targets or alternative time-stop horizons, and Phase 2p §J explicitly forbids that without a separate operator-authorized phase. The exit-axis is therefore at its committed singular configuration.

### 4.2 What has been learned about setup filters

R1a established that **compression-precedes-breakout is real on ETH** and **compression-bar selection on BTC produces post-breakout follow-through that does not extend**. The same percentile predicate, on the same v002 datasets, produces ETH V netPct +0.69% AND BTC V netPct −0.88% (n=4, 0% WR). Phase 2o §C diagnosed this as market-structure × directional-bias interaction.

The lesson: **setup-validity filters are symbol-specific.** A compression filter that works on ETH does not work on BTC under the same R-window, and the §1.7.3 BTCUSDT-primary lock makes ETH-favorable / BTC-unfavorable variants ineligible for v1 deployment. The practical consequence is that R1a-style setup filters cannot be promoted to baseline-of-record without either (a) lifting §1.7.3 (an operator-policy change) or (b) developing a regime-conditional R1a-prime that recovers BTC (Phase 2o §F.1, Phase 2p §F.1, both unspecified).

The **ceiling on setup-validity-axis improvement** under unchanged §1.7.3 is therefore: R1a is retained-for-future-hypothesis-planning, not promoted. No other setup-axis candidate is in the carry-forward set.

### 4.3 What has been learned about bias filters

R1b-narrow demonstrated that **bias-strength magnitude filtering can produce the strongest-formal §10.3 verdict** (first-time §10.3.a-on-both at magnitude) **without a corresponding absolute-edge gain**. The R3-anchor view is roughly neutral on BTC (Δexp_R3 −0.023); the improvement vs H0 is dominated by R3's exit-machinery contribution plus trade-count concentration. The post-2s joint interpretation — "bias-strength was not the missing mechanism" — captured this precisely.

The lesson: **the §10.3 framework's threshold mechanics can be cleared by trade-count concentration alone** when the underlying baseline (R3) already produces an absolute-edge improvement. A candidate that surgically selects a subset of R3's trades can clear §10.3.a-on-both even when its marginal contribution on top of R3 is approximately zero. The framework's discipline is not weakened by this — the §10.3 thresholds are **comparison metrics**, not absolute-edge metrics — but the methodological caution is: a §10.3.a clearance does not imply genuine per-trade-expectancy gain over the R3 baseline.

The **ceiling on bias-axis improvement** appears to be R1b-narrow's exact configuration. The remaining bias-axis candidate identified in Phase 2i (R1b-broad with regime-conditional bias) was excluded for high overfitting risk; revival would require evidence-grounded justification not yet developed.

### 4.4 What has been learned about entry timing

R2 demonstrated **two distinct, separable findings**:

- **Entry-timing structural redesign produces real per-trade-expectancy gain.** M1 +0.123 R on BTC intersection trades is the strongest mechanism-level pass any post-R3 candidate has produced. M3's mechanical R-distance reduction passes cleanly. The smaller-stop / larger-position-size geometry produces measurably better per-trade outcomes on the trades that fill.
- **Entry-timing structural redesign is slippage-fragile.** §11.6 FAILS at HIGH slippage on both symbols. The per-trade expectancy gain (+0.12 R on BTC) is approximately equal to the slippage-induced cost increase (~0.06 R per trade at HIGH; ~0.12 R per trade adverse-direction × directional-volume effects). The committed next-bar-open fill model produces the only path eligible for §10.3 governing evaluation; the diagnostic-only limit-at-pullback intrabar fill model shows BTC Δexp +0.24 R divergence — meaning the live-trading fill realism question is open and material.

The lesson: **entry-timing redesigns sit in a band where the edge can be wiped out by realistic cost variation.** This is a different ceiling from the exit-axis (where R3 was robust to slippage) or the setup-axis (where R1a was symbol-asymmetric). The entry-axis ceiling is **cost-realism-dependent** rather than market-structure-dependent.

The **ceiling on entry-axis improvement** under unchanged Phase 2f §11.6 is: R2's framework verdict is FAILED. The entry-axis cannot produce a deployable variant unless one of:
- The §11.6 HIGH-slippage threshold is revised based on documented Binance BTCUSDT futures slippage profile (an operator-policy decision; Phase 2w-B §11.3 Option 3).
- A different entry-axis variant produces a path that survives §11.6 at HIGH (no such candidate currently specified).

### 4.5 What has been learned about slippage / cost sensitivity

The slippage-sensitivity profile is informative about the **nature** of each candidate's edge:

| Candidate | LOW (0 bps) | MEDIUM (5 bps, committed) | HIGH (8 bps) | Cost-sensitivity profile |
|-----------|-------------|---------------------------|--------------|--------------------------|
| **R3** | BTC −0.139 / PF 0.719; ETH −0.271 / 0.561 | BTC −0.240 / 0.560; ETH −0.351 / 0.474 | BTC −0.445 / 0.359; ETH −0.549 / 0.316 | Cost-robust. Even at HIGH (3× MED), R3 is still better than H0 at MED. |
| **R1a + R3** | BTC −0.319 / 0.449; ETH −0.022 / 0.965 | BTC −0.420 / 0.355; ETH −0.114 / 0.833 | BTC −0.544 / 0.358; ETH −0.354 / 0.583 | Cost-monotone. ETH essentially break-even at LOW; BTC monotone-degraded. |
| **R1b-narrow** | BTC −0.196 / 0.654; ETH −0.174 / 0.690 | BTC −0.263 / 0.561; ETH −0.224 / 0.622 | BTC −0.389 / 0.445; ETH −0.371 / 0.452 | Cost-monotone. PROMOTES at HIGH on both symbols; framework-clearing across the band. |
| **R2 + R3** | BTC −0.180 / 0.973 (PROMOTE); ETH −0.481 / 0.366 (DISQ at LOW) | BTC −0.275 / 0.529 (PROMOTE); ETH −0.432 / 0.454 (PROMOTE) | BTC −0.473 / 0.315 (DISQ); ETH −0.705 / 0.256 (DISQ) | **Cost-fragile.** §11.6 gate FAILS. ETH disqualifies even at LOW (Δexp_H0 −0.006). |

Two cross-cutting observations:

1. **Exit-machinery improvements (R3) are cost-robust.** R3 captures a structural improvement in how trades are terminated; the magnitude of improvement is large enough to absorb realistic cost variation. The improvement is **economic-mechanism-driven** (replacing a destructive trailing topology with a fixed-R + time-stop terminal), not dependent on close-to-margin price geometry.
2. **Entry-axis improvements (R2) are cost-fragile.** R2 captures a per-trade expectancy gain through smaller-stop / larger-position-size geometry — but this gain operates within the slippage band itself. At HIGH slippage, the gain is consumed by cost. The improvement is **price-geometry-driven**, not economic-mechanism-driven.

The framework's §11.6 cost-sensitivity gate (Phase 2f §11.6 with thresholds preserved per §11.3.5) is therefore producing evidence-grounded discrimination between robust and fragile improvements — exactly the discipline it was designed for.

### 4.6 What has been learned about BTC vs ETH behavior

The **BTC/ETH asymmetry** is a stable family-level feature:

- ETH consistently shows stronger response to structural-redesign attempts. ETH produced the only positive V-window netPct results (R1a+R3 V +0.69%; R1b-narrow V +0.28%). ETH low-vol cells produced the only positive expR with PF > 1 (R1a+R3 ETH low-vol +0.281 / 1.353; R2+R3 ETH low-vol +0.091 / 1.115). ETH shorts produced the strongest direction-symbol cells (R1a+R3 ETH shorts +0.387 / 1.906; R1b-narrow ETH shorts +0.125 / 1.416).
- BTC shows narrower improvement margins, sample-fragile cells, and slippage-sensitivity. BTC R1a+R3 R-window §10.3.a barely fails (Δexp +0.039 < +0.10); BTC R1b-narrow per-fold sample sizes 0/2/1/2/3; BTC R2+R3 §11.6 fails. R3 alone is the only candidate whose BTC improvement is broad-based and robust.
- Phase 2o §C diagnosed the asymmetry as **market-structure × strategy interaction** (symbol-specific market behavior + directional-bias interaction), not a fixable rule defect.
- Phase 2i §1.7.3 BTCUSDT-primary lock makes ETH-favorable / BTC-unfavorable variants ineligible for v1 deployment.

The lesson: **the family's edge is more robustly demonstrable on ETH; BTC requires either more conservative structural commitment (R3-only) or accepting that BTC's edge sits at the margin of statistical detectability under the current framework.** The operator-policy choice between (a) BTCUSDT-primary deployment with R3-alone, (b) ETH-primary deployment with R1a+R3 / R1b-narrow / R2+R3, or (c) deferring deployment is exactly the choice §1.7.3 forecloses for v1. The asymmetry-evidence is preserved for any future operator-policy revision.

---

## 5. Has the V1 breakout family reached its useful ceiling under the current framework?

**Likely yes.**

The case for "ceiling reached" is structural, not opinion-driven:

1. **All four structural axes have been tested.** Exit (R3); setup-validity (R1a); bias-validity (R1b-narrow); entry-lifecycle (R2). Each axis has had one Phase-2j-style spec-writing phase, one §10.3 / §10.4 / §11.3 / §11.4 / §11.6-disciplined execution, and one comparison report. The post-Phase-2j carry-forward set (Phase 2i §3.1) is exhausted.
2. **The pattern across post-R3 candidates is one of diminishing absolute-edge return.** R3 produced a clean broad-based PROMOTE with substantial per-fold and per-regime improvement. R1a+R3 produced a mixed-PROMOTE (ETH-asymmetric). R1b-narrow produced the strongest-formal §10.3.a-on-both PROMOTE but with R3-anchor-neutral marginal contribution and 65–70% trade-count drop. R2+R3 produced framework FAILED via §11.6. The evidence is consistent with a candidate-level diminishing-returns curve in which the family's exit-axis edge (R3) is the dominant contributor and the post-R3 axes contribute smaller-and-smaller marginal gain that is increasingly absorbed by cost-realism, sample-fragility, or symbol-asymmetry.
3. **The absolute-edge gap has not closed.** Across all four candidates, R-window aggregate expR remains negative on both symbols. R3 BTC is the cleanest result and is at −0.240 R per trade. Closing that gap to positive territory under the current framework would require a structural improvement of magnitude ≥ +0.24 R per trade — which only R3 itself has produced (vs H0's −0.459 baseline). No subsequent candidate has produced an R3-displacing improvement of comparable magnitude.
4. **Phase 2h §11.1 stopping rule is partially met but ambiguously.** The stopping rule paraphrased: "abandon a family only when structural redesign has been honestly tried with a falsifiable hypothesis and produced its own clean negative". The arc has produced four structural-redesign attempts; one cleanly PROMOTED (R3); three produced PROMOTE-with-mechanism-caveat or framework-FAIL. None produced a clean negative §10.3 disqualification — but the pattern across the three post-R3 candidates is the *opposite* of an absolute-edge accumulation. The stopping rule was written assuming a clean disqualification would arrive; what arrived instead is **a methodologically-disciplined demonstration that no axis is producing absolute-edge gain on top of R3**.
5. **Phase 2t §3.3 explicitly noted R2 was the only remaining structural axis with a concrete deferred candidate.** R1a covered setup; R1b-narrow covered bias; R2 covered entry. Phase 2t §3.3 stated "R2 was the only remaining structural axis with a concrete deferred candidate after R1a (setup-shape) and R1b-narrow (bias-shape) were tested". With R2 now executed and FAILED, the carry-forward set is exhausted. Any new candidate would require either (a) a regime-conditional variant of one of the existing axes (R1a-prime, R1b-broad), all of which carry higher overfitting risk per Phase 2i §3.2, or (b) a structurally novel axis not yet enumerated.

The case against "ceiling reached" is non-trivial but narrower:

- A regime-conditional R1a-prime (Phase 2o §F.1, Phase 2p §F.1) is an **un-specified hypothesis** that could in principle recover R1a's ETH gain while avoiding the BTC degradation. The hypothesis is undeveloped; specifying it would require a Phase 2j-style §C-equivalent docs-only spec-writing phase. Whether such a spec would pass Phase 2i §1.7 binding test (rule-shape change vs parameter-tuning under another label) is unclear.
- An operator-policy revision of §11.6 HIGH-slippage threshold based on actual Binance BTCUSDT futures slippage profile (Phase 2w-B §11.3 Option 3) could in principle rehabilitate R2's framework verdict. The revision is operator-policy territory, not strategy-redesign — and the prior is that the threshold is correctly calibrated for unsupervised research; revision would require evidence not yet developed.
- Family-shift planning (Phase 2p §F.4) — moving to a non-breakout family — is the "ceiling reached" downstream consequence, not a contradiction to it.

**Net assessment:** the V1 breakout family has likely reached its useful ceiling under the current framework. R3 is the deployable variant; R1a / R1b-narrow / R2 are research-evidence-only. Further candidate-level structural redesigns are unlikely to produce R3-displacing results without operator-policy changes (lifting §1.7.3, revising §11.6, etc.) or a structurally novel axis not yet enumerated. The "likely" qualifier reflects that the ceiling assessment is evidence-based, not definitive — a future operator decision to develop a specific regime-conditional R1a-prime spec or to revise §11.6 based on cost-realism evidence could in principle re-open the family arc.

---

## 6. Next-option menu evaluation

The five mutually-exclusive options (one option must be chosen; "do nothing" is Option A).

### Option A — Remain paused

The project holds the consolidation state established by Phase 2p + the post-Phase-2w consolidation. R3 baseline-of-record stands. R1a / R1b-narrow / R2 stay in retained-research-evidence state. H0 remains framework anchor. No next phase is authorized. Future operator decisions resume the path when an evidence-grounded reason or a policy change produces one.

### Option B — One more narrowly-justified breakout-family research phase

A docs-only Phase 2j-style spec-writing phase for one specific evidence-grounded hypothesis. Most plausible candidates:

- **Regime-conditional R1a-prime** (Phase 2o §F.1, Phase 2p §F.1) — recover R1a's ETH gain while regime-gating away BTC degradation. Requires explicit per-symbol-regime predicate and singular sub-parameters per Phase 2j §C.6 / §11.3.5.
- **R1b-broad with regime-conditional bias** — Phase 2i §3.2 excluded for higher overfitting risk; revival would require renewed evidence-grounded justification.
- **R2-prime with operator-policy-revised §11.6** — depends on Option C outcome; not standalone.

### Option C — Independent slippage / cost-policy review

A docs-only operator-policy review of the framework's HIGH-slippage threshold (Phase 2f §11.6, currently 8 bps) in light of:

- R2's §11.6 failure pattern (BTC Δexp_H0 −0.014 at HIGH; ETH Δexp_H0 −0.230 at HIGH).
- R2's BTC fill-model divergence (Δexp +0.24 R between committed next-bar-open and diagnostic limit-at-pullback).
- Documentation of Binance USDⓈ-M BTCUSDT actual slippage profile (would require external evidence-collection, possibly from venue documentation, market-microstructure research, or third-party broker analytics — operator decides scope).

This is **not a strategy-redesign decision**; it is a **framework-calibration decision**. The output would be one of:

- Confirmation that 8 bps HIGH is correctly conservative for unsupervised research → R2's FAILED verdict consolidates.
- Evidence that 8 bps HIGH is too conservative for actual Binance live conditions → R2's framework verdict could be revised under the revised §11.6 threshold.
- Evidence that 8 bps HIGH is too loose → §11.6 tightens for future candidates.

### Option D — New strategy-family planning

A docs-only survey of candidate non-breakout families with falsifiable mechanism hypotheses compatible with the same v002 datasets (or motivating new v003 datasets). Phase 2p §F.4 enumerated example candidate families: mean-reversion in low-vol regimes; funding-rate arbitrage; cross-symbol relative momentum.

The output would be a candidate-family enumeration with pre-committed §10.3-style thresholds and a Phase 2j-style spec-writing path for one specifically-recommended next-family.

### Option E — Paper/shadow or Phase 4

Lift operator deferrals on paper/shadow or Phase 4 (runtime / state / persistence). Phase 4 begins operational scaffolding (runtime modes, dry-run adapter, persistence, dashboard hooks, alert routing, kill-switch wiring) without committing to live deployment. Paper/shadow runs the deployable variant (currently R3) on live market data without capital exposure.

---

## 7. Per-option evaluation

### Option A — Remain paused

- **What it answers:** Nothing new. Holds the post-Phase-2w consolidation state.
- **Why it may be useful:** Cheapest. Preserves discipline. Keeps every door open. Aligns with Phase 2p §H.1 + post-Phase-2w consolidation. No risk of treadmill behavior, premature deployment, or premature family-shift.
- **Why it may be dangerous:** No active research. If the family has any remaining useful evidence to extract (Option B, C), this option delays that. If the family has truly reached its ceiling and the right move is family-shift (Option D), this option also delays that.
- **Restriction violations:** None. Aligns with all current restrictions.
- **Recommended now?** **YES (primary recommendation).** See §8.

### Option B — One more narrowly-justified breakout-family research phase

- **What it would answer:** Whether a regime-conditional R1a-prime (or another specific candidate not yet specified) can produce a clean cross-symbol R3-displacement under unchanged framework discipline.
- **Why it may be useful:** Keeps the structural-redesign path alive cleanly. Forces explicit Phase 2i §1.7 binding-test decision before any execution. Documented failure is itself information.
- **Why it may be dangerous:** **Treadmill risk is now elevated.** Three structural-redesign candidates post-R3 have produced PROMOTE-with-caveats or FAILED. Authorizing a fourth without a specific operator-developed hypothesis risks producing another mixed result that doesn't move the family-ceiling question forward. The Phase 2o §F.1 regime-conditional R1a-prime hypothesis is **undeveloped** — no spec exists; specifying one purely from Phase 2x review is exactly the kind of "operator-policy decision under research framing" Phase 2p §H.4 explicitly does not authorize.
- **Restriction violations:** None (docs-only spec-writing phase). But the restriction *spirit* is violated if Option B is invoked without an independently-developed hypothesis grounding from the operator.
- **Recommended now?** **NO** — not recommended primary. Recommended *only as fallback if* the operator independently develops a falsifiable regime-conditional R1a-prime hypothesis or a comparable specific candidate.

### Option C — Independent slippage / cost-policy review

- **What it would answer:** Whether the §11.6 HIGH-slippage threshold (8 bps) is calibrated to Binance's actual BTCUSDT futures slippage profile, and consequently whether R2's FAILED verdict reflects a strategy-fragility finding or a framework-calibration artifact.
- **Why it may be useful:** R2's §11.6 failure is the single most consequential finding from Phase 2w. If the threshold is correctly calibrated, the FAILED verdict consolidates the family-ceiling assessment (§5). If the threshold is over-conservative, revising it could rehabilitate R2's framework verdict and re-open the entry-axis. Either outcome adds material information to the family-level decision. Low-risk: docs-only review; framework-calibration vs strategy-redesign is a clean separation; no parameter or threshold change without evidence.
- **Why it may be dangerous:** Risk of framework-discipline erosion if the review is invoked as a way to retroactively rehabilitate R2 without independent cost-realism evidence. The Phase 2f §11.3.5 binding rule (no post-hoc loosening) must be preserved verbatim — Option C is not "lower the threshold to clear R2"; it is "audit the threshold against external evidence". The output may well be "the threshold is correct as stated".
- **Restriction violations:** None inherent. But the review must explicitly forbid changing §11.6 without external Binance-cost-realism evidence; otherwise it becomes a framework-discipline shortcut.
- **Recommended now?** **CONDITIONAL — recommended as the highest-value next docs-only phase IF the operator wants any active path.** See §8.

### Option D — New strategy-family planning

- **What it would answer:** Which non-breakout strategy families are credible candidates with falsifiable mechanisms and §10.3-style threshold compatibility, and which one (if any) is the operator's preferred next research direction.
- **Why it may be useful:** Acknowledges the family-ceiling assessment from §5. Frees research capacity from a family that has been adequately characterized. Avoids treadmill behavior. Phase 2p §F.4 family-abandonment pre-conditions are partially-met (no clean-negative third-strike, but a structural ceiling pattern across three post-R3 candidates).
- **Why it may be dangerous:** **Premature relative to the evidence.** Option D treats the family as closed; the evidence supports "likely ceiling reached" but does not support "definitively closed". Option C (slippage/cost-policy review) is a precondition for confidently moving to Option D — without it, the family-ceiling assessment is partially confounded by an open framework-calibration question (R2's §11.6 failure). Authorizing Option D before Option C risks abandoning the family on a framework-calibration artifact rather than a strategy-fragility finding.
- **Restriction violations:** None. Docs-only family-survey phase is within scope.
- **Recommended now?** **NO** — recommended only after Option A or Option C clarity. Option D becomes the right move if (a) the operator independently confirms the family-ceiling assessment, and (b) Option C confirms §11.6 is correctly calibrated.

### Option E — Paper/shadow or Phase 4

- **What it would answer:** Operational-scaffolding readiness for R3 (Phase 4); or live-equivalent observability for R3 (paper/shadow).
- **Why it may be useful:** Builds runtime infrastructure on the strength of R3's evidence; allows operational reliability evidence to accumulate even if strategy-edge evidence is at its current ceiling.
- **Why it may be dangerous:** **Operator policy explicitly defers paper/shadow and Phase 4** per Phase 2p §F.2 / F.3 and the post-Phase-2w consolidation. Even R3's R-window expR is still negative (BTC −0.240); operationalizing a strategy with negative aggregate expectancy on the BTCUSDT live primary symbol — even at 0.25% risk and 2× leverage caps — would be a meaningful policy decision that requires operator-level deliberation outside Phase 2x scope. Premature relative to current operator policy.
- **Restriction violations:** **YES.** Direct violation of the operator restriction list in the Phase 2x brief: "No paper/shadow planning is authorized; No Phase 4 runtime/state/persistence work is authorized; No live-readiness or deployment work is authorized."
- **Recommended now?** **NO.** Forbidden by Phase 2x scope; cannot be recommended.

---

## 8. Recommended next operator decision

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### 8.1 Primary recommendation

**Remain paused.** This is **Option A** of §6.

The post-Phase-2w consolidation already established the right pause posture: R3 baseline-of-record locked; R1a / R1b-narrow / R2 retained as research evidence; H0 anchor preserved; framework discipline preserved; operational restrictions (paper/shadow, Phase 4, live-readiness) preserved. Phase 2x's family-level review confirms that this consolidation state is the right place to be at the post-Phase-2w boundary.

The §5 family-ceiling assessment supports a pause: the four structural axes have been tested; the carry-forward set is exhausted; the absolute-edge gap has not closed; the diminishing-returns pattern across post-R3 candidates is consistent with a structural ceiling. None of those findings produces an immediate evidence-grounded direction-change requirement. They produce a **clarified pause**: the operator now has more information about *what kind of pause* this is — it is a "family arc complete; carry-forward set exhausted; ceiling likely reached" pause, not a "next-candidate-pending" pause.

### 8.2 Fallback recommendation

If the operator judges that maintaining a stay-paused state without any active path is too inert, the highest-value next docs-only phase is **Option C — independent slippage / cost-policy review**.

Option C is the only option that:

- Produces material new family-level information (whether R2's §11.6 failure is calibration-driven or fragility-driven).
- Adds no strategy-redesign treadmill risk.
- Does not violate any current operator restriction.
- Is genuinely informative regardless of outcome (confirmation OR revision both clarify the family-ceiling assessment).
- Sits cleanly within the §11.3.5 binding rule (framework-calibration is operator-policy, not post-hoc loosening; the review is an audit, not a threshold change).

Option B (one more breakout-family research phase) is not recommended without an independently-developed hypothesis. Option D (new strategy-family planning) is not recommended before Option C clarity. Option E (paper/shadow or Phase 4) is not authorized.

### 8.3 What the recommendation explicitly does NOT recommend

- **No subsequent execution phase.** Phase 2x does not authorize R1a-prime, R1b-broad, R2-prime, or any other execution candidate.
- **No paper/shadow planning.** Phase 2p §F.2 / post-Phase-2w deferrals stand.
- **No Phase 4 (runtime / state / persistence) work.** Phase 2p §F.3 / post-Phase-2w deferrals stand.
- **No live-readiness or deployment work.** Operator policy explicit.
- **No threshold change.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds preserved per Phase 2f §11.3.5.
- **No project-level lock change.** §1.7.3 BTCUSDT-primary, ETHUSDT research-only, one-position max, 0.25% risk, 2× leverage cap, mark-price stops, v002 datasets — all preserved.
- **No family-shift authorization yet.** Option D becomes appropriate after Option C clarity OR after operator independently judges family-ceiling confirmed.
- **No closure of any candidate's research-evidence status.** R1a / R1b-narrow / R2 stay retained-as-research-evidence, not closed.

### 8.4 What would change this recommendation

- **Operator independently develops a falsifiable regime-conditional R1a-prime spec** → switch primary → Option B.
- **Operator independently judges §11.6 calibration question is irrelevant given current evidence** → Option C is dropped; Option A or Option D becomes primary depending on operator's family-ceiling judgment.
- **Operator independently lifts paper/shadow restriction** based on accumulated R3 evidence → Option E becomes available; not recommended by Phase 2x.
- **Operator independently authorizes family-shift planning** without Option C precedent → Option D becomes primary; Phase 2x notes that without Option C, the family-ceiling judgment is partially confounded by open framework-calibration question.
- **Discovery of an implementation issue or a documentation inconsistency in prior phase records** that requires a docs-only correction phase before any further strategy work.

---

## 9. Explicit project-state preservation statement

This memo explicitly preserves the following project state per the Phase 2x operator brief:

- **R3 remains the baseline-of-record** per Phase 2p §C.1. Locked sub-parameters: `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`. Same-bar priority STOP > TAKE_PROFIT > TIME_STOP. Phase 2j memo §D.6 invariants preserved.
- **H0 remains the formal framework anchor** per Phase 2i §1.7.3. All §10.3 / §10.4 evaluations across all phases anchored on H0; no anchor shift.
- **R1a (volatility-percentile setup predicate) remains research evidence only.** Retained-for-future-hypothesis-planning per Phase 2p §D. Not the current default. Not the deployable path. §1.7.3 BTCUSDT-primary lock makes ETH-favorable / BTC-degrading variants ineligible.
- **R1b-narrow (bias-strength magnitude predicate) remains research evidence only.** Retained per Phase 2s §13. Not the current default. Not the deployable path.
- **R2 (pullback-retest entry-lifecycle topology) remains research evidence only.** Retained per Phase 2w §16.3 framing applied. Framework verdict FAILED — §11.6 cost-sensitivity blocks. Not the current default. Not the deployable path.
- **No paper/shadow planning is authorized.** Phase 2p §F.2 / post-Phase-2w consolidation deferrals stand.
- **No Phase 4 (runtime / state / persistence) is authorized.** Phase 2p §F.3 / post-Phase-2w consolidation deferrals stand.
- **No live-readiness work is authorized.** No deployment, no exchange-write capability, no production keys, no §11.6 threshold change without independent evidence-grounded operator-policy review.
- **No project-level locks change.** §1.7.3 BTCUSDT-primary, ETHUSDT research/comparison only, one-symbol-only, one-position max, 0.25% risk per trade, 2× leverage cap, mark-price stops, v002 datasets — all preserved verbatim.

---

## 10. GO / NO-GO recommendation for any next docs-only phase

**NO-GO** for any next strategy-redesign execution phase, paper/shadow planning, Phase 4 work, live-readiness work, deployment work, threshold change, or project-lock change.

**NO-GO** for Option B (one more breakout-family research phase) without an operator-independently-developed falsifiable hypothesis.

**NO-GO** for Option D (new strategy-family planning) without Option C clarity OR operator-independent family-ceiling confirmation.

**NO-GO** for Option E (paper/shadow or Phase 4) per current operator restrictions.

**GO (provisional)** for **Option A — remain paused** as the primary recommendation. This is the natural extension of the post-Phase-2w consolidation; no new phase is started; the operator decides any future direction-change independently.

**GO (provisional, fallback only)** for **Option C — independent slippage / cost-policy review** as a docs-only operator-policy phase **IF** the operator wants any active path during the pause. Option C is narrowly bounded (framework-calibration only; no threshold change without external Binance-cost-realism evidence; no parameter change; no candidate change), explicitly forbids §11.3.5 violations, and produces material new family-level information regardless of outcome.

The recommended next operator decision is therefore one of:

1. **Stay paused (Option A).** No next phase. Recommended primary.
2. **Authorize Option C (slippage/cost-policy review).** Recommended fallback if the operator wants any active path.
3. **Independently develop a regime-conditional R1a-prime hypothesis** → then authorize Option B (docs-only spec-writing). Not recommended by Phase 2x; conditional on operator hypothesis development.

Phase 2x explicitly does **not** authorize execution of any kind. The next docs-only phase, whichever it is, becomes a separate operator decision.

---

**End of Phase 2x family-level review memo.** Sections 1–10 complete. The V1 breakout family arc has likely reached its useful ceiling under the current framework: R3 is the only clean broad-based PROMOTE; R1a / R1b-narrow / R2 are PROMOTE-with-caveats or FAILED with mechanism-partial-support; the absolute-edge gap has not closed; the carry-forward set is exhausted. Recommendation: stay paused after Phase 2x (Option A primary); authorize Option C (slippage/cost-policy review) only as fallback if any active path is desired. NO-GO for any execution / paper-shadow / Phase 4 / live-readiness / deployment / threshold-change / project-lock change. R3 remains baseline-of-record; H0 remains framework anchor; R1a / R1b-narrow / R2 remain research evidence only. No Phase 2x-authorized successor phase. Awaiting operator review.
