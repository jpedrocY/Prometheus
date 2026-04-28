# Phase 3f — Merge Report

**Phase:** 3f — Docs-only next research-direction discovery memo merged into `main`.

**Date:** 2026-04-28 UTC.

---

## 1. Phase 3f branch tip SHA before merge

`ba3cd76b3d49e088a760e78f6078d2ebe214b1f5` on `phase-3f/research-direction-discovery`.

Branch contained two commits ahead of `main`:

- `0371c5d` — `phase-3f: next research-direction discovery memo (docs-only)` (2 files, +627).
- `ba3cd76` — `phase-3f: record commit hash 0371c5d in closeout report` (1 file, +5 / −1).

## 2. Merge commit hash

`a7607b691af962aa450619e4321e9e1bd8d99f54`.

Created by `git merge --no-ff phase-3f/research-direction-discovery` from `main` at `93a39434fe4dba64d10c85ac93b8b5923af473f7` (pre-merge). Merge produced by the `ort` strategy. Two files added; +631 insertions; no deletions.

## 3. Merge-report commit hash

To be recorded after this merge-report file is committed to `main` and pushed. The merge-report commit appends this Markdown file under `docs/00-meta/implementation-reports/` and changes nothing else.

## 4. Main / origin sync confirmation

Local `main` and `origin/main` are synced at the merge commit:

```text
local  main         a7607b691af962aa450619e4321e9e1bd8d99f54
origin/main         a7607b691af962aa450619e4321e9e1bd8d99f54
```

Push completed cleanly: `93a3943..a7607b6  main -> main`.

## 5. Git status

Working tree clean immediately after the merge and push. No untracked files. No staged changes. No `data/` artifacts staged or tracked.

## 6. Latest 5 commits

```text
a7607b6 Merge Phase 3f (next research-direction discovery memo) into main
ba3cd76 phase-3f: record commit hash 0371c5d in closeout report
0371c5d phase-3f: next research-direction discovery memo (docs-only)
93a3943 docs(phase-3e): merge report
577d9ae Merge Phase 3e (post-F1 research consolidation memo) into main
```

## 7. Files included in the merge

Two new files, both under `docs/00-meta/implementation-reports/`:

- `docs/00-meta/implementation-reports/2026-04-28_phase-3f_research-direction-discovery.md` (Phase 3f memo; §§ 1–11 per the operator brief; 531 insertions).
- `docs/00-meta/implementation-reports/2026-04-28_phase-3f_closeout-report.md` (Phase 3f closeout; 100 insertions).

No source code, no tests, no scripts, no `.claude/` files, no `.mcp.json`, no configuration, no credentials, no `data/`, no existing-doc modifications.

## 8. Confirmation that Phase 3f was docs-only

Confirmed. Phase 3f produced two new Markdown memos under `docs/00-meta/implementation-reports/` and no other artifacts. No source code, tests, scripts, configuration, credentials, MCP servers, Graphify integration, `.mcp.json`, or exchange-write paths were touched. No backtest was run; no variant was created; no parameter was tuned.

## 9. Confirmation of Phase 3f recommendation hierarchy

Confirmed per Phase 3f §9:

| Tier | Direction | Phase 3f role |
|------|-----------|---------------|
| **Primary recommendation (active path)** | **D1 — funding-aware directional / carry-aware strategy** | **Best active docs-only candidate.** Cleanest §5-constraint compliance: lowest expected cost-sensitivity (addresses §5.2); episodic frequency (addresses §5.1); v002 sufficient (addresses §5.5); BTC-friendly mechanism (addresses §5.4); two falsifiable sub-hypotheses (addresses §5.6); not a disguised V1-breakout or F1-target-subset rescue (addresses §5.7). |
| **Alternative active recommendation** | **D7 — external execution-cost evidence review** | Framework-calibration audit; not a strategy redesign. Useful if operator prefers confirming the framework before any new strategy work. F1 HARD REJECT at HIGH (BTC expR=−0.7000 / PF=0.2181) is fresh empirical trigger arguably warranting verification against live-trading cost realism. |
| **Default recommendation** | **D8 — pause / no further active research** | Consistent with Phase 3e §7 + §8.1 + §9 primary recommendation. Phase 3f does not contradict Phase 3e's pause; it operates within it. |

Five other directions are not recommended now:

- D2 (volatility contraction redesigned) — later research candidate; family-shift cleanliness uncertainty.
- D3 (regime-first framework) — blocked by complexity; Phase 4 dependence.
- D4 (trend pullback avoiding R2 fragility) — later research candidate; operator-developed entry-geometry redesign required first.
- D5 (BTC/ETH relative strength) — blocked by §1.7.3 lock without operator-policy revision.
- D6 (range-bound regime strategy) — later research candidate; downgraded post-F1 due to small-R-multiple cost-sensitivity risk confirmed empirically by F1 HARD REJECT.

F1-prime / F1-target-subset / R1a-prime / R1b-prime / R2-prime rescue paths are explicitly forbidden.

## 10. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after merge and push shows zero `data/` entries. The two Phase 3f memo files are the only files touched by the merge. No `data/` directory contents are tracked by git.

## 11. Confirmation that no thresholds, strategy parameters, project locks, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, or exchange-write work changed

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) | UNCHANGED |
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

## 12. Confirmation that no next phase was started

Confirmed. Phase 3f merged into `main` is terminal-as-of-now. No Phase 3g (D1 funding-aware spec memo), no Phase 3h (D7 external cost-evidence review), no Phase 4, no paper/shadow, no live-readiness work, and no implementation phase has been started. The recommended next operator decision (per Phase 3f §9) is one of:

1. Authorize a docs-only spec memo for D1 (Phase 3g-equivalent) — Phase 3f primary recommendation.
2. Authorize D7 external execution-cost evidence review — Phase 3f alternative.
3. Remain paused per Phase 3e §9 — Phase 3f default.
4. Any other operator-driven decision consistent with Phase 3e / Phase 3f restrictions.

Until the operator authorizes one of those decisions, the project remains at the post-Phase-3f / Phase-3e / Phase-3d-B2 consolidation boundary.

---

**End of Phase 3f merge report.** Phase 3f docs-only research-direction discovery memo merged into `main` at `a7607b691af962aa450619e4321e9e1bd8d99f54`. R3 V1-breakout baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 locks preserved verbatim. No paper/shadow, no Phase 4, no live-readiness, no deployment, no implementation, no execution, no backtest, no parameter tuning, no threshold change, no project-lock change, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits, no code change. No next phase started. Awaiting operator review.
