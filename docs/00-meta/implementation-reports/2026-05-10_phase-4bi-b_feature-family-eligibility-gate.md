# Phase 4bi-B — Feature-Family Eligibility-Gate Design + Implementation + Execution

## Phase header

- **Phase id:** 4bi-B
- **Type:** code + docs + local gitignored gate-report execution
- **Branch:** `phase-4bi-b/feature-family-eligibility-gate`
- **Base:** `main` at `2bc026b4e0d9702d1cf80130282bf8dacab70901` (Phase 4bi-A merge-closeout commit; merge commit ancestor `97f9d760698d89900fb4c43d57c7bbc559c8a52e`)
- **Dataset family inspected:** `microstructure_features_aggtrades_v001`
- **Symbol / date:** `BTCUSDT` / `2025-01-15`
- **Code commit SHA recorded inside outputs:** `2bc026b4e0d9702d1cf80130282bf8dacab70901`

## Current state

Phase 4bi-A (Feature Artefact Structural QA Memo, read-only) is merged to `main`. The Phase 4bh feature parquet, feature parquet sidecar, feature manifest, and feature manifest sidecar exist locally under the gitignored `data/microstructure/` tree. Feature Stage-1 implementation is merged. Feature Stage-2 local artefacts exist with manifest. Feature Stage-3 was reached at memo level by Phase 4bi-A (structural QA on the local one-day artefact). Feature Stage-4 (feature-family eligibility-gate-passed) and Stage-5 (research-use / ML-use decision) have **not** been reached. No labels, targets, signals, ML, strategy, backtests, or acquisition are authorised.

## Inputs reviewed

- Phase 4bh feature parquet (`618d9b86…`; 224,382,279 B; 1,681,098 rows; 61 columns).
- Phase 4bh feature manifest (`624e8c5e…`; 3,851 B).
- Paired SHA256 sidecars for both.
- Source normalized parquet (`2b3d6978…`).
- Source normalized manifest (`f6f0d947…`).
- Raw manifest (`a371edd4…`).
- Phase 4bb-D raw gate report (`96f09159…`).
- Phase 4bf derived gate report (`dd4e0c1c…`).
- Phase 4bg-B successor-state JSON (`8bcc7d01…`).
- Phase 4bh `validate_feature_dataset` (read-only re-run during Phase 4bi-B; 135/135 PASS).
- Phase 4bh-B locked feature schema contract (`FEATURE_SCHEMA_V001`, 61 columns; `FEATURE_NAMES_V001`, 45 names; `FEATURE_WINDOWS_MS_V001 = (1000, 5000, 15000, 60000)`; `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS`, 26 substrings).
- Phase 4bh, Phase 4bi-A merge-closeout files.

The raw zip, Phase 4bb-D gate report, Phase 4bf gate report, and Phase 4bg-B successor-state JSON were SHA-verified only — never used as feature data.

## Scope

- Implement the offline Phase 4bi-B feature-family eligibility gate.
- Run the gate exactly once against the on-disk Phase 4bh artefacts.
- Emit one local gitignored gate report JSON plus paired SHA256 sidecar under `data/microstructure/gate-reports/features/`.
- Reach Feature Stage-4 only at **report level**; never flip the on-disk feature manifest's `research_eligible` flag, never transition `eligibility_gate_status`, never imply Stage-5 research-use / ML-use.

## Non-scope

- Do **not** acquire or modify any data.
- Do **not** call public, private, authenticated, or WebSocket endpoints.
- Do **not** read or create credentials, `.env`, `.mcp.json`, or invoke MCP / Graphify.
- Do **not** rerun the normalizer, raw eligibility gate, derived-family gate, or feature kernel.
- Do **not** mutate any source artefact, sidecar, manifest, or successor-state file.
- Do **not** create labels, targets, signals, ML, strategy, or backtest artefacts.
- Do **not** authorise any successor phase.
- Do **not** revise retained verdicts, change project locks, or amend M0.

## Phase 4bi-A dependency

Phase 4bi-A's read-only structural QA over the same artefacts produced 67 explicit checks PASS, 18 causal spot-checks PASS, same-timestamp tie-break PASS, and `validate_feature_dataset` 135/135 PASS. Phase 4bi-B re-runs `validate_feature_dataset` independently and adds the report-level Phase 4bi-B check suite that converts the structural evidence into stable feature-family gate checks with their own IDs.

## Gate design objective

Convert the existing Phase 4bh / Phase 4bi-A evidence into a deterministic, stable, atomic, refuse-overwrite gate report that records exactly one Feature Stage-4 report-level outcome for the locked one-day BTCUSDT 2025-01-15 feature artefact, while preserving every retained verdict and project lock.

## Gate implementation summary

Four new offline-only modules under `src/prometheus/research/microstructure/`:

- **`feature_gate_io.py`** — read-only artefact loaders, path discipline (`data/microstructure/gate-reports/features/`), atomic JSON writer, paired-SHA256 sidecar writer, refuse-overwrite, no networking imports, no env reads.
- **`feature_gate_report.py`** — `FeatureGateReport` frozen data model + `build_feature_gate_report` + `write_feature_gate_report`. Hard-locks `research_eligible_after = False`, `feature_manifest_research_eligible_after = False`, `feature_manifest_eligibility_gate_status_after = "pending"`, `stage_5_authorized = False`, `stage_5_research_or_ml_use = False`, `no_successor_authorization = True`. Refuses to write if any of those invariants is mutated.
- **`feature_gate_checks.py`** — 70 stable check functions grouped A..N, `FeatureGateCheckStatus` (PASS / FAIL / NOT_APPLICABLE / ERROR), `FeatureGateCheckResult`, `FeatureGateContext`, `CHECK_ORDER`, `run_all_checks`. Calls only pyarrow + numpy + stdlib + a `subprocess` invocation of `git check-ignore -q` for Group B path-discipline checks.
- **`feature_gate.py`** — `FeatureGateInput`, `FeatureGateResult`, `validate_feature_gate_inputs`, `run_feature_family_gate`. Calls `validate_feature_dataset` once for Group L cross-evidence. Builds and writes the report under `data/microstructure/gate-reports/features/`.

Plus a narrow `__init__.py` re-export update.

## Source files added / modified

Added (tracked in git):

- `src/prometheus/research/microstructure/feature_gate_io.py`
- `src/prometheus/research/microstructure/feature_gate_report.py`
- `src/prometheus/research/microstructure/feature_gate_checks.py`
- `src/prometheus/research/microstructure/feature_gate.py`

Modified narrowly:

- `src/prometheus/research/microstructure/__init__.py` — re-export 14 new public symbols + extend the package docstring with a Phase 4bi-B section.

## Test files added / modified

Added (tracked in git):

- `tests/research/microstructure/_feature_gate_fixtures.py` (shared mini-fixture builder)
- `tests/research/microstructure/test_feature_gate_io.py` (18 tests)
- `tests/research/microstructure/test_feature_gate_report.py` (6 tests)
- `tests/research/microstructure/test_feature_gate_checks.py` (31 tests)
- `tests/research/microstructure/test_feature_gate.py` (7 tests)
- `tests/research/microstructure/test_feature_gate_no_network.py` (15 tests)

Total: 77 new tests.

## Public API implemented

Re-exported from `prometheus.research.microstructure`:

- `FeatureGateError`
- `FeatureGateIOError`
- `FeatureGateReportError`
- `FeatureGateCheckStatus`
- `FeatureGateCheckResult`
- `FeatureGateContext`
- `FeatureGateReport`
- `FeatureGateReportPaths`
- `FeatureGateInput`
- `FeatureGateResult`
- `build_feature_gate_report`
- `run_feature_family_gate`
- `write_feature_gate_report`
- `validate_feature_gate_inputs`

## Gate report schema

The report JSON includes (exact JSON keys, sorted alphabetically when serialised):

- `report_schema_version` = `v001`
- `phase_id` = `4bi-B`
- `report_id`, `created_at_unix_ms` (via `generated_at_unix_ms`), `code_commit_sha`
- `dataset_family`, `dataset_version`, `feature_schema_version`, `symbol`, `utc_date`
- `input_artefacts` (paths + SHAs of every read-only input + Phase 4bh / Phase 4bi-A merge commits)
- `expected_row_count`, `observed_row_count`
- `expected_schema_columns`, `observed_schema_columns`
- `expected_feature_columns`, `observed_feature_columns`
- `expected_lineage_columns`, `observed_lineage_columns`
- `feature_config_hash` (= `49b4ec1f…571f0c77`)
- `checks` (ordered tuple of 70 stable check results), plus the four counters
- `boundary_confirmations`
- `overall_status`
- `research_eligible_before` / `research_eligible_after`
- `eligibility_gate_status_before` / `eligibility_gate_status_after`
- `feature_manifest_research_eligible_after` (invariant `false`)
- `feature_manifest_eligibility_gate_status_after` (invariant `"pending"`)
- `stage_5_authorized` (invariant `false`)
- `stage_5_research_or_ml_use` (invariant `false`)
- `no_successor_authorization` (invariant `true`)
- `measured_summary` (pre/post SHAs of every input + validate_feature_dataset evidence)

## Gate check taxonomy

Stable IDs `4bi-b.<group><nn>`. Total: **70 checks** in this version.

| Group | IDs | Coverage |
| ----- | --- | -------- |
| A | A01..A07 (7) | Artefact presence (feature parquet, sidecar, feature manifest, sidecar, normalized parquet, normalized manifest, raw manifest) |
| B | B01..B04 (4) | Gitignore / tracked-file boundary (microstructure, features, manifests, gate-reports/features) |
| C | C01..C10 (10) | Feature manifest governance (dataset_family, dataset_version, feature_schema_version, symbol, utc_date, row_count, invalid_windows, research_eligible, eligibility_gate_status, governance labels) |
| D | D01..D09 (9) | Schema / column-order / feature-list (61-column count, canonical order, 45 features, 16 lineage, feature_list, window_list, window_ms_list, no forbidden substrings, deferred 30s/5m absent) |
| E | E01..E05 (5) | Row-count / identity / timestamp-alignment (1,681,098 rows, contiguous row_index, agg_trade_id parity, transact_time parity, feature_timestamp_ms == source_transact_time_ms) |
| F | F01..F06 (6) | Lineage hash (feature parquet SHA, sidecar match, feature manifest SHA, sidecar match, feature_config_hash, lineage SHA columns constant + match) |
| G | G01..G07 (7) | Dtype / null / Decimal / float sanity (count int64 ≥ 0, Decimal columns parse, ratio in [0,1], log-return finite, utc_hour, utc_minute, milliseconds_since_day_start) |
| H | H01..H02 (2) | Quality flags (`invalid_window_flag` / `rolling_missing_window_flag` strict bool, all false) |
| I | I01..I04 (4) | Causal spot-check evidence (first-row no-prior-reference; last-row identity; rolling_aggtrade_count_1s spot-checks; rolling_aggtrade_count_60s spot-checks) |
| J | J01 (1) | Same-timestamp tie-break evidence |
| K | K01..K07 (7) | Upstream immutability (normalized parquet/manifest/raw manifest/raw zip/Phase 4bb-D/Phase 4bf/Phase 4bg-B SHAs) |
| L | L01..L04 (4) | Forbidden-output and no-rescue (raw / derived manifest state preserved, feature manifest boundary confirmations, validate_feature_dataset PASS) |
| M | M01..M03 (3) | Stage interpretation (`research_eligible_after` False, `eligibility_gate_status_after` pending, `stage_5_research_or_ml_use` False) |
| N | N01 (1) | Boundary confirmations (every required key present in feature manifest) |

## Real Phase 4bi-B gate execution result

- **Overall status:** `pass`
- **Checks total:** 70
- **PASS / FAIL / ERROR / NOT_APPLICABLE:** 70 / 0 / 0 / 0
- **Validation evidence:** `validate_feature_dataset` overall_status = `pass`; `validate_failed_checks = []`.
- **Boundary confirmations:** all 17 keys `true`.
- **Result invariants:** `research_eligible_after = False`, `feature_manifest_research_eligible_after = False`, `feature_manifest_eligibility_gate_status_after = "pending"`, `stage_5_authorized = False`, `stage_5_research_or_ml_use = False`, `no_successor_authorization = True`.

## Local gitignored gate report artefacts (NOT committed)

- **Report path:** `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v001__phase-4bi-b__1778436978312__2bc026b4e0d9.json`
- **Report SHA256:** `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`
- **Report size:** 30,696 bytes
- **Sidecar path:** same with `.sha256` suffix
- **Sidecar size:** 158 bytes (matches recomputed bytes)
- **Report id:** `microstructure_features_aggtrades_v001__v001__phase-4bi-b__1778436978312__2bc026b4e0d9`
- **Created at:** `1778436978312` (Unix ms)

`git check-ignore -v` confirms both files are gitignored under `.gitignore:85: data/microstructure/`.

## Validation evidence

- Whole-repo `ruff check .` — `All checks passed!`
- `pytest tests/research/microstructure/` — **666 passed** (Phase 4aw 114 + Phase 4ax 47 + Phase 4az 35 + Phase 4bb-C 62 + Phase 4bd 71 + Phase 4bf 155 + Phase 4bh 97 + Phase 4bi-B 77, with cross-phase shared `_features_fixtures.py` reused by Phase 4bi-B's gate fixture).
- Whole-repo `pytest` — **1449 passed, 2 failed** (the same pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py`; no new regressions from Phase 4bi-B).
- Whole-repo `mypy src/prometheus` — `Success: no issues found in 110 source files` (was 106 prior to Phase 4bi-B; +4 new modules).
- `git diff --check` — clean.

## Hash and immutability evidence

All 9 upstream artefacts byte-for-byte identical pre/post the Phase 4bi-B run:

| Artefact | SHA256 |
| --- | --- |
| Feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| Normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Normalized (original derived) manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B successor-state | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

## Boundary confirmations

All Phase 4bi-B boundary confirmations are `true` on the report:

- `no_feature_manifest_mutation`
- `no_source_artefact_mutation`
- `no_data_microstructure_write_outside_gate_reports_features`
- `no_label_computed`
- `no_signal_computed`
- `no_ml_trained`
- `no_strategy_created`
- `no_backtest_run`
- `no_acquisition`
- `no_network_io`
- `no_websocket`
- `no_credential_read`
- `no_env_read`
- `no_mcp_or_graphify`
- `feature_manifest_research_eligible_after_is_false`
- `stage_5_research_or_ml_use_is_false`
- `no_successor_authorization`

## Feature-stage interpretation

Phase 4bi-B reaches **Feature Stage-4 at the report level only** for the locked one-day BTCUSDT 2025-01-15 artefact. The on-disk feature manifest still carries `research_eligible = false` and `eligibility_gate_status = pending`, and Phase 4aw's `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant was preserved end-to-end. Stage-5 (research-use / ML-use decision) is **not** reached.

## What this phase proves

- The Phase 4bh feature artefacts conform exactly to the Phase 4bh-B locked schema and Phase 4bh implementation contract on the locked one-day BTCUSDT 2025-01-15 cell.
- The artefacts pass an independent, stable, ID'd 70-check feature-family eligibility-gate suite that aggregates Phase 4bh kernel evidence, Phase 4bi-A structural-QA evidence, and `validate_feature_dataset` cross-evidence into one atomic, refuse-overwrite report.
- The report's invariants prevent the very mutations that would otherwise let the report be misread as Stage-5 authorisation.

## What this phase does not prove

- Stage-5 research-use / ML-use approval — explicitly NOT reached.
- Edge, alpha, predictiveness, signal quality, profitability — none claimed; none computable; none authorised.
- Multi-day / multi-symbol generalisation — out of scope; the gate operates on the single locked one-day BTCUSDT artefact.
- Future feature-family extensions (additional windows, additional features, mark-price columns, OI columns) — none authorised.

## Preserved boundaries

- Retained verdict ledger: H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure — all preserved verbatim.
- Project locks: §11.6 (8 bps per side); §1.7.3 (0.25% / 2× / one-position / mark-price stops); Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al refined no-rescue; Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A..E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B, 4bh-A, 4bh-B, 4bh, 4bi-A — all preserved verbatim.
- M0 governance: untouched.
- 5m research thread: closed (Phase 3t).

## Recommended future options

- **Primary:** remain paused.
- **Conditional next (NOT authorised by this phase):** Phase 4bi-C — Feature-Family Research-Use / ML-Use Decision Memo (docs-only).
- **Conditional cleanup (NOT authorised):** Phase 4bb-F — Gate Report Output Path Hygiene (a previous derived-family run produced a doubled `gate-reports/gate-reports/` segment under the normalized namespace; the Phase 4bi-B namespace is `gate-reports/features/` and is unaffected).
- **Conditional raw policy marker (NOT authorised):** Phase 4bb-G — Raw Manifest Successor-State Recording.
- **Conditional later (NOT authorised; would require Stage-5 first):** Phase 4bi-D — Feature-Family Successor-State Recording.
- **Conditional fallback (NOT authorised):** Phase 4bh-C — Feature Schema Finalization Review / Red-Team Memo.

## Closeout / lock preservation

- No source artefact, sidecar, manifest, or successor-state file was mutated.
- No labels, targets, signals, ML, strategy, or backtest artefacts created.
- No data acquired.
- No public, private, authenticated, or WebSocket endpoints called.
- No credentials, `.env`, `.mcp.json`, MCP, or Graphify referenced.
- No retained verdict revised.
- No project lock loosened.
- No M0 amendment.
- No successor authorised.
- Recommended state: **remain paused.**
