# Phase 4ah Closeout — Single-Position Cross-Sectional Trend / Relative-Strength Feasibility Memo

## Phase identity

- Phase title: Single-Position Cross-Sectional Trend / Relative-Strength
  Feasibility Memo
- Phase status: docs-only
- Phase branch: `phase-4ah/single-position-cross-sectional-trend-feasibility`
- Base main SHA: `fa72870ff38e024e80d2d2987d1820bfa1b48c9c`

## Files created

```text
docs/00-meta/implementation-reports/2026-05-04_phase-4ah_single-position-cross-sectional-trend-feasibility.md
docs/00-meta/implementation-reports/2026-05-04_phase-4ah_closeout.md
```

## Files updated narrowly

```text
docs/00-meta/current-project-state.md   (Phase 4ah paragraph added; prior phase preserved)
```

## Phase 4ah summary

Phase 4ah evaluated whether a future Prometheus research lane based
on **single-position cross-sectional trend / relative-strength /
symbol-selection** is admissible after Phase 4ag, while preserving
the project's `one position max` operational lock.

Phase 4ah:

- defined the future mechanism family as
  **single-position cross-sectional trend / relative-strength
  symbol selection** — rank a fixed predeclared symbol universe on
  predeclared trend / relative-strength descriptors using prior-
  completed bars, and select **at most one symbol** for future
  hypothetical consideration, with "no symbol" as a possible
  output;
- recommended that any future feasibility study use the
  **fixed five-symbol Phase 4ac core universe**
  (`BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`) under
  Phase 4ad Rule B1 common-post-gap scope, and that the Phase 4aa
  deferred secondary watchlist (`BNBUSDT`, `DOGEUSDT`, `LINKUSDT`,
  `AVAXUSDT`) **remain deferred**;
- recorded five candidate ranking-descriptor families (multi-
  horizon relative return; relative trend state; volatility-
  adjusted relative strength; volume / notional confirmation;
  market-state conditional ranking) with risk profiles, but
  **did not compute** any descriptors;
- recorded twelve binding **anti-rescue / anti-reduction** rules
  any future research must respect, including no old-strategy
  alt-symbol reruns, no "rank then run V2 / G1 / C1 breakout",
  no post-hoc threshold tuning, no symbol-mining, and explicit
  preservation of `one position max` and §11.6 cost realism;
- applied the Phase 4ag proposed M0 mechanism-admissibility gate
  as a **non-binding diagnostic checklist** (six PASS / four
  CONDITIONAL / zero FAIL), without adopting M0 as binding
  governance;
- defined a possible future Phase 4ai analysis-and-docs design
  sketch with required boundaries, inputs, and outputs, and
  explicitly stated that Phase 4ai is **NOT authorized** by
  Phase 4ah.

Phase 4ah's primary recommendation is to **merge Phase 4ah into
main and then remain paused** unless the operator separately
authorizes a future Phase 4ai single-position cross-sectional
trend feasibility analysis.

## External research availability

External web / literature research was **available** during
Phase 4ah. Three narrow search queries were run:

- "time-series momentum cryptocurrency Han Kang Ryu transaction
  costs realistic assumptions"
- "cryptocurrency momentum crash drawdown volatility-managed
  strategy 2024 2025"
- "single-asset symbol selection relative strength versus
  portfolio momentum factor crypto"

Search results were used to record verbatim references in §4 of
the memo. References were recorded as found (titles, identifiers,
and snippet-verbatim findings); no claims were synthesized beyond
what the search results stated. **No fabricated citations were
introduced.**

The literature review's headline implications recorded in the
memo:

- Time-series momentum is the better-documented crypto family
  (Han / Kang / Ryu 2023, SSRN 4675565); cross-sectional long-
  short factor evidence is weaker.
- Crash / drawdown risk is real and partly forecastable
  (*Cryptocurrency momentum has (not) its moments* 2025).
- Volatility-managed weighting (the standard crash mitigation)
  is a multi-position technique that does **not** directly port
  to single-position selection.
- Practitioner relative-strength models are typically multi-
  position; Prometheus's reframe to single-position is novel
  and is its own design problem.

## Boundary confirmations

Phase 4ah did **NOT**:

- modify or create any source code,
- modify or create any test,
- modify or create any analysis script,
- run any analysis script,
- rerun Phase 4ac, Phase 4ae, Phase 4af, or Phase 4ag,
- acquire data,
- download data,
- call APIs,
- call exchange data endpoints,
- consult `data.binance.vision`,
- use authenticated APIs,
- use private endpoints,
- use public endpoints in code,
- use user stream / WebSocket / listenKey,
- modify raw data,
- modify normalized data,
- patch / forward-fill / interpolate / impute / synthesize /
  regenerate / replace data,
- create or modify any manifest,
- create v003 or any other dataset version,
- run any backtest,
- run any strategy diagnostic,
- rerun Q1–Q7,
- compute strategy PnL,
- compute entry / exit returns,
- optimize any parameter,
- select thresholds for any future strategy,
- create a new strategy candidate,
- name a strategy candidate,
- create a fresh-hypothesis discovery memo,
- create a hypothesis-spec memo,
- create a strategy-spec memo,
- create a backtest-plan memo,
- implement or rescue R3 / R2 / F1 / D1-A / V2 / G1 / C1,
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime /
  G1-prime / C1-prime / V1-D1 / F1-D1 or any cross-strategy hybrid,
- propose old-strategy alt-symbol reruns,
- silently reduce cross-sectional ranking into V2 / G1 / C1-style
  single-symbol breakout continuation,
- propose multi-position portfolio trading,
- adopt the Phase 4z recommendations as binding governance,
- adopt the Phase 4aa admissibility framework as binding
  governance,
- adopt the Phase 4ab recommendations as binding governance,
- adopt the Phase 4ag M0 mechanism-admissibility gate as binding
  governance,
- broaden Phase 4ac results beyond data / integrity evidence,
- broaden Phase 4ad Rules A / B / C beyond prospective analysis-
  time scope,
- broaden Phase 4ae findings beyond descriptive substrate-
  feasibility evidence,
- broaden Phase 4af findings beyond descriptive regime-continuity /
  directional-persistence evidence,
- broaden Phase 4ag recommendations beyond recommendation-only
  status,
- perform a broad documentation refresh,
- modify existing strategy docs, phase gates, technical-debt
  register, runtime docs, implementation code, or live-readiness
  materials except for the narrow `current-project-state.md`
  Phase 4ah paragraph addition,
- commit gitignored / transient files such as
  `.claude/scheduled_tasks.lock`,
  `data/research/`,
  `data/raw/`, or
  `data/normalized/`,
- authorize Phase 4ai,
- authorize Phase 5,
- authorize Phase 4 canonical,
- authorize paper / shadow,
- authorize live-readiness,
- authorize deployment,
- request or create production keys,
- touch MCP, Graphify, `.mcp.json`, or credentials,
- revise any retained verdict,
- change any project lock,
- amend any specialist governance file beyond the narrow
  `current-project-state.md` Phase 4ah paragraph addition.

## Preserved verdicts and locks

Phase 4ah preserved every retained verdict and project lock
verbatim:

- H0 FRAMEWORK ANCHOR
- R3 BASELINE-OF-RECORD
- R1a RETAINED — NON-LEADING
- R1b-narrow RETAINED — NON-LEADING
- R2 FAILED — §11.6
- F1 HARD REJECT
- D1-A MECHANISM PASS / FRAMEWORK FAIL
- 5m thread CLOSED operationally
- V2 HARD REJECT — terminal for V2 first-spec
- G1 HARD REJECT — terminal for G1 first-spec
- C1 HARD REJECT — terminal for C1 first-spec
- §11.6 HIGH cost = 8 bps per side
- §1.7.3 0.25% / 2× / one-position / mark-price stops
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4z recommendations remain recommendations only
- Phase 4aa admissibility framework remains recommendation only
- Phase 4ab recommendations remain recommendations only
- Phase 4ac results remain data / integrity evidence only
- Phase 4ad Rules A / B / C remain prospective analysis-time scope
- Phase 4ae findings remain descriptive substrate-feasibility
  evidence only
- Phase 4af findings remain descriptive regime-continuity /
  directional-persistence evidence only
- Phase 4ag recommendations remain recommendations only

## Recommendation from Phase 4ah

Primary: merge Phase 4ah into main, then remain paused unless the
operator separately authorizes a future Phase 4ai single-position
cross-sectional trend feasibility analysis.

Conditional secondary (only if operator separately authorizes):
future analysis-and-docs Phase 4ai using the fixed five-symbol
core universe under Phase 4ad Rule B1 scope, with predeclared
ranking descriptors (primarily families 7.A and 7.C from the
memo), predeclared rebalance frequency, predeclared rank-quality
filter, and predeclared falsification criteria. Phase 4ai must
not name a strategy candidate, must not write a strategy spec,
must not draft a backtest plan, and must not authorize successor
phases.

Acceptable alternative: future docs-only M0 governance
reconciliation phase, if the operator wishes to formalize
admissibility gates before any analysis runs.

NOT recommended at this boundary: future derivatives-context
feasibility memo (higher D1-A rescue risk than the cross-sectional
lane), future microstructure data-admissibility memo (heavy data
burden; low expected information gain at this boundary), fresh-
hypothesis discovery memo (premature relative to Phase 4m / 4t /
4z gates).

FORBIDDEN: paper / shadow / live / exchange-write / production
keys / authenticated APIs / private endpoints / user stream /
WebSocket / MCP / Graphify / `.mcp.json` / credentials / strategy-
spec / backtest / old-strategy alt-symbol rerun / R3 / R2 / F1 /
D1-A / V2 / G1 / C1 rescue / multi-position portfolio trading.

## Successor authorization status

Phase 4ah did **NOT** authorize Phase 4ai.

Phase 4ai / Phase 5 / Phase 4 canonical / any successor phase
remains unauthorized.

Recommended state remains paused unless the operator separately
authorizes a future phase.

## Working tree / git status evidence

At Phase 4ah commit time:

- Working tree contained only the two new Phase 4ah implementation-
  report Markdown files and the narrow `current-project-state.md`
  Phase 4ah paragraph addition.
- Untracked / ignored transients (`.claude/scheduled_tasks.lock`,
  `data/research/`) were not committed.
- Branch: `phase-4ah/single-position-cross-sectional-trend-feasibility`.
- Base main SHA: `fa72870ff38e024e80d2d2987d1820bfa1b48c9c`.
