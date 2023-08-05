"""Registers the keras models as plugins."""

from simba_ml.prediction.time_series.models import factory


from simba_ml.prediction.time_series.models.keras import dense_neural_network


def register() -> None:
    """Registers the keras models."""
    factory.register(
        "KerasDenseNeuralNetwork",
        dense_neural_network.DenseNeuralNetworkConfig,
        dense_neural_network.DenseNeuralNetwork,
    )
