"""Provides an abstract Model."""
import abc
import dataclasses

import numpy as np
import numpy.typing as npt

from simba_ml import error_handler


@dataclasses.dataclass
class ModelConfig:
    """Defines the configuration for the Model."""
    name: str = "Model"


class Model(abc.ABC):
    """Defines the abstract model."""

    @property
    def name(self) -> str:
        """Returns the models name.

        Returns:
            The models name.
        """
        return self.config.name

    def __init__(self, input_length: int, output_length: int, config: ModelConfig):
        """Inits the model.

        Args:
            input_length: length of the input data.
            output_length: length of the output data.
            config: configuration for the model.

        Raises:
            TypeError: if input_length or output_length is not an integer.
        """
        error_handler.confirm_param_is_int(param=input_length, param_name="input_length")
        error_handler.confirm_param_is_int(param=output_length, param_name="output_length")
        self.input_length = input_length
        self.output_length = output_length
        self.config = config

    @abc.abstractmethod
    def train(self, train: list[npt.NDArray[np.float64]], val: list[npt.NDArray[np.float64]]) -> None:
        """Trains the model with the given data.

        Args:
            train: training data.
            val: validation data
        """

    @abc.abstractmethod
    def predict(self, data: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Predicts the next timesteps.

        Args:
            data: 3 dimensional numpy array.
                First dimension contains time-series.
                Second dimension contains time steps of a time-series.
                Third dimension contains the attributes at a single timestep.
        """

    def validate_prediction_input(self, data: npt.NDArray[np.float64]) -> None:
        """Validates the input of the `predict` function.

        Args:
            data: a single dataframe containing the input data, where the output will be predicted.

        Raises:
            ValueError: if data has incorrect shape (row length does not equal )
        """
        if data.shape[1] != self.input_length:
            raise ValueError(f"Row length ({data.shape}) should be equal to input_length ({self.input_length})")
