"""Provides the configuration for the data."""
import dataclasses
from typing import Optional
from simba_ml.prediction.time_series.config import (
    time_series_config,
)


@dataclasses.dataclass
class DataConfig:
    """Config for time-series data."""

    synthetic: Optional[str] = None
    time_series: time_series_config.TimeSeriesConfig = dataclasses.field(
        default_factory=time_series_config.TimeSeriesConfig
    )
    test_split: float = 0.2
    split_axis: str = "vertical"
