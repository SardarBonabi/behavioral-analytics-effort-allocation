"""Representative effect arithmetic; keep relative and percentage-point changes distinct.

Research is under review; full research code and data remain proprietary.
These helpers do not estimate causal effects or reproduce research findings.
"""
from math import expm1, isfinite


def _as_percent(change: float) -> float:
    """Reject numeric overflow rather than returning an infinite percentage."""
    percent = 100 * change
    if not isfinite(percent):
        raise ValueError("Percentage exceeds the supported numeric range")
    return percent


def relative_change_percent(log_coefficient: float) -> float:
    """Convert a log-link coefficient without rounding tiny effects to zero."""
    if not isfinite(log_coefficient):
        raise ValueError("Coefficient must be finite")
    try:
        change = expm1(log_coefficient)
    except OverflowError as error:
        raise ValueError("Coefficient implies an unrepresentable relative change") from error
    return _as_percent(change)


def share_scenario(baseline_share: float, incidence_rate_ratio: float) -> dict:
    """Hypothetical arithmetic, not a fitted marginal effect or study result.

    The relative change describes the supplied multiplier. At a zero baseline,
    the implied absolute change is zero; an observed relative change is undefined.
    """
    if not 0 <= baseline_share <= 1 or not isfinite(incidence_rate_ratio) or incidence_rate_ratio < 0:
        raise ValueError("Invalid share or ratio")
    implied_share = baseline_share * incidence_rate_ratio
    if implied_share > 1:
        raise ValueError("Scenario implies a share above one")
    multiplier_change = incidence_rate_ratio - 1
    return {
        "relative_change_percent": _as_percent(multiplier_change),
        "implied_share": implied_share,
        "percentage_point_change": _as_percent(baseline_share * multiplier_change),
    }
