# Phase 4u — Volatility-Contraction Expansion Breakout Hypothesis Spec Memo

**Authority:** Operator authorization for Phase 4u (Phase 4t §"Operator decision menu" Option B conditional secondary alternative — docs-only hypothesis-spec memo on Phase 4t Candidate D, only if separately authorized; operator has so chosen). Phase 4t (post-G1 fresh-hypothesis discovery memo); Phase 4s (post-G1 strategy research consolidation memo); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology binding); Phase 4p (G1 strategy spec locked); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery memo); Phase 4m (post-V2 consolidation; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4f (external strategy research landscape memo); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t (5m diagnostic thread closure); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/04-data/live-data-spec.md`; `docs/04-data/timestamp-policy.md`; `docs/04-data/dataset-versioning.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4u — **Volatility-Contraction Expansion Breakout Hypothesis Spec Memo** (docs-only). Defines C1 — Volatility-Contraction Expansion Breakout as a new ex-ante research candidate at the hypothesis-spec layer, predeclared before any data is touched and before any strategy spec / backtest plan / backtest execution exists. **Phase 4u does NOT create a strategy spec, name a runnable strategy beyond the conceptual name, define exact thresholds, define a threshold grid, define a backtest plan, run a backtest, run diagnostics, acquire data, modify data, modify manifests, write code, modify `src/prometheus/`, modify tests, modify scripts, authorize Phase 4v, or authorize paper / shadow / live / exchange-write.** **Phase 4u is text-only.**

**Branch:** `phase-4u/volatility-contraction-expansion-hypothesis-spec`. **Memo date:** 2026-05-03 UTC.

---

## Summary

Phase 4u defines **C1 — Volatility-Contraction Expansion Breakout** as the project's second regime-aware breakout candidate after G1's terminal failure. C1 is conceptually distinct from G1 in a structurally important way: G1 used a top-level multi-dimension regime state machine that suppressed entry evaluation on most bars (causing a 2.03% active-fraction outcome and zero qualifying trades in Phase 4r); C1 instead uses **local volatility-contraction state as a setup precondition** with the entry rule firing **on or near the contraction-to-expansion transition itself**. Phase 4u commits, before any data is touched, the binding design principles (contraction is local and short-lived; entry is tied to the transition itself; no top-level state machine; no five-dimension AND classifier; no R1a-style per-bar bolt-on filter; no V2 / G1 / D1-A / F1 / R2 rescue; opportunity-rate viability must be predeclared before any data touch in any future Phase 4v memo) and the conceptual mechanism-check / negative-test / pass-fail / catastrophic-floor frameworks (M1 contraction-state validity; M2 expansion-transition value-add; M3 opportunity-rate / sample viability; M4 BTC primary / ETH comparison; optional M5 compression-box structural validity; CFP-1..CFP-12 adapted from Phase 4q; CFP-9 enriched as opportunity-rate / sparse-intersection collapse). **C1 is pre-research only: not implemented; not strategy-specced; not backtest-planned; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A / V2 / G1.** Phase 4u recommends **Option A — Phase 4v C1 Strategy Spec Memo (docs-only) as primary**, with **remain paused as conditional secondary**. Phase 4u does NOT authorize Phase 4v. **Phase 4u is the conceptual / theoretical hypothesis layer only**; the strategy-spec layer (exact thresholds; threshold grid; mechanism-check numeric thresholds; CFP numeric thresholds; data inputs; timeframes; structural-stop / target / time-stop / sizing exact rules; chronological train / validation / OOS holdout window choice) is deferred entirely to a separately authorized Phase 4v.

## Authority and boundary

- **Authority granted:** create the Phase 4u docs-only hypothesis-spec memo; create the Phase 4u closeout; name the conceptual hypothesis family (C1); define first-principles theory; define high-level design principles; define allowed and forbidden conceptual components; define opportunity-rate viability requirements conceptually; define future mechanism-check / negative-test / pass-fail / catastrophic-floor frameworks conceptually; recommend a future Phase 4v docs-only strategy-spec memo if justified, or remain-paused.
- **Authority NOT granted:** create a full strategy spec (forbidden); create a runnable strategy (forbidden); use any implementation name V3 / H2 / G2 / any runnable candidate name (forbidden); define exact thresholds (forbidden); define a threshold grid (forbidden); define a backtest plan (forbidden); run a backtest (forbidden); run diagnostics (forbidden); acquire / modify / patch / regenerate / replace data (forbidden); modify manifests (forbidden); create v003 (forbidden); modify `src/prometheus/`, tests, or existing scripts (forbidden); authorize Phase 4v or any successor phase (forbidden); authorize paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials (forbidden).
- **Hard rule:** Phase 4u is text-only. No code is written. No data is touched. No backtest is run. No exact thresholds are introduced; placeholder values, if any, are explicitly deferred to a future Phase 4v decision and are NOT adopted rules.
- **Naming hard rule:** the candidate is named **C1 — Volatility-Contraction Expansion Breakout**. The candidate must NOT be referred to as V3 / H2 / G2 / G1-prime / G1-extension / R1c / R3-prime / V2-prime, or any other rescue-implying label.

## Starting state

```text
Branch (Phase 4u):   phase-4u/volatility-contraction-expansion-hypothesis-spec
main / origin/main:  aa4716a43832f22238f1ba63857198490908e618 (unchanged)
Phase 4t merge:      5e831d2a1f0e881f963a44d1cf8b1a7fb6b83b5b (merged)
Phase 4t housekeeping: aa4716a43832f22238f1ba63857198490908e618 (merged)
Working-tree state:  clean (no tracked modifications); only gitignored
                     transients .claude/scheduled_tasks.lock and
                     data/research/ are untracked and will not be committed.
Quality gates (verified at memo creation):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Why this memo exists

Phase 4t evaluated eight candidate spaces after the G1 hard reject and recommended **Option A — remain paused** as primary, with **Option B — Phase 4u on Candidate D** as conditional secondary, only if the operator explicitly chose to continue research now. The operator chose Option B. Phase 4u therefore exists to define Candidate D conceptually as **C1 — Volatility-Contraction Expansion Breakout**, before any strategy spec / backtest plan / backtest execution work, with explicit predeclaration of how C1 differs from G1 / R1a / V2 / D1-A / F1 / R2 (Phase 4t's "Moderate" rescue-risk distance from those lines must be raised to "Strong" by careful design before any Phase 4v authorization).

Phase 4u also exists to **distill the Phase 4r G1 lesson into C1's design discipline** without using Phase 4r forensic numbers as tuning inputs. The G1 lesson was: **regime gates can destroy sample size and prevent expectancy evaluation entirely** if the gate's selectivity is high and its frequency is low. C1's design imposes a structural answer: contraction is a *local* precondition, not a *broad* regime; the entry rule fires on the *transition*, not despite the state.

## Relationship to Phase 4t

- Phase 4t recommended remain-paused as primary and Phase 4u (docs-only) on Candidate D as conditional secondary.
- The operator has now chosen Option B; Phase 4u is authorized as docs-only.
- Phase 4u operates under the Phase 4m 18-requirement validity gate, the Phase 4s rejection topology, the Phase 4s reusable insights, and the Phase 4s + Phase 4t forbidden-rescue observations.
- Phase 4u does NOT modify Phase 4t. Phase 4t's discovery framework, candidate scoring, and forbidden-rescue observations are binding inputs.
- **Phase 4u must NOT** create a strategy spec, run a backtest, acquire data, or implement code. Phase 4u must NOT authorize Phase 4v.

## Relationship to prior strategy research

C1 must be evaluated against the full project rejection topology, not just G1. Compact recap (Phase 4s):

```text
Strategy   Rejection mode                                  Mechanism evidence layer
---------- ----------------------------------------------- --------------------------------------
R2         cost-fragility                                  failed WITH evidence
F1         catastrophic-floor                              failed WITH evidence
D1-A       mechanism / framework mismatch                  failed WITH evidence
V2         design-stage incompatibility                    failed BEFORE evidence
G1         regime-gate-meets-setup intersection sparseness failed BEFORE evidence
```

C1 is a continuation / breakout family candidate (like R3 / V2 / G1), not a mean-reversion family (F1) or directional-funding family (D1-A) or pullback family (R2). C1's failure-mode targeting is therefore most relevant against V2 (design-stage incompatibility) and G1 (regime-gate sparseness). C1's design intent is to *avoid both V2's setup-vs-stop-filter incompatibility and G1's regime-gate sparseness simultaneously*, by making the contraction-to-expansion transition a single, local, opportunity-generating event rather than a multi-dimension AND-classifier or an inherited stop-distance bound.

Retained verdicts and locks (preserved verbatim by Phase 4u):

```text
H0           : FRAMEWORK ANCHOR (Phase 2i §1.7.3)
R3           : BASELINE-OF-RECORD (Phase 2p §C.1 — V1 breakout)
R1a          : RETAINED — NON-LEADING
R1b-narrow   : RETAINED — NON-LEADING
R2           : FAILED — §11.6 cost-sensitivity gate
F1           : HARD REJECT (Phase 3c §7.3 catastrophic-floor)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3h §11.2)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
V2           : HARD REJECT — terminal for V2 first-spec (Phase 4l)
G1           : HARD REJECT — terminal for G1 first-spec (Phase 4r)

§11.6        : 8 bps HIGH per side (preserved verbatim)
§1.7.3       : 0.25% risk / 2× leverage / 1 position / mark-price stops
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
Phase 3r §8                 : mark-price gap governance
Phase 3v §8                 : stop-trigger-domain governance
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
Phase 4j §11                : metrics OI-subset partial-eligibility (binding)
Phase 4k                    : V2 backtest-plan methodology (binding)
Phase 4p / Phase 4q         : G1 strategy-spec / methodology (binding)
```

## Hypothesis name

```text
C1 — Volatility-Contraction Expansion Breakout
```

The conceptual letter `C` denotes "Compression / Contraction" and is deliberately distinct from `R` (R1a / R1b-narrow / R2 / R3), `V` (V1 / V2), `F` (F1), `D` (D1-A), `H` (H0), and `G` (G1) — none of which carry a contraction-as-precondition framing.

**Forbidden alternative names** (would imply rescue):

```text
V3
G2
H2
G1-prime
G1-extension
G1-narrow
G1-hybrid
R1c
R3-prime
V2-prime
V2-narrow
V2-relaxed
```

The `VC1` alternative is acceptable but Phase 4u uses **C1** unless a future Phase 4v memo explicitly justifies a name change.

## Core hypothesis

**C1's core hypothesis (plain language):** BTCUSDT trend-continuation breakouts may be more meaningful and more cost-resilient when they occur **on or near the moment a local volatility-contraction state transitions into volatility expansion in a directional manner**.

Five clauses make this hypothesis distinct from prior rejected lines:

1. **Contraction is local, not broad.** The contraction state is measured over a short, recent window (on the order of a few bars to a few dozen bars on the candidate signal timeframe), not across multi-day or multi-week regimes.
2. **Contraction is a precondition, not a gate.** Contraction does not suppress entry evaluation across most bars. It identifies *where in time* the candidate setup is allowed to fire — namely, at the transition, not afterwards. Outside contraction-to-expansion windows, the candidate setup does not fire because the rule itself is tied to the transition, not because the transition acts as a global filter.
3. **Entry fires on the transition itself.** The candidate setup is **the directional release of compression**, not a generic breakout that happens to occur during a contraction state. Late entries after the transition has already played out are not C1 candidates.
4. **The purpose is to detect compression releasing into directional movement** — capturing the move from low realized volatility into directional expansion — not to filter a pre-existing R3 / V2 / G1 setup.
5. **Opportunity-rate viability is intrinsic to the theory.** Contraction-to-expansion transitions occur with predictable frequency (locally); the candidate's design must make that frequency derivable from first principles before any data is touched.

C1's central testable claim, expressed in conceptual terms, is: *expansion entries timed to contraction releases out-perform comparable always-active breakouts under §11.6 = 8 bps HIGH cost realism, with adequate OOS sample size, on BTCUSDT primary with ETHUSDT cross-symbol consistency.*

## Why this is not a rescue

C1 must be sharply distinguished from each prior rejected line. Phase 4u records the binding distinctions:

**vs. G1 (regime-gate-meets-setup intersection sparseness):**

- G1 used a five-dimension AND classifier (HTF trend AND DE_4h ≥ E_min AND ATR percentile in band AND relative-volume ≥ V_liq_min AND funding percentile in band) plus a 4-state regime state machine (`regime_inactive` / `regime_candidate` / `regime_active` / `regime_cooldown`) with `K_confirm` confirmation length, that suppressed entry evaluation on the vast majority of bars.
- C1 must NOT use any top-level multi-dimension AND classifier; must NOT use a state machine that gates entry evaluation across most bars; must NOT reduce G1's five-dimension classifier to a one-dimension volatility-only classifier with the same gating shape; must NOT use Phase 4r forensic numbers (the 2.03% active fraction; the K_confirm ∈ {2, 3} confirmation lengths; the ATR percentile band {[20, 80], [30, 70]}; the V_liq_min ∈ {0.80, 1.00}; the funding band {[15, 85], [25, 75]}; the 124 always-active baseline trades; the −0.34 mean_R always-active outcome).
- C1's contraction is a **local, short-lived precondition**; the transition itself is the entry-generating event.

**vs. R1a (volatility as a per-bar bolt-on filter to R3):**

- R1a used a volatility percentile predicate on the same R3-style breakout setup, applied per-bar.
- C1 must NOT use volatility percentile (or any volatility measure) as a per-bar bolt-on filter on a separate breakout rule; the entry rule itself must depend on the contraction-to-expansion transition.
- C1's setup geometry is *redesigned* around compression release, not augmented from R3.

**vs. V2 (design-stage incompatibility):**

- V2 used a 20/40-bar Donchian setup combined with the V1-inherited 0.60–1.80 × ATR(20) stop-distance filter, which produced ~3–5 × ATR raw stops that were rejected before trade generation.
- C1 must NOT use V2's 20/40-bar Donchian geometry (or any V1-derived Donchian shape); must NOT use V2's stop-distance bounds; must NOT use Phase 4l forensic numbers.
- C1's setup geometry is **derived from compression release** (e.g., compression-boundary breach + ATR-buffered structural stop tied to compression invalidation), not from a Donchian channel pattern.

**vs. D1-A (mechanism / framework mismatch — funding-as-direction):**

- D1-A used trailing-90-day funding-rate Z-score |Z_F| ≥ 2.0 as a contrarian directional trigger.
- C1 must NOT use funding as a directional trigger; if funding is used at all, it is risk-context only (block / size-down), and Phase 4u does NOT mandate that funding be used.

**vs. F1 (catastrophic-floor):**

- F1 was a mean-reversion-after-overextension hypothesis.
- C1 is **continuation / expansion**, not mean-reversion. The directional intent is opposite: expansion *follows* compression in the same direction; mean-reversion *opposes* the prior move.

**vs. R2 (cost-fragility):**

- R2 was a pullback-retest entry that failed §11.6 cost-sensitivity.
- C1 is **expansion entry on transition**, not a pullback retest. C1 must NOT relax §11.6 = 8 bps HIGH per side under any framing.

**Summary distinction:** C1's identity is "directional release of compression" — a categorically distinct mechanism from regime-gating (G1), per-bar volatility filtering (R1a), inherited Donchian + stop-filter (V2), funding-as-direction (D1-A), mean-reversion (F1), and pullback-retest (R2).

## Volatility-contraction expansion design principle

Binding design principles for C1 (any future Phase 4v memo must honor these verbatim):

1. **First identify local contraction.** The contraction state is computed on prior-completed bars only, over a short, recent window.
2. **Then require an expansion transition.** The transition is the moment the local contraction state ends with directional range expansion.
3. **Then consider directional breakout.** Direction is determined by the transition's directional component (e.g., close beyond compression boundary), not by an external regime classifier.
4. **Contraction must be a local setup precondition, not a long-lived top-level regime.** The contraction state should typically last on the order of bars to dozens of bars on the candidate signal timeframe; longer "regimes" are out of scope for C1.
5. **Entry opportunity must be generated by the transition itself.** No "candidate setup that happens to fire during a contraction state" — the entry rule must be tied to the transition event.
6. **No multi-dimension AND classifier.** A single contraction-state precondition + a single transition trigger is the design intent. Adding more dimensions risks G1-style sparse-intersection failure.
7. **No top-level state machine that suppresses most bars.** If a state machine is used at all in Phase 4v, it must not have the G1 shape (`inactive` / `candidate` / `active` / `cooldown` over a multi-dimension classifier).
8. **All calculations must use prior-completed data only.** No future-bar leakage. No partial-bar consumption for strategy decisions.
9. **No thresholds chosen from V2 or G1 forensic outcomes.** Phase 4l's 3–5 × ATR observation, V2's locked Phase 4g axes, G1's locked Phase 4p axes, and Phase 4r's 2.03% / 124-trade / −0.34 mean_R numbers are all forbidden as tuning inputs for any Phase 4v decision.
10. **Opportunity-rate viability must be predeclared before any data touch in any future Phase 4v memo.** This is the central design discipline lesson from G1.

## Local precondition versus top-level regime gate

This section is critical. C1's identity hinges on the distinction.

**G1's failure mode (Phase 4r):** the five-dimension AND classifier produced `regime_active = true` for only 2.03% of OOS BTC 30m bars for the train-best variant. Because the breakout setup was independent of the classifier and fired at its own arrival rate, the joint event `(regime_active AND breakout_setup AND stop_distance_pass)` produced zero qualifying entries on OOS HIGH for the train-best variant. The classifier's selectivity was high; its frequency was low; the joint with the entry rule was empty.

**C1's structural answer:** the contraction state is *local* (short-lived, recent, frequently occurring), and the entry rule *fires on the transition*. This is structurally different from G1 in three ways:

- **Frequency.** Contraction states should occur frequently in normal markets; bars exhibiting recent low realized volatility / range compression are common.
- **Tied entry.** The entry rule does NOT fire whenever the precondition is true; it fires *as the precondition ends* (the transition). This means the entry-generating event is the *change*, not the *state*.
- **No AND-conjunction across regime dimensions.** C1's precondition is a *single* contraction concept (operationalized by a single measure in Phase 4v, e.g., ATR percentile, Donchian width, realized volatility, narrow-range structure — *one* of these, not all five).

**C1 must not repeat G1's mistake** by replacing a five-dimension regime gate with a one-dimension volatility-only gate. The shape of the failure (broad gate; sparse joint with entry rule) is what matters, not the dimension count. The C1 design intent is that the contraction-state precondition should be *transient* (lasting briefly), and the entry rule should fire *during the transient ending*, not over the duration of the precondition.

**Future Phase 4v must explicitly predeclare:**

- **Maximum contraction-state persistence** (a contraction state cannot last indefinitely; if it does, the candidate setup expires).
- **Maximum delay between contraction ending and breakout trigger** (the entry rule fires at transition; "near transition" must be bounded).
- **Minimum opportunity-rate floor** (intrinsic to the theory; predeclared *before* any data is touched; NOT derived from Phase 4r forensic numbers).
- **Negative controls** that detect a G1-style sparse-intersection failure early (e.g., always-active baseline on the same setup geometry; non-contraction breakout baseline; delayed-breakout baseline).

## Contraction state concept

**Conceptually only**, contraction may be measured by one of the following dimensions on the candidate signal timeframe (Phase 4v will choose exactly one; Phase 4u does NOT pick):

- **Range compression** — a rolling window of high-low ranges below a percentile / threshold.
- **ATR percentile** — current ATR ranked low within a recent window.
- **Donchian width** — recent Donchian-channel width below a threshold.
- **Realized volatility** — a short-window rolling standard deviation of returns below a threshold.
- **Inside-bar / narrow-range structure** — series of inside bars or sequence of narrow-range bars.

Constraints (binding for any Phase 4v decision):

- Contraction must be **local** (a few to a few dozen bars on signal timeframe).
- Contraction must be **recent** (computed on prior-completed bars; no future-bar leakage).
- Contraction **cannot be a generic market regime** (e.g., cannot be defined over multi-day / multi-week windows in a way that creates G1-style broad gating).
- Contraction must be **identifiable on existing trade-price klines** (Phase 4i v001 30m / 4h klines; v002 15m / 1h-derived klines).
- Contraction must NOT require order book, aggTrades, mark-price, spot, cross-venue, or private data.
- Contraction logic must NOT use Phase 4r active-fraction numbers, Phase 4l forensic stop-distance numbers, or any other prior-rejected-strategy numeric values.

## Expansion transition concept

**Conceptually only**, the expansion transition may be detected by one of the following dimensions:

- **Range expansion** — current bar's high-low range exceeds the prior contraction window's range by some factor.
- **Close beyond compression boundary** — directional close past the contraction-window high (long) or low (short).
- **ATR expansion** — current ATR exceeds the contraction-window ATR by some factor.
- **Directional close** — closing in the upper / lower fraction of the bar's range, paired with range expansion.

Constraints:

- The transition trigger MUST be tied to the **end of contraction**, not to an arbitrary later breakout. A breakout that occurs many bars after the contraction state has already expired is NOT a C1 candidate.
- The transition trigger MUST be on completed bars only.
- The transition trigger should avoid both:
  - **Too-early noise entries** (a single bar of mild range expansion does not qualify if it is within the contraction's typical noise envelope).
  - **Too-late post-expansion entries** (entries that fire after the move is largely complete are not C1 candidates).
- Future Phase 4v MUST decide the exact transition trigger (one specific rule; no AND-chain of multiple triggers).

## Breakout concept

**Conceptually only**, the C1 breakout is the directional release of compression, distinct from V1 / V2 / G1 breakout shapes:

- Breakout direction MUST be tied to the expansion transition's directional component.
- Breakout MUST be distinct from:
  - V1's 8-bar setup;
  - V2's 20/40-bar Donchian setup;
  - G1's 30m Donchian-after-regime setup;
  - R3's V1 breakout-continuation;
  - R2's pullback-retest.
- Breakout geometry SHOULD be designed around the compression range (e.g., compression-boundary breach + ATR-buffered margin).
- Structural stop SHOULD be tied to compression invalidation (i.e., a return into the compression range invalidates the candidate trade).
- Target and time-stop MUST reflect expected post-compression expansion behavior, not arbitrary fixed-R / fixed-time inherited from V1 / V2 / G1.

## Opportunity-rate viability principle

**This is the most important design discipline in Phase 4u.** It is the structural lesson distilled from Phase 4r G1's failure.

- **C1 MUST include an opportunity-rate viability story BEFORE any backtest** is authorized.
- **The opportunity rate MUST be derived from the conceptual frequency of contraction-to-expansion transitions on BTCUSDT at the candidate signal timeframe**, derived from first principles (e.g., expected fraction of bars exhibiting recent compression × expected fraction of those that resolve in directional expansion within the bounded delay window). The opportunity rate MUST NOT be derived from Phase 4r G1 forensic numbers (the 2.03% active fraction, the 124 always-active trades, the −0.34 mean_R) or from Phase 4l V2 forensic numbers.
- **Future Phase 4v MUST predeclare:**
  - **Minimum candidate-transition rate** — the expected fraction of bars at which a contraction-to-expansion transition is detected.
  - **Minimum joint setup rate** — the expected fraction of those transitions that produce a qualifying directional candidate.
  - **Minimum post-stop-distance-pass rate** — the expected fraction of those candidates that pass the structural stop-distance gate (if any).
  - **What happens if these rates collapse** — i.e., explicit catastrophic-floor predicates (CFP-9-equivalent for sparse-intersection collapse).
- **C1 MUST include a negative control to detect sparse-intersection failure** (e.g., always-active baseline on the same setup geometry; non-contraction breakout baseline; delayed-breakout baseline). The negative control's purpose is to detect a G1-style sparse-intersection failure *before* over-interpreting any mechanism evidence.
- **Phase 4u does NOT set exact numeric floors for opportunity-rate viability.** Any numeric values that appear in Phase 4u (if any) are explicitly **deferred placeholders, not adopted rules**, and Phase 4v must derive its own from first principles.

## Candidate design dimensions

Phase 4u evaluates each dimension qualitatively. **Phase 4u does NOT select final values; selections are deferred to Phase 4v.**

### Contraction measure

| Option | Why it may matter | Rescue risk | Data required |
|---|---|---|---|
| ATR percentile | rank-based, robust to scale | risk: re-creates R1a's per-bar volatility filter if applied as boolean gate; mitigation: use as a precondition with maximum-persistence bound, not a per-bar filter | klines (existing) |
| Donchian width | range-based, parametric | risk: re-creates V2's 20/40-bar Donchian shape if windows are V2-like; mitigation: use shorter / different window not derived from V2 | klines (existing) |
| High-low range compression | direct measurement | low rescue risk | klines (existing) |
| Realized volatility | return-based | low rescue risk | klines (existing) |
| Inside-bar / narrow-range structure | candle-pattern based | low rescue risk; rich literature | klines (existing) |

Phase 4v must decide one; Phase 4u recommends Phase 4v consider the compactness of the contraction definition (a single, simple measure) over compound measures.

### Expansion trigger

| Option | Why it may matter | Rescue risk | Data required |
|---|---|---|---|
| Range expansion | direct measurement | low rescue risk | klines |
| Close beyond compression boundary | natural for compression-release framing | risk: re-creates Donchian-style breakout if compression boundary is Donchian-derived; mitigation: tie boundary to compression measure (high/low of compression window) | klines |
| ATR expansion | ratio-based | low rescue risk | klines |
| Directional breakout close | direction confirmation | low rescue risk | klines |

Phase 4v must decide one (or a combination if explicitly justified).

### Directional confirmation

| Option | Why it may matter | Rescue risk | Data required |
|---|---|---|---|
| Close location | candle-shape directional signal | low rescue risk | klines |
| Candle body fraction | trend strength signal | low rescue risk | klines |
| HTF directional context (shaping input) | adds context without gating | risk: re-creates G1-style HTF gate if used as boolean precondition; mitigation: use as continuous shaping parameter (e.g., target multiplier), not gate | klines |
| Volume expansion | confirms participation | low rescue risk; volume is in existing klines | klines |

Phase 4v must decide.

### Stop model

| Option | Why it may matter | Rescue risk | Data required |
|---|---|---|---|
| Compression-box invalidation | structurally tied to hypothesis | low rescue risk; preferred | klines |
| ATR-buffered boundary | volatility-aware | risk: re-creates V2 stop-distance bounds if buffer ranges are V2-like; mitigation: derive buffer from compression-box, not from V1 / V2 forensic numbers | klines |
| Structural low/high (without ATR) | simple | risk: re-creates V1 / G1 structural-stop pattern; mitigation: combine with compression-box | klines |

Phase 4v must decide; Phase 4u recommends compression-box invalidation as the primary stop framing.

### Target model

| Option | Why it may matter | Rescue risk | Data required |
|---|---|---|---|
| Fixed-R | simple | risk: re-creates V1 / R3 / G1 fixed-R pattern; not necessarily a rescue but does inherit a familiar shape | klines |
| Measured move based on compression range | structurally tied to hypothesis | low rescue risk; preferred for C1 framing | klines |
| Hybrid target + time-stop | balanced | low rescue risk | klines |

Phase 4v must decide.

### Timeframe

| Option | Why it may matter | Rescue risk | Data required |
|---|---|---|---|
| 30m signal | likely primary | low rescue risk; matches G1 timeframe but not G1 rule | Phase 4i 30m klines |
| 1h optional context | shaping only | risk: re-creates G1 1h gating pattern if used as gate; mitigation: continuous shaping only | v002 1h-derived klines |
| 4h only as context, not gate | HTF awareness without gating | low rescue risk | Phase 4i 4h klines |
| Sub-30m signal (e.g., 15m, 5m) | finer detection | risk: 5m is the diagnostic-only thread per Phase 3t §14.2; 15m is V1's signal timeframe; either may carry rescue overtones; mitigation: prefer 30m | klines (existing for 15m; 5m forbidden as features) |

Phase 4v must decide; Phase 4u recommends 30m primary signal.

## Entry / stop / target / sizing co-design principles

The V2 lesson (setup geometry / stop / target / sizing must be co-designed) and the G1 lesson (regime gate / entry-rule arrival / sample-size viability must be co-designed) both apply to C1. Phase 4v MUST honor both:

- **Setup geometry (compression box)** must be designed *together with* the structural stop. The stop should represent compression-box invalidation; the setup should not import a stop model from V1 / V2 / G1.
- **Wide stops are NOT automatically invalid** if fixed-risk sizing controls trade-level risk; risk is normalized via 0.25% per trade.
- **Tight stops CAN be invalid** if they sit inside compression noise (i.e., the structural stop level is within the compression range and would be hit by normal compression bar action).
- **Target should be plausible for post-compression expansion** — historically, compression releases tend to produce moves of magnitudes proportional to the compression range itself; a measured-move target tied to the compression range is the default expression.
- **Time-stop should match expected expansion follow-through duration** — typically a small multiple of the compression duration; an excessively long time-stop loses C1's transition-tied identity.
- **Sizing preserves §1.7.3 verbatim:**
  - 0.25% risk per trade.
  - 2× leverage cap.
  - One position max.
- **Stop-trigger-domain governance** from Phase 3v §8 remains preserved: research = `trade_price_backtest`; future runtime = `mark_price_runtime`; future mark-price validation = `mark_price_backtest_candidate`; `mixed_or_unknown` invalid / fail-closed.
- **Break-even / EMA / stagnation governance** from Phase 3w §6 / §7 / §8 remains preserved if Phase 4v uses any of these schemes.

## Cost-sensitivity argument

§11.6 = 8 bps HIGH per side preserved verbatim. C1's cost-survival thesis must come from **catching fewer but stronger expansion transitions**, not from cost-model relaxation. Phase 4u records:

- **§11.6 HIGH cost = 8 bps per side preserved verbatim.** No relaxation under any framing.
- **Taker fee convention preserved** (4 bps per side per Phase 4k / Phase 4l / Phase 4q methodology); any future Phase 4v / 4w backtest MUST include this.
- **No maker rebate assumption.**
- **No live fee assumption.**
- **No cost relaxation.** Phase 3l "B — conservative but defensible" stance preserved.
- **No R2 cheaper-cost rescue.** R2's cost-fragility verdict is binding for any future hypothesis; cost-relaxation rescue is forbidden.

C1's cost-survival argument:

- Because C1 fires only at transitions (relatively few moments per OOS window), trade frequency is low; this means *each trade* must carry sufficient mean_R after costs to survive.
- Lower trade count is **not** sufficient; opportunity-rate AND sample-size floors must both survive.
- Any future backtest MUST include **LOW / MEDIUM / HIGH cost cells** and MUST block framework promotion if HIGH cost fails (R2 pattern preserved verbatim).
- C1 MUST NOT promote a candidate that survives at LOW or MEDIUM cost but fails at HIGH cost.

## Data-readiness assessment

Likely data sources for any Phase 4v / 4w arc on C1:

```text
Existing-data feasible:
  Phase 4i BTCUSDT / ETHUSDT 30m trade-price klines  (research-eligible)
  Phase 4i BTCUSDT / ETHUSDT 4h trade-price klines   (research-eligible)
  v002 BTCUSDT / ETHUSDT 15m trade-price klines      (sanity / fallback)
  v002 BTCUSDT / ETHUSDT 1h-derived trade-price klines  (HTF context)
  v002 BTCUSDT / ETHUSDT funding history             (optional risk context only)
  Existing volume column on klines                    (if used)

Forbidden inputs (binding for any Phase 4v / 4w arc):
  mark-price (any timeframe) unless separately authorized later
  aggTrades
  spot data
  cross-venue data
  order book
  private / authenticated data
  user stream / WebSocket / listenKey
  metrics OI (Phase 4j §11 governance preserved; not used by C1)
  optional metrics ratio columns (Phase 4j §11.3 forbidden)
  5m Q1–Q7 diagnostic outputs as rule inputs (Phase 3t §14.2 preserved)
  V2 Phase 4l forensic stop-distance numbers as design inputs
  G1 Phase 4r active-fraction / 124-trade / -0.34 mean_R numbers as
    tuning targets
```

**Existing data is sufficient for a future docs-only C1 strategy-spec memo (Phase 4v) if C1 uses only trade-price klines and existing volume.** Phase 4u does NOT authorize data acquisition. If a future Phase 4v memo chooses mark-price / aggTrades / spot / order book / cross-venue / private data, **a separate data-requirements phase would be required first** (analogous to Phase 4h for V2). Candidate F-style microstructure data remains rejected at this boundary (per Phase 4t).

## Mechanism-check framework

Conceptual mechanism checks for C1 (any future Phase 4v memo will translate these into numeric thresholds):

### M1 — Contraction-state validity

- **Question:** do breakouts after contraction outperform comparable breakouts not preceded by contraction?
- **Negative control:** non-contraction breakout baseline — same breakout / stop / target / time-stop / cost model, but on bars where the contraction precondition is *absent*.
- **Pass shape:** contraction-population mean_R minus non-contraction-population mean_R is positive AND statistically supported by bootstrap CI (numeric thresholds deferred to Phase 4v).

### M2 — Expansion-transition value-add

- **Question:** do transition-tied entries outperform arbitrary breakout entries?
- **Negative control:** same setup but entries fire at *any* directional breakout (i.e., no transition-timing condition), with the same stop / target / cost.
- **Pass shape:** transition-tied mean_R minus arbitrary-breakout mean_R is positive AND statistically supported.

### M3 — Opportunity-rate / sample viability

- **Question:** is the candidate-transition rate, setup rate, stop-distance-pass rate, and OOS trade count sufficient?
- **Pass shape:** all rates AND OOS trade counts exceed predeclared floors (numeric thresholds deferred to Phase 4v; Phase 4q's `trade_count >= 30` style is a starting reference, but Phase 4v will derive C1-specific floors from first principles, NOT from Phase 4r forensic numbers).

### M4 — BTC primary / ETH comparison

- **Pass shape:** BTCUSDT primary positive expectancy under HIGH cost; ETHUSDT comparison non-negative differential AND directional consistency. **ETH cannot rescue BTC.**

### M5 — Compression-box structural validity (optional)

- **Question:** do stops tied to compression invalidation behave better than generic ATR stops?
- **Negative control:** same setup but with V1-style structural-stop-with-ATR-buffer (note: "comparable" stop, NOT V2's specific 0.60–1.80 × ATR bound — that bound is forbidden).
- **Pass shape:** compression-box stops produce non-degraded mean_R AND lower stop-rejection rate than the generic baseline.
- **Optional:** Phase 4v may include this as a binding gate or a diagnostic only; Phase 4u defers the decision.

**Phase 4u does NOT define numeric thresholds for any mechanism check.** Any thresholds in this memo (if accidentally implied) are deferred to Phase 4v; Phase 4v must derive them from first principles, not from Phase 4r G1 / Phase 4l V2 forensic numbers.

## Negative-test framework

Phase 4u defines the conceptual negative-test menu; Phase 4v selects the binding subset.

```text
non_contraction_breakout_baseline
  same breakout / stop / target / time-stop / cost model;
  entries during non-contraction bars only.
  PURPOSE: M1 validity check.

random_contraction_baseline (optional)
  same active fraction as real classifier;
  separate RNG seed;
  same entry rule;
  same costs.
  PURPOSE: classifier specificity check.
  PHASE 4v DECISION: binding gate vs. diagnostic only.

always_active_breakout_baseline
  same setup geometry;
  no contraction precondition;
  no transition timing.
  PURPOSE: M2 value-add check (analogous to G1's M2 vs. always-active).

delayed_breakout_baseline
  same breakout but fires at a delay after contraction-end;
  tests whether transition timing matters or only the post-state.
  PURPOSE: M2 value-add detail.

active_opportunity_rate_diagnostic
  measure candidate-transition rate, setup rate, post-stop-distance-pass
  rate, OOS trade count by symbol / cost cell / window.
  PURPOSE: M3 viability check; CFP-9-equivalent detection.
```

**If non-contraction or random-contraction performs equally well or better, the C1 hypothesis FAILS** at the mechanism layer.

**If opportunity-rate collapses (sparse-intersection failure analogous to G1's 2.03% outcome), the C1 hypothesis FAILS** at the viability layer.

**If only the train window works (CFP-5 train-only success), the C1 hypothesis FAILS.**

## Pass / fail gate framework

Conceptual future gates (numeric thresholds deferred to Phase 4v):

```text
G1: sufficient OOS trade count                                  (analogous to CFP-1)
G2: positive BTC OOS HIGH expectancy                            (analogous to M3)
G3: C1 > non-contraction baseline                               (M1)
G4: C1 > always-active same-geometry baseline                   (M2)
G5: transition-tied > delayed / arbitrary breakout baseline     (M2 detail)
G6: no overconcentration (single calendar month not >50%)       (CFP-7)
G7: no PBO / DSR / CSCV failure if grid is used                 (CFP-6)
G8: no forbidden input access                                   (CFP-10 / CFP-12)
G9: no data governance violation                                (CFP-12)
G10: no opportunity-rate collapse                               (CFP-9)
```

All ten gates must PASS for C1 framework promotion. Any single gate FAIL = HARD REJECT.

## Catastrophic-floor predicate framework

Conceptual future CFPs adapted from Phase 4q (numeric thresholds deferred to Phase 4v):

```text
CFP-1   insufficient trade count.
CFP-2   negative BTC OOS HIGH expectancy.
CFP-3   catastrophic profit-factor / drawdown.
CFP-4   BTC failure with ETH pass (ETH cannot rescue BTC).
CFP-5   train-only success / OOS failure.
CFP-6   excessive PBO (rank-based + CSCV) / DSR failure.
CFP-7   regime / month overconcentration.
CFP-8   sensitivity fragility (small parameter perturbation produces
        catastrophic degradation).
CFP-9   opportunity-rate / sparse-intersection collapse
        (active fraction collapse OR transition-AND-setup-AND-stop-pass
         rate collapse).
CFP-10  forbidden optional ratio access.
CFP-11  lookahead / transition-dependency violation (entry rule consults
        future bars; entry rule depends on the breakout-trigger of the
        same evaluation; signal emitted outside contraction-to-expansion
        window when window is a Phase 4v-required precondition).
CFP-12  data governance violation (metrics OI loaded; mark-price loaded
        without authorization; aggTrades loaded; spot / cross-venue
        loaded; non-binding manifest loaded; network I/O attempted;
        credentials read; write attempted to data/raw / data/normalized /
        data/manifests; manifest modified; v003 created;
        private / authenticated / user-stream / WebSocket / listenKey
        path touched).
```

CFP-9 is enriched relative to G1's CFP-9 to include both *active fraction* (broad regime collapse, applicable if any state machine is added) AND *transition-AND-setup-AND-stop-pass* (sparse intersection at the joint level, the binding C1 viability concern).

CFP-11 is enriched to include the C1-specific transition-dependency violation: the entry rule must fire **on the transition itself**, not despite the state.

**Phase 4u does NOT define numeric thresholds for any CFP.** Phase 4v must derive them from first principles.

## Forbidden rescue interpretations

**Phase 4u explicitly forbids** (binding for Phase 4v and any successor phase, until and unless a separate explicit operator authorization removes the prohibition):

- **C1 as G1 with a one-dimension volatility-only regime gate** — the gate shape is what failed in G1; reducing dimension count does not change the failure mode.
- **C1 as G1 with relaxed thresholds.**
- **C1 as R1a with a volatility compression filter** — R1a's per-bar filter pattern is forbidden as the C1 operationalization; C1 redesigns the entry rule to depend on the transition itself.
- **C1 as V2 with different Donchian windows** — V2's Donchian shape is forbidden as the C1 setup geometry.
- **C1 as V2 stop-distance rescue** — V2's 0.60–1.80 × ATR bound is forbidden as the C1 stop-distance gate.
- **C1 as R2 pullback-retest** — C1 is expansion entry on transition, not pullback retest.
- **C1 as F1 mean-reversion** — C1 is continuation / expansion, opposite direction to F1's mean-reversion thesis.
- **C1 as D1-A funding-trigger strategy** — C1 must NOT use funding as a directional trigger.
- **C1 as always-active G1** — the always-active baseline produced mean_R = −0.34 under HIGH cost in Phase 4r; promoting it as a candidate is forbidden.
- **C1 as 5m Q1–Q7 strategy** — Phase 3t §14.2 preserved; 5m is diagnostic-only.
- **C1 using Phase 4r active-fraction or always-active numbers as tuning targets** — the 2.03% / 124-trade / −0.34 mean_R numbers are forbidden as Phase 4v decision inputs.
- **C1 using V2 stop-distance forensic numbers** — Phase 4l's "3–5 × ATR" observation, V2's locked Phase 4g axes, and the locked 0.60–1.80 × ATR bound are forbidden as Phase 4v decision inputs.
- **C1 using optional metrics ratio columns** — Phase 4j §11.3 forbidden.
- **C1 using unavailable microstructure data without separate authorization** — Phase 4t Candidate F's data dependency is unresolved; mark-price / aggTrades / spot / order book / cross-venue / private data are forbidden absent a separately authorized data-requirements memo.
- **Immediate C1 backtest** — data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014.
- **Immediate C1 implementation** in `src/prometheus/` — Phase 4 canonical preconditions are not met.
- **Immediate data acquisition** — Phase 4u does NOT authorize acquisition.

## What future Phase 4v would need to decide

If the operator separately authorizes Phase 4v — C1 Strategy Spec Memo (docs-only), it would need to decide (verbatim):

- exact contraction measure (one of: ATR percentile, Donchian width, range compression, realized volatility, inside-bar / narrow-range structure);
- exact expansion transition rule (one of: range expansion, close beyond compression boundary, ATR expansion, directional close);
- exact signal timeframe (recommended: 30m) and context timeframe(s);
- exact breakout setup geometry (compression-box-derived; not Donchian / V2 / G1);
- exact structural stop model (recommended: compression-box invalidation + small ATR buffer derived from compression range);
- exact target model (recommended: measured move based on compression range; alternative: fixed-R or hybrid; numeric values to be predeclared);
- exact time-stop horizon (numeric value to be predeclared; should be a small multiple of compression duration);
- exact position sizing constraints (preserving §1.7.3 verbatim);
- whether volume is used (yes / no; conceptual rule);
- whether funding is excluded or used only as risk context (Phase 4u's recommendation: exclude unless a clear risk-context rule is justified);
- exact opportunity-rate floor derived from first principles (NOT from Phase 4r forensic numbers);
- exact mechanism-check thresholds (M1 / M2 / M3 / M4 + optional M5);
- exact CFP thresholds (CFP-1..CFP-12);
- whether existing data is sufficient (recommended: yes, if C1 stays on trade-price klines + existing volume);
- whether a separate data-requirements memo is needed before any backtest-plan memo (recommended: only if Phase 4v chooses unavailable data);
- chronological train / validation / OOS holdout windows (recommendation: reuse Phase 4k windows verbatim);
- threshold-grid handling policy (recommendation: small grid analogous to Phase 4p's 32-variant 2^5; NOT V2's 512-variant overbreadth);
- governance label preservation (preserved verbatim from Phase 3v / 3w / 4j §11).

**Phase 4u itself does NOT decide any of these. They are all deferred to Phase 4v if ever authorized.**

## What this does not authorize

Phase 4u does NOT authorize:

- Phase 4v execution (must be separately authorized);
- creation of a strategy spec;
- creation of a runnable strategy;
- definition of exact thresholds (any numeric values in Phase 4u are deferred placeholders, not adopted rules);
- definition of a threshold grid;
- definition of a backtest plan;
- a backtest run;
- diagnostics rerun;
- data acquisition of any kind;
- modification of `data/raw/`, `data/normalized/`, or `data/manifests/`;
- creation of new manifests or v003;
- modification of `src/prometheus/`, tests, or existing scripts;
- start of Phase 4 canonical;
- paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- amendment of any project lock (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- amendment of any governance rule (Phase 3r / 3v / 3w / 4j §11 / 4k);
- amendment of any retained verdict (R3 / R2 / R1a / R1b-narrow / F1 / D1-A / V2 / G1 / H0).

## Forbidden-work confirmation

Phase 4u did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run `scripts/phase4r_g1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a strategy spec (deferred to Phase 4v if ever authorized);
- name a runnable strategy (the conceptual name C1 is reserved as the hypothesis layer; no implementation name is created);
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4v / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding driver; CFP-9 independent driver;
                       terminal for G1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price stops
                      (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t
                            : all preserved verbatim
Phase 4u                    : C1 — Volatility-Contraction Expansion Breakout
                              hypothesis-spec memo (this phase; new; docs-only)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              not strategy-specced;
                              not backtest-planned;
                              not implemented; not backtested; not validated;
                              not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : Phase 4v conditional secondary;
                              remain-paused conditional secondary
```

## Operator decision menu

- **Option A — primary recommendation:** Phase 4v — C1 Strategy Spec Memo (docs-only). Phase 4v would translate the Phase 4u hypothesis-spec layer into a complete ex-ante C1 strategy specification with exact thresholds, mirroring Phase 4p's discipline (NOT V2 / G1 numeric thresholds). Phase 4v would be docs-only; would NOT acquire data; would NOT run a backtest; would NOT name a runnable strategy beyond C1.
- **Option B — conditional secondary:** remain paused. Acceptable if the operator prefers not to commit to a C1 strategy-spec layer at this time (or if external evidence shifts the cost / data assumptions, or if the project's research-discovery process improves).

NOT recommended:

- immediate C1 backtest — REJECTED;
- immediate C1 implementation — REJECTED;
- data acquisition of any kind — REJECTED;
- paper / shadow / live-readiness — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN;
- production-key creation / authenticated APIs / private endpoints / user stream / WebSocket — FORBIDDEN;
- MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN;
- exchange-write capability — FORBIDDEN;
- any G1 / V2 / R2 / F1 / D1-A rescue — FORBIDDEN;
- any C1-prime / C1-narrow / C1-extension / C1-hybrid framing — FORBIDDEN at this layer (those concepts are not introduced; if C1's first-spec ever fails in a future Phase 4w, a separate post-rejection consolidation memo would be required, analogous to Phase 4m for V2 and Phase 4s for G1).

**Phase 4v is NOT authorized by this Phase 4u memo.** Phase 4v execution would require a separate explicit operator authorization brief.

## Next authorization status

```text
Phase 4v                       : NOT authorized
Phase 4 (canonical)            : NOT authorized
Paper / shadow                 : NOT authorized
Live-readiness                 : NOT authorized
Deployment                     : NOT authorized
Production-key creation        : NOT authorized
Authenticated REST             : NOT authorized
Private endpoints              : NOT authorized
User stream / WebSocket        : NOT authorized
Exchange-write capability      : NOT authorized
MCP / Graphify                 : NOT authorized
.mcp.json / credentials        : NOT authorized
C1 implementation              : NOT authorized
C1 strategy-spec / threshold grid / backtest plan / backtest execution
                               : NOT authorized; deferred to Phase 4v / 4w / 4x
                                  if separately authorized.
G1 / V2 / R2 / F1 / D1-A rescue: NOT authorized; not proposed
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                               : NOT authorized; data unavailable.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4v (C1 Strategy Spec Memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4u hypothesis-spec boundary.

---

**Phase 4u was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state: Phase 4v conditional primary (or remain paused conditional secondary). No next phase authorized.**
