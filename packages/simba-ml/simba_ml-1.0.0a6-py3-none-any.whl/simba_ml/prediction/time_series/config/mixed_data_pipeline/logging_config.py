"""Provides the configuration for logging."""
import dataclasses


@dataclasses.dataclass
class LoggingConfig:
    """Config for the data."""

    wandb: bool
    wandb_project: str
    wandb_entity: str
