"""Representative design diagnostic; research under review, full code/data proprietary."""
import numpy as np


def validate_within_group_rank(design, groups):
    """Check numerical rank without making feature units determine the answer.

    Inputs are already validated, nonempty numeric features and aligned groups.
    Scale before centering to limit overflow, then normalize within-group changes
    before checking rank. Returned model inputs retain their original scale.
    This diagnostic does not establish causal identification or rule out separation.
    Differences already lost to input floating-point precision cannot be recovered.
    """
    values = design.astype(float)
    if not np.isfinite(values.to_numpy()).all():
        raise ValueError("Design must be representable as finite float64 values")
    scale = values.abs().max()
    scaled = values.div(scale.where(scale.ne(0), 1))
    centered = scaled - scaled.groupby(groups).transform("mean")
    within_scale = centered.abs().max()
    if within_scale.eq(0).any():
        raise ValueError("Features must vary within choice groups")
    normalized = centered.div(within_scale)
    if np.linalg.matrix_rank(normalized.to_numpy()) < design.shape[1]:
        raise ValueError("Features are linearly dependent within choice groups")
