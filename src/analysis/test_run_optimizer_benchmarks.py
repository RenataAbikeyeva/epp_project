from itertools import product

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal as aae
from numpy.testing import assert_array_almost_equal as aaae

true_df = pd.read_csv("true_value_21_opt.csv")
esti_df = pd.read_csv("21_optimizers.csv")

# Test to compare columns
@pytest.fixture
def true_value():
    true_value = true_df["value"]
    return true_value


@pytest.fixture
def calculated_value():
    calculated_value = esti_df["value"]
    return calculated_value


def test_optimizer_simple(true_value, calculated_value):
    aaae(true_value, calculated_value, decimal=5)


# Same test but with parametrization
test_cases = list(
    product(
        esti_df["algorithm"].unique().tolist(),
        esti_df["constraints"].unique().tolist(),
        esti_df["criterion"].unique().tolist(),
        esti_df["parameters"].unique().tolist(),
    )
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

    aae(true_value, calculated_value, decimal=2)
