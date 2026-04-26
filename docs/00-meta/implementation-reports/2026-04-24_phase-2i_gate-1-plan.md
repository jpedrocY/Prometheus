# Phase 2i — Gate 1 Plan: Structural Breakout Redesign Planning

**Working directory:** `C:\Prometheus`
**Plan date:** 2026-04-24
**Branch (current):** `main` at `61696a6` — verified clean working tree, synchronized with `origin/main` after the Phase 2h PR #9 merge
**Proposed Phase 2i working branch:** `phase-2i/structural-redesign-planning` (proposal only — branch is created after Gate 1 approval per the operator's restriction)
**Scope of this document:** Gate 1 plan only. No code, no edits to source, no new backtests, no new variants, no new data, no Binance API calls, no MCP/Graphify, no `.mcp.json`, no Phase 4 work, no edits to `docs/12-roadmap/technical-debt-register.md`.

This Gate 1 plan is a draft sitting in the working tree as an untracked file pending Gate 1 approval. After Gate 1 approval the file is committed to the proposed branch alongside the redesign-analysis memo, the Gate 2 review, and the checkpoint report.

---

## Context — why this phase, why now

Phase 2g executed the four operator-approved single-axis variants of the locked v1 breakout strategy on R = 2022-01-01 → 2025-01-01 against the v002 datasets. All four disqualified on BTC under the pre-declared Phase 2f §10.3 floor (REJECT ALL). H-B2 was the closest case — Δexp +0.133 R, ΔPF +0.17 — vetoed by |maxDD| > 1.5× baseline (ratio 1.505x). Per Phase 2f §11.3.5 the threshold was binding; no V-window run, no slippage sensitivity, no stop-trigger sensitivity was performed.

Phase 2h then issued a provisional recommendation: **Phase 2i Option B — Structural Breakout Redesign Planning, docs-only** (primary), with **Phase 2i Option A — narrow Wave 2 with H-D6 exit-model bake-off** (provisional fallback). Phase 4 stayed deferred per existing operator policy. The Phase 2h decision memo §3.3 enumerated four switch-condition blocks (B → A, B → C, B → defer, any → D) that would justify changing the recommendation. The operator approved Phase 2h Gate 2 and authorized starting Phase 2i.

**Phase 2i is decision/planning only.** It defines what "structural redesign" actually means for the v1 breakout family, evaluates redesign axes, proposes a small structural-candidate shortlist, surfaces interactions with the four open Phase 2f GAPs, defines a redesign comparison/validation framework that preserves the Phase 2f / 2g discipline, and recommends what Phase 2j should look like. **Phase 2i does not write rule specs, does not propose code, and does not run anything.** The redesign rule-spec writing is Phase 2j.

---

## 1. Executive summary

Phase 2i produces a single committable redesign-analysis memo that (a) recaps the locked facts from Phase 2e/2f/2g/2h, (b) defines structural-vs-parametric for the v1 breakout family explicitly enough that the next phase cannot quietly turn a parameter tweak into "structural", (c) evaluates five redesign axes (setup-pattern, HTF bias/regime, entry-timing, exit-philosophy, risk/position-management interaction) on rationale, evidence, expected effects, overfitting risk, implementation complexity, validation burden, (d) proposes a small redesign-candidate shortlist where each candidate is a genuine rule-shape change with a thesis, a problem-it-solves, replaced-vs-kept parts, and new risks, (e) handles the four open strategy GAPs (030 / 031 / 032 / 033) explicitly per candidate (resolve / carry / supersede), (f) defines a validation framework for redesigns that preserves §10.3 / §10.4 / §11.3 / §11.4 / §11.6 discipline and the GAP-036 fold-scheme convention, (g) compares four next-phase options after 2i, (h) issues a provisional primary + fallback recommendation with explicit "what would change this recommendation" switch conditions, and (i) at most one ambiguity-log append (only if a clean structural-vs-parametric ambiguity surfaces during the analysis; otherwise no new GAP).

**Headline recommendation, provisional and subject to operator review:** primary path is **Phase 2j Option A — Structural Redesign Memo Only (docs-only)** — i.e., another focused docs-only step in which the Phase 2i shortlist of structural candidates is taken further by writing full rule specs for 1–2 candidates with falsifiable hypotheses and pre-declared success criteria. Fallback is **Phase 2j Option B — Redesign Candidate Execution Planning (Gate 1 plan for executing 1–2 redesigns)** — appropriate only if the Phase 2i memo produces a clear single-best candidate with no remaining design decisions. Phase 4 stays deferred. Reasoning is in §13–§14.A below.

## 2. Plain-English statement

Phase 2h told us "single-axis tweaks on the four tested axes don't work; before more tweaking, ask whether the strategy's *shape* is right." Phase 2i is the asking. We define what changing the *shape* (rather than the *value*) of breakout setup / bias / entry / exit / risk-interaction would look like. We propose a small list of rule-shape candidates that would be genuinely different from the current v1 spec — not just renamed knobs. We DO NOT write the new specs in this phase. The next phase (2j) writes specs for 1–2 of the most promising candidates. We only execute against real data after both 2i and 2j are committed and approved.

## 3. Branch and status verification commands

Before any Phase 2i work (after Gate 1 approval), run:

```
git -C c:/Prometheus status --short
git -C c:/Prometheus rev-parse --abbrev-ref HEAD
git -C c:/Prometheus fetch origin
git -C c:/Prometheus log --oneline -10
git -C c:/Prometheus checkout -b phase-2i/structural-redesign-planning
```

Abort gate at start of phase: if working tree is not clean (apart from this Gate 1 plan as an untracked file) or current branch is not `main`, stop and escalate.

## 4. Exact scope

- Read the Phase 2e baseline summary, Phase 2f strategy-review memo + Gate 1 plan, Phase 2g comparison report + Gate 2 review + checkpoint, and Phase 2h decision memo + Gate 2 review + checkpoint in full. Confirm the recap below matches the on-disk record.
- Produce a written redesign-analysis memo with: factual recap, definition of structural vs parametric for the v1 family, redesign-axis analysis (5 families), redesign-candidate shortlist (initial frame is 3 candidates max — R1 / R2 / R3 — but the Gate 1 condition 2 R1 coherence test may split R1 into R1a + R1b, expanding the interim shortlist to up to 4 candidates; rule-shape changes only), GAP-030/031/032/033 interactions per candidate, validation framework for redesigns, relationship to fallback Wave 2 and to Phase 4, four-option analysis for the next phase (2j memo / 2j execution / fallback Wave 2 / Phase 4), provisional recommendation with explicit switch conditions and a recommended carry-forward set capped at ≤ 2 candidates per Gate 1 condition 1.
- At most one new GAP entry appended to `docs/00-meta/implementation-ambiguity-log.md` only if a structural-vs-parametric ambiguity in the v1 spec surfaces during the analysis. Otherwise no log change in 2i.
- Produce a Gate 2 pre-commit review.
- Produce a Phase 2i checkpoint report.
- Stop before any commit awaiting operator/ChatGPT Gate 2 approval.

## 5. Explicit non-goals (hard boundaries)

- No code changes. No new tests. No new backtests, runs, or variants.
- No re-running of H0 or any H-* variant.
- No writing of redesign rule specs (deferred to Phase 2j Option A).
- No writing of redesign execution Gate 1 plan (deferred to Phase 2j Option B if the operator picks it).
- No new data downloads, no new dataset versions, no manifest changes.
- No Binance API calls (authenticated or public).
- No live-trading code, no exchange-write, no production keys.
- No MCP enablement, no `.mcp.json`, no Graphify indexing.
- No Phase 4 work.
- No edits to `docs/12-roadmap/technical-debt-register.md` (operator restriction held).
- No `data/` commits.
- No re-derivation or re-ranking of the wave-1 result. The verdict is REJECT ALL per Phase 2g and stays REJECT ALL.
- No re-derivation or re-framing of the Phase 2h provisional recommendation. It is the input to Phase 2i, not a target for revision.
- No threshold tightening or loosening on §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- No live deployment, paper/shadow readiness, or capital exposure proposal.
- No assumption that redesign automatically means a better strategy — the memo states explicitly that redesign is a research bet that may itself produce a clean negative.
- No quietly turning parameter changes into "structural" changes — the memo's structural-vs-parametric definition (§7) is the binding test.

## 6. Factual recap to be reproduced in the memo

(All numbers are quoted from committed reports.)

### 6.1 Phase 2e baseline (FULL window, untouched control)

- Window: 2022-01-01 → 2026-04-01 UTC (51 months); v002 manifests; zero invalid windows.
- BTCUSDT: 41 trades, WR 29.27%, expR −0.43, PF 0.32, net −3.95%, max DD −4.23%, L/S 21/20, exits STOP 22 / STAGNATION 19 / TRAIL 0.
- ETHUSDT: 47 trades, WR 23.40%, expR −0.39, PF 0.42, net −4.07%, max DD −4.89%, L/S 18/29, exits STOP 35 / STAGNATION 11 / TRAIL 1.
- Funnel dominant rejections (both symbols): `no valid setup` ~57–58%, `neutral bias` ~37%, `no close-break` ~5%; trailing filters each <0.5%.
- Sizing never bound at Phase 3 defaults (`risk=0.0025`, `risk_usage=0.90`, `max_leverage=2.0`, `notional_cap=100_000`, `taker=5bps`, `slippage=MEDIUM`, `equity=10_000`).

### 6.2 Phase 2f strategy-review conclusions (committed)

- Filter inventory + structural/parametric classification of 25 strategy elements (§7.3 of Phase 2f memo).
- Six new GAP entries: GAP-20260424-030..035 (4 OPEN strategy items + 2 RESOLVED verification-only).
- Pre-declared §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds and discipline.
- Wave-1 cap = 4 single-axis variants; ≤ 1 exit/management variant per wave.
- Wave-1 selection: H-A1 (setup window 8 → 10), H-B2 (expansion 1.0 → 0.75 × ATR20), H-C1 (HTF EMA 50/200 → 20/100), H-D3 (break-even +1.5R → +2.0R).

### 6.3 Phase 2g wave-1 result (committed; preserved unchanged)

R-window headline (entries filtered to R = 2022-01..2025-01):

| Variant | BTC trades / WR / expR / PF / netPct / maxDD                          | ETH trades / WR / expR / PF / netPct / maxDD                          |
|---------|-----------------------------------------------------------------------|-----------------------------------------------------------------------|
| H0      | 33 / 30.30% / −0.459 / 0.26 / −3.39% / 3.67%                          | 33 / 21.21% / −0.475 / 0.32 / −3.53% / 4.13%                          |
| H-A1    | 13 / 15.38% / −0.831 / 0.10 / −2.42% / 2.21%                          | 11 / 18.18% / −0.360 / 0.49 / −0.89% / 1.75%                          |
| H-B2    | 69 / 30.43% / −0.326 / 0.43 / −5.07% / 5.53%                          | 57 / 24.56% / −0.440 / 0.35 / −5.65% / 6.53%                          |
| H-C1    | 30 / 26.67% / −0.499 / 0.24 / −3.35% / 3.28%                          | 32 / 15.62% / −0.495 / 0.29 / −3.56% / 3.99%                          |
| H-D3    | 33 / 30.30% / −0.475 / 0.25 / −3.51% / 3.79%                          | 33 / 21.21% / −0.491 / 0.31 / −3.64% / 4.20%                          |

Per-fold consistency (Phase 2f §11.2 5-rolling-folds, fold 1 partial-train per GAP-036): no variant produces a positive expR on **any** BTC test fold. §10.3 / §10.4 verdict: **all four variants disqualified on BTC**.

### 6.4 Phase 2h recommendation (committed; preserved unchanged)

- Primary (provisional): Option B — Phase 2i: Structural Breakout Redesign Planning (docs-only) → this is the phase being planned now.
- Fallback (provisional): Option A — Phase 2i: narrow Wave 2 with H-D6 exit-model bake-off as the centerpiece.
- Phase 4 stays deferred.
- Decision memo §3.3 enumerates four switch-condition blocks (B → A, B → C, B → defer, any → D) that would change the recommendation.

### 6.5 What is now known technically

- The data layer (v002 manifests, 51-month coverage, mark-price + funding joins) is research-credible.
- The backtester is deterministic at fixed inputs.
- The variant-config + stop-trigger-source infrastructure works and is in place for any future approved wave.
- Pre-declared §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds applied without post-hoc adjustment produce a clean, defensible verdict.
- The fold-scheme convention is pinned (GAP-20260424-036): 5 rolling folds with fold 1 partial-train, all tests inside R.

### 6.6 What remains unresolved strategically

- Is the locked v1 breakout family viable on BTCUSDT/ETHUSDT 15m + 1h with v002 data? Wave 1 says "not on these four axes"; it does not say "not at all".
- Do exit-model decisions matter (the H-D6 question)? Untested.
- Are bundled variants justified (under Phase 2f §9.1 deviation)? Untested.
- **Is there a structural redesign axis that meaningfully changes rule shapes (not values) and produces a falsifiable hypothesis?** This is what Phase 2i answers.

## 7. Definition of "structural redesign"

This is the binding test that prevents Phase 2j from quietly relabeling parameter tweaks as "structural".

### 7.1 What counts as structural

A change is **structural** if it is one of the following:

- A change to **rule shape** (the form of the predicate, not the threshold value). Example: replacing `range_width <= 1.75 × ATR20` with `current_ATR <= percentile_20(rolling_500_bar_ATR)` — the predicate's form changes from "range-based ratio" to "percentile-based ranking".
- A change to **rule input domain** (which signals the rule consumes). Example: replacing 1h `EMA(50) vs EMA(200) + slope` with `ADX threshold + volatility-regime classifier` — the bias rule consumes different signals.
- A change to **rule output coupling** (how a rule's result flows to other rules). Example: replacing the current "if bias is NEUTRAL → reject" gate with "bias acts as a position-size multiplier" — the bias signal stops being a binary gate and becomes a continuous modifier.
- A change to **trade-lifecycle topology** (the sequence and conditions under which lifecycle events fire). Example: replacing the current "market entry on next-bar open after breakout-bar close" with "limit-order entry at setup boundary, valid for N bars after breakout" — the entry topology changes from immediate-fill to conditional-pending.
- A change to **risk/position-management interaction** that introduces a new dimension. Example: introducing volatility-regime-scaled risk_fraction, or introducing a cooldown-after-consecutive-losses rule.

### 7.2 What counts as parametric (and thus is NOT a structural redesign)

A change is **parametric** if it only:

- Changes a numeric threshold (e.g., 1.75 → 2.00, 0.10 → 0.15, +1.5R → +2.0R).
- Changes a window length while keeping the same rule shape (e.g., setup window 8 → 10).
- Changes an indicator period (e.g., EMA(50) → EMA(20)).
- Combines two parametric changes into a "bundle" without changing any rule shape.

Wave 1 was a parameter search on parametric axes. Phase 2i must not produce candidates that are parameter-search results in disguise.

### 7.3 What remains fixed in any structural redesign

The following are **outside the scope** of Phase 2i / 2j redesign — they are project-level locks and must not be silently reconsidered:

- BTCUSDT as the live primary symbol; ETHUSDT as research/comparison only.
- One-way mode, isolated margin, one position max, one active protective stop max, no pyramiding, no reversal while positioned.
- Initial live risk 0.25% of sizing equity for any *live-deployment-eligible* configuration (a research redesign may sweep wider risk for sensitivity, but a redesign that requires a different live risk to be viable is moving the wrong direction).
- Effective leverage cap 2x for live deployment.
- Internal notional cap mandatory for live operation.
- Exchange state is authoritative; commands are not facts; restart begins in SAFE_MODE.
- Mark-price stops as live protective-stop type (workingType=MARK_PRICE, closePosition=true, priceProtect=TRUE).
- v002 datasets, manifests, and the 51-month coverage window.

### 7.4 What must not be silently redefined

- The §10.3 disqualification floor (worse expR, worse PF, |maxDD| > 1.5× baseline) and the §10.4 hard reject. Any redesign uses the same thresholds applied to its R-window result vs. H0 baseline.
- The §11.3 no-peeking discipline. Redesign candidates rank on R only; only top-1–2 proceed to V.
- The §11.4 ETH-as-comparison rule. BTC must clear; ETH must not catastrophically fail.
- The §11.6 cost-sensitivity gate.
- The §11.3.5 pre-declared-thresholds discipline. A redesign cannot loosen thresholds because its hypothesis is "different".
- The Phase 2g wave-1 verdict (REJECT ALL).
- The Phase 2h provisional recommendation (it is the input to 2i, not a target for revision).

## 8. Redesign-axis analysis

The memo will evaluate five redesign families. Each is a legitimate axis where rule-shape change is plausible; the candidate shortlist (§9) will pick at most one shape per axis or a coherent multi-axis combination.

### 8.1 Setup-pattern redesign (Family S)

**Rationale.** The dominant 58% "no valid setup" funnel rejection (Phase 2e) is the largest single source of decision-bar attrition. H-A1 showed window-length is not the binding parameter. The shape itself — range-width as a fraction of ATR — may be the issue.

**Evidence from prior phases.** Wave-1 H-A1 (setup window 8 → 10) collapsed trade frequency without recovering edge (BTC 33 → 13, expR −0.831). H-A2 (range-width ceiling 1.75 → 2.00) and H-A3 (drift cap 0.35 → 0.50) are untested.

**Candidate rule-shape changes:**
- **Volatility-contraction pattern (VCP)**: setup valid when 15m ATR(20) is below the X-th percentile of its trailing-N distribution. Replaces "range-based ratio" with "vol-percentile ranking".
- **Multi-window consolidation**: setup valid when a composite signal across 6/8/12 windows confirms compression — not a single window length.
- **Bollinger-band squeeze**: setup valid when band-width is at a trailing-N low.

**Expected effect on trade frequency.** Plausibly moderate increase if the new shape captures more genuine compressions; could equally produce fewer if the new shape is more discriminating.

**Expected effect on expectancy/drawdown.** Uncertain. If VCP captures regime-aligned setups better than range-based, expR could improve; if not, drawdown scales similarly to H-B2's pattern.

**Overfitting risk.** MEDIUM. Percentile-based shapes have implicit lookback parameters; multiple parameter choices (percentile threshold, lookback window) become testable once the shape is committed.

**Implementation complexity.** MEDIUM. Requires either rolling-percentile computation on ATR series (manageable in incremental indicator cache) or band-width arithmetic.

**Validation burden.** Standard Phase 2f §10.3/§10.4 framework; fold scheme per GAP-036; no new diagnostics required beyond the recommended regime-tagging analytic that any redesign should carry.

### 8.2 Higher-timeframe bias / regime redesign (Family B)

**Rationale.** The 37% "neutral bias" funnel rejection (Phase 2e) is the second-largest source of decision-bar attrition. H-C1 showed EMA-pair speed is not the binding parameter. The bias *shape* may be the issue.

**Evidence from prior phases.** Wave-1 H-C1 (EMA 50/200 → 20/100) was marginally worse on both symbols. H-C2 (slope-rule definition, GAP-031) and H-C3 (slope window) are untested but parametric. No structural alternative has been tried.

**Candidate rule-shape changes:**
- **ADX-based trend filter**: replace EMA-pair + slope with ADX(14) > 20 (or comparable) on 1h. Replaces "trend direction" rule with "trend strength" rule.
- **Regime-switching detector**: HMM-style or simpler rule-based regime classification (e.g., trending / chopping / volatile-breakout) gates trade direction. Bias becomes a regime label, not a long/short flag.
- **Volatility-adjusted bias**: combine trend (EMA) with volatility regime (ATR-percentile) — e.g., long bias active only when 1h trend is up AND 1h volatility is above its trailing-N median.
- **Multi-timeframe confirmation**: 1h trend AND 4h trend (instead of single 1h slope).

**Expected effect on trade frequency.** Plausibly increases by reducing NEUTRAL bias hits (e.g., ADX strength filter cares about trend strength, not direction-flips).

**Expected effect on expectancy/drawdown.** Uncertain. If the current EMA-slope NEUTRAL is genuinely filtering out chop, replacing it with a different filter may admit chop and worsen expectancy; if the EMA-slope NEUTRAL is too strict on real trends, replacement could improve.

**Overfitting risk.** MEDIUM-HIGH. Regime classifiers have more degrees of freedom than EMA-pair + slope. ADX has known parameter (14) but threshold (20) is testable.

**Implementation complexity.** MEDIUM (ADX) to HIGH (HMM). HMM also introduces non-deterministic state-estimation in the pipeline that current backtester is not designed for.

**Validation burden.** Standard. Note that §11.4's ETH-as-comparison rule may stress regime classifiers because ETH and BTC have different volatility regimes; cross-symbol robustness becomes harder.

### 8.3 Entry-timing redesign (Family E)

**Rationale.** Wave-1 H0 BTC stops out 22/41 trades (54%). Stop-out-on-entry-bar may indicate entry timing is too eager.

**Evidence from prior phases.** No entry-timing redesign has been tested. Wave 1 used the spec's "market entry on next-bar open after breakout-bar close" baseline.

**Candidate rule-shape changes:**
- **Breakout retest**: enter on first pullback to the breakout level (within N bars of the breakout). Replaces "immediate market entry" with "pending entry on retest".
- **Limit-order entry near setup level**: instead of market on next-bar open, place a limit at setup_high + buffer (long); fill if reached within N bars.
- **Momentum confirmation lag**: enter only after N additional bars of continuation in the breakout direction.
- **Breakout-and-retrace combo**: enter only when price has broken AND retraced AND resumed.

**Expected effect on trade frequency.** Plausibly *decreases* (some breakouts will not retest within N bars and be missed) — opposite direction from setup/bias redesigns.

**Expected effect on expectancy/drawdown.** Plausibly improves expectancy (better entry quality) but may reduce sample size to non-credible levels.

**Overfitting risk.** MEDIUM. Multiple parameters become testable per shape (retest depth, retest window, momentum-lag count).

**Implementation complexity.** MEDIUM. Backtester currently does next-bar-open fills only; pending-limit logic would need adding.

**Validation burden.** Standard, with the additional concern that reduced trade count makes per-fold consistency harder to assess.

### 8.4 Exit-philosophy redesign (Family X)

**Rationale.** H-D3 was tested in wave 1 but only changed one threshold within the same staged-trailing exit philosophy. The major untested axis is the entire exit philosophy class. Phase 2h §3.3 explicitly flagged the exit-philosophy gap as the strongest case for fallback Wave 2 (Option A) with H-D6 as the centerpiece. Family X is the structural-redesign equivalent.

**Evidence from prior phases.** H-B2's "more trades + worse drawdown" pattern hints that the exit machinery may be the binding constraint on a less-restrictive trigger. Wave-1 trail exit count was 0/41 (BTC) and 1/47 (ETH); the trailing logic almost never fires. Stagnation exits dominate (BTC 19/41; ETH 11/47). The current exit philosophy may be misaligned with how trades actually behave.

**Candidate rule-shape changes:**
- **Fixed R-multiple targets**: 2R or 3R take-profit; if not hit within N bars, exit at market. Replaces "staged-trailing" with "fixed target + time-based fallback".
- **Volatility-adaptive trailing**: ATR-percentile-scaled trail instead of fixed 2.5× multiplier.
- **Time-based exit (max-hold N bars)**: exit regardless of MFE after N bars.
- **Opposite-signal exit**: exit when an opposite-direction setup forms.
- **MAE-aware exit**: tighten or close on MAE crossing a threshold (not just stop level).

**Expected effect on trade frequency.** Unchanged (exit changes don't gate entries) unless paired with a re-entry-after-exit shape change.

**Expected effect on expectancy/drawdown.** This is the highest-leverage axis on expectancy reshaping. Fixed-2R could clip trailing winners (bad for expectancy if there are real big winners) or improve consistency (good if winners rarely run far). Empirical answer unknown.

**Overfitting risk.** MEDIUM. Each exit shape has 1–2 parameters (target multiplier, time bound).

**Implementation complexity.** LOW-MEDIUM. Exit logic is the most localized part of the strategy module; replacing TradeManagement with a different exit class is manageable.

**Validation burden.** Standard. Regime-tagging analytic is especially valuable for exit redesign because exit behavior interacts strongly with volatility regime.

### 8.5 Risk / position-management interaction redesign (Family R)

**Rationale.** Phase 2g sizing was never bound (zero rejections). Risk per trade is fixed at 0.25%. There is no equity-curve-aware risk reduction. This means a strategy that can be tweaked to be less negative-expectancy still draws down in a fixed-risk pattern across regimes.

**Evidence from prior phases.** Per-fold tables show universally bad fold (2024H1) on every variant on both symbols. Fixed-risk sizing makes the strategy as exposed in the bad regime as in the good one.

**Candidate rule-shape changes:**
- **Volatility-targeted sizing**: scale risk by inverse of ATR-percentile (low vol → larger size, high vol → smaller). Replaces "fixed risk fraction" with "volatility-equalized risk".
- **Equity-curve-aware risk dampening**: reduce risk after a drawdown of X% from peak; restore after recovery. Crosses into operational-policy territory (similar to drawdown-controls).
- **Cooldown after consecutive losses**: skip N entries after L losses in a row.
- **Concurrent-trade allowance**: relax one-position rule to allow up to 2 concurrent trades on different setups (still single symbol). **Note: violates Phase 2f §7.3 "one position max" structural lock.** This sub-candidate is OUT OF SCOPE per §7.3.

**Expected effect on trade frequency.** Cooldown and equity-aware reduce frequency in bad runs; volatility-targeted leaves count unchanged.

**Expected effect on expectancy/drawdown.** Volatility-targeted shifts the per-trade R distribution but not the underlying expectancy. Equity-aware and cooldown change drawdown profile substantially without affecting per-trade expectancy.

**Overfitting risk.** HIGH. Equity-curve-aware rules can fit the historical drawdown precisely without generalizing.

**Implementation complexity.** MEDIUM. Risk-modulation is a Phase 4-adjacent concern in some shapes (e.g., equity-aware needs equity tracking across restarts).

**Validation burden.** HIGH. Risk-policy changes interact with the project-level locks in §7.3 — any candidate that touches sizing must explicitly verify it preserves the live-deployment constraints (initial risk 0.25%, max leverage 2x, notional cap, one-position).

## 9. Redesign-candidate shortlist

Phase 2i proposes **at most three** structural-redesign candidates. Each is a genuine rule-shape change. Each has a thesis, an explicit problem-it-solves, replaced-vs-kept parts, and new risks. The shortlist is the menu Phase 2j writes specs for; Phase 2i does not pick one.

### Candidate R1 — "Volatility-regime breakout"

- **Thesis.** The strategy fails because (a) range-based setups don't actually capture volatility-contraction periods that precede genuine breakouts, and (b) the EMA-pair-slope bias filter excludes too many bars while letting through chop-prone regimes.
- **Problem from Phase 2e/2g it tries to solve.** Combined ~95% of decision-bar attrition (no-valid-setup + neutral-bias) on a per-bar basis. Wave-1 H-A1 and H-C1 showed value-tweaking these rule shapes doesn't help.
- **What of the current v1 family it replaces.** Setup-pattern (range-based ratio → volatility-percentile ranking) AND bias rule (EMA-pair + slope → ADX-based trend strength + volatility-regime classifier).
- **What it keeps.** 15m signal, 1h bias horizon (different rule), bar-close confirmation, structural stop formula, exchange-side STOP_MARKET protective stop, one-position rule, locked v1 risk/leverage/notional caps.
- **New risks.** Two simultaneous rule-shape changes (multi-axis structural change). Higher overfitting surface (percentile thresholds, lookback windows, ADX threshold). May not be cleanly falsifiable in a single Phase 2j spec.
- **Family map.** S + B (multi-axis structural). NOT bundled-parametric (which is forbidden); multi-axis structural is allowed because each axis change is genuinely a rule-shape change.

### Candidate R2 — "Pullback-confirmed entry"

- **Thesis.** The strategy fails because immediate next-bar-open entry on a breakout close gets whipsawed; pullback-confirmed entries reduce false-start rate at the cost of lower frequency.
- **Problem from Phase 2e/2g it tries to solve.** 54% STOP exit rate on BTC wave-1 baseline; H-D3 (a parametric exit tweak) didn't help, suggesting the issue is upstream of exit logic.
- **What of the current v1 family it replaces.** Entry-timing rule (next-bar-open after breakout close → pending limit at setup boundary, valid for N bars).
- **What it keeps.** Setup-pattern, bias, trigger condition (breakout bar still defines the candidate), stop, exit, and all locks per §7.3.
- **New risks.** Lower trade count (some breakouts won't retest within N bars). Potential per-fold sample-size issues. Backtester needs new pending-limit-fill logic (not currently implemented).
- **Family map.** E (single-axis structural).

### Candidate R3 — "Fixed-R exit with time stop"

- **Thesis.** The strategy fails because the staged-trailing exit clips profits during retracements (trailing rarely fires) while exposing trades to multi-bar adverse moves; a clean fixed-2R target with a time-based fallback aligns exits with how trades actually behave.
- **Problem from Phase 2e/2g it tries to solve.** Trail exit count was 0/41 (BTC) and 1/47 (ETH) in the wave-1 baseline; stagnation dominates exits on BTC (19/41); H-D3 (a parametric break-even tweak) didn't move the needle.
- **What of the current v1 family it replaces.** Exit philosophy (Stage 3–7 staged-trailing → fixed-2R take-profit + time-based 8-bar fallback exit). Stage-3 risk-reduction (−0.25R move) is removed; break-even at Stage 4 is removed; trailing is removed.
- **What it keeps.** Setup, bias, trigger, entry timing, structural stop formula (initial stop preserved), exchange-side STOP_MARKET protective stop, one-position rule, all §7.3 locks.
- **New risks.** Clipping real big winners. R-multiple choice is a parameter that becomes structural-rule-shape-only-if-pre-declared. Note: this candidate overlaps significantly with the H-D6 fallback's "fixed-2R" sub-variant — see §11 for handling.
- **Family map.** X (single-axis structural). The line vs. parametric is "fixed-2R" being a *philosophy commitment* (no parameter sweep) rather than a *parameter value* (one of many sweep points).

### Why this initial 3-candidate frame, and how the R1 coherence test may expand it

This is the **pre-split initial frame** that Phase 2i starts from. The Gate 1 condition 2 R1 coherence test (executed in the redesign-analysis memo) determines whether R1 stays as one bundled candidate or splits into R1a (Family-S setup-pattern volatility) + R1b (Family-B HTF bias/regime).

Pre-split frame: R1 is multi-axis (S + B); R2 is entry-timing (E); R3 is exit-philosophy (X). Bias-only structural change (B alone) is initially folded into R1 because the original drafting hypothesis was that bias change without setup change is a small sub-set of R1 and not a meaningfully different thesis. Risk/position-management redesign (R) is excluded from this shortlist because (a) Phase 2g sizing was never bound and (b) any risk-policy candidate that touches sizing crosses into the §7.3 project-level locks. A Family-R candidate could be a legitimate Phase 2j addition only with explicit operator authorization to revisit the sizing locks, which Phase 2i does not propose.

**Post-split frame (only if the R1 coherence test concludes R1 is two separable ideas).** The interim shortlist expands to **up to 4 candidates** — R1a, R1b, R2, R3 — to honor the Gate 1 condition 2 split discipline. The recommended **carry-forward set to Phase 2j stays capped at ≤ 2** per Gate 1 condition 1 regardless of whether the interim shortlist is 3 or 4. The redesign-analysis memo records the actual outcome of the coherence test and the actual recommended carry-forward set.

## 10. Interaction with existing open GAPs

The four open Phase 2f strategy-spec GAPs interact differently with each candidate. The redesign-analysis memo states per-candidate disposition explicitly.

**Pre-split frame (R1 / R2 / R3):**

| GAP | Topic | Candidate R1 | Candidate R2 | Candidate R3 |
|---|---|---|---|---|
| GAP-20260424-030 | Break-even +1.5R vs +2.0R rule-text conflict | CARRIED — R1 keeps current exit logic so the conflict stays open | CARRIED — R2 keeps current exit logic so the conflict stays open | SUPERSEDED — R3 removes break-even from the exit machinery; the conflict becomes moot. To be marked SUPERSEDED in the ambiguity log when R3 is selected for execution. |
| GAP-20260424-031 | EMA slope wording (discrete vs. fitted) | SUPERSEDED — R1 replaces EMA-slope with ADX/regime; the slope-wording question becomes moot. To be marked SUPERSEDED when R1 is selected for execution. | CARRIED — R2 keeps the current bias rule | CARRIED — R3 keeps the current bias rule |
| GAP-20260424-032 | Backtest trade-price stop vs. live MARK_PRICE stop sensitivity | CARRIED — execution-realism question, survives any redesign. Mark-price sensitivity must be a required report cut for any promoted redesign per §11. | CARRIED | CARRIED |
| GAP-20260424-033 | Stagnation window (8 bars, +1R gate) classification | CARRIED — R1 keeps current exit logic | CARRIED — R2 keeps current exit logic | CARRIED-AND-EXTENDED — R3's time-based 8-bar fallback overlaps the stagnation window concept; the redesign should explicitly state whether the time-based fallback is the "new stagnation" or whether stagnation is removed entirely. |

**Post-split frame (R1a / R1b / R2 / R3) — applies if the R1 coherence test splits R1.** The redesign-analysis memo §2.4 contains the authoritative 4-candidate × 4-GAP matrix. Briefly: GAP-030 SUPERSEDED only by R3; GAP-031 SUPERSEDED only by R1b (the Family-B half of the original R1); GAP-032 CARRIED by all four candidates as a mandatory mark-price sensitivity report cut; GAP-033 CARRIED-AND-EXTENDED by R3 as in the pre-split frame, CARRIED by R1a / R1b / R2.

The memo's per-candidate spec-implications section will reproduce the relevant rows verbatim so each candidate's GAP exposure is explicit.

## 11. Comparison/validation framework for redesigned candidates

### 11.1 Comparison anchor

Redesigned candidates compare to **H0 only** (the locked Phase 2e baseline, re-run on R per the Phase 2g pattern). They do **not** compare directly to wave-1 variants — wave-1 was a closed parameter search, not a sibling redesign. Comparing to wave-1 variants would risk implicitly using wave-1 results to retune the redesign, which is the §11.3.5 violation.

### 11.2 Pre-declared thresholds

Redesigned candidates use the **same** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds as wave 1 — applied to the redesign's R-window result vs. H0 baseline. Specifically:

- §10.3.a (Δexp ≥ +0.10 R, ΔPF ≥ +0.05) — applies unchanged.
- §10.3.b (Δexp ≥ 0, trades + ≥ 50%, |maxDD| not worse > 1.0pp) — applies unchanged.
- §10.3.c (exit-model bake-off strict dominance) — applicable to R3 since it is an exit-philosophy candidate.
- §10.3 disqualification floor (worse expR / worse PF / |maxDD| > 1.5× baseline) — applies unchanged.
- §10.4 hard reject (rising trades + expR < −0.50 OR PF < 0.30) — applies unchanged.
- §11.3 no-peeking + top-1–2 promotion — applies unchanged.
- §11.4 ETH-as-comparison — applies unchanged.
- §11.6 cost-sensitivity (LOW + HIGH slippage on any §10.3 pass) — applies unchanged.

A redesign **cannot** loosen these thresholds because its hypothesis is "different". Per §11.3.5, the thresholds are pre-committed and cannot be tightened or loosened after seeing results — for any wave, including a redesign wave.

### 11.3 New phase, new threshold pre-declaration

Each redesign candidate enters a new operator-approved phase (Phase 2k or later, per the operator's chosen sequence) with its own Gate 1 plan that pre-declares (a) the candidate's exact rule spec from the Phase 2j memo, (b) the §10.3/§10.4 threshold values reused from Phase 2f (no change), (c) the comparison anchor (H0 on R), (d) any candidate-specific success-criterion that goes beyond §10.3 (e.g., R3 may require a per-symbol "fixed-2R hit rate" diagnostic to be pre-declared).

### 11.4 R/V split remains appropriate

The R = 2022-01..2025-01 / V = 2025-01..2026-04 split per Phase 2f §11.1 stays as the canonical split for any redesign wave. No reason to change.

### 11.5 Fold methodology stays the same

The 5-rolling-folds with fold-1 partial-train per GAP-20260424-036 stays as the canonical fold scheme. Supplemental 6-half-year appendix per Phase 2g §3.A may be retained for descriptive coverage.

### 11.6 Additional diagnostics that should be mandatory for redesigns

Every redesign report must include (in addition to the §10.1–§10.2 / §7.5 cuts already required by Phase 2f):

- **Per-regime expR**: classify each trade's entry by realized 1h volatility regime (low / medium / high based on trailing percentile) and compute per-regime expR. This is the regime-tagging analytic deferred from Phase 2h §2.10.3.
- **MFE distribution**: histogram of MFE in R-multiples to characterize where in the trade lifecycle the strategy captures or fails to capture profit.
- **Per-direction long/short asymmetry**: separate expR / PF / win rate for long-only and short-only subsets.
- **GAP-032 mark-price sensitivity** (required per Phase 2f §10.6 / GAP-032): every promoted redesign candidate must run with `stop_trigger_source=TRADE_PRICE` and report the comparison.

These diagnostics do not require new code in Phase 2i (this phase is docs-only); they are a required output specification for the eventual execution phase.

## 12. Relationship to fallback Wave 2 (Phase 2h Option A)

Phase 2h §3.1 fallback was Wave 2 narrowly bounded to H-D6 (exit-model bake-off: fixed-2R / fixed-3R / staged+trailing baseline / opposite-signal). That fallback is conceptually adjacent to Candidate R3 (fixed-R exit with time stop) but not identical:

- **H-D6** is a **comparative bake-off** — it tests four exit philosophies side-by-side as parametric variants on H0's other rules, without committing to one. Per the Phase 2h fallback framing, H-D6 is a single-axis variant under Phase 2f §9.1 in the wave-2 scope.
- **Candidate R3** is a **structural commitment** to one specific exit philosophy (fixed-2R + time-based 8-bar fallback) with its own pre-declared spec. R3 is not a sweep across multiple exit forms.

The two are different research bets:

- If the project takes Phase 2j Option A (memo with full rule specs for whichever ≤ 2 carry-forward candidates the operator chooses from the interim shortlist — pre-split R1/R2/R3 or post-split R1a/R1b/R2/R3 per the §9 coherence test), R3 is the candidate that absorbs the exit-philosophy axis. H-D6's bake-off is implicitly resolved by picking one philosophy in R3.
- If the project takes Phase 2i fallback (i.e., switches the recommendation to Phase 2h Option A and runs H-D6), R3 is not pursued; the bake-off result determines whether any single exit form has signal, and a future redesign can use that result as input.

**Why fallback remains fallback.** The redesign path is the higher-value next step **given the wave-1 evidence pattern**. Wave 1 disqualified 4 of 4 single-axis variants on the BTC §10.3 floor; H-B2's near-pass was vetoed by tail-risk, not edge. The disciplined reading is "single-axis search on these axes does not work"; the right next step is to re-examine the rule shapes, not to keep searching parametric values. H-D6 is a worthwhile *secondary* but it is still a parameter search at heart (one of four exit shapes), and the pattern-from-wave-1 says parameter search isn't where the answer is.

**When fallback wins.** If the Phase 2i analysis concludes that the structural redesign space is so design-vacuum-prone that 2j cannot produce a falsifiable hypothesis, the project should switch to fallback Wave 2 with H-D6. This is one of the §13.A switch conditions.

## 13. Relationship to Phase 4

Phase 2h §2.10 / §3.3 noted Phase 4 stays deferred per existing operator policy. Phase 2i further strengthens the case for deferral:

- Phase 4's strategy-coupled parts (entry-intent contracts, exit-reason taxonomy, management lifecycle, dispatch hooks) interact with the v1 spec. A structural redesign of the strategy will reshape these.
- Phase 2j writing specs for 1–2 redesign candidates will produce concrete spec deltas that any Phase 4 implementation must absorb. Building Phase 4 first and then reshaping it for redesigned strategies is wasted effort on the strategy-coupled portions.
- Phase 4's strategy-agnostic parts (runtime DB schema, persistence, SAFE_MODE startup, kill switch state) could in principle be built independently — but the project policy has been to keep Phase 4 paused until strategy direction is settled, and this phase does not propose changing that.

**What would need to happen before Phase 4 becomes the better next move.** Per Phase 2h §3.3 "any → D" switch block: an explicit operator policy change accepting that operational infrastructure will be built without strategy-edge confirmation. Phase 2i does not propose this change; if the operator updates that policy independently, Phase 4 becomes available immediately and Phase 2i's recommendation does not block it.

## 14. Proposed next-phase options after 2i

### Option A — Phase 2j: Structural redesign memo only (docs-only)

| Aspect | Detail |
|---|---|
| Pros | Forces full rule-spec writing for ≤ 2 carry-forward candidates (drawn from the interim shortlist after the §9 R1 coherence test — pre-split R1/R2/R3 or post-split R1a/R1b/R2/R3) with falsifiable hypotheses and pre-declared success criteria; preserves Phase 2f-style discipline; same low-risk surface as Phase 2f / 2h |
| Cons | More upfront thinking before any execution; risk of designing in a vacuum on rule shapes the project hasn't yet stress-tested |
| Risk of wasted effort | MEDIUM (mitigated by pre-declared falsifiability) |
| EVI | HIGH if the spec-writing produces a rule that materially differs from H0 in measurable ways; LOW if the specs are relabeled parameter sets |

### Option B — Phase 2j: Redesign candidate execution planning (Gate 1 plan for execution)

| Aspect | Detail |
|---|---|
| Pros | Faster path to evidence; uses existing variant-config + stop-trigger-source infrastructure |
| Cons | Skips the rule-spec writing step; risk of executing a poorly specified candidate; most candidates (R1 especially) are multi-axis and may need spec disambiguation before execution |
| Risk of wasted effort | MEDIUM-HIGH (without Phase 2j memo, candidates are under-specified) |
| EVI | HIGH on the candidate's actual performance; LOW on the pre-execution understanding of why it's expected to work |

### Option C — Fallback narrow Wave 2 planning (operator switches to Phase 2h fallback)

| Aspect | Detail |
|---|---|
| Pros | Fills the H-D6 exit-model evidence gap directly; uses existing infrastructure |
| Cons | Redesign discipline is paused; project takes a parameter-search step that wave-1 evidence already suggests is the wrong direction |
| Risk of wasted effort | MEDIUM-LOW (H-D6 has high info value regardless); MEDIUM (entry-axis follow-ups have lower value) |
| EVI | HIGH for H-D6; structural-redesign question stays unanswered |

### Option D — Phase 4: Runtime / state / persistence

| Aspect | Detail |
|---|---|
| Pros | Decoupled from strategy debate; required for any future paper/shadow/live |
| Cons | Premature commitment to operational plumbing while strategy direction is unsettled; strategy-coupled parts need re-review after redesign |
| Risk of wasted effort | LOW for strategy-agnostic parts; MEDIUM-HIGH for strategy-coupled parts |
| EVI | LOW on strategy question; MEDIUM-HIGH on operational-readiness question |

## 14. Final recommendation (provisional; subject to operator/ChatGPT review)

This recommendation is **provisional and evidence-based, not definitive**. It is a judgement about the highest-value next research step given the evidence currently in hand. It is explicitly **not** any of the following:

- It is **not** a claim that structural redesign automatically produces a better strategy. Redesign is a research bet that may itself produce a clean negative.
- It is **not** a claim that the breakout family is permanently viable. Wave-1 evidence rules out four single-axis paths on this spec on this data; redesign tests whether different rule shapes on this data produce edge.
- It is **not** a claim that fallback Wave 2 is invalid. Wave 2 with H-D6 remains a legitimate alternative path; the recommendation is only that, given current evidence, redesign is the higher-value next step.

With those caveats explicit:

**Primary (provisional): Option A — Phase 2j: Structural redesign memo only (docs-only).**

Rationale: Phase 2h's recommendation was for "structural redesign planning". Phase 2i (this phase) is the planning level — analysis, axis evaluation, candidate shortlist (pre-split R1/R2/R3 or post-split R1a/R1b/R2/R3 per §9 R1 coherence test), validation framework. Phase 2j Option A is the next disciplined step: writing full rule specs for ≤ 2 carry-forward candidates with falsifiable hypotheses and pre-declared success criteria. This is the same docs-only step Phase 2f executed for the v1 spec axes; doing it for redesign candidates is the intellectually consistent path. Going straight from Phase 2i analysis to Phase 2j execution planning (Option B) skips the rule-spec writing and risks executing under-specified candidates.

**Secondary (fallback, provisional): Option B — Phase 2j: Redesign candidate execution planning.**

Rationale: If the Phase 2i analysis produces a clear single-best candidate with no remaining design decisions and a fully-specified rule (rare but possible — most likely for R3 if its spec is judged complete from Phase 2i alone), Phase 2j can skip the memo step and go directly to execution Gate 1 planning. The fallback is appropriate only if the candidate's spec is truly ready, not as a way to skip the spec step out of urgency.

**Phase 4 stays deferred** per existing operator policy. Phase 2i does not propose advancing it.

## 14.A What would change this recommendation

The recommendation is provisional. The following kinds of evidence or reasoning would justify switching paths:

### Switch from Option A (primary) to Option B (secondary as primary)

- Phase 2i analysis converges on a single candidate (most plausibly R3 — exit-philosophy commitment is the most contained candidate) with a complete rule spec and no remaining design decisions.
- Operator preference for execution evidence over additional docs-only spec writing once the candidate space is narrowed.
- Identification that the chosen candidate's spec is small enough that "memo" and "execution Gate 1 plan" collapse into a single document.

### Switch from Option A to Option C (fallback Wave 2)

- Phase 2i analysis concludes that the structural redesign space is design-vacuum-prone — i.e., none of the interim candidates (pre-split R1/R2/R3 or post-split R1a/R1b/R2/R3) produces a hypothesis falsifiable in a single execution wave without unmanageable parameter-overfitting risk.
- Phase 2i analysis concludes that H-D6's exit-model bake-off is sufficient to address the dominant evidence-gap from wave 1, and structural redesign should be re-considered after H-D6 results.
- Operator preference for execution evidence on the exit-model axis specifically before any structural redesign.

### Switch from Option A to Option D (Phase 4)

- Explicit operator policy change that operational infrastructure should be built without strategy-edge confirmation. Current policy is against this; Phase 2i does not propose changing it. If the operator updates that policy independently, Phase 4 becomes available immediately and Phase 2i's recommendation does not block it.

### Switch from Option A back to "defer" (no new phase)

- Discovery during Phase 2i analysis that prior phase documents have an unresolved inconsistency requiring a docs-only correction phase before any further strategy work.
- Operator decision to pause strategy work and prioritize a different operational concern (e.g., security review, host-hardening prep, documentation cleanup).
- A new operator restriction (timing, capital, scope) that makes the current options materially less attractive.

The redesign-analysis memo will reproduce this section verbatim so the conditions for switching are as explicit and pre-declared as the §10.3 / §10.4 thresholds were for wave 1.

## 15. Proposed files / directories

Phase 2i produces docs only:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md` — this plan, committed after Gate 1 approval (currently sitting as an untracked draft on `main` per the operator's branch-creation restriction).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md` — the main redesign-analysis memo (§§ 6–14.A above as the committable artifact, expanded into rule-shape rationale per §8 and per-candidate detail per §9).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-2-review.md` — pre-commit review.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i-checkpoint-report.md` — checkpoint.
- `docs/00-meta/implementation-ambiguity-log.md` — append at most one new GAP entry **only if** a structural-vs-parametric ambiguity in the v1 spec surfaces during the analysis. Currently no new GAP is anticipated; if one is needed, GAP-20260424-037 is the next available identifier.

No other files touched. No `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `.claude/`, `data/`, or `technical-debt-register.md` edits.

## 16. No code / dependency changes

No source code changes. No tests added or modified. No new top-level packages. No new dependencies. No `pyproject.toml` or `uv.lock` change.

## 17. Output artifacts

- **Committed (to git, after Gate 2 approval):** Gate 1 plan, redesign-analysis memo, Gate 2 review, checkpoint report, optionally one ambiguity-log append (only if a clean ambiguity surfaces).
- **Not committed:** none — Phase 2i produces no intermediate parquet, no run output, no notebook artifact.
- **Presented to operator / ChatGPT:** concise markdown summaries with tables. No screenshots.

## 18. Safety constraints

| Check | Requirement |
|---|---|
| Production Binance keys | none |
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
| Phase 2j work | none (this is the phase that proposes 2j, not starts it) |
| New backtests / variants / data | none |
| Tightening / loosening of any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold | none |
| Re-derivation of wave-1 verdict | none — REJECT ALL preserved |
| Re-framing of Phase 2h provisional recommendation | none — Phase 2h is input, not target |
| Quietly re-classifying parametric as structural | none — §7 binding test applies |

## 19. Ambiguity / spec-gap items to log

**At most one new GAP entry**, conditional on the analysis surfacing a clean structural-vs-parametric ambiguity in the v1 spec. Most likely candidate (if it surfaces): the spec's "Open Questions" §553–567 list contains both genuine parameter ambiguities (already covered by GAP-030/031/033) and what could be read as structural-axis questions (e.g., open question on whether the breakout-bar buffer rule shape should be ATR-multiplier vs. price-distance — this is parametric in the current spec but could be re-cast as structural if a redesign candidate replaces it).

If no new GAP is needed, the ambiguity log is unchanged. The Phase 2i memo will state explicitly which case obtained and why.

## 20. Technical-debt register — no edits

`docs/12-roadmap/technical-debt-register.md` is NOT edited in Phase 2i. TD-016 (statistical live-performance thresholds) is informationally affected but the register itself stays untouched per operator restriction.

## 21. Proposed commit structure (end of Phase 2i)

Four to five commits on `phase-2i/structural-redesign-planning`, after two operator gate approvals (Gate 1 = this plan; Gate 2 = pre-commit review). Pytest runs before each commit and is expected at 396 passed (no code change anywhere).

1. `phase-2i: Gate 1 plan` — this file's content as `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md`.
2. `phase-2i: structural redesign analysis memo` — `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md`.
3. `phase-2i: ambiguity log append (GAP-20260424-037)` — *conditional, only if a new ambiguity surfaces*. Append-only edit.
4. `phase-2i: Gate 2 review` — `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-2-review.md`.
5. `phase-2i: checkpoint report` — `docs/00-meta/implementation-reports/2026-04-24_phase-2i-checkpoint-report.md`.

If no new GAP, the ambiguity-log commit is omitted and the sequence is four commits + checkpoint = five total. If a new GAP is needed, six commits including the checkpoint.

No `data/` commits. No `src/` or `tests/` commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## 22. Gate 2 review format (to be produced at end of 2i)

```
Phase: 2i — Structural Breakout Redesign Planning
Scope confirmed against Gate 1 plan: yes / no + diffs
Docs written: list
Ambiguity-log appends: list (GAP IDs) — may be empty
Factual recap completeness: cross-checked vs Phase 2e/2f/2g/2h committed reports
Structural vs parametric definition: §7 binding test reproduced; no relabeled parametrics
Redesign-axis analysis: 5 families covered with rationale / evidence / expected-effect / overfitting / complexity / validation burden
Redesign-candidate shortlist: pre-split R1/R2/R3 (3 candidates) or post-split R1a/R1b/R2/R3 (up to 4 candidates) per the Gate 1 condition 2 R1 coherence test; each with thesis / problem / replaced-vs-kept / new-risks / family-map; recommended carry-forward set capped at ≤ 2 per Gate 1 condition 1
GAP-030/031/032/033 disposition: per-candidate matrix
Validation framework: comparison anchor / pre-declared thresholds / R/V split / fold scheme / mandatory diagnostics
Relationship to fallback Wave 2: present
Relationship to Phase 4: present
Recommendation: primary + fallback recorded; provisional framing present
"What would change this recommendation": present with switch-condition blocks
Wave-1 result preserved: REJECT ALL stands; no re-derivation
Phase 2h recommendation preserved: not re-framed
Threshold preservation: §10.3 / §10.4 / §11.3 / §11.4 / §11.6 all unchanged
§7.3 project-level locks preserved: BTCUSDT live primary, one-way mode, isolated margin, one-position, 0.25% live risk, 2x leverage, notional cap, mark-price stops, v002 datasets
Safety posture: no code, no data, no APIs, no MCP, no Graphify, no TD-register edits
Operator restrictions honoured: yes
Test suite: pytest 396 passed (no code change expected)
Recommended next step: operator chooses among Option A / B / C / D
Questions for operator: list or "none"
```

## 23. Checkpoint report format

Follows `.claude/rules/prometheus-phase-workflow.md` exactly: Phase, Goal, Summary, Files changed (all docs), Files created (all docs), Commands run (none safety-relevant — pytest + git status/diff), Installations performed (none), Configuration changed (none), Tests/checks passed (pytest 396 expected), Tests/checks failed (none), Known gaps (any new GAP-037 if logged; otherwise unchanged), Safety constraints verified (full table), Current runtime capability (research-only, unchanged), Exchange connectivity status (zero), Exchange-write capability (disabled), Recommended next step (proposal only — operator decides among Option A / B / C / D).

## 24. Approval gates

- **Gate 1 — this plan.** Approved 2026-04-24 with three conditions (all applied; see §26).
- **Gate 2 — pre-commit review.** After redesign-analysis memo + (optional) GAP append + Gate 2 review + checkpoint report drafted, operator reviews diff + pytest output before any `git add` / `git commit`.

## 25. Post-approval execution sequence (docs-only)

After Gate 1 approval, proceed in this order and **stop before any `git add` / `git commit`**:

1. Verify branch state (working tree should show this Gate 1 plan as untracked, plus any operator-applied edits).
2. Create the working branch:
   ```
   git -C c:/Prometheus checkout -b phase-2i/structural-redesign-planning
   git -C c:/Prometheus status --short
   ```
3. The Gate 1 plan file is already at `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md` (sitting in the working tree from this drafting step); it follows the branch.
4. Draft the redesign-analysis memo at `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md`, structured around §§ 6–14.A of this Gate 1 plan with the §13 provisional-framing language and §14.A "What would change this recommendation" reproduced verbatim.
5. If a structural-vs-parametric ambiguity surfaces during the memo writing, append GAP-20260424-037 to `docs/00-meta/implementation-ambiguity-log.md`. Otherwise no log change.
6. Draft Gate 2 review at `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-2-review.md` using the §22 format.
7. Stop. Show operator `git status`, `git diff --stat`, and `uv run pytest` output (expect 396 passed). Do not run `git add` / `git commit`. Await operator/ChatGPT Gate 2 review.

The Phase 2i checkpoint report (§23) is produced after Gate 2 approval, immediately before the commit sequence (§21).

## 26. Gate 1 operator conditions applied (2026-04-24)

The operator approved Gate 1 with three conditions. All are now incorporated into this plan and will be carried into the redesign-analysis memo verbatim where applicable:

1. **Candidate carry-forward discipline (≤ 2 to Phase 2j).** Phase 2i may shortlist up to 3 structural candidates (or up to 4 if the R1 coherence test forces a split per condition 2), but the recommended carry-forward set to Phase 2j is **at most 2**. The redesign-analysis memo will state this cap explicitly in its candidate-shortlist section and will rank the carry-forward picks with reasoning.
2. **R1 coherence requirement.** The redesign-analysis memo will explicitly test whether R1 ("Volatility-regime breakout" — combined setup-pattern volatility + bias/regime change) is one coherent thesis or two separable ideas. If the analysis concludes R1 is two separable ideas, the memo will split it into R1a (setup-pattern volatility-percentile) and R1b (HTF bias/regime change) for Phase 2j carry-forward purposes, instead of carrying R1 forward as a disguised bundle. Phase 2j is then free to pick one or neither of R1a/R1b within the ≤ 2 carry-forward cap.
3. **H0 anchor wording.** The redesign-analysis memo will include one explicit statement (in its validation framework section) that:
   - **H0 remains the only comparison anchor for redesign candidates.** All redesign performance is computed vs. the locked Phase 2e baseline H0 re-run on R, never vs. wave-1 variants.
   - **Phase 2g wave-1 variants (H-A1, H-B2, H-C1, H-D3) are historical evidence only, not promotion baselines.** Their R-window numbers may be cited diagnostically but they do not serve as comparison anchors for any redesign §10.3 / §10.4 evaluation.

These three conditions are binding for the Phase 2i memo and will also be re-verified in the Phase 2i Gate 2 review's traceability table.
