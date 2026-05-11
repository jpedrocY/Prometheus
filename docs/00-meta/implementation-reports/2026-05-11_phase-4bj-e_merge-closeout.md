# Phase 4bj-E — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-E — Label-Family Eligibility Gate Design +
  Implementation + Execution
- **Type:** code + docs + local gitignored output (one-time gate
  execution against existing Phase 4bj-C local artefacts)
- **Action:** merge into `main`
- **Merge purpose:** bring the Phase 4bj-E offline label-family
  eligibility gate (four new source modules, six new test files,
  narrow package `__init__.py` re-export update, Phase 4bj-E
  implementation report, Phase 4bj-E closeout, and narrow
  `current-project-state.md` update) into `main` so that the gate
  primitive and its 79 new tests are part of the project record. The
  merge also records that Phase 4bj-E executed the gate exactly once
  against the local Phase 4bj-C label artefacts (BTCUSDT 2025-01-15)
  and produced GATE PASS at the report level. The gate report and its
  paired `.sha256` sidecar are local-only gitignored artefacts under
  `data/microstructure/gate-reports/labels/`; they are not committed.
  The merge does not modify any prior manifest, parquet, sidecar, or
  gate report; does not flip `research_eligible`; does not transition
  `eligibility_gate_status`; does not change `chronological_split_policy`;
  does not create a label successor-state; and does not authorize
  Phase 4bj-F, Phase 4bj-G, or any other successor.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-e/label-family-eligibility-gate`

## 2. SHAs

- **`main` SHA before merge:**
  `26a3bebc020fabf78f30bdd9b433c5fbd074e85a`
  (post-Phase-4bk-A merge-closeout state)
- **Phase 4bj-E branch commit SHAs:**
  - `89cde8ad14b5ce92cdd718a7a4eca7bfce3e3835` — feat: label-family
    eligibility gate implementation + tests (four new source modules
    + narrow `__init__.py` re-export update + six new test files)
  - `20e4b21311c87e7b1bab7adc6b1cad01f3e50b9f` — docs: implementation
    report + closeout + narrow `current-project-state.md` update
- **Phase 4bj-E merge commit SHA:**
  `e06dbbd973f02352f61479918267a619b78a4c7b`
- **Final `main` / `origin/main` SHA after merge push:**
  `e06dbbd973f02352f61479918267a619b78a4c7b`
- **Final `main` / `origin/main` SHA after merge-closeout commit +
  push:** (recorded in §16 below after the merge-closeout commit +
  push)
- **Phase 4bk-A merge commit (verified ancestor of `main` at branch
  start):** `6f76b02b8b5fbf1f22b80d88e878e42dd3671571`
- **Phase 4bj-D merge commit (verified ancestor of `main` at branch
  start):** `11e25acbf7d33b30f5149b93919594c3ccab9fe2`

## 3. Merge method

- `git merge --no-ff` with `ort` strategy (no fast-forward; merge
  commit created).
- Merge commit message:
  `docs(phase-4bj-e): merge label-family eligibility gate`.
- Pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing.

## 4. Files brought forward by the merge

Source modules (4 new):

- `src/prometheus/research/microstructure/label_gate_io.py`
- `src/prometheus/research/microstructure/label_gate_checks.py`
- `src/prometheus/research/microstructure/label_gate_report.py`
- `src/prometheus/research/microstructure/label_gate.py`

Package re-export (1 narrowly updated):

- `src/prometheus/research/microstructure/__init__.py` (Phase 4bj-E
  docstring section + 14 new public symbols re-exported + matching
  `__all__` entries; no prior export removed)

Tests (6 new):

- `tests/research/microstructure/_label_gate_fixtures.py`
- `tests/research/microstructure/test_label_gate_io.py` (16 tests)
- `tests/research/microstructure/test_label_gate_checks.py` (23
  tests)
- `tests/research/microstructure/test_label_gate_report.py` (11
  tests; 1 labeled `pytest.skip` placeholder for symmetry with
  sibling files)
- `tests/research/microstructure/test_label_gate.py` (9 tests)
- `tests/research/microstructure/test_label_gate_no_network.py`
  (static no-network / no-credential / no-MCP / no-Graphify scan)

Implementation docs (2 added):

- `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-e_label-family-eligibility-gate.md`
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-e_closeout.md`

Project state (1 narrowly updated):

- `docs/00-meta/current-project-state.md` (Phase 4bj-E narrative
  paragraph + Current phase block; prior Phase 4bk-A block demoted
  to historical context)

No `data/microstructure/` file was modified by the merge.
No prior governance memo was modified beyond the narrow
`current-project-state.md` Phase 4bj-E paragraph addition.
No prior source / test / script was modified outside the narrow
package `__init__.py` re-export update.
No `.gitignore`, `pyproject.toml`, `README.md`, or MCP file was
modified by the merge.

## 5. Total diff summary

From the Phase 4bj-E merge:

```text
14 files changed, 5095 insertions(+), 0 deletions
```

The diff matches the expected change set from the authorization
prompt (4 new source modules + 1 narrowly updated `__init__.py` + 6
new test files + 2 new implementation report files + 1 narrowly
updated `current-project-state.md`).

## 6. Verdict

**GATE PASS — label artefact remains not research-eligible. Code,
tests, and process artefacts landed on `main`.**

Phase 4bj-E is the project's first label-family eligibility gate.
The gate is a standalone offline primitive that reads the existing
local Phase 4bj-C label parquet, paired `.sha256` sidecar, label
manifest, and paired `.sha256` sidecar, runs 72 stable check
functions across 15 groups (`4bj-e.A01` .. `4bj-e.O01`), and emits
an atomic, refuse-overwrite JSON gate report under
`data/microstructure/gate-reports/labels/` with paired `.sha256`
sidecar (gitignored, not committed). The gate enforces seven binding
invariants before write: `research_eligible_after = False`,
`label_manifest_research_eligible_after = False`,
`label_manifest_eligibility_gate_status_after = "pending"`,
`label_manifest_chronological_split_policy_after = "not_yet_defined"`,
`stage_5_authorized = False`, `stage_5_research_or_ml_use = False`,
and `no_successor_authorization = True`. The gate run produced
`overall_status = pass` with 72 / 72 PASS (0 FAIL / 0 ERROR / 0
NOT_APPLICABLE). The label manifest remains
`research_eligible = false`,
`eligibility_gate_status = "pending"`, and
`chronological_split_policy = "not_yet_defined"`. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant is preserved (never invoked). GATE PASS is report-level
evidence only — it does not transition any manifest field, does not
authorize any successor, and does not authorize ML, strategy,
backtests, acquisition, paper / shadow, live, or exchange-write.
Phase 4bj-E is now project-complete only with this merge-closeout
commit on `main`. Recommended state: **remain paused.**

## 7. Local gitignored outputs

The Phase 4bj-E one-time gate execution produced exactly one gate
report and its paired SHA256 sidecar. Both files are local-only and
gitignored. They are NOT committed by this merge:

- **Gate report:**
  - path: `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json`
  - size: 24,715 bytes
  - SHA256: `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0`
  - "not committed" status: confirmed
  - `git check-ignore -v` confirmation: covered by
    `.gitignore:85: data/microstructure/`
  - report id: `microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5`
  - code commit SHA recorded inside report:
    `89cde8ad14b5ce92cdd718a7a4eca7bfce3e3835`
  - input artefacts: Phase 4bj-C label parquet + sidecar + label
    manifest + sidecar (paths recorded inside the report)
- **Gate report sidecar:**
  - path: `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json.sha256`
  - size: 156 bytes
  - SHA256: `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191`
  - "not committed" status: confirmed
  - `git check-ignore -v` confirmation: covered by
    `.gitignore:85: data/microstructure/`
  - matches recomputed bytes of paired report

The gate writer (`write_label_gate_report` in `label_gate_report.py`)
performs atomic write-then-rename under the
`data/microstructure/gate-reports/labels/` path with refuse-overwrite
semantics. The path discipline helper `assert_label_gate_report_path`
in `label_gate_io.py` raises `LabelGateIOError` if any output path
escapes the labels namespace. The gate orchestrator
`run_label_family_gate` in `label_gate.py` accepts
`output_root=data/microstructure/gate-reports/labels/` and rejects
output paths outside `data/microstructure/`.

## 8. Validation results

All commands run from `C:\Prometheus` post-merge on `main` at
commit `e06dbbd973f02352f61479918267a619b78a4c7b`:

- `ruff check src/prometheus/research/microstructure/ tests/research/microstructure/`
  — `All checks passed!`
- `mypy src` (strict) — `Success: no issues found in 119 source
  files` (was 115 at the Phase 4bk-A merge-closeout state; +4 new
  `label_gate_*` modules)
- `pytest tests/research/microstructure/` —
  `823 passed, 1 skipped in 9.27s`
  (the single skipped test is the labeled `pytest.skip` placeholder
  in `test_label_gate_report.py` that exists for symmetry with
  sibling Phase 4bj-* test files; the actual invariant-violation
  tests are the seven `test_write_label_gate_report_rejects_*` cases
  that follow it, all of which pass)
- `git diff --check` — clean (no whitespace errors)
- `git status --short` — only pre-existing untracked entries
  (`.claude/scheduled_tasks.lock`, `data/research/`); working tree
  otherwise clean
- `git check-ignore -v data/microstructure/` —
  `.gitignore:85:data/microstructure/	data/microstructure/`
- `git check-ignore -v data/microstructure/labels/` —
  `.gitignore:85:data/microstructure/	data/microstructure/labels/`
- `git check-ignore -v data/microstructure/manifests/` —
  `.gitignore:85:data/microstructure/	data/microstructure/manifests/`
- `git check-ignore -v data/microstructure/gate-reports/` —
  `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/`
- `git check-ignore -v data/microstructure/gate-reports/labels/` —
  `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/labels/`

Whole-repo pytest was not rerun in this merge phase. The Phase 4bj-D
merge-closeout recorded two pre-existing simulation failures
(`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'`
inside the unrelated `src/prometheus/research/data/storage.py:232`).
Those failures are unchanged from prior phases and are not
introduced by this merge. Phase 4bj-E modifies neither
`src/prometheus/research/data/storage.py` nor
`tests/simulation/`, so no behavioural change on those failures is
expected.

## 9. Upstream immutability evidence

All four upstream Phase 4bj-C artefacts are byte-identical
pre/post the Phase 4bj-E gate run (recomputed on `main` post-merge):

| Artefact | Pre-Phase-4bj-E SHA256 | Post-Phase-4bj-E SHA256 | Status |
| --- | --- | --- | --- |
| Label parquet (`data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet`) | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | IDENTICAL |
| Label parquet sidecar (`...parquet.sha256`) | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | IDENTICAL |
| Label manifest (`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`) | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | IDENTICAL |
| Label manifest sidecar (`...json.sha256`) | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | IDENTICAL |

The Phase 4bj-C label artefacts were the only `data/microstructure/`
files the gate read. No write occurred under `data/microstructure/`
outside the gate-reports/labels/ namespace.

## 10. Manifest state preservation

The Phase 4bj-C label manifest (`microstructure_labels_aggtrades_v001__v001.json`):

- `research_eligible` — `false` pre and post (unchanged)
- `eligibility_gate_status` — `"pending"` pre and post (unchanged)
- `chronological_split_policy` — `"not_yet_defined"` pre and post
  (unchanged)
- `governance_labels` — unchanged: `ml=forbidden`,
  `strategy=forbidden`, `backtest=forbidden`,
  `paper_shadow_live=forbidden`, `deployment=forbidden`,
  `exchange_write=forbidden`, `acquisition=unauthorized`
- `boundary_confirmations` — unchanged
- `label_config_hash` —
  `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`
  pre and post (unchanged)
- `invalid_price_row_count` — `0` pre and post (unchanged)
- `censored_per_horizon` —
  `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` pre and post
  (unchanged)
- `row_count` — `1,681,098` pre and post (unchanged)

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

The Phase 4bj-E merge honours every boundary below:

- no label parquet modified
- no label parquet sidecar modified
- no label manifest modified
- no label manifest sidecar modified
- no feature parquet, feature manifest, normalized parquet,
  original derived manifest, raw manifest, raw zip, Phase 4bb-D
  raw gate report, Phase 4bf derived gate report, Phase 4bg-B
  successor-state, Phase 4bi-B feature-family gate report, or
  Phase 4bi-D feature-family successor-state modified
- no `data/microstructure/` write outside
  `data/microstructure/gate-reports/labels/`
- no `data/microstructure/` artefact committed
- no label-family successor-state artefact created
- no replacement parquet / manifest / sidecar / gate report /
  successor-state created
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `chronological_split_policy` changed on any actual manifest
- no ML model trained
- no ML architecture designed
- no feature ranking performed
- no meta-labeling created
- no strategy created
- no strategy signal computed
- no backtest run
- no data acquired
- no public endpoint called
- no Binance API called
- no WebSocket opened
- no credential read
- no `.env` read or created
- no `.mcp.json` read or created
- no MCP enabled
- no Graphify enabled
- no normalizer rerun
- no raw eligibility gate rerun
- no derived-family gate rerun
- no feature kernel rerun
- no feature-family eligibility gate rerun
- no label kernel rerun
- no existing source file modified outside the narrow package
  `__init__.py` re-export update
- no existing test modified
- no existing script modified
- no `.gitignore`, `pyproject.toml`, or `README.md` modified
- no MCP file modified
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## 12. Retained verdict ledger

All retained verdicts preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

All locks preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy

All prior phase results (Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as,
4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D,
4bb-E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B, 4bh-A, 4bh-B,
4bh, 4bi-A, 4bi-B, 4bi-C, 4bi-D, 4bj-A, 4bj-B, 4bj-C, 4bj-D, 4bk-A)
preserved verbatim.

## 14. No-rescue constraints

The Phase 4bj-E merge does not, and cannot, be construed as
authorising:

- ML model training, model selection, feature ranking, meta-labeling,
  or any conversion of labels into signals;
- strategy hypothesis generation, signal construction, strategy logic,
  position state, entry / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible` from this
  evidence alone;
- transitioning any manifest's `eligibility_gate_status` from this
  evidence alone;
- changing any manifest's `chronological_split_policy` from this
  evidence alone;
- creating a label-family successor-state artefact from this
  evidence alone;
- treating the GATE PASS report as authorisation to design ML,
  strategy, backtests, or live work;
- treating the gate primitive as authorisation to rerun it without
  separate operator authorization and explicit recorded reason.

GATE PASS is report-level evidence only. The on-disk label manifest
is not transitioned by the gate run.

## 15. Successor authorization

**None.**

The following candidate successors are NOT authorised by this merge:

- Phase 4bj-F — Label-Family Research / ML-Use Decision Memo
- Phase 4bj-G — Label-Family Successor-State Recording
- Phase 4bj (catch-all)
- Phase 4bb-F — Gate Report Output Path Hygiene
- Phase 4bb-G — Raw Manifest Successor-State Recording
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book
  data acquisition
- ML implementation
- strategy implementation
- backtest implementation
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- user stream
- live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials

## 16. Recommended state

**Remain paused.**

Phase 4bj-E is project-complete with this merge-closeout commit on
`main`. The label-family eligibility gate primitive is now part of
the project record, the one-time gate run is recorded as GATE PASS
at the report level, and the label manifest remains
`research_eligible=false / eligibility_gate_status=pending /
chronological_split_policy=not_yet_defined`. No successor phase is
authorized.

**Conditional next, NOT authorised:**

Phase 4bj-F — Label-Family Research / ML-Use Decision Memo
(docs-only) is the cleanest non-paused option. It would record a
policy decision about whether and how the label artefact (which now
has a passing gate report at the report level) may be admitted for
future research / ML use, without flipping any manifest field and
without authorising ML / strategy / backtest / acquisition. Phase
4bj-F is **not** authorised by this merge. Per the Phase 4bk-A
workflow standard, a separately authorised authorization prompt is
required before any successor begins.

**Final `main` / `origin/main` SHA after this merge-closeout commit
+ push:** `ef37b0fa3c4f91565b96d0f7da74885704d014b3`
