# Phase 4bn-W — Label-Only Pre-V002 Segment

## 1. Purpose

This phase is a **code + tests + docs + local gitignored label artefact
generation** deliverable. It implements and runs a bounded **label-only
execution** over the Phase 4bn-S / 4bn-T pre-v002 BTCUSDT Binance USDⓈ-M
futures aggTrades **feature** segment and its Phase 4bn-O / 4bn-P
**normalized** predecessor (2024-03-01 .. 2024-11-30 inclusive UTC; 275
days; 400,001,695 rows), exactly following the Phase 4bn-V selected label
manifest/versioning, non-eligible-source precondition, segment-scoped
`label_config_hash`, lineage re-mapping, and pre-v002 envelope-terminal
conventions.

It produces a bounded new `phase4bn_*` label wrapper, an offline test
module, 275 local gitignored non-eligible label Parquet files + 275
canonical sidecars, and one non-eligible pre-v002 label **segment**
manifest + sidecar — leaving every output **non-eligible** and
**uncommitted**, and authorizing no ML, no diagnostics, no strategy, no
PnL, no backtests, no research-eligibility flip, no split policy, and no
successor.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`. **Active Claude Code
  lightweight workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`.
- **Branch:** `phase-4bn-w/label-only-pre-v002-segment`.
- **Base `main` SHA:** `e53652a11e8586d26803aebb616a87fccd571353`
  (`docs(phase-4bn-v): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` verified in sync; the Phase 4bn-V
  SHA-finalization `e53652a`, merge-closeout `02b3259`, merge `7d6409c`,
  and branch `6785495` are present on `main`.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (reads local
  feature + normalized segments; generates local gitignored label
  artefacts; implements a bounded wrapper + segment-scoped config-hash
  builder; prepares the label layer for a future label-layer gate).
- **Working-tree expectation at start:** only the untracked transient
  `.claude/scheduled_tasks.lock`; the gitignored namespaces
  `data/microstructure/` (`.gitignore:85`) and `data/research/`
  (`.gitignore:88`) exist locally and remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** code + tests + docs + local gitignored label artefact
generation.

**Allowed work performed:** read the committed docs/code/tests and the
approved local inputs (Phase 4bn-S feature segment + manifest + sidecar;
Phase 4bn-T feature-layer gate report; Phase 4bn-O normalized segment +
manifest + sidecar; Phase 4bn-P normalized-layer gate report); implement a
bounded new `phase4bn_w` wrapper + offline tests; generate 275 local
gitignored non-eligible label Parquet + sidecars + 1 label segment
manifest + sidecar; create two tracked docs; update
`current-project-state.md` narrowly.

**This phase did NOT and must NOT:** run a label-layer eligibility gate;
run ML, diagnostics, strategy, signals, PnL, or backtests; create
`data/research` outputs / model outputs / predictions / scores /
paper-shadow-live artefacts; read the published label/feature/normalized
`__v002` family content or the v002 terminal raw/normalized/feature window
or any sealed-test date; flip `research_eligible` or transition
`eligibility_gate_status`; create a database / `.duckdb` / `.sqlite`,
compact Parquet, or create v003; commit any `data/microstructure` or
`data/research` artefact; or authorize any successor.

## 4. Evidence base and input boundary

**Committed evidence read (read-only):** the process standards
(`merge-closeout-standard.md`, `phase-risk-tiering-standard.md`,
`phase-workflow-standard.md`, `phase-prompt-template.md`,
`operator-report-standard.md`); the Phase 4bn-V memo / merge-closeout /
closeout; the Phase 4bn-U / 4bn-T / 4bn-S / 4bn-R / 4bn-P / 4bn-O / 4bn-L
reports; the data specs (`data-requirements.md`, `historical-data-spec.md`,
`timestamp-policy.md`, `dataset-versioning.md`, `database-design.md`); the
committed label tooling (`labels_schema_v002.py`, `labels_io_v002.py`,
`labels_manifest_v002.py`, `labels_compute_v002.py`, `labels_io.py`,
`labels_validation.py`, `label_gate*.py`, `multiday_label_gate*.py`); the
v002 label orchestrator `scripts/phase4bm_o_compute_multiday_labels.py`;
the Phase 4bn-S / 4bn-T scripts as the bounded-wrapper template; and the
committed test surface.

**Approved local inputs read by the wrapper:** the Phase 4bn-S feature
segment manifest + sidecar; the 275 feature Parquet (four anchor columns
`row_index, agg_trade_id, feature_timestamp_ms, source_transact_time_ms`)
+ per-day SHA verification; the Phase 4bn-T feature-layer gate report; the
Phase 4bn-O normalized segment manifest + sidecar; the 275 normalized
Parquet (`transact_time_ms, price, agg_trade_id, utc_date, row_index`) +
per-day SHA verification; the Phase 4bn-P normalized-layer gate report.

**Input boundary honoured:** no published `__v002` label / feature /
normalized Parquet or manifest content was read; no v002 terminal
(2024-12-01 .. 2025-02-28) raw / normalized / feature window was read; no
sealed-test (2025-02-14 .. 2025-02-28) date was read; no `data/research`
artefact was read or written. The README was treated as potentially stale.

## 5. Phase 4bn-V selected conventions carried forward

The wrapper implements exactly the Phase 4bn-V (merge-complete on `main`)
selected conventions:

1. **Label manifest/versioning** — a phase-scoped **pre-v002 label segment
   manifest** `microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json`
   (`dataset_version: "v002"`, `label_schema_version: "v001"`,
   `segment_label: "pre_v002_segment"`); tied to the existing v002 label
   family but marked a pre-v002 backward segment; **no v003**; published
   `__v002` label manifest/directory untouched and immutable.
2. **Non-eligible-source precondition** — Phase 4bn-S feature segment
   manifest (`4881eb87…`) + Phase 4bn-T feature-layer gate PASS
   (`db731d1b…`) + Phase 4bn-O normalized segment manifest (`0e96ae37…`) +
   Phase 4bn-P normalized-layer gate PASS (`3452fd9d…`), replacing the
   Phase 4bm-L Stage-5 research-use successor-state; source segments
   verified `research_eligible=false` / `eligibility_gate_status=pending`;
   no Stage-5 successor required/created; the published v002 feature config
   hash `819cfa7a…` is rejected; the segment `feature_config_hash` is
   `0726b41d…`.
3. **Segment-scoped `label_config_hash`** —
   `build_label_config_hash_v002_pre_v002_segment` (§11).
4. **Lineage re-mapping** — `LABEL_SCHEMA_V002` kept exactly; the two
   terminal-specific lineage columns re-mapped per row (§12).
5. **Pre-v002 envelope terminal** — locked to the segment terminal (§13).
6. **Full-envelope label reference** — by reference only; segment manifest
   carries `full_intended_envelope_*` + `existing_v002_label_reference`
   (`read=false`, `mutated=false`); no optional companion manifest created.

## 6. Phase 4bn-S / 4bn-T feature prerequisite carried forward

- Phase 4bn-S feature segment: 2024-03-01 .. 2024-11-30; 275 feature
  Parquet + sidecars; 400,001,695 rows; footprint 54,254,406,538 bytes;
  schema exactly `FEATURE_SCHEMA_V002` (62 columns);
  `feature_config_hash = 0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`;
  manifest SHA256 `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`
  (+ sidecar `f2ca2f48…92e5`); `research_eligible=false`,
  `eligibility_gate_status=pending`.
- Phase 4bn-T feature-layer gate: 27/27 PASS; verdict
  `FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  gate report SHA256 `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`;
  `input_feature_manifest_sha256` == the Phase 4bn-S manifest SHA.

The wrapper re-verifies all of the above before any output is written and
re-hashes them post-write to confirm immutability.

## 7. Phase 4bn-O / 4bn-P normalized prerequisite carried forward

- Phase 4bn-O normalized segment: 2024-03-01 .. 2024-11-30; 275 normalized
  Parquet; 400,001,695 rows; footprint 3,954,532,918 bytes; manifest
  SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`
  (+ sidecar `5d7dcbef…6402`); `research_eligible=false`,
  `eligibility_gate_status=pending`.
- Phase 4bn-P normalized-layer gate: 25/25 PASS; verdict
  `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  gate report SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`.

The label kernel reads anchor/reference **trade prices** from the
normalized Parquet (`load_normalized_day_ref`) and the four anchor columns
from the feature Parquet. The wrapper cross-binds the two segments by
verifying that each feature inventory entry's
`paired_source_normalized_parquet_sha256` equals the normalized inventory
entry's `parquet_sha256` for the same date.

## 8. Phase 4bn-L budget carried forward

LABEL-layer caps applied verbatim: label footprint warn 75 GiB / hard cap
125 GiB; runtime warn 4 h / hard cap 8 h; temporary workspace warn 50 GiB
/ hard cap 100 GiB; total derived-stack warn 250 GiB / hard cap 300 GiB;
`D:` free ≥ 500 GiB before execution; fail closed if `D:` free falls below
350 GiB during execution. The preflight estimates label / temp / total
footprints and the `D:` floor before any write; per-day budget enforcement
fails closed on any hard-cap breach.

## 9. Label-only execution contract

- **Input:** Phase 4bn-S feature segment (anchors) + Phase 4bn-O
  normalized segment (prices) for 2024-03-01 .. 2024-11-30 only; v002
  terminal / sealed-test by reference only / unread.
- **Output family:** label artefacts only — schema exactly
  `LABEL_SCHEMA_V002` (40 columns = 17 lineage + `label_config_hash` + 8
  label + 14 support); horizons 1s/5s/15s/60s; causal forward-return /
  forward-direction only (no barrier / target-before-stop / stop / MFE /
  MAE / R-multiple / strategy / signal / PnL); forbidden-substring column
  guard enforced.
- **Output storage:** segment-scoped gitignored directory
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet`
  + canonical two-space `.sha256` sidecars; one non-eligible label segment
  manifest + sidecar under `data/microstructure/manifests/`. Refuse
  overwrite; atomic write-then-rename.
- **Posture:** `research_eligible=false`, `eligibility_gate_status=pending`,
  `no_successor_authorization=true`; nothing committed.

## 10. Wrapper implementation

`scripts/phase4bn_w_compute_pre_v002_labels.py` is a bounded, offline,
network-free orchestrator that reuses the locked v002 label primitives
unchanged — `labels_compute_v002` (`compute_aggtrade_labels_v002_for_day`,
`load_normalized_day_ref`, `write_label_dataset_v002`, `LabelLineageV002`,
`LabelMultiDaySummaryV002`), `labels_io` (atomic writers + path guards),
and `labels_schema_v002` (schema + policy constants) — and adds only
bounded orchestration:

- the §15 non-eligible-source precondition (four predecessor artefacts
  verified by SHA + posture + gate PASS), replacing the Stage-5
  successor-state;
- a segment-scoped path helper `derive_label_segment_parquet_path` that
  routes outputs into the `…_pre_v002_segment_4bn_w/` directory and fails
  closed on any path under the published `__v002` / generic label
  directory or any v003 token;
- the §11 segment-scoped `label_config_hash` builder;
- the §12 lineage re-mapping fed through `LabelLineageV002`;
- the §13 pre-v002 envelope terminal (computed from the normalized
  inventory, asserted on 2024-11-30);
- a rolling normalized-day reference cache (each normalized day loaded once
  and reused as `current_day` after serving as the prior iteration's
  `next_day`);
- the Phase 4bn-L preflight + per-day budget enforcement;
- a label segment manifest builder + a label-appropriate field contract
  (required fields present; forbidden fields absent; governance posture
  non-eligible / pending / no-successor) + atomic manifest writer;
- post-write source immutability re-hash of all four predecessor artefacts.

The kernel is **segment-neutral**: it writes whatever lineage SHAs are
passed via `LabelLineageV002` into the per-row lineage columns and writes
outputs to whatever `labels/`-resident path is supplied — so the §12
lineage re-mapping and the §10 segment output directory required **no
change to any `src/prometheus` module**. No source module, no committed
script, and no prior test was modified.

## 11. Segment-scoped label_config_hash implementation

`build_label_config_hash_v002_pre_v002_segment(...)` returns a
deterministic SHA256 over a canonical-JSON payload (sorted keys, ASCII, no
whitespace) that **preserves** the locked v002 label policy fields
(`ANCHOR_POLICY_V002`, `DIRECTION_THRESHOLD_POLICY_V002`,
`NULL_CENSORING_POLICY_V002`, `DTYPE_POLICY_V002`, and the schema / horizon
/ lineage lists) but:

- **re-specifies the future-reference envelope clause** — the payload uses
  `_segment_future_reference_policy()`, which replaces the locked v002
  clause `envelope_terminal_unix_ms=max_source_transact_time_ms_across_v002_90day_envelope`
  with `…_across_pre_v002_segment_2024-03-01_to_2024-11-30` (failing closed
  if the locked v002 clause is absent — kernel-drift guard);
- **replaces the successor-state input** with the
  `source_feature_layer_gate_report_sha256` (Phase 4bn-T, `db731d1b…`) and
  `source_normalized_layer_gate_report_sha256` (Phase 4bn-P, `3452fd9d…`)
  witnesses;
- **binds** `source_feature_manifest_sha256` (`4881eb87…`),
  `source_normalized_manifest_sha256` (`0e96ae37…`),
  `source_raw_manifest_sha256` (`1659e6da…`), and
  `feature_config_hash = 0726b41d…` — and **fails closed** if
  `feature_config_hash == 819cfa7a…` (the published v002 lock);
- **adds** a `segment_label = "pre_v002_segment"` discriminator.

Verbatim reuse of `build_label_config_hash_v002` is rejected because its
hashed `FUTURE_REFERENCE_POLICY_V002` string literally encodes the v002
90-day envelope. The computed segment hash for this run is
**`b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`**
(verified identical in the dry-run preflight and the real run). The
manifest records `label_config_hash_input_fields` (the exact hashed field
list) for reproducibility.

## 12. Lineage re-mapping implementation

`LABEL_SCHEMA_V002` is preserved **exactly** (40 columns,
`label_schema_version = "v001"`, column names verbatim). The two
terminal-specific lineage columns are re-mapped **per row** by the values
passed into `LabelLineageV002`:

- `source_phase_4bm_j_gate_report_sha256` → Phase 4bn-T feature-layer gate
  report SHA (`db731d1b…`) — the segment's feature-gate witness;
- `source_feature_successor_state_sha256` → Phase 4bn-P normalized-layer
  gate report SHA (`3452fd9d…`) — the non-eligible admissibility witness
  that replaces the absent Stage-5 successor-state.

The remaining lineage columns carry their natural segment values:
`source_feature_manifest_sha256 = 4881eb87…`, per-day
`source_feature_parquet_sha256`, `source_normalized_manifest_sha256 =
0e96ae37…`, `source_raw_manifest_sha256 = 1659e6da…`, plus the per-row
identity columns (`symbol`, `utc_date`, `row_index`, `agg_trade_id`,
`feature_timestamp_ms`, `source_transact_time_ms`) and the constant
`label_config_hash`. The authoritative re-mapping is recorded in the
segment manifest `lineage_column_reinterpretation` block. **No new label
schema version; no v003.**

## 13. Pre-v002 envelope-terminal implementation

`envelope_terminal_unix_ms` is computed as the maximum
`last_transact_time_ms` across the 275 normalized inventory entries and
asserted to fall on **2024-11-30** (it equals the last day's last
`transact_time_ms`). For this run the terminal is **`1733011199331`**
(2024-11-30 23:59:59.331 UTC); `envelope_terminal_utc_date = "2024-11-30"`.
For each feature row and horizon `H ∈ {1s,5s,15s,60s}`, the kernel censors
(`horizon_censored_flag` true, label values null, `label_any_censored_flag`
true) whenever `feature_timestamp_ms + H_ms > envelope_terminal_unix_ms`;
otherwise it resolves the reference row within the segment envelope
(cross-day allowed only into the next in-segment day; the last day uses
`next_day=None`). No 2024-12-01+ row and no sealed-test row is read.

## 14. Preflight and fail-closed controls

The preflight verifies the four predecessor SHAs + posture + gate PASS,
resolves and cross-binds the 275 per-day feature+normalized sources,
computes the envelope terminal, and estimates label / temp / total-stack
footprints against the Phase 4bn-L caps and the `D:` ≥ 500 GiB floor —
all **before any output is written**. Per-day computation hash-verifies
each feature and normalized Parquet before compute, refuses to overwrite
any finalised output, writes atomically, and enforces the hard caps each
day (fail closed on label > 125 GiB, runtime > 8 h, temp > 100 GiB,
total-stack > 300 GiB, or `D:` free < 350 GiB). The 53 enumerated
fail-closed stop conditions from the authorization prompt are covered by:
the branch/segment-naming guards, the four-artefact precondition, the
per-day SHA verification, the segment date guard (rejecting ≥ 2024-12-01
and the sealed-test window), the envelope-terminal assertion, the
output-path-under-`labels/` guard, the refuse-overwrite guards, the
manifest field contract, and the post-write immutability re-hash. Any
breach aborts before the segment manifest is written; partial per-day
Parquets remain independently verifiable via their sidecars and remain
non-eligible / gitignored.

## 15. Test coverage

`tests/research/microstructure/test_phase4bn_w_label_pre_v002.py` (36
offline tests, synthetic fixtures + temp dirs only; no production / sealed
data; no network; no local `data/microstructure` reads; no `data/research`
writes) covers: network-free / no-forbidden-import posture; identity
constants; segment output path layout and rejection of bad symbol /
published-`__v002` / generic / v003 paths; the segment date guard
(rejecting 2024-12-01+ and 2025-02-14..28); the segment-scoped
`label_config_hash` determinism, sensitivity to `feature_config_hash` and
to each gate SHA, rejection of the published `819cfa7a…` config hash and of
non-hex inputs, the re-specified envelope clause, and distinctness from a
v002-style payload; exact `LABEL_SCHEMA_V002` preservation and the
lineage-remap column keys; the forbidden-substring column guard; the
manifest field contract (accepts a valid manifest; rejects
research_eligible=true, eligible status, the published config hash, a
forbidden field, a split-policy change, an authorized flag, and an
allowed-ML governance value); the Phase 4bn-L budget caps and the
`_enforce_budgets` hard-cap / `D:`-floor / warning behaviour; and the gate
report verification (PASS, rejection of research_eligible_after=true, wrong
check count, SHA mismatch) and the identity/posture helper. All 36 tests
pass.

## 16. Real label execution

The bounded wrapper was run once over the real local pre-v002 segment via
`python scripts/phase4bn_w_compute_pre_v002_labels.py` (defaults resolve
the four predecessor artefacts and the gitignored `labels/` + `manifests/`
roots). The run computed labels for all 275 dates 2024-03-01 .. 2024-11-30
in strict chronological order, hash-verified each feature and normalized
Parquet before compute, wrote 275 label Parquet + 275 sidecars under the
segment directory, and wrote one label segment manifest + sidecar. All 6
preconditions, all 9 month-boundary budget checks, the aggregate check, the
manifest field-contract check, the write, and the post-write source
immutability re-hash returned **PASS** (overall status `pass`).

- **Measured runtime:** 4,217.80 s (≈1.17 h) — below the 4 h warning / 8 h
  hard cap.
- **Per-month budget checks (2024-03 … 2024-11):** all PASS; warning
  thresholds crossed: **none**; hard caps crossed: **none**.

## 17. Local gitignored outputs

- **Label Parquet count:** 275; **label sidecar count:** 275 (confirmed on
  disk).
- **Label output directory:**
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w/BTCUSDT/<YYYY>/<MM>/`.
- **Total label rows:** 400,001,695 (== source feature / normalized rows).
- **Total label footprint:** 15,654,082,679 bytes (≈14.58 GiB) — far below
  the 75 GiB warning / 125 GiB hard cap.
- All outputs gitignored (`.gitignore:85`) and **uncommitted**.

## 18. Manifest and sidecar summary

- **Label segment manifest:**
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json`;
  SHA256 `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`.
- **Manifest sidecar:** `…_4bn_w.json.sha256`; SHA256
  `636a4c1a0159364e7d67f502dda48664f18fc16545c993935e6429ccdf868239`.
- The manifest records all Phase 4bn-V required fields (identity, schema,
  policy, config hash + input fields + lineage re-mapping, window /
  inventory, censoring aggregates, non-eligible-source lineage,
  by-reference v002 / sealed-test witnesses, governance / boundary /
  non-authorization declarations, budget witnesses) and passes the
  field-contract + forbidden-field scan.

## 19. Row counts, footprint, censoring, and runtime

- **Total rows:** 400,001,695 (per-date row counts == source feature /
  normalized rows; aggregate row count == 400,001,695).
- **`label_config_hash`:**
  `b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`
  (constant across the segment; identical in the dry-run and the real run).
- **`envelope_terminal_unix_ms`:** `1733011199331`;
  **`envelope_terminal_utc_date`:** 2024-11-30.
- **Per-horizon censored counts (segment totals):** 1s = 3, 5s = 20,
  15s = 42, 60s = 216 (total 281 rows — exactly the last ≤60 s of
  2024-11-30 whose forward target crosses the segment terminal; no
  2024-12-01+ row was read).
- **Invalid-price row count:** 0.
- **`D:` free before / min-observed / after:** 1,278,562,484,224 B
  (≈1190.7 GiB) / 1,262,907,052,032 B (≈1176.2 GiB) / 1,262,907,052,032 B
  (≈1176.2 GiB) — all far above the 500 GiB pre-floor and 350 GiB
  in-execution floor.

## 20. Boundary confirmations

- no published label `__v002` Parquet / manifest content read; no published
  feature / normalized `__v002` content read;
- no v002 terminal raw / normalized / feature window read; no sealed-test
  (2025-02-14 .. 2025-02-28) date read; `test_rows_loaded = 0`;
- no `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transition; segment outputs `research_eligible=false`,
  `eligibility_gate_status=pending`, `no_successor_authorization=true`;
- no ML / model scoring / predictions / diagnostics / strategy / signals /
  PnL / backtests; no label-layer gate run;
- no `data/research` output; no `data/microstructure` or `data/research`
  artefact committed; no database / `.duckdb` / `.sqlite`; no Parquet
  compaction; no v003;
- no acquisition / endpoint / archive / HEAD preflight; no feature /
  feature-gate / normalization / normalized-gate / raw rerun;
- no `src/prometheus` module modified; no prior committed script or test
  modified; the locked 40-column `LABEL_SCHEMA_V002` and the
  forbidden-substring column guard preserved verbatim;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked); all four predecessor artefacts byte-identical pre/post.

## 21. Validation

- `ruff check scripts/phase4bn_w_compute_pre_v002_labels.py
  tests/research/microstructure/test_phase4bn_w_label_pre_v002.py` → All
  checks passed.
- `pytest tests/research/microstructure/test_phase4bn_w_label_pre_v002.py`
  → 36 passed.
- Predecessor regression (`test_phase4bn_t_feature_layer_gate.py`,
  `test_phase4bn_s_feature_pre_v002.py`,
  `test_phase4bn_p_normalized_layer_gate.py`,
  `test_phase4bn_o_normalization_pre_v002.py`) co-run with the new module →
  **155 passed** (36 new + 119 predecessor), 0 failed.
- `mypy src/prometheus` is the repo-standard scope; this phase added **no**
  `src/prometheus` change (the wrapper + segment-scoped config-hash builder
  / lineage re-mapping / manifest builder live under `scripts/`, outside
  the repo-standard mypy scope), so `mypy src/prometheus` was **not run**
  (no in-scope change to validate).
- `git diff --check` → clean; `git check-ignore -v data/microstructure/` →
  `.gitignore:85` (the label Parquet + manifest both resolve to
  `.gitignore:85`); `git check-ignore -v data/research/` → `.gitignore:88`;
  `git status --short` shows the five tracked files plus the expected
  untracked `.claude/scheduled_tasks.lock`, with **no** staged/tracked
  `data/microstructure` or `data/research` artefact.

## 22. Result state

`LABEL_EXECUTION_SUCCEEDED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.

The bounded label-only execution completed with overall status `pass`: 275
non-eligible label Parquet + 275 sidecars + 1 segment manifest + 1 sidecar
were produced over 2024-03-01 .. 2024-11-30 (400,001,695 rows; 14.58 GiB),
the segment-scoped `label_config_hash` and pre-v002 envelope terminal were
applied, all four predecessor artefacts remained byte-identical, no v002
terminal / sealed-test date was read, and the segment remains
`research_eligible=false` / `eligibility_gate_status=pending` /
`no_successor_authorization=true`.

## 23. Decision

`RECOMMEND_AUTHORIZE_LABEL_LAYER_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale: the predeclared preferred decision when label execution succeeds
is exactly this option. With the local pre-v002 label segment now produced
and structurally self-describing (segment manifest + per-day inventory +
sidecars), the cleanest next technical step is a separately-authorized,
read-only **label-layer eligibility gate** that recomputes and validates
the segment (field contract, per-date Parquet/sidecar SHA recomputation,
exact 40-column `LABEL_SCHEMA_V002`, segment-scoped `label_config_hash`
recomputation, envelope-terminal censoring, and predecessor integrity)
**without** flipping eligibility or authorizing any downstream use — exactly
mirroring the normalize → normalized-gate (4bn-O → 4bn-P) and feature →
feature-gate (4bn-S → 4bn-T) arcs. **This phase does not authorize that
gate; the operator decides separately. No successor is authorized from
inside Phase 4bn-W.**

## 24. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-W is **branch-complete
only**; not merged into `main`; not project-complete until a separately
authorized merge phase records its merge-closeout on `main` (Tier 1).

**Operator options (each subject to separate operator authorization; none
authorized here):** remain paused; request a merge prompt for Phase 4bn-W;
separately authorize a **label-layer eligibility gate** (the recommended
follow-on — a bounded read-only segment-scoped gate validating the label
segment manifest field contract, per-date Parquet + sidecar SHA
recomputation, the exact 40-column `LABEL_SCHEMA_V002`, the segment-scoped
`label_config_hash` recomputation, the envelope-terminal censoring, and
predecessor integrity, **without** flipping eligibility); separately
authorize a holdout-boundary memo (only if a future scope touches the v002
terminal or sealed-test dates — not required here); a source-policy
documentation memo; a process-doc `D:` path-string update; or reject
further ML-baseline successors and close the ML-baseline arc.

## 25. Explicit non-authorizations

Phase 4bn-W did **not** and does **not** authorize: a label-layer
eligibility gate; ML training / model scoring / predictions / diagnostics;
strategy / signals / PnL / backtests; feature / feature-gate /
normalization / normalized-gate / raw rerun; acquisition / endpoint /
archive / HEAD preflight; any `research_eligible` flip or
`eligibility_gate_status` / `chronological_split_policy` /
`diagnostics_authorized` / `ml_authorized` transition; `data/research` or
`data/microstructure` artefact creation-then-commit; storage migration;
DuckDB / SQLite / database creation; Parquet compaction; v003 creation;
ETHUSDT / mark-price / spot / cross-venue / order-book / tick / extra
horizons; paper / shadow / live-readiness / deployment / exchange-write /
production keys; any Phase 5; or any successor phase. Every retained
verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1
/ C1) and every project lock (§11.6; round-trip; §1.7.3; the Phase 3/4
governance chain; Phase 4ak M0; Phase 4al no-rescue; Phase 4aw always-raises
invariant; Phase 4bb-F canonical path policy; Phase 4bl-F risk tiers; Phase
4bn-L budgets; Phase 4bn-N / 4bn-R / 4bn-V conventions) is preserved
verbatim.

## 26. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: a new Phase
4bn-W prose paragraph appended after the Phase 4bn-V paragraph, and a new
`Current phase:` block for Phase 4bn-W inserted ahead of the Phase 4bn-V
block. All prior Phase 4bn-A … 4bn-V paragraphs/blocks are preserved
verbatim as labelled historical context. No other section was changed. No
`data/microstructure` or `data/research` artefact was committed.
