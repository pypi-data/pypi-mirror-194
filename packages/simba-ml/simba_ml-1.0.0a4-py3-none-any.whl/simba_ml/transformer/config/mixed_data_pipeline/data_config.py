"""Provides the configuration for the data."""
import dataclasses
from typing import Optional


@dataclasses.dataclass
class DataConfig:
    """Config for the data."""

    ratios: list[float]
    real: Optional[str] = None
    simulated: Optional[str] = None
    input_length: int = 2
    output_length: int = 2
    test_split: float = 0.2
    k_cross_validation: int = 5
    split_axis: str = "vertical"
