# Phase 4bn-AT — Closeout

## Phase

Phase 4bn-AT — Top-of-Book Mechanism Admissibility and Bounce-Decomposition Preregistration.

## Branch

`phase-4bn-at/top-of-book-mechanism-admissibility-bounce-preregistration`.

## Base SHA

`40377e231cc72318c884a11d258775912fe71b4c` (main == origin/main at phase start).

## Phase type

Docs-only source-admissibility and scientific-preregistration **decision** phase. No market-data acquisition, capture, read, parse, normalization, alignment, label/feature construction, model, diagnostic, builder, or workflow. Documentation committed only.

## Files created

- `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-at_top-of-book-mechanism-admissibility-bounce-preregistration.md` (main memo, 61 sections).
- `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-at_closeout.md` (this closeout).

No other file added, modified, renamed, or deleted.

## Committed project documents inspected

`docs/00-meta/current-project-state.md` (stale past Phase 3k); `docs/00-meta/m0-mechanism-admissibility-gate.md`; process standards under `docs/00-meta/process/`; Phase 4bn-AB source-admissibility memo; Phase 4bn-Y split/holdout policy; Phase 4bn-AA split-policy artefact; Phase 4bn-AC ML-dataset-contract memo; Phase 4bn-AE preregistration + §19 M0 boundary; Phase 4bn-AH…AO reports/closeouts; Phase 4bn-AJ 15s verdict/closeout; Phase 4bn-AK ML-arc decision memo (deferred §16(b) bookTicker admissibility memo); Phase 4bn-AP long-horizon contract; Phase 4bn-AQ dataset build; Phase 4bn-AR long-horizon verdict; Phase 4bn-AS ambiguity decision + closeout + merge-closeout; prior microstructure arc Phase 4as/4at/4au/4av/4az/4ba/4bb-C/4bb-F; Phase 4bn-L storage/budget; `docs/04-data/{timestamp-policy,data-requirements,live-data-spec,historical-data-spec,dataset-versioning}.md`; `docs/06-execution-exchange/{binance-usdm-order-model,exchange-adapter-design}.md`. Committed source read (not modified): `manifest.py`, `pre_v002_ml_dataset_contract.py`, `pre_v002_split_policy.py`, `canonical_paths.py`.

## External sources inspected (accessed 2026-07-14 UTC; documentation / index / issue metadata only)

- `https://github.com/binance/binance-public-data` (README; aggTrades/klines/trades documented; `.CHECKSUM` SHA256; MIT).
- `https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2FbookTicker%2FBTCUSDT%2F` (archive index — undocumented futures um bookTicker tree exists).
- `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/daily/bookTicker/BTCUSDT/` (index metadata only; coverage of 2024-10/11 unconfirmed; earliest visible ~2023-05-16; `.CHECKSUM` present).
- `https://github.com/binance/binance-public-data/issues/305` (out-of-sequence futures bookTicker BTC/ETH; opened 2024-01-16, Closed, no maintainer fix; 7-column layout).
- `https://dev.binance.vision/t/how-and-where-can-i-get-the-history-bookticker-data/36122/1` (2025-08-16; reports bookTicker archive ceased updating in 2024; no staff response).
- `https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Individual-Symbol-Book-Ticker-Streams` (official WS field doc; SPA, not retrievable as static content; live field contract taken from committed Phase 4au spec).
- Tier-3 (candidate-identification only, not admitted): Tardis.dev, cryptodatadownload.

## Exact source hierarchy

Tier 1 (official primary): Binance API docs; `data.binance.vision` archive; public-data GitHub README; checksum/format docs; terms/licensing. Tier 2 (official secondary): Binance GitHub issues/maintainer responses; announcements/changelogs; Developer Community threads. Tier 3 (reputable third party): used only to identify candidates; not admitted on coverage claims. Excluded: mirrors, torrents, scraped/reconstructed/synthetic data, or any source with undocumented timestamps/update semantics. **Result:** futures um bookTicker is Tier-1-*present* but Tier-1-*undocumented*; its schema and ordering defect are Tier-2/Tier-3 only; its coverage/cessation are Tier-2 assertion, unconfirmed by Tier-1 metadata.

## Exact coverage finding

Required = 59 BTCUSDT UTC dates (validation 2024-10-02…2024-11-15 = 45; holdout 2024-11-17…2024-11-30 = 14; 2024-11-16 embargo excluded). A futures um daily bookTicker archive for BTCUSDT exists, but **complete coverage of the required 59-date window could not be established** from Tier-1 index metadata, and a Tier-2 report indicates the archive ceased updating in 2024. Under the default conservative rule, unestablished validation/holdout coverage does not qualify for retrospective admission.

## Retrospective feasibility

**Fails.** Coverage unestablished; archived-file timestamp/sequencing semantics undocumented and documented-defective (out-of-order, issue #305, closed with no fix); provenance/immutability/terms inadequate; the project's own prior finding recorded the family as unavailable; resolving the uncertainty would require prohibited data acquisition (counts against admission). Checksums present but insufficient alone.

## Prospective feasibility

**Fails for this question.** Live bookTicker capture is technically/legally feasible and officially documented, but a 2026 capture is regime-non-comparable and — decisively — cannot be aligned to the 2024 aggTrades that constitute the result under examination, so it cannot answer the specific mechanism question; disproportionate cost; rescue/relitigation risk.

## Frozen future admissibility screens

Coverage (all 59 dates; 0 missing/partial; full UTC-day; ≤60 s data gaps); file integrity (0 checksum/unreadable failures; exact 7-column schema; duplicate ≤0.5 %/day; residual out-of-order ≤0.5 % after evidence-preserving stable sort; mandatory reorder-evidence bundle); quote validity (finite/positive bid&ask; bid≤ask; crossed/locked/zero-qty excluded not repaired; invalid >1.0 %/day rejects day, >0.5 % segment fails); timestamp coherence (authoritative `transaction_time`; secondary `event_time`; ties by `update_id` then original order; ms precision; UTC date by `transaction_time`); freshness (quote age ≤2000 ms; stale >5.0 %/day rejects, >2.0 % segment fails; no backfill/interpolation); alignment (latest valid quote with `transaction_time`≤t; never future; support both endpoints; ≥95 % support, <90 %/day rejects, <95 % segment fails); partition/dataset rejection (59/59 required; no post-inspection relaxation; fail-closed).

## Frozen causal-alignment contract

For observation timestamp t, use only the latest valid quote with authoritative `transaction_time` ≤ t; never a future quote; no interpolation; no nearest-neighbor that could pick a future quote; no backfill; equal timestamps resolved by `update_id` then deterministic original order; documented out-of-order records may be stably sorted **only** with full before/after evidence (original SHA256, counts, pre/post monotonicity diagnostics, sort keys, post-sort SHA256, duplicate policy); crossed/invalid quotes never silently repaired; stale/missing quotes excluded under the frozen support rules; no target crosses a split or UTC-date boundary contrary to the pre-v002 split policy.

## Frozen metric registry

Model-free only (no fit/score/predict/calibrate/threshold-tune): quoted midpoint; quoted spread (raw and bps); half-spread bps; quote age; trade-to-midpoint location (price/bps/half-spread); trade-price 15s direction (frozen strict-sign, descriptive); midpoint 15s direction (strict-sign on causal midpoint); label-agreement matrix; agreement measures (exact, non-zero directional, disagreement, opposite, trade-only, midpoint-only, Cohen's κ alongside raw rates); bounce indicators; spread/freshness distributions; materiality comparison (|trade|/spread, |midpoint|/spread, fractions exceeding one spread and the locked 16 bps); observable-friction-component audit. Aggregation: segment / UTC date / UTC month / hour / spread bucket / quote-age bucket.

## Frozen science-outcome categories

`BOUNCE_DOMINATED` (A<0.60 ∧ TOM≥0.50 ∧ SUB≥0.60 ∧ OPP≥0.10, consistent ≥80 % dates + both months); `MIDPOINT_CONFIRMED` (A≥0.80 ∧ TOM≤0.25 ∧ MNZ≥0.60 ∧ OPP≤0.05 ∧ SUB≤0.40, consistent ≥80 % dates + both months); `MIXED_MECHANISM` (integrity passes, neither pure region met, or consistency <80 %); `DATA_INTEGRITY_FAILURE` (any admissibility screen fails; fail-closed, takes precedence). Consequences frozen per the main memo §44; no outcome authorizes a model/strategy/backtest/live work, reopens the stopped arc, revises prior metrics, or changes the locked 8/16 bps reference.

## Exact decision

**STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE.**

## Phase result state

`TOP_OF_BOOK_MECHANISM_ADMISSIBILITY_MEMO_COMPLETE__STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## Concise rationale

The retrospective bookTicker archive is Tier-1-undocumented, of unconfirmed coverage for the required 2024 window, reportedly ceased in 2024, and carries an unremediated documented out-of-order defect with undocumented timestamp semantics — provenance and causal-alignment validity are inadequate, and resolving them requires prohibited acquisition. Prospective capture cannot align to the 2024 trades and so cannot answer the question, at disproportionate cost and with rescue/relitigation risk. Expected decision-relevant information gain is low regardless of outcome and changes no authorized action. A causal, falsifiable contract is frozen for any future genuinely-admissible data, but no current source can execute it admissibly. Remain paused.

## Confirmation no data acquired or read

Confirmed. No bookTicker/aggTrades archive, sample, Parquet, CSV, or JSON market snapshot downloaded, opened, or parsed. Only documentation, a GitHub issue, and archive index metadata (file names / LastModified) were fetched. `test_rows_loaded = 0`.

## Confirmation no local generated output read

Confirmed. No AQ/AR JSON artefacts, model parameters/predictions, feature/label Parquet, raw aggTrades, v002 terminal, or sealed-test data read. Nothing under `data/` opened.

## Confirmation no market endpoint called

Confirmed. No live or historical Binance market-data endpoint called; no WebSocket opened; no capture started.

## Confirmation no model / workflow / rerun

Confirmed. No model trained/scored/predicted/calibrated; no builder/normalizer/aligner/label/feature/diagnostic/baseline/workflow run; no acquisition/parser/capture script run or created.

## Confirmation no source / test / script / config changed

Confirmed. Only two documentation files added under `docs/00-meta/implementation-reports/`. No source, test, script, config, manifest, gate, sidecar, split, or model-config modified. No data/model artefact committed.

## Confirmation no authorization flag changed

Confirmed. All published authorization flags remain `false`; `research_eligible` unchanged (`False`); `eligibility_gate_status` unchanged (`PENDING`); `flip_research_eligible(...)` not invoked; `STOP_LONGHORIZON_ML_ARC` preserved; Phase 4bn-AE claim scope and §19 M0 boundary preserved; locked 8/16 bps preserved; Phase 4bn-AP/AQ/AR/AS preserved.

## Allowed claims

Per main memo §57: the 15s label may embed bounce and cannot be determined on current admissible data; the futures um bookTicker archive exists but is Tier-1-undocumented, out-of-order-defective (#305), reportedly ceased in 2024, and of unconfirmed required-window coverage; the retrospective source is inadmissible and the prospective analogue cannot answer §15; a falsifiable admissibility/alignment/metric/outcome contract is preregistered for any future genuinely-admissible data only.

## Forbidden claims

Per main memo §58: no claim that the 15s result is/is not bounce; no "true trading cost" / "true-cost audit"; no revision of AJ/AK/AR/AS metrics, completed rejections, materiality decisions, or the locked 8/16 bps reference by any future/prospective spread evidence (prospective-only); no describing the consumed holdout as unseen/independent confirmation; no reopening the stopped arc; no model/strategy/backtest/live authorization.

## Remaining blockers

Top-of-book mechanism decomposition is blocked by data inadmissibility: no admissible retrospective source (undocumented schema/timestamps/ordering, unconfirmed coverage, reported cessation, inadequate provenance) and no comparable prospective source (cannot align to 2024 trades). Any future reconsideration requires genuinely-new, fully-admissible top-of-book data and would begin with a docs-only admissibility re-check, not acquisition. The §19 M0 boundary remains the gate for any strategy/PnL/backtest/live path.

## Recommended state

**Remain paused.** No successor phase recommended.

## Explicit no-successor execution statement

**No successor execution is authorized.** No data acquisition, capture, download, parse, normalization, alignment, label/feature build, model, strategy, signal, PnL, backtest, replay, simulated fill, paper/shadow/live/exchange-write, or successor phase of any kind is authorized. Documentation committed only; project remains paused.
