"""Risk-engine specific errors."""

from __future__ import annotations

from prometheus.core.errors import PrometheusError


class RiskError(PrometheusError):
    """Base class for risk-engine errors."""


class MissingMetadataError(RiskError):
    """Raised when a required input is missing or invalid (fail closed)."""


class SizingError(RiskError):
    """Raised when a sizing computation rejects an input."""


class ExposureGateError(RiskError):
    """Raised when an exposure gate rejects a candidate entry."""


class StopValidationError(RiskError):
    """Raised when a stop request fails validation."""
