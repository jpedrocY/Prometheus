# Phase 4ai Closeout — Single-Position Cross-Sectional Trend Feasibility Analysis

## Phase identity

- Phase title: Single-Position Cross-Sectional Trend Feasibility Analysis
- Phase status: analysis-and-docs only
- Phase branch: `phase-4ai/single-position-cross-sectional-trend-analysis`
- Base main SHA: `5384589aff24d2d1e0634617deb57385041a7979`

## Files created

```text
scripts/phase4ai_single_position_cross_sectional_trend.py
docs/00-meta/implementation-reports/2026-05-04_phase-4ai_single-position-cross-sectional-trend-analysis.md
docs/00-meta/implementation-reports/2026-05-04_phase-4ai_closeout.md
```

## Files updated narrowly

```text
docs/00-meta/current-project-state.md   (Phase 4ai paragraph added; prior phase preserved)
```

## Local analysis outputs (gitignored; NOT committed)

```text
data/research/phase4ai/run_metadata.json
data/research/phase4ai/verdict.json
data/research/phase4ai/tables/
    omitted_datasets.csv
    verdict_summary.csv
    15m__alignment.csv
    15m__concentration.csv
    15m__cost_adjusted_movement.csv
    15m__coverage.csv
    15m__crash_exposure.csv
    15m__forward_behavior.csv
    15m__persistence_turnover.csv
    15m__rank_distribution.csv
    15m__rank_ic.csv
    30m__alignment.csv
    30m__concentration.csv
    30m__cost_adjusted_movement.csv
    30m__coverage.csv
    30m__crash_exposure.csv
    30m__forward_behavior.csv
    30m__persistence_turnover.csv
    30m__rank_distribution.csv
    30m__rank_ic.csv
    1h__alignment.csv
    1h__concentration.csv
    1h__cost_adjusted_movement.csv
    1h__coverage.csv
    1h__crash_exposure.csv
    1h__forward_behavior.csv
    1h__persistence_turnover.csv
    1h__rank_distribution.csv
    1h__rank_ic.csv
    4h__alignment.csv
    4h__concentration.csv
    4h__cost_adjusted_movement.csv
    4h__coverage.csv
    4h__crash_exposure.csv
    4h__forward_behavior.csv
    4h__persistence_turnover.csv
    4h__rank_distribution.csv
    4h__rank_ic.csv
```

Local outputs reside under `data/research/phase4ai/`. The directory
is gitignored. No analysis output files were committed.

## Phase 4ai summary

Phase 4ai computed predeclared descriptive single-position
cross-sectional trend / relative-strength feasibility metrics for
the fixed five-symbol Phase 4ac core universe (`BTCUSDT`,
`ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`) at intervals 15m / 30m /
1h / 4h under Phase 4ad Rule B1 common post-gap scope
(`2022-04-03 00:00 UTC` through `2026-04-30 23:59:59 UTC`).

The analysis script computed per-interval ranking timestamps with no
omitted datasets and zero alignment dropouts due to missing bars:

| Interval | n_aligned | n_ranking_timestamps | NO_SYMBOL fraction |
| -------- | --------- | -------------------- | ------------------- |
| 15m      | 140 064   | 139 007              | 0.555               |
| 30m      | 70 032    | 69 455               | 0.553               |
| 1h       | 35 736    | 35 399               | 0.549               |
| 4h       | 8 754     | 8 597                | 0.545               |

The predeclared composite primary score
(0.7 × multi-horizon relative-return + 0.3 × vol-adjusted
relative-strength) and the predeclared rank-quality filter
(top-score ≥ 0.60; top-second gap ≥ 0.05; top-symbol's raw 24h and
72h returns both > 0) were applied verbatim.

Headline forward-behavior findings on the four primary evaluation
cells `(1h, 24h)`, `(1h, 72h)`, `(4h, 24h)`, `(4h, 72h)`:

- `frac_selected > median` is **0.498 / 0.484 / 0.492 / 0.490** —
  below random (0.50) in every primary cell.
- Median `selected − median` spread is
  **-1.0 / -16.6 / -3.3 / -10.3 bps** — non-positive in every
  primary cell.
- Spearman IC median is **0.0 in every cell**; mean IC ranges
  -0.020 to +0.007.
- `frac_directional_alignment` (top-score symbol = top-forward
  symbol) is ~ 0.21–0.23 versus a random baseline of 0.20 for
  five symbols.
- Selected-symbol crash exposure is **slightly worse** than top-
  ranked or median-ranked at every horizon.

The predeclared falsification verdict is:

```text
Verdict: NOT_SUPPORTED
```

All three primary falsification criteria triggered simultaneously
across all four primary cells; zero cells passed any conditional-
supported criterion.

## External research availability

External web / literature research was not used during Phase 4ai
itself; the literature context was already recorded by Phase 4ah
(merged `5384589`). Phase 4ai is an analysis-and-docs phase whose
descriptive metrics stand on their own; no fresh literature search
was needed to apply the predeclared falsification criteria.

## Boundary confirmations

Phase 4ai did **NOT**:

- modify any source code under `src/prometheus/`,
- modify any test,
- modify any existing script,
- rerun Phase 4ac, Phase 4ae, Phase 4af, Phase 4ag, or Phase 4ah,
- acquire data,
- download data,
- call APIs,
- call exchange data endpoints,
- consult `data.binance.vision`,
- use authenticated APIs,
- use private endpoints,
- use public endpoints in code,
- use user stream / WebSocket / listenKey,
- enable network I/O from the analysis script,
- modify raw data,
- modify normalized data,
- patch / forward-fill / interpolate / impute / synthesize /
  regenerate / replace data,
- create or modify any manifest,
- flip any Phase 4ac `research_eligible` flag,
- create v003 or any other dataset version,
- run any backtest,
- run any strategy diagnostic,
- rerun Q1–Q7,
- compute strategy PnL,
- compute entry / exit returns,
- create a cumulative equity curve or trade ledger,
- optimize any parameter,
- select thresholds or symbols **after** seeing results,
- create a new strategy candidate,
- name a strategy candidate,
- create a fresh-hypothesis discovery memo,
- create a hypothesis-spec memo,
- create a strategy-spec memo,
- create a backtest-plan memo,
- implement or rescue R3 / R2 / F1 / D1-A / V2 / G1 / C1,
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime /
  G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid,
- propose old-strategy alt-symbol reruns,
- propose multi-position portfolio trading,
- silently reduce cross-sectional ranking into V2 / G1 / C1-style
  single-symbol breakout continuation,
- use old strategy entry / exit rules as ranking descriptors,
- use funding as a directional trigger,
- adopt the Phase 4z recommendations as binding governance,
- adopt the Phase 4aa admissibility framework as binding governance,
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
- broaden Phase 4ah recommendations beyond recommendation-only
  status,
- perform a broad documentation refresh,
- modify existing strategy docs, phase gates, technical-debt
  register, runtime docs, implementation code, or live-readiness
  materials except for the narrow `current-project-state.md`
  Phase 4ai paragraph addition,
- commit gitignored / transient files (`.claude/scheduled_tasks.lock`,
  `data/research/`, `data/raw/`, `data/normalized/`),
- authorize Phase 4aj,
- authorize Phase 5,
- authorize Phase 4 canonical,
- authorize paper / shadow,
- authorize live-readiness,
- authorize deployment,
- request or create production keys,
- touch MCP, Graphify, `.mcp.json`, or credentials,
- revise any retained verdict,
- change any project lock.

## Quality gates

```text
ruff check scripts/phase4ai_single_position_cross_sectional_trend.py   PASS
python -m compileall scripts/phase4ai_single_position_cross_sectional_trend.py   PASS
ruff check . (whole repo)                                                PASS
```

## Preserved verdicts and locks

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
- Phase 4ah recommendations remain recommendations only
- Phase 4ai findings remain descriptive cross-sectional feasibility
  evidence only

## Recommendation from Phase 4ai

Primary: **merge Phase 4ai into main, then remain paused**.

The cross-sectional trend / relative-strength symbol-selection lane
under the Phase 4ah / Phase 4ai predeclared descriptors did not
produce a descriptive forward edge on the five-symbol Phase 4ac core
universe under Phase 4ad Rule B1. Verdict: `NOT_SUPPORTED`.

NOT recommended at this boundary: future docs-only fresh-hypothesis
discussion (Phase 4ai evidence does not support proceeding); future
docs-only derivatives-context feasibility memo (D1-A rescue risk;
the cross-sectional null does not strengthen that lane); future
microstructure data-admissibility memo (heavy data burden; not
strengthened by Phase 4ai).

Acceptable alternative if the operator wishes to formalize
admissibility governance: future docs-only M0 governance
reconciliation phase reconciling Phase 4ag M0 with Phase 4z,
Phase 4m, and Phase 4t. Phase 4ai does not authorize such a phase.

FORBIDDEN: paper / shadow / live / exchange-write / production
keys / authenticated APIs / private endpoints / user stream /
WebSocket / MCP / Graphify / `.mcp.json` / credentials / strategy
spec / backtest / old-strategy alt-symbol rerun / R3 / R2 / F1 /
D1-A / V2 / G1 / C1 rescue / multi-position portfolio trading /
silent reduction to V2-G1-C1 breakout under a ranking wrapper.

## Successor authorization status

Phase 4ai did **NOT** authorize Phase 4aj.

Phase 4aj / Phase 5 / Phase 4 canonical / any successor phase
remains unauthorized.

Recommended state remains paused unless the operator separately
authorizes a future phase.

## Working tree / git status evidence

At Phase 4ai commit time:

- Working tree contained the new analysis script, the two new
  Phase 4ai implementation-report Markdown files, and the narrow
  `current-project-state.md` Phase 4ai paragraph addition.
- Untracked / ignored transients (`.claude/scheduled_tasks.lock`,
  `data/research/`) were not committed.
- Branch: `phase-4ai/single-position-cross-sectional-trend-analysis`.
- Base main SHA: `5384589aff24d2d1e0634617deb57385041a7979`.
