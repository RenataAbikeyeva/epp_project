import pandas as pd
from criterion_functions import rosenbrock_v2
from criterion_functions import rotated_hyper_ellipsoid
from criterion_functions import sum_of_squares_v1
from criterion_functions import trid
from estimagic.optimization.optimize import minimize

# from criterion_functions import rosenbrock_v1
# from criterion_functions import sum_of_squares_v2

# from src.model_code.criterion_functions import sum_of_squares_v1


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

criteria = [sum_of_squares_v1, trid, rotated_hyper_ellipsoid, rosenbrock_v2]

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

constr_without_bounds = [constraints[2], constraints[3], constraints[4], constraints[9]]

# run the actual benchmark
results = []
for alg in algorithms:
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

    for constr, param in zip(constraints, start_params_constr):
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

        for crit in criteria:
            info, opt_params = minimize(
                crit,
                start_params,
                constraints=constr,
                algorithm=alg,
                algo_options=algo_options,
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

df.to_csv("11optimizers.csv", index=False)
