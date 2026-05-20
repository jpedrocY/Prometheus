# Phase 4bm-E Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo
- **Tier**: Tier 1 (docs-only Full Phase; governance / research-eligibility decision memo; multi-day analogue of Phase 4bg-A for the v002 derived family)
- **Type**: docs-only research-eligibility decision / governance memo — adds two new tracked docs files under `docs/00-meta/implementation-reports/` and narrowly updates `docs/00-meta/current-project-state.md`; no source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-E as project-complete on `main` after a clean docs-only branch that interprets the Phase 4bm-D `DERIVED_GATE_PASS` evidence and records Option B / Decision form 2 — Stage-3 admissible in principle at policy level for the multi-day v002 normalized / derived family, with no manifest mutation in this phase and a separately authorized successor-state recording phase (Phase 4bm-F) required before any machine-readable `research_eligible = true` marker exists for the v002 derived family
- **Branch merged**: `phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo`
- **Target branch**: `main`
- **Base**: `main` at `8234375f927f029211747eeae4ef493c612b2df3` (Phase 4bm-D-P1 merge-closeout commit)
- **Predecessor**: Phase 4bm-D-P1 (Lightweight Claude Code Workspace Execution Standard, project-complete on `main`)

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-E is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `8234375f927f029211747eeae4ef493c612b2df3`
- **Pre-merge `origin/main` SHA**: `8234375f927f029211747eeae4ef493c612b2df3` (in sync; `git pull --ff-only` reported `Already up to date.`)
- **Phase 4bm-E branch docs commit SHA**: `1715a8adaa6eeeb478c7af363ed39af311783773` (`docs(phase-4bm-e): add multi-day derived family research eligibility decision memo`; 3 files / +1,241 / -0; single commit on branch)
- **Phase 4bm-E branch tip SHA pre-merge**: `1715a8adaa6eeeb478c7af363ed39af311783773`
- **Merge commit SHA**: `fcc1bd044d274c99520b4ab15282046e1428b3d0`
- **Merge commit message**: `docs(phase-4bm-e): merge multi-day derived-family research eligibility decision memo`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `fcc1bd044d274c99520b4ab15282046e1428b3d0`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `fcc1bd044d274c99520b4ab15282046e1428b3d0` (in sync)
- **Merge-closeout commit SHA**: `d6acae535fee19a074096e3d7fa3590f4a0dd9ec` (`docs(phase-4bm-e): add merge closeout`; 1 file / +364 / -0; this file's commit on `main`)
- **Post-merge-closeout-commit `main` SHA**: `d6acae535fee19a074096e3d7fa3590f4a0dd9ec`
- **Post-merge-closeout-commit `origin/main` SHA**: `d6acae535fee19a074096e3d7fa3590f4a0dd9ec` (pushed cleanly via `fcc1bd0..d6acae5  main -> main`; no force, no skip-hooks, no skip-signing)
- **Final `main == origin/main`**: true (both at `d6acae535fee19a074096e3d7fa3590f4a0dd9ec`)

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo -m "docs(phase-4bm-e): merge multi-day derived-family research eligibility decision memo"`
- **Strategy**: `ort` (git default; reported by git as `Merge made by the 'ort' strategy.`)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     8234375..fcc1bd0  main -> main
  ```
  Second push (this merge-closeout commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     fcc1bd0..d6acae5  main -> main
  ```

## §4 Files Brought Forward by the Merge

Three tracked files brought forward from the Phase 4bm-E branch into `main`, all from the single source-branch commit (`1715a8a`).

**Tracked files added (2):**

1. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-e_multi-day-derived-family-research-eligibility-decision-memo.md` (NEW, +653; the 31-section main memo)
2. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-e_closeout.md` (NEW, +207; Phase 4bm-E closeout)

**Tracked files modified narrowly (1):**

3. `docs/00-meta/current-project-state.md` (MODIFIED, +381 / -0; Phase 4bm-E narrative paragraph + new "Current phase:" block; prior Phase 4bm-D-P1 "Current phase:" block preserved verbatim as labelled historical context — pure addition, no deletions, consistent with the Phase 4bm-D-P1 precedent pattern)

**This merge-closeout commit — 1 additional tracked file (allowed by the operator authorization for the merge phase):**

4. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-e_merge-closeout.md` (NEW; this file)

**Explicit non-changes:** No `data/microstructure/` file was modified, added, or deleted. No `data/research/` file was committed. No file under `src/prometheus/`, `tests/`, `scripts/`, or any other source / test / script surface was modified. No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP file (`.mcp.json` absent before and after), or `.claude/settings.json` / `.claude/settings.local.json` / `.claude/hooks/` / `.claude/agents/` file in `C:\Prometheus` was modified or created. No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph + new "Current phase:" block addition. No prior implementation report, closeout, or merge-closeout was modified. No prior process standard was modified. No manifest, sidecar, gate report, normalized parquet, derived parquet, raw zip, acquisition log, successor-state JSON, feature parquet, label parquet, or any other data artefact was modified.

## §5 Diff Summary

```text
 docs/00-meta/current-project-state.md              | 381 ++++++++++++
 .../2026-05-18_phase-4bm-e_closeout.md             | 207 +++++++
 ...ed-family-research-eligibility-decision-memo.md | 653 +++++++++++++++++++++
 3 files changed, 1241 insertions(+)
```

- 3 files changed
- 1,241 insertions
- 0 deletions
- The merge diff exactly matches the expected change set from the authorization prompt (2 added + 1 modified = 3 tracked files; no `data/microstructure/` files; no source / test / script / configuration files).
- `git diff --check` clean across the branch and post-merge (no whitespace errors; no unresolved merge markers).

## §6 Result / Verdict

**MEMO RECORDED — Phase 4bm-E Multi-Day Derived-Family Research-Eligibility Decision Memo (Option B / Decision form 2) recorded on `main`; Phase 4bm-E is project-complete on `main`.**

Phase 4bm-E is a docs-only Tier 1 research-eligibility decision memo — the multi-day analogue of Phase 4bg-A for the v002 derived family. It interprets the Phase 4bm-D authoritative gate evidence (`overall_status = pass`; `gate_verdict = DERIVED_GATE_PASS`; 60 / 60 checks PASS; 19 / 19 boundary confirmations `True`; `research_eligible_after = False`; `eligibility_gate_status_after = "pass"` report-level only; `no_successor_authorization = True`; report SHA256 `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a`; sidecar SHA256 `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711`; `code_commit_sha = 57e1c97e6e938797d448b331cdc27b50b8e935dd`) plus the Phase 4bm-B Stage-0 (90 per-day v002 Parquets + 90 sidecars + v002 multi-day index manifest), Phase 4bm-C Stage-1 (56 / 56 multi-day structural QA PASS), Phase 4bl-D-R raw multi-day `RAW_MULTIDAY_GATE_PASS`, and Phase 4bl-E raw multi-day successor-state JSON evidence, and records **Option B / Decision form 2**: Stage-3 is admissible in principle at policy level for the multi-day v002 normalized / derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events; ~1.40 GiB), but **no manifest mutation occurs in Phase 4bm-E**, and a separately authorized successor-state recording phase (**Phase 4bm-F**; multi-day analogue of Phase 4bg-B) is required before any machine-readable `research_eligible = true` marker exists for the v002 derived family. Phase 4bm-E confirms all 15 Stage-3 admissibility criteria are satisfied at the policy level for v002; records that the v002 evidence chain is strictly broader and stronger than the v001 evidence chain along every dimension v002 measured (90 days vs. 1 day; 155,153,449 events vs. 1,681,098 events; 19 / 19 boundary confirmations vs. 15 / 15; multi-day raw integrity established by Phase 4bl-D-R; raw multi-day successor-state recorded by Phase 4bl-E); and records that the cross-symbol evidence gap is unchanged from v001 (BTCUSDT only). The raw family `microstructure_raw_aggtrades_v001` remains permanently `research_eligible = false` across both v001 and v002 versions (Phase 4bb-E + Phase 4bl-E preserved). The actual v002 derived multi-day index manifest, the v002 raw manifest, the v001 derived manifest, and the v001 raw manifest all remain unchanged on disk (verified pre- and post-Phase-4bm-E). Phase 4bm-E is now project-complete on `main`. **Phase 4bm-E does not authorize Phase 4bm-F, any multi-day v002 feature-boundary design memo, any multi-day v002 feature implementation phase, any other successor, MCP, Graphify, agents-by-default, copying Prometheus agent packs or agent memory into the lightweight workspace, or any change to any on-disk manifest.**

## §7 Local Gitignored Outputs

**None.** Phase 4bm-E is docs-only and produced no local gitignored artefacts. No file under `data/microstructure/`, `data/research/`, or any other local gitignored namespace was created, modified, or deleted by the source branch, by the merge commit, or by this merge-closeout commit. The two pre-existing untracked entries in the working tree (`.claude/scheduled_tasks.lock`, `data/research/`) are operator-side state, not produced by Phase 4bm-E, and remain uncommitted per the authorization prompt.

The local Phase 4bm-D authoritative gate report at `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` (SHA256 `3b45e70b…`; paired sidecar SHA256 `8e74261c…`) is the evidence base Phase 4bm-E interprets; it is **not** modified by this phase. Both files remain gitignored under `.gitignore:85: data/microstructure/` and are not committed.

## §8 Validation Results

### Pre-merge (on Phase 4bm-E branch tip `1715a8a`)

- `git status --short`: only the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).
- `git branch --show-current`: `phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo`.
- `git rev-parse main`: `8234375f927f029211747eeae4ef493c612b2df3`.
- `git rev-parse origin/main`: `8234375f927f029211747eeae4ef493c612b2df3` (`main == origin/main` in sync).
- `git rev-parse phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo`: `1715a8adaa6eeeb478c7af363ed39af311783773`.
- `git rev-parse origin/phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo`: `1715a8adaa6eeeb478c7af363ed39af311783773` (in sync).
- `git diff main..phase-4bm-e/...` `--name-status`: 3 files (1 M `current-project-state.md` + 2 A new memos under `docs/00-meta/implementation-reports/`) matching §4.
- `git diff main..phase-4bm-e/...` `--stat`: 3 files / +1,241 insertions / 0 deletions (matches expected).
- `git diff --check main..phase-4bm-e/...`: clean (no whitespace errors).

### Pre-merge on-disk manifest / artefact re-verification

Re-verified on disk pre-merge (these SHAs must match the values recorded in §10 of this closeout):

- v002 derived multi-day index manifest: `research_eligible=False`; `eligibility_gate_status="pending"`; SHA256 `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (matches Phase 4bm-D merge-closeout §9 value).
- v002 raw manifest: `research_eligible=False`; `eligibility_gate_status="pending"`; SHA256 `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` (matches Phase 4bm-D merge-closeout §9 value).
- v001 derived manifest: `research_eligible=False`; `eligibility_gate_status="pending"`; SHA256 `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` (matches Phase 4bm-D merge-closeout §9 / Phase 4bg-A / Phase 4bg-B / Phase 4bh-A / Phase 4bh-B values).
- Phase 4bm-D authoritative gate report: SHA256 `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` (matches Phase 4bm-D merge-closeout §7 value).
- Phase 4bm-D authoritative sidecar: SHA256 `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` (matches Phase 4bm-D merge-closeout §7 value).

### Checkout main + pull

- `git checkout main`: `Switched to branch 'main'.`
- `git pull --ff-only`: `Already up to date.`
- `git status --short` on main pre-merge: only the two pre-existing untracked entries.

### Merge command output

- `git merge --no-ff phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo -m "docs(phase-4bm-e): merge multi-day derived-family research eligibility decision memo"`: `Merge made by the 'ort' strategy.`
- Files: 3 files changed, 1,241 insertions(+), 0 deletions(-).
- Conflicts: none.
- Merge commit SHA: `fcc1bd044d274c99520b4ab15282046e1428b3d0`.

### Post-merge (on `main` after the merge commit)

- `git diff --check` (post-merge): clean — exit code 0 (no whitespace errors, no unresolved markers).
- `git status --short` (post-merge, pre-closeout-commit): only the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).
- `git log --oneline -8 --decorate` (post-merge, pre-closeout-commit):
  ```text
  fcc1bd0 (HEAD -> main) docs(phase-4bm-e): merge multi-day derived-family research eligibility decision memo
  1715a8a (origin/phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo, phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo) docs(phase-4bm-e): add multi-day derived family research eligibility decision memo
  8234375 (origin/main, origin/HEAD) docs(phase-4bm-d-p1): add merge closeout
  3ddad02 docs(phase-4bm-d-p1): merge lightweight claude workspace standard
  055a670 (phase-4bm-d-p1/lightweight-claude-workspace-standard) docs(phase-4bm-d-p1): add lightweight claude workspace standard
  59e3e6c docs(phase-4bm-d): add merge closeout
  a80b8a0 docs(phase-4bm-d): merge multi-day derived family eligibility gate
  71ec483 (origin/phase-4bm-d/multi-day-derived-family-eligibility-gate, phase-4bm-d/multi-day-derived-family-eligibility-gate) docs(phase-4bm-d): add gate report and closeout
  ```
- `git push origin main`: `8234375..fcc1bd0  main -> main` (fast-forward push of the merge commit; no force, no skip-hooks, no skip-signing).
- `git rev-parse main` (post-push): `fcc1bd044d274c99520b4ab15282046e1428b3d0`.
- `git rev-parse origin/main` (post-push): `fcc1bd044d274c99520b4ab15282046e1428b3d0` (in sync).

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by this merge phase, and were **not** invoked by the Phase 4bm-E branch itself.

**Justification.** Phase 4bm-E is a Tier 1 docs-only research-eligibility decision memo per `docs/00-meta/process/phase-risk-tiering-standard.md`. The Phase 4bm-E branch and this merge commit introduce zero source / test / script / configuration changes — only three tracked documentation files are touched (1 modified + 2 added) plus this single additional merge-closeout file. Per the established Tier 1 docs-only governance-memo precedent — Phase 4bg-A (the direct v001 research-eligibility decision precedent that this phase mirrors), Phase 4bh-A, Phase 4bh-B, Phase 4bi-A, Phase 4bi-C, Phase 4bj-A, Phase 4bj-B, Phase 4bj-D, Phase 4bj-F, Phase 4bj-H, Phase 4bj-I, Phase 4bj-K, Phase 4bk-A, Phase 4bl-A, Phase 4bl-B, Phase 4bl-D-S1, Phase 4bl-F, Phase 4bm-A, Phase 4bm-A-P1, Phase 4bm-C, and Phase 4bm-D-P1 each explicitly skipped `ruff` / `mypy` / `pytest` for the same reason, the code / type / test gate subset is deliberately not invoked for this merge. No new regression is possible by construction because no source / test / script / configuration file is modified. The most recent authoritative whole-repo `pytest` baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; two pre-existing `KeyError: 'trade_count'` simulation failures on `tests/simulation/test_backtest_real_2026_03.py` in `src/prometheus/research/data/storage.py:232` are unrelated to Phase 4bm-E and are preserved as the baseline). Phase 4bm-E introduces zero new regressions vs that baseline.

### Gitignore policy verification

- `git check-ignore -v data/microstructure/`: `.gitignore:85: data/microstructure/` (pre-existing rule, unchanged).
- `git check-ignore -v data/microstructure/gate-reports/`: `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/manifests/`: `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/`: `.gitignore:85: data/microstructure/`.
- No new gitignored paths were introduced by Phase 4bm-E.

## §9 Upstream Immutability Evidence

Phase 4bm-E is a docs-only research-eligibility decision phase. It does not read, hash, write, or otherwise touch any file under `data/microstructure/`. Every prior local artefact under `data/microstructure/` is byte-identical pre- and post-Phase-4bm-E by construction: no file under `data/microstructure/` is read, hashed, written, deleted, or otherwise modified by the source branch, the merge commit, or this merge-closeout commit.

Specific governance and evidence witnesses re-confirmed at the start of Phase 4bm-E (matching the SHAs recorded in the Phase 4bm-D merge-closeout §9):

| Artefact | SHA256 (pre and post Phase 4bm-E) |
| -------- | ---------------------------------- |
| v002 derived multi-day index manifest (`microstructure_normalized_aggtrades_v001__v002.json`) | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |
| v002 raw manifest (`microstructure_raw_aggtrades_v001__v002.json`) | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bl-D-R raw multi-day `RAW_MULTIDAY_GATE_PASS` report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| Phase 4bm-D authoritative gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| v001 derived manifest (`microstructure_normalized_aggtrades_v001__v001.json`) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| v001 normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| v001 raw manifest (`microstructure_raw_aggtrades_v001__v001.json`) | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| v001 raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Phase 4bb-D v001 raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf v001 derived gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B v001 successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

The 90 v002 per-day Parquets, 90 v002 sidecars, 90 v002 raw zips, and 90 v002 raw zip sidecars are unchanged byte-for-byte by Phase 4bm-E by construction (Phase 4bm-E reads no Parquet, runs no kernel, and writes nothing under `data/microstructure/`). Every other prior `data/microstructure/` artefact (Phase 4bh v001 feature parquet and manifest, Phase 4bj-C v001 label parquet and manifest, Phase 4bj-G v001 label successor-state JSON, Phase 4bi-D v001 feature successor-state JSON, Phase 4bj-J no-split successor-state JSON, the Phase 4bm-D preliminary pre-commit sanity gate report and its sidecar, and any other artefact present locally) is preserved bit-for-bit.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

## §10 Manifest State Preservation

- **v002 derived multi-day index manifest** (`microstructure_normalized_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bm-B output. Not modified by Phase 4bm-D, Phase 4bm-D-P1, Phase 4bm-E, or this merge. SHA256 `01c5fa53…` byte-identical.
- **v002 raw manifest** (`microstructure_raw_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bl-C. Not modified. SHA256 `01696786…` byte-identical.
- **v001 derived manifest** (`microstructure_normalized_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bd. Not modified. SHA256 `f6f0d947…` byte-identical.
- **v001 raw manifest** (`microstructure_raw_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4az. Not modified. SHA256 `a371edd4…` byte-identical.
- **Every other manifest** under `data/microstructure/manifests/` and `data/manifests/`: unchanged.

No `research_eligible` flip occurred. No `eligibility_gate_status` transition occurred on any actual on-disk manifest. No `chronological_split_policy` change occurred on any actual on-disk manifest. No path exists in this phase or this merge to mutate any manifest: Phase 4bm-E is docs-only and writes no code that touches manifests; this merge introduces only documentation.

The Phase 4bm-D gate report's `eligibility_gate_status_after = "pass"` field is a **report-level recommendation only** and is **not written back to any manifest**. The Phase 4bm-E memo explicitly preserves this distinction: per Phase 4bb-E / Phase 4bf precedent (and per the Phase 4bg-A v001 precedent that Phase 4bm-E mirrors), the report-level PASS is governance evidence and does not by itself flip any manifest field. The actual on-disk v002 derived multi-day index manifest's `eligibility_gate_status` remains `"pending"`.

Any machine-readable Stage-3 marker for the v002 derived family would require a separately authorized successor-state recording phase (the multi-day analogue of Phase 4bg-B; if ever authorized, that phase would be **Phase 4bm-F**). Phase 4bm-F is **not** authorized by this merge.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## §11 Boundary Confirmations

The Phase 4bm-E merge honours every relevant boundary. Citing the canonical reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 by name, plus phase-specific additions:

- **N-ACQUISITION** applies — no acquisition; no download; no extension of any existing dataset; no creation or modification of raw data files.
- **N-ENDPOINT** applies — no Binance / public / authenticated / private endpoint called; no `data.binance.vision` contact; no WebSocket opened.
- **N-CREDENTIALS** applies — no credential used, read, created, or referenced; `.env` not read or created; `.mcp.json` not read or created; MCP / Graphify not enabled; no order placed; no exchange-write surface contacted.
- **N-MANIFEST** applies — no actual manifest file modified; no `research_eligible` flip; no `eligibility_gate_status` transition; no `chronological_split_policy` change; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- **N-GATE-RERUN** applies — no raw / derived / feature / label / metrics gate rerun; no new gate report generated; the Phase 4bm-D authoritative gate report is only interpreted (read-only), not regenerated.
- **N-SUCCESSOR-STATE** applies — no successor-state artefact created or modified; no v002 successor-state JSON exists or is created by this phase; the Phase 4bl-E raw multi-day successor-state JSON (`a0576ca6…`) is unchanged; the Phase 4bg-B v001 derived successor-state JSON (`8bcc7d01…`) is unchanged.
- **N-DERIVATION** applies — no normalization, derivation, feature, or label computation; no kernel run; no derived / feature / label parquet produced; no v002 feature or label artefact exists or is created.
- **N-DIAGNOSTICS-ML-STRATEGY** applies — no diagnostics, ML, strategy, signal construction, or backtest; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit output.
- **N-PHASE-5** applies — no Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.
- **N-VERDICT-LOCK** applies — no retained verdict revised (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure all preserved verbatim); no project lock changed (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt Claude Code context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace execution standard — all preserved verbatim).

Additional merge-level confirmations:

- no `data/microstructure/` file committed by either the source-branch commit, the merge commit, or this merge-closeout commit
- no `data/research/` file committed
- no `.claude/` file in `C:\Prometheus` modified or committed (local operator-side hook tooling under `C:\ClaudeRuns\prometheus-light\.claude\...` is not part of `C:\Prometheus`)
- no prior source / test / script modified by any commit in this merge
- no `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file modified
- no `.mcp.json` created
- no prior governance memo modified beyond the narrow `current-project-state.md` paragraph + new "Current phase:" block addition
- no prior phase implementation report, closeout, or merge-closeout modified
- no prior process standard modified
- no gate rerun (no gate kernel invoked); the Phase 4bm-D authoritative gate report is only interpreted, not regenerated
- no acquisition; no endpoint contacted; no WebSocket opened; no credential used; no `.env` / `.mcp.json` read or created; MCP / Graphify not enabled
- no features / labels / signals / proxies / ML / strategy / backtest output computed
- no successor-state JSON created (Phase 4bm-F would require a separately authorized phase)
- agents and project memory remain default-off for heavy light-workspace execution sessions (per the Phase 4bm-D-P1 standard)
- no agent pack or agent memory copied from `C:\Prometheus` into `C:\ClaudeRuns\prometheus-light`
- no retained verdict revised; no project lock loosened; no M0 amendment; no Phase 4al rule amended; no Phase 4aw invariant amended; no Phase 4bb-F canonical path policy amended; no Phase 4bl-F rule amended; no Phase 4bm-A-P1 standard amended; no Phase 4bm-D-P1 standard amended
- no successor authorized (Phase 4bm-F / Phase 4bm-G / Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical all remain unauthorized)
- merge command was a clean `git merge --no-ff` with `ort` strategy, no conflicts, no `--no-verify`, no `--no-gpg-sign`, no force-push

## §12 Retained Verdict Ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim by Phase 4bm-E and by this merge.

## §13 Preserved Project Locks

All preserved verbatim:

- §11.6 = 8 bps per side
- Round-trip = 16 bps
- §1.7.3 = 0.25% risk / 2× leverage / one-position / mark-price stops
- Phase 3p §4.7 (strict integrity gate)
- Phase 3r §8 (mark-price gap governance)
- Phase 3v §8 (stop-trigger-domain governance)
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance)
- Phase 4j §11 (metrics OI-subset partial-eligibility rule)
- Phase 4k (V2 backtest-plan methodology)
- Phase 4p (G1 strategy spec)
- Phase 4q (G1 backtest-plan methodology)
- Phase 4v (C1 strategy spec)
- Phase 4w (C1 backtest-plan methodology)
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; never invoked)
- Phase 4bb-F canonical path policy
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked — Phase 4bm-E introduces no new sidecars)
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard (cited)
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard (cited; honoured by this phase — Claude Code launched from the lightweight workspace `C:\ClaudeRuns\prometheus-light` with all shell commands using `cd C:\Prometheus && <command>` per the standard)
- Phase 4am .. Phase 4bm-D-P1 results — all preserved verbatim

## §14 No-Rescue Constraints

The Phase 4bm-E merge records a docs-only Tier 1 research-eligibility decision memo (Option B / Decision form 2). The decision is policy-level only. It does NOT, and CANNOT, be construed as authorising:

- ML model training, model selection, strategy hypothesis generation, signal construction, or any conversion of policy-level Stage-3 admissibility evidence into trading signals
- strategy logic, position state, entry / exit rules, or backtest design
- paper / shadow / live-readiness / deployment / exchange-write work
- Phase 4 canonical or Phase 5 authorisation
- transitioning any manifest's `research_eligible` flag from `false` to `true` from this evidence alone (Phase 4bm-F, separately authorized, would be required for any machine-readable v002 successor-state marker — and even then, the actual on-disk v002 derived multi-day index manifest would remain byte-identical with `research_eligible = false`, per the Phase 4bg-B v001 pattern)
- transitioning any manifest's `eligibility_gate_status` from `"pending"` to anything else on disk
- transitioning any manifest's `chronological_split_policy`
- creating any successor-state JSON (Phase 4bm-F, multi-day analogue of Phase 4bg-B, would require a separately authorized phase; not authorized)
- features, labels, diagnostics, ML, strategy, or backtests on v002 (or on v001)
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- cross-symbol acquisition (the v002 cross-symbol evidence gap is unchanged from v001; closing it would require a separately authorized acquisition phase)
- old-strategy alt-symbol rerun or cooled-down-family reopening (cooled-down families — price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane — all remain cooled down)
- 5m research-thread reopening (Phase 3t closure preserved)
- revising or weakening any retained verdict (R2 / F1 / D1-A / V2 / G1 / C1 first-specs remain terminally rejected as recorded; H0 framework anchor, R3 baseline-of-record, and R1a / R1b-narrow retained-non-leading status all preserved)
- cross-strategy hybrids (V1-D1, F1-D1, V2-G1, G1-C1, or any other combination)
- -prime, -narrow, -extension, or -hybrid variants of any historical candidate
- §11.6 cost-realism relaxation, §1.7.3 risk / leverage / one-position / mark-price stop amendment, or any other lock loosening
- M0 amendment, post-null cooldown weakening, cooled-down families list shortening, or memo template alteration
- use of Phase 4l V2 forensic numbers, Phase 4r G1 forensic numbers, or Phase 4x C1 forensic numbers as parameter-selection inputs
- use of 5m Q1–Q7 diagnostic outputs as rule-input candidates
- MCP / Graphify / `.mcp.json` / credential enablement
- copying Prometheus agent packs or agent memory into the lightweight workspace at `C:\ClaudeRuns\prometheus-light`
- enabling agents-by-default for heavy execution sessions
- committing local hook files from the lightweight workspace into `C:\Prometheus` without a separately authorized process phase
- amending the Phase 4bm-A-P1 thin-prompt Claude Code context-management standard (Phase 4bm-E cites it; does not amend it)
- amending the Phase 4bm-D-P1 lightweight Claude Code workspace execution standard (Phase 4bm-E cites and honours it; does not amend it)
- public-endpoint code calls, user-stream implementation, live WebSocket implementation, or any authenticated-API / private-endpoint access
- any change to any on-disk v002 / v001 manifest

Policy-level Stage-3 admissibility for the multi-day v002 derived family is necessary but not sufficient evidence for any of the above; sufficient evidence requires separately authorized subsequent phases under the established phase ladder (Phase 4bm-F successor-state recording → later multi-day feature-boundary design memo → later multi-day feature implementation phase → later v002 research / feasibility / strategy / backtest phases under M0 admissibility and Phase 4al §14 hierarchy).

## §15 Successor Authorization

**None.**

This merge-closeout records that Phase 4bm-E is project-complete on `main`. It does **not** authorize:

- **Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording** (multi-day analogue of Phase 4bg-B; would write a single sibling successor-state JSON + paired Phase 4bb-F sidecar under `data/microstructure/successor-state/`, preserving the original v002 derived multi-day index manifest and the v002 raw manifest byte-identically; would not authorize feature / label / ML / strategy / backtest work)
- future docs-only **multi-day v002 feature-boundary design memo** (multi-day analogue of Phase 4bh-A / Phase 4bh-B; would extend the v001 feature-boundary design to v002 inputs; would not authorize feature computation)
- future code + docs **multi-day v002 feature schema / feature computation implementation** (multi-day analogue of Phase 4bh; only after Stage-4 authorization on v002)
- future multi-day v002 **feature-family structural QA / feature-family eligibility gate / feature-family research-use decision / feature-family successor-state recording** (multi-day analogues of Phase 4bi-A / Phase 4bi-B / Phase 4bi-C / Phase 4bi-D)
- future multi-day v002 **label-family** phases (multi-day analogues of Phase 4bj-A through Phase 4bj-K)
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any other Phase 4 successor
- Phase 5 / Phase 4 canonical
- paper / shadow / live-readiness / deployment / exchange-write
- production-key creation / authenticated APIs / private endpoints
- user-stream / live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credential work
- any additional aggTrades / 5m / 1m / tick / mark-price / order-book / cross-venue / cross-symbol data acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- ML implementation, model selection, feature ranking, meta-labeling
- strategy implementation, signal construction, backtest implementation
- diagnostics rerun (Phase 3s Q1–Q7 closure preserved)
- any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual on-disk manifest
- any successor-state JSON creation
- agents-by-default for heavy Claude Code execution sessions
- copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light`
- committing local hook files from the lightweight workspace into `C:\Prometheus`

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

## §16 Recommended State

**Remain paused.**

Phase 4bm-E is now project-complete on `main` (this merge-closeout records the lifecycle anchor). The v002 multi-day derived family has policy-level Stage-3 admissibility recorded (Option B / Decision form 2) on top of the Stage-0 (Phase 4bm-B), Stage-1 (Phase 4bm-C 56 / 56 PASS), and report-level Stage-2 (Phase 4bm-D 60 / 60 PASS; `DERIVED_GATE_PASS`) evidence. The actual v002 derived multi-day index manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` byte-for-byte; no machine-readable Stage-3 marker exists for the v002 derived family. The operator's broader pause decision continues to apply.

**Conditional next, NOT authorized:**

Future operator-authorized **Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording** would be the natural next step in the v002 lifecycle ladder by precedent of Phase 4bg-B (research-eligibility successor-state recording for the Phase 4bd v001 derived family). Phase 4bm-F would write a single sibling successor-state JSON + paired Phase 4bb-F sidecar under `data/microstructure/successor-state/` (gitignored; not committed) recording Stage-3 at the successor-state level for the v002 derived family, while preserving the original v002 derived multi-day index manifest, the v002 raw manifest, and every other prior `data/microstructure/` artefact byte-identically (preserving the Phase 4aw `flip_research_eligible(...)` always-raises invariant; never invoking it). Phase 4bm-F is **not** authorised by this merge-closeout.

After any Phase 4bm-F merge, the recommended state would remain **remain paused** pending operator decision on a further conditional **multi-day v002 feature-boundary design memo** (multi-day analogue of Phase 4bh-A / Phase 4bh-B). That memo would extend the v001 feature-boundary design to v002 inputs and would not authorize feature computation. It is **not** authorised by this merge-closeout.

After any such multi-day v002 feature-boundary design merge, the recommended state would still remain **remain paused** pending operator decision on a further conditional **multi-day v002 feature implementation phase** (multi-day analogue of Phase 4bh). That phase, if ever authorized, would compute features locally under `data/microstructure/features/` (gitignored; not committed) and would still not authorize ML, strategy, or backtest work. It is **not** authorised by this merge-closeout.

— end of Phase 4bm-E merge-closeout —
