"""Static import-boundary scan for Phase 4bj-C label modules.

Confirms that the five new ``labels_*`` source modules:

- never import any networking library;
- never reference credential-shaped tokens, ``.env`` files,
  ``.mcp.json``, or Graphify / MCP integrations.

The scan strips Python docstrings and ``#`` comments before checking
forbidden tokens, so docstrings that *describe* the policy ("must NOT
import requests") do not trigger false positives. The forbidden-import
list mirrors the Phase 4aw + Phase 4ax + Phase 4bb-C + Phase 4bd +
Phase 4bf + Phase 4bh patterns extended with Phase 4bj-C-specific
prohibitions.
"""

from __future__ import annotations

import ast
import io
import re
import tokenize
from pathlib import Path

import pytest

_PACKAGE_DIR = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "prometheus"
    / "research"
    / "microstructure"
)

_LABEL_MODULES = (
    _PACKAGE_DIR / "labels_schema.py",
    _PACKAGE_DIR / "labels_io.py",
    _PACKAGE_DIR / "labels_compute.py",
    _PACKAGE_DIR / "labels_manifest.py",
    _PACKAGE_DIR / "labels_validation.py",
)

_FORBIDDEN_IMPORTS = (
    "requests",
    "urllib",
    "urllib.request",
    "urllib3",
    "httpx",
    "aiohttp",
    "websockets",
    "websocket",
    "binance",
    "ccxt",
    "dotenv",
    "python_dotenv",
    "socket",
)

# Tokens that must never appear in source code (after stripping
# docstrings and comments). Note: lower-cased and substring-matched.
# ``token`` is deliberately excluded because it is a generic English
# noun used by stdlib ``tokenize`` and by the schema's local loop
# variable name (consistent with the Phase 4bh ``features_schema``
# pattern). Credential-shaped surfaces are still covered by ``api_key``,
# ``apikey``, ``secret``, ``listenkey``, and ``userdatastream``.
_FORBIDDEN_TOKENS = (
    "api_key",
    "apikey",
    "secret",
    "private_endpoint",
    "authenticated_endpoint",
    "listenkey",
    "userdatastream",
    "/fapi/v1/order",
    "/fapi/v2/account",
    "/fapi/v2/positionrisk",
    "/fapi/v1/leverage",
    "/fapi/v1/margintype",
    "/fapi/v1/forceorders",
    ".env",
    ".mcp.json",
    "graphify",
)


def _strip_comments_and_docstrings(source: str) -> str:
    """Return *source* with docstrings and ``#`` comments removed.

    Docstrings are removed via :mod:`ast`; ``#`` comments are removed
    via :mod:`tokenize`. The transformations are intentionally
    conservative and do not modify the structure of any executable
    code.
    """
    tree = ast.parse(source)

    class _DocstringStripper(ast.NodeTransformer):
        def visit_Module(self, node: ast.Module) -> ast.Module:  # type: ignore[override]
            return self._strip(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:  # type: ignore[override]
            return self._strip(node)

        def visit_AsyncFunctionDef(  # type: ignore[override]
            self, node: ast.AsyncFunctionDef
        ) -> ast.AsyncFunctionDef:
            return self._strip(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:  # type: ignore[override]
            return self._strip(node)

        def _strip(
            self,
            node: ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
        ) -> ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef:
            if node.body and isinstance(node.body[0], ast.Expr):
                first = node.body[0]
                if isinstance(first.value, ast.Constant) and isinstance(
                    first.value.value, str
                ):
                    node.body = node.body[1:]
            for child in ast.iter_child_nodes(node):
                self.visit(child)
            return node

    stripped = ast.unparse(_DocstringStripper().visit(tree))
    tokens = tokenize.generate_tokens(io.StringIO(stripped).readline)
    filtered: list[str] = []
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            continue
        filtered.append(tok.string)
    return " ".join(filtered)


def _collect_imports(source: str) -> list[str]:
    tree = ast.parse(source)
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


@pytest.mark.parametrize("module_path", _LABEL_MODULES)
def test_label_module_has_no_forbidden_imports(module_path: Path) -> None:
    source = module_path.read_text(encoding="utf-8")
    imports = _collect_imports(source)
    flat_imports = {name.split(".")[0] for name in imports}
    flat_imports.update(imports)
    for forbidden in _FORBIDDEN_IMPORTS:
        assert forbidden not in flat_imports, (
            f"{module_path.name}: forbidden import {forbidden!r} detected"
        )


@pytest.mark.parametrize("module_path", _LABEL_MODULES)
def test_label_module_has_no_forbidden_tokens(module_path: Path) -> None:
    raw = module_path.read_text(encoding="utf-8")
    stripped = _strip_comments_and_docstrings(raw).lower()
    # Eliminate identifier-internal substrings that share legitimate prefixes
    # (e.g. "tokenize" should not match "token"). We use word-ish boundaries.
    pattern = re.compile(r"[a-z0-9_.]+|[/]+[a-z0-9_./]+")
    matches = pattern.findall(stripped)
    for forbidden in _FORBIDDEN_TOKENS:
        for m in matches:
            assert forbidden not in m or (
                # Whitelist: legitimate identifiers that happen to contain a
                # forbidden substring but are demonstrably unrelated:
                # * "mcp" appears inside "compute"; "tokenize" / "tokens" do
                #   not match a standalone "token" word boundary; etc.
                forbidden == "mcp" and "compute" in m
                or forbidden == "mcp" and "compares" in m
                or forbidden == "token" and ("tokenize" in m or "tokens" in m)
                or forbidden == "secret" and m == "secretly"
                or forbidden == "apikey" and m == "apikey_unrelated"
            ), f"{module_path.name}: forbidden token {forbidden!r} detected in {m!r}"


def test_no_dot_env_or_dot_mcp_files_present_in_repo_check() -> None:
    """Sanity check that the package directory has no .env or .mcp.json file."""
    for path in _PACKAGE_DIR.iterdir():
        assert path.name != ".env"
        assert path.name != ".mcp.json"


def test_label_modules_do_not_call_os_environ_for_credentials() -> None:
    """Confirm no label module reads ``os.environ`` or ``os.getenv``."""
    for module_path in _LABEL_MODULES:
        source = module_path.read_text(encoding="utf-8")
        stripped = _strip_comments_and_docstrings(source)
        assert "os.environ" not in stripped, (
            f"{module_path.name} references os.environ"
        )
        assert "os.getenv" not in stripped, (
            f"{module_path.name} references os.getenv"
        )
