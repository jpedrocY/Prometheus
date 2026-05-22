# Phase 4bm-I — Closeout

**Phase identity:** Phase 4bm-I — Multi-Day V002 Feature Artefact Structural QA Memo.
**Phase type:** docs-only + read-only local artefact analysis (no code / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file modified).
**Status:** branch-complete; **NOT** project-complete. Project-completion requires a separately authorized merge phase per `docs/00-meta/process/merge-closeout-standard.md`.

## 1. Branch name

`phase-4bm-i/multi-day-v002-feature-artefact-structural-qa-memo`

## 2. Base SHA

`0106321f6e9dc9d028739ecf89ee3ded6867862a` (Phase 4bm-H merge-closeout SHA-finalization on `main`). Pre-branch `main == origin/main`.

## 3. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 hierarchy and the direct v001 precedent (Phase 4bi-A v001 feature artefact structural QA memo was Tier 1). This is the first multi-day v002 feature artefact structural QA, and although docs-only + read-only by construction (no source / test / script / data is modified), the verdict influences downstream authorization decisions (Phase 4bm-J feature-family eligibility gate; future feature-family research-use). Tier 1 ceremony applies: dedicated branch, full implementation report, this closeout, narrow `current-project-state.md` update, and (separately) a future Tier 1 merge-closeout.

## 4. Tracked files added / modified

Added (new tracked files):

- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-i_multi-day-v002-feature-artefact-structural-qa-memo.md` — the 24-section main structural QA memo.
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-i_closeout.md` — this closeout.

Modified (narrow, tracked):

- `docs/00-meta/current-project-state.md` — narrow Phase 4bm-I narrative paragraph + new "Current phase:" block; prior Phase 4bm-H "Current phase:" block preserved as labelled historical context.

**No** source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified. **No** `data/microstructure/` artefact is created, modified, or deleted by Phase 4bm-I. `.gitignore`, `.gitattributes`, `pyproject.toml`, `README.md`, `.mcp.json` (absent), `.claude/`, and every other tracked file outside the three docs files above are unchanged.

## 5. Local gitignored outputs inspected (not modified)

Phase 4bm-I inspected the local gitignored Phase 4bm-H v002 feature artefacts on disk in **read-only** mode:

- 90 v002 feature Parquets under `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/` (one per UTC date 2024-12-01..2025-02-28 inclusive).
- 90 paired canonical Phase 4bb-F sidecars under the same tree.
- 1 v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`.
- 1 paired canonical Phase 4bb-F sidecar at `<manifest>.sha256`.

Total: **182 local gitignored artefacts inspected**. **None modified.** All four representative paths confirmed gitignored under `.gitignore:85` (`data/microstructure/`); `git status --short` shows only the pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).

## 6. Structural QA verdict

**FEATURE_STRUCTURAL_QA_PASS.**

## 7. Key PASS evidence

- 90 / 90 v002 feature Parquets present at expected paths (QA A).
- 90 / 90 v002 feature sidecars present at expected paths (QA A).
- Manifest SHA256 = `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (matches Phase 4bm-H expected; QA C.1).
- Manifest sidecar SHA256 = `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` (matches Phase 4bm-H expected; QA C.2).
- Manifest sidecar canonical Phase 4bb-F format (66 hex + two ASCII spaces + 50-byte basename + LF; total 116 bytes; no CRLF; no BOM; QA C.3–C.5).
- feature_config_hash = `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` (matches Phase 4bm-H expected; QA D.9).
- Total feature row count = 155,153,449 (1:1 parity with Phase 4bm-B v002 normalized event count; QA F.1).
- 90 / 90 per-day feature row counts equal corresponding v002 normalized per-day event counts byte-for-byte (QA F.2).
- 90 / 90 per-day feature Parquet SHA256 values match manifest `per_day_outputs[i].feature_parquet_sha256` byte-for-byte (QA F.5).
- 90 / 90 per-day feature sidecars canonical Phase 4bb-F format and SHA-consistent (QA G.1).
- All 90 feature Parquets share the identical canonical 62-column schema (17 lineage + 45 feature/quality) and identical pyarrow `num_rows` matching the manifest (QA H.3, H.4).
- Sampled deep scan over 6 representative dates (day 1, last day of each month, day 90) confirms: canonical column order; symbol / utc_date / dataset_version / source_dataset_version / feature_schema_version / lineage SHA columns constant per-day; row_index 0..n-1 contiguous and strictly increasing by 1; feature_timestamp_ms monotonic non-decreasing; feature_timestamp_ms == source_transact_time_ms; all rows in half-open `[day_start_ms, day_end_ms)` (QA H.*).
- Day 1 (`2024-12-01`) `rolling_missing_window_flag = True` rule applied correctly to 384 rows in the first 60 seconds of UTC `2024-12-01`; days 2..90 sampled have `rolling_missing_window_flag = False` everywhere (QA I.1–I.4).
- Phase 4bm-G §13 forbidden-substring detector: 0 hits across the 62-column schema; safe `source_phase_4bm_e_outcome` column present; unsafe `source_phase_4bm_e_decision` absent (QA E.9–E.12).
- 12 / 12 upstream lineage artefacts byte-identical pre/post QA (QA J.* across the v002 derived manifest + sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-D-R gate report, Phase 4bl-E successor-state, Phase 4bm-D gate report + sidecar, Phase 4bm-F successor-state + sidecar, and the v001 Phase 4bh single-day feature parquet + sidecar). 90 / 90 v002 normalized per-day Parquets byte-identical to the v002 derived multi-day index manifest's `per_file_inventory` SHAs.
- v002 derived manifest still `research_eligible = false` / `eligibility_gate_status = "pending"`; v002 raw manifest still `research_eligible = false` / `eligibility_gate_status = "pending"`; Phase 4bm-F successor-state JSON unchanged; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- 89 / 89 targeted v002 pytest pass (QA K).

The only QA-script-level observation (E.5 `feature_dtypes` dict iteration order) is an intentional canonical-JSON serialization convention (`json.dumps(sort_keys=True)` at write time alphabetizes dict keys in the JSON file). Every one of the 62 canonical columns has a dtype entry; set equality with `feature_column_names` is exact; the authoritative canonical column order is preserved in the `feature_column_names` list. This is not a structural defect and does not change the verdict.

## 8. Validation results

- `git status --short`: shows only the expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); no `data/microstructure/` artefact in `git status` (all gitignored).
- `git diff --check`: clean (no whitespace, no conflict markers).
- `git check-ignore -v data/microstructure/`, `data/microstructure/features/`, `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`, `<manifest>.sha256`: all return `.gitignore:85: data/microstructure/`.

## 9. Targeted test results

```text
pytest tests/research/microstructure/test_features_schema_v002.py \
       tests/research/microstructure/test_features_io_v002.py \
       tests/research/microstructure/test_features_manifest_v002.py \
       tests/research/microstructure/test_features_no_network_v002.py \
       tests/research/microstructure/test_features_compute_v002.py
```

Result: **89 passed in 0.91s**. All 89 Phase 4bm-H v002 tests pass against the locked v002 schema, kernel, manifest, IO, and static no-network surface. The compute test module uses pytest `tmp_path` exclusively and writes nothing to real `data/microstructure/` outputs.

## 10. Non-authorization boundaries

Phase 4bm-I honors **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION** (no normalization / derivation / feature recomputation / label computation occurred — QA inspected existing artefacts read-only), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).

## 11. Recommended state

**Remain paused.**

Phase 4bm-I is branch-complete by this work. Per `phase-workflow-standard.md`, Phase 4bm-I is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per the full Tier 1 16-section structure. The operator's broader pause decision continues to apply.

## 12. Non-authorization (explicit)

Phase 4bm-I does **not**, and **cannot**, authorize:

- **Phase 4bm-J — Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution** (the canonical successor; the multi-day analogue of Phase 4bi-B);
- v002 feature-family eligibility gate;
- v002 feature-family research-use decision;
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
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, or Phase 4bm-H feature computation;
- amending this QA verdict;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.
