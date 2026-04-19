"""Research and validation workflows.

Per docs/08-architecture/codebase-structure.md, the ``research`` package owns
historical data ingestion, normalization, backtesting, validation, and
reporting. It must not depend on live execution, runtime state, operator
controls, or production secrets.
"""
