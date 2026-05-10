# Phase 4bg-A — Closeout

**Phase identity:** Phase 4bg-A — Derived-Family Research-Eligibility Decision Memo (docs-only).
**Date:** 2026-05-10.
**Branch:** `phase-4bg-a/derived-family-research-eligibility-decision`.
**Base:** `main` at the post-Phase-4bf merge-closeout state (Phase 4bf merge commit `cad383cd5e85dae6b96fa83650d211842d5e070f` confirmed as ancestor of `main`).
**Status:** drafted; pending operator review.

---

## Summary

Phase 4bg-A is a docs-only research-eligibility decision memo. It evaluates whether the normalized derived family `microstructure_normalized_aggtrades_v001` is admissible in principle for a future Stage-3 research-eligibility transition, given the completed Stage-0 (Phase 4bd), Stage-1 (Phase 4be 60 / 60 PASS), and report-level Stage-2 (Phase 4bf 55 / 55 PASS; report SHA `dd4e0c1c…`) evidence.

**Recorded decision (Option B / Decision form 2):**

> Stage-3 is admissible in principle at policy level for the normalized derived family, but no manifest mutation occurs in this phase. A separately authorized successor-state recording phase is required before any machine-readable `research_eligible=true` marker exists.

The raw family `microstructure_raw_aggtrades_v001` remains permanently `research_eligible=false`. The actual derived manifest remains `research_eligible=false` and `eligibility_gate_status=pending` throughout Phase 4bg-A. Feature computation, ML, strategy work, and backtests remain forbidden until a separately authorized Stage-4 feature-boundary design memo and a separately authorized feature implementation phase.

---

## Files added (tracked in git)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_derived-family-research-eligibility-decision.md` (the main memo).
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_closeout.md` (this file).

## Files modified narrowly (tracked in git)

- `docs/00-meta/current-project-state.md` — narrow Phase 4bg-A paragraph + new "Current phase:" block; prior Phase 4bf block preserved as historical context.

## Files NOT modified

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No file under `data/`, `data/manifests/`, `data/microstructure/`, `data/research/`, `data/derived/`, `data/raw/`, or `data/normalized/`.
- No file under `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, or `data/microstructure/gate-reports/`.
- `.gitignore` is unchanged.
- `pyproject.toml` is unchanged.
- `README.md` is unchanged.
- No prior memo (other than the narrow `current-project-state.md` paragraph addition).
- No script under `scripts/...` was created or modified.
- The Phase 4bb-D raw gate report and paired sidecar are unchanged.
- The Phase 4bd normalized Parquet and derived manifest are unchanged.
- The Phase 4bf gate report and paired sidecar are unchanged.

---

## Validation

| Check | Result |
| ----- | ------ |
| `git diff --stat` (pre-commit) | 3 docs files changed (only the two new memos and the narrow `current-project-state.md` paragraph) |
| `git diff --name-only` | docs only |
| `ruff check .` | All checks passed |
| `pytest tests/research/microstructure/` | 492 passed |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py`; identical to the pre-Phase-4bg-A baseline) |
| `mypy src/prometheus` (strict) | Success: no issues found in 101 source files |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/gate-reports/normalized/` | `.gitignore:85: data/microstructure/` |
| Manifest state (raw) | `research_eligible=false`, `eligibility_gate_status=pending` |
| Manifest state (derived) | `research_eligible=false`, `eligibility_gate_status=pending` |
| Phase 4bf gate report SHA256 (recomputed) | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` (matches sidecar) |

Phase 4bg-A introduces zero new test regressions.

---

## Pre/post immutability evidence

The following SHAs were verified at the start of Phase 4bg-A and remained unchanged at the end (Phase 4bg-A does not write under `data/microstructure/`):

| Artefact | SHA256 |
| -------- | ------ |
| derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| raw sidecar | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` |
| acquisition log | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end.

---

## Decision recorded

**Option B / Decision form 2 (verbatim from the main memo §20):**

> **Stage-3 is admissible in principle at policy level for the normalized derived family `microstructure_normalized_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized successor-state recording phase is required before any machine-readable `research_eligible=true` marker exists.**

Specifically:

- raw family remains `research_eligible=false` permanently;
- actual derived manifest remains `research_eligible=false` and `eligibility_gate_status=pending` in Phase 4bg-A;
- no data, feature, ML, strategy, or backtest work is authorized;
- the next safe phase is one of: future Phase 4bg-B (successor-state policy / recording memo), future Phase 4bh-A (feature-boundary design memo), or remain paused;
- Stage-4 authorization is not implied;
- Phase 4ak M0 admissibility gate, post-null cooldown rule, cooled-down families list, and Phase 4al refined no-rescue rule remain binding;
- §11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w preserved verbatim.

---

## What Phase 4bg-A did NOT do

- did not modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, or runtime configuration;
- did not implement, run, or rerun any gate, normalizer, or backtest;
- did not generate a new gate report;
- did not create a new normalized Parquet, derived manifest, successor manifest, or any `data/microstructure/` artefact;
- did not delete, move, rename, or modify any existing `data/microstructure/` file;
- did not modify the Phase 4az raw manifest, raw zip, sidecar, or acquisition log;
- did not modify the Phase 4bb-D raw gate report or its sidecar;
- did not modify the Phase 4bd normalized Parquet or derived manifest;
- did not modify the Phase 4bf derived-family gate report or its sidecar;
- did not create JSONL, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- did not acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request credentials, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- did not compute features, taker imbalance, sweep detection, aggressive-flow score, spread / depth / liquidity / slippage / order-flow / execution-quality proxies, returns, alpha, edge, predictiveness, signal quality, profitability, opportunity rate, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- did not flip `research_eligible` on any family;
- did not transition `eligibility_gate_status` on any actual manifest;
- did not authorize Stage-3 manifest transition, Stage-4 feature-cleared status, feature computation, ML, strategy, or backtests;
- did not revise retained verdicts, change project locks, or amend M0;
- did not authorize Phase 4bg-B, Phase 4bh-A, Phase 4bh, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- did not commit anything under `data/microstructure/`.

---

## Preserved boundaries

H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 retained verdict ledger preserved verbatim. §11.6 / §1.7.3 / Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w project locks preserved verbatim. Phase 4ak M0 (12-clause gate + post-null cooldown + cooled-down families list + memo template) preserved. Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy preserved. Phase 4am / 4an / 4ao / 4ap / 4aq / 4ar / 4as / 4at / 4au / 4av / 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf results preserved verbatim.

---

## Recommended state

**Remain paused.**

Conditional next options (none authorized by Phase 4bg-A):

- future docs-only **Phase 4bg-B** — Derived-Family Research-Eligibility Successor-State Policy / Recording memo;
- future docs-only **Phase 4bh-A** — Feature-Boundary Design memo;
- future code + docs **Phase 4bh** — Feature Schema / Feature Computation implementation (only after Stage-4 authorization);
- future code + docs **Phase 4bb-F** — Gate Report Output Path Hygiene (only before any repeated raw gate execution);
- future docs-only or docs-and-local-gitignored-output **Phase 4bb-G** — Raw Manifest Successor-State Recording.

**No successor phase is authorized by Phase 4bg-A.**
