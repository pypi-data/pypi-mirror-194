"""Factory for creating a models."""
import dacite

from simba_ml.transformer import models


class ModelNotFoundError(Exception):
    """Raised when a model type is not found."""


model_config_creation_funcs: dict[str, tuple[type[models.model.ModelConfig], type[models.model.Model]]] = {}


def register(model_id: str, config_class: type[models.model.ModelConfig], model_class: type[models.model.Model]) -> None:
    """Register a new model type.

    Args:
        model_id: the model type to register.
        config_class: the configuration class for the model.
        model_class: the model class.
    """
    model_config_creation_funcs[model_id] = (config_class, model_class)


def unregister(model_id: str) -> None:
    """Unregister a model type.

    Args:
        model_id: the model type to unregister.
    """
    model_config_creation_funcs.pop(model_id, None)


def create(model_id: str, config: dict[str, object], input_length: int, output_length: int) -> models.model.Model:
    """Create a model of a specific type, given JSON data.

    Args:
        model_id: the model type to create.
        config: the JSON data to use to create the model.
        input_length: length of the input data.
        output_length: length of the output data.

    Returns:
        The created model if model can be created, None otherwise.

    Raises:
        ModelNotFoundError: if the model type is unknown.
    """
    try:
        config_class, Model_class = model_config_creation_funcs[model_id]
    except KeyError as e:
        raise ModelNotFoundError(f"Model type {model_id} not found") from e

    model_config: models.model.ModelConfig = dacite.from_dict(data_class=config_class, data=config, config=dacite.Config(strict=True))  # type: ignore
    model = Model_class(input_length, output_length, model_config)
    return model


register("DenseNeuralNetwork", models.dense_neural_network.DenseNeuralNetworkConfig, models.dense_neural_network.DenseNeuralNetwork)
register("AveragePredictor", models.average_predictor.AveragePredictorConfig, models.average_predictor.AveragePredictor)
register("LastValuePredictor", models.last_value_predictor.LastValuePredictorConfig, models.last_value_predictor.LastValuePredictor)
