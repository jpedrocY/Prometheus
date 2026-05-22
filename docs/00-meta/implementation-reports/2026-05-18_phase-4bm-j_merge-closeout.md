# Phase 4bm-J Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-J — Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution
- **Tier**: **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bi-B feature-family eligibility gate precedent.
- **Type**: code + tests + docs + local gitignored feature-family gate report. Tracked code/tests/script/docs are committed; the gate report + paired canonical Phase 4bb-F sidecar remain gitignored under `.gitignore:85` (`data/microstructure/`) and are NOT committed.
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-J as project-complete on `main` after a clean code + tests + docs + local gitignored gate-report branch that designs, implements, and runs the first multi-day v002 feature-family eligibility gate over the Phase 4bm-H v002 feature artefacts (90 per-day Parquets + 90 sidecars + 1 feature manifest + 1 manifest sidecar; 155,153,449 rows; BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28). Phase 4bm-J reaches **v002 Feature Stage-4 (eligibility-gate-passed)** at the report level only.
- **Branch merged**: `phase-4bm-j/multi-day-v002-feature-family-eligibility-gate`
- **Target branch**: `main`
- **Base**: `main` at `3212722a7ffdd572ac2291ba1500f63f6fad6c59` (Phase 4bm-I merge-closeout SHA-finalization commit)
- **Predecessor**: Phase 4bm-I (Multi-Day V002 Feature Artefact Structural QA Memo; project-complete on `main`; verdict FEATURE_STRUCTURAL_QA_PASS)
- **Direct v001 precedent**: Phase 4bi-B (v001 feature-family eligibility gate)

**Phase 4bm-J is a feature-family eligibility gate phase only.** **Gate verdict: FEATURE_GATE_PASS.** **FEATURE_GATE_PASS is report-level only.** **Phase 4bm-K is not authorized by Phase 4bm-J.** **Feature-family research-use is not authorized by Phase 4bm-J.** **Feature-family successor-state recording is not authorized by Phase 4bm-J.** **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-J.** **No feature artefact was modified.** **No upstream artefact was mutated.** **No data/microstructure file was committed.**

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-J is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `3212722a7ffdd572ac2291ba1500f63f6fad6c59`
- **Pre-merge `origin/main` SHA**: `3212722a7ffdd572ac2291ba1500f63f6fad6c59` (in sync; verified)
- **Phase 4bm-J branch commit 1 SHA**: `2771890` (`feat(phase-4bm-j): implement multi-day v002 feature-family eligibility gate`; 12 files / +3,288; 4 modules + 1 script + 1 fixture + 5 tests + 1 `__init__.py` modification)
- **Phase 4bm-J branch commit 2 SHA**: `81b7495` (`docs(phase-4bm-j): add gate report and closeout`; 3 files / +782; main implementation report + closeout + `current-project-state.md` narrow update)
- **Phase 4bm-J branch tip SHA pre-merge**: `81b74951204f82563a8593210bbb2487c215fa28`
- **Merge commit SHA**: `2fe5e5949ddd7aedf8e2ba60f5dc88f2afc550ec`
- **Merge commit message**: `feat(phase-4bm-j): merge multi-day v002 feature-family eligibility gate`
- **Post-merge `main` SHA (after merge commit, pre-closeout-commit)**: `2fe5e5949ddd7aedf8e2ba60f5dc88f2afc550ec`
- **Post-merge `origin/main` SHA (after `git push origin main` of the merge commit)**: `2fe5e5949ddd7aedf8e2ba60f5dc88f2afc550ec` (in sync; pushed cleanly via `3212722..2fe5e59  main -> main`; no force, no skip-hooks, no skip-signing)
- **Merge-closeout commit SHA**: `9af355c3f3f7d93c84ba23e93819a7e1ced74db5` (`docs(phase-4bm-j): add merge closeout`; 1 file / +321; this file's commit on `main`)
- **Post-merge-closeout-commit `main` SHA**: `9af355c3f3f7d93c84ba23e93819a7e1ced74db5`
- **Post-merge-closeout-commit `origin/main` SHA**: `9af355c3f3f7d93c84ba23e93819a7e1ced74db5` (pushed cleanly via `2fe5e59..9af355c  main -> main`; no force, no skip-hooks, no skip-signing)
- **Final `main == origin/main` after closeout push**: true (both at `9af355c3f3f7d93c84ba23e93819a7e1ced74db5` immediately after the merge-closeout commit + push; the subsequent SHA-finalization commit then advances `main` and `origin/main` together by one additional commit, recorded in the final operator report)

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-j/multi-day-v002-feature-family-eligibility-gate -m "feat(phase-4bm-j): merge multi-day v002 feature-family eligibility gate"`
- **Strategy**: `ort` (git default)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing. First push (merge commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     3212722..2fe5e59  main -> main
  ```
  Second push (this merge-closeout commit) output:
  ```
  To https://github.com/jpedrocY/Prometheus.git
     2fe5e59..9af355c  main -> main
  ```

## §4 Files Brought Forward by the Merge

Fifteen tracked files brought forward from the Phase 4bm-J branch into `main`, across the two source-branch commits (`2771890` feat + `81b7495` docs).

**Tracked source / script / fixture / test files added (12):**

1. `src/prometheus/research/microstructure/multiday_feature_gate_io.py` (NEW, +248; path discipline, SHA256 helpers, JSON / sidecar atomic writers with refuse-to-overwrite, canonical Phase 4bb-F sidecar composer, report-id derivation).
2. `src/prometheus/research/microstructure/multiday_feature_gate_report.py` (NEW, +434; `MultidayFeatureGateReport` frozen data model with hard-invariant enforcement, `_classify_gate_verdict`, `build_report`, `write_gate_report`).
3. `src/prometheus/research/microstructure/multiday_feature_gate_checks.py` (NEW, +957; 50 check functions A1..G6, `MultidayFeatureGateCheckStatus`, `MultidayFeatureGateCheckResult`, `MultidayFeatureGateContext`, `CHECK_ORDER`, `SAMPLE_DATES`, `EXPECTED_*` locked constants, `run_all_checks`).
4. `src/prometheus/research/microstructure/multiday_feature_gate.py` (NEW, +194; `MultidayFeatureGateInput`, `MultidayFeatureGateResult`, `MultidayFeatureGateError`, `run_multiday_feature_family_gate`).
5. `scripts/phase4bm_j_run_multiday_feature_gate.py` (NEW, +156; standalone offline gate runner; emits single deterministic local gitignored gate report + paired sidecar).
6. `tests/research/microstructure/_multiday_feature_gate_fixtures.py` (NEW, +436; shared fixture builder).
7. `tests/research/microstructure/test_multiday_feature_gate_io.py` (NEW, +134; 12 tests).
8. `tests/research/microstructure/test_multiday_feature_gate_report.py` (NEW, +196; 9 tests).
9. `tests/research/microstructure/test_multiday_feature_gate_checks.py` (NEW, +165; 18 tests).
10. `tests/research/microstructure/test_multiday_feature_gate.py` (NEW, +185; 9 tests).
11. `tests/research/microstructure/test_multiday_feature_gate_no_network.py` (NEW, +105; 6 parametrized tests).

(53 new tests total; all PASS.)

**Tracked source files modified narrowly (1):**

12. `src/prometheus/research/microstructure/__init__.py` (MODIFIED, +78; re-exports the Phase 4bm-J public API).

**Tracked docs files added (2):**

13. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-j_multi-day-v002-feature-family-eligibility-gate.md` (NEW, +313; the main implementation report).
14. `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-j_closeout.md` (NEW, +151; closeout).

**Tracked docs files modified narrowly (1):**

15. `docs/00-meta/current-project-state.md` (MODIFIED, +318; Phase 4bm-J narrative paragraph + new "Current phase:" block; prior Phase 4bm-I "Current phase:" block preserved as labelled historical context).

**No** `data/microstructure/` artefact is committed by this merge. **No** source / test / script / configuration file outside the above 15-file set is modified. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, and every other tracked file outside the above list are unchanged.

## §5 Diff Summary

`git diff --stat 3212722..2fe5e59` (against pre-merge `main`):

```text
 docs/00-meta/current-project-state.md              | 318 +++++++
 .../2026-05-18_phase-4bm-j_closeout.md             | 151 ++++
 ...lti-day-v002-feature-family-eligibility-gate.md | 313 +++++++
 scripts/phase4bm_j_run_multiday_feature_gate.py    | 156 ++++
 src/prometheus/research/microstructure/__init__.py |  78 ++
 .../microstructure/multiday_feature_gate.py        | 194 +++++
 .../microstructure/multiday_feature_gate_checks.py | 957 +++++++++++++++++++++
 .../microstructure/multiday_feature_gate_io.py     | 248 ++++++
 .../microstructure/multiday_feature_gate_report.py | 434 ++++++++++
 .../_multiday_feature_gate_fixtures.py             | 436 ++++++++++
 .../microstructure/test_multiday_feature_gate.py   | 185 ++++
 .../test_multiday_feature_gate_checks.py           | 165 ++++
 .../test_multiday_feature_gate_io.py               | 134 +++
 .../test_multiday_feature_gate_no_network.py       | 105 +++
 .../test_multiday_feature_gate_report.py           | 196 +++++
 15 files changed, 4070 insertions(+)
```

No deletions. No `data/microstructure/` path appears. `git diff --check` produces no whitespace or conflict-marker findings.

## §6 Result / Verdict / Decision

**Phase 4bm-J is project-complete on `main`.** **Gate verdict: FEATURE_GATE_PASS.** **overall_status = pass.** **50 / 50 checks PASS** (0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking failures). The v002 multi-day derived family now carries a complete ladder of evidence through **v002 Feature Stage-4** at report level:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3: Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts.
- v002 Feature Stage-3: Phase 4bm-I FEATURE_STRUCTURAL_QA_PASS.
- v002 **Feature Stage-4 (eligibility-gate-passed at report level)**: Phase 4bm-J **FEATURE_GATE_PASS** (this phase).

**FEATURE_GATE_PASS is report-level only.** It does not authorize feature-family research-use, successor-state recording, labels, diagnostics, ML, strategy, or backtests. v002 Feature Stage-5 (research-use-cleared), Stage-6 (successor-state-marked), and overall Stage-4 feature-cleared on the manifest remain **unauthorized**.

## §7 Local Gitignored Outputs

Phase 4bm-J produced 2 local gitignored artefacts (gate report + sidecar), both under `data/microstructure/gate-reports/features/` and both covered by `.gitignore:85` (`data/microstructure/`). **None are committed.**

- **Gate report path**: `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json`
- **Gate report SHA256**: `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`
- **Gate report size**: 16,176 bytes
- **Gate report sidecar path**: `<report>.json.sha256`
- **Gate report sidecar SHA256**: `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`
- **Gate report sidecar size**: 158 bytes
- **Gate report sidecar exact content** (canonical Phase 4bb-F format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`):
  ```text
  3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242  microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json
  ```
  (66 + 92 = 158 bytes; ASCII only; no BOM; LF only; exactly two ASCII spaces between SHA and basename; trailing LF.)

Confirmation: `git check-ignore -v data/microstructure/`, `data/microstructure/gate-reports/`, `data/microstructure/gate-reports/features/`, the gate report path, and the sidecar path all return `.gitignore:85: data/microstructure/`.

## §8 Gate Check Summary

| Group | Count | Scope | Result |
| --- | --- | --- | --- |
| **A** Locked preconditions | 12 | Phase 4bm-G / 4bm-H / 4bm-I lineage SHA + verdict preconditions | 12 / 12 PASS |
| **B** Inventory / sidecar / gitignore | 10 | 90 feature parquets + 90 sidecars present; canonical date inventory; BTCUSDT only; per_day_outputs length 90 + unique dates; all sidecars canonical + SHA-consistent; all per-day parquet SHAs match manifest | 10 / 10 PASS |
| **C** Schema / lineage / forbidden | 10 | 62-column total; canonical column order; 17 lineage + 45 feature/quality counts; safe `source_phase_4bm_e_outcome` present; unsafe `source_phase_4bm_e_decision` absent; 0 forbidden-substring hits; feature_config_hash matches; dataset identity literals match; all 90 parquets share canonical 62-column schema | 10 / 10 PASS |
| **D** Row-count / partition / timestamp | 6 | Total 155,153,449; sum(per_day_outputs.row_count) == total; per-day == source normalized (90/90); no zero-row day; pyarrow num_rows matches (90/90); 6 sample dates pass all partition/timestamp/lineage invariants | 6 / 6 PASS |
| **E** Quality flags / cross-day boundary | 3 | Day 1 `rolling_missing_window_flag` rule matches `(T - 60_000) < day_start_ms`; days 2..90 sampled all False; `invalid_window_flag = False` on every sampled day | 3 / 3 PASS |
| **F** Upstream immutability | 3 | All 90 v002 normalized per-day Parquets byte-identical to derived manifest; v002 derived + raw manifest preserve `research_eligible=false / eligibility_gate_status="pending"` | 3 / 3 PASS |
| **G** Non-authorization invariants | 6 | Feature manifest `research_eligible=false` / `eligibility_gate_status="pending"` / `stage_4_feature_cleared=false`; all 7 non-authorization flags false; all 5 immutability flags true; 18 boundary_confirmations all True | 6 / 6 PASS |
| **Total** | **50** | | **50 / 50 PASS** |

- **PASS count**: 50
- **FAIL count**: 0
- **ERROR count**: 0
- **NOT_APPLICABLE count**: 0
- **Blocking failures**: 0
- **Gate verdict**: **FEATURE_GATE_PASS**

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
- Schema column count: 62 (17 lineage + 45 feature/quality)

## §10 Boundary Statements (required exact phrases)

The following phrases appear verbatim:

- **Phase 4bm-J is a feature-family eligibility gate phase only.**
- **Gate verdict: FEATURE_GATE_PASS.**
- **FEATURE_GATE_PASS is report-level only.**
- **Phase 4bm-K is not authorized by Phase 4bm-J.**
- **Feature-family research-use is not authorized by Phase 4bm-J.**
- **Feature-family successor-state recording is not authorized by Phase 4bm-J.**
- **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-J.**
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
- no labels / diagnostics / ML / strategy / backtest / acquisition work was authorized or performed.

## §11 Upstream Lineage SHA Table

All upstream artefacts are byte-identical pre- and post-Phase-4bm-J. Recomputed SHA256 on disk at merge time matches the expected value byte-for-byte.

| Artefact | SHA256 | Status |
| --- | --- | --- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | unchanged |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | unchanged |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged |
| Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged |
| Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | unchanged |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | unchanged |
| Phase 4bm-F v002 successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | unchanged |
| Phase 4bm-F v002 successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | unchanged |

90 / 90 v002 normalized per-day Parquets byte-identical (verified by Group F.1 check). The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and was **never invoked**.

## §12 Validation Results

- `git diff --check main..phase-4bm-j/multi-day-v002-feature-family-eligibility-gate`: clean (no whitespace, no conflict markers).
- `git diff main..phase-4bm-j/... --name-only`: exactly 15 paths (12 source/script/test/fixture + 1 `__init__.py` + 2 docs); no `data/microstructure/` path.
- `git status --short` after merge: only the two expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); no tracked changes; no `data/microstructure/` artefact visible (gitignored).
- `git check-ignore -v` on all five v002 / gate-report paths returns `.gitignore:85: data/microstructure/`.
- Gate report JSON parses cleanly; `gate_verdict == "FEATURE_GATE_PASS"`; `overall_status == "pass"`; `pass_count == 50`; `fail_count == 0`; `error_count == 0`; `not_applicable_count == 0`; `blocking_fail_count == 0`; `len(checks) == 50`; all 8 non-authorization flags `false`; all 14 immutability flags `true`.
- v002 feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false`; `feature_config_hash == 819cfa7a…`; `actual_feature_row_count == 155153449`; `per_day_outputs` length 90.

## §13 Quality Gate Commands and Results

- Phase 4bm-J surface `ruff check` (11 paths): **All checks passed!**
- Whole-repo `ruff check .`: **All checks passed!**
- `pytest tests/research/microstructure/test_multiday_feature_gate*.py`: **53 passed in 7.40s**.
- **mypy skipped at merge time** per the Phase 4bm-H baseline rationale: Phase 4bm-J adds new isolated modules without modifying existing source. The Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files; 28 pre-existing v001 / labels / httpx baseline + 8 in `features_compute_v002.py` mirroring v001 idiom) is preserved by construction. The Phase 4bm-J branch report indicated no new mypy category is expected.
- **Whole-repo `pytest` skipped at merge time** per the Phase 4bm-H baseline rationale: 15 collection errors from missing `httpx` / `duckdb` env modules + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures (both env baseline). Targeted Phase 4bm-J pytest (53 PASS) is the relevant verification surface for the new modules; the baseline failures cannot be regressed by Phase 4bm-J because no existing source / test is modified.

These skips conform to the project's standing precedent for Tier 1 code-and-gate-report phases that produce a single deterministic gate output (Phase 4bi-B v001 feature-family gate precedent; Phase 4bm-D multi-day derived-family gate precedent).

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked**).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..F / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I results — all preserved verbatim.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN** (no prior gate is rerun; this is the first v002 feature-family gate), **N-SUCCESSOR-STATE**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**. **N-DERIVATION** does NOT apply — Phase 4bm-J inspects existing artefacts but does not normalize / derive / compute features / labels.

## §15 Recommended State

**Remain paused.**

Phase 4bm-J is project-complete on `main` by this merge + merge-closeout. The operator's broader pause decision continues to apply.

## §16 Conditional Next Options (none authorized)

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | n/a | **recommended** |
| Future **Phase 4bm-K — Multi-Day V002 Feature-Family Research-Use Decision Memo** (multi-day analogue of Phase 4bi-C) | docs-only | **NOT authorized by this merge** |
| Future v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D) | docs + local gitignored successor-state JSON | **NOT authorized by this merge** |
| Future multi-day v002 label-family phases (multi-day analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by this merge** |
| Additional acquisition / cross-symbol / mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated APIs / private endpoints | docs + data | **NOT authorized by this merge** |
| Label computation, diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this merge** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this merge** |

## §17 Explicit Non-Authorization

This merge does **not**, and **cannot**, authorize:

- Phase 4bm-K (the canonical conditional successor; the multi-day v002 feature-family research-use decision memo);
- v002 feature-family research-use;
- v002 feature-family successor-state recording;
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
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, Phase 4bm-H feature computation, Phase 4bm-I structural QA verdict, or Phase 4bm-J gate verdict;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.
