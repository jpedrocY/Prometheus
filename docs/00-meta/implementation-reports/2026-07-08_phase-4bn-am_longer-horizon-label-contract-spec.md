# Phase 4bn-AM — Longer-Horizon Label Contract / Spec Memo

## 1. Branch

`phase-4bn-am/longer-horizon-label-contract-spec`

## 2. Base SHA

`4b96b671df485fffbe1f369baebcb8ecfdb4fe5e`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AL merge
closeout. Verified in sync before branching.)

## 3. Phase type and strict scope

Docs-only **longer-horizon label contract / specification memo** — the memo
recommended by Phase 4bn-AL (`RECOMMEND_LONGER_HORIZON_LABEL_CONTRACT_MEMO_NEXT`),
authorized by a separate operator prompt for Phase 4bn-AM only. It defines a
prospective longer-horizon (5m / 30m / 1h) label layer **at the design /
specification level**: it pre-registers the prospective label family, horizons,
columns, direction-threshold policy, continuous-return / cost-realism summary
requirements, leakage / split / censoring invariants, storage / budget posture,
validation / proof-artefact requirements, interpretation scope, and claim-scope
boundaries, and records a build recommendation.

It **builds nothing**, generates **no label / data file**, creates **no label /
dataset / output namespace**, reads **no data**, trains / scores / predicts
**nothing**, reruns **no** builder / diagnostics / baseline, changes **no** source /
test / manifest / gate / sidecar / split / ML config, and authorizes **no** successor
execution phase. It **does not claim** longer horizons are tradable; it only defines a
future contract and interpretation framework precise enough that a later, separately
authorized build prompt could be bounded safely.

## 4. Files created / modified

Created (committed):

- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-am_longer-horizon-label-contract-spec.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-am_closeout.md`.

No source module, test, script, manifest, gate report, sidecar, split file, ML
config, research matrix, or `data/` artefact was created or modified. No label /
dataset / output namespace was created or mutated. `current-project-state.md` is
**unchanged** (see §32/§34).

## 5. Exact documents / source inspected

Read-only (committed docs + committed source only; README treated as potentially
stale and **not** used as current-state authority):

- `docs/00-meta/current-project-state.md` (head + tail; navigational summary only —
  its tracked tail stops at Phase 3k / 2026-04-29 and does not track the 4bn ML arc).
- Phase 4bn-AE preregistration memo
  (`2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`) — via
  the frozen contract constants and the AK/AL recoveries.
- Phase 4bn-AH report + closeout + merge-closeout (data-reading builder + single run;
  leakage proof).
- Phase 4bn-AI report + closeout + merge-closeout (descriptive diagnostics, no
  models).
- Phase 4bn-AJ report + closeout + merge-closeout (fixed baseline run + verdict).
- Phase 4bn-AK report + closeout + merge-closeout (arc-decision memo).
- Phase 4bn-AL report + closeout + merge-closeout (longer-horizon label memo — the
  recommendation this phase implements at the spec level).
- Process standards under `docs/00-meta/process/`
  (phase-workflow-standard, merge-closeout-standard, phase-risk-tiering-standard,
  operator-report-standard, phase-prompt-template) — for method only.
- Committed source constants (read for constant confirmation only; **none
  modified**):
  `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py`
  (`PRIMARY_TARGET`, `PRIMARY_HORIZON_MS = 15000`, `TARGET_CLASSES = (-1,0,1)`,
  `LOCKED_COST_BPS_PER_SIDE = 8.0`, `LOCKED_ROUND_TRIP_COST_BPS = 16.0`,
  `CONTINUE_FOLLOWUP_CATEGORIES`, `CLAIM_SCOPE_ALLOWED/FORBIDDEN`,
  `CONTRACT_KNOWN_HORIZONS`, `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`,
  `FORBIDDEN_RAW_PRICE_COLUMNS`, `ALIGNMENT_KEYS`, `SPLIT_POLICY_NAME`,
  `EXPECTED_SPLIT_DATE_COUNTS`, `STANDARDIZATION_RULE`, `NON_AUTHORIZATION_FLAGS` all
  `False`, `V002_TERMINAL_*`, `SEALED_TEST_*`);
  `src/prometheus/research/microstructure/labels_schema_v002.py`
  (`LABEL_DATASET_FAMILY_V002 = "microstructure_labels_aggtrades_v001"`,
  `LABEL_HORIZONS_V002 = ("1s","5s","15s","60s")`,
  `LABEL_HORIZON_MS_V002 = (1000,5000,15000,60000)`, the `_build_label_names` /
  `_build_support_column_names` builders, `LABEL_LINEAGE_COLUMNS_V002` (17),
  `LABEL_SCHEMA_V002` (40 columns), `DIRECTION_THRESHOLD_POLICY_V002` (strict-sign /
  no-deadband / no-bp-threshold / no-threshold-optimization / no-cost-based-threshold),
  `NULL_CENSORING_POLICY_V002` (per-horizon independent envelope-terminal censoring),
  `FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002`, the import-time asserts freezing the
  horizon set);
  `pre_v002_fixed_baseline_run.py`, `ml_baseline_design_v002.py`,
  `ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py` (baseline family, frozen
  hyperparameters, cost lock, calibration/stability helpers) — confirmed for constant
  reference only.

## 6. Confirmation no data files were read

Confirmed. This phase read **no** feature/label Parquet row, **no** v002 terminal
window, **no** sealed test split, **no** raw zip, **no** AH/AJ local result artefact
under `data/research/` or `data/microstructure/`, and called **no** endpoint. All
evidence was recovered from committed Markdown reports and committed source constants.
No file under `data/microstructure/` or `data/research/` was opened, listed for
content, hashed, or otherwise inspected (only `git status` / `git ls-files` /
`git check-ignore` tracked-state checks were run against those paths).

## 7. Confirmation no label was built

Confirmed. No longer-horizon label, label column, label Parquet, sidecar, manifest,
or proof artefact was built or written. This memo specifies a prospective contract
only; it produces no label output and creates no namespace.

## 8. Confirmation no AH builder / AI diagnostics / AJ baseline rerun occurred

Confirmed. The Phase 4bn-AH dataset builder, the Phase 4bn-AI diagnostics, and the
Phase 4bn-AJ fixed baseline runner were **not** re-run. No model was trained, scored,
or evaluated; no metric was recomputed, revised, or re-derived. Every figure below is
quoted verbatim from the committed AH / AI / AJ / AK / AL reports.

## 9. AL recommendation summary (recovered)

- **Final decision:** `RECOMMEND_LONGER_HORIZON_LABEL_CONTRACT_MEMO_NEXT`.
- **Recommended next memo:** a docs-only **longer-horizon label contract / spec memo**
  (this Phase 4bn-AM).
- **Horizons:** 5m / 30m / 1h at design level; **5m primary / lead**; **30m and 1h
  secondary diagnostic**.
- **Default family:** conservative **multi-horizon diagnostic family** — extend the
  strict-sign family pattern to the new horizons **and** record the continuous
  forward-return distributions + descriptive 8 bps / 16 bps cost-clearing shares
  (economic materiality as a **descriptive diagnostic**, not a baked-in target);
  cost-aware / magnitude / deadband options evaluated but not adopted-by-default.
- **Boundary:** no build, no data read, no namespace; any actual build requires a
  further separate authorization; no successor execution authorized.

## 10. AJ / AI / AH evidence summary (recovered)

**AJ (fixed baselines, once each; verbatim):** validation L2 accuracy **0.5453**;
majority **0.4950**; persistence **0.5158**; **L2 uplift over majority +5.03 pp / over
persistence +2.96 pp**; validation **date- and month-block agreement 1.000**;
**holdout no sign reversal**; **high-confidence tail (≥0.8) 0.633, beats the floor
0.4950 but overconfident** (ranking/diagnostic use only); **2.47%** of validation 15s
moves exceed the locked 16 bps round-trip cost (median |ret| 2.53 bps, mean 3.84, p90
9.66, p99 23.0; holdout > 16 bps 1.20%). Verdict `CONTINUE_ONE_FOLLOWUP`; target
remains **information-diagnostic, not economic**.

**AI (descriptive, no models):** near-binary 15s target (flat class ~1%: train 1.18%,
val 1.48%, holdout 0.97%; ±1 classes ~49–50%); the ~397M kept rows are **not** ~397M
independent observations (heavy 15s label overlap); decision blocks are **275 UTC
dates / 9 UTC months**; the continuous **forward**-return distribution was **not**
available from AH artefacts alone (measured only later during the AJ row-level read).

**AH (data-reading builder, single run):** leakage/split proof **VALIDATED before any
write** (strict alignment over 4 keys + `utc_date` on all 400,001,695 rows, **0
mismatches**; per-horizon earlier-split boundary crossings **= 0** at 1s/5s/15s/60s; 0
embargo rows used; **45-column** feature allowlist, empty forbidden scan; train-only
transform); **no v002 terminal** (`v002_terminal_window_read = false`), **no sealed
test** (`sealed_test_split_touched = false`), **`test_rows_loaded = 0`**; **compact
leakage-proof dataset specification** (a full 400M×45 float64 matrix ≈ 144 GiB would
breach the Phase 4bn-L 125 GiB cap); all 8 non-authorization flags `false`.

**AK:** `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`; selected
`longer_horizon_label_memo`; the other three §16 categories
(`bookticker_midprice_data_admissibility_memo`,
`code_only_evaluation_framework_extension` / block-bootstrap,
`fixed_capacity_model_comparison_memo`) rejected / deferred.

## 11. Recovered Phase 4bn-AE label / cost / claim-scope constraints

- **Allowed claim scope (§8):** (a) short-horizon directional **information**; (b)
  **v002 small-lift sign reproduction**; (c) **calibration / confidence-tail**
  assessment. Nothing more.
- **Forbidden claim scope (§8 / §19):** tradability; profitability; strategy
  viability; execution viability; slippage/spread adequacy; live-readiness;
  paper/shadow readiness; PnL; backtest validity; production suitability; economic
  significance.
- **Locked cost:** 8 bps per side / 16 bps round-trip. Descriptive only.
- **Cost-realism policy (§15):** report the forward-return distribution and the
  cost-clearing shares **descriptively only** — no trading rule, no cost-aware label,
  no PnL at evaluation stage.
- **Dependence policy (§10, Option 1):** decision evidence at the UTC date/month block
  level; no per-row significance language; decimation reserved-not-adopted.
- **Direction-threshold lock:** strict sign of `forward_log_return_H` at a zero
  threshold; **no deadband, no bp threshold, no threshold optimization, no cost-based
  threshold** — target **non-economic by construction**.
- **Existing label family** (`microstructure_labels_aggtrades_v001`) covers **1s / 5s
  / 15s / 60s only**, frozen by import-time asserts; **5m / 30m / 1h are a new label
  layer**, not a config toggle.
- **§19 strategy / PnL / backtest / live boundary (absolute):** any strategy path
  requires a future **M0-style mechanism-admissibility memo** (M0.5 cost realism at
  8 bps/side · 16 bps round-trip, execution feasibility, slippage/spread — which
  aggTrades-only data cannot support, mid/book required — label economic relevance,
  strategy admissibility vs retained rejections, no-rescue) **plus** separate
  authorization for each capability.

## 12. Contract / spec purpose

To pre-register — at the design level only — a **future** longer-horizon aggTrades
label layer that would let Prometheus **measure**, descriptively, whether the
short-horizon directional information demonstrated at 15s (AJ) persists and whether
longer-horizon **raw** moves clear the locked 16 bps round-trip cost materially more
often at 5m / 30m / 1h. The contract is written to be precise enough that a later,
separately authorized build prompt is tightly bounded — same admitted pre-v002
aggTrades sources, same leakage machinery, compact-spec posture, descriptive
diagnostics only, and no ML / strategy / PnL of any kind. **The contract does not
authorize the build.**

## 13. Prospective label family name and relationship to existing family

- **Prospective label family:** `microstructure_labels_longhorizon_aggtrades_v001`
  (a **new sibling family**, parallel to the existing
  `microstructure_labels_aggtrades_v001`).
- **Prospective contract identity:**
  `microstructure_longhorizon_label_aggtrades_pre_v002_contract_v001`.
- **Why a new family, not an extension:** the existing v002 label schema freezes its
  horizon set to `("1s","5s","15s","60s")` via import-time asserts
  (`assert LABEL_HORIZONS_V002 == ("1s","5s","15s","60s")`), so the frozen schema
  **cannot** be mutated to add 5m/30m/1h. The new family therefore **reuses the exact
  schema pattern** (identical column-name builders, the 17 lineage columns +
  `label_config_hash`, the per-horizon support-column structure, the
  `DIRECTION_THRESHOLD_POLICY` string, the `NULL_CENSORING_POLICY` structure, and the
  forbidden-substring scan) applied to the **new horizon set**, leaving the existing
  v002 family and all its frozen constants **untouched**.
- **Future build outputs (design-level):** compact per-partition label Parquet
  artefacts + per-Parquet `.sha256` sidecars + inventory, a label manifest, a
  source-binding record (feature / normalized / raw manifest + config + gate-report
  SHA256), and a leakage / split / censoring **proof** artefact — mirroring the AH
  compact-spec posture (Phase 4bb-F sidecar policy). **None built in this phase.**

## 14. Horizon set

| Role | Horizon string | Horizon ms | Multiple of 60s (existing max) |
| --- | --- | --- | --- |
| **Primary / lead** | `5m` | `300000` | 5× |
| Secondary diagnostic | `30m` | `1800000` | 30× |
| Secondary diagnostic | `1h` | `3600000` | 60× |

- **Ordering:** ascending — `5m`, `30m`, `1h` — mirroring the existing family's
  canonical ascending order.
- **Naming convention:** consistent with the existing family's suffix style
  (`60s` → `5m` / `30m` / `1h`); minutes/hours units for readability beyond 60s. All
  names pass the `FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002` scan (no `target`, `signal`,
  `strategy`, `pnl`, etc.).
- **Relationship to existing 1s/5s/15s/60s family:** disjoint horizon set; identical
  schema pattern; the new family is the **long-horizon sibling** of the existing
  short-horizon family. `5m` is designated the lead per AL (best
  signal-persistence-vs-materiality tradeoff); `30m`/`1h` are diagnostic (larger raw
  moves but weaker feature→target link, heavier overlap, larger censoring).

## 15. Column / schema specification (design-level; not implemented)

**Regression label columns (per horizon):**
`forward_log_return_5m`, `forward_log_return_30m`, `forward_log_return_1h`.

**Classification label columns (per horizon):**
`forward_direction_5m`, `forward_direction_30m`, `forward_direction_1h`
(class set `(-1, 0, 1)`; zero class preserved).

**Per-horizon support columns** (for each of `5m`, `30m`, `1h`):
`reference_row_index_H`, `reference_timestamp_ms_H`, `horizon_censored_flag_H`.

**Global support columns:** `label_invalid_price_flag`, `label_any_censored_flag`.

**Lineage / identity columns (reused verbatim, 17):** `dataset_family`,
`dataset_version`, `label_schema_version`, `source_feature_dataset_family`,
`source_feature_dataset_version`, `source_feature_manifest_sha256`,
`source_feature_parquet_sha256`, `source_feature_successor_state_sha256`,
`source_phase_4bm_j_gate_report_sha256` (or the pre-v002 equivalent gate-report SHA
field), `source_normalized_manifest_sha256`, `source_raw_manifest_sha256`, `symbol`,
`utc_date`, `row_index`, `agg_trade_id`, `feature_timestamp_ms`,
`source_transact_time_ms`; plus `label_config_hash`.

Row-schema size ≈ 6 label + 11 support + 17 lineage + 1 config-hash ≈ **35 columns**
(narrow — cf. the frozen v002 family's 40).

**Report / manifest-level summary fields (NOT row-level columns):** per horizon × per
split (and per-month / per-date where feasible): forward-return location / dispersion
/ tail summaries (median, mean, p90, p99, max of `|forward_log_return_H|`); share of
moves `> 8 bps` one-way; share of moves `> 16 bps` round-trip; per-horizon censored /
support counts. These live in the manifest / proof / report, not as per-row columns,
and are **descriptive diagnostics only**.

**Forbidden columns (design-level):** no `pnl` / `profit` / `signal` / `strategy` /
`target` / `barrier` / `prediction` / `model` / `score` / `decision` / `entry` /
`exit` / `edge` / `alpha` (etc.) columns; no raw-price / mid / book / bid / ask
columns as labels; the forbidden-substring scan must pass. **None of these columns is
implemented here.**

## 16. Direction-threshold policy

**Default (adopted for the contract):** strict-sign extension of the v002 policy to
the new horizons, verbatim in structure —
`forward_direction_H` derived **only** from the sign of `forward_log_return_H`:
`+1` if strictly positive, `0` if exactly zero, `-1` if strictly negative, `null` if
`forward_log_return_H` is null; **strict zero-log-return threshold; no deadband; no bp
threshold; no threshold optimization; no learned threshold; no cost-fitted threshold;
no threshold selected after looking at the empirical distributions.**

**Evaluated but NOT adopted by default:** cost-aware ternary labels; magnitude /
material-move labels; abstain / neutral-band (deadband) labels. If any such option is
adopted by a **future** phase, it must be: **fixed**; **pre-registered before any data
is read**; **tied to the locked cost** (8 bps one-way / 16 bps round-trip); **never
optimized, tuned, learned, or chosen after seeing the distributions**; and
**separately authorized**. This contract does **not** adopt them; the economic-
materiality question is answered by the **descriptive** cost-clearing summaries (§17),
not by baking a threshold into the target.

## 17. Continuous-return and cost-realism summary specification

A future build / report must produce, **per horizon (`5m`/`30m`/`1h`) and per split
(train / validation / holdout)**, and per-month / per-date where feasible:

- location / dispersion / tail summaries for `forward_log_return_H` (median, mean, p90,
  p99, max of the absolute value, and sign balance of the raw return);
- **share of moves exceeding 8 bps one-way**;
- **share of moves exceeding 16 bps round-trip**;
- per-horizon **censored** and **support** (valid, non-null, non-censored) counts;
- the near-binary / flat-class prevalence of `forward_direction_H` (mirroring the AI
  15s diagnostic).

These are **descriptive diagnostics only** and must be reported as such. They must
**not** be interpreted as, or cited as evidence of, tradability, PnL, edge, economic
significance, or strategy viability. Per §10, the unit of decision evidence remains
the UTC date/month block; no per-row significance / p-value / confidence-interval
language. **No empirical 5m/30m/1h distribution value is asserted in this memo** — the
distributions are unmeasured and would be produced only by a later authorized build.

## 18. Leakage / split / censoring policy

The future build must preserve every Phase 4bn-AH leakage invariant, extended to the
new horizons:

- **Completed-event / completed-bar discipline.** Each `forward_log_return_H` is
  computed strictly from the **future horizon endpoint** of a completed event; no
  partial / in-progress horizon; the reference row/timestamp recorded in
  `reference_row_index_H` / `reference_timestamp_ms_H`.
- **Target endpoint strictly at the future horizon**; no target may depend on any
  value at or before the anchor beyond the endpoint definition.
- **No future-derived features.** The 45-feature causal allowlist stays **past-only**
  and **unchanged**; longer horizons add **labels**, never features; the forbidden
  model-matrix / raw-price scans must stay empty.
- **No source reordering or lookahead**; strict positional alignment over the
  alignment keys (`row_index`, `agg_trade_id`, `feature_timestamp_ms`,
  `source_transact_time_ms`, + `utc_date`), 0 mismatches, no join/reorder/fill —
  exactly as AH proved.
- **Split boundary handling / 1-day boundary embargo.** The chrono split
  `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` and its **1-day
  boundary embargo** are preserved. Because 5m / 30m / 1h are all **≪ 1 day**, the
  1-day embargo remains **sufficient** to prevent forward-window leakage across the
  train/validation/holdout boundaries.
- **Forward endpoint must not cross into a disallowed split/window.** Any row whose
  forward endpoint would cross an earlier-split boundary must be **censored** (target
  dropped); the build must report per-horizon earlier-split boundary-crossing counts
  and require them **= 0** into earlier splits, mirroring the AH proof.
- **Per-horizon censoring near segment / envelope ends.** The per-horizon independent
  envelope-terminal censoring policy (`NULL_CENSORING_POLICY_V002` structure) extends
  to the new horizons; the **censored fraction grows with H** and must be **measured
  and reported** (unlike the near-zero 60s drop) — a first-class contract obligation.
  No forward-fill beyond the envelope; no cross-envelope stitching; no NaN/Inf in
  outputs.
- **v002 terminal exclusion** (2024-12-01..2025-02-28): `v002_terminal_window_read =
  false`; the v002-terminal config hashes rejected by value + prefix.
- **Sealed-test exclusion** (2025-02-14..2025-02-28): `sealed_test_split_touched =
  false`; the sealed test is outside the pre-v002 segment and never read.
- **`test_rows_loaded = 0`** preserved in both the proof and the manifest.
- **UTC date assignment and timestamp discipline.** UTC Unix-ms; deterministic
  UTC-date split assignment; `open_time` / `source_transact_time_ms` /
  `feature_timestamp_ms` discipline preserved.

## 19. Storage / budget / build posture

- **No build now.** This phase specifies only; it allocates no storage and creates no
  namespace.
- **Future build separately authorized** (see §24–§26): a later, separate operator
  prompt is required before any label is built or any data is read.
- **Preserve the AH compact-spec posture.** The future build should write a **compact
  label layer** (narrow per-partition label Parquet + sidecars + manifest + proof),
  not a re-materialised wide matrix; the label layer is narrow (~35 columns) and is
  expected to be modest (single-digit to low-tens of GiB), well within budget.
- **Preserve the Phase 4bn-L 125 GiB derived cap.** A **budget preflight** (as in AH,
  which checked free space ≥ 500 GiB) must PASS before any write.
- **Local / gitignored output namespace.** Any future output namespace must be
  **local and gitignored** (e.g. under `data/research/microstructure/...`, matching
  `.gitignore:88`), unless a future authorization explicitly changes that. **No data
  file may be committed.**
- **Phase 4bb-F sidecar policy applies** (per-Parquet `.sha256` sidecars + inventory).
- **No committed data files**; `.claude/scheduled_tasks.lock` never committed.

## 20. Future build validation / proof artefact requirements

At the design level, a future build must produce and validate (fail-closed, before
any write where applicable):

- a **label manifest** (family / version / horizons / row & partition counts / config
  hash);
- **per-Parquet `.sha256` sidecars + an inventory**;
- a **source manifest / config / gate-report SHA256 binding** to the admitted pre-v002
  feature / normalized / raw sources;
- a **leakage / split / censoring proof** VALIDATED **before** any write (strict
  key-alignment count + 0 mismatches; deterministic UTC-date split; embargo rows used
  = 0);
- a **per-horizon earlier-split boundary-crossing report** (= 0 into earlier splits);
- **per-horizon censored / support counts** and drop-by-reason accounting (never
  impute);
- **hash / sidecar validation** of all inputs and outputs;
- explicit **no-v002 / no-sealed / no-test proof fields**
  (`v002_terminal_window_read = false`, `sealed_test_split_touched = false`,
  `test_rows_loaded = 0`);
- a clean **forbidden-substring scan** over all output column names;
- **non-authorization flags all `false`** (`ml_authorized`, `diagnostics_authorized`,
  `strategy_authorized`, `signals_authorized`, `pnl_authorized`, `backtest_authorized`,
  `live_authorized`, `exchange_write_authorized`).

## 21. Evaluation / interpretation scope

- This label contract **does not authorize ML training**.
- This label contract **does not authorize diagnostics**.
- Any future evaluation (baselines, diagnostics, calibration, block agreement, etc.)
  must be **separately authorized** — building a longer-horizon label layer is not
  permission to model it.
- **Allowed claims remain design / label-materiality diagnostics only** (AE §8
  a/b/c). If the layer is later built, its continuous-return distributions and
  cost-clearing shares may answer only the **economic-materiality diagnostic**
  question (do longer-horizon raw moves clear cost materially more often?), **never**
  tradability.
- **Forbidden claims remain absolute** (AE §8 / §19): no tradability / profitability /
  strategy / execution / slippage-spread / live / paper-shadow / PnL / backtest /
  production-suitability / economic-significance claim, however favourable any future
  distribution looks.

## 22. Interaction with the bookTicker / mid-price deferred path

Longer horizons **reduce** bid-ask-bounce sensitivity but do **not** provide mid-price
or order-book realism. On aggTrades-only data, the longer-horizon label layer can
answer *"do raw last-trade-price moves clear 16 bps materially more often at
5m/30m/1h?"* but **cannot** answer *"can we execute at those prices net of spread and
slippage?"* The `bookticker_midprice_data_admissibility_memo` (AE §16(b)) therefore
**remains the required, still-deferred, still-unauthorized** gate for execution
realism; the longer-horizon labels are **complementary to**, not a substitute for,
that path. A favourable longer-horizon materiality result would strengthen — but not
authorize — the future case for the mid/book path.

## 23. Interaction with strategy / PnL / backtest / live boundary

Absolute and unsoftened (AE §19). **No label contract, and no future longer-horizon
label result, authorizes anything toward strategy.** Any strategy / signals /
threshold-or-confidence-gated trading / backtest / PnL / Sharpe / hit-rate / position
sizing / execution / paper / shadow / live-readiness / exchange-write path remains
behind a future **M0-style mechanism-admissibility memo** clearing M0.5 cost realism
at 8 bps/side · 16 bps round-trip, execution feasibility, slippage/spread (which
aggTrades-only data cannot support — mid/book required), label economic relevance,
strategy admissibility vs the retained rejections and the M0 §7.D microstructure-lane
`NOT_RECOMMENDED_NOW` posture, and the no-rescue constraints — **plus** separate
authorization for each capability. This contract does not move any part of that
boundary.

## 24. Final AM decision

**`LABEL_CONTRACT_SPEC_RECORDED__LABEL_BUILD_AUTHORIZATION_RECOMMENDED`.**

Reasoning (evidence-driven; not overfit toward proving ML works; not biased toward
build authorization; no economic/trading claim):

- **A safe, precise contract is definable from committed evidence.** The prospective
  family reuses the proven v002 label schema pattern, the frozen alignment keys, the
  chrono split + 1-day embargo, the per-horizon envelope-terminal censoring, and the
  cost lock — all recovered from committed source. So `LABEL_CONTRACT_SPEC_BLOCKED`
  (option C) does **not** apply.
- **Recording a contract but recommending no build (option B) would dead-end the
  longer-horizon line.** The entire point of the AL/AK inquiry is to **measure**
  whether longer-horizon raw moves clear cost materially more often; that measurement
  requires a bounded build (a descriptive data read). Refusing the build would leave a
  spec that is never exercised, without a safety justification for doing so — the
  build is bounded (same already-admitted pre-v002 aggTrades sources, same leakage
  machinery, compact-spec, descriptive outputs, all non-authorization flags false) and
  answers exactly the open economic-materiality question AK/AL identified.
- Therefore the honest outcome is to **record the contract and recommend a future,
  separately authorized label-build phase** — while authorizing nothing here. This is
  a **recommendation**, not an authorization: the build still needs its own operator
  prompt, may read data only under that prompt, and would produce only descriptive
  label artefacts + distributions (no ML, no diagnostics beyond the descriptive
  summaries, no strategy).

This is **not** a trading, strategy, PnL, backtest, economic, or live-readiness
decision, and it does not claim longer horizons are tradable.

## 25. Exact high-level future build scope (option A)

Recommend **exactly one** future **label-build authorization phase** (Phase 4bn-AN, by
sequence — name not binding), scoped at a high level as:

- **Build** the `microstructure_labels_longhorizon_aggtrades_v001` layer for horizons
  **5m / 30m / 1h** over the **admitted pre-v002 aggTrades segment only**
  (2024-03-01..2024-11-30; 275 partitions; the AH-verified feature/normalized/raw
  sources), under the schema and policies pre-registered in §13–§20.
- **Produce** the compact label Parquet layer + sidecars + inventory + manifest +
  leakage/split/censoring proof, and the §17 **descriptive** continuous-return / cost-
  clearing summaries per horizon × split (+ per-month/per-date where feasible).
- **Preserve** every §18 leakage invariant, the compact-spec posture, the 125 GiB cap
  (with budget preflight), the local/gitignored namespace, and all non-authorization
  flags `false`; **exclude** the v002 terminal and sealed test; keep `test_rows_loaded
  = 0`.
- **Explicitly excluded from that build:** any ML / model / scoring / prediction /
  inference; any feature selection / threshold optimization / model selection /
  hyperparameter search; any cost-aware / magnitude / deadband label adoption (unless a
  still-later phase pre-registers and separately authorizes it); any strategy /
  signals / PnL / backtest / paper / shadow / live / exchange-write; any new data
  acquisition / endpoint / raw-zip read beyond the already-admitted pre-v002 sources.
- The build would be a **single controlled run** with a one-run guard, mirroring AH.

Evaluation of the resulting labels (baselines / diagnostics) would be a **further,
separate** authorization beyond the build.

## 26. No prompt generated / no build authorized (option A)

This memo **does not generate** the recommended build-authorization phase's prompt and
**does not authorize** any build, data read, or successor execution phase. The
recommended label-build phase begins **only** under a separate future operator prompt,
and the build may **read data only under that prompt**. Recommending the build consumes
nothing beyond recording the recommendation; the operator remains free to build, defer,
or decline.

## 27. If no build recommended — N/A

Not applicable; the decision is
`LABEL_CONTRACT_SPEC_RECORDED__LABEL_BUILD_AUTHORIZATION_RECOMMENDED`. (Had the build
been judged unsafe or unjustified, this memo would have recorded
`LABEL_CONTRACT_SPEC_RECORDED__NO_BUILD_RECOMMENDED`, stated the reason, and remained
paused.)

## 28. If blocked — N/A

Not applicable; a safe, precise contract is definable from committed evidence (§24).
(Had committed evidence been insufficient to specify a safe contract, this memo would
have recorded `LABEL_CONTRACT_SPEC_BLOCKED__INSUFFICIENT_SPEC_EVIDENCE` with the exact
blocker and remained paused.)

## 29. Allowed claims preserved

Preserved verbatim (AE §8 / `CLAIM_SCOPE_ALLOWED`): (a) the 45 causal aggTrades
features contain **short-horizon directional information** about
`forward_direction_15s` on the pre-v002 segment; (b) the **directional sign** of the
v002 small-lift result **is reproduced** on the larger, earlier pre-v002 regime; (c)
the probability outputs' **calibration / confidence tail** beats the majority floor on
accuracy but is overconfident in level — ranking/diagnostic use only. This AM memo adds
**no** new empirical claim; its longer-horizon content is **design-level and
qualitative**, and it invents **no** empirical longer-horizon distribution.

## 30. Forbidden claims preserved

Preserved verbatim (AE §8 / `CLAIM_SCOPE_FORBIDDEN`, §19). Nothing in this memo may be
cited as evidence of: tradability; profitability; strategy viability; execution
viability; slippage/spread adequacy; live-readiness; paper/shadow readiness; PnL;
backtest validity; production suitability; economic significance. **This memo does not
claim longer horizons are tradable.** `forward_direction_15s` remains an
information-diagnostic, non-economic target that may embed bid-ask bounce
(aggTrades-only, no mid/book); the prospective longer-horizon targets are likewise
information / materiality **diagnostics** only. The 2.47%-of-moves-clear-cost figure is
descriptive context, not evidence of edge. The locked cost remains **8 bps per side /
16 bps round-trip**. The §19 strategy/PnL/backtest/live boundary is absolute and
unsoftened.

## 31. Exact validation commands and results

Docs-only phase (no source/test/script changed), so no pytest/ruff/mypy required.

- `git rev-parse --abbrev-ref HEAD` (pre-branch) → `main`. ✅
- `git rev-parse main` / `origin/main` / `HEAD` (pre-branch) → all
  `4b96b671df485fffbe1f369baebcb8ecfdb4fe5e`. ✅
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`. ✅
- `git checkout -b phase-4bn-am/longer-horizon-label-contract-spec` → created at base
  SHA `4b96b671…`. ✅
- `git ls-files data/microstructure/` → **0 tracked**. ✅
- `git ls-files data/research/` → **0 tracked**. ✅
- `git check-ignore -v data/microstructure/` → `.gitignore:85`. ✅
- `git check-ignore -v data/research/` → `.gitignore:88`. ✅
- `.claude/scheduled_tasks.lock` → `git check-ignore` returns nothing; left
  **untracked and not committed**. ✅
- `git diff --check` → clean. ✅
- `git diff --name-status main..HEAD` (after commit) → only the two new
  `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-am_*.md` files. ✅
- No data-output tracked-file check → no file under `data/` staged or committed. ✅

(Exact post-commit command outputs are reproduced in the closeout and the final
operator report.)

## 32. Git status

Before commit: the two new Phase 4bn-AM docs untracked, plus the transient
`?? .claude/scheduled_tasks.lock` (not committed). No `data/` file staged. Final
committed SHA and post-commit `git status --short` are reproduced in the closeout and
the final operator report. `current-project-state.md` unchanged (§34).

## 33. Result state

`LONGER_HORIZON_LABEL_CONTRACT_SPEC_RECORDED__LABEL_BUILD_AUTHORIZATION_RECOMMENDED__NO_LABEL_BUILD__NO_DATA_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## 34. Recommended next state

**Remain paused.** The longer-horizon label contract / spec is recorded and recommends
**exactly one** future, separately authorized **label-build phase** (5m/30m/1h over the
admitted pre-v002 aggTrades segment; compact-spec; descriptive summaries; no ML /
strategy). The recommended build is **not started** and requires a **separate future
operator prompt**; the build may read data only under that prompt. No ML, diagnostics,
strategy, signals, PnL, backtest, paper/shadow, live, or exchange-write path is
authorized (all remain behind their own separate authorizations and, for any trading
path, the §19 M0-style gate). `current-project-state.md` is left unchanged, matching
the immediate Phase 4bn-AH/AI/AJ/AK/AL precedent (the update convention at this arc
point is not clear/consistent, and per the operator instruction it is not updated;
recorded here as unchanged).

## 35. Explicit no-successor execution statement

Phase 4bn-AM authorizes **no** successor execution phase. It does **not**, and does not
authorize anyone to: generate the recommended build phase's prompt; build, generate, or
write any longer-horizon label / label column / label Parquet / sidecar / manifest /
proof; create any new label / dataset / output namespace; read any feature/label
Parquet / v002 terminal / sealed test / raw zip / AH / AJ data artefact; acquire data
or call any endpoint; change any source / test / manifest / gate report / sidecar /
split file / ML config; train / score / predict / infer; run new diagnostics; perform
feature selection / threshold optimization / model selection / hyperparameter search;
rerun the AH builder, AI diagnostics, or AJ baselines; do strategy / signals / PnL /
backtest / Sharpe / hit-rate / position sizing / execution / paper / shadow /
live-readiness / deployment / exchange-write; use credentials / `.env` / `.mcp.json` /
MCP / Graphify / WebSocket / user stream; or authorize any Phase 5 / successor phase.
Every retained verdict and project lock (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A /
5m thread / V2 / G1 / C1; §11.6 = 8 bps per side / 16 bps round-trip; the Phase 4ak M0
twelve-clause gate; Phase 4al no-rescue; the Phase 4aw `flip_research_eligible(...)`
always-raises invariant — never invoked; Phase 4bb-F sidecar policy; the Phase 4bn-AA
split artefact, 4bn-AB source-admissibility posture, 4bn-AC ML dataset contract, 4bn-AE
pre-registration claim-scope, and the 4bn-AH..AL results including the AK
single-follow-up selection and the AL label-memo recommendation / no-build boundary) is
preserved verbatim. Phase 4 canonical remains unauthorized. The recommended label-build
phase begins only under a separate future operator prompt. Do not merge to main and do
not push unless explicitly instructed in a later prompt; do not generate a
merge-closeout or the recommended next prompt unless explicitly instructed later.
