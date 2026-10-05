"""Representative feature construction for the effort-allocation study.

Input: complete, non-overlapping counts for one developer-week per row.
The schema is illustrative and does not expose the proprietary data model.
Research is under review; full research code and data remain proprietary.
"""
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_complex_dtype

PUBLIC_ACTIVITIES = [
    "repositories_created", "commits", "pull_requests", "reviews",
    "discussions_started", "discussions_answered", "issues",
]


def validate_allocation_panel(panel: pd.DataFrame) -> None:
    """Validate observed developer-weeks without treating missing data as zero."""
    keys = ["developer", "week"]
    counts = PUBLIC_ACTIVITIES + ["private_contributions"]
    if not panel.columns.is_unique or not set(keys + counts).issubset(panel.columns):
        raise ValueError("Expected unique columns and all required fields")
    if panel[keys + counts].isna().any().any() or panel.duplicated(keys).any():
        raise ValueError("Expected complete, unique developer-week observations")
    for name in counts:
        values = panel[name]
        if not is_numeric_dtype(values.dtype) or is_complex_dtype(values.dtype):
            raise ValueError("Activity counts must be real numeric values")
        if not np.isfinite(values).all() or values.lt(0).any():
            raise ValueError("Activity counts must be finite and nonnegative")


def _sum_activity_counts(counts: pd.DataFrame) -> pd.Series:
    """Use floating arithmetic to avoid fixed-width integer wraparound.

    Feature totals are approximate above float64's exact-integer range. Reject
    unrepresentable totals instead of emitting infinite totals or invalid shares.
    Input validation must run first; missing activity is never filled with zero.
    """
    with np.errstate(over="ignore", invalid="ignore"):
        totals = counts.astype("float64").sum(axis=1, skipna=False)
    if not np.isfinite(totals).all():
        raise ValueError("Activity total exceeds the supported numeric range")
    return totals


def build_allocation_features(panel: pd.DataFrame) -> pd.DataFrame:
    validate_allocation_panel(panel)
    result = panel.copy()
    result["public_contributions"] = _sum_activity_counts(result[PUBLIC_ACTIVITIES])
    total = _sum_activity_counts(result[["public_contributions", "private_contributions"]])
    result["total_contributions"] = total
    result["public_share"] = result["public_contributions"].div(total.where(total.gt(0)))
    return result
