# Phase 4bm-P — Merge Closeout

**Phase identity:** Phase 4bm-P — Multi-Day V002 Label Artefact Structural QA Memo.
**Phase type:** docs-only + read-only local artefact analysis (Tier 1 Full Phase).
**Status:** **merged into `main`**; project-complete after this merge-closeout commit + the subsequent SHA-finalization commit.

## 1. Phase identity

Phase 4bm-P is the multi-day v002 analogue of the v001 **Phase 4bj-D** label artefact structural QA memo. It performs a read-only structural QA review of the local gitignored Phase 4bm-O v002 label artefacts (90 per-day label Parquets + 90 paired Phase 4bb-F sidecars + 1 label manifest + 1 paired sidecar = 182 total local gitignored label artefacts inspected) against the Phase 4bm-N locked 40-column schema, the Phase 4bm-M label-family boundary / design, the Phase 4bm-L Feature Stage-5 marker, the Phase 4bm-J `FEATURE_GATE_PASS` evidence, and the Phase 4bm-O manifest evidence.

**Phase 4bm-P is read-only label artefact structural QA.**
**No label artefact is modified by Phase 4bm-P.**
**No label artefact is committed by Phase 4bm-P.**
**Phase 4bm-Q is not authorized by Phase 4bm-P.**
**Label-family eligibility gate is not authorized by Phase 4bm-P.**
**Label-family research-use is not authorized by Phase 4bm-P.**
**Label-family successor-state recording is not authorized by Phase 4bm-P.**
**Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-P.**
**No feature artefact was modified.**
**No upstream artefact was mutated.**
**No data/microstructure file was committed.**

## 2. Branch merged

`phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo`

## 3. Base `main` SHA before merge

`75371ffd8607f3586130f02d6ffd124b7b707dfb` (Phase 4bm-O merge-closeout SHA-finalization commit; pre-merge `main == origin/main`).

## 4. Phase branch commit SHA(s)

- `df2cf6cb2347a79ef780da0c8ff1df1435561e17` (precursor) — `docs(phase-4bm-p): add multi-day v002 label artefact structural qa memo`.
- `d177ecc1f19710a16a26cf299a6dc32ecefce090` (branch HEAD) — `docs(phase-4bm-p): add closeout`.

## 5. Merge commit SHA

`78b3db3193d449dd6e61eb82dd81c2207551d9de` — `docs(phase-4bm-p): merge multi-day v002 label artefact structural qa memo` (no-fast-forward merge using the project-standard `--no-ff` merge method).

## 6. Merge-closeout commit SHA

`33b8082a600f9f3192325e4fc5d6ae4e9d97e68a` — `docs(phase-4bm-p): add merge closeout` (the commit that added this file on `main`).

## 7. Post-merge `main` / `origin/main` SHA evolution

- After `git merge --no-ff phase-4bm-p/...`: `main = 78b3db3193d449dd6e61eb82dd81c2207551d9de`.
- After first `git push origin main`: `main = origin/main = 78b3db3193d449dd6e61eb82dd81c2207551d9de`.
- After `docs(phase-4bm-p): add merge closeout` commit: `main = 33b8082a600f9f3192325e4fc5d6ae4e9d97e68a`.
- After second `git push origin main` (push of the merge-closeout commit; remote update line `78b3db3..33b8082  main -> main`): `main = origin/main = 33b8082a600f9f3192325e4fc5d6ae4e9d97e68a`.
- `main == origin/main` after the merge-closeout commit push: **YES**.

Per the project SHA-hygiene boundary, the SHA of the immediately-following SHA-finalization commit (`docs(phase-4bm-p): finalize merge closeout shas`) is intentionally **NOT** recorded inside this file (recording it would create an infinite self-reference, since the SHA-finalization commit modifies only this file and that modification would change the SHA itself). The SHA-finalization commit is recorded separately in the final operator report.

## 8. Merge method

`git merge --no-ff phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo -m "docs(phase-4bm-p): merge multi-day v002 label artefact structural qa memo"` — no-fast-forward merge into `main`, matching the project-standard merge method used for prior Phase 4bm-* merges.

## 9. Files brought forward by merge

| File | Action |
| --- | --- |
| `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_multi-day-v002-label-artefact-structural-qa-memo.md` | Added (new 31-section Tier 1 structural QA memo; 789 inserted lines) |
| `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_closeout.md` | Added (162 inserted lines) |
| `docs/00-meta/current-project-state.md` | Modified narrowly (Phase 4bm-P narrative paragraph + new "Current phase:" block; prior Phase 4bm-O paragraph and "Current phase:" block preserved as labelled historical context; 348 inserted lines net) |

Total: **3 files changed; 1,299 insertions; 0 deletions** (per `git diff --stat main^..main`).

**No** source / test / script / configuration file changed. **No** `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/` change. **No** path under `data/microstructure/` is in the diff.

## 10. Files added by this merge-closeout commit

This merge-closeout commit (`docs(phase-4bm-p): add merge closeout`) adds exactly one file:

- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_merge-closeout.md` (this file).

No other tracked file is modified by the merge-closeout commit.

## 11. Decision / outcome recorded by Phase 4bm-P

- Read-only label artefact structural QA completed against the local gitignored Phase 4bm-O v002 label artefacts.
- **Structural QA verdict: LABEL_STRUCTURAL_QA_PASS — label artefact remains not research-eligible.** Equivalent to the Phase 4bj-D v001 precedent phrasing "STRUCTURAL QA PASS — label artefact remains not research-eligible" with the `<FAMILY>_STRUCTURAL_QA_PASS` naming convention also used in Phase 4bm-I.
- **182 local gitignored label artefacts inspected** (90 per-day label Parquets + 90 paired Phase 4bb-F sidecars + 1 label manifest + 1 paired sidecar).
- **No label artefact modified.** No label parquet, sidecar, manifest, or manifest sidecar was opened for write at any point during Phase 4bm-P.
- **No label artefact committed.** All 182 inspected artefacts are gitignored under `.gitignore:85: data/microstructure/`.
- **No feature artefact modified.** The v002 feature manifest, its sidecar, and the 90 per-day feature Parquets are byte-identical pre/post QA.
- **No upstream artefact mutated.** All 9 spot-checked upstream lineage artefacts (Phase 4bm-J + sidecar; Phase 4bm-L + sidecar; v002 feature manifest + sidecar; v002 derived/normalized manifest + sidecar; v002 raw manifest) are byte-identical pre/post QA; the v002 derived/normalized manifest and v002 raw manifest still carry `research_eligible = false` / `eligibility_gate_status = "pending"`; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).
- **No `data/microstructure/` file was committed.** `git diff main^..main --name-only` shows only the three tracked docs files above.

## 12. Tracked docs files merged

As enumerated in §9: the 31-section structural QA memo, the closeout, and the narrow `current-project-state.md` update. Total **3 tracked docs files**.

## 13. Local gitignored outputs created by Phase 4bm-P

**None.** Phase 4bm-P is read-only and creates no `data/microstructure/` artefact, no gate report, no successor-state JSON, no chronological split-policy artefact, no QA-result JSON, and no temporary tracked file. The QA inspector Python script was kept in the OS temp directory (`C:\Users\jpedr\AppData\Local\Temp\phase4bmp_qa.py`), outside the tracked tree, and is not committed.

## 14. Local gitignored artefacts inspected by Phase 4bm-P

- **90 v002 label Parquets** under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet` (one per UTC date 2024-12-01..2025-02-28 inclusive).
- **90 paired canonical Phase 4bb-F sidecars** under the same tree.
- **1 v002 label manifest** at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`.
- **1 paired canonical Phase 4bb-F sidecar** at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256`.

### Label manifest evidence

| Field | Value |
| --- | --- |
| Path | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` |
| SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` |
| Size | 84,732 bytes |

### Label manifest sidecar evidence

| Field | Value |
| --- | --- |
| Path | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` |
| SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` |
| Size | 114 bytes |
| Format | canonical Phase 4bb-F (`<sha256_lowercase_hex><two ASCII spaces><basename><LF>`); ASCII / UTF-8 no BOM; LF only |

Exact label manifest sidecar content:

```text
5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed  microstructure_labels_aggtrades_v001__v002.json
```

## 15. Label structural QA summary

| Field | Value |
| --- | --- |
| `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` |
| Aggregate row count (90 per-day parquets) | **155,153,449** |
| Column count | **40** (Phase 4bm-N §14 canonical schema; 17 lineage + 1 `label_config_hash` + 8 labels + 14 support) |
| Date count | **90** (2024-12-01 .. 2025-02-28 inclusive) |
| Horizons (`horizon_list`) | `["1s", "5s", "15s", "60s"]` |
| `horizon_ms_list` | `[1000, 5000, 15000, 60000]` |
| `envelope_terminal_unix_ms` | `1740787199996` (2025-02-28T23:59:59.996Z) |
| `censored_per_horizon` | `{"1s": 14, "5s": 39, "15s": 170, "60s": 634}` |
| `invalid_price_row_count` | `0` |
| Aggregate label parquet byte size | **6,145,349,264** bytes (≈ 5.72 GiB) |
| Per-day row-count parity vs v002 feature per-day | **90 / 90 MATCH** (1:1; aggregate 155,153,449 equals v002 feature row count) |
| Per-day label parquet SHA vs manifest field | **90 / 90 MATCH** |
| Per-day label parquet byte_size vs manifest field | **90 / 90 MATCH** |
| Per-day label sidecar canonical Phase 4bb-F + SHA-consistent | **90 / 90 PASS** |
| All 90 parquets share identical canonical 40-column schema | **YES** (pyarrow `schema_arrow.names` cross-check) |
| Forbidden-substring audit over 21-token list (pnl/profit/loss/mfe/mae/r_multiple/equity/position/alpha/edge/prediction/model/score/decision/strategy/entry/exit/signal/target/barrier/liquidation) | **0 hits** |
| Per-row censoring rule (`flag iff feature_timestamp_ms + horizon_ms_H > envelope_terminal_unix_ms`) | **0 violations** across sampled rows × 4 horizons × 6 dates |
| Censoring concentration | entirely on envelope-terminal day `2025-02-28` (the only day with non-zero per-horizon censored counts) |
| `forward_direction_H` value range | `{-1, 0, 1, null}` strict-sign across all sampled rows |
| `label_invalid_price_flag` aggregate | `False` for every sampled row (consistent with `invalid_price_row_count = 0`) |
| `label_any_censored_flag = OR(horizon_censored_flag_*)` | byte-for-byte match across every sampled row |
| Identity alignment (`agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`, `row_index`) with v002 feature parquets | byte-for-byte match across every sampled row |
| Per-day `source_feature_parquet_sha256` lineage vs v002 feature manifest | **90 / 90 MATCH** |
| Targeted v002 label pytest | **91 / 91 PASS** in 0.65s |
| 9 / 9 upstream lineage artefacts byte-identical pre/post QA | **PASS** |
| Structural defects | **None** |
| INDETERMINATE rows | **None** |
| Non-blocking observations (§25 in the main memo) | informational only; do not change the verdict |

## 16. Evidence summary

### Phase 4bm-O label artefact evidence

- Label manifest SHA256: `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (MATCH Phase 4bm-O byte-for-byte).
- Label manifest sidecar SHA256: `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (MATCH; canonical Phase 4bb-F 114 bytes; no CRLF; no BOM).
- `label_config_hash`: `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` (MATCH; constant on every label parquet row).

### Phase 4bm-N schema finalization

- `dataset_family = "microstructure_labels_aggtrades_v001"`, `dataset_version = "v002"`, `label_schema_version = "v001"`.
- 40-column canonical schema (Phase 4bm-N §14): exact ordered match with the manifest's `schema_column_list` and every one of the 90 per-day Parquets.
- Forbidden-substring detector: 0 hits.

### Phase 4bm-L Feature Stage-5 marker

- Phase 4bm-L successor-state JSON SHA256: `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (MATCH pre/post QA; pinned in every label parquet row via `source_feature_successor_state_sha256`).
- Phase 4bm-L successor-state sidecar SHA256: `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` (MATCH pre/post QA).
- Phase 4bm-K decision: **Outcome 1 / Decision form 1** → equivalent label `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`.

### Phase 4bm-J `FEATURE_GATE_PASS` evidence

- Phase 4bm-J gate verdict: `FEATURE_GATE_PASS` (50/50 PASS; 0 FAIL; 0 ERROR; 0 NOT_APPLICABLE).
- Phase 4bm-J gate report SHA256: `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (MATCH pre/post QA; pinned in every label parquet row via `source_phase_4bm_j_gate_report_sha256`).
- Phase 4bm-J gate sidecar SHA256: `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` (MATCH pre/post QA).

### Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS` precedent

The sibling Phase 4bm-I v002 feature artefact structural QA memo (`FEATURE_STRUCTURAL_QA_PASS`) is the direct multi-day v002 sibling precedent for the QA shape used by Phase 4bm-P; both phases use the same canonical full-coverage + sampled-deep-scan inspection methodology.

### v002 feature artefact evidence

- v002 feature manifest SHA256: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (MATCH pre/post QA; pinned in every label parquet row via `source_feature_manifest_sha256`).
- v002 feature manifest sidecar SHA256: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` (MATCH pre/post QA).
- `feature_config_hash`: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` (recorded in label manifest top-level).
- v002 feature row count: **155,153,449** (1:1 parity with v002 label row count).
- v002 feature schema column count: **62**.

## 17. Upstream lineage SHA table

| Artefact | Expected SHA256 | Status |
| --- | --- | --- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | MATCH pre/post QA |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | MATCH pre/post QA |
| Phase 4bm-L successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | MATCH pre/post QA |
| Phase 4bm-L successor-state sidecar | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` | MATCH pre/post QA |
| Phase 4bm-J gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | MATCH pre/post QA |
| Phase 4bm-J gate sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | MATCH pre/post QA |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | MATCH pre/post QA |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | MATCH pre/post QA |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | MATCH pre/post QA |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged (transitively via raw manifest and prior Phase 4bm-O immutability evidence) |
| Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged (transitively) |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged (transitively) |
| Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | MATCH pre/post QA |
| Phase 4bm-F v002 derived-family successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | MATCH pre/post QA |

## 18. Validation commands and results

### Pre-merge validation (on the Phase 4bm-P branch / pre-merge `main`)

| Command | Result |
| --- | --- |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected pre-existing) |
| `git branch --show-current` | `phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo` (on branch) → `main` (after checkout) |
| `git rev-parse main` (pre-merge) | `75371ffd8607f3586130f02d6ffd124b7b707dfb` |
| `git rev-parse origin/main` (pre-merge) | `75371ffd8607f3586130f02d6ffd124b7b707dfb` (in sync) |
| `git rev-parse phase-4bm-p/...` | `d177ecc1f19710a16a26cf299a6dc32ecefce090` |
| `git rev-parse origin/phase-4bm-p/...` | `d177ecc1f19710a16a26cf299a6dc32ecefce090` (in sync) |
| `git diff main..phase-4bm-p/... --stat` | `3 files changed, 1,299 insertions(+)` |
| `git diff main..phase-4bm-p/... --name-status` | `M docs/00-meta/current-project-state.md` + 2 `A` for the two new docs files (no other path) |
| `git diff --check main..phase-4bm-p/...` | clean (exit 0; no whitespace, no conflict markers) |
| `git check-ignore -v data/microstructure/labels/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` | `.gitignore:85: data/microstructure/` |
| Label parquet count under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/` | **90** |
| Label sidecar count under same tree | **90** |
| Label manifest SHA256 (recomputed via stdlib `hashlib`) | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` MATCH |
| Label manifest sidecar SHA256 (recomputed) | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` MATCH |
| Exact label manifest sidecar bytes | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed  microstructure_labels_aggtrades_v001__v002.json\n` (114 bytes; ASCII; no CRLF; no BOM) |
| Label manifest JSON parses cleanly | YES (`json.loads` succeeds; 65 top-level keys) |
| Label manifest `row_count` | `155153449` |
| Label manifest `column_count` | `40` |
| Label manifest `date_count` | `90` |
| Label manifest `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` |
| Label manifest `censored_per_horizon` | `{"1s": 14, "5s": 39, "15s": 170, "60s": 634}` |
| Label manifest `invalid_price_row_count` | `0` |
| Label manifest `research_eligible` | `false` |
| Label manifest `eligibility_gate_status` | `"pending"` |
| Label manifest `label_family_research_use_authorized` | `false` |
| Label manifest `stage_5_label_cleared` | `false` |
| Label manifest `chronological_split_policy` | `"not_yet_defined"` |
| Upstream SHA spot-check (9 governance artefacts) | 9 / 9 MATCH (see §17) |
| Phase 4bm-F derived-family successor-state SHA256 | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` MATCH |
| Phase 4bm-D authoritative derived-family gate report SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` MATCH |
| No label output in `git status` | confirmed (all gitignored under `.gitignore:85`) |
| No `data/microstructure/` path staged | confirmed |

### Post-merge validation (on `main` after merge + push)

| Command | Result |
| --- | --- |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked |
| `git log --oneline -8 --decorate` | latest is `78b3db3 docs(phase-4bm-p): merge multi-day v002 label artefact structural qa memo` |
| `git rev-parse main` (post-merge) | `78b3db3193d449dd6e61eb82dd81c2207551d9de` |
| `git rev-parse origin/main` (post-merge push) | `78b3db3193d449dd6e61eb82dd81c2207551d9de` |
| `git diff --check` (post-merge) | clean |
| `main == origin/main` | YES |

## 19. Quality gate commands and results / skipped-check rationale

Because Phase 4bm-P is docs-only + read-only structural QA, the only required pre-merge quality gate is:

```text
git diff --check main..phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo
```

Result: **clean** (exit 0). No whitespace error, no conflict marker, no merge-conflict residue.

**No project-specific lightweight markdown gate exists** in the Prometheus repo (no `markdownlint`, `vale`, `mdsf`, or equivalent target is configured in `pyproject.toml`, `package.json`, or `Makefile`).

`ruff`, `mypy`, and full whole-repo `pytest` were intentionally **not** rerun at the merge phase. Rationale:

- Phase 4bm-P modifies **no** source code, **no** tests, **no** scripts, **no** configurations.
- Phase 4bm-P branch already recorded a passing **targeted v002 label pytest** sweep (`91 / 91 passed in 0.65s`).
- Phase 4bm-O branch quality gates already passed at the prior phase:
  - Phase 4bm-O surface `ruff check` **PASS** ("All checks passed!").
  - Targeted `pytest tests/research/microstructure/test_labels_*_v002.py` **91 / 91 passed**.
  - Whole-microstructure `pytest tests/research/microstructure/` **1623 passed, 1 skipped**.
  - Static no-network / no-credential scan over 4 source modules + the orchestrator script **PASS**.
- Known baseline remains unchanged on `main` and is unrelated to label / feature surfaces:
  - `mypy src/prometheus` baseline from Phase 4bm-H / Phase 4bm-O documentation (29 errors in 5 files).
  - whole-repo `pytest` blocked by 15 pre-existing collection errors (missing `httpx` / `duckdb`) + 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py`.

Rerunning these tools at the merge phase would yield identical output to the Phase 4bm-O / Phase 4bm-P recorded baselines and add no audit value.

## 20. Boundaries preserved

- **No tracked `data/microstructure/` artefact changed** by Phase 4bm-P or by this merge. The diff between `main` pre-merge (`75371ff`) and `main` post-merge (`78b3db3`) is exactly the three tracked docs files in §9; no other path appears.
- **No generated label artefact was committed.** All 182 inspected label artefacts remain gitignored under `.gitignore:85`.
- **No label artefact was modified.** All 90 per-day label Parquets, all 90 paired sidecars, the v002 label manifest, and the v002 label manifest sidecar are byte-identical pre/post QA (manifest SHA `5e17074d…` recomputed equal).
- **No feature artefact was modified.** The v002 feature manifest (`512a0a54…`), the v002 feature manifest sidecar (`22e2fb77…`), the 90 per-day feature Parquets, and the 90 per-day feature sidecars are byte-identical pre/post QA.
- **No upstream artefact was mutated.** The Phase 4bm-J gate report + sidecar, Phase 4bm-L successor-state JSON + sidecar, v002 derived/normalized manifest + sidecar, v002 raw manifest, and Phase 4bm-F / Phase 4bm-D derived governance artefacts are byte-identical pre/post QA.
- **No label gate report was created.** No file exists under `data/microstructure/gate-reports/labels/` as a result of Phase 4bm-P.
- **No label successor-state JSON was created.** No file with `phase-4bm-p` in its name exists under `data/microstructure/successor-state/`.
- **No chronological split-policy artefact was created.** No file with `chronological_split_policy` semantics was written or committed.
- **v002 feature manifest unchanged** and still carries `research_eligible = false` / `eligibility_gate_status = "pending"` / `stage_4_feature_cleared = false`.
- **v002 derived/normalized manifest unchanged** and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`.
- **v002 raw manifest unchanged** and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`.
- **v002 label manifest unchanged** and still carries `research_eligible = false` / `eligibility_gate_status = "pending"` / `label_family_research_use_authorized = false` / `stage_5_label_cleared = false` / `chronological_split_policy = "not_yet_defined"`.
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved end-to-end** (never invoked by Phase 4bm-P or by this merge).
- **No diagnostics / ML / strategy / backtest / acquisition work was authorized or performed.**
- **No `data/microstructure/` file was committed** by Phase 4bm-P or by this merge.

All retained verdicts and project locks are preserved verbatim:

H0 — FRAMEWORK ANCHOR; R3 — BASELINE-OF-RECORD; R1a / R1b-narrow — RETAINED — NON-LEADING; R2 — FAILED — §11.6; F1 — HARD REJECT; D1-A — MECHANISM PASS / FRAMEWORK FAIL; 5m thread — OPERATIONALLY CLOSED (Phase 3t); V2 / G1 / C1 — HARD REJECT — terminal for first-spec; §11.6 = 8 bps per side / round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant (preserved; never invoked); Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard; Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..F / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L / 4bm-M / 4bm-N / 4bm-O results — all preserved verbatim.

## 21. Recommended state

**Remain paused.**

Phase 4bm-P is now project-complete (this merge-closeout + the immediately-following SHA-finalization commit). The v002 multi-day label family carries a complete evidence ladder through **v002 Label Stage-3 (label artefacts structurally QA-passed)**:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3: Phase 4bm-F derived-family successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts.
- v002 Feature Stage-3: Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`.
- v002 Feature Stage-4: Phase 4bm-J 50/50 `FEATURE_GATE_PASS`.
- v002 Feature Stage-5-decision: Phase 4bm-K Outcome 1 / Decision form 1.
- v002 Feature Stage-5-marker: Phase 4bm-L SHA `7eccaa8f…`.
- v002 Label Stage-0: Phase 4bm-M label-family boundary / design.
- v002 Label Stage-1: Phase 4bm-N label schema finalization.
- v002 Label Stage-2: Phase 4bm-O label kernel implemented + local label artefacts generated.
- **v002 Label Stage-3: Phase 4bm-P label artefacts structurally QA-passed.**

v002 Label Stage-4 (eligibility-gate-passed), Stage-5 (research-use-cleared at policy level), Stage-6 (label-family successor-state JSON), Stage-7 (chronological-split-policy decided), and Stage-8 (`stage_5_label_cleared = true` on the manifest) remain **unauthorized**.

## 22. Conditional next options, none authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | n/a | **recommended** |
| **Conditional next** — future **Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution** (multi-day analogue of Phase 4bj-E) | code + docs + local gitignored gate report | **NOT authorized by this merge-closeout** |
| **Conditional after Phase 4bm-Q** — future v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized** |
| **Conditional after the v002 label-family research-use decision** — future v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state JSON | **NOT authorized** |
| **Conditional later** — future multi-day v002 chronological-split-policy memo + successor-state recording (multi-day analogues of Phase 4bj-H / Phase 4bj-I / Phase 4bj-J) | docs (+ optionally local gitignored sibling artefact) | **NOT authorized** |
| Additional acquisition (more days, cross-symbol, mark-price, order-book, funding, OI, liquidation, cross-venue, authenticated APIs, private endpoints) | docs + data | **NOT authorized** |
| Diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN** |

## 23. Explicit non-authorization

Phase 4bm-P and this merge-closeout do **not**, and **cannot**, authorize:

- **Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution**;
- multi-day v002 label-family eligibility gate;
- multi-day v002 label-family research-use decision;
- multi-day v002 label-family successor-state recording;
- multi-day v002 chronological-split-policy memo;
- multi-day v002 chronological-split-policy successor-state recording;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
- additional acquisition (more days, cross-symbol, mark-price, order-book, funding, OI, liquidation, cross-venue, authenticated APIs, private endpoints);
- Phase 5;
- Phase 4 canonical;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- user-stream / live WebSocket implementation;
- public-endpoint calls in code;
- MCP / Graphify / `.mcp.json` / credentials;
- any mutation of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` / `stage_5_label_cleared` / `label_family_research_use_authorized` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- any successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

**Reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 honored by this merge-closeout**: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION** (no normalization / derivation / feature recomputation / label computation occurred — QA inspected existing artefacts read-only; merge only brought forward tracked docs files), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

---

**Final reminders, recorded verbatim:**

- **Phase 4bm-P is read-only label artefact structural QA.**
- **No label artefact is modified by Phase 4bm-P.**
- **No label artefact is committed by Phase 4bm-P.**
- **Phase 4bm-Q is not authorized by Phase 4bm-P.**
- **Label-family eligibility gate is not authorized by Phase 4bm-P.**
- **Label-family research-use is not authorized by Phase 4bm-P.**
- **Label-family successor-state recording is not authorized by Phase 4bm-P.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-P.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

**Structural QA verdict: LABEL_STRUCTURAL_QA_PASS — label artefact remains not research-eligible.**

**Recommended state: remain paused.**
