"""Provides a model, which predicts the last given input value."""
import dataclasses

import numpy as np
import numpy.typing as npt

from simba_ml.transformer.models import model


@dataclasses.dataclass
class LastValuePredictorConfig(model.ModelConfig):
    """Defines the configuration for the DenseNeuralNetwork."""
    name: str = "Last Value Predictor"


class LastValuePredictor(model.Model):
    """Defines a model, which predicts the previous value."""

    def train(self, train: list[npt.NDArray[np.float64]], val: list[npt.NDArray[np.float64]]) -> None:
        """Trains the model with the given data.

        Args:
            train: data, that can be used for training.
            val: data, that is used for validation.
        """

    def predict(self, data: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Predicts the next timestamps for every row.

        Args:
            data: 3 dimensional numpy array.
                First dimension contains time-series.
                Second dimension contains time steps of a time-series.
                Third dimension contains the attributes at a single timestep.

        Returns:
            A 3 dimensional numpy array, with the predicted values.

        Example:
            >>> import numpy as np
            >>> from simba_ml.transformer.models import last_value_predictor
            >>> train = np.array([[[1,2], [1,2]], [[2,5], [2,6]], [[10, 11], [12,12]]])
            >>> val = np.array([[[1,2], [1,2]], [[2,5], [2,6]], [[10, 11], [12,12]]])
            >>> train.shape
            (3, 2, 2)
            >>> config = last_value_predictor.LastValuePredictorConfig()
            >>> model = last_value_predictor.LastValuePredictor(2, 1, config)
            >>> model.train(train=train, val=val)
            >>> test_input = np.array([[[10, 10], [20, 20]], [[15, 15], [15, 16]]])
            >>> print(test_input)
            [[[10 10]
              [20 20]]
            <BLANKLINE>
             [[15 15]
              [15 16]]]
            >>> print(model.predict(test_input))
            [[[20 20]]
            <BLANKLINE>
             [[15 16]]]
        """
        self.validate_prediction_input(data)
        return np.array([[ts[-1] for _ in range(self.output_length)] for ts in data])
