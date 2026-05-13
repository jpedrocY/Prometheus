# Phase 4bl-D Closeout

## Status

**Branch-complete only.** Per the Phase 4bk-A workflow standard,
Phase 4bl-D is NOT project-complete until a separately authorized
merge phase records its merge-closeout on `main`. This phase does
not authorize any successor.

**Gate verdict: `RAW_MULTIDAY_GATE_FAIL`** (4 / 33 critical-severity
checks failed; single root cause; one pre-existing Phase 4az fixture
sidecar; no remediation attempted; no manifest mutation).

## Identity

- **Phase**: Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate /
  Raw QA
- **Type**: docs + code + one local gitignored raw gate-report
  artefact (plus its paired `.sha256` sidecar)
- **Branch**:
  `phase-4bl-d/multi-day-raw-manifest-eligibility-gate`
- **Base commit (main / origin/main at branch creation)**:
  `2576a004c18a76e939303e794317d346c75303d2` (Phase 4bl-C SHA-chain
  fixup; one commit after the Phase 4bl-C merge-closeout commit
  `2ec0a9a5b18214aff99fe86a5fcea3702e20313e`)

## Files changed (tracked)

- `scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py` (new;
  standalone gate script)
- `tests/research/microstructure/test_phase4bl_d_raw_gate.py` (new;
  41 offline tests)
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d_multi-day-raw-manifest-eligibility-gate.md`
  (new; this phase's implementation report)
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d_closeout.md`
  (new; this closeout)
- `docs/00-meta/current-project-state.md` (narrow update: new Phase
  4bl-D narrative paragraph + new "Current phase:" block; prior
  Phase 4bl-C "Current phase:" block preserved as historical
  context)

Nothing else is committed. No `data/microstructure/` artefact is
committed.

## Local gitignored output (NOT committed)

- **Gate report**:
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
  - SHA256:
    `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`
  - Size: 169,637 bytes
- **Gate report sidecar**:
  same path + `.sha256`
  - SHA256 (self):
    `b201dcd977ea2ef370b502f3840d90d6efd28b10354ca30eafcf155838c7a9c6`
  - Size: 153 bytes
  - Body: canonical Phase 4bb-F `<sha>  <basename>\n` (two spaces,
    trailing LF)

Both files are gitignored under `.gitignore:85: data/microstructure/`.

## Exact gate result

- `overall_status`: **fail**
- `gate_verdict`: **RAW_MULTIDAY_GATE_FAIL**
- `checks_total / passed / failed / error / not_applicable`:
  33 / 29 / 4 / 0 / 0
- `recomputed_total_row_count`: 153,472,351
  (manifest expected 155,153,449; shortfall exactly 1,681,098 — the
  recorded Phase 4az 2025-01-15 row count)
- `recomputed_total_size_bytes`: 1,943,823,208
  (matches manifest and Phase 4bl-C expected exactly)
- `all_rows_validated_count`: 153,472,351
  (every iterated aggTrade row passed Phase 4ax
  `validate_aggtrade_payload`)
- `acquired_file_count`: 89 / 90 reached per-row validation
  (`2025-01-15` stopped at sidecar-parse step under fail-closed
  discipline)
- `existing_fixture_preservation_zip_sha`: pass (2025-01-15 zip
  SHA256 matches Phase 4az recorded value
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`)
- `manifest_mutated`: false
- `manifest_transition_performed`: false
- `research_eligible_after`: false
- `eligibility_gate_status_after`: `fail_report_level_only`
  (report-level only; the on-disk v002 manifest's
  `eligibility_gate_status` remains `pending`)
- `no_successor_authorization`: true
- `strict_fail_closed`: true

**Failure analysis (single root cause; four cascaded checks)**:

The pre-existing Phase 4az 2025-01-15 fixture sidecar uses Windows
CRLF (`\r\n`) line terminator (100 bytes) instead of the canonical
Phase 4bb-F LF (`\n`) terminator (99 bytes for the same basename).
All 89 Phase 4bl-C newly-acquired sidecars, the v002 manifest
sidecar, and the v002 acquisition-log sidecar use canonical LF.
Under fail-closed discipline, the gate rejected the CRLF sidecar
on parse, skipped per-row validation for that date only (the rest
of the 89 dates ran clean), and recorded the cascading effects in
the gate report verbatim:

1. `raw_zip_sidecar_integrity` — critical FAIL — 1 sidecar format
   failure on `2025-01-15`; 0 sidecar SHA mismatches.
2. `per_file_row_count_consistency` — critical FAIL — mismatched
   dates `['2025-01-15']` because the gate's recomputed row_count
   is `None` (validation skipped) while the manifest entry is
   `1,681,098`.
3. `per_file_time_bounds_consistency` — critical FAIL — mismatched
   bounds `['2025-01-15: first_trade_time_ms', '2025-01-15:
   last_trade_time_ms', '2025-01-15: min_agg_trade_id', '2025-01-15:
   max_agg_trade_id']` because the gate did not iterate 2025-01-15
   rows.
4. `total_row_count_consistency` — critical FAIL —
   `recomputed_total_row_count = 153,472,351` vs
   `manifest_total_row_count = 155,153,449`; shortfall exactly
   equals the Phase 4az 2025-01-15 row count.

The 2025-01-15 **zip** is byte-identical to the Phase 4az fixture
(`f560c2e5...` matches manifest and Phase 4az recorded values
exactly). Only the **sidecar's line terminator** differs from
canonical. No remediation was attempted; the result is recorded
as descriptive evidence only.

## Validation results

- `git status --short` after the gate run shows only the tracked
  Phase 4bl-D docs/script/test files staged for commit (no
  `data/microstructure/` artefact is staged).
- `git diff --check`: clean.
- `git check-ignore -v data/microstructure/`: `.gitignore:85`.
- `git check-ignore -v data/microstructure/gate-reports/raw/`:
  `.gitignore:85`.
- `python -m py_compile scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`:
  OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_d_raw_gate.py`:
  OK.
- `uv run ruff check scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`:
  All checks passed.
- `uv run ruff check tests/research/microstructure/test_phase4bl_d_raw_gate.py`:
  All checks passed.
- `uv run pytest tests/research/microstructure/test_phase4bl_d_raw_gate.py`:
  41 passed.
- Whole-repo `pytest` and whole-repo `mypy` were NOT rerun by Phase
  4bl-D (no source-package code was modified). The latest
  authoritative whole-repo validation remains the Phase
  4bb-F-implementation merge baseline.
- v002 manifest / log / sidecars / existing 2025-01-15 fixture all
  have byte-identical SHA256s pre and post the gate run.

## Output SHAs

- Gate report SHA256:
  `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`
- Gate report sidecar SHA256 (self):
  `b201dcd977ea2ef370b502f3840d90d6efd28b10354ca30eafcf155838c7a9c6`
- Gate report sidecar body matches recomputed report SHA bit-for-bit.

## Retained verdicts preserved verbatim

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

## Project locks preserved

- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position
  max / mark-price stops.
- M0 (Phase 4ak) twelve-clause gate, post-null cooldown rule, and
  cooled-down families list remain binding.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
  remains binding.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant remains binding (never invoked by Phase
  4bl-D).
- Phase 3v §8 stop-trigger-domain governance remains binding.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance remains binding.
- Phase 4bb-F canonical path policy remains binding (Phase 4bl-D
  follows it for the gate-report filename and identified one
  pre-existing Phase 4az fixture sidecar that does not conform —
  recorded as a finding, not amended).

## No-successor / no-rescue constraints

Phase 4bl-D explicitly does NOT authorize:

- Phase 4bl-E (multi-day raw successor-state recording);
- Phase 4bm-* (multi-day derived arc);
- Phase 4bn-* (multi-day feature arc);
- Phase 4bo-* (multi-day label arc);
- Phase 4bp-* (multi-day diagnostics);
- Phase 4bq-* (multi-day chronological split);
- Phase 5;
- Phase 4 canonical;
- any remediation of the Phase 4az 2025-01-15 sidecar CRLF
  terminator (Options B1 / B2 / B3 in the implementation report's
  §8 operator decision menu);
- normalization, derived parquet, features, labels, diagnostics,
  ML, strategy, signals, backtests;
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book / spot / cross-venue / funding / open-interest data
  acquisition;
- paper / shadow / live-readiness / deployment / exchange-write /
  production-key creation / authenticated APIs / private endpoints
  / user stream / live WebSocket implementation;
- MCP, Graphify, `.mcp.json`, credentials;
- mutation of the v002 manifest, the v002 acquisition log, any
  paired sidecar, any prior gate report, any successor-state
  artefact, the Phase 4az fixture, or any other `data/microstructure/`
  artefact;
- flipping `research_eligible` on the v002 manifest or any other
  manifest;
- transitioning `eligibility_gate_status` on the v002 manifest or
  any other manifest;
- changing `chronological_split_policy` on any manifest.

## Recommended state

**Remain paused** after Phase 4bl-D branch completion. The gate FAIL
is recorded as descriptive evidence only; no remediation is
authorized by this phase.

The natural conditional next step (NOT authorized by Phase 4bl-D) is
a separately authorized docs-only **sidecar-canonicalization
governance memo** that decides among:

- **B1**: normalize the Phase 4az 2025-01-15 sidecar to canonical
  LF and re-run a future Phase 4bl-D-equivalent gate;
- **B2**: amend the Phase 4bb-F canonical sidecar format to
  grandfather the Phase 4az fixture sidecar CRLF;
- **B3**: amend the gate to accept CRLF as canonical-equivalent.

Each of B1 / B2 / B3 mutates a pre-existing artefact or a governance
contract and therefore requires separate operator authorization.
Phase 4bl-D does NOT recommend any of the three; the operator
decision is deferred. The natural conditional follow-on (Phase
4bl-E — Multi-Day Raw Manifest Successor-State Recording) remains
unauthorized and is not appropriate while the Phase 4bl-D gate
verdict is FAIL.
