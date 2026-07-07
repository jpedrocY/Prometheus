# Phase 4bn-AF — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-AF — Code-Only ML Dataset Builder Skeleton.
- **Phase type:** code-only / synthetic-fixture-only / no-data-read / no-output /
  ML dataset builder skeleton / amended-contract encoding / offline tests.
- **Action:** merge into `main`.
- **Merge purpose:** bring the branch-complete Phase 4bn-AF work (three new source
  modules, one offline test module, the implementation report, the closeout, and
  the narrow additive `current-project-state.md` update) onto `main`.
- **Source branch:** `phase-4bn-af/code-only-ml-dataset-builder-skeleton`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (it converts the Phase
  4bn-AC source contract, the Phase 4bn-AD builder-readiness decision, and the
  Phase 4bn-AE amendment-001 pre-registration into executable pure-code
  invariants; an error could later permit data reads, forbidden columns, invalid
  split handling, leakage, improper evaluation interpretation, or accidental
  output creation — even though the phase reads no data and creates no output).
  The full 16-section merge-closeout structure is used.

---

## 2. SHAs

- **Pre-merge `main` / base SHA:** `3e0e26e00bad5bce4c239d9157349b4acd296702`
  (`docs(phase-4bn-ae): finalize merge closeout shas`).
- **Branch / code+docs commit SHA:** `77da4be7ad69098217785ad2b750e9dd22db2cfd`
  (`code(phase-4bn-af): add code-only ml dataset builder skeleton`).
- **Merge commit SHA:** `3ca22344315e58a08f666c3c4802b6a3f29ade3b`
  (`code(phase-4bn-af): merge code-only ml dataset builder skeleton`).
- **Merge-closeout commit SHA:** `e6151dd63e0a86fd43f718e89e047b36ae74c1af`
  (`docs(phase-4bn-af): add merge closeout`).
- **SHA-finalization commit SHA:** this update
  (`docs(phase-4bn-af): finalize merge closeout shas`) that fills the exact
  merge-closeout commit SHA above — its exact SHA equals the resulting `main` /
  `origin/main` tip, reproduced in the final operator report and `git log`.
- **Final `main` / `origin/main` SHA after push:** equal to the SHA-finalization
  commit SHA above; reproduced in the final operator report and `git log`.

---

## 3. Merge method

`git checkout main` → `git pull --ff-only origin main` (already up to date at
`3e0e26e`) → `git merge --no-ff
phase-4bn-af/code-only-ml-dataset-builder-skeleton -m "code(phase-4bn-af): merge
code-only ml dataset builder skeleton"`. Merge made by the `ort` strategy; no
conflicts. No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
force-push. Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
(push status recorded in the final operator report).

---

## 4. Files brought forward by the merge

**Source (3, added):**

- `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py`
  (pure constants + 5 frozen dataclasses).
- `src/prometheus/research/microstructure/pre_v002_ml_dataset_builder.py`
  (`PreV002MlDatasetError` + 12 pure validators/planners + 3 dataclasses).
- `src/prometheus/research/microstructure/pre_v002_ml_dataset_proof.py`
  (7 proof dataclasses + build/validate helpers).

**Tests (1, added):**

- `tests/research/microstructure/test_phase4bn_af_pre_v002_ml_dataset_builder_skeleton.py`
  (97 offline synthetic tests).

**Docs (3):**

- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-af_code-only-ml-dataset-builder-skeleton.md`
  (35 sections).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-af_closeout.md`.
- **Modified (additive only):** `docs/00-meta/current-project-state.md`
  (161 insertions, 0 deletions; new Phase 4bn-AF paragraph after the Phase
  4bn-AE paragraph + new `Current phase:` block ahead of the Phase 4bn-AE block;
  all prior content preserved verbatim).

**No existing source or test was modified.** No scripts, config, `.gitignore`,
`pyproject.toml`, README, MCP file, manifest, sidecar, gate report,
successor-state artefact, split file, research matrix, ML config, model output,
prediction output, or data file was added or modified. **No `data/microstructure/`
or `data/research/` file was modified.**

---

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 161 +++++
 .../2026-06-05_phase-4bn-af_closeout.md            | 147 ++++
 ...4bn-af_code-only-ml-dataset-builder-skeleton.md | 376 +++++++++++
 .../microstructure/pre_v002_ml_dataset_builder.py  | 631 +++++++++++++++++
 .../microstructure/pre_v002_ml_dataset_contract.py | 492 ++++++++++++++
 .../microstructure/pre_v002_ml_dataset_proof.py    | 316 +++++++++
 ...e4bn_af_pre_v002_ml_dataset_builder_skeleton.py | 745 +++++++++++++++++++++
 7 files changed, 2868 insertions(+)
```

2868 insertions, 0 deletions. The diff matches the expected change set from the
merge prompt exactly (add 3 source modules, add 1 test module, add memo, add
closeout, modify `current-project-state.md`).

---

## 6. Result / verdict

**CODE-ONLY SKELETON IMPLEMENTED — SYNTHETIC TESTS PASS — MERGE COMPLETE.** Phase
4bn-AF implemented a **code-only** ML dataset builder skeleton for the pre-v002
path using synthetic in-memory fixtures and offline tests only. It encodes the
Phase 4bn-AC source contract, the Phase 4bn-AD no-data-I/O readiness controls, and
the Phase 4bn-AE amendment-001 evaluation obligations as pure, tested, fail-closed
invariants. It read no local data, created no local data, wrote no Parquet,
mutated no manifest, produced no `data/research` / `data/microstructure` artefact,
created no future output namespace, and called no endpoint. It is not a
data-reading builder, not an ML dataset, not a research matrix, not a trainer, not
diagnostics, and not strategy / PnL / backtesting. With this merge, Phase 4bn-AF
is **merge-complete on `main`**.

- **Result state:**
  `CODE_ONLY_ML_DATASET_BUILDER_SKELETON_IMPLEMENTED__SYNTHETIC_TESTS_PASS__NO_DATA_READ__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_AUTHORIZATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the project convention, project completion also requires the SHA-finalization
commit (`docs(phase-4bn-af): finalize merge closeout shas`) that fills the exact
post-merge SHAs in §2; that commit is recorded below and in the final operator
report.

---

## 7. Local gitignored outputs (if any)

**None.** This phase created no `data/microstructure/` or `data/research/` output
and read none. `git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. The sole untracked entry
is the expected transient `.claude/scheduled_tasks.lock` (not committed). The
future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` was **not**
created (proven by test).

---

## 8. Validation results

- `ruff check` (3 modules + test) → **All checks passed**.
- `pytest …test_phase4bn_af…` → **97 passed**.
- `mypy` (3 new modules) → **0 direct errors in the new modules**; 29 pre-existing
  unrelated errors surface transitively from committed sibling modules
  (`features_compute.py`, `features_compute_v002.py`,
  `multiday_feature_gate_checks.py`) — the identical set reproduced by
  `mypy pre_v002_split_policy.py` on a committed module, as documented by the
  Phase 4bn-AA closeout. The new modules introduced none.
- `git diff --check` → clean (pre- and post-merge).
- `git diff --stat` (merge, `3e0e26e..HEAD`) → 7 files, 2868 insertions, 0
  deletions.
- `git diff --numstat -- docs/00-meta/current-project-state.md` → `161 0`
  (additive only).
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` (post-merge) → only `?? .claude/scheduled_tasks.lock`.
- No acquisition / raw / normalization / feature / label / gate / ML /
  diagnostics / backtest / strategy script was run; no endpoint called; no
  archive downloaded; no HEAD preflight; no local data read or created.
- Git emitted the standard LF→CRLF advisory for the new files at branch commit
  time (`.gitattributes` / `core.autocrlf`, Windows convention); cosmetic;
  committed blobs are correct.

---

## 9. Upstream immutability evidence (if applicable)

**n/a — phase accessed no local artefact.** Phase 4bn-AF reads and mutates no
manifest, sidecar, gate report, successor-state, or published dataset. The
published `__v002` families and the local gated pre-v002 normalized (4bn-O) /
feature (4bn-S) / label (4bn-W) segments and their gate reports (4bn-P / 4bn-T /
4bn-X) remain byte-for-byte immutable and unread. The new modules import only
stdlib, the inert schema-constant modules, and the inert Phase 4bn-AA split-policy
artefact — never `manifest.py`, `ml_baseline_dataset_v002.py`, or any data reader.

---

## 10. Manifest state preservation (if applicable)

No manifest in scope was created, read, or mutated. Byte-identically before and
after this phase, at every pre-v002 layer (normalized `0e96ae37…`, feature
`4881eb87…`, label `69746c88…`):

- `research_eligible` — **false** (not flipped).
- `eligibility_gate_status` — **pending** (not transitioned).
- `chronological_split_policy` — **not set / not transitioned** in any manifest.
- `diagnostics_authorized` / `ml_authorized` — **false** (not transitioned).
- `no_successor_authorization` — **true** (preserved).

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant preserved (never invoked; the new modules import no manifest reader).

---

## 11. Boundary confirmations

- No local data read; no local data created.
- Three source modules + one test module added; no existing source / test /
  script / config / `.gitignore` / `pyproject.toml` / README / MCP file modified.
- No split file, research matrix, ML dataset, ML config, manifest, gate report,
  sidecar, successor-state artefact, model, score, or prediction created.
- No real proof sidecar produced (only an inert in-memory proof dataclass).
- No file under `data/microstructure/` or `data/research/` read or inspected
  (raw zip / normalized / feature / label Parquet / manifest / gate report /
  sidecar / v002-terminal / sealed-test).
- No v002 terminal window read; no sealed test touched (`test_rows_loaded = 0`).
- No ML trained / scored / predicted; no diagnostics; no strategy / signals /
  PnL / backtests.
- No acquisition, endpoint call, archive download, or HEAD preflight; no
  layer-gate re-run.
- No storage migration; no database; no Parquet compaction; no v003.
- No `research_eligible` flipped; no `eligibility_gate_status` /
  `chronological_split_policy` transitioned.
- No `data/microstructure` or `data/research` artefact staged or committed; the
  future output namespace
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/` was not
  created.
- `.claude/scheduled_tasks.lock` remains untracked and uncommitted.
- No credential / `.env` / `.mcp.json` / MCP / Graphify used.
- No retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

---

## 12. Retained verdict ledger

All preserved verbatim:

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

---

## 13. Preserved project locks

All preserved verbatim: §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 =
0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8;
Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13
boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises
invariant (never invoked); Phase 4bb-F canonical path + sidecar policy;
Phase 4bl-F risk tiers; Phase 4bm-U / 4bm-W v002 split policy; Phase 4bn-J-R1
raw-only cap amendment; Phase 4bn-L derived-stack storage budget; Phase 4bn-N
normalization manifest/versioning; Phase 4bn-R feature manifest/versioning;
Phase 4bn-V label manifest/versioning; Phase 4bn-Y chronological split/holdout
policy; Phase 4bn-Z ML-baseline readiness memo; Phase 4bn-AA pre-v002 split-policy
artefact; Phase 4bn-AB source-admissibility posture; Phase 4bn-AC ML dataset
contract; Phase 4bn-AD ML dataset builder readiness verdict; Phase 4bn-AE
pre-registration amendment. All prior phase results preserved verbatim.

---

## 14. No-rescue constraints

The Phase 4bn-AF merge does not, and cannot, be construed as authorising:

- a data-reading ML dataset builder authorization memo (Phase 4bn-AG); a
  current-state consolidation memo; additional skeleton hardening; a
  source-admissibility gate artefact; a data-reading ML dataset builder; a
  research matrix;
- running the skeleton against real data; creating the future output namespace;
  writing any Parquet / sidecar / manifest / gate report;
- ML model training, model selection, scoring, predictions, or any conversion of
  labels into signals;
- strategy signal construction, position state, entry / exit rules, backtest
  design, PnL, or diagnostics;
- any actual data read of the pre-v002 normalized / feature / label segments;
- reading the v002 terminal window or touching the sealed test
  (`test_rows_loaded = 0` preserved);
- relaxing any pre-registered success / continue / kill threshold, adopting a
  decimation stride, or introducing per-row significance inference;
- full-envelope assembly or a holdout-boundary memo;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- additional aggTrades / bookTicker / mid-price / mark-price / order-book
  acquisition;
- storage migration / database creation / Parquet compaction / v003;
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`,
  or `chronological_split_policy` from this phase alone.

---

## 15. Successor authorization

**None.** No successor is authorized by this merge. A **data-reading ML dataset
builder authorization memo (Phase 4bn-AG)** is *recommended* as the next step but
requires separate operator authorization. A **current-state consolidation memo**
is *recommended* as a near-term parallel docs-only option but is not a blocker and
is not authorized.

Candidate successors explicitly **NOT** authorized:

- a data-reading ML dataset builder authorization memo (Phase 4bn-AG;
  recommended; not authorized)
- a current-state consolidation memo (recommended parallel option; not
  authorized)
- additional skeleton hardening
- a source-admissibility gate artefact
- a data-reading ML dataset builder
- a research matrix
- a full-envelope reference-assembly memo
- a holdout-boundary memo
- ML implementation / model training / scoring / predictions / diagnostics
- strategy / signals / PnL / backtest implementation
- additional aggTrades / bookTicker / mid-price / mark-price / order-book
  acquisition
- Phase 5; Phase 4 canonical
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials

---

## 16. Recommended state

**Remain paused.** No next phase authorized.

**Conditional next, NOT authorized:** a **data-reading ML dataset builder
authorization memo (Phase 4bn-AG)** is the cleanest non-paused option. It would
be a docs-only memo that resolves `source_admissible_for_data_read` /
`source_admissible_for_dataset_builder`, binds the leakage proof + Phase 4bn-L
budget preflight into a future data-reading builder, and gates the first actual
data read — reading no data itself. A **current-state consolidation memo** is a
recommended parallel docs-only option (the state doc is now large / partially
stale) but is not a blocker. Neither is authorised by this merge.

---

## 17. Phase 4bn-AF carry-forward (informational)

Recorded here so the merged project state carries the skeleton verdict without
re-reading the report.

**Code/tooling added:** three new source modules. **Tests added:** one offline
synthetic test module (97 tests, all passing).

**Source modules created:**
`pre_v002_ml_dataset_contract.py` (pure constants + 5 frozen dataclasses:
`ContractIdentity`, `SourceScope`, `ManifestBinding`, `EvaluationPreregistration`,
`NonAuthorizationPosture`; imports stdlib + inert schema modules only),
`pre_v002_ml_dataset_builder.py` (`PreV002MlDatasetError` + 12 pure
validators/planners + `FilterResult` / `TransformPlan` / `SkeletonPlan`; imports
stdlib + the contract module + the Phase 4bn-AA split-policy artefact only), and
`pre_v002_ml_dataset_proof.py` (7 proof dataclasses: `SplitProof`,
`AlignmentProof`, `FilteringProof`, `EvaluationPreregistrationProof`,
`BudgetPreflightPlaceholder`, `NonAuthorizationProof`, `DatasetBuilderProof`;
`build_dataset_builder_proof` + `validate_dataset_builder_proof`; inert in-memory
only; writes no sidecar).

**Public API:** builder — `validate_source_scope`, `validate_manifest_hashes`,
`validate_feature_allowlist`, `scan_forbidden_columns`, `find_forbidden_columns`,
`assert_no_forbidden_columns`, `filter_targets`, `assert_strict_alignment`,
`assign_split`, `should_drop_for_split`, `validate_no_boundary_crossing`,
`plan_train_only_transform`, `validate_evaluation_schema`, `build_skeleton_plan`;
proof — `build_dataset_builder_proof`, `validate_dataset_builder_proof`; contract
— constants + frozen dataclasses. All three modules expose a stable `__all__`.

**Contract constants encoded:** contract name
`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`; amendment id
`amendment_001`; BTCUSDT / binance_usdm_futures / aggTrades; segment
2024-03-01..2024-11-30; 275/275/275 partitions; 400,001,695 rows; primary target
`forward_direction_15s` / horizon 15000 ms / classes {-1,0,+1}; high-confidence
threshold 0.8; cost locks 8 bps/side · 16 bps round-trip; inert output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`; the eight
expected manifest/config/gate-report SHA256s (`0e96ae37…` / `4881eb87…` /
`0726b41d…` / `69746c88…` / `b3bd5d2b…` / `3452fd9d…` / `db731d1b…` / `ffb5b092…`);
the full rejected v002-terminal config hashes `819cfa7a…` / `352bad41…` (values +
prefixes); the 45-column allowlist (imported from committed `FEATURE_NAMES_V002`);
the 17 excluded lineage columns; `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`
(`forward_log_return` / `forward_direction` / `horizon_censored_flag` / `label_` /
`split_` / `censored_`); forbidden raw-price columns.

**Phase 4bn-AE amendment obligations encoded:** mandatory metric registry (21
entries); granularities aggregate/utc_month/utc_date; row-level metrics
descriptive-only; decision block units (utc_date, utc_month); decimation stride
None / policy `reserved_not_adopted`; high-confidence threshold 0.8; cost locks
8/16 bps; success thresholds +2.0 pp accuracy / +1.0 pp balanced accuracy / +0.03
macro-F1; claim-scope allowed/forbidden; non-authorization flags all False;
no-strategy boundary; enforced by `validate_evaluation_schema`.

**Source-scope validation:** requires BTCUSDT / binance_usdm_futures / aggTrades /
2024-03-01 / 2024-11-30 / correct partition + row counts; rejects v002 terminal,
sealed test, full envelope, private / authenticated / external source, and
missing critical keys.

**Manifest/hash/gate validation:** verifies the three manifest SHA256s, the
feature/label config hashes, optional gate-report SHA256s and partition counts;
rejects wrong/missing hashes, the rejected v002 `819cfa7a…` / `352bad41…` values
and prefixes, and wrong partition counts.

**Feature allowlist / forbidden-column validation:** exactly 45 columns
(order-independent input, canonical order returned); rejects missing / extra /
duplicate / lineage / label / support / forward / split / censor / raw-price
columns; `find_forbidden_columns` / `scan_forbidden_columns` /
`assert_no_forbidden_columns` provide strict detection.

**Split-policy binding:** `assign_split` delegates to Phase 4bn-AA
`split_for_timestamp_ms`, returns lowercase `train`/`validation`/`holdout`/
`embargo`, and hard-raises (wrapped as `PreV002MlDatasetError`) for out-of-segment
/ v002 / sealed dates; `should_drop_for_split` drops embargo only;
`validate_no_boundary_crossing` uses the Phase 4bn-AA helper; holdout never
crosses; embargo rows fail closed.

**Target filtering:** `filter_targets` drops (never imputes) by precedence
invalid_price → censored → null_direction → null_log_return, records
`dropped_by_reason`, preserves valid rows, and never mutates the input.

**Strict alignment:** `assert_strict_alignment` compares `row_index`,
`agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`, and optional
`symbol` / `utc_date` per row in order; fails closed on length / value / order
mismatch or missing key; no join repair / reorder / fill / tolerance merge /
heuristic dedup.

**Train-only transform planning:** `plan_train_only_transform` returns an inert
`TransformPlan` fit on `train` only; non-train fit (validation / holdout / test /
embargo) fails closed; fixed-zero fit-free imputation; boolean flags
unstandardized; no actual fitting.

**Evaluation schema / metric registry:** `validate_evaluation_schema` enforces
the mandatory metric registry, the three granularities, the descriptive-only
flag, the dependence caveat, the null decimation stride, the success constants,
the calibration schema, the cost-descriptive fields, and the no-strategy
boundary.

**Dependence / date-month block schema:** `ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY=True`,
`DECISION_BLOCK_UNITS=("utc_date","utc_month")`, `DECIMATION_STRIDE=None`,
`DECIMATION_POLICY="reserved_not_adopted"`; proof includes dependence-caveat and
granularity fields.

**Calibration / confidence-tail schema:** `HIGH_CONFIDENCE_THRESHOLD=0.8`,
mandatory calibration/reliability and high-confidence-tail metrics; proof
calibration-schema and threshold fields.

**Cost-realism descriptive schema:** cost locks 8/16 bps, `cost_descriptive_fields`
requirement, proof cost fields; descriptive only; authorizes no trading rule /
label / PnL / backtest.

**Success / continue / kill constants:** `SUCCESS_ACCURACY_UPLIFT_PP=2.0`,
`SUCCESS_BALANCED_ACCURACY_UPLIFT_PP=1.0`, `SUCCESS_MACRO_F1_UPLIFT=0.03`, and four
bounded `CONTINUE_FOLLOWUP_CATEGORIES` (longer-horizon label memo; bookTicker /
mid-price data-admissibility memo; code-only evaluation-framework extension;
fixed-capacity model-comparison memo).

**Proof schema:** `validate_dataset_builder_proof` fails closed on wrong split
counts (214/1/45/1/14), `test_rows_loaded≠0`, v002/sealed access, non-empty
forbidden scan, missing metrics/granularities, imputed targets, a non-placeholder
budget preflight, any True non-authorization flag, or a created output namespace.
`BudgetPreflightPlaceholder` is interface-shape only (`is_placeholder=True`,
`measured_disk=False`, `wrote_output=False`, Phase 4bn-L caps echoed; never
measures disk or writes).

**No-data-I/O controls:** no import-time side effects beyond constant assertions;
no filesystem reads/writes; no path resolution; no pyarrow reads/writes; no
network; a test monkeypatches `open` / `Path.mkdir` / `Path.read_text` /
`Path.write_text` / `Path.open` / `pyarrow.parquet.read_table` / `write_table` to
raise, then runs the full public surface without tripping any guard.

**No-output-namespace proof:** a test asserts
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` does not exist
before or after exercising the surface and is never created.

**Remaining blockers before data reads:** code-level builder bound to the passed
gates (`3452fd9d…` / `db731d1b…` / `ffb5b09…`), manifests, hashes, and the split
artefact; leakage proof + Phase 4bn-L budget preflight bound into a data-reading
builder; separate data-read authorization
(`source_admissible_for_data_read=false`).
**Remaining blockers before real dataset builder:** the readiness decision (done);
this passing code-only skeleton (done); leakage proof + budget preflight designed
into the data-reading builder; separate builder authorization
(`source_admissible_for_dataset_builder=false`).
**Remaining blockers before ML training:** all data-read + builder blockers;
target/horizon/filtering locked (done) and the evaluation/dependence/success-kill
layer pre-registered (Phase 4bn-AE) and now encoded (this phase); a committed
end-to-end pre-v002 trainer (does **not** exist); separate ML authorization
(`ml_authorized=false`).

**Selected next recommendation:**
`RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_AUTHORIZATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— a docs-only data-reading builder authorization memo (Phase 4bn-AG). A
current-state consolidation memo is a recommended near-term parallel docs-only
option (not a blocker). Final `git status` / `git log` / SHAs are reproduced in
the final operator report so the operator need not run a separate status/SHA check
manually.
