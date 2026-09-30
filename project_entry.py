"""Representative conditional-logit reconstruction.

A choice group is a developer-week in this example. This is a modeling example,
not a claim that the original proprietary implementation used this exact choice
set, feature list, or normalization. The caller must define eligible alternatives
using information available before the decision and account for sampling design.
"""
import pandas as pd
from choice_sets import prepare_choice_sets


def fit_entry_model(choices: pd.DataFrame, feature_columns: list[str]):
    """Fit within-group project selection among varying alternatives.

    Expected columns: developer, week, project, entered (0/1), and features.
    Group-constant effects, including a standalone Italy-by-ban term, cannot be
    identified with developer-week conditioning. Interactions must vary across
    alternatives. This sample does not implement causal effect estimation.
    """
    eligible = prepare_choice_sets(choices, feature_columns)
    from statsmodels.discrete.conditional_models import ConditionalLogit

    model = ConditionalLogit(
        eligible["entered"], eligible[feature_columns], groups=eligible["choice_group"]
    )
    return model.fit(disp=False)
