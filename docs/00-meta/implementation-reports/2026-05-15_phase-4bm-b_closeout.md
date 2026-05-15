# Phase 4bm-B — Closeout

**Phase identity:** Phase 4bm-B — Multi-Day Normalization Implementation.
**Type:** docs-and-code Tier 1 implementation phase.
**Date:** 2026-05-15.
**Branch:** `phase-4bm-b/multi-day-normalization-implementation`.
**Status:** branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Phase identity and status

Phase 4bm-B operationalises the Phase 4bm-A locked Multi-Day Normalization Design Memo by implementing an offline orchestrator that normalises the v002 multi-day BTCUSDT aggTrades raw archive (90 contiguous UTC dates 2024-12-01..2025-02-28; 155,153,449 events; 1,943,823,208 bytes) into a future normalized derived dataset family with identity `dataset_family = microstructure_normalized_aggtrades_v001` (reused; schema unchanged) and `dataset_version = v002` (new; bounded source-dataset discriminator).

Phase 4bm-B is **branch-complete only** by this work. Per the Phase 4bk-A workflow standard, Phase 4bm-B is not project-complete until a separately authorized merge phase records its merge-closeout on `main`.

---

## 2. SHAs

| Item | SHA |
| ---- | --- |
| `main` HEAD before Phase 4bm-B branch | `56f96a4c613a3d8c8794905be4c1847fcdac5e58` (Phase 4bm-A-P1 merge-closeout) |
| Phase 4bm-A merge commit (predecessor multi-day-normalization design memo) | `af97285` (intermediate ancestor) |
| Phase 4bm-A-P1 merge commit (immediate predecessor on `main`) | `e00e178` |
| Phase 4bm-B branch | `phase-4bm-b/multi-day-normalization-implementation` |
| Phase 4bm-B branch tip (HEAD on this branch) | `80f596daed0fc867f2b0c1d7fc282d8d052f76ae` (feat commit; a follow-up docs commit on this branch may shift the tip — a SHA-chain fixup can record the post-docs HEAD if precise final-HEAD recording is later required, mirroring the Phase 4bm-A merge-closeout pattern) |
| Multi-day index manifest SHA256 (NEW) | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| Multi-day index manifest sidecar SHA256 (NEW) | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |

---

## 3. Files brought forward by this branch

Tracked files added:

- `scripts/phase4bm_b_normalize_multiday_aggtrades.py` (~1,620 lines; standalone offline orchestrator);
- `tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` (~870 lines; 33 tests);
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_multi-day-normalization-implementation.md` (this phase's implementation report);
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_closeout.md` (this closeout).

Tracked files modified narrowly:

- `docs/00-meta/current-project-state.md` (Phase 4bm-B narrative paragraph + new "Current phase:" block; prior Phase 4bm-A-P1 "Current phase:" block preserved as historical context).

No other tracked file modified.

---

## 4. Local gitignored outputs produced (NOT committed)

- 90 per-day Parquet files at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/{2024/12,2025/01,2025/02}/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet`;
- 90 paired canonical Phase 4bb-F sidecars (one per Parquet, `.parquet.sha256`, body `<sha>  <basename>\n`);
- 1 multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`;
- 1 paired manifest sidecar at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256`.

All outputs are under the gitignored `data/microstructure/` namespace (`.gitignore:85`).

---

## 5. Diff summary

| Area | Lines added | Lines removed |
| ---- | ----------- | ------------- |
| `scripts/phase4bm_b_normalize_multiday_aggtrades.py` | ~1,620 | 0 |
| `tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` | ~870 | 0 |
| `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_multi-day-normalization-implementation.md` | ~350 | 0 |
| `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_closeout.md` | ~250 | 0 |
| `docs/00-meta/current-project-state.md` | ~80 | 0 (narrow append + Current phase block update) |

No prior `src/prometheus/` module modified. No prior test modified. No prior `scripts/` script modified. No prior governance memo modified beyond the narrow `current-project-state.md` paragraph addition.

---

## 6. Result / verdict

- **Overall status:** `pass`
- **Produced file count:** 90 (matches expected)
- **Total event count:** 155,153,449 (matches expected; matches v002 raw manifest `total_row_count`)
- **Wall-clock seconds:** 1460.5 (~24.3 min)
- **Failed check id (if any):** none — all 65 criteria PASS (10 precondition + 1 per-day aggregate + 8 aggregate + 12 immutability + 6 governance + 8 quality-gate; NA classes covered the 20 conditional rows that did not apply on this run)

The orchestrator's 65-criterion strict-fail-closed validation contract is applied across 6 groups (precondition, per-day, aggregate, immutability, governance, quality-gate). Any single criterion failure aborts the run before the multi-day index manifest is written.

---

## 7. Local gitignored outputs evidence

| Path | SHA256 | Size (bytes) |
| ---- | ------ | ------------ |
| `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | 104,094 |
| `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256` | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | 118 |
| 90 per-day Parquet files | recorded in manifest's `per_file_inventory[i].parquet_sha256` | recorded in manifest's `per_file_inventory[i].parquet_size_bytes` |
| 90 paired sidecars | recorded in manifest's `per_file_inventory[i].sidecar_sha256` | recorded in manifest's `per_file_inventory[i].sidecar_size_bytes` |

---

## 8. Validation results

- `ruff check scripts/phase4bm_b_normalize_multiday_aggtrades.py tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` → PASS (`All checks passed!`)
- `mypy scripts/phase4bm_b_normalize_multiday_aggtrades.py` → PASS (`Success: no issues found`)
- `pytest tests/research/microstructure/test_phase4bm_b_multiday_normalization.py -q` → `33 passed`
- `pytest tests/research/microstructure/ -q` → `1156 passed, 1 skipped in 12.64s` (zero new test regressions; the 1 skip is the pre-existing labelled placeholder in `test_label_gate_report.py`)
- `git diff --check` → clean
- `git status --short` → only tracked Phase 4bm-B files + pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`)
- `git check-ignore -v data/microstructure/` → `.gitignore:85`
- `git check-ignore -v data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/` → covered by `.gitignore:85`
- `git check-ignore -v data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` → covered by `.gitignore:85`

---

## 9. Upstream immutability evidence (188 witnesses)

The orchestrator captures pre-run SHA256 for **188 immutability witnesses** before any output write and re-captures post-run SHA256 after all outputs are committed:

- 4 governance artefacts (v002 raw manifest, v002 acquisition log, Phase 4bl-D-R PASS gate report, Phase 4bl-E successor-state);
- 4 governance sidecars;
- 90 v002 raw zips;
- 90 v002 raw zip sidecars.

All 188 witnesses verified byte-identical pre/post. Drift fails closed (criteria 40-51).

The Phase 4bd v001 single-day parquet at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` was re-verified post-cleanup with recomputed SHA256 = `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` (matches recorded Phase 4bd value).

---

## 10. Manifest state preservation

- v002 raw manifest: `research_eligible=false`, `eligibility_gate_status=pending` (unchanged from Phase 4bl-C).
- Phase 4bd v001 derived manifest: `research_eligible=false`, `eligibility_gate_status=pending` (unchanged from Phase 4bd).
- Phase 4bh feature manifest: `research_eligible=false`, `eligibility_gate_status=pending` (unchanged).
- Phase 4bj-C label manifest: `research_eligible=false`, `eligibility_gate_status=pending`, `chronological_split_policy=not_yet_defined` (unchanged).
- **NEW** Phase 4bm-B v002 derived manifest: `research_eligible=false`, `eligibility_gate_status=pending` (locked at Stage-0).

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end. The new multi-day index manifest is a sibling shape and does NOT use the single-file `MicrostructureManifest` data class.

---

## 11. Boundary confirmations

All true at the close of Phase 4bm-B:

- no `data/microstructure/` commit;
- no modification of any prior `data/microstructure/` artefact other than the new v002 derived outputs;
- no source code / test / script change outside the two new files and the narrow `current-project-state.md` paragraph addition;
- no MCP / Graphify / `.mcp.json` / credentials / `.env`;
- no network I/O;
- no Binance / public / private endpoint contact;
- no WebSocket;
- no features / labels / signals / proxies / ML / strategy / backtests;
- no acquisition;
- no `research_eligible` flip;
- no `eligibility_gate_status` transition on any actual manifest;
- no `chronological_split_policy` change on any actual manifest;
- no retained verdict revision;
- no project lock change;
- no M0 amendment;
- no successor authorization;
- no merge into `main`;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).

---

## 12. Retained verdict ledger preserved verbatim

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec.

---

## 13. Preserved project locks (verbatim)

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant; Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule.

---

## 14. No-rescue constraints reaffirmed

No R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy hybrid is created, designed, named, or implied by Phase 4bm-B. No 5m research thread reopened. No retained verdict revised. No project lock changed. No M0 amendment.

---

## 15. Successor authorization

**None.** Phase 4bm-B does not authorize any successor phase. The conditional next-step ladder is operator-driven:

- merge Phase 4bm-B into `main` via a separately authorized merge phase (Tier 1) with merge-closeout per `docs/00-meta/process/merge-closeout-standard.md`;
- followed by operator discussion;
- followed conditionally by Phase 4bm-C (Multi-Day Normalized Structural QA Memo), Phase 4bm-D (Multi-Day Derived-Family Eligibility Gate), Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision Memo), and Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording) — none authorized by Phase 4bm-B.

**Phase 4 canonical / Phase 5 / paper / shadow / live-readiness / deployment / exchange-write / production keys / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials / any additional acquisition beyond the 90 locked BTCUSDT UTC dates** all remain unauthorized.

---

## 16. Recommended state

**Remain paused.**
