# Phase 4bn-M — Closeout

**Phase 4bn-M is branch-complete only by this work; not merged into main;
not project-complete.** Phase 4bn-M is a docs-only / normalization-readiness
/ execution-planning / boundary-contract phase (**Tier 1 Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3). It produces a
predeclared future normalization-only execution contract for the expanded
12-month BTCUSDT Binance USDⓈ-M futures aggTrades raw envelope and
authorizes nothing executable and no successor.

**Phase 4bn-M does not run normalization, derive features, derive labels,
run ML, score models, generate predictions, run diagnostics, run strategy /
signals / PnL / backtests, acquire data, call any endpoint, download any
archive or CHECKSUM, run any HEAD preflight, read any local raw zip / v002
terminal window / sealed test split / local `data/microstructure` /
`data/research` artefact / local manifest / local gate report, create a
database, create `.duckdb` / `.sqlite`, compact Parquet, migrate storage,
create v003, mutate any manifest / sidecar / gate report / successor-state
artefact, flip `research_eligible`, transition `eligibility_gate_status`,
use credentials / `.env` / `.mcp.json` / MCP / Graphify, or authorize any
successor phase. Recommended state remains paused.**

## Branch and base

- **Branch:** `phase-4bn-m/normalization-readiness-execution-plan`.
- **Base `main` SHA:** `b7767a636a864bcb2eeca6a613c8f7c602a85c5b`
  (`docs(phase-4bn-l): finalize merge closeout shas`; pre-branch
  `main == origin/main == HEAD` verified in sync; Phase 4bn-L
  SHA-finalization `b7767a6`, merge-closeout `4479a69`, merge `5c7b5a9`,
  branch finalization `20022d2`, and the Phase 4bn-L original memo commit
  `d56420c` all present on `main`; Phase 4bn-K SHA-finalization `d8d3ba8`
  present as predecessor).
- **Commit SHA:** recorded in §"Final git status / log / SHAs" after the
  single phase commit `docs(phase-4bn-m): plan normalization readiness`.
- **Active local repo path:** `D:\Prometheus`.
- **Active Claude workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` →
  `https://github.com/jpedrocY/Prometheus.git`, verified intact.

## Files created

- `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_normalization-readiness-execution-plan.md`
  (added; the normalization-readiness / execution-plan memo; 20 sections).
- `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_closeout.md`
  (added; this closeout).

## Files modified

- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4bn-M prose paragraph + new `Current phase:`
  block; prior Phase 4bn-A … 4bn-L paragraphs and blocks preserved as
  labelled historical context).

No code, test, script, data file, configuration, `.gitignore`,
`pyproject.toml`, `README.md`, MCP file, manifest, sidecar, gate report, or
successor-state artefact was created or modified. **No local data was read;
no local data was created.**

## Validation commands run

- `git status --short` → only the tracked Phase 4bn-M docs files +
  expected untracked `.claude/scheduled_tasks.lock`; no
  `data/microstructure/` or `data/research/` artefact staged.
- `git diff --check` → clean.
- `git diff -- docs/00-meta/current-project-state.md docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_normalization-readiness-execution-plan.md docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_closeout.md`
  → only the three intended docs changes.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- Markdown lint tooling: none is configured in the repository (no
  `.markdownlint*`, `.mdlrc`, or markdownlint / mdformat / remark
  dependency); a repo-standard markdown validator does not exist, so none
  was run (running an ad-hoc one is unnecessary and could create outputs).
  Repository tooling (ruff / mypy / pytest) is omitted for a docs-only
  Tier 1 phase that creates no code surface; the status-check, diff-check,
  and gitignore confirmation are the relevant validation surface.

## Result / decision

- **Result state:** `RECORD_NORMALIZATION_READINESS_PLAN__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_NORMALIZATION_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

## Readiness findings

- **Existing normalization tooling — primitives:** **SAFE and directly
  reusable** (`normalize_aggtrades.py`, `normalize_io.py`,
  `normalize_manifest.py`, `normalize_validation.py`, `canonical_paths.py`;
  network-free, credential-free, atomic, refuse-overwrite, canonical
  two-space `.sha256` sidecars, locked 19-column `NORMALIZED_SCHEMA_V001`;
  established offline test suite present).
- **Existing normalization tooling — runner:** **NEEDS A BOUNDED NEW
  WRAPPER.** `scripts/phase4bm_b_normalize_multiday_aggtrades.py` is
  hardcoded to the 90-day v002 window and locked v002 precondition SHAs,
  reads the published v002 raw manifest (not the pre-v002 segment manifest),
  enforces a v002 identity cross-check, and has no Phase 4bn-L
  preflight/budget caps; it cannot be repointed at the pre-v002 segment. A
  bounded new runner reusing the locked primitives and adding segment-date
  guards + the 4bn-L caps + an offline test module is required, mirroring
  the Phase 4bn-J-R2 and Phase 4bn-K precedents. This is safe and bounded,
  not unsafe.
- **Manifest / versioning:** **AMBIGUOUS — requires a memo.** The pre-v002
  raw segment used a phase-scoped segment manifest; the dataset-versioning
  doc codifies only monotonic `__vNNN` + predecessor linkage and does not
  settle the normalized segment-manifest / backward-extension /
  full-envelope identity; v003 is forbidden.
- **Sealed-test / v002 terminal boundary:** **CLEAR for the conservative
  pre-v002-only scope** (sealed-test dates are not in the pre-v002 input
  range and are already normalized in the `__v002` family; raw-to-normalized
  over sealed dates is not test-use). A separate holdout-boundary memo is
  required **only if** a future phase proposes to read the v002 terminal raw
  window.

## Future normalization scope recommended

BTCUSDT only; Binance USDⓈ-M futures; aggTrades only; normalized aggTrades
output only; conservative first execution = **pre-v002 segment
2024-03-01 .. 2024-11-30 only**, with the existing v002 terminal window
**treated by reference** (already normalized as `__v002`) and assembled into
a full 12-month envelope **by manifest/reference** rather than re-reading the
terminal window; Parquet canonical; canonical sidecars; non-eligible
manifest; no database; no Parquet compaction; no v003; no features / labels
/ research outputs.

## Future normalization budget carried forward

Normalized layer **100 GiB warn / 150 GiB hard** footprint, **4 h warn / 8 h
hard** runtime; temporary workspace **50 GiB / 100 GiB**; total derived-stack
binding aggregate **250 GiB warn / 300 GiB hard**; `D:` free-space floor
**≥ 500 GiB before execution**, **fail closed below 350 GiB during
execution**; stop before writing if normalized > 150 GiB, total > 300 GiB, or
`D:` free < 500 GiB.

## Recommended state

**Remain paused.** Phase 4bn-M is branch-complete only; not merged into
main; not project-complete until a separately authorized merge phase records
its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1).
**No successor authorized.**

## Scope confirmations

- **No local data read.** No raw zip, normalized parquet, feature file,
  label file, manifest, sidecar, gate report, or any `data/microstructure`
  / `data/research` artefact was opened, hashed, counted, or inspected.
- **No local data created.** No data artefact, manifest, sidecar, or gate
  output was produced under `data/microstructure` or `data/research`.
- **No code / tests / scripts added or modified.** Existing tooling was
  inspected read-only; nothing under `scripts/`, `src/`, or `tests/` was
  changed.
- **No normalization / features / labels / ML / diagnostics / strategy /
  PnL / backtests / storage migration / database / Parquet compaction /
  v003** was performed or authorized.
- **No manifest eligibility transition** occurred; `research_eligible`
  remains `false`; `eligibility_gate_status` remains `pending`.
- **No successor authorized** from inside Phase 4bn-M.

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v;
Phase 4w; Phase 4ak M0; Phase 4al refined no-rescue rule; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked);
Phase 4bb-F canonical path + sidecar policy; the Phase 4bn-J-R1 raw-only cap
amendment; the Phase 4bn-L derived-stack storage budget) is preserved
verbatim. Phase 4 canonical remains unauthorized. The Phase 4bn-M merge
phase / any normalization manifest/versioning memo / any normalization-only
execution phase / any holdout-boundary memo / any source-policy
documentation memo / any process-doc `D:` path update / any normalization /
feature / label / ML / diagnostics / strategy / signals / PnL / backtest /
storage-migration / database-creation / Parquet-compaction / v003-creation /
paper / shadow / live-readiness / deployment / exchange-write /
production-key / any Phase 5 / any successor phase remains unauthorized.

## Final git status / log / SHAs

To be recorded at the phase commit `docs(phase-4bn-m): plan normalization
readiness`:

- `git status --short`: `?? .claude/scheduled_tasks.lock` (only the expected
  untracked transient; no `data/microstructure/` or `data/research/`
  artefact staged).
- `git log --oneline -8 --decorate`, `git rev-parse HEAD`,
  `git rev-parse main`, `git rev-parse origin/main`: recorded in the final
  operator report. `main` and `origin/main` remain at
  `b7767a636a864bcb2eeca6a613c8f7c602a85c5b` (not merged).
