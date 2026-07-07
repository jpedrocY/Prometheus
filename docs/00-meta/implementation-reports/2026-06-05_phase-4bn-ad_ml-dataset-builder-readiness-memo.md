# Phase 4bn-AD — ML Dataset Builder Readiness Memo

## 1. Purpose

This is a **docs-only** ML dataset builder readiness memo. It answers exactly
one question:

> Now that the pre-v002 ML dataset **contract** is recorded (Phase 4bn-AC), what
> is the safest next implementation step — remain paused, a **code-only** ML
> dataset builder skeleton (synthetic fixtures + offline tests, no data read), a
> **data-reading** ML dataset builder, another docs-only memo / gate first, or
> close the ML-baseline arc?

The memo **settles readiness and records prerequisites**. It builds nothing,
reads no local data, creates no local data, adds no code / tests / scripts,
creates no split file / research matrix / ML dataset / ML config / manifest /
gate report / sidecar, transitions no manifest field, and authorizes no
successor. Its conclusions are determined from committed documentation and
committed source read read-only; every figure it carries forward comes from the
predecessor implementation reports already merged to `main` (chiefly Phase
4bn-AC), not from reading any local artefact.

The expected conservative outcome — confirmed below — is that the project is
ready for a **code-only ML dataset builder skeleton with synthetic tests only**,
and is **not** ready for a data-reading builder, dataset creation, research-matrix
creation, or ML training.

---

## 2. Authority and repository state

- **Phase:** 4bn-AD — ML Dataset Builder Readiness Memo.
- **Authorization:** separately authorized by the operator following the Phase
  4bn-AC decision
  `RECOMMEND_AUTHORIZE_ML_DATASET_BUILDER_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Branch:** `phase-4bn-ad/ml-dataset-builder-readiness-memo`.
- **Base `main` SHA:** `0331aead38f6c43d7aec1cc22da0501c38b0f53e`
  (`docs(phase-4bn-ac): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 0331aead…` verified.
- **Predecessors present on `main`:** Phase 4bn-AC SHA-finalization `0331aea`,
  merge-closeout `aab527a`, merge `4543103`, branch `c9c6c7e`; Phase 4bn-AB
  finalization `46bcdd3` present as predecessor.
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Gitignored data namespaces:** `data/microstructure/` (`.gitignore:85`) and
  `data/research/` (`.gitignore:88`) — both confirmed; both remain uncommitted.

This phase is branch-complete only by its own work; it is **not merged into
`main`** and is **not project-complete**. It becomes project-complete only when a
separately authorized merge phase records its merge-closeout on `main`.

---

## 3. Phase type and strict scope

- **Phase type:** docs-only / ML dataset builder readiness /
  code-only-vs-data-reading decision / implementation-sequencing / no-data-read
  memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3, because this phase
  decides whether the next implementation step should be a code-only ML dataset
  builder skeleton with synthetic tests, a data-reading builder, another
  readiness / gate phase, or no builder at all. An incorrect readiness decision
  could authorize data reads too early, weaken leakage controls, bypass budget
  preflight, or create invalid ML dataset artefacts — even though this phase is
  docs-only and reads no local data.

**Strict scope (all enforced):** no code, no tests, no scripts, no data read,
no data created, no inspection of any file under `data/microstructure/` or
`data/research/`, no inspection of raw zip / normalized / feature / label
Parquet / manifest / gate report / sidecar, no v002-terminal read, no
sealed-test read, no split file, no research matrix, no ML dataset, no ML
config, no manifest, no gate report, no sidecar, no training, no scoring, no
prediction, no diagnostics, no strategy / signals / PnL / backtests, no
`research_eligible` flip, no `eligibility_gate_status` transition, no
`chronological_split_policy` set, no invocation of the Phase 4aw
`flip_research_eligible(...)` always-raises invariant, no successor
authorization. The memo does **not** create the future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`.

---

## 4. Evidence base and input boundary

This memo was written from **committed docs + committed source/tests only**. No
local artefact under `data/microstructure/` or `data/research/` was read or
inspected. The README is treated as potentially stale and is **not** used as a
current-state authority.

**Committed docs grounding (read-only):** the process standards
(`merge-closeout-standard`, `phase-risk-tiering-standard`,
`phase-workflow-standard`, `phase-prompt-template`, `operator-report-standard`);
`current-project-state.md`; and the Phase 4bn-L / O / P / S / T / W / X / Y / Z /
AA / AB / AC implementation reports, merge-closeouts, and closeouts (the source of
every figure carried forward in §5). The Phase 4bn-AC ML dataset contract memo,
its closeout, and its merge-closeout are the primary predecessor authority.

**Committed source grounding (read-only, for readiness precision):**

- `src/prometheus/research/microstructure/pre_v002_split_policy.py` — the Phase
  4bn-AA split artefact; its exact public API and windows ground the skeleton's
  split-binding surface (§16, §18).
- `tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py` — the
  split-artefact contract-test precedent.
- `src/prometheus/research/microstructure/diagnostics_split_policy_v002.py`,
  `ml_baseline_design_v002.py`, `ml_baseline_dataset_v002.py` — the **v002
  terminal-bound** ML-baseline stack, read only to establish the reuse boundary
  (§7). In particular `ml_baseline_dataset_v002.py` is the direct precedent for a
  *data-reading* loader (`discover_partition_refs()` reads manifests and calls
  `pq.read_table`; `load_partition_matrices()` reads Parquet; the
  `StreamingStandardizer.fit_partition` train-only guard), and is therefore
  precisely what a code-only skeleton must **not** replicate.
- `features_schema_v002.py`, `labels_schema_v002.py`, `labels_compute_v002.py`,
  `features_compute_v002.py` — the schema / column / forbidden-substring
  precedent for the contract constants the skeleton would encode.

**Input boundary (not read):** no local Parquet (raw / normalized / feature /
label); no local raw zip; no local manifest or gate report under
`data/microstructure/`; no v002-terminal window; no sealed-test file; no
`data/research/` output; no v002-terminal terminal files. The absence of a
committed pre-v002 dataset builder, a builder proof-schema implementation, and an
end-to-end pre-v002 trainer is itself evidence (§7, §10, §25).

---

## 5. Phase 4bn-AC contract carried forward

The Phase 4bn-AC memo recorded, **by reference only**, the binding contract
`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001` that any future
pre-v002 ML dataset builder must obey. Carried forward verbatim (not re-derived
here):

- **Source scope (permitted, by reference / future-authorized read only):**
  BTCUSDT / Binance USDⓈ-M futures / aggTrades; pre-v002 only 2024-03-01 ..
  2024-11-30 inclusive UTC (275 dates; 400,001,695 rows by reference); Phase
  4bn-S features (manifest SHA256
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`;
  `feature_config_hash`
  `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`; feature gate
  `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08` 27/27) +
  Phase 4bn-W labels (manifest SHA256
  `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`;
  `label_config_hash`
  `b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`; label gate
  `ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984` 40/40) +
  Phase 4bn-O normalized lineage (manifest SHA256
  `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`; normalized
  gate `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134` 25/25).
- **Forbidden source scope:** v002 terminal (2024-12-01 .. 2025-02-28); sealed
  test (2025-02-14 .. 2025-02-28); full-envelope assembly; non-BTCUSDT; spot /
  mark-price / order-book / kline / liquidation / funding / open-interest /
  cross-venue; newly acquired data; raw zip; any family not in the pre-v002 chain
  (incl. published `819cfa7a…` / `352bad41…`); `data/research` priors; external /
  private / authenticated sources — all fail-closed.
- **Split binding:** import `pre_v002_split_policy.py`
  (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`); train
  2024-03-01..2024-09-30 (214) / embargo 2024-10-01 / validation
  2024-10-02..2024-11-15 (45) / embargo 2024-11-16 / internal holdout (dry-run,
  NOT sealed test) 2024-11-17..2024-11-30 (14) = 275; assignment by
  `source_transact_time_ms` UTC date via `split_for_timestamp_ms`; drop embargo;
  per-horizon earlier-split boundary protection; hard-raise on out-of-segment /
  v002 / sealed dates; no shuffle / random / k-fold / bootstrap / resampling.
- **Target / horizon:** family `microstructure_labels_aggtrades_v001 @ v002`;
  primary first-baseline target `forward_direction_15s` (3-class signed
  `{-1, 0, +1}`, zero class preserved); secondary descriptive (not a model
  target) `forward_log_return_15s`; 1s/5s/60s deferred; no binary collapse; no
  regression-only reframing; no barrier / stop / MFE / MAE / R-multiple / PnL
  labels.
- **Feature allowlist:** exactly the 45 causal computed `FEATURE_SCHEMA_V002`
  columns; 17 lineage columns excluded; all label / support / split / censor
  columns excluded; forbidden substrings `forward_log_return`,
  `forward_direction`, `horizon_censored_flag`, `label_`, `split_`, `censored_`;
  raw prices excluded unless a future revision authorizes; no feature selection /
  ranking / pruning / PCA / embeddings.
- **Filtering / alignment / train-only transforms / leakage proof /
  budget preflight / output posture:** exactly as recorded in Phase 4bn-AC §13 –
  §21 and carried into §17 – §22 of this memo.
- **Phase 4bn-AC result:**
  `ML_DATASET_CONTRACT_RECORDED__PRE_V002_CONTRACT_ONLY__NO_DATA_READ__REMAIN_PAUSED`.
- **Phase 4bn-AC decision:**
  `RECOMMEND_AUTHORIZE_ML_DATASET_BUILDER_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`,
  with the noted alternative
  `RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

**Admissibility posture carried forward (Phase 4bn-AB, unchanged):**
`layer_integrity_passed=true`; `source_admissible_for_dataset_contract=true`;
`source_admissible_for_data_read=false`;
`source_admissible_for_dataset_builder=false`; `ml_authorized=false`;
`diagnostics_authorized=false`; `strategy_backtest_authorized=false`;
`manifest_research_eligible=false`; `manifest_eligibility_gate_status=pending`;
`manifest_chronological_split_policy=not set`.

This memo alters none of these values and sets no new manifest field.

---

## 6. Builder-readiness question

This memo answers the following seventeen readiness questions (verdicts
consolidated in §8):

1. Is the project ready for a docs-only builder readiness **decision**? — **Yes.**
2. Ready for a **code-only** ML dataset builder skeleton (synthetic fixtures +
   offline tests only)? — **Yes.**
3. Ready for a **data-reading** ML dataset builder? — **No.**
4. Ready to create any **local dataset output**? — **No.**
5. Ready to create a **research matrix**? — **No.**
6. Ready to **train ML**? — **No.**
7. Should the next phase be a **code-only skeleton** or **another docs memo**? —
   Code-only skeleton (§26 – §27).
8. What exact **source/data boundaries** must the future skeleton enforce? — §19,
   §20.
9. What exact **APIs / modules** should the future skeleton implement? — §15,
   §16.
10. What **tests** should the future skeleton include? — §18.
11. What must remain **impossible** in the skeleton? — §19, §20.
12. What remains required before a later **data-reading builder**? — §24.
13. What remains required before **ML training**? — §25.
14. Should `ml_baseline_dataset_v002.py` be **reused, wrapped, copied, or treated
    only as precedent**? — Precedent only; new pre-v002-specific module (§7, §14).
15. How should the skeleton avoid data I/O at **import and runtime**? — §19.
16. How should the skeleton **prove** no output namespace is created? — §20, §21.
17. What **result / decision** should this phase record? — §29, §30.

---

## 7. Existing v002-bound ML dataset tooling boundary

The only committed ML-baseline dataset tooling is the **Phase 4bn-B** stack,
identity-bound to the **published v002 terminal** family:

- `diagnostics_split_policy_v002.py` (Phase 4bm-W) — encodes **only** the v002
  split `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (train
  2024-12-01..2025-01-14 / validation 2025-01-15..2025-02-13 / test
  2025-02-14..2025-02-28); `split_for_date()` **raises `SplitPolicyError`** for
  every pre-v002 date.
- `ml_baseline_design_v002.py` (Phase 4bn-B) — design constants hardcoded to the
  v002 terminal: `EXPECTED_PARTITION_COUNT = 90`,
  `EXPECTED_TOTAL_ROW_COUNT = 155,153,449`,
  `EXPECTED_FEATURE_CONFIG_HASH = 819cfa7a…`,
  `EXPECTED_LABEL_CONFIG_HASH = 352bad41…`. It also holds the **reusable leakage
  controls**: the frozen 45-column `COMPUTED_FEATURE_COLUMN_NAMES` (`len == 45`),
  the 17 `EXCLUDED_LINEAGE_COLUMN_NAMES`, the `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`
  guard, the `STANDARDIZATION_RULE` / `STANDARDIZATION_EPSILON` /
  `IMPUTATION_RULE` / `IMPUTATION_FILL_VALUE` train-only transform rules, the
  3-class signed direction framing, and the full `NON_AUTHORIZATION_FLAGS` block.
- `ml_baseline_dataset_v002.py` (Phase 4bn-B) — a **data-reading**,
  bounded-memory streaming loader. `discover_partition_refs()` reads the label /
  feature manifests, hard-fails (`MlBaselineDatasetError`) unless the v002 family
  / version / `feature_config_hash 819cfa7a…` match, expects exactly 90
  partitions, resolves partition paths under `data/`, and asserts each Parquet
  file exists; `load_partition_matrices()` calls `pq.read_table` on real Parquet
  and applies the v002 `policy.split_for_date()`, the alignment check, the
  supervised mask, imputation, and standardization. It would reject the pre-v002
  segment on the first guard (`feature_config_hash 0726b41d…` ≠ `819cfa7a…`;
  275 ≠ 90 partitions).
- **`ml_baseline_splits.py` and `ml_baseline_train.py` do not exist.** There is
  **no committed end-to-end trainer**, and no committed pre-v002 dataset builder.

**Boundary conclusion.** The committed stack is **inadmissible as direct builder
code for pre-v002**. Per the Phase 4bn-AC §10 binding, it may be used **only as
precedent** — for the column constants (the 45-column matrix, the 17 lineage
exclusions, the forbidden substrings), the train-only transform rules, the
supervised-mask semantics, and the non-authorization flags. It must **not** be
reused by "just changing constants": `ml_baseline_dataset_v002.py` is a
*data-reading* module whose whole purpose is to read Parquet, whereas the next
recommended step is explicitly a **no-data-read** skeleton. Wrapping or copying
it would import real-I/O functions (`pq.read_table`, manifest resolution,
filesystem existence assertions) into a phase that must prove it performs no data
I/O. The preferred posture (§14) is therefore a **new pre-v002-specific
skeleton** that encodes the Phase 4bn-AC contract in code and validates it against
synthetic in-memory fixtures only, borrowing the v002 constants and rules as
precedent without importing its data-reading surface.

---

## 8. Readiness verdict matrix

**Verdict: the project is contract-ready and skeleton-ready, but NOT
data-reading-ready, NOT dataset-ready, and NOT ML-ready.**

| # | Readiness question | Verdict |
|---|---|---|
| 1 | Docs-only builder readiness decision ready? | **Yes** (this phase). |
| 2 | Code-only skeleton (synthetic fixtures + offline tests) ready? | **Yes.** |
| 3 | Data-reading ML dataset builder ready? | **No.** |
| 4 | Local dataset output creation ready? | **No.** |
| 5 | Research matrix creation ready? | **No.** |
| 6 | ML training ready? | **No.** |
| 7 | Model scoring / predictions / diagnostics ready? | **No.** |
| 8 | Strategy / signals / PnL / backtest ready? | **No.** |
| 9 | Next phase: code-only skeleton or another docs memo? | **Code-only skeleton.** |
| 10 | Reuse `ml_baseline_dataset_v002.py` directly? | **No — precedent only.** |
| 11 | Create the future output namespace now? | **No.** |
| 12 | Flip any eligibility / manifest field? | **No.** |

**Why a code-only skeleton is ready.** It reads no data and creates no output,
so it is **not** blocked by `source_admissible_for_data_read=false` or
`source_admissible_for_dataset_builder=false` — exactly as the Phase 4bn-AA split
artefact (pure arithmetic, no I/O) was buildable while sources stayed
non-eligible. The Phase 4bn-AC contract is now precise enough to encode as code
constants and validators. A skeleton exercises contract enforcement (allowlist,
forbidden-column scan, split assignment, embargo drop, alignment, target
filtering, train-only transform planning, proof schema) against synthetic
fixtures, catching contract bugs **before** any real data is ever touched.

**Why a data-reading builder is not ready.** It would read the pre-v002 feature
and label Parquet, which requires `source_admissible_for_data_read=true` and
`source_admissible_for_dataset_builder=true` — both currently **false**. There is
no code-only skeleton, no builder proof-schema implementation, no synthetic
validation, and no builder-bound budget preflight yet. Any one of these is
independently disqualifying (§24).

---

## 9. Code-only skeleton readiness

**Ready.** A code-only ML dataset builder skeleton is the safest next
implementation step, on the same grounds that made the Phase 4bn-AA split
artefact safe:

- It performs **no data I/O** — no Parquet read, no manifest read, no gate-report
  read, no directory creation, no Parquet write — at import time or runtime.
- It is **not** gated by source admissibility, because it touches no data and
  confers no eligibility.
- It makes real, testable progress: it turns the Phase 4bn-AC prose contract into
  executable constants + validators + a proof schema, all exercised against
  synthetic in-memory fixtures.
- It hard-encodes the fail-closed and non-authorization posture so a *future*
  data-reading builder inherits a validated, contract-bound core rather than
  re-deriving it under data-read pressure.

The skeleton is **not** a dataset builder: it validates the contract; it does not
build a dataset, and it must be structurally incapable of doing so (§19, §20).

---

## 10. Data-reading builder readiness

**Not ready.** A real data-reading ML dataset builder must remain blocked behind
a separate authorization, because **all** of the following hold:

- `source_admissible_for_data_read = false`;
- `source_admissible_for_dataset_builder = false`;
- no code-only skeleton exists;
- no builder **proof-schema implementation** exists;
- no **synthetic validation** of the contract exists;
- no **budget-preflight** implementation is bound to this builder;
- no explicit **data-read authorization** exists.

Therefore this memo does **not** recommend a data-reading builder as the next
phase. A data-reading builder is a later, separately-authorized phase that may
only be considered after the skeleton and its synthetic validation exist and
after data-read admissibility is explicitly resolved (§24).

---

## 11. Dataset output readiness

**Not ready.** No local dataset output may be created. The future output
namespace `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
must **not** be created by this phase or by a code-only skeleton phase. Creating a
dataset requires reading the feature / label Parquet (blocked, §10), a
builder-bound budget preflight (does not exist, §22), Phase 4bb-F canonical
sidecars for every artefact, and a separate builder authorization. A code-only
skeleton may define the output-namespace path **as an inert string constant** for
proof purposes but must not create, write to, or even define a filesystem-mutating
function bound to it (§19, §20).

---

## 12. Research matrix readiness

**Not ready.** No research matrix may be created. A research matrix is a
downstream dataset artefact assembled from real feature / label rows; it inherits
every data-reading blocker in §10 plus the dataset-output blockers in §11. The
skeleton validates matrix-assembly *logic* against synthetic fixtures (allowlist
selection, forbidden-column scan, positional alignment) but produces no real
matrix and writes nothing.

---

## 13. ML training readiness

**Not ready.** No ML training, model, scoring, prediction, diagnostics, strategy,
signal, PnL, or backtest may occur. ML training inherits all data-read and
dataset-builder blockers (§10 – §12), plus: `ml_authorized = false`; no committed
end-to-end pre-v002 trainer exists (`ml_baseline_train.py` does not exist, §7);
and a separate ML authorization is required. The Phase 4bn-AC contract has locked
the first target / horizon / filtering (`forward_direction_15s`, 15s, 3-class
signed), but a locked contract is a precondition for training, not an
authorization of it.

---

## 14. Recommended future skeleton scope

If — and only if — separately authorized, the next phase (assume **Phase
4bn-AE**) should be a **new pre-v002-specific code-only skeleton** with the
following scope:

- **Add a new pre-v002-specific builder skeleton** (do not wrap / copy the
  v002-terminal `ml_baseline_dataset_v002.py`; use it as precedent only, §7).
- **Encode the Phase 4bn-AC contract constants in code**: the 45-column feature
  allowlist, the 17 lineage exclusions, the forbidden substrings, the target /
  horizon selection (`forward_direction_15s`, 15s), the 275/275 partition-count
  expectation, and the pre-v002 feature / label / normalized manifest / config /
  gate identifiers as **string constants** (not read from disk).
- **Import the Phase 4bn-AA split artefact** (`pre_v002_split_policy.py`) as the
  sole split authority — it is pure arithmetic and performs no I/O.
- **Use synthetic in-memory fixtures only**: manifest-like dicts, feature /
  label "partitions" as small in-memory tables/arrays, hash / gate identifiers as
  strings — never a real Parquet, manifest, or gate report.
- **Validate, against synthetic inputs only:** source-scope metadata; manifest /
  hash / gate identifier binding (string equality, rejecting the v002 `819cfa7a…`
  / `352bad41…` values); the feature allowlist and forbidden-column scan; label
  target / horizon filtering (null / censored / invalid drops); strict positional
  alignment; split assignment and embargo drop; per-horizon boundary-crossing
  checks; train-only transform *planning* (which split statistics come from,
  without fitting on real data); and the proof / sidecar schema shape.
- **Define the proof / sidecar schema in memory** (an inert, JSON-serialisable
  dict, mirroring `pre_v002_split_policy.build_split_policy_contract()`), with the
  non-authorization flags all `False`.
- **Define the output-namespace path as an inert string constant** but create no
  directory and write no file; prefer **not defining any filesystem-creating
  function at all** in the skeleton.
- **Carry non-authorization flags** and **fail closed** on any forbidden scope
  (out-of-segment date, v002 / sealed date, wrong hash, forbidden column, wrong
  partition count).

The skeleton implements **interfaces, validators, and the proof schema against
synthetic fixtures only**. It does **not** read local data, create output
directories, write Parquet, mutate manifests, produce `data/research` /
`data/microstructure` artefacts, or call any endpoint.

---

## 15. Future skeleton module / test naming recommendation

Recommended future modules (to be **implemented by a later, separately-authorized
phase**, not by this memo):

- `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py` —
  contract constants + inert contract-builder helper.
- `src/prometheus/research/microstructure/pre_v002_ml_dataset_builder.py` —
  the code-only skeleton: interfaces + validators over synthetic fixtures; no
  data I/O.
- `src/prometheus/research/microstructure/pre_v002_ml_dataset_proof.py` —
  the proof / sidecar schema + a pure proof-assembler over synthetic inputs.

Recommended future test path:

- `tests/research/microstructure/test_phase4bn_ae_pre_v002_ml_dataset_builder_skeleton.py`.

A future skeleton phase may reasonably be **Phase 4bn-AE** if Phase 4bn-AD is
merged first. This memo recommends these names but **implements none of them**.

---

## 16. Future skeleton API surface recommendation

The skeleton's public surface should be small, pure, and synthetic-input-only.
Modeled on the shape of `pre_v002_split_policy.py` (constants + pure functions +
an inert contract dict) and the *logic* (not the I/O) of
`ml_baseline_dataset_v002.py`:

- **Contract constants:** `PRE_V002_ML_DATASET_CONTRACT_NAME`,
  `EXPECTED_FEATURE_PARTITION_COUNT = 275`,
  `EXPECTED_LABEL_PARTITION_COUNT = 275`, `PRIMARY_TARGET = "forward_direction_15s"`,
  `PRIMARY_HORIZON_MS = 15000`, `ALLOWED_FEATURE_COLUMNS` (the 45 names),
  `EXCLUDED_LINEAGE_COLUMNS` (the 17 names), `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`,
  `EXPECTED_FEATURE_CONFIG_HASH = "0726b41d…"`,
  `EXPECTED_LABEL_CONFIG_HASH = "b3bd5d2b…"`, the normalized / feature / label
  manifest + gate SHAs, `REJECTED_V002_FEATURE_CONFIG_HASH = "819cfa7a…"`,
  `REJECTED_V002_LABEL_CONFIG_HASH = "352bad41…"`, and
  `OUTPUT_NAMESPACE_PATH = "data/research/microstructure/ml_datasets/pre_v002_contract_v001/"`
  (inert string; never created).
- **Validators (pure, over synthetic dicts / arrays):**
  `validate_source_scope(manifest_like) -> None|raise`;
  `validate_manifest_hashes(feature_like, label_like, normalized_like) -> None|raise`
  (rejects v002 hashes / wrong partition counts);
  `validate_feature_allowlist(columns) -> None|raise`;
  `scan_forbidden_columns(columns) -> tuple[str, ...]` (must be empty);
  `filter_targets(direction, log_return, censored_flag, invalid_price_flag) ->
  mask` (drop null / censored / invalid; never impute);
  `assert_strict_alignment(feature_keys, label_keys) -> None|raise`;
  `assign_split(source_transact_time_ms) -> str` (delegates to
  `pre_v002_split_policy.split_for_timestamp_ms`);
  `plan_train_only_transform(split_row_counts) -> dict` (records that statistics
  come from `train` only; fits nothing on real data).
- **Proof assembler (pure):** `build_dataset_builder_proof(**synthetic) -> dict`
  returning the §21 schema with non-authorization flags all `False`.

Every function must be a **pure transform of its arguments** — no default that
resolves to a filesystem path, no manifest read, no Parquet read, no directory
creation.

---

## 17. Future skeleton synthetic fixture requirements

The skeleton's tests must use **synthetic in-memory fixtures only**:

- **Manifest-like objects:** small Python dicts carrying `dataset_family`,
  `dataset_version`, `feature_config_hash` / `label_config_hash`,
  `per_day_outputs` with a handful of synthetic `utc_date` entries — never a real
  manifest file.
- **Feature / label "partitions":** tiny in-memory tables / arrays (a few rows)
  with the alignment keys (`row_index`, `agg_trade_id`, `feature_timestamp_ms`,
  `source_transact_time_ms`) and a subset of the 45 feature columns + the active
  label columns — never a real Parquet.
- **Hash / gate identifiers:** plain strings (both the correct pre-v002 values and
  deliberately wrong / v002 values, to exercise fail-closed).
- **Timestamps:** hand-chosen epoch-ms values inside and outside the pre-v002
  segment (incl. an embargo date, a boundary-crossing case, a v002 date, a
  sealed-test date) to exercise assignment, embargo drop, boundary protection, and
  hard-raise.
- **No fixture may reference a path under `data/microstructure/` or
  `data/research/`.** No fixture is loaded from disk.

---

## 18. Future skeleton validation requirements

The future skeleton's offline tests must cover (mirroring Phase 4bn-AC §22, over
synthetic inputs only):

- manifest / hash / gate binding (accept pre-v002 values; **reject** v002
  `819cfa7a…` / `352bad41…` and wrong partition counts);
- partition-count expectation 275 / 275;
- pre-v002 date range 2024-03-01 .. 2024-11-30;
- v002 / sealed exclusion (hard-raise via the split artefact);
- split assignment via `pre_v002_split_policy.py`; embargo-date dropping;
  per-horizon boundary-crossing exclusion;
- horizon validation (15s primary; 1s/5s/60s known);
- target censored / null / invalid filtering; never-impute;
- feature allowlist exactly 45 columns; forbidden-column substring scan empty;
- no-raw-price;
- strict positional alignment (fail closed on key mismatch);
- train-only transform planning (statistics attributed to `train` only);
- proof / sidecar schema shape; non-authorization flags all `False`;
- **no-data-I/O proof** (§19) and **no-output-namespace proof** (§20).

---

## 19. Future skeleton no-data-I/O controls

The skeleton must be **structurally incapable of data I/O** at import and
runtime. Recommended controls:

- **No import-time side effects:** the module performs no read/write at import;
  it defines only constants, classes, and pure functions (as
  `pre_v002_split_policy.py` does).
- **No filesystem-reading calls:** the skeleton imports and calls **no**
  `pyarrow.parquet.read_table`, `open()`, `Path.read_text`, `json.load` over a
  file, manifest reader, or gate-report reader. Validators accept
  already-in-memory synthetic objects as arguments; they never resolve a path.
- **No filesystem-writing calls:** no `Path.mkdir`, `open(..., "w")`,
  `pq.write_table`, or sidecar writer. Prefer **not defining** any
  filesystem-creating function at all.
- **No network / endpoint calls.**
- **Tests assert absence:** at least one test greps the skeleton module (or
  monkeypatches `builtins.open` / `pyarrow.parquet.read_table` / `Path.mkdir` to
  raise) to prove that exercising the full validator surface performs **zero**
  file reads, file writes, or directory creations.

This is the same discipline `pre_v002_split_policy.py` already documents ("This
module performs no I/O … writes nothing and mutates nothing … declares no local
data-path constants").

---

## 20. Future skeleton fail-closed controls

The skeleton must **fail closed** (raise a dedicated error, e.g.
`PreV002MlDatasetError`) on any forbidden condition, and prove it did **not**
create the output namespace:

- any out-of-segment / v002-terminal / sealed-test date (delegated to the split
  artefact's `PreV002SplitPolicyError`);
- any manifest / config / gate identifier mismatch, including the v002
  `819cfa7a…` / `352bad41…` values;
- any wrong partition count (≠ 275);
- any forbidden model-matrix column (substring scan non-empty);
- any raw-price column absent an explicit future authorization;
- any feature/label key-alignment mismatch;
- any attempt to select on / fit transforms using validation / holdout / test.

**No-output-namespace proof:** a test must assert that after the full validator +
proof surface runs, `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
does **not** exist (was not created), and that `OUTPUT_NAMESPACE_PATH` is only an
inert string. Any missing / malformed synthetic input must raise, never fall back
to a permissive default.

---

## 21. Future builder proof / sidecar schema requirements

A future builder (and the skeleton's inert proof-assembler) must emit a
machine-checkable proof with a Phase 4bb-F canonical sidecar, mirroring Phase
4bn-AC §19, containing at least:

- exact split-policy name
  (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`);
- split-policy module path + version / commit SHA;
- date-assignment counts **214 / 1 / 45 / 1 / 14**; no missing / duplicate /
  multi-assigned in-segment dates; no `EMBARGO` date used; **zero** out-of-segment
  dates;
- `v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
  `test_rows_loaded = 0`;
- no random / shuffle / k-fold / bootstrap; deterministic assignment by
  `source_transact_time_ms` UTC date;
- per-horizon **zero** earlier-split boundary-crossing rows;
- strict feature/label key-alignment counts;
- target null / censored / invalid **rows dropped, by split**;
- active feature-column list hash (45 columns, in order);
- forbidden-column scan result (empty);
- train-only transform provenance;
- budget-preflight result (§22);
- non-authorization flags all `False` for ML / diagnostics / strategy / PnL /
  backtest / live / exchange-write.

In the **skeleton**, this schema is validated against synthetic inputs only; it
writes no real proof file.

---

## 22. Future budget-preflight integration requirements

A future **data-reading** builder must run the Phase 4bn-L budget preflight
**before any write** and **fail closed** on any breach (carried from Phase
4bn-AC §20):

- derived footprint: **warn 75 GiB / hard 125 GiB**;
- total derived-stack: **warn 250 GiB / hard 300 GiB**;
- runtime: **warn 4 h / hard 8 h**;
- temp: **warn 50 GiB / hard 100 GiB**;
- `D:` free space **≥ 500 GiB before start**; **fail closed below 350 GiB
  during**.

In the **code-only skeleton**, the budget-preflight is represented only as a
**proof field / interface shape** validated against synthetic inputs — no real
disk / runtime measurement, no write. A real budget preflight bound to a real
builder is a data-reading-builder concern and remains blocked (§24).

---

## 23. Remaining blockers before data reads

A data read on the pre-v002 segment remains blocked until **all** of:

- the ML dataset contract is recorded (Phase 4bn-AC — done); **and**
- a code-level builder is implemented and bound to the passed gates
  (`3452fd9d…` / `db731d1b…` / `ffb5b09…`), the manifests / hashes, and the Phase
  4bn-AA split artefact; **and**
- the leakage / split-integrity proof and the Phase 4bn-L budget preflight are
  bound into the builder; **and**
- a **separate operator authorization** for data reads is granted
  (`source_admissible_for_data_read` is currently **false**).

The recommended code-only skeleton advances the second and third items **without**
performing any data read; it does not unblock data reads.

---

## 24. Remaining blockers before real dataset builder

A data-reading dataset builder remains blocked until:

- the recorded contract (Phase 4bn-AC — done); **and**
- this builder-readiness decision (this phase — code-only-first); **and**
- a **code-only skeleton** with synthetic validation exists and passes; **and**
- the leakage proof + budget preflight are designed into the builder; **and**
- a **separate operator authorization** for the builder is granted
  (`source_admissible_for_dataset_builder` is currently **false**).

---

## 25. Remaining blockers before ML training

ML training remains blocked until:

- all of §23 and §24; **and**
- the per-task target / horizon / filtering is locked by contract (Phase 4bn-AC
  selects `forward_direction_15s`, 15s, 3-class signed — done); **and**
- a committed **end-to-end pre-v002 trainer** exists (it does **not** today; the
  only committed ML-baseline stack is v002-terminal-bound and inadmissible to
  pre-v002); **and**
- a **separate operator authorization** for ML is granted (`ml_authorized` is
  currently **false**).

---

## 26. Candidate next phases considered

1. **Code-only ML dataset builder skeleton** (code + synthetic tests, no data
   read) — encode the Phase 4bn-AC contract as constants + validators + proof
   schema, validated against synthetic fixtures only. **Lowest risk that still
   makes real implementation progress; not blocked by admissibility.**
2. **ML dataset builder implementation** (data-reading) — read and process real
   Parquet. **Highest risk; requires data-read + builder authorization that does
   not exist; no skeleton / proof / synthetic validation precedes it.**
3. **Additional docs-only builder design memo** — possible, but the Phase 4bn-AC
   contract is already precise enough to encode in code; another pure-docs memo
   would delay safe progress without adding contract precision.
4. **Source-admissibility gate artefact** — a code-level admissibility gate; not
   required before the code-only skeleton (the skeleton touches no data), and
   necessary only before a data-reading builder.
5. **Full-envelope reference-assembly memo** — only relevant if a future path
   combines pre-v002 + v002; not required for the conservative pre-v002-only
   path.
6. **Holdout-boundary memo** — only relevant if a future scope touches the v002
   terminal or sealed-test dates; not required here.
7. **Remain paused / close the ML-baseline arc** — valid operator options, but
   the arc has a clear, low-risk next step, so closing is not recommended.

---

## 27. Selected next recommendation

**Recommend authorizing a code-only ML dataset builder skeleton with synthetic
tests only (assume Phase 4bn-AE), subject to separate operator authorization.**

After the contract (Phase 4bn-AC) and this readiness decision, the safest
implementation step is code-only with synthetic fixtures: it exercises contract
enforcement without reading data, writing outputs, mutating manifests, or
authorizing ML. It is not blocked by source admissibility, mirrors the safe
precedent of the Phase 4bn-AA pure split artefact, and leaves the data-reading
builder, dataset creation, budget preflight over real data, and training each as
later, separately-authorized phases. This memo does **not** recommend a
data-reading builder next; the committed evidence does not support it and
`source_admissible_for_data_read = false`.

No successor is authorized from inside Phase 4bn-AD.

---

## 28. Explicit non-authorizations

Phase 4bn-AD does **not**, and does not authorize anyone to: build a code-only or
data-reading ML dataset builder; read or create any local data; inspect any file
under `data/microstructure/` or `data/research/`; inspect any raw zip /
normalized / feature / label Parquet / manifest / gate report / sidecar; read the
v002 terminal window; touch the sealed v002 test split (`test_rows_loaded = 0`);
create a split file / research matrix / ML dataset / ML config / manifest /
sidecar / gate report; create the future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`; mutate any
manifest / sidecar / gate report / successor-state artefact; flip
`research_eligible`; transition `eligibility_gate_status` /
`chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`; invoke
or alter the Phase 4aw `flip_research_eligible(...)` always-raises invariant;
train / score / predict; run diagnostics / strategy / signals / PnL / backtests;
acquire data; call any public / authenticated / private endpoint; download any
archive / CHECKSUM; run a HEAD preflight; rerun any acquisition / raw /
normalization / feature / label execution or any layer gate; create a database /
`.duckdb` / `.sqlite`; compact Parquet; migrate storage; create v003; use
credentials / `.env` / `.mcp.json` / MCP / Graphify; open any WebSocket / user
stream; authorize Phase 5, paper / shadow, live-readiness, deployment,
exchange-write, production keys, or any successor phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side; round-trip = 16
bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0;
Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path + sidecar
policy; Phase 4bl-F risk tiers; Phase 4bm-U / 4bm-W v002 split policy; Phase
4bn-J-R1 raw-only cap amendment; Phase 4bn-L derived-stack storage budget; Phase
4bn-N normalization manifest/versioning; Phase 4bn-R feature manifest/versioning;
Phase 4bn-V label manifest/versioning; Phase 4bn-Y chronological split/holdout
policy; Phase 4bn-AA pre-v002 split-policy artefact; Phase 4bn-AB
source-admissibility posture; Phase 4bn-AC ML dataset contract) is preserved
verbatim. Phase 4 canonical remains unauthorized.

---

## 29. Result state

`ML_DATASET_BUILDER_READINESS_RECORDED__CODE_ONLY_SKELETON_RECOMMENDED__NO_DATA_READ__REMAIN_PAUSED`

The builder-readiness is recorded: the project is ready for a **code-only** ML
dataset builder skeleton with synthetic tests only; it is **not** ready for a
data-reading builder, dataset creation, research-matrix creation, or ML training.
No data reads are authorized; no dataset builder is authorized; no ML is
authorized. `source_admissible_for_dataset_contract` remains **true**;
`source_admissible_for_data_read` remains **false**;
`source_admissible_for_dataset_builder` remains **false**; `ml_authorized`
remains **false**; manifest state is unchanged.

---

## 30. Decision

`RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`

Rationale: after the contract and readiness memo, the safest implementation step
is code-only with synthetic fixtures. It exercises contract enforcement without
reading data, writing outputs, mutating manifests, or authorizing ML. A
data-reading builder must not be authorized yet — `source_admissible_for_data_read`
and `source_admissible_for_dataset_builder` are both `false`, and no skeleton /
proof / synthetic validation exists to precede it.

---

## 31. Recommended state and successor options

**Recommended state: remain paused. No next phase authorized by this memo.**

Operator options (each subject to separate authorization after the
branch-complete report):

- remain paused;
- request a merge prompt for Phase 4bn-AD;
- separately authorize a **code-only ML dataset builder skeleton** (preferred;
  assume Phase 4bn-AE);
- separately authorize an **additional builder design memo** (if preferred);
- separately authorize a **source-admissibility gate artefact** (if preferred to
  sequence admissibility before a later data-reading builder);
- separately authorize a **full-envelope reference-assembly memo** only if a
  future path combines pre-v002 + v002 data;
- separately authorize a **holdout-boundary memo** only if a future scope touches
  the v002 terminal or sealed-test dates;
- separately authorize a **source-policy documentation memo**;
- separately authorize a **process-doc `D:` path-string update**;
- reject further ML-baseline successors and **close the ML arc**.

No data-reading builder / ML / diagnostics / strategy / PnL / backtest / storage
migration / paper / shadow / live / exchange-write option is valid from this state
unless separately authorized after this branch is merged.

---

## 32. Current-project-state update summary

`docs/00-meta/current-project-state.md` is amended **additively only**: one new
Phase 4bn-AD paragraph appended after the Phase 4bn-AC paragraph, and one new
`Current phase:` block inserted ahead of the Phase 4bn-AC block. All prior content
(Phase 4bn-A … 4bn-AC paragraphs and blocks, every retained verdict, and every
project lock) is preserved verbatim. No manifest field, eligibility flag, or
split-policy field is set. The update records: builder-readiness recorded;
code-only skeleton recommended; data-reading builder not ready; dataset output /
research matrix / ML training not ready; v002-bound tooling precedent-only
boundary; recommended future modules
(`pre_v002_ml_dataset_contract.py`, `pre_v002_ml_dataset_builder.py`,
`pre_v002_ml_dataset_proof.py`) and test
(`test_phase4bn_ae_pre_v002_ml_dataset_builder_skeleton.py`); no-data-I/O and
fail-closed controls; remaining blockers before data reads / dataset builder / ML
training; result
`ML_DATASET_BUILDER_READINESS_RECORDED__CODE_ONLY_SKELETON_RECOMMENDED__NO_DATA_READ__REMAIN_PAUSED`;
decision
`RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
remain paused; no successor authorized.
