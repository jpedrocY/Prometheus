# Phase 4bb-F-implementation — Merge Closeout

## §1. Phase identity

- **Phase identifier:** Phase 4bb-F-implementation
- **Phase name:** Gate Report / Successor-State Writer Path Policy
  Implementation
- **Phase type:** Implementation phase (code + tests + docs); narrow,
  backward-compatible safe subset of Phase 4bb-F Option C.
- **Merge purpose:** Land the prospective Phase 4bb-F canonical path
  policy in code via a new pure-path helper module plus optional
  backward-compatible kwargs on the raw-gate writer and orchestrator.
- **Source branch:**
  `phase-4bb-f-implementation/gate-report-successor-state-writer-path-policy`
- **Target branch:** `main`

Per the Phase 4bk-A workflow standard, **Phase 4bb-F-implementation is
project-complete only after this merge plus the merge-closeout commit
on `main`.**

## §2. SHAs

- **Pre-merge `main` SHA (full):**
  `72d171060498769875ab892a886558af762b28f0`
- **Source branch commit SHA (full):**
  `9284c45461d6aae0edf08354e659e574e64afab3`
  (the single `feat(phase-4bb-f-implementation): canonical path policy
  helpers + opt-in family_subdir / phase_id` commit on the branch).
- **Merge commit SHA (full):**
  `ce20da7f5084fffe89adef6722c58a15dcbc4823`
  (created by `git merge --no-ff -s ort
  phase-4bb-f-implementation/gate-report-successor-state-writer-path-policy`
  on `main`).
- **Merge-closeout commit SHA (full):**
  `b1c49a12fd931a64e9c7d46821739432acd94479`
  (the commit that adds this merge-closeout file on `main`).
- **Final `main` / `origin/main` SHA after merge-closeout commit + SHA-chain fixup (full):**
  recorded by the SHA-chain-fixup commit that follows this merge-closeout
  on `main`. The fixup commit only edits §2 of this merge-closeout to
  insert the final-main SHA value; it does not change merge lifecycle
  semantics. Per the precedent set by Phase 4bb-F (`72d1710` fixup on
  top of `eddc28c` merge-closeout), Phase 4bj-G (`bb9e132` fixup on
  top of `73970af`), and Phase 4bj-F (`0a069e2` fixup on top of
  `9657651`), the merge-closeout commit (`b1c49a12fd931a64e9c7d46821739432acd94479`)
  is the canonical project-complete anchor.

## §3. Merge method

- **Merge command:**

  ```text
  git merge --no-ff -s ort \
    phase-4bb-f-implementation/gate-report-successor-state-writer-path-policy
  ```

- **Strategy:** `ort` (the Git default).
- **Merge commit message:**
  `docs(phase-4bb-f-implementation): merge gate report / successor-state writer path policy implementation`
- **`--no-verify`:** none.
- **`--no-gpg-sign`:** none.
- **`-c commit.gpgsign=false`:** none.
- **Force-push:** none.
- **Push status:** Pushed to `origin/main` with no force, no
  skip-hooks, no skip-signing.

## §4. Files brought forward by the merge

### 4.1 docs (5)

- `docs/00-meta/current-project-state.md` — narrow update (new
  Phase 4bb-F-implementation narrative paragraph + new "Current phase:"
  block; prior Phase 4bb-F "Current phase:" block preserved as
  historical context).
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bb-f-implementation_gate-report-successor-state-writer-path-policy.md`
  — the implementation memo (13 sections).
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bb-f-implementation_closeout.md`
  — the branch closeout.
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bb-f-implementation_merge-closeout.md`
  — this merge-closeout (added by the merge-closeout commit on `main`
  after the merge).

### 4.2 source (4)

- **New:** `src/prometheus/research/microstructure/canonical_paths.py`
  — pure path-policy helpers (`FAMILY_SUBDIRS`,
  `MICROSTRUCTURE_ROOT_PARTS`, `GATE_REPORTS_ROOT_PARTS`,
  `SUCCESSOR_STATE_ROOT_PARTS`, `CanonicalPathError`,
  `derive_short_commit`, `normalize_family`,
  `compose_canonical_gate_report_id`,
  `compose_canonical_successor_state_filename`,
  `derive_canonical_gate_report_path`,
  `derive_canonical_successor_state_path`, `derive_sidecar_path`,
  `compose_canonical_sidecar_body`, `write_paired_sha256_sidecar`,
  `assert_path_under_microstructure`,
  `assert_path_under_gate_reports_subdir`,
  `assert_path_under_successor_state`, `compute_file_sha256`).
- **Narrow modification:**
  `src/prometheus/research/microstructure/eligibility_report.py` —
  optional keyword-only `family_subdir: str | None = None` added to
  `write_report_atomic`; default preserves Phase 4bb-C placement
  exactly.
- **Narrow modification:**
  `src/prometheus/research/microstructure/eligibility_gate.py` —
  optional fields `family_subdir: str | None = None` and
  `phase_id: str | None = None` added to
  `AggTradesEligibilityGateInput`; threaded through
  `run_eligibility_gate`; `_make_report_id` gained optional `phase_id`
  kwarg.
- **Narrow modification:**
  `src/prometheus/research/microstructure/__init__.py` — re-exports the
  canonical-path public API with stable aliases
  (`assert_canonical_path_under_microstructure`,
  `compute_canonical_file_sha256`); package docstring extended with a
  Phase 4bb-F-implementation section.

### 4.3 tests (2)

- **New:** `tests/research/microstructure/test_canonical_paths.py` —
  47 tests covering family-subdir mapping, root-parts tuples, family
  normalisation, `derive_short_commit` validation, canonical
  gate-report id, canonical successor-state filename, canonical path
  placement per family, sidecar derivation / format / atomic write /
  refuse-overwrite / explicit-overwrite-allowed / parents-mkdir /
  non-Path rejection, path validation helpers.
- **New:**
  `tests/research/microstructure/test_eligibility_report_canonical_subdir.py`
  — 19 tests covering writer default preserves legacy `gate-reports/`;
  writer with each `family_subdir` produces canonical placement; writer
  rejects empty / separator-containing `family_subdir`; writer still
  validates `output_root` under microstructure; writer with canonical
  placement writes sidecar correctly and refuses overwrite; GateInput
  defaults; GateInput accepts and validates `family_subdir` +
  `phase_id`; orchestrator default preserves legacy doubled-path
  placement and legacy report-id format; orchestrator with canonical
  kwargs produces non-doubled canonical placement, canonical
  `phase-<id>` report-id, two-space + trailing-newline sidecar,
  manifest immutability preserved, `research_eligible_after = False` /
  `no_successor_authorization = True` preserved.

### 4.4 scripts

None.

### 4.5 config

None. `pyproject.toml` unchanged. `README.md` unchanged. `.gitignore`
unchanged. No `.mcp.json` change.

### 4.6 Explicit `data/microstructure/` statement

**No file under `data/microstructure/` was modified by this merge.**
The merge added no raw zip, no parquet, no sidecar, no manifest, no
gate report, no successor-state JSON. The Phase 4bb-D doubled-path
artefact at
`data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`
(SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`)
remains valid at its recorded path. All seven prior local gitignored
artefacts (4 gate reports + 3 successor-state JSONs) remain valid at
their recorded paths and SHA256 digests. No migration was performed.

### 4.7 Explicit prior governance memo statement

No prior governance memo was modified beyond the narrow Phase
4bb-F-implementation paragraph addition to
`docs/00-meta/current-project-state.md`. Phase-gates document,
technical-debt register, AI coding handoff, implementation ambiguity
log, all prior phase memos and closeouts, and all prior merge-closeouts
remain unchanged.

### 4.8 Explicit prior source / test / script statement

No prior source module was modified outside the three narrow edits
listed in §4.2. No prior test was modified. No script was added or
modified.

## §5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 301 +++++++++++++
 ...26-05-11_phase-4bb-f-implementation_closeout.md |  99 +++++
 ...te-report-successor-state-writer-path-policy.md | 342 ++++++++++++++
 src/prometheus/research/microstructure/__init__.py |  74 +++
 .../research/microstructure/canonical_paths.py     | 412 +++++++++++++++++
 .../research/microstructure/eligibility_gate.py    |  61 ++-
 .../research/microstructure/eligibility_report.py  |  45 +-
 .../microstructure/test_canonical_paths.py         | 494 +++++++++++++++++++++
 .../test_eligibility_report_canonical_subdir.py    | 382 ++++++++++++++++
 9 files changed, 2202 insertions(+), 8 deletions(-)
```

The diff matches the expected change set from the authorization
prompt: canonical-path helper source module + narrow raw-gate writer /
orchestrator / `__init__.py` updates + new canonical-path tests + new
canonical raw-placement tests + Phase 4bb-F-implementation docs +
narrow `current-project-state.md` update.

## §6. Result / verdict

**CODE LANDED.** Phase 4bb-F-implementation lands the prospective
Phase 4bb-F canonical path policy in code as a narrow,
backward-compatible safe subset of Option C: a new pure-path helper
module (`canonical_paths.py`) and two optional keyword-only kwargs
(`family_subdir`, `phase_id`) threaded through the raw-gate writer
(`eligibility_report.write_report_atomic`) and the raw-gate orchestrator
(`eligibility_gate.run_eligibility_gate` via the
`AggTradesEligibilityGateInput` dataclass). Default behaviour preserves
Phase 4bb-C placement verbatim — every existing call site, the Phase
4bb-D recorded doubled-path artefact, and the seven prior local
gitignored artefacts continue to be valid without modification. Future
raw-gate executions can opt into canonical placement under
`data/microstructure/gate-reports/raw/<canonical-filename>.json` with
phase-tagged report identifiers
(`<family>__<version>__phase-<id>__<unix_ms>__<short_commit>`). The
project lifecycle conclusion is **remain paused.** No artefact was
migrated, no gate was rerun, no manifest was mutated, no
`research_eligible` flag was flipped, no `eligibility_gate_status` was
transitioned, no `chronological_split_policy` was changed, no ML /
strategy / signal / backtest / acquisition / paper / shadow / live /
exchange-write was authorised or performed, and no successor phase is
authorised by this merge.

## §7. Local gitignored outputs

**None produced by this phase.** Phase 4bb-F-implementation is a
code + tests + docs implementation phase. It did not produce any new
local gitignored artefact under `data/microstructure/`. The seven prior
local gitignored artefacts (Phase 4bb-D raw gate report at the doubled
path; Phase 4bf derived gate report; Phase 4bi-B feature gate report;
Phase 4bj-E label gate report; Phase 4bg-B derived successor-state JSON;
Phase 4bi-D feature successor-state JSON; Phase 4bj-G label
successor-state JSON) remain valid at their recorded paths and SHA256
digests and were not touched.

## §8. Validation results

All validations were run after the `--no-ff` merge commit
(`ce20da7f5084fffe89adef6722c58a15dcbc4823`) was created on `main`:

- **`git diff --check` (post-merge):** clean.
- **`ruff check .` (whole repo, post-merge):** `All checks passed!`.
- **`mypy src/prometheus` (strict, post-merge):**
  `Success: no issues found in 120 source files`. (Was 119 prior to
  the merge; +1 for the new `canonical_paths.py` module.)
- **`pytest tests/research/microstructure/` (post-merge):**
  `915 passed, 1 skipped` — the one skip is the pre-existing labelled
  `pytest.skip` placeholder in
  `tests/research/microstructure/test_label_gate_report.py`. No new
  regressions.
- **`pytest` (whole repo, post-merge):**
  `1698 passed, 1 skipped, 2 failed`. The two failures are the
  unchanged pre-existing simulation `KeyError: 'trade_count'` failures
  in `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
  and `::test_real_2026_03_ethusdt`, caused by an unrelated schema
  mismatch in `src/prometheus/research/data/storage.py:232`. **Zero new
  test regressions from Phase 4bb-F-implementation or the merge.**
- **`git status` (post-merge):** only the always-untracked
  `.claude/scheduled_tasks.lock` and the gitignored `data/research/`
  tree.
- **`git check-ignore -v data/microstructure/`:** confirmed gitignored
  under `.gitignore:85: data/microstructure/`.

## §9. Upstream immutability evidence

Phase 4bb-F-implementation made no change to any data artefact, raw
zip, parquet, manifest, sidecar, gate report, or successor-state JSON
under `data/microstructure/`. The seven prior local gitignored artefacts
were preserved by construction (the implementation modifies no file
under `data/microstructure/` and never invokes any gate). The recorded
SHA256 digests for those artefacts (Phase 4bb-D `96f09159…`, Phase 4bf
`dd4e0c1c…`, Phase 4bi-B `aa5d29c2…`, Phase 4bj-E `b0b5405b…`,
Phase 4bg-B `8bcc7d01…`, Phase 4bi-D `8176aa3f…`, Phase 4bj-G
`ce7d3917…`) remain authoritative; no migration was performed.

## §10. Manifest state preservation

n/a. Phase 4bb-F-implementation modifies no manifest under
`data/microstructure/manifests/`. All in-scope manifest states are
preserved by construction:

- raw manifest `microstructure_raw_aggtrades_v001__v001.json`:
  `research_eligible = false`, `eligibility_gate_status = "pending"`,
  governance labels unchanged.
- derived manifest `microstructure_normalized_aggtrades_v001__v001.json`:
  `research_eligible = false`, `eligibility_gate_status = "pending"`,
  governance labels unchanged.
- feature manifest `microstructure_features_aggtrades_v001__v001.json`:
  `research_eligible = false`, `eligibility_gate_status = "pending"`,
  governance labels unchanged.
- label manifest `microstructure_labels_aggtrades_v001__v001.json`:
  `research_eligible = false`, `eligibility_gate_status = "pending"`,
  `chronological_split_policy = "not_yet_defined"`, governance labels
  unchanged.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).

## §11. Boundary confirmations

The merge honoured every Phase 4bb-F-implementation boundary verbatim:

- no `data/microstructure/` artefact was committed;
- no manifest was mutated;
- no sidecar was modified;
- no parquet was modified;
- no raw zip was modified;
- `research_eligible` was not flipped on any family;
- `eligibility_gate_status` was not transitioned on any actual manifest;
- `chronological_split_policy` was not changed on any actual manifest;
- no gate was rerun (raw / derived / feature / label);
- no new gate report was created;
- no new successor-state artefact was created;
- no existing artefact was moved, copied, renamed, deleted, or
  migrated;
- no ML model was designed, trained, ranked, or selected;
- no meta-labeling was created;
- no strategy was created;
- no signal was computed;
- no backtest was run;
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge /
  prediction / model-score / decision-score / entry-exit / strategy
  output was computed;
- no data was acquired;
- no Binance endpoint, public endpoint, or private endpoint was called;
- no authenticated API was used;
- no user stream / WebSocket / listenKey was opened;
- no credential was created or read;
- no `.env` was created or modified;
- no `.mcp.json` was created or modified;
- no MCP was enabled, queried, or modified;
- no Graphify was enabled or queried;
- no project lock was modified;
- no retained verdict was revised;
- no M0 governance was amended;
- no successor phase was authorized.

## §12. Retained verdict ledger

Every retained verdict is preserved verbatim across this merge:

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6 cost-sensitivity blocks.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other.
- **5m research thread** — OPERATIONALLY CLOSED per Phase 3t.
- **V2** — HARD REJECT (terminal for V2 first-spec).
- **G1** — HARD REJECT (terminal for G1 first-spec).
- **C1** — HARD REJECT (terminal for C1 first-spec).

## §13. Preserved project locks

Every project lock is preserved verbatim across this merge:

- **§11.6** — HIGH cost = 8 bps slippage per side.
- **round-trip** — 16 bps.
- **§1.7.3** — 0.25% risk per trade; 2× leverage cap; one position max;
  mark-price stops.
- **Phase 3p §4.7** — strict integrity gate (aggTrades equivalent
  applied verbatim).
- **Phase 3r §8** — mark-price gap governance.
- **Phase 3v §8** — stop-trigger-domain governance.
- **Phase 3w §6 / §7 / §8** — break-even / EMA slope / stagnation
  governance.
- **Phase 4j §11** — metrics OI-subset partial-eligibility rule.
- **Phase 4k** — V2 backtest-plan methodology.
- **Phase 4p** — G1 strategy-spec memo.
- **Phase 4q** — G1 backtest-plan methodology.
- **Phase 4v** — C1 strategy-spec memo.
- **Phase 4w** — C1 backtest-plan methodology.
- **Phase 4ak M0** — twelve-clause mechanism-admissibility gate +
  post-null cooldown rule + cooled-down families list + memo template.
- **Phase 4al** — refined no-rescue rule + §13 boundary + §14 hierarchy.
- **Phase 4aw** — `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant.
- **All prior phase results** (Phase 4am .. Phase 4bb-F) — preserved
  verbatim.

## §14. No-rescue constraints

This merge does NOT authorize and CANNOT be construed as authorizing:

- ML training, ML model selection, feature ranking, meta-labeling, or
  any ML implementation phase;
- strategy hypothesis generation, strategy spec authoring, or strategy
  implementation;
- signal construction, signal generation, or signal evaluation;
- backtest design, backtest execution, or backtest reporting;
- paper / shadow / live-readiness / deployment / exchange-write;
- Phase 4 canonical;
- Phase 5;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- old-strategy alt-symbol rerun (R2 / F1 / D1-A / V2 / G1 / C1);
- reopening any cooled-down family;
- reopening the 5m research thread (Phase 3t closure preserved);
- manifest transition (`research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`) from QA evidence alone;
- production-key creation, authenticated APIs, private endpoints,
  user-stream / WebSocket implementation, MCP, Graphify, `.mcp.json`,
  credentials;
- migration of any existing local gitignored artefact.

## §15. Successor authorization

**None.**

Candidate successor phases that are explicitly **not authorized** by
this merge include:

- **Phase 4bb-G** — raw-manifest successor-state recording.
- **Phase 4bj-H** — label-family evaluation, ML, or strategy from
  label artefacts.
- **A future raw-gate rerun under canonical placement** — the
  canonical-path machinery is available, but no authorization to
  invoke it exists.
- **A future canonical-successor-state writer module** — the
  `derive_canonical_successor_state_path` helper is available, but no
  authorization to build a writer or invoke it exists.
- **A migration phase** to move the Phase 4bb-D doubled-path artefact
  to canonical placement — explicitly NOT recommended (Phase 4bb-F §6
  recommends preserving the existing artefact at its recorded path).
- **Phase 5 / Phase 4 canonical** — strategy / live readiness phases.
- **Any ML / strategy / signal / backtest / acquisition / paper /
  shadow / live / exchange-write phase.**

## §16. Recommended state

**Remain paused.**

The canonical path policy helpers are now available on `main` for any
future authorised raw-gate execution and for any future canonical
successor-state writer. The Phase 4bb-D doubled-path artefact remains
preserved at its recorded path and SHA256 digest, in line with the
Phase 4bb-F §6 recommendation against migration. No successor phase
work is authorised.
