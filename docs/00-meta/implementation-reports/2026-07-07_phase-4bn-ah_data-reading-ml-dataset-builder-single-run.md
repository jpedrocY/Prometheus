# Phase 4bn-AH — Data-Reading ML Dataset Builder Implementation + Single Run

## 1. Branch

`phase-4bn-ah/data-reading-ml-dataset-builder-single-run`

## 2. Base SHA

`1f4c89b6649181dc7b82e34bcfa97f4b3b7c87f9`
(`docs(phase-4bn-ag): finalize merge closeout shas`; pre-branch `main ==
origin/main == HEAD` verified in sync).

Authorized by the operator as **Phase 4bn-AH** — the separate authorization Phase
4bn-AG required for (a) implementing the pre-v002 data-reading ML dataset builder
and (b) performing exactly one controlled local builder run.

## 3. Files created / modified

**Source (1, added):**

- `src/prometheus/research/microstructure/pre_v002_ml_dataset_run.py` — the
  data-reading builder. Imports and reuses the Phase 4bn-AF skeleton
  (`pre_v002_ml_dataset_contract`, `pre_v002_ml_dataset_builder`,
  `pre_v002_ml_dataset_proof`) and the Phase 4bn-AA split artefact
  (`pre_v002_split_policy`). It never wraps, copies, or reuses the v002-terminal
  loader `ml_baseline_dataset_v002`.

**Tests (1 added, 1 modified):**

- **Added:**
  `tests/research/microstructure/test_phase4bn_ah_pre_v002_ml_dataset_run.py` —
  26 offline tests (budget preflight, Phase 4bb-F sidecars, feature-list hash,
  boundary-crossing arithmetic, run-proof assembly + validation, reused skeleton
  fail-closed guards, namespace confinement, one-run guard).
- **Modified (2 tests, behavioural only):**
  `tests/research/microstructure/test_phase4bn_af_pre_v002_ml_dataset_builder_skeleton.py`
  — `test_imports_do_not_create_future_namespace` and
  `test_no_output_namespace_created` previously asserted the output namespace was
  *absolutely absent*. That assumption held only before any data-reading builder
  ran; Phase 4bn-AH is the authorized phase that creates it. Both tests now assert
  the real invariant they protect — the **skeleton's own surface never creates or
  removes the namespace** (existence unchanged across exercising the full skeleton
  surface) — which passes whether or not the Phase 4bn-AH dataset exists. No other
  skeleton test changed.

**Docs (2, added):**

- this implementation report;
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ah_closeout.md`.

**No existing source module was modified. No manifest, gate report, sidecar,
split file, research matrix, ML config, or data file under `data/microstructure/`
was created or modified. No committed data file was created.**

## 4. Exact implementation summary

`pre_v002_ml_dataset_run.py` is a **streaming, bounded-memory, fail-closed**
data-reading builder with these components:

- **Pre-read verification** (all before any feature/label row read):
  `verify_manifest_and_gate_hashes` (computes SHA256 of the 3 manifest files + 3
  gate-report files, reuses the skeleton `validate_manifest_hashes` for the
  config-hash / v002-rejection path); `verify_source_scope` (reuses the skeleton
  `validate_source_scope` over real manifest fields; normalizes the recorded
  `usdm_futures` market to the contract token `binance_usdm_futures` and
  recognizes the `by_reference` v002-terminal mode as safe); per-Parquet SHA256 +
  Phase 4bb-F sidecar + manifest-inventory verification for all 550 files
  (`verify_per_parquet_sidecars_and_inventory`); 275/275 partition discovery;
  `bind_split_authority` (confirms the split-policy name + arithmetic; records the
  module git commit SHA).
- **Streaming build** (`run` → `_process_partition`): one pass over all 275
  in-segment dates in chronological order; per partition it reads only the needed
  columns, verifies strict positional alignment vectorised over the 4 alignment
  keys + `utc_date`, assigns the split by date, drops embargo dates in full,
  applies vectorised target filtering (invalid → censored → null-direction →
  null-log-return precedence; **never imputes**) with drop accounting, and (for
  `train` partitions only) accumulates streaming per-feature sum / sum-of-squares
  / count / null-count to fit the **train-only** standardization statistics.
- **Real budget preflight** (`evaluate_budget_preflight` / `measure_d_free_gib` /
  `assert_budget_during`): measures `D:` free space (≥ 500 GiB before start;
  fail-closed < 350 GiB during); the Phase 4bn-L caps (75/125 GiB derived,
  250/300 GiB total-stack, 4/8 h runtime, 50/100 GiB temp) are carried verbatim
  and never approached because the artefact is compact.
- **Leakage / split-integrity proof** (`BuilderRunProof` +
  `validate_builder_run_proof`): the conservative-posture sections reuse the
  **existing** skeleton `validate_dataset_builder_proof` path; the real-IO fields
  (real budget preflight passed, `output_namespace_created=True`,
  `no_data_io=False`, per-horizon zero boundary crossings, `test_rows_loaded=0`)
  are validated by the extended run validator **before any write**.
- **Compact artefact writers** (`write_json_with_sidecar`): every artefact gets a
  Phase 4bb-F canonical two-space `.sha256` sidecar; writes occur only inside the
  authorized namespace, and only after the proof validates.
- **One-run guard**: `run` refuses to overwrite a completed build (a `dataset_manifest.json`
  present in the namespace fails closed with "rerun requires separate operator
  authorization").

**Design decision — compact dataset specification, not a re-materialised matrix.**
A full `400,001,695 × 45` float64 model matrix is `~144 GiB`, which would breach
the Phase 4bn-L `125 GiB` derived-footprint hard cap and merely duplicate the
already-gated feature Parquet. The builder therefore materialises a **compact
specification** — the train-only fitted transform statistics, a per-date split /
filter index, per-split / per-month row and class-distribution summaries, the
leakage proof, and a dataset manifest — total ~97 KB. This respects the budget
gate honestly (a full materialisation would fail it) and forbids the prohibited
"compacted Parquet" / "v003" outputs.

## 5. Exact run summary

The single controlled run completed successfully in **1152.6 s (~19.2 min)**,
streaming all **400,001,695** rows across 275 partitions.

- **Split raw rows:** train `304,816,127`; embargo `3,071,370`; validation
  `68,578,296`; holdout `23,535,902` (sum = 400,001,695).
- **Split filtered (kept) rows:** train `304,816,127`; validation `68,578,296`;
  holdout `23,535,860`.
- **Dropped rows by split and reason:** holdout `censored = 42` (all at the
  2024-11-30 segment terminal — exactly matching the label manifest's 15s
  `censored_per_horizon = 42`); every other split/reason = **0**;
  `invalid_price = 0` everywhere; **no targets imputed**.
- **Kept-row class distribution** (`forward_direction_15s`, `{-1, 0, +1}`):
  train `150,077,008 / 3,590,082 / 151,149,037`; validation
  `33,619,134 / 1,013,759 / 33,945,403`; holdout `11,532,338 / 228,247 /
  11,775,275`. The flat/zero class is a ~1% minority (consistent with the Phase
  4bn-AE v002 observation).
- **Per-horizon earlier-split boundary-crossing rows:** `0` for 1s / 5s / 15s /
  60s (the one-full-UTC-date embargo dominates the ≤ 60 s horizons; proven from
  the observed per-split max `source_transact_time_ms`).
- **`test_rows_loaded = 0`; `v002_terminal_window_read = false`;
  `sealed_test_split_touched = false`.**

**Two prior invocations fail-closed at pre-read** (before any feature/label row
was read, and before any output was written), each on a bug in this new builder
code: (1) the manifest records `market = 'usdm_futures'` while the contract token
is `'binance_usdm_futures'` — the market-token normalisation was missing; (2) the
manifest inventory paths are recorded relative to `data/` — the path resolver was
missing the `data/` prefix. Both were corrected and verified on the first
partition before the successful run. Neither invocation read any data, created the
namespace, or wrote any artefact, so re-invoking after fixing the code is not a
"rerun of a data build" — it is completing the builder implementation.

## 6. Output namespace path

`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` — created
**exactly once**, local and **gitignored** (`.gitignore:88`).

## 7. Data outputs are gitignored and not committed

`git check-ignore -v data/research/microstructure/ml_datasets/pre_v002_contract_v001/dataset_manifest.json`
→ `.gitignore:88`. `git status --short` shows **no** file under `data/` (only the
new source module, the new test, the modified skeleton test, and the transient
`.claude/scheduled_tasks.lock`). No data output is staged or committed.

Artefacts written (each with a Phase 4bb-F `.sha256` sidecar; all sidecars
verified against recomputed SHA256 and basename):

| Artefact | Size | SHA256 |
|---|---|---|
| `dataset_manifest.json` | 5,590 B | `36a13213aa52cd0312dabfaf2befaed129b8d91318a6b1b5314d5b9d4b0f659c` |
| `train_only_transform.json` | 8,753 B | `85f6ea359a169e5f170aa207ea04f0aac357aa100d29e0bf7db39f7ce2d28ee5` |
| `split_index.json` | 77,244 B | `d1681acd489dfb923bb0203b6f4e2875c2a3b8c80ff34d9177269010bf9f0e35` |
| `leakage_split_integrity_proof.json` | 5,311 B | `e36c9163704dc764c9165cd6205667fb79787369f55bfe5972c90d619783a4a8` |

## 8. Pre-read checks and outcomes

| Check | Outcome |
|---|---|
| Source-scope validation (BTCUSDT / binance_usdm_futures / aggTrades / 2024-03-01..2024-11-30 / 275 / 400,001,695) | **PASS** |
| Manifest SHA256 (normalized `0e96ae37…`, feature `4881eb87…`, label `69746c88…`) | **PASS** (full values matched) |
| Config hashes (feature `0726b41d…`, label `b3bd5d2b…`) | **PASS**; v002 `819cfa7a…` / `352bad41…` rejected by value + prefix |
| Gate-report SHA256 (normalized `3452fd9d…`, feature `db731d1b…`, label `ffb5b092…`) | **PASS** (full values matched) |
| Per-Parquet SHA256 + `.sha256` sidecar + manifest inventory (550 files) | **PASS** (all 275 feature + 275 label) |
| Partition discovery (275 feature / 275 label; paired by UTC date) | **PASS** |
| Split-authority binding (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; commit `e12e928e33aa84e530a85a1a58b04d6ac217b1fb`; arithmetic 214/1/45/1/14=275) | **PASS** |
| `test_rows_loaded == 0` on both manifests; v002 window mode `by_reference` (safe) | **PASS** |

Full hash values were bound from the committed manifests / gate reports (not
prefixes alone), per the authorization requirement.

## 9. Pre-write checks and outcomes

All pre-read checks (above); strict feature/label pairing by UTC date; strict
positional alignment over `row_index` / `agg_trade_id` / `feature_timestamp_ms` /
`source_transact_time_ms` + `utc_date` (400,001,695 rows checked, **0 mismatches**,
no join/reorder/fill/tolerance); split assignment by `source_transact_time_ms` UTC
date; embargo drop; per-horizon boundary-crossing exclusion (0 crossings); target
filtering with drop accounting (never impute); 45-column allowlist model matrix;
forbidden-column scan **empty**; train-only transform planning + fitting (train
split only); Phase 4bn-L budget preflight **passed**; leakage/split-integrity
proof assembled and **validated before any write**; no output outside the
authorized namespace. **All PASS.**

## 10. Budget preflight details and outcome

Real Phase 4bn-L preflight, run before any write, fail-closed on breach. Measured
`D:` free before start = **1166.24 GiB** (≥ 500 GiB floor). Live free space
re-checked during the run (fail-closed < 350 GiB); never breached. Caps recorded:
derived 75/125 GiB, total-stack 250/300 GiB, runtime 4/8 h, temp 50/100 GiB.
Compact artefact footprint ~97 KB — far below every cap. **Result: PASSED**
(recorded in the proof `budget_preflight` section: `is_placeholder=false`,
`ran_preflight=true`, `measured_disk=true`, `passed=true`, `breaches=[]`).

## 11. Split / leakage proof details and outcome

`leakage_split_integrity_proof.json` (SHA256 `e36c9163…`) records, and
`validate_builder_run_proof` confirmed: split-policy name / module path / commit
SHA; date counts 214/1/45/1/14; no missing / duplicate / multi-assigned in-segment
dates; no embargo rows used; zero out-of-segment dates; `v002_terminal_window_read=false`;
`sealed_test_split_touched=false`; `test_rows_loaded=0`; no random / shuffle /
k-fold / bootstrap; deterministic `source_transact_time_ms` UTC-date assignment;
per-horizon zero boundary-crossing rows; strict key-alignment count 400,001,695 /
0 mismatches; target drops by split and reason; 45-column feature-list hash
`8e705ba8…`; empty forbidden-column scan; train-only transform provenance;
budget-preflight result; the 21-metric registry; the aggregate/utc_month/utc_date
granularities; the dependence caveat; the calibration schema; the cost descriptive
fields; the success/kill constants; all 8 non-authorization flags `false`; output
namespace created exactly once; no outputs outside the namespace. **Result:
VALIDATED.**

## 12. Sidecar / metadata details

Every artefact carries a canonical Phase 4bb-F two-space `.sha256` sidecar
(`<sha256>␠␠<basename>\n`); the proof carries its own sidecar. All four sidecars
re-verified (recomputed SHA256 == recorded; basename matches). A local dataset
manifest (`dataset_manifest.json`) was written as explicitly defined by this
phase. All sidecars/metadata are local, gitignored, uncommitted, imply no
research eligibility, set no `chronological_split_policy`, and transition no
`ml_authorized` / `diagnostics_authorized`.

## 13. Row counts by split and by target/drop reason

See §5. Totals: 400,001,695 streamed = train 304,816,127 + embargo 3,071,370 +
validation 68,578,296 + holdout 23,535,902. Kept: train 304,816,127; validation
68,578,296; holdout 23,535,860. Dropped: holdout censored 42; all other cells 0.

## 14. Date/month block reporting schema status

**Present.** `dataset_manifest.json` records `decision_block_units =
[utc_date, utc_month]`, `metric_granularities = [aggregate, utc_month, utc_date]`,
`month_block_split_rows` (9 UTC months, 2024-03..2024-11, train months Mar–Sep),
`row_level_metrics_descriptive_only = true`, the dependence caveat, and
`decimation_stride = null` / `decimation_policy = reserved_not_adopted`.
`split_index.json` records per-date split label + raw/filtered counts + drop
accounting for all 275 dates. **No metric, model, or score was computed** — only
descriptive row/class counts required to prove the builder worked.

## 15. Explicit `v002_terminal_window_read = false` confirmation

Confirmed. The builder read only the pre-v002 (2024-03-01..2024-11-30) normalized-
lineage / feature / label sources bound by the Phase 4bn-AC contract. The split
artefact hard-raises for any out-of-segment date, and the manifest v002 mode is
`by_reference` (referenced, not read). Recorded `v002_terminal_window_read=false`.

## 16. Explicit `sealed_test_split_touched = false` confirmation

Confirmed. `sealed_test_split_touched=false` in the proof; the sealed test
(2025-02-14..2025-02-28) is entirely outside the pre-v002 segment and was never
read.

## 17. Explicit `test_rows_loaded = 0` confirmation

Confirmed. `test_rows_loaded=0` in the proof and the dataset manifest.

## 18. Explicit no ML / model / scoring / prediction / diagnostics / strategy / PnL / backtest confirmation

Confirmed. No model was trained; nothing was scored; no prediction was generated;
no diagnostics were run; no strategy / signal / PnL / backtest was computed. The
builder assembled a leakage-proof dataset specification only. All 8
non-authorization flags are `false`.

## 19. Exact validation commands and results

- `pytest …test_phase4bn_ah… …test_phase4bn_af…` → **123 passed** (26 new AH + 97
  AF skeleton).
- `ruff check` (new module + both test files) → **All checks passed**.
- `mypy src/…/pre_v002_ml_dataset_run.py` → **0 direct errors in the new module**;
  2 pre-existing unrelated sibling errors surface transitively
  (`labels_manifest_v002.py:370`, `multiday_feature_gate_checks.py:847`), both
  reproduced by `mypy` on the committed skeleton builder module and unmodified by
  this phase.
- `git diff --check` → clean.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`;
  `git check-ignore -v …/pre_v002_contract_v001/dataset_manifest.json` →
  `.gitignore:88`.
- Budget preflight → **PASSED** (D: 1166.24 GiB free).
- Proof validator (`validate_builder_run_proof`) → **VALIDATED** (run-time, before
  write) and re-verified against the on-disk proof.
- No-sealed / no-v002 proof → `test_rows_loaded=0`, `v002_terminal_window_read=false`,
  `sealed_test_split_touched=false`.
- No-output-outside-namespace → only the 4 artefacts + 4 sidecars exist in the
  namespace; `git status` shows no `data/` file.
- One-run guard → a second `run()` invocation fails closed
  ("rerun requires separate operator authorization").

## 20. Git status

`git status --short`:

```text
 M tests/research/microstructure/test_phase4bn_af_pre_v002_ml_dataset_builder_skeleton.py
?? .claude/scheduled_tasks.lock
?? src/prometheus/research/microstructure/pre_v002_ml_dataset_run.py
?? tests/research/microstructure/test_phase4bn_ah_pre_v002_ml_dataset_run.py
```

No `data/microstructure/` or `data/research/` file appears (all gitignored). The
transient `.claude/scheduled_tasks.lock` is not committed.

## 21. Whether any rerun occurred

**No rerun of a data build occurred.** The successful run was executed once. The
two prior invocations fail-closed at **pre-read** (before any data read, before
any write) on builder-code bugs (market normalisation; inventory path resolution),
read no data, and created no namespace/artefact; correcting the code and
re-invoking is completing the implementation, not rerunning a build. After the
successful build, the one-run guard now refuses any further invocation.

## 22. Remaining blockers before Phase 4bn-AI diagnostics

- separate diagnostics authorization (`diagnostics_authorized = false`);
- a pre-declared **descriptive-only** diagnostics scope (class balance,
  label-overlap / effective-sample statistics, `forward_log_return_15s`
  distribution vs the 16 bps lock, per-month regime slices) that **trains no
  model, scores nothing, and generates no predictions**;
- Phase 4bn-AI is **not** authorized by this phase.

## 23. Remaining blockers before ML training

- all diagnostics blockers; a committed **end-to-end pre-v002 trainer** (does not
  exist); separate ML authorization (`ml_authorized = false`); the pre-registered
  Phase 4bn-AE success/kill evaluation applied by a separately-authorized baseline
  run (Phase 4bn-AJ). ML training is **not** authorized by this phase.

## 24. Remaining blockers before any strategy / PnL / backtest / liveness path

**Absolute boundary.** No dataset, diagnostic, baseline, or metric authorizes
strategy / signals / threshold or confidence-gated trading / backtest / PnL /
position sizing / execution / live-readiness / paper / shadow / exchange-write.
Any such path requires a separate future **M0-style mechanism-admissibility memo**
(Phase 4ak M0) clearing cost realism at 8 bps/side · 16 bps round-trip, execution
feasibility, slippage / spread assumptions (aggTrades-only data cannot currently
support these — mid-price / book data would be required), label economic relevance
(the 15s strict-sign target is explicitly non-economic), strategy admissibility
vs the retained rejections and the M0 §7.D microstructure-lane `NOT_RECOMMENDED_NOW`
posture, and the Phase 4al no-rescue constraints.

## 25. Recommended next state

**Remain paused. No successor authorized.** Phase 4bn-AH is branch-complete
(implementation + single run done; leakage-proof dataset specification built
locally and gitignored). The pre-registered arc's next step would be **Phase
4bn-AI** (descriptive dataset diagnostics, no models), which is **not** authorized
and requires a separate operator authorization. The operator may also request a
merge prompt for Phase 4bn-AH, or close the ML arc.

## 26. Explicit non-authorizations

Phase 4bn-AH does not, and does not authorize anyone to: run the builder again
(one-run guard active; rerun requires separate authorization); read the v002
terminal window; touch the sealed test; train / score / predict; run diagnostics /
strategy / signals / PnL / backtests; create a research matrix beyond this dataset
specification, a model, a v003, compacted Parquet, a database, or any output
outside the authorized namespace; commit any data file; acquire data / call
endpoints / download archives; flip `research_eligible`; transition
`eligibility_gate_status` / `chronological_split_policy` / `diagnostics_authorized`
/ `ml_authorized` / `source_admissible_for_data_read` /
`source_admissible_for_dataset_builder`; mutate any published manifest / gate
report / sidecar; use credentials / `.env` / `.mcp.json` / MCP / Graphify; or
authorize any successor. Every retained verdict and project lock is preserved
verbatim; the Phase 4aw `flip_research_eligible(...)` always-raises invariant was
never invoked.
