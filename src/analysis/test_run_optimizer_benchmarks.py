import glob
import json
from itertools import product

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal as aae

from bld.project_paths import project_paths_join as ppj

true_df = pd.read_csv(ppj("IN_ANALYSIS", "true_df.csv"))
# esti_df = pd.read_csv(ppj("IN_ANALYSIS", "calculated_21_df.csv"))
preci_df = pd.read_csv(ppj("IN_ANALYSIS", "precisions_21_df.csv"))

with open(ppj("IN_MODEL_SPECS", "algorithms.json"), "r") as read_file:
    algorithms = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "constraints.json"), "r") as read_file:
    constraints = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "constr_without_bounds_test.json"), "r") as read_file:
    constr_without_bounds_test = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "constr_trid.json"), "r") as read_file:
    constr_trid = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "constr_rosen.json"), "r") as read_file:
    constr_rosen = json.load(read_file)

path = ppj("OUT_ANALYSIS", "*.csv")
all_calculated_df = glob.glob(path)
esti_list = []
for calculated_df in all_calculated_df:
    calculated_alg_df = pd.read_csv(calculated_df, index_col=None)
    esti_list.append(calculated_alg_df)
esti_df = pd.concat(esti_list, sort=False)
esti_df.reset_index(inplace=True, drop=True)
# The order of algorithms is different from the order of algorithms in a list "algorithms".
esti_df.to_csv(ppj("OUT_ANALYSIS", "calculated_21_df.csv"), index=False)

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
        ((origin == "pygmo") & (constraint in constr_without_bounds_test))
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
