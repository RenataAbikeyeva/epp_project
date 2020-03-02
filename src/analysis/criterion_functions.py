import numpy as np
import pandas as pd


def sum_of_squares_v1(params):
    """ Implement Sum of Squared Parameters function.

    Function description: https://www.sfu.ca/~ssurjano/sumsqu.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer:  Sum of Squared Parameters function output.

    """
    params["indexer"] = np.arange(1, len(params.index) + 1)
    return (params["indexer"] * params["value"] ** 2).sum()


def sum_of_squares_v2(params):
    """ Implement Sum of Squared Parameters function.

    Function description: https://www.sfu.ca/~ssurjano/sumsqu.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer: Sum of Squared Parameters function output.

    """
    val = pd.array([(i + 1) * i_val ** 2 for i, i_val in enumerate(params["value"])])

    return val.sum()


def trid(params):
    """ Implement Trid function.

    Function description: https://www.sfu.ca/~ssurjano/trid.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer:  Trid function output.

    """
    return ((params["value"] - 1) ** 2).sum() - (
        params["value"][1:] * params["value"][:-1].values
    ).sum()


def rotated_hyper_ellipsoid(params):
    """ Implement Rotated Hyper Ellipsoid function.

    Function description: https://www.sfu.ca/~ssurjano/rothyp.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer: Rotated Hyper Ellipsoid function output.

    """
    val = 0
    for i in range(len(params["value"])):
        val += (params["value"][: i + 1] ** 2).sum()

    return val


def rosenbrock_v1(params):
    """ Implement Rosenbrock function.

    Function description: https://www.sfu.ca/~ssurjano/rosen.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer: Rosenbrock function output.

    """
    val = 0
    for i in range(0, len(params["value"]) - 1):
        val_1 = 100 * (params["value"][i + 1] - params["value"][i] ** 2) ** 2
        val_2 = (params["value"][i] - 1) ** 2
        val += val_1 + val_2

    return val


def rosenbrock_v2(params):
    """ Implement Rosenbrock function.

    Function description: https://www.sfu.ca/~ssurjano/rosen.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer:  Rosenbrock function output.

    """
    #    params_np = params["value"].to_numpy()
    r1 = ((params["value"][1:] - params["value"][:-1].values ** 2) ** 2).sum() * 100
    r2 = ((params["value"][:-1] - 1) ** 2).sum()
    return r1 + r2
