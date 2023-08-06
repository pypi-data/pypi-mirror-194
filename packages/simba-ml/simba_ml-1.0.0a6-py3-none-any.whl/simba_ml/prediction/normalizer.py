"""Provides a normalizer, which can normalize train and test data."""
import numpy as np
from numpy import typing as npt


class NotInitializedError(Exception):
    """Raised when `normalize_test_data` is called on uninitialized Normalizer."""


class Normalizer:
    """Normalizes train and test data."""

    train_std: npt.NDArray[np.float64]
    train_mean: npt.NDArray[np.float64]
    initialized: bool = False

    def normalize_train_data(
        self, train: list[npt.NDArray[np.float64]]
    ) -> list[npt.NDArray[np.float64]]:
        """Normalizes the train data.

        Normalizes the train data by subtracting the mean and dividing
        through the standard deviation of the train set.

        Args:
            train: Train data.

        Returns:
            The normalized train data.
        """
        self.initialized = True
        self.train_mean = np.concatenate(train).mean(axis=0)
        self.train_std = np.concatenate(train).std(axis=0)
        self.train_std[self.train_std == 0.0] = 1.0
        return [
            (train[i] - self.train_mean) / self.train_std for i in range(len(train))
        ]

    def normalize_test_data(
        self, test: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]:
        """Normalizes the test data.

        Subtracts the mean and divides through the standard deviation of the train set.

        Args:
            test: Test data.

        Returns:
            The normalized test data.

        Raises:
            NotInitializedError: If the normalizer is not initialized.
        """
        if not self.initialized:
            raise NotInitializedError()
        return (test - self.train_mean) / self.train_std

    def denormalize_prediction_data(
        self, data: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]:
        """Denormalizes the data.

        Denormalizes the data, by multiplying with the standard deviation
        and adding the mean of the train set.

        Args:
            data: Data to denormalize.

        Returns:
            The denormalized data.

        Raises:
            NotInitializedError: If the normalizer is not initialized.
        """
        if not self.initialized:
            raise NotInitializedError()

        return data * self.train_std + self.train_mean
