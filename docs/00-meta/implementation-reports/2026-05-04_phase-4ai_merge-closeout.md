# Phase 4ai Merge Closeout

## Merge identity

- Phase: 4ai — Single-Position Cross-Sectional Trend Feasibility Analysis
- Branch merged: `phase-4ai/single-position-cross-sectional-trend-analysis`
- Merge target: `main`
- Branch tip SHA before merge: `3ad3fba238d85bc18e1df03d3c67117a4f968713`
- Main SHA before merge: `5384589aff24d2d1e0634617deb57385041a7979`

## Files merged from branch

```text
scripts/phase4ai_single_position_cross_sectional_trend.py   (new)
docs/00-meta/implementation-reports/2026-05-04_phase-4ai_single-position-cross-sectional-trend-analysis.md   (new)
docs/00-meta/implementation-reports/2026-05-04_phase-4ai_closeout.md   (new)
docs/00-meta/current-project-state.md   (Phase 4ai paragraph added)
```

## Files added at merge time

```text
docs/00-meta/implementation-reports/2026-05-04_phase-4ai_merge-closeout.md   (this file)
```

## Quality gates at merge

```text
ruff check scripts/phase4ai_single_position_cross_sectional_trend.py   PASS
python -m compileall scripts/phase4ai_single_position_cross_sectional_trend.py   PASS
ruff check . (whole repo)                                                PASS
```

## Phase 4ai verdict preserved

```text
Verdict: NOT_SUPPORTED
```

All three primary falsification criteria triggered simultaneously across all four
primary evaluation cells `(1h, 24h)`, `(1h, 72h)`, `(4h, 24h)`, `(4h, 72h)`.
Zero cells passed any conditional-supported criterion.

## Successor authorization status

Phase 4ai did NOT authorize Phase 4aj.

Phase 4aj / Phase 5 / Phase 4 canonical / any successor phase remains unauthorized.

Recommended state remains paused unless the operator separately authorizes a future phase.

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
- Phase 4ae findings remain descriptive substrate-feasibility evidence only
- Phase 4af findings remain descriptive regime-continuity / directional-persistence evidence only
- Phase 4ag recommendations remain recommendations only
- Phase 4ah recommendations remain recommendations only
- Phase 4ai findings remain descriptive cross-sectional feasibility evidence only
