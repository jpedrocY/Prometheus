# Phase 4az — Public AggTrades Archive Acquisition (BTCUSDT, 2025-01-15 UTC)

**Type:** code-and-docs public-archive acquisition phase.
**Status:** drafted on branch `phase-4az/public-aggtrades-archive-acquisition`; pending operator review and merge approval.
**Date:** 2026-05-07.
**Acquisition status:** **`SUCCESSFUL_ACQUISITION`**.

---

## 1. Executive summary

Phase 4az is the first authorized real-data microstructure acquisition phase of the project. It acquired exactly one Binance USDⓈ-M Futures aggTrades daily archive for `BTCUSDT` on `2025-01-15` UTC from the public `data.binance.vision` archive, under the strict integrity gate predeclared in Phase 4ay §10. The archive's checksum was downloaded first, parsed, and bit-for-bit verified against the SHA256 of the downloaded ZIP. Every row was validated against the Phase 4ax `validate_aggtrade_payload`. The raw `.zip`, paired `.sha256`, and a `MicrostructureManifest`-shaped JSON manifest plus an acquisition log were written under the gitignored `data/microstructure/` tree.

No code under `src/prometheus/` was modified. Phase 4az added one new standalone acquisition script under `scripts/`. No existing test was modified except a narrow update to one Phase 4ax regression check whose premise (no microstructure data ever) was specific to Phase 4ax. No retained verdict, project lock, M0 governance, or `.gitignore` rule was changed.

The acquired dataset has `research_eligible=false` and `eligibility_gate_status=pending`. It is **infrastructure evidence only**. It does **not** create a strategy candidate, does **not** open any rescue path for cooled-down candidates, does **not** authorize feature computation, ML, paper / shadow / live-readiness, exchange-write, or any successor phase. The Phase 4ay §11.6 cost-realism preservation, the Phase 4ay M0 + post-null-cooldown preservation, and the Phase 4ay no-rescue boundary are preserved verbatim.

---

## 2. Scope and explicit non-scope

### Allowed (and performed) in Phase 4az

- Implement `scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` (standalone, stdlib + Phase 4ax/4aw scaffold imports only, allowed network host `data.binance.vision` only).
- Download exactly two files: the `.CHECKSUM` companion first, then (only after the checksum was parsed) the daily archive ZIP.
- Verify SHA256.
- Validate every row via `validate_aggtrade_payload` plus the per-file integrity checks of Phase 4ay §10 (timestamp range, monotonic non-decreasing aggregate trade IDs, no duplicate aggregate IDs, single-CSV-member ZIP, nonzero size, max 5 GiB).
- Create `data/microstructure/{staging,raw,manifests}/...` directories.
- Write the raw `.zip`, paired `.sha256`, manifest, and acquisition log under `data/microstructure/`.
- Implement `tests/research/microstructure/test_phase4az_archive_acquisition.py` (35 offline tests; pytest `tmp_path` only; `do_network=False` orchestrator hook).
- Narrowly update `tests/research/microstructure/test_aggtrades.py` to repurpose one Phase 4ax regression check (its premise was no longer valid once Phase 4az was authorized).
- Add this Phase 4az memo and the Phase 4az closeout under `docs/00-meta/implementation-reports/`.
- Update `docs/00-meta/current-project-state.md` narrowly.

### Forbidden (and not performed) in Phase 4az

- No call to `fapi.binance.com` or any other Binance API host.
- No REST polling.
- No WebSocket.
- No private endpoints.
- No authenticated endpoints.
- No API keys, no `.env`, no credentials.
- No user stream / listenKey.
- No order / account / position / leverage / margin / `forceOrders` REST.
- No ETHUSDT.
- No alt symbols.
- No multi-day acquisition.
- No monthly archive.
- No depth / bookTicker / forceOrder / OI / funding / mark-price / index-price / 5m / 1m / tick / order-book.
- No normalization to JSONL / Parquet as a separate dataset.
- No feature computation.
- No predictive statistic computation.
- No backtest.
- No historical strategy script.
- No rerun of Phase 4aq or any prior research script.
- No simulation as research.
- No strategy candidate.
- No entry / exit design.
- No ML model.
- No retained-verdict alteration.
- No project-lock alteration.
- No M0 governance alteration.
- No successor authorization.

---

## 3. Repository verification summary

Before branching:

- Branch: `main`.
- Working tree: clean (only gitignored `.claude/scheduled_tasks.lock` and `data/research/` untracked).
- `git rev-parse main` and `git rev-parse origin/main` both `caaad39e40604571758bc58eaac374344c7852e8`.
- All Phase 4ay artefacts present on main: memo, closeout, merge-closeout.
- All Phase 4ax / 4aw artefacts present on main.
- `.gitignore` line `data/microstructure/` present.
- `data/microstructure/` directory did not exist.

Phase 4az branch `phase-4az/public-aggtrades-archive-acquisition` was created from this clean base.

---

## 4. Methodology

- **Public archive acquisition only.** Two and only two HTTP GET requests against `data.binance.vision` were issued: the `.CHECKSUM` companion first, then the daily ZIP after the checksum was parsed and validated.
- **BTCUSDT only.** No alt symbol, no ETHUSDT.
- **One UTC day only.** The predeclared date is `2025-01-15`.
- **Archive mode only.** No REST polling. No WebSocket. No private endpoint. No credentials.
- **Checksum first.** A 64-character lowercase SHA256 hex was parsed from the `.CHECKSUM` body before the ZIP was fetched.
- **Strict integrity gate.** Every Phase 4ay §10 check ran (see §12 below).
- **Raw archive only.** The acquired `.zip` is preserved verbatim. No decompression into the final tree. No normalised JSONL or Parquet.
- **Manifest with `research_eligible=false` and `eligibility_gate_status=pending`.** The Phase 4ay manifest contract is honoured field-for-field; the manifest is JSON to keep the script stdlib-only, while still matching the Phase 4aw `MicrostructureManifest` data shape (see §13).
- **No feature computation.** No metric, transform, or summary statistic is derived from the rows beyond what the Phase 4ax validator already enforces (`Decimal` price / quantity, taker-side derivation per row).
- **No strategy interpretation.** No row, no count, no time-series, no taker-side mix is exposed to any strategy candidate or any cooled-down family.
- **No successor authorization.** The phase ends without authorising Phase 4ba, Phase 5, or any other successor.

---

## 5. Phase 4ay boundary followed

Phase 4ay §7 acquisition target: data family `microstructure_raw_aggtrades_v001`; Binance USDⓈ-M Futures; public archive only via `data.binance.vision`; **BTCUSDT only**; one complete UTC daily archive; archive mode only; descriptive future paths under `data/microstructure/{staging,raw,manifests}/...`; `research_eligible=false` default; `eligibility_gate_status=pending` default. **Followed verbatim.**

Phase 4ay §10 integrity gate (19 checks): see §12 below for per-check PASS / FAIL / NOT_APPLICABLE.

Phase 4ay §11 staging plan: archive landed in staging first; final move atomic via `Path.replace`; raw `.zip` preserved; SHA256 paired file written; no normalization; `data/microstructure/` remains gitignored; staging cleaned on success. **Followed verbatim.**

Phase 4ay §12 manifest contract: every required field present (see §13). **Followed verbatim.**

Phase 4ay §13 fail-closed rules (14): not exercised on the success path; the test suite exercises every fail-closed path on offline fixtures and confirms staging is preserved on failure with no final raw / manifest written.

Phase 4ay §15 §11.6 preservation: the acquisition is infrastructure only; no fee / slippage / funding assumption changed; §11.6 = 8 bps per side preserved verbatim.

Phase 4ay §16 M0 + no-rescue preservation: data is infrastructure only; no cooled-down family reopened; no R3 / R2 / V1 rescue; no 5m thread reopening; no feature, ML, or strategy work derived from the acquired rows.

---

## 6. Acquisition target

| Item | Value |
| ---- | ----- |
| Symbol | `BTCUSDT` |
| Date | `2025-01-15` (UTC) |
| Archive URL | `https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip` |
| Checksum URL | `https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip.CHECKSUM` |
| Capture mode | `historical_archive` |
| Dataset family | `microstructure_raw_aggtrades_v001` |
| Dataset version | `v001` |
| Schema version | `v001` |

**Date rationale:** the date is predeclared verbatim by the operator brief. It is BTCUSDT only, exactly one complete UTC day, stable historical (well over 30 days before the current project date of 2026-05-07), and was not selected based on expected market behaviour. No date-window mining was performed.

---

## 7. Script implementation summary

`scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` is standard library only (`urllib.request`, `urllib.parse`, `urllib.error`, `zipfile`, `csv`, `hashlib`, `json`, `argparse`, `subprocess`, `io`, `sys`, `dataclasses`, `datetime`, `pathlib`) plus three names imported from `prometheus.research.microstructure.aggtrades` (`validate_aggtrade_payload`, `AggTradeValidationError`, `TakerSide`). `subprocess` is used only to read the current `git rev-parse HEAD` for the manifest's `code_commit_sha` field. `urllib.request.urlopen` is used only for the two predeclared `data.binance.vision` URLs.

Public surface:

- `assert_archive_url_allowed(url)` — URL allowlist enforcement (https only; host `data.binance.vision`; path must contain `/aggTrades/`; rejects every Binance API host, private endpoint, credential-shaped string, MCP / Graphify / `.mcp.json` / `.env` token).
- `parse_sha256_from_checksum(content)` — first-64-hex-character extraction with strict hex validation; rejects empty, short, or non-hex content.
- `validate_aggtrades_archive(zip_path)` — runs the per-row Phase 4ax validator plus the per-file integrity checks (single CSV member; nonzero rows; UTC-day timestamp range; trade-id duplicate detection; trade-id monotonicity).
- `acquire(*, output_root, fail_if_existing, do_network)` — orchestrator; `do_network=False` is a test-only hook that consumes a pre-staged fixture; production calls always use `do_network=True`.
- `main(argv)` — CLI wrapper; supports `--dry-run`, `--fail-if-existing/--no-fail-if-existing`, and `--output-root`.

CLI safety: the CLI refuses `--output-root` paths that do not contain `data/microstructure` substring; the underlying `acquire(...)` orchestrator is invariant under this constraint as well. The dry-run path prints planned URLs and paths without creating any directory.

The script does **not** import from `prometheus.runtime`, `prometheus.execution`, or `prometheus.persistence`. The repo's pytest `pythonpath` already exposes `src/`; the script also prepends `src/` to `sys.path` at start so direct invocation (`python scripts/...`) works without an editable install.

---

## 8. Test implementation summary

`tests/research/microstructure/test_phase4az_archive_acquisition.py` provides **35 offline tests** that consume only pytest `tmp_path` and call the orchestrator with `do_network=False`:

- 6 checksum parsing tests (accepts 64-hex; lowercases hex; rejects short / non-hex / empty / non-string content).
- 11 URL allowlist tests (accepts archive ZIP and `.CHECKSUM`; parametrised rejection of `fapi.binance.com`, `/fapi/v1/order`, `/fapi/v2/account`, `/fapi/v2/positionRisk`, `/fapi/v1/listenKey`, user stream, http instead of https, foreign hosts, credential-shaped paths, empty string).
- 9 CSV / row tests (header CSV validates; headerless CSV validates; invalid `m` strings reject; duplicate `a` rejects; out-of-order `a` rejects; trade-time before UTC day rejects; trade-time at next-day-start rejects; empty CSV rejects; multi-CSV-member ZIP rejects).
- 7 end-to-end orchestrator tests (successful fixture acquisition writes under `tmp_path`; manifest has `research_eligible=false` and `eligibility_gate_status=pending`; manifest contains no feature-shaped keys; failure before ZIP when checksum is invalid; failure when checksum does not match ZIP; `urllib.request.urlopen` is monkey-patched to refuse network and the acquisition still succeeds via fixture; CLI dry-run prints plan without creating directories; CLI rejects `--output-root` outside `data/microstructure/`).
- The remaining 2 tests cover hex-uppercase normalisation and timestamp-equals-day-end-exclusive boundary.

`tests/research/microstructure/test_aggtrades.py` had one obsolete regression check (`test_no_data_microstructure_directory_created`) that asserted the project `data/microstructure/` directory does not exist. Phase 4az is now authorised to create that directory, so the test was repurposed (renamed to `test_phase_4ax_tests_do_not_write_under_data_microstructure`) to verify only that *Phase 4ax test code* writes solely under `tmp_path`. This is the only existing test modified by Phase 4az.

The `test_import_boundaries.py` scan continues to cover `src/prometheus/research/microstructure/`. The Phase 4az script lives under `scripts/`, which is outside the package scan; the script's own URL allowlist + targeted unit tests enforce the `data.binance.vision`-only network discipline. No other source file in the package gained network capability.

---

## 9. Acquisition status

**`SUCCESSFUL_ACQUISITION`.**

---

## 10. Successful acquisition details

| Item | Value |
| ---- | ----- |
| Final raw path | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` |
| Final SHA file | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` |
| ZIP SHA256 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Checksum source | `data.binance.vision/.../BTCUSDT-aggTrades-2025-01-15.zip.CHECKSUM` |
| Event count | `1,681,098` |
| First trade time (ms) | `1736899205109` (2025-01-15 00:00:05.109 UTC) |
| Last trade time (ms) | `1736985599991` (2025-01-15 23:59:59.991 UTC) |
| UTC-day coverage | every observed `T` falls in `[2025-01-15 00:00:00.000 UTC, 2025-01-16 00:00:00.000 UTC)` |
| Duplicate aggregate-trade IDs | none |
| Aggregate-trade-ID monotonicity | non-decreasing across the file |
| Schema validation | every row passed `validate_aggtrade_payload` |
| Manifest path | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` |
| Acquisition log path | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json` |
| Local dataset size | ~21 MiB on disk |
| Staging cleanup | staging artefacts cleaned on success |

All five output files are under the gitignored `data/microstructure/` tree (line 85 of `.gitignore` added by Phase 4aw). `git status` does not list them. `git check-ignore -v` confirms the rule applies.

---

## 11. If fail-closed (not applicable)

The acquisition succeeded; no fail-closed branch was taken. The fail-closed branches are exhaustively exercised by the offline test suite (`tests/research/microstructure/test_phase4az_archive_acquisition.py`), which verifies that on validation failure no final raw file or manifest is produced and staging is preserved.

---

## 12. Integrity gate checklist (Phase 4ay §10, 19 checks)

| # | Check | Result |
| - | ----- | ------ |
| 1 | Source provenance recorded | **PASS** (`endpoint_docs_reference` recorded in manifest) |
| 2 | File downloaded exactly once into staging | **PASS** |
| 3 | Checksum downloaded if available; bit-for-bit verified | **PASS** (matched on first compare) |
| 4 | Nonzero file size with predeclared upper bound (5 GiB) | **PASS** (~21 MiB) |
| 5 | Decompression succeeds cleanly | **PASS** (single CSV member opened with `zipfile`) |
| 6 | Every row passes `validate_aggtrade_payload` | **PASS** (1,681,098 / 1,681,098) |
| 7 | Row count strictly > 0 | **PASS** (1,681,098) |
| 8 | Timestamp range matches requested UTC day | **PASS** (min `T = 1736899205109`; max `T = 1736985599991`) |
| 9 | Symbol consistency | **PASS via path scope** (archive path is symbol-scoped; `governance_labels.symbol_scope_source = "archive_path"`) |
| 10 | No duplicate aggregate trade IDs | **PASS** |
| 11 | Aggregate trade IDs monotonically non-decreasing | **PASS** |
| 12 | Price > 0 | **PASS** (Phase 4ax validator) |
| 13 | Quantity > 0 | **PASS** (Phase 4ax validator) |
| 14 | `m` strict bool | **PASS** (string→bool coercion: `true/True/TRUE`/`false/False/FALSE`) |
| 15 | No project data overwrite | **PASS** (final paths did not pre-exist; `--fail-if-existing` default) |
| 16 | Invalid windows recorded | **NOT_APPLICABLE** (no integrity events; `invalid_windows` is `[]`) |
| 17 | Manifest written with `research_eligible=false` and `eligibility_gate_status=pending` | **PASS** |
| 18 | Eligibility gate fails closed until separately authorized | **PASS** (gate not implemented; `eligibility_gate_status=pending`) |
| 19 | No feature computation | **PASS** |

---

## 13. Manifest review

The produced manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json`:

```json
{
  "dataset_family": "microstructure_raw_aggtrades_v001",
  "version": "v001",
  "symbol": "BTCUSDT",
  "source": "binance_data_archive",
  "endpoint": "data.binance.vision/data/futures/um/daily/aggTrades",
  "capture_mode": "historical_archive",
  "start_time_ms": 1736899205109,
  "end_time_ms": 1736985599991,
  "event_count": 1681098,
  "file_count": 1,
  "files": [
    {
      "path": "raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip",
      "sha256": "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e",
      "event_count": 1681098,
      "start_time_ms": 1736899205109,
      "end_time_ms": 1736985599991
    }
  ],
  "schema_version": "v001",
  "endpoint_docs_reference": "https://github.com/binance/binance-public-data#trades (futures aggTrades daily archive convention)",
  "capture_config_hash": "d7508638b2184f4754900b6f2c2165a9499d5e79d0494600a62516738368010d",
  "code_commit_sha": "caaad39e40604571758bc58eaac374344c7852e8",
  "invalid_windows": [],
  "retention_warning": null,
  "proxy_warning": null,
  "governance_labels": {
    "phase": "4az",
    "source_phase_boundary": "4ay",
    "validator": "phase_4ax_aggtrades_v001",
    "stop_trigger_domain": "trade_price_backtest_candidate",
    "symbol_scope_source": "archive_path",
    "feature_computation": "forbidden",
    "strategy_use": "forbidden"
  },
  "research_eligible": false,
  "eligibility_gate_status": "pending"
}
```

**`research_eligible=false` and `eligibility_gate_status=pending` are present.** The Phase 4aw `MicrostructureManifest` `flip_research_eligible(...)` method (which always raises) is not bypassed here; the manifest is JSON-only and never round-trips back through the Phase 4aw dataclass, but the field defaults match Phase 4ay §12 verbatim.

The manifest is shape-compatible with `MicrostructureManifest.from_dict(...)`: each required field is present with the right type and the file entry has the 64-character hex `sha256`. A future eligibility-gate phase could load and inspect this manifest via the Phase 4aw model.

---

## 14. Data boundary

- **`data/microstructure/` is gitignored.** The line `data/microstructure/` is present at `.gitignore:85` (added by Phase 4aw).
- **Local data was not committed.** `git status` shows only the untracked source / test / docs from this phase plus the pre-existing transient files (`.claude/scheduled_tasks.lock`, `data/research/`). No file under `data/microstructure/` is staged or tracked.
- **No normalised dataset.** The archive `.zip` is preserved verbatim. No JSONL or Parquet is produced.
- **No features.** No metric, transform, or summary statistic is derived from the rows.

---

## 15. Security / endpoint boundary

- **Only `data.binance.vision` archive / checksum downloads were performed.** Two URLs total: the `.CHECKSUM` companion (`https://data.binance.vision/.../BTCUSDT-aggTrades-2025-01-15.zip.CHECKSUM`) and the archive (`https://data.binance.vision/.../BTCUSDT-aggTrades-2025-01-15.zip`).
- **No Binance API endpoint contacted.** No `fapi.binance.com`. No `/fapi/v1/aggTrades`. No `/fapi/v1/order`. No `/fapi/v2/account`. No `/fapi/v2/positionRisk`. No `/fapi/v1/leverage`. No `/fapi/v1/marginType`. No `/fapi/v1/forceOrders`. No `/fapi/v1/listenKey`.
- **No WebSocket.** No subscription, no stream.
- **No credentials.** No API key, no secret, no signed request, no `X-MBX-APIKEY` header.
- **No `.env` reads.**
- **No private endpoints.**
- **No user stream / listenKey.**
- **No MCP, Graphify, or `.mcp.json`.**

The script's URL allowlist enforces every one of these denials in code, and the test suite verifies the allowlist with parametrised denylist references.

---

## 16. Relationship to §11.6

`§11.6 = 8 bps slippage per side; round-trip = 16 bps` is unchanged. AggTrades acquisition is **market-data infrastructure**, not a trading result. No fee / slippage / funding assumption was changed. The acquired dataset cannot be used to weaken cost assumptions without a separately authorized methodology phase. Phase 4az does not propose such a phase.

---

## 17. Relationship to M0 and no-rescue

- **Data is infrastructure only.** The acquired dataset has `research_eligible=false` and `eligibility_gate_status=pending`. It is not eligible for any feature, strategy, or ML use until a separately authorized eligibility-gate phase runs.
- **No strategy.** No strategy candidate is created. No entry / exit is designed. No threshold is selected.
- **No feature.** No metric, transform, taker-imbalance, sweep detection, or aggressive-flow score is computed.
- **No cooled-down family reopened.** R2 / F1 / D1-A / V2 / G1 / C1 all remain in their current cooled-down posture. No R3 / R2 / V1 rescue. No old-strategy alt-symbol rerun.
- **No 5m thread reopening.** Phase 3t closure preserved.
- **Future feature work must separately clear M0.** Any hypothesis derived from acquired aggTrades must satisfy the Phase 4ak twelve-clause M0 gate, the Phase 4l 18-requirement validity gate, and the Phase 4t 10-dimension scoring matrix in a separately authorized hypothesis-spec memo *before* any feature is computed.

---

## 18. Validation results

| Command | Result |
| ------- | ------ |
| `python -m compileall scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` | pass |
| `python -m compileall tests/research/microstructure` | pass |
| `ruff check scripts/phase4az_acquire_btcusdt_aggtrades_archive.py tests/research/microstructure` | `All checks passed!` |
| `ruff check .` (whole repo) | `All checks passed!` |
| `pytest tests/research/microstructure` | **196 passed** (Phase 4aw 114 + Phase 4ax 47 + Phase 4az 35) |
| `pytest tests/research/microstructure/test_phase4az_archive_acquisition.py` | **35 passed** |
| `pytest` (whole repo) | **979 passed, 2 failed** (the two pre-existing `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt` failures, both `KeyError: 'trade_count'` in the unrelated `src/prometheus/research/data/storage.py:232`); **Phase 4az introduced zero new regressions** |
| `mypy scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` | `Success: no issues found in 1 source file` |
| `mypy` (whole repo) | `Success: no issues found in 89 source files` |
| `git diff --check` | clean |
| `data/microstructure/` directory | exists locally, **gitignored**; `git status` does not list it |
| `python scripts/phase4az_acquire_btcusdt_aggtrades_archive.py --output-root data/microstructure` | `SUCCESSFUL_ACQUISITION` |

---

## 19. Implementation / governance review

### What changed?

- One new acquisition script (`scripts/phase4az_acquire_btcusdt_aggtrades_archive.py`).
- One new test file (`tests/research/microstructure/test_phase4az_archive_acquisition.py`, 35 tests).
- One narrow update to `tests/research/microstructure/test_aggtrades.py`: the obsolete `test_no_data_microstructure_directory_created` regression check (which asserted the project `data/microstructure/` directory does not exist) was repurposed to instead verify that Phase 4ax test code itself writes only under `tmp_path`. Phase 4az is now authorised to populate `data/microstructure/`, so the original assertion's premise no longer holds.
- Two new docs files (memo + closeout) under `docs/00-meta/implementation-reports/`.
- One narrow `current-project-state.md` update.
- Local data outputs created under the gitignored `data/microstructure/` tree (raw `.zip`, paired `.sha256`, manifest, acquisition log). None of these is committed.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text.
- No Phase 4ak / 4al / 4j / 3p §4.7 / 3r / 3v / 3w governance.
- No Phase 4aw scaffold module.
- No Phase 4ax aggTrades skeleton module.
- No existing dataset manifest under `data/manifests/`.
- No existing trade log under `data/derived/backtests/`.
- No existing strategy spec, validation checklist, runtime doc, or governance memo.
- No existing script under `scripts/` other than the new Phase 4az script.
- No existing test outside the narrowly-updated `test_aggtrades.py` regression check.
- No `pyproject.toml`, `README.md`, or `.gitignore`.

### Were any locks, verdicts, or safety boundaries affected?

No. Phase 4az is data acquisition, not strategy or methodology. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, existing data, manifests, or strategy specs modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4az paragraph addition and the Phase 4ax obsolete-regression-check repurpose described above.

### Mergeability

Mergeable as code-and-docs acquisition. The new script is fully covered by 35 offline tests; whole-repo ruff and mypy strict are clean; whole-repo pytest has zero new regressions. The acquired data is gitignored and not committed. No verdict, lock, or governance was modified.

---

## 20. Research interpretation review

### 1. What did this phase prove?

That the project can safely acquire one predeclared BTCUSDT public aggTrades daily archive from the public `data.binance.vision` archive, verify its checksum bit-for-bit, validate every one of 1,681,098 rows against the Phase 4ax aggTrades validator, enforce every Phase 4ay §10 integrity check (timestamp range, monotonicity, no duplicates, single-CSV member, nonzero size, max 5 GiB), and store the raw archive plus a manifest under the gitignored `data/microstructure/` tree — without contacting any Binance API endpoint, opening any WebSocket, using any credential, modifying any verdict / lock / governance, normalizing into a separate dataset, computing any feature, or authorising any successor phase. It proved that the Phase 4aw scaffold + Phase 4ax aggTrades skeleton + Phase 4ay authorization framework compose cleanly with a working public-archive acquisition.

### 2. What did this phase not prove?

Anything about edge, opportunity rate, predictive content, microstructure feature viability, or strategy potential of the acquired data. The acquired dataset is a single UTC day's worth of one symbol's aggregate trades; no statistical claim is made or licensed. No historical strategy verdict changed. No project lock changed. No cooled-down family is reopened.

### 3. Which original questions did it answer?

- "Can the project safely acquire one predeclared BTCUSDT public aggTrades daily archive, verify checksum, validate row integrity, store the raw archive under gitignored `data/microstructure/`, write a manifest with `research_eligible=false`, and fail closed on any uncertainty?" → **Yes** (verified in production by `SUCCESSFUL_ACQUISITION` for 1,681,098 rows; verified in the offline test suite by 35 passing tests covering every fail-closed branch; verified by `git status` showing zero `data/microstructure/` entries).
- "Does the Phase 4aw raw-writer / manifest discipline survive a real archive download?" → **Yes**, with the manifest as JSON to keep the acquisition script stdlib-only.
- "Does the Phase 4ax aggTrades validator handle real Binance public-archive rows without modification?" → **Yes** (1,681,098 rows validated cleanly; no false rejections, no schema patching).
- "Does the Phase 4ay strict integrity gate work in practice?" → **Yes**, all 18 of the 19 checks passed (the 19th is `NOT_APPLICABLE` because no integrity events occurred).

### 4. Which original questions remain open?

- Whether the Binance public archive is uniformly checksum-companion-equipped across other (symbol, date) combinations remains an acquisition-time consideration; Phase 4az verified availability for BTCUSDT 2025-01-15 only.
- Whether any aggTrades-derived feature would carry edge under §11.6 cost realism is not addressed; a future feature memo must satisfy M0 and the Phase 4m 18-requirement validity gate first.
- Whether the eligibility-gate primitive should ever be implemented is deferred to a separately authorized future phase.
- Whether to acquire ETHUSDT, additional days, monthly archives, or other data families (depth / bookTicker / forceOrder / OI / funding / mark-price) is deferred — Phase 4az is one acquisition only.

### 5. What does it mean for strategy research?

Plumbing only. The project now has its first real microstructure raw dataset. The dataset is `research_eligible=false` and `eligibility_gate_status=pending`; it is **infrastructure evidence only**. No strategy candidate is created. No cooled-down family is reopened. No 5m thread reopening. No old-strategy alt-symbol rerun. The Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, and the Phase 4ak twelve-clause M0 gate remain binding for any future hypothesis derived from this dataset.

### 6. What does it mean for governance?

Nothing changes. M0 (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4j §11 OI subset governance, the Phase 3p §4.7 strict integrity gate, the Phase 3r §8 mark-price gap governance, the Phase 3v §8 stop-trigger-domain governance, the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, and §11.6 / §1.7.3 project-level locks all remain verbatim. Phase 4az is the first concrete demonstration that the Phase 4ay authorization framework — and the §10 integrity gate, the §11 staging plan, the §12 manifest contract, and the §13 fail-closed rules — works end-to-end on real data.

### 7. What is the clean next step?

After operator review and merge of Phase 4az, **remain paused** is the primary recommendation. The dataset exists locally as infrastructure evidence; it is not eligible for any further use until a separately authorized phase activates it. If the operator separately wishes to advance, two natural separately-authorized next steps exist:

- **Future docs-only Phase 4ba** — eligibility-gate review memo: discusses whether (and how) to ever implement the Phase 4aw `flip_research_eligible(...)` primitive and the Phase 4ay §10 audit-of-pass evidence required to flip the flag for *this specific* dataset.
- **Future docs-only Phase 4ba alt** — data-quality interpretation memo: enumerates what the dataset's row count, taker-side mix, time-density histogram, etc. show *as descriptive statistics only*, framed strictly as data-quality observations and not as edge or feature evidence.

Phase 4az **does not authorize** either of these.

### 8. What should we not do yet?

- Do not flip `research_eligible` to `True`. The Phase 4aw `flip_research_eligible(...)` primitive is intentionally not callable from Phase 4az; an eligibility gate must be implemented in a separately authorized phase before any dataset can be promoted.
- Do not normalise the dataset into Parquet / JSONL.
- Do not compute features (taker imbalance, sweep, aggressive-flow, OI proxy, etc.).
- Do not create a strategy candidate.
- Do not run any backtest against the dataset.
- Do not acquire ETHUSDT, additional days, monthly archives, or any other data family.
- Do not contact any Binance API endpoint.
- Do not open any WebSocket.
- Do not approach paper / shadow, live-readiness, deployment, exchange-write, or production keys.
- Do not authorize a successor phase.

---

## 21. Recommendation

- **Primary:** remain paused. After operator review, merge Phase 4az into `main`, then stop.
- **Conditional secondary (NOT authorized by Phase 4az):** future docs-only Phase 4ba eligibility-gate review memo, separately authorized.
- **Conditional tertiary (NOT authorized by Phase 4az):** future docs-only Phase 4ba data-quality interpretation memo, separately authorized.
- **Not recommended:** acquiring more data, normalizing the dataset, computing features, implementing the eligibility-gate primitive without a docs-only review first.
- **Forbidden:** verdict revision, lock revision, parameter optimization, strategy resurrection, M0 amendment derived from Phase 4az reasoning, reopening the 5m research thread, paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / user stream / MCP / Graphify / `.mcp.json` / credentials.

---

## 22. Explicit preservation of verdicts, locks, and no-rescue constraints

Phase 4az preserves verbatim:

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
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent recorded by Phase 4ay and applied by Phase 4az).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4ak (M0 twelve-clause gate, post-null cooldown rule, cooled-down families list, memo template).
- Phase 4al (refined no-rescue rule + §13 boundary + §14 hierarchy).
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay results.

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane.

**Recommended state remains paused. No successor phase is authorized.**
