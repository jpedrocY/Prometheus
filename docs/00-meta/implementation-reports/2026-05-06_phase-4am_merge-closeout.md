# Phase 4am Merge Closeout — Exit Architecture Backtest-Logic Audit

## Purpose

This document records the no-fast-forward merge of completed Phase 4am into `main`.

This is a merge closeout only. It does not authorize Phase 4an, full exit-path forensic analysis, fresh-hypothesis discovery, strategy work, strategy specs, backtest plans, backtests, data acquisition, 5m / 1m / aggTrades / tick work, verdict revision, lock revision, code / script / test / manifest changes, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, WebSocket, MCP, Graphify, `.mcp.json`, or credentials.

## Merge Summary

- Phase 4am title: Exit Architecture Backtest-Logic Audit
- Merge branch: `phase-4am/exit-architecture-backtest-logic-audit`
- Target branch: `main`
- Main before merge: `f97f85025b05ea5591c6e2bc977d68d835381135`
- Phase 4am commit: `6fe3fede7eff6f619ba5ad9775982621c35a7542`
- Merge commit: `9c2c7db222789c6c86d9dd1a3843dbac60740788`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4am

Phase 4am was docs-only (narrow audit-only successor; no code, scripts, tests, data, or manifests modified).

Phase 4am created:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4am_exit-architecture-backtest-logic-audit.md`
- `docs/00-meta/implementation-reports/2026-05-06_phase-4am_closeout.md`

This merge closeout creates:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4am_merge-closeout.md`

Phase 4am also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Phase 4am Summary

Phase 4am was the narrow audit-only successor contemplated by Phase 4al §11.A and Phase 4al Decision Menu Option D.

Phase 4am audited the existing backtest scripts and reports already in the repository, against the documented Phase 4k / 4q / 4w plan-memo rules and the Phase 3v / 3w governance:

- `scripts/phase4l_v2_backtest.py` (V2; 2 449 lines);
- `scripts/phase4r_g1_backtest.py` (G1; 2 997 lines);
- `scripts/phase4x_c1_backtest.py` (C1; 3 338 lines).

Phase 4am audited the eleven §11.A subjects:

- fee handling;
- slippage handling;
- funding handling;
- stop / TP sequencing;
- stop-trigger-domain governance;
- partial-exit logic;
- break-even logic;
- trailing-exit logic;
- time-exit logic;
- realized-R-after-costs accounting;
- intrabar ambiguity.

Phase 4am explicitly did not:

- run a backtest;
- modify any backtest script (Phase 4l, Phase 4r, Phase 4x preserved unchanged);
- modify any source / test / data / manifest;
- generate new analysis output;
- compute full retained-population MFE / MAE / time-to-MFE / time-to-stop forensic distributions (Phase 4al §11.A.10 / Option C scope; not part of Phase 4am);
- tune or optimize any TP / SL / break-even / trailing / partial-exit / time-exit parameter;
- rescue any prior strategy candidate;
- revise any historical verdict;
- acquire 5m / 1m / aggTrades / tick data.

No helper script was created. Findings were derivable from direct code inspection (`Grep` + `Read`) and direct spec inspection of Phase 4k / 4q / 4w plan memos and Phase 3v / 3w governance memos.

## Audit Result

```text
Aggregate result:                DOCUMENTATION_LIMITATION
Material defects:                zero
Governance-blocked findings:     zero
Not-auditable findings:          zero
```

Non-material findings:

- **F-1.** V2 funding-event right-boundary inclusivity — `DEFECT_NON_MATERIAL`. V2 uses `(entry_ms, exit_ms]` via `searchsorted(..., side="right")` on both endpoints; G1 uses strictly between per Phase 4q spec. Phase 4k did not specify boundary handling. Affects only events at exact-boundary timestamps; bounded R impact; non-material to V2's zero-trade Verdict C HARD REJECT.
- **F-2.** V2 cost-application formula approximation — `DOCUMENTATION_LIMITATION` / `PASS_WITH_LIMITATION`. V2 uses `cost_R = round_trip_frac × entry_price / initial_R` (flat-`entry_price` round-trip approximation); G1 / C1 use the executed-price-shifting formula per Phase 4q / 4w. Per-trade error bound `≤ 2 × N_R × per_side_bps / 10000 ≈ 0.48% R` at HIGH N_R = 2.0; partially cancelling at population level. Phase 4k did not specify the executed-price formula explicitly, so this is more accurately a documentation gap than an implementation defect.
- **F-3.** V2 / G1 missing governance-label artefact fields — `DOCUMENTATION_LIMITATION`. V2 and G1 do not record the four governance labels (`stop_trigger_domain`, `break_even_rule`, `ema_slope_method`, `stagnation_window_role`) in `run_metadata.json`; C1 records all four. Behaviour matches the labels in all three scripts; the gap is artefact-recording only.
- **F-4.** Entry-bar exit handling divergence between V2 and G1 / C1 — `DEFECT_NON_MATERIAL`. V2 guards exit checking with `if i > entry_idx:` and cannot exit on the entry bar; G1 / C1 lack the guard and can. Plan memos do not specify the behaviour. Both conventions defensible.

All findings were non-material to existing verdicts. V2 and G1 zero-trade outcomes are unaffected by funding boundary, cost approximation, or entry-bar exit handling. C1's `mean_R = -0.36` across 149 BTC OOS HIGH trades is too dominant to be flipped by any of the bounded effects.

No verdict requires review on the basis of audit findings. No future governance decision is required before any verdict could even be considered for review.

## Recommendation

Phase 4am primary recommendation:

```text
Remain paused with documented non-material findings logged.
```

Conditional secondary (NOT authorized by Phase 4am):

```text
A future docs-only methodology-harmonization memo may be proposed separately.
Possible content: specify the executed-price-shifting cost formula prospectively;
specify entry-bar exit handling prospectively; specify funding-event boundary
handling prospectively; add the four governance labels to V2 / G1 run_metadata.json
for parity with C1.
```

Conditional tertiary (NOT recommended; NOT authorized):

```text
Full Phase 4al-Option-C exit-path forensic analysis. Audit foundation is clean
enough that forensic analysis is acceptable but not preferred over remain-paused.
```

No verdict review is implied or recommended.

## Governance Status

Phase 4am does not authorize Phase 4an.

Phase 4am does not authorize full exit-path forensic analysis.

Phase 4am does not authorize fresh-hypothesis discovery.

Phase 4am does not authorize strategy specs.

Phase 4am does not authorize backtest plans.

Phase 4am does not authorize backtests.

Phase 4am does not authorize data acquisition.

Phase 4am does not authorize 5m / 1m / aggTrades / tick work.

Phase 4am does not authorize verdict revision.

Phase 4am does not authorize lock revision.

Phase 4am does not authorize code, script, test, manifest, credential, `.mcp.json`, MCP, Graphify, exchange-write, paper / shadow, live-readiness, deployment, or production-key work.

Phase 4am does not adopt the Phase 4z 32-item framework as binding governance.

Phase 4am does not adopt the Phase 4z M0–M7 mechanism-check redesign wholesale.

Phase 4am does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4am does not adopt Phase 4ab recommendations as binding governance.

Phase 4am does not broaden Phase 4ac results beyond data / integrity evidence.

Phase 4am does not broaden Phase 4ad Rules A / B / C beyond prospective analysis-time scope.

Phase 4am does not broaden Phase 4ae findings beyond descriptive substrate-feasibility evidence.

Phase 4am does not broaden Phase 4af findings beyond descriptive regime-continuity / directional-persistence evidence.

Phase 4am does not broaden Phase 4ag recommendations beyond recommendation-only status.

Phase 4am does not broaden Phase 4ah recommendations beyond recommendation-only status.

Phase 4am does not broaden Phase 4ai findings beyond descriptive cross-sectional feasibility evidence.

Phase 4am does not broaden Phase 4aj recommendations beyond the specific revised M0 and post-null cooldown rule already adopted by Phase 4ak.

Phase 4am does not broaden the Phase 4ak adoption beyond §5–§8 of `docs/00-meta/m0-mechanism-admissibility-gate.md`.

Phase 4am does not broaden Phase 4al's CONDITIONAL / PARTIAL admissibility verdict beyond the §9 / §10 / §11 / §13 boundaries, the §14 future data-resolution recommendation, and the §17 explicit non-authorization statement.

## Boundary Confirmation

This merge did not start:

- Phase 4an;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- full exit-path forensic analysis;
- strategy diagnostics;
- strategy work;
- backtests;
- data acquisition;
- data download;
- API calls;
- endpoint calls;
- 5m / 1m / aggTrades / tick work;
- MFE / MAE retained-population forensics;
- mark-price stop-domain forensic analysis;
- analysis execution;
- data modification;
- manifest creation;
- manifest modification;
- v003 or any dataset version;
- Phase 4l / 4r / 4x backtest rerun;
- any backtest;
- any strategy diagnostic;
- Q1–Q7 rerun;
- strategy PnL calculation;
- entry / exit strategy-return calculation;
- parameter optimization;
- threshold selection for a future strategy;
- a new strategy candidate;
- a strategy-candidate name;
- a fresh-hypothesis discovery memo;
- a hypothesis-spec memo;
- a strategy spec;
- a backtest plan;
- R3 rescue;
- R2 rescue;
- F1 rescue;
- D1-A rescue;
- V2 rescue;
- G1 rescue;
- C1 rescue;
- R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime;
- V1-D1 / F1-D1 / any hybrid;
- old-strategy alt-symbol reruns;
- multi-position portfolio trading;
- verdict revision;
- lock revision;
- paper / shadow;
- live-readiness;
- deployment;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user stream;
- WebSocket;
- exchange-write;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

This merge did not modify:

- source code under `src/prometheus/`;
- tests;
- scripts;
- backtest scripts (Phase 4l, Phase 4r, Phase 4x preserved unchanged);
- raw data;
- normalized data;
- manifests;
- runtime implementation;
- existing strategy specifications;
- credentials;
- `.mcp.json`;
- specialist governance files (Phase 3r, 3v, 3w, 4j §11, 4k, 4p, 4q, 4v, 4w, M0 governance preserved verbatim);
- retained verdicts;
- project locks.

## Retained Verdict Ledger

Retained verdicts remain unchanged:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains operationally CLOSED per Phase 3t.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

No retained verdicts were revised.

## Project Locks

Project locks remain unchanged, including:

- §11.6 HIGH cost = 8 bps per side.
- Round-trip HIGH slippage = 16 bps.
- §1.7.3 project-level locks:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 preserved.
- Phase 3v §8 preserved.
- Phase 3w §6 / §7 / §8 preserved.
- Phase 4j §11 preserved.
- Phase 4k preserved.
- Phase 4p preserved.
- Phase 4q preserved.
- Phase 4v preserved.
- Phase 4w preserved.
- M0 (Phase 4ak) §5 / §6 / §7 / §8 of `docs/00-meta/m0-mechanism-admissibility-gate.md` preserved.
- Phase 4z recommendations remain recommendations only.
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.
- Phase 4ac results remain data / integrity evidence only.
- Phase 4ad Rules A / B / C remain prospective analysis-time scope rules only.
- Phase 4ae findings remain descriptive substrate-feasibility evidence only.
- Phase 4af findings remain descriptive regime-continuity / directional-persistence evidence only.
- Phase 4ag recommendations remain recommendations only.
- Phase 4ah recommendations remain recommendations only.
- Phase 4ai findings remain descriptive cross-sectional feasibility evidence only.
- Phase 4aj recommendations remain recommendations only beyond the specific revised M0 and post-null cooldown rule already adopted by Phase 4ak.
- Phase 4al CONDITIONAL / PARTIAL admissibility verdict remains bounded by §9 / §10 / §11 / §13 of the Phase 4al main memo and §14 future data-resolution recommendation only.
- Phase 4am findings remain documentation-limitation / non-material-defect evidence only.

No project locks were changed.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4am does not recommend immediate fresh-hypothesis discovery.

Phase 4am does not recommend immediate strategy work.

Phase 4am does not recommend full exit-path forensic analysis over remain-paused.

Phase 4am does not authorize Phase 4an.

No next phase is authorized by this merge closeout.
