# Phase 4bn-J-R1 — Closeout

**Phase 4bn-J-R1 is branch-complete only by this work; not merged into
main; not project-complete.** Phase 4bn-J-R1 is a docs-only /
governance-only / amendment-only **Tier 1 Full Phase** (per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3) that records
the workspace relocation from the `C:` drive to the `D:` drive, intakes
and preserves the Phase 4bn-J stop report as tracked documentation, and
amends the Phase 4bn-I disk-footprint cap as **raw-only** for the
acquisition retry only. It authorizes nothing executable.

**Phase 4bn-J-R1 does not acquire data. Does not call any public,
Binance, authenticated, or private endpoint. Does not open any WebSocket
or user stream. Does not write acquisition code. Does not modify any
script. Does not run acquisition. Does not create any manifest. Does not
create any sidecar except normal tracked Git docs files. Does not create
any data/microstructure or data/research artefact. Does not read any
local parquet / data/microstructure / data/research output. Does not run
ML. Does not train or score models. Does not generate predictions. Does
not run diagnostics. Does not run backtests. Does not migrate storage.
Does not create any database. Does not compact Parquet. Does not create
v003. Does not mutate any manifest, sidecar, gate report, or
successor-state artefact. Does not inspect or use the sealed test split.
Does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify. Does
not authorize Phase 4bn-J-R2, Phase 5, paper / shadow, live-readiness,
deployment, exchange-write, production keys, or any successor phase.
Recommended state remains paused.**

## Branch and base

- **Branch:** `phase-4bn-j-r1/workspace-relocation-raw-cap-amendment`.
- **Base `main` SHA:** `27dbc5723f3f068c34663ec57cd85a0e6b42f501`
  (`docs(phase-4bn-i): finalize merge closeout shas`; pre-branch
  `main == origin/main == HEAD` verified in sync; Phase 4bn-I
  merge-closeout `5aed510`, merge `4733d90`, and branch `a513c4f` all
  present on `main`).
- **Active local repo path:** `D:\Prometheus` (relocated from
  `C:\Prometheus`).
- **Active Claude Code lightweight workspace:**
  `D:\ClaudeRuns\prometheus-light` (relocated from
  `C:\ClaudeRuns\prometheus-light`).
- **GitHub remote:** `origin` →
  `https://github.com/jpedrocY/Prometheus.git` (fetch + push), verified
  intact and not re-pointed.

## Tracked changes

- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j_acquisition-stop-report.md`
  (added / preserved; the Phase 4bn-J **stop report**, previously
  untracked, now committed as tracked documentation by this amendment
  phase — **stop report, not a closeout**; preserved byte-for-byte as
  written by the stopped attempt).
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r1_workspace-relocation-raw-cap-amendment.md`
  (added; this phase's amendment memo; 17 sections).
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r1_closeout.md`
  (added; this closeout).
- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4bn-J-R1 prose paragraph + new
  `Current phase:` block; prior Phase 4bn-A … 4bn-I paragraphs and prior
  `Current phase:` blocks preserved as labelled historical context).

No other tracked file was created, modified, or deleted. `pyproject.toml`,
`README.md`, `.gitignore`, MCP files, manifests, sidecars, gate reports,
successor-state artefacts, existing source / test / script files, and
the `docs/00-meta/process/claude-code-lightweight-workspace-standard.md`
process standard were all left byte-identical. (The lightweight-workspace
standard was deliberately **not** modified: it was not named in this
phase's allowed tracked files, and its own §15 change-control requires a
phase that names it; a separate §15-compliant process-doc update phase is
recommended in the amendment memo §16 to refresh its `C:` path strings.)

## Local gitignored outputs

**None.** Phase 4bn-J-R1 is a docs-only / governance-only /
amendment-only phase and produces no local artefact under
`data/microstructure/` or `data/research/`. No CSV, no JSON, no parquet,
no manifest, no sidecar, no gate report, no successor-state file, and no
database file was created. No diagnostic, ML, simulation, backtest, or
acquisition kernel was invoked. The expected untracked transient
`.claude/scheduled_tasks.lock` was present and was not committed.

## Decision

`RECOMMEND_AUTHORIZE_REVISED_ACQUISITION_ONLY_RETRY__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

The stopped Phase 4bn-J attempt found that source policy passed and that
the only binding issue was an unrealistically low, scope-confused disk
cap. The repository is now on `D:\Prometheus` with ~1.25 TB free on
`D:`. The cap is amended as **raw-only** — **10 GiB warning / 25 GiB
hard** additional local raw acquisition footprint — for the
BTCUSDT / Binance USDⓈ-M futures / aggTrades / 2024-03-01..2024-11-30
new pre-v002 segment retry only, under the existing 2024-03-01..
2025-02-28 envelope. The runtime cap (2 h warning / 4 h hard) and every
other Phase 4bn-I boundary are unchanged. A revised acquisition-only
retry, bounded exactly by the amendment memo §7–§14, is recommended as
the cleanest non-paused option **but is not authorized by this
amendment.** No successor is authorized from inside Phase 4bn-J-R1.

## Old vs new disk cap (acquisition retry only)

- **Old (Phase 4bn-I, mixed raw + derived scope):** 3 GiB warning /
  5 GiB hard additional local footprint.
- **New (this amendment, raw-only scope, retry only):** 10 GiB warning /
  25 GiB hard additional local **raw** acquisition footprint.
- **Runtime cap (unchanged):** 2 h warning / 4 h hard total wall-clock.
- The amendment applies **only** to the raw-only acquisition retry. It
  does **not** apply to derived normalized / feature / label phases,
  which need a **separate derived-stack disk budget** (planning warning
  only: ~150–250 GiB plausible, ~300 GiB comfortable; exact cap set in
  the future derivation / gate phase, not here).

## Phase 4bn-J stop-report preservation

The Phase 4bn-J stop report is preserved as **tracked documentation, not
a closeout**. Phase 4bn-J **stopped before acquisition**; is **not**
branch-complete; is **not** merged; is **not** committed (by the stopped
attempt); is **not** project-complete. The stopped attempt downloaded no
archive, acquired no data, created no data/microstructure or
data/research artefact, created no manifest, created no sidecar, wrote no
acquisition code, modified no script, made no `current-project-state.md`
update, and made no commit. This amendment phase (Phase 4bn-J-R1) is the
first phase to commit the stop report, and commits it byte-for-byte as
written.

## Phase 4bn-I / 4bn-H / 4bn-G … decisions carried forward

- **Phase 4bn-I (verbatim):**
  `RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  — the docs-only acquisition execution plan; its envelope, source-policy
  confirmation requirement, sealed-test preservation, storage posture,
  manifest / sidecar policy, runtime cap, and 25 fail-closed stop
  conditions are carried forward intact; only its disk cap is amended
  (raw-only, retry only).
- **Phase 4bn-H (verbatim):**
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-G (verbatim):**
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-F (verbatim):**
  `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-E (verbatim):** `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`.
- **Phase 4bn-D (verbatim):**
  `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-C (verbatim):** `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.
- **Phase 4bn-B (verbatim):** `RECORD_EVIDENCE_ONLY` — test holdout
  sealed (`test_rows_loaded: 0`).

Phase 4bn-J-R1 inherits all of these verbatim and softens none of them.
None of Phase 4bn-A through Phase 4bn-J-R1 establishes edge,
profitability, tradability, strategy-readiness, signal-readiness,
paper / shadow readiness, or live-readiness.

## Validation summary

Phase 4bn-J-R1 is a docs-only amendment phase. Its validation is limited
to documentation / repository-state checks appropriate for a docs-only
Tier 1 phase:

- `git status --short` — only the four tracked Phase 4bn-J-R1 files (the
  preserved stop report, the amendment memo, this closeout, and the
  narrow `current-project-state.md` update) plus the pre-existing
  untracked `.claude/scheduled_tasks.lock` and the pre-existing
  gitignored `data/microstructure/` + `data/research/` namespaces.
- `git diff --check` — clean (no whitespace errors).
- `git diff` over the four tracked files reviewed pre-commit: the only
  tracked changes are the four named files.
- `git remote -v` — `origin` →
  `https://github.com/jpedrocY/Prometheus.git` (fetch + push), intact.
- `git rev-parse HEAD` / `main` / `origin/main` recorded.
- No code, no tests, no scripts, no configuration, no manifests, no
  sidecars, no gate reports, no successor-state artefacts, and no
  `data/microstructure/` or `data/research/` artefacts were created,
  modified, read, hashed, or accessed for mutation.
- No ML / diagnostics / backtest / acquisition script was run; no
  acquisition kernel invoked; no local gitignored output inspected.
- The test holdout was not used in any way; the
  `iter_partitions(split="test", ...)` raise pattern remains in force in
  the unchanged Phase 4bn-B implementation; this phase opened no test
  row.
- Repository tooling (ruff, mypy, pytest) is not invoked for a docs-only
  amendment phase that creates no code surface and modifies no code; the
  Phase 4bn-I / 4bn-H / 4bn-G precedents recorded the same omission
  rationale; the diff-check, status-check, remote check, and SHA checks
  are the relevant validation surface for this docs-only Tier 1 phase.

## Boundary confirmations

- no source code modified;
- no test modified;
- no committed script modified (no script modification was required to
  preserve the stop report as docs);
- no config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file
  modified;
- no `docs/00-meta/process/claude-code-lightweight-workspace-standard.md`
  modification (deliberately deferred to a separate §15-compliant phase);
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
- no prior Phase 4bn-* / 4bm-* local output mutated, read, or hashed;
- no archive downloaded; no data acquired; no public / Binance /
  authenticated / private endpoint called; no `data.binance.vision`
  contacted; no WebSocket / user stream opened;
- no acquisition code written; no new acquisition script created;
- no ML model trained / scored; no prediction generated; no feature
  ranked / selected / pruned / engineered; no hyperparameter or threshold
  tuned; no calibrator fitted; no strategy defined / run; no signal
  generated; no PnL simulated; no backtest run;
- test holdout not used for any reason; sealed v002 split
  2025-02-14..2025-02-28 untouched;
- no v003 dataset created; no new dataset family created; no new label /
  feature / horizon / symbol acquisition; no mark-price / spot /
  cross-venue / order-book / tick acquisition;
- no storage migration; no database created; no Parquet compaction; no
  `.duckdb` / `.sqlite` file created; no partitioning / compression /
  dataset-layout change;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0
  amendment; no successor authorized.

## Recommended state

**Remain paused.** Phase 4bn-J-R1 is branch-complete only by this work;
not merged into main; not project-complete. Per the
`phase-workflow-standard.md` rule, it is NOT project-complete until a
separately authorized merge phase records its merge-closeout on `main`
per `merge-closeout-standard.md` (Tier 1). **No next phase authorized.**
The operator may equivalently:

- remain paused (default);
- request a merge prompt for Phase 4bn-J-R1;
- separately authorize the revised acquisition-only retry (the
  recommendation; bounded exactly by the amendment memo §7–§14;
  raw-only 10 GiB / 25 GiB cap; 2 h / 4 h runtime cap; BTCUSDT
  aggTrades 2024-03-01..2024-11-30; v002 terminal window and sealed
  split untouched; Parquet canonical; no v003 / ETHUSDT / mark-price /
  spot / cross-venue / order-book / tick; must remain acquisition-only);
- separately authorize a docs-only source-policy documentation memo;
- separately authorize a docs-only derived-stack storage-budget memo;
- separately authorize a docs-only process-doc update phase that names
  `claude-code-lightweight-workspace-standard.md` in its allowed tracked
  files and refreshes its `C:` path strings to `D:`;
- reject further ML-baseline successors and close the ML arc.

**No acquisition / ML / diagnostics / strategy / PnL / backtest /
storage-migration / database-creation / Parquet-compaction / v003 /
paper / shadow / live / exchange-write option is valid from this state
unless separately authorized after this branch is merged.**

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side /
round-trip 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 + post-null cooldown + cooled-down
families list + memo template; Phase 4al refined no-rescue + §13
boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path +
sidecar policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine
reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt
context-management standard; Phase 4bm-D-P1 lightweight Claude Code
workspace standard — principle preserved; its `C:` example path strings
superseded by this memo for the active convention pending a separate
§15-compliant update phase) is preserved verbatim.

Phase 4 canonical remains unauthorized. The Phase 4bn-J-R1 merge phase /
the recommended revised acquisition-only retry / Phase 4bn-J / Phase
4bn-J-R2 / any source-policy documentation memo / any derived-stack
storage-budget memo / any process-doc update phase / any acquisition
phase / any storage-migration phase / any database-creation phase / any
v003-creation phase / any Parquet-compaction phase / any ML
implementation / any diagnostics implementation / any strategy / any
signals / any PnL / any backtest / any paper / shadow / live-readiness /
deployment / exchange-write / production-key / any Phase 5 / any
successor phase remains unauthorized.
