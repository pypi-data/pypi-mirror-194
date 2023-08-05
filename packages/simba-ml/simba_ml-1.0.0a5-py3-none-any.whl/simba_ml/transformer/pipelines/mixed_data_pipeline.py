"""Pipeline for running predictions."""
import argparse
import logging
import tomli

import dacite
import pandas as pd
from numpy import typing as npt
import numpy as np

from simba_ml.transformer.models import model as model_module
from simba_ml.transformer.models import factory
from simba_ml.transformer import plugin_loader
from simba_ml.transformer.config.mixed_data_pipeline import pipeline_config
from simba_ml.transformer.data_loader import mixed_data_loader
from simba_ml.transformer.metrics import metrics as metrics_module

logger = logging.getLogger(__name__)


def _model_config_factory(
    model_dict: dict[str, object], input_length: int, output_length: int
) -> model_module.Model:
    if not isinstance(model_dict["id"], str):
        raise TypeError("Model id must be a string.")
    model_id: str = model_dict["id"]
    del model_dict["id"]
    return factory.create(model_id, model_dict, input_length, output_length)


def __train_model_on_validation_sets(
    model: model_module.Model, train_validation_sets: list[dict[str, pd.DataFrame]]
) -> None:
    for i, train_validation_set in enumerate(train_validation_sets):
        logger.info("Training model: %s on cross-validation-set %d", model.name, i)
        model.train(train_validation_set["train"][i], train_validation_set["validation"][i])


def __evaluate_metrics(
    metrics: dict[str, metrics_module.Metric],
    y_test: npt.NDArray[np.float64],
    predictions: npt.NDArray[np.float64],
) -> dict[str, np.float64]:
    return {
        metric_id: metric_function(y_true=y_test, y_pred=predictions)
        for metric_id, metric_function in metrics.items()
    }


def main(config_path: str) -> dict[str, dict[str, dict[str, np.float64]]]:
    """Starts the pipeline.

    Args:
        config_path: path to the config file.

    Returns:
        Returns a dictionary which contains the evaluation results for each ratio for each models
    """
    # read in config and load defined plugins
    with open(config_path, mode="rb") as fp:
        config_json = tomli.load(fp)
    config = dacite.from_dict(data_class=pipeline_config.PipelineConfig, data=config_json, config=dacite.Config(strict=True))  # type: ignore
    plugin_loader.load_plugins(config.plugins)

    # instantiate models
    logging.info("Creating models...")
    models = [
        _model_config_factory(
            model, config.data.input_length, config.data.output_length
        )
        for model in config.models
    ]

    # create list of evaluation results for each ratio-run: {model, {metric, value}}
    evaluation_results: dict[str, dict[str, dict[str, np.float64]]] = {
        str(ratio): {} for ratio in config.data.ratios
    }

    # instantiate dataloader with config file
    dataloader = mixed_data_loader.MixedDataLoader(config.data)

    # train models on all defined ratios of synthethic to observed data
    for r, ratio in enumerate(config.data.ratios):
        for model in models:
            __train_model_on_validation_sets(model, dataloader.list_of_train_validation_sets[r])
            logger.info("Running prediction for %s", model.name)
            evaluation_results[str(ratio)][model.name] = __evaluate_metrics(
                config.metric_functions,
                dataloader.y_test,
                model.predict(dataloader.X_test),
            )

    return evaluation_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-path", type=str)
    args = parser.parse_args()

    logger.setLevel(logging.INFO)

    results = main(args.config_path)
    for result in results:
        logger.info(result)
