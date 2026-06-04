# Phase 4bn-Q — Closeout

**Phase 4bn-Q is branch-complete only by this work; not merged into main; not
project-complete.** Phase 4bn-Q is a docs-only / feature-derivation readiness /
feature execution planning / feature manifest and gate boundary-contract phase
(**Tier 1 Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md`
§3). It determines, from committed docs and committed tooling only, whether a
future feature-only execution phase can be safely authorized over the Phase
4bn-O / 4bn-P pre-v002 normalized BTCUSDT Binance USDⓈ-M futures aggTrades
segment, and what that future execution's contract must be. It authorizes
nothing executable and no successor.

**Phase 4bn-Q does not derive features, create feature artefacts, rerun
normalization, rerun any gate, acquire data, call any endpoint, read any local
raw/normalized/feature/label/research artefact, read the v002 terminal window,
touch the sealed test split, create a database, create `.duckdb`/`.sqlite`,
compact Parquet, migrate storage, create v003, mutate any manifest/sidecar/
gate-report/successor-state, flip `research_eligible`, transition
`eligibility_gate_status`, or authorize any successor.** Recommended state
remains paused.

## Branch and base

- **Branch:** `phase-4bn-q/feature-derivation-readiness-execution-plan`.
- **Base `main` SHA:** `b2b46de6a27311318b2e9d58f5de28e5137b28dd`
  (`docs(phase-4bn-p): finalize merge closeout shas`; pre-branch
  `main == origin/main == HEAD` verified in sync; Phase 4bn-P SHA-finalization
  `b2b46de`, merge-closeout `486c8c7`, merge `a10f255`, and branch `6e75711`
  all present on `main`).
- **Commit SHA:** recorded in §"Final git status / log / SHAs" after the single
  phase commit `docs(phase-4bn-q): plan feature derivation readiness`.
- **Active local repo path:** `D:\Prometheus`. **Active Claude workspace:**
  `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`,
  verified intact.

## Files created

- `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-q_feature-derivation-readiness-execution-plan.md`
  (added; the readiness/execution-plan memo; 21 sections).
- `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-q_closeout.md`
  (added; this closeout).

## Files modified

- `docs/00-meta/current-project-state.md` (narrow update: new Phase 4bn-Q prose
  paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-P paragraphs
  and blocks preserved verbatim as labelled historical context).

No code, test, script, data file, configuration, `.gitignore`,
`pyproject.toml`, `README.md`, MCP file, manifest, sidecar, gate report, or
successor-state artefact was created or modified. **No local data was read; no
local data was created.**

## Validation commands run

- `git status --short` → only the tracked Phase 4bn-Q docs files + expected
  untracked `.claude/scheduled_tasks.lock`; no `data/microstructure/` or
  `data/research/` artefact staged.
- `git diff --check` → clean (no whitespace errors).
- `git diff` over the three named docs → only the intended changes.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- Markdown lint tooling: none is configured in the repository standard, so none
  was run (running an ad-hoc one is unnecessary and could create outputs).
  ruff / mypy / pytest omitted for a docs-only Tier 1 phase with no code surface.

## Result / decision

- **Result state:** `RECORD_FEATURE_DERIVATION_READINESS_PLAN__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_FEATURE_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Recommended state:** remain paused.

## Feature tooling readiness

- **Existing feature primitives** (`features_schema_v002`, `features_compute_v002`,
  `features_io_v002`, `features_manifest_v002`, `features_schema`): **directly
  reusable** (causal-only, no labels/targets/future, forbidden-substring guard,
  canonical sidecars, atomic refuse-overwrite, network-free; offline tests
  present).
- **Feature compute orchestrator (`scripts/phase4bm_h_compute_multiday_features.py`)
  and feature gate (`multiday_feature_gate*`, Phase 4bm-J): NOT directly
  reusable — need bounded new wrappers.** Both are hardcoded to the 90-day v002
  terminal window (2024-12-01 .. 2025-02-28; count 90; 155,153,449 events),
  expect the published `__v002` normalized manifest, **require the Phase 4bm-F
  Stage-3 research-eligible successor-state**, and have no Phase 4bn-L
  preflight/budget caps. Existing tests do not cover the pre-v002 segment shape.

## Feature manifest/versioning

- **Ambiguous; requires a docs-only memo.** Two unsettled questions: (a) the
  existing feature tooling hard-requires a Stage-3 **research-eligible**
  successor-state source, but the pre-v002 normalized segment is **non-eligible**
  (gate-passed, pending), so the non-eligible-source feature precondition must be
  defined; (b) the pre-v002 **feature segment** manifest/versioning shape and
  non-eligible posture are not codified (Phase 4bn-N settled this only for the
  normalized layer). The precedent-consistent shape is a phase-scoped feature
  segment manifest `microstructure_features_aggtrades_v001__v002_pre_v002_segment_<phase-id>.json`
  + version-suffixed segment directory under `data/microstructure/features/`,
  but it must be settled in a memo before execution.

## Sealed-test / v002 terminal boundary

- **Clear; no holdout-boundary memo required** for the conservative
  causal-only pre-v002 feature scope. The feature kernel is strictly causal
  (backward-only, 60 s tail); the segment's last day (2024-11-30) needs no
  forward read into the v002 terminal window, and the first day (2024-03-01)
  needs no pre-segment read (early rows flagged `rolling_missing_window_flag`).
  No segment date overlaps the sealed split (2025-02-14 .. 2025-02-28). A
  holdout-boundary memo becomes required only if a future scope reads the v002
  terminal normalized window or sealed-test dates.

## Scope confirmations

- **No local data read.** No normalized/raw/feature/label/manifest/sidecar/
  gate-report or `data/research` artefact was opened, hashed, counted, or
  inspected. SHA256 digests cited were quoted from committed Markdown evidence.
- **No local data created.** No artefact under `data/microstructure` or
  `data/research`.
- **No code / tests / scripts added or modified.** Existing tooling was inspected
  read-only.
- **No feature derivation / labels / ML / diagnostics / strategy / signals / PnL
  / backtests / storage migration / database / Parquet compaction / v003.**
- **No manifest eligibility transition;** `research_eligible` remains false;
  `eligibility_gate_status` remains pending.
- **No successor authorized** from inside Phase 4bn-Q.

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side; round-trip = 16
bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0;
Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path + sidecar
policy; the Phase 4bn-J-R1 raw-only cap amendment; the Phase 4bn-L derived-stack
storage budget; the Phase 4bn-N normalization manifest/versioning convention) is
preserved verbatim. Phase 4 canonical remains unauthorized. The Phase 4bn-Q
merge phase / any feature manifest/versioning memo / any feature-only execution /
any feature-layer gate / any holdout-boundary memo / any source-policy memo /
any process-doc `D:` path update / any label / ML / diagnostics / strategy /
signals / PnL / backtest / storage-migration / database / Parquet-compaction /
v003 / paper / shadow / live-readiness / deployment / exchange-write /
production-key / any Phase 5 / any successor phase remains unauthorized.

## Final git status / log / SHAs

To be recorded at the phase commit `docs(phase-4bn-q): plan feature derivation
readiness`:

- `git status --short`: `?? .claude/scheduled_tasks.lock` (only the expected
  untracked transient; no `data/microstructure/` or `data/research/` artefact
  staged).
- `git log --oneline -8 --decorate`, `git rev-parse HEAD`,
  `git rev-parse main`, `git rev-parse origin/main`: recorded in the final
  operator report. `main` and `origin/main` remain at
  `b2b46de6a27311318b2e9d58f5de28e5137b28dd` (not merged).
