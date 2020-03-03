# import sys
import numpy as np
import pandas as pd
from criterion_functions import rosenbrock
from criterion_functions import rotated_hyper_ellipsoid
from criterion_functions import sum_of_squares
from criterion_functions import trid
from estimagic.optimization.optimize import minimize


def algo_options(alg):
    origin, algo_name = alg.split("_", 1)
    if origin == "pygmo":
        if algo_name in ["ihs"]:
            algo_options = {"popsize": 1, "gen": 1000}
        elif algo_name in ["sea"]:
            algo_options = {"popsize": 5, "gen": 7000}
        else:
            algo_options = {"popsize": 30, "gen": 150}
    else:
        algo_options = {}

    return algo_options


def set_up_start_params(constr, param):
    if constr in constr_without_bounds:
        index = pd.Index(["x_1", "x_2", "x_3"], name="parameters")
        start_params = pd.DataFrame(index=index)
        start_params["value"] = param
    else:
        index = pd.Index(["x_1", "x_2", "x_3"], name="parameters")
        start_params = pd.DataFrame(index=index)
        start_params["value"] = param
        start_params["lower"] = -5
        start_params["upper"] = 5

    return start_params


constraints = [
    [],
    [{"loc": "x_1", "type": "fixed", "value": 1}],
    [{"loc": ["x_1", "x_2"], "type": "probability"}],
    [{"loc": ["x_2", "x_3"], "type": "increasing"}],
    [{"loc": ["x_1", "x_2"], "type": "decreasing"}],
    [{"loc": ["x_1", "x_2", "x_3"], "type": "equality"}],
    [{"locs": ["x_1", "x_2"], "type": "pairwise_equality"}],
    [{"loc": ["x_1", "x_2", "x_3"], "type": "covariance"}],
    [{"loc": ["x_1", "x_2", "x_3"], "type": "sdcorr"}],
    [{"loc": ["x_1", "x_2"], "type": "linear", "weights": [1, 2], "value": 4}],
]

algorithms = [
    "pygmo_de1220",
    "pygmo_sade",
    "pygmo_pso",
    "pygmo_pso_gen",
    "pygmo_bee_colony",
    "pygmo_cmaes",
    "pygmo_xnes",
    "pygmo_ihs",
    "pygmo_sea",
    "pygmo_de",
    "scipy_SLSQP",
    "scipy_TNC",
    "scipy_L-BFGS-B",
    "nlopt_auglag_eq",
    "nlopt_auglag",
    "nlopt_newuoa",
    "nlopt_newuoa_bound",
    "nlopt_neldermead",
    "nlopt_sbplx",
    "nlopt_cobyla",
    "nlopt_bobyqa",
]

criteria = [sum_of_squares, trid, rotated_hyper_ellipsoid, rosenbrock]

start_params_constr = [
    [1, 2, 3],
    [1, 3, 2],
    [0.5, 0.5, 3],
    [1, 2, 3],
    [2, 1, 3],
    [2, 2, 2],
    [2, 2, 3],
    [1, 1, 1],
    [1, 1, 1],
    [2, 1, 3],
]

constr_without_bounds = [
    [{"loc": ["x_1", "x_2"], "type": "probability"}],
    [{"loc": ["x_2", "x_3"], "type": "increasing"}],
    [{"loc": ["x_1", "x_2"], "type": "decreasing"}],
    [{"loc": ["x_1", "x_2"], "type": "linear", "weights": [1, 2], "value": 4}],
]
results = []
# if __name__ = "__main__":
#    alg = sys.argv[1]
for alg in algorithms:
    algo_options = algo_options(alg)
    for constr, param in zip(constraints, start_params_constr):
        start_params = set_up_start_params(constr, param)
        for crit in criteria:
            origin, algo_name = alg.split("_", 1)
            if origin == "pygmo" and constr in constr_without_bounds:
                index = pd.Index(["x_1", "x_2", "x_3"], name="parameters")
                opt_params = pd.DataFrame(index=index)
                opt_params["value"] = np.NaN

            else:
                info, opt_params = minimize(
                    crit,
                    start_params,
                    constraints=constr,
                    algorithm=alg,
                    algo_options=algo_options,
                    logging=False,
                )

            opt_params["algorithm"] = alg
            opt_params["constraints"] = str(constr)
            opt_params["criterion"] = crit.__name__
            opt_params.reset_index(inplace=True)
            opt_params = opt_params[
                ["criterion", "constraints", "parameters", "algorithm", "value"]
            ]

            results.append(opt_params)

df = pd.concat(results, sort=False)
df.reset_index(inplace=True, drop=True)

df.to_csv("calculated_21_df.csv", index=False)
