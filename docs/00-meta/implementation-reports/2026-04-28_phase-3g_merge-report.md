# Phase 3g — Merge Report

**Phase:** 3g — Docs-only D1 funding-aware directional / carry-aware strategy spec memo + methodology sanity audit, merged into `main`.

**Date:** 2026-04-28 UTC.

---

## 1. Phase 3g branch tip SHA before merge

`fc603f24ccd0782d40a1e0cc4cae17047784ffdf` on `phase-3g/d1-funding-aware-spec`.

The branch contained eight commits ahead of `main` at merge time:

- `2c3a91b` — `phase-3g: D1 funding-aware spec memo (docs-only)` — original Phase 3g memo + closeout.
- `e439c6b` — `phase-3g: record commit hash 2c3a91b in closeout report`.
- `97085d9` — `phase-3g: amend spec memo for five spec-consistency corrections` (first amendment).
- `7dfa596` — `phase-3g: record amendment commit 97085d9 in closeout report`.
- `5817cbb` — `phase-3g: RR/target sanity amendment -- target revised to +2.0R (Option A)` (second amendment).
- `01bd227` — `phase-3g: record RR/target sanity amendment commit 5817cbb in closeout`.
- `0cf3fd7` — `phase-3g: methodology sanity audit (docs-only retrospective)`.
- `aa18703` — `phase-3g: record methodology audit commit 0cf3fd7 in closeout`.
- `fc603f2` — `phase-3g: closeout sec.5 wording cleanup -- three docs files` (final pre-merge cleanup).

## 2. Merge commit hash

`f9b81195e2c518d6aa48b78a12149aab873db127`.

Created by `git merge --no-ff phase-3g/d1-funding-aware-spec` from `main` at `aee1b0d9d5436cc4beca382fd3d2165be63b0d84` (pre-merge). Merge produced by the `ort` strategy. Three new files added; 1404 insertions; no deletions.

## 3. Merge-report commit hash

To be recorded after this merge-report file is committed to `main` and pushed. The merge-report commit appends this Markdown file under `docs/00-meta/implementation-reports/` and changes nothing else.

## 4. Main / origin sync confirmation

Local `main` and `origin/main` are synced at the merge commit:

```text
local  main         f9b81195e2c518d6aa48b78a12149aab873db127
origin/main         f9b81195e2c518d6aa48b78a12149aab873db127
```

Push completed cleanly: `aee1b0d..f9b8119  main -> main`.

## 5. Git status

Working tree clean immediately after the merge and push. No untracked files. No staged changes. No `data/` artifacts staged or tracked.

## 6. Latest 5 commits

```text
f9b8119 Merge Phase 3g (D1 funding-aware spec memo + methodology sanity audit) into main
fc603f2 phase-3g: closeout sec.5 wording cleanup -- three docs files
aa18703 phase-3g: record methodology audit commit 0cf3fd7 in closeout
0cf3fd7 phase-3g: methodology sanity audit (docs-only retrospective)
01bd227 phase-3g: record RR/target sanity amendment commit 5817cbb in closeout
```

## 7. Files included in the merge

Three new files, all under `docs/00-meta/implementation-reports/`:

- `docs/00-meta/implementation-reports/2026-04-28_phase-3g_D1_funding-aware-spec-memo.md` (D1-A spec memo with both spec amendments incorporated; 897 lines).
- `docs/00-meta/implementation-reports/2026-04-28_phase-3g_methodology-sanity-audit.md` (retrospective methodology sanity audit; 340 lines).
- `docs/00-meta/implementation-reports/2026-04-28_phase-3g_closeout-report.md` (closeout with §0 amendment summary; 167 lines).

No source code, no tests, no scripts, no `.claude/` files, no `.mcp.json`, no configuration, no credentials, no `data/`, no existing-doc modifications.

## 8. Confirmation that Phase 3g was docs-only

Confirmed. Phase 3g produced three Markdown documentation files under `docs/00-meta/implementation-reports/` and no other artifacts. No source code, tests, scripts, configuration, credentials, MCP servers, Graphify integration, `.mcp.json`, or exchange-write paths were touched. No backtest was run; no variant was created; no parameter was tuned (other than the D1-A target rule revision from +1.0R to +2.0R per the Phase 3g RR/target sanity review Option A, which was explicitly authorized by the operator brief that introduced that review).

## 9. Confirmation of D1-A specification

Confirmed. D1-A was specified with the following locked axes per the Phase 3g spec memo §6 and amended per the two spec amendments:

- **Funding-rate extreme contrarian directional signal** at the most recent completed Binance USDⓈ-M 8h funding event prior to 15m bar close.
- **|Z_F| ≥ 2.0** over **trailing 90 days** of completed funding events (excluding the current event to avoid lookahead).
- **1.0 × ATR(20)** stop at fill, never moved intra-trade, MARK_PRICE stop trigger.
- **+2.0R TARGET** (recorded exit reason: TARGET; revised from +1.0R via Phase 3g §5.6 RR/target sanity review Option A using R3's non-fitting project convention; same-bar priority STOP > TARGET > TIME_STOP).
- **32-bar time-stop** (= 8 hours = exactly one funding cycle), with completed-bar fill discipline (TIME_STOP triggers at close of bar `B+1+32`; fills at open of bar `B+1+33`; no same-close fill).
- **Funding-event-level funnel counters** (`funding_extreme_events_detected`, `funding_extreme_events_filled`, `funding_extreme_events_rejected_stop_distance`, `funding_extreme_events_blocked_cooldown`); identity preserved; repeated 15m bars referencing the same `funding_event_id` must not inflate event-level counts.

## 10. Confirmation that the methodology sanity audit found Phase 3g safe to merge

Confirmed. The Phase 3g methodology sanity audit (`2026-04-28_phase-3g_methodology-sanity-audit.md` §7.1) concluded:

> **YES.** The Phase 3g spec memo (with both amendments — five spec-consistency corrections + RR/target sanity Option A revision to +2.0R) is methodologically sound.

The audit also confirmed:

- All prior V1-family + F1 verdicts (R1a mixed-PROMOTE non-leading; R1b-narrow PROMOTE-with-caveats non-leading; R2 FRAMEWORK FAILED — §11.6; F1 HARD REJECT) correctly handle the structural concerns identified retrospectively.
- The amended D1-A +2.0R spec is structurally sane and aligned with R3's non-fitting project convention (§5.1 / §5.2).
- TIME_STOP-subset diagnostics confirmed central for any future first execution (§5.3).
- No target sweep or D1-prime is authorized; single-spec discipline preserved (§5.4).
- Future-spec checklist (12 items) added as forward-looking guidance for any subsequent operator-authorized strategy spec; non-binding on existing candidates.
- Phase 3h remains only a future operator decision (§7.3).

## 11. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after merge and push shows zero `data/` entries. The three Phase 3g doc files are the only files touched by the merge. No `data/` directory contents are tracked by git.

## 12. Confirmation that no thresholds, strategy parameters, project locks, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, or exchange-write work changed

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) | UNCHANGED |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`; `exit_r_target=2.0`; `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP) | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes | UNCHANGED |
| R3 baseline-of-record status (Phase 2p §C.1) | PRESERVED |
| H0 framework anchor status (Phase 2i §1.7.3) | PRESERVED |
| R1a / R1b-narrow / R2 / F1 retained-research-evidence status | PRESERVED |
| R2 framework verdict (FAILED — §11.6 cost-sensitivity blocks) | PRESERVED |
| F1 framework verdict (HARD REJECT) | PRESERVED |
| Phase 3d-B2 terminal-for-F1 status | PRESERVED |
| D1-A target rule | REVISED (+1.0R → +2.0R per Phase 3g §5.6 RR/target sanity review Option A; explicitly authorized by the operator brief that introduced the RR/target sanity review; reuses R3's non-fitting project convention) |
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

The only locked-axis revision under Phase 3g is the D1-A target rule (+1.0R → +2.0R), explicitly authorized by the operator brief that introduced the RR/target sanity review under Option A. No Phase 2f-framework threshold is loosened; no §10.4 absolute floor revised; no §11.6 cost-sensitivity gate revised; no §1.7.3 project-level lock revised.

## 13. Confirmation that no next phase was started and Phase 3h remains only a future operator decision

Confirmed. Phase 3g merged into `main` is terminal-as-of-now. **No Phase 3h** (D1-A execution-planning memo, Phase-3c-style) and no implementation phase has been started. Phase 3g recommends GO (provisional) for a future Phase 3h with target +2.0R, contingent on operator authorization (per Phase 3g §15.3 and methodology sanity audit §7.3).

The recommended next operator decision is one of:

1. Authorize Phase 3h (D1-A execution-planning memo) — Phase 3g primary recommendation.
2. Remain paused per Phase 3e §9 / Phase 3f §8 default.
3. Authorize an alternative direction (D7 external cost-evidence review per Phase 3f §7.7) or any other operator-driven docs-only direction.
4. Any other operator-driven decision consistent with Phase 3e / Phase 3f / Phase 3g restrictions.

Until the operator authorizes one of those decisions, the project remains at the post-Phase-3g / Phase-3f / Phase-3e / Phase-3d-B2 consolidation boundary. No paper/shadow planning, no Phase 4 runtime work, no live-readiness work, no deployment work, no production-key creation, no exchange-write capability — all remain unauthorized.

---

**End of Phase 3g merge report.** Phase 3g D1 funding-aware spec memo + methodology sanity audit + closeout merged into `main` at `f9b81195e2c518d6aa48b78a12149aab873db127`. D1-A specified with funding extreme contrarian signal, |Z_F| ≥ 2.0 over trailing 90 days, 1.0 × ATR stop, +2.0R TARGET, 32-bar time stop, funding-event-level counters. Methodology sanity audit confirms Phase 3g safe to merge. R3 V1-breakout baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved verbatim. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 locks preserved verbatim. No paper/shadow, no Phase 4, no live-readiness, no deployment, no implementation, no execution, no backtest, no parameter tuning, no Phase 2f-framework threshold change, no project-lock change, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits, no code change. **No next phase started; Phase 3h remains only a future operator decision.** Awaiting operator review.
