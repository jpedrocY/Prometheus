# Phase 4bm-H — Closeout

**Phase identity:** Phase 4bm-H — Multi-Day V002 Feature Schema / Feature Computation Implementation.
**Phase type:** code + tests + docs + local gitignored feature artefacts.
**Status:** branch-complete; **NOT** project-complete. Project-completion requires a separately authorized merge phase per `docs/00-meta/process/merge-closeout-standard.md`.

## 1. Branch name

`phase-4bm-h/multi-day-v002-feature-schema-computation-implementation`

## 2. Base SHA

`3a7c6488d38997ffd25bc06952dab4e9f040ef8f` (Phase 4bm-G merge-closeout SHA-finalization on `main`). Pre-branch `main == origin/main`.

## 3. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules ("any phase that creates features / labels / diagnostics" → Tier 1, period). Phase 4bm-H creates the first multi-day v002 feature artefacts (code + tests + local gitignored data) and therefore receives the full Tier 1 ceremony: authorization prompt, dedicated branch, full implementation report, this closeout, narrow `current-project-state.md` update, and (separately) a future Tier 1 merge-closeout.

## 4. Tracked files added / modified

Added (new tracked files):

- `src/prometheus/research/microstructure/features_schema_v002.py`
- `src/prometheus/research/microstructure/features_io_v002.py`
- `src/prometheus/research/microstructure/features_compute_v002.py`
- `src/prometheus/research/microstructure/features_manifest_v002.py`
- `scripts/phase4bm_h_compute_multiday_features.py`
- `tests/research/microstructure/_multiday_features_fixtures_v002.py`
- `tests/research/microstructure/test_features_schema_v002.py`
- `tests/research/microstructure/test_features_io_v002.py`
- `tests/research/microstructure/test_features_compute_v002.py`
- `tests/research/microstructure/test_features_manifest_v002.py`
- `tests/research/microstructure/test_features_no_network_v002.py`
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-h_multi-day-v002-feature-schema-computation-implementation.md`
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-h_closeout.md` (this file)

Modified (narrow, tracked):

- `src/prometheus/research/microstructure/__init__.py` — re-exports the Phase 4bm-H v002 public API symbols (sorted into the existing alphabetical-by-section convention).
- `docs/00-meta/current-project-state.md` — narrow update to record Phase 4bm-H branch-complete status.

**No** prior tracked source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is otherwise modified. **No** prior `data/microstructure/` artefact is mutated.

## 5. Local gitignored outputs created

All outputs are gitignored under `.gitignore:85` (`data/microstructure/`) and are NOT committed.

- 90 v002 feature Parquets under `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet` (one per UTC date 2024-12-01 .. 2025-02-28 inclusive).
- 90 v002 feature canonical Phase 4bb-F sidecars (one per Parquet, format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`).
- 1 v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`.
- 1 v002 feature manifest canonical Phase 4bb-F sidecar at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json.sha256`.

Total local gitignored artefacts: **182**.

The per-day output inventory (utc_date, row_count, parquet SHA256, sidecar SHA256, source per-day normalized parquet SHA256) is recorded in the v002 feature manifest's `per_day_outputs` list.

## 6. Feature manifest SHA256

- Path: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`
- SHA256: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d`
- Size: 85,929 bytes
- `feature_config_hash` recorded inside the manifest: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`

## 7. Feature manifest sidecar SHA256

- Path: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json.sha256`
- SHA256: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`
- Size: 116 bytes
- Canonical Phase 4bb-F format (`<sha256>  <basename>\n`); embedded SHA matches the recomputed manifest SHA byte-for-byte; basename matches manifest basename byte-for-byte.

## 8. Number of feature Parquets and sidecars

- feature parquet count: **90**
- feature sidecar count: **90**
- feature manifest count: **1**
- feature manifest sidecar count: **1**

## 9. Total feature row count

**155,153,449** rows across the 90 per-day feature Parquets (1:1 parity with the Phase 4bm-B v002 normalized total event count; per-day parity verified).

## 10. Validation results

All validations PASS. See implementation report §16 for the full list:

- 10 / 10 locked precondition SHAs match expected pre-run (v002 derived manifest, v002 derived manifest sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-D-R raw multi-day PASS gate report, Phase 4bl-E raw multi-day successor-state JSON, Phase 4bm-D authoritative derived-family gate report, Phase 4bm-D sidecar, Phase 4bm-F v002 derived successor-state JSON, Phase 4bm-F successor-state sidecar);
- 92 / 92 refuse-to-overwrite pre-write checks PASS (90 per-day parquets + 1 manifest + 1 manifest sidecar);
- 90 per-day kernel invocations PASS (19-column source schema check; `dataset_version == "v002"`; `row_index == arange(n)`; `transact_time_ms` non-decreasing; quantities > 0; prices finite > 0; output schema canonical; row count parity; no forbidden substring);
- 90 / 90 per-day feature row counts equal per-day source normalized row counts;
- total feature row count == 155,153,449;
- 90 sidecars verified canonical Phase 4bb-F format;
- 1 feature manifest carries `research_eligible = false`, `eligibility_gate_status = "pending"`, all 8 non-authorization flags `false`, all 18 boundary confirmations `true`, all expected lineage SHAs cited;
- 100 / 100 upstream immutability checks PASS post-run (10 governance + 90 per-day normalized parquets all byte-identical);
- `git status` shows no tracked-file change outside the authorized scope and no `data/microstructure/` artefact (all data is gitignored).

## 11. Quality gate results

- `ruff check` — Phase 4bm-H surface: PASS. Whole-repo: PASS (after a one-line `__init__.py` import-sort auto-fix).
- `mypy src/prometheus` — 29 errors in 5 files (28 pre-existing v001 / labels / httpx baseline; 1 new file `features_compute_v002.py` mirrors the v001 `features_compute.py` `np.concatenate(([0], ...))` idiom; no new mypy category introduced; consistent with v001 Phase 4bh baseline).
- `pytest tests/research/microstructure` — **1471 passed, 1 skipped** (the skipped test is pre-existing baseline). All 89 new Phase 4bm-H tests PASS.
- Whole-repo `pytest` baseline — 15 pre-existing collection errors (missing `httpx` / `duckdb` env modules) + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures (`prometheus` import in subprocess); confirmed identical baseline on `main`. **No new pytest failure introduced by Phase 4bm-H.**

## 12. Non-authorization boundaries

Phase 4bm-H honors **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST** (original v002 derived manifest preserved byte-identically; new sibling v002 feature manifest is the only manifest written and is gitignored), **N-GATE-RERUN**, **N-SUCCESSOR-STATE** (no successor-state artefact created), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

**N-DERIVATION** does NOT apply — Phase 4bm-H is the explicitly authorized feature-computation phase.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).

## 13. Recommended state

**Remain paused.**

Phase 4bm-H is branch-complete by this work. Per `phase-workflow-standard.md`, Phase 4bm-H is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per the full Tier 1 16-section structure. The operator's broader pause decision continues to apply.

## 14. Non-authorization (explicit)

Phase 4bm-H does **not**, and **cannot**, authorize:

- Phase 4bm-I — Multi-Day V002 Feature Artefact Structural QA Memo (the canonical successor);
- v002 feature artefact structural QA;
- v002 feature-family eligibility-gate design / implementation / execution;
- v002 feature-family research-use decision memo;
- v002 feature-family successor-state recording;
- any multi-day v002 label-family phase;
- any multi-day v002 chronological-split-policy memo;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy implementation, signal construction;
- backtest implementation or execution;
- additional acquisition (cross-symbol, multi-quarter, mark-price, order-book, funding, OI, liquidation, cross-venue);
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
- amending Phase 4ak M0, Phase 4al refined no-rescue, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, or Phase 4bm-G feature-boundary design;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.
