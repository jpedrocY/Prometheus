# Phase 4bm-D — Closeout

**Phase identity:** Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate.
**Type:** docs-and-code Tier 1 implementation phase.
**Date:** 2026-05-15.
**Branch:** `phase-4bm-d/multi-day-derived-family-eligibility-gate`.
**Status:** branch-complete only by this work; not merged into `main`; not project-complete.

---

## §1 Lifecycle status

Phase 4bm-D is **branch-complete only**.

Per the Phase 4bk-A workflow standard, Phase 4bm-D is **not project-complete** until a separately authorized merge phase records its merge-closeout on `main`.

Not merged. No merge performed by this branch.

---

## §2 SHAs

| Item | SHA |
| ---- | --- |
| `main` HEAD before Phase 4bm-D branch | `d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3` (Phase 4bm-C merge-closeout commit) |
| Phase 4bm-D branch | `phase-4bm-d/multi-day-derived-family-eligibility-gate` |
| Phase 4bm-D implementation commit | `57e1c97e6e938797d448b331cdc27b50b8e935dd` |
| Phase 4bm-D docs/closeout commit | recorded by this commit's `git log` entry; placeholder here (post-commit `git rev-parse HEAD` is the final value) |
| Authoritative gate report SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Authoritative gate report sidecar SHA256 | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |

---

## §3 Authoritative gate report

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` |
| SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Sidecar path | same path with `.json.sha256` suffix |
| Sidecar SHA256 | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| Sidecar body format | canonical Phase 4bb-F `<sha256_lowercase_hex>  <basename>\n` (two ASCII spaces; trailing LF) |
| Overall status | `pass` |
| Gate verdict | `DERIVED_GATE_PASS` |
| Checks total / PASS / FAIL / ERROR / NA | 60 / 60 / 0 / 0 / 0 |
| Boundary confirmations | 19 / 19 `True` |
| `research_eligible_after` | `False` |
| `no_successor_authorization` | `True` |
| `eligibility_gate_status_after` | `"pass"` (report-level recommendation only) |
| `code_commit_sha` recorded | `57e1c97e6e938797d448b331cdc27b50b8e935dd` |

Both files are gitignored under `.gitignore:85` (`git check-ignore -v` confirms). Not committed.

A separate preliminary pre-commit sanity report (SHA `ffde54bb…`; sidecar SHA `11c95251…`; recorded `code_commit_sha = d39ffd8a…`) was retained on disk as a non-authoritative continuity witness; it is not the Phase 4bm-D evidence and the implementation report explicitly marks it as such.

---

## §4 Files added (tracked, by the implementation commit `57e1c97`)

- `src/prometheus/research/microstructure/multiday_derived_gate.py`
- `src/prometheus/research/microstructure/multiday_derived_gate_io.py`
- `src/prometheus/research/microstructure/multiday_derived_gate_checks.py`
- `src/prometheus/research/microstructure/multiday_derived_gate_report.py`
- `tests/research/microstructure/_multiday_derived_gate_fixtures.py`
- `tests/research/microstructure/test_multiday_derived_gate_checks.py`
- `tests/research/microstructure/test_multiday_derived_gate_io.py`
- `tests/research/microstructure/test_multiday_derived_gate_report.py`
- `tests/research/microstructure/test_multiday_derived_gate.py`
- `tests/research/microstructure/test_multiday_derived_gate_no_network.py`

Files modified narrowly (tracked, by the implementation commit `57e1c97`):

- `src/prometheus/research/microstructure/__init__.py` — narrow re-exports for the new public surface.

Files added (tracked, by the docs/closeout commit):

- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-d_multi-day-derived-family-eligibility-gate.md` (this phase's implementation report)
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-d_closeout.md` (this closeout)

Files modified narrowly (tracked, by the docs/closeout commit):

- `docs/00-meta/current-project-state.md` — Phase 4bm-D narrative paragraph + new "Current phase:" block; prior Phase 4bm-C "Current phase:" block preserved as historical context.

---

## §5 Files NOT modified

- No prior `src/prometheus/` module modified beyond the narrow `__init__.py` re-export update.
- No prior `tests/` file modified beyond two `F841` unused-`d`-assignment removals and three `F401` unused-import removals in two Phase 4bm-D-owned test files (`test_multiday_derived_gate_checks.py` + `test_multiday_derived_gate_report.py`), an `I001` import-sort fix in `test_multiday_derived_gate_report.py`, two `SIM300` Yoda swaps in `test_multiday_derived_gate_report.py`, an `I001` import-sort fix in `test_multiday_derived_gate.py`, and a `B007` dead-loop removal in `test_multiday_derived_gate.py` — all in-scope Phase 4bm-D cleanups; no semantic change to test coverage.
- No `scripts/` script modified.
- `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP files — unchanged.
- Every prior `data/microstructure/` artefact (the 90 v002 raw zips and sidecars, the v002 raw manifest and sidecar, the v002 acquisition log and sidecar, the Phase 4bl-D-R gate report and sidecar, the Phase 4bl-E successor-state record and sidecar, the Phase 4bm-B v002 derived manifest and sidecar, the 90 Phase 4bm-B v002 per-day Parquets and 90 sidecars, the Phase 4bd v001 single-day derived parquet, the Phase 4bd derived manifest, the Phase 4bf v001 derived gate report, the Phase 4bg-B successor-state, the Phase 4bh feature parquet and manifest, the Phase 4bj-C label parquet and manifest, every prior gate report and successor-state artefact) — byte-identical pre/post Phase 4bm-D, confirmed by the orchestrator's post-check re-hash (4 mutation-class boundary confirmations all `True`).
- Every prior phase implementation report, closeout, and merge-closeout.

---

## §6 Validation summary

| Tool | Scope | Result |
| ---- | ----- | ------ |
| `ruff check` | 10 Phase 4bm-D source/test files | **PASS** after minimal in-scope cleanups |
| `mypy --strict` | `src/prometheus` | **PASS** — `Success: no issues found in 124 source files` |
| `pytest` | 5 Phase 4bm-D test files | **218 passed in 2.51 s** |
| `git diff --check` | working tree | clean |
| `git status --short` | working tree | only tracked Phase 4bm-D files + pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`) |
| `git check-ignore -v data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` | gate report | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v` … `.sha256` sidecar | sidecar | `.gitignore:85: data/microstructure/` |

Whole-repo `pytest` was not rerun in this implementation phase; the latest authoritative whole-repo baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; the pre-existing 2 simulation failures unrelated to Phase 4bm-D are preserved as the baseline; Phase 4bm-D introduces zero new regressions vs that baseline).

---

## §7 No source artefact mutation

The Phase 4bm-D orchestrator never modifies the derived manifest, any of the 90 per-day Parquets, any sidecar, any raw zip, the raw manifest, the acquisition log, the Phase 4bl-D-R gate report, the Phase 4bl-E successor-state record, or any prior gate report. The four mutation-class boundary confirmations on the authoritative gate result are all `True`:

- `no_manifest_mutation = True`
- `no_per_file_parquet_mutation = True`
- `no_per_file_sidecar_mutation = True`
- `no_raw_zip_mutation = True`

These four are computed by re-hashing every governance artefact + every per-file Parquet + every sidecar + every raw zip post-checks and comparing each value byte-identically against the pre-check SHA. All matched.

---

## §8 No manifest mutation

- v002 derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` — `research_eligible = false` / `eligibility_gate_status = "pending"` preserved byte-for-byte.
- v002 raw manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` — `research_eligible = false` / `eligibility_gate_status = "pending"` preserved byte-for-byte.
- Phase 4bd v001 derived manifest — `research_eligible = false` / `eligibility_gate_status = "pending"` preserved byte-for-byte (never touched by Phase 4bm-D).

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## §9 No research_eligible flip

No manifest's `research_eligible` is mutated by Phase 4bm-D. The `eligibility_gate_status_after = "pass"` value on the new gate report is a **report-level recommendation only**; it is not written back to any manifest, and it does not flip `research_eligible` on any actual manifest.

---

## §10 No successor authorization

Phase 4bm-D does **not** authorize Phase 4bm-D merge phase, Phase 4bm-E, Phase 4bm-F, Phase 4bm-*, Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow / live-readiness / deployment / exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, live WebSocket implementation, MCP / Graphify / `.mcp.json` / credentials, any additional acquisition beyond the 90 locked BTCUSDT UTC dates, any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` on any actual manifest, feature computation, label computation, signal computation, proxy computation, ML training, model selection, feature ranking, meta-labeling, strategy creation, or backtest execution.

---

## §11 Not merged

Phase 4bm-D is not merged into `main`. The conditional next step is a separately authorized Phase 4bm-D merge phase that merges this branch into `main` and records a Phase 4bm-D merge-closeout per `docs/00-meta/process/merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout). That merge phase is not authorized by Phase 4bm-D.

---

## §12 Recommended next step

**Operator review of the Phase 4bm-D implementation report and authoritative gate report, then — if accepted — a separately authorized Phase 4bm-D merge phase per the established Phase 4bk-A workflow standard.**

After merge, the recommended state remains **remain paused** pending operator decision on the conditional Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision Memo) → Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording) ladder. Neither is authorized by Phase 4bm-D.

---

## §13 Retained verdicts and project locks (preserved verbatim)

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec; §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked); Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked — the Phase 4bm-D writer emits canonical LF natively); Phase 4am .. Phase 4bm-C results — all preserved verbatim.

— end of Phase 4bm-D closeout —