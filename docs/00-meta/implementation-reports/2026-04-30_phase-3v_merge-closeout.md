# Phase 3v Merge Closeout

## Summary

Phase 3v — the **docs-only GAP-20260424-032 stop-trigger domain ambiguity resolution memo** — has been merged to `main` and pushed to `origin/main`. **GAP-20260424-032 (Backtest uses trade-price stops; live uses MARK_PRICE stops) is now RESOLVED at the governance level.** The resolution preserves historical retained-evidence backtests under their original `trade_price_backtest` provenance with all verdicts unchanged; preserves the §1.7.3 mark-price-stop lock for any future runtime / paper / live operation; forces stop-trigger domain to be explicit in any future evidence or runtime artifact via the §8.4 label scheme (`trade_price_backtest` | `mark_price_runtime` | `mark_price_backtest_candidate`); and makes `mixed_or_unknown` fail closed at any decision boundary.

**No retained-evidence verdict revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other — all preserved verbatim. **No policy locks changed.** §11.6 = 8 bps HIGH per side preserved. §1.7.3 mark-price-stops preserved. **No strategy rescue authorized. No Phase 4 / 4a authorized.**

**Three remaining OPEN ambiguity-log items** (GAP-20260424-030 break-even rule conflict — MEDIUM risk; GAP-20260424-031 EMA slope wording — LOW-MEDIUM risk; GAP-20260424-033 stagnation window — LOW risk) preserved unchanged. They remain pre-coding blockers per Phase 3u §8.5 and would require a separately authorized docs-only resolution phase if the operator wishes to close them.

**No code, tests, scripts, data, manifests modified beyond the ambiguity-log GAP-20260424-032 RESOLVED update. No diagnostics rerun. No Q1–Q7 rerun. No backtests. No data acquisition / patching / regeneration / modification. No verdict revision. No strategy / parameter / threshold / project-lock changes. No §11.6 change. No §1.7.3 change. No stop-loss-policy substantive change. No 5m strategy / hybrid / retained-evidence successor / new variant. No Phase 4 / Phase 4a authorization. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets requested or stored.** Recommended state remains **paused**. **No successor phase has been authorized.**

## Files changed

The Phase 3v merge into `main` brought in two new files plus one targeted edit to the ambiguity log (the Phase 3v artefacts that previously existed only on the Phase 3v branch):

- `docs/00-meta/implementation-reports/2026-04-30_phase-3v_gap-20260424-032-stop-trigger-domain-resolution.md` — Phase 3v governance memo (553 lines; 18 sections covering Summary; Authority and boundary; Starting state; Ambiguity being resolved; Historical backtest stop-trigger provenance; Runtime / paper / live stop-trigger policy; Phase 3s Q6 evidence relevance; Formal resolution (8-clause §8 rule); Required stop-trigger domain labels; Implications for retained verdicts; Implications for future backtests; Implications for future Phase 4a / runtime work; What this does not authorize; Ambiguity-log update; Forbidden-work confirmation; Remaining boundary; Operator decision menu; Next authorization status).
- `docs/00-meta/implementation-reports/2026-04-30_phase-3v_closeout.md` — Phase 3v closeout artefact (160 lines).
- `docs/00-meta/implementation-ambiguity-log.md` — targeted edit to GAP-20260424-032 entry only. `Status` changed from `OPEN` to `RESOLVED — Phase 3v governance memo (2026-04-30)`. `Operator decision` records the full Phase 3v governance resolution. `Resolution evidence` points to the Phase 3v memo. `Related docs` extended to include Phase 3s Q6, Phase 3u §8.5, Phase 3v memo, stop-loss-policy, and binance-usdm-order-model. **No other ambiguity-log entry modified.**

Total Phase 3v merge: 3 file changes, 719 insertions (net of the 6 lines replaced in the GAP-20260424-032 entry).

The post-merge housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-3v_merge-closeout.md` — this file.
- `docs/00-meta/current-project-state.md` — narrow update recording Phase 3v merged, GAP-20260424-032 resolved, stop-trigger-domain governance adopted, historical backtests remain `trade_price_backtest` provenance, runtime / paper / live stop handling remains `MARK_PRICE` locked, future evidence/runtime artifacts must label stop-trigger domain, `mixed_or_unknown` stop-trigger domain fails closed, remaining ambiguity-log OPEN items (GAP-20260424-030 / 031 / 033) noted, Phase 4 remains unauthorized, Phase 4a remains conditional only and not authorized, recommended state paused, no next phase authorized, all prior verdicts and locks preserved. Stale "Current phase" and "Most recent merge" code blocks refreshed to point at the Phase 3v merge.

NOT modified by this merge or by the housekeeping commit:

- All `data/manifests/*.manifest.json` files (v002 manifests + Phase 3q v001-of-5m manifests; mark-price `research_eligible: false` flag preserved).
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions.
- All `src/prometheus/**` source code.
- All `scripts/**`.
- All `tests/**`.
- All `.claude/rules/**`.
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u reports / closeouts / merge-closeouts.
- `docs/07-risk/stop-loss-policy.md` — substantive policy preserved verbatim. The Phase 3v memo notes that an optional minimal cross-reference back-pointer was permitted but Phase 3v opted not to make that edit because the Phase 3v memo + ambiguity-log RESOLVED entry are sufficient pointers.
- `docs/06-execution-exchange/binance-usdm-order-model.md` — preserved verbatim.
- `docs/12-roadmap/phase-gates.md` — preserved verbatim.
- `docs/12-roadmap/technical-debt-register.md` — preserved verbatim.
- All other `docs/**` files (other than `current-project-state.md` and the new merge-closeout artefact).

## Phase 3v commits included

| Commit | Subject |
|---|---|
| `671f6e2f344b3c9734f7dcd5deb3353aac02af57` | `phase-3v: GAP-20260424-032 stop-trigger domain ambiguity resolution memo (docs-only)` — Phase 3v governance memo + ambiguity-log GAP-20260424-032 RESOLVED update. |
| `5be99783f86eb3830cd9814defda3032073de3c7` | `docs(phase-3v): closeout report (Markdown artefact)` — Phase 3v closeout. |

## Merge commit

- **Phase 3v merge commit (`--no-ff`, ort strategy):** `15ba71cbc0e0a009a07f8950bf8013eade50cf9f`
- **Merge title:** `Merge Phase 3v (docs-only GAP-20260424-032 stop-trigger domain ambiguity resolution memo) into main`

The initial push attempt returned a transient remote 500 (HTTP error from GitHub); the immediate retry confirmed both local `main` and `origin/main` already at `15ba71c`, so the merge commit was pushed despite the spurious 500 status — reproducible per `git rev-parse main` and `git rev-parse origin/main` agreement.

## Housekeeping commit

The post-merge housekeeping commit adds this Phase 3v merge-closeout file and updates `current-project-state.md` narrowly. Its SHA advances `main` by one further commit beyond the merge commit `15ba71c` and is reported in the chat closeout block accompanying this commit. Per prior phase pattern, the housekeeping commit's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged.

## Final git status

```text
clean
```

Working tree empty after the post-merge housekeeping commit. No uncommitted changes. No untracked files.

## Final git log --oneline -8

Snapshot at the housekeeping commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this housekeeping commit itself is committed>  docs(phase-3v): merge closeout + current-project-state sync
15ba71c  Merge Phase 3v (docs-only GAP-20260424-032 stop-trigger domain ambiguity resolution memo) into main
5be9978  docs(phase-3v): closeout report (Markdown artefact)
671f6e2  phase-3v: GAP-20260424-032 stop-trigger domain ambiguity resolution memo (docs-only)
4577d75  docs(phase-3u): merge closeout + current-project-state sync
f2aba6d  Merge Phase 3u (docs-only implementation-readiness and Phase-4 boundary review) into main
f31903a  docs(phase-3u): closeout report (Markdown artefact)
711329f  phase-3u: implementation-readiness and Phase-4 boundary review (docs-only)
```

## Final rev-parse

- **`git rev-parse main`** (after housekeeping commit + push): the housekeeping commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse origin/main`** (after push): same as `main` above.
- **`git rev-parse HEAD`** (on `main`): same as `main` above.
- **`git rev-parse phase-3v/gap-20260424-032-stop-trigger-domain-resolution`**: `5be99783f86eb3830cd9814defda3032073de3c7` (branch tip preserved).
- **`git rev-parse origin/phase-3v/gap-20260424-032-stop-trigger-domain-resolution`**: `5be99783f86eb3830cd9814defda3032073de3c7`.
- **`git rev-parse phase-3u/implementation-readiness-and-phase-4-boundary-review`**: `f31903af800e4ce0ac25f17d56e7f3fa7cc83822` (branch tip preserved).
- **`git rev-parse phase-3t/post-5m-diagnostics-consolidation`**: `fcf8192e150e7dc783da345d2e54be8cff1611db` (branch tip preserved).
- **`git rev-parse phase-3s/5m-diagnostics-execution`**: `a93695f23d78f8975f33211439d66f8e5c90b49a` (branch tip preserved).
- **`git rev-parse phase-3r/mark-price-gap-governance`**: `06111957e465a4fc5d59190d82db379cc0f7cc86` (branch tip preserved).
- **`git rev-parse phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3` (branch tip preserved).

## main == origin/main confirmation

After the Phase 3v merge push: local `main` = `origin/main` = `15ba71cbc0e0a009a07f8950bf8013eade50cf9f`. Synced.

After the post-merge housekeeping commit + push: local `main` = `origin/main` advances to the housekeeping commit's SHA (reported in the chat closeout block accompanying this commit). Synced.

## GAP-20260424-032 resolution summary

**GAP-20260424-032 — Backtest uses trade-price stops; live uses MARK_PRICE stops.** Status: **RESOLVED — Phase 3v governance memo (2026-04-30)**. Resolution evidence: `docs/00-meta/implementation-reports/2026-04-30_phase-3v_gap-20260424-032-stop-trigger-domain-resolution.md` (Phase 3v memo §8 formal-resolution rule, eight clauses).

The resolution comprises eight binding clauses (Phase 3v §8) that establish:

- **Historical retained-evidence backtests remain valid under `trade_price_backtest` provenance.** Phase 2 / Phase 3 retained-evidence backtests (R3 / R1a / R1b-narrow / R2 / F1 / D1-A) carry implicit `stop_trigger_domain = trade_price_backtest`. v002 historical datasets remain authoritative. Verdict provenance unchanged.
- **Future runtime / paper / live stop handling remains `MARK_PRICE` locked.** Per §1.7.3 + `docs/07-risk/stop-loss-policy.md` + `docs/06-execution-exchange/binance-usdm-order-model.md` (`workingType=MARK_PRICE`, `priceProtect=TRUE`). Stop widening forbidden categorically per `.claude/rules/prometheus-safety.md`.
- **Valid stop-trigger-domain labels** (Phase 3v §8.4):
  - `trade_price_backtest` — historical or research backtest using trade-price stop-trigger modeling.
  - `mark_price_runtime` — future runtime / paper / live stop-trigger pathway using `workingType=MARK_PRICE`.
  - `mark_price_backtest_candidate` — research backtest explicitly modeling mark-price stop-triggers.
- **`mixed_or_unknown` is invalid and fails closed at any decision boundary.** A trade-execution decision under `mixed_or_unknown` must block the trade. A verdict decision must block the verdict. A persistence decision must block the persist. An evidence-promotion decision must block the promotion. Fail-closed is the only acceptable response to ambiguous stop-trigger domain.
- **Phase 3s Q6 remains descriptive only.** D1-A: mark-price stops trigger ~1.3–1.8 5m bars after trade-price stops would have triggered. R3 / R2 / F1: non-informative under Q6. Q6 does NOT revise verdicts; does NOT change stop-policy; does NOT authorize strategy rescue or live-readiness. The §1.7.3 mark-price-stop lock is preserved verbatim regardless of any Q6 finding.
- **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. All preserved verbatim.
- **No strategy rescue was authorized.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, 5m-on-X variant, or any other successor authorized.
- **No Phase 4 or Phase 4a was authorized.** Phase 3u §16 recommendations stand; Phase 4 remains unauthorized; Phase 4a remains conditional only and not authorized. Future Phase 4a (if ever authorized subject to Phase 3u §10 prohibitions) may implement the §8.4 labels and fail-closed validation locally — but Phase 3v does not authorize Phase 4a.
- **Future backtests intended to support paper/shadow/live readiness must explicitly use or validate `mark_price_backtest_candidate` modeling, or disclose that they are not live-readiness evidence.** Cross-domain comparability is bounded; live-readiness disclosure is required for `trade_price_backtest` reports that touch the readiness conversation.

## Remaining ambiguity-log items

After Phase 3v's GAP-20260424-032 resolution, three OPEN items remain in `docs/00-meta/implementation-ambiguity-log.md`:

| ID | Title | Risk | Notes |
|---|---|---|---|
| GAP-20260424-030 | Break-even rule text conflicts with spec Open Question #8 | MEDIUM | Documentation-level conflict in V1 strategy spec. Pre-coding blocker for any future runtime that implements break-even logic. |
| GAP-20260424-031 | EMA slope wording ambiguous: discrete comparison vs. fitted slope | LOW-MEDIUM | Documentation-level ambiguity. Already resolved at implementation level for executed backtests; spec text is unclear. Pre-coding blocker for any future runtime that re-implements EMA bias. |
| GAP-20260424-033 | Stagnation window not in Open Questions but discussed as metric | LOW | Documentation hygiene item. Weak pre-coding-blocker classification. |

These three items remain pre-coding blockers per Phase 3u §8.5 and would require a separately authorized docs-only resolution phase if the operator wishes to close them. Phase 3v does not authorize that follow-up phase; Phase 3v Option B (per Phase 3v §17.2) records this as a conditional secondary alternative.

## Forbidden-work confirmation

- **No Phase 3w / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No Phase 4 / Phase 4a started.** Phase 3v recommends Phase 4 remain unauthorized and Phase 4a remain conditional only; the merge does not change those recommendations into authorizations.
- **No implementation code written.** Phase 3v is text-only (memo + ambiguity-log entry edit); the merge brings in pre-existing Phase 3v artefacts unchanged.
- **No runtime / strategy / execution / risk-engine / database / dashboard / exchange code modified.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun. No new diagnostic computation.
- **No Q1–Q7 rerun.**
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. **§11.6 unchanged.** **§1.7.3 mark-price-stop lock unchanged.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No strategy rescue proposal.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, or 5m-on-X variant.
- **No new strategy candidate proposal.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No paper/shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket subscription.**
- **No public endpoints consulted.** This merge + housekeeping commit performs no network I/O.
- **No secrets requested or stored.**

## Remaining boundary

- **main HEAD:** the housekeeping commit (SHA reported in chat closeout). After the merge: `15ba71c`. Phase 3v memo + ambiguity-log update + closeout consolidated on `main`.
- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a (safe slice) remains conditional only and not authorized.
- **GAP-20260424-032:** **RESOLVED** by Phase 3v governance memo (this phase). The §8.4 stop-trigger-domain label scheme is binding from this commit forward on any future evidence or runtime artifact.
- **Remaining OPEN ambiguity-log items:** GAP-20260424-030 (MEDIUM), GAP-20260424-031 (LOW-MEDIUM), GAP-20260424-033 (LOW). Pre-coding blockers per Phase 3u §8.5; would require separately authorized resolution phase.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:**
  - `phase-3v/gap-20260424-032-stop-trigger-domain-resolution` pushed at `5be9978`. Commits in main via Phase 3v merge.
  - All prior phase branches preserved at their respective tips.

## Next authorization status

**No next phase has been authorized.** Phase 3v recommended Option A (remain paused) as primary; Option B (resolve remaining 3 OPEN ambiguity-log items via separate docs-only memos: GAP-20260424-030 / 031 / 033) as conditional secondary; Option C (Phase 4a safe-slice scoping memo per Phase 3u §16.3) as conditional tertiary subject to Phase 3u §10 anti-live-readiness preconditions; Option D (mark-price-stop sensitivity analysis on retained-evidence populations) as conditional alternative not recommended now (low expected new information); Options E (Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write) and F (strategy rescue / fresh-hypothesis research / regime-first / ML feasibility / new strategy-family discovery) NOT recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
