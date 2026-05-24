# Phase 4bm-O — Closeout

**Phase identity:** Phase 4bm-O — Multi-Day V002 Label Kernel Implementation + Local Label Artefact Generation.
**Phase type:** code + tests + docs + local gitignored label artefacts.
**Status:** branch-complete; **NOT** project-complete. Project-completion requires a separately authorized merge phase per `docs/00-meta/process/merge-closeout-standard.md`.

## 1. Branch name

`phase-4bm-o/multi-day-v002-label-kernel-local-artefacts`

## 2. Base SHA

`e2574c4ad6497686b974c39bfb351880e38fb0dd` (Phase 4bm-N merge-closeout SHA-finalization on `main`). Pre-branch `main == origin/main`.

## 3. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules ("any phase that creates features / labels / diagnostics" → Tier 1, period). Phase 4bm-O creates the first multi-day v002 label artefacts (code + tests + local gitignored data) and therefore receives the full Tier 1 ceremony: authorization prompt, dedicated branch, full implementation report, this closeout, narrow `current-project-state.md` update, and (separately) a future Tier 1 merge-closeout.

## 4. Tracked files added / modified

Added (new tracked files):

Source modules:
- `src/prometheus/research/microstructure/labels_schema_v002.py`
- `src/prometheus/research/microstructure/labels_io_v002.py`
- `src/prometheus/research/microstructure/labels_compute_v002.py`
- `src/prometheus/research/microstructure/labels_manifest_v002.py`

Script:
- `scripts/phase4bm_o_compute_multiday_labels.py`

Tests:
- `tests/research/microstructure/_labels_fixtures_v002.py`
- `tests/research/microstructure/test_labels_schema_v002.py`
- `tests/research/microstructure/test_labels_io_v002.py`
- `tests/research/microstructure/test_labels_compute_v002.py`
- `tests/research/microstructure/test_labels_manifest_v002.py`
- `tests/research/microstructure/test_labels_no_network_v002.py`

Docs:
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_multi-day-v002-label-kernel-local-artefacts.md`
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_closeout.md` (this file)

Modified (narrow, tracked):

- `src/prometheus/research/microstructure/__init__.py` — re-exports the Phase 4bm-O v002 label public API symbols (sorted into the existing alphabetical-by-section convention).
- `docs/00-meta/current-project-state.md` — narrow update to record Phase 4bm-O branch-complete status (new Phase 4bm-O narrative paragraph + new "Current phase:" block; prior Phase 4bm-N "Current phase:" block preserved as labelled historical context).

**No** prior tracked source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is otherwise modified. **No** prior `data/microstructure/` artefact is mutated.

## 5. Local gitignored outputs created

All outputs are gitignored under `.gitignore:85` (`data/microstructure/`) and are NOT committed.

- 90 v002 label Parquets under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet` (one per UTC date 2024-12-01 .. 2025-02-28 inclusive).
- 90 v002 label canonical Phase 4bb-F sidecars (one per Parquet, format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`).
- 1 v002 label manifest at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`.
- 1 v002 label manifest canonical Phase 4bb-F sidecar at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256`.

Total local gitignored artefacts created: **182**.

The per-day output inventory (utc_date, byte size, row count, label parquet SHA256, label sidecar SHA256, per-horizon censored counts, invalid-price row count, source feature parquet SHA256) is recorded in the v002 label manifest's `per_day_outputs` list.

## 6. Label manifest SHA256

- Path: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`
- SHA256: `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed`
- Size: 84,732 bytes
- `label_config_hash` recorded inside the manifest: `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`

## 7. Label manifest sidecar SHA256

- Path: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256`
- SHA256: `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd`
- Size: 114 bytes
- Canonical Phase 4bb-F format (`<sha256>  <basename>\n`); embedded SHA matches the recomputed manifest SHA byte-for-byte; basename matches manifest basename byte-for-byte; ASCII / UTF-8 no BOM; LF only; no CRLF.

## 8. Exact label manifest sidecar content

```
5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed  microstructure_labels_aggtrades_v001__v002.json
```

(One LF terminator after the basename; total file size 114 bytes = 64 + 2 + 47 + 1.)

## 9. Label artefact inventory

- 90 v002 label Parquets
- 90 v002 label sidecars
- 1 v002 label manifest
- 1 v002 label manifest sidecar
- **Total: 182 local gitignored artefacts.** **None are committed.**

## 10. Aggregate row count

**155,153,449** rows across the 90 per-day label parquets (1:1 parity with the Phase 4bm-H v002 feature row count exactly; per-day parity verified for every one of the 90 days by the orchestrator).

## 11. Column count

**40** columns per label parquet, in Phase 4bm-N §14 canonical order: 17 lineage / identity / metadata + 1 `label_config_hash` + 4 regression `forward_log_return_<horizon>` + 4 classification `forward_direction_<horizon>` + 12 per-horizon support + 2 global support.

## 12. label_config_hash

`352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`

(Constant across all 155,153,449 label parquet rows; matches `label_manifest.label_config_hash`.)

## 13. Censoring counts per horizon

```json
{"1s": 14, "5s": 39, "15s": 170, "60s": 634}
```

All 14 / 39 / 170 / 634 censorings are envelope-terminal censorings (target timestamp exceeds the envelope-terminal `1740787199996` = 2025-02-28T23:59:59.996Z); they fall entirely on day 90 (`2025-02-28`).

Per Phase 4bm-N §20 verbatim, censoring is **envelope-terminal only**: `horizon_censored_flag_H = true` iff `feature_timestamp_ms + horizon_ms_H > envelope_terminal_unix_ms` (= 1740787199996 ms = 2025-02-28T23:59:59.996Z). No per-day censoring is performed; horizons may cross UTC day boundaries inside the v002 90-day envelope (the kernel resolves the reference into the immediately-following day when the target lands past the current day's last `transact_time_ms`).

## 14. Invalid price row count

`0` (matches expectations: Phase 4bl-D-R + Phase 4bm-D upstream PASS evidence confirmed strictly positive prices for every row; the defensive `label_invalid_price_flag = true` branch in `labels_compute_v002` was never taken).

## 15. Key evidence

| Evidence item | Value |
|---|---|
| Phase 4bm-L successor-state JSON SHA256 | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (MATCH pre + MATCH post) |
| Phase 4bm-L successor-state sidecar SHA256 | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` (MATCH pre + MATCH post) |
| Phase 4bm-J gate verdict | `FEATURE_GATE_PASS` (`overall_status = pass`; 50 / 50 PASS; 0 FAIL; 0 ERROR; 0 NOT_APPLICABLE; 0 blocking failures) |
| Phase 4bm-J gate report SHA256 | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (MATCH pre + MATCH post) |
| Phase 4bm-J gate sidecar SHA256 | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` (MATCH pre + MATCH post) |
| Phase 4bm-I structural QA verdict | `FEATURE_STRUCTURAL_QA_PASS` (transitively confirmed by Phase 4bm-J check A12 PASS) |
| v002 feature manifest SHA256 | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (MATCH pre + MATCH post; unchanged) |
| v002 feature manifest sidecar SHA256 | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` (MATCH pre + MATCH post; unchanged) |
| v002 feature `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| v002 derived multi-day index manifest SHA256 | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (MATCH pre + MATCH post; unchanged) |
| v002 derived manifest sidecar SHA256 | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` (MATCH pre + MATCH post; unchanged) |
| Phase 4bm-F derived successor-state JSON SHA256 | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` (MATCH pre + MATCH post; unchanged) |
| Phase 4bm-D derived gate report SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` (MATCH pre + MATCH post; unchanged) |
| v002 raw manifest SHA256 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` (MATCH pre + MATCH post; unchanged) |
| v002 acquisition log SHA256 | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` (MATCH pre + MATCH post; unchanged) |
| Phase 4bl-E raw successor-state JSON SHA256 | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` (MATCH pre + MATCH post; unchanged) |
| Phase 4bl-D-R raw gate report SHA256 | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` (MATCH pre + MATCH post; unchanged) |
| 90 per-day v002 feature parquets | per-day SHAs from feature manifest `per_day_outputs[].feature_parquet_sha256` (90 / 90 MATCH pre + 90 / 90 MATCH post) |
| 90 per-day v002 normalized parquets | per-day SHAs from derived manifest `per_file_inventory[].parquet_sha256` (90 / 90 MATCH pre + 90 / 90 MATCH post) |
| `envelope_terminal_unix_ms` | `1740787199996` (= 2025-02-28T23:59:59.996Z) |
| `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` |
| Label manifest SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` |
| Label manifest sidecar SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` |
| Aggregate label parquet bytes (90 per-day Parquets) | 6,145,349,264 bytes (≈ 5.72 GiB) |
| Run elapsed | 1454.1 s (≈ 24m 14s) |

Total immutability witnesses: **194** (14 governance + 90 feature parquets + 90 normalized parquets), all byte-identical pre/post the Phase 4bm-O run.

## 16. Validation results

| Item | Result |
|---|---|
| 14 / 14 locked precondition SHAs MATCH pre-run | PASS |
| 90 / 90 per-day v002 feature parquet SHAs MATCH pre-run | PASS |
| 90 / 90 per-day v002 normalized parquet SHAs MATCH pre-run | PASS |
| 92 / 92 refuse-to-overwrite pre-write checks (90 parquets + 1 manifest + 1 manifest sidecar) | PASS |
| 90 per-day kernel invocations (40-column canonical schema; row count parity; identity column parity; no forbidden substring) | PASS |
| 90 / 90 per-day label row counts equal per-day feature row counts | PASS |
| Total label row count == 155,153,449 | PASS |
| 90 sidecars verified canonical Phase 4bb-F format (two-space; LF only; lowercase hex; basename match) | PASS |
| 1 label manifest carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `label_family_research_use_authorized = false`, `stage_5_label_cleared = false`, `chronological_split_policy = "not_yet_defined"`, all governance values locked, all 17 boundary confirmations `true`, all lineage SHAs cited verbatim | PASS |
| 194 / 194 upstream immutability checks PASS post-run | PASS |
| `git status` shows no tracked-file change outside the authorized scope and no `data/microstructure/` artefact (all label data is gitignored under `.gitignore:85`) | PASS |
| `git check-ignore -v data/microstructure/labels/` | covered by `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/` | covered by `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` | covered by `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` | covered by `.gitignore:85: data/microstructure/` |

## 17. Quality gate results or skipped-check rationale

- `ruff check` — Phase 4bm-O surface (4 source modules + 1 `__init__.py` update + 1 script + 6 test files): **PASS** ("All checks passed!" after one round of auto-fixable import-sort + Yoda-condition fixes).
- `pytest tests/research/microstructure/test_labels_*_v002.py` — **91 / 91 passed**.
- `pytest tests/research/microstructure/` — **1623 passed, 1 skipped** (no new regression; the 1 skipped test is pre-existing baseline).
- `git diff --check` — clean (exit 0).
- Static no-network / no-credential scan over 4 source modules + the orchestrator script — PASS.
- `mypy src/prometheus` and whole-repo `pytest` skipped at Phase 4bm-O level per the Phase 4bm-H precedent. Rationale: documented project baseline (29 mypy errors in 5 files; 15 pytest collection errors from missing `httpx` / `duckdb`; 2 `test_engine_d1a_dispatch.py` subprocess failures) is unchanged on `main` and unrelated to label / feature surfaces; new modules avoid third-party deps beyond the existing pyarrow / numpy / Decimal idioms used by v001 labels and v002 features; targeted Phase 4bm-O test sweep passes 91 / 91 + 1623 / 1623 + 1 skipped microstructure with no regression. Future Phase 4bm-O merge phase may rerun the full mypy + whole-repo pytest passes if the operator wishes to record them at merge-closeout time.

## 18. Non-authorization boundaries

Phase 4bm-O honors **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST** (the v002 feature / derived / raw manifests remain byte-identical; a new sibling v002 label manifest is the only manifest written, and it is gitignored), **N-GATE-RERUN**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (no successor-state artefact created by Phase 4bm-O).

**N-DERIVATION** does NOT apply — Phase 4bm-O is the explicitly authorized label-kernel computation phase.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).

## 19. Recommended state

**Remain paused.**

Phase 4bm-O is branch-complete by this work. Per `phase-workflow-standard.md`, Phase 4bm-O is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per the full Tier 1 16-section structure. The operator's broader pause decision continues to apply.

## 20. Non-authorization (explicit)

Phase 4bm-O does **not**, and **cannot**, authorize:

- Phase 4bm-P (any provisional successor; not authorized);
- multi-day v002 label artefact structural QA;
- multi-day v002 label-family eligibility-gate design / implementation / execution;
- multi-day v002 label-family research-use decision memo;
- multi-day v002 label-family successor-state recording;
- multi-day v002 chronological-split-policy memo;
- multi-day v002 chronological-split-policy successor-state recording;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
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
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` / `stage_5_label_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, Phase 4bm-L, Phase 4bm-M, or Phase 4bm-N;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

## 21. Required exact phrases (verbatim, per task brief)

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
