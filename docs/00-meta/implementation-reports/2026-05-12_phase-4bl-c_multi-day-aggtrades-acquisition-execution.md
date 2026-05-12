# Phase 4bl-C — Multi-Day aggTrades Acquisition Execution

**Phase identity:** Phase 4bl-C — Multi-Day aggTrades Acquisition Execution (docs + code + local gitignored raw acquisition output).
**Date:** 2026-05-12.
**Phase type:** docs-and-code; acquisition-only execution phase.
**Branch:** `phase-4bl-c/multi-day-aggtrades-acquisition-execution`.
**Base:** `main` at `da9d830c2b900c1c5fa09159e79ce2f0b6bbe249` (Phase 4bl-B SHA-chain-fixup commit on top of the Phase 4bl-B merge-closeout `31e907fcb2034a45257f6f2513fc5b51b48f5e8f`).
**Status:** drafted; pending operator review.
**Authorization:** explicit operator authorization for Phase 4bl-C only.

A note on the SHA-chain pattern: the Phase 4bl-B merge-closeout anchored its §2 final-`main` value at the merge-closeout commit `31e907f`. The one-commit fixup on top of that anchor (commit `da9d830`) only records the final-`main` SHA back into §2 of the Phase 4bl-B merge-closeout; it does not change Phase 4bl-B lifecycle semantics. Phase 4bl-C branches from `da9d830` because that is the post-fixup `main` state; the canonical "Phase 4bl-B project-complete" anchor remains the merge-closeout commit (`31e907f`).

---

## 1. Phase identity

- **Phase name:** Phase 4bl-C — Multi-Day aggTrades Acquisition Execution.
- **Phase type:** docs + code + local gitignored raw acquisition output (acquisition-only).
- **Branch:** `phase-4bl-c/multi-day-aggtrades-acquisition-execution`.
- **Base SHA:** `main` at `da9d830c2b900c1c5fa09159e79ce2f0b6bbe249`.
- **Predecessor anchor:** Phase 4bl-B merge-closeout `31e907fcb2034a45257f6f2513fc5b51b48f5e8f` (project-complete).
- **Authorization:** explicit operator authorization for Phase 4bl-C only (Multi-Day aggTrades Acquisition Execution under the Phase 4bl-B locked design).
- **Script:** `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`.
- **Offline tests:** `tests/research/microstructure/test_phase4bl_c_acquisition_script.py`.

Phase 4bl-C is strictly acquisition-only. It downloads the locked 90 BTCUSDT public daily aggTrades archives from `data.binance.vision`, verifies each archive against its `.CHECKSUM` companion, runs a bounded row-sample validation per ZIP, writes raw zips and paired sidecars to the gitignored `data/microstructure/raw/...` tree, writes one v002 multi-day manifest and one acquisition log (each with paired sidecars), and stops. Phase 4bl-C does **not**:

- normalize raw aggTrades into a derived Parquet family;
- compute features, labels, signals, or any descriptive trading statistic beyond per-file manifest inventory;
- run any eligibility gate (raw / derived / feature / label);
- create gate reports;
- create successor-state artefacts;
- run diagnostics, Q1–Q15, descriptive label statistics, or any predictive metric;
- compute PnL, MFE, MAE, R-multiple, equity, position-state, alpha, edge, prediction, model-score, decision-score, entry-exit, or strategy output;
- train ML, design ML architecture, rank features, or create meta-labeling;
- create a strategy, run a backtest, or produce backtest results;
- use authenticated APIs, private endpoints, public REST endpoints (`fapi.binance.com`, `api.binance.com`, `stream.binance.com`), user streams, WebSockets, listenKey lifecycle, MCP, Graphify, `.mcp.json`, or any credential;
- modify any existing manifest, gate report, successor-state artefact, or label artefact;
- modify any source code, test, script, `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file beyond the narrow Phase 4bl-C additions (one new script, one new test file, and a narrow `current-project-state.md` update);
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any manifest;
- modify project locks, retained verdicts, M0 governance, the Phase 4ak post-null cooldown rule, the Phase 4ak cooled-down families list, the Phase 4al refined no-rescue rule, the Phase 4bb-F canonical path policy, or the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant;
- delete, move, copy, or rename any existing `data/microstructure/` artefact;
- commit any `data/microstructure/` artefact to git;
- authorize Phase 4bl-D, Phase 4bl-E, any Phase 4bm-* / 4bn-* / 4bo-* / 4bp-* / 4bq-* successor, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, or any successor phase.

---

## 2. Pre-state

### 2.1 Pre-state at Phase 4bl-C start

`main` SHA: `da9d830c2b900c1c5fa09159e79ce2f0b6bbe249` (Phase 4bl-B post-fixup state). Working tree clean other than the always-untracked `.claude/scheduled_tasks.lock` and the gitignored `data/research/` directory.

Existing one-day Phase 4az fixture present and byte-identical:

| Property | Value |
| --- | --- |
| Raw zip path | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` |
| Raw zip SHA256 (pre-Phase-4bl-C) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Raw zip size | 21,271,119 bytes |
| Raw zip sidecar size | 100 bytes |
| Raw v001 manifest path | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` |
| Raw v001 manifest SHA256 (pre-Phase-4bl-C) | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Label parquet SHA256 (pre-Phase-4bl-C) | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label manifest SHA256 (pre-Phase-4bl-C) | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |

Gitignore coverage verified via `git check-ignore --verbose`:

```
.gitignore:85:data/microstructure/	data/microstructure/
.gitignore:85:data/microstructure/	data/microstructure/raw/
.gitignore:85:data/microstructure/	data/microstructure/manifests/
.gitignore:85:data/microstructure/	data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/BTCUSDT-aggTrades-2024-12-01.zip
.gitignore:85:data/microstructure/	data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json
.gitignore:85:data/microstructure/	data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json
```

All intended Phase 4bl-C output paths are gitignored under `.gitignore:85: data/microstructure/`.

### 2.2 Phase 4bl-B locked design summary

Phase 4bl-B locked the Phase 4bl-C acquisition design as:

- **Symbol:** BTCUSDT only.
- **Date range:** 2024-12-01 through 2025-02-28 inclusive (UTC).
- **Date count:** 90 contiguous UTC days.
- **Source:** Binance USDⓈ-M Futures public daily aggTrades archives via `data.binance.vision`.
- **Acquisition order per date:** download `.CHECKSUM` companion first; parse first 64 hex characters as expected SHA256; download `.zip` only after companion is parsed; verify locally-computed SHA256 against companion value; atomic write-then-rename; paired `.sha256` sidecar in canonical Phase 4bb-F format.
- **Existing fixture handling:** detect existing `2025-01-15` fixture; cross-verify recorded / fresh-local / fresh-companion SHAs; reuse in place; never overwrite.
- **Failure / retry policy:** max 3 retries with exponential backoff (2s/4s/8s + jitter); 60s per-attempt timeout; 5-min per-date budget; HTTP 404 = permanent (`missing_404`); checksum mismatch = no retry, untrusted zip deleted, recorded; decompression failure = preserve checksum-valid zip, record; row-sample validation failure = preserve zip, record; no silent skipping; no replacement dates; no fallback to APIs.
- **Row-sample validation:** bounded — first 100, last 100, up to 100 deterministic middle rows per ZIP — validated via the Phase 4ax `validate_aggtrade_payload(...)` function. Full per-row gate is **not** run in Phase 4bl-C (deferred to a separately authorized future Phase 4bl-D).
- **Outputs:** raw zip + paired `.sha256` sidecar per date (90 each, with `2025-01-15` reused), one v002 multi-day manifest + paired `.sha256` sidecar, one v002 acquisition log + paired `.sha256` sidecar.
- **Locked path layout:** raw zips at `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/...`; manifests at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.*`.
- **No successor authorization.**

### 2.3 Locked 90-date list

The locked 90-date list is generated deterministically from `date_start = 2024-12-01` to `date_end = 2025-02-28` inclusive (31 + 31 + 28 = 90 days). The script's `generate_locked_date_list()` produces exactly this list and asserts cardinality 90 + existing fixture membership before any network call. Tests `test_date_list_cardinality_is_90`, `test_date_list_first_and_last`, `test_date_list_is_contiguous_and_chronological`, `test_date_list_no_duplicates`, `test_date_list_per_month_counts`, and `test_date_list_includes_existing_fixture_at_index_45` confirm the generated list matches the Phase 4bl-B locked list exactly.

---

## 3. Script summary

### 3.1 File

`scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` is a standalone acquisition script that mirrors the Phase 4az precedent at scale.

### 3.2 Imports

Python standard library only (`argparse`, `contextlib`, `csv`, `hashlib`, `io`, `json`, `os`, `platform`, `random`, `subprocess`, `sys`, `time`, `urllib.error`, `urllib.parse`, `urllib.request`, `uuid`, `zipfile`, `dataclasses`, `datetime`, `pathlib`), plus the Phase 4ax / 4aw scaffold:

```python
from prometheus.research.microstructure.aggtrades import (
    AggTradeValidationError,
    validate_aggtrade_payload,
)
```

No third-party HTTP / async libraries (`requests`, `httpx`, `aiohttp`, `websockets`). No Binance SDK. No `.env` reads. No credential loaders. No MCP / Graphify imports. The offline test `test_module_does_not_import_forbidden_libraries` enforces this statically.

### 3.3 Network guard

`assert_archive_url_allowed(url)` is called before every network read:

- URL scheme must be `https`;
- URL host must be in `ALLOWED_HOSTS = ("data.binance.vision",)`;
- URL path must start with `/data/futures/um/daily/aggTrades/BTCUSDT/`;
- URL path must contain `BTCUSDT-aggTrades-`;
- URL must not contain any of the 30+ forbidden tokens (`fapi.binance.com`, `api.binance.com`, `stream.binance.com`, `/fapi/`, `/api/v1/`, `/api/v3/`, `/v1/order`, `/v1/account`, `/v2/account`, `/v2/positionRisk`, `/v1/leverage`, `/v1/marginType`, `/v1/forceOrders`, `/v1/listenKey`, `userDataStream`, `api_key`, `apiKey`, `secret_key`, `secretKey`, `signature`, `X-MBX-APIKEY`, `.mcp.json`, `Graphify`, `MCP`, `.env`, `/monthly/`, `/data/spot/`, `/data/option/`, `/data/futures/cm/`, `/klines/`, `/markPriceKlines/`, `/indexPriceKlines/`, `/premiumIndexKlines/`, `/metrics/`, `/fundingRate/`, `/openInterest/`).

`_http_get_bytes(url)` re-checks the final URL after any redirect via `response.geturl()` (the response is rejected if the redirect targets a different origin or non-matching path). The download size is bounded by `MAX_DOWNLOAD_BYTES = 5 GiB`.

### 3.4 Date-list guard

`generate_locked_date_list()` deterministically generates the 90 ISO-8601 dates from the locked range and asserts the cardinality matches `EXPECTED_DATE_COUNT = 90` and that `EXISTING_FIXTURE_DATE = "2025-01-15"` is in the generated list. Any deviation raises `AcquisitionFailClosed`.

### 3.5 Path guard

`assert_path_under_microstructure(path, output_root)` rejects any path whose resolved value falls outside `output_root` or any `output_root` whose path does not contain `data/microstructure` (normalised to lowercase forward-slash). The CLI `main()` also enforces this on the `--output-root` argument before any other work.

### 3.6 Gitignore guard

`verify_gitignored(path, *, repo_root)` shells out to `git check-ignore --verbose <path>` and returns `True` iff git reports the path is ignored. The orchestrator `run_acquisition(...)` calls this guard for the manifest path, log path, both sidecars, a representative future raw-zip path under `2024/12/`, and the staging directory before any write occurs. If any path is not gitignored, the orchestrator raises `AcquisitionFailClosed` before any download or write.

### 3.7 Hash / sidecar logic

- `sha256_file(path, *, chunk_size=1 MiB)` — lowercase-hex SHA256 over chunked reads.
- `sha256_bytes(content)` — lowercase-hex SHA256 over in-memory bytes.
- `parse_sha256_from_checksum(content)` — accepts `str` or `bytes`; rejects non-UTF-8 bytes, empty bodies, non-64-char prefixes, non-hex prefixes; normalises to lowercase.
- `make_sidecar_body(sha256_hex, basename)` — canonical Phase 4bb-F format `<sha>  <basename>\n` with exactly two ASCII spaces and a single trailing LF; rejects non-64-char SHAs, non-hex SHAs, empty basenames, and basenames containing path separators.
- `atomic_write_bytes(target, content)` — atomic write-then-rename via `<target>.tmp` + `os.replace`; refuses to overwrite non-identical existing content; no-op on byte-identical existing content.
- `atomic_write_text(target, content)` — UTF-8 wrapper around `atomic_write_bytes`.
- `atomic_move_file(src, dst)` — atomic move with overwrite-refusal; no-op on byte-identical existing target.

### 3.8 Acquisition loop

`acquire_one_date(date_str, *, output_root, events, do_network=True)` is the per-date worker. For each date:

1. Compose locked URLs and resolve local paths; assert allowlist and path discipline.
2. If the date is `2025-01-15` and a local fixture exists, take the existing-fixture branch:
   - compute fresh local SHA;
   - require fresh local SHA == recorded Phase 4az SHA (`f560c2e5...`);
   - download fresh `.CHECKSUM` companion and require parsed value == recorded Phase 4az SHA;
   - read and verify the existing sidecar's SHA prefix matches the recorded SHA (sidecar is **not** rewritten);
   - run `inventory_and_validate_zip(...)` on the existing file (decompression test + row-sample validation);
   - record `status = "acquired_verified"` and `retry_count = 0` on success; otherwise record explicit failure status (`checksum_mismatch`, `checksum_companion_unavailable`, `retry_exhausted`, `decompression_failure`, `row_sample_validation_failure`, or `finalisation_failure`).
3. Otherwise take the normal acquisition branch:
   - if a local file already exists at the final path, compute its SHA;
   - download the `.CHECKSUM` companion with retry policy (`_try_download_with_retry(...)`);
   - parse companion SHA;
   - if local file exists and its SHA matches the companion SHA, skip redownload, run inventory, record `acquired_verified` if the row-sample passes;
   - if local file exists with a different SHA, record `checksum_mismatch` and refuse to overwrite;
   - if no local file, download the ZIP into memory with retry policy;
   - verify in-memory SHA == companion SHA; on mismatch record `checksum_mismatch`;
   - stage-write to `<final>.tmp`, fsync (where supported), atomic-rename to final path;
   - write paired `.sha256` sidecar in canonical Phase 4bb-F format;
   - run `inventory_and_validate_zip(...)` to compute `row_count`, `first_trade_time_ms`, `last_trade_time_ms`, `min_agg_trade_id`, `max_agg_trade_id`, and the row-sample validation result;
   - on success record `acquired_verified`; otherwise record explicit failure status.
4. Best-effort staging cleanup (suppressed `OSError`).

### 3.9 Inventory + row-sample validation

`inventory_and_validate_zip(zip_path, *, date_str)` decompresses the ZIP once and:

- runs `ZipFile.testzip()` and rejects on any corrupt member;
- requires exactly one CSV member;
- streams the CSV to count rows, capture min/max `agg_trade_id`, capture min/max `transact_time`, and accumulate head/tail row buffers (ROW_SAMPLE_HEAD = 100, ROW_SAMPLE_TAIL = 100);
- in a second streaming pass picks up to ROW_SAMPLE_MIDDLE = 100 deterministically-sampled middle rows (RNG seeded by `int(date_str.replace("-", ""))`);
- runs `validate_aggtrade_payload(...)` on every sampled row (head + tail + middle = up to 300 rows per ZIP);
- returns a `ZipInventory` record with `row_count`, `first_trade_time_ms`, `last_trade_time_ms`, `min_agg_trade_id`, `max_agg_trade_id`, `row_sample_validation_passed`, `row_sample_failure_reason`, `decompression_failure_reason`.

This is the bounded row-sample validation policy locked by Phase 4bl-B §11.5. **Full per-row validation is not run** in Phase 4bl-C; it is deferred to a future Phase 4bl-D-equivalent eligibility gate.

### 3.10 Failure policy

The retry / failure / missing-file policy is implemented in `_try_download_with_retry(...)` and the per-date branches of `acquire_one_date(...)`:

| Condition | Status | Retries | Action |
| --- | --- | --- | --- |
| HTTP 404 on `.zip` | `missing_404` | none | record and continue |
| HTTP 404 on `.CHECKSUM` | `checksum_companion_unavailable` | none | record and continue |
| HTTP 5xx / DNS / TCP / TLS / timeout | retry up to 3 times with backoff (2s/4s/8s + ±25% jitter); 60s per-attempt timeout; 5-min per-date budget | up to 3 | continue after exhaustion as `retry_exhausted` |
| Local SHA ≠ companion SHA | `checksum_mismatch` | none | delete staged ZIP, do not overwrite existing, continue |
| `ZipFile.testzip()` reports corruption | `decompression_failure` | none | preserve final ZIP (checksum-valid), continue |
| Row-sample validation row fails | `row_sample_validation_failure` | none | preserve ZIP, continue |
| Final move / sidecar write fails | `finalisation_failure` | none | record, continue |
| Existing fixture SHA mismatch | `checksum_mismatch` | none | **never overwrite**, continue |

No date is silently skipped; every date appears in `per_file_inventory` and the acquisition-log `events`. No date is substituted. No fallback to API. The orchestrator's `run_acquisition` returns `SUCCESSFUL_ACQUISITION` if all 90 dates are `acquired_verified`, `PARTIAL_ACQUISITION` if some failed, or `FAIL_CLOSED_NO_ACQUISITION` if every date failed.

### 3.11 Manifest / log writing

After all per-date results are collected, the orchestrator writes:

1. The acquisition log at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` via `write_acquisition_log(...)` (sorted-key JSON with trailing newline; deterministic content).
2. The acquisition log sidecar at `...json.sha256` via `make_sidecar_body(...)`.
3. The multi-day manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` via `write_multiday_manifest(...)` (sorted-key JSON; embedded acquisition-log SHA so the manifest pins the log content).
4. The manifest sidecar at `...json.sha256`.

The manifest's `governance_labels` block is exactly:

```json
{
  "feature_computation": "forbidden",
  "labels": "forbidden",
  "ml": "forbidden",
  "phase": "4bl-C",
  "source_phase_boundary": "4bl-B",
  "stop_trigger_domain": "trade_price_backtest_candidate",
  "strategy": "forbidden",
  "strategy_use": "forbidden",
  "symbol_scope_source": "archive_path",
  "validator": "phase_4ax_aggtrades_v001"
}
```

`research_eligible` is fixed to `false`; `eligibility_gate_status` is fixed to `"pending"`. Neither field can be flipped by Phase 4bl-C.

### 3.12 Fixture reuse logic

The existing-fixture branch (`date_str == EXISTING_FIXTURE_DATE` and the existing fixture is present) requires three independent SHA values to agree before reuse:

1. The recorded Phase 4az SHA `EXISTING_FIXTURE_SHA256 = "f560c2e5...2852b3e"` (hard-coded constant).
2. The fresh local SHA, computed by `sha256_file(final_zip)`.
3. The fresh companion SHA, parsed from the freshly downloaded `.CHECKSUM` companion.

If any pair disagrees, the script records `checksum_mismatch` for that date, leaves the existing fixture untouched, and continues. The script **does not** rewrite the existing fixture sidecar even if its canonical format is slightly different — it only verifies the embedded SHA prefix matches.

### 3.13 Offline tests

`tests/research/microstructure/test_phase4bl_c_acquisition_script.py` contains 71 offline tests that use `pytest.tmp_path` only and make zero network calls. Coverage groups: date list (6 tests), URL allowlist (5 tests including 13 parametrised forbidden URLs), path discipline (3 tests), sidecar format (5 tests), checksum parsing (4 tests including 6 parametrised bad inputs), SHA256 helpers (2 tests), atomic write (4 tests), capture-config hash (2 tests), ZIP inventory + row-sample validation (6 tests covering happy path, short archive, zero rows, multi-member, bad ZIP, invalid row), module-level guarantees (3 tests including static forbidden-import scan), `acquire_one_date(do_network=False)` (2 tests on existing-fixture mismatch and no-network/no-fixture), CLI dry-run + reject-output-outside-microstructure (2 tests), and JSON determinism (1 test verifying sorted-key emission, required keys, and locked governance values).

All 71 tests pass with `uv run pytest`. Whole-script ruff is clean.

---

## 4. Acquisition result

The acquisition orchestrator was invoked with:

```
uv run python scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py \
    --output-root data/microstructure
```

The orchestrator ran the locked 90-date list once, end-to-end, against `https://data.binance.vision` only. The full per-date inventory is recorded in the multi-day manifest's `per_file_inventory` field; the chronological event log is recorded in the acquisition log's `events` field.

### 4.1 Summary counters

Values below are verbatim from the on-disk multi-day manifest and acquisition log produced by the live run. All counters were also re-verified against the orchestrator's final stdout summary.

| Counter | Value | Source |
| --- | --- | --- |
| `expected_file_count` | 90 | manifest |
| `acquired_file_count` | 90 | manifest |
| `missing_file_count` | 0 | manifest |
| `checksum_mismatch_count` | 0 | manifest |
| `checksum_companion_unavailable_count` | 0 | log.summary |
| `decompression_failure_count` | 0 | manifest |
| `row_sample_validation_failure_count` | 0 | log.summary |
| `total_size_bytes` | 1,943,823,208 | manifest |
| `total_row_count` | 155,153,449 | manifest |
| `existing_fixture_reused` | true | log.summary |
| `existing_fixture_sha_match` | true | log.summary |
| `overall_status` | `SUCCESSFUL_ACQUISITION` | log (top-level) |
| `wall_clock_seconds` | 717 | log (top-level) |

Supplementary log evidence:

- `acquisition_run_id`: `phase-4bl-C-1778622616325-1080b925`
- `started_at_utc`: `2026-05-12T21:50:16.325000+00:00`
- `finished_at_utc`: `2026-05-12T22:02:13.858000+00:00`
- `errors` array length: 0
- `events` array length: 629 (1 `run_started`, 1 `run_finished`, 1 `date_skipped_existing_fixture`, 1 `existing_fixture_verified`, 179 `download_attempt`, 179 `download_success`, 89 `checksum_match`, 89 `finalisation_success`, 89 `sidecar_write`)
- `eligibility_gate_status_after_acquisition`: `pending` (lock preserved)
- `research_eligible_after_acquisition`: `false` (lock preserved)
- `non_authorizations_preserved`: `true`

### 4.2 Existing fixture handling

The `2025-01-15` Phase 4az fixture was detected at the canonical path. Its pre-acquisition SHA256 matched the recorded value `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` bit-for-bit. The fresh `.CHECKSUM` companion was downloaded and parsed; its value was cross-verified against the recorded SHA. The existing sidecar's SHA prefix was verified. The existing file was reused in place — no redownload of the ZIP itself was performed.

The existing fixture was not overwritten, modified, or rewritten in any way by Phase 4bl-C.

### 4.3 Failure handling

Any per-date failures are recorded explicitly in:

- the multi-day manifest's `per_file_inventory[].status` and `per_file_inventory[].failure_reason`;
- the acquisition log's `events` (per-event type) and `errors` array;
- the acquisition log's `summary` counters.

No date was silently skipped. No date was substituted. No fallback to APIs was attempted.

---

## 5. Local output inventory

All values below are from the on-disk live run and were independently re-verified via `sha256sum` + `wc -c` after the orchestrator finished.

| Artefact | Path | SHA256 | Size (bytes) |
| --- | --- | --- | --- |
| v002 multi-day manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | 105,052 |
| v002 manifest sidecar | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json.sha256` | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` | 111 |
| v002 acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | 302,055 |
| v002 log sidecar | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256` | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` | 127 |
| Raw zips (acquired this phase) | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/...` (31 dates), `.../2025/01/...` (31 dates including reused fixture), `.../2025/02/...` (28 dates) | per-date SHA recorded in manifest `per_file_inventory[].sha256` | 90 zips total; per-zip ~5–30 MB; aggregate `total_size_bytes` = 1,943,823,208 |
| Raw zip sidecars | same per-date directories; one `.zip.sha256` per zip in canonical Phase 4bb-F two-space-then-LF format | per-zip-sha matches paired zip; sidecar self-SHA not separately recorded | 90 sidecars; each ~80–100 bytes |

Sidecar body format (verified live):

```
<sha256_lowercase_hex>  <basename>
```

with exactly two spaces between the hash and the basename and a single trailing line-feed.

All local outputs are gitignored under `.gitignore:85: data/microstructure/`. `git check-ignore --verbose` was rerun against `data/microstructure/`, `data/microstructure/manifests/`, `data/microstructure/raw/`, the new v002 manifest, the manifest sidecar, the acquisition log, the log sidecar, and a representative `2024/12` raw zip path; every check returned `.gitignore:85: data/microstructure/`. None of these outputs are staged or committed. They are reproducible from the public archive at any time by re-running the orchestrator script.

---

## 6. Validation commands and results

### 6.1 Pre-state verification

```
git rev-parse main          -> da9d830c2b900c1c5fa09159e79ce2f0b6bbe249
git rev-parse origin/main   -> da9d830c2b900c1c5fa09159e79ce2f0b6bbe249
git status                  -> clean (untracked: .claude/scheduled_tasks.lock, data/research/)
git log --oneline -12 ...   -> Phase 4bl-B chain through Phase 4bj-K
```

### 6.2 Script validation

```
python -m py_compile scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py   -> OK
python -m py_compile tests/research/microstructure/test_phase4bl_c_acquisition_script.py  -> OK
uv run ruff check scripts/phase4bl_c_*.py tests/research/microstructure/test_phase4bl_c_*.py  -> All checks passed!
uv run pytest tests/research/microstructure/test_phase4bl_c_acquisition_script.py  -> 71 passed
```

CLI dry-run:

```
uv run python scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py --dry-run
Phase 4bl-C dry-run plan:
  symbols        : ('BTCUSDT',)
  date_start     : 2024-12-01
  date_end       : 2025-02-28
  date_count     : 90
  url_template   : https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-{date}.zip
  output_root    : C:\Prometheus\data\microstructure
  manifest_path  : C:\Prometheus\data\microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json
  log_path       : C:\Prometheus\data\microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json
  first_3_dates  : ['2024-12-01', '2024-12-02', '2024-12-03']
  last_3_dates   : ['2025-02-26', '2025-02-27', '2025-02-28']
No download will be performed.
```

### 6.3 Gitignore coverage verification (pre-run)

```
git check-ignore -v data/microstructure/                                            -> .gitignore:85
git check-ignore -v data/microstructure/raw/                                        -> .gitignore:85
git check-ignore -v data/microstructure/manifests/                                  -> .gitignore:85
git check-ignore -v data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/BTCUSDT-aggTrades-2024-12-01.zip -> .gitignore:85
git check-ignore -v data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json -> .gitignore:85
git check-ignore -v data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json -> .gitignore:85
```

### 6.4 Acquisition execution

```
uv run python scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py --output-root data/microstructure

[1/90] 2024-12-01 ... acquired_verified
[2/90] 2024-12-02 ... acquired_verified
[3/90] 2024-12-03 ... acquired_verified
... (per-date lines emitted for each of the 90 dates) ...
[46/90] 2025-01-15 ... acquired_verified   (existing Phase 4az fixture reused in place)
... (continues) ...
[90/90] 2025-02-28 ... acquired_verified
```

Final orchestrator stdout summary (verbatim):

```
Phase 4bl-C: SUCCESSFUL_ACQUISITION
  acquired                        : 90
  missing_404                     : 0
  checksum_mismatch               : 0
  checksum_companion_unavailable  : 0
  decompression_failure           : 0
  row_sample_validation_failure   : 0
  finalisation_failure            : 0
  retry_exhausted                 : 0
  manifest_path                   : C:\Prometheus\data\microstructure\manifests\microstructure_raw_aggtrades_v001__v002.json
  manifest_sha256                 : 016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485
  acquisition_log_path            : C:\Prometheus\data\microstructure\manifests\microstructure_raw_aggtrades_v001__v002_acquisition_log.json
  acquisition_log_sha256          : 52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314
  total_size_bytes                : 1943823208
  total_row_count                 : 155153449
  wall_clock_seconds              : 717
```

Cross-checks performed after the orchestrator returned:

- recomputed manifest SHA via `sha256sum` matched `016967865c97…1d87485` bit-for-bit;
- recomputed acquisition log SHA via `sha256sum` matched `52f6d7fb3cb0…0c6b314` bit-for-bit;
- manifest's embedded `acquisition_log_sha256` field equalled the recomputed log SHA bit-for-bit;
- manifest sidecar body parsed under the canonical two-space format and the embedded SHA equalled the recomputed manifest SHA bit-for-bit;
- log sidecar body parsed under the canonical two-space format and the embedded SHA equalled the recomputed log SHA bit-for-bit;
- manifest `per_file_inventory` length equalled 90;
- every entry in `per_file_inventory` carried a non-null `date` and a `status` value of `acquired_verified`;
- the `2025-01-15` entry's `sha256` equalled the recorded Phase 4az fixture SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` bit-for-bit; the entry's `sha256_from_companion` also equalled that value (three-way agreement: recorded ↔ fresh-local ↔ fresh-companion);
- the `2025-01-15` entry's `size_bytes` equalled the recorded `21271119` and `row_count` equalled the recorded `1681098`.

### 6.5 Post-acquisition verification

After the orchestrator finished, the operator (Claude Code) verified:

- the manifest path and sidecar exist with byte-identical SHAs to the orchestrator's reported values;
- the acquisition log path and sidecar exist with byte-identical SHAs;
- the manifest's embedded `acquisition_log_sha256` matches the on-disk acquisition log file's recomputed SHA bit-for-bit;
- the manifest's `per_file_inventory` length equals 90;
- every entry in `per_file_inventory` has a non-null `date` and a valid `status` from the locked status enum;
- the existing fixture's recorded SHA matches the per-file-inventory SHA for `2025-01-15`;
- raw artefact pre/post immutability (all values byte-identical):
  - Phase 4az raw zip SHA `f560c2e5...`;
  - Phase 4az raw v001 manifest SHA `a371edd4...`;
  - Phase 4bb-D gate report SHA `96f09159...`;
  - Phase 4bf gate report SHA `dd4e0c1c...`;
  - Phase 4bg-B successor-state SHA `8bcc7d01...`;
  - Phase 4bh feature parquet SHA `618d9b86...`;
  - Phase 4bh feature manifest SHA `624e8c5e...`;
  - Phase 4bi-B feature gate report SHA `aa5d29c2...`;
  - Phase 4bi-D feature successor-state SHA `8176aa3f...`;
  - Phase 4bj-C label parquet SHA `ef50038a...`;
  - Phase 4bj-C label manifest SHA `181a799c...`;
  - Phase 4bj-E label gate report SHA `b0b5405b...`;
  - Phase 4bj-G label successor-state SHA `ce7d3917...`;
  - Phase 4bj-J no-split determination SHA `7e461eb5...`;
  - Phase 4bb-G raw successor-state SHA `ab6a82e7...`.

### 6.6 Final `git status`

Immediately before staging the Phase 4bl-C tracked files, `git status` showed only the four new Phase 4bl-C deliverables plus the pre-existing always-untracked entries:

```
git status
On branch phase-4bl-c/multi-day-aggtrades-acquisition-execution
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/scheduled_tasks.lock
	data/research/
	docs/00-meta/implementation-reports/2026-05-12_phase-4bl-c_closeout.md
	docs/00-meta/implementation-reports/2026-05-12_phase-4bl-c_multi-day-aggtrades-acquisition-execution.md
	scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py
	tests/research/microstructure/test_phase4bl_c_acquisition_script.py

nothing added to commit but untracked files present (use "git add" to track)
```

After the documentation update to `docs/00-meta/current-project-state.md` and the final Phase 4bl-C commit, `git status` reduces to:

```
git status
On branch phase-4bl-c/multi-day-aggtrades-acquisition-execution
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/scheduled_tasks.lock
	data/research/

nothing added to commit but untracked files present (use "git add" to track)
```

The only untracked entries are then the always-untracked `.claude/scheduled_tasks.lock` and the gitignored `data/research/` directory. No `data/microstructure/` artefact is staged or tracked at any point. `git check-ignore --verbose` on any `data/microstructure/...` path returns `.gitignore:85: data/microstructure/`.

---

## 7. Boundary confirmations

| Boundary | Confirmation |
| --- | --- |
| No data/microstructure artefact committed | True (all under `.gitignore:85`) |
| No normalization | True (no normalized parquet created) |
| No features | True (no feature dataset created) |
| No labels | True (no label dataset created) |
| No gates | True (no gate report created) |
| No successor-state | True (no successor-state artefact created) |
| No diagnostics | True (no diagnostic artefact created) |
| No ML | True (no ML model created or trained) |
| No strategy | True (no strategy artefact created) |
| No backtest | True (no backtest artefact created) |
| No authenticated API | True (no authenticated endpoint contacted) |
| No private endpoint | True (no private endpoint contacted) |
| No WebSocket | True (no WebSocket opened) |
| No credentials | True (no credentials read or generated) |
| No `.env` | True (no `.env` read or created) |
| No `.mcp.json` | True (no `.mcp.json` read or created) |
| No MCP | True (MCP not used) |
| No Graphify | True (Graphify not used) |
| No manifest transition | True (existing manifests unchanged; new v002 manifest is `research_eligible=false`, `eligibility_gate_status="pending"`) |
| No `research_eligible` flip | True (`flip_research_eligible(...)` not invoked) |
| No `eligibility_gate_status` transition | True (no manifest's status changed) |
| No `chronological_split_policy` change | True (label manifest's `chronological_split_policy="not_yet_defined"` is unchanged) |
| `pyproject.toml` unchanged | True |
| `README.md` unchanged | True |
| `.gitignore` unchanged | True |
| `.gitattributes` unchanged | True |
| MCP files unchanged | True |
| No existing manifest modified | True |
| No existing sidecar modified | True |
| Existing Phase 4az fixture byte-identical | True (recorded SHA == fresh local SHA == fresh companion SHA) |
| Existing v001 manifest byte-identical | True |
| Existing Phase 4bb-D gate report byte-identical | True |
| Existing Phase 4bd derived artefacts byte-identical | True |
| Existing Phase 4bf gate report byte-identical | True |
| Existing Phase 4bg-B successor-state byte-identical | True |
| Existing Phase 4bh feature artefacts byte-identical | True |
| Existing Phase 4bi-B gate report byte-identical | True |
| Existing Phase 4bi-D successor-state byte-identical | True |
| Existing Phase 4bj-C label artefacts byte-identical | True |
| Existing Phase 4bj-E label gate report byte-identical | True |
| Existing Phase 4bj-G label successor-state byte-identical | True |
| Existing Phase 4bj-J no-split determination byte-identical | True |
| Existing Phase 4bb-G raw successor-state byte-identical | True |
| Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved | True (never invoked) |
| Phase 4ak M0 twelve-clause gate preserved | True (not invoked; not amended) |
| Phase 4ak post-null cooldown rule preserved | True |
| Phase 4ak cooled-down families list preserved | True |
| Phase 4al refined no-rescue rule preserved | True (no rescue of R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread) |
| Phase 4bb-F canonical path policy preserved | True (raw zips under `data/microstructure/raw/...`; manifests under `data/microstructure/manifests/...`; sidecars in `<sha>  <basename>\n` format) |
| Retained verdict ledger preserved verbatim | True (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1) |
| Project locks preserved verbatim | True (§11.6 = 8 bps per side, round-trip 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w) |

---

## 8. Recommended state

### 8.1 Primary recommendation

**Remain paused after branch completion.** Phase 4bl-C is branch-complete only; per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main`.

### 8.2 Conditional next, NOT authorized

The natural conditional successor to Phase 4bl-C is **Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate / Raw QA**, which would translate the Phase 4bb-D raw-eligibility-gate pattern into a v002-multi-day analogue, run a comprehensive 45-check eligibility gate over the 90-day inventory + manifest pair, and emit one gate report under `data/microstructure/gate-reports/raw/` (Phase 4bb-F canonical path policy). Phase 4bl-D is **not** authorized by Phase 4bl-C. It requires a separate operator authorization prompt.

A future Phase 4bl-D would be expected to verify, for each of the 90 dates:

- the raw zip exists at the canonical Phase 4bb-F path with matching SHA;
- the raw zip sidecar matches in canonical format;
- the zip is decompressible to a single CSV member;
- the CSV row count, time bounds, and agg-id monotonicity match the manifest's recorded values;
- full per-row validation via `validate_aggtrade_payload(...)` (not the bounded row-sample done in Phase 4bl-C);
- no duplicate `agg_trade_id` across rows;
- no out-of-day timestamps;
- no overlapping date ranges with other dates;
- no implausible price / quantity values.

A future Phase 4bl-D could emit a 45-check gate report similar to the Phase 4bb-D PASS report (`microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`, SHA `96f09159...`, 45 / 45 PASS, `research_eligible_after=False`, `no_successor_authorization=True`). The Phase 4bl-D gate report would also have `research_eligible_after=False` (because raw families are permanently `research_eligible=false` per Phase 4bb-E), and would set `eligibility_gate_status_after="pass_report_level_only"` for the v002 manifest as report-level recommendation only.

Phase 4bl-C does not authorize Phase 4bl-D. Phase 4bl-C does not authorize Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

### 8.3 Strict stop point

Phase 4bl-C branch work stops here. The next step is operator review and merge of the Phase 4bl-C branch into `main`, followed by recording the Phase 4bl-C merge-closeout. Phase 4bl-D is NOT authorized by this memo and must be the subject of a separate operator prompt.

---

**End of Phase 4bl-C implementation report.**
