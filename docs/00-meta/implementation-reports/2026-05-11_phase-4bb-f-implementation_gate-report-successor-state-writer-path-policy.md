# Phase 4bb-F-implementation — Gate Report / Successor-State Writer Path Policy Implementation

## §1. Phase identity

- **Phase name:** Phase 4bb-F-implementation — Gate Report / Successor-State Writer Path Policy Implementation
- **Phase type:** Implementation phase (code + tests + docs).
- **Scope:** Narrow, backward-compatible Option C of the Phase 4bb-F memo.
- **Authorization basis:** Phase 4bb-F merge-closeout
  (`docs/00-meta/implementation-reports/2026-05-11_phase-4bb-f_merge-closeout.md`)
  recorded the canonical path policy as binding. Phase 4bb-F-implementation
  realises the narrow safe subset of Option C: a docs + helper module + an
  optional, backward-compatible kwarg on the raw-gate writer / orchestrator
  that lets future raw-gate executions write under the canonical
  `data/microstructure/gate-reports/raw/...` path. No existing artefact is
  migrated, rerun, or rewritten. No new artefact is produced. No manifest
  is mutated. No successor phase is authorised.

## §2. Pre-state and base SHA

- **Main HEAD at start of phase:** `72d171060498769875ab892a886558af762b28f0`
  (the Phase 4bb-F merge-closeout SHA-chain-fixup commit).
- **Branch created:** `phase-4bb-f-implementation/gate-report-successor-state-writer-path-policy`
  from `main` at `72d1710`.
- **Working tree status pre-implementation:** clean apart from the always-untracked `.claude/scheduled_tasks.lock` and the gitignored `data/research/`.
- **Local microstructure data state unchanged.** The seven existing local
  gitignored artefacts produced by Phase 4bb-D, Phase 4bf, Phase 4bi-B,
  Phase 4bj-E, Phase 4bg-B, Phase 4bi-D, and Phase 4bj-G remain valid at
  their recorded paths and SHA256 digests. No artefact was migrated.

## §3. Why this phase exists

Phase 4bb-F locked a canonical path policy for gate reports and
successor-state JSON artefacts:

- gate-report root: `data/microstructure/gate-reports/<family-subdir>/`
- family subdirs: `raw/`, `normalized/`, `features/`, `labels/`
- gate-report filename: `<family>__<version>__phase-<id>__<unix_ms>__<short_commit>.json`
- successor-state root: `data/microstructure/successor-state/` (flat)
- successor-state filename: `<family>__<version>__<stage_marker>__phase-<id>.json`
- sidecar body: `<sha>  <basename>\n` (two spaces, trailing newline)

The Phase 4bb-D raw-gate report was written to a doubled path:
`data/microstructure/gate-reports/gate-reports/...`. The root cause is at
`src/prometheus/research/microstructure/eligibility_report.py:159`:

```python
gate_dir = output_root / GATE_REPORTS_SUBDIR
```

with `GATE_REPORTS_SUBDIR = "gate-reports"` defined at
`src/prometheus/research/microstructure/eligibility_io.py:45`. When Phase 4bb-D
passed `output_root = data/microstructure/gate-reports`, the writer
composed `data/microstructure/gate-reports / "gate-reports" / filename`.

The derived (Phase 4bf), feature (Phase 4bi-B), and label (Phase 4bj-E)
gate writers already place reports under their family subdir correctly —
each of them has its own `derive_report_paths` helper. Only the raw-gate
writer is anomalous.

## §4. What this phase changes

### 4.1 New source module

- **`src/prometheus/research/microstructure/canonical_paths.py`** — pure
  path-policy helpers:
  - `FAMILY_SUBDIRS` mapping (`raw`, `normalized`, `features`, `labels`);
  - `MICROSTRUCTURE_ROOT_PARTS`, `GATE_REPORTS_ROOT_PARTS`, `SUCCESSOR_STATE_ROOT_PARTS` tuples;
  - `CanonicalPathError`;
  - `derive_short_commit`;
  - `normalize_family`;
  - `compose_canonical_gate_report_id` (with `phase-<id>` tag);
  - `compose_canonical_successor_state_filename`;
  - `derive_canonical_gate_report_path`;
  - `derive_canonical_successor_state_path`;
  - `derive_sidecar_path`;
  - `compose_canonical_sidecar_body` (two spaces, trailing newline);
  - `write_paired_sha256_sidecar` (atomic, refuse-overwrite, parents-mkdir);
  - `assert_path_under_microstructure`;
  - `assert_path_under_gate_reports_subdir`;
  - `assert_path_under_successor_state`;
  - `compute_file_sha256`.
- The module performs no real `data/microstructure/` I/O at import time
  and only writes to the filesystem when `write_paired_sha256_sidecar` is
  called explicitly. Tests use `pytest tmp_path` only.

### 4.2 Backward-compatible kwargs on the raw-gate writer

- **`eligibility_report.write_report_atomic`** gains an optional
  keyword-only argument `family_subdir: str | None = None`:
  - default (`None`) — preserves the Phase 4bb-C placement exactly:
    `<output_root>/gate-reports/<report_id>.json`;
  - non-empty string (e.g. `"raw"`) — canonical placement:
    `<output_root>/<family_subdir>/<report_id>.json`, skipping the legacy
    `gate-reports` subdir injection;
  - empty string or string containing path separators raises `ValueError`.

### 4.3 Backward-compatible kwargs on the orchestrator

- **`eligibility_gate.AggTradesEligibilityGateInput`** gains two optional
  fields:
  - `family_subdir: str | None = None`
  - `phase_id: str | None = None`
- **`eligibility_gate.run_eligibility_gate`** threads `family_subdir`
  through to `write_report_atomic` and passes `phase_id` to the report-id
  constructor. When `phase_id is None`, the legacy report-id format
  `<family>__<version>__<unix_ms>__<short>` is preserved verbatim. When
  `phase_id` is provided, the canonical format
  `<family>__<version>__phase-<id>__<unix_ms>__<short>` is used.
- `__post_init__` validates the new kwargs (non-empty strings, no path
  separators, type checks) and raises `AggTradesGateInputError` on
  violation.

### 4.4 Package `__init__.py` re-exports

The package re-exports the canonical-path helper API with a stable
alias for clarity:

- `CanonicalPathError`
- `FAMILY_SUBDIRS`
- `GATE_REPORTS_ROOT_PARTS`
- `MICROSTRUCTURE_ROOT_PARTS`
- `SUCCESSOR_STATE_ROOT_PARTS`
- `assert_canonical_path_under_microstructure` (alias for `canonical_paths.assert_path_under_microstructure`)
- `assert_path_under_gate_reports_subdir`
- `assert_path_under_successor_state`
- `compose_canonical_gate_report_id`
- `compose_canonical_sidecar_body`
- `compose_canonical_successor_state_filename`
- `compute_canonical_file_sha256` (alias for `canonical_paths.compute_file_sha256`)
- `derive_canonical_gate_report_path`
- `derive_canonical_successor_state_path`
- `derive_short_commit`
- `derive_sidecar_path`
- `normalize_family`
- `write_paired_sha256_sidecar`

The package docstring was extended with a Phase 4bb-F-implementation
section explaining the canonical path policy helpers and the
backward-compatible threading of `family_subdir` / `phase_id`.

### 4.5 New tests

- **`tests/research/microstructure/test_canonical_paths.py`** — 47 tests
  covering: family-subdir mapping, root-parts tuples, family normalisation
  (accepts / rejects), `derive_short_commit` (defaults, explicit length,
  invalid hex, non-string), canonical gate-report id construction
  (format + parametrised invalid kwargs), canonical successor-state
  filename construction (format + parametrised invalid kwargs), canonical
  gate-report path placement (each family), canonical successor-state path
  placement, sidecar path derivation, sidecar body format,
  `write_paired_sha256_sidecar` writes-correct-format / refuses-overwrite
  / explicit-overwrite-allowed / creates-parent-dirs / rejects-non-Path,
  `assert_path_under_microstructure` accepts/rejects/non-Path,
  `assert_path_under_gate_reports_subdir` accepts/rejects-wrong-family/rejects-outside,
  `assert_path_under_successor_state` accepts/rejects,
  `compute_canonical_file_sha256` matches hashlib / rejects-non-Path.
- **`tests/research/microstructure/test_eligibility_report_canonical_subdir.py`**
  — 19 tests covering: writer default preserves legacy `gate-reports/`
  placement (backward compatibility); writer with `family_subdir="raw"`
  uses canonical `raw/` placement; writer with each family-subdir;
  writer rejects empty `family_subdir`; writer rejects path-separators in
  `family_subdir`; writer still validates `output_root` is under
  `data/microstructure/`; writer with `family_subdir` writes sidecar
  correctly; writer with `family_subdir` refuses to overwrite; GateInput
  defaults; GateInput accepts new kwargs; GateInput rejects bad
  `family_subdir`; GateInput rejects empty `phase_id`; orchestrator
  default preserves legacy doubled-path placement; orchestrator with
  canonical `family_subdir="raw"` + `phase_id="4bb-F"` produces canonical
  placement without doubled `gate-reports/gate-reports/`; orchestrator
  canonical report-id short-commit length 12; orchestrator canonical
  sidecar two-space + trailing-newline format; orchestrator preserves
  manifest immutability under canonical placement; orchestrator canonical
  payload `research_eligible_after=False` and
  `no_successor_authorization=True`.

## §5. Files changed

### 5.1 Tracked files added (3)

- `src/prometheus/research/microstructure/canonical_paths.py`
- `tests/research/microstructure/test_canonical_paths.py`
- `tests/research/microstructure/test_eligibility_report_canonical_subdir.py`

### 5.2 Tracked files modified (3)

- `src/prometheus/research/microstructure/eligibility_report.py` — added
  optional `family_subdir` kwarg to `write_report_atomic`. Preserves all
  existing call-site behaviour and refuse-overwrite discipline.
- `src/prometheus/research/microstructure/eligibility_gate.py` — added
  optional `family_subdir` and `phase_id` fields to
  `AggTradesEligibilityGateInput`; threaded them through
  `run_eligibility_gate` and `_make_report_id`. Preserves all existing
  default behaviour.
- `src/prometheus/research/microstructure/__init__.py` — re-exports the
  canonical-path helper public API and extends the package docstring
  with a Phase 4bb-F-implementation section.

### 5.3 Tracked docs added (2)

- `docs/00-meta/implementation-reports/2026-05-11_phase-4bb-f-implementation_gate-report-successor-state-writer-path-policy.md`
  (this memo)
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bb-f-implementation_closeout.md`

### 5.4 Tracked docs modified narrowly (1)

- `docs/00-meta/current-project-state.md` — new Phase 4bb-F-implementation
  narrative paragraph + new "Current phase:" block; prior Phase 4bb-F
  "Current phase:" block preserved as historical context.

### 5.5 Untouched

- No file under `data/microstructure/`.
- No existing manifest, gate report, successor-state, sidecar,
  acquisition log, raw zip, normalized parquet, feature parquet, label
  parquet, or any prior local gitignored artefact.
- No existing test outside the two new test files.
- No existing source module other than the three narrow edits above.
- No `pyproject.toml`, `README.md`, `.gitignore`, `.mcp.json`,
  `.claude/`, `docs/12-roadmap/phase-gates.md`,
  `docs/12-roadmap/technical-debt-register.md`,
  `docs/00-meta/ai-coding-handoff.md`,
  `docs/00-meta/implementation-ambiguity-log.md`,
  `docs/00-meta/process/`, retained-verdict ledger, project lock, or M0
  governance document.

## §6. Validation

- **`ruff check .` (whole repo):** PASS — `All checks passed!`.
- **`mypy src/prometheus` (strict, whole project):** PASS — `Success: no
  issues found in 120 source files`. (One more file than the prior 119 —
  the new `canonical_paths.py`.)
- **`pytest tests/research/microstructure/` (full microstructure suite):**
  `915 passed, 1 skipped` — the one skip is the pre-existing labelled
  `pytest.skip` placeholder in `test_label_gate_report.py`. No new
  regressions.
- **`pytest` (whole repo):** `1698 passed, 1 skipped, 2 failed`. The two
  failures are the unchanged pre-existing simulation `KeyError:
  'trade_count'` failures in `tests/simulation/test_backtest_real_2026_03.py`
  caused by an unrelated `src/prometheus/research/data/storage.py:232`
  schema mismatch. **Zero new test regressions from Phase
  4bb-F-implementation.**
- **`git diff --check`:** clean.
- **`git check-ignore`:** confirmed `data/microstructure/` is still
  gitignored.

## §7. Backward-compatibility evidence

- The existing test
  `tests/research/microstructure/test_eligibility_report.py::test_write_report_atomic_writes_under_gate_reports`
  passes unchanged. It asserts `written.parent.name == "gate-reports"`
  when `family_subdir` is not supplied. The default behaviour of
  `write_report_atomic` is preserved exactly.
- The existing test
  `tests/research/microstructure/test_eligibility_report.py::test_full_gate_report_has_all_required_fields`
  passes unchanged. It runs the full orchestrator end-to-end with the
  legacy invocation pattern.
- The existing 168 eligibility-gate tests (canonical-paths +
  canonical-subdir + io + report + gate + import-boundaries +
  no-network) all pass.
- All 915 microstructure tests pass (1 pre-existing labelled skip).
- The Phase 4bb-C / Phase 4bb-D recorded report path remains the
  canonical interpretation of the Phase 4bb-D historical artefact. No
  migration. No rewrite.

## §8. Preserved retained verdicts and project locks

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED —
NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS /
FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD
REJECT — terminal; G1 HARD REJECT — terminal; C1 HARD REJECT — terminal;
§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× /
one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown
+ cooled-down families list + memo template; Phase 4al refined no-rescue
rule + §13 boundary + §14 hierarchy; Phase 4am .. Phase 4bb-F results —
all preserved verbatim.

## §9. Phase 4aw invariant preservation

`MicrostructureManifest.flip_research_eligible(...)` always-raises invariant
preserved (never invoked by this phase). No manifest of any family is
mutated.

## §10. Boundary confirmations

Phase 4bb-F-implementation did NOT:

- modify any prior raw, normalized, feature, label, gate-report, or
  successor-state artefact;
- migrate the Phase 4bb-D doubled-path report to a canonical location;
- run the raw-gate, derived-gate, feature-gate, or label-gate;
- create a new gate report or new successor-state artefact;
- mutate any manifest;
- flip `research_eligible` on any family;
- transition `eligibility_gate_status` on any actual manifest;
- change `chronological_split_policy` on any actual manifest;
- compute features, labels, signals, ML, strategy, or backtest output;
- acquire data; call any endpoint; open any WebSocket; use any
  credential; read `.env`; create `.env`; create or read `.mcp.json`;
  enable MCP or Graphify;
- revise any retained verdict; change any project lock; amend M0
  governance;
- authorize Phase 4bb-G, Phase 4bj-H, Phase 5, Phase 4 canonical, paper /
  shadow, live-readiness, deployment, exchange-write, production-key
  creation, authenticated APIs, private endpoints, user stream, or live
  WebSocket implementation;
- merge into `main`.

## §11. No-rescue constraints preserved verbatim

The Phase 4al refined no-rescue rule remains binding. The Phase 4ak M0
twelve-clause gate, post-null cooldown rule, and cooled-down families
list remain binding. No cooled-down strategy candidate (R2 / F1 / D1-A /
V2 / G1 / C1) is reopened, rescued, or reinterpreted. No new strategy
candidate is created.

## §12. Successor authorization

**No successor phase is authorised by Phase 4bb-F-implementation.**

The natural follow-ups remain unauthorised:

- a future Phase 4bb-G that re-runs the raw-gate against the Phase 4az
  artefacts under canonical placement (would require a separately
  authorised brief);
- a future migration phase that moves the doubled-path Phase 4bb-D
  report to canonical placement (the Phase 4bb-F memo §6 explicitly
  recommends NOT migrating);
- a future Phase 4bj-H label-evaluation phase;
- any ML / strategy / backtest / paper / shadow / live phase.

## §13. Recommended state

**Remain paused.** The canonical path policy helpers are now available
for any future authorised raw-gate execution and for any future
canonical successor-state writer. The Phase 4bb-D doubled-path artefact
is preserved unchanged in line with the Phase 4bb-F §6 recommendation.

Phase 4bb-F-implementation is **branch-complete** only by this work; per
the Phase 4bk-A workflow standard it is **not** project-complete until a
separately authorized merge phase records its merge-closeout on `main`.
