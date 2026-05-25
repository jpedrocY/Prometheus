# Phase 4bm-R — Merge-Closeout

**Phase identity:** Phase 4bm-R — Multi-Day V002 Label-Family Research-Use Decision Memo.
**Tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section merge-closeout).
**Date:** 2026-05-25.
**Status:** **merge-complete on `main`**.

---

## 1. Phase identity

- **Phase:** Phase 4bm-R — Multi-Day V002 Label-Family Research-Use Decision Memo.
- **Type:** docs-only research-use decision / governance memo (multi-day v002 analogue of Phase 4bj-F).
- **Action:** merge into `main`.
- **Merge purpose:** record on `main` the Phase 4bm-R policy-level research-use admissibility decision for the multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002`, making the phase project-complete. The phase itself records a *recommendation* only; it performs no manifest mutation, no successor-state recording, and no data work.
- **Target branch:** `main`.
- **Source branch:** `phase-4bm-r/multi-day-v002-label-family-research-use-decision-memo`.

## 1a. Required exact phrases

- **Phase 4bm-R is now merge-complete on main.**
- **Phase 4bm-R decision result is RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION.**
- **Phase 4bm-R is a docs-only label-family research-use decision memo.**
- **Phase 4bm-R does not mutate any manifest.**
- **Phase 4bm-R does not create successor-state JSON.**
- **Phase 4bm-R does not define chronological split policy.**
- **Phase 4bm-R does not authorize diagnostics, ML, strategy, or backtests.**
- **Phase 4bm-R does not authorize acquisition.**
- **Phase 4bm-R does not commit data/microstructure.**
- **LABEL_GATE_PASS from Phase 4bm-Q remains report-level evidence only.**
- **Label-family research-use is not recorded by Phase 4bm-R.**
- **Any label-family research-use recording requires a separately authorized successor-state phase.**
- **Phase 4bm-S is not authorized by Phase 4bm-R.**
- **Recommended state remains paused.**

## 2. SHAs

- **`main` SHA before merge (base SHA):** `219c8b0d1f7e74c596ecc9aa50662101dc59a9d3` (Phase 4bm-Q merge-closeout SHA-finalization commit; pre-branch `main == origin/main`).
- **Branch tip SHA before merge:** `fbb8ad4132e1615029de1797f66464163baeb3e7` — `docs(phase-4bm-r): decide label-family research-use recommendation` (the single Phase 4bm-R docs commit: decision memo + closeout + narrow `current-project-state.md` update).
- **Merge commit SHA:** `1c132f35b8afe759b1da3f5cd6fe584187dfc35b` — `docs(phase-4bm-r): merge label-family research-use decision`. Merge strategy: `--no-ff` (true merge commit via `ort`; preserves the branch in history).
- **Merge-closeout commit SHA (this memo, initial commit on `main`):** `c0630b95e5c0995cce42d484c873ab6cc52bc230` — `docs(phase-4bm-r): add merge closeout`.
- **SHA-finalization commit SHA (the follow-on commit finalizing this §2, i.e. this edit):** per prior-phase repo convention (Phase 4bm-Q / 4bm-P / 4bm-O merge-closeout SHA-finalization), the SHA-finalization commit's own SHA is **not** self-referenced inside this memo (it cannot be known at edit time without amending the commit it is supposed to record); it is captured in the final operator report and in `git log` immediately after this memo edit is committed as `docs(phase-4bm-r): finalize merge closeout shas`.
- **Final `main` / `origin/main` SHA after the SHA-finalization push:** equal to the SHA-finalization commit SHA above; recorded in the final operator report and in `git log`. After this commit, `main == origin/main`, and the final `main` SHA equals the final `origin/main` SHA.

## 3. Merge method

- `git merge --no-ff phase-4bm-r/multi-day-v002-label-family-research-use-decision-memo -m "docs(phase-4bm-r): merge label-family research-use decision"`.
- Strategy: `ort` (default).
- Push status: pushed to `origin/main` with **no force, no skip-hooks, no skip-signing** (`--no-verify` not used; `--no-gpg-sign` not used; `-c commit.gpgsign=false` not used).

## 4. Files brought forward by the merge

Total: **3 files changed, 906 insertions(+), 551 deletions(-)**.

### Docs (3)

- **Added** — `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-r_multi-day-v002-label-family-research-use-decision-memo.md`
- **Added** — `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-r_closeout.md`
- **Modified** — `docs/00-meta/current-project-state.md` (new Phase 4bm-R narrative paragraph + new "Current phase:" block; prior Phase 4bm-Q "Current phase:" block preserved as labelled historical context, replacing the previously-historical Phase 4bm-P block).

### Source (0) / Tests (0) / Scripts (0) / Config (0)

None.

**No `data/microstructure/` file was modified.** No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition + Current/Prior phase block rotation. No prior source / test / script was modified. The diff matches the expected change set from the authorization prompt exactly (2 `A` + 1 `M`).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 935 +++++++++------------
 .../2026-05-25_phase-4bm-r_closeout.md             | 147 ++++
 ...v002-label-family-research-use-decision-memo.md | 375 +++++++++
 3 files changed, 906 insertions(+), 551 deletions(-)
```

The `current-project-state.md` churn (935 changed lines) reflects the documented Current/Prior phase block rotation: the Phase 4bm-Q "Current phase:" block was demoted to "Prior phase (historical context):" (replacing the previously-historical Phase 4bm-P block) and a new Phase 4bm-R "Current phase:" block was inserted, plus the new Phase 4bm-R narrative paragraph. Net +384 lines. The diff matches the expected change set.

## 6. Result / verdict

**MEMO RECORDED — RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION.**

Phase 4bm-R is a docs-only governance decision memo that evaluated the multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 40-column locked v002 label schema) against thirteen decision criteria (A–M), all of which PASS on the strength of the Phase 4bm-M boundary design + Phase 4bm-N schema finalization + Phase 4bm-O local label artefact generation + Phase 4bm-P `LABEL_STRUCTURAL_QA_PASS` + Phase 4bm-Q `LABEL_GATE_PASS` (60 / 60 at report level) evidence chain, plus the already-cleared upstream feature family (Phase 4bm-K → Phase 4bm-L `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`). **Phase 4bm-R decision result is RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION.** The recommendation means only that the project may, separately and explicitly, authorize a future multi-day v002 label-family research-use successor-state recording phase (multi-day analogue of Phase 4bj-G) to record a machine-readable admissibility marker as a sibling successor-state JSON while preserving the original label manifest byte-identically. **Label-family research-use is not recorded by Phase 4bm-R.** The v002 label manifest remains `research_eligible=false`, `eligibility_gate_status="pending"`, `stage_5_label_cleared=false`, `label_family_research_use_authorized=false`, `chronological_split_policy="not_yet_defined"`. **Recommended state remains paused.**

## 7. Local gitignored outputs

**None produced by Phase 4bm-R.** Phase 4bm-R is docs-only and created no file under `data/microstructure/`.

The Phase 4bm-Q gate report (locked input evidence, not produced by Phase 4bm-R) was read-only re-hashed during Phase 4bm-R review and during this merge:

| Output | Path | SHA256 | Bytes | Committed? | gitignore |
|---|---|---|---|---|---|
| Phase 4bm-Q gate report JSON | `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json` | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | 20,259 | **No** | `.gitignore:85: data/microstructure/` |
| Phase 4bm-Q gate report sidecar | `<report>.sha256` | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | 156 | **No** | `.gitignore:85: data/microstructure/` |

Both SHAs match the values recorded in the Phase 4bm-Q merge-closeout byte-for-byte.

## 8. Validation results

Run from `C:\Prometheus`:

| Command | Result |
|---|---|
| `git status --short` (pre-merge, on phase branch) | only `data/research/` untracked (expected) |
| `git rev-parse main` (pre-merge) | `219c8b0d1f7e74c596ecc9aa50662101dc59a9d3` |
| `git rev-parse origin/main` (pre-merge) | `219c8b0d1f7e74c596ecc9aa50662101dc59a9d3` (in sync) |
| `git rev-parse phase-4bm-r/...` (pre-merge) | `fbb8ad4132e1615029de1797f66464163baeb3e7` (branch tip) |
| `git diff --stat main..phase-4bm-r/...` | 3 files changed, 906 insertions(+), 551 deletions(-) — matches closeout inventory |
| `git diff --name-status main..phase-4bm-r/...` | `M current-project-state.md`, `A 2026-05-25_phase-4bm-r_closeout.md`, `A 2026-05-25_phase-4bm-r_multi-day-v002-label-family-research-use-decision-memo.md` (1 `M` + 2 `A`) |
| `git diff --check main..phase-4bm-r/...` | clean (exit 0; no whitespace / conflict markers) |
| `Get-FileHash <Phase 4bm-Q gate report>` | SHA256 `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (matches expected) |
| `Get-FileHash <Phase 4bm-Q gate report sidecar>` | SHA256 `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (matches expected) |
| `git check-ignore -v <gate report>` | `.gitignore:85: data/microstructure/` (gitignored) |
| `git check-ignore -v <gate report sidecar>` | `.gitignore:85: data/microstructure/` (gitignored) |
| `git merge --no-ff phase-4bm-r/...` | merged via `ort` strategy; merge commit `1c132f35…` |
| `git status --short` (post-merge, on main) | only `data/research/` untracked (no `data/microstructure/` entry) |

No test / lint / type-check was run: Phase 4bm-R is a pure docs-only memo touching no source / test / script / config / data surface, so the project standard requires no test / lint / type-check coverage for this phase, and none is claimed. No markdown-lint result is invented (no repo markdown-lint standard was invoked).

## 9. Upstream immutability evidence

Phase 4bm-R is docs-only and mutates no `data/microstructure/` artefact. The single artefact family read (read-only) is the Phase 4bm-Q gate report + sidecar, both byte-identical pre/post:

| Artefact | Pre/Post SHA256 |
|---|---|
| Phase 4bm-Q gate report JSON | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (identical) |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (identical) |

All other upstream artefacts (v002 label manifest `5e17074d…` + sidecar `451d5b88…`; v002 feature manifest `512a0a54…` + sidecar `22e2fb77…`; Phase 4bm-J feature-family gate report `3c59dfae…` + sidecar `14a17764…`; Phase 4bm-L feature-family successor-state `7eccaa8f…` + sidecar `c2b73330…`; v002 derived manifest `01c5fa53…`; v002 raw manifest `01696786…`; Phase 4bm-D derived gate report `3b45e70b…`; Phase 4bm-F derived successor-state `72b6edd4…`; Phase 4bl-D-R raw gate report `f9493fd1…`; Phase 4bl-E raw successor-state `a0576ca6…`; 90 label parquets + 90 label sidecars) were not accessed for write by Phase 4bm-R and remain at the SHAs recorded in the Phase 4bm-Q merge-closeout.

## 10. Manifest state preservation

| Manifest | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Other |
|---|---|---|---|---|
| v002 label manifest | `false` (unchanged) | `"pending"` (unchanged) | `"not_yet_defined"` (unchanged) | `stage_5_label_cleared=false`, `label_family_research_use_authorized=false`, `label_family_eligibility_gate_authorized=false` (all unchanged) |
| v002 feature manifest | `false` (unchanged) | `"pending"` (unchanged) | n/a | `stage_4_feature_cleared=false` (unchanged) |
| v002 derived/normalized manifest | `false` (unchanged) | `"pending"` (unchanged) | n/a | — |
| v002 raw manifest | `false` (unchanged) | `"pending"` (unchanged) | n/a | — |

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked by Phase 4bm-R or its merge).

## 11. Boundary confirmations

- no source code modified
- no test modified
- no script modified
- no `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file modified
- no v002 label parquet / label manifest / label sidecar modified
- no v002 feature parquet / feature manifest / feature sidecar modified
- no Phase 4bm-J / 4bm-D / 4bl-D-R gate report, Phase 4bm-L / 4bm-F / 4bl-E successor-state, or any prior gate report / successor-state artefact modified
- no `data/microstructure/` write occurred
- no `data/microstructure/` artefact committed
- no label-family successor-state JSON created
- no replacement parquet / manifest / sidecar / gate report / successor-state created
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `stage_5_label_cleared` / `label_family_research_use_authorized` / `label_family_eligibility_gate_authorized` / `stage_4_feature_cleared` set on any actual manifest
- no `chronological_split_policy` changed on any actual manifest
- no ML model trained / architecture designed / feature ranked / meta-labeling created
- no strategy created or strategy signal computed
- no backtest run
- no data acquired; no public endpoint called; no Binance API called; no WebSocket opened; no credential / `.env` / `.mcp.json` / MCP / Graphify used
- no normalizer / raw eligibility gate / derived-family gate / feature kernel / feature-family eligibility gate / label kernel / label-family eligibility gate rerun
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## 12. Retained verdict ledger

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-R)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks
- Phase 4bm-A-P1 context management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results (Phase 4am .. Phase 4bm-Q) preserved verbatim.

## 14. No-rescue constraints

The Phase 4bm-R merge does **not**, and **cannot**, be construed as authorising:

- Phase 4bm-S or any multi-day v002 label-family research-use successor-state recording;
- multi-day v002 chronological-split-policy memo or chronological-split-policy successor-state recording;
- ML model training, model selection, strategy hypothesis generation, or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state, entry / exit rules, or backtest design;
- diagnostics of any kind;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` from this decision memo alone;
- creating any successor-state JSON;
- MCP / Graphify / `.mcp.json` / credentials / authenticated APIs / private endpoints / user streams / WebSockets / production keys.

**LABEL_GATE_PASS from Phase 4bm-Q remains report-level evidence only.** **Label-family research-use is not recorded by Phase 4bm-R.** **Any label-family research-use recording requires a separately authorized successor-state phase.**

## 15. Successor authorization

**None.**

The following candidate successors are **NOT** authorized by the Phase 4bm-R merge:

- Phase 4bm-S — multi-day v002 label-family research-use successor-state recording (multi-day analogue of Phase 4bj-G)
- multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / -I)
- multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J)
- multi-day v002 diagnostics
- multi-day v002 ML implementation / training / model selection / feature ranking / meta-labeling
- multi-day v002 strategy specification / implementation / signal construction
- multi-day v002 backtest specification / plan / execution
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot / cross-venue / multi-symbol / additional-day data acquisition
- Phase 4bn-* / 4bo-* / 4bp-* / 4bq-*
- Phase 5
- Phase 4 canonical
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- user stream
- WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials

**Phase 4bm-S is not authorized by Phase 4bm-R.**

## 16. Recommended state

**Remain paused.** **Recommended state remains paused.**

Phase 4bm-R is now merge-complete on `main`. No successor phase is authorized.

**Conditional next, NOT authorized:**

A future multi-day v002 label-family research-use successor-state recording phase (informally Phase 4bm-S; multi-day analogue of Phase 4bj-G) is the cleanest non-paused option. It would, if separately authorized by the operator under explicit ex-ante scope, produce exactly one sibling successor-state JSON artefact + paired canonical Phase 4bb-F sidecar under a gitignored `data/microstructure/successor-state/labels/` namespace recording a machine-readable label-family research-use admissibility marker, while preserving the original v002 label manifest byte-identically (SHA `5e17074d…` unchanged) and lifting no forbidden flag on any manifest. Phase 4bm-S is **not** authorized by this merge. Per the Phase 4bk-A workflow standard, a separately authorized operator prompt is required before any successor begins.

---

**Phase 4bm-R is now merge-complete on main.** **Phase 4bm-R decision result is RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION.** **Phase 4bm-R is a docs-only label-family research-use decision memo.** **Phase 4bm-R does not mutate any manifest.** **Phase 4bm-R does not create successor-state JSON.** **Phase 4bm-R does not define chronological split policy.** **Phase 4bm-R does not authorize diagnostics, ML, strategy, or backtests.** **Phase 4bm-R does not authorize acquisition.** **Phase 4bm-R does not commit data/microstructure.** **LABEL_GATE_PASS from Phase 4bm-Q remains report-level evidence only.** **Label-family research-use is not recorded by Phase 4bm-R.** **Any label-family research-use recording requires a separately authorized successor-state phase.** **Phase 4bm-S is not authorized by Phase 4bm-R.** **Recommended state remains paused.**
