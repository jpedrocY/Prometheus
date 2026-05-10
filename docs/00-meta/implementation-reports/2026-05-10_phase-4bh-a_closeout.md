# Phase 4bh-A — Closeout

**Phase identity:** Phase 4bh-A — AggTrades Feature-Boundary Design Memo.
**Phase type:** docs-only feature-boundary design memo.
**Date:** 2026-05-10.
**Branch:** `phase-4bh-a/aggtrades-feature-boundary-design`.
**Base:** `main` at the post-Phase-4bg-B merge-closeout state (`81747263a12b5593282f2f5cfbb17ed413a84cb3`); Phase 4bg-B merge commit `f134a7bbcf04b51139b8094ebc13839e50f5302e` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.

---

## Summary

Phase 4bh-A is a docs-only feature-boundary design memo. It defines the canonical input, forbidden inputs, proposed feature-family naming, feature-stage model, definitions of feature / label / signal / feature-computation, the allowed and forbidden feature classes, the temporal-leakage / windowing / aggregation / precision / type / missing-window policies, the proposed output namespace and manifest, the validation gate sequence, the M0 / cooled-down / no-rescue boundaries, and the acceptance criteria for any future Phase 4bh implementation phase. No feature is computed; no feature dataset, manifest, or sidecar is created; no source code, test, or script is added or modified; no data is acquired; no successor phase is authorized.

The memo records that Phase 4bh-A reaches **Feature Stage-0** (feature schema designed) only. The proposed (NOT created) future feature family is `microstructure_features_aggtrades_v001`, a sibling derived family that does not mutate the normalized derived family `microstructure_normalized_aggtrades_v001`.

---

## Files added (tracked in git)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_aggtrades-feature-boundary-design.md` (the main memo).
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_closeout.md` (this file).

## Files modified narrowly (tracked in git)

- `docs/00-meta/current-project-state.md` — narrow Phase 4bh-A paragraph + new "Current phase:" block; prior Phase 4bg-B block preserved as historical context.

## Files NOT modified

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No file under `data/`, `data/manifests/`, `data/research/`, `data/derived/`, `data/raw/`, `data/normalized/`.
- No file under `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, `data/microstructure/gate-reports/`, or `data/microstructure/successor-state/`.
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

---

## Pre/post immutability evidence

The following SHAs were verified at the start of Phase 4bh-A and remained unchanged at the end (Phase 4bh-A does not write under `data/microstructure/`):

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

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked by Phase 4bh-A).

---

## Decision recorded

- **Phase 4bh-A reaches Feature Stage-0** (feature schema designed) only;
- proposed future feature family: `microstructure_features_aggtrades_v001` (sibling derived family; **not** created by this memo);
- proposed future output namespace: `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/` (**not** created);
- proposed future feature manifest: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` (**not** created);
- canonical input: `microstructure_normalized_aggtrades_v001` (Stage-3 admissible only via Phase 4bg-B successor-state JSON SHA `8bcc7d01…`);
- forbidden inputs: raw aggTrades family, raw zip, raw manifest, Phase 4bb-D / Phase 4bf gate reports, mark-price, order book, liquidation, funding, OI, cross-symbol, network feeds, credentials, MCP / Graphify;
- forbidden feature classes: future returns, next-window movement, future high / low, future realized volatility, future volume, labels, target columns, signals, entry / exit flags, PnL, MFE / MAE, R-multiple, equity curve, position state, ML embeddings, learned representations, full-day-distribution normalization (unless explicitly causal), z-scores using future data, post-hoc-fitted thresholds, any feature whose purpose is to revise or rescue a retained verdict;
- temporal-leakage boundary: every feature row uses only `transact_time_ms <= T`; trailing windows only; no centered windows; no future labels; train / validation / OOS splits are future work;
- proposed candidate windows (NOT approved for computation): 1 s, 5 s, 15 s, 30 s, 60 s, 5 min;
- proposed precision policy: Decimal-as-string for `price` and `quantity`; UTC ms `int64` for timestamps; strict bool for `is_buyer_maker`; raw price and raw quantity must never be stored as float in any future feature dataset;
- validation gate sequence: future Phase 4bh implementation must be followed by Phase 4bi-A structural QA → Phase 4bi-B feature-family eligibility-gate → Phase 4bi-C feature-family research-use decision → Phase 4bi-D successor-state recording (each separately authorized);
- M0 / cooled-down / no-rescue / cost-realism / acquisition boundaries all preserved verbatim.

---

## Validation

| Check | Result |
| ----- | ------ |
| `git diff --stat` (pre-commit) | 3 docs files changed (only the two new memos and the narrow `current-project-state.md` paragraph) |
| `git diff --name-only` | docs only |
| `ruff check .` | All checks passed |
| `pytest tests/research/microstructure/` | 492 passed |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py`; identical to pre-Phase-4bh-A baseline) |
| `mypy src/prometheus` (strict) | Success: no issues found in 101 source files |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |

Phase 4bh-A introduces zero new test regressions.

---

## What Phase 4bh-A did NOT do

- did not modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, or runtime configuration;
- did not implement, run, or rerun any gate, normalizer, feature pipeline, or backtest;
- did not generate a new gate report, feature dataset, feature manifest, or successor-state artefact;
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
- did not authorize Phase 4bh, Phase 4bh-B, Phase 4bi-A, Phase 4bi-B, Phase 4bi-C, Phase 4bi-D, Phase 4bj, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- did not commit anything under `data/microstructure/`.

---

## Preserved boundaries

H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 retained verdict ledger preserved verbatim. §11.6 / §1.7.3 / Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w project locks preserved verbatim. Phase 4ak M0 (12-clause gate + post-null cooldown + cooled-down families list + memo template) preserved. Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy preserved. Phase 4am / 4an / 4ao / 4ap / 4aq / 4ar / 4as / 4at / 4au / 4av / 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B results preserved verbatim.

---

## Recommended state

**Remain paused.**

Conditional next options (none authorized by Phase 4bh-A):

- future docs-only **Phase 4bh-B** — AggTrades Feature Schema Finalization Memo;
- future docs + code + local gitignored output **Phase 4bh** — AggTrades Feature Schema / Feature Computation Implementation;
- future analysis + docs **Phase 4bi-A** — Feature Artefact Structural QA Memo;
- future code + docs **Phase 4bb-F** — Gate Report Output Path Hygiene;
- future docs-only or docs-and-local-gitignored-output **Phase 4bb-G** — Raw Manifest Successor-State Recording.

**No successor phase is authorized by Phase 4bh-A.**
