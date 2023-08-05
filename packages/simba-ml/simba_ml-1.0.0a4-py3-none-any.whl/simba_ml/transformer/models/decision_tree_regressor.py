"""Provides a model, which predicts next timesteps from with a decision tree regressor."""
import enum
import sklearn as sk
from sklearn import tree

from simba_ml.transformer.models import sk_learn_model


class Criterion(enum.Enum):
    """The function to measure the quality of a split."""
    squared_error = 'squared_error'
    """Mean squared error, which is equal to variance reduction as feature selection criterion and minimizes the L2 loss using the mean of each terminal node."""
    friedman_mse = 'friedman_mse'
    """Mean squared error with Friedman's improvement score, which uses mean squared error with Friedman's improvement score for potential splits."""
    absolute_error = 'absolute_error'
    """mean absolute error for the mean absolute error, which minimizes the L1 loss using the median of each terminal node."""
    poisson = 'poisson'
    """reduction in Poisson deviance."""


class Splitter(enum.Enum):
    """The strategy used to choose the split at each node."""
    best = 'best'
    """Chooses always the best split."""
    random = 'random'
    """Choose randomly from the distribution of the used criterion."""


class DecisionTreeRegressorConfig(sk_learn_model.SkLearnModelConfig):
    """Defines the configuration for the DecisionTreeRegressor."""
    name: str = 'Decision Tree Regressor'
    criterion: Criterion = Criterion.squared_error
    splitter: Splitter = Splitter.best


class DecisionTreeRegressorModel(sk_learn_model.SkLearnModel):
    """Defines a model, which uses a decision tree regressor to predict the next timestamps."""

    def __init__(self, input_length: int, output_length: int, config: DecisionTreeRegressorConfig) -> None:
        """Initializes the configuration for the DecisionTreeRegressor.

        Args:
            input_length: length of the input data.
            output_length: length of the output data.
            config: configuration for the model.
        """
        super().__init__(input_length=input_length, output_length=output_length, config=config)

    def get_model(self, config: DecisionTreeRegressorConfig) -> sk.base.BaseEstimator:  # type: ignore
        """Returns the model.

        Args:
            config: configuration for the model.

        Returns:
            The model.
        """
        return tree.DecisionTreeRegressor(criterion=config.criterion.value, splitter=config.splitter.value)
