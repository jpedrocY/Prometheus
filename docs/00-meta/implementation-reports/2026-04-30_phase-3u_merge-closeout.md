# Phase 3u Merge Closeout

## Summary

Phase 3u — the **docs-only implementation-readiness and Phase-4 boundary review** — has been merged to `main` and pushed to `origin/main`. Phase 3u writes into the project record a forward-looking review evaluating whether the project should later move toward implementation-readiness / Phase-4 boundary work or remain paused.

**Phase 3u recommends remain paused as primary.** A conditional secondary alternative (docs-only ambiguity-resolution memo, especially resolving GAP-20260424-032 mark-price vs trade-price stop) is acceptable as it produces unconditional documentation value but is not endorsed over remain-paused. A conditional tertiary alternative (docs-only Phase 4a safe-slice scoping memo) is acceptable only with explicit anti-live-readiness preconditions and explicit operator commitment to deprioritize research.

**The reasoning:** no strategy is ready (R3 baseline-of-record but aggregate-negative; R2 / F1 / D1-A terminal; 5m research thread closed Phase 3t with descriptive-only findings); pre-coding blockers exist (4 currently-OPEN ambiguity-log items, most importantly GAP-20260424-032 HIGH risk); the cumulative pattern across 11 phases (3k–3u) is "remain paused" — reversing should be deliberate, not reactive. Canonical Phase 4 framing assumes strategy evidence which the project does not have. Future Phase 4a, if ever authorized, must be categorically local-only / fake-exchange / dry-run / exchange-write-free.

**No code, tests, scripts, data, manifests, strategy specs, thresholds, parameters, project locks, or prior verdicts modified.** No diagnostics rerun. No backtests. No data acquisition / patching / regeneration / modification. No Phase 3p §4.7 amendment. No 5m strategy / hybrid / retained-evidence successor / new variant. No Phase 4 / Phase 4a authorization. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private Binance endpoints / user stream / WebSocket / public endpoints consulted. No secrets requested or stored. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false` — all preserved verbatim. **Recommended state remains paused.** **No successor phase has been authorized.**

## Files changed

The Phase 3u merge into `main` brought in two new files (the Phase 3u artefacts that previously existed only on the Phase 3u branch):

- `docs/00-meta/implementation-reports/2026-04-30_phase-3u_implementation-readiness-and-phase-4-boundary-review.md` — Phase 3u review memo (548 lines; 17 sections covering Summary; Authority and boundary; Starting state; Why this review exists; Post-Phase-3t research state; Phase-gate assessment; Current documentation readiness; Technical-debt and blocker review; What Phase 4 would mean; What Phase 4 must not mean; Candidate Phase 4a safe slice; Risks of moving too early; Benefits of implementation-readiness work; Fresh-hypothesis research alternative; Recommendation; Operator decision menu; Next authorization status).
- `docs/00-meta/implementation-reports/2026-04-30_phase-3u_closeout.md` — Phase 3u closeout artefact (129 lines).

Total Phase 3u merge: 2 files added, 677 insertions.

The post-merge housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-3u_merge-closeout.md` — this file.
- `docs/00-meta/current-project-state.md` — narrow update recording Phase 3u merged, implementation-readiness and Phase-4 boundary reviewed, Phase 4 remains unauthorized, Phase 4a remains conditional only and not authorized, pre-coding blockers remain open (especially GAP-20260424-032), recommended state paused, no next phase authorized, all prior verdicts and locks preserved. Stale "Current phase" and "Most recent merge" code blocks refreshed to point at the Phase 3u merge.

NOT modified by this merge or by the housekeeping commit:

- All `data/manifests/*.manifest.json` files (v002 + Phase 3q v001-of-5m manifests; mark-price `research_eligible: false` flag preserved).
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions (git-ignored per repo convention; v002 partitions and Phase 3q 5m partitions untouched on local filesystem).
- All `src/prometheus/**` source code.
- All `scripts/**`.
- All `tests/**`.
- All `.claude/rules/**`.
- All Phase 3o / 3p / 3q / 3r / 3s / 3t reports / closeouts / merge-closeouts (predeclared rules, prior boundaries, Phase 3p §4.7, Phase 3r §8, Phase 3s diagnostic outputs, Phase 3t consolidation conclusions all preserved verbatim).
- `docs/00-meta/implementation-ambiguity-log.md` — surveyed read-only by Phase 3u; no entries modified. The 4 currently-OPEN items (GAP-20260424-030 / 031 / 032 / 033) remain OPEN.
- `docs/12-roadmap/phase-gates.md` — cited by Phase 3u; not modified.
- `docs/12-roadmap/technical-debt-register.md` — cited by Phase 3u; not modified.

## Phase 3u commits included

| Commit | Subject |
|---|---|
| `711329ff755ee6791b501fb7c3937b163e302197` | `phase-3u: implementation-readiness and Phase-4 boundary review (docs-only)` — Phase 3u review memo. |
| `f31903af800e4ce0ac25f17d56e7f3fa7cc83822` | `docs(phase-3u): closeout report (Markdown artefact)` — Phase 3u closeout. |

## Merge commit

- **Phase 3u merge commit (`--no-ff`, ort strategy):** `f2aba6d6b112bb3d1b3bfb2e47285b9195bcf205`
- **Merge title:** `Merge Phase 3u (docs-only implementation-readiness and Phase-4 boundary review) into main`

## Housekeeping commit

The post-merge housekeeping commit adds this Phase 3u merge-closeout file and updates `current-project-state.md` narrowly. Its SHA advances `main` by one further commit beyond the merge commit `f2aba6d` and is reported in the chat closeout block accompanying this commit. Per prior phase pattern, the housekeeping commit's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged.

## Final git status

```text
clean
```

Working tree empty after the post-merge housekeeping commit. No uncommitted changes. No untracked files.

## Final git log --oneline -8

Snapshot at the housekeeping commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this housekeeping commit itself is committed>  docs(phase-3u): merge closeout + current-project-state sync
f2aba6d  Merge Phase 3u (docs-only implementation-readiness and Phase-4 boundary review) into main
f31903a  docs(phase-3u): closeout report (Markdown artefact)
711329f  phase-3u: implementation-readiness and Phase-4 boundary review (docs-only)
e982d9c  docs(phase-3t): merge closeout + current-project-state sync
56b5b72  Merge Phase 3t (docs-only post-5m diagnostics consolidation and research thread closure memo) into main
fcf8192  docs(phase-3t): closeout report (Markdown artefact)
5842413  phase-3t: post-5m diagnostics consolidation and research thread closure memo (docs-only)
```

## Final rev-parse

- **`git rev-parse main`** (after housekeeping commit + push): the housekeeping commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse origin/main`** (after push): same as `main` above.
- **`git rev-parse HEAD`** (on `main`): same as `main` above.
- **`git rev-parse phase-3u/implementation-readiness-and-phase-4-boundary-review`**: `f31903af800e4ce0ac25f17d56e7f3fa7cc83822` (branch tip preserved).
- **`git rev-parse origin/phase-3u/implementation-readiness-and-phase-4-boundary-review`**: `f31903af800e4ce0ac25f17d56e7f3fa7cc83822`.
- **`git rev-parse phase-3t/post-5m-diagnostics-consolidation`**: `fcf8192e150e7dc783da345d2e54be8cff1611db` (branch tip preserved).
- **`git rev-parse phase-3s/5m-diagnostics-execution`**: `a93695f23d78f8975f33211439d66f8e5c90b49a` (branch tip preserved).
- **`git rev-parse phase-3r/mark-price-gap-governance`**: `06111957e465a4fc5d59190d82db379cc0f7cc86` (branch tip preserved).
- **`git rev-parse phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3` (branch tip preserved).

## main == origin/main confirmation

After the Phase 3u merge push: local `main` = `origin/main` = `f2aba6d6b112bb3d1b3bfb2e47285b9195bcf205`. Synced.

After the post-merge housekeeping commit + push: local `main` = `origin/main` advances to the housekeeping commit's SHA (reported in the chat closeout block accompanying this commit). Synced.

## Readiness conclusion

The Phase 3u review establishes the following readiness conclusion in the project record:

- **Implementation-readiness can help future strategy discovery only indirectly.** Building strategy-agnostic runtime infrastructure (state machine; persistence; risk gates; fake-exchange dry-run; dashboard read model) provides "common ground" that any future strategy would need, plus a forcing function that surfaces specification ambiguities. But it does NOT produce strategy evidence by itself; it does NOT shorten the path to live-readiness; and it does NOT relax framework discipline. The benefit-vs-risk balance does not currently favour authorizing it.
- **Phase 4 (canonical) remains unauthorized.** Canonical Phase 4 framing per `docs/12-roadmap/phase-gates.md` implicitly assumes strategy evidence that the project does not have. Authorizing canonical Phase 4 now would create rhetorical pressure to "have a strategy ready by the end of Phase 4" — exactly the kind of pressure that compromises framework discipline and risks post-hoc loosening of evidence thresholds.
- **Phase 4a remains conditional only and not authorized.** Phase 4a (safe-slice) is a strict subset of Phase 4 limited to strategy-agnostic runtime infrastructure, with no live-readiness implication, no paper-shadow commitment, no exchange-write capability, no production keys, no MCP / Graphify / `.mcp.json` / credentials. It is acceptable as a conditional tertiary alternative subject to explicit anti-live-readiness preconditions, but it is not endorsed over remain-paused.
- **Any future Phase 4a must be local-only / fake-exchange / dry-run / exchange-write-free.** Categorically. Per Phase 3u §10 / §11.2, the prohibitions are: no live exchange-write code paths; no production keys; no authenticated REST or WebSocket calls; no user-stream subscriptions; no paper/shadow execution; no live runtime deployment; no tiny-live or any real-capital exposure; no strategy commitment; no verdict / parameter / threshold / project-lock revision; no MCP / Graphify / `.mcp.json` / credentials. These are binding constraints that any future Phase 4a brief must reaffirm explicitly.
- **Fresh-hypothesis research remains paused for now.** Per Phase 3t §14.2 and Phase 3u §14: three strategy-research arcs have framework-failed under unchanged discipline; starting a fourth without first addressing why the first three failed is procedurally premature; the likelihood of a clean fourth arc passing where three previous arcs failed is bounded; if the operator ever wishes to authorize fresh-hypothesis research, it should be with explicit anti-rescue / anti-circular-reasoning preconditions, predeclared evidence thresholds, and a clear separation from the Phase 3s findings.
- **Pre-coding blockers must be resolved before any coding phase.** Per Phase 3u §8.5, the four currently-OPEN ambiguity-log items are pre-coding blockers regardless of which path the operator eventually selects (Phase 4a, fresh-hypothesis research, or even continued pause). They should be resolved by a separately authorized docs-only ambiguity-resolution memo before any coding phase begins.
- **GAP-20260424-032 is the highest-priority blocker.** *Backtest uses trade-price stops; live uses MARK_PRICE stops.* HIGH risk. The §1.7.3 mark-price-stops lock and the Phase 3s Q6 D1-A finding (mark-price stops trigger ~1.3–1.8 5m bars after trade-price stops would have triggered) are now both on record and must be reconciled in any future runtime stop-handling specification. This is the most operationally significant OPEN item.
- **Recommended state remains paused.** Across 11 prior phases (3k → 3u), the cumulative recommendation has been remain paused. Phase 3u reinforces that recommendation with a forward-looking implementation-readiness review.

## Pre-coding blocker summary

The four currently-OPEN ambiguity-log items (per `docs/00-meta/implementation-ambiguity-log.md`):

| ID | Title | Risk | Pre-coding-blocker classification |
|---|---|---|---|
| **GAP-20260424-032** | Backtest uses trade-price stops; live uses MARK_PRICE stops | **HIGH** | Pre-coding blocker for any future runtime; pre-paper-shadow blocker for any live work. **Highest priority.** |
| GAP-20260424-030 | Break-even rule text conflicts with spec Open Question #8 | MEDIUM | Pre-coding blocker for any future runtime that implements break-even logic. |
| GAP-20260424-031 | EMA slope wording ambiguous: discrete comparison vs. fitted slope | LOW-MEDIUM | Pre-coding blocker for any future runtime that re-implements EMA bias. |
| GAP-20260424-033 | Stagnation window not in Open Questions but discussed as metric | LOW | Documentation hygiene item; weak pre-coding blocker. |

Phase 3u recommends that any operator decision to move toward implementation work be preceded by a docs-only ambiguity-resolution memo that resolves at minimum GAP-20260424-032 (and ideally the other three). Phase 3u does not authorize that ambiguity-resolution phase; it recommends it.

In addition, several ACCEPTED_LIMITATION items (e.g., GAP-20260419-018 taker commission rate parameterization; GAP-20260419-020 ExchangeInfo snapshot proxy; GAP-20260419-024 leverageBracket placeholder limitation) are not pre-coding blockers in the strict sense but should be reviewed before any tiny-live transition, as already documented in the technical-debt register.

## Forbidden-work confirmation

- **No Phase 3v / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No Phase 4 / Phase 4a started.** Phase 3u recommends Phase 4 remain unauthorized and Phase 4a remain conditional only; the merge does not change those recommendations into authorizations.
- **No implementation code written.** Phase 3u is text-only; the merge brings in pre-existing Phase 3u artefacts unchanged.
- **No runtime / strategy / execution / risk / database / dashboard / exchange code modified.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun. No new diagnostic computation.
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- **No strategy / parameter / threshold / project-lock / prior-verdict modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **No verdict revision.**
- **No strategy rescue proposal.** R2 / F1 / D1-A successors not proposed.
- **No new strategy candidate proposal.**
- **No 5m strategy / hybrid / variant / retained-evidence successor created.**
- **No paper/shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket subscription.**
- **No public endpoints consulted.** This merge + housekeeping commit performs no network I/O.
- **No secrets requested or stored.**

## Remaining boundary

- **main HEAD:** the housekeeping commit (SHA reported in chat closeout). After the merge: `f2aba6d`. Phase 3u review memo + closeout consolidated on `main`.
- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a (safe slice) remains conditional only and not authorized. Pre-coding blockers (4 OPEN ambiguity-log items, especially GAP-20260424-032) recorded as items to be resolved before any future coding phase.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:**
  - `phase-3u/implementation-readiness-and-phase-4-boundary-review` pushed at `f31903a`. Commits in main via Phase 3u merge.
  - `phase-3t/post-5m-diagnostics-consolidation` pushed at `fcf8192`; commits in main via Phase 3t merge.
  - `phase-3s/5m-diagnostics-execution` pushed at `a93695f`; commits in main via Phase 3s merge.
  - `phase-3r/mark-price-gap-governance` pushed at `0611195`; commits in main via Phase 3r merge.
  - `phase-3q/5m-data-acquisition-and-integrity-validation` pushed at `3078b44`; commits in main via Phase 3r merge.

## Next authorization status

**No next phase has been authorized.** Phase 3u recommended Option A (remain paused) as primary; Option B (docs-only ambiguity-resolution memo, especially resolving GAP-20260424-032) as conditional secondary that produces unconditional documentation value but is not endorsed over remain-paused; Option C (docs-only Phase 4a safe-slice scoping memo) as conditional tertiary subject to explicit anti-live-readiness preconditions; Options D (fresh-hypothesis research) and E (Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write) NOT recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
