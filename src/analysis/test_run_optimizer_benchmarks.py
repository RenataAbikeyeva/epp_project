from itertools import product

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal as aae

true_df = pd.read_csv("corrected_true_value_21_opt.csv")
esti_df = pd.read_csv("21_optimizers.csv")
preci_df = pd.read_csv("precisions_21.csv")

test_cases = list(
    product(
        esti_df["algorithm"].unique().tolist(),
        esti_df["constraints"].unique().tolist(),
        esti_df["criterion"].unique().tolist(),
        esti_df["parameters"].unique().tolist(),
    )
)

list_of_constraints = esti_df["constraints"].unique().tolist()

constr_without_bounds = [
    list_of_constraints[2],
    list_of_constraints[9],
    list_of_constraints[3],
    list_of_constraints[4],
]

constr_trid = [
    list_of_constraints[4],
    list_of_constraints[7],
    list_of_constraints[8],
]

constr_rosen = [
    list_of_constraints[2],
    list_of_constraints[9],
]

for tuple in test_cases:
    origin, algo_name = tuple[0].split("_", 1)
    if (
        ((origin == "pygmo") & (tuple[1] in constr_without_bounds))
        or ((tuple[2] == "trid") & (tuple[1] in constr_trid))
        or ((tuple[2] == "rosenbrock_v2") & (tuple[1] in constr_rosen))
    ):
        test_cases[test_cases.index(tuple)] = pytest.param(
            tuple[0], tuple[1], tuple[2], tuple[3], marks=pytest.mark.xfail
        )


@pytest.mark.parametrize("algorithm, constraint, criterion, parameters", test_cases)
def test_optimizer(algorithm, constraint, criterion, parameters):
    true_value = true_df.loc[
        (true_df["algorithm"] == "true_result")
        & (true_df["constraints"] == constraint)
        & (true_df["criterion"] == criterion)
        & (true_df["parameters"] == parameters),
        "value",
    ].iloc[0]

    calculated_value = esti_df.loc[
        (esti_df["algorithm"] == algorithm)
        & (esti_df["constraints"] == constraint)
        & (esti_df["criterion"] == criterion)
        & (esti_df["parameters"] == parameters),
        "value",
    ].iloc[0]

    precision = preci_df.loc[
        (preci_df["algorithm"] == algorithm)
        & (preci_df["constraints"] == constraint)
        & (preci_df["criterion"] == criterion)
        & (preci_df["parameters"] == parameters),
        "precision",
    ].iloc[0]

    aae(true_value, calculated_value, decimal=precision)
