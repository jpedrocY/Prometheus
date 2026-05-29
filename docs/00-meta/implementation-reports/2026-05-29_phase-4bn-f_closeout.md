# Phase 4bn-F — Closeout

**Phase 4bn-F is branch-complete only by this work; not merged into main;
not project-complete.** Phase 4bn-F is the docs-only / design-only /
scoping-only V002 data-sufficiency / representativeness scoping memo
authorised by the operator following the Phase 4bn-E recommendation that
listed "separately authorize a future docs-only data-sufficiency /
representativeness scoping memo" as one of several equivalent operator
options. The phase evaluates whether the current 3-month v002 microstructure
ML-baseline evidence window is sufficient for future ML-baseline
interpretation, whether it may be regime-specific or outlier-like, and
what a future data-expansion decision would need to prove before any
acquisition is authorized; it also discusses storage-scaling questions at
design level only. **Phase 4bn-F is a docs-only / design-only / scoping-
only v002 data-sufficiency / representativeness scoping memo.** **Phase
4bn-F does not acquire data.** **Phase 4bn-F does not run diagnostics.**
**Phase 4bn-F does not run ML.** **Phase 4bn-F does not train models.**
**Phase 4bn-F does not score models.** **Phase 4bn-F does not generate
predictions.** **Phase 4bn-F does not inspect the test holdout.** **Phase
4bn-F does not use the sealed test split.** **Phase 4bn-F does not rank
features.** **Phase 4bn-F does not select features.** **Phase 4bn-F does
not prune features.** **Phase 4bn-F does not engineer features.** **Phase
4bn-F does not tune hyperparameters.** **Phase 4bn-F does not tune
thresholds.** **Phase 4bn-F does not fit calibrators.** **Phase 4bn-F does
not run strategy research.** **Phase 4bn-F does not define a strategy.**
**Phase 4bn-F does not generate trade signals.** **Phase 4bn-F does not
simulate PnL.** **Phase 4bn-F does not run backtests.** **Phase 4bn-F does
not authorize acquisition.** **Phase 4bn-F does not authorize storage
migration.** **Phase 4bn-F does not create a v003 dataset.** **Phase 4bn-F
does not create a database.** **Phase 4bn-F does not compact Parquet.**
**Phase 4bn-F does not modify dataset layout.** **Phase 4bn-F does not call
any public, authenticated, or private endpoint.** **Phase 4bn-F does not
open any WebSocket or user stream.** **Phase 4bn-F does not use credentials,
`.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-F does not mutate any
manifest.** **Phase 4bn-F does not mutate any successor-state artefact.**
**Phase 4bn-F does not commit `data/microstructure`.** **Phase 4bn-F does
not commit `data/research`.** **Phase 4bn-F does not authorize Phase 4bn-G,
Phase 5, paper / shadow, live-readiness, deployment, exchange-write,
production keys, or any successor phase.** **Recommended state remains
paused.**

## Branch and base

- **Branch:** `phase-4bn-f/v002-data-sufficiency-representativeness-scoping`.
- **Base `main` SHA:** `8fa219c83326c79ffb6406cc1904440fdc63c376` (Phase
  4bn-E SHA-finalization commit `docs(phase-4bn-e): finalize merge closeout
  shas`; pre-branch `main == origin/main` verified in sync).

## Tracked changes

- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_v002-data-sufficiency-representativeness-scoping.md`
  (added; this phase's implementation report; 20 sections).
- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_closeout.md`
  (added; this closeout).
- `docs/00-meta/current-project-state.md`
  (narrow update: Phase 4bn-F paragraph + new "Current phase:" block;
  prior Phase 4bn-A / 4bn-B / 4bn-C / 4bn-D / 4bn-E paragraphs and prior
  "Current phase:" blocks preserved as labelled historical context).

No other tracked file was created, modified, or deleted. `pyproject.toml`,
`README.md`, `.gitignore`, MCP files, manifests, sidecars, gate reports,
successor-state artefacts, and existing source / test / script files were
all left byte-identical.

## Local gitignored outputs

**None.** Phase 4bn-F is a docs-only / design-only / scoping-only phase
and produces no local artefact under `data/microstructure/` or
`data/research/`. No CSV, no JSON, no parquet, no manifest, no sidecar,
no gate report, no successor-state file, and no database file was created.
No diagnostic, ML, simulation, backtest, or acquisition kernel was invoked.

## Decision

`RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Phase 4bn-F evaluates the operator's standing future data-sufficiency /
representativeness concern about the 90-day v002 microstructure ML-baseline
envelope and the standing future storage-architecture concern about
Parquet / DuckDB / database tradeoffs, and recommends that any future work
combine those two questions into a single docs-only / design-only /
scoping-only memo because longer-history microstructure acquisition and
storage layout are tightly coupled. **The successor is recommended only
and is not authorized.** A separate operator authorization is required
for any executable follow-up. The operator may equivalently remain paused,
request a merge prompt for Phase 4bn-F, reject further ML-baseline
successors and close the ML arc, separately authorize only a future
docs-only data-expansion requirements memo, or separately authorize only
a future docs-only storage-scaling architecture memo; Phase 4bn-F does
not foreclose any of these alternatives.

## Phase 4bn-E decision carried forward

`RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED` — Phase 4bn-E executed
the bounded descriptive C-D candidate (train-vs-validation feature drift
diagnostics) and produced descriptive feature-drift evidence (31 low / 13
moderate / 0 high / 1 undefined drift classification; highest absolute
standardized mean delta 0.330; highest absolute missing-rate delta ≈ 6e-06).
Phase 4bn-E partially ruled out gross feature-distribution drift at the
measurement-frame level only; it did not address regime / volatility /
cost-commensurability / calendar-coverage / outlier questions. Phase 4bn-F
inherits this boundary without softening it.

## Phase 4bn-D scoping decision carried forward

`RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— Phase 4bn-D scoped six bounded ML-baseline expansion candidates at
design level only and recommended the C-D candidate as one of three
allowable bounded implementation candidates. Phase 4bn-F does not revisit
the six bounded ML-baseline expansion candidates; it addresses the
operator's standing future data-sufficiency / representativeness concern
that Phase 4bn-D / 4bn-E recorded as a non-authorizing note.

## Phase 4bn-C interpretation carried forward

`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` — Phase 4bn-C
interpreted the Phase 4bn-B `RECORD_EVIDENCE_ONLY` result and surfaced
twelve forensic hypotheses for the weak baseline-vs-prior separation.
Phase 4bn-F preserves the corrected interpretation of Phase 4bn-B evidence
verbatim (flat-class underrepresented; near-balanced binary in practice;
small but reproducible linear lift at 15s; well-calibrated dominant 0.5 –
0.6 confidence bin; severely over-confident 0.6 – 1.0 tail; persistence
uncalibrated on log-loss / Brier; §11.6 cost-commensurability fractions
per horizon; no overfitting at the measurement level; test holdout sealed
with `test_rows_loaded: 0`).

## Phase 4bn-B decision carried forward

`RECORD_EVIDENCE_ONLY` — Phase 4bn-B implemented exactly the Phase 4bn-A
§9 – §20 design and produced descriptive ML-baseline evidence on train
and validation only; the test holdout is sealed (`test_rows_loaded: 0`);
no model was selected as best; no feature was ranked or selected; no
hyperparameter or threshold was tuned; no strategy / signal / PnL /
backtest exists. Phase 4bn-F preserves every Phase 4bn-B boundary verbatim.

## Validation summary

Phase 4bn-F is a docs-only phase. Its validation is limited to
documentation / repository-state checks:

- `git status --short` — only expected tracked Phase 4bn-F files plus
  pre-existing untracked `.claude/scheduled_tasks.lock` and pre-existing
  gitignored `data/research/` + `data/microstructure/` entries.
- `git diff --check` — clean (no whitespace errors).
- `git diff -- docs/00-meta/current-project-state.md docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_v002-data-sufficiency-representativeness-scoping.md docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_closeout.md`
  reviewed pre-commit: the only tracked changes are the new
  data-sufficiency scoping memo, the new closeout, and the narrow
  `current-project-state.md` Phase 4bn-F paragraph + new Current-phase
  block addition.
- No code, no tests, no scripts, no configuration, no manifests, no
  sidecars, no gate reports, no successor-state artefacts, and no
  `data/microstructure/` or `data/research/` artefacts were created,
  modified, or accessed for mutation.
- No ML script was run; no diagnostics script was run; no backtest script
  was run; no acquisition script was run; the Phase 4bn-E runner was not
  invoked; no local gitignored output was inspected.
- The test holdout was not used in any way; the
  `iter_partitions(split="test", ...)` raise pattern remains in force in
  the unchanged Phase 4bn-B implementation; Phase 4bn-F never opened any
  test row.
- Repository tooling (ruff, mypy, pytest) is not invoked for a docs-only
  scoping memo that creates no code surface and modifies no code; running
  the whole-repo lint / type / test suites for this phase would produce
  the same baseline output as the pre-branch `main` state (Phase 4bn-E
  recorded that whole-repo mypy baseline carries pre-existing
  `Missing type parameters for generic type "ndarray"` warnings that are
  unrelated to a docs-only phase). Running them here is not required by
  the tier model for a docs-only Tier 1 scoping memo and is omitted; the
  diff-check and status-check are the relevant validation surface.

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
- no prior Phase 4bn-B / 4bn-E local output mutated, read, or hashed by
  Phase 4bn-F;
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
- no retained verdict revised; no project lock loosened; no M0 amendment;
  no successor authorized.

## Recommended state

**Remain paused.** Phase 4bn-F is branch-complete only by this work; not
merged into main; not project-complete. Per the `phase-workflow-standard.md`
rule, Phase 4bn-F is NOT project-complete until a separately authorized
merge phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1). **No next phase authorized.** The
operator may equivalently:

- remain paused (default);
- request a merge prompt for Phase 4bn-F so the data-sufficiency scoping
  decision becomes project-complete on `main`;
- reject further ML-baseline successors and close the ML arc;
- separately authorize a future docs-only combined data-expansion +
  storage-scaling scoping memo (Phase 4bn-F's recommendation; subject to
  separate operator authorization);
- separately authorize a future docs-only data-expansion requirements
  memo only;
- separately authorize a future docs-only storage-scaling architecture
  memo only.

**No acquisition / paper / shadow / live / exchange-write option is valid
from this state.**

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side /
round-trip 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase
3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v;
Phase 4w; Phase 4ak M0 + post-null cooldown + cooled-down families list
+ memo template; Phase 4al refined no-rescue + §13 boundary + §14
hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant
(never invoked); Phase 4bb-F canonical path policy; Phase 4bl-F four-tier
risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks;
Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1
lightweight Claude Code workspace standard) is preserved verbatim.

Phase 4 canonical remains unauthorized. Phase 4bn-F merge phase / Phase
4bn-G / any further successor (under any name performing the recommended
combined data-expansion + storage-scaling scoping memo, the separately-
recommended data-expansion-only or storage-scaling-only memos, any
acquisition phase, any storage-migration phase, any database-creation
phase, any v003-creation phase, any ML implementation, any model training,
any model selection through results, any feature ranking, any feature
selection, any hyperparameter tuning, any threshold tuning, any strategy,
any signals, any PnL, any backtest, any paper / shadow / live-readiness /
deployment / exchange-write / production-key / Phase 5 / any successor
phase) remains unauthorized.
