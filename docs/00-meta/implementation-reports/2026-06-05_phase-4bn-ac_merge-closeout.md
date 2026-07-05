# Phase 4bn-AC — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-AC — ML Dataset Contract Memo.
- **Phase type:** docs-only / ML dataset contract / pre-v002 source-binding /
  target-feature-filtering / leakage-proof / budget-preflight / no-data-read
  memo.
- **Action:** merge into `main`.
- **Merge purpose:** bring the branch-complete Phase 4bn-AC work (the ML dataset
  contract memo, the closeout, and the narrow additive `current-project-state.md`
  update) onto `main`.
- **Source branch:** `phase-4bn-ac/ml-dataset-contract-memo`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (it defines the
  binding contract any future pre-v002 ML dataset builder must obey — targets,
  admissible features, excluded columns, filtering, split binding, manifest /
  hash / gate-report binding, leakage-proof obligations, budget-preflight
  obligations, output namespace, non-authorization boundaries — where an error
  could cause downstream leakage, misaligned labels/features, accidental data
  reads, or invalid ML claims, even though the memo performs no data I/O).

---

## 2. SHAs

- **Pre-merge `main` / base SHA:** `46bcdd3862c2b82b268d668f1e2d0180243f0dce`
  (`docs(phase-4bn-ab): finalize merge closeout shas`).
- **Branch / docs commit SHA:** `c9c6c7eb349a8323e499c484d7028848ba74b49d`
  (`docs(phase-4bn-ac): record ml dataset contract`).
- **Merge commit SHA:** `454310357be778bf920bf339d952a3983789d0a8`
  (`docs(phase-4bn-ac): merge ml dataset contract`).
- **Merge-closeout commit SHA:** `1d032a4`-style follow-up
  (`docs(phase-4bn-ac): add merge closeout`) — its exact SHA is recorded by the
  SHA-finalization update below and in the final operator report.
- **SHA-finalization commit SHA:** this update
  (`docs(phase-4bn-ac): finalize merge closeout shas`) — its exact SHA is the
  resulting `main` / `origin/main` tip, reproduced in the final operator report
  and `git log`.
- **Final `main` / `origin/main` SHA after push:** equal to the SHA-finalization
  commit SHA above; reproduced in the final operator report and `git log`.

---

## 3. Merge method

`git checkout main` → `git pull --ff-only origin main` (already up to date at
`46bcdd3`) → `git merge --no-ff phase-4bn-ac/ml-dataset-contract-memo -m
"docs(phase-4bn-ac): merge ml dataset contract"`. Merge made by the `ort`
strategy; no conflicts. No `--no-verify`; no `--no-gpg-sign`; no
`-c commit.gpgsign=false`; no force-push. Push status recorded in the final
operator report.

---

## 4. Files brought forward by the merge

**Docs (3):**

- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ac_ml-dataset-contract-memo.md`
  (32 sections; 856 insertions).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ac_closeout.md`
  (275 insertions).
- **Modified (additive only):** `docs/00-meta/current-project-state.md`
  (208 insertions, 0 deletions; new Phase 4bn-AC paragraph + new `Current phase:`
  block; all prior content preserved verbatim).

**Source:** none. **Tests:** none. **Scripts:** none. **Config:** none.

**No** existing source or test was modified; no scripts, config, `.gitignore`,
`pyproject.toml`, README, MCP file, manifest, sidecar, gate report,
successor-state artefact, split file, research matrix, ML config, model output,
prediction output, or data file was added or modified. **No `data/microstructure/`
or `data/research/` file was modified.** No prior governance memo was modified
beyond the narrow additive `current-project-state.md` paragraph.

---

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 208 +++++
 .../2026-06-05_phase-4bn-ac_closeout.md            | 275 +++++++
 ...-06-05_phase-4bn-ac_ml-dataset-contract-memo.md | 856 +++++++++++++++++++++
 3 files changed, 1339 insertions(+)
```

1339 insertions, 0 deletions. The diff matches the expected change set from the
authorization prompt exactly (add memo, add closeout, modify
`current-project-state.md`).

---

## 6. Result / verdict

**CONTRACT RECORDED — ML DATASET CONTRACT RECORDED — MERGE COMPLETE.** Phase
4bn-AC is a docs-only ML dataset contract / pre-v002 source-binding /
target-feature-filtering / leakage-proof / budget-preflight / no-data-read memo.
It recorded, by reference only, the binding contract any future pre-v002 ML
dataset builder must obey. It created no dataset, no dataset config, no manifest,
no gate report, no sidecar, no split file, no research matrix, no model output,
no prediction output, and no data file; it read no local data; it created no
local data; it added no code, tests, or scripts; it mutated no manifest; it set
no `chronological_split_policy`; it flipped no `research_eligible`; it
transitioned no `eligibility_gate_status`; it invoked no Phase 4aw eligibility
function; it authorized no successor. With this merge, Phase 4bn-AC is
**merge-complete on `main`**.

- **Result state:**
  `ML_DATASET_CONTRACT_RECORDED__PRE_V002_CONTRACT_ONLY__NO_DATA_READ__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_ML_DATASET_BUILDER_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the project convention, project completion also requires the
SHA-finalization commit (`docs(phase-4bn-ac): finalize merge closeout shas`) that
fills the exact post-merge SHAs in §2; that commit is recorded below and in the
final operator report.

---

## 7. Dataset contract verdict

The pre-v002 normalized / feature / label stack is **source-admissible for a
docs-only ML dataset contract only**. The contract is recorded by reference. The
stack is **not** admissible for actual data reads, **not** admissible for
dataset-builder implementation, and **not** admissible for ML. Carried-forward
admissibility posture (Phase 4bn-AB, unchanged): `layer_integrity_passed=true`;
`source_admissible_for_dataset_contract=true`;
`source_admissible_for_data_read=false`;
`source_admissible_for_dataset_builder=false`; `ml_authorized=false`;
`diagnostics_authorized=false`; `strategy_backtest_authorized=false`;
`manifest_research_eligible=false`; `manifest_eligibility_gate_status=pending`;
`manifest_chronological_split_policy=not set`.

---

## 8. Contract name

`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001` — a docs-level
contract name only. No dataset was created; no config was created; no manifest
was created; no field was set.

---

## 9. Permitted source scope

- BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only.
- Pre-v002 only: 2024-03-01 through 2024-11-30 inclusive UTC; 275 dates;
  400,001,695 rows by reference.
- **Feature source (by reference only):** Phase 4bn-S; manifest SHA256
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`;
  `feature_config_hash`
  `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`; feature
  gate `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`
  (27/27 PASS).
- **Label source (by reference only):** Phase 4bn-W; manifest SHA256
  `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`;
  `label_config_hash`
  `b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`; label gate
  `ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984`
  (40/40 PASS).
- **Normalized lineage (by reference only):** Phase 4bn-O; manifest SHA256
  `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`; normalized
  gate `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`
  (25/25 PASS).

---

## 10. Forbidden source scope

v002 terminal 2024-12-01..2025-02-28; sealed test 2025-02-14..2025-02-28;
full-envelope pre-v002 + v002 combined assembly; non-BTCUSDT symbols; spot /
mark-price / index-price / order-book / kline / liquidation / funding /
open-interest / cross-venue data; newly acquired data; raw zip direct read; any
raw / normalized / feature / label family not already carried by the pre-v002
chain (incl. published `feature_config_hash 819cfa7a…` /
`label_config_hash 352bad41…`); `data/research` prior experiment outputs;
external sources; private / authenticated API endpoint data; WebSocket / user
stream data. All fail-closed.

---

## 11. Manifest / hash / gate-report binding

A future builder must: hash-verify every Parquet against its `.sha256` sidecar
and the manifest inventory before row-level processing; verify the pre-v002
`feature_config_hash` is exactly `0726b41d…` and the pre-v002 `label_config_hash`
is exactly `b3bd5d2b…`; bind to the normalized / feature / label gates
(`3452fd9d…` / `db731d1b…` / `ffb5b09…`); reject the v002-terminal-bound committed
stack (`ml_baseline_design_v002.py` / `ml_baseline_dataset_v002.py` /
`diagnostics_split_policy_v002.py`; 90 partitions / 155,153,449 rows / `819cfa7a…`
/ `352bad41…`) and its 90-day identity; fail closed on any manifest / sidecar /
hash / gate-report / partition-count / config-hash mismatch.

---

## 12. Split-policy binding

Import and use `src/prometheus/research/microstructure/pre_v002_split_policy.py`
(`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`): train
2024-03-01..2024-09-30 (214) / embargo 2024-10-01 / validation
2024-10-02..2024-11-15 (45) / embargo 2024-11-16 / internal holdout (dry-run,
NOT sealed test) 2024-11-17..2024-11-30 (14) = 275; assignment by
`source_transact_time_ms` UTC date via `split_for_timestamp_ms` /
`split_for_date`; drop embargo dates/rows; apply per-horizon earlier-split
boundary protection; hard-raise on out-of-segment / v002-terminal / sealed-test
dates; no random split; no shuffle; no k-fold-over-time; no bootstrap; no
post-hoc temporal resampling.

---

## 13. Target / horizon choice

Family `microstructure_labels_aggtrades_v001 @ v002` (`label_schema_version
v001`). Contract-known horizons 1s / 5s / 15s / 60s. Primary first-baseline
target `forward_direction_15s` — locked 3-class signed `{-1, 0, +1}`, zero class
preserved; threshold is the strict sign of `forward_log_return_15s` (no deadband,
no bp threshold, no cost-based threshold, no threshold optimization). Secondary
descriptive target (not a model target) `forward_log_return_15s` for reporting /
cost-context only. Multi-horizon use deferred. **15s chosen over 60s** on
committed terminal-censor evidence (1s=3 / 5s=20 / 15s=42 / 60s=216; 60s drops
~5× more terminal rows) and reduced ultra-micro tie/noise structure vs 1s/5s — a
contract choice, not a performance claim. Forbidden target actions: no training;
no target experimentation; no multi-horizon model selection; no regression-only
reframing; no binary collapse; no ordinal / meta-labeling; no barrier / stop /
MFE / MAE / R-multiple / PnL labels.

---

## 14. Target filtering policy

Drop null `forward_direction_15s`; drop null `forward_log_return_15s` where
required; drop `horizon_censored_flag_15s = true`; reject
`label_invalid_price_flag = true` (pre-v002 has 0 such rows by reference); never
impute targets; censored / invalid rows must never enter train / validation /
holdout; internal holdout is dry-run only (no model selection, hyperparameter
tuning, threshold tuning, feature selection, final / strategy / production
claims); sealed test remains `test_rows_loaded = 0`; future builder must record
dropped-row counts by split and reason.

---

## 15. Feature allowlist

Exactly the 45 causal computed `FEATURE_SCHEMA_V002` columns: 40 windowed (10
per-window templates — `rolling_aggtrade_count`, `rolling_quantity_sum`,
`rolling_quantity_mean`, `rolling_aggressive_buy_quantity`,
`rolling_aggressive_sell_quantity`, `rolling_aggressive_buy_count`,
`rolling_aggressive_sell_count`, `rolling_aggressive_flow_ratio`,
`rolling_aggressive_quantity_imbalance`, `rolling_log_return_past_window` — over
1s/5s/15s/60s), 3 time-context (`utc_hour`, `utc_minute`,
`milliseconds_since_day_start`), 2 data-quality flags (`invalid_window_flag`,
`rolling_missing_window_flag`). No additions; no feature selection / ranking /
pruning; no PCA / embeddings / learned representations; no raw prices unless a
future contract revision explicitly authorizes them.

---

## 16. Forbidden model-matrix policy

Exclude the 17 lineage columns; exclude all label columns, all support columns,
all split columns, all censor columns; exclude raw prices unless a future
revision authorizes; exclude any future-looking / post-label / strategy / PnL
column. Forbidden substrings: `forward_log_return`, `forward_direction`,
`horizon_censored_flag`, `label_`, `split_`, `censored_`. A future builder must
run a forbidden-column substring scan and fail closed on any hit.

---

## 17. Feature / label alignment policy

Strict per-day positional alignment with identical-key verification: `row_index`,
`agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`, and
`symbol` / `utc_date` where present. No join-based repair; no reordering; no
forward-fill; no back-fill; no tolerance merge; no duplicate-key heuristic; any
key mismatch fails closed.

---

## 18. Split / filtering execution order

1. Discover expected 275 feature partitions and 275 label partitions from
   manifest references.
2. Verify manifest / config / gate-report hashes before row-level processing.
3. Pair feature and label partitions by UTC date.
4. Verify positional alignment keys within each paired partition.
5. Assign split using `source_transact_time_ms` UTC date and the Phase 4bn-AA
   split artefact.
6. Drop embargo dates/rows and apply active-horizon earlier-split boundary
   protection.
7. Filter censored / null / invalid active-horizon targets.
8. Build the model matrix from the 45 allowed feature columns only.
9. Run the forbidden-column scan.
10. Fit transforms only on the train split.
11. Apply train-fitted transforms to validation and internal holdout.
12. Emit proof / sidecar metadata.
13. Write outputs only to the local gitignored output namespace if separately
    authorized.

---

## 19. Train-only transform policy

Fit standardization and imputation statistics on the train split only.
Standardization: subtract train mean; divide by `max(train std, 1e-8)`.
Fixed-zero imputation allowed for null numeric features only, because it is the
locked v002 fit-free design. Boolean quality flags are not standardized (pass
through as `{0, 1}`). Never fit on validation; never fit on holdout; never fit on
sealed test; never use validation / holdout / test for feature selection.
Transform metadata must record train-only provenance.

---

## 20. Leakage / split-integrity proof obligations

A future builder must emit a machine-checkable proof with a Phase 4bb-F sidecar
containing: exact policy name; split-policy module path and commit SHA; date
assignment counts 214 / 1 / 45 / 1 / 14; no missing in-segment dates; no
duplicate in-segment dates; no date assigned to more than one split; no embargo
date used for train / validation / holdout; zero out-of-segment dates;
`v002_terminal_window_read=false`; `sealed_test_split_touched=false`;
`test_rows_loaded=0`; no random / shuffle / k-fold / bootstrap; deterministic
assignment by `source_transact_time_ms` UTC date; for each active horizon, zero
earlier-split boundary-crossing rows under the Phase 4bn-AA helper; strict
feature/label key-alignment counts; target null / censor / invalid rows dropped
by split; active feature-column list hash; forbidden-column scan results (empty);
train-only transform provenance; budget-preflight result; non-authorization flags
all false for ML / diagnostics / strategy / PnL / backtest / live /
exchange-write.

---

## 21. Budget-preflight obligations

A future dataset-building phase must run the Phase 4bn-L budget preflight before
any write and fail closed if any limit is exceeded: derived footprint warn 75
GiB / hard 125 GiB; total derived-stack warn 250 GiB / hard 300 GiB; runtime
warn 4 h / hard 8 h; temp warn 50 GiB / hard 100 GiB; `D:` free space ≥ 500 GiB
before start; fail closed below 350 GiB during. No builder may write any output
without recording the budget-preflight result.

---

## 22. Output namespace and sidecar posture

Future outputs, if separately authorized, must be local and gitignored only under
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`. This
namespace was **not** created by Phase 4bn-AC and was **not** created during the
merge; it must not be committed. Each future artefact must carry a Phase 4bb-F
canonical sidecar. Future outputs must not imply research eligibility, must not
set `chronological_split_policy` in source manifests, and must not transition
`ml_authorized` or `diagnostics_authorized`.

---

## 23. Future builder validation requirements

A future builder must include offline tests for: manifest / hash / gate binding;
275 partition count; date range 2024-03-01..2024-11-30; v002 / sealed exclusion;
split assignment via `pre_v002_split_policy.py`; embargo date dropping; horizon
validation; target censor / null / invalid filtering; 45-column feature
allowlist; forbidden substring scan; no raw prices unless explicitly authorized;
strict positional alignment; train-only transforms; output namespace under
`data/research` only; sidecar metadata; no data output committed; no eligibility
transition; no ML / training / diagnostics / strategy. A future builder phase
must separately decide code-only-with-synthetic-tests-first vs
implement-and-run-on-real-data; this contract recommends a readiness or code-only
skeleton phase first.

---

## 24. Remaining blockers

**Before data reads:** dataset contract recorded (Phase 4bn-AC); code-level
dataset builder implemented and bound to passed gates / manifests / hashes /
split artefact; leakage / split-integrity proof; Phase 4bn-L budget preflight;
separate data-read authorization. Current `source_admissible_for_data_read =
false`.

**Before dataset builder:** recorded contract; builder-readiness decision
(code-only-first vs data-reading); leakage proof and budget preflight designed
into the builder; separate builder authorization. Current
`source_admissible_for_dataset_builder = false`.

**Before ML training:** all data-read and dataset-builder blockers;
target / horizon / filtering decision locked by contract (`forward_direction_15s`);
committed end-to-end pre-v002 trainer (does not exist); separate ML
authorization. Current `ml_authorized = false`.

---

## 25. Selected next recommendation

`RECOMMEND_AUTHORIZE_ML_DATASET_BUILDER_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— a docs-only ML dataset builder readiness memo (decide code-only-first vs
data-reading). **Alternative noted:**
`RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
Do not jump directly to a data-reading builder.

---

## 26. Local gitignored outputs (if any)

**None.** This phase created no `data/microstructure/` or `data/research/` output
and read none. `git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. The sole untracked entry
is the expected transient `.claude/scheduled_tasks.lock` (not committed). No
`data/microstructure` or `data/research` artefact was staged or committed. The
future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` was **not**
created.

---

## 27. Validation results

- `git diff --check` → clean (no whitespace / conflict markers), pre- and
  post-merge.
- `git diff --name-status main..phase-4bn-ac/ml-dataset-contract-memo`
  (pre-merge) → `M current-project-state.md`, `A …_closeout.md`,
  `A …_ml-dataset-contract-memo.md`.
- `git diff --stat` (merge) → 3 files, 1339 insertions, 0 deletions.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` (post-merge) → only `?? .claude/scheduled_tasks.lock`.
- No repo-standard markdown lint tooling exists, so none was run; ruff / mypy /
  pytest omitted because Phase 4bn-AC is docs-only with no code surface.
- No acquisition / raw / normalization / feature / label / gate / ML /
  diagnostics / backtest / strategy script was run; no endpoint called; no
  archive downloaded; no HEAD preflight; no local data read or created.

---

## 28. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bn-AC reads and mutates
no manifest, sidecar, gate report, successor-state, or published dataset. The
published `__v002` raw / normalized / feature / label families and the local
gated pre-v002 normalized (4bn-O) / feature (4bn-S) / label (4bn-W) segments and
their gate reports (4bn-P / 4bn-T / 4bn-X) remain byte-for-byte immutable and
unread.

---

## 29. Manifest state preservation (if applicable)

No manifest in scope was created, read, or mutated. Byte-identically before and
after this phase, at every pre-v002 layer (normalized `0e96ae37…`, feature
`4881eb87…`, label `69746c88…`):

- `research_eligible` — **false** (not flipped).
- `eligibility_gate_status` — **pending** (not transitioned).
- `chronological_split_policy` — **not set / not transitioned** in any manifest.
- `diagnostics_authorized` / `ml_authorized` — **false** (not transitioned).
- `no_successor_authorization` — **true** (preserved).
- Governance label state — **unchanged**.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant preserved (never invoked).

---

## 30. Boundary confirmations

- No local data read; no local data created.
- No split file, research matrix, ML dataset, ML config, manifest, gate report,
  sidecar, successor-state artefact, model, score, or prediction created.
- No existing source / test / script / config / `.gitignore` / `pyproject.toml`
  / README / MCP file modified; no new code, tests, scripts, or data files added.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar under `data/microstructure/` read or inspected.
- No v002 terminal window read; no sealed-test read or touch
  (`test_rows_loaded = 0`).
- No ML trained; no ML dataset created; no research matrix created; no model
  scored; no prediction generated; no diagnostics run; no strategy / signals /
  PnL / backtests.
- No acquisition, endpoint call, archive download, or HEAD preflight; no
  acquisition / raw / normalization / feature / label execution or layer-gate
  re-run.
- No storage migration; no database; no Parquet compaction; no v003.
- No `research_eligible` flipped on any actual manifest; no
  `eligibility_gate_status` transitioned; no `chronological_split_policy` changed.
- No `data/microstructure` or `data/research` artefact staged or committed; the
  future output namespace was not created.
- `.claude/scheduled_tasks.lock` remains untracked and uncommitted.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- No retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

---

## 31. Retained verdict ledger

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

## 32. Preserved project locks

All preserved verbatim: §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 =
0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8;
Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
cooled-down families list + memo template; Phase 4al refined no-rescue rule +
§13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path + sidecar
policy; Phase 4bl-F risk tiers; Phase 4bm-U / 4bm-W v002 split policy;
Phase 4bn-J-R1 raw-only cap amendment; Phase 4bn-L derived-stack storage budget;
Phase 4bn-N normalization manifest/versioning; Phase 4bn-R feature
manifest/versioning; Phase 4bn-V label manifest/versioning; Phase 4bn-Y
chronological split/holdout policy; Phase 4bn-Z ML-baseline readiness memo;
Phase 4bn-AA pre-v002 split-policy artefact; Phase 4bn-AB source-admissibility
posture. All prior phase results preserved verbatim.

---

## 33. No-rescue constraints

The Phase 4bn-AC merge does not, and cannot, be construed as authorising:

- an ML dataset builder readiness memo; a code-only ML dataset builder skeleton;
  a source-admissibility gate artefact; a data-reading ML dataset builder; a
  research matrix;
- ML model training, model selection, scoring, predictions, strategy hypothesis
  generation, or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state, entry / exit
  rules, backtest design, PnL, or diagnostics;
- any actual data read of the pre-v002 normalized / feature / label segments;
- reading the v002 terminal window or touching the sealed test
  (`test_rows_loaded = 0` preserved);
- full-envelope assembly or a holdout-boundary memo for the conservative
  pre-v002-only path;
- creating the future output namespace
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- storage migration / database creation / Parquet compaction / v003;
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`,
  or `chronological_split_policy` from this memo alone.

---

## 34. Successor authorization

**None.** No successor is authorized by this merge. A docs-only **ML dataset
builder readiness memo** is *recommended* as the next step but requires separate
operator authorization.

Candidate successors explicitly **NOT** authorized:

- an ML dataset builder readiness memo (recommended; not authorized)
- a code-only ML dataset builder skeleton
- a source-admissibility gate artefact
- a data-reading ML dataset builder
- a research matrix
- a full-envelope reference-assembly memo
- a holdout-boundary memo
- a source-policy documentation memo
- a process-doc `D:` path-string update
- ML implementation / model scoring / predictions / diagnostics
- strategy / signals / PnL / backtest implementation
- additional aggTrades / 5m / 1m / tick / mark-price / order-book acquisition
- Phase 5; Phase 4 canonical
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials

---

## 35. Recommended state

**Remain paused.** No next phase authorized.

**Conditional next, NOT authorized:** an ML dataset builder readiness memo
(docs-only) is the cleanest non-paused option — it would decide whether the
builder should be code-only first or whether a data-reading builder may be
authorized later, reading no data. It is **not** authorized by this merge.

**Next operator options:** remain paused; separately authorize an ML dataset
builder readiness memo; separately authorize a code-only ML dataset builder
skeleton; separately authorize a source-admissibility gate artefact if preferred;
separately authorize a full-envelope reference-assembly memo only if a future
path combines pre-v002 + v002 data; separately authorize a holdout-boundary memo
only if a future scope touches the v002 terminal or sealed-test dates; separately
authorize a source-policy documentation memo; separately authorize a process-doc
`D:` path-string update; or reject further ML-baseline successors and close the
ML arc. No ML / diagnostics / strategy / PnL / backtest / storage-migration /
paper / shadow / live / exchange-write option is valid from this state unless
separately authorized after this merge.

Final `git status` / `git log` / SHAs are reproduced in the final operator report
so the operator need not run a separate status/SHA check manually.
