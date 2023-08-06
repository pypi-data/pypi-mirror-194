"""Module containing preprocessing functionalities."""
import os
import random

import numpy as np
import numpy.typing as npt
import pandas as pd

random.seed(42)


def dataframes_from_csvs(path_to_csvs: str) -> list[pd.DataFrame]:
    """Reads all csv files in a given directory and returns a numpy array with the data. Constraint: defined folder must not be empty.

    Args:
        path_to_csvs: path to the directory containing the csv files.

    Raises:
        ValueError: if the given directory is empty.
        ValueError: if the given directory contains no csvs.

    Returns:
        data: numpy array containing the data.
    """
    if len(os.listdir(path_to_csvs)) == 0:
        raise ValueError("The given directory is empty.")
    if data_list := [pd.read_csv(path_to_csvs + file, header=0) for file in os.listdir(path_to_csvs) if file.endswith(".csv")]:
        return data_list
    raise ValueError("No csvs in the specified folder.")


def dataframe_to_numpy(data: list[pd.DataFrame]) -> list[npt.NDArray[np.float64]]:
    """Converts a list of dataframes to a list of numpy arrays.

    Args:
        data: list of dataframes.

    Returns:
        list of numpy arrays.
    """
    return [(df.to_numpy()).astype("float64") for df in data]


def train_test_split_vertical(data: list[pd.DataFrame], test_split: float, input_length: float)\
        -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """Splits a given dataframe in train, test and validations split.

    Args:
        data: List of time series.
        test_split: percentage of data that will be used for the test split.
        input_length: length of the input window.

    Returns:
        Tuple of train and test set.
    """
    test = []
    train = []
    for dataFrame in data:
        test_train_split = int(dataFrame.shape[0]*(1-test_split))
        train_validation_df = dataFrame.iloc[:test_train_split].reset_index(drop=True)
        train.append(train_validation_df)
        test.append(dataFrame.iloc[int(test_train_split-input_length):].reset_index(drop=True))
    return train, test


def train_test_split_horizontal(data: list[pd.DataFrame], test_split: float)\
        -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """Splits a given dataframe in train, test and validations split.

    Args:
        data: List of time series.
        test_split: percentage of data that will be used for the test split.

    Returns:
        Tuple of train and test set.
    """
    test = []
    train = []
    random.shuffle(data)
    total_data_len = len(data)
    test_train_split = int(-total_data_len*test_split)
    test = data[test_train_split:]
    train = data[:test_train_split]
    return train, test


def train_test_split(data: list[pd.DataFrame], test_split: float = 0.2, input_length: float = 0, split_axis: str = "vertical")\
        -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """Splits a given dataframe in train, test and validations split.

    Args:
        data: List of time series.
        test_split: percentage of data that will be used for the test split. Defaults to 0.2.
        input_length: length of the input window. Defaults to 0.
        split_axis: Axis along which the data will be split. Either "horizontal" "vertical". Defaults to "vertical".

    Returns:
        Tuple of train and test set.

    Raises:
        ValueError: if split_axis is not "horizontal" or "vertical".
    """
    if split_axis == "vertical":
        return train_test_split_vertical(data=data, test_split=test_split, input_length=input_length)
    if split_axis == "horizontal":
        return train_test_split_horizontal(data=data, test_split=test_split)
    raise ValueError("split_axis must be either 'horizontal' or 'vertical'.")


def train_validation_split_vertical(data: list[pd.DataFrame], k_cross_validation: int = 5, input_length: int = 0)\
        -> list[dict[str, list[pd.DataFrame]]]:
    """Splits a given dataframe vertically in train and validations split.

    Args:
        data: List of time series.
        k_cross_validation: Number of cross validation splits. Defaults to 5.
        input_length: length of the input window. Defaults to 0.

    Returns:
        train_validation_set: this set consist of a List with k cross validation sets,
            with a train set  and a validation set, each set is a List of Data Frame time series.
    """
    train_validation = [{"train": [], "validation": []} for _ in range(k_cross_validation)]  # type: list[dict[str, list[pd.DataFrame]]]
    for dataFrame in data:
        train_validation_split_point = dataFrame.shape[0]//(k_cross_validation+1)
        for i in range(k_cross_validation):
            train_validation[i]["train"].append(dataFrame.iloc[:train_validation_split_point*(i+1)].reset_index(drop=True))
            train_validation[i]["validation"].append(dataFrame.iloc[max(int(train_validation_split_point*(i+1) - input_length), 0):train_validation_split_point*(i+2)]
                                                     .reset_index(drop=True))
    return train_validation


def train_validation_split_horizontal(data: list[pd.DataFrame], k_cross_validation: int = 5)\
        -> list[dict[str, list[pd.DataFrame]]]:
    """Splits a given dataframe horizontally in train and validations split.

    Args:
        data: List of time series.
        k_cross_validation: Number of cross validation splits. Defaults to 5.

    Returns:
        A set consisting of a List with k cross validation sets,
            with a train set and a validation set, where each set is a List of Data Frame time series.
    """
    random.shuffle(data)
    train_validation = [{"train": [pd.DataFrame], "validation": [pd.DataFrame]} for _ in range(k_cross_validation)]
    train_validation_split_point = len(data)//k_cross_validation
    for i in range(k_cross_validation):
        train = data[:i*train_validation_split_point] + data[(i+1)*train_validation_split_point:]
        validation = data[i*train_validation_split_point:(i+1)*train_validation_split_point]
        train_validation[i]["train"] = train
        train_validation[i]["validation"] = validation
    return train_validation


def train_validation_split(data: list[pd.DataFrame], k_cross_validation: int = 5, input_length: int = 0, split_axis: str = "vertical")\
        -> list[dict[str, list[pd.DataFrame]]]:
    """Splits a given dataframe in train and validations split.

    Args:
        data: List of time series.
        k_cross_validation: Number of cross validation splits. Defaults to 5.
        input_length: length of the input window. Defaults to 0.
        split_axis: Axis along which the data will be split. Either "horizontal" "vertical". Defaults to "vertical".

    Returns:
        A set consisting of a List with k cross validation sets,
            with a train set and a validation set, where each set is a List of Data Frame time series.

    Raises:
        ValueError: if split_axis is not "horizontal" or "vertical".
    """
    if split_axis == "vertical":
        return train_validation_split_vertical(data=data, input_length=input_length, k_cross_validation=k_cross_validation)
    if split_axis == "horizontal":
        return train_validation_split_horizontal(data=data, k_cross_validation=k_cross_validation)
    raise ValueError("split_axis must be either 'horizontal' or 'vertical'.")
