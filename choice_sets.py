"""Representative choice-set preparation; research under review.

Full research code and data are proprietary. These public checks illustrate
sample preparation, not the confidential eligibility or sampling rules.
"""
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_complex_dtype


def prepare_choice_sets(choices: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    """Return observed groups with binary outcome variation and a usable design.

    Within-group centering is used only to check identification; returned features
    retain their original scale. Full column rank is necessary, not sufficient,
    for reliable fitting: separation and convergence still require model checks.
    """
    keys = ["developer", "week", "project"]
    reserved = set(keys + ["entered", "choice_group"])
    if not feature_columns or len(set(feature_columns)) != len(feature_columns):
        raise ValueError("Select nonempty, unique feature names")
    if reserved.intersection(feature_columns):
        raise ValueError("Exclude identifiers, outcomes and generated groups from features")
    required = keys + ["entered"] + feature_columns
    if not choices.columns.is_unique or not set(required).issubset(choices.columns):
        raise ValueError("Expected unique columns and all required fields")
    if choices[required].isna().any().any():
        raise ValueError("Resolve missing identifiers, outcomes and features")
    if choices.duplicated(keys).any():
        raise ValueError("Duplicate project alternatives")
    if not choices["entered"].isin([0, 1]).all():
        raise ValueError("entered must be binary")
    for name in feature_columns:
        values = choices[name]
        if not is_numeric_dtype(values.dtype) or is_complex_dtype(values.dtype):
            raise ValueError("Features must be real numeric values")
        if not np.isfinite(values).all():
            raise ValueError("Features must be finite")
    data = choices.copy()
    data["choice_group"] = data.groupby(["developer", "week"], sort=False, observed=True).ngroup()
    variation = data.groupby("choice_group")["entered"].transform("nunique")
    eligible = data.loc[variation.eq(2)].copy()
    if eligible.empty:
        raise ValueError("No groups with within-group outcome variation")
    design = eligible[feature_columns].astype(float)
    centered = design - design.groupby(eligible["choice_group"]).transform("mean")
    if np.linalg.matrix_rank(centered.to_numpy()) < len(feature_columns):
        raise ValueError("Features are constant or linearly dependent within choice groups")
    return eligible
