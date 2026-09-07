"""Keep relative effects distinct from percentage-point changes."""
from math import exp, isfinite


def relative_change_percent(log_coefficient: float) -> float:
    if not isfinite(log_coefficient):
        raise ValueError("Coefficient must be finite")
    return 100 * (exp(log_coefficient) - 1)


def share_scenario(baseline_share: float, incidence_rate_ratio: float) -> dict:
    """Hypothetical arithmetic, not a fitted marginal effect or study result."""
    if not 0 <= baseline_share <= 1 or not isfinite(incidence_rate_ratio) or incidence_rate_ratio < 0:
        raise ValueError("Invalid share or ratio")
    implied_share = baseline_share * incidence_rate_ratio
    if implied_share > 1:
        raise ValueError("Scenario implies a share above one")
    return {
        "relative_change_percent": 100 * (incidence_rate_ratio - 1),
        "implied_share": implied_share,
        "percentage_point_change": 100 * (implied_share - baseline_share),
    }
