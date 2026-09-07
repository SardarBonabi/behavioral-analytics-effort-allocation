"""Representative conditional-logit reconstruction based on the resume.

A choice group is a developer-week in this example. This is a modeling example,
not a claim that the original proprietary implementation used this exact choice
set, feature list, or normalization. The caller must define eligible alternatives
using information available before the decision and account for sampling design.
"""
import pandas as pd
from statsmodels.discrete.conditional_models import ConditionalLogit


def fit_entry_model(choices: pd.DataFrame, feature_columns: list[str]):
    """Fit within-group project selection among varying alternatives.

    Expected columns: developer, week, project, entered (0/1), and features.
    Group-constant effects, including a standalone Italy-by-ban term, cannot be
    identified with developer-week conditioning. Interactions must vary across
    alternatives. This sample does not implement causal effect estimation.
    """
    data = choices.copy()
    if data.duplicated(["developer", "week", "project"]).any():
        raise ValueError("Duplicate project alternatives")
    if data[["entered"] + feature_columns].isna().any().any():
        raise ValueError("Resolve missing outcomes and features")
    if not data["entered"].isin([0, 1]).all():
        raise ValueError("entered must be binary")
    data["choice_group"] = data.groupby(["developer", "week"], sort=False).ngroup()
    variation = data.groupby("choice_group")["entered"].transform("nunique")
    eligible = data.loc[variation.eq(2)]
    if eligible.empty:
        raise ValueError("No groups with within-group outcome variation")
    varying = eligible.groupby("choice_group")[feature_columns].nunique().gt(1).any()
    if not varying.all():
        raise ValueError("Each regressor must vary within at least one choice group")
    model = ConditionalLogit(
        eligible["entered"], eligible[feature_columns], groups=eligible["choice_group"]
    )
    return model.fit(disp=False)
