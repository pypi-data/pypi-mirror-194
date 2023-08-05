"""Module with utility function that can be used by models."""
import random

import pandas as pd


# sourcery skip: require-parameter-annotation
def mix_data(
    *,
    observed_data: list[pd.DataFrame],
    synthetic_data: list[pd.DataFrame],
    ratio: float = 1,
) -> list[pd.DataFrame]:
    """Mixes real and synthetic data according to a ratio.

    Args:
        observed_data: observed data.
        synthetic_data: synthetic data.
        ratio: Ratio of synthethic to observed data.

    Raises:
        ValueError: If number of observed datapoints is not sufficient to fulfill ratio.

    Returns:
        The mixed data.
    """
    datapoints_in_observed_data = sum((len(df) for df in observed_data))
    datapoints_in_synthetic_data = sum((len(df) for df in synthetic_data))
    if datapoints_in_synthetic_data < datapoints_in_observed_data * ratio:
        raise ValueError(
            f"Synthetic data has {datapoints_in_synthetic_data} datapoints, "
            f"but {datapoints_in_observed_data * ratio} are required to fulfill the defined ratio. "
            f"Please generate more synthetic data."
        )
    synthetic_data_in_mix = []
    datapoints_in_synthetic_data_in_mix = 0
    for df in synthetic_data:
        if (
            datapoints_in_synthetic_data_in_mix + len(df)
            < datapoints_in_observed_data * ratio
        ):
            synthetic_data_in_mix.append(df)
            datapoints_in_synthetic_data_in_mix += len(df)
        else:
            synthetic_data_in_mix.append(
                df[
                    : int(
                        datapoints_in_observed_data * ratio
                        - datapoints_in_synthetic_data_in_mix
                    )
                ]
            )
            break

    res = observed_data + synthetic_data_in_mix
    random.shuffle(res)
    return res
