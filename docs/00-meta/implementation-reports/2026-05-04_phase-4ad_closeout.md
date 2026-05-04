# Phase 4ad Closeout

## Summary

Phase 4ad authored the **Alt-Symbol Gap-Governance and Scope-Revision Memo** (docs-only) on branch `phase-4ad/alt-symbol-gap-governance-scope-revision`. Phase 4ad resolved how future alt-symbol substrate-feasibility work may treat Phase 4ac gap / invalid-window findings before any substrate-feasibility analysis, strategy discovery, backtest, diagnostics, or strategy work is allowed. Phase 4ad defined three Phase 4ad-scope future-use rules: (Rule A) Mark-Price Invalid-Window Exclusion Rule (analogous to Phase 3r §8 precedent; per-window exclusion test for any bar / trade / candidate event / diagnostic window / stop-domain window / analysis window intersecting a known mark-price upstream gap; conclusions labeled "conditional on valid mark-price coverage"); (Rule B) SOL/XRP Early-2022 Kline Gap Scope Rule with three policy options: B1 common post-gap start at 2022-04-03 UTC (recommended default), B2 full-history with invalid-window exclusion, B3 PASS-only subset; (Rule C) PASS-Only Subset Rule for conservative fallback restricted to the 9 Phase 4ac PASS datasets. Phase 4ad recommends merging into main, then remaining paused unless the operator separately authorizes a future Phase 4ae substrate-feasibility analysis memo. **Phase 4ad is text-only.** No data acquired or modified. No manifest created or modified. No backtest run. No diagnostic run. No Q1–Q7 rerun. No substrate-feasibility execution. No strategy candidate / hypothesis-spec / strategy-spec / backtest-plan created. No `src/prometheus/`, tests, or scripts modified. No retained verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update). **No successor phase authorized.** **Phase 4z recommendations remain recommendations only and are NOT adopted as binding governance by Phase 4ad.** **Phase 4aa admissibility framework remains recommendation only and is NOT adopted as binding governance by Phase 4ad.** **Phase 4ab recommendations remain recommendations only and are NOT adopted as binding governance by Phase 4ad.** **Phase 4ac results remain data / integrity evidence only and are NOT broadened beyond data / integrity evidence by Phase 4ad — except that Phase 4ad explicitly defines Rules A / B / C as future-use scope rules for prospective analysis-time use of Phase 4ac data only. Phase 4ad rules do NOT modify Phase 4ac manifests, do NOT flip eligibility flags, and do NOT revise prior verdicts or locks.**

## Phase 4ad title

**Phase 4ad — Alt-Symbol Gap-Governance and Scope-Revision Memo** (docs-only).

## Branch

`phase-4ad/alt-symbol-gap-governance-scope-revision`

## Base main SHA

`3478d05d97c43ee9ef885ae3defa4d1559189605`

## Files created

```text
docs/00-meta/implementation-reports/2026-05-04_phase-4ad_alt-symbol-gap-governance-scope-revision.md  (new; main memo)
docs/00-meta/implementation-reports/2026-05-04_phase-4ad_closeout.md                                  (new; this file)
```

## Files updated

```text
docs/00-meta/current-project-state.md  (narrow Phase 4ad paragraph addition; no broad refresh)
```

## Docs-only status

Phase 4ad is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. The two memo files added under `docs/00-meta/implementation-reports/` and the narrow `docs/00-meta/current-project-state.md` update are the only repository changes.

## No code / tests / scripts / data / manifests modified

Phase 4ad did NOT:

- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`, `scripts/phase4ac_alt_symbol_acquisition.py`);
- create any new script;
- modify `data/raw/`, `data/normalized/`, or `data/manifests/`;
- create any new manifest;
- modify any existing manifest (Phase 4ac manifests inspected read-only for documentation/planning context only);
- create v003 or any other dataset version;
- modify any specialist governance file (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist document beyond the narrow `current-project-state.md` update).

## No data acquisition / download / API calls / endpoint calls

Phase 4ad did NOT:

- acquire any data;
- download any data;
- call `data.binance.vision`;
- call any Binance API;
- call any authenticated REST endpoint;
- call any private endpoint;
- call any public endpoint from code;
- consult any user stream / WebSocket / listenKey lifecycle;
- use any credentials or `.env`;
- enable any network I/O.

## No backtests / diagnostics / Q1–Q7 rerun

Phase 4ad did NOT:

- run any backtest (no Phase 2 / 3 / 4l / 4r / 4x rerun; no new backtest);
- run any diagnostic (no Q1–Q7 rerun; no new diagnostic phase);
- execute any committed acquisition / backtest / analysis / orchestrator script.

## No substrate-feasibility execution

Phase 4ad did NOT:

- compute cost-to-volatility ratios;
- compute ATR / median range distributions;
- compute expansion-event frequencies;
- compute trend-regime frequencies;
- compute wick / stop-pathology descriptive measures;
- compute funding-rate distributions;
- compute volume / notional turnover proxies;
- generate common-overlap coverage tables;
- generate event-count sufficiency summaries;
- generate per-symbol gap / exclusion tabulation;
- generate cross-symbol descriptive comparisons;
- perform any other substrate-feasibility metric computation.

These computations would belong only to a future separately authorized Phase 4ae-equivalent substrate-feasibility analysis memo (NOT authorized by Phase 4ad).

## No strategy created

Phase 4ad did NOT:

- create a new strategy candidate;
- name a new strategy;
- create a fresh-hypothesis discovery memo;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid;
- create any "rescue" or "improvement" of R3 / R2 / F1 / D1-A / V2 / G1 / C1.

## No prior verdict revised

Phase 4ad preserved every retained verdict verbatim:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains CLOSED operationally.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

No retained verdicts were revised.

## No locks changed

Phase 4ad preserved every project lock verbatim:

- §11.6 HIGH cost = 8 bps per side.
- §1.7.3 project-level locks: 0.25% risk; 2× leverage; one position max; mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.
- Phase 4j §11 metrics OI-subset partial-eligibility rule (preserved; not invoked by Phase 4ad / Phase 4ae scope).
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy-spec.
- Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy-spec.
- Phase 4w C1 backtest-plan methodology.

No project locks changed.

## Phase 4z recommendations not adopted as governance

Phase 4z recommendations (32-item proposed admissibility framework, design-family-distance matrix, M0 theoretical-admissibility gate concept, edge-rate viability gate concept, future memo template additions) remain recommendations only. **Phase 4ad did NOT adopt them as binding governance.**

## Phase 4aa admissibility framework not adopted as governance

Phase 4aa admissibility framework (eight pre-backtest gates) remains recommendation only. **Phase 4ad did NOT adopt it as binding governance.**

## Phase 4ab recommendations not adopted as governance

Phase 4ab recommendations (core acquisition-planning set; data-family requirements / optionality; date-range policy; manifest-field requirements; integrity gates; feasibility-check targets) remain recommendations only. **Phase 4ad did NOT adopt them as binding governance.**

## Phase 4ac results remain data / integrity evidence (with Phase 4ad future-use scope rules)

Phase 4ac results remain data / integrity evidence only. **Phase 4ad does NOT broaden Phase 4ac results into binding cross-project governance.** Phase 4ad does explicitly define **Rules A / B / C** as future-use scope rules for **prospective analysis-time use of Phase 4ac data only**. The rules:

- apply only to future Phase 4ae-equivalent substrate-feasibility analysis (NOT authorized by Phase 4ad);
- do NOT modify Phase 4ac manifests;
- do NOT flip any `research_eligible` flag;
- do NOT revise any retained verdict;
- do NOT change any project lock;
- do NOT amend any specialist governance file;
- do NOT broaden Phase 4ac results into binding cross-project governance.

## Recommendation from Phase 4ad memo

```text
Primary recommendation:
Merge Phase 4ad into main, then remain paused unless the operator separately
authorizes a Phase 4ae substrate-feasibility analysis memo.

For any future Phase 4ae cross-symbol substrate-feasibility analysis, use the
Phase 4ad SOL/XRP Early-2022 Kline Gap Scope Rule with Policy B1 common
post-gap start as the default.

Use the Phase 4ad Mark-Price Invalid-Window Exclusion Rule for any mark-
price-dependent analysis.

Do not backtest yet.
Do not create a strategy yet.
Do not rescue prior strategies.
Do not expand market type yet.
```

Conditional secondary acceptable: Option A — remain paused without merging Phase 4ad (always procedurally valid).

NOT recommended: data re-acquisition (premature; bounded gaps handled by Rules A / B); direct strategy discovery (substrate evidence still being established).

FORBIDDEN: old-strategy alt-symbol rerun; backtest / diagnostics / Q1–Q7 rerun at this boundary; paper / shadow / live / exchange-write.

## No successor phase authorized

Phase 4ad does NOT authorize:

- Phase 4ae (any kind);
- Phase 5;
- Phase 4 canonical;
- any other named successor phase.

The next step is operator-driven: the operator decides whether to remain paused (with or without merging Phase 4ad) or authorize Phase 4ae (or some other phase).

## Working tree / git status evidence

Working tree at memo creation time:

```text
On branch phase-4ad/alt-symbol-gap-governance-scope-revision
Untracked files (gitignored transients only; not committed):
  .claude/scheduled_tasks.lock
  data/research/        (gitignored)
  data/raw/binance_usdm/    (gitignored)
  data/normalized/      (gitignored)
nothing added to commit but untracked files present
```

Repository state at base:

```text
main / origin/main: 3478d05d97c43ee9ef885ae3defa4d1559189605 (unchanged)
Phase 4ac merge commit:                3478d05d97c43ee9ef885ae3defa4d1559189605
Phase 4ac acquisition commit:          e3018a9c085deab04432f3df039933bc487d340b
Phase 4ad branch:                      phase-4ad/alt-symbol-gap-governance-scope-revision (this branch)
```

Quality gates were not re-run for Phase 4ad because Phase 4ad is text-only and does not modify any code, test, script, or quality-gate input. Last-known clean state: ruff PASS; mypy strict 0 issues across 82 source files (verified during Phase 4ac).

## Forbidden-work confirmation

Phase 4ad did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / impute / synthesize / regenerate / replace any data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- amend the Phase 4m 18-requirement validity gate;
- amend the Phase 4t 10-dimension scoring matrix;
- amend the Phase 4u opportunity-rate principle;
- amend the Phase 4w negative-baseline / PBO / DSR / CSCV methodology;
- amend the Phase 4aa admissibility framework;
- amend the Phase 4ab data-requirements / feasibility framework;
- modify any specialist governance file beyond the narrow `docs/00-meta/current-project-state.md` update;
- adopt any Phase 4z recommendation as binding governance;
- adopt the Phase 4aa admissibility framework as binding governance;
- adopt any Phase 4ab recommendation as binding governance;
- broaden Phase 4ac results beyond data / integrity evidence;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4ae / Phase 5 / Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- merge Phase 4ad to main (the branch is preserved; merge would require separate operator instruction).

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal; preserved)
G1                  : HARD REJECT (Phase 4r terminal; preserved)
C1                  : HARD REJECT (Phase 4x terminal; preserved)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : project-level locks preserved
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility rule (preserved;
                              not invoked by 4ad / future 4ae scope)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4p                    : G1 strategy spec (preserved)
Phase 4q                    : G1 backtest-plan methodology (preserved)
Phase 4v                    : C1 strategy spec (preserved)
Phase 4w                    : C1 backtest-plan methodology (preserved)
Phase 4z recommendations    : remain recommendations only; NOT adopted by 4ad
Phase 4aa admissibility framework : remain recommendation only; NOT adopted by 4ad
Phase 4ab recommendations   : remain recommendations only; NOT adopted by 4ad
Phase 4ac results           : data / integrity evidence only;
                              Phase 4ad future-use rules apply prospectively
                              to analysis-time use of Phase 4ac data only;
                              Phase 4ac manifests unchanged
Phase 4ad                   : Alt-symbol gap-governance and scope-revision memo
                              (this phase; new; docs-only; feature-branch only;
                              not merged)
Phase 4ad Rule A            : Mark-Price Invalid-Window Exclusion Rule (analogous
                              to Phase 3r §8 precedent; future-use only)
Phase 4ad Rule B            : SOL/XRP Early-2022 Kline Gap Scope Rule
                              (B1 / B2 / B3 policies; default B1; future-use only)
Phase 4ad Rule C            : PASS-Only Subset Rule (conservative fallback;
                              future-use only)
Recommended state           : remain paused (primary; Option B merge then stop);
                              docs-only Phase 4ae substrate-feasibility analysis
                              memo (conditional next; not authorized by 4ad)
```

## Next authorization status

```text
Phase 4ae / Phase 5 / successor    : NOT authorized
Phase 4 (canonical)                : NOT authorized
Paper / shadow                     : NOT authorized
Live-readiness                     : NOT authorized
Deployment                         : NOT authorized
Production-key creation            : NOT authorized
Authenticated REST                 : NOT authorized
Private endpoints                  : NOT authorized
Public endpoint calls in code      : NOT authorized
User stream / WebSocket            : NOT authorized
Exchange-write capability          : NOT authorized
MCP / Graphify                     : NOT authorized
.mcp.json / credentials            : NOT authorized
C1 / V2 / G1 / R2 / F1 / D1-A rescue : NOT authorized; FORBIDDEN
C1-prime / V2-prime / G1-prime /
  R2-prime / F1-prime / D1-A-prime  : NOT authorized; FORBIDDEN
Old-strategy alt-symbol re-run     : NOT authorized; FORBIDDEN (retrospective rescue)
Adoption of Phase 4z recommendations
  as binding governance            : NOT authorized
Adoption of Phase 4aa admissibility
  framework as binding governance  : NOT authorized
Adoption of Phase 4ab recommendations
  as binding governance            : NOT authorized
Broadening of Phase 4ac results
  beyond data / integrity evidence : NOT authorized; Phase 4ad Rules A / B / C
                                     are narrowly-scoped future-use rules only
Alt-symbol substrate-feasibility
  analysis memo (Phase 4ae)        : NOT authorized; conditional next
Alt-symbol PASS-only feasibility
  analysis memo (Phase 4ae-narrow) : NOT authorized; conditional alternative
Alt-symbol data re-acquisition     : NOT authorized; not recommended now
Alt-symbol fresh-hypothesis memo   : NOT authorized
Alt-symbol strategy-spec memo      : NOT authorized
Alt-symbol backtest-plan memo      : NOT authorized
Alt-symbol backtest execution      : NOT authorized
Spot / COIN-M / options / cross-
  venue expansion                  : NOT authorized; not recommended
Phase 4ad merge to main            : NOT authorized; preserved on
                                     feature branch unless separately
                                     instructed
```

The next step is operator-driven: the operator decides whether to remain paused, merge Phase 4ad to main and authorize a future docs-only Phase 4ae substrate-feasibility analysis memo (or PASS-only narrow alternative), or take some other action. Until then, the project remains at the post-Phase-4ac merge boundary on `main` with Phase 4ad preserved on its feature branch.

---

**Phase 4ad is text-only. main remains unchanged at `3478d05d97c43ee9ef885ae3defa4d1559189605`. Phase 4ad defines Phase 4ad-scope future-use rules (Rule A mark-price invalid-window exclusion; Rule B SOL/XRP early-2022 kline gap scope policy with B1 / B2 / B3; Rule C PASS-only subset) that apply prospectively to future Phase 4ae-equivalent substrate-feasibility analysis only. Phase 4ad does NOT modify Phase 4ac manifests, does NOT flip any `research_eligible` flag, does NOT revise any retained verdict, does NOT change any project lock, does NOT broaden Phase 4ac results into binding cross-project governance. Phase 4z, Phase 4aa, Phase 4ab recommendations all remain recommendations only — not binding governance. C1 / V2 / G1 first-specs remain terminally HARD REJECTED. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. Recommended state: remain paused (primary; Option B merge Phase 4ad then stop); Phase 4ae substrate-feasibility analysis memo (conditional next; not authorized by Phase 4ad). No next phase authorized.**
