# Phase 3d-B2 Merge Report

**Phase:** 3d-B2 — F1 (mean-reversion-after-overextension) candidate execution + first-execution gate evaluation + M1/M2/M3 mechanism checks + Phase 3c §8 mandatory diagnostics + P.14 hard-block invariants.

**Date:** 2026-04-28 UTC.

**Status:** **Merged into `main`.** F1 framework verdict is **HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate (multiple BTC/ETH × MED/HIGH absolute-floor violations). F1 V-window run #5 was not executed because the R-window first-execution gate hard-rejected per Phase 3c §6.2 / §11.3 conditional-rule. F1 is retained as research evidence; the F1 family is concluded as FAILED. **Phase 3d-B2 is terminal for F1; no subsequent F1 phase is proposed.**

---

## 1. Phase 3d-B2 branch tip SHA before merge

```
760245d1dba83392c0e75a365014ce908be24d69
```

(Branch `phase-3d-b2/f1-execution-diagnostics`; 1 commit ahead of `main`'s pre-merge tip `4a2b7d0d6f8547535318cbae15ca738c4a47f8b3`.)

## 2. Merge commit hash

```
f6df7c7b9957c47ec54e32fb56661c8c3f27dab9
```

`--no-ff` merge of `phase-3d-b2/f1-execution-diagnostics` into `main`. Merge commit message: `Merge Phase 3d-B2 (F1 execution + diagnostics + HARD REJECT verdict) into main`.

## 3. Merge-report commit hash

The merge-report commit hash is recorded in the final chat response after this report file is committed to `main` and pushed.

## 4. Main / origin sync confirmation

After the merge push:

```
local  main HEAD: f6df7c7b9957c47ec54e32fb56661c8c3f27dab9
origin main HEAD: f6df7c7b9957c47ec54e32fb56661c8c3f27dab9
```

Local `main` and `origin/main` are synced at the merge commit. After this merge-report commit and push, both advance one further commit in lockstep.

## 5. Git status

```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

(State as of immediately after the merge push, before this merge-report commit. After the merge-report commit and push, both local `main` and `origin/main` advance to the merge-report commit recorded in §3 / final chat response.)

## 6. Latest 5 commits

After the merge push, before this merge-report commit:

```
f6df7c7 Merge Phase 3d-B2 (F1 execution + diagnostics + HARD REJECT verdict) into main
760245d phase-3d-B2: F1 execution + diagnostics + first-execution gate (HARD REJECT)
4a2b7d0 docs(phase-3d-B1): merge report
cbe5f67 Merge Phase 3d-B1 (F1 engine wiring + control reproduction) into main
c682e22 docs(phase-3d-B1): fix closeout §3 file-count to 9
```

After the merge-report commit and push, the latest commit advances to the merge-report commit (recorded in §3 / final chat response).

## 7. Files included in the merge

The merge introduces **4 files** to `main` (vs the pre-merge tip `4a2b7d0`):

### 7.1 Modified — Phase 3d runner upgraded from scaffold to full run-loop (1 file)

- `scripts/phase3d_F1_execution.py` (+480 / −49) — replaced the Phase 3d-B1 hard-guard scaffold with a full Phase 3d-B2 run-loop. The `f1` subcommand (under `--phase-3d-b2-authorized`) loads v002 datasets, builds a `BacktestConfig` with `strategy_family=MEAN_REVERSION_OVEREXTENSION` and the locked default `MeanReversionConfig()`, runs the engine via the merged Phase 3d-B1 dispatch, and writes per-symbol per-run `trade_log.parquet` + `summary_metrics.json` (F1-aware exit-reason taxonomy: STOP / TARGET / TIME_STOP / END_OF_DATA) + `f1_lifecycle_total.json` + `monthly_breakdown.parquet` + the standard report manifest. Adds slippage aliases LOW / MED / MEDIUM / HIGH; window R / V; stop-trigger MARK_PRICE / TRADE_PRICE. Preserves the Phase 3d-B1 `check-imports` action unchanged.

### 7.2 Created — analysis script (1 file)

- `scripts/_phase3d_F1_analysis.py` (~509 lines) — consumes the Phase 3d-B2 F1 run artifacts plus the H0/R3 control runs and computes (a) the §7.2 first-execution-gate evaluation, (b) M1 post-entry counter-displacement at horizons {1, 2, 4, 8} normalized to R-multiples, (c) M2 chop-regime stop-out fraction for F1 vs H0, (d) M3 TARGET-exit subset aggregate / mean R, (e) Phase 3c §8 mandatory-diagnostics subset (per-fold, exit-reason fractions, distributions, P.14 invariants), and (f) descriptive cross-family deltas vs H0 R / R3 R. Writes a single JSON summary to `data/derived/backtests/phase-3d-f1-analysis-<run_id>.json` (git-ignored).

### 7.3 Created — Phase 3d-B2 reports (2 files)

- `docs/00-meta/implementation-reports/2026-04-28_phase-3d-B2_F1_execution-diagnostics.md` (~404 lines) — Phase 3d-B2 diagnostics report (18 brief-required items): preflight, quality gates, H0/R3 reproduction, F1 runs executed, summary metrics, first-execution gate, verdict, M1/M2/M3 mechanism, mandatory diagnostics, P.14, cross-family descriptive comparison, scope confirmations.
- `docs/00-meta/implementation-reports/2026-04-28_phase-3d-B2_closeout-report.md` (~182 lines) — Phase 3d-B2 closeout report (10 brief-required items).

Total: 4 files; +1575 / −49 net lines.

## 8. Confirmation that F1 verdict is HARD REJECT

Confirmed. Per the Phase 3d-B2 diagnostics report §10 and the closeout report §6:

**F1 framework verdict: HARD REJECT.**

Per Phase 3c §7.3 verdict mapping, any catastrophic absolute-floor violation (`expR ≤ −0.50` OR `PF ≤ 0.30` on BTC/ETH × MED/HIGH × MARK_PRICE) classifies the outcome as HARD REJECT. F1's Phase 3d-B2 results produce **five separate catastrophic-floor violations**:

| Cell | Symbol | Metric | Threshold | Observed | Violation |
|------|:-:|--------|----------|----------|:-:|
| F1 R MED MARK | BTC | expR | > −0.50 | −0.5227 | ✗ |
| F1 R HIGH MARK | BTC | expR | > −0.50 | −0.7000 | ✗ |
| F1 R HIGH MARK | BTC | PF | > 0.30 | 0.2181 | ✗ |
| F1 R HIGH MARK | ETH | expR | > −0.50 | −0.5712 | ✗ |
| F1 R HIGH MARK | ETH | PF | > 0.30 | 0.2997 | ✗ |

The HARD REJECT outcome supersedes the alternative MECHANISM-FAIL / MECHANISM-PASS / FRAMEWORK-FAIL classifications even though M3 (target-exit subset isolated profitability) is mechanism-supported. F1 is retained as research evidence per the same precedent that retained R1a / R1b-narrow / R2 as research evidence.

## 9. Confirmation that F1 V-window was skipped correctly

Confirmed. F1 V MED MARK (run #5) was **NOT executed.** Per Phase 3c §6.2 / §11.3, run #5 is conditional on §7.2 PROMOTE outcome at the R-window governing run. The R-window verdict is HARD REJECT (§8 above), which is not PROMOTE, so the conditional rule skips run #5. The skip preserves Phase 2f §11.3 V-window no-peeking discipline: V is not consulted on any non-PROMOTE outcome.

## 10. Confirmation that no forbidden runs were executed

Confirmed. The Phase 3c §6 inventory + Phase 3d-B2 brief explicitly forbid:

- F1 V LOW
- F1 V HIGH
- F1 V TRADE_PRICE
- F1 R LOW TRADE_PRICE
- F1 R HIGH TRADE_PRICE
- Any parameter variant
- Any alternative threshold
- Any extra symbols
- Any post-hoc reruns (no bug found requiring correction)

**None of the above were executed.** Only the four mandatory R-window cells (F1 R MED MARK, F1 R LOW MARK, F1 R HIGH MARK, F1 R MED TRADE_PRICE) were run. The conditional V-window run #5 was skipped per the §6.2 / §11.3 conditional rule.

## 11. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after the merge shows zero `data/` entries. The four F1 R-window runs and the four V1 H0/R3 control re-runs wrote into the git-ignored `data/derived/backtests/` tree only. The analysis script's JSON output also wrote under `data/derived/backtests/` (git-ignored). No `git add data/` was executed. The merge commit and the underlying branch commit (`760245d`) are limited to source code (1 modified script + 1 new analysis script under `scripts/`) and `docs/00-meta/implementation-reports/`.

## 12. Confirmation that no forbidden areas changed

Confirmed across all forbidden categories per the Phase 3d-B2 operator brief:

| Category | Status |
|----------|--------|
| Phase 3b F1 spec axes (window 8 / threshold 1.75 / mean window 8 / stop buffer 0.10 / time-stop 8 / band [0.60, 1.80]) | LOCKED VERBATIM in `MeanReversionConfig` and consumed unmodified |
| Phase 3d-A F1 module + primitives + locked config | PRESERVED VERBATIM |
| Phase 3d-B1 engine wiring (`engine.py`, `config.py`, `trade_log.py`) | PRESERVED VERBATIM (used unchanged from `main`) |
| V1 breakout strategy module | UNCHANGED (control reproduction bit-for-bit on all 48 metric cells) |
| V1 strategy logic, V1 entry/exit machinery, V1 setup predicate, V1 bias filter | UNCHANGED |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH) | PRESERVED VERBATIM |
| Strategy parameters (R3 sub-parameters; H0 baseline; R1a / R1b-narrow / R2 sub-parameters) | PRESERVED VERBATIM |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) | PRESERVED VERBATIM |
| Phase 3c §6 run inventory | PRESERVED (4 mandatory R-window cells executed; conditional V skipped per §6.2; no forbidden cells executed) |
| MCP / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Paper/shadow planning | NOT PROPOSED, NOT AUTHORIZED |
| Phase 4 (runtime / state / persistence) work | NOT PROPOSED, NOT AUTHORIZED |
| Live-readiness work, deployment, exchange-write capability, production keys | NOT PROPOSED, NOT AUTHORIZED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |

**Project-state preservation:** R3 V1-breakout baseline-of-record per Phase 2p §C.1 stands. H0 V1-breakout framework anchor per Phase 2i §1.7.3 stands. R1a / R1b-narrow / R2 retained-research-evidence stand. R2 framework verdict FAILED — §11.6 cost-sensitivity blocks stands. §11.6 = 8 bps HIGH numerical threshold per Phase 2y closeout stands. Phase 2f §11.3.5 binding rule preserved. Phase 3b F1 spec preserved verbatim per Phase 3c §3 / Phase 3d-A scope.

## 13. Confirmation that Phase 3d-B2 is terminal for F1 and no subsequent F1 phase is proposed

Confirmed. Per the Phase 3d-B2 diagnostics report §18 and the closeout report §10:

- **F1 family research is concluded as FAILED (HARD REJECT).** F1 is retained as research evidence per the same Phase 2x / Phase 2y precedent that retained R1a / R1b-narrow / R2 as research evidence.
- **Phase 3d-B2 is the terminal phase for F1.** No subsequent F1 phase is proposed.
- **F1 is not a baseline-of-record candidate.** R3 remains the V1-breakout baseline-of-record per Phase 2p §C.1.
- **F1 is not eligible for paper/shadow consideration** (which remains operator-policy-deferred and would in any case require a PROMOTE outcome).
- **F1 mechanism evidence is partial and informational only:** the SMA(8) target-exit subset is mechanism-consistent and cost-survivable in isolation (M3 PASS), but the wider F1 strategy-as-specified is FAILED. This M3-only mechanism evidence may inform any hypothetical future F1-prime spec consideration in a separately-authorized phase, but Phase 3d-B2 does not propose such a phase.
- **The Phase 2x family-review conclusion stands:** the V1 breakout family is at its useful ceiling; F1 (the Phase 3a rank-1 near-term family candidate) does not extend the framework's edge. No new strategy family is currently proposed.

The next operator decision is operator-driven only:

- (a) Authorize a new research arc (would require a separately-authorized Phase 3a-style discovery memo + Phase 3b spec memo + Phase 3c execution-planning memo + Phase 3d implementation phases), or
- (b) Approve eventual paper/shadow on the existing R3 baseline-of-record (subject to Phase 4 runtime / state / persistence implementation, which is not currently authorized), or
- (c) Hold at the current Phase 3d-B2 boundary indefinitely.

Phase 3d-B2 makes no recommendation among (a), (b), or (c); the decision is operator authority. **Phase 3d-B2 is terminal for F1.**

---

**End of Phase 3d-B2 merge report.** Phase 3d-B2 merged to `main` at `f6df7c7b9957c47ec54e32fb56661c8c3f27dab9`. **F1 framework verdict: HARD REJECT.** F1 V-window correctly skipped per Phase 3c §6.2 conditional. No forbidden runs executed. No `data/` commits. No threshold / strategy parameter / project-lock / paper-shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credential / exchange-write change. Phase 3d-B2 is terminal for F1; no subsequent F1 phase is proposed. Awaiting operator review.
