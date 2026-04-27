# Phase 2t — R2 (Pullback-Entry Redesign) Gate 1 Planning Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7 binding test for structural-vs-parametric and §1.7.3 project-level locks (H0 anchor; BTCUSDT primary; one-position max; 0.25% risk; 2× leverage; mark-price stops; v002 datasets); Phase 2i §3.2 entry-redesign survey (R2 originally enumerated and deferred); Phase 2j memo §C / §D (spec-style template); Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE locked); Phase 2m comparison report (R1a+R3 mixed-PROMOTE preserved as research evidence); Phase 2n strategy-review memo (R3 = research-leading; R1a+R3 = promoted-but-non-leading); Phase 2o asymmetry-review memo (asymmetry diagnosed as market-structure × strategy interaction; §F.1 / §F.4 future-hypothesis framing); Phase 2p consolidation memo (R3 = baseline-of-record; R1a = retained-for-future-hypothesis-planning); Phase 2r R1b-narrow spec memo; Phase 2s R1b-narrow execution comparison report (PROMOTE on R; PASS classification with explicit sample-size and per-trade-expectancy caveats); operator brief authorizing Phase 2t docs-only hypothesis planning for R2.

**Phase:** 2t — Docs-only Gate 1 planning for R2 (pullback-entry redesign).
**Branch:** to be created by operator (recommended naming: `phase-2t/r2-gate-1-planning`).
**Memo date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

**Status:** Planning memo only. **No code, no runs, no parameter tuning, no candidate-set widening beyond R2, no Phase 4 / paper-shadow / live-readiness work, no MCP / Graphify / `.mcp.json` activity, no credentials.** This memo describes what Phase 2t is deciding, recaps what Phase 2s proved, defines the R2 hypothesis structurally (not parametrically), enumerates required backtester changes, expected mechanism / failure modes / trade-count implications / overfitting risk, and the §10.3 falsifiability framing — and concludes with a clear GO / NO-GO recommendation for a follow-on docs-only spec-writing phase. Phase 2t itself does **not** authorize spec-writing or execution; the operator decides separately.

---

## 1. What Phase 2t is deciding

### 1.1 Plain-English

Phase 2t is the planning gate that decides whether **R2 (pullback-entry redesign)** is worth specifying as the next structural-redesign hypothesis. It is the analogue of Phase 2r's Gate 1 planning memo (which decided "Path B = R1b-narrow"), one phase later in the sequence and on a different structural axis.

Concretely, Phase 2t answers four questions:

1. **Is the next structural axis worth pursuing inside the breakout family at all?** Two filter-shape redesigns (R1a setup-shape, R1b-narrow bias-shape) have run. Both PROMOTE'd under §10.3 but neither closed the absolute-edge gap on BTC. The operator's Phase 2s interpretation is that bias-strength is not the missing mechanism. If filtering further is unlikely to move the picture, the question becomes whether **entry mechanics** (the only un-tested structural axis with a concrete deferred candidate) is the right next thing to specify, or whether the family should be consolidated and operator strategy should shift.
2. **If so, is R2 specifically the right candidate?** Phase 2i §3.2 originally surveyed three entry-redesign rule shapes: breakout-retest, limit-order entry, momentum-confirmation lag. They cluster together as "entry-timing topology change". R2 is shorthand for that cluster; the planning memo does not commit which sub-shape the eventual spec will adopt, only that the cluster is structurally distinct from filter-axis redesigns and addresses a different failure mode (post-entry whipsaw, not selection quality).
3. **Has the deferral rationale from Phase 2i changed enough to justify reviving R2 now?** Phase 2i §3.2 deferred R2 for three reasons: (a) wave-1 stop-out evidence was *indirect* — could be a setup or trigger problem rather than entry timing; (b) backtester needs new pending-limit-fill logic — additional implementation cost; (c) lower trade count — per-fold consistency harder to establish. Reasons (a) and (c) are partially addressed by the Phase 2l / 2m / 2s evidence; reason (b) is a fixed cost that has been deferred long enough that the alternatives (filter-axis variants on the existing market-fill backtester) are now exhausted.
4. **GO or NO-GO for a follow-on docs-only spec-writing phase (Phase 2u-equivalent)?** Phase 2t itself does not write the spec. If GO, a Phase 2j-style spec memo with single-axis structural change, sub-parameters committed singularly with explicit non-fitting rationale, falsifiable hypothesis, mandatory diagnostics, and full §1.7 binding-test evaluation becomes the next phase. If NO-GO, R2 stays in its Phase 2i-deferred state and the operator's next move is non-R2 (e.g., consolidate at R3; family-shift planning; lift Phase 4 deferral; lift paper/shadow deferral).

### 1.2 What Phase 2t is NOT deciding

Phase 2t is **not** deciding:

- The exact pullback level (breakout level vs setup boundary vs midpoint of breakout-bar range — committed in Phase 2u spec).
- The exact confirmation rule (bar-close inside vs bar-low/high holding — committed in Phase 2u spec).
- The exact validity window (8 bars vs 5 bars vs 10 bars — committed in Phase 2u spec).
- The exact fill model (limit-at-pullback vs next-bar-open after confirmation — committed in Phase 2u spec).
- Whether to authorize execution. Execution requires a separate operator-approved Gate 1 plan after the spec memo lands (mirroring Phase 2k → Phase 2l for R3, Phase 2k → Phase 2m for R1a+R3, Phase 2r-spec → Phase 2s for R1b-narrow).
- Any change to R3's locked exit machinery (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`). R2 is specified as "X on top of R3", same as R1a+R3 and R1b-narrow.
- Any change to Phase 2i §1.7.3 project-level locks (BTCUSDT primary; ETHUSDT research/comparison only; one-position max; 0.25% risk; 2× leverage; mark-price stops; v002 datasets).
- Any change to Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds.
- Any change to the H0-anchor framework. H0 remains the sole governing comparison anchor.
- Operator policy on paper/shadow, Phase 4, or family abandonment. Those remain operator-policy decisions outside Phase 2t's scope.

### 1.3 Authority for what Phase 2t may do

Phase 2t may:

- Read prior phase reports and the strategy/validation/data specs.
- Recap evidence already committed (no re-running, no re-derivation).
- Define R2's structural shape conceptually, not parametrically.
- Enumerate backtester changes required (descriptive; no code).
- Articulate falsifiability under §10.3 unchanged.
- Recommend GO / NO-GO for a follow-on spec-writing phase.

Phase 2t may not:

- Run any backtest, any code, any parameter sweep.
- Commit any sub-parameter value (those belong to the Phase 2u spec).
- Change any threshold or any §1.7.3 lock.
- Add a candidate beyond R2 to the planning surface.
- Authorize the spec-writing phase by itself; only the operator authorizes phases.
- Touch source code, tests, scripts, datasets, manifests, the technical-debt register, the implementation-ambiguity log, `.claude/`, `.mcp.json`, or any credential.

---

## 2. Summary of what Phase 2s proved (R1b-narrow outcome)

(All numbers quoted verbatim from the Phase 2s comparison report. No re-derivation. No new statistic.)

### 2.1 Headline numbers

R1b-narrow on R = 2022-01-01 → 2025-01-01, MEDIUM slippage, MARK_PRICE stop trigger, v002 datasets:

| Variant     | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|-------------|---------|-------:|-------:|--------:|------:|--------:|--------:|
| H0          | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% |
| R3          | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% |
| R1b-narrow  | BTCUSDT |     10 | 50.00% |  −0.263 | 0.561 |  −0.59% |  −1.09% |
| H0          | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% |
| R3          | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% |
| R1b-narrow  | ETHUSDT |     12 | 33.33% |  −0.224 | 0.622 |  −0.60% |  −1.28% |

H0 and R3 controls reproduce locked baselines bit-for-bit. R1b-narrow PROMOTES under §10.3.a + §10.3.c on both BTC and ETH; no §10.3 disqualification floor; no §10.4 (Δn < 0); §11.4 satisfied. PASS classification under Phase 2f.

### 2.2 What the framework verdict says vs what the deltas mean

- R1b-narrow is the **first** Phase-2x candidate to clear §10.3.a on both BTC and ETH simultaneously at the magnitude threshold (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05 on both). On the formal-framework metric alone, this is the strongest result the project has produced.
- **However**, the R3-anchor view is essentially neutral on BTC: Δexp_R3 **−0.023 R**, ΔPF_R3 **+0.000**. R1b-narrow's marginal contribution on top of R3 is roughly nothing on BTC; it is positive on ETH (Δexp_R3 +0.127, ΔPF_R3 +0.148). The improvement vs H0 is dominated by R3's exit-machinery contribution plus R1b-narrow's filter-induced trade-count concentration — **not** by per-trade expectancy improvement on BTC.
- **Trade-count drops sharply.** BTC 33 → 10 (−69.7%); ETH 33 → 12 (−63.6%). Per-fold sub-counts collapse: BTC 0/2/1/2/3, ETH 3/2/1/2/2. BTC F1 has zero trades; F3 BTC has a single trade.
- **V-window evidence is fragile.** BTC V has only 1 trade (a single losing trade, expR −1.270; uninterpretable on n=1). ETH V is the project's second positive-netPct V-window (8 trades, 50% WR, expR +0.154, PF 1.408, netPct +0.28%) but smaller than R1a+R3's +0.69%.
- **Slope-strength bucket diagnostic** (Phase 2r §P.3): zero entries in the "strong" bucket (≥ 0.0100); R1b-narrow's improvement, when it materializes, comes from the *moderate-strength* bucket. The moderate > marginal trend within the available buckets directionally supports the bias-strength mechanism but is unable to be fully tested at these sample sizes.
- **Direction-asymmetry on BTC.** Phase 2r §P.4 predicted BTC's R1b-narrow result should remain direction-symmetric. Instead, BTC longs −0.529 / shorts +0.136 (n=4 shorts, single-trade-flip-fragile). Deviated from prediction.

### 2.3 Operator + ChatGPT joint Phase 2s interpretation

The operator brief for Phase 2t records the joint review conclusion:

- R1b-narrow's marginal contribution vs R3 is neutral on BTC.
- The trade-count reduction (~65–70%) drives most of the apparent improvement vs H0.
- There is no evidence that bias-strength improves per-trade expectancy.
- **Conclusion: bias-strength is not the missing mechanism.**

This conclusion is consistent with the Phase 2s report's own §13 ("What the PASS does NOT claim"): the PASS verdict is framework-valid but does not establish absolute edge, does not establish BTC-shorts edge, and does not change R3's status as the baseline-of-record. The framework verdict and the strategic interpretation diverge — both are honest readings of the same data; the planning question is what to do next.

### 2.4 What Phase 2s teaches Phase 2t

Two filter-shape redesigns have now been tested:

| Axis                  | Candidate    | R-window vs H0 framework | R3-anchor BTC                     | R3-anchor ETH                     | V-window BTC          | V-window ETH                   |
|-----------------------|--------------|--------------------------|-----------------------------------|-----------------------------------|-----------------------|--------------------------------|
| Setup shape (S)       | R1a+R3       | PROMOTE (BTC §10.3.c only; ETH §10.3.a + c) | Δexp_R3 **−0.180** / ΔPF_R3 **−0.205** | Δexp_R3 +0.237 / ΔPF_R3 +0.359   | n=4, 0% WR, expR −0.990 | n=8, 62.5% WR, +0.69% netPct |
| Bias-strength (B-narrow) | R1b-narrow | PROMOTE (BTC §10.3.a + c; ETH §10.3.a + c) | Δexp_R3 **−0.023** / ΔPF_R3 **+0.000** | Δexp_R3 +0.127 / ΔPF_R3 +0.148   | n=1, 0% WR, expR −1.270 | n=8, 50.0% WR, +0.28% netPct |

The pattern is consistent: **filter-axis redesigns reduce trade count substantially, produce ETH-side improvement, and either hurt or fail to help BTC's per-trade expectancy on top of R3**. R1a's BTC degradation was severe (Δexp_R3 −0.180); R1b-narrow's BTC contribution is essentially nil (Δexp_R3 −0.023). Both share trade-count fragility on BTC's V-window.

The reasonable next inference: filtering — at least filtering of the kinds attempted so far — does not appear to be the leverage point on BTC. The BTC trades that survive R3's exit machinery are not improvable by selecting fewer of them; they are improvable (if at all) by changing **when or how** they are entered, **whether they are taken at all on certain price-action conditions**, or by accepting that the absolute-edge gap on BTC is structural to the family.

R2 is the only remaining structural axis with a concrete Phase 2i-deferred candidate that addresses a *different* failure mode. Phase 2t evaluates whether to specify it.

---

## 3. Definition of the R2 hypothesis

### 3.1 What problem R2 targets

R2 targets the **post-entry whipsaw / immediate-stop-out problem** that Phase 2i §3.2 identified as a candidate cause of the H0/wave-1 BTC stop-out rate.

The empirical anchor (already-committed evidence; no re-derivation):

- **Phase 2i §3.2 entry-axis observation:** "Wave-1 H0 BTC stops out 22 of 41 trades (54%). Stop-out-on-entry-bar may indicate entry timing is too eager."
- **Phase 2l / 2m / 2s exit decomposition:** R3's improvement comes substantially from replacing staged-trailing exits with a fixed +2 R take-profit and an unconditional 8-bar time-stop. The staged-trailing machinery was firing late or never; the time-stop now exits stagnant trades cleanly. But R3 does not change the *initial* stop placement or the *entry price* — the trades that R3 stops out are the same trades H0 would have stopped out, just managed differently afterwards.
- **R3 BTC stop-exit count:** 8 / 33 trades stop-exit (under R3 BTC). BTC's stop-out concentration relative to total exits is meaningfully lower under R3 than H0 (which stop-exits 17 / 33), but the structural fact remains that a non-trivial fraction of BTC trades are stopped before the time-stop horizon. R2's hypothesis is that some of those stop-outs are not "the breakout thesis was wrong" but "the entry was placed at the worst short-term price and then mean-reverted before the breakout's directional follow-through arrived".
- **R1b-narrow + R3 on BTC** does not change the stop-out structure: it admits fewer trades, but the surviving trades' MFE distribution (Phase 2s §7.2) is approximately preserved relative to R3 — meaning the trades that survive have similar best-case behaviour, suggesting the worst-case (stop-out) behaviour is also similarly distributed across the survivors. Filter-axis redesigns can move the *count* of stop-outs but not the *ratio* of stop-outs to other exits.

R2's thesis: the stop-out rate is partly a function of *entering at the breakout-bar's high* (for longs) or *low* (for shorts), which is structurally close to where short-term mean-reversion will undo the breakout-bar's expansion. Pullback-confirmed entry attempts to enter closer to the structural invalidation (the setup level / breakout level), reducing the stop distance and reducing the probability that ordinary post-breakout volatility triggers the stop before the directional follow-through can develop.

### 3.2 Why R2 may improve BTC specifically

The asymmetry-review evidence (Phase 2o §C, §D) and the Phase 2s evidence point to BTC's failure mode being different from ETH's:

- **ETH** has a pre-existing direction-asymmetric regime in the v002 R-window (R3 ETH longs −0.934 / shorts +0.028; R1a+R3 ETH shorts +0.387 / PF 1.906). Filter-axis redesigns expose and amplify this directional regime. The ETH improvements seen so far come from selecting *which* compression bars or bias-strength bars to enter, not from improving entry mechanics on bars that were already going to be entered.
- **BTC** is direction-symmetric under R3 alone (longs −0.252 / shorts −0.230) and remains roughly direction-symmetric or marginally asymmetric under R1a+R3 (−0.363 / −0.488) and R1b-narrow (−0.529 / +0.136 with shorts at n=4). Filter redesigns do not surface a directional sub-structure on BTC the way they do on ETH. BTC's failure mode is *not* directional — it is uniform across long/short.

If BTC's failure mode is uniform across direction, then the lever that helps BTC is also direction-uniform: a change to *how every trade is entered*, not a change to *which trades are selected*. R2 is precisely that — every trade R2 takes is a trade the breakout-and-bias filter had already qualified; R2 changes the **entry price and timing**, not the **selection**.

Mechanism-of-improvement-on-BTC sketch:

- Pullback entry is closer to the setup boundary / breakout level. The structural stop is anchored *below the setup boundary minus an ATR buffer* (for longs); the entry price is now closer to that anchor. Stop distance shrinks.
- Smaller stop distance → larger position size at fixed 0.25% equity risk (sizing is `risk_amount / stop_distance`).
- Larger position size → larger payoff per ATR of follow-through (if the trade works).
- If the breakout fails before pullback fills, the candidate expires unfilled — *no loss is taken*. R2 trades the certainty of entry for a partial protection against early failure.
- The stop-distance filter (0.60 ≤ d ≤ 1.80 × ATR(20)_15m per current spec) acts as a natural floor: if pullback entry would put the stop closer than 0.60 × ATR, the trade is rejected at fill time. This prevents R2 from creating pathologically tight stops.

Mechanism-of-improvement-on-ETH sketch:

- ETH's directional regime should still produce R3-style follow-through on shorts; pullback entry on ETH shorts captures that follow-through at a better price.
- ETH longs catastrophic under R1a+R3 may or may not be helped by R2 — pullback entry filters out trades that don't pull back, which on a regime where longs were structurally weak is a partial protection.
- The R2 effect on ETH is expected to be smaller than on BTC because ETH's directional regime is doing more of the work; R2 is timing-side rather than selection-side.

Note: these are *expected* mechanisms, not committed predictions. The falsifiable hypothesis (§10.3 framing) is recorded in §10 below; the mechanistic sketches inform what diagnostics to require but do not narrow the hypothesis space prematurely.

### 3.3 Why R2 is the right next candidate (rather than another filter)

Three structural axes have been visible in Phase 2 throughout:

| Axis  | Family-letter | Status                                                                                   |
|-------|---------------|------------------------------------------------------------------------------------------|
| Setup shape (S)         | R1a            | Tested in Phase 2m. PROMOTE under H0; mixed under R3-anchor; ETH-favorable; BTC-degrading. Retained-for-future-hypothesis-planning per Phase 2p. |
| Bias-strength shape (B-narrow) | R1b-narrow | Tested in Phase 2s. PROMOTE under H0 §10.3.a + c on both symbols; R3-anchor BTC neutral; trade-count-reduction-driven. |
| Entry-mechanic shape (E) | R2             | Deferred at Phase 2i §3.2. Untested. Addresses a different failure mode (post-entry whipsaw).                          |
| Bias-classifier shape (B-classifier) | R1b-classifier | Deferred at Phase 2i §3.2. Higher overfitting risk; HMM-style classifier complexity; cross-symbol robustness harder. |
| Exit-philosophy shape (X) | R3             | Tested in Phase 2l. PROMOTE; broad-based; baseline-of-record per Phase 2p. |

After R3 (X) was confirmed, two of the three remaining axes (S, B-narrow) were tested, both with the same broad pattern (PROMOTE-but-trade-count-driven). R1b-classifier is the highest-overfitting-risk option Phase 2i flagged. **R2 is the lowest-overfitting-risk untested axis**, and it tests a structurally different lever (timing / topology, not selection).

Choosing R2 over R1b-classifier is a discipline choice. R1b-classifier introduces multi-parameter regime-classifier surfaces that conflict with Phase 2j-style single-parameter discipline. R2 introduces conditional-pending entry-timing topology, which has 3-4 sub-parameters but each can be anchored to existing project conventions (see §9 overfitting analysis).

### 3.4 What R2 keeps unchanged

R2 only changes entry-mechanic topology. Everything else is preserved:

- **H0 setup-validity rule** (range_width ≤ 1.75 × ATR(20)_15m AND |close[-1] − open[-8]| ≤ 0.35 × range_width): unchanged. R2 does not combine with R1a's percentile predicate. Setup predicate stays at H0 default `RANGE_BASED`.
- **H0 bias-validity rule** (EMA(50) > EMA(200) + close-relative-to-EMA + slope direction sign): unchanged. R2 does not combine with R1b-narrow's magnitude check. Bias predicate stays at H0 default (`bias_slope_strength_threshold == 0.0`).
- **Six-condition trigger** (close-broke-level, true-range vs ATR, close-location, ATR-regime, etc.): unchanged. The breakout signal that registers the R2 candidate is exactly H0's breakout signal.
- **Initial structural stop formula** (`min(setup_low, breakout_bar_low) − 0.10 × ATR(20)` for longs; symmetric for shorts): unchanged in shape, but anchored to the same structural reference as before. The stop's price level is unchanged; only the **entry price** changes, which causes the **stop distance** (entry_price − stop_price for longs) to shrink.
- **Stop-distance filter** (0.60 ≤ d ≤ 1.80 × ATR(20)_15m): unchanged. Applied at fill time, not at signal time. If pullback entry would produce d < 0.60 × ATR, the trade is rejected.
- **R3 exit machinery** (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`; same-bar STOP > TAKE_PROFIT > TIME_STOP priority; protective stop never moved intra-trade): unchanged.
- **Sizing pipeline** (`risk_fraction=0.0025`, `risk_usage=0.90`, `max_leverage=2.0`, `notional_cap=100_000`, `taker=0.0005`): unchanged in shape. Position size is `risk_amount / stop_distance`; the entry-price change → stop-distance change → position-size change is a *consequence* of the topology change, not a sizing-rule change.
- **Re-entry lockout** (requires `setup_size = 8` bars after exit before same-direction re-entry): unchanged.
- **Phase 2i §1.7.3 project-level locks**: unchanged.

The **single axis** R2 changes is **trade-lifecycle topology**: from "signal → immediate market entry on next-bar open" to "signal → conditional-pending candidate → fill-or-expire". This matches Phase 2i §1.7.1's structural example verbatim:

> Example: replacing "market entry on next-bar open after breakout-bar close" with "limit-order entry at setup boundary, valid for N bars after breakout" — entry topology changes from immediate-fill to conditional-pending.

R2 is the textbook structural-redesign case for the "trade-lifecycle topology" sub-category of the §1.7.1 binding test.

---

## 4. Exact conceptual rule shape for pullback-entry

### 4.1 Conceptual diagram of the entry-lifecycle change

**Current (H0/R3/R1a+R3/R1b-narrow):**

```
[breakout-bar close, completed]
   ↓
[trigger six-condition pass + bias + stop-distance filter]
   ↓
[entry executed at next-bar open as MARKET]
   ↓
[stop placed at next-bar open]
   ↓
[exit machinery (R3) takes over for trade lifecycle]
```

**Proposed (R2 — generic conceptual shape; sub-parameters not committed in Phase 2t):**

```
[breakout-bar close, completed]
   ↓
[trigger six-condition pass + bias + stop-distance pre-filter]
   ↓
[CANDIDATE registered in pending state with:
   - direction (LONG | SHORT)
   - target pullback level (anchored to a structural reference)
   - confirmation requirement
   - validity window (N completed 15m bars after breakout)]
   ↓
[for each subsequent completed 15m bar within validity window:
    if pullback level is reached AND confirmation is satisfied:
        enter at fill price; place stop; trade enters R3 exit machinery
        break
    elif breakout-bar invalidation occurred (e.g., bias flip; opposite signal):
        cancel candidate (no entry); break
    else:
        continue waiting]
   ↓
[if validity window ends without fill: candidate expires; no trade]
```

The key topology change is the **insertion of a pending-state phase between signal and fill**. The signal is a *necessary but not sufficient* condition for entry under R2; the pullback + confirmation jointly with the validity window make the signal sufficient.

### 4.2 How entry differs from breakout market entry — conceptually

Three structural differences:

1. **Two events instead of one.** H0/R3 has a single event-trigger: the breakout-bar's close. The trade is committed at that moment (next-bar open is just the fill mechanic). R2 has two event-triggers: the breakout-bar's close registers a candidate; a subsequent pullback bar (within the validity window, satisfying the confirmation) executes the fill. The candidate may never fill.
2. **Entry price is closer to the structural invalidation reference.** H0/R3 enters at next-bar open, which is structurally at-or-near the breakout-bar's close — i.e., on the *far side* of the setup boundary from the structural invalidation. R2 enters at a pullback level, which is structurally *closer* to the setup boundary / breakout level — i.e., closer to the structural invalidation. Smaller stop distance follows. (Smaller stop distance × fixed 0.25% risk = larger position size, per the sizing pipeline.)
3. **Some signals never become trades.** Under H0/R3, every signal that passes the trigger and stop-distance filter becomes a trade. Under R2, signals that fail to produce a pullback-and-confirmation within the validity window expire unfilled. The signal-to-trade ratio drops; the trade count drops; the *quality* of the trades that do occur (in the R2 thesis) rises because they are filtered by post-signal price action that confirms the breakout was not an immediate exhaustion.

### 4.3 How pullback + confirmation is defined (conceptually, not parametrically)

Phase 2t does **not** commit specific values. The Phase 2u spec memo, if authorized, would commit one value per axis with explicit non-fitting rationale (mirroring Phase 2r §F's `S = 0.0020 ↔ ATR_REGIME_MIN` anchor pattern). The conceptual shape is enumerated below; the eventual spec memo will pick one concrete instance per axis.

#### 4.3.1 Pullback level (target price for fill)

The pullback level is a structural reference that price must reach (from the breakout direction back toward the setup) for a fill to occur. Conceptual options:

- **Breakout level itself.** For longs: the `setup_high` value used in the breakout trigger. Entry at the level the breakout closed above. The "retest" interpretation.
- **Breakout level minus the breakout-buffer.** For longs: `setup_high + 0.10 × ATR(20)` reverse — i.e., the level the trigger required the close to exceed by. This is a slightly tighter pullback (price must give up the buffer to hit it).
- **Setup boundary unbuffered.** For longs: `setup_high` exactly. Same as the first option; restated for symmetry with the buffered option.
- **Midpoint of the breakout-bar's range.** For longs: `(breakout_bar_high + breakout_bar_low) / 2`. A 50% retracement of the breakout bar.
- **Breakout-bar's open.** For longs: `breakout_bar_open`. The price at which the breakout bar started — typically below the close-broke-level for a strong breakout.

Each option has a different fill-rate / fill-quality trade-off. Phase 2u must commit ONE with a non-fitting rationale (e.g., "breakout level is the project's structural-invalidation reference for a long setup; pulling back to that level is the textbook retest pattern; the value is *defined by the strategy's existing setup logic*, not chosen by examining R-window outcomes").

For shorts, all options are mirrored symmetrically (e.g., breakout level → `setup_low` for shorts).

#### 4.3.2 Confirmation requirement (validation that the pullback didn't invalidate the breakout)

The confirmation rule is the structural test that the pullback is a retest, not a reversal. Conceptual options:

- **Bar-close-back-on-breakout-side.** For longs: a completed 15m bar after the pullback level is touched closes *above* the breakout level. The pullback is "confirmed" by a bar-close that returns to the breakout-side of the level. This is the most rule-conservative confirmation.
- **Bar-close-not-violating-breakout.** For longs: a completed 15m bar's close is not below the structural-stop level. (The pullback may go below the breakout level intra-bar but the close must not breach the stop.) Less strict than option (a); allows wicks but not closes.
- **Bar-low-holding-above-stop.** For longs: a completed 15m bar's low is at or above the structural-stop level. (Even intra-bar wicks must not breach the stop.) Strict but uses the bar's extreme rather than its close.
- **Time-only confirmation.** No price-action confirmation; the pullback level being touched *is* the entry trigger. Equivalent to a passive limit order with no extra confirmation — relies on the validity window and the stop-distance filter as the only protections.
- **Continuation-bar confirmation.** A completed 15m bar after the pullback level is touched closes in the breakout-direction *and* its true range is at least some-fraction of ATR. (Mechanically similar to the breakout-bar's own conditions.)

Each option has a different fill-realism profile. The most conservative (a, c) has the lowest fill rate and highest implied fill quality; the most permissive (d) has the highest fill rate and may fire on reversal-then-continuation patterns. Phase 2u must commit ONE with explicit non-fitting rationale.

#### 4.3.3 Validity window (how long the candidate remains pending)

The validity window is the time horizon (in completed 15m bars) after which an unfilled candidate expires. Conceptual options anchored to existing project conventions:

- **8 bars.** Matches `setup_size = 8` (the setup-window length used by the H0 setup-validity rule) AND matches `exit_time_stop_bars = 8` (the R3 unconditional time-stop horizon). This is the strongest candidate for a non-fitting anchor — the value already appears in the project as a "time horizon at which the strategy stops considering a setup or trade actionable".
- **Half of the setup window (4 bars).** A shorter validity window. Fewer bars for pullback to develop; lower fill rate; tighter selection. No existing project anchor.
- **The setup-window length plus the breakout-bar (9 bars).** Reflects the idea that the breakout-bar plus the setup window define the structural reference for valid setup/breakout; pullback should resolve within that span. Weak project anchor.

Phase 2u should anchor to the strongest convention (likely 8 bars matching setup_size and exit_time_stop_bars, but to be evaluated in the spec memo).

#### 4.3.4 Fill model (price at which the fill is recorded for backtest realism)

Even with pullback level and confirmation defined, the backtester needs a fill-realism rule. Conceptual options:

- **Limit-at-pullback (intrabar).** The fill occurs at the pullback level on the bar that touches it. Requires the backtester to use bar-high/low (not close) to detect touch. Most aggressive; assumes resting limit-order fills perfectly at the level.
- **Next-bar-open after confirmation.** The pullback touch and the confirmation bar are detected; the fill is recorded at the *next* completed 15m bar's open. Most conservative; matches the project's existing market-on-next-bar-open convention. Simpler backtester change because no intra-bar logic is required.
- **Bar-close after confirmation.** The fill is recorded at the close of the confirmation bar itself. Intermediate.

Phase 2u should pick the option whose realism profile matches paper/shadow expectations. The most-conservative option (next-bar-open after confirmation) has lower fill rate but matches Phase 2i §10 backtest-vs-live discipline most cleanly. The most-aggressive option (limit-at-pullback intrabar) has higher fill rate but introduces bar-high/low look-ahead concerns that need explicit no-lookahead enforcement.

#### 4.3.5 Cancellation conditions

While a candidate is pending, certain events should cancel it:

- **Bias flip during pending.** If the 1h bias evaluated at the close of any bar within the validity window differs from the candidate's direction, the candidate is cancelled. (A candidate registered LONG must remain valid only while bias remains LONG.)
- **Opposite-direction signal during pending.** If a new breakout signal in the opposite direction fires during the validity window, the candidate is cancelled.
- **Stop-distance violation at fill time.** If the pullback fill price would produce stop_distance < 0.60 × ATR(20)_15m (the existing lower-bound filter), the trade is rejected at fill time. (The upper-bound 1.80 × ATR is also re-checked but is far less likely to trigger after a pullback.)
- **Validity window expiry.** Default cancellation: N bars elapsed without fill.

Each of these is structural to the conditional-pending topology. They are not new sub-parameters; they are the cancellation logic that any conditional-pending entry must define. Phase 2u spec memo should enumerate them explicitly.

### 4.4 Worked example (illustrative; no parameters committed)

Suppose:

- A LONG breakout signal fires at the close of 15m bar `B` at price `1000`.
- `setup_high = 980`, `breakout_bar_high = 1010`, `breakout_bar_low = 990`, `breakout_bar_open = 992`, `breakout_bar_close = 1000`.
- `ATR(20)_15m = 12`. `0.10 × ATR = 1.2`.
- Structural-stop level (longs): `min(setup_low, breakout_bar_low) − 0.10 × ATR = min(960, 990) − 1.2 = 958.8`.
- H0/R3 entry: at `B+1` open ≈ 1000. Stop distance = 1000 − 958.8 = **41.2**.
- R2 entry (illustrative; example uses pullback level = setup_high = 980, confirmation = bar-close-not-violating-stop, validity = 8 bars):
  - Bars `B+1`, `B+2`, ... are observed.
  - On bar `B+3`, low = 979 (touches 980 from above). Bar `B+3` close = 985. Confirmation (close not below 958.8) is satisfied.
  - Fill recorded at bar `B+4` open ≈ 985 (next-bar-open after confirmation).
  - Stop distance = 985 − 958.8 = **26.2**.
  - Position size at 0.25% risk on $10,000 equity: H0 size = $25 / 41.2 = 0.607 BTC; R2 size = $25 / 26.2 = 0.954 BTC. R2 size is **57% larger** than H0 size for the same risk.
  - If the trade reaches +2 R take-profit (R3 exit machinery), R2's R-distance is 26.2 → take-profit at 985 + 52.4 = 1037.4. H0's R-distance is 41.2 → take-profit at 1000 + 82.4 = 1082.4. **R2's take-profit triggers earlier** in price-distance terms (52.4 vs 82.4), meaning R2 is more likely to hit +2 R within the time-stop horizon if a partial follow-through occurs.

This example illustrates the *structural* effect of R2: smaller stop distance, larger position size, closer take-profit, asymmetric exposure to early-failure (since unfilled candidates avoid the loss entirely). The illustrative example uses *example* parameter values; Phase 2u commits the actual values.

### 4.5 What the rule shape is NOT

To clarify scope:

- **R2 is not a new filter.** It does not reject signals that pass H0's trigger; it changes how signals become trades. Every signal that R2 sees has already passed the same six-condition trigger and bias rule that H0 uses.
- **R2 is not a new exit rule.** R3's exit machinery is preserved. The fixed +2 R take-profit and 8-bar time-stop run unchanged after the R2 fill.
- **R2 is not a stop-modification rule.** The structural-stop *level* is unchanged from H0. Only the **entry price** changes, which mechanically changes the stop **distance**.
- **R2 is not a same-direction re-entry rule.** If a candidate expires unfilled, the H0 re-entry lockout (8 bars after exit) does not apply because no exit occurred. The next eligible R2 candidate fires when a new completed 8-bar setup window forms and a new breakout signal fires (per the existing setup-validity rule).
- **R2 is not multi-axis.** It is a single-axis structural change to entry-lifecycle topology. Phase 2u must reject any temptation to combine R2 with R1a, R1b-narrow, or other variants in the same wave.

---

## 5. Required backtester changes (descriptive only — Phase 2t writes no code)

This section enumerates the backtester surface a future Phase 2u-or-execution phase would need to extend. **Phase 2t does not write any of this.** The enumeration is necessary because backtester-cost was one of Phase 2i's reasons for deferring R2; the planning memo needs to make that cost explicit so the operator can weigh it against expected information value.

### 5.1 Pending-state representation

The current backtester models trades as immediate-fill: signal → market fill at next-bar open. R2 requires a new state machine:

- **PendingCandidate object** with fields: direction (LONG | SHORT); registered-at-bar timestamp; pullback-target price; confirmation-rule identifier; validity-window expiry timestamp; structural-stop reference (the price level the stop would be placed at if filled); ATR snapshot at signal time (for stop-distance filter at fill time).
- **Per-symbol pending-candidate list.** Under v1's one-position max + one-symbol scope, the list typically contains 0 or 1 items, but the data structure must support 0..1 cleanly. Multiple pending candidates in the same direction (overlapping breakout signals) must be handled — the simplest discipline is "first-registered candidate wins; subsequent registrations are dropped while one is pending".
- **State transitions.** A candidate moves from `PENDING` → `FILLED` (entry recorded; trade enters normal lifecycle) or `PENDING` → `CANCELLED_INVALIDATION` (bias flip, opposite signal, stop-distance violation at fill) or `PENDING` → `EXPIRED` (validity window elapsed). These transitions must be deterministic and replayable from the same input data.

### 5.2 Limit / conditional fill simulation

The backtester currently assumes market-on-next-bar-open fills with explicit slippage modeling. R2 introduces conditional fills:

- **Touch detection.** For each pending candidate, on each completed 15m bar within the validity window, the backtester must determine whether the bar's price action reached the pullback level. Implementation depends on the fill model:
  - If fill model is "limit-at-pullback intrabar", touch is `bar_low ≤ pullback_level` (longs) or `bar_high ≥ pullback_level` (shorts). Uses bar high/low.
  - If fill model is "next-bar-open after confirmation", touch is detected on bar `t`, confirmation is detected on bar `t` (same bar) or `t+1` (next bar), fill is recorded on bar `t+confirmation_lag+1` open. Simpler; uses bar high/low only for touch; fill price uses next-bar open.
- **Fill price.** Depends on fill model (committed in Phase 2u). The most conservative (next-bar-open after confirmation) reuses the existing fill-price logic verbatim; the most aggressive (limit-at-pullback intrabar) requires a new "fill at limit price" code path with its own slippage model (typically zero or near-zero — limit orders are makers, not takers).
- **Fee model at fill.** Limit fills may use *maker* fees rather than *taker* fees. Binance USDⓈ-M futures has different maker/taker rates. The current backtester uses a single `taker = 0.0005` constant; R2's limit-fill mode would need a `maker` rate (typically lower, e.g., 0.0002). If fill model is "next-bar-open after confirmation", the fill is still a market order by structure, so taker fee applies.

### 5.3 No-lookahead discipline

The conditional-fill logic introduces new no-lookahead concerns:

- **Pullback touch must use only post-signal bars.** A candidate registered at bar `B` close consults bars `B+1`, `B+2`, ... — never bar `B` itself or earlier. The backtester must enforce this with bar-iteration discipline.
- **Confirmation must use only data available at confirmation-bar close.** No future bars may inform the confirmation decision.
- **Stop-distance filter at fill must use ATR at signal time.** The `ATR(20)_15m` used for the stop-distance filter is the value computed at the signal-bar close (bar `B`), not the value at the fill-bar close. Re-computing at fill time would be a subtle look-ahead change. The candidate's ATR snapshot is recorded at registration.
- **Bias evaluation during pending must use current 1h bias.** The cancellation-on-bias-flip rule consults the most recent completed 1h bar's bias evaluation, exactly as the H0 strategy does. No special new bias logic.

A test that compares R2 backtest results across "recompute everything at fill time" vs "use snapshot at signal time" can confirm there is no accidental lookahead — the two should be identical when the snapshot rule is followed correctly.

### 5.4 Funnel attribution

The diagnostic funnel (`run_signal_funnel`) currently has buckets for `rejected_no_valid_setup`, `rejected_neutral_bias`, `rejected_trigger`, `rejected_stop_distance`, etc., terminating in `entry_intents` and `trades_filled`. R2 introduces new candidate-state buckets:

- **`registered_candidates`.** Count of candidates that were registered (passed signal + bias + stop-distance pre-filter at signal time). Equivalent to H0's `entry_intents` for the comparison axis.
- **`expired_candidates_no_pullback`.** Count of candidates that expired without fill because the pullback level was never reached within the validity window.
- **`expired_candidates_invalidated`.** Count of candidates that were cancelled because of bias flip or opposite signal within the validity window.
- **`expired_candidates_stop_distance_at_fill`.** Count of candidates that touched the pullback level but failed the stop-distance filter at fill time (entry too close to structural stop).
- **`trades_filled` (R2).** Count of candidates that filled. Equivalent to H0's `trades_filled` for the actual-trade axis.

The new buckets allow the operator to see the **fill rate** (`trades_filled / registered_candidates`) as a top-line diagnostic, which is the single most informative number for assessing R2's behavior. A fill rate near 100% means the validity window is too long or the pullback level is too easy to reach (R2 degenerates toward H0); a fill rate near 0% means the rule is too strict (R2 produces no trades).

### 5.5 Interaction with existing stop logic

R3's exit machinery operates on filled trades and is independent of how the trade was entered. After an R2 fill, the trade is identical from R3's perspective to a trade that entered at next-bar-open under H0:

- The `protective_stop` is placed at the structural-stop level (same level as H0).
- `exit_r_target = 2.0` is computed in R-distance terms; R-distance = (entry_price − stop_price) for longs. R2's smaller R-distance means the take-profit price is closer to the entry price.
- `exit_time_stop_bars = 8` counts bars from entry-bar close, regardless of how many bars elapsed during the candidate-pending phase. **This is a subtle interaction**: a candidate that fills 5 bars after registration uses 5 bars of the 13-bar total "signal-to-time-stop" window (8 R3 bars after fill); a candidate that fills 1 bar after registration uses 9 bars total. The Phase 2u spec must decide whether the time-stop horizon is "8 bars after fill" (R3-consistent) or "8 bars after signal" (lifecycle-consistent). The R3-consistent interpretation is the expected default.
- Same-bar STOP > TAKE_PROFIT > TIME_STOP priority unchanged.

### 5.6 Implementation surface estimate (descriptive only)

Comparing to past phases:

| Phase | Candidate    | Net source/test lines added | Notes                                                                                                  |
|-------|--------------|----------------------------:|--------------------------------------------------------------------------------------------------------|
| 2l    | R3           |                       ~1100 | New `ExitKind.FIXED_R_TIME_STOP` enum value + new exit-decision branch + ~30 unit tests.               |
| 2m    | R1a (on R3)  |                        ~470 | New `SetupPredicateKind.VOLATILITY_PERCENTILE` enum value + new percentile predicate + 13 unit tests.   |
| 2s    | R1b-narrow   |                        ~250 | New optional `bias_slope_strength_threshold` field + sibling bias function + 14 unit tests.            |

R2's surface is expected to be **larger than R3's** because the pending-state representation is a new state machine that touches strategy session, backtest engine, diagnostics funnel, and tests. A rough estimate (subject to revision in Phase 2u): **~1500–2500 net lines** including tests. The bulk is the pending-state representation, the touch-detection logic, the funnel-bucket additions, and the confirmation-rule unit tests across multiple direction × pullback-level × confirmation cells.

This is the single largest backtester change Phase 2 has contemplated. Phase 2t records this honestly as a deferral-cost that has now been justified by exhausted alternatives.

---

## 6. Expected mechanism of improvement

(Restated and consolidated from §3.2 with explicit prediction structure, but **not** committed as a parameter — the falsifiable hypothesis lives in §10 below.)

### 6.1 Primary mechanism (BTC-focused)

1. The breakout-and-bias filter qualifies a setup-and-breakout pattern. This part is unchanged from H0.
2. Under H0/R3, entry occurs at next-bar open ≈ breakout-bar close. The entry price is structurally on the *far side* of the setup boundary from the structural-stop level — i.e., at maximum stop-distance.
3. Under R2, the candidate waits for price to retrace toward the structural-invalidation reference. If price retraces to the pullback level and the breakout context remains valid (confirmation passes), the entry occurs at a smaller stop-distance.
4. Smaller stop-distance → larger position size at fixed 0.25% equity risk.
5. R3's exit machinery (`+2 R` take-profit) triggers at a smaller absolute price distance from entry. The probability that price reaches `+2 R` within 8 bars is therefore *higher* (assuming any directional follow-through occurs at all).
6. If price does not retrace (the "best" breakouts that just run), the candidate expires unfilled — **no loss is taken**. The strongest moves are the ones R2 misses, but the corresponding cost is also zero.
7. If price retraces too far (breaks the structural stop before confirmation), the candidate is either cancelled (no trade) or filled-then-stopped (small loss). The fill-rate diagnostic shows which.

The expected aggregate effect on BTC: per-trade expectancy improves because the trades that fill are entered at better prices and stopped at smaller absolute losses; aggregate edge improves because the trades that *don't* fill incur no loss; trade count drops because some signals never become trades.

### 6.2 Mechanism prediction structure

Phase 2t's expected-mechanism predictions are arranged in three falsifiable claims (the falsifiable hypothesis under §10.3 is in §10; these are *internal mechanism* predictions used to define mandatory diagnostics):

- **Claim M1 (per-trade expectancy):** Under R2 + R3, BTC per-trade expectancy improves vs R3 alone. Δexp_R3 ≥ +0.10 R is the expected magnitude (roughly the §10.3.a threshold).
- **Claim M2 (stop-out rate):** Under R2 + R3, BTC stop-exit count as a fraction of total exits is *lower* than under R3 alone. (Trades that would have stopped out under H0/R3 because of post-entry whipsaw are now either (i) not taken because no pullback, or (ii) taken at a better price and stopped at a smaller absolute loss.)
- **Claim M3 (R-distance):** Under R2 + R3, BTC mean R-distance (entry − stop, normalized by ATR at signal time) is *smaller* than under R3 alone.

If M1 fails, the framework verdict captures it as §10.3 disqualification or PROMOTE-with-caveat (similar to R1b-narrow's PASS-with-caveats). If M2 fails despite M1 passing, R2's improvement comes from a different mechanism than the entry-timing one (this would be informative — the candidate may help BTC for reasons other than reducing stop-out rate). If M3 fails, the implementation is broken (M3 is mechanically guaranteed if pullback entry is implemented correctly).

These three claims become mandatory diagnostics in the Phase 2u spec memo. They are **not** §10.3 thresholds; they are mechanism-validation cuts that interpret the framework verdict.

### 6.3 Mechanism on ETH (secondary)

ETH's directional-asymmetric regime under R3 alone (longs −0.934 / shorts +0.028) and the strong ETH-shorts result under R1a+R3 suggests R2's effect on ETH is more ambiguous:

- **ETH shorts**: pullback entry on ETH shorts captures the bearish-regime follow-through at a better price. Likely improvement; magnitude uncertain.
- **ETH longs**: catastrophic under R1a+R3. Pullback entry on ETH longs may filter out the worst trades (those that don't pull back because the longs are immediately invalidated by the bearish regime). Likely improvement *if* R2 acts as an implicit filter against bad longs; likely no effect *if* the longs that pull back also fail.
- **Aggregate ETH effect**: expected positive but smaller than BTC because ETH's direction-asymmetry under R3 is already doing most of the work. R2's ETH improvement may not clear §10.3.a's +0.10 R threshold; §10.3.c (strict dominance) is the more likely path on ETH.

§11.4's ETH-as-comparison rule requires BTC to clear §10.3 and ETH to not catastrophically fail. The expected Phase 2u/execution outcome is BTC-driven §10.3.a clearance with ETH §10.3.c clearance or modest §10.3.a clearance.

---

## 7. Expected failure modes

R2 has more failure modes than the filter-axis redesigns because the topology change introduces fill-realism and timing-interaction concerns. The list below is **expected**, not committed; each failure mode informs a mandatory diagnostic.

### 7.1 Pullback never comes (low fill rate)

**Symptom.** Fill rate (trades_filled / registered_candidates) is < 30%. The strongest breakouts are typically the ones that don't pull back; R2 selects against them.

**Mechanism interpretation.** R2 trades absolute frequency for per-trade quality. If the per-trade quality improvement is large enough, aggregate edge can still improve even with a low fill rate. If the per-trade quality improvement is too small, aggregate edge degrades (fewer winners, similar per-trade payoff).

**Diagnostic.** Mandatory fill-rate report cut. Mandatory comparison of R2-filled vs R3-filled trade outcomes on the *intersection* (trades both candidates fired on, comparing entry price differences and stop-distance differences). If R2 is filtering out the strongest moves and not improving the surviving trades' expectancy, the candidate fails the M1 mechanism prediction.

### 7.2 Pullback exceeds stop (intra-pending invalidation)

**Symptom.** A non-trivial fraction of candidates touch the pullback level and then breach the structural-stop level *before* confirmation, or touch the pullback and confirmation but produce a stop-distance below the 0.60 × ATR floor at fill time.

**Mechanism interpretation.** R2's pullback level is too close to the structural stop; the volatility of the pullback bar(s) routinely puts price below the stop level intra-bar. The trade is rejected (or filled-then-stopped immediately).

**Diagnostic.** Mandatory `expired_candidates_stop_distance_at_fill` count. Mandatory MFE/MAE distribution at fill time vs at signal time (does the pullback consume a meaningful fraction of the eventual MFE distribution?).

### 7.3 Confirmation rule too strict (low fill rate without quality gain)

**Symptom.** Fill rate is low *and* per-trade expectancy on filled trades does not improve materially over R3.

**Mechanism interpretation.** The confirmation rule rejects pullbacks that would have been profitable trades. R2 is overfitted to a specific pullback-and-bounce pattern that is rarer than the mechanism assumed.

**Diagnostic.** Compare fill-rate × per-trade-expectancy product: R2's aggregate edge is roughly fill-rate × (R2 expectancy − R3 expectancy), assuming R2 takes a subset of R3's trades. If fill-rate is low but per-trade gain doesn't compensate, R2 is strictly worse than R3.

### 7.4 Confirmation rule too loose (high fill rate without quality gain)

**Symptom.** Fill rate is high (close to 100%) and R2's per-trade behavior approaches R3's behavior.

**Mechanism interpretation.** R2 degenerates toward H0 because the confirmation rule effectively passes every signal that produces *any* pullback within the validity window, which is most signals.

**Diagnostic.** A high fill rate with neutral expR_R3 delta should be flagged as "R2 is mechanically active but functionally equivalent to R3". The candidate should not PROMOTE under §10.3.a (no per-trade expectancy gain) and likely fails §10.3.c (no strict dominance).

### 7.5 Fill-realism over-generosity (backtest-vs-live gap)

**Symptom.** Backtest results assume fills at the exact pullback level (limit fills); live execution produces partial fills, missed fills, or worse fill prices because resting limit liquidity at that level is thin.

**Mechanism interpretation.** This is the hardest failure mode to diagnose in backtest because it is a *backtest-vs-paper-shadow gap*. Phase 2u should pre-commit to the *most conservative* fill model (next-bar-open after confirmation) precisely to avoid this gap, accepting lower fill rates in exchange for fill-realism.

**Diagnostic.** Mandatory fill-model sensitivity diagnostic: run R2 with both the most-aggressive (limit-at-pullback intrabar) and the most-conservative (next-bar-open after confirmation) fill models; report the divergence. Large divergence is a red flag; small divergence increases confidence the candidate is robust to fill-realism choices.

### 7.6 The stop-out problem isn't entry timing (R2 doesn't help BTC)

**Symptom.** R2 + R3 produces a §10.3 PROMOTE under H0 anchor but a near-zero R3-anchor BTC delta — the same pattern as R1b-narrow. Trade count drops, fill rate is moderate, per-trade expectancy on BTC is unchanged.

**Mechanism interpretation.** BTC's stop-out rate is *not* primarily an entry-timing issue. The trades that stop out under H0/R3 do so because the breakout thesis was wrong on those bars, not because the entry price was suboptimal. R2 cannot fix what isn't broken in the way it assumed.

**Diagnostic.** This is the most important diagnostic for Phase 2t's GO/NO-GO logic at the *post-execution* stage. If R2 also produces an R3-anchor-neutral BTC result, the operator has now exhausted three structural axes (S, B-narrow, E) without moving BTC's per-trade expectancy. The reasonable next inference would be that the family's BTC edge is structural and not addressable from within the candidate-axis space — pointing to family-shift or operator-policy decisions outside Phase 2t's scope.

### 7.7 Trade-count fragility (worse than R1b-narrow)

**Symptom.** Per-fold trade counts collapse below R1b-narrow's already-small 0/2/1/2/3 BTC distribution. V-window has 0 or 1 trade.

**Mechanism interpretation.** R2's combined effect (signal filter via pullback-non-occurrence + stop-distance-at-fill rejection) reduces the trade pool more aggressively than R1b-narrow's bias-strength filter alone.

**Diagnostic.** Trade-count sanity-check is mandatory. If V-window BTC has 0 or 1 trade, the §11.3 V-window evidence is uninterpretable (Phase 2s already documented this for R1b-narrow). The framework PROMOTE may stand on R-window aggregate, but the absolute-edge interpretation is weakened further.

### 7.8 R3 time-stop horizon interaction (subtle)

**Symptom.** R2-filled trades that take longer to fill (later within the validity window) have fewer R3 bars to reach +2 R. The MFE distribution shows R2 trades concentrated at lower MFE values because they ran out of time.

**Mechanism interpretation.** The Phase 2u choice between "8 bars after fill" (R3-consistent) and "8 bars after signal" (lifecycle-consistent) changes this. Under "8 bars after fill", later-filling candidates have the same R3 horizon as immediate-filling candidates; under "8 bars after signal", later-filling candidates have a compressed horizon. The R3-consistent interpretation is the expected default.

**Diagnostic.** Time-to-fill distribution; per-time-to-fill expR cell.

### 7.9 Direction-specific failure (BTC longs vs shorts; ETH longs vs shorts)

**Symptom.** R2's effect is direction-asymmetric on a symbol that was previously direction-symmetric (e.g., BTC), or amplifies/reverses an existing asymmetry on ETH.

**Mechanism interpretation.** Pullback structure differs between bull and bear markets (bear-market pullbacks have different volatility profiles than bull-market pullbacks). R2's confirmation rule may fire differently on long vs short candidates. This was the failure mode that surprised Phase 2s on R1b-narrow (BTC introduced an asymmetry that wasn't predicted).

**Diagnostic.** Long/short asymmetry comparison vs R3 baseline mandatory.

---

## 8. Trade-count implications

### 8.1 Expected magnitude

R1b-narrow on R-window cut trade count by 65–70% (BTC 33 → 10; ETH 33 → 12). R1a+R3 cut by ~30% (33 → 22 BTC; 33 → 23 ETH). R2 sits between or below these depending on the specific pullback level + confirmation + validity window choices.

A descriptive estimate (not committed; for planning purposes):

- **Conservative pullback level + strict confirmation + 8-bar validity:** expected fill rate ~30–40%. R2 trade count ~10–13 BTC / ~10–13 ETH. Comparable to R1b-narrow's drop.
- **Moderate pullback level + moderate confirmation + 8-bar validity:** expected fill rate ~50–65%. R2 trade count ~17–21 BTC / ~17–21 ETH. Comparable to R1a+R3's drop.
- **Permissive pullback level + lax confirmation + 8-bar validity:** expected fill rate ~75–90%. R2 trade count ~25–30 BTC / ~25–30 ETH. Smaller drop than either prior candidate.

The Phase 2u spec memo will commit one configuration; the trade-count outcome is not predictable without execution, but it is unlikely to *exceed* H0's 33 (because R2 only filters, never adds). §10.3.b (Δn ≥ +50%) is mechanically unavailable.

### 8.2 Per-fold consistency concern

GAP-20260424-036's 5-rolling-fold convention requires meaningful per-fold sample sizes to support per-fold consistency claims. R1b-narrow's BTC per-fold counts (0/2/1/2/3) are at the lower bound of usefulness; R2 may produce similar or smaller per-fold distributions.

The Phase 2u spec memo should anticipate this and:

- Pre-declare that per-fold consistency is reported descriptively even when sample sizes are uninterpretable (treating the §11.2 fold-consistency machinery at its operational lower bound, as Phase 2s did for R1b-narrow).
- Pre-declare that V-window failure on n=1 BTC is not a §11.3 disqualification by itself — it ends the candidate's wave but does not retroactively invalidate the R-window classification.

This is exactly the discipline Phase 2s applied. R2 inherits it.

### 8.3 §10.3 path implications

With Δn likely negative, the available §10.3 paths are:

- **§10.3.a** (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05) — magnitude path. The mechanism prediction suggests this is the *expected* path: per-trade expectancy improves on BTC under the R2 thesis.
- **§10.3.c** (strict dominance: Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0) — strict-dominance path. Available as a fallback.

§10.3.b (rising trade count) is unavailable as for R1b-narrow.

The framework verdict could PROMOTE on either path. The strategic interpretation should distinguish "PROMOTE via §10.3.a with positive per-trade expectancy gain" (mechanism validated) from "PROMOTE via §10.3.c with neutral per-trade expectancy gain on R3-anchor" (similar to R1b-narrow's BTC outcome — formal pass but mechanism not validated).

### 8.4 Trade-count-driven vs mechanism-driven improvement

Phase 2s's diagnostic for R1b-narrow established a clear pattern:

| Anchor | R1b-narrow BTC Δexp |
|--------|---------------------:|
| H0     | +0.196 (formal pass) |
| R3     | −0.023 (essentially neutral) |

The H0-anchor framework verdict was driven by the trade-count concentration removing the lossiest trades; the R3-anchor view shows the surviving trades have similar per-trade behaviour. The same diagnostic must be applied to R2:

- R2 vs H0 (governing): expected to pass §10.3.a or §10.3.c.
- R2 vs R3 (descriptive): the **mechanism test**. If R2 vs R3 is materially positive on BTC (Δexp_R3 ≥ +0.10 R), the M1 mechanism prediction is validated. If R2 vs R3 is neutral on BTC (similar to R1b-narrow), R2 is exhibiting the same trade-count-reduction pattern as the filter-axis redesigns and the operator faces the same strategic interpretation question.

The Phase 2u spec memo should pre-declare both anchor cuts and pre-declare that the R3-anchor cut is the **mechanism-test reading**, even though it is not the §10.3 governing comparison.

---

## 9. Overfitting risk analysis

### 9.1 Baseline overfitting risk classification

**MODERATE.** R2 is structural (per Phase 2i §1.7.1's explicit topology-change example) but introduces 3-4 sub-parameter axes each requiring single-value commitment. The risk profile is comparable to R1a's (Phase 2j memo §C had 2 sub-parameters: percentile threshold X = 25, lookback N = 200) and lower than R1b-classifier's (which would have introduced ADX threshold + regime-classifier parameters).

### 9.2 Sub-parameter axes and anti-fitting anchors

Each of the four conceptual axes from §4.3 must be committed singularly in Phase 2u with explicit non-fitting rationale. The recommended anchors:

| Axis                          | Recommended anchor                                                                                          | Rationale shape                                                                                                                                                                                                         |
|-------------------------------|-------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Pullback level                | **Breakout level itself** (`setup_high` for longs; `setup_low` for shorts)                                   | The structural-invalidation reference of the H0 setup definition. Used unchanged from H0 setup detection. Not selected by examining R-window outcomes. The textbook "retest" interpretation.                              |
| Confirmation requirement      | **Bar-close-not-violating-stop** (close not below structural-stop level for longs; symmetric for shorts)     | The H0 stop-distance filter is already anchored to the structural-stop level. Confirming that close has not breached the stop reuses the same structural reference. Not selected by examining outcomes.                  |
| Validity window               | **8 bars** (matches `setup_size = 8` AND `exit_time_stop_bars = 8`)                                          | Two existing project conventions converge on the same value: the H0 setup-window length and the R3 unconditional time-stop horizon. Strongest non-fitting anchor available.                                                |
| Fill model                    | **Next-bar-open after confirmation**                                                                          | Matches the project's existing market-on-next-bar-open convention. Uses the same fee/slippage path. Most conservative choice on the backtest-vs-live realism axis. Avoids new bar-high/low look-ahead concerns.            |

Each anchor is taken from an **existing project value or convention**, not from an examination of R-window data. This mirrors Phase 2j memo §D.6 (R3's `R-target = 2.0 ↔ STAGE_5_MFE_R = 2.0`; `time-stop = 8 ↔ STAGNATION_BARS = 8`) and Phase 2r §F (R1b-narrow's `S = 0.0020 ↔ ATR_REGIME_MIN`).

If Phase 2u's spec memo commits these anchors, the overfitting risk is comparable to or lower than R1a's. If Phase 2u drifts toward a sweep of pullback depths (e.g., 25%, 50%, 75% of breakout-bar range) or sweeps validity windows, the overfitting risk rises substantially and Phase 2i §1.7 binding test may fail.

### 9.3 §1.7 binding test evaluation

Phase 2i §1.7.1 enumerates structural-vs-parametric criteria. For R2:

- **Rule-shape change.** YES. The entry rule changes from "fire-on-signal" to "register-and-wait-for-pullback". The functional form of the entry mechanism is different.
- **Rule-input domain change.** YES. The entry rule now consumes additional inputs: subsequent bar high/low (or close) for pullback detection; subsequent bias evaluations for cancellation; subsequent opposite-signal detection for cancellation. H0's entry rule consumes only the signal-bar's outputs.
- **Trade-lifecycle topology change.** **YES — explicitly verbatim.** Phase 2i §1.7.1's example: "replacing 'market entry on next-bar open after breakout-bar close' with 'limit-order entry at setup boundary, valid for N bars after breakout' — entry topology changes from immediate-fill to conditional-pending."

Phase 2i §1.7.2 secondary check: changing a numeric threshold while keeping the same rule shape is parametric. R2 introduces *new* sub-parameter axes (pullback level, confirmation, validity window, fill model) along with a *new* functional form. The values are parameters of the new form, not tweaks of existing parameters.

R2 passes the Phase 2i §1.7 binding test cleanly.

### 9.4 GAP dispositions

R2 affects the following GAPs (descriptive — Phase 2t does not edit the implementation-ambiguity log; Phase 2u may surface new GAPs if the spec memo identifies them):

| GAP                  | Topic                                                                                                  | R2 disposition (descriptive, planning-only)                                                                                       |
|----------------------|--------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| GAP-20260424-030     | Break-even +1.5R vs +2.0R rule-text conflict                                                            | **CARRIED.** R2 keeps R3 exit logic; conflict stays open.                                                                          |
| GAP-20260424-031     | EMA slope wording (discrete vs fitted)                                                                  | **CARRIED.** R2 does not touch bias-validity rule.                                                                                  |
| GAP-20260424-032     | Mark-price stop-trigger sensitivity                                                                     | **CARRIED-AND-MORE-RELEVANT.** R2's pullback entry typically produces smaller stop-distances; mark-price proximity matters more. Required cut. |
| GAP-20260424-033     | Stagnation window classification                                                                        | **CARRIED.** R2 keeps R3's exit logic; stagnation disposition unchanged.                                                            |
| GAP-20260424-036     | 5-rolling-fold consistency with sample-size lower-bound                                                  | **CARRIED.** R2 expected to operate at or below R1b-narrow's per-fold sample-size lower bound.                                       |
| **NEW (Phase 2u-candidate)** | **Fill-realism for limit/conditional orders**                                                  | **Phase 2u spec memo may need to introduce a new GAP entry** documenting the fill-model decision and the backtest-vs-live realism limits. To be evaluated in Phase 2u, not in Phase 2t. |

Phase 2t does not commit any GAP changes. The spec memo evaluates them.

### 9.5 Carry-forward count

Phase 2i §1.7.3 capped the carry-forward set at ≤ 2 candidates per execution wave. R2 is one candidate; combined with R3 as the locked exit baseline, the carry-forward set is [R2 + R3] = 1 active structural-redesign candidate. Within the cap.

### 9.6 BTC-primary lock compliance

R2 does not introduce symbol-conditional logic. The same pullback rule applies on BTCUSDT and ETHUSDT. §1.7.3 BTCUSDT-primary lock is preserved. (R1a's symbol-asymmetric outcome was a *result* of running a symbol-independent rule on different markets, not an explicit symbol-conditional rule. R2 expects similar — the rule is symbol-independent; the outcomes may diverge by symbol, which is then a §11.4 ETH-as-comparison evaluation, not a lock violation.)

### 9.7 Overfitting risk summary

If Phase 2u commits the recommended anchors (§9.2 table), R2's overfitting risk is **MODERATE-LOW** — comparable to R1a's commitment of `X = 25 / N = 200` and slightly higher than R1b-narrow's commitment of `S = 0.0020`. The discipline that has held through Phases 2j, 2k, 2l, 2m, 2r, 2s applies unchanged: single-axis structural change; sub-parameters committed singularly with explicit non-fitting rationale; no post-hoc tuning; falsifiable hypothesis pre-declared.

If Phase 2u drifts (sweeps; multiple anchor candidates competing; symbol-conditional rules), the risk rises and the spec memo should be rejected under the §1.7 binding test.

---

## 10. Falsifiability under §10.3 framework

### 10.1 Anchor preservation

H0 remains the sole governing anchor per Phase 2i §1.7.3. R3 is the locked exit baseline (per Phase 2p) and the supplemental descriptive comparison anchor. The candidate naming convention is "R2 on top of R3" (mirroring R1a+R3 and R1b-narrow's "X on top of R3" pattern).

### 10.2 Pre-committed §10.3 thresholds (unchanged from Phase 2f)

Applied without post-hoc loosening per Phase 2f §11.3.5:

- **§10.3 disqualification floor.** R2 + R3 fails framework if any of:
  - Δexp < 0 (worse expR than H0 on either symbol).
  - ΔPF < 0 (worse profit factor than H0 on either symbol).
  - |maxDD| ratio > 1.5× the H0 baseline (drawdown more than 1.5× worse).
- **§10.3.a magnitude path.** R2 + R3 PROMOTES if BOTH:
  - Δexp ≥ +0.10 R, AND
  - ΔPF ≥ +0.05.
- **§10.3.b rising-trade-count path.** R2 + R3 PROMOTES if ALL:
  - Δexp ≥ 0, AND
  - Δn ≥ +50%, AND
  - Δ|maxDD| ≤ +1.0 pp (drawdown not worse by more than 1 percentage point).
  - **Mechanically unavailable for R2** (Δn expected negative).
- **§10.3.c strict-dominance path.** R2 + R3 PROMOTES if ALL:
  - Δexp > 0, AND
  - ΔPF > 0, AND
  - Δ|maxDD| ≤ 0 (drawdown not worse).

§10.4 hard reject (Δn > 0 AND expR / PF worsen) is mechanically inapplicable (Δn expected negative).

§11.4 ETH-as-comparison: BTC must clear; ETH must not catastrophically fail (no §10.3 disqualification on ETH).

§11.6 cost-sensitivity (slippage LOW / MED / HIGH): R2 must not trigger §10.3 disqualification at HIGH slippage. **Particularly relevant for R2** because limit-fill assumptions interact with slippage differently than market-fill assumptions; the cost-sensitivity must be reported across multiple slippage levels even if the fill model is "next-bar-open after confirmation" (which is market-fill-equivalent and matches H0/R3's slippage profile).

§11.3 V-window: R-window PROMOTE → V-window confirmation run; V-window failure ends the candidate's wave but does not retroactively change R-window classification.

### 10.3 Pre-committed candidate falsifiable hypothesis

(To be re-stated and committed in Phase 2u; recorded here as the *expected shape* of the hypothesis the spec memo will produce.)

> **R2 hypothesis (planning-stage, not yet committed):** On R = 2022-01-01 → 2025-01-01 with v002 datasets, an R2 variant — H0 setup + H0 trigger + H0 bias + R2 conditional-pending entry topology with sub-parameters committed singularly per Phase 2u spec memo (recommended anchors per §9.2) + R3 exit logic locked + all other rules at H0 defaults — produces a §10.3-passing result vs H0 baseline.
>
> The acceptable §10.3 paths are §10.3.a (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05) or §10.3.c (strict dominance). §10.3.b is mechanically unavailable.
>
> No §10.3 disqualification floor may be triggered on either symbol. §11.4 ETH-as-comparison must be satisfied. §11.6 cost-sensitivity must clear at HIGH slippage. §11.3 V-window confirmation must be run if R-window PROMOTES.
>
> **The hypothesis is FALSIFIED if** R2 fails §10.3 on BTC OR triggers §10.3 disqualification on BTC, OR triggers §10.3 disqualification on ETH per §11.4 ETH-as-comparison rule.
>
> **The hypothesis is INDETERMINATE if** R2 clears §10.3 on R but fails on V (per §11.3 no-peeking discipline).
>
> **The mechanism is VALIDATED (separate from framework verdict) if** Δexp_R3 ≥ +0.10 R on BTC AND BTC stop-exit count fraction is materially lower under R2 than under R3 (M1 + M2 mechanism predictions per §6.2).
>
> **The mechanism is NOT VALIDATED but framework still passes** in the same pattern as R1b-narrow if Δexp_R3 ≈ 0 on BTC despite §10.3.a clearance vs H0 (improvement is trade-count-reduction-driven rather than per-trade-expectancy-driven).

### 10.4 Pre-committed candidate-specific mandatory diagnostics

(To be enumerated in Phase 2u spec memo §P-equivalent. Phase 2t records the *expected* enumeration:)

- **D.1 Fill-rate diagnostic.** `trades_filled / registered_candidates` per symbol. The single most informative R2-specific diagnostic.
- **D.2 Pullback-touch distribution.** Distribution of "bars elapsed from registration to first pullback touch" per symbol. Informs the validity window's reasonableness.
- **D.3 Stop-distance reduction.** Mean and distribution of `(R3_entry_price − stop_level) / (R2_entry_price − stop_level)` per symbol — i.e., the fraction by which R2 reduces stop distance vs R3 on the same signals. Tests M3 mechanism prediction.
- **D.4 Stop-exit count fraction.** Stop-exit count / total exit count, comparing R2 + R3 vs R3 alone vs H0. Tests M2 mechanism prediction.
- **D.5 Per-trade expectancy on intersection.** For trades that both R3 and R2+R3 fill (the intersection): compare expR. Tests whether R2's improvement (if any) is from price-improvement or selection.
- **D.6 Fill-model sensitivity.** Run R2 with both "next-bar-open after confirmation" and "limit-at-pullback intrabar" fill models; report divergence. Cost-realism diagnostic.
- **D.7 Long/short asymmetry comparison.** Per-direction expR / PF for R2 + R3 vs R3 vs H0. Catches R1b-narrow-style direction-asymmetry surprises.
- **D.8 Per-fold consistency.** GAP-036 5-rolling-fold convention applied unchanged. Per-fold trade counts and expR vs both H0 and R3 anchors. Sample-size caveats expected.
- **D.9 Per-regime expR.** Realized 1h-volatility terciles, same convention as Phase 2l / 2m / 2s.
- **D.10 MFE/MAE distribution at fill time.** Distribution of MFE and MAE measured from R2 fill price (not signal price). Compares to R3 baseline.
- **D.11 R-distance (normalized stop-distance) distribution.** Mean and quantiles of `(entry_price − stop_level) / ATR_15m_at_signal` for R2 trades; compare to R3 trades on the same signals.
- **D.12 Time-to-fill distribution.** Distribution of bars elapsed from candidate registration to fill. Informs whether the validity-window choice was binding.
- **D.13 Mark-price vs trade-price stop-trigger sensitivity** (GAP-032). Required cut; expected more sensitive than for H0/R3 because R2's smaller stop-distance is closer to mark-price tracking precision.
- **D.14 Implementation-bug check.** Zero TRAILING_BREACH / STAGNATION exits on R3-or-R2+R3 trades; H0 + R3 controls reproduce locked baselines bit-for-bit.

These diagnostics are descriptive-only at planning stage; Phase 2u commits them.

---

## 11. GO / NO-GO recommendation

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### 11.1 Conditions evaluated

| Condition                                                                                                                                                                  | Status              |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| Two filter-axis hypotheses (R1a setup-shape, R1b-narrow bias-shape) have been tested and produce trade-count-reduction-driven PROMOTEs without absolute-edge gain on BTC.   | MET (Phase 2m / 2s) |
| Operator's joint Phase 2s interpretation explicitly rules out further filter-axis work as the next direction.                                                              | MET (operator brief) |
| R2 is Phase 2i's deferred entry-mechanic candidate; addresses a structurally different failure mode (post-entry whipsaw, not selection quality).                            | MET (Phase 2i §3.2) |
| R2 passes the Phase 2i §1.7 binding test cleanly (rule-shape change; rule-input domain change; trade-lifecycle topology change — explicit verbatim §1.7.1 example).         | MET (§9.3 above)    |
| Recommended sub-parameter anchors are available from existing project conventions (breakout level; bar-close-not-violating-stop; 8-bar validity; next-bar-open fill).      | MET (§9.2 above)    |
| Backtester implementation cost is non-trivial (~1500–2500 net lines) but manageable; comparable to or larger than R3 was; cost is justified by exhausted alternatives.    | MET (§5.6 above)    |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds remain unchanged; no post-hoc loosening.                                                                                   | MET (§10.2 above)   |
| Phase 2p baseline-of-record (R3) is locked and ready to serve as the locked exit machinery for "R2 on top of R3".                                                          | MET (Phase 2p)      |
| H0 anchor preserved as sole governing comparison; R3 supplemental descriptive only.                                                                                         | MET (Phase 2i §1.7.3) |
| §1.7.3 project-level locks (BTCUSDT primary; one-position max; 0.25% risk; 2× leverage; mark-price stops; v002 datasets) preserved.                                          | MET (§9.6 above)    |
| Carry-forward count (≤ 2 candidates per wave) preserved at [R2 + R3] = 1 active structural-redesign + 1 locked exit baseline.                                                | MET (§9.5 above)    |
| Operator restrictions on Phase 4 / paper-shadow / live-readiness / MCP / credentials preserved.                                                                              | MET                 |

No condition is unmet.

### 11.2 Risks evaluated

| Risk                                                                                                                                                                         | Mitigation                                                                                                                              |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Spec memo may drift toward parametric (sweeps; multiple anchor candidates).                                                                                                  | Phase 2u spec memo enforces single-value commitment with explicit non-fitting rationale. §1.7 binding test re-evaluated in spec memo.   |
| R2 may exhibit the same trade-count-reduction-driven-PROMOTE pattern as R1b-narrow (framework PROMOTE, R3-anchor neutral).                                                    | M1/M2/M3 mechanism predictions are mandatory diagnostics. R3-anchor cut pre-declared. Distinguishes mechanism-validation from framework verdict. |
| Backtester implementation cost is higher than past phases.                                                                                                                    | Cost is acknowledged in §5.6. The cost is justified by exhausted filter-axis alternatives; the planning memo records this honestly.    |
| V-window sample sizes likely uninterpretable on BTC (n=0 or 1) at the same level as R1b-narrow's BTC V (n=1).                                                                 | Pre-declared in Phase 2u spec memo: V-window failure on n=1 ends candidate's wave but does not retroactively invalidate R-window verdict. |
| Fill-realism gap between backtest and live execution may be larger than for prior candidates.                                                                                 | Recommended fill model is the most-conservative (next-bar-open after confirmation); fill-model sensitivity diagnostic mandatory in Phase 2u. |
| If R2 + R3 also produces an R3-anchor-neutral BTC result, three structural axes are exhausted without moving BTC's per-trade expectancy — pointing toward family-shift.        | Acknowledged in §7.6. The strategic interpretation question is operator-policy, not Phase 2t's place to answer.                          |

No risk is unmitigated. All mitigations are within the existing Phase 2j-style discipline.

### 11.3 Recommendation

**GO** for Phase 2t spec-writing (a follow-on docs-only Phase 2u-style memo) **conditional on the following discipline locks for the spec memo**:

1. **Single-axis commitment.** Phase 2u writes the R2 spec only. No other candidate (R1b-classifier, R1a-prime, R2 + R1a, R2 + R1b-narrow, etc.) is considered in Phase 2u's scope.
2. **Sub-parameters committed singularly.** Each of the four axes (pullback level, confirmation, validity window, fill model) commits one value with explicit non-fitting rationale anchored to an existing project convention. Recommended anchors per §9.2 above; alternative anchors require equivalent rationale.
3. **Phase 2i §1.7 binding-test re-evaluation.** Phase 2u spec memo includes an explicit §1.7.1 / §1.7.2 evaluation showing R2 is structural, not parametric.
4. **R3 preserved as locked exit baseline.** No change to `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`. Time-stop horizon under R2 fills uses the R3-consistent interpretation ("8 bars after fill", not "8 bars after signal").
5. **Mandatory diagnostics enumerated.** Phase 2u spec memo enumerates the M1/M2/M3 mechanism predictions and the §10.4-style mandatory diagnostics (fill rate, stop-distance reduction, intersection-trades expectancy, fill-model sensitivity, per-direction asymmetry, per-fold, per-regime, MFE/MAE-at-fill, R-distance distribution, time-to-fill, mark-price sensitivity, implementation-bug check).
6. **§10.3 falsifiable hypothesis recorded.** Mirrors Phase 2r §O / Phase 2j §C.13. Explicit FALSIFIED / INDETERMINATE / mechanism-VALIDATED-vs-NOT cases stated.
7. **GAP dispositions explicit.** GAP-030 / 031 / 032 / 033 / 036 carried; new fill-realism GAP introduced if necessary in Phase 2u.
8. **Backtester cost acknowledged.** Phase 2u spec memo includes the descriptive backtester surface estimate (per §5 of this memo) so the operator can make the execution-authorization decision with full cost visibility.
9. **No execution authorization.** Phase 2u is docs-only. Execution requires a separate operator-approved Gate 1 plan after the spec memo lands (mirroring Phase 2k → Phase 2l for R3 and Phase 2r-spec → Phase 2s for R1b-narrow).
10. **Operator restrictions preserved.** No Phase 4, no paper-shadow, no live-readiness, no MCP / Graphify / `.mcp.json`, no credentials, no exchange-write, no `data/` commits, no edits to `docs/12-roadmap/technical-debt-register.md` or `.claude/`.

### 11.4 What GO does NOT mean

- **GO does not authorize Phase 2u directly.** Phase 2u is a separate operator decision after Phase 2t closure.
- **GO does not authorize execution.** Execution is a separate operator decision after Phase 2u-spec closure.
- **GO does not pre-judge the spec memo's outcome.** Phase 2u may, after full evaluation, determine that R2's anti-fitting anchors cannot be cleanly committed under §1.7 binding test (e.g., the spec drifts toward parametric or symbol-conditional logic). In that case, Phase 2u itself reaches a NO-GO and R2 returns to deferred state with documented reason.
- **GO does not change R3's baseline-of-record status.** R3 remains the locked baseline-of-record per Phase 2p. R2 + R3 is the candidate; R3 alone is the supplemental anchor.
- **GO does not change family abandonment timing.** Phase 2p §F.4 family-abandonment pre-conditions remain unchanged.

### 11.5 Fallback recommendation

If the operator judges that Phase 2u's spec-writing cost is not justified by R2's expected information value — for example, if the operator's reading of Phase 2s is that the family's BTC absolute-edge gap is structural and not addressable by *any* further structural redesign — the disciplined alternative is **NO-GO with explicit reason**:

- Phase 2t closes with the documented finding that R2 is the only remaining structural axis with a concrete deferred candidate.
- The operator's NO-GO decision is recorded as a *family-level consolidation* (not a R2-specific rejection).
- The next phase shifts to a non-R2 path: extended consolidation at R3 (Phase 2p Option A continued); or operator-policy lifts on Phase 4 / paper-shadow; or family-shift planning (Phase 2p §F.4 pre-conditions).

NO-GO is consistent with Phase 2p's "stay-paused" primary recommendation; GO is consistent with Phase 2p's "fallback" recommendation (one more docs-only spec-writing cycle for a specific deferred candidate). Both are framework-disciplined paths.

### 11.6 Recommended primary path

**GO** — Phase 2u spec-writing for R2, with the discipline locks of §11.3 above. R2 is the disciplined next candidate because:

1. It tests a structurally different lever (timing, not selection) than the two exhausted filter-axis candidates.
2. Its anti-fitting anchors are available and conservative (all four recommended values are existing project conventions).
3. Its overfitting risk is comparable to R1a's, lower than R1b-classifier's, and the §1.7 binding test passes verbatim.
4. The backtester cost is justified by the exhaustion of cheaper alternatives.
5. The framework discipline (H0 anchor; R3 locked exit; §10.3 thresholds preserved; H0 + R3 controls bit-for-bit) carries over unchanged.
6. The mechanism-validation question (M1/M2/M3 vs framework verdict) is the same question the operator faced after Phase 2s and is the natural next-test for whether the family's BTC absolute-edge gap is mechanically addressable.

Phase 2u, if authorized, produces a docs-only Phase 2j-style memo with the recommended anchors evaluated, the §1.7 binding test affirmed, the falsifiable hypothesis committed, and the mandatory diagnostics enumerated. Phase 2u itself does not authorize execution; execution is a separate Gate 1 plan after Phase 2u closure.

---

## 12. Threshold preservation

Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening. Phase 2j §C.6 R1a sub-parameters preserved (R1a is not part of R2). Phase 2j §D.6 R3 sub-parameters preserved (R3 is the locked exit baseline). Phase 2r §F R1b-narrow sub-parameter preserved (R1b-narrow is not part of R2). GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. No new GAP entries are introduced in Phase 2t. Phase 2i §1.7.3 project-level locks preserved (H0 anchor; BTCUSDT primary; ETHUSDT research/comparison only; one-position max; 0.25% risk; 2× leverage; mark-price stops; v002 datasets).

---

## 13. Wave / phase preservation

Phase 2g Wave-1 REJECT ALL preserved as historical evidence only. Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen, designated baseline-of-record per Phase 2p). Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D). Phase 2s R1b-narrow PROMOTE / PASS preserved unchanged (formal-framework-strongest result with explicit per-trade-expectancy and sample-size caveats). H0 anchor preserved as the sole §10.3 / §10.4 anchor.

---

## 14. Safety posture

Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to `.claude/`. No edits to source files, test files, scripts, datasets, or manifests. No `data/` writes. No Phase 4 work. No paper/shadow planning. No live-readiness claim. No code in Phase 2t. No backtests in Phase 2t. No parameter tuning in Phase 2t. No candidate-set widening in Phase 2t (only R2 is on the planning surface). Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as sensitivity diagnostic in any future execution wave). R3 sub-parameters frozen. R1a sub-parameters frozen. R1b-narrow sub-parameter frozen. The 8-bar setup window unchanged. No new structural redesign candidate exposed beyond H0 / R3 / R1a+R3 / R1b-narrow / R2-as-planning-surface.

---

**End of Phase 2t R2 (pullback-entry redesign) Gate 1 planning memo.** Sections 1–14 complete. R2 is defined as a single-axis structural redesign of entry-lifecycle topology — the explicit Phase 2i §1.7.1 example for trade-lifecycle topology change. Sub-parameters are NOT committed in Phase 2t; recommended anchors are described conceptually (breakout level; bar-close-not-violating-stop; 8-bar validity; next-bar-open fill) for evaluation in a follow-on Phase 2u spec memo if the operator authorizes one. R3 remains the locked exit baseline. H0 remains the sole §10.3 / §10.4 governing anchor. Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds preserved unchanged. Phase 2i §1.7.3 project-level locks preserved. Falsifiable hypothesis recorded as expected shape; will be re-stated and committed in Phase 2u. M1 / M2 / M3 mechanism predictions enumerated as mandatory diagnostics. Backtester implementation surface estimate: ~1500–2500 net lines including tests; cost justified by exhausted filter-axis alternatives.

**Recommendation: GO for Phase 2u spec-writing**, conditional on the §11.3 discipline locks (single-axis commitment; sub-parameters committed singularly with explicit non-fitting rationale; §1.7 binding-test re-evaluation; R3 preserved; mandatory diagnostics enumerated; §10.3 falsifiable hypothesis recorded; GAP dispositions explicit; backtester cost acknowledged; no execution authorization in Phase 2u; operator restrictions preserved). Fallback: NO-GO with documented family-level consolidation reason if the operator judges R2's expected information value is not justified by the backtester cost.

**No code changes after memo drafting; no new runs; no new evidence; no live-readiness claim.** Phase 2t is complete and ready for operator/ChatGPT Gate 2 review. Stop after producing this memo.
