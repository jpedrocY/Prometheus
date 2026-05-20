# Phase 4bm-G Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-G — Multi-Day V002 Feature-Boundary Design Memo
- **Tier**: Tier 1 (docs-only Full Phase; governance / boundary-design memo; multi-day v002 analogue of Phase 4bh-A and the Phase 4bh-B v001 schema-finalization layer it eventually fed)
- **Type**: docs-only feature-boundary design memo — adds two new tracked docs files under `docs/00-meta/implementation-reports/` and narrowly updates `docs/00-meta/current-project-state.md`; no source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified; no feature artefact is created
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-G as project-complete on `main` after a clean docs-only branch that defines the feature boundary for any future multi-day v002 feature work on the Stage-3 successor-state-marked normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events). Phase 4bm-G reaches **v002 Feature Stage-0** only.
- **Branch merged**: `phase-4bm-g/multi-day-v002-feature-boundary-design-memo`
- **Target branch**: `main`
- **Base**: `main` at `bc7fa817ec712d296f9cd88dec89136b818edcbd` (Phase 4bm-F merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording; project-complete on `main`)
- **Direct v001 precedent**: Phase 4bh-A (v001 feature-boundary design memo) + Phase 4bh-B (v001 feature schema finalization memo)

**Feature-boundary design is not feature computation.** **Stage-4 is not authorized by Phase 4bm-G.** **Phase 4bm-H is not authorized by Phase 4bm-G.** **No v002 feature artefact exists after Phase 4bm-G.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-G is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `bc7fa817ec712d296f9cd88dec89136b818edcbd`
- **Pre-merge `origin/main` SHA**: `bc7fa817ec712d296f9cd88dec89136b818edcbd` (in sync; `git pull --ff-only` reported `Already up to date.`)
- **Phase 4bm-G branch docs commit SHA**: `6a7a814e94723c143f1c20dfb1951dbf4790b30b` (`docs(phase-4bm-g): add multi-day v002 feature-boundary design memo`; 3 files / +1,491 / -0; single tracked commit on branch)
- **Phase 4bm-G branch tip SHA pre-merge**: `6a7a814e94723c143f1c20dfb1951dbf4790b30b`
- **Merge commit SHA**: `06c1f8318db9a34d0b6738d995449dfb0cfee144`
- **Merge commit message**: `docs(phase-4bm-g): merge multi-day v002 feature-boundary design memo`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `06c1f8318db9a34d0b6738d995449dfb0cfee144`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `06c1f8318db9a34d0b6738d995449dfb0cfee144` (in sync; pushed cleanly via `bc7fa81..06c1f83 main -> main`)
- **Merge-closeout commit SHA**: `685031339df97f6935f480533323063d59554118` (`docs(phase-4bm-g): add merge closeout`; 1 file / +386 / -0; this file's commit on `main`)
- **Post-merge-closeout-commit `main` SHA**: `685031339df97f6935f480533323063d59554118`
- **Post-merge-closeout-commit `origin/main` SHA**: `685031339df97f6935f480533323063d59554118` (pushed cleanly via `06c1f83..6850313  main -> main`; no force, no skip-hooks, no skip-signing)
- **Final `main == origin/main` after closeout push**: true (both at `685031339df97f6935f480533323063d59554118` immediately after the merge-closeout commit + push; the subsequent SHA-finalization commit then advances `main` and `origin/main` together by one additional commit, recorded in the final operator report)

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-g/multi-day-v002-feature-boundary-design-memo -m "docs(phase-4bm-g): merge multi-day v002 feature-boundary design memo"`
- **Strategy**: `ort` (git default; reported by git as `Merge made by the 'ort' strategy.`)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     bc7fa81..06c1f83  main -> main
  ```
  Second push (this merge-closeout commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     06c1f83..6850313  main -> main
  ```

## §4 Files Brought Forward by the Merge

Three tracked files brought forward from the Phase 4bm-G branch into `main`, all from the single source-branch commit (`6a7a814`).

**Tracked files added (2):**

1. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-g_multi-day-v002-feature-boundary-design-memo.md` (NEW, +627; the 24-section main feature-boundary design memo)
2. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-g_closeout.md` (NEW, +210; Phase 4bm-G closeout)

**Tracked files modified narrowly (1):**

3. `docs/00-meta/current-project-state.md` (MODIFIED, +654 / -0; Phase 4bm-G narrative paragraph + new "Current phase:" block; prior Phase 4bm-F "Current phase:" block preserved verbatim as labelled historical context — pure addition, no deletions, consistent with the Phase 4bm-E / Phase 4bm-F precedent pattern)

**This merge-closeout commit — 1 additional tracked file (allowed by the operator authorization for the merge phase):**

4. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-g_merge-closeout.md` (NEW; this file)

**Explicit non-changes:** No `data/microstructure/` file was modified, added, or deleted by the merge commit or by this merge-closeout commit. The Phase 4bm-G branch produced **zero** new local gitignored outputs (Phase 4bm-G is docs-only — no successor-state JSON, no feature artefact, no manifest, no sidecar, no gate report). No file under `src/prometheus/`, `tests/`, `scripts/`, or any other source / test / script surface was modified. No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP file (`.mcp.json` absent before and after), or `.claude/settings.json` / `.claude/settings.local.json` / `.claude/hooks/` / `.claude/agents/` file in `C:\Prometheus` was modified or created. No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph + new "Current phase:" block addition. No prior implementation report, closeout, or merge-closeout was modified. No prior process standard was modified. No manifest, sidecar, gate report, normalized parquet, derived parquet, raw zip, acquisition log, prior successor-state JSON, feature parquet, or label parquet was modified.

**Pre-existing v001 feature artefact note:** the `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/` directory exists locally from prior Phase 4bh v001 single-day feature implementation work and contains exactly one v001 per-day feature parquet (`BTCUSDT-features-aggtrades-2025-01-15.parquet`; SHA256 `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`) and its paired Phase 4bb-F sidecar (`<file>.sha256`; SHA256 `cc880c0820f96ad6f45d1fedeeaa3277941cd5c129c946d72639b921854e311c`). Both files are gitignored under `.gitignore:85: data/microstructure/` and are unchanged by Phase 4bm-G. Phase 4bm-G creates no v002 entry under that namespace and modifies no existing v001 entry. The §10 of the Phase 4bm-G main memo (paragraph stating "the `data/microstructure/features/` namespace does not exist as of Phase 4bm-G") is a narrow inaccuracy: the namespace does pre-exist from Phase 4bh v001 work, but the operative claim — that **no v002 subdirectory exists** and **Phase 4bm-G creates no v002 feature artefact** — remains true and is the materially correct outcome. This nuance does not affect the merge.

## §5 Diff Summary

```text
 docs/00-meta/current-project-state.md              | 654 +++++++++++++++++++++
 .../2026-05-18_phase-4bm-g_closeout.md             | 210 +++++++
 ..._multi-day-v002-feature-boundary-design-memo.md | 627 ++++++++++++++++++++
 3 files changed, 1491 insertions(+)
```

- 3 files changed
- 1,491 insertions
- 0 deletions
- The merge diff exactly matches the expected change set from the authorization prompt (2 added + 1 modified = 3 tracked files; no `data/microstructure/` files committed; no source / test / script / configuration files).
- `git diff --check` clean across the branch and post-merge (no whitespace errors; no unresolved merge markers).
- `git diff main..phase-4bm-g/... --name-only` confirms the changed file list is limited to exactly the three expected docs files.

## §6 Result / Verdict

**MEMO RECORDED — Phase 4bm-G v002 Feature Stage-0 boundary design recorded on `main`; Phase 4bm-G is project-complete on `main`.**

Phase 4bm-G is a docs-only Tier 1 feature-boundary design memo — the multi-day v002 analogue of Phase 4bh-A / Phase 4bh-B for the v002 derived family. It reaches **v002 Feature Stage-0** only (feature schema designed on paper; no code, no data, no artefact). The memo cites the Phase 4bm-F successor-state JSON SHA `72b6edd4…` as the **only** Stage-3 machine-readable marker for v002, records the upstream v002 lineage SHA table that any future v002 feature implementation must cite (v002 derived multi-day index manifest `01c5fa53…`, v002 derived sidecar `d96f31ae…`, v002 raw manifest `01696786…`, v002 acquisition log `52f6d7fb…`, Phase 4bl-D-R raw multi-day gate report `f9493fd1…`, Phase 4bl-E raw successor-state `a0576ca6…`, Phase 4bm-D authoritative gate report `3b45e70b…`, Phase 4bm-D sidecar `8e74261c…`, Phase 4bm-F successor-state `72b6edd4…`, Phase 4bm-F sidecar `1e9ffb23…`; with Phase 4bg-B v001 derived successor-state `8bcc7d01…` and v001 derived manifest `f6f0d947…` cross-referenced as historical precedent only), records the proposed future v002 feature family naming (`microstructure_features_aggtrades_v001` with `dataset_version = v002`; sibling derived family, not a mutation), the proposed future v002 feature manifest path and per-day v002 feature Parquet path conventions (NOT created), the future v002 feature schema design including lineage / timestamp / source-row-identity / non-feature-retained / computed-feature / forbidden columns, the allowed v002 feature categories A–H (event-count/intensity, buy/sell aggressor imbalance, volume/notional, price-movement causal descriptors, inter-arrival/activity-rate, rolling-window descriptive, time-of-day context, data-quality/coverage), the forbidden v002 feature categories with a binding 26-token forbidden-substring detector, the timestamp/leakage policy (UTC only; no future-looking windows; explicit `(T - window_ms, T]` left-open right-closed trailing-window convention; deterministic `(transact_time_ms ASC, row_index ASC)` sorting; same-timestamp tie-break by `row_index ASC`; per-day boundary honouring half-open UTC day convention; three admissible multi-day rolling-window boundary policies with the recommended default of causal cross-day lookback; no centered windows; all train/validation/OOS/evaluation splits as future work; label construction forbidden), the decimal/precision policy (raw price/quantity Decimal-as-string; never float; aggressive-flow ratios and log returns float64-nullable; explicit Decimal context declared in feature config and included in `feature_config_hash`), the multi-day partitioning policy (90 per-day v002 feature Parquets one-per-`(symbol, utc_date)` partition; warm-up handling for day 1; `invalid_windows = []` propagation; atomic write-then-rename; refuse-to-overwrite; determinism across reruns), the chronological-split / research-split readiness rules (no split assigned; future v002 split-policy memo required; strictly chronological; no random shuffle; no boundary leakage), 16 feature-boundary fail-closed rules, and 17 proposed future v002 feature-implementation acceptance criteria. The actual v002 derived multi-day index manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically (SHA `01c5fa53…` re-verified pre- and post-merge). The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked). Phase 4bm-G is now project-complete on `main`.

The v002 multi-day derived family now carries the complete Phase 4ba 5-stage ladder of evidence through Stage-3 (Phase 4bm-B → 4bm-C → 4bm-D → 4bm-E → 4bm-F) PLUS a complete v002 Feature Stage-0 boundary design (Phase 4bm-G this merge). **v002 Feature Stages 1 through 5 and Stage-4 (feature-cleared) remain unauthorized.** **Phase 4bm-G does not authorize Phase 4bm-H, any multi-day v002 feature schema finalization memo, any feature computation, any label / diagnostics / ML / strategy / backtest work, any acquisition, MCP, Graphify, agents-by-default, copying Prometheus agent packs or agent memory into the lightweight workspace, or any change to any on-disk manifest.**

## §7 Local Gitignored Outputs

**None produced by Phase 4bm-G.** Phase 4bm-G is docs-only and produced no local gitignored artefacts — no successor-state JSON, no feature parquet, no feature manifest, no gate report, no sidecar. No file under `data/microstructure/`, `data/research/`, or any other local gitignored namespace was created, modified, or deleted by the source branch, the merge commit, or this merge-closeout commit. The two pre-existing untracked entries in the working tree (`.claude/scheduled_tasks.lock`, `data/research/`) are operator-side state, not produced by Phase 4bm-G, and remain uncommitted per the authorization prompt.

The pre-existing Phase 4bh v001 single-day feature parquet at `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` (SHA256 `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`) and its paired Phase 4bb-F sidecar (SHA256 `cc880c0820f96ad6f45d1fedeeaa3277941cd5c129c946d72639b921854e311c`) — gitignored from Phase 4bh — are **unchanged** by Phase 4bm-G. The pre-existing Phase 4bm-F v002 derived successor-state JSON at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` (SHA `72b6edd4…`) and its paired sidecar (SHA `1e9ffb23…`) — gitignored from Phase 4bm-F — are unchanged. Every other prior local gitignored artefact under `data/microstructure/` (90 v002 per-day Parquets + 90 v002 sidecars + 90 v002 raw zips + 90 v002 raw zip sidecars + v002 derived multi-day index manifest + sidecar + v002 raw manifest + v002 acquisition log + Phase 4bl-D-R raw multi-day gate report + Phase 4bl-E raw successor-state JSON + Phase 4bm-D authoritative gate report + sidecar + Phase 4bm-D preliminary pre-commit sanity gate report + sidecar + Phase 4bg-B v001 derived successor-state JSON + Phase 4bb-G v001 raw successor-state JSON + Phase 4bi-D v001 feature successor-state JSON + Phase 4bj-G v001 label successor-state JSON + Phase 4bj-J v001 label split-policy successor-state JSON + Phase 4bd v001 normalized Parquet + Phase 4bd v001 derived manifest + Phase 4az v001 raw artefacts + Phase 4bb-D v001 raw gate report + Phase 4bf v001 derived gate report + Phase 4bj-C v001 label parquet and manifest if present) is preserved bit-for-bit.

## §8 Validation Results

### Pre-merge (on Phase 4bm-G branch tip `6a7a814`)

- `git status --short`: only the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).
- `git branch --show-current`: `phase-4bm-g/multi-day-v002-feature-boundary-design-memo`.
- `git rev-parse main`: `bc7fa817ec712d296f9cd88dec89136b818edcbd`.
- `git rev-parse origin/main`: `bc7fa817ec712d296f9cd88dec89136b818edcbd` (`main == origin/main` in sync).
- `git rev-parse phase-4bm-g/...`: `6a7a814e94723c143f1c20dfb1951dbf4790b30b`.
- `git rev-parse origin/phase-4bm-g/...`: `6a7a814e94723c143f1c20dfb1951dbf4790b30b` (in sync).
- `git diff main..phase-4bm-g/... --name-status`: 3 files (1 M `current-project-state.md` + 2 A new memos) matching §4.
- `git diff main..phase-4bm-g/... --stat`: 3 files / +1,491 insertions / 0 deletions (matches expected).
- `git diff main..phase-4bm-g/... --name-only`: confirms exactly the three expected docs files (no `data/microstructure/` files, no source / test / script / configuration files).
- `git diff --check main..phase-4bm-g/...`: clean (no whitespace errors).

### Pre-merge on-disk SHA re-verification

Re-verified on disk pre-merge — all 12 upstream evidence SHAs match the values recorded in §11 of this closeout:

- v002 derived multi-day index manifest: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` ✓
- v002 derived manifest sidecar: `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` ✓
- v002 raw manifest: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` ✓ (`research_eligible=false`, `eligibility_gate_status="pending"` confirmed)
- v002 acquisition log: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` ✓
- v001 derived manifest: `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` ✓ (`research_eligible=false`, `eligibility_gate_status="pending"`)
- Phase 4bm-D authoritative derived-family gate report: `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` ✓
- Phase 4bm-D authoritative sidecar: `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` ✓
- Phase 4bl-D-R raw multi-day PASS gate report: `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` ✓
- Phase 4bl-E raw multi-day successor-state JSON: `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` ✓
- Phase 4bg-B v001 derived successor-state JSON: `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` ✓
- Phase 4bm-F v002 derived successor-state JSON: `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` ✓
- Phase 4bm-F v002 derived sidecar: `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` ✓

v002 derived multi-day index manifest, v002 raw manifest, and v001 derived manifest re-read on disk all confirm `research_eligible=false` and `eligibility_gate_status="pending"`.

### Checkout main + pull

- `git checkout main`: `Switched to branch 'main'.`
- `git pull --ff-only`: `Already up to date.`
- `git status --short` on main pre-merge: only the two pre-existing untracked entries.

### Merge command output

- `git merge --no-ff phase-4bm-g/multi-day-v002-feature-boundary-design-memo -m "docs(phase-4bm-g): merge multi-day v002 feature-boundary design memo"`: `Merge made by the 'ort' strategy.`
- Files: 3 files changed, 1,491 insertions(+), 0 deletions(-).
- Conflicts: none.
- Merge commit SHA: `06c1f8318db9a34d0b6738d995449dfb0cfee144`.

### Post-merge (on `main` after the merge commit)

- `git diff --check` (post-merge): clean — exit code 0.
- `git status --short` (post-merge, pre-closeout-commit): only the two pre-existing untracked entries.
- `git log --oneline -5 --decorate` (post-merge, pre-closeout-commit):
  ```text
  06c1f83 (HEAD -> main) docs(phase-4bm-g): merge multi-day v002 feature-boundary design memo
  6a7a814 (origin/phase-4bm-g/multi-day-v002-feature-boundary-design-memo, phase-4bm-g/multi-day-v002-feature-boundary-design-memo) docs(phase-4bm-g): add multi-day v002 feature-boundary design memo
  bc7fa81 (origin/main, origin/HEAD) docs(phase-4bm-f): finalize merge closeout shas
  37adf9b docs(phase-4bm-f): add merge closeout
  35227cb docs(phase-4bm-f): merge multi-day derived-family successor-state recording
  ```
- `git push origin main`: `bc7fa81..06c1f83  main -> main` (fast-forward push of the merge commit; no force, no skip-hooks, no skip-signing).
- `git rev-parse main` (post-push): `06c1f8318db9a34d0b6738d995449dfb0cfee144`.
- `git rev-parse origin/main` (post-push): `06c1f8318db9a34d0b6738d995449dfb0cfee144` (in sync).

### Post-merge artefact re-verification

Re-computed on disk post-merge — every SHA byte-identical to pre-merge:

- v002 derived multi-day index manifest: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` ✓
- v002 derived manifest sidecar: `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` ✓
- v002 raw manifest: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` ✓
- v002 acquisition log: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` ✓
- v001 derived manifest: `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` ✓
- Phase 4bm-D authoritative gate report: `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` ✓
- Phase 4bm-D authoritative sidecar: `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` ✓
- Phase 4bl-D-R raw multi-day PASS gate report: `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` ✓
- Phase 4bl-E raw multi-day successor-state JSON: `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` ✓
- Phase 4bg-B v001 derived successor-state JSON: `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` ✓
- Phase 4bm-F v002 derived successor-state JSON: `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` ✓
- Phase 4bm-F v002 derived sidecar: `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` ✓
- Phase 4bh v001 single-day feature parquet (pre-existing): `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` ✓
- Phase 4bh v001 single-day feature sidecar (pre-existing): `cc880c0820f96ad6f45d1fedeeaa3277941cd5c129c946d72639b921854e311c` ✓

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by this merge phase, and were **not** invoked by the Phase 4bm-G branch itself.

**Justification.** Phase 4bm-G is a Tier 1 docs-only governance / boundary-design memo per `docs/00-meta/process/phase-risk-tiering-standard.md`. The Phase 4bm-G branch and this merge commit introduce zero source / test / script / configuration changes — only three tracked documentation files are touched (1 modified + 2 added) plus this single additional merge-closeout file. Per the established Tier 1 docs-only governance / boundary-design memo precedent — **Phase 4bh-A (the direct v001 feature-boundary design precedent that this phase mirrors)**, Phase 4bh-B (v001 feature schema finalization), Phase 4bg-A, Phase 4bi-A, Phase 4bi-C, Phase 4bj-A, Phase 4bj-B, Phase 4bj-D, Phase 4bj-F, Phase 4bj-H, Phase 4bj-I, Phase 4bj-K, Phase 4bk-A, Phase 4bl-A, Phase 4bl-B, Phase 4bl-D-S1, Phase 4bl-F, Phase 4bm-A, Phase 4bm-A-P1, Phase 4bm-C, Phase 4bm-D-P1, and Phase 4bm-E each explicitly skipped `ruff` / `mypy` / `pytest` for the same reason, the code / type / test gate subset is deliberately not invoked for this merge. No new regression is possible by construction because no source / test / script / configuration file is modified. The most recent authoritative whole-repo `pytest` baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; two pre-existing `KeyError: 'trade_count'` simulation failures on `tests/simulation/test_backtest_real_2026_03.py` in `src/prometheus/research/data/storage.py:232` are unrelated to Phase 4bm-G and are preserved as the baseline). Phase 4bm-G introduces zero new regressions vs that baseline.

### Gitignore policy verification

- `git check-ignore -v data/microstructure/`: `.gitignore:85: data/microstructure/` (pre-existing rule, unchanged).
- No new gitignored paths were introduced by Phase 4bm-G.
- The pre-existing `data/microstructure/features/microstructure_features_aggtrades_v001/...` namespace (created by Phase 4bh v001) remains gitignored under the same `.gitignore:85` rule; no new entry was created by Phase 4bm-G.

## §9 Upstream Immutability Evidence

Phase 4bm-G is a docs-only governance / boundary-design phase. It does not read, hash, write, or otherwise touch any file under `data/microstructure/`. Every prior local artefact under `data/microstructure/` is byte-identical pre- and post-Phase-4bm-G by construction: no file under `data/microstructure/` is read in a mutating way, hashed in a mutating way, written, deleted, or otherwise modified by the source branch, the merge commit, or this merge-closeout commit.

Specific governance and evidence witnesses re-confirmed at the start of Phase 4bm-G and re-confirmed post-merge (table mirrored in §11 below for ease of reference):

| Artefact | SHA256 (pre and post Phase 4bm-G) |
| -------- | ---------------------------------- |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| v001 derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Phase 4bm-D authoritative derived gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| Phase 4bg-B v001 derived successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| **Phase 4bm-F v002 derived successor-state JSON** | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` |
| **Phase 4bm-F v002 derived sidecar** | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` |
| Phase 4bh v001 single-day feature parquet (pre-existing) | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Phase 4bh v001 single-day feature sidecar (pre-existing) | `cc880c0820f96ad6f45d1fedeeaa3277941cd5c129c946d72639b921854e311c` |

The 90 v002 per-day Parquets, 90 v002 sidecars, 90 v002 raw zips, and 90 v002 raw zip sidecars are unchanged byte-for-byte by Phase 4bm-G by construction. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

## §10 Manifest State Preservation

- **v002 derived multi-day index manifest** (`microstructure_normalized_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bm-B output. Not modified by Phase 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G. SHA256 `01c5fa53…` byte-identical (re-verified on disk pre- and post-merge).
- **v002 raw manifest** (`microstructure_raw_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bl-C. Not modified. SHA256 `01696786…` byte-identical.
- **v001 derived manifest** (`microstructure_normalized_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bd. Not modified. SHA256 `f6f0d947…` byte-identical.
- **v001 raw manifest** (`microstructure_raw_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4az. Not modified.
- **Every other manifest** under `data/microstructure/manifests/` and `data/manifests/`: unchanged.

No `research_eligible` flip occurred on any actual on-disk manifest. No `eligibility_gate_status` transition occurred on any actual on-disk manifest. No `chronological_split_policy` change occurred on any actual on-disk manifest. Phase 4bm-G is docs-only and writes no code that touches manifests; this merge introduces only documentation.

The Phase 4bm-F successor-state JSON's `successor_research_eligible: true` is a sibling-artefact assertion only and does not flip the actual on-disk v002 derived multi-day index manifest. Phase 4bm-G cites this Phase 4bm-F SHA `72b6edd4…` as the only Stage-3 marker but does not create any new successor-state artefact. Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

The v002 multi-day derived family now carries: Stage-0 (Phase 4bm-B), Stage-1 (Phase 4bm-C 56/56 PASS), Stage-2 (Phase 4bm-D 60/60 `DERIVED_GATE_PASS`), Stage-2-decision (Phase 4bm-E Option B / Decision form 2), Stage-3 (Phase 4bm-F successor-state JSON `72b6edd4…`), and v002 Feature Stage-0 (Phase 4bm-G boundary design on paper). **Stage-4 (feature-cleared) and v002 Feature Stages 1 through 5 remain unauthorized.**

## §11 Upstream Lineage SHA Table

The full v002 upstream lineage that any future v002 feature implementation must cite by SHA256 — recorded here as the authoritative reference for Phase 4bm-G:

| Artefact | Path | SHA256 |
| -------- | ---- | ------ |
| v002 derived multi-day index manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived manifest sidecar | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256` | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |
| v002 raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bl-D-R raw multi-day PASS gate report | `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E raw multi-day successor-state JSON | `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json` | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| Phase 4bm-D authoritative derived-family gate report | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Phase 4bm-D authoritative sidecar | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json.sha256` | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| **Phase 4bm-F v002 derived successor-state JSON (Stage-3 marker)** | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` |
| Phase 4bm-F v002 derived sidecar | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json.sha256` | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` |
| Phase 4bg-B v001 derived successor-state JSON (precedent cross-reference only; not transitive) | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json` | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| v001 derived manifest (cross-reference only; not transitive) | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |

## §12 Boundary Confirmations

The Phase 4bm-G merge honours every relevant boundary. Citing the canonical reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 by name:

- **N-ACQUISITION** applies — no acquisition; no download; no extension of any existing dataset; no creation or modification of raw data files.
- **N-ENDPOINT** applies — no Binance / public / authenticated / private endpoint called; no `data.binance.vision` contact; no WebSocket opened.
- **N-CREDENTIALS** applies — no credential used, read, created, or referenced; `.env` not read or created; `.mcp.json` not read or created; MCP / Graphify not enabled; no order placed; no exchange-write surface contacted.
- **N-MANIFEST** applies — no actual manifest file modified; no `research_eligible` flip on any actual on-disk manifest; no `eligibility_gate_status` transition on any actual on-disk manifest; no `chronological_split_policy` change; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- **N-GATE-RERUN** applies — no raw / derived / feature / label / metrics gate rerun; no new gate report generated; the Phase 4bm-D authoritative gate report is read-only referenced, not regenerated.
- **N-SUCCESSOR-STATE** applies — no successor-state artefact created or modified by Phase 4bm-G. The Phase 4bm-F v002 successor-state JSON (`72b6edd4…`), the Phase 4bg-B v001 successor-state JSON (`8bcc7d01…`), the Phase 4bl-E raw multi-day successor-state JSON (`a0576ca6…`), the Phase 4bb-G v001 raw successor-state JSON, the Phase 4bi-D v001 feature successor-state JSON, the Phase 4bj-G v001 label successor-state JSON, and the Phase 4bj-J v001 label split-policy successor-state JSON are all unchanged.
- **N-DERIVATION** applies — no normalization, derivation, feature, or label computation; no kernel run; no derived / feature / label parquet produced; no v002 feature artefact exists.
- **N-DIAGNOSTICS-ML-STRATEGY** applies — no diagnostics, ML, strategy, signal construction, or backtest; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit output.
- **N-PHASE-5** applies — no Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.
- **N-VERDICT-LOCK** applies — no retained verdict revised (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure all preserved verbatim); no project lock changed (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt Claude Code context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace execution standard — all preserved verbatim).

Additional merge-level confirmations:

- no tracked `data/microstructure/` file committed by either the source-branch commit, the merge commit, or this merge-closeout commit
- no `data/research/` file committed
- no `.claude/` file in `C:\Prometheus` modified or committed
- no prior source / test / script modified by any commit in this merge
- no `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file modified
- no `.mcp.json` created
- no prior governance memo modified beyond the narrow `current-project-state.md` paragraph + new "Current phase:" block addition
- no prior phase implementation report, closeout, or merge-closeout modified
- no prior process standard modified
- no gate rerun (no gate kernel invoked); the Phase 4bm-D authoritative gate report is only read-referenced, not regenerated
- no normalizer rerun; no structural QA rerun
- no acquisition; no endpoint contacted; no WebSocket opened; no credential used; no `.env` / `.mcp.json` read or created; MCP / Graphify not enabled
- no features / labels / signals / proxies / ML / strategy / backtest output computed
- agents and project memory remain default-off for heavy light-workspace execution sessions (per the Phase 4bm-D-P1 standard); Claude Code was launched from the lightweight workspace at `C:\ClaudeRuns\prometheus-light` with all shell commands using `cd C:\Prometheus && <command>` per the standard
- no agent pack or agent memory copied from `C:\Prometheus` into `C:\ClaudeRuns\prometheus-light`
- no retained verdict revised; no project lock loosened; no M0 amendment; no Phase 4al rule amended; no Phase 4aw invariant amended; no Phase 4bb-F policy amended; no Phase 4bl-F rule amended; no Phase 4bm-A-P1 standard amended; no Phase 4bm-D-P1 standard amended; no Phase 4bm-E decision changed; no Phase 4bm-F outcome changed
- no successor authorized (Phase 4bm-H / multi-day v002 feature schema finalization memo / multi-day v002 feature implementation / multi-day v002 feature-family phases / multi-day v002 label-family phases / Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical all remain unauthorized)
- merge command was a clean `git merge --no-ff` with `ort` strategy, no conflicts, no `--no-verify`, no `--no-gpg-sign`, no force-push

## §13 Retained Verdict Ledger

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

All preserved verbatim by Phase 4bm-G and by this merge.

## §14 Preserved Project Locks

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
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard (cited; honoured by this phase — Claude Code launched from the lightweight workspace `C:\ClaudeRuns\prometheus-light` with all shell commands using `cd C:\Prometheus && <command>` per the standard)
- Phase 4am .. Phase 4bm-F results — all preserved verbatim

## §15 Successor Authorization

**None.**

This merge-closeout records that Phase 4bm-G is project-complete on `main`. It does **not** authorize:

- **Phase 4bm-H — Multi-Day V002 Feature Schema / Feature Computation Implementation** (multi-day analogue of Phase 4bh; the canonical successor)
- future docs-only **multi-day v002 feature schema finalization memo** (multi-day analogue of Phase 4bh-B), if the operator chooses to separate design from finalization
- future multi-day v002 **feature artefact structural QA memo** (multi-day analogue of Phase 4bi-A)
- future multi-day v002 **feature-family eligibility-gate design + implementation + execution** (multi-day analogue of Phase 4bi-B)
- future multi-day v002 **feature-family research-use decision memo** (multi-day analogue of Phase 4bi-C)
- future multi-day v002 **feature-family successor-state recording** (multi-day analogue of Phase 4bi-D)
- future multi-day v002 **label-family** phases (multi-day analogues of Phase 4bj-A through Phase 4bj-K)
- future multi-day v002 **chronological-split-policy memo** (multi-day analogue of Phase 4bj-H / Phase 4bj-I / Phase 4bj-J)
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any other Phase 4 successor
- Phase 5 / Phase 4 canonical
- paper / shadow / live-readiness / deployment / exchange-write
- production-key creation / authenticated APIs / private endpoints
- user-stream / live WebSocket implementation / public-endpoint calls in code
- MCP / Graphify / `.mcp.json` / credential work
- any additional aggTrades / 5m / 1m / tick / mark-price / order-book / cross-venue / cross-symbol data acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- ML implementation, model selection, feature ranking, meta-labeling
- strategy implementation, signal construction, backtest implementation
- diagnostics rerun (Phase 3s Q1–Q7 closure preserved)
- any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual on-disk manifest
- any further successor-state JSON creation
- agents-by-default for heavy Claude Code execution sessions
- copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light`
- committing local hook files from the lightweight workspace into `C:\Prometheus`

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

## §16 Recommended State

**Remain paused.**

Phase 4bm-G is now project-complete on `main` (this merge-closeout records the lifecycle anchor). The v002 multi-day derived family carries the complete Phase 4ba 5-stage ladder of evidence through Stage-3 (Phase 4bm-B → 4bm-C → 4bm-D → 4bm-E → 4bm-F) PLUS a complete v002 Feature Stage-0 boundary design (Phase 4bm-G this merge). **Stage-4 (feature-cleared) and v002 Feature Stages 1 through 5 remain unauthorized.** The actual v002 derived multi-day index manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked). The operator's broader pause decision continues to apply.

**Required exact phrases (preserved verbatim):**

- **Feature-boundary design is not feature computation.**
- **Stage-4 is not authorized by Phase 4bm-G.**
- **Phase 4bm-H is not authorized by Phase 4bm-G.**
- **No v002 feature artefact exists after Phase 4bm-G.**

**Conditional next, NOT authorized:**

Future operator-authorized **Phase 4bm-H — Multi-Day V002 Feature Schema / Feature Computation Implementation** (multi-day analogue of Phase 4bh) would be the natural next step in the v002 lifecycle ladder. It would compute v002 features locally under `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`, produce gitignored per-day v002 feature Parquets + paired Phase 4bb-F sidecars + a future v002 feature manifest (gitignored under `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`), preserve the original v002 derived multi-day index manifest, the original v002 raw manifest, every other prior `data/microstructure/` artefact, the Phase 4bm-F v002 successor-state JSON, and the Phase 4aw always-raises invariant byte-identically (never invoking it), cite the Phase 4bm-F successor-state SHA `72b6edd4…` verbatim, and would not authorize ML, strategy, label, diagnostics, or backtest work. **Phase 4bm-H is not authorised by this merge-closeout.**

Alternatively, the operator may separately authorize a future docs-only **multi-day v002 feature schema finalization memo** (multi-day analogue of Phase 4bh-B) before Phase 4bm-H, if desired, to convert the Phase 4bm-G boundary design into an exact column list / windows / cadence with `feature_config_hash` fixed in writing. This memo is **not authorised by this merge-closeout**.

After any future v002 feature implementation merge, the recommended state would still remain **remain paused** pending operator decision on a further conditional multi-day v002 feature artefact structural QA → feature-family eligibility gate → feature-family research-use decision → feature-family successor-state recording ladder (multi-day analogues of Phase 4bi-A through Phase 4bi-D). None of those is authorised by this merge-closeout.

— end of Phase 4bm-G merge-closeout —
