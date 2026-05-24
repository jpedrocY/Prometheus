# Phase 4bm-M Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-M — Multi-Day V002 Label-Family Boundary / Design Memo
- **Tier**: **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bj-A label-boundary precedent. First-of-kind multi-day v002 label-family boundary / design memo; defines future target / label semantics for a Stage-5-admissible feature family and therefore can affect downstream ML admissibility under §3 ("creates features / labels / diagnostics" + "affects eligibility / admissibility / downstream authorization").
- **Type**: docs-only. Three tracked docs files committed (39-section boundary / design memo + closeout + narrow `current-project-state.md` update). **No** local gitignored output created. **No** source / test / script / configuration / data / manifest / sidecar / gate-report / prior-successor-state file modified. **No** `data/microstructure/` artefact created, modified, deleted, renamed, or committed.
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-M as project-complete on `main` after a clean docs-only branch that defines, at policy level only, the future multi-day v002 label-family boundary on top of the Phase 4bm-L machine-readable v002 Feature Stage-5 research-use admissibility marker. Phase 4bm-M reaches the **v002 Label Stage-0 (boundary / design at policy level)** layer; no label artefact exists.
- **Branch merged**: `phase-4bm-m/multi-day-v002-label-family-boundary-design-memo`
- **Target branch**: `main`
- **Base**: `main` at `38cf6693425f91e85e2d5a295800aa5ee2287db3` (Phase 4bm-L merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-L (Multi-Day V002 Feature-Family Research-Use Successor-State Recording; project-complete on `main`; machine-readable v002 Feature Stage-5 marker recorded as sibling gitignored successor-state JSON SHA `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4`)
- **Direct v001 precedent**: Phase 4bj-A (v001 label-family boundary / target-definition memo; merged on `main`; selected Outcome 1 — label boundary admissible in principle, implementation deferred)

**Phase 4bm-M is label-boundary design only.** **No label artefact exists after Phase 4bm-M.** **Phase 4bm-N is not authorized by Phase 4bm-M.** **Label computation is not authorized by Phase 4bm-M.** **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-M.** **No feature artefact was modified.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-M is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `38cf6693425f91e85e2d5a295800aa5ee2287db3`
- **Pre-merge `origin/main` SHA**: `38cf6693425f91e85e2d5a295800aa5ee2287db3` (in sync; verified)
- **Phase 4bm-M branch commit SHA**: `2ec568b01cfee0254a95d06db3a0af66c6dece6c` (`docs(phase-4bm-m): add multi-day v002 label-family boundary design memo`; 3 docs files / +1407 lines; the boundary / design memo + closeout + narrow `current-project-state.md` update)
- **Phase 4bm-M branch tip SHA pre-merge**: `2ec568b01cfee0254a95d06db3a0af66c6dece6c`
- **Merge commit SHA**: `a4c523475b6ef283badf140c05ad01744b922991`
- **Merge commit message**: `docs(phase-4bm-m): merge multi-day v002 label-family boundary design memo`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `a4c523475b6ef283badf140c05ad01744b922991`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `a4c523475b6ef283badf140c05ad01744b922991` (in sync; pushed cleanly via `38cf669..a4c5234  main -> main`; no force, no skip-hooks, no skip-signing)
- **Merge-closeout commit SHA**: to be recorded in §2 immediately after this file is committed and pushed (the SHA-hygiene patch step will replace this placeholder with the concrete value).
- **Post-merge-closeout-commit `main` SHA**: to be recorded after the closeout push.
- **Post-merge-closeout-commit `origin/main` SHA**: to be recorded after the closeout push.
- **Final `main == origin/main` after closeout push**: to be recorded after the closeout push.

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-m/multi-day-v002-label-family-boundary-design-memo -m "docs(phase-4bm-m): merge multi-day v002 label-family boundary design memo"`
- **Strategy**: `ort` (git default)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     38cf669..a4c5234  main -> main
  ```
  Second push (this merge-closeout commit) output: to be recorded after the closeout push by the SHA-hygiene patch step.

## §4 Files Brought Forward by the Merge

Three tracked docs files brought forward from the Phase 4bm-M branch into `main`, all from the single source-branch commit (`2ec568b`).

**Tracked docs files added (2):**

1. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_multi-day-v002-label-family-boundary-design-memo.md` (NEW, +691; 39 sections; the main boundary / design memo — phase identity / scope / non-scope / linkage to Phase 4bm-L machine-readable v002 Feature Stage-5 marker / linkage to Phase 4bm-K research-use decision / linkage to Phase 4bm-J `FEATURE_GATE_PASS` / linkage to Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS` / linkage to Phase 4bm-H feature artefacts / linkage to Phase 4bj-A v001 precedent / evidence SHA table / proposed future family name + versioning / proposed future manifest naming / proposed future parquet path / proposed future sidecar convention / proposed future lineage fields / proposed future timestamp fields / proposed future source feature / source normalized lineage requirements / proposed future label schema categories transposed from Phase 4bj-A / allowed future label categories / forbidden future label categories / future-data access policy / timestamp / leakage policy / multi-day label boundary policy / proposed future label family identity consolidated / proposed future output namespace consolidated / future label manifest required fields / future label implementation gate prerequisites / what this memo proves / what this memo does not prove / non-authorization / recommended state / conditional next options / preserved boundaries / validation commands and results / quality gate results / no source/test/script/config modified / no labels/diagnostics/ML/strategy/backtests / no endpoint/credential/MCP/Graphify/exchange-write / required exact phrases verbatim).
2. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_closeout.md` (NEW, +183; 13 sections; closeout summarising branch / base SHA / risk tier / tracked files / local-gitignored-outputs-none / decision / design result / key evidence table / validation results / quality gate skipped-check rationale / non-authorization boundaries / recommended state / explicit non-authorization statement / required exact phrases verbatim).

**Tracked docs files modified narrowly (1):**

3. `docs/00-meta/current-project-state.md` (MODIFIED, +533; Phase 4bm-M narrative paragraph + new "Current phase:" block; prior Phase 4bm-L "Current phase:" block preserved as labelled historical context).

**No** `data/microstructure/` artefact is committed by this merge. **No** source / test / script / configuration file outside the above 3-file set is modified. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, and every other tracked file outside the above list are unchanged.

## §5 Diff Summary

`git diff --stat 38cf669..a4c5234` (against pre-merge `main`):

```text
 docs/00-meta/current-project-state.md              | 533 ++++++++++++++++
 .../2026-05-18_phase-4bm-m_closeout.md             | 183 ++++++
 ...i-day-v002-label-family-boundary-design-memo.md | 691 +++++++++++++++++++++
 3 files changed, 1407 insertions(+)
```

No deletions. No `data/microstructure/` path appears. `git diff --check` produces no whitespace or conflict-marker findings.

## §6 Result / Decision / Outcome Recorded by Phase 4bm-M

**Phase 4bm-M is project-complete on `main`.** **The future multi-day v002 label-family boundary is now recorded at policy level on `main`.** **No label artefact exists.** **No data/microstructure file was committed.**

Specifically:

- **future label-family boundary designed at policy level**: the multi-day v002 label-family boundary is fixed in writing on `main` and constrains all future v002 label-family work.
- **proposed future label family**: `microstructure_labels_aggtrades_v001 @ v002` (`label_schema_version = "v001"`).
- **proposed future source feature family**: `microstructure_features_aggtrades_v001 @ v002`.
- **proposed future source normalized family**: `microstructure_normalized_aggtrades_v001 @ v002`.
- **proposed future source raw family**: `microstructure_raw_aggtrades_v001 @ v002`.
- **proposed future output namespace**:
  - label parquets: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/...`;
  - label manifest: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`;
  - label gate reports under `data/microstructure/gate-reports/labels/`;
  - sibling label successor-states under `data/microstructure/successor-state/`.
- **symbol scope**: BTCUSDT only (one symbol).
- **date range**: 2024-12-01 through 2025-02-28 inclusive (90 contiguous UTC days; `date_count = 90`).
- **no label schema finalization** in Phase 4bm-M.
- **no label computation** in Phase 4bm-M.
- **no label artefact created** in Phase 4bm-M.
- **no `data/microstructure/` changes** in Phase 4bm-M.
- **v002 feature manifest unchanged** at SHA256 `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (re-verified on disk at merge time).
- **v002 feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false`** (re-verified on disk at merge time; `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`; `actual_feature_row_count = 155153449`; `symbol = "BTCUSDT"`; `per_day_outputs` length = 90).
- **no manifest mutation** in Phase 4bm-M; **no feature artefact modification** in Phase 4bm-M; **no upstream artefact mutation** in Phase 4bm-M.
- **no Phase 4bm-N authorization**; no successor phase authorized.

The v002 multi-day derived / feature / label-design family now carries a complete ladder of evidence through **v002 Label Stage-0 (boundary / design at policy level)**:

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
- **v002 Label Stage-0 (boundary / design at policy level)**: Phase 4bm-M boundary / design memo (this phase).

v002 Label Stage-1 (schema finalization), v002 Label Stage-2 (artefacts), v002 Label Stage-3 (inspected), v002 Label Stage-4 (gate-passed), v002 Label Stage-5 admissibility, v002 Label Stage-5 machine-readable marker, multi-day v002 chronological-split-policy, multi-day v002 diagnostics, multi-day v002 ML, multi-day v002 strategy, multi-day v002 backtests, v002 Feature Stage-6, and `stage_4_feature_cleared = true` on the v002 feature manifest all remain **unauthorized**. v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any v002 label computation.

## §7 Local Gitignored Outputs

**None.** Phase 4bm-M produced **zero** local gitignored artefacts. No label parquet, no label sidecar, no label manifest, no label manifest sidecar, no label gate report, no label successor-state JSON, no label successor-state sidecar, no `.json`, no `.parquet`, no `.csv`, no `.duckdb`, no `.jsonl` was created under `data/microstructure/` or anywhere else.

The local gitignored Phase 4bm-L successor-state JSON + sidecar, Phase 4bm-J gate report + sidecar, Phase 4bm-H per-day feature parquets + sidecars + manifest + sidecar, Phase 4bm-F successor-state JSON + sidecar, Phase 4bm-D gate report + sidecar, v002 derived multi-day index manifest + sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-E raw successor-state JSON, and Phase 4bl-D-R raw gate report continue to exist on the local workstation, gitignored under `.gitignore:85: data/microstructure/`, byte-identical to their prior recorded SHAs (read-only SHA verification of 4 key upstream artefacts performed at merge time MATCH).

## §8 Label-Boundary Field Summary

The Phase 4bm-M boundary / design memo records the following at policy level (no artefacts created; design only):

**Future label-family identity (proposed; not authorized):**

| Field | Proposed value |
| ----- | -------------- |
| `dataset_family` | `"microstructure_labels_aggtrades_v001"` |
| `dataset_version` | `"v002"` |
| `label_schema_version` | `"v001"` |
| `source_feature_dataset_family` | `"microstructure_features_aggtrades_v001"` |
| `source_feature_dataset_version` | `"v002"` |
| `source_normalized_dataset_family` | `"microstructure_normalized_aggtrades_v001"` |
| `source_normalized_dataset_version` | `"v002"` |
| `source_raw_dataset_family` | `"microstructure_raw_aggtrades_v001"` |
| `source_raw_dataset_version` | `"v002"` |
| `symbol_list` | `["BTCUSDT"]` |
| `utc_date_start` | `"2024-12-01"` |
| `utc_date_end` | `"2025-02-28"` |
| `date_count` | `90` |

**Allowed future label categories (admissible in principle):**

- class A `forward_log_return_<horizon>` (numeric / regression);
- class B `forward_direction_<horizon>` (classification with predeclared thresholds; never optimised on the evaluation cell);
- class F per-horizon validity / censoring flags `horizon_valid_<horizon>` / `forward_censored_<horizon>` (REQUIRED for any label parquet that spans the 2025-02-28 envelope or mixes horizons);
- strictly deterministic labels derived from the locked v002 BTCUSDT time / event series.

**Deferred future label categories (admissible in principle; not part of v002 first pass; mirrors Phase 4bj-A v001 deferral):**

- class C `barrier_outcome_<horizon>` / `target_before_stop_<horizon>`;
- class D `mfe_mae_r_path_<horizon>` (forensic / evaluation only; never strategy rules; Phase 4al refined no-rescue rule applies verbatim);
- class E `time_to_event_<horizon>`;
- multi-symbol label families (no ETHUSDT / alts authorized at v002);
- horizons beyond a conservative initial set (no 5m / 30m / 1h / 4h / 1d / multi-day horizons authorized at v002 first pass);
- cross-day chronological-split-policy labels (a future separately authorized split-policy memo must precede any split definition).

**Forbidden future label categories:**

- strategy entry / exit decisions;
- PnL / equity / R-multiple / position-state / alpha / edge / prediction / model-probability / decision-score targets;
- post-model labels (any label derived from a trained model's output);
- mark-price stop labels at v002 first-pass scope (unless a separately authorized memo reconciles Phase 3v §8 stop-trigger-domain governance with label semantics);
- cross-venue / external-data labels (no spot, no order-book, no funding, no OI, no liquidation, no mark-price 30m / 4h / 5m / 15m, no metrics beyond Phase 4j §11 OI subset);
- labels that require public or private endpoint calls in code;
- labels that mutate any prior `data/microstructure/` artefact;
- post-hoc optimised-threshold labels (thresholds fitted to the evaluation cell rather than predeclared);
- rescue-shaped label families that reproduce R2 / F1 / D1-A / V2 / G1 / C1 / 5m-thread entry / exit rules under a different name;
- labels using the live exchange's own decision boundaries as targets (exchange-side stop triggers, liquidation events, ADL events).

**Causal-separation rule (binding):**

- v002 features must remain causal per the Phase 4bm-G / Phase 4bh contract verbatim (row `R` at timestamp `T` uses only `transact_time_ms <= T` and tie-break `row_index <= R`);
- labels may use future information **only inside the label kernel routine**;
- features must not be modified by label computation;
- label columns must never appear in feature parquets (v002 feature parquets remain at exactly 62 columns);
- labels must never be used to normalize / z-score / rank / bucket / filter / mask / select feature rows before any split definition;
- label code must be independently importable from feature code;
- cross-imports that let label results feed back into feature computation are forbidden;
- future label-kernel implementation must include a static and runtime test asserting no label value flows back into any feature column for any v002 row.

**Future-data access policy:**

- labels may use future information only inside label generation;
- labels must be stored in a separate label artefact family (`data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/...`);
- label columns must never be placed inside feature parquets;
- all future-looking label fields must be explicitly marked `column_role = "label"` (or `"target"`) so that any feature-recompute routine refuses to read label columns as feature inputs.

**Timestamp / leakage policy:**

- UTC only (integer milliseconds);
- deterministic event ordering `(feature_timestamp_ms, agg_trade_id, row_index)`;
- one label row per feature row per horizon;
- same-timestamp tie-break `row_index`;
- end-of-sample censoring at 2025-02-28 23:59:59.999 UTC (null label + explicit boolean `forward_censored_<horizon> = true` flag);
- day-boundary horizons recorded with anchor row's `utc_date` (not the future reference's date);
- no random shuffle;
- no train / validation / test split assignment in this phase.

**Multi-day end-of-envelope censoring policy:**

- labels may require future-day lookahead inside the label kernel only;
- end-of-dataset rows with insufficient future horizon must be censored explicitly (null label + boolean censoring flag);
- **no data beyond 2025-02-28 may be acquired by this phase or any future label phase unless a separately authorized acquisition phase is approved**;
- silent extrapolation / synthetic future fills / zero-padding beyond 2025-02-28 is forbidden.

**Future label manifest required fields (proposed; not created):**

- `dataset_family` = `"microstructure_labels_aggtrades_v001"`, `dataset_version` = `"v002"`, `label_schema_version` = `"v001"`;
- source feature / normalized / raw lineage SHAs (verbatim from §11 below);
- `source_feature_successor_state_sha256` = `"7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4"` (Phase 4bm-L);
- `source_phase_4bm_j_gate_report_sha256` = `"3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242"`;
- `feature_config_hash` = `"819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"`;
- `label_config_hash`: deterministic hash of the future label kernel configuration (computed by the kernel);
- `label_list`: ordered list of label column names;
- `horizon_list`: ordered list of future horizons;
- `symbol_list` = `["BTCUSDT"]`; `utc_date_start` = `"2024-12-01"`; `utc_date_end` = `"2025-02-28"`; `date_count` = `90`;
- `row_count`: total label rows (may equal feature row count 155,153,449 or be lower if right-edge censoring removes rows);
- `per_day_outputs`: ordered list of 90 per-day label parquet entries (path + SHA256 + sidecar SHA256 + row count);
- `nullable_tail_policy`: explicit description of how horizon-censored rows are represented;
- `chronological_split_policy` = `"not_yet_defined"` (until a separately authorized split-policy memo locks it);
- `governance_labels`: `labels` = `"allowed_by_future_phase_only"`; `targets` = `"allowed_by_future_phase_only"`; `ml` = `"forbidden"`; `strategy` = `"forbidden"`; `backtest` = `"forbidden"`; `acquisition` = `"unauthorized"`; `paper_shadow_live` = `"forbidden"`; `deployment` = `"forbidden"`; `exchange_write` = `"forbidden"`;
- `research_eligible` = `false` (default); `eligibility_gate_status` = `"pending"` (default); `label_family_research_use_authorized` = `false` (default);
- `code_commit_sha`: the implementation phase's commit SHA at run time;
- `created_at_unix_ms`: the implementation phase's creation time.

**Future implementation gate prerequisites (14 conditions; all currently UNMET):**

1. Phase 4bm-M merged + project-complete;
2. separately authorized Phase 4bm-N (or equivalent) schema-finalization memo;
3. separately authorized label-kernel implementation phase;
4. exact-schema implementation (no widening / narrowing / drift);
5. gitignored-only artefacts under `data/microstructure/labels/`, manifests/, gate-reports/labels/, successor-state/;
6. refuse-overwrite logic;
7. byte-identical preservation of ALL upstream artefacts (v002 feature manifest + sidecar; 90 v002 per-day feature parquets + sidecars; Phase 4bm-J gate report + sidecar; Phase 4bm-L successor-state JSON + sidecar; Phase 4bm-F successor-state JSON + sidecar; Phase 4bm-D gate report + sidecar; v002 derived multi-day index manifest + sidecar; v002 raw manifest; v002 acquisition log; Phase 4bl-E successor-state JSON; Phase 4bl-D-R gate report);
8. no ML / strategy / backtest output;
9. manifest defaults `research_eligible=false`, `eligibility_gate_status="pending"`, `label_family_research_use_authorized=false`, `chronological_split_policy="not_yet_defined"`;
10. explicit null / censoring / horizon / split-policy metadata;
11. passing `ruff` / `mypy` / `pytest` against the Phase 4bm-H / Phase 4bm-J baseline;
12. matching closeout discipline;
13. cleared M0 admissibility for the label family (Phase 4ak twelve-clause gate applies prospectively);
14. cleared Phase 4al refined no-rescue rule for the label family.

## §9 Evidence Summary

- Phase 4bm-L successor-state SHA256: `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (recomputed on disk at merge time; MATCH).
- Phase 4bm-L successor-state sidecar SHA256: `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98`.
- Phase 4bm-K decision: **Outcome 1 / Decision form 1** (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`).
- Phase 4bm-K SHA-finalization commit: `121865a26120d5f097fee95c00185ebd4c995703`.
- Phase 4bm-J gate verdict: `FEATURE_GATE_PASS` (`overall_status = "pass"`).
- Phase 4bm-J gate report SHA256: `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (recomputed on disk at merge time; MATCH).
- Phase 4bm-J gate sidecar SHA256: `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`.
- Phase 4bm-J check totals: 50 / 50 PASS / 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking failures.
- Phase 4bm-I structural QA verdict: `FEATURE_STRUCTURAL_QA_PASS`.
- v002 feature manifest SHA256: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (recomputed on disk at merge time; MATCH; unchanged).
- v002 feature manifest sidecar SHA256: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` (unchanged).
- `feature_config_hash`: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`.
- Feature parquet count: 90; feature sidecar count: 90; total feature row count: 155,153,449.
- Date range: 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days).
- Symbol scope: BTCUSDT (one symbol).
- Feature schema column count: 62 (17 lineage / identity / metadata + 45 feature / quality).
- v002 derived multi-day index manifest SHA256: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (recomputed on disk at merge time; MATCH; unchanged).
- On-disk v002 feature manifest invariants verified: `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`; `actual_feature_row_count = 155153449`; `symbol = "BTCUSDT"`; `per_day_outputs` length = 90.

## §10 Boundary Statements (required exact phrases)

The following exact phrases are recorded verbatim by the merge-closeout per the task brief:

- **Phase 4bm-M is label-boundary design only.**
- **No label artefact exists after Phase 4bm-M.**
- **Phase 4bm-N is not authorized by Phase 4bm-M.**
- **Label computation is not authorized by Phase 4bm-M.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-M.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

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

Phase 4bm-M does not read or open any v002 per-day parquet (90 normalized + 90 feature) or per-day sidecar (90 + 90); they are byte-identical pre/post merge by construction (Phase 4bm-M is docs-only).

## §12 Validation Results

### Initial verification (pre-merge)

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-m/multi-day-v002-label-family-boundary-design-memo` (on the phase branch) |
| `git rev-parse main` | `38cf6693425f91e85e2d5a295800aa5ee2287db3` |
| `git rev-parse origin/main` | `38cf6693425f91e85e2d5a295800aa5ee2287db3` (in sync) |
| `git rev-parse phase-4bm-m/multi-day-v002-label-family-boundary-design-memo` | `2ec568b01cfee0254a95d06db3a0af66c6dece6c` |
| `git rev-parse origin/phase-4bm-m/multi-day-v002-label-family-boundary-design-memo` | `2ec568b01cfee0254a95d06db3a0af66c6dece6c` (in sync) |
| `git log --oneline -12 --decorate` | latest main commit is `38cf669 docs(phase-4bm-l): finalize merge closeout shas`; latest branch commit is `2ec568b docs(phase-4bm-m): add multi-day v002 label-family boundary design memo` |

### Pre-merge diff validation

| Command | Result |
| ------- | ------ |
| `git diff main..phase-4bm-m/... --stat` | exactly 3 docs files / +1407 insertions / 0 deletions |
| `git diff main..phase-4bm-m/... --name-status` | `M docs/00-meta/current-project-state.md`; `A docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_closeout.md`; `A docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_multi-day-v002-label-family-boundary-design-memo.md` |
| `git diff main..phase-4bm-m/... --name-only` | exactly 3 paths; no `data/microstructure/` paths |
| `git diff --check main..phase-4bm-m/...` | clean (exit 0; no whitespace errors; no conflict markers) |

### Read-only SHA verification (recomputed on disk at merge time)

| Artefact | SHA256 (recomputed) | Expected | Match |
| -------- | ------------------- | -------- | ----- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | ✓ |
| Phase 4bm-J gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | same | ✓ |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | same | ✓ |
| Phase 4bm-L successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | same | ✓ |

The remaining 13 upstream lineage artefacts in §11 (sidecars, v002 raw / acquisition log, Phase 4bl-D-R, Phase 4bl-E, Phase 4bm-D, Phase 4bm-F, Phase 4bi-D reference) are not re-hashed at merge time because Phase 4bm-M reads no Parquet, runs no kernel, and modifies no `data/microstructure/` file; their SHAs are taken verbatim from the Phase 4bm-L successor-state JSON `boundary_confirmations` block and the Phase 4bm-L implementation report Evidence Table §15.

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

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (**never invoked** by Phase 4bm-M).

### Post-merge validation

| Command | Result |
| ------- | ------ |
| `git status --short` (post-merge, pre-closeout-commit) | only `.claude/scheduled_tasks.lock` and `data/research/` (untracked, expected) |
| `git log --oneline -8 --decorate` (post-merge) | latest `main` commit is `a4c5234 docs(phase-4bm-m): merge multi-day v002 label-family boundary design memo` (HEAD -> main); prior commit is `2ec568b docs(phase-4bm-m): add multi-day v002 label-family boundary design memo`; pre-merge `38cf669` remains intact |
| `git rev-parse main` (post-merge) | `a4c523475b6ef283badf140c05ad01744b922991` |
| `git rev-parse origin/main` (post-merge push) | `a4c523475b6ef283badf140c05ad01744b922991` (in sync; pushed cleanly via `38cf669..a4c5234  main -> main`) |
| `git diff --check` (post-merge) | clean (exit 0) |

## §13 Quality Gate Commands and Results

- `git diff --check` (against pre-merge `main`, pre-merge phase branch, post-merge `main`): clean (exit 0 in all three positions).
- Repo-standard markdown lint or check: **no project-specific lightweight markdown gate exists** in this repository; therefore none is run.
- `ruff check`, `mypy src/prometheus`, `pytest` — see Skipped-check rationale below.

### Skipped-check rationale

Per the standing precedent for Tier 1 docs-only boundary / design-memo phases (Phase 4bj-A v001 label-boundary, Phase 4bg-A v001 derived-family research-eligibility, Phase 4bi-C v001 feature-family research-use, Phase 4bm-A multi-day normalization design, Phase 4bm-E multi-day derived-family research-eligibility decision, Phase 4bm-G v002 feature-boundary design, Phase 4bm-K v002 feature-family research-use decision — each of which deliberately skipped these gates for the same reason), `ruff check`, `mypy src/prometheus`, and `pytest` are **not** invoked here:

- Phase 4bm-M modifies no Python source, tests, scripts, or configs. Nothing under `src/prometheus/`, `tests/`, or `scripts/` is touched.
- The Phase 4bm-J branch quality gates already locked the codebase status into the Phase 4bm-J merge-closeout on `main`:
  - Phase 4bm-J surface `ruff check` (11 paths): PASS.
  - Whole-repo `ruff check .`: PASS.
  - `pytest tests/research/microstructure/test_multiday_feature_gate*.py`: 53 PASS in 7.86 s.
  - Whole-repo `pytest`: 15 collection errors from missing `httpx` / `duckdb` env modules + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures (both env baseline).
- The Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files) is preserved by construction because Phase 4bm-M modifies no existing source / test / script.

These skips conform to the project's standing precedent for Tier 1 docs-only boundary / design-memo phases.

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked** by Phase 4bm-M).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..G / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L results — all preserved verbatim.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (Phase 4bm-M creates **no** new successor-state artefact).

## §15 Recommended State

**Remain paused.**

Phase 4bm-M is project-complete on `main` immediately after this merge-closeout commit is pushed and recorded. Per the Phase 4bk-A workflow standard, project-completion advances the project state by exactly this one phase only. The operator's broader pause decision continues to apply.

## §16 Conditional Next Options (none authorized)

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next, if continuing on the v002 label lifecycle ladder** — future Phase 4bm-N — Multi-Day V002 Label Schema Finalization Memo (multi-day analogue of Phase 4bj-B) | docs-only; no computation | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 label-kernel implementation (multi-day analogue of Phase 4bj-C) | code + docs + local gitignored output | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 label artefact structural QA (multi-day analogue of Phase 4bj-D) | docs + read-only analysis | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 label-family eligibility gate (multi-day analogue of Phase 4bj-E) | code + docs + local gitignored gate report | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state JSON | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I) | docs-only | **NOT authorized by this merge-closeout** |
| **Conditional later** — future multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J) | docs + local gitignored successor-state JSON | **NOT authorized by this merge-closeout** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN** |

## §17 Explicit Non-Authorization

This merge-closeout does **not**, and **cannot**, authorize:

- Phase 4bm-N (any provisional successor; not authorized);
- multi-day v002 label-family schema finalization (multi-day analogue of Phase 4bj-B);
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
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, or Phase 4bm-L;
- any further successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (**never invoked**). v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any v002 label computation.

**Phase 4bm-M is label-boundary design only.** **No label artefact exists after Phase 4bm-M.** **Phase 4bm-N is not authorized by Phase 4bm-M.** **Label computation is not authorized by Phase 4bm-M.** **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-M.** **No feature artefact was modified.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**
