# Phase 4bm-N Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-N — Multi-Day V002 Label Schema Finalization Memo
- **Tier**: **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bj-B label-schema precedent. First-of-kind multi-day v002 label-schema finalization; locks future target / label semantics for a Stage-5-admissible feature family and can therefore affect downstream ML admissibility under §3 ("creates features / labels / diagnostics" + "affects eligibility / admissibility / downstream authorization").
- **Type**: docs-only. Three tracked docs files committed (43-section schema-finalization memo + closeout + narrow `current-project-state.md` update). **No** local gitignored output. **No** source / test / script / configuration / data / manifest / sidecar / gate-report / prior-successor-state file modified. **No** `data/microstructure/` artefact created, modified, deleted, renamed, or committed.
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-N as project-complete on `main` after a clean docs-only branch that locks, at memo level only, the exact v002 label schema (40 columns; horizons `{1s, 5s, 15s, 60s}`; forward log returns + strict-sign forward directions; 90-day envelope-terminal censoring), building on Phase 4bm-M's boundary / design memo and the Phase 4bj-B v001 schema-finalization precedent. Phase 4bm-N reaches the **v002 Label Stage-1 (schema finalized at memo level)** layer; no label artefact exists.
- **Branch merged**: `phase-4bm-n/multi-day-v002-label-schema-finalization-memo`
- **Target branch**: `main`
- **Base**: `main` at `e74dc13021900a54153cba81eaed8fdb397fb292` (Phase 4bm-M merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-M (Multi-Day V002 Label-Family Boundary / Design Memo; project-complete on `main`; v002 Label Stage-0 boundary recorded at policy level)
- **Direct v001 precedent**: Phase 4bj-B (v001 label-schema-finalization memo; merged on `main`; selected Outcome 1 — label schema finalized, implementation deferred; 39-column v001 schema)

**Phase 4bm-N is label schema finalization only.** **No label artefact exists after Phase 4bm-N.** **Phase 4bm-O is not authorized by Phase 4bm-N.** **Label computation is not authorized by Phase 4bm-N.** **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-N.** **No feature artefact was modified.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-N is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `e74dc13021900a54153cba81eaed8fdb397fb292`
- **Pre-merge `origin/main` SHA**: `e74dc13021900a54153cba81eaed8fdb397fb292` (in sync; verified)
- **Phase 4bm-N branch commit SHA**: `2bec753909695bff394c91bdac0e23efac2be015` (`docs(phase-4bm-n): add multi-day v002 label schema finalization memo`; 3 docs files / +1709 lines; the schema-finalization memo + closeout + narrow `current-project-state.md` update)
- **Phase 4bm-N branch tip SHA pre-merge**: `2bec753909695bff394c91bdac0e23efac2be015`
- **Merge commit SHA**: `ebae05dc7b9c07a4944d1463c471e642029239f6`
- **Merge commit message**: `docs(phase-4bm-n): merge multi-day v002 label schema finalization memo`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `ebae05dc7b9c07a4944d1463c471e642029239f6`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `ebae05dc7b9c07a4944d1463c471e642029239f6` (in sync; pushed cleanly via `e74dc13..ebae05d  main -> main`; no force, no skip-hooks, no skip-signing)
- **Merge-closeout commit SHA**: to be recorded in §2 immediately after this file is committed and pushed (the SHA-hygiene patch step will replace this placeholder with the concrete value).
- **Post-merge-closeout-commit `main` SHA**: to be recorded after the closeout push.
- **Post-merge-closeout-commit `origin/main` SHA**: to be recorded after the closeout push.
- **Final `main == origin/main` after closeout push**: to be recorded after the closeout push.

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-n/multi-day-v002-label-schema-finalization-memo -m "docs(phase-4bm-n): merge multi-day v002 label schema finalization memo"`
- **Strategy**: `ort` (git default)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     e74dc13..ebae05d  main -> main
  ```
  Second push (this merge-closeout commit) output: to be recorded after the closeout push by the SHA-hygiene patch step.

## §4 Files Brought Forward by the Merge

Three tracked docs files brought forward from the Phase 4bm-N branch into `main`, all from the single source-branch commit (`2bec753`).

**Tracked docs files added (2):**

1. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-n_multi-day-v002-label-schema-finalization-memo.md` (NEW, +948; 43 sections; the main schema-finalization memo — phase identity / scope / non-scope / linkage to Phase 4bm-M Label Stage-0 boundary / linkage to Phase 4bm-L machine-readable v002 Feature Stage-5 marker / linkage to Phase 4bm-K research-use decision / linkage to Phase 4bm-J `FEATURE_GATE_PASS` / linkage to Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS` / linkage to Phase 4bm-H feature artefacts / linkage to Phase 4bj-B v001 precedent with three explicit v002-specific adaptations / evidence table / finalized label-family identity / finalized row model / finalized 40-column schema with canonical order and per-column dtype + nullability / finalized label list / finalized horizon list / finalized forward-reference price policy (multi-day cross-day-allowed; envelope-bounded) / finalized `forward_log_return` natural-log formula / finalized `forward_direction` strict-sign policy / finalized null / censoring policy (multi-day, envelope-bounded) / finalized dtype policy / finalized lineage / identity policy / finalized label manifest schema / finalized label parquet path convention / finalized `label_config_hash` policy / finalized future validation and QA requirements / finalized forbidden outputs / finalized chronological split policy / finalized no-rescue / M0 policy / 27-criterion future implementation acceptance criteria / future v002 label QA / gate sequence / what this phase proves / what this phase does not prove / non-authorization / recommended state / conditional next options / preserved boundaries / validation commands and results / quality gate skipped-check rationale / no source/test/script/config modified / no labels/diagnostics/ML/strategy/backtests / no endpoint/credential/MCP/Graphify/exchange-write / required exact phrases verbatim).
2. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-n_closeout.md` (NEW, +186; 12 sections; closeout summarising branch / base SHA / risk tier / tracked files / local-gitignored-outputs-none / final schema result with v001→v002 delta / key evidence table / validation results / quality gate skipped-check rationale / non-authorization boundaries / recommended state / explicit non-authorization statement / required exact phrases verbatim).

**Tracked docs files modified narrowly (1):**

3. `docs/00-meta/current-project-state.md` (MODIFIED, +575; Phase 4bm-N narrative paragraph + new "Current phase:" block; prior Phase 4bm-M "Current phase:" block preserved as labelled historical context).

**No** `data/microstructure/` artefact is committed by this merge. **No** source / test / script / configuration file outside the above 3-file set is modified. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, and every other tracked file outside the above list are unchanged.

## §5 Diff Summary

`git diff --stat e74dc13..ebae05d` (against pre-merge `main`):

```text
 docs/00-meta/current-project-state.md              | 575 +++++++++++++
 .../2026-05-18_phase-4bm-n_closeout.md             | 186 ++++
 ...ulti-day-v002-label-schema-finalization-memo.md | 948 +++++++++++++++++++++
 3 files changed, 1709 insertions(+)
```

No deletions. No `data/microstructure/` path appears. `git diff --check` produces no whitespace or conflict-marker findings.

## §6 Result / Decision / Outcome Recorded by Phase 4bm-N

**Phase 4bm-N is project-complete on `main`.** **The exact v002 label schema is now finalized at memo level on `main`.** **No label artefact exists.** **No data/microstructure file was committed.**

Specifically:

- **future label-family schema finalized at memo level**: the multi-day v002 label-family schema is locked in writing on `main` and constrains all future v002 label-family implementation work.
- **future label family**: `microstructure_labels_aggtrades_v001 @ v002` (`label_schema_version = "v001"`).
- **finalized column count**: 40 columns per per-day label parquet (17 lineage / identity / metadata + 1 `label_config_hash` + 4 regression labels + 4 classification labels + 12 per-horizon support + 2 global support). v001 → v002 delta = +1 column (added `source_raw_manifest_sha256`; replaced v001's optional per-day `source_normalized_parquet_sha256` with the v002-required `source_normalized_manifest_sha256`).
- **finalized horizons**: `["1s", "5s", "15s", "60s"]` exactly (mirror of Phase 4bj-B v001; widening forbidden).
- **finalized label classes**: 4 × `forward_log_return_<horizon>` (nullable float64; natural-log formula) + 4 × `forward_direction_<horizon>` (nullable int8 in `{-1, 0, 1, null}`, strict-sign threshold at `0.0`, no dead-band).
- **finalized 90-day envelope-terminal censoring policy**: end-of-sample censoring at the v002 envelope's terminal boundary (`envelope_terminal_unix_ms`; the maximum `source_transact_time_ms` across all 90 v002 normalized per-day parquets; corresponds to 2025-02-28 23:59:59.999 UTC at envelope terminus); cross-day horizon lookahead is allowed inside the label kernel only, within the 90-day v002 envelope; anchor row's `utc_date` column records the anchor's date (not the future reference's date).
- **finalized v002-specific multi-day adaptations vs Phase 4bj-B v001 (3 total)**:
  1. lineage SHAs point to v002 multi-day artefacts (Phase 4bm-L successor-state, Phase 4bm-J gate report, v002 feature / normalized / raw manifests) instead of Phase 4bi-* / per-day v001 artefacts;
  2. `source_normalized_manifest_sha256` replaces v001's per-day `source_normalized_parquet_sha256`, and `source_raw_manifest_sha256` is added as new required lineage column;
  3. end-of-sample censoring at the 90-day envelope's terminal boundary rather than per-day censoring.
- **finalized output namespace** (NOT created):
  - per-day label parquets: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet`;
  - label manifest: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`;
  - label gate reports under `data/microstructure/gate-reports/labels/`;
  - sibling label successor-states under `data/microstructure/successor-state/`;
  - paired canonical Phase 4bb-F sidecars throughout.
- **finalized manifest defaults**: `research_eligible = false`, `eligibility_gate_status = "pending"`, `label_family_research_use_authorized = false`, `stage_5_label_cleared = false`, `chronological_split_policy = "not_yet_defined"`, all `governance_labels.*` at default `forbidden` / `unauthorized` / `allowed_by_future_phase_only` values.
- **finalized future implementation acceptance criteria (27 total)** locked at memo level.
- **finalized future structural QA list (22 checks)** locked at memo level (mirror of Phase 4bj-B §22 with v002 multi-day adaptations).
- **symbol scope**: BTCUSDT only (one symbol).
- **date range**: 2024-12-01 through 2025-02-28 inclusive (90 contiguous UTC days; `date_count = 90`).
- **no label schema computation** in Phase 4bm-N.
- **no label artefact created** in Phase 4bm-N.
- **no `data/microstructure/` changes** in Phase 4bm-N.
- **v002 feature manifest unchanged** at SHA256 `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (re-verified on disk at merge time).
- **v002 feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false`** (re-verified on disk at merge time; `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`; `actual_feature_row_count = 155153449`; `symbol = "BTCUSDT"`; `per_day_outputs` length = 90).
- **no manifest mutation** in Phase 4bm-N; **no feature artefact modification** in Phase 4bm-N; **no upstream artefact mutation** in Phase 4bm-N.
- **no Phase 4bm-O authorization**; no successor phase authorized.

The v002 multi-day derived / feature / label-design family now carries a complete ladder of evidence through **v002 Label Stage-1 (schema finalized at memo level)**:

- Stage-0 (derived): Phase 4bm-B normalization.
- Stage-1 (derived inspected): Phase 4bm-C 56/56 structural QA PASS.
- Stage-2 (derived gate-passed at report level): Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision (derived): Phase 4bm-E Option B / Decision form 2.
- Stage-3 (derived successor-state marker): Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0 (design): Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2 (artefacts): Phase 4bm-H computed feature artefacts.
- v002 Feature Stage-3 (inspected): Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`.
- v002 Feature Stage-4 (gate-passed at report level): Phase 4bm-J `FEATURE_GATE_PASS`.
- v002 Feature Stage-5 admissibility decision (policy-level only): Phase 4bm-K Outcome 1 / Decision form 1.
- v002 Feature Stage-5 machine-readable successor-state marker: Phase 4bm-L successor-state JSON SHA `7eccaa8f…`.
- v002 Label Stage-0 (boundary / design at policy level): Phase 4bm-M boundary / design memo.
- **v002 Label Stage-1 (schema finalized at memo level)**: Phase 4bm-N schema-finalization memo (this phase).

v002 Label Stage-2 (kernel implementation / artefacts), v002 Label Stage-3 (inspected), v002 Label Stage-4 (gate-passed), v002 Label Stage-5 admissibility, v002 Label Stage-5 machine-readable marker, multi-day v002 chronological-split-policy, multi-day v002 diagnostics, multi-day v002 ML, multi-day v002 strategy, multi-day v002 backtests, v002 Feature Stage-6, and `stage_4_feature_cleared = true` on the v002 feature manifest all remain **unauthorized**. v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any v002 label computation.

## §7 Local Gitignored Outputs

**None.** Phase 4bm-N produced **zero** local gitignored artefacts. No label parquet, no label sidecar, no label manifest, no label manifest sidecar, no label gate report, no label successor-state JSON, no label successor-state sidecar, no `.json`, no `.parquet`, no `.csv`, no `.duckdb`, no `.jsonl` was created under `data/microstructure/` or anywhere else.

The local gitignored Phase 4bm-L successor-state JSON + sidecar, Phase 4bm-J gate report + sidecar, Phase 4bm-H per-day feature parquets + sidecars + manifest + sidecar, Phase 4bm-F successor-state JSON + sidecar, Phase 4bm-D gate report + sidecar, v002 derived multi-day index manifest + sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-E raw successor-state JSON, and Phase 4bl-D-R raw gate report continue to exist on the local workstation, gitignored under `.gitignore:85: data/microstructure/`, byte-identical to their prior recorded SHAs (read-only SHA verification of 4 key upstream artefacts performed at merge time MATCH).

## §8 Schema Summary

**Final label family identity (locked):**

| field | value |
| ----- | ----- |
| `dataset_family` | `microstructure_labels_aggtrades_v001` |
| `dataset_version` | `v002` |
| `label_schema_version` | `v001` |
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` |
| `source_feature_dataset_version` | `v002` |
| `source_normalized_dataset_family` | `microstructure_normalized_aggtrades_v001` |
| `source_normalized_dataset_version` | `v002` |
| `source_raw_dataset_family` | `microstructure_raw_aggtrades_v001` |
| `source_raw_dataset_version` | `v002` |
| `symbol_list` | `["BTCUSDT"]` |
| `utc_date_start` | `2024-12-01` |
| `utc_date_end` | `2025-02-28` |
| `date_count` | `90` |

**Final 40-column schema (canonical order):**

- Lineage / identity / metadata (17): `dataset_family`, `dataset_version`, `label_schema_version`, `source_feature_dataset_family`, `source_feature_dataset_version`, `source_feature_manifest_sha256`, `source_feature_parquet_sha256`, `source_feature_successor_state_sha256`, `source_phase_4bm_j_gate_report_sha256`, `source_normalized_manifest_sha256`, `source_raw_manifest_sha256`, `symbol`, `utc_date`, `row_index`, `agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`.
- Label config hash (1): `label_config_hash`.
- Regression labels (4): `forward_log_return_1s`, `forward_log_return_5s`, `forward_log_return_15s`, `forward_log_return_60s`.
- Classification labels (4): `forward_direction_1s`, `forward_direction_5s`, `forward_direction_15s`, `forward_direction_60s`.
- Per-horizon support (12 = 3 × 4): `reference_row_index_<H>`, `reference_timestamp_ms_<H>`, `horizon_censored_flag_<H>` for H ∈ {1s, 5s, 15s, 60s}.
- Global support / QA (2): `label_invalid_price_flag`, `label_any_censored_flag`.

**Final horizon list (locked):** `["1s", "5s", "15s", "60s"]` exactly (1000, 5000, 15000, 60000 ms). Mirror of Phase 4bj-B v001. Widening forbidden without a separately authorized schema-amendment memo.

**Final label list (locked):**

- `forward_log_return_1s`
- `forward_log_return_5s`
- `forward_log_return_15s`
- `forward_log_return_60s`
- `forward_direction_1s`
- `forward_direction_5s`
- `forward_direction_15s`
- `forward_direction_60s`

**Final support columns (locked):**

- `reference_row_index_1s`, `reference_timestamp_ms_1s`, `horizon_censored_flag_1s`
- `reference_row_index_5s`, `reference_timestamp_ms_5s`, `horizon_censored_flag_5s`
- `reference_row_index_15s`, `reference_timestamp_ms_15s`, `horizon_censored_flag_15s`
- `reference_row_index_60s`, `reference_timestamp_ms_60s`, `horizon_censored_flag_60s`
- `label_invalid_price_flag`
- `label_any_censored_flag`

**Final dtype / nullability policy:**

- `row_index`, `agg_trade_id`, all timestamp columns (`feature_timestamp_ms`, `source_transact_time_ms`, `reference_timestamp_ms_*`), `reference_row_index_*`: `int64` (timestamps are UTC ms; `reference_row_index_*` is nullable; others are non-nullable).
- Hashes, dataset IDs, dataset / schema versions, symbol, `utc_date`, `label_config_hash`: `string` (non-nullable).
- `forward_log_return_*`: nullable `float64`.
- `forward_direction_*`: nullable `int8` with values `{-1, 0, 1, null}`.
- `horizon_censored_flag_*`, `label_invalid_price_flag`, `label_any_censored_flag`: non-nullable `bool`.
- **No NaN values** in any column (including float columns). **No inf values** in any column. **Null is allowed only** in the columns explicitly typed as nullable above and only under the censoring / invalid-price conditions defined in §10 of the schema-finalization memo.

**Final forward-reference price policy (multi-day, envelope-bounded):**

For every feature row `R` with anchor timestamp `T = feature_timestamp_ms` and per horizon `H` ∈ `{1s, 5s, 15s, 60s}` with `H_ms` ∈ `{1000, 5000, 15000, 60000}`:

- `target_timestamp_ms = T + H_ms`.
- `envelope_terminal_unix_ms` = the maximum `source_transact_time_ms` across the entire v002 90-day envelope (discoverable via the v002 derived multi-day index manifest at SHA `01c5fa53…`).
- If `target_timestamp_ms > envelope_terminal_unix_ms`: `horizon_censored_flag_H = true`; all that horizon's label columns = `null`.
- Otherwise: `reference_row_index_H` = the row_index of the largest-row-index normalized aggTrades row across the v002 90-day envelope such that `transact_time_ms <= target_timestamp_ms` (may cross UTC day boundaries within the envelope); `reference_timestamp_ms_H` = that row's `transact_time_ms`; `reference_trade_price_H` = that row's trade price (parsed from Decimal-as-string).

**Final forward-return formula (locked):**

```
forward_log_return_H = ln(reference_trade_price_H / anchor_trade_price)
```

Natural log; `Decimal`-as-string parsed exactly; cast to `float64` only at the log step; no `NaN`; no `inf`; null only under censoring or invalid price.

**Final direction policy (locked):**

- `+1` if `forward_log_return_H > 0`
- `0` if `forward_log_return_H == 0`
- `-1` if `forward_log_return_H < 0`
- `null` if `forward_log_return_H` is null
- Strict sign threshold = `0.0` log-return; no dead-band; no bp threshold; no threshold optimization; no evaluation-window fitting; no cost-based threshold at the label-schema level.

**Final 90-day envelope-terminal censoring policy:**

- Keep all feature rows in the label artefact (`row_count` per per-day label parquet equals the per-day feature parquet's `row_count`; aggregate expected `155,153,449`).
- Do not drop right-edge rows.
- For each horizon `H` independently: if `target_timestamp_ms > envelope_terminal_unix_ms`, set `horizon_censored_flag_H = true` and all that horizon's label columns to `null`.
- `label_any_censored_flag = true` if any horizon is censored for that row.
- If invalid price encountered: set affected label columns to null and `label_invalid_price_flag = true`.
- No forward-fill beyond `envelope_terminal_unix_ms`. No cross-envelope stitching.

**Final label manifest required fields (proposed; not created):**

All v002 lineage SHAs verbatim (`source_feature_manifest_sha256`, `source_feature_successor_state_sha256` [Phase 4bm-L], `source_phase_4bm_j_gate_report_sha256`, `source_normalized_manifest_sha256`, `source_phase_4bm_f_derived_successor_state_sha256`, `source_phase_4bm_d_derived_gate_report_sha256`, `source_raw_manifest_sha256`, `source_acquisition_log_sha256`, `source_phase_4bl_e_raw_successor_state_sha256`, `source_phase_4bl_d_r_raw_gate_report_sha256`, `feature_config_hash`); `label_config_hash` (deterministic SHA256 over canonical-JSON schema-locking fields); `column_count = 40`; `row_count` (expected 155,153,449 aggregate); `label_list` (8); `support_column_list` (14); `lineage_column_list` (17); `horizon_list = ["1s", "5s", "15s", "60s"]`; `horizon_ms_list = [1000, 5000, 15000, 60000]`; `envelope_terminal_unix_ms` (deterministically computed); `nullable_tail_policy`; `reference_price_policy`; `direction_threshold_policy`; `chronological_split_policy = "not_yet_defined"`; `per_day_outputs` (90 entries); manifest defaults `research_eligible=false`, `eligibility_gate_status="pending"`, `label_family_research_use_authorized=false`, `stage_5_label_cleared=false`, all `governance_labels.*` at default values.

**Final output path conventions (proposed; not created):**

- per-day label parquet: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet`;
- paired canonical Phase 4bb-F sidecar: same path with `.sha256` suffix;
- label manifest: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`;
- label manifest sidecar: same path with `.sha256` suffix;
- label gate-report directory: `data/microstructure/gate-reports/labels/`;
- label successor-state directory: `data/microstructure/successor-state/` (sibling files only).

**Final future implementation acceptance criteria (27 total; locked in memo §30):**

separately authorized; exact-schema; gitignored-only artefacts; refuse-overwrite; byte-identical preservation of all upstream artefacts (v002 feature manifest + sidecar, 90 v002 per-day feature parquets + sidecars, Phase 4bm-J gate report + sidecar, Phase 4bm-L successor-state JSON + sidecar, Phase 4bm-F successor-state JSON + sidecar, Phase 4bm-D gate report + sidecar, v002 derived multi-day index manifest + sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-E successor-state JSON, Phase 4bl-D-R gate report); no ML / strategy / backtest output; manifest defaults preserved; explicit null / censoring / horizon / split-policy metadata; `envelope_terminal_unix_ms` recorded deterministically; passing `ruff` / `mypy` / `pytest` against the Phase 4bm-H / Phase 4bm-J baseline; matching closeout discipline; M0 clearance for any admissibility transition; Phase 4al refined no-rescue clearance.

## §9 Boundary Statements (required exact phrases)

The following exact phrases are recorded verbatim by the merge-closeout per the task brief:

- **Phase 4bm-N is label schema finalization only.**
- **No label artefact exists after Phase 4bm-N.**
- **Phase 4bm-O is not authorized by Phase 4bm-N.**
- **Label computation is not authorized by Phase 4bm-N.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-N.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

## §10 Evidence Summary

- Phase 4bm-L successor-state SHA256: `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (recomputed on disk at merge time; MATCH).
- Phase 4bm-K decision: **Outcome 1 / Decision form 1** (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`).
- Phase 4bm-K SHA-finalization commit: `121865a26120d5f097fee95c00185ebd4c995703`.
- Phase 4bm-J gate verdict: `FEATURE_GATE_PASS` (`overall_status = "pass"`).
- Phase 4bm-J gate report SHA256: `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (recomputed on disk at merge time; MATCH).
- Phase 4bm-J check totals: 50 / 50 PASS / 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking failures.
- Phase 4bm-I structural QA verdict: `FEATURE_STRUCTURAL_QA_PASS`.
- v002 feature manifest SHA256: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (recomputed on disk at merge time; MATCH; unchanged).
- `feature_config_hash`: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`.
- Feature parquet count: 90; feature sidecar count: 90; total feature row count: 155,153,449.
- Date range: 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days).
- Symbol scope: BTCUSDT (one symbol).
- Feature schema column count: 62 (17 lineage / identity / metadata + 45 feature / quality).
- v002 derived multi-day index manifest SHA256: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (recomputed on disk at merge time; MATCH; unchanged).
- On-disk v002 feature manifest invariants verified: `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`; `actual_feature_row_count = 155153449`; `symbol = "BTCUSDT"`; `per_day_outputs` length = 90.

## §11 Upstream Lineage SHA Table

| # | Artefact | SHA256 | Status |
| - | -------- | ------ | ------ |
|  1 | v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | IDENTICAL (recomputed at merge time; MATCH) |
|  2 | v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | IDENTICAL |
|  3 | Phase 4bm-J v002 feature-family gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | IDENTICAL (recomputed at merge time; MATCH) |
|  4 | Phase 4bm-J v002 feature-family gate sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | IDENTICAL |
|  5 | v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | IDENTICAL (recomputed at merge time; MATCH) |
|  6 | v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | IDENTICAL |
|  7 | v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
|  8 | v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
|  9 | Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | IDENTICAL |
| 10 | Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | IDENTICAL |
| 11 | Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | IDENTICAL |
| 12 | Phase 4bm-D authoritative gate sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | IDENTICAL |
| 13 | Phase 4bm-F v002 derived-family Stage-3 successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | IDENTICAL |
| 14 | Phase 4bm-F v002 derived-family Stage-3 successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | IDENTICAL |
| 15 | Phase 4bm-L v002 feature-family Stage-5 successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | IDENTICAL (recomputed at merge time; MATCH) |
| 16 | Phase 4bm-L v002 feature-family Stage-5 successor-state sidecar | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` | IDENTICAL |
| 17 | Phase 4bi-D v001 feature-family Stage-5 successor-state JSON (reference precedent only) | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` | IDENTICAL |

Phase 4bm-N does not read or open any v002 per-day parquet (90 normalized + 90 feature) or per-day sidecar (90 + 90); they are byte-identical pre/post merge by construction (Phase 4bm-N is docs-only).

## §12 Validation Results

### Initial verification (pre-merge)

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-n/multi-day-v002-label-schema-finalization-memo` (on the phase branch) |
| `git rev-parse main` | `e74dc13021900a54153cba81eaed8fdb397fb292` |
| `git rev-parse origin/main` | `e74dc13021900a54153cba81eaed8fdb397fb292` (in sync) |
| `git rev-parse phase-4bm-n/multi-day-v002-label-schema-finalization-memo` | `2bec753909695bff394c91bdac0e23efac2be015` |
| `git rev-parse origin/phase-4bm-n/multi-day-v002-label-schema-finalization-memo` | `2bec753909695bff394c91bdac0e23efac2be015` (in sync) |
| `git log --oneline -12 --decorate` | latest main commit is `e74dc13 docs(phase-4bm-m): finalize merge closeout shas`; latest branch commit is `2bec753 docs(phase-4bm-n): add multi-day v002 label schema finalization memo` |

### Pre-merge diff validation

| Command | Result |
| ------- | ------ |
| `git diff main..phase-4bm-n/... --stat` | exactly 3 docs files / +1709 insertions / 0 deletions |
| `git diff main..phase-4bm-n/... --name-status` | `M docs/00-meta/current-project-state.md`; `A docs/00-meta/implementation-reports/2026-05-18_phase-4bm-n_closeout.md`; `A docs/00-meta/implementation-reports/2026-05-18_phase-4bm-n_multi-day-v002-label-schema-finalization-memo.md` |
| `git diff main..phase-4bm-n/... --name-only` | exactly 3 paths; no `data/microstructure/` paths |
| `git diff --check main..phase-4bm-n/...` | clean (exit 0; no whitespace errors; no conflict markers) |

### Read-only SHA verification (recomputed on disk at merge time)

| Artefact | SHA256 (recomputed) | Expected | Match |
| -------- | ------------------- | -------- | ----- |
| Phase 4bm-L successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | same | ✓ |
| Phase 4bm-J gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | same | ✓ |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | ✓ |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | same | ✓ |

The remaining 13 upstream lineage artefacts in §11 are not re-hashed at merge time because Phase 4bm-N reads no Parquet, runs no kernel, and modifies no `data/microstructure/` file; their SHAs are taken verbatim from the Phase 4bm-L successor-state JSON `boundary_confirmations` block and the Phase 4bm-M merge-closeout.

### v002 feature manifest content invariants (re-read on disk at merge time)

| Field | Value |
| ----- | ----- |
| `research_eligible` | `false` (unchanged) |
| `eligibility_gate_status` | `"pending"` (unchanged) |
| `stage_4_feature_cleared` | `false` (unchanged) |
| `feature_config_hash` | `"819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"` |
| `actual_feature_row_count` | `155153449` |
| `symbol` | `"BTCUSDT"` |
| `per_day_outputs` length | `90` |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (**never invoked** by Phase 4bm-N).

### Post-merge validation

| Command | Result |
| ------- | ------ |
| `git status --short` (post-merge, pre-closeout-commit) | only `.claude/scheduled_tasks.lock` and `data/research/` (untracked, expected) |
| `git log --oneline -8 --decorate` (post-merge) | latest `main` commit is `ebae05d docs(phase-4bm-n): merge multi-day v002 label schema finalization memo` (HEAD -> main); prior commit is `2bec753 docs(phase-4bm-n): add multi-day v002 label schema finalization memo`; pre-merge `e74dc13` remains intact |
| `git rev-parse main` (post-merge) | `ebae05dc7b9c07a4944d1463c471e642029239f6` |
| `git rev-parse origin/main` (post-merge push) | `ebae05dc7b9c07a4944d1463c471e642029239f6` (in sync; pushed cleanly via `e74dc13..ebae05d  main -> main`) |
| `git diff --check` (post-merge) | clean (exit 0) |

## §13 Quality Gate Commands and Results

- `git diff --check` (against pre-merge `main`, pre-merge phase branch, post-merge `main`): clean (exit 0 in all three positions).
- Repo-standard markdown lint or check: **no project-specific lightweight markdown gate exists** in this repository; therefore none is run.
- `ruff check`, `mypy src/prometheus`, `pytest` — see Skipped-check rationale below.

### Skipped-check rationale

Per the standing precedent for Tier 1 docs-only schema-finalization memos (Phase 4bj-B v001 label schema finalization, Phase 4bh-B v001 feature schema finalization, Phase 4bj-A v001 label-boundary, Phase 4bg-A v001 derived-family research-eligibility, Phase 4bi-C v001 feature-family research-use, Phase 4bm-A multi-day normalization design, Phase 4bm-E multi-day derived-family research-eligibility decision, Phase 4bm-G v002 feature-boundary design, Phase 4bm-K v002 feature-family research-use decision, Phase 4bm-M v002 label-family boundary / design — each of which deliberately skipped these gates for the same reason), `ruff check`, `mypy src/prometheus`, and `pytest` are **not** invoked here:

- Phase 4bm-N modifies no Python source, tests, scripts, or configs. Nothing under `src/prometheus/`, `tests/`, or `scripts/` is touched.
- The Phase 4bm-J branch quality gates already locked the codebase status into the Phase 4bm-J merge-closeout on `main`:
  - Phase 4bm-J surface `ruff check` (11 paths): PASS.
  - Whole-repo `ruff check .`: PASS.
  - `pytest tests/research/microstructure/test_multiday_feature_gate*.py`: 53 PASS in 7.86 s.
  - Whole-repo `pytest`: 15 collection errors from missing `httpx` / `duckdb` env modules + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures (both env baseline).
- The Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files) is preserved by construction because Phase 4bm-N modifies no existing source / test / script.

These skips conform to the project's standing precedent for Tier 1 docs-only schema-finalization memos.

## §14 Boundaries Preserved

- H0 — FRAMEWORK ANCHOR.
- R3 — BASELINE-OF-RECORD.
- R1a / R1b-narrow — RETAINED — NON-LEADING.
- R2 — FAILED — §11.6.
- F1 — HARD REJECT.
- D1-A — MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread — OPERATIONALLY CLOSED (Phase 3t).
- V2 — HARD REJECT — terminal for V2 first-spec.
- G1 — HARD REJECT — terminal for G1 first-spec.
- C1 — HARD REJECT — terminal for C1 first-spec.
- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked** by Phase 4bm-N).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..G / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L / 4bm-M results — all preserved verbatim.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (Phase 4bm-N creates **no** new successor-state artefact).

v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any v002 label computation.

## §15 Recommended State

**Remain paused.**

Phase 4bm-N is project-complete on `main` immediately after this merge-closeout commit is pushed and recorded. Per the Phase 4bk-A workflow standard, project-completion advances the project state by exactly this one phase only. The operator's broader pause decision continues to apply.

## §16 Conditional Next Options (none authorized)

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next, if continuing on the v002 label lifecycle ladder** — future Phase 4bm-O — Multi-Day V002 Label Kernel Implementation + Local Label Artefact Generation (multi-day analogue of Phase 4bj-C) | code + docs + local gitignored output | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 label artefact structural QA (multi-day analogue of Phase 4bj-D) | docs + read-only analysis | **NOT authorized** |
| **Conditional later** — future multi-day v002 label-family eligibility gate (multi-day analogue of Phase 4bj-E) | code + docs + local gitignored gate report | **NOT authorized** |
| **Conditional later** — future multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized** |
| **Conditional later** — future multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state JSON | **NOT authorized** |
| **Conditional later** — future multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I) | docs-only | **NOT authorized** |
| **Conditional later** — future multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J) | docs + local gitignored successor-state JSON | **NOT authorized** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN** |

## §17 Explicit Non-Authorization

This merge-closeout does **not**, and **cannot**, authorize:

- Phase 4bm-O (any provisional successor; not authorized);
- multi-day v002 label-kernel implementation (multi-day analogue of Phase 4bj-C);
- multi-day v002 label artefact generation;
- multi-day v002 label artefact structural QA (multi-day analogue of Phase 4bj-D);
- multi-day v002 label-family eligibility gate (multi-day analogue of Phase 4bj-E);
- multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F);
- multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G);
- multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I);
- multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J);
- multi-day v002 diagnostics;
- multi-day v002 ML training, model selection, feature ranking, meta-labeling;
- multi-day v002 strategy specification, implementation, signal construction;
- multi-day v002 backtest specification, plan, or execution;
- additional acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue data, no aggTrades acquisition beyond the existing locked v002 90-day envelope);
- Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*;
- Phase 5;
- Phase 4 canonical;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user-stream / live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, Phase 4bm-L, or Phase 4bm-M;
- any further successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (**never invoked**). v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any v002 label computation.

**Phase 4bm-N is label schema finalization only.** **No label artefact exists after Phase 4bm-N.** **Phase 4bm-O is not authorized by Phase 4bm-N.** **Label computation is not authorized by Phase 4bm-N.** **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-N.** **No feature artefact was modified.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**
