# Phase 4bn-N — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-N — Normalization Manifest / Versioning Memo.
- **Type:** docs-only / normalization-manifest / dataset-versioning /
  boundary-contract phase. **Risk tier: Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-N normalization manifest/versioning
  memo, its closeout, and the narrow `current-project-state.md` update onto
  `main` so the resolved manifest/versioning convention for a future pre-v002
  normalized BTCUSDT Binance USDⓈ-M futures aggTrades segment becomes project
  state. The phase resolves the manifest/versioning ambiguity that Phase
  4bn-M deferred; it authorizes nothing executable and no successor; it
  records a convention and a decision and remains paused.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-n/normalization-manifest-versioning-memo`.

## 2. SHAs

- **`main` SHA before merge:** `6d41c2e069ce688fa08b36473fe4449e008bdb18`
  (`docs(phase-4bn-m): finalize merge closeout shas`).
- **Branch commit SHA (memo + closeout + state update):**
  `0ba6ef0a13b3a65a084c115f9fa23de880f43866`
  (`docs(phase-4bn-n): settle normalization manifest versioning`).
- **Merge commit SHA:** `9ee0c4becf652302c8f3607b2c2b202e9c45ba36`
  (`docs(phase-4bn-n): merge normalization manifest versioning`).
- **Merge-closeout commit SHA:**
  `7417a25acf3aa278a6ac2c17f31ebcd00db46328`
  (`docs(phase-4bn-n): add merge closeout` — the commit that adds this file).
- **SHA-finalization commit:** `docs(phase-4bn-n): finalize merge closeout
  shas` — the published `main` tip after push; its exact 40-char SHA is
  recorded in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization
  commit above; exact 40-char SHA recorded in the final operator report
  after push (`main == origin/main` at that SHA).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message:
  `docs(phase-4bn-n): merge normalization manifest versioning`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- **Push status:** pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing, after the SHA-finalization commit
  `docs(phase-4bn-n): finalize merge closeout shas`.

## 4. Files brought forward by the merge

- **Docs (3 files):**
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-n_normalization-manifest-versioning-memo.md`
    (added; the 21-section manifest/versioning memo).
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-n_closeout.md`
    (added; the branch closeout).
  - `docs/00-meta/current-project-state.md` (modified; new Phase 4bn-N prose
    paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-M
    paragraphs and blocks preserved as labelled historical context; 172
    insertions, 0 deletions).
- **Source:** none.
- **Tests:** none.
- **Scripts:** none.
- **Config / `.gitignore` / `pyproject.toml` / `README.md` / MCP:** none.
- **No `data/microstructure/` file was modified.** No prior governance memo
  was modified beyond the narrow `current-project-state.md` paragraph + block
  addition. No prior source / test / script was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 172 ++++++
 .../2026-06-04_phase-4bn-n_closeout.md             | 184 ++++++
 ...4bn-n_normalization-manifest-versioning-memo.md | 679 +++++++++++++++++++++
 3 files changed, 1035 insertions(+)
```

The diff matches the expected change set from the authorization prompt
exactly: add the memo, add the closeout, modify `current-project-state.md`.
No deletions; no other files touched.

## 6. Verdict

**MEMO RECORDED —
`RECORD_NORMALIZATION_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`.**
Phase 4bn-N resolved, from committed docs and committed tooling only, the
manifest/versioning ambiguity Phase 4bn-M deferred: it selected a
**phase-scoped normalized segment manifest** (mirroring the merged raw-layer
segment precedent) tied to the existing terminal normalized `__v002` family
and clearly marked as a **pre-v002 backward segment / extension** — **not** a
write into the published `__v002`, **not** a new `__vNNN`, **not** v003 — with
a version-suffixed segment directory, predecessor linkage by SHA to the Phase
4bn-J-R2 raw segment manifest and Phase 4bn-K raw gate report, and the full
12-month normalized envelope represented **by reference**. It ran no
normalization, created no normalized artefacts, created or mutated no
manifest, read no local data, and created no local data. The decision is
`RECOMMEND_AUTHORIZE_NORMALIZATION_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
With this merge, **Phase 4bn-N is merge-complete on `main`.** All current
manifests remain non-eligible (`research_eligible: false`,
`eligibility_gate_status: "pending"`); no manifest eligibility transition
occurred. **Recommended state: remain paused.**

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-N produced no local artefact under `data/microstructure/`
or `data/research/`. It read no local data and created no local data. The
only untracked working-tree entry is the known scheduler transient
`.claude/scheduled_tasks.lock` (not committed).

## 8. Validation results

Docs-only Tier 1 phase with no code/test/script/config surface; the relevant
validation surface is git status, diff review, `git diff --check`, gitignore
confirmation, and SHA checks.

- `git diff --check` → clean (no whitespace errors).
- `git diff --name-status main..phase-4bn-n/normalization-manifest-versioning-memo`
  (pre-merge) →
  `M docs/00-meta/current-project-state.md`,
  `A docs/00-meta/implementation-reports/2026-06-04_phase-4bn-n_closeout.md`,
  `A docs/00-meta/implementation-reports/2026-06-04_phase-4bn-n_normalization-manifest-versioning-memo.md`.
- `git diff --stat` (merge) → `3 files changed, 1035 insertions(+)`.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`; no
  `data/microstructure/` or `data/research/` artefact staged or committed.
- **ruff / mypy / pytest:** not required and not run — Phase 4bn-N creates no
  code/test/script/config surface (no source change to lint or type-check, no
  test to run). **No repo-standard markdown validator exists** (no
  `.markdownlint*`, `.mdlrc`, or markdownlint / mdformat / remark dependency),
  so none was run.

## 9. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bn-N did not open,
hash, read, or mutate any raw manifest, raw zip, normalized parquet, feature
parquet, label parquet, gate report, successor-state JSON, or sidecar under
`data/microstructure/`, and created nothing under `data/research/`. SHA256
digests cited in the memo (Phase 4bn-J-R2 raw segment manifest
`1659e6da…3a3d1`, Phase 4bn-K raw gate report `051bed7b…20f9c24`, raw
acquisition log `0266210f…88bcf93`) were quoted from committed Markdown
evidence, not by reading the local gitignored files.

## 10. Manifest state preservation (if applicable)

No manifest was read or mutated by this phase. State carried forward
unchanged for all microstructure manifests in the project:

- `research_eligible` — **false** (unchanged; no transition).
- `eligibility_gate_status` — **"pending"** (unchanged; no transition).
- `chronological_split_policy` — **"not_yet_defined"** for the label manifest
  (unchanged; no transition).
- Governance labels — **unchanged**.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant **preserved (never invoked).**

## 11. Boundary confirmations

- no source code modified;
- no test modified;
- no script modified;
- no `.gitignore`, `pyproject.toml`, or `README.md` modified;
- no MCP file modified;
- no manifest created or mutated;
- no sidecar created or mutated;
- no gate report created or mutated;
- no successor-state artefact created or mutated;
- no `data/microstructure/` write or commit;
- no `data/research/` write or commit;
- no `research_eligible` flipped on any manifest;
- no `eligibility_gate_status` transitioned on any manifest;
- no `chronological_split_policy` changed;
- no `diagnostics_authorized` / `ml_authorized` transition;
- no normalization run; no normalized artefact generated; no normalizer
  rerun;
- no raw eligibility gate rerun; no derived/feature/label gate rerun;
- no feature / label kernel run;
- no ML model trained; no model scoring; no predictions;
- no diagnostics run;
- no strategy created; no signal computed; no PnL; no backtest run;
- no data acquired; no public / Binance / `data.binance.vision` endpoint
  called; no archive or CHECKSUM downloaded; no HEAD preflight; no WebSocket
  / user stream opened;
- no local raw zip contents inspected; no v002 terminal raw window read; no
  sealed test split read / counted / sampled / hashed / inspected;
- no storage migration; no DuckDB / SQLite / `.duckdb` / `.sqlite` / database
  created; no Parquet compaction; no v003 created;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment;
- no successor authorized.

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

**All preserved verbatim.**

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bn-J-R1 raw-only cap amendment (10 GiB warning / 25 GiB hard)
- Phase 4bn-L derived-stack storage budget

**All prior phase results preserved verbatim.**

## 14. No-rescue constraints

The Phase 4bn-N merge does not, and cannot, be construed as authorising:

- normalization execution, normalized-artefact generation, a bounded
  normalization runner, or manifest creation/mutation;
- feature derivation, label derivation, or any research-matrix construction;
- ML model training, model selection, model scoring, predictions, feature
  ranking / selection / pruning / engineering, hyperparameter tuning,
  threshold tuning, or calibration fitting;
- strategy hypothesis generation, signal construction, position state, entry
  / exit rules, PnL simulation, or backtest design / execution;
- raw acquisition; public / Binance / `data.binance.vision` endpoint calls;
  archive or CHECKSUM downloads; HEAD preflight; WebSocket / user stream;
- reading the v002 terminal raw window or touching the sealed test split for
  any ML / diagnostics / statistics / strategy / research use;
- storage migration; DuckDB / SQLite / database creation; Parquet compaction;
  v003 dataset creation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / tick / ETHUSDT /
  extra-horizon / additional aggTrades acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- paper / shadow / live-readiness / deployment / exchange-write / production
  keys / authenticated APIs / private endpoints / credentials / MCP /
  Graphify / `.mcp.json`;
- Phase 4 canonical or Phase 5 authorisation;
- transitioning any manifest's `research_eligible` or
  `eligibility_gate_status` from this memo alone;
- authorizing the recommended normalization-only execution phase — it is
  recommended only, **subject to separate operator authorization.**

## 15. Successor authorization

**None.**

Candidate successors that are **NOT** authorized by this merge:

- normalization-only execution phase (the Phase 4bn-N recommendation — a
  bounded new runner over the pre-v002 segment; recommended only, not
  authorized);
- docs-only holdout-boundary memo (only relevant if a future phase reads the
  v002 terminal raw window; **not required** for the conservative
  pre-v002-only scope);
- source-policy documentation memo;
- process-doc `D:` path-string update (Phase 4bm-D-P1 lightweight-workspace
  standard still carries old `C:` example paths);
- optional full-envelope reference / assembly manifest creation;
- normalized-layer eligibility gate; feature derivation + feature gate;
  label derivation + label gate; chronological-split / holdout policy memo;
- ML implementation; strategy implementation; backtest implementation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / ETHUSDT
  data acquisition;
- paper / shadow; live-readiness; deployment; exchange-write; production
  keys; authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials;
- Phase 5; Phase 4 canonical.

## 16. Recommended state

**Remain paused.**

**Conditional next, NOT authorized:** a normalization-only execution phase is
the cleanest non-paused option. With the manifest/versioning convention now
settled, it would build a bounded new runner over the pre-v002 raw segment
(2024-03-01 .. 2024-11-30), reusing the locked normalization primitives
unchanged and adding the segment-date guard, the §10/§14 segment naming, and
the Phase 4bn-L preflight/budget caps; it would write only normalized
aggTrades parquet + canonical sidecars under the segment directory plus the
pre-v002 normalized segment manifest + sidecar, leave the published `__v002`
family and the sealed test split untouched, and keep all outputs non-eligible.
It is **not** authorized by this merge.

---

### Selected manifest/versioning convention carried onto `main`

- **Representation:** a **phase-scoped normalized segment manifest** mirroring
  the merged raw-layer segment precedent — tied to the existing v002
  normalized family, clearly marked as a **pre-v002 backward segment /
  extension**; **not** a predecessor-linked write into `__v002`; **not** a new
  `__vNNN`; **not** v003; does **not** mutate the published normalized `__v002`
  family; does **not** read the v002 terminal raw window; does **not** touch
  sealed-test dates.
- **Future segment manifest filename (under
  `data/microstructure/manifests/`):**
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_<normalization-phase-id>.json`,
  with a paired canonical two-space `.sha256` sidecar.
- **Inner identity fields:** `dataset_family =
  "microstructure_normalized_aggtrades_v001"`; `dataset_version = "v002"`;
  `version = "v002"`; `schema_version = "v001"`;
  `segment_label = "pre_v002_segment"`; `data_family = "aggTrades"`;
  `symbol_list = ["BTCUSDT"]`; `market = "usdm_futures"`;
  `dataset_category = "normalized"`.

### Selected output directory convention carried onto `main`

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_<normalization-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet
```

each with a paired canonical two-space `.sha256` sidecar. It is a
version-suffixed segment directory **distinct from** the published `__v002/`
directory; **not** the generic `microstructure_normalized_aggtrades_v001/`
directory; **not** a new `__vNNN` directory; satisfies the existing normalized
root path discipline under `data/microstructure/normalized/`.

### Selected full-envelope reference convention carried onto `main`

- The eventual 12-month normalized envelope **2024-03-01 .. 2025-02-28** is
  represented **by reference, never by rewriting existing v002 artefacts**.
- The future pre-v002 normalized **segment manifest** itself carries
  `full_intended_envelope_start = "2024-03-01"`,
  `full_intended_envelope_end = "2025-02-28"`, an
  `existing_v002_normalized_reference` block (published `__v002` manifest path
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`,
  window 2024-12-01 .. 2025-02-28, `read: false`, `mutated: false`), an
  `existing_v002_terminal_window` block, and an `existing_v002_sealed_test_split`
  block.
- A separate, **optional, deferred** full-envelope reference / assembly
  manifest
  `microstructure_normalized_aggtrades_v001__v002_full_envelope_reference_<phase-id>.json`
  may later be written **only if** a single 12-month handle is needed
  downstream — a thin, non-eligible, by-reference index naming exactly two
  halves (the pre-v002 normalized segment manifest path + SHA256; the
  published `__v002` manifest path + SHA256, read-only). It must not re-read
  or re-normalize the v002 terminal raw window, must not mutate `__v002.json`,
  must not create v003, and must not flip eligibility. **Phase 4bn-N neither
  creates nor requires it.**
- Answer to "segment manifest only / separate reference manifest / both /
  neither": **both, sequenced** — segment manifest mandatory at execution;
  full-envelope reference manifest defined-but-deferred optional companion.

### Predecessor linkage carried onto `main`

- **Input raw segment manifest:**
  `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`,
  SHA256 `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`.
- **Input raw gate report:** SHA256
  `051bed7b3a146278e389bd8e265243d30fd541b5f36061d0573f3522920f9c24`.
- **Raw acquisition log:** SHA256
  `0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`.
- **Existing normalized `__v002` family — by reference only:**
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`;
  window 2024-12-01 .. 2025-02-28; `read: false`; `mutated: false`.

### Future manifest required fields carried onto `main`

`dataset_family = "microstructure_normalized_aggtrades_v001"`;
`dataset_version = "v002"`; `version = "v002"`; `schema_version = "v001"`;
`segment_label = "pre_v002_segment"`; `data_family = "aggTrades"`;
`symbol_list = ["BTCUSDT"]`; `market = "usdm_futures"`;
`dataset_category = "normalized"`; `phase` / `phase_id`;
`source_phase_boundary`; `created_at_unix_ms`; `created_at_utc`;
`code_commit_sha`; `base_commit_sha`; `capture_config_hash`;
`date_start = "2024-03-01"`; `date_end = "2024-11-30"`; `date_count`;
`date_list`; `expected_file_count`; `produced_file_count`;
`total_event_count` / `total_row_count`; `per_file_inventory`; total
normalized footprint in bytes; `source_dataset_family =
"microstructure_raw_aggtrades_v001"`; `source_dataset_version = "v002"`; input
raw segment manifest path + SHA256; input raw gate report path / report_id +
SHA256; raw acquisition log path + SHA256; `existing_v002_normalized_reference`;
`full_intended_envelope_start = "2024-03-01"`;
`full_intended_envelope_end = "2025-02-28"`; `research_eligible = false`;
`eligibility_gate_status = "pending"`;
`governance_labels.feature_computation = "forbidden"`;
`governance_labels.strategy_use = "forbidden"`;
`no_successor_authorization = true`;
`v002_terminal_window_mode = "by_reference"`; `existing_v002_terminal_window`
(read/overwritten/redownloaded/re_normalized all false);
`sealed_test_split_touched = false`; `existing_v002_sealed_test_split`
(touched false); `test_holdout_touched = false`; `test_rows_loaded = 0`;
partitioning rule; primary key; storage format; sidecar policy;
`invalid_windows`; Phase 4bn-L budget witnesses.

### Future manifest forbidden fields carried onto `main`

No model outputs / predictions / scores / `model_*`; no label outputs / label
horizons / barrier / target / MFE / MAE / R-multiple / `label_*` / `target_*`;
no future returns / forward-looking values / `future_*`; no signal / entry /
exit / `signal_*`; no PnL / equity / profit / loss / position / backtest; no
strategy / alpha / edge; no diagnostic scores / statistics / research-quality
metrics; no field asserting or implying `research_eligible: true`,
`eligibility_gate_status` other than `"pending"`, any
`chronological_split_policy` value, `diagnostics_authorized: true`, or
`ml_authorized: true`; no research-ready / admissible-for-ML /
approved-for-backtest claim; no v003 / mark-price / funding / open-interest /
order-book / spot / cross-venue / tick / ETHUSDT field.

### Future normalization execution implications carried onto `main`

A future normalization-only execution phase (separately authorized) must
build a bounded new runner reusing the locked primitives unchanged; add the
pre-v002 segment manifest as input source; hard-reject any date `>= 2024-12-01`
and any date outside 2024-03-01 .. 2024-11-30; enforce Phase 4bn-L preflight/
budget caps; implement the selected segment naming; read only approved
pre-v002 raw inputs verified by SHA256 against the Phase 4bn-J-R2 segment
manifest, relying on the Phase 4bn-K gate report as predecessor evidence;
never open the v002 terminal raw window; never read sealed-test raw dates;
write only normalized aggTrades parquet + canonical sidecars under the segment
directory and only the segment manifest + sidecar under
`data/microstructure/manifests`; refuse overwrite; atomic write-then-rename;
preserve the locked 19-column `NORMALIZED_SCHEMA_V001` and the
forbidden-substring column guard; leave the published `__v002` directory and
`microstructure_normalized_aggtrades_v001__v002.json` manifest byte-for-byte
unchanged; honour the Phase 4bn-L budget (normalized 100 GiB warn / 150 GiB
hard, 4 h / 8 h; temporary workspace 50 GiB / 100 GiB; total derived-stack
250 GiB warn / 300 GiB hard; `D:` free ≥ 500 GiB before, fail closed below
350 GiB during) and stop before writing on any breach; leave all outputs
non-eligible; commit no data artefact; create no database, no v003, no
compacted Parquet, no features, no labels, no research outputs; carry its own
offline test module; preserve the Phase 4aw `flip_research_eligible(...)`
always-raises invariant.

### Future normalized-layer gate implications carried onto `main`

A future separately-authorized normalized-layer eligibility gate is required
after normalization execution. It must validate the segment manifest
required-field contract; verify forbidden fields are absent; validate per-date
parquet + sidecar presence and SHA256s; recompute aggregates; validate
predecessor integrity (raw segment manifest + raw gate report SHA256s);
confirm the published `__v002` family was not mutated; confirm the v002
terminal raw window and sealed-test split were not read; confirm the schema is
exactly `NORMALIZED_SCHEMA_V001`; and confirm `research_eligible` remains
false and `eligibility_gate_status` remains pending. **A passing
normalized-layer gate must not flip eligibility and must not authorize
features, labels, ML, diagnostics, strategy, or any successor.**

### Sealed-test / v002 terminal boundary carried onto `main`

The new pre-v002 normalized segment covers 2024-03-01 .. 2024-11-30 and
contains no sealed-test dates and no v002 terminal-window dates. The existing
v002 terminal window 2024-12-01 .. 2025-02-28 is **by reference only** and is
not read, re-downloaded, overwritten, or re-normalized. The sealed v002 test
split 2025-02-14 .. 2025-02-28 remains **untouched**
(`sealed_test_split_touched: false`, `test_holdout_touched: false`,
`test_rows_loaded: 0`). A holdout-boundary memo is **not required** for the
conservative pre-v002-only normalization; it is required **only if** a future
phase proposes to read the v002 terminal raw window.

### Execution-review confirmation

During this merge review, **no acquisition was run, no endpoints were called,
no archives were downloaded, no HEAD preflight was run, no raw gate was run,
no normalization was run, no normalized artefact was generated, no manifest
was created or mutated, no raw zip contents were inspected, no local manifest
or gate report under `data/microstructure` was read, no v002 terminal window
was read, no test holdout was touched, no features were derived, no labels
were derived, no ML was trained, no model scoring was performed, no
predictions were generated, no diagnostics were run, no backtests were run,
no strategy / signal / PnL work was performed, no storage migration occurred,
no database was created, no Parquet was compacted, no v003 dataset was
created, no manifest eligibility transition occurred, no `data/research`
artefacts were created or committed, no `data/microstructure` artefacts were
created or committed, and no paper / shadow / live-readiness / deployment /
exchange-write / production-key / credentials / MCP / Graphify work was
authorized.**

### Lifecycle note

With this merge and merge-closeout, **Phase 4bn-N is merge-complete on
`main`** per `merge-closeout-standard.md` (Tier 1, full 16-section
structure). Per the project's current convention, project completion is
finalized by a separate **SHA-finalization** commit
(`docs(phase-4bn-n): finalize merge closeout shas`) that records the
merge-closeout commit SHA and the final `main` / `origin/main` SHA, which are
not knowable before the merge-closeout commit exists.
