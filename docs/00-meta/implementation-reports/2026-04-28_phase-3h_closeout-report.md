# Phase 3h — Closeout Report

**Phase:** 3h — Docs-only D1-A execution-planning memo (Phase-3c-style), with post-review docs-only timing-clarification amendment.

**Branch:** `phase-3h/d1-execution-planning`.

**Date:** 2026-04-28 UTC.

---

## 0. Post-review docs-only clarification amendment

After the initial Phase 3h commit, operator review surfaced two execution-plan timing details that needed unambiguous clarification before merge. A subsequent docs-only amendment to the Phase 3h execution-planning memo (and this closeout) addressed them, all without changing the D1-A locked spec values, thresholds, strategy parameters, project locks, or recommendations:

### 0.1 TARGET trigger/fill timing clarification

The original §5.6 said "check STOP > TARGET > TIME_STOP precedence at bar close; close position at next-bar open" while §7.2's `test_d1a_target_close_fill` test description said "If price reaches target during a bar, position closes with TARGET exit reason at the bar's close." This was internally inconsistent.

The amendment standardizes D1-A TARGET behavior across all sections:

- **TARGET trigger condition is completed-bar close confirmation** (LONG `close ≥ target_price`; SHORT `close ≤ target_price`).
- **TARGET fills at the next bar open**, never at the trigger bar's close.
- **No intrabar target-touch fill.** A bar whose high (LONG) or low (SHORT) touches `target_price` but whose completed close does NOT satisfy the trigger condition produces no TARGET exit; the position remains open.
- **No same-close TARGET fill.**
- **Same-bar priority remains STOP > TARGET > TIME_STOP**, evaluated on the completed bar; trigger evaluation is at bar close, fill is at next bar open.
- **STOP behavior unchanged** — retains the existing MARK_PRICE stop-trigger machinery; this clarification does not alter existing stop modeling.
- **TIME_STOP remains:** trigger at close of bar `B+1+32`; fill at open of bar `B+1+33`.

Updated sections: §5.6 (engine dispatch step 5); §7.2 (engine wiring tests — replaced `test_d1a_target_close_fill` with `test_d1a_target_completed_close_trigger_long/_short` + `test_d1a_target_fills_at_next_bar_open` + `test_d1a_intrabar_target_touch_does_not_fill`; clarified `test_d1a_same_bar_priority_*` to specify completed-close evaluation and next-bar-open fill); §14 (added P.14 invariant 9b for TARGET trigger/fill timing; clarified invariant 10 same-bar precedence to specify completed-close evaluation).

### 0.2 Funding timestamp equality clarification

The original §4.5 said "funding event used at signal must satisfy `funding_time ≤ bar_close_time`" but also said "Strict inequality if `funding_time == bar_close_time` is treated implementation-defined." This implementation-defined ambiguity was removed.

The amendment makes the equality case unambiguous:

- A funding event is eligible for a 15m signal bar **if and only if `funding_time ≤ bar_close_time`** (non-strict ≤).
- If `funding_time == bar_close_time`, the funding event IS treated as completed for that bar's signal evaluation (eligible).
- No signal may use a funding event where `funding_time > bar_close_time` (strict ineligibility above).
- Any trade triggered by such a signal still enters only at the next 15m bar open (bar B+1 open) per the §6.4 entry-timing rule; the equality case does not enable a same-close fill.
- Rolling 90-day Z-score still excludes the current event from its own normalization (this is independent of the alignment rule and remains unchanged).

Additionally, an **escalation rule** is now explicit: if any future implementation phase discovers that v002 `funding_time` does not represent a completed settlement timestamp (e.g., next-funding-due, in-progress-funding, or any forward-looking semantics), implementation must STOP and escalate before continuing. Lookahead in the funding-event source data would invalidate the entire D1-A specification.

Updated sections: §4.5 (replaced implementation-defined ambiguity with non-strict ≤ rule and added v002 funding-timestamp semantics escalation paragraph); §7 (replaced `test_event_alignment_strict_lte` with `test_event_alignment_non_strict_lte` + `test_event_alignment_equality_eligible`; clarified `test_no_lookahead_funding_event_alignment` companion test for exact equality); §14 (clarified P.14 invariant 12 to specify non-strict ≤ and add the v002 escalation cross-reference).

### 0.3 Scope confirmation

Both clarifications are **docs-only** and do not change:

- The D1-A locked spec values (signal threshold |Z_F| ≥ 2.0; 90-day lookback; 1.0 × ATR(20) stop; +2.0R TARGET; 32-bar time-stop; per-funding-event cooldown; symmetric direction; no regime filter).
- Any Phase 2f-framework threshold (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side).
- Any §1.7.3 project-level lock.
- The Phase 3h §17 recommendation (authorize Phase 3i-A implementation-control only).
- The Phase 3h precommitted run inventory or first-execution gate.
- Source code, tests, scripts, configuration, data, credentials, MCP / Graphify / `.mcp.json`, or exchange-write paths.

The clarifications strengthen the spec's unambiguous interpretability for any future Phase 3i-A / 3i-B1 / 3j implementation; they do not loosen, tighten, or substantively alter the spec's substance.

---

## 1. Current branch

`phase-3h/d1-execution-planning`, created from `main` at `562b43e18dd00055c5923aaf8d3788f68d5f3543` (Phase 3g merge-report commit).

## 2. Git status

Working tree clean after the Phase 3h commit. No untracked files outside the two Phase 3h deliverables. No `data/` files staged or tracked. No `src/`, `tests/`, `scripts/`, `.claude/`, `.mcp.json`, `config/`, `secrets/` changes.

## 3. Files changed

Two new files under `docs/00-meta/implementation-reports/`:

- `docs/00-meta/implementation-reports/2026-04-28_phase-3h_D1_execution-planning-memo.md` — Phase 3h execution-planning memo (§§ 1–17 per the operator brief).
- `docs/00-meta/implementation-reports/2026-04-28_phase-3h_closeout-report.md` — this file.

No other file is created, modified, or deleted by Phase 3h.

## 4. Commit hash(es)

Single Phase 3h commit on `phase-3h/d1-execution-planning`:

- `71c06f1` — `phase-3h: D1-A execution-planning memo (docs-only)` (2 files, 923 insertions; both Phase 3h deliverables landed in one commit).

The Phase 3h commit message references both files and explicitly preserves the Phase 3g + Phase 3f + Phase 3e + Phase 3d-B2 + Phase 2y + Phase 2x + §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side discipline. No subsequent commit is added by Phase 3h itself; an operator-authorized merge into `main` would add a separate `--no-ff` merge commit (and an optional follow-on merge-report commit modeled on Phase 3g's pattern).

## 5. Confirmation that Phase 3h was docs-only

Confirmed. Phase 3h produced two Markdown documentation files under `docs/00-meta/implementation-reports/` and no other artifacts. No source code, no tests, no scripts, no data, no configuration, no credentials, no MCP / Graphify integration, no `.mcp.json`, no exchange-write paths, no backtest run, no variant created, no parameter tuned.

## 6. Confirmation of preserved scope

The following project state is preserved verbatim by Phase 3h:

| Category | Status |
|----------|--------|
| Source code (`src/prometheus/**`) | UNCHANGED |
| Tests (`tests/**`) | UNCHANGED |
| Scripts (`scripts/**`) | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| `.mcp.json` | NOT CREATED, NOT MODIFIED |
| MCP servers / Graphify | NOT ACTIVATED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT MODIFIED |
| Production / sandbox / testnet keys | NONE EXIST, NONE PROPOSED |
| Exchange-write paths | NOT PROPOSED, NOT ENABLED |
| `data/` directory | UNCHANGED, NO COMMITS |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | PRESERVED VERBATIM |
| **§11.6 = 8 bps HIGH per side** | PRESERVED VERBATIM |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) | PRESERVED VERBATIM |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`; `exit_r_target=2.0`; `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP) | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes (overextension window 8; threshold 1.75 × ATR(20); mean-reference window 8; stop buffer 0.10 × ATR(20); time-stop 8 bars; stop-distance band [0.60, 1.80]) | UNCHANGED |
| D1-A locked spec (Phase 3g binding) — `|Z_F| ≥ 2.0`; 90-day lookback; 1.0 × ATR(20) stop never moved; +2.0R TARGET; STOP > TARGET > TIME_STOP; 32-bar time-stop; per-funding-event cooldown; symmetric direction; no regime filter | PRESERVED VERBATIM |
| R3 baseline-of-record status (Phase 2p §C.1) | PRESERVED |
| H0 framework anchor status (Phase 2i §1.7.3) | PRESERVED |
| R1a / R1b-narrow / R2 / F1 retained-research-evidence status | PRESERVED |
| R2 framework verdict (FAILED — §11.6 cost-sensitivity blocks) | PRESERVED |
| F1 framework verdict (HARD REJECT) | PRESERVED |
| Phase 3d-B2 terminal-for-F1 status | PRESERVED |
| Paper/shadow planning | NOT AUTHORIZED, NOT PROPOSED |
| Phase 4 (runtime / state / persistence) work | NOT AUTHORIZED, NOT PROPOSED |
| Live-readiness / deployment / production-key / exchange-write work | NOT AUTHORIZED, NOT PROPOSED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |

No threshold, strategy parameter, project lock, paper/shadow plan, Phase 4 work, live-readiness work, deployment work, MCP server, Graphify integration, `.mcp.json` change, credential creation, or exchange-write authorization occurred in Phase 3h.

## 7. Confirmation that Phase 3i was not started

Confirmed. Phase 3h is execution-planning-only. It does NOT implement the D1-A engine path; it does NOT add the `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum value to source code; it does NOT create the `prometheus.strategy.funding_aware_directional` module; it does NOT add `FundingAwareConfig` to source code; it does NOT modify `BacktestConfig` validators; it does NOT add `_run_symbol_d1a` to `BacktestEngine`; it does NOT extend `TradeRecord`; it does NOT add `FundingAwareLifecycleCounters`; it does NOT add D1-A unit tests; it does NOT add a D1-A runner script; it does NOT execute any D1-A backtest.

All Phase 3i-A architecture is described in Phase 3h §5 / §6 / §7 as **forward-looking planning only**, not implementation. Phase 3i-A authorization requires a separately-authorized operator decision after Phase 3h merges.

## 8. Branch ready for operator review and possible merge

**YES.** The branch tip is the Phase 3h single commit landing both deliverables. The branch is ready for operator review.

If the operator approves the Phase 3h execution-planning memo:

- Phase 3h may be merged into `main` with `--no-ff` per the Phase 3d-B2 / Phase 3e / Phase 3f / Phase 3g merge-pattern precedent.
- A merge-report commit may follow, modeled on `docs/00-meta/implementation-reports/2026-04-28_phase-3g_merge-report.md`.
- The recommended next operator decision (per Phase 3h §17) is **authorize Phase 3i-A implementation-control only**, contingent on operator authorization. Phase 3i-A would be a Phase-3d-A-style implementation phase: D1-A primitives + config + tests + H0/R3/F1 control reproduction, with deliberate non-runnability (engine guard rejects D1-A runtime dispatch). It would NOT authorize execution; Phase 3i-B1 (engine wiring) and Phase 3j (candidate runs) would each require their own subsequent operator decisions.

If the operator does not approve Phase 3h or prefers a different framing, the branch may be discarded without affecting `main` (Phase 3g merge stands; project state remains at `562b43e`).

Phase 3h does NOT recommend implementation, backtesting, paper/shadow, Phase 4, live-readiness, deployment, F1-prime / target-subset rescue, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, threshold revision, or §1.7.3 lock revision. Awaiting operator review.

---

**End of Phase 3h closeout report.**
