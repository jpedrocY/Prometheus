# Phase 4bm-K Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-K — Multi-Day V002 Feature-Family Research-Use Decision Memo
- **Tier**: **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bi-C v001 feature-family research-use / ML-use decision memo precedent. First-of-kind multi-day v002 feature-family research-use governance / admissibility decision.
- **Type**: docs-only research-use decision / governance memo. No source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file modified. No `data/microstructure/` artefact committed.
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-K as project-complete on `main` after a clean docs-only branch that records a policy-level Stage-5 admissibility decision for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002` (90 per-day Parquets + 90 sidecars + 1 feature manifest + 1 manifest sidecar; 155,153,449 rows; BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28). Phase 4bm-K reaches **v002 Feature Stage-5 admissibility-in-principle at policy level only**; no machine-readable Stage-5 marker is created.
- **Branch merged**: `phase-4bm-k/multi-day-v002-feature-family-research-use-decision-memo`
- **Target branch**: `main`
- **Base**: `main` at `89bf2cfb45b7c46f77e23669570e9f380c6a2e91` (Phase 4bm-J merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-J (Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution; project-complete on `main`; verdict FEATURE_GATE_PASS)
- **Direct v001 precedent**: Phase 4bi-C (v001 feature-family research-use / ML-use decision memo; Outcome 1 / Decision form 1)

**Phase 4bm-K is a docs-only research-use decision / governance memo only.** **Recorded decision: Outcome 1 / Decision form 1 — equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`.** **Feature-family research-use is approved in principle at policy level only.** **No machine-readable research-use marker exists after Phase 4bm-K.** **Phase 4bm-L is not authorized by Phase 4bm-K.** **Successor-state recording is not authorized by Phase 4bm-K.** **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-K.** **No feature artefact was modified.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-K is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `89bf2cfb45b7c46f77e23669570e9f380c6a2e91`
- **Pre-merge `origin/main` SHA**: `89bf2cfb45b7c46f77e23669570e9f380c6a2e91` (in sync; verified)
- **Phase 4bm-K branch commit SHA**: `ecfb8841a22bac23d0fde7d1b4e32fe69896d178` (`docs(phase-4bm-k): add multi-day v002 feature-family research-use decision memo`; 3 files / +1022; the decision memo + closeout + narrow `current-project-state.md` update)
- **Phase 4bm-K branch tip SHA pre-merge**: `ecfb8841a22bac23d0fde7d1b4e32fe69896d178`
- **Merge commit SHA**: `a9f09ae7af3bf9a4cf74e6498f38eb092b67ac78`
- **Merge commit message**: `docs(phase-4bm-k): merge multi-day v002 feature-family research-use decision memo`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `a9f09ae7af3bf9a4cf74e6498f38eb092b67ac78`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `a9f09ae7af3bf9a4cf74e6498f38eb092b67ac78` (in sync; pushed cleanly via `89bf2cf..a9f09ae  main -> main`; no force, no skip-hooks, no skip-signing)
- **Merge-closeout commit SHA**: `feaeff3e557223d122c0383c67cdab6fbd5a2345` (`docs(phase-4bm-k): add merge closeout`; 1 file / +329; this file's commit on `main`)
- **Post-merge-closeout-commit `main` SHA**: `feaeff3e557223d122c0383c67cdab6fbd5a2345`
- **Post-merge-closeout-commit `origin/main` SHA**: `feaeff3e557223d122c0383c67cdab6fbd5a2345` (pushed cleanly via `a9f09ae..feaeff3  main -> main`; no force, no skip-hooks, no skip-signing)
- **Final `main == origin/main` after closeout push**: true (both at `feaeff3e557223d122c0383c67cdab6fbd5a2345` immediately after the merge-closeout commit + push; the subsequent SHA-finalization commit then advances `main` and `origin/main` together by one additional commit, recorded in the final operator report)

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-k/multi-day-v002-feature-family-research-use-decision-memo -m "docs(phase-4bm-k): merge multi-day v002 feature-family research-use decision memo"`
- **Strategy**: `ort` (git default)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     89bf2cf..a9f09ae  main -> main
  ```
  Second push (this merge-closeout commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     a9f09ae..feaeff3  main -> main
  ```

## §4 Files Brought Forward by the Merge

Three tracked docs files brought forward from the Phase 4bm-K branch into `main`, all from the single source-branch commit (`ecfb884`).

**Tracked docs files added (2):**

1. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-k_multi-day-v002-feature-family-research-use-decision-memo.md` (NEW, +481; 22 sections; the main decision memo — phase identity, scope, linkage to Phase 4bm-J / 4bm-I / 4bm-H / 4bm-G / 4bm-F, linkage to v001 Phase 4bi-C precedent, evidence table, upstream lineage SHA table, decision criteria, decision analysis, final research-use decision, required affirmative-decision phrases, residual risks, what the decision proves, what the decision does not prove, non-authorization, recommended state, conditional next options, preserved boundaries, closeout / lock preservation).
2. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-k_closeout.md` (NEW, +159; 12 sections; closeout summarising branch name, base SHA, risk tier, tracked files, decision verdict, key evidence, validation results, quality gate results / skipped-check rationale, non-authorization boundaries, recommended state, explicit non-authorization statement, and the required affirmative-decision phrases).

**Tracked docs files modified narrowly (1):**

3. `docs/00-meta/current-project-state.md` (MODIFIED, +382; Phase 4bm-K narrative paragraph + new "Current phase:" block; prior Phase 4bm-J "Current phase:" block preserved as labelled historical context).

**No** `data/microstructure/` artefact is committed by this merge. **No** source / test / script / configuration file outside the above 3-file set is modified. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, and every other tracked file outside the above list are unchanged.

## §5 Diff Summary

`git diff --stat 89bf2cf..a9f09ae` (against pre-merge `main`):

```text
 docs/00-meta/current-project-state.md              | 382 ++++++++++++++++
 .../2026-05-18_phase-4bm-k_closeout.md             | 159 +++++++
 ...02-feature-family-research-use-decision-memo.md | 481 +++++++++++++++++++++
 3 files changed, 1022 insertions(+)
```

No deletions. No `data/microstructure/` path appears. `git diff --check` produces no whitespace or conflict-marker findings.

## §6 Result / Verdict / Decision

**Phase 4bm-K is project-complete on `main`.** **Recorded decision: Outcome 1 / Decision form 1 — equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`.**

> v002 Feature Stage-5 research-use admissibility is admissible in principle at policy level for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bm-L successor-state recording phase is required before any machine-readable v002 Feature Stage-5 marker exists.

Specifically:

- the v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` continues to carry `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false` (verified on disk at merge time; SHA256 `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` unchanged);
- **no machine-readable v002 Feature Stage-5 marker exists yet**;
- **no manifest mutation occurred** in Phase 4bm-K;
- **no successor-state JSON was created** by Phase 4bm-K (Phase 4bm-L is **not** authorized by Phase 4bm-K);
- labels / targets / ML / strategy / backtests / diagnostics / additional acquisition all remain forbidden / unauthorized;
- v002 Feature Stage-5 admissibility is **not** a strategy hypothesis, predictive claim, edge claim, backtest permission, or M0 bypass.

The v002 multi-day derived family now carries a complete ladder of evidence through **v002 Feature Stage-5 admissibility-in-principle at policy level only**:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3: Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts.
- v002 Feature Stage-3: Phase 4bm-I FEATURE_STRUCTURAL_QA_PASS.
- v002 Feature Stage-4 (eligibility-gate-passed at report level): Phase 4bm-J **FEATURE_GATE_PASS**.
- v002 **Feature Stage-5 admissibility decision (policy-level only; docs-only memo)**: Phase 4bm-K **Outcome 1 / Decision form 1** (this phase).

**FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE is POLICY-LEVEL ONLY.** It does not authorize feature-family successor-state recording, labels, diagnostics, ML, strategy, or backtests. v002 Feature Stage-6 (successor-state-marked) and overall Stage-4 feature-cleared on the manifest remain **unauthorized**.

## §7 Local Gitignored Outputs

Phase 4bm-K produced **zero** new local artefacts under `data/microstructure/`. The phase is a docs-only governance memo and reads upstream artefacts in read-only mode for SHA verification only.

The pre-existing local gitignored artefacts that Phase 4bm-K cites as locked input (all unchanged by this merge):

- Phase 4bm-J gate report: `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json` (SHA `3c59dfae…`; gitignored under `.gitignore:85`).
- Phase 4bm-J gate sidecar: `<report>.json.sha256` (SHA `14a17764…`; gitignored).
- v002 feature manifest: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` (SHA `512a0a54…`; gitignored).
- v002 feature manifest sidecar: `<manifest>.sha256` (SHA `22e2fb77…`; gitignored).
- 90 per-day v002 feature Parquets + 90 paired canonical Phase 4bb-F sidecars under `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/` (all gitignored).
- v002 derived multi-day index manifest + sidecar (SHA `01c5fa53…` / `d96f31ae…`; gitignored).
- v002 raw manifest + acquisition log (SHA `01696786…` / `52f6d7fb…`; gitignored).
- Phase 4bl-D-R raw multi-day PASS gate report (SHA `f9493fd1…`; gitignored).
- Phase 4bl-E raw multi-day successor-state JSON (SHA `a0576ca6…`; gitignored).
- Phase 4bm-D authoritative derived-family gate report + sidecar (SHA `3b45e70b…` / `8e74261c…`; gitignored).
- Phase 4bm-F v002 derived-family Stage-3 successor-state JSON + sidecar (SHA `72b6edd4…` / `1e9ffb23…`; gitignored).

Confirmation: `git check-ignore -v data/microstructure/`, every subnamespace under it, and every path above all return `.gitignore:85: data/microstructure/`. **None are committed** by this merge.

## §8 Phase 4bm-K Decision Summary

| Attribute | Value |
| --- | --- |
| Decision verdict | **Outcome 1 / Decision form 1** (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) |
| Decision form | docs-only research-use admissibility memo at policy level only |
| Manifest mutation | none (forbidden by Phase 4bm-K scope) |
| Successor-state JSON | not created (forbidden by Phase 4bm-K scope) |
| Phase 4bm-L authorization | not granted |
| Labels / diagnostics / ML / strategy / backtests | not authorized |
| Additional acquisition | not authorized |
| Manifest `research_eligible` field | unchanged (`false`) |
| Manifest `eligibility_gate_status` field | unchanged (`pending`) |
| Manifest `stage_4_feature_cleared` field | unchanged (`false`) |
| Phase 4aw `flip_research_eligible(...)` invariant | preserved (never invoked) |

## §9 Feature Artefact Summary

- Feature manifest path: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`
- Feature manifest SHA256: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d`
- Feature manifest sidecar SHA256: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`
- feature_config_hash: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`
- Feature parquet count: **90**
- Feature sidecar count: **90**
- Total feature row count: **155,153,449**
- Date range: 2024-12-01 .. 2025-02-28 (90 contiguous UTC days)
- Symbol: BTCUSDT
- Schema column count: 62 (17 lineage / identity / metadata + 45 feature / quality)

The feature artefact set is the immutable Phase 4bm-H output preserved end-to-end through Phase 4bm-I structural QA, Phase 4bm-J eligibility gate, and now Phase 4bm-K research-use decision memo. Phase 4bm-K reads it in read-only mode for SHA verification only.

## §10 Boundary Statements (required exact phrases)

The following phrases appear verbatim in this merge-closeout per the task brief:

- **Feature-family research-use is approved in principle at policy level only.**
- **No machine-readable research-use marker exists after Phase 4bm-K.**
- **Phase 4bm-L is not authorized by Phase 4bm-K.**
- **Successor-state recording is not authorized by Phase 4bm-K.**
- **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-K.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

Additional preserved boundaries:

- no tracked `data/microstructure/` artefact changed by this merge;
- no generated feature artefact was committed;
- no gate report was committed;
- no feature artefact was modified;
- original v002 derived manifest unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- original v002 raw manifest unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"`;
- v002 feature manifest unchanged and still carries `research_eligible = false` / `eligibility_gate_status = "pending"` / `stage_4_feature_cleared = false`;
- Phase 4bm-F successor-state JSON unchanged;
- Phase 4bm-J gate report unchanged;
- no labels / diagnostics / ML / strategy / backtest / acquisition work was authorized or performed.

## §11 Upstream Lineage SHA Table

All upstream artefacts are byte-identical pre- and post-Phase-4bm-K. Recomputed SHA256 on disk at merge time matches the expected value byte-for-byte.

| Artefact | SHA256 | Status |
| --- | --- | --- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | unchanged |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | unchanged |
| Phase 4bm-J v002 feature-family gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | unchanged |
| Phase 4bm-J v002 feature-family gate sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | unchanged |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged |
| Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged |
| Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | unchanged |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | unchanged |
| Phase 4bm-F v002 derived-family Stage-3 successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | unchanged |
| Phase 4bm-F v002 derived-family Stage-3 successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | unchanged |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and was **never invoked**.

## §12 Validation Results

- `git diff --check main..phase-4bm-k/multi-day-v002-feature-family-research-use-decision-memo`: clean (no whitespace, no conflict markers).
- `git diff main..phase-4bm-k/... --name-only`: exactly 3 paths (2 new docs + 1 narrowly modified docs); no `data/microstructure/` path.
- `git diff main..phase-4bm-k/... --name-status`: 1 `M` (`current-project-state.md`) + 2 `A` (the two new memo files); no `D`, no `R`, no `C`.
- `git diff main..phase-4bm-k/... --stat`: `3 files changed, 1022 insertions(+)`; no deletions.
- `git status --short` after merge: only the two expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); no tracked changes; no `data/microstructure/` artefact visible (gitignored).
- `git check-ignore -v` on `data/microstructure/`, every subnamespace, and every upstream-artefact path: returns `.gitignore:85: data/microstructure/`.
- SHA256 verification of the v002 feature manifest, feature manifest sidecar, Phase 4bm-J gate report, Phase 4bm-J gate sidecar, v002 derived multi-day index manifest, v002 derived manifest sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-D-R raw multi-day gate report, Phase 4bl-E raw multi-day successor-state JSON, Phase 4bm-D gate report, Phase 4bm-D sidecar, Phase 4bm-F successor-state JSON, and Phase 4bm-F successor-state sidecar: **all 14 / 14 MATCH** the recorded values byte-for-byte.
- Feature manifest on-disk content invariants verified directly at merge time:
  - `research_eligible = false`
  - `eligibility_gate_status = "pending"`
  - `stage_4_feature_cleared = false`
  - `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`
  - `actual_feature_row_count = 155153449`
  - `symbol = "BTCUSDT"`
  - `per_day_outputs` length = 90
- Phase 4bm-J gate-report on-disk content invariants verified directly at merge time:
  - `gate_verdict = "FEATURE_GATE_PASS"`
  - `overall_status = "pass"`
  - `pass_count = 50`
  - `fail_count = 0`
  - `error_count = 0`
  - `not_applicable_count = 0`
  - `blocking_fail_count = 0`
  - `len(checks) = 50`
  - `research_eligible_after = false`
  - `stage_4_feature_cleared_after = false`

## §13 Quality Gate Commands and Results

- `git diff --check main..phase-4bm-k/multi-day-v002-feature-family-research-use-decision-memo`: **clean** (exit 0).
- Repo-standard markdown lint or check: **no project-specific lightweight markdown gate exists** in this repository; therefore none is run.

**Skipped checks (justified for docs-only governance / research-use decision memos):**

- `ruff check`: **skipped at merge time.** Phase 4bm-K modifies no Python source, tests, scripts, or configs. The Phase 4bm-K branch contains exactly 3 docs files; nothing under `src/prometheus/`, `tests/`, or `scripts/` is touched.
- `mypy src/prometheus`: **skipped at merge time.** Same rationale; no source-code touch. The Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files) is preserved by construction.
- `pytest` (targeted or whole-repo): **skipped at merge time.** Same rationale; no source / test / script touch. The Phase 4bm-J branch quality gates already locked the codebase status into the Phase 4bm-J merge-closeout on `main`:
  - Phase 4bm-J surface `ruff check` (11 paths): PASS.
  - Whole-repo `ruff check .`: PASS.
  - `pytest tests/research/microstructure/test_multiday_feature_gate*.py`: 53 PASS in 7.86 s.
  - Whole-repo `pytest`: 15 collection errors from missing `httpx` / `duckdb` env modules + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures (both env baseline). This baseline cannot regress in Phase 4bm-K because Phase 4bm-K modifies no existing source / test / script.

These skips conform to the project's standing precedent for Tier 1 docs-only governance / research-use decision memos (Phase 4bi-C v001 precedent; Phase 4bg-A v001 derived-family precedent; Phase 4bm-E v002 derived-family precedent).

## §14 Boundaries Preserved

All retained verdicts and project locks are preserved verbatim by this merge:

- H0 — FRAMEWORK ANCHOR.
- R3 — BASELINE-OF-RECORD.
- R1a / R1b-narrow — RETAINED — NON-LEADING.
- R2 — FAILED — §11.6.
- F1 — HARD REJECT.
- D1-A — MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread — OPERATIONALLY CLOSED (Phase 3t).
- V2 / G1 / C1 — HARD REJECT — terminal for first-spec.
- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked** by Phase 4bm-K).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..G / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J results — all preserved verbatim.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

## §15 Recommended State

**Remain paused.**

Phase 4bm-K is project-complete on `main` by this merge + merge-closeout. The operator's broader pause decision continues to apply.

## §16 Conditional Next Options (none authorized)

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | n/a | **recommended** |
| Future **Phase 4bm-L — Multi-Day V002 Feature-Family Research-Use Successor-State Recording** (v002 analogue of Phase 4bi-D) | docs + local gitignored successor-state JSON | **NOT authorized by this merge** |
| Future multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by this merge** |
| Future multi-day v002 chronological-split-policy memo | docs-only | **NOT authorized by this merge** |
| Additional acquisition / cross-symbol / mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated APIs / private endpoints | docs + data | **NOT authorized by this merge** |
| Label computation, diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this merge** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this merge** |

## §17 Explicit Non-Authorization

This merge does **not**, and **cannot**, authorize:

- Phase 4bm-L (Multi-Day V002 Feature-Family Research-Use Successor-State Recording; the canonical conditional successor; v002 analogue of Phase 4bi-D);
- v002 feature-family successor-state recording (any form);
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest;
- any multi-day v002 label-family phase;
- any multi-day v002 chronological-split-policy memo;
- labels;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
- additional acquisition;
- Phase 5;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- user-stream / live WebSocket implementation;
- public-endpoint calls in code;
- MCP / Graphify / `.mcp.json` / credentials;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, or the Phase 4bm-K decision verdict;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.
