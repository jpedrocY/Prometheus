# Phase 3g — Closeout Report

**Phase:** 3g — Docs-only D1 funding-aware directional / carry-aware strategy spec memo (Phase-3b-style), with post-review docs-only amendment for spec-consistency corrections.

**Branch:** `phase-3g/d1-funding-aware-spec`.

**Date:** 2026-04-28 UTC.

---

## 0. Post-review docs-only amendments

After the initial Phase 3g commit, two rounds of operator review surfaced spec-consistency and risk-reward concerns. Two subsequent docs-only amendments addressed them.

### 0.1 First amendment — five spec-consistency corrections

1. **Exit-reason consistency.** §6.8 / §7 / §12 standardized on D1-A recorded exit reason **TARGET** (matching F1 precedent), not TAKE_PROFIT (which is a V1-family multi-stage exit reason). Same-bar priority `STOP > TARGET > TIME_STOP`. D1-A emits only `STOP / TARGET / TIME_STOP / END_OF_DATA`.
2. **Time-stop fill timing.** §6.9 clarified the completed-bar discipline: TIME_STOP triggers at the close of the 32nd completed 15m bar from entry fill (bar `B+1+32`); the position fills at the **next bar open** (`B+1+33`); no same-close TIME_STOP fill.
3. **M1 displacement reference.** §10.1 changed the post-entry displacement reference from `close(B+1)` to **`fill_price`** (the actual next-bar-open fill price): `counter_displacement_h_R = ((close(entry_bar + h) − fill_price) × trade_direction_sign) / stop_distance`.
4. **BTC HIGH PF floor explicitness.** §13.2 / §13.3 / §13.4 made the §10.4-style PF floor explicit at BTC R HIGH MARK: `PF > 0.30`. The HIGH-slip gate is now stated as four explicit conditions (BTC HIGH expR > 0; BTC HIGH PF > 0.30; ETH HIGH expR > −0.50; ETH HIGH PF > 0.30). **No threshold loosened**; the PF floor was already implicit via the §7.3 catastrophic-floor predicate, now explicit at the gate level.
5. **Funnel counting level.** §9.4 / §12 renamed the lifecycle / funnel counters to **funding-event-level** (`funding_extreme_events_detected`, `funding_extreme_events_filled`, `funding_extreme_events_rejected_stop_distance`, `funding_extreme_events_blocked_cooldown`) with the identity preserved. Repeated 15m bars referencing the same `funding_event_id` must not inflate the event-level detected count.

This first amendment is docs-only and does not change source code, tests, scripts, configuration, data, thresholds, strategy parameters, or project locks (the BTC HIGH PF floor was already implicit; making it explicit does not loosen any threshold).

### 0.2 Second amendment — RR / target sanity review (Option A: target revised to +2.0R)

A second round of operator review raised a structural concern that the original +1.0R target produced an excessive required win-rate after fees, slippage, and uncertain funding accrual. Specifically, at MED–HIGH slippage the +1.0R target implied a 76–93% breakeven win-rate without funding (68–85% with one-cycle funding accrual), which is impractical given empirical V1 / R3 / F1 win rates of 21–42%, and is structurally inconsistent with the Phase 3f / Phase 3g thesis that D1-A should *address* cost-sensitivity (not inherit R2's small-R-multiple slippage-fragility regime).

A new dedicated section **§5.6 — Risk-reward and target sanity review** was added containing:

- **§5.6.1** — Gross-breakeven analysis at the original +1.0R target (winner net +0.60 / +0.47 / +0.14 R at LOW / MED / HIGH; breakeven WR 70 / 76.5 / 93%).
- **§5.6.2** — Effect of fees, slippage, and uncertain funding accrual.
- **§5.6.3** — Required win-rate burden is impractical at +1.0R (70%+ structural requirement vs 21–42% empirical V1 / R3 / F1 win rates).
- **§5.6.4** — Structural compatibility with the cost-sensitivity thesis (+1.0R sits in R2's failed-§11.6 small-R-multiple regime).
- **§5.6.5** — Decision: **Option A** — revise D1-A target to **+2.0R**, reusing R3's established non-fitting project convention (Phase 2j §D `exit_r_target=2.0`; Phase 2p §C.1 baseline-of-record). Option B (keep +1.0R) and Option C (NO-GO) explicitly rejected.

The +2.0R target moderates breakeven WR to 51% (MED) / 62% (HIGH) without funding, or 45% / 56% with one-cycle funding accrual — within the band of empirical observed V1 / R3 / F1 win rates (challenging but plausible). Tradeoff acknowledged: TARGET-exit fraction will be lower than F1's ~33% (estimated 5–20% range; descriptive only), with the bulk of trades exiting at TIME_STOP at intermediate R-multiples; the 32-bar / one-funding-cycle hold remains compatible because TIME_STOP catches partial-reversion outcomes.

Updated sections (in addition to new §5.6): §5.1 hypothesis statement; §5.5 cost arithmetic; §6.8 target / exit definition (LONG/SHORT target_price formulas; conceptual exit "+2.0 R target"); §7 non-fitting rationale Target row; §9.3 config model (`target_r_multiple = 2.0`; renamed from `take_profit_r_multiple`); §10.3 M3 description; §11 expected failure modes (added items 12–13 on +2.0R reachability and TIME_STOP-subset dominance); §12 P.14 invariants ("+1.0 R target hit" → "+2.0 R target hit"); §14 overfitting risk (added target-sweep prohibition); §15.1 / §15.3 GO/NO-GO conditions; end-of-memo summary.

**No changes to:** funding Z-score threshold |Z_F| ≥ 2.0; 90-day lookback; entry timing (next-bar open); allowed directionality (symmetric long/short); cooldown concept (per-funding-event consumption); §11.6 = 8 bps HIGH per side; §10.4 absolute floors; §1.7.3 project locks; recorded exit reason TARGET; same-bar priority STOP > TARGET > TIME_STOP; 32-bar time-stop length; 1.0 × ATR(20) stop. The target rule is the only locked axis revised (per the brief's explicit allowance for revising the D1-A target rule under Option A).

The second amendment is **docs-only** and does not change source code, tests, scripts, configuration, data, project locks, or any threshold (other than revising the D1-A target rule per Option A; no Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold changed).

---

## 1. Current branch

`phase-3g/d1-funding-aware-spec`, created from `main` at `aee1b0d9d5436cc4beca382fd3d2165be63b0d84` (Phase 3f merge-report commit).

## 2. Git status

Working tree clean after the Phase 3g commit. No untracked files outside the two Phase 3g deliverables. No `data/` files staged or tracked. No `src/`, `tests/`, `scripts/`, `.claude/`, `.mcp.json`, `config/`, `secrets/` changes.

## 3. Files changed

Two files under `docs/00-meta/implementation-reports/`, both touched by the original Phase 3g commit and the post-review amendment commit:

- `docs/00-meta/implementation-reports/2026-04-28_phase-3g_D1_funding-aware-spec-memo.md` — Phase 3g spec memo (§§ 1–16 per the operator brief), amended in §§ 6.8 / 6.9 / 7 / 9.4 / 10.1 / 12 / 13.2 / 13.3 / 13.4 / end-summary for the five spec-consistency corrections in §0 above.
- `docs/00-meta/implementation-reports/2026-04-28_phase-3g_closeout-report.md` — this file (added §0 post-review amendment summary; updated §4 to record both commits).

No other file is created, modified, or deleted by Phase 3g.

## 4. Commit hash(es)

Five Phase 3g commits on `phase-3g/d1-funding-aware-spec`:

- `2c3a91b` — `phase-3g: D1 funding-aware spec memo (docs-only)` — original Phase 3g memo + closeout (2 files, 856 insertions).
- `e439c6b` — `phase-3g: record commit hash 2c3a91b in closeout report` — closeout §4 commit-hash backfill (1 file, +5 / −1).
- `97085d9` — `phase-3g: amend spec memo for five spec-consistency corrections` — first amendment (per §0.1 above) (2 files, +89 / −29).
- `7dfa596` — `phase-3g: record amendment commit 97085d9 in closeout report` — closeout backfill for first amendment (1 file, +8 / −4).
- `5817cbb` — `phase-3g: RR/target sanity amendment -- target revised to +2.0R (Option A)` — second amendment (per §0.2 above) revising D1-A target from +1.0R to +2.0R per RR/target sanity review (2 files, +135 / −20).

**Branch HEAD full SHA (current `git rev-parse HEAD`):** `5817cbba1f76e7f93ca125aa4943de9dd21febd1`.

Both amendments preserve all Phase 3f + Phase 3e + Phase 3d-B2 + Phase 2y + Phase 2x + §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side discipline. The only locked-axis revision is the D1-A target rule (+1.0R → +2.0R) under the second amendment's Option A — explicitly authorized by the operator brief that introduced the RR/target sanity review. No Phase 2f-framework threshold is loosened; the §10.4 absolute floors and §11.6 cost-sensitivity gate are preserved verbatim. Both amendments change nothing other than docs in `docs/00-meta/implementation-reports/`. An operator-authorized merge into `main` would add a separate `--no-ff` merge commit (and an optional follow-on merge-report commit modeled on Phase 3f's pattern).

## 5. Confirmation that Phase 3g was docs-only

Confirmed. Phase 3g produced two Markdown memos under `docs/00-meta/implementation-reports/` and no other artifacts. No source code, no tests, no scripts, no data, no configuration, no credentials, no MCP / Graphify integration, no `.mcp.json`, no exchange-write paths, no backtest run, no variant created, no parameter tuned.

## 6. Confirmation of preserved scope

The following project state is preserved verbatim by Phase 3g:

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
| **§11.6 = 8 bps HIGH per side** | PRESERVED VERBATIM (Phase 2y closeout preserved) |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) | PRESERVED VERBATIM |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`; `exit_r_target=2.0`; `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP) | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes (overextension window 8; threshold 1.75 × ATR(20); mean-reference window 8; stop buffer 0.10 × ATR(20); time-stop 8 bars; stop-distance band [0.60, 1.80]) | UNCHANGED |
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
| `docs/03-strategy-research/v1-breakout-strategy-spec.md` | UNCHANGED |
| `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` | UNCHANGED |
| `docs/05-backtesting-validation/cost-modeling.md` | UNCHANGED |
| `docs/05-backtesting-validation/backtesting-principles.md` | UNCHANGED |
| `docs/04-data/data-requirements.md` | UNCHANGED |
| `docs/04-data/dataset-versioning.md` | UNCHANGED |

No threshold, strategy parameter, project lock, paper/shadow plan, Phase 4 work, live-readiness work, deployment work, MCP server, Graphify integration, `.mcp.json` change, credential creation, or exchange-write authorization occurred in Phase 3g.

## 7. Branch ready for operator review and possible merge

**YES.** The branch tip after both post-review amendments is `5817cbba1f76e7f93ca125aa4943de9dd21febd1`. The branch contains five commits ahead of `main`: the original Phase 3g spec memo + closeout (`2c3a91b`), the closeout commit-hash backfill (`e439c6b`), the first post-review docs-only amendment (`97085d9` — five spec-consistency corrections), the closeout backfill for the first amendment (`7dfa596`), and the second post-review docs-only amendment (`5817cbb` — RR/target sanity amendment Option A revising target from +1.0R to +2.0R). The branch is ready for operator review and possible merge.

If the operator approves the Phase 3g spec memo:

- Phase 3g may be merged into `main` with `--no-ff` per the Phase 3d-B2 / Phase 3e / Phase 3f merge-pattern precedent.
- A merge-report commit may follow, modeled on `docs/00-meta/implementation-reports/2026-04-28_phase-3f_merge-report.md`.
- The recommended next operator decision (per Phase 3g §15.3) is **GO (provisional) for a future Phase 3h execution-planning memo for D1-A**, contingent on operator authorization. Phase 3h would be a Phase-3c-style docs-only execution-planning phase; it would not authorize execution, implementation, or any code change. Each subsequent phase (Phase 3h / Phase 3i / Phase 3j) requires its own separate operator-decision gate.

If the operator does not approve Phase 3g or prefers a different framing, the branch may be discarded without affecting `main` (Phase 3f merge stands; project state remains at `aee1b0d`).

Phase 3g does NOT recommend implementation, backtesting, paper/shadow, Phase 4, live-readiness, deployment, F1-prime / target-subset rescue, threshold revision, or §1.7.3 lock revision. Awaiting operator review.

---

**End of Phase 3g closeout report.**
