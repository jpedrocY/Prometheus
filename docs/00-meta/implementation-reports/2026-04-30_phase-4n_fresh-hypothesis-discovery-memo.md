# Phase 4n — Fresh-Hypothesis Discovery Memo

**Authority:** Operator authorization for Phase 4n (Phase 4m §"Operator
decision menu" Option B conditional secondary alternative: docs-only
fresh-hypothesis discovery memo, conditional on operator explicitly
choosing to continue research after consolidation; operator has so
chosen). Phase 4m §"Fresh-hypothesis validity gate" (18 binding
requirements); Phase 4m §"Candidate future research spaces"
(structural-R trend continuation; regime-first breakout continuation;
funding-context trend filter; structural pullback continuation; mean-
reversion de-prioritized; market-making / HFT rejected; ML-first
rejected; paper / shadow / live forbidden); Phase 4m §"Forbidden
rescue observations" (V2 / F1 / D1-A / R2 rescue patterns explicitly
forbidden); Phase 4l (V2 backtest execution Verdict C HARD REJECT —
terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology
binding); Phase 4j §11 (metrics OI-subset partial-eligibility binding
rule); Phase 4i (V2 acquisition + integrity validation; partial pass);
Phase 4h (V2 data-requirements / feasibility); Phase 4g (V2 strategy
spec); Phase 4f (V2 hypothesis predeclaration); Phase 3v §8 (stop-
trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA
slope / stagnation governance); Phase 3r §8 (mark-price gap
governance); Phase 3t §12 (validity gate for any future ex-ante
hypothesis); Phase 3m (regime-first research framework memo;
recommend-paused precedent); Phase 3k (post-D1-A consolidation
memo); Phase 3l (external execution-cost evidence review); Phase 3e
(post-F1 consolidation memo); Phase 3c §7.3 (catastrophic-floor
predicate); Phase 2w §16.1 (R2 §11.6 cost-sensitivity FAIL); Phase 2p
§C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks);
`docs/03-strategy-research/v1-breakout-strategy-spec.md`;
`docs/03-strategy-research/v1-breakout-backtest-plan.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/timestamp-policy.md`;
`docs/04-data/dataset-versioning.md`;
`docs/07-risk/stop-loss-policy.md`;
`docs/07-risk/position-sizing-framework.md`;
`docs/07-risk/exposure-limits.md`;
`docs/12-roadmap/phase-gates.md`;
`docs/12-roadmap/technical-debt-register.md`;
`docs/00-meta/ai-coding-handoff.md`;
`docs/00-meta/implementation-ambiguity-log.md`;
`.claude/rules/prometheus-core.md`;
`.claude/rules/prometheus-safety.md`;
`.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4n — **Fresh-Hypothesis Discovery Memo** (docs-only).
Evaluates the four Phase 4m §"Candidate future research spaces"
candidates against the Phase 4m 18-requirement fresh-hypothesis
validity gate, distinguishes valid new hypothesis spaces from
forbidden rescue patterns, and recommends at most one candidate
family for a future docs-only strategy-spec phase. **Phase 4n does
NOT create a full strategy spec, run a backtest, acquire data, or
implement anything. Phase 4n is text-only.**

**Branch:** `phase-4n/fresh-hypothesis-discovery-memo`. **Memo
date:** 2026-05-02 UTC.

---

## Summary

Phase 4m's primary recommendation was **remain paused**; its
conditional secondary was a docs-only fresh-hypothesis discovery
memo only if the operator explicitly chose to continue research.
**The operator has chosen to continue.** Phase 4n is that discovery
memo.

Phase 4n evaluates the four candidate future research spaces from
Phase 4m §"Candidate future research spaces" against the Phase 4m
18-requirement fresh-hypothesis validity gate:

| Candidate | Family | Phase 4m note |
|---|---|---|
| **A** | Structural-R trend continuation | "allowed if defined from first principles, not as V2 with widened stops" |
| **B** | Regime-first breakout continuation | "possible if regime is primary design choice, not bolt-on filter; Phase 3m precedent" |
| **C** | Funding-context trend filter | "possible if funding is context, not directional trigger; structurally distinct from D1-A" |
| **D** | Structural pullback continuation | "possible if cost model and stop geometry designed together; structurally distinct from R2" |

**Phase 4n's central finding:** all four candidates have rescue
traps that must be explicitly avoided to satisfy the Phase 4m
validity gate. Two candidates (A: structural-R trend continuation
and B: regime-first breakout) are sufficiently theoretically
distinct from the cumulative project record to justify further
docs-only specification work. Two candidates (C: funding-context
filter and D: structural pullback) are weaker — C because the
funding-as-context idea was already exercised inside V2 without
being independently testable, and D because R2's failure mode
(slippage fragility under HIGH cost from entry-style change) is
inherent to pullback geometry on BTCUSDT.

**Phase 4n's primary recommendation: Phase 4o — Regime-First
Breakout Hypothesis Spec Memo (docs-only).** Regime-first breakout
continuation (Candidate B) is selected because:

1. **It has the cleanest theoretical novelty.** Regime as primary
   design choice (not bolt-on) is conceptually distinct from R1a /
   R1b-narrow (regime-as-bolt-on) and from V2 (regime-as-one-of-
   multiple-AND-gates).
2. **It has Phase 3m precedent.** The Phase 3m regime-first research
   framework memo previously identified this direction; Phase 3m
   recommended remain paused, but Phase 4n now operates in a
   different cumulative state where the operator has explicitly
   chosen to continue research.
3. **Its rescue trap is identifiable and avoidable.** The trap is
   "R1a / R1b plus another bolt-on regime gate". Avoidable by
   requiring regime to determine *whether the strategy is active at
   all*, not which trade qualifies — i.e., regime gating happens at
   the strategy-active-vs-inactive level, not at the per-bar level.
4. **Cost-sensitivity can be designed in from the start.** Regime
   determines whether to trade; outside the favorable regime, the
   strategy does NOT trade at all, naturally avoiding HIGH-cost
   margin-of-error trades.
5. **Setup / stop / target / sizing co-design is feasible per
   regime.** Inside each predeclared regime, the setup geometry can
   be calibrated to that regime's volatility and trade-frequency
   profile.

**Phase 4n's conditional secondary: remain paused.** If the operator
prefers not to continue with regime-first or any other candidate,
remain paused is the safe alternative.

**Phase 4n does NOT:**

- create V3 or any full strategy spec;
- define a threshold grid for any candidate;
- define a complete entry / exit rule set;
- run any backtest;
- run diagnostics;
- acquire or modify data;
- modify manifests;
- write implementation code;
- modify `src/prometheus/`;
- modify existing strategy specs;
- rescue V2 / F1 / D1-A / R2 in any form;
- authorize Phase 4o or any successor phase;
- authorize paper / shadow / live / exchange-write.

**Phase 4n IS:** a docs-only candidate evaluation that selects ONE
candidate family for a future docs-only strategy-spec memo (if the
operator separately authorizes Phase 4o), or recommends remain
paused if the operator prefers.

**Verification:**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No project lock changed.** **No retained verdict revised.** R3
baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 /
D1-A / V2 retained research evidence only — all preserved verbatim.

**Recommended state remains paused** outside the conditional Phase
4o spec memo. **No next phase authorized by Phase 4n.**

---

## Authority and boundary

Phase 4n operates strictly inside the post-Phase-4m-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10;
  Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t
  consolidation; Phase 3t §12 validity gate; Phase 3u §10 / §11;
  Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4a's anti-live-readiness
  statement; Phase 4d review; Phase 4e reconciliation-model design
  memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2 strategy
  spec; Phase 4h V2 data-requirements / feasibility memo; Phase 4i
  V2 acquisition + integrity validation; Phase 4j §11 metrics
  OI-subset partial-eligibility rule; Phase 4k V2 backtest-plan
  methodology; Phase 4l V2 backtest execution Verdict C HARD REJECT;
  Phase 4m post-V2 strategy research consolidation memo (18-
  requirement fresh-hypothesis validity gate).
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md`
  unchanged.
- **Project-level locks preserved verbatim.** §1.7.3.
- **Phase 2f thresholds preserved verbatim.** §11.6 = 8 bps HIGH per
  side.
- **Retained-evidence verdicts preserved verbatim.** R3 / H0 / R1a /
  R1b-narrow / R2 / F1 / D1-A / V2.
- **Safety rules preserved verbatim.**
- **MCP and secrets rules preserved verbatim.**

Phase 4n adds *only* a docs-only fresh-hypothesis discovery memo,
without modifying any prior phase memo, any data, any code under
`src/prometheus/`, any rule, any threshold, any manifest, any verdict,
any lock, or any gate.

---

## Starting state

```text
branch:           phase-4n/fresh-hypothesis-discovery-memo
parent commit:    40a29e1fce8f7b8828d208fe5ed8f1ead94f7eb9 (post-Phase-4m-merge housekeeping)
working tree:     clean before memo authoring (transient .claude/scheduled_tasks.lock + gitignored data/research/ excluded)
main:             40a29e1fce8f7b8828d208fe5ed8f1ead94f7eb9 (unchanged)

Phase 4a foundation:                                          merged.
Phase 4b/4c cleanup:                                          merged.
Phase 4d review:                                              merged.
Phase 4e reconciliation-model design memo:                    merged.
Phase 4f V2 hypothesis predeclaration:                        merged.
Phase 4g V2 strategy spec:                                    merged.
Phase 4h V2 data-requirements / feasibility memo:             merged.
Phase 4i V2 public data acquisition + integrity:              merged (partial-pass).
Phase 4j V2 metrics data governance memo:                     merged (Phase 4j §11 binding).
Phase 4k V2 backtest-plan memo:                               merged.
Phase 4l V2 backtest execution:                               merged (Verdict C HARD REJECT).
Phase 4m post-V2 strategy research consolidation memo:        merged.

Repository quality gate:           fully clean.
research thread (5m):              operationally complete and closed (Phase 3t).
v002 datasets:                     locked; manifests untouched.
v001-of-5m datasets:               trade-price research-eligible; mark-price research_eligible:false.
Phase 4i datasets:                 30m + 4h klines × 2 research-eligible; metrics × 2 NOT research-eligible.
```

---

## Why this memo exists

Phase 4m closed the post-V2 retrospective consolidation with a
binary recommendation:

- **Option A (PRIMARY):** remain paused.
- **Option B (CONDITIONAL SECONDARY):** authorize a separate docs-only
  fresh-hypothesis discovery memo only if the operator explicitly
  chose to continue research.

The operator has chosen Option B. Phase 4n is that discovery memo.

The job of Phase 4n is narrow: **evaluate the four Phase 4m candidate
spaces against the Phase 4m 18-requirement fresh-hypothesis validity
gate, identify rescue-risk traps, and recommend at most one
candidate for a future docs-only strategy-spec phase.**

Phase 4n is NOT:

- a strategy spec (no thresholds, no complete rule set);
- a feasibility study (no data acquisition, no backtest);
- an authorization (no successor phase started).

Phase 4n IS:

- a candidate evaluation against the Phase 4m gate;
- a rescue-risk analysis;
- a single recommendation (or remain-paused fallback).

The discipline behind Phase 4n is the same anti-data-snooping
discipline applied at every prior research-direction selection
(Phase 3a F1 discovery; Phase 3f D1-A discovery; Phase 4f V2
discovery). The selection of a future direction must be conceptually
grounded *before* any spec, threshold, or data is touched, so that
when a future Phase 4o spec memo (if authorized) is briefed, the
direction has already been justified on theory.

---

## Relationship to Phase 4m

- **Phase 4m consolidated the full strategy-research arc** (H0 / R3 /
  R1a / R1b-narrow / R2 / F1 / D1-A / 5m diagnostics / V2).
- **Phase 4m's primary recommendation was remain paused.**
- **Phase 4m's conditional secondary** was a docs-only fresh-
  hypothesis discovery memo if the operator explicitly chose to
  continue research.
- **The operator has chosen to continue.**
- **Phase 4n must operate under the Phase 4m 18-requirement fresh-
  hypothesis validity gate** (recapitulated in §"Fresh-hypothesis
  validity gate recap" below).

**Phase 4m verdict preservation (verbatim):**

- **H0 remains FRAMEWORK ANCHOR.**
- **R3 remains BASELINE-OF-RECORD.**
- **R1a remains RETAINED — NON-LEADING.**
- **R1b-narrow remains RETAINED — NON-LEADING.**
- **R2 remains FAILED — §11.6.**
- **F1 remains HARD REJECT.**
- **D1-A remains MECHANISM PASS / FRAMEWORK FAIL.**
- **5m thread remains CLOSED operationally.**
- **V2 remains HARD REJECT — structural CFP-1 critical.**
- **No verdict is revised.**
- **No project lock is changed.**

Phase 4n does NOT modify Phase 4m. Phase 4m text remains verbatim.
Phase 4n applies Phase 4m's fresh-hypothesis validity gate to the
four Phase 4m candidate spaces.

---

## Fresh-hypothesis validity gate recap

The 18 binding requirements from Phase 4m, restated as the Phase 4n
scoring basis:

1. **Named as a new hypothesis, not a rescue label.** Names like
   "V2.1", "V2-prime", "V2-modified" are forbidden. The hypothesis
   must have a distinct name and a distinct conceptual foundation.
2. **Specified before any data is touched.** No exploratory plotting
   / aggregating / backtest runs of the new direction before
   predeclaration.
3. **Explains why it is new in theory, not just a parameter tweak.**
   The conceptual basis must distinguish it from R3 / R2 / R1a /
   R1b-narrow / F1 / D1-A / V2.
4. **Defines entry, stop, target, sizing, cost, timeframe, and exit
   together.** The five-element co-design (Phase 4m §"Stop / target /
   sizing lessons") must be done from first principles.
5. **Predeclares data requirements** (analogous to Phase 4h).
6. **Predeclares mechanism checks** (analogous to Phase 4g §30 M1 /
   M2 / M3).
7. **Predeclares pass / fail gates** including catastrophic-floor
   predicates.
8. **Predeclares forbidden comparisons and forbidden rescue
   interpretations** (specific to the new hypothesis).
9. **Does NOT choose thresholds from prior failed outcomes.**
10. **Does NOT use Phase 4l root-cause analysis as a direct
    optimization target.**
11. **Preserves §11.6 cost sensitivity.** No relaxation.
12. **Preserves project locks and governance.** §1.7.3, mark-price
    stops, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 3r §8, Phase 4j
    §11, Phase 4k methodology.
13. **Commits to predeclared chronological train / validation / OOS
    holdout windows.**
14. **Commits to deflated Sharpe / PBO / CSCV correction** if grid
    search is involved.
15. **Distinguishes mechanism evidence from framework promotion.**
16. **Preserves BTCUSDT-primary / ETHUSDT-comparison protocol.**
17. **Does NOT propose live-readiness or paper / shadow / Phase 4
    canonical** as part of its first phase.
18. **Satisfies separate operator authorization** as a separately
    briefed phase.

A candidate that fails ANY of these is not a valid fresh hypothesis.

Phase 4n's scoring of each candidate is grounded in the
designability of these requirements at the candidate-family level,
NOT at any specific threshold / parameter level (which is Phase 4o's
job, if Phase 4o is ever authorized).

---

## Discovery method

Phase 4n applies a structured evaluation method:

1. **For each of the four Phase 4m candidate spaces (A / B / C / D),
   write a candidate description** consisting of:
   - core idea (verbatim from Phase 4m §"Candidate future research
     spaces");
   - distinguishing-feature claim (what makes it conceptually new);
   - nearest forbidden rescue trap (and how to avoid it);
   - rough mechanism question (what would M1 / M2 / M3 look like);
   - rough data-feasibility note (what data would be needed; whether
     existing v002 / v001-of-5m / Phase 4i datasets suffice);
   - rough cost-sensitivity discussion (how would §11.6 HIGH be
     accommodated).
2. **Assign qualitative scores** on the 10 dimensions in §"Candidate
   scoring matrix" using {Strong, Moderate, Weak, High risk, Reject}.
3. **Identify the strongest candidate by qualitative aggregation.**
   Tied candidates are broken by:
   - rescue-risk (lower is better);
   - new-theory strength (higher is better);
   - co-design clarity (higher is better);
   - data feasibility (higher is better).
4. **Write the recommendation** with a clear primary and at most one
   conditional secondary.
5. **Identify what Phase 4n does NOT authorize.**

**Phase 4n does NOT use numeric optimization or backtest-derived
scoring.** All scoring is qualitative and derived from the cumulative
research record (R2 cost-fragility; F1 catastrophic-floor; D1-A
mechanism / framing mismatch; V2 design-stage incompatibility;
5m diagnostic findings; Phase 3l external cost evidence; Phase 3m
regime-first precedent).

---

## Candidate pool considered

The four Phase 4m candidate spaces (A / B / C / D) are the entire
candidate pool for Phase 4n. No other candidates are evaluated;
Phase 4m §"Candidate future research spaces" already filtered out
mean-reversion (de-prioritized), market-making / HFT (rejected for
Prometheus), ML-first black-box forecasting (rejected for now), and
paper / shadow / live (forbidden).

The four candidates:

| Candidate | Family | Phase 4m note |
|---|---|---|
| A | Structural-R trend continuation | "allowed if defined from first principles, not as V2 with widened stops" |
| B | Regime-first breakout continuation | "possible if regime is primary design choice, not bolt-on filter; Phase 3m precedent" |
| C | Funding-context trend filter | "possible if funding is context, not directional trigger; structurally distinct from D1-A" |
| D | Structural pullback continuation | "possible if cost model and stop geometry designed together; structurally distinct from R2" |

Each candidate is evaluated below. The de-prioritized / rejected
spaces are listed in §"De-prioritized / rejected spaces".

---

## Candidate A — Structural-R trend continuation

**Phase 4m one-liner:** "allowed if defined from first principles,
not as V2 with widened stops".

### Core idea

Trend continuation where the structural invalidation point, stop
distance, target logic, time stop, and position sizing are designed
together from first principles. The five-element co-design (per
Phase 4m §"Stop / target / sizing lessons") is the central design
discipline.

The hypothesis is that **a trend-continuation strategy whose stop
geometry is explicitly co-designed with its setup window can produce
a viable trade rate at acceptable cost-sensitivity, where V1 / R3
(short setup, fixed bounds) and V2 (long setup, V1-inherited bounds)
each have specific limitations**.

### Distinguishing-feature claim

- **NOT V2 with widened stops.** Candidate A defines its stop /
  target / sizing from first principles; it does not start from V2's
  Donchian setup and then loosen the stop filter to admit V2's
  rejected candidates.
- **NOT R3 / V1 with extended setup.** Candidate A does not start
  from V1's 8-bar setup and stretch it; instead, it asks "given the
  fixed-R + time-stop exit family is canonical (R3 baseline-of-record),
  what setup window N produces a stop / target geometry compatible
  with the empirical win-rate distribution and §11.6 HIGH cost?"
- **NOT a parameter tweak of any prior strategy.** Candidate A is a
  primary co-design exercise, not a tweak.

### Nearest forbidden rescue trap

**"V2 but with a wider stop filter."** This is the most obvious
trap. Avoidable by:

- **Not using Phase 4l forensic numbers as design inputs.** The
  observed 3-5 × ATR distribution in V2 forensics CANNOT inform
  Candidate A's stop bounds.
- **Not starting from V2's Donchian setup.** Candidate A's setup
  geometry must be designed from first principles (e.g., from
  trend-persistence literature: Moskowitz / Ooi / Pedersen 2012;
  Hurst / Ooi / Pedersen 2017) without reference to V2's specific
  20/40-bar Donchian choice.
- **Not using V2's 8-feature AND chain.** Candidate A's entry
  conditions must be designed independently.

A second trap is "R3 / V1 with extended setup window". Avoidable by
NOT using V1's 8-bar baseline as the comparison reference for
Candidate A's setup window choice.

### Rough mechanism question

For Candidate A, M1 / M2 / M3 might look like:

- **M1 (price-structure):** does the trend-continuation entry
  produce ≥ 50% trades reaching +N × R MFE (where N depends on the
  strategy's chosen target ratio) before stop, on BOTH BTCUSDT and
  ETHUSDT, on OOS data?
- **M2 (setup-geometry):** does the explicitly-co-designed
  stop / target geometry produce stat-significant expectancy uplift
  vs. a degenerate variant with V1-style stop bounds applied to
  Candidate A's setup, on BOTH symbols, with bootstrap-CI lower
  bound > 0?
- **M3 (cost-resilience):** does Candidate A pass §11.6 HIGH
  cost-survival on BTCUSDT primary?

These are *rough sketches*; Phase 4n does NOT predeclare M1 / M2 /
M3 thresholds for Candidate A. That is Phase 4o's job (if Phase 4o
is ever authorized).

### Rough data-feasibility note

Candidate A's data requirements likely overlap with V1 / V2: kline
data at the chosen signal timeframe + HTF bias timeframe + funding
data (for funding cost in P&L). Whether 15m / 30m / 1h / 4h kline
data is needed depends on Phase 4o's setup-window choice.

- **15m + 1h:** v002 datasets cover this (R3 / V1 / F1 / D1-A
  basis).
- **30m + 4h:** Phase 4i datasets cover this (V2 basis;
  research-eligible).
- **1h + 4h:** v002 1h + Phase 4i 4h cover this.
- **4h + daily:** would require new daily acquisition.

If Phase 4o chooses a timeframe outside existing data, a separate
docs-only Phase 4o-data-requirements memo would be needed (analogous
to Phase 4h). If Phase 4o reuses existing data, no new acquisition
is needed.

### Rough cost-sensitivity discussion

Candidate A's §11.6 HIGH cost-survival depends on:

- **Trade frequency:** wider setup windows → wider stops → fewer
  trades per year → smaller per-year cost burden BUT also smaller
  sample size for DSR / PBO / CSCV.
- **Per-trade R unit cost:** at HIGH-slip = 8 bps per side, the
  per-trade cost in R units = (16 + 16) bps × entry_price / R / 10000
  ≈ 0.0032 × entry_price / R. For a 1-ATR stop on BTC at $60K with
  ATR ≈ $300, cost ≈ $192 per trade per BTC, or ≈ 0.64 R. For a
  3-ATR stop, cost ≈ 0.21 R. Wider stops have LOWER per-trade R cost.
- **But a 3-ATR stop with fixed +2R target requires a 6-ATR move for
  TP** — substantially less frequent than a 1-ATR stop with 2R
  target (2-ATR move). Trade frequency matters more than per-trade
  R cost at the framework-promotion level.

The Phase 4o brief, if authorized, would have to commit to a setup-
window choice and demonstrate at the brief-time level (without
backtesting) that the resulting trade-frequency × per-trade-R-cost
math is plausible.

### Validity gate scorecard (Candidate A)

| Gate # | Requirement | Score | Note |
|---|---|---|---|
| 1 | Named as new hypothesis | **Strong** | "Structural-R trend continuation" is a distinct name |
| 2 | Specified before data | **Strong** | Phase 4o would predeclare before any new data work |
| 3 | New in theory | **Moderate** | Trend continuation is a known broad family; the "new" part is the explicit co-design discipline |
| 4 | Five-element co-design | **Strong** | Co-design IS the candidate's central design choice |
| 5 | Predeclares data requirements | **Strong** | Phase 4h template applies directly |
| 6 | Predeclares mechanism checks | **Strong** | M1 / M2 / M3 framework reusable |
| 7 | Predeclares pass / fail gates | **Strong** | Phase 4k CFP-1..CFP-12 framework reusable |
| 8 | Predeclares forbidden rescue interps | **Strong** | "V2 but wider stop" trap is well-defined |
| 9 | Does NOT choose thresholds from failed outcomes | **High risk** | Most obvious risk: temptation to use Phase 4l forensics |
| 10 | Does NOT use Phase 4l root-cause as optimization target | **High risk** | Same |
| 11 | Preserves §11.6 | **Strong** | No relaxation contemplated |
| 12 | Preserves project locks | **Strong** | All Phase 3v / 3w / 3r / Phase 4j §11 / Phase 4k preserved |
| 13 | Predeclared chronological windows | **Strong** | Phase 4k methodology applies |
| 14 | DSR / PBO / CSCV | **Strong** | Framework reusable |
| 15 | Mechanism vs. framework promotion | **Strong** | Distinction preserved |
| 16 | BTCUSDT-primary / ETHUSDT-comparison | **Strong** | §1.7.3 preserved |
| 17 | No live-readiness in first phase | **Strong** | Docs-only spec phase |
| 18 | Separate operator authorization | **Strong** | Phase 4o brief required |

**Net assessment:** Candidate A is procedurally feasible. **Rescue-
risk is the central concern.** Candidate A is the closest of the
four candidates to V2; the operator and any future Phase 4o brief
must be vigilant about the "V2 with widened stops" trap.

---

## Candidate B — Regime-first breakout continuation

**Phase 4m one-liner:** "possible if regime is primary design choice,
not bolt-on filter; Phase 3m precedent".

### Core idea

Regime detection (volatility regime, trend regime, funding regime,
or a composite regime classifier) is the **primary design choice**.
A breakout continuation strategy is only **active inside specific
predeclared regimes**. The strategy does NOT trade outside those
regimes — not because of a per-bar filter, but because the strategy
itself is dormant.

This is **categorically different** from R1a (volatility-percentile
setup predicate at the per-bar level), R1b-narrow (bias-strength
threshold at the per-bar level), and V2 (regime as one of multiple
AND gates that all evaluate per-bar).

The hypothesis is that **trend-continuation breakouts have
qualitatively different post-trade distributions in different
regimes, and a strategy that only operates in favorable regimes —
ignoring all other bars entirely — can outperform a strategy that
tries to filter per-bar inside a single timeframe**.

### Distinguishing-feature claim

- **NOT R1a / R1b plus another bolt-on regime filter.** Candidate B
  does not add a filter to V1 / R3; it makes regime the primary
  design choice. Outside the favorable regime, the strategy is
  inactive.
- **NOT V2 with regime as one of 8 gates.** Candidate B's regime
  classification operates at the strategy-active-vs-inactive level,
  not at the per-bar AND-gate level.
- **NOT 5m diagnostics converted to rules.** Q1–Q7 informative
  findings are NOT used as regime signals (Phase 3o §6 forbidden
  question forms).
- **Phase 3m precedent.** The Phase 3m regime-first research
  framework memo previously identified this direction. Phase 3m
  recommended remain paused at that time. Phase 4n now operates in
  a different cumulative state (post-V2 HARD REJECT) where the
  operator has explicitly chosen to continue research.

### Nearest forbidden rescue trap

**"R1a / R1b-narrow but with another bolt-on regime filter."** This
is the most obvious trap. Avoidable by:

- **Defining regime as a top-level state machine.** The strategy is
  in one of `{regime_active, regime_inactive}` states; in the
  inactive state, no signals are generated regardless of bar-level
  conditions.
- **Defining regime classifier independently of any per-bar trade
  trigger.** The regime classifier may use features (e.g., HTF
  trend slope, volatility percentile, funding pathology) but it
  produces a binary regime state, not a per-bar gate.
- **Not using V1's 8-bar setup as a baseline reference.** Candidate
  B's regime-active-window setup geometry must be designed from
  first principles for that specific regime.

A second trap is "regime classifier overfits the historical regime
distribution". Avoidable by chronological train / validation / OOS
holdout discipline (Phase 4k methodology applies).

A third trap is "regime classifier becomes a 5m-diagnostics-derived
indicator". Avoidable by NOT using Q1 / Q2 / Q3 / Q6 informative
findings as regime indicators (Phase 3o §6 forbidden question
forms).

### Rough mechanism question

For Candidate B, M1 / M2 / M3 might look like:

- **M1 (regime-state-conditional price-structure):** does the
  breakout entry produce ≥ X% trades reaching +N × R MFE INSIDE the
  predeclared favorable regime, on BOTH BTCUSDT and ETHUSDT, OOS?
  And does it FAIL to do so in the predeclared unfavorable regime
  (negative test)?
- **M2 (regime-vs-no-regime):** does the regime-conditional strategy
  produce stat-significant expectancy uplift vs. the same strategy
  without the regime gate (i.e., always-active baseline), on BOTH
  symbols?
- **M3 (regime-classifier robustness):** is the regime classifier
  itself stable across train / validation / OOS windows? (A
  classifier that defines different regimes in different windows is
  unreliable.)

The negative-test component of M1 (strategy must FAIL in unfavorable
regime) is a stronger validity claim than V2's M1 (strategy must
PASS in single timeframe). It catches over-broad regime
classifications.

### Rough data-feasibility note

Candidate B's data requirements depend on the regime-classifier
design:

- **Volatility regime:** can be derived from existing v002 15m / 1h
  klines (ATR, realized volatility) — no new data needed.
- **Trend regime:** can be derived from existing v002 1h klines or
  Phase 4i 4h klines (EMA, slope) — no new data needed.
- **Funding regime:** can be derived from existing v002 funding
  manifests — no new data needed.
- **Composite regime:** combines the above — no new data needed.

**Existing data should suffice for most plausible regime-classifier
designs.** No mark-price 30m / 4h, no aggTrades, no spot data, no
metrics ratio columns needed for the regime classifier itself.

The breakout-continuation entry inside the favorable regime may
require additional data depending on Phase 4o's design choice
(timeframe, features). Most plausible designs reuse v002 / Phase 4i
existing data.

### Rough cost-sensitivity discussion

Candidate B has a structural cost-sensitivity advantage:

- **Outside the favorable regime, the strategy does not trade.** Zero
  trades = zero cost burden in those windows.
- **Inside the favorable regime, trade frequency is bounded by the
  regime's prevalence.** If the favorable regime occupies (e.g.)
  30% of the historical window, the strategy is active for 30% of
  the time and accumulates costs accordingly.
- **The regime classification itself can be cost-sensitivity-aware.**
  A favorable regime can be defined as "high realized volatility +
  positive trend + non-pathological funding" — empirically a
  smaller fraction of total time, but with cleaner signal-to-noise
  and lower cost-fragility.

This contrasts favorably with Candidate A (single-timeframe always-
active) and Candidate D (pullback geometry with inherent cost-
fragility).

### Validity gate scorecard (Candidate B)

| Gate # | Requirement | Score | Note |
|---|---|---|---|
| 1 | Named as new hypothesis | **Strong** | "Regime-first breakout continuation" is distinct |
| 2 | Specified before data | **Strong** | Phase 4o would predeclare |
| 3 | New in theory | **Strong** | Regime-first as PRIMARY (not bolt-on) is a categorically different design |
| 4 | Five-element co-design | **Strong** | Co-design happens per regime |
| 5 | Predeclares data requirements | **Strong** | Phase 4h template applies; mostly reuses existing data |
| 6 | Predeclares mechanism checks | **Strong** | M1 / M2 / M3 framework + negative-test component reusable |
| 7 | Predeclares pass / fail gates | **Strong** | Phase 4k CFP-1..CFP-12 framework reusable |
| 8 | Predeclares forbidden rescue interps | **Strong** | Three traps identified above |
| 9 | Does NOT choose thresholds from failed outcomes | **Moderate** | Some risk if classifier uses observed-regime statistics |
| 10 | Does NOT use Phase 4l root-cause as optimization target | **Strong** | No direct dependency on Phase 4l |
| 11 | Preserves §11.6 | **Strong** | No relaxation contemplated |
| 12 | Preserves project locks | **Strong** | All preserved |
| 13 | Predeclared chronological windows | **Strong** | Phase 4k methodology applies |
| 14 | DSR / PBO / CSCV | **Strong** | Framework reusable; smaller variant grid likely |
| 15 | Mechanism vs. framework promotion | **Strong** | Distinction preserved + negative-test sharpens it |
| 16 | BTCUSDT-primary / ETHUSDT-comparison | **Strong** | §1.7.3 preserved |
| 17 | No live-readiness in first phase | **Strong** | Docs-only spec phase |
| 18 | Separate operator authorization | **Strong** | Phase 4o brief required |

**Net assessment:** Candidate B is procedurally feasible AND
theoretically novel. **Rescue-risk is moderate but identifiable.**
The "regime as primary, not bolt-on" discipline is the central
distinguishing feature; it must be airtight in any future Phase 4o
brief.

---

## Candidate C — Funding-context trend filter

**Phase 4m one-liner:** "possible if funding is context, not
directional trigger; structurally distinct from D1-A".

### Core idea

Funding-rate is used as a **context filter** (avoid trading when
funding is in pathological extremes) on top of an otherwise
trend-continuation strategy. Funding does NOT determine direction
(unlike D1-A, where funding-rate Z-score signaled contrarian
direction). Funding does NOT determine entry timing (unlike D1-A,
where entry happened at funding-settlement time).

The hypothesis is that **a trend-continuation strategy that avoids
trading during pathological funding extremes (where reversion
pressure is strongest) outperforms the same strategy without the
filter, on a §11.6-cost-survival basis**.

### Distinguishing-feature claim

- **NOT D1-A.** D1-A used funding as the primary directional trigger
  (|Z_F| ≥ 2.0 → enter contrarian). Candidate C uses funding only
  as a context filter on a different primary signal (trend
  continuation).
- **NOT D1-A-prime / D1-B / D1-A with extra filters.** Candidate C
  is not D1-A with the contrarian framing replaced; it is a
  trend-continuation strategy with an additional funding-context
  gate.
- **NOT V1 / R3 + funding filter as bolt-on.** Candidate C must be
  designed from first principles, not as "V1 plus a funding gate".
- **Conceptually similar to V2's funding-rate-percentile band gate**
  (Phase 4g §17 sub-component (b)), which was one of V2's 8 entry
  features. **However, V2 produced 0 trades, so the funding-as-
  context contribution was never independently evaluated.** Candidate
  C is the first independent test of funding-as-context in a
  trend-continuation framework.

### Nearest forbidden rescue trap

**"D1-A but with extra filters" or "D1-A-prime".** This is the most
obvious trap. Avoidable by:

- **Not using D1-A's |Z_F| ≥ 2.0 directional rule.** Candidate C
  uses funding only to determine whether to trade at all, not which
  direction.
- **Not entering at funding-settlement time.** Candidate C's entry
  timing is determined by the trend-continuation signal, not by the
  funding cycle.
- **Not framing the funding gate as a contrarian signal.** Candidate
  C's funding gate is a "do not trade in pathological funding"
  filter, not a "trade contrarian when funding is extreme" trigger.

A second trap is "V2 funding band re-extracted as a standalone
strategy". Avoidable by NOT importing V2's specific funding
percentile bands ([20, 80] or [30, 70]) as Candidate C's bounds.
Candidate C must define its bounds from first principles.

A third trap is "Phase 4l forensic V2 funding usage as Candidate C
optimization target". Avoidable by not referencing V2's empirical
funding distribution as a design input.

### Rough mechanism question

For Candidate C, M1 / M2 / M3 might look like:

- **M1 (price-structure trend continuation):** does the underlying
  trend-continuation entry produce ≥ X% trades reaching +N × R MFE,
  on BOTH symbols, OOS — *with the funding context filter active*?
- **M2 (funding-context value-add):** does the funding-context-
  filtered strategy produce stat-significant expectancy uplift vs.
  the same strategy without the funding filter, on BOTH symbols?
- **M3 (funding-context cost-resilience):** does the funding-context
  filter improve §11.6 HIGH cost-survival vs. the always-active
  baseline?

### Rough data-feasibility note

Candidate C's data requirements:

- **v002 funding manifests:** sufficient. Existing data.
- **Underlying trend-continuation strategy data:** depends on Phase
  4o design (likely 15m / 30m + 1h / 4h klines from v002 or Phase
  4i).
- **No new acquisition needed** for the funding-context component.

### Rough cost-sensitivity discussion

Candidate C's §11.6 HIGH cost-survival depends on:

- **The underlying trend-continuation strategy's cost profile.**
  Inherits from the chosen base strategy.
- **The funding-context filter's reduction in trade frequency.** A
  filter that excludes (e.g.) 30% of trades reduces the cost burden
  by ~30% but ALSO reduces sample size by ~30%.
- **Whether the excluded trades have systematically worse expectancy
  at HIGH cost.** This is the central empirical question; only Phase
  4o + a future backtest would answer it.

### Validity gate scorecard (Candidate C)

| Gate # | Requirement | Score | Note |
|---|---|---|---|
| 1 | Named as new hypothesis | **Moderate** | "Funding-context trend filter" is a distinct name but functionally adjacent to D1-A |
| 2 | Specified before data | **Strong** | Phase 4o would predeclare |
| 3 | New in theory | **Moderate** | Funding-as-context was already a V2 component (untested due to 0 trades); the "new" part is making it standalone |
| 4 | Five-element co-design | **Moderate** | Funding filter is a component, not the central design choice |
| 5 | Predeclares data requirements | **Strong** | v002 funding sufficient |
| 6 | Predeclares mechanism checks | **Strong** | M1 / M2 / M3 framework reusable |
| 7 | Predeclares pass / fail gates | **Strong** | Phase 4k CFP-1..CFP-12 framework reusable |
| 8 | Predeclares forbidden rescue interps | **Strong** | Three traps identified above |
| 9 | Does NOT choose thresholds from failed outcomes | **High risk** | Temptation to use D1-A or V2 funding statistics |
| 10 | Does NOT use Phase 4l root-cause as optimization target | **Moderate** | Direct dependency on Phase 4l V2 funding feature |
| 11 | Preserves §11.6 | **Strong** | No relaxation contemplated |
| 12 | Preserves project locks | **Strong** | All preserved |
| 13 | Predeclared chronological windows | **Strong** | Phase 4k methodology applies |
| 14 | DSR / PBO / CSCV | **Strong** | Framework reusable |
| 15 | Mechanism vs. framework promotion | **Strong** | Distinction preserved |
| 16 | BTCUSDT-primary / ETHUSDT-comparison | **Strong** | §1.7.3 preserved |
| 17 | No live-readiness in first phase | **Strong** | Docs-only spec phase |
| 18 | Separate operator authorization | **Strong** | Phase 4o brief required |

**Net assessment:** Candidate C is procedurally feasible but
theoretically less novel. **Rescue-risk is moderate-to-high.** The
funding-as-context idea was already a component of V2 (untested due
to V2's 0 trades), so making it standalone is conceptually closer
to "V2 component extracted" than to a genuinely new direction.

---

## Candidate D — Structural pullback continuation

**Phase 4m one-liner:** "possible if cost model and stop geometry
designed together; structurally distinct from R2".

### Core idea

Pullback / retest continuation strategy where the cost model, stop
geometry, and execution timing are designed together from first
principles. R2's failure mode (slippage fragility under HIGH cost
from entry-style change) is the central design constraint to be
overcome.

The hypothesis is that **a pullback-continuation strategy that
explicitly models the entry-time slippage interaction (rather than
inheriting V1 / R3 cost assumptions) and chooses pullback-confirmation
geometry that minimizes adverse-execution-time exposure can produce
viable §11.6 HIGH cost-survival on BTCUSDT**.

### Distinguishing-feature claim

- **NOT R2.** R2 used a specific pullback-retest entry style with V1
  cost assumptions. Candidate D explicitly models entry-time
  slippage at the pullback-confirmation moment.
- **NOT R2 with cheaper costs.** §11.6 HIGH = 8 bps per side is
  preserved verbatim. Candidate D's edge cannot come from cost
  relaxation.
- **NOT R2 with more trade-quality filters.** Candidate D's design
  starts from the cost model and stop geometry, not from R2's entry
  signal plus filters.

### Nearest forbidden rescue trap

**"R2 but with lower assumed costs."** This is the most obvious trap.
Avoidable by:

- **Preserving §11.6 HIGH = 8 bps per side verbatim.** No relaxation.
- **Modeling entry-time slippage explicitly,** not assuming V1 / R3
  cost-cell mapping.
- **Designing pullback-confirmation geometry such that the
  entry-time microstructure is similar to V1 breakout-bar entries,**
  not the less-liquid intra-trade-cycle moments R2 used.

A second trap is "R2 with extra filters". Avoidable by NOT starting
from R2's pullback-retest signal and adding filters; Candidate D's
entry signal is designed from first principles.

A third trap is "R2's pullback semantics applied to V2's Donchian
setup". Avoidable by NOT importing V2's Donchian-setup-window
choice as Candidate D's setup geometry.

### Rough mechanism question

For Candidate D, M1 / M2 / M3 might look like:

- **M1 (pullback-confirmation price-structure):** does the
  pullback-confirmation entry produce ≥ X% trades reaching +N × R
  MFE, on BOTH symbols, OOS?
- **M2 (cost-modeling value-add):** does Candidate D's explicit
  entry-time slippage model produce stat-significant expectancy
  uplift vs. a degenerate variant using V1 / R3 cost-cell mapping?
- **M3 (cost-resilience under HIGH-slip):** does Candidate D pass
  §11.6 HIGH on BTCUSDT — the gate that R2 failed?

### Rough data-feasibility note

Candidate D's data requirements:

- **v002 15m / 1h klines:** sufficient for R2-style pullback signals.
- **Phase 4i 30m / 4h klines:** sufficient for V2-style timeframes.
- **5m or 1m kline data for entry-time slippage modeling:** v001-of-
  5m datasets exist (Phase 3q acquisition); 1m would require new
  acquisition.
- **mark-price data for slippage realism:** v002 mark-price 15m
  exists; v001-of-5m mark-price has known integrity gaps (Phase 3r
  §8 governance).
- **aggTrades for tick-level slippage modeling:** would require new
  acquisition (Phase 4h §7.E deferred).

If Candidate D requires aggTrades, a separate Phase 4o-data-
requirements memo would be needed (analogous to Phase 4h). If
Candidate D reuses existing data, no new acquisition.

### Rough cost-sensitivity discussion

Candidate D's central design challenge is **proving that an
explicitly-modeled entry-time slippage approach produces a
qualitatively different cost-survival outcome than R2's V1-cost-
mapped approach**.

This is harder than it appears. R2's failure pattern (HIGH cost
breaks marginal expectancy) reflects a real microstructure effect
on BTCUSDT futures: pullback-entry timing tends to occur during
liquidity-thin moments. **Improving the cost model only helps if
the underlying microstructure can be exploited** — e.g., by
choosing a pullback-confirmation criterion that systematically
falls in a different microstructure window.

### Validity gate scorecard (Candidate D)

| Gate # | Requirement | Score | Note |
|---|---|---|---|
| 1 | Named as new hypothesis | **Moderate** | "Structural pullback continuation" is a distinct name but R2-adjacent |
| 2 | Specified before data | **Strong** | Phase 4o would predeclare |
| 3 | New in theory | **Weak** | Pullback continuation is well-explored; the "new" part is the cost-model discipline, which is methodological |
| 4 | Five-element co-design | **Moderate** | Cost model is central but other elements may inherit |
| 5 | Predeclares data requirements | **Moderate** | May need aggTrades or 1m data |
| 6 | Predeclares mechanism checks | **Strong** | M1 / M2 / M3 framework reusable |
| 7 | Predeclares pass / fail gates | **Strong** | Phase 4k CFP-1..CFP-12 framework reusable |
| 8 | Predeclares forbidden rescue interps | **Strong** | Three traps identified above |
| 9 | Does NOT choose thresholds from failed outcomes | **High risk** | Temptation to use R2 specific failures as design targets |
| 10 | Does NOT use Phase 4l root-cause as optimization target | **Strong** | No direct dependency on Phase 4l |
| 11 | Preserves §11.6 | **Strong** | §11.6 = 8 bps HIGH preserved |
| 12 | Preserves project locks | **Strong** | All preserved |
| 13 | Predeclared chronological windows | **Strong** | Phase 4k methodology applies |
| 14 | DSR / PBO / CSCV | **Strong** | Framework reusable |
| 15 | Mechanism vs. framework promotion | **Strong** | Distinction preserved |
| 16 | BTCUSDT-primary / ETHUSDT-comparison | **Strong** | §1.7.3 preserved |
| 17 | No live-readiness in first phase | **Strong** | Docs-only spec phase |
| 18 | Separate operator authorization | **Strong** | Phase 4o brief required |

**Net assessment:** Candidate D is procedurally feasible but
**theoretically weak**. The novelty claim ("explicit entry-time
slippage modeling") is methodological rather than structural; the
underlying strategy family is the same as R2. **Rescue-risk is high
because R2 is structurally close** — even with a different cost
model, Candidate D's framework-level success depends on the same
microstructure fact that R2 failed on.

---

## De-prioritized / rejected spaces

Per Phase 4m §"Candidate future research spaces" (preserved
verbatim):

### Mean-reversion (de-prioritized)

- **F1 hard-rejected.** Future use requires materially new thesis.
- **Phase 4n does NOT consider mean-reversion as an immediate next
  research space.** The four candidates (A / B / C / D) are all
  trend-continuation or related; mean-reversion is outside Phase
  4n's scope.

### Market-making / HFT (rejected)

- **Phase 4f §"transferable vs. non-transferable institutional
  families"** classified HFT / liquidity-provision as non-transferable
  to Prometheus's substrate.
- **Phase 4n does NOT reconsider this.**

### ML-first black-box forecasting (rejected)

- **Phase 4f §"V2 non-goals"** excluded ML-first; project remains
  rules-based per §1.7.3.
- **Phase 4n does NOT reconsider this.**

### V2-prime / V2-narrow / V2-relaxed / V2 hybrid (forbidden)

- **Phase 4l verdict + Phase 4m §"Forbidden rescue observations"**
  explicitly forbid V2 rescue.
- **Phase 4n does NOT consider V2 rescue.**

### F1 rescue (forbidden)

- **Phase 3d-B2 / Phase 3e / Phase 3k / Phase 4m** preserve F1 HARD
  REJECT and forbid F1-prime / F1 with extra filters / F1 hybrid.
- **Phase 4n does NOT consider F1 rescue.**

### D1-A rescue (forbidden)

- **Phase 3j / Phase 3k / Phase 4m** preserve D1-A MECHANISM PASS /
  FRAMEWORK FAIL — other and forbid D1-A-prime / D1-B / D1-A with
  extra filters / V1-D1 hybrid / F1-D1 hybrid.
- **Phase 4n does NOT consider D1-A rescue.**

### R2 rescue (forbidden)

- **Phase 2w §16.1 / Phase 4m** preserve R2 FAILED — §11.6 and forbid
  R2 with cheaper costs.
- **Phase 4n does NOT consider R2 rescue.**

### 5m-only scalping (forbidden)

- **Phase 3o §6 / Phase 3t** preserve 5m as diagnostic-only.
- **Phase 4n does NOT consider 5m-only scalping.**

### Paper / shadow / live (forbidden)

- **Per `docs/12-roadmap/phase-gates.md`.**
- **Phase 4n does NOT consider paper / shadow / live.**

---

## Candidate scoring matrix

Qualitative ratings: **Strong**, **Moderate**, **Weak**, **High
risk**, **Reject**. No numeric optimization. No backtest-derived
scoring.

| Dimension | A: Structural-R | B: Regime-first | C: Funding-context | D: Structural pullback |
|---|---|---|---|---|
| **New-theory strength** | Moderate | **Strong** | Moderate | Weak |
| **Rescue-risk** | High risk (V2-adjacent) | Moderate | Moderate-to-high (D1-A / V2-component-adjacent) | High risk (R2-adjacent) |
| **Co-design clarity** | Strong (co-design IS the central choice) | Strong (co-design happens per regime) | Moderate (filter is a component) | Moderate (cost model central but rest inherits) |
| **Data feasibility** | Strong (existing v002 / Phase 4i suffice for most timeframes) | Strong (existing data sufficient for regime classifier) | Strong (v002 funding sufficient) | Moderate (may need aggTrades or 1m) |
| **Mechanism-check clarity** | Strong (M1/M2/M3 framework directly applicable) | **Strong (M1/M2/M3 + negative-test enriches the framework)** | Strong (M1/M2/M3 applicable) | Strong (M1/M2/M3 applicable) |
| **Cost-risk plausibility** | Moderate (depends on setup-window / target geometry) | **Strong (regime gate naturally avoids HIGH-cost margin trades)** | Moderate (depends on funding-filter trade-frequency reduction) | Weak (R2-style cost-fragility risk inherent) |
| **Expected sample-size feasibility** | Moderate (depends on setup-window choice) | Moderate (regime prevalence × signal density) | Moderate (depends on filter strictness) | Moderate (depends on pullback-confirmation strictness) |
| **Compatibility with project constraints** | Strong | Strong | Strong | Strong |
| **Research value** | Moderate (would clarify setup-stop co-design) | **Strong (would test regime-as-primary claim, an unexplored Prometheus design space)** | Moderate (would isolate funding-as-context value) | Weak (would primarily be a cost-model methodological exercise) |
| **Recommended / Not recommended** | Conditionally OK | **Recommended (primary)** | Not recommended now | Not recommended now |

### Tie-breaking rationale

A and B are both procedurally feasible and theoretically
non-trivial. The tie-breakers favor B:

- **Rescue-risk:** B (moderate) < A (high risk).
- **New-theory strength:** B (Strong) > A (Moderate).
- **Co-design clarity:** B (Strong, per regime) ~ A (Strong, central
  choice).
- **Cost-risk plausibility:** B (Strong) > A (Moderate).

C and D have higher rescue-risk and lower theoretical novelty than
A and B; not recommended now. Either could be revisited in a future
phase if the operator chooses.

---

## Rescue-risk analysis

Per-candidate nearest-forbidden-rescue trap and avoidance pattern:

### Candidate A — Structural-R trend continuation

- **Trap:** "V2 but with a wider stop filter."
- **Avoidance:**
  - Do not start from V2's Donchian setup;
  - Do not use Phase 4l forensic numbers (3-5 × ATR observed
    distribution) as design inputs;
  - Design setup geometry from first principles using
    trend-persistence literature, not internal V2 evidence;
  - Design stop / target / sizing co-design from first principles;
  - Predeclare bounds before any data is touched.

### Candidate B — Regime-first breakout continuation

- **Trap:** "R1a / R1b-narrow but with another bolt-on regime
  filter."
- **Avoidance:**
  - Define regime as a top-level state machine (active / inactive),
    not a per-bar gate;
  - Define regime classifier independently of any per-bar trade
    trigger;
  - Do not use V1's 8-bar setup as a baseline reference;
  - Do not use 5m diagnostic findings (Q1–Q7) as regime indicators;
  - Predeclare regime classifier before any data is touched.

### Candidate C — Funding-context trend filter

- **Trap:** "D1-A but with extra filters" / "D1-A-prime".
- **Avoidance:**
  - Do not use D1-A's |Z_F| ≥ 2.0 directional rule;
  - Do not enter at funding-settlement time;
  - Do not frame the funding gate as a contrarian signal;
  - Do not import V2's funding percentile bands as Candidate C
    bounds;
  - Predeclare funding-context bounds from first principles.

### Candidate D — Structural pullback continuation

- **Trap:** "R2 but with lower assumed costs."
- **Avoidance:**
  - Preserve §11.6 HIGH = 8 bps per side verbatim;
  - Model entry-time slippage explicitly;
  - Design pullback-confirmation geometry such that entry-time
    microstructure is similar to V1 breakout-bar entries;
  - Do not start from R2's pullback-retest signal and add filters;
  - Predeclare cost model and stop geometry before any data is
    touched.

---

## Data-readiness implications

### Candidate A — Structural-R trend continuation

- **15m + 1h:** v002 datasets cover this.
- **30m + 4h:** Phase 4i datasets cover this.
- **1h + 4h:** v002 1h + Phase 4i 4h cover this.
- **4h + daily:** would require new daily acquisition (out-of-scope
  unless Phase 4o brief authorizes).

### Candidate B — Regime-first breakout continuation

- **Volatility regime classifier:** v002 15m / 1h klines (ATR,
  realized volatility) — sufficient.
- **Trend regime classifier:** v002 1h klines / Phase 4i 4h klines
  (EMA, slope) — sufficient.
- **Funding regime classifier:** v002 funding manifests — sufficient.
- **Composite regime classifier:** combines above — sufficient.
- **Underlying breakout-continuation entry data:** depends on Phase
  4o design choice.
- **No new acquisition needed for the regime classifier itself.**

### Candidate C — Funding-context trend filter

- **v002 funding manifests:** sufficient.
- **Underlying trend-continuation strategy data:** depends on Phase
  4o design.
- **No new acquisition needed for the funding-context component.**

### Candidate D — Structural pullback continuation

- **v002 15m / 1h klines:** sufficient for R2-style pullback signals.
- **Phase 4i 30m / 4h klines:** sufficient for V2-style timeframes.
- **5m kline data for entry-time slippage modeling:** v001-of-5m
  exists.
- **mark-price data for slippage realism:** v002 mark-price 15m
  exists; v001-of-5m mark-price has known integrity gaps (Phase 3r
  §8).
- **aggTrades for tick-level slippage modeling:** would require new
  acquisition.
- **May need new data acquisition** depending on Phase 4o design.

**Phase 4n's data-readiness conclusion:** Candidates A, B, C are
likely data-feasible with existing v002 / Phase 4i / v001-of-5m
datasets. Candidate D may require new data acquisition (aggTrades
or 1m), which would add a Phase 4h-equivalent step.

---

## Stop / target / sizing co-design implications

### Candidate A

The five-element co-design (setup window, structural stop, target
ratio, time stop, position sizing) IS the central design choice.
A future Phase 4o brief for Candidate A would have to demonstrate
that the chosen co-design produces:

- **Plausible trade frequency** (sample size sufficient for DSR /
  PBO / CSCV at Phase 4k methodology);
- **Plausible per-trade R cost** at HIGH-slip (8 bps per side);
- **Plausible win rate × target ratio breakeven** (math compatible
  with empirical ATR / volatility distributions on BTCUSDT).

### Candidate B

Co-design happens *per regime*. Inside the favorable regime, the
setup / stop / target / sizing are calibrated to that regime's
volatility and trade-frequency profile. Outside the regime, the
strategy is dormant.

A future Phase 4o brief for Candidate B would have to demonstrate
that the regime-conditional co-design produces:

- **Plausible regime prevalence × signal density × per-trade R cost
  math** at HIGH-slip;
- **Stable regime classifier** across train / validation / OOS
  windows;
- **Distinguishable regime states** (negative-test component of M1).

### Candidate C

Co-design happens primarily at the underlying trend-continuation
level. The funding-context filter is a component, not the central
design choice. A future Phase 4o brief for Candidate C would have
to demonstrate that:

- **The underlying trend-continuation strategy** has plausible
  cost-survival math;
- **The funding-context filter** systematically excludes higher-
  HIGH-cost trades, not arbitrary trades.

### Candidate D

Co-design centers on the cost model and stop geometry. A future
Phase 4o brief for Candidate D would have to demonstrate that:

- **The explicit entry-time slippage model** produces materially
  different cost predictions than R2's V1-cost-mapping;
- **The pullback-confirmation geometry** systematically falls in
  liquidity-rich microstructure windows, not the less-liquid windows
  R2 used.

---

## Cost-sensitivity implications

§11.6 = 8 bps HIGH per side is preserved verbatim across all
candidates. No relaxation. Per-candidate cost-sensitivity profile:

### Candidate A

**Cost survival depends on setup-window choice.** Trade-off:

- **Wider setup → wider stop → lower per-trade R cost BUT lower
  trade frequency BUT smaller absolute target requires same-N R move
  at lower frequency.**
- The math must close: per-year (trade count × per-trade R after
  cost) > 0 with statistical significance.

### Candidate B

**Cost survival has a structural advantage.** Outside the favorable
regime, the strategy doesn't trade — automatic cost avoidance in
unfavorable regimes. Inside the favorable regime, the strategy
operates with whatever cost-survival math its internal design
produces.

This is the strongest cost-sensitivity profile of the four
candidates.

### Candidate C

**Cost survival depends on whether the funding-context filter
excludes HIGH-cost trades systematically.** If the filter
empirically excludes (e.g.) 30% of trades AND those excluded trades
are systematically HIGH-cost-fragile, the filter improves cost
survival. If the excluded trades are a random fraction, the filter
doesn't help.

The empirical question can only be answered by a future backtest;
Phase 4o brief level can only commit to predeclared filter bounds.

### Candidate D

**Cost survival is the central concern.** R2 failed on §11.6 HIGH;
Candidate D must improve on R2 specifically at the cost-survival
level. This is a difficult bar.

---

## Mechanism-check implications

Phase 4g §30 M1 / M2 / M3 framework is reusable for all four
candidates with adaptations:

### Candidate A (M1 / M2 / M3 sketch)

- **M1:** does the trend-continuation entry produce ≥ 50% trades
  reaching +0.5R MFE on BOTH symbols, OOS?
- **M2:** does the explicitly-co-designed stop / target geometry
  produce stat-significant expectancy uplift vs. a degenerate variant
  with V1-style stop bounds?
- **M3:** does Candidate A pass §11.6 HIGH cost-survival on BTCUSDT?

### Candidate B (M1 / M2 / M3 sketch with negative-test)

- **M1 (regime-conditional + negative-test):** strategy produces
  ≥ X% trades reaching +N × R MFE INSIDE favorable regime, AND fails
  to do so OUTSIDE favorable regime.
- **M2 (regime-vs-no-regime):** regime-conditional strategy produces
  stat-significant expectancy uplift vs. always-active baseline.
- **M3 (regime-classifier robustness):** classifier is stable across
  train / validation / OOS windows.

### Candidate C (M1 / M2 / M3 sketch)

- **M1:** underlying trend-continuation produces ≥ X% trades
  reaching +N × R MFE WITH funding-context filter active.
- **M2:** funding-filtered strategy produces stat-significant
  expectancy uplift vs. unfiltered baseline.
- **M3:** funding filter improves §11.6 HIGH cost-survival.

### Candidate D (M1 / M2 / M3 sketch)

- **M1:** pullback-confirmation entry produces ≥ X% trades reaching
  +N × R MFE on BOTH symbols.
- **M2:** explicit entry-time slippage model produces stat-
  significant expectancy uplift vs. V1-cost-mapping baseline.
- **M3:** Candidate D passes §11.6 HIGH on BTCUSDT — the gate that
  R2 failed.

**Phase 4n does NOT predeclare M1 / M2 / M3 thresholds for any
candidate.** That is Phase 4o's job (if Phase 4o is ever
authorized). The sketches above are conceptual placeholders to
demonstrate that the M1 / M2 / M3 framework is reusable, not
authoritative.

---

## Final discovery recommendation

### Primary recommendation

**Phase 4o — Regime-First Breakout Hypothesis Spec Memo (docs-only).**

Selecting **Candidate B (Regime-first breakout continuation)** for a
future docs-only strategy-spec memo on the basis of:

- **strongest theoretical novelty** (regime-as-primary is a
  categorically different design from R1a / R1b-narrow / V2);
- **moderate rescue-risk** (lower than A's V2-adjacent and D's
  R2-adjacent traps);
- **strong cost-sensitivity profile** (regime gate naturally avoids
  HIGH-cost margin trades);
- **strong data-readiness** (existing v002 / Phase 4i datasets
  sufficient for the regime classifier itself);
- **enriched mechanism-check framework** (negative-test component
  sharpens M1 validity);
- **Phase 3m precedent** (regime-first research framework memo
  already identified this direction; Phase 3m's "remain paused"
  recommendation is now superseded by the operator's explicit
  choice to continue research).

**The future Phase 4o brief, if authorized, MUST include:**

- **Regime classification framework** (volatility regime, trend
  regime, funding regime, or composite — to be specified in Phase
  4o, not in Phase 4n);
- **Strategy-active vs. strategy-inactive state machine** with
  predeclared transitions;
- **Inside-regime entry / stop / target / sizing co-design** from
  first principles per regime;
- **Cost-sensitivity argument** at brief-time level (§11.6 HIGH);
- **Forbidden rescue interpretations** (no R1a / R1b-narrow bolt-on
  rescue; no V2 hybrid; no 5m-diagnostic-derived regime indicators;
  no Phase 4l forensic optimization);
- **Predeclared validity gate** (Phase 4m 18 requirements satisfied);
- **No data acquisition** authorized by Phase 4o brief; if
  Phase 4o's design requires data not in v002 / Phase 4i / v001-of-
  5m, a separate Phase 4o-data-requirements memo (analogous to Phase
  4h) would be needed.

**Phase 4n does NOT authorize Phase 4o.** Phase 4n recommends Phase
4o as the operator's PRIMARY next-step option. Phase 4o
authorization is a separate operator decision.

### Conditional secondary recommendation

**Remain paused.**

If the operator prefers not to continue with regime-first or any
other candidate, remain paused is the safe alternative. Phase 4n's
Candidate B recommendation does not foreclose remain paused; it
only identifies Candidate B as the strongest fresh-hypothesis
candidate among the four Phase 4m spaces.

### Other options NOT recommended

- **Phase 4o on Candidate A (Structural-R trend continuation):**
  procedurally feasible but rescue-risk is too close to V2.
  Acceptable as a third-priority option only if the operator wishes
  to pursue the setup-stop co-design discipline as the central
  research question.
- **Phase 4o on Candidate C (Funding-context trend filter):** the
  funding-as-context idea was already a V2 component; making it
  standalone is conceptually closer to "V2 component extracted"
  than a genuinely new direction. Not recommended now.
- **Phase 4o on Candidate D (Structural pullback continuation):**
  R2-adjacent rescue-risk is too high; the theoretical novelty is
  primarily methodological. Not recommended now.

### Explicitly REJECTED options

- **Immediate strategy spec / V3 / V4 authoring.** REJECTED. Phase
  4n is consolidation only.
- **V2 amendment / V2 rescue.** REJECTED.
- **Backtest authorization.** REJECTED.
- **Implementation authorization.** REJECTED.
- **Data acquisition authorization.** REJECTED.
- **Paper / shadow / live / exchange-write.** FORBIDDEN.
- **Phase 4 canonical.** Per `docs/12-roadmap/phase-gates.md`.

---

## What this does not authorize

Phase 4n explicitly does NOT authorize, propose, or initiate any of
the following:

- **Phase 4o or any successor phase.** Authorization is a separate
  operator decision.
- **V3 or any full strategy spec.** Phase 4n is candidate evaluation
  only; it does not create a strategy.
- **Threshold definition** for any candidate.
- **Complete entry / exit rule set** for any candidate.
- **V2 rescue in any form.** V2-prime / V2-narrow / V2-relaxed / V2
  hybrid all forbidden.
- **F1 / D1-A / R2 rescue in any form.** All forbidden.
- **Phase 4g V2 strategy-spec amendment.** Preserved verbatim.
- **Phase 4j §11 metrics OI-subset rule amendment.** Preserved
  verbatim.
- **Phase 4k V2 backtest-plan methodology amendment.** Preserved
  verbatim.
- **§11.6 / §1.7.3 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r
  §8 modification.** All preserved verbatim.
- **R3 baseline-of-record revision.** Preserved.
- **H0 framework anchor revision.** Preserved.
- **V1 strategy spec revision.** Preserved.
- **5m research thread reopening.** Phase 3t closure preserved.
- **Phase 3o §6 forbidden question form revision.** Preserved.
- **Q1–Q7 conversion to rules.** Forbidden.
- **Mark-price 30m / 4h acquisition.** Deferred per Phase 4h §20.
- **`aggTrades` acquisition.** Deferred per Phase 4h §7.E.
- **v003 dataset creation.** Not authorized.
- **Manifest modification.** All Phase 4i / v002 / v001-of-5m
  manifests preserved verbatim.
- **Live exchange-write capability, production Binance keys,
  authenticated APIs, private endpoints, user stream, WebSocket,
  listenKey lifecycle, production alerting, Telegram / n8n
  production routes, MCP, Graphify, `.mcp.json`, credentials.** None
  touched.
- **Reconciliation implementation.** Phase 4e design preserved
  verbatim, not implemented.
- **Paper / shadow / live-readiness / deployment.** Not authorized.
- **Phase 4 (canonical).** Per `docs/12-roadmap/phase-gates.md`.

---

## Forbidden-work confirmation

- **No Phase 4o / Phase 4 canonical / successor phase started.**
- **No V3 or any new strategy spec authored.**
- **No V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec
  authored.**
- **No F1 / D1-A / R2 rescue spec authored.**
- **No threshold grid defined.**
- **No complete entry / exit rule set defined.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No `.claude/rules/**` modification.**
- **No data acquired.**
- **No data modified.**
- **No public Binance endpoint consulted in code.**
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4n performs no network
  I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No diagnostics run.**
- **No Phase 3o / 3p Q1–Q7 question rerun.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No `scripts/phase4l_v2_backtest.py` execution.**
- **No data acquisition / download / patch / regeneration /
  modification.**
- **No data manifest modification.** All
  `data/manifests/*.manifest.json` preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No Phase 4i manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A / V2 all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4k V2 backtest-plan methodology modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k / 4l / 4m text
  modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive
  change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4n branch.** Per Phase 4n brief.
- **No optional ratio-column access in any code.** Phase 4n is
  text-only.
- **No merge to main.**
- **No successor phase started.**

---

## Remaining boundary

- **Recommended state:** **paused** (with conditional Phase 4o
  authorization available if operator chooses).
- **Phase 4n output:** docs-only fresh-hypothesis discovery memo +
  Phase 4n closeout artefact.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified at Phase 4n start).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4m all merged. Phase
  4n discovery memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Metrics OI-subset partial-eligibility governance:** Phase 4j §11
  (preserved verbatim).
- **V2 backtest methodology governance:** Phase 4k (preserved
  verbatim).
- **V2 first-spec terminal verdict:** Phase 4l Verdict C HARD REJECT
  (preserved verbatim).
- **Phase 4m post-V2 strategy research consolidation:** complete
  (preserved verbatim).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j)
  + backtest-plan binding (Phase 4k) + executed (Phase 4l) →
  **Verdict C HARD REJECT, terminal for V2 first-spec; consolidated
  by Phase 4m**.
- **Fresh-hypothesis discovery direction:** evaluated by Phase 4n
  (this phase); **Candidate B (Regime-first breakout continuation)**
  recommended as primary candidate for a future docs-only Phase 4o
  strategy-spec memo, conditional on separate operator authorization.
- **OPEN ambiguity-log items after Phase 4n:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2
  HARD REJECT (Phase 4l, structural CFP-1 critical, terminal for V2
  first-spec); §11.6 = 8 bps HIGH per side; §1.7.3 project-level
  locks; mark-price stops; v002 verdict provenance; Phase 3q
  mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4n/fresh-hypothesis-discovery-memo` exists
  locally and (after push) on `origin`. NOT merged to main.

---

## Operator decision menu

### Option A — Phase 4o on Candidate B (PRIMARY RECOMMENDATION)

Authorize a separate **docs-only** Phase 4o — Regime-First Breakout
Hypothesis Spec Memo. Phase 4o would predeclare the regime
classifier (independent of any per-bar trade trigger), the
strategy-active vs. strategy-inactive state machine, the
inside-regime co-designed entry / stop / target / sizing, the
cost-sensitivity argument, and the forbidden rescue interpretations.
Phase 4o would NOT acquire data, NOT run backtests, NOT implement
code, NOT propose paper / shadow / live.

### Option B — Remain paused (CONDITIONAL SECONDARY)

If the operator prefers not to commit to any candidate, remain
paused is the safe alternative.

### Option C — Phase 4o on Candidate A (NOT RECOMMENDED FIRST)

Procedurally feasible but rescue-risk too close to V2; only as a
third-priority option.

### Option D — Phase 4o on Candidate C (NOT RECOMMENDED NOW)

Funding-as-context conceptually adjacent to V2 component / D1-A; not
recommended now.

### Option E — Phase 4o on Candidate D (NOT RECOMMENDED NOW)

R2-adjacent; theoretical novelty primarily methodological.

### Option F — Immediate strategy spec / V3 (REJECTED)

Phase 4n is candidate evaluation only.

### Option G — V2 / F1 / D1-A / R2 rescue (REJECTED / FORBIDDEN)

Per Phase 4m §"Forbidden rescue observations".

### Option H — Paper / shadow / live / exchange-write / Phase 4 canonical (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`.

### Phase 4n recommendation

**Phase 4n recommendation: Option A (Phase 4o on Candidate B —
Regime-First Breakout Hypothesis Spec Memo, docs-only) primary;
Option B (remain paused) conditional secondary.** Options C / D / E
not recommended. Options F / G / H rejected / forbidden.

---

## Next authorization status

**No next phase has been authorized.** Phase 4n's recommendation is
**Option A (Phase 4o on Candidate B) as primary**, with **Option B
(remain paused) as conditional secondary**. The operator must
separately authorize Phase 4o.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.

The 5m research thread remains operationally complete and closed
(per Phase 3t). The implementation-readiness boundary remains
reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding
governance blockers remain RESOLVED at the governance level (per
Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented
(per Phase 4a). The Phase 4b script-scope quality-gate restoration
is complete (per Phase 4b). The Phase 4c state-package quality-gate
residual cleanup is complete (per Phase 4c). The Phase 4d
post-4a/4b/4c review is complete (per Phase 4d). The Phase 4e
reconciliation-model design memo is complete (per Phase 4e). The
Phase 4f V2 hypothesis predeclaration is complete (per Phase 4f).
The Phase 4g V2 strategy spec is complete (per Phase 4g). The Phase
4h V2 data-requirements / feasibility memo is complete (per Phase
4h). The Phase 4i V2 public data acquisition + integrity validation
is complete (per Phase 4i; partial-pass). The Phase 4j V2 metrics
data governance memo is complete (per Phase 4j; Phase 4j §11
binding). The Phase 4k V2 backtest-plan memo is complete (per
Phase 4k; methodology binding). The Phase 4l V2 backtest execution
is complete (per Phase 4l; Verdict C HARD REJECT terminal for V2
first-spec). The Phase 4m post-V2 strategy research consolidation
memo is complete (per Phase 4m). The Phase 4n fresh-hypothesis
discovery memo is complete on this branch (this phase).

**Recommended state remains paused outside the conditional Phase 4o
spec memo. No next phase authorized.**
