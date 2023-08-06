"""Runs the application by starting the user interface."""
import typing
import argparse

from streamlit.web import bootstrap

from simba_ml import problem_viewer


def main() -> None:
    """Starts the user interface on a local webserver.

    The user interface is documented in `problem_viewer.py.`
    """
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--module", type=str, help="Module containing the PredictionTask"
    )
    my_args = parser.parse_args()
    file = problem_viewer.__file__
    flag_options: dict[str, typing.Any] = {}
    args = ["--module", my_args.module]
    bootstrap.run(file, None, args, flag_options)


if __name__ == "__main__":
    main()
