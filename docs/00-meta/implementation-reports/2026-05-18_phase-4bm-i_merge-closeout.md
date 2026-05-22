# Phase 4bm-I Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-I — Multi-Day V002 Feature Artefact Structural QA Memo
- **Tier**: **Tier 1 — Full Phase** per the v001 Phase 4bi-A structural QA precedent and `docs/00-meta/process/phase-risk-tiering-standard.md` §3 hierarchy (first-of-kind QA of admissibility-relevant evidence).
- **Type**: docs-only + read-only local artefact analysis — adds two new tracked docs files under `docs/00-meta/implementation-reports/` and narrowly updates `docs/00-meta/current-project-state.md`. No source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified; no `data/microstructure/` artefact is created, modified, or deleted; no v002 feature artefact is regenerated.
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-I as project-complete on `main` after a clean docs-only + read-only QA branch that verifies the Phase 4bm-H v002 feature artefacts against the Phase 4bm-G feature-boundary design, the Phase 4bm-H implementation result, and the Phase 4bm-H merge-closeout evidence. Phase 4bm-I reaches **v002 Feature Stage-3 (structurally QA-passed)** at the memo level.
- **Branch merged**: `phase-4bm-i/multi-day-v002-feature-artefact-structural-qa-memo`
- **Target branch**: `main`
- **Base**: `main` at `0106321f6e9dc9d028739ecf89ee3ded6867862a` (Phase 4bm-H merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-H (Multi-Day V002 Feature Schema / Feature Computation Implementation; project-complete on `main`)
- **Direct v001 precedent**: Phase 4bi-A (v001 feature artefact structural QA memo)

**Phase 4bm-I is read-only structural QA + docs.** **No v002 feature artefact was regenerated.** **No upstream artefact was mutated.** **No data/microstructure file was committed.** **Phase 4bm-J is not authorized by Phase 4bm-I.** **Stage-4 / feature-family eligibility gate / research-use / successor-state / labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-I.** **Structural QA verdict: FEATURE_STRUCTURAL_QA_PASS.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-I is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `0106321f6e9dc9d028739ecf89ee3ded6867862a`
- **Pre-merge `origin/main` SHA**: `0106321f6e9dc9d028739ecf89ee3ded6867862a` (in sync; verified via `git rev-parse`)
- **Phase 4bm-I branch commit 1 SHA**: `1896cc7` (`docs(phase-4bm-i): add multi-day v002 feature artefact structural qa memo`; 2 files / +943; the 24-section main QA memo + the `current-project-state.md` narrative paragraph and Current phase block update)
- **Phase 4bm-I branch commit 2 SHA**: `b9406bf` (`docs(phase-4bm-i): add closeout`; 1 file / +132; the Phase 4bm-I closeout)
- **Phase 4bm-I branch tip SHA pre-merge**: `b9406bfdb51d44f0e61bcfc839c3d6218fa987b6`
- **Merge commit SHA**: `759b32bdf614d306c9485474555838528aa3c0ac`
- **Merge commit message**: `docs(phase-4bm-i): merge multi-day v002 feature artefact structural qa memo`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `759b32bdf614d306c9485474555838528aa3c0ac`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `759b32bdf614d306c9485474555838528aa3c0ac` (in sync; pushed cleanly via `0106321..759b32b  main -> main`; no force, no skip-hooks, no skip-signing)
- **Merge-closeout commit SHA**: recorded by the next commit (this file; `docs(phase-4bm-i): add merge closeout`)
- **Post-merge-closeout-commit `main` SHA**: recorded by the next commit
- **Post-merge-closeout-commit `origin/main` SHA**: recorded by the next commit
- **Final `main == origin/main` after closeout push**: recorded by the next commit

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-i/multi-day-v002-feature-artefact-structural-qa-memo -m "docs(phase-4bm-i): merge multi-day v002 feature artefact structural qa memo"`
- **Strategy**: `ort` (git default)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     0106321..759b32b  main -> main
  ```
  Second push (this merge-closeout commit) output: recorded by the next commit.

## §4 Files Brought Forward by the Merge

Three tracked files brought forward from the Phase 4bm-I branch into `main`, across the two source-branch commits (`1896cc7` memo + state, `b9406bf` closeout).

**Tracked docs files added (2):**

1. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-i_multi-day-v002-feature-artefact-structural-qa-memo.md` (NEW, +588; the 24-section main structural QA memo).
2. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-i_closeout.md` (NEW, +132; the 12-section Phase 4bm-I closeout).

**Tracked docs files modified narrowly (1):**

3. `docs/00-meta/current-project-state.md` (MODIFIED, +355; new Phase 4bm-I narrative paragraph appended before the Phase 4bm-H paragraph + new "Current phase:" block + preserved labelled historical Phase 4bm-H "Current phase:" block; prior Phase 4bm-H content preserved verbatim as historical context).

**No** source / test / script / configuration file is modified by this merge. **No** `data/microstructure/` artefact is committed by this merge. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, and every other tracked file outside the above 3-file set are unchanged.

## §5 Diff Summary

`git diff --stat 0106321..759b32b` (against pre-merge `main`):

```text
 docs/00-meta/current-project-state.md              | 355 +++++++++++++
 .../2026-05-18_phase-4bm-i_closeout.md             | 132 +++++
 ...day-v002-feature-artefact-structural-qa-memo.md | 588 +++++++++++++++++++++
 3 files changed, 1075 insertions(+)
```

No deletions. No `data/microstructure/` path appears. `git diff --check` produces no whitespace or conflict marker findings.

## §6 Result / Verdict

**Phase 4bm-I is project-complete on `main`.** The v002 multi-day derived family now carries a complete Phase 4ba 5-stage ladder of evidence through Stage-3 plus a complete v002 Feature Stage-2 (computed) + **v002 Feature Stage-3 (structurally QA-passed)** marker via this memo:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3: Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts (90 per-day Parquets + 90 sidecars + 1 manifest + 1 manifest sidecar; 155,153,449 rows; all local gitignored).
- v002 **Feature Stage-3 (structurally QA-passed)**: Phase 4bm-I (this phase) — read-only structural QA verdict **FEATURE_STRUCTURAL_QA_PASS**.

v002 Feature Stage-4 (eligibility-gate-passed), Stage-5 (research-use-cleared), Stage-6 (successor-state-marked), and overall Stage-4 (feature-cleared on the manifest) remain **unauthorized**. The recommended state is **remain paused**.

## §7 Local Gitignored Outputs (inspected, NOT modified)

Phase 4bm-I inspected the existing **182 local gitignored Phase 4bm-H artefacts** on disk in read-only mode. **None were modified.** All four representative paths are gitignored under `.gitignore:85` (`data/microstructure/`); `git status` does not surface any of them.

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
- **feature_config_hash**: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`
- **feature parquet count**: 90 (one per UTC date 2024-12-01 .. 2025-02-28 inclusive)
- **feature sidecar count**: 90 (one per parquet, canonical Phase 4bb-F format)
- **total feature row count**: **155,153,449** (1:1 parity with Phase 4bm-B v002 normalized event count)
- **date range**: 2024-12-01 .. 2025-02-28 (90 contiguous UTC days)
- **symbol**: BTCUSDT
- **feature parquet output directory tree**: `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`

Confirmation: `git check-ignore -v data/microstructure/`, `data/microstructure/features/`, the manifest path, and the manifest sidecar path all return `.gitignore:85:data/microstructure/`.

## §8 Structural QA Evidence Summary

**A. Inventory (PASS)** — 90 / 90 feature Parquets present; 90 / 90 sidecars present; manifest present (85,929 B); manifest sidecar present (116 B); date inventory exactly 2024-12-01..2025-02-28 (90 contiguous days); symbol subdir exactly `["BTCUSDT"]`.

**C. Manifest SHA / sidecar (PASS)** — recomputed manifest SHA `512a0a54…` matches expected; sidecar SHA `22e2fb77…` matches expected; sidecar canonical Phase 4bb-F format byte-verified (66 hex + two ASCII spaces + 50-byte basename + LF; no CRLF; no BOM); manifest JSON parses cleanly; 90 unique `per_day_outputs` dates.

**D. Manifest content (PASS)** — all 32 content invariants match (dataset_family, dataset_version=v002, feature_schema_version=v001, source_dataset_family, source_dataset_version=v002, source_successor_state_sha256=`72b6edd4…`, source_phase_4bm_d_gate_report_sha256=`3b45e70b…`, source_phase_4bm_e_outcome="Option B / Decision form 2", feature_config_hash=`819cfa7a…`, input_date_start=2024-12-01, input_date_end=2025-02-28, date_count=90, symbol=BTCUSDT, expected_event_count=155153449, actual_feature_row_count=155153449, research_eligible=false, eligibility_gate_status="pending", stage_4_feature_cleared=false, 8 non-authorization flags all false, 5 immutability flags all true, 18 / 18 boundary confirmations all true).

**E. Schema (PASS)** — 62 columns total = 17 lineage + 45 feature/quality; `feature_column_names` matches the canonical 62-column tuple in exact order; `feature_dtypes` covers all 62 columns (set equality is exact; `len == 62`); `feature_windows_ms == [1000, 5000, 15000, 60000]`; `feature_window_labels == ["1s", "5s", "15s", "60s"]`; **Phase 4bm-G §13 forbidden-substring detector: 0 hits across the 62-column schema**; safe `source_phase_4bm_e_outcome` lineage column present; unsafe `source_phase_4bm_e_decision` absent; manifest `forbidden_substring_detector_tokens` length = 26.

**F. Row counts (PASS)** — `sum(per_day_outputs.row_count) == 155,153,449` exactly; per-day feature row count == source normalized event count for all 90 days (0 mismatches); no zero-row day; no duplicate dates; **all 90 per-day feature Parquet SHA256 values recomputed on disk match the manifest's `per_day_outputs[i].feature_parquet_sha256` byte-for-byte** (0 mismatches across 90 files).

**G. Sidecars (PASS)** — all 90 paired sidecars canonical Phase 4bb-F format (two ASCII spaces, LF, no CRLF, no BOM); all 90 sidecar embedded SHA values match the corresponding feature parquet SHA; all 90 sidecar SHA256 values match the manifest's `per_day_outputs[i].feature_sidecar_sha256`. 0 violations.

**H. Partition / timestamp structural (PASS)** — pyarrow `read_schema` confirms all 90 parquets have the identical canonical 62-column schema (0 schema diffs); pyarrow `ParquetFile.metadata.num_rows` matches manifest row counts on every day (0 mismatches). Deep sample of 6 representative dates (day 1 `2024-12-01`, last-day-of-each-month, day 90 `2025-02-28`) confirms canonical column order; `symbol` / `utc_date` / `dataset_version` / `source_dataset_version` / `feature_schema_version` / lineage SHA columns constant per-day; `row_index` 0..n-1 contiguous and strictly increasing by 1; `feature_timestamp_ms` monotonic non-decreasing; `feature_timestamp_ms == source_transact_time_ms` (event-aligned per Phase 4bm-G §14); all rows in half-open `[day_start_ms, day_end_ms)`.

**I. Quality flags / cross-day boundary (PASS)** — day 1 (2024-12-01) `rolling_missing_window_flag` rule (`(T - 60_000) < day_start_ms`) is correctly applied to 384 rows in the first 60 seconds; remaining day-1 rows carry False; days 2..90 sampled (`2024-12-31`, `2025-01-15`, `2025-01-31`, `2025-02-15`, `2025-02-28`) all carry `rolling_missing_window_flag = False` (causal cross-day lookback fully populates the windows); per-event `invalid_window_flag = False` everywhere (Phase 4bm-D `invalid_windows = []`).

**E.9–E.11 Forbidden-column / non-label (PASS)** — schema check finds 0 hits across the 62-column list against the Phase 4bm-G §13 26-token list (`label, target, future, signal, entry, exit, pnl, profit, loss, mfe, mae, r_multiple, equity, position, alpha, edge, prediction, model, score, decision, strategy, liquidation, funding, open_interest, order_book, mark_price`); the unsafe `source_phase_4bm_e_decision` column is not present anywhere; the safe `source_phase_4bm_e_outcome` column carries the literal value `"Option B / Decision form 2"` verbatim. **Implication**: no feature column implies labels, targets, signals, PnL, MFE, MAE, R-multiple, equity, position, alpha, edge, predictions, model scores, strategy decisions, mark-price, order-book, funding, OI, liquidation, or cross-venue data.

**J. Upstream immutability (PASS)** — all 10 v002 governance artefacts (v002 derived manifest + sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-D-R gate report, Phase 4bl-E raw successor-state, Phase 4bm-D gate report + sidecar, Phase 4bm-F successor-state + sidecar) byte-identical pre- and post-QA. All 90 v002 per-day normalized Parquets byte-identical to the v002 derived multi-day index manifest's `per_file_inventory` SHAs (0 mismatches). v001 Phase 4bh single-day feature parquet (SHA `618d9b86…`) and sidecar (SHA `cc880c08…`) byte-identical. v002 derived manifest still `research_eligible = false` / `eligibility_gate_status = "pending"`; v002 raw manifest still `research_eligible = false` / `eligibility_gate_status = "pending"`; Phase 4bm-F successor-state JSON unchanged. Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved end-to-end (never invoked).

**K. Targeted v002 pytest (PASS)** — `pytest tests/research/microstructure/test_features_schema_v002.py test_features_io_v002.py test_features_manifest_v002.py test_features_no_network_v002.py test_features_compute_v002.py`: **89 passed in 3.94s**. All 89 Phase 4bm-H v002 tests still pass.

The single QA-script-level observation (E.5 `feature_dtypes` dict iteration order in the on-disk JSON is alphabetical due to `json.dumps(sort_keys=True)` canonical serialization, while `feature_column_names` preserves canonical order as a JSON list) is intentional and not a defect: every one of the 62 canonical columns has a dtype entry; set equality is exact; the authoritative canonical column order lives in the `feature_column_names` JSON array.

## §9 Manifest State Preservation

| Manifest | Path | `research_eligible` | `eligibility_gate_status` | `stage_4_feature_cleared` | Status |
| --- | --- | --- | --- | --- | --- |
| v002 derived multi-day index manifest | `microstructure_normalized_aggtrades_v001__v002.json` | `false` | `"pending"` | n/a | unchanged |
| v002 raw manifest | `microstructure_raw_aggtrades_v001__v002.json` | `false` | `"pending"` | n/a | unchanged |
| v001 derived manifest | `microstructure_normalized_aggtrades_v001__v001.json` | `false` | `"pending"` | n/a | unchanged |
| v002 feature manifest (Phase 4bm-H; gitignored) | `microstructure_features_aggtrades_v001__v002.json` | `false` | `"pending"` | `false` | unchanged (read-only inspection only) |

The Phase 4bm-F successor-state JSON's `successor_research_eligible = true` continues to be the **only** machine-readable Stage-3 marker for the v002 derived family. The v002 feature manifest cites the Phase 4bm-F successor-state SHA `72b6edd4…` verbatim and never interprets the v002 derived multi-day index manifest alone as Stage-3.

## §10 Upstream Lineage SHA Table

All upstream artefacts are byte-identical pre- and post-Phase-4bm-I. Recomputed SHA256 on disk at merge-time matches the expected value byte-for-byte for every entry below.

| Artefact | SHA256 | Status |
| --- | --- | --- |
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
| Phase 4bh v001 single-day feature parquet (2025-01-15) | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | unchanged |
| Phase 4bh v001 single-day feature sidecar | `cc880c0820f96ad6f45d1fedeeaa3277941cd5c129c946d72639b921854e311c` | unchanged |

90 / 90 v002 normalized per-day Parquets re-hashed and match the v002 derived multi-day index manifest's `per_file_inventory` SHAs byte-for-byte.

## §11 Validation Results

- `git diff --check main..phase-4bm-i/multi-day-v002-feature-artefact-structural-qa-memo` — clean (no whitespace, no conflict markers).
- `git diff main..phase-4bm-i/multi-day-v002-feature-artefact-structural-qa-memo --name-only` — exactly 3 paths (memo, closeout, current-project-state.md); no `data/microstructure/` path.
- `git status --short` after merge — only the two expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); no tracked changes; no `data/microstructure/` artefact visible (gitignored).
- `git check-ignore -v` on all four v002 output paths (`data/microstructure/`, `data/microstructure/features/`, manifest, manifest sidecar) returns `.gitignore:85: data/microstructure/`.

Manifest / sidecar / 90-parquet / 90-sidecar verification (recomputed on disk at merge-time):

- 90 / 90 feature parquets present at expected paths.
- 90 / 90 feature sidecars present at expected paths.
- manifest SHA `512a0a54…` matches expected.
- manifest sidecar SHA `22e2fb77…` matches expected.
- manifest sidecar canonical Phase 4bb-F content byte-verified.
- feature_config_hash `819cfa7a…` matches expected.
- actual_feature_row_count = 155,153,449.
- per_day_outputs length = 90.
- research_eligible = false; eligibility_gate_status = "pending"; stage_4_feature_cleared = false.
- 62-column schema; 0 forbidden token hits; safe `source_phase_4bm_e_outcome` present; unsafe `source_phase_4bm_e_decision` absent.

## §12 Quality Gate Commands and Results

- `git diff --check main..phase-4bm-i/...`: **clean**.
- `pytest tests/research/microstructure/test_features_schema_v002.py test_features_io_v002.py test_features_manifest_v002.py test_features_no_network_v002.py test_features_compute_v002.py`: **89 passed in 3.94s**.

**Skipped checks and rationale**:

- **`mypy src/prometheus`**: skipped. Phase 4bm-I modifies no source code; the Phase 4bm-H baseline (`29 errors in 5 files`; 28 pre-existing v001 / labels / httpx baseline + 8 in `features_compute_v002.py` mirroring the v001 `np.concatenate(([0], ...))` idiom verbatim) is preserved by construction. Re-running mypy would yield identical output and add no audit value.
- **Whole-repo `pytest`**: skipped. Phase 4bm-I modifies no source / test / script / configuration. The Phase 4bm-H baseline (whole-repo `pytest` blocked by 15 pre-existing collection errors from missing `httpx`/`duckdb` env modules + 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py`) is preserved by construction.
- **`ruff check .`**: skipped for the whole repo at merge time. Phase 4bm-I modifies no source; the Phase 4bm-H baseline (`All checks passed!`) is preserved by construction.
- **`scripts/phase4bm_h_compute_multiday_features.py`**: not run. Phase 4bm-I is read-only QA; rerunning the orchestrator would attempt to recompute feature Parquets and would fail closed at the refuse-to-overwrite check (the intended Phase 4bm-G §18(15) fail-closed protection). The Phase 4bm-H prior real-run result is the authoritative reference; Phase 4bm-I verified that result without rerunning.

These skips conform to the project's standing precedent for read-only docs / QA phases (Phase 4bi-A v001 precedent; Phase 4bm-C v002 normalized structural QA precedent; Phase 4bm-G v002 feature-boundary design memo precedent).

## §13 Boundary Statements (required exact phrases)

The following phrases appear verbatim:

- **Phase 4bm-I is read-only structural QA + docs.**
- **No v002 feature artefact was regenerated.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**
- **Phase 4bm-J is not authorized by Phase 4bm-I.**
- **Stage-4 / feature-family eligibility gate / research-use / successor-state / labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-I.**
- **Structural QA verdict: FEATURE_STRUCTURAL_QA_PASS.**

Additional preserved boundaries:

- no tracked data/microstructure artefact changed by this merge;
- no generated feature artefact was committed;
- the original v002 derived manifest is unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- the original v002 raw manifest is unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- the Phase 4bm-F successor-state JSON is unchanged;
- no labels / diagnostics / ML / strategy / backtest / acquisition work was authorized or performed.

## §14 Boundaries Preserved

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..F / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H results — all preserved verbatim.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION** (no normalization / derivation / feature recomputation / label computation; read-only QA only), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

## §15 Recommended State

**Remain paused.**

Phase 4bm-I is project-complete on `main` by this merge + merge-closeout. The operator's broader pause decision continues to apply.

## §16 Conditional Next Options (none authorized)

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | n/a | **recommended** |
| Future **Phase 4bm-J — Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution** (multi-day analogue of Phase 4bi-B) | code + docs + local gitignored gate report | **NOT authorized by this merge** |
| Future v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C) | docs-only | **NOT authorized by this merge** |
| Future v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D) | docs + local gitignored successor-state JSON | **NOT authorized by this merge** |
| Multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by this merge** |
| Additional acquisition (more days / cross-symbol / mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated APIs / private endpoints) | docs + data | **NOT authorized by this merge** |
| Label computation, diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this merge** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this merge** |

## §17 Explicit Non-Authorization

This merge does **not**, and **cannot**, authorize:

- Phase 4bm-J (the canonical successor; the multi-day v002 feature-family eligibility gate);
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
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, or Phase 4bm-H feature computation;
- amending the Phase 4bm-I QA verdict;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.
