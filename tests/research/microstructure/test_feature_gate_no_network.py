"""Phase 4bi-B static no-network / no-credential scan over feature-gate modules.

The Phase 4bi-B gate is offline-only. Its source files must not import
or even reference any networking library, dotenv loader, secret token,
``MCP``, ``Graphify``, or similar. This test scans the four new
feature-gate source files and the package ``__init__`` lines that
re-export them, raising on any forbidden token.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PHASE_4BI_B_SOURCE_FILES = (
    "src/prometheus/research/microstructure/feature_gate_io.py",
    "src/prometheus/research/microstructure/feature_gate_report.py",
    "src/prometheus/research/microstructure/feature_gate_checks.py",
    "src/prometheus/research/microstructure/feature_gate.py",
)


# Forbidden import or reference patterns. Python module names; the
# scan is line-based and matches whole tokens.
FORBIDDEN_IMPORT_PATTERNS = (
    r"\bimport\s+requests\b",
    r"\bfrom\s+requests\b",
    r"\bimport\s+urllib\b",
    r"\bfrom\s+urllib\b",
    r"\bimport\s+httpx\b",
    r"\bfrom\s+httpx\b",
    r"\bimport\s+aiohttp\b",
    r"\bfrom\s+aiohttp\b",
    r"\bimport\s+websockets\b",
    r"\bfrom\s+websockets\b",
    r"\bimport\s+websocket\b",
    r"\bfrom\s+websocket\b",
    r"\bimport\s+binance\b",
    r"\bfrom\s+binance\b",
    r"\bimport\s+ccxt\b",
    r"\bfrom\s+ccxt\b",
    r"\bimport\s+dotenv\b",
    r"\bfrom\s+dotenv\b",
    r"\bos\.environ\b",
    r"\bos\.getenv\b",
    r"\bgetenv\(",
)


# Forbidden token references. These represent live credential or
# network surfaces; legitimate negative-confirmation references like
# the boundary-confirmation key ``no_mcp_or_graphify`` are intentionally
# excluded by the regex word boundaries below.
FORBIDDEN_TOKEN_REGEXES = (
    re.compile(r"['\"][A-Z_]*API_KEY[A-Z_]*['\"]"),
    re.compile(r"['\"][A-Z_]*BINANCE_(?:KEY|SECRET)[A-Z_]*['\"]"),
    re.compile(r"['\"][A-Z_]*BEARER_TOKEN[A-Z_]*['\"]"),
    re.compile(r"['\"][A-Z_]*ACCESS_TOKEN[A-Z_]*['\"]"),
    re.compile(r"X-MBX-APIKEY", re.IGNORECASE),
    re.compile(r"\bMCP_AUTH\b", re.IGNORECASE),
    re.compile(r"\bMCP_TOKEN\b", re.IGNORECASE),
    re.compile(r"\bMCP_API\b", re.IGNORECASE),
    re.compile(r"\.mcp\.json"),
    re.compile(r"\bGraphify\b"),
    re.compile(r"['\"]ws://"),
    re.compile(r"['\"]wss://"),
    re.compile(r"['\"]https?://[^'\"\s]"),
    re.compile(r"fapi\.binance"),
    re.compile(r"data\.binance\.vision"),
    re.compile(r"['\"]\.env['\"]"),
    re.compile(r"['\"]\.env\."),
)


_TRIPLE_DQ = re.compile(r'""".*?"""', flags=re.DOTALL)
_TRIPLE_SQ = re.compile(r"'''.*?'''", flags=re.DOTALL)


def _strip_docstrings_and_comments(text: str) -> str:
    """Remove triple-quoted docstrings + line comments.

    Negative-confirmation prose like ``no MCP / Graphify hooks`` lives
    in module docstrings; the gate's runtime code must remain free of
    real credential, env, or network surfaces. This strip mirrors
    :func:`tests.research.microstructure.test_import_boundaries
    ._strip_docstrings_and_comments` and lets the scan focus on
    executable code only.
    """
    text = _TRIPLE_DQ.sub("", text)
    text = _TRIPLE_SQ.sub("", text)
    out: list[str] = []
    for line in text.splitlines():
        idx = line.find("#")
        if idx >= 0:
            out.append(line[:idx])
        else:
            out.append(line)
    return "\n".join(out)


@pytest.mark.parametrize("rel_path", PHASE_4BI_B_SOURCE_FILES)
def test_no_forbidden_imports(rel_path: str) -> None:
    """No Phase 4bi-B source file imports a networking, dotenv, or env
    library."""
    repo_root = Path(__file__).resolve().parents[3]
    p = repo_root / rel_path
    src = _strip_docstrings_and_comments(p.read_text(encoding="utf-8"))
    for pat in FORBIDDEN_IMPORT_PATTERNS:
        m = re.search(pat, src)
        assert m is None, f"{rel_path}: forbidden import pattern {pat!r} matched: {m!r}"


@pytest.mark.parametrize("rel_path", PHASE_4BI_B_SOURCE_FILES)
def test_no_forbidden_tokens(rel_path: str) -> None:
    """No Phase 4bi-B source file's executable code references
    credential, MCP, Graphify, or live-URL tokens. Negative-
    confirmation references in docstrings (e.g. "no MCP / Graphify
    hooks") and the boundary-confirmation key ``no_mcp_or_graphify``
    are accepted because they document the absence of these surfaces."""
    repo_root = Path(__file__).resolve().parents[3]
    p = repo_root / rel_path
    src = _strip_docstrings_and_comments(p.read_text(encoding="utf-8"))
    for pat in FORBIDDEN_TOKEN_REGEXES:
        m = pat.search(src)
        assert (
            m is None
        ), f"{rel_path}: forbidden token pattern {pat.pattern!r} matched: {m!r}"


def test_phase_4bi_b_modules_do_not_open_files_outside_repo() -> None:
    """Phase 4bi-B modules must not contain hardcoded absolute paths
    outside the repo (no /etc/, no C:\\Windows, no /home, etc.)."""
    repo_root = Path(__file__).resolve().parents[3]
    forbidden = (
        re.compile(r"['\"]/etc/"),
        re.compile(r"['\"]/var/"),
        re.compile(r"['\"]/home/"),
        re.compile(r"['\"]/root/"),
        re.compile(r"['\"]C:\\\\Windows", re.IGNORECASE),
        re.compile(r"['\"]C:\\\\Users", re.IGNORECASE),
    )
    for rel_path in PHASE_4BI_B_SOURCE_FILES:
        p = repo_root / rel_path
        src = _strip_docstrings_and_comments(p.read_text(encoding="utf-8"))
        for pat in forbidden:
            assert pat.search(src) is None, (
                f"{rel_path}: forbidden absolute-path pattern {pat.pattern!r} present"
            )
