"""Provides the configuration for logging."""
import dataclasses


@dataclasses.dataclass
class TimeSeriesConfig:
    """Config for the time-series parameters."""

    input_length: int = 1
    output_length: int = 1
    num_species: int = 1
