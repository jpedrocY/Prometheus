# Phase 3j — Closeout Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1; Phase 2y closeout (§11.6 = 8 bps HIGH preserved); Phase 3d-B2 precedent (F1 HARD REJECT); **Phase 3g D1-A spec memo + methodology audit (binding spec)**; **Phase 3h D1-A execution-planning memo (binding execution plan, with timing-clarification amendments)**; **Phase 3i-B1 engine wiring (binding implementation surface)**.

**Phase:** 3j — D1-A first-execution candidate phase. **Branch:** `phase-3j/d1a-execution-diagnostics`. **Date:** 2026-04-29 UTC.

**Status:** Phase 3j complete. Verdict **MECHANISM PASS / FRAMEWORK FAIL — other** (Phase 3h §11.2). D1-A retained as research evidence; non-leading; Phase 3j terminal for D1-A. **Awaiting operator review and merge.**

---

## 1. Phase 3j scope summary

Phase 3j is the **first real candidate-execution phase for the D1-A funding-aware directional / carry-aware strategy family**. It implements the Phase 3i-B1 runner-scaffold body, runs the precommitted Phase 3h §10 R-window inventory (4 mandatory cells), evaluates the Phase 3h §11 first-execution gate, computes the §12 M1 / M2 / M3 mechanism checks, gathers the §13 mandatory diagnostics, and validates the §14 P.14 hard-block invariants. No spec axes were modified; no successor variants authorized.

Phase 3j is analogous to Phase 3d-B2 in role (first real execution + first-execution-gate evaluation), but for D1-A instead of F1 and with a milder framework-fail outcome (no catastrophic-floor predicate violation).

## 2. Files changed

Modified:

- `scripts/phase3j_D1A_execution.py` — replaced Phase 3i-B1 scaffold body with the full F1-precedent-style D1-A run-loop. The `check-imports` subcommand output preserves the substring `"imports OK"` for backward compatibility with the existing Phase 3i-B1 test.

New:

- `scripts/_phase3j_D1A_analysis.py` — Phase 3j D1-A analysis script (gate / M1 / M2 / M3 / diagnostics / P.14 / cross-family / RR-breakeven). Reads only existing run artifacts + v002 normalized klines; writes a single git-ignored JSON output.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3j_D1A_execution-diagnostics.md` — full execution + diagnostics report (the primary Phase 3j artifact).
- `docs/00-meta/implementation-reports/2026-04-29_phase-3j_closeout-report.md` — this closeout.

NOT touched:

- `src/prometheus/research/backtest/engine.py`, `trade_log.py`, `config.py`, `accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py`, `report.py`.
- `src/prometheus/strategy/v1_breakout/**`, `src/prometheus/strategy/mean_reversion_overextension/**`, `src/prometheus/strategy/funding_aware_directional/**`.
- `tests/**` (no test changes; runner-scaffold check-imports test continues to pass).
- `docs/03-strategy-research/**`, `docs/05-backtesting-validation/**`, `docs/12-roadmap/**`, `docs/00-meta/current-project-state.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`.
- `data/` (zero `data/` artifacts staged — all run outputs under git-ignored directories).
- `.claude/`, `.mcp.json`, `config/`, `secrets/`.

Total non-`data/` files changed: **4** (1 modified + 3 new).

## 3. Quality gates (Phase 3j brief §1)

All four pre-execution gates green prior to any D1-A candidate run:

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **668 passed** in 12.10s |
| Linter | `uv run ruff check .` | **All checks passed!** |
| Formatter | `uv run ruff format --check .` | **157 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 61 source files** |

No regression. Test count unchanged from Phase 3i-B1 (668 passed) — Phase 3j adds the run-loop body + analysis script, both of which are exercised by the candidate-cell runs themselves; no new pytest unit tests were authored (per Phase 3h §15 governance, the engine-test surface was the Phase 3i-B1 deliverable and is preserved bit-for-bit).

## 4. Control reproduction (Phase 3j brief §1)

Full control set re-executed and compared against the most-recent committed Phase 3i-B1 baselines:

| Control | Window | Slippage | Stop trigger | Symbol | Reproduces |
|---------|--------|----------|--------------|--------|-----------|
| H0 | R | MED | MARK | BTC | **identical** (n=33) |
| H0 | R | MED | MARK | ETH | **identical** (n=33) |
| H0 | V | MED | MARK | BTC | **identical** (n=8) |
| H0 | V | MED | MARK | ETH | **identical** (n=14) |
| R3 | R | MED | MARK | BTC | **identical** (n=33) |
| R3 | R | MED | MARK | ETH | **identical** (n=33) |
| R3 | V | MED | MARK | BTC | **identical** (n=8) |
| R3 | V | MED | MARK | ETH | **identical** (n=14) |
| F1 | R | MED | MARK | BTC | **identical** (n=4720) |
| F1 | R | MED | MARK | ETH | **identical** (n=4826) |

Bit-for-bit on summary metrics + trade-log content (excluding random `trade_id` UUID suffix and NaN-equality semantics). The Phase 3j runner-loop body addition does not perturb V1 or F1 dispatch.

## 5. D1-A R-window inventory results

Per Phase 3h §10 (4 mandatory R-window cells; V conditional on PROMOTE).

| Cell | BTC trades | BTC expR | BTC PF | ETH trades | ETH expR | ETH PF |
|------|----------:|---------:|-------:|----------:|---------:|-------:|
| **R MED MARK** | 198 | **−0.3217** | **0.6467** | 179 | **−0.1449** | **0.8297** |
| R LOW MARK | 198 | −0.2423 | 0.7248 | 180 | −0.1168 | 0.8609 |
| **R HIGH MARK** | 197 | **−0.4755** | **0.5145** | 178 | **−0.2543** | **0.7217** |
| R MED TRADE_PRICE | 198 | −0.3703 | 0.6014 | 180 | −0.2222 | 0.7478 |

**No catastrophic-floor predicate violation.** A cell is non-catastrophic iff `expR > −0.50 AND PF > 0.30` (both conditions); equivalently, the catastrophic-floor predicate triggers iff `expR ≤ −0.50 OR PF ≤ 0.30`. All 4 R-window × 2 symbols cells satisfy the non-catastrophic conjunction on both metrics simultaneously. This is materially better than Phase 3d-B2 F1 (which tripped 5 catastrophic-floor violations producing HARD REJECT).

V MED MARK cell **NOT EXECUTED** — verdict was not PROMOTE.

## 6. Phase 3h §11 first-execution gate verdict

| Condition | Empirical | Pass? |
|-----------|-----------|------:|
| (i) BTC MED expR > 0 | −0.3217 | **FAIL** |
| (ii) M1 BTC h=32 PASS | mean +0.1748 R; fraction 0.5101 | **PASS** |
| (iii) ETH MED non-catastrophic | expR −0.1449 / PF 0.8297 | **PASS** |
| (iv) BTC HIGH cost-resilience | BTC HIGH expR −0.4755 (FAIL) | **FAIL** |
| (v) MED absolute floors | both symbols above floors | **PASS** |
| Catastrophic-floor predicate | none of 4 cells trip | **No** |

**Verdict: MECHANISM PASS / FRAMEWORK FAIL — other** (Phase 3h §11.2 mapping).

## 7. M1 / M2 / M3 mechanism summary

| Check | BTC | ETH | Threshold |
|-------|-----|-----|-----------|
| **M1** post-entry counter-displacement at h=32 (mean R / fraction ≥ 0) | +0.1748 / 0.5101 | +0.1670 / 0.5140 | mean ≥ +0.10 R AND fraction ≥ 0.50 |
| M1 verdict (BTC drives §11.1 (ii)) | **PASS** | (descriptive PASS) | — |
| **M2** funding-cost benefit (mean funding_pnl / realized_risk_usdt) | +0.00234 R | +0.00452 R | ≥ +0.05 R |
| M2 verdict | **FAIL** | **FAIL** | — |
| **M3** TARGET-exit subset (n / aggregate R / mean R) | 52 / +111.46 / +2.143 R | 49 / +119.89 / +2.447 R | mean ≥ +0.30 R AND aggregate > 0 |
| M3 verdict | **PASS** | **PASS** | — |

The mechanism (M1) IS empirically present — D1-A's post-extreme-funding contrarian entries do produce positive expected counter-displacement at the 32-bar horizon. The TARGET-exit subset (M3) is highly profitable when isolated. But the realized framework expectation fails because the win rate (~30%) is far below the +51% breakeven WR forecast — too many trades hit the −1.0R stop before reaching the +2.0R target. M2 (funding-cost benefit) fails clearly: BTC is ~21× below the +0.05R PASS threshold (+0.00234 R vs +0.05 R); ETH is ~11× below (+0.00452 R vs +0.05 R). Funding accrual does not offset costs.

## 8. RR / breakeven realized-vs-expected (Phase 3h §13 #24)

| Symbol | Empirical winner R | Empirical loser R | Empirical WR | Forecast breakeven WR | Gap |
|--------|------------------:|------------------:|-------------:|----------------------:|----:|
| BTC | +1.979 (vs +1.47 forecast) | −1.298 (vs −1.53 forecast) | 0.298 | 0.51 | −0.21 |
| ETH | +2.256 | −1.238 | 0.313 | 0.51 | −0.20 |

Per-trade R magnitudes are BETTER than forecast on both sides. But empirical WR is ~21 percentage points below the breakeven WR — the framework failure is a win-rate failure, not a per-trade R magnitude failure.

## 9. P.14 hard-block invariants (subset checkable from trade log)

| Invariant | BTC | ETH | Pass? |
|-----------|-----|-----|------:|
| Exit reasons in {STOP, TARGET, TIME_STOP, END_OF_DATA} | All 198 | All 179 | **PASS** |
| No V1-only forbidden exit reasons | 0 / 198 | 0 / 179 | **PASS** |
| `stop_distance_at_signal_atr` in [0.60, 1.80] | 1.000 | 1.000 | **PASS** |
| `funding_event_id_at_signal` populated | 198 / 198 | 179 / 179 | **PASS** |
| Lifecycle accounting identity | 201 = 198 + 0 + 3 ✓ | 188 = 179 + 0 + 9 ✓ | **PASS** |

The +2.0R target geometry is enforced by construction in the engine (`compute_d1a_target(fill_price, stop_distance=post_slip_stop_distance, target_r=2.0)` at `engine.py:2088`) — see diagnostics report §7 for the construction-level invariant; verified indirectly by M3 TARGET-subset mean R staying within +0.14R / +0.45R of the +2.0R nominal target.

## 10. Phase 3j terminal-for-D1-A status

Phase 3j is **terminal for D1-A** under Phase 3h §11 / §15 framework:

- **D1-A is retained as research evidence**, analogous to R1a / R1b-narrow / R2 / F1.
- **D1-A is non-leading.** R3 remains the V1 baseline-of-record. H0 remains the framework anchor.
- **No D1-A-prime, D1-B, or hybrid authorized.** Any successor variant requires a separately authorized phase per Phase 3h §15.
- **No further D1-A backtest cells authorized** (no LOW / TRADE_PRICE V-window cell; no alternative-axes cell; no M1 / M2 / M3 re-evaluation under modified spec).
- **No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write authorization** flows from this verdict.

The recommended next step per Phase 3h §15 framework is **operator-driven post-Phase-3j consolidation** (a docs-only memo analogous to Phase 3e's post-F1 consolidation). Phase 3j does NOT author this memo; it is reserved for an authorized Phase 3k or equivalent.

## 11. Confirmation of preserved scope

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| §11.6 = 8 bps HIGH per side | UNCHANGED |
| §1.7.3 project-level locks | UNCHANGED |
| H0 / R3 / R1a / R1b-narrow / R2 / F1 spec axes | UNCHANGED |
| **D1-A locked spec values** (Phase 3g binding) | **PRESERVED VERBATIM in `FundingAwareConfig`** |
| R3 baseline-of-record / H0 framework anchor | PRESERVED |
| R1a / R1b-narrow / R2 / F1 retained-research-evidence status | PRESERVED |
| F1 framework verdict (HARD REJECT) | PRESERVED |
| Phase 3d-B2 terminal-for-F1 | PRESERVED |
| **D1-A framework verdict (Phase 3j MECHANISM PASS / FRAMEWORK FAIL — other)** | **NEW** |
| **Phase 3j terminal-for-D1-A** | **NEW** |
| Paper/shadow planning / Phase 4 / live-readiness / deployment / production-key / exchange-write | NOT AUTHORIZED, NOT PROPOSED |
| MCP servers / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED (will be updated post-merge) |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

## 12. Phase 3j → main authority

Phase 3j is **NOT merged to main** by Phase 3j itself. Per the brief: "Commit non-data/ files; do not merge to main." The Phase 3j branch (`phase-3j/d1a-execution-diagnostics`) carries:

- 1 modified file (`scripts/phase3j_D1A_execution.py`)
- 3 new files (`scripts/_phase3j_D1A_analysis.py`; the diagnostics report; this closeout)

Awaiting operator review of the diagnostics report and explicit operator approval before any merge to main. No Phase 3k or post-Phase-3j consolidation memo is authored within Phase 3j.

---

**End of Phase 3j closeout report.** Phase 3j scope: D1-A first execution + diagnostics + first-execution-gate evaluation. Verdict: **MECHANISM PASS / FRAMEWORK FAIL — other**. M1 PASS, M2 FAIL, M3 PASS-isolated. No catastrophic-floor violation. V-window NOT executed. D1-A retained as research evidence; non-leading; no D1-A-prime authorized. Phase 3j terminal for D1-A. Quality gates green (668 pytest / ruff / format / mypy). Full control set reproduces bit-for-bit. Awaiting operator review.
