# Phase 4ag Closeout — Research-Program Pivot and Mechanism-Source Triage Memo

## Phase identity

- Phase title: Research-Program Pivot and Mechanism-Source Triage Memo
- Phase status: docs-only
- Phase branch: `phase-4ag/research-program-pivot-mechanism-source-triage`
- Base main SHA: `25959dd5239a1c3af27e842826eb49589cb1da4d`

## Files created

```text
docs/00-meta/implementation-reports/2026-05-04_phase-4ag_research-program-pivot-mechanism-source-triage.md
docs/00-meta/implementation-reports/2026-05-04_phase-4ag_closeout.md
```

## Files updated narrowly

```text
docs/00-meta/current-project-state.md   (Phase 4ag paragraph added; prior phase preserved)
```

## Phase 4ag summary

Phase 4ag evaluated whether Prometheus should continue investigating
price-only single-symbol directional continuation, or pivot toward a
different mechanism-source family, given the cumulative evidence
through Phase 4af.

The Phase 4ag triage matrix evaluated seven candidate mechanism-source
families:

1. Continue price-only single-symbol continuation (NOT_RECOMMENDED).
2. Cross-sectional trend / relative-strength / symbol-selection
   (ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY — strongest non-paused
   option).
3. Market-state / regime-transition momentum (CONDITIONAL_ONLY).
4. Derivatives positioning (context only) (CONDITIONAL_ONLY).
5. Microstructure / order-flow (NOT_RECOMMENDED).
6. Mark-price stop-domain / execution realism (NOT_RECOMMENDED now).
7. Remain paused (REMAIN_PAUSED — primary recommendation).

Phase 4ag also recorded a proposed ten-clause M0 mechanism-
admissibility gate as a **recommendation only**, not as binding
governance. Adoption of the M0 gate (and reconciliation with the
Phase 4z proposed admissibility framework, the Phase 4m 18-requirement
validity gate, and the Phase 4t 10-dimension scoring matrix) is
deferred to a possible separately-authorized future docs-only phase.

Phase 4ag's primary recommendation is **remain paused**.

Phase 4ag's conditional secondary recommendation is a future docs-only
Phase 4ah single-position cross-sectional trend / relative-strength
feasibility memo, only if the operator separately authorizes one.

## External research availability

External web / literature research was **available** during Phase 4ag.
Two narrow search queries were run:

- "cross-sectional momentum cryptocurrency academic study 2024
  transaction costs"
- "crypto perpetual futures funding rate factor strategy academic
  2024"

Search results were used to record verbatim references in the
memo's §3 External Research / Web Context section. References
were recorded as found (titles and identifiers visible in the
search results); no claims were synthesized beyond what the search
results stated. No fabricated citations were introduced.

Phase 4ag did **not** broadly canvass the literature; the searches
were intentionally narrow and scoped to mechanism-source triage.

## Boundary confirmations

Phase 4ag did **NOT**:

- modify or create any source code,
- modify or create any test,
- modify or create any analysis script,
- run any analysis script,
- rerun Phase 4ac, Phase 4ae, or Phase 4af,
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
- name a new strategy candidate,
- create a fresh-hypothesis discovery memo,
- create a hypothesis-spec memo,
- create a strategy-spec memo,
- create a backtest-plan memo,
- implement or rescue R3 / R2 / F1 / D1-A / V2 / G1 / C1,
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime /
  G1-prime / C1-prime / V1-D1 / F1-D1 or any cross-strategy hybrid,
- propose old-strategy alt-symbol reruns,
- adopt the Phase 4z recommendations as binding governance,
- adopt the Phase 4aa admissibility framework as binding
  governance,
- adopt the Phase 4ab recommendations as binding governance,
- broaden Phase 4ac results beyond data / integrity evidence,
- broaden Phase 4ad Rules A / B / C beyond prospective analysis-
  time scope,
- broaden Phase 4ae findings beyond descriptive substrate-
  feasibility evidence,
- broaden Phase 4af findings beyond descriptive regime-continuity /
  directional-persistence evidence,
- adopt the Phase 4ag M0 mechanism-admissibility gate as binding
  governance,
- perform a broad documentation refresh,
- modify existing strategy docs, phase gates, technical-debt
  register, runtime docs, implementation code, or live-readiness
  materials except for the narrow `current-project-state.md`
  Phase 4ag paragraph addition,
- authorize Phase 4ah,
- authorize Phase 5,
- authorize Phase 4 canonical,
- authorize paper / shadow,
- authorize live-readiness,
- authorize deployment,
- request or create production keys,
- touch MCP, Graphify, `.mcp.json`, or credentials,
- commit gitignored / transient files such as
  `.claude/scheduled_tasks.lock`,
  `data/research/`,
  `data/raw/`, or
  `data/normalized/`,
- revise any retained verdict,
- change any project lock,
- amend any specialist governance file beyond the narrow
  `current-project-state.md` Phase 4ag paragraph addition.

## Preserved verdicts and locks

Phase 4ag preserved every retained verdict and project lock
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

## Recommendation from Phase 4ag

Primary: remain paused.

Conditional secondary (only if operator separately authorizes):
future docs-only Phase 4ah single-position cross-sectional trend /
relative-strength feasibility memo.

NOT recommended: fresh-hypothesis discovery memo, derivatives-
context memo (Lane B is conditional but higher D1-A rescue risk
than Lane A), microstructure data-admissibility memo, mark-price
stop-domain feasibility memo (unless operator explicitly chooses
execution-realism research over directional-edge research).

FORBIDDEN: paper / shadow / live / exchange-write / production
keys / authenticated APIs / private endpoints / user stream /
WebSocket / MCP / Graphify / `.mcp.json` / credentials / strategy-
spec / backtest / old-strategy alt-symbol rerun / R3 / R2 / F1 /
D1-A / V2 / G1 / C1 rescue.

## Successor authorization status

Phase 4ag did **NOT** authorize Phase 4ah.

Phase 4ah / Phase 5 / Phase 4 canonical / any successor phase
remains unauthorized.

Recommended state remains paused unless the operator separately
authorizes a future phase.

## Working tree / git status evidence

At Phase 4ag commit time:

- Working tree contained only the two new Phase 4ag implementation-
  report Markdown files and the narrow `current-project-state.md`
  Phase 4ag paragraph addition.
- Untracked / ignored transients (`.claude/scheduled_tasks.lock`,
  `data/research/`) were not committed.
- Branch: `phase-4ag/research-program-pivot-mechanism-source-triage`.
- Base main SHA: `25959dd5239a1c3af27e842826eb49589cb1da4d`.
