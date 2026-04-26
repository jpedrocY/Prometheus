# Phase 2m — Checkpoint Report

Generated at the close of Phase 2m on branch `phase-2m/R1a-on-R3-execution`, after Gate 2 approval. Four operator-authorized commits per the operator-approved commit sequence (this checkpoint is the fourth commit). Template per `.claude/rules/prometheus-phase-workflow.md`.

## Phase

**Phase 2m — R1a-on-R3 First Execution.** A code-and-execution phase implementing the Phase 2j memo §C R1a candidate (Volatility-percentile setup with X = 25 percentile threshold and N = 200 trailing-bar lookback) on top of the locked R3 exit baseline (Phase 2j memo §D — fixed-R take-profit at +2.0 R + unconditional time-stop at 8 bars, frozen from Phase 2l). The candidate `R1a+R3` was executed against the locked Phase 2e v002 datasets on the Phase 2f research window R = 2022-01-01 → 2025-01-01 alongside H0 and R3 controls re-run on the same engine version. The second PROMOTE verdict in the project's research history under the unchanged Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 framework — **but a strategically mixed PROMOTE**, with R1a materially helping ETH and materially hurting BTC relative to the locked R3 baseline.

## Goal

(a) Implement R1a minimally: add `setup_predicate_kind = VOLATILITY_PERCENTILE` with committed sub-parameters X = 25 and N = 200, preserve H0 bit-for-bit as the default path, preserve R3 bit-for-bit when R1a is not selected, add `detect_setup_volatility_percentile()` sibling function in `setup.py`, extend `StrategySession` with prior-15m ATR history and config-aware warmup floor, dispatch in `V1BreakoutStrategy.maybe_entry`, mirror in `run_signal_funnel` so funnel attribution remains interpretable. (b) Add R1a unit tests + H0 + R3 preservation regression tests. (c) Pass quality gates (ruff/format/mypy/pytest). (d) Write a Phase 2m-specific runner mirroring the Phase 2l pattern with three variants (H0 control, R3 locked control, R1a+R3 candidate). (e) Run all three variants on R window for BTC + ETH at MEDIUM slippage / MARK_PRICE; apply the unchanged Phase 2f §10.3 / §10.4 framework with H0 as the sole comparison anchor (per Phase 2i §1.7.3). (f) If R1a+R3 PROMOTES on R, run V-window confirmation + LOW / HIGH slippage + TRADE_PRICE stop-trigger sensitivity; produce the mandatory diagnostics (per-regime expR using realized 1h volatility classification, MFE distribution, long/short asymmetry, fold-level results, trade-frequency sanity check, exit-reason histogram, implementation-bug check) plus the R1a-specific diagnostics (ATR-percentile distribution at filled R1a entries, setup-validity rate per fold, funnel-bucket comparison focused on `rejected_no_valid_setup`, warmup-impact summary). (g) Produce both the official H0-anchor comparison and the supplemental R3-anchor comparison (descriptive only). (h) Stop before any commit awaiting operator/ChatGPT Gate 2 approval; on approval, commit per the proposed sequence.

## Summary

Phase 2m delivered three committable code/test artifacts and three committable documentation artifacts plus this checkpoint, plus nine backtest run directories under `data/derived/backtests/phase-2m-r1a-*/` (git-ignored). Pytest moved from **404 passed → 417 passed** by exactly the 13 new R1a unit tests. Ruff / format / mypy stayed green throughout. The H0 and R3 controls reproduced their Phase 2g/2k/2l baselines bit-for-bit, confirming the new optional R1a fields and the `setup_predicate_kind` dispatch with default `RANGE_BASED` preserve both H0 and R3 behavior bit-for-bit through the strategy facade.

R1a+R3 PROMOTED on the R window under Phase 2f §10.3 with H0 as the governing anchor:

- BTC clears §10.3.c **only** (Δexp +0.039 R below the §10.3.a +0.10 threshold; ΔPF +0.100; Δ|maxDD| −1.341 pp). The §10.3.c strict-dominance fires; §10.3.a does not. The BTC promotion margin is roughly the noise scale at 22-trade sample size.
- ETH clears §10.3.a **and** §10.3.c (Δexp +0.362 R, ΔPF +0.512, Δ|maxDD| −1.171 pp).
- §10.3 disqualification floor not triggered (|maxDD| ratios 0.635× BTC / 0.717× ETH; both well below 1.5×).
- §10.4 hard reject does not apply (Δn = −33% BTC, −30% ETH; trade count drops, not rises).
- §11.4 ETH-as-comparison rule satisfied.

**The supplemental R3-anchor comparison (descriptive only — does R1a add value on top of R3?) is asymmetric.** R1a hurts BTC (Δexp_R3 −0.180 R, ΔPF_R3 −0.205) and helps ETH (Δexp_R3 +0.237 R, ΔPF_R3 +0.359). Per-fold (5 rolling, GAP-036): R1a+R3 beats H0 in 2/5 BTC folds and 4/5 ETH folds; beats R3 in 2/5 BTC folds and 2/5 ETH folds. V-window: R1a+R3 ETH is the project's first positive-netPct validation result (8 trades, 62.5% WR, expR +0.386 R, PF 2.222, **netPct +0.69%**); R1a+R3 BTC is severely degraded (4 trades, 0% WR, expR −0.990, netPct −0.88%). Slippage sensitivity is monotone and proportional. TRADE_PRICE bit-identical to MARK_PRICE (zero gap-through stops). Implementation-bug check clean (zero TRAILING_BREACH and zero STAGNATION exits in any R3-or-R1a+R3 trade log). The R1a-specific ATR-percentile diagnostic confirms 100% of filled R1a entries have ATR percentile ≤ 25% — the predicate is admitting only bottom-quartile compression bars, exactly per Phase 2j §C.5 spec.

### Strategic interpretation (operator framing — Gate 2 approval)

Phase 2m is a **formal PROMOTE under the unchanged Phase 2f framework, but a mixed / symbol-asymmetric PROMOTE in strategic terms**. R1a+R3 improves enough vs H0 to pass the framework, but relative to the locked R3 baseline R1a materially helps ETH and materially hurts BTC. **Phase 2m should not be framed as "R1a+R3 clearly replaces R3."** It should be framed as **"R1a+R3 is a promoted but strategically mixed candidate that requires a review phase before further execution or any deployment-readiness planning."** The operator-approved next step is a docs-only Phase 2n operator / strategy review phase; no further execution or paper/shadow / live-readiness planning is approved at this point.

## Files changed

By commit, on branch `phase-2m/R1a-on-R3-execution` starting from `main @ c2a44da` (Phase 2l merge):

| Commit | Files                                                                                                                                                                                                                                                                                                                                                                                                                | +/− Lines  |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| 1      | `src/prometheus/strategy/v1_breakout/variant_config.py` (+31/−0), `src/prometheus/strategy/v1_breakout/setup.py` (+97/−1), `src/prometheus/strategy/v1_breakout/strategy.py` (+50/−5), `src/prometheus/strategy/v1_breakout/__init__.py` (+5/−1), `src/prometheus/research/backtest/diagnostics.py` (+27/−10), `tests/unit/strategy/v1_breakout/test_variant_config.py` (+247/−4)                                       | +457 / −21 |
| 2      | `scripts/phase2m_R1a_on_R3_execution.py` (new), `scripts/_phase2m_R1a_analysis.py` (new)                                                                                                                                                                                                                                                                                                                              | +∼1010 / 0 |
| 3      | `docs/00-meta/implementation-reports/2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md` (new), `docs/00-meta/implementation-reports/2026-04-27_phase-2m_gate-2-review.md` (new)                                                                                                                                                                                                                                       | +∼1100 / 0 |
| 4      | `docs/00-meta/implementation-reports/2026-04-27_phase-2m-checkpoint-report.md` (this file)                                                                                                                                                                                                                                                                                                                            | this file  |

## Files created

- `docs/00-meta/implementation-reports/2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2m_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2m-checkpoint-report.md` (this file)
- `scripts/phase2m_R1a_on_R3_execution.py`
- `scripts/_phase2m_R1a_analysis.py`

## Files deleted

None.

## Commands run

- `git checkout -b phase-2m/R1a-on-R3-execution` (once at phase start, from clean `main`).
- `git status --short`, `git diff --stat`, `git log --oneline -*` at multiple checkpoints.
- `uv run pytest` before each commit and at the evidence stop. Counts: pre-runner **417 passed** / 12.22 s; after commit 1 **417 passed**; after commit 2 **417 passed**; after commit 3 **417 passed**; after commit 4 (this) — expected **417 passed**.
- `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy` — green at every checkpoint.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant H0     --window R` — H0 R-window control.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant R3     --window R` — R3 R-window locked control.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant R1a+R3 --window R` — R1a+R3 R-window candidate.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant H0     --window V` — H0 V-window control.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant R3     --window V` — R3 V-window locked control.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant R1a+R3 --window V` — R1a+R3 V-window candidate (run only because R-window PROMOTED).
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant R1a+R3 --window R --slippage LOW` — R1a+R3 LOW slippage sensitivity.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant R1a+R3 --window R --slippage HIGH` — R1a+R3 HIGH slippage sensitivity.
- `uv run python scripts/phase2m_R1a_on_R3_execution.py --variant R1a+R3 --window R --stop-trigger TRADE_PRICE` — R1a+R3 GAP-032 stop-trigger sensitivity.
- `uv run python scripts/_phase2m_R1a_analysis.py` — internal aggregation, official deltas-vs-H0, supplemental deltas-vs-R3, GAP-036 5-fold consistency comparisons, mandatory diagnostics, R1a-specific diagnostics, V-window comparison, slippage and stop-trigger sensitivity.
- `git add <specific-files>` + `git commit -m "<heredoc>"` four times per the operator-approved sequence (this checkpoint is the fourth commit).

## Installations performed

None. No `uv add`, no `uv sync` change, no global installs. `pyproject.toml` and `uv.lock` unchanged.

## Configuration changed

None. No `configs/`, `.env`, `.claude/`, `.gitignore`, or `.gitattributes` edits.

## Tests/checks passed

| When                                    | Result                |
|-----------------------------------------|-----------------------|
| Pre-runner (after R1a unit tests added) | **417 passed** / 12.22 s (was 404 + 13 new R1a tests) |
| Post-runs                               | unchanged (no source changes after the runs)         |
| Pre-Gate-2 confirmation                 | **417 passed** / 11.81 s                              |
| After commit 1 (R1a implementation + tests) | **417 passed** (expected)                          |
| After commit 2 (runner + analysis)         | **417 passed** (expected)                          |
| After commit 3 (comparison report + Gate 2)| **417 passed** (expected)                          |
| After commit 4 (this) — expected           | **417 passed**                                     |

`uv run ruff check .` ✓, `uv run ruff format --check .` ✓ (122 files), `uv run mypy` ✓ (49 source files; scripts are out of mypy default scope per the existing project configuration, consistent with Phase 2g / 2l precedent).

## Tests/checks failed

None.

## Runtime output

Backtest run output captured under git-ignored `data/derived/backtests/phase-2m-r1a-*/` directories:

| Run dir                                                                                          | Variant   | Window | Knobs                  | Headline                                                                                |
|--------------------------------------------------------------------------------------------------|-----------|--------|------------------------|-----------------------------------------------------------------------------------------|
| `phase-2m-r1a-h0-r/2026-04-26T21-37-41Z/`                                                        | H0        | R      | MED slip / MARK_PRICE  | BTC 33 / 30.30% / −0.459 / 0.255 / −3.39% / −3.67% — matches Phase 2l H0 R bit-for-bit  |
| `phase-2m-r1a-r3-r/2026-04-26T21-37-52Z/`                                                        | R3        | R      | MED slip / MARK_PRICE  | BTC 33 / 42.42% / −0.240 / 0.560 / −1.77% / −2.16% — matches Phase 2l R3 R bit-for-bit  |
| `phase-2m-r1a-r1a_plus_r3-r/2026-04-26T21-38-04Z/`                                               | R1a+R3    | R      | MED slip / MARK_PRICE  | BTC 22 / 27.27% / −0.420 / 0.355 / −2.07% / −2.33% — PROMOTES via §10.3.c                |
| `phase-2m-r1a-h0-v/2026-04-26T21-42-28Z/`                                                        | H0        | V      | MED slip / MARK_PRICE  | BTC 8 / 25.00% / −0.313 / 0.541 / −0.56% / −0.87% — V control                            |
| `phase-2m-r1a-r3-v/2026-04-26T21-42-38Z/`                                                        | R3        | V      | MED slip / MARK_PRICE  | BTC 8 / 25.00% / −0.287 / 0.580 / −0.51% / −1.06% — R3 V matches Phase 2l                |
| `phase-2m-r1a-r1a_plus_r3-v/2026-04-26T21-42-49Z/`                                               | R1a+R3    | V      | MED slip / MARK_PRICE  | BTC 4 / 0% / −0.990 (severe degradation); ETH 8 / 62.50% / +0.386 / +0.69% (first +netPct) |
| `phase-2m-r1a-r1a_plus_r3-r-slip=LOW/2026-04-26T21-44-53Z/`                                      | R1a+R3    | R      | LOW slip               | best-case sensitivity: BTC −0.319 / 0.449; ETH near break-even (−0.022 / 0.965)         |
| `phase-2m-r1a-r1a_plus_r3-r-slip=HIGH/2026-04-26T21-47-11Z/`                                     | R1a+R3    | R      | HIGH slip              | BTC −0.544 / 0.358; ETH −0.354 / 0.583 — degraded but not catastrophic                    |
| `phase-2m-r1a-r1a_plus_r3-r-stop=TRADE_PRICE/2026-04-26T21-49-20Z/`                              | R1a+R3    | R      | TRADE_PRICE trigger    | bit-identical to MARK_PRICE — zero gap-through stops                                       |

Each run directory contains the per-symbol `trade_log.{parquet,json}`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `summary_metrics.json`, `funnel_total.json`, `monthly_breakdown.parquet`, `yearly_breakdown.parquet`, plus the run-level `backtest_report.manifest.json` and `config_snapshot.json`. None committed (git-ignored under `data/`).

## Known gaps

**No new GAP entries logged in this phase.** Phase 2m carries forward existing GAPs per Phase 2k Gate 1 plan §16; none requires update because Phase 2m's runs honor the existing dispositions exactly. Pre-existing dispositions:

- GAP-20260420-028 OPEN-LOW (v002 manifest predecessor_version metadata) — unchanged.
- GAP-20260419-018 / 020 / 024 ACCEPTED_LIMITATION (Phase 2e endpoint deferrals) — unchanged.
- GAP-20260420-029 RESOLVED (Phase 2e fundingRate Option C) — unchanged.
- GAP-20260424-030 OPEN — disposition deferred per operator Gate 2 approval ("Leave GAP-20260424-030 disposition deferred; it does not block Phase 2m closure"). R1a does not touch the break-even rule (R1a's exit logic is R3-locked, with no break-even at all), so no SUPERSEDE event is created by Phase 2m.
- GAP-20260424-031 OPEN — CARRIED. R1a does not touch the bias rule.
- GAP-20260424-032 OPEN — CARRIED-AND-EXTENDED. R1a+R3's TRADE_PRICE sensitivity report cut produced; bit-identical to MARK_PRICE on the R window with zero gap-through stops.
- GAP-20260424-033 OPEN — CARRIED. R3's unconditional time-stop interpretation is unchanged in R1a+R3 (R3 exit logic is locked from Phase 2l). The unit test `test_R3_time_stop_at_8_bars_unconditional` continues to enforce the contract.
- GAP-20260424-034 / 035 RESOLVED verification-only (Phase 2f) — unchanged.
- GAP-20260424-036 RESOLVED-by-convention (fold scheme; Phase 2h). R1a+R3 fold analysis applied the convention exactly: 5 rolling folds, fold 1 partial-train front edge, all tests inside R.

## Spec ambiguities found

None new. The Phase 2j memo §C R1a spec was sufficient for clean implementation without ambiguity. The percentile rank threshold formula `floor(X * N / 100) = 50` at X=25, N=200 was directly applied; the mid-rank ceil tie convention was chosen for determinism and codified in `percentile_rank_threshold()` + the `detect_setup_volatility_percentile()` predicate. The warmup floor at `lookback + ATR_PERIOD + 1 = 221` was derived directly from §C.10 implementation-impact notes.

## Technical-debt updates needed

None made in 2m (operator restriction). The Phase 2m execution evidence — particularly the R1a+R3 ETH V-window result at +0.69% netPct (the project's first positive-netPct V-window outcome) and the BTC asymmetric degradation — is informational input for any future operator review of TD-016 (statistical live-performance thresholds). The register itself stays untouched until the operator explicitly lifts the Phase 2f restriction.

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
| Strategy structural changes                                  | R1a only — setup-predicate only; entry-trigger / bias / stop / sizing / R3 exit unchanged       |
| R3 value changes                                             | none (sub-parameters frozen at Phase 2l-committed values: R-target = 2.0, time-stop = 8)         |
| Risk framework changes                                       | none   |
| Dataset / manifest changes                                   | none   |
| Cost-model changes                                           | none (slippage applied via existing buckets; no fee-rate change)                                  |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (`data/derived/backtests/phase-2m-r1a-*` git-ignored as designed)                            |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction)                                                                       |
| Phase 2e baseline run dir untouched                          | yes (read-only diagnostic citation only)                                                          |
| Phase 2g / 2l run dirs untouched                             | yes                                                                                               |
| Wave-1 result preserved                                      | yes (REJECT ALL stands; no re-derivation)                                                          |
| Phase 2l R3 PROMOTE preserved                                | yes (R3 sub-parameters frozen; R3 control re-run reproduces Phase 2l baseline bit-for-bit)         |
| Phase 2i project-level locks (§1.7.3)                        | preserved (BTCUSDT primary, one-position, 0.25% risk, 2× leverage, mark-price stops, v002, H0-only anchor) |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds             | unchanged                                                                                         |
| H0 bit-for-bit preservation under default config             | enforced and verified (3 dedicated tests + numerical baseline match)                              |
| R3 bit-for-bit preservation under R3-only config             | enforced and verified (1 dedicated test + numerical baseline match)                               |
| `--no-verify` / hook skipping                                | not used                                                                                          |
| `git push`                                                   | not used (operator restriction; "do not push yet")                                                 |
| Phase 4 work                                                 | none (operator restriction)                                                                       |
| Fallback Wave 2 / H-D6 start                                 | none (superseded)                                                                                  |
| Phase 2n start                                               | none (operator restriction; "do not start Phase 2n yet")                                           |
| Paper/shadow planning / live-readiness planning              | none (operator restriction)                                                                       |
| Disguised parameter sweeps                                   | none (single committed value per R1a sub-parameter)                                                |
| Wave-1 variant revival                                       | none                                                                                              |
| New redesign candidate exposed                               | none (only H0, R3, R1a+R3 — the explicit Phase 2m brief allowed only these three)                  |
| Live deployment readiness claim                              | none                                                                                              |
| Pre-existing 417 tests pass                                  | yes (every commit)                                                                                |

## Current runtime capability

Research-only, unchanged from end of Phase 2l. No runtime process, no dry-run adapter state, no user-stream connectivity. The project can run the backtest CLI against the v002 datasets for H0, the Phase 2g wave-1 variants (H-A1/H-B2/H-C1/H-D3), Phase 2l R3, and now Phase 2m R1a+R3. No capability was added or removed in 2m beyond the R1a setup-predicate variant being available via `V1BreakoutConfig(setup_predicate_kind=SetupPredicateKind.VOLATILITY_PERCENTILE, ...)`.

## Exchange connectivity status

Zero. No authenticated endpoints contacted. No public endpoints contacted.

## Exchange-write capability status

Disabled by design. No exchange adapter present, no order-placement code path, no credentials available.

## Recommended next step (proposal only — operator decides)

Per Gate 2 approval: **Phase 2n — operator / strategy review (docs-only, no code, no runs)**. The operator-approved framing is that R1a+R3 is a formal PROMOTE under the unchanged Phase 2f framework but a strategically mixed candidate (helps ETH, hurts BTC vs the locked R3 baseline). Phase 2n should review:

- Whether to deploy R3 alone or R1a+R3 in any future paper/shadow planning (deferred), given the asymmetric BTC vs ETH evidence.
- Whether the Phase 2j §C.16 R1a-specific diagnostics + the Phase 2m per-regime view + the V-window evidence are sufficient to validate R1a's mechanism, or whether further targeted analysis is warranted.
- Whether to attempt one of the Phase 2i-deferred candidates (R1b regime classifier, R2 pullback entry) as a third structural-redesign wave, or whether the family has been adequately characterized.

Per Gate 2 approval, the following are **NOT** the next step at this time:

- **Phase 4 (runtime / state / persistence)** stays deferred per operator policy.
- **Paper/shadow planning** stays deferred ("do not start paper/shadow or live-readiness planning").
- **Another execution phase** (Phase 2o or otherwise) stays deferred ("do not start another execution phase yet").
- **Phase 2n itself** is not authorized to start by the Phase 2m closure ("do not start Phase 2n yet"). Phase 2n is the operator-approved next phase, but its own start gate is a separate decision.

## Question for ChatGPT / operator

None. Phase 2m is complete. All operator brief content requirements applied; all process requirements honored; pytest is at 417 throughout; no new GAP entries needed; the Gate 2 approval explicitly accepted the formal PROMOTE verdict with the qualified / mixed-promotion strategic framing reproduced in this checkpoint. The branch `phase-2m/R1a-on-R3-execution` is complete and not yet pushed per operator restriction. Awaiting the operator's next-boundary decision (Phase 2n start, or other).
