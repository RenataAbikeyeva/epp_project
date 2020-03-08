import numpy as np


def sum_of_squares(params):
    """ Implement Sum of Squared Parameters function.

    Function description: https://www.sfu.ca/~ssurjano/sumsqu.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer:  Sum of Squared Parameters function output.

    """
    params["multiplier"] = np.arange(1, len(params.index) + 1)
    return (params["multiplier"] * params["value"] ** 2).sum()


def trid(params):
    """ Implement Trid function.

    Function description: https://www.sfu.ca/~ssurjano/trid.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer:  Trid function output.

    """
    params_np = params["value"].to_numpy()
    return ((params["value"] - 1) ** 2).sum() - (
        params["value"][1:] * params_np[:-1]
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


def rosenbrock(params):
    """ Implement Rosenbrock function.

    Function description: https://www.sfu.ca/~ssurjano/rosen.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer:  Rosenbrock function output.

    """
    params_np = params["value"].to_numpy()
    r1 = ((params_np[1:] - params_np[:-1] ** 2) ** 2).sum() * 100
    r2 = ((params_np[:-1] - 1) ** 2).sum()
    return r1 + r2
