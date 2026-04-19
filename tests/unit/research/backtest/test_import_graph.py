"""Mechanical guardrail: the backtest package must not depend on any
module capable of network access or live exchange writes.

This enforces Phase 3 non-goals §5 items 2-6 and Gate-1 condition D
at import time. If someone later adds an import of a forbidden
module to the backtest package, this test fails the build.

The test uses Python's AST instead of simply importing-and-checking
to avoid depending on import order.
"""

from __future__ import annotations

import ast
from pathlib import Path

# Directories that host backtest source. Do NOT add
# research/data/binance_rest.py or similar Binance-network modules.
BACKTEST_PACKAGE = (
    Path(__file__).resolve().parents[4] / "src" / "prometheus" / "research" / "backtest"
)

FORBIDDEN_PREFIXES = (
    # Any future or existing live-exchange module path.
    "prometheus.exchange",
    # Binance REST client was built for Phase 2c data fetching; the
    # backtester must not import it even for "just to reuse types".
    "prometheus.research.data.binance_rest",
    "prometheus.research.data.binance_bulk",
    # Explicit network transports.
    "httpx",
    "requests",
    "urllib3",
    # Third-party exchange SDKs that might get added later.
    "ccxt",
    "binance",
    "python_binance",
)


def _imported_modules(py_file: Path) -> set[str]:
    src = py_file.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(py_file))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names.add(node.module)
    return names


def test_backtest_package_does_not_import_network_modules() -> None:
    assert BACKTEST_PACKAGE.is_dir(), f"expected backtest package at {BACKTEST_PACKAGE}"
    offenders: list[tuple[Path, str]] = []
    for py in sorted(BACKTEST_PACKAGE.rglob("*.py")):
        if py.name == "__pycache__":
            continue
        for name in _imported_modules(py):
            for prefix in FORBIDDEN_PREFIXES:
                if name == prefix or name.startswith(prefix + "."):
                    offenders.append((py, name))
    assert not offenders, f"backtest package imports forbidden modules: {offenders}"


def test_strategy_package_does_not_import_network_modules() -> None:
    strategy_root = BACKTEST_PACKAGE.parents[1] / "strategy"
    assert strategy_root.is_dir(), f"expected strategy package at {strategy_root}"
    offenders: list[tuple[Path, str]] = []
    for py in sorted(strategy_root.rglob("*.py")):
        if py.name == "__pycache__":
            continue
        for name in _imported_modules(py):
            for prefix in FORBIDDEN_PREFIXES:
                if name == prefix or name.startswith(prefix + "."):
                    offenders.append((py, name))
    assert not offenders, f"strategy package imports forbidden modules: {offenders}"
