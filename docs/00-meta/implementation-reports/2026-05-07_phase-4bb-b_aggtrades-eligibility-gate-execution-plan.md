# Phase 4bb-B — AggTrades Eligibility-Gate Execution-Plan Memo

**Type:** docs-only eligibility-gate execution-plan memo.
**Status:** drafted on branch `phase-4bb-b/aggtrades-eligibility-gate-execution-plan`; pending operator review.
**Date:** 2026-05-07.

---

## 1. Phase header

Phase 4bb-B is a docs-only execution-plan memo for a future offline aggTrades eligibility-gate primitive (Phase 4bb-C, **not authorized** by this memo). It translates Phase 4ba's staged eligibility model + 45-check eligibility-time gate + fail-closed rules, plus Phase 4bb-A's 13 implementation-planning observations, plus the existing Phase 4aw scaffold (`MicrostructureManifest`, `InvalidWindow`, `RawWriter`, `EligibilityGateStatus`, `MicrostructureConfig`, `ALLOWLIST_PATTERNS` / `DENYLIST_TOKENS`) and Phase 4ax aggTrades skeleton (`validate_aggtrade_payload`, `assert_aggtrades_endpoint_allowed`, `TakerSide`, `AggTradeValidationError`) into a precise, file-by-file, function-by-function implementation plan.

Phase 4bb-B is **planning only**. It does **not** implement code, does **not** run the gate as a new tool, does **not** modify data or manifests, does **not** flip any eligibility flag, does **not** authorize Phase 4bb-C, and does **not** authorize any other successor.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Branch | `phase-4bb-b/aggtrades-eligibility-gate-execution-plan` |
| Base SHA (`main`) | `32a41ddc39b7f0fae33de0f6d59d27eed65d2f11` |
| Base parent | `docs(phase-4bb-a): add merge closeout` |
| Type | docs-only |
| Touches source / tests / scripts? | **No** |
| Touches data / manifests? | **No** |
| Touches `data/microstructure/`? | **No** (`.gitignore:85` continues to apply) |
| Touches retained verdicts / locks / M0? | **No** |
| Authorizes any successor? | **No** |
| Acquires data / calls endpoints / opens WebSockets / uses credentials? | **No** |

---

## 3. Inputs reviewed

Static repo inspection only. Phase 4bb-B did not run the gate, did not run scripts, did not run tests, did not download anything, and did not modify any file under `data/microstructure/`. The following committed sources were read:

- The Phase 4ba memo (`docs/00-meta/implementation-reports/2026-05-07_phase-4ba_aggtrades-dataset-eligibility-gate-review.md`), §9 (staged five-stage ladder), §10.1–§10.12 (45-check enumeration), §11 (manifest-field contract), §12 (invalid-window taxonomy), §13 (dataset-versioning policy), §14 (downstream-use permissions), §15 (six-category fail-closed rules + cross-cutting rules), §16 (recommended future phase options).
- The Phase 4ba closeout.
- The Phase 4bb-A memo (`docs/00-meta/implementation-reports/2026-05-07_phase-4bb-a_aggtrades-structural-data-quality-interpretation.md`), §15 (13 implementation-planning observations) and §6 / §7 / §8 / §9 / §10 / §11 / §12 (structural QA result; 21/21 PASS).
- The Phase 4bb-A closeout and merge-closeout.
- The Phase 4aw scaffold modules: `src/prometheus/research/microstructure/__init__.py`, `config.py`, `allowlist.py`, `invalid_window.py`, `manifest.py`, `raw_writer.py` — including `MicrostructureManifest` (`research_eligible: bool = False`, `eligibility_gate_status: EligibilityGateStatus = EligibilityGateStatus.PENDING`, `flip_research_eligible(...)` always raises), `EligibilityGateStatus` (`PENDING` / `PASS` / `FAIL`), `InvalidWindowReason` (17 values), `InvalidWindowSeverity` (3 values), `DownstreamEligibilityAction` (3 values), `MicrostructureConfig.symbol_allowlist` defaulting to `("BTCUSDT", "ETHUSDT")`, `ALLOWLIST_PATTERNS` and `DENYLIST_TOKENS` with denylist dominance.
- The Phase 4ax aggTrades skeleton: `src/prometheus/research/microstructure/aggtrades.py` — `validate_aggtrade_payload`, `AggTradeValidationError`, `assert_aggtrades_endpoint_allowed`, `TakerSide`.
- The Phase 4az acquisition memo (especially §11–§13) and the on-disk Phase 4az manifest under `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (read-only, not modified).
- `pyproject.toml` (ruff line-length 100; py311; mypy strict on `src/prometheus`; pytest pythonpath `["src", "."]`).
- `.gitignore` (line 85: `data/microstructure/`).
- The Phase 4ak M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md`).
- The retained-verdict ledger and project locks (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11).

---

## 4. Scope

Phase 4bb-B is **docs-only**. The allowed activities are:

- Static repository inspection.
- Reasoning derived from the Phase 4ba memo, the Phase 4bb-A memo, the Phase 4aw scaffold, and the Phase 4ax aggTrades skeleton.
- Authoring this memo and the Phase 4bb-B closeout under `docs/00-meta/implementation-reports/`.
- A narrow `docs/00-meta/current-project-state.md` update (Phase 4bb-B narrative paragraph + new "Current phase:" block; prior Phase 4bb-A block preserved as historical context).

---

## 5. Non-scope

The following are **forbidden** and **not performed** in Phase 4bb-B:

- Implement code, write source files under `src/prometheus/`, write tests under `tests/`, or write scripts under `scripts/`.
- Run any gate as a new tool.
- Modify any data, manifest, sidecar, acquisition log, or `data/microstructure/` entry.
- Flip `research_eligible` or transition `eligibility_gate_status` out of `pending`.
- Compute features, descriptive trading statistics, returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread / depth / liquidity / slippage / order-flow / execution-quality proxies.
- Normalize the dataset (no JSONL, no Parquet, no DuckDB, no derived dataset).
- Train ML, create labels, create a strategy, or run backtests.
- Acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request or use credentials.
- Create `.env`, `.mcp.json`, MCP, or Graphify.
- Modify any source / test / script / config / `README.md` / `pyproject.toml` / `.gitignore` / runtime configuration.
- Modify any strategy / validation / governance doc beyond the allowed Phase 4bb-B files.
- Revise retained verdicts, change project locks, amend M0.
- Authorize Phase 4bb-C, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, or production keys.

---

## 6. Planning assumptions

Phase 4bb-B's plan is grounded in the following assumptions, all of which are required to remain true at the time Phase 4bb-C (if ever authorized) runs:

1. The Phase 4aw scaffold is the single source of truth for the manifest data model, the invalid-window taxonomy, the allowlist / denylist, the `EligibilityGateStatus` enum, and the `RawWriter` primitive. Phase 4bb-C does **not** modify these; it composes them.
2. The Phase 4ax `validate_aggtrade_payload` is the single source of truth for per-row aggTrades validation. Phase 4bb-C does **not** modify it; it imports and re-applies it.
3. The Phase 4ba §10 forty-five-check enumeration is the binding contract. Phase 4bb-C may not skip a check, may not weaken a check, and may not silently relax a check.
4. The Phase 4ba §15 fail-closed rules (six categories: unknown, mixed, stale, partial, ambiguous, cross-cutting) are binding.
5. The Phase 4ba §9 staged eligibility ladder is binding: `research_eligible=true` is reserved for Stage 3 (normalized derived family). For raw families, Phase 4bb-C may at most transition `eligibility_gate_status` from `pending` to `pass` or `fail`, but **never** flip `research_eligible` to `true`.
6. The Phase 4az archive's `governance_labels` shape is the canonical raw-family shape (`feature_computation: forbidden`, `strategy_use: forbidden`, `phase`, `source_phase_boundary`, `validator`, `stop_trigger_domain`, `symbol_scope_source`).
7. `data/microstructure/` remains gitignored at `.gitignore:85`. Phase 4bb-C must not commit any output under this subtree.
8. Phase 4bb-C is offline. The whole test suite must remain runnable with no network access.
9. The Phase 4bb-A 13 application-time observations apply.

---

## 7. Future Phase 4bb-C implementation goal

Phase 4bb-C, if ever authorized, must implement an **offline-only** primitive that:

- Accepts a `(dataset_family, version, symbol)` triple plus paths (or, equivalently, a manifest path) and locates the raw `.zip`, paired `.sha256` sidecar, and acquisition log under `data/microstructure/`.
- Reads each of those four artefacts read-only.
- Re-applies all 45 Phase 4ba §10 checks against the on-disk artefacts plus the manifest's declarative content.
- Records the result of each check as `PASS` / `FAIL` / `NOT_APPLICABLE` / `ERROR` with structured evidence.
- Records candidate invalid-window observations as `InvalidWindowCandidate` records (not directly mutating the manifest's `invalid_windows`).
- Writes a single gate report under `data/microstructure/gate-reports/<dataset_family>__<version>__<report_id>.json`. The output path is **gitignored** because it falls under `data/microstructure/`.
- Recommends a successor `eligibility_gate_status` (PASS or FAIL) for raw families, but only writes a successor manifest if Phase 4bb-C's authorization brief explicitly permits it. By default Phase 4bb-C **does not** mutate the original manifest.
- Always sets `research_eligible_after = false` for raw families. Even on overall PASS, the gate cannot promote a raw family to `research_eligible=true`. Promotion to `research_eligible=true` is reserved for a separately authorized normalization phase (Phase 4ba §9.2 Stage 3).
- Performs no network I/O, no credential read, no MCP / Graphify integration, no `.env` reads, no external tool spawning beyond stdlib.

---

## 8. Proposed package / file layout

All paths are **proposed** for Phase 4bb-C. Phase 4bb-B does **not** create any of them. None of these paths exists today.

### 8.1 Source modules (under `src/prometheus/research/microstructure/`)

```
src/prometheus/research/microstructure/
├── eligibility_gate.py            (NEW; gate orchestrator + value objects)
├── eligibility_checks.py          (NEW; 45 individual check functions, grouped 10.1..10.12)
├── eligibility_report.py          (NEW; AggTradesGateReport data model + JSON serialisation)
├── eligibility_io.py              (NEW; read-only artefact readers + path resolvers)
├── manifest.py                    (UNCHANGED; provides MicrostructureManifest, EligibilityGateStatus)
├── invalid_window.py              (UNCHANGED; provides InvalidWindowReason / Severity / Action / InvalidWindow)
├── allowlist.py                   (UNCHANGED; provides ALLOWLIST_PATTERNS / DENYLIST_TOKENS)
├── config.py                      (UNCHANGED; provides MicrostructureConfig, validate_config, EligibilityGateThresholds)
├── aggtrades.py                   (UNCHANGED; provides validate_aggtrade_payload, AggTradeValidationError, TakerSide)
├── raw_writer.py                  (UNCHANGED; provides RawWriter for any future report-write primitive)
└── __init__.py                    (NARROW UPDATE; re-export new public symbols only)
```

### 8.2 Tests (under `tests/research/microstructure/`)

```
tests/research/microstructure/
├── test_eligibility_gate.py       (NEW; orchestrator-level tests; 30+ tests; all offline; pytest tmp_path)
├── test_eligibility_checks.py     (NEW; per-check tests; 45+ tests; all offline; pytest tmp_path)
├── test_eligibility_report.py     (NEW; report serialisation tests; round-trip)
├── test_eligibility_io.py         (NEW; read-only artefact reader tests; tmp_path fixtures)
├── test_eligibility_no_network.py (NEW; URL allowlist guard / no-network guard)
├── test_aggtrades.py              (UNCHANGED beyond Phase 4ax / 4az narrow update)
├── test_phase4az_archive_acquisition.py (UNCHANGED)
├── test_config.py / test_allowlist.py / test_invalid_window.py / test_manifest.py / test_raw_writer.py / test_import_boundaries.py (UNCHANGED)
```

### 8.3 No new script, no CLI surface

Phase 4bb-C does **not** add any `scripts/...` entrypoint. The gate primitive is a Python module callable via `python -c "from prometheus.research.microstructure.eligibility_gate import run_eligibility_gate; ..."` or via direct import in a future tool. A CLI wrapper is **deferred** to a separately authorized future phase. Reasons:

- No CLI = no accidental shell-time mutation of `data/microstructure/`.
- No CLI = no `--output-root` / `--allow-network` / `--force` flag surface to misuse.
- The Phase 4az acquisition path already has a one-shot CLI (`scripts/phase4az_...`); the eligibility-gate primitive is conceptually a library-style read-only verifier and does not need CLI parity.

### 8.4 No new docs files beyond the report under gate-reports/

The gate primitive does not produce any new tracked Markdown. Its only output is a JSON gate report under `data/microstructure/gate-reports/...`, which is gitignored.

### 8.5 No `.gitignore` change

The existing `.gitignore:85` line `data/microstructure/` already covers `data/microstructure/gate-reports/`. Phase 4bb-C does not modify `.gitignore`.

### 8.6 No `pyproject.toml` change

No new runtime dependency is required. The gate uses stdlib only (`hashlib`, `zipfile`, `csv`, `json`, `pathlib`, `dataclasses`, `enum`, `collections.abc`, `typing`) plus the existing Phase 4aw / Phase 4ax modules. No `pyarrow`, `numpy`, `pandas`, `httpx`, `requests`, or any other external dependency is added.

---

## 9. Proposed CLI / invocation model

Phase 4bb-C does **not** add a CLI script. Invocation model:

```python
from pathlib import Path
from prometheus.research.microstructure.eligibility_gate import (
    AggTradesEligibilityGateInput,
    AggTradesEligibilityGateResult,
    run_eligibility_gate,
)

inp = AggTradesEligibilityGateInput(
    manifest_path=Path("data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json"),
    output_root=Path("data/microstructure/gate-reports"),
    code_commit_sha="<deterministic short sha>",
    write_report=True,           # default True
    write_successor_manifest=False,  # default False; Phase 4bb-C must not flip status without authorization
)
result: AggTradesEligibilityGateResult = run_eligibility_gate(inp)
```

The orchestrator returns an in-memory `AggTradesEligibilityGateResult` and (optionally) writes a JSON gate report. It does **not** mutate the original manifest under any default invocation. A `write_successor_manifest=True` mode is reserved for a later separately-authorized phase and must remain a no-op (or raise) in Phase 4bb-C unless the Phase 4bb-C authorization brief explicitly enables it.

---

## 10. Proposed value objects and enums

All of the following are **proposed**. Phase 4bb-B does not create them.

### 10.1 `AggTradesEligibilityGateInput` (frozen dataclass)

```python
@dataclass(frozen=True)
class AggTradesEligibilityGateInput:
    manifest_path: Path                  # required; resolved read-only
    output_root: Path                    # required; must be under data/microstructure/
    code_commit_sha: str                 # required; gate run identity
    write_report: bool = True            # default True; if False, no JSON write
    write_successor_manifest: bool = False  # MUST stay False in Phase 4bb-C unless brief enables
    explicit_extra_symbols: tuple[str, ...] = ()
    config: MicrostructureConfig | None = None  # if None, default config is used
```

Construction is fail-closed: `manifest_path` must exist; `output_root` must resolve under `data/microstructure/` (mirrors `RawWriter` discipline); `code_commit_sha` must be a non-empty short / long hex; explicit non-allowlisted symbols must be admitted only via `explicit_extra_symbols`.

### 10.2 `AggTradesEligibilityCheckResult` (frozen dataclass)

```python
@dataclass(frozen=True)
class AggTradesEligibilityCheckResult:
    check_id: str                        # e.g. "10.6.21" — group.subsection.check
    group: str                           # one of "source"/"checksum"/"manifest"/...
    title: str                           # short human title from Phase 4ba §10
    status: AggTradesEligibilityCheckStatus  # PASS / FAIL / NOT_APPLICABLE / ERROR
    detail: str                          # short structured one-line detail
    evidence: Mapping[str, object]       # structured key/value evidence
```

### 10.3 `AggTradesEligibilityCheckStatus` (StrEnum)

```python
class AggTradesEligibilityCheckStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"
```

`PASS` = the check was applicable and passed. `FAIL` = the check was applicable and failed; gate-level status will be FAIL. `NOT_APPLICABLE` = the check is structurally not relevant for this dataset family / acquisition mode; does not affect gate-level status. `ERROR` = the gate could not evaluate the check (e.g. file missing, unreadable); treated as fail-closed (gate-level FAIL).

### 10.4 `InvalidWindowCandidate` (frozen dataclass)

```python
@dataclass(frozen=True)
class InvalidWindowCandidate:
    reason: InvalidWindowReason          # Phase 4aw enum
    severity: InvalidWindowSeverity      # Phase 4aw enum
    downstream_eligibility_action: DownstreamEligibilityAction  # Phase 4aw enum
    start_time_ms: int
    end_time_ms: int
    family: str
    symbol: str
    evidence: Mapping[str, object]
    discovered_by_check_id: str          # e.g. "10.6.21"
```

A candidate is **not** appended to the original manifest by Phase 4bb-C. Candidates are recorded only inside the gate report.

### 10.5 `AggTradesEligibilityGateResult` (frozen dataclass)

```python
@dataclass(frozen=True)
class AggTradesEligibilityGateResult:
    overall_status: AggTradesEligibilityCheckStatus   # PASS / FAIL / ERROR; never NOT_APPLICABLE
    research_eligible_after: bool                     # ALWAYS False for raw aggTrades families
    eligibility_gate_status_after: EligibilityGateStatus  # recommendation only; not written by default
    checks: tuple[AggTradesEligibilityCheckResult, ...]  # exactly 45 entries
    invalid_window_candidates: tuple[InvalidWindowCandidate, ...]
    measured_summary: Mapping[str, object]            # row count, SHA, first/last T, etc.
    boundary_confirmations: Mapping[str, bool]        # see §16
    no_successor_authorization: bool                  # ALWAYS True; gate cannot authorize Phase 4bb-* / Phase 5 / paper / live
    report_path: Path | None                          # populated iff write_report=True succeeded
```

### 10.6 `AggTradesGateReport` (frozen dataclass; JSON-serialisable)

```python
@dataclass(frozen=True)
class AggTradesGateReport:
    report_id: str                       # deterministic; e.g. f"{dataset_family}__{version}__{utc_ms}__{short_sha}"
    dataset_family: str
    version: str
    symbol: str
    source_manifest_path: str
    raw_zip_path: str
    sidecar_path: str
    acquisition_log_path: str
    created_at_utc_ms: int
    code_commit_sha: str
    overall_status: str                  # PASS / FAIL / ERROR
    research_eligible_after: bool        # always False for raw families
    eligibility_gate_status_after: str   # recommended successor status
    checks: list[dict[str, object]]      # serialised AggTradesEligibilityCheckResult
    invalid_window_candidates: list[dict[str, object]]
    measured_summary: dict[str, object]
    boundary_confirmations: dict[str, bool]
    no_successor_authorization: bool     # always True
```

The report is JSON-serialised via `json.dumps(..., indent=2, sort_keys=True)` and written via the Phase 4aw `RawWriter` discipline (atomic temp + rename + paired SHA256 sidecar) under `data/microstructure/gate-reports/`.

---

## 11. Proposed gate execution flow

The orchestrator function `run_eligibility_gate(inp: AggTradesEligibilityGateInput) -> AggTradesEligibilityGateResult` executes the 45 checks in a fixed order inside one read-only pass:

1. **Construct read context.** Load the manifest from `inp.manifest_path` via `MicrostructureManifest.load(...)`. Resolve the raw zip / sidecar / acquisition-log paths (Phase 4bb-A confirmed all four artefacts exist for the Phase 4az dataset). Refuse to proceed if any path is outside `data/microstructure/`.
2. **Group 1 — source checks (10.1.1–10.1.5).** Pure declarative checks against the manifest fields. No file I/O.
3. **Group 2 — checksum checks (10.2.6–10.2.8).** Stream the raw `.zip` through `hashlib.sha256` once. Compare to manifest `files[0].sha256` and to the on-disk `.sha256` sidecar text (parsed first 64 hex characters). Verify presence-or-explicit-absence-recorded for `.CHECKSUM` companion governance.
4. **Group 3 — manifest checks (10.3.9–10.3.13).** Pure declarative. Verify required-field non-emptiness, current `research_eligible=false` and `eligibility_gate_status=pending`, `governance_labels` minimum keys, `code_commit_sha` exists in repo history (best-effort `git cat-file -e`; ERROR not FAIL on git unavailable), `capture_config_hash` is non-empty.
5. **Group 4 — schema checks (10.4.14–10.4.16).** Open the ZIP read-only via `zipfile`. Decompress in memory. Header-detection heuristic per Phase 4bb-A §15 item 1 (numeric first cell ⇒ headerless; Phase 4az is headered). Iterate rows once: re-apply Phase 4ax `validate_aggtrade_payload` per row; record column order in `measured_summary["csv_column_order"]`; flag any unexpected extra column not in the documented schema.
6. **Group 5 — timestamp checks (10.5.17–10.5.20).** Same single pass: confirm every `T` is `int` ms; `start_time_ms ≤ end_time_ms`; `T` non-decreasing across the file (record `OUT_OF_ORDER_EVENT` candidates if violated and FAIL); UTC-day match against the archive-path-encoded date (half-open at next-day midnight per Phase 4bb-A §15 item 7).
7. **Group 6 — aggregate-trade-ID monotonicity (10.6.21–10.6.23).** Same single pass: `a` non-decreasing; non-negative increments; no `a` reappears with different `(p, q, m, T)` tuple.
8. **Group 7 — duplicate checks (10.7.24–10.7.25).** Same single pass: no duplicate `a`; `f ≤ l` for every row.
9. **Group 8 — row count checks (10.8.26–10.8.28).** Cross-check the in-pass row count against `manifest.event_count` and `sum(files[*].event_count)`.
10. **Group 9 — symbol / date checks (10.9.29–10.9.32).** Verify symbol allowlist (default `("BTCUSDT", "ETHUSDT")` from `MicrostructureConfig`; unknown symbol via `explicit_extra_symbols`); `symbol_scope_source` recorded; archive-path-encoded date matches all `T` values; retention window per separately authorized retention-governance memo (default fail-closed when retention is unknown).
11. **Group 10 — archive integrity (10.10.33–10.10.36).** Single CSV member; clean decompression; size > 0 and ≤ predeclared upper bound (5 GiB per Phase 4ay §10 / Phase 4ba §10.10); raw byte count matches on-disk file size.
12. **Group 11 — invalid-window checks (10.11.37–10.11.40).** Round-trip every `manifest.invalid_windows` entry through `InvalidWindow.from_dict / to_dict`; verify `evidence` non-empty; verify severity / action consistency (`ERROR` ⇒ `EXCLUDE` or `PROXY_ONLY`; `INFO` + `EXCLUDE` rejected); verify no per-row failure discovered in steps 5–7 lacks a corresponding manifest `InvalidWindow`.
13. **Group 12 — cross-cutting (10.12.41–10.12.45).** `governance_labels.feature_computation` is `forbidden`; `governance_labels.strategy_use` is `forbidden`; `governance_labels.stop_trigger_domain` is from the Phase 3v §8 enum; no private-endpoint or credential-shaped string anywhere in the manifest or acquisition log (re-uses Phase 4aw `DENYLIST_TOKENS`); acquisition log present and self-consistent (matches `start_time_ms` / `end_time_ms` / `event_count` / `code_commit_sha`).
14. **Aggregate.** `overall_status = PASS` iff all 45 checks are `PASS` or `NOT_APPLICABLE`; `FAIL` iff any check is `FAIL`; `ERROR` iff any check is `ERROR` and no FAIL is present.
15. **Successor recommendation.** `research_eligible_after = False` always. `eligibility_gate_status_after = PASS` iff `overall_status == PASS`, else `FAIL` (or `PENDING` if unrecoverable error and operator review is needed).
16. **Write report.** If `inp.write_report` and the ancestor directory is under `data/microstructure/`, serialise an `AggTradesGateReport` to JSON via the `RawWriter` atomic-temp-rename pattern + paired `.sha256`.
17. **Return** the in-memory `AggTradesEligibilityGateResult`.

The orchestrator does **not** mutate the original manifest under any default invocation. Successor-manifest writing is reserved for a separately authorized future phase.

---

## 12. Mapping from Phase 4ba 45 checks to future functions

Each check is a pure function in `eligibility_checks.py`. The proposed function names and the Phase 4ba §10 check-number they implement are:

| Group | Phase 4ba check # | Proposed function (in `eligibility_checks.py`) |
| ----- | ----------------- | ----------------------------------------------- |
| Source (10.1) | 1 | `check_source_label_whitelisted` |
|  | 2 | `check_endpoint_label_documented_archive_family` |
|  | 3 | `check_endpoint_docs_reference_present` |
|  | 4 | `check_no_private_endpoint_label` |
|  | 5 | `check_capture_mode_is_historical_archive` |
| Checksum (10.2) | 6 | `check_files_sha256_is_64char_lowercase_hex` |
|  | 7 | `check_recomputed_sha_matches_manifest_and_sidecar` |
|  | 8 | `check_checksum_companion_verification_recorded` |
| Manifest (10.3) | 9 | `check_required_manifest_fields_populated` |
|  | 10 | `check_research_eligible_false_and_status_pending` |
|  | 11 | `check_governance_labels_minimum_keys` |
|  | 12 | `check_code_commit_sha_exists_in_repo_history` |
|  | 13 | `check_capture_config_hash_nonempty_and_redrivable` |
| Schema (10.4) | 14 | `check_every_row_passes_validate_aggtrade_payload` |
|  | 15 | `check_column_order_recorded` |
|  | 16 | `check_no_unexpected_extra_columns` |
| Timestamps (10.5) | 17 | `check_all_T_are_int_ms_within_manifest_range` |
|  | 18 | `check_start_time_ms_le_end_time_ms` |
|  | 19 | `check_T_non_decreasing_across_file` |
|  | 20 | `check_utc_day_match` |
| Monotonicity (10.6) | 21 | `check_a_non_decreasing_across_file` |
|  | 22 | `check_a_increments_non_negative` |
|  | 23 | `check_no_a_value_reappears_with_different_tuple` |
| Duplicates (10.7) | 24 | `check_no_duplicate_a_within_file` |
|  | 25 | `check_f_le_l_for_every_row` |
| Row count (10.8) | 26 | `check_event_count_gt_zero` |
|  | 27 | `check_event_count_matches_actual_row_count` |
|  | 28 | `check_event_count_consistent_with_files_sum` |
| Symbol / date (10.9) | 29 | `check_symbol_in_project_allowlist` |
|  | 30 | `check_symbol_scope_source_recorded_and_path_match` |
|  | 31 | `check_archive_path_date_matches_T_values` |
|  | 32 | `check_date_within_retention_window_or_fail_closed` |
| Archive integrity (10.10) | 33 | `check_zip_single_csv_member` |
|  | 34 | `check_zip_decompresses_cleanly` |
|  | 35 | `check_file_size_within_bounds` |
|  | 36 | `check_archive_byte_count_matches_on_disk` |
| Invalid windows (10.11) | 37 | `check_invalid_windows_parseable_round_trip` |
|  | 38 | `check_every_invalid_window_has_evidence` |
|  | 39 | `check_invalid_window_severity_action_consistency` |
|  | 40 | `check_no_silent_omission_of_per_row_failures` |
| Cross-cutting (10.12) | 41 | `check_feature_computation_forbidden_on_raw_family` |
|  | 42 | `check_strategy_use_forbidden_on_raw_family` |
|  | 43 | `check_stop_trigger_domain_in_phase3v8_enum` |
|  | 44 | `check_no_private_endpoint_or_credential_shaped_strings` |
|  | 45 | `check_acquisition_log_present_and_self_consistent` |

Each function returns an `AggTradesEligibilityCheckResult`. The orchestrator in `eligibility_gate.py` calls them in this exact order and aggregates. Functions that need to share streamed bytes (e.g. checks 6 / 7 / 14 / 17 / 19 / 20 / 21 / 22 / 23 / 24 / 25 / 27 / 31 / 33 / 34 / 36 / 40) operate against a shared single-pass row iterator constructed by `eligibility_io.py` so the file is decompressed and SHA-hashed exactly once.

---

## 13. Gate-report schema

The JSON-serialisable schema for `data/microstructure/gate-reports/<dataset_family>__<version>__<report_id>.json`:

```json
{
  "report_id": "microstructure_raw_aggtrades_v001__v001__1736985600000__32a41dd",
  "dataset_family": "microstructure_raw_aggtrades_v001",
  "version": "v001",
  "symbol": "BTCUSDT",
  "source_manifest_path": "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json",
  "raw_zip_path": "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip",
  "sidecar_path": "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256",
  "acquisition_log_path": "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json",
  "created_at_utc_ms": 1736985600000,
  "code_commit_sha": "<deterministic short or long sha>",
  "overall_status": "pass",
  "research_eligible_after": false,
  "eligibility_gate_status_after": "pass",
  "checks": [
    {
      "check_id": "10.1.1",
      "group": "source",
      "title": "Source label whitelisted",
      "status": "pass",
      "detail": "source = 'binance_data_archive'",
      "evidence": {"observed": "binance_data_archive", "allowed": ["binance_data_archive"]}
    }
    /* ... 44 more entries ... */
  ],
  "invalid_window_candidates": [],
  "measured_summary": {
    "recomputed_sha256": "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e",
    "row_count": 1681098,
    "first_T_ms": 1736899205109,
    "last_T_ms": 1736985599991,
    "min_a": 2516301323,
    "max_a": 2517982420,
    "duplicate_a_count": 0,
    "out_of_order_a_count": 0,
    "largest_consecutive_a_gap": 1,
    "m_true_count": 840378,
    "m_false_count": 840720,
    "csv_column_order": ["agg_trade_id", "price", "quantity", "first_trade_id", "last_trade_id", "transact_time", "is_buyer_maker"],
    "raw_byte_count": 21271119,
    "csv_uncompressed_size": 111698506
  },
  "boundary_confirmations": {
    "no_network_io": true,
    "no_credential_read": true,
    "no_env_read": true,
    "no_websocket": true,
    "no_mcp_or_graphify": true,
    "no_normalization_written": true,
    "no_feature_computed": true,
    "no_strategy_created": true,
    "no_ml_trained": true,
    "no_backtest_run": true,
    "no_manifest_mutation": true,
    "no_data_microstructure_write_outside_gate_reports": true,
    "research_eligible_after_is_false_for_raw_family": true
  },
  "no_successor_authorization": true
}
```

Schema rules:

- `overall_status` is one of `pass` / `fail` / `error`.
- `research_eligible_after` is `false` for all raw aggTrades families. There is no Phase 4bb-C input or branch that produces `true` here.
- `eligibility_gate_status_after` is `pass` / `fail` / `pending` (the latter only on `error`).
- `checks` always has exactly 45 entries even when some are `not_applicable`.
- `invalid_window_candidates` is `[]` when no candidate is recorded; entries match the `InvalidWindowCandidate` shape (§10.4) but are JSON-serialised.
- `measured_summary` carries the structural-QA-shape numbers from the single-pass row iterator. The `m_true_count` / `m_false_count` / `largest_consecutive_a_gap` keys are reported as structural shape only and are **not** features.
- `boundary_confirmations` is a fixed-key dict; every key must be `true` for `overall_status = pass`.
- `no_successor_authorization` is always `true`.

The report is paired with a `<report>.json.sha256` sidecar file written via the same `RawWriter` discipline, for the same audit reasons that apply to the Phase 4az raw archive.

---

## 14. Invalid-window handling plan

- Phase 4bb-C **must not** mutate `manifest.invalid_windows`. The original manifest is read-only.
- Per-row anomalies discovered during the gate run (e.g. an `OUT_OF_ORDER_EVENT` not previously recorded) are surfaced as `InvalidWindowCandidate` entries inside the gate report. They are **candidates**, not authorised invalid windows; promoting a candidate into a manifest requires a separately authorized phase that explicitly enables successor-manifest writing.
- The seventeen Phase 4aw `InvalidWindowReason` values cover every per-row anomaly the gate is expected to detect on raw archive aggTrades: `MISSING_SEQUENCE`, `OUT_OF_ORDER_EVENT`, `DUPLICATE_EVENT`, `GAP_AFTER_RECONNECT` (n/a archive), `SNAPSHOT_MISMATCH` (n/a archive), `CLOCK_SKEW` (n/a archive), `SYMBOL_MISMATCH`, `STALE_STREAM` / `STALE_BOOK` (n/a archive), `IMPOSSIBLE_SPREAD` (n/a aggTrades), `NEGATIVE_SIZE`, `ZERO_OR_INVALID_PRICE`, `ARCHIVE_CHECKSUM_MISMATCH`, `REST_RETENTION_GAP`, `FORCE_ORDER_PROXY_INCOMPLETENESS` (n/a archive), `FAILED_ATOMIC_WRITE`, `PARTIAL_FILE_RECOVERY_EVENT`.
- The candidate's `severity` defaults to `ERROR` for any per-row failure that comes from a §10 check that fails, and to `WARN` for partial / informational discoveries. `INFO` is reserved for purely informational candidates that do not affect overall status.
- The candidate's `downstream_eligibility_action` defaults to `EXCLUDE` for `ERROR` and `WARN`; `PROXY_ONLY` is reserved for proxy-class datasets that the archive aggTrades family is not.
- A `severity = ERROR` candidate makes the orchestrator force `overall_status = FAIL`.

---

## 15. Manifest immutability and successor-state policy

- Default mode (`write_successor_manifest=False`): Phase 4bb-C **never** writes any successor manifest. The original `data/microstructure/manifests/<dataset_family>__<version>.json` is read-only. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` raise behaviour is **not** bypassed.
- Reserved mode (`write_successor_manifest=True`): only available if the Phase 4bb-C authorization brief explicitly enables it. Even then, the constraint is:
  - `research_eligible_after` **must remain `false`** for raw aggTrades families.
  - At most, `eligibility_gate_status` may be transitioned from `pending` to `pass` or `fail`.
  - The successor manifest must be written to a *new* path with an explicit version-suffix bump (e.g. `__v001b.json` or `__v002.json` per Phase 4ba §13.2 governance), never overwriting the original.
  - The original `__v001.json` remains on disk byte-identical and gitignored.
- Default mode is the **only** mode Phase 4bb-C is expected to run in unless the operator explicitly authorizes the reserved mode. Tests must cover both cases, but the reserved mode test must include a canary check that fails the test if the Phase 4bb-C authorization brief is missing the explicit enablement (i.e. tests cannot accidentally enable the reserved mode).
- `data/microstructure/gate-reports/` is a new conceptual directory under the existing gitignored namespace. Phase 4bb-C creates it on first write; no `.gitignore` change is needed because `data/microstructure/` already covers it.

---

## 16. Fail-closed conditions

The Phase 4bb-C primitive must fail closed (i.e. set `overall_status = FAIL` or `ERROR` and refuse to write any successor manifest, even in reserved mode) on any of:

1. **Path discipline.** `manifest_path` does not resolve to a file under `data/microstructure/manifests/`. `output_root` does not resolve under `data/microstructure/`.
2. **Read-only discipline.** The orchestrator detects an attempt to mutate any file outside `data/microstructure/gate-reports/` (and only the new gate report, not the existing manifest, raw zip, sidecar, or acquisition log).
3. **Network discipline.** Any module the gate imports must not transitively import `requests` / `httpx` / `aiohttp` / `urllib.request` / `urllib3` / `socket` / `websockets` / `binance` / `dotenv` / `os.environ` / `getenv`. Tests must include an import-boundary scan that fails if any of these is reachable from the gate module tree.
4. **Credential discipline.** Any string in the input config or read manifest matching `DENYLIST_TOKENS` (`api_key`, `secret`, `signature`, `listenKey`, `userDataStream`, `/fapi/v1/order`, `/fapi/v2/account`, `/fapi/v2/positionRisk`, `/fapi/v1/leverage`, `/fapi/v1/marginType`, `/fapi/v1/forceOrders`, `.env`, `Graphify`, `MCP`, `.mcp.json`) fails the gate.
5. **Manifest immutability.** The original manifest's bytes hash must be identical before and after the gate run. The orchestrator records both hashes in `boundary_confirmations` and FAILs if they differ.
6. **research_eligible discipline.** If at any point the in-memory `research_eligible_after` would compute to `true` for a raw family, the orchestrator raises an explicit assertion error and FAILs.
7. **eligibility_gate_status discipline.** `eligibility_gate_status_after` must be `pass` only when every `check` is `pass` or `not_applicable`; any `fail` or `error` forces `fail` (or `pending` on unrecoverable error).
8. **45-check completeness.** Exactly 45 entries in `result.checks`. Fewer or more is an internal error and FAIL.
9. **Forbidden-derived data.** No JSONL, no Parquet, no DuckDB, no derived dataset, no normalised feature table, no label, no aggregated statistic beyond `measured_summary`. Tests must scan the gate output tree to enforce this.
10. **No successor authorization.** `result.no_successor_authorization` must always be `true`. Any code path that would set it `false` is an internal error and FAIL.
11. **Static governance shape.** `governance_labels.feature_computation == "forbidden"` and `governance_labels.strategy_use == "forbidden"` for raw families. The gate FAILs if either is missing or different.

---

## 17. Test plan for future implementation

Phase 4bb-C must add at least the following tests under `tests/research/microstructure/`. All tests must be offline (`pytest tmp_path` only) and must not hit `data/microstructure/` outside the test's own `tmp_path` fixture.

### 17.1 Happy-path tests

- `test_run_eligibility_gate_passes_on_phase4az_fixture`: a tmp_path-scoped mini-fixture that mirrors the Phase 4az archive shape (small synthesised aggTrades CSV with header, monotone IDs, in-day timestamps, valid manifest, valid sidecar, valid acquisition log) produces `overall_status=pass`, `research_eligible_after=false`, `eligibility_gate_status_after=pass`, exactly 45 checks all `pass` or `not_applicable`, empty `invalid_window_candidates`, `boundary_confirmations` all `true`.
- `test_run_eligibility_gate_writes_report_under_gate_reports`: verifies the gate report file is written under `tmp_path/.../gate-reports/...json` with paired `.sha256`.
- `test_run_eligibility_gate_does_not_mutate_original_manifest`: hashes the manifest before and after, asserts equality.
- `test_run_eligibility_gate_does_not_mutate_raw_zip_or_sidecar`: same hash equality for raw zip and sidecar.
- `test_run_eligibility_gate_returns_45_checks_exactly`: regression guard.
- `test_run_eligibility_gate_research_eligible_after_is_false_for_raw_family`: regression guard.

### 17.2 Failure-path tests (one per failure pattern)

- `test_sha_recompute_mismatch_fails`: mutate the test fixture's zip bytes after manifest creation; gate FAILs at check 10.2.7.
- `test_missing_sidecar_fails`: omit the `.sha256` sidecar; gate FAILs at check 10.2.7.
- `test_missing_acquisition_log_fails`: omit the acquisition log; gate FAILs at check 10.12.45.
- `test_multiple_zip_csv_members_fail`: ZIP with two CSV members; gate FAILs at check 10.10.33.
- `test_malformed_row_fails`: row with `m="maybe"`; gate FAILs at check 10.4.14.
- `test_duplicate_aggregate_trade_id_fails`: gate FAILs at check 10.7.24 and records `DUPLICATE_EVENT` candidate.
- `test_out_of_order_aggregate_trade_id_fails`: gate FAILs at check 10.6.21 and records `OUT_OF_ORDER_EVENT` candidate.
- `test_out_of_day_timestamp_fails`: a row with `T` past `UTC_DAY_END`; gate FAILs at check 10.5.20.
- `test_manifest_sha_disagrees_with_sidecar_fails`: gate FAILs at check 10.2.7.
- `test_manifest_row_count_mismatch_fails`: manifest declares 1681098 but CSV has 1681097; gate FAILs at check 10.8.27.
- `test_unknown_governance_label_fails`: missing `validator` key; gate FAILs at check 10.3.11.
- `test_feature_computation_not_forbidden_fails`: `governance_labels.feature_computation = "allowed"`; gate FAILs at check 10.12.41.
- `test_strategy_use_not_forbidden_fails`: same pattern at check 10.12.42.
- `test_raw_family_research_eligible_true_fails`: manifest declares `research_eligible: true`; gate FAILs at check 10.3.10.
- `test_eligibility_gate_status_inconsistent_with_research_eligible_fails`: any `(true, pending)` or `(true, fail)` combination fails at check 10.3.10.
- `test_invalid_windows_evidence_missing_fails`: a manifest invalid-window with empty `evidence`; gate FAILs at check 10.11.38.
- `test_no_silent_omission_fails`: a per-row anomaly that has no manifest invalid-window; gate FAILs at check 10.11.40 and records a candidate.
- `test_unexpected_extra_columns_warn_or_fail`: an extra unknown column; gate either WARNs (recorded in candidate) or FAILs depending on Phase 4bb-C policy choice — the policy must be predeclared in Phase 4bb-C's authorization brief.

### 17.3 Boundary tests

- `test_no_network_call_possible`: import-boundary scan + monkey-patched `socket.socket` raising; gate must run and PASS without ever hitting the patched socket.
- `test_url_denylist_guard_runs_during_gate`: the gate's denylist scan rejects manifest containing a credential-shaped string; gate FAILs at check 10.12.44.
- `test_no_environment_or_dotenv_read`: monkey-patch `os.environ` access to raise; gate must still PASS on the happy path (it does not need env vars).
- `test_no_mcp_or_graphify_imported`: import-boundary scan asserts that `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`, `eligibility_io.py` do not import any `mcp*` / `graphify*` package or read `.mcp.json`.
- `test_output_root_outside_data_microstructure_rejected`: gate refuses to construct an `AggTradesEligibilityGateInput` whose `output_root` resolves outside `data/microstructure/`.
- `test_write_successor_manifest_default_false_is_no_op`: even on PASS, default invocation does not write any successor manifest.
- `test_write_successor_manifest_true_only_with_brief_enablement`: the test infrastructure asserts that this mode is locked behind a brief-enablement flag and refuses by default.

### 17.4 Re-run tests

- `test_re_running_gate_on_same_inputs_produces_same_overall_status`: deterministic.
- `test_re_running_gate_does_not_overwrite_existing_report`: report file path uses `report_id` containing `created_at_utc_ms` so reruns produce distinct files; if a path collision occurs, refuse to overwrite (RawWriter discipline).

### 17.5 Coverage minimum

Phase 4bb-C must achieve:

- 45 / 45 check functions covered by at least one test (one happy path per check + one explicit failure path per check that has a failure mode).
- Total new test count ≥ 90.
- All tests offline (no network).
- All tests use `pytest tmp_path` only.
- Whole-repo `pytest`, `ruff check .`, `mypy` (strict) must pass with the same pre-existing 2-failure baseline (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`).

---

## 18. Acceptance criteria for future Phase 4bb-C

Phase 4bb-C is acceptable if and only if:

1. **Code surface.** Only the four new modules listed in §8.1 are added under `src/prometheus/research/microstructure/`. The narrow `__init__.py` re-export update is allowed. No other source file is modified.
2. **Test surface.** Only the new test files listed in §8.2 are added under `tests/research/microstructure/`. No existing test is modified except possibly `test_import_boundaries.py` to add the new modules to the scan list (lint-level only).
3. **No script.** No new `scripts/...` entrypoint.
4. **No dependency.** No change to `pyproject.toml`. Stdlib + Phase 4aw / Phase 4ax modules only.
5. **No `.gitignore` change.** `data/microstructure/` already covers the new `gate-reports/` subdirectory.
6. **No data or manifest mutation under default invocation.** Hash before / hash after must match exactly for the manifest, raw zip, and sidecar.
7. **Gate report only under gitignored path.** All output goes to `data/microstructure/gate-reports/`.
8. **All planned failure tests pass.** Every test in §17.2 fails the gate at exactly the predicted check id.
9. **45-check completeness.** Result always carries exactly 45 entries.
10. **research_eligible discipline.** `research_eligible_after = false` for every raw aggTrades family in every test path.
11. **eligibility_gate_status discipline.** `eligibility_gate_status_after` is `pass` only when every check is `pass` or `not_applicable`; in default mode, no successor manifest is written even on PASS.
12. **Quality gates.** `ruff check .` passes; `mypy` strict passes (89 + 4 = 93 source files); whole-repo `pytest` passes apart from the 2 pre-existing simulation failures; `git check-ignore -v data/microstructure/` continues to report `.gitignore:85`.
13. **No successor authorization.** `result.no_successor_authorization == true` always; the gate must not output any text suggesting Phase 4bb-* successor or paper / shadow / live / Phase 5 / Phase 4 canonical.
14. **No `.env`, no `.mcp.json`, no MCP, no Graphify, no credentials, no network call.** Verified by import-boundary scan and runtime monkey-patches.

---

## 19. What this phase proves

- That the Phase 4ba 45-check enumeration, the Phase 4ba fail-closed rules, the Phase 4ba staged eligibility ladder, the Phase 4bb-A 13 application-time observations, and the existing Phase 4aw / Phase 4ax scaffold can be expressed as a precise, file-by-file, function-by-function execution plan **without writing any code**.
- That a future Phase 4bb-C, if separately authorized, has a clean implementation contract: four new source modules, one narrow `__init__.py` re-export update, several new test files under `tests/research/microstructure/`, no new script, no new dependency, no new `.gitignore` entry, no manifest mutation, no data acquisition, no flag flip on raw families, and no successor authorization.
- That `data/microstructure/gate-reports/` is a viable output namespace under the existing gitignore boundary.

---

## 20. What this phase does not prove

- Anything about edge, opportunity rate, microstructure feature viability, or strategy potential of any aggTrades dataset.
- Anything about additional dataset families, alt symbols, additional UTC days, or live-stream capture.
- That Phase 4bb-C will be authorized.
- That the eligibility-gate primitive must be implemented at all. Phase 4bb-B is planning evidence; remain-paused remains a valid permanent posture.

---

## 21. Preserved boundaries

- **No data was modified.** `data/microstructure/` is byte-identical to the post-Phase-4az state. Phase 4az manifest mtime is the original `May 7 21:55`. The Phase 4ba and Phase 4bb-A merge-closeouts are on `main` unchanged.
- **`data/microstructure/` remains gitignored.** `git check-ignore -v` continues to report `.gitignore:85`.
- **`research_eligible` remains `false`** on the Phase 4az manifest. **`eligibility_gate_status` remains `pending`**.
- **No acquisition.** No HTTP request, no `data.binance.vision` fetch, no Binance API call, no WebSocket, no credential, no `.env`, no `.mcp.json`, no MCP, no Graphify.
- **No code change.** No file under `src/prometheus/`. No test under `tests/`. No script under `scripts/`. No `pyproject.toml`, `README.md`, or `.gitignore`. No M0 governance text.
- **No retained verdict revised. No project lock loosened.**
- **No successor phase authorized.**

---

## 22. Recommended future options

Phase 4bb-B does not authorize any successor. The following are recorded for operator evaluation only.

### Option A — Remain paused (primary)

Procedurally clean. Preserves every retained verdict and project lock. The execution plan is now on record and can be picked up by a separately authorized Phase 4bb-C if and when the operator chooses.

### Option B — Future docs-and-code Phase 4bb-C eligibility-gate primitive implementation (conditional next)

**Allowable; not authorized.**

A future docs-and-code phase implements the four new modules under `src/prometheus/research/microstructure/`, the new test files under `tests/research/microstructure/`, and runs the gate against the Phase 4az dataset to produce a first JSON gate report under `data/microstructure/gate-reports/`. Phase 4bb-C is **not** activated by this memo.

### Option C — Future docs-only Phase 4bb-D eligibility-gate extension to additional dataset families (conditional later)

**Allowable; not authorized.**

A future docs-only memo extends the Phase 4ba / Phase 4bb-A / Phase 4bb-B chain to additional dataset families (e.g. `microstructure_raw_bookticker_v001`, `microstructure_raw_depth_v001`, `microstructure_raw_forceorder_proxy_v001`). Each family has its own check list; Phase 4ba's contract is aggTrades-only.

### Forbidden

- Acquire additional aggTrades data.
- Compute features / train ML / build strategy.
- Flip `research_eligible` to `true` on any raw family.
- Authorize Phase 5 / Phase 4 canonical / paper / shadow / live-readiness / deployment / exchange-write / production keys.

---

## 23. Closeout / lock preservation

Phase 4bb-B preserves verbatim:

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** — OPERATIONALLY CLOSED.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

Project locks preserved verbatim:

- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade, 2× leverage cap, one position max, mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent applied verbatim by Phase 4az and reaffirmed by Phase 4ba; structural QA confirmed by Phase 4bb-A; execution plan mapped by Phase 4bb-B).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4ak — M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al — refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay, Phase 4az, Phase 4ba, Phase 4bb-A results — all preserved verbatim.

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane. The Phase 4az dataset's `research_eligible=false` and `eligibility_gate_status=pending` are unchanged.

**Recommended state:** remain paused. **No successor phase is authorized.**
