# Phase 3h — Merge Report

**Phase:** 3h — Docs-only D1-A execution-planning memo (Phase-3c-style) merged into `main`.

**Date:** 2026-04-28 UTC.

---

## 1. Phase 3h branch tip SHA before merge

`f75aebc2c146f642ea16a0145bc5403da46c59f7` on `phase-3h/d1-execution-planning`.

The branch contained four commits ahead of `main` at merge time:

- `71c06f1` — `phase-3h: D1-A execution-planning memo (docs-only)` — original Phase 3h memo + closeout.
- `2f364ed` — `phase-3h: record commit hash 71c06f1 in closeout report` — closeout commit-hash backfill.
- `4f996c6` — `phase-3h: clarify TARGET fill timing and funding timestamp equality` — post-review timing-clarification amendment.
- `f75aebc` — `phase-3h: record clarification amendment commit 4f996c6 in closeout` — closeout backfill for the clarification amendment.

## 2. Merge commit hash

`c2ba2fddf612adce5105ff6dc21e8642503dce08`.

Created by `git merge --no-ff phase-3h/d1-execution-planning` from `main` at `562b43e18dd00055c5923aaf8d3788f68d5f3543` (pre-merge). Merge produced by the `ort` strategy. Two new files added; 988 insertions; no deletions.

## 3. Merge-report commit hash

To be recorded after this merge-report file is committed to `main` and pushed. The merge-report commit appends this Markdown file under `docs/00-meta/implementation-reports/` and changes nothing else.

## 4. Main / origin sync confirmation

Local `main` and `origin/main` are synced at the merge commit:

```text
local  main         c2ba2fddf612adce5105ff6dc21e8642503dce08
origin/main         c2ba2fddf612adce5105ff6dc21e8642503dce08
```

Push completed cleanly: `562b43e..c2ba2fd  main -> main`.

## 5. Git status

Working tree clean immediately after the merge and push. No untracked files. No staged changes. No `data/` artifacts staged or tracked.

## 6. Latest 5 commits

```text
c2ba2fd Merge Phase 3h (D1-A execution-planning memo) into main
f75aebc phase-3h: record clarification amendment commit 4f996c6 in closeout
4f996c6 phase-3h: clarify TARGET fill timing and funding timestamp equality
2f364ed phase-3h: record commit hash 71c06f1 in closeout report
71c06f1 phase-3h: D1-A execution-planning memo (docs-only)
```

## 7. Files included in the merge

Two new files, both under `docs/00-meta/implementation-reports/`:

- `docs/00-meta/implementation-reports/2026-04-28_phase-3h_D1_execution-planning-memo.md` — Phase 3h execution-planning memo (§§ 1–17 per the operator brief; with both timing-clarification amendments incorporated; 830 lines).
- `docs/00-meta/implementation-reports/2026-04-28_phase-3h_closeout-report.md` — Phase 3h closeout (with §0 post-review clarification amendment summary; 158 lines).

No source code, no tests, no scripts, no `.claude/` files, no `.mcp.json`, no configuration, no credentials, no `data/`, no existing-doc modifications.

## 8. Confirmation that Phase 3h was docs-only

Confirmed. Phase 3h produced two Markdown documentation files under `docs/00-meta/implementation-reports/` and no other artifacts. No source code, tests, scripts, configuration, credentials, MCP servers, Graphify integration, `.mcp.json`, or exchange-write paths were touched. No backtest was run; no variant was created; no parameter was tuned.

## 9. Confirmation that the TARGET trigger/fill timing clarification is present

Confirmed per Phase 3h memo §5.6 (engine dispatch step 5), §7.2 (engine wiring tests), and §14 (P.14 invariant 9b):

- **TARGET triggers only on completed-bar close confirmation:** LONG `close ≥ target_price`; SHORT `close ≤ target_price`.
- **TARGET fills at the next bar open** (never at the trigger bar's close).
- **No intrabar target-touch fill** — a bar whose high (LONG) or low (SHORT) touches `target_price` but whose completed close does NOT satisfy the trigger condition produces no TARGET exit.
- **No same-close TARGET fill.**
- Same-bar priority remains `STOP > TARGET > TIME_STOP`, evaluated on the completed bar; trigger evaluation at bar close, fill at next bar open.
- STOP behavior unchanged (existing MARK_PRICE stop-trigger machinery preserved).
- TIME_STOP unchanged (close of `B+1+32` trigger; open of `B+1+33` fill).

Test plan reflects: `test_d1a_target_completed_close_trigger_long`, `test_d1a_target_completed_close_trigger_short`, `test_d1a_target_fills_at_next_bar_open`, `test_d1a_intrabar_target_touch_does_not_fill`, `test_d1a_same_bar_priority_stop_before_target` (clarified for completed-close evaluation), `test_d1a_same_bar_priority_target_before_time_stop` (clarified for next-bar-open fill).

## 10. Confirmation that the funding timestamp equality clarification is present

Confirmed per Phase 3h memo §4.5 (timestamp and no-lookahead invariants), §7 (event-alignment tests), and §14 (P.14 invariant 12):

- A funding event is eligible for a 15m signal bar **if and only if `funding_time ≤ bar_close_time`** (non-strict ≤).
- **`funding_time == bar_close_time` is eligible** — the event is treated as completed for that bar's signal evaluation.
- **`funding_time > bar_close_time` is forbidden** — strictly excluded; no signal may use such an event.
- Any trade triggered by such a signal still enters only at the **next 15m bar open** (bar B+1 open) per §6.4 entry-timing rule; the equality case does not enable a same-close fill.
- Rolling 90-day Z-score continues to exclude the current event from its own normalization (μ_F and σ_F at event N use events N−1..N−270; event N is not in the sample).
- **v002 funding-timestamp semantics escalation explicit:** if any future implementation phase (Phase 3i-A / 3i-B1 / 3j) discovers v002 `funding_time` does not represent a completed settlement timestamp (e.g., next-funding-due, in-progress-funding, or any forward-looking semantics), implementation must **STOP and escalate** before continuing.

Test plan reflects: `test_event_alignment_non_strict_lte`, `test_event_alignment_equality_eligible`, `test_event_alignment_no_lookahead`, `test_no_lookahead_funding_event_alignment` (with companion equality test).

## 11. Confirmation that D1-A remains specified but not implemented

Confirmed. Phase 3h is execution-PLANNING only. The D1-A spec was locked by Phase 3g (merged into `main` at `f9b8119` per the Phase 3g merge report). Phase 3h reproduces the Phase 3g binding spec verbatim and defines the future implementation, validation, run inventory, diagnostics, hard-block checks, and first-execution gate, but **does not implement** any of the architecture described.

Specifically, Phase 3h does NOT:

- Add the `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum value to `src/prometheus/research/backtest/config.py`.
- Create the `prometheus.strategy.funding_aware_directional` module.
- Add `FundingAwareConfig` to source code.
- Modify the `BacktestConfig` validator.
- Add `_run_symbol_d1a` to `BacktestEngine`.
- Extend `TradeRecord` with D1-A-specific fields.
- Add `FundingAwareLifecycleCounters`.
- Add D1-A unit tests.
- Add a D1-A runner script.
- Execute any D1-A backtest.

D1-A remains a specified-but-not-implemented strategy family at the post-Phase-3h plan boundary.

## 12. Confirmation that Phase 3i-A was not started

Confirmed. Phase 3h is execution-planning-only and explicitly does NOT authorize Phase 3i-A. Per Phase 3h §17, the recommended next operator decision is:

> **authorize Phase 3i-A implementation-control only**, contingent on operator authorization.

Phase 3i-A would be a Phase-3d-A-style implementation phase: D1-A primitives + config + tests + H0/R3/F1 control reproduction with deliberate non-runnability (engine guard rejects D1-A runtime dispatch). It would NOT authorize execution; Phase 3i-B1 (engine wiring) and Phase 3j (candidate runs + first-execution gate) would each require their own subsequent operator decisions.

No implementation, no execution, no Phase 3i-A code surface, no tests, no scripts, no runner, no D1-A backtest invocation has been started. Phase 3i-A authorization requires a separately-authorized operator decision after Phase 3h merges.

## 13. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after merge and push shows zero `data/` entries. The two Phase 3h doc files are the only files touched by the merge. No `data/` directory contents are tracked by git.

## 14. Confirmation that no thresholds, strategy parameters, project locks, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, or exchange-write work changed

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) | UNCHANGED |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`; `exit_r_target=2.0`; `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP) | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes | UNCHANGED |
| **D1-A locked spec values** (`|Z_F| ≥ 2.0`; 90-day lookback; 1.0 × ATR(20) stop never moved; +2.0R TARGET; 32-bar time-stop; per-funding-event cooldown; symmetric direction; no regime filter; recorded exit reason TARGET; STOP > TARGET > TIME_STOP) | UNCHANGED (preserved per Phase 3g binding) |
| R3 baseline-of-record status (Phase 2p §C.1) | PRESERVED |
| H0 framework anchor status (Phase 2i §1.7.3) | PRESERVED |
| R1a / R1b-narrow / R2 / F1 retained-research-evidence status | PRESERVED |
| R2 framework verdict (FAILED — §11.6 cost-sensitivity blocks) | PRESERVED |
| F1 framework verdict (HARD REJECT) | PRESERVED |
| Phase 3d-B2 terminal-for-F1 status | PRESERVED |
| Paper/shadow planning | NOT AUTHORIZED, NOT PROPOSED |
| Phase 4 (runtime / state / persistence) work | NOT AUTHORIZED, NOT PROPOSED |
| Live-readiness / deployment / production-key / exchange-write work | NOT AUTHORIZED, NOT PROPOSED |
| MCP servers / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |
| Source code (`src/prometheus/**`) | UNCHANGED |
| Tests (`tests/**`) | UNCHANGED |
| Scripts (`scripts/**`) | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

No threshold, strategy parameter, project lock, paper/shadow plan, Phase 4 work, live-readiness work, deployment work, MCP server, Graphify integration, `.mcp.json` change, credential creation, or exchange-write authorization occurred in Phase 3h. The two timing-clarification amendments are docs-only and strengthen the spec's unambiguous interpretability without altering its substance.

---

**End of Phase 3h merge report.** Phase 3h D1-A execution-planning memo + closeout (with two post-review timing-clarification amendments) merged into `main` at `c2ba2fddf612adce5105ff6dc21e8642503dce08`. Both clarifications present: TARGET triggers only on completed-bar close confirmation and fills at next bar open (no intrabar / no same-close fill); funding event eligibility is non-strict ≤ (equality eligible; strict-greater forbidden), with v002 funding-timestamp semantics escalation rule explicit. D1-A remains specified-but-not-implemented per Phase 3g binding. R3 V1-breakout baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved verbatim. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 locks preserved verbatim. D1-A locked spec preserved verbatim. No paper/shadow, no Phase 4, no live-readiness, no deployment, no implementation, no execution, no backtest, no parameter tuning, no threshold change, no project-lock change, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits, no code change. **Phase 3i-A NOT authorized; no next phase started.** Awaiting operator review.
