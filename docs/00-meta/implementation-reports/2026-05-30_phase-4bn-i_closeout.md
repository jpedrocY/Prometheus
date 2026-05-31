# Phase 4bn-I — Closeout

**Phase 4bn-I is branch-complete only by this work; not merged into main;
not project-complete.** Phase 4bn-I is the docs-only / design-only /
scoping-only acquisition **execution plan** authorised by the operator
following the Phase 4bn-H recommendation
`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
The phase takes the Phase 4bn-H acquisition-readiness recommendation one
level lower of abstraction by pre-declaring the **exact** Option C
envelope (12-month continuous BTCUSDT Binance USDⓈ-M futures aggTrades
history), the exact UTC calendar range (2024-03-01 .. 2025-02-28
inclusive UTC), the exact canonical path layout, the exact
source-endpoint policy confirmation requirement, the exact disk-footprint
cap (5 GiB hard / 3 GiB warning), the exact derivation-time cap (4 hours
hard / 2 hours warning), the exact manifest and sidecar policy, the exact
sealed-test preservation language, the exact new-holdout policy, the
exact 25 fail-closed stop conditions, the exact acquisition-phase
non-authorization envelope, and the exact post-acquisition successor
chain. The phase authorises nothing executable.

**Phase 4bn-I is a docs-only / design-only / scoping-only acquisition
execution plan.** **Phase 4bn-I does not acquire data.** **Phase 4bn-I
does not call public, Binance, authenticated, or private endpoints.**
**Phase 4bn-I does not migrate storage.** **Phase 4bn-I does not create
any database.** **Phase 4bn-I does not compact Parquet.** **Phase 4bn-I
does not create v003.** **Phase 4bn-I does not authorize acquisition.**
**Phase 4bn-I does not authorize any successor.** **Phase 4bn-I does not
read local parquets.** **Phase 4bn-I does not inspect local data.**
**Phase 4bn-I does not run diagnostics.** **Phase 4bn-I does not run
ML.** **Phase 4bn-I does not train models.** **Phase 4bn-I does not score
models.** **Phase 4bn-I does not generate predictions.** **Phase 4bn-I
does not inspect the test holdout.** **Phase 4bn-I does not use the
sealed test split.** **Phase 4bn-I does not rank features.** **Phase
4bn-I does not select features.** **Phase 4bn-I does not prune
features.** **Phase 4bn-I does not engineer features.** **Phase 4bn-I
does not tune hyperparameters.** **Phase 4bn-I does not tune
thresholds.** **Phase 4bn-I does not fit calibrators.** **Phase 4bn-I
does not run strategy research.** **Phase 4bn-I does not define a
strategy.** **Phase 4bn-I does not generate trade signals.** **Phase
4bn-I does not simulate PnL.** **Phase 4bn-I does not run backtests.**
**Phase 4bn-I does not modify dataset layout.** **Phase 4bn-I does not
open any WebSocket or user stream.** **Phase 4bn-I does not use
credentials, `.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-I does
not mutate any manifest.** **Phase 4bn-I does not mutate any
successor-state artefact.** **Phase 4bn-I does not commit
`data/microstructure`.** **Phase 4bn-I does not commit `data/research`.**
**Phase 4bn-I does not authorize Phase 4bn-J, Phase 5, paper / shadow,
live-readiness, deployment, exchange-write, production keys, or any
successor phase.** **Recommended state remains paused.**

## Branch and base

- **Branch:** `phase-4bn-i/docs-only-acquisition-execution-plan`.
- **Base `main` SHA:** `654befd236884c8c47cc062722ac74c794272d12` (Phase
  4bn-H SHA-finalization commit `docs(phase-4bn-h): finalize merge
  closeout shas`; pre-branch `main == origin/main` verified in sync;
  Phase 4bn-H merge commit `1aad93a983f6e4fdfefeef97503bfc9327bc2c14`,
  merge-closeout commit `55b011d96b9693f331c277ed874f28f84dc68200`, and
  branch commit `c1038f94e19b23bd883972e2fd1a7a5d88a7b3d3` all present on
  main).

## Tracked changes

- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_docs-only-acquisition-execution-plan.md`
  (added; this phase's implementation report; 22 sections + 3
  appendices).
- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_closeout.md`
  (added; this closeout).
- `docs/00-meta/current-project-state.md`
  (narrow update: Phase 4bn-I paragraph + new "Current phase:" block;
  prior Phase 4bn-A / 4bn-B / 4bn-C / 4bn-D / 4bn-E / 4bn-F / 4bn-G /
  4bn-H paragraphs and prior "Current phase:" blocks preserved as
  labelled historical context).

No other tracked file was created, modified, or deleted. `pyproject.toml`,
`README.md`, `.gitignore`, MCP files, manifests, sidecars, gate reports,
successor-state artefacts, and existing source / test / script files were
all left byte-identical.

## Local gitignored outputs

**None.** Phase 4bn-I is a docs-only / design-only / scoping-only phase
and produces no local artefact under `data/microstructure/` or
`data/research/`. No CSV, no JSON, no parquet, no manifest, no sidecar,
no gate report, no successor-state file, and no database file was
created. No diagnostic, ML, simulation, backtest, or acquisition kernel
was invoked.

## Decision

`RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Phase 4bn-I crystallises the Phase 4bn-H acquisition-readiness
recommendation into a concrete, exact acquisition execution plan for the
recommended Option C envelope: BTCUSDT-only Binance USDⓈ-M futures
aggTrades, 12-month continuous history over the exact UTC range
2024-03-01 .. 2025-02-28 inclusive (extending the existing 90-day v002
window backward and preserving the existing v002 sealed test split
2025-02-14 .. 2025-02-28 as terminal historical evidence); v002 feature
(45 columns) and label (3-class strict-sign at 15s / 60s) semantics
preserved; Parquet canonical; DuckDB querying Parquet in place as a
non-invasive query layer only; no DuckDB database cache; no Parquet
compaction; no SQLite research matrices; no ETHUSDT; no extra horizons;
no mark-price / spot / cross-venue / order-book / tick data; no v003; no
storage migration; no database creation. The plan pre-declares the exact
canonical `data/microstructure/<family>/` path layout; the exact
source-endpoint policy confirmation requirement (public Binance USDⓈ-M
bulk archives only, fail-closed on any divergence, source-policy memo
required if ambiguous — and the committed `historical-data-spec.md`
aggTrades-bulk-archive gap is flagged for the future phase to resolve);
the exact disk-footprint cap (5 GiB hard / 3 GiB warning, preflight +
runtime fail-closed); the exact derivation-time cap (4 hours hard / 2
hours warning, preflight + runtime fail-closed); the exact Phase 4bb-F
sidecar policy and manifest-immutability / `__vNNN` / non-eligible
manifest-start policy; the exact sealed-test preservation and
new-holdout policy; the exact 25 fail-closed stop conditions; the exact
acquisition-phase non-authorization envelope; and the exact
post-acquisition successor chain (acquisition merge-closeout → raw gate →
normalized gate → feature gate → label gate → successor-state recording →
new split / holdout policy memo → ML-baseline implementation plan →
diagnostics plan → no test-holdout use without a separate terminal
phase).

**The successor acquisition-only phase is recommended only and is not
authorized.** A separate operator authorization is required after this
branch is merged for any executable follow-up. The operator may
equivalently remain paused, request a merge prompt for Phase 4bn-I,
reject further ML-baseline successors and close the ML arc, separately
authorize a docs-only storage-architecture decision memo, or separately
authorize a docs-only holdout and split-policy memo; Phase 4bn-I does not
foreclose any of these alternatives.

## Phase 4bn-H decision carried forward

`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— Phase 4bn-H selected Option B as the candidate expansion shape,
compared calendar-coverage options A / B / C / D / E at design level
only, recommended Option C (12-month continuous BTCUSDT) as the cleanest
first-expansion coverage, preserved the Phase 4bn-G `A + F + C` storage
posture verbatim, defined 14 pre-acquisition gates and 13 stop
conditions, and recommended this docs-only acquisition execution plan.
Phase 4bn-I is the chosen acquisition execution plan and inherits the
Phase 4bn-H recommendation boundary verbatim.

## Phase 4bn-G / 4bn-F / 4bn-E / 4bn-D / 4bn-C / 4bn-B interpretation carried forward

- **Phase 4bn-G (verbatim):**
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-F (verbatim):**
  `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  — concluded the 90-day window is useful but not enough to prove broad
  sufficiency, insufficiency, representativeness, or outlier status;
  treated "outlier" as an unresolved risk, not a conclusion.
- **Phase 4bn-E (verbatim):** `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`
  — partially ruled out gross train-vs-validation feature-distribution
  drift at the measurement-frame level only.
- **Phase 4bn-D (verbatim):**
  `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-C (verbatim):** `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`
  — interpreted Phase 4bn-B evidence as small descriptive lift, not edge.
- **Phase 4bn-B (verbatim):** `RECORD_EVIDENCE_ONLY` — descriptive
  ML-baseline evidence on train / validation only; test holdout sealed
  (`test_rows_loaded: 0`).

Phase 4bn-I inherits all six decisions verbatim and softens none of
them.

## Validation summary

Phase 4bn-I is a docs-only phase. Its validation is limited to
documentation / repository-state checks:

- `git status --short` — only the expected tracked Phase 4bn-I files plus
  the pre-existing untracked `.claude/scheduled_tasks.lock` and
  pre-existing gitignored `data/research/` + `data/microstructure/`
  entries.
- `git diff --check` — clean (no whitespace errors).
- `git diff -- docs/00-meta/current-project-state.md docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_docs-only-acquisition-execution-plan.md docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_closeout.md`
  reviewed pre-commit: the only tracked changes are the new acquisition
  execution plan memo, the new closeout, and the narrow
  `current-project-state.md` Phase 4bn-I paragraph + new "Current phase:"
  block addition.
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
  the unchanged Phase 4bn-B implementation; Phase 4bn-I never opened any
  test row.
- Repository tooling (ruff, mypy, pytest) is not invoked for a docs-only
  scoping memo that creates no code surface and modifies no code; the
  Phase 4bn-H / 4bn-G / 4bn-F precedents recorded the same omission
  rationale; the diff-check and status-check are the relevant validation
  surface for this docs-only Tier 1 phase.

## Boundary confirmations

- no source code modified;
- no test modified;
- no committed script modified;
- no config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file
  modified;
- no `data/microstructure/` artefact committed;
- no `data/research/` artefact committed;
- no `data/microstructure/` artefact created, modified, moved, read, or
  hashed;
- no `data/research/` artefact created, modified, moved, read, or hashed;
- no local parquet / CSV / JSON output read or inspected;
- no manifest mutated; no `research_eligible` flipped; no
  `eligibility_gate_status` transitioned; no `chronological_split_policy`
  changed; no `diagnostics_authorized` / `ml_authorized` changed;
- no successor-state artefact mutated, created, moved, or accessed for
  mutation;
- no prior gate report mutated;
- no prior Phase 4bn-B / 4bn-E / 4bm-* local output mutated, read, or
  hashed by Phase 4bn-I;
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
- no data acquired; no public / Binance / authenticated / private
  endpoint called; no WebSocket / user stream opened; no credential /
  `.env` / `.mcp.json` / MCP / Graphify used;
- no v003 dataset created; no new dataset family created; no new label /
  feature / horizon / symbol acquisition; no longer-history acquisition;
  no mark-price / spot / cross-venue / order-book / tick / aggTrades
  acquisition;
- no storage migration; no database created; no Parquet compaction; no
  DuckDB database file created; no SQLite database created; no
  partitioning policy changed; no compression policy changed; no dataset
  layout changed;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0
  amendment; no successor authorized.

## Recommended state

**Remain paused.** Phase 4bn-I is branch-complete only by this work; not
merged into main; not project-complete. Per the
`phase-workflow-standard.md` rule, Phase 4bn-I is NOT project-complete
until a separately authorized merge phase records its merge-closeout on
`main` per `merge-closeout-standard.md` (Tier 1). **No next phase
authorized.** The operator may equivalently:

- remain paused (default);
- request a merge prompt for Phase 4bn-I so the acquisition execution
  plan becomes project-complete on `main`;
- reject further ML-baseline successors and close the ML arc;
- separately authorize the recommended acquisition-only phase (Phase
  4bn-I's recommendation; subject to separate operator authorization;
  bounded exactly by this plan — BTCUSDT aggTrades, 2024-03-01 ..
  2025-02-28, 5 GiB / 4 h caps, v002 semantics preserved, Parquet
  canonical, DuckDB-in-place, no ETHUSDT / v003 / compaction / database,
  sealed v002 test split untouched, 25 fail-closed stop conditions; must
  remain acquisition-only);
- separately authorize a docs-only storage-architecture decision memo;
- separately authorize a docs-only holdout and split-policy memo.

**No acquisition / storage migration / paper / shadow / live /
exchange-write option is valid from this state unless separately
authorized after this branch is merged.**

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side /
round-trip 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase
4v; Phase 4w; Phase 4ak M0 + post-null cooldown + cooled-down families
list + memo template; Phase 4al refined no-rescue + §13 boundary + §14
hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises
invariant (never invoked); Phase 4bb-F canonical path + sidecar policy;
Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable
non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management
standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard) is
preserved verbatim.

Phase 4 canonical remains unauthorized. Phase 4bn-I merge phase / the
recommended acquisition-only phase / Phase 4bn-J / any further successor
(under any name performing the recommended acquisition-only phase, any
docs-only storage-architecture decision memo, any docs-only holdout /
split-policy memo, any acquisition phase, any storage-migration phase,
any database-creation phase, any v003-creation phase, any
Parquet-compaction phase, any ML implementation, any model training, any
model selection through results, any feature ranking, any feature
selection, any hyperparameter tuning, any threshold tuning, any strategy,
any signals, any PnL, any backtest, any paper / shadow / live-readiness /
deployment / exchange-write / production-key / Phase 5 / any successor
phase) remains unauthorized.
