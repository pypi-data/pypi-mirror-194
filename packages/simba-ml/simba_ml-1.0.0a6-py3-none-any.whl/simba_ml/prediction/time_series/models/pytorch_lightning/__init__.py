"""Registers the pytorch lightning models as plugins."""

from simba_ml.prediction.time_series.models import factory


from simba_ml.prediction.time_series.models.pytorch_lightning import (
    dense_neural_network,
)


def register() -> None:
    """Registers the pytorch lightning models."""
    factory.register(
        "PytorchLightningDenseNeuralNetwork",
        dense_neural_network.DenseNeuralNetworkConfig,
        dense_neural_network.DenseNeuralNetwork,
    )
