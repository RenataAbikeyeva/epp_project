import json
import sys
from itertools import product

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal as aae

from bld.project_paths import project_paths_join as ppj

true_df = pd.read_csv(ppj("IN_ANALYSIS", "true_df.csv"))
esti_df = pd.read_csv(ppj("OUT_ANALYSIS", "21_calculated_df.csv"))
preci_df = pd.read_csv(ppj("IN_ANALYSIS", "precisions_21_df.csv"))


with open(ppj("IN_MODEL_SPECS", "constr_without_bounds_test.json"), "r") as read_file:
    constr_without_bounds_test = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "constr_trid.json"), "r") as read_file:
    constr_trid = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "constr_rosen.json"), "r") as read_file:
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
    if (origin == "pygmo") & (constraint in constr_without_bounds_test):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="Pygmo doesn't work without bounds. With bounds, \
                error for probability: incompatible with bounds. For\
                 increasing, decreasinng and linear, error: too many constraints."
            ),
        )
    elif (criterion == "trid") & (constraint in constr_trid):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="In true_df, Trid (decreasing, covariance and\
                 sdcorr constraints) set to NaN."
            ),
        )
    elif (criterion == "rosenbrock") & (constraint in constr_rosen):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="In true_df, Rosenbrock (probability and linear \
                constraints) set to NaN."
            ),
        )
    elif (
        (algorithm == "nlopt_cobyla")
        & (criterion == "rosenbrock")
        & (
            (constraint == "[{'loc': ['x_2', 'x_3'], 'type': 'increasing'}]")
            or (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'equality'}]")
        )
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, nlopt_cobyla fails for rosenbrock \
                (increasing and equality constraints)."
            ),
        )
    elif (
        (algorithm == "nlopt_neldermead")
        & (criterion == "rosenbrock")
        & (
            (constraint == "[{'loc': ['x_2', 'x_3'], 'type': 'increasing'}]")
            or (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'equality'}]")
        )
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, nlopt_neldermead fails for rosenbrock \
                (increasing and equality constraints)."
            ),
        )
    elif (algorithm == "nlopt_newuoa") & (
        (
            (criterion == "trid")
            & (constraint == "[{'loc': ['x_2', 'x_3'], 'type': 'increasing'}]")
        )
        or (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'equality'}]")
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, nlopt_newuoa fails for trid increasing \
                constraint, and with equality, fails all 4 criterion functions."
            ),
        )
    elif (algorithm == "nlopt_newuoa_bound") & (
        constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'equality'}]"
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, nlopt_newuoa_bound fails all 4 \
                criterion functions with equality constraint."
            ),
        )
    elif (
        (algorithm == "nlopt_sbplx")
        & (criterion == "rosenbrock")
        & (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'equality'}]")
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, nlopt_sbplx fails rosenbrock with \
                 equality constraint."
            ),
        )
    elif (
        (algorithm == "pygmo_bee_colony")
        & (criterion == "rosenbrock")
        & (
            (constraint == "[]")
            or (
                constraint
                == "[{'locs': ['x_1', 'x_2'], \
            'type': 'pairwise_equality'}]"
            )
        )
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, pygmo_bee_colony fails rosenbrock\
                 in unconstrained and pairwise_equality constraint."
            ),
        )
    elif (
        (algorithm == "pygmo_ihs")
        & (criterion == "rosenbrock")
        & (
            (constraint == "[]")
            or (
                constraint
                == "[{'locs': ['x_1', 'x_2'], \
            'type': 'pairwise_equality'}]"
            )
        )
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, pygmo_ihs fails rosenbrock in \
                unconstrained and pairwise_equality constraint."
            ),
        )
    elif (
        (algorithm == "pygmo_pso") & (criterion == "rosenbrock") & (constraint == "[]")
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, pygmo_pso fails rosenbrock\
                 in unconstrained case."
            ),
        )
    elif (
        (algorithm == "pygmo_pso_gen")
        & (criterion == "rosenbrock")
        & (constraint == "[]")
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, pygmo_pso_gen fails rosenbrock in unconstrained case."
            ),
        )
    elif (algorithm == "pygmo_sea") & (
        (
            (criterion == "rosenbrock")
            & (
                (constraint == "[]")
                or (
                    (constraint == "[{'loc': 'x_1', 'type': 'fixed', 'value': 1}]")
                    & (parameter == "x_3")
                )
                or (
                    constraint
                    == "[{'locs': ['x_1', 'x_2'], 'type': 'pairwise_equality'}]"
                )
            )
        )
        or (
            (criterion == "sum_of_squares")
            & (
                ((constraint == "[]") & (parameter == "x_1"))
                or (
                    (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'sdcorr'}]")
                    & (parameter == "x_2")
                )
            )
        )
        or (
            (criterion == "rotated_hyper_ellipsoid")
            & (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'covariance'}]")
            & (parameter == "x_1")
        )
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, pygmo_sea fails rosenbrock in\
                 unconstrained, fixed and pairwise_equality. Fails \
                 sum_of_squares in unconstrained and sdcorr. Fails \
                 rotated_hyper_ellipsoid with covariance constraint."
            ),
        )
    elif (
        (algorithm == "scipy_L-BFGS-B")
        & (criterion == "rosenbrock")
        & (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'equality'}]")
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, scipy_L-BFGS-B fails rosenbrock \
                with equality constraint."
            ),
        )
    elif (
        (algorithm == "scipy_TNC")
        & (criterion == "rosenbrock")
        & (constraint == "[{'loc': ['x_1', 'x_2', 'x_3'], 'type': 'equality'}]")
    ):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, scipy_TNC fails rosenbrock with equality constraint."
            ),
        )
    elif (algorithm == "nlopt_auglag") or (algorithm == "nlopt_auglag_eq"):
        test_cases[test_cases.index(case)] = pytest.param(
            algorithm,
            constraint,
            criterion,
            parameter,
            marks=pytest.mark.xfail(
                reason="At precision=2, nlopt_auglag and nlopt_auglag_eq \
                together pass only 58 out of 240 test cases. Hence, set both\
                 algorithms to xfail."
            ),
        )
    else:
        pass


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
    aae(calculated_value, true_value, decimal=precision)


if __name__ == "__main__":
    status = pytest.main([sys.argv[1]])
    sys.exit(status)
