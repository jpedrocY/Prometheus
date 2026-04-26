# Phase 2g — Checkpoint Report

Generated at the close of Phase 2g on branch `phase-2g/wave1-variant-execution`, after Gate 2 approval (with the operator's fold-methodology correction and the post-Gate-2 hygiene fix to the Gate 2 review's §1 file description). Five commits + this checkpoint = six commits total. Template per `.claude/rules/prometheus-phase-workflow.md`.

## Phase

**Phase 2g — Wave-1 Variant Execution.** Implements four operator-approved single-axis variants of the locked v1 breakout strategy (H-A1 setup window 8 → 10, H-B2 expansion 1.0 → 0.75 × ATR20, H-C1 EMA pair 50/200 → 20/100, H-D3 break-even +1.5R → +2.0R) plus the H0 control, runs them on the Phase 2f research window R, computes Phase 2f §11.2 5-rolling-fold consistency metrics, applies the pre-declared §10.3 / §10.4 thresholds, and reports the verdict.

## Goal

(a) Add the minimal code needed to support the four named variants without changing structural strategy rules. (b) Preserve H0 baseline behavior bit-for-bit. (c) Run H-A1, H-B2, H-C1, H-D3 + H0 on R = 2022-01-01 → 2025-01-01 against the existing v002 datasets. (d) Apply the pre-declared promotion / disqualification thresholds without post-hoc tightening or loosening. (e) Run promoted candidates (top 1–2 only) on V = 2025-01-01 → 2026-04-01, with required slippage and stop-trigger sensitivity, *if any candidate clears*. (f) Produce a committed comparison report and Gate 2 review. No live capability. No new dataset. No threshold tuning.

## Summary

Phase 2g delivered the wired variant infrastructure, ran the wave on R, and produced the disciplined outcome of the pre-declared thresholds:

- A frozen `V1BreakoutConfig` with five fields threaded through the strategy package (setup-size, expansion-mult, EMA pair, break-even-R) and through the backtest engine (via `BacktestConfig.strategy_variant`). A new `BacktestConfig.stop_trigger_source` enum (default `MARK_PRICE`) implements the GAP-20260424-032 sensitivity hook. Defaults preserve H0 bit-for-bit; the existing 387-test baseline still passes; +9 new variant tests.
- `scripts/phase2g_variant_wave1.py` runner (one variant per invocation) and `scripts/_phase2g_wave1_analysis.py` read-only analysis helper.
- All four variants were run on R for both BTCUSDT and ETHUSDT; the H0 control was re-run on R for an apples-to-apples 36-month comparison (the Phase 2e FULL-window baseline run dir remains the permanent control, untouched).
- **All four variants disqualify on BTC under the pre-declared §10.3 floor.** H-A1 / H-C1 / H-D3 worsen expR and PF; H-B2 marginally exceeds the |maxDD| > 1.5× baseline veto (ratio 1.505x). H-B2 is the closest case but per Phase 2f §11.3.5 the threshold is binding and cannot be loosened.
- **Recommendation: REJECT ALL.** Per §11.3, V is reserved for top-1–2 promoted variants — with zero promoted, V was not run. Per §11.6 + §10.6, slippage and stop-trigger sensitivity sweeps are conditional on promotion — neither was run. The infrastructure for both is wired and exercised by the runner CLI; it is unused this wave by design.
- Gate 2 reviewer caught a methodology mismatch: the first draft used six non-overlapping half-year folds instead of Phase 2f §11.2's approved five rolling folds. The fold scheme was corrected before commit; the comparison report's §3 was rebuilt around the approved scheme and the half-year cut was demoted to a clearly-labeled supplemental appendix (§3.A). The §10.3 / §10.4 verdict (computed on the full R window per §11.3) is unchanged.
- A small post-Gate-2 hygiene fix (`six-fold breakdown` → `5 rolling-fold breakdown + supplemental 6-half-year appendix`) was applied to the Gate 2 review's §1 file description before the commit sequence.

## Files changed

By commit, on `phase-2g/wave1-variant-execution` starting from `main @ b37c75f` (Phase 2f merge):

| Commit | SHA       | Files                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | +Lines | −Lines |
|--------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------:|-------:|
| 1      | `0adb5f2` | `src/prometheus/strategy/v1_breakout/{variant_config.py (new), __init__.py, setup.py, trigger.py, management.py, strategy.py}`; `src/prometheus/research/backtest/{__init__.py, config.py, diagnostics.py, engine.py, stops.py}`; `tests/unit/strategy/v1_breakout/test_variant_config.py (new)`                                                                                                                                                                                          | +510   | −89    |
| 2      | `ce4ba65` | `scripts/phase2g_variant_wave1.py (new)`; `scripts/_phase2g_wave1_analysis.py (new)`                                                                                                                                                                                                                                                                                                                                                                                                  | +799   |   0    |
| 3      | `495928f` | `docs/00-meta/implementation-reports/2026-04-24_phase-2g_wave1_variant-comparison.md (new)`                                                                                                                                                                                                                                                                                                                                                                                            | +292   |   0    |
| 4      | `8eecdca` | `docs/00-meta/implementation-reports/2026-04-24_phase-2g_gate-2-review.md (new)`                                                                                                                                                                                                                                                                                                                                                                                                       | +213   |   0    |
| 5      | (this)    | `docs/00-meta/implementation-reports/2026-04-24_phase-2g-checkpoint-report.md (new)`                                                                                                                                                                                                                                                                                                                                                                                                   | this file |   0    |

## Files created

- `src/prometheus/strategy/v1_breakout/variant_config.py`
- `tests/unit/strategy/v1_breakout/test_variant_config.py`
- `scripts/phase2g_variant_wave1.py`
- `scripts/_phase2g_wave1_analysis.py`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2g_wave1_variant-comparison.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2g_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2g-checkpoint-report.md` (this file)

## Files deleted

None.

## Commands run

- `git checkout -b phase-2g/wave1-variant-execution` (once at phase start, from clean `main`).
- `git status --short`, `git diff --stat`, `git log --oneline -*` at multiple checkpoints.
- `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`, `uv run pytest` — green at every checkpoint and after every commit.
- `uv run python scripts/phase2g_variant_wave1.py --variant {H0, H-A1, H-B2, H-C1, H-D3} --window R` — five wave-1 R-window runs (one per variant, each ~10 seconds with the Phase 2e indicator-cache optimization).
- `uv run python scripts/_phase2g_wave1_analysis.py` — read-only analysis against the five run dirs; produced the §3 / §3.A fold tables and the §10.3 / §10.4 classification.
- `git add <specific-files>` + `git commit -m "<heredoc>"` five times so far for commits 1–5; commit 6 (this checkpoint) follows immediately.

## Installations performed

None. No `uv add`, no `uv sync` change, no global installs. `pyproject.toml` and `uv.lock` unchanged.

## Configuration changed

None at the project level. `BacktestConfig` gained two new optional fields (`strategy_variant`, `stop_trigger_source`) with safe defaults that reproduce the locked Phase 2e baseline. No `configs/`, `.env`, `.claude/`, or `.gitignore` edits.

## Tests/checks passed

| When                              | Result                |
|-----------------------------------|-----------------------|
| Pre-commit-1 (full surface ready) |  396 passed / 10.96s  |
| After commit 1 (source + tests)   |  396 passed / 10.98s  |
| After commit 2 (scripts)          |  396 passed / 10.97s  |
| After commit 3 (comparison)       |  396 passed / 11.00s  |
| After commit 4 (Gate 2 review)    |  396 passed / 11.03s  |
| After commit 5 (this) — expected  |  396 passed           |

`uv run ruff check .` — All checks passed (118 files).
`uv run ruff format --check .` — 118 files already formatted.
`uv run mypy` — Success: no issues found in 49 source files.

## Tests/checks failed

None.

## Runtime output

Engine runtime per variant on R (two symbols): ~10 seconds end-to-end thanks to the Phase 2e Wilder/EMA incremental indicator cache. Output artifacts under `data/derived/backtests/phase-2g-wave1-<variant>-r/<run_id>/<SYMBOL>/` are git-ignored and contain `trade_log.{parquet,json}`, `summary_metrics.json`, `funnel_total.json`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `monthly_breakdown.parquet`, `yearly_breakdown.parquet`, plus the run-level `backtest_report.manifest.json` and `config_snapshot.json`. No data was committed.

## Known gaps

- **GAP-20260424-032** (mark-price stop-trigger sensitivity) — implementation hook now wired (`StopTriggerSource` enum on `BacktestConfig`, engine routes to mark-price by default and to trade-price under the switch, `evaluate_stop_hit` parameter type relaxed). The hook is **available** for any future approved wave that produces a promoted variant; it is **unused this wave** because no candidate cleared §10.3.
- **Phase 2f §11.2 fold-scheme interpretation** — the spec says "five rolling folds, 12-month train / 6-month test, stepping 6 months on R." Strict interpretation (each fold has a full 12m train, step 6m, in 36m R) yields 4 folds; "5 folds" requires fold 1 to start at month 6 with a 6m partial-train front edge. Phase 2g uses the latter to honor the count. The supplemental §3.A 6-half-year appendix is provided for descriptive coverage of the months no §11.2 test fold reaches (2022-01..2022-06). No new GAP entry — this is documented inline rather than logged as a separate ambiguity.

No new GAP entries were appended in Phase 2g. `docs/00-meta/implementation-ambiguity-log.md` is unchanged.

## Spec ambiguities found

The fold-scheme interpretation noted above is the only spec-ambiguity-adjacent item that surfaced. It was resolved inline by selecting the interpretation that matches "5 folds" while keeping all tests inside R, and by adding a supplemental cut for the months excluded from any test fold.

## Technical-debt updates needed

None made in 2g (operator restriction). The wave-1 result (REJECT ALL) is informational input for any future operator review of TD-016 (statistical live-performance thresholds), but the register itself is not edited until the operator explicitly lifts the Phase 2f restriction.

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
| Strategy structural changes                                  | none — only Parametric-classified parameters threaded |
| Risk framework changes                                       | none — same `risk_fraction`, `max_leverage`, `notional_cap` |
| Dataset / manifest changes                                   | none — same v002 files as Phase 2e |
| Cost-model changes                                           | none — same taker / slippage / funding model |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none |
| `pyproject.toml` / `uv.lock` change                          | none |
| `data/` commits                                              | none (all run output remains git-ignored) |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction) |
| `docs/00-meta/implementation-ambiguity-log.md` edits         | none |
| Phase 2e baseline run dir untouched                          | yes (read-only access for diagnostics only) |
| H0 reproduces baseline behavior bit-for-bit                  | yes (tests + R-window subset trade counts) |
| Pre-existing 387 tests pass; +9 variant tests; total 396     | yes |
| Ruff / format / mypy green at every commit                   | yes |
| `--no-verify` / hook skipping                                | not used |
| `git push`                                                   | not used (operator restriction) |
| Phase 4 work                                                 | none (operator restriction) |
| Phase 2h or beyond                                           | none (operator restriction) |
| Extra variants beyond the four approved                      | none |
| Threshold tuning                                             | none |

## Current runtime capability

Research-only, unchanged from end of Phase 2f. No runtime process, no dry-run adapter state, no user-stream connectivity. The project can run the backtest CLI against the v002 datasets for H0 or any approved variant via the new runner — same read-only research surface, augmented only by the variant + stop-trigger switches.

## Exchange connectivity status

Zero. No authenticated endpoints contacted. No public endpoints contacted. v002 datasets read read-only from the existing `data/` tree.

## Exchange-write capability status

Disabled by design. No adapter loaded, no write path exercised.

## Recommended next step (proposal only — operator decides)

Three non-exclusive options follow from the wave-1 REJECT ALL result. Phase 2g does **not** start any of them; all three require an explicit fresh approval.

- **(a) Wave 2 (operator-approved hypothesis set).** Per Phase 2f Gate 1 §3.6 + §11.3.5, wave 2 is not implicit. If it is approved, the cleanest direction is a different setup-logic axis (H-A2 range-width ceiling 2.00 × ATR20, H-A3 drift cap 0.50) targeting the same dominant 58% "no valid setup" rejection without the trade-frequency collapse H-A1 produced. H-B2 paired with a tighter stop-distance band would be a bundled variant and requires explicit deviation from Phase 2f §9.1's one-change-at-a-time rule.
- **(b) Different research direction.** The wave-1 result suggests the locked v1 strategy's edge problem is not a parameter-tightness problem on these axes. A wave 2 might be the wrong frame; a different research direction (e.g., stop-loss policy variants per spec Open Q #6 / #7, or revisiting whether the breakout-continuation family is the right v1 family at all) would be a separate Phase 2f-style strategy-review work item.
- **(c) Phase 4 — risk / state / persistence runtime.** Independent of wave-1 results and does not block (a) or (b). The deferred-from-Phase-3 phase that builds the operational-safety core.

No recommendation is made among (a), (b), (c).

## Question for ChatGPT / operator

None. Phase 2g is complete. All operator restrictions and Phase 2f / Phase 2g approvals were honored. Pytest is at 396 throughout. Awaiting the next-boundary decision.
