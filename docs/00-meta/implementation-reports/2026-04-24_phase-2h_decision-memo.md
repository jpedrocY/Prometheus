# Phase 2h — Post-Wave Decision Memo

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2h/post-wave-decision-memo` (created from `main` at `0b67357` — verified clean working tree, `main` synchronized with `origin/main` after the Phase 2g PR #8 merge)
**Author:** Claude Code (Phase 2h)
**Date:** 2026-04-24
**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict); Phase 2h Gate 1 plan §§ 6–14.A.
**Scope:** Decision/planning memo only. No code, no new backtests, no new variants, no data downloads, no Binance API calls, no MCP/Graphify, no `.mcp.json`, no Phase 4 work, no edits to `docs/12-roadmap/technical-debt-register.md`.

This memo presents three parts:

- **Part 1 — Factual recap.** Locked facts from Phase 2e baseline, Phase 2f review, Phase 2g wave-1 execution.
- **Part 2 — Diagnosis and decision-options analysis.** What wave 1 ruled out / didn't, four candidate next phases (A wave 2 / B structural redesign / C new family / D Phase 4) compared on pros, cons, wasted-effort risk, and expected value of information, plus explicit handling of H-B2's near-pass and a methodology / anti-overfitting section.
- **Part 3 — Recommendation (provisional).** Primary path, fallback, and the explicit conditions that would change either choice ("What would change this recommendation").

---

# Part 1 — Factual recap

## 1.1 Phase 2e baseline (FULL window, untouched control)

Source: `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md`.

- Window: 2022-01-01 → 2026-04-01 UTC (51 months); v002 manifests; zero invalid windows.
- BTCUSDT: 41 trades, WR 29.27%, expR −0.43, PF 0.32, net −3.95%, max DD −4.23%, L/S 21/20, exits STOP 22 / STAGNATION 19 / TRAIL 0.
- ETHUSDT: 47 trades, WR 23.40%, expR −0.39, PF 0.42, net −4.07%, max DD −4.89%, L/S 18/29, exits STOP 35 / STAGNATION 11 / TRAIL 1.
- Funnel dominant rejections (both symbols): `no valid setup` ~57–58%, `neutral bias` ~37%, `no close-break` ~5%; trailing filters each <0.5%.
- Sizing never bound at Phase 3 defaults (`risk=0.0025`, `risk_usage=0.90`, `max_leverage=2.0`, `notional_cap=100_000`, `taker=5bps`, `slippage=MEDIUM`, `equity=10_000`).
- Mark-price gap impact on held-position intervals: zero trades affected on either symbol.

This is the descriptive baseline. It is not promotion or live-readiness evidence; it is the permanent control against which any variant is compared.

## 1.2 Phase 2f review conclusions (committed)

Source: `docs/00-meta/implementation-reports/2026-04-24_phase-2f_strategy-review-memo.md`, `2026-04-24_phase-2f_gate-1-plan.md`.

- Filter inventory + structural/parametric classification of 25 strategy elements (Phase 2f §7.3).
- Six new GAP entries: GAP-20260424-030..035 (4 OPEN strategy items + 2 RESOLVED verification-only).
- Pre-declared promotion / disqualification thresholds:
  - **§10.3 promotion**: a variant is a candidate if (a) Δexp ≥ +0.10 R/trade AND ΔPF ≥ +0.05, OR (b) Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse by > 1.0pp, OR (c) exit-model bake-off strictly dominates baseline on both expR and maxDD.
  - **§10.3 disqualification floor**: any variant with worse expR, worse PF, |maxDD| > 1.5× baseline, broken funnel invariant, or failed conformity check is disqualified regardless of any promotion path.
  - **§10.4 hard reject**: trade count rises AND (expR < −0.50 OR PF < 0.30) — rejection regardless of sample size.
  - **§11.3 no-peeking discipline**: rank on R only, top 1–2 to V, no re-rank, no iterative peeking, pre-declared thresholds.
  - **§11.4 ETH-as-comparison**: BTC must clear; ETH must not catastrophically fail; ETH-only wins do not qualify a variant on BTC.
  - **§11.6 cost-sensitivity**: any variant clearing §10.3 on MEDIUM slippage must also be run on LOW and HIGH; HIGH-slippage inversion demotes to "fragile".
- Wave-1 cap: ≤ 4 single-axis variants; ≤ 1 exit/management variant per wave.
- Selected wave-1 set: H-A1 (setup window 8 → 10), H-B2 (expansion 1.0 → 0.75 × ATR20), H-C1 (HTF EMA 50/200 → 20/100), H-D3 (break-even +1.5R → +2.0R).

## 1.3 Phase 2g wave-1 result (committed)

Source: `docs/00-meta/implementation-reports/2026-04-24_phase-2g_wave1_variant-comparison.md`, `2026-04-24_phase-2g_gate-2-review.md`.

R-window headline (entries filtered to R = 2022-01..2025-01):

| Variant | BTC trades / WR / expR / PF / netPct / maxDD                          | ETH trades / WR / expR / PF / netPct / maxDD                          |
|---------|-----------------------------------------------------------------------|-----------------------------------------------------------------------|
| H0      | 33 / 30.30% / −0.459 / 0.26 / −3.39% / 3.67%                          | 33 / 21.21% / −0.475 / 0.32 / −3.53% / 4.13%                          |
| H-A1    | 13 / 15.38% / −0.831 / 0.10 / −2.42% / 2.21%                          | 11 / 18.18% / −0.360 / 0.49 / −0.89% / 1.75%                          |
| H-B2    | 69 / 30.43% / −0.326 / 0.43 / −5.07% / 5.53%                          | 57 / 24.56% / −0.440 / 0.35 / −5.65% / 6.53%                          |
| H-C1    | 30 / 26.67% / −0.499 / 0.24 / −3.35% / 3.28%                          | 32 / 15.62% / −0.495 / 0.29 / −3.56% / 3.99%                          |
| H-D3    | 33 / 30.30% / −0.475 / 0.25 / −3.51% / 3.79%                          | 33 / 21.21% / −0.491 / 0.31 / −3.64% / 4.20%                          |

Per-fold consistency (Phase 2f §11.2 5-rolling-folds): no variant produces a positive expR on **any** BTC test fold. On ETH only H0 F1 (+0.39 from 8 trades) is a credible positive sub-period; H-A1 F1's +1.94 is from a single trade and not sample-size-credible.

§10.3 / §10.4 verdict: **all four variants disqualified on BTC**. H-A1 / H-C1 / H-D3 worsen expR and PF; H-B2 narrowly exceeds the |maxDD| > 1.5× veto (ratio 1.505x). No V-window run, no slippage sensitivity, no stop-trigger sensitivity (all conditional on §10.3 promotion per §11.3 / §11.6).

## 1.4 What the project has proved technically

- The data layer (v002 manifests, 51-month coverage, mark-price + funding joins) is research-credible.
- The backtester is deterministic at fixed inputs and reproduces baseline numbers on R-window subsets bit-for-bit.
- The variant-config + stop-trigger-source infrastructure works and exists for any future approved wave.
- Pre-declared §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds applied without post-hoc adjustment produce a clean, defensible verdict (REJECT ALL).

## 1.5 What remains unresolved strategically

- Is the locked v1 breakout family viable on BTCUSDT/ETHUSDT 15m + 1h with v002 data? Wave 1 says "not on these four axes"; it does not say "not at all".
- Are exit-model decisions material? Wave 1 left H-D6 (fixed-2R / fixed-3R / staged+trailing baseline / opposite-signal exit-model bake-off) entirely untested per the operator's "≤ 1 exit variant per wave" cap.
- Are bundled variants justified? Phase 2f §9.1 forbids them in single-axis wave 1; a future bundled wave would require explicit deviation approval.
- Is there a structural redesign axis (setup-pattern definition, bias-regime detection, entry-timing rule) that would not just tweak parameters but change the strategy's geometry?

---

# Part 2 — Diagnosis and decision-options analysis

## 2.1 What wave 1 actually ruled out (single-axis only, on these four axes, on this data)

- **Setup-window length is not the binding parameter** — H-A1's longer window collapses trade frequency without recovering edge (BTC trades 33→13, expR worsens to −0.831). The dominant 58% "no valid setup" rejection is not primarily a length problem; it's a range-width / drift-cap / regime problem.
- **HTF EMA pair speed is not the binding parameter** — H-C1's faster pair (20/100) is marginally worse on both symbols, not better. The 37% "neutral bias" rejection isn't fixed by faster trend tracking.
- **Break-even threshold timing is not the binding parameter** — H-D3 (+1.5R → +2.0R) produced essentially identical entry/exit counts and marginally worse expR. Most trades stop out before reaching break-even territory; pushing the threshold later doesn't move the needle.

## 2.2 What wave 1 did NOT rule out

- **Trigger expansion does carry signal**: H-B2 added 109% more BTC trades while improving expR by +0.133 R and PF by +0.17. The veto was on |maxDD| ratio (1.505x of baseline), not on edge. This is a genuine non-noise signal about trigger looseness — but the proportional-DD scaling is also real.
- **Other entry-side axes are entirely untested**: H-A2 (range-width ceiling 1.75 → 2.00), H-A3 (drift cap 0.35 → 0.50), H-B1 (breakout buffer 0.10 → 0.05/0.15), H-B3 (close-location 25% → 35%), H-C2 (slope-rule definition resolution per GAP-031), H-C3 (slope window).
- **Exit-side axes are almost entirely untested**: H-D1 (stop buffer), H-D2 (stop-distance band), H-D4 (trailing multiplier 2.5 → 2.0/3.0), H-D5 (stagnation-window timing), and most importantly **H-D6 (full exit-model bake-off: fixed-2R, fixed-3R, staged+trailing baseline, opposite-signal)** — the operator's wave-1 cap of "1 exit variant" reduced the exit search to H-D3 alone.
- **Bundled variants are entirely untested**, by Phase 2f §9.1 design.
- **Structural axes** (setup-pattern definition, bias-regime detector, entry-timing rule, exit-philosophy class) are entirely untested by definition — they were classified Structural in Phase 2f §7.3 and thus excluded from wave-1 scope.

## 2.3 What the evidence pattern suggests

Most likely interpretation, ranked by support strength:

1. **Edge problem dominates parameter-tightness problem on the tested axes.** H0 has negative expR on every BTC fold of every wave-1 run. Single-axis nudges don't move that. (HIGH confidence.)
2. **Trigger may be modestly too restrictive — but only relevant if exit/risk machinery can absorb the proportional drawdown increase.** H-B2 demonstrated this both ways: edge improves with looser trigger; drawdown scales proportionally. (MEDIUM confidence; would require exit-model evidence.)
3. **Exits may be undertuned** — H-D3 was a minor knob; H-D6 would have been the right test for whether exits matter. We don't know yet. (MEDIUM confidence on the gap; UNKNOWN on the answer.)
4. **Setup definition (not length) and HTF bias definition (not speed) may be the structural issues** — but no test has separated structural from parametric in those layers. (LOW confidence; would require a redesign step.)

This does **not** imply: the strategy family is broken; the breakout-continuation thesis is wrong; live deployment is even potentially viable. None of those are supported by current evidence. The honest reading is "single-axis parameter changes on this spec do not produce a promoted variant on this data", with one promising-but-vetoed signal.

## 2.4 Option A — Wave 2 inside the same breakout family

**What it would look like.** Another wave of ≤ 4 single-axis variants drawn from the untested axes in §2.2. Per Phase 2f §9.1 still single-axis; per the Phase 2g operator brief still no extra variants beyond approved.

**Hypotheses still justified.**
- **H-D6 (exit-model bake-off)** — *strongest case*. Almost entirely untested in wave 1 by design. Tests fundamentally different exit philosophies (fixed-target, opposite-signal, staged+trailing baseline) rather than one threshold tweak. Most likely to produce a genuinely informative result whether positive or negative.
- **H-A2 (range-width ceiling 1.75 → 2.00)** — relaxes setup without H-A1's frequency-collapse problem; a complementary test of the "no valid setup" 58% rejection.
- **H-B1 (breakout buffer 0.10 → 0.05)** — a smaller, more conservative version of H-B2's "trigger looser" thesis that may not blow up |maxDD| as severely.

**Should be excluded from a wave 2.**
- More setup-window-length variants (H-A1 already showed length isn't it).
- More HTF-EMA-speed variants (H-C1 already showed speed isn't it).
- More break-even threshold variants (H-D3 already showed threshold timing isn't it).
- **H-B2-bundled-with-tighter-stop-band**: this is the textbook "rescue a near-pass with one more knob" pattern that Phase 2f §11.3.5 was designed to forbid. Strongly out of scope.

**Bundled variants justified?** No, not in a wave 2. Phase 2f §9.1 still applies. A bundled wave is a separate operator-approval question.

**Evidence threshold to justify trying wave 2.** A hypothesis that has a clear non-result-driven motivation — i.e., it tests an axis we genuinely don't know about (H-D6 above all), not an axis we already know about and want to retune.

| Aspect | Detail |
|---|---|
| Pros | Reuses existing infrastructure; H-D6 covers a major untested axis; small marginal cost |
| Cons | Risk of single-axis-wave-treadmill; even with H-D6, evidence may again say "doesn't work on this spec" |
| Risk of wasted effort | MEDIUM-LOW (high info value of H-D6); MEDIUM (entry-axis follow-ups) |
| EVI | HIGH for H-D6 specifically; LOWER for entry-axis follow-ups |

## 2.5 Option B — Structural breakout-strategy redesign

**What "structural" means here.** Not "different parameter values" — different rule shapes:

- Different **setup-pattern definition** (e.g., volatility-contraction pattern measured by Bollinger-band squeeze or ATR-percentile compression, instead of consolidation-range-width).
- Different **bias definition** (e.g., regime-switch detector or volatility-adjusted bias, instead of EMA-pair + slope).
- Different **entry-timing rule** (e.g., breakout retest or pullback-from-breakout, instead of breakout-bar close).
- Different **exit-philosophy class** (e.g., dynamic-trail by realized volatility, instead of static ATR-mult trail).

**Whether the current family should be redesigned before more parameter tests.** Wave-1 evidence is consistent with "parameter-level fixes don't move the needle on this spec", which is a reasonable trigger for a structural rethink. A redesign is also the cleanest place to honestly reckon with what regime/edge thesis the strategy is actually claiming.

**Most-justified redesign axes** (to surface in 2i, not in 2h itself):

- Setup-pattern reformulation as the primary candidate (the 58% "no valid setup" dominant rejection is the obvious first thing a redesign should target).
- Exit-philosophy class change as a secondary candidate (H-B2's "more trades + worse drawdown" hint suggests the exit machinery may be the binding constraint on a less-restrictive trigger).
- Bias formulation change as a tertiary candidate (less evidence; but the 37% neutral-bias rejection is the second-largest funnel bucket).

| Aspect | Detail |
|---|---|
| Pros | Reckons honestly with wave-1 evidence; produces a falsifiable redesign hypothesis; preserves discipline |
| Cons | More upfront thinking; risk of designing in a vacuum |
| Risk of wasted effort | MEDIUM (mitigated by pre-declared falsifiability) |
| EVI | HIGH if redesign is structural; LOW if it produces a relabeled parameter set |

## 2.6 Option C — Different research direction (new strategy family)

**What it would look like.** A different family on the same v002 datasets:

- Mean-reversion in low-volatility regimes (uses same data, opposite trigger logic).
- Funding-rate arbitrage (already have funding-event data; close to operationally feasible).
- Cross-symbol relative-momentum (BTC vs ETH; uses both symbols already loaded).
- Volatility-regime-aware ensemble (combines strategies).

**Whether the evidence justifies this now.** Not yet. Wave-1 evidence supports "parameter-level fixes don't work on this spec"; it does NOT support "the breakout family is wrong on this data". Skipping straight to a new family without first honestly reckoning with the breakout family's structural redesign is premature.

**Compatibility with existing infrastructure.** Each candidate is reasonably compatible with the data layer (same v002 datasets); none reuses the v1 strategy spec without invalidating it.

| Aspect | Detail |
|---|---|
| Pros | Resets the question; uses existing data; may unlock different edge classes |
| Cons | Premature without first exhausting Option B; throws away v1 spec investment |
| Risk of wasted effort | HIGH if invoked now |
| EVI | HIGH only after Option B is honestly tried |

## 2.7 Option D — Phase 4 (runtime / state / persistence) anyway

**What it would look like.** Build the operational-safety core (runtime state model, persistence, kill switch, reconciliation states, SQLite runtime DB, safe-mode startup) per the Phase 4 spec in `ai-coding-handoff.md` §"Phase 4 — Risk, State, and Persistence Runtime".

| Aspect | Detail |
|---|---|
| Pros | Decoupled from strategy debate; required for any future paper/shadow/live |
| Cons | Premature commitment to operational plumbing while strategy direction is unsettled |
| Risk of wasted effort | LOW for strategy-agnostic parts; MEDIUM-HIGH for strategy-coupled parts |
| EVI | LOW on strategy question; MEDIUM-HIGH on operational-readiness question |

## 2.8 Recommended decision criteria (what would justify each path)

A future Phase 2i should be **Wave 2** if and only if:

- a hypothesis can be stated that tests an axis NOT covered in wave 1 (e.g., H-D6),
- the hypothesis is single-axis (no bundled variants in wave 2 either, unless §9.1 deviation is separately approved),
- it is NOT a result-driven retrofit of H-B2's veto (no "H-B2 + tighter stop-band" rescue variants),
- the variant-comparison framework (§10.3 / §10.4 / §11.3) is reused unchanged, with the fold-scheme clarification per the new GAP entry,
- expected-value-of-information is genuinely high on a question the project hasn't already answered.

A future Phase 2i should be **Structural Redesign** if and only if:

- the redesign target is a rule shape, not a parameter value,
- it produces a falsifiable hypothesis with pre-declared success criteria,
- it inherits the Phase 2f §10.3 / §10.4 / §11.3 discipline for any subsequent execution,
- the spec change is documented before any code work begins.

A future Phase 2i should be a **Different Strategy Family** only after Option B has been honestly tried. Wave-1 evidence alone does not justify family abandonment.

A future phase should be **Phase 4** only if the operator explicitly accepts that operational infrastructure will be built without strategy-edge confirmation. Current operator policy has been against this; this memo does not propose changing it.

## 2.9 Explicit handling of H-B2's near-pass

H-B2 cleared §10.3.a (Δexp = +0.133, ΔPF = +0.17 on BTC; smaller positives on ETH) and was vetoed by §10.3 disqualification on |maxDD| > 1.5× baseline (ratio 1.505x). This requires careful, explicit handling:

- **Is the near-pass a genuine signal worth targeted follow-up?** Yes, the edge improvement is non-trivial (+0.133 R/trade is materially larger than typical noise on a 33-trade baseline). But the proportional drawdown scaling is also real, and a Phase 2f §10.3 disqualification on a binding tail-risk threshold is binding.
- **Is a bundled follow-up around H-B2 justified?** No. "H-B2 + tighter stop-distance band" is the canonical "rescue a near-pass with one more knob" pattern. Pursuing it after seeing the wave-1 result is exactly what Phase 2f §11.3.5 forbids ("operators cannot tighten or loosen [the thresholds] after seeing results"). A bundled variant motivated by the H-B2 result is by definition result-driven retrofitting.
- **What guardrails would be required if H-B2-related follow-up is ever recommended?** It would have to come from a structural redesign (Option B) that has been justified independently of H-B2's near-pass — i.e., a redesign that would be motivated even if H-B2 had cleanly failed. Anything else is post-hoc rationalization.
- **Where the H-B2 signal legitimately informs future work.** As a *diagnostic input* into Option B's redesign: any breakout-family redesign should anticipate that loosening the trigger increases drawdown roughly proportionally, and design exit/risk machinery to handle that. This is a structural design constraint, not a permission slip for a bundled wave-2 variant.

## 2.10 Anti-overfitting / methodology

### 2.10.1 Avoiding "just one more tweak"

The strongest anti-pattern after a near-pass is "the next variant will fix it". Phase 2h treats wave-1's REJECT-ALL outcome as a stop signal for single-axis parameter search **on the four tested axes** (H-A1, H-B2, H-C1, H-D3). Future hypotheses must come from **untested axes** (§2.2) or from **structural redesign** (Option B), not from re-tweaking the same axes with adjusted bounds.

### 2.10.2 When a negative result should stop a family

Wave 1 produced a 4/4 disqualification on BTC. That alone is not sufficient evidence to abandon the breakout family — it ruled out four single-axis paths, not the family. The disciplined stopping rule is: a family is abandoned only when (a) structural redesign has been honestly tried with a falsifiable hypothesis and produced its own clean negative, OR (b) a clearly better candidate family is justified on its own merits. Neither applies yet.

### 2.10.3 Sample segmentation / alternative scoring (analytic enhancements for a future phase, not 2h)

Wave 1 used per-symbol full-R metrics + per-fold consistency (Phase 2f §11.2 5-rolling-folds). This worked. Additional analytics that could inform future waves *without* requiring new runs:

- **Regime tagging on existing trade logs**: classify each trade by realized 1h volatility regime (low / medium / high) and compute per-regime expR. Wave-1 fold tables already hint at strong regime dependence.
- **MFE distribution analysis on existing logs**: look at where in the trade lifecycle pnl is captured; tells whether exits truly bind.
- **Per-direction long/short asymmetry**: Phase 2g headline shows L/S splits but didn't decompose expR by direction.

These are analytic enhancements for the eventual Phase 2i memo or execution wave; **not** Phase 2h itself.

### 2.10.4 Fold-scheme ambiguity

Phase 2f §11.2 said "five rolling folds of 12-month train / 6-month test, stepping 6 months on R". The strict mathematical reading produces only 4 folds entirely inside R; 5 folds requires fold 1 to start at month 6 with a 6m partial-train front edge. Phase 2g resolved this inline and committed to a permanent record in the comparison report §3 + Gate 2 review §7. This memo recommends logging this as **GAP-20260424-036** for permanent ambiguity-log capture. No spec edit is proposed in 2h; the ambiguity log entry is sufficient documentation for future waves to inherit a clear interpretation.

### 2.10.5 Other methodology items

- §10.3 disqualification floor's "any expR worsens / any PF worsens" was strict-but-correct; no proposal to soften it.
- §10.4's "rising trade count" gating was correct; no proposal to change it.
- §11.4 ETH-as-comparison rule was correct; no proposal to change it.
- The pre-declared-thresholds discipline (§11.3.5) is binding and was honored; no proposal to weaken it.

---

# Part 3 — Recommendation

## 3.1 Final recommendation (provisional; subject to operator/ChatGPT review)

This recommendation is **provisional and evidence-based, not definitive**. It is a judgement about the highest-value next research step given the evidence currently in hand. It is explicitly **not** any of the following:

- It is **not** a claim that Wave 2 is permanently ruled out. Wave 2 remains a legitimate path; the recommendation is only that, given current evidence, a structural redesign is the higher-value next step.
- It is **not** a claim that the breakout family is already disproven. Wave-1 evidence rules out four single-axis paths on this spec on this data; it does not rule out the family.
- It is **not** a recommendation against further parameter exploration in principle. It is a recommendation against single-axis parameter exploration on the four already-tested axes specifically.

With those caveats explicit:

**Primary (provisional): Option B — Phase 2i: Structural Breakout Redesign Planning (docs-only).**

Rationale: Wave-1 evidence is consistent with "parameter-level fixes don't move the needle on this spec on these axes". Continuing single-axis search on the same axes risks fitting noise; re-trying H-B2's near-pass via a bundled wave is exactly the post-hoc rationalization §11.3.5 forbids. A structural redesign forces honest reckoning with the strategy's edge thesis, produces a falsifiable redesign hypothesis with pre-declared success criteria, and either yields a stronger spec to test or itself produces clean evidence that the family should be set aside. It is also a docs-only phase — same low-risk, low-cost surface as Phase 2f.

**Secondary (fallback, provisional): Option A — Phase 2i: narrow Wave 2 with H-D6 exit-model bake-off as the centerpiece.**

Rationale: If the operator/ChatGPT judges that more execution evidence is needed before committing to a structural redesign, the highest-value-of-information variant is H-D6 (fixed-2R / fixed-3R / staged+trailing baseline / opposite-signal exit) — the major axis untested by wave 1's "≤ 1 exit variant" cap. A wave 2 narrowly bounded to H-D6 plus at most one untouched entry axis (H-A2 or H-B1 — not H-B2 retest, not H-A1/H-C1/H-D3 retest) would fill the largest evidence gap before any redesign. Bundled variants remain forbidden.

**Phase 4 stays deferred** per existing operator policy. This memo does not propose advancing it.

## 3.2 Why this recommendation and not Option A as primary

The choice between Option A primary and Option B primary is not obvious. The argument for Option A as primary: H-D6 is a clear evidence gap; running it costs little; the result is high-information whatever it shows. The argument for Option B as primary (which the recommendation takes): wave-1 evidence already supports "parameter-level fixes don't work on these axes" with three of four variants disqualified for the ordinary "worse expR / worse PF" reasons, and one (H-B2) on a binding tail-risk threshold; the honest next step is to ask "what would actually produce edge here?" which is a structural question, not a parameter-search question. Running H-D6 first risks producing yet another "doesn't move the needle" result and pushing the structural conversation further out. **Option B-then-A is more disciplined than A-then-B given current evidence.**

The operator may legitimately prefer the secondary as primary; the memo presents both clearly and the operator chooses.

## 3.3 What would change this recommendation

The recommendation is provisional. The following kinds of evidence or reasoning would justify switching paths:

### Switch from Option B (primary) to Option A (secondary as primary)

- A reasoned argument that the H-D6 exit-model gap should be filled before any structural redesign because exit-model results would directly inform what kind of structural redesign is justified — i.e., if H-D6 shows fixed-2R or opposite-signal exits dramatically reshape the result, the structural redesign should be exit-led; if not, redesign should be entry-led.
- A reasoned operator preference for execution evidence over additional structural reasoning at this stage.
- Identification of an additional untested low-risk axis where the cost of running is small relative to the information value.
- An ambiguity in the H-B2 result that further single-axis testing would resolve cheaply.

### Switch from Option B to Option C (different family, escalation)

- New evidence (e.g., from regime decomposition of existing wave-1 trade logs) that shows the breakout-continuation thesis is structurally incompatible with the BTCUSDT/ETHUSDT 15m + 1h regime in the v002 window — specifically, that no realistic redesign of setup / trigger / bias / exit produces a positive-expectancy expectation on this data.
- A clearly more justified alternative family (e.g., funding-rate arbitrage with a credible edge thesis) that compatible-tests on the same v002 datasets.
- An honest reckoning that structural redesign of the breakout family has been tried and produced its own clean negative.

### Switch from Option B (or any 2i option) back to "defer" (no new phase)

- Operator decision to pause strategy work and prioritize a different operational concern (e.g., security review, host-hardening prep, documentation cleanup) without committing to either Phase 2i or Phase 4.
- Discovery of a documentation inconsistency in the prior phase records that requires a docs-only correction phase before any further strategy work.
- A new operator restriction (timing, capital, scope) that makes the current options materially less attractive.

### Switch to Option D (Phase 4) ahead of any 2i strategy work

- Explicit operator policy change that operational infrastructure should be built without strategy-edge confirmation. Current policy is against this; this memo does not propose changing it. If the operator updates that policy independently, Phase 4 becomes available immediately and this memo's recommendation does not block it.

## 3.4 What this memo does NOT propose

To keep the boundary explicit: this memo does **not** propose any of the following.

- Any code change, test addition, or backtest run.
- Any threshold tightening or loosening on §10.3 / §10.4 / §11.3 / §11.6.
- Any re-derivation or re-ranking of the wave-1 result. The verdict is REJECT ALL per Phase 2g and stays REJECT ALL.
- Any V-window run, slippage sensitivity, or stop-trigger sensitivity (all gated on §10.3 promotion, which did not occur).
- Any live deployment, paper/shadow readiness, or capital exposure proposal.
- Any edits to `docs/12-roadmap/technical-debt-register.md` (operator restriction held).
- Any MCP / Graphify enablement.
- Any Phase 4 work.

---

**End of memo.** Phase 2h is decision/planning only; Part 3's recommendation hands the next-boundary decision to the operator with the conditions that would change either choice spelled out explicitly.
