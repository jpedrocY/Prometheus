# Phase 4aj Closeout — M0 Governance Reconciliation Memo

## Phase identity

- Phase title: M0 Governance Reconciliation Memo
- Phase status: docs-only
- Phase branch: `phase-4aj/m0-governance-reconciliation`
- Base main SHA: `d8e2f87277a74faff84a142fbc5e523eabbda848`

## Files created

```text
docs/00-meta/implementation-reports/2026-05-04_phase-4aj_m0-governance-reconciliation.md
docs/00-meta/implementation-reports/2026-05-04_phase-4aj_closeout.md
```

## Files updated narrowly

```text
docs/00-meta/current-project-state.md   (Phase 4aj paragraph added; prior phase content preserved)
```

## Phase 4aj summary

Phase 4aj reconciled the proposed Phase 4ag ten-clause M0
mechanism-admissibility gate with the existing Prometheus
governance record — Phase 4z (post-rejection research-process
redesign), Phase 4m (post-V2 strategy-research consolidation;
source of the 18-requirement fresh-hypothesis validity gate), and
Phase 4t (post-G1 fresh-hypothesis discovery; source of the
10-dimension candidate scoring matrix) — after Phase 4ai returned
a predeclared `NOT_SUPPORTED` verdict on the cross-sectional trend /
relative-strength symbol-selection feasibility lane.

Phase 4aj concluded:

- Phase 4ag's ten-clause M0 is a *strict subset* of the Phase 4z
  proposed admissibility framework: it is one upstream
  operationalized fragment, not the whole proposal.
- M0 does not conflict with the Phase 4m 18-requirement validity
  gate or the Phase 4t 10-dimension scoring matrix; it is an
  *additional pre-discovery admissibility screen* that complements
  both.
- The central C1 lesson — opportunity-rate viability ≠ edge-rate
  viability — was not explicit in Phase 4ag M0 and is not explicit
  in the Phase 4m gate. The Phase 4ai null reinforced this lesson
  at the cross-sectional layer.
- A revised twelve-clause M0 (Phase 4aj §8) was proposed that adds
  a non-price-only / structurally-distinct source requirement
  (clause 2), an explicit predicted-Δ_R baseline-superiority
  theory clause (clause 3), an edge-rate plausibility clause
  separate from opportunity-rate (clause 7), and a post-null
  cooldown reference (clause 12).
- A post-null cooldown rule (Phase 4aj §9) was proposed: a
  feasibility family that returns `NOT_SUPPORTED` may not be
  re-opened through descriptor / threshold / symbol / interval /
  composite-weight / rebalance-frequency / forward-horizon tweaks
  unless a future memo identifies a materially new mechanism
  source from external theory or external evidence.
- Phase 4aj's primary recommendation is to merge Phase 4aj into
  main and then remain paused. The conditional governance
  recommendation is to authorize a future docs-only Phase 4ak M0
  governance adoption phase only if the operator wants to
  formalize admissibility governance.
- Phase 4aj does **NOT** adopt M0 as binding governance, does
  **NOT** adopt the Phase 4z 32-item framework as binding
  governance, does **NOT** adopt the post-null cooldown rule as
  binding governance, and does **NOT** authorize Phase 4ak.

## Boundary confirmations

Phase 4aj did **NOT**:

- modify any source code under `src/prometheus/`,
- modify any test,
- modify any existing script,
- create any new script,
- create any analysis script,
- run any analysis script,
- rerun Phase 4ac, Phase 4ae, Phase 4af, Phase 4ag, Phase 4ah, or
  Phase 4ai,
- acquire data,
- download data,
- call APIs,
- call exchange data endpoints,
- consult `data.binance.vision`,
- use authenticated APIs,
- use private endpoints,
- use public endpoints in code,
- use user stream / WebSocket / listenKey,
- enable network I/O,
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
- adopt M0 as binding governance,
- adopt Phase 4z recommendations as binding governance,
- adopt the Phase 4aa admissibility framework as binding governance,
- adopt Phase 4ab recommendations as binding governance,
- adopt the Phase 4aj post-null cooldown rule as binding governance,
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
- broaden Phase 4ai findings beyond descriptive cross-sectional
  feasibility evidence,
- perform a broad documentation refresh,
- modify `docs/12-roadmap/phase-gates.md`,
- modify `docs/12-roadmap/technical-debt-register.md`,
- modify `docs/00-meta/ai-coding-handoff.md`,
- modify `docs/00-meta/implementation-ambiguity-log.md`,
- modify any specialist governance file (beyond the narrow
  `current-project-state.md` Phase 4aj paragraph addition),
- commit gitignored / transient files (`.claude/scheduled_tasks.lock`,
  `data/research/`, `data/raw/`, `data/normalized/`),
- authorize Phase 4ak,
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

Phase 4aj is docs-only and does not introduce, modify, or run any
code. No ruff / pytest / mypy execution was performed by Phase 4aj
itself; the project quality-gate state remains as recorded in
Phase 4ai's closeout (whole-repo `ruff check .` PASS at the time
Phase 4ai was merged).

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
- Phase 4aj recommendations remain recommendations only unless
  separately adopted later

## Recommendation from Phase 4aj

Primary: **merge Phase 4aj into main, then remain paused**.

Conditional governance recommendation: if the operator wants
further forward motion, authorize a future docs-only Phase 4ak M0
governance adoption phase that decides whether to adopt the
revised twelve-clause M0 gate (Phase 4aj §8) and the post-null
cooldown rule (Phase 4aj §9) as binding governance.

NOT recommended now:

- a fresh-hypothesis discovery memo,
- a derivatives-context feasibility memo,
- a microstructure data-admissibility memo,
- a return to the cross-sectional lane via descriptor tweaks,
- adoption of the Phase 4z 32-item framework as binding governance.

FORBIDDEN:

- strategy spec / backtest / old-strategy rerun,
- multi-position portfolio trading,
- silent reduction of cross-sectional ranking into V2 / G1 /
  C1-style breakout under a ranking wrapper,
- paper / shadow / live / exchange-write,
- production-key creation / authenticated APIs / private
  endpoints / user stream / WebSocket / MCP / Graphify /
  `.mcp.json` / credentials.

## Successor authorization status

Phase 4aj did **NOT** authorize Phase 4ak.

Phase 4ak / Phase 5 / Phase 4 canonical / any successor phase
remains unauthorized.

Recommended state remains paused unless the operator separately
authorizes a future phase.

## Working tree / git status evidence

At Phase 4aj commit time:

- Working tree contained the two new Phase 4aj implementation-
  report Markdown files and the narrow `current-project-state.md`
  Phase 4aj paragraph addition.
- Untracked / ignored transients (`.claude/scheduled_tasks.lock`,
  `data/research/`) were not committed.
- Branch: `phase-4aj/m0-governance-reconciliation`.
- Base main SHA: `d8e2f87277a74faff84a142fbc5e523eabbda848`.
