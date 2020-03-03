import json
from itertools import product

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal as aae

true_df = pd.read_csv("true_df.csv")
esti_df = pd.read_csv("calculated_21_df.csv")
preci_df = pd.read_csv("precisions_21_df.csv")

with open("constraints.json", "r") as read_file:
    constraints = json.load(read_file)
with open("constr_without_bounds.json", "r") as read_file:
    constr_without_bounds = json.load(read_file)
with open("constr_trid.json", "r") as read_file:
    constr_trid = json.load(read_file)
with open("constr_rosen.json", "r") as read_file:
    constr_rosen = json.load(read_file)

test_cases = list(
    product(
        esti_df["algorithm"].unique().tolist(),
        esti_df["constraints"].unique().tolist(),
        esti_df["criterion"].unique().tolist(),
        esti_df["parameters"].unique().tolist(),
    )
)


for case in test_cases:
    algorithm, constraint, criterion, parameter = case
    origin, algo_name = algorithm.split("_", 1)
    if (
        ((origin == "pygmo") & (constraint in constr_without_bounds))
        or ((criterion == "trid") & (constraint in constr_trid))
        or ((criterion == "rosenbrock") & (constraint in constr_rosen))
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm, constraint, criterion, parameter, marks=pytest.mark.xfail
        )


@pytest.mark.parametrize("algorithm, constraint, criterion, parameters", test_cases)
def test_optimizer(algorithm, constraint, criterion, parameters):
    true_value = true_df.set_index(["constraints", "criterion", "parameters"])
    true_value = true_value.loc[(constraint, criterion, parameters), "value"]
    calculated_value = esti_df.set_index(
        ["algorithm", "constraints", "criterion", "parameters"]
    )
    calculated_value = calculated_value.loc[
        (algorithm, constraint, criterion, parameters), "value"
    ]
    precision = preci_df.set_index(
        ["algorithm", "constraints", "criterion", "parameters"]
    )
    precision = precision.loc[
        (algorithm, constraint, criterion, parameters), "precision"
    ]
    aae(true_value, calculated_value, decimal=precision)
