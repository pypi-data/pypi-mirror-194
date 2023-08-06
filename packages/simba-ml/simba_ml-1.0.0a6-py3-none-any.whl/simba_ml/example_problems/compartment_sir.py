import numpy as np
from simba_ml.simulation import constraints, distributions, generators
from simba_ml.simulation import kinetic_parameters as kinetic_parameters_module
from simba_ml.simulation import noisers
from simba_ml.simulation import sparsifier as sparsifier_module
from simba_ml.simulation import species, system_model


A = np.array([[1, 2], [4, 5]])
N = np.array([10, 20])

P = np.transpose(np.transpose(A) / A.sum(axis=1))

N_ij = P * N
N_j = N_ij.sum(axis=0)

Q = N_ij / N_j


name = "Compartment_SIR"

specieses_to_flatten = [
    [
        species.Species(
            f"Suspectible_{i}_{j}",
            distributions.Constant(0.9),
            contained_in_output=False,
            min_value=0,
        ),
        species.Species(f"Infected_{i}_{j}", distributions.Constant(0.1), min_value=0),
    ]
    for i in range(len(A))
    for j in range(len(A))
]
specieses = flatten(specieses_to_flatten)

kinetic_parameters: dict[str, kinetic_parameters_module.KineticParameter] = {
    "beta": kinetic_parameters_module.DictBasedKineticParameter(
        {0: 0.05, 50: 0.1, 100: 0.3}
    ),
    "gamma": kinetic_parameters_module.ConstantKineticParameter(
        distributions.Constant(0.04)
    ),
    "p": kinetic_parameters_module.ConstantKineticParameter(distributions.Constant(P)),
    "q": kinetic_parameters_module.ConstantKineticParameter(distributions.Constant(Q)),
}


@y_as_numpy_array
def deriv(_t: float, y: np.typing.NDArray[np.float], arguments: dict[str, float]) -> tuple[float, ...]:
    """Defines the derivative of the function at the point _.

    Args:
        y: Current y vector.
        arguments: Dictionary of arguments configuring the problem.

    Returns:
        Tuple[float, float, float]
    """
    suspectible = np.array(y[::2]).reshape(len(A), len(A))
    infected = np.array(y[1::2]).reshape(len(A), len(A))

    ones = np.ones(len(A))

    lambda_home = arguments["beta"] / 2 * (np.matmul(P * infected, ones))
    lambda_work = np.transpose(
        arguments["beta"] / 2 * np.transpose(np.matmul(ones, Q * infected))
    )

    lambda_combined = lambda_home + lambda_work

    dS_dt = -lambda_combined * suspectible
    dI_dt = lambda_combined * suspectible - arguments["gamma"] * infected

    return tuple(
        state[i] for state in zip(dS_dt.reshape(-1), dI_dt.reshape(-1)) for i in (0, 1)
    )


noiser = noisers.AdditiveNoiser(distributions.LogNormalDistribution(0, 2))
sparsifier1 = sparsifier_module.ConstantSuffixRemover(n=5, epsilon=1, mode="absolute")
sparsifier2 = sparsifier_module.ConstantSuffixRemover(n=5, epsilon=0.1, mode="relative")
sparsifier = sparsifier_module.SequentialSparsifier(
    sparsifiers=[sparsifier1, sparsifier2]
)

sm = constraints.SpeciesValueTruncator(
    system_model.SystemModel(
        name,
        specieses,
        kinetic_parameters,
        deriv=deriv,
        timestamps=distributions.Constant(1000),
    )
)

generators.TimeSeriesGenerator(sm).generate_csv()


def flatten(unflattened_list: list[list[species.Species]]) -> list[species.Species]:
    """Flattens a list of lists.

    Args:
        unflattened_list: A list of lists of specieses.

    Returns:
        A flattened list of specieses.
    """
    return [item for sublist in unflattened_list for item in sublist]


def y_as_numpy_array(
    deriv: callable[[float, np.typing.NDArray[np.float], dict[str, float]], tuple[float, ...]],
    shape: tuple[int, ...],
) -> callable[[float, list[float], dict[str, float]], tuple[float]]:
    return lambda: tuple(deriv(0, np.zeros(shape), {}))
