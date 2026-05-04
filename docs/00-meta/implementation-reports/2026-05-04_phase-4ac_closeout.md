# Phase 4ac Closeout

## Summary

Phase 4ac authored `scripts/phase4ac_alt_symbol_acquisition.py` and acquired the predeclared Phase 4ab core alt-symbol public datasets from public unauthenticated `data.binance.vision` bulk archives only. **Phase 4ac is docs-and-data acquisition / integrity validation only.** Phase 4ac acquired 35 dataset families (52 monthly archives each = 1 820 monthly archives total, all SHA256-verified against `.CHECKSUM` companions) for the core symbol set BTCUSDT / ETHUSDT / SOLUSDT / XRPUSDT / ADAUSDT (with 10 (symbol, family, interval) tuples skipped because committed Phase 2 / Phase 3q / Phase 4i `__v001` manifests already cover them). Of the 35 newly-written manifests, 9 PASSED the Phase 3p §4.7 / Phase 4h §17 strict integrity gate (`research_eligible: true`) and 26 FAILED with documented invalid-window / gap evidence (`research_eligible: false`; no patching, no forward-fill, no interpolation, no imputation, no silent omission). **No backtest run. No diagnostic run. No Q1–Q7 rerun. No new strategy candidate created. No hypothesis-spec memo, strategy-spec memo, or backtest-plan memo created. No `src/prometheus/`, tests, or existing scripts modified. No existing manifests modified. No retained verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update). No authenticated APIs / private endpoints / public-endpoint code calls / user stream / WebSocket / listenKey / credentials / `.env` / MCP / Graphify / `.mcp.json` touched.** **No successor phase authorized.** **Phase 4z, Phase 4aa admissibility framework, Phase 4ab recommendations, and Phase 4ac results all remain recommendations / data evidence only and are NOT adopted as binding governance.**

## Phase 4ac title

**Phase 4ac — Alt-Symbol Public Data Acquisition and Integrity Validation** (docs-and-data, standalone-script mode).

## Branch

`phase-4ac/alt-symbol-public-data-acquisition`

## Base main SHA

`9db120741413ec9cb5b02ffd9622d0f43a1d8c57`

## Files created

```text
scripts/phase4ac_alt_symbol_acquisition.py  (new; standalone orchestrator;
                                              public bulk archives only;
                                              ruff clean; py compile clean)

docs/00-meta/implementation-reports/2026-05-04_phase-4ac_alt-symbol-public-data-acquisition.md
                                            (new; main report)
docs/00-meta/implementation-reports/2026-05-04_phase-4ac_closeout.md
                                            (new; this file)

35 manifests under data/manifests/ (new):
  binance_usdm_btcusdt_1h__v001.manifest.json                 [research_eligible=true]
  binance_usdm_btcusdt_markprice_30m__v001.manifest.json      [research_eligible=false]
  binance_usdm_btcusdt_markprice_1h__v001.manifest.json       [research_eligible=false]
  binance_usdm_btcusdt_markprice_4h__v001.manifest.json       [research_eligible=false]
  binance_usdm_ethusdt_1h__v001.manifest.json                 [research_eligible=true]
  binance_usdm_ethusdt_markprice_30m__v001.manifest.json      [research_eligible=false]
  binance_usdm_ethusdt_markprice_1h__v001.manifest.json       [research_eligible=false]
  binance_usdm_ethusdt_markprice_4h__v001.manifest.json       [research_eligible=false]
  binance_usdm_solusdt_15m__v001.manifest.json                [research_eligible=false]
  binance_usdm_solusdt_30m__v001.manifest.json                [research_eligible=false]
  binance_usdm_solusdt_1h__v001.manifest.json                 [research_eligible=false]
  binance_usdm_solusdt_4h__v001.manifest.json                 [research_eligible=false]
  binance_usdm_solusdt_markprice_15m__v001.manifest.json      [research_eligible=false]
  binance_usdm_solusdt_markprice_30m__v001.manifest.json      [research_eligible=false]
  binance_usdm_solusdt_markprice_1h__v001.manifest.json       [research_eligible=false]
  binance_usdm_solusdt_markprice_4h__v001.manifest.json       [research_eligible=false]
  binance_usdm_solusdt_funding__v001.manifest.json            [research_eligible=true]
  binance_usdm_xrpusdt_15m__v001.manifest.json                [research_eligible=false]
  binance_usdm_xrpusdt_30m__v001.manifest.json                [research_eligible=false]
  binance_usdm_xrpusdt_1h__v001.manifest.json                 [research_eligible=false]
  binance_usdm_xrpusdt_4h__v001.manifest.json                 [research_eligible=false]
  binance_usdm_xrpusdt_markprice_15m__v001.manifest.json      [research_eligible=false]
  binance_usdm_xrpusdt_markprice_30m__v001.manifest.json      [research_eligible=false]
  binance_usdm_xrpusdt_markprice_1h__v001.manifest.json       [research_eligible=false]
  binance_usdm_xrpusdt_markprice_4h__v001.manifest.json       [research_eligible=false]
  binance_usdm_xrpusdt_funding__v001.manifest.json            [research_eligible=true]
  binance_usdm_adausdt_15m__v001.manifest.json                [research_eligible=true]
  binance_usdm_adausdt_30m__v001.manifest.json                [research_eligible=true]
  binance_usdm_adausdt_1h__v001.manifest.json                 [research_eligible=true]
  binance_usdm_adausdt_4h__v001.manifest.json                 [research_eligible=true]
  binance_usdm_adausdt_markprice_15m__v001.manifest.json      [research_eligible=false]
  binance_usdm_adausdt_markprice_30m__v001.manifest.json      [research_eligible=false]
  binance_usdm_adausdt_markprice_1h__v001.manifest.json       [research_eligible=false]
  binance_usdm_adausdt_markprice_4h__v001.manifest.json       [research_eligible=false]
  binance_usdm_adausdt_funding__v001.manifest.json            [research_eligible=true]
```

## Files updated

```text
docs/00-meta/current-project-state.md  (narrow Phase 4ac paragraph addition;
                                         no broad refresh)
```

## Scripts created

```text
scripts/phase4ac_alt_symbol_acquisition.py   (standalone orchestrator;
                                               idempotent; public bulk only;
                                               no credentials; no .env;
                                               no authenticated REST;
                                               no private endpoints;
                                               no public-endpoint code calls;
                                               no WebSocket; no user stream;
                                               no listenKey;
                                               no exchange-write;
                                               no MCP / Graphify / .mcp.json;
                                               no prometheus.runtime imports;
                                               ruff clean; py compileall clean)
```

## Manifests created

35 manifests committed under `data/manifests/`. Each manifest follows existing
repository convention with these fields populated:

```text
schema_version, dataset_category, dataset_name, dataset_version,
created_at_utc_ms, canonical_timezone, canonical_timestamp_format,
symbols, market, instrument_type, intervals, sources, pipeline_version,
partitioning, primary_key, generator, predecessor_dataset_versions,
invalid_windows, notes, listing_first_month_utc, end_month_utc,
months_404, middle_gap_months, date_range_start_open_time_utc_ms,
date_range_end_open_time_utc_ms, bar_count or record_count,
raw_archive_count, raw_sha256_index, quality_checks, research_eligible,
partial_eligibility, known_exclusions, governance_references,
operator_authorization_ref, command_used, no_credentials_confirmation,
private_endpoint_used, authenticated_api_used, websocket_used,
user_stream_used, exchange_write_attempted
```

## Raw / normalized local data paths

```text
data/raw/binance_usdm/klines/symbol=X/interval=Y/year=YYYY/month=MM/X-Y-YYYY-MM.zip
data/raw/binance_usdm/markPriceKlines/symbol=X/interval=Y/year=YYYY/month=MM/X-Y-YYYY-MM.zip
data/raw/binance_usdm/fundingRate/symbol=X/year=YYYY/month=MM/X-fundingRate-YYYY-MM.zip

data/normalized/klines/symbol=X/interval=Y/year=YYYY/month=MM/part-0000.parquet
data/normalized/markprice_klines/symbol=X/interval=Y/year=YYYY/month=MM/part-0000.parquet
data/normalized/funding/symbol=X/year=YYYY/month=MM/part-0000.parquet
```

All raw and normalized paths are gitignored. Reproducible from the orchestrator script.

## Docs-and-data status

Phase 4ac is **docs-and-data**. Phase 4ac added one standalone orchestrator script, 35 committed manifests, two committed report markdown files, and a narrow `current-project-state.md` update. Local raw and normalized data are gitignored. **No source code under `src/prometheus/` modified. No tests modified. No existing scripts modified. No existing manifests modified.**

## Acquisition source and public-only confirmation

- **Source:** `https://data.binance.vision/data/futures/um/monthly/{klines|markPriceKlines|fundingRate}/...` (public unauthenticated bulk archives).
- **SHA256 verification** against paired `.CHECKSUM` companion files for every monthly archive. Zero checksum mismatches.
- **No authenticated APIs.**
- **No private endpoints.**
- **No public-endpoint code calls** (the orchestrator does NOT call live REST endpoints; it downloads bulk archives only).
- **No WebSocket / user stream / listenKey lifecycle.**
- **No credentials / `.env` / MCP / Graphify / `.mcp.json`.**

## No authenticated / private / live / exchange-write confirmation

- `authenticated_api_used = false` recorded in every Phase 4ac manifest.
- `private_endpoint_used = false` recorded in every Phase 4ac manifest.
- `websocket_used = false` recorded in every Phase 4ac manifest.
- `user_stream_used = false` recorded in every Phase 4ac manifest.
- `exchange_write_attempted = false` recorded in every Phase 4ac manifest.
- `no_credentials_confirmation = true` recorded in every Phase 4ac manifest.

## No backtests / diagnostics / Q1–Q7 rerun

Phase 4ac did NOT:

- run any backtest (no Phase 2 / 3 / 4l / 4r / 4x rerun; no new backtest);
- run any diagnostic (no Q1–Q7 rerun; no new diagnostic phase);
- execute any committed acquisition / backtest / analysis script other than `scripts/phase4ac_alt_symbol_acquisition.py` (the new Phase 4ac orchestrator).

## No strategy created

Phase 4ac did NOT:

- create a new strategy candidate;
- name a new strategy;
- create a fresh-hypothesis discovery memo;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid;
- create any "rescue" or "improvement" of R3 / R2 / F1 / D1-A / V2 / G1 / C1.

## No prior verdict revised

Phase 4ac preserved every retained verdict verbatim:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains CLOSED operationally.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

No retained verdicts were revised.

## No locks changed

Phase 4ac preserved every project lock verbatim:

- §11.6 HIGH cost = 8 bps per side.
- §1.7.3 project-level locks: 0.25% risk; 2× leverage; one position max; mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.
- Phase 4j §11 metrics OI-subset partial-eligibility rule.
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy-spec.
- Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy-spec.
- Phase 4w C1 backtest-plan methodology.

No project locks changed.

## Phase 4z recommendations not adopted as governance

Phase 4z recommendations (32-item proposed admissibility framework, design-family-distance matrix, M0 theoretical-admissibility gate concept, edge-rate viability gate concept, future memo template additions) remain recommendations only. **Phase 4ac did NOT adopt them as binding governance.**

## Phase 4aa admissibility framework not adopted as governance

Phase 4aa admissibility framework (eight pre-backtest gates) remains recommendation only. **Phase 4ac did NOT adopt it as binding governance.**

## Phase 4ab recommendations not adopted as governance

Phase 4ab recommendations (core acquisition-planning set; data-family requirements / optionality; date-range policy; manifest-field requirements; integrity gates; feasibility-check targets) remain recommendations only. **Phase 4ac did NOT adopt them as binding governance.** Phase 4ac used Phase 4ab as a planning input only and produced concrete data + integrity evidence consistent with Phase 4ab's recommendations.

## Phase 4ac results not adopted as binding governance

Phase 4ac results are **data / integrity evidence only**. The 35 committed manifests record per-family `research_eligible` status with verbatim gap windows. Phase 4ac does NOT convert any of these results into binding governance (e.g., Phase 4ac does NOT create a per-bar exclusion rule for SOL / XRP early-2022 trade-price kline gaps; that would require a separately authorized Phase 4ad-equivalent governance memo analogous to Phase 4j §11).

## Recommendation from Phase 4ac report

```text
Recommended primary next step:
After review, merge Phase 4ac into main, then remain paused unless the operator
separately authorizes a docs-only Phase 4ad gap-governance / scope-revision memo
(Option A) or a docs-only Phase 4ad PASS-subset substrate-feasibility analysis
memo (Option B).

Option A is recommended as primary because the pattern of mark-price gaps
and SOL/XRP early-2022 kline gaps will affect both PASS-subset analysis and
any later mark-price-using research; resolving governance first avoids
analyzing-then-amending.

Always procedurally valid: remain paused without authorizing Phase 4ad.

Do not backtest yet.
Do not create a strategy yet.
Do not rescue prior strategies.
Do not expand market type yet.
```

## No successor phase authorized

Phase 4ac does NOT authorize:

- Phase 4ad (any kind);
- Phase 5;
- Phase 4 canonical;
- any other named successor phase.

The next step is operator-driven: the operator decides whether to remain paused (with or without merging Phase 4ac) or authorize Phase 4ad (or some other phase).

## Working tree / git status evidence

```text
On branch phase-4ac/alt-symbol-public-data-acquisition
Untracked files (gitignored transients only; not committed):
  .claude/scheduled_tasks.lock
  data/research/        (gitignored; contains Phase 4ac local log)
  data/raw/binance_usdm/    (gitignored)
  data/normalized/      (gitignored)
```

Repository state at base:

```text
main / origin/main: 9db120741413ec9cb5b02ffd9622d0f43a1d8c57 (unchanged)
Phase 4ab merge commit:                9db120741413ec9cb5b02ffd9622d0f43a1d8c57
Phase 4ab report commit:               524e4e7323df2e36b05be48423524f42af4d1e5c
Phase 4ac branch:                      phase-4ac/alt-symbol-public-data-acquisition (this branch)
```

### Acquisition counters

- Archives attempted: 1 820 (35 families × 52 months).
- Archives downloaded: 1 820 (zero 404).
- Archives checksum-verified: 1 820 (zero mismatches).
- Archives failed / unavailable: 0.
- Local raw footprint: 189.0 MiB (Phase 4ac-attributable).
- Local normalized footprint: ~257.6 MiB (across all phases sharing the directory; Phase 4ac added the new alt-symbol partitions).
- Manifests created: 35.
- `research_eligible: true` datasets: 9.
- `research_eligible: false` datasets: 26.
- Invalid windows recorded: see report §7.
- Symbols / families / intervals that failed strict gate: see report §6 FAIL table.

## Forbidden-work confirmation

Phase 4ac did NOT do any of the following:

- run a backtest (any phase);
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
- modify any existing manifest (the 26 manifests previously committed remain unchanged);
- patch / forward-fill / interpolate / impute / synthesize / replace any data;
- silently drop gaps;
- silently relax strict integrity gates;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- amend the Phase 4m 18-requirement validity gate;
- amend the Phase 4t 10-dimension scoring matrix;
- amend the Phase 4u opportunity-rate principle;
- amend the Phase 4w negative-baseline / PBO / DSR / CSCV methodology;
- amend the Phase 4aa admissibility framework;
- amend the Phase 4ab data-requirements / feasibility framework;
- modify any specialist governance file beyond the narrow `docs/00-meta/current-project-state.md` update;
- adopt any Phase 4z recommendation as binding governance;
- adopt the Phase 4aa admissibility framework as binding governance;
- adopt any Phase 4ab recommendation as binding governance;
- adopt any Phase 4ac result as binding governance;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4ad / Phase 5 / Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- merge Phase 4ac to main (the branch is preserved; merge would require separate operator instruction).

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal; preserved)
G1                  : HARD REJECT (Phase 4r terminal; preserved)
C1                  : HARD REJECT (Phase 4x terminal; preserved)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : project-level locks preserved
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility rule (preserved)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4p                    : G1 strategy spec (preserved)
Phase 4q                    : G1 backtest-plan methodology (preserved)
Phase 4v                    : C1 strategy spec (preserved)
Phase 4w                    : C1 backtest-plan methodology (preserved)
Phase 4z recommendations    : remain recommendations only; NOT adopted by 4ac
Phase 4aa admissibility framework : remain recommendation only; NOT adopted by 4ac
Phase 4ab recommendations   : remain recommendations only; NOT adopted by 4ac
Phase 4ac                   : Alt-symbol public data acquisition / integrity
                              validation (this phase; new; docs-and-data;
                              feature-branch only; not merged)
Phase 4ac results           : data / integrity evidence only;
                              NOT binding governance
Recommended state           : remain paused (primary);
                              docs-only Phase 4ad gap-governance / scope-
                              revision memo OR docs-only Phase 4ad-B PASS-
                              subset substrate-feasibility analysis memo
                              (conditional next; not authorized by 4ac)
```

## Next authorization status

```text
Phase 4ad / Phase 5 / successor    : NOT authorized
Phase 4 (canonical)                : NOT authorized
Paper / shadow                     : NOT authorized
Live-readiness                     : NOT authorized
Deployment                         : NOT authorized
Production-key creation            : NOT authorized
Authenticated REST                 : NOT authorized
Private endpoints                  : NOT authorized
Public endpoint calls in code      : NOT authorized
User stream / WebSocket            : NOT authorized
Exchange-write capability          : NOT authorized
MCP / Graphify                     : NOT authorized
.mcp.json / credentials            : NOT authorized
C1 / V2 / G1 / R2 / F1 / D1-A rescue : NOT authorized; FORBIDDEN
C1-prime / V2-prime / G1-prime /
  R2-prime / F1-prime / D1-A-prime  : NOT authorized; FORBIDDEN
Old-strategy alt-symbol re-run     : NOT authorized; FORBIDDEN (retrospective rescue)
Adoption of Phase 4z recommendations
  as binding governance            : NOT authorized
Adoption of Phase 4aa admissibility
  framework as binding governance  : NOT authorized
Adoption of Phase 4ab recommendations
  as binding governance            : NOT authorized
Adoption of Phase 4ac results
  as binding governance            : NOT authorized
Alt-symbol governance memo
  (Phase 4ad gap-governance)       : NOT authorized; conditional next in
                                     operator decision menu
Alt-symbol PASS-subset feasibility
  analysis memo (Phase 4ad-B)      : NOT authorized; conditional next in
                                     operator decision menu
Alt-symbol fresh-hypothesis memo   : NOT authorized
Alt-symbol strategy-spec memo      : NOT authorized
Alt-symbol backtest-plan memo      : NOT authorized
Alt-symbol backtest execution      : NOT authorized
Spot / COIN-M / options / cross-
  venue expansion                  : NOT authorized; not recommended
Phase 4ac merge to main            : NOT authorized; preserved on
                                     feature branch unless separately
                                     instructed
```

The next step is operator-driven: the operator decides whether to remain paused, merge Phase 4ac to main and authorize a future docs-only Phase 4ad gap-governance / scope-revision memo or PASS-subset substrate-feasibility analysis memo, or take some other action. Until then, the project remains at the post-Phase-4ab merge boundary on `main` with Phase 4ac preserved on its feature branch.

---

**Phase 4ac is docs-and-data acquisition / integrity validation only. main remains unchanged at `9db120741413ec9cb5b02ffd9622d0f43a1d8c57`. Phase 4ac added one orchestrator script, 35 committed manifests, two report markdown files, and a narrow `current-project-state.md` update. Phase 4ac did NOT modify any source under `src/prometheus/`, any test, any existing script, any existing manifest, any specialist governance file, or any prior phase's substantive content. Phase 4z, Phase 4aa, Phase 4ab, and Phase 4ac results all remain recommendations / data evidence only — not binding governance. C1 / V2 / G1 first-specs remain terminally HARD REJECTED. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. Recommended state: remain paused (primary); Phase 4ad gap-governance OR Phase 4ad-B PASS-subset feasibility analysis (conditional next; not authorized by Phase 4ac). No next phase authorized.**
