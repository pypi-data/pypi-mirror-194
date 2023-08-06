"""Provides a normalizer, which can normalize train and test data."""
import typing

import numpy as np
from numpy import typing as npt


class NotInitializedError(Exception):
    """Raised when the normalizer is not initialized, but the normalize_test_data function is called."""


class AlreadyInitializedError(Exception):
    """Raised when the normalizer is already initialized, but the normalize_train_data function is called."""


class Normalizer:
    """Normalizes train and test data."""

    train_std: typing.Optional[np.float64] = None
    train_mean: typing.Optional[np.float64] = None
    initialized: bool = False

    def normalize_train_data(self, train: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Normalizes the train data by subtracting the mean and dividing through the standard deviation of the train set.

        Args:
            train: Train data.

        Returns:
            The normalized train data, the mean and the standard deviation.

        Raises:
            AlreadyInitializedError: If the normalizer is already initialized.
        """
        if self.initialized or self.train_mean is not None or self.train_std is not None:
            raise AlreadyInitializedError()
        self.initialized = True

        self.train_mean = train.mean()
        self.train_std = train.std()
        return (train - self.train_mean) / self.train_std

    def normalize_test_data(self, test: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Normalizes the test data by subtracting the mean and dividing through the standard deviation of the train set.

        Args:
            test: Test data.

        Returns:
            The normalized test data.

        Raises:
            NotInitializedError: If the normalizer is not initialized.
        """
        if not self.initialized or self.train_mean is None or self.train_std is None:
            raise NotInitializedError()

        return (test - self.train_mean) / self.train_std
