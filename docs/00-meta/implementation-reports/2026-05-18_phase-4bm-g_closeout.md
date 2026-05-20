# Phase 4bm-G — Closeout

**Phase identity:** Phase 4bm-G — Multi-Day V002 Feature-Boundary Design Memo (docs-only).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-g/multi-day-v002-feature-boundary-design-memo`.
**Base:** `main` at `bc7fa817ec712d296f9cd88dec89136b818edcbd` (Phase 4bm-F merge-closeout SHA-finalization commit; pre-branch `main == origin/main` in sync).
**Tier:** Tier 1 (docs-only Full Phase; governance / boundary-design memo; multi-day v002 analogue of Phase 4bh-A and the Phase 4bh-B schema-finalization layer it eventually fed).
**Status:** drafted; pending operator review.

---

## Summary

Phase 4bm-G is a docs-only Tier 1 feature-boundary design memo — the multi-day v002 analogue of the Phase 4bh-A v001 Feature-Boundary Design Memo (with elements of Phase 4bh-B v001 feature schema finalization included for completeness in a single docs phase). It defines the feature boundary that any future multi-day v002 feature work on the Stage-3 successor-state-marked normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events) must respect before any v002 feature-computation phase is authorized. The memo reaches **v002 Feature Stage-0** only (feature schema designed on paper; no code, no data, no artefact).

**Feature-boundary design is not feature computation.** **Stage-4 is not authorized by Phase 4bm-G.** **Phase 4bm-H is not authorized by Phase 4bm-G.** **No v002 feature artefact exists after Phase 4bm-G.**

The memo records: the current v002 lifecycle state through Stage-3 (with explicit citation of the Phase 4bm-F successor-state JSON SHA `72b6edd4…` as the only Stage-3 marker); the upstream lineage SHA table for the future v002 feature implementation; the direct comparison to Phase 4bh-A / Phase 4bh-B v001 feature-boundary precedent; the explicit statement that v001 feature-boundary work does not transitively authorize v002 feature computation; the proposed future v002 feature family naming (`microstructure_features_aggtrades_v001` with `dataset_version = v002`), feature manifest path, feature parquet path, schema design (lineage / timestamp / source-row-identity / non-feature-retained / computed-feature / forbidden columns); the allowed feature categories (A–H: count/intensity, buy/sell aggressor imbalance, volume/notional, price-movement causal descriptors, inter-arrival/activity-rate, rolling-window descriptive, time-of-day, data-quality); the forbidden feature categories (with a binding forbidden-substring detector); the timestamp/leakage policy (UTC only; no future-looking windows; explicit closed/open interval; deterministic sorting; same-timestamp tie-break by `row_index ASC`; per-day boundary handling; multi-day rolling-window boundary handling); the decimal/precision policy; the multi-day partitioning policy; the chronological-split / research-split readiness rules; the 16 feature-boundary fail-closed rules; the 17 proposed future v002 feature-implementation acceptance criteria; the M0 admissibility boundary, cooled-down lane boundary, ML/strategy/backtest boundary, acquisition boundary; explicit non-authorization; preserved verdicts and locks; and the recommended state (remain paused).

---

## Files added (tracked in git)

- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-g_multi-day-v002-feature-boundary-design-memo.md` (the 24-section main memo).
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-g_closeout.md` (this file).

## Files modified narrowly (tracked in git)

- `docs/00-meta/current-project-state.md` — narrow Phase 4bm-G paragraph + new "Current phase:" block; prior Phase 4bm-F "Current phase:" block preserved as labelled historical context (pure addition, no deletions, consistent with the Phase 4bm-E / Phase 4bm-F precedent pattern).

## Files NOT modified

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No file under `data/`, `data/manifests/`, `data/microstructure/`, `data/research/`, `data/derived/`, `data/raw/`, or `data/normalized/`.
- No file under `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, `data/microstructure/gate-reports/`, or `data/microstructure/successor-state/`.
- `.gitignore`, `.gitattributes`, `pyproject.toml`, `README.md` are unchanged.
- No MCP file (`.mcp.json` absent before and after).
- No `.claude/settings.json`, `.claude/settings.local.json`, `.claude/hooks/`, or `.claude/agents/` file in `C:\Prometheus` modified or created.
- No prior governance memo (other than the narrow `current-project-state.md` paragraph addition).
- No prior implementation report, closeout, or merge-closeout modified.
- No prior process standard modified.
- The Phase 4bm-F v002 derived successor-state JSON (`72b6edd4…`) and its paired sidecar (`1e9ffb23…`) are unchanged.
- The Phase 4bm-D authoritative gate report (`3b45e70b…`) and its sidecar (`8e74261c…`) are unchanged.
- The v002 derived multi-day index manifest (`01c5fa53…`) and its sidecar (`d96f31ae…`) are unchanged.
- The v002 raw manifest (`01696786…`), v002 acquisition log (`52f6d7fb…`), 90 v002 raw zips, and 90 v002 raw zip sidecars are unchanged.
- The 90 v002 per-day Parquets and 90 paired sidecars (Phase 4bm-B outputs) are unchanged.
- The Phase 4bl-D-R raw multi-day PASS gate report (`f9493fd1…`) and its sidecar are unchanged.
- The Phase 4bl-E raw multi-day successor-state JSON (`a0576ca6…`) and its sidecar are unchanged.
- The Phase 4bd v001 normalized Parquet (`2b3d6978…`) and v001 derived manifest (`f6f0d947…`) are unchanged.
- The Phase 4az v001 raw artefacts (`a371edd4…`, `f560c2e5…`, `b80c2768…`, `f88b28b4…`) are unchanged.
- The Phase 4bb-D v001 raw gate report (`96f09159…`), Phase 4bf v001 derived gate report (`dd4e0c1c…`), Phase 4bg-B v001 derived successor-state JSON (`8bcc7d01…`), Phase 4bb-G v001 raw successor-state JSON, Phase 4bh v001 feature parquet and manifest (if present), Phase 4bj-C v001 label parquet and manifest (if present), Phase 4bj-G v001 label successor-state JSON (if present), Phase 4bi-D v001 feature successor-state JSON (if present), and Phase 4bj-J v001 label split-policy successor-state JSON (if present) are all unchanged.

---

## Validation

| Check | Result |
| ----- | ------ |
| `git status --short` (pre-commit) | only the three tracked Phase 4bm-G files (1 M `current-project-state.md` + 2 A memos) plus the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`) — recorded in the final operator report |
| `git diff --check` (pre-commit) | clean (no whitespace errors, no merge markers) — recorded in the final operator report |
| `git branch --show-current` | `phase-4bm-g/multi-day-v002-feature-boundary-design-memo` |
| `git rev-parse main` | `bc7fa817ec712d296f9cd88dec89136b818edcbd` (base for the Phase 4bm-G branch) |
| `git rev-parse origin/main` | `bc7fa817ec712d296f9cd88dec89136b818edcbd` (`main == origin/main` in sync) |
| Manifest state (v002 derived multi-day index) | `research_eligible=false`, `eligibility_gate_status="pending"`; SHA256 `01c5fa53…` (verified on disk by this phase) |
| Manifest state (v002 raw) | `research_eligible=false`, `eligibility_gate_status="pending"`; SHA256 `01696786…` (verified on disk by this phase) |
| Manifest state (v001 derived) | `research_eligible=false`, `eligibility_gate_status="pending"`; SHA256 `f6f0d947…` (verified on disk by this phase) |
| Phase 4bm-D authoritative gate report SHA (recomputed on disk) | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` — matches the value recorded in the Phase 4bm-D / Phase 4bm-E / Phase 4bm-F merge-closeouts |
| Phase 4bm-D authoritative sidecar SHA (recomputed on disk) | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` — matches |
| Phase 4bm-F v002 derived successor-state JSON SHA (recomputed on disk) | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` — matches the Phase 4bm-F closeout |
| Phase 4bm-F v002 derived sidecar SHA (recomputed on disk) | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` — matches the Phase 4bm-F closeout |
| Phase 4bl-D-R raw multi-day PASS gate report SHA (recomputed on disk) | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` — matches |
| Phase 4bl-E raw multi-day successor-state JSON SHA (recomputed on disk) | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` — matches |
| Phase 4bg-B v001 derived successor-state JSON SHA (recomputed on disk; precedent cross-reference) | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` — matches |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/features/` | n/a — the `data/microstructure/features/` directory does not exist (no future feature artefact has been created by Phase 4bm-G; the namespace would inherit the existing `.gitignore:85` rule if it ever existed) |

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by Phase 4bm-G. Per the Phase 4bk-A workflow standard, the Phase 4bl-F risk-tiering standard, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight-workspace standard, and the established Tier 1 docs-only governance / boundary-design memo precedent — **Phase 4bh-A (the direct v001 feature-boundary design memo that this phase mirrors)**, Phase 4bh-B (v001 feature schema finalization), Phase 4bg-A, Phase 4bi-A, Phase 4bi-C, Phase 4bj-A, Phase 4bj-B, Phase 4bj-D, Phase 4bj-F, Phase 4bj-H, Phase 4bj-I, Phase 4bj-K, Phase 4bk-A, Phase 4bl-A, Phase 4bl-B, Phase 4bl-D-S1, Phase 4bl-F, Phase 4bm-A, Phase 4bm-A-P1, Phase 4bm-C, Phase 4bm-D-P1, and Phase 4bm-E each deliberately skipped these gates for the same reason — the code / type / test gate subset is not invoked here. No source / test / script / configuration file is modified. The most recent authoritative whole-repo `pytest` baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; two pre-existing `KeyError: 'trade_count'` simulation failures on `tests/simulation/test_backtest_real_2026_03.py` in `src/prometheus/research/data/storage.py:232` are unrelated to Phase 4bm-G and are preserved as the baseline). Phase 4bm-G introduces zero new test regressions by construction.

---

## Pre/post immutability evidence

The following 10 evidence artefacts were verified byte-identical at the start of Phase 4bm-G and remain byte-identical at the end (Phase 4bm-G does not write under `data/microstructure/` and does not touch any tracked file outside the three docs files listed above):

| Artefact | SHA256 (pre and post Phase 4bm-G) |
| -------- | ---------------------------------- |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| v001 derived manifest (Phase 4bd) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Phase 4bm-D authoritative derived gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| Phase 4bl-D-R raw multi-day `RAW_MULTIDAY_GATE_PASS` report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| Phase 4bg-B v001 derived successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| **Phase 4bm-F v002 derived successor-state JSON** | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` |
| **Phase 4bm-F v002 derived sidecar** | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` |

The 90 v002 per-day Parquets, 90 v002 sidecars, 90 v002 raw zips, and 90 v002 raw zip sidecars are unchanged byte-for-byte by Phase 4bm-G by construction (Phase 4bm-G reads no Parquet, runs no kernel, and writes nothing under `data/microstructure/`).

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked by Phase 4bm-G).

---

## Decision recorded

**v002 Feature Stage-0 reached.** Phase 4bm-G defines the feature boundary for any future multi-day v002 feature work on the Stage-3 successor-state-marked normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`). The memo records (verbatim from the main memo §22 and §23):

- the canonical v002 input (`microstructure_normalized_aggtrades_v001` `dataset_version=v002`) and forbidden inputs;
- the proposed future v002 feature family name `microstructure_features_aggtrades_v001` `dataset_version=v002` (multi-day analogue of the Phase 4bh-A / Phase 4bh-B v001 proposal, with `dataset_version=v002`);
- the proposed future v002 feature manifest path `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` (NOT created);
- the proposed future v002 per-day feature Parquet output namespace `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/...` (NOT created; the directory does not exist);
- the future v002 feature schema design including lineage / timestamp / source-row-identity / non-feature-retained / computed-feature / forbidden columns;
- the allowed v002 feature categories A–H (count/intensity, buy/sell aggressor imbalance, volume/notional, price-movement causal descriptors, inter-arrival/activity-rate, rolling-window descriptive, time-of-day, data-quality);
- the forbidden v002 feature categories (with a binding forbidden-substring detector listing 26 forbidden tokens);
- the timestamp/leakage policy (UTC only; no future-looking windows; explicit `(T - window_ms, T]` closed/open interval; deterministic `(transact_time_ms ASC, row_index ASC)` sorting; same-timestamp tie-break by `row_index ASC`; per-day boundary handling; three admissible multi-day rolling-window boundary policies with the recommended default of causal cross-day lookback);
- the decimal/precision policy (Decimal-as-string for raw price/quantity and quantity-derived sums; float64 permitted only for dimensionless ratios and log returns; explicit float justification required for any other float feature);
- the multi-day partitioning policy (90 per-day v002 feature Parquets one-per-`(symbol, utc_date)` partition; warm-up handling for day 1; invalid-window propagation discipline);
- the chronological-split / research-split readiness rules (no split assigned; future v002 split-policy memo required before ML/backtest use; strictly chronological; no random shuffle; no boundary leakage);
- the 16 feature-boundary fail-closed rules (missing successor-state JSON; SHA mismatch on any of the 7 lineage artefacts; any missing lineage field; any future-looking feature; any forbidden column; any monotonicity violation; any manifest mutation attempt; network/credential discipline; path discipline; refuse-to-overwrite; static-import discipline);
- the 17 proposed future v002 feature-implementation acceptance criteria.

The Phase 4bm-F v002 successor-state JSON SHA `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` is cited as the **only** machine-readable Stage-3 marker for the multi-day v002 derived family. The original v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` continues to carry `research_eligible = false` and `eligibility_gate_status = "pending"` byte-identically (SHA `01c5fa53…`). The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## What Phase 4bm-G did NOT do

- did not compute features;
- did not create feature files, datasets, manifests, sidecars, or feature-config files for v002 (or v001);
- did not create the `data/microstructure/features/` namespace;
- did not modify source code, tests, scripts, configs, `README.md`, `pyproject.toml`, `.gitignore`, `.gitattributes`, MCP files, runtime configuration, or `.claude/` files in `C:\Prometheus`;
- did not implement, run, or rerun any gate, normalizer, structural QA, diagnostics, or backtest;
- did not generate a new gate report;
- did not create a new normalized Parquet, derived manifest, successor manifest, successor-state JSON, sibling artefact, or any `data/microstructure/` artefact;
- did not delete, move, rename, or modify any existing `data/microstructure/` file;
- did not modify the Phase 4az v001 raw manifest, raw zip, sidecar, or acquisition log;
- did not modify the Phase 4bl-C v002 raw manifest, raw zips, sidecars, or acquisition log;
- did not modify the Phase 4bb-D v001 raw gate report or its sidecar;
- did not modify the Phase 4bl-D-R v002 raw multi-day gate report or its sidecar;
- did not modify the Phase 4bl-E v002 raw successor-state JSON or its sidecar;
- did not modify the Phase 4bd v001 normalized Parquet or v001 derived manifest;
- did not modify the Phase 4bm-B v002 normalized Parquets (90 files), v002 derived manifest, or v002 derived sidecar;
- did not modify the Phase 4bf v001 derived gate report, the Phase 4bm-D v002 derived gate report, or any sidecar;
- did not modify the Phase 4bg-B v001 derived successor-state JSON, the Phase 4bm-F v002 derived successor-state JSON, or any other successor-state artefact;
- did not modify any Phase 4bh / Phase 4bj-C / Phase 4bj-G / Phase 4bi-D / Phase 4bj-J v001 feature / label / successor-state artefact (if present locally);
- did not create JSONL, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts on v002 or v001;
- did not acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request credentials, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- did not compute features, taker imbalance, sweep detection, aggressive-flow score, spread / depth / liquidity / slippage / order-flow / execution-quality proxies, returns, alpha, edge, predictiveness, signal quality, profitability, opportunity rate, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- did not flip `research_eligible` on any family;
- did not transition `eligibility_gate_status` on any actual manifest;
- did not change `chronological_split_policy` on any actual manifest;
- did not authorize Stage-3 manifest transition, Stage-4 feature-cleared status, feature computation, ML, strategy, or backtests on v002 (or on v001);
- did not revise any retained verdict;
- did not change any project lock;
- did not amend M0;
- did not amend the Phase 4al refined no-rescue rule;
- did not amend the Phase 4aw `flip_research_eligible(...)` always-raises invariant;
- did not amend the Phase 4bb-F canonical path policy;
- did not amend the Phase 4bl-F four-tier risk model, R-SIDECAR-CRLF standing rule, or nine reusable non-authorization blocks;
- did not amend the Phase 4bm-A-P1 thin-prompt Claude Code context-management standard;
- did not amend the Phase 4bm-D-P1 lightweight Claude Code workspace execution standard;
- did not amend the Phase 4bm-E decision (Option B / Decision form 2 preserved verbatim);
- did not authorize Phase 4bm-G merge phase, Phase 4bm-H, any multi-day v002 feature schema finalization memo, any multi-day v002 feature artefact structural QA memo, any multi-day v002 feature-family eligibility-gate phase, any multi-day v002 feature-family research-use decision memo, any multi-day v002 feature-family successor-state recording, any multi-day v002 label-family phase, Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- did not commit anything under `data/microstructure/`.

Reusable non-authorization blocks per `docs/00-meta/process/phase-risk-tiering-standard.md` §7 honoured by this phase: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

---

## Preserved boundaries

H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 retained verdict ledger preserved verbatim. §11.6 / §1.7.3 / Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w project locks preserved verbatim. Phase 4ak M0 (12-clause gate + post-null cooldown + cooled-down families list + memo template) preserved. Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy preserved. Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked). Phase 4bb-F canonical path policy preserved. Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks preserved. Phase 4bm-A-P1 thin-prompt Claude Code context-management standard preserved. Phase 4bm-D-P1 lightweight Claude Code workspace execution standard preserved. Phase 4am .. Phase 4bm-F results preserved verbatim.

---

## Recommended state

**Remain paused.**

Phase 4bm-G is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

Conditional next options (none authorized by Phase 4bm-G):

- future code + docs + local gitignored feature artefacts **Phase 4bm-H — Multi-Day V002 Feature Schema / Feature Computation Implementation** (multi-day analogue of Phase 4bh; would compute v002 features locally under `data/microstructure/features/microstructure_features_aggtrades_v001/...`; would produce gitignored per-day feature Parquets + sidecars + future v002 feature manifest; would not authorize ML, strategy, label, diagnostics, or backtest work);
- future docs-only multi-day v002 feature schema finalization memo (multi-day analogue of Phase 4bh-B), if the operator chooses to separate design from finalization;
- future multi-day v002 feature artefact structural QA memo (multi-day analogue of Phase 4bi-A);
- future multi-day v002 feature-family eligibility-gate design + implementation + execution (multi-day analogue of Phase 4bi-B);
- future multi-day v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C);
- future multi-day v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D);
- future multi-day v002 label-family phases (multi-day analogues of Phase 4bj-A through Phase 4bj-K);
- future multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / Phase 4bj-I / Phase 4bj-J).

**No successor phase is authorized by Phase 4bm-G.**

---

## Phase 4bm-G / Phase 4bm-H / feature-boundary / feature implementation / ML / strategy / backtest authorization status

**Phase 4bm-H and all successors remain unauthorized.** This phase does not, and cannot, be construed as authorising Phase 4bm-G merge phase, Phase 4bm-H, any multi-day v002 feature schema finalization memo, any multi-day v002 feature implementation phase, any multi-day v002 feature-family / label-family phase, Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical / any other successor; feature computation; label computation; signal computation; diagnostics rerun; ML training / model selection / feature ranking / meta-labeling; strategy implementation / signal construction / backtest implementation; additional acquisition (beyond the 90 locked v002 BTCUSDT UTC dates); cross-symbol acquisition; paper / shadow; live-readiness; deployment; exchange-write; production-key creation; authenticated APIs; private endpoints; public-endpoint calls in code; user-stream / live WebSocket implementation; MCP / Graphify / `.mcp.json` / credentials; any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` on any on-disk manifest; any further successor-state JSON creation; agents-by-default for heavy Claude Code execution sessions; copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light`.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard, and merge-closeout standard.

**Feature-boundary design is not feature computation. Stage-4 is not authorized by Phase 4bm-G. Phase 4bm-H is not authorized by Phase 4bm-G. No v002 feature artefact exists after Phase 4bm-G.**
