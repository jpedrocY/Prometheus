# Phase 4bn-R — Closeout

**Phase 4bn-R is branch-complete only by this work; not merged into main; not
project-complete.** Phase 4bn-R is a docs-only / feature-manifest /
feature-versioning / non-eligible-source precondition / boundary-contract phase
(**Tier 1 Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md`
§3). It resolves, from committed docs and committed tooling only, the feature
manifest/versioning ambiguity and the non-eligible-source precondition
divergence that Phase 4bn-Q identified, so that a future feature-only execution
phase over the Phase 4bn-O / 4bn-P pre-v002 normalized BTCUSDT Binance USDⓈ-M
futures aggTrades segment can later be cleanly authorized. It authorizes nothing
executable and no successor.

**Phase 4bn-R does not derive features, create feature artefacts, create or
mutate any manifest or gate report, run any feature gate, rerun normalization,
rerun any gate, acquire data, call any endpoint, read any local
raw/normalized/feature/label/research artefact, read any local
`data/microstructure` manifest or gate report, read the v002 terminal raw or
normalized window, touch the sealed test split, create a database, create
`.duckdb`/`.sqlite`, compact Parquet, migrate storage, create v003, flip
`research_eligible`, transition `eligibility_gate_status`, or authorize any
successor.** Recommended state remains paused.

## Branch and base

- **Branch:** `phase-4bn-r/feature-manifest-versioning-memo`.
- **Base `main` SHA:** `014c58add240e2c0bd2666b971cb76024942f89d`
  (`docs(phase-4bn-q): finalize merge closeout shas`; pre-branch
  `main == origin/main == HEAD` verified in sync; Phase 4bn-Q SHA-finalization
  `014c58a`, merge-closeout `51a20a2`, merge `7ac685b`, and branch `b7f8f2c`
  all present on `main`; Phase 4bn-P SHA-finalization `b2b46de` present as
  predecessor).
- **Commit SHA:** recorded in §"Final git status / log / SHAs" after the single
  phase commit `docs(phase-4bn-r): settle feature manifest versioning`.
- **Active local repo path:** `D:\Prometheus`. **Active Claude workspace:**
  `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`,
  verified intact.

## Files created

- `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-r_feature-manifest-versioning-memo.md`
  (added; the feature manifest/versioning memo; 23 sections).
- `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-r_closeout.md`
  (added; this closeout).

## Files modified

- `docs/00-meta/current-project-state.md` (narrow update: new Phase 4bn-R prose
  paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-Q paragraphs
  and blocks preserved verbatim as labelled historical context).

No code, test, script, data file, configuration, `.gitignore`,
`pyproject.toml`, `README.md`, MCP file, manifest, sidecar, gate report, or
successor-state artefact was created or modified. **No local data was read; no
local data was created.**

## Validation commands run

- `git status --short` → only the tracked Phase 4bn-R docs files + expected
  untracked `.claude/scheduled_tasks.lock`; no `data/microstructure/` or
  `data/research/` artefact staged.
- `git diff --check` → clean (no whitespace errors).
- `git diff` over the three named docs → only the intended changes.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- Markdown lint tooling: none is configured in the repository standard, so none
  was run (running an ad-hoc one is unnecessary and could create outputs).
  ruff / mypy / pytest omitted for a docs-only Tier 1 phase with no code
  surface.

## Result / decision

- **Result state:** `RECORD_FEATURE_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_FEATURE_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Recommended state:** remain paused.

## Selected feature manifest/versioning convention

- **Shape:** a phase-scoped **feature segment manifest** mirroring the merged
  raw-layer (Phase 4bn-J-R2 / 4bn-K) and normalized-layer (Phase 4bn-N / 4bn-O)
  precedents — a backward segment of the v002 envelope, not a new monotonic
  version, not a write into the published `__v002` family, not v003.
- **Manifest filename:**
  `microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>.json`
  (+ canonical two-space `.sha256` sidecar), inner `dataset_family =
  "microstructure_features_aggtrades_v001"`, `dataset_version = "v002"`,
  `version = "v002"`, `feature_schema_version = "v001"`, `segment_label =
  "pre_v002_segment"`.
- **Both, sequenced:** a mandatory segment manifest at execution, plus an
  optional deferred by-reference full-envelope feature reference/assembly
  manifest.

## Selected non-eligible-source precondition

- Replace the existing Stage-3 research-eligible successor-state precondition
  (the Phase 4bm-F `stage3_research_eligible` artefact pinned by the v002
  feature manifest builder) with a **non-eligible-source precondition**:
  - source admissibility predecessor = the **Phase 4bn-P normalized-layer gate
    report** (SHA256 `3452fd9d…f134`, PASS verdict
    `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`);
  - source normalized segment = the **Phase 4bn-O segment manifest** (SHA256
    `0e96ae37…d9fa`), verified by SHA256; not the published `__v002` normalized
    manifest;
  - the source normalized segment must remain non-eligible
    (`research_eligible: false`, `eligibility_gate_status: "pending"`);
  - **no `research_eligible: true` and no Stage-3 successor-state is required or
    created** for this pre-v002 expansion path;
  - generated feature outputs remain non-eligible and pending
    (`no_successor_authorization: true`); the Phase 4aw
    `flip_research_eligible(...)` invariant is never invoked;
  - generated features cannot be used for labels / ML / diagnostics / strategy /
    research / split policy until later separately authorized gates/policies.

## Selected future feature output directory convention

- `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`
  (+ canonical two-space `.sha256` sidecar) — a version-suffixed segment
  directory distinct from the published `__v002/` feature directory; the future
  bounded wrapper builds the segment-suffixed `family_dir` exactly as
  `features_io_v002` builds `V002_FEATURE_DIR_SEGMENT` for `__v002`.

## Selected full-envelope feature reference convention

- By reference only — `full_intended_envelope_start = 2024-03-01`,
  `full_intended_envelope_end = 2025-02-28` in the segment manifest; an
  `existing_v002_feature_reference` block (published `__v002` feature manifest
  path + window, `read: false`, `mutated: false`); and an optional, deferred,
  by-reference full-envelope feature reference/assembly manifest
  (`microstructure_features_aggtrades_v001__v002_full_envelope_reference_<phase-id>.json`)
  naming the segment manifest + published `__v002` feature manifest; never
  rewriting v002 feature artefacts, never reading v002 terminal normalized
  dates.

## Recommendation flags

- **Feature-only execution recommended?** Yes — `RECOMMEND_AUTHORIZE_FEATURE_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`,
  the predeclared preferred decision because the memo resolved
  manifest/versioning and the non-eligible-source precondition without requiring
  v003 or a v002 terminal/sealed-test read. Subject to separate operator
  authorization; not authorized here.
- **Holdout-boundary memo required?** No — the conservative causal-only
  pre-v002 feature scope reads neither the v002 terminal normalized window nor
  sealed-test dates. It becomes required only if a future feature scope reads
  the v002 terminal normalized window or sealed-test dates.

## Boundary confirmations

- **v003 remains forbidden.**
- **Published feature `__v002` manifests/directories remain immutable**
  (by-reference only).
- **v002 terminal normalized window remains by-reference only** (not read).
- **Sealed-test split remains untouched** (`sealed_test_split_touched: false`,
  `test_holdout_touched: false`, `test_rows_loaded: 0`).

## Scope confirmations

- **No local data read.** No normalized/raw/feature/label/manifest/sidecar/
  gate-report or `data/research` artefact was opened, hashed, counted, or
  inspected. SHA256 digests cited were quoted from committed Markdown evidence.
- **No local data created.** No artefact under `data/microstructure` or
  `data/research`.
- **No code / tests / scripts added or modified.** Existing tooling was
  inspected read-only.
- **No feature derivation / labels / ML / diagnostics / strategy / signals /
  PnL / backtests / storage migration / database / Parquet compaction / v003.**
- **No manifest eligibility transition;** `research_eligible` remains false;
  `eligibility_gate_status` remains pending.
- **No successor authorized** from inside Phase 4bn-R.

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side; round-trip = 16
bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0;
Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path + sidecar
policy; the Phase 4bn-J-R1 raw-only cap amendment; the Phase 4bn-L derived-stack
storage budget; the Phase 4bn-N normalization manifest/versioning convention) is
preserved verbatim. Phase 4 canonical remains unauthorized. The Phase 4bn-R
merge phase / any feature-only execution / any feature-layer gate / any
holdout-boundary memo / any source-policy memo / any process-doc `D:` path
update / any label / ML / diagnostics / strategy / signals / PnL / backtest /
storage-migration / database / Parquet-compaction / v003 / paper / shadow /
live-readiness / deployment / exchange-write / production-key / any Phase 5 /
any successor phase remains unauthorized.

## Final git status / log / SHAs

To be recorded at the phase commit `docs(phase-4bn-r): settle feature manifest
versioning`:

- `git status --short`: `?? .claude/scheduled_tasks.lock` (only the expected
  untracked transient; no `data/microstructure/` or `data/research/` artefact
  staged).
- `git log --oneline -8 --decorate`, `git rev-parse HEAD`,
  `git rev-parse main`, `git rev-parse origin/main`: recorded in the final
  operator report. `main` and `origin/main` remain at
  `014c58add240e2c0bd2666b971cb76024942f89d` (not merged).
