"""Phase 4bn-AQ — Long-Horizon ML Dataset Build + Single Controlled Run (CLI).

Thin orchestrator around
``prometheus.research.microstructure.build_longhorizon_ml_dataset_v001``. It
binds the already-gated Phase 4bn-AH 45-feature causal aggTrades source to the
Phase 4bn-AN long-horizon label family
(``microstructure_labels_longhorizon_aggtrades_v001``; horizons ``5m/30m/1h``)
and writes a compact, leakage-proof dataset **specification** (train-only
transform stats, split/support index, source binding, leakage/split-integrity
proof, dataset manifest, sidecar inventory, build run record) — with Phase 4bb-F
``.sha256`` sidecars — to the single authorized local/gitignored namespace
``data/research/microstructure/ml_datasets/longhorizon_pre_v001/``.

Strict scope — this script does NOT and MUST NOT: train / score / predict /
infer; run any baseline (majority / persistence / L2 logistic); run diagnostics;
select features; optimise thresholds; run strategy / signals / PnL / backtests;
mutate the AH dataset namespace, the AJ baseline namespace, the AN label
namespace, or any frozen v002 family / published manifest / gate / sidecar /
split file; read the v002 terminal window, any sealed-test date, or any test row;
acquire data, call endpoints, or read raw archives; commit any data artefact.
All source bindings are verified before any data read; any pre-read / alignment /
split / boundary / budget / output-guard breach fails closed and writes nothing.

Usage:
    python scripts/phase4bn_aq_build_longhorizon_ml_dataset.py --dry-run
    python scripts/phase4bn_aq_build_longhorizon_ml_dataset.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure import (  # noqa: E402
    build_longhorizon_ml_dataset_v001 as build_mod,
)

PHASE_ID = "4bn-AQ"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Phase 4bn-AQ long-horizon ML dataset build (single run)"
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "verify all source bindings (manifests, gates, 550 sidecars, "
            "feature<->label cross-binding) and the budget preflight, but read "
            "no rows and write nothing"
        ),
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="suppress per-partition progress output",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    summary = build_mod.run(progress=not args.quiet, dry_run=args.dry_run)
    print(f"[{PHASE_ID}] DONE")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
