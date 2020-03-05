import json
import sys

import numpy as np
import pandas as pd
from estimagic.optimization.optimize import minimize

from bld.project_paths import project_paths_join as ppj
from src.model_code.criterion_functions import rosenbrock
from src.model_code.criterion_functions import rotated_hyper_ellipsoid
from src.model_code.criterion_functions import sum_of_squares
from src.model_code.criterion_functions import trid

with open(ppj("IN_MODEL_SPECS", "constraints.json"), "r") as read_file:
    constraints = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "algorithms.json"), "r") as read_file:
    algorithms = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "start_params_constr.json"), "r") as read_file:
    start_params_constr = json.load(read_file)
with open(ppj("IN_MODEL_SPECS", "constr_without_bounds.json"), "r") as read_file:
    constr_without_bounds = json.load(read_file)


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


criteria = [sum_of_squares, trid, rotated_hyper_ellipsoid, rosenbrock]

results = []
if __name__ == "__main__":
    alg = sys.argv[1]
    algo_options = algo_options(alg)
    for constr, param in zip(constraints, start_params_constr):
        start_params = set_up_start_params(constr, param)
        for crit in criteria:
            origin, algo_name = alg.split("_", 1)
            if (origin == "pygmo") and (constr in constr_without_bounds):
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

df.to_csv(ppj("OUT_ANALYSIS", f"calculated_{alg}.csv"), index=False)
