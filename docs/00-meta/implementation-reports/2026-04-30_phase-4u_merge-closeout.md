# Phase 4u Merge Closeout

## Summary

Phase 4u — C1 Volatility-Contraction Expansion Breakout Hypothesis Spec Memo (docs-only) — has been merged into `main` via a no-fast-forward merge commit. Phase 4u defines **C1 — Volatility-Contraction Expansion Breakout** as the project's second regime-aware breakout candidate after G1's terminal failure (Phase 4r Verdict C HARD REJECT). C1 is conceptually distinct from G1: G1 used a top-level multi-dimension regime state machine that suppressed entry evaluation on most bars (causing 2.03% active-fraction and zero qualifying trades); C1 instead uses **local volatility-contraction state as a setup precondition** with the entry rule firing **on or near the contraction-to-expansion transition itself**. Phase 4u predeclares the binding design principles (contraction is local and short-lived; entry is tied to the transition itself; no top-level state machine; no multi-dimension AND classifier; no V2 / G1 / D1-A / F1 / R2 rescue framing; opportunity-rate viability must be predeclared before any data touch in any future Phase 4v memo) and the conceptual mechanism-check / negative-test / pass-fail / catastrophic-floor frameworks. **C1 is pre-research only: not implemented; not strategy-specced; not backtest-planned; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A / V2 / G1.** Phase 4u was docs-only.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4u_volatility-contraction-expansion-hypothesis-spec.md   (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4u_closeout.md                                            (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4u_merge-closeout.md                                     (added by housekeeping commit — this file)
docs/00-meta/current-project-state.md                                                                          (modified by housekeeping commit — narrow Phase 4u paragraph + "Current phase" / "Most recent merge" refresh)
```

No other files modified by Phase 4u or by this merge.

## Phase 4u commits included

```text
0c017f64b57d57a5591a1970c79ecd8c23f15abd   phase-4u: C1 Volatility-Contraction Expansion Breakout hypothesis-spec memo (docs-only)
af746dc923f87d4df485c081a1bdba177c300599   phase-4u: closeout (C1 Volatility-Contraction Expansion Breakout hypothesis-spec memo)
```

## Merge commit

```text
f1b1a30fbc0ae4d120a63c38c9edb9d9b30e734c   Merge Phase 4u (C1 Volatility-Contraction Expansion Breakout hypothesis-spec memo, docs-only) into main
```

## Housekeeping commit

```text
<recorded after this file is committed>
```

## Final git status

(recorded after housekeeping commit and push)

## Final git log --oneline -8

(recorded after housekeeping commit and push)

## Final rev-parse

```text
main          : <recorded after housekeeping push>
origin/main   : <recorded after housekeeping push>
```

## main == origin/main confirmation

(verified after housekeeping push; reported in chat)

## Hypothesis-spec conclusion

- **Phase 4u was docs-only.**
- Phase 4u defines **C1 — Volatility-Contraction Expansion Breakout** as a **conceptual hypothesis layer**.
- **C1 is pre-research only:**
  - not strategy-specced;
  - not backtest-planned;
  - not implemented;
  - not backtested;
  - not validated;
  - not live-ready;
  - **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**.
- **Phase 4u does NOT authorize Phase 4v.**
- Phase 4u does **NOT** authorize backtest, implementation, data acquisition, paper / shadow / live, or exchange-write.
- **No retained verdict is revised.**
- **No project lock is changed.**

## Relationship to Phase 4t

- Phase 4t primary recommendation was remain paused.
- Phase 4t conditional secondary was Phase 4u on Candidate D, only if separately authorized.
- Phase 4u was separately authorized by the operator.
- Phase 4u operates under Phase 4m (18-requirement validity gate), Phase 4s (rejection topology + reusable insights + forbidden-rescue observations), and Phase 4t (discovery framework + candidate scoring + forbidden-rescue observations) governance / anti-rescue boundaries.
- **Phase 4u does NOT modify Phase 4t.** Phase 4t's discovery framework, candidate scoring, and forbidden-rescue observations are binding inputs.

## Hypothesis name

```text
C1 — Volatility-Contraction Expansion Breakout
```

The conceptual letter `C` denotes "Compression / Contraction" and is deliberately distinct from `R` / `V` / `F` / `D` / `H` / `G` to avoid any rescue overtones.

**Forbidden alternative names:**

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

## Core hypothesis

C1's core hypothesis (plain language): *BTCUSDT trend-continuation breakouts may be more meaningful and more cost-resilient when they occur on or near the moment a local volatility-contraction state transitions into volatility expansion in a directional manner.* Five binding clauses:

1. **Contraction is local, not broad.**
2. **Contraction is a precondition, not a gate.**
3. **Entry fires on the transition itself.**
4. **The purpose is to detect compression releasing into directional movement.**
5. **Opportunity-rate viability is intrinsic to the theory.**

## Why this is not a rescue

C1 is sharply distinguished from each prior rejected line:

- **vs G1:** no top-level multi-dimension AND classifier; no state machine that suppresses entry evaluation on most bars; no one-dimension volatility-only regime gate that re-creates G1's failure shape at lower dimension count; no use of Phase 4r forensic numbers (the 2.03% active fraction; the K_confirm ∈ {2, 3} confirmation lengths; the ATR percentile band {[20, 80], [30, 70]}; the V_liq_min ∈ {0.80, 1.00}; the funding band {[15, 85], [25, 75]}; the 124 always-active baseline trades; the −0.34 mean_R always-active outcome).
- **vs R1a:** no per-bar volatility-percentile bolt-on filter on R3's existing setup; the entry rule is **redesigned** around the transition, not augmented.
- **vs V2:** no V2 20/40-bar Donchian geometry; no V2 0.60–1.80 × ATR(20) stop-distance bound; no use of Phase 4l forensic numbers (the "3–5 × ATR" stop-distance observation; V2's locked Phase 4g axes).
- **vs D1-A:** funding is **NOT** a directional trigger; if used at all, it is risk-context only (Phase 4u recommends excluding funding from C1 first-spec).
- **vs F1:** continuation / expansion, not mean-reversion.
- **vs R2:** expansion entry on transition, not pullback retest; **no cost-model relaxation**.

## Local precondition versus top-level regime gate

The central anti-G1 lesson:

- **C1 must NOT repeat G1's failure shape.** Replacing G1's five-dimension AND classifier with a one-dimension volatility-only AND-style gate at lower dimension count would re-create the same failure mode (broad gate; sparse joint with entry rule). The failure shape is what matters, not the dimension count.
- The contraction state is **local, short-lived, and transient** on the candidate signal timeframe.
- The entry rule fires **as the contraction state ends** (the transition).
- **No broad state machine.**
- **No broad gate.**
- Future Phase 4v must explicitly predeclare:
  - **maximum contraction-state persistence** (a contraction state cannot last indefinitely);
  - **maximum delay between contraction ending and breakout trigger** (entry fires "near transition" with bounded delay);
  - **minimum opportunity-rate floor** (intrinsic to the theory; predeclared *before* any data is touched; NOT derived from Phase 4r forensic numbers);
  - **negative controls** that detect a G1-style sparse-intersection failure early.

## Opportunity-rate viability principle

The most important design discipline in Phase 4u, distilled from Phase 4r G1's failure:

- C1 MUST include an opportunity-rate viability story BEFORE any future backtest is authorized.
- Future Phase 4v MUST predeclare:
  - **minimum candidate-transition rate** (expected fraction of bars at which a contraction-to-expansion transition is detected);
  - **minimum joint setup rate** (expected fraction of those transitions that produce a qualifying directional candidate);
  - **minimum post-stop-distance-pass rate** (expected fraction of those candidates that pass the structural stop-distance gate);
  - **collapse handling / CFP-9-equivalent** — what happens if these rates collapse.
- These rates MUST be derived from **first principles** (e.g., expected fraction of bars exhibiting recent compression × expected fraction of those that resolve in directional expansion within the bounded delay window).
- These rates **MUST NOT** be derived from Phase 4r G1 forensic numbers (the 2.03% active fraction, the 124 always-active trades, the −0.34 mean_R) or Phase 4l V2 forensic numbers.
- **Phase 4u does NOT set exact numeric floors.** Any numeric values in Phase 4u (if any) are explicitly **deferred placeholders, not adopted rules**.

## Candidate design dimensions

Phase 4u evaluates each dimension qualitatively. **Phase 4u does NOT select final values; selections are deferred to Phase 4v.**

```text
Contraction measure        : ATR percentile | Donchian width | high-low range
                              compression | realized volatility | inside-bar /
                              narrow-range structure  (Phase 4v decides one)
Expansion trigger          : range expansion | close beyond compression boundary |
                              ATR expansion | directional close
                              (Phase 4v decides one)
Directional confirmation   : close location | candle body fraction | HTF context
                              as continuous shaping (NOT gate) | volume expansion
Stop model                 : compression-box invalidation (recommended) |
                              ATR-buffered boundary derived from compression-box |
                              structural low/high (NOT V1/V2/G1 inherited)
Target model               : measured move based on compression range
                              (recommended) | fixed-R | hybrid + time-stop
Timeframe                  : 30m signal (recommended) | 1h optional context
                              (continuous shaping only) | 4h context only
                              (NOT gate)
```

## Data-readiness assessment

Existing data appears sufficient for any future Phase 4v / 4w arc on C1 if C1 stays on trade-price klines + existing volume:

- Phase 4i BTCUSDT / ETHUSDT 30m / 4h trade-price klines (research-eligible).
- v002 BTCUSDT / ETHUSDT 15m / 1h-derived trade-price klines (sanity / fallback / HTF context).
- v002 BTCUSDT / ETHUSDT funding history (optional risk context only; Phase 4u recommends excluding from C1 first-spec).
- Existing volume column on klines (if used).

**Phase 4u does NOT authorize data acquisition.** If a future Phase 4v memo chooses unavailable data, a separate data-requirements phase would be required first (analogous to Phase 4h for V2).

**Forbidden inputs (binding for any Phase 4v / 4w arc):**

- mark-price (any timeframe) unless separately authorized later;
- aggTrades;
- spot data;
- cross-venue data;
- order book;
- private / authenticated data;
- user stream / WebSocket / listenKey;
- metrics OI (Phase 4j §11 governance preserved; not used by C1);
- optional metrics ratio columns (Phase 4j §11.3 forbidden);
- 5m Q1–Q7 diagnostic outputs as rule inputs (Phase 3t §14.2 preserved);
- V2 Phase 4l forensic stop-distance numbers as design inputs;
- G1 Phase 4r active-fraction / 124-trade / −0.34 mean_R numbers as tuning targets.

## Mechanism-check framework

Conceptual future mechanism checks. **Numeric thresholds deferred to Phase 4v.**

```text
M1 — Contraction-state validity:
       breakouts after contraction outperform comparable breakouts
       not preceded by contraction; non-contraction baseline.
M2 — Expansion-transition value-add:
       transition-tied entries outperform arbitrary breakout entries;
       always-active baseline AND delayed-breakout baseline.
M3 — Opportunity-rate / sample viability:
       candidate-transition rate, setup rate, stop-distance-pass rate,
       and OOS trade count exceed predeclared floors.
M4 — BTC primary / ETH comparison:
       BTCUSDT primary positive expectancy under HIGH cost; ETHUSDT
       comparison non-negative differential AND directional consistency;
       ETH cannot rescue BTC.
M5 — (optional) Compression-box structural validity:
       stops tied to compression invalidation behave better than generic
       ATR stops; Phase 4v decides binding-vs-diagnostic.
```

## Negative-test framework

Conceptual menu (Phase 4v selects the binding subset):

- **non-contraction breakout baseline** (M1 validity check);
- **random-contraction baseline** (optional; classifier specificity check);
- **always-active breakout baseline** (M2 value-add check);
- **delayed-breakout baseline** (M2 detail);
- **active opportunity-rate diagnostic** (M3 / CFP-9-equivalent detection).

**If non-contraction or random-contraction performs equally well or better, the C1 hypothesis FAILS** at the mechanism layer.

**If opportunity-rate collapses (sparse-intersection failure analogous to G1's 2.03% outcome), the C1 hypothesis FAILS** at the viability layer.

## Pass / fail gate framework

Ten conceptual future gates (numeric thresholds deferred to Phase 4v):

1. sufficient OOS trade count;
2. positive BTC OOS HIGH expectancy;
3. C1 > non-contraction baseline;
4. C1 > always-active same-geometry baseline;
5. transition-tied > delayed / arbitrary breakout baseline;
6. no overconcentration;
7. no PBO / DSR / CSCV failure if grid is used;
8. no forbidden input access;
9. no data governance violation;
10. no opportunity-rate collapse.

All ten gates must PASS for C1 framework promotion. Any single gate FAIL = HARD REJECT.

## Catastrophic-floor predicate framework

Conceptual future CFPs adapted from Phase 4q with G1 lessons enriched (numeric thresholds deferred to Phase 4v):

```text
CFP-1   insufficient trade count.
CFP-2   negative BTC OOS HIGH expectancy.
CFP-3   catastrophic profit-factor / drawdown.
CFP-4   BTC failure with ETH pass (ETH cannot rescue BTC).
CFP-5   train-only success / OOS failure.
CFP-6   excessive PBO (rank-based + CSCV) / DSR failure.
CFP-7   regime / month overconcentration.
CFP-8   sensitivity fragility.
CFP-9   opportunity-rate / sparse-intersection collapse
        (active fraction collapse OR transition-AND-setup-AND-stop-pass
         joint collapse) — enriched relative to G1's CFP-9.
CFP-10  forbidden optional ratio access.
CFP-11  lookahead / transition-dependency violation
        (entry rule consults future bars; entry rule depends on the
         breakout-trigger of the same evaluation; signal emitted
         outside contraction-to-expansion window) — enriched for C1.
CFP-12  data governance violation.
```

## Forbidden rescue interpretations

Phase 4u explicitly forbids (binding for Phase 4v and any successor):

- **C1 as G1 with one-dimension volatility-only regime gate**;
- **C1 as G1 with relaxed thresholds**;
- **C1 as R1a with volatility compression filter**;
- **C1 as V2 with different Donchian windows**;
- **C1 as V2 stop-distance rescue**;
- **C1 as R2 pullback-retest**;
- **C1 as F1 mean-reversion**;
- **C1 as D1-A funding-trigger**;
- **C1 as always-active G1**;
- **C1 as 5m Q1–Q7 strategy**;
- **C1 using Phase 4r active-fraction or always-active numbers as tuning targets**;
- **C1 using V2 stop-distance forensic numbers**;
- **C1 using optional metrics ratio columns**;
- **C1 using unavailable microstructure data without separate authorization**;
- **immediate C1 backtest**;
- **immediate C1 implementation**;
- **immediate data acquisition**.

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4v — C1 Strategy Spec Memo (docs-only). Phase 4v would translate the Phase 4u hypothesis-spec layer into a complete ex-ante C1 strategy specification with exact thresholds, mirroring Phase 4p's discipline (NOT V2 / G1 numeric thresholds).
- **Option B — conditional secondary:** remain paused.

**Phase 4v is NOT started by this merge.** Phase 4v execution requires a separate explicit operator authorization brief.

NOT recommended:

- immediate C1 backtest — REJECTED;
- immediate C1 implementation — REJECTED;
- data acquisition — REJECTED;
- paper / shadow / live / exchange-write — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN;
- production-key creation / authenticated APIs / private endpoints / user stream / WebSocket — FORBIDDEN;
- MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN;
- exchange-write capability — FORBIDDEN;
- G1 / V2 / R2 / F1 / D1-A rescue — FORBIDDEN.

## Verification evidence

Quality gates verified clean during Phase 4u and across the merge:

```text
ruff check .   : All checks passed!
pytest         : 785 passed (no regressions)
mypy           : Success: no issues found in 82 source files
```

No code, tests, scripts, data, or manifests were modified by Phase 4u; the quality gates simply confirm that the documentation-only changes did not regress the repository.

## Forbidden-work confirmation

Phase 4u and this merge did NOT do any of the following:

- start Phase 4v or any successor phase;
- create a C1 strategy spec;
- define exact thresholds;
- define a threshold grid;
- define a backtest plan;
- create a runnable strategy;
- create V3 / H2 / G2 / any runnable candidate;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- run a backtest;
- run diagnostics;
- run acquisition scripts;
- modify `src/prometheus/` code;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- modify `data/raw/` / `data/normalized/` / `data/manifests/`;
- commit `data/research/` outputs;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- create v003;
- use metrics OI as a hypothesis input;
- use optional metrics ratio columns;
- use 5m Q1–Q7 findings as rule candidates;
- use V2 Phase 4l stop-distance failure numbers to choose thresholds;
- use Phase 4r G1 active-fraction numbers to choose thresholds;
- use the G1 always-active 124-trade / −0.34 mean_R result as a candidate-tuning target;
- modify Phase 4p G1 strategy-spec selections;
- modify Phase 4q methodology;
- modify Phase 4j §11 governance;
- modify Phase 4k methodology;
- revise retained verdicts;
- revise project locks, thresholds, parameters, or governance rules;
- change §11.6 / §1.7.3 / Phase 3r governance / Phase 3v governance / Phase 3w governance / Phase 4j governance / Phase 4k methodology;
- start Phase 4 canonical;
- implement reconciliation;
- implement a real exchange adapter;
- implement exchange-write capability;
- place or cancel orders;
- use / request / store credentials;
- add authenticated REST / private endpoints / public endpoint clients / user stream / WebSocket / listenKey lifecycle;
- enable MCP / Graphify or modify `.mcp.json`;
- create `.env` files;
- deploy anything;
- create paper / shadow runtime;
- imply live-readiness.

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
                              hypothesis-spec memo (this phase; merged)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              not strategy-specced;
                              not backtest-planned;
                              not implemented; not backtested; not validated;
                              not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : Phase 4v conditional primary;
                              remain-paused conditional secondary
```

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

**Phase 4u was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state: Phase 4v conditional primary; remain-paused conditional secondary. No next phase authorized.**
