"""Provides the configuration for the data."""
import dataclasses
from simba_ml.prediction.time_series.config import (
    time_series_config,
)


@dataclasses.dataclass
class DataConfig:
    """Config for time-series data."""

    observed: str
    synthetic: str
    test_split: float = 0.2
    split_axis: str = "vertical"
    time_series: time_series_config.TimeSeriesConfig = dataclasses.field(
        default_factory=time_series_config.TimeSeriesConfig
    )
