# Phase 4bm-C Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-C — Multi-Day Normalized Structural QA Memo
- **Tier**: Tier 1 (analysis-and-docs)
- **Type**: descriptive structural QA, read-only on data
- **Branch**: `phase-4bm-c/multi-day-normalized-structural-qa-memo`
- **Base**: `main` at `1613cf19de874293a545866000f1788e64e83cb3` (Phase 4bm-B merge-closeout commit)
- **Predecessor**: Phase 4bm-B (Multi-Day Normalization Implementation, project-complete on main)

## §2 Scope

Phase 4bm-C performed read-only inspection of the v002 derived family produced by Phase 4bm-B and emitted a structural QA verdict against the locked Phase 4bm-A design and the merged Phase 4bm-B implementation evidence.

The QA inspected:

- the v002 derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` (gitignored)
- the manifest sidecar
- all 90 per-file inventory entries
- all 90 derived Parquet files
- all 90 derived sidecars
- 4 governance witnesses (raw manifest, acquisition log, Phase 4bl-D-R gate report, Phase 4bl-E successor-state)
- 4 governance witness sidecars
- 90 raw zips
- 90 raw zip sidecars
- 1 Phase 4bd v001 single-day parquet (immutability witness)

Phase 4bm-C did not normalize, gate, transition, mutate, or authorize anything.

## §3 Verdict

**STRUCTURAL_QA_PASS.**

All 28 predeclared QA questions returned PASS. All 188 upstream immutability witnesses are byte-identical to recorded values. The v002 derived family is structurally well-formed.

The verdict is descriptive only. It does not transition the manifest, does not flip `research_eligible`, does not transition `eligibility_gate_status`, and does not authorize any successor.

## §4 Files Added (tracked, 2)

- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-c_multi-day-normalized-structural-qa-memo.md` (17-section structural QA memo)
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-c_closeout.md` (this file)

## §5 Files Modified Narrowly (tracked, 1)

- `docs/00-meta/current-project-state.md` — Phase 4bm-C narrative paragraph + new "Current phase:" block; prior Phase 4bm-B "Current phase:" block preserved as historical context.

## §6 Files NOT Modified

- `src/prometheus/` — no source file modified.
- `tests/` — no test file modified.
- `scripts/` — no script modified.
- `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP files — unchanged.
- Every prior `data/microstructure/` artefact (90 raw zips, raw manifest, 90 raw zip sidecars, acquisition log, Phase 4bd v001 derived parquet, Phase 4bd derived manifest, Phase 4bf gate report, Phase 4bg-B successor-state, Phase 4bh feature parquet, Phase 4bh feature manifest, Phase 4bj-C label parquet, Phase 4bj-C label manifest, every prior gate report and successor-state artefact, Phase 4bm-B v002 manifest, Phase 4bm-B 90 v002 parquets, Phase 4bm-B 90 v002 sidecars) — byte-identical pre/post Phase 4bm-C.
- Every prior phase implementation report and merge-closeout.

## §7 QA Findings Summary

| Area | Result |
|---|---|
| Manifest envelope (24 scalar fields + governance_labels) | PASS |
| Manifest sidecar canonical Phase 4bb-F format | PASS |
| per_file_inventory: 90 entries, contiguous UTC dates 2024-12-01..2025-02-28 | PASS |
| All 90 parquet paths exist on disk | PASS |
| All 90 sidecar paths exist on disk | PASS |
| All 90 parquet SHA256 match inventory | PASS |
| All 90 parquet sizes match inventory | PASS |
| All 90 sidecar SHA256 match inventory | PASS |
| All 90 sidecars canonical Phase 4bb-F format | PASS |
| Parquet schema = 19 columns in NORMALIZED_SCHEMA_V001 order (sample dates) | PASS |
| Parquet dtypes match locked policy (sample dates) | PASS |
| Row counts match manifest event_count (sample dates) | PASS |
| `row_index` is exactly `0..n-1` per file (sample dates) | PASS |
| `agg_trade_id` non-decreasing within file (sample dates) | PASS |
| `transact_time_ms` non-decreasing within file (sample dates) | PASS |
| All `transact_time_ms` within `[UTC date, UTC date + 1)` (sample dates) | PASS |
| Lineage columns constant per file (sample dates) | PASS |
| `price` / `quantity` Decimal-as-string positive (sample dates) | PASS |
| `is_buyer_maker` strict bool (sample dates) | PASS |
| `first_trade_id <= last_trade_id` per row (sample dates) | PASS |
| Adjacent-date temporal monotonicity (89 pairs) | PASS |
| Adjacent-date agg_trade_id non-overlap and continuity (89 pairs) | PASS |
| Per-file agg_trade_id density (90 files) | PASS |
| Total event count = 155,153,449 | PASS |
| Total parquet size = 1.40 GiB | PASS |
| Upstream governance witnesses (4 + 4 sidecars) immutable | PASS |
| 90 raw zips immutable | PASS |
| 90 raw zip sidecars immutable (canonical format) | PASS |
| Phase 4bd v001 single-day parquet immutable | PASS |
| Manifest `research_eligible=false` / `eligibility_gate_status="pending"` preserved | PASS |

Combined: **28/28 QA questions PASS**, **188 upstream witnesses immutable**, **9,718,154 rows row-level inspected** (6.26% of total event count).

## §8 Validation

- `git status` — clean working tree (only the tracked Phase 4bm-C files plus the pre-existing untracked `.claude/scheduled_tasks.lock` and `data/research/` entries; no `data/microstructure/` files staged).
- `git diff --check` — clean.
- `git check-ignore -v data/microstructure/` — `.gitignore:85`.
- `git check-ignore -v data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/` — covered by `.gitignore:85`.

Whole-repo `ruff` / `mypy` / `pytest` were NOT rerun by Phase 4bm-C (no source / test / script / configuration file was modified). The latest authoritative whole-repo validation remains the Phase 4bm-B merge baseline (`ruff` PASS, `mypy` PASS, `pytest tests/research/microstructure/` 1156 passed + 1 skipped, no new regressions).

## §9 Non-Authorizations

Phase 4bm-C does NOT authorize:

- Phase 4bm-C merge phase
- Phase 4bm-D (Multi-Day Derived-Family Eligibility Gate)
- Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision)
- Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording)
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*
- Phase 5 / Phase 4 canonical
- Paper / shadow / live-readiness / deployment / exchange-write
- Production-key creation / authenticated APIs / private endpoints
- User stream / live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials
- Acquisition beyond the 90 locked BTCUSDT UTC dates
- Any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual manifest

## §10 Retained Verdicts and Project Locks (Preserved Verbatim)

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec; §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked); Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked — forward writes use canonical LF natively); Phase 4am .. Phase 4bm-B results — all preserved verbatim.

## §11 Lifecycle Status

Phase 4bm-C is **branch-complete only**.

Per the Phase 4bk-A workflow standard, Phase 4bm-C is **not project-complete** until a separately authorized merge phase records its merge-closeout on `main`.

## §12 Recommended State

**Remain paused.**

Conditional next, NOT authorized:

- Future operator-authorized Phase 4bm-C merge phase that merges this branch into `main` and records a Phase 4bm-C merge-closeout per `docs/00-meta/process/merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

After merge, the recommended state remains **remain paused** pending operator decision on the conditional Phase 4bm-D ladder (Multi-Day Derived-Family Eligibility Gate → Phase 4bm-E research-eligibility decision → Phase 4bm-F successor-state).

— end of Phase 4bm-C closeout —
