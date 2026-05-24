# Phase 4bm-P — Closeout

**Phase identity:** Phase 4bm-P — Multi-Day V002 Label Artefact Structural QA Memo.
**Phase type:** docs-only + read-only local artefact analysis (no code / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file modified).
**Status:** branch-complete; **NOT** project-complete. Project-completion requires a separately authorized merge phase per `docs/00-meta/process/merge-closeout-standard.md`.

## 1. Branch name

`phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo`

## 2. Base SHA

`75371ffd8607f3586130f02d6ffd124b7b707dfb` (Phase 4bm-O merge-closeout SHA-finalization on `main`). Pre-branch `main == origin/main`.

## 3. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 hierarchy and the direct v001 precedent (Phase 4bj-D v001 label artefact structural QA memo was Tier 1). This is the first multi-day v002 label artefact structural QA, and although docs-only + read-only by construction (no source / test / script / data is modified), the verdict influences downstream authorization decisions (the future multi-day v002 label-family eligibility gate Phase 4bm-Q; future label-family research-use; future chronological-split-policy decisions). Tier 1 ceremony applies: dedicated branch, full implementation report, this closeout, narrow `current-project-state.md` update, and (separately) a future Tier 1 merge-closeout.

## 4. Tracked files added / modified

Added (new tracked files):

- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_multi-day-v002-label-artefact-structural-qa-memo.md` — the 31-section main structural QA memo.
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_closeout.md` — this closeout.

Modified (narrow, tracked):

- `docs/00-meta/current-project-state.md` — narrow Phase 4bm-P narrative paragraph + new "Current phase:" block; prior Phase 4bm-O "Current phase:" block preserved as labelled historical context.

**No** source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified. **No** `data/microstructure/` artefact is created, modified, or deleted by Phase 4bm-P. `.gitignore`, `.gitattributes`, `pyproject.toml`, `README.md`, `.mcp.json` (absent), `.claude/`, and every other tracked file outside the three docs files above are unchanged.

## 5. Local gitignored outputs inspected (not modified)

Phase 4bm-P inspected the local gitignored Phase 4bm-O v002 label artefacts on disk in **read-only** mode:

- 90 v002 label Parquets under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/` (one per UTC date 2024-12-01..2025-02-28 inclusive).
- 90 paired canonical Phase 4bb-F sidecars under the same tree.
- 1 v002 label manifest at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`.
- 1 paired canonical Phase 4bb-F sidecar at `<manifest>.sha256`.

Total: **182 local gitignored label artefacts inspected**. **None modified.** All four representative paths confirmed gitignored under `.gitignore:85` (`data/microstructure/`); `git status --short` shows only the pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).

## 6. Structural QA verdict

**LABEL_STRUCTURAL_QA_PASS — label artefact remains not research-eligible.**

(Equivalent to the Phase 4bj-D v001 precedent verdict phrasing "STRUCTURAL QA PASS — label artefact remains not research-eligible", with the `<FAMILY>_STRUCTURAL_QA_PASS` naming convention also used in Phase 4bm-I.)

## 7. Key PASS evidence

- 90 / 90 v002 label Parquets present at expected paths (QA A).
- 90 / 90 v002 label sidecars present at expected paths (QA A).
- Label manifest SHA256 = `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (matches Phase 4bm-O expected; QA C.1).
- Label manifest sidecar SHA256 = `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (matches Phase 4bm-O expected; QA C.2).
- Label manifest sidecar canonical Phase 4bb-F format (64 hex + two ASCII spaces + 47-byte basename + LF; total 114 bytes; no CRLF; no BOM; QA C.3–C.5).
- `label_config_hash` = `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` (matches Phase 4bm-O expected; manifest top-level + per-row constant across sampled days).
- Total label row count = **155,153,449** (1:1 parity with v002 feature row count; QA E.1 / E.3).
- 90 / 90 per-day label row counts equal corresponding v002 feature per-day row counts byte-for-byte (QA E.2).
- 90 / 90 per-day label Parquet SHA256 values match manifest `per_day_outputs[i].sha256` byte-for-byte (QA E.6).
- 90 / 90 per-day label Parquet byte sizes match manifest `per_day_outputs[i].byte_size` byte-for-byte; aggregate **6,145,349,264** bytes (QA E.7).
- 90 / 90 per-day label sidecars canonical Phase 4bb-F format and SHA-consistent with manifest `per_day_outputs[i].sidecar_sha256` (QA F.1).
- All 90 label Parquets share the identical canonical 40-column schema (17 lineage + 1 `label_config_hash` + 8 labels + 14 support) at the pyarrow `schema_arrow.names` level and identical `metadata.num_rows` matching the manifest (QA D.1–D.11; D.8).
- Forbidden-substring scan: **0 hits** across the 40-column canonical list (QA D.9).
- Per-horizon censored counts `{"1s": 14, "5s": 39, "15s": 170, "60s": 634}` (manifest top-level) aggregate from per-day `per_horizon_censored_counts` byte-for-byte; concentrated entirely on the envelope terminal day `2025-02-28`; per-row censoring rule `flag iff feature_timestamp_ms + horizon_ms_H > envelope_terminal_unix_ms` verified across sampled rows × 4 horizons × 6 dates with 0 violations (QA G.1–G.8).
- Invalid-price row count = **0** at manifest top-level and per-day aggregate; sampled rows confirm `label_invalid_price_flag == False` uniformly (QA H.1–H.3); sampled uncensored `forward_log_return_H` finite (QA H.4).
- `forward_direction_H ∈ {-1, 0, 1, null}` strict-sign policy preserved (QA I.1); per-horizon nullable / boolean dtype checks pass (QA I.2–I.6).
- Sampled deep scan over 6 representative dates (`2024-12-01`, `2024-12-31`, `2025-01-15`, `2025-01-31`, `2025-02-15`, `2025-02-28`) confirms: canonical column order; `dataset_family` / `dataset_version` / `label_schema_version` / `symbol` / `utc_date` / `source_feature_dataset_family` / `source_feature_dataset_version` / `source_feature_manifest_sha256` / `source_feature_parquet_sha256` (day-varying) / `source_feature_successor_state_sha256` / `source_phase_4bm_j_gate_report_sha256` / `source_normalized_manifest_sha256` / `source_raw_manifest_sha256` / `label_config_hash` columns constant per-day at the expected values; `row_index` 0..n-1 contiguous and strictly increasing by 1; `feature_timestamp_ms` monotonic non-decreasing; `feature_timestamp_ms == source_transact_time_ms`; identity alignment (`agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`, `row_index`) with v002 feature parquets byte-for-byte across every sampled row (QA J.1–J.10).
- Causal-separation / leakage-boundary audit (QA K.1–K.5): labels are a sibling artefact (no feature mutation); feature lineage SHA pinning on every label row; cross-day reference resolution stays inside the 90-day v002 envelope; envelope-terminal censoring only; `label_config_hash` constant.
- 9 / 9 upstream lineage artefacts byte-identical pre/post QA (v002 feature manifest + sidecar; Phase 4bm-L successor-state + sidecar; Phase 4bm-J gate report + sidecar; v002 derived/normalized manifest + sidecar; v002 raw manifest) — QA §18.
- v002 feature manifest still `research_eligible = false` / `eligibility_gate_status = "pending"` / `stage_4_feature_cleared = false`; v002 derived/normalized manifest still `research_eligible = false` / `eligibility_gate_status = "pending"`; v002 raw manifest still `research_eligible = false` / `eligibility_gate_status = "pending"`; v002 label manifest still `research_eligible = false` / `eligibility_gate_status = "pending"` / `label_family_research_use_authorized = false` / `stage_5_label_cleared = false` / `chronological_split_policy = "not_yet_defined"`; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- 91 / 91 targeted v002 label pytest pass (QA §20).
- Post-QA git state byte-identical to pre-QA; label manifest SHA recomputed post-QA equals pre-QA value byte-for-byte (QA §19).

The three QA-script-level observations (§25 in the main memo: `per_horizon_censored_counts` vs `censored_per_horizon` naming, duplicative top-level boundary booleans vs `boundary_confirmations` dict, absence of redundant top-level `source_normalized_dataset_family/version` and `source_raw_dataset_family/version` scalars) are informational only — not structural defects and do not change the verdict.

## 8. Validation results

- `git status --short` (pre-execution and post-execution): only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected pre-existing).
- `git branch --show-current`: `phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo`.
- `git rev-parse main` and `git rev-parse origin/main`: both `75371ffd8607f3586130f02d6ffd124b7b707dfb` (in sync).
- `git log --oneline -12 --decorate`: latest main commit is `75371ff docs(phase-4bm-o): finalize merge closeout shas` (matches expectation).
- `git diff --check`: clean (exit 0; no whitespace, no conflict markers).
- `git diff --name-only`: empty (no tracked file modified by QA itself; the docs additions are separate commits).
- `git check-ignore -v data/microstructure/labels/`, `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/`, `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`, `<manifest>.sha256`: all return `.gitignore:85: data/microstructure/`.

## 9. Targeted test results

```text
pytest tests/research/microstructure/test_labels_schema_v002.py \
       tests/research/microstructure/test_labels_io_v002.py \
       tests/research/microstructure/test_labels_compute_v002.py \
       tests/research/microstructure/test_labels_manifest_v002.py \
       tests/research/microstructure/test_labels_no_network_v002.py
```

Result: **91 passed in 0.65s**. All 91 Phase 4bm-O v002 label tests pass against the locked v002 schema, kernel, manifest, IO, and static no-network surface. The compute test module uses pytest `tmp_path` fixtures exclusively and writes nothing to real `data/microstructure/` outputs (post-run on-disk SHA recompute confirms label manifest still equals `5e17074d…`).

## 10. Skipped checks and rationale

`scripts/phase4bm_o_compute_multiday_labels.py`, full whole-repo `pytest`, whole-repo `mypy src/prometheus`, and whole-repo `ruff check .` are intentionally **not** rerun by Phase 4bm-P. Rationale:

- Phase 4bm-P modifies **no** source / test / script / configuration; the Phase 4bm-O baselines (surface ruff PASS; 91/91 targeted v002 label tests PASS; 1623 microstructure pytest passed + 1 skipped; static no-network / no-credential scan PASS; mypy baseline of 29 errors in 5 files; whole-repo pytest blocked by 15 collection errors + 2 pre-existing subprocess failures) are preserved by construction.
- Rerunning the Phase 4bm-O orchestrator would attempt to recompute 90 per-day label Parquets and would fail closed at the refuse-to-overwrite check (Phase 4bm-O's intended fail-closed protection).

These skips conform to the project's standing precedent for read-only docs / QA phases (Phase 4bj-D v001 label QA precedent; Phase 4bm-C v002 normalized structural QA precedent; Phase 4bm-I v002 feature structural QA precedent).

## 11. Non-authorization boundaries

Phase 4bm-P honors **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION** (no normalization / derivation / feature recomputation / label computation occurred — QA inspected existing artefacts read-only), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).

## 12. Recommended state

**Remain paused.**

Phase 4bm-P is branch-complete by this work. Per `phase-workflow-standard.md`, Phase 4bm-P is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per the full Tier 1 16-section structure. The operator's broader pause decision continues to apply.

## 13. Non-authorization (explicit)

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

Phase 4bm-P does **not**, and **cannot**, authorize:

- **Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution** (the canonical conditional successor; the multi-day analogue of Phase 4bj-E);
- v002 label-family eligibility gate;
- v002 label-family research-use decision;
- v002 label-family successor-state recording;
- any multi-day v002 chronological-split-policy memo;
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
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` / `stage_5_label_cleared` / `label_family_research_use_authorized` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, Phase 4bm-H feature implementation, Phase 4bm-I feature structural QA, Phase 4bm-J feature-family eligibility gate, Phase 4bm-K feature-family research-use decision, Phase 4bm-L feature-family successor-state recording, Phase 4bm-M label-family boundary / design, Phase 4bm-N label schema finalization, or Phase 4bm-O label kernel implementation;
- amending this QA verdict;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.
