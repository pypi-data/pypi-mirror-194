"""Provides a model, which predicts the average of the train data."""
import dataclasses
import statistics

import numpy as np
import numpy.typing as npt

from simba_ml.transformer.models import model


@dataclasses.dataclass
class AveragePredictorConfig(model.ModelConfig):
    """Defines the configuration for the DenseNeuralNetwork."""
    name: str = "Average Predictor"


class AveragePredictor(model.Model):
    """Defines a model, which predicts the average of the train data."""

    def __init__(self, input_length: int, output_length: int, config: model.ModelConfig):
        """Inits the `AveragePredictor`.

        Args:
            input_length: the length of the input data.
            output_length: the length of the output data.
            config: the config for the model
        """
        super().__init__(input_length, output_length, config)
        self.avg = 0.0

    def train(self, train: list[npt.NDArray[np.float64]], val: list[npt.NDArray[np.float64]]) -> None:
        """Trains the model with the given data.

        Args:
            train: data, that can be used for training.
            val: data, that can be used for validation
        """
        self.avg = statistics.mean([df.mean().mean() for df in train])

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
            >>> from simba_ml.transformer.models import average_predictor
            >>> train = np.array([[[1,2], [1,2]], [[2,5], [2,6]], [[10, 11], [12,12]]])
            >>> val = np.array([[[1,2], [1,2]], [[2,5], [2,6]], [[10, 11], [12,12]]])

            >>> train.shape
            (3, 2, 2)
            >>> config = average_predictor.AveragePredictorConfig()
            >>> model = average_predictor.AveragePredictor(2, 1, config)
            >>> model.train(train=train, val=val)
            >>> model.avg
            5.5
            >>> test_input = np.array([[[10, 10], [20, 20]], [[15, 15], [15, 16]]])
            >>> print(test_input)
            [[[10 10]
              [20 20]]
            <BLANKLINE>
             [[15 15]
              [15 16]]]
            >>> print(model.predict(test_input))
            [[[5.5 5.5]]
            <BLANKLINE>
             [[5.5 5.5]]]


        """
        self.validate_prediction_input(data)
        return np.full((data.shape[0], self.output_length, data.shape[2]), self.avg)
