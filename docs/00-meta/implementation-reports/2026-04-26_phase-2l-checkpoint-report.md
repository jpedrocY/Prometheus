# Phase 2l — Checkpoint Report

Generated at the close of Phase 2l on branch `phase-2l/R3-first-execution`, after Gate 2 approval (with the operator-required regime-diagnostic correction applied during the review cycle). Four operator-authorized commits + this checkpoint = four commits total per the operator-approved commit sequence (this checkpoint is itself the fourth commit). Template per `.claude/rules/prometheus-phase-workflow.md`.

## Phase

**Phase 2l — R3 First Execution.** A code-and-execution phase implementing the Phase 2j memo §D R3 candidate (Fixed-R take-profit + unconditional time-stop, exit-philosophy-only structural redesign) and executing it against the locked Phase 2e v002 datasets on the Phase 2f research window R = 2022-01-01 → 2025-01-01 alongside an H0 control re-run on the same engine version. The first PROMOTE verdict in the project's research history under the unchanged Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 framework. V-window confirmation + LOW/HIGH slippage + TRADE_PRICE stop-trigger sensitivity also produced.

## Goal

(a) Implement R3 minimally: add `exit_kind = FIXED_R_TIME_STOP` with committed sub-parameters R-target = 2.0 and time-stop bars = 8, preserve H0 bit-for-bit as the default path, add `TAKE_PROFIT` and `TIME_STOP` ExitReason values, dispatch in `TradeManagement.on_completed_bar`, wire through `V1BreakoutStrategy.manage`, extend the report aggregator with the new exit-reason counters. (b) Add R3 unit tests + an H0-preservation regression test. (c) Pass quality gates (ruff/format/mypy/pytest). (d) Write a Phase 2l-specific runner mirroring the Phase 2g pattern. (e) Run H0 + R3 on R window for BTC + ETH at MEDIUM slippage, MARK_PRICE stop-trigger; apply the unchanged Phase 2f §10.3 / §10.4 framework. (f) If R3 PROMOTES on R, run V-window confirmation + LOW / HIGH slippage + TRADE_PRICE stop-trigger sensitivity; produce the mandatory diagnostics (per-regime expR using realized 1h volatility classification, MFE distribution, long/short asymmetry, fold-level results, extended exit-reason histogram, TAKE_PROFIT R-multiple distribution, time-stop bias diagnostic). (g) Flag any implementation bug if TRAILING_BREACH or STAGNATION appears in the R3 trade log. (h) Produce the comparison report + Gate 2 review + checkpoint report. (i) Stop before any commit awaiting operator/ChatGPT Gate 2 approval; on approval, commit per the proposed sequence.

## Summary

Phase 2l delivered three committable code/test artifacts (∼450 lines net) and three committable documentation artifacts (∼1,400 lines), plus seven backtest run directories under `data/derived/backtests/phase-2l-*/` (git-ignored). Pytest moved from **396 passed → 404 passed** by exactly the 8 new R3 unit tests. Ruff / format / mypy stayed green throughout. The H0 control re-run reproduced the Phase 2g/2k baseline numbers bit-for-bit (BTC 33 trades / 30.30% / −0.459 / 0.255 / −3.39% / −3.67%; ETH 33 / 21.21% / −0.475 / 0.321 / −3.53% / −4.13%) — confirming the new optional R3 fields and the `exit_kind` dispatch with default `STAGED_TRAILING` preserve H0 behavior bit-for-bit through the strategy facade.

R3 PROMOTED on the R window under Phase 2f §10.3 paths (a) and (c) on both BTC and ETH:

- BTC: Δexp = +0.219 R; ΔPF = +0.305; |maxDD| ratio 0.588× (well below 1.5× veto). expR −0.459 → −0.240; PF 0.255 → 0.560; maxDD 3.67% → 2.16%.
- ETH: Δexp = +0.124 R; ΔPF = +0.153; |maxDD| ratio 0.882×. expR −0.475 → −0.351; PF 0.321 → 0.474; maxDD 4.13% → 3.65%.

Per-fold (5 rolling, GAP-036): R3 beats H0 in 4/5 BTC folds and 3/5 ETH folds; first-ever positive-expR BTC folds (F2 +0.015, F3 +0.100). V-window confirms direction-of-improvement out-of-sample; slippage sensitivity (LOW / MED / HIGH) is monotone and proportional with R3 still beating H0-at-MED at HIGH; TRADE_PRICE bit-identical to MARK_PRICE (zero gap-through stops). Implementation-bug check clean (zero TRAILING_BREACH and zero STAGNATION exits in R3).

The mandatory per-regime expR diagnostic was produced using the operator-required realized 1h volatility-regime classification (trailing 1000 1h-bar window of Wilder ATR(20), tercile cutoffs at 33% / 67%) — **not** as a trade-duration proxy. R3 improves expR in **all six** regime-symbol cells with the largest gains in BTC low_vol (Δexp +0.318) and BTC high_vol (Δexp +0.216) — the regimes where H0 was most broken. No regime-symbol cell shows R3 worse than H0. The duration-bucket view is retained as an auxiliary supplemental diagnostic in §6.1.A of the comparison report, explicitly relabeled. (The Gate 2 first submission had used the duration proxy as the per-regime diagnostic; the operator returned NOT-YET-APPROVED with the regime-classifier correction required; the fix was applied without changing the R3 implementation, run results, promotion framework, committed sub-parameter values, or H0 baseline handling.)

R3 PROMOTE is the **first PROMOTE verdict** in the project's research history. Phase 2g Wave-1's REJECT ALL verdict is preserved as historical evidence under the same framework; no re-derivation, no re-ranking, no comparison-baseline shifting. R3 still has negative aggregate expR; PROMOTE means "less negative than H0 by enough to clear the pre-declared improvement threshold", not "live-ready" — paper/shadow / tiny-live preparation remain bound by `docs/12-roadmap/phase-gates.md`.

## Files changed

By commit, on branch `phase-2l/R3-first-execution` starting from `main @ 1ab3aa3` (Phase 2k merge):

| Commit | Files                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | +/− Lines  |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| 1      | `src/prometheus/strategy/types.py` (+5), `src/prometheus/strategy/v1_breakout/variant_config.py` (+35), `src/prometheus/strategy/v1_breakout/__init__.py` (+2/−1), `src/prometheus/strategy/v1_breakout/management.py` (+60), `src/prometheus/strategy/v1_breakout/strategy.py` (+6/−1), `src/prometheus/research/backtest/report.py` (+6), `tests/unit/strategy/v1_breakout/test_variant_config.py` (+325/−1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | +439 / −3  |
| 2      | `scripts/phase2l_R3_first_execution.py` (new), `scripts/_phase2l_R3_analysis.py` (new)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | +∼720 / 0  |
| 3      | `docs/00-meta/implementation-reports/2026-04-26_phase-2l_R3_variant-comparison.md` (new), `docs/00-meta/implementation-reports/2026-04-26_phase-2l_gate-2-review.md` (new)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | +∼1100 / 0 |
| 4      | `docs/00-meta/implementation-reports/2026-04-26_phase-2l-checkpoint-report.md` (this file)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | this file  |

## Files created

- `docs/00-meta/implementation-reports/2026-04-26_phase-2l_R3_variant-comparison.md`
- `docs/00-meta/implementation-reports/2026-04-26_phase-2l_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-26_phase-2l-checkpoint-report.md` (this file)
- `scripts/phase2l_R3_first_execution.py`
- `scripts/_phase2l_R3_analysis.py`

## Files deleted

None.

## Commands run

- `git checkout phase-2l/R3-first-execution` (existing branch from clean `main`).
- `git status --short`, `git diff --stat`, `git log --oneline -*` at multiple checkpoints.
- `uv run pytest` before each commit and at the evidence stop. Counts: pre-commit-1 **404 passed** / 11.34 s; after commit 1 **404 passed**; after commit 2 **404 passed** (no source changes in 2); after commit 3 **404 passed** (docs only); after commit 4 (this) — expected **404 passed**.
- `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy` — all green at every checkpoint.
- `uv run python scripts/phase2l_R3_first_execution.py --variant H0 --window R` — H0 R-window control.
- `uv run python scripts/phase2l_R3_first_execution.py --variant R3 --window R` — R3 R-window primary.
- `uv run python scripts/phase2l_R3_first_execution.py --variant H0 --window V` — H0 V-window confirmation.
- `uv run python scripts/phase2l_R3_first_execution.py --variant R3 --window V` — R3 V-window confirmation.
- `uv run python scripts/phase2l_R3_first_execution.py --variant R3 --window R --slippage LOW` — R3 LOW slippage.
- `uv run python scripts/phase2l_R3_first_execution.py --variant R3 --window R --slippage HIGH` — R3 HIGH slippage.
- `uv run python scripts/phase2l_R3_first_execution.py --variant R3 --window R --stop-trigger TRADE_PRICE` — R3 GAP-032 stop-trigger sensitivity.
- `uv run python scripts/_phase2l_R3_analysis.py` — internal aggregation, deltas-vs-H0, GAP-036 5-fold consistency, mandatory diagnostics, V-window comparison, slippage sensitivity, stop-trigger sensitivity. Re-run after the regime-classifier correction.
- `git add <specific-files>` + `git commit -m "<heredoc>"` four times per the operator-approved sequence (this checkpoint is the fourth commit).

## Installations performed

None. No `uv add`, no `uv sync` change, no global installs. `pyproject.toml` and `uv.lock` unchanged.

## Configuration changed

None. No `configs/`, `.env`, `.claude/`, `.gitignore`, or `.gitattributes` edits.

## Tests/checks passed

| When                                    | Result                |
|-----------------------------------------|-----------------------|
| Pre-runner (after R3 unit tests added)  | **404 passed** / 11.34 s (was 396 + 8 new R3 tests) |
| Post-runs                               | unchanged (no source changes after the runs)        |
| Pre-Gate-2 (first submission)           | **404 passed**                                       |
| Pre-Gate-2 (after regime-classifier fix; analysis-script-only, no src change) | **404 passed** / 11.13 s |
| After commit 1 (R3 implementation + tests) | **404 passed** (expected)                          |
| After commit 2 (runner + analysis)         | **404 passed** (expected)                          |
| After commit 3 (comparison report + Gate 2)| **404 passed** (expected)                          |
| After commit 4 (this) — expected           | **404 passed**                                     |

`uv run ruff check .` ✓, `uv run ruff format --check .` ✓ (120 files), `uv run mypy` ✓ (49 source files; scripts are out of mypy default scope per the existing project configuration, consistent with Phase 2g pattern).

## Tests/checks failed

None.

## Runtime output

Backtest run output captured under git-ignored `data/derived/backtests/phase-2l-*/` directories:

| Run dir                                                                                  | Variant | Window | Knobs                  | Headline                                                                            |
|------------------------------------------------------------------------------------------|---------|--------|------------------------|-------------------------------------------------------------------------------------|
| `phase-2l-h0-r/2026-04-26T18-12-46Z/`                                                    | H0      | R      | MED slip / MARK_PRICE  | BTC 33 / 30.30% / −0.459 / 0.255 / −3.39% / −3.67% — matches Phase 2g/2k baseline    |
| `phase-2l-r3-r/2026-04-26T18-13-21Z/`                                                    | R3      | R      | MED slip / MARK_PRICE  | BTC 33 / 42.42% / −0.240 / 0.560 / −1.77% / −2.16% — PROMOTES                        |
| `phase-2l-h0-v/2026-04-26T18-15-22Z/`                                                    | H0      | V      | MED slip / MARK_PRICE  | BTC 8 / 25.00% / −0.313 / 0.541 / −0.56% / −0.87% — V control                        |
| `phase-2l-r3-v/2026-04-26T18-15-33Z/`                                                    | R3      | V      | MED slip / MARK_PRICE  | BTC 8 / 25.00% / −0.287 / 0.580 / −0.51% / −1.06% — direction-of-improvement holds   |
| `phase-2l-r3-r-slip=LOW/2026-04-26T18-15-51Z/`                                           | R3      | R      | LOW slip               | BTC 33 / 45.45% / −0.139 / 0.719 / −1.02% / −1.46% — best-case sensitivity            |
| `phase-2l-r3-r-slip=HIGH/2026-04-26T18-16-02Z/`                                          | R3      | R      | HIGH slip              | BTC 33 / 30.30% / −0.445 / 0.359 / −3.29% / −3.69% — still beats H0-at-MED            |
| `phase-2l-r3-r-stop=TRADE_PRICE/2026-04-26T18-16-13Z/`                                   | R3      | R      | TRADE_PRICE trigger    | bit-identical to MARK_PRICE — zero gap-through stops                                  |

Each run directory contains the per-symbol `trade_log.{parquet,json}`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `summary_metrics.json`, `funnel_total.json`, `monthly_breakdown.parquet`, `yearly_breakdown.parquet`, plus the run-level `backtest_report.manifest.json` and `config_snapshot.json`. None committed (git-ignored under `data/`).

## Known gaps

**No new GAP entries logged in this phase.** Phase 2l carries forward existing GAPs per Phase 2k Gate 1 plan §16; none requires update because Phase 2l's runs honor the existing dispositions exactly. Pre-existing dispositions:

- GAP-20260420-028 OPEN-LOW (v002 manifest predecessor_version metadata) — unchanged.
- GAP-20260419-018 / 020 / 024 ACCEPTED_LIMITATION (Phase 2e endpoint deferrals) — unchanged.
- GAP-20260420-029 RESOLVED (Phase 2e fundingRate Option C) — unchanged.
- GAP-20260424-030 OPEN — was previously flagged for "SUPERSEDED-on-execution when R3 advances per Phase 2j memo §D.16". The R3 execution that triggers the supersession has now happened; per operator Gate 2 approval (§ "GAP-20260424-030 ambiguity-log disposition does not need to block Phase 2l closure. Defer it unless you want a tiny follow-up docs-only commit."), the disposition update is **deferred**. The status remains OPEN until a future docs-only follow-up commit (or a Phase 2m ambiguity-log housekeeping pass) marks it SUPERSEDED.
- GAP-20260424-031 OPEN — CARRIED. R3 does not touch the bias rule; the EMA-slope discrete-comparison convention from Phase 2g is preserved.
- GAP-20260424-032 OPEN — CARRIED-AND-EXTENDED. R3's TRADE_PRICE sensitivity report cut produced; bit-identical to MARK_PRICE on the R window with zero gap-through stops.
- GAP-20260424-033 OPEN — CARRIED-AND-EXTENDED. R3's unconditional time-stop interpretation is implemented in `_fixed_r_time_stop_decision` exactly per §D.10; no MFE gate; semantically distinct from H0 STAGNATION (which has an MFE gate). The unit test `test_R3_time_stop_at_8_bars_unconditional` exercises this contract.
- GAP-20260424-034 / 035 RESOLVED verification-only (Phase 2f) — unchanged.
- GAP-20260424-036 RESOLVED-by-convention (fold scheme; Phase 2h). R3 fold analysis applied the convention exactly: 5 rolling folds, fold 1 partial-train front edge, all tests inside R.

## Spec ambiguities found

None new. The Gate 2 first submission used a trade-duration proxy as the "per-regime expR" diagnostic; the operator returned NOT-YET-APPROVED with the realized-1h-volatility regime-classification correction required. This was a reporting / diagnostic mislabeling, not a spec ambiguity — the Phase 2i / 2j / 2k validation framework had specified realized 1h volatility regime as the required form; the corrected analysis applied trailing 1000 1h-bar window of Wilder ATR(20) with tercile cutoffs at 33% / 67%. The verdict from the corrected diagnostic stays PROMOTE; R3 improves expR in all six regime-symbol cells.

## Technical-debt updates needed

None made in 2l (operator restriction). The Phase 2l execution evidence is informational input for any future operator review of TD-016 (statistical live-performance thresholds): R3's R-window expR (BTC −0.240, ETH −0.351), V-window confirmation (BTC −0.287, ETH −0.093), per-regime decomposition, and slippage / stop-trigger sensitivity all inform the eventual TD-016 threshold determination. The register itself stays untouched until the operator explicitly lifts the Phase 2f restriction.

## Safety constraints verified

| Check                                                        | Result |
|--------------------------------------------------------------|--------|
| Production Binance keys                                      | none   |
| Exchange-write code                                          | none   |
| REST / WebSocket / authenticated endpoints                   | none   |
| Credentials / `.env`                                         | none   |
| `.mcp.json`                                                  | absent |
| Graphify                                                     | disabled |
| MCP servers                                                  | not activated |
| Manual trading controls                                      | none   |
| Strategy structural changes                                  | R3 only — exit-machinery only; entry pipeline unchanged       |
| Risk framework changes                                       | none   |
| Dataset / manifest changes                                   | none   |
| Cost-model changes                                           | none (slippage applied via existing buckets; no fee-rate change) |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (`data/derived/backtests/phase-2l-*` git-ignored as designed) |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction)                                       |
| Phase 2e baseline run dir untouched                          | yes (read-only diagnostic citation only)                          |
| Phase 2g run dirs untouched                                  | yes                                                                |
| Wave-1 result preserved                                      | yes (REJECT ALL stands; no re-derivation)                          |
| Phase 2h provisional recommendation preserved                | yes (input, not target for revision)                               |
| Phase 2i / 2j / 2k specs preserved                           | yes (R3 sub-parameter values committed singularly; no sweeps)      |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds             | unchanged                                                          |
| §1.7.3 project-level locks                                   | preserved                                                          |
| H0 bit-for-bit preservation under default config             | enforced and verified (test + numerical baseline match)            |
| `--no-verify` / hook skipping                                | not used                                                           |
| `git push`                                                   | not used (operator restriction; "do not push yet")                 |
| Phase 4 work                                                 | none (operator restriction)                                        |
| Fallback Wave 2 / H-D6 start                                 | none (operator restriction; superseded by R3 PROMOTE)              |
| Phase 2m R1a execution                                       | none (operator restriction; "do not start Phase 2m yet")           |
| R1a work in any form                                         | none                                                                |
| Disguised parameter sweeps                                   | none (single committed value per R3 sub-parameter)                  |
| Wave-1 variant revival                                       | none                                                                |
| Live deployment / paper / shadow / tiny-live readiness claim | none                                                                |
| Pre-existing 404 tests pass                                  | yes (every commit)                                                  |

## Current runtime capability

Research-only, unchanged from end of Phase 2k. No runtime process, no dry-run adapter state, no user-stream connectivity. The project can run the backtest CLI against the v002 datasets for H0 or any approved variant (H0 baseline; Phase 2g wave-1 variants H-A1/H-B2/H-C1/H-D3; Phase 2l R3); no capability was added or removed in 2l beyond the R3 strategy variant being available via `V1BreakoutConfig(exit_kind=ExitKind.FIXED_R_TIME_STOP, ...)`.

## Exchange connectivity status

Zero. No authenticated endpoints contacted. No public endpoints contacted.

## Exchange-write capability status

Disabled by design. No exchange adapter present, no order-placement code path, no credentials available.

## Recommended next step (proposal only — operator decides)

Per Gate 2 approval and the comparison report §11.1, the **recommended next phase is Phase 2m — R1a structural redesign execution, with R3 locked as the exit baseline**. The base config for Phase 2m would be `V1BreakoutConfig(exit_kind=ExitKind.FIXED_R_TIME_STOP, exit_r_target=2.0, exit_time_stop_bars=8)` plus the R1a-specific setup-validity-percentile change (X = 25, N = 200 per Phase 2j §C.6 + Phase 2k §11.B / §13).

Phase 2m would test whether the percentile trigger (the dominant 58% no-valid-setup funnel rejection target) produces additional improvement on top of R3, or whether R3 alone captured the available edge. The same Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework, the same v002 datasets, the same per-fold convention (GAP-036), the same H0-only anchor (per Phase 2i §1.7.3) all apply unchanged.

Phase 2m is **not yet started**. The operator-approved Phase 2l closure does not authorize Phase 2m initiation; that is a separate Gate 1 / Gate 2 cycle.

**Phase 4 stays deferred** per operator policy. Phase 2l does not propose advancing it.

## Question for ChatGPT / operator

None. Phase 2l is complete. All operator brief content requirements applied; the regime-diagnostic correction was applied within the Gate 2 review cycle; all process requirements honored; pytest is at 404 throughout; no new GAP entries needed; the Gate 2 approval explicitly noted: "GAP-20260424-030 ambiguity-log disposition does not need to block Phase 2l closure" (deferred as a future tiny follow-up if the operator wants it). The branch `phase-2l/R3-first-execution` is complete and not yet pushed per operator restriction. Awaiting the operator's next-boundary decision: Phase 2m planning, a docs-only follow-up to mark GAP-030 SUPERSEDED, or other.
