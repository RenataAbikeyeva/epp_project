import numpy as np
import pandas as pd

params = pd.DataFrame([1, 2, 3], columns=["value"])


def sum_of_squares(params):
    """ Implement Sum of Squared Parameters function.

    Function description: https://www.sfu.ca/~ssurjano/sumsqu.html.

    Args:
        params (pandas.DataFrame): Must have the column "value" containing
        input values for parameters. Accepts arbitrary numbers of input values.

    Returns:
        integer:  Sum of Squared Parameters function output.

    """
    params["indexer"] = np.arange(
        1, len(params.index) + 1
    )  # what if params has a multi-index?
    return (params["indexer"] * params["value"] ** 2).sum()


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
