# Phase 4bi-C — Closeout

**Phase identity:** Phase 4bi-C — Feature-Family Research-Use / ML-Use Decision Memo (docs-only).
**Date:** 2026-05-10.
**Branch:** `phase-4bi-c/feature-family-research-ml-use-decision`.
**Base:** `main` at the post-Phase-4bi-B merge-closeout state. Phase 4bi-B merge commit `046ec90ddfefb3c59164740eaf572ce104fb060f` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.

---

## Summary

Phase 4bi-C is a docs-only research-use / ML-use decision memo. It evaluates whether the feature family `microstructure_features_aggtrades_v001` is admissible in principle for a future Stage-5 research-use / ML-use admissibility recording, given the completed Stage-1 (Phase 4bh implementation), Stage-2 (Phase 4bh local artefacts), Stage-3 (Phase 4bi-A 67/67 + 18/18 PASS), and report-level Stage-4 (Phase 4bi-B 70/70 PASS; report SHA `aa5d29c2…`) evidence.

**Recorded decision (Outcome 1 / Decision form 1):**

> Stage-5 research-use / ML-use admissibility is admissible in principle at policy level for the feature family `microstructure_features_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bi-D successor-state recording phase is required before any machine-readable Stage-5 marker exists.

The feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` remains `research_eligible=false` and `eligibility_gate_status=pending` throughout Phase 4bi-C. The raw family `microstructure_raw_aggtrades_v001` remains permanently `research_eligible=false`. The derived family `microstructure_normalized_aggtrades_v001` retains `research_eligible=false` / `eligibility_gate_status=pending` on the actual manifest. Labels, targets, signals, ML, strategy, backtests, and acquisition all remain forbidden.

---

## Files added (tracked in git)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-c_feature-family-research-ml-use-decision.md` (the main memo).
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-c_closeout.md` (this file).

## Files modified narrowly (tracked in git)

- `docs/00-meta/current-project-state.md` — narrow Phase 4bi-C paragraph + new "Current phase:" block; prior Phase 4bi-B block preserved as historical context.

## Files NOT modified

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No file under `data/`, `data/manifests/`, `data/microstructure/`, `data/research/`, `data/derived/`, `data/raw/`, or `data/normalized/`.
- No file under `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, `data/microstructure/features/`, or `data/microstructure/gate-reports/`.
- `.gitignore` is unchanged.
- `pyproject.toml` is unchanged.
- `README.md` is unchanged.
- No prior memo (other than the narrow `current-project-state.md` paragraph addition).
- No script under `scripts/...` was created or modified.
- The Phase 4bb-D raw gate report and paired sidecar are unchanged.
- The Phase 4bd normalized parquet and derived manifest are unchanged.
- The Phase 4bf gate report and paired sidecar are unchanged.
- The Phase 4bg-B successor-state JSON and paired sidecar are unchanged.
- The Phase 4bh feature parquet and feature manifest are unchanged.
- The Phase 4bi-B gate report and paired sidecar are unchanged.

---

## Validation

| Check | Result |
| ----- | ------ |
| `git diff --stat` (pre-commit) | 3 docs files changed (only the two new memos and the narrow `current-project-state.md` paragraph) |
| `git diff --name-only` | docs only |
| `ruff check .` | All checks passed |
| `pytest tests/research/microstructure/` | 666 passed |
| Whole-repo `pytest` | 1 449 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py`; identical to the pre-Phase-4bi-C baseline) |
| `mypy src/prometheus` (strict) | Success: no issues found in 110 source files |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/features/` | gitignored under `.gitignore:85` |
| `git check-ignore -v data/microstructure/manifests/` | gitignored under `.gitignore:85` |
| `git check-ignore -v data/microstructure/gate-reports/features/` | gitignored under `.gitignore:85` |
| Manifest state (raw) | `research_eligible=false`, `eligibility_gate_status=pending` |
| Manifest state (derived) | `research_eligible=false`, `eligibility_gate_status=pending` |
| Manifest state (feature) | `research_eligible=false`, `eligibility_gate_status=pending` |
| Phase 4bi-B gate report SHA256 (recomputed) | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` (matches sidecar) |

Phase 4bi-C introduces zero new test regressions.

---

## Pre/post immutability evidence

The following SHAs were verified at the start of Phase 4bi-C and remained unchanged at the end (Phase 4bi-C does not write under `data/microstructure/`):

| Artefact | SHA256 |
| -------- | ------ |
| Feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| Normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Phase 4bi-B feature-family gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked by Phase 4bi-C).

---

## Decision recorded

**Outcome 1 / Decision form 1 (verbatim from the main memo §19):**

> **Stage-5 research-use / ML-use admissibility is admissible in principle at policy level for the feature family `microstructure_features_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bi-D successor-state recording phase is required before any machine-readable Stage-5 marker exists.**

Specifically:

- the feature manifest remains `research_eligible=false` and `eligibility_gate_status=pending` throughout Phase 4bi-C;
- no machine-readable Stage-5 marker exists yet;
- a future Phase 4bi-D would be required to create a sibling successor-state artefact while preserving the feature manifest byte-identically;
- labels, targets, ML, strategy, backtests, and acquisition all remain forbidden;
- Stage-5 admissibility is **not** a strategy hypothesis, predictive claim, edge claim, backtest permission, or M0 bypass;
- Phase 4ak M0 admissibility gate, post-null cooldown rule, cooled-down families list, and Phase 4al refined no-rescue rule remain binding;
- §11.6 / §1.7.3 / Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w preserved verbatim.

---

## What Phase 4bi-C did NOT do

- did not modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, or runtime configuration;
- did not implement, run, or rerun any gate, normalizer, feature kernel, or backtest;
- did not generate a new gate report;
- did not create a new normalized parquet, derived manifest, feature parquet, feature manifest, successor-state artefact, or any `data/microstructure/` artefact;
- did not delete, move, rename, or modify any existing `data/microstructure/` file;
- did not modify the Phase 4az raw manifest, raw zip, sidecar, or acquisition log;
- did not modify the Phase 4bb-D raw gate report or its sidecar;
- did not modify the Phase 4bd normalized parquet or derived manifest;
- did not modify the Phase 4bf derived-family gate report or its sidecar;
- did not modify the Phase 4bg-B successor-state JSON or its sidecar;
- did not modify the Phase 4bh feature parquet or feature manifest;
- did not modify the Phase 4bi-B feature-family gate report or its sidecar;
- did not create JSONL, DuckDB, feature, label, target, signal, proxy, ML, or strategy artefacts;
- did not acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request credentials, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- did not compute features, taker imbalance, sweep detection, aggressive-flow score, spread / depth / liquidity / slippage / order-flow / execution-quality proxies, returns, alpha, edge, predictiveness, signal quality, profitability, opportunity rate, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position state, prediction, model score, or decision score;
- did not flip `research_eligible` on any family;
- did not transition `eligibility_gate_status` on any actual manifest;
- did not authorize Stage-5 implementation, feature-family successor-state recording, label / target design, ML, strategy, or backtests;
- did not revise retained verdicts, change project locks, or amend M0;
- did not authorize Phase 4bi-D, Phase 4bj, Phase 4bj-A, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- did not commit anything under `data/microstructure/`.

---

## Preserved boundaries

H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 retained verdict ledger preserved verbatim. §11.6 / §1.7.3 / Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w project locks preserved verbatim. Phase 4ak M0 (12-clause gate + post-null cooldown + cooled-down families list + memo template) preserved. Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy preserved. Phase 4am / 4an / 4ao / 4ap / 4aq / 4ar / 4as / 4at / 4au / 4av / 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B results preserved verbatim.

---

## Recommended state

**Remain paused.**

Conditional next options (none authorized by Phase 4bi-C):

- future docs-and-local-gitignored-output **Phase 4bi-D** — Feature-Family Successor-State Recording (records the Stage-5 research-use / ML-use admissibility marker in a sibling successor-state JSON while preserving the feature manifest byte-identically; conditional next given Outcome 1);
- future docs-only **Phase 4bj-A** — Label Boundary / Target Definition Memo (only after Stage-5 successor-state is in place);
- future code-and-docs **Phase 4bb-F** — Gate Report Output Path Hygiene (only before any future repeated raw or feature-family gate execution);
- future docs-only or docs-and-local-gitignored-output **Phase 4bb-G** — Raw Manifest Successor-State Recording.

**No successor phase is authorized by Phase 4bi-C.**
