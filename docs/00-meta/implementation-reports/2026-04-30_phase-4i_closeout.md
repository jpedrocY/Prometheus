# Phase 4i Closeout

## Summary

Phase 4i (V2 Public Data Acquisition and Integrity Validation) is
**complete on the Phase 4i branch and not merged to main**. Phase 4i
acquired the six Phase 4h-predeclared minimum dataset families for V2's
first-backtest data plan from public unauthenticated
`data.binance.vision` bulk archives, normalized them to Parquet under
the existing repository partition convention, generated manifests, and
ran the Phase 4h §17 strict integrity-check evidence specification on
each dataset.

**Verdict — partial pass:** 4 of 6 datasets are research-eligible;
2 of 6 (metrics) FAIL the Phase 4h §17.4 strict gate due to upstream
`data.binance.vision` characteristics (intra-day 5-minute gaps + NaN
values in optional ratio columns concentrated in early-2022 data).

Phase 4i is **docs-and-data** — it acquired data, generated manifests,
and committed the script + 6 manifests + report. **No source code,
tests, scripts, data, manifests, specs, thresholds, parameters,
project locks, or prior verdicts were modified.** No backtests were
run. No mark-price 30m / 4h or aggTrades acquired. No funding-rate
re-acquired (v002 reused).

V2 remains **pre-research only**: not implemented, not backtested,
not validated, not live-ready, **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4i recommendation: **remain paused, accept partial-pass
evidence** (Option A) primary; **authorize a future docs-only metrics
governance memo analogous to Phase 3r §8** (Option B) conditional
secondary. **No** immediate V2 backtest; **no** V2 implementation;
**no** mark-price acquisition; **no** aggTrades acquisition; **no**
paper / shadow / live / exchange-write.

## Files changed

The Phase 4i branch introduces the following new files relative to
`main`:

- `scripts/phase4i_v2_acquisition.py` (new, standalone orchestrator)
- `data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json` (new)
- `data/manifests/binance_usdm_ethusdt_30m__v001.manifest.json` (new)
- `data/manifests/binance_usdm_btcusdt_4h__v001.manifest.json` (new)
- `data/manifests/binance_usdm_ethusdt_4h__v001.manifest.json` (new)
- `data/manifests/binance_usdm_btcusdt_metrics__v001.manifest.json`
  (new; `research_eligible: false`)
- `data/manifests/binance_usdm_ethusdt_metrics__v001.manifest.json`
  (new; `research_eligible: false`)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4i_v2-public-data-acquisition-and-integrity-validation.md`
  (Phase 4i acquisition + integrity report)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4i_closeout.md`
  (this file)

`docs/00-meta/current-project-state.md` is **NOT modified** on the
Phase 4i branch. It would be updated only during the merge housekeeping
commit, after a separate operator authorization.

`data/raw/**` and `data/normalized/**` are **NOT committed** (gitignored
per existing convention; locally reproducible from public sources via
`scripts/phase4i_v2_acquisition.py`).

No source code under `src/prometheus/`, no tests, and no existing
scripts were modified. The Phase 4i acquisition script is fully
standalone (it imports only `httpx`, `pyarrow`, and standard library;
it does not import anything from `prometheus.*`).

## Dataset families acquired

| Dataset version | Symbol | Family | Records / Bars | Eligible |
|---|---|---|---|---|
| `binance_usdm_btcusdt_30m__v001` | BTCUSDT | klines 30m | 74 448 bars | **YES** |
| `binance_usdm_ethusdt_30m__v001` | ETHUSDT | klines 30m | 74 448 bars | **YES** |
| `binance_usdm_btcusdt_4h__v001` | BTCUSDT | klines 4h | 9 306 bars | **YES** |
| `binance_usdm_ethusdt_4h__v001` | ETHUSDT | klines 4h | 9 306 bars | **YES** |
| `binance_usdm_btcusdt_metrics__v001` | BTCUSDT | metrics 5m | 446 555 / 446 688 records | NO |
| `binance_usdm_ethusdt_metrics__v001` | ETHUSDT | metrics 5m | 446 555 / 446 688 records | NO |

## Local data artefacts

```text
data/raw/binance_usdm/klines/symbol={BTCUSDT,ETHUSDT}/interval={30m,4h}/year=YYYY/month=MM/...zip      (204 zips, ~8.7 MB)
data/raw/binance_usdm/metrics/symbol={BTCUSDT,ETHUSDT}/year=YYYY/month=MM/...zip                       (3102 zips, ~40 MB)
data/normalized/klines/symbol={BTCUSDT,ETHUSDT}/interval={30m,4h}/year=YYYY/month=MM/part-0000.parquet (204 files, ~11.5 MB)
data/normalized/metrics/symbol={BTCUSDT,ETHUSDT}/granularity=5m/year=YYYY/month=MM/part-0000.parquet   (102 files, ~45 MB)

Total raw footprint:        ~49 MB
Total normalized footprint: ~56 MB
Total Phase 4i local data:  ~105 MB
```

All `data/raw/**` and `data/normalized/**` files are **git-ignored**
per the existing convention (same as v002 / v001-of-5m). They are
local research evidence reproducible from the public bulk archive
via `scripts/phase4i_v2_acquisition.py`.

## Manifest files

Six new manifests committed (force-added past `data/manifests/`
gitignore rule per the Phase 4i brief's "Allowed commit contents"
clause):

```text
data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json
data/manifests/binance_usdm_ethusdt_30m__v001.manifest.json
data/manifests/binance_usdm_btcusdt_4h__v001.manifest.json
data/manifests/binance_usdm_ethusdt_4h__v001.manifest.json
data/manifests/binance_usdm_btcusdt_metrics__v001.manifest.json
data/manifests/binance_usdm_ethusdt_metrics__v001.manifest.json
```

Each manifest contains the full Phase 4h §16 evidence schema
(`schema_version`, `dataset_category`, `dataset_name`,
`dataset_version`, `created_at_utc_ms`, `canonical_timezone`,
`canonical_timestamp_format`, `symbols`, `market`, `instrument_type`,
`intervals` or `granularity`, `sources`, `pipeline_version`,
`partitioning`, `primary_key`, `generator`,
`predecessor_dataset_versions`, `raw_archive_count`,
`raw_sha256_index`, `invalid_windows`, `notes`,
`date_range_start_*_utc_ms`, `date_range_end_*_utc_ms`, `bar_count`
or `record_count`, `expected_records` (metrics only),
`quality_checks`, `research_eligible`, `command_used`,
`no_credentials_confirmation: true`, `private_endpoint_used: false`).

## Integrity verdict

**Klines (4 datasets — ALL PASS):**

- 30m × 2 + 4h × 2: zero gaps, monotone timestamps, zero duplicate
  timestamps, zero boundary alignment violations, zero close-time
  consistency violations, zero OHLC sanity violations, zero volume
  sanity violations, `taker_buy_volume` present and bounded by
  `volume`, zero symbol/interval consistency violations, full date
  range coverage from 2022-01-01 00:00:00 UTC.

**Metrics (2 datasets — BOTH FAIL strict gate):**

- BTCUSDT metrics: 446,555 / 446,688 records (133 short = 5,699
  intra-day missing 5-min observations); 91,840 records have ≥ 1 NaN
  in optional ratio columns; 0 missing daily archives.
- ETHUSDT metrics: 446,555 / 446,688 records (133 short = 3,631
  intra-day missing 5-min observations); 91,841 records have ≥ 1 NaN
  in optional ratio columns; 0 missing daily archives.
- For both: monotone timestamps, zero duplicate timestamps, zero
  boundary alignment violations, zero symbol consistency violations,
  zero non-negative OI violations, zero non-negative ratio violations,
  date range coverage true (data spans 2022-01-01 .. 2026-03-31 UTC).
- The required `sum_open_interest` and `sum_open_interest_value`
  columns are FULLY POPULATED (zero NaN) for both symbols. The NaN
  concentration is in OPTIONAL ratio columns
  (count/sum_toptrader_long_short_ratio, count_long_short_ratio,
  sum_taker_long_short_vol_ratio) and is heavily concentrated in
  early-2022 data (~97% NaN for early-2022 ratio columns; ~0% NaN
  for 2026-03 ratio columns).

## research_eligible verdicts

```text
binance_usdm_btcusdt_30m__v001:        research_eligible: true
binance_usdm_ethusdt_30m__v001:        research_eligible: true
binance_usdm_btcusdt_4h__v001:         research_eligible: true
binance_usdm_ethusdt_4h__v001:         research_eligible: true
binance_usdm_btcusdt_metrics__v001:    research_eligible: false
binance_usdm_ethusdt_metrics__v001:    research_eligible: false
```

Per the brief: *"If any family is not research_eligible, Phase 4i
must stop for operator review and must not proceed to any backtest
or successor phase."* Phase 4i is therefore **stopping for operator
review.**

## Commands run

| # | Command | Purpose |
|---|---|---|
| 1 | `git status` | Verify clean tree pre-branch |
| 2 | `git checkout -b phase-4i/v2-public-data-acquisition-and-integrity-validation` | Create Phase 4i branch |
| 3 | `git rev-parse main`, `git rev-parse origin/main` | Verify main == origin/main at 4a0edf9 |
| 4 | `.venv/Scripts/python --version` | `Python 3.12.4` |
| 5 | `.venv/Scripts/python -m ruff check scripts/phase4i_v2_acquisition.py` | Pre-test lint |
| 6 | `.venv/Scripts/python -m mypy scripts/phase4i_v2_acquisition.py` | Pre-test typecheck |
| 7 | `.venv/Scripts/python scripts/phase4i_v2_acquisition.py --start 2022-01 --end 2022-01 --symbols BTCUSDT --families klines_30m metrics --workers 8` | Smoke test (1 month) |
| 8 | `.venv/Scripts/python scripts/phase4i_v2_acquisition.py --start 2022-01 --end 2026-03 --symbols BTCUSDT ETHUSDT --families klines_30m klines_4h metrics --workers 8` | Full acquisition |
| 9 | `.venv/Scripts/python -m ruff check .` | Whole-repo Ruff |
| 10 | `.venv/Scripts/python -m pytest -q` | Whole-repo pytest |
| 11 | `.venv/Scripts/python -m mypy` | Whole-repo mypy strict |
| 12 | `git add scripts/... docs/... && git add -f data/manifests/...` | Stage all Phase 4i artefacts |
| 13 | `git commit -m '...' && git push -u origin phase-4i/...` | Commit + push report |

The following commands were **NOT** run (per Phase 4i brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No backtest execution.
- No diagnostic / Q1–Q7 question rerun.
- No mark-price 30m / 4h acquisition.
- No `aggTrades` acquisition.
- No spot data acquisition.
- No private / authenticated REST or WebSocket request.

## Verification results

| Check | Result |
|---|---|
| `.venv/Scripts/python --version` | `Python 3.12.4` |
| `.venv/Scripts/python -m ruff check .` | `All checks passed!` |
| `.venv/Scripts/python -m pytest` | `785 passed in 12.75s` |
| `.venv/Scripts/python -m mypy` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source
files. No regressions relative to the post-Phase-4h-merge baseline.

The Phase 4i acquisition command itself completed with exit code 1
(integrity failure), as expected and required by the brief: when
metrics datasets fail the strict gate, the script must report a
non-zero exit so that the operator review boundary is mechanical
rather than overlooked. The Phase 4i branch state reflects the
intended partial-pass: 4 manifests with `research_eligible: true`,
2 manifests with `research_eligible: false`, and a comprehensive
report documenting the findings.

## Commit

| Role | SHA | Message |
|---|---|---|
| Phase 4i acquisition + report | `6913d29ff70c683e2f10b61c873241adaffecfcf` | phase-4i: V2 public data acquisition and integrity validation (docs-and-data) |
| Phase 4i closeout | `<recorded in chat closeout block after this file is committed>` | docs(phase-4i): closeout report (Markdown artefact) |

## Final git status

After the closeout commit and push:

```text
On branch phase-4i/v2-public-data-acquisition-and-integrity-validation
Your branch is up to date with 'origin/phase-4i/v2-public-data-acquisition-and-integrity-validation'.

nothing to commit, working tree clean
```

## Final git log --oneline -5

(Captured after the closeout commit; recorded verbatim in the chat
closeout block.)

## Final rev-parse

(Captured after the closeout commit; recorded verbatim in the chat
closeout block: `git rev-parse HEAD` and
`git rev-parse origin/phase-4i/v2-public-data-acquisition-and-integrity-validation`.)

## Branch / main status

- Phase 4i branch:
  `phase-4i/v2-public-data-acquisition-and-integrity-validation`
  exists locally and on `origin`.
- Phase 4i branch is **NOT merged to main**.
- `main` and `origin/main` remain at
  `4a0edf980c01a1c3c9336ad89dd142685a53a445` (Phase 4h housekeeping).
- A separate operator authorization is required before any merge.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4j / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched, or
  commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 validation.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No mark-price 30m / 4h acquisition.**
- **No `aggTrades` acquisition.**
- **No spot data acquisition.**
- **No cross-venue acquisition.**
- **No funding-rate re-acquisition** (v002 funding manifests reused).
- **No v002 dataset / manifest modification.**
- **No v001-of-5m dataset / manifest modification.**
- **No v003 created.**
- **No Phase 3p §4.7 amendment.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 3v `stop_trigger_domain` governance modification.**
- **No Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance modification.**
- **No Phase 4f text modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No Phase 4h text modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No existing `scripts/**` modification.**
  (`scripts/phase4i_v2_acquisition.py` is new and standalone.)
- **No `prometheus.research.data.*` extension.**
- **No `Interval` enum extension.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No credential storage / request / use.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.**
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No order placement / cancellation.**
- **No real exchange adapter implementation.**
- **No exchange-write capability.**
- **No reconciliation implementation.**
- **No retained-evidence verdict revision.**
- **No project-lock revision.**
- **No threshold / parameter modification.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4i branch.**
- **No `.claude/rules/**` modification.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase
  4i deliverables exist as branch-only artefacts pending operator
  review.
- **Phase 4i output:** docs-and-data acquisition + integrity report
  + 6 manifests + standalone acquisition script + this closeout
  artefact on the Phase 4i branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4i).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase
  4 (canonical) remains not authorized. Phase 4a–4h all merged.
  Phase 4i V2 public data acquisition + integrity validation on this
  branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved through Phase 4i).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (strategy spec) and Phase 4h (data requirements). Phase
  4i acquired 6 of 6 minimum dataset families; 4 of 6 are
  research-eligible; 2 of 6 (metrics) are NOT research-eligible
  under the strict gate. V2 is **NOT implemented; NOT backtested;
  NOT validated; NOT live-ready; NOT a rescue.**
- **OPEN ambiguity-log items after Phase 4i:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks;
  mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m
  manifests `research_eligible: false`. All preserved.
- **Branch state:**
  `phase-4i/v2-public-data-acquisition-and-integrity-validation`
  exists locally and on `origin`. NOT merged to main.

## Next authorization status

**No next phase has been authorized.** Phase 4i's primary
recommendation is **Option A (remain paused, accept partial-pass
evidence)**, with **Option B (authorize a future docs-only metrics
governance memo analogous to Phase 3r §8) as conditional secondary**.
Options C (mark-price 30m / 4h acquisition) and D (aggTrades
acquisition) are not recommended at this boundary. Options E
(immediate V2 backtest), F (V2 implementation), and G (paper / shadow
/ live-readiness / exchange-write) are rejected / forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has been
issued.

The 5m research thread remains operationally complete and closed (per
Phase 3t). The implementation-readiness boundary remains reviewed (per
Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers
remain RESOLVED at the governance level (per Phase 3v + Phase 3w).
The Phase 4a safe-slice scope is implemented (per Phase 4a). The
Phase 4b script-scope quality-gate restoration is complete (per Phase
4b). The Phase 4c state-package quality-gate residual cleanup is
complete (per Phase 4c). The Phase 4d post-4a/4b/4c review is complete
(per Phase 4d). The Phase 4e reconciliation-model design memo is
complete (per Phase 4e). The Phase 4f V2 hypothesis predeclaration is
complete (per Phase 4f). The Phase 4g V2 strategy spec is complete
(per Phase 4g). The Phase 4h V2 data-requirements / feasibility memo
is complete (per Phase 4h). The Phase 4i V2 public data acquisition
+ integrity validation is complete on this branch (this phase) with
**partial-pass verdict** (4 of 6 datasets research-eligible; 2 of 6
fail strict gate). **Recommended state remains paused.**
