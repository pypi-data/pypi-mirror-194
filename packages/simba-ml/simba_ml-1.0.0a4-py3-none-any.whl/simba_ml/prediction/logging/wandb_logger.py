"""Wrapper for wandb logging."""
import typing

import wandb

P = typing.ParamSpec("P")
T = typing.TypeVar("T")


class WandbLogger:
    """Wrapper for wandb logging."""

    def __init__(self, log: bool) -> None:
        """Initializes the wandb logger.

        Args:
            log: Whether to log to wandb.
        """
        self.logging = log

    def __getattr__(self, name: str) -> typing.Callable[..., typing.Optional[T]]:
        """Passes the message to wandb if wandb logging is enabled.

        Args:
            name: The name of the wandb function to call.

        Returns:
            A function that calls the corresponding wandb function
            if wandb logging is enabled.
        """
        func = getattr(wandb, name)

        def outer(
            func: typing.Callable[..., T]
        ) -> typing.Callable[..., typing.Optional[T]]:
            def pass_message(
                *args: typing.Any, **kwargs: typing.Any
            ) -> typing.Optional[T]:
                return func(*args, **kwargs) if self.logging else None

            return pass_message

        return outer(func)
