# Phase 4bn-H — Closeout

**Phase 4bn-H is branch-complete only by this work; not merged into main;
not project-complete.** Phase 4bn-H is the docs-only / design-only /
scoping-only acquisition-readiness memo authorised by the operator
following the Phase 4bn-G recommendation
`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
The phase takes the Phase 4bn-G combined data-expansion + storage-scaling
scoping decision one level lower of abstraction by selecting Option B
(longer single continuous BTCUSDT aggTrades history) as the candidate
expansion shape, comparing calendar-coverage options A / B / C / D / E
at design level only, recommending Option C (12-month continuous
BTCUSDT) as the cleanest first-expansion calendar coverage subject to
separate operator authorization of a docs-only acquisition execution
plan, preserving the Phase 4bn-G `A + F + C` storage posture verbatim
(Parquet canonical; defer migration; DuckDB querying Parquet in place as
the preferred non-invasive query layer), defining 14 pre-acquisition
gates extending Phase 4bn-G §13, and defining 13 stop conditions
extending Phase 4bn-G §8.24. The phase authorises nothing executable.
**Phase 4bn-H is a docs-only / design-only / scoping-only
acquisition-readiness memo.** **Phase 4bn-H does not acquire data.**
**Phase 4bn-H does not migrate storage.** **Phase 4bn-H does not create
any database.** **Phase 4bn-H does not compact Parquet.** **Phase 4bn-H
does not create v003.** **Phase 4bn-H does not authorize acquisition.**
**Phase 4bn-H does not authorize any successor.** **Phase 4bn-H does not
run diagnostics.** **Phase 4bn-H does not run ML.** **Phase 4bn-H does
not train models.** **Phase 4bn-H does not score models.** **Phase
4bn-H does not generate predictions.** **Phase 4bn-H does not inspect
the test holdout.** **Phase 4bn-H does not use the sealed test split.**
**Phase 4bn-H does not rank features.** **Phase 4bn-H does not select
features.** **Phase 4bn-H does not prune features.** **Phase 4bn-H does
not engineer features.** **Phase 4bn-H does not tune hyperparameters.**
**Phase 4bn-H does not tune thresholds.** **Phase 4bn-H does not fit
calibrators.** **Phase 4bn-H does not run strategy research.** **Phase
4bn-H does not define a strategy.** **Phase 4bn-H does not generate
trade signals.** **Phase 4bn-H does not simulate PnL.** **Phase 4bn-H
does not run backtests.** **Phase 4bn-H does not modify dataset
layout.** **Phase 4bn-H does not call any public, authenticated, or
private endpoint.** **Phase 4bn-H does not open any WebSocket or user
stream.** **Phase 4bn-H does not use credentials, `.env`, `.mcp.json`,
MCP, or Graphify.** **Phase 4bn-H does not mutate any manifest.**
**Phase 4bn-H does not mutate any successor-state artefact.** **Phase
4bn-H does not commit `data/microstructure`.** **Phase 4bn-H does not
commit `data/research`.** **Phase 4bn-H does not authorize Phase 4bn-I,
Phase 5, paper / shadow, live-readiness, deployment, exchange-write,
production keys, or any successor phase.** **Recommended state remains
paused.**

## Branch and base

- **Branch:** `phase-4bn-h/docs-only-acquisition-readiness`.
- **Base `main` SHA:** `1ab9ebea5b959764c9cfc6821245103ceb301ffa` (Phase
  4bn-G SHA-finalization commit `docs(phase-4bn-g): finalize merge
  closeout shas`; pre-branch `main == origin/main` verified in sync).

## Tracked changes

- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-h_docs-only-acquisition-readiness.md`
  (added; this phase's implementation report; 19 sections + 3
  appendices).
- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-h_closeout.md`
  (added; this closeout).
- `docs/00-meta/current-project-state.md`
  (narrow update: Phase 4bn-H paragraph + new "Current phase:" block;
  prior Phase 4bn-A / 4bn-B / 4bn-C / 4bn-D / 4bn-E / 4bn-F / 4bn-G
  paragraphs and prior "Current phase:" blocks preserved as labelled
  historical context).

No other tracked file was created, modified, or deleted. `pyproject.toml`,
`README.md`, `.gitignore`, MCP files, manifests, sidecars, gate reports,
successor-state artefacts, and existing source / test / script files were
all left byte-identical.

## Local gitignored outputs

**None.** Phase 4bn-H is a docs-only / design-only / scoping-only phase
and produces no local artefact under `data/microstructure/` or
`data/research/`. No CSV, no JSON, no parquet, no manifest, no sidecar,
no gate report, no successor-state file, and no database file was
created. No diagnostic, ML, simulation, backtest, or acquisition kernel
was invoked.

## Decision

`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Phase 4bn-H crystallises the Phase 4bn-G combined scoping decision into
a concrete acquisition-readiness framework for Option B (longer single
continuous BTCUSDT aggTrades history), a concrete calendar-coverage
comparison (Options A / B / C / D / E covering no acquisition, 6
months, 12 months, 24 months, and close-the-arc respectively at design
level only), an explicit data-family contract preserving v002
semantics, a storage posture preserving the Phase 4bn-G `A + F + C`
baseline verbatim (Parquet canonical; defer migration; DuckDB querying
Parquet in place as the preferred non-invasive query layer; defer
Storage B compaction and Storage D DuckDB database cache; preserve
SQLite verbatim for the runtime role only), 14 pre-acquisition gates
extending the Phase 4bn-G §13 14-gate framework by narrowing it to the
Option B shape, 13 stop conditions extending the Phase 4bn-G §8.24
"exact stop conditions" requirement at one level lower of abstraction,
and a single recommended path: a future docs-only acquisition execution
plan focused on Option C (12-month continuous BTCUSDT) that pre-declares
the exact UTC date range, the exact disk-footprint cap, the exact
derivation-time cap, the exact canonical path layout, the exact
sidecar / manifest policy, the exact source-endpoint policy
confirmation, the exact test-holdout preservation language, the exact
new-holdout policy (if any), and the exact fail-closed stop conditions.
**The successor is recommended only and is not authorized.** A separate
operator authorization is required for any executable follow-up. The
operator may equivalently remain paused, request a merge prompt for
Phase 4bn-H, reject further ML-baseline successors and close the ML
arc, separately authorize only a future docs-only storage-architecture
decision memo, or separately authorize a future docs-only combined
acquisition execution plan + storage-architecture decision memo; Phase
4bn-H does not foreclose any of these alternatives.

## Phase 4bn-G decision carried forward

`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— Phase 4bn-G defined the combined data-expansion + storage-scaling
scoping framework (24-requirement framework; seven candidate expansion
shapes; six candidate storage architectures; 7 × 6 coupled
decision matrix; 14 pre-acquisition gates; 10 pre-storage-migration
gates; 13 non-authorization constraints; recommended `A + F + C`
storage path) and recommended the docs-only acquisition-readiness memo
(this phase) as the cleanest non-paused option focused on a specific
expansion shape, most plausibly Option B — longer continuous BTCUSDT.
Phase 4bn-H is the chosen acquisition-readiness memo execution and
inherits the Phase 4bn-G recommendation boundary verbatim.

## Phase 4bn-F / 4bn-E / 4bn-D / 4bn-C / 4bn-B interpretation carried forward

- **Phase 4bn-F (verbatim):**
  `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  — concluded the 90-day window is useful but not enough to prove
  broad sufficiency, insufficiency, representativeness, or outlier
  status; treated "outlier" as an unresolved risk, not a conclusion.
- **Phase 4bn-E (verbatim):** `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`
  — partially ruled out gross train-vs-validation feature-distribution
  drift at the measurement-frame level only (31 low / 13 moderate /
  0 high / 1 undefined drift classification; highest absolute
  standardized mean delta 0.330; highest missing-rate delta ≈ 6e-06;
  13 moderate-drift features cluster on count and mean-quantity
  dimensions, signed consistently count-up / mean-quantity-down
  between train and validation).
- **Phase 4bn-D (verbatim):**
  `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-C (verbatim):** `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`
  — interpreted Phase 4bn-B evidence as small descriptive lift with a
  severe high-confidence calibration tail and §11.6 cost-commensurability
  fractions consistent with 80 – 95 % of validation rows being below
  the round-trip cost.
- **Phase 4bn-B (verbatim):** `RECORD_EVIDENCE_ONLY` — descriptive
  ML-baseline evidence on train / validation only; test holdout sealed
  (`test_rows_loaded: 0`); no model selected as best; no feature
  ranked or selected; no hyperparameter or threshold tuned; no
  strategy / signal / PnL / backtest.

Phase 4bn-H inherits all five decisions verbatim and softens none of
them.

## Validation summary

Phase 4bn-H is a docs-only phase. Its validation is limited to
documentation / repository-state checks:

- `git status --short` — only expected tracked Phase 4bn-H files plus
  pre-existing untracked `.claude/scheduled_tasks.lock` and
  pre-existing gitignored `data/research/` + `data/microstructure/`
  entries.
- `git diff --check` — clean (no whitespace errors).
- `git diff -- docs/00-meta/current-project-state.md docs/00-meta/implementation-reports/2026-05-30_phase-4bn-h_docs-only-acquisition-readiness.md docs/00-meta/implementation-reports/2026-05-30_phase-4bn-h_closeout.md`
  reviewed pre-commit: the only tracked changes are the new
  acquisition-readiness memo, the new closeout, and the narrow
  `current-project-state.md` Phase 4bn-H paragraph + new Current-phase
  block addition.
- No code, no tests, no scripts, no configuration, no manifests, no
  sidecars, no gate reports, no successor-state artefacts, and no
  `data/microstructure/` or `data/research/` artefacts were created,
  modified, or accessed for mutation.
- No ML script was run; no diagnostics script was run; no backtest
  script was run; no acquisition script was run; the Phase 4bn-E
  runner was not invoked; the Phase 4bn-B runner was not invoked; no
  local gitignored output was inspected.
- The test holdout was not used in any way; the
  `iter_partitions(split="test", ...)` raise pattern remains in force
  in the unchanged Phase 4bn-B implementation; Phase 4bn-H never
  opened any test row.
- Repository tooling (ruff, mypy, pytest) is not invoked for a
  docs-only scoping memo that creates no code surface and modifies no
  code; the Phase 4bn-G / 4bn-F precedents recorded the same omission
  rationale (whole-repo mypy baseline carries pre-existing
  `Missing type parameters for generic type "ndarray"` warnings that
  are unrelated to a docs-only phase); the diff-check and status-check
  are the relevant validation surface for this docs-only Tier 1
  scoping memo.

## Boundary confirmations

- no source code modified;
- no test modified;
- no committed script modified;
- no config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file
  modified;
- no `data/microstructure/` artefact committed;
- no `data/research/` artefact committed;
- no `data/microstructure/` artefact created, modified, or moved;
- no `data/research/` artefact created, modified, or moved;
- no manifest mutated; no `research_eligible` flipped; no
  `eligibility_gate_status` transitioned; no `chronological_split_policy`
  changed; no `diagnostics_authorized` / `ml_authorized` changed;
- no successor-state artefact mutated, created, moved, or accessed for
  mutation;
- no prior gate report mutated;
- no prior Phase 4bn-B / 4bn-E / 4bm-W local output mutated, read, or
  hashed by Phase 4bn-H;
- no ML model trained / scored; no prediction generated; no reusable
  split mask materialised; no model binary persisted; no row-level
  prediction persisted;
- no feature ranked, selected, pruned, or engineered;
- no hyperparameter or threshold tuned;
- no calibrator fitted;
- no probability-to-signal conversion;
- no strategy defined or run; no signal generated; no PnL simulated;
  no backtest run; no walk-forward optimization;
- test holdout not used for any reason;
- no data acquired; no public / authenticated / private endpoint
  called; no Binance API called; no WebSocket / user stream opened;
  no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- no v003 dataset created; no new dataset family created; no new
  label / feature / horizon / symbol acquisition; no longer-history
  acquisition; no multiple-window acquisition; no mark-price / spot /
  cross-venue / order-book / additional-aggTrades acquisition;
- no storage migration; no database created; no Parquet compaction;
  no DuckDB database file created; no SQLite database created; no
  partitioning policy changed; no compression policy changed; no
  dataset layout changed;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0
  amendment; no successor authorized.

## Recommended state

**Remain paused.** Phase 4bn-H is branch-complete only by this work;
not merged into main; not project-complete. Per the
`phase-workflow-standard.md` rule, Phase 4bn-H is NOT project-complete
until a separately authorized merge phase records its merge-closeout
on `main` per `merge-closeout-standard.md` (Tier 1). **No next phase
authorized.** The operator may equivalently:

- remain paused (default);
- request a merge prompt for Phase 4bn-H so the acquisition-readiness
  scoping decision becomes project-complete on `main`;
- reject further ML-baseline successors and close the ML arc;
- separately authorize a future docs-only acquisition execution plan
  (Phase 4bn-H's recommendation; subject to separate operator
  authorization; focused on the recommended Option C — 12-month
  continuous BTCUSDT aggTrades history, preserving v002 semantics,
  Parquet canonical storage, DuckDB-in-place query posture, and no
  ETHUSDT / v003 / compaction / cache in the first expansion);
- separately authorize a future docs-only storage-architecture
  decision memo only;
- separately authorize a future docs-only combined acquisition
  execution plan + storage-architecture decision memo (one level
  lower in abstraction than Phase 4bn-H; same recommendation pattern;
  same docs-only constraints).

**No acquisition / paper / shadow / live / exchange-write option is
valid from this state.**

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A /
5m thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per
side / round-trip 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase
3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase
4q; Phase 4v; Phase 4w; Phase 4ak M0 + post-null cooldown +
cooled-down families list + memo template; Phase 4al refined
no-rescue + §13 boundary + §14 hierarchy; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked);
Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model
+ R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase
4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1
lightweight Claude Code workspace standard) is preserved verbatim.

Phase 4 canonical remains unauthorized. Phase 4bn-H merge phase / Phase
4bn-I / any further successor (under any name performing the
recommended docs-only acquisition execution plan, the
separately-recommended docs-only storage-architecture decision memo,
the docs-only combined acquisition execution plan + storage-decision
memo, any acquisition phase, any storage-migration phase, any
database-creation phase, any v003-creation phase, any
Parquet-compaction phase, any ML implementation, any model training,
any model selection through results, any feature ranking, any feature
selection, any hyperparameter tuning, any threshold tuning, any
strategy, any signals, any PnL, any backtest, any paper / shadow /
live-readiness / deployment / exchange-write / production-key / Phase 5
/ any successor phase) remains unauthorized.
