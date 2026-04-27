# Phase 2 Backtest Data Verification Report

**Repo:** `C:\Prometheus`
**Date:** 2026-04-27
**Goal:** Verify the copied `data/` directory is sufficient to run existing Phase 2 backtests.
**Scope:** Read-only audit. No code changes, no new variants, no fresh smoke run.

---

## 1. `data/` exists

Top-level `data/` is present with the full Phase-2 layout:

```
data/
├── raw/binance_usdm/{exchange_info,klines,markPriceKlines}/
├── normalized/{klines,mark_price_klines,funding_rate}/symbol={BTCUSDT,ETHUSDT}/
├── derived/{bars_1h/standard, exchange_info, backtests/<32 prior runs>}/
└── manifests/{v001 + v002 for both symbols × 4 datasets, plus _downloads/}
```

## 2. v002 manifests — all 8 present

| Manifest | Schema | Sources |
|---|---|---|
| `binance_usdm_btcusdt_15m__v002` | `kline_v1` | 51 monthly zips |
| `binance_usdm_btcusdt_1h_derived__v002` | `kline_v1` | 1 (derived from 15m) |
| `binance_usdm_btcusdt_markprice_15m__v002` | `mark_price_kline_v1` | 51 monthly zips |
| `binance_usdm_btcusdt_funding__v002` | `funding_rate_event_v1` | 1 (REST paginator) |
| `binance_usdm_ethusdt_15m__v002` | `kline_v1` | 51 monthly zips |
| `binance_usdm_ethusdt_1h_derived__v002` | `kline_v1` | 1 |
| `binance_usdm_ethusdt_markprice_15m__v002` | `mark_price_kline_v1` | 51 monthly zips |
| `binance_usdm_ethusdt_funding__v002` | `funding_rate_event_v1` | 1 |

v001 manifests also retained as audit trail per Phase 2e GAP-20260420-029.

## 3. Required data files

DuckDB hive-partitioning scan over `data/normalized/**` and `data/derived/**`:

| Dataset | Rows | First | Last | Partitions |
|---|---:|---|---|---:|
| BTCUSDT 15m klines | 148,896 | 2022-01-01 00:00 UTC | 2026-03-31 23:45 UTC | 51 |
| ETHUSDT 15m klines | 148,896 | 2022-01-01 00:00 UTC | 2026-03-31 23:45 UTC | 51 |
| Derived 1h bars (BTC+ETH) | 74,448 | 2022-01-01 00:00 UTC | 2026-03-31 23:00 UTC | 102 |
| BTCUSDT mark-price 15m | 148,607 | 2022-01-01 00:00 UTC | 2026-03-31 23:45 UTC | 51 |
| ETHUSDT mark-price 15m | 148,703 | 2022-01-01 00:00 UTC | 2026-03-31 23:45 UTC | 51 |
| BTCUSDT funding | 4,653 | 2022-01-01 00:00 UTC | 2026-03-31 16:00 UTC | 51 |
| ETHUSDT funding | 4,653 | 2022-01-01 00:00 UTC | 2026-03-31 16:00 UTC | 51 |

**Row-count cross-check:** klines and 1h-derived match `51 months × interval-frequency × 2 symbols` arithmetic exactly. Funding events match `3 events/day × ~365.25 days × 4.25 years = 4,653` exactly.

**Mark-price gap analysis:** BTC missing 289 of 148,896 (0.19%), ETH missing 193 of 148,896 (0.13%). Consistent with documented Binance archive limitations (GAP-20260420-029, mark-price < 2024-01). Within accepted tolerance — Phase 2e baseline ran on this profile.

## 4. Exchange-info snapshot

`data/derived/exchange_info/2026-04-19T21-22-59Z.json` — single point-in-time snapshot containing both BTCUSDT and ETHUSDT (2 symbols total). This is the snapshot Phase 2/3 backtests load.

## 5. Read-only validation result

**Method:** `uv run python` ad-hoc DuckDB scan of every dataset (no code committed, no artifacts written).

**Result:** Every dataset loaded cleanly through `pyarrow` hive-partitioning. No row-validation drift. Time ranges align across all four datasets. Row counts match the expected `51 months × interval frequency × 2 symbols` arithmetic exactly for klines / 1h-derived / funding.

## 6. Prior backtest run directories preserved

`data/derived/backtests/` retains 32 prior run directories from earlier work, including:

- `phase-2e-baseline`
- `phase-2g-wave1-{h0,h-a1,h-b2,h-c1,h-d3}-r`
- `phase-2l-{h0,r3}-{r,v}` plus slippage and stop-trigger sensitivity variants
- `phase-2m-r1a-{h0,r3,r1a_plus_r3}-{r,v}` plus sensitivities
- `phase-2s-r1b-{h0,r3,r1b_narrow}-{r,v}` plus sensitivities
- `phase-3-smoke`

These remain available as oracle baselines for diff-checking re-runs.

## 7. Verdict

| Backtest | Runnable now? |
|---|---|
| Phase 2e baseline | **Yes** |
| Phase 2g wave-1 variants (H0/A1/B2/C1/D3) | **Yes** |
| Phase 2l (R3, slip variants, stop-trigger variants) | **Yes** |
| Phase 2m (R1a + R1a×R3 combinations) | **Yes** |
| Phase 2s (R1b-narrow + H0/R3 controls) | **Yes** |
| Phase 3 smoke run ([scripts/phase3_smoke_run.py](../../../scripts/phase3_smoke_run.py)) | **Yes** |

All four required v002 datasets and the exchange-info snapshot are present, complete, and time-aligned for both BTCUSDT and ETHUSDT across 2022-01-01 → 2026-03-31.

**Phase 2s and Phase 3 backtests are runnable on this laptop. No backfill needed.**
