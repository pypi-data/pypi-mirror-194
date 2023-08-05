"""Provides a model, which predictits next steps with a dense architecture."""
import dataclasses

import tensorflow as tf

from simba_ml.transformer.models import keras_model


@dataclasses.dataclass
class DenseNeuralNetworkConfig(keras_model.KerasModelConfig):
    """Defines the configuration for the DenseNeuralNetwork."""
    name: str = "Dense Neural Network"


class DenseNeuralNetwork(keras_model.KerasModel):
    """Defines a model, which uses a dense neural network to predict the next timestamps.

    Args:
        history: History documenting the training process of the model.
    """

    def get_model(self, input_length: int, output_length: int, config: keras_model.KerasModelConfig) -> tf.keras.Model:
        """Returns the model.

        Args:
            input_length: length of the input data.
            output_length: length of the output data.
            config: configuration for the model.

        Returns:
            The uncompiled model.
        """
        return tf.keras.Sequential([
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=32, activation="relu"),
            tf.keras.layers.Dense(units=output_length * config.architecture_params.num_species),
            tf.keras.layers.Reshape([output_length, -1])])
