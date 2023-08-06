"""Introduces the epidemiological SIR model.

[SIR](https://medium.com/@shaliniharkar/sir-model-for-spread-of-disease-the-differential-equation-model-7e441e8636ab)
is a epidemiological model modeling the spread of deseases.
"""
import numpy as np
from simba_ml.simulation import constraints, distributions, generators
from simba_ml.simulation import kinetic_parameters as kinetic_parameters_module
from simba_ml.simulation import noisers
from simba_ml.simulation import sparsifier as sparsifier_module
from simba_ml.simulation import species, system_model

# -------------------------------------------
A = np.array([[1, 2], [4, 5]])
N = np.array([10, 20])

P = np.transpose(np.transpose(A) / A.sum(axis=1))

N_ij = P * N
N_j = N_ij.sum(axis=0)

Q = N_ij / N_j


# -------------------------------------------


name = "SIR"
specieses = [
    [
        species.Species(f"Suspectible_{i}_{j}", distributions.Constant(
            0.9), contained_in_output=False, min_value=0),
        species.Species(f"Infected_{i}_{j}",
                        distributions.Constant(0.1), min_value=0),
    ] for i in range(len(A)) for j in range(len(A))
]
specieses = [
    species for specieses in specieses for species in specieses]  # flatten

print(specieses[0].distribution.value)

# names = [species.name for species in specieses]
# print([species.distribution.value for species in specieses])

# print(np.array(names[::2]).reshape(len(A), len(A))))
# print(np.array(names[::2]).reshape(len(A), len(A)))

kinetic_parameters: dict[str, kinetic_parameters_module.KineticParameter] = {
    "beta": kinetic_parameters_module.ConstantKineticParameter(distributions.ContinuousUniformDistribution(0.1, 0.3)),
    "gamma": kinetic_parameters_module.ConstantKineticParameter(distributions.Constant(0.04)),
}

p_parameters: dict[str, kinetic_parameters_module.KineticParameter] = {
    f"P_{i}_{j}": kinetic_parameters_module.ConstantKineticParameter(distributions.Constant(P[(i, j)])) for i in range(len(A)) for j in range(len(A))
}

q_parameters: dict[str, kinetic_parameters_module.KineticParameter] = {
    f"Q_{i}_{j}": kinetic_parameters_module.ConstantKineticParameter(distributions.Constant(Q[(i, j)])) for i in range(len(A)) for j in range(len(A))
}

kinetic_parameters = kinetic_parameters | p_parameters | q_parameters


def deriv(_t: float, y: list[float], arguments: dict[str, float]) -> tuple[float, ...]:
    """Defines the derivative of the function at the point _.

    Args:
        y: Current y vector.
        arguments: Dictionary of arguments configuring the problem.

    Returns:
        Tuple[float, float, float]
    """
    # print(y)
    # print(arguments)
    print(_t)

    S = np.array(y[::2]).reshape(len(A), len(A))
    # print(S)
    I = np.array(y[1::2]).reshape(len(A), len(A))
    # print(I)

    ones = np.ones(len(A))

    lambda_home = arguments["beta"]/2 * (np.matmul(P * I, ones))
    lambda_work = np.transpose(
        arguments["beta"]/2 * np.transpose(np.matmul(ones, Q * I)))

    lambda_combined = lambda_home + lambda_work

    dS_dt = -lambda_combined * S
    dI_dt = lambda_combined * S - arguments["gamma"] * I

    return tuple(state[i] for state in zip(dS_dt.reshape(-1), dI_dt.reshape(-1)) for i in (0, 1))


noiser = noisers.AdditiveNoiser(distributions.LogNormalDistribution(0, 2))
sparsifier1 = sparsifier_module.ConstantSuffixRemover(
    n=5, epsilon=1, mode="absolute")
sparsifier2 = sparsifier_module.ConstantSuffixRemover(
    n=5, epsilon=0.1, mode="relative")
sparsifier = sparsifier_module.SequentialSparsifier(
    sparsifiers=[sparsifier1, sparsifier2])

sm = constraints.SpeciesValueTruncator(
    system_model.SystemModel(
        name,
        specieses,
        kinetic_parameters,
        deriv=deriv,
        # noiser=noiser,
        timestamps=distributions.Constant(1000)
    )
)

generators.TimeSeriesGenerator(sm).generate_csv()
