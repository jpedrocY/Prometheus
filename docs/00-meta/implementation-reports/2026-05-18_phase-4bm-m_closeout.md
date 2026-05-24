# Phase 4bm-M — Closeout

**Phase identity:** Phase 4bm-M — Multi-Day V002 Label-Family Boundary / Design Memo (docs-only label-boundary / design memo; multi-day v002 analogue of Phase 4bj-A).
**Date:** 2026-05-18.
**Phase type:** docs-only. No source / test / script / config / data / manifest / sidecar / gate-report / successor-state mutation. **No** local gitignored output is created.
**Status:** branch-complete; pending operator review; **NOT** project-complete. Project-completion requires a separately authorized merge phase per `docs/00-meta/process/merge-closeout-standard.md`.

---

## 1. Branch name

`phase-4bm-m/multi-day-v002-label-family-boundary-design-memo`

## 2. Base SHA

`38cf6693425f91e85e2d5a295800aa5ee2287db3` (Phase 4bm-L merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified in sync).

## 3. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bj-A label-boundary precedent. First-of-kind multi-day v002 label-family boundary / design memo; defines future target / label semantics for a Stage-5-admissible feature family and therefore can affect downstream ML admissibility under §3 ("creates features / labels / diagnostics" + "affects eligibility / admissibility / downstream authorization").

## 4. Tracked files added / modified

Added (new tracked files):

- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_multi-day-v002-label-family-boundary-design-memo.md` — the main 39-section boundary / design memo.
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_closeout.md` — this closeout.

Modified narrowly:

- `docs/00-meta/current-project-state.md` — new Phase 4bm-M narrative paragraph + new "Current phase:" block; the prior Phase 4bm-L "Current phase:" block is preserved as labelled historical context.

**No** source / test / script / configuration / data / manifest / sidecar / gate-report / prior successor-state file is modified. **No** `data/microstructure/` artefact is created, modified, deleted, renamed, or committed. **No** prior implementation report, closeout, or merge-closeout is modified. **No** prior governance memo is modified.

## 5. Local gitignored outputs created

**None.** Phase 4bm-M is docs-only. No label parquet, no label sidecar, no label manifest, no label manifest sidecar, no label gate report, no label successor-state JSON, no label successor-state sidecar, no `.json`, no `.parquet`, no `.csv`, no `.duckdb`, no `.jsonl` was created under `data/microstructure/` or anywhere else.

## 6. Decision / design result

Phase 4bm-M records the future multi-day v002 label-family boundary at policy level only:

- **Proposed future family identity:** `dataset_family = "microstructure_labels_aggtrades_v001"`, `dataset_version = "v002"`, `label_schema_version = "v001"`, source feature / normalized / raw lineage at `v002`, symbol scope `["BTCUSDT"]`, date range `2024-12-01 .. 2025-02-28` inclusive (90 contiguous UTC days).
- **Proposed future namespace:** label parquets at `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/...`; label manifest at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`; paired canonical Phase 4bb-F sidecars throughout; label gate reports under `data/microstructure/gate-reports/labels/`; sibling label successor-states under `data/microstructure/successor-state/`.
- **Allowed future label classes (in principle):** class A `forward_log_return_<horizon>` (numeric / regression), class B `forward_direction_<horizon>` (classification with predeclared thresholds), class F per-horizon validity / censoring flags. Classes C (barrier), D (MFE / MAE / R-multiple), and E (time-to-event) are admissible **in principle** but deferred at v002 first pass to mirror v001 Phase 4bj-A deferral.
- **Forbidden future label classes:** strategy entry / exit decisions, PnL, equity, model predictions / probabilities / scores, post-model labels, mark-price stop labels (at v002 first-pass scope), cross-venue / external data labels, rescue-shaped labels, labels that mutate any upstream artefact, labels that require public or private endpoint calls.
- **Causal-separation rule:** features must remain causal; labels may use future information **only inside the label kernel**; label columns must never appear in feature parquets; label code must be independently importable from feature code.
- **Multi-day horizon / boundary policy:** UTC-only timestamps; deterministic event ordering; explicit per-horizon censoring at 2025-02-28 23:59:59.999 UTC envelope; no acquisition beyond the 90 locked v002 dates.
- **Future implementation gate prerequisites (14 conditions, all currently unmet):** Phase 4bm-M merged + project-complete; separately authorized schema finalization phase; separately authorized implementation phase; exact-schema implementation; gitignored-only artefacts; byte-identical preservation of all upstream artefacts; no ML / strategy / backtest output; manifest defaults `research_eligible=false` / `eligibility_gate_status="pending"`; explicit null / censoring / horizon / split-policy metadata; passing `ruff` / `mypy` / `pytest`; matching closeout discipline.

**No label artefact is created, computed, validated, or committed by Phase 4bm-M.** The decision is design-only.

## 7. Key evidence

| # | Evidence item | Value |
| - | ------------- | ----- |
|  1 | Phase 4bm-L successor-state JSON SHA256 | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (recomputed on disk; matches) |
|  2 | Phase 4bm-L successor-state sidecar SHA256 | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` |
|  3 | Phase 4bm-K decision | **Outcome 1 / Decision form 1** (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) |
|  4 | Phase 4bm-K SHA-finalization commit | `121865a26120d5f097fee95c00185ebd4c995703` |
|  5 | Phase 4bm-J gate verdict | `FEATURE_GATE_PASS` (`overall_status = pass`) |
|  6 | Phase 4bm-J gate report SHA256 | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (recomputed on disk; matches) |
|  7 | Phase 4bm-J gate sidecar SHA256 | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` |
|  8 | Phase 4bm-J check totals | 50 / 50 PASS / 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking |
|  9 | Phase 4bm-I structural QA verdict | `FEATURE_STRUCTURAL_QA_PASS` |
| 10 | v002 feature manifest SHA256 | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (recomputed on disk; matches; unchanged) |
| 11 | v002 feature manifest sidecar SHA256 | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` (unchanged) |
| 12 | `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| 13 | Feature parquet count | 90 |
| 14 | Feature sidecar count | 90 |
| 15 | Total feature row count | 155,153,449 |
| 16 | Feature date range | 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days) |
| 17 | Symbol scope | BTCUSDT (one symbol) |
| 18 | Feature schema column count | 62 (17 lineage / identity / metadata + 45 feature / quality) |
| 19 | v002 derived multi-day index manifest SHA256 | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (recomputed on disk; matches; unchanged) |
| 20 | v002 derived manifest sidecar SHA256 | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` (unchanged) |
| 21 | v002 raw manifest SHA256 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` (unchanged) |
| 22 | v002 acquisition log SHA256 | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` (unchanged) |
| 23 | Phase 4bl-D-R raw multi-day PASS gate report SHA256 | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` (unchanged) |
| 24 | Phase 4bl-E raw multi-day successor-state JSON SHA256 | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` (unchanged) |
| 25 | Phase 4bm-D authoritative derived-family gate report SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` (unchanged) |
| 26 | Phase 4bm-D authoritative gate sidecar SHA256 | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` (unchanged) |
| 27 | Phase 4bm-F v002 derived-family Stage-3 successor-state JSON SHA256 | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` (unchanged) |
| 28 | Phase 4bm-F v002 derived-family Stage-3 successor-state sidecar SHA256 | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` (unchanged) |
| 29 | v001 precedent (label-family boundary / design) | Phase 4bj-A (`docs/00-meta/implementation-reports/2026-05-10_phase-4bj-a_label-boundary-target-definition.md`); selected Outcome 1 (label boundary admissible in principle, implementation deferred) |
| 30 | On-disk v002 feature manifest invariants (verified) | `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false` |

## 8. Validation results

- `git status --short` (pre-write, post-write, post-commit): only the two expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); no new gitignored artefacts created.
- `git branch --show-current`: `phase-4bm-m/multi-day-v002-label-family-boundary-design-memo`.
- `git rev-parse main`: `38cf6693425f91e85e2d5a295800aa5ee2287db3`.
- `git rev-parse origin/main`: `38cf6693425f91e85e2d5a295800aa5ee2287db3` (in sync).
- `git log --oneline -12 --decorate`: latest main commit `38cf669 docs(phase-4bm-l): finalize merge closeout shas` (matches expectation).
- `git diff --check`: clean (exit 0).
- `git diff --name-only`: exactly 3 tracked docs paths (the boundary / design memo, this closeout, and the narrow `current-project-state.md` update).
- Read-only SHA verification (recomputed on disk at the start of this phase):
  - v002 feature manifest: `512a0a54…` matches; **byte-identical**.
  - Phase 4bm-J gate report: `3c59dfae…` matches; **byte-identical**.
  - v002 derived multi-day index manifest: `01c5fa53…` matches; **byte-identical**.
  - Phase 4bm-L successor-state JSON: `7eccaa8f…` matches; **byte-identical**.
- v002 feature manifest invariants verified on disk: `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false` (unchanged).
- The remaining 13 upstream artefacts (per the Phase 4bm-M memo §10 evidence table) were not re-hashed in this phase because Phase 4bm-M reads no Parquet, runs no kernel, and modifies no `data/microstructure/` file; their SHAs are taken verbatim from the Phase 4bm-L successor-state JSON and the Phase 4bm-L implementation report.
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (**never invoked** by Phase 4bm-M).

## 9. Quality gate results / skipped-check rationale

- `git diff --check`: clean (exit 0).
- Repo-standard markdown lint or check: no project-specific lightweight markdown gate exists in this repository; not run.

**Skipped checks (justified):**

- `ruff check`: **skipped.** Phase 4bm-M modifies no Python source, tests, scripts, or configs. Nothing under `src/prometheus/`, `tests/`, or `scripts/` is touched.
- `mypy src/prometheus`: **skipped.** Same rationale. The Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files) is preserved by construction.
- `pytest` (targeted or whole-repo): **skipped.** Same rationale. The Phase 4bm-J branch quality gates already locked the codebase status into the Phase 4bm-J merge-closeout on `main`:
  - Phase 4bm-J surface `ruff check` (11 paths): PASS.
  - Whole-repo `ruff check .`: PASS.
  - `pytest tests/research/microstructure/test_multiday_feature_gate*.py`: 53 PASS in 7.86 s.
  - Whole-repo `pytest`: 15 collection errors from missing `httpx` / `duckdb` env modules + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures (both env baseline). This baseline is unchanged by Phase 4bm-M because Phase 4bm-M modifies no existing source / test / script.

These skips conform to the project's standing precedent for Tier 1 docs-only boundary / design-memo phases (Phase 4bj-A v001 label-boundary, Phase 4bg-A v001 derived-family research-eligibility, Phase 4bi-C v001 feature-family research-use, Phase 4bm-A multi-day normalization design, Phase 4bm-E multi-day derived-family research-eligibility decision, Phase 4bm-G v002 feature-boundary design, Phase 4bm-K v002 feature-family research-use decision — each of which deliberately skipped these gates for the same reason).

## 10. Non-authorization boundaries

Phase 4bm-M honors reusable non-authorization blocks **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, and **N-SUCCESSOR-STATE** (Phase 4bm-M creates **no** new successor-state artefact) per `docs/00-meta/process/phase-risk-tiering-standard.md` §7.

Phase 4bm-M does **not**, and **cannot**, authorize:

- Phase 4bm-N (any provisional successor; not authorized);
- multi-day v002 label-family schema finalization (multi-day analogue of Phase 4bj-B);
- multi-day v002 label-kernel implementation (multi-day analogue of Phase 4bj-C);
- multi-day v002 label artefact structural QA (multi-day analogue of Phase 4bj-D);
- multi-day v002 label-family eligibility gate design / implementation / execution (multi-day analogue of Phase 4bj-E);
- multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F);
- multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G);
- multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I);
- multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J);
- multi-day v002 diagnostics;
- multi-day v002 ML training, model selection, feature ranking, meta-labeling;
- multi-day v002 strategy specification, implementation, signal construction;
- multi-day v002 backtest specification, plan, or execution;
- additional acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue data, no aggTrades acquisition beyond the existing locked v002 90-day envelope);
- Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*;
- Phase 5;
- Phase 4 canonical;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user-stream / live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, or Phase 4bm-L;
- any further successor-state JSON creation;
- any successor phase whatsoever.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (**never invoked**).

## 11. Recommended state

**Remain paused.**

Phase 4bm-M is branch-complete only by this work. Per the Phase 4bk-A workflow standard, Phase 4bm-M is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per the full Tier 1 16-section structure. The operator's broader pause decision continues to apply.

## 12. Explicit non-authorization statement

**Phase 4bm-N / multi-day v002 label schema finalization memo / multi-day v002 label kernel implementation / multi-day v002 label artefact structural QA / multi-day v002 label-family eligibility gate / multi-day v002 label-family research-use decision memo / multi-day v002 label-family successor-state recording / multi-day v002 chronological-split-policy memo / multi-day v002 chronological-split-policy successor-state recording / multi-day v002 diagnostics / multi-day v002 ML / multi-day v002 strategy / multi-day v002 backtests / additional acquisition / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical / paper-shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / user-stream / live WebSocket implementation / public-endpoint calls in code / MCP / Graphify / `.mcp.json` / credentials / any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest / any committed `data/microstructure/` artefact / any further successor-state JSON creation / any successor phase whatsoever — all remain unauthorized after Phase 4bm-M.**

## 13. Required exact phrases (verbatim, per task brief)

- **Phase 4bm-M is label-boundary design only.**
- **No label artefact exists after Phase 4bm-M.**
- **Phase 4bm-N is not authorized by Phase 4bm-M.**
- **Label computation is not authorized by Phase 4bm-M.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-M.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**
