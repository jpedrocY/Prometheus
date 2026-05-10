# Phase 4bh-B — Closeout

**Phase identity:** Phase 4bh-B — AggTrades Feature Schema Finalization Memo.
**Phase type:** docs-only feature schema finalization memo.
**Date:** 2026-05-10.
**Branch:** `phase-4bh-b/aggtrades-feature-schema-finalization`.
**Base:** `main` at the post-Phase-4bh-A merge-closeout state (`714a2730d2a03ffb9ef16daba7eea28fc359611c`); Phase 4bh-A merge commit `c85b0ec9efd8a00b05eb4f39fe156eb31fe07875` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.

---

## Summary

Phase 4bh-B converts the broad Phase 4bh-A Feature Stage-0 design into an exact, implementable feature schema for any future Phase 4bh implementation. The memo finalizes the feature family name (`microstructure_features_aggtrades_v001`), the canonical input (`microstructure_normalized_aggtrades_v001` cited only via Phase 4bg-B successor-state JSON), the future output namespace (`data/microstructure/features/...`; not created), the future feature manifest path (not created), the event-aligned output row model with expected `row_count = 1,681,098` for BTCUSDT 2025-01-15, the timestamp cadence (`feature_timestamp_ms = source transact_time_ms`), the four-window subset {1s, 5s, 15s, 60s}, the 45-feature column list (40 windowed + 3 time-context + 2 data-quality), the 16 lineage / identity / metadata columns, the full output schema table (61 columns), the dtype / null / NaN / decimal-float / invalid-window / causal windowing policies, the same-timestamp tie-break rule, the price rule for log returns, the aggressive-side rule, the forbidden-substring detector, the future feature manifest schema, the future feature config schema, the future Phase 4bh module / test layout, 26 acceptance criteria, and 17 fail-closed rules.

**No feature computation occurred.** No feature dataset, manifest, sidecar, or feature-config file was created. No source code, test, script, configuration, manifest, raw artefact, gate report, successor-state artefact, or `.gitignore` entry was modified. No data was acquired. No successor phase is authorized.

The original derived manifest remains `research_eligible=false / eligibility_gate_status=pending`. The raw family remains permanently `research_eligible=false`. Stage-4 (feature-family eligibility-gate-passed) is **not** authorized.

---

## Files added (tracked in git)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_aggtrades-feature-schema-finalization.md` (the main memo).
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_closeout.md` (this file).

## Files modified narrowly (tracked in git)

- `docs/00-meta/current-project-state.md` — narrow Phase 4bh-B paragraph + new "Current phase:" block; prior Phase 4bh-A block preserved as historical context.

## Files NOT modified

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No file under `data/`, `data/manifests/`, `data/research/`, `data/derived/`, `data/raw/`, `data/normalized/`.
- No file under `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, `data/microstructure/gate-reports/`, `data/microstructure/successor-state/`, or `data/microstructure/features/` (the last directory does not exist).
- `.gitignore` is unchanged.
- `pyproject.toml` is unchanged.
- `README.md` is unchanged.
- No prior memo (other than the narrow `current-project-state.md` paragraph addition).
- No script under `scripts/...` was created or modified.
- The Phase 4bb-D raw gate report and paired sidecar are unchanged.
- The Phase 4bd normalized Parquet and derived manifest are unchanged.
- The Phase 4bf gate report and paired sidecar are unchanged.
- The Phase 4az raw manifest, raw zip, raw sidecar, and acquisition log are unchanged.
- The Phase 4bg-B successor-state JSON and paired sidecar are unchanged.
- The proposed future feature dataset / manifest / sidecar paths do not exist.

---

## Pre/post immutability evidence

The following SHAs were verified at the start of Phase 4bh-B and remained unchanged at the end (Phase 4bh-B does not write under `data/microstructure/`):

| Artefact | SHA256 |
| -------- | ------ |
| derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

Both original manifest states preserved:

- derived manifest `research_eligible=false / eligibility_gate_status=pending`;
- raw manifest `research_eligible=false / eligibility_gate_status=pending`.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

The future feature dataset path (`data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet`), its sidecar, and the future feature manifest path (`data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json`) do not exist. The directory `data/microstructure/features/` does not exist.

---

## Decision recorded

- **Phase 4bh-B finalizes the feature schema** for any future Phase 4bh implementation;
- final feature family name: `microstructure_features_aggtrades_v001`;
- final canonical input: `microstructure_normalized_aggtrades_v001` (Stage-3 marker = Phase 4bg-B successor-state JSON only);
- final output row model: **event-aligned**, one feature row per source aggTrade row, expected `row_count = 1,681,098` for BTCUSDT 2025-01-15;
- final timestamp cadence: `feature_timestamp_ms = source transact_time_ms`;
- final windows: `{1s, 5s, 15s, 60s}` (`window_ms = [1000, 5000, 15000, 60000]`); 30s and 5min explicitly deferred;
- final feature column count: 45 (40 windowed `= 4 × 10` + 3 time-context + 2 data-quality);
- final lineage / identity / metadata column count: 16;
- **final total schema column count: 61** (16 lineage / identity / metadata + 45 features);
- aggressive-side rule: `is_buyer_maker=false` ⇒ aggressive buy; `is_buyer_maker=true` ⇒ aggressive sell;
- causal windowing rule: trailing window `(T - window_ms, T]` with same-timestamp tie-break by `row_index <= R`;
- log-return rule: prior reference price = last source row with `transact_time_ms <= T - window_ms` (with same-timestamp tie-break by `row_index ASC` among ties); null if no prior reference price;
- decimal/float policy: raw `price` and raw `quantity` always Decimal-as-string; quantity sums / aggressive-side quantities / quantity means / imbalances Decimal-as-string; ratios and log returns `float64` nullable;
- null / NaN policy: counts `0` if empty window; quantity sums `"0"` if empty; quantity means null if empty; aggressive flow ratio null if denominator == 0; log returns null if no prior reference price; no imputation across invalid windows;
- invalid-window propagation: source `invalid_windows` propagated verbatim; `invalid_window_flag` per row; `rolling_missing_window_flag` per row (OR across windows);
- forbidden-substring detector: 26 substrings enforced at validation time;
- future Phase 4bh module layout: 5 new modules + narrow `__init__.py` re-export update;
- future Phase 4bh test layout: 6 new test files + optional fixture builder;
- 26 acceptance criteria + 17 fail-closed rules predeclared.

---

## Validation

| Check | Result |
| ----- | ------ |
| `git diff --stat` (pre-commit) | 3 docs files changed (only the two new memos and the narrow `current-project-state.md` paragraph) |
| `git diff --name-only` | docs only |
| `ruff check .` | All checks passed |
| `pytest tests/research/microstructure/` | 492 passed |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py`; identical to pre-Phase-4bh-B baseline) |
| `mypy src/prometheus` (strict) | Success: no issues found in 101 source files |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |

Phase 4bh-B introduces zero new test regressions.

---

## What Phase 4bh-B did NOT do

- did not modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, or runtime configuration;
- did not implement, run, or rerun any gate, normalizer, feature pipeline, or backtest;
- did not generate a new gate report, feature dataset, feature manifest, feature-config file, or successor-state artefact;
- did not create `data/microstructure/features/`;
- did not delete, move, rename, or modify any existing `data/microstructure/` file;
- did not modify the Phase 4az raw manifest, raw zip, sidecar, or acquisition log;
- did not modify the Phase 4bb-D gate report or its sidecar;
- did not modify the Phase 4bd normalized Parquet or derived manifest;
- did not modify the Phase 4bf gate report or its sidecar;
- did not modify the Phase 4bg-B successor-state JSON or its sidecar;
- did not create JSONL, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- did not acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request credentials, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- did not compute features, taker imbalance, sweep detection, aggressive-flow score, spread / depth / liquidity / slippage / order-flow / execution-quality proxies, returns, alpha, edge, predictiveness, signal quality, profitability, opportunity rate, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- did not create labels, targets, or strategy signals;
- did not train ML, create strategy logic, or run backtests;
- did not flip `research_eligible` on any actual manifest;
- did not transition `eligibility_gate_status` on any actual manifest;
- did not authorize Stage-4 feature-cleared status, feature computation, ML, strategy, or backtests;
- did not revise any retained verdict, change any project lock, or amend M0;
- did not authorize Phase 4bh-C, Phase 4bh, Phase 4bi-A, Phase 4bi-B, Phase 4bi-C, Phase 4bi-D, Phase 4bj, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- did not commit anything under `data/microstructure/`.

---

## Preserved boundaries

H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 retained verdict ledger preserved verbatim. §11.6 / §1.7.3 / Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w project locks preserved verbatim. Phase 4ak M0 (12-clause gate + post-null cooldown + cooled-down families list + memo template) preserved. Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy preserved. Phase 4am / 4an / 4ao / 4ap / 4aq / 4ar / 4as / 4at / 4au / 4av / 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A results preserved verbatim.

---

## Recommended state

**Remain paused.**

Conditional next options (none authorized by Phase 4bh-B):

- future docs-only **Phase 4bh-C** — Feature Schema Finalization Review / Red-Team Memo;
- future code + docs + local gitignored output **Phase 4bh** — AggTrades Feature Schema / Feature Computation Implementation, using the exact Phase 4bh-B finalized schema;
- future analysis + docs **Phase 4bi-A** — Feature Artefact Structural QA Memo;
- future code + docs **Phase 4bb-F** — Gate Report Output Path Hygiene;
- future docs-only or docs-and-local-gitignored-output **Phase 4bb-G** — Raw Manifest Successor-State Recording.

**No successor phase is authorized by Phase 4bh-B.**
