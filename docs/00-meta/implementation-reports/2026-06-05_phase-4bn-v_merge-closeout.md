# Phase 4bn-V — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-V — Label Manifest / Versioning Memo.
- **Type:** docs-only / label-manifest / label-versioning / label-lineage /
  non-eligible-source precondition / envelope-terminal boundary-contract memo.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-V label manifest/versioning memo, its
  branch closeout, and the narrow `current-project-state.md` update onto `main`
  as project state. Phase 4bn-V resolves — from committed repository Markdown and
  committed code/tests only, reading no local data — the label
  manifest/versioning ambiguity that Phase 4bn-U identified as the single binding
  obstacle to authorizing a future label-only execution phase over the Phase
  4bn-S / 4bn-T pre-v002 BTCUSDT Binance USDⓈ-M futures aggTrades feature segment
  (2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates; 400,001,695 rows). The
  phase decided
  `RECOMMEND_AUTHORIZE_LABEL_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  (result state
  `RECORD_LABEL_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`); it authorizes no
  label derivation, no label artefact, no manifest mutation, no label gate, no
  ML, no diagnostics, no strategy, and no successor.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-v/label-manifest-versioning-memo`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `4cf47348fd51061719e36102fab207b541cc6dcd`
  (`docs(phase-4bn-u): finalize merge closeout shas`).
- **Branch commit SHA (memo + closeout + narrow state update):**
  `6785495961d475f2c8523f6c9d59c146d55e1dee`
  (`docs(phase-4bn-v): settle label manifest versioning`).
- **Merge commit SHA:** `7d6409c1f201c3e2ed5bdba8b218aa6cb92d2a33`
  (`docs(phase-4bn-v): merge label manifest versioning`).
- **Merge-closeout commit SHA:** recorded in the final operator report after the
  `docs(phase-4bn-v): add merge closeout` commit.
- **SHA-finalization commit SHA:** the subsequent
  `docs(phase-4bn-v): finalize merge closeout shas` commit — its own hash becomes
  the new `main` tip; recorded verbatim in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit;
  `main == origin/main` after push (recorded in the final operator report).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `docs(phase-4bn-v): merge label manifest versioning`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
  (recorded at the final operator report after the SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-V prose
    paragraph after the Phase 4bn-U paragraph + new `Current phase:` block ahead
    of the Phase 4bn-U block; prior Phase 4bn-A … 4bn-U paragraphs and blocks
    preserved verbatim as labelled historical context; 142 insertions, 0
    deletions — insertion-only);
  - `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-v_label-manifest-versioning-memo.md`
    (added — the implementation report, 29 sections);
  - `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-v_closeout.md`
    (added — branch closeout).
- **Source / tests / scripts / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No manifest, sidecar, gate report, successor-state
  artefact, `.gitignore`, `pyproject.toml`, `README.md`, or MCP file was
  modified. No source module, test, or script was created or modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 2 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  142 +++
 .../2026-06-05_phase-4bn-v_closeout.md             |  168 +++
 ...5_phase-4bn-v_label-manifest-versioning-memo.md | 1292 ++++++++++++++++++++
 3 files changed, 1602 insertions(+)
```

The diff matches the expected change set (insertion-only; docs only; no data, no
code, no tests, no scripts, no config).

## 6. Result / verdict

**MEMO RECORDED — REMAIN PAUSED.** Phase 4bn-V is a docs-only label
manifest/versioning memo. From committed docs and committed tooling only (no
local data read), it resolves the label manifest/versioning ambiguity Phase
4bn-U deferred, by mirroring the merged raw-/normalized-/feature-layer segment
precedents. It selects: (1) a **phase-scoped pre-v002 label segment manifest**
`microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>.json`
(`dataset_version: "v002"`, `label_schema_version: "v001"`, `segment_label:
"pre_v002_segment"`), tied to the existing v002 label family but marked a
pre-v002 backward segment; **no v003**; published `__v002` label
manifest/directory byte-for-byte immutable. (2) A **non-eligible-source
precondition** built on the Phase 4bn-S feature segment manifest (`4881eb87…`) +
Phase 4bn-T feature-layer gate PASS (`db731d1b…`) + Phase 4bn-O normalized
segment manifest (`0e96ae37…`) + Phase 4bn-P normalized-layer gate PASS
(`3452fd9d…`), replacing the Phase 4bm-L Stage-5 research-use successor-state;
segment `feature_config_hash = 0726b41d…` (not the v002 lock `819cfa7a…`). (3) A
**new segment-scoped `label_config_hash` builder**
(`build_label_config_hash_v002_pre_v002_segment`) preserving the label policy
fields but re-specifying the future-reference envelope clause to the pre-v002
segment terminal, replacing the successor-state input with the Phase 4bn-T /
4bn-P gate witnesses, and binding `feature_config_hash = 0726b41d…`; verbatim
reuse of `build_label_config_hash_v002` is rejected because its hashed
`FUTURE_REFERENCE_POLICY_V002` string literally encodes
`across_v002_90day_envelope`. (4) **`LABEL_SCHEMA_V002` retained exactly** (40
columns, `label_schema_version "v001"`, names verbatim), with the two
terminal-specific lineage columns re-mapped per-row
(`source_phase_4bm_j_gate_report_sha256` → Phase 4bn-T gate SHA;
`source_feature_successor_state_sha256` → Phase 4bn-P gate SHA) and recorded in a
manifest `lineage_column_reinterpretation` block; no new label schema version; no
v003. (5) **`envelope_terminal_unix_ms` locked to the pre-v002 segment terminal**
(max `source_transact_time_ms` / `feature_timestamp_ms` within 2024-11-30;
`envelope_terminal_utc_date = "2024-11-30"`); 1s/5s/15s/60s horizons crossing it
censor; no 2024-12-01+ read; no sealed-test read; no holdout-boundary memo
required. (6) The full 12-month label envelope represented **by reference**
(segment manifest fields now; optional deferred full-envelope label reference
manifest later). Decision:
`RECOMMEND_AUTHORIZE_LABEL_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
result state `RECORD_LABEL_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`. The
merge lands the memo + closeout + narrow state update on `main`; the project
remains paused; the pre-v002 feature/normalized segments remain **non-eligible**
(`research_eligible: false`, `eligibility_gate_status: "pending"`); no manifest
eligibility transition occurred.

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-V is docs-only: it produced no local artefact, read no local
data, and created nothing under `data/microstructure/` or `data/research/`.
`git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88` (the pre-existing local
gitignored Phase 4bn-O/4bn-P/4bn-S/4bn-T artefacts remain local, uncommitted, and
were not accessed by this phase).

## 8. Validation results

Docs-only merge-review validation (no code/test/script/config surface; no
acquisition, gate, normalization, feature, label, ML, diagnostics, strategy, or
backtest run):

- `git diff --check` → clean (no whitespace errors / conflict markers).
- `git diff --name-status main..branch` (pre-merge) → exactly the 3 expected
  files (M `current-project-state.md`; A closeout; A implementation report).
- `git diff --stat main..branch` (pre-merge) and the merge diff → `3 files
  changed, 1602 insertions(+)` (insertion-only).
- `ruff` / `mypy` / `pytest` → **not run; not required.** Phase 4bn-V adds no
  code, tests, scripts, or config surface; the validation surface for a docs-only
  phase is git status, diff review, `git diff --check`, gitignore confirmation,
  and SHA checks. No repo-standard Markdown validator that runs without producing
  outputs / mutating artefacts is configured; none was run.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `.claude/scheduled_tasks.lock` untracked; no
  `data/microstructure/` or `data/research/` artefact staged or committed; the
  merge committed exactly the 3 tracked docs files (no `data/` file).

## 9. Upstream immutability evidence

**n/a — phase did not access any local artefact.** Phase 4bn-V read no local
Parquet, manifest, sidecar, gate report, or zip; it referenced upstream artefacts
only by their committed-document SHAs (Phase 4bn-S feature segment manifest
`4881eb87…b52` / feature_config_hash `0726b41d…`; Phase 4bn-T feature-layer gate
report `db731d1b…6ab08`; Phase 4bn-O normalized segment manifest `0e96ae37…d9fa`;
Phase 4bn-P normalized-layer gate report `3452fd9d…f134`; the pre-v002 raw
segment manifest `1659e6da…3a3d1`; the published-v002 label tooling lock
`819cfa7a…`) cited from committed reports, not by hashing local data. No
`data/microstructure/` file was read or modified by the phase or the merge.

## 10. Manifest state preservation

- **Phase 4bn-S feature segment manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; unchanged — no transition (referenced by
  document SHA only; not read or mutated).
- **Phase 4bn-O normalized segment manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; unchanged — no transition.
- **Published normalized / feature / label `__v002` manifests:** untouched; no
  transition.
- No `chronological_split_policy`, `diagnostics_authorized`, or `ml_authorized`
  transition occurred (the future label segment manifest, defined in this memo at
  design level only, would carry `chronological_split_policy: "not_yet_defined"`,
  but no such manifest was created by this phase).
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code created or modified; no test created or modified; no script
  created or modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no manifest / sidecar / gate report / successor-state artefact created or
  modified;
- no `data/microstructure/` or `data/research/` artefact opened, hashed, counted,
  inspected, created, staged, or committed;
- no local raw zip / normalized Parquet / feature Parquet / label file / gate
  report / manifest read under `data/microstructure`;
- no v002 terminal raw / normalized / feature window read; no sealed-test split
  read;
- no label derivation; no label artefact / manifest creation or mutation; no
  label gate execution; no targets / future returns; no barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels;
- no feature execution rerun; no feature-layer gate rerun; no normalization
  rerun; no raw-gate rerun; no normalized-layer-gate rerun;
- no ML / model scoring / predictions; no diagnostics; no strategy / signal /
  PnL / backtest; no feature ranking / selection / pruning; no label
  optimization / threshold / hyperparameter / calibration tuning;
- no acquisition; no endpoint / public / Binance / `data.binance.vision` call;
  no archive / CHECKSUM download; no HEAD preflight;
- no `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transition;
- no database / `.duckdb` / `.sqlite`; no Parquet compaction; no storage
  migration; no v003;
- no ETHUSDT / mark-price / spot / cross-venue / order-book / tick /
  extra-horizon data;
- no credential / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user stream
  / private / authenticated endpoint used;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

## 12. Retained verdict ledger

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked)
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bl-F four-tier risk model
- Phase 4bn-J-R1 raw-only cap amendment
- Phase 4bn-L derived-stack storage budget (carried forward by this memo)
- Phase 4bn-N normalization manifest/versioning convention
- Phase 4bn-R feature manifest/versioning convention + non-eligible-source
  precondition

All prior phase results preserved verbatim. Phase 4 canonical remains
unauthorized.

## 14. No-rescue constraints

The Phase 4bn-V merge does not, and cannot, be construed as authorising:

- the label-only execution it recommends (recommended only, NOT authorized), a
  holdout-boundary memo, a source-policy memo, or a process-doc path update;
- label derivation; label artefact / manifest creation or mutation; label gate
  execution; targets; future returns; barrier / target-before-stop / MFE / MAE /
  R-multiple / PnL labels; 30s / 5m / 30m / 1h / 4h / longer-horizon label
  generation; extra horizons beyond the committed 1s/5s/15s/60s label policy;
- ML model training / selection / scoring, predictions, strategy hypothesis
  generation, signal construction, position state, entry/exit rules, diagnostics,
  or backtest design;
- feature ranking / selection / pruning / engineering / hyperparameter /
  threshold / calibration tuning;
- a chronological-split / holdout policy decision or transition;
- paper / shadow / live-readiness / deployment / exchange-write / production-key
  work; Phase 4 canonical or Phase 5 authorisation;
- mark-price / spot / cross-venue / order-book / tick / additional aggTrades /
  ETHUSDT acquisition; v003 creation;
- reading the v002 terminal raw/normalized/feature window or sealed-test split;
  mutating the published normalized / feature / label `__v002` family;
- database creation / DuckDB / SQLite / Parquet compaction / storage migration;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status`
  from this docs-only memo alone;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a label-only execution phase (Phase 4bn-V's recommendation — requires separate
  operator authorization) — a bounded new `phase4bn_*` wrapper over the Phase
  4bn-S feature + Phase 4bn-O normalized pre-v002 segments honouring the memo's
  §14–§24 and the Phase 4bn-L budget, including the new segment-scoped
  config-hash builder + lineage re-mapping with offline tests;
- a label-layer eligibility gate (only after label execution, separately
  authorized);
- a docs-only holdout-boundary memo (only if a future scope reads the v002
  terminal raw/normalized/feature window or sealed-test dates);
- a source-policy documentation memo; a process-doc `D:` path-string update;
- a chronological-split / holdout policy memo;
- ML implementation; strategy implementation; backtest implementation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot /
  cross-venue / ETHUSDT acquisition; v003 creation; storage migration; database
  creation;
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials;
- Phase 5; Phase 4 canonical.

## 16. Recommended state

**Remain paused.**

Phase 4bn-V is now **merge-complete on `main`** as of merge commit
`7d6409c1f201c3e2ed5bdba8b218aa6cb92d2a33` and the subsequent merge-closeout +
SHA-finalization commits. Project completion of this phase requires the
SHA-finalization commit (`docs(phase-4bn-v): finalize merge closeout shas`) per
the repository's merge-closeout convention. The pre-v002 feature and normalized
segments remain **non-eligible** (`research_eligible: false`,
`eligibility_gate_status: "pending"`); no manifest eligibility transition
occurred. v003 remains forbidden and absent; the published `__v002`
normalized/feature/label families remain immutable; the v002 terminal
raw/normalized/feature window remains by-reference only and unread; the
sealed-test split remains untouched.

**Conditional next, NOT authorized:** a separately-authorized **label-only
execution phase** is the cleanest non-paused option. It would build a bounded new
`phase4bn_*` wrapper over the Phase 4bn-S pre-v002 feature segment + Phase 4bn-O
pre-v002 normalized segment, honouring the selected label segment manifest/naming
convention, the non-eligible-source precondition, the new segment-scoped
`build_label_config_hash_v002_pre_v002_segment` builder, the lineage re-mapping,
the pre-v002 envelope terminal, the segment-scoped output directory, and the
Phase 4bn-L budget — producing 275 per-day non-eligible label Parquet + sidecars
+ a single non-eligible label segment manifest + sidecar, with offline tests,
followed (only if separately authorized) by a bounded label-layer eligibility
gate. It is **not** authorized by this merge.

### Selected conventions (preserved)

- **Label manifest/versioning convention:** phase-scoped pre-v002 label segment
  manifest
  `microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>.json`
  (+ canonical two-space `.sha256` sidecar); `dataset_family =
  "microstructure_labels_aggtrades_v001"`, `dataset_version = "v002"`, `version =
  "v002"`, `label_schema_version = "v001"`, `segment_label = "pre_v002_segment"`,
  `data_family = "aggTrades"`, `symbol = "BTCUSDT"`, `market = "usdm_futures"`,
  `dataset_category = "labels"`; tied to the existing v002 label family but marked
  a pre-v002 backward segment; **not** a new `__vNNN`; **not** a write into the
  published `__v002` label family; **not** v003; published `__v002` label
  manifest/directory byte-for-byte immutable.
- **Non-eligible-source precondition:** Phase 4bn-S feature segment manifest
  (`4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`) + Phase
  4bn-T feature-layer gate PASS
  (`db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`) + Phase
  4bn-O normalized segment manifest
  (`0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`) + Phase
  4bn-P normalized-layer gate PASS
  (`3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`), replacing
  the Phase 4bm-L Stage-5 research-use successor-state; source segments remain
  `research_eligible = false` / `eligibility_gate_status = pending`; generated
  outputs remain non-eligible/pending with `no_successor_authorization = true`; no
  Stage-5 successor and no `EXPECTED_FEATURE_CONFIG_HASH = 819cfa7a…` required or
  created; segment `feature_config_hash =
  0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`; Phase 4aw
  `flip_research_eligible(...)` always-raises invariant never invoked.
- **`label_config_hash` convention:** new segment-scoped builder
  `build_label_config_hash_v002_pre_v002_segment`; preserves the committed v002
  label policy fields (anchor / direction-threshold / null-censoring / dtype +
  schema / horizon / lineage lists); re-specifies the future-reference envelope
  clause to the pre-v002 segment (2024-03-01 .. 2024-11-30); replaces the
  successor-state input with the Phase 4bn-T / 4bn-P gate witnesses; binds
  `feature_config_hash = 0726b41d…` and must not bind `819cfa7a…`; adds a
  `pre_v002_segment` discriminator; requires a future code-level change + offline
  tests before execution; verbatim reuse of `build_label_config_hash_v002`
  rejected because its hashed `FUTURE_REFERENCE_POLICY_V002` encodes the v002
  90-day envelope.
- **Label lineage convention:** keep `LABEL_SCHEMA_V002` exactly (40 columns = 17
  lineage + `label_config_hash` + 8 label + 14 support; `label_schema_version =
  "v001"`; column names verbatim); re-map the two terminal-specific lineage
  columns per row — `source_phase_4bm_j_gate_report_sha256` → Phase 4bn-T
  feature-layer gate SHA (`db731d1b…`);
  `source_feature_successor_state_sha256` → Phase 4bn-P normalized-layer gate SHA
  (`3452fd9d…`, the non-eligible admissibility witness replacing the absent
  Stage-5 successor-state) — recorded in a manifest
  `lineage_column_reinterpretation` block; no new label schema version; no v003.
- **Pre-v002 envelope-terminal convention:** `envelope_terminal_unix_ms` = max
  `source_transact_time_ms` / `feature_timestamp_ms` within 2024-11-30;
  `envelope_terminal_utc_date = "2024-11-30"`; horizons 1s/5s/15s/60s crossing the
  terminal censor (`horizon_censored_flag` true, label values null,
  `label_any_censored_flag` true when applicable); no 2024-12-01+ row read; no
  sealed-test row read; no holdout-boundary memo required.
- **Full-envelope label reference convention:** full 12-month label envelope
  (2024-03-01 .. 2025-02-28) represented by reference — segment manifest carries
  `full_intended_envelope_start/end` + `existing_v002_label_reference` (path
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`,
  window 2024-12-01 .. 2025-02-28, `read = false`, `mutated = false`); optional
  deferred full-envelope label reference/assembly manifest
  `microstructure_labels_aggtrades_v001__v002_full_envelope_reference_<phase-id>.json`
  defined-but-not-created; no v002 rewrite; no v003; no eligibility flip.
- **Future label output directory convention:**
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet`
  + canonical two-space `.sha256` sidecars; distinct from the published `__v002/`
  directory; not generic; not a new `__vNNN`; not v003.

### Future label manifest required fields (preserved by reference)

dataset_family / dataset_version / version / label_schema_version / segment_label
/ data_family / symbol / market / dataset_category; phase_id /
source_phase_boundary / created_at_unix_ms / created_at_utc / code_commit_sha /
base_commit_sha; column_count = 40 / lineage_column_count = 17 /
label_column_count = 8 / support_column_count = 14 / schema_column_list /
lineage_column_list / label_list / support_column_list / label_family_id /
dtype_policy / anchor_policy / future_reference_policy (pre-v002-segment-terminal
variant) / direction_threshold_policy / null_censoring_policy / horizon_list /
horizon_ms_list / forbidden_label_column_substrings; label_config_hash /
label_config_hash_input_fields / feature_config_hash = 0726b41d… /
lineage_column_reinterpretation; date_start = 2024-03-01 / date_end = 2024-11-30 /
date_count = 275 / date_list / expected_file_count = 275 / produced_file_count /
row_count / total_footprint_bytes / per_day_outputs (per-date parquet path,
SHA256, byte size, row count, per_horizon_censored_counts, invalid_price_row_count,
sidecar path, sidecar SHA256, paired source_feature_parquet_sha256);
envelope_terminal_unix_ms / envelope_terminal_utc_date = 2024-11-30 /
censored_per_horizon; source_feature_segment_manifest_path + SHA256 /
source_feature_layer_gate_report_path + SHA256 /
source_normalized_segment_manifest_path + SHA256 /
source_normalized_layer_gate_report_path + SHA256 /
source_raw_segment_manifest_path + SHA256 / source_feature_schema_version =
FEATURE_SCHEMA_V002 / source_normalized_schema_version = NORMALIZED_SCHEMA_V001 /
source_eligibility_posture = non_eligible_gate_passed_pending;
existing_v002_label_reference (read=false, mutated=false);
full_intended_envelope_start/end; research_eligible = false /
eligibility_gate_status = pending / chronological_split_policy = not_yet_defined /
governance labels (labels/targets allowed_by_future_phase_only;
ml/strategy/backtest/acquisition/paper_shadow_live/deployment/exchange_write
forbidden or unauthorized) / no_successor_authorization = true;
v002_terminal_window_mode = by_reference / existing_v002_terminal_window
(read=false, feature_normalized_raw_dates_read=false) / sealed_test_split_touched
= false / test_holdout_touched = false / test_rows_loaded = 0; label_computation =
non_eligible_pre_v002_segment / ml_use = forbidden / diagnostics_use = forbidden /
strategy_use = forbidden / backtest_use = forbidden; partitioning rule
<SYMBOL>/<YYYY>/<MM>/ ; primary key symbol, utc_date, agg_trade_id, row_index;
storage format Parquet; sidecar policy canonical two-space `.sha256`; Phase 4bn-L
budget witnesses.

### Future label manifest forbidden fields (preserved by reference)

no ML / model / score / prediction / signal / entry / exit / PnL / equity /
profit / loss / position / backtest / strategy / alpha / edge / diagnostic-score /
statistics / research-quality fields; no field implying research_eligible true; no
eligibility_gate_status other than pending; no chronological_split_policy other
than not_yet_defined; no diagnostics_authorized true; no ml_authorized true; no
research-ready / admissible-for-ML / approved-for-backtest claim; no Stage-5
research-use successor-state reference as required precondition; no
stage_5_label_cleared true; no label_family_research_use_authorized true; no v003
/ mark-price / funding / open-interest / order-book / spot / cross-venue / tick /
ETHUSDT fields; no extra horizon beyond 1s/5s/15s/60s; no barrier /
target-before-stop / stop / MFE / MAE / R-multiple / PnL-label semantics.

### Future label execution & label-layer gate implications (preserved by reference)

A future separately-authorized label-only execution phase must build a bounded
new `phase4bn_*` wrapper reusing the locked primitives (`labels_schema_v002`,
`labels_compute_v002`, `labels_io_v002`, `labels_manifest_v002` validation
helpers, `labels_validation`); add the selected non-eligible-source precondition,
segment-scoped config-hash builder, lineage re-mapping, pre-v002 envelope
terminal, segment-scoped path/manifest helpers, and Phase 4bn-L preflight/budget
caps; read only the approved 275 feature + 275 normalized segment dates (SHA256
verified); never open the published `__v002` families; never read v002 terminal or
sealed-test dates; write only label Parquet + canonical sidecars under the
selected segment directory plus one non-eligible label segment manifest + sidecar;
refuse overwrite; atomic write-then-rename; preserve the locked 40-column
`LABEL_SCHEMA_V002` and the causal forward-return/direction semantics and the
forbidden-substring guard; leave the published label `__v002` byte-for-byte
unchanged; obey the Phase 4bn-L budgets (label footprint 75 GiB warn / 125 GiB
hard; runtime 4 h warn / 8 h hard; temp 50 GiB warn / 100 GiB hard; total
derived-stack 250 GiB warn / 300 GiB hard; D: ≥ 500 GiB before / fail closed below
350 GiB during) and stop before writing on any breach; leave all outputs
non-eligible; commit no data artefact; create no ML / diagnostics / strategy / PnL
/ backtest / research outputs / database / v003 / compacted Parquet; carry offline
tests; preserve the Phase 4aw always-raises invariant. A future separately
authorized label-layer eligibility gate (read-only, segment-scoped) should
validate the manifest field contract + forbidden-field absence, every per-date
Parquet + sidecar + recomputed SHA256, date count = 275, contiguous dates
2024-03-01 .. 2024-11-30, totals/footprint/per-horizon-censored/invalid-price
counts, the exact 40-column `LABEL_SCHEMA_V002` + forbidden-substring guard, the
segment-scoped `label_config_hash` recomputation, the recomputed pre-v002 envelope
terminal with correct censoring (no reference row past 2024-11-30), and
predecessor integrity (Phase 4bn-S `4881eb87…`, Phase 4bn-T `db731d1b…` PASS,
Phase 4bn-O `0e96ae37…`, Phase 4bn-P `3452fd9d…` PASS); confirm the published
`__v002` label family was not mutated, the v002 terminal feature/normalized/raw
window and sealed-test split were not read, and `research_eligible` / 
`eligibility_gate_status` remain `false` / `pending`. A passing label-layer gate
must not flip eligibility and must not authorize ML / diagnostics / strategy /
split policy / backtests / any successor.

### Sealed-test and v002 terminal boundary (preserved)

The pre-v002 label segment covers 2024-03-01 .. 2024-11-30 — no sealed-test dates
and no v002 terminal dates. Forward horizons 1s/5s/15s/60s keep references inside
2024-03-01 .. 2024-11-30; labels near the end of 2024-11-30 censor rather than
reading 2024-12-01+. The v002 terminal feature/normalized/raw windows and the
published label `__v002` family are by reference only and unread/immutable. The
sealed v002 test split 2025-02-14 .. 2025-02-28 remains untouched
(`sealed_test_split_touched = false`, `test_holdout_touched = false`,
`test_rows_loaded = 0`). A holdout-boundary memo is not required for the
conservative pre-v002-only label scope; it is required only if a future design
proposes reading the v002 terminal window or sealed-test dates.

### Explicit confirmations

- Phase 4bn-V is merge-complete on `main` after this merge.
- Project completion requires the SHA-finalization commit
  (`docs(phase-4bn-v): finalize merge closeout shas`).
- Label-only execution / any successor is **NOT authorized**.
- `research_eligible` remains `false`; `eligibility_gate_status` remains
  `pending`; no manifest eligibility transition occurred.
- v003 remains forbidden and absent; the published `__v002`
  normalized/feature/label families remained immutable; the v002 terminal
  raw/normalized/feature window remained by-reference only and unread; the
  sealed-test split remained untouched.
- No local data was read; no local data was created; no local
  `data/microstructure` or `data/research` artefact was opened, hashed, counted,
  inspected, created, staged, or committed.
- No acquisition was run, no endpoints were called, no archives were downloaded,
  no HEAD preflight was run, no raw gate was rerun, no normalization was rerun, no
  normalized-layer gate was rerun, no feature execution was rerun, no
  feature-layer gate was rerun, no label derivation was run, no label gate was
  run, no local raw zip contents were inspected, no local normalized Parquet files
  were read, no local feature Parquet files were read, no local label files were
  read, no local manifest or gate report was read, no v002 terminal window was
  read, no test holdout was touched, no ML was trained, no model scoring was
  performed, no predictions were generated, no diagnostics were run, no backtests
  were run, no strategy/signal/PnL work was performed, no storage migration
  occurred, no database was created, no Parquet was compacted, no v003 dataset was
  created, no manifest eligibility transition occurred, no `data/research`
  artefacts were created or committed, no `data/microstructure` artefacts were
  created or committed, and no paper/shadow/live/exchange-write/credentials/MCP/
  Graphify work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
