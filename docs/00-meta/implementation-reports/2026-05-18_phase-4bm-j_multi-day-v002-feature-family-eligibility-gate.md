# Phase 4bm-J — Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution

**Phase identity:** Phase 4bm-J — Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution.
**Date:** 2026-05-18.
**Branch:** `phase-4bm-j/multi-day-v002-feature-family-eligibility-gate`.
**Base:** `main` at `3212722a7ffdd572ac2291ba1500f63f6fad6c59` (Phase 4bm-I merge-closeout SHA-finalization commit; pre-branch `main == origin/main` in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bi-B feature-family eligibility gate precedent. First-of-kind v002 multi-day feature-family eligibility gate design + implementation + execution. Tier 1 ceremony applies: dedicated branch, full implementation report, separate closeout, narrow `current-project-state.md` update, and (separately) a future Tier 1 merge-closeout.
**Phase type:** code + tests + docs + local gitignored feature-family gate report. Tracked code/tests/scripts/docs are committed; the gate report + paired canonical Phase 4bb-F sidecar remain gitignored under `.gitignore:85` (`data/microstructure/`) and are NOT committed.
**Status:** branch-complete; pending operator review; **not** project-complete (requires separately authorized merge phase).

---

## 1. Scope and boundary

Phase 4bm-J implements a deterministic, offline, fail-closed, read-only feature-family eligibility gate over the existing Phase 4bm-H v002 feature artefacts (90 per-day Parquets + 90 sidecars + 1 feature manifest + 1 manifest sidecar; 155,153,449 rows; BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28). It runs the gate exactly once and emits a single local gitignored gate report JSON + paired canonical Phase 4bb-F sidecar under `data/microstructure/gate-reports/features/`. The gate verdict reached **FEATURE_GATE_PASS** at report level only.

**Phase 4bm-J does not authorize feature-family research-use.** **Phase 4bm-J does not authorize feature-family successor-state recording.** **Phase 4bm-J does not authorize labels, diagnostics, ML, strategy, or backtests.** **Phase 4bm-J does not authorize additional acquisition, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.**

---

## 2. Linkage to Phase 4bm-I FEATURE_STRUCTURAL_QA_PASS

Phase 4bm-J treats the v002 feature family as structurally well-formed only via the Phase 4bm-I structural QA verdict. Check **A12** in the gate suite asserts `structural_qa_verdict == "FEATURE_STRUCTURAL_QA_PASS"` as a precondition. The Phase 4bm-I memo (read-only QA, 50+ checks; no upstream mutation) is the immediate evidence base for the v002 Feature Stage-3 marker; Phase 4bm-J converts that evidence into a stable, deterministic Feature Stage-4 report-level marker without altering any artefact.

---

## 3. Linkage to Phase 4bm-H feature artefacts

Every Phase 4bm-J check inspects the on-disk Phase 4bm-H artefacts read-only:

- Feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` (SHA `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d`; 85,929 bytes).
- Feature manifest sidecar at `<manifest>.sha256` (SHA `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`; 116 bytes; canonical Phase 4bb-F format).
- 90 per-day v002 feature Parquets under `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`.
- 90 paired canonical Phase 4bb-F sidecars.
- `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` (Phase 4bm-H locked value).

The gate also re-hashes all 10 v002 governance artefacts (v002 derived manifest + sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-D-R gate report, Phase 4bl-E raw successor-state, Phase 4bm-D gate report + sidecar, Phase 4bm-F successor-state + sidecar) and confirms they remain byte-identical to the Phase 4bm-G / Phase 4bm-H / Phase 4bm-I recorded values.

---

## 4. Linkage to Phase 4bm-G feature-boundary design

The Phase 4bm-J check suite enforces every Phase 4bm-G §13 / §14 / §16 / §18 binding rule by direct on-disk verification:

- §13 forbidden-substring detector: 0 hits across the 62-column schema (C7).
- §14 leakage / timestamp policy: `feature_timestamp_ms == source_transact_time_ms` on every sampled row; `(feature_timestamp_ms, row_index)` monotonic per day (D6).
- §16 multi-day rolling-window / cross-day lookback: day 1 `rolling_missing_window_flag` rule confirmed against `(T - 60_000) < day_start_ms` (E1); days 2..90 sampled `rolling_missing_window_flag = False` (E2); per-event `invalid_window_flag = False` everywhere (E3).
- §18 fail-closed rules: missing/SHA-mismatched lineage artefact, manifest mutation attempt, non-monotonic timestamp, forbidden column, network/credential surface — every category surfaces as an A/B/C/D/F group check.

The safe `source_phase_4bm_e_outcome` lineage column is verified present (C5) and the unsafe `source_phase_4bm_e_decision` column is verified absent (C6).

---

## 5. Linkage to v001 Phase 4bi-B precedent

Phase 4bm-J is the multi-day v002 analogue of Phase 4bi-B (the v001 feature-family eligibility gate). The v002 implementation mirrors the v001 module structure verbatim with v002-specific schema and lineage:

| Surface | v001 Phase 4bi-B | v002 Phase 4bm-J |
| --- | --- | --- |
| IO module | `feature_gate_io.py` | `multiday_feature_gate_io.py` |
| Report model | `feature_gate_report.py` | `multiday_feature_gate_report.py` |
| Check suite | `feature_gate_checks.py` (70 checks) | `multiday_feature_gate_checks.py` (50 checks) |
| Orchestrator | `feature_gate.py` | `multiday_feature_gate.py` |
| Script | n/a (run via tests) | `scripts/phase4bm_j_run_multiday_feature_gate.py` |
| Output namespace | `data/microstructure/gate-reports/features/` | same |
| Verdict taxonomy | PASS / FAIL / (no INDETERMINATE) | **PASS / FAIL / INDETERMINATE** (added INDETERMINATE for ERROR-only path) |

The Phase 4bm-J check count is tighter (50 vs 70) because the multi-day v002 data range is much larger and each check encompasses 90-day data. Schema-level checks are bulk operations (all 90 parquets) rather than single-day.

---

## 6. Gate design and check groups

The gate suite runs **50 deterministic checks** in canonical order across 7 groups:

| Group | Count | Scope |
| --- | --- | --- |
| **A** Locked preconditions | 12 | Phase 4bm-G / 4bm-H / 4bm-I lineage SHA + verdict preconditions (feature manifest SHA, manifest sidecar SHA + canonical content, Phase 4bm-D gate report + sidecar SHAs, Phase 4bm-F successor-state + sidecar SHAs, Phase 4bl-D-R + Phase 4bl-E SHAs, v002 derived manifest SHA, v002 raw manifest SHA, Phase 4bm-I structural QA verdict). |
| **B** Inventory / sidecar / gitignore | 10 | 90 feature parquets present; 90 feature sidecars present; canonical date inventory; BTCUSDT only; per_day_outputs length 90 + unique dates; all 90 sidecars canonical Phase 4bb-F + SHA-consistent; all 90 per-day parquet SHAs match manifest. |
| **C** Schema / lineage / forbidden | 10 | 62-column total; feature_column_names canonical order; 17 lineage + 45 feature/quality counts; safe `source_phase_4bm_e_outcome` present; unsafe `source_phase_4bm_e_decision` absent; 0 forbidden-substring hits across 26-token Phase 4bm-G §13 list; feature_config_hash matches; dataset identity literals match; all 90 parquets share canonical 62-column schema. |
| **D** Row-count / partition / timestamp | 6 | Total row count 155,153,449; sum(per_day_outputs.row_count) == total; per-day feature row count == source normalized event count (90/90 days); no zero-row day; pyarrow num_rows matches manifest (90/90); 6 sample dates pass canonical column order + symbol/utc_date/dataset_version/source_dataset_version/feature_schema_version/lineage-SHA constancy + row_index 0..n-1 contiguous + row_index step 1 + T monotonic + T == source_transact_time + half-open day partitioning. |
| **E** Quality flags / cross-day boundary | 3 | Day 1 `rolling_missing_window_flag` matches `(T - 60_000) < day_start_ms`; days 2..90 sampled `rolling_missing_window_flag = False` everywhere; `invalid_window_flag = False` on every sampled day. |
| **F** Upstream immutability | 3 | All 90 v002 normalized per-day Parquets byte-identical to derived manifest's `per_file_inventory` SHAs; v002 derived manifest still `research_eligible=false / eligibility_gate_status="pending"`; v002 raw manifest still `research_eligible=false / eligibility_gate_status="pending"`. |
| **G** Non-authorization invariants | 6 | Feature manifest `research_eligible=false`; `eligibility_gate_status="pending"`; `stage_4_feature_cleared=false`; all 7 non-authorization flags (`label_computation_authorized` / `diagnostics_authorized` / `ml_authorized` / `strategy_authorized` / `backtest_authorized` / `acquisition_authorized` / `successor_authorization_after`) `false`; all 5 immutability flags (`no_network_io` / `no_credentials` / `no_mcp_or_graphify` / `no_manifest_mutation` / `phase_4aw_flip_research_eligible_invariant_preserved`) `true`; boundary_confirmations count >= 18 and all True. |

Verdict classification: **FEATURE_GATE_PASS** iff zero blocking failures AND zero ERROR results; **FEATURE_GATE_INDETERMINATE** iff zero blocking failures AND >0 ERROR results; **FEATURE_GATE_FAIL** otherwise.

---

## 7. Gate implementation files

Added (new source, all under `src/prometheus/research/microstructure/`):

- `multiday_feature_gate_io.py` (~210 lines) — path discipline (`assert_path_under_feature_gate_reports`), SHA256 helpers, JSON / sidecar atomic writers with refuse-to-overwrite, canonical Phase 4bb-F sidecar composer, report-id derivation.
- `multiday_feature_gate_report.py` (~330 lines) — `MultidayFeatureGateReport` frozen data model with hard-invariant enforcement (`research_eligible_after = false`, `eligibility_gate_status_after = "pending"`, `stage_4_feature_cleared_after = false`, all 8 non-authorization flags false, all 14 immutability flags true), `_classify_gate_verdict`, `build_report`, `write_gate_report`.
- `multiday_feature_gate_checks.py` (~870 lines) — 50 check functions A1..G6, `MultidayFeatureGateCheckStatus`, `MultidayFeatureGateCheckResult`, `MultidayFeatureGateContext`, `CHECK_ORDER`, `SAMPLE_DATES`, `EXPECTED_*` locked constants, `run_all_checks` orchestrator with safe per-check ERROR conversion.
- `multiday_feature_gate.py` (~170 lines) — `MultidayFeatureGateInput`, `MultidayFeatureGateResult`, `MultidayFeatureGateError`, `run_multiday_feature_family_gate`.

Modified narrowly:

- `src/prometheus/research/microstructure/__init__.py` — re-exports the Phase 4bm-J public API.

Added (script):

- `scripts/phase4bm_j_run_multiday_feature_gate.py` (~140 lines) — standalone runner; ``--code-commit-sha``; ``--write-report`` (default True); emits a single deterministic local gitignored gate report + paired sidecar.

No prior source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified by Phase 4bm-J.

---

## 8. Tests added

Added under `tests/research/microstructure/`:

- `_multiday_feature_gate_fixtures.py` — shared fixture builder that constructs a tiny on-disk replica of the v002 feature family (90-day stub parquets + sidecars + manifest + sidecar + upstream lineage stubs) inside a pytest `tmp_path`.
- `test_multiday_feature_gate_io.py` — 12 tests covering canonical sidecar format, path discipline, gate-report-id derivation, atomic write + refuse-to-overwrite, SHA helpers, JSON parsing rejection.
- `test_multiday_feature_gate_report.py` — 9 tests covering verdict classification (PASS / FAIL / INDETERMINATE / NOT_APPLICABLE), required report fields, fail-verdict path, hard-invariant enforcement.
- `test_multiday_feature_gate_checks.py` — 18 tests covering CHECK_ORDER stability (50 in canonical order); SAMPLE_DATES; expected locked constants; per-group spot checks (C5/C6/C7/D1/D2/B7/B8/G1/G2/G3); full-suite end-to-end against the synthetic fixture (verifies 50 results returned in canonical order; G-group all PASS).
- `test_multiday_feature_gate.py` — 9 tests covering orchestrator returns 50 results; atomic report + canonical sidecar write; refuse-to-overwrite; orchestrator rejects non-Path input; FAIL fixture for missing manifest, noncanonical sidecar, per-day SHA mismatch, row-count mismatch, forbidden column, research_eligible=True; INDETERMINATE fixture for missing lineage artefact (ERROR conversion).
- `test_multiday_feature_gate_no_network.py` — 6 parametrized tests scanning the 4 new source modules + the orchestrator script for forbidden imports (`prometheus.runtime`, `prometheus.execution`, `prometheus.persistence`, `requests`, `httpx`, `aiohttp`, `websockets`, `binance`, `dotenv`, `python_dotenv`, `urllib.request`, `urllib3`, `socket`, `os.environ`, `getenv`) and forbidden tokens (`api_key`, `secret`, `signature`, `listenKey`, `userDataStream`, `/fapi/...`, `.env`, `Graphify`, `MCP`, `.mcp.json`).

**Total new tests: 53. All 53 PASS** in 7.86s (`pytest tests/research/microstructure/test_multiday_feature_gate*.py`).

---

## 9. Gate execution command

```text
python scripts/phase4bm_j_run_multiday_feature_gate.py --code-commit-sha 3212722a7ffdd572ac2291ba1500f63f6fad6c59
```

Runtime: <1 s for the 50-check suite (deep-sample reads 6 parquets via pyarrow; metadata-only operations on the other 84; SHA recomputation on the 10 governance artefacts + 90 normalized parquets + 90 feature parquets + 90 feature sidecars). Exit code 0.

---

## 10. Gate report path and SHA256

- **Gate report path:** `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json`
- **Gate report SHA256:** `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`
- **Gate report size:** 16,176 bytes
- **Gate report sidecar path:** `<report>.json.sha256`
- **Gate report sidecar SHA256:** `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`
- **Gate report sidecar size:** 158 bytes
- **Gate report sidecar exact content** (canonical Phase 4bb-F format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`):
  ```text
  3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242  microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json
  ```
  (66 + 92 = 158 bytes; ASCII only; no BOM; LF; exactly two ASCII spaces between SHA and basename; trailing LF.)
- Both artefacts gitignored under `.gitignore:85` (`data/microstructure/`); `git status` does not surface them.

---

## 11. Gate verdict

**FEATURE_GATE_PASS** (overall_status `"pass"`).

---

## 12. Check summary

- **Total checks:** 50
- **PASS:** 50
- **FAIL:** 0
- **ERROR:** 0
- **NOT_APPLICABLE:** 0
- **Blocking failures:** 0

All 50 checks PASS across all 7 groups (A: 12/12, B: 10/10, C: 10/10, D: 6/6, E: 3/3, F: 3/3, G: 6/6).

---

## 13. Local gitignored output summary

Total local gitignored artefacts created by Phase 4bm-J: **2** (gate report + sidecar). Total local gitignored Phase 4bm-H + Phase 4bm-J artefacts under `data/microstructure/`: **184** (90 feature parquets + 90 feature sidecars + 1 feature manifest + 1 feature manifest sidecar + 1 gate report + 1 gate sidecar). **None committed.**

---

## 14. Feature manifest / row count / schema / sidecar / upstream immutability evidence

Re-verified at gate-run time against the Phase 4bm-G / Phase 4bm-H / Phase 4bm-I recorded values (12 / 12 byte-identical):

| Artefact | SHA256 | Status |
| --- | --- | --- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | unchanged |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | unchanged |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged |
| Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged |
| Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | unchanged |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | unchanged |
| Phase 4bm-F v002 successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | unchanged |
| Phase 4bm-F v002 successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | unchanged |

90 / 90 v002 normalized per-day Parquets byte-identical (verified by Group F check F1). The v002 feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false` byte-identically before and after the gate run. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and was **never invoked**.

---

## 15. Quality gate results

- Phase 4bm-J surface `ruff check` (11 paths covering modules, script, tests, fixture): **All checks passed!**
- Whole-repo `ruff check .`: **All checks passed!** (after a few line-length suppressions in tests/fixture/checks/report files where v002 SHA literals + lineage column names are inherently long; suppressed per-file via `# ruff: noqa: E501`).
- `pytest tests/research/microstructure/test_multiday_feature_gate*.py`: **53 passed in 7.86s**.
- mypy skipped at this phase per the Phase 4bm-H baseline rationale (`mypy src/prometheus`: 29 errors in 5 files; Phase 4bm-J adds new modules of similar shape — the per-module `_Ctx`/`_Res` type aliases keep the checks module narrow; no new error category is expected; `# ruff: noqa: E501` does not affect mypy).
- Whole-repo `pytest` skipped per the Phase 4bm-H baseline rationale (15 collection errors from missing `httpx`/`duckdb` env modules + 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py`; both baselines are unchanged by Phase 4bm-J because it modifies no existing code).

---

## 16. Skipped checks and rationale

- Phase 4bm-H feature recomputation: **not run.** Phase 4bm-J is read-only over the Phase 4bm-H outputs; the orchestrator script's refuse-to-overwrite policy would block any rerun. The Phase 4bm-H prior real-run result is the authoritative reference.
- Full whole-repo `pytest`: skipped; Phase 4bm-H baseline preserved by construction (no code regression possible because the 4bm-J modules are new and modify no existing module beyond `__init__.py` re-exports).
- mypy whole-package: skipped at merge time; the new 4bm-J modules follow the same idioms as the v001 / 4bm-H baselines, no new mypy category expected.

These skips conform to the project's standing precedent for Tier 1 code-and-gate-report phases that produce a single deterministic gate output (Phase 4bm-D multi-day derived gate; Phase 4bi-B v001 feature gate).

---

## 17. What this gate proves

- The Phase 4bm-H v002 feature artefacts are structurally consistent with the Phase 4bm-G feature-boundary design **at report level**.
- All 12 v002 governance / lineage artefacts remain byte-identical pre- and post-gate.
- The v002 feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false`.
- The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end.
- The 62-column canonical schema is identical across all 90 per-day parquets (pyarrow `read_schema` on every file confirms 0 diffs).
- Per-day feature row counts match the source normalized event counts byte-for-byte (90/90 days).
- The Phase 4bm-G §13 forbidden-substring detector finds 0 hits.

---

## 18. What this gate does not prove

- That any v002 feature has statistical / predictive value for any research question.
- That feature-family research-use is admissible (separate decision phase required — Phase 4bm-K analogue).
- That successor-state recording is admissible (separate phase required).
- That labels, diagnostics, ML, strategy, or backtests are admissible.
- That any retained verdict may be revisited.
- That any project lock may be loosened.
- That paper / shadow / live / exchange-write may begin.

---

## 19. Non-authorization

Phase 4bm-J does **not**, and **cannot**, authorize:

- **Phase 4bm-K — Multi-Day V002 Feature-Family Research-Use Decision Memo** (the canonical conditional successor; multi-day analogue of Phase 4bi-C);
- v002 feature-family research-use decision;
- v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D);
- any multi-day v002 label-family phase;
- any multi-day v002 chronological-split-policy memo;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy implementation, signal construction;
- backtest implementation or execution;
- additional acquisition;
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
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, Phase 4bm-H feature computation, or Phase 4bm-I structural QA verdict;
- amending the Phase 4bm-J gate verdict;
- any successor phase whatsoever.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN** (no prior gate is rerun; this is the first v002 feature-family gate), **N-SUCCESSOR-STATE**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**. **N-DERIVATION** does NOT apply — Phase 4bm-J reads existing derived/feature outputs but does not normalize/derive/compute features/labels.

---

## 20. Recommended state

**Remain paused.**

Phase 4bm-J is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

The v002 multi-day derived family now carries a complete ladder of evidence through v002 Feature Stage-4 at report level:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3: Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts.
- v002 Feature Stage-3: Phase 4bm-I FEATURE_STRUCTURAL_QA_PASS.
- **v002 Feature Stage-4 (eligibility-gate-passed at report level)**: Phase 4bm-J **FEATURE_GATE_PASS** (this phase).

v002 Feature Stage-5 (research-use-cleared), Stage-6 (successor-state-marked), and overall Stage-4 (feature-cleared on the manifest) remain **unauthorized**.

---

## 21. Conditional next options, none authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | n/a | **recommended** |
| Future **Phase 4bm-K — Multi-Day V002 Feature-Family Research-Use Decision Memo** (multi-day analogue of Phase 4bi-C) | docs-only | **NOT authorized by this phase** |
| Future v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D) | docs + local gitignored successor-state JSON | **NOT authorized by this phase** |
| Multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by this phase** |
| Additional acquisition / cross-symbol / mark-price / order-book / funding / OI / liquidation / cross-venue | docs + data | **NOT authorized by this phase** |
| Diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this phase** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this phase** |

**No successor phase is authorized by Phase 4bm-J.**
