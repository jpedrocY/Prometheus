# Phase 4bn-R — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-R — Docs-Only Feature Manifest / Versioning Memo.
- **Type:** docs-only / feature-manifest / feature-versioning /
  non-eligible-source precondition / boundary-contract.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-R feature manifest/versioning memo, its
  closeout, and the narrow `current-project-state.md` update onto `main` as
  project state. The phase produced **no** code, tests, scripts, data, or local
  artefacts; it is a docs-only boundary-contract memo resolving the feature
  manifest/versioning ambiguity and the non-eligible-source precondition
  divergence identified by Phase 4bn-Q.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-r/feature-manifest-versioning-memo`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `014c58add240e2c0bd2666b971cb76024942f89d`
  (`docs(phase-4bn-q): finalize merge closeout shas`).
- **Branch commit SHA (docs):** `4e7851e85f9118548cbe03d573114806303292a5`
  (`docs(phase-4bn-r): settle feature manifest versioning`).
- **Merge commit SHA:** `b7d13e4f3d079194983212df929f2a0b61a1f4cb`
  (`docs(phase-4bn-r): merge feature manifest versioning`).
- **Merge-closeout commit SHA:** this commit
  (`docs(phase-4bn-r): add merge closeout`) — recorded verbatim in the final
  operator report.
- **SHA-finalization commit SHA:** the subsequent commit
  (`docs(phase-4bn-r): finalize merge closeout shas`) — its own hash becomes the
  new `main` tip; recorded verbatim in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit;
  `main == origin/main` after push (recorded in the final operator report).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `docs(phase-4bn-r): merge feature manifest versioning`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
  (recorded at the final operator report after the SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-R
    paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-Q
    paragraphs and blocks preserved verbatim as labelled historical context;
    117 insertions, 0 deletions — insertion-only);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-r_feature-manifest-versioning-memo.md`
    (added — the feature manifest/versioning memo, 23 sections);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-r_closeout.md`
    (added — branch closeout).
- **Source / tests / scripts / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No published manifest, sidecar, gate report,
  successor-state artefact, `.gitignore`, `pyproject.toml`, `README.md`, or MCP
  file was modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 2 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 117 +++
 .../2026-06-04_phase-4bn-r_closeout.md             | 201 +++++
 ...phase-4bn-r_feature-manifest-versioning-memo.md | 939 +++++++++++++++++++++
 3 files changed, 1257 insertions(+)
```

The diff matches the expected change set (insertion-only; docs-only).

## 6. Verdict

**MEMO RECORDED.** Phase 4bn-R resolved, from committed docs and committed
tooling only, the feature manifest/versioning ambiguity and the
non-eligible-source precondition divergence that Phase 4bn-Q deferred. It
selected: (a) a **phase-scoped feature segment manifest** mirroring the merged
raw-layer (Phase 4bn-J-R2 / 4bn-K) and normalized-layer (Phase 4bn-N / 4bn-O)
precedents — a backward segment of the v002 envelope, not a new `__vNNN`, not a
write into the published `__v002` feature family, not v003; (b) a
**non-eligible-source precondition** anchored on the Phase 4bn-P normalized-layer
gate PASS over the Phase 4bn-O normalized segment manifest (both verified by
SHA256), replacing the existing Stage-3 research-eligible successor-state
precondition; (c) a **version-suffixed segment output directory** distinct from
the published `__v002/` feature directory; and (d) a **by-reference full
12-month feature envelope** (mandatory segment manifest now; optional deferred
full-envelope reference manifest later). The decision is
`RECOMMEND_AUTHORIZE_FEATURE_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(result state `RECORD_FEATURE_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`),
mirroring how the normalization arc went readiness (4bn-M) →
manifest/versioning memo (4bn-N) → execution (4bn-O) → gate (4bn-P). The merge
lands the memo + closeout + narrow state update on `main`; the project remains
paused; the segment remains non-eligible.

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-R is docs-only: it created no local artefact under
`data/microstructure/` or `data/research/`, read no local data, hashed no local
data, and counted no local data. The pre-existing Phase 4bn-O normalized outputs
and Phase 4bn-P normalized-layer gate report remain local, gitignored
(`.gitignore:85`), and uncommitted; this phase did not touch them.

## 8. Validation results

Docs-only validation (no code/test/script/config surface; no real gate /
normalization / feature run):

- `git diff --check` → clean (no whitespace errors).
- `git diff --name-status main..branch` (pre-merge) → exactly the 3 expected
  docs files (M `current-project-state.md`; A memo; A closeout).
- `git diff --stat main..branch` (pre-merge) → `3 files changed, 1257
  insertions(+)`.
- `git status --short` → only `.claude/scheduled_tasks.lock` untracked; no
  `data/microstructure/` or `data/research/` artefact staged.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- **ruff / pytest / mypy:** not required — Phase 4bn-R adds no
  code/test/script surface. The relevant validation surface for a docs-only
  phase is git status, diff review, `git diff --check`, gitignore confirmation,
  and SHA checks.
- **Markdown validator:** no repo-standard markdown lint tooling is configured;
  none was run (running an ad-hoc one is unnecessary and could create outputs).

## 9. Upstream immutability evidence

**n/a — phase did not access any local artefact.** Phase 4bn-R read only
committed repository Markdown and committed code/tests; it opened no local
normalized/raw/feature/label/manifest/sidecar/gate-report/successor-state or
`data/research` artefact. The merge modified no `data/microstructure/` file.
The published normalized and feature `__v002` families, the Phase 4bn-O pre-v002
normalized segment, and the Phase 4bn-P gate report were untouched. SHA256
digests cited in the memo for local gitignored artefacts (Phase 4bn-O segment
manifest `0e96ae37…d9fa`, Phase 4bn-P gate report `3452fd9d…f134`) were quoted
from committed Markdown evidence, not by reading local files.

## 10. Manifest state preservation

- No manifest was read, created, or mutated by this phase. The Phase 4bn-O
  normalized segment manifest and all prior manifests remain unchanged:
  `research_eligible: false`, `eligibility_gate_status: "pending"`; no
  transition occurred.
- `chronological_split_policy` unchanged/absent.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no test modified; no script modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no published manifest / sidecar / gate report / successor-state artefact
  modified;
- no `data/microstructure/` or `data/research/` artefact read, created,
  staged, or committed;
- no feature derivation; no feature artefact generation; no feature manifest
  creation or mutation; no feature gate execution; no label derivation;
- no normalization rerun; no raw-gate rerun; no normalized-layer-gate rerun; no
  acquisition; no endpoint / public / Binance / `data.binance.vision` call; no
  archive / CHECKSUM download; no HEAD preflight;
- no local raw zip / normalized Parquet / feature / label read; no v002
  terminal raw/normalized window read; no sealed-test read; no local manifest /
  gate-report read under `data/microstructure`;
- no diagnostics; no ML; no scoring; no predictions; no feature ranking /
  selection / pruning / engineering / tuning / calibration; no strategy /
  signal / PnL / backtest;
- no `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transition;
- no database / `.duckdb` / `.sqlite`; no Parquet compaction; no storage
  migration; no v003;
- no credential / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user
  stream / private / authenticated endpoint used;
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
- Phase 4aw `flip_research_eligible(...)` always-raises invariant (never
  invoked)
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bn-J-R1 raw-only cap amendment
- Phase 4bn-L derived-stack storage budget
- Phase 4bn-N normalization manifest/versioning convention

All prior phase results preserved verbatim. Phase 4 canonical remains
unauthorized.

## 14. No-rescue constraints

The Phase 4bn-R merge does not, and cannot, be construed as authorising:

- a feature-only execution phase, a feature-layer eligibility gate, or any
  successor (recommended only, NOT authorized);
- feature derivation, feature artefact generation, feature manifest creation or
  mutation, feature gate execution, label derivation, or research outputs;
- ML model training / selection, strategy hypothesis generation, signal
  construction, position state, entry/exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / tick / additional aggTrades /
  ETHUSDT acquisition; extra horizons; v003 creation;
- reading the v002 terminal raw/normalized window or sealed-test split;
  mutating the published normalized or feature `__v002` family;
- database creation / DuckDB / SQLite / Parquet compaction / storage migration;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status`
  from this memo alone;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a feature-only execution phase + bounded wrapper + offline tests (Phase
  4bn-R's recommendation — requires separate operator authorization);
- a feature-layer eligibility gate;
- a docs-only holdout-boundary memo (only if a future scope reads the v002
  terminal raw/normalized window or sealed-test dates);
- a source-policy documentation memo; a process-doc `D:` path-string update;
- label derivation + label gate; a chronological-split / holdout policy memo;
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

Phase 4bn-R is now **merge-complete on `main`** as of merge commit
`b7d13e4f3d079194983212df929f2a0b61a1f4cb` and the subsequent merge-closeout +
SHA-finalization commits. The normalized segment and any future feature output
remain **non-eligible** (`research_eligible: false`, `eligibility_gate_status:
"pending"`); no manifest eligibility transition occurred. The **conditional
next, NOT authorized** option is a separately-authorized **feature-only
execution phase** (a bounded new wrapper over the Phase 4bn-O pre-v002
normalized segment honouring the memo §11–§18 and the Phase 4bn-L budget),
followed only later — and only if separately authorized — by a bounded
feature-layer eligibility gate. It is **not** authorized by this merge.

### Selected feature manifest/versioning convention (preserved)

- **Shape:** a phase-scoped **feature segment manifest**, tied to the existing
  v002 feature family but clearly marked as a pre-v002 backward segment /
  extension; a backward segment of the v002 envelope, **not** a new monotonic
  version, **not** a write into the published `__v002` feature family, **not**
  v003. Keeps the published feature `__v002` family immutable; reads no v002
  terminal normalized dates; touches no sealed-test dates.
- **Manifest filename:**
  `microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>.json`
  (+ canonical two-space `.sha256` sidecar
  `…_pre_v002_segment_<feature-phase-id>.json.sha256`).
- **Inner identity fields:** `dataset_family =
  "microstructure_features_aggtrades_v001"`, `dataset_version = "v002"`,
  `version = "v002"`, `feature_schema_version = "v001"`, `segment_label =
  "pre_v002_segment"`, `data_family = "aggTrades"`, `symbol = "BTCUSDT"`,
  `market = "usdm_futures"`, `dataset_category = "features"`.
- **Both, sequenced:** mandatory segment manifest at execution + optional
  deferred by-reference full-envelope feature reference/assembly manifest.

### Selected non-eligible-source precondition (preserved)

- Replace the existing Stage-3 research-eligible successor-state precondition
  with a non-eligible-source precondition.
- Source admissibility predecessor = the **Phase 4bn-P normalized-layer gate
  report** (PASS verdict
  `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`;
  path
  `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json`),
  not a Stage-3 successor-state.
- Source normalized segment = the **Phase 4bn-O normalized segment manifest**
  (SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`;
  sidecar SHA256
  `5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`; path
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`),
  not the published `__v002` normalized manifest.
- Source normalized segment must remain non-eligible (`research_eligible:
  false`, `eligibility_gate_status: "pending"`).
- No `research_eligible: true` and no Stage-3 successor-state is required or
  created for this pre-v002 expansion path.
- Generated feature outputs must remain non-eligible/pending
  (`research_eligible: false`, `eligibility_gate_status: "pending"`,
  `no_successor_authorization: true`); the Phase 4aw
  `flip_research_eligible(...)` invariant must never be invoked.
- Generated features cannot be used for labels / ML / diagnostics / strategy /
  research / split policy until later separately authorized gates/policies;
  governance labels mark labels / ml / strategy / backtest / acquisition
  forbidden or unauthorized.

### Selected future feature output directory convention (preserved)

`data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`,
each with a paired canonical two-space `.sha256` sidecar. A version-suffixed
segment directory distinct from the published `__v002/` feature directory; not
the generic `microstructure_features_aggtrades_v001/` directory; not a new
`__vNNN`; not v003; satisfies the existing `data/microstructure/features/` path
discipline.

### Selected full-envelope feature reference convention (preserved)

- Full 12-month feature envelope 2024-03-01 .. 2025-02-28 identified **by
  reference**, never by rewriting existing v002 feature artefacts.
- Segment manifest carries `full_intended_envelope_start = "2024-03-01"`,
  `full_intended_envelope_end = "2025-02-28"`, an `existing_v002_feature_reference`
  block (published `__v002` feature manifest path
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`,
  `window_start = "2024-12-01"`, `window_end = "2025-02-28"`, `read = false`,
  `mutated = false`), an `existing_v002_terminal_window` block (`read = false`,
  `normalized_dates_read = false`), and an `existing_v002_sealed_test_split`
  block (`touched = false`).
- Optional deferred companion
  `microstructure_features_aggtrades_v001__v002_full_envelope_reference_<phase-id>.json`
  — a thin, non-eligible, by-reference index naming exactly the pre-v002 feature
  segment manifest (path + SHA256) and the published `__v002` feature manifest
  (path + SHA256, read-only); must not read/recompute the v002 terminal feature
  family, must not read v002 terminal normalized dates, must not mutate
  `microstructure_features_aggtrades_v001__v002.json`, must not create v003, must
  not flip eligibility. Phase 4bn-R does not create or require it; it only
  defines its shape.
- Answer to "segment manifest only / separate reference manifest / both /
  neither": **both, sequenced** — segment manifest mandatory at execution;
  full-envelope feature reference manifest defined-but-deferred optional
  companion.

### Future feature manifest required fields (preserved)

Identity (`dataset_family = "microstructure_features_aggtrades_v001"`,
`dataset_version = "v002"`, `version = "v002"`, `feature_schema_version =
"v001"`, `segment_label = "pre_v002_segment"`, `data_family = "aggTrades"`,
`symbol = "BTCUSDT"`, `market = "usdm_futures"`, `dataset_category =
"features"`); segment/phase (`phase_id`, `source_phase_boundary`,
`created_at_unix_ms`, `created_at_utc`, `code_commit_sha`, `base_commit_sha`,
`feature_config_hash`); feature schema (`feature_column_count = 62`,
`lineage_column_count = 17`, `feature_quality_column_count = 45`,
`feature_column_names` in canonical `FEATURE_SCHEMA_V002` order,
`lineage_column_names`, `computed_feature_column_names`, `feature_dtypes`,
`feature_family_id = "microstructure_features_aggtrades_v001"`,
`feature_schema_hash` if supported else `feature_config_hash`); kernel policy
(`leakage_policy = "causal_only_no_future_lookahead"`,
`cross_day_lookback_policy = "causal_cross_day_lookback"`,
`cross_day_tail_buffer_ms = 60000`, `feature_windows_ms` /
`feature_window_labels` 1s/5s/15s/60s, `window_boundary_policy`,
`invalid_window_policy`, `same_timestamp_tie_rule`, `timestamp_policy`,
`forbidden_substring_detector_tokens`); window/inventory (`date_start =
"2024-03-01"`, `date_end = "2024-11-30"`, `date_count = 275`, `date_list`,
`expected_file_count = 275`, `produced_file_count`, `total_row_count` /
`actual_feature_row_count`, `total_footprint_bytes`, `per_file_inventory` /
`per_day_outputs` with per-date feature parquet path, parquet SHA256, parquet
size bytes, row count, sidecar path, sidecar SHA256, paired source normalized
per-day parquet SHA256); non-eligible-source lineage (`source_dataset_family =
"microstructure_normalized_aggtrades_v001"`, `source_dataset_version = "v002"`,
`source_normalized_segment_manifest_path` + SHA256,
`source_normalized_layer_gate_report_path` + SHA256,
`source_normalized_schema_version = "NORMALIZED_SCHEMA_V001"`,
`source_eligibility_posture = "non_eligible_gate_passed_pending"`, **no**
Stage-3 successor-state field); `existing_v002_feature_reference` block;
`full_intended_envelope_start = "2024-03-01"`, `full_intended_envelope_end =
"2025-02-28"`; posture (`research_eligible = false`, `eligibility_gate_status =
"pending"`, governance labels marking labels/ml/strategy/backtest/acquisition
forbidden or unauthorized, `no_successor_authorization = true`, 18-key boundary
confirmations all true including `no_future_lookahead` and
`phase_4aw_flip_research_eligible_invariant_preserved`, 8-flag non-authorization
set all false including `successor_authorization_after`); boundary witnesses
(`v002_terminal_window_mode = "by_reference"`, `existing_v002_terminal_window`
read=false / normalized_dates_read=false, `sealed_test_split_touched = false`,
`test_holdout_touched = false`, `test_rows_loaded = 0`); partitioning
(`<SYMBOL>/<YYYY>/<MM>/`), primary key (`symbol, utc_date, agg_trade_id,
row_index`), storage Parquet zstd, sidecar policy canonical two-space `.sha256`,
`invalid_windows`; Phase 4bn-L budget witnesses (feature footprint,
temporary-workspace footprint, runtime, `D:` free space, cap thresholds
honoured).

### Future feature manifest forbidden fields (preserved)

No label outputs / horizons; no barrier / target / MFE / MAE / R-multiple
fields; no `label_*` / `target_*` fields; no future returns / forward-looking
values / `future_*` fields; no model outputs / predictions / scores / `model_*`
/ `score_*` / `prediction_*` fields; no signal / entry / exit / `signal_*`
fields; no PnL / equity / profit / loss / position / backtest fields; no
strategy / alpha / edge fields; no diagnostic scores / statistics /
research-quality metrics; no field asserting/implying `research_eligible: true`;
no `eligibility_gate_status` other than `"pending"`; no
`chronological_split_policy` value; no `diagnostics_authorized: true`; no
`ml_authorized: true`; no research-ready / admissible-for-ML /
approved-for-backtest claim; no Stage-3 research-eligible successor-state
reference presented as a required precondition for this segment; no v003 /
mark-price / funding / open-interest / order-book / spot / cross-venue / tick /
ETHUSDT fields; no extra-horizon field.

### Future feature execution implications (preserved)

A future separately authorized feature-only execution phase must: build a
bounded new wrapper reusing the locked feature primitives unchanged
(`features_schema_v002`, `features_compute_v002`, `features_io_v002`,
`features_manifest_v002`, `features_schema`); add the pre-v002 normalized
segment source contract and the selected non-eligible-source precondition;
hard-reject any date `>= 2024-12-01` and any date outside 2024-03-01 ..
2024-11-30; implement the selected segment naming; enforce the Phase 4bn-L
preflight/budget caps; read only the approved 275 normalized segment dates
verified by SHA256 against the Phase 4bn-O segment manifest and Phase 4bn-P gate
evidence; never open the published `__v002` normalized family; never read v002
terminal normalized dates; never read sealed-test dates; write only feature
Parquet + canonical sidecars under the selected segment directory plus one
non-eligible feature segment manifest + sidecar under
`data/microstructure/manifests/`; refuse overwrite; atomic write-then-rename;
preserve the locked 62-column `FEATURE_SCHEMA_V002`, the forbidden-substring
column guard, the strictly-causal kernel, the backward-only 60 s cross-day tail,
and first-segment-day `rolling_missing_window_flag` behaviour; leave the
published feature `__v002` directory and manifest byte-for-byte unchanged;
honour the Phase 4bn-L budget (feature layer 50 GiB warn / 100 GiB hard
footprint, 4 h warn / 8 h hard runtime; temporary workspace 50 GiB / 100 GiB;
total derived-stack 250 GiB warn / 300 GiB hard; `D:` free ≥ 500 GiB before,
fail closed below 350 GiB during) and stop before writing on any breach; leave
all outputs non-eligible; commit no data artefact; create no labels / targets /
future returns / ML outputs / diagnostics / research outputs / database / v003 /
compacted Parquet; carry its own offline test module; preserve the Phase 4aw
`flip_research_eligible(...)` always-raises invariant.

### Future feature-layer gate implications (preserved)

A future separately authorized feature-layer eligibility gate should validate:
the feature segment manifest exists and parses; the required-field contract
passes; forbidden fields are absent; every per-date feature parquet exists with
a canonical sidecar; recomputed SHA256s match the segment manifest; recomputed
aggregates match (date count 275, total feature rows, per-date row counts,
contiguous in-segment dates, segment footprint); schema is exactly the locked
62-column `FEATURE_SCHEMA_V002` (17 lineage + 45 feature/quality);
forbidden-substring column guard passes; leakage / cross-day policies match;
predecessor integrity (Phase 4bn-O normalized segment manifest SHA256
`0e96ae37…d9fa`; Phase 4bn-P gate report SHA256 `3452fd9d…f134` and PASS
verdict); per-day source normalized parquet SHA256s consistent; published
`__v002` feature family not mutated; v002 terminal normalized window not read;
sealed-test split not read; `research_eligible` remains false;
`eligibility_gate_status` remains pending. A passing feature-layer gate must not
flip eligibility and must not authorize labels, ML, diagnostics, strategy, or
any successor.

### Sealed-test / v002 terminal boundary (preserved)

The new pre-v002 feature segment covers 2024-03-01 .. 2024-11-30 and contains no
sealed-test dates and no v002 terminal-window dates. The feature kernel is
strictly causal; cross-day lookback is limited to a 60 s backward tail.
Computing 2024-11-30 requires no forward read into 2024-12-01; computing
2024-03-01 requires no pre-segment read (early rows use
`rolling_missing_window_flag`). The existing v002 terminal normalized window is
by reference only; the published feature `__v002` family is by reference only
and immutable. The sealed v002 test split 2025-02-14 .. 2025-02-28 remains
untouched (`sealed_test_split_touched = false`, `test_holdout_touched = false`,
`test_rows_loaded = 0`). A holdout-boundary memo is **not required** for the
conservative pre-v002-only feature scope; it is required only if a future
feature phase proposes to read the v002 terminal normalized window or
sealed-test dates.

### Explicit confirmations

- Phase 4bn-R is merge-complete on `main` after this merge.
- Project completion of this phase requires the SHA-finalization commit
  (`docs(phase-4bn-r): finalize merge closeout shas`) per the repository's
  merge-closeout convention.
- Feature-only execution / any successor is **NOT authorized**.
- `research_eligible` remains `false`; `eligibility_gate_status` remains
  `pending`; no manifest eligibility transition occurred.
- v003 remains forbidden; existing published feature `__v002` manifests/
  directories remain immutable; the v002 terminal normalized window remains
  by-reference only; the sealed-test split remains untouched.
- No local data was read, created, or committed; the pre-existing gitignored
  Phase 4bn-O / 4bn-P artefacts remain local and uncommitted.
- No acquisition was run, no endpoints were called, no archives were downloaded,
  no HEAD preflight was run, no raw gate was rerun, no normalization was rerun,
  no normalized-layer gate was rerun, no feature derivation was run, no feature
  gate was run, no local raw zip contents were inspected, no local normalized
  Parquet files were read, no local feature files were read, no local manifest
  or gate report was read, no v002 terminal window was read, no test holdout was
  touched, no labels were derived, no ML was trained, no model scoring was
  performed, no predictions were generated, no diagnostics were run, no
  backtests were run, no strategy/signal/PnL work was performed, no storage
  migration occurred, no database was created, no Parquet was compacted, no v003
  dataset was created, no manifest eligibility transition occurred, no
  `data/research` artefacts were created or committed, no `data/microstructure`
  artefacts were created or committed, and no paper/shadow/live/exchange-write/
  credentials/MCP/Graphify work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
