"""Module for starting a prediction pipeline."""
import typing
import argparse
import logging
import datetime

import pandas as pd

from simba_ml.prediction.time_series.pipelines import synthetic_data_pipeline

logger = logging.getLogger(__name__)


class Pipeline(typing.Protocol):
    """Protocol for a prediction pipeline."""

    def __call__(self, config_path: str) -> pd.DataFrame:
        """Runs the Pipeline.

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
        choices=PIPELINES.keys(),
        help="The name of the pipeline to run.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=f"results{datetime.datetime.now()}.csv",
        help="Path to the output file.",
    )
    parser.add_argument(
        "--config-path",
        type=str,
        default="config.toml",
        help="Path to the config file.",
    )
    args = parser.parse_args()

    results = PIPELINES[args.pipeline](args.config_path).T
    results.to_csv(args.output_path)


if __name__ == "__main__":
    main()
