"""Provides a model, which predictits next timesteps from an arbitrary keras architecture."""
import abc
import dataclasses

import tensorflow as tf
import numpy as np
import numpy.typing as npt

from simba_ml.transformer.models import model
from simba_ml.transformer.data_loader import window_generator


@dataclasses.dataclass
class ArchitectureParams:
    """Defines the parameters for the architecture."""
    units: int = 32
    activation: str = "relu"
    num_species: int = 1


@dataclasses.dataclass
class TrainingParams:
    """Defines the parameters for the training."""
    epochs: int = 10
    patience: int = 5
    batch_size: int = 32
    validation_split: float = 0.2
    verbose: int = 0


@dataclasses.dataclass
class KerasModelConfig(model.ModelConfig):
    """Defines the configuration for the KerasModel."""
    architecture_params: ArchitectureParams = dataclasses.field(default_factory=ArchitectureParams)
    training_params: TrainingParams = dataclasses.field(default_factory=TrainingParams)
    name: str = "Keras Model"


class KerasModel(model.Model):
    """Defines a model, which uses a dense neural network to predict the next timestamps.

    Args:
        history: History documenting the training process of the model.
    """

    config: KerasModelConfig

    def __init__(self, input_length: int, output_length: int, config: KerasModelConfig) -> None:
        """Initializes the model.

        Args:
            input_length: length of the input data.
            output_length: length of the output data.
            config: configuration for the model.


        Raises:
            TypeError: if input_length or output_length is not an integer.
        """
        super().__init__(input_length, output_length, config)
        self.history = None
        self.model = self.get_model(input_length, output_length, config)

    @abc.abstractmethod
    def get_model(self, input_length: int, output_length: int, config: KerasModelConfig) -> tf.keras.Model:
        """Returns the model.

        Args:
            input_length: length of the input data.
            output_length: length of the output data.
            config: configuration for the model.
        """

    def train(self, train: list[npt.NDArray[np.float64]], val: list[npt.NDArray[np.float64]]) -> None:
        """Trains the model with the given data.

        Args:
            train: training data.
            val: validatation data
        """
        # compile and train the model
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                          patience=self.config.training_params.patience,
                                                          mode="min")
        self.model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mean_absolute_error"])
        # create window dataset
        X_train, y_train = window_generator.create_window_dataset(train, self.input_length, self.output_length)
        X_val, y_val = window_generator.create_window_dataset(val, self.input_length, self.output_length)
        self.history = self.model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            epochs=self.config.training_params.epochs,
            callbacks=[early_stopping],
            verbose=False
        )

    def predict(self, data: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Predicts the next timestamps for every row (time series).

        Args:
            data: np.array, where each dataframe is a time series.

        Returns:
            np.array, where each value is a time series.
        """
        return self.model.predict(data, verbose=False)
