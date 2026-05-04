# Phase 4aa Closeout

## Summary

Phase 4aa authored the **Alt-Symbol Market-Selection and Strategy-Admissibility Memo** (docs-only) on branch `phase-4aa/alt-symbol-market-selection-admissibility`. Phase 4aa frames the question of whether future strategy research should remain restricted to BTCUSDT / ETHUSDT or expand to liquid large-cap Binance USDⓈ-M perpetual alt symbols (SOLUSDT / XRPUSDT / ADAUSDT primary candidate set; BNBUSDT / DOGEUSDT / LINKUSDT / AVAXUSDT secondary watchlist). Phase 4aa defines a pre-backtest symbol-admissibility framework with eight gates (A listing/continuity; B public-data availability; C cost-to-volatility; D opportunity-rate; E liquidity/execution-risk; F wick/stop-pathology; G idiosyncratic-risk; H governance-label compatibility) and recommends remain-paused as primary with a future docs-only alt-symbol data-requirements / feasibility memo as conditional secondary (Option B; only if separately authorized). **Phase 4aa is text-only.** No data acquired or modified. No manifest created or modified. No backtest run. No diagnostics run. No strategy candidate named. No implementation code written. No `src/prometheus/`, tests, or scripts modified. No retained verdict revised. No project lock changed. No governance file amended. **No successor phase authorized.** **Phase 4z recommendations remain recommendations only and are NOT adopted as binding governance by Phase 4aa.**

## Phase 4aa title

**Phase 4aa — Alt-Symbol Market-Selection and Strategy-Admissibility Memo** (docs-only research-direction memo).

## Branch

`phase-4aa/alt-symbol-market-selection-admissibility`

## Base main SHA

`6fb0c6c8ab0e634684a80e7b339c9c96f3a56b02`

## Files created

```text
docs/00-meta/implementation-reports/2026-05-04_phase-4aa_alt-symbol-market-selection-admissibility.md  (new; main memo)
docs/00-meta/implementation-reports/2026-05-04_phase-4aa_closeout.md                                   (new; this file)
```

## Files updated

```text
docs/00-meta/current-project-state.md  (narrow Phase 4aa paragraph addition; no broad refresh)
```

## Docs-only status

Phase 4aa is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. The two memo files added under `docs/00-meta/implementation-reports/` and the narrow `docs/00-meta/current-project-state.md` update are the only repository changes.

## No code / tests / scripts / data / manifests modified

Phase 4aa did NOT:

- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
- create any new script;
- modify `data/raw/`, `data/normalized/`, or `data/manifests/`;
- create any new manifest;
- modify any existing manifest;
- create v003 or any other dataset version;
- modify any specialist governance file (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, `docs/03-strategy-research/v1-breakout-strategy-spec.md`, `docs/03-strategy-research/v1-breakout-backtest-plan.md`, `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`, `docs/04-data/data-requirements.md`, or any other specialist document).

## No backtests / diagnostics / data acquisition run

Phase 4aa did NOT:

- run any backtest (no Phase 4l / Phase 4r / Phase 4x rerun; no new backtest script);
- run any diagnostic (no Q1–Q7 rerun; no new diagnostic phase);
- run any acquisition script (no Phase 3q, Phase 4i execution; no new acquisition);
- download any data;
- consult `data.binance.vision`, Binance APIs, authenticated REST, private endpoints, public endpoints in code, user stream, WebSocket, listenKey lifecycle, or any external data source;
- access credentials, `.env`, or any secret;
- enable network I/O of any kind.

## No strategy created

Phase 4aa did NOT:

- create a new strategy candidate;
- name a new strategy;
- create a fresh-hypothesis discovery memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid;
- create any "rescue" or "improvement" of R3 / R2 / F1 / D1-A / V2 / G1 / C1.

## No prior verdict revised

Phase 4aa preserved every retained verdict verbatim:

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

Phase 4aa preserved every project lock verbatim:

- §11.6 HIGH cost = 8 bps per side.
- §1.7.3 project-level locks: 0.25% risk; 2× leverage; one position max; mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.
- Phase 4j §11 metrics OI-subset partial-eligibility rule.
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy-spec.
- Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy-spec.
- Phase 4w C1 backtest-plan methodology.

No project locks changed.

## Phase 4z recommendations not adopted as governance

Phase 4z (merged at `6fb0c6c`) proposed recommendations for any future research-process memo, including a 32-item proposed admissibility framework, design-family-distance matrix, M0 theoretical-admissibility gate concept, edge-rate viability gate concept, and template additions. **Phase 4aa did NOT adopt any of these recommendations as binding governance.** Phase 4z recommendations remain recommendations only. Adoption of any Phase 4z proposal would require a separately authorized governance-update phase, which Phase 4aa does NOT initiate.

## Recommendation from Phase 4aa memo

```text
Primary recommendation:
Proceed next, if operator authorizes, with a docs-only alt-symbol data-requirements
and feasibility memo (Option B).

Do not backtest yet.
Do not acquire data yet unless separately authorized.
Do not rescue prior strategies.
Do not expand market type yet.
Keep research on Binance USDⓈ-M perpetuals for clean attribution.
```

Secondary acceptable: Option A — Remain paused (always procedurally valid).

NOT recommended: direct public data acquisition (Option C; premature); direct ex-ante strategy-family discovery memo (Option D; premature); old-strategy improvement / rescue (Option E; forbidden); spot / options / COIN-M / other venue expansion (Option F; premature).

FORBIDDEN: paper / shadow / live / exchange-write (Option G; phase-gate requirements not met).

## No successor phase authorized

Phase 4aa does NOT authorize:

- Phase 4ab (alt-symbol public data feasibility / acquisition plan; described conceptually but explicitly not authorized);
- Phase 5;
- Phase 4 canonical;
- any other named successor phase.

The next step is operator-driven: the operator decides whether to remain paused (primary) or authorize a docs-only alt-symbol data-requirements / feasibility memo (Option B; conditional secondary).

## Working tree / git status evidence

Working tree at memo creation time:

```text
On branch phase-4aa/alt-symbol-market-selection-admissibility
Untracked files (gitignored transients only; not committed):
  .claude/scheduled_tasks.lock
  data/research/
nothing added to commit but untracked files present
```

Repository state at base:

```text
main / origin/main: 6fb0c6c8ab0e634684a80e7b339c9c96f3a56b02 (unchanged)
Phase 4z merge commit:                 6fb0c6c8ab0e634684a80e7b339c9c96f3a56b02
Phase 4z report commit:                cb426b127c8fce41e00f9c0684f4d4d7269b82d8
Phase 4z closeout commit:              9968f346e00641a02817fc475491e27d6e5efe2e
Phase 4aa branch:                      phase-4aa/alt-symbol-market-selection-admissibility (this branch)
```

Quality gates were not re-run for Phase 4aa because Phase 4aa is text-only and does not modify any code, test, script, or quality-gate input. Last-known clean state: ruff PASS; pytest 785 PASS; mypy strict 0 issues across 82 source files (verified during Phase 4z).

## Forbidden-work confirmation

Phase 4aa did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- amend the Phase 4m 18-requirement validity gate;
- amend the Phase 4t 10-dimension scoring matrix;
- amend the Phase 4u opportunity-rate principle;
- amend the Phase 4w negative-baseline / PBO / DSR / CSCV methodology;
- modify any specialist governance file beyond the narrow `docs/00-meta/current-project-state.md` update;
- adopt any Phase 4z recommendation as binding governance;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4ab / Phase 5 / Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values;
- merge Phase 4aa to main (the branch is preserved; merge would require separate operator instruction).

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
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x / 4y / 4z
                            : all preserved verbatim
Phase 4z recommendations    : remain recommendations only; NOT adopted by 4aa
Phase 4aa                   : Alt-symbol market-selection and admissibility memo
                              (this phase; new; docs-only; feature-branch only;
                              not merged)
Recommended state           : remain paused (primary);
                              docs-only alt-symbol data-requirements / feasibility
                              memo (conditional secondary; not authorized by 4aa)
```

## Next authorization status

```text
Phase 4ab / Phase 5 / successor    : NOT authorized
Phase 4 (canonical)                : NOT authorized
Paper / shadow                     : NOT authorized
Live-readiness                     : NOT authorized
Deployment                         : NOT authorized
Production-key creation            : NOT authorized
Authenticated REST                 : NOT authorized
Private endpoints                  : NOT authorized
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
Alt-symbol data acquisition        : NOT authorized; conditional secondary
                                     in operator decision menu
Alt-symbol fresh-hypothesis memo   : NOT authorized
Alt-symbol strategy-spec memo      : NOT authorized
Alt-symbol backtest-plan memo      : NOT authorized
Alt-symbol backtest execution      : NOT authorized
Spot / COIN-M / options / cross-
  venue expansion                  : NOT authorized; not recommended
Phase 4aa merge to main            : NOT authorized; preserved on
                                     feature branch unless separately
                                     instructed
```

The next step is operator-driven: the operator decides whether to remain paused, merge Phase 4aa to main and authorize a future docs-only alt-symbol data-requirements / feasibility memo (Option B), or take some other action. Until then, the project remains at the post-Phase-4z merge boundary on `main` with Phase 4aa preserved on its feature branch.

---

**Phase 4aa is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. main remains unchanged at `6fb0c6c8ab0e634684a80e7b339c9c96f3a56b02`. Phase 4aa frames the alt-symbol substrate question and proposes an admissibility framework as a recommendation only. Phase 4z recommendations remain recommendations only. C1 / V2 / G1 first-specs remain terminally HARD REJECTED. Recommended state: remain paused (primary); Option B docs-only alt-symbol data-requirements memo (conditional secondary; not authorized by Phase 4aa). No next phase authorized.**
