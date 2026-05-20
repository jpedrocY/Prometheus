# Phase 4bm-F Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording
- **Tier**: Tier 1 (docs + local gitignored output; governance / successor-state recording; multi-day analogue of Phase 4bg-B for the v002 derived family)
- **Type**: docs + local gitignored output — adds two new tracked docs files under `docs/00-meta/implementation-reports/`, narrowly updates `docs/00-meta/current-project-state.md`, and produces exactly one new local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar under `data/microstructure/successor-state/`; no source / test / script / configuration / manifest / sidecar / gate-report mutation; no normalized Parquet, raw zip, feature parquet, label parquet, or any other prior `data/microstructure/` artefact touched
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-F as project-complete on `main` after a clean docs + local gitignored output branch that operationalises the Phase 4bm-E Option B / Decision form 2 outcome by writing the canonical machine-readable Stage-3 successor-state marker for the multi-day v002 normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events) as a sibling artefact, while preserving every retained verdict, every project lock, every on-disk manifest, and every prior `data/microstructure/` artefact byte-identically
- **Branch merged**: `phase-4bm-f/multi-day-derived-family-successor-state-recording`
- **Target branch**: `main`
- **Base**: `main` at `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece` (Phase 4bm-E merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision Memo; Option B / Decision form 2; project-complete on `main`)
- **Direct precedent**: Phase 4bg-B (v001 derived-family research-eligibility successor-state recording; project-complete on `main`)

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-F is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece`
- **Pre-merge `origin/main` SHA**: `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece` (in sync; `git pull --ff-only` reported `Already up to date.`)
- **Phase 4bm-F branch docs commit SHA**: `30c23480c52e3be5127b6cd1ed1ef83867e3664a` (`docs(phase-4bm-f): record multi-day derived-family successor state`; 3 files / +1,139 / -0; single tracked commit on branch)
- **Phase 4bm-F branch tip SHA pre-merge**: `30c23480c52e3be5127b6cd1ed1ef83867e3664a`
- **Merge commit SHA**: `35227cb059a623932c9246c952b49d2d7a998746`
- **Merge commit message**: `docs(phase-4bm-f): merge multi-day derived-family successor-state recording`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `35227cb059a623932c9246c952b49d2d7a998746`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `35227cb059a623932c9246c952b49d2d7a998746` (in sync)
- **Merge-closeout commit SHA**: `37adf9b8760b2f77cd7dc83f959f385ec3e7a343` (`docs(phase-4bm-f): add merge closeout`; 1 file / +444 / -0; this file's commit on `main`)
- **Post-merge-closeout-commit `main` SHA**: `37adf9b8760b2f77cd7dc83f959f385ec3e7a343`
- **Post-merge-closeout-commit `origin/main` SHA**: `37adf9b8760b2f77cd7dc83f959f385ec3e7a343` (pushed cleanly via `35227cb..37adf9b  main -> main`; no force, no skip-hooks, no skip-signing)
- **Final `main == origin/main`**: true (both at `37adf9b8760b2f77cd7dc83f959f385ec3e7a343`)

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-f/multi-day-derived-family-successor-state-recording -m "docs(phase-4bm-f): merge multi-day derived-family successor-state recording"`
- **Strategy**: `ort` (git default; reported by git as `Merge made by the 'ort' strategy.`)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     fb0aa97..35227cb  main -> main
  ```
  Second push (this merge-closeout commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     35227cb..37adf9b  main -> main
  ```

## §4 Files Brought Forward by the Merge

Three tracked files brought forward from the Phase 4bm-F branch into `main`, all from the single source-branch commit (`30c2348`).

**Tracked files added (2):**

1. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-f_multi-day-derived-family-successor-state-recording.md` (NEW, +382; the 23-section main implementation report)
2. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-f_closeout.md` (NEW, +231; Phase 4bm-F closeout)

**Tracked files modified narrowly (1):**

3. `docs/00-meta/current-project-state.md` (MODIFIED, +526 / -0; Phase 4bm-F narrative paragraph + new "Current phase:" block; prior Phase 4bm-E "Current phase:" block preserved verbatim as labelled historical context — pure addition, no deletions, consistent with the Phase 4bm-E precedent pattern)

**This merge-closeout commit — 1 additional tracked file (allowed by the operator authorization for the merge phase):**

4. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-f_merge-closeout.md` (NEW; this file)

**Explicit non-changes:** No `data/microstructure/` file was modified, added, or deleted by the merge commit or by this merge-closeout commit. The Phase 4bm-F branch produced exactly two new local gitignored files under `data/microstructure/successor-state/` (recorded in §7); both are gitignored under `.gitignore:85: data/microstructure/` and **NOT committed**. No file under `src/prometheus/`, `tests/`, `scripts/`, or any other source / test / script surface was modified. No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP file (`.mcp.json` absent before and after), or `.claude/settings.json` / `.claude/settings.local.json` / `.claude/hooks/` / `.claude/agents/` file in `C:\Prometheus` was modified or created. No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph + new "Current phase:" block addition. No prior implementation report, closeout, or merge-closeout was modified. No prior process standard was modified. No manifest, sidecar, gate report, normalized parquet, derived parquet, raw zip, acquisition log, prior successor-state JSON, feature parquet, label parquet, or any other prior data artefact was modified.

## §5 Diff Summary

```text
 docs/00-meta/current-project-state.md              | 526 +++++++++++++++++++++
 .../2026-05-18_phase-4bm-f_closeout.md             | 231 +++++++++
 ...day-derived-family-successor-state-recording.md | 382 +++++++++++++++
 3 files changed, 1139 insertions(+)
```

- 3 files changed
- 1,139 insertions
- 0 deletions
- The merge diff exactly matches the expected change set from the authorization prompt (2 added + 1 modified = 3 tracked files; no `data/microstructure/` files committed; no source / test / script / configuration files).
- `git diff --check` clean across the branch and post-merge (no whitespace errors; no unresolved merge markers).

## §6 Result / Verdict

**LOCAL ARTEFACT PRODUCED — Phase 4bm-F machine-readable Stage-3 successor-state marker for the multi-day v002 derived family recorded on `main`; Phase 4bm-F is project-complete on `main`.**

Phase 4bm-F operationalises the Phase 4bm-E Option B / Decision form 2 outcome by writing the canonical machine-readable Stage-3 successor-state marker for the multi-day v002 normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events; ~1.40 GiB; symbol = BTCUSDT). The successor-state marker is a **sibling artefact**, not a manifest replacement: one new local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar were created under `data/microstructure/successor-state/`. Both files are gitignored under `.gitignore:85: data/microstructure/` and **NOT committed**. The original v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` continues to carry `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically (SHA256 `01c5fa53…` re-verified pre- and post-merge). The v002 raw manifest, the v001 derived manifest, the v001 raw manifest, the Phase 4bm-D authoritative derived gate report + sidecar, the Phase 4bl-D-R raw multi-day PASS gate report, the Phase 4bl-E raw multi-day successor-state JSON, the Phase 4bg-B v001 derived successor-state JSON, and every other prior `data/microstructure/` artefact remain byte-identical. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked). The v002 multi-day derived family now carries a complete Phase 4ba 5-stage ladder of evidence: Stage-0 (Phase 4bm-B normalization), Stage-1 (Phase 4bm-C 56 / 56 structural QA PASS), Stage-2 (Phase 4bm-D 60 / 60 `DERIVED_GATE_PASS`), and Stage-3 (Phase 4bm-F successor-state JSON SHA `72b6edd4…`). **Stage-4 (feature-cleared) remains unauthorized.** Phase 4bm-F is now project-complete on `main`. **Phase 4bm-F does not authorize Phase 4bm-G, any multi-day v002 feature-boundary design memo, any multi-day v002 feature implementation phase, any other successor, MCP, Graphify, agents-by-default, copying Prometheus agent packs or agent memory into the lightweight workspace, or any change to any on-disk manifest.**

## §7 Local Gitignored Outputs

**Two new files, both gitignored under `.gitignore:85: data/microstructure/`; NOT committed.** These are the Phase 4bm-F evidence.

| Path | Size | SHA256 |
| ---- | ---- | ------ |
| `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` | 9,963 bytes | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` |
| `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json.sha256` | 157 bytes | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` |

**Exact sidecar content** (canonical Phase 4bb-F format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`):

```text
72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9  microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json
```

Byte-by-byte verification (all checks PASS): bytes 0..63 = JSON SHA lowercase hex; bytes 64..65 = `0x20 0x20` (two ASCII spaces); bytes 66..155 = ASCII basename `microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` (90 bytes); byte 156 = `0x0A` (LF terminator); total = 64 + 2 + 90 + 1 = **157 bytes** (matches `Get-Item.Length`). The embedded SHA matches the recomputed `Get-FileHash` of the JSON byte-for-byte (no drift). UTF-8 (no BOM, ASCII content only).

**JSON file structural properties:** UTF-8 (no BOM); LF line endings only; two-space indent; final newline at EOF; parses cleanly via `ConvertFrom-Json`. Schema mirrors the Phase 4bg-B v001 derived precedent (compact 38-field base) extended with multi-day-specific fields (90-date range, total event count, v002 raw lineage, Phase 4bl-D-R / Phase 4bl-E raw multi-day evidence, Phase 4bm-B / 4bm-C / 4bm-D pipeline references, Phase 4bm-E decision linkage, Phase 4bg-B v001 precedent cross-reference, v001 derived manifest cross-reference) and the prompt-required non-authorization markers, plus a 43-field `boundary_confirmations` block (all `true`). Key field values re-verified on-disk post-merge:

- `phase_id`: `"4bm-F"`
- `phase_name`: `"Multi-Day Derived-Family Successor-State Recording"`
- `dataset_family`: `"microstructure_normalized_aggtrades_v001"`
- `dataset_version`: `"v002"`
- `successor_state_kind`: `"research_eligibility_successor_state"`
- `successor_stage`: `"Stage-3"`
- `successor_research_eligible`: `true`
- `successor_eligibility_gate_status`: `"pass"`
- `stage_3_policy_admissible`: `true`
- `research_eligible_successor_state`: `true`
- `symbol`: `"BTCUSDT"`
- `utc_date_start`: `"2024-12-01"`
- `utc_date_end`: `"2025-02-28"`
- `date_count`: `90`
- `event_count`: `155153449`
- `original_manifest_sha256`: `"01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"`
- `original_manifest_research_eligible`: `false`
- `original_manifest_eligibility_gate_status`: `"pending"`
- `original_manifest_byte_identical`: `true`
- `raw_family_research_eligible`: `false`
- `raw_family_permanently_ineligible`: `true`
- `phase_4bm_d_derived_gate_report_sha256`: `"3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a"`
- `phase_4bm_d_derived_gate_verdict`: `"DERIVED_GATE_PASS"`
- `phase_4bm_d_derived_gate_result`: `"60/60 PASS"`
- `phase_4bm_e_decision`: `"Option B / Decision form 2"`
- `phase_4bg_b_v001_derived_successor_state_sha256`: `"8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e"`
- `stage_4_feature_cleared`: `false`
- `no_successor_authorization`: `true`
- `successor_authorization_after`: `false`
- All 43 fields in `boundary_confirmations` block: `true`

**Gitignore confirmation** for both file pairs:

```text
.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json
.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json.sha256
```

The pre-existing Phase 4bg-B v001 derived successor-state JSON (SHA `8bcc7d01…`), Phase 4bb-G v001 raw successor-state JSON, Phase 4bl-E v002 raw successor-state JSON (SHA `a0576ca6…`), Phase 4bi-D v001 feature successor-state JSON, Phase 4bj-G v001 label successor-state JSON, and Phase 4bj-J v001 label split-policy successor-state JSON under `data/microstructure/successor-state/` are unchanged.

## §8 Validation Results

### Pre-merge (on Phase 4bm-F branch tip `30c2348`)

- `git status --short`: only the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`). The two new gitignored successor-state files do not appear in status output (confirmed gitignored via `git check-ignore -v`).
- `git branch --show-current`: `phase-4bm-f/multi-day-derived-family-successor-state-recording`.
- `git rev-parse main`: `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece`.
- `git rev-parse origin/main`: `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece` (`main == origin/main` in sync).
- `git rev-parse phase-4bm-f/...`: `30c23480c52e3be5127b6cd1ed1ef83867e3664a`.
- `git rev-parse origin/phase-4bm-f/...`: `30c23480c52e3be5127b6cd1ed1ef83867e3664a` (in sync).
- `git diff main..phase-4bm-f/... --name-status`: 3 files (1 M `current-project-state.md` + 2 A new memos under `docs/00-meta/implementation-reports/`) matching §4.
- `git diff main..phase-4bm-f/... --stat`: 3 files / +1,139 insertions / 0 deletions (matches expected).
- `git diff --check main..phase-4bm-f/...`: clean (no whitespace errors).

### Pre-merge gitignore + successor-state output verification

- `git check-ignore -v data/microstructure/successor-state/`: `.gitignore:85: data/microstructure/` ✓
- `git check-ignore -v <Phase 4bm-F JSON path>`: `.gitignore:85: data/microstructure/` ✓
- `git check-ignore -v <Phase 4bm-F sidecar path>`: `.gitignore:85: data/microstructure/` ✓
- Phase 4bm-F JSON SHA256 recomputed: `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` (size 9,963 bytes) — **matches prompt expected value** ✓
- Phase 4bm-F sidecar SHA256 recomputed: `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` (size 157 bytes) — **matches prompt expected value** ✓
- Exact sidecar content read raw (UTF-8 no BOM): `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9  microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json\n` — **matches prompt expected content** ✓

### Pre-merge on-disk manifest / artefact re-verification

Re-verified on disk pre-merge (all SHAs must match the values recorded in §10 of this closeout):

- v002 derived multi-day index manifest: `research_eligible=False`; `eligibility_gate_status="pending"`; SHA256 `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` ✓
- v002 raw manifest: `research_eligible=False`; `eligibility_gate_status="pending"`; SHA256 `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` ✓
- v001 derived manifest: `research_eligible=False`; `eligibility_gate_status="pending"`; SHA256 `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` ✓
- Phase 4bm-D authoritative gate report: SHA256 `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` ✓
- Phase 4bm-D authoritative sidecar: SHA256 `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` ✓
- Phase 4bl-D-R raw multi-day PASS gate report: SHA256 `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` ✓
- Phase 4bl-E raw multi-day successor-state JSON: SHA256 `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` ✓
- Phase 4bg-B v001 derived successor-state JSON: SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` ✓

### Checkout main + pull

- `git checkout main`: `Switched to branch 'main'.`
- `git pull --ff-only`: `Already up to date.`
- `git status --short` on main pre-merge: only the two pre-existing untracked entries.

### Merge command output

- `git merge --no-ff phase-4bm-f/multi-day-derived-family-successor-state-recording -m "docs(phase-4bm-f): merge multi-day derived-family successor-state recording"`: `Merge made by the 'ort' strategy.`
- Files: 3 files changed, 1,139 insertions(+), 0 deletions(-).
- Conflicts: none.
- Merge commit SHA: `35227cb059a623932c9246c952b49d2d7a998746`.

### Post-merge (on `main` after the merge commit)

- `git diff --check` (post-merge): clean — exit code 0 (no whitespace errors, no unresolved markers).
- `git status --short` (post-merge, pre-closeout-commit): only the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).
- `git log --oneline -8 --decorate` (post-merge, pre-closeout-commit):
  ```text
  35227cb (HEAD -> main) docs(phase-4bm-f): merge multi-day derived-family successor-state recording
  30c2348 (origin/phase-4bm-f/multi-day-derived-family-successor-state-recording, phase-4bm-f/multi-day-derived-family-successor-state-recording) docs(phase-4bm-f): record multi-day derived-family successor state
  fb0aa97 (origin/main, origin/HEAD) docs(phase-4bm-e): finalize merge closeout shas
  d6acae5 docs(phase-4bm-e): add merge closeout
  fcc1bd0 docs(phase-4bm-e): merge multi-day derived-family research eligibility decision memo
  1715a8a (origin/phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo, phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo) docs(phase-4bm-e): add multi-day derived family research eligibility decision memo
  8234375 docs(phase-4bm-d-p1): add merge closeout
  3ddad02 docs(phase-4bm-d-p1): merge lightweight claude workspace standard
  ```
- `git push origin main`: `fb0aa97..35227cb  main -> main` (fast-forward push of the merge commit; no force, no skip-hooks, no skip-signing).
- `git rev-parse main` (post-push): `35227cb059a623932c9246c952b49d2d7a998746`.
- `git rev-parse origin/main` (post-push): `35227cb059a623932c9246c952b49d2d7a998746` (in sync).

### Post-merge artefact re-verification

Re-computed on disk post-merge — every SHA byte-identical to pre-merge:

- v002 derived multi-day index manifest: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` ✓
- v002 raw manifest: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` ✓
- v001 derived manifest: `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` ✓
- Phase 4bm-D authoritative gate report: `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` ✓
- Phase 4bm-D authoritative sidecar: `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` ✓
- Phase 4bl-D-R raw multi-day PASS gate report: `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` ✓
- Phase 4bl-E raw multi-day successor-state JSON: `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` ✓
- Phase 4bg-B v001 derived successor-state JSON: `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` ✓
- Phase 4bm-F v002 derived successor-state JSON: `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` ✓
- Phase 4bm-F v002 derived sidecar: `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` ✓

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by this merge phase, and were **not** invoked by the Phase 4bm-F branch itself.

**Justification.** Phase 4bm-F is a Tier 1 docs + local gitignored output successor-state recording phase per `docs/00-meta/process/phase-risk-tiering-standard.md`. The Phase 4bm-F branch and this merge commit introduce zero source / test / script / configuration changes — only three tracked documentation files are touched (1 modified + 2 added) plus this single additional merge-closeout file, and only two new local gitignored files under `data/microstructure/successor-state/` (which are not committed). Per the established Tier 1 docs + local gitignored output successor-state recording precedent — **Phase 4bg-B (the direct v001 derived-family successor-state recording precedent that this phase mirrors)**, Phase 4bb-G (v001 raw successor-state), Phase 4bl-E (v002 raw multi-day successor-state), Phase 4bi-D (v001 feature successor-state), Phase 4bj-G (v001 label successor-state), and Phase 4bj-J (v001 label split-policy successor-state) each explicitly skipped `ruff` / `mypy` / `pytest` for the same reason, the code / type / test gate subset is deliberately not invoked for this merge. No new regression is possible by construction because no source / test / script / configuration file is modified. The most recent authoritative whole-repo `pytest` baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; two pre-existing `KeyError: 'trade_count'` simulation failures on `tests/simulation/test_backtest_real_2026_03.py` in `src/prometheus/research/data/storage.py:232` are unrelated to Phase 4bm-F and are preserved as the baseline). Phase 4bm-F introduces zero new regressions vs that baseline.

### Gitignore policy verification

- `git check-ignore -v data/microstructure/`: `.gitignore:85: data/microstructure/` (pre-existing rule, unchanged).
- `git check-ignore -v data/microstructure/successor-state/`: `.gitignore:85: data/microstructure/`.
- `git check-ignore -v <Phase 4bm-F JSON path>`: `.gitignore:85: data/microstructure/`.
- `git check-ignore -v <Phase 4bm-F sidecar path>`: `.gitignore:85: data/microstructure/`.
- No new gitignored paths were introduced by Phase 4bm-F.

## §9 Upstream Immutability Evidence

Phase 4bm-F is a docs + local gitignored output successor-state recording phase. It writes exactly two new local files under `data/microstructure/successor-state/<new file pair>` and touches no other path under `data/microstructure/`. Every prior local artefact under `data/microstructure/` is byte-identical pre- and post-Phase-4bm-F by construction: no other file under `data/microstructure/` is read in a mutating way, hashed in a mutating way, written, deleted, or otherwise modified by the source branch, the merge commit, or this merge-closeout commit.

Specific governance and evidence witnesses re-confirmed at the start of Phase 4bm-F and re-confirmed post-merge:

| Artefact | SHA256 (pre and post Phase 4bm-F) |
| -------- | ---------------------------------- |
| v002 derived multi-day index manifest (`microstructure_normalized_aggtrades_v001__v002.json`) | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 raw manifest (`microstructure_raw_aggtrades_v001__v002.json`) | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v001 derived manifest (`microstructure_normalized_aggtrades_v001__v001.json`) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Phase 4bm-D authoritative derived gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| Phase 4bl-D-R raw multi-day `RAW_MULTIDAY_GATE_PASS` report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| Phase 4bg-B v001 derived successor-state JSON (direct precedent) | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

The 90 v002 per-day Parquets, 90 v002 sidecars, 90 v002 raw zips, and 90 v002 raw zip sidecars are unchanged byte-for-byte by Phase 4bm-F by construction. Every other prior `data/microstructure/` artefact (Phase 4bd v001 normalized Parquet `2b3d6978…`, Phase 4az v001 raw artefacts `a371edd4…` / `f560c2e5…` / `b80c2768…` / `f88b28b4…`, Phase 4bb-D v001 raw gate report `96f09159…`, Phase 4bf v001 derived gate report `dd4e0c1c…`, Phase 4bh v001 feature parquet and manifest if present locally, Phase 4bj-C v001 label parquet and manifest if present locally, Phase 4bj-G v001 label successor-state JSON if present, Phase 4bi-D v001 feature successor-state JSON if present, Phase 4bj-J v001 label split-policy successor-state JSON if present, the Phase 4bm-D preliminary pre-commit sanity gate report `ffde54bb…` and its sidecar, and any other artefact present locally) is preserved bit-for-bit.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

## §10 Manifest State Preservation

- **v002 derived multi-day index manifest** (`microstructure_normalized_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bm-B output. Not modified by Phase 4bm-D, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, or this merge. SHA256 `01c5fa53…` byte-identical (re-verified on disk pre- and post-merge).
- **v002 raw manifest** (`microstructure_raw_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bl-C. Not modified. SHA256 `01696786…` byte-identical.
- **v001 derived manifest** (`microstructure_normalized_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4bd. Not modified. SHA256 `f6f0d947…` byte-identical.
- **v001 raw manifest** (`microstructure_raw_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. **Unchanged** from Phase 4az. Not modified. SHA256 `a371edd4…` byte-identical.
- **Every other manifest** under `data/microstructure/manifests/` and `data/manifests/`: unchanged.

No `research_eligible` flip occurred on any actual on-disk manifest. No `eligibility_gate_status` transition occurred on any actual on-disk manifest. No `chronological_split_policy` change occurred on any actual on-disk manifest.

The Phase 4bm-F successor-state JSON's `successor_research_eligible: true` is a **sibling-artefact assertion only** — it lives in the local gitignored successor-state JSON at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` (SHA `72b6edd4…`) and does **not** modify the original v002 derived multi-day index manifest or any other on-disk manifest. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and is never invoked by Phase 4bm-F. Any future tool that wishes to interpret the v002 derived family as Stage-3 must read this successor-state artefact, not the original manifest.

The v002 multi-day derived family now carries a complete Phase 4ba 5-stage ladder of evidence:

- Stage-0 (acquired + normalized): Phase 4bm-B output (90 per-day Parquets + 90 sidecars + v002 multi-day index manifest).
- Stage-1 (inspected): Phase 4bm-C 56 / 56 multi-day structural QA PASS.
- Stage-2 (gate-passed at report level): Phase 4bm-D 60 / 60 PASS with `DERIVED_GATE_PASS`; 19 / 19 boundary confirmations `True`.
- **Stage-3 (machine-readable successor-state marker)**: Phase 4bm-F successor-state JSON (SHA `72b6edd4…`) + paired Phase 4bb-F sidecar (SHA `1e9ffb23…`).

**Stage-4 (feature-cleared) remains unauthorized** for v002.

## §11 Boundary Confirmations

The Phase 4bm-F merge honours every relevant boundary. Citing the canonical reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 by name, plus phase-specific additions:

- **N-ACQUISITION** applies — no acquisition; no download; no extension of any existing dataset; no creation or modification of raw data files.
- **N-ENDPOINT** applies — no Binance / public / authenticated / private endpoint called; no `data.binance.vision` contact; no WebSocket opened.
- **N-CREDENTIALS** applies — no credential used, read, created, or referenced; `.env` not read or created; `.mcp.json` not read or created; MCP / Graphify not enabled; no order placed; no exchange-write surface contacted.
- **N-MANIFEST** applies — no actual manifest file modified; no `research_eligible` flip on any actual on-disk manifest; no `eligibility_gate_status` transition on any actual on-disk manifest; no `chronological_split_policy` change; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- **N-GATE-RERUN** applies — no raw / derived / feature / label / metrics gate rerun; no new gate report generated; the Phase 4bm-D authoritative gate report is read-only referenced, not regenerated.
- **N-DERIVATION** applies — no normalization, derivation, feature, or label computation; no kernel run; no derived / feature / label parquet produced; no v002 feature or label artefact exists.
- **N-DIAGNOSTICS-ML-STRATEGY** applies — no diagnostics, ML, strategy, signal construction, or backtest; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit output.
- **N-PHASE-5** applies — no Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.
- **N-VERDICT-LOCK** applies — no retained verdict revised (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure all preserved verbatim); no project lock changed (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt Claude Code context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace execution standard — all preserved verbatim).

**N-SUCCESSOR-STATE — single named exception**: Phase 4bm-F is the explicit scope authorising the creation of exactly **one** new local gitignored v002 derived successor-state JSON + paired canonical Phase 4bb-F sidecar under `data/microstructure/successor-state/`. No other successor-state artefact is created, modified, or deleted by this phase or this merge. The Phase 4bl-E v002 raw successor-state JSON (`a0576ca6…`), the Phase 4bg-B v001 derived successor-state JSON (`8bcc7d01…`), the Phase 4bb-G v001 raw successor-state JSON, the Phase 4bi-D v001 feature successor-state JSON, the Phase 4bj-G v001 label successor-state JSON, and the Phase 4bj-J v001 label split-policy successor-state JSON are all unchanged.

Additional merge-level confirmations:

- no tracked `data/microstructure/` file committed by either the source-branch commit, the merge commit, or this merge-closeout commit
- no `data/research/` file committed
- no `.claude/` file in `C:\Prometheus` modified or committed (local operator-side hook tooling under `C:\ClaudeRuns\prometheus-light\.claude\...` is not part of `C:\Prometheus`)
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
- no retained verdict revised; no project lock loosened; no M0 amendment; no Phase 4al rule amended; no Phase 4aw invariant amended; no Phase 4bb-F canonical path policy amended; no Phase 4bl-F rule amended; no Phase 4bm-A-P1 standard amended; no Phase 4bm-D-P1 standard amended; no Phase 4bm-E decision changed
- no successor authorized (Phase 4bm-G / multi-day v002 feature-boundary design / multi-day v002 feature implementation / multi-day v002 feature-family phases / multi-day v002 label-family phases / Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical all remain unauthorized)
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

All preserved verbatim by Phase 4bm-F and by this merge.

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
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; the new Phase 4bm-F sidecar is canonical LF natively; R-SIDECAR-CRLF not invoked)
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard (cited)
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard (cited; honoured by this phase — Claude Code launched from the lightweight workspace `C:\ClaudeRuns\prometheus-light` with all shell commands using `cd C:\Prometheus && <command>` per the standard)
- Phase 4am .. Phase 4bm-E results — all preserved verbatim

## §14 No-Rescue Constraints

The Phase 4bm-F merge records a Tier 1 docs + local gitignored output successor-state recording that creates exactly one new local gitignored sibling artefact (the v002 derived Stage-3 successor-state JSON + paired canonical Phase 4bb-F sidecar) for the multi-day v002 normalized derived family. The successor-state JSON's `successor_research_eligible: true` is a sibling-artefact assertion only; it does NOT modify any actual on-disk manifest. The merge does NOT, and CANNOT, be construed as authorising:

- ML model training, model selection, strategy hypothesis generation, signal construction, or any conversion of the v002 Stage-3 successor-state marker into trading signals
- strategy logic, position state, entry / exit rules, or backtest design
- paper / shadow / live-readiness / deployment / exchange-write work
- Phase 4 canonical or Phase 5 authorisation
- transitioning any actual on-disk manifest's `research_eligible` flag from `false` to `true` from this evidence alone (no manifest mutation occurred and the Phase 4aw always-raises invariant is preserved)
- transitioning any actual on-disk manifest's `eligibility_gate_status` from `"pending"` to anything else
- transitioning any actual on-disk manifest's `chronological_split_policy`
- creating any further successor-state JSON (no Phase 4bm-G is authorized; no v002 feature-family successor-state, label-family successor-state, or sibling-version successor-state is created or authorized)
- features, labels, diagnostics, ML, strategy, or backtests on v002 (or on v001)
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- cross-symbol acquisition (the v002 cross-symbol evidence gap is unchanged from v001)
- old-strategy alt-symbol rerun or cooled-down-family reopening (cooled-down families — price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane — all remain cooled down)
- 5m research-thread reopening (Phase 3t closure preserved)
- revising or weakening any retained verdict (R2 / F1 / D1-A / V2 / G1 / C1 first-specs remain terminally rejected as recorded; H0 framework anchor, R3 baseline-of-record, and R1a / R1b-narrow retained-non-leading status all preserved)
- cross-strategy hybrids (V1-D1, F1-D1, V2-G1, G1-C1, or any other combination)
- -prime, -narrow, -extension, or -hybrid variants of any historical candidate
- §11.6 cost-realism relaxation, §1.7.3 risk / leverage / one-position / mark-price stop amendment, or any other lock loosening
- M0 amendment, post-null cooldown weakening, cooled-down families list shortening, or memo template alteration
- use of Phase 4l V2 forensic numbers, Phase 4r G1 forensic numbers, or Phase 4x C1 forensic numbers as parameter-selection inputs
- use of Phase 3s Q1–Q7 diagnostic outputs as rule-input candidates
- MCP / Graphify / `.mcp.json` / credential enablement
- copying Prometheus agent packs or agent memory into the lightweight workspace at `C:\ClaudeRuns\prometheus-light`
- enabling agents-by-default for heavy execution sessions
- committing local hook files from the lightweight workspace into `C:\Prometheus` without a separately authorized process phase
- amending the Phase 4bm-A-P1 thin-prompt Claude Code context-management standard (cited; not amended)
- amending the Phase 4bm-D-P1 lightweight Claude Code workspace execution standard (cited and honoured; not amended)
- amending the Phase 4bm-E decision (Option B / Decision form 2 preserved verbatim)
- public-endpoint code calls, user-stream implementation, live WebSocket implementation, or any authenticated-API / private-endpoint access
- any change to any on-disk v002 / v001 manifest

Stage-3 at the successor-state-marker level for the multi-day v002 derived family is necessary but not sufficient evidence for any of the above; sufficient evidence requires separately authorized subsequent phases under the established phase ladder (a future multi-day v002 feature-boundary design memo, a future multi-day v002 feature implementation phase, and later v002 feature-family / label-family / research / feasibility / strategy / backtest phases under M0 admissibility and Phase 4al §14 hierarchy).

## §15 Successor Authorization

**None.**

This merge-closeout records that Phase 4bm-F is project-complete on `main`. It does **not** authorize:

- **Phase 4bm-G** — any further v002 multi-day governance phase
- future docs-only **multi-day v002 feature-boundary design memo** (multi-day analogue of Phase 4bh-A / Phase 4bh-B; would cite the Phase 4bm-F successor-state SHA `72b6edd4…` and predeclare future v002 feature schema with lineage SHAs; would not authorize feature computation)
- future code + docs **multi-day v002 feature schema / feature computation implementation** (multi-day analogue of Phase 4bh; only after Stage-4 authorization on v002)
- future multi-day v002 **feature-family structural QA / eligibility gate / research-use decision / successor-state recording** (multi-day analogues of Phase 4bi-A / Phase 4bi-B / Phase 4bi-C / Phase 4bi-D)
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
- any further successor-state JSON creation
- agents-by-default for heavy Claude Code execution sessions
- copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light`
- committing local hook files from the lightweight workspace into `C:\Prometheus`

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

## §16 Recommended State

**Remain paused.**

Phase 4bm-F is now project-complete on `main` (this merge-closeout records the lifecycle anchor). The v002 multi-day derived family carries a complete Phase 4ba 5-stage ladder of evidence: Stage-0 (Phase 4bm-B), Stage-1 (Phase 4bm-C 56/56 PASS), Stage-2 (Phase 4bm-D 60/60 `DERIVED_GATE_PASS`), and Stage-3 (Phase 4bm-F successor-state JSON SHA `72b6edd4…`). Stage-4 (feature-cleared) remains unauthorized. The actual v002 derived multi-day index manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked). The operator's broader pause decision continues to apply.

**Conditional next, NOT authorized:**

Future operator-authorized **multi-day v002 feature-boundary design memo** (multi-day analogue of Phase 4bh-A / Phase 4bh-B) would be the natural next step in the v002 lifecycle ladder. It would extend the v001 feature-boundary design to v002 inputs, cite the Phase 4bm-F successor-state SHA `72b6edd4…` verbatim, predeclare future v002 feature schema with lineage SHAs (Phase 4bm-D gate report `3b45e70b…`, Phase 4bm-F successor-state `72b6edd4…`, v002 derived multi-day index manifest `01c5fa53…`, raw lineage), and would not authorize feature computation. It is **not** authorised by this merge-closeout.

After any such v002 feature-boundary design memo merge, the recommended state would remain **remain paused** pending operator decision on a further conditional **multi-day v002 feature implementation phase** (multi-day analogue of Phase 4bh). That phase, if ever authorized, would compute v002 features locally under `data/microstructure/features/` (gitignored; not committed) and would still not authorize ML, strategy, or backtest work. It is **not** authorised by this merge-closeout.

— end of Phase 4bm-F merge-closeout —
