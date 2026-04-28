# Phase 3d-B2 Closeout Report

**Phase:** 3d-B2 — F1 (mean-reversion-after-overextension) candidate execution + first-execution gate evaluation + M1/M2/M3 mechanism checks + Phase 3c §8 mandatory diagnostics + P.14 hard-block invariants. **First phase to authorize F1 candidate backtest invocation.**

**Date:** 2026-04-28 UTC.

**Status:** **F1 framework verdict: HARD REJECT.** All four mandatory R-window runs executed (F1 R MED MARK / R LOW MARK / R HIGH MARK / R MED TRADE_PRICE) per Phase 3c §6.1. Conditional F1 V MED MARK run #5 NOT executed because the R-window first-execution gate hard-rejected per Phase 3c §6.2 / §11.3 conditional-rule. Multiple catastrophic absolute-floor violations: BTC MED expR=−0.5227 ≤ −0.50; BTC HIGH expR=−0.7000 ≤ −0.50; BTC HIGH PF=0.2181 ≤ 0.30; ETH HIGH expR=−0.5712 ≤ −0.50; ETH HIGH PF=0.2997 ≤ 0.30. Pre-execution quality gates green; H0/R3 control reproduction bit-for-bit on all 48 metric cells before F1 interpretation; P.14 hard-block invariants all PASS. **F1 is retained as research evidence; the F1 family is concluded as FAILED (HARD REJECT) under Phase 3c §7.3 governance.** No project-state change. No `data/` commits. Phase 3d-B2 is terminal for F1; no subsequent F1 phase proposed. Branch `phase-3d-b2/f1-execution-diagnostics` not pushed and not merged. Awaiting operator review.

---

## 1. Current branch

```
phase-3d-b2/f1-execution-diagnostics
```

Branched from `main` at `4a2b7d0d6f8547535318cbae15ca738c4a47f8b3` (the post-Phase-3d-B1 merge-report tip). Not pushed. Not merged.

## 2. Git status

After the Phase 3d-B2 commit:

```
On branch phase-3d-b2/f1-execution-diagnostics
nothing to commit, working tree clean
```

(State as of immediately after the final Phase 3d-B2 commit, which includes the runner upgrade, the analysis script, the diagnostics report, and this closeout report.)

## 3. Files changed

Total: **4 files** added or modified across the entire Phase 3d-B2 branch (vs `main`):

### 3.1 Modified — Phase 3d runner upgraded from scaffold to full run-loop (1 file)

- [scripts/phase3d_F1_execution.py](../../../scripts/phase3d_F1_execution.py) — replaced the Phase 3d-B1 hard-guard scaffold with a full Phase 3d-B2 run-loop. The `f1` subcommand now (under `--phase-3d-b2-authorized`) loads v002 datasets, builds a `BacktestConfig` with `strategy_family=MEAN_REVERSION_OVEREXTENSION` and the locked default `MeanReversionConfig()`, runs the engine via the merged Phase 3d-B1 dispatch, and writes `trade_log.parquet` + `summary_metrics.json` (F1-aware: TARGET / TIME_STOP / STOP / END_OF_DATA exit-reason taxonomy) + `f1_lifecycle_total.json` + `monthly_breakdown.parquet` per symbol per run, plus the standard report manifest. Adds slippage aliases LOW / MED / MEDIUM / HIGH; window R / V; stop-trigger MARK_PRICE / TRADE_PRICE. Preserves the Phase 3d-B1 `check-imports` action unchanged.

### 3.2 Created — analysis script (1 file)

- [scripts/_phase3d_F1_analysis.py](../../../scripts/_phase3d_F1_analysis.py) — consumes the Phase 3d-B2 F1 run artifacts plus the H0/R3 control runs and computes (a) the §7.2 first-execution-gate evaluation, (b) M1 post-entry counter-displacement at horizons {1, 2, 4, 8} normalized to R-multiples, (c) M2 chop-regime (low-vol tercile) stop-out fraction for F1 vs H0, (d) M3 TARGET-exit subset aggregate / mean R, (e) Phase 3c §8 mandatory-diagnostics subset (per-fold, exit-reason fractions, distributions, P.14 invariants), and (f) descriptive cross-family deltas vs H0 R / R3 R. Writes a single JSON summary under `data/derived/backtests/phase-3d-f1-analysis-<run_id>.json` (git-ignored).

### 3.3 Created — Phase 3d-B2 reports (2 files)

- [docs/00-meta/implementation-reports/2026-04-28_phase-3d-B2_F1_execution-diagnostics.md](2026-04-28_phase-3d-B2_F1_execution-diagnostics.md) — Phase 3d-B2 diagnostics report (18 brief-required items): preflight, quality gates, H0/R3 reproduction, F1 runs executed, summary metrics, first-execution gate, verdict, M1/M2/M3 mechanism, mandatory diagnostics, P.14, cross-family descriptive comparison, scope confirmations.
- [docs/00-meta/implementation-reports/2026-04-28_phase-3d-B2_closeout-report.md](2026-04-28_phase-3d-B2_closeout-report.md) — this file (10 brief-required items).

### 3.4 Files NOT touched

- `src/prometheus/research/backtest/engine.py` — engine F1 dispatch is the merged Phase 3d-B1 path, used unchanged.
- `src/prometheus/research/backtest/config.py` — F1 dispatch validator merged in Phase 3d-B1, used unchanged.
- `src/prometheus/research/backtest/trade_log.py` — F1 TradeRecord fields merged in Phase 3d-B1, used unchanged.
- `src/prometheus/strategy/v1_breakout/` — entire V1 module unchanged.
- `src/prometheus/strategy/mean_reversion_overextension/` — Phase 3d-A primitives preserved verbatim.
- All existing tests under `tests/unit/` — preserved bit-for-bit; pytest 567 passing.
- All existing scripts under `scripts/` (`phase2l_R3_first_execution.py`, `phase2w_R2_execution.py`, etc.) — unchanged; Phase 3d-B2 used `phase2l_R3_first_execution.py` unmodified for the H0/R3 control re-runs.
- `data/`, `.claude/`, `.mcp.json`, configuration / credentials — untouched.
- All existing docs (current-project-state, ai-coding-handoff, phase-gates, technical-debt-register, validation-checklist, cost-modeling, backtesting-principles, data-requirements, dataset-versioning, v1-breakout-strategy-spec, Phase 3a/3b/3c/3d-A/3d-B1 memos and reports) — unchanged.

## 4. Commit hash or hashes

The Phase 3d-B2 branch has a single artifact commit on top of `main` (`4a2b7d0d6f8547535318cbae15ca738c4a47f8b3`). The full SHA is recorded in the final chat response after the commit lands.

The branch is therefore **1 commit ahead of `main`** at the time of any future merge.

## 5. F1 runs executed

Four mandatory R-window cells per Phase 3c §6.1, plus four V1 H0/R3 control re-runs per Phase 3c §6.3 / §6.4 baseline-preservation discipline (the latter use the existing `scripts/phase2l_R3_first_execution.py` unchanged):

| Run | Variant | Window | Slippage | Stop trigger | Run dir (under `data/derived/backtests/`) |
|---:|:-------:|:------:|:--------:|:------------:|:-----------------------------------------|
| 1 | F1 | R | MEDIUM | MARK_PRICE | `phase-3d-f1-window=r-slip=medium/2026-04-28T21-55-59Z/` |
| 2 | F1 | R | LOW | MARK_PRICE | `phase-3d-f1-window=r-slip=low/2026-04-28T22-05-42Z/` |
| 3 | F1 | R | HIGH | MARK_PRICE | `phase-3d-f1-window=r-slip=high/2026-04-28T22-15-22Z/` |
| 4 | F1 | R | MEDIUM | TRADE_PRICE | `phase-3d-f1-window=r-slip=medium-stop=trade_price/2026-04-28T22-25-02Z/` |
| 5 (skipped) | F1 | V | MEDIUM | MARK_PRICE | NOT EXECUTED (R-window HARD REJECT per §6.2) |
| 6 | H0 | R | MEDIUM | MARK_PRICE | `phase-2l-h0-r/2026-04-28T21-40-58Z/` |
| 7 | H0 | V | MEDIUM | MARK_PRICE | `phase-2l-h0-v/2026-04-28T21-41-09Z/` |
| 8 | R3 | R | MEDIUM | MARK_PRICE | `phase-2l-r3-r/2026-04-28T21-41-20Z/` |
| 9 | R3 | V | MEDIUM | MARK_PRICE | `phase-2l-r3-v/2026-04-28T21-41-31Z/` |

All `data/derived/backtests/` artifacts are git-ignored; **no `data/` commit was made.**

## 6. F1 verdict

**HARD REJECT.**

Per Phase 3c §7.3 verdict mapping, any catastrophic absolute-floor violation (`expR ≤ −0.50` OR `PF ≤ 0.30` on BTC/ETH × MED/HIGH × MARK_PRICE) classifies the outcome as HARD REJECT. F1's Phase 3d-B2 results produce **five separate catastrophic-floor violations**:

| Cell | Symbol | Metric | Threshold | Observed | Violation |
|------|:-:|--------|----------|----------|:-:|
| F1 R MED MARK | BTC | expR | > −0.50 | −0.5227 | ✗ |
| F1 R HIGH MARK | BTC | expR | > −0.50 | −0.7000 | ✗ |
| F1 R HIGH MARK | BTC | PF | > 0.30 | 0.2181 | ✗ |
| F1 R HIGH MARK | ETH | expR | > −0.50 | −0.5712 | ✗ |
| F1 R HIGH MARK | ETH | PF | > 0.30 | 0.2997 | ✗ |

The verdict is **HARD REJECT** with substantial margin. Per Phase 3c §7.3, this supersedes the alternative MECHANISM-FAIL / MECHANISM-PASS / FRAMEWORK-FAIL classifications even though M3 (target-exit subset isolated profitability) is mechanism-supported. F1 is retained as research evidence; the F1 family is concluded as FAILED.

Mechanism summary (descriptive):

- **M1 BTC PARTIAL:** mean counter-displacement at h=8 is +0.0238 R (well below the +0.10 R PASS threshold) but fraction non-neg is 55.38% (above the 50% PASS threshold). Conjunctive M1 PASS fails. Direction-supported, magnitude-falsified.
- **M2 BTC FAIL / ETH PASS-with-weak-baseline:** F1's BTC low-vol stop-out fraction (55.56%) is *higher* than H0's (46.15%), the *opposite* of the §9.2 chop-regime advantage hypothesis. ETH Δ_M2 = +0.39 supports the hypothesis on ETH but H0's ETH low-vol n=12 baseline is statistically weak.
- **M3 PASS on both symbols:** the TARGET-exit subset is profitable in isolation (BTC mean +0.75 R / ETH mean +0.87 R; aggregate +1149 R BTC / +1398 R ETH). However the wider F1 strategy-as-specified is FAILED because STOP exits (53–54% of trades) overwhelm the TARGET-exit positive contribution.

## 7. Confirmation that no disallowed runs were executed

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

**None of the above were executed.** Only the four mandatory R-window cells (§5 runs #1–#4) were run. The conditional V-window run #5 was skipped per the §6.2 / §11.3 conditional rule because the R-window gate hard-rejected.

## 8. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` shows zero `data/` entries. The four F1 runs, the four V1 H0/R3 control re-runs, and the analysis script's JSON output all wrote into the git-ignored `data/derived/backtests/` tree only. No `git add data/` was executed. The Phase 3d-B2 commit is limited to `scripts/phase3d_F1_execution.py`, `scripts/_phase3d_F1_analysis.py`, and the two `docs/00-meta/implementation-reports/` files.

## 9. Confirmation that no forbidden areas changed

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

## 10. Whether the branch is ready for operator review

**Ready for review.** Phase 3d-B2 has executed the precommitted Phase 3c §6 run inventory in full, computed the §7.2 first-execution gate and §9 M1/M2/M3 mechanism checks, produced the §8 mandatory diagnostics, and recorded the F1 framework verdict (HARD REJECT) under §7.3 governance.

- **Technically ready:**
  - Branch is clean (`nothing to commit, working tree clean` after the Phase 3d-B2 commit).
  - All 4 quality gates green pre-execution: `pytest`: 567 passed; `ruff check`: All checks passed; `ruff format --check`: 144 files already formatted; `mypy src`: Success no issues.
  - All 48 H0/R3 control cells reproduce bit-for-bit on locked Phase 2 baselines pre-F1-interpretation.
  - All P.14 hard-block invariants PASS on F1 R MED MARK BTC and ETH.
  - F1 funnel-counter accounting identity holds on all four cells.
  - F1 emits only allowed exit reasons (STOP / TARGET / TIME_STOP / END_OF_DATA).
  - F1 stop-distance band [0.60, 1.80] empirically respected (min=0.6001 / max=1.7992 BTC; min=0.6002 / max=1.7988 ETH).
  - No `data/` commits.
- **Procedurally ready:**
  - Phase 3b F1 spec axes consumed verbatim; no spec change.
  - Phase 3c §3 forbidden adjustments not made (no parameter variant, threshold change, F1-prime, run-set expansion, post-hoc rerun).
  - Phase 3c §10.4 sequencing requirement satisfied (quality gates → H0/R3 controls bit-for-bit → F1 candidates).
  - Phase 3c §6 run inventory respected (only the 4 mandatory R-window cells + conditional V skipped per §6.2).
  - Phase 3c §7.2 + §7.3 verdict mapping applied without post-hoc loosening (Phase 2f §11.3.5).
  - Phase 3c §7.4 cross-family-fairness preserved (H0/R3 deltas reported descriptively only).
- **Verdict ready:** F1 framework outcome is HARD REJECT. F1 is retained as research evidence per the same precedent as R1a / R1b-narrow / R2.
- **Not yet merged.** Per explicit operator instruction: "Do not merge to main."
- **Phase 3d-B2 is terminal for F1.** Per explicit operator instruction: "Do not start any next phase." No subsequent F1 phase is proposed.

**Open Phase 3d-B2 recommendation (deferred to operator):** **CLOSE the F1 research arc.** F1 family is FAILED-HARD-REJECT; no subsequent F1 phase is proposed. The operator may also choose to merge or hold the Phase 3d-B2 branch indefinitely; either choice preserves project state. All Phase 3c-affirmed restrictions stand: no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / threshold-change / project-lock change.

The branch can be merged to `main` and pushed when the operator authorizes the merge. No technical blocker exists.

---

**Stopped per operator instruction.** No file modified outside the Phase 3d-B2 scope. F1 verdict recorded as HARD REJECT. F1 V-window run not executed (R-window hard-rejected). No subsequent phase started. Branch `phase-3d-b2/f1-execution-diagnostics` not pushed and not merged. Awaiting operator review.
