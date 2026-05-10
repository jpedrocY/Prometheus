# Phase 4bj-C — Closeout

## 1. Branch and base

- Branch: `phase-4bj-c/label-implementation-local-artefacts`
- Base: `main` at the post-Phase-4bj-B merge-closeout state
- Phase 4bj-B merge ancestor (verified):
  `decc6624079ef786d5f360226303ae10a644a237`
- Code commit SHA recorded in label manifest:
  `f73a3db591bb0aa376b21ce0294f24de4acdfee4`

## 2. Files changed

Source modules added (5):

- `src/prometheus/research/microstructure/labels_schema.py`
- `src/prometheus/research/microstructure/labels_io.py`
- `src/prometheus/research/microstructure/labels_compute.py`
- `src/prometheus/research/microstructure/labels_manifest.py`
- `src/prometheus/research/microstructure/labels_validation.py`

Source narrowly updated (1):

- `src/prometheus/research/microstructure/__init__.py` (Phase 4bj-C
  re-exports + docstring extension)

Test files added (7):

- `tests/research/microstructure/_labels_fixtures.py`
- `tests/research/microstructure/test_labels_schema.py`
- `tests/research/microstructure/test_labels_io.py`
- `tests/research/microstructure/test_labels_compute.py`
- `tests/research/microstructure/test_labels_manifest.py`
- `tests/research/microstructure/test_labels_validation.py`
- `tests/research/microstructure/test_labels_no_network.py`

Docs added (2):

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-c_label-implementation-local-artefacts.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-c_closeout.md`

Docs narrowly updated (1):

- `docs/00-meta/current-project-state.md`

No `.gitignore` change. No `pyproject.toml` change. No `README.md`
change. No `scripts/...` entrypoint added. No existing script
modified. No existing test outside the new
`tests/research/microstructure/test_labels_*.py` files modified.

## 3. Local gitignored output paths and SHAs

| Output | Path | SHA256 | Size (bytes) |
|---|---|---|---|
| Label parquet | `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | 66,073,234 |
| Label parquet sidecar | same path with `.sha256` | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | 154 |
| Label manifest | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | 6,786 |
| Label manifest sidecar | same path with `.sha256` | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | 138 |

All four files are gitignored under `.gitignore:85: data/microstructure/`
and are **not** committed.

## 4. Validation summary

`validate_label_dataset_v001` returned `overall_status = pass` with
**100 / 100** checks PASS, 0 FAIL, 0 NOT_APPLICABLE.

Targeted pytest: 73 / 73 tests passed.
`pytest tests/research/microstructure/`: 744 passed.
Whole-repo `pytest`: 1527 passed, 2 failed (pre-existing simulation
`KeyError: 'trade_count'` failures in
`tests/simulation/test_backtest_real_2026_03.py`; zero new Phase 4bj-C
regressions).
Whole-repo `ruff check .`: All checks passed.
Whole-repo `mypy`: Success on 115 source files.
`git diff --check`: clean.
`git check-ignore -v data/microstructure/`: covered by `.gitignore:85`.
`git check-ignore -v data/microstructure/labels/`: covered by
`.gitignore:85`.
`git check-ignore -v data/microstructure/manifests/`: covered by
`.gitignore:85`.

## 5. Row count

- `label_parquet.num_rows = 1,681,098`
- `feature_parquet.num_rows = 1,681,098`
- per-row alignment (row_index, agg_trade_id, feature_timestamp_ms,
  source_transact_time_ms): OK

## 6. Column count

- `label_parquet.num_columns = 39`
- `LABEL_SCHEMA_V001 column count = 39`
- schema-order parity: OK
- forbidden-substring scan on column names: OK (no hits)

## 7. label_config_hash

`fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`

(Constant across all 1,681,098 label parquet rows; matches
`label_manifest.label_config_hash`.)

## 8. invalid_price_row_count

`0`

## 9. censored_per_horizon

```json
{"1s": 9, "5s": 42, "15s": 118, "60s": 507}
```

All 9 / 42 / 118 / 507 censorings are right-edge censorings (target
timestamp exceeds the final source normalized transact_time_ms for
2025-01-15). Anchor / reference price domain was strictly positive for
every row; no invalid-price flagging was needed.

## 10. Boundary confirmations

| Boundary | Status |
|---|---|
| Label parquet writes under `data/microstructure/labels/` only | OK |
| Label manifest writes under `data/microstructure/manifests/` only | OK |
| Refuse-overwrite enforced for all four label output paths | OK |
| Sidecar SHAs match recomputed bytes (both parquet and manifest) | OK |
| Label manifest `research_eligible = false` | OK |
| Label manifest `eligibility_gate_status = "pending"` | OK |
| Feature manifest unchanged at `research_eligible = false / pending` | OK |
| Original derived manifest unchanged at `research_eligible = false / pending` | OK |
| Raw manifest unchanged at `research_eligible = false / pending` | OK |
| No label gate report file created | OK |
| No label successor-state artefact created | OK |
| No ML, strategy, backtest, acquisition activity | OK |
| No network, credential, `.env`, `.mcp.json`, MCP, or Graphify activity | OK |
| All 11 upstream artefacts byte-identical pre/post the run | OK |
| Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved | OK (never invoked) |
| No retained verdict revision | OK |
| No project lock change | OK |
| No M0 amendment | OK |
| No successor phase authorised | OK |

## 11. Retained verdict ledger

- H0 → FRAMEWORK ANCHOR
- R3 → BASELINE-OF-RECORD
- R1a → RETAINED — NON-LEADING
- R1b-narrow → RETAINED — NON-LEADING
- R2 → FAILED — §11.6
- F1 → HARD REJECT
- D1-A → MECHANISM PASS / FRAMEWORK FAIL — other
- 5m thread → OPERATIONALLY CLOSED per Phase 3t
- V2 → HARD REJECT — terminal for V2 first-spec
- G1 → HARD REJECT — terminal for G1 first-spec
- C1 → HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 12. Project locks

All preserved verbatim:

- §11.6 = 8 bps per side; round-trip = 16 bps
- §1.7.3 = 0.25% risk / 2× leverage / one-position max / mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy spec
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy spec
- Phase 4w C1 backtest-plan methodology
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy

## 13. No-rescue constraints

Phase 4bj-C does not, and cannot, be construed as authorising:

- ML model training, model selection, or strategy hypothesis
  generation from these labels;
- strategy signal construction or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / aggTrades-beyond-day
  data acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved).

## 14. Successor authorisation

**None.**

Phase 4bj-C is implementation-and-local-output only. No subsequent
phase is authorised. Specifically not authorised:

- Phase 4bj-D Label Artefact Structural QA Memo
- Phase 4bj-E Label-Family Eligibility Gate
- Phase 4bj-F Label-Family Research / ML-Use Decision
- Phase 4bj-G Label-Family Successor-State Recording
- Phase 4bb-F Gate Report Output Path Hygiene
- Phase 4bb-G Raw Manifest Successor-State Recording
- Phase 4 canonical
- Phase 5
- Paper / shadow, live-readiness, deployment, exchange-write,
  production-key creation, authenticated APIs, private endpoints,
  user stream, live WebSocket implementation, MCP, Graphify,
  `.mcp.json`, credentials

## 15. Recommended state

**Remain paused.**

The Phase 4bj-C label artefacts and manifest are preserved as local
gitignored Stage-0 derived research-time scaffolding. Any future
movement toward label-family eligibility, research-use, ML-use, or
strategy work requires a separately authorised successor phase. The
recommended next operator decision is to merge Phase 4bj-C to main
(under separate authorisation) and remain paused, with the optional
Phase 4bj-D structural QA memo path available if and when the
operator separately authorises it.

**No next phase authorised.**
