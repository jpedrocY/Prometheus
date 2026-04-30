# Phase 3r Merge Closeout

## Summary

Phase 3r — the docs-only **mark-price gap governance memo** (Phase 3p §10 / Phase 3q decision menu Option B) — has been merged to `main` and pushed to `origin/main`. Because the Phase 3r branch was created from the Phase 3q branch tip (rather than from `main`), the Phase 3r merge transitively brings the two Phase 3q commits (`8d99375` acquisition + integrity-validation; `3078b44` closeout) into `main` for the first time. The merge therefore consolidates the entire post-Phase-3p / pre-diagnostics-execution sub-arc (Phase 3q acquisition evidence + Phase 3r governance) in a single `--no-ff` merge commit on `main`.

**Recommendation preserved: Option B (known invalid-window exclusion for Q6 only).** Phase 3p §4.7 strict integrity gate stays unchanged. Mark-price 5m datasets remain `research_eligible: false`. The Phase 3q manifests are not modified. The four upstream `data.binance.vision` maintenance-window gaps (BTC: 2022-07-30/31, 2022-10-02, 2023-02-24, 2023-11-10; ETH: 2022-07-12, 2022-10-02, 2023-02-24, 2023-11-10) remain exclusion zones, not patch zones. Phase 3r §8 specifies the full normative Q6 invalid-window exclusion rule (no forward-fill / interpolation / imputation / replacement; per-trade exclusion test based on Q6 analysis-window intersection; excluded counts reported by candidate / symbol / side / exit-type / gap-window; Q6 conclusions labeled "conditional on valid mark-price coverage"; no automatic prior-verdict revision; no strategy rescue / parameter change / live-readiness implication; no silent §8 rule revision; per-trade exclusion algorithm must be predeclared in any future diagnostics-execution phase brief) that any future Q6-running phase must obey *if* Q6 is ever authorized.

**Q6 disposition: bounded-conditional optionality.** Q6 stays on the menu but only as a §8-bounded option. Q6 is NOT permanently retired. Q6 is NOT currently authorized.

**No diagnostics, Q1–Q7 answers, backtests, prior-verdict revisions, threshold revisions, project-lock revisions, strategy-parameter changes, data acquisition, data patching, manifest modifications, Phase 3p §4.7 amendments, mark-price `research_eligible` flag flips, 5m strategy / hybrid / variant creations, paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work occurred.** Recommended state remains **paused**. **No successor phase has been authorized.**

## Files changed

The Phase 3r merge into `main` brought in five new files (the Phase 3q + Phase 3r artefacts that previously existed only on their respective branches):

- `scripts/phase3q_5m_acquisition.py` — standalone Phase 3q orchestrator (public-bulk-archive only; no credentials; no Interval-enum extension; no modification to `prometheus.research.data.*`).
- `docs/00-meta/implementation-reports/2026-04-30_phase-3q_5m-data-acquisition-and-integrity-validation.md` — Phase 3q acquisition + integrity-validation report.
- `docs/00-meta/implementation-reports/2026-04-30_phase-3q_closeout.md` — Phase 3q closeout artefact.
- `docs/00-meta/implementation-reports/2026-04-30_phase-3r_mark-price-gap-governance-memo.md` — Phase 3r governance memo with §8 Q6 invalid-window exclusion rule.
- `docs/00-meta/implementation-reports/2026-04-30_phase-3r_closeout.md` — Phase 3r closeout artefact.

The post-merge housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-3r_merge-closeout.md` — this file.
- `docs/00-meta/current-project-state.md` — narrow update recording Phase 3q acquisition evidence, Phase 3r governance decision, final main/origin sync after merge, recommended state paused, no next phase authorized. Stale "Current phase" and "Most recent merge" code blocks refreshed to point at the Phase 3r merge.

NOT modified by this merge or by the housekeeping commit:

- All `data/manifests/*.manifest.json` files — including v002 manifests and the four Phase 3q v001-of-5m manifests (mark-price `research_eligible: false` flag preserved).
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions — git-ignored per repo convention; v002 partitions untouched on local filesystem.
- All `src/prometheus/**` source code — including `src/prometheus/core/intervals.py` (Interval enum NOT extended).
- All other scripts under `scripts/` (only `phase3q_5m_acquisition.py` is new; others untouched).
- All `tests/**` — untouched.
- All `.claude/rules/**` — untouched.
- All Phase 3o / 3p memos — untouched (Phase 3p §4.7 NOT amended).

## Phase 3q commits included

The Phase 3r merge transitively brings the following Phase 3q branch commits into `main`:

| Commit | Subject |
|---|---|
| `8d99375c39ab25508b800b8378996d40290f03dc` | `phase-3q: 5m data acquisition + integrity validation (docs-and-data, partial pass)` — orchestrator script + acquisition + integrity-validation report. |
| `3078b448e5850f943079899c9048b2c19e07adb3` | `docs(phase-3q): closeout report (Markdown artefact replacing chat-only closeout)` — Phase 3q closeout. |

Phase 3q is therefore consolidated into `main` without a separate Phase 3q merge commit, since the Phase 3r branch was forked from `3078b44` and includes the Phase 3q ancestry.

## Phase 3r commits included

| Commit | Subject |
|---|---|
| `0082488c3238fcd35330603b7a4d08601771f79c` | `phase-3r: mark-price gap governance memo (docs-only)` — Phase 3r governance memo with §8 rule. |
| `06111957e465a4fc5d59190d82db379cc0f7cc86` | `docs(phase-3r): closeout report (Markdown artefact)` — Phase 3r closeout. |

## Merge commit

- **Phase 3r merge commit (`--no-ff`, ort strategy):** `3cf2ba200e2d107a01a499e22ddc4d55dce32adb`
- **Merge title:** `Merge Phase 3r (docs-only mark-price gap governance memo + Phase 3q acquisition evidence) into main`
- **Files added by the merge:** 5 (above). Total: 1 770 insertions.

## Housekeeping commit

The post-merge housekeeping commit adds this Phase 3r merge-closeout file and updates `current-project-state.md` narrowly. Its SHA advances `main` by one further commit beyond the merge commit `3cf2ba2` and is reported in the chat closeout block accompanying this commit. Per prior phase pattern (Phase 3k / 3l / 3m / 3n / 3o / 3p), the housekeeping commit's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged.

## Final git status

```text
clean
```

Working tree empty after the post-merge housekeeping commit. No uncommitted changes. No untracked files.

## Final git log --oneline -8

Snapshot at the housekeeping commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this housekeeping commit itself is committed>  docs(phase-3r): merge closeout + current-project-state sync
3cf2ba2  Merge Phase 3r (docs-only mark-price gap governance memo + Phase 3q acquisition evidence) into main
0611195  docs(phase-3r): closeout report (Markdown artefact)
0082488  phase-3r: mark-price gap governance memo (docs-only)
3078b44  docs(phase-3q): closeout report (Markdown artefact replacing chat-only closeout)
8d99375  phase-3q: 5m data acquisition + integrity validation (docs-and-data, partial pass)
9428b05  docs(phase-3p): merge closeout + current-project-state sync
b78ee63  Merge Phase 3p (docs-only 5m diagnostics data-requirements and execution-plan memo) into main
```

## Final rev-parse

- **`git rev-parse main`** (after housekeeping commit + push): the housekeeping commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse origin/main`** (after push): same as `main` above.
- **`git rev-parse HEAD`** (on `main`): same as `main` above.
- **`git rev-parse phase-3r/mark-price-gap-governance`**: `06111957e465a4fc5d59190d82db379cc0f7cc86` (branch tip preserved).
- **`git rev-parse origin/phase-3r/mark-price-gap-governance`**: `06111957e465a4fc5d59190d82db379cc0f7cc86`.
- **`git rev-parse phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3` (branch tip preserved).
- **`git rev-parse origin/phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3`.

## main == origin/main confirmation

After the Phase 3r merge push: local `main` = `origin/main` = `3cf2ba200e2d107a01a499e22ddc4d55dce32adb`. Synced.

After the post-merge housekeeping commit + push: local `main` = `origin/main` advances to the housekeeping commit's SHA (reported in the chat closeout block accompanying this commit). Synced.

## Forbidden-work confirmation

- **No Phase 3s / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question answered. No diagnostic table, plot, or classification produced.
- **No Q1–Q7 answers.**
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
- **No data acquisition / download / patch / regeneration / modification.** Phase 3r is text-only; the merge brings in pre-existing Phase 3q artefacts unchanged.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim; the four Phase 3q v001-of-5m manifests retain their committed content (mark-price still `research_eligible: false`).
- **No v002 dataset / manifest modification.** v002 partitions and manifests untouched.
- **No mark-price 5m manifest re-issue.** `research_eligible: false` flag remains on `binance_usdm_btcusdt_markprice_5m__v001.manifest.json` and `binance_usdm_ethusdt_markprice_5m__v001.manifest.json`. NOT flipped to `true`.
- **No Phase 3p §4.7 amendment.** Phase 3p §4.7 strict integrity gate stands as-written.
- **No strategy / parameter / threshold / project-lock / prior-verdict modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **No 5m strategy / hybrid / variant created.**
- **No Phase 4 / paper/shadow / live-readiness / deployment / production-key / exchange-write paths touched.**
- **No MCP / Graphify / `.mcp.json` / credentials.**
- **No private Binance endpoints / user stream / WebSocket subscription / public endpoints consulted.** This merge + housekeeping commit performs no network I/O.
- **No secrets requested or stored.**

## Remaining boundary

- **main HEAD:** the housekeeping commit (SHA reported in chat closeout). After the merge: `3cf2ba2`. Phase 3q acquisition evidence + Phase 3r governance now consolidated on `main`.
- **Recommended state:** **paused.**
- **5m research thread state:** Phase 3o predeclared Q1–Q7 + forbidden forms + diagnostic terms + analysis boundary; Phase 3p added data-requirements + dataset-versioning approach + manifest specification + per-question outputs + outcome-interpretation rules; Phase 3q acquired the 5m datasets and ran integrity checks (trade-price PASS, mark-price FAIL strict gate); Phase 3r added the mark-price gap governance memo + Phase 3r §8 Q6 invalid-window exclusion rule. The thread now has a complete, predeclared, immutable specification covering questions, data, governance, and outcome-interpretation. Whether to *act on* the specification is a separate operator-strategic decision.
- **Trade-price 5m datasets:** locally research-eligible; Q1, Q2 (trade-price-side), Q3, Q4, Q5 unaffected by Phase 3r §8.
- **Mark-price 5m datasets:** NOT research-eligible under Phase 3p §4.7 strict gate. Q6 is conditionally permitted under Phase 3r §8 *only*.
- **Project locks preserved verbatim.**
- **Phase 3q branch:** `phase-3q/5m-data-acquisition-and-integrity-validation` remains pushed at `3078b44`. Its commits are now reachable from `main` via the Phase 3r merge ancestry.
- **Phase 3r branch:** `phase-3r/mark-price-gap-governance` remains pushed at `0611195`. Its commits are now reachable from `main` via the Phase 3r merge ancestry.

## Next authorization status

**No next phase has been authorized.** Phase 3r recommends Option A (adopt §8; remain paused) as primary; Option B (adopt §8 AND authorize a future docs-only diagnostics-execution phase, with operator-explicit Q6 disposition) as conditional secondary; Options C / D / E / F (Q6-only run / §4.7 amendment combo / permanent Q6 retirement / strategy rescue / Phase 4 / paper/shadow / live-readiness / deployment) NOT recommended. Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
