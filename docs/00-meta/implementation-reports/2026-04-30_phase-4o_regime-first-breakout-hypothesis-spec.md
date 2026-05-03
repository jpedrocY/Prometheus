# Phase 4o — Regime-First Breakout Hypothesis Spec Memo

**Authority:** Operator authorization for Phase 4o (Phase 4n
§"Operator decision menu" Option A primary recommendation: Phase 4o
— Regime-First Breakout Hypothesis Spec Memo on Phase 4n Candidate B,
docs-only). Phase 4n (fresh-hypothesis discovery memo; Candidate B
selected as primary); Phase 4m §"Fresh-hypothesis validity gate"
(18 binding requirements); Phase 4m §"Forbidden rescue observations"
(V2 / F1 / D1-A / R2 rescue patterns explicitly forbidden); Phase 4l
(V2 backtest execution Verdict C HARD REJECT — terminal for V2
first-spec); Phase 4k (V2 backtest-plan methodology binding); Phase
4j §11 (metrics OI-subset partial-eligibility binding rule); Phase
4i (V2 acquisition + integrity validation; partial pass); Phase 4h
(V2 data-requirements / feasibility); Phase 4g (V2 strategy spec);
Phase 4f (V2 hypothesis predeclaration); Phase 3v §8 (stop-trigger-
domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope /
stagnation governance); Phase 3r §8 (mark-price gap governance);
Phase 3t §12 (validity gate for any future ex-ante hypothesis);
Phase 3m (regime-first research framework memo precedent); Phase 3k
(post-D1-A consolidation memo); Phase 3l (external execution-cost
evidence review); Phase 3e (post-F1 consolidation memo); Phase 3c
§7.3 (catastrophic-floor predicate); Phase 2w §16.1 (R2 §11.6
cost-sensitivity FAIL); Phase 2p §C.1 (R3 baseline-of-record); Phase
2i §1.7.3 (project-level locks);
`docs/03-strategy-research/v1-breakout-strategy-spec.md`;
`docs/03-strategy-research/v1-breakout-backtest-plan.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/live-data-spec.md`;
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

**Phase:** 4o — **Regime-First Breakout Hypothesis Spec Memo**
(docs-only). Defines a genuinely new ex-ante regime-first breakout
continuation research direction (G1) from first principles. **Phase
4o does NOT run a backtest, run diagnostics, acquire data, modify
data, modify manifests, write implementation code, modify
`src/prometheus/`, create a runnable strategy, create V3
implementation, or authorize paper / shadow / live / exchange-write.
Phase 4o is text-only.**

**Branch:** `phase-4o/regime-first-breakout-hypothesis-spec`. **Memo
date:** 2026-05-02 UTC.

---

## Summary

Phase 4o defines **G1 — Regime-First Breakout Continuation**, a
genuinely new ex-ante research candidate selected by Phase 4n as
the primary fresh-hypothesis direction after Phase 4l's V2 HARD
REJECT and Phase 4m's consolidation. G1 is conceptually distinct
from every prior Prometheus strategy line:

- **G1 ≠ R1a / R1b-narrow.** R1a / R1b-narrow apply per-bar regime
  predicates as bolt-on filters on top of the V1 framework. G1
  defines regime as a **top-level state machine**: outside the
  active regime, the strategy is **completely inactive** and
  evaluates **no** entry conditions.
- **G1 ≠ V2.** V2's 8-feature AND chain combined regime-related
  features (HTF bias, volatility band, funding band) with breakout
  / participation features at the per-bar level. G1 separates regime
  detection (top-level state machine) from inside-regime entry
  evaluation.
- **G1 ≠ F1 / D1-A / R2.** G1 is a trend-continuation breakout
  family conceptually, not a mean-reversion / contrarian / pullback-
  retest family. Inside-regime entry geometry is co-designed from
  first principles per Phase 4m §"Stop / target / sizing lessons".

**G1's central claim:** breakout continuation may be viable only
when the market is already in a predeclared favorable regime, where
the regime classifier:

1. **operates exclusively on prior-completed data** (no lookahead);
2. **does not depend on the presence or absence of a per-bar
   breakout signal** (orthogonal to the entry trigger);
3. **classifies the market into a small set of mutually exclusive
   states** (`regime_inactive`, `regime_candidate`, `regime_active`,
   `regime_cooldown` / `regime_suspended`);
4. **only enables strategy activity inside `regime_active`** —
   outside that state, no entry signals are generated, no orders are
   placed, no position is opened.

**Phase 4o is hypothesis-spec, not strategy-spec.** Phase 4o
defines:

- the hypothesis name (G1);
- the conceptual core hypothesis;
- the regime-first design principle;
- the regime state machine at conceptual level (states, transitions,
  forbidden behaviors);
- regime classifier design constraints (allowed / forbidden inputs;
  binding rules);
- candidate regime dimensions (qualitative evaluation, no thresholds);
- inside-regime breakout concept (no concrete entry rules);
- entry / stop / target / sizing co-design principles per Phase 4m;
- cost-sensitivity argument (§11.6 preserved);
- data-readiness assessment (existing v002 / Phase 4i sufficient
  for most plausible classifier designs);
- mechanism-check framework (M1 / M2 / M3 + negative-test);
- pass / fail gate framework;
- 12 catastrophic-floor predicates (analogous to Phase 4k);
- forbidden rescue interpretations.

**Phase 4o does NOT define:**

- final regime classifier formula or thresholds;
- final regime state-machine transition thresholds;
- final signal timeframe / HTF timeframe choices;
- final inside-regime breakout setup geometry;
- final stop / target / sizing thresholds;
- threshold grid;
- exact data requirements (deferred to a future Phase 4p data
  decision);
- exact mechanism-check pass thresholds (placeholders only);
- exact pass / fail gate numerical bounds (placeholders only).

These are explicitly deferred to a future **Phase 4p — G1 Strategy
Spec Memo (docs-only)**, which Phase 4o recommends but does NOT
authorize. Phase 4p authorization is a separate operator decision.

**Phase 4o preserves verbatim:**

- R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
  F1 / D1-A / V2 retained research evidence only;
- §11.6 = 8 bps HIGH per side;
- §1.7.3 project-level locks (BTCUSDT primary live; ETHUSDT
  research / comparison only; one position max; 0.25% risk; 2×
  leverage cap; mark-price stops; v002 verdict provenance);
- Phase 3q mark-price 5m manifests `research_eligible: false`;
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule;
- Phase 4k V2 backtest-plan methodology;
- Phase 4l V2 backtest execution Verdict C HARD REJECT (terminal
  for V2 first-spec);
- Phase 4m 18-requirement fresh-hypothesis validity gate;
- Phase 4n Candidate B avoidance pattern.

**Verification:**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No project lock changed.** **No retained verdict revised.**

**Recommended next operator choice:** **Option A primary — Phase 4p
G1 Strategy Spec Memo (docs-only).** Conditional secondary: remain
paused.

**Phase 4 canonical remains unauthorized.** **Phase 4p / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain
unauthorized.**

**Recommended state remains paused outside conditional Phase 4p.
No next phase authorized by Phase 4o.**

---

## Authority and boundary

Phase 4o operates strictly inside the post-Phase-4n-merge boundary:

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
  Phase 4m post-V2 strategy research consolidation memo +
  18-requirement fresh-hypothesis validity gate; Phase 4n fresh-
  hypothesis discovery memo (Candidate B selected as primary).
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md`
  unchanged.
- **Project-level locks preserved verbatim.** §1.7.3.
- **Phase 2f thresholds preserved verbatim.** §11.6 = 8 bps HIGH
  per side.
- **Retained-evidence verdicts preserved verbatim.** R3 / H0 / R1a /
  R1b-narrow / R2 / F1 / D1-A / V2.
- **Safety rules preserved verbatim.**
- **MCP and secrets rules preserved verbatim.**

Phase 4o adds *only* a docs-only hypothesis-spec memo, without
modifying any prior phase memo, any data, any code under
`src/prometheus/`, any rule, any threshold, any manifest, any verdict,
any lock, or any gate.

---

## Starting state

```text
branch:           phase-4o/regime-first-breakout-hypothesis-spec
parent commit:    3f71d5e1c7d7d47504ca8f92b19a11373c4cfd24 (post-Phase-4n-merge housekeeping)
working tree:     clean before memo authoring (transient .claude/scheduled_tasks.lock + gitignored data/research/ excluded)
main:             3f71d5e1c7d7d47504ca8f92b19a11373c4cfd24 (unchanged)

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
Phase 4n fresh-hypothesis discovery memo:                     merged (Candidate B selected as primary).

Repository quality gate:           fully clean.
research thread (5m):              operationally complete and closed (Phase 3t).
v002 datasets:                     locked; manifests untouched.
v001-of-5m datasets:               trade-price research-eligible; mark-price research_eligible:false.
Phase 4i datasets:                 30m + 4h klines × 2 research-eligible; metrics × 2 NOT research-eligible.
```

---

## Why this memo exists

Phase 4n recommended Phase 4o on Candidate B (Regime-first breakout
continuation) as the primary next-step option after evaluating four
Phase 4m candidate research spaces. The operator has explicitly
authorized Phase 4o.

Phase 4o's purpose is narrowly scoped: **define the conceptual
hypothesis (G1) for regime-first breakout continuation, plus the
binding design principles a future strategy spec must obey, without
specifying any final thresholds or running any tests.**

This is the **hypothesis-spec layer** of the project's strategy-
research lifecycle:

```text
discovery memo (Phase 4n)
  → hypothesis-spec memo (this Phase 4o)
    → strategy-spec memo (future Phase 4p)
      → data-requirements memo (future Phase 4q, if needed)
        → data acquisition (future Phase 4r, if needed)
          → backtest-plan memo (future Phase 4s)
            → backtest execution (future Phase 4t)
              → consolidation (future Phase 4u)
                → fresh-hypothesis discovery (future Phase 4v, if continued)
```

Phase 4o sits between discovery and strategy-spec. It does NOT
specify a strategy; it defines what a strategy spec must satisfy
and what design principles must be honored.

The discipline behind Phase 4o is the same anti-data-snooping
discipline applied at every prior research-direction selection
(Phase 3a F1 discovery; Phase 3f D1-A discovery; Phase 4f V2
discovery): the conceptual hypothesis must be committed *before*
any specific threshold, parameter, or data is touched, so that
when a future Phase 4p strategy-spec memo (if authorized) is
briefed, the hypothesis has already been pinned on theory.

Phase 4o's central operational concern is **avoiding Candidate B's
nearest forbidden rescue trap** identified by Phase 4n: "R1a /
R1b-narrow but with another bolt-on regime filter". Phase 4o's
binding **regime-first design principle** (§"Regime-first design
principle" below) is the structural bulwark against this trap.

---

## Relationship to Phase 4n

- **Phase 4n evaluated four Phase 4m candidate spaces** (A:
  Structural-R; B: Regime-first; C: Funding-context; D: Structural
  pullback) against the Phase 4m 18-requirement validity gate.
- **Phase 4n recommended Phase 4o on Candidate B as primary** with
  remain paused as conditional secondary.
- **Phase 4n did NOT authorize Phase 4o.**
- **The operator now authorizes Phase 4o.**
- **Phase 4o must remain docs-only.**
- **Phase 4o must not run a backtest, acquire data, or implement
  code.**

**Phase 4n verdict preservation (verbatim):**

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains CLOSED operationally.
- V2 remains HARD REJECT — structural CFP-1 critical.
- §11.6 HIGH cost remains 8 bps per side.
- §1.7.3 project-level locks remain unchanged.
- Phase 4j §11 and Phase 4k methodology remain unchanged.
- Phase 4m 18-requirement validity gate remains binding.

**No verdict is revised by Phase 4o. No project lock is changed by
Phase 4o.**

---

## Relationship to prior breakout research

G1 is a trend-continuation breakout candidate, sharing the *broad
family* with H0 / R3 / R1a / R1b-narrow / R2 / V2. Phase 4o records
how G1 differs from each:

| Prior strategy | What it is | How G1 differs |
|---|---|---|
| **H0 (V1 framework anchor)** | 15m signal, 1h bias, 8-bar setup, fixed bounds, staged exit. Canonical V1 reference. | G1 is regime-first; the strategy is INACTIVE outside the active regime. H0 is always-active inside its data range. |
| **R3 (V1 baseline-of-record)** | H0 with fixed-R take-profit + unconditional time-stop. Canonical exit family. | G1 inherits the spirit of fixed-R + time-stop only conditionally; inside-regime exit geometry is co-designed per regime, not fixed at H0's bounds. |
| **R1a (V1 + volatility-percentile setup predicate)** | Per-bar volatility filter on H0/R3. | G1 is NOT R1a with a "different volatility band". R1a evaluates per-bar; G1 evaluates a regime classifier at the strategy-active level, then evaluates per-bar entry only inside the active regime. |
| **R1b-narrow (V1 + bias-strength threshold)** | Per-bar bias-strength filter on H0/R3. | G1 is NOT R1b with a "stronger threshold". Same structural distinction as R1a. |
| **R2 (V1 + pullback-retest entry)** | Pullback-retest entry style on V1. | G1 is NOT R2; G1 retains breakout-bar-close entry conceptually. (R2 entry style is forbidden as rescue per Phase 4m.) |
| **V2 (Participation-Confirmed Trend Continuation)** | 30m signal + 4h bias + 8-feature AND chain (HTF bias, Donchian breakout, width compression, ATR band, range expansion, relative volume, volume z-score, UTC-hour percentile, taker imbalance, OI delta, funding band) + V1-inherited stop-distance filter. | G1's regime detection is at the **state-machine level**, not part of an 8-feature AND chain. G1's stop-distance bounds are co-designed from first principles per Phase 4m §"Stop / target / sizing lessons", not inherited from V1. G1 must NOT use V2's 8-feature AND chain, V2's Donchian setup, or V2's stop-distance bounds. |
| **F1 (mean-reversion-after-overextension)** | 8-bar cumulative displacement → contrarian SMA(8) target. | G1 is trend-continuation, not mean-reversion. G1 must NOT re-introduce F1's mechanism. |
| **D1-A (funding-aware contrarian)** | 90-day funding-Z-score → contrarian directional entry at funding-settlement. | G1 is trend-continuation; G1 may use funding as **context** in the regime classifier, NOT as directional trigger. |

**G1 inherits no specific threshold from V1 / R3 / R1a / R1b-narrow /
R2 / F1 / D1-A / V2.** The only inherited project-level constraints
are: §1.7.3 (BTCUSDT primary live; ETHUSDT research / comparison;
one position max; 0.25% risk; 2× leverage cap; mark-price stops);
§11.6 = 8 bps HIGH per side; Phase 3v §8 / Phase 3w §6 / §7 / §8
governance label schemes; Phase 3r §8 mark-price gap governance;
Phase 4j §11 metrics OI-subset partial-eligibility rule (only if
G1's regime classifier or entry uses metrics OI subset); Phase 4k
V2 backtest-plan methodology (only if G1 ever runs a backtest, and
only as a methodology pattern; specific Phase 4k variant counts /
windows are NOT inherited).

---

## Hypothesis name

**G1 — Regime-First Breakout Continuation.**

Per Phase 4n §6 / §"Final discovery recommendation", the operator
brief recommended the name `G1 — Regime-First Breakout Continuation`.
Phase 4o adopts this name verbatim.

The "G1" prefix denotes a **new strategy generation** distinct from
the V-family (V1 / V2). The "1" indicates it is the first regime-
first hypothesis; future regime-first variants (if any) would be
G2, G3, etc., subject to separate operator authorization.

**Forbidden alternative names** (per Phase 4n / Phase 4m
forbidden-rescue list):

- **V3:** forbidden — V3 implies direct succession of V2.
- **V2-prime:** forbidden — V2 rescue.
- **R3-prime:** forbidden — R3 rescue.
- **R1c:** forbidden — R1a / R1b extension.
- **R1a-extension:** forbidden — R1a rescue.
- **R1b-extension:** forbidden — R1b rescue.
- **Any name implying direct rescue of any retained-evidence
  strategy.**

**G1 is the canonical name for this hypothesis.**

---

## Core hypothesis

**G1 — Regime-First Breakout Continuation:**

> Breakout continuation may be viable on BTCUSDT perpetual futures
> only when the market is already in a predeclared favorable
> regime, where the regime is determined by a top-level state
> machine that operates exclusively on prior-completed data.
> Outside the active regime, the strategy is completely inactive
> and produces no candidate signals; inside the active regime,
> entry / stop / target / sizing are co-designed from first
> principles for that regime's volatility / trend / cost profile.

**Plain-language elaboration:**

- **Most of the time, the strategy does nothing.** This is
  intentional. A regime-first design accepts that there are extended
  periods where no trade should be considered.
- **The regime classifier is the gatekeeper.** The classifier
  consumes prior-completed market state (HTF trend, volatility
  regime, funding context, etc.) and outputs a regime state
  (`regime_inactive`, `regime_candidate`, `regime_active`,
  `regime_cooldown`). Only `regime_active` enables strategy
  activity.
- **Inside the active regime, breakout-continuation logic is
  evaluated** at the per-bar level, but the geometry of that logic
  (setup window, stop, target, sizing, time-stop) is calibrated to
  the active-regime's structural properties — not inherited from
  V1 / V2.
- **Outside the active regime, no entry signal is even computed.**
  This contrasts with R1a / R1b-narrow (which compute the breakout
  signal then filter on a per-bar regime predicate) and with V2
  (which computes the breakout signal as one of 8 AND'd gates).
- **The hypothesis is testable.** It either holds (regime-active
  breakouts have materially better risk-adjusted outcomes than
  regime-inactive breakouts AND than always-active baselines) or it
  fails (the regime classifier doesn't sort outcomes meaningfully).
- **It is conceptually distinct from prior strategies** (per
  §"Relationship to prior breakout research" above).

**The hypothesis is NOT:**

- "V2 with a regime filter."
- "R1a / R1b plus another regime feature."
- "F1 / D1-A / R2 with a different gate."
- "5m diagnostic findings converted to rules."

---

## Why this is not a rescue

Phase 4n identified the nearest forbidden-rescue trap for Candidate
B: "R1a / R1b-narrow but with another bolt-on regime filter". Phase
4o's design must demonstrate G1 is structurally distinct from this
trap. The structural distinction is the **regime-first design
principle** (§"Regime-first design principle" below):

- **R1a / R1b-narrow:** signal first, then per-bar filter.
  Strategy is always active; per-bar filter rejects some bars.
- **G1:** regime first, then signal. Strategy is conditionally
  active; outside the active regime, no signal is computed at all.

This is a **categorical** distinction, not a degree distinction. R1a
/ R1b-narrow per-bar filters cannot be reorganized into G1's regime
state machine without redesigning the strategy from scratch — which
is precisely Phase 4o's design discipline.

**Additional structural distinctions:**

- **No reuse of V1 / V2 setup geometry.** G1's inside-regime
  breakout setup is co-designed for the active regime per Phase 4m
  §"Stop / target / sizing lessons"; V1's 8-bar setup and V2's
  20/40-bar Donchian setup are NOT inherited as defaults.
- **No reuse of V1's stop-distance filter bounds.** Phase 4l's
  forensic finding (V2 0-trade outcome) MUST NOT inform G1's stop
  bounds. G1's stop bounds (if a filter is used) must be derived
  from the active-regime's volatility distribution, not from
  V1 / V2 numbers.
- **No reuse of V2's 8-feature AND chain.** G1's inside-regime
  entry conditions are designed independently.
- **No conversion of 5m Q1–Q7 informative findings to rules.**
  Phase 3o §6 forbidden question forms preserved.
- **No reuse of D1-A's funding-Z-score directional rule.** G1 may
  use funding as a regime-context dimension (e.g., "regime is
  inactive when funding is in pathological extremes") but NOT as
  a directional trigger.
- **No reuse of R2's pullback-retest entry style.** G1 retains
  breakout-bar-close entry conceptually.

**Phase 4o records these structural distinctions as binding for
Phase 4p:** any future Phase 4p strategy-spec memo for G1 must
demonstrate that each of the above structural distinctions is
preserved.

---

## Regime-first design principle

**Binding principle (Phase 4o §1):**

1. **First decide whether the market is in a favorable regime.**
   The regime classifier consumes prior-completed data and outputs
   a regime state.
2. **Only inside the active regime can a breakout setup be
   considered.** The breakout-evaluation function is invoked only
   when the regime state machine is in `regime_active`.
3. **Outside the active regime, the strategy is inactive and
   produces no candidate signals.** The breakout-evaluation function
   is not invoked.
4. **Regime classifier must be computed from prior-completed data
   only.** No mid-bar use; no future bars; no future-event lookups.
5. **Regime classifier must not depend on whether a breakout signal
   is present.** The classifier is orthogonal to the entry trigger.
   Concretely: if the classifier output is `regime_active`, then
   `regime_active` was computed without examining whether a
   breakout signal exists at this bar.
6. **Regime classifier must not be tuned to rescue prior failures.**
   The classifier MUST NOT be derived from observing V1 / V2 / R1a /
   R1b / R2 / F1 / D1-A failure patterns.

This principle is the structural bulwark against the Candidate B
rescue trap ("R1a / R1b-narrow but with another bolt-on regime
filter"). Any classifier that violates principles 1-6 is, by
construction, a per-bar bolt-on filter and not a regime-first
state machine.

**Future Phase 4p strategy-spec memo MUST demonstrate** that its
proposed classifier satisfies all six principles.

---

## Regime state machine

Phase 4o defines the regime state machine at the **conceptual
level**: states, purposes, allowed signal behaviors, transition
concepts, forbidden behaviors. Phase 4o does NOT define final
transition thresholds. Those are Phase 4p's responsibility.

### State 1: `regime_inactive`

- **Purpose:** the market is NOT in a favorable regime for breakout
  continuation. The strategy is completely dormant.
- **Allowed signal behavior:**
  - **No** entry signals are computed.
  - **No** breakout evaluation function is invoked.
  - **No** orders are placed.
  - **No** position is opened.
  - **Reading prior bars for regime classification IS allowed**
    (the classifier itself runs continuously to detect regime
    transitions).
- **Transition concept:**
  - `regime_inactive` → `regime_candidate` when the regime
    classifier observes a sustained shift toward favorable
    conditions over a predeclared lookback window.
  - The transition does NOT depend on whether an entry signal is
    present.
- **What future Phase 4p must specify:**
  - the exact classifier inputs;
  - the exact transition criterion (e.g., "trend slope ≥ X over
    Y bars AND volatility percentile in [P_lo, P_hi] over Z bars");
  - the exact lookback windows.
- **Forbidden behavior:**
  - any entry signal computation in this state;
  - any reference to mid-bar / future data;
  - any classifier that depends on whether a breakout is in
    progress.

### State 2: `regime_candidate`

- **Purpose:** the regime classifier has observed early evidence of
  a regime shift toward favorable, but the shift has not yet been
  confirmed.
- **Allowed signal behavior:**
  - **No** entry signals are computed.
  - **No** orders are placed.
  - **The classifier continues to evaluate** whether the candidate
    regime is becoming a confirmed active regime or reverting to
    inactive.
- **Transition concept:**
  - `regime_candidate` → `regime_active` when classifier confirms
    sustained favorable regime over a predeclared confirmation
    window.
  - `regime_candidate` → `regime_inactive` when classifier observes
    a reversion within a predeclared timeout window.
- **What future Phase 4p must specify:**
  - the exact confirmation criterion;
  - the exact reversion criterion;
  - the timeout window.
- **Forbidden behavior:** same as `regime_inactive`. No entry
  signals.

### State 3: `regime_active`

- **Purpose:** the market is confirmed in a favorable regime.
  Strategy is active.
- **Allowed signal behavior:**
  - Entry signals **may be** computed at completed-bar boundaries.
  - Inside-regime breakout setup is evaluated per Phase 4o
    §"Inside-regime breakout concept".
  - Orders may be placed if entry signals + risk gates pass.
  - Position may be opened (one position max per §1.7.3).
- **Transition concept:**
  - `regime_active` → `regime_suspended` when classifier detects
    regime degradation.
  - `regime_active` → `regime_cooldown` after a normal exit (per
    Phase 4p design choice).
- **What future Phase 4p must specify:**
  - the exact regime degradation criterion;
  - whether `regime_active` exits to `regime_cooldown` after each
    trade or persists across multiple trades.
- **Forbidden behavior:**
  - entry signals computed using future-bar data;
  - entry signals where the classifier and the entry trigger share
    a feature (per §"Regime classifier design constraints" below);
  - entry under wrong governance label (`mixed_or_unknown` fails
    closed per Phase 3v §8.4).

### State 4: `regime_cooldown` / `regime_suspended`

- **Purpose:** post-trade or post-degradation pause to avoid
  immediate re-entry or to wait for regime confirmation reset.
- **Allowed signal behavior:**
  - **No** new entries.
  - **Existing position management continues** if a position is
    open (stop / take-profit / time-stop honored).
- **Transition concept:**
  - `regime_cooldown` / `regime_suspended` → `regime_inactive` if
    classifier observes regime reversion.
  - `regime_cooldown` → `regime_active` after a predeclared cooldown
    bar count if classifier remains favorable.
- **What future Phase 4p must specify:**
  - the cooldown bar count;
  - the suspended-state recovery criterion.
- **Forbidden behavior:**
  - new entries during cooldown;
  - skipping the cooldown to take an immediate same-direction
    re-entry.

### State machine summary

```text
                    ┌──────────────────┐
                    │ regime_inactive  │ ← initial state
                    └────┬─────────────┘
                         │  (classifier observes early shift)
                         ▼
                    ┌──────────────────┐
                    │ regime_candidate │
                    └────┬─────────────┘
                         │  (confirmation OR reversion)
                ┌────────┼──────────────┐
                ▼                       ▼
           ┌───────────────┐     (back to)
           │ regime_active │     regime_inactive
           └────┬──────────┘
                │ (degradation OR exit)
                ▼
           ┌───────────────────────────┐
           │ regime_cooldown /         │
           │ regime_suspended          │
           └────┬──────────────────────┘
                │ (reset)
                ▼
           regime_inactive (or regime_active after cooldown)
```

### Transition discipline

- **All transitions use prior-completed bars only.** No lookahead.
- **All transition criteria must be predeclared** in any future
  Phase 4p brief.
- **The state machine is deterministic** given the classifier
  inputs.
- **The state machine has bounded memory.** Recent classifier
  history (within predeclared windows) determines current state;
  no unbounded path-dependence.

---

## Regime classifier design constraints

Phase 4o defines binding rules for the regime classifier. Phase 4o
does NOT specify the final classifier formula. Phase 4p (if
authorized) must propose a specific classifier that satisfies these
rules.

### Allowed classifier dimensions

The classifier MAY consume one or more of the following dimensions
(Phase 4p chooses the specific subset):

1. **HTF trend direction / slope** computed from completed 4h or 1h
   bars. Examples: EMA(N) / EMA(M) discrete comparison; closed-bar
   slope across the prior K completed bars; HTF bias state per
   Phase 3w §7.3 `discrete_comparison`.
2. **Volatility expansion / compression regime** computed from ATR
   percentile or realized-volatility percentile over a trailing
   window of completed bars. Examples: ATR(N) percentile in a
   defined band; realized volatility regime classification.
3. **Trend persistence / directional efficiency** over the higher
   timeframe. Examples: efficiency ratio; cumulative absolute return
   vs. net return ratio; sustained slope-sign across multiple
   completed bars.
4. **Funding context (risk-context dimension only, NOT directional
   trigger).** Examples: funding-rate percentile band over a
   predeclared lookback; funding-rate not-pathological flag. **This
   must NOT be the funding-Z-score directional rule from D1-A**
   (rescue forbidden).
5. **Optional OI context (only if Phase 4j §11 OI-subset governance
   is preserved).** Examples: OI delta direction over a defined
   window using the Phase 4j §11 OI-subset only. **The four optional
   metrics ratio columns remain forbidden.** If OI is used, the
   classifier MUST honor Phase 4j §11 per-bar exclusion exactly.

### Forbidden classifier inputs

The classifier MUST NOT use:

- **5m Q1–Q7 diagnostic findings as regime indicators.** Phase 3o
  §6 forbidden question forms preserved.
- **V2 Phase 4l observed stop-distance failure numbers** (3-5 × ATR
  empirical distribution). Bailey et al. 2014 / Phase 4m
  forbidden-rescue.
- **Any result from future backtests.** Predeclaration discipline.
- **Future bars.** Lookahead forbidden.
- **Optional metrics ratio columns** (`count/sum_toptrader_long_short_ratio`,
  `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`).
  Phase 4j §11.3 forbidden.
- **Mark-price 30m / 4h.** Deferred per Phase 4h §20; not
  authorized.
- **`aggTrades`.** Deferred per Phase 4h §7.E; not authorized.
- **Spot data, cross-venue data.** Forbidden by §1.7.3.
- **Private / authenticated / WebSocket / user-stream data.**
  Forbidden by safety rules.
- **Discretionary / manual regime labels.** The classifier must be
  algorithmic and deterministic given its inputs.

### Binding classifier rules

In addition to the regime-first design principle (§"Regime-first
design principle"), the classifier MUST satisfy:

- **Deterministic given inputs.** Same inputs → same regime state.
- **Stateful but bounded.** May depend on recent classifier history
  within predeclared windows; no unbounded path-dependence.
- **Predeclared.** Phase 4p strategy-spec memo MUST predeclare the
  classifier formula before any data is touched.
- **Stable across train / validation / OOS windows.** Phase 4p must
  predeclare a stability check; classifier instability across
  windows is a CFP-9-analogous catastrophic-floor predicate.
- **Distinguishable.** The classifier must produce all four states
  (`regime_inactive`, `regime_candidate`, `regime_active`,
  `regime_cooldown` / `regime_suspended`) at non-trivial fractions
  on the historical record. A classifier where one state dominates
  > 95% of the time is unreliable.

---

## Candidate regime dimensions

Phase 4o evaluates each allowed classifier dimension qualitatively.
Phase 4o does NOT select final thresholds.

### Trend regime

- **Why it may matter:** breakout-continuation strategies
  conceptually require a trending market. In a non-trending market,
  breakouts are usually false signals.
- **Data required:** completed 1h or 4h klines (open, close);
  rolling EMA / slope computation.
- **Rescue risk:** moderate. The trap is "use V1's EMA(50)/(200) on
  1h" or "use V2's 4h EMA(20)/(50)" as a default. G1 must NOT
  inherit a specific EMA pair from V1 / V2.
- **Allowed in G1 first spec:** YES (subject to Phase 4p choosing
  EMA pair / slope criterion from first principles, not by
  inheritance).
- **What future Phase 4p must decide:**
  - timeframe (1h or 4h);
  - exact EMA pair (or alternative slope formulation);
  - threshold for "trend is up" / "trend is down" / "trend is
    neutral";
  - whether trend regime is binary (active / inactive) or
    multi-state (e.g., strong-up, weak-up, neutral, weak-down,
    strong-down).

### Volatility regime

- **Why it may matter:** breakout efficacy depends on volatility
  state. In compressed-volatility regimes, the next expansion may
  be the breakout. In expanded-volatility regimes, breakouts have
  different cost-survival profiles.
- **Data required:** completed 30m / 1h / 4h klines for ATR or
  realized-volatility computation; trailing percentile windows.
- **Rescue risk:** moderate. Trap: "use V2's ATR percentile band
  [25, 75]" as a default. G1 must NOT inherit V2's bounds.
- **Allowed in G1 first spec:** YES (Phase 4p chooses bounds from
  first principles).
- **What future Phase 4p must decide:**
  - timeframe;
  - ATR period or realized-volatility window;
  - trailing-percentile lookback;
  - threshold band(s) for favorable vs. unfavorable volatility.

### Liquidity / volume regime

- **Why it may matter:** breakouts in low-liquidity regimes have
  systematically worse cost-survival (R2's failure pattern at HIGH
  cost). A liquidity regime classifier could exclude such windows
  entirely.
- **Data required:** completed kline volume; possibly UTC-hour
  buckets (per Hattori 2024 / Eross et al. 2019 intraday
  periodicities).
- **Rescue risk:** moderate-to-high. Trap: "use V2's UTC-hour
  percentile gate" or "use R2's empirical low-liquidity window
  observation". G1 must NOT inherit V2's session-bucket or R2's
  observed cost-fragility.
- **Allowed in G1 first spec:** YES with caution. Phase 4p must
  define liquidity regime from first principles.
- **What future Phase 4p must decide:**
  - whether to use liquidity regime;
  - if yes, the volume / spread / participation feature(s);
  - the threshold criterion.

### Funding context regime

- **Why it may matter:** funding extremes correlate with eventual
  reversion (D1-A demonstrated funding contains information at
  M1-PASS level). For G1, funding can be used as a regime-context
  dimension: avoid trading when funding is pathological.
- **Data required:** v002 funding manifests.
- **Rescue risk:** moderate. Trap: "use D1-A's |Z_F| ≥ 2.0 as
  context boundary" or "use V2's funding percentile bands [20, 80]
  / [30, 70]". G1 must NOT inherit D1-A's directional Z-score rule
  or V2's specific bands.
- **Allowed in G1 first spec:** YES (Phase 4p chooses bounds from
  first principles).
- **What future Phase 4p must decide:**
  - whether to use funding context;
  - if yes, the funding-rate window (per-event vs. trailing
    percentile);
  - the pathological-extreme criterion (and confirm it is NOT
    D1-A's |Z_F| rule).

### Composite regime

- **Why it may matter:** any single dimension may produce an
  unreliable regime classifier; a composite (e.g., "trend AND
  volatility AND funding context") could be more robust.
- **Data required:** combination of the above.
- **Rescue risk:** moderate-to-high. Composite classifiers can
  become "V2 with regime semantics relabeled". Phase 4p must
  demonstrate the composite is a regime classifier (top-level state
  machine) and not an 8-feature AND chain.
- **Allowed in G1 first spec:** YES with caution. Phase 4p must
  rigorously distinguish composite regime from V2's AND chain.
- **What future Phase 4p must decide:**
  - which dimensions to combine;
  - how to combine them (AND, OR, weighted, hierarchical);
  - whether the composite produces a regime state machine or a
    per-bar gate (only the former is allowed).

**Phase 4o does NOT select** any specific dimension(s) for G1.
Phase 4p (if authorized) must predeclare its classifier dimensions
before any data is touched.

---

## Strategy-active versus strategy-inactive behavior

### When `regime_active`:

- Entry signals MAY be computed at completed-bar boundaries (the
  signal timeframe is Phase 4p's choice).
- Inside-regime breakout setup is evaluated per the rules in
  §"Inside-regime breakout concept".
- If a setup passes all entry conditions AND no position is open
  AND cooldown has elapsed, a market entry order is placed at the
  next completed bar's open.
- Position is managed per Phase 4p's exit model (stop / take-profit
  / time-stop precedence).
- Risk gates apply: 0.25% risk per trade; 2× leverage cap; one
  position max; mark-price stops in any future runtime per Phase
  3v §8.

### When NOT `regime_active`:

- **No** entry signals are computed.
- **No** breakout evaluation function is invoked.
- **No** orders are placed.
- **No** new position is opened.
- If a position is open from the prior `regime_active` window,
  position management continues per the existing exit rules until
  exit.
- The regime classifier continues running.

### Position-and-regime interaction (Phase 4p decision)

There are two acceptable ways to handle position-vs-regime:

- **Option A:** position lifecycle independent of regime. If
  regime transitions from `regime_active` to `regime_inactive` /
  `regime_suspended` during an open position, the position
  continues until its exit rules trigger (stop / take-profit /
  time-stop). The regime change does NOT force an exit.
- **Option B:** position closes when regime transitions away from
  `regime_active`. Regime degradation acts as a soft exit signal.

**Phase 4o does NOT decide between A and B.** Phase 4p must
predeclare which option applies. **Note:** Option B introduces a
regime-driven exit; this can interact non-trivially with the
target / time-stop logic and must be co-designed accordingly.

---

## Inside-regime breakout concept

Phase 4o defines what "breakout continuation" means at the
**conceptual level** for G1. Phase 4o does NOT define concrete
entry rules.

### Conceptual definition

A G1 inside-regime breakout setup is a price-structure event,
evaluated at completed-bar boundaries inside `regime_active`, that
indicates a likely continuation of the regime's trend direction.

### Binding constraints (Phase 4o §1)

- **Setup window N is a Phase 4p decision.** Phase 4p must select
  N from first principles for the active regime — not as N=8
  (V1 default), not as N=20 / 40 (V2 default).
- **Structural stop is a Phase 4p decision.** The structural stop
  must represent invalidation of the breakout-in-progress hypothesis
  inside the active regime. Phase 4p must derive the stop from the
  active regime's volatility distribution, not from V1 / V2
  numbers.
- **Target logic is a Phase 4p decision.** Fixed-R take-profit is
  one option (R3 baseline); other options are admissible if
  justified. Phase 4p must demonstrate target-distance × win-rate
  math is plausible for the active regime.
- **Time-stop is a Phase 4p decision.** Time-stop must match
  expected regime persistence: too short discards trades that need
  more time; too long ties up capital in stalled trades.
- **Position sizing is locked.** 0.25% risk per trade, 2× leverage
  cap, one position max (§1.7.3 preserved). Phase 4p inherits these
  verbatim.
- **Stop-trigger domain is locked per Phase 3v §8.** Research /
  backtest = `trade_price_backtest`; future runtime / paper / live
  = `mark_price_runtime`; future live-readiness validation =
  `mark_price_backtest_candidate`; `mixed_or_unknown` invalid /
  fail-closed.

### Forbidden inside-regime entry features

Phase 4p MUST NOT use:

- **V1's 8-bar setup window as the default N.** Phase 4p must
  justify N from first principles.
- **V2's 20/40-bar Donchian setup as the default N.** Same.
- **V1's 0.60–1.80 × ATR(20) stop-distance filter as default
  bounds.** Phase 4p must derive bounds from the active regime's
  volatility distribution.
- **V2's 8-feature AND chain.**
- **R2's pullback-retest entry style.**
- **F1's mean-reversion logic.**
- **D1-A's funding-Z-score directional rule.**

### Conceptual entry condition (Phase 4o sketch only)

Inside `regime_active`, a G1 long entry **conceptually** requires
all of:

1. **Regime is `regime_active`** (state machine, not per-bar gate).
2. **No active cooldown** (per Phase 4p cooldown design).
3. **No active position** on the symbol.
4. **A completed-bar breakout structure** — the specific structure
   is Phase 4p's choice (could be Donchian-style, channel-break,
   range-break, or another well-defined structural breakout).
5. **The breakout direction is consistent with the active
   regime's trend direction** (long breakouts only in upward-
   trending regime; short breakouts only in downward-trending
   regime).
6. **Inside-regime stop / target / sizing math is plausible** for
   the proposed entry — i.e., stop distance is within an
   active-regime-derived band; target is reachable given regime
   volatility; position size respects 0.25% risk + 2× leverage
   cap.
7. **No governance-label failure** (Phase 3v §8 / Phase 3w §6 / §7 /
   §8 schemes; `mixed_or_unknown` invalid).

**Phase 4p must specify each of (1)-(7) precisely.** Phase 4o
provides the conceptual placeholder only.

A G1 short entry is the strict mirror image with downward-trending
regime and downward breakout structure.

---

## Entry / stop / target / sizing co-design principles

Phase 4m §"Stop / target / sizing lessons" identified five
interdependent elements that must be co-designed:

1. **Setup window N** determines structural stop distance.
2. **Structural stop distance** determines (with N_R) target
   absolute movement.
3. **Target absolute movement** determines achievable trade rate.
4. **Trade rate** × N years of data determines sample size.
5. **Sample size** determines CFP-1 / DSR / PBO statistical power.

Phase 4o adopts these as binding for G1.

### Position sizing (locked)

- **0.25% risk per trade** (§1.7.3 locked).
- **2× effective leverage cap** (§1.7.3 locked).
- **One position max** (§1.7.3 locked).
- **R = |entry_price − initial_stop|** (R3 / V2 convention).
- **Position size = floor((equity × 0.0025) / stop_distance)**,
  subject to leverage and notional caps.

### Stop-distance bounds (Phase 4p decision; G1 first principles)

- **Stop must represent structural invalidation inside the active
  regime.** Phase 4p derives the structural stop construction from
  the active regime's market structure (e.g., recent regime-active-
  window low for long; regime-active-window high for short).
- **Stop-distance bounds, if any, must be justified from the active
  regime's volatility distribution.** NOT inherited from V1's
  0.60–1.80 × ATR.
- **Wider stops are not automatically invalid** if position sizing
  controls risk. But wider stops require realistic target / time-
  stop logic.
- **Too-tight stops can be invalid** if they sit inside intra-
  regime noise. Phase 4p must demonstrate the chosen stop is
  outside expected noise.
- **Stop-distance filter, if used as a trade-quality gate, must
  reject trades whose stop distance falls outside the active
  regime's expected band.** The band is Phase 4p's design choice.

### Target distance in R (Phase 4p decision)

- **Fixed-R take-profit** is one valid option (R3 baseline-of-
  record uses N_R = 2).
- **Other target structures** (regime-target, structure-based
  target, multi-target) are admissible if justified by Phase 4p.
- **Target-distance × win-rate math must be plausible** for the
  active regime. At HIGH-slip = 8 bps per side (§11.6 preserved),
  breakeven win rate ≈ 35% at fixed 2R + 16 bps round-trip.

### Time-stop horizon (Phase 4p decision)

- **Time-stop must match expected regime persistence.** Phase 4p
  estimates regime persistence from the regime classifier's
  empirical state-duration distribution.
- **Unconditional time-stop** is the canonical R3 / V1 / V2 form.
- **Regime-driven exit** is Option B in §"Strategy-active versus
  strategy-inactive behavior". If chosen, time-stop interacts with
  regime-degradation exit and must be co-designed.

### Cost-budget in R units

- **Per-trade cost in R = round_trip_bps × entry_price / R / 10000.**
- **Cost-budget must be evaluated in R units** at LOW / MEDIUM /
  HIGH cost cells.
- **§11.6 HIGH = 8 bps per side preserved verbatim.**
- **Phase 4p must demonstrate cost-budget is plausible** at brief
  time, before any backtest.

---

## Cost-sensitivity argument

### §11.6 HIGH cost preserved

- **§11.6 HIGH = 8 bps slippage per side, plus 4 bps taker fee per
  side = 24 bps round-trip total at HIGH.**
- **No relaxation.** No maker rebate. No live-fee assumptions.
  No paper / live implication.
- **Phase 3l external execution-cost evidence review** confirmed
  §11.6 is "B — current cost model conservative but defensible".
  Phase 4o preserves §11.6 verbatim.

### Expected cost logic for G1

G1 has a structural cost-sensitivity advantage from its regime-first
design:

- **Outside `regime_active`, the strategy doesn't trade.** Zero
  trades = zero cost burden in those windows.
- **Inside `regime_active`, trade frequency is bounded by the
  regime's prevalence and signal density.** If the favorable
  regime occupies (e.g.) 30% of the historical window, the strategy
  is active for 30% of the time and accumulates costs accordingly.
- **The regime classifier itself can be cost-sensitivity-aware.**
  A favorable regime can be defined to exclude pathological
  liquidity / volatility windows where cost-fragility is empirically
  highest.

This contrasts favorably with always-active strategies (V1 / V2)
that accumulate costs continuously.

### Sample-size constraint

Lower trade count is acceptable **only if** sample size remains
adequate for:

- Phase 4k methodology DSR / PBO / CSCV (T ≥ 30 train-window trades
  per variant for DSR computation);
- mechanism-check stat-significance (M2 / M3 bootstrap-by-trade
  with B = 10 000 needs ≥ ~30 trades per cell for stable 95% CI);
- catastrophic-floor predicate evaluation.

If G1's regime-active fraction × signal density × N years yields
< 30 OOS trades on BTCUSDT, **CFP-1 critical fires** (analogous
to V2's failure mode under different mechanism).

### Cost must survive HIGH-cell

Phase 4p must demonstrate at brief time that:

- per-trade R cost at HIGH-cell is bounded;
- expected per-trade R after HIGH-cost is plausibly positive;
- regime gating systematically excludes HIGH-cost-fragile trades;
- §11.6 HIGH cost-survival is a binding pass / fail gate.

---

## Data-readiness assessment

### Likely data sources

| Data | Source | Status |
|---|---|---|
| BTCUSDT 15m trade-price klines | v002 | research-eligible; locked |
| BTCUSDT 1h derived | v002 | research-eligible; locked |
| BTCUSDT 30m trade-price klines | Phase 4i v001 | research-eligible |
| BTCUSDT 4h trade-price klines | Phase 4i v001 | research-eligible |
| ETHUSDT 15m trade-price klines | v002 | research-eligible; locked |
| ETHUSDT 1h derived | v002 | research-eligible; locked |
| ETHUSDT 30m trade-price klines | Phase 4i v001 | research-eligible |
| ETHUSDT 4h trade-price klines | Phase 4i v001 | research-eligible |
| BTCUSDT funding history | v002 | reused; (research_eligible flag per v002 lock) |
| ETHUSDT funding history | v002 | reused |
| BTCUSDT metrics OI subset | Phase 4i metrics | metrics manifest globally `research_eligible: false`; OI-subset feature-eligible per Phase 4j §11 binding rule |
| ETHUSDT metrics OI subset | Phase 4i metrics | same |
| Mark-price 30m / 4h | NOT acquired | not authorized; deferred per Phase 4h §20 |
| `aggTrades` | NOT acquired | not authorized; deferred per Phase 4h §7.E |
| Spot data | NOT acquired | forbidden by §1.7.3 |
| Cross-venue data | NOT acquired | forbidden by §1.7.3 |
| Authenticated REST / private endpoints / user stream / WebSocket | NOT used | forbidden by safety rules |

### Assessment

- **For most plausible regime classifier designs**, existing data
  appears sufficient:
  - Trend regime: v002 1h / Phase 4i 4h klines.
  - Volatility regime: v002 15m / 1h or Phase 4i 30m / 4h klines.
  - Funding context: v002 funding manifests.
  - OI context (optional): Phase 4j §11 OI-subset under per-bar
    exclusion.
- **For inside-regime breakout entry**, existing data appears
  sufficient:
  - Signal timeframe options 15m, 30m, or 1h — all available.
  - HTF bias options 1h, 4h — all available.
- **Mark-price 30m / 4h**, `aggTrades`, spot, cross-venue, optional
  metrics ratio columns — all NOT used by G1's first-principles
  scope.

### Need for future data-requirements memo

**Phase 4o assesses that an immediate future Phase 4q
data-requirements memo is NOT strictly required** before Phase 4p
strategy-spec memo, **provided** Phase 4p's regime classifier and
entry design stay within existing data:

- v002 trade-price klines (15m, 1h derived, 4h via Phase 4i v001);
- v002 funding manifests;
- Phase 4i 30m + 4h klines;
- Phase 4i metrics OI-subset under Phase 4j §11.

**If Phase 4p's design requires data outside the above set**, a
separate Phase 4q data-requirements memo (analogous to Phase 4h)
becomes required before any further data-related decision. Possible
triggers for needing Phase 4q:

- Phase 4p chooses mark-price 30m / 4h: requires Phase 4q +
  acquisition.
- Phase 4p chooses tick-level slippage modeling: requires `aggTrades`
  acquisition + Phase 4q.
- Phase 4p chooses 1m kline data: requires acquisition + Phase 4q.

**Phase 4o does NOT authorize data acquisition.** Phase 4p must
reuse existing data, OR a separate Phase 4q must be authorized
before any acquisition.

### Phase 4j §11 metrics OI-subset rule (binding if metrics used)

If Phase 4p's regime classifier uses metrics OI-subset (e.g., as
funding-context dimension or as standalone OI-context dimension),
then Phase 4j §11 binding rule applies:

- Metrics manifests remain globally `research_eligible: false`.
- OI subset only: `create_time`, `symbol`, `sum_open_interest`,
  `sum_open_interest_value`.
- Optional ratio columns categorically forbidden.
- Per-bar exclusion algorithm matches Phase 4j §16 verbatim.
- No forward-fill, interpolation, imputation, synthetic data, or
  silent omission.
- Future backtest must report exclusion counts and main-cell vs.
  exclude-entire-affected-days sensitivity comparison.

---

## Mechanism-check framework

Phase 4o defines the conceptual mechanism-check framework for G1.
Phase 4o does NOT set numeric thresholds; those are Phase 4p's
responsibility.

### M1 — Regime-validity negative test

**Claim:** Inside `regime_active`, breakout continuation should show
better follow-through than outside `regime_active` (i.e., than
breakout signals computed in the inactive regime would have shown
if the strategy had not been gated).

**Test design:**

- Compute hypothetical breakout signals at completed-bar boundaries
  in BOTH `regime_active` AND `regime_inactive` periods (the latter
  is a "would-have-been" trade population, NOT actually traded).
- Compare:
  - active-regime trade population's MFE distribution and
    expectancy;
  - inactive-regime "would-have-been" trade population's MFE
    distribution and expectancy.
- **Pass criterion:** active-regime population's expectancy >
  inactive-regime population's expectancy by a Phase 4p-predeclared
  threshold (placeholder: ≥ +0.10R), with bootstrap-by-trade 95%
  CI lower bound > 0.
- **Fail criterion:** if active-regime population is NOT
  meaningfully better than inactive-regime population, the regime
  hypothesis fails.

**Phase 4o does NOT predeclare M1 thresholds.** Placeholders are
illustrative. Phase 4p must commit specific thresholds.

### M2 — Regime-gating value-add over always-active baseline

**Claim:** Regime-first strategy should outperform an always-active
breakout baseline, ESPECIALLY at HIGH-cost cell.

**Test design:**

- Compute always-active baseline (the same inside-regime entry
  rules but applied at every completed bar, ignoring regime state).
- Compare:
  - G1 (regime-gated) expectancy at HIGH-cost cell;
  - always-active baseline expectancy at HIGH-cost cell.
- **Pass criterion:** G1 expectancy at HIGH-cost > baseline
  expectancy at HIGH-cost by a Phase 4p-predeclared threshold
  (placeholder: ≥ +0.05R), with bootstrap-CI lower bound > 0.
- **Fail criterion:** if regime-gating doesn't help at HIGH-cost,
  the regime hypothesis fails.

### M3 — Inside-regime co-design validity

**Claim:** Inside-regime entry / stop / target / sizing co-design
produces adequate trade count AND OOS expectancy WITHOUT
catastrophic-floor trigger.

**Test design:**

- Verify trade count ≥ Phase 4p-predeclared minimum (placeholder:
  ≥ 30 OOS trades per variant).
- Verify expectancy is positive at MEDIUM cost cell on BTCUSDT OOS.
- Verify CFP-1 / CFP-2 / CFP-3 not triggered.
- **Pass criterion:** all three above.
- **Fail criterion:** any one of the three.

### M4 — Cross-symbol robustness

**Claim:** BTCUSDT primary; ETHUSDT comparison only; ETHUSDT cannot
rescue BTCUSDT failure.

**Test design:**

- M1 / M2 / M3 evaluated on BTCUSDT (primary).
- M1 / M2 / M3 evaluated on ETHUSDT (comparison only).
- **Pass criterion:** BTCUSDT passes M1 / M2 / M3 AND ETHUSDT shows
  directional support (M1 ≥ 50% MFE on ETH; M2 / M3 differential
  not negative on ETH).
- **Fail criterion:** BTCUSDT fails any of M1 / M2 / M3, regardless
  of ETHUSDT.

### Mechanism-check independence

M1 / M2 / M3 / M4 are evaluated independently of overall expectancy.
A variant that has positive expectancy but fails any of M1 / M2 /
M3 / M4 is STILL a partial rejection.

**Phase 4o does NOT predeclare M1 / M2 / M3 / M4 numeric thresholds.**
Phase 4p must do so.

---

## Negative-test framework

The negative-test component of M1 is critical for regime-first.

### Why negative test matters

- **Regime classifier can be illusory.** A classifier might appear
  to identify favorable regimes simply by data-snooping the historical
  record (Bailey et al. 2014). Without a negative test, this is
  undetectable.
- **Inactive regime must be measurably less favorable.** If the
  inactive regime performs equally well or better than the active
  regime, the regime hypothesis is wrong; the classifier's
  "favorable" label is meaningless.

### Required negative-test components for any future Phase 4p backtest

1. **Active vs. inactive comparison.** As described in M1.
2. **Always-active baseline comparison.** As described in M2.
3. **Random-regime baseline comparison (optional but recommended).**
   Replace the regime classifier with a random binary state
   generator with the same active-regime fraction. If G1 doesn't
   outperform random-regime baseline, the classifier carries no
   information.

### Failure modes

- **Inactive regime equally favorable:** regime hypothesis fails.
- **Sample size collapse from regime gating:** if the active regime
  yields too few trades for DSR / PBO / CSCV, CFP-1 fires.
- **Train-only success:** if the regime classifier works on train
  but fails on validation / OOS, classifier is not stable; CFP-5 /
  CFP-9-analogous fires.

---

## Pass / fail gate framework

Phase 4o defines conceptual pass / fail gates. Phase 4p must define
numerical thresholds.

### Gates a future G1 backtest must satisfy

1. **Sufficient OOS trade count** on BTCUSDT.
2. **Positive BTCUSDT OOS expectancy under HIGH cost.** §11.6
   binding.
3. **ETHUSDT comparison directionally supportive but cannot rescue
   BTC.** §1.7.3 / Phase 4g §10 / Phase 4k preserved.
4. **Active-regime > inactive-regime baseline** (M1 negative test).
5. **G1 > always-active baseline** (M2).
6. **Inside-regime co-design validity** (M3).
7. **No PBO / DSR / CSCV failure** if grid search is used.
8. **No overconcentration in one month / regime** (CFP-7).
9. **No data governance violation** (Phase 4j §11 / Phase 3r §8 /
   Phase 3v §8 / Phase 3w preserved).
10. **No forbidden input access** (Phase 4j §11.3, Phase 4n
    forbidden-input list).

### Aggregation

A G1 backtest **passes** if all 10 gates are satisfied. **Failure of
any single gate** triggers Verdict B (PARTIAL PASS) or Verdict C
(HARD REJECT) per Phase 4k taxonomy adapted.

---

## Catastrophic-floor predicates

Phase 4o adapts Phase 4k's CFP-1..CFP-12 conceptually. Phase 4o
does NOT define numeric thresholds; Phase 4p must do so.

| Predicate | Concept | Adaptation for G1 |
|---|---|---|
| **CFP-1** | Insufficient trade count | < threshold OOS trades per variant on BTCUSDT |
| **CFP-2** | Negative OOS expectancy under HIGH cost | BTC OOS HIGH mean_R < 0 |
| **CFP-3** | Catastrophic drawdown / PF floor failure | OOS max DD > threshold OR PF < threshold |
| **CFP-4** | BTC failure with ETH pass | BTC fails M1 / M2 / M3 / CFP-2 / CFP-3 but ETH passes |
| **CFP-5** | Train-only performance | train Sharpe > threshold AND OOS Sharpe < threshold |
| **CFP-6** | PBO / DSR failure | PBO > 0.5 OR DSR < 1.96 |
| **CFP-7** | Overconcentration in one month / regime | one calendar month contributes > 50% total R |
| **CFP-8** | Regime sensitivity failure | active-regime expectancy not better than inactive-regime expectancy |
| **CFP-9** | Regime excludes too much data / sample-size collapse | active-regime fraction × signal density × N years yields < 30 OOS trades per variant |
| **CFP-10** | Forbidden input access | optional metrics ratio columns / mark-price / aggTrades / spot / authenticated APIs accessed |
| **CFP-11** | Regime classifier lookahead or dependency on signal | classifier uses future bars OR depends on entry signal presence |
| **CFP-12** | Data governance violation | Phase 4j §11 / Phase 3r §8 / Phase 3v §8 / Phase 3w / V2 backtest-plan methodology violation |

**Any single CFP triggering produces Verdict C HARD REJECT for G1
first-spec**, analogous to F1 / V2 patterns.

---

## Forbidden rescue interpretations

Phase 4o explicitly forbids the following rescue patterns:

### G1 rescue forms (forbidden)

- **G1 as R1a with another volatility filter.** G1 must NOT be
  R1a with a volatility-percentile classifier; G1's classifier is
  a top-level state machine, not a per-bar predicate.
- **G1 as R1b-narrow with a stronger bias threshold.** Same.
- **G1 as V2 with fewer gates.** G1's regime detection is at the
  state-machine level, not part of a per-bar AND chain.
- **G1 as V2 with a regime filter added to the AND chain.** Same.
- **G1 as V2 stop-distance rescue.** G1's stop bounds are derived
  from active-regime volatility, not from V2's failure numbers.
- **G1 as F1 / D1-A / R2 rescue.** G1 is trend-continuation, not
  mean-reversion / contrarian / pullback-retest.

### Forbidden classifier inputs (binding)

- **Using 5m Q1–Q7 findings as regime rules.** Phase 3o §6 forbidden
  question forms preserved.
- **Choosing regime thresholds from prior failed outcomes** (V1 /
  V2 / R1a / R1b / R2 / F1 / D1-A failure pattern statistics).
  Bailey et al. 2014 / Phase 4m.
- **Using future bars or future events.** Lookahead forbidden.

### Forbidden Phase 4o successor actions

- **Immediate backtest after Phase 4o.** Forbidden.
- **Immediate data acquisition from Phase 4o.** Forbidden.
- **Immediate implementation from Phase 4o.** Forbidden.
- **Immediate paper / shadow / live.** FORBIDDEN.

### Forbidden cross-strategy rescue

- **Using G1 to "validate" V2 mechanism findings retroactively.**
  V2 is HARD REJECT terminal; no future research can revise that
  verdict.
- **Using G1 as evidence that R1a / R1b-narrow regime predicates
  were "right all along".** R1a / R1b-narrow remain RETAINED —
  NON-LEADING; G1's potential success would NOT promote them.

---

## What future Phase 4p would need to decide

Phase 4o recommends but does NOT authorize a future **Phase 4p —
G1 Strategy Spec Memo (docs-only)**. Phase 4p must decide:

### Regime classifier specification

- exact regime dimensions (e.g., trend + volatility, or trend +
  volatility + funding context, or composite);
- exact regime classifier formula per dimension (EMA pair, slope
  formulation, ATR percentile band, funding-rate window, etc.);
- exact threshold for transitions between states.

### Regime state machine specification

- exact transition criteria (`inactive → candidate`, `candidate →
  active`, `active → suspended`, `suspended → cooldown`, `cooldown →
  inactive`);
- exact lookback windows;
- exact confirmation / reversion timeouts.

### Inside-regime breakout setup specification

- exact signal timeframe (15m, 30m, or 1h);
- exact HTF bias timeframe (1h or 4h);
- exact setup window N;
- exact breakout structure (Donchian, channel-break, range-break,
  or another well-defined structure);
- exact entry trigger (close > breakout level + buffer; or other
  formulation).

### Stop / target / sizing co-design specification

- exact stop-distance bounds (derived from active-regime volatility
  distribution, NOT from V1's 0.60–1.80 × ATR);
- exact target structure (fixed-R N_R, regime-target, or other);
- exact time-stop horizon;
- whether `regime_active → suspended` forces position exit (Option
  B in §"Strategy-active versus strategy-inactive behavior").

### Threshold grid (if any)

- whether to use a threshold grid at all;
- if yes, the exact axes and cardinalities;
- if yes, commitment to deflated Sharpe / PBO / CSCV per Phase 4k
  methodology.

### Data requirements

- whether existing v002 / Phase 4i / v001-of-5m datasets are
  sufficient;
- if a new family is needed (mark-price 30m / 4h, aggTrades, 1m),
  trigger a separate Phase 4q data-requirements memo BEFORE any
  acquisition.

### Mechanism-check thresholds

- exact M1 / M2 / M3 / M4 numeric thresholds (e.g., active-vs-
  inactive ≥ +0.10R, with bootstrap-CI lower bound > 0).

### Pass / fail gates

- exact CFP-1 trade-count threshold (likely ≥ 30 per variant);
- exact CFP-3 drawdown / PF thresholds;
- exact CFP-6 PBO / DSR thresholds;
- exact CFP-7 monthly overconcentration threshold;
- exact CFP-9 regime sample-size threshold.

### Catastrophic-floor predicates

- adapt Phase 4k CFP-1..CFP-12 with G1-specific thresholds.

### Validation windows

- chronological train / validation / OOS holdout windows (likely
  reusing Phase 4k's `train 2022-01-01..2023-06-30 UTC; validation
  2023-07-01..2024-06-30 UTC; OOS holdout 2024-07-01..2026-03-31
  UTC`, but Phase 4p must explicitly commit).

### Forbidden-rescue interpretations

- explicit per-G1-design forbidden patterns (in addition to Phase
  4o §"Forbidden rescue interpretations").

### Backtest-plan handover

- Phase 4p decides whether the strategy spec memo is followed
  directly by Phase 4q (data requirements; if needed) or by Phase
  4r (backtest-plan memo, analogous to Phase 4k).

**Phase 4o does NOT do any of the above.** Those are Phase 4p's
responsibilities, conditional on separate operator authorization.

---

## What this does not authorize

Phase 4o explicitly does NOT authorize, propose, or initiate any of
the following:

- **Any successor phase.** Phase 4p / Phase 4 canonical / any
  research / implementation / deployment phase NOT authorized.
- **Strategy spec creation.** Phase 4o is hypothesis-spec only.
- **Threshold grid definition.** Deferred to Phase 4p.
- **Complete entry / exit rule set definition.** Deferred to
  Phase 4p.
- **V3 implementation.** Forbidden as alias for V2 rescue.
- **V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec.**
  All forbidden.
- **F1 / D1-A / R2 rescue spec.** All forbidden.
- **Phase 4g V2 strategy-spec amendment.** Preserved verbatim.
- **Phase 4j §11 metrics OI-subset rule amendment.** Preserved
  verbatim.
- **Phase 4k V2 backtest-plan methodology amendment.** Preserved
  verbatim.
- **§11.6 / §1.7.3 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r
  §8 modification.** All preserved verbatim.
- **R3 baseline-of-record / H0 framework anchor / V1 strategy spec
  revision.** Preserved.
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

- **No Phase 4p / Phase 4 canonical / successor phase started.**
- **No V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec
  authored.**
- **No V3 or any new strategy spec authored.**
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
- **No public Binance endpoint consulted.**
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4o performs no network I/O.
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
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k / 4l / 4m / 4n text
  modification.**
- **No Phase 4g V2 strategy-spec modification.**
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
  Phase 4o branch.** Per Phase 4o brief.
- **No optional ratio-column access in any code.** Phase 4o is
  text-only; no code at all.
- **No merge to main.**
- **No successor phase started.**

---

## Remaining boundary

- **Recommended state:** **paused** outside conditional Phase 4p
  authorization. Phase 4o deliverables exist as branch-only
  artefacts pending operator review.
- **Phase 4o output:** docs-only hypothesis-spec memo + Phase 4o
  closeout artefact.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified at Phase 4o start).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4n all merged. Phase
  4o hypothesis-spec memo on this branch.
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
  (preserved verbatim); 18-requirement fresh-hypothesis validity
  gate binding.
- **Phase 4n fresh-hypothesis discovery:** complete (preserved
  verbatim); Candidate B (Regime-First Breakout Continuation)
  selected as primary.
- **G1 — Regime-First Breakout Continuation hypothesis:**
  predeclared by Phase 4o (this phase) as a new ex-ante research
  candidate. Conditional on separate operator authorization, Phase
  4p would proceed to a docs-only G1 strategy-spec memo.
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **OPEN ambiguity-log items after Phase 4o:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2
  HARD REJECT (Phase 4l, structural CFP-1 critical, terminal for V2
  first-spec); §11.6 = 8 bps HIGH per side; §1.7.3 project-level
  locks; mark-price stops; v002 verdict provenance; Phase 3q
  mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4o/regime-first-breakout-hypothesis-spec`
  exists locally and (after push) on `origin`. NOT merged to main.

---

## Operator decision menu

### Option A — Phase 4p G1 Strategy Spec Memo (PRIMARY RECOMMENDATION)

Authorize a separate **docs-only** Phase 4p — G1 Strategy Spec
Memo. Phase 4p would predeclare:

- exact regime classifier formula and dimensions;
- exact regime state machine transitions and thresholds;
- exact inside-regime breakout setup geometry (signal timeframe,
  HTF bias timeframe, setup window N, breakout structure);
- exact stop / target / sizing co-design (stop-distance bounds
  from active-regime volatility distribution; target structure;
  time-stop horizon);
- exact threshold grid (if any) with deflated Sharpe / PBO / CSCV
  commitment;
- exact data requirements (with confirmation that existing data
  suffices, OR explicit Phase 4q data-requirements memo trigger);
- exact M1 / M2 / M3 / M4 mechanism-check thresholds;
- exact CFP-1..CFP-12 catastrophic-floor predicate thresholds;
- exact validation windows (likely reusing Phase 4k's split);
- explicit forbidden-rescue interpretations specific to G1 spec.

Phase 4p would NOT acquire data, NOT run backtests, NOT implement
code, NOT propose paper / shadow / live.

### Option B — Remain paused (CONDITIONAL SECONDARY)

If the operator prefers not to commit to Phase 4p immediately,
remain paused is the safe alternative. Phase 4o's G1 hypothesis
remains predeclared but unrealized.

### Option C — Phase 4q data-requirements memo first (NOT RECOMMENDED unless data-readiness blocker)

Phase 4q before Phase 4p would only be necessary if the operator
wants to predetermine data requirements before specifying the
strategy. Phase 4o's data-readiness assessment indicates this is
NOT necessary for plausible G1 designs that reuse v002 / Phase 4i
existing data. Only triggers Phase 4q if Phase 4p chooses
mark-price 30m / 4h, aggTrades, or 1m kline data.

### Option D — Immediate G1 backtest (REJECTED)

A backtest before Phase 4p strategy-spec is data-snooping. REJECTED.

### Option E — V2 / F1 / D1-A / R2 rescue (REJECTED / FORBIDDEN)

Per Phase 4m §"Forbidden rescue observations".

### Option F — Paper / shadow / live / exchange-write / Phase 4 canonical (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`.

### Phase 4o recommendation

**Phase 4o recommendation: Option A (Phase 4p — G1 Strategy Spec
Memo, docs-only) primary; Option B (remain paused) conditional
secondary.** Options C / D / E / F not recommended / rejected /
forbidden.

---

## Next authorization status

**No next phase has been authorized.** Phase 4o's recommendation is
**Option A (Phase 4p — G1 Strategy Spec Memo, docs-only) as
primary**, with **Option B (remain paused) as conditional
secondary**. Other options not recommended / rejected / forbidden.

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
memo is complete (per Phase 4m; 18-requirement validity gate
binding). The Phase 4n fresh-hypothesis discovery memo is complete
(per Phase 4n; Candidate B selected). The Phase 4o regime-first
breakout hypothesis-spec memo is complete on this branch (this
phase).

**Recommended state remains paused outside conditional Phase 4p
spec memo. No next phase authorized.**
