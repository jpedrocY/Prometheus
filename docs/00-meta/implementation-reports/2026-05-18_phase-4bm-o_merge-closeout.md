# Phase 4bm-O Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-O — Multi-Day V002 Label Kernel Implementation + Local Label Artefact Generation
- **Tier**: **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules ("any phase that creates features / labels / diagnostics" requires Tier 1, period). Phase 4bm-O is the first multi-day v002 label implementation (code + tests + docs + local gitignored label artefacts).
- **Type**: code + tests + docs + local gitignored label artefacts — adds four new offline source modules under `src/prometheus/research/microstructure/`, one new orchestrator script under `scripts/`, six new test files (one shared fixture helper + five test modules) under `tests/research/microstructure/`, two new docs files under `docs/00-meta/implementation-reports/`, narrowly modifies `src/prometheus/research/microstructure/__init__.py` for Phase 4bm-O re-exports, and narrowly updates `docs/00-meta/current-project-state.md`. **No** `data/microstructure/` artefact is committed; all label outputs (90 v002 label Parquets + 90 sidecars + 1 v002 label manifest + 1 manifest sidecar = 182 local artefacts) remain gitignored under `.gitignore:85` (`data/microstructure/`).
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-O as project-complete on `main` after a clean code + tests + docs + local gitignored label artefact branch that implements the Phase 4bm-N-locked 40-column v002 label schema verbatim and runs the kernel exactly once over the locked 90-day v002 envelope (`microstructure_labels_aggtrades_v001` at `dataset_version = "v002"`; BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 label rows = 1:1 parity with the Phase 4bm-H v002 feature row count), strictly under the Phase 4bm-N label-schema finalization memo and the v001 Phase 4bj-C precedent. Phase 4bm-O reaches **v002 Label Stage-2** (kernel implemented + local gitignored label artefacts generated; not yet QA'd; not yet gate-passed; not yet research-use-cleared; not yet successor-state-marked; chronological-split-policy still `"not_yet_defined"`).
- **Branch merged**: `phase-4bm-o/multi-day-v002-label-kernel-local-artefacts`
- **Target branch**: `main`
- **Base**: `main` at `e2574c4ad6497686b974c39bfb351880e38fb0dd` (Phase 4bm-N merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-N (Multi-Day V002 Label Schema Finalization Memo; project-complete on `main`)
- **Direct v001 precedent**: Phase 4bj-A (v001 label-family boundary / design memo) + Phase 4bj-B (v001 label schema finalization memo) + Phase 4bj-C (v001 label kernel implementation + local gitignored label artefact generation, single day 2025-01-15)

**Phase 4bm-O implements the Phase 4bm-N label schema and generates local gitignored label artefacts only.** **No label artefact is committed by Phase 4bm-O.** **Phase 4bm-P is not authorized by Phase 4bm-O.** **Label artefact structural QA is not authorized by Phase 4bm-O.** **Label-family eligibility gate is not authorized by Phase 4bm-O.** **Label-family research-use is not authorized by Phase 4bm-O.** **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-O.** **No feature artefact was modified.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-O is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `e2574c4ad6497686b974c39bfb351880e38fb0dd`
- **Pre-merge `origin/main` SHA**: `e2574c4ad6497686b974c39bfb351880e38fb0dd` (in sync; verified via `git rev-parse`)
- **Phase 4bm-O branch commit 1 SHA**: `252f7ce5dd494097c0ee42c7213579ba5823e30e` (`feat(phase-4bm-o): implement multi-day v002 label kernel`; 12 files / +4,229; source modules + tests + script + `__init__.py` re-export)
- **Phase 4bm-O branch commit 2 SHA**: `99c0dec9db50412214b0a684905cd906a1501c2a` (`docs(phase-4bm-o): add label artefact report and closeout`; 3 files / +1,209; implementation report + closeout + `current-project-state.md` narrative paragraph and Current phase block update)
- **Phase 4bm-O branch tip SHA pre-merge**: `99c0dec9db50412214b0a684905cd906a1501c2a`
- **Merge commit SHA**: `a6d31cc2eda87b6245e617a895b80f4315a8eb4c`
- **Merge commit message**: `feat(phase-4bm-o): merge multi-day v002 label kernel local artefacts`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `a6d31cc2eda87b6245e617a895b80f4315a8eb4c`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `a6d31cc2eda87b6245e617a895b80f4315a8eb4c` (in sync; pushed cleanly via `e2574c4..a6d31cc  main -> main`; no force, no skip-hooks, no skip-signing)
- **Merge-closeout commit SHA**: recorded by the SHA-finalization patch (`docs(phase-4bm-o): finalize merge closeout shas`) immediately after this file is first committed and pushed; written in §2 of this file by that patch
- **Post-merge-closeout-commit `main` SHA**: recorded by the SHA-finalization patch
- **Post-merge-closeout-commit `origin/main` SHA**: recorded by the SHA-finalization patch
- **Final `main == origin/main` after closeout push**: recorded by the SHA-finalization patch; the subsequent SHA-finalization commit then advances `main` and `origin/main` together by one additional commit, recorded in the final operator report

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-o/multi-day-v002-label-kernel-local-artefacts -m "feat(phase-4bm-o): merge multi-day v002 label kernel local artefacts ..."`
- **Strategy**: `ort` (git default)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     e2574c4..a6d31cc  main -> main
  ```
  Second push (this merge-closeout commit) output: recorded by the SHA-finalization patch.

## §4 Files Brought Forward by the Merge

Fifteen tracked files brought forward from the Phase 4bm-O branch into `main`, spread across the two source-branch commits (`252f7ce` code+tests, `99c0dec` docs).

**Tracked source / script / test files added (11):**

1. `src/prometheus/research/microstructure/labels_schema_v002.py` (NEW, +394; the 40-column v002 label schema, horizon constants `("1s", "5s", "15s", "60s")` / `(1000, 5000, 15000, 60000)`, lineage column tuple of 17, label name tuple of 8, support column tuple of 14, `LABEL_SCHEMA_V002` 40-column canonical order, identity / version constants for the four upstream lineage families, 21-token forbidden-substring detector list verbatim from Phase 4bm-N §27, five locked policy descriptors (`ANCHOR_POLICY_V002`, `FUTURE_REFERENCE_POLICY_V002`, `DIRECTION_THRESHOLD_POLICY_V002`, `NULL_CENSORING_POLICY_V002`, `DTYPE_POLICY_V002`), `build_label_config_hash_v002` (canonical-JSON sorted-key SHA256 over the schema-locking fields named in Phase 4bm-N §25 plus the six v002 upstream lineage SHAs and `feature_config_hash`), `LabelSchemaErrorV002`, `assert_no_forbidden_label_substrings_v002`).
2. `src/prometheus/research/microstructure/labels_io_v002.py` (NEW, +125; v002 path helpers: `derive_v002_label_parquet_path`, `derive_v002_label_manifest_path`, `compose_canonical_sidecar_v002_label`, `V002_LABEL_DIR_SEGMENT`, `V002_LABEL_MANIFEST_BASENAME`; the v001 `labels_io` atomic Parquet / manifest writers and sidecar writer are reused verbatim; path discipline asserts that all outputs resolve under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/` or `data/microstructure/manifests/`).
3. `src/prometheus/research/microstructure/labels_compute_v002.py` (NEW, +475; the v002 multi-day label computation kernel `compute_aggtrade_labels_v002_for_day`, `LabelLineageV002`, `LabelComputationSummaryV002`, `LabelMultiDaySummaryV002`, `NormalizedDayRef`, `LabelComputationErrorV002`, `load_normalized_day_ref`, `write_label_dataset_v002`; per-day kernel with cross-day reference resolution into the immediately following day's normalized parquet bounded by `envelope_terminal_unix_ms`; vectorised `np.searchsorted(side='right') - 1` for both current-day and next-day reference candidates; `Decimal`-parsed prices with `Decimal` ratio and `float64` cast only at the natural-log step; strict-sign direction policy `{+1, 0, -1, null}`; defensive `label_invalid_price_flag = true` on any anchor or reference price ≤ 0; envelope-terminal censoring per horizon when `target_timestamp_ms > envelope_terminal_unix_ms`; no NaN / no inf in output; refuse-to-overwrite at the writer level).
4. `src/prometheus/research/microstructure/labels_manifest_v002.py` (NEW, +366; `build_label_manifest_v002`, `LabelManifestErrorV002`, required-keys constants `REQUIRED_LABEL_GOVERNANCE_KEYS_V002`, `REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002`, `FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002`; manifest defaults `research_eligible = false`, `eligibility_gate_status = "pending"`, `label_family_research_use_authorized = false`, `stage_5_label_cleared = false`, `chronological_split_policy = "not_yet_defined"`, all 10 governance keys locked, all 17 boundary confirmations true; carries all 16 upstream lineage SHAs verbatim).
5. `scripts/phase4bm_o_compute_multiday_labels.py` (NEW, +585; the standalone offline orchestrator that verifies all 14 locked precondition SHAs pre-write, refuses to overwrite any target output, computes `envelope_terminal_unix_ms` from the v002 derived multi-day index manifest's `per_file_inventory[].last_transact_time_ms`, runs the v002 label kernel day-by-day with rolling current-day / next-day normalized reference, writes per-day label Parquets + canonical Phase 4bb-F sidecars atomically, builds and writes the multi-day label manifest + canonical sidecar, then re-hashes all 194 upstream artefacts (14 governance + 90 v002 feature parquets + 90 v002 normalized parquets) to confirm byte-identical immutability).
6. `tests/research/microstructure/_labels_fixtures_v002.py` (NEW, +132; v002 label fixture helper that produces tiny synthetic 19-column normalized aggTrades Parquets and 4-column feature tables suitable for offline label unit tests; never reads or writes under the real `data/microstructure/` namespace).
7. `tests/research/microstructure/test_labels_schema_v002.py` (NEW, +252; 17 tests: identity / horizon / column constants; canonical 40-column order; uniqueness; forbidden-substring list verbatim; detector flags all bad columns; `label_config_hash` determinism; per-input field sensitivity; rejects non-hex; canonical-JSON payload composition; v001 ≠ v002 hash collision).
8. `tests/research/microstructure/test_labels_io_v002.py` (NEW, +113; 12 tests: v002 dir segment / manifest basename constants; derived paths; root-must-end-in-`labels` enforcement; rejects bad symbol / bad date / wrong root / short SHA / uppercase SHA / basename newline; canonical Phase 4bb-F two-space sidecar format; LF only).
9. `tests/research/microstructure/test_labels_compute_v002.py` (NEW, +572; 18 tests: smoke; anchor alignment + lineage propagation; envelope-terminal censoring; target == envelope OK if row exists; same-timestamp tie-break (largest local row_index); cross-day reference into next day; cross-day picks largest next-day row; cross-day target-beyond-envelope censors; strict-sign direction; Decimal-into-float64 formula; invalid anchor price; no NaN/inf; row-alignment mismatch fails; atomic write + canonical sidecar; refuse-to-overwrite; `load_normalized_day_ref` round-trip + rejects missing file; horizon ms locked).
10. `tests/research/microstructure/test_labels_manifest_v002.py` (NEW, +263; 18 tests: required top-level fields; governance defaults locked; boundary confirmations all true; schema introspection (column count, label list, support list, lineage list, schema column list, horizons); per_day_outputs validated; rejects lower-case / non-BTCUSDT symbol / bad date / negative counts / per-day length mismatch / bad censored keys / short SHA / overriding locked governance key; extras allowed when unique; censored / invalid-price round-trip).
11. `tests/research/microstructure/test_labels_no_network_v002.py` (NEW, +173; 21 tests: static no-network / no-credential / no-MCP scan over the 4 new v002 source modules plus the Phase 4bm-O orchestrator script; forbidden import patterns enforced; case-sensitive forbidden token scan after stripping docstrings + comments; no `os.environ` / `os.getenv`; no `.env` / `.mcp.json` files in package).

**Tracked source files modified narrowly (1):**

12. `src/prometheus/research/microstructure/__init__.py` (MODIFIED, +115; re-exports the Phase 4bm-O v002 label public API symbols — sorted into the existing alphabetical-by-section convention; no removal of any existing v001 / v002-feature symbol).

**Tracked docs files added (2):**

13. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_multi-day-v002-label-kernel-local-artefacts.md` (NEW, +416; the 30-section main implementation report).
14. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_closeout.md` (NEW, +264; the 21-section closeout).

**Tracked docs files modified narrowly (1):**

15. `docs/00-meta/current-project-state.md` (MODIFIED, +529; new Phase 4bm-O narrative paragraph appended before the Phase 4bm-N paragraph + new "Current phase:" block + preserved labelled historical Phase 4bm-N "Current phase:" block; prior Phase 4bm-N content preserved verbatim as historical context).

**No `data/microstructure/` artefact is committed by this merge.** No source / test / script / configuration file outside the above 15-file set is modified. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), and every other tracked file outside the above list are unchanged.

## §5 Diff Summary

`git diff --stat e2574c4..a6d31cc` (against pre-merge `main`):

```text
 docs/00-meta/current-project-state.md              |  529 ++++++++
 .../2026-05-18_phase-4bm-o_closeout.md             |  264 ++++
 ...y-v002-label-kernel-local-artefacts.md          |  416 +++++++
 scripts/phase4bm_o_compute_multiday_labels.py      |  585 ++++++++
 src/prometheus/research/microstructure/__init__.py |  115 ++
 .../microstructure/labels_compute_v002.py          |  475 ++++++++
 .../research/microstructure/labels_io_v002.py      |  125 ++
 .../microstructure/labels_manifest_v002.py         |  366 +++++
 .../research/microstructure/labels_schema_v002.py  |  394 ++++++
 .../microstructure/_labels_fixtures_v002.py        |  132 ++
 .../microstructure/test_labels_compute_v002.py     |  572 +++++++++
 .../microstructure/test_labels_io_v002.py          |  113 ++
 .../microstructure/test_labels_manifest_v002.py    |  263 ++++
 .../microstructure/test_labels_no_network_v002.py  |  173 +++
 .../microstructure/test_labels_schema_v002.py      |  261 ++++
 15 files changed, 5438 insertions(+)
```

No deletions. No `data/microstructure/` path appears. `git diff --check` produces no whitespace or conflict marker findings.

## §6 Result / Verdict

**Phase 4bm-O is project-complete on `main`.** The v002 multi-day derived / feature / label-design / label-data family now carries a complete Phase 4ba 5-stage ladder of evidence through Stage-3 (derived family) + a complete v002 **Feature Stage-2..5** chain + a complete v002 **Label Stage-0..2** chain:

- Stage-0 (derived): Phase 4bm-B normalization (90 per-day Parquets + 90 sidecars + v002 multi-day index manifest; gitignored).
- Stage-1 (derived): Phase 4bm-C 56/56 multi-day structural QA PASS.
- Stage-2 (derived): Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision (derived): Phase 4bm-E Option B / Decision form 2.
- Stage-3 (derived): Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts (155,153,449 rows; 62 columns; gitignored).
- v002 Feature Stage-3: Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`.
- v002 Feature Stage-4: Phase 4bm-J `FEATURE_GATE_PASS` (50 / 50; 0 FAIL).
- v002 Feature Stage-5 decision: Phase 4bm-K Outcome 1 / Decision form 1 (policy-level admissibility).
- v002 Feature Stage-5 successor-state marker: Phase 4bm-L successor-state JSON SHA `7eccaa8f…`.
- v002 Label Stage-0: Phase 4bm-M label-family boundary / design memo.
- v002 Label Stage-1: Phase 4bm-N label schema finalization memo.
- v002 **Label Stage-2**: Phase 4bm-O (this phase) — 90 v002 label Parquets + 90 canonical sidecars + 1 v002 label manifest + 1 manifest sidecar; all local gitignored; aggregate row count 155,153,449.

v002 Label Stages 3 and beyond (structural QA / eligibility-gate / research-use / successor-state / chronological-split-policy), v002 Feature Stage-6 and beyond, and Stage-4 feature-cleared on the actual on-disk manifest remain **unauthorized**. The recommended state is **remain paused**.

## §7 Local Gitignored Outputs

Phase 4bm-O produced **182 local gitignored artefacts**, all under `data/microstructure/` and all covered by `.gitignore:85` (`data/microstructure/`). **None are committed.**

- **v002 label parquet root**: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet`
- **v002 label parquet count**: 90 (one per UTC date 2024-12-01 .. 2025-02-28 inclusive)
- **v002 label sidecar count**: 90 (one per parquet, canonical Phase 4bb-F format)
- **v002 label parquet aggregate bytes**: 6,145,349,264 bytes (≈ 5.72 GiB across 90 per-day Parquets)
- **v002 label manifest path**: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`
- **v002 label manifest SHA256**: `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed`
- **v002 label manifest size**: 84,732 bytes
- **v002 label manifest sidecar path**: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256`
- **v002 label manifest sidecar SHA256**: `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd`
- **v002 label manifest sidecar size**: 114 bytes
- **v002 label manifest sidecar exact content** (canonical Phase 4bb-F format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`):
  ```text
  5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed  microstructure_labels_aggtrades_v001__v002.json
  ```
  (64 + 2 + 47 + 1 = 114 bytes; ASCII only; no BOM; LF line ending; exactly two ASCII spaces between SHA and basename; trailing LF.)
- **Total local gitignored artefact count**: 182 (90 parquets + 90 sidecars + 1 manifest + 1 manifest sidecar)

Confirmation: `git check-ignore -v data/microstructure/`, `data/microstructure/labels/`, `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/`, `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`, and `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` all return `.gitignore:85:data/microstructure/`.

## §8 Label Artefact Summary

- **label_config_hash**: `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` (deterministic SHA256 over canonical-JSON of all Phase 4bm-N §25 schema-locking fields + the six v002 upstream lineage SHAs + `feature_config_hash`; constant across all 155,153,449 label parquet rows; equal to `label_manifest.label_config_hash`)
- **row_count**: 155,153,449 (1:1 parity with the Phase 4bm-H v002 feature row count exactly; per-day parity verified for every one of the 90 days)
- **column_count**: 40 (canonical Phase 4bm-N §14 order: 17 lineage / identity / metadata + 1 `label_config_hash` + 4 regression `forward_log_return_<horizon>` + 4 classification `forward_direction_<horizon>` + 12 per-horizon support + 2 global support)
- **date_count**: 90 (contiguous UTC dates 2024-12-01 .. 2025-02-28 inclusive)
- **horizons (`horizon_list`)**: `["1s", "5s", "15s", "60s"]`
- **horizon_ms_list**: `[1000, 5000, 15000, 60000]`
- **envelope_terminal_unix_ms**: `1740787199996` (= 2025-02-28T23:59:59.996Z; the maximum `source_transact_time_ms` across the 90-day v002 envelope, computed deterministically from the v002 derived multi-day index manifest's `per_file_inventory[].last_transact_time_ms`)
- **censored_per_horizon**: `{"1s": 14, "5s": 39, "15s": 170, "60s": 634}` (all 857 envelope-terminal censorings fall on day 90 `2025-02-28`)
- **invalid_price_row_count**: 0 (matches the Phase 4bl-D-R + Phase 4bm-D upstream PASS evidence — no invalid prices anywhere; the defensive `label_invalid_price_flag = true` branch in `labels_compute_v002` was never taken)
- **first day**: 2024-12-01, row_count 731,065
- **last day**: 2025-02-28, row_count 4,526,219 (envelope-terminal day; contributes all 857 envelope-terminal censorings)
- **min row count day**: 2025-02-15, row_count 451,314
- **max row count day**: 2025-01-20, row_count 5,435,481

## §9 Schema Summary

- **Total columns**: 40 = 17 lineage / identity / metadata + 1 `label_config_hash` + 8 labels + 14 support
- **Lineage / identity / metadata columns (17)**: `dataset_family` (= `"microstructure_labels_aggtrades_v001"`), `dataset_version` (= `"v002"`), `label_schema_version` (= `"v001"`), `source_feature_dataset_family` (= `"microstructure_features_aggtrades_v001"`), `source_feature_dataset_version` (= `"v002"`), `source_feature_manifest_sha256`, `source_feature_parquet_sha256` (per-day-constant), `source_feature_successor_state_sha256` (Phase 4bm-L), `source_phase_4bm_j_gate_report_sha256`, `source_normalized_manifest_sha256`, `source_raw_manifest_sha256` (v002-new vs v001), `symbol` (= `"BTCUSDT"`), `utc_date`, `row_index`, `agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`.
- **Label config hash column (1)**: `label_config_hash`.
- **Regression label columns (4)**: `forward_log_return_1s`, `forward_log_return_5s`, `forward_log_return_15s`, `forward_log_return_60s` (nullable float64).
- **Classification label columns (4)**: `forward_direction_1s`, `forward_direction_5s`, `forward_direction_15s`, `forward_direction_60s` (nullable int8 in `{-1, 0, 1, null}`).
- **Per-horizon support columns (12 = 4 × 3)**: for each horizon `H ∈ {1s, 5s, 15s, 60s}`: `reference_row_index_H` (nullable int64), `reference_timestamp_ms_H` (nullable int64 UTC ms), `horizon_censored_flag_H` (non-nullable bool).
- **Global support columns (2)**: `label_invalid_price_flag`, `label_any_censored_flag` (both non-nullable bool).
- **Formula**: `forward_log_return_H = ln(reference_trade_price_H / anchor_trade_price)` (natural log; Decimal-as-string parsed exactly, cast to float64 only at the log step; no NaN, no inf).
- **Direction policy**: `+1` if `forward_log_return_H > 0`; `0` if `forward_log_return_H == 0`; `-1` if `forward_log_return_H < 0`; `null` if `forward_log_return_H` is null. Strict sign threshold at `0.0` log-return; no dead-band; no bp threshold; no threshold optimization.
- **Censoring policy**: envelope-terminal only — `horizon_censored_flag_H = true` iff `feature_timestamp_ms + horizon_ms_H > envelope_terminal_unix_ms` (= 1,740,787,199,996 ms = 2025-02-28T23:59:59.996Z). No per-day censoring is performed; horizons may cross UTC day boundaries inside the v002 90-day envelope (the kernel resolves the reference into the immediately-following day when the target lands past the current day's last `transact_time_ms`).
- **Reference-row tie-break**: same-timestamp tie-break is the largest `row_index` at that timestamp inside its per-day source parquet; this is automatically handled by `np.searchsorted(side='right') - 1` over each per-day normalized parquet's `transact_time_ms` array (the per-day normalized parquet has `row_index == np.arange(n)` and is sorted by `(transact_time_ms ASC, row_index ASC)` per the Phase 4bm-B normalization contract).
- **Output directory tree (v002-suffixed)**: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet`. The `__v002` directory suffix mirrors the v002 normalized and v002 feature directory layouts (Phase 4bm-B / Phase 4bm-H) and preserves the refuse-to-overwrite invariant against the prior v001 Phase 4bj-C single-day label parquet at the unsuffixed `microstructure_labels_aggtrades_v001/...` path (which remains byte-identical).
- **Forbidden-substring detector compliance**: the Phase 4bm-N §27 21-token list (`pnl, profit, loss, mfe, mae, r_multiple, equity, position, alpha, edge, prediction, model, score, decision, strategy, entry, exit, signal, target, barrier, liquidation`) is applied to the v002 label schema at import time and at compute-build time and passes.

## §10 Validation Results

**Phase 4bm-O surface ruff (12 paths)**:

```text
ruff check src/prometheus/research/microstructure/labels_schema_v002.py \
           src/prometheus/research/microstructure/labels_io_v002.py \
           src/prometheus/research/microstructure/labels_compute_v002.py \
           src/prometheus/research/microstructure/labels_manifest_v002.py \
           src/prometheus/research/microstructure/__init__.py \
           scripts/phase4bm_o_compute_multiday_labels.py \
           tests/research/microstructure/_labels_fixtures_v002.py \
           tests/research/microstructure/test_labels_schema_v002.py \
           tests/research/microstructure/test_labels_io_v002.py \
           tests/research/microstructure/test_labels_compute_v002.py \
           tests/research/microstructure/test_labels_manifest_v002.py \
           tests/research/microstructure/test_labels_no_network_v002.py
```

Result: **All checks passed!**

**Targeted v002 label pytest**:

```text
pytest tests/research/microstructure/test_labels_schema_v002.py \
       tests/research/microstructure/test_labels_io_v002.py \
       tests/research/microstructure/test_labels_compute_v002.py \
       tests/research/microstructure/test_labels_manifest_v002.py \
       tests/research/microstructure/test_labels_no_network_v002.py
```

Result: **91 / 91 passed**.

**Microstructure pytest**:

```text
pytest tests/research/microstructure/
```

Result: **1623 passed, 1 skipped in 21.31s** (91 new Phase 4bm-O tests all PASS; 1 pre-existing skipped test preserved as baseline; zero regression vs Phase 4bm-H / Phase 4bm-J / Phase 4bm-N baselines).

**Static no-network / no-credential scan**:

The Phase 4bm-O `test_labels_no_network_v002.py` module's 21 tests cover the case-sensitive forbidden-token scan and the forbidden-import enforcement across the 4 new v002 source modules + the orchestrator script. **All PASS** as part of the targeted v002 label pytest above.

**Git checks**:

- `git diff --check main..phase-4bm-o/...`: clean (no whitespace, no conflict markers).
- `git diff --check` post-merge on `main`: clean (no whitespace, no conflict markers).
- `git status --short` after merge: only the two expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); no tracked changes; no `data/microstructure/` artefact visible (gitignored).
- `git check-ignore -v` on all four v002 label output paths: returns `.gitignore:85: data/microstructure/`.

**mypy (skipped at merge time; Phase 4bm-H baseline cited)**:

Per the Phase 4bm-H precedent (and Phase 4bm-N skip rationale), `mypy src/prometheus` was not invoked at Phase 4bm-O merge time. The documented Phase 4bm-H baseline is **29 errors in 5 files** (`features_compute.py` 8 + `features_compute_v002.py` 8 + `labels_compute.py` 1 + `binance_rest.py` 1 + `binance_bulk.py` 1 + 1 note; 28 pre-existing v001 + 1 v002 mirror error). The new Phase 4bm-O `labels_compute_v002.py` mirrors the v001 `labels_compute.py` `np.searchsorted` + Decimal idiom; it is expected to contribute the same baseline pattern (≤ 1 additional error of the same category as the v001 `labels_compute.py` baseline). No new mypy error category is introduced by Phase 4bm-O. A future Phase 4bm-O successor / merge-related phase may rerun mypy if the operator explicitly requests it.

**Whole-repo pytest (skipped at merge time; baseline known)**:

The Phase 4bm-O branch implementation report (§22 / §24) documents that whole-repo pytest is blocked by two pre-existing baseline issues:

- 15 collection errors caused by missing `httpx` / `duckdb` modules in this Python environment (`tests/integration/test_binance_bulk_end_to_end.py`, `tests/integration/test_fixture_pipeline_end_to_end.py`, `tests/simulation/test_backtest_real_2026_03.py`, and 12 modules under `tests/unit/research/data/`).
- 2 tests in `tests/unit/research/backtest/test_engine_d1a_dispatch.py` (`test_d1a_runner_scaffold_requires_authorization_flag`, `test_d1a_runner_scaffold_check_imports_ok`) that spawn a subprocess whose `prometheus` import fails (the subprocess Python doesn't have the repo's `src/` on `PYTHONPATH` — an environment baseline, not a regression).

These were re-confirmed on the pre-merge `main` (commit `e2574c4`) during the Phase 4bm-O branch work (the Phase 4bm-O branch and `main` both produce the identical 15 + 2 baseline failures). The merge phase does **not** rerun whole-repo pytest because the targeted `pytest tests/research/microstructure` already proves zero regression in the microstructure surface, and the pre-existing failures are env-baseline (missing modules) not code-baseline. This is consistent with `phase-risk-tiering-standard.md` "Short-form report guidance".

## §11 Upstream Immutability Evidence

All upstream artefacts are byte-identical pre- and post-Phase-4bm-O. Recomputed SHA256 on disk at merge-time matches the expected value byte-for-byte for every entry below.

**v002 feature lineage block (6 artefacts):**

| Artefact | Path | SHA256 | Status |
| --- | --- | --- | --- |
| v002 feature manifest | `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | unchanged |
| v002 feature manifest sidecar | `<...>.json.sha256` | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | unchanged |
| Phase 4bm-L successor-state JSON | `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json` | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | unchanged |
| Phase 4bm-L successor-state sidecar | `<...>.json.sha256` | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` | unchanged |
| Phase 4bm-J gate report | `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json` | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | unchanged |
| Phase 4bm-J gate sidecar | `<...>.json.sha256` | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | unchanged |

**v002 derived / raw lineage block (8 artefacts):**

| Artefact | Path | SHA256 | Status |
| --- | --- | --- | --- |
| v002 derived multi-day index manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| v002 derived manifest sidecar | `<...>.json.sha256` | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| Phase 4bm-F v002 derived-family successor-state | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | unchanged |
| Phase 4bm-D v002 derived gate report | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | unchanged |
| v002 raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |
| v002 acquisition log | `<...>_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged |
| Phase 4bl-D-R raw multi-day PASS gate report | `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged |
| Phase 4bl-E raw multi-day successor-state JSON | `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json` | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged |

**90 per-day v002 feature parquets**: re-hashed by the Phase 4bm-O orchestrator immediately after writing all label outputs; all 90 byte-identical to the SHAs recorded in the v002 feature manifest's `per_day_outputs[].feature_parquet_sha256`.

**90 per-day v002 normalized parquets**: re-hashed by the Phase 4bm-O orchestrator immediately after writing all label outputs; all 90 byte-identical to the SHAs recorded in the v002 derived multi-day index manifest's `per_file_inventory[].parquet_sha256`.

**Total immutability witnesses**: 194 (14 governance + 90 v002 feature parquets + 90 v002 normalized parquets), all byte-identical pre and post the Phase 4bm-O run.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end. It was **never invoked** by Phase 4bm-O.

## §12 Manifest State Preservation

| Manifest | Path | `research_eligible` | `eligibility_gate_status` | `stage_4_feature_cleared` / `stage_5_label_cleared` | `chronological_split_policy` | Status |
| --- | --- | --- | --- | --- | --- | --- |
| v002 feature manifest | `microstructure_features_aggtrades_v001__v002.json` | `false` | `"pending"` | `stage_4_feature_cleared = false` | n/a (not present at this version) | unchanged |
| v002 derived multi-day index manifest | `microstructure_normalized_aggtrades_v001__v002.json` | `false` | `"pending"` | n/a | n/a | unchanged |
| v002 raw manifest | `microstructure_raw_aggtrades_v001__v002.json` | `false` | `"pending"` | n/a | n/a | unchanged |
| v001 derived manifest | `microstructure_normalized_aggtrades_v001__v001.json` | `false` | `"pending"` | n/a | n/a | unchanged |
| v001 label manifest (Phase 4bj-C single-day) | `microstructure_labels_aggtrades_v001__v001.json` | `false` | `"pending"` | n/a | `"not_yet_defined"` | unchanged |
| **NEW** v002 label manifest | `microstructure_labels_aggtrades_v001__v002.json` | `false` | `"pending"` | `stage_5_label_cleared = false` | `"not_yet_defined"` | created (gitignored; NOT committed) |

The new v002 label manifest (gitignored) defaults `research_eligible = false`, `eligibility_gate_status = "pending"`, `label_family_research_use_authorized = false`, `stage_5_label_cleared = false`, `chronological_split_policy = "not_yet_defined"`, all 10 governance label keys locked at their `forbidden` / `unauthorized` / `allowed_by_future_phase_only` values, and all 17 boundary confirmations `true`.

The Phase 4bm-L successor-state JSON's `feature_family_research_use_approved_in_principle = true` continues to be the **only** machine-readable Stage-5 admissibility marker for the v002 feature family. The Phase 4bm-O label manifest cites the Phase 4bm-L successor-state SHA `7eccaa8f…` verbatim as the `source_feature_successor_state_sha256` lineage field and never interprets the v002 feature manifest alone as Stage-5.

## §13 Boundary Statements (Required Exact Phrases)

The following phrases appear verbatim:

- **Phase 4bm-O implements the Phase 4bm-N label schema and generates local gitignored label artefacts only.**
- **No label artefact is committed by Phase 4bm-O.**
- **Phase 4bm-P is not authorized by Phase 4bm-O.**
- **Label artefact structural QA is not authorized by Phase 4bm-O.**
- **Label-family eligibility gate is not authorized by Phase 4bm-O.**
- **Label-family research-use is not authorized by Phase 4bm-O.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-O.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

Additional preserved boundaries:

- no tracked `data/microstructure/` artefact changed by this merge;
- no generated label artefact was committed;
- the original v002 feature manifest is unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"` / `stage_4_feature_cleared = false`;
- the original v002 derived multi-day index manifest is unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- the original v002 raw manifest is unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- the Phase 4bm-L successor-state JSON is unchanged;
- the Phase 4bm-J gate report is unchanged;
- the Phase 4bm-F successor-state JSON is unchanged;
- the Phase 4bm-D gate report is unchanged;
- the v001 Phase 4bj-C single-day label parquet, sidecar, manifest, and manifest sidecar are unchanged;
- no label gate report was created;
- no label successor-state JSON was created;
- no chronological-split-policy artefact was created;
- no diagnostics / ML / strategy / backtest / acquisition work was authorized or performed;
- no endpoint, credential, MCP, Graphify, `.env`, `.mcp.json`, WebSocket, authenticated API, private endpoint, or exchange-write surface was touched.

## §14 Evidence Summary

- **Phase 4bm-N schema finalization**: 40-column v002 label schema locked at memo level on `main` (Phase 4bm-N merge-closeout SHA-finalization commit `e2574c4`).
- **Phase 4bm-L successor-state SHA**: `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (sidecar `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98`); machine-readable v002 Feature Stage-5 research-use admissibility marker.
- **Phase 4bm-K decision**: Outcome 1 / Decision form 1 (equivalent label `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`; SHA-finalization commit `121865a26120d5f097fee95c00185ebd4c995703`).
- **Phase 4bm-J gate verdict**: `FEATURE_GATE_PASS` (`overall_status = pass`; 50 / 50 PASS; 0 FAIL; 0 ERROR; 0 NOT_APPLICABLE; 0 blocking failures); gate report SHA `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`; sidecar `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`.
- **Phase 4bm-I structural QA verdict**: `FEATURE_STRUCTURAL_QA_PASS` (transitively confirmed by Phase 4bm-J check A12 PASS).
- **v002 feature manifest SHA**: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (unchanged).
- **v002 derived multi-day index manifest SHA**: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (unchanged).
- **feature_config_hash**: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`.
- **feature row count**: 155,153,449 (90 days; BTCUSDT; 2024-12-01 .. 2025-02-28 inclusive).
- **feature schema column count**: 62 (17 lineage + 45 feature / quality).
- **date range**: 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days).
- **symbol**: BTCUSDT.

## §15 Boundaries Preserved

All retained verdicts and project locks are preserved verbatim by this merge:

- H0 — FRAMEWORK ANCHOR.
- R3 — BASELINE-OF-RECORD.
- R1a / R1b-narrow — RETAINED — NON-LEADING.
- R2 — FAILED — §11.6.
- F1 — HARD REJECT.
- D1-A — MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread — OPERATIONALLY CLOSED (Phase 3t).
- V2 / G1 / C1 — HARD REJECT — terminal for first-spec.
- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked**).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..F / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L / 4bm-M / 4bm-N results — all preserved verbatim.

v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any further v002 label phase.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST** (the v002 feature / derived / raw manifests remain byte-identical; the new sibling v002 label manifest is gitignored), **N-GATE-RERUN**, **N-SUCCESSOR-STATE** (no successor-state artefact created by Phase 4bm-O), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

**N-DERIVATION** does NOT apply to Phase 4bm-O, because the phase explicitly performs label-kernel computation — its sole authorized scope.

## §16 Recommended State

**Remain paused.**

Phase 4bm-O is project-complete on `main` by this merge + merge-closeout. The operator's broader pause decision continues to apply.

## §17 Conditional Next Options (none authorized)

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | n/a | **recommended** |
| Future **Phase 4bm-P — Multi-Day V002 Label Artefact Structural QA Memo** (multi-day analogue of Phase 4bj-D) | docs-only + analysis | **NOT authorized by this merge** |
| Future v002 label-family eligibility-gate design + implementation + execution (multi-day analogue of Phase 4bj-E) | code + docs + local gitignored gate report | **NOT authorized by this merge** |
| Future v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized by this merge** |
| Future v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state JSON | **NOT authorized by this merge** |
| Future multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I) | docs-only | **NOT authorized by this merge** |
| Future multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J) | docs + local gitignored successor-state JSON | **NOT authorized by this merge** |
| Additional acquisition (more days / cross-symbol / mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated APIs / private endpoints) | docs + data | **NOT authorized by this merge** |
| Diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this merge** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this merge** |

## §18 Explicit Non-Authorization

This merge does **not**, and **cannot**, authorize:

- Phase 4bm-P (canonical successor; the multi-day v002 label artefact structural QA memo);
- v002 label artefact structural QA;
- v002 label-family eligibility-gate design / implementation / execution;
- v002 label-family research-use decision memo;
- v002 label-family successor-state recording;
- multi-day v002 chronological-split-policy memo;
- multi-day v002 chronological-split-policy successor-state recording;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
- additional acquisition (more days, cross-symbol, mark-price, order-book, funding, OI, liquidation, cross-venue, authenticated APIs, private endpoints);
- Phase 5;
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
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` / `stage_5_label_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- any further successor-state JSON creation;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, Phase 4bm-L, Phase 4bm-M, or Phase 4bm-N;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.
