"""Module for starting a prediction pipeline."""
import typing
import argparse
import logging

import pandas as pd

from simba_ml.prediction.time_series.pipelines import synthetic_data_pipeline

logger = logging.getLogger(__name__)


class Pipeline(typing.Protocol):
    """Protocol for a prediction pipeline."""

    def __call__(self, config_path: str) -> pd.DataFrame:
        """A Protocol is a method, which expects a config path.

        Args:
            config_path: path to the config file.
        """


PIPELINES: typing.Dict[str, Pipeline] = {
    "synthetic_data": synthetic_data_pipeline.main,
}


def main() -> None:
    """Start a prediction pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pipeline",
        choicse=PIPELINES.keys(),
        help="The name of the pipeline to run.",
    )
    parser.add_argument("--config-path", type=str, required=True)
    args = parser.parse_args()

    logger.info(PIPELINES[args.pipeline](args.config))


if __name__ == "__main__":
    main()
