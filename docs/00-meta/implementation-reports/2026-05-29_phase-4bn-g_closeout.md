# Phase 4bn-G — Closeout

**Phase 4bn-G is branch-complete only by this work; not merged into main;
not project-complete.** Phase 4bn-G is the docs-only / design-only /
scoping-only combined data-expansion requirements + storage-scaling
architecture scoping memo authorised by the operator following the Phase
4bn-F recommendation
`RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
The phase defines a concrete data-expansion requirements framework and a
concrete storage-scaling architecture comparison at design level only, and
turns the Phase 4bn-F recommendation into a governance blueprint for any
possible future data expansion and storage scaling, without acquiring data,
without migrating storage, without creating a database, without compacting
Parquet, without creating a v003 dataset, and without authorizing any
executable successor. **Phase 4bn-G is a docs-only / design-only /
scoping-only combined data-expansion requirements + storage-scaling
architecture scoping memo.** **Phase 4bn-G does not acquire data.** **Phase
4bn-G does not run diagnostics.** **Phase 4bn-G does not run ML.** **Phase
4bn-G does not train models.** **Phase 4bn-G does not score models.**
**Phase 4bn-G does not generate predictions.** **Phase 4bn-G does not
inspect the test holdout.** **Phase 4bn-G does not use the sealed test
split.** **Phase 4bn-G does not rank features.** **Phase 4bn-G does not
select features.** **Phase 4bn-G does not prune features.** **Phase 4bn-G
does not engineer features.** **Phase 4bn-G does not tune hyperparameters.**
**Phase 4bn-G does not tune thresholds.** **Phase 4bn-G does not fit
calibrators.** **Phase 4bn-G does not run strategy research.** **Phase
4bn-G does not define a strategy.** **Phase 4bn-G does not generate trade
signals.** **Phase 4bn-G does not simulate PnL.** **Phase 4bn-G does not
run backtests.** **Phase 4bn-G does not authorize acquisition.** **Phase
4bn-G does not authorize storage migration.** **Phase 4bn-G does not create
a v003 dataset.** **Phase 4bn-G does not create a database.** **Phase 4bn-G
does not compact Parquet.** **Phase 4bn-G does not modify dataset layout.**
**Phase 4bn-G does not call any public, authenticated, or private
endpoint.** **Phase 4bn-G does not open any WebSocket or user stream.**
**Phase 4bn-G does not use credentials, `.env`, `.mcp.json`, MCP, or
Graphify.** **Phase 4bn-G does not mutate any manifest.** **Phase 4bn-G
does not mutate any successor-state artefact.** **Phase 4bn-G does not
commit `data/microstructure`.** **Phase 4bn-G does not commit
`data/research`.** **Phase 4bn-G does not authorize Phase 4bn-H, Phase 5,
paper / shadow, live-readiness, deployment, exchange-write, production
keys, or any successor phase.** **Recommended state remains paused.**

## Branch and base

- **Branch:** `phase-4bn-g/combined-data-expansion-storage-scaling-scoping`.
- **Base `main` SHA:** `c9a2df0eb3e76a91b72c3687f3767b931b458fe2` (Phase
  4bn-F SHA-finalization commit `docs(phase-4bn-f): finalize merge closeout
  shas`; pre-branch `main == origin/main` verified in sync).

## Tracked changes

- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_combined-data-expansion-storage-scaling-scoping.md`
  (added; this phase's implementation report; 19 sections + 3 appendices).
- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_closeout.md`
  (added; this closeout).
- `docs/00-meta/current-project-state.md`
  (narrow update: Phase 4bn-G paragraph + new "Current phase:" block; prior
  Phase 4bn-A / 4bn-B / 4bn-C / 4bn-D / 4bn-E / 4bn-F paragraphs and prior
  "Current phase:" blocks preserved as labelled historical context).

No other tracked file was created, modified, or deleted. `pyproject.toml`,
`README.md`, `.gitignore`, MCP files, manifests, sidecars, gate reports,
successor-state artefacts, and existing source / test / script files were
all left byte-identical.

## Local gitignored outputs

**None.** Phase 4bn-G is a docs-only / design-only / scoping-only phase
and produces no local artefact under `data/microstructure/` or
`data/research/`. No CSV, no JSON, no parquet, no manifest, no sidecar,
no gate report, no successor-state file, and no database file was
created. No diagnostic, ML, simulation, backtest, or acquisition kernel
was invoked.

## Decision

`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Phase 4bn-G crystallises the Phase 4bn-F recommendation into a concrete
data-expansion requirements framework (memo §8 — 24 requirements covering
calendar coverage, window shape, volatility / trend / activity / funding /
intraday / event regimes, symbol / horizon scope, split allocation,
test-holdout preservation, label / feature family preservation,
cost-commensurability under §11.6, high-confidence calibration failure
from Phase 4bn-C, reproducibility from public Binance sources, sidecar /
manifest implications, disk footprint, derivation time, query load, and
exact stop conditions), a concrete storage-scaling architecture
comparison (memo §10 — six storage options scored on what-they-solve /
disk impact / query impact / reproducibility / sidecar / migration risk /
recommendation), a coupled data-and-storage decision matrix (memo §11 —
7 × 6 grid classifying every combination as compatible, compatible but
deferred, not recommended, or structurally rejected), required
pre-acquisition gates (memo §13 — 14 gates), required pre-storage-
migration gates (memo §14 — 10 gates), a required non-authorization
envelope for any successor (memo §15 — 13 constraints), and a single
recommended path: a future docs-only acquisition-readiness memo that
keeps Parquet canonical (Storage A) and DuckDB in place (Storage C) as
the preferred non-invasive query layer, while deferring any DuckDB
database-cache (Storage D) or Parquet-compaction (Storage B) decision
until there is a concrete acquisition envelope. **The successor is
recommended only and is not authorized.** A separate operator
authorization is required for any executable follow-up. The operator may
equivalently remain paused, request a merge prompt for Phase 4bn-G,
reject further ML-baseline successors and close the ML arc, separately
authorize only a future docs-only storage-architecture decision memo,
or separately authorize a future docs-only combined acquisition-
readiness + storage-decision memo; Phase 4bn-G does not foreclose any of
these alternatives.

## Phase 4bn-F decision carried forward

`RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— Phase 4bn-F recorded the v002 data-sufficiency / representativeness
scoping decision, defined seven candidate expansion shapes at design
level only, discussed storage-scaling questions at design level only, and
recommended the combined memo (this phase) as the cleanest non-paused
option because longer-history microstructure acquisition and storage
layout are tightly coupled. Phase 4bn-G is the chosen combined-memo
execution and inherits the Phase 4bn-F recommendation boundary verbatim.

## Phase 4bn-E / 4bn-D / 4bn-C / 4bn-B interpretation carried forward

- **Phase 4bn-E (verbatim):** `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`
  — partially ruled out gross train-vs-validation feature-distribution
  drift at the measurement-frame level only (31 low / 13 moderate /
  0 high / 1 undefined drift; highest absolute standardized mean delta
  0.330; highest missing-rate delta ≈ 6e-06; 13 moderate-drift features
  cluster on count and mean-quantity dimensions, signed consistently
  count-up / mean-quantity-down between train and validation).
- **Phase 4bn-D (verbatim):**
  `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-C (verbatim):** `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`
  — interpreted Phase 4bn-B evidence as small descriptive lift with a
  severe high-confidence calibration tail and §11.6 cost-commensurability
  fractions consistent with 80 – 95 % of validation rows being below the
  round-trip cost.
- **Phase 4bn-B (verbatim):** `RECORD_EVIDENCE_ONLY` — descriptive
  ML-baseline evidence on train / validation only; test holdout sealed
  (`test_rows_loaded: 0`); no model selected as best; no feature ranked
  or selected; no hyperparameter or threshold tuned; no strategy / signal
  / PnL / backtest.

Phase 4bn-G inherits all four decisions verbatim and softens none of
them.

## Validation summary

Phase 4bn-G is a docs-only phase. Its validation is limited to
documentation / repository-state checks:

- `git status --short` — only expected tracked Phase 4bn-G files plus
  pre-existing untracked `.claude/scheduled_tasks.lock` and pre-existing
  gitignored `data/research/` + `data/microstructure/` entries.
- `git diff --check` — clean (no whitespace errors).
- `git diff -- docs/00-meta/current-project-state.md docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_combined-data-expansion-storage-scaling-scoping.md docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_closeout.md`
  reviewed pre-commit: the only tracked changes are the new combined
  data-expansion + storage-scaling scoping memo, the new closeout, and
  the narrow `current-project-state.md` Phase 4bn-G paragraph + new
  Current-phase block addition.
- No code, no tests, no scripts, no configuration, no manifests, no
  sidecars, no gate reports, no successor-state artefacts, and no
  `data/microstructure/` or `data/research/` artefacts were created,
  modified, or accessed for mutation.
- No ML script was run; no diagnostics script was run; no backtest script
  was run; no acquisition script was run; the Phase 4bn-E runner was not
  invoked; the Phase 4bn-B runner was not invoked; no local gitignored
  output was inspected.
- The test holdout was not used in any way; the
  `iter_partitions(split="test", ...)` raise pattern remains in force in
  the unchanged Phase 4bn-B implementation; Phase 4bn-G never opened any
  test row.
- Repository tooling (ruff, mypy, pytest) is not invoked for a docs-only
  scoping memo that creates no code surface and modifies no code; the
  Phase 4bn-F precedent recorded the same omission rationale (whole-repo
  mypy baseline carries pre-existing `Missing type parameters for generic
  type "ndarray"` warnings that are unrelated to a docs-only phase); the
  diff-check and status-check are the relevant validation surface for
  this docs-only Tier 1 scoping memo.

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
  hashed by Phase 4bn-G;
- no ML model trained / scored; no prediction generated; no reusable
  split mask materialised; no model binary persisted; no row-level
  prediction persisted;
- no feature ranked, selected, pruned, or engineered;
- no hyperparameter or threshold tuned;
- no calibrator fitted;
- no probability-to-signal conversion;
- no strategy defined or run; no signal generated; no PnL simulated; no
  backtest run; no walk-forward optimization;
- test holdout not used for any reason;
- no data acquired; no public / authenticated / private endpoint called;
  no Binance API called; no WebSocket / user stream opened; no
  credential / `.env` / `.mcp.json` / MCP / Graphify used;
- no v003 dataset created; no new dataset family created; no new label /
  feature / horizon / symbol acquisition; no longer-history acquisition;
  no multiple-window acquisition; no mark-price / spot / cross-venue /
  order-book / additional-aggTrades acquisition;
- no storage migration; no database created; no Parquet compaction; no
  DuckDB database file created; no SQLite database created; no
  partitioning policy changed; no compression policy changed; no dataset
  layout changed;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0
  amendment; no successor authorized.

## Recommended state

**Remain paused.** Phase 4bn-G is branch-complete only by this work; not
merged into main; not project-complete. Per the
`phase-workflow-standard.md` rule, Phase 4bn-G is NOT project-complete
until a separately authorized merge phase records its merge-closeout on
`main` per `merge-closeout-standard.md` (Tier 1). **No next phase
authorized.** The operator may equivalently:

- remain paused (default);
- request a merge prompt for Phase 4bn-G so the combined data-expansion
  + storage-scaling scoping decision becomes project-complete on `main`;
- reject further ML-baseline successors and close the ML arc;
- separately authorize a future docs-only acquisition-readiness memo
  (Phase 4bn-G's recommendation; subject to separate operator
  authorization; focused on a specific expansion shape, most plausibly
  Option B — longer continuous BTCUSDT, keeping Parquet canonical and
  DuckDB in place as the preferred non-invasive query layer);
- separately authorize a future docs-only storage-architecture decision
  memo only;
- separately authorize a future docs-only combined acquisition-readiness
  + storage-decision memo (one level lower in abstraction than Phase
  4bn-G; same recommendation pattern; same docs-only constraints).

**No acquisition / paper / shadow / live / exchange-write option is
valid from this state.**

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side /
round-trip 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 + post-null cooldown + cooled-down
families list + memo template; Phase 4al refined no-rescue + §13
boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path
policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine
reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt
context-management standard; Phase 4bm-D-P1 lightweight Claude Code
workspace standard) is preserved verbatim.

Phase 4 canonical remains unauthorized. Phase 4bn-G merge phase / Phase
4bn-H / any further successor (under any name performing the recommended
docs-only acquisition-readiness memo, the separately-recommended
docs-only storage-architecture decision memo, the docs-only combined
acquisition-readiness + storage-decision memo, any acquisition phase,
any storage-migration phase, any database-creation phase, any
v003-creation phase, any Parquet-compaction phase, any ML
implementation, any model training, any model selection through results,
any feature ranking, any feature selection, any hyperparameter tuning,
any threshold tuning, any strategy, any signals, any PnL, any backtest,
any paper / shadow / live-readiness / deployment / exchange-write /
production-key / Phase 5 / any successor phase) remains unauthorized.
