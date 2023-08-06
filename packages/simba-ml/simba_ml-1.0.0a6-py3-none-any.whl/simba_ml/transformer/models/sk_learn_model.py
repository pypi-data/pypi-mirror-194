"""Provides a model, which predicts next timesteps from an arbitrary sk learn architecture."""
import abc
import dataclasses

import sklearn as sk
import numpy as np
import numpy.typing as npt

from simba_ml.transformer.models import model
from simba_ml.transformer.data_loader import window_generator


@dataclasses.dataclass
class SkLearnModelConfig(model.ModelConfig):
    """Defines the configuration for the SkLearnModel."""
    name: str = "SkLearn Model"


class SkLearnModel(model.Model):
    """Defines a model, which uses the scikit learn library to predict the next timestamps.

    Args:
        config: configuration for the model.
    """

    config: SkLearnModelConfig

    def __init__(self, input_length: int, output_length: int, config: SkLearnModelConfig) -> None:
        """Initializes the model.

        Args:
            input_length: length of the input data.
            output_length: length of the output data.
            config: configuration for the model.

        Raises:
            TypeError: if input_length or output_length is not an integer.
        """
        super().__init__(input_length, output_length, config)
        self.model = self.get_model(config)

    @abc.abstractmethod
    def get_model(self, config: SkLearnModelConfig) -> sk.base.BaseEstimator:
        """Returns the model.

        Args:
            config: configuration for the model.
        """

    def train(self, train: list[npt.NDArray[np.float64]], val: list[npt.NDArray[np.float64]]) -> None:
        """Trains the model with the train data flattened to two dimensions.

        Args:
            train: training data.
            val: validation data
        """
        X_train, y_train = window_generator.create_window_dataset(train, self.input_length, self.output_length)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1] * X_train.shape[2]))
        y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1] * y_train.shape[2]))
        self.model.fit(X_train, y_train)

    def predict(self, data: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Predicts the next time steps.

        Args:
            data: 3 dimensional numpy array.

        Returns:
            The predicted next time steps.
        """
        original_data_shape = data.shape
        data = np.reshape(data, (data.shape[0], data.shape[1] * data.shape[2],))
        prediction = self.model.predict(data)
        prediction = np.reshape(prediction, (original_data_shape[0], self.output_length, original_data_shape[2]))
        return prediction
