# Phase 4am — Closeout Report

## 1. Phase Identity

```text
Phase:                Phase 4am
Title:                Exit Architecture Backtest-Logic Audit
Type:                 narrow audit-only successor
                      (Phase 4al §11.A scope; Option D)
Branch:               phase-4am/exit-architecture-backtest-logic-audit
Base SHA (origin/main on entry):
                      f97f85025b05ea5591c6e2bc977d68d835381135
```

## 2. Goal

Perform a docs-only audit of the existing backtest scripts
(Phase 4l / V2, Phase 4r / G1, Phase 4x / C1) against the eleven
§11.A audit subjects defined by Phase 4al, and report whether the
existing implementations and reports faithfully apply the
documented Phase 4k / 4q / 4w plan-memo rules and the Phase 3v / 3w
governance.

The allowed outcomes were: clean bill, non-material defect list,
material defect list requiring future governance, or
blocked / insufficient evidence. **No** strategy backtest was rerun;
**no** parameter was tuned; **no** verdict was revised; **no**
script was modified.

## 3. Audit Result

```text
AUDIT RESULT: DOCUMENTATION_LIMITATION

Sub-findings (all non-material to existing verdicts):
- F-1: V2 funding-event right-boundary inclusivity
       (DEFECT_NON_MATERIAL).
- F-2: V2 cost-application formula approximation
       (PASS_WITH_LIMITATION; better classified as
       DOCUMENTATION_LIMITATION since Phase 4k did not specify
       the executed-price formula).
- F-3: V2 / G1 missing governance-label artefact fields
       (DOCUMENTATION_LIMITATION).
- F-4: Entry-bar exit handling divergence between V2 and G1 / C1
       (DEFECT_NON_MATERIAL).

Material defects:                zero.
Governance-blocked findings:     zero.
Not-auditable findings:          zero.

Per-§11.A summary:
  .1  Fee handling                  — PASS (all 3 scripts)
  .2  Slippage handling             — PASS (all 3 scripts)
  .3  Funding handling              — V2 DEFECT_NON_MATERIAL;
                                      G1 PASS; C1 PASS (excluded
                                      per spec)
  .4  Stop / TP sequencing          — PASS (all 3 scripts)
  .5  Stop-trigger-domain           — V2 / G1 DOCUMENTATION_LIMITATION
                                      on label recording; C1 PASS
  .6  Partial-exit logic            — PASS (absent in all 3)
  .7  Break-even logic              — V2 / G1 DOCUMENTATION_LIMITATION
                                      on label recording; C1 PASS
  .8  Trailing-exit logic           — PASS (absent in all 3)
  .9  Time-exit logic               — PASS (all 3 scripts)
  .10 Realized-R-after-costs        — V2 PASS_WITH_LIMITATION;
                                      G1 / C1 PASS
  .11 Intrabar ambiguity (tie-break) — PASS (all 3 scripts)
  .11 Intrabar ambiguity (entry-bar
       exit handling)                — DEFECT_NON_MATERIAL (V2 vs
                                      G1 / C1 divergence)
```

## 4. What Was Audited

- `scripts/phase4l_v2_backtest.py` (V2; 2 449 lines).
- `scripts/phase4r_g1_backtest.py` (G1; 2 997 lines).
- `scripts/phase4x_c1_backtest.py` (C1; 3 338 lines).
- Phase 4k V2 backtest-plan memo (cost / funding rules; cost cells;
  §11.6 promotion gate).
- Phase 4q G1 backtest-plan memo (cost / funding implementation
  plan; sizing / exposure plan; governance labels).
- Phase 4w C1 backtest-plan memo (cost-model implementation plan;
  funding excluded for C1 first-spec; governance labels).
- Phase 3v stop-trigger-domain governance (§8 four-value label
  scheme; `mixed_or_unknown` invalid).
- Phase 3w break-even / EMA-slope / stagnation governance
  (§6 / §7 / §8; per-candidate historical provenance preserved).
- Phase 4l / 4r / 4x execution reports (verdict context;
  CFP-1 critical for V2 and G1; mean_R = −0.36 for C1).

## 5. What Was Not Audited

- No retained-population MFE / MAE / time-to-MFE / time-to-stop
  forensic distributions were computed (Phase 4al §11.A.10 / Option
  C scope; not part of Phase 4am).
- No trade ledger was opened or aggregated.
- No backtest was rerun.
- No new analysis output was generated.
- No 5m / 1m / aggTrades / tick data was considered.
- No mark-price-stop-domain forensic was performed.

## 6. Files Added

```text
docs/00-meta/implementation-reports/
  2026-05-06_phase-4am_exit-architecture-backtest-logic-audit.md
docs/00-meta/implementation-reports/
  2026-05-06_phase-4am_closeout.md
```

## 7. Files Modified

```text
docs/00-meta/current-project-state.md
  (narrow Phase 4am status entry; no governance, locks, or verdict
   changes beyond the addition)
```

## 8. Files NOT Modified

Phase 4am did not modify:

- any source code under `src/prometheus/`,
- any test under `tests/`,
- any script under `scripts/` (V2, G1, C1, or any other),
- any data under `data/raw/`, `data/normalized/`, or
  `data/manifests/`,
- any manifest,
- any backtest script (Phase 4l, Phase 4r, Phase 4x specifically
  preserved unchanged),
- `docs/00-meta/m0-mechanism-admissibility-gate.md`,
- `docs/00-meta/ai-coding-handoff.md`,
- `docs/00-meta/implementation-ambiguity-log.md`,
- `docs/12-roadmap/phase-gates.md`,
- `docs/12-roadmap/technical-debt-register.md`,
- `docs/03-strategy-research/*`,
- `docs/04-data/*`,
- `docs/05-backtesting-validation/*`,
- `docs/06-execution-exchange/*`,
- `docs/07-risk/*`,
- `docs/08-architecture/*`,
- `docs/09-operations/*`,
- `docs/10-security/*`,
- `docs/11-interface/*`,
- prior phase implementation reports,
- prior phase closeout reports,
- `.mcp.json`, `.env*`, `pyproject.toml`.

No helper script was created.

## 9. Helper Script

**No helper script was created.** All audit findings are
derivable from direct code inspection (`Grep` + `Read`) and direct
spec inspection of Phase 4k / 4q / 4w plan memos and Phase 3v / 3w
governance memos. No synthetic micro-cases were required.

Per the operator instruction: "If no helper script is created, no
pytest / ruff / mypy is required unless docs tooling requires it."
No source / test / script changes were made; quality gates are
unchanged from the post-Phase-4al merge state.

## 10. Verdicts and Locks Preserved

```text
H0:           FRAMEWORK ANCHOR
R3:           BASELINE-OF-RECORD
R1a:          RETAINED — NON-LEADING
R1b-narrow:   RETAINED — NON-LEADING
R2:           FAILED — §11.6
F1:           HARD REJECT
D1-A:         MECHANISM PASS / FRAMEWORK FAIL — other
5m thread:    OPERATIONALLY CLOSED per Phase 3t
V2:           HARD REJECT — terminal for V2 first-spec
G1:           HARD REJECT — terminal for G1 first-spec
C1:           HARD REJECT — terminal for C1 first-spec

§11.6:        8 bps per side; round-trip 16 bps slippage
§1.7.3:       0.25% / 2× / 1-position / mark-price stops
Phase 3r §8:  mark-price gap governance
Phase 3v §8:  stop-trigger-domain governance
Phase 3w §6/§7/§8:
              break-even / EMA-slope / stagnation governance
Phase 4j §11: metrics OI-subset partial eligibility
Phase 4k:     V2 backtest-plan methodology
Phase 4p:     G1 strategy-spec discipline
Phase 4q:     G1 backtest-plan methodology
Phase 4v:     C1 strategy-spec discipline
Phase 4w:     C1 backtest-plan methodology
M0 (4ak):     twelve-clause gate + post-null cooldown +
              cooled-down families + memo template
```

No verdict revised. No lock changed.

## 11. Verification Commands Run

- `git status` — clean working tree on entry.
- `git fetch origin` — succeeded.
- `git checkout main` — succeeded.
- `git pull --ff-only origin main` — succeeded; already up to date.
- `git rev-parse main` → `f97f85025b05ea5591c6e2bc977d68d835381135`.
- `git rev-parse origin/main` → `f97f85025b05ea5591c6e2bc977d68d835381135`
  (matched required base).
- `git log --oneline -5` — matched expected post-Phase-4al state.
- `git checkout -b phase-4am/exit-architecture-backtest-logic-audit`
  — succeeded.
- `Grep`, `Read`, `Glob` — used to locate scripts, governance docs,
  and key code regions; full inspection of cost / funding / stop /
  TP / time-stop / break-even / partial-exit / trailing / governance-
  label / R-denominator code paths in all three backtest scripts.
- `git diff --check` — no whitespace errors; only LF→CRLF advisory warning.
- `git diff --stat` — docs-only diff; `docs/00-meta/current-project-state.md`
  modified and two Phase 4am implementation-report files added.
- No `pytest` / `ruff` / `mypy` was required because no source,
  test, or script was changed.

## 12. Recommendation

```text
Primary:               REMAIN PAUSED with documented non-material
                       findings logged.
Conditional secondary: future docs-only methodology-harmonization
                       memo (specify executed-price-shifting cost
                       formula prospectively; specify entry-bar
                       exit handling prospectively; specify funding-
                       event boundary handling prospectively; add
                       four governance labels to V2 / G1 run_metadata
                       for parity with C1) — NOT authorized by
                       Phase 4am.
Conditional tertiary:  full Phase 4al-Option-C exit-path forensic
                       analysis — NOT recommended (audit foundation
                       is clean; forensic analysis is acceptable
                       but not preferred over remain-paused) and
                       NOT authorized by Phase 4am.
Forbidden:             verdict revision; lock revision; parameter
                       optimization; rescue of any historical
                       candidate; paper / shadow / live-readiness /
                       deployment / exchange-write.
```

## 13. Final Status

```text
Phase 4am type:                    narrow audit-only successor
                                   (Phase 4al Option D / §11.A scope)
Aggregate audit result:            DOCUMENTATION_LIMITATION
Material defects:                  zero
Non-material defects:              two (F-1 V2 funding right-boundary
                                   inclusivity; F-4 entry-bar exit
                                   handling divergence)
Documentation limitations:         two (F-2 V2 cost-application
                                   approximation; F-3 V2 / G1
                                   missing governance-label artefact
                                   fields)
Verdicts revised:                  none
Locks changed:                     none
Successor phase authorized:        none
Recommended project state:         remain paused
```

**No successor phase is authorized.** The recommended state remains
**paused**. Any future Phase 4an or other successor phase requires
explicit, separate operator authorization and is not implied by
Phase 4am's findings.
