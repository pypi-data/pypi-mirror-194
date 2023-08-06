"""This module provides the dataloader."""
import os
from typing import Optional, Tuple

import pandas as pd
import numpy as np
from numpy import typing as npt

from simba_ml.transformer.config.mixed_data_pipeline import data_config
from simba_ml.transformer.data_loader import preprocessing
from simba_ml.transformer.data_loader import window_generator
from simba_ml.transformer.data_loader import mix_data


class MixedDataLoader:
    """Loads and preprocesses the data.

    Attributes:
        X_test: the input of the test data
        y_test: the labels for the test data
        train_validation_sets: list of validations sets, one for each ratio of synthethic to observed data
    """

    config: data_config.DataConfig
    __X_test: Optional[npt.NDArray[np.float64]] = None
    __y_test: Optional[npt.NDArray[np.float64]] = None
    __list_of_train_validation_sets: list[list[dict[str, list[npt.NDArray[np.float64]]]]] = []

    def __init__(self, config: data_config.DataConfig) -> None:
        """Inits the DataLoader.

        Args:
            config: the data configuration.
        """
        self.config = config
        self.__list_of_train_validation_sets = [[] for _ in range(len(self.config.ratios))]

    def load_data(self) -> Tuple[list[pd.DataFrame], list[pd.DataFrame]]:
        """Loads the data.

        Returns:
            A list of dataframes.
        """
        synthetic = (
            []
            if self.config.simulated is None
            else preprocessing.dataframes_from_csvs(os.getcwd() + self.config.simulated)
        )
        observed = (
            []
            if self.config.real is None
            else preprocessing.dataframes_from_csvs(os.getcwd() + self.config.real)
        )
        return synthetic, observed

    def prepare_data(self) -> None:
        """This function preprocesses the data."""
        if self.__X_test is not None:  # pragma: no cover
            return  # pragma: no cover

        synthethic_data, observed_data = self.load_data()

        synthetic_train, _ = preprocessing.train_test_split(
            data=synthethic_data,
            test_split=self.config.test_split,
            input_length=self.config.input_length,
            split_axis=self.config.split_axis,
        )
        observed_train, observed_test = preprocessing.train_test_split(
            data=observed_data,
            test_split=self.config.test_split,
            input_length=self.config.input_length,
            split_axis=self.config.split_axis,
        )

        # compute train validation sets for each of the data ratios defined in the data config
        for ratio_idx, ratio in enumerate(self.config.ratios):
            train = mix_data.mix_data(
                synthetic_data=synthetic_train,
                observed_data=observed_train,
                ratio=ratio,
            )
            train_validation_sets = preprocessing.train_validation_split(
                train,
                k_cross_validation=self.config.k_cross_validation,
                input_length=self.config.input_length,
                split_axis=self.config.split_axis,
            )
            for train_validation_set in train_validation_sets:
                train_validation_set["train"] = preprocessing.dataframe_to_numpy(
                    train_validation_set["train"]
                )
                train_validation_set["validation"] = preprocessing.dataframe_to_numpy(
                    train_validation_set["validation"]
                )
            self.__list_of_train_validation_sets[ratio_idx] = train_validation_sets

        test = preprocessing.dataframe_to_numpy(observed_test)
        self.__X_test, self.__y_test = window_generator.create_window_dataset(
            test, self.config.input_length, self.config.output_length
        )

    # sourcery skip: snake-case-functions
    @property
    def X_test(self) -> npt.NDArray[np.float64]:
        """The input of the test dataset.

        Returns:
            The input of the test dataset.
        """
        if self.__X_test is None:
            self.prepare_data()
            return self.X_test
        return self.__X_test

    @property
    def y_test(self) -> npt.NDArray[np.float64]:
        """The output of the test dataset.

        Returns:
            The output of the test dataset.
        """
        if self.__y_test is None:
            self.prepare_data()
            return self.y_test
        return self.__y_test

    @property
    def list_of_train_validation_sets(
        self,
    ) -> list[list[dict[str, list[npt.NDArray[np.float64]]]]]:
        """Lists of train validation sets. One set for each ratio of synthethic to observed data.

        Returns:
            A list of list of dicts containing train and validation sets.
        """
        if self.__list_of_train_validation_sets == [[], []]:
            self.prepare_data()
            return self.__list_of_train_validation_sets
        return self.__list_of_train_validation_sets
