# Phase 4bl-C Closeout

**Phase:** Phase 4bl-C — Multi-Day aggTrades Acquisition Execution.
**Date:** 2026-05-12.
**Branch:** `phase-4bl-c/multi-day-aggtrades-acquisition-execution`.
**Base:** `main` at `da9d830c2b900c1c5fa09159e79ce2f0b6bbe249` (Phase 4bl-B SHA-chain-fixup commit; predecessor anchor is the Phase 4bl-B merge-closeout commit `31e907fcb2034a45257f6f2513fc5b51b48f5e8f`).
**Status:** branch-complete only.

---

## 1. Branch-complete status

Phase 4bl-C is **branch-complete only by this work**. Per the Phase 4bk-A workflow standard, Phase 4bl-C is **NOT project-complete** until a separately authorized merge phase records a Phase 4bl-C merge-closeout on `main`. The canonical project-complete anchor for Phase 4bl-C will be the future Phase 4bl-C merge-closeout commit on `main`, not the branch tip.

---

## 2. Files changed (tracked)

Phase 4bl-C adds four tracked files:

1. `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` — the standalone acquisition orchestrator (Python stdlib + Phase 4ax / 4aw scaffold only).
2. `tests/research/microstructure/test_phase4bl_c_acquisition_script.py` — 71 offline tests covering date-list generation, URL allowlist, path discipline, sidecar format, checksum parsing, SHA256 helpers, atomic write, capture-config hash, ZIP inventory + row-sample validation, module-level import-boundary guarantees, `acquire_one_date(do_network=False)` paths, CLI dry-run, CLI reject-outside-microstructure, and JSON determinism.
3. `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-c_multi-day-aggtrades-acquisition-execution.md` — the 8-section Phase 4bl-C implementation report.
4. `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-c_closeout.md` — this closeout.

Phase 4bl-C narrowly modifies one tracked file:

- `docs/00-meta/current-project-state.md` — adds a new Phase 4bl-C narrative paragraph above the Phase 4bl-B paragraph; replaces the existing top "Current phase:" block (Phase 4bl-B's) with a new Phase 4bl-C block; preserves the prior Phase 4bl-B block as historical context immediately below the new block.

No other source / test / script / configuration / governance file is modified. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP files, and all prior phase memos are unchanged.

---

## 3. Local outputs (gitignored; NOT committed)

Phase 4bl-C produced the following local artefacts under `data/microstructure/` (all gitignored under `.gitignore:85`, none committed):

- 90 raw aggTrades `.zip` files under `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/...` (one per locked UTC date; the `2025-01-15` fixture is the existing Phase 4az file reused in place);
- 90 paired `.sha256` sidecars at the matching `.zip.sha256` paths (canonical Phase 4bb-F format);
- one v002 multi-day raw manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`;
- one paired `.sha256` sidecar at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json.sha256`;
- one v002 acquisition log at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`;
- one paired `.sha256` sidecar at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256`.

Live SHA256 values for the four manifest / log files are recorded in §4 of the Phase 4bl-C implementation report and verbatim in the final operator report. They are reproducible from the public archive at any time by re-running the orchestrator script (with the Phase 4ax / 4aw scaffold and the existing one-day fixture in place).

The existing Phase 4az one-day fixture (`2025-01-15`) was reused in place and is byte-identical pre/post Phase 4bl-C (SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`).

---

## 4. Exact acquisition result

The orchestrator returned **`overall_status = SUCCESSFUL_ACQUISITION`**. All 90 locked UTC dates achieved `acquired_verified`. Summary counters were:

- `acquired_file_count = 90`;
- `missing_file_count = 0`;
- `checksum_mismatch_count = 0`;
- `checksum_companion_unavailable_count = 0`;
- `decompression_failure_count = 0`;
- `row_sample_validation_failure_count = 0`;
- `finalisation_failure_count = 0`;
- `retry_exhausted_count = 0`;
- `total_size_bytes = 1,943,823,208`;
- `total_row_count = 155,153,449`;
- `wall_clock_seconds = 717`;
- `existing_fixture_reused = true`;
- `existing_fixture_sha_match = true`.

See §4 of the Phase 4bl-C implementation report (`2026-05-12_phase-4bl-c_multi-day-aggtrades-acquisition-execution.md`) for the cross-checked supplementary log evidence (`acquisition_run_id`, `started_at_utc` / `finished_at_utc`, `events` array breakdown, 0 errors). The full per-date detail is in the gitignored v002 multi-day manifest's `per_file_inventory` field; the chronological event log is in the gitignored acquisition log's `events` field.

---

## 5. Output SHAs

Verbatim SHA256 values for the four manifest / log files produced by the live run:

| Artefact | SHA256 | Size (bytes) |
| --- | --- | --- |
| v002 multi-day manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | 105,052 |
| v002 manifest sidecar | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` | 111 |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | 302,055 |
| v002 log sidecar | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` | 127 |

The manifest pins its corresponding log's SHA via the `acquisition_log_sha256 = 52f6d7fb3cb0…0c6b314` field, and each sidecar pins its paired manifest / log file via the canonical `<sha>  <basename>\n` body. The two artefacts are therefore tamper-evident relative to each other and relative to their own sidecars.

The existing one-day Phase 4az fixture's SHA256 (`f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`) is byte-identical pre/post Phase 4bl-C and is the same value recorded in the v002 manifest's `per_file_inventory` entry for `2025-01-15` (in both the `sha256` and `sha256_from_companion` fields — three-way agreement: recorded ↔ fresh-local ↔ fresh-companion).

---

## 6. Validation results

Pre-run validation:

- `git rev-parse main` → `da9d830c2b900c1c5fa09159e79ce2f0b6bbe249`;
- `git rev-parse origin/main` → `da9d830c2b900c1c5fa09159e79ce2f0b6bbe249`;
- `git status` → clean (only `.claude/scheduled_tasks.lock` + gitignored `data/research/` as untracked);
- `python -m py_compile scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` → OK;
- `python -m py_compile tests/research/microstructure/test_phase4bl_c_acquisition_script.py` → OK;
- `uv run ruff check scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py tests/research/microstructure/test_phase4bl_c_acquisition_script.py` → All checks passed!
- `uv run pytest tests/research/microstructure/test_phase4bl_c_acquisition_script.py` → 71 passed;
- `uv run python scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py --dry-run` → prints locked plan with `date_count: 90`, first dates `['2024-12-01', '2024-12-02', '2024-12-03']`, last dates `['2025-02-26', '2025-02-27', '2025-02-28']`, and "No download will be performed.";
- `git check-ignore --verbose` on each intended output path (`data/microstructure/`, `data/microstructure/raw/`, `data/microstructure/manifests/`, a representative future raw-zip path, the v002 manifest path, the v002 log path) → all return `.gitignore:85: data/microstructure/`.

Post-run validation:

- `git diff --check` → clean;
- `git status` (post-commit) → only the always-untracked `.claude/scheduled_tasks.lock` plus the gitignored `data/research/` directory; **no `data/microstructure/` artefact is staged or tracked at any point**; the five tracked Phase 4bl-C changes (four new files: orchestrator script, offline test suite, implementation report, this closeout; one narrow modification: `docs/00-meta/current-project-state.md`) are committed on the Phase 4bl-C branch only;
- `git check-ignore --verbose data/microstructure/` → `.gitignore:85: data/microstructure/`;
- SHA256 recomputation of the v002 manifest file = `016967865c97…1d87485` (matches the manifest sidecar's parsed value bit-for-bit);
- SHA256 recomputation of the v002 acquisition log file = `52f6d7fb3cb0…0c6b314` (matches both the log sidecar's parsed value and the manifest's embedded `acquisition_log_sha256` field bit-for-bit);
- existing Phase 4az fixture SHA256 = `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` bit-for-bit;
- all 15 listed upstream artefacts byte-identical pre/post Phase 4bl-C (full list in §6.5 of the implementation report; verified via `sha256sum` after the orchestrator finished).

mypy and whole-repo pytest were **not rerun** by Phase 4bl-C because Phase 4bl-C does not modify any prior source module beyond adding one new standalone script and one new offline test file. The latest authoritative whole-repo validation remains the Phase 4bb-F-implementation merge baseline (ruff PASS, mypy strict 120 source files PASS, microstructure pytest 915 passed + 1 pre-existing labelled skip, whole-repo pytest 1698 passed + 1 skipped + 2 pre-existing simulation failures).

---

## 7. Retained verdicts preserved

All retained verdicts are preserved verbatim through Phase 4bl-C:

- **H0** — FRAMEWORK ANCHOR. Preserved.
- **R3** — BASELINE-OF-RECORD. Preserved.
- **R1a** — RETAINED — NON-LEADING. Preserved.
- **R1b-narrow** — RETAINED — NON-LEADING. Preserved.
- **R2** — FAILED — §11.6 cost-sensitivity blocks. Preserved.
- **F1** — HARD REJECT. Preserved.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other. Preserved.
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t. Preserved.
- **V2** — HARD REJECT — terminal for V2 first-spec. Preserved.
- **G1** — HARD REJECT — terminal for G1 first-spec. Preserved.
- **C1** — HARD REJECT — terminal for C1 first-spec. Preserved.

No retained verdict is revised by Phase 4bl-C. No retained verdict is silently reframed. No retained verdict is re-evaluated on the prospective multi-day substrate by Phase 4bl-C (the multi-day acquisition is data infrastructure only; it does not constitute strategy evidence).

---

## 8. Locks preserved

All project locks are preserved verbatim through Phase 4bl-C:

- **§11.6 cost lock** — HIGH cost = 8 bps slippage per side; round-trip = 16 bps slippage.
- **§1.7.3 project-level locks** — 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops.
- **Phase 3p §4.7 strict integrity gate.**
- **Phase 3r §8 mark-price gap governance.**
- **Phase 3v §8 stop-trigger-domain governance.**
- **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.**
- **Phase 4j §11 metrics OI-subset partial-eligibility rule.**
- **Phase 4k V2 backtest-plan methodology.**
- **Phase 4p G1 strategy-spec memo.**
- **Phase 4q G1 backtest-plan methodology.**
- **Phase 4v C1 strategy-spec memo.**
- **Phase 4w C1 backtest-plan methodology.**
- **Phase 4ak M0 mechanism-admissibility twelve-clause gate.**
- **Phase 4ak post-null cooldown rule.**
- **Phase 4ak cooled-down families list.**
- **Phase 4ak future M0 memo template.**
- **Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.**
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant.**
- **Phase 4bb-F canonical path policy.**

No project lock is modified by Phase 4bl-C. No project lock is silently weakened. No project lock is amended.

---

## 9. No successor authorization

Phase 4bl-C does **not** authorize any successor phase. Specifically:

- Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate / Raw QA: **NOT authorized**;
- Phase 4bl-E — Multi-Day Raw Manifest Successor-State Recording: **NOT authorized**;
- Phase 4bm-* — Multi-Day Derived (Normalized) Family arc: **NOT authorized**;
- Phase 4bn-* — Multi-Day Feature arc: **NOT authorized**;
- Phase 4bo-* — Multi-Day Label arc: **NOT authorized**;
- Phase 4bp-* — Multi-Day Label Diagnostic arc: **NOT authorized**;
- Phase 4bq-* — Multi-Day Chronological Split arc: **NOT authorized**;
- ML feasibility memo: **NOT authorized**;
- Baseline ML diagnostic: **NOT authorized**;
- Failure interpretation / fallback selection memo: **NOT authorized**;
- Strategy hypothesis under M0: **NOT authorized**;
- Strategy spec: **NOT authorized**;
- Backtest plan: **NOT authorized**;
- Backtest execution: **NOT authorized**;
- Paper / shadow: **NOT authorized**;
- Live-readiness: **NOT authorized**;
- Phase 5: **NOT authorized**;
- Phase 4 canonical: **NOT authorized**;
- Exchange-write: **NOT authorized**;
- Production keys: **NOT authorized**;
- Authenticated APIs / private endpoints / user stream / live WebSocket implementation: **NOT authorized**;
- MCP / Graphify / `.mcp.json`: **NOT authorized**;
- Any manifest transition (`research_eligible` flip, `eligibility_gate_status` transition, `chronological_split_policy` change): **NOT authorized**.

The next conditional successor — Phase 4bl-D Multi-Day Raw Manifest Eligibility Gate — would translate the Phase 4bb-D pattern into a v002-multi-day analogue. Phase 4bl-D would require a separate operator authorization prompt; it is not implicit in the Phase 4bl-C branch or in the future Phase 4bl-C merge.

---

## 10. Recommended state

**Remain paused after Phase 4bl-C branch work.** The natural conditional successor is a future operator-authorized merge of this Phase 4bl-C branch into `main` with a Phase 4bl-C merge-closeout per the Phase 4bk-A workflow standard. Per that workflow standard, a separately authorized merge prompt is required before the merge proceeds. After merge + merge-closeout, the next conditional successor (NOT authorized by Phase 4bl-C) would be Phase 4bl-D Multi-Day Raw Manifest Eligibility Gate, or remain-paused.

---

**End of Phase 4bl-C closeout.**
