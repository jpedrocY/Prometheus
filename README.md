# Prometheus

Prometheus is a **production-oriented, safety-first, operator-supervised trading system** for **Binance USDⓈ-M futures**.

The v1 project is intentionally **rules-based**, **not self-learning**, and built in **phases with review gates**, runnable checkpoints, and explicit human approval before any move toward real exchange-write capability.

## Current status

**Project state:** post-Phase 4az (first public aggTrades archive acquisition merged to `main`).

What that means right now:

- The project is **intentionally paused**. No new strategy candidate, fresh-hypothesis discovery, additional data acquisition, feature computation, normalization, ML, backtest, paper / shadow, live-readiness, deployment, exchange-write, production-key, MCP, Graphify, `.mcp.json`, or credential work is authorized.
- Six terminal strategy rejections are on the project record (see "Strategy research arc outcomes" below). The old OHLCV / V1-arc research is closed and governed by retained verdicts.
- The current active research arc is **crypto microstructure infrastructure** (Phases 4as → 4az). It is **infrastructure-first, not strategy-first**: the project now has its first real microstructure raw dataset, but the dataset is `research_eligible=false` and is **not** strategy evidence. No features, normalization, ML, strategy, or backtest were performed on it.
- **R3** remains the **baseline-of-record**; **H0** remains the framework anchor; **R1a** and **R1b-narrow** remain retained research evidence (non-leading).
- The **M0 mechanism-admissibility gate** is **binding prospective governance** for any future research lane (durable artifact: [docs/00-meta/m0-mechanism-admissibility-gate.md](docs/00-meta/m0-mechanism-admissibility-gate.md)).
- The **Phase 4a–4c local safe runtime foundation** is implemented and behind quality gates, but is strategy-agnostic and not authorized to place orders.
- Pytest baseline: **979 passing tests** with **2 pre-existing simulation failures** unrelated to the microstructure arc (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'` in the unrelated `src/prometheus/research/data/storage.py:232`); full-repo `ruff check .` clean; `mypy --strict` clean across 89 source files. Phase 4az introduced zero new regressions.

## Strategy research arc outcomes

The project has produced the V1/R-series baseline arc plus F1, D1-A, V2, G1, and C1 strategy-family investigations, followed by the alt-symbol substrate arc; none produced a newly validated deployable strategy.

| Strategy | Family signature                          | Verdict                                            |
| -------- | ----------------------------------------- | -------------------------------------------------- |
| H0       | V1 breakout framework anchor              | FRAMEWORK ANCHOR (preserved)                       |
| R3       | Fixed-R take-profit + unconditional time-stop | BASELINE-OF-RECORD                              |
| R1a      | Volatility-percentile setup predicate     | Retained research evidence — non-leading           |
| R1b-narrow | Bias-strength magnitude threshold       | Retained research evidence — non-leading           |
| R2       | V1 pullback-retest variant                | FAILED — §11.6 cost-sensitivity blocks             |
| F1       | Mean-reversion after overextension        | HARD REJECT (Phase 3d-B2 catastrophic-floor)       |
| D1-A     | Funding-aware contrarian directional rule | MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3j) |
| V2       | Participation-confirmed breakout          | HARD REJECT (Phase 4l — design-stage; zero trades) |
| G1       | Regime-first breakout continuation        | HARD REJECT (Phase 4r — gate × setup sparseness)   |
| C1       | Volatility-contraction expansion breakout | HARD REJECT (Phase 4x — fires-and-loses)           |

The 5m diagnostic thread (Phases 3o → 3p → 3q → 3r → 3s → 3t) is operationally closed.

The alt-symbol substrate arc (Phases 4aa → 4ai) on BTCUSDT / ETHUSDT / SOLUSDT / XRPUSDT / ADAUSDT produced descriptive cost-cushion / regime-continuity / cross-sectional ranking evidence, with the Phase 4ai cross-sectional ranking feasibility lane returning `NOT_SUPPORTED`. No strategy was promoted from substrate work.

After Phase 4y (post-C1 consolidation) and Phase 4z (post-rejection research-process redesign), the project pivoted to docs-only governance work: Phase 4ag mechanism-source triage; Phase 4ah / 4ai cross-sectional feasibility; Phase 4aj M0 governance reconciliation; Phase 4ak M0 governance adoption.

## Microstructure arc (Phases 4as → 4az)

After M0 governance adoption, the project opened a new infrastructure-first arc on Binance USDⓈ-M Futures public microstructure data. Each phase is documented in `docs/00-meta/implementation-reports/`.

| Phase  | Title                                                                            | Type                       |
| ------ | -------------------------------------------------------------------------------- | -------------------------- |
| 4as    | Crypto microstructure research reset and mechanism map                           | docs-only                  |
| 4at    | Binance microstructure data availability / capture feasibility                   | docs-only                  |
| 4au    | Binance microstructure capture design specification                              | docs-only                  |
| 4av    | Public-only microstructure capture implementation plan                           | docs-only                  |
| 4aw    | Inert public-only microstructure scaffold implementation                         | code-and-docs (scaffold)   |
| 4ax    | AggTrades-only public microstructure collector skeleton                          | code-and-docs (skeleton)   |
| 4ay    | AggTrades public archive acquisition authorization boundary                      | docs-only                  |
| 4az    | First public aggTrades archive acquisition (BTCUSDT, 2025-01-15 UTC)             | code-and-docs (acquisition) |

The Phase 4aw scaffold (`src/prometheus/research/microstructure/`) provides an inert public-only allowlist + denylist, a 17-trigger invalid-window taxonomy, a manifest data model with `research_eligible=False` default, and an atomic raw-writer primitive. The Phase 4ax aggTrades-only skeleton adds payload validation, taker-side derivation, dry-run plan building, and a temp-path writer composition. The Phase 4ay docs-only authorization-boundary memo defines the strict-integrity gate, staging plan, manifest contract, and fail-closed rules under which a future acquisition phase may run. Phase 4az is the first concrete acquisition that exercised that framework end-to-end on real public-archive data.

## Phase 4az dataset (acquired; infrastructure evidence only)

Phase 4az acquired exactly one Binance USDⓈ-M Futures aggTrades daily archive from the public `data.binance.vision` archive:

- **Symbol:** `BTCUSDT`
- **UTC date:** `2025-01-15`
- **Source:** public Binance archive (`data.binance.vision`) only — no Binance API endpoint, no REST polling, no WebSocket, no credentials, no `.env`, no private endpoints, no user stream, no listenKey
- **Mode:** `historical_archive` (one daily archive only)
- **Dataset family:** `microstructure_raw_aggtrades_v001`
- **Archive SHA256 (verified bit-for-bit against the published `.CHECKSUM`):** `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
- **Event count:** **1,681,098** rows, every one of which passed Phase 4ax `validate_aggtrade_payload`
- **UTC-day coverage:** every observed `T` in `[2025-01-15 00:00:00.000 UTC, 2025-01-16 00:00:00.000 UTC)` (first 1736899205109 ms; last 1736985599991 ms)
- **Local outputs:** raw `.zip`, paired `.sha256`, manifest, acquisition log under the **gitignored** `data/microstructure/` tree (line 85 of `.gitignore`); **none committed**, **none staged**
- **Manifest:** `research_eligible=false`, `eligibility_gate_status=pending`, `governance_labels.feature_computation=forbidden`, `governance_labels.strategy_use=forbidden`

The Phase 4az dataset is **infrastructure evidence only**. It is **not** strategy evidence. **No features were computed; no normalization to JSONL or Parquet was performed; no ML model was trained; no strategy candidate was created; no backtest was run; `research_eligible` is and remains `false` until a separately authorized eligibility-gate phase runs.**

## Current technical capabilities

What the repository currently has working on `main`:

- **Public-only microstructure scaffold** (`src/prometheus/research/microstructure/`): inert allowlist / denylist; 17-trigger invalid-window taxonomy; manifest data model with `research_eligible=False` default and no public flip helper; atomic raw-writer primitive; aggTrades payload validator; aggTrades dry-run plan builder; temp-path writer composition.
- **Phase 4az acquisition script** (`scripts/phase4az_acquire_btcusdt_aggtrades_archive.py`): standalone stdlib-only orchestrator with a `data.binance.vision`-only URL allowlist, parametrised denylist for Binance API hosts / private endpoints / credential-shaped strings / MCP / Graphify / `.mcp.json` / `.env`, dry-run mode, and `--output-root` refusal of paths outside `data/microstructure/`.
- **Phase 4a–4c local safe runtime foundation** (`src/prometheus/state`, `src/prometheus/persistence`, `src/prometheus/events`, `src/prometheus/risk`, `src/prometheus/execution/fake_adapter.py`, `src/prometheus/operator`, `src/prometheus/cli`): strategy-agnostic; not authorized to place orders.
- **Gitignored data tree:** `data/microstructure/` (Phase 4aw line). Nothing under it is committed.

What the repository explicitly does **not** have:

- No live REST polling of Binance API endpoints in code.
- No WebSocket capture (no `<symbol>@aggTrade`, `@bookTicker`, `@depth`, `@forceOrder`, mark-price stream, etc.).
- No private endpoints, no authenticated APIs, no credentials, no `.env` reads.
- No exchange-write capability.
- No MCP / Graphify / `.mcp.json`.
- No order-book reconstruction, no deterministic replay, no normalization to JSONL / Parquet, no eligibility-gate execution.
- No microstructure-derived feature, no microstructure-derived strategy candidate, no microstructure-derived ML model.

## What the project has not done yet

Prometheus has **not** started:

- paper / shadow operation,
- tiny-live preparation,
- scaled-live preparation,
- production Binance trade-capable key creation,
- live exchange-write capability,
- authenticated REST / private endpoints / user stream / WebSocket / listenKey integration in code,
- MCP / Graphify / `.mcp.json` / credentials work,
- additional microstructure data acquisition (no ETHUSDT, no alt symbols, no multi-day backfill, no monthly archive, no depth / bookTicker / forceOrder / OI / funding / mark-price / index-price / 5m / 1m / tick / order-book),
- normalization of the Phase 4az dataset into Parquet / JSONL,
- feature computation on the Phase 4az dataset,
- flipping `research_eligible` to `True` for the Phase 4az dataset,
- strategy candidate creation derived from microstructure data,
- ML model training on microstructure data.

Phase 4 canonical (paper / shadow / live-readiness gates) remains unauthorized. Phase 4ba is **not** authorized. The Phase 4a–4c runtime foundation that is implemented is local-only, fake-exchange, exchange-write-free, and strategy-agnostic per the Phase 3x scoping memo and Phase 4a authorization brief.

## Project locks (preserved verbatim across every phase)

- **§11.6** HIGH cost = 8 bps per side (round-trip = 16 bps).
- **§1.7.3** project-level locks: 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation governance.
- Phase 4j §11 metrics OI-subset partial-eligibility rule.
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy-spec discipline; Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy-spec discipline; Phase 4w C1 backtest-plan methodology.
- **M0 mechanism-admissibility gate** and **post-null cooldown rule** (binding prospective; adopted Phase 4ak).

## Safety principles

Prometheus is deliberately conservative.

- No production trade-capable Binance keys exist or are authorized.
- Credentials alone must never enable trading; live exchange-write capability requires explicit environment / config / phase-gate approval.
- Dry-run, fake-adapter, and paper / shadow stages must come before any tiny-live operation.
- Unknown state must fail closed; restart must begin in `SAFE_MODE`.
- Operator approval is required across major phase boundaries.
- Every future research lane must clear the **M0 admissibility gate** before discovery, hypothesis spec, strategy spec, or backtest work.

## Repository layout

```text
Prometheus/
├─ docs/                     # canonical project memory, specifications, governance, implementation reports
├─ src/prometheus/           # Phase 4a–4c local safe runtime foundation (state, persistence, events, governance,
│                            #   risk sizing/exposure/stop-validation, fake_adapter, operator, cli)
├─ tests/                    # 979 passing pytest tests; 2 pre-existing simulation failures unrelated to the microstructure arc
├─ scripts/                  # standalone phase research scripts (no runtime imports; no network I/O)
├─ data/                     # local research/runtime artifacts (most paths git-ignored)
└─ README.md                 # this file
```

For the full documentation map, read [docs/README.md](docs/README.md).

## Most important documents

Start here if you want to understand the repo quickly:

- [docs/00-meta/current-project-state.md](docs/00-meta/current-project-state.md) — high-level project memory checkpoint
- [docs/00-meta/m0-mechanism-admissibility-gate.md](docs/00-meta/m0-mechanism-admissibility-gate.md) — binding prospective governance for any future research lane
- [docs/00-meta/ai-coding-handoff.md](docs/00-meta/ai-coding-handoff.md)
- [docs/09-operations/first-run-setup-checklist.md](docs/09-operations/first-run-setup-checklist.md)
- [docs/12-roadmap/phase-gates.md](docs/12-roadmap/phase-gates.md)
- [docs/12-roadmap/technical-debt-register.md](docs/12-roadmap/technical-debt-register.md)
- [docs/03-strategy-research/v1-breakout-strategy-spec.md](docs/03-strategy-research/v1-breakout-strategy-spec.md)
- [docs/05-backtesting-validation/v1-breakout-validation-checklist.md](docs/05-backtesting-validation/v1-breakout-validation-checklist.md)

Representative recent implementation reports (full set under `docs/00-meta/implementation-reports/`):

- Phase 2p consolidation memo (R3 baseline-of-record locked)
- Phase 2w consolidation (R2 FAILED — §11.6)
- Phase 3d-B2 (F1 HARD REJECT)
- Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL)
- Phase 3t (5m diagnostic thread closure)
- Phase 4a (local safe runtime foundation)
- Phase 4l (V2 backtest execution — Verdict C HARD REJECT)
- Phase 4m (post-V2 strategy-research consolidation; 18-requirement validity gate)
- Phase 4r (G1 backtest execution — Verdict C HARD REJECT)
- Phase 4s (post-G1 consolidation)
- Phase 4t (post-G1 fresh-hypothesis discovery)
- Phase 4x (C1 backtest execution — Verdict C HARD REJECT)
- Phase 4y (post-C1 consolidation)
- Phase 4z (post-rejection research-process redesign)
- Phase 4ag (research-program pivot / mechanism-source triage)
- Phase 4ai (cross-sectional trend feasibility — `NOT_SUPPORTED`)
- Phase 4aj (M0 governance reconciliation)
- Phase 4ak (M0 governance adoption)
- Phase 4al (exit architecture / trade-management M0 admissibility memo)
- Phase 4am (exit architecture backtest-logic audit)
- Phase 4an (historical trade-population exit-path inventory)
- Phase 4ao (exit-path methodology / artefact harmonization)
- Phase 4ap (V1-arc exit-path forensic plan)
- Phase 4aq (V1-arc exit-path forensic computation)
- Phase 4ar (V1-arc exit-path forensic interpretation)
- Phase 4as (crypto microstructure research reset and mechanism map)
- Phase 4at (Binance microstructure data availability / capture feasibility)
- Phase 4au (Binance microstructure capture design specification)
- Phase 4av (public-only microstructure capture implementation plan)
- Phase 4aw (inert public-only microstructure scaffold implementation)
- Phase 4ax (aggTrades-only public microstructure collector skeleton)
- Phase 4ay (aggTrades public archive acquisition authorization boundary)
- Phase 4az (first public aggTrades archive acquisition — BTCUSDT 2025-01-15 UTC)

## Local development

The project uses **uv** for environment and command execution.

Typical local commands:

```powershell
cd C:\Prometheus
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Do not treat successful local tests as authorization for live trading. They confirm the current research / runtime-foundation code state only.

## Working method

The project is developed with a dual-review workflow:

- **Claude Code** performs repo work inside the local checkout.
- **ChatGPT** reviews plans, reports, checkpoint outputs, errors, and phase-gate decisions.
- The **operator** is the approval authority.

That workflow is intentional and is preserved for future phases.

## Phase model

Prometheus is governed by staged phase gates.

High-level phase sequence:

```text
PHASE 0 — Documentation and implementation planning
PHASE 1 — Local development foundation
PHASE 2 — Historical data, validation foundation, and V1 strategy research arc
PHASE 3 — F1 / D1-A research arcs and 5m diagnostic thread
PHASE 4 — Local safe runtime foundation, V2 / G1 / C1 research arcs, alt-symbol substrate arc, governance adoption, V1-arc exit-path forensic arc, microstructure infrastructure arc
PHASE 5 — Dashboard, observability, and alerts (not started; not authorized)
PHASE 6 — Dry-run exchange simulation (not started; not authorized)
PHASE 7 — Paper / shadow operation (not authorized)
PHASE 8 — Tiny live (not authorized)
PHASE 9 — Scaled live (not authorized)
```

Phases 4a–4c (runtime foundation) are merged but strategy-agnostic; Phase 4 canonical (the live-readiness gate) is **not** authorized. Research sub-phases live inside Phase 4 (e.g., 4f → 4l for V2; 4n → 4r for G1; 4u → 4x for C1; 4aa → 4ai for alt-symbol substrate; 4al → 4ar for V1-arc exit-path forensics; 4as → 4az for the microstructure infrastructure arc).

## Next possible step (conditional only)

No successor phase is authorized. If the operator separately wishes to advance the microstructure arc, two natural docs-only next steps are documented in the Phase 4az memo and closeout:

- a possible future **Phase 4ba docs-only eligibility-gate review memo** (discusses whether and how to ever implement a `flip_research_eligible(...)` primitive plus the audit-of-pass evidence required to flip the flag for the Phase 4az dataset specifically), or
- a possible future **Phase 4ba docs-only data-quality interpretation memo** (descriptive statistics on the Phase 4az dataset only — row count distributions, taker-side mix, time-density histograms, etc. — framed strictly as data-quality observations, not as edge or feature evidence).

Neither is authorized. The recommended state remains **paused**.

## Current recommendation

If you are reopening this repo later, the correct default assumption is:

- start from **R3 as the baseline-of-record**;
- treat **R1a / R1b-narrow** as preserved research evidence (non-leading);
- treat the **Phase 4az BTCUSDT 2025-01-15 aggTrades dataset** as **infrastructure evidence only**, not strategy evidence; it is `research_eligible=false` and `eligibility_gate_status=pending`;
- do **not** flip `research_eligible` to `True` without a separately authorized eligibility-gate phase;
- do **not** normalize, compute features, train models, or backtest against the Phase 4az dataset;
- do **not** acquire additional microstructure data (no ETHUSDT, no alt symbols, no multi-day, no monthly archive, no other data family) without separate authorization;
- do **not** restart strategy execution momentum automatically;
- do **not** start readiness or live-path planning automatically;
- any future research lane must clear the **M0 admissibility gate** ([docs/00-meta/m0-mechanism-admissibility-gate.md](docs/00-meta/m0-mechanism-admissibility-gate.md)) before discovery / spec / backtest;
- read the most recent implementation reports under `docs/00-meta/implementation-reports/` to decide whether a new docs-only phase is justified.

## License / usage

Add the project license here if and when one is selected.
