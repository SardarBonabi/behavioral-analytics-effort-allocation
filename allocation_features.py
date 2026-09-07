"""Representative feature construction for the effort-allocation study.

Input: complete, non-overlapping counts for one developer-week per row.
The schema is illustrative and does not expose the proprietary data model.
"""
import pandas as pd

PUBLIC_ACTIVITIES = [
    "repositories_created", "commits", "pull_requests", "reviews",
    "discussions_started", "discussions_answered", "issues",
]


def build_allocation_features(panel: pd.DataFrame) -> pd.DataFrame:
    columns = PUBLIC_ACTIVITIES + ["private_contributions"]
    if panel.duplicated(["developer", "week"]).any():
        raise ValueError("Expected one row per developer-week")
    if panel[columns].isna().any().any() or panel[columns].lt(0).any().any():
        raise ValueError("Reconcile incomplete or invalid collection records first")
    result = panel.copy()
    result["public_contributions"] = result[PUBLIC_ACTIVITIES].sum(axis=1)
    total = result["public_contributions"] + result["private_contributions"]
    result["total_contributions"] = total
    result["public_share"] = result["public_contributions"].div(total.where(total.gt(0)))
    return result
