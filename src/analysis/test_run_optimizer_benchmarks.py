# from itertools import product
import pandas as pd
import pytest
from numpy.testing import assert_array_almost_equal as aaae


true_df = pd.read_csv("true_value_1opt.csv")
esti_df = pd.read_csv("test_df_scipy.csv")


@pytest.fixture
def true_value():
    true_df = pd.read_csv("true_value_1opt.csv")
    true_value = true_df["value"]
    return true_value


@pytest.fixture
def calculated_value():
    esti_df = pd.read_csv("test_df_scipy.csv")
    calculated_value = esti_df["value"]
    return calculated_value


def test_optimizer(true_value, calculated_value):
    aaae(true_value, calculated_value, decimal=5)
