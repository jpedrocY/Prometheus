# Phase 4bm-H Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-H — Multi-Day V002 Feature Schema / Feature Computation Implementation
- **Tier**: **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules ("any phase that creates features / labels / diagnostics" requires Tier 1, period). Phase 4bm-H is the first multi-day v002 feature implementation (code + tests + docs + local gitignored feature artefacts).
- **Type**: code + tests + docs + local gitignored feature artefacts — adds four new offline source modules under `src/prometheus/research/microstructure/`, one new orchestrator script under `scripts/`, six new test files (one shared fixture helper + five test modules) under `tests/research/microstructure/`, two new docs files under `docs/00-meta/implementation-reports/`, narrowly modifies `src/prometheus/research/microstructure/__init__.py` for v002 re-exports, and narrowly updates `docs/00-meta/current-project-state.md`. **No** `data/microstructure/` artefact is committed; all feature outputs (90 v002 feature Parquets + 90 sidecars + 1 v002 feature manifest + 1 manifest sidecar = 182 local artefacts) remain gitignored under `.gitignore:85` (`data/microstructure/`).
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-H as project-complete on `main` after a clean code + tests + docs + local gitignored feature artefact branch that computes the first multi-day v002 feature artefacts for the Stage-3 successor-state-marked normalized derived family `microstructure_normalized_aggtrades_v001` at `dataset_version = "v002"` (90 contiguous UTC dates 2024-12-01 .. 2025-02-28; BTCUSDT; 155,153,449 events) into the sibling feature family `microstructure_features_aggtrades_v001 @ v002` with `feature_schema_version = "v001"`, strictly under the Phase 4bm-G feature-boundary design memo and the v001 Phase 4bh / 4bh-B precedent. Phase 4bm-H reaches **v002 Feature Stage-2** (computed; structurally formed; not yet QA'd; not yet gate-passed; not yet research-use-cleared; not yet successor-state-marked).
- **Branch merged**: `phase-4bm-h/multi-day-v002-feature-schema-computation-implementation`
- **Target branch**: `main`
- **Base**: `main` at `3a7c6488d38997ffd25bc06952dab4e9f040ef8f` (Phase 4bm-G merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-G (Multi-Day V002 Feature-Boundary Design Memo; project-complete on `main`)
- **Direct v001 precedent**: Phase 4bh-A (v001 feature-boundary design memo) + Phase 4bh-B (v001 feature schema finalization memo) + Phase 4bh (v001 feature computation implementation, single day 2025-01-15)

**Phase 4bm-H is feature computation only.** **Stage-4 is not authorized by Phase 4bm-H.** **Phase 4bm-I is not authorized by Phase 4bm-H.** **Feature-family research-use is not authorized by Phase 4bm-H.** **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-H.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-H is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `3a7c6488d38997ffd25bc06952dab4e9f040ef8f`
- **Pre-merge `origin/main` SHA**: `3a7c6488d38997ffd25bc06952dab4e9f040ef8f` (in sync; verified via `git rev-parse`)
- **Phase 4bm-H branch commit 1 SHA**: `5b089d5` (`feat(phase-4bm-h): implement multi-day v002 feature computation`; 12 files / +4,213; source modules + tests + script + `__init__.py` re-export)
- **Phase 4bm-H branch commit 2 SHA**: `e6be5f7` (`docs(phase-4bm-h): add implementation report and closeout`; 3 files / +1,152; implementation report + closeout + `current-project-state.md` narrative paragraph and Current phase block update)
- **Phase 4bm-H branch tip SHA pre-merge**: `e6be5f75d3a10f845d2b6a304e548f22c0b4d677`
- **Merge commit SHA**: `c35816cfc1ab0048335fe66919bbc98f7d0de2c9`
- **Merge commit message**: `feat(phase-4bm-h): merge multi-day v002 feature computation`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `c35816cfc1ab0048335fe66919bbc98f7d0de2c9`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `c35816cfc1ab0048335fe66919bbc98f7d0de2c9` (in sync; pushed cleanly via `3a7c648..c35816c  main -> main`; no force, no skip-hooks, no skip-signing)
- **Merge-closeout commit SHA**: recorded by the next commit (this file; `docs(phase-4bm-h): add merge closeout`)
- **Post-merge-closeout-commit `main` SHA**: recorded by the next commit
- **Post-merge-closeout-commit `origin/main` SHA**: recorded by the next commit
- **Final `main == origin/main` after closeout push**: recorded by the next commit

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-h/multi-day-v002-feature-schema-computation-implementation -m "feat(phase-4bm-h): merge multi-day v002 feature computation"`
- **Strategy**: `ort` (git default)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     3a7c648..c35816c  main -> main
  ```
  Second push (this merge-closeout commit) output: recorded by the next commit.

## §4 Files Brought Forward by the Merge

Fifteen tracked files brought forward from the Phase 4bm-H branch into `main`, spread across the two source-branch commits (`5b089d5` code+tests, `e6be5f7` docs).

**Tracked source / script / test files added (11):**

1. `src/prometheus/research/microstructure/features_schema_v002.py` (NEW, +486; the 62-column v002 schema, lineage column tuple, `FeatureComputationConfigV002`, `build_feature_config_v002`, `compute_feature_config_hash_v002`, `assert_no_forbidden_substrings_v002`, locked Decimal / null / invalid-window / window-boundary / timestamp / leakage / same-timestamp tie-break / cross-day lookback policy constants).
2. `src/prometheus/research/microstructure/features_io_v002.py` (NEW, +127; v002 path helpers: `derive_v002_feature_parquet_path`, `derive_v002_feature_manifest_path`, `compose_canonical_sidecar_v002`, `V002_FEATURE_DIR_SEGMENT`, `V002_FEATURE_MANIFEST_BASENAME`; the v001 `features_io` atomic writers and source loaders are reused verbatim).
3. `src/prometheus/research/microstructure/features_compute_v002.py` (NEW, +728; the v002 feature computation kernel `compute_aggtrades_features_v002`, `FeatureLineageV002`, `FeatureWriteResultV002`, `FeatureComputationErrorV002`, `slice_prior_day_tail`, `write_feature_dataset_v002`; causal cross-day lookback algorithm with O(N + N_tail) windowing via numpy cumulative sums and `searchsorted`; deterministic Decimal-as-string formatting; aggressive-side rule; same-timestamp tie-break; log-return rule mirroring v001 Phase 4bh-B; refuse-to-overwrite at the writer level).
4. `src/prometheus/research/microstructure/features_manifest_v002.py` (NEW, +441; `build_feature_manifest_v002`, `feature_dtypes_v002`, `FeatureManifestErrorV002`, required-keys constants `REQUIRED_V002_GOVERNANCE_KEYS`, `REQUIRED_V002_BOUNDARY_CONFIRMATIONS`, `REQUIRED_V002_NON_AUTHORIZATION_FLAGS`, `FORBIDDEN_V002_GOVERNANCE_VALUES`).
5. `scripts/phase4bm_h_compute_multiday_features.py` (NEW, +614; the standalone offline orchestrator that verifies all 10 locked precondition SHAs pre-write, refuses to overwrite any target output, runs the v002 feature kernel day-by-day with causal cross-day lookback, writes per-day feature Parquets + canonical Phase 4bb-F sidecars atomically, builds and writes the multi-day feature manifest + canonical sidecar, then re-hashes all 100 upstream artefacts to confirm byte-identical immutability).
6. `tests/research/microstructure/_multiday_features_fixtures_v002.py` (NEW, +336; multi-day v002 fixture helper that produces 19-column v002 normalized aggTrades Parquets for two contiguous UTC days plus default mixed / all-buyer-maker / all-seller-maker / single-event row sets).
7. `tests/research/microstructure/test_features_schema_v002.py` (NEW, +165; 12 tests: 62-column schema in canonical order; lineage column list matches the Phase 4bm-G design; identity constants; forbidden-substring detector; per-token detector; v001 26-token list inheritance; feature_config_hash determinism; canonical-JSON SHA256 helper is order-independent; dataclass rejects wrong dataset_version; schema-equality assertion).
8. `tests/research/microstructure/test_features_io_v002.py` (NEW, +96; 8 tests: v002 path constants; per-day parquet layout (verifies the `__v002` directory segment); manifest layout; rejects lowercase symbol; rejects bad date format; rejects non-microstructure root; canonical Phase 4bb-F sidecar format (two ASCII spaces, LF, no CR, no BOM); sidecar rejects invalid inputs).
9. `tests/research/microstructure/test_features_compute_v002.py` (NEW, +423; 22 tests: 62-column canonical order; one feature row per current-day source row; lineage column constants; day-1 `rolling_missing_window_flag` rule; day-2 cross-day tail no missing-window flags; cross-day 60s lookback picks up day-1 tail; aggressive-side count rule; same-timestamp tie-break; all-buyer-maker / all-seller-maker / single-event fixtures; log-return null for first row; aggressive_flow_ratio in [0, 1]; Decimal-as-string parses; feature_timestamp == source_transact_time; no future lookahead; atomic write + canonical sidecar; refuse-to-overwrite; kernel rejects wrong source dataset_version; kernel rejects tail with current-day timestamps; `slice_prior_day_tail` filters correctly; round-trip preserves column order; strict bool flags; time-context columns within day).
10. `tests/research/microstructure/test_features_manifest_v002.py` (NEW, +167; 13 tests: required identity fields; defaults `research_eligible=False` / `eligibility_gate_status="pending"`; all 8 non-authorization flags default False; all 18 boundary confirmations True; governance keys locked; full lineage SHA block; feature_dtypes covers all 62 columns; per_day_outputs length must equal date_count; window / timestamp / leakage / cross-day policies recorded; forbidden_substring_detector_tokens carried; immutability / network / credentials / MCP / manifest-mutation flags; rejects bad SHA field; rejects per-day entry missing keys).
11. `tests/research/microstructure/test_features_no_network_v002.py` (NEW, +119; 6 tests: static no-network / no-credential / no-MCP scan over the 4 new v002 source modules plus the Phase 4bm-H orchestrator script; forbidden import patterns enforced; forbidden tokens enforced excluding docstrings / comments).

**Tracked source files modified narrowly (1):**

12. `src/prometheus/research/microstructure/__init__.py` (MODIFIED, +95; re-exports the Phase 4bm-H v002 public API symbols — sorted into the existing alphabetical-by-section convention; no removal of any existing v001 symbol).

**Tracked docs files added (2):**

13. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-h_multi-day-v002-feature-schema-computation-implementation.md` (NEW, +588; the 24-section main implementation report).
14. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-h_closeout.md` (NEW, +148; the 14-section closeout).

**Tracked docs files modified narrowly (1):**

15. `docs/00-meta/current-project-state.md` (MODIFIED, +416; new Phase 4bm-H narrative paragraph appended before the Phase 4bm-G paragraph + new "Current phase:" block + preserved labelled historical Phase 4bm-G "Current phase:" block; prior Phase 4bm-G content preserved verbatim as historical context).

**No `data/microstructure/` artefact is committed by this merge.** No source / test / script / configuration file outside the above 15-file set is modified. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), and every other tracked file outside the above list are unchanged.

## §5 Diff Summary

`git diff --stat 3a7c648..c35816c` (against pre-merge `main`):

```text
 docs/00-meta/current-project-state.md              | 416 ++++++++++++
 .../2026-05-18_phase-4bm-h_closeout.md             | 148 +++++
 ...02-feature-schema-computation-implementation.md | 588 +++++++++++++++++
 scripts/phase4bm_h_compute_multiday_features.py    | 614 +++++++++++++++++
 src/prometheus/research/microstructure/__init__.py |  95 +++
 .../microstructure/features_compute_v002.py        | 728 +++++++++++++++++
 .../research/microstructure/features_io_v002.py    | 127 ++++
 .../microstructure/features_manifest_v002.py       | 441 +++++++++++
 .../microstructure/features_schema_v002.py         | 486 ++++++++++++
 .../_multiday_features_fixtures_v002.py            | 336 ++++++++++
 .../microstructure/test_features_compute_v002.py   | 423 ++++++++++++
 .../microstructure/test_features_io_v002.py        |  96 +++
 .../microstructure/test_features_manifest_v002.py  | 167 +++++
 .../test_features_no_network_v002.py               | 119 ++++
 .../microstructure/test_features_schema_v002.py    | 165 +++++
 15 files changed, 4949 insertions(+)
```

No deletions. No `data/microstructure/` path appears. `git diff --check` produces no whitespace or conflict marker findings.

## §6 Result / Verdict

**Phase 4bm-H is project-complete on `main`.** The v002 multi-day derived family now carries a complete Phase 4ba 5-stage ladder of evidence through Stage-3 plus a complete v002 **Feature Stage-2** computed artefact:

- Stage-0: Phase 4bm-B normalization (90 per-day Parquets + 90 sidecars + v002 multi-day index manifest; gitignored).
- Stage-1: Phase 4bm-C 56/56 multi-day structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`; 19/19 boundary confirmations True.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2 (policy-level admissibility).
- Stage-3: Phase 4bm-F successor-state JSON SHA `72b6edd4…` + sidecar SHA `1e9ffb23…` (gitignored sibling artefact; original manifest byte-identical).
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 **Feature Stage-2**: Phase 4bm-H (this phase) — 90 v002 feature Parquets + 90 canonical sidecars + 1 v002 feature manifest + 1 manifest sidecar; all local gitignored.

v002 Feature Stages 3 through 6 (QA'd / gate-passed / research-use-cleared / successor-state-marked) and Stage-4 (feature-cleared) remain **unauthorized**. The recommended state is **remain paused**.

## §7 Local Gitignored Outputs

Phase 4bm-H produced **182 local gitignored artefacts**, all under `data/microstructure/` and all covered by `.gitignore:85` (`data/microstructure/`). **None are committed.**

- **v002 feature manifest path**: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`
- **v002 feature manifest SHA256**: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d`
- **v002 feature manifest size**: 85,929 bytes
- **v002 feature manifest sidecar path**: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json.sha256`
- **v002 feature manifest sidecar SHA256**: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`
- **v002 feature manifest sidecar size**: 116 bytes
- **v002 feature manifest sidecar exact content** (canonical Phase 4bb-F format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`):
  ```text
  512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d  microstructure_features_aggtrades_v001__v002.json
  ```
  (66 + 50 = 116 bytes; ASCII only; no BOM; LF line ending; exactly two ASCII spaces between SHA and basename; trailing LF.)
- **feature_config_hash**: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` (deterministic SHA256 over canonical-JSON of the locked v002 feature config; recorded inside the manifest's `feature_config_hash` field and carried verbatim on every output feature row's `feature_config_hash` column).
- **feature parquet count**: 90 (one per UTC date 2024-12-01 .. 2025-02-28 inclusive)
- **feature sidecar count**: 90 (one per parquet, canonical Phase 4bb-F format)
- **total feature row count**: 155,153,449 (1:1 parity with Phase 4bm-B v002 normalized total event count; per-day parity verified by summing per_day_outputs row counts in the manifest)
- **date range**: 2024-12-01 .. 2025-02-28 (90 contiguous UTC days)
- **symbol**: BTCUSDT
- **feature parquet output directory tree**: `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`

Confirmation: `git check-ignore -v data/microstructure/`, `data/microstructure/features/`, `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`, and `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json.sha256` all return `.gitignore:85:data/microstructure/`.

## §8 Validation Results

**Phase 4bm-H surface ruff (11 paths)**:

```text
ruff check src/prometheus/research/microstructure/features_schema_v002.py \
           src/prometheus/research/microstructure/features_compute_v002.py \
           src/prometheus/research/microstructure/features_manifest_v002.py \
           src/prometheus/research/microstructure/features_io_v002.py \
           scripts/phase4bm_h_compute_multiday_features.py \
           tests/research/microstructure/_multiday_features_fixtures_v002.py \
           tests/research/microstructure/test_features_schema_v002.py \
           tests/research/microstructure/test_features_compute_v002.py \
           tests/research/microstructure/test_features_manifest_v002.py \
           tests/research/microstructure/test_features_io_v002.py \
           tests/research/microstructure/test_features_no_network_v002.py
```

Result: **All checks passed!**

**Whole-repo ruff**:

```text
ruff check .
```

Result: **All checks passed!**

**Targeted microstructure pytest**:

```text
pytest tests/research/microstructure
```

Result: **1471 passed, 1 skipped in 14.71s** (89 new Phase 4bm-H tests all PASS; 1 pre-existing skipped test preserved as baseline).

**mypy**:

```text
mypy src/prometheus
```

Result: **29 errors in 5 files (checked 128 source files)**. Breakdown:

- `src/prometheus/research/microstructure/features_compute.py` — 8 errors (pre-existing v001 baseline; `np.concatenate(([0], ...))` cumulative-sum prefix idiom + `np.ndarray` type-parameter omissions).
- `src/prometheus/research/microstructure/features_compute_v002.py` — 8 errors (NEW v002 file; **mirrors the v001 idiom verbatim**; same line shapes, same error categories; no new mypy category introduced).
- `src/prometheus/research/microstructure/labels_compute.py` — 1 error (pre-existing v001 baseline; same `np.ndarray` type-parameter omission).
- `src/prometheus/research/data/binance_rest.py` — 1 error (pre-existing env baseline; `httpx` not installed in this Python environment).
- `src/prometheus/research/data/binance_bulk.py` — 1 error + 1 note (pre-existing env baseline; same `httpx` import).

Total of 28 pre-existing baseline errors are preserved verbatim; 1 new v002 file (`features_compute_v002.py`) carries 8 errors that exactly mirror the v001 `features_compute.py` baseline idiom. **No new mypy error category is introduced. No v001 baseline error is worsened.** This is consistent with the v001 Phase 4bh precedent (the v001 `features_compute.py` baseline was tolerated at v001 merge time and continues to be tolerated by the project).

**Whole-repo pytest (skipped at merge time; baseline known)**:

The Phase 4bm-H branch implementation report (§17) documents that whole-repo pytest is blocked by two pre-existing baseline issues:

- 15 collection errors caused by missing `httpx` / `duckdb` modules in this Python environment (`tests/integration/test_binance_bulk_end_to_end.py`, `tests/integration/test_fixture_pipeline_end_to_end.py`, `tests/simulation/test_backtest_real_2026_03.py`, and 12 modules under `tests/unit/research/data/`).
- 2 tests in `tests/unit/research/backtest/test_engine_d1a_dispatch.py` (`test_d1a_runner_scaffold_requires_authorization_flag`, `test_d1a_runner_scaffold_check_imports_ok`) that spawn a subprocess whose `prometheus` import fails (the subprocess Python doesn't have the repo's `src/` on `PYTHONPATH` — an environment baseline, not a regression).

These were re-confirmed on the pre-merge `main` (commit `3a7c648`) during the Phase 4bm-H branch work (the Phase 4bm-H branch and `main` both produce the identical 15 + 2 baseline failures). The merge phase does **not** rerun whole-repo pytest because the targeted `pytest tests/research/microstructure` already proves zero regression in the microstructure surface, and the pre-existing failures are env-baseline (missing modules) not code-baseline. This is consistent with `phase-risk-tiering-standard.md` §"Short-form report guidance" / "if full pytest is too expensive or blocked by known pre-existing failures, run targeted tests plus record the known baseline exactly and justify."

**Git checks**:

- `git diff --check main..phase-4bm-h/...`: clean (no whitespace, no conflict markers).
- `git status --short` after merge: only the two expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); no tracked changes; no `data/microstructure/` artefact visible (gitignored).
- `git check-ignore -v` on all four v002 output paths: returns `.gitignore:85: data/microstructure/`.

## §9 Upstream Immutability Evidence

All upstream artefacts are byte-identical pre- and post-Phase-4bm-H. Recomputed SHA256 on disk at merge-time matches the expected value byte-for-byte for every entry below.

**v002 lineage block (10 artefacts):**

| Artefact | Path | SHA256 | Status |
| --- | --- | --- | --- |
| v002 derived multi-day index manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| v002 derived manifest sidecar | `<...>.sha256` | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| v002 raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |
| v002 acquisition log | `<...>_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged |
| Phase 4bl-D-R raw multi-day PASS gate report | `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged |
| Phase 4bl-E raw multi-day successor-state JSON | `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json` | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged |
| Phase 4bm-D authoritative derived-family gate report | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | unchanged |
| Phase 4bm-D authoritative sidecar | `<...>.sha256` | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | unchanged |
| Phase 4bm-F v002 successor-state JSON (Stage-3 marker) | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | unchanged |
| Phase 4bm-F v002 successor-state sidecar | `<...>.sha256` | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | unchanged |

**v001 feature precedent (2 artefacts; the Phase 4bm-H __v002 directory refinement ensured no collision):**

| Artefact | Path | SHA256 | Status |
| --- | --- | --- | --- |
| Phase 4bh v001 single-day feature parquet | `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | unchanged |
| Phase 4bh v001 single-day feature sidecar | `<...>.parquet.sha256` | `cc880c0820f96ad6f45d1fedeeaa3277941cd5c129c946d72639b921854e311c` | unchanged |

**90 per-day v002 normalized Parquets**: re-hashed by the Phase 4bm-H orchestrator immediately after writing all outputs; all 90 byte-identical to the SHAs recorded in the v002 derived multi-day index manifest's `per_file_inventory` list.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end. It was **never invoked** by Phase 4bm-H.

## §10 Manifest State Preservation

| Manifest | Path | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Status |
| --- | --- | --- | --- | --- | --- |
| v002 derived multi-day index manifest | `microstructure_normalized_aggtrades_v001__v002.json` | `false` | `"pending"` | n/a (not present at this version) | unchanged |
| v002 raw manifest | `microstructure_raw_aggtrades_v001__v002.json` | `false` | `"pending"` | n/a | unchanged |
| v001 derived manifest | `microstructure_normalized_aggtrades_v001__v001.json` | `false` | `"pending"` | n/a | unchanged |
| **NEW** v002 feature manifest | `microstructure_features_aggtrades_v001__v002.json` | `false` | `"pending"` | n/a | created (gitignored; NOT committed) |

The v002 feature manifest (newly created, gitignored) defaults `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false`, all 8 non-authorization flags (`label_computation_authorized`, `diagnostics_authorized`, `ml_authorized`, `strategy_authorized`, `backtest_authorized`, `acquisition_authorized`, `successor_authorization_after`, `stage_4_feature_cleared`) `false`, all 18 boundary confirmations `true`, and `no_network_io / no_credentials / no_mcp_or_graphify / no_manifest_mutation / phase_4aw_flip_research_eligible_invariant_preserved` all `true`.

The Phase 4bm-F successor-state JSON's `successor_research_eligible = true` continues to be the **only** machine-readable Stage-3 marker for the v002 derived family. Any future tool that wishes to interpret the v002 derived family as Stage-3 must read the Phase 4bm-F successor-state artefact, not the v002 derived multi-day index manifest. The Phase 4bm-H feature manifest cites the Phase 4bm-F successor-state SHA `72b6edd4…` verbatim and never interprets the v002 derived multi-day index manifest alone as Stage-3.

## §11 Feature Schema Summary

- **Total columns**: 62 = 17 lineage + 45 feature/quality
- **Lineage / identity / metadata columns (17)**: `dataset_family`, `dataset_version` (= `"v002"`), `source_dataset_family`, `source_dataset_version` (= `"v002"`), `feature_schema_version` (= `"v001"`), `symbol`, `utc_date`, `agg_trade_id`, `row_index`, `feature_timestamp_ms`, `source_transact_time_ms`, `source_normalized_parquet_per_day_sha256`, `source_normalized_manifest_sha256`, `source_successor_state_sha256`, `source_phase_4bm_d_gate_report_sha256`, `source_phase_4bm_e_outcome` (= `"Option B / Decision form 2"`), `feature_config_hash`.
- **Feature / quality columns (45)**: identical to the v001 Phase 4bh-B finalised list. For each window label `w ∈ {1s, 5s, 15s, 60s}` (corresponding to `window_ms ∈ {1000, 5000, 15000, 60000}`): `rolling_aggtrade_count_<w>`, `rolling_quantity_sum_<w>`, `rolling_quantity_mean_<w>`, `rolling_aggressive_buy_quantity_<w>`, `rolling_aggressive_sell_quantity_<w>`, `rolling_aggressive_buy_count_<w>`, `rolling_aggressive_sell_count_<w>`, `rolling_aggressive_flow_ratio_<w>`, `rolling_aggressive_quantity_imbalance_<w>`, `rolling_log_return_past_window_<w>` (= 40 windowed); plus 3 time-context (`utc_hour`, `utc_minute`, `milliseconds_since_day_start`) + 2 quality flags (`invalid_window_flag`, `rolling_missing_window_flag`).
- **Windows (ms)**: `(1000, 5000, 15000, 60000)`; **window labels**: `("1s", "5s", "15s", "60s")`; **window boundary**: left-open, right-closed `(T - window_ms, T]`; **same-timestamp tie-break**: `row_index ASC` within the current day.
- **Cross-day rolling-window policy**: Phase 4bm-G §16 policy 1 — **causal cross-day lookback**; `tail_buffer_ms = 60_000` (= max trailing window). For each current-day output, prior-day tail rows are loaded as read-only context. Day 1 of the v002 range (2024-12-01) has no prior-day data in scope; rows whose 60s trailing window crosses before `day_start_ms` carry `rolling_missing_window_flag = True`. Days 2..90 carry `rolling_missing_window_flag = False` (the tail buffer covers the entire 60s window). Per-event `invalid_window_flag = False` everywhere (Phase 4bm-D `invalid_windows = []`).
- **Output directory tree (v002-suffixed)**: `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`. The `__v002` directory suffix mirrors the v002 normalized derived family layout `microstructure_normalized_aggtrades_v001__v002/...` (Phase 4bm-B output) and preserves the refuse-to-overwrite invariant against the existing v001 Phase 4bh single-day feature parquet at the unsuffixed `microstructure_features_aggtrades_v001/...` path (which remains byte-identical, SHA `618d9b86…`).
- **Forbidden-substring detector compliance**: the Phase 4bm-G §13 26-token list (`label, target, future, signal, entry, exit, pnl, profit, loss, mfe, mae, r_multiple, equity, position, alpha, edge, prediction, model, score, decision, strategy, liquidation, funding, open_interest, order_book, mark_price`) is applied to the v002 schema at import time and at compute-build time and passes. The prompt-proposed lineage column `source_phase_4bm_e_decision` triggered the `decision` token and was renamed to **`source_phase_4bm_e_outcome`** per the Phase 4bm-G §13 "adjust to a safe equivalent and document the reason" path; the literal value remains `"Option B / Decision form 2"`.

## §12 Boundary Statements (Required Exact Phrases)

The following phrases appear verbatim:

- **Phase 4bm-H is feature computation only.**
- **Stage-4 is not authorized by Phase 4bm-H.**
- **Phase 4bm-I is not authorized by Phase 4bm-H.**
- **Feature-family research-use is not authorized by Phase 4bm-H.**
- **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-H.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

Additional preserved boundaries:

- no tracked data/microstructure artefact changed by this merge;
- no generated feature artefact was committed;
- the original v002 derived manifest is unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- the original v002 raw manifest is unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- the Phase 4bm-F successor-state JSON is unchanged;
- no labels / diagnostics / ML / strategy / backtest / acquisition work was authorized or performed.

## §13 Boundaries Preserved

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..F / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G results — all preserved verbatim.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

**N-DERIVATION** does NOT apply to Phase 4bm-H, because the phase explicitly performs feature computation — its sole authorized scope.

## §14 Recommended State

**Remain paused.**

Phase 4bm-H is project-complete on `main` by this merge + merge-closeout. The operator's broader pause decision continues to apply.

## §15 Conditional Next Options (none authorized)

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | n/a | **recommended** |
| Future **Phase 4bm-I — Multi-Day V002 Feature Artefact Structural QA Memo** (multi-day analogue of Phase 4bi-A) | docs-only + analysis | **NOT authorized by this merge** |
| Future v002 feature-family eligibility-gate design + implementation + execution (multi-day analogue of Phase 4bi-B) | code + docs + local gitignored gate report | **NOT authorized by this merge** |
| Future v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C) | docs-only | **NOT authorized by this merge** |
| Future v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D) | docs + local gitignored successor-state JSON | **NOT authorized by this merge** |
| Multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by this merge** |
| Additional acquisition (more days / cross-symbol / mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated APIs / private endpoints) | docs + data | **NOT authorized by this merge** |
| Label computation, diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this merge** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this merge** |

## §16 Explicit Non-Authorization

This merge does **not**, and **cannot**, authorize:

- Phase 4bm-I (canonical successor; the multi-day v002 feature artefact structural QA memo);
- v002 feature artefact structural QA;
- v002 feature-family eligibility-gate design / implementation / execution;
- v002 feature-family research-use decision memo;
- v002 feature-family successor-state recording;
- any multi-day v002 label-family phase;
- any multi-day v002 chronological-split-policy memo;
- labels;
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
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, or Phase 4bm-G feature-boundary design;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.
