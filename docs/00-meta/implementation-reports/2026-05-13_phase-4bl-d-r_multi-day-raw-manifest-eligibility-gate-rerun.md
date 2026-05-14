# Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate Rerun

## 1. Phase identity

- **Phase:** Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate
  Rerun
- **Type:** docs + tiny standalone wrapper script + offline tests + one
  local gitignored gate-rerun report (with paired SHA256 sidecar)
- **Branch:** `phase-4bl-d-r/multi-day-raw-manifest-eligibility-gate-rerun`
- **Base commit (`main` / `origin/main` at branch creation):**
  `69e45280f080e320171f1d851933fdb13213aaea`
  (Phase 4bl-D-S2 merge-closeout commit
  `docs(phase-4bl-d-s2): add merge closeout`; `main` and
  `origin/main` in sync at branch creation; Phase 4bl-D-S2 is
  project-complete).
- **Wrapper script path:**
  `scripts/phase4bl_d_r_rerun_raw_gate.py` (Python standard library +
  the Phase 4bl-D gate module loaded by file path; no network imports;
  no credential reads; no `.env`; no `.mcp.json`; no MCP / Graphify; no
  exchange adapters; no `prometheus.runtime` / `prometheus.execution`
  / `prometheus.persistence` imports).
- **Offline tests path:**
  `tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py`
  (23 offline tests; uses pytest `tmp_path` only; verifies identity
  constants, augmentation purity, deterministic serialisation, lineage
  fields, and static forbidden-import / forbidden-token scans).
- **Local gitignored gate-rerun report path:**
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`
- **Local gitignored gate-rerun sidecar path:**
  same path with `.sha256` suffix.

Phase 4bl-D-R is the operator-authorised rerun of the Phase 4bl-D
multi-day raw eligibility gate against the unchanged Phase 4bl-C v002
90-day BTCUSDT aggTrades dataset with the Phase 4bl-D-S2-canonicalised
2025-01-15 sidecar in place. Phase 4bl-D-R re-runs the full 33-check
Phase 4bl-D protocol verbatim (no protocol weakening) and emits a
distinct Phase 4bl-D-R-shaped gate report under the canonical
Phase 4bb-F path. Phase 4bl-D-R does **not** modify the Phase 4bl-D
gate script, does **not** modify any upstream artefact (raw zip,
sidecar, v002 manifest, v002 acquisition log, Phase 4bl-D gate
report, Phase 4bl-D-S2 canonicalisation report), does **not** flip
`research_eligible` on any manifest, does **not** transition
`eligibility_gate_status` on any actual manifest, does **not** create
a successor-state artefact, and does **not** authorise Phase 4bl-E,
Phase 4bm-*, Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*,
Phase 5, paper / shadow, live-readiness, deployment, exchange-write,
production-key creation, authenticated APIs, private endpoints, user
stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`,
credentials, or any successor phase.

## 2. Pre-state

### Predecessor lineage

- **Predecessor phase:** Phase 4bl-D — Multi-Day Raw Manifest
  Eligibility Gate (project-complete on `main` at the
  Phase 4bl-D merge-closeout commit
  `01ca1d07c601655e3c66b6349038ea4385d4e281`).
- **Predecessor gate report path:**
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
- **Predecessor gate report SHA256:**
  `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`
- **Predecessor gate verdict:** `RAW_MULTIDAY_GATE_FAIL`
- **Predecessor checks:** 29 PASS / 4 FAIL / 0 ERROR / 0 NA / 33 total
- **Predecessor failing check IDs:** `raw_zip_sidecar_integrity`,
  `per_file_row_count_consistency`,
  `per_file_time_bounds_consistency`,
  `total_row_count_consistency`.
- **Root cause:** the pre-existing Phase 4az 2025-01-15 sidecar at
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
  used Windows CRLF (`\r\n`) line terminator (100 bytes) instead of
  canonical Phase 4bb-F LF (`\n`) terminator. All other Phase 4bl-C
  newly-acquired sidecars were already in canonical LF form. The
  2025-01-15 raw zip itself was byte-identical to the Phase 4az
  fixture (SHA `f560c2e529e9...e2852b3e`).

### Remediation lineage

- **Remediation phase:** Phase 4bl-D-S2 — Controlled Sidecar
  Canonicalisation Execution (project-complete on `main` at the
  Phase 4bl-D-S2 merge-closeout commit
  `69e45280f080e320171f1d851933fdb13213aaea`).
- **Remediation type:** `metadata_sidecar_line_ending_canonicalization`.
- **Remediation report path:**
  `data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`
- **Remediation report SHA256:**
  `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3`
- **Target sidecar path:**
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
- **Target sidecar pre-state SHA256 (Phase 4bl-D-S2 pre-state):**
  `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`
  (100 bytes; CRLF)
- **Target sidecar post-state SHA256 (Phase 4bl-D-S2 post-state):**
  `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc`
  (99 bytes; LF; embedded SHA value and basename preserved verbatim)
- **Target raw zip path:**
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`
- **Target raw zip SHA256:**
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  (unchanged; 21,271,119 bytes; matches Phase 4az fixture exactly)

### Pre-rerun SHA snapshot (measured at branch creation)

| Artefact | Path | Size (bytes) | SHA256 |
| --- | --- | ---: | --- |
| target sidecar (canonicalised) | `data/microstructure/raw/.../BTCUSDT-aggTrades-2025-01-15.zip.sha256` | 99 | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` |
| target raw zip | `data/microstructure/raw/.../BTCUSDT-aggTrades-2025-01-15.zip` | 21,271,119 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| v002 raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | 105,052 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` | 302,055 | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bl-D gate report | `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json` | 169,637 | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` |
| Phase 4bl-D-S2 canonicalisation report | `data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json` | 5,241 | `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3` |

The on-disk v002 raw manifest carried `research_eligible: false` and
`eligibility_gate_status: "pending"` at branch creation. Phase 4bl-D-R
does not touch those fields.

## 3. Scope and discipline

Phase 4bl-D-R is bounded by:

- **Script reuse over script change.** The wrapper imports the
  Phase 4bl-D gate module unchanged via
  `importlib.util.spec_from_file_location`. The wrapper monkey-patches
  exactly three module-level identity constants
  (`PHASE_ID`, `PHASE_NAME`, `ARTEFACT_TYPE`) and two entries of the
  `GOVERNANCE_LABELS` dict in place (`phase`, `source_phase_boundary`).
  No other gate logic is modified. The 33-check protocol runs
  verbatim.
- **One execution only.** The gate's `run_gate(...)` is called
  exactly once. The wrapper's atomic-write helper refuses to
  overwrite an existing report.
- **No protocol weakening.** Every Phase 4bl-D check (33 / 33) runs
  verbatim. The strict-fail-closed posture is preserved verbatim. The
  sidecar parser is not relaxed. CRLF-vs-LF discipline is not
  amended. Full per-row Phase 4ax `validate_aggtrade_payload` is run
  across every row.
- **No upstream artefact mutation.** Raw zip, target sidecar, v002
  manifest, v002 acquisition log, Phase 4bl-D gate report, and
  Phase 4bl-D-S2 canonicalisation report are read-only.
- **No manifest mutation.** The actual v002 raw manifest's
  `research_eligible` and `eligibility_gate_status` fields remain
  `false` and `"pending"`. The Phase 4aw
  `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant is preserved (never invoked).
- **No successor authorisation.** The rerun PASS is descriptive
  evidence; it does **not** itself authorise Phase 4bl-E, raw
  successor-state recording, normalisation, features, labels,
  diagnostics, ML, strategy, paper / shadow, live-readiness,
  deployment, exchange-write, production-key creation, authenticated
  APIs, private endpoints, user stream, live WebSocket
  implementation, MCP, Graphify, `.mcp.json`, credentials, or any
  successor phase.

## 4. Wrapper design

`scripts/phase4bl_d_r_rerun_raw_gate.py` is a thin wrapper. Its
responsibilities, in order:

1. **Load the Phase 4bl-D gate module by file path.** Because
   `scripts/` is not a Python package, the wrapper uses
   `importlib.util.spec_from_file_location` with `sys.modules`
   registration (so `@dataclass` and similar decorators in the gate
   module resolve `cls.__module__` correctly).
2. **Monkey-patch identity constants:**
   - `gate.PHASE_ID = "4bl-d-r"` — lowercase, so the canonical
     Phase 4bb-F filename segment becomes `phase-4bl-d-r`.
   - `gate.PHASE_NAME = "Phase 4bl-D-R"`.
   - `gate.ARTEFACT_TYPE = "raw_multiday_manifest_eligibility_gate_rerun_report"`.
   - `gate.GOVERNANCE_LABELS["phase"] = "4bl-d-r"`.
   - `gate.GOVERNANCE_LABELS["source_phase_boundary"] = "4bl-D-S2"`
     (the remediation phase that produced the canonicalised sidecar;
     Phase 4bl-D itself had used `"4bl-C"` because Phase 4bl-C
     produced the acquisition).
3. **Run the gate once** by calling `gate.run_gate(output_root=...)`.
   The gate writes its report and paired SHA256 sidecar atomically to
   the canonical Phase 4bb-F path. The atomic-write helper inside
   the gate refuses to overwrite existing files; a refuse-overwrite
   error here would indicate an unexpected race or a stale prior
   rerun.
4. **Augment the report in memory.** The wrapper reads back the
   gate-produced JSON via the canonical Phase 4bb-F filename pattern
   (filtered to the `phase-4bl-d-r` segment), then calls the
   pure-function `augment_report(...)` to attach the Phase 4bl-D-R-
   specific lineage fields:
   - `phase_id` is normalised from lowercase `"4bl-d-r"` (the
     filename-segment convention) to the brief-specified mixed-case
     `"4bl-D-R"` in the report body. The canonical filename retains
     the lowercase segment to honour the Phase 4bb-F lowercase
     filename convention preserved from Phase 4bl-D / 4bf / 4bi-B /
     4bj-E.
   - `predecessor_gate_phase = "4bl-D"`,
     `predecessor_gate_id = "4bl-d"`,
     `predecessor_gate_report_path = ".../phase-4bl-d__1778627360966__2576a004c18a.json"`,
     `predecessor_gate_report_sha256 = "d97948ed4d...6629e7"`,
     `predecessor_gate_verdict = "RAW_MULTIDAY_GATE_FAIL"`,
     `predecessor_gate_overall_status = "fail"`,
     `predecessor_gate_failure_summary = <one-paragraph plain-English
     description of the CRLF root cause and the Phase 4bl-D-S2
     remediation>`,
     `predecessor_gate_failed_check_ids = [<the four failing check
     IDs>]`.
   - `remediation_phase = "4bl-D-S2"`,
     `remediation_type = "metadata_sidecar_line_ending_canonicalization"`,
     `remediation_report_path = ".../phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json"`,
     `remediation_report_sha256 = "8c6457b6...20809d3"`,
     `canonicalized_sidecar_path = ".../BTCUSDT-aggTrades-2025-01-15.zip.sha256"`,
     `canonicalized_sidecar_pre_sha256 = "b80c2768...605b42d"`,
     `canonicalized_sidecar_post_sha256 = "c40e6be6...0226018fc"`,
     `target_raw_zip_path = ".../BTCUSDT-aggTrades-2025-01-15.zip"`,
     `target_raw_zip_sha256 = "f560c2e5...e2852b3e"`.
   - Wrapper-identity metadata:
     `wrapper_phase = "Phase 4bl-D-R"`,
     `wrapper_phase_id_lowercase = "4bl-d-r"`,
     `wrapper_artefact_type = "raw_multiday_manifest_eligibility_gate_rerun_report"`.
   All other gate-produced fields are preserved verbatim:
   `checks` (33-element list), `per_file_validation_summary`
   (90-element list), `aggregate_summary`,
   `recomputed_totals`, `governance_labels`, `non_authorizations`,
   `retained_verdict_ledger`, `preserved_locks`,
   `source_artefacts`, `manifest_mutated`,
   `manifest_transition_performed`, `research_eligible_after`,
   `eligibility_gate_status_after`, `no_successor_authorization`,
   `strict_fail_closed`, etc.
5. **Atomic rewrite.** The wrapper deletes the gate's own report +
   sidecar (its own outputs from the same run), then atomically
   rewrites both with deterministic JSON
   (`json.dumps(sort_keys=True, indent=2, ensure_ascii=False) + "\n"`,
   UTF-8 encoding). The rewrite is guarded by a defence-in-depth
   filename check: the wrapper refuses to rewrite any report whose
   filename does not contain `phase-4bl-d-r`. The paired SHA256
   sidecar is written in canonical Phase 4bb-F format
   `<sha256_hex>  <basename>\n` (two spaces, trailing newline).

## 5. Wrapper tests

`tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py`
contains **23 offline tests**:

1. **Locked identity constants** (10 tests): verify
   `_GATE_PHASE_ID = "4bl-d-r"`, `_GATE_PHASE_NAME = "Phase 4bl-D-R"`,
   `_GATE_ARTEFACT_TYPE = "raw_multiday_manifest_eligibility_gate_rerun_report"`,
   `_AUGMENT_PHASE_ID = "4bl-D-R"`, predecessor lineage values, and
   remediation lineage values (all SHA256 hex literals match the
   recorded values for Phase 4bl-D and Phase 4bl-D-S2 exactly).
2. **`augment_report` contract** (10 tests): verify the function
   is pure (does not mutate input), preserves the gate-produced
   `checks`, `per_file_validation_summary`, `aggregate_summary`,
   `governance_labels`, `non_authorizations`,
   `retained_verdict_ledger`, and `preserved_locks` blocks verbatim,
   sets `phase_id = "4bl-D-R"`, adds the predecessor lineage
   fields, adds the remediation lineage fields, records the
   pre/post sidecar SHAs, records the target raw zip SHA, preserves
   the no-authorisation invariants, and records the wrapper metadata.
3. **Deterministic serialisation** (1 test): verify
   `json.dumps(sort_keys=True, indent=2, ensure_ascii=False) + "\n"`
   produces stable, sorted-key bytes.
4. **Forbidden import / token static guards** (2 tests): scan the
   wrapper source for forbidden import tokens (`requests`, `httpx`,
   `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`,
   `binance`, `dotenv`) and forbidden runtime tokens
   (`os.environ[`, `os.getenv(`, `BINANCE_API_KEY`,
   `BINANCE_API_SECRET`, `MCP`, `Graphify`, `.mcp.json`). All
   absent.

Test execution result:

```text
uv run pytest tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py
============================= 23 passed in 0.07s ==============================
```

## 6. Execution

The wrapper was executed exactly once on the synchronised
`phase-4bl-d-r/multi-day-raw-manifest-eligibility-gate-rerun` branch:

```text
uv run python -X utf8 scripts/phase4bl_d_r_rerun_raw_gate.py
```

The gate started at `created_at_unix_ms = 1778717359124`
(`2026-05-14T00:09:19.124000Z`) and completed in
`run_wall_clock_seconds = 893.984` (~14.9 minutes). The wall-clock
runtime is consistent with the Phase 4bl-D first run
(`880.188 s` per the Phase 4bl-D report).

## 7. Result

### Final verdict

**`RAW_MULTIDAY_GATE_PASS`** (`overall_status = "pass"`).

### Check counts

| Status | Count |
| --- | ---: |
| PASS | 33 |
| FAIL | 0 |
| ERROR | 0 |
| NOT_APPLICABLE | 0 |
| **Total** | **33** |

The four previously-failing Phase 4bl-D checks now all pass:

| Check ID | Phase 4bl-D status | Phase 4bl-D-R status |
| --- | --- | --- |
| `raw_zip_sidecar_integrity` | FAIL | PASS |
| `per_file_row_count_consistency` | FAIL | PASS |
| `per_file_time_bounds_consistency` | FAIL | PASS |
| `total_row_count_consistency` | FAIL | PASS |

The remaining 29 Phase 4bl-D PASS checks remain PASS.

### Aggregate recomputation

| Quantity | Manifest | Recomputed (Phase 4bl-D-R) | Status |
| --- | ---: | ---: | --- |
| `total_row_count` | 155,153,449 | 155,153,449 | MATCH |
| `total_size_bytes` | 1,943,823,208 | 1,943,823,208 | MATCH |

The 2025-01-15 file's per-row Phase 4ax `validate_aggtrade_payload`
pass count is 1,681,098 (matches the Phase 4az fixture row count and
the Phase 4bl-C manifest entry for 2025-01-15 exactly). The
shortfall observed in Phase 4bl-D (`recomputed_total_row_count =
153,472,351`, exactly 1,681,098 short) is fully recovered.

### Per-file validation summary

90 of 90 dates report `status = "pass"` (no schema validation
errors, no timestamp boundary errors, no duplicate aggregate trade
IDs, no monotonicity violations, no adjacent-date overlap errors).

### Augmented report location and SHA

- **Path:**
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`
- **Size:** 171,342 bytes
- **SHA256:**
  `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`
- **Paired sidecar path:** same path with `.sha256` suffix
- **Sidecar size:** 155 bytes
- **Sidecar body format:**
  `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46  microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json\n`
  (two spaces between the hex digest and the basename; one trailing
  LF; canonical Phase 4bb-F format).
- **Sidecar self-SHA256:**
  `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02`
- **Sidecar parses to a token that matches the recomputed augmented
  report SHA bit-for-bit.**

Both files are gitignored under `.gitignore:85: data/microstructure/`
(verified via `git check-ignore -v`).

### Predecessor and remediation lineage in the augmented report

- `predecessor_gate_phase = "4bl-D"`,
  `predecessor_gate_id = "4bl-d"`,
  `predecessor_gate_verdict = "RAW_MULTIDAY_GATE_FAIL"`,
  `predecessor_gate_overall_status = "fail"`,
  `predecessor_gate_report_sha256 = "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7"`,
  `predecessor_gate_failed_check_ids = ["raw_zip_sidecar_integrity",
  "per_file_row_count_consistency",
  "per_file_time_bounds_consistency",
  "total_row_count_consistency"]`,
  `predecessor_gate_failure_summary = <records the CRLF root cause
  and the Phase 4bl-D-S2 remediation>`.
- `remediation_phase = "4bl-D-S2"`,
  `remediation_type = "metadata_sidecar_line_ending_canonicalization"`,
  `remediation_report_sha256 = "8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3"`,
  `canonicalized_sidecar_pre_sha256 = "b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d"`,
  `canonicalized_sidecar_post_sha256 = "c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc"`,
  `target_raw_zip_sha256 = "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"`.

### Governance labels (verbatim in the augmented report)

```text
backtest              = forbidden
diagnostics           = forbidden
feature_computation   = forbidden
labels                = forbidden
ml                    = forbidden
phase                 = 4bl-d-r
source_phase_boundary = 4bl-D-S2
stop_trigger_domain   = trade_price_backtest_candidate
strategy              = forbidden
strategy_use          = forbidden
validator             = phase_4ax_aggtrades_v001
```

### Non-authorisations (verbatim in the augmented report)

All 21 `non_authorizations.*` keys are `false`:
`acquisition_authorized`, `additional_downloads_authorized`,
`normalization_authorized`, `derived_generation_authorized`,
`feature_generation_authorized`, `label_generation_authorized`,
`diagnostics_authorized`, `label_statistics_authorized`,
`ml_authorized`, `strategy_authorized`, `signal_authorized`,
`backtest_authorized`, `successor_state_authorized`,
`phase_4bl_e_authorized`, `phase_5_authorized`,
`paper_shadow_authorized`, `live_authorized`,
`exchange_write_authorized`, `manifest_transition_authorized`,
`research_eligible_flip_authorized`,
`eligibility_gate_status_transition_authorized`.

The augmented report's own top-level invariants additionally record
`research_eligible_after = false`,
`eligibility_gate_status_after = "pass_report_level_only"`,
`manifest_mutated = false`,
`manifest_transition_performed = false`,
`no_successor_authorization = true`,
`strict_fail_closed = true`.

## 8. Upstream immutability (verified pre/post)

| Artefact | Size (bytes) | SHA256 (post-rerun) | Status |
| --- | ---: | --- | --- |
| target sidecar (canonicalised) | 99 | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` | IDENTICAL |
| target raw zip | 21,271,119 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | IDENTICAL |
| v002 raw manifest | 105,052 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
| v002 acquisition log | 302,055 | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
| Phase 4bl-D gate report | 169,637 | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` | IDENTICAL |
| Phase 4bl-D-S2 canonicalisation report | 5,241 | `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3` | IDENTICAL |

All six upstream artefact SHAs match the recorded values from
Phase 4az, Phase 4bl-C, Phase 4bl-D, and Phase 4bl-D-S2 exactly.

## 9. Manifest state preservation

The on-disk v002 raw manifest still carries:

```text
research_eligible:        false
eligibility_gate_status:  pending
```

No `research_eligible` flag flipped. No `eligibility_gate_status`
transition performed. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant was preserved (never invoked).

## 10. Validation

| Check | Result |
| --- | --- |
| `python -m py_compile scripts/phase4bl_d_r_rerun_raw_gate.py` | OK |
| `python -m py_compile tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py` | OK |
| `uv run ruff check scripts/phase4bl_d_r_rerun_raw_gate.py tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py` | All checks passed |
| `uv run pytest tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py` | 23 passed |
| Gate-rerun execution (one-shot) | `RAW_MULTIDAY_GATE_PASS` (33 / 33) |
| Augmented report SHA256 vs sidecar token | MATCH |
| Augmented report sidecar body in canonical Phase 4bb-F format | YES |
| Augmented report and sidecar gitignored | YES (`.gitignore:85`) |
| Six upstream artefacts byte-identical pre/post | YES |
| v002 raw manifest `research_eligible` / `eligibility_gate_status` unchanged | YES |
| `git diff --check` | clean |

Whole-repo `ruff` / `mypy` / `pytest` were NOT rerun by Phase 4bl-D-R
because no prior source module was modified. The wrapper is a new
file; its scoped ruff check passes; its 23 offline tests pass. The
gate script itself is unchanged.

## 11. Boundary confirmations

| Confirmation | Value |
| --- | --- |
| `research_eligible_after_is_false` | true |
| `no_manifest_mutation` | true |
| `no_eligibility_gate_status_transition_on_actual_manifest` | true |
| `no_chronological_split_policy_change` | true |
| `no_data_microstructure_write_outside_gate_reports_raw` | true |
| `no_normalization_written` | true |
| `no_feature_computed` | true |
| `no_label_computed` | true |
| `no_diagnostic_computed` | true |
| `no_ml_trained` | true |
| `no_strategy_created` | true |
| `no_backtest_run` | true |
| `no_acquisition_performed` | true |
| `no_network_io` | true |
| `no_credential_read` | true |
| `no_env_read` | true |
| `no_dot_mcp_json_read_or_created` | true |
| `no_mcp_enabled` | true |
| `no_graphify_enabled` | true |
| `phase_4bb_f_canonical_path_policy_preserved` | true |
| `phase_4bl_d_gate_protocol_preserved_verbatim` | true |
| `phase_4bl_d_gate_script_unchanged` | true |
| `phase_4aw_flip_research_eligible_always_raises_invariant_preserved` | true |
| `33_check_protocol_executed_in_full` | true |
| `full_per_row_validation_executed_across_all_rows` | true |
| `no_protocol_weakening` | true |
| `successor_authorizes_next_phase` | false |
| `no_successor_authorization` | true |

## 12. Retained verdict ledger (preserved verbatim)

| ID | Status |
| --- | --- |
| H0 | FRAMEWORK ANCHOR |
| R3 | BASELINE-OF-RECORD |
| R1a | RETAINED — NON-LEADING |
| R1b-narrow | RETAINED — NON-LEADING |
| R2 | FAILED — §11.6 |
| F1 | HARD REJECT |
| D1-A | MECHANISM PASS / FRAMEWORK FAIL |
| 5m thread | OPERATIONALLY CLOSED (Phase 3t) |
| V2 | HARD REJECT — terminal for V2 first-spec |
| G1 | HARD REJECT — terminal for G1 first-spec |
| C1 | HARD REJECT — terminal for C1 first-spec |

## 13. Preserved project locks (verbatim)

- §11.6 = 8 bps per side; round-trip = 16 bps;
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max
  / mark-price stops;
- Phase 3p §4.7 strict integrity gate;
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule;
- Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w methodology;
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down
  families list + memo template;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant;
- Phase 4bb-F canonical path policy (Phase 4bl-D-R follows it
  verbatim — the rerun report filename contains the canonical
  `phase-4bl-d-r` segment and is written under
  `data/microstructure/gate-reports/raw/`);
- Phase 4bl-C v002 acquisition results (90-date BTCUSDT raw dataset;
  155,153,449 events; 1,943,823,208 bytes) — preserved verbatim.

## 14. No-rescue and successor-not-authorised statement

Phase 4bl-D-R is the operator-authorised rerun of the Phase 4bl-D
gate against the unchanged v002 dataset with the Phase 4bl-D-S2-
canonicalised sidecar in place. The PASS verdict is **descriptive
evidence only**. Phase 4bl-D-R does **not**:

- modify the Phase 4bl-D gate script;
- weaken any of the 33 Phase 4bl-D checks;
- relax the sidecar parser to accept CRLF;
- amend the Phase 4bb-F canonical path policy;
- amend the Phase 4ak M0 twelve-clause gate, post-null cooldown rule,
  cooled-down families list, or memo template;
- amend the Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy;
- amend the Phase 4aw `flip_research_eligible(...)` always-raises
  invariant;
- modify any prior data/microstructure/ artefact (every raw zip /
  sidecar / manifest / log / gate report / successor-state / parquet
  / canonicalization-report artefact is byte-identical pre/post);
- flip `research_eligible` on any actual manifest;
- transition `eligibility_gate_status` on any actual manifest;
- change `chronological_split_policy` on any actual manifest;
- revise any retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 /
  D1-A / 5m thread / V2 / G1 / C1);
- change any project lock;
- acquire data;
- download anything;
- call any Binance, public, or private endpoint;
- open any WebSocket;
- use any credential;
- read or create `.env`;
- create or read `.mcp.json`;
- enable MCP or Graphify;
- run normalization, derivation, features, labels, diagnostics, ML,
  strategy, signals, or backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha /
  edge / prediction / model-score / decision-score / entry-exit /
  strategy output;
- create a successor-state artefact;
- mutate the original v002 raw manifest field
  `research_eligible` from `false` (it remains `false`);
- mutate the original v002 raw manifest field
  `eligibility_gate_status` from `"pending"` (it remains `"pending"`);
- authorise Phase 4bl-E (Multi-Day Raw Manifest Successor-State
  Recording), Phase 4bm-* (Multi-Day Derived / Normalised Family
  arc), Phase 4bn-* (Multi-Day Feature arc), Phase 4bo-* (Multi-Day
  Label arc), Phase 4bp-* (Multi-Day Label Diagnostic arc),
  Phase 4bq-* (Multi-Day Chronological Split arc), Phase 5, Phase 4
  canonical, paper / shadow, live-readiness, deployment,
  exchange-write, production-key creation, authenticated APIs,
  private endpoints, user stream, or live WebSocket implementation.

The Phase 4bl-D-R PASS report is sufficient evidence at the **report
level** that the v002 dataset (with the Phase 4bl-D-S2-canonicalised
sidecar in place) clears the full 33-check Phase 4bl-D protocol.
Whether this becomes a Stage-2 transition (`pending → pass`) on the
v002 manifest field depends on a future, separately authorised
successor-state recording phase — by precedent, that would be
**Phase 4bl-E** (analogue of Phase 4bb-G for the raw family at the
v002 level). Phase 4bl-D-R does not authorise Phase 4bl-E.

## 15. Lifecycle anchors

- **`main` / `origin/main` at branch creation:**
  `69e45280f080e320171f1d851933fdb13213aaea`
- **Phase 4bl-D project-complete anchor:**
  `01ca1d07c601655e3c66b6349038ea4385d4e281` (Phase 4bl-D
  merge-closeout commit)
- **Phase 4bl-D-S1 project-complete anchor:**
  `0d51bd7bac1eec1e11d7bad280e480dd8674a97f` (Phase 4bl-D-S1
  merge-closeout commit)
- **Phase 4bl-D-S2 project-complete anchor:**
  `69e45280f080e320171f1d851933fdb13213aaea` (Phase 4bl-D-S2
  merge-closeout commit)
- **Gate rerun start (`created_at_unix_ms`):** `1778717359124`
- **Gate rerun start (`created_at_utc`):** `2026-05-14T00:09:19.124000Z`
- **Wall-clock seconds:** `893.984`
- **Phase 4bl-D-R `code_commit_sha` recorded inside the report:**
  `69e45280f080e320171f1d851933fdb13213aaea`

## 16. Phase 4bl-D-R is branch-complete only

Per the Phase 4bk-A workflow standard, Phase 4bl-D-R is
**branch-complete only by this work**; it is NOT project-complete
until a separately authorised merge phase records its merge-closeout
on `main`. Phase 4bl-D-R does not authorise its own merge.

## 17. Recommended state

**Remain paused** unless the operator separately authorises a
Phase 4bl-D-R merge phase, then a separately authorised
Phase 4bl-E phase (Multi-Day Raw Manifest Successor-State
Recording). Phase 4bl-D-R does not recommend or authorise any
successor by itself.
