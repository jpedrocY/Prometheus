# Phase 4bm-D Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate
- **Tier**: Tier 1 (docs-and-code Full Phase; multi-day analogue of Phase 4bf)
- **Type**: 60-check offline eligibility-gate implementation + one read-only authoritative gate run against the Phase 4bm-B v002 derived family
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-D as project-complete on `main` after a clean DERIVED_GATE_PASS (60 / 60 PASS) authoritative real-artefact gate run from the committed implementation SHA, preserving every retained verdict, every project lock, every on-disk manifest, and every prior governance artefact byte-for-byte
- **Branch merged**: `phase-4bm-d/multi-day-derived-family-eligibility-gate`
- **Target branch**: `main`
- **Base**: `main` at `d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3` (Phase 4bm-C merge-closeout commit)
- **Predecessor**: Phase 4bm-C (Multi-Day Normalized Structural QA Memo, project-complete on `main`)

## §2 SHAs

- **Pre-merge `main` SHA**: `d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3`
- **Pre-merge `origin/main` SHA**: `d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3` (in sync)
- **Phase 4bm-D implementation commit SHA**: `57e1c97e6e938797d448b331cdc27b50b8e935dd` (`feat(phase-4bm-d): implement multi-day derived eligibility gate`; 11 files / +6,786 / −0)
- **Phase 4bm-D docs/closeout commit SHA**: `71ec4834e7867f90b09c4fefe2441040f58545e4` (`docs(phase-4bm-d): add gate report and closeout`; 3 files / +902 / −2)
- **Phase 4bm-D branch tip SHA pre-merge**: `71ec4834e7867f90b09c4fefe2441040f58545e4`
- **Merge commit SHA**: `a80b8a050c66397c8a4a51a9a6e87b7f8c785dbc`
- **Merge commit message**: `docs(phase-4bm-d): merge multi-day derived family eligibility gate`
- **Post-merge `main` SHA after merge-closeout commit + push**: recorded in §18 of the operator report (final `git rev-parse main` / `git rev-parse origin/main` values)

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-d/multi-day-derived-family-eligibility-gate -m "docs(phase-4bm-d): merge multi-day derived family eligibility gate"`
- **Strategy**: `ort` (git default; reported by git as `Merge made by the 'ort' strategy.`)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing (recorded in §18 of the operator report).

## §4 Files Brought Forward by the Merge

Fourteen tracked files brought forward from the Phase 4bm-D branch into `main`, split across the two source commits.

**Implementation commit (`57e1c97`) — 11 tracked files:**

Source (5; 1 modified + 4 added):

1. `src/prometheus/research/microstructure/__init__.py` (MODIFIED, +195 / −0; narrow re-exports for the new public surface of the four new gate modules)
2. `src/prometheus/research/microstructure/multiday_derived_gate.py` (NEW, +617; orchestrator + frozen input/result types + boundary-confirmation builder + per-file measurement walker)
3. `src/prometheus/research/microstructure/multiday_derived_gate_io.py` (NEW, +481; streaming 1 MiB SHA hashing / atomic JSON write-then-rename / canonical Phase 4bb-F sidecar write / path-discipline helpers / per-file path resolver)
4. `src/prometheus/research/microstructure/multiday_derived_gate_checks.py` (NEW, +1,391; the 60-check suite + `CHECK_ORDER` tuple + locked constants `EXPECTED_*_SHA` / `EXPECTED_GATE_REPORT_ID` / `EXPECTED_TOTAL_EVENT_COUNT=155,153,449` / `EXPECTED_DATE_COUNT=90` / `CANONICAL_DATE_START="2024-12-01"` / `CANONICAL_DATE_END="2025-02-28"` / Phase 4bm-C documentation-dependency paths / `_PASS_28_RE` 28-question regex / required 34 top-level + 16 governance-label key tuples / forbidden-column-token list / `SAMPLE_DATES` 5-date tuple / normalized schema constant)
5. `src/prometheus/research/microstructure/multiday_derived_gate_report.py` (NEW, +182; frozen report data model + builder + writer enforcing the two hard safety invariants and the three-state verdict whitelist)

Tests (6; all added):

6. `tests/research/microstructure/_multiday_derived_gate_fixtures.py` (NEW, +379; canonical PASS-shape fixture builders)
7. `tests/research/microstructure/test_multiday_derived_gate.py` (NEW, +665; 12 orchestrator end-to-end tests using parser-format `per_file_inventory` keys throughout)
8. `tests/research/microstructure/test_multiday_derived_gate_checks.py` (NEW, +1,737; per-check PASS / FAIL unit tests covering all 60 checks)
9. `tests/research/microstructure/test_multiday_derived_gate_io.py` (NEW, +545; I/O primitive tests)
10. `tests/research/microstructure/test_multiday_derived_gate_report.py` (NEW, +460; report data-model + writer-refuse-invariant tests)
11. `tests/research/microstructure/test_multiday_derived_gate_no_network.py` (NEW, +134; static no-network / no-credential / `.env` / `dotenv` scan over the four gate modules)

**Docs/closeout commit (`71ec483`) — 3 tracked files:**

12. `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-d_multi-day-derived-family-eligibility-gate.md` (NEW, +257; 16-section implementation report)
13. `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-d_closeout.md` (NEW, +166; 13-section closeout)
14. `docs/00-meta/current-project-state.md` (MODIFIED, +479 / −2; Phase 4bm-D narrative paragraph + new "Current phase:" block; prior Phase 4bm-C "Current phase:" block preserved as labelled historical context)

**This merge-closeout commit — 1 additional tracked file (allowed by the operator authorization for the merge phase):**

15. `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-d_merge-closeout.md` (NEW; this file)

**Explicit non-changes:** No `data/microstructure/` file was modified, added, or deleted. No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition. No prior `src/prometheus/` module was modified beyond the narrow `__init__.py` re-export update. No prior test was modified except for the in-scope ruff cleanups inside two Phase-4bm-D-owned test files (`test_multiday_derived_gate_checks.py` and `test_multiday_derived_gate_report.py`; both were created in this phase). No `scripts/`, `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file was modified.

## §5 Diff Summary

```text
 docs/00-meta/current-project-state.md              |  481 +++++-
 .../2026-05-15_phase-4bm-d_closeout.md             |  166 ++
 ...-d_multi-day-derived-family-eligibility-gate.md |  257 +++
 src/prometheus/research/microstructure/__init__.py |  195 +++
 .../microstructure/multiday_derived_gate.py        |  617 +++++++
 .../microstructure/multiday_derived_gate_checks.py | 1391 ++++++++++++++++
 .../microstructure/multiday_derived_gate_io.py     |  481 ++++++
 .../microstructure/multiday_derived_gate_report.py |  182 ++
 .../_multiday_derived_gate_fixtures.py             |  379 +++++
 .../microstructure/test_multiday_derived_gate.py   |  665 ++++++++
 .../test_multiday_derived_gate_checks.py           | 1737 ++++++++++++++++++++
 .../test_multiday_derived_gate_io.py               |  545 ++++++
 .../test_multiday_derived_gate_no_network.py       |  134 ++
 .../test_multiday_derived_gate_report.py           |  460 ++++++
 14 files changed, 7688 insertions(+), 2 deletions(-)
```

- 14 files changed
- 7,688 insertions
- 2 deletions (both from `current-project-state.md` — the prior Phase 4bm-C "Earlier 'Current phase:' content (Phase 4bm-B) is preserved by..." reference being demoted; the prior 4bm-C content is preserved verbatim in a new labelled historical block)
- The merge diff exactly matches the expected change set from the authorization prompt (11 implementation-commit files + 3 docs-commit files = 14 tracked files).
- `git diff --check` clean (no whitespace errors; no unresolved merge markers).

## §6 Result / Verdict

**GATE PASS — DERIVED_GATE_PASS recorded as authoritative Phase 4bm-D evidence; Phase 4bm-D is project-complete on `main`.**

Phase 4bm-D implemented the offline 60-check multi-day derived-family eligibility gate for the Phase 4bm-B v002 derived family (`dataset_family = microstructure_normalized_aggtrades_v001`; `dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events; ~1.40 GiB) as the multi-day analogue of the Phase 4bf 55-check single-day gate, and ran it exactly once read-only against the real v002 artefacts from the committed implementation SHA. The authoritative run returned `overall_status = pass`, `gate_verdict = DERIVED_GATE_PASS`, **60 / 60 checks PASS** (0 FAIL / 0 ERROR / 0 NOT_APPLICABLE), all 19 boundary confirmations `True`, and both hard safety invariants preserved (`research_eligible_after = False`; `no_successor_authorization = True`). The `eligibility_gate_status_after = "pass"` field on the new gate report is a **report-level recommendation only** and is **not written back to any manifest**; the v002 derived manifest, the v002 raw manifest, and the Phase 4bd v001 derived manifest all remain `research_eligible = false` / `eligibility_gate_status = "pending"` byte-for-byte. Phase 4bm-D is now project-complete on `main`. **Phase 4bm-D does not authorize Phase 4bm-E, Phase 4bm-F, any other successor, or any change to any on-disk manifest.**

## §7 Local Gitignored Outputs

Phase 4bm-D produced two gate-report file pairs under `data/microstructure/gate-reports/normalized/` (the canonical Phase 4bb-F namespace), both gitignored under `.gitignore:85` and **not committed**.

**Authoritative (the Phase 4bm-D evidence):**

| Path | Size | SHA256 |
| ---- | ---- | ------ |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` | (gitignored) | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json.sha256` | (gitignored) | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |

Sidecar body: canonical Phase 4bb-F format `<sha256_lowercase_hex>  <basename>\n` (two ASCII spaces; trailing LF). The sidecar's leading 64 hex characters parse to the recomputed JSON SHA bit-for-bit. The `code_commit_sha` field recorded inside this report is the Phase 4bm-D implementation commit SHA `57e1c97e6e938797d448b331cdc27b50b8e935dd`.

**Preliminary pre-commit sanity (NON-AUTHORITATIVE; retained as continuity witness; explicitly marked as non-authoritative in both the implementation report and the closeout):**

| Path | SHA256 |
| ---- | ------ |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779055831936__d39ffd8aa1fe.json` | `ffde54bb7dd96f9df3269915271238b3e3f463fee6af6ce845e95d8713651764` |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779055831936__d39ffd8aa1fe.json.sha256` | `11c952519e16a967f1a916273bff3d64381fe8fa2e2851379b47f4f5a930e99d` |

The preliminary report recorded `code_commit_sha = d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3` (the predecessor `main` HEAD), executed before the Phase 4bm-D implementation was committed; it is **not the Phase 4bm-D evidence** and is retained only as a non-authoritative continuity witness.

Gitignore confirmation for both file pairs:

```text
.gitignore:85:data/microstructure/	data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json
.gitignore:85:data/microstructure/	data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json.sha256
```

The pre-existing Phase 4bf v001 single-day gate report under the same namespace (`microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json`) is unchanged. The Phase 4bm-B v002 derived manifest, its sidecar, and all 90 per-day Parquets + 90 sidecars are unchanged.

## §8 Validation Results

### Pre-merge (on Phase 4bm-D branch tip `71ec483`)

- `git status --short`: clean (only pre-existing untracked `.claude/scheduled_tasks.lock` and `data/research/`)
- `git diff --check`: clean
- `git diff --name-status main...phase-4bm-d/...`: 14 files (1 M `__init__.py` + 11 A code/tests + 1 M `current-project-state.md` + 2 A docs)
- `git diff --stat main...phase-4bm-d/...`: 14 files / +7,688 insertions / 2 deletions (matches expected)
- `git check-ignore -v` on authoritative gate report and sidecar: both `.gitignore:85: data/microstructure/`
- Authoritative gate report SHA256 recomputed = `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` (matches recorded value)
- Authoritative sidecar SHA256 recomputed = `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` (matches recorded value)
- main == origin/main = `d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3` (in sync; `git pull --ff-only` reported `Already up to date.`)
- phase-4bm-d branch == origin/phase-4bm-d branch = `71ec4834e7867f90b09c4fefe2441040f58545e4` (in sync)

### Merge command output

- `Merge made by the 'ort' strategy.`
- 14 files changed, 7,688 insertions(+), 2 deletions(-)
- Conflicts: none
- Merge commit SHA: `a80b8a050c66397c8a4a51a9a6e87b7f8c785dbc`

### Post-merge (on `main` after the merge commit)

- `git diff --check` (post-merge): clean — exit code 0
- `uv run ruff check <10 Phase 4bm-D source/test files>`: **PASS** — `All checks passed!`
- `uv run mypy src/prometheus` (strict): **PASS** — `Success: no issues found in 124 source files`
- `uv run pytest <5 Phase 4bm-D test files>` (`test_multiday_derived_gate_io.py` + `_checks.py` + `_report.py` + `.py` + `_no_network.py`): **218 passed in 2.68 s**
- `git rev-parse HEAD`: `a80b8a050c66397c8a4a51a9a6e87b7f8c785dbc` (merge commit)
- `git status --short` (post-merge, pre-closeout-commit): only the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`)

### Whole-repo gates

Whole-repo `pytest` was **not** rerun by this merge. The most recent authoritative whole-repo baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; the two pre-existing `KeyError: 'trade_count'` simulation failures on `tests/simulation/test_backtest_real_2026_03.py` in `src/prometheus/research/data/storage.py:232` are unrelated to Phase 4bm-D and are preserved as the baseline). Phase 4bm-D introduces zero new regressions vs that baseline (the scoped Phase 4bm-D pytest set is 218 / 218 PASS).

### Gitignore policy verification

- `git check-ignore -v data/microstructure/`: `.gitignore:85: data/microstructure/`
- Authoritative gate report path + sidecar both covered by `.gitignore:85` (recorded above)
- Preliminary gate report path + sidecar both covered by `.gitignore:85`

## §9 Upstream Immutability Evidence

The Phase 4bm-D orchestrator captures pre-check SHA256 for every governance artefact, every per-file Parquet, every per-file sidecar, and every raw zip, and re-captures post-check SHA256 after the 60-check suite completes. On the authoritative run, **all four mutation-class boundary confirmations returned `True`**, evidencing byte-identical immutability:

- `no_manifest_mutation = True` — derived manifest, raw manifest, acquisition log, Phase 4bl-D-R gate report, Phase 4bl-E successor-state record all byte-identical pre/post
- `no_per_file_parquet_mutation = True` — all 90 v002 per-day Parquets byte-identical pre/post
- `no_per_file_sidecar_mutation = True` — all 90 v002 per-day sidecars byte-identical pre/post
- `no_raw_zip_mutation = True` — all 90 v002 raw zips byte-identical pre/post

Specific governance witnesses preserved:

| Artefact | SHA256 |
| -------- | ------ |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bl-D-R PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E successor-state | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| v002 derived multi-day index manifest (Phase 4bm-B output) | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |

The 90 v002 raw zips and 90 v002 raw zip sidecars (Phase 4bl-C outputs) are unchanged. The 90 v002 per-day Parquets and 90 paired sidecars (Phase 4bm-B outputs) are unchanged. The Phase 4bd v001 single-day Parquet (`2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`) is unchanged. The Phase 4bd v001 derived manifest is unchanged. The pre-existing Phase 4bf v001 derived gate report at `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` is unchanged.

This merge introduces no new mutations; the immutability evidence carries forward unchanged.

## §10 Manifest State Preservation

- **v002 derived multi-day index manifest** (`microstructure_normalized_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged from Phase 4bm-B output. Not modified by Phase 4bm-D. Not modified by this merge.
- **v002 raw manifest** (`microstructure_raw_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged from Phase 4bl-C. Not modified.
- **Phase 4bd v001 derived manifest** (`microstructure_normalized_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged from Phase 4bd. Not modified.

The Phase 4bm-D gate's `eligibility_gate_status_after = "pass"` field is a **report-level recommendation only** and is **not written back to any manifest**. No `research_eligible` flip occurred. No `eligibility_gate_status` transition occurred on any actual on-disk manifest. No `chronological_split_policy` change occurred on any actual manifest. The v002 multi-day index manifest is a sibling shape that does **not** use the single-file `MicrostructureManifest` data class; no path exists in this phase to flip any flag on any manifest.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## §11 Boundary Confirmations

All 19 boundary confirmation keys on the authoritative Phase 4bm-D gate result returned `True` (verbatim from the gate report's `boundary_confirmations` block):

- `no_manifest_mutation`
- `no_per_file_parquet_mutation`
- `no_per_file_sidecar_mutation`
- `no_raw_zip_mutation`
- `no_normalization_written_outside_namespace`
- `no_data_microstructure_write_outside_gate_reports`
- `no_feature_computed`
- `no_label_computed`
- `no_signal_computed`
- `no_ml_trained`
- `no_strategy_created`
- `no_backtest_run`
- `no_network_io`
- `no_websocket`
- `no_credential_read`
- `no_env_read`
- `no_mcp_or_graphify`
- `research_eligible_after_is_false_for_derived_family`
- `no_successor_authorization`

Additional merge-level confirmations:

- no `data/microstructure/` file committed by either source branch commit or this merge-closeout commit
- no prior source / test / script modified beyond the narrow `__init__.py` re-export and the in-scope ruff cleanups in two Phase-4bm-D-owned test files
- no `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file modified
- no prior governance memo modified beyond the narrow `current-project-state.md` paragraph addition
- no prior phase implementation report, closeout, or merge-closeout modified
- no gate rerun (the authoritative gate report is the one from the post-commit run captured at branch tip; this merge does not rerun the gate)
- no acquisition; no Binance / public / private endpoint contacted; no WebSocket opened; no credential used; no `.env` / `.mcp.json` read or created; MCP / Graphify not enabled
- no features / labels / signals / proxies / ML / strategy / backtest output computed
- no successor-state JSON created
- no retained verdict revised; no project lock loosened; no M0 amendment; no Phase 4al rule amended; no Phase 4aw invariant amended; no Phase 4bb-F canonical path policy amended; no Phase 4bl-F rule amended
- no successor authorized (Phase 4bm-E / 4bm-F / 4bm-* / 4bn-* / 4bo-* / 4bp-* / 4bq-* / Phase 5 / Phase 4 canonical all remain unauthorized)
- merge command was a clean `git merge --no-ff` with `ort` strategy, no conflicts, no `--no-verify`, no `--no-gpg-sign`, no force-push

## §12 Retained Verdict Ledger

All preserved verbatim:

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

All preserved verbatim by Phase 4bm-D and by this merge.

## §13 Preserved Project Locks

All preserved verbatim:

- §11.6 = 8 bps per side
- Round-trip = 16 bps
- §1.7.3 = 0.25% risk / 2× leverage / one-position / mark-price stops
- Phase 3p §4.7 (strict integrity gate)
- Phase 3r §8 (mark-price gap governance)
- Phase 3v §8 (stop-trigger-domain governance)
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance)
- Phase 4j §11 (metrics OI-subset partial-eligibility rule)
- Phase 4k (V2 backtest-plan methodology)
- Phase 4p (G1 strategy spec)
- Phase 4q (G1 backtest-plan methodology)
- Phase 4v (C1 strategy spec)
- Phase 4w (C1 backtest-plan methodology)
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; never invoked)
- Phase 4bb-F canonical path policy
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked — the Phase 4bm-D writer emits canonical LF natively)
- Phase 4am .. Phase 4bm-C results — all preserved verbatim

## §14 No-Rescue Constraints

The Phase 4bm-D merge records a passing report-level eligibility-gate result on the v002 derived family produced by Phase 4bm-B. The verdict is report-level only. It does NOT, and CANNOT, be construed as authorising:

- ML model training, model selection, strategy hypothesis generation, signal construction, or any conversion of report-level gate evidence into trading signals
- strategy logic, position state, entry / exit rules, or backtest design
- paper / shadow / live-readiness / deployment / exchange-write work
- Phase 4 canonical or Phase 5 authorisation
- transitioning the v002 derived manifest's `research_eligible` flag from `false` to `true` from this evidence alone
- transitioning the v002 derived manifest's `eligibility_gate_status` from `"pending"` to anything else on disk
- transitioning any other manifest's `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy`
- creating a Phase 4bm-D successor-state JSON (that would require a separately authorized Phase 4bm-F)
- creating a Phase 4bm-E research-eligibility decision memo (that requires a separately authorized Phase 4bm-E)
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- old-strategy alt-symbol rerun or cooled-down-family reopening
- 5m research-thread reopening (Phase 3t closure preserved)
- revising or weakening any retained verdict (R2 / F1 / D1-A / V2 / G1 / C1 first-specs remain terminally rejected as recorded; H0 framework anchor, R3 baseline-of-record, and R1a / R1b-narrow retained-non-leading status all preserved)
- cross-strategy hybrids (V1-D1, F1-D1, V2-G1, G1-C1, or any other combination)
- -prime, -narrow, -extension, or -hybrid variants of any historical candidate
- §11.6 cost-realism relaxation, §1.7.3 risk / leverage / one-position / mark-price stop amendment, or any other lock loosening
- M0 amendment, post-null cooldown weakening, cooled-down families list shortening, or memo template alteration
- use of Phase 4l V2 forensic numbers, Phase 4r G1 forensic numbers, or Phase 4x C1 forensic numbers as parameter-selection inputs
- use of 5m Q1–Q7 diagnostic outputs as rule-input candidates
- MCP / Graphify / `.mcp.json` / credential enablement
- public-endpoint code calls, user-stream implementation, live WebSocket implementation, or any authenticated-API / private-endpoint access

The v002 derived family carrying DERIVED_GATE_PASS at report level is necessary but not sufficient evidence for any of the above; sufficient evidence requires separately authorized subsequent phases under the established phase ladder (Phase 4bm-E → Phase 4bm-F → later research / feasibility / strategy / backtest phases under M0 admissibility and Phase 4al §14 hierarchy).

## §15 Successor Authorization

**None.**

This merge-closeout records that Phase 4bm-D is project-complete on `main`. It does **not** authorize:

- Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo
- Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any other Phase 4 successor
- Phase 5 / Phase 4 canonical
- Paper / shadow / live-readiness / deployment / exchange-write
- Production-key creation / authenticated APIs / private endpoints
- User-stream / live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credential work
- Any additional aggTrades / 5m / 1m / tick / mark-price / order-book / cross-venue data acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- ML implementation, model selection, feature ranking, meta-labeling
- Strategy implementation, signal construction, backtest implementation
- Any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual on-disk manifest
- Any successor-state JSON creation

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, and the merge-closeout standard.

## §16 Recommended State

**Remain paused.**

Phase 4bm-D is now project-complete on `main` (this merge-closeout records the lifecycle anchor). The v002 derived family has report-level eligibility-gate confirmation (DERIVED_GATE_PASS; 60 / 60 checks PASS) but no successor is authorized. The operator's broader pause decision continues to apply.

**Conditional next, NOT authorized:**

Future operator-authorized **Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo** would be the natural next step in the v002 lifecycle ladder by precedent of Phase 4bg-A (research-eligibility decision for the Phase 4bd v001 derived family). Phase 4bm-E would evaluate whether the v002 derived family is admissible in principle for a future Stage-3 research-eligibility transition given the completed Stage-0 (Phase 4bm-B), report-level Stage-1 / Stage-2 (Phase 4bm-C structural QA PASS + Phase 4bm-D DERIVED_GATE_PASS) evidence, and emit a docs-only decision memo. Phase 4bm-E is **not** authorised by this merge-closeout.

After any Phase 4bm-E merge, the recommended state would remain **remain paused** pending operator decision on the further conditional **Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording** ladder step (by precedent of Phase 4bg-B for the v001 derived family). Phase 4bm-F is **not** authorised by this merge-closeout.

— end of Phase 4bm-D merge-closeout —