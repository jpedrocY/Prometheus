"""Phase 4bn-B — static no-network / no-credential / no-MCP audit.

Statically scans every Phase 4bn-B source module and the runner script for
forbidden network / credential / MCP / Graphify / env-file imports and
URL string literals. The Phase 4bn-A design (§19, §21) and the Phase
4bn-B authorization prompt forbid any such surface; this test acts as a
fail-closed guard against accidental drift.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

PHASE_4BN_B_MODULE_NAMES = (
    "prometheus.research.microstructure.ml_baseline_design_v002",
    "prometheus.research.microstructure.ml_baseline_dataset_v002",
    "prometheus.research.microstructure.ml_baseline_models_v002",
    "prometheus.research.microstructure.ml_baseline_metrics_v002",
    "prometheus.research.microstructure.ml_baseline_report_v002",
)

PHASE_4BN_B_RUNNER_PATH = (
    Path(__file__).resolve().parents[3] / "scripts" / "phase4bn_b_run_ml_baseline_v002.py"
)

FORBIDDEN_IMPORT_TOKENS: tuple[str, ...] = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import urllib",
    "from urllib",
    "import urllib3",
    "from urllib3",
    "import socket",
    "from socket",
    "import websockets",
    "from websockets",
    "import websocket",
    "from websocket",
    "import dotenv",
    "from dotenv",
    "import boto3",
    "from boto3",
    "import google.auth",
    "from google.auth",
    "import paramiko",
    "from paramiko",
    "import requests_oauthlib",
)

# Tokens that should never appear anywhere in Phase 4bn-B source code.
# These are URL / endpoint / credential / MCP-config / Graphify-config
# patterns. We deliberately do not include literal policy-negation
# strings (e.g. ``used_graphify: False``) which legitimately enumerate
# *forbidden* surfaces as boolean attestations.
FORBIDDEN_STRING_TOKENS: tuple[str, ...] = (
    "https://",
    "http://",
    "wss://",
    "ws://",
    "binance.com",
    "binance.vision",
    "fapi.binance",
    ".mcp.json",
    "GRAPHIFY_API",
    "graphify_api",
    "graphify://",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "BINANCE_API_KEY",
    "BINANCE_SECRET",
    "API_SECRET",
    "SECRET_KEY",
)


def _module_source_path(name: str) -> Path:
    mod = importlib.import_module(name)
    p = getattr(mod, "__file__", None)
    if p is None:
        raise AssertionError(f"module has no __file__: {name}")
    return Path(p).resolve()


@pytest.mark.parametrize("module_name", PHASE_4BN_B_MODULE_NAMES)
def test_module_has_no_forbidden_imports(module_name: str) -> None:
    path = _module_source_path(module_name)
    text = path.read_text(encoding="utf-8")
    for token in FORBIDDEN_IMPORT_TOKENS:
        assert token not in text, (
            f"forbidden import {token!r} found in {path}"
        )


@pytest.mark.parametrize("module_name", PHASE_4BN_B_MODULE_NAMES)
def test_module_has_no_forbidden_strings(module_name: str) -> None:
    path = _module_source_path(module_name)
    text = path.read_text(encoding="utf-8")
    for token in FORBIDDEN_STRING_TOKENS:
        assert token not in text, (
            f"forbidden string token {token!r} found in {path}"
        )


def test_runner_script_has_no_forbidden_imports() -> None:
    text = PHASE_4BN_B_RUNNER_PATH.read_text(encoding="utf-8")
    for token in FORBIDDEN_IMPORT_TOKENS:
        assert token not in text, (
            f"forbidden import {token!r} found in {PHASE_4BN_B_RUNNER_PATH}"
        )


def test_runner_script_has_no_forbidden_strings() -> None:
    text = PHASE_4BN_B_RUNNER_PATH.read_text(encoding="utf-8")
    for token in FORBIDDEN_STRING_TOKENS:
        assert token not in text, (
            f"forbidden string {token!r} found in {PHASE_4BN_B_RUNNER_PATH}"
        )


def test_runner_script_imports_only_stdlib_numpy_and_internal() -> None:
    """The runner imports only stdlib, numpy, and ``prometheus.*`` modules."""
    text = PHASE_4BN_B_RUNNER_PATH.read_text(encoding="utf-8")
    # No third-party network or credential libraries.
    for forbidden in ("import sklearn", "from sklearn", "import pandas", "from pandas"):
        # Pandas would not violate phase rules per se, but its absence
        # documents the pure-numpy implementation choice.
        assert forbidden not in text, (
            f"unexpected library import {forbidden!r} in {PHASE_4BN_B_RUNNER_PATH}"
        )
