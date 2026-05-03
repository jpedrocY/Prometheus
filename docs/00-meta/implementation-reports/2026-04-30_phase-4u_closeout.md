# Phase 4u Closeout

## Summary

Phase 4u authored the docs-only hypothesis-spec memo for Candidate D — Volatility-Contraction Expansion Breakout, naming it **C1 — Volatility-Contraction Expansion Breakout**. Phase 4u defines C1 conceptually as the project's second regime-aware breakout candidate after G1's terminal failure (Phase 4r Verdict C HARD REJECT), with explicit anti-G1 design discipline (contraction is local, not broad; entry fires on the transition itself; no top-level state machine; no multi-dimension AND classifier; no V2 / R1a / R2 / F1 / D1-A rescue framing). Phase 4u predeclares the conceptual mechanism-check framework (M1 contraction-state validity; M2 expansion-transition value-add; M3 opportunity-rate / sample viability; M4 BTC primary / ETH comparison; optional M5 compression-box structural validity), the negative-test framework, the pass / fail gate framework, and the catastrophic-floor predicate framework (CFP-1..CFP-12 adapted from Phase 4q with G1 lessons enriched in CFP-9 and CFP-11). Phase 4u was docs-only; no source code, tests, scripts, data, or manifests modified.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4u_volatility-contraction-expansion-hypothesis-spec.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4u_closeout.md                                            (new — this file)
```

No other files modified by Phase 4u.

## Hypothesis-spec conclusion

C1 — Volatility-Contraction Expansion Breakout is now fully defined at the **conceptual hypothesis layer** in the project record. The hypothesis is structurally distinct from G1 (top-level multi-dimension regime gate that suppressed entry evaluation across most bars), R1a (per-bar volatility-percentile bolt-on filter), V2 (20/40-bar Donchian + V1-inherited stop-distance bound), D1-A (funding-as-direction), F1 (mean-reversion), and R2 (pullback-retest). C1 places the contraction-state precondition as **local and short-lived** and ties the entry rule to the **contraction-to-expansion transition itself**, with opportunity-rate viability declared a *binding* design discipline (the central anti-G1 lesson). Phase 4u defers all numeric thresholds and exact rule shapes to a future Phase 4v Strategy Spec Memo. Phase 4u was docs-only; no source code, tests, scripts, data, or manifests modified; C1 remains pre-research only (not implemented; not strategy-specced; not backtest-planned; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A / V2 / G1).

## Relationship to Phase 4t

- Phase 4t recommended remain-paused as primary and Phase 4u (docs-only) on Candidate D as conditional secondary, contingent on explicit operator authorization.
- The operator chose Option B; Phase 4u was authorized as docs-only.
- Phase 4u operates under the Phase 4m 18-requirement validity gate, the Phase 4s rejection topology, the Phase 4s reusable insights, and the Phase 4s + Phase 4t forbidden-rescue observations.
- Phase 4u does NOT modify Phase 4t. Phase 4t's discovery framework, candidate scoring, and forbidden-rescue observations are binding inputs.
- **Phase 4u does NOT** create a strategy spec, run a backtest, acquire data, or implement code.
- **Phase 4u does NOT** authorize Phase 4v.

## Hypothesis name

```text
C1 — Volatility-Contraction Expansion Breakout
```

The conceptual letter `C` denotes "Compression / Contraction" and is deliberately distinct from `R` / `V` / `F` / `D` / `H` / `G` to avoid any rescue overtones. **Forbidden alternative names:** V3, G2, H2, G1-prime, G1-extension, G1-narrow, G1-hybrid, R1c, R3-prime, V2-prime, V2-narrow, V2-relaxed.

## Core hypothesis

BTCUSDT trend-continuation breakouts may be more meaningful and more cost-resilient when they occur **on or near the moment a local volatility-contraction state transitions into volatility expansion in a directional manner**. Five binding clauses:

1. Contraction is local, not broad.
2. Contraction is a precondition, not a gate.
3. Entry fires on the transition itself.
4. The purpose is to detect compression releasing into directional movement.
5. Opportunity-rate viability is intrinsic to the theory.

## Why this is not a rescue

C1 is sharply distinguished from each prior rejected line:

- **vs G1:** no top-level multi-dimension AND classifier; no state machine that suppresses entry evaluation on most bars; no one-dimension volatility-only regime gate that re-creates G1's failure mode at lower dimension count; no use of Phase 4r forensic numbers.
- **vs R1a:** no per-bar volatility-percentile bolt-on filter; the entry rule is redesigned around the transition, not augmented.
- **vs V2:** no V2 20/40-bar Donchian geometry; no V2 0.60–1.80 × ATR stop-distance bound; no use of Phase 4l forensic numbers.
- **vs D1-A:** funding is NOT a directional trigger; if used at all, it is risk-context only (Phase 4u recommends excluding funding from C1 first-spec).
- **vs F1:** continuation / expansion, not mean-reversion.
- **vs R2:** expansion entry on transition, not pullback retest; no cost-model relaxation.

## Local precondition versus top-level regime gate

This is the central anti-G1 lesson. Binding:

- C1 must NOT repeat G1's mistake by replacing a five-dimension regime gate with a one-dimension volatility-only gate; the failure shape (broad gate; sparse joint with entry rule) is what matters, not dimension count.
- The contraction state must be **transient** (lasting briefly) on the candidate signal timeframe.
- The entry rule must fire **during the transient ending** (i.e., the transition), not over the duration of the precondition.
- Future Phase 4v must explicitly predeclare:
  - maximum contraction-state persistence;
  - maximum delay between contraction ending and breakout trigger;
  - minimum opportunity-rate floor (intrinsic to theory; NOT derived from Phase 4r forensic numbers);
  - negative controls that detect a G1-style sparse-intersection failure early.

## Opportunity-rate viability principle

The most important design discipline in Phase 4u, distilled from Phase 4r G1's failure:

- C1 MUST include an opportunity-rate viability story BEFORE any backtest is authorized.
- Opportunity rate MUST be derived from the conceptual frequency of contraction-to-expansion transitions on BTCUSDT, derived from first principles.
- Opportunity rate MUST NOT be derived from Phase 4r G1 forensic numbers (2.03% active fraction, 124 always-active trades, −0.34 mean_R) or Phase 4l V2 forensic numbers.
- Future Phase 4v MUST predeclare: minimum candidate-transition rate; minimum joint setup rate; minimum post-stop-distance-pass rate; what happens if these rates collapse (CFP-9-equivalent).
- C1 MUST include a negative control to detect sparse-intersection failure (always-active baseline; non-contraction baseline; delayed-breakout baseline).
- Phase 4u does NOT set exact numeric floors; any numeric values that appear are deferred placeholders, not adopted rules.

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
                              (NOT gate) | sub-30m forbidden as features
```

## Data-readiness assessment

Existing data appears sufficient for any future Phase 4v / 4w arc on C1 if C1 stays on trade-price klines + existing volume:

- Phase 4i BTCUSDT / ETHUSDT 30m / 4h klines (research-eligible).
- v002 BTCUSDT / ETHUSDT 15m / 1h-derived klines (sanity / fallback / HTF context).
- v002 BTCUSDT / ETHUSDT funding history (optional risk context only).
- Existing volume column on klines (if used).

**Forbidden inputs (binding):** mark-price (any timeframe) unless separately authorized; aggTrades; spot data; cross-venue data; order book; private / authenticated data; user stream / WebSocket / listenKey; metrics OI; optional metrics ratio columns; 5m Q1–Q7 diagnostic outputs as rule inputs; V2 Phase 4l forensic stop-distance numbers; G1 Phase 4r active-fraction / 124-trade / −0.34 mean_R numbers as tuning targets.

**Phase 4u does NOT authorize data acquisition.** If a future Phase 4v memo chooses unavailable data, a separate data-requirements phase would be required first (analogous to Phase 4h for V2).

## Mechanism-check framework

Conceptual future mechanism checks (numeric thresholds deferred to Phase 4v):

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
       BTCUSDT primary positive expectancy; ETHUSDT comparison
       non-negative differential AND directional consistency;
       ETH cannot rescue BTC.
M5 — (optional) Compression-box structural validity:
       stops tied to compression invalidation behave better than
       generic ATR stops; Phase 4v decides binding-vs-diagnostic.
```

Phase 4u does NOT define numeric thresholds for any mechanism check.

## Negative-test framework

Conceptual menu (Phase 4v selects binding subset):

- non-contraction breakout baseline (M1);
- random-contraction baseline (optional; classifier specificity check);
- always-active breakout baseline (M2);
- delayed-breakout baseline (M2 detail);
- active opportunity-rate diagnostic (M3 / CFP-9-equivalent).

If non-contraction or random-contraction performs equally well or better → C1 hypothesis FAILS at mechanism layer. If opportunity-rate collapses → C1 hypothesis FAILS at viability layer. If only train works → C1 hypothesis FAILS (CFP-5).

## Forbidden rescue interpretations

Phase 4u explicitly forbids:

- C1 as G1 with one-dimension volatility-only regime gate;
- C1 as G1 with relaxed thresholds;
- C1 as R1a with volatility compression filter;
- C1 as V2 with different Donchian windows;
- C1 as V2 stop-distance rescue;
- C1 as R2 pullback-retest;
- C1 as F1 mean-reversion;
- C1 as D1-A funding-trigger;
- C1 as always-active G1;
- C1 as 5m Q1–Q7 strategy;
- C1 using Phase 4r active-fraction or always-active numbers as tuning targets;
- C1 using V2 stop-distance forensic numbers;
- C1 using optional metrics ratio columns;
- C1 using unavailable microstructure data without separate authorization;
- immediate C1 backtest;
- immediate C1 implementation;
- immediate data acquisition.

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4v — C1 Strategy Spec Memo (docs-only). Phase 4v would translate the Phase 4u hypothesis-spec layer into a complete ex-ante C1 strategy specification with exact thresholds, mirroring Phase 4p's discipline (NOT V2 / G1 numeric thresholds). Phase 4v would be docs-only; would NOT acquire data; would NOT run a backtest; would NOT name a runnable strategy beyond C1.
- **Option B — conditional secondary:** remain paused.

NOT recommended: immediate C1 backtest (REJECTED); immediate C1 implementation (REJECTED); data acquisition (NOT authorized); paper / shadow / live (FORBIDDEN); Phase 4 canonical (FORBIDDEN); production keys / authenticated APIs / private endpoints / user stream / WebSocket (FORBIDDEN); MCP / Graphify / `.mcp.json` / credentials (FORBIDDEN); exchange-write capability (FORBIDDEN); G1 / V2 / R2 / F1 / D1-A rescue (FORBIDDEN).

**Phase 4v is NOT authorized by this memo or this closeout.** Phase 4v execution requires a separate explicit operator authorization brief.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4u/volatility-contraction-expansion-hypothesis-spec
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q (-> pytest)
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4u_volatility-contraction-expansion-hypothesis-spec.md
git commit -F <commit-message-file>
git push -u origin phase-4u/volatility-contraction-expansion-hypothesis-spec
```

(No acquisition, diagnostics, or backtest scripts were run. No web research was performed for this memo; all analysis is derived from the existing project record and the Phase 4m / Phase 4s / Phase 4t / Phase 4n validity gate frameworks.)

## Verification results

```text
Python version             : 3.12.4
ruff check . (initial)     : All checks passed!
pytest (initial)           : 785 passed
mypy (initial)             : Success: no issues found in 82 source files
git status (initial)       : clean working tree (only gitignored
                              .claude/scheduled_tasks.lock and data/research/
                              untracked; not committed)
git rev-parse main         : aa4716a43832f22238f1ba63857198490908e618
git rev-parse origin/main  : aa4716a43832f22238f1ba63857198490908e618
```

## Commit

```text
Phase 4u memo commit:      0c017f64b57d57a5591a1970c79ecd8c23f15abd
Phase 4u closeout commit:  <recorded after this file is committed>
```

## Final git status

(recorded after closeout commit and push)

## Final git log --oneline -5

(recorded after closeout commit and push)

## Final rev-parse

```text
HEAD                                                                          : <recorded after closeout commit>
origin/phase-4u/volatility-contraction-expansion-hypothesis-spec              : <recorded after closeout push>
main                                                                          : aa4716a43832f22238f1ba63857198490908e618 (unchanged)
origin/main                                                                   : aa4716a43832f22238f1ba63857198490908e618 (unchanged)
```

## Branch / main status

`main` remains unchanged at `aa4716a43832f22238f1ba63857198490908e618`. Phase 4u is authored exclusively on the `phase-4u/volatility-contraction-expansion-hypothesis-spec` branch. Phase 4u is **not** merged to main by this closeout. Any future merge to main requires a separate explicit operator authorization brief (analogous to prior phase merge closeouts).

## Forbidden-work confirmation

Phase 4u did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script;
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
- name a runnable strategy beyond the conceptual hypothesis name C1;
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
